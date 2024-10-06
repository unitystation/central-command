from django.contrib import admin

from .models import (
    AccountModerationInfo,
    CodeScanInformation,
    ServerAdmonition,
    ServerInformation,
)


class ServerAdmonitionInline(admin.TabularInline):
    model = ServerAdmonition
    extra = 1
    raw_id_fields = ["server"]
    fields = ["server", "created_at", "reason", "severity"]
    readonly_fields = ["created_at"]


@admin.register(CodeScanInformation)
class CodeScanInformationAdmin(admin.ModelAdmin):
    list_display = ["version"]


@admin.register(ServerInformation)
class ServerInformationAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "is_18_plus", "is_delisted"]
    search_fields = ["name", "owner__username"]
    list_filter = ["is_18_plus", "is_delisted"]
    raw_id_fields = ["owner", "code_scan_version"]


@admin.register(AccountModerationInfo)
class AccountModerationInfoAdmin(admin.ModelAdmin):
    list_display = ["account", "can_create_servers", "can_list_servers"]
    search_fields = ["account__username"]
    list_filter = ["can_create_servers", "can_list_servers"]
    raw_id_fields = ["account"]
