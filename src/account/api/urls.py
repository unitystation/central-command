from django.urls import path

from account.api.views import (
    register_account_view,
    account_by_identifiers_view,
    character_by_identifier_view,
)

app_name = "account"

urlpatterns = [
    path("register/", register_account_view, name="Register"),
    path("get_account/", account_by_identifiers_view, name="Get Account"),
    path("get_character", character_by_identifier_view, name="Get Character"),
]
