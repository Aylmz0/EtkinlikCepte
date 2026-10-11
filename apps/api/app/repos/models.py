"""Single registration point for all models; Alembic reads Base from here."""

from app.repos import auth, chat, clubs, content, events, geo, pipeline  # noqa: F401
from app.repos.base import Base

__all__ = ["Base", "auth", "chat", "clubs", "content", "events", "geo", "pipeline"]
