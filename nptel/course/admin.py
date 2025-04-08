from django.contrib import admin
from .models import Course, Registration

# Register your models here.
admin.site.register(Course)
admin.site.register(Registration)