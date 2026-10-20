# P3 — İsmail Can Kocaman — Data Engineer (Miner)

**Alan (sabit, §6 Ekip):** Kaynak adaptörleri, temizleme, tekrar eleme, veri kalitesi. Çıktıların: 4–6 kaynak, veri kalitesi panosu, `data-sources.md`. 7 hafta bu kavramdasın; P1 ile buddy'sin (§6.2 Çalışma kuralları).
**Buddy:** P1 (§6.2). **Lider haftan:** H3.

## Envanterin

Senin işin ham internet verisini güvenilir uygulama verisine çevirmek. Boru hattı şöyle akar: kaynaklardan topla (`sources/`) → başlık/tarih/fiyat/konumu temizle (`normalize/`) → tekrarları ele (`dedup/`) → mekânları doğrula (`geo/`) → yayınla. Hepsi `development.md`'de tanımlı; burası sadece senin listen:

- **Tablolar (§7 Veri modeli):** `source_events` (ham kayıt; GIST indeksi + unique `(source, source_ref)`), `event_sources` (birleştirme bağları; kaynak kaydı asla silinmez), `events` (`origin`: club/collected, `trust`: verified/collected), `venues`, `source_configs` (zamanlama, hız sınırı, user-agent, `terms_checked_at` ToS tarihi).
- **Sıra (§1.4 Veri kaynakları):** RSS/Atom → JSON-LD → HTML. Biletix, Bubilet vb.: her hedef site için `robots.txt` + kullanım koşulları kontrolü yapılır, tarih ve istek hızıyla `data-sources.md`'ye yazılır (§4.3 Veri kaynakları). Her bilgi tipi en az 2 farklı kaynaktan gelir.
- **Araçların (§3.3 Veri hattı):** Dramatiq + APScheduler (görev kuyruğu ve zamanlama), Scrapy 2.19 (toplama), parsel + lxml (HTML ayıklama), Playwright (JS ile yüklenen sayfalar), feedparser + extruct (RSS ve JSON-LD), rapidfuzz (benzerlik), shapely (coğrafi doğrulama), polars 2 (tablo işleme, Rust çekirdekli), faker (test verisi).
- **Dizinlerin (§5 Depo yapısı):** `apps/pipeline/src/pipeline/{sources,normalize,dedup,geo,rank}/`, `apps/pipeline/{tests/fixtures/,pyproject.toml}`.
- **Kuralın:** `content_hash` ile değişim takibi (aynı kayıt tekrar gelirse anlaşılır); `payload JSONB` ham saklanır; birleştirme kuralı = başlık benzerliği + aynı mekân + yakın tarih.

## H1 — İskelet (P1 ile)

Bu hafta iki sitenin robot iskeletini + izin evrakını çıkarıyorsun. Veritabanına yazmak yok — o H2'nin işi.

- **H1.9 İki adaptör iskeleti + `data-sources.md` v1.** **Adımlar:** 1. Dramatiq + APScheduler görev iskeleti (`schedule_cron` zamanlaması §7 Veri modeli). 2. Kullanım koşulları uygun 2 RSS kaynağı seç. 3. `source_events` yazma + `content_hash` üretme (veritabanına bağlama H2.8 başında yapılır, H1.3 önceki haftadan). 4. Kapı kontrol kaydını `data-sources.md`'ye işle. **Kabul:** iskeletler veritabanısız koşar (örümcek + ayrıştırma + örnek test). **Çıktı:** H2.8/H2.14/H2.15 adaptörleri bu iskeletlerden büyür.
- **H1.16 `source_configs` + admin iskeleti.** Kaynak ayarlarının (`GET /admin/sources`, `PATCH`, `POST …/run`) migration dosyası + uç taslakları §7 Veri modelinden yazılır (veritabanı beklenmez); çalıştırması H2.8'deki ilk `just migrate` ile yapılır (H1.3 onaylı revision). **Kabul:** revision + taslak PR açık. **Çıktı:** H3.11 mekân çekme ile H5.10 işletim işi buraya dayanır.

## H2 — Adaptör haftan

Üç toplama yöntemini de çalışır hale getiriyorsun. Sıra bilinçli: en güvenli yol önce, en kırılgan yol en sona.

