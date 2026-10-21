"""EtkinlikCepte – Keşif & Öneri servisi: veritabanı sorguları (SQLAlchemy 2.0 Core + ham SQL, PostGIS).

VARSAYILAN ŞEMA (kendi tablolarınıza göre uyarlayın):
    venues(id, name, category, address, location geography(Point,4326))
    clubs(id, name)
    events(id, title, category, status, starts_at, ends_at, price numeric, popularity int,
           created_at, venue_id, club_id, location geography(Point,4326))   -- location, venue'dan kopyalanmış (denormalize)
    club_follows(user_id, club_id)
    user_category_prefs(user_id, category, affinity float 0..1)

PERFORMANS (300 ms hedefi) İÇİN GEREKLİ İNDEKSLER – bir kez migration'da çalıştırın:
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from sqlalchemy import select, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncConnection

from app.schemas.discovery import RankingWeights, ranking_weights

MIGRATION_SQL = r"""
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Türkçe duyarsız karşılaştırma: İ I ı Ç ç Ş ş Ğ ğ Ü ü Ö ö  ->  ASCII + küçük harf
CREATE OR REPLACE FUNCTION tr_fold(t text) RETURNS text
LANGUAGE sql IMMUTABLE PARALLEL SAFE STRICT AS
$$ SELECT lower(translate(t, 'İIıÇçŞşĞğÜüÖö', 'iiiccssgguuoo')) $$;

-- Mekânsal indeksler (kaba filtrenin kalbi)
CREATE INDEX IF NOT EXISTS ix_events_location_gist ON events USING GIST (location);
CREATE INDEX IF NOT EXISTS ix_venues_location_gist ON venues USING GIST (location);

-- Yardımcı indeksler
CREATE INDEX IF NOT EXISTS ix_events_starts_at ON events (starts_at) WHERE status = 'published';
CREATE INDEX IF NOT EXISTS ix_events_category_fold ON events (tr_fold(category));
CREATE INDEX IF NOT EXISTS ix_venues_category_fold ON venues (tr_fold(category));
CREATE INDEX IF NOT EXISTS ix_events_title_fold_trgm ON events USING GIN (tr_fold(title) gin_trgm_ops);
CREATE INDEX IF NOT EXISTS ix_club_follows_user ON club_follows (user_id);

