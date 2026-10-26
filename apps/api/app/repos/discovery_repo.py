"""Discovery SQL over the actual §7 schema (PostGIS + SQLAlchemy async).

All queries are parameterized; Turkish-insensitive comparison is done with
inline ``translate`` expressions so no custom SQL function is required.
"""

from __future__ import annotations

import datetime
import uuid
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

MAX_CANDIDATES = 200
MAX_VENUES = 500
STATEMENT_TIMEOUT_MS = 300

def tr_fold(value: str) -> str:
    """Fold Turkish characters to ASCII lowercase for Python-side matching."""
    return value.translate(str.maketrans("İIıÇçŞşĞğÜüÖö", "iiiccssgguuoo")).lower().strip()


def _like(value: str) -> str:
    """Build a parameter value for a folded LIKE search."""
    escaped = value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{tr_fold(escaped)}%"


async def _execute(session: AsyncSession, sql: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    """Run a statement with a 300 ms timeout, translating timeouts to a domain signal."""
    try:
        await session.execute(text(f"SET LOCAL statement_timeout = {STATEMENT_TIMEOUT_MS}"))
        result = await session.execute(text(sql), params)
        return [dict(row) for row in result.mappings()]
    except DBAPIError as exc:
        if "statement timeout" in str(exc.orig).lower():
            raise CandidateQueryTimeout from exc
        raise


class CandidateQueryTimeout(Exception):
    """The candidate query exceeded the 300 ms budget."""


async def search_venues_in_bbox(
    session: AsyncSession,
    *,
    min_lng: float,
    min_lat: float,
    max_lng: float,
    max_lat: float,
    category: str | None = None,
    limit: int = MAX_VENUES,
) -> list[dict[str, Any]]:
    """Find venues whose point lies inside a WGS84 bounding box."""
    sql = """
        SELECT v.id, v.name, v.category, v.address, v.city,
               ST_Y(v.geom::geometry) AS lat,
               ST_X(v.geom::geometry) AS lng
        FROM venues v
        WHERE v.geom IS NOT NULL
          AND v.geom && ST_MakeEnvelope(:min_lng, :min_lat, :max_lng, :max_lat, 4326)
    """
    params: dict[str, Any] = {
        "min_lng": min_lng,
        "min_lat": min_lat,
        "max_lng": max_lng,
        "max_lat": max_lat,
        "limit": min(limit, MAX_VENUES),
    }
    if category:
        sql += " AND lower(v.category) = lower(:category)"
        params["category"] = category
    sql += " ORDER BY v.name LIMIT :limit"
    return await _execute(session, sql, params)


async def fetch_candidates(
    session: AsyncSession,
    *,
    lat: float,
    lng: float,
    radius_m: float,
    starts_from: datetime.datetime,
    starts_to: datetime.datetime,
    category: str | None = None,
    q: str | None = None,
    price_min_minor: int | None = None,
    price_max_minor: int | None = None,
    limit: int = MAX_CANDIDATES,
) -> list[dict[str, Any]]:
    """Return nearby published events with venue, price, popularity and distance."""
    point = "ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography"
    sql = f"""
        SELECT e.id, e.title, e.category, e.starts_at, e.ends_at,
               e.venue_id, v.name AS venue_name, e.club_id, c.name AS club_name,
               ST_Y(v.geom::geometry) AS lat,
               ST_X(v.geom::geometry) AS lng,
               ST_Distance(v.geom::geography, {point}) AS distance_m,
               (SELECT MIN(t.price_minor) FROM event_tickets t WHERE t.event_id = e.id) AS price_minor,
               (SELECT t.currency FROM event_tickets t WHERE t.event_id = e.id
                ORDER BY t.price_minor NULLS LAST LIMIT 1) AS currency,
               (SELECT COUNT(*) FROM registrations r
                WHERE r.event_id = e.id AND r.status IN ('paid', 'free_granted')) AS popularity
        FROM events e
        JOIN venues v ON v.id = e.venue_id
        LEFT JOIN clubs c ON c.id = e.club_id
        WHERE e.status = 'published'
          AND v.geom IS NOT NULL
          AND ST_DWithin(v.geom::geography, {point}, :radius_m)
          AND e.starts_at >= :starts_from
          AND e.starts_at < :starts_to
    """
    params: dict[str, Any] = {
        "lat": lat,
        "lng": lng,
        "radius_m": radius_m,
        "starts_from": starts_from,
        "starts_to": starts_to,
        "limit": min(limit, MAX_CANDIDATES),
    }
    if category:
        sql += " AND lower(e.category) = lower(:category)"
        params["category"] = category
    if q:
        sql += " AND lower(e.title) LIKE :q_pattern ESCAPE '\\'"
        params["q_pattern"] = _like(q)
    if price_min_minor is not None:
        sql += " AND COALESCE((SELECT MIN(t.price_minor) FROM event_tickets t WHERE t.event_id = e.id), 0) >= :price_min"
        params["price_min"] = price_min_minor
    if price_max_minor is not None:
        sql += " AND COALESCE((SELECT MIN(t.price_minor) FROM event_tickets t WHERE t.event_id = e.id), 0) <= :price_max"
        params["price_max"] = price_max_minor

    sql += " ORDER BY distance_m, e.starts_at LIMIT :limit"
    return await _execute(session, sql, params)


async def fetch_weights(session: AsyncSession) -> dict[str, float]:
    """Read named ranking weights from ``ranking_weights`` (name/value rows)."""
    rows = await _execute(session, "SELECT name, value FROM ranking_weights", {})
    return {str(row["name"]): float(row["value"]) for row in rows}


async def fetch_user_signals(
    session: AsyncSession, user_id: uuid.UUID | None
) -> tuple[set[str], set[uuid.UUID]]:
    """Return folded interest categories and followed club ids for a user."""
    if user_id is None:
        return set(), set()
    user = await session.execute(
        text("SELECT interests FROM users WHERE id = :uid"), {"uid": user_id}
    )
    row = user.mappings().first()
    interests = {tr_fold(str(item)) for item in (row["interests"] if row else []) if item}
    follows = await session.execute(
        text("SELECT club_id FROM club_followers WHERE user_id = :uid"), {"uid": user_id}
    )
    return interests, {row["club_id"] for row in follows.mappings()}
