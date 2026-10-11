"""H1.3 schema tests: every §7 table is mapped with its critical indexes."""

from app.repos import models  # noqa: F401  (register all tables)
from app.repos.base import Base

EXPECTED_TABLES = {
    "users",
    "refresh_tokens",
    "devices",
    "clubs",
    "club_members",
    "club_invitations",
    "club_followers",
    "club_posts",
    "club_post_media",
    "club_post_likes",
    "club_post_comments",
    "venues",
    "source_events",
    "events",
    "event_sources",
    "event_tickets",
    "registrations",
    "event_invitations",
    "chat_channels",
    "chat_members",
    "chat_messages",
    "media_rooms",
    "media",
    "notifications",
    "reports",
    "audit_log",
    "source_configs",
    "ranking_weights",
    "user_event_stats",
}


def test_all_contract_tables_mapped() -> None:
    """Every §7 table has a SQLAlchemy model (H1.3 exit gate, part 1)."""
    assert set(Base.metadata.tables) == EXPECTED_TABLES


def test_users_profile_columns() -> None:
    """P1 H1.3 decision: users carries locale plus optional budget (§1.5)."""
    columns = Base.metadata.tables["users"].columns
    assert columns["locale"].default.arg == "tr"
    assert "budget_minor" in columns
    assert "budget_currency" in columns


def test_money_never_float() -> None:
    """Money columns are integer minor units, never float (§8.1)."""
    tables = Base.metadata.tables
    assert str(tables["source_events"].columns["price_minor"].type) == "INTEGER"
    assert str(tables["event_tickets"].columns["price_minor"].type) == "INTEGER"
    assert str(tables["registrations"].columns["amount_minor"].type) == "INTEGER"


def test_critical_indexes_present() -> None:
    """Spot-check the §7 critical index list on mapped metadata."""
    inspector_tables = {
        "events": {"ix_events_starts_at", "ix_events_status", "ix_events_origin_status"},
        "chat_messages": {"ix_chat_messages_feed"},
        "club_posts": {"ix_club_posts_feed"},
    }
    for table, names in inspector_tables.items():
        mapped = {i.name for i in Base.metadata.tables[table].indexes}
        assert names <= mapped, f"{table}: missing {names - mapped}"
