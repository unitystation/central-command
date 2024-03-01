from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account


class ServerVerificationTokenTest(APITestCase):
    def setUp(self):
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

        self.url_request = reverse("account:request-verification-token")
        self.url_verify = reverse("account:verify-account")

        response = self.client.post(reverse("account:login-credentials"), self.valid_login_data, format="json")
        self.token = response.data["token"]

    def test_request_verification_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(self.url_request, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_account(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(self.url_request, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("verification_token", response.data)
        verification_token = response.data["verification_token"]

        data = {"verification_token": verification_token, "unique_identifier": self.valid_account.unique_identifier}
        response = self.client.post(self.url_verify, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ver_token_without_auth(self):
        response = self.client.get(self.url_request, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_with_invalid_token(self):
        data = {"verification_token": "invalidToken", "unique_identifier": self.valid_account.unique_identifier}
        response = self.client.post(self.url_verify, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_with_invalid_identifier(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")
        response = self.client.get(self.url_request, format="json")

        data = {"verification_token": response.data["verification_token"], "unique_identifier": "invalidIdentifier"}
        response = self.client.post(self.url_verify, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
