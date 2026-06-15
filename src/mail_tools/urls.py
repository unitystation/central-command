from django.urls import path

from . import views

app_name = "mail_tools"

urlpatterns = [
    path("", views.preview_list, name="list"),
    path("preview/<slug:slug>/", views.preview_detail, name="detail"),
    path("broadcast/", views.broadcast_email, name="broadcast"),
]
