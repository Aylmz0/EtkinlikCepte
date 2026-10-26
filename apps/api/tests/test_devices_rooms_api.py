"""H2.18/H2.19 live smoke: device, notifications and LiveKit event token."""

from __future__ import annotations

import datetime
import os
import uuid

import httpx
import pytest
from app.main import app

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1", reason="requires migrated Postgres"
)


@pytest.mark.asyncio
async def test_device_notifications_and_room_token() -> None:
    """Device registration, notification list and room token are wired."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        email = f"p5-{uuid.uuid4()}@example.com"
        reg = await client.post(
            "/v1/auth/register",
            json={"email": email, "password": "correct-horse-battery", "display_name": "P5"},
        )
        assert reg.status_code == 201, reg.text
        token = reg.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        device = await client.post(
            "/v1/devices", headers=headers, json={"platform": "android", "app_version": "0.1.0"}
        )
        assert device.status_code == 201, device.text

        notes = await client.get("/v1/notifications", headers=headers)
        assert notes.status_code == 200
        assert notes.json() == []

        slug = f"p5-{uuid.uuid4().hex[:8]}"
        club = await client.post(
            "/v1/clubs", headers=headers, json={"name": "P5 Kulüp", "slug": slug}
        )
        assert club.status_code == 201, club.text
        starts_at = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)).isoformat()
        event = await client.post(
            "/v1/events",
            headers=headers,
            json={"club_id": club.json()["id"], "title": "P5 Etkinlik", "starts_at": starts_at},
        )
        assert event.status_code == 201, event.text

        room = await client.get(f"/v1/events/{event.json()['id']}/room/token", headers=headers)
        assert room.status_code == 200, room.text
        assert room.json()["room"].startswith("event-")
        assert room.json()["token"]
