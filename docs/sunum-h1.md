# H1 Sunumu — Temeller (1. Hafta)

**Hafta lideri:** Abdullah Yılmaz · **Durum:** hafta hedefleri tuttu ✅
**Ekip:** 7 kişi · **Plan:** 7 hafta, 17 görev bu hafta

## Genel anlatım

EtkinlikCepte, Türkiye'deki dağınık etkinlik duyurularını tek haritada toplayan bir telefon uygulaması olacak: konser, tiyatro, belediye etkinliği ne varsa haritada görünecek, kulüpler duyuru yapacak, biletler QR kodla cebe girecek. Yedi kişilik ekibiz ve önümüzde yedi hafta var; sonunda çalışan bir uygulamayla hocanın karşısına çıkacağız.

Bu hafta, tabiri caizse atölyeyi kurduk. Kimse daha "ürün" yazmadı; herkes kendi tezgâhını hazırladı: sunucu iskeleti ayağa kalktı, veritabanı yapısı kilitlendi, telefon uygulaması ilk deneme sürümünü üretti, internetten etkinlik toplayacak robotların iskeleti yazıldı, harita ve sohbet tarafının denemeleri yapıldı. Haftanın en önemli çıktısı teknik değil, idari: bundan sonra kimse kimseyi beklemeden çalışacak. Telefonla sunucunun nasıl konuşacağının kurallarını dondurduk — yani "istekler böyle olacak" diye el sıkıştık — ve herkes işini bu kurallara bakarak, örnek verilerle yazmaya başladı. Gerçek bağlantılar haftalar ilerledikçe, prova günlerinde takılacak.

Rakiple değil takvimle yarışıyoruz: 23 ekranın listesi kilitlendi, neyin yapılıp neyin yapılmayacağı (ödeme yok, video yok, kapalıyken bildirim yok) herkesçe imzalandı. Önümüzdeki hafta ilk gerçek akış çalışacak: kayıt ol, kulüp aç, etkinlik gör, bilet al. Bu sunumdaki tablolar da o hikâyenin muhasebesi — kim neyi bitirdi, hangi iş aksadığı için değil, tasarım gereği haftaya kilitlenecek.

## Hafta hedefi ve sonuç

