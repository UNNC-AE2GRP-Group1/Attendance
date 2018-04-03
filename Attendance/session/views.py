from django.shortcuts import render, redirect
from django.http import HttpResponse
from bridgekeeper import perms
from io import StringIO

import csv

from .models import *
from .forms import *

# Create your views here.

def module_create(request):
    if request.method == 'POST':
        form = ModuleCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module-index')
    else:
        form = ModuleCreateForm()

    return render(request, 'module/create.html', { 'form': form })

def module_index(request):
    all_modules = Module.objects.all()
    # visible_modules = perms['module.view'].filter(request.user, all_modules);

    context = {
        'modules': all_modules
    }
    return render(request, 'module/index.html', context)

def module_detail(request, module_pk):
    try:
        m = Module.objects.get(pk=module_pk)
    except Module.DoesNotExist:
        raise Http404("Module does not exist")

    context = {
        'module': m
    }
    return render(request, 'module/detail.html', context)

# todo: permission
def module_create_session(request, module_pk):
    try:
        m = Module.objects.get(pk=module_pk)
    except Module.DoesNotExist:
        raise Http404("Module does not exist")

    if request.method == 'POST':
        form = SessionCreateForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.module = m
            session.save()
            return redirect('module-detail', module_pk=m.pk)
    else:
        form = SessionCreateForm()

    context = {
        'module': m,
        'form': form,
    }
    return render(request, 'session/create.html', context)

# todo: data validation
# todo: error checks
# todo: resolve information conflicts instead of overwriting
# todo: permission
def module_students(request, module_pk):
    try:
        m = Module.objects.get(pk=module_pk)
    except Module.DoesNotExist:
        raise Http404("Module does not exist")

    context = {
        'module': m
    }
    return render(request, 'module/students.html', context)

# todo: permission
def module_student_import(request, module_pk):
    if request.method == 'POST':
        try:
            m = Module.objects.get(pk=module_pk)
        except Module.DoesNotExist:
            raise Http404("Module does not exist")

        csv_file = request.FILES['student_list_csv']
        student_reader = csv.reader(StringIO(csv_file.read().decode('utf-8')), delimiter=',')
        m.batch_enroll_from_csv(student_reader)

    return redirect('module-students', module_pk=module_pk)

def module_attendance_history(request, module_pk):
    return render(request, 'module/attendance_history.html')

def session_overview(request):
    return render(request, 'session/index.html')

# show attendees, 
def session_detail(request, session_pk):
    return render(request, 'session/detail.html')

def session_taking_attendance(request, session_pk):
    return render(request, 'session/taking.html')

# todo: permission
def session_download_attendance_sheet(request, session_pk):
    try:
        s = Session.objects.get(pk=session_pk)
    except Session.DoesNotExist:
        raise Http404("Session does not exist")

    response = HttpResponse(content_type='application/pdf')
    # todo: sanitize file name
    filename = 'attendance_sheet_{0}_{1}_{2}'.format(
        s.module.name,
        s.time.strftime('%Y-%m-%d'),
        s.place
    )
    response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(filename)
    pdf = s.get_signature_sheet_pdf()
    response.write(pdf)
    return response
