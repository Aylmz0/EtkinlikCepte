"""Auth and profile endpoints (§8 Kimlik, H2.1/H2.2)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header

from app.core.auth import get_current_user
from app.repos.auth import User
from app.repos.users import UserRepository, get_user_repo
from app.schemas.auth import (
    AuthResponse,
    LoginIn,
    ProfileUpdate,
    RefreshIn,
    RegisterIn,
    TokenPair,
    UserRead,
)
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

Repo = Annotated[UserRepository, Depends(get_user_repo)]
CurrentUser = Annotated[User, Depends(get_current_user)]
DeviceId = Annotated[str | None, Header(alias="X-Device-Id")]


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(payload: RegisterIn, repo: Repo, device_id: DeviceId = None) -> AuthResponse:
    """Create a user and return an access/refresh token pair."""
    return await auth_service.register_user(
        repo,
        email=str(payload.email),
        password=payload.password,
        display_name=payload.display_name,
        device_id=device_id,
    )


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginIn, repo: Repo, device_id: DeviceId = None) -> AuthResponse:
    """Authenticate and return an access/refresh token pair."""
    return await auth_service.login_user(
        repo, email=str(payload.email), password=payload.password, device_id=device_id
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshIn, repo: Repo, device_id: DeviceId = None) -> TokenPair:
    """Rotate the refresh token and return a new pair."""
    return await auth_service.refresh_tokens(
        repo, raw_refresh=payload.refresh_token, device_id=device_id
    )


@router.post("/logout")
async def logout(payload: RefreshIn, repo: Repo) -> dict[str, str]:
    """Revoke the refresh token; safe to call twice."""
    await auth_service.logout_user(repo, raw_refresh=payload.refresh_token)
    return {"status": "ok"}


@router.get("/me", response_model=UserRead)
async def me(user: CurrentUser) -> UserRead:
    """Return the authenticated user's full profile."""
    return UserRead.model_validate(user)


@router.patch("/me", response_model=UserRead)
async def update_me(payload: ProfileUpdate, user: CurrentUser, repo: Repo) -> UserRead:
    """Update profile fields: name, bio, city, interests, locale, budget."""
    return await auth_service.update_profile(repo, user=user, payload=payload)
