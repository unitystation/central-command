from unittest.mock import patch

from django.test import SimpleTestCase

from commons import cache as cache_module


class CommonsCacheTests(SimpleTestCase):
    def test_set_baby_server_status_uses_ephemeral_timeout(self) -> None:
        payload = {"ServerName": "test"}
        server_id = "server-123"

        with patch.object(cache_module, "cache") as fake_cache:
            cache_module.set_baby_server_status(server_id, payload)

        fake_cache.set.assert_called_once_with(
            f"{cache_module.SERVER_STATUS_KEY_PREFIX}{server_id}",
            payload,
            timeout=cache_module.BABY_SERVER_STATUS_TTL_SECONDS,
        )

    def test_set_baby_server_heartbeat_uses_ephemeral_timeout(self) -> None:
        timestamp = "2024-01-01T00:00:00+00:00"
        server_id = "server-456"

        with patch.object(cache_module, "cache") as fake_cache:
            cache_module.set_baby_server_heartbeat(server_id, timestamp)

        fake_cache.set.assert_called_once_with(
            f"{cache_module.SERVER_HEARTBEAT_KEY_PREFIX}{server_id}",
            timestamp,
            timeout=cache_module.BABY_SERVER_HEARTBEAT_TTL_SECONDS,
        )
