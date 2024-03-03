from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..models import Account, AccountConfirmation


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

    def validate_password(self, value: str):
        # Validate the password using Django's built-in validators
        temp_user = Account(
            unique_identifier=self.initial_data.get("unique_identifier"),
            username=self.initial_data.get("username"),
        )
        validate_password(value, temp_user)
        return value

    def create(self, validated_data):
        """Create and return a new account"""
        account: Account = Account.objects.create_user(**validated_data)
        if settings.REQUIRE_EMAIL_CONFIRMATION:
            account.send_confirmation_mail()
        return account


class LoginWithCredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})


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


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={"input_type": "password"})

    def validate_password(self, value: str):
        # Validate the password using Django's built-in validators
        temp_user = Account(
            unique_identifier=self.initial_data.get("unique_identifier"),
            username=self.initial_data.get("username"),
        )
        validate_password(value, temp_user)
        return value


class ConfirmAccountSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        try:
            account_confirmation = AccountConfirmation.objects.get(token=data["token"])
        except AccountConfirmation.DoesNotExist:
            raise serializers.ValidationError({"token": "Token is invalid or expired."})

        if not account_confirmation.is_token_valid():
            raise serializers.ValidationError({"token": "Token is invalid or expired."})
        return {"token": data["token"]}


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
