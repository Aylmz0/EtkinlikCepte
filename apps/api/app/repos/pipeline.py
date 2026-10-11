"""Pipeline-owned tables: source configs and ranking inputs (§7).

Tuning values live here, not in code: ranking weights are rows in
ranking_weights (AGENTS.md coherence rule).
"""

from __future__ import annotations

import datetime
import uuid

from sqlalchemy import TIMESTAMP, Numeric, Text
from sqlalchemy.dialects.postgresql import CITEXT, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.repos.base import Base, uuid_pk


class SourceConfig(Base):
    """Scraper configuration with Terms-of-Service audit trail (owner P3)."""

    __tablename__ = "source_configs"

    id: Mapped[uuid.UUID] = uuid_pk()
    name: Mapped[str] = mapped_column(CITEXT, unique=True)
    adapter: Mapped[str | None] = mapped_column(Text)
    enabled: Mapped[bool | None]
    schedule_cron: Mapped[str | None] = mapped_column(Text)
    rate_limit_rps: Mapped[float | None] = mapped_column(Numeric)
    user_agent: Mapped[str | None] = mapped_column(Text)
    terms_checked_at: Mapped[datetime.date | None]
    terms_url: Mapped[str | None] = mapped_column(Text)
    config: Mapped[dict | None] = mapped_column(JSONB)
    last_run_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    last_status: Mapped[str | None] = mapped_column(Text)


class RankingWeight(Base):
    """Named recommendation weight, tuned per place without code changes."""

    __tablename__ = "ranking_weights"

    name: Mapped[str] = mapped_column(Text, primary_key=True)
    value: Mapped[float | None] = mapped_column(Numeric)


class UserEventStat(Base):
    """Cached per-user event score feeding the transparent ranker (owner P4)."""

    __tablename__ = "user_event_stats"

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    event_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    score: Mapped[float | None] = mapped_column(Numeric)
    updated_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
