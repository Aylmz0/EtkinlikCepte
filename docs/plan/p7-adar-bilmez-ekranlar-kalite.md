# P7 — Adar Bilmez — Mobile UI Engineer & QA

**Alan (sabit, §6 Ekip):** Keşif/harita, etkinlik detayı, bilet cüzdanı, E2E testleri, sürüm. Çıktıların: harita + filtre, detay, cüzdan, E2E paketi, imzalı APK. Ekranları P6 ile birlikte yazarsın. 7 hafta bu kavramdasın.
**Hat:** Kalite kapısının ikinci bekçisisin (P6 ile). **Lider haftan:** H7 (demo sahibi: prova programı + kapanış notu sende).

## Envanterin

Senin işin kullanıcının gördüğü her şey + her şeyin kanıtı. Ekran listesi H1.14'te kilitlendi, sonrası değişiklik PR ister:

- **Ekranların (§1.6 Ekran listesi):** `/(tabs)/discover`, `FilterSheet`, `/events/[id]`, `/events/[id]/tickets`, `/(tabs)/tickets`, `/about`; ortak: `/scanner` (P2 ile), `/(tabs)/feed` (P2 ile), oda ekranı (P5 ile).
- **Tükettiklerin:** `/discover/*` uçları (P4 yazar), bilet uçları (P2 yazar), `api-client` tipleri (P1 üretir), `packages/ui` bileşenleri (P6 paketler), rozet mantığı (P4 H5.14 yazar).
- **Cephanen (§12 Test stratejisi):** Vitest + happy-dom (birim), openapi-ts + CI kayma kontrolü (sözleşme), Podman compose (entegrasyon), Playwright (8 web akışı), adb + UI Automator (**3 telefon akışıyla sınırlısın**, H1'de seçilir H6'da değiştirilmez), `ruff + svelte-check + eslint` (kalite kapısı).
- **Bütçelerin (§11 Performans hedefleri):** ilk paket < 250 KB gzip, APK < 25 MB, açılış < 1.2 sn, bellek < 120 MB, 60 fps kaydırma.
- **Sekmeler (§1.5 Kullanıcı görünümü):** Keşfet/Akış/Kulüpler/Biletler/Profil; mesajlar ve bildirimler üst çubuktan açılır (altı sekme yapılmadı: parmak erişimi zorlaşırdı).

## H1 — Liste + iskelet haftan

