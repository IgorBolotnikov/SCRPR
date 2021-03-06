"""personal_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from .sitemap import StaticViewSitemap

API_V1_PREFIX = "api/v1/"

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("scrpr.urls")),
    path("auth/", include("authentication.urls")),
    # API V1
    path(API_V1_PREFIX, include("api_v1.urls")),
    # JWT
    path(f"{API_V1_PREFIX}auth/obtain-token", obtain_jwt_token),
    path(f"{API_V1_PREFIX}auth/refresh-token", refresh_jwt_token),
    # Reset password
    re_path(
        r"^api/v1/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    # Tinymce app
    re_path(r"^tinymce/", include("tinymce.urls")),
    # robots.txt
    re_path(
        r"^robots.txt$",
        TemplateView.as_view(
            template_name="scrpr/robots.txt", content_type="text/plain"
        ),
    ),
    # Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "scrpr.views.page_not_found_view"
handler500 = "scrpr.views.internal_server_error_view"

# Django Debug Toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
