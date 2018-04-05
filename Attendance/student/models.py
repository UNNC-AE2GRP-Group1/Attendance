from django.db import models

# Create your models here.

def trimed_title_case(str):
    return " ".join(str.split()).title()

class Student(models.Model):
    student_id = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    degree_name = models.CharField(max_length=255, blank=True)
    GENDERS = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    gender = models.CharField(max_length=2, choices=GENDERS, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        indexes = [
            # the student id is use for searching
            models.Index(fields=['student_id']),
        ]

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return '[{}] {}'.format(self.student_id, self.get_full_name())

    def save(self, *args, **kwargs):
        """The method is overridden to sanitize the data"""
        self.student_id = self.student_id.strip()
        self.first_name = trimed_title_case(self.first_name)
        self.last_name = trimed_title_case(self.last_name)

        super().save(*args, **kwargs)
