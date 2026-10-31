"""Raw adapter rows -> clean -> dedup -> database (H3.1)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from pipeline.normalize import clean_rows, group_duplicates
from pipeline.repos.events import write_clean_events

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoadStats:
    """Counts for the dashboard (H3.2): nothing is dropped silently."""

    raw: int
    dropped: int
    no_ref: int
    clean: int
    events: int


def load_rows(dsn: str, rows: list[dict[str, Any]]) -> LoadStats:
    """Clean raw rows, group duplicates and write them to the database."""
    clean, dropped = clean_rows(rows)
    usable = [event for event in clean if event.source_ref]
    no_ref = len(clean) - len(usable)
    if no_ref:
        log.warning("dropping records without source_ref", extra={"count": no_ref})
    groups = group_duplicates(usable)
    _, events = write_clean_events(dsn, groups) if groups else (0, 0)
    stats = LoadStats(len(rows), dropped, no_ref, len(usable), events)
    log.info("load finished", extra={"stats": stats})
    return stats
