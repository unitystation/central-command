from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdminView(admin.ModelAdmin):
    list_display = (
        "email",
        "is_active",
        "unique_identifier",
        "username",
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
                    "is_verified",
                ),
            },
        ),
        ("Legacy", {"classes": ("wide",), "fields": ("legacy_id",)}),
    )
