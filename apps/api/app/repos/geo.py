"""Geo tables: venues and raw collected source_events (§7 Coğrafi).

events shown to users live in app.repos.events; source_events rows never
reach the UI directly.
"""

from __future__ import annotations

import datetime
import uuid

from geoalchemy2 import Geometry
from sqlalchemy import CHAR, TIMESTAMP, Index, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.repos.base import Base, uuid_pk


class Venue(Base):
    """Physical place with a PostGIS point (§7)."""

    __tablename__ = "venues"

    id: Mapped[uuid.UUID] = uuid_pk()
    name: Mapped[str | None] = mapped_column(Text)
    address: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(Text)
    geom = mapped_column(Geometry("POINT", srid=4326, spatial_index=False))
    category: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(Text)
    source_ref: Mapped[str | None] = mapped_column(Text)
    capacity: Mapped[int | None]
    wheelchair_accessible: Mapped[bool | None]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (Index("ix_venues_geom", "geom", postgresql_using="gist"),)


class SourceEvent(Base):
    """Raw row scraped from one source; dedup key is (source, source_ref)."""

    __tablename__ = "source_events"

    id: Mapped[uuid.UUID] = uuid_pk()
    source: Mapped[str | None] = mapped_column(Text)
    source_ref: Mapped[str | None] = mapped_column(Text)
    title_raw: Mapped[str | None] = mapped_column(Text)
    venue_geom = mapped_column(Geometry("POINT", srid=4326, spatial_index=False))
    starts_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    ends_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    price_minor: Mapped[int | None] = mapped_column(Integer)
    currency: Mapped[str | None] = mapped_column(CHAR(3))
    url: Mapped[str | None] = mapped_column(Text)
    payload: Mapped[dict | None] = mapped_column(JSONB)
    fetched_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    content_hash: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        Index("ix_source_events_geom", "venue_geom", postgresql_using="gist"),
        Index("uq_source_events_ref", "source", "source_ref", unique=True),
    )
