from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('faculty-courses/', views.CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('courses/<str:course_code>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
    path('register/<str:course_code>', views.CourseRegistrationAPIView.as_view(), name='course-register'),
    path('all-courses/', views.CourseListAPIView.as_view(), name='course-list-all'),
   
]