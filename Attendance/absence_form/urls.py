from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.EC_index, name='index'),
    url(r'^$', views.AbsenceForm_index, name='index'),
]