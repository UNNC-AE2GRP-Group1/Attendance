from django.db import models
from django.utils import timezone
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.db.models import Avg

from student.models import Student

# Create your models here.

class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8)
    academic_year = models.SmallIntegerField()
    convenors = models.ManyToManyField(User, related_name='convenors', blank=True)
    assistants = models.ManyToManyField(User, related_name='assistants', blank=True)
    students = models.ManyToManyField(Student, through='Enrollment', blank=True)
    attendance_rate = models.FloatField(null=True)

    def __str__(self):
        return self.name + ' (' + str(self.academic_year) + ')'

    def update_attendance_rate(self):
        session_avg_rate = self.session_set\
            .filter(attendance_rate__isnull=False)\
            .aggregate(Avg('attendance_rate'))
        self.attendance_rate = session_avg_rate['attendance_rate__avg']
        self.save()
        

# todo: 
class Enrollment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    date_enrolled = models.DateField(default=date.today)
    date_unenrolled = models.DateField(default=date.today)


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

    SCHEDULED = 'S'
    IN_PROGRESS = 'P'
    FINISHED = 'F'
    CANCELLED = 'C'
    SESSION_STATUSES = (
        (SCHEDULED, 'Scheduled'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
        (CANCELLED, 'Cancelled'),
    )
    status = models.CharField(max_length=1, choices=SESSION_STATUSES, default=SCHEDULED)
    attendance_recorded = models.BooleanField(default=False)
    attendance_rate = models.FloatField(null=True)

    def __str__(self):
        ret = ''
        ret += '[' + str(self.time) + ']'   # time
        ret += '[' + self.type + ']'        # type
        ret += ' '
        ret += str(self.module)             # module
        return ret


class Attendee(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    presented = models.BooleanField()
    comment = models.TextField()

    # todo: potential performance issue when amount entries are large
    def __str__(self):
        return self.student.get_full_name() + ' from ' + str(self.session.module)
