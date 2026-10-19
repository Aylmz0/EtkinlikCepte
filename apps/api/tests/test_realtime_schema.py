"""WebSocket frame contract tests: the docs/realtime.md examples must parse."""

import json

import pytest
from app.schemas.realtime import ServerFrame, parse_client_frame
from pydantic import TypeAdapter, ValidationError

U = "6f1c0a52-2b0e-4a43-9a53-1d7c1b7f000"
T = "2026-01-01T12:00:00Z"
SEND = {"channel_id": U + "1", "client_id": U + "2", "kind": "text", "body": "Hi", "reply_to": None}
ACK = {"client_id": U + "2", "id": U + "3", "created_at": T}
ERR = {"title": "Forbidden", "status": 403, "detail": "no"}

CLIENT = [
    ("msg.send", SEND),
    ("msg.typing", {"channel_id": U + "1"}),
    ("presence.update", {"status": "online"}),
]
SYSTEM_MSG = {
    "id": U + "3",
    "channel_id": U + "1",
    "user_id": U + "4",
    "kind": "system",
    "body": "x",
    "reply_to": None,
    "created_at": T,
    "client_id": None,
}
SERVER = [
    ("msg.send", SYSTEM_MSG),
    ("msg.ack", ACK),
    ("msg.ack", {"client_id": U + "2", "error": ERR}),
    ("msg.typing", {"channel_id": U + "1", "user_id": U + "4"}),
    ("presence.update", {"user_id": U + "4", "status": "offline", "last_seen": T}),
    ("event.updated", {"event_id": U + "5", "status": "published", "updated_at": T}),
    ("ticket.sold_out", {"event_id": U + "5", "ticket_id": U + "6"}),
    (
        "notification.push",
        {"id": U + "7", "kind": "k", "title": "t", "body": "b", "data": {"a": 1}, "created_at": T},
    ),
]


def frame(type_: str, payload: dict) -> str:
    return json.dumps({"type": type_, "payload": payload})


@pytest.mark.parametrize(("type_", "payload"), CLIENT)
def test_client_examples_parse(type_, payload):
    assert parse_client_frame(frame(type_, payload)).type == type_


@pytest.mark.parametrize(("type_", "payload"), SERVER)
def test_server_examples_parse(type_, payload):
    assert TypeAdapter(ServerFrame).validate_json(frame(type_, payload)).type == type_


@pytest.mark.parametrize(
    "raw",
    [
        frame("event.updated", {}),  # server-only type
        frame("msg.send", {**SEND, "body": "x" * 4001}),
        frame("msg.send", {**SEND, "kind": "system"}),
        "not json",
    ],
)
def test_bad_client_frames_rejected(raw):
    with pytest.raises(ValidationError):
        parse_client_frame(raw)


@pytest.mark.parametrize("payload", [{**ACK, "error": ERR}, {"client_id": U + "2"}])
def test_ack_needs_exactly_one_of_success_or_error(payload):
    with pytest.raises(ValidationError):
        TypeAdapter(ServerFrame).validate_json(frame("msg.ack", payload))
