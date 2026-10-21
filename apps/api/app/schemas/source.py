"""Admin source-config schemas (§7 source_configs, §8 Yönetim)."""

from __future__ import annotations

import datetime
import uuid

from pydantic import BaseModel, Field


class SourceConfigRead(BaseModel):
    """A scraper source as shown to admins."""

    id: uuid.UUID
    name: str
    adapter: str | None = None
    enabled: bool
    schedule_cron: str | None = None
    rate_limit_rps: float | None = Field(default=None, ge=0)
    user_agent: str | None = None
    terms_checked_at: datetime.date | None = None
    terms_url: str | None = None
    last_run_at: datetime.datetime | None = None
    last_status: str | None = None


class SourceConfigUpdate(BaseModel):
    """Partial update for a source; omitted fields stay unchanged."""

    enabled: bool | None = None
    schedule_cron: str | None = None
    rate_limit_rps: float | None = Field(default=None, ge=0)
    user_agent: str | None = None
