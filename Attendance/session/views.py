from django.shortcuts import render
from django.http import HttpResponse
from bridgekeeper import perms
from io import StringIO

import csv

from .models import *

# Create your views here.

def module_index(request):
    #all_modules = Module.objects.all()
    #visible_modules = perms['module.view'].filter(request.user, all_modules);

    return render(request, 'module/index.html')

# todo: data validation
# todo: error checks
# todo: resolve information conflicts instead of overwriting
# todo: permission
def module_student_import(request, module_pk):
    try:
        m = Module.objects.get(pk=module_pk)
    except Module.DoesNotExist:
        raise Http404("Module does not exist")

    if request.method == 'POST':
        csv_file = request.FILES['student_list_csv']
        student_reader = csv.reader(StringIO(csv_file.read().decode('utf-8')), delimiter=',')
        m.batch_enroll_from_csv(student_reader)

    context = {
        'module': m
    }
    return render(request, 'module/student_import.html', context)

def module_attendance_history(request, module_pk):
    return render(request, 'module/attendance_history.html')

def session_overview(request):
    return render(request, 'session/overview.html')

# show attendees, 
def session_detail(request, session_pk):
    return render(request, 'session/detail.html')

def session_taking_attendance(request, session_pk):
    return render(request, 'session/taking.html')
