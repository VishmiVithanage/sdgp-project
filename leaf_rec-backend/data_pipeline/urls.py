from django.urls import path, include, re_path

from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import ProcessImageView, FileUploadView


schema_view = get_schema_view(
    openapi.Info(
        title="Data Pipeline",
        default_version='v1',
        contact=openapi.Contact(email="vikumdabare@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('reswagger/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('processed_images/', ProcessImageView.as_view()),
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
]
