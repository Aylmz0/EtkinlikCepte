# P1 — Abdullah Yılmaz — Tech Lead

**Alan (sabit, §6 Ekip):** Sözleşme, veritabanı şeması, kimlik doğrulama, sunucu kurulumu. 7 hafta boyunca bu kavramdasın; başka bir alana kod yazmazsın, sorarsın.
**Buddy:** P3 (§6.2 Çalışma kuralları eşleşmesi). **Lider haftan:** H1. **Kalıcı yetki:** `/v1` sözleşmesini bozan değişiklik ve tüm şema/göç onayları sende (§6.2 Çalışma kuralları, §8.1 Sözleşme kuralları).

## Envanterin

Bu dosyadaki işler şu tablo, dizin, uç ve komutlarla yapılır. Hepsi `development.md`'de tanımlı; burası sadece senin listen:

- **Tablolar (§7 Veri modeli):** `users`, `refresh_tokens`, `devices`, `audit_log` + tüm göçler (`apps/api/alembic/`).
- **Dizinlerin (§5 Depo yapısı):** `apps/api/app/{core,domain,schemas,routers,services,repos}`, `apps/api/{pyproject.toml,tests/}`, `ruff.toml`, `.editorconfig`.
- **Uçlar (§8 API sözleşmesi):** `POST /auth/register|login|refresh|logout`, `GET /auth/me`, `GET /health|metrics|openapi.json`.
- **Komutların:** `just setup|dev|migrate|hurl|ci`, `mise install|trust`, `alembic upgrade head`.
- **Kapıların (§13.1 Otomatik doğrulama):** `contract` (üretim sonrası fark boş olmalı), `migrate` (boş veritabanında), `audit`, `deny`.

## H1 — Temeller (lider sensin)

Bu hafta ekibin geri kalanının üstüne basacağı zemini atıyorsun: depo, sözleşme taslağı, veritabanı, servisler, denetim hattı. Hafta bitmeden hiçbiri tam ürün vermez ama hepsi başlar; o yüzden senin işlerin haftanın đầu girdisidir.

- **H1.1 Depo/mise/just/Podman.** **Hedef:** 7 kişi aynı sürümle başlar (§4.7 Sürüm sabitleme: tek doğruluk kaynağı `mise.toml`). **Adımlar:** 1. `mise.toml`'a Node 24 LTS, Python 3.13, uv, just, Podman sürümlerini pin'le. 2. `justfile`'a `setup/dev/test/ci/hurl/migrate` hedeflerini + `services` (oxker konteyner izleme §3.4 Araçlar) hedefini yaz (§15 Komutlar). 3. Temiz bir makinede `just setup` dene. **Kabul:** ikinci bir makinede `just setup && just dev` hatasız çalışır. **Çıktı:** H1.2/H1.4/H1.12/H1.6'nın girdisi hazır, ekip kuruluma geçer.
- **H1.2 FastAPI iskeleti + OpenAPI v1.** **Hedef:** Pydantic modellerinden OpenAPI 3.1 belgesi otomatik üretilir, kimse sözleşmeyi elle yazmaz (§4.5 Backend dili). **Adımlar:** 1. `apps/api/app/main.py` + içi boş router'lar (`auth, clubs, events, channels, discover, media, admin`). 2. `GET /openapi.json` + `GET /health` uçlarını aç. 3. Sunucu yığınını kur: Uvicorn + uvloop + orjson + hiredis + psycopg bağlantı havuzu (PgBouncer ilk fazda yok §11 Performans hedefleri) + structlog günlükleme — hepsi `apps/api/app/core/` dizininde. 4. `just api-types` ile istemci üretimi provası yap. **Kabul:** `/openapi.json` 200 döner. **Çıktı:** P2'nin H1.7/H1.8 karar ve taslakları ile P3'ün H1.9 adaptörleri bu iskelete dayanır.
- **H1.3 Şema v1 + Alembic.** **Hedef:** §7 Veri modelindeki tablolar ve kritik indeksler (`events(starts_at)`, `venues` GIST, `chat_messages(channel_id, created_at DESC)`…) ilk göçle veritabanında. **Adımlar:** 1. Modelleri yaz (para: kuruş tam sayı + `CHAR(3)` para birimi; zaman: TIMESTAMPTZ). 2. `alembic revision` üret, boş veritabanında `upgrade head` koştur. 3. CI'ın `migrate` adımını bağla. **Kabul:** boş veritabanına göç uygulanır ve şema karşılaştırması yeşil verir. **Çıktı:** H2'deki tüm backend işlerinin veritabanı hazır.
- **H1.4 Compose.** postgres+postgis, valkey, caddy, martin servisleri (§2 Mimari). **Adımlar:** 1. `infra/compose.yaml` + `compose.dev.yaml` dosyalarını yaz. 2. Caddyfile (yerelde HTTP; gerçek HTTPS sertifikası H5.15 staging işinde). 3. `infra/docs/ports.md` port listesini aç. **Kabul:** `pg_isready` + Valkey `PING` + Martin `/health` döner. **Çıktı:** P4'ün H1.10/H1.17 coğrafi işleri ile P5'in H1.11 medya denemesi bu servislere dayanır.
- **H1.6 CI iskeleti.** **Hedef:** §13.1 Otomatik doğrulamadaki adımlar (lint, test, contract, hurl, migrate, audit, deny, build) ilk PR'dan itibaren koşar. **Adımlar:** 1. Platformu kararlaştır (kurumun GitHub/GitLab hesabı varsa o, yoksa kendi sunucumuzda Forgejo). 2. `deny.txt` yasaklı listesini (ADR-0003) yaz + ilk PR'ı CI'dan geçir. **Kabul:** kırmızı (hatalı) PR birleştirilemez.
- **Desteklerin (görev değil, pair/onay):** H1.5'te P2'nin Hurl testlerini doğrula · H1.9'da P3 ile yan yana çalış (R11) · H1.16 migration dosyasını onayla · H1.17 Nominatim profilini gözden geçir.
- **Liderlik:** Pazartesi 30 dakika senkronu yönet + planı ekibe tebliğ et + §18 Onay tablosundaki imzaları takip et. Cuma günü: imzasız APK üretildi mi, `just dev` ayakta mı, `/v1` dondu mu — bunları kontrol edip P2'ye devir notunu yazarsın.

