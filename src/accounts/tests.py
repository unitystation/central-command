from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Account
from ..api.serializers import (
    PublicAccountDataSerializer,
    RegisterAccountSerializer,
    LoginWithCredentialsSerializer,
    UpdateAccountSerializer,
    UpdateCharactersSerializer,
    VerifyAccountSerializer,
)
from faker import Faker

faker = Faker()

User = get_user_model()

class AccountModelTest(TestCase):
    def test_create_account(self):
        password = faker.password()
        account = Account.objects.create(
            email="test@test.com",
            account_identifier="test_account",
            username="test_user",
            password=password,
        )
        self.assertEqual(account.email, "test@test.com")
        self.assertEqual(account.account_identifier, "test_account")
        self.assertEqual(account.username, "test_user")

class PublicAccountDataSerializerTest(TestCase):
    def test_serialize_account(self):
        account = Account.objects.create(
            email="test@test.com",
            account_identifier="test_account",
            username="test_user",
            password=faker.password(),
        )
        serializer = PublicAccountDataSerializer(account)
        self.assertEqual(serializer.data, {
            "account_identifier": "test_account",
            "username": "test_user",
            "legacy_id": "null",
            "is_verified": False,
            "is_authorized_server": False,
            "characters_data": {},
        })

class RegisterAccountSerializerTest(TestCase):
    def test_create_account(self):
        serializer = RegisterAccountSerializer(data={
            "email": "test@test.com",
            "account_identifier": "test_account",
            "username": "test_user",
            "password": faker.password(),
        })
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        self.assertEqual(account.email, "test@test.com")
        self.assertEqual(account.account_identifier, "test_account")
        self.assertEqual(account.username, "test_user")

class LoginWithCredentialsSerializerTest(TestCase):
    def test_authenticate_account(self):
        password = faker.password()
        Account.objects.create_user(
            email="test@test.com",
            account_identifier="test_account",
            username="test_user",
            password=password,
        )
        serializer = LoginWithCredentialsSerializer(data={
            "email": "test@test.com",
            "password": password,
        })
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data
        self.assertEqual(account.email, "test@test.com")
        self.assertEqual(account.account_identifier, "test_account")
        self.assertEqual(account.username, "test_user")

class UpdateAccountSerializerTest(TestCase):
    def test_update_account(self):
        password = faker.password()
        account = Account.objects.create_user(
            email="test@test.com",
            account_identifier="test_account",
            username="test_user",
            password=password,
        )
        serializer = UpdateAccountSerializer(account, data={
            "username": "new_user",
            "email": "new@test.com",
            "password": faker.password(),
        })
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        self.assertEqual(account.email, "new@test.com")
        self.assertEqual(account.username, "new_user")

class UpdateCharactersSerializerTest(TestCase):
    def test_update_characters(self):
        account = Account.objects.create_user(
            email="test@test.com",
            account_identifier="test_account",
            username="test_user",
            password=faker.password(),
        )
        serializer = UpdateCharactersSerializer(account, data={
            "characters_data": {"character1": "data1"},
        })
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        self.assertEqual(account.characters_data, {"character1": "data1"})

class VerifyAccountSerializerTest(TestCase):
    def test_verify_account(self):
        account = Account.objects.create_user(
            email="test@test.com",
            account_identifier="test_account",
            username="test_user",
            password=faker.password(),
        )
        serializer = VerifyAccountSerializer(data={
            "account_identifier": "test_account",
            "verification_token": account.verification_token,
        })
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data
        self.assertEqual(account.email, "test@test.com")
        self.assertEqual(account.account_identifier, "test_account")
        self.assertEqual(account.username, "test_user")
