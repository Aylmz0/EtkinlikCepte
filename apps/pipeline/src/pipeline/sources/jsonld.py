"""JSON-LD (schema.org/Event) adapter, second extraction path (§1.4)."""

from __future__ import annotations

import hashlib
import json
import logging
import urllib.request
from datetime import UTC, datetime
from typing import Any

import dramatiq
from extruct.jsonld import JsonLdExtractor

log = logging.getLogger(__name__)


def _event_items(value: Any) -> list[dict[str, Any]]:
    """Flatten a JSON-LD document into schema.org/Event dictionaries."""
    items: list[dict[str, Any]] = []
    if isinstance(value, dict):
        type_value = value.get("@type")
        is_event = type_value == "Event" or (isinstance(type_value, list) and "Event" in type_value)
        if is_event:
            items.append(value)
        graph = value.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                if isinstance(item, dict):
                    item_type = item.get("@type")
                    if item_type == "Event" or (
                        isinstance(item_type, list) and "Event" in item_type
                    ):
                        items.append(item)
    elif isinstance(value, list):
        for item in value:
            items.extend(_event_items(item))
    return items


def build_events(
    html: str | bytes, source_name: str, base_url: str | None = None
) -> list[dict[str, Any]]:
    """Extract schema.org/Event JSON-LD blocks into raw source rows.

    Args:
        html: Page HTML.
        source_name: Stable source identifier.
        base_url: Optional URL used to resolve relative links.

    Returns:
        Raw source-event dictionaries with stable content hashes.
    """
    blocks = JsonLdExtractor().extract(html, base_url=base_url)
    rows: list[dict[str, Any]] = []
    for block in blocks:
        for item in _event_items(block):
            link = str(item.get("url", "")).strip()
            payload = {
                "source": source_name,
                "source_ref": link,
                "title": str(item.get("name", "")).strip(),
                "starts_at": item.get("startDate"),
                "ends_at": item.get("endDate"),
                "location": item.get("location"),
                "offers": item.get("offers"),
                "description": item.get("description"),
            }
            canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
            rows.append(
                {
                    "source": source_name,
                    "source_ref": link,
                    "content_hash": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
                    "payload": payload,
                }
            )
    return rows


def parse_jsonld(
    html: str | bytes, source_name: str, base_url: str | None = None
) -> list[dict[str, Any]]:
    """Parse JSON-LD without touching the network (test/fixture entry point)."""
    return build_events(html, source_name, base_url)


@dramatiq.actor
def fetch_jsonld_page(source_name: str, page_url: str) -> list[dict[str, Any]]:
    """Fetch one HTML page and return its schema.org/Event rows."""
    log.info("fetching json-ld page", extra={"source": source_name, "url": page_url})
    with urllib.request.urlopen(page_url, timeout=30) as response:  # noqa: S310
        html = response.read()
    return build_events(html, source_name, base_url=page_url)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log.info("json-ld adapter ready at %s", datetime.now(UTC).isoformat())
