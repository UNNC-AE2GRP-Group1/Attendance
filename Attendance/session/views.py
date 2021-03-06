from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from bridgekeeper import perms
from io import StringIO
import json
import csv
from django.db import transaction
from copy import deepcopy
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from absence_form.models import *

# Create your views here.

@login_required
def module_create(request):
    if not request.user.has_perm('module.create'):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ModuleCreateForm(request.POST)
        if form.is_valid():
            m = form.save()
            return redirect('module_detail', m.pk)
    else:
        form = ModuleCreateForm()

    context = {
        'form': form,
        'title': "Create module"
    }
    return render(request, 'module/create.html', context)

@login_required
def module_index(request):
    all_modules = Module.objects.all()
    visible_modules = perms['module.view'].filter(request.user, all_modules)

    context = {
        'title': "All modules",
        'modules': visible_modules
    }
    return render(request, 'module/index.html', context)

# todo: permission
def get_module(module_pk):
    try:
        m = Module.objects.get(pk=module_pk)
    except Module.DoesNotExist:
        raise Http404("Module does not exist")
    return m

@login_required
def module_detail(request, module_pk):
    m = get_module(module_pk)

    if not request.user.has_perm('module.view', m):
        return HttpResponseForbidden()

    context = {
        'title': m,
        'module': m
    }
    return render(request, 'module/detail.html', context)

# todo: permission
@login_required
def module_create_session(request, module_pk):
    m = get_module(module_pk)

    if not request.user.has_perm('module.create_session', m):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = SessionCreateForm(request.POST)
        # todo: bulk create
        if form.is_valid():
            prototype = form.save(commit=False)
            prototype.module = m
            week = datetime.timedelta(days=7)
            sessions = []
            for x in range(0, form.cleaned_data['repeat_for_weeks']):
                sessions.append(deepcopy(prototype))
                prototype.time += week
            Session.objects.bulk_create(sessions)
            return redirect('module_detail', module_pk=m.pk)
    else:
        form = SessionCreateForm()

    context = {
        'title': 'Create sessions for {}'.format(m),
        'module': m,
        'form': form,
    }
    return render(request, 'session/create.html', context)

# todo: @requires_csrf_token
@login_required
def module_student_import(request, module_pk):
    if request.method == 'POST':
        m = get_module(module_pk)

        if not request.user.has_perm('module.import_student', m):
            return HttpResponseForbidden()

        csv_file = request.FILES['student_list_csv']
        student_reader = csv.reader(StringIO(csv_file.read().decode('utf-8')), delimiter=',')
        conflicts = m.batch_enroll_from_csv(student_reader)
        if not conflicts:
            return HttpResponse("Student list imported.")
        else:
            json_conflicts = serialize('json', conflicts, fields=('student_id','first_name','last_name'))
            return HttpResponse(json_conflicts, status=409)

    return redirect('module_detail', module_pk=m.pk)

@login_required
def module_attendance_history(request, module_pk):
    module = get_module(module_pk)

    if not request.user.has_perm('module.view_history', module):
        return HttpResponseForbidden()

    attendees = Attendee.objects.filter(session__module=module)\
        .prefetch_related('session', 'student')
    sessions = set()
    students = set()
    cells = {}

    # fetch application details affecting this module
    application_details = Detail.objects.filter(module=module).prefetch_related('application__student')
    student_to_app_details = {}

    for d in application_details:
        stupk = d.application.student.pk
        stu = student_to_app_details.get(stupk)
        if stu == None:
            student_to_app_details[stupk] = [d]
        else:
            student_to_app_details[stupk].append(d)

    # first iteration: find universal set of sessions and students
    for a in attendees:
        sessions.add(a.session)
        students.add(a.student)
        # build reverse search dict
        cells[a.session.pk,a.student.pk] = a

    sorted_sessions = sorted(sessions, key=lambda x: x.time)        # sort by time
    sorted_students = sorted(students, key=lambda x: x.student_id)  # sort by student id

    context = {
        'title': 'Attendance history of {}'.format(module),
        'module': module,
        'students': sorted_students,
        'sessions': sorted_sessions,
        'cells': cells,
        'student_to_app_details': student_to_app_details
    }
    return render(request, 'module/attendance_history.html', context)

