from django.urls import path

from teachers import views

app_name = "teachers"

urlpatterns = [
    path("", views.teacher_list, name="list"),
    path("free/", views.free_teachers, name="free"),
    path("<int:teacher_id>/", views.teacher_detail, name="detail"),
]
