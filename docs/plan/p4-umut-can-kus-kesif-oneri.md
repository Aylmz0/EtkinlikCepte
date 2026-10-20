# P4 — Umut Can Kuş — Backend Engineer, Discovery & Ranking

**Alan (sabit, §6 Ekip):** Mekan/etkinlik arama, coğrafi sorgu, sıralama. Çıktıların: keşif akışı, mesafe sorguları, şeffaf skor. ML (makine öğrenmesi) yok (D1 kesinti). 7 hafta bu kavramdasın.
**Buddy:** P6 (§6.2 Çalışma kuralları eşleşmesi). **Lider haftan:** H4.

## Envanterin

Senin işin "yakınımda ne var" sorusunu milisaniyeler içinde cevaplamak. Coğrafi aday üretimi veritabanında olur, skor şeffaftır (kullanıcı neden önerildiğini görür §1.2 Uygulama):

- **Tablolar (§7 Veri modeli):** `venues` (POINT 4326 koordinat, GIST coğrafi indeks), `events` (salt okuma), `ranking_weights` (senin tablon: ağırlıklar kodda değil burada), `user_event_stats` (Faz 2 şeması, şimdi değil), `club_followers` (w6 takip sinyalinin girdisi).
- **Uçlar (§8 API sözleşmesi):** `GET /discover/venues?bbox=&category=`, `GET /discover/events?lat=&lng=&radius=&category=&when=&price=`, `GET /discover/recommendations`.
- **Skor (§9 Öneri motoru):** w1 mesafe (2 km'de 1.0 → 20 km'de 0.0, doğrusal) + w2 kategori + w3 tazelik + w4 popülerlik (log ölçek) + w5 fiyat + w6 takip (en güçlü sinyal: takip etmek tıklamaktan güçlüdür). Ağırlıklar yönetim ekranından ayarlanır (§9).
- **Harita (§1.4 Veri kaynakları):** mavi (etkinlik var), gri (yapılabilir ama boş), yeşil halka (senin kulübün); rozetler: kulüp rozeti / collected işareti.
- **Altyapın:** Nominatim self-host adres→koordinat servisi (§2 Mimari, §4.3 Veri kaynakları), Martin/PMTiles harita paketi doğrulama (dışarıdan hazır paket yok).

## H1 — Öğrenme haftan

- **H1.10 PostGIS eğitimi (2 gün).** Coğrafi sorguları öğrenirsin. Kabul: eğitim tamam. Prototip sorgusu H2.6'da yazılır (H1.4 önceki haftadan). Çıktı: H2.6.
- **H1.17 Nominatim self-host (P1 destekli).** Adresleri koordinata çeviren servis kendi sunucumuzda çalışır (dış servise bağımlı kalınmaz §4.3 Veri kaynakları). **Adımlar:** 1. Compose profili + veri planı. 2. Veri yükleme H2.6 ile yapılır (H1.4 önceki haftadan). **Kabul:** profil PR'da; adres→koordinat dönüşü H2.6'da kanıtlanır. **Çıktı:** H2.6 mesafe işi ile H3.11 mekân çekme buraya dayanır.

## H2 — Uç haftan

- **H2.6 Mesafe çekirdeği.** 200 aday sorgusu (H1 prototipi dahil: mesafe+kategori+tarih penceresi, §9 Öneri motoru Aşama 1), GIST indeksi kullanılır. **Kabul:** 100 bin kayıtta süre notlu (hedef < 300 ms §11 Performans hedefleri) + `EXPLAIN ANALYZE` çıktısı + Nominatim veri yüklemesi kanıtlı (adres→koordinat döner). **Çıktı:** P7'nin H3.3 harita ve H3.5 yakınımdakiler ekranları ile H2.7 skor ve H2.16 uçları buradan beslenir.
- **H2.7 Şeffaf skor v1.** w1–w6 ağırlıkları + `ranking_weights` tablosu + Vitest skor testleri (§12 Test stratejisi: doğrulama ve skor testleri). **Kabul:** örnek çıktıda gerekçe cümlesi görünür (§1.2 Uygulama: "bunu önerdik çünkü…").
- **H2.16 Keşif uçları.** venues tarafı bbox+kategori; events tarafı 6 filtre (konum, yarıçap, kategori, zaman, fiyat) + Türkçe duyarsız arama (İ/i, ğ/ü/ş harfleri sonucu kaçırmaz). **Kabul:** Hurl testleri + süre notu yeşil.
- **H2.17 Recommendations.** Skor + rozet girdisi + weights okuma birleşir. **Kabul:** uç, 200'lük skorlu listeyi döner. **Çıktı:** P7'nin H3.3 keşif ekranı buradan beslenir.

## H3 — Kanıt haftan

