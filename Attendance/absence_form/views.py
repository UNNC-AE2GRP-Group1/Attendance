from django.shortcuts import render, redirect
from bridgekeeper import perms
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden

from .models import *
from .forms import *

def get_application(application_pk):
    try:
        app = Application.objects.get(pk=application_pk)
    except Application.DoesNotExist:
        raise Http404("Application does not exist")
    return app

@login_required
def application_index(request):
    if not request.user.has_perm('application'):
        return HttpResponseForbidden()

    appication_list = Application.objects.order_by('-created_at')\
        .prefetch_related('detail_set')
    context = {'app_list': appication_list}
    return render(request, 'application/index.html', context)

@login_required
def application_detail(request, application_pk):
    if not request.user.has_perm('application'):
        return HttpResponseForbidden()

    context = { 'application': get_application(application_pk) }
    return render(request, 'application/detail.html', context)

@login_required
def application_create(request):
    if not request.user.has_perm('application'):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ApplicationCreateForm(request.POST)
        if form.is_valid():
            app = form.save()
            return redirect('application_detail', application_pk=app.pk)
    else:
        form = ApplicationCreateForm()

    return render(request, 'application/create.html', { 'form': form })

@login_required
def application_detail_create(request, application_pk):
    if not request.user.has_perm('application'):
        return HttpResponseForbidden()

    app = get_application(application_pk)

    if request.method == 'POST':
        form = DetailAddForm(request.POST)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.application = app
            detail.save()
            return redirect('application_detail', application_pk=app.pk)
    else:
        form = DetailAddForm()

    context = {
        'application': app,
        'form': form,
    }
    
    return render(request, 'application/add_detail.html', context)


def get_detail(detail_pk):
    try:
        d = Detail.objects.get(pk=detail_pk)
    except Detail.DoesNotExist:
        raise Http404("Module affection detail does not exist")
    return d

@login_required
def application_appeal_create(request, application_pk, detail_pk):
    if not request.user.has_perm('application'):
        return HttpResponseForbidden()

    app = get_application(application_pk)
    d = get_detail(detail_pk)

    if request.method == 'POST':
        form = AppealAddForm(request.POST)
        if form.is_valid():
            appeal = form.save(commit=False)
            appeal.detail = d
            appeal.save()
            return redirect('application_detail', application_pk=app.pk)
    else:
        form = AppealAddForm()

    context = {
        'application': app,
        'detail': d,
        'form': form,
    }
    
    return render(request, 'application/add_appeal.html', context)
