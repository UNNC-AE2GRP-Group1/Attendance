from django.conf.urls import include, url

from . import views

# todo: add url tests
urlpatterns = [
    url(r'^students/(?P<student_id>\w+)/stat$', views.student_attendance_history),
    url(r'^modules/(?P<module_pk>\w+)/stat$', views.module_attendance_history),
]
