from django.urls import path

from .views import (
    CreateCharacterView,
    DeleteCharacterView,
    GetAllCharactersByAccountView,
    GetCharacterByIdView,
    GetCompatibleCharacters,
    UpdateCharacterView,
)

app_name = "persistence"

urlpatterns = [
    path("characters", GetAllCharactersByAccountView.as_view(), name="characters-all"),
    path("characters/create", CreateCharacterView.as_view(), name="characters-create"),
    path("characters/<int:pk>", GetCharacterByIdView.as_view(), name="characters-by-id"),
    path("characters/compatible", GetCompatibleCharacters.as_view(), name="characters-compatible"),
    path("characters/<int:pk>/update", UpdateCharacterView.as_view(), name="characters-patch"),
    path("characters/<int:pk>/delete", DeleteCharacterView.as_view(), name="characters-delete"),
]
