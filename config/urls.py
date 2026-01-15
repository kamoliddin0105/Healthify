from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('location/', include('apps.location.urls')),
    path('api/clinic/', include('apps.clinic.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Task-Management Swagger",
            default_version='v1',
            description="Swagger foy Task-Management project, token authorization: user __/auth/token/__ API "
                        "then click authorize button and type __Bearer {token}__.",
            terms_of_service="https://domen.com/",
            contact=openapi.Contact(email="help@domen.com"),
            license=openapi.License(name="Task-Management License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny, ],
        # **SWAGGER_SETTINGS
    )
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]