from typing import Tuple

from django.contrib import admin
from django.db.models import Q, QuerySet
from django.http import HttpRequest

from .models import Character


@admin.register(Character)
class CharacterAdminView(admin.ModelAdmin):
    readonly_fields = ("character_name", "last_updated")
    list_filter = ("character_sheet_version", "account__unique_identifier")
    search_fields = ("data__Name__icontains", "account__unique_identifier__icontains", "account__email__icontains")

    def get_search_results(self, request: HttpRequest, queryset: QuerySet, search_term: str) -> Tuple[QuerySet, bool]:
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        queryset |= self.model.objects.filter(Q(data__Name__icontains=search_term))
        return queryset, use_distinct
