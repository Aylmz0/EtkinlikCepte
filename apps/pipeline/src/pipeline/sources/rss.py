"""RSS/Atom adapter: fetch a feed, normalize entries, and hash raw payloads.

The adapter is deliberately database-free: it returns rows that the pipeline
worker writes to ``source_events`` once the database wiring lands. RSS/Atom is
the first extraction choice because it survives page redesigns (§1.4).
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import UTC, datetime
from typing import Any

import dramatiq
import feedparser

log = logging.getLogger(__name__)


def build_events(feed: Any, source_name: str) -> list[dict[str, Any]]:
    """Convert a parsed feed into raw source-event dictionaries.

    Args:
        feed: A ``feedparser`` result or any object exposing ``entries``.
        source_name: Stable source identifier stored with every row.

    Returns:
        One dictionary per entry with a stable SHA-256 ``content_hash``.
    """
    events: list[dict[str, Any]] = []
    for entry in feed.entries:
        title = str(entry.get("title", "")).strip()
        link = str(entry.get("link", "")).strip()
        published = str(entry.get("published", datetime.now(UTC).isoformat()))
        summary = str(entry.get("summary", "")).strip()
        payload = {
            "source": source_name,
            "source_ref": link,
            "title": title,
            "published_at": published,
            "summary": summary,
        }
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        events.append(
            {
                "source": source_name,
                "source_ref": link,
                "content_hash": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
                "payload": payload,
            }
        )
    return events


def parse_feed(xml: str | bytes, source_name: str) -> list[dict[str, Any]]:
    """Parse RSS/Atom text without touching the network.

    Args:
        xml: Raw feed document.
        source_name: Stable source identifier stored with every row.

    Returns:
        Raw source-event dictionaries ready for normalization.
    """
    return build_events(feedparser.parse(xml), source_name)


@dramatiq.actor
def fetch_rss_feed(source_name: str, feed_url: str) -> list[dict[str, Any]]:
    """Fetch one feed and return its raw rows (DB write is a later stage).

    Args:
        source_name: Stable source identifier.
        feed_url: RSS/Atom URL from ``source_configs``.

    Returns:
        Raw source-event dictionaries for the normalizer.
    """
    log.info("fetching rss feed", extra={"source": source_name, "url": feed_url})
    return build_events(feedparser.parse(feed_url), source_name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log.info("adapter ready; schedule it through source_configs")
