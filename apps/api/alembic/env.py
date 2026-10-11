"""Alembic environment: metadata comes from app.repos.models (H1.3, owner P1).

The database URL always comes from DATABASE_URL; alembic.ini carries no
credentials (secrets never enter the repo, §13.2).
"""

from __future__ import annotations

import os
import sys
from logging.config import fileConfig

from alembic import context

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.repos.models import Base
from sqlalchemy import engine_from_config, pool

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

DB_URL = os.environ.get("DATABASE_URL", "postgresql://projectx:projectx@localhost:5432/projectx")
config.set_main_option("sqlalchemy.url", DB_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Emit SQL without a live connection.

    Args:
        None.
    """
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Apply migrations against the DATABASE_URL database."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
