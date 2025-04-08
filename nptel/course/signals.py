from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Course
import hashlib


@receiver(pre_save, sender=Course)
def add_course_code(sender, instance, **kwargs):
    if not instance.course_code:  # Only generate if course_code is not already set
        # Combine course_name and description to create a unique hash
        unique_string = f"{instance.course_name}-{instance.description}"
        hash_object = hashlib.sha256(unique_string.encode('utf-8'))
        instance.course_code = f"COURSE-{hash_object.hexdigest()[:8].upper()}"