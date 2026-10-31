# H2 audit — 2026-10-27

Bu dosya H2 kabul ölçütlerinin repo kanıtına göre durumudur. “Test geçiyor”
ile “görev tamamlandı” aynı şey değildir; aşağıdaki tablo ikisini ayırır.

## Özet

| Kişi | H2 görevleri | Durum | Not |
|---|---|---|---|
| P1 Abdullah | H2.1, H2.2, H2.12 | ✅ | Auth/profil/API client; test + Hurl |
| P2 Eren | H2.3, H2.4, H2.5 | ✅ | Kulüp/üyelik, etkinlik, bilet/QR/check-in; DB integration |
| P3 İsmail | H2.8, H2.14, H2.15 | ✅ | RSS/JSON-LD/HTML + `source_events` upsert; fixture test |
| P4 Umut | H2.6, H2.7, H2.16, H2.17 | ⚠️ | Uçlar/testler var; 100k süre ve Nominatim import kanıtı yok |
| P5 Cevat | H2.18, H2.19, H2.20 | ✅ | Token, devices, notifications, realtime client; ses provası fiziksel |
| P6 Hilal | H2.9, H2.10, H2.11, H2.13 | ⚠️ | Auth/offline cache/UI var; APK ve gerçek cihaz doğrulaması yok |
| P7 Adar | H2.21 | ✅ | QA listesi + mock veri notu |

## Kalan iki fiziksel doğrulama

- **P6:** Android SDK/NDK olmadığı için `tauri android build --apk` bu makinede
  çalıştırılamadı. Kod/build web tarafı yeşil; APK başka makinede üretilmeli.
- **P4:** 100k kayıt fixture’ı ve Nominatim Türkiye import’u staging işi;
  sorgu prototipi ve PostGIS smoke testi yeşil.

## Doğrulama

- API: 56 passed (DB testleri `RUN_DB_TESTS=1` ile)
- Pipeline: 7 passed (DB writer testi `RUN_DB_TESTS=1` ile)
- UI: Vitest 2 passed, svelte-check 0 error
- Mobile: svelte-check 0 error, build başarılı
- Playwright: 1 pass, 8 skipped
- `just api-types`: diff boş
