"""Event endpoints: H1.8 contract draft, implemented in H2.4 (§8 Etkinlik)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.event import EventCreate, EventList, EventRead

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=EventList)
def list_events(
    cursor: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
) -> EventList:
    """List events (empty until the H2.4 query lands)."""
    return EventList(items=[], next_cursor=None)


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate) -> EventRead:
    """Create an event (H2.4)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="H2.4")


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: uuid.UUID) -> EventRead:
    """Read one event (H2.4)."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="H2.4")
