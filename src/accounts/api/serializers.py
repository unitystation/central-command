from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import authenticate
from django_email_verification import sendConfirm

from ..models import Account


class PublicAccountDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("account_identifier", "username", "is_verified", "characters_data")


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
            raise serializers.ValidationError(
                "Unable to login with provided credentials."
            )
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
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.set_password(validated_data.get("password", instance.password))
        instance.save()
        return instance


class UpdateCharactersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("characters_data",)

    def update(self, instance, validated_data):
        instance.characters_data = validated_data.get(
            "characters_data", instance.characters_data
        )
        instance.save()
        return instance
