# ADR-0011: JS runtime — Deno yerine Node

**Tarih:** 2026-10-11
**Durum:** Kabul edildi
**Kapsam:** §3.1, §4.4, §4.12, §5, §13.1, §14, §15, §16, §17

[ADR-0001](0001-tauri-deno-sveltekit.md)'i geçersiz kılar (eskisine `Superseded by ADR-0011` notu düşüldü).

## Karar

Mobil kabuğun JS runtime ve paket yöneticisi Node 24 LTS + npm. `deno.json` yerine `package.json` (npm çalışma alanı), `deno task` yerine `npm run`, `deno fmt` yerine Prettier, `deno lint` yerine eslint.

## Gerekçe

**Deno tarafı kapandı.** 2026-10-09'da Deno ekibi Cloudflare'e katıldı: runtime'a 12 ay hata/güvenlik güncellemesi, sonra geliştirme bitiyor; Deno Deploy 6 ay sonra kapanıyor (https://deno.com/blog/cloudflare, https://blog.cloudflare.com/deno-joins-cloudflare/). Yeni başlanan bir projeyi, dondurulacağı açıklanmış bir runtime üzerine kurmak savunulamaz.

**Node tarafı hazır.** Tauri dokümanının varsayılan zinciri Node/npm (`npm run tauri ...`); `create-tauri-app` npm'i birinci sınıf destekliyor. Yığının geri kalanı zaten npm'den geliyor (bits-ui, shadcn-svelte — bkz. §3.1). Ekip Node biliyor; öğrenme maliyeti sıfır.

## Sonuçlar

**R14 kapandı.** Deno + Vite + SvelteKit uyumsuzluk riski ortadan kalktı; Sprint 0'da tek deneme yeterli (§10, madde 0.2).

**`node_modules` geri geldi.** ADR-0001'in Deno gerekçesindeki "`node_modules` yönetimi gerekmez" avantajı kaybedildi. Bağımlılıklar npm üzerinden; sürümler `mise.toml` + `package-lock.json` ile sabitlenir.

**Format/lint zinciri.** Prettier (`.ts` `.js` `.json` `.md` `.svelte`) + eslint + svelte-check — bkz. §4.12, §13.1.
