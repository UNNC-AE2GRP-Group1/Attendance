from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('sessions/', views.session_overview, name='session_overview'),
    path('sessions/<int:session_pk>/attendance_sheet', views.session_download_attendance_sheet, name='session_download_attendance_sheet'),
    path('sessions/<int:session_pk>/attendance', views.session_taking_attendance, name='session_attendance'),
    path('modules/', views.module_index, name='module_index'),
    path('modules/create', views.module_create, name='module_create'),
    path('modules/<int:module_pk>/', views.module_detail, name="module_detail"),
    path('modules/<int:module_pk>/sessions/create', views.module_create_session, name='module_create_session'),
    path('modules/<int:module_pk>/students/', views.module_students, name="module_students"),
    path('modules/<int:module_pk>/students/import', views.module_student_import, name="module_student_import"),
    path('modules/<int:module_pk>/attendance/', views.module_attendance_history, name="module_attendance_history"),
]
