# ADR-0001: Uygulama kabuğu — Tauri + SvelteKit + Deno

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §3.1, §4.4

## Karar

Uygulama kabuğu Tauri 2.12. Arayüz SvelteKit 3 + Svelte 5, çalışma zamanı ve paket yöneticisi Deno 2.9. Rust yüzeyi en fazla 200 satır.

## Gerekçe

**Tauri.** APK boyutu ve bellek. React Native ve Flutter'ın aksine, uygulama WebView üzerinde çalıştığı için ikil dosya çok küçük ve boşta bellek düşük kalıyor. Ölçülebilir hedefler: APK < 25 MB, boşta bellek < 120 MB, açılış < 1,2 sn.

**Svelte.** Derleme adımı yok, durum yönetimi ayrı kütüphane gerektirmiyor. Ekip TypeScript bildiği için öğrenme yükü kütüphanede değil, Svelte'nin reaktif söz diziminde.

**Deno.** TypeScript ve JavaScript'i tek runtime'da çalıştırır — ayrı bir derleme adımı ve ayrı bir `node_modules` yönetimi gerekmez. `create-tauri-app` Deno'yu 4.5.2'den beri resmî olarak destekliyor; Tauri dokümanında `"beforeDevCommand": "deno task dev"` örneği veriliyor.

## Rust bütçesi: 200 satır

Tauri Rust kullanır. Ekip Rust bilmiyor. Bu yüzden:

| Katman | Yazılan Rust |
|---|---|
| Önbellek, konum, bildirim, QR, derin link, pano, güncelleme | 0 — hazır eklentiler |
| Özel komut (en fazla 2) | ~30 satır |
| Bütçe tavanı | 200 satır |

Bütçe aşılırsa PR gerekçeyi yazar. `src-tauri/` dizinine yalnızca P6 dokunur; CODEOWNERS bunu zorunlu kılar.

## Sonuçlar

**Java/Kotlin zorunluluğu.** Tauri, Android sistem ekranlarına hazır gelen Java/Kotlin eklenti kodu üzerinden erişir. Uygulama kodunda Java/Kotlin yoktur ama JDK/NDK derleme sırasında devreye girer. Bkz. §4.6.

**Sunucu Rust değil.** Rust tarafının minimal olması, API'nin Rust olabileceği anlamına gelmez. API Python ile yazılıyor — bkz. [ADR-0002](0002-backend-python.md).

**Web sürümü ikincil.** APK teslim edilen şeydir. Web sürümü ekran paylaşımı ve tarayıcı E2E testleri için var.