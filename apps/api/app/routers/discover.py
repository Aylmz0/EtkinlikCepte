"""Discovery endpoints: venues, events, recommendations (§8 Keşif, H2.6/H2.16/H2.17)."""

from __future__ import annotations

import datetime
import math
from dataclasses import dataclass
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_optional_user
from app.core.db import get_session
from app.core.errors import ApiError
from app.repos import discovery_repo as repo
from app.repos.auth import User
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

WhenFilter = Literal["today", "tomorrow", "weekend", "week"]
PriceFilter = Literal["free", "paid", "low", "mid", "high"]

DEFAULT_RADIUS_M = 10_000
DEFAULT_HORIZON_DAYS = 30
FRESHNESS_HORIZON_DAYS = 30.0
POPULARITY_CAP = 5_000
PRICE_CAP_MINOR = 100_000  # 1000 TRY

PRICE_RANGES: dict[str, tuple[int | None, int | None]] = {
    "free": (0, 0),
    "paid": (1, None),
    "low": (0, 10_000),
    "mid": (10_000, 30_000),
    "high": (30_000, None),
}

WEIGHT_KEYS = (
    "w1_distance",
    "w2_category",
    "w3_freshness",
    "w4_popularity",
    "w5_price",
    "w6_club_follow",
)

SessionDep = Annotated[AsyncSession, Depends(get_session)]
OptionalUser = Annotated[User | None, Depends(get_optional_user)]


@dataclass(frozen=True)
class BBox:
    """WGS84 bounding box for the map viewport."""

    min_lng: float
    min_lat: float
    max_lng: float
    max_lat: float


def parse_bbox(
    bbox: str = Query(..., description="minLng,minLat,maxLng,maxLat (WGS84)"),
) -> BBox:
    """Parse and validate a map bounding box."""
    try:
        min_lng, min_lat, max_lng, max_lat = (float(part) for part in bbox.split(","))
    except ValueError as exc:
        raise ApiError(422, "Invalid bbox", "bbox must be minLng,minLat,maxLng,maxLat.") from exc
    if not (-180 <= min_lng < max_lng <= 180 and -90 <= min_lat < max_lat <= 90):
        raise ApiError(422, "Invalid bbox", "Coordinates must be ordered and in range.")
    if (max_lng - min_lng) > 2.0 or (max_lat - min_lat) > 2.0:
        raise ApiError(422, "bbox too large", "At most 2° x 2° can be queried.")
    return BBox(min_lng, min_lat, max_lng, max_lat)


def resolve_when(
    when: WhenFilter | None, now: datetime.datetime
) -> tuple[datetime.datetime, datetime.datetime]:
    """Turn a date filter into a [start, end) UTC window."""
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if when == "today":
        return now, day_start + datetime.timedelta(days=1)
    if when == "tomorrow":
        return day_start + datetime.timedelta(days=1), day_start + datetime.timedelta(days=2)
    if when == "weekend":
        weekday = now.weekday()  # Monday=0, Saturday=5
        if weekday >= 5:
            return now, day_start + datetime.timedelta(days=7 - weekday)
        saturday = day_start + datetime.timedelta(days=5 - weekday)
        return saturday, saturday + datetime.timedelta(days=2)
    if when == "week":
        return now, now + datetime.timedelta(days=7)
    return now, now + datetime.timedelta(days=DEFAULT_HORIZON_DAYS)


def _event_out(row: dict[str, object]) -> EventOut:
    price = row.get("price_minor")
    return EventOut(
        id=row["id"],  # type: ignore[arg-type]
        title=str(row["title"]),
        category=row.get("category"),  # type: ignore[arg-type]
        starts_at=row["starts_at"],  # type: ignore[arg-type]
        ends_at=row.get("ends_at"),  # type: ignore[arg-type]
        venue_id=row.get("venue_id"),  # type: ignore[arg-type]
        venue_name=row.get("venue_name"),  # type: ignore[arg-type]
        club_id=row.get("club_id"),  # type: ignore[arg-type]
        club_name=row.get("club_name"),  # type: ignore[arg-type]
        lat=float(row["lat"]),  # type: ignore[arg-type]
        lng=float(row["lng"]),  # type: ignore[arg-type]
        distance_m=round(float(row["distance_m"]), 1)
        if row.get("distance_m") is not None
        else None,
        price_minor=int(price) if price is not None else None,
        currency=str(row.get("currency") or "TRY"),
    )


