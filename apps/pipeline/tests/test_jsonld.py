"""JSON-LD adapter fixture test: schema.org/Event is extracted and hashed."""

from pipeline.sources.jsonld import parse_jsonld

HTML = """<!doctype html><html><head>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Event","name":"Sahne Gecesi",
 "url":"https://example.com/events/sahne-gecesi",
 "startDate":"2026-11-12T20:00:00+03:00","endDate":"2026-11-12T22:00:00+03:00",
 "location":{"@type":"Place","name":"Kültür Merkezi"},
 "offers":{"@type":"Offer","price":"250","priceCurrency":"TRY"}}
</script></head><body></body></html>
"""


def test_parse_jsonld_event() -> None:
    """A schema.org Event block becomes one raw row."""
    rows = parse_jsonld(HTML, "example-jsonld")
    assert len(rows) == 1
    row = rows[0]
    assert row["source"] == "example-jsonld"
    assert row["payload"]["title"] == "Sahne Gecesi"
    assert row["payload"]["starts_at"].startswith("2026-11-12")
    assert len(row["content_hash"]) == 64
