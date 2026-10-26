"""LiveKit room token endpoints (H2.18)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from livekit import api
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.config import settings
from app.core.db import get_session
from app.core.errors import ApiError
from app.repos.auth import User
from app.repos.chat import ChatMember
from app.repos.event_repo import get_event
from app.schemas.room import RoomToken

router = APIRouter(tags=["rooms"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def _token(user: User, room: str) -> RoomToken:
    token = api.AccessToken(settings.livekit_api_key, settings.livekit_api_secret)
    token.with_identity(str(user.id)).with_name(user.display_name).with_grants(
        api.VideoGrants(room_join=True, room=room)
    )
    return RoomToken(url=settings.livekit_url, token=token.to_jwt(), room=room)


@router.get("/events/{event_id}/room/token", response_model=RoomToken)
async def event_room_token(
    event_id: uuid.UUID, user: CurrentUser, session: SessionDep
) -> RoomToken:
    """Issue a LiveKit token for an event room."""
    event = await get_event(session, event_id)
    if event is None:
        raise ApiError(404, "Not found", "Event does not exist.")
    return _token(user, f"event-{event_id}")


@router.post("/channels/{channel_id}/room/token", response_model=RoomToken)
async def channel_room_token(
    channel_id: uuid.UUID, user: CurrentUser, session: SessionDep
) -> RoomToken:
    """Issue a LiveKit token for a club/DM channel room."""
    member = await session.execute(
        select(ChatMember).where(ChatMember.channel_id == channel_id, ChatMember.user_id == user.id)
    )
    if member.scalar_one_or_none() is None:
        raise ApiError(403, "Forbidden", "Not a channel member.")
    return _token(user, f"channel-{channel_id}")
