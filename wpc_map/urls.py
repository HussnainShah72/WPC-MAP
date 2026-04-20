from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("panel/admin/", include("core.admin_urls")),
    path("auth/", include("accounts.urls")),
    path("facilities/", include("facilities.urls")),
    path("", include("core.urls")),
]
