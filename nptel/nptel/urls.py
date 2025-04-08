"""
URL configuration for nptel project.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('course/', include('course.urls')),
    path('user/', include('user.urls')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path('api/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

admin.site.site_header = 'NPTEL Admin'
admin.site.site_title = 'NPTEL Admin Portal'
admin.site.index_title= 'Admin Portal'