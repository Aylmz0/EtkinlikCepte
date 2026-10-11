"""Media, notifications, moderation and audit tables (§7, §4.9).

File bytes live in media.data (BYTEA), referenced by *_media_id columns —
never by path or URL (AGENTS.md invariant).
"""

from __future__ import annotations

import datetime
import enum
import uuid

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, Index, Integer, LargeBinary, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.repos.base import Base, uuid_pk


class MediaKind(enum.StrEnum):
    """What the stored bytes represent; size caps enforced in services."""

    avatar = "avatar"
    club_cover = "club_cover"
    event_image = "event_image"
    chat_attachment = "chat_attachment"
    club_post_image = "club_post_image"


class ReportStatus(enum.StrEnum):
    """Moderation queue status."""

    open = "open"
    reviewed = "reviewed"
    actioned = "actioned"


class Media(Base):
    """Stored file: avatar 2 MB, images 5 MB (§4.9)."""

    __tablename__ = "media"

    id: Mapped[uuid.UUID] = uuid_pk()
    owner_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    kind: Mapped[MediaKind | None] = mapped_column(Enum(MediaKind, name="media_kind"))
    content_type: Mapped[str | None] = mapped_column(Text)
    byte_size: Mapped[int | None] = mapped_column(Integer)
    sha256: Mapped[str | None] = mapped_column(Text)
    data: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))


class Notification(Base):
    """In-app notification row; closed-app delivery is out of scope (§1.3)."""

    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str | None] = mapped_column(Text)
    title: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str | None] = mapped_column(Text)
    data: Mapped[dict | None] = mapped_column(JSONB)
    read_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))


class Report(Base):
    """User complaint against a post, comment or club (§7)."""

    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = uuid_pk()
    reporter_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    target_kind: Mapped[str | None] = mapped_column(Text)
    target_id: Mapped[uuid.UUID | None]
    reason: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus, name="report_status"), default=ReportStatus.open
    )
    handled_by: Mapped[uuid.UUID | None]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    handled_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (Index("ix_reports_open", "status"),)


class AuditLog(Base):
    """Append-only admin action log, surfaced via GET /admin/audit (§7)."""

    __tablename__ = "audit_log"

    id: Mapped[uuid.UUID] = uuid_pk()
    actor_id: Mapped[uuid.UUID | None]
    action: Mapped[str | None] = mapped_column(Text)
    target: Mapped[str | None] = mapped_column(Text)
    meta: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (Index("ix_audit_log_created", "created_at"),)
