"""Normalization + grouping tests (R11)."""

from pipeline.normalize import clean_rows, group_duplicates, to_clean_event


def _raw(source: str, ref: str, payload: dict) -> dict:
    return {"source": source, "source_ref": ref, "content_hash": "h" * 64, "payload": payload}


def test_html_row_is_cleaned() -> None:
    raw = _raw(
        "site-a",
        "https://a.example.com/e1",
        {
            "title": " Sahne Gecesi ",
            "starts_at": "12.11.2026 20:00",
            "location": "Kültür Merkezi",
            "price": "250 TL",
        },
    )
    event = to_clean_event(raw)
    assert event is not None
    assert event.title == "Sahne Gecesi"
    assert event.starts_at.hour == 20
    assert event.price_minor == 25000
    assert event.currency == "TRY"
    assert event.venue_name == "Kültür Merkezi"


def test_jsonld_row_keeps_geo_and_offer() -> None:
    raw = _raw(
        "jsonld",
        "https://b.example.com/e2",
        {
            "title": "Bahçe Konseri",
            "starts_at": "2026-11-12T20:00:00+03:00",
            "location": {
                "@type": "Place",
                "name": "Bahçe",
                "geo": {"latitude": "41.0082", "longitude": "28.9784"},
            },
            "offers": {"price": "0", "priceCurrency": "TRY"},
        },
    )
    event = to_clean_event(raw)
    assert event is not None
    assert (event.lat, event.lon) == (41.0082, 28.9784)
    assert event.price_minor == 0


def test_rss_row_without_event_date_is_dropped() -> None:
    raw = _raw("rss", "https://c.example.com/e3", {"title": "Duyuru", "published_at": "x"})
    clean, dropped = clean_rows([raw])
    assert clean == [] and dropped == 1


def test_same_event_from_two_sources_is_grouped() -> None:
    base = {"starts_at": "2026-11-12T20:00:00+03:00"}
    geo = {"name": "Kültür Merkezi", "geo": {"latitude": 41.0082, "longitude": 28.9784}}
    rows = [
        _raw("s1", "r1", {**base, "title": "Sahne Gecesi", "location": geo}),
        _raw("s2", "r2", {**base, "title": "SAHNE GECESİ", "location": geo}),
        _raw("s3", "r3", {**base, "title": "Tamamen Başka", "location": geo}),
    ]
    clean, _ = clean_rows(rows)
    groups = group_duplicates(clean)
    assert sorted(len(g) for g in groups) == [1, 2]
