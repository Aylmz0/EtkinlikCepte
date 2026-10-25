"""Authentication and profile services (H2.1/H2.2)."""

from __future__ import annotations

import datetime
import uuid

from app.core import security
from app.core.config import settings
from app.core.errors import ApiError
from app.repos.users import UserRepository
from app.schemas.auth import AuthResponse, ProfileUpdate, TokenPair, UserRead


async def _issue_tokens(
    repo: UserRepository, user_id: uuid.UUID, device_id: str | None
) -> TokenPair:
    """Create an access JWT and store a new refresh token."""
    raw_refresh, refresh_hash = security.new_refresh_token()
    await repo.add_refresh_token(
        user_id=user_id,
        token_hash=refresh_hash,
        expires_at=datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(days=settings.refresh_token_ttl_days),
        device_id=device_id,
    )
    return TokenPair(
        access_token=security.create_access_token(user_id),
        refresh_token=raw_refresh,
        expires_in=security.access_token_ttl_seconds(),
    )


async def register_user(
    repo: UserRepository, *, email: str, password: str, display_name: str, device_id: str | None
) -> AuthResponse:
    """Register a user and return a token pair.

    Raises:
        ApiError: 409 when the e-mail is already registered.
    """
    if await repo.get_by_email(email) is not None:
        raise ApiError(409, "Conflict", "This e-mail is already registered.")
    user = await repo.create_user(
        email=email,
        password_hash=security.hash_password(password),
        display_name=display_name,
    )
    tokens = await _issue_tokens(repo, user.id, device_id)
    await repo.commit()
    return AuthResponse(**tokens.model_dump(), user=UserRead.model_validate(user))


async def login_user(
    repo: UserRepository, *, email: str, password: str, device_id: str | None
) -> AuthResponse:
    """Authenticate a user and return a token pair.

    Raises:
        ApiError: 401 for an unknown e-mail or wrong password.
    """
    user = await repo.get_by_email(email)
    if user is None or not security.verify_password(password, user.password_hash):
        raise ApiError(401, "Unauthorized", "E-mail or password is incorrect.")
    tokens = await _issue_tokens(repo, user.id, device_id)
    await repo.commit()
    return AuthResponse(**tokens.model_dump(), user=UserRead.model_validate(user))


async def refresh_tokens(
    repo: UserRepository, *, raw_refresh: str, device_id: str | None
) -> TokenPair:
    """Rotate a refresh token: revoke the old one and issue a new pair.

    Raises:
        ApiError: 401 when the token is unknown, revoked or expired.
    """
    record = await repo.get_refresh_token(security.hash_refresh_token(raw_refresh))
    if (
        record is None
        or record.revoked_at is not None
        or record.expires_at <= datetime.datetime.now(datetime.UTC)
    ):
        raise ApiError(401, "Unauthorized", "Refresh token is invalid or expired.")
    await repo.revoke_refresh_token(record)
    tokens = await _issue_tokens(repo, record.user_id, device_id or record.device_id)
    await repo.commit()
    return tokens


async def logout_user(repo: UserRepository, *, raw_refresh: str) -> None:
    """Revoke a refresh token; unknown tokens are a no-op (idempotent logout)."""
    record = await repo.get_refresh_token(security.hash_refresh_token(raw_refresh))
    if record is not None and record.revoked_at is None:
        await repo.revoke_refresh_token(record)
    await repo.commit()


async def update_profile(repo: UserRepository, *, user: object, payload: ProfileUpdate) -> UserRead:
    """Apply a partial profile update and return the public profile."""
    changes = payload.model_dump(exclude_unset=True)
    updated = await repo.update_profile(user, changes)  # type: ignore[arg-type]
    await repo.commit()
    return UserRead.model_validate(updated)
