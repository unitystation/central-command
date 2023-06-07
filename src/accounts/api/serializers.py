from django.conf import settings
from django.contrib.auth import authenticate
from django_email_verification import sendConfirm
from rest_framework import serializers

from ..models import Account


class PublicAccountDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "account_identifier",
            "username",
            "legacy_id",
            "is_verified",
            "is_authorized_server",
            "characters_data",
        )


class RegisterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("account_identifier", "username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Create and return a new account"""
        account = Account.objects.create_user(**validated_data)
        if settings.REQUIRE_EMAIL_CONFIRMATION:
            sendConfirm(account)
        return account


class LoginWithCredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        account = authenticate(username=data["email"], password=data["password"])
        if account is None:
            raise serializers.ValidationError("Unable to login with provided credentials.")
        if not account.is_active:
            raise serializers.ValidationError(
                "This account hasn't done the mail confirmation step or has been disabled."
            )
        return account


class UpdateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        old_email = instance.email
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.set_password(validated_data.get("password", instance.password))

        if old_email != instance.email and settings.REQUIRE_EMAIL_CONFIRMATION:
            instance.is_active = False
            sendConfirm(instance)

        instance.save()
        return instance


class UpdateCharactersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("characters_data",)

    def update(self, instance, validated_data):
        instance.characters_data = validated_data.get("characters_data", instance.characters_data)
        instance.save()
        return instance


class VerifyAccountSerializer(serializers.Serializer):
    account_identifier = serializers.CharField()
    verification_token = serializers.UUIDField()

    def validate(self, data):
        account = Account.objects.get(account_identifier=data["account_identifier"])

        data_token = data["verification_token"]
        account_token = account.verification_token

        if account_token != data_token:
            raise serializers.ValidationError(
                "Verification token seems invalid or maybe outdated. Try requesting a new one."
            )
        return account
