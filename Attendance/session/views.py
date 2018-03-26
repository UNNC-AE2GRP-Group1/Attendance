from django.shortcuts import render
from bridgekeeper import perms

from .models import *

# Create your views here.

def module_index(request):
    #all_modules = Module.objects.all()
    #visible_modules = perms['module.view'].filter(request.user, all_modules);

    return render(request, 'module/index.html')

def module_attendance_history(request, module_pk):
    return render(request, 'module/attendance_history.html')

def session_overview(request):
    return render(request, 'session/overview.html')

# show attendees, 
def session_detail(request, session_pk):
    return render(request, 'session/detail.html')

def session_taking_attendance(request, session_pk):
    return render(request, 'session/taking.html')
