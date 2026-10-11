"""Lazy Valkey client for cache, pub/sub fan-out and presence (H1.2 skeleton).

Valkey speaks the Redis protocol, so the client uses hiredis parsing
(development.md §3.2, §11: Uvicorn + uvloop + orjson + hiredis).
"""

from __future__ import annotations

from valkey.asyncio import Valkey

from app.core.config import settings

_client: Valkey | None = None


def get_valkey() -> Valkey:
    """Return the process-wide Valkey client, creating it on first call.

    Returns:
        The shared async Valkey client.
    """
    global _client
    if _client is None:
        _client = Valkey.from_url(settings.valkey_url)
    return _client


async def close_valkey() -> None:
    """Close the process-wide Valkey client if one was created."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