def _weights_from_rows(rows: dict[str, float]) -> RankingWeights:
    values = {key: rows[key] for key in WEIGHT_KEYS if key in rows}
    return RankingWeights(**values).normalized()


@router.get("/venues", response_model=VenueListResponse)
async def discover_venues(
    bbox: Annotated[BBox, Depends(parse_bbox)],
    session: SessionDep,
    category: str | None = Query(default=None),
) -> VenueListResponse:
    """Return venues inside the map viewport, optionally filtered by category."""
    try:
        rows = await repo.search_venues_in_bbox(
            session,
            min_lng=bbox.min_lng,
            min_lat=bbox.min_lat,
            max_lng=bbox.max_lng,
            max_lat=bbox.max_lat,
            category=category,
        )
    except repo.CandidateQueryTimeout as exc:
        raise ApiError(503, "Query timeout", "Narrow the bounding box.") from exc
    return VenueListResponse(count=len(rows), items=[VenueOut(**row) for row in rows])


@router.get("/events", response_model=EventListResponse)
async def discover_events(
    session: SessionDep,
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius: int = Query(DEFAULT_RADIUS_M, gt=0, le=50_000),
    category: str | None = None,
    when: WhenFilter | None = None,
    price: PriceFilter | None = None,
    q: str | None = Query(default=None, min_length=2, max_length=80),
    limit: int = Query(default=50, ge=1, le=200),
) -> EventListResponse:
    """Return published events around a point with date, category and price filters."""
    starts_from, starts_to = resolve_when(when, datetime.datetime.now(datetime.UTC))
    price_min, price_max = PRICE_RANGES[price] if price else (None, None)
    try:
        rows = await repo.fetch_candidates(
            session,
            lat=lat,
            lng=lng,
            radius_m=radius,
            starts_from=starts_from,
            starts_to=starts_to,
            category=category,
            q=q,
            price_min_minor=price_min,
            price_max_minor=price_max,
            limit=limit,
        )
    except repo.CandidateQueryTimeout as exc:
        raise ApiError(503, "Query timeout", "Narrow the radius.") from exc
    return EventListResponse(count=len(rows), items=[_event_out(row) for row in rows])


def _linear(value: float, horizon: float) -> float:
    if horizon <= 0:
        return 0.0
    return max(0.0, min(1.0, 1.0 - value / horizon))


def _popularity(count: float) -> float:
    return min(1.0, math.log1p(max(count, 0.0)) / math.log1p(POPULARITY_CAP))


def _distance_text(meters: float) -> str:
    if meters < 1000:
        return f"{round(meters / 10) * 10:.0f} m"
    return f"{meters / 1000:.1f} km"


def score_candidate(
    row: dict[str, object],
    *,
    radius_m: float,
    weights: RankingWeights,
    interests: set[str],
    followed_clubs: set[object],
    now: datetime.datetime,
) -> tuple[float, list[ScoreFactor]]:
    """Score one candidate with the transparent six-factor formula."""
    price = int(row.get("price_minor") or 0)
    distance = float(row.get("distance_m") or 0)
    created = row.get("created_at")
    age_days = (
        max(0.0, (now - created).total_seconds() / 86_400)
        if isinstance(created, datetime.datetime)
        else 0.0
    )
    category = repo.tr_fold(str(row.get("category") or ""))
    affinity = 1.0 if category and category in interests else 0.0
    followed = 1.0 if row.get("club_id") in followed_clubs else 0.0
    popularity = float(row.get("popularity") or 0)

    specs = [
        ("distance", "Mesafe", distance, _linear(distance, radius_m), weights.w1_distance),
        ("category", "Kategori uyumu", affinity, affinity, weights.w2_category),
        (
            "freshness",
            "Tazelik",
            age_days,
            _linear(age_days, FRESHNESS_HORIZON_DAYS),
            weights.w3_freshness,
        ),
        ("popularity", "Popülerlik", popularity, _popularity(popularity), weights.w4_popularity),
        ("price", "Fiyat", float(price), _linear(float(price), PRICE_CAP_MINOR), weights.w5_price),
        ("club_follow", "Kulüp takibi", followed, followed, weights.w6_club_follow),
    ]
    factors = [
        ScoreFactor(
            key=key,
            label=label,
            raw=round(raw, 2),
            normalized=round(normalized, 4),
            weight=round(weight, 4),
            contribution=round(100 * weight * normalized, 2),
        )
        for key, label, raw, normalized, weight in specs
    ]
    return min(100.0, round(sum(factor.contribution for factor in factors), 1)), factors


