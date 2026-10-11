# P3 — Veri toplama

**Alan (sabit, §6):** Kaynak adaptörleri, temizleme, tekrar eleme, veri kalitesi. Çıktın: 4–6 kaynak, pano, `data-sources.md`. 7 hafta bu kavramdasın.
**Buddy:** P1 (§6.2). **Lider haftan:** H3.

## Envanterin

- **Tablolar (§7):** `source_events` (GIST + unique `(source, source_ref)`), `event_sources` (kaynak silinmez), `events` (`origin` club/collected, `trust` verified/collected), `venues`, `source_configs` (cron, rate-limit, user-agent, `terms_checked_at`).
- **Sıra (§1.4):** RSS/Atom → JSON-LD → HTML. Biletix, Bubilet vb. her hedefte `robots.txt` + ToS → `data-sources.md` (tarih + hız §4.3). Her bilgi tipi ≥ 2 kaynak.
- **Araçların (§3.3):** Dramatiq + APScheduler, Scrapy 2.19, parsel + lxml, Playwright, feedparser + extruct, rapidfuzz, shapely, polars 2, faker.
- **Dizinlerin (§5):** `apps/pipeline/src/pipeline/{sources,normalize,dedup,geo,rank}/`, `apps/pipeline/{tests/fixtures/,pyproject.toml}`.
- **Kuralın:** `content_hash` değişim takibi; `payload JSONB` ham; birleştirme = başlık + mekan + tarih.

## H1 — İskelet (P1 ile)

- **H1.9 İki adaptör iskeleti + `data-sources.md` v1.** Adımlar: 1. Dramatiq + APScheduler iskeleti (`schedule_cron` §7). 2. ToS izinli 2 RSS kaynağı seç. 3. `source_events` yazma + `content_hash`. 4. Kapı kontrolü kaydı. Kabul: iskeletler koşar. Çıktı: H2.8/H2.14/H2.15.
- **H1.16 `source_configs` + admin iskeleti.** Migration (P1 onayı) + `GET /admin/sources`, `PATCH`, `POST …/run` taslakları. Kabul: `openapi.json`'da görünür. Çıktı: H3.11, H5.10.

## H2 — Adaptör haftan

- **H2.8 Scrapy + parsel HTML (2 hedef).** En kırılgan yol en sona (§1.4). Kabul: `faker` testli (R11: her adaptörün testi).
- **H2.14 RSS/Atom (feedparser).** En güvenli yol önce. Kabul: ToS kaydı + test.
- **H2.15 JSON-LD (extruct).** `schema.org/Event` → başlık/tarih/mekan/fiyat. Kabul: dayanıklılık notu.

## H3 — Canlı haftan (lider sensin)

- **H3.1 Dört kaynak canlı.** 5 iskeletten olgun 4'ü; temizleme (tarih/fiyat/konum) + rapidfuzz/coğrafi dedup → `events` + `event_sources`. Kabul: 100+ temiz kayıt. Çıktı: P7 (H3.3–H3.6), P4 skor girdisi.
- **H3.2 Pano v1.** Kaynak başına kayıt/kalite + `last_status` + beklenen/gerçekleşen denetimi (eksik kayıt loglanır). Kabul: pano açılır.
- **H3.8-pay.** Admin uçlarının Hurl'ları. Kabul: yeşil.
- **H3.10 Dedup kuralları.** Eşikler yazılı (benzerlik, mesafe toleransı) + polars tablo işleme (lazy frame §3.3). Kabul: doküman + test.
- **H3.11 OSM/Overpass (P4 ile).** `venues` çekme + osm2pgsql aktarımı + shapely doğrulama; ağır sorgu kendi sunucudan (§4.3). Kabul: gri noktalar haritada (§1.4).
- **Liderlik:** "Gerçek veri akıyor mu" senkronu; H3.9'u yönet + P4'e devir.

## H4 — Sağlamlaştırma haftan

- **H4.12 Fikstür + kota simülasyonu.** Hedef: §12 "her kaynak kendi örneğiyle". Adımlar: 1. `tests/fixtures/`a kaynakların HTML/RSS örnekleri (canlı 4 + iskeletler; H5.8'deki 2 yeni kaynağınki H5'te eklenir). 2. rate-limit + `robots.txt` red simülasyonu + AdaptiveDelay (429/5xx'te 2sn→60sn backoff, başarıda decay). 3. Yumuşak bekleme iddiası (R4) + transient ayrımı (DNS/429/5xx `retry_count` artırmaz). Kabul: pytest + fikstür yeşil. Çıktı: H5.8'in güveni.
- Ayrıca: P4'ün skor sorularında C konumundasın.

## H5 — Büyütme haftan

- **H5.8 İki ek kaynak (toplam 6).** Biri Playwright (JS-render §3.3). Kabul: 6 kaynak kapı kontrollü.
- **H5.10 `source_configs` işletimi.** cron + `rate_limit_rps` + user-agent + `POST /admin/sources/{id}/run` + checkpoint-resume (`last_run_at`ten devam, graceful shutdown'ta yarım iş kaybolmaz). Kabul: zamanlanmış koşu log'lu.

## H6 — Gözlem haftan

- **H6.7-pay.** `data-sources.md` finali (6 kaynak eksiksiz).
- **H6.8 Profil çıkarımı.** Faz 2 girdisi; hatta çalışır + dokümante.
- **H6.10 Gözlemlenebilirlik.** `last_run_at`/`last_status`, pano v2, işçi RSS < 200 MB (§11). Kabul: ölçüm raporlu.

## H7 — Veri kapanışı

- **H7.4 Seed + demo veri.** `just seed` (Türkiye, 3 şehir §15) + prova senaryosuna özel set (kulüp, etkinlik, biletli kullanıcı). Kabul: temiz DB'den prova 10 dakikada hazır.
- **H7.1-pay.** "Gerçek veri" ayağı sende.

## Risklerin

R11: H1.9 pair + H2 turu P4'e attır. R4: kapı kontrolsüz kaynak yayına girmez; kanıt `data-sources.md`.
