from collections.abc import Iterable
from typing import Any

from django.core.cache import cache

from central_command.settings import BABY_SERVER_STATUS_TTL_SECONDS

SERVER_STATUS_KEY_PREFIX = "baby_server_status:"
SERVER_HEARTBEAT_KEY_PREFIX = "baby_server_heartbeat:"


def _status_key(server_id: str) -> str:
    """Build the cache key used to store a server's status payload."""
    return f"{SERVER_STATUS_KEY_PREFIX}{server_id}"


def _heartbeat_key(server_id: str) -> str:
    """Build the cache key used to store a server's last heartbeat timestamp."""
    return f"{SERVER_HEARTBEAT_KEY_PREFIX}{server_id}"


def set_baby_server_status(server_id: str, status: dict[str, Any]) -> None:
    """Persist the latest status payload for a server."""
    cache.set(_status_key(server_id), status, timeout=BABY_SERVER_STATUS_TTL_SECONDS)


def get_baby_server_status(server_id: str) -> dict[str, Any] | None:
    """Fetch the cached status payload for a server, if present."""
    cached = cache.get(_status_key(server_id))
    return cached if isinstance(cached, dict) else None


def get_many_baby_server_statuses(server_ids: Iterable[str]) -> dict[str, dict[str, Any]]:
    """Fetch cached statuses for a list of servers using a single multi-get call."""
    key_map = {_status_key(server_id): server_id for server_id in server_ids}
    raw = cache.get_many(key_map.keys())
    return {
        key_map[cache_key]: value for cache_key, value in raw.items() if isinstance(value, dict) and cache_key in key_map
    }


def set_baby_server_heartbeat(server_id: str, timestamp: str) -> None:
    """Persist the last-reported timestamp for a server."""
    cache.set(_heartbeat_key(server_id), timestamp, timeout=BABY_SERVER_STATUS_TTL_SECONDS)


def get_baby_server_heartbeat(server_id: str) -> str | None:
    """Retrieve the cached heartbeat timestamp for a server."""
    cached = cache.get(_heartbeat_key(server_id))
    return cached if isinstance(cached, str) else None


def get_many_baby_server_heartbeats(server_ids: Iterable[str]) -> dict[str, str]:
    """Fetch heartbeat timestamps for multiple servers in a single call."""
    key_map = {_heartbeat_key(server_id): server_id for server_id in server_ids}
    raw = cache.get_many(key_map.keys())
    return {
        key_map[cache_key]: value for cache_key, value in raw.items() if isinstance(value, str) and cache_key in key_map
    }
