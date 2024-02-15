from accounts.models import Account  # type: ignore
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LoginCredentialsTest(APITestCase):
    def setUp(self):
        self.url = reverse("account:login-credentials")
        self.valid_account = Account.objects.create_user(
            username="validUser",
            email="validUser@valid.com",
            unique_identifier="validUser",
        )

        self.valid_account.set_password("aValidPss963")
        self.valid_account.is_confirmed = True
        self.valid_account.save()
        self.valid_login_data = {
            "email": "validUser@valid.com",
            "password": "aValidPss963",
        }

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.url, self.valid_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        data = {
            "email": "wrongUser@invalid.com",
            "password": "wrongPassword",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_unconfirmed_account(self):
        self.valid_account.is_confirmed = False
        self.valid_account.save()

        response = self.client.post(self.url, self.valid_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_inactive_account(self):
        self.valid_account.is_active = False
        self.valid_account.save()

        response = self.client.post(self.url, self.valid_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_invalid_email(self):
        data = {
            "email": "invalidEmail",
            "password": "aValidPss963",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
