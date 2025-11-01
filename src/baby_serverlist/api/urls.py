from django.urls import path

from .views import (
    CreateBabyServerView,
    ListBabyServersView,
    ListOwnedBabyServersView,
    PostServerStatusView,
    RegenerateServerlistTokenView,
)

app_name = "baby_serverlist"
urlpatterns = [
    path("status/", PostServerStatusView.as_view(), name="report-status"),
    path("servers/create/", CreateBabyServerView.as_view(), name="create"),
    path("servers/owned/", ListOwnedBabyServersView.as_view(), name="list-owned"),
    path("servers/", ListBabyServersView.as_view(), name="list"),
    path("servers/regenerate-token/", RegenerateServerlistTokenView.as_view(), name="regenerate-token"),
]
