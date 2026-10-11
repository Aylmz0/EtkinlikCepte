# P2 — Kulüpler, etkinlikler, biletler

**Alan (sabit, §6):** Kulüp/üyelik, etkinlik, kayıt, bilet + QR, davetiye, **kulüp sosyal medyası (metin)**. Fotoğraf (D2), yorum (D3) yok. 7 hafta bu kavramdasın.
**Buddy:** P5 (§6.2). **Lider haftan:** H2.

## Envanterin

- **Tablolar (§7):** `clubs`, `club_members` (owner/admin/moderator/member), `club_invitations`, `events` + `event_sources`, `event_tickets`, `registrations` (§4.2 makinesi), `event_invitations`, `club_followers`, `club_posts` (public/followers/members), `club_post_likes`, `reports`.
- **Uçlar (§8):** Kulüp, Takipçilik, Gönderiler (+beğeni), Akış (`GET /feed?cursor=`), Etkinlik, Kaynaklar (`GET /events/{id}/sources`), Bilet, Davetiye, Şikâyet.
- **Bileşenlerin (§3.1):** `ClubBadge`, `PostCard`, `PostComposer`, `FollowButton`, `TicketRow`, `QRDisplay`.
- **Ekranların (§1.6):** `/invite/[code]`, `/settings/following`, `/clubs/[id]/followers`, `/clubs/[id]/new-post`; ortak: `/clubs/[id]` (P6), `/(tabs)/feed` (P7), `/scanner` (P7).
- **Dizinlerin (§5):** `apps/api/app/{routers,schemas,services,domain}/` (kulüp/etkinlik/bilet/davetiye/akış), `apps/api/tests/`.
- **Kuralların:** Kapasite `quantity`/`sold_count`tan düşer (§7, §8.1 md.7); `sold_count` yalnızca `paid`+`free_granted`; yazmalarda `Idempotency-Key` (md.6).

## H1 — Karar haftan

- **H1.5 Hurl ilk 5 (yazar sensin).** `apps/api/hurl/`da auth+kulüp happy-path'leri; P1 doğrular. Kabul: `just hurl` 5/5. Çıktı: H3.8 temeli.
- **H1.7 Bilet makinesi + QR kararı.** `reserved(15 dk) → pending_payment → paid → used`, `free_granted`, `cancelled/expired/refunded` (§4.2); organizatör tek dokunuşla `paid`. Adımlar: 1. Geçiş tablosu + otomatik iptal. 2. QR = `qr_token` UNIQUE + segno. 3. Kararı PR'a yaz. Kabul: geçiş matrisi testli. Çıktı: H2.5, H5.1.
- **H1.8 Router taslakları.** P1 iskeletine kulüp/etkinlik uçları (boş gövde + Pydantic). Kabul: `/openapi.json`'da görünür. Çıktı: H2.3/H2.4.

## H2 — Çekirdek (lider sensin)

- **H2.3 Kulüp/üyelik/roller.** `GET/POST /clubs`, `GET/PATCH /clubs/{id}`, üyelik uçları, `POST /clubs/{id}/invitations` + `POST /invitations/{code}/redeem`. Kabul: rol testi (üye kapalı içeriği göremez §1.2) + pytest payın (%90 hedefine §12). Çıktı: P6 (H2.11).
- **H2.4 Etkinlik + kayıt.** `GET/POST /events`, `GET/PATCH`, `/cancel`, `/publish`; `status` draft/published/cancelled/completed. Kabul: kapasite kuralı testi. Çıktı: P7 (H3.4).
- **H2.5 Bilet + QR üretim.** `GET /events/{id}/tickets`, `POST …/register`, `DELETE /registrations/{id}`, `GET …/qr`; grup bileti `quantity > 1` (§7). Kabul: QR okunur, sayım kuralı testli. Çıktı: H5.1, P7 (H5.3).
- **H2.11-destek.** `/clubs/[id]` ekranında P6'ya alan bilgisi.
- **Liderlik:** Cuma provası giriş→bilet al + P3'e devir notu.

## H3 — Takipçilik + kapsam

- **H3.7 Takipçilik.** `POST/DELETE /clubs/{id}/follow`, listeler, `GET /users/me/following`. Üyelikten ayrı tablo (20 üye/2000 takipçi §1.2). Kabul: sayaç testi + `(user_id, created_at DESC)` indeksi. Çıktı: H5.4, P4 (H4.8 w6).
- **H3.8-pay.** Uçların tam Hurl kapsamlı. Kabul: kulüp/etkinlik/bilet/davetiye yeşil.
- **H3.9-katılım.** Kulüp/bilet ayağının durumu (§6.1 P2 satırı). Kabul: tablon hazır.

## H4 — Yarış haftan

- **H4.11 Kayıt/kapasite yarış testleri.** Hedef: aynı anda iki kayıt `UNIQUE(event_id, user_id)`'yi ve `sold_count`'u bozmasın. Adımlar: 1. pytest'te eşzamanlı register senaryosu (H2.5 endpoint'lerine karşı). 2. `reserved`/`pending_payment`'in saymaması iddiası. 3. Hurl'a ekle. Kabul: yarış testi yeşil. Çıktı: H5.1'in güveni.
- Ayrıca: P5'in H4.6 kulüp bağlamı soruları (C konumun) — aynı gün yanıt.

## H5 — Topluluk (en yoğun haftan)

- **H5.1 Davetiye + QR okutma.** Kulüp/etkinlik aynı yol (§8); `GET /invitations/{code}` tür döndürür; `max_uses/uses`. Kabul: kabul akışı testli. Çıktı: H5.2, H5.12.
- **H5.2 `/scanner` (P7 ile).** `POST …/checkin` → `used` + `checked_in_at`; QR çevrimdışı okunur (§1.5). Kabul: gerçek QR cihaz provası.
- **H5.4 Gönderi + akış (P7 ile; backend senin).** `POST /clubs/{id}/posts` (yalnızca yönetici/mod. §1.2), liste `?before=`, `PATCH/DELETE`, `GET /feed?cursor=`; `link_url` dış bağlantı (§4.13); soft-delete. Kabul: üç görünürlük kademesi testli.
- **H5.5 Beğeni.** `POST/DELETE /posts/{id}/like`, idempotent. Kabul: çift beğeni tek kayıt.
- **H5.6 Moderasyon.** `POST /reports`, `/admin/reports*` (open→reviewed→actioned). Kabul: üye silemez testi.
- **H5.12 Ekranların.** `/invite/[code]`, `/settings/following`, `/clubs/[id]/followers`, `/clubs/[id]/new-post` (`PostComposer` + formsnap/superforms/Zod doğrulama §3.1). Kabul: §16 ekran kutuları.

## H6 — Regresyon haftan

- **H6.16 QR/check-in regresyonu (P7 ile).** Hedef: H6.2'nin 8 akışındaki bilet ayağı cihazda. Adımlar: 1. Üret→cüzdan→çevrimdışı aç→okut→`used` zinciri. 2. Bozuk/tekrar QR red senaryoları. Kabul: zincir yeşil. Çıktı: H6 çıkışı.
- **H6.7-pay.** Kulüp-bilet sözleşme/ADR payın.

## H7 — Demo

Kulüp→bilet→QR ayağı provada sende (H7.1). Bozulursa ilk müdahale.

## Risklerin

R5: API'yi H1.8'den erken dondur, P6/P7 beklemez. §6.1: H3 işlerin yarından azı biterse kesinti gündeme gelir — H3.9'a tablon hazır.
