"""H1.10 PostGIS prototype: distance filter and index-friendly predicates."""

from app.repos.discover import nearby_events_sql


def test_query_uses_postgis_distance_and_radius() -> None:
    """The prototype must filter by ST_DWithin and order by distance."""
    sql = nearby_events_sql()
    assert "ST_DWithin" in sql
    assert "ST_Distance" in sql
    assert "::geography" in sql
    assert "ORDER BY distance_m" in sql
    assert "e.status = 'published'" in sql
