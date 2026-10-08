# ADR-0008: Kulüp gönderilerinde video yüklenmez

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §4.13

## Karar

Kulüp gönderisi metin, fotoğraf ve dış bağlantı içerir. Video yüklenmez.

## Gerekçe

Üç seçenek ölçüldü:

| Seçenek | Sonuç |
|---|---|
| Videoyu veritabanında sakla | 100 MB bir video 80 GB diski tüketir — 800 video. [ADR-0004](0004-media-storage-postgres.md) kabul edilmediği için uygun değil |
| Kendi video sunucunu kur | Kod dönüştürme (ffmpeg), iş kuyruğu, depolama, bant genişliği. Haftalarca iş |
| Dış bağlantı (YouTube, Vimeo, çekim linki) | Sıfır altyapı |

Kulüplerin çoğunun zaten bir video kanalı var. Bağlantı vermek, gönderide tanıtım yapmanın en ucuz yolu.

## Sonuçlar

**Gönderi içeriği sabit.**

| Alan | Kural |
|---|---|
| Metin | Zorunlu değil |
| Fotoğraf | En fazla 4 adet, her biri 5 MB |
| Bağlantı | Tek adet; kapak görseli gösterilir, tıklayınca dışarı açılır |
| Görünürlük | `public`, `followers` (varsayılan), `members` |

**`club_post_video` medya türü yok.** `media.kind` enum'unda yer almıyor. Şema, ileride video eklenirse değişmeden kalır.

**Kendi video barındırma ayrı bir proje.** PeerTube FOSS ve self-host edilebilir, ancak dönüştürme kuyruğu ve bant genişliği bütçesi gerektirir. Sprint planında yok; ekip isterse ayrı bir ADR ve sprint açar.