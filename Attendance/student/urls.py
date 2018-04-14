from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('students/<str:student_id>', views.student_detail, name='student_detail'),
]
