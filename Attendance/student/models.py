from django.db import models

# Create your models here.

class Student(models.Model):
    student_id = models.CharField(max_length=16)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    degree_name = models.CharField(max_length=255)
    GENDERS = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    gender = models.CharField(max_length=2, choices=GENDERS, blank=True)
    email = models.EmailField()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.get_full_name()
