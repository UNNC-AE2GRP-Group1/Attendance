from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Application)
admin.site.register(Detail)
admin.site.register(Appeal)
