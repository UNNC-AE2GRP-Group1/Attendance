from django.conf.urls import include, url

from . import views

urlpatterns = [
    url('^sessions/$', views.session_index),
    url('^sessions/(?P<session_pk>\w+)/attendance$', views.session_taking_attendance),
    url('^modules/$', views.module_index),
    url('^modules/(?P<module_pk>\w+)/attendance$', views.module_attendance_history),
]
