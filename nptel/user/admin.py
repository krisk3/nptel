from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, FacultyProfile, StudentProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'account_type', 'is_active', 'is_staff', 'created_at']
    list_filter = ['account_type', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'student_profile__email', 'faculty_profile__email']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Account Type'), {'fields': ('account_type',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'modified_at')}),
    )
    readonly_fields = ['last_login', 'created_at', 'modified_at']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'account_type'),
        }),
    )

admin.site.register(FacultyProfile)
admin.site.register(StudentProfile)
