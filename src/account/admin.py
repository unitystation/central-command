from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


@admin.register(Account)
class AccountAdmin(UserAdmin):
    fieldsets = (
        ('Account data', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        })
    )
    add_fieldsets = (
        ('Account data', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    list_display = ['user_id', 'email', 'username', 'is_staff', 'is_active']
    readonly_fields = ['user_id']
    list_editable = ['email', 'username']


admin.site.unregister(Group)