def build_reason(row: dict[str, object], factors: list[ScoreFactor]) -> str:
    """Build a short Turkish explanation from the highest contributions."""
    phrases: list[str] = []
    for factor in sorted(factors, key=lambda item: item.contribution, reverse=True):
        if factor.key == "club_follow" and factor.normalized > 0:
            phrases.append(
                f"takip ettiğiniz {row.get('club_name') or 'kulüp'} tarafından düzenleniyor"
            )
        elif factor.key == "category" and factor.normalized >= 0.3:
            phrases.append(f"ilgi duyduğunuz {row.get('category')} kategorisinde")
        elif factor.key == "distance" and factor.normalized >= 0.4:
            phrases.append(
                f"size yalnızca {_distance_text(float(row.get('distance_m') or 0))} uzaklıkta"
            )
        elif factor.key == "popularity" and factor.normalized >= 0.4:
            phrases.append(f"{int(float(row.get('popularity') or 0))} kişi tarafından ilgi görüyor")
        elif factor.key == "price" and factor.normalized >= 0.7:
            phrases.append(
                "ücretsiz" if int(row.get("price_minor") or 0) == 0 else "bütçenize uygun"
            )
        if len(phrases) == 3:
            break
    if not phrases:
        return "Bunu önerdik çünkü size yakın ve yaklaşan etkinliklerden biri."
    return "Bunu önerdik çünkü " + ", ".join(phrases[:-1]) + " ve " + phrases[-1] + "."


@router.get("/recommendations", response_model=RecommendationsResponse)
async def discover_recommendations(
    session: SessionDep,
    user: OptionalUser,
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius: int = Query(DEFAULT_RADIUS_M, gt=0, le=50_000),
    limit: int = Query(default=20, ge=1, le=50),
) -> RecommendationsResponse:
    """Return up to 200 nearby candidates, scored with the transparent weights."""
    now = datetime.datetime.now(datetime.UTC)
    starts_from, starts_to = resolve_when(None, now)
    try:
        rows = await repo.fetch_candidates(
            session,
            lat=lat,
            lng=lng,
            radius_m=radius,
            starts_from=starts_from,
            starts_to=starts_to,
            limit=repo.MAX_CANDIDATES,
        )
    except repo.CandidateQueryTimeout as exc:
        raise ApiError(503, "Query timeout", "Narrow the radius.") from exc

    weights = _weights_from_rows(await repo.fetch_weights(session))
    interests, followed = await repo.fetch_user_signals(session, user.id if user else None)
    scored = []
    for row in rows:
        total, factors = score_candidate(
            row,
            radius_m=radius,
            weights=weights,
            interests=interests,
            followed_clubs=followed,
            now=now,
        )
        scored.append((total, row, factors))
    scored.sort(
        key=lambda item: (-item[0], float(item[1].get("distance_m") or 0), item[1]["starts_at"])
    )
    items = [
        RecommendationOut(
            event=_event_out(row), score=total, reason=build_reason(row, factors), factors=factors
        )
        for total, row, factors in scored[:limit]
    ]
    return RecommendationsResponse(
        count=len(items),
        candidate_count=len(rows),
        weights=weights,
        generated_at=now,
        items=items,
    )