| Hedef | Sonuç |
|---|---|
| Deneme uygulaması telefonda açılır (Tauri + SvelteKit ile üretildi) | ✅ Üretildi, kuruldu, açıldı |
| Tüm servisler tek komutla ayağa kalkar (Podman: PostgreSQL+PostGIS veritabanı, Valkey önbelleği, Caddy, Martin harita sunucusu) | ✅ Hepsi çalışıyor |
| Telefon-sunucu konuşma kuralları donduruldu (FastAPI iskeleti + Pydantic'ten otomatik kural belgesi) | ✅ Bozan değişiklik yok |
| 23 ekranın listesi ve sorumluları kilitli | ✅ İki ekran sorumlusu imzaladı |

## Kim ne yaptı

| Kişi | Görevler | Çıktı / kanıt |
|---|---|---|
| Abdullah Yılmaz (Tech Lead) | Proje deposu + `mise` (araç sürümleri: Node 24, Python 3.13) + `just` (ortak komutlar) + Podman kurulumu · FastAPI sunucu iskeleti + Pydantic'ten otomatik kural belgesi (OpenAPI) · veritabanı yapısı (PostgreSQL+PostGIS) + Alembic göçleri · servis kurulumu (postgres, Valkey, Caddy, Martin) · CI denetim hattı iskeleti | Temiz bilgisayarda kurulum çalışır · kural belgesi açılır · boş veritabanına kurulum yeşil · hatalı değişiklik birleştirilemez |
| Eren Yığmatepe (Backend, Ticketing & Social) | Hurl ile ilk 5 sözleşme testi (yazdı; testler sunucuya istek atıp cevabı denetler) · bilet durum makinesi + segno ile QR kararı · FastAPI istek taslakları (router'lar) | 5 test dosyası + durum makinesi kararı + taslak hazır |
| İsmail Can Kocaman (Data Engineer, Miner) | İki Scrapy kaynak robotu iskeleti (sitelerden etkinlik toplar) + kaynak izin listesi (her sitenin kullanım koşulu kontrolü) · kaynak ayar tablosu + yönetim taslağı (Dramatiq/APScheduler görev iskeletiyle) | Robotlar veritabanısız koşar · izinler kayıtlı · veritabanı değişikliği + taslak hazır |
| Umut Can Kuş (Backend, Discovery & Ranking) | PostGIS eğitimi, yani harita-veritabanı sorguları (2 gün) · Nominatim kurulum planı (adresleri koordinata çeviren servis, kendi sunucumuzda çalışacak) | Eğitim tamam · kurulum planı hazır |
| Cevat (Backend, Realtime & Media) | 7 WebSocket mesaj tipi dokümanı (anlık sohbetin mesajlaşma kuralları) + LiveKit port planı (sesli-görüntülü odalar için ağ kapıları: TCP 7880, UDP 7881/7882 ve 50000-50100) | Tipler hazır · port listesi hazır |
| Abdullah Hilal (Mobile, Core & Design System) | Tauri + SvelteKit ile deneme APK'sı (telefon kabuğu) · Tailwind tema (`tokens.css`) + kod tamamlama · ekran listesi kilidi (Adar ile) | Deneme uygulaması · tema değişimi yansır · 23 ekran dondu |
| Adar Bilmez (Mobile UI & QA) | Ekran listesi kilidi (Hilal ile) · Playwright test iskeleti (tarayıcıda koşan 8 kritik akış) + telefonda denenecek 3 akışın listesi | Liste dondu · test iskeleti koşar |

## Bilerek 2. haftaya sarkan yürütme adımları (gecikme değil, tasarım)

Yazımı bu hafta bitti; çalıştırması 2. haftanın kendi işlerinde. Kimse kimseyi beklemedi:

| İş | Bu hafta biten | 2. haftada kilitlenen |
|---|---|---|
| İlk 5 Hurl testi | test dosyaları yazıldı | toplu test haftasında koşar |
| Bilet makinesi kararı | karar + pytest test iskeleti | etkinlik kaydında koşar |
| İstek taslakları | taslak hazır (FastAPI router) | kulüp/etkinlik işlerinin başında birleşir |
| Robot iskeletleri | Scrapy toplama + ayıklama + örnek test | 2. haftada veritabanına bağlanır |
| Kaynak ayar değişikliği | değişiklik (Alembic) dosyası | 2. haftada ilk kurulumda koşar |
| Harita prototipi | PostGIS eğitimi | 2. haftada mesafe sorgusu yazılır |
| Sesli-görüntülü deneme | tip dokümanı + port planı | 2. haftada LiveKit odasında canlı prova |
| Adres-çeviri veri yükleme | Nominatim profili + plan | 2. haftada Türkiye verisi yüklenir |

## Görev dağılımı (1. hafta)

Lider dahil herkes yüklü: altyapı 5 iş, kulüp-bilet 3 iş, veri 2 iş, keşif 2 iş, medya 1 iş (+ deneme), çekirdek 2,5 iş, ekran-kalite 1,5 iş. İkili yardımlaşmalar çalıştı (altyapı-veri birlikte, kulüp-medya kulüp bağlamında).

## Risk notları

- **Uygulama derleme zinciri (Tauri/Android):** deneme tuttu, yedek web planı rafta. **LiveKit UDP portları:** liste hazır, engel 2. hafta provasında doğrulanacak.
- Geliştirme araçları tüm makinelere kuruldu (`mise` ile Node 24 + Python 3.13 kilitli). İki Python ortamı (sunucu 59, veri hattı 76 paket) import testli.
- Kapsam dışı bırakılan yok; ertelenen büyük işler (öğrenen öneri motoru, gönderi fotoğrafı, yorumlar, web ekran paylaşımı) 3. hafta değerlendirmesine kadar kapalı.

## 2. hafta önizleme

Kimlik doğrulama (argon2 şifrelemeli) (Abdullah), kulüp/etkinlik/bilet istekleri (Eren), 3 robot iskeleti (Scrapy, RSS, JSON-LD) (İsmail), mesafe + şeffaf öneri skoru istekleri (Umut), sesli-görüntülü jetonları (LiveKit) (Cevat), kabuk + giriş ekranları + tasarım sistemi (Hilal), tasarım kalite turu (Adar). Çıkış: giriş yap → kulüp aç → etkinlik gör → bilet al.
