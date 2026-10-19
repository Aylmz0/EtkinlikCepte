import hashlib
import json
from datetime import datetime
import feedparser
import dramatiq


@dramatiq.actor
def fetch_rss_feed(source_name: str, feed_url: str):
    """
    Belirtilen RSS/Atom kaynağından verileri çeker, content_hash üretir
    ve ham payload'ı hazırlar (Veritabanı yazması H2.8'de eklenecektir).
    """
    print(f"[{datetime.utcnow()}] Kaynak taranıyor: {source_name} ({feed_url})")

    feed = feedparser.parse(feed_url)
    raw_events = []

    for entry in feed.entries:
        # Alanların çıkarılması
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        published = entry.get("published", datetime.utcnow().isoformat())
        summary = entry.get("summary", "").strip()

        # Ham payload oluşturma
        payload = {
            "source": source_name,
            "source_ref": link,
            "title": title,
            "published_at": published,
            "summary": summary
        }

        # Değişim takibi için content_hash üretimi (SHA-256)
        payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        content_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

        raw_event = {
            "source": source_name,
            "source_ref": link,
            "content_hash": content_hash,
            "payload": payload
        }
        raw_events.append(raw_event)

    print(f"-> {source_name}: {len(raw_events)} kayıt başarıyla çekildi ve hash'lendi.")
    return raw_events


if __name__ == "__main__":
    # Test amaçlı örnek çalıştırma (Veritabanı bağımlılığı yok)
    test_feeds = [
        ("ornek_kultur_sanat", "https://example.com/rss/events"),  # Kendi seçeceğin RSS 1
        ("ornek_etkinlik", "https://example.org/feed")  # Kendi seçeceğin RSS 2
    ]
    for name, url in test_feeds:
        # Doğrudan fonksiyon çağrısı ile test edebilirsin
        pass
