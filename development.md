# ProjectX — Geliştirme Dokümanı

> **Not:** Projenin adı henüz kesinleşmedi. Bu dokümanda geçici ad **ProjectX** kullanılıyor.
> Alan adı örnekleri (`api.projectx.app`) yer tutucudur, isim kararıyla değiştirilecektir.

**Ekip:** 7 kişi · **Süre:** 15 hafta · **Hedef:** Android uygulaması (APK)
**Doküman tarihi:** 2026-10-06 · **Sahip:** P1 (teknik lider)

Bu bir **mobil uygulama** projesi. Teslim edilen şey APK'dır. Web sürümü ikincil amacıyla vardır: ekran paylaşımı orada çalışır ve E2E testleri tarayıcıda koşar.

---

## 1. Bu proje ne

**ProjectX**, Türkiye'nin etkinliklerini düzenli olarak toplayıp tek yerde gösteren bir uygulama. Sonra o etkinliği düzenleyeni bulman, kulüp kurman, duyuru yapman, sohbet kurman ve biletini cebinde taşıman için gerekli olan her şeyi içinde barındırır.

Bugün bir etkinlik aradığında şunlar oluyor: **on ayrı siteye** bakıyorsun — Biletix, Bubilet, bir kültür merkezi, belediye sayfası, Instagram, WhatsApp grubu. Her sitede farklı arayüz, farklı hesap, farklı biçim. Aynı konser üç yerde listelenmiş, hangisi güncel bilmiyorsun. Google'a yazıyorsun, reklam çıkıyor. Sosyal medyada bir paylaşım görüyorsun, ama etkinliğin detayına veya bilet sayfasına ulaşamıyorsun. Bir konsere gidiyorsun, çıkarken aklına "bunu her ay yapıyorlar mı, bunu başka kimler yapıyor, onlardan başka ne var" soruları geliyor — cevabını verecek tek bir yer yok.

ProjectX bunu iki işi birden yapar:

**Derli toplu.** Bilet satışı sitelerini, kültür merkezlerini, üniversite etkinlik sayfalarını, belediye kültür dairelerini düzenli olarak okur, topladığı etkinlikleri **tek bir listede birleştirir**, tekrar eden kayıtları eler. Sen on siteyi tek tek gezmek zorunda kalmazsın. Bilet almak istediğinde seni o etkinliğin kendi satış sayfasına gönderir.

**Üstüne kurulur.** Toplanan etkinliğe bakınca "bunu kim yapıyor, hep mi yapıyor, onlardan başka ne var" sorusunu sorarsın. ProjectX'te kulüp açarsın, etkinlik düzenlersin, duyuru yapar, takipçi toplarsın, sohbet kurarsın. Yani sadece bir arama uygulaması değil — etkinlik düzenleyenlerin de toplandığı bir yer.

### 1.1 Kimler kullanıyor

Uygulamanın tek bir hedef kitlesi yok. Aynı altyapı yedi farklı ihtiyaca cevap veriyor:

**Etkinlik arayan biri** — "Bu hafta sonu ne yapabilirim?" sorusunun cevabını tek ekranda bulmak istiyor. Konser, tiyatro, spor, atölye, fuar... Karışık ilgi alanlarını bir arada görmek, tarihe ve konuma göre süzmek istiyor.

**Bir etkinliğe gitmek isteyen, sonra "bir daha var mı?" diyen** — Bir konsere gitti. Çıkarıyordu ki: "Bunu her ay yapıyorlar mı?" "Bunu başka kimler düzenliyor?" "Onlardan başka ne var?" ProjectX'te kulüp sayfasını açar, o etkinliği düzenleyen kişiyi ve onun etkinlik geçmişini görürsün.

**Düzenli etkinlik yapan bir organizasyon** — Sahne, kulüp, dernek, şirket ekibi, topluluk. Sürekli duyuru yapmak zorunda: "yeni etkinlik açtık", "program değişti", "biletler başladı". Her defterinde Instagram'a, WhatsApp grubuna, e-posta listesine ayrı ayrı yazmak zorunda kalıyor. ProjectX'te kulüp açarsın, duyurularını gönderi olarak paylaşırsın, takipçilerine akışta görünür. **Duğurular kanalı.**

**Bir okul kulübü** — Üye alıyor, etkinlik açıyor, bilet dağıtıyor, katılımcı listesi tutuyor, kapıda giriş kontrolü yapıyor. Bütün bunlar WhatsApp grubunda ve kâğıtta. ProjectX'te kulüp yönetimi, bilet durum makinesi ve QR kapıda kontrol var.

**Bir arkadaş grubu** — "Haftaya basketbol oynayalım", "cumartesi sinema", "cuma yürüyüş". Bir kulüp açarsın. Etkinlik açarsın. Kim katılıyor, kim katılmıyor, kim kimin arabasında gidiyor — hepsi gönderi ve sohbette. Grup sohbeti kaybolmaz, etkinlik bilgisi kaybolmaz.

**Çevresini keşfetmek isteyen biri** — Yeni bir şehre taşındın. Ya da mahallede ne olduğunu merak ediyorsun. "Burada neler var, neler yapılabilir, hangi kafede konser var, hangi salonda atölye yapılıyor" sorusunu cevaplayacak bir harita.

**Yalnızca sohbet etmek isteyen biri** — Etkinlikle ilgisi yok; sadece yazışmak, konuşmak, görüntülü konuşmak istiyor. Kulüp sohbet odası, özel mesajlaşma, sesli ve görüntülü arama — hepsi çalışır. Etkinlik şart değil.

### 1.2 Uygulama şunları yapıyor

**Derli toplu etkinlik listesi** — Bilet satışı siteleri, kültür merkezleri, üniversite etkinlik sayfaları ve belediye duyuruları düzenli olarak toplanır. Hepsini tek listede görürsün. Aynı etkinlik üç sitede listelenmişse tek kayıt olarak görünür, altında "şu kaynaklarda da listeleniyor" yazar. Kaynakların tamamı ve toplama sırası §1.4'te.

**Yakınındakini bul** — Haritada çevrendeki etkinlikleri görürsün. "2 km yakınımda bu hafta sonu ne var?" dersen, liste hazırlanır. Tarihe, konuma, fiyata, kategoriye göre süzersin.

**Seni ilgilendirenleri öner** — İlgi alanlarını girersin, bir şeyleri beğenirsin, kulüpleri takip edersin. ProjectX ne önerdiğini **söyler**: "bunu önerdik çünkü 1,5 km uzakta, takip ettiğin bir kulübün etkinliği ve geçen ay aynı yerde 40 kişi katılmış". Kararı sen verirsin.

**Kulüp aç ve yönet** — Bir kulüp açarsın. Üye alırsın, rol verirsin, davetiye gönderirsin. Kulüp etkinlik açar, bilet tipi ve fiyat tanımlar. Kulübün sayfası bir vitrin olur: kimler var, ne yapıyorlar, yaklaşık etkinlikleri neler.

**Etkinlik duyurusu aracı** — Kulüpler gönderi paylaşır: fotoğraf, duyuru metni, etkinlik tanıtımı, dış bağlantı. Takipçileri bunları akışında görür. Yeni etkinlik duyurusu, program değişikliği, iptal bildirimi — hepsi burada.

**Biletini al, QR kodun ol** — Etkinliğe katılırsın. Biletin telefonda QR kod olarak durur. Kapıda organizatör QR'ı okutur, girişin onaylanır. Biletini kaybetmezsin, çevrimdışıyken de okunur. Birden fazla bilet alabilirsin — grup bileti senin alıp arkadaşlarına dağıtabilirsin.

**Davetiyeni paylaş** — Davetiye linki üretirsin, WhatsApp'tan arkadaşına atarsın. Arkadaşın linke tıklar, kulübe üye olur veya etkinliğe kaydolur. Kaç kişide kullanıldığını görürsün.

**Yazış, konuş, gör** — Metin sohbeti, sesli arama, görüntülü arama, dosya paylaşımı. Kulüp sohbet odası, etkinlik odası, kişisel konuşma. Yalnızca metin de olur — katılan herkesin görüntü açması zorunda değil.

**Uzaktan katıl** — Online etkinliklerde odaya girersin. Ses ve görüntü, ekran paylaşımı (web sürümünde), dosya paylaşımı.

**Çevrendeki yerleri gör** — Haritada sadece etkinlik olan yerler değil, etkinlik yapılabilecek yerler de görünür: tiyatro, konser salonu, kültür merkezi, kampüs, kütüphane, kahve, bar. "Burada başka ne olabilir?" sorusunu da cevaplıyorsun.

**Kulüpleri takip et** — Bir kulübü takip edersin. Gönderileri akışına düşer, etkinlikleri önerilerde öne çıkar. Üye olmadan da takip edebilirsin.

Takipçilik ile üyelik farklıdır:

| | Üyelik | Takipçilik |
|---|---|---|
| Kim ekler | Yönetici ekler | Sen kendin takip edersin |
| Rol | Var (sahibi, yönetici, moderatör, üye) | Yok |
| Kapalı kulüp içeriği | Görür | Görmez |
| Gönderi paylaşabilir mi | Yönetici/mod. | Hayır |

Bir kulübün 20 üyesi, 2.000 takipçisi olabilir. Bu yüzden iki ayrı kayıt tutulur.

**Kulüp gönderileri** — Kulüpler fotoğraf paylaşır, duyuru yapar, etkinlik tanıtır. Gönderileri beğenirsin, yorum yazarsın. Görünürlük üç kademede:

| Kime | Nerede |
|---|---|
| Herkese açık | Uygulamada herkes görebilir |
| Takipçilere | Sadece kulübü takip edenler |
| Sadece üyelere | Yalnızca kulüp üyeleri |

**Biletini cebinde taşı** — Biletler, davetiyeler ve etkinlik takvimi tek ekranda.

### 1.3 Ne yapmıyoruz

Dürüst olmak gerekirse, sınırlarımız net:

