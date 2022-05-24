"""SIGPEL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include

from api_rest.views import index

handler404 = "error.views.error_404"
handler500 = "error.views.error_500"
handler403 = "error.views.error_403"
handler400 = "error.views.error_400"

urlpatterns = [
    path("", index),
    path("media/", include("protected_media.urls")),
    re_path(r"^api/v1/", include("api_rest.urls", namespace="api_rest")),
    # re_path(r'^api/v1/session/', include('rest_auth.urls')),
    re_path("grappelli/", include("grappelli.urls")),
    re_path("admin/", admin.site.urls),
    # re_path(r"^admin/defender/", include("defender.urls")),
    # re_path(r'^ltw/',include('useraudit.urls', namespace="useraudit")),
    re_path(r"^advanced_filters/", include("advanced_filters.urls")),
    # re_path(r'error/', include(('error.urls', 'error'), namespace='error')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
