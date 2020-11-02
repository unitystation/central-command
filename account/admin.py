from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreationForm, AccountChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = get_user_model()

    # list_display = ['hardware_id', 'user_id', 'username', 'email']
    list_display = ["email", "username", "user_id", "hardware_id"]


admin.site.register(get_user_model(), CustomUserAdmin)