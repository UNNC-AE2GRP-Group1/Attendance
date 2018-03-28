from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('sessions/', views.session_overview, name='session-overview'),
    path('sessions/<int:session_pk>/attendance/', views.session_taking_attendance),
    path('modules/', views.module_index, name='module-index'),
    path('modules/<int:module_pk>/students/', views.module_student_import, name="module-students"),
    path('modules/<int:module_pk>/attendance/', views.module_attendance_history),
]
