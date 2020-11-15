from rest_framework import serializers

from persistence.models import PolyPhrase


class PolyPhrasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolyPhrase
        fields = ("id", "said_by", "phrase")
