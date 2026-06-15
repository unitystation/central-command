from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account, AccountConfirmation


class ConfirmAccountTest(APITestCase):
    def setUp(self) -> None:
        cache.clear()
        self.account = Account.objects.create_user(
            username="confirmUser",
            email="confirm@example.com",
            unique_identifier="confirmUser",
        )
        self.account.set_password("aValidPss963")
        self.account.is_confirmed = False
        self.account.save()

        self.confirmation = AccountConfirmation.objects.create(account=self.account, token="confirm-token")  # noqa: S106 - test-only credential
        self.url = reverse("account:confirm")

    def test_confirm_account_with_valid_token(self) -> None:
        response = self.client.post(self.url, {"token": self.confirmation.token}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.account.refresh_from_db()
        self.assertTrue(self.account.is_confirmed)
        self.assertFalse(AccountConfirmation.objects.filter(pk=self.confirmation.pk).exists())

    def test_confirm_account_with_invalid_token(self) -> None:
        response = self.client.post(self.url, {"token": "invalid-token"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.account.refresh_from_db()
        self.assertFalse(self.account.is_confirmed)
