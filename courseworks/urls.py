from django.urls import path

from courseworks import views

app_name = "courseworks"

urlpatterns = [
    path("", views.coursework_list, name="list"),
    path("active/", views.active_courseworks, name="active"),
    path("by-status/", views.by_status, name="by_status"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:coursework_id>/", views.coursework_detail, name="detail"),
]
