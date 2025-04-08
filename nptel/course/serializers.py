from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Course, Registration


# Serializers
class CourseCreateSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'course_name',
            'course_code',
            'description',
            'duration',
            'difficulty_level',
            'is_active',
            'instructor',
            'instructor_name', 
            'created_at', 
            'updated_at']
        read_only_fields = ['id', 'course_code', 'instructor', 'is_active', 'created_at', 'updated_at']

    def get_instructor_name(self, obj):
        return obj.instructor.get_full_name()

    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user.faculty_profile
        validated_data['is_active'] = True
        return super().create(validated_data)
    

class CourseDetailSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'course_name',
            'course_code',
            'description',
            'duration',
            'difficulty_level',
            'is_active',
            'instructor',
            'instructor_name', 
            'created_at', 
            'updated_at']
        read_only_fields = ['id','course_code', 'instructor', 'created_at', 'updated_at']

    def get_instructor_name(self, obj):
        return obj.instructor.get_full_name()
    
class RegistrationSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()  
    course = serializers.SerializerMethodField()  

    class Meta:
        model = Registration
        fields = ['id', 'student', 'course', 'status', 'registration_date', 'grade']
        read_only_fields = ['id', 'status', 'registration_date', 'grade']

    def get_student(self, obj):
        return {
            "name": obj.student.get_full_name(),
            "student_id": obj.student.student_id,
            "username": obj.student.user.username,
            "email": obj.student.email
        }

    def get_course(self, obj):
        return {
            "course_name": obj.course.course_name,
            "course_code": obj.course.course_code,
            "course_description": obj.course.description,
            "course_duration": obj.course.duration,
            "course_difficulty_level": obj.course.difficulty_level,
            "course_instructor": obj.course.instructor.get_full_name()
        }