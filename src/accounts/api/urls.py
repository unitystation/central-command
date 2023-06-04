from django.urls import path
from knox import views as knox_views

from .views import (
    LoginWithCredentialsView,
    LoginWithTokenView,
    PublicAccountDataView,
    RegisterAccountView,
    RequestVerificationTokenView,
    UpdateAccountView,
    UpdateCharactersView,
    VerifyAccountView,
)

app_name = "account"

urlpatterns = [
    path("login-token", LoginWithTokenView.as_view(), name="login-token"),
    path(
        "login-credentials",
        LoginWithCredentialsView.as_view(),
        name="login-credentials",
    ),
    path("register", RegisterAccountView.as_view(), name="register"),
    path("update-account", UpdateAccountView.as_view(), name="update"),
    path("update-characters", UpdateCharactersView.as_view(), name="update-characters"),
    path("account", PublicAccountDataView.as_view(), name="public-data"),
    path("account/<str:pk>", PublicAccountDataView.as_view(), name="public-data"),
    path("logout", knox_views.LogoutView.as_view(), name="logout"),
    path("logoutall", knox_views.LogoutAllView.as_view(), name="logoutall"),
    path(
        "request-verification-token",
        RequestVerificationTokenView.as_view(),
        name="request-verification-token",
    ),
    path("verify-account", VerifyAccountView.as_view(), name="verify-account"),
]
