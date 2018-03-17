from django.db import models
from django.utils import timezone
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from datetime import date

from student.models import Student

# Create your models here.

class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8)
    academic_year = models.SmallIntegerField()
    convenors = models.ManyToManyField(User, related_name='convenors', blank=True)
    assistants = models.ManyToManyField(User, related_name='assistants', blank=True)
    students = models.ManyToManyField(Student, through='Enrollment', blank=True)
    def __str__(self):
        return self.name + ' (' + str(self.academic_year) + ')'


# todo: 
class Enrollment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    date_enrolled = models.DateField(default=date.today)
    date_unenrolled = models.DateField(default=date.today)


class Session(models.Model):
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    time = models.DateTimeField(default=timezone.now)
    place = models.CharField(max_length=127)
    SESSION_TYPES = (
        ('LAB', 'Lab'),
        ('LEC', 'Lecture'),
    )
    type = models.CharField(max_length=3, choices=SESSION_TYPES)

    def __str__(self):
        ret = ''
        ret += '[' + str(self.time) + ']'   # time
        ret += '[' + self.type + ']'        # type
        ret += ' '
        ret += str(self.module)             # module
        return ret


class Attendee(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    presented = models.BooleanField()
    comment = models.TextField()

    # todo: potential performance issue when amount entries are large
    def __str__(self):
        return self.student.get_full_name() + ' from ' + str(self.session.module)
