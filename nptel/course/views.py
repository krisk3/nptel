from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.shortcuts import get_object_or_404
from .models import Course, Registration
from user.models import FacultyProfile, StudentProfile
from .serializers import CourseCreateSerializer, CourseDetailSerializer, RegistrationSerializer


# Views
class IsFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and FacultyProfile.objects.filter(user=request.user).exists())


class CourseListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourseCreateSerializer
    permission_classes = [IsFaculty]

    @extend_schema(
        summary="List courses of the faculty",
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of courses created by the faculty.
        """
        faculty_profile = request.user.faculty_profile
        courses = Course.objects.filter(instructor=faculty_profile)

        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Enables faculty to create a course",
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new course.
        """
        faculty_profile = request.user.faculty_profile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instructor=faculty_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [IsFaculty]

    @extend_schema(
        summary="Retrieve a course",
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve a specific course using its course code.
        """
        course_code = kwargs.get('course_code')  
        faculty_profile = request.user.faculty_profile  
        course = get_object_or_404(Course, course_code=course_code, instructor=faculty_profile)  
        serializer = self.get_serializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update a course - Full Update",
        request=CourseDetailSerializer,
    )
    def put(self, request, *args, **kwargs):
        """
        Update a specific course using its course code."""
        course_code = kwargs.get('course_code')  
        faculty_profile = request.user.faculty_profile  
        course = get_object_or_404(Course, course_code=course_code, instructor=faculty_profile)  
        serializer = self.get_serializer(course, data=request.data)  
        serializer.is_valid(raise_exception=True)
        serializer.save(instructor=faculty_profile)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete a course",
        responses={204: OpenApiResponse(description="No content")}
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete a specific course using its course code.
        """
        course_code = kwargs.get('course_code')  
        faculty_profile = request.user.faculty_profile  
        course = get_object_or_404(Course, course_code=course_code, instructor=faculty_profile)  
        course.delete()  
        return Response(
            {"message": "Course deleted successfully."},
            status=status.HTTP_200_OK
        )
    
    @extend_schema(
        summary="Update a course - Partial Update",
        request=CourseDetailSerializer,
    )
    def patch(self, request, *args, **kwargs):
        """
        Update a specific course using its course code.
        """
        course_code = kwargs.get('course_code')  
        faculty_profile = request.user.faculty_profile  
        course = get_object_or_404(Course, course_code=course_code, instructor=faculty_profile)  
        serializer = self.get_serializer(course, data=request.data, partial=True)  
        serializer.is_valid(raise_exception=True)
        serializer.save(instructor=faculty_profile)  
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and StudentProfile.objects.filter(user=request.user).exists())

class CourseRegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsStudent]

    @extend_schema(
        summary="Enables students to register for a course"
    )
    def post(self, request, *args, **kwargs):
        """
        Register for a specific course using its course code.
        """
        course_code = kwargs.get('course_code')
        course = get_object_or_404(Course, course_code=course_code)

        if not course.is_active:
            return Response({"detail": "This course is not active."}, status=status.HTTP_400_BAD_REQUEST)

        student_profile = request.user.student_profile

        if Registration.objects.filter(student=student_profile, course=course).exists():
            return Response({"detail": "You are already registered for this course."}, status=status.HTTP_400_BAD_REQUEST)

        approved_courses_count = student_profile.registrations.filter(status='approved').count()
        if approved_courses_count >= 2:
            return Response({"detail": "You cannot enroll in more than 2 courses."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(student=student_profile, course=course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination  

    @extend_schema(
        summary="List all courses",
        responses={200: CourseDetailSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve all available courses.
        """
        courses = Course.objects.all()
        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)