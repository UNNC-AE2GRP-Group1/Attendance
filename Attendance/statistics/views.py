from django.shortcuts import render
from django.http import Http404
from student.models import Student
from session.models import Module

# todo: which student should a user be allowed to view?
def student_attendance_history(request, student_id):
    try:
        s = Student.objects.get(student_id=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    return render(
        request,
        'statistics/student.html',
        # {'poll': p}
    )

def module_attendance_history(request, module_pk):
    try:
        m = Module.objects.get(pk=module_pk)
    except Module.DoesNotExist:
        raise Http404("Module does not exist")
    return render(
        request,
        'statistics/module.html',
        # {'poll': p}
    )
