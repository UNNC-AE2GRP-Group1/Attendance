from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # todo: seems to be useless except when the user is senior tutor, as the permissions are check using module fields
    SENIOR_TUTOR = 'ST'
    MODULE_CONVENOR = 'MC'
    TEACHING_ASSISTANT = 'TA'
    USER_ROLES = (
        (SENIOR_TUTOR, 'Senior Tutor'),
        (MODULE_CONVENOR, 'Module Convenor'),
        (TEACHING_ASSISTANT, 'Teaching Assistant'),
    )
    primary_role = models.CharField(max_length=2, choices=USER_ROLES)

    def __str__(self):
        return '[{}] {}'.format(self.get_primary_role_display(), str(self.user))
