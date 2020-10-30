from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ("email", "username", "uid", "admin", "staff", "superuser")
    search_fields = ("email", "username", "uid")
    readonly_fields = ["uid"]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)


