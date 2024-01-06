from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("occweb.urls")),
    path("admin/", admin.site.urls),
]
