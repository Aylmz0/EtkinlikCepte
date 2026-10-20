# P2 — Eren Yığmatepe — Backend Engineer, Ticketing & Social

**Alan (sabit, §6 Ekip):** Kulüp/üyelik, etkinlik, kayıt, bilet + QR, davetiye, **kulüp sosyal medyası (metin)**. Fotoğraf (D2) ve yorum (D3) kapsam dışı; bunlara dokunmazsın. 7 hafta bu kavramdasın.
**Buddy:** P5 (§6.2 Çalışma kuralları eşleşmesi). **Lider haftan:** H2.

## Envanterin

Bu dosyadaki işler şu tablo, uç, bileşen, ekran ve dizinlerle yapılır. Hepsi `development.md`'de tanımlı; burası sadece senin listen:

- **Tablolar (§7 Veri modeli):** `clubs`, `club_members` (roller: owner/admin/moderator/member), `club_invitations`, `events` + `event_sources`, `event_tickets`, `registrations` (§4.2 Ödeme'deki durum makinesi), `event_invitations`, `club_followers`, `club_posts` (görünürlük: public/followers/members), `club_post_likes`, `reports`.
- **Uçlar (§8 API sözleşmesi):** Kulüp, Takipçilik, Gönderiler (+beğeni), Akış (`GET /feed?cursor=`), Etkinlik, Kaynaklar (`GET /events/{id}/sources`), Bilet, Davetiye, Şikâyet.
- **Bileşenlerin (§3.1 Mobil yığın):** `ClubBadge`, `PostCard`, `PostComposer`, `FollowButton`, `TicketRow`, `QRDisplay`. Bunları P6 paketler, sen tüketirsin; görünümüne karışmazsın.
- **Ekranların (§1.6 Ekran listesi):** `/invite/[code]`, `/settings/following`, `/clubs/[id]/followers`, `/clubs/[id]/new-post`; ortak: `/clubs/[id]` (P6 ile), `/(tabs)/feed` (P7 ile), `/scanner` (P7 ile).
- **Dizinlerin (§5 Depo yapısı):** `apps/api/app/{routers,schemas,services,domain}/` içinde kulüp/etkinlik/bilet/davetiye/akış dosyaların + `apps/api/tests/` altında testlerin.
- **Kuralların:** Kapasite `quantity`/`sold_count` üzerinden düşer, kayıt sayısından değil (§7 Veri modeli, §8.1 Sözleşme kuralları md.7); `sold_count` yalnızca `paid` + `free_granted` durumlarından artar; bilet alma gibi yazma işlerinde `Idempotency-Key` başlığı zorunlu (md.6).

## H1 — Karar haftan

Bu hafta koddan çok karar üretiyorsun: biletin durum makinesi, QR biçimi ve ilk testler kâğıt üstünde netleşir, çalışan koda H2'de dönüşür.

- **H1.5 Hurl ilk 5 (yazar sensin).** Hurl, sunucuya gerçek istek atıp cevabı denetleyen sözleşme test aracıdır (§12 Test stratejisi). **Hedef:** kimlik + kulüp uçlarının ilk 5 happy-path testi dosyada dursun. Sözleşmeden (§8 API sözleşmesi uçları) yazılır, çalışan kod beklenmez; koşması H3.8 toplu test haftasında (H1.2 önceki haftadan). P1 doğrular. **Kabul:** 5 test dosyası yazıldı. **Çıktı:** H3.8'e girdi olarak girer.
- **H1.7 Bilet makinesi + QR kararı.** Biletin hayat hikâyesi: `reserved` (15 dk) → `pending_payment` → `paid` → `used`, ayrıca `free_granted` (ücretsiz), `cancelled`/`expired`/`refunded` (§4.2 Ödeme); organizatör bekleyen ödemeyi tek dokunuşla `paid` yapar. **Adımlar:** 1. Geçiş tablosu + süresi dolanın otomatik iptali. 2. QR içeriği = `qr_token` benzersiz alanı + segno üretim kütüphanesi. 3. Kararı PR açıklamasına yaz (§4.2'deki tablo esas alınır, kod beklenmez). **Kabul:** karar + geçiş matrisi yazılı, pytest iskeleti hazır (koşması H2.4'te, H1.2 önceki haftadan). **Çıktı:** H2.5 bilet üretimi ile H5.1 davetiye işi bu karara dayanır.
- **H1.8 Router taslakları.** FastAPI'de her uç grubunun dosyası (router) ayrı durur; taslak = boş gövde + Pydantic doğrulama şeması. Kulüp/etkinlik uçlarını iskeletten bağımsız yazarsın. **Kabul:** taslak PR açık (sözleşme diff'i temiz); birleştirme H2.3/H2.4 işlerinin başında yapılır (H1.2 önceki haftadan). **Çıktı:** H2.3/H2.4 implementasyonları bu taslaklardan büyür.