- **Gerçek ödeme alma yok.** iyzico, Stripe gibi kurumlarla sözleşme, vergi numarası ve banka onayı gerekiyor. Ders projesinde yapılmıyor. Bilet sistemi var, ödeme adımı organizatör tarafından elle onaylanıyor.
- **Telefonda ekran paylaşımı yok.** Android'un bu özelliği teknik olarak yok. Web sürümünde çalışıyor.
- **Uygulama kapalıyken bildirim yok.** Açıkken anında bildirim geliyor. Google'ın bildirim servisine bağlanmıyoruz.
- **Yol tarifi göstermiyoruz.** "Yol tarifi" düğmesi telefonundaki harita uygulamasını açar. İçindeki yönlendirme bizim değil.
- **Bilet satmıyoruz.** Toplanan etkinliğin detayında "Bilet al" düğmesi ilgili satış sitesini açar. ProjectX üzerinden ödeme alınmaz (§1.4).
- **Video yükleme yok.** Kulüpler fotoğraf paylaşabiliyor, video paylaşamıyor. Gönderiye video bağlantısı eklenebiliyor ya da kendi videomuzu hiç barındırmıyoruz. Gerekçe §4.13.
- **Uygulamaya giriş herkese açık.** Kayıt için okul e-postası şart değiller. Üniversite öğrencileri için ayrıca doğrulama ekledik ama tek koşul değil.

Bu yedi madde kapsam kararıdır; gerekçeleri `docs/adr/` dizinindedir.

### 1.4 Etkinlikler nereden geliyor

ProjectX'teki her etkinlik dört farklı yerden geliyor. Hepsi tek listede birleşiyor ve hepsinin "güvenilirlik" durumu farklı.

**1. Kullanıcının kendi kulübü ve uygulama içi etkinlikleri**

Bir kulüp üyesi ya da yöneticisi uygulamadan etkinlik açtığında bu veri bize aittir. Ad, açıklama, bilet tipi, fiyat, kapasite elle giriliyor. Bu en güvenilir veri — kaynağı biliyoruz, hızlı ve hatasız.

**2. İnternetten toplanan etkinlikler**

Bilet satışı yapan siteler, kültür merkezleri, üniversite etkinlik sayfaları, belediye kültür daireleri. Bunlardan etkinlik bilgisi düzenli olarak toplanıyor ve uygulamaya ekleniyor.

Toplama sırası şöyle çalışıyor:

| Yöntem | Ne zaman | Neden önce bu |
|---|---|---|
| **RSS / Atom** | Site yayınlıyorsa | Sitesi bize izin vermiş. En güvenli yol, en temiz veri |
| **Yapılandırılmış veri (JSON-LD)** | Sayfada `schema.org/Event` varsa | Başlık, tarih, mekan, fiyat hazır geliyor. CSS seçiciye göre daha dayanıklı, sayfa tasarımı değişse bile bozulmuyor |
| **Sayfa okuma (HTML)** | Son çare | En kırılgan yol. Sayfa tasarımı değişince bozuluyor |

Şu an Türkiye'de bu alanda çalışan başlıca yerler: Biletix, Bubilet, Bilet Bende, Biletinial, biletimGO, Biletgo ve Türkiye'nin büyük kültür merkezlerinin kendi etkinlik sayfaları. **Bunların her biri eklenmeden önce `robots.txt` ve kullanım koşulları kontrol edilir.** İzin verilmeyen hiçbir kaynak toplanmaz; gerekirse o kaynak alternatif olarak istenen bir şekilde kullanılır.

**3. Haritalardan gelen yerler**

OpenStreetMap'ten mekan bilgisi alınıyor: tiyatro, konser salonu, kültür merkezi, üniversite kampüsü, kütüphane, belediye salonu, kahve ve bar (bunlarda de ara sıra etkinlik olur). Sınırlarımızı şöyle koyuyoruz:

> Haritada **etkinlik yapılabilecek yerleri** listeliyoruz. Yani "Burada bugün etkinlik var" demiyoruz, **"Burada etkinlik yapılabilir"** diyoruz.

Kullanıcı haritayı açtığında üç farklı şey görüyor:

