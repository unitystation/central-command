import logging

from datetime import UTC, datetime
from typing import cast

from django.core import signing
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import Account
from baby_serverlist.models import SERVERLIST_TOKEN_SALT, BabyServer
from commons.cache import (
    get_baby_server_status,
    get_many_baby_server_statuses,
    set_baby_server_heartbeat,
    set_baby_server_status,
)
from commons.error_response import ErrorResponse

from .serializers import (
    BabyServerStatusListSerializer,
    BabyServerTokenSerializer,
    OwnedBabyServerSerializer,
    RegenerateServerlistTokenSerializer,
    ServerStatusSerializer,
)

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=extend_schema(
        request=ServerStatusSerializer,
        responses={
            200: OpenApiResponse(description="Status accepted and cached"),
            400: OpenApiResponse(description="Invalid payload or signature"),
        },
    )
)
class PostServerStatusView(GenericAPIView):
    """Accepts signed status payloads from baby servers and stores the latest state in cache.

    *** Public Endpoint ***
    """

    serializer_class = ServerStatusSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return ErrorResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

        status_payload = serializer.validated_data
        server_token = status_payload.get("ServerToken")

        try:
            payload = signing.loads(server_token, salt=SERVERLIST_TOKEN_SALT)
        except signing.BadSignature:
            return ErrorResponse("Invalid or expired token", status.HTTP_400_BAD_REQUEST)

        try:
            baby_server = BabyServer.objects.get(id=payload.get("server_id"), serverlist_token=server_token)
        except BabyServer.DoesNotExist:
            return ErrorResponse("Invalid or expired token", status.HTTP_400_BAD_REQUEST)

        server_id = str(baby_server.id)
        status_without_token = {key: value for key, value in status_payload.items() if key != "ServerToken"}

        set_baby_server_status(server_id, status_without_token)
        set_baby_server_heartbeat(server_id, datetime.now(tz=UTC).isoformat())

        logger.debug("Received server status update for server %s: %s", baby_server.id, status_without_token)

        return Response(status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        responses={201: BabyServerTokenSerializer},
    )
)
class CreateBabyServerView(GenericAPIView):
    """Creates a new baby server for the authenticated user and returns the freshly minted token.

    *** Requires Token Authentication. ***
    """

    queryset = BabyServer.objects.all()

    def post(self, request, *args, **kwargs):
        user = cast(Account, request.user)
        baby_server = BabyServer.objects.create(owner=user)

        return Response(
            {
                "id": str(baby_server.id),
                "serverlist_token": baby_server.serverlist_token,
                "whitelisted": baby_server.whitelisted,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(
    list=extend_schema(
        responses={200: OwnedBabyServerSerializer(many=True)},
    )
)
class ListOwnedBabyServersView(ListAPIView):
    """Lists the caller's baby servers with a derived `live` flag based on recent heartbeats.

    *** Requires Token Authentication. ***
    """

    def get_queryset(self):
        user = cast(Account, self.request.user)
        return BabyServer.objects.filter(owner=user).only("id", "whitelisted")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        data = [
            {
                "id": str(server.id),
                "whitelisted": server.whitelisted,
                "live": server.is_live(),
                "status": get_baby_server_status(server.id),
            }
            for server in queryset
        ]
        return Response(data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        responses={200: BabyServerStatusListSerializer},
    )
)
class ListBabyServersView(ListAPIView):
    """Return cached status payloads for all baby servers that have reported recently.

    *** Public Endpoint ***
    """

    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        servers = BabyServer.objects.filter(whitelisted=True)
        server_ids = [str(server.id) for server in servers]
        status_map = get_many_baby_server_statuses(server_ids)

        data = [
            status_map[server_id] for server_id in sorted(status_map.keys()) if isinstance(status_map[server_id], dict)
        ]

        return Response({"servers": data}, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        responses={200: BabyServerTokenSerializer},
    )
)
class RegenerateServerlistTokenView(GenericAPIView):
    """Regenerates a server's signed token after validating ownership.

    *** Requires Token Authentication. ***
    """

    serializer_class = RegenerateServerlistTokenSerializer
    queryset = BabyServer.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        server_id = serializer.validated_data["server_id"]

        try:
            baby_server: BabyServer = BabyServer.objects.get(id=server_id)
        except BabyServer.DoesNotExist:
            return ErrorResponse("Baby server not found", status.HTTP_404_NOT_FOUND)

        user = cast(Account, request.user)

        if baby_server.owner != user:
            return ErrorResponse(
                "You do not have permission to modify this baby server",
                status.HTTP_403_FORBIDDEN,
            )

        baby_server.serverlist_token = baby_server.generate_serverlist_token()
        baby_server.save(update_fields=["serverlist_token"])

        return Response(
            {
                "id": str(baby_server.id),
                "serverlist_token": baby_server.serverlist_token,
            },
            status=status.HTTP_200_OK,
        )
