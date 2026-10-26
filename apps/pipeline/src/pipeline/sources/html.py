"""HTML adapter (Scrapy/parsel selectors), last-resort extraction path (§1.4).

Page scraping breaks when the site redesigns, so RSS and JSON-LD are tried
first. Each target declares its own CSS selectors; the parser itself is a pure
function so it can be tested offline with fixtures.
"""

from __future__ import annotations

import hashlib
import json
import logging
import urllib.request
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import dramatiq
from parsel import Selector

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class HtmlTarget:
    """CSS selectors for one scraped site.

    ``item`` selects each event card; every other selector is evaluated
    relative to that card and may end with ``::text`` or ``::attr(name)``.
    """

    name: str
    item: str
    title: str
    link: str
    date: str
    venue: str
    price: str


# Selector'ları gerçek sitelere göre DevTools (F12) ile doldur.
TARGETS: dict[str, HtmlTarget] = {
    "site-a": HtmlTarget(
        name="site-a",
        item="div.event-card",
        title="h3.event-title::text",
        link="a.event-link::attr(href)",
        date="time::attr(datetime)",
        venue="span.venue::text",
        price="span.price::text",
    ),
    "site-b": HtmlTarget(
        name="site-b",
        item="li.listing",
        title="a.name::text",
        link="a.name::attr(href)",
        date="span.when::text",
        venue="span.where::text",
        price="span.cost::text",
    ),
}


def _first(card: Selector, query: str) -> str:
    """Return the first match for ``query`` as stripped text ('' if missing)."""
    return (card.css(query).get() or "").strip()


def build_events(
    html: str | bytes, target: HtmlTarget, base_url: str | None = None
) -> list[dict[str, Any]]:
    """Extract event cards from a page into raw source rows.

    Args:
        html: Page HTML.
        target: Selector set for the site.
        base_url: Optional URL used to resolve relative links.

    Returns:
        Raw source-event dictionaries with stable content hashes. Cards
        without a title or link are skipped.
    """
    text = html.decode("utf-8", errors="replace") if isinstance(html, bytes) else html
    selector = Selector(text=text)
    rows: list[dict[str, Any]] = []
    for card in selector.css(target.item):
        title = _first(card, target.title)
        link = _first(card, target.link)
        if not title or not link:
            log.warning("skipping card without title/link", extra={"source": target.name})
            continue
        if base_url:
            link = urljoin(base_url, link)
        payload = {
            "source": target.name,
            "source_ref": link,
            "title": title,
            "starts_at": _first(card, target.date),
            "location": _first(card, target.venue),
            "price": _first(card, target.price),
        }
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        rows.append(
            {
                "source": target.name,
                "source_ref": link,
                "content_hash": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
                "payload": payload,
            }
        )
    return rows


def parse_html(
    html: str | bytes, target: HtmlTarget, base_url: str | None = None
) -> list[dict[str, Any]]:
    """Parse a page without touching the network (test/fixture entry point)."""
    return build_events(html, target, base_url)


@dramatiq.actor
def fetch_html_page(source_name: str, page_url: str) -> list[dict[str, Any]]:
    """Fetch one listing page and return its raw rows."""
    target = TARGETS[source_name]
    log.info("fetching html page", extra={"source": source_name, "url": page_url})
    request = urllib.request.Request(  # noqa: S310
        page_url, headers={"User-Agent": "EtkinlikCepteBot/0.1"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
        html = response.read()
    return build_events(html, target, base_url=page_url)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log.info("html adapter ready; targets: %s", ", ".join(TARGETS))
