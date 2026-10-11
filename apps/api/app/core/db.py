"""Async psycopg connection pool, opened lazily (H1.2 skeleton).

The pool is NOT opened at import or startup: H1.3 owns the schema and H1.4
owns the database container. Routers call get_pool() once they need it.
"""

from __future__ import annotations

from psycopg_pool import AsyncConnectionPool

from app.core.config import settings

_pool: AsyncConnectionPool | None = None


def get_pool() -> AsyncConnectionPool:
    """Return the process-wide pool, creating it closed on first call.

    Returns:
        The shared AsyncConnectionPool (still closed; open it explicitly).
    """
    global _pool
    if _pool is None:
        _pool = AsyncConnectionPool(settings.database_url, open=False)
    return _pool


async def close_pool() -> None:
    """Close the process-wide pool if one was created."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
