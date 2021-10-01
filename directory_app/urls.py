"""
directory_app URL Configuration

"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from .serializer import UserViewSet
from .serializer import GroupViewSet
from .serializer import SubjectViewSet
from .serializer import TeacherViewSet


from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Directory API",
        default_version = "v1",
        description = "APIs for the Direcotry App",

    ),
    public = True,
    permission_classes = [permissions.AllowAny,]
)

# schema_view = get_swagger_view(title='Directory API')


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'Users', UserViewSet)
router.register(r'Groups', GroupViewSet)
router.register(r'Subjects', SubjectViewSet)
router.register(r'Teachers', TeacherViewSet)

app_name = 'directory_app'

urlpatterns = [
    path('admin', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-docs/', schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('api-redoc/', schema_view.with_ui('redoc',cache_timeout=0),name='schema-redoc'),
    path('', include(router.urls)),
    path('celery', include('main_app.urls')),

# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)