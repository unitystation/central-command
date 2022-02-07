from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdminView(admin.ModelAdmin):
    list_display = (
        "email",
        "account_identifier",
        "username",
        "is_verified",
        "legacy_id",
        "characters_data",
        "is_authorized_server",
    )
    fieldsets = (
        (
            "Account basic data",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "account_identifier",
                    "username",
                    "verification_token",
                ),
            },
        ),
        ("Characters", {"classes": ("wide",), "fields": ("characters_data",)}),
        (
            "Authorization",
            {
                "classes": ("wide",),
                "fields": ("is_active", "is_verified", "is_authorized_server"),
            },
        ),
        ("Legacy", {"classes": ("wide",), "fields": ("legacy_id",)}),
    )
