from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('courses/', views.CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
] 