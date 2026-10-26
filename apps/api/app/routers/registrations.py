"""Registration QR and check-in endpoints (H2.5, §8 Bilet)."""

from __future__ import annotations

import uuid
from typing import Annotated

import segno
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import ApiError
from app.repos import event_repo
from app.repos.auth import User
from app.repos.events import RegistrationStatus

router = APIRouter(prefix="/registrations", tags=["tickets"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


async def _registration_for_user(registration_id: uuid.UUID, user: User, session: AsyncSession):
    registration = await event_repo.get_registration(session, registration_id)
    if registration is None:
        raise ApiError(404, "Not found", "Registration does not exist.")
    if registration.user_id != user.id:
        event = await event_repo.get_event(session, registration.event_id)
        if event is None or not await event_repo.can_manage_event(session, event, user.id):
            raise ApiError(403, "Forbidden", "Not your registration.")
    return registration


@router.delete("/{registration_id}", response_model=dict[str, str])
async def cancel_registration(
    registration_id: uuid.UUID, user: CurrentUser, session: SessionDep
) -> dict[str, str]:
    """Cancel a registration; owners and event managers can cancel."""
    registration = await _registration_for_user(registration_id, user, session)
    try:
        await event_repo.cancel_registration(
            session, registration, by_organizer=registration.user_id != user.id
        )
    except ValueError as exc:
        raise ApiError(409, "Conflict", "Registration cannot be cancelled.") from exc
    return {"status": "cancelled"}


@router.get("/{registration_id}/qr")
async def qr_code(registration_id: uuid.UUID, user: CurrentUser, session: SessionDep) -> Response:
    """Return the registration QR as an SVG image."""
    registration = await _registration_for_user(registration_id, user, session)
    if registration.qr_token is None:
        raise ApiError(404, "Not found", "QR token is missing.")
    svg = segno.make(registration.qr_token, error="m").svg_inline()
    return Response(content=svg, media_type="image/svg+xml")


@router.post("/{registration_id}/checkin", response_model=dict[str, str])
async def check_in(
    registration_id: uuid.UUID, user: CurrentUser, session: SessionDep
) -> dict[str, str]:
    """Mark a paid/free registration as used at the door."""
    registration = await event_repo.get_registration(session, registration_id)
    if registration is None:
        raise ApiError(404, "Not found", "Registration does not exist.")
    event = await event_repo.get_event(session, registration.event_id)
    if event is None or not await event_repo.can_manage_event(session, event, user.id):
        raise ApiError(403, "Forbidden", "Only event managers can check in.")
    if registration.status not in {RegistrationStatus.paid, RegistrationStatus.free_granted}:
        raise ApiError(409, "Conflict", "Registration is not valid for check-in.")
    try:
        await event_repo.check_in(session, registration)
    except ValueError as exc:
        raise ApiError(409, "Conflict", "Registration cannot be checked in.") from exc
    return {"status": "used"}
