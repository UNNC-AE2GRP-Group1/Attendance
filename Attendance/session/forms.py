from django.forms import ModelForm
from django import forms
import datetime
from .models import *

class ModuleCreateForm(ModelForm):
    class Meta:
        model = Module
        exclude = ['students', 'attendance_rate']

class SessionCreateForm(ModelForm):
    repeat_for_weeks = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = Session
        fields = ['time', 'duration', 'place', 'type', 'repeat_for_weeks']
