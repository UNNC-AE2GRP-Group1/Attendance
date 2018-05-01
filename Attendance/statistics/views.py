from django.shortcuts import render
from django.http import Http404
from student.models import Student
from session.models import Module, Session
import json
import time
from django.contrib.auth.decorators import login_required

# todo: which student should a user be allowed to view?
@login_required
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

@login_required
def module_attendance_history_all(request):
#get name list for all modules
    modules = Module.objects.all()
    modulesName=[m.name for m in modules]

#get session:time，attendance_rate,5(absentStudents num),"absent student list" 
#for all sessions all modules
# as allModuleList  

    allModulesSessions=[]
    for m in modules:
         sessionList=m.session_set.filter(attendance_rate__isnull=False).order_by('time')
         moduleValueList=[]
         for s in sessionList:
             currValue=[]
             currValue.append(s.time)
             currValue.append(s.attendance_rate)
             currValue.append(10000/(s.attendance_rate-30))
             currValue.append("absent student list")
             moduleValueList.append(currValue)
         allModulesSessions.append(moduleValueList)

#       sessionTimeList = [sessionList.append(m.session_set.all().time) for m in modules]
#       session_by_modules = [m.session_set.all().order_by('time') for m in modules]
#       vm = filter(request.user,m)

    return render(
        request,
        'statistics/module.html',
        {
            'title': 'Attendance statistics',
            'legendData': json.dumps(modulesName),
            'sessions': json.dumps(allModulesSessions, indent=4, sort_keys=True, default=str),
        }
    )

@login_required
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
