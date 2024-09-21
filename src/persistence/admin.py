from django.contrib import admin

from .models import Character


@admin.register(Character)
class CharacterAdminView(admin.ModelAdmin):
    readonly_fields = ("character_name", "last_updated")
