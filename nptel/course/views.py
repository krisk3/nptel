from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course
from .serializers import CourseCreateSerializer, CourseDetailSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from user.models import FacultyProfile


# Create your views here.
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
        # Retrieve the FacultyProfile for the authenticated user
        faculty_profile = request.user.faculty_profile  # Corrected attribute name
        courses = Course.objects.filter(instructor=faculty_profile)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a course",
    )
    def post(self, request, *args, **kwargs):
        # Retrieve the FacultyProfile for the authenticated user
        faculty_profile = request.user.faculty_profile  # Corrected attribute name
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instructor=faculty_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#TODO: Complete Serializer for Course Detail
class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [IsFaculty]

    @extend_schema(
        summary="Retrieve a course",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a course - Full Update",
        request=CourseDetailSerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a course",
        responses={204: OpenApiResponse(description="No content")}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @extend_schema(
        summary="Update a course - Partial Update",
        request=CourseDetailSerializer,
    )
    def patch(self, serializer):
        serializer.save(instructor=self.request.user.facultyprofile)