## H2 — Çekirdek (lider sensin)

Bu hafta ürünün para eden çekirdeğini yazıyorsun: kulüp, etkinlik, bilet. Cuma provası senin sorumluluğunda.

- **H2.3 Kulüp/üyelik/roller.** `GET/POST /clubs`, `GET/PATCH /clubs/{id}`, üyelik uçları, `POST /clubs/{id}/invitations` + `POST /invitations/{code}/redeem`. **Kabul:** rol testi yeşil (üye, kapalı kulüp içeriğini göremez §1.2 Uygulama) + pytest payın (hedef: `services/`+`domain/` %90, §12 Test stratejisi). **Çıktı:** P6'nın H2.11 kulüp ekranları bu uçlara dayanır.
- **H2.4 Etkinlik + kayıt.** `GET/POST /events`, `GET/PATCH`, `/cancel`, `/publish`; `status` alanı draft/published/cancelled/completed değerlerini alır. **Kabul:** kapasite kuralı testi yeşil. **Çıktı:** P7'nin H3.4 detay ekranı buradan beslenir.
- **H2.5 Bilet + QR üretim.** `GET /events/{id}/tickets`, `POST …/register`, `DELETE /registrations/{id}`, `GET …/qr`; grup bileti demek `quantity > 1` demek (§7 Veri modeli). **Kabul:** QR okunur, sayım kuralı testli. **Çıktı:** H5.1 davetiye işi ile P7'nin H5.3 cüzdanı buraya dayanır.
- **H2.11-destek.** `/clubs/[id]` ekranında P6'ya alan bilgisi verirsin (rol/görünürlük kuralları); kod yazmazsın, danışılan konumundasın.
- **Liderlik:** Cuma provası: giriş→bilet al zinciri çalışır; P3'e devir notu yazarsın.

## H3 — Takipçilik + kapsam

- **H3.7 Takipçilik.** `POST/DELETE /clubs/{id}/follow`, takipçi/takip listeleri, `GET /users/me/following`. Üyelikten ayrı tabloda tutulur — bir kulübün 20 üyesi, 2000 takipçisi olabilir (§1.2 Uygulama). **Kabul:** sayaç testi + `(user_id, created_at DESC)` indeksi yeşil. **Çıktı:** H5.4 takip akışı + P4'ün H4.8 w6 kalibrasyonu buradan beslenir.
- **H3.8-pay.** Kendi uçlarının (kulüp/etkinlik/bilet/davetiye) Hurl kapsamı sende; başkasını beklemezsin. **Kabul:** dört grup yeşil.
- **H3.9-katılım.** Kulüp/bilet ayağının durumu (§6.1 Değerlendirme'deki P2 satırı). **Kabul:** tablon hazır.

## H4 — Yarış haftan

- **H4.11 Kayıt/kapasite yarış testleri.** **Hedef:** aynı anda gelen iki kayıt isteği `UNIQUE(event_id, user_id)` kısıtını ve `sold_count` sayacını bozmasın. **Adımlar:** 1. pytest'te eşzamanlı register senaryosu yaz (H2.5 endpoint'lerine karşı). 2. `reserved`/`pending_payment` durumlarının sayaca katılmadığı iddiasını ekle. 3. Hurl'a ekle. **Kabul:** yarış testi yeşil. **Çıktı:** H2.5 regresyon koruması (H5.1 üstüne kurulur).
- Ayrıca: P5'in H4.6 kulüp ekranlarındaki kulüp bağlamı sorularında C/danışılan konumundasın — bekletmeden yanıtla.

