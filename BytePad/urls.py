from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger Options
schema_view = get_schema_view(
    openapi.Info(
        title="BytePad API",
        default_version="v1",
        description="API for BytePad For SDC-SI Major Project",
        contact=openapi.Contact(email="yash114bansal@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[JWTAuthentication],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("accounts/", include("accounts.urls")),
    path("papers/", include("papers.urls")),
    path("details/", include("details.urls")),
    path("attendence/",include("attendence.urls")),
    path("announcements/",include("announcement.urls")),
    path("time-table/",include("timetable.urls")),

    # Swagger documentation URLs
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
