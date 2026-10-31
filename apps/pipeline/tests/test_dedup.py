"""Dedup tests: thresholds from docs/dedup-rules.md (R11)."""

from datetime import datetime

from pipeline.clean import TR_TZ
from pipeline.dedup import cluster_duplicates, find_duplicate_pairs


def _rec(rec_id: int, title: str, hour: int, lat: float | None, lon: float | None, day: int = 12):
    return {
        "id": rec_id,
        "title": title,
        "starts_at": datetime(2026, 11, day, hour, 0, tzinfo=TR_TZ),
        "lat": lat,
        "lon": lon,
    }


def test_same_event_from_two_sources_is_duplicate() -> None:
    records = [
        _rec(1, "Sahne Gecesi", 20, 41.0082, 28.9784),
        _rec(2, "SAHNE GECESİ - Kültür Merkezi", 20, 41.0085, 28.9786),
    ]
    assert find_duplicate_pairs(records) == [(1, 2)]


def test_far_away_same_title_is_not_duplicate() -> None:
    records = [
        _rec(1, "Sahne Gecesi", 20, 41.0082, 28.9784),
        _rec(2, "Sahne Gecesi", 20, 39.9334, 32.8597),  # Ankara
    ]
    assert find_duplicate_pairs(records) == []


def test_different_day_or_time_is_not_duplicate() -> None:
    records = [
        _rec(1, "Sahne Gecesi", 20, 41.0082, 28.9784),
        _rec(2, "Sahne Gecesi", 20, 41.0082, 28.9784, day=13),
        _rec(3, "Sahne Gecesi", 11, 41.0082, 28.9784),
    ]
    assert find_duplicate_pairs(records) == []


def test_missing_coordinates_fall_back_to_title_and_time() -> None:
    records = [_rec(1, "Bahçe Konseri", 18, None, None), _rec(2, "Bahçe Konseri", 18, None, None)]
    assert find_duplicate_pairs(records) == [(1, 2)]


def test_clusters_use_smallest_id() -> None:
    records = [
        _rec(5, "Sahne Gecesi", 20, 41.0082, 28.9784),
        _rec(2, "Sahne Gecesi", 20, 41.0083, 28.9784),
        _rec(9, "Bambaşka Etkinlik", 20, 41.0082, 28.9784),
    ]
    assert cluster_duplicates(records) == {5: 2, 2: 2, 9: 9}
