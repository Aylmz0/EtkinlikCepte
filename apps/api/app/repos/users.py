"""User and refresh-token persistence (H2.1/H2.2)."""

from __future__ import annotations

import datetime
import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.repos.auth import RefreshToken, User

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class UserRepository:
    """Small repository around the users and refresh_tokens tables."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """Find a user by e-mail."""
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Find a user by id."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, *, email: str, password_hash: str, display_name: str) -> User:
        """Insert a user with default profile fields."""
        user = User(
            id=uuid.uuid4(),
            email=email,
            password_hash=password_hash,
            display_name=display_name,
            created_at=datetime.datetime.now(datetime.UTC),
            locale="tr",
            budget_currency="TRY",
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def update_profile(self, user: User, changes: dict[str, object]) -> User:
        """Apply a partial profile update and flush."""
        for key, value in changes.items():
            setattr(user, key, value)
        await self.session.flush()
        return user

    async def add_refresh_token(
        self,
        *,
        user_id: uuid.UUID,
        token_hash: str,
        expires_at: datetime.datetime,
        device_id: str | None,
    ) -> RefreshToken:
        """Store a hashed refresh token."""
        record = RefreshToken(
            id=uuid.uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            device_id=device_id,
        )
        self.session.add(record)
        await self.session.flush()
        return record

    async def get_refresh_token(self, token_hash: str) -> RefreshToken | None:
        """Find a refresh token by its hash."""
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none()

    async def revoke_refresh_token(self, record: RefreshToken) -> None:
        """Mark a refresh token revoked."""
        record.revoked_at = datetime.datetime.now(datetime.UTC)
        await self.session.flush()

    async def commit(self) -> None:
        """Commit the current unit of work."""
        await self.session.commit()


def get_user_repo(session: SessionDep) -> UserRepository:
    """FastAPI dependency returning a repository bound to the request session."""
    return UserRepository(session)
