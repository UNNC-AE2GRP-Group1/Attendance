from django.urls import include, path, re_path

# todo: review url
from . import views

urlpatterns = [
    path('applications/', views.application_index, name='application-index'),
    path('applications/<int:application_pk>/EcDetail', views.ec_detail, name='ec-detail'),
    path('applications/<int:Ec_pk>/AddAssessment', views.add_assessment, name='add-assessment'),
    path('applications/<int:assessment_pk>/EcDetailAppeal', views.detail_appeal, name='detail-appeal'),
    path('applications/<int:assessment_pk>/AddAppeal', views.add_appeal, name='add-appeal'),
    path('applications/ec/create', views.create_ec, name='create_ec'),
    path('applications/absence/', views.AbsenceForm_index, name='AbsenceForm-index'),
    path('applications/<int:absence_pk>/AbsenceDetail', views.absence_detail, name='absence-detail'),
    path('applications/absence/create', views.create_absence, name='create_absence'),
    path('applications/<int:absence_pk>/AddModule', views.add_module, name='add-module'),
    path('applications/<int:absencemodule_pk>/AbsenceDetailAppeal', views.absence_appeal, name='absence-appeal'),
    path('applications/<int:absencemodule_pk>/AddAbsenceAppeal', views.add_absenceform_appeal, name='absence-add-appeal')
]
