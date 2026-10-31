"""Redeem club invitations (H2.3, §8 Davetiye)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import ApiError
from app.repos import club_repo
from app.repos.auth import User
from app.schemas.club import ClubMemberRead

router = APIRouter(tags=["clubs"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/invitations/{code}/redeem", response_model=ClubMemberRead)
async def redeem(code: str, user: CurrentUser, session: SessionDep) -> ClubMemberRead:
    """Redeem a club invitation and create the membership."""
    invitation = await club_repo.get_invitation(session, code)
    if invitation is None:
        raise ApiError(404, "Not found", "Invitation does not exist.")
    try:
        member = await club_repo.redeem_invitation(session, invitation, user)
    except ValueError as exc:
        raise ApiError(409, "Conflict", str(exc)) from exc
    return ClubMemberRead(
        club_id=member.club_id, user_id=member.user_id, role=member.role, joined_at=member.joined_at
    )
