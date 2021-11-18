from knox import views as knox_views
from django.urls import path

from .views import (
    LoginWithTokenView,
    LoginWithCredentialsView,
    RegisterAccountView,
    UpdateAccountView,
    UpdateCharactersView,
    PublicAccountDataView,
)

app_name = "account"

urlpatterns = [
    path("login-token", LoginWithTokenView.as_view(), name="login-token"),
    path("login-credentials", LoginWithCredentialsView.as_view(), name="login-credentials"),
    path("register", RegisterAccountView.as_view(), name="register"),
    path("update-account", UpdateAccountView.as_view(), name="update"),
    path("update-characters", UpdateCharactersView.as_view(), name="update-characters"),
    path("account", PublicAccountDataView.as_view(), name="public-data"),
    path("account/<str:pk>", PublicAccountDataView.as_view(), name="public-data"),
    path("logout", knox_views.LogoutView.as_view(), name="logout"),
    path("logoutall", knox_views.LogoutAllView.as_view(), name="logoutall"),
]