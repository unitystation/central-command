from datetime import UTC, datetime, timedelta
from uuid import uuid4

from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account
from baby_serverlist.models import LIVE_HEARTBEAT_GRACE_SECONDS, BabyServer
from commons.cache import (
    BABY_SERVER_HEARTBEAT_TTL_SECONDS,
    get_baby_server_heartbeat,
    get_baby_server_status,
    set_baby_server_heartbeat,
    set_baby_server_status,
)


def _sample_status_payload(server_token: str) -> dict[str, object]:
    return {
        "ServerToken": server_token,
        "Passworded": False,
        "ServerName": "Unitystation - Playtest Server",
        "ForkName": "UnityStationDevelop",
        "BuildVersion": 25103114,
        "CurrentMap": "MainStations/SquareStation.json",
        "GameMode": "Secret",
        "IngameTime": "a lot",
        "RoundTime": "0",
        "PlayerCount": 0,
        "PlayerCountMax": 45,
        "ServerIP": "127.0.0.1",
        "ServerPort": 7777,
        "WinDownload": "https://example.com/win.zip",
        "OSXDownload": "https://example.com/osx.zip",
        "LinuxDownload": "https://example.com/linux.zip",
        "fps": 98,
        "GoodFileVersion": "0.31.0",
    }


class BabyServerAPITests(APITestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create_user(
            email="owner@example.com",
            password="password123",  # noqa: S106 - test-only credential
            unique_identifier="owner",
            username="Owner",
        )
        self.other_user = Account.objects.create_user(
            email="other@example.com",
            password="password123",  # noqa: S106 - test-only credential
            unique_identifier="otheruser",
            username="Other",
        )

    def tearDown(self) -> None:
        cache.clear()

    def test_create_baby_server_returns_token(self) -> None:
        self.client.force_authenticate(self.user)

        response = self.client.post(reverse("baby_serverlist:create"))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payload = response.json()
        self.assertIn("serverlist_token", payload)
        self.assertTrue(BabyServer.objects.filter(id=payload["id"]).exists())

    def test_regenerate_token_changes_token_for_owner(self) -> None:
        self.client.force_authenticate(self.user)
        baby_server = BabyServer.objects.create(owner=self.user)
        original_token = baby_server.serverlist_token

        response = self.client.post(
            reverse("baby_serverlist:regenerate-token"),
            {"server_id": str(baby_server.id)},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        baby_server.refresh_from_db()
        self.assertNotEqual(original_token, baby_server.serverlist_token)

    def test_regenerate_token_rejects_non_owner(self) -> None:
        baby_server = BabyServer.objects.create(owner=self.user)
        self.client.force_authenticate(self.other_user)

        response = self.client.post(
            reverse("baby_serverlist:regenerate-token"),
            {"server_id": str(baby_server.id)},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regenerate_token_not_found_returns_404(self) -> None:
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse("baby_serverlist:regenerate-token"),
            {"server_id": str(uuid4())},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_server_status_stores_payload_in_cache(self) -> None:
        baby_server = BabyServer.objects.create(owner=self.user, whitelisted=True)
        payload = _sample_status_payload(baby_server.serverlist_token)

        response = self.client.post(
            reverse("baby_serverlist:report-status"),
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cached_status = get_baby_server_status(str(baby_server.id))
        self.assertIsNotNone(cached_status)
        cached_status = cached_status or {}
        self.assertNotIn("ServerToken", cached_status)
        self.assertEqual(cached_status["ServerName"], payload["ServerName"])

        cached_heartbeat = get_baby_server_heartbeat(str(baby_server.id))
        self.assertIsNotNone(cached_heartbeat)

    def test_post_server_status_rejects_invalid_token(self) -> None:
        baby_server = BabyServer.objects.create(owner=self.user)
        payload = _sample_status_payload("invalid-token")

        response = self.client.post(
            reverse("baby_serverlist:report-status"),
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        cached_status = get_baby_server_status(str(baby_server.id))
        self.assertIsNone(cached_status)

    def test_list_owned_baby_servers_live_flag(self) -> None:
        self.client.force_authenticate(self.user)
        baby_server = BabyServer.objects.create(owner=self.user)

        response = self.client.get(reverse("baby_serverlist:list-owned"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()[0]["live"])

        set_baby_server_heartbeat(str(baby_server.id), datetime.now(tz=UTC).isoformat())

        response = self.client.get(reverse("baby_serverlist:list-owned"))
        self.assertTrue(response.json()[0]["live"])

        stale_time = datetime.now(tz=UTC) - timedelta(
            seconds=BABY_SERVER_HEARTBEAT_TTL_SECONDS + LIVE_HEARTBEAT_GRACE_SECONDS + 1
        )
        set_baby_server_heartbeat(str(baby_server.id), stale_time.isoformat())

        response = self.client.get(reverse("baby_serverlist:list-owned"))
        self.assertFalse(response.json()[0]["live"])

    def test_list_baby_servers_returns_whitelisted_status(self) -> None:
        baby_server = BabyServer.objects.create(owner=self.user, whitelisted=True)
        status_data = _sample_status_payload(baby_server.serverlist_token)
        status_without_token = status_data.copy()
        status_without_token.pop("ServerToken")

        set_baby_server_status(str(baby_server.id), status_without_token)

        response = self.client.get(reverse("baby_serverlist:list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.json()
        self.assertIn("servers", payload)
        self.assertEqual(len(payload["servers"]), 1)
        self.assertEqual(payload["servers"][0]["ServerName"], status_without_token["ServerName"])

    def test_list_baby_servers_ignores_non_whitelisted(self) -> None:
        non_whitelisted = BabyServer.objects.create(owner=self.user, whitelisted=False)
        set_baby_server_status(str(non_whitelisted.id), {"ServerName": "Hidden"})

        response = self.client.get(reverse("baby_serverlist:list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"servers": []})

    def test_baby_server_is_live_respects_heartbeat_ttl(self) -> None:
        baby_server = BabyServer.objects.create(owner=self.user)

        fresh_time = datetime.now(tz=UTC) - timedelta(
            seconds=BABY_SERVER_HEARTBEAT_TTL_SECONDS + LIVE_HEARTBEAT_GRACE_SECONDS - 1
        )
        set_baby_server_heartbeat(str(baby_server.id), fresh_time.isoformat())
        self.assertTrue(baby_server.is_live())

        stale_time = datetime.now(tz=UTC) - timedelta(
            seconds=BABY_SERVER_HEARTBEAT_TTL_SECONDS + LIVE_HEARTBEAT_GRACE_SECONDS + 1
        )
        set_baby_server_heartbeat(str(baby_server.id), stale_time.isoformat())
        stored = get_baby_server_heartbeat(str(baby_server.id))
        self.assertEqual(stored, stale_time.isoformat())
        self.assertFalse(baby_server.is_live())
