# Realtime protocol

Source of truth for code: `apps/api/app/schemas/realtime.py`.

## Envelope

Every frame is one JSON text message: `{"type": "<str>", "payload": {...}}`. Field names are snake_case. Timestamps are UTC ISO 8601. Exactly seven types exist (below).

## Connection and auth

`GET /v1/ws?token=<access JWT>`. A missing or invalid token closes the socket with 4401. The server rejects anything that is not a valid client frame with 4400.

| Code | Meaning |
|------|---------|
| 4400 | Malformed frame or unknown type |
| 4401 | Missing or invalid token |
| 4408 | Heartbeat timeout |

## Heartbeat and presence

Browsers cannot send protocol ping frames from JS, so the heartbeat is an app message: the client sends `presence.update` with `status: "online"` every 30 s (§11). After 2 missed heartbeats (60 s) the server marks the user offline, broadcasts `presence.update`, and closes with 4408.

## Reconnect and message window

Clients reconnect with backoff 1, 2, 4, 8 s, capped at 8 s (§11), and refetch what they missed. A client keeps the last 200 messages per channel; older ones come from `GET /channels/{id}/messages?before=`.

## Frames

### `msg.send` (both directions)

Client to server. `client_id` is the idempotency key (the WS form of `Idempotency-Key`, §8.1 rule 6); the server dedupes on (user, `client_id`).

| Field | Type | Notes |
|-------|------|-------|
| channel_id | UUID | |
| client_id | UUID | |
| kind | `text` \| `file` \| `link` | `system` is server-only |
| body | string | 1 to 4000 chars |
| reply_to | UUID \| null | |

```json
{"type": "msg.send", "payload": {"channel_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0001", "client_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0002", "kind": "text", "body": "Hello", "reply_to": null}}
```

Server to client: fan-out to all channel members, including the sender's other devices.

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | |
| channel_id | UUID | |
| user_id | UUID | |
| kind | `text` \| `file` \| `link` \| `system` | |
| body | string | |
| reply_to | UUID \| null | |
| created_at | datetime | |
| client_id | UUID \| null | null for system messages |

```json
{"type": "msg.send", "payload": {"id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0003", "channel_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0001", "user_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0004", "kind": "text", "body": "Hello", "reply_to": null, "created_at": "2026-01-01T12:00:00Z", "client_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0002"}}
```

### `msg.ack` (server to client)

Sent only to the sending connection. Exactly one of (`id` + `created_at`) or `error` is set.

| Field | Type | Notes |
|-------|------|-------|
| client_id | UUID | echoes the request |
| id | UUID | success |
| created_at | datetime | success |
| error | ProblemDetail | RFC 9457 body, failure |

```json
{"type": "msg.ack", "payload": {"client_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0002", "id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0003", "created_at": "2026-01-01T12:00:00Z"}}
```

```json
{"type": "msg.ack", "payload": {"client_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0002", "error": {"type": "about:blank", "title": "Forbidden", "status": 403, "detail": "Not a channel member"}}}
```

### `msg.typing` (both directions)

Ephemeral, never stored. Clients send at most once per 3 s; receivers hide the indicator after 5 s.

| Direction | Fields |
|-----------|--------|
| client to server | channel_id |
| server to client | channel_id, user_id |

```json
{"type": "msg.typing", "payload": {"channel_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0001"}}
```

```json
{"type": "msg.typing", "payload": {"channel_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0001", "user_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0004"}}
```

### `presence.update` (both directions)

Client to server is the heartbeat: `status` is always `online`.

```json
{"type": "presence.update", "payload": {"status": "online"}}
```

Server to client:

| Field | Type | Notes |
|-------|------|-------|
| user_id | UUID | |
| status | `online` \| `offline` | |
| last_seen | datetime \| null | |

```json
{"type": "presence.update", "payload": {"user_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0004", "status": "offline", "last_seen": "2026-01-01T12:00:00Z"}}
```

### `event.updated` (server to client)

The client just invalidates its event query.

| Field | Type | Notes |
|-------|------|-------|
| event_id | UUID | |
| status | `draft` \| `published` \| `cancelled` \| `completed` | |
| updated_at | datetime | |

```json
{"type": "event.updated", "payload": {"event_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0005", "status": "published", "updated_at": "2026-01-01T12:00:00Z"}}
```

### `ticket.sold_out` (server to client)

| Field | Type |
|-------|------|
| event_id | UUID |
| ticket_id | UUID |

```json
{"type": "ticket.sold_out", "payload": {"event_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0005", "ticket_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0006"}}
```

### `notification.push` (server to client)

Same fields as a `notifications` row (§7).

| Field | Type |
|-------|------|
| id | UUID |
| kind | string |
| title | string |
| body | string |
| data | object \| null |
| created_at | datetime |

```json
{"type": "notification.push", "payload": {"id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0007", "kind": "event_reminder", "title": "Starting soon", "body": "Your event starts in 1 hour", "data": {"event_id": "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f0005"}, "created_at": "2026-01-01T12:00:00Z"}}
```
