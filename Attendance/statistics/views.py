from django.shortcuts import render
from django.http import Http404
from student.models import Student
from session.models import Module, Session
from bridgekeeper import perms
#from .models import *

# todo: which student should a user be allowed to view?
def module_attendance_history(request):
#    try:
#       m = Module.objects.all()
#       vm = filter(request.user,m)
#       sessions = Session.objects.get(module=vm)
#    except Module.DoesNotExist:
#        raise Http404("Module does not exist")
    return render(
        request,
         'statistics/module.html'
 #        {'sessions': sessions},{'modules': vm}
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