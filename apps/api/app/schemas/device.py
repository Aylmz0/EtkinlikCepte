"""Device registration schemas (§8 Cihaz, H2.19)."""

from __future__ import annotations

import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):
    """Register this device for presence/version tracking."""

    platform: str = Field(min_length=2, max_length=32)
    app_version: str = Field(min_length=1, max_length=32)


class DeviceRead(BaseModel):
    """Registered device."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    platform: str | None = None
    app_version: str | None = None
    last_seen: datetime.datetime | None = None
