# P4 — Umut Can Kuş — Keşif ve öneri

**Alan (sabit, §6):** Mekan/etkinlik arama, coğrafi sorgu, sıralama. Çıktıların: keşif akışı, mesafe sorguları, şeffaf skor. ML yok (D1). 7 hafta bu kavramdasın.
**Buddy:** P6 (§6.2). **Lider haftan:** H4.

## Envanterin

- **Tablolar (§7):** `venues` (POINT 4326, GIST), `events` (okuma), `ranking_weights` (senin), `user_event_stats` (Faz 2 şeması), `club_followers` (w6 girdisi).
- **Uçlar (§8):** `GET /discover/venues?bbox=&category=`, `GET /discover/events?lat=&lng=&radius=&category=&when=&price=`, `GET /discover/recommendations`.
- **Skor (§9):** w1 mesafe (2 km→1.0, 20 km→0.0) + w2 kategori + w3 tazelik + w4 popülerlik (log) + w5 fiyat + w6 takip (en güçlü sinyal). Ağırlıklar yönetim ekranından ayarlanır (§9).
- **Harita (§1.4):** mavi/gri/yeşil halka; rozetler: kulüp rozeti / collected işareti.
- **Altyapın:** Nominatim self-host (§2, §4.3), Martin/PMTiles (hazır paket yok).

## H1 — Öğrenme haftan

- **H1.10 PostGIS eğitimi (2 gün).** Kabul: eğitim tamam. Prototip sorgusu H2.6'da yazılır (H1.4 önceki haftadan). Çıktı: H2.6.
- **H1.17 Nominatim self-host (P1 destekli).** Adımlar: 1. Compose profili + veri planı. 2. Veri yükleme H2.6 ile (H1.4 önceki haftadan). Kabul: profil PR'da; adres→koordinat H2.6'da kanıtlanır. Çıktı: H2.6, H3.11.

## H2 — Uç haftan

- **H2.6 Mesafe çekirdeği.** 200 aday sorgusu (H1 prototipi dahil: mesafe+kategori+tarih, §9 Aşama 1), GIST kullanımı. Kabul: 100k kayıtta süre notlu (hedef < 300 ms §11) + `EXPLAIN ANALYZE` çıktısı + Nominatim veri yüklemesi kanıtlı (adres→koordinat döner). Çıktı: P7 (H3.3/H3.5), H2.7/H2.16.
- **H2.7 Şeffaf skor v1.** w1–w6 + `ranking_weights` + Vitest skor testleri (§12: doğrulama, skor). Kabul: örnek çıktıda gerekçe cümlesi (§1.2: "bunu önerdik çünkü…").
- **H2.16 Keşif uçları.** venues bbox+kategori; events 6 filtre + Türkçe duyarsız arama (İ/i, ğ/ü/ş… kaçırmaz). Kabul: Hurl + süre notu.
- **H2.17 Recommendations.** Skor + rozet girdisi + weights okuma. Kabul: uç, 200'lük skorlu listeyi döner. Çıktı: P7 (H3.3).

## H3 — Kanıt haftan

- **H3.11 OSM/Overpass (P3 ile).** Senin payın: kategori eşleme + mesafe tutarlılığı (örnek mekanla başlar, kurallar yazılı). Kabul: örnekte doğru kategori; canlı veriye karşı doğrulama H6.11'de (H3.1 önceki haftalardan).
- **H3.12 Martin/PMTiles.** Kendi sunucudan üretim (§4.3); P7 tüketir. Kabul: paketler istemcide açılır.
- **H3.13 EXPLAIN + indeks raporu.** §7 kritik listesi satır satır. Kabul: rapor + < 300 ms kanıtı. Çıktı: H6.9.
- **H3.8-pay.** Keşif uçları tam Hurl kapsamlı.
- **H3.9-katılım.** Keşif ayağının durumu. Kabul: H3.13 raporu masada.

## H4 — Liderlik haftan (süreç sende, teknik P5'te)

- **H4.8 w6 kalibrasyonu.** `club_followers(user_id, created_at DESC)` indeksi (H3.7 verisiyle) + takip ağırlığı. Kabul: indeks var + örnek çıktıda w6 etkisi görünür.
- **Liderlik:** Cuma provası (H4 çıkışı) + H4 sonu 1 saat ara bakış (§6.2 ritüeli) + P5'e devir. Buddy P6'nın H4.7'si tıkanırsa ona öncelik verirsin.

## H5 — Karışım haftan

- **H5.14 Rozet mantığı.** `origin`/`trust` → kulüp rozeti / collected işareti (§1.4); P7 tüketir. Kabul: detayda rozet görünür.
- **H5.16 Akışa öneri karışımı.** Hedef: Akış sekmesi = takip edilen kulüp gönderileri + önerilen etkinlikler (§1.5). Adımlar: 1. `GET /feed` içine `recommendations` bölümü (P2'nin backend'ine ek, P2 ile pair). 2. "Öneri" etiketi zorunlu (§1.4: gerçek sanılmasın). Kabul: akışta etiketli öneri. Çıktı: H5 çıkışı.

## H6 — Optimizasyon haftan

- **H6.9 Keşif optimizasyonu.** H3.13 bulgularını kapat. Kabul: < 300 ms, 100k, raporlu.
- **H6.11 Coğrafi doğrulama + kategori eşleme.** shapely + OSM kategorileri + H3.11 kurallarının canlı veriye karşı doğrulaması. Kabul: eşleme tablosu dokümante.
- **H6.7-pay.** Keşif/öneri ADR payın.

## H7 — Prova

Keşif akışı (ara → filtrele → detay) + weights son gözden geçirmesi sende (H7.1 içinde).

## Risklerin

R6: yavaş sorguyu H2.7'de işaretle, H3.8'e süre testi ekle. D1/D6 yok: öğrenme sözü verme.
