"""Auth tables: users, refresh_tokens, devices (§7 Kullanıcı).

P1 decision (H1.3): users carries locale (default 'tr') plus an optional
budget (budget_minor INT NULL + budget_currency CHAR(3) DEFAULT 'TRY')
because the §1.5 profile tab shows language and budget.
"""

from __future__ import annotations

import datetime
import uuid

from sqlalchemy import ARRAY, CHAR, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.repos.base import Base, uuid_pk


class User(Base):
    """Application user; money follows §8.1 (integer minor units + CHAR(3))."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = uuid_pk()
    email: Mapped[str] = mapped_column(CITEXT, unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    display_name: Mapped[str] = mapped_column(Text)
    avatar_media_id: Mapped[uuid.UUID | None]
    bio: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(Text)
    interests: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    locale: Mapped[str] = mapped_column(Text, default="tr", server_default="tr")
    budget_minor: Mapped[int | None]
    budget_currency: Mapped[str] = mapped_column(CHAR(3), default="TRY", server_default="TRY")
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))


class RefreshToken(Base):
    """Hashed refresh token with revocation timestamp (§7)."""

    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID]
    token_hash: Mapped[str] = mapped_column(Text, unique=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    revoked_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    device_id: Mapped[str | None] = mapped_column(Text)


class Device(Base):
    """Online-only device record for presence and version info (§4.8)."""

    __tablename__ = "devices"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID]
    platform: Mapped[str | None] = mapped_column(Text)
    app_version: Mapped[str | None] = mapped_column(Text)
    last_seen: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
