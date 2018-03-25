from django.conf.urls import url

# todo: review url
from . import views
urlpatterns = [
    url(r'^application/ec/$', views.EC_index, name='index'),
    url(r'^application/absence/$', views.AbsenceForm_index, name='index'),
]
