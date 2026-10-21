"""Корневые маршруты проекта: каждый раздел подключается через include()."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("students/", include("students.urls")),
    path("teachers/", include("teachers.urls")),
    path("courseworks/", include("courseworks.urls")),
]
