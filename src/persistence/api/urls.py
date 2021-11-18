from django.urls import path
from .views import (
    CreateOtherDataView,
    ReadOtherDataView,
    WriteOtherDataView,
    RandomPolyPhraseView,
    WritePolyPhraseView,
)

app_name = "persistence"

urlpatterns = [
    path("other-data/create", CreateOtherDataView.as_view(), name="create"),
    path("other-data/read", ReadOtherDataView.as_view(), name="read"),
    path("other-data/write", WriteOtherDataView.as_view(), name="write"),
    path("poly-says", RandomPolyPhraseView.as_view(), name="poly-says"),
    path("poly-hears", WritePolyPhraseView.as_view(), name="poly-hears"),
]
