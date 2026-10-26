# H2 audit — 2026-10-26

Bu dosya H2 kabul ölçütlerinin repo kanıtına göre durumudur. “Test geçiyor”
ile “görev tamamlandı” aynı şey değildir; aşağıdaki tablo ikisini ayırır.

## Özet

| Kişi | H2 görevleri | Durum |
|---|---|---|
| P1 Abdullah | H2.1, H2.2, H2.12 | ✅ Tamam |
| P2 Eren | H2.3, H2.4, H2.5 | ❌ Başlanmadı; router’lar 501 dönüyor |
| P3 İsmail | H2.8, H2.14, H2.15 | ⚠️ Kısmi; RSS/JSON-LD var, HTML/DB bağlantısı yok |
| P4 Umut | H2.6, H2.7, H2.16, H2.17 | ⚠️ Kısmi; endpoint’ler var, performans/Nominatim kanıtı yok |
| P5 Cevat | H2.18, H2.19, H2.20 | ❌ Yok; token/device/notification/realtime istemcisi yok |
| P6 Hilal | H2.9, H2.10, H2.11, H2.13 | ⚠️ UI var; auth bağlantısı, Vitest ve SQLite offline yok |
| P7 Adar | H2.21 | ❌ Yok; QA listesi ve mock veri seti yok |

## P1 — tamam

- `POST /v1/auth/register|login|refresh|logout`, `GET/PATCH /v1/auth/me`
- argon2id, HS256 access JWT, 30 günlük refresh rotation/revocation
- RFC 9457 hata gövdesi
- `just api-types` OpenAPI → TypeScript + Zod üretiyor; diff-boş
- 48 unit + 1 DB integration test; Hurl auth flow 5 istek yeşil

## P2 — eksik

`apps/api/app/routers/clubs.py` ve `events.py` yalnızca 501 dönen taslaklar.
H2.3/H2.4/H2.5 için gerçek uçlar yok:

- kulüp CRUD, üyelik/rol, davetiye redeem
- etkinlik CRUD, publish/cancel, kapasite
- bilet tipleri, register, QR üretimi, check-in

## P3 — kısmi

- `sources/rss.py` ve `sources/jsonld.py` + fixture testleri var.
- `sources/html.py` hedef seçicileri `site-a`/`site-b` placeholder.
- `source_events`’e yazma ve dedup bağlantısı yok.
- H2.8’in “`just migrate` + faker test verisi” kabulü gösterilmedi.

## P4 — kısmi

- `/discover/venues`, `/discover/events`, `/discover/recommendations` çalışıyor.
- PostGIS `ST_DWithin`/`ST_Distance`, Türkçe katlama, altı faktörlü skor var.
- Eksik: 100k kayıt `EXPLAIN ANALYZE` süresi, Hurl kapsamı, Nominatim veri
  yüklemesi ve adres→koordinat kanıtı.

## P5 — eksik

`realtime/`, `media/`, `notifications/` yalnızca boş `__init__.py`.
H2.18–H2.20 için:

- LiveKit oda jetonu uçları
- `POST/DELETE /devices`
- `GET /notifications`, `POST /notifications/{id}/read`
- `apps/mobile/src/lib/realtime/` WS istemcisi + presence store

## P6 — kısmi

UI ekranları ve tasarım sistemi var; ancak:

- `lib/api/`, `lib/auth/`, `lib/offline/`, `lib/realtime/`, `lib/platform/` boş
- login/register formları gerçek auth’a bağlı değil
- SQLite WAL tabanlı çevrimdışı okuma yok
- Vitest bileşen/store testi yok
- `src-tauri/gen/android` yok; APK bu makinede üretilemedi

## P7 — eksik

- H2.21 QA listesi, focus/klavye/ARIA denetimi ve mock veri seti yok.
- Playwright iskeleti H1’den var; senaryolar H4.13’e ait.

## Bu branch’te yapılanlar

- H1’deki eksikler kapatıldı.
- CI billing/e2e takılması düzeltildi.
- P4 keşif kodu gerçek §7 şemasına göre yeniden yazıldı.
- P1 auth/profil/API client tamamlandı.
- P7 mobil UI build’i düzeltildi.

Yukarıdaki H2 eksikleri **feature işi**; “debug” ile tamamlanamaz. Bunları
tamamlamadan H2’yi “kusursuz” ilan etmek doğru olmaz.
