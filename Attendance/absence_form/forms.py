from django import forms
import datetime
from .models import *

class CreateAbsenceApplicationForm(forms.ModelForm):
    class Meta:
        model = AbsenceApplication
        exclude  = ['created_at']
        
class CreateExtenuatingCircumstanceApplicationForm(forms.ModelForm):
    class Meta:
        model = ExtenuatingCircumstanceApplication
        exclude  = ['created_at']
        field_order = ['identifier', 'from_date', 'to_date', 'student', 'status', 'comment']

class AddApplicationDetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        exclude = []

class AddApplicationAppealForm(forms.ModelForm):
    class Meta:
        model = Appeal
        exclude = []
