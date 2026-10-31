"""Raw adapter rows -> clean events -> duplicate groups (H3.1)."""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from pipeline.clean import clean_date, clean_price
from pipeline.dedup import cluster_duplicates

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class CleanEvent:
    """One cleaned source record, ready for the ``source_events`` table."""

    id: uuid.UUID
    source: str
    source_ref: str
    title: str
    starts_at: datetime
    ends_at: datetime | None
    price_minor: int | None
    currency: str | None
    venue_name: str
    lat: float | None
    lon: float | None
    url: str
    payload: dict[str, Any]
    content_hash: str
    fetched_at: datetime

    def as_source_event_row(self) -> dict[str, Any]:
        """Columns of ``source_events`` (geometry is written by the loader)."""
        return {
            "id": self.id,
            "source": self.source,
            "source_ref": self.source_ref,
            "title_raw": self.title,
            "starts_at": self.starts_at,
            "ends_at": self.ends_at,
            "price_minor": self.price_minor,
            "currency": self.currency,
            "url": self.url,
            "payload": {**self.payload, "venue_name": self.venue_name},
            "fetched_at": self.fetched_at,
            "content_hash": self.content_hash,
        }


def _to_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _location(value: Any) -> tuple[str, float | None, float | None]:
    """Return (venue name, lat, lon) from a string or a schema.org Place."""
    if isinstance(value, list):
        value = value[0] if value else None
    if isinstance(value, dict):
        geo = value.get("geo")
        lat = lon = None
        if isinstance(geo, dict):
            lat, lon = _to_float(geo.get("latitude")), _to_float(geo.get("longitude"))
        return str(value.get("name") or "").strip(), lat, lon
    return str(value or "").strip(), None, None


def _price(payload: dict[str, Any]) -> tuple[int | None, str | None]:
    """Return (price in kurus, currency) from ``price`` or schema.org ``offers``."""
    raw: Any = payload.get("price")
    currency: Any = None
    offers = payload.get("offers")
    if isinstance(offers, list):
        offers = offers[0] if offers else None
    if isinstance(offers, dict):
        raw = offers.get("price", raw)
        currency = offers.get("priceCurrency")
    amount = clean_price(raw)
    if amount is None:
        return None, None
    return round(amount * 100), str(currency or "TRY").upper()[:3]


def to_clean_event(raw: dict[str, Any]) -> CleanEvent | None:
    """Clean one adapter row; return None (and log why) if it is unusable."""
    payload = raw.get("payload") or {}
    title = str(payload.get("title") or "").strip()
    starts_at = clean_date(payload.get("starts_at"))
    ref = str(raw.get("source_ref") or "").strip()
    if not title or starts_at is None:
        log.warning(
            "dropping unusable record",
            extra={"source": raw.get("source"), "ref": ref, "has_title": bool(title)},
        )
        return None
    venue_name, lat, lon = _location(payload.get("location"))
    price_minor, currency = _price(payload)
    return CleanEvent(
        id=uuid.uuid4(),
        source=str(raw["source"]),
        source_ref=ref,
        title=title,
        starts_at=starts_at,
        ends_at=clean_date(payload.get("ends_at")),
        price_minor=price_minor,
        currency=currency,
        venue_name=venue_name,
        lat=lat,
        lon=lon,
        url=ref,
        payload=payload,
        content_hash=str(raw["content_hash"]),
        fetched_at=datetime.now(UTC),
    )


def clean_rows(rows: list[dict[str, Any]]) -> tuple[list[CleanEvent], int]:
    """Clean many rows; returns (clean events, number dropped). Drops are never silent."""
    clean = [event for row in rows if (event := to_clean_event(row)) is not None]
    return clean, len(rows) - len(clean)


def group_duplicates(events: list[CleanEvent]) -> list[list[CleanEvent]]:
    """Group events that dedup rules consider the same event."""
    records = [
        {"id": i, "title": e.title, "starts_at": e.starts_at, "lat": e.lat, "lon": e.lon}
        for i, e in enumerate(events)
    ]
    clusters = cluster_duplicates(records)
    groups: dict[int, list[CleanEvent]] = {}
    for index, root in clusters.items():
        groups.setdefault(root, []).append(events[index])
    return [groups[root] for root in sorted(groups)]
