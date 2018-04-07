from django.shortcuts import render, redirect
from bridgekeeper import perms

from .models import *
from .forms import *

# todo: implement function
def application_index(request):
    EC_list = Ec.objects.all()
    context = {'EC_list': EC_list}
    return render(request, 'application/index.html', context)

def AbsenceForm_index(request):
    AbsenceForm_list = AbsenceForm.objects.all()
    context = {'AbsenceForm_list': AbsenceForm_list}
    return render(request, 'absence/index.html', context)

def ec_detail(request, application_pk):
    context = {'specific_ec':Ec.objects.get(pk = application_pk)}
    return render(request, 'application/ec_detail.html', context)

def detail_appeal(request, assessment_pk):
    context = {'assessment':EcDetail.objects.get(pk = assessment_pk)}
    return render(request, 'application/detail_appeal.html', context)

def absence_appeal(request, absencemodule_pk):
    context = {'absencemodule':AbsenceDetail.objects.get(pk = absencemodule_pk)}
    return render(request, 'absence/absence_appeal.html', context)

def absence_detail(request, absence_pk):
    context = {'absence':AbsenceForm.objects.get(pk = absence_pk)}
    return render(request, 'absence/absence_detail.html', context)

def create_ec(request):
    if request.method == 'POST':
        form = CreateEcForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('application_index')
    else:
        form = CreateEcForm()

    return render(request, 'application/create_ec.html', { 'form': form })

def create_absence(request):
    if request.method == 'POST':
        form = CreateAbsenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AbsenceForm-index')
    else:
        form = CreateAbsenceForm()

    return render(request, 'absence/create_absence.html', { 'form': form })

def add_assessment(request, Ec_pk):
    try:
        e = Ec.objects.get(pk=Ec_pk)
    except Ec.DoesNotExist:
        raise Http404("Ec does not exist")
    if request.method == 'POST':
        form = AddAssessment(request.POST)
        if form.is_valid():
            EcDetail = form.save(commit=False)
            EcDetail.Ec = e
            EcDetail.save()
            return redirect('ec-detail', application_pk=e.pk)
    else:
        form = AddAssessment()

    context = {
        'Ec': e,
        'form': form,
    }
    
    return render(request, 'application/add_assessment.html', context)

def add_module(request, absence_pk):
    try:
        a = AbsenceForm.objects.get(pk=absence_pk)
    except AbsenceForm.DoesNotExist:
        raise Http404("Ec does not exist")
    if request.method == 'POST':
        form = AddModule(request.POST)
        if form.is_valid():
            AbsenceDetail = form.save(commit=False)
            AbsenceDetail.AbsenceForm = a
            AbsenceDetail.save()
            return redirect('absence-detail', absence_pk=a.pk)
    else:
        form = AddModule()

    context = {
        'Absence': a,
        'form': form,
    }
    
    return render(request, 'absence/add_module.html', context)

def add_appeal(request, assessment_pk):
    try:
        d = EcDetail.objects.get(pk=assessment_pk)
    except EcDetail.DoesNotExist:
        raise Http404("EcDetail does not exist")
    if request.method == 'POST':
        form = AddAppeal(request.POST)
        if form.is_valid():
            EcAppeal = form.save(commit=False)
            EcAppeal.EcDetail = d
            EcAppeal.save()
            return redirect('detail-appeal', assessment_pk=d.pk)
    else:
        form = AddAppeal()

    context = {
        'Assessment': d,
        'form': form,
    }
    
    return render(request, 'application/add_appeal.html', context)

def add_absenceform_appeal(request, absencemodule_pk):
    try:
        d = AbsenceDetail.objects.get(pk=absencemodule_pk)
    except AbsenceDetail.DoesNotExist:
        raise Http404("AbsenceDetail does not exist")
    if request.method == 'POST':
        form = AddAbsenceAppeal(request.POST)
        if form.is_valid():
            AbsenceAppeal = form.save(commit=False)
            AbsenceAppeal.AbsenceDetail = d
            AbsenceAppeal.save()
            return redirect('absence-appeal', absencemodule_pk=d.pk)
    else:
        form = AddAbsenceAppeal()

    context = {
        'Absencemodule': d,
        'form': form,
    }
    
    return render(request, 'absence/absence_add_appeal.html', context)