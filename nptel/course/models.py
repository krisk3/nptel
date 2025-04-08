from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from user.models import FacultyProfile, StudentProfile

# Models
class Course(models.Model):
    """
    Course model to represent a course in the system
    """
    DIFFICULTY_CHOICES = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced')
    ]

    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)   
    duration = models.IntegerField(help_text="Duration in days")
    difficulty_level = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES)
    instructor = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='courses')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_name} ({self.course_code})"

class Registration(models.Model):
    """
    Registration model for students to register for courses
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    registration_date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=2, blank=True, null=True, default="")

    class Meta:
        unique_together = ['student', 'course']

    def save(self, *args, **kwargs):
        if self.status == 'approved':
            approved_count = self.student.registrations.filter(status='approved').exclude(pk=self.pk).count()
            if approved_count >= 2:
                raise ValidationError("Students can only register for a maximum of 2 courses.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.course}"