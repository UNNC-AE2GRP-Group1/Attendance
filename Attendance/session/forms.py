from django.forms import ModelForm
import datetime
from .models import *

class ModuleCreateForm(ModelForm):
    class Meta:
        model = Module
        exclude = ['students', 'attendance_rate']

class SessionCreateForm(ModelForm):
    class Meta:
        model = Session
        fields = ['time', 'duration', 'place', 'type']
