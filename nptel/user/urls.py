from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('faculty/login/', views.FacultyLoginView.as_view(), name='faculty-login'),
    path('student/login/', views.StudentLoginView.as_view(), name='student-login'),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('student/register/', views.CreateStudentView.as_view(), name='student-register'),
    path('faculty/register/', views.CreateFacultyView.as_view(), name='faculty-register'),
]