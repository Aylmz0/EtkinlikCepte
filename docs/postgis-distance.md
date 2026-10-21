# PostGIS distance prototype

H1.10 training output and the query used as the H2.6 starting point.

## What the team learned

- Store coordinates as `GEOMETRY(POINT, 4326)`, not as two floats.
- Use `::geography` for metres; `geometry` distance is in degrees.
- Filter with `ST_DWithin` first so the GIST index is usable; sort after the
  candidate set is small.
- Keep the radius and category in query parameters; never interpolate them
  into SQL.

## Prototype query

Source: `apps/api/app/repos/discover.py`.

```sql
SELECT e.id, e.title, e.starts_at, v.name,
       ST_Distance(v.geom::geography,
                   ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography) AS distance_m
FROM events e
JOIN venues v ON v.id = e.venue_id
WHERE e.status = 'published'
  AND v.geom IS NOT NULL
  AND ST_DWithin(v.geom::geography,
                 ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography,
                 :radius_m)
ORDER BY distance_m, e.starts_at
LIMIT :limit;
```

Expected plan on the 100k-row target: `Index Scan` on `ix_venues_geom` for the
`ST_DWithin` predicate, then a small sort. Measure with `EXPLAIN ANALYZE` and
record the result in the H3.13 report.

## Next step

H2.6 wraps this query in `GET /discover/events?lat=&lng=&radius=&category=&when=&price=`
and adds pagination. H1 keeps the SQL as a tested prototype, not an endpoint.
