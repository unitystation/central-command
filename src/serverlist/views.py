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
        data = json.loads(request.body)
        name = data.get("name")
        ip_address = data.get("ip_address")
        port = data.get("port")
        player_count = data.get("player_count")
        image_link = data.get("image_link")

        existing_server = Server.objects.filter(name=name).first()
        if existing_server:
            # In case the server updates its info quickly before the 10 seconds pass,
            # we update everything while we're updating the experitation date as well
            existing_server.ip_address = ip_address
            existing_server.port = port
            existing_server.player_count = player_count
            existing_server.image_link = image_link
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
