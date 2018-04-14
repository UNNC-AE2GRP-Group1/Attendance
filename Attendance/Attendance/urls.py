"""
Definition of urls for Attendance.
"""

from datetime import datetime
from django.contrib import admin
from django.urls import include, path, re_path

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    path('', include('app.urls')),
    path('', include('session.urls')),
    path('', include('statistics.urls')),
    path('', include('absence_form.urls')),
    path('', include('student.urls')),

    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
]
