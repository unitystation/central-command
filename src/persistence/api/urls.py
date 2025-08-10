from django.urls import path

from .views import (
    CreateCharacterView,
    CreateCharacterViewToken,
    DeleteCharacterView,
    DeleteCharacterViewToken,
    GenerateForkTokenView,
    GetAllCharactersByAccountView,
    GetCharacterByIdView,
    GetCompatibleCharacters,
    GetCompatibleCharactersToken,
    UpdateCharacterView,
    UpdateCharacterViewToken,
)

app_name = "persistence"

urlpatterns = [
    path("characters", GetAllCharactersByAccountView.as_view(), name="characters-all"),
    path("characters/create", CreateCharacterView.as_view(), name="characters-create"),
    path("characters/<int:pk>", GetCharacterByIdView.as_view(), name="characters-by-id"),
    path("characters/compatible", GetCompatibleCharacters.as_view(), name="characters-compatible"),
    path("characters/<int:pk>/update", UpdateCharacterView.as_view(), name="characters-patch"),
    path("characters/<int:pk>/delete", DeleteCharacterView.as_view(), name="characters-delete"),
    path(
        "characters/<int:pk>/updateToken", UpdateCharacterViewToken.as_view(), name="characters-patch-token"
    ),  # PutAccountsCharacterByIDByCharactersToken
    path(
        "characters/createToken", CreateCharacterViewToken.as_view(), name="characters-create-token"
    ),  # PostMakeAccountsCharacterByCharactersToken
    path(
        "characters/compatibleToken", GetCompatibleCharactersToken.as_view(), name="characters-compatible-token"
    ),  # GetCharactersByCharacterSheetToken
    path(
        "characters/<int:pk>/deleteToken", DeleteCharacterViewToken.as_view(), name="characters-delete-token"
    ),  # DeleteAccountsCharacterByIDByCharactersToken
    path("characters/GenForkToken", GenerateForkTokenView.as_view(), name="Gen-Fork-token"),
]
