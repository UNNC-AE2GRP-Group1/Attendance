from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from datetime import date, timedelta

from student.models import Student
from session.models import Module

# todo: review
class Ec(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    comment = models.TextField(verbose_name="Comment for Approval/Disapproval")
    submit_date = models.DateTimeField(default = timezone.now)
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
        return '({}) comment:{} {} status:{}'.format(self.student, self.comment, self.submit_date, self.EC_status)
    

class EcDetail(models.Model):
    Ec = models.ForeignKey(Ec, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, blank=True, on_delete=models.PROTECT)
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
    
    def __str__(self):
        return 'Module:{} Duration: (from {} to {}) Assessment:{}'.format(self.module, self.from_time, self.due_date, self.assessment_kind)

class EcAppeal(models.Model):
    EcDetail = models.ForeignKey(EcDetail, on_delete=models.PROTECT)
    time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=Ec.EC_approved, default=Ec.WAITING, editable=True)


class AbsenceForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    comment = models.TextField(verbose_name="Comment for Approval/Disapproval")
    submit_date = models.DateTimeField(default = timezone.now)
    APPROVED = 'A'
    DISAPPROVED = 'D'
    WAITING = 'W'
    AbsenceForm_approved = (
        (APPROVED,'Approved'),
        (DISAPPROVED,'Disapproved'),
        (WAITING,'Waiting')
    )
    AbsenceForm_status = models.CharField(max_length=1, choices=AbsenceForm_approved, default=WAITING, editable=True)
    def __str__(self):
        return '({}) comment:{} {} status:{}'.format(self.student, self.comment, self.submit_date, self.AbsenceForm_status)
    

class AbsenceDetail(models.Model):
    AbsenceForm = models.ForeignKey(AbsenceForm, on_delete=models.PROTECT)
    module = models.ForeignKey(Module, blank=True, on_delete=models.PROTECT)
    from_time = models.DateTimeField(default = timezone.now)
    due_date = models.DateTimeField(default = timezone.now)
    
    def __str__(self):
        return 'Module:{} Duration: (from {} to {})'.format(self.module, self.from_time, self.due_date)

class AbsenceAppeal(models.Model):
    AbsenceDetail = models.ForeignKey(AbsenceDetail, on_delete=models.PROTECT)
    time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=AbsenceForm.AbsenceForm_approved, default=AbsenceForm.WAITING, editable=True)
