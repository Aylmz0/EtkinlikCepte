# Karar kayıtları (ADR)

Bu dizin, `development.md` içindeki kararların **gerekçesini** tutar. Doküman kararın ne olduğunu söyler, buradaki dosya nedenini.

Her ADR tek bir kararı kapsar. Kararlar Sprint 0'da ekip tarafından birlikte kabul edilir; kabul sonrası değişiklik yeni bir ADR ile yapılır, eskisi silinmez — yerine `superseded by ADR-XXXX` notu düşülür.

## Dizin

| ADR | Karar | development.md |
|---|---|---|
| [0001](0001-tauri-deno-sveltekit.md) | Uygulama kabuğu: Tauri + SvelteKit + Deno (superseded by 0011) | §3.1, §4.4 |
| [0002](0002-backend-python.md) | Sunucu dili: Python + FastAPI | §3.2, §4.5 |
| [0003](0003-declined-dependencies.md) | Kullanılmayacak bağımlılıklar | §3.5 |
| [0004](0004-media-storage-postgres.md) | Dosyalar veritabanında | §4.9 |
| [0005](0005-no-push-notifications.md) | Kapalıyken bildirim yok | §4.8 |
| [0006](0006-no-payments.md) | Tahsilat yok | §4.2 |
| [0007](0007-css-framework.md) | CSS: Tailwind | §3.1, §3.5 |
| [0008](0008-no-video-upload.md) | Kulüp gönderisinde video yok | §4.13 |
| [0009](0009-screen-share-web-only.md) | Ekran paylaşımı yalnızca web'de | §4.1 |
| [0010](0010-a11y-component-stack.md) | Erişilebilirlik: bits-ui + shadcn-svelte | §3.1 |
| [0011](0011-node-runtime.md) | JS runtime: Deno yerine Node 24 LTS + npm (0001'i geçersiz kılar) | §3.1, §4.4, §4.12, §5, §13.1, §14–§17 |

## Şablon

Yeni ADR için:

```markdown
# ADR-XXXX: <kararın tek cümlelik özeti>

**Tarih:** YYYY-MM-DD
**Durum:** Kabul edildi | Superseded by ADR-YYYY
**Kapsam:** §<hangi bölümler>

## Karar

Ne yapıyoruz. Cümle veya kısa tablo.

## Gerekçe

Neden bu. Ölçülebilir veri varsa ver, tahmin varsa tahmin olduğunu yaz.

## Sonuçlar

Bu kararın getirdiği kısıtlar, alınan riskler, geri dönüş maliyeti.
```

**Kural:** Gerekçe ölçülebilir olmalı. "Daha iyi" geçerli gerekçe değil. Sayı, sürüm, tarih veya ölçüm gerekir.