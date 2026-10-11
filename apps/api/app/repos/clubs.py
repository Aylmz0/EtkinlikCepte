"""Club tables: clubs, members, invitations, followers, posts (§7 Kulüpler).

Membership and following stay separate: a club may have 20 members but
2000 followers (§7).
"""

from __future__ import annotations

import datetime
import enum
import uuid

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import CITEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.repos.base import Base, uuid_pk


class ClubRole(enum.StrEnum):
    """Membership role inside a club."""

    owner = "owner"
    admin = "admin"
    moderator = "moderator"
    member = "member"


class PostVisibility(enum.StrEnum):
    """Who may see a club post."""

    public = "public"
    followers = "followers"
    members = "members"


class Club(Base):
    """Club profile and ownership (§7)."""

    __tablename__ = "clubs"

    id: Mapped[uuid.UUID] = uuid_pk()
    name: Mapped[str] = mapped_column(Text)
    slug: Mapped[str] = mapped_column(CITEXT, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(Text)
    cover_media_id: Mapped[uuid.UUID | None]
    owner_id: Mapped[uuid.UUID | None]
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))


class ClubMember(Base):
    """Membership row; composite primary key (club_id, user_id)."""

    __tablename__ = "club_members"

    club_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clubs.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role: Mapped[ClubRole] = mapped_column(Enum(ClubRole, name="club_role"))
    joined_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))


class ClubInvitation(Base):
    """Email invitation carrying a unique redeem code (§7)."""

    __tablename__ = "club_invitations"

    id: Mapped[uuid.UUID] = uuid_pk()
    club_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("clubs.id"))
    email: Mapped[str | None] = mapped_column(Text)
    code: Mapped[str] = mapped_column(Text, unique=True)
    role: Mapped[ClubRole | None] = mapped_column(Enum(ClubRole, name="club_role"))
    expires_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    accepted_by: Mapped[uuid.UUID | None]
    created_by: Mapped[uuid.UUID | None]


class ClubFollower(Base):
    """Follow row, separate from membership; indexed for the following feed."""

    __tablename__ = "club_followers"

    club_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clubs.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (Index("ix_following_feed", "user_id", "created_at"),)


class ClubPost(Base):
    """Text-plus-photo club post with an optional external link (§4.13)."""

    __tablename__ = "club_posts"

    id: Mapped[uuid.UUID] = uuid_pk()
    club_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("clubs.id"))
    author_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str | None] = mapped_column(Text)
    visibility: Mapped[PostVisibility] = mapped_column(
        Enum(PostVisibility, name="post_visibility"), default=PostVisibility.followers
    )
    link_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    edited_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (Index("ix_club_posts_feed", "club_id", "created_at"),)


class ClubPostMedia(Base):
    """Post attachments: at most 4 images of 5 MB each (§7)."""

    __tablename__ = "club_post_media"

    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("club_posts.id"), primary_key=True)
    media_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("media.id"), primary_key=True)
    position: Mapped[int | None]


class ClubPostLike(Base):
    """Post like; composite primary key (post_id, user_id)."""

    __tablename__ = "club_post_likes"

    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("club_posts.id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))


class ClubPostComment(Base):
    """Comment on a club post (§7)."""

    __tablename__ = "club_post_comments"

    id: Mapped[uuid.UUID] = uuid_pk()
    post_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("club_posts.id"), index=True)
    author_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=True))
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (Index("ix_post_comments", "post_id", "created_at"),)


# UUID imported for re-export clarity in FK string contexts.
_ = UUID
