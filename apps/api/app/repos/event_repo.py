"""Event, ticket and registration persistence (H2.4/H2.5)."""

from __future__ import annotations

import datetime
import secrets
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tickets import RegistrationStatus, can_transition
from app.repos.clubs import ClubMember, ClubRole
from app.repos.events import Event, EventStatus, EventTicket, Registration, TicketKind


async def list_events(
    session: AsyncSession, *, club_id: uuid.UUID | None, limit: int = 50
) -> list[Event]:
    """List events newest first, optionally by club."""
    query = select(Event).order_by(Event.starts_at.asc()).limit(limit)
    if club_id:
        query = query.where(Event.club_id == club_id)
    result = await session.execute(query)
    return list(result.scalars())


async def get_event(session: AsyncSession, event_id: uuid.UUID) -> Event | None:
    """Read one event."""
    result = await session.execute(select(Event).where(Event.id == event_id))
    return result.scalar_one_or_none()


async def can_manage_event(session: AsyncSession, event: Event, user_id: uuid.UUID) -> bool:
    """Return whether the user owns/admins the event's club."""
    if event.club_id is None:
        return False
    role = await session.execute(
        select(ClubMember.role).where(
            ClubMember.club_id == event.club_id,
            ClubMember.user_id == user_id,
            ClubMember.role.in_([ClubRole.owner, ClubRole.admin]),
        )
    )
    return role.scalar_one_or_none() is not None


async def create_event(
    session: AsyncSession,
    *,
    club_id: uuid.UUID,
    title: str,
    description: str | None,
    category: str | None,
    venue_id: uuid.UUID | None,
    starts_at: datetime.datetime,
    ends_at: datetime.datetime | None,
    is_online: bool,
    online_url: str | None,
    capacity: int | None,
    created_by: uuid.UUID,
) -> Event:
    """Create a draft event."""
    event = Event(
        id=uuid.uuid4(),
        club_id=club_id,
        venue_id=venue_id,
        title=title,
        description=description,
        category=category,
        starts_at=starts_at,
        ends_at=ends_at,
        is_online=is_online,
        online_url=online_url,
        capacity=capacity,
        status=EventStatus.draft,
        origin="club",
        trust="verified",
        created_by=created_by,
        created_at=datetime.datetime.now(datetime.UTC),
    )
    session.add(event)
    await session.commit()
    return event


async def update_event(session: AsyncSession, event: Event, changes: dict[str, object]) -> Event:
    """Apply a partial event update."""
    for key, value in changes.items():
        setattr(event, key, value)
    await session.commit()
    return event


async def set_event_status(session: AsyncSession, event: Event, status: EventStatus) -> Event:
    """Publish, cancel or complete an event."""
    event.status = status
    await session.commit()
    return event


async def list_tickets(session: AsyncSession, event_id: uuid.UUID) -> list[EventTicket]:
    """List ticket types for an event."""
    result = await session.execute(select(EventTicket).where(EventTicket.event_id == event_id))
    return list(result.scalars())


async def create_ticket(
    session: AsyncSession,
    *,
    event_id: uuid.UUID,
    name: str,
    price_minor: int,
    currency: str,
    quantity: int,
    sales_start: datetime.datetime | None,
    sales_end: datetime.datetime | None,
) -> EventTicket:
    """Create a ticket type."""
    ticket = EventTicket(
        id=uuid.uuid4(),
        event_id=event_id,
        name=name,
        price_minor=price_minor,
        currency=currency,
        quantity=quantity,
        sold_count=0,
        sales_start=sales_start,
        sales_end=sales_end,
        kind=TicketKind.free if price_minor == 0 else TicketKind.paid,
    )
    session.add(ticket)
    await session.commit()
    return ticket


async def get_ticket(session: AsyncSession, ticket_id: uuid.UUID) -> EventTicket | None:
    """Read one ticket type."""
    result = await session.execute(select(EventTicket).where(EventTicket.id == ticket_id))
    return result.scalar_one_or_none()


async def active_reservations(session: AsyncSession, ticket_id: uuid.UUID) -> int:
    """Count reserved/pending/paid quantities for capacity checks."""
    result = await session.execute(
        select(func.coalesce(func.sum(Registration.quantity), 0)).where(
            Registration.ticket_id == ticket_id,
            Registration.status.in_(
                [RegistrationStatus.reserved, RegistrationStatus.pending_payment]
            ),
        )
    )
    return int(result.scalar_one())


async def get_registration(
    session: AsyncSession, registration_id: uuid.UUID
) -> Registration | None:
    """Read one registration."""
    result = await session.execute(select(Registration).where(Registration.id == registration_id))
    return result.scalar_one_or_none()


async def register_for_event(
    session: AsyncSession, *, event: Event, ticket: EventTicket, user_id: uuid.UUID, quantity: int
) -> Registration:
    """Create a reservation/free registration and enforce capacity."""
    existing = await session.execute(
        select(Registration).where(
            Registration.event_id == event.id, Registration.user_id == user_id
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise ValueError("already registered")
    active = await active_reservations(session, ticket.id)
    if (ticket.sold_count or 0) + active + quantity > (ticket.quantity or 0):
        raise ValueError("capacity")
    now = datetime.datetime.now(datetime.UTC)
    is_free = ticket.kind == TicketKind.free or (ticket.price_minor or 0) == 0
    registration = Registration(
        id=uuid.uuid4(),
        event_id=event.id,
        user_id=user_id,
        ticket_id=ticket.id,
        quantity=quantity,
        status=RegistrationStatus.free_granted if is_free else RegistrationStatus.reserved,
        amount_minor=(ticket.price_minor or 0) * quantity,
        reserved_until=None if is_free else now + datetime.timedelta(minutes=15),
        qr_token=secrets.token_urlsafe(32),
        created_at=now,
    )
    if is_free:
        ticket.sold_count = (ticket.sold_count or 0) + quantity
    session.add(registration)
    await session.commit()
    return registration


async def cancel_registration(
    session: AsyncSession, registration: Registration, *, by_organizer: bool
) -> Registration:
    """Cancel a registration and release sold capacity when it counted."""
    if not can_transition(RegistrationStatus(registration.status), RegistrationStatus.cancelled):
        raise ValueError("transition")
    if registration.status in {RegistrationStatus.paid, RegistrationStatus.free_granted}:
        ticket = await get_ticket(session, registration.ticket_id)
        if ticket is not None:
            ticket.sold_count = max(0, (ticket.sold_count or 0) - registration.quantity)
    registration.status = RegistrationStatus.cancelled
    await session.commit()
    return registration


async def check_in(session: AsyncSession, registration: Registration) -> Registration:
    """Mark a paid/free registration as used."""
    if not can_transition(RegistrationStatus(registration.status), RegistrationStatus.used):
        raise ValueError("transition")
    registration.status = RegistrationStatus.used
    registration.checked_in_at = datetime.datetime.now(datetime.UTC)
    await session.commit()
    return registration
