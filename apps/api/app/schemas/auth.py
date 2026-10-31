"""Auth and profile schemas (§8 Kimlik, H2.1/H2.2)."""

from __future__ import annotations

import datetime
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterIn(BaseModel):
    """Registration payload; the e-mail is the login identity."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=2, max_length=80)


class LoginIn(BaseModel):
    """Login payload."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RefreshIn(BaseModel):
    """Refresh/logout payload carrying the opaque refresh token."""

    refresh_token: str = Field(min_length=20, max_length=200)


class UserRead(BaseModel):
    """Public profile returned by /auth/me."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    display_name: str
    bio: str | None = None
    city: str | None = None
    interests: list[str] | None = None
    locale: str = "tr"
    budget_minor: int | None = None
    budget_currency: str = "TRY"
    created_at: datetime.datetime


class ProfileUpdate(BaseModel):
    """Partial profile update; omitted fields stay unchanged."""

    display_name: str | None = Field(default=None, min_length=2, max_length=80)
    bio: str | None = Field(default=None, max_length=2000)
    city: str | None = Field(default=None, max_length=80)
    interests: list[str] | None = Field(default=None, max_length=20)
    locale: str | None = Field(default=None, min_length=2, max_length=8)
    budget_minor: int | None = Field(default=None, ge=0)
    budget_currency: str | None = Field(default=None, min_length=3, max_length=3)


class TokenPair(BaseModel):
    """Access + refresh token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthResponse(TokenPair):
    """Token pair plus the authenticated user."""

    user: UserRead
