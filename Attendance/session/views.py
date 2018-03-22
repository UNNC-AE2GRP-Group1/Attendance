from django.shortcuts import render
from .models import *

# Create your views here.
def module_index(request):
    return render(request, 'module/index.html')

def session_index(request):
    return render(request, 'session/index.html')
