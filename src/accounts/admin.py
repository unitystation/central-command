from django.contrib import admin

from .models import Account, AccountConfirmation, PasswordResetRequestModel


class AccountConfirmationInline(admin.TabularInline):
    model = AccountConfirmation
    extra = 0
    readonly_fields = ("token", "created_at", "is_token_valid_display")

    def is_token_valid_display(self, instance):
        return instance.is_token_valid()

    is_token_valid_display.short_description = "Is Token Valid"


class PasswordResetRequestInline(admin.TabularInline):
    model = PasswordResetRequestModel
    extra = 0
    readonly_fields = ("token", "created_at", "is_token_valid_display")

    def is_token_valid_display(self, instance):
        return instance.is_token_valid()

    is_token_valid_display.short_description = "Is Token Valid"


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
    inlines = [AccountConfirmationInline, PasswordResetRequestInline]
