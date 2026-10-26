"""Club, membership and invitation endpoints (H2.3, §8 Kulüp)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import ApiError
from app.repos import club_repo
from app.repos.auth import User
from app.repos.clubs import Club, ClubRole
from app.schemas.club import (
    ClubCreate,
    ClubInvitationCreate,
    ClubInvitationRead,
    ClubList,
    ClubMemberAdd,
    ClubMemberRead,
    ClubRead,
    ClubUpdate,
)

router = APIRouter(prefix="/clubs", tags=["clubs"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _club_out(club: object) -> ClubRead:
    return ClubRead.model_validate(club)


def _require_manager(role: ClubRole | None) -> None:
    if role not in {ClubRole.owner, ClubRole.admin}:
        raise ApiError(403, "Forbidden", "Only club owners/admins can do this.")


@router.get("", response_model=ClubList)
async def list_clubs(session: SessionDep, limit: int = Query(default=50, ge=1, le=100)) -> ClubList:
    """List clubs newest first."""
    clubs = await club_repo.list_clubs(session, limit)
    return ClubList(items=[_club_out(club) for club in clubs], next_cursor=None)


@router.post("", response_model=ClubRead, status_code=201)
async def create_club(payload: ClubCreate, user: CurrentUser, session: SessionDep) -> ClubRead:
    """Create a club and make the caller its owner."""
    existing = await session.execute(select(Club).where(club_repo.Club.slug == payload.slug))
    if existing.scalar_one_or_none() is not None:
        raise ApiError(409, "Conflict", "This slug is already taken.")
    club = await club_repo.create_club(
        session,
        name=payload.name,
        slug=payload.slug,
        description=payload.description,
        city=payload.city,
        owner=user,
    )
    return _club_out(club)


@router.get("/{club_id}", response_model=ClubRead)
async def get_club(club_id: uuid.UUID, session: SessionDep) -> ClubRead:
    """Read one club."""
    club = await club_repo.get_club(session, club_id)
    if club is None:
        raise ApiError(404, "Not found", "Club does not exist.")
    return _club_out(club)


@router.patch("/{club_id}", response_model=ClubRead)
async def update_club(
    club_id: uuid.UUID, payload: ClubUpdate, user: CurrentUser, session: SessionDep
) -> ClubRead:
    """Update a club; owners/admins only."""
    club = await club_repo.get_club(session, club_id)
    if club is None:
        raise ApiError(404, "Not found", "Club does not exist.")
    _require_manager(await club_repo.club_role(session, club_id, user.id))
    club = await club_repo.update_club(session, club, payload.model_dump(exclude_unset=True))
    return _club_out(club)


@router.post("/{club_id}/members", response_model=ClubMemberRead)
async def add_member(
    club_id: uuid.UUID, payload: ClubMemberAdd, user: CurrentUser, session: SessionDep
) -> ClubMemberRead:
    """Add a member; owners/admins only."""
    _require_manager(await club_repo.club_role(session, club_id, user.id))
    if await club_repo.club_role(session, club_id, payload.user_id) is not None:
        raise ApiError(409, "Conflict", "User is already a member.")
    target = await session.execute(select(User).where(club_repo.User.id == payload.user_id))
    if target.scalar_one_or_none() is None:
        raise ApiError(404, "Not found", "User does not exist.")
    member = await club_repo.add_member(session, club_id, payload.user_id, payload.role)
    return ClubMemberRead(
        club_id=member.club_id, user_id=member.user_id, role=member.role, joined_at=member.joined_at
    )


@router.delete("/{club_id}/members/{user_id}", status_code=204)
async def remove_member(
    club_id: uuid.UUID, user_id: uuid.UUID, user: CurrentUser, session: SessionDep
) -> None:
    """Remove a member; owners/admins only."""
    _require_manager(await club_repo.club_role(session, club_id, user.id))
    if not await club_repo.remove_member(session, club_id, user_id):
        raise ApiError(404, "Not found", "Membership does not exist.")


@router.post("/{club_id}/invitations", response_model=ClubInvitationRead, status_code=201)
async def create_invitation(
    club_id: uuid.UUID, payload: ClubInvitationCreate, user: CurrentUser, session: SessionDep
) -> ClubInvitationRead:
    """Create a club invitation code; owners/admins only."""
    _require_manager(await club_repo.club_role(session, club_id, user.id))
    invitation = await club_repo.create_invitation(
        session,
        club_id=club_id,
        email=payload.email,
        role=payload.role,
        expires_in_days=payload.expires_in_days,
        created_by=user.id,
    )
    return ClubInvitationRead(
        id=invitation.id,
        club_id=invitation.club_id,
        code=invitation.code,
        role=invitation.role or ClubRole.member,
        expires_at=invitation.expires_at,
        accepted_by=invitation.accepted_by,
    )
