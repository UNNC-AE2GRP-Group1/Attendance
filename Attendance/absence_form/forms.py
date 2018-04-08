from django import forms
import datetime
from .models import *

class ApplicationCreateForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude  = ['created_at']

class DetailAddForm(forms.ModelForm):
    class Meta:
        model = Detail
        exclude = ['application']

class AppealAddForm(forms.ModelForm):
    class Meta:
        model = Appeal
        exclude = ['detail']
