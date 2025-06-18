from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'profiles', views.EmployeeProfileViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'educations', views.EducationViewSet)
router.register(r'certifications', views.CertificationViewSet)
router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]