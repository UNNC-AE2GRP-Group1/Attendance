from django.urls import include, path, re_path

# todo: review url
from . import views

urlpatterns = [
    path('applications/', views.application_index, name='application_index'),
    path('applications/create', views.application_create, name='application_create'),
    path('applications/<int:application_pk>', views.application_detail, name='application_detail'),
    path('applications/<int:application_pk>/details/create', views.application_detail_create, name='application_detail_create'),
    path('applications/<int:application_pk>/details/<int:detail_pk>/appeals/create', views.application_appeal_create, name='application_appeal_create'),
]