@login_required
def session_overview(request):
    all_modules = Module.objects.all()
    visible_modules = perms['module.view'].filter(request.user, all_modules)

    sessions = Session.objects.filter(module__in=visible_modules)\
        .order_by('-time').prefetch_related('module')

    context = {
        'title': 'All sessions',
        'modules': visible_modules,
        'sessions': sessions,
    }
    return render(request, 'session/index.html', context)

# todo: permission
def get_session(session_pk):
    try:
        s = Session.objects.get(pk=session_pk)
    except Session.DoesNotExist:
        raise Http404("Session does not exist")
    return s

@login_required
def session_detail(request, session_pk):
    return redirect('session_taking_attendance', session_pk=session_pk)

@login_required
@ensure_csrf_cookie
def session_taking_attendance(request, session_pk):
    session = get_session(session_pk)

    if not request.user.has_perm('module.view', session.module):
        return HttpResponseForbidden()

    if request.method == 'POST':
        # todo: test csrf
        @csrf_protect
        @transaction.atomic
        def take_attendance(request):
            # possibilities:
            # in module student list - create Attendees
            # not in module list, but in database - fetch them, if name conflicts, a comment is addd
            # not in database - create a record, but it can only be changed afterwards by admin
            # { sid: { student_id: , first_name: , last_name: , presented: , comment: } }
            attendance = json.loads(request.body.decode('utf-8'))
            sid_dict = dict(Student.objects.filter(student_id__in=attendance.keys()).values_list('student_id', 'pk'))

            attendees = []
            for sid, a in attendance.items():
                spk = sid_dict.get(sid)
                if spk == None:
                    new_student = Student(
                        student_id=sid,
                        first_name=a['first_name'],
                        last_name=a['last_name']
                    )
                    new_student.save()
                    spk = new_student.pk
                attendees.append(Attendee(
                    session=session,
                    student=Student(pk=spk),
                    presented=a['presented'],
                    comment=a['comment']
                ))
            session.attendee_set.all().delete()
            session.attendee_set.bulk_create(attendees)
            # this is the only place that the attendance rate should be updated
            session.update_attendance_rate()
            session.module.update_attendance_rate()

            # get back to parent method but via GET
            return redirect('session_taking_attendance', session_pk=session_pk)
        take_attendance(request)

    attendees = []
    if session.attendee_set.exists():
        for a in session.attendee_set.prefetch_related('student').all().order_by('student__student_id'):
            attendees.append({
                'student_id': a.student.student_id,
                'first_name': a.student.first_name,
                'last_name': a.student.last_name,
                'presented': a.presented,
                'comment': a.comment,
            })
    else:
        for s in session.module.students.all().order_by('student_id'):
            attendees.append({
                'student_id': s.student_id,
                'first_name': s.first_name,
                'last_name': s.last_name,
                'presented': True,
                'comment': '',
            })
    context = {
        'title': 'Attendance sheet of {}'.format(session),
        'session': session,
        'attendees': json.dumps(attendees),
    }
    return render(request, 'session/attendance.html', context)

@login_required
def session_download_attendance_sheet(request, session_pk):
    s = get_session(session_pk)

    if not request.user.has_perm('module.view', s.module):
        return HttpResponseForbidden()

    response = HttpResponse(content_type='application/pdf')
    # todo: sanitize file name
    filename = 'attendance_sheet_{0}_{1}_{2}'.format(
        s.module.name,
        s.time.strftime('%Y-%m-%d'),
        s.place
    )
    response['Content-Disposition'] = 'filename={0}.pdf'.format(filename)
    pdf = s.get_signature_sheet_pdf()
    response.write(pdf)
    return response
