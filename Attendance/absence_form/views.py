from django.http import HttpResponse
from django.shortcuts import render
from bridgekeeper import perms

from .models import *

# todo: implement function
def EC_index(request):
    return render(request, 'EC/index.html')

def AbsenceForm_index(request):
    return render(request, 'AbsenceForm/index.html')
