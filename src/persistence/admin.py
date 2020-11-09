from django.contrib import admin

from .models import Book, BookPage, PolyPhrase, BookCategory


class InlineBookPage(admin.StackedInline):
    model = BookPage
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ["title", "categories"]
    inlines = [InlineBookPage]

    list_display = ["title", "isbn"]
    list_filter = ["categories"]
    search_fields = ["title", "isbn"]


admin.site.register(PolyPhrase)
admin.site.register(BookCategory)
