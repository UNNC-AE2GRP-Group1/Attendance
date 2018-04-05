from django.shortcuts import render, redirect
from bridgekeeper import perms

from .models import *
from .forms import *

# todo: implement function
def application_index(request):
    EC_list = Ec.objects.all()
    context = {'EC_list': EC_list}
    return render(request, 'application/index.html', context)

def ec_detail(request, application_pk):
    context = {'specific_ec':Ec.objects.get(pk = application_pk)}
    return render(request, 'application/ec_detail.html', context)

def single_edit(request, detail_pk):
    context = {'specific_module':Ec.objects.get(pk = detail_pk)}
    return render(request, 'application/single_edit.html', context)

def create_ec(request):
    if request.method == 'POST':
        form = CreateEcForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application-index')
    else:
        form = CreateEcForm()

    return render(request, 'application/create_ec.html', { 'form': form })

def add_assessment(request):
    if request.method == 'POST':
        form = AddAssessment(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ec-detail')
    else:
        form = AddAssessment()

    return render(request, 'application/add_assessment.html', { 'form': form })