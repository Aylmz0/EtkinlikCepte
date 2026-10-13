# EtkinlikCepte — Ana Plan (7 hafta, v3)

**Kaynak:** `development.md` + ADR-0001/0011. Kapsam kararları `development.md` §4 Kapsam kararları'tedir; çelişmede o geçerlidir.
**Kural:** Herkes §6 Ekip alanıyla başlar, 7 hafta boyunca aynı kavramda ilerler. Alan değişimi yok.
**Süre notu:** `development.md` §10 Takvim (15 hafta) 7 haftaya sıkıştırıldı; düşenler 3. bölümde.
**Bitirme disiplini:** Proje H7'de biter. H6 kapısı eksiksiz geçilmeden H7'ye geçilmez; H7'ye kalan iş yalnızca H7.1 listesidir. Faz 2'ye devredenler H7 kapanış notunda yazılır, sessizce sarkmaz.

## Nasıl okunur

Bu dosya **genel orkestrasyondur**: hiyerarşi, ritüel, kavram haritası, kesinti listesi, kritik yol, haftalık hedef/çıkış ve lider rotası. **Görev detayı (adım, dosya, komut, kabul) kişisel dosyalardadır.** ID'ler (`H<hafta>.<sıra>`) her iki tarafta aynıdır; aşağıdaki endeks ana kayıttır.

**Referanslar nasıl okunur:** `§4.8 Bildirim` demek, `development.md` 4.8. bölümdeki bildirim kuralları demek. `H3.1` planın 3. hafta 1. görevi, `R9` 14. bölümdeki 9. risk, `D4` 3. bölümdeki düşen 4. iş demek. Hepsi parantez içinde yazar; numara tek başına durmaz.

## 1. Hiyerarşi

| Katman | Kim | Yetki |
|---|---|---|
| Teknik lider (kalıcı) | P1 | `/v1` bozma, şema ve göç onayı (§6.2 Çalışma kuralları, §8.1 Sözleşme kuralları). Teknik konularda son söz. |
| Hafta lideri (dönüşümlü) | H1 P1 → H2 P2 → H3 P3 → H4 P4 → H5 P5 → H6 P6 → H7 P7 | Süreç: 30' senkron, tıkanıklık takibi, cuma çıkış kontrolü, devir notu. Teknik karara karışmaz. |
| Alan sahibi | Herkes kendi §6 Ekip alanında | İşinin `A/R`'si (§6.3 Sorumluluk matrisi). Başkasının alanına kod yazmaz. |

**Eşleşme çiftleri (§6.2 Çalışma kuralları):** P1-P3, P2-P5, P4-P6. P7 ekran hattında P6 ile çalışır.
**Ritüeller (§6.2 Çalışma kuralları):** Haftalık 30' senkron (pazartesi) · H3 sonu değerlendirme + H4 sonu ara bakış + H7 demo · trunk-based, branch ≤ 3 gün · PR tek konu ≤ 400 satır, CI yeşil, bir onay · şemada P1 onayı şart · `src-tauri/` yalnızca P6 · dil: kod İngilizce, kullanıcı metni `tr.json` · sürüm: `mise.toml` · her şey `just` ile · bitti tanımı §16 Bitti tanımı.
**Devir notu (cuma, ≤10 satır):** çıkış tuttu mu + eksik; devreden ID + sahip; tıkanıklık + çözücü; sonraki lidere tek öneri.

## 2. Kavram haritası

| Kişi | Kavram (§6 Ekip) | Çekirdek envanter |
|---|---|---|
| P1 · Tech Lead (Abdullah Yılmaz) | Sözleşme, şema, auth, sunucu | `users`, `refresh_tokens`, `devices`, `audit_log`, göçler; Kimlik/Sistem uçları; `api-client` üretimi; CI; imzalama |
| P2 · Backend, Ticketing & Social (Eren Yığmatepe) | Kulüp, etkinlik, bilet, QR, metin-sosyal | `clubs`, `club_members`, `events`, `event_tickets`, `registrations`, davetiyeler, takipçilik, gönderiler, beğeni, raporlar; Kulüp/Etkinlik/Bilet/Davetiye/Akış uçları; `ClubBadge`, `PostCard`, `PostComposer`, `FollowButton`, `TicketRow`, `QRDisplay` |
| P3 · Data Engineer, Miner (İsmail Can Kocaman) | Veri toplama | `source_events`, `event_sources`, `source_configs`, `venues`; Dramatiq/APScheduler, Scrapy/parsel, Playwright, feedparser/extruct, rapidfuzz, shapely; `data-sources.md`, pano |
| P4 · Backend, Discovery & Ranking (Umut Can Kuş) | Keşif ve öneri | `venues`, `ranking_weights`; `/discover/*`; şeffaf skor w1–w6; Nominatim self-host; Martin/PMTiles doğrulama |
| P5 · Backend, Realtime & Media (Cevat) | Sohbet ve medya | `chat_channels/members/messages`, `media_rooms`, `notifications`, `devices`; Sohbet/DM/Oda/Bildirim uçları, `/ws`; 5 ekran + 4 bileşen; LiveKit |
| P6 · Mobile, Core & Design System (Abdullah Hilal) | Uygulama çekirdeği | `apps/mobile` iskelet/nav/cache, `packages/ui`, `src-tauri` (200 satır tavan), deep-link/`geo:`, `ssr=false`, plugin-updater |
| P7 · Mobile UI & QA (Adar Bilmez) | Ekranlar ve kalite | discover/detay/cüzdan/`about` + ortak ekranlar; E2E (8 web + 3 cihaz); paket bütçesi; imzalı APK |

Kurallar: para kuruş + `TRY`, zaman UTC ISO-8601, hata RFC 9457, bilet/mesaj yazmalarında `Idempotency-Key` (§8.1 Sözleşme kuralları).

## 3. Kapsam: düşenler (§6.1 Değerlendirme sırası + ek)

