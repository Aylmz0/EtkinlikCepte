"""SQLAlchemy declarative base with shared conventions (H1.3, owner P1).

All models register here via app.repos.models; Alembic autogenerate reads
Base.metadata from this module.
"""

from __future__ import annotations

import uuid

from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base class carrying the project-wide constraint naming convention."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def uuid_pk() -> Mapped[uuid.UUID]:
    """Return a UUID primary-key column defaulting to uuid4 (§7: id UUID PK)."""
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
