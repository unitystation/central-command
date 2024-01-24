from django.contrib import admin

from .models import Account, AccountConfirmation, PasswordResetRequestModel


@admin.register(Account)
class AccountAdminView(admin.ModelAdmin):
    list_display = (
        "email",
        "is_active",
        "unique_identifier",
        "username",
        "is_confirmed",
        "is_verified",
        "legacy_id",
    )
    fieldsets = (
        (
            "Account basic data",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "unique_identifier",
                    "username",
                    "verification_token",
                ),
            },
        ),
        (
            "Authorization",
            {
                "classes": ("wide",),
                "fields": (
                    "is_active",
                    "is_confirmed",
                    "is_verified",
                ),
            },
        ),
        ("Legacy", {"classes": ("wide",), "fields": ("legacy_id",)}),
    )


@admin.register(AccountConfirmation)
class AccountConfirmationAdminView(admin.ModelAdmin):
    pass


@admin.register(PasswordResetRequestModel)
class PasswordResetRequestModelAdmin(admin.ModelAdmin):
    pass
