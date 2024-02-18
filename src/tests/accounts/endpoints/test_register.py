from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account


class RegisterTest(APITestCase):
    def setUp(self):
        self.url = reverse("account:register")
        self.valid_data = {
            "email": "validUser@valid.com",
            "password": "aValidPss963",
            "unique_identifier": "validUser",
            "username": "validUser",
        }

    def test_register_valid_account(self):
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_account = Account.objects.get(email=self.valid_data["email"])
        self.assertIsNotNone(created_account)
        self.assertEqual(created_account.username, self.valid_data["username"])
        self.assertEqual(created_account.email, self.valid_data["email"])
        self.assertEqual(created_account.unique_identifier, self.valid_data["unique_identifier"])

    def test_register_with_invalid_email(self):
        data = self.valid_data.copy()
        data["email"] = "invalidEmail"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_too_common_password(self):
        data = self.valid_data.copy()
        data["password"] = "password"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_password_same_as_unique_identifier(self):
        data = self.valid_data.copy()
        data["password"] = "validUser"  # assuming 'validUser' is the unique_identifier
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_too_common_admin_password(self):
        data = self.valid_data.copy()
        data["password"] = "admin123"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_too_short_password(self):
        data = self.valid_data.copy()
        data["password"] = "short"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_valid_password(self):
        data = self.valid_data.copy()
        data["password"] = "aValidPss963"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_with_existing_email(self):
        data = self.valid_data.copy()
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_unique_identifier(self):
        data = self.valid_data.copy()
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data["email"] = "another-email@email.com"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_username(self):
        data = self.valid_data.copy()
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data["email"] = "another-email@mail.com"
        data["unique_identifier"] = "anotherUnique"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # existing username is allowed

    def test_register_with_missing_field(self):
        data = self.valid_data.copy()
        for field in data:
            data = self.valid_data.copy()
            data.pop(field)
            response = self.client.post(self.url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_confirmed_state_at_registering(self):
        data = self.valid_data.copy()
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_account = Account.objects.get(email=self.valid_data["email"])
        self.assertFalse(created_account.is_confirmed)
