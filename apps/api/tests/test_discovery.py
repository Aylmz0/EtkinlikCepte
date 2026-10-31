"""H2.6/H2.16/H2.17 discovery helpers: filters, folding, scoring, reasons."""

from __future__ import annotations

import datetime
import uuid

from app.repos.discovery_repo import tr_fold
from app.routers.discover import (
    build_reason,
    parse_bbox,
    resolve_when,
    score_candidate,
)
from app.schemas.discovery import RankingWeights


def test_tr_fold_handles_turkish_characters() -> None:
    """Category/title matching is Turkish-insensitive."""
    assert tr_fold("İSTANBUL") == "istanbul"
    assert tr_fold("Şişli") == "sisli"
    assert tr_fold("Müzik") == "muzik"


def test_parse_bbox_rejects_inverted_coordinates() -> None:
    """An invalid bbox becomes a 422 at the boundary."""
    try:
        parse_bbox("39,40,38,41")
    except Exception as exc:  # ApiError is the public contract
        assert getattr(exc, "status_code", None) == 422
    else:
        raise AssertionError("inverted bbox accepted")


def test_resolve_when_week_is_seven_days() -> None:
    """The week filter produces a seven-day window."""
    now = datetime.datetime(2026, 10, 26, 12, tzinfo=datetime.UTC)
    start, end = resolve_when("week", now)
    assert start == now
    assert end - start == datetime.timedelta(days=7)


def test_score_candidate_prefers_followed_club_and_interest() -> None:
    """The transparent score exposes each factor and boosts follow/category."""
    now = datetime.datetime(2026, 10, 26, 12, tzinfo=datetime.UTC)
    club_id = uuid.uuid4()
    row = {
        "id": uuid.uuid4(),
        "title": "Kampüs Konseri",
        "category": "Müzik",
        "starts_at": now + datetime.timedelta(days=1),
        "ends_at": None,
        "venue_id": uuid.uuid4(),
        "venue_name": "Kültür Merkezi",
        "club_id": club_id,
        "club_name": "Müzik Kulübü",
        "lat": 39.9,
        "lng": 32.8,
        "distance_m": 700.0,
        "price_minor": 0,
        "currency": "TRY",
        "popularity": 120,
        "created_at": now - datetime.timedelta(days=1),
    }
    score, factors = score_candidate(
        row,
        radius_m=10_000,
        weights=RankingWeights().normalized(),
        interests={"muzik"},
        followed_clubs={club_id},
        now=now,
    )
    by_key = {factor.key: factor for factor in factors}
    assert by_key["category"].normalized == 1.0
    assert by_key["club_follow"].normalized == 1.0
    assert by_key["distance"].contribution > 0
    assert 0 <= score <= 100
    assert "takip ettiğiniz" in build_reason(row, factors)
