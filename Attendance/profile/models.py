from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_ROLES = (
        ('ST', 'Senior Tutor'),
        ('MC', 'Module Convenor'),
        ('TA', 'Teaching Assistant'),
    )
    primary_role = models.CharField(max_length=2, choices=USER_ROLES)
