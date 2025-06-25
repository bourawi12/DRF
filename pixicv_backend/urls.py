from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from profiles import views
from profiles.auth_views import register, logout, user_profile, protected_test
from profiles.views import ProfileSkillsView ,ProfileProjectsView  # Import your new view here


# Create router and register viewsets
router = DefaultRouter()
router.register(r'profiles', views.EmployeeProfileViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'education', views.EducationViewSet)
router.register(r'certifications', views.CertificationViewSet)
router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints via router
    path('api/', include(router.urls)),

    # JWT Authentication endpoints
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/register/', register, name='register'),
    path('api/auth/logout/', logout, name='logout'),
    path('api/auth/user/', user_profile, name='user_profile'),
    path('api/auth/test/', protected_test, name='protected_test'),

    # Your new custom URL
    path('api/profiles/<int:profile_id>/skills/', ProfileSkillsView.as_view(), name='profile-skills'),
    path('api/profiles/<int:profile_id>/projects/', ProfileProjectsView.as_view(), name='profile-projects'),

    # DRF Browsable API (for development)
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
