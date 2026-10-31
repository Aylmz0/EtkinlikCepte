"""Duplicate detection with polars lazy frames + rapidfuzz (H3.10, §3.3)."""

from __future__ import annotations

import math
from datetime import UTC
from typing import Any

import polars as pl
from rapidfuzz import fuzz

from pipeline.clean import TR_TZ, normalize_text

TITLE_SIMILARITY_THRESHOLD = 85
DISTANCE_TOLERANCE_M = 150.0
TIME_TOLERANCE_MINUTES = 120
_EARTH_RADIUS_M = 6_371_000.0


def _prepare(records: list[dict[str, Any]], suffix: str = "") -> pl.LazyFrame:
    """Build a lazy frame whose column names end with ``suffix``.

    ``starts_at`` must be a datetime (naive values are assumed Europe/Istanbul).
    """
    rows = []
    for rec in records:
        starts = rec["starts_at"]
        if starts.tzinfo is None:
            starts = starts.replace(tzinfo=TR_TZ)
        rows.append(
            {
                f"id{suffix}": rec["id"],
                f"title{suffix}": normalize_text(rec["title"]),
                f"day{suffix}": starts.astimezone(TR_TZ).date(),
                f"starts_at{suffix}": starts.astimezone(UTC).replace(tzinfo=None),
                f"lat{suffix}": rec.get("lat"),
                f"lon{suffix}": rec.get("lon"),
            }
        )
    schema = {
        f"id{suffix}": pl.Int64,
        f"title{suffix}": pl.String,
        f"day{suffix}": pl.Date,
        f"starts_at{suffix}": pl.Datetime,
        f"lat{suffix}": pl.Float64,
        f"lon{suffix}": pl.Float64,
    }
    return pl.LazyFrame(rows, schema=schema)


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in meters."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat = p2 - p1
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * _EARTH_RADIUS_M * math.asin(math.sqrt(a))


def find_duplicate_pairs(records: list[dict[str, Any]]) -> list[tuple[int, int]]:
    """Return (id_a, id_b) pairs that satisfy all dedup rules."""
    if len(records) < 2:
        return []
    left = _prepare(records)
    right = _prepare(records, suffix="_b")
    # Polars builds same-day candidate pairs; precise rules are applied below.
    candidates = (
        left.join(right, left_on="day", right_on="day_b", how="inner")
        .filter(pl.col("id") < pl.col("id_b"))
        .collect()
    )
    pairs: list[tuple[int, int]] = []
    for row in candidates.iter_rows(named=True):
        minutes = abs((row["starts_at"] - row["starts_at_b"]).total_seconds()) / 60
        if minutes > TIME_TOLERANCE_MINUTES:
            continue
        coords = (row["lat"], row["lon"], row["lat_b"], row["lon_b"])
        if None not in coords and haversine_m(*coords) > DISTANCE_TOLERANCE_M:
            continue
        if fuzz.token_set_ratio(row["title"], row["title_b"]) < TITLE_SIMILARITY_THRESHOLD:
            continue
        pairs.append((row["id"], row["id_b"]))
    return sorted(pairs)


def cluster_duplicates(records: list[dict[str, Any]]) -> dict[int, int]:
    """Map every record id to its cluster representative (smallest id)."""
    parent = {rec["id"]: rec["id"] for rec in records}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in find_duplicate_pairs(records):
        root_a, root_b = find(a), find(b)
        if root_a != root_b:
            parent[max(root_a, root_b)] = min(root_a, root_b)
    return {rec_id: find(rec_id) for rec_id in parent}
