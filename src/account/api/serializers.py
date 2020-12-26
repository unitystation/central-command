import django.contrib.auth.password_validation as validators

from django.conf import settings
from django.core import exceptions
from rest_framework import serializers
from django_email_verification import sendConfirm

from account.models import Account


class RegisterAccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Account
        fields = ["email", "username", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        account = Account(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )

        password = self.validated_data["password"]
        account.set_password(password)

        if settings.REQUIRE_EMAIL_CONFIRMATION:
            sendConfirm(account)
        else:
            account.save()

        return account

    def validate(self, data):
        filtered_data = dict(data)
        filtered_data.pop("password2")
        account = Account(**filtered_data)

        errors = dict()

        if data.get("password") != data.get("password2"):
            errors["password"] = "Passwords must match."

        try:
            validators.validate_password(data.get("password"), account)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterAccountSerializer, self).validate(data)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["email", "username", "user_id", "character_setting"]
