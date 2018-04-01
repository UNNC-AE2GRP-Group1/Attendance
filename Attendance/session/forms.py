from django.forms import ModelForm
from django import forms
import datetime
from .models import *

class ModuleCreateForm(ModelForm):
    class Meta:
        model = Module
        exclude = ['students', 'attendance_rate']

class SessionCreateForm(ModelForm):
    repeat = forms.BooleanField()
    repeat_times = forms.IntegerField(min_value=1)

    class Meta:
        model = Session
        fields = ['time', 'duration', 'place', 'type', 'repeat', 'repeat_times']