| Renk | Anlamı |
|---|---|
| **Mavi** | Etkinlik var (etkinlik kayıtlarından) |
| **Gri** | Etkinlik yapılabilir ama şu an programda yok (OSM'den) |
| **Yeşil halka** | Senin kulübünün etkinliği |

Bu ayrım önemli — kullanıcı "mavi nokta yok" deyip "burası boş bir bina" sanmıyor.

**4. Önerilen etkinlikler (üretilmiş, toplanmamış)**

Kullanıcının ilgi alanları, geçmiş tercihleri ve konumu birleştirilerek **yeni** bir şey önerilir. Bu hiçbir yerden toplanmaz, hesaplanır. ProjectX bunu açıkça "öneri" olarak etiketler — kullanıcı bunun gerçek bir etkinlik olduğunu sanmaz.

**Tekrar eden kayıtlar nasıl elenir**

Aynı etkinlik birden fazla sitede listelenmiş olabilir (örneğin konser hem bilet sitesinde hem kültür merkezinde). Başlık benzerliği + aynı mekan + yakın tarih karşılaştırılır, eşleşen kayıtlar birleştirilir.

Bu iki katmanı ayırıyoruz:

| Katman | Nedir | Kim görür |
|---|---|---|
| `source_events` | Kaynaktan gelen ham kayıt. Değişmemiş, ham haliyle durur | Kimse |
| `events` | Normalize edilmiş, tekrar elenmiş, yayınlanmış kayıt | Herkes |

Birleştirme kuralı: `events` kaydı bir kez oluşur, her `source_events` satırı `event_sources` ile ona bağlanır. **Hiçbir kaynak kaydı silinmez** — hangi siteden geldiği saklanır ve kullanıcıya **orijinal bilet sayfasına giden bağlantı** gösterilir. Kullanıcı etkinlik detayında "şu kaynaklarda da listeleniyor" başlığını görür.

Kaynağımız olmayan (toplanmış) etkinlikler `origin=collected`, `trust=collected` ile işaretlenir. Uygulama içinden kulüplerin açtığı etkinlikler `origin=club`, `trust=verified` olur ve arayüzde "kulüp etkinliği" rozetiyle görünür — böylece kullanıcı bir kayıtla diğerini karıştırmaz.

> **ProjectX bilet satmaz, satan siteye yönlendirir.** Toplanan etkinliğin detayında "Bilet al" düğmesi ilgili sitede açılır. Bu, hem teknik hem de hukuki olarak en temiz yol.

### 1.5 Kullanıcı ne görür

Alt çubukta beş sekme var:

```
[Keşfet]  → harita (mekan + etkinlik pin) ve liste, alt sheet: filtre çubuğu
[Akış]    → takip ettiğin kulüplerin gönderileri + sana önerilen etkinlikler
[Kulüpler]→ kulüp listesi/detayı, takip et, üye ol, kulüp gönderileri, kulüp sohbeti
[Biletler]→ QR kod, davetiye linki, takvime ekle, iptal
[Profil]  → ilgi alanları, bütçe, şehir, dil, takip edilenler
```

Sekmeye sığmayan iki yer üst çubuktan açılır: **mesajlar** (`/(tabs)/messages`) ve **bildirimler** (`/notifications`). Altı ayrı sekme yapmadık — parmak erişimi zorlaşıyor ve kulüpler sekmesi gereksiz daralıyordu.

Akışlar:

```
Keşfet → Etkinlik detay → Bilet seç → Kayıt
  ücretsiz: anında | ücretli: rezervasyon (15 dk) → ödeme onayı → QR

Kulüp → Gönderi paylaş (yönetici/mod.) → takipçi görüntüyü beğenir, yorum yazar

Etkinlik detay → Oda → online: ses + görüntü + sohbet + dosya paylaşımı
                              web'de ekran paylaşımı
```

**Çevrimdışı:** Keşif listesi ve alınan biletler akıllı telefonda saklanır, internetsiz açılır. **Bilet QR'ı her zaman okunabilir olmalı** — kapıda şebeke olmayabilir.

### 1.6 Ekran listesi

Hafta 1'de P6 ve P7 birlikte çıkarır. 23 ekran:

| Ekran | Route | Sahip |
|---|---|---|
| Keşfit / harita | `/(tabs)/discover` | P7 |
| Filtre sheet | `FilterSheet` bileşeni | P7 |
| Etkinlik detay | `/events/[id]` | P7 |
| Bilet seçme | `/events/[id]/tickets` | P7 |
| Bilet cüzdanı | `/(tabs)/tickets` | P7 |
| Kulüp listesi | `/(tabs)/clubs` | P6 |
| Kulüp detay | `/clubs/[id]` | P2, P6 |
| Kulüp sohbeti | `/clubs/[id]/chat` | P5 |
| **Mesajlar (DM listesi)** | `/(tabs)/messages` (üst çubuk) | P5 |
| **Özel mesajlaşma** | `/channels/[id]` | P5 |
| **Oda (medya)** | `/events/[id]/room`, `/channels/[id]/room` | P5 |
| Profil | `/(tabs)/profile` | P6 |
| Giriş / kayıt | `/login`, `/register` | P6 |
| Davetiye kabul | `/invite/[code]` | P2 |
| Kapıda doğrulama | `/scanner` | P2, P7 |
| Hakkında / kaynak atfı | `/about` | P7 |
| Ayarlar | `/settings` | P6 |
| Bildirim listesi | `/notifications` | P5 |
| **Takip akışı** | `/(tabs)/feed` | P2, P7 |
| **Takip edilenler** | `/settings/following` | P2 |
| **Takipçiler** | `/clubs/[id]/followers` | P2 |
| **Gönderi oluştur** | `/clubs/[id]/new-post` | P2 |
| **Gönderi yorumları** | `Sheet` bileşeni | P2 |

---

## 2. Nasıl kuruluyor

```
┌──────────────────────────────────────────────────────────────────┐
│  MOBİL — Tauri 2.12 + SvelteKit 3 / Node 24 LTS                 │
│  ├─ Webview: SvelteKit SPA (TypeScript, ssr=false)               │
│  │   Tailwind v4 · bits-ui (davranış) · shadcn-svelte (görsel)  │
│  ├─ src-tauri: Rust — yalnızca kabuk, ~200 satır                 │
│  └─ Yerel SQLite cache · deep-link · yerel bildirim · QR · konum │
└────────────────────────────┬─────────────────────────────────────┘
                             │ HTTPS + WebSocket (OpenAPI 3.1 sözleşmesi)
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  API — Python 3.13 / FastAPI / uv / Uvicorn                      │
│  ├─ REST + OpenAPI 3.1 (Pydantic'ten otomatik)                   │
│  ├─ WebSocket: sohbet, presence, bildirim                         │
│  └─ LiveKit token · JWT auth (argon2id) · medya servisi           │
└──────┬────────────────────┬───────────────────┬──────────────────┘
       │ SQL                │ pub/sub           │ HTTP
       ▼                    ▼                   ▼
 PostgreSQL 17          Valkey 9             Martin (tile)
 + PostGIS 3.5          cache/presence       PostGIS'ten üretir
 + BYTEA medya (§4.9)
       ▲
       │ yazma (staging → publish)
┌──────┴───────────────────────────────────────────────────────────┐
│  VERİ HATTI — Python 3.13 / Dramatiq + APScheduler              │
│  ├─ Scrapy + parsel + lxml: etkinlik/bilet kaynakları            │
│  ├─ Playwright: JS render edilen sayfalar                        │
│  ├─ feedparser + extruct: RSS / JSON-LD öncelikli                 │
│  ├─ Overpass/OSM: mekan & kategori                               │
│  └─ Öneri: aday üretim (PostGIS) + şeffaf skor                   │
└──────────────────────────────────────────────────────────────────┘

  MEDYA   LiveKit v1.13 (self-host, tek node)
  HARİTA  MapLibre GL 6 + PMTiles
  GEOKOD  Nominatim 5.3.2 (self-host)
  ALTYAPI Podman + Caddy + Headscale
```

**Bölümler:** Uygulama (telefonda görünen) → API (sunucu) → Veri katmanı → Veri hattı (etkinlikleri toplayan).

### 2.1 Beş ilke

1. **Sözleşme önce gelir.** API sözleşmesi ve veritabanı şeması koda göre hazırlanır. Şema kilitlidir; değişiklik PR ile yapılır. Yedi kişi paralel çalışırken asıl kaybedilecek zaman budur.
2. **Tek depo.** Şema, tipler ve kod aynı yerde durur, aynı PR ile değişir.
3. **Telefon ilk.** Mobil şebeke güvenilmez. Ekranda gördüğün her şey akıllı telefonda saklanır, sunucuya bağlanınca eşitlenir.
4. **Ölçülebilir hedefler.** Boşta bellek 120 MB altında, açılış 1.2 saniyenin altında, APK 25 MB altında. Hedefler baştan konur, sonra ölçülür.
5. **Açık kaynak varsayılan.** Her bağımlılık lisansı ve bakım durumuyla değerlendirilir.

---

## 3. Kullanılan teknolojiler

Buradaki sürümler o an kullanılan sürümleri gösterir, bilgi amaçlıdır. **Kurulumun tek doğruluk kaynağı `mise.toml`'dır.** Bir sürüm burada güncellenmez; güncelleme yapılacaksa `mise.toml` düzenlenir ve buradaki satırlar gerekiyorsa tazelenir.

### 3.1 Telefonda (Svelte)

| İş | Ne |
|---|---|
| Uygulama kabuğu, APK üretimi | Tauri 2.12 |
| Sayfalar, bileşenler | SvelteKit 3 + Svelte 5 |
| JavaScript runtime, paket yönetimi | Node 24 LTS + npm |
| Derleme | Vite 8 + TypeScript 7 |
| Stil | Tailwind CSS 4 |
| Erişilebilir bileşen mantığı (focus trap, klavye, ARIA) | bits-ui 2.19 |
| Hazır bileşenlerin görünümü (koda kopyalanır) | shadcn-svelte 1.7 |
| Formlar ve doğrulama | formsnap + sveltekit-superforms + Zod 4 |
| Sunucudan gelen veriyi önbellekleme | @tanstack/svelte-query 6 |
| Uzun listelerde akıcılık | @tanstack/svelte-virtual 3 |
| Küçük bildirimler (toast) | svelte-sonner |
| Takvim | @internationalized/date |
| İkon | @lucide/svelte |
| Harita | MapLibre GL 6 |
| Harita paketleri | PMTiles 4 |
| Ses ve görüntülü görüşme | livekit-client 2.22 |
| Açıklama metni gösterimi | marked + DOMPurify |
| Görsel küçültme (telefonda) | @jsquash/resize |
| Testler | Vitest + happy-dom |
| E2E testleri (web) | @playwright/test |

**Bileşenler üç katmanlıdır:**

| Katman | Ne sağlar | Nerede |
|---|---|---|
| bits-ui | Erişilebilirlik ve davranış. Focus tuzağı, klavye navigasyonu, ekran okuyucu etiketleri | npm'den kurulur |
| shadcn-svelte | Buton, kart, pencere gibi hazır parçaların **görünümü** | `packages/ui/src/lib/components/ui/` — kopyalanan kod, bağımlılık değil |
| Bizim yazdıklarımız | Sadece bize ait olan parçalar | `packages/ui/src/lib/features/` |

Bizim yazdığımız 13 parça:

| Alan | Parçalar |
|---|---|
| Keşif | `EventCard`, `VenueMarker`, `FilterSheet` |
| Bilet | `TicketRow`, `QRDisplay` |
| Kulüp | `ClubBadge`, `PostCard`, `PostComposer`, `FollowButton` |
| Sohbet | `ChatBubble`, `PresenceDot`, `VoiceBar`, `VideoTile` |

Bu ayrım sayesinde tasarım değişince erişilebilirlik bozulmaz, davranış değişince tasarım bozulmaz.

### 3.2 Sunucuda (Python)

| İş | Ne |
|---|---|
| Python | 3.13 |
| Paket yönetimi | uv |
| Web framework | FastAPI 0.142 |
| Sunucu | Uvicorn + uvloop |
| Veri doğrulama ve şema | Pydantic 2.13 |
| Sorgu | SQLAlchemy (Core + ham SQL) |
| Veritabanı bağlantısı | psycopg 3 |
| Göçler (migration) | Alembic |
| Veritabanı | PostgreSQL 17 + PostGIS 3.5 |
| Önbellek, anlık mesaj dağıtımı, çevrimiçi durumu | Valkey 9 |
| Parola şifreleme | argon2-cffi |
| Oturum jetonu | PyJWT |
| Günlük kayıt | structlog |
| Hız sınırı | limits |
| Kod kalitesi | ruff |
| Medya erişim jetonu | LiveKit (livekit-api) |
| QR kod üretimi | segno |
| Yük testi | k6 |
| Güvenlik taraması | pip-audit, bandit, Trivy |

### 3.3 Etkinlik verisini toplayan kısım

| İş | Ne |
|---|---|
| Görev kuyruğu | Dramatiq + APScheduler |
| Web sayfası toplama | Scrapy 2.19 |
| HTML'den bilgi çıkarma | parsel + lxml 6.1 |
| JavaScript ile yüklenen sayfalar | Playwright |
| RSS ve yapılandırılmış veri | feedparser + extruct |
| Tekrarlı kayıtları eleme | rapidfuzz |
| Coğrafi doğrulama | shapely |
| Tablo işleme | polars 2 (Rust çekirdekli; pandas yerine — hafiflik) |
| Test verisi | faker |

### 3.4 Sunucu tarafı donanım ve araçlar

| İş | Ne |
|---|---|
| Konteyner çalıştırma | Podman |
| Konteynerleri terminalden izleme | oxker |
| Ortak komutlar | just |
| Araç sürüm sabitleme | mise |
| HTTPS otomatik kurulum | Caddy |
| Sunucuya port açmadan erişim | Headscale |
| Harita paketi sunucusu | Martin |
| Hazır harita paketi | Protomaps basemap |
| Adres→koordinat çevirisi | Nominatim |
| Açık kaynak harita verisini veritabanına alma | osm2pgsql |
| API sözleşme testleri | Hurl |
| Python testleri | pytest |
| Telefon testleri | adb + UI Automator |
| Sunucu izleme | Grafana + Loki |
| Hata takibi | GlitchTip |
| Dokümantasyon | mdBook |
| Otomatik doğrulama testleri (faz 2) | schemathesis |

### 3.5 Kullanılmayacaklar

Listeye `deny.txt` dosyası üzerinden eklenir. CI'ın `deny` adımı bu listeyi kontrol eder (§13.1). Gerekçeler `docs/adr/0003-declined-dependencies.md` içinde.

---

## 4. Kapsam kararları

Bu 13 karar Sprint 0'da ekip tarafından yazılı olarak kabul edilir. Gerekçeler `docs/adr/` dizinindedir.

| # | Karar | Kısaca |
|---|---|---|
| 4.1 | Ekran paylaşımı | Web'de var, telefonda yok |
| 4.2 | Ödeme | Tahsilat yok, bilet akışı var |
| 4.3 | Veri kaynakları | Her kaynak için ToS kontrolü kayıt altında, en az 2 kaynak |
| 4.4 | Rust yüzeyi | Sadece P6 dokunur. Bütçe 200 satır |
| 4.5 | Backend dili | Python |
| 4.6 | Derleme zinciri | Uygulama kodunda Java/Kotlin yok. Derleme araçları JDK/NDK kullanıyor |
| 4.7 | Sürüm sabitleme | Tek doğruluk kaynağı `mise.toml`. Dokümandaki sürümler bilgi amaçlı |
| 4.8 | Bildirim | Açıkken anında, kapalıyken yok |
| 4.9 | Dosya saklama | Veritabanı içinde. Avatar 2 MB, görsel 5 MB |
| 4.10 | Yol tarifi | `geo:` ile telefonun harita uygulaması |
| 4.11 | Sayfa kuralları | `ssr = false`, `adapter-static` |
| 4.12 | Format kuralları | Her dosya tipinin tek bir format aracı var |
| 4.13 | Kulüp gönderileri | Metin + fotoğraf + dış bağlantı |

### 4.1 Ekran paylaşımı

Ekran paylaşımı web sürümünde çalışır, telefonda yok. Android'un WebView katmanı `getDisplayMedia` sağlamaz.

Telefonda paylaşım şunlarla yapılır: belge gönderme, bağlantı paylaşma, dosya atma.

### 4.2 Ödeme

Tahsilat yapılmaz. Bilet akışı tam çalışır, ödeme onayını organizatör elle verir.

Tahsilat için ödeme kuruluşuyla sözleşme, vergi numarası ve banka onayı gerekir. Bilet durum makinesi:

```
reserved → pending_payment → paid → used
     │            │           │
     └────────────┴───────────┴──→ cancelled / expired
                                  refunded
```

| Durum | Ne oldu |
|---|---|
| `reserved` | Rezervasyon yapıldı, 15 dakika süre var |
| `pending_payment` | Ödeme bekleniyor — organizatör onaylayacak |
| `paid` | Organizatör onayladı, QR geçerli |
| `free_granted` | Ücretsiz bilet, doğrudan geçerli |
| `used` | Kapıda okutuldu |
| `cancelled` / `expired` / `refunded` | İptal, süre doldu, iade |

Organizatör kulüp panelinden `pending_payment` kayıtlarını listeler, tek dokunuşla `paid` yapar. Kullanıcı tarafında birkaç saniyelik bekleme olarak görünür.

### 4.3 Veri kaynakları

| Kaynak | Ne için | Yükümlülük |
|---|---|---|
| OpenStreetMap | Mekan, kategori, koordinat | Kaynak atfı uygulamada görünür |
| Nominatim | Adresi koordinata çevirme | Kendi sunucumuzda çalışır |
| Overpass API | Mekan toplama | Ağır sorgular kendi sunucumuzdan |
| Etkinlik/bilet siteleri | Etkinlik bilgisi | Her hedef için kullanım koşulları ayrı incelenir ve `docs/data-sources.md`'ye yazılır |
| Harita paketleri | Martin, kendi sunucumuz | Dışarıdan hazır paket kullanılmaz |

**Kural:** Kaynak ekleyen PR, `docs/data-sources.md` dosyasına kaynağı, ToS kontrol tarihini ve istek hızını ekler. Her bilgi tipi en az 2 farklı kaynaktan gelir.

### 4.4 Tauri Rust yüzeyi

> **P6 dışında hiçkimse `src-tauri/` dizinine dokunmaz.**

| İhtiyaç | Çözüm | Yazılacak Rust |
|---|---|---|
| Veri önbelleği, konum, bildirim, QR okutma, derin link, parmak izi, pano, işletim sistemi bilgisi, güncelleme | Tauri eklentileri (config) | 0 |
| En fazla 2 özel komut | P6 yazar | ~30 satır |

**Bütçe: 200 satır.** Aşarsa gerekçe PR'da yazılır.

### 4.5 Backend dili: Python

Sunucu Python ile yazılıyor. Pydantic OpenAPI 3.1'i otomatik üretir, sözleşme elle yazılmaz. Veri katmanı ihtiyaçları (`polars`, `lxml`, `parsel`, Playwright, geokodlama) Python'da hazır.

### 4.6 Derleme zincirinde Java ve Kotlin

Uygulama kodunda Java veya Kotlin yok. APK derlenirken JDK ve NDK devreye girer.

Tauri, Android'deki sistem ekranlarına (kamera, dosya seçici, konum, bildirim) hazır gelen Java/Kotlin eklenti kodu üzerinden erişir. Bunu değiştirmek Tauri'yi değiştirmek demek.

| Katman | Dil | Sahip |
|---|---|---|
| Arayüz, mantık, tasarım | TypeScript + Svelte | Ekip |
| Tauri kabuğu | Rust, ~200 satır | P6 |
| Android sistem köprüsü | Java/Kotlin | Tauri eklentisi, hazır gelir |

### 4.7 Sürüm sabitleme

Tam sürüm tek yerdedir: `mise.toml`. Dockerfile ve README'de tekrarlanmaz — `mise install` herkesin aynı sürümü kurmasını sağlar.

Bu dokümanın §3 bölümünde sürümler bilgi amaçlı listelenir. Çelişki olursa `mise.toml` kazanır.

### 4.8 Bildirim

Uygulama açıkken bildirim gelir, kapalıyken gelmez.

| Durum | Bildirim |
|---|---|
| Uygulama açık, WebSocket bağlı | Anında, ekran içi bildirim + rozet |
| Uygulama açık, arka planda | Anında, sistem bildirimi |
| Uygulama kapalı | Yok |
| Bildirim açıkken internet yok | Kuyruğa alınır, bağlantı gelince gönderilir |

Bildirim sunucuda `notifications` tablosunda tutulur; uygulama açılınca `GET /notifications` ile çekilir. `devices` tablosunda push token yoktur — sunucu kime ne göndereceğini bilmez. Tablo çevrimiçi durumu ve sürüm bilgisi tutar.

### 4.9 Dosya saklama

```sql
media(id UUID PK, owner_id UUID FK,
      kind ENUM(avatar,club_cover,event_image,chat_attachment,club_post_image),
      content_type TEXT, byte_size INT, sha256 TEXT,
      data BYTEA NOT NULL, created_at TIMESTAMPTZ)
```

- Boyut sınırı: avatar 2 MB, kulüp afişi / etkinlik görseli / kulüp gönderi görseli 5 MB
- Kulüp gönderi görseli: gönderi başına en fazla 4 adet
- Dosya tipi sunucuda gerçek içerikten okunur, uzantıya bakılmaz
- Telefonda yüklemeden önce küçültülür ve WebP'ye çevrilir
- Sunum: `GET /media/{id}` — önbellek başlıklarıyla
- Kullanıcı, kulüp ve etkinlik kayıtları görseli `*_media_id` ile tutar; dosya yolu veya URL yazılmaz
- Harici depoya taşımak gerekirse: tek migration. Uygulama kodu değişmez

### 4.10 Yol tarifi

"Yol tarifi" düğmesi telefonun kendi harita uygulamasını açar.

```
[Etkinlik detay] → "Yol tarifi" → geo:?q=lat,lng(Etkinlik adı)
                          → telefonun harita uygulaması açılır
```

`geo:` bir web standardı (RFC 5870); Android'de Google Haritalar, Yandex, HERE ve OpenStreetMap anlar. Uygulama koordinatı devreder, yönlendirmeyi hesaplamaz.

Android'de her zaman çalışır. Web sürümünde `geo:` desteklenmiyorsa harita uygulamasını açan buton gösterilir.

### 4.11 Sayfa kuralları

| Konu | Kural |
|---|---|
| Sunucu tarafı sayfa üretimi | `ssr = false` ve `prerender = false` — her zaman |
| Adapter | `@sveltejs/adapter-static`, `fallback: 'index.html'` |
| Derin link | `index.html` üzerinden route'e düşer |
| Telefon API'leri | Tüm çağrılar `src/lib/platform/` üzerinden. Testlerde tek noktadan sahte veri |
| Tarayıcı API'leri | İzin ve çağrı Tauri eklentisi üzerinden |
| Stil | Tailwind `@theme` (`tokens.css`) |

### 4.12 Format kuralları

| Araç | Hangi dosyalar |
|---|---|
| Prettier | `.ts` `.js` `.json` `.md` `.svelte` |
| `ruff format` + `ruff check` | `.py` |

Her araç yalnızca kendi dosyalarına dokunur.

### 4.13 Kulüp gönderileri: fotoğraf var, video yükleme yok

Kulüp gönderisi = metin + fotoğraflar + dış bağlantı. Video yüklenmez; kulüpler bağlantı verir (YouTube, Vimeo, kendi çekim linki).

Gönderi içeriği:

| Alan | Kural |
|---|---|
| Metin | Zorunlu değil, fotoğraf varsa da tek başına yazılabilir |
| Fotoğraf | Gönderi başına en fazla 4 adet, her biri 5 MB |
| Bağlantı | Tek adet. Kapak görseli gösterilir, tıklayınca dışarı açılır |
| Görünürlük | `public`, `followers` (varsayılan) veya `members` |

Video barındırma kapsam dışı — bkz. `docs/adr/0008-no-video-upload.md`.

---

## 5. Depo yapısı

```
/
├── apps/
│   ├── mobile/                      # Tauri 2 + SvelteKit — P6, P7
│   │   ├── src/
│   │   │   ├── routes/              # sayfa iskeletleri
│   │   │   ├── lib/
│   │   │   │   ├── api/             # sunucu istekleri + sorgu anahtarları
│   │   │   │   ├── auth/            # jeton saklama, giriş akışı
│   │   │   │   ├── realtime/        # WebSocket istemcisi + çevrimiçi durumu
│   │   │   │   ├── offline/         # SQLite okuma modeli + eşitleme kuyruğu
│   │   │   │   └── platform/        # Tauri eklenti sarmalayıcıları
│   │   │   └── locales/tr.json + en.json  # arayüz metinleri (TR birincil, EN ikinci)
│   │   ├── static/
│   │   ├── src-tauri/               # ⚠️ SADECE P6
│   │   │   ├── capabilities/        # android.json / desktop.json
│   │   │   ├── tauri.conf.json
│   │   │   └── src/
│   │   ├── package.json
│   │   ├── svelte.config.js
│   │   ├── vite.config.ts
│   │   └── tailwind.config.ts       # SADECE IntelliSense için
│   │
│   ├── api/                         # FastAPI — P1, P2, P4, P5
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── core/                # config, db, valkey, security, errors
│   │   │   ├── domain/              # veritabanından bağımsız iş kuralları
│   │   │   ├── schemas/             # Pydantic → OpenAPI
│   │   │   ├── routers/             # endpoint'ler
│   │   │   ├── services/            # iş mantığı
│   │   │   ├── repos/               # SQLAlchemy / ham SQL
│   │   │   ├── realtime/            # WebSocket merkezi
│   │   │   ├── media/               # LiveKit jetonu + medya servisi
│   │   │   └── notifications/
│   │   ├── alembic/                 # migration — P1 sahipliği
│   │   ├── hurl/                    # API sözleşmesi testleri
│   │   ├── tests/
│   │   └── pyproject.toml
│   │
│   └── pipeline/                    # ETL — P3
│       ├── src/pipeline/
│       │   ├── sources/             # her kaynak bir adaptör
│       │   ├── normalize/           # başlık, tarih, fiyat, konum
│       │   ├── dedup/               # rapidfuzz + coğrafi
│       │   ├── geo/                 # Nominatim / Overpass
│       │   └── rank/                # öneri skorlama
│       ├── tests/fixtures/
│       └── pyproject.toml
│
├── packages/
│   ├── ui/                          # tasarım sistemi — P6
│   │   ├── src/lib/components/ui/   # shadcn-svelte kopyaları
│   │   ├── src/lib/features/        # bizim bileşenlerimiz
│   │   ├── src/tokens.css           # tema kaynağı
│   │   ├── src/base.css
│   │   └── components.json
│   └── api-client/                  # API'den üretilen tipler + doğrulama şemaları
│
├── infra/
│   ├── compose.yaml                 # postgres+postgis, valkey, livekit,
│   │                                #   caddy, martin, nominatim
│   ├── compose.dev.yaml
│   ├── martin/martin.yaml
│   ├── livekit/livekit.yaml
│   ├── caddy/Caddyfile
│   ├── headscale/config.yaml
│   └── docs/ports.md
│
├── docs/
│   ├── plan/                        # 7 haftalık yürütme planı (ana-plan + p1-p7)
│   ├── book.toml + SUMMARY.md
│   ├── adr/                         # karar kayıtları + README.md dizini
│   ├── data-sources.md
│   └── runbook.md
│
├── deny.txt                         # CI'ın okuduğu yasaklı bağımlılık listesi (ADR-0003)
│
├── development.md                   # ANA KARAR DOKÜMANI (kökte; §4.7'deki gibi sürümler hariç her şey)
├── AGENTS.md                        # çalışma anlaşması (felsefe + kurallar)
│
├── package.json                     # npm çalışma alanı kökü
├── mise.toml                        # araç sürüm sabitleme
├── justfile                         # ortak komutlar
└── .editorconfig / .prettierrc / ruff.toml
```

### 5.1 Nerede ne

| Ne | Nerede |
|---|---|
| Sayfa (route) | `apps/mobile/src/routes/` |
| Hazır bileşen görünümleri | `packages/ui/src/lib/components/ui/` |
| Bize ait bileşenler | `packages/ui/src/lib/features/` |
| Sunucudan veri çeken sorgular | `apps/mobile/src/lib/api/` |
| Arayüz durumu (açık/kapalı, seçili sekme) | `apps/mobile/src/lib/` |
| Telefon API'lerine erişim | `apps/mobile/src/lib/platform/` |

**Kural:** `packages/ui` içinde sunucu isteği, jeton veya rota bilgisi olmaz. `routes/` içinde elle yazılmış stil sınıfı olmaz — görsel her şey `packages/ui`'den gelir.

---

## 6. Ekip

| # | Rol | Alan | Ana çıktı |
|---|---|---|---|
| **P1** | Tech Lead — Backend & Infrastructure | Sözleşme, veritabanı şeması, kimlik doğrulama, sunucu kurulumu | API sözleşmesi, veritabanı şeması, göçler, kimlik doğrulama, Podman/Caddy, `mise`/`just` |
| **P2** | Backend Engineer — Ticketing & Social | Kulüp/üyelik, etkinlik, kayıt, bilet + QR, davetiye, **kulüp sosyal medyası** | Kulüp yönetimi, bilet durum makinesi, QR üretim/doğrulama, davetiye, takipçilik, kulüp gönderileri |
| **P3** | Data Engineer (Miner) | Kaynak adaptörleri, temizleme, tekrar eleme, veri kalitesi | 4-6 kaynak, veri kalitesi panosu, `data-sources.md` |
| **P4** | Backend Engineer — Discovery & Ranking | Mekan/etkinlik arama, coğrafi sorgu, sıralama | Keşif akışı, mesafe sorguları, şeffaf skor |
| **P5** | Backend Engineer — Realtime & Media | Sohbet, özel mesaj, çevrimiçi durumu, bildirim, ses/görüntü | WebSocket sohbet, kulüp kanalları, özel mesaj, LiveKit odaları |
| **P6** | Mobile Engineer — Core & Design System | Tauri kabuğu, yönlendirme, giriş ekranları, çevrimdışı önbellek, tasarım sistemi | Uygulama iskeleti, giriş/kayıt, navigasyon, eşitleme kuyruğu, `packages/ui` |
| **P7** | Mobile UI Engineer & QA | Keşif/harita, etkinlik detayı, bilet cüzdanı, E2E testleri, sürüm | Harita + filtre, etkinlik detayı, bilet cüzdanı, E2E paketi, imzalı APK |

P1 sözleşme ve şema sahibi. P3'ün veri toplama işi Sprint 0'da P1 ile başlar. P4'e Sprint 0'da iki gün PostGIS eğitimi verilir. P5 medya katmanını tek elinde tutar. P6 ve P7 ekranları birlikte yazar. P2'nin alanı kulüp merkezli olduğu için sosyal medya kısmı da ona ait.

### 6.1 Hafta 6 değerlendirmesi

P2, P5 ve P7'nin o sprint için üstlendikleri işlerin yarısından azı bittiyse, aşağıdaki sırayla ilk iş düşer:

1. Öneri motorunun 3. aşaması (makine öğrenmesi) — zaten Faz 2'ye ertelenmişti
2. Kulüp gönderilerinde fotoğraf — metin gönderi çalışır, görsel Sprint 4'e kayar
3. Yorumlar — beğeni çalışır, yorum sonra gelir
4. Ekran paylaşımı (web)

Takipçilik, kulüp gönderileri (metin), sohbet, özel mesaj, bilet ve QR düşürülemez. Birden fazlası düşecekse hafta planı yeniden yazılır.

### 6.2 Çalışma kuralları

- **Trunk-based.** `main` her zaman çalışır durumda durur. Branch ömrü en fazla 3 gün.
- **PR:** Tek konu, en fazla 400 satır, CI yeşil, bir onay. Veritabanı şeması ve göç değişikliklerinde P1 onayı gerekir.
- **Doğrudan `main`'e gönderim yok** (`main` ve `release/*` korumalı).
- **CODEOWNERS** alan sahipliğini otomatik reviewer atar.
- **Ritüel:** Haftalık 30 dakika senkron, aylık 1 saat değerlendirme. Eşleşme çiftleri: P1-P3, P2-P5, P4-P6.
- **Dil:** Kod, commit, doküman ve PR açıklamaları İngilizce. Arayüz dili Türkçe birincil, İngilizce ikincil; görünen tüm metinler `locales/tr.json` + `locales/en.json` içinde.
- **Sürüm:** Tam sürüm yalnızca `mise.toml` içinde sabitlenir.
- **`just` her şeyi çalıştırır.** Herkes kendi kabuğunda geçici komut yazmaz.

### 6.3 Sorumluluk matrisi

| Alan | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|---|---|---|---|---|---|---|---|
| API sözleşmesi | **A** | C | I | C | C | C | I |
| Veritabanı göçü | **A** | C | I | C | C | I | I |
| Kimlik doğrulama | **A/R** | I | — | I | C | C | I |
| Kulüp / üyelik | C | **A/R** | — | I | C | C | C |
| Takipçilik | I | **A/R** | — | C | I | C | C |
| Kulüp gönderileri | I | **A/R** | — | I | I | C | C |
| Etkinlik / kayıt | C | **A/R** | C | C | C | C | C |
| Bilet / QR / davetiye | C | **A/R** | — | — | I | C | C |
| Veri toplama | C | I | **A/R** | C | — | — | I |
| Coğrafi arama | C | I | C | **A/R** | — | I | C |
| Öneri sıralama | I | I | C | **A/R** | — | I | C |
| Sohbet / WebSocket | I | I | — | — | **A/R** | C | C |
| Ses ve görüntü | C | I | — | — | **A/R** | C | C |
| Tauri kabuğu / Rust | C | I | — | — | C | **A/R** | C |
| Tasarım sistemi | I | C | — | I | C | **A/R** | C |
| Keşif / harita ekranı | I | C | — | C | — | C | **A/R** |
| Bilet cüzdanı ekranı | I | C | — | — | — | C | **A/R** |
| Sunucu kurulumu / CI | **A/R** | I | C | I | I | I | C |
| E2E testleri | C | C | I | I | C | C | **A/R** |
| Sürüm çıkarma | C | I | — | — | I | C | **A/R** |

`A` Sorumlu · `R` Yapan · `C` Danışılan · `I` Bilgilendirilen

---

## 7. Veri modeli

```sql
-- Kullanıcı
-- Görsel referansları media tablosunu gösterir; dosya içeriği BYTEA'da durur (§4.9)
users(id UUID PK, email CITEXT UNIQUE, password_hash TEXT, display_name TEXT,
      avatar_media_id UUID FK → media, bio TEXT, city TEXT,
      interests TEXT[], locale TEXT DEFAULT 'tr',
      budget_minor INT, budget_currency CHAR(3) DEFAULT 'TRY',
      created_at TIMESTAMPTZ)
refresh_tokens(id UUID PK, user_id UUID FK, token_hash TEXT UNIQUE,
               expires_at TIMESTAMPTZ, revoked_at TIMESTAMPTZ, device_id TEXT)
-- Cihaz kaydı yalnızca çevrimiçi durumu ve sürüm bilgisi için (bkz. §4.8)
devices(id UUID PK, user_id UUID FK, platform TEXT, app_version TEXT,
        last_seen TIMESTAMPTZ)

-- Kulüpler
clubs(id UUID PK, name TEXT, slug CITEXT UNIQUE, description TEXT, city TEXT,
      cover_media_id UUID FK → media, owner_id UUID FK, created_at TIMESTAMPTZ)
club_members(club_id UUID FK, user_id UUID FK, role ENUM(owner,admin,moderator,member),
             joined_at TIMESTAMPTZ, PRIMARY KEY (club_id, user_id))
club_invitations(id UUID PK, club_id UUID FK, email TEXT, code TEXT UNIQUE,
                 role ENUM, expires_at TIMESTAMPTZ, accepted_by UUID, created_by UUID)

-- Kulüp sosyal medyası (§1)
-- Üyelik ve takipçilik AYRI tutulur: bir kulübün 20 üyesi, 2000 takipçisi olabilir
club_followers(club_id UUID FK, user_id UUID FK, created_at TIMESTAMPTZ,
               PRIMARY KEY (club_id, user_id))
CREATE INDEX ON club_followers (user_id, created_at DESC);   -- "ne takip ediyorum" akışı

club_posts(id UUID PK, club_id UUID FK, author_id UUID FK,
           body TEXT,
           visibility ENUM(public,followers,members) DEFAULT 'followers',
           link_url TEXT,                                    -- dış video/bağlantı (§4.13)
           created_at TIMESTAMPTZ, edited_at TIMESTAMPTZ, deleted_at TIMESTAMPTZ)
CREATE INDEX ON club_posts (club_id, created_at DESC) WHERE deleted_at IS NULL;

club_post_media(post_id UUID FK, media_id UUID FK, position SMALLINT,
                PRIMARY KEY (post_id, media_id))
club_post_likes(post_id UUID FK, user_id UUID FK, created_at TIMESTAMPTZ,
                PRIMARY KEY (post_id, user_id))
club_post_comments(id UUID PK, post_id UUID FK, author_id UUID FK,
                   body TEXT, created_at TIMESTAMPTZ, deleted_at TIMESTAMPTZ)
CREATE INDEX ON club_post_comments (post_id, created_at);

-- Coğrafi
venues(id UUID PK, name TEXT, address TEXT, city TEXT,
       geom GEOMETRY(POINT,4326), category TEXT, source TEXT, source_ref TEXT,
       capacity INT, wheelchair_accessible BOOL, created_at TIMESTAMPTZ)
source_events(id UUID PK, source TEXT, source_ref TEXT, title_raw TEXT,
              venue_geom GEOMETRY(POINT,4326), starts_at TIMESTAMPTZ, ends_at TIMESTAMPTZ,
              price_minor INT, currency CHAR(3), url TEXT, payload JSONB,
              fetched_at TIMESTAMPTZ, content_hash TEXT)
CREATE INDEX ON source_events USING GIST (venue_geom);
CREATE UNIQUE INDEX ON source_events (source, source_ref);

-- Etkinlikler
-- events = kullanıcıya gösterilen kayıt (ya kulüp girdisi ya da toplamış kayıt)
-- source_events = kaynaklardan gelen ham kayıt (kullanıcıya gösterilmez)
events(id UUID PK, club_id UUID FK, venue_id UUID FK, title TEXT, description TEXT,
       category TEXT, cover_media_id UUID FK → media, starts_at TIMESTAMPTZ, ends_at TIMESTAMPTZ,
       is_online BOOL, online_url TEXT, capacity INT,
       origin ENUM(club,collected) DEFAULT 'club',
       trust ENUM(verified,collected) DEFAULT 'verified',
       status ENUM(draft,published,cancelled,completed),
       created_by UUID, created_at TIMESTAMPTZ)
-- bir etkinlik birden çok kaynakta listelenmiş olabilir; biri silinmez
event_sources(event_id UUID FK, source_event_id UUID FK, is_primary BOOL,
              PRIMARY KEY (event_id, source_event_id))
event_tickets(id UUID PK, event_id UUID FK, name TEXT, price_minor INT, currency CHAR(3),
              quantity INT, sold_count INT, sales_start TIMESTAMPTZ, sales_end TIMESTAMPTZ,
              kind ENUM(free,paid))
-- quantity: bir kullanıcı bir etkinliğe 1'den fazla bilet alabilir
-- (grup bileti satın alıp arkadaşlarına dağıtabilir). Kapasite event_tickets.quantity
-- ve sold_count üzerinden düşülür, registrations üzerinden değil.
registrations(id UUID PK, event_id UUID FK, user_id UUID FK, ticket_id UUID FK,
              quantity INT DEFAULT 1,
              status ENUM(reserved,pending_payment,paid,free_granted,used,cancelled,refunded,expired),
              amount_minor INT, reserved_until TIMESTAMPTZ, qr_token TEXT UNIQUE,
              checked_in_at TIMESTAMPTZ, created_at TIMESTAMPTZ,
              UNIQUE (event_id, user_id))
event_invitations(id UUID PK, event_id UUID FK, code TEXT UNIQUE, created_by UUID,
                  max_uses INT, uses INT, expires_at TIMESTAMPTZ, created_at TIMESTAMPTZ)

-- Sohbet
-- kind=dm ise tam olarak 2 üye vardır; çift tekilleştirilir (dm_key = "kucuk:id:buyuk:id")
chat_channels(id UUID PK, kind ENUM(dm,club,event), club_id UUID, event_id UUID,
              dm_key TEXT, created_at TIMESTAMPTZ)
CREATE UNIQUE INDEX ON chat_channels (dm_key) WHERE dm_key IS NOT NULL;
chat_members(channel_id UUID FK, user_id UUID FK, last_read_at TIMESTAMPTZ,
             PRIMARY KEY (channel_id, user_id))
chat_messages(id UUID PK, channel_id UUID FK, user_id UUID FK, body TEXT,
              kind ENUM(text,file,link,system), reply_to UUID, created_at TIMESTAMPTZ)
media_rooms(id UUID PK, livekit_room TEXT UNIQUE,
            event_id UUID FK, channel_id UUID FK,
            created_at TIMESTAMPTZ, ended_at TIMESTAMPTZ)

-- Dosyalar (§4.9)
media(id UUID PK, owner_id UUID FK,
      kind ENUM(avatar,club_cover,event_image,chat_attachment,club_post_image),
      content_type TEXT, byte_size INT, sha256 TEXT,
      data BYTEA NOT NULL, created_at TIMESTAMPTZ)
-- kulüp gönderi görseli: gönderi başına en fazla 4 adet, her biri 5 MB sınırında

-- Bildirimler
notifications(id UUID PK, user_id UUID FK, kind TEXT, title TEXT, body TEXT,
              data JSONB, read_at TIMESTAMPTZ, created_at TIMESTAMPTZ)

-- Veri kaynağı ayarları
source_configs(id UUID PK, name CITEXT UNIQUE, adapter TEXT, enabled BOOL,
               schedule_cron TEXT, rate_limit_rps NUMERIC, user_agent TEXT,
               terms_checked_at DATE, terms_url TEXT, config JSONB,
               last_run_at TIMESTAMPTZ, last_status TEXT)

-- Öneri
ranking_weights(name TEXT PK, value NUMERIC)
user_event_stats(user_id UUID, event_id UUID, score NUMERIC,
                 updated_at TIMESTAMPTZ, PRIMARY KEY (user_id, event_id))

-- Güvenlik
audit_log(id UUID PK, actor_id UUID, action TEXT, target TEXT, meta JSONB,
          created_at TIMESTAMPTZ)

-- Şikâyet / moderasyon (gönderi, yorum, kulüp)
reports(id UUID PK, reporter_id UUID FK, target_kind TEXT, target_id UUID,
        reason TEXT, status ENUM(open,reviewed,actioned) DEFAULT 'open',
        handled_by UUID, created_at TIMESTAMPTZ, handled_at TIMESTAMPTZ)
CREATE INDEX ON reports (status) WHERE status = 'open';
```

**Kritik indeksler:** `events(starts_at)`, `events(status)`, `events(origin, status)`, `registrations(event_id, status)`, `venues` GIST, `source_events` GIST + unique, `event_sources(source_event_id)`, `chat_messages(channel_id, created_at DESC)`, `club_posts(club_id, created_at DESC)`, `club_followers(user_id, created_at DESC)`, `reports(status)` kısmi, `audit_log(created_at DESC)`.

**Para:** Her yerde tam sayı (kuruş) + `CHAR(3)` para birimi. Ondalık sayı kullanılmaz. Türkiye için `TRY`.

---

## 8. API sözleşmesi

FastAPI + Pydantic, OpenAPI 3.1'i kendiliğinden üretir. TypeScript tipleri ve doğrulama şemaları tek komutla gelir:

```bash
just api-types   # openapi.json -> packages/api-client/
```

| Grup | Endpoint'ler |
|---|---|
| Kimlik | `POST /auth/register` · `/auth/login` · `/auth/refresh` · `/auth/logout` · `GET /auth/me` |
| Kulüp | `GET/POST /clubs` · `GET/PATCH /clubs/{id}` · `POST/DELETE /clubs/{id}/members[/{uid}]` · `POST /clubs/{id}/invitations` · `POST /invitations/{code}/redeem` |
| Takipçilik | `POST/DELETE /clubs/{id}/follow` · `GET /clubs/{id}/followers` · `GET /clubs/{id}/following` · `GET /users/me/following` |
| Kulüp gönderileri | `GET /clubs/{id}/posts?before=` · `POST /clubs/{id}/posts` · `PATCH /posts/{id}` · `DELETE /posts/{id}` |
| Gönderi etkileşimi | `POST/DELETE /posts/{id}/like` · `GET/POST /posts/{id}/comments` · `DELETE /comments/{id}` |
| Akış | `GET /feed?cursor=` (takip edilen kulüplerin gönderileri) |
| Etkinlik | `GET/POST /events` · `GET/PATCH /events/{id}` · `POST /events/{id}/cancel` · `/publish` |
| Etkinlik kaynakları | `GET /events/{id}/sources` (toplanmış etkinliğin hangi sitelerde listelendiği) |
| Bilet | `GET /events/{id}/tickets` · `POST /events/{id}/register` · `DELETE /registrations/{id}` · `GET /registrations/{id}/qr` · `POST /registrations/{id}/checkin` |
| Davetiye | `POST /events/{id}/invitations` · `GET /invitations/{code}` · `GET /invitations/{code}/status` · `POST /invitations/{code}/redeem` |

Kulüp ve etkinlik davetileri aynı yolu kullanır. `GET /invitations/{code}` çağrısı davetiyenin türünü döndürür — kullanıcı davetiyi açtığında üyelik mi kayıt mı olacağını önceden bilir.
| Keşif | `GET /discover/venues?bbox=&category=` · `GET /discover/events?lat=&lng=&radius=&category=&when=&price=` · `GET /discover/recommendations` |
| Öneri geri bildirimi | `POST /recommendations/feedback` |
| Sohbet | `GET /channels` · `GET /channels/{id}/messages?before=` · `POST /channels/{id}/messages` |
| Özel mesaj (DM) | `POST /channels/dm` (karşı kullanıcı + metin) · `GET /channels?kind=dm` · `POST /channels/{id}/read` |
| Oda (medya) | `GET /events/{id}/room/token` · `POST /channels/{id}/room/token` (kulüp ve DM odası için) |
| Bildirim | `GET /notifications` · `POST /notifications/{id}/read` |
| Şikâyet | `POST /reports` · `GET /admin/reports?status=open` · `POST /admin/reports/{id}/handle` |
| Dosya | `POST /media` · `GET /media/{id}` · `DELETE /media/{id}` |
| Cihaz | `POST /devices` · `DELETE /devices/{id}` |
| Yönetim | `GET /admin/sources` · `PATCH /admin/sources/{id}` · `POST /admin/sources/{id}/run` · `GET /admin/audit` |
| Sistem | `GET /health` · `GET /metrics` · `GET /openapi.json` |

**WebSocket:** `GET /ws?token=` — `{type, payload}`.
Tipler: `msg.send`, `msg.typing`, `msg.ack`, `presence.update`, `event.updated`, `ticket.sold_out`, `notification.push`.

### 8.1 Sözleşme kuralları

1. **Geriye dönük bozan değişiklik = ana sürüm artışı.** `/v1` sabit; P1 onayı olmadan bozulmaz.
2. **Boş değerler açık.** `T | None` ↔ `null`.
3. **Para:** `{ "amountMinor": 12500, "currency": "TRY" }`.
4. **Zaman:** UTC + ISO-8601.
5. **Hata:** RFC 9457 problem details. `type` makine-okunur, `title` insan-okunur.
6. **Idempotency:** `Idempotency-Key` başlığı — bilet alma ve mesaj gönderme.
7. **Kapasite:** `event_tickets.sold_count` yalnızca `paid` ve `free_granted` durumlarından artar. `reserved` ve `pending_payment` kapasiteyi rezerve eder ama saymaz; süresi dolan rezervasyon otomatik iptal edilir.

---

## 9. Öneri motoru

```
Aşama 1 (Sprint 2) — Coğrafi aday üretim, veritabanında
  Mesafe + kategori + tarih penceresi ile 200 aday

Aşama 2 (Sprint 2) — Şeffaf skor
  score = w1·mesafe_uygunluğu     (2 km'de 1.0 → 20 km'de 0.0, doğrusal)
        + w2·kategori_uyumu       (ilgi profili + takip edilen kulüplerin kategorileri)
        + w3·tazelik
        + w4·popülerlik           (katılımcı sayısı, log ölçek)
        + w5·fiyat_uyumu
        + w6·takip_sinyali        (etkinliğin kulübünü takip ediyor musun?)
  Ağırlıklar ranking_weights tablosunda, yönetim ekranından ayarlanır

  w6 önemli: takip etmek, tıklamaktan çok güçlü bir ilgi sinyalidir.
  "Şunu beğendin" demek, "bunu beğeniyorum" demekten güçlüdür.

Aşama 3 (Faz 2) — Öğrenen katman
  Görüntüleme/kaydetme/katılma → user_event_stats
  TF-IDF tabanlı içerik benzerliği
  Değerlendirme: NDCG@10, MAP@10 — mevcut skoru geçmezse KAPATILIR
```

Kullanıcı davranışı toplamaya zorunlu değildir. Profil açıkça doldurulur veya boş bırakılır; boş profilde şeffaf skor çalışır.

**Takip sinyali öneriyi erken çalıştırır.** Kullanıcının "beğenme" geçmişi birkaç haftada birikir ve zayıftır. Kulüp takibi ise tek tıkla güçlü bir sinyaldir. Bu yüzden kişiselleştirme Sprint 3'te takipçilik bittikten sonra anlamlı hale gelir — Aşama 3'e (makine öğrenmesi) Sprint 4'ten önce ihtiyaç kalmayabilir.

---

## 10. Takvim

**15 hafta + 1 demo haftası.** Sprint 3 haftadır.

Hafta 2'de imzasız APK, hafta 14'te imzalı APK, hafta 15'te demo akışı. Her sprint'in çıktısı telefonda açılabilir bir APK'dır; yarım kalan hiçbir sprint kabul edilmez.

### Sprint 0 — Temeller (Hafta 1-2)

| # | İş | Sahip |
|---|---|---|
| 0.1 | Depo, `mise.toml`, `justfile`, Podman kurulumu | P1 |
| 0.2 | **Deneme: Node + SvelteKit + Tauri → APK** | P6 |
| 0.3 | **Deneme: LiveKit + Valkey** | P5 |
| 0.4 | **Deneme: Tailwind + shadcn-svelte + IntelliSense** | P6 |
| 0.5 | FastAPI iskeleti + OpenAPI üretimi | P1 |
| 0.6 | Veritabanı şeması + Alembic | P1 |
| 0.7 | Podman: postgres+postgis, valkey, caddy, martin | P1 |
| 0.8 | 2 kaynak adaptörü iskeleti + `data-sources.md` | P3 |
| 0.9 | Hurl ile ilk 5 endpoint sözleşme testi | P1, P2 |
| 0.10 | PostGIS iki günlük ekip eğitimi | P4 |

**Çıkış ölçütü:** `just android-apk` imzasız APK üretir. `just dev` tüm servisleri ayağa kaldırır. IntelliSense doğrulanmıştır.

### Sprint 1 — Çekirdek alan (Hafta 3-5)

| # | İş | Sahip |
|---|---|---|
| 1.1 | Kimlik doğrulama: kayıt, giriş, jeton yenileme, argon2 | P1 |
| 1.2 | Profil + ilgi alanları | P1 |
| 1.3 | Kulüp oluşturma, üyelik, roller | P2 |
| 1.4 | Etkinlik oluşturma, bilet tipleri, kayıt durum makinesi | P2 |
| 1.5 | Tauri kabuğu, yönlendirme, giriş ekranı | P6 |
| 1.6 | Yerel önbellek + çevrimdışı okuma | P6 |
| 1.7 | Mekan toplama (Overpass) → PostGIS aktarımı | P3, P4 |
| 1.8 | Tasarım sistemi + hazır bileşenler | P6 |
| 1.9 | Keşif API'si: mesafe sorgusu + şeffaf skor | P4 |
| 1.10 | Profil ve kulüp ekranları | P6, P2 |

**Çıkış ölçütü:** Giriş → kulüp oluştur → etkinlik gör → bilet al.

### Sprint 2 — Veri ve harita (Hafta 6-8)

| # | İş | Sahip |
|---|---|---|
| 2.1 | 4 kaynak canlı + temizleme + tekrar eleme | P3 |
| 2.2 | Veri kalitesi panosu | P3 |
| 2.3 | Keşif ekranı: harita, pin'ler, filtre | P7 |
| 2.4 | Etkinlik detayı + bilet seçme | P7 |
| 2.5 | Konum izni + "yakınımdakiler" | P7 |
| 2.6 | Kaynak atfı ekranı | P7 |
| 2.7 | **Hafta 6 değerlendirmesi** (§6.1) | P1 + ekip |
| 2.8 | Öneri geri bildirimi toplama | P4 |
| 2.9 | Hurl sözleşme testleri %60 kapsam | P1, P2, P4, P5 |
| 2.10 | Kulüp takipçiliği (takip/takipten çık, sayaçlar) | P2 |

**Çıkış ölçütü:** Gerçek harita, gerçek etkinlikler, gerçek mekanlar. 100+ temizlenmiş kayıt.

### Sprint 3 — Topluluk ve zaman (Hafta 9-11)

| # | İş | Sahip |
|---|---|---|
| 3.1 | WebSocket sohbet (kanal, mesaj, yazıyor) | P5 |
| 3.2 | Çevrimiçi durum + mesaj dağıtımı | P5 |
| 3.3 | LiveKit odaları + ses/görüntü ekranı | P5 |
| 3.4 | Online etkinlik akışı | P5, P7 |
| 3.5 | Davetiye linkleri + QR + okutma | P2 |
| 3.6 | Kapıda doğrulama ekranı | P2, P7 |
| 3.7 | Yerel bildirim + derin link | P5, P6 |
| 3.8 | Bilet cüzdanı + takvime ekleme | P7 |
| 3.9 | Öneri motoru 3. aşama (geçerse) | P4 |
| 3.10 | Kulüp gönderileri: metin + fotoğraf, görünürlük ayarı | P2 |
| 3.11 | Takip akışı ekranı | P2, P7 |
| 3.12 | Beğeni + yorum | P2 |
| 3.13 | Özel mesajlaşma (DM listesi + DM ekranı) | P5 |
| 3.14 | Kulüp gönderileri için moderasyon (yönetici siler, şikâyet) | P2 |

**Çıkış ölçütü:** İki kişi kulüp sohbetinde yazışır, üçüncü katılır, ses duyulur. İki kişi birbirine özel mesaj atar ve sesli arar. Kulüp yöneticisi gönderi paylaşır, takipçi görüntüyü beğenir ve yorum yapar. Davetiye QR okutularak kabul edilir.

### Sprint 4 — Sıkılaştırma (Hafta 12-14)

| # | İş | Sahip |
|---|---|---|
| 4.1 | Ekran paylaşımı (web) | P5, P7 |
| 4.2 | Telefonda belge/bağlantı paylaşımı | P5 |
| 4.3 | Çevrimdışı eşitleme + çakışma çözümü | P6 |
| 4.4 | E2E test paketi (8 akış) | P7 |
| 4.5 | Performans ölçümü (§11) | P6, P7 |
| 4.6 | İmzalama + sürüm hattı | P1, P7 |
| 4.7 | Güvenlik: yetki denetimi, hız sınırı, gizli anahtar taraması | P1 |
| 4.8 | ADR'ler + `data-sources.md` + `runbook.md` | tüm |
| 4.9 | Yük testi + sunucu maliyeti raporu | P1 |
| 4.10 | Veri hattı profil çıkarımı | P3 |

**Çıkış ölçütü:** İmzalı APK, 8 E2E yeşil, performans hedefleri tutturulmuş, yük testi raporu.

### Sprint 5 — Demo (Hafta 15)

Demo akışı baştan sona prova edilir, ekran kaydı alınır, `README` ve dokümantasyon güncellenir.

---

## 11. Performans hedefleri

| Ölçüt | Hedef | Nasıl ölçülür |
|---|---|---|
| Açılış süresi (p50) | < 1.2 sn | Sürüm derlemesi, orta sınıf cihaz |
| Boşta bellek | < 120 MB | Android Studio profiler |
| APK boyutu | < 25 MB | Sürüm APK'sı |
| İlk yükleme paketi | < 250 KB (gzip) | Derleme raporu |
| Boşta WebSocket belleği | < 5 MB | 30 dakika bekleme testi |
| Sunucu yanıt süresi (okuma, p95) | < 200 ms | k6 |
| Sunucu yanıt süresi (yazma, p95) | < 350 ms | k6 |
| Keşif sorgusu | < 300 ms | `EXPLAIN ANALYZE`, 100k kayıt |
| Harita akıcılığı | 60 fps kaydırma | Orta segment cihaz |
| Harita önbelleği (telefon) | 300 MB üst sınır | LRU ile temizlenir |
| Veri toplama işçi belleği | < 200 MB | RSS ölçümü |

**Uygulama kuralları:**

- Harita ve WebSocket ekranları kapandığında arka planda durur
- Görseller tembel yüklenir, WebP/AVIF formatında
- 1000+ satırda `@tanstack/svelte-virtual`
- WebSocket 30 saniyede bir ping; kopunca 1/2/4/8 saniye artan aralıkla yeniden bağlanır
- Sohbet mesajları 200 mesajlık pencere ile tutulur, geri kalanı sayfalanır
- Ses ve görüntü izleri katmandan çıkarken kapatılır
- `just perf-apk` her sürümde çalışır; hedefi aşan PR CI'da durdurulur

**Sunucu:** Uvicorn + uvloop + orjson + hiredis + psycopg bağlantı havuzu. İlk fazda PgBouncer yok.

---

## 12. Test stratejisi

| Seviye | Araç | Hedef |
|---|---|---|
| Sunucu birim testleri | pytest + pytest-asyncio | `services/`, `domain/` %90 |
| **API sözleşme testleri** | **Hurl** | Tüm endpoint'ler + hata senaryoları |
| Veri hattı birim testleri | pytest + HTML örnekleri | Her kaynak kendi örneğiyle |
| Arayüz birim testleri | Vitest + happy-dom | Store'lar, doğrulama, skor |
| Sözleşme kayması | @hey-api/openapi-ts + CI | Üretim sonrası fark boş olmalı |
| Entegrasyon | Podman compose | Göçler + veri katmanı |
| E2E (web) | @playwright/test | 8 kritik akış |
| E2E (telefon) | adb + UI Automator | 3 kritik akış |
| Yük | k6 | 500 eşzamanlı okuma |
| Özellik tabanlı | schemathesis (faz 2) | OpenAPI'den otomatik fuzz |
| Güvenlik | pip-audit, bandit, Trivy, gizli anahtar taraması | CI |
| Kod kalitesi | ruff + svelte-check + eslint | CI |

Playwright tarayıcıda çalışır, Android'un WebView katmanında değil. İzin akışları ve QR gibi telefon tarafı sınırlar cihaz testiyle doğrulanır; P7 üç akışla sınırlar.

---

## 13. Sunucu kurulumu ve dağıtım

### 13.1 Otomatik doğrulama (her PR)

```
lint      → ruff check + ruff format --check + svelte-check + eslint
test      → pytest + vitest
contract  → openapi.json yeniden üret → git diff boş olmalı
hurl      → API çalışırken .http dosyaları koştur
migrate   → boş veritabanına göçleri uygula → şema karşılaştır
audit     → pip-audit, bandit, Trivy, gizli anahtar taraması
deny      → deny.txt'teki yasaklı bağımlılıklar eklenmiş mi
build-web → derleme + paket bütçe kontrolü
build-apk → yalnızca main/release/*: tauri android build --apk
```

**`deny` adımı:** PR'ın eklediği bağımlılıklar `deny.txt` listesiyle karşılaştırılır. Listeye yeni bir madde eklemek ADR yazmayı gerektirir; CI, ADR'si olmayan maddeyi reddeder.

`build-apk` yalnızca `main` dalında çalışır; PR'da Gradle/NDK indirme süresi CI'ı yavaşlatır.

**CI platformu:** Sprint 0'da karar verilir. Kurumun GitHub/GitLab hesabı varsa o kullanılır; yoksa Forgejo Actions kendi sunucumuzda.

### 13.2 Dağıtım

- **Sunucu:** Tek VPS (Hetzner sınıfı), 4 çekirdek / 8 GB / 80 GB. Podman Compose.
- **HTTPS:** Caddy otomatik Let's Encrypt.
- **Adresler:** `api.projectx.app` + `app.projectx.app` (yer tutucu). APK aynı API'ye bağlanır.
- **Medya portları:** LiveKit TCP 7880 + UDP 7881/7882 + **UDP 50000-50100** açık. Ayrıntı `infra/docs/ports.md`
- **Erişim:** Headscale — deneme ve demo sunucularına port açmadan erişim.
- **Gizli anahtarlar:** `.env` depoya girmez, SOPS veya Infisical ile şifrelenir.
- **APK imzalama:** Sürüm anahtarı CI'da, parolası gizli.
- **Güncelleme:** `plugin-updater` — kendi imzalı bildirimimizden.
- **Harita paketleri:** Martin kendi sunucumuzda, veritabanından üretir.

---

## 14. Riskler

| # | Risk | Olasılık | Etki | Önlem | Sahip |
|---|---|---|---|---|---|
| R1 | Tauri Android derleme zinciri sorun çıkarır | Orta | Yüksek | Sprint 0 denemesi; yedek plan web sürümü | P6 |
| R2 | Rust yüzeyi beklenenden büyür | Yüksek | Yüksek | 200 satır sınırı, CODEOWNERS, eklenti yeterliyse komut yazılmaz | P1, P6 |
| R3 | Telefonda ekran paylaşımı mümkün değil | Kesin | Orta | §1.3'te kapsam dışı | P5 |
| R4 | Kaynak kullanım koşulları ihlal edilir | Orta | Yüksek | `data-sources.md` kapı kontrolü, `robots.txt`, yumuşak bekleme, en az 2 kaynak | P3 |
| R5 | Ekran işi yetişmez | Yüksek | Yüksek | §6.1 değerlendirmesi, hafta 1'de ekran listesi | P1 |
| R6 | Sunucu performansı yetersiz kalır | Düşük | Orta | Sprint 4 yük testi; ağır sorgular veritabanında | P1 |
| R7 | Yedi farklı kod stili | Yüksek | Orta | `just fmt`, PR kapısı, ADR, haftalık senkron | P1 |
| R8 | API sözleşmesi kayar | Orta | Yüksek | Pydantic'ten otomatik OpenAPI + CI fark kontrolü | P1 |
| R9 | LiveKit kurulumunda UDP port engeli | Orta | Orta | `infra/docs/ports.md`, Sprint 0 denemesi | P5 |
| R10 | Ödeme beklentisi | Orta | Orta | §1.3'te yazılı, elle onay akışı çalışır | P1 |
| R11 | Veri toplama tek kişide kalır | Yüksek | Yüksek | Sprint 0'da P1 ortak; her adaptörün testi; P4 destek verir | P1, P3 |
| R12 | Demo günü medya çöker | Düşük | Yüksek | Video canlı gösterilmez, kayıt önceden hazırlanır | P5 |
| R13 | Harita bellek hedefini aşar | Düşük | Orta | Sprint 0'da erken ölçüm; gerekirse düşük çözünürlük | P6 |
| R14 | JS runtime uyumsuzluğu (Vite + SvelteKit) | Düşük | Orta | ADR-0011 ile Node'a geçildi; Sprint 0'da tek deneme | P6 |
| R15 | Format araçları birbirine giriyor | Orta | Düşük | §4.12'deki sorumluluk paylaşımı | P6 |
| R16 | Kayıt engellenir (okul e-postası zorunlu olur) | Düşük | Düşük | Okul e-postası hiçbir koşul değil; istenirse isteğe bağlı doğrulama | P1 |
| R17 | Harici depoya taşımak gerekirse seçenek azalır | Düşük | Düşük | §4.9'da veritabanı içinde; RustFS/Garage/SeaweedFS/Ceph hazır | P1 |
| R18 | Bildirim beklentisi | Orta | Orta | §1.3'te yazılı; uygulama açıkken anında bildirim çalışıyor | P5 |

---

## 15. Geliştirme komutları

```bash
just setup            # mise trust + kurulum + örnek veri
just dev              # podman compose up + sıcak yenileme (masaüstü)
just dev-mobile       # npm run tauri android dev
just android-apk      # imzasız deneme APK'ı
just android-release  # imzalı sürüm APK'sı
just api-types        # openapi.json -> tipler + doğrulama şemaları
just migrate          # alembic upgrade head
just seed             # örnek veri (Türkiye, 3 şehir)
just hurl             # API sözleşme testleri
just perf-apk         # paket + APK boyutu raporu
just test             # tüm testler
just ci               # CI ile aynı lokal komutlar
just fmt              # ruff format + prettier
just lint             # ruff check + svelte-check + eslint
just services         # oxker ile konteyner izleme
just vpn              # headscale ile sunucuya bağlan
```

```bash
git switch -c feat/ticket-qr
# ... çalış ...
just fmt && just lint && just test
git push -u origin feat/ticket-qr
gh pr create --fill
```

---

## 16. "Bitti" tanımı

- [ ] Derleniyor; `ruff`, `svelte-check`, `eslint` temiz (uyarı yok)
- [ ] Birim testi var
- [ ] OpenAPI yeniden üretildi, CI fark kontrolü yeşil
- [ ] Veritabanı göçü değiştiyse P1 onayı alındı
- [ ] Hata durumları işlendi (boş durum, ağ hatası, 401/403/409/410)
- [ ] Yükleme göstergesi + iskelet ekran var
- [ ] Boşta bellek ölçüldü, hedefi aşmadı
- [ ] Erişilebilirlik: ekran okuyucu etiketi, 44px dokunma hedefi, koyu mod
- [ ] Arayüz metni `locales/tr.json` + `locales/en.json` içinde (TR birincil), sabit yazılmış metin yok
- [ ] PR açık, bir kişi onayladı
- [ ] Karar gerektiriyorsa `docs/adr/` yazıldı
- [ ] Yeni veri kaynağı eklendiyse `docs/data-sources.md` güncellendi
- [ ] Yeni eklenti eklendiyse §3.1 güncellendi
- [ ] Format kuralı uygulandı (§4.12)
- [ ] Yeni bağımlılık açık kaynak ve lisansla uyumlu
- [ ] Yeni endpoint eklendiyse Hurl testi ve OpenAPI yeniden üretimi yapıldı
- [ ] `just perf-apk` hedefi aşmadı

---

## 17. Ek kaynaklar

- Tauri v2: https://v2.tauri.app/
- Tauri + SvelteKit: https://v2.tauri.app/start/frontend/sveltekit/
- Tauri eklenti kataloğu: https://v2.tauri.app/plugin/
- Node: https://nodejs.org/en/docs
- SvelteKit static adapter: https://svelte.dev/docs/kit/adapter-static
- Tailwind CSS v4: https://tailwindcss.com/docs
- shadcn-svelte: https://www.shadcn-svelte.com/docs
- bits-ui: https://bits-ui.com/docs
- formsnap: https://formsnap.dev/docs
- TanStack Svelte Query: https://tanstack.com/query/latest/docs/framework/svelte/overview
- Hey API: https://heyapi.dev/
- FastAPI: https://fastapi.tiangolo.com/
- PostGIS: https://postgis.net/documentation/
- OpenStreetMap ODbL: https://opendatacommons.org/licenses/odbl/
- Nominatim kullanım politikası: https://operations.osmfoundation.org/policies/nominatim/
- Overpass API: https://wiki.openstreetmap.org/wiki/Overpass_API
- LiveKit kendi sunucunuzda: https://docs.livekit.io/transport/self-hosting
- Hurl: https://hurl.dev/
- Martin: https://github.com/maplibre/martin
- uv: https://docs.astral.sh/uv/
- MapLibre GL: https://maplibre.org/maplibre-gl-js/docs/
- DOMPurify: https://github.com/cure53/DOMPurify
- WAI-ARIA tasarım örüntüleri: https://www.w3.org/WAI/ARIA/apg/

---

## 18. Onay

Bu dokümanı okuyan ve kapsam kararlarını (§4) kabul eden 7 kişi:

| Rol | İsim | Tarih | İmza |
|---|---|---|---|
| P1 Tech Lead | Abdullah Yılmaz | | |
| P2 Backend Engineer | Eren Yığmatepe | | |
| P3 Data Engineer | İsmail Can Kocaman | | |
| P4 Backend Engineer | Umut Can Kuş | | |
| P5 Backend Engineer | Cevat | | |
| P6 Mobile Engineer | Abdullah Hilal | | |
| P7 Mobile UI Engineer & QA | Adar Bilmez | | |