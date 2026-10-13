# P5 — Cevat — Backend Engineer, Realtime & Media

**Alan (sabit, §6 Ekip):** Sohbet, özel mesaj, çevrimiçi durumu, bildirim, ses/görüntü. Medya katmanı tek elinde (§6 Ekip: başkası dokunmaz). 7 hafta bu kavramdasın.
**Buddy:** P2 (§6.2 Çalışma kuralları eşleşmesi). **Lider haftan:** H5.

## Envanterin

Senin işin uygulamanın canlı dokusu: yazışma anında iletilir, kim çevrimiçi görünür, oda açılır, bildirim düşer. Kurallar serttir çünkü gerçek zamanlı sistemde hata kullanıcıya anında yansır:

- **Tablolar (§7 Veri modeli):** `chat_channels` (türler: dm/club/event; `dm_key` ile çift tekilleştirme), `chat_members` (`last_read_at` okundu bilgisi), `chat_messages` (türler: text/file/link/system, `reply_to` yanıtlar), `media_rooms` (`livekit_room` benzersiz), `notifications`, `devices` (push token yok — sunucu itme yapmaz §4.8 Bildirim), `media` (ek olarak `chat_attachment`, 5 MB).
- **Uçlar (§8 API sözleşmesi):** `GET /channels`, `GET /channels/{id}/messages?before=`, `POST …/messages`; `POST /channels/dm` (karşı kullanıcı + ilk metin), `GET /channels?kind=dm`, `POST …/read` (okundu); `GET /events/{id}/room/token` (etkinlik odası) · `POST /channels/{id}/room/token` (kanal odası §8); `GET /notifications`, `POST …/read`; WS `GET /ws?token=` (7 mesaj tipi).
- **Dizinlerin (§5 Depo yapısı):** `apps/api/app/{realtime,media,notifications}/` (sunucu tarafı), `apps/mobile/src/lib/realtime/` (WS istemcisi + çevrimiçi durumu deposu).
- **Kurallar (§11 Performans hedefleri):** 30 sn'de bir ping, kopunca 1/2/4/8 sn aralıklarla yeniden bağlanma, 200 mesajlık pencere + sayfalama, boşta WS belleği < 5 MB, ortam izleri (ses/görüntü) katmandan çıkarken kapatılır, yazma işlerinde `Idempotency-Key` (§8.1 Sözleşme kuralları md.6).
- **Bildirim (§4.8 Bildirim):** uygulama açık + WS bağlıyken anında ekran-içi + rozet; arka plandayken sistem bildirimi; kapalıyken yok; internetsizken kuyruğa alınır, bağlantı gelince gönderilir.
- **Ekranların (§1.6 Ekran listesi):** `/clubs/[id]/chat`, `/(tabs)/messages`, `/channels/[id]`, `/events/[id]/room` + `/channels/[id]/room`, `/notifications`. Bileşenlerin: `ChatBubble`, `PresenceDot`, `VoiceBar`, `VideoTile` (§3.1 Mobil yığın).

## H1 — Deneme haftan

- **H1.11 LiveKit + Valkey + WS şeması.** **Adımlar:** 1. 7 `/ws` mesaj tipini PR'a yaz (§8 API sözleşmesinden, H1.4 beklenmez). 2. `livekit.yaml` + port planı (`infra/docs/ports.md`, R9 UDP engeli riski). Canlı deneme H2.18'de yapılır (H1.4 önceki haftadan). **Kabul:** tip dokümanı + port planı PR'da. **Çıktı:** H2.18 jeton işi ile H4.1–H4.4 sohbet işleri buraya dayanır.

## H2 — Hazırlık haftan

Bu hafta H4'ün büyük sohbet haftasına zemin hazırlarsın: jetonlar, cihaz kaydı, istemci iskeleti.

