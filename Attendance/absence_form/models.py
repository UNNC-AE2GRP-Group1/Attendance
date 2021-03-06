from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from datetime import date, timedelta

from student.models import Student
from session.models import Module

class Application(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    ABSENCE_Y1 = 'A1'
    ABSENCE_Y2P = 'A2'
    EXT_CIRCUMSTANCE = 'EC'
    APPLICATION_TYPE = (
        (ABSENCE_Y1, 'Absence form for Year 1'),
        (ABSENCE_Y2P, 'Absence form for Year 2+'),
        (EXT_CIRCUMSTANCE, 'Extenuating Circumstance'),
    )
    type = models.CharField(max_length=2, choices=APPLICATION_TYPE)

    identifier = models.CharField(max_length=10, blank=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    from_date = models.DateTimeField(null=True)
    to_date = models.DateTimeField(null=True)

    APPROVED = 'A'
    DISAPPROVED = 'D'
    PENDING = 'P'
    APPROVAL_STATUS = (
        (APPROVED, 'Approved'),
        (DISAPPROVED, 'Disapproved'),
        (PENDING, 'Pending')
    )
    status = models.CharField(max_length=1, choices=APPROVAL_STATUS)

    comment = models.TextField(blank=True)

    def __str__(self):
        return '[{}] {}'.format(self.get_status_display(), self.student)

class Detail(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    

class Appeal(models.Model):
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=Application.APPROVAL_STATUS)
    comment = models.TextField(blank=True)
