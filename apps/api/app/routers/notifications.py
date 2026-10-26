"""Notification list/read endpoints (§8 Bildirim, H2.19)."""

from __future__ import annotations

import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import ApiError
from app.repos.auth import User
from app.repos.content import Notification
from app.schemas.notification import NotificationRead

router = APIRouter(prefix="/notifications", tags=["notifications"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("", response_model=list[NotificationRead])
async def list_notifications(
    user: CurrentUser,
    session: SessionDep,
    limit: int = Query(default=50, ge=1, le=100),
) -> list[NotificationRead]:
    """Return the caller's notifications, newest first."""
    result = await session.execute(
        select(Notification)
        .where(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
    )
    return [NotificationRead.model_validate(row) for row in result.scalars()]


@router.post("/{notification_id}/read", response_model=NotificationRead)
async def mark_read(
    notification_id: uuid.UUID, user: CurrentUser, session: SessionDep
) -> NotificationRead:
    """Mark one notification read."""
    result = await session.execute(select(Notification).where(Notification.id == notification_id))
    notification = result.scalar_one_or_none()
    if notification is None:
        raise ApiError(404, "Not found", "Notification does not exist.")
    if notification.user_id != user.id:
        raise ApiError(403, "Forbidden", "Not your notification.")
    notification.read_at = datetime.datetime.now(datetime.UTC)
    await session.commit()
    return NotificationRead.model_validate(notification)
