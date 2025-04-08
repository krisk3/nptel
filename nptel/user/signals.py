import random
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import StudentProfile, FacultyProfile, User

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create a profile based on account type when a new User is created.
    """
    if created:
        if instance.account_type == 'student':
            StudentProfile.objects.create(user=instance)
        elif instance.account_type == 'faculty':
            FacultyProfile.objects.create(user=instance)


@receiver(pre_save, sender=StudentProfile)
def assign_student_id(sender, instance, **kwargs):
    """
    Assign a unique student_id before saving, if not already assigned.
    """
    if not instance.student_id and instance.user_id:
        random_suffix = random.randint(1000, 9999)
        instance.student_id = f"STU{instance.user.id}{random_suffix}"


@receiver(pre_save, sender=FacultyProfile)
def assign_faculty_id(sender, instance, **kwargs):
    """
    Assign a unique faculty_id before saving, if not already assigned.
    """
    if not instance.faculty_id and instance.user_id:
        random_suffix = random.randint(1000, 9999)
        instance.faculty_id = f"FAC{instance.user.id}{random_suffix}"
