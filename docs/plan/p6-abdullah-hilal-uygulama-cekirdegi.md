# P6 — Abdullah Hilal — Mobile Engineer, Core & Design System

**Alan (sabit, §6 Ekip):** Tauri kabuğu, yönlendirme, giriş ekranları, çevrimdışı önbellek, tasarım sistemi. `src-tauri/` yalnızca senin (§4.4 Rust yüzeyi: başkası dokunmaz). Ekranları P7 ile birlikte yazarsın. 7 hafta bu kavramdasın.
**Buddy:** P4 (§6.2 Çalışma kuralları eşleşmesi). **Lider haftan:** H6 (kalite kapısı: eksiksiz devretmezsin).

## Envanterin

Senin işin telefonun kendisi: kabuk, navigasyon, çevrimdışı veri, tasarım dili. Kurallar katıdır çünkü `packages/ui` herkesin kullandığı ortak maldır:

- **Dizinlerin (§5 Depo yapısı):** `apps/mobile/src/routes/` (sayfalar), `apps/mobile/src/lib/{api,auth,realtime,offline,platform}/` (sorgular, jeton, canlı bağlantı, çevrimdışı, telefon sarmalayıcıları), `apps/mobile/src/locales/{tr,en}.json` (arayüz metinleri), `apps/mobile/src-tauri/` (capabilities, `tauri.conf.json`) + `apps/mobile/{static,svelte.config.js,vite.config.ts,tailwind.config.ts}`, `.prettierrc` (ön yüz formatı).
- **Kuralların (§5.1 Nerede ne, §4.11 Sayfa kuralları):** `packages/ui` içinde sunucu isteği/jeton/rota bilgisi yok; `routes/` içinde elle yazılmış stil sınıfı yok (görsel her şey paketten gelir); `ssr=false`, `prerender=false`, adapter-static + `fallback: index.html`; `geo:` ile telefonun harita uygulamasına devretme (§4.10 Yol tarifi).
- **Ekranların (§1.6 Ekran listesi):** `/login`, `/register`, `/(tabs)/clubs`, `/clubs/[id]` (P2 ile ortak), `/(tabs)/profile`, `/settings`.
- **Rust bütçen (§4.4 Rust yüzeyi):** eklenti işleri 0 satır Rust (hazır eklenti config'i); en fazla 2 özel komut ~30 satır; tavan 200 satır, aşarsa PR'da gerekçe yazılır.
- **Paketlerin (§3.1 Mobil yığın):** shadcn kopyaları `components/ui/`da (görünüm), seninkiler `features/`da (davranış) (+`base.css`, `components.json`); 13 özel parça tablosu.

## H1 — İskelet haftan

- **H1.12 APK denemesi + iskelet.** `apps/mobile` + `src-tauri` (Vite 8 + TS 7 §3.1 Mobil yığın); `beforeDevCommand: npm run dev`; `just android-apk` ile imzasız deneme (mise 24 gelene kadar sistem node ile başlanabilir, sürüm kilidi hafta içinde konur). **Kabul:** APK kurulur/açılır (R1 derleme zinciri riski: zincir kırılırsa vakit kaybetmeden P1'e bildirirsin, yedek web planı hazır). **Çıktı:** H2.9 kabuk, H1.13 tema ve H2.10 tasarım sistemi buraya dayanır.
- **H1.13 Tema + IntelliSense.** `tokens.css` tema kaynağı + Tailwind `@theme` + `tailwind.config.ts` (yalnızca IntelliSense için §5 Depo yapısı). **Kabul:** tema jetonu değişimi temaya yansır. **Çıktı:** H2.10 buraya dayanır.
- **H1.14 Ekran kilidi (P7 ile).** 23 ekran + sahibi §1.6 Ekran listesinden dondurulur. **Kabul:** liste donar, sonrası değişiklik PR ister.

## H2 — Ekran temeli haftan

Bu hafta uygulamanın görünen yüzünün temelini atarsın: kabuk, giriş, tasarım sistemi, ilk ekranlar.

- **H2.9 Kabuk + nav + giriş/kayıt.** `api-client` ile kayıt→giriş→jeton akışı (`lib/auth/`, formsnap/superforms/Zod doğrulama §3.1 Mobil yığın). H2.1 auth ucu gelene kadar mock jetonla başlar. **Kabul:** mock akış yeşil; gerçek bağlama H3.15'te yapılır (H2.1 önceki haftadan).
- **H2.10 Tasarım sistemi.** İlk bileşenler + `components.json` (svelte-sonner bildirim baloncuğu, lucide ikonları §3.1 Mobil yığın). **Kabul:** herkes `features/`'tan tüketir + Vitest bileşen testleri yeşil (§12 Test stratejisi).
- **H2.11 Kulüp/profil/ayarlar (P2 destekli).** `tr.json` (+`en.json`) Türkçe metin, 44px dokunma hedefi (§16 Bitti tanımı). H2.3 kulüp uçları gelene kadar örnek kulüp verisiyle başlar. **Kabul:** §16'nın ekran kutuları (Türkçe metin, 44px, koyu mod, yükleme göstergesi).
- **H2.13 SQLite okuma.** Keşif listesi + biletler çevrimdışı durur (§1.5 Kullanıcı görünümü; bilet QR'ı hep okunur) + WAL mode (okuma/yazma çakışmaz). **Kabul:** uygulama internetsiz açılır. **Çıktı:** H4.7 eşitleme kuyruğu buraya dayanır.

## H3 — Platform haftan

- **H3.15 İstemci sözleşme provası (P7 ile).** **Hedef:** `api-client` tipleri canlı API'ya uyar. **Adımlar:** 1. `just api-types` + örnek ekranlarda tüketim denemesi. 2. Uyuşmazlıkları P1'e PR'la (sözleşme kayması §12 Test stratejisi). **Kabul:** prova yeşil, kayma yok. **Çıktı:** H3.3–H3.6 ekranları bu provaya dayanır.
- **H3.9-katılım.** Kabuk/offline ayağının durumu toplantıda sende. **Kabul:** APK durumu + kuyruk durumu raporu hazır.
- **H3.17 Platform sarmalayıcılar.** `lib/platform/` altında konum, pano, QR okutma, bildirim taslakları + test sahte verisi (§4.11 Sayfa kuralları: testlerde tek sahte veri noktası). **Kabul:** testler sahte veriyle koşar. **Çıktı:** H4.5 bildirim ile H5.2 scanner buraya dayanır.
- Ayrıca: P7'nin H3 ekranlarındaki kabuk/nav sorularını yanıtlarsın; buddy P4'ün sorularına yanıt verirsin.

## H4 — Bağlantı haftan

- **H4.5 Bildirim + deep-link (P5 ile).** Eklenti config ile kurulur (0 Rust demek: hiç Rust yazılmaz) + izin akışı gerçek cihazda denenir. **Kabul:** dört §4.8 Bildirim durumu provada gösterilir.
- **H4.7 Eşitleme kuyruğu.** Yazma işlemleri biriktirilir, okuma önceliklidir. **Kabul:** kuyruk birikir ve bağlantı gelince boşalır. **Çıktı:** H5.9 kuyruk bitirme buraya dayanır.
- **H4.9 Deep-link + `geo:` + SSR.** Route'a düşüş `index.html` üzerinden olur (§4.11 Sayfa kuralları); `geo:?q=` ile telefonun harita uygulamasına devredilir (§4.10 Yol tarifi); web sürümünde açma butonu gösterilir. **Kabul:** dış bağlantıdan ilgili ekran açılır.

## H5 — Kuyruk kapanışın

- **H5.9 Kuyruk bitirme.** Bağlantı gelince kuyruktaki işlemler gönderilir (§4.8 Bildirim son satırı: kuyruk + gönderim). **Kabul:** çevrimdışı yapılan işlemler eşitlenir. **Çıktı:** H6.1 çakışma çözümü buraya dayanır.

## H6 — Kapı haftan (lider sensin)

Bu hafta kalite kapısının bekçisisin: eksik varsa H7'ye devretmezsin.

- **H6.1 Eşitleme + çakışma.** Çakışma kuralı yazılı belgede + testli. **Kabul:** çakışma testi yeşil.
- **H6.3 Performans (P7 ile).** §11 Performans hedefleri istemci satırları: açılış < 1.2 sn, bellek < 120 MB, APK < 25 MB, 60 fps kaydırma, LRU 300 MB harita önbelleği, WebP/tembel görsel, 1000+ satırda sanal liste. **Kabul:** `just perf-apk` yeşil; hedefi aşan PR CI'da durdurulur.
- **H6.13 `plugin-updater`.** Kendi imzalı güncelleme bildirimi (§13.2 Dağıtım). **Kabul:** entegrasyon kodda + imzasız provada çalışır; imzalı prova H7.1'de yapılır.
- **H6.7-pay.** Kabuk/offline dokümanını (`runbook.md` mobil kısmı) + eklenti listesi güncelliğini yazarsın (§16 Bitti tanımı: yeni eklenti → §3.1 güncellemesi).
- **Liderlik:** H7'ye eksiksiz devredersin; eksik varsa H7.1'de kimin kapatacağı devir notunda yazar. P7'ye devir notu yazarsın.

## H7 — Kapanış

Kabuk/offline ayağı provada sende (H7.1). Rust 200 satırı aşıldıysa gerekçesi H7.3 kapanışından önce PR'da olur.

## Risklerin

R1 (derleme zinciri): denemede erken belli olur, H1.12'de yakalarsın. R2 (Rust büyümesi): eklenti yetiyorsa özel komut yazılmaz. R5 (ekran yetişmez): H2.10 tasarım sistemini erken dondurur. R13 (harita bellek): bellekte düşük çözünürlük yedeği hazırdır.
