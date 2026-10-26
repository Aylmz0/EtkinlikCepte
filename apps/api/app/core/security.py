"""Password hashing and JWT helpers for H2.1 (§8.1)."""

from __future__ import annotations

import datetime
import hashlib
import secrets
import uuid

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

from app.core.config import settings
from app.core.errors import ApiError

_hasher = PasswordHasher()
_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hash a plaintext password with argon2id."""
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Return whether a plaintext password matches a stored argon2 hash."""
    try:
        return _hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError):
        return False


def create_access_token(user_id: uuid.UUID) -> str:
    """Issue a short-lived access JWT.

    Args:
        user_id: User identifier stored in ``sub``.

    Returns:
        Signed HS256 JWT.
    """
    now = datetime.datetime.now(datetime.UTC)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + datetime.timedelta(minutes=settings.access_token_ttl_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=_ALGORITHM)


def decode_access_token(token: str) -> uuid.UUID:
    """Decode an access JWT and return its user id.

    Raises:
        ApiError: 401 when the token is missing, expired or malformed.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[_ALGORITHM])
        if payload.get("type") != "access":
            raise ValueError("wrong token type")
        return uuid.UUID(str(payload["sub"]))
    except (jwt.PyJWTError, KeyError, ValueError) as exc:
        raise ApiError(401, "Unauthorized", "Invalid or expired access token.") from exc


def new_refresh_token() -> tuple[str, str]:
    """Return a raw refresh token and its SHA-256 hash."""
    raw = secrets.token_urlsafe(48)
    return raw, hash_refresh_token(raw)


def hash_refresh_token(raw: str) -> str:
    """Hash a refresh token before storing it."""
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def access_token_ttl_seconds() -> int:
    """Return the access-token lifetime in seconds for the API response."""
    return settings.access_token_ttl_minutes * 60