- **H2.8 Scrapy + parsel HTML (2 hedef).** Sayfa okuma son çaredir çünkü sayfa tasarımı değişince bozulur (§1.4 Veri kaynakları). **Kabul:** önce `just migrate` (H1.3 + H1.16 revision'ları) yeşil, sonra `faker` test verisiyle test yeşil (R11: her adaptörün testi).
- **H2.14 RSS/Atom (feedparser).** Site yayınlıyorsa en güvenli yol, en temiz veri. **Kabul:** ToS kaydı `data-sources.md`'de + test yeşil.
- **H2.15 JSON-LD (extruct).** Sayfada `schema.org/Event` varsa başlık/tarih/mekân/fiyat hazır gelir; CSS seçiciye göre dayanıklıdır. **Kabul:** test + dayanıklılık notu (sayfa tasarımı değişse bile JSON-LD bozulmaz).

## H3 — Canlı haftan (lider sensin)

Bu hafta robotlar gerçek sitelere çıkar, harita gerçek veriyle dolar. Hafta liderliği de sende.

- **H3.1 Dört kaynak canlı.** 5 iskeletten olgunlaşan 4'ü yayına alınır; temizleme (tarih/fiyat/konum) + rapidfuzz/coğrafi tekrar eleme yapılır, sonuç `events` + `event_sources` tablolarına yazılır. **Kabul:** 100+ temiz kayıt. **Çıktı:** P7'nin H3.3–H3.6 ekranları ile P4'ün skor girdisi buradan beslenir.
- **H3.2 Pano v1.** Kaynak başına kayıt/kalite sayıları + `last_status` + beklenen/gerçekleşen denetimi (eksik kayıt loglanır, kayıp gizlenmez). **Kabul:** pano açılır.
- **H3.8-pay.** Kendi admin uçlarının Hurl testleri; başkasını beklemezsin. **Kabul:** yeşil.
- **H3.10 Dedup kuralları.** Eşikler yazılı belgede durur (benzerlik eşiği, mesafe toleransı) + polars tablo işleme (lazy frame §3.3 Veri hattı). **Kabul:** doküman + test.
- **H3.11 OSM/Overpass (P1 sunucu + P4 ile).** Senin payın: `venues` mekân verisini **örnek OSM kesiti/fikstür** üzerinden çekme + shapely doğrulama. Ağır sorgu ortamı P1'in H3.11-sunucu işinde kurulur; canlı sunucu sorgusu doğrulaması H6.11'de yapılır (H2.8/H2.14/H2.15 önceki haftadan). **Kabul:** fikstürden gri noktalar (etkinlik yapılabilir mekânlar §1.4) üretilir.
- **Liderlik:** "Gerçek veri akıyor mu" senkronunu yönetirsin; H3.9 değerlendirmesini yönetip P4'e devir notu yazarsın.

## H4 — Sağlamlaştırma haftan

- **H4.12 Fikstür + kota simülasyonu.** **Hedef:** §12 Test stratejisi kuralı — her kaynak kendi örneğiyle test edilir. **Adımlar:** 1. `tests/fixtures/` altına kaynakların HTML/RSS örneklerini koy (canlı 4 + iskeletler; H5.8'deki 2 yeni kaynağın örnekleri H5'te eklenir). 2. rate-limit + `robots.txt` red simülasyonu + AdaptiveDelay (429/5xx hatalarında 2 sn→60 sn arası bekleme, başarıda süre kısalır). 3. Yumuşak bekleme iddiası (R4) + transient ayrımı (DNS/429/5xx gibi geçici hatalar `retry_count` artırmaz). **Kabul:** pytest + fikstür yeşil. **Çıktı:** H5.8 bu testlere dayanır.
- Ayrıca: P4'ün skor sorularında C/danışılan konumundasın; sorarsa yanıtlarsın.

## H5 — Büyütme haftan

- **H5.8 İki ek kaynak (toplam 6).** Biri Playwright ile (JS ile yüklenen sayfalar §3.3 Veri hattı). **Kabul:** 6 kaynağın da kapı kontrolü (ToS + hız) kayıtlı.
- **H5.10 `source_configs` işletimi.** cron zamanlama + `rate_limit_rps` hız sınırı + user-agent + `POST /admin/sources/{id}/run` ile elle çalıştırma + checkpoint-resume (`last_run_at`ten devam eder) + düzgün kapanış (yarım kalan iş kaybolmaz). **Kabul:** zamanlanmış koşu log'lu.

## H6 — Gözlem haftan

- **H6.7-pay.** `data-sources.md` finali (6 kaynak eksiksiz, ToS tarihleriyle). **Kabul:** altı kaynağın da izin tarihi ve istek hızı yazılı.
- **H6.8 Profil çıkarımı.** Faz 2'deki öğrenen katmanın girdisi; iş hattında çalışır ve dokümantelidir (kapanış değil, devir işi). **Kabul:** küçük örnek veriyle uçtan uca koşar.
- **H6.10 Gözlemlenebilirlik.** `last_run_at`/`last_status` alanları, pano v2, işçi belleği (RSS) < 200 MB (§11 Performans hedefleri). **Kabul:** ölçüm raporlu.

## H7 — Veri kapanışı

- **H7.4 Seed + demo veri.** `just seed` (Türkiye, 3 şehir §15 Komutlar) + prova senaryosuna özel set (kulüp, etkinlik, biletli kullanıcı). **Kabul:** temiz veritabanından prova 10 dakikada hazır.
- **H7.1-pay.** Provada "gerçek veri" ayağı sende: kayıt yoksa ilk müdahale senin. **Kabul:** provada haritada temiz veri görünür.

## Risklerin

R11 (veri toplama tek kişide kalır): H1.9'da P1 ile pair çalışırsın + H2'de P4'e adaptör turu attırırsın (destek verir — §6 Ekip). R4 (kaynak koşul ihlali): kapı kontrolsüz kaynak yayına girmez; kanıt `data-sources.md`'dir.
