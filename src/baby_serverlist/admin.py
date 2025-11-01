from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from .models import BabyServer


@admin.register(BabyServer)
class BabyServerAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "whitelisted", "serverlist_token_display")
    search_fields = ("id", "owner__email", "owner__unique_identifier")
    list_filter = ("whitelisted",)
    readonly_fields = ("serverlist_token",)
    change_form_template = "admin/baby_serverlist/babyserver/change_form.html"

    @admin.display(description="Server token", ordering="serverlist_token")
    def serverlist_token_display(self, obj: BabyServer) -> str:
        # Return the full token so it can be copied without Django's default truncation.
        return obj.serverlist_token

    def response_change(self, request: HttpRequest, obj: BabyServer) -> HttpResponse:
        if "_regenerate_token" in request.POST:
            obj.serverlist_token = obj.generate_serverlist_token()
            obj.save(update_fields=["serverlist_token"])
            self.message_user(request, "Server token regenerated.")
            return HttpResponseRedirect(request.path)
        return super().response_change(request, obj)
