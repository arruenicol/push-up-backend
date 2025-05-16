from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from notiff import views

from users.views import UserViewSet
from courses.views import CourseViewSet, CourseGroupViewSet
from notifications.views import NotificationViewSet

# Configuración del router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'courses', CourseViewSet)
router.register(r'groups', CourseGroupViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    # API URLs
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Servir archivos estáticos y de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)