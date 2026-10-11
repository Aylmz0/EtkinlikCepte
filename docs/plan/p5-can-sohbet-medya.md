# P5 — Can — Sohbet ve medya

**Alan (sabit, §6):** Sohbet, özel mesaj, çevrimiçi durumu, bildirim, ses/görüntü. Medya katmanı tek elinde (§6). 7 hafta bu kavramdasın.
**Buddy:** P2 (§6.2). **Lider haftan:** H5.

## Envanterin

- **Tablolar (§7):** `chat_channels` (dm/club/event; `dm_key` tekilleştirme), `chat_members` (`last_read_at`), `chat_messages` (text/file/link/system, `reply_to`), `media_rooms` (`livekit_room` UNIQUE), `notifications`, `devices` (push token yok §4.8), `media` (ek: `chat_attachment` 5 MB).
- **Uçlar (§8):** `GET /channels`, `GET /channels/{id}/messages?before=`, `POST …/messages`; `POST /channels/dm`, `GET /channels?kind=dm`, `POST …/read`; `GET /events/{id}/room/token` (etkinlik odası) · `POST /channels/{id}/room/token` (kanal odası §8); `GET /notifications`, `POST …/read`; WS `GET /ws?token=` (7 tip).
- **Dizinlerin (§5):** `apps/api/app/{realtime,media,notifications}/`, `apps/mobile/src/lib/realtime/` (WS istemcisi + presence store).
- **Kurallar (§11):** 30 sn ping, 1/2/4/8 sn aralıkla yeniden bağlanma, 200 mesajlık pencere + sayfalama, boşta WS < 5 MB, ortam izleri katmandan çıkarken kapatılır, yazmalarda `Idempotency-Key` (§8.1 md.6).
- **Bildirim (§4.8):** uygulama açık + WS bağlı: anında ekran-içi + rozet; arka planda: sistem bildirimi; kapalı: yok; internetsiz: kuyruğa alınır.
- **Ekranların (§1.6):** `/clubs/[id]/chat`, `/(tabs)/messages`, `/channels/[id]`, `/events/[id]/room` + `/channels/[id]/room`, `/notifications`. Bileşenlerin: `ChatBubble`, `PresenceDot`, `VoiceBar`, `VideoTile`.

## H1 — Deneme haftan

- **H1.11 LiveKit + Valkey + WS şeması.** Adımlar: 1. 7 `/ws` tipini PR'a yaz (§8'den, H1.4 beklenmez). 2. `livekit.yaml` + port planı (`infra/docs/ports.md`, R9). Canlı deneme H2.18'de (H1.4 önceki haftadan). Kabul: tip dokümanı + port planı PR'da. Çıktı: H2.18, H4.1–H4.4.

## H2 — Hazırlık haftan

- **H2.18 Token uçları + deneme provası.** `livekit-api` ile oda jetonları (etkinlik + kanal §8) + H1.11 deneme odası (H1.4/H1.11 önceki haftalardan). Kabul: jetonla giriş + ses duyulur. Çıktı: H4.3.
- **H2.19 Devices + bildirim API.** `POST /devices`, `GET /notifications` + `POST …/read` ile okundu işareti + kuyruk kuralı (§4.8). Kabul: uygulama açılışında `GET /notifications` çeker. Çıktı: H4.5.
- **H2.20 Realtime istemci iskeleti.** `apps/mobile/src/lib/realtime/` (WS istemcisi + presence store) + `@tanstack/svelte-query` anahtarları (§5.1: istekler `lib/api/`da; §8'den yazılır). H2.1 şemasına H4.6'da kilitlenir (H2.1 önceki haftadan). Kabul: iskelet mock WS'ye bağlanır/kopanır. Çıktı: H4.6.
- Ayrıca: P1'in H2.1'ini izle (korumalı WS tasarımı için); buddy P2'nin kulüp bağlamı sorularını yanıtlarsın.

## H3 — Sözleşme haftan

- **H3.14 WS testleri + tip dokümanı.** Hurl iskeleti + 7 tipin anlamı yazılı. Kabul: iskelet dosyaları hazır, tip dokümanı PR'da.
- **H3.16 Bildirim metinleri + rozet sayacı.** `locales/tr.json` girdileri (başlık/gövde şablonları §4.8) + bildirim rozet sayacı kuralı. Kabul: metinler `tr.json`'da, sabit metin yok (§16). Çıktı: H4.5/H4.6.
- **H3.8-pay.** Sohbet/DM/oda/bildirim Hurl payın.
- **H3.9-katılım.** Medya ayağının durumu + §6.1 P5 satırı (işlerin yarından azı biterse kesinti). Kabul: tablon hazır.

## H4 — Büyük haftan

- **H4.1 WS sohbet.** Kanal/mesaj/yazıyor + `reply_to` + `kind`. Kabul: 200 mesajlık pencere + sayfalama testi.
- **H4.2 Presence + dağıtım.** Valkey pub/sub. Kabul: 30 dk beklemede < 5 MB (§11).
- **H4.3 LiveKit odalar.** `media_rooms` + `ended_at`. Kabul: oda açma/kapama + iz temizliği testli.
- **H4.4 DM.** `dm_key` tekilleştirme (§7). Kabul: ikinci kanal açılmaz.
- **H4.5 Bildirim + deep-link (P6 ile).** Dört §4.8 durumu provada. Kabul: bildirimden ekrana düşüş.
- **H4.6 Beş ekran + dört bileşen (livekit-client 2.22 §3.1).** Kabul: cuma provasında H4 çıkışı kanıtlanır.

## H5 — Liderlik haftan

- **H5.7 Online akış (P7 ile).** `is_online`/`online_url` → oda. Kabul: canlı odada ses+görüntü+sohbet (§1.2 akışı).
- **H5.11 Sohbet dosya eki.** `kind=file`: `POST /media` (5 MB, tip içerikten §4.9) + `GET /media/{id}` (önbellek başlıklı) + `DELETE /media/{id}`; telefonda WebP küçültme (`@jsquash/resize` §3.1). Kabul: gönderilir/açılır/silinir. (D5 dışı — sohbetin parçası.)
- **Liderlik:** 15 iş — bekleme zincirleri tablosuyla aç (H5.1→H5.2, H3.7→H5.4). Cuma üç prova + P6'ya devir.

## H6 — Kanıt haftan

- **H6.12 Presence ölçeği.** Valkey pub/sub + 30 dk < 5 MB raporu. Kabul: ölçüm raporu docs'ta.
- **H6.7-pay.** LiveKit notları `runbook.md`'ye (portlar dahil).

## H7 — Demo

Medya ayağı sende (H7.1); R12: kayıt hazır, canlıya güvenme.

## Risklerin

R9 portları H1.11'de çözülür, H4'e taşınmaz. Ping + pencere + iz kuralları H4.1'de yazılır.
