from django.urls import path

from .views import (
    CreateCharacterView,
    DeleteCharacterView,
    GetAllCharactersByAccountView,
    GetCharacterByIdView,
    GetCompatibleCharacters,
    RandomPolyPhraseView,
    ReadOtherDataView,
    UpdateCharacterView,
    WriteOtherDataView,
    WritePolyPhraseView,
)

app_name = "persistence"

urlpatterns = [
    path("characters", GetAllCharactersByAccountView.as_view(), name="characters-all"),
    path("characters/<int:pk>", GetCharacterByIdView.as_view(), name="characters-by-id"),
    path("characters/compatible", GetCompatibleCharacters.as_view(), name="characters-compatible"),
    path("characters/create", CreateCharacterView.as_view(), name="characters-create"),
    path("characters/update/<int:pk>", UpdateCharacterView.as_view(), name="characters-patch"),
    path("characters/delete/<int:pk>", DeleteCharacterView.as_view(), name="characters-delete"),
    path("other-data/read", ReadOtherDataView.as_view(), name="read"),
    path("other-data/write", WriteOtherDataView.as_view(), name="write"),
    path("poly-says", RandomPolyPhraseView.as_view(), name="poly-says"),
    path("poly-hears", WritePolyPhraseView.as_view(), name="poly-hears"),
]
