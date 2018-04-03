from io import BytesIO
from datetime import date, timedelta
from django.db import models
from django.utils import timezone
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.core.validators import MaxValueValidator, MinValueValidator
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from student.models import Student

# Create your models here.

def getyear():
    return timezone.now().year

class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8)
    academic_year = models.SmallIntegerField(validators=[
        MaxValueValidator(3881),
        MinValueValidator(1881)
    ], default=getyear)
    convenors = models.ManyToManyField(User, related_name='convenors', blank=True)
    assistants = models.ManyToManyField(User, related_name='assistants', blank=True)
    students = models.ManyToManyField(Student, blank=True)
    attendance_rate = models.FloatField(null=True, editable=False)

    def __str__(self):
        return '{} ({})'.format(self.name, self.academic_year)

    # returns: conflicted Student objects
    def batch_enroll_from_csv(self, student_reader):
        # todo: make column name more explicit
        # the students in the uploaded list can be:
        # - not in the student db table
        # - the same as in the table
        # - same id with different name
        uploaded_dict = {
            row[0]: Student(
                student_id=row[0],
                first_name=row[1],
                last_name=row[2],
            )
            for row in student_reader
        }
        # find out conflicts -> report
        # find out identical -> add to student list
        # find out new students -> create & add
        conflicts_models = []
        identical_dict = {}
        # fetch old information and compare
        existing_students = Student.objects.filter(student_id__in=uploaded_dict.keys())
        for s in existing_students:
            new_info = uploaded_dict.get(s.student_id)
            # the existing student must also be in the uploaded_dict
            assert(new_info is not None)
            # conflicts
            if s.first_name != new_info.first_name or s.last_name != new_info.last_name:
                conflicts_models.append(s)
            # exactly the same
            else:
                identical_dict[s.student_id] = new_info

        if not conflicts_models:
            # if their is no conflict, uploaded_dict = new_student_models + identical_models
            new_student_models = [uploaded_dict[id] for id in set(uploaded_dict) - set(identical_dict)]
            Student.objects.bulk_create(new_student_models)
            new_students_saved = Student.objects.filter(student_id__in=uploaded_dict.keys())
            self.students.add(*new_students_saved)

        return conflicts_models

    def calculate_attendance_rate(self):
        """Calculate the average attendance rate from all sessions whose
        attendance records are completed.
        The instance must be saved from otherwhere afterwards.

        Call this after updating the attendance rate of a session.
        It should be not be called from Session.update_attendance_rate()
        because when several sessions from a module are updated together,
        doing the calculation after each update will be inefficient.
        """
        session_avg_rate = self.session_set\
            .filter(attendance_rate__isnull=False)\
            .aggregate(Avg('attendance_rate'))
        self.attendance_rate = session_avg_rate['attendance_rate__avg']
        assert(self.attendance_rate != None)


class Session(models.Model):
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    time = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(default=timedelta(hours=1))
    place = models.CharField(max_length=127)

    LAB = 'A'
    LECTURE = 'E'
    SESSION_TYPES = (
        (LAB, 'Lab'),
        (LECTURE, 'Lecture'),
    )
    type = models.CharField(max_length=1, choices=SESSION_TYPES)

    # todo: when to switch to I and F status?
    SCHEDULED = 'S'
    PENDING = 'P'       # prepare: S -> P
    IN_PROGRESS = 'I'   # implicit, when now() is between time and time + duration
    FINISHED = 'F'      # implicit, when now() > time + duration
    CANCELLED = 'C'
    SESSION_STATUSES = (
        (SCHEDULED, 'Scheduled'),
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
        (CANCELLED, 'Cancelled'),
    )
    # this field does not change automatically with time, thus it can only be
    # S/P/C. use get_status() to get the logical status instead.
    status = models.CharField(max_length=1, choices=SESSION_STATUSES, default=SCHEDULED, editable=False)
    attendance_recorded = models.BooleanField(default=False, editable=False)
    attendance_rate = models.FloatField(null=True, editable=False)

    def __str__(self):
        return '[{}][{}] {}'.format(self.time, self.get_type_display(), self.module)

    def cancel(self):
        """Mark the session as cancelled and save the status.
        """
        status = self.get_status()
        assert(status == self.SCHEDULED or status == self.PENDING)

        self.status = CANCELLED
        self.save()

    def get_status(self):
        """Get the logical status of the session including IN_PROGRESS and FINISHED,
        the status will be updated according to current time without saving.
        """
        now = timezone.now()
        if now >= self.time:
            if now < self.time + self.duration:
                self.status = self.IN_PROGRESS
            else:
                self.status = self.FINISHED
        return self.status

    def prepare(self):
        """Initialize attendee list using the student list of the module of this session,
        then change the status from scheduled to pending.
        The attendee list can now be edited, and the signature sheet is available for
        download.
        """
        assert(self.status == self.SCHEDULED)

        student_list = self.module.students.all()
        attendee_list = []
        for s in student_list:
            attendee_list.append(Attendee(session=self, student=s))
        Attendee.objects.bulk_create(attendee_list)

        self.status = self.PENDING

    # todo
    # https://assist-software.net/blog/how-create-pdf-files-python-django-application-using-reportlab
    def get_signature_sheet_pdf(self):
        self.prepare()
        buffer = BytesIO()
        # set some characteristics for pdf document
        doc = SimpleDocTemplate(
            buffer,
            rightMargin=30,
            leftMargin=40,
            topMargin=40,
            bottomMargin=30,
            pagesize=A4
        )
        # a collection of styles offer by the library
        styles = getSampleStyleSheet()
        # add custom paragraph style
        styles.add(ParagraphStyle(
            name="TableHeader", fontSize=11, alignment=TA_CENTER))
        styles.add(ParagraphStyle(
            name="ParagraphTitle", fontSize=11, alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(
            name="Justify", alignment=TA_JUSTIFY))
        # list used for elements added into document
        data = []
        data.append(Paragraph("{0} Signature Sheet".format(self.module), styles['h2']))
        data.append(Paragraph("Time: {0} Place: {1}".format(
            self.time.strftime('%a, %d %b %Y %H:%M'),
            self.place
        ), styles['h2']))
        # insert a blank space
        data.append(Spacer(1, 12))
        table_data = []
        # table header
        table_data.append([
            Paragraph('Student Id', styles['TableHeader']),
            Paragraph('First Name', styles['TableHeader']),
            Paragraph('Last Name', styles['TableHeader']),
            Paragraph('Signature', styles['TableHeader']),
        ])
        for a in self.attendee_set.prefetch_related('student').all():
            s = a.student
            # add a row to table
            table_data.append([
                s.student_id,
                s.first_name,
                s.last_name,
                '',
            ])
        # create table
        wh_table = Table(table_data, colWidths=[doc.width/4.0]*4)
        wh_table.hAlign = 'LEFT'
        wh_table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
        data.append(wh_table)
        # create document
        doc.build(data)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def calculate_attendance_rate(self):
        """Calculate the attendance rate from the attendance record.
        The instance must be saved from otherwhere afterwards.
        Call this when the attendance record is saved for the first time or updated.
        """
        assert(self.attendance_recorded == True)

        total_attendees = self.attendee_set.all().count()
        attended = self.attendee_set\
            .filter(presented=True)\
            .count()
        self.attendance_rate = attended / total_attendees


class Attendee(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    presented = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    # todo: potential performance issue when amount entries are large
    def __str__(self):
        return '{} from {}'.format(self.student.get_full_name(), self.session.module)