Bu hafta "çalışıyor" demek yetmez, ölçümle kanıtlarsın.

- **H3.11 OSM/Overpass (P3 ile).** Senin payın: kategori eşleme + mesafe tutarlılığı (örnek mekanla başlar, kurallar yazılı). **Kabul:** örnekte doğru kategori; canlı veriye karşı doğrulama H6.11'de yapılır.
- **H3.12 Martin/PMTiles (P1 sunucu ile).** Paket üretimi P1'in H3.12-sunucu işinde; senin payın istemci tarafı: **statik örnek paket** ile harita katmanlarının açıldığını doğrula; sunucuda üretilen paketin canlı doğrulaması H6.11'de yapılır. **Kabul:** örnek paket istemcide açılır, katmanlar doğrulanır.
- **H3.13 EXPLAIN + indeks raporu.** §7 Veri modelindeki kritik indeks listesi satır satır elden geçer. **Kabul:** rapor + < 300 ms kanıtı hazır. **Çıktı:** H6.9 optimizasyonu bu rapora dayanır.
- **H3.8-pay.** Kendi keşif uçlarının Hurl kapsamı sende; başkasını beklemezsin. **Kabul:** yeşil.
- **H3.9-katılım.** Keşif ayağının durumu toplantıda sende. **Kabul:** H3.13 raporu masada.

## H4 — Liderlik haftan (süreç sende, teknik P5'te)

- **H4.8 w6 kalibrasyonu.** `club_followers(user_id, created_at DESC)` indeksi (H3.7 verisiyle) + takip ağırlığının ayarı. **Kabul:** indeks var + örnek çıktıda w6 etkisi görünür.
- **Liderlik:** Cuma provası yapılır (H4 çıkışı kanıtlanır) + H4 sonu 1 saat ara bakış (§6.2 Çalışma kuralları ritüeli) + P5'e devir notu yazarsın. Buddy P6'nın H4.7'si tıkanırsa ona öncelik verirsin.
- **H4.14 Arama kalitesi regresyon testleri.** **Hedef:** Türkçe karakterli aramalar (İ/i, ğ, ü, ş) ve filtre kombinasyonları H2.16 uçlarında doğru sonuç versin (önceki haftadan). **Adımlar:** 1. Örnek veri setiyle Türkçe arama senaryoları yaz. 2. Filtre kombinasyonlarının (kategori + tarih + fiyat) kesişimini test et. 3. Hurl'a kalıcı regresyon olarak ekle. **Kabul:** test seti yeşil, yanlış eşleşme yok. **Çıktı:** H5.16 akış karışımı bu doğrulanmış aramaya dayanır.

## H5 — Karışım haftan

- **H5.14 Rozet mantığı.** `origin`/`trust` alanları → kulüp rozeti / collected işareti (§1.4 Veri kaynakları); P7 tüketir. **Kabul:** detay ekranında rozet görünür.
- **H5.16 Akışa öneri karışımı.** **Hedef:** Akış sekmesi = takip edilen kulüplerin gönderileri + sana önerilen etkinlikler (§1.5 Kullanıcı görünümü). **Adımlar:** 1. `GET /feed` içine `recommendations` bölümü eklenir (P2'nin backend'ine ek olarak, P2 ile pair çalışırsın). 2. "Öneri" etiketi zorunlu (§1.4 Veri kaynakları: hesaplanmış içerik gerçek sanılmasın). **Kabul:** akışta etiketli öneri görünür. **Çıktı:** H5 çıkışına girer.

## H6 — Optimizasyon haftan

- **H6.9 Keşif optimizasyonu.** H3.13 bulgularını kapatırsın. **Kabul:** < 300 ms, 100 bin kayıt, raporlu.
- **H6.11 Coğrafi doğrulama + kategori eşleme.** shapely + OSM kategorileri + H3.11 kurallarının canlı veriye karşı doğrulaması + sunucuda üretilen PMTiles paketinin canlı doğrulaması (P1'in H3.11-sunucu/H3.12-sunucu ortamı, önceki haftalardan). **Kabul:** eşleme tablosu dokümante, canlı paket istemcide açılır.
- **H6.7-pay.** Keşif/öneri alanının ADR payını yazarsın.

## H7 — Prova

**H7.6 Weights son hali + keşif demo veri kontrolü.** Demo öncesi `ranking_weights` son değerleri kilitlenir, keşif akışı demo verisiyle prova edilir. **Kabul:** öneri gerekçeleri demoda görünür.
Keşif akışı provada sende (ara → filtrele → detay) + weights son gözden geçirmesi sende (H7.1 içinde).

## Risklerin

R6 (sunucu performansı): yavaş sorguyu H2.7'de işaretle, H3.8'e süre testi ekle. D1/D6 yok: öğrenme sözü verme, manuel ağırlıklarla savun.
