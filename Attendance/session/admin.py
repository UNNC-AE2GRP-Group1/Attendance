from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(Session)
admin.site.register(Attendee)
