import json

from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Server


def server_list(request):
    servers = Server.objects.all()
    data = []
    ## TODO: ADD VALIDATION FOR APPROVED API KEYS SO THAT STRANGERS DONT SPAM STATIONHUB WITH INVALID SERVERS ##
    for server in servers:
        if server.is_expired():
            server.delete()
        else:
            data.append(
                {
                    "name": server.name,
                    "ip_address": server.ip_address,
                    "port": server.port,
                    "player_count": server.player_count,
                    "image_link": server.image_link,
                }
            )
    return JsonResponse(data, safe=False)


@csrf_exempt
def add_server(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
    try:
        server_validation = validate_server_info(request)
        if server_validation.status_code != 200:
            return server_validation
        data = json.loads(request.body)
        name = data.get("name")
        ip_address = data.get("ip_address")
        port = data.get("port")
        player_count = data.get("player_count")
        player_limit = data.get("player_limit")
        image_link = data.get("image_link")
        windows_build = data.get("player_count")
        linux_build = data.get("player_count")
        mac_build = data.get("player_count")
        build_version = data.get("player_count")
        code_scan_version = data.get("player_count")

        existing_server = Server.objects.filter(name=name).first()
        if existing_server:
            # In case the server updates its info quickly before the 10 seconds pass,
            # we update everything while we're updating the experitation date as well
            existing_server.ip_address = ip_address
            existing_server.port = port
            existing_server.player_count = player_count
            existing_server.player_limit = player_limit
            existing_server.image_link = image_link
            existing_server.windows_build = windows_build
            existing_server.linux_build = linux_build
            existing_server.mac_build = mac_build
            existing_server.build_version = build_version
            existing_server.code_scan_version = code_scan_version
            existing_server.updated_at = datetime.now()
            existing_server.save()
        else:
            Server.objects.create(
                name=name,
                ip_address=ip_address,
                port=port,
                player_count=player_count,
                image_link=image_link,
                updated_at=datetime.now(),
            )
        return JsonResponse({"success": "Server data added/updated successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def validate_server_info(request):
    data = json.loads(request.body)
    name = data.get("name")
    ip_address = data.get("ip_address")
    port = data.get("port")
    windows_build = data.get("player_count")
    linux_build = data.get("player_count")
    mac_build = data.get("player_count")
    build_version = data.get("player_count")
    code_scan_version = data.get("player_count")

    if name is None or ip_address is None or port is None:
        return JsonResponse(
            {
                "error": "Identifying server info are required, otherwise the server will not show up or be connectable on stationhub."
            },
            status=400,
        )

    if (
        windows_build is None
        or linux_build is None
        or mac_build is None
        or build_version is None
        or code_scan_version is None
    ):
        return JsonResponse({"error": "Missing build information."}, status=400)

    return JsonResponse({"success": "Server info validated successfully"}, status=200)
