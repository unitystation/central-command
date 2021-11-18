from rest_framework import serializers
from ..models import Other, PolyPhrase

class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = ("account", "other_data",)


class PolyPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolyPhrase
        fields = ("id", "said_by", "phrase")