"""Event and ticketing tables (§7 Etkinlikler).

Capacity rule (§8.1 rule 7): sold_count grows only from paid and
free_granted registrations; reserved and pending_payment hold capacity
without counting until they expire.
"""

from __future__ import annotations

import datetime
import enum
import uuid

from sqlalchemy import CHAR, TIMESTAMP, Enum, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.tickets import RegistrationStatus
from app.repos.base import Base, uuid_pk


class EventOrigin(enum.StrEnum):
    """Whether the event was entered by a club or collected from a source."""

    club = "club"
    collected = "collected"


class EventTrust(enum.StrEnum):
    """Verification level of the event record."""

    verified = "verified"
    collected = "collected"


class EventStatus(enum.StrEnum):
    """Lifecycle status of an event."""

    draft = "draft"
    published = "published"
    cancelled = "cancelled"
    completed = "completed"


class TicketKind(enum.StrEnum):
    """Free or paid ticket type."""

    free = "free"
    paid = "paid"


class Event(Base):
    """User-facing event: either a club entry or a collected record (§7)."""

    __tablename__ = "events"

    id: Mapped[uuid.UUID] = uuid_pk()
    club_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("clubs.id"))
    venue_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("venues.id"))
    title: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(Text)
    cover_media_id: Mapped[uuid.UUID | None]
    starts_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    ends_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    is_online: Mapped[bool | None]
    online_url: Mapped[str | None] = mapped_column(Text)
    capacity: Mapped[int | None]
    origin: Mapped[EventOrigin] = mapped_column(
        Enum(EventOrigin, name="event_origin"), default=EventOrigin.club
    )
    trust: Mapped[EventTrust] = mapped_column(
        Enum(EventTrust, name="event_trust"), default=EventTrust.verified
    )
    status: Mapped[EventStatus | None] = mapped_column(Enum(EventStatus, name="event_status"))
    created_by: Mapped[uuid.UUID | None]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (
        Index("ix_events_starts_at", "starts_at"),
        Index("ix_events_status", "status"),
        Index("ix_events_origin_status", "origin", "status"),
    )


class EventSource(Base):
    """Links one event to every source listing it; one row is primary."""

    __tablename__ = "event_sources"

    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("events.id"), primary_key=True)
    source_event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("source_events.id"), primary_key=True, index=True
    )
    is_primary: Mapped[bool | None]


class EventTicket(Base):
    """Ticket type; one user may hold several (group purchase, §7)."""

    __tablename__ = "event_tickets"

    id: Mapped[uuid.UUID] = uuid_pk()
    event_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("events.id"))
    name: Mapped[str | None] = mapped_column(Text)
    price_minor: Mapped[int | None] = mapped_column(Integer)
    currency: Mapped[str | None] = mapped_column(CHAR(3))
    quantity: Mapped[int | None] = mapped_column(Integer)
    sold_count: Mapped[int | None] = mapped_column(Integer)
    sales_start: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    sales_end: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    kind: Mapped[TicketKind | None] = mapped_column(Enum(TicketKind, name="ticket_kind"))


class Registration(Base):
    """Ticket hold through the state machine; one row per (event, user)."""

    __tablename__ = "registrations"

    id: Mapped[uuid.UUID] = uuid_pk()
    event_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("events.id"))
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    ticket_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("event_tickets.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[RegistrationStatus | None] = mapped_column(
        Enum(RegistrationStatus, name="registration_status")
    )
    amount_minor: Mapped[int | None] = mapped_column(Integer)
    reserved_until: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    qr_token: Mapped[str | None] = mapped_column(Text, unique=True)
    checked_in_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (
        Index("ix_registrations_event_status", "event_id", "status"),
        Index("uq_registrations_event_user", "event_id", "user_id", unique=True),
    )


class EventInvitation(Base):
    """Capacity-capped redeem code for one event (§7)."""

    __tablename__ = "event_invitations"

    id: Mapped[uuid.UUID] = uuid_pk()
    event_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("events.id"))
    code: Mapped[str | None] = mapped_column(Text, unique=True)
    created_by: Mapped[uuid.UUID | None]
    max_uses: Mapped[int | None] = mapped_column(Integer)
    uses: Mapped[int | None] = mapped_column(Integer)
    expires_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
