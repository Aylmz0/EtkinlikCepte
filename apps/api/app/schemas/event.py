"""Event schemas for the H1.8 router draft (§7, §8)."""

from __future__ import annotations

import datetime
import enum
import uuid

from pydantic import BaseModel, Field


class EventStatus(enum.StrEnum):
    """Lifecycle status exposed by the API."""

    draft = "draft"
    published = "published"
    cancelled = "cancelled"
    completed = "completed"


class EventCreate(BaseModel):
    """Payload for creating a club event."""

    title: str = Field(min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=10_000)
    category: str | None = Field(default=None, max_length=80)
    venue_id: uuid.UUID | None = None
    starts_at: datetime.datetime
    ends_at: datetime.datetime | None = None
    is_online: bool = False
    online_url: str | None = Field(default=None, max_length=500)
    capacity: int | None = Field(default=None, ge=1)


class EventRead(BaseModel):
    """Event representation returned by list and detail endpoints."""

    id: uuid.UUID
    club_id: uuid.UUID | None = None
    venue_id: uuid.UUID | None = None
    title: str
    description: str | None = None
    category: str | None = None
    starts_at: datetime.datetime
    ends_at: datetime.datetime | None = None
    is_online: bool = False
    status: EventStatus
    created_at: datetime.datetime


class EventList(BaseModel):
    """Cursor page of events."""

    items: list[EventRead]
    next_cursor: str | None = None
