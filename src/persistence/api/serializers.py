from rest_framework import serializers

from ..models import Character, Other, PolyPhrase


class CompatibleCharactersRequestSerializer(serializers.Serializer):
    fork_compatibility = serializers.CharField(max_length=25)
    character_sheet_version = serializers.CharField(max_length=10)


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = (
            "id",
            "account",
            "fork_compatibility",
            "character_sheet_version",
            "data",
        )

        read_only_fields = ("id",)


class UpdateCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = (
            "id",
            "account",
            "fork_compatibility",
            "character_sheet_version",
            "data",
        )

        read_only_fields = ("id", "account")


class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = (
            "account",
            "other_data",
        )


class PolyPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolyPhrase
        fields = ("id", "said_by", "phrase")
