from django.contrib import admin

from .models import BabyServer


@admin.register(BabyServer)
class BabyServerAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "whitelisted", "serverlist_token")
    search_fields = ("id", "owner__email", "owner__unique_identifier")
    list_filter = ("whitelisted",)
