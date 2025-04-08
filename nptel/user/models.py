from django.db import models
from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, username, password, **extra_fields):
        """Create, save and return a new user."""
        if not username:
            raise ValueError('User must have an username.')
        if not password:
            raise ValueError('User must have a password.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """Create and return a new superuser."""
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )

    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    account_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def is_student(self):
        return self.user_type == 'student'
    
    def is_faculty(self):
        return self.user_type == 'faculty'

    

    def __str__(self):
        return self.username
    

class StudentProfile(models.Model):
    """Student profile model."""
    USER_LANGUAGE_CHOICES = (
        ('english', 'English'),
        ('hindi', 'Hindi'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=63, blank=True, null=True)
    last_name = models.CharField(max_length=63, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, validators=[MinLengthValidator(10)],)
    biography = models.TextField(blank=True, null=True)
    preferred_language = models.CharField(max_length=10, choices=USER_LANGUAGE_CHOICES, default='english')

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return f"No name provided"

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return f"No name provided"
    

class FacultyProfile(models.Model):
    """Faculty profile model."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='faculty_profile')
    faculty_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Faculty Profile"
        verbose_name_plural = "Faculty Profiles"

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return f"No name provided"


    def __str__(self):
        if self.first_name and self.last_name and self.department: 
            return f"{self.first_name} {self.last_name} ({self.department})"
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return f"No name provided"