## H2 — Çekirdek

Bu hafta kimlik katmanını bitiriyor ve telefon tarafının beklediği tip paketini üretiyorsun.

- **H2.1 Auth.** `POST /auth/*` + `GET /auth/me` uçları (argon2-cffi ile parola şifreleme, PyJWT jetonlar, `refresh_tokens` tablosu; hatalar RFC 9457 formatında, §8.1 Sözleşme kuralları md.5). **Adımlar:** 1. Pydantic doğrulama şemaları. 2. Jeton yenileme akışı + `revoked_at` iptal kaydı. 3. Hurl ile auth akış testi. **Kabul:** kayıt→giriş→yenileme→çıkış zinciri yeşil + pytest `services/`+`domain/` kapsamı %90 (§12 Test stratejisi). **Çıktı:** P6'nın H2.9 giriş ekranları ile P4/P5'in korumalı uçları bu kimliğe dayanır.
- **H2.2 Profil.** `users` tablosunda profil CRUD'u (interests TEXT[], city, bio). **Kabul:** `GET /auth/me` profili eksiksiz döner. **Çıktı:** P6'nın H2.11 profil ekranı buradan beslenir.
- **H2.12 `api-client` v1.** **Hedef:** telefon tarafı tipleri tek komutla üretilir, elle yazılmaz. **Adımlar:** 1. H1.8 taslakları + H2.1/H2.2'ye karşı ilk üretim (`just api-types`). 2. Üretim sonrası `git diff` boş olmalı + P6/P7'ye kullanım turu attır (§13.1 Otomatik doğrulama). H2.3–H2.5 router'ları düşünce yeniden üretim CI'da döner (bu rutin iştir, görevin parçası değil — görev ilk üretimde biter). **Kabul:** ilk üretim fark-boş ve paket import edilebiliyor. **Çıktı:** H3 ekranlarının tamamı bu tiplere dayanır.

## H3 — Veri haftası (senin işin: kapsam + değerlendirme)

Bu hafta kodtan çok kapı nöbeti tutuyorsun: sözleşme test kapsamı ve hafta sonu değerlendirmesinin teknik masası sende.

- **H3.8-pay.** Kendi uçlarının (kimlik/sistem/yönetim) Hurl testleri — başkasını beklemezsin — + kapsam raporu iskeleti + sözleşme dondurma denetimi (H2'de açılan uçları `/v1`'e karşı tek tek karşılaştır); birleştirme H3.9 değerlendirme ritüelinde yapılır. **Kabul:** kendi payın yeşil + denetim notu PR'da.
- **H3.11-sunucu.** **Hedef:** OSM/Overpass ağır sorguları kendi sunucumuzdan koşar, dış servise yük binmez (§4.3 Veri kaynakları). **Adımlar:** 1. Overpass ortamını sunucuda ayağa kaldır (kaynak limitleriyle). 2. osm2pgsql ile `venues` yükleme hattını sunucu tarafında kur. 3. İstek hızı/kota sınırlarını yazılı hale getir (R4). **Kabul:** sunucudan koşan örnek Overpass sorgusu döner + kota notu PR'da. **Çıktı:** P3'ün H3.11 veri çekme ve P4'ün kategori eşleme işleri bu ortama dayanır.
- **H3.12-sunucu.** **Hedef:** harita paketleri kendi sunucumuzdan üretilir, dışarıdan hazır paket kullanılmaz (§4.3 Veri kaynakları). **Adımlar:** 1. Martin servisini sunucuda yapılandır (`infra/martin/martin.yaml`). 2. `venues` tablosundan PMTiles paket üretimini çalıştır. 3. Üretim komutunu `runbook.md`'ye yaz. **Kabul:** sunucuda üretilen paket URL'i istemcide açılır. **Çıktı:** P4'ün H3.12 doğrulaması ve P7'nin harita tüketimi bu üretime dayanır.
- **H3.9-değerlendirme.** Çıkan/çıkmayan işlerin teknik tablosunu hazırlarsın (ana plan 3. bölümdeki ikinci dalga kesinti önerisiyle); toplantıyı P3 yönetir, kararı ekip verir. **Kabul:** karar yazılı durur.

