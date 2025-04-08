from django.contrib import admin
from .models import Course, Registration

# Admin Portal configuration
admin.site.register(Course)
admin.site.register(Registration)