- **H1.14 Ekran kilidi (P6 ile).** 23 ekran + sahibi §1.6 Ekran listesinden dondurulur. **Kabul:** liste donar, sonrası değişiklik PR ister.
- **H1.15 E2E iskeleti + akış listesi.** **Adımlar:** 1. Playwright kur (tarayıcıda koşar, telefonun WebView katmanında değil §12 Test stratejisi). 2. 8 akışın iskeletini yaz (içi boş: kayıt→bilet, keşif→detay, kulüp→gönderi, sohbet, DM, davetiye, check-in, çevrimdışı bilet; içleri H4.13/H6.2'de dolar). 3. Telefon 3 akışını seç (değiştirme kuralı: konum izni, QR okutma, çevrimdışı cüzdan). **Kabul:** iskelet koşar (APK doğrulama P6'nın H1.12'sinde yapılır; senin işin değil). **Çıktı:** H4.13 senaryoları ile H6.2 paketi buraya dayanır.

## H2 — QA haftan

- **H2.21 Tasarım QA turu.** **Hedef:** H3 ekranları başlamadan erişilebilirlik ön denetimi yapılır. **Adımlar:** 1. `packages/ui` ilk bileşenlerinde focus tuzağı, klavye navigasyonu, ARIA rolleri denetle (bits-ui §3.1 Mobil yığın). 2. 44px dokunma hedefi + koyu mod + `tr.json` (+`en.json`) metin kontrolü (§16 Bitti tanımı). 3. Bulguları P6'ya PR'la. **Kabul:** QA listesi kapandı + H3 ekranları için mock veri seti hazır. **Çıktı:** H3.3–H3.6 ekranları bu denetimden geçmiş bileşenlerle başlar.
- Ayrıca: `api-client` v1'i P1'den erken alıp tüketim provası yaparsın.

## H3 — Harita haftan

Bu hafta uygulamanın vitrini çıkar: harita, detay, cüzdan değil — harita, detay, atıf. (Cüzdan H5'te.)

- **H3.3 Keşif ekranı.** Mavi (etkinlik var) / gri (yapılabilir ama boş) / yeşil halka (senin kulübün) pin'leri (§1.4 Veri kaynakları) + MapLibre GL 6 + PMTiles 4 (§3.1 Mobil yığın); `EventCard` + `VenueMarker` + `FilterSheet` (tarih/konum/fiyat/kategori §1.2 Uygulama). **Kabul:** 60 fps hedefli, 1000+ satırda @tanstack/svelte-virtual (§11 Performans hedefleri); veri H3.1'den gelene kadar mock kullanılır (H3.15 provasıyla kilitlenir).
- **H3.4 Detay + bilet seçme.** "Şu kaynaklarda da listeleniyor" başlığı + dış bilet sitesi linki (§1.4 Veri kaynakları: ProjectX bilet satmaz, satan siteye yönlendirir) + `GET /events/{id}/sources`. Açıklama metni: marked + DOMPurify ile güvenli gösterim (§3.1 Mobil yığın). **Kabul:** collected işareti görünür.
- **H3.5 Konum izni + yakınımdakiler.** **Kabul:** izin ret akışı testli (3 cihaz hakkından ilki).
- **H3.6 `/about`.** OSM kaynak atfı (§4.3 Veri kaynakları: atıf uygulamada görünür). İçerik H3.1 verisinden gelir; taslakla başlanır. **Kabul:** atıf görünür.
- **H3.15 İstemci provası + bağlama (P6 ile).** `api-client` canlı API'ya uyar mı (§12 Test stratejisi kayma kontrolü) + auth'lu ekran bağlama (H2.1/H2.3 önceki haftalardan). **Kabul:** kayma yok, bağlı ekranlar yeşil.
- **H3.9-katılım.** Ekran ayağının durumu toplantıda sende (§6.1 Değerlendirmedeki P7 satırın: işlerin yarısından azı biterse kesinti gündeme gelir). **Kabul:** tablon hazır.

## H4 — Senaryo haftan

- **H4.13 E2E senaryo yazımı (4 akış).** Auth, keşif, bilet senaryoları H1.15 iskeletine yazılır (önceki haftaların backend'lerine karşı test edilir) + sohbet senaryo iskeleti (koşması H6.2'de). **Kabul:** 3 senaryo web'de koşar + sohbet iskeleti hazır. **Çıktı:** H6.2 paketi buraya dayanır.
- Ayrıca: P5'in H4.6 ekranlarına tutarlılık gözüyle bakarsın (C/danışılan konumun).

## H5 — Cüzdan haftan

- **H5.2 `/scanner` (P2 ile).** Mock QR akışıyla başlar. **Kabul:** mock akış yeşil; gerçek QR cihaz provası H6.16'da yapılır (hak 2/3).
- **H5.3 Cüzdan + takvim.** `TicketRow` + `QRDisplay` + @internationalized/date takvim (§3.1 Mobil yığın); grup biletleri (§7 Veri modeli: bir kullanıcı birden fazla bilet alabilir); çevrimdışı açılır (P6'nın kuyruğu sayesinde). **Kabul:** internetsiz cüzdan açılır (hak 3/3).
- **H5.4-ekran Takip akışı (P2 ile).** `PostCard` + beğeni; akış = takip edilen kulüplerin gönderileri (§1.5 Kullanıcı görünümü). **Kabul:** gönderi→beğeni provası yapılır.
- **H5.7-ekran Oda ekranı (P5 ile).** Oda açma/kapama + iz temizliği testli (§11 Performans hedefleri: izler katmandan çıkarken kapatılır). **Kabul:** çıkışta iz kapanır.

## H6 — Kapı haftan

- **H6.2 E2E 8 akış.** Web'de 8/8 + telefonda 3/3, gerçek cihazda. **Kabul:** 8/8 web + 3/3 cihaz yeşil (H6 çıkışı budur).
- **H6.3 Performans (P6 ile).** §11 Performans hedefleri satır satır raporlanır. **Kabul:** `just perf-apk` yeşil.
- **H6.4 İmzalama (P1 ile).** **Kabul:** CI'dan imzalı APK iner.
- **H6.14 Paket bütçesi.** `build-web` + ilk paket < 250 KB gzip; hedefi aşan PR CI'da durdurulur (§11 Performans hedefleri). **Kabul:** kural CI'da aktif.
- **H6.7-pay.** E2E raporu + §11 ölçüm tablosunu docs'a yazarsın (H6.3 kanıtlarıyla).

## H7 — Demo (lider sensin)

- **H7.2 Kayıt + README (koordine).** **Kabul:** ekran kaydı + güncel `README` + mdBook derlemesi (`book.toml` + SUMMARY §3.4 Araçlar).
- **H7.1-prova.** Prova programı + rol dağılımı yaparsın (herkes kendi ayağının sahibi). R12 kuralı: kayıt önceden hazırdır, canlı demoya güvenilmez.
- **Kapanış notu:** 10 satır — çıkan/çıkmayan işler + Faz 2'ye devredenler.

## Risklerin

R5 (ekran işi yetişmez) + §6.1 Değerlendirme: H3/H5 işlerin yarısından azı biterse kesinti gündeme gelir — H3.9'a tablon hazır. 3 cihaz hakkını seçtikten sonra değiştirme.
