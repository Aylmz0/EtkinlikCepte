"""Write clean source events, events and their links (H3.1)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import psycopg
from psycopg.types.json import Jsonb

from pipeline.normalize import CleanEvent

SOURCE_EVENT_SQL = """
INSERT INTO source_events
    (id, source, source_ref, title_raw, venue_geom, starts_at, ends_at, price_minor,
     currency, url, payload, fetched_at, content_hash)
VALUES
    (%(id)s, %(source)s, %(source_ref)s, %(title_raw)s,
     CASE WHEN %(lat)s::float8 IS NULL OR %(lon)s::float8 IS NULL THEN NULL
          ELSE ST_SetSRID(ST_MakePoint(%(lon)s::float8, %(lat)s::float8), 4326) END,
     %(starts_at)s, %(ends_at)s, %(price_minor)s, %(currency)s,
     %(url)s, %(payload)s, %(fetched_at)s, %(content_hash)s)
ON CONFLICT (source, source_ref) DO UPDATE
SET title_raw = EXCLUDED.title_raw,
    venue_geom = EXCLUDED.venue_geom,
    starts_at = EXCLUDED.starts_at,
    ends_at = EXCLUDED.ends_at,
    price_minor = EXCLUDED.price_minor,
    currency = EXCLUDED.currency,
    url = EXCLUDED.url,
    payload = EXCLUDED.payload,
    fetched_at = EXCLUDED.fetched_at,
    content_hash = EXCLUDED.content_hash
RETURNING id
"""

FIND_EVENT_SQL = "SELECT event_id FROM event_sources WHERE source_event_id = ANY(%s) LIMIT 1"

INSERT_EVENT_SQL = """
INSERT INTO events
    (id, title, starts_at, ends_at, is_online, origin, trust, status, created_at)
VALUES
    (%(id)s, %(title)s, %(starts_at)s, %(ends_at)s, false,
     'collected', 'collected', 'published', %(created_at)s)
"""

UPDATE_EVENT_SQL = "UPDATE events SET title = %s, starts_at = %s, ends_at = %s WHERE id = %s"

LINK_SQL = """
INSERT INTO event_sources (event_id, source_event_id, is_primary)
VALUES (%s, %s, %s)
ON CONFLICT (event_id, source_event_id) DO UPDATE SET is_primary = EXCLUDED.is_primary
"""


def write_clean_events(
    dsn: str, groups: list[list[CleanEvent]]
) -> tuple[int, int]:
    """Upsert source rows, then one ``events`` row per duplicate group.

    Re-running with the same input updates rows instead of duplicating them:
    source rows are keyed by (source, source_ref), and a group that is already
    linked to an event reuses that event.

    Returns:
        (source_events written, events written or updated).
    """
    source_count = 0
    event_count = 0
    now = datetime.now(UTC)
    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        for group in groups:
            members = sorted(group, key=lambda e: (e.source, e.source_ref))
            ids: list[uuid.UUID] = []
            for event in members:
                row = event.as_source_event_row()
                row["payload"] = Jsonb(row["payload"])
                row["lat"], row["lon"] = event.lat, event.lon
                cur.execute(SOURCE_EVENT_SQL, row)
                ids.append(cur.fetchone()[0])
                source_count += 1

            primary = members[0]
            cur.execute(FIND_EVENT_SQL, (ids,))
            found = cur.fetchone()
            if found:
                event_id = found[0]
                cur.execute(
                    UPDATE_EVENT_SQL,
                    (primary.title, primary.starts_at, primary.ends_at, event_id),
                )
            else:
                event_id = uuid.uuid4()
                cur.execute(
                    INSERT_EVENT_SQL,
                    {
                        "id": event_id,
                        "title": primary.title,
                        "starts_at": primary.starts_at,
                        "ends_at": primary.ends_at,
                        "created_at": now,
                    },
                )
            for index, source_event_id in enumerate(ids):
                cur.execute(LINK_SQL, (event_id, source_event_id, index == 0))
            event_count += 1
        conn.commit()
    return source_count, event_count