ANALYZE events; ANALYZE venues;
"""

MAX_CANDIDATES = 200          # kaba filtre üst sınırı (LIMIT 200)
STATEMENT_TIMEOUT_MS = 300    # aday sorgusu için sert zaman aşımı
MAX_VENUES = 500

# Kullanıcının konumu -> geography noktası (GIST indeksinin kullanılabilmesi için sabit ifade)
_USER_POINT = "ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography"

# ---------------------------------------------------------------------------
# Türkçe duyarsız arama yardımcıları (SQL'deki tr_fold ile birebir aynı eşleme)
# ---------------------------------------------------------------------------
_TR_MAP = str.maketrans("İIıÇçŞşĞğÜüÖö", "iiiccssgguuoo")
_LIKE_ESCAPE = re.compile(r"([\\%_])")


def tr_fold(value: str) -> str:
    """'İSTANBUL', 'istanbul', 'Istanbul' hepsi -> 'istanbul'; 'Şişli' -> 'sisli'."""
    return value.translate(_TR_MAP).lower().strip()


def _like_pattern(value: str) -> str:
    escaped = _LIKE_ESCAPE.sub(r"\\\1", tr_fold(value))  # % _ \ karakterlerini kaçır
    return "%" + escaped + "%"


class CandidateQueryTimeout(Exception):
    """Aday sorgusu STATEMENT_TIMEOUT_MS içinde tamamlanamadı."""


async def _execute(conn: AsyncConnection, sql: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        await conn.execute(text(f"SET LOCAL statement_timeout = {int(STATEMENT_TIMEOUT_MS)}"))
        result = await conn.execute(text(sql), params)
        return [dict(row) for row in result.mappings()]
    except DBAPIError as exc:
        if "statement timeout" in str(exc.orig).lower():
            raise CandidateQueryTimeout from exc
        raise


# ---------------------------------------------------------------------------
# /discover/venues – bbox sorgusu
# ---------------------------------------------------------------------------
async def search_venues_in_bbox(
    conn: AsyncConnection,
    *,
    min_lng: float,
    min_lat: float,
    max_lng: float,
    max_lat: float,
    category: str | None = None,
    limit: int = MAX_VENUES,
) -> list[dict[str, Any]]:
    sql = """
        SELECT v.id, v.name, v.category, v.address,
               ST_Y(v.location::geometry) AS lat,
               ST_X(v.location::geometry) AS lng
        FROM venues v
        WHERE v.location && ST_MakeEnvelope(:min_lng, :min_lat, :max_lng, :max_lat, 4326)::geography
    """
    params: dict[str, Any] = {
        "min_lng": min_lng,
        "min_lat": min_lat,
        "max_lng": max_lng,
        "max_lat": max_lat,
        "limit": min(limit, MAX_VENUES),
    }
    if category:
        sql += " AND tr_fold(v.category) = :category"
        params["category"] = tr_fold(category)
    sql += " ORDER BY v.id LIMIT :limit"
    return await _execute(conn, sql, params)


# ---------------------------------------------------------------------------
# KABA FİLTRE: ST_DWithin + GIST indeksi + LIMIT 200  (events & recommendations ortak)
# ---------------------------------------------------------------------------
async def fetch_candidates(
    conn: AsyncConnection,
    *,
    lat: float,
    lng: float,
    radius_m: float,
    starts_from: datetime,
    starts_to: datetime,
    category: str | None = None,
    q: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    limit: int = MAX_CANDIDATES,
) -> list[dict[str, Any]]:
    """Kullanıcının (lat, lng) noktasına `radius_m` metre içindeki en yakın en fazla 200 etkinliği getirir.

    - `ST_DWithin(geography, geography, metre)` -> GIST indeksini (ix_events_location_gist) kullanır.
    - `ORDER BY location <-> nokta` -> GIST KNN taraması; tüm kümeyi sıralamaya gerek kalmaz.
    - `LIMIT :limit` her zaman en fazla MAX_CANDIDATES (200) ile sınırlanır.
    - `SET LOCAL statement_timeout = 300` -> 300 ms'yi aşan sorgu iptal edilir (CandidateQueryTimeout).
    Doğrulama:  EXPLAIN (ANALYZE, BUFFERS)  çıktısında 'Index Scan using ix_events_location_gist' görmelisiniz.
    """
    sql = f"""
        SELECT e.id, e.title, e.category, e.starts_at, e.ends_at, e.price, e.popularity,
               e.created_at, e.venue_id, v.name AS venue_name, e.club_id, c.name AS club_name,
               ST_Y(e.location::geometry) AS lat,
               ST_X(e.location::geometry) AS lng,
               ST_Distance(e.location, {_USER_POINT}) AS distance_m
        FROM events e
        JOIN venues v ON v.id = e.venue_id
        LEFT JOIN clubs c ON c.id = e.club_id
        WHERE e.status = 'published'
          AND ST_DWithin(e.location, {_USER_POINT}, :radius_m)
          AND e.starts_at >= :starts_from
          AND e.starts_at <  :starts_to
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
        sql += " AND tr_fold(e.category) = :category"
        params["category"] = tr_fold(category)
    if q:
        sql += " AND tr_fold(e.title) LIKE :q_pattern ESCAPE '\\'"
        params["q_pattern"] = _like_pattern(q)
    if min_price is not None:
        sql += " AND e.price >= :min_price"
        params["min_price"] = min_price
    if max_price is not None:
        sql += " AND e.price <= :max_price"
        params["max_price"] = max_price

    sql += f" ORDER BY e.location <-> {_USER_POINT} LIMIT :limit"
    return await _execute(conn, sql, params)


# ---------------------------------------------------------------------------
# Öneri sinyalleri ve ağırlıklar
# ---------------------------------------------------------------------------
async def fetch_active_weights(conn: AsyncConnection) -> RankingWeights:
    """Aktif `ranking_weights` satırını döndürür; yoksa varsayılan ağırlıklar kullanılır."""
    stmt = select(
        ranking_weights.c.w1_distance,
        ranking_weights.c.w2_category,
        ranking_weights.c.w3_freshness,
        ranking_weights.c.w4_popularity,
        ranking_weights.c.w5_price,
        ranking_weights.c.w6_club_follow,
    ).where(ranking_weights.c.is_active.is_(True)).limit(1)
    row = (await conn.execute(stmt)).mappings().first()
    return RankingWeights(**row) if row else RankingWeights()


async def fetch_user_signals(
    conn: AsyncConnection, user_id: int
) -> tuple[dict[str, float], set[int]]:
    """(kategori_afinitesi {tr_fold(kategori): 0..1}, takip_edilen_kulüp_idleri)."""
    prefs = await conn.execute(
        text("SELECT category, affinity FROM user_category_prefs WHERE user_id = :uid"),
        {"uid": user_id},
    )
    affinity = {tr_fold(r.category): float(r.affinity) for r in prefs}

    follows = await conn.execute(
        text("SELECT club_id FROM club_follows WHERE user_id = :uid"),
        {"uid": user_id},
    )
    followed = {int(r.club_id) for r in follows}
    return affinity, followed
