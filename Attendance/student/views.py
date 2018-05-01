from django.shortcuts import render, Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Student
from session.models import *
from absence_form.models import *

# todo: permission
def get_student_by_id(student_id):
    try:
        s = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    return s

@login_required
def student_detail(request, student_id):
    if not request.user.has_perm('student.view'):
        return HttpResponseForbidden()

    s = get_student_by_id(student_id)

    # participated modules
    modules = Module.objects.filter(students__student_id=student_id)

    # involved sessions
    attendances = Attendee.objects.filter(student=s)\
        .prefetch_related('session')\
        .order_by('-session__time')

    # affected applications
    applications = Application.objects.filter(student=s)

    context = {
        'title': s,
        'student': s,
        'modules': modules,
        'attendances': attendances,
        'applications': applications,
    }

    return render(request, 'student/detail.html', context)
