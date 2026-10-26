"""Device registration endpoints (§8 Cihaz, H2.19)."""

from __future__ import annotations

import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db import get_session
from app.core.errors import ApiError
from app.repos.auth import Device, User
from app.schemas.device import DeviceCreate, DeviceRead

router = APIRouter(prefix="/devices", tags=["devices"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("", response_model=DeviceRead, status_code=201)
async def register_device(
    payload: DeviceCreate, user: CurrentUser, session: SessionDep
) -> DeviceRead:
    """Register a device; no push token is stored (§4.8)."""
    device = Device(
        id=uuid.uuid4(),
        user_id=user.id,
        platform=payload.platform,
        app_version=payload.app_version,
        last_seen=datetime.datetime.now(datetime.UTC),
    )
    session.add(device)
    await session.commit()
    return DeviceRead.model_validate(device)


@router.delete("/{device_id}", status_code=204)
async def unregister_device(device_id: uuid.UUID, user: CurrentUser, session: SessionDep) -> None:
    """Remove a device owned by the caller."""
    result = await session.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if device is None:
        raise ApiError(404, "Not found", "Device does not exist.")
    if device.user_id != user.id:
        raise ApiError(403, "Forbidden", "Not your device.")
    await session.delete(device)
    await session.commit()
