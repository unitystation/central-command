from django.urls import path
from knox import views as knox_views

from .views import (
    ConfirmAccountView,
    LoginWithCredentialsView,
    LoginWithTokenView,
    RegisterAccountView,
    RequestPasswordResetView,
    RequestVerificationTokenView,
    ResendAccountConfirmationView,
    ResetPasswordView,
    UpdateAccountView,
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
    path("logout", knox_views.LogoutView.as_view(), name="logout"),
    path("logoutall", knox_views.LogoutAllView.as_view(), name="logoutall"),
    path(
        "request-verification-token",
        RequestVerificationTokenView.as_view(),
        name="request-verification-token",
    ),
    path("verify-account", VerifyAccountView.as_view(), name="verify-account"),
    path(
        "resend-account-confirmation",
        ResendAccountConfirmationView.as_view(),
        name="resend-account-confirmation",
    ),
    path("confirm-account", ConfirmAccountView.as_view(), name="confirm"),
    path(
        "reset-password/<str:reset_token>",
        ResetPasswordView.as_view(),
        name="reset-password-token",
    ),
    path("reset-password/", RequestPasswordResetView.as_view(), name="reset-password"),
]
