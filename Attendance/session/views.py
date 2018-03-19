from django.shortcuts import render
from bridgekeeper import perms

from .models import *

# Create your views here.

def session_index(request):
    return render(request, 'session/index.html')

def module_index(request):
    #all_modules = Module.objects.all()
    #visible_modules = perms['module.view'].filter(request.user, all_modules);

    return render(request, 'session/module_index.html')

# show attendees, 
def session_detail(request, session_id):
    return render(request, 'session/session_detail.html')
