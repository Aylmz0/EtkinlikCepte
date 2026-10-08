# ADR-0002: Sunucu dili — Python + FastAPI

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §3.2, §4.5

## Karar

API ve veri hattı Python ile yazılır. Web framework: FastAPI, sunucu: Uvicorn.

## Gerekçe

**Ekip Python biliyor, Rust öğrenmiyor.** Yedi kişi, on beş hafta. Sunucuyu Rust ile yazmak, dil öğrenme süresi ve o dilde hata ayıklama süresi ekler. Projenin riski teknoloji seçimi değil, takvim.

**Sözleşme otomatik üretilir.** Pydantic, OpenAPI 3.1 şemasını endpoint'lenden üretir. Elle şema yazılmaz; tipler `just api-types` ile TypeScript'e ve Zod'a çevrilir. Yedi kişinin elle şema güncellemesi, ilk kaydıracak şey budur.

**Veri katmanı hazır.** `lxml`, `parsel`, `pandas`, Playwright, geokodlama — hepsi Python'da. Veri hattı ayrı bir dil öğrenmeyi gerektirmez.

**Performans bu projede darboğaz değil.** Beklenen yük: 500 eşzamanlı okuma. Darboğaz PostGIS sorgusu ve ağ. Python'ın eklediği gecikme bu katmanların yanında ölçüm altında.

## Sonuçlar

**Hız sınırı ve açgözlülük şart.** `limits` ile hız sınırı, uvicorn'da `uvloop` + `orjson` + `hiredis`. Psycopg bağlantı havuzu. Bunlar olmadan yazılım hız sınırı sınırsız olurdu.

**Sorgu katmanı SQLAlchemy + ham SQL.** SQLAlchemy tekdüze sorgu yazımı için, PostGIS uzamsal sorguları ham SQL ile. Karma yaklaşım kasıtlı: hazır yazılan SQL'i değiştirmiyoruz.

**Rust tarafı etkilenmez.** Tauri'nin Rust kodu bu karardan bağımsız.