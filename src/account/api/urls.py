from knox import views as knox_views
from django.urls import path

from account.api.views import Login, AccountById, CharacterById, RegisterAccount

app_name = "account"

urlpatterns = [
    path("register/", RegisterAccount.as_view(), name="Register"),
    path("login/", Login.as_view(), name="Login"),
    path("logout/", knox_views.LogoutView.as_view(), name="Logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="Logout All"),
    path("users/<user_id>/", AccountById.as_view(), name="Get account"),
    path("users/<user_id>/characters/", CharacterById.as_view(), name="Get Characters"),
]
