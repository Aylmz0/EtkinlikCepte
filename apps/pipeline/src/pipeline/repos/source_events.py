"""Write adapter rows to ``source_events`` with change detection (H2.8)."""

from __future__ import annotations

import datetime
import uuid
from typing import Any

import psycopg
from psycopg.types.json import Jsonb

UPSERT_SQL = """
INSERT INTO source_events
    (id, source, source_ref, title_raw, starts_at, ends_at, price_minor, currency,
     url, payload, fetched_at, content_hash)
VALUES
    (%(id)s, %(source)s, %(source_ref)s, %(title_raw)s, NULL, NULL, NULL, NULL,
     %(url)s, %(payload)s, %(fetched_at)s, %(content_hash)s)
ON CONFLICT (source, source_ref) DO UPDATE
SET title_raw = EXCLUDED.title_raw,
    payload = EXCLUDED.payload,
    fetched_at = EXCLUDED.fetched_at,
    content_hash = EXCLUDED.content_hash
WHERE source_events.content_hash IS DISTINCT FROM EXCLUDED.content_hash
"""


def write_source_events(dsn: str, rows: list[dict[str, Any]]) -> int:
    """Upsert adapter rows, returning the number of SQL statements executed.

    Args:
        dsn: PostgreSQL connection string.
        rows: Output of an RSS/JSON-LD/HTML adapter.

    Returns:
        Number of rows sent to the database (including unchanged rows).
    """
    if not rows:
        return 0
    now = datetime.datetime.now(datetime.UTC)
    with psycopg.connect(dsn) as conn, conn.cursor() as cursor:
        for row in rows:
            payload = row.get("payload") or {}
            cursor.execute(
                UPSERT_SQL,
                {
                    "id": uuid.uuid4(),
                    "source": row["source"],
                    "source_ref": row["source_ref"],
                    "title_raw": payload.get("title"),
                    "url": payload.get("source_ref"),
                    "payload": Jsonb(payload),
                    "fetched_at": now,
                    "content_hash": row["content_hash"],
                },
            )
        conn.commit()
    return len(rows)
