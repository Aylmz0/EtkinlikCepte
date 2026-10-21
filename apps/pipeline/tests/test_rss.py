"""RSS adapter fixture test: parse, normalize fields, hash deterministically."""

from pipeline.sources.rss import parse_feed

FEED = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Örnek Etkinlikler</title>
    <item>
      <title>Bahçe Konseri</title>
      <link>https://example.com/events/bahce-konseri</link>
      <pubDate>Mon, 06 Oct 2026 18:00:00 +0300</pubDate>
      <description>Akustik bir akşam.</description>
    </item>
  </channel>
</rss>
"""


def test_parse_feed_builds_stable_hash() -> None:
    """One entry becomes one raw row with a stable content hash."""
    rows = parse_feed(FEED, "example")
    assert len(rows) == 1
    row = rows[0]
    assert row["source"] == "example"
    assert row["source_ref"] == "https://example.com/events/bahce-konseri"
    assert row["payload"]["title"] == "Bahçe Konseri"
    assert len(row["content_hash"]) == 64

    again = parse_feed(FEED, "example")
    assert again[0]["content_hash"] == row["content_hash"]