## H5 — Topluluk (en yoğun haftan)

Bu hafta kulübün sosyal yüzünü bitiriyorsun: davetiye, kapı doğrulama, gönderi, beğeni, moderasyon + kendi ekranların.

- **H5.1 Davetiye + QR okutma.** Kulüp ve etkinlik davetiyesi aynı yolu kullanır (§8 API sözleşmesi); `GET /invitations/{code}` davetiyenin türünü döndürür, kullanıcı neye katılacağını önceden bilir; `max_uses`/`uses` sayaçları kaç kişide kullanıldığını gösterir. **Kabul:** kabul akışı testli. **Çıktı:** H5.2 scanner ile H5.12 ekranların buraya dayanır.
- **H5.2 `/scanner` (P7 ile).** Kapı görevlisinin QR okuttuğu ekran; `POST …/checkin` kaydı `used` yapar + `checked_in_at` damgası vurur; QR çevrimdışıyken de okunur (§1.5 Kullanıcı görünümü). H5.1 gelene kadar mock QR yüküyle başlar. **Kabul:** mock QR akışı yeşil; gerçek cihaz provası H6.16'da (H5.1 önceki haftadan).
- **H5.4 Gönderi + akış (P7 ile; backend senin).** `POST /clubs/{id}/posts` yalnızca yönetici/mod. açabilir (§1.2 Uygulama), liste `?before=` ile sayfalanır, `PATCH/DELETE` ile düzenlenir/silinir, `GET /feed?cursor=` takip edilenlerin akışını verir; `link_url` dış video/bağlantı (§4.13 Gönderiler); silinen kayıtlar saklanır (`deleted_at` §7 Veri modeli). **Kabul:** üç görünürlük kademesi (public/followers/members) testli.
- **H5.5 Beğeni.** `POST/DELETE /posts/{id}/like`, idempotent (iki kez basınca tek kayıt). **Kabul:** çift beğeni tek kayıt.
- **H5.6 Moderasyon.** `POST /reports` şikâyeti + `/admin/reports*` kuyruğu (open→reviewed→actioned §7 Veri modeli). **Kabul:** üye silemez testi yeşil (yalnızca yönetici siler).
- **H5.12 Ekranların.** `/invite/[code]`, `/settings/following`, `/clubs/[id]/followers`, `/clubs/[id]/new-post` (`PostComposer` + formsnap/superforms/Zod doğrulama §3.1 Mobil yığın). **Kabul:** §16 Bitti tanımının ekran kutuları (Türkçe metin, 44px dokunma hedefi, koyu mod, yükleme göstergesi).

## H6 — Regresyon haftan

- **H6.16 QR/check-in regresyonu (P7 ile).** **Hedef:** H6.2'nin 8 akışındaki bilet ayağı gerçek cihazda kanıtlansın. **Adımlar:** 1. Üret→cüzdan→çevrimdışı aç→okut→`used` zincirini koş. 2. Bozuk/tekrar QR red senaryoları. **Kabul:** zincir yeşil (P7 ile eşzamanlı koşar). **Çıktı:** H6 çıkış ölçütüne kanıt.
- **H6.7-pay.** Kulüp-bilet alanının sözleşme/ADR payını yazarsın.

## H7 — Demo

**H7.5 Bilet/QR demo verisi doğrulama + yedek QR.** Demo öncesi biletli kullanıcı, kullanılmış/iptal bilet ve yedek QR çıktısı hazırlanır. **Kabul:** prova sırasında QR okutma zinciri çalışır; yedek QR basılı hazır.
Kulüp→bilet→QR ayağı provada sende (H7.1). Bozulursa ilk müdahale sende.

## Risklerin

R5 (ekran işi yetişmez): API'yi H1.8 taslağıyla erken dondur; P6/P7 beklemez. §6.1 Değerlendirme: H3 işlerin yarısından azı biterse kesinti gündeme gelir — H3.9'a tablon hazır.
