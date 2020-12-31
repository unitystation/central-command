from django.urls import path

from persistence.api.views import (
    poly_phrase_by_id_view,
    poly_store_phrase_view,
    poly_random_phrase_view,
)

app_name = "persistence"

urlpatterns = [
    path("polysays/", poly_random_phrase_view, name="Poly says"),
    path("polysays/<phrase_id>/", poly_phrase_by_id_view, name="Phrase by id"),
    path("post/polyphrase", poly_store_phrase_view, name="Post poly phrase"),
]
