from django.contrib import admin

from .models import Other, PolyPhrase


@admin.register(Other)
class OtherAdminView(admin.ModelAdmin):
    pass


@admin.register(PolyPhrase)
class PolyPhraseAdminView(admin.ModelAdmin):
    pass
