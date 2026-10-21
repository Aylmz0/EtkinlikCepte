"""EtkinlikCepte – Keşif & Öneri servisi: FastAPI endpoint'leri.

Uçlar:
    GET /discover/venues?bbox=minLng,minLat,maxLng,maxLat&category=
    GET /discover/events?lat=&lng=&radius=&category=&when=&price=&q=
    GET /discover/recommendations?lat=&lng=&radius=&limit=

Projenize göre uyarlayın:
    app.core.db.get_conn          -> AsyncConnection döndüren bağımlılık
    app.core.auth.get_current_user_id -> oturumdaki kullanıcının id'sini döndüren bağımlılık
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Literal
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.auth import get_current_user_id
from app.core.db import get_conn
from app.repos import discovery_repo as repo
from app.schemas.discovery import (
    EventListResponse,
    EventOut,
    RankingWeights,
    RecommendationOut,
    RecommendationsResponse,
    ScoreFactor,
    VenueListResponse,
    VenueOut,
)

router = APIRouter(prefix="/discover", tags=["discover"])

TZ = ZoneInfo("Europe/Istanbul")

WhenFilter = Literal["today", "tomorrow", "weekend", "week"]
PriceFilter = Literal["free", "paid", "low", "mid", "high"]

# low <= 100 TL, mid 100–300 TL, high > 300 TL
_PRICE_RANGES: dict[str, tuple[float | None, float | None]] = {
    "free": (None, 0.0),
    "paid": (0.01, None),
    "low": (0.0, 100.0),
    "mid": (100.0, 300.0),
    "high": (300.0, None),
}


# ===========================================================================
# Yardımcılar
# ===========================================================================
@dataclass(frozen=True)
class BBox:
    min_lng: float
    min_lat: float
    max_lng: float
    max_lat: float


def parse_bbox(
    bbox: str = Query(..., description="minLng,minLat,maxLng,maxLat (WGS84)", examples=["38.6,39.5,39.0,39.9"]),
) -> BBox:
    try:
        min_lng, min_lat, max_lng, max_lat = (float(p) for p in bbox.split(","))
    except ValueError:
        raise HTTPException(422, "bbox 'minLng,minLat,maxLng,maxLat' biçiminde 4 sayı olmalıdır.")
    if not (-180 <= min_lng < max_lng <= 180 and -90 <= min_lat < max_lat <= 90):
        raise HTTPException(422, "bbox değerleri geçersiz (min < max ve geçerli koordinat aralığında olmalı).")
    if (max_lng - min_lng) > 2.0 or (max_lat - min_lat) > 2.0:
        raise HTTPException(422, "bbox çok geniş; en fazla 2° x 2° alan sorgulanabilir.")
    return BBox(min_lng, min_lat, max_lng, max_lat)


def resolve_when(when: WhenFilter | None, now: datetime) -> tuple[datetime, datetime]:
    """`when` filtresini [başlangıç, bitiş) zaman aralığına çevirir (Europe/Istanbul)."""
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if when == "today":
        return now, start_of_day + timedelta(days=1)
    if when == "tomorrow":
        return start_of_day + timedelta(days=1), start_of_day + timedelta(days=2)
    if when == "weekend":
        wd = now.weekday()  # Pzt=0 ... Cmt=5, Paz=6
        if wd >= 5:
            return now, start_of_day + timedelta(days=7 - wd)
        return start_of_day + timedelta(days=5 - wd), start_of_day + timedelta(days=7 - wd)
    if when == "week":
        return now, now + timedelta(days=7)
    return now, now + timedelta(days=30)  # varsayılan: önümüzdeki 30 gün


def _to_event_out(row: dict[str, Any]) -> EventOut:
    price = float(row["price"] or 0)
    return EventOut(
        **{k: row[k] for k in (
            "id", "title", "category", "starts_at", "ends_at", "popularity",
            "venue_id", "venue_name", "club_id", "club_name", "lat", "lng",
        )},
        price=price,
        is_free=price == 0,
        distance_m=round(float(row["distance_m"]), 1) if row.get("distance_m") is not None else None,
    )


# ===========================================================================
# 1) GET /discover/venues
# ===========================================================================
@router.get("/venues", response_model=VenueListResponse)
async def discover_venues(
    bbox: BBox = Depends(parse_bbox),
    category: str | None = Query(None, description="Türkçe duyarsız (Müzik = müzik = MÜZİK)"),
    conn: AsyncConnection = Depends(get_conn),
) -> VenueListResponse:
    try:
        rows = await repo.search_venues_in_bbox(
            conn,
            min_lng=bbox.min_lng, min_lat=bbox.min_lat,
            max_lng=bbox.max_lng, max_lat=bbox.max_lat,
            category=category,
        )
    except repo.CandidateQueryTimeout:
        raise HTTPException(503, "Sorgu zaman aşımına uğradı, lütfen alanı daraltın.", headers={"Retry-After": "2"})
    items = [VenueOut(**r) for r in rows]
    return VenueListResponse(count=len(items), items=items)


# ===========================================================================
# 2) GET /discover/events
# ===========================================================================
@router.get("/events", response_model=EventListResponse)
async def discover_events(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius: float = Query(5000, gt=0, le=50_000, description="Yarıçap (metre)"),
    category: str | None = Query(None, description="Türkçe duyarsız kategori filtresi"),
    when: WhenFilter | None = Query(None, description="today | tomorrow | weekend | week"),
    price: PriceFilter | None = Query(None, description="free | paid | low | mid | high"),
    q: str | None = Query(None, min_length=2, max_length=80, description="Başlıkta Türkçe duyarsız arama"),
    conn: AsyncConnection = Depends(get_conn),
) -> EventListResponse:
    starts_from, starts_to = resolve_when(when, datetime.now(TZ))
    min_price, max_price = _PRICE_RANGES[price] if price else (None, None)
    try:
        rows = await repo.fetch_candidates(
            conn,
            lat=lat, lng=lng, radius_m=radius,
            starts_from=starts_from, starts_to=starts_to,
            category=category, q=q,
            min_price=min_price, max_price=max_price,
        )
    except repo.CandidateQueryTimeout:
        raise HTTPException(503, "Sorgu zaman aşımına uğradı, lütfen yarıçapı daraltın.", headers={"Retry-After": "2"})
    items = [_to_event_out(r) for r in rows]
    return EventListResponse(count=len(items), items=items)


# ===========================================================================
# 3) GET /discover/recommendations  – puanlama (scoring)
# ===========================================================================
# Normalizasyon sabitleri
FRESHNESS_HORIZON_DAYS = 30.0   # etkinlik ilanı 30 günde "bayatlar" (doğrusal)
POPULARITY_CAP = 5_000          # bu katılımcı sayısında popülerlik skoru = 1.0 (logaritmik)
PRICE_CAP_TRY = 1_000.0         # 1000 TL ve üstü fiyat skoru = 0 (doğrusal)

_WEIGHT_TTL_SECONDS = 60
_weights_cache: tuple[float, RankingWeights] | None = None


def linear_decay(value: float, horizon: float) -> float:
    """1.0 (value=0) -> 0.0 (value>=horizon) arası doğrusal düşüş."""
    if horizon <= 0:
        return 0.0
    return max(0.0, min(1.0, 1.0 - value / horizon))


def log_popularity(count: float) -> float:
    """Logaritmik popülerlik: ilk katılımcılar çok, sonrakiler giderek az puan getirir. 0..1"""
    return min(1.0, math.log1p(max(count, 0.0)) / math.log1p(POPULARITY_CAP))


async def _get_weights(conn: AsyncConnection) -> RankingWeights:
    """Aktif ağırlıkları 60 sn bellekte tutar (her istekte DB'ye gitmemek için)."""
    global _weights_cache
    now = time.monotonic()
    if _weights_cache and now - _weights_cache[0] < _WEIGHT_TTL_SECONDS:
        return _weights_cache[1]
    weights = (await repo.fetch_active_weights(conn)).normalized()
    _weights_cache = (now, weights)
    return weights


def _fmt_distance(meters: float) -> str:
    if meters < 1000:
        return f"{round(meters / 10) * 10:.0f} m"
    return f"{meters / 1000:.1f}".replace(".", ",") + " km"


def _join_tr(parts: list[str]) -> str:
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " ve " + parts[-1]


def score_candidate(
    row: dict[str, Any],
    *,
    radius_m: float,
    weights: RankingWeights,
    affinity: dict[str, float],
    followed_clubs: set[int],
    now: datetime,
) -> tuple[float, list[ScoreFactor]]:
    price = float(row["price"] or 0)
    distance_m = float(row["distance_m"] or 0)
    age_days = max(0.0, (now - row["created_at"]).total_seconds() / 86_400)
    popularity = int(row["popularity"] or 0)
    cat_affinity = max(0.0, min(1.0, affinity.get(repo.tr_fold(row["category"]), 0.0)))
    is_followed = row["club_id"] is not None and row["club_id"] in followed_clubs

    specs: list[tuple[str, str, float, float, float]] = [
        # key, label, raw, normalized (0..1), weight
        ("distance", "Mesafe", distance_m, linear_decay(distance_m, radius_m), weights.w1_distance),
        ("category", "Kategori uyumu", cat_affinity, cat_affinity, weights.w2_category),
        ("freshness", "Tazelik", age_days, linear_decay(age_days, FRESHNESS_HORIZON_DAYS), weights.w3_freshness),
        ("popularity", "Popülerlik", float(popularity), log_popularity(popularity), weights.w4_popularity),
        ("price", "Fiyat", price, linear_decay(price, PRICE_CAP_TRY), weights.w5_price),
        ("club_follow", "Kulüp takibi", 1.0 if is_followed else 0.0, 1.0 if is_followed else 0.0, weights.w6_club_follow),
    ]
    factors = [
        ScoreFactor(
            key=key, label=label, raw=round(raw, 2),
            normalized=round(norm, 4), weight=round(w, 4),
            contribution=round(100.0 * w * norm, 2),
        )
        for key, label, raw, norm, w in specs
    ]
    total = round(sum(f.contribution for f in factors), 1)
    return min(total, 100.0), factors


def build_reason(row: dict[str, Any], factors: list[ScoreFactor], now: datetime) -> str:
    """En çok katkı yapan (en fazla 3) faktörden 'Bunu önerdik çünkü ...' cümlesini kurar."""
    price = float(row["price"] or 0)
    age_days = max(0.0, (now - row["created_at"]).total_seconds() / 86_400)

    def phrase(f: ScoreFactor) -> str | None:
        if f.key == "club_follow" and f.normalized > 0:
            return f"takip ettiğiniz {row['club_name'] or 'kulüp'} tarafından düzenleniyor"
        if f.key == "category" and f.normalized >= 0.3:
            return f"ilgi duyduğunuz {row['category']} kategorisinde"
        if f.key == "distance" and f.normalized >= 0.4:
            return f"size yalnızca {_fmt_distance(float(row['distance_m']))} uzaklıkta"
        if f.key == "popularity" and f.normalized >= 0.4:
            return f"{int(row['popularity'])} kişi tarafından ilgi görüyor"
        if f.key == "freshness" and f.normalized >= 0.5:
            return "bugün eklendi" if age_days < 1 else f"{int(age_days)} gün önce eklendi"
        if f.key == "price" and f.normalized >= 0.7:
            return "ücretsiz" if price == 0 else f"{price:.0f} ₺ ile bütçenize uygun"
        return None

    parts = []
    for f in sorted(factors, key=lambda x: x.contribution, reverse=True):
        text_part = phrase(f)
        if text_part:
            parts.append(text_part)
        if len(parts) == 3:
            break
    if not parts:
        return "Bunu önerdik çünkü size yakın ve yaklaşan etkinliklerden biri."
    return f"Bunu önerdik çünkü {_join_tr(parts)}."


@router.get("/recommendations", response_model=RecommendationsResponse)
async def discover_recommendations(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius: float = Query(10_000, gt=0, le=50_000, description="Yarıçap (metre)"),
    limit: int = Query(20, ge=1, le=50),
    user_id: int = Depends(get_current_user_id),
    conn: AsyncConnection = Depends(get_conn),
) -> RecommendationsResponse:
    now = datetime.now(TZ)
    starts_from, starts_to = resolve_when(None, now)

    # 1) Kaba filtre: ST_DWithin + GIST, en fazla 200 aday (<300 ms)
    try:
        candidates = await repo.fetch_candidates(
            conn, lat=lat, lng=lng, radius_m=radius,
            starts_from=starts_from, starts_to=starts_to,
            limit=repo.MAX_CANDIDATES,
        )
    except repo.CandidateQueryTimeout:
        raise HTTPException(503, "Öneri sorgusu zaman aşımına uğradı.", headers={"Retry-After": "2"})

    # 2) Kullanıcı sinyalleri + ağırlıklar (küçük sorgular / önbellek)
    weights = await _get_weights(conn)
    affinity, followed_clubs = await repo.fetch_user_signals(conn, user_id)

    # 3) Bellekte puanlama (200 satır için mikrosaniyeler)
    scored: list[tuple[float, dict[str, Any], list[ScoreFactor]]] = []
    for row in candidates:
        total, factors = score_candidate(
            row, radius_m=radius, weights=weights,
            affinity=affinity, followed_clubs=followed_clubs, now=now,
        )
        scored.append((total, row, factors))

    # puan ↓, mesafe ↑, başlangıç zamanı ↑
    scored.sort(key=lambda t: (-t[0], float(t[1]["distance_m"] or 0), t[1]["starts_at"]))

    items = [
        RecommendationOut(
            event=_to_event_out(row),
            score=total,
            reason=build_reason(row, factors, now),
            factors=factors,
        )
        for total, row, factors in scored[:limit]
    ]
    return RecommendationsResponse(
        count=len(items),
        candidate_count=len(candidates),
        weights=weights,
        generated_at=now,
        items=items,
    )
