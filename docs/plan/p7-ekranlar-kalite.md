# P7 — Ekranlar ve kalite

**Alan (sabit, §6):** Keşif/harita, etkinlik detayı, bilet cüzdanı, E2E testleri, sürüm. Çıktın: harita + filtre, detay, cüzdan, E2E paketi, imzalı APK. 7 hafta bu kavramdasın.
**Hat:** Ekranları P6 ile yazarsın. **Lider haftan:** H7 (demo sahibi).

## Envanterin

- **Ekranların (§1.6):** `/(tabs)/discover`, `FilterSheet`, `/events/[id]`, `/events/[id]/tickets`, `/(tabs)/tickets`, `/about`; ortak: `/scanner` (P2), `/(tabs)/feed` (P2), oda ekranı (P5).
- **Tükettiklerin:** `/discover/*` (P4), bilet uçları (P2), `api-client` (P1), `packages/ui` (P6), rozetler (P4 H5.14).
- **Cephanen (§12):** Vitest + happy-dom, openapi-ts + CI kayma kontrolü, Podman entegrasyon, Playwright (8 akış), adb + UI Automator (**3 akışla sınırlısın**), `ruff + svelte-check + eslint`.
- **Bütçelerin (§11):** ilk paket < 250 KB gzip, APK < 25 MB, açılış < 1.2 sn, bellek < 120 MB, 60 fps.
- **Sekmeler (§1.5):** Keşfet/Akış/Kulüpler/Biletler/Profil; mesajlar + bildirimler üst çubuk.

## H1 — Liste + iskelet haftan

- **H1.14 Ekran kilidi (P6 ile).** Kabul: 23 ekran + sahip donar.
- **H1.15 E2E iskeleti + APK doğrulama.** Adımlar: 1. Playwright (tarayıcıda, WebView'da değil §12). 2. 8 akışı yaz: kayıt→bilet, keşif→detay, kulüp→gönderi, sohbet, DM, davetiye, check-in, çevrimdışı bilet. 3. Telefon 3 akışını seç (değiştirme: konum izni, QR okutma, çevrimdışı cüzdan). 4. P6 APK'sını doğrula. Kabul: iskelet koşar. Çıktı: H4.13, H6.2.

## H2 — QA haftan

- **H2.21 Tasarım QA turu.** Hedef: H3 ekranları başlamadan erişilebilirlik ön denetimi. Adımlar: 1. `packages/ui` ilk bileşenlerinde focus tuzağı, klavye, ARIA (bits-ui §3.1). 2. 44px hedef + koyu mod + `tr.json` kontrolü (§16). 3. Bulguları P6'ya PR'la. Kabul: QA listesi kapandı. Çıktı: H3.3–H3.6'nın kalite zemini.
- Ayrıca: `api-client` v1'i P1'den erken al, tüketim provası yap.

## H3 — Harita haftan

- **H3.3 Keşif ekranı.** Mavi/gri/yeşil halka (§1.4) + MapLibre GL 6 + PMTiles 4 (§3.1); `EventCard` + `VenueMarker` + `FilterSheet` (tarih/konum/fiyat/kategori §1.2). Kabul: 60 fps hedefli, 1000+ satırda @tanstack/svelte-virtual (§11).
- **H3.4 Detay + bilet seçme.** "Şu kaynaklarda da listeleniyor" + dış bilet linki (§1.4: satmayız) + `GET /events/{id}/sources`. Açıklama metni: marked + DOMPurify (§3.1). Kabul: collected işareti görünür.
- **H3.5 Konum izni + yakınımdakiler.** Kabul: ret akışı testli (cihaz hakkı 1/3).
- **H3.6 `/about`.** OSM atfı (§4.3). Kabul: atıf görünür.
- **H3.15 İstemci provası (P6 ile).** `api-client` canlı API'ya uyar mı (§12 kayma kontrolü). Kabul: kayma yok.
- **H3.9-katılım.** Ekran ayağının durumu (§6.1 P7 satırı). Kabul: tablon hazır.

## H4 — Senaryo haftan

- **H4.13 E2E senaryo yazımı (4 akış).** Auth, keşif, bilet, sohbet senaryoları H1.15 iskeletine (kalan 4'ü H6.2'de). Kabul: 4 senaryo web'de koşar. Çıktı: H6.2.
- Ayrıca: P5'in H4.6'sına tutarlılık gözü (C konumun).

## H5 — Cüzdan haftan

- **H5.2 `/scanner` (P2 ile).** Kabul: gerçek QR cihaz provası (hak 2/3).
- **H5.3 Cüzdan + takvim.** `TicketRow` + `QRDisplay` + @internationalized/date (§3.1); grup biletleri (§7); çevrimdışı açılır (P6 kuyruğu). Kabul: internetsiz cüzdan (hak 3/3).
- **H5.4-ekran Takip akışı (P2 ile).** `PostCard` + beğeni; akış = takip edilenler (§1.5). Kabul: gönderi→beğeni provası.
- **H5.7-ekran Oda ekranı (P5 ile).** Aç/kapat, iz temizliği (§11). Kabul: çıkışta iz kapanır.

## H6 — Kapı haftan

- **H6.2 E2E 8 akış.** Web 8/8 + telefon 3/3 cihazda. Kabul: H6 çıkışı.
- **H6.3 Performans (P6 ile).** §11 satır satır rapor. Kabul: `perf-apk` yeşil.
- **H6.4 İmzalama (P1 ile).** Kabul: CI'dan imzalı APK.
- **H6.14 Paket bütçesi.** `build-web` + < 250 KB gzip; aşan PR durur (§11). Kabul: kural aktif.
- **H6.7-pay.** E2E raporu + §11 ölçüm tablosu docs'a (H6.3 kanıtları).

## H7 — Demo (lider sensin)

- **H7.2 Kayıt + README (koordine).** Kabul: kayıt + güncel `README` + mdBook derlemesi (`book.toml` + SUMMARY §3.4).
- **H7.1-prova.** Program + roller (herkes ayağının sahibi). R12: kayıt hazır.
- **Kapanış notu:** 10 satır — çıkan/çıkmayan + Faz 2 devri.

## Risklerin

R5 + §6.1: H3/H5 işlerin yarından azı biterse kesinti — H3.9'a tablon hazır. 3 cihaz hakkını değiştirme.