- **H2.18 Token uçları + deneme provası.** `livekit-api` ile oda jetonları üretilir (etkinlik + kanal §8 API sözleşmesi) + H1.11 deneme odası provası (H1.4/H1.11 önceki haftalardan). **Kabul:** jetonla odaya giriş + ses duyulur. **Çıktı:** H4.3 odalar buraya dayanır.
- **H2.19 Devices + bildirim API.** `POST /devices` (cihaz kaydı: çevrimiçi durumu + sürüm, push token yok), `GET /notifications` + `POST …/read` ile okundu işareti + kuyruk kuralı (§4.8 Bildirim). **Kabul:** uygulama açılışında `GET /notifications` çeker. **Çıktı:** H4.5 bildirim işi buraya dayanır.
- **H2.20 Realtime istemci iskeleti.** `apps/mobile/src/lib/realtime/` altında WS istemcisi + çevrimiçi durumu deposu + `@tanstack/svelte-query` sorgu anahtarları (§5.1 Nerede ne: istekler `lib/api/`da durur; §8'den yazılır). H2.1 auth şemasına H4.6'da kilitlenir (H2.1 önceki haftadan). **Kabul:** iskelet mock WS'ye bağlanır/kopanır. **Çıktı:** H4.6 ekranları buraya dayanır.
- Ayrıca: P1'in H2.1 auth işini izle (korumalı WS tasarımı için); buddy P2'nin kulüp bağlamı sorularını yanıtlarsın.

## H3 — Sözleşme haftan

- **H3.14 WS testleri + tip dokümanı.** Hurl iskeleti + 7 tipin anlamı yazılı doküman. **Kabul:** iskelet dosyaları hazır, tip dokümanı PR'da.
- **H3.16 Bildirim metinleri + rozet sayacı.** `locales/tr.json` (+`en.json`) girdileri (başlık/gövde şablonları §4.8 Bildirim) + bildirim rozet sayacı kuralı. **Kabul:** metinler `tr.json`'da, sabit yazılmış metin yok (§16 Bitti tanımı). **Çıktı:** H4.5/H4.6 buraya dayanır.
- **H3.8-pay.** Kendi sohbet/DM/oda/bildirim uçlarının Hurl testleri; başkasını beklemezsin. **Kabul:** yeşil.
- **H3.9-katılım.** Medya ayağının durumu toplantıda sende + §6.1 Değerlendirmedeki P5 satırın (işlerin yarısından azı biterse kesinti gündeme gelir). **Kabul:** tablon hazır.

## H4 — Büyük haftan

Projenin en yoğun backend haftası senin: sohbet, presence, odalar, DM, bildirim, beş ekran — hepsi bu hafta canlanır.

- **H4.1 WS sohbet.** Kanal/mesaj/yazıyor göstergesi + `reply_to` yanıtlar + `kind` türleri. **Kabul:** 200 mesajlık pencere + sayfalama testi yeşil.
- **H4.2 Presence + dağıtım.** Valkey pub/sub ile kim çevrimiçi bilgisi dağıtılır. **Kabul:** 30 dk beklemede bellek < 5 MB (§11 Performans hedefleri).
- **H4.3 LiveKit odalar.** `media_rooms` kaydı + `ended_at` kapanış damgası. **Kabul:** oda açma/kapama + iz temizliği testli.
- **H4.4 DM.** `dm_key` ile çift tekilleştirilir (§7 Veri modeli: aynı ikiliye ikinci kanal açılmaz). **Kabul:** ikinci kanal açılmaz.
- **H4.5 Bildirim + deep-link (P6 ile).** Dört §4.8 Bildirim durumu cuma provasında gösterilir (açık+WS, arka plan, kapalı, internetsiz). **Kabul:** bildirimden ilgili ekrana düşüş çalışır.
- **H4.6 Beş ekran + dört bileşen (livekit-client 2.22 §3.1 Mobil yığın).** **Kabul:** cuma provasında H4 çıkışı kanıtlanır (iki kişi yazışır, üçüncü katılır, ses duyulur).

## H5 — Liderlik haftan

Teknik işin az, orkestrasyonun çok: 15 işlik haftayı sen yönetirsin.

- **H5.7 Online akış (P7 ile).** `is_online`/`online_url` alanları olan etkinlikte oda açılır (§7 Veri modeli). **Kabul:** canlı odada ses+görüntü+sohbet bir arada (§1.2 Uygulama akışı).
- **H5.11 Sohbet dosya eki.** `kind=file`: `POST /media` (5 MB, dosya tipi uzantıya değil içeriğe bakılarak okunur §4.9 Dosya saklama) + `GET /media/{id}` (önbellek başlıklı sunum) + `DELETE /media/{id}`; telefonda yüklemeden önce WebP küçültme (`@jsquash/resize` §3.1 Mobil yığın). **Kabul:** dosya gönderilir/açılır/silinir. (D5 ekran-paylaşımı kesintisi dışı — bu, sohbetin parçası.)
- **Liderlik:** 15 işlik haftayı bekleme zincirleri tablosuyla açarsın (H5.1→H5.2 davetiye zinciri, H3.7→H5.4 takip zinciri). Cuma üç prova yapılır + P6'ya devir notu yazarsın.

## H6 — Kanıt haftan

- **H6.12 Presence ölçeği.** Valkey pub/sub yük altında + 30 dk < 5 MB raporu. **Kabul:** ölçüm raporu docs'ta durur.
- **H6.7-pay.** LiveKit kurulum notlarını `runbook.md`'ye yazarsın (portlar dahil).

## H7 — Demo

Medya ayağı provada sende (H7.1); R12 gereği kayıt önceden hazırdır, canlı demoya güvenilmez.

## Risklerin

R9 (UDP port engeli): portlar H1.11'de çözülür, H4'e taşınmaz. Ping + pencere + iz kuralları H4.1'de yazılır, sonraya kalmaz.
