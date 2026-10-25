"""SQLAlchemy async engine and session dependency (H2.1).

The engine is lazy: importing the app does not connect. Tests and endpoints
use ``get_session``; Alembic keeps its own synchronous URL.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


def _async_url(url: str) -> str:
    """Return a SQLAlchemy async URL for psycopg."""
    if url.startswith("postgresql+psycopg://"):
        return url
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url.removeprefix("postgresql://")
    return url


engine = create_async_engine(_async_url(settings.database_url), pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Yield one async session per request."""
    async with SessionLocal() as session:
        yield session


async def dispose_engine() -> None:
    """Dispose the process-wide engine on shutdown."""
    await engine.dispose()
