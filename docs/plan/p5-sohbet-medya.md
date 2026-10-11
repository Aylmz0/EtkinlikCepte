# P5 — Sohbet ve medya

**Alan (sabit, §6):** Sohbet, özel mesaj, çevrimiçi durumu, bildirim, ses/görüntü. Medya tek elinde. 7 hafta bu kavramdasın.
**Buddy:** P2 (§6.2). **Lider haftan:** H5.

## Envanterin

- **Tablolar (§7):** `chat_channels` (dm/club/event; `dm_key` tekilleştirme), `chat_members` (`last_read_at`), `chat_messages` (text/file/link/system, `reply_to`), `media_rooms` (`livekit_room` UNIQUE), `notifications`, `devices` (push token YOK §4.8), `media` (ek: `chat_attachment` 5 MB).
- **Uçlar (§8):** `GET /channels`, `GET /channels/{id}/messages?before=`, `POST …/messages`; `POST /channels/dm`, `GET /channels?kind=dm`, `POST …/read`; `GET /events/{id}/room/token`, `POST /channels/{id}/room/token`; `GET /notifications`, `POST …/read`; WS `GET /ws?token=` (7 tip).
- **Dizinlerin (§5):** `apps/api/app/{realtime,media,notifications}/`, `apps/mobile/src/lib/realtime/` (WS istemcisi + presence store).
- **Kurallar (§11):** 30 sn ping, 1/2/4/8 yeniden bağlanma, 200 pencere + sayfalama, boşta WS < 5 MB, iz çıkarken kapanır, yazmalarda `Idempotency-Key` (§8.1 md.6).
- **Bildirim (§4.8):** açık+WS anında + rozet; arka plan sistem; kapalı yok; internetsiz kuyruk.
- **Ekranların (§1.6):** `/clubs/[id]/chat`, `/(tabs)/messages`, `/channels/[id]`, `/events/[id]/room` + `/channels/[id]/room`, `/notifications`. Bileşenlerin: `ChatBubble`, `PresenceDot`, `VoiceBar`, `VideoTile`.

## H1 — Deneme haftan

- **H1.11 LiveKit + Valkey + WS şeması.** Adımlar: 1. Tek node LiveKit + Valkey 9 (`compose.dev`). 2. Deneme odasında ses (R9: TCP 7880, UDP 7881/7882 + 50000-50100 → `infra/docs/ports.md`). 3. 7 `/ws` tipini PR'a yaz. Kabul: ses + port listesi. Çıktı: H2.18, H4.1–H4.4.

## H2 — Hazırlık haftan

- **H2.18 Token uçları.** `livekit-api` ile oda jetonları (etkinlik + kanal §8). Kabul: jetonla giriş. Çıktı: H4.3.
- **H2.19 Devices + bildirim API.** `POST /devices`, `GET /notifications` + okundu + kuyruk kuralı (§4.8). Kabul: açılışta çekilir. Çıktı: H4.5.
- **H2.20 Realtime istemci iskeleti.** `apps/mobile/src/lib/realtime/` (WS istemcisi + presence store) + `@tanstack/svelte-query` anahtarları (§5.1: istekler `lib/api/`da). Kabul: iskelet bağlanır/kopanır (1/2/4/8). Çıktı: H4.6.
- Ayrıca: P1'in H2.1'ini izle (korumalı WS); buddy P2'ye kulüp bağlamı.

## H3 — Sözleşme haftan

- **H3.14 WS testleri + tip dokümanı.** Hurl iskeleti + 7 tipin anlamı. Kabul: iskelet yeşil.
- **H3.16 Bildirim metinleri + rozet sayacı.** `locales/tr.json` girdileri (başlık/gövde şablonları §4.8) + bildirim rozet sayacı kuralı. Kabul: metinler `tr.json`'da, sabit metin yok (§16). Çıktı: H4.5/H4.6.
- **H3.8-pay.** Sohbet/DM/oda/bildirim Hurl payın.
- **H3.9-katılım.** Medya ayağının durumu + §6.1 P5 satırı (işlerin yarından azı biterse kesinti). Kabul: tablon hazır.

## H4 — Büyük haftan

- **H4.1 WS sohbet.** Kanal/mesaj/yazıyor + `reply_to` + `kind`. Kabul: 200 pencere + sayfalama testi.
- **H4.2 Presence + dağıtım.** Valkey pub/sub. Kabul: 30 dk < 5 MB (§11).
- **H4.3 LiveKit odalar.** `media_rooms` + `ended_at`. Kabul: aç/kapat, iz temizliği.
- **H4.4 DM.** `dm_key` tekilleştirme (§7). Kabul: ikinci kanal açılmaz.
- **H4.5 Bildirim + deep-link (P6 ile).** Dört §4.8 durumu provada. Kabul: bildirimden ekrana düşüş.
- **H4.6 Beş ekran + dört bileşen (livekit-client 2.22 §3.1).** Kabul: cuma provası = H4 çıkışı.

## H5 — Liderlik haftan

- **H5.7 Online akış (P7 ile).** `is_online`/`online_url` → oda. Kabul: canlı odada ses+görüntü+sohbet (§1.2 akışı).
- **H5.11 Sohbet dosya eki.** `kind=file`, `POST /media` (5 MB, tip içerikten §4.9), telefonda WebP küçültme (`@jsquash/resize` §3.1). Kabul: gönderilir/açılır. (D5 dışı — sohbetin parçası.)
- **Liderlik:** 15 iş — zincir tablosuyla aç (H5.1→H5.2, H3.7→H5.4). Cuma üç prova + P6'ya devir.

## H6 — Kanıt haftan

- **H6.12 Presence ölçeği.** Valkey pub/sub + 30 dk < 5 MB raporu. Kabul: ölçüm raporlu.
- **H6.7-pay.** LiveKit notları `runbook.md`'ye (portlar dahil).

## H7 — Demo

Medya ayağı sende (H7.1); R12: kayıt hazır, canlıya güvenme.

## Risklerin

R9 portları H1.11'de kapat, H4'e taşıma. Ping/pencere/iz kuralları H4.1'de olur.
