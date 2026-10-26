"""HTML adapter fixture tests: faker-generated pages, offline (R11)."""

from faker import Faker

from pipeline.sources.html import TARGETS, parse_html

fake = Faker("tr_TR")
Faker.seed(42)


def _fake_events(count: int) -> list[dict[str, str]]:
    return [
        {
            "title": fake.sentence(nb_words=3).rstrip("."),
            "path": f"/events/{fake.slug()}",
            "iso": fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "venue": fake.company(),
            "price": f"{fake.random_int(50, 500)} TL",
        }
        for _ in range(count)
    ]


def _site_a_page(events: list[dict[str, str]]) -> str:
    cards = "".join(
        f'<div class="event-card"><h3 class="event-title">{e["title"]}</h3>'
        f'<a class="event-link" href="{e["path"]}">detay</a>'
        f'<time datetime="{e["iso"]}">{e["iso"][:10]}</time>'
        f'<span class="venue">{e["venue"]}</span>'
        f'<span class="price">{e["price"]}</span></div>'
        for e in events
    )
    return f"<html><body>{cards}</body></html>"


def _site_b_page(events: list[dict[str, str]]) -> str:
    items = "".join(
        f'<li class="listing"><a class="name" href="{e["path"]}">{e["title"]}</a>'
        f'<span class="when">{e["iso"]}</span>'
        f'<span class="where">{e["venue"]}</span>'
        f'<span class="cost">{e["price"]}</span></li>'
        for e in events
    )
    return f"<html><body><ul>{items}</ul></body></html>"


def test_parse_site_a_extracts_fields() -> None:
    """Site A cards become raw rows with resolved links and hashes."""
    events = _fake_events(3)
    rows = parse_html(_site_a_page(events), TARGETS["site-a"], "https://a.example.com")
    assert len(rows) == 3
    first = rows[0]
    assert first["source"] == "site-a"
    assert first["source_ref"] == f"https://a.example.com{events[0]['path']}"
    assert first["payload"]["title"] == events[0]["title"]
    assert first["payload"]["starts_at"] == events[0]["iso"]
    assert first["payload"]["location"] == events[0]["venue"]
    assert first["payload"]["price"] == events[0]["price"]
    assert len(first["content_hash"]) == 64


def test_parse_site_b_extracts_fields() -> None:
    """Site B uses a different layout and selectors, same output shape."""
    events = _fake_events(2)
    rows = parse_html(_site_b_page(events), TARGETS["site-b"], "https://b.example.com")
    assert len(rows) == 2
    assert rows[1]["payload"]["title"] == events[1]["title"]
    assert rows[1]["payload"]["location"] == events[1]["venue"]


def test_hash_is_stable() -> None:
    """Parsing the same page twice yields the same content hash."""
    page = _site_a_page(_fake_events(1))
    first = parse_html(page, TARGETS["site-a"], "https://a.example.com")
    again = parse_html(page, TARGETS["site-a"], "https://a.example.com")
    assert first[0]["content_hash"] == again[0]["content_hash"]


def test_card_without_title_is_skipped() -> None:
    """A broken card must not crash the parser or produce a row."""
    page = '<div class="event-card"><a class="event-link" href="/x">x</a></div>'
    assert parse_html(page, TARGETS["site-a"], "https://a.example.com") == []
