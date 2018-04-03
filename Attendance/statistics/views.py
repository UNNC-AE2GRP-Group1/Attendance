from django.shortcuts import render
from django.http import Http404
from student.models import Student
from session.models import Module, Session
from bridgekeeper import perms
from django.db.models import Prefetch
import json
import time
#from .models import *

# todo: absent student list
def module_attendance_history(request):

#get name list for all modules
    modules = Module.objects.all()
    modulesName=[m.name for m in modules]

#get session:time，attendance_rate,5(absentStudents num),"absent student list" 
#for all sessions all modules
# as allModuleList  

    allModulesSessions=[]
    for m in modules:
         sessionList=m.session_set.all()
         moduleValueList=[]
         for s in sessionList:
             currValue=[]
             currValue.append(s.time)
             currValue.append(s.attendance_rate)
             currValue.append(5)
             currValue.append("absent student list")
             moduleValueList.append(currValue)
         allModulesSessions.append(moduleValueList)

#       sessionTimeList = [sessionList.append(m.session_set.all().time) for m in modules]
#       session_by_modules = [m.session_set.all().order_by('time') for m in modules]

#       prefetch_related(
#       Prefetch('Sessions__time', queryset=Sessions.objects.order_by('time')))
#       vm = filter(request.user,m)
#       sessions = m.sessions_set
#       except Module.DoesNotExist:
#       raise Http404("Module does not exist")

    return render(
        request,
        'statistics/module.html',
        {

            'legendData': json.dumps(['LAC', 'IIP', 'CPP']),

            #to do:test legendData0
            'legendData0': json.dumps(modulesName),

             #to do:test sessions0
             'sessions0': json.dumps(allModulesSessions, indent=4, sort_keys=True, default=str),

            'sessions': json.dumps([
              [time.mktime(time.strptime('2015-09-01',"%Y-%m-%d"))*1000,11,3,"absent student list"],
              [time.mktime(time.strptime('2015-09-03',"%Y-%m-%d"))*1000,20,1,"absent student list"],
              [time.mktime(time.strptime('2015-09-04',"%Y-%m-%d"))*1000,12,5,"absent student list"],
              [time.mktime(time.strptime('2015-09-05',"%Y-%m-%d"))*1000,10,8,"absent student list"],
              [time.mktime(time.strptime('2015-09-06',"%Y-%m-%d"))*1000,8,3,"absent student list"],
              [time.mktime(time.strptime('2015-09-08',"%Y-%m-%d"))*1000,16,3,"absent student list"],
              [time.mktime(time.strptime('2015-09-10',"%Y-%m-%d"))*1000,12,3,"absent student list"],
              [time.mktime(time.strptime('2015-09-11',"%Y-%m-%d"))*1000,16,3,"absent student list"]
              
                
                         ])
        }
    )


#def module_attendance_history(request):
#    try:
# m = Module.objects.all()
# vm = perms['module.view'].filter(request.user,m)
# sessions = Session.objects.get(module=vm)
#   except Module.DoesNotExist:
#        raise Http404("Module does not exist")
#    return render(
 #       request,
#        'statistics/module.html',
 #       { 'sessions': sessions }
#    )