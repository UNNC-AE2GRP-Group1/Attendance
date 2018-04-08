from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(AbsenceApplication)
admin.site.register(ExtenuatingCircumstanceApplication)
admin.site.register(Detail)
admin.site.register(Appeal)
