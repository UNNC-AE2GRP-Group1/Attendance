from django.http import HttpResponse
from django.shortcuts import render
from bridgekeeper import perms

from .models import *

# todo: implement function
def application_index(request):
    return render(request, 'application/index.html')

def application_edit(request, application_pk):
    return render(request, 'application/edit.html')
