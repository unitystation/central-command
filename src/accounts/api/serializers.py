import secrets

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..models import Account, AccountConfirmation, PasswordResetRequestModel


class PublicAccountDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "unique_identifier",
            "username",
            "legacy_id",
            "is_verified",
        )


class RegisterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("unique_identifier", "username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Create and return a new account"""
        account: Account = Account.objects.create_user(**validated_data)
        if settings.REQUIRE_EMAIL_CONFIRMATION:
            account.send_confirmation_mail()
        return account


class LoginWithCredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        account: Account | None = authenticate(username=data["email"], password=data["password"])  # type: ignore[assignment]
        if account is None:
            raise serializers.ValidationError("Unable to login with provided credentials.")
        if not account.is_confirmed:
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
            instance.is_confirmed = False
            instance.send_confirmation_mail()

        instance.save()
        return instance


class VerifyAccountSerializer(serializers.Serializer):
    unique_identifier = serializers.CharField()
    verification_token = serializers.UUIDField()

    def validate(self, data):
        account = Account.objects.get(unique_identifier=data["unique_identifier"])

        data_token = data["verification_token"]
        account_token = account.verification_token

        if account_token != data_token:
            raise serializers.ValidationError(
                "Verification token seems invalid or maybe outdated. Try requesting a new one."
            )
        return account


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("password",)
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        # Validate the password using Django's built-in validators
        validate_password(value)
        return value


class ResetPasswordRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetRequestModel
        fields = ("email",)

    email = serializers.EmailField()

    def validate(self, data):
        email = data["email"]
        account = Account.objects.get(email=email)
        if account is None:
            raise serializers.ValidationError("Account with this email doesn't exist.")

        return {
            "token": secrets.token_urlsafe(32),
            "account": account,
        }

    def create(self, validated_data):
        return PasswordResetRequestModel.objects.create(**validated_data)


class ConfirmAccountSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        try:
            account_confirmation = AccountConfirmation.objects.get(token=data["token"])
        except AccountConfirmation.DoesNotExist:
            raise serializers.ValidationError("Token is invalid or expired.")

        if not account_confirmation.is_token_valid():
            raise serializers.ValidationError("Token is invalid or expired.")
        return account_confirmation


class ResendAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
