from django.urls import path

from courseworks import views

app_name = "courseworks"

urlpatterns = [
    path("", views.coursework_list, name="list"),
    path("<int:coursework_id>/", views.coursework_detail, name="detail"),
]
