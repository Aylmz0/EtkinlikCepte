# ADR-0009: Ekran paylaşımı yalnızca web sürümünde çalışır

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §4.1

## Karar

Ekran paylaşımı web sürümünde çalışır, Android'de yok. Telefonda paylaşım belge gönderme, bağlantı paylaşma ve dosya atma ile yapılır.

## Gerekçe

Android'un WebView katmanı `getDisplayMedia` API'sini sağlamaz. Bu, tarayıcıda veya kütüphaneyle aşılamayan bir platform eksiği. Ekran paylaşımı mümkün olduğu tek ortam masaüstü tarayıcısıdır.

Bu, LiveKit'in sunduğu bir özellik değil — API'nin içinde yok. Workaround aramak yerine kapsam dışı bırakıldı.

## Sonuçlar

**Online etkinlikler telefonda çalışır**, ses ve görüntü açılır, dosya paylaşılır. Ekran paylaşımı gereken etkinlikler için web sürümü kullanılır.

**Sprint 4'e yedeklendi.** `4.1 Ekran paylaşımı (web)` Sprint 4'te. Hafta 6 değerlendirmesinde düşülebilir ilk işlerden biridir (§6.1).

**Risk R3 kapatıldı.** "Telefonda ekran paylaşımı mümkün değil" kesin bir gerçek; önlem olarak kapsam dışı ilan edildi.