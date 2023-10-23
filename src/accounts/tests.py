from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from knox.models import AuthToken

from ..api.serializers import (
    LoginWithCredentialsSerializer,
    PublicAccountDataSerializer,
    RegisterAccountSerializer,
    UpdateAccountSerializer,
    UpdateCharactersSerializer,
    VerifyAccountSerializer,
)
from ..models import Account

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
        self.assertEqual(
            serializer.data,
            {
                "account_identifier": "test_account",
                "username": "test_user",
                "legacy_id": "null",
                "is_verified": False,
                "is_authorized_server": False,
                "characters_data": {},
            },
        )


class RegisterAccountSerializerTest(TestCase):
    def test_create_account(self):
        serializer = RegisterAccountSerializer(
            data={
                "email": "test@test.com",
                "account_identifier": "test_account",
                "username": "test_user",
                "password": faker.password(),
            }
        )
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
        serializer = LoginWithCredentialsSerializer(
            data={
                "email": "test@test.com",
                "password": password,
            }
        )
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
        serializer = UpdateAccountSerializer(
            account,
            data={
                "username": "new_user",
                "email": "new@test.com",
                "password": faker.password(),
            },
        )
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
        serializer = UpdateCharactersSerializer(
            account,
            data={
                "characters_data": {"character1": "data1"},
            },
        )
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        self.assertEqual(account.characters_data, {"character1": "data1"})


# Add test case classes for each view here
class PublicAccountDataViewTest(TestCase):
    """Test case for the PublicAccountDataView."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for the test case."""
        cls.account = Account.objects.create(
            email="test@test.com",
            account_identifier="test_account",
            username="test_user",
            password=faker.password(),
        )

    def test_get(self):
        """Test the GET method of the view."""
        response = self.client.get(reverse('public_account_data', kwargs={'pk': self.account.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), PublicAccountDataSerializer(self.account).data)

class LoginWithTokenViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password=faker.password())
        self.token = AuthToken.objects.create(self.user)[1]
        self.user = User.objects.create_user(username='test', password=faker.password())
        response = self.client.post(reverse('register_account'), {'username': 'test', 'password': faker.password(), 'email': 'test@test.com'})
        self.user = User.objects.create_user(username='test', password=faker.password())
        self.user = User.objects.create_user(username='test', password=faker.password())
        self.user = User.objects.create_user(username='test', password=faker.password())
        self.user = User.objects.create_user(username='test', password=faker.password())
        self.token = AuthToken.objects.create(self.user)[1]

    def test_post(self):
        response = self.client.post(reverse('login_with_token'), {'token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user'], PublicAccountDataSerializer(self.user).data)

class LoginWithCredentialsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_post(self):
        response = self.client.post(reverse('login_with_credentials'), {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user'], PublicAccountDataSerializer(self.user).data)

class RegisterAccountViewTest(TestCase):
    def test_post(self):
        response = self.client.post(reverse('register_account'), {'username': 'test', 'password': 'test', 'email': 'test@test.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['username'], 'test')

class UpdateAccountViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_post(self):
        self.client.login(username='test', password='test')
        response = self.client.post(reverse('update_account'), {'username': 'new_test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'new_test')

class UpdateCharactersViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_post(self):
        self.client.login(username='test', password='test')
        response = self.client.post(reverse('update_characters'), {'characters_data': {'character1': 'data1'}})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['characters_data'], {'character1': 'data1'})

class RequestVerificationTokenViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_get(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('request_verification_token'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['account_identifier'], self.user.account_identifier)

class VerifyAccountViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_post(self):
        response = self.client.post(reverse('verify_account'), {'account_identifier': self.user.account_identifier})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, PublicAccountDataSerializer(self.user).data)
