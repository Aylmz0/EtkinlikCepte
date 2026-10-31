"""Notification schemas (§8 Bildirim, H2.19)."""

from __future__ import annotations

import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class NotificationRead(BaseModel):
    """In-app notification row."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    kind: str | None = None
    title: str | None = None
    body: str | None = None
    data: dict | None = None
    read_at: datetime.datetime | None = None
    created_at: datetime.datetime
