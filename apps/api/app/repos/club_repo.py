"""Club, membership and invitation persistence (H2.3)."""

from __future__ import annotations

import datetime
import secrets
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repos.auth import User
from app.repos.clubs import Club, ClubInvitation, ClubMember, ClubRole


async def list_clubs(session: AsyncSession, limit: int = 50) -> list[Club]:
    """List clubs newest first."""
    result = await session.execute(select(Club).order_by(Club.created_at.desc()).limit(limit))
    return list(result.scalars())


async def get_club(session: AsyncSession, club_id: uuid.UUID) -> Club | None:
    """Read one club by id."""
    result = await session.execute(select(Club).where(Club.id == club_id))
    return result.scalar_one_or_none()


async def create_club(
    session: AsyncSession,
    *,
    name: str,
    slug: str,
    description: str | None,
    city: str | None,
    owner: User,
) -> Club:
    """Create a club and its owner membership in one transaction."""
    now = datetime.datetime.now(datetime.UTC)
    club = Club(
        id=uuid.uuid4(),
        name=name,
        slug=slug,
        description=description,
        city=city,
        owner_id=owner.id,
        created_at=now,
    )
    session.add(club)
    session.add(ClubMember(club_id=club.id, user_id=owner.id, role=ClubRole.owner, joined_at=now))
    await session.commit()
    return club


async def update_club(session: AsyncSession, club: Club, changes: dict[str, object]) -> Club:
    """Apply a partial club update."""
    for key, value in changes.items():
        setattr(club, key, value)
    await session.commit()
    return club


async def club_role(
    session: AsyncSession, club_id: uuid.UUID, user_id: uuid.UUID
) -> ClubRole | None:
    """Return the user's role in a club, or None."""
    result = await session.execute(
        select(ClubMember.role).where(ClubMember.club_id == club_id, ClubMember.user_id == user_id)
    )
    role = result.scalar_one_or_none()
    return ClubRole(role) if role is not None else None


async def add_member(
    session: AsyncSession, club_id: uuid.UUID, user_id: uuid.UUID, role: ClubRole
) -> ClubMember:
    """Add a member; duplicate membership is a conflict handled by the router."""
    member = ClubMember(
        club_id=club_id,
        user_id=user_id,
        role=role,
        joined_at=datetime.datetime.now(datetime.UTC),
    )
    session.add(member)
    await session.commit()
    return member


async def remove_member(session: AsyncSession, club_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """Remove a membership; returns False when it did not exist."""
    result = await session.execute(
        select(ClubMember).where(ClubMember.club_id == club_id, ClubMember.user_id == user_id)
    )
    member = result.scalar_one_or_none()
    if member is None:
        return False
    await session.delete(member)
    await session.commit()
    return True


async def create_invitation(
    session: AsyncSession,
    *,
    club_id: uuid.UUID,
    email: str | None,
    role: ClubRole,
    expires_in_days: int,
    created_by: uuid.UUID,
) -> ClubInvitation:
    """Create a unique invitation code."""
    invitation = ClubInvitation(
        id=uuid.uuid4(),
        club_id=club_id,
        email=email,
        code=secrets.token_urlsafe(8),
        role=role,
        expires_at=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=expires_in_days),
        created_by=created_by,
    )
    session.add(invitation)
    await session.commit()
    return invitation


async def get_invitation(session: AsyncSession, code: str) -> ClubInvitation | None:
    """Find an invitation by code."""
    result = await session.execute(select(ClubInvitation).where(ClubInvitation.code == code))
    return result.scalar_one_or_none()


async def redeem_invitation(
    session: AsyncSession, invitation: ClubInvitation, user: User
) -> ClubMember:
    """Accept an invitation and create the membership."""
    now = datetime.datetime.now(datetime.UTC)
    if invitation.expires_at is not None and invitation.expires_at < now:
        raise ValueError("expired")
    if invitation.accepted_by is not None:
        raise ValueError("already accepted")
    invitation.accepted_by = user.id
    member = ClubMember(
        club_id=invitation.club_id,
        user_id=user.id,
        role=invitation.role or ClubRole.member,
        joined_at=now,
    )
    session.add(member)
    await session.commit()
    return member
