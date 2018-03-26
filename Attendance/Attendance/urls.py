"""
Definition of urls for Attendance.
"""

from datetime import datetime
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^', include('app.urls')),
    url(r'^', include('session.urls')),
    url(r'^', include('statistics.urls')),
    url(r'^', include('absence_form.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
