"""Live Postgres smoke test for discovery SQL (run with RUN_DB_TESTS=1)."""

from __future__ import annotations

import os

import httpx
import pytest
from app.main import app

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1", reason="requires migrated Postgres"
)


@pytest.mark.asyncio
async def test_discovery_endpoints_run_against_postgis() -> None:
    """The venue/event/recommendation queries are valid PostGIS SQL."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        venues = await client.get("/v1/discover/venues", params={"bbox": "32.7,39.8,33.0,40.0"})
        assert venues.status_code == 200, venues.text
        assert venues.json()["count"] >= 0

        events = await client.get(
            "/v1/discover/events", params={"lat": 39.9, "lng": 32.8, "radius": 10000}
        )
        assert events.status_code == 200, events.text
        assert events.json()["count"] >= 0

        recs = await client.get(
            "/v1/discover/recommendations", params={"lat": 39.9, "lng": 32.8, "limit": 5}
        )
        assert recs.status_code == 200, recs.text
        assert recs.json()["candidate_count"] >= 0
