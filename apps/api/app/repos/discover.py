"""PostGIS discovery query prototype (H1.10, implemented fully in H2.6).

The query keeps distance in metres and filters with ``ST_DWithin`` so the
GIST index on ``venues.geom`` can be used before sorting.
"""

from __future__ import annotations

from sqlalchemy import text


def nearby_events_sql() -> str:
    """Return the prototype SQL for nearby published events.

    Returns:
        SQL text with ``:lat``, ``:lng``, ``:radius_m`` and ``:limit`` binds.
    """
    return """
        SELECT e.id,
               e.title,
               e.starts_at,
               v.name AS venue_name,
               ST_Distance(
                   v.geom::geography,
                   ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography
               ) AS distance_m
        FROM events e
        JOIN venues v ON v.id = e.venue_id
        WHERE e.status = 'published'
          AND v.geom IS NOT NULL
          AND ST_DWithin(
              v.geom::geography,
              ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
              :radius_m
          )
        ORDER BY distance_m, e.starts_at
        LIMIT :limit
    """


def nearby_events_statement():
    """Return the prototype query as a SQLAlchemy ``TextClause``."""
    return text(nearby_events_sql())