D1 Öneri ML 3. aşama (Faz 2'ydi) · D2 Gönderi fotoğrafı (metin çalışır) · D3 Yorumlar (beğeni çalışır) · D4 Ekran paylaşımı web · D5 Ekran-paylaşımı bağlamında belge/bağlantı (kapsamda kalan: sohbet dosya eki H5.11 + oda dosya paylaşımı §1.2 Uygulama) · D6 `POST /recommendations/feedback` (model yok).
**Korunan çekirdek:** takipçilik, metin gönderi, sohbet, DM, bilet/QR.
**H3-sonu gerideyse ikinci dalga:** online akış → moderasyon (sade) → takvime ekleme → pano v2.
**Faz 2'ye kalanlar (7 haftada yok):** ML Aşama 3 (D1), `POST /recommendations/feedback` (D6), schemathesis fuzz (§12 Test stratejisi).

## 4. Kritik yol

1. **Şema → API → istemci:** H1.3 → H2 backend'leri → H2.12 → H3 ekranları.
2. **Veri → harita:** H1.9 → H2.8/H2.14/H2.15 → H3.1 → H3.3–H3.6. ToS'suz kaynak yayına girmez (§4.3 Veri kaynakları).
3. **Medya:** H1.11 → H4.1–H4.4 → H5.7. Port işi H4'te kapanır (R9).
4. **Kabuk:** H1.12 → H2.9 → H4.5/H4.9 → H6.1. Rust 200 tavan.
5. **Kalite:** H1.6 → H1.15 → H3.8 → H6.2 → H6.4.

## 5. Haftalar (hedef + çıkış + doğrulama)

- **H1 Temeller (P1):** İskeletler + `/v1` donar + ekran listesi kilitlenir. Çıkış: imzasız APK (`just android-apk`), `just dev` tüm servisler, `/openapi.json` 200. Sıra: P1 iskelet (H1.1/H1.2/H1.4) + P6 denemesi (H1.12) → P2/P3/P4/P5 işleri → H1.15 doğrulama.
- **H2 Çekirdek (P2):** Auth, kulüp/etkinlik/bilet API'leri, kabuk + giriş ekranları, `api-client` v1. Çıkış: giriş → kulüp → etkinlik → bilet al (gerçek API). Sıra: P1 auth (H2.1) + P2 uçlar (H2.3–H2.5) → ekranlar (H2.9/H2.11) + H2.12 üretim.
- **H3 Veri + harita (P3):** 4 kaynak canlı, pano, harita/detay/atfı ekranları, takipçilik, Hurl %60, H3-sonu değerlendirme. Çıkış: gerçek harita + 100+ temiz kayıt. Sıra: P3 canlı veri (H3.1) → P7 ekranları (mock'la başlar). H3.8/H3.9 en sonda.
- **H4 Sohbet + medya (P4):** WS, presence, LiveKit, DM, bildirim/deep-link, 5 ekran. Çıkış: 2 kişi yazışır + 3. katılır + ses; DM + arama (cuma provası). Sıra: P5 içi H4.1 → H4.2/H4.4 → H4.6; H4.5/H4.7/H4.9/H4.10–H4.13 bağımsız paralel, kişiler arası bekleme yok.
- **H5 Topluluk (P5):** Davetiye/QR, check-in, cüzdan, gönderi/akış, beğeni, moderasyon, online akış, staging HTTPS. Çıkış: gönderi → beğeni; QR davet kabul; cüzdan açılır. Sıra: P2 davetiye API (H5.1) → H5.2/H5.12; gerisi paralel.
- **H6 Sıkılaştırma (P6):** Eşitleme/çakışma, 8 E2E, perf, imza, güvenlik, yük+maliyet, docs finali. Çıkış: imzalı APK, 8 E2E yeşil, §11 Performans hedefleri tuttu (`just ci` + `just perf-apk`). Sıra: H6.1 → H6.3; H6.2 sürecinde; H6.4 en sonda (H6.2 sonrası). H6.5–H6.17 paralel.
- **H7 Demo (P7):** Prova + kayıt + README + §16/§18 Onay tablosu kapanış. Çıkış: baştan sona demo + imzalı APK + güncel doküman (R12: kayıt hazır).

## 6. Görev endeksi (ana kayıt: 103 ID)

### H1

| ID | İş | Sahip |
|---|---|---|
| H1.1 | Depo, `mise.toml`, `justfile` (+`just services` oxker), Podman | P1 |
| H1.2 | FastAPI iskeleti + OpenAPI v1 taslağı (uvloop/orjson/hiredis/psycopg havuzu, structlog) | P1 |
| H1.3 | DB şeması v1 + Alembic | P1 |
| H1.4 | Compose: postgres+postgis, valkey, caddy, martin | P1 |
| H1.5 | Hurl ilk 5 sözleşme testi | P2 |
| H1.6 | CI platformu kararı + boru hattı iskeleti (`deny.txt` ADR-0003 ile) | P1 |
| H1.7 | Bilet durum makinesi + QR format kararı | P2 |
| H1.8 | Kulüp/etkinlik router taslakları | P2 |
| H1.9 | 2 kaynak adaptörü iskeleti + `data-sources.md` v1 | P3 |
| H1.10 | PostGIS eğitimi + mesafe sorgu prototipi | P4 |
| H1.11 | LiveKit + Valkey denemesi + WS şema kararı | P5 |
| H1.12 | Node + SvelteKit + Tauri → APK denemesi + iskelet (Vite 8 + TS 7, `svelte.config.js`, `vite.config.ts`) | P6 |
| H1.13 | Tailwind + shadcn + IntelliSense + `tokens.css` | P6 |
| H1.14 | 23 ekran listesi kilidi | P6, P7 |
| H1.15 | E2E iskeleti + 8+3 akış listesi | P7 |
| H1.16 | `source_configs` şeması + `/admin/sources` iskeleti | P3 |
| H1.17 | Nominatim self-host kurulumu | P4 |

### H2

| ID | İş | Sahip |
|---|---|---|
| H2.1 | Auth: kayıt/giriş/jeton/argon2 | P1 |
| H2.2 | Profil + ilgi alanları | P1 |
| H2.3 | Kulüp/üyelik/roller API | P2 |
| H2.4 | Etkinlik CRUD + kayıt durum makinesi | P2 |
| H2.5 | Bilet tipleri + QR üretim | P2 |
| H2.6 | Mesafe endpoint çekirdeği | P4 |
| H2.7 | Şeffaf skor v1 (w1–w6, Vitest) | P4 |
| H2.8 | Scrapy + parsel HTML iskeleti | P3 |
| H2.9 | Tauri kabuk + nav + giriş/kayıt ekranları (formsnap/superforms/Zod) | P6 |
| H2.10 | `packages/ui` ilk bileşenler (sonner, lucide, Vitest) | P6 |
| H2.11 | Kulüp listesi/detay + profil + ayarlar | P6 |
| H2.12 | `api-client` v1 üretimi | P1 |
| H2.13 | SQLite okuma modeli başlangıcı | P6 |
| H2.14 | RSS/Atom adaptörü | P3 |
| H2.15 | JSON-LD adaptörü | P3 |
| H2.16 | `/discover/venues` + `/discover/events` | P4 |
| H2.17 | `/discover/recommendations` | P4 |
| H2.18 | LiveKit token uçları | P5 |
| H2.19 | Devices + bildirim API | P5 |
| H2.20 | Realtime istemci iskeleti | P5 |
| H2.21 | Tasarım QA turu | P7 |

### H3

| ID | İş | Sahip |
|---|---|---|
| H3.1 | 4 kaynak canlı + temizleme + dedup | P3 |
| H3.2 | Kalite panosu v1 | P3 |
| H3.3 | Keşif ekranı: harita/pin/filtre (MapLibre GL 6 + PMTiles 4, svelte-virtual) | P7 |
| H3.4 | Etkinlik detayı + bilet seçme (marked + DOMPurify açıklama) | P7 |
| H3.5 | Konum izni + yakınımdakiler | P7 |
| H3.6 | Kaynak atfı `/about` | P7 |
| H3.7 | Takipçilik API | P2 |
| H3.8 | Hurl %60 kapsam (pytest `services/`+`domain/` %90 §12 Test stratejisi) | P1, P2, P3, P4, P5 |
| H3.9 | H3-sonu değerlendirme | Tümü |
| H3.10 | Normalize + dedup kuralları | P3 |
| H3.11 | OSM/Overpass mekan çekme (osm2pgsql) | P3, P4 |
| H3.12 | Martin/PMTiles doğrulama (Protomaps basemap) | P4 |
| H3.13 | EXPLAIN + indeks raporu | P4 |
| H3.14 | WS sözleşme testleri + tip dokümanı | P5 |
| H3.15 | İstemci sözleşme provası | P6, P7 |
| H3.16 | Bildirim metinleri + rozet sayacı | P5 |
| H3.17 | Platform sarmalayıcılar + sahte veri | P6 |

### H4

| ID | İş | Sahip |
|---|---|---|
| H4.1 | WS sohbet | P5 |
| H4.2 | Presence + dağıtım | P5 |
| H4.3 | LiveKit odalar | P5 |
| H4.4 | DM backend | P5 |
| H4.5 | Bildirim + deep-link | P5, P6 |
| H4.6 | Sohbet/DM/oda/bildirim ekranları | P5 |
| H4.7 | Eşitleme kuyruğu devamı | P6 |
| H4.8 | w6 kalibrasyonu | P4 |
| H4.9 | Deep-link + `geo:` + SSR doğrulama | P6 |
| H4.10 | Sözleşme denetimi (WS/token uçları) | P1 |
| H4.11 | Kayıt/kapasite yarış testleri | P2 |
| H4.12 | Adaptör fikstürleri + kota simülasyonu | P3 |
| H4.13 | E2E senaryo yazımı (4 akış) | P7 |

### H5

| ID | İş | Sahip |
|---|---|---|
| H5.1 | Davetiye + QR okutma API | P2 |
| H5.2 | Kapıda doğrulama `/scanner` | P2, P7 |
| H5.3 | Bilet cüzdanı + takvim | P7 |
| H5.4 | Metin gönderi + akış (`GET /feed`) | P2, P7 |
| H5.5 | Beğeni | P2 |
| H5.6 | Moderasyon | P2 |
| H5.7 | Online etkinlik akışı | P5, P7 |
| H5.8 | 2 ek kaynak (toplam 6) | P3 |
| H5.9 | Eşitleme kuyruğu bitirme | P6 |
| H5.10 | `source_configs` işletimi | P3 |
| H5.11 | Sohbet dosya eki | P5 |
| H5.12 | P2 ekranları (davet/takip/gönderi) | P2 |
| H5.14 | Rozet mantığı | P4 |
| H5.15 | Staging HTTPS + secrets | P1 |
| H5.16 | Akışa öneri karışımı | P4 |

### H6

| ID | İş | Sahip |
|---|---|---|
| H6.1 | Eşitleme + çakışma çözümü | P6 |
| H6.2 | E2E 8 akış | P7 |
| H6.3 | Performans ölçümü | P6, P7 |
| H6.4 | İmzalama + sürüm hattı | P1, P7 |
| H6.5 | Güvenlik denetimi | P1 |
| H6.6 | Yük testi + maliyet raporu | P1 |
| H6.7 | ADR + `data-sources` + `runbook` finali (mdBook derlemesi) | Tümü |
| H6.8 | Veri hattı profil çıkarımı | P3 |
| H6.9 | Keşif optimizasyonu (< 300 ms) | P4 |
| H6.10 | Pipeline gözlemlenebilirlik | P3 |
| H6.11 | Coğrafi doğrulama + kategori eşleme | P4 |
| H6.12 | Presence ölçeği kanıtı | P5 |
| H6.13 | `plugin-updater` | P6 |
| H6.14 | Paket bütçe kapısı | P7 |
| H6.16 | QR/check-in regresyonu | P2 |
| H6.17 | İzleme + hata takibi (Grafana + Loki, GlitchTip) | P1 |

### H7

| ID | İş | Sahip |
|---|---|---|
| H7.1 | Demo provası + eksik kapatma | Tümü |
| H7.2 | Ekran kaydı + README finali | P7 |
| H7.3 | §16 Bitti tanımı kutuları + §18 Onay tablosu imzalar | P1 |
| H7.4 | Seed + demo veri seti | P3 |

## 7. Lider rotası

H1 P1 (kurulum + tebliğ + imzalar) · H2 P2 (sözleşme donması) · H3 P3 (veri + değerlendirme) · H4 P4 (medya provası + ara bakış) · H5 P5 (15 iş — zincirler) · H6 P6 (kapı: eksiksiz devretmeme) · H7 P7 (prova + kapanış notu: çıkan/çıkmayan + Faz 2).

## 8. Kişisel dosyalar

`p1-abdullah-yilmaz-teknik-lider-altyapi.md` (Abdullah Yılmaz) · `p2-eren-yigmatepe-kulup-etkinlik-bilet.md` (Eren Yığmatepe) · `p3-ismail-can-kocaman-veri-toplama.md` (İsmail Can Kocaman) · `p4-umut-can-kus-kesif-oneri.md` (Umut Can Kuş) · `p5-cevat-sohbet-medya.md` (Cevat) · `p6-abdullah-hilal-uygulama-cekirdegi.md` (Abdullah Hilal) · `p7-adar-bilmez-ekranlar-kalite.md` (Adar Bilmez)

## 9. Teknoloji × repo × sahip × hafta (`development.md` §3 Teknolojiler + §5 Depo yapısı tam kapsama)

`development.md`'deki her teknoloji/teknik unsur aşağıdaki satırlardan birindedir; boşta teknoloji yoktur.

| Teknoloji (§3 Teknolojiler) | Repo yolu (§5 Depo yapısı) | Sahip | Hafta |
|---|---|---|---|
| Tauri 2.12, Rust (~200 satır) | `apps/mobile/src-tauri/` | P6 | H1–H7 |
| SvelteKit 3 + Svelte 5, Vite 8 + TS 7 | `apps/mobile/` (`svelte.config.js`, `vite.config.ts`) | P6 | H1, H2 |
| Node 24 LTS + npm, `package.json` (kök workspace) | `/package.json`, `apps/mobile/package.json` | P6 (P1 `mise` pin'i) | H1 |
| Tailwind 4, `tokens.css`, `base.css`, `components.json` | `packages/ui/src/` | P6 | H1, H2 |
| bits-ui 2.19 (davranış) | npm + `packages/ui` tüketimi | P6 (P7 QA) | H2 |
| shadcn-svelte 1.7 (görünüm kopyaları) | `packages/ui/src/lib/components/ui/` | P6 | H2 |
| 13 özel parça (EventCard…VideoTile) | `packages/ui/src/lib/features/` | P6 (P2/P5/P7 tüketir) | H2–H5 |
| formsnap + superforms + Zod 4 | giriş/kayıt + gönderi/davet formları | P6 (H2.9), P2 (H5.12) | H2, H5 |
| svelte-sonner, @lucide/svelte | `packages/ui` (toast + ikon) | P6 | H2 |
| @tanstack/query 6, virtual 3 | `apps/mobile/src/lib/api/` | P6 (P5 H2.20, P7 H3.3) | H2, H3 |
| @internationalized/date | takvim ekleme (cüzdan) | P7 | H5 |
| marked + DOMPurify | etkinlik açıklaması (detay) | P7 | H3 |
| @jsquash/resize (WebP küçültme) | sohbet dosya eki istemcisi | P5 | H5 |
| MapLibre GL 6 + PMTiles 4 | keşif ekranı + Martin doğrulama | P7 (H3.3), P4 (H3.12) | H3 |
| livekit-client 2.22 | oda ekranı | P5 | H4 |
| Vitest + happy-dom | skor/store/bileşen testleri | P4 (H2.7), P6 (H2.10) | H2 |
| @playwright/test (web E2E) | E2E iskeleti + 8 akış | P7 | H1, H4, H6 |
| Python 3.13, uv, `pyproject.toml` | `apps/api/`, `apps/pipeline/` | P1 (pin), P2–P5 (kullanım) | H1 |
| FastAPI 0.142, Pydantic 2.13, `openapi.json` | `apps/api/app/{main.py,schemas,routers}` | P1 (+P2/P4/P5 router) | H1, H2 |
| Uvicorn + uvloop + orjson + hiredis + psycopg havuzu, structlog | `apps/api/app/core/` | P1 | H1 |
| SQLAlchemy (Core + ham SQL), Alembic göçleri | `apps/api/app/{repos,domain}` + `apps/api/alembic/` | P1 (+P2–P5 sorgu) | H1, H2 |
| PostgreSQL 17 + PostGIS 3.5 | `infra/compose*.yaml` | P1 (P4 sorgu) | H1 |
| Valkey 9 (cache/pub-sub/presence) | `infra/compose*.yaml` + `app/core/` | P1 (kurulum), P5 (kullanım) | H1, H4 |
| argon2-cffi, PyJWT | auth (`app/core/security/`) | P1 | H2 |
| `limits` (hız sınırı) | güvenlik denetimi | P1 | H6 |
| livekit-api (jeton), segno (QR) | `app/media/`, bilet uçları | P5 (H2.18), P2 (H2.5) | H2 |
| ruff + `ruff.toml`, eslint, svelte-check, Prettier + `.prettierrc` | CI `lint` + `just fmt` | Tümü (P1 kapı) | H1–H7 |
| k6 (500 okuma, p95 hedefleri) | yük testi + rapor | P1 | H6 |
| pip-audit, bandit, Trivy, gizli anahtar taraması | CI `audit` | P1 | H6 |
| `deny.txt` (ADR-0003) | CI `deny` | P1 | H1 |
| Hurl (sözleşme testleri) | `apps/api/hurl/` | P1–P5 | H1, H3 |
| pytest + pytest-asyncio (`services/`+`domain/` %90) | `apps/api/tests/` | P1, P2, P4, P5 | H2, H3 |
| Dramatiq + APScheduler, `source_configs` | `apps/pipeline/` + `/admin/sources` | P3 | H1–H6 |
| Scrapy 2.19, parsel + lxml 6.1 | `apps/pipeline/src/pipeline/sources/` | P3 | H2 |
| Playwright (JS-render), feedparser + extruct | aynı dizin | P3 | H2, H5 |
| rapidfuzz + coğrafi dedup, polars 2 | `.../normalize/`, `.../dedup/` | P3 | H3 |
| shapely, osm2pgsql, Overpass/OSM | `.../geo/` + `venues` | P3, P4 | H3 |
| faker (test verisi) | `apps/pipeline/tests/fixtures/` | P3 | H4 |
| Nominatim 5.3.2 self-host, Martin + Protomaps basemap | `infra/compose*.yaml`, `martin/martin.yaml` | P4 (P1 destek) | H1, H3 |
| livekit.yaml, Caddyfile, Headscale, `infra/docs/ports.md` | `infra/` | P1 (kurulum), P5 (port) | H1, H5 |
| Podman, `mise.toml`, `justfile`, oxker (`just services`) | kök | P1 | H1 |
| adb + UI Automator (3 akış) | cihaz testleri | P7 | H6 |
| Grafana + Loki, GlitchTip | izleme + hata takibi | P1 | H6 |
| mdBook (`book.toml` + SUMMARY) | `docs/` derlemesi | P7 (H7.2), Tümü (H6.7) | H6, H7 |
| `data-sources.md`, `runbook.md`, ADR'ler | `docs/` | P3, P1, Tümü | H1–H7 |
| schemathesis, ML Aşama 3 | Faz 2 — kapsam dışı (3. bölüm) | — | — |

## 10. Paralellik protokolü (kimse boş beklemez)

Bağımlılık var, boş bekleme yok. Üç kural:

1. **Tüketici mock'la başlar.** Ekran ve istemci işleri haftaya sözleşme + örnek veriyle girer; hafta çıkışında gerçeğe kilitlenir (H2.12 üretim, H3.15 prova, H4/H5 provaları, H6.2). "API bitmedi" cümlesi mazeret değildir — sözleşme H1.2/H1.8'de dondu.
2. **Tıkandın mı buddy'ye, çözülmezse lidere.** Lider seni sıradaki bağımsız işine kaydırır — her dosyada her hafta en az iki bağımsız iş vardır. Tıkanıklık devir notuna yazılır.
3. **Hafta çıkışı kilitleme.** Mock'la başlanan iş hafta bitmeden gerçeğe bağlanır ve provada kanıtlanır; bağlanmazsa devir notuna ID + sahip yazılır.
