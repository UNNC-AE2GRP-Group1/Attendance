from django.db import models
from django.utils import timezone
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from datetime import date, timedelta

from student.models import Student
from session.models import Module

# todo: review
class EC(models.Model):
    modules = models.ManyToManyField(Module, blank=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    from_time = models.DateTimeField(default = timezone.now)
    due_date = models.DateTimeField(default = timezone.now)
    EXAM = 'E'
    COURSEWORK = 'C'
    PLACEMENT = 'P'
    assessment = (
        (EXAM,'Exam'),
        (COURSEWORK,'coursework'),
        (PLACEMENT,'placement')
    )
    assessment_kind = models.CharField(max_length=1, choices=assessment, editable=True)
    APPROVED = 'A'
    DISAPPROVED = 'D'
    WAITING = 'W'
    EC_approved = (
        (APPROVED,'Approved'),
        (DISAPPROVED,'Disapproved'),
        (WAITING,'Waiting')
    )
    EC_status = models.CharField(max_length=1, choices=EC_approved, default=WAITING, editable=True)
    comment = models.TextField(verbose_name="Comment for Approval/Disapproval")
    
    def __str__(self):
        return '{}{}{}{}{}'.format(self.student, self.modules, self.from_time, self.due_date, self.EC_status)

    def approve(self):
        """Mark the EC application as approved and save the status.
        """
        status = self.get_status()
        assert(status == self.DISAPPROVED or status == self.WAITING)

        self.status = APPROVED
        self.save()

    def disapprove(self):
        """Mark the EC application as disapproved and save the status.
        """
        status = self.get_status()
        assert(status == self.APPROVED or status == self.WAITING)

        self.status = DISAPPROVED
        self.save()



class Absence_Form(models.Model):
    modules = models.ManyToManyField(Module, blank=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    APPROVED = 'A'
    DISAPPROVED = 'D'
    WAITING = 'W'
    Absence_approved = (
        (APPROVED,'Approved'),
        (DISAPPROVED,'Disapproved'),
        (WAITING,'Waiting')
    )
    Absence_status = models.CharField(max_length=1, choices=Absence_approved, default=WAITING, editable=True)
