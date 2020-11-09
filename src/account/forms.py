from django.conf import settings
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django_email_verification import sendConfirm

from .models import Account


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("email", "username")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit and settings.REQUIRE_EMAIL_CONFIRMATION:
            sendConfirm(user)
        elif commit:
            user.is_active = True
            user.save()
        return user


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ("email", "username")
