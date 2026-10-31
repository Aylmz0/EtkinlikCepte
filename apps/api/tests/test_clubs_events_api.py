"""H2.3/H2.4/H2.5 live flow: club -> event -> free ticket -> QR -> check-in."""

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


async def _register(client: httpx.AsyncClient) -> dict:
    email = f"club-{uuid.uuid4()}@example.com"
    response = await client.post(
        "/v1/auth/register",
        json={"email": email, "password": "correct-horse-battery", "display_name": "Test"},
    )
    assert response.status_code == 201, response.text
    return response.json()


async def _headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_club_event_ticket_flow() -> None:
    """The complete H2.3-H2.5 happy path works against the real schema."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        owner = await _register(client)
        member = await _register(client)
        owner_headers = await _headers(owner["access_token"])
        member_headers = await _headers(member["access_token"])

        club = await client.post(
            "/v1/clubs",
            headers=owner_headers,
            json={
                "name": "Kampüs Kulübü",
                "slug": f"kampus-{uuid.uuid4().hex[:8]}",
                "city": "Ankara",
            },
        )
        assert club.status_code == 201, club.text
        club_id = club.json()["id"]

        added = await client.post(
            f"/v1/clubs/{club_id}/members",
            headers=owner_headers,
            json={"user_id": member["user"]["id"], "role": "member"},
        )
        assert added.status_code == 200, added.text

        forbidden = await client.patch(
            f"/v1/clubs/{club_id}", headers=member_headers, json={"city": "İzmir"}
        )
        assert forbidden.status_code == 403

        starts_at = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=2)).isoformat()
        event = await client.post(
            "/v1/events",
            headers=owner_headers,
            json={"club_id": club_id, "title": "Kampüs Konseri", "starts_at": starts_at},
        )
        assert event.status_code == 201, event.text
        event_id = event.json()["id"]

        ticket = await client.post(
            f"/v1/events/{event_id}/tickets",
            headers=owner_headers,
            json={"name": "Ücretsiz", "price_minor": 0, "quantity": 2},
        )
        assert ticket.status_code == 201, ticket.text
        ticket_id = ticket.json()["id"]

        published = await client.post(f"/v1/events/{event_id}/publish", headers=owner_headers)
        assert published.status_code == 200, published.text

        first = await client.post(
            f"/v1/events/{event_id}/register",
            headers=member_headers,
            json={"ticket_id": ticket_id, "quantity": 1},
        )
        assert first.status_code == 200, first.text
        registration_id = first.json()["id"]
        assert first.json()["status"] == "free_granted"

        qr = await client.get(f"/v1/registrations/{registration_id}/qr", headers=member_headers)
        assert qr.status_code == 200
        assert qr.headers["content-type"].startswith("image/svg+xml")

        second = await _register(client)
        second_headers = await _headers(second["access_token"])
        filled = await client.post(
            f"/v1/events/{event_id}/register",
            headers=second_headers,
            json={"ticket_id": ticket_id, "quantity": 1},
        )
        assert filled.status_code == 200, filled.text

        third = await _register(client)
        third_headers = await _headers(third["access_token"])
        overflow = await client.post(
            f"/v1/events/{event_id}/register",
            headers=third_headers,
            json={"ticket_id": ticket_id, "quantity": 1},
        )
        assert overflow.status_code == 400

        checked = await client.post(
            f"/v1/registrations/{registration_id}/checkin", headers=owner_headers
        )
        assert checked.status_code == 200, checked.text
