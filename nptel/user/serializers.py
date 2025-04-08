from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db import transaction
from user.models import FacultyProfile, StudentProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class FacultyLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            try:
                faculty = FacultyProfile.objects.get(user=user)
                return {'user': user, 'faculty': faculty}
            except FacultyProfile.DoesNotExist:
                raise serializers.ValidationError("User is not a faculty.")
        raise serializers.ValidationError("Invalid credentials.")
    

class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            try:
                student = StudentProfile.objects.get(user=user)
                return {'user': user, 'student': student}
            except StudentProfile.DoesNotExist:
                raise serializers.ValidationError("User is not a student.")
        raise serializers.ValidationError("Invalid credentials.")


class CreateStudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = StudentProfile
        fields = [
            'username',
            'password',
            'student_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'biography',
            'preferred_language',
        ]

        read_only_fields = ['student_id']

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=username,
            password=password,
            account_type='student'
        )

        student_profile = StudentProfile.objects.get(user=user)

        for attr, value in validated_data.items():
            setattr(student_profile, attr, value)

        student_profile.save()
        return student_profile

    def to_representation(self, instance):
        return {
            "username": instance.user.username,  
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "student_id": instance.student_id,
            "email": instance.email,
            "phone_number": instance.phone_number,
            "biography": instance.biography,
            "preferred_language": instance.preferred_language,
        }    

class CreateFacultySerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = FacultyProfile
        fields = [
            'username',
            'password',
            'faculty_id',
            'first_name',
            'last_name',
            'email',
            'department',
            'designation',
        ]

        read_only_fields = ['faculty_id']

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=username,
            password=password,
            account_type='faculty'
        )

        faculty_profile = FacultyProfile.objects.get(user=user)

        for attr, value in validated_data.items():
            setattr(faculty_profile, attr, value)

        faculty_profile.save()
        return faculty_profile

    def to_representation(self, instance):
        return {
            "username": instance.user.username,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "faculty_id": instance.faculty_id,
            "email": instance.email,
            "department": instance.department,
            "designation": instance.designation,
        }