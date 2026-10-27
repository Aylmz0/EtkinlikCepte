"""Process-wide settings, read once from the environment.

Plain os.environ instead of pydantic-settings: one fewer dependency for
twelve string values (AGENTS.md: boring technology, KISS).
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env(name: str, default: str) -> str:
    """Return the environment value or default when unset or blank."""
    value = os.environ.get(name, "").strip()
    return value or default


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for the API process."""

    app_name: str = "EtkinlikCepte API"
    app_version: str = "0.1.0"
    api_prefix: str = "/v1"
    database_url: str = "postgresql://projectx:projectx@localhost:5432/projectx"
    valkey_url: str = "redis://localhost:6379/0"
    log_level: str = "INFO"
    jwt_secret: str = "dev-only-change-me-use-32-bytes-minimum"
    access_token_ttl_minutes: int = 15
    refresh_token_ttl_days: int = 30
    livekit_url: str = "ws://localhost:7880"
    livekit_api_key: str = "devkey"
    livekit_api_secret: str = "secret"
    web_dir: str = ""


def load_settings() -> Settings:
    """Build Settings from the environment.

    Returns:
        Settings populated from APP_* / DATABASE_URL / VALKEY_URL variables.
    """
    return Settings(
        app_name=_env("APP_NAME", Settings.app_name),
        app_version=_env("APP_VERSION", Settings.app_version),
        api_prefix=_env("API_PREFIX", Settings.api_prefix),
        database_url=_env("DATABASE_URL", Settings.database_url),
        valkey_url=_env("VALKEY_URL", Settings.valkey_url),
        log_level=_env("LOG_LEVEL", Settings.log_level),
        jwt_secret=_env("JWT_SECRET", Settings.jwt_secret),
        access_token_ttl_minutes=int(_env("ACCESS_TOKEN_TTL_MINUTES", "15")),
        refresh_token_ttl_days=int(_env("REFRESH_TOKEN_TTL_DAYS", "30")),
        livekit_url=_env("LIVEKIT_URL", Settings.livekit_url),
        livekit_api_key=_env("LIVEKIT_KEY", Settings.livekit_api_key),
        livekit_api_secret=_env("LIVEKIT_SECRET", Settings.livekit_api_secret),
        web_dir=_env("WEB_DIR", Settings.web_dir),
    )


settings = load_settings()
