from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .serializers import FacultyLoginSerializer, StudentLoginSerializer, CreateStudentSerializer, CreateFacultySerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

class FacultyLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request=FacultyLoginSerializer,
        summary="Faculty Login",
        description="Authenticates faculty and returns JWT tokens."
    )
    def post(self, request):
        serializer = FacultyLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'id': user.id,
                    'username': user.username,
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request=StudentLoginSerializer,
        summary="Student Login",
        description="Authenticates student and returns JWT tokens."
    )
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'id': user.id,
                    'username': user.username,
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateStudentView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateStudentSerializer
    
    @extend_schema(
        request=CreateStudentSerializer,
        summary="Create Student Account",
        description="Creates a new student account with user and profile."
    )
    def post(self, request):
        serializer = CreateStudentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                student = serializer.save()
                # Generate tokens for immediate login
                refresh = RefreshToken.for_user(student.user)
                
                return Response({
                    'message': 'Student account created successfully',
                    'token': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    },
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateFacultyView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateFacultySerializer

    @extend_schema(
        request=CreateFacultySerializer,
        summary="Create Faculty Account",
        description="Creates a new faculty account with user and profile."
    )
    def post(self, request):
        serializer = CreateFacultySerializer(data=request.data)
        if serializer.is_valid():
            try:
                faculty = serializer.save()
                # Generate tokens for immediate login
                refresh = RefreshToken.for_user(faculty.user)
                
                return Response({
                    'message': 'Faculty account created successfully',
                    'token': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    },
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)