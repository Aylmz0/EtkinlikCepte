# H3.8 — Hurl coverage (P1 share)

Command:

```bash
cd apps/api
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
# in another shell, from repo root:
hurl --test apps/api/hurl/*.hurl
```

Last result: **11 files / 33 requests / 100% green** against a migrated
Postgres database.

| Area | Endpoint(s) | Hurl file | Status |
|---|---|---|---|
| Auth | `POST /v1/auth/register` | `01`, `06`, `08` | ✅ |
| Auth | `POST /v1/auth/login` | `01`, `06`, `08` | ✅ |
| Auth | `POST /v1/auth/refresh` | `06` | ✅ |
| Auth | `POST /v1/auth/logout` | `06` | ✅ |
| Auth | `GET /v1/auth/me` | `06`, `08`, `09` | ✅ |
| Auth | `PATCH /v1/auth/me` | `09` | ✅ |
| System | `GET /health` | `10` | ✅ |
| System | `GET /openapi.json` | `10` | ✅ |
| Admin | `GET /v1/admin/sources` | `11` | ✅ |
| Admin | `POST /v1/admin/sources/{id}/run` | `11` | ✅ |
| Clubs | list/create/detail/members | `02`–`05` | ✅ |
| Discover | venues/events/recommendations | `07` | ✅ |

## P1-owned gaps (documented, not silently skipped)

- `GET /metrics`: contract §8 lists it; H6.5 owns implementation.
- `GET /admin/audit`: contract §8 lists it; H6.5 owns audit wiring.
- `PATCH /admin/sources/{id}`: returns 501 in the H1.16 skeleton; H5.10 owns it.
- `/ws` text chat: H4.1/H3.14; not part of H2/H3 P1 share.

## Team coverage note

H3.8’s 60% target is a team number. P1’s owned endpoints above are green;
the remaining routes belong to H2/H3 owners and are tracked in
`docs/contract-audit-h2.md`.
