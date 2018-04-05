from django.urls import include, path, re_path

# todo: review url
from . import views

urlpatterns = [
    path('applications/', views.application_index, name='application-index'),
    path('applications/<int:application_pk>/EcDetail', views.ec_detail, name='ec-detail'),
    path('applications/<int:Ec_pk>/AddAssessment', views.add_assessment, name='add-assessment'),
    path('applications/<int:application_pk>/single_edit', views.single_edit, name='single-edit'),
    path('applications/ec/create', views.create_ec, name='create_ec'),
]
