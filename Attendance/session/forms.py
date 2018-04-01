from django import forms
from django.forms import ModelForm
import datetime
from .models import *

class ModuleCreateForm(ModelForm):
    class Meta:
        model = Module
        exclude = ['students', 'attendance_rate']

class SessionCreateForm(forms.Form):
    time = forms.DateTimeField(initial=datetime.datetime.now)
    repeat = forms.BooleanField()
    repeat_time = forms.IntegerField(min_value=1)
    type = forms.ChoiceField(choices=Session.SESSION_TYPES)
