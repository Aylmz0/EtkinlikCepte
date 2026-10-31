# H3 technical evaluation — P1 preparation

Prepared for the H3.9 meeting (P3 chairs; team decides). Status is based on
the repo at 2026-10-31.

| H3 | Owner | Status | Evidence / blocker |
|---|---|---|---|
| H3.1 4 sources live + cleanup/dedup | P3 | ❌ | adapters/fixtures only; no live source run |
| H3.2 quality dashboard | P3 | ❌ | not started |
| H3.3 discovery map/filter screen | P7 | ⚠️ | UI mock; MapLibre/PMTiles not wired |
| H3.4 event detail + ticket select | P7 | ⚠️ | UI mock; API not wired |
| H3.5 location permission/nearby | P7 | ❌ | not started |
| H3.6 source attribution `/about` | P7 | ⚠️ | screen exists; live source data absent |
| H3.7 follow API | P2 | ❌ | H3 work not started |
| H3.8 Hurl 60% / pytest 90% | P1–P5 | ⚠️ | P1 share 33/33 green; team routes incomplete |
| H3.9 evaluation | all | ⚠️ | technical table prepared; team decision pending |
| H3.10 normalize + dedup | P3 | ⚠️ | adapter code; no live dedup run |
| H3.11 Overpass + osm2pgsql | P1/P3/P4 | ❌ | server deferred: 2.9 GB RAM / 133 MB free |
| H3.12 Martin/PMTiles | P1/P4 | ❌ | server deferred; config exists |
| H3.13 EXPLAIN/index report | P4 | ⚠️ | SQL prototype; no 100k fixture |
| H3.14 WS contract tests + types | P5 | ⚠️ | schema/docs exist; `/ws` handler absent |
| H3.15 client contract rehearsal | P6/P7 | ⚠️ | api-client generated; screens still mock |
| H3.16 notification texts + badge | P5 | ⚠️ | API list/read; UI badge mock |
| H3.17 platform wrappers + fake data | P6 | ⚠️ | mock data exists; wrappers not complete |

## Second-wave cut proposal (for the meeting)

1. Defer **H3.11 Overpass** until the server has headroom (current RAM is the
   blocker; do not disturb other projects).
2. Defer **H3.12 PMTiles** with H3.11; keep Martin config and production
   command in the repo.
3. Do not cut **H3.8** P1 share; it is green and protects `/v1`.
4. Keep H3.3–H3.5 UI work but mark map data as mock until H3.11/H3.12 returns.

Decision: **pending team meeting**.
