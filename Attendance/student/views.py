from django.shortcuts import render, Http404

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

def student_detail(request, student_id):
    s = get_student_by_id(student_id)

    # participated modules
    modules = Module.objects.filter(students__student_id=student_id)

    # involved sessions
    attendances = Session.objects.filter(attendee__student=s)

    # affected applications
    applications = Application.objects.filter(student=s)

    context = {
        'student': s,
        'modules': modules,
        'attendances': attendances,
        'applications': applications,
    }

    return render(request, 'student/detail.html', context)
