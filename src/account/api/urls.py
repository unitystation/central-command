from knox import views as knox_views
from django.urls import path

from account.api.views import (
    LoginView,
    RegisterAccountView,
    account_by_id_view,
    character_by_id_view,
)

app_name = "account"

urlpatterns = [
    path("register/", RegisterAccountView.as_view(), name="Register"),
    path("login/", LoginView.as_view(), name="Login"),
    path("logout/", knox_views.LogoutView.as_view(), name="Logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="Logout All"),
    path("users/<user_id>/", account_by_id_view, name="Get account"),
    path("users/<user_id>/character/", character_by_id_view, name="Get Character"),
]
