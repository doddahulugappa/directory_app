"""
directory_app URL Configuration

"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from directory_app.schema import schema
from django.contrib.auth import views as auth_views #new

from rest_framework import routers
from . import settings

from . import views
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
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-docs/', schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('api-redoc/', schema_view.with_ui('redoc',cache_timeout=0),name='schema-redoc'),
    path('rest-api/', include(router.urls)),
    path('celery/', include('main_app.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True,schema=schema)),
    path('', views.index, name="index"),
    path('del-teacher/<int:id>/', views.delete_teacher, name="delete_teacher"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), #new
    path('logout/',auth_views.LogoutView.as_view(),{'next_page':settings.LOGOUT_REDIRECT_URL},name="logout"),
    path('export/',views.export_data, name="export"),
    path('export-popup/',views.export_popup, name="export-popup"),
    path('import/',views.upload_data, name="import"),

# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)