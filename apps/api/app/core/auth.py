"""FastAPI authentication dependency (H2.1)."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.errors import ApiError
from app.core.security import decode_access_token
from app.repos.auth import User
from app.repos.users import UserRepository, get_user_repo

_bearer = HTTPBearer(auto_error=False)


async def get_optional_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> User | None:
    """Resolve a Bearer token when present; anonymous requests return None."""
    if credentials is None:
        return None
    try:
        user_id: uuid.UUID = decode_access_token(credentials.credentials)
    except ApiError:
        return None
    return await repo.get_by_id(user_id)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> User:
    """Resolve the Bearer access token to a user.

    Raises:
        ApiError: 401 when the header is missing/invalid or the user is gone.
    """
    if credentials is None:
        raise ApiError(401, "Unauthorized", "Missing Authorization header.")
    user_id: uuid.UUID = decode_access_token(credentials.credentials)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise ApiError(401, "Unauthorized", "User no longer exists.")
    return user
