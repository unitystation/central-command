from django.contrib import admin

from .models import Account, AccountConfirmation, PasswordResetRequestModel


class AccountConfirmationInline(admin.TabularInline):
    model = AccountConfirmation
    extra = 0
    readonly_fields = ("token", "created_at", "is_token_valid_display")

    def is_token_valid_display(self, instance):
        return instance.is_token_valid()

    is_token_valid_display.short_description = "Is Token Valid"  # type: ignore[attr-defined]


class PasswordResetRequestInline(admin.TabularInline):
    model = PasswordResetRequestModel
    extra = 0
    readonly_fields = ("token", "created_at", "is_token_valid_display")

    def is_token_valid_display(self, instance):
        return instance.is_token_valid()

    is_token_valid_display.short_description = "Is Token Valid"  # type: ignore[attr-defined]


@admin.register(Account)
class AccountAdminView(admin.ModelAdmin):
    list_display = (
        "unique_identifier",
        "email",
        "username",
        "is_confirmed",
        "is_verified",
        "is_active",
        "is_staff",
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
                    "is_staff",
                ),
            },
        ),
        ("Legacy", {"classes": ("wide",), "fields": ("legacy_id",)}),
    )
    inlines = [AccountConfirmationInline, PasswordResetRequestInline]
    list_filter = ("is_staff", "is_verified", "is_confirmed", "is_active")
    search_fields = (
        "email__icontains",
        "username__icontains",
        "unique_identifier__icontains",
    )
