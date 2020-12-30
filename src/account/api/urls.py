from knox import views as knox_views
from django.urls import path

from account.api.views import (
    LoginView,
    RegisterAccountView,
    AccountByIdentifierView,
    CharacterByIdentifierView,
)

app_name = "account"

urlpatterns = [
    path("register/", RegisterAccountView.as_view(), name="Register"),
    path("login/", LoginView.as_view(), name="Login"),
    path("logout/", knox_views.LogoutView.as_view(), name="Logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="Logout All"),
    path("get_account/", AccountByIdentifierView.as_view(), name="Get Account"),
    path("get_character", CharacterByIdentifierView.as_view(), name="Get Character"),
]
