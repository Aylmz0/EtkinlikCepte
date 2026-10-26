"""H2.8 DB writer test; skipped unless RUN_DB_TESTS=1."""

from __future__ import annotations

import os
import uuid

import pytest
from pipeline.repos.source_events import write_source_events

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1", reason="requires migrated Postgres"
)


def test_write_source_events_is_idempotent() -> None:
    """The same (source, source_ref) upserts instead of duplicating."""
    dsn = os.environ.get("DATABASE_URL", "postgresql://projectx:projectx@localhost:5432/projectx")
    ref = f"https://example.com/{uuid.uuid4()}"
    row = {
        "source": "fixture",
        "source_ref": ref,
        "content_hash": "a" * 64,
        "payload": {"title": "Fixture", "source_ref": ref},
    }
    assert write_source_events(dsn, [row]) == 1
    assert write_source_events(dsn, [row]) == 1
    with __import__("psycopg").connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT count(*) FROM source_events WHERE source = 'fixture' AND source_ref = %s",
            (ref,),
        )
        assert cur.fetchone()[0] == 1
