from django.conf.urls import url

# todo: review url
from . import views
urlpatterns = [
    url(r'^applications/$', views.application_index, name='application-index'),
    url(r'^applications/(?P<application_pk>\w+)/edit$', views.application_edit, name='index'),
]
