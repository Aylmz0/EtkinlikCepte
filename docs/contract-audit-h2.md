# H2 contract freeze audit — 2026-10-31

Compared against `development.md` §8 and the generated `/openapi.json`.

## Auth

| Contract | OpenAPI | Note |
|---|---|---|
| POST /auth/register | ✅ | email/password/display_name |
| POST /auth/login | ✅ | |
| POST /auth/refresh | ✅ | rotation + revocation |
| POST /auth/logout | ✅ | idempotent |
| GET /auth/me | ✅ | full profile |
| PATCH /auth/me | ✅ | H2.2 profile fields |

## System

| Contract | OpenAPI | Note |
|---|---|---|
| GET /health | ✅ | |
| GET /openapi.json | ✅ | 3.1 |
| GET /metrics | ❌ | H6.5 |

## Admin / moderation

| Contract | OpenAPI | Note |
|---|---|---|
| GET /admin/sources | ✅ | list skeleton |
| PATCH /admin/sources/{id} | ✅ | 501 until H5.10 |
| POST /admin/sources/{id}/run | ✅ | 202 |
| GET /admin/audit | ❌ | H6.5 |
| GET /admin/reports | ❌ | H5.6 |
| POST /admin/reports/{id}/handle | ❌ | H5.6 |

## Club / event / ticket

| Contract | OpenAPI | Note |
|---|---|---|
| Club CRUD, members, invitations | ✅ | H2.3 |
| Follow endpoints | ❌ | H3.7 |
| Event CRUD, publish/cancel | ✅ | H2.4 |
| `GET /events/{id}/sources` | ❌ | H3/H2 source attribution |
| Ticket types, register, QR, check-in | ✅ | H2.5 |
| `/registrations/{id}` delete | ✅ | implemented |
| Recommendation feedback | ❌ | D1/Faz 2 |

## Chat / media / notification

| Contract | OpenAPI | Note |
|---|---|---|
| Room tokens | ✅ | H2.18 |
| `GET /channels`, messages, DM | ❌ | H4.1–H4.4 |
| `GET /ws` | ❌ | H4.1 |
| Notifications list/read | ✅ | H2.19 |
| Media upload/read | ❌ | H4 |
| `/devices` | ✅ | H2.19 |

## Discover

| Contract | OpenAPI | Note |
|---|---|---|
| venues/events/recommendations | ✅ | H2.6/H2.16/H2.17 |
| Feedback | ❌ | deferred |

## Findings

1. H2 scope is frozen and internally consistent for auth, club/event/ticket,
   discovery, devices and notifications.
2. Missing routes are later-work ownership, not accidental `/v1` drift.
3. `PATCH /admin/sources/{id}` is intentionally 501 until H5.10; it must not be
   presented as a working admin operation.
4. Error bodies for validation and HTTP exceptions are RFC 9457 after the
   H3.8 fix.
