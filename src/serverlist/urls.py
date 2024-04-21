from django.urls import path

from .views import server_list

urlpatterns = [
    path("serverlist/", server_list, name="server_list"),
]
