from django.urls import include, path, re_path
from session.views import module_attendance_history

from . import views

# todo: add url tests
urlpatterns = [
  path('statistics/', views.module_attendance_history, name='module_attendance_history')
 #   path('students/(<int:student_id>/stat/', views.student_attendance_history),
 #  path('modules/(<int:module_pk>/stat/', views.module_attendance_history),
]
