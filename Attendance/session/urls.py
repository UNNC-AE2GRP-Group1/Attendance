from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^sessions/$', views.session_index),
    url(r'^sessions/(?P<session_pk>\w+)/attendance$', views.session_taking_attendance),
    url(r'^modules/$', views.module_index),
    url(r'^modules/(?P<module_pk>\w+)/attendance$', views.module_attendance_history),
]
