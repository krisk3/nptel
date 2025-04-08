from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Course

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
        validated_data['instructor'] = self.context['request'].user.facultyprofile
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