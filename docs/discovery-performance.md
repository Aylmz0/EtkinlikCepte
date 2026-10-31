# Discovery performance notes (H2.6/H2.16)

The query is implemented in `apps/api/app/repos/discovery_repo.py`:

- candidate filter: `ST_DWithin(venues.geom::geography, point, radius)`
- index: `ix_venues_geom` (GIST)
- ordering: `distance_m`, then `starts_at`
- hard cap: 200 candidates
- statement timeout: 300 ms

Target from §11: discovery query < 300 ms at 100k records.

Benchmark command once a seeded database exists:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT e.id, v.geom
FROM events e JOIN venues v ON v.id = e.venue_id
WHERE e.status = 'published'
  AND ST_DWithin(v.geom::geography,
                 ST_SetSRID(ST_MakePoint(32.8, 39.9), 4326)::geography,
                 10000)
ORDER BY v.geom <-> ST_SetSRID(ST_MakePoint(32.8, 39.9), 4326)::geography
LIMIT 200;
```

The 100k-row fixture and Nominatim Turkey import are staging tasks; the SQL
prototype and integration smoke test are green.
