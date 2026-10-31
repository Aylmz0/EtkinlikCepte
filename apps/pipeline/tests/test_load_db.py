"""H3.1 load test; skipped unless RUN_DB_TESTS=1."""

from __future__ import annotations

import os
import uuid

import psycopg
import pytest

from pipeline.load import load_rows

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1", reason="requires migrated Postgres"
)


def _row(source: str, ref: str, title: str) -> dict:
    return {
        "source": source,
        "source_ref": ref,
        "content_hash": uuid.uuid4().hex * 2,
        "payload": {
            "title": title,
            "starts_at": "2026-11-12T20:00:00+03:00",
            "location": {"name": "Kültür Merkezi", "geo": {"latitude": 41.0082, "longitude": 28.9784}},
            "price": "250 TL",
        },
    }


def test_load_is_idempotent_and_dedups() -> None:
    dsn = os.environ.get("DATABASE_URL", "postgresql://projectx:projectx@localhost:5432/projectx")
    tag = uuid.uuid4().hex[:8]
    sources = [f"fx-a-{tag}", f"fx-b-{tag}"]
    rows = [
        _row(sources[0], f"https://a.example.com/{tag}", f"Sahne Gecesi {tag}"),
        _row(sources[1], f"https://b.example.com/{tag}", f"SAHNE GECESİ {tag}"),
    ]
    first = load_rows(dsn, rows)
    again = load_rows(dsn, rows)
    assert first.events == 1 and again.events == 1
    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT count(*), count(DISTINCT es.event_id) FROM event_sources es "
            "JOIN source_events se ON se.id = es.source_event_id WHERE se.source = ANY(%s)",
            (sources,),
        )
        links, distinct_events = cur.fetchone()
    assert (links, distinct_events) == (2, 1)
