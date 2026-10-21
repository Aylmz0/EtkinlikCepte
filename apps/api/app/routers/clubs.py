"""Club endpoints: H1.8 contract draft, implemented in H2.3 (§8 Kulüp)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.club import ClubCreate, ClubList, ClubMemberRead, ClubRead

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.get("", response_model=ClubList)
def list_clubs(
    cursor: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
) -> ClubList:
    """List clubs (empty until the H2.3 repo query lands)."""
    return ClubList(items=[], next_cursor=None)


@router.post("", response_model=ClubRead, status_code=status.HTTP_201_CREATED)
def create_club(payload: ClubCreate) -> ClubRead:
    """Create a club (H2.3)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="H2.3")


@router.get("/{club_id}", response_model=ClubRead)
def get_club(club_id: uuid.UUID) -> ClubRead:
    """Read one club (H2.3)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="H2.3")


@router.post(
    "/{club_id}/members",
    response_model=ClubMemberRead,
    status_code=status.HTTP_200_OK,
)
def join_club(club_id: uuid.UUID, user_id: uuid.UUID) -> ClubMemberRead:
    """Add a member (H2.3)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="H2.3")
