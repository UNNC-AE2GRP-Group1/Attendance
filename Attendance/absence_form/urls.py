from django.urls import include, path, re_path

# todo: review url
from . import views

urlpatterns = [
    path('applications/', views.application_index, name='application-index'),
    path('applications/<int:application_pk>/edit', views.application_edit, name='index'),
]
