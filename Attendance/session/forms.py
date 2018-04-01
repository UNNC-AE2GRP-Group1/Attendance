from django import forms
import datetime
from .models import Session

class SessionCreateForm(forms.Form):
    time = forms.DateTimeField(initial=datetime.datetime.now)
    repeat = forms.BooleanField()
    repeat_time = forms.IntegerField(min_value=1)
    type = forms.ChoiceField(choices=Session.SESSION_TYPES)
