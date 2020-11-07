from rest_framework import serializers
from persistence.models import PolyPhrase


class PolyPhrasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolyPhrase
        fields = ('phrase_id', 'said_by', 'phrase')
