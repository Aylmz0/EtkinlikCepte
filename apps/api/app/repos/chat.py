"""Chat tables: channels, members, messages, media rooms (§7 Sohbet).

DM channels hold exactly 2 members, deduplicated by dm_key
("smaller:id:bigger:id", §7). Owner: P5 from H4 on.
"""

from __future__ import annotations

import datetime
import enum
import uuid

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.repos.base import Base, uuid_pk


class ChannelKind(enum.StrEnum):
    """Channel scope: direct message, club channel, or event channel."""

    dm = "dm"
    club = "club"
    event = "event"


class MessageKind(enum.StrEnum):
    """Message payload kind."""

    text = "text"
    file = "file"
    link = "link"
    system = "system"


class ChatChannel(Base):
    """Conversation channel; dm_key set only for DM channels."""

    __tablename__ = "chat_channels"

    id: Mapped[uuid.UUID] = uuid_pk()
    kind: Mapped[ChannelKind | None] = mapped_column(Enum(ChannelKind, name="channel_kind"))
    club_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("clubs.id"))
    event_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("events.id"))
    dm_key: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (Index("uq_chat_channels_dm_key", "dm_key", unique=True),)


class ChatMember(Base):
    """Channel membership with per-user read watermark."""

    __tablename__ = "chat_members"

    channel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chat_channels.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    last_read_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))


class ChatMessage(Base):
    """Single chat message, optionally threaded via reply_to (§7)."""

    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = uuid_pk()
    channel_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("chat_channels.id"))
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str | None] = mapped_column(Text)
    kind: Mapped[MessageKind | None] = mapped_column(Enum(MessageKind, name="message_kind"))
    reply_to: Mapped[uuid.UUID | None]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (Index("ix_chat_messages_feed", "channel_id", "created_at"),)


class MediaRoom(Base):
    """LiveKit room backing an event or channel call (owner P5)."""

    __tablename__ = "media_rooms"

    id: Mapped[uuid.UUID] = uuid_pk()
    livekit_room: Mapped[str | None] = mapped_column(Text, unique=True)
    event_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("events.id"))
    channel_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("chat_channels.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    ended_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
