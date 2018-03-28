from django.shortcuts import render
from bridgekeeper import perms

from .models import *

# todo: implement function
def application_index(request):
    EC_list = EC.objects.all()
    context = {'EC_list': EC_list}
    return render(request, 'application/index.html', context)

def application_edit(request, application_pk):
    context = {'specific_ec':EC.objects.get(pk = application_pk)}
    return render(request, 'application/edit.html', context)
