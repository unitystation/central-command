from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account, PasswordResetRequestModel


def get_reset_url(token):
    return reverse("account:reset-password-token", kwargs={"reset_token": token})


class PasswordResetTest(APITestCase):
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

        self.url_request = reverse("account:reset-password")

    def test_request_password_reset_with_valid_email(self):
        data = {"email": "validUser@valid.com"}

        response = self.client.post(self.url_request, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(PasswordResetRequestModel.objects.count(), 1)
        password_reset_request = PasswordResetRequestModel.objects.first()
        self.assertIsNotNone(password_reset_request)

    def test_request_password_reset_with_invalid_email(self):
        data = {"email": "invalid@mail.com"}

        response = self.client.post(self.url_request, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # We don't want to give away if an email is valid or not
        self.assertEqual(PasswordResetRequestModel.objects.count(), 0)  # No password reset request should be created

    def test_reset_password_with_valid_token(self):
        data = {"email": "validUser@valid.com"}

        self.client.post(self.url_request, data, format="json")
        reset_token = PasswordResetRequestModel.objects.first().token  # type: ignore
        url = get_reset_url(reset_token)

        data = {"password": "newPss963!"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Account.objects.count(), 1)  # there is only one account in the database
        self.assertEqual(PasswordResetRequestModel.objects.count(), 0)  # The reset token should be deleted after use
        account = Account.objects.first()
        self.assertTrue(account.check_password(data["password"]))  # type: ignore
