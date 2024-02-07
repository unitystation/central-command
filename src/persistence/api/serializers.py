from rest_framework import serializers

from ..models import Character


class CompatibleCharactersRequestSerializer(serializers.Serializer):
    fork_compatibility = serializers.CharField(max_length=25)
    character_sheet_version = serializers.CharField(max_length=10)


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ("id", "account", "fork_compatibility", "character_sheet_version", "data", "last_updated")

        read_only_fields = ("id", "last_updated")


class UpdateCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ("id", "account", "fork_compatibility", "character_sheet_version", "data", "last_updated")

        read_only_fields = ("id", "account", "last_updated")
