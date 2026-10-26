"""Event schemas for the H1.8 router draft (§7, §8)."""

from __future__ import annotations

import datetime
import enum
import uuid

from pydantic import BaseModel, ConfigDict, Field


class EventStatus(enum.StrEnum):
    """Lifecycle status exposed by the API."""

    draft = "draft"
    published = "published"
    cancelled = "cancelled"
    completed = "completed"


class EventCreate(BaseModel):
    """Payload for creating a club event."""

    club_id: uuid.UUID
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

    model_config = ConfigDict(from_attributes=True)

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


class EventUpdate(BaseModel):
    """Partial event update."""

    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=10_000)
    category: str | None = Field(default=None, max_length=80)
    venue_id: uuid.UUID | None = None
    starts_at: datetime.datetime | None = None
    ends_at: datetime.datetime | None = None
    is_online: bool | None = None
    online_url: str | None = Field(default=None, max_length=500)
    capacity: int | None = Field(default=None, ge=1)


class TicketCreate(BaseModel):
    """Create a ticket type for an event."""

    name: str = Field(min_length=1, max_length=80)
    price_minor: int = Field(default=0, ge=0)
    currency: str = Field(default="TRY", min_length=3, max_length=3)
    quantity: int = Field(ge=1)
    sales_start: datetime.datetime | None = None
    sales_end: datetime.datetime | None = None


class TicketRead(BaseModel):
    """Ticket type returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    event_id: uuid.UUID
    name: str
    price_minor: int
    currency: str
    quantity: int
    sold_count: int
    kind: str
    sales_start: datetime.datetime | None = None
    sales_end: datetime.datetime | None = None


class RegistrationCreate(BaseModel):
    """Register for one ticket type; quantity > 1 is a group ticket."""

    ticket_id: uuid.UUID
    quantity: int = Field(default=1, ge=1, le=10)


class RegistrationRead(BaseModel):
    """Registration state returned to the buyer."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    event_id: uuid.UUID
    user_id: uuid.UUID
    ticket_id: uuid.UUID
    quantity: int
    status: str
    amount_minor: int | None = None
    reserved_until: datetime.datetime | None = None
    qr_token: str | None = None
    checked_in_at: datetime.datetime | None = None
