from accounts.models import Account
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LoginTokenTest(APITestCase):
    def setUp(self):
        self.url = reverse("account:login-token")
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

        # needs to log in with credentials to get the token
        response = self.client.post(reverse("account:login-credentials"), self.valid_login_data, format="json")
        self.token = response.data["token"]

    def test_login_with_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidToken")
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_without_token(self):
        response = self.client.post(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
