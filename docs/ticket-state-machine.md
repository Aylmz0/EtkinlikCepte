# Ticket state machine and QR decision

Source of truth for code: `apps/api/app/domain/tickets.py`.

## States

| State | Meaning |
|---|---|
| `reserved` | Slot held for 15 minutes; no payment yet |
| `pending_payment` | Organiser must approve the payment |
| `paid` | Paid ticket; QR is valid |
| `free_granted` | Free ticket; QR is valid |
| `used` | Checked in at the door |
| `cancelled` | Cancelled by user or organiser |
| `refunded` | Refunded after payment |
| `expired` | Reservation/payment window elapsed |

## Transition matrix

| From | Allowed to |
|---|---|
| `reserved` | `pending_payment`, `cancelled`, `expired` |
| `pending_payment` | `paid`, `cancelled`, `expired` |
| `paid` | `used`, `refunded`, `cancelled` |
| `free_granted` | `used`, `cancelled` |
| `used` | — |
| `cancelled` | — |
| `refunded` | — |
| `expired` | — |

`reserved` expires after 15 minutes. Expiry is a scheduled transition, not a
client request; the worker moves stale rows to `expired` and releases capacity.

## Capacity rule

`event_tickets.sold_count` increments only for `paid` and `free_granted`
(§8.1 rule 7). `reserved` and `pending_payment` hold capacity but do not count
until they become `paid`/`free_granted`. A unique `registrations(event_id,
user_id)` row prevents duplicate registrations.

## QR decision

- Payload: a unique random `qr_token` (URL-safe, 32 bytes), never the
  registration UUID or user id.
- Generation: `segno` renders the token as a QR image; the API returns the
  image or an `image/svg+xml` response.
- Validation: `POST /registrations/{id}/checkin` looks up the token, checks
  the status (`paid` or `free_granted`), sets `checked_in_at`, and transitions
  to `used`.
- Offline: the QR image is cached on the device; the door client can verify
  after reconnecting. A used token cannot be replayed because the status is
  terminal.
