from django.conf.urls import include, url

from . import views

urlpatterns = [
    url('^sessions/$', views.session_index),
    url('^modules/$', views.module_index),
    url('^modules/(?P<module_pk>\w+)/attendance$', views.module_attendance_history),
]
