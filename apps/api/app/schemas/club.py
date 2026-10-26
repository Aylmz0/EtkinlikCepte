"""Club schemas shared by the API contract (§7, §8).

These models are the H1.8 draft: the router bodies land in H2.3, but the
request/response shapes are frozen here so clients can generate types now.
"""

from __future__ import annotations

import datetime
import enum
import uuid

from pydantic import BaseModel, ConfigDict, Field


class ClubRole(enum.StrEnum):
    """Membership role inside a club."""

    owner = "owner"
    admin = "admin"
    moderator = "moderator"
    member = "member"


class ClubCreate(BaseModel):
    """Payload for creating a club; the owner comes from the access token."""

    name: str = Field(min_length=2, max_length=120)
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=64)
    description: str | None = Field(default=None, max_length=2000)
    city: str | None = Field(default=None, max_length=80)


class ClubUpdate(BaseModel):
    """Partial club update; omitted fields stay unchanged."""

    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    city: str | None = Field(default=None, max_length=80)


class ClubRead(BaseModel):
    """Club representation returned by list and detail endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    description: str | None = None
    city: str | None = None
    owner_id: uuid.UUID
    created_at: datetime.datetime


class ClubMemberRead(BaseModel):
    """A club membership row with its role."""

    club_id: uuid.UUID
    user_id: uuid.UUID
    role: ClubRole
    joined_at: datetime.datetime


class ClubList(BaseModel):
    """Cursor page of clubs; ``next_cursor`` is null on the last page."""

    items: list[ClubRead]
    next_cursor: str | None = None


class ClubMemberAdd(BaseModel):
    """Add a user to a club with an explicit role."""

    user_id: uuid.UUID
    role: ClubRole = ClubRole.member


class ClubInvitationCreate(BaseModel):
    """Create a redeemable club invitation."""

    email: str | None = Field(default=None, max_length=255)
    role: ClubRole = ClubRole.member
    expires_in_days: int = Field(default=7, ge=1, le=90)


class ClubInvitationRead(BaseModel):
    """Invitation state returned to the creator."""

    id: uuid.UUID
    club_id: uuid.UUID
    code: str
    role: ClubRole
    expires_at: datetime.datetime | None = None
    accepted_by: uuid.UUID | None = None


class InvitationRedeem(BaseModel):
    """Redeem response: the new membership."""

    club_id: uuid.UUID
    user_id: uuid.UUID
    role: ClubRole
