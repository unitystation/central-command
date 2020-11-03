from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from .models import Account


class AccountCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('email', 'username')


class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('email', 'username')