## H4 — Denetim haftan

- **H4.10 Sözleşme denetimi.** **Hedef:** H4'te açılan sohbet/jeton uçları `/v1` sözleşmesini bozmasın. **Adımlar:** 1. `POST /channels/{id}/messages`, DM ve jeton uçlarının şemalarını H1.2 taslağıyla karşılaştır. 2. Bozan bir değişiklik varsa ana sürüm artışı dayat (§8.1 Sözleşme kuralları md.1). 3. WS tip listesini onayla. **Kabul:** statik denetim notu PR'da durur (taslak + §7 Veri modeli + §8.1'e karşı bakılır, çalışan kod beklenmez); canlı doğrulama H6.5 güvenlik işinde yapılır. **Çıktı:** H5'in işleri bu denetime dayanarak ilerler.
- Ayrıca: P5'in H4.1–H4.4 işlerinde C/danışılan konumundasın; soruları bekletmeden yanıtla.

## H5 — Staging haftan

- **H5.15 Staging HTTPS + secrets.** **Hedef:** deneme sunucusu gerçek sertifikayla ayağa kalkar, gizli anahtarlar depoya girmez (§13.2 Dağıtım). **Adımlar:** 1. Yer tutucu adreslerde (`api.projectx.app`) staging ortamı aç. 2. Gizli anahtarlar depoya girmez; SOPS veya Infisical ile şifreli saklanır. 3. Headscale ile sunucuya portsuz erişim kur. **Kabul:** HTTPS staging ayakta + denetim log'u tutuluyor. **Çıktı:** H6.4 sürüm hattı bu ortama kurulur.
- Ayrıca: P2'nin H5.1 QR şemasında kapasite kuralını (§8.1 Sözleşme kuralları md.7) gözden geçirirsin.

## H6 — Sıkılaştırma

- **H6.4 İmzalama (P7 ile).** İmzalama anahtarı CI gizlisinde durur, parolası gizli (§13.2 Dağıtım); `build-apk` yalnızca `main`/`release/*` dallarında çalışır. **Kabul:** CI'dan imzalı APK iner.
- **H6.5 Güvenlik.** Rol denetimi, `limits` hız sınırı, gizli anahtar taraması (+ `GET /admin/audit` ucu, `audit_log` §7 Veri modeli) + H4.10 bulgularının canlı doğrulaması. **Kabul:** CI `audit` adımı yeşil.
- **H6.6 Yük + maliyet.** k6 ile 500 eşzamanlı okuma; hedef p95 okuma < 200 ms, yazma < 350 ms (§11 Performans hedefleri). **Kabul:** rapor hazır + §11 sunucu hedefleri tuttu.
- **H6.17 İzleme + hata takibi.** **Hedef:** Grafana + Loki ile sunucu izleme, GlitchTip ile hata takibi (§3.4 Araçlar). **Adımlar:** 1. Compose'a log toplama + gösterge paneli kur (k6 yükü altında dene). 2. GlitchTip'e istemci + sunucu hata akışını bağla. **Kabul:** panel açılır, deneme hatası panele düşer. **Çıktı:** H7 provası bu gözlemle izlenir.
- **H6.7-koordinasyon.** Herkes kendi doküman payını yazar; sen ölü link ve güncel-dışı ADR bırakılmadığını denetlersin. **Kabul:** mdBook uyarısız derlenir, kırık link yok.

## H7 — Demo

- **H7.1-pay.** Demo provasında sözleşme ayağı sende: bozulan uç olursa ilk müdahale senin. **Kabul:** prova sırasında sözleşme hatası çıkmaz.
- **H7.3 Kapanış.** §16 Bitti tanımı kutuları + §18 Onay tablosunda 7 imza. **Kabul:** tüm kutular tikli.

## Risklerin

R8 (`contract` kapısı): H1.6'dan itibaren kırmızı PR'ı bekletirsin. R6/R7 (performans/stil): H6.6 ölçümü + `just fmt` kapısı kapsar. Şema değişikliği = PR + senin onayın; sözlü onay yok.
