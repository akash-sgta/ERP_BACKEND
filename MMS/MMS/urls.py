"""
URL configuration for MMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from MMS._views.logger import logger_view

SWAGGER = "swagger"
REDOC = "redoc"

schema_view = get_schema_view(
    openapi.Info(
        title="Medical Management System",
        default_version="v1",
        description="API Documentation",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="alphatrionakash@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    # =========================================================
    re_path(
        r"^admin/",
        admin.site.urls,
    ),
    re_path(
        r"^log/",
        logger_view,
    ),
    # =========================================================
    re_path(
        r"^doc/swagger/",
        schema_view.with_ui(SWAGGER, cache_timeout=0),
        name="doc_swagger",
    ),
    re_path(
        r"^doc/redoc/",
        schema_view.with_ui(REDOC, cache_timeout=0),
        name="doc_redoc",
    ),
    # =========================================================
    re_path(
        r"^util/",
        include("util.urls"),
    ),
    re_path(
        r"^profile/",
        include("profile.urls"),
    ),
    re_path(
        r"^patient/",
        include("patient.urls"),
    ),
    re_path(
        r"^staff/",
        include("staff.urls"),
    ),
    # =========================================================
    # re_path(r"^action/", include("util.urls"),),
]
