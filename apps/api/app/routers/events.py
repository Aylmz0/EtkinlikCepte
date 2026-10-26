"""Event, ticket and registration endpoints (H2.4/H2.5, §8 Etkinlik/Bilet)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import ApiError
from app.repos import event_repo
from app.repos.auth import User
from app.repos.events import EventStatus
from app.schemas.event import (
    EventCreate,
    EventList,
    EventRead,
    EventUpdate,
    RegistrationCreate,
    RegistrationRead,
    TicketCreate,
    TicketRead,
)

router = APIRouter(prefix="/events", tags=["events"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _event_out(event: object) -> EventRead:
    return EventRead.model_validate(event)


def _ticket_out(ticket: object) -> TicketRead:
    return TicketRead.model_validate(ticket)


def _registration_out(reg: object) -> RegistrationRead:
    return RegistrationRead.model_validate(reg)


@router.get("", response_model=EventList)
async def list_events(
    session: SessionDep,
    club_id: uuid.UUID | None = None,
    limit: int = Query(default=50, ge=1, le=100),
) -> EventList:
    """List events newest first, optionally by club."""
    events = await event_repo.list_events(session, club_id=club_id, limit=limit)
    return EventList(items=[_event_out(event) for event in events], next_cursor=None)


@router.post("", response_model=EventRead, status_code=201)
async def create_event(payload: EventCreate, user: CurrentUser, session: SessionDep) -> EventRead:
    """Create a draft event; the caller must manage the club."""
    # A draft event has no row yet, so check the club role directly.
    from app.repos.club_repo import club_role
    from app.repos.clubs import ClubRole

    if await club_role(session, payload.club_id, user.id) not in {ClubRole.owner, ClubRole.admin}:
        raise ApiError(403, "Forbidden", "Only club owners/admins can create events.")
    event = await event_repo.create_event(
        session,
        club_id=payload.club_id,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        venue_id=payload.venue_id,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        is_online=payload.is_online,
        online_url=payload.online_url,
        capacity=payload.capacity,
        created_by=user.id,
    )
    return _event_out(event)


@router.get("/{event_id}", response_model=EventRead)
async def get_event(event_id: uuid.UUID, session: SessionDep) -> EventRead:
    """Read one event."""
    event = await event_repo.get_event(session, event_id)
    if event is None:
        raise ApiError(404, "Not found", "Event does not exist.")
    return _event_out(event)


async def _event_for_manager(event_id: uuid.UUID, user: User, session: AsyncSession):
    event = await event_repo.get_event(session, event_id)
    if event is None:
        raise ApiError(404, "Not found", "Event does not exist.")
    if not await event_repo.can_manage_event(session, event, user.id):
        raise ApiError(403, "Forbidden", "Only club owners/admins can do this.")
    return event


@router.patch("/{event_id}", response_model=EventRead)
async def update_event(
    event_id: uuid.UUID, payload: EventUpdate, user: CurrentUser, session: SessionDep
) -> EventRead:
    """Update an event; managers only."""
    event = await _event_for_manager(event_id, user, session)
    event = await event_repo.update_event(session, event, payload.model_dump(exclude_unset=True))
    return _event_out(event)


@router.post("/{event_id}/publish", response_model=EventRead)
async def publish_event(event_id: uuid.UUID, user: CurrentUser, session: SessionDep) -> EventRead:
    """Publish a draft event."""
    event = await _event_for_manager(event_id, user, session)
    return _event_out(await event_repo.set_event_status(session, event, EventStatus.published))


@router.post("/{event_id}/cancel", response_model=EventRead)
async def cancel_event(event_id: uuid.UUID, user: CurrentUser, session: SessionDep) -> EventRead:
    """Cancel an event."""
    event = await _event_for_manager(event_id, user, session)
    return _event_out(await event_repo.set_event_status(session, event, EventStatus.cancelled))


@router.get("/{event_id}/tickets", response_model=list[TicketRead])
async def list_tickets(event_id: uuid.UUID, session: SessionDep) -> list[TicketRead]:
    """List ticket types for an event."""
    return [_ticket_out(ticket) for ticket in await event_repo.list_tickets(session, event_id)]


@router.post("/{event_id}/tickets", response_model=TicketRead, status_code=201)
async def create_ticket(
    event_id: uuid.UUID, payload: TicketCreate, user: CurrentUser, session: SessionDep
) -> TicketRead:
    """Create a ticket type; managers only."""
    await _event_for_manager(event_id, user, session)
    ticket = await event_repo.create_ticket(
        session,
        event_id=event_id,
        name=payload.name,
        price_minor=payload.price_minor,
        currency=payload.currency,
        quantity=payload.quantity,
        sales_start=payload.sales_start,
        sales_end=payload.sales_end,
    )
    return _ticket_out(ticket)


@router.post("/{event_id}/register", response_model=RegistrationRead)
async def register(
    event_id: uuid.UUID, payload: RegistrationCreate, user: CurrentUser, session: SessionDep
) -> RegistrationRead:
    """Reserve a ticket; free tickets become immediately valid."""
    event = await event_repo.get_event(session, event_id)
    if event is None or event.status != EventStatus.published:
        raise ApiError(404, "Not found", "Published event does not exist.")
    ticket = await event_repo.get_ticket(session, payload.ticket_id)
    if ticket is None or ticket.event_id != event_id:
        raise ApiError(404, "Not found", "Ticket does not exist for this event.")
    try:
        registration = await event_repo.register_for_event(
            session, event=event, ticket=ticket, user_id=user.id, quantity=payload.quantity
        )
    except ValueError as exc:
        code = 409 if str(exc) == "already registered" else 400
        raise ApiError(code, "Registration failed", str(exc)) from exc
    return _registration_out(registration)
