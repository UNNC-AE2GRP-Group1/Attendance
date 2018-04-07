from django import forms
import datetime
from .models import *

class CreateEcForm(forms.ModelForm):
    class Meta:
        model = Ec
        fields = ['student', 'comment', 'submit_date', 'EC_status']
        
class CreateAbsenceForm(forms.ModelForm):
    class Meta:
        model = AbsenceForm
        fields = ['student', 'comment', 'submit_date', 'AbsenceForm_status']

class AddAssessment(forms.ModelForm):
    class Meta:
        model = EcDetail
        fields = ['module', 'from_time', 'due_date', 'assessment_kind']

class AddModule(forms.ModelForm):
    class Meta:
        model = AbsenceDetail
        fields = ['module', 'from_time', 'due_date']
        

class AddAppeal(forms.ModelForm):
    class Meta:
        model = EcAppeal
        fields = ['time', 'status']
        

class AddAbsenceAppeal(forms.ModelForm):
    class Meta:
        model = AbsenceAppeal
        fields = ['time', 'status']