# P6 — Uygulama çekirdeği

**Alan (sabit, §6):** Tauri kabuğu, yönlendirme, giriş ekranları, çevrimdışı önbellek, tasarım sistemi. `src-tauri/` yalnızca senin (§4.4). Ekranları P7 ile yazarsın. 7 hafta bu kavramdasın.
**Buddy:** P4 (§6.2). **Lider haftan:** H6 (kalite kapısı).

## Envanterin

- **Dizinlerin (§5):** `apps/mobile/src/routes/` (sayfalar), `apps/mobile/src/lib/{api,auth,realtime,offline,platform}/`, `apps/mobile/src/locales/tr.json`, `apps/mobile/src-tauri/` (capabilities, `tauri.conf.json`) + `apps/mobile/{static,svelte.config.js,vite.config.ts,tailwind.config.ts}`, `.prettierrc`.
- **Kuralların (§5.1, §4.11):** `ui`'da istek/jeton/rota yok; `routes/`ta elle stil yok; `ssr=false`, `prerender=false`, adapter-static + `fallback: index.html`; `geo:` devretme (§4.10).
- **Ekranların (§1.6):** `/login`, `/register`, `/(tabs)/clubs`, `/clubs/[id]` (P2), `/(tabs)/profile`, `/settings`.
- **Rust bütçen (§4.4):** eklenti işleri 0 satır; ≤2 komut ~30 satır; tavan 200.
- **Paketlerin (§3.1):** shadcn kopyaları `components/ui/`da, seninkiler `features/`da (+`base.css`, `components.json`); 13 parça tablosu.

## H1 — İskelet haftan

- **H1.12 APK denemesi + iskelet.** `apps/mobile` + `src-tauri` (Vite 8 + TS 7 §3.1); `beforeDevCommand: npm run dev`; `just android-apk` imzasız. Kabul: APK kurulur/açılır (R1: kırılırsa çarşamba P1'e, yedek web). Çıktı: P7 (H1.15), H1.13, H2.9.
- **H1.13 Tema + IntelliSense.** `tokens.css` + Tailwind `@theme` + `tailwind.config.ts` (yalnızca IntelliSense §5). Kabul: jeton değişimi yansır. Çıktı: H2.10.
- **H1.14 Ekran kilidi (P7 ile).** 23 ekran + sahip (§1.6). Kabul: liste donar.

## H2 — Ekran temeli haftan

- **H2.9 Kabuk + nav + giriş/kayıt.** `api-client` ile kayıt→giriş→jeton (`lib/auth/`, formsnap/superforms/Zod §3.1). Kabul: gerçek API akışı.
- **H2.10 Tasarım sistemi.** İlk bileşenler + `components.json` (svelte-sonner toast, lucide ikon §3.1). Kabul: herkes `features/`'tan tüketir + Vitest bileşen testleri (§12).
- **H2.11 Kulüp/profil/ayarlar (P2 destekli).** `tr.json` Türkçe, 44px (§16). Kabul: ekran kutuları.
- **H2.13 SQLite okuma.** Keşif listesi + biletler çevrimdışı (§1.5; QR hep okunur) + WAL mode (okuma/yazma çakışmaz). Kabul: internetsiz açılır. Çıktı: H4.7.

## H3 — Platform haftan

- **H3.15 İstemci sözleşme provası (P7 ile).** Hedef: `api-client` tipleri canlı API'ya uyar. Adımlar: 1. `just api-types` + örnek ekranlarda tüketim. 2. Uyuşmazlıkları P1'e PR'la (sözleşme kayması §12). Kabul: prova yeşil, kayma yok. Çıktı: H3.3–H3.6'nın güveni.
- **H3.9-katılım.** Kabuk/offline ayağının durumu. Kabul: APK + kuyruk tablosu hazır.
- **H3.17 Platform sarmalayıcılar.** `lib/platform/`: konum, pano, QR okutma, bildirim stub'ları + test sahte verisi (§4.11: tek nokta). Kabul: testler sahteyle koşar. Çıktı: H4.5, H5.2.
- Ayrıca: P7'nin H3 ekranlarında kabuk/nav soruları; buddy P4'e destek.

## H4 — Bağlantı haftan

- **H4.5 Bildirim + deep-link (P5 ile).** Eklenti config (0 Rust) + izin akışı cihazda. Kabul: dört §4.8 durumu provada.
- **H4.7 Eşitleme kuyruğu.** Yazma biriktirme, okuma öncelikli. Kabul: kuyruk birikir ve bağlantıda boşalır. Çıktı: H5.9.
- **H4.9 Deep-link + `geo:` + SSR.** `index.html`ten route'a düşüş (§4.11); `geo:?q=` devretme (§4.10); web'de buton. Kabul: linkten ekran açılır.

## H5 — Kuyruk kapanışın

- **H5.9 Kuyruk bitirme.** Bağlantıda gönderim (§4.8). Kabul: çevrimdışı işlemler eşitlenir. Çıktı: H6.1.

## H6 — Kapı haftan (lider sensin)

- **H6.1 Eşitleme + çakışma.** Kural yazılı + testli. Kabul: çakışma testi yeşil.
- **H6.3 Performans (P7 ile).** §11 istemci: açılış < 1.2 sn, bellek < 120 MB, APK < 25 MB, 60 fps, LRU 300 MB, WebP/tembel, 1000+ sanal liste. Kabul: `just perf-apk` yeşil; aşan PR durur.
- **H6.13 `plugin-updater`.** Kendi imzalı bildirimi (§13.2). Kabul: güncelleme provada.
- **H6.7-pay.** Kabuk/offline dokümanı (`runbook.md` mobil kısmı) + eklenti listesi güncelliği (§16: yeni eklenti → §3.1).
- **Liderlik:** Eksiksiz H7'ye devretmeme; eksik varsa H7.1'de kimin kapatacağı devir notunda. P7'ye devir.

## H7 — Kapanış

Kabuk/offline ayağı sende (H7.1). Rust 200 aşıldıysa gerekçe H7.3'ten önce PR'da.

## Risklerin

R1 çarşambadan belli olur. R2: eklenti yetiyorsa komut yok. R5: H2.10'u erken dondur. R13: harita bellekte düşük çözünürlük yedeği.
