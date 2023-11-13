from django.contrib import admin

from .models import Character, Other, PolyPhrase


@admin.register(Other)
class OtherAdminView(admin.ModelAdmin):
    pass


@admin.register(PolyPhrase)
class PolyPhraseAdminView(admin.ModelAdmin):
    pass


@admin.register(Character)
class CharacterAdminView(admin.ModelAdmin):
    pass
