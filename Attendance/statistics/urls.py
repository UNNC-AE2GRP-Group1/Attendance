from django.urls import include, path, re_path

from . import views

# todo: add url tests
urlpatterns = [
    path('modules/stat/', views.module_attendance_history_all, name='module-attendance-history-all'),
    path('students/(<int:student_id>/stat/', views.student_attendance_history),
    path('modules/(<int:module_pk>/stat/', views.module_attendance_history),
]
