# ADR-0004: Dosyalar veritabanında saklanır

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §4.9

## Karar

Görseller ve dosyalar PostgreSQL `BYTEA` sütununda saklanır. Ayrı bir nesne deposu kurulmaz.

## Gerekçe

**Dosya boyutu.** Avatar 2 MB, diğer görseller 5 MB. En büyük dosya 5 MB — nesne deposunun çözdüğü problem burada oluşmuyor.

**Proje ömrü.** On beş hafta, tek sunucu. Nesne deposu ayrı bir servis, ayrı kurulum, ayrı yedekleme, ayrı izleme demek. Bu yatırım hiçbir dosya boyutunda karşılığını bulmaz.

**Sunucu diski.** 80 GB disk. BYTEA ile tüm dosyalar tek yerde, tek yedekleme stratejisiyle yedeklenir.

**Sınır ihlali.** `byte_size` kontrolü veritabanı kabul katmanında yapılır. Sunucu diski büyüse yük de düşer, medyanın sınırları içinde kalır.

## Sonuçlar

**Tablo şişer, PostgreSQL yavaşlar mı?** Hayır, `media` tablosu sorguların `TOAST` alanı üzerinden okunur. Ana tablo satır sayısı düşük kalır. Yine de `byte_size` ve `content_type` indeksli değil — gerekirse Sprint 4'te ölçülür.

**Yedekleme tek komut.** `pg_dump` her şeyi alır. Ayrı depo olsaydı iki ayrı yedek tutulurdu.

**Ölçek limiti kabul edildi.** Video barındırma bu kararı bozar; bu yüzden video yüklemiyoruz ([ADR-0008](0008-no-video-upload.md)).

**Geri dönüş yolu açık.** Harici depoya taşımak gerekirse tek migration. `media.id` ve `GET /media/{id}` sözleşmesi aynı kalır, uygulama kodu değişmez.

## Neden MinIO değil

MinIO, sahibi tarafından 25 Nisan 2026'da arşivlendi. Bakımı durmuş bir yazılıma bağımlılık kabul edilmedi. Alternatifler (Garage, SeaweedFS, Ceph) FOSS ve aktif — biri gerekirse ADR güncellenir.