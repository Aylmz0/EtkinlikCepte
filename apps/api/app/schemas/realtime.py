"""WebSocket frame contract: `GET /v1/ws?token=<access JWT>` (docs/realtime.md).

Every frame is `{"type": ..., "payload": {...}}`. `ClientFrame` is what a client
may send; `ServerFrame` is everything the server may send.
"""

from __future__ import annotations

import datetime
import enum
import uuid
from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter, model_validator

from app.repos.chat import MessageKind
from app.repos.events import EventStatus
from app.schemas.common import ProblemDetail

HEARTBEAT_INTERVAL_S = 30  # §11: client sends presence.update every 30 s
PRESENCE_TIMEOUT_S = 60  # 2 missed heartbeats -> offline + close 4408
TYPING_THROTTLE_S = 3  # client sends msg.typing at most once per 3 s
TYPING_EXPIRE_S = 5  # receivers hide the indicator after 5 s of silence
RECONNECT_BACKOFF_S = (1, 2, 4, 8)  # §11: capped at the last value
MESSAGE_WINDOW = 200  # §11: messages kept per channel on the client
MESSAGE_BODY_MAX = 4000  # chars; matches the chat message size limit

CLOSE_MALFORMED = 4400  # malformed frame or unknown type
CLOSE_UNAUTHORIZED = 4401  # missing or invalid token
CLOSE_HEARTBEAT_TIMEOUT = 4408  # no heartbeat within PRESENCE_TIMEOUT_S


class ClientMessageKind(enum.StrEnum):
    """Message kinds a client may send; `system` is server-only."""

    text = MessageKind.text.value
    file = MessageKind.file.value
    link = MessageKind.link.value


class PresenceStatus(enum.StrEnum):
    """User presence as seen by other clients."""

    online = "online"
    offline = "offline"


# --- payloads ---------------------------------------------------------------


class MsgSendIn(BaseModel):
    """Client sends a message; `client_id` is the idempotency key (§8.1 rule 6)."""

    channel_id: uuid.UUID
    client_id: uuid.UUID
    kind: ClientMessageKind
    body: str = Field(min_length=1, max_length=MESSAGE_BODY_MAX)
    reply_to: uuid.UUID | None = None


class MsgSendOut(BaseModel):
    """Stored message fanned out to channel members (incl. sender's other devices)."""

    id: uuid.UUID
    channel_id: uuid.UUID
    user_id: uuid.UUID
    kind: MessageKind
    body: str
    reply_to: uuid.UUID | None = None
    created_at: datetime.datetime
    client_id: uuid.UUID | None = None  # None for system messages


class MsgAck(BaseModel):
    """Result of a `msg.send`, sent only to the sending connection."""

    client_id: uuid.UUID
    id: uuid.UUID | None = None
    created_at: datetime.datetime | None = None
    error: ProblemDetail | None = None

    @model_validator(mode="after")
    def _success_xor_error(self) -> MsgAck:
        success = (self.id, self.created_at)
        if self.error is None and None in success:
            raise ValueError("set id+created_at, or error")
        if self.error is not None and any(v is not None for v in success):
            raise ValueError("set id+created_at, or error, not both")
        return self


class TypingIn(BaseModel):
    """Client is typing in a channel."""

    channel_id: uuid.UUID


class TypingOut(BaseModel):
    """Someone is typing in a channel."""

    channel_id: uuid.UUID
    user_id: uuid.UUID


class PresenceIn(BaseModel):
    """Client heartbeat; only `online` is ever sent."""

    status: Literal[PresenceStatus.online]


class PresenceOut(BaseModel):
    """A user's presence changed."""

    user_id: uuid.UUID
    status: PresenceStatus
    last_seen: datetime.datetime | None = None


class EventUpdated(BaseModel):
    """An event changed; the client invalidates its event query."""

    event_id: uuid.UUID
    status: EventStatus
    updated_at: datetime.datetime


class TicketSoldOut(BaseModel):
    """A ticket type has no stock left."""

    event_id: uuid.UUID
    ticket_id: uuid.UUID


class NotificationPush(BaseModel):
    """Same fields as a `notifications` row (§7)."""

    id: uuid.UUID
    kind: str
    title: str
    body: str
    data: dict | None = None
    created_at: datetime.datetime


# --- frames -----------------------------------------------------------------


class MsgSendInFrame(BaseModel):
    """Client `msg.send`."""

    type: Literal["msg.send"]
    payload: MsgSendIn


class MsgSendOutFrame(BaseModel):
    """Server `msg.send`."""

    type: Literal["msg.send"]
    payload: MsgSendOut


class MsgAckFrame(BaseModel):
    """Server `msg.ack`."""

    type: Literal["msg.ack"]
    payload: MsgAck


class TypingInFrame(BaseModel):
    """Client `msg.typing`."""

    type: Literal["msg.typing"]
    payload: TypingIn


class TypingOutFrame(BaseModel):
    """Server `msg.typing`."""

    type: Literal["msg.typing"]
    payload: TypingOut


class PresenceInFrame(BaseModel):
    """Client `presence.update` (heartbeat)."""

    type: Literal["presence.update"]
    payload: PresenceIn


class PresenceOutFrame(BaseModel):
    """Server `presence.update`."""

    type: Literal["presence.update"]
    payload: PresenceOut


class EventUpdatedFrame(BaseModel):
    """Server `event.updated`."""

    type: Literal["event.updated"]
    payload: EventUpdated


class TicketSoldOutFrame(BaseModel):
    """Server `ticket.sold_out`."""

    type: Literal["ticket.sold_out"]
    payload: TicketSoldOut


class NotificationPushFrame(BaseModel):
    """Server `notification.push`."""

    type: Literal["notification.push"]
    payload: NotificationPush


ClientFrame = Annotated[
    MsgSendInFrame | TypingInFrame | PresenceInFrame, Field(discriminator="type")
]
ServerFrame = Annotated[
    MsgSendOutFrame
    | MsgAckFrame
    | TypingOutFrame
    | PresenceOutFrame
    | EventUpdatedFrame
    | TicketSoldOutFrame
    | NotificationPushFrame,
    Field(discriminator="type"),
]

_client_adapter: TypeAdapter[ClientFrame] = TypeAdapter(ClientFrame)


def parse_client_frame(raw: str | bytes) -> ClientFrame:
    """Parse a raw WebSocket frame sent by a client.

    Args:
        raw: JSON text or bytes of one frame.

    Returns:
        The validated client frame.

    Raises:
        pydantic.ValidationError: Malformed JSON, unknown type, or bad payload;
            the caller closes with `CLOSE_MALFORMED`.
    """
    return _client_adapter.validate_json(raw)
