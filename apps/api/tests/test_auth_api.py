"""H2.1/H2.2 end-to-end auth flow against a live migrated Postgres.

Skipped by default; run with `RUN_DB_TESTS=1` after `just migrate`.
"""

from __future__ import annotations

import os
import uuid

import httpx
import pytest
from app.main import app

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1", reason="requires migrated Postgres"
)


@pytest.mark.asyncio
async def test_register_login_profile_refresh_logout() -> None:
    """The full H2.1 flow and the H2.2 profile round-trip work together."""
    email = f"auth-{uuid.uuid4()}@example.com"
    password = "correct-horse-battery"
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        registered = await client.post(
            "/v1/auth/register",
            json={"email": email, "password": password, "display_name": "Test Kullanıcı"},
        )
        assert registered.status_code == 201, registered.text
        tokens = registered.json()
        assert tokens["user"]["email"] == email
        access = tokens["access_token"]
        refresh = tokens["refresh_token"]

        me = await client.get("/v1/auth/me", headers={"Authorization": f"Bearer {access}"})
        assert me.status_code == 200
        assert me.json()["display_name"] == "Test Kullanıcı"

        updated = await client.patch(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {access}"},
            json={"bio": "Kampüs", "city": "Ankara", "interests": ["müzik"]},
        )
        assert updated.status_code == 200
        assert updated.json()["city"] == "Ankara"
        assert updated.json()["interests"] == ["müzik"]

        logged_in = await client.post("/v1/auth/login", json={"email": email, "password": password})
        assert logged_in.status_code == 200

        rotated = await client.post("/v1/auth/refresh", json={"refresh_token": refresh})
        assert rotated.status_code == 200
        assert rotated.json()["refresh_token"] != refresh

        old_again = await client.post("/v1/auth/refresh", json={"refresh_token": refresh})
        assert old_again.status_code == 401

        out = await client.post(
            "/v1/auth/logout", json={"refresh_token": rotated.json()["refresh_token"]}
        )
        assert out.status_code == 200
