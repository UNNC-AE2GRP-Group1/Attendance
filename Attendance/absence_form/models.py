from django.db import models
from django.utils import timezone
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from datetime import date, timedelta

from student.models import Student
from session.models import Module
from session.models import Enrollment

# todo: review
class EC(models.Model):
    modules = models.ManyToManyField(Module, blank=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    from_date = models.DateTimeField(default = timezone.now)
    duration = models.DurationField(default=timedelta(hours=1))
    EXAM = 'E'
    COURSEWORK = 'C'
    PLACEMENT = 'P'
    assessment = (
        (EXAM,'Exam'),
        (COURSEWORK,'coursework'),
        (PLACEMENT,'placement')
    )
    APPROVED = 'A'
    DISAPPROVED = 'D'
    WAITING = 'W'
    EC_approved = (
        (APPROVED,'Approved'),
        (DISAPPROVED,'Disapproved'),
        (WAITING,'Waiting')
    )
    EC_status = models.CharField(max_length=1, choices=EC_approved, default=WAITING, editable=True)
    
    def __str__(self):
        return self.student.get_full_name() + str(self.module) + str(self.date) + self.assessment + self.EC_approved

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
