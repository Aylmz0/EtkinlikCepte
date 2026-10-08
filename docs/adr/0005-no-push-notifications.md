# ADR-0005: Uygulama kapalıyken bildirim gönderilmez

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §4.8

## Karar

Uygulama açıkken bildirim anında gelir, kapalıyken gelmez. Android bildirim servisine (FCM) bağlanılmaz.

## Gerekçe

**FCM ücretsiz değil ve ticari şartlar içerir.** Google'ın bildirim altyapısına bağlanmak ücretli hesap ve kullanım koşulları demek. FOSS-only bir proje için kabul edilmedi.

**Arka planda WebSocket güvenilir değil.** Android uygulamayı öldürdüğünde bağlantı düşer. Başlatıcı servis kullanmak pil tüketimini ciddi biçimde artırır ve kısıtlamaların bir kısmına takılır.

**Sunucu bildirimi gecikmeden saklar.** `notifications` tablosu kalıcı. Kullanıcı uygulamayı açtığında `GET /notifications` ile kaçırdıklarını görür — hiçbir bildirim kaybolmaz, sadece o anda telefonuna gitmez.

| Durum | Bildirim |
|---|---|
| Uygulama açık, WebSocket bağlı | Anında, ekran içi bildirim + rozet |
| Uygulama açık, arka planda | Anında, sistem bildirimi |
| Uygulama kapalı | Yok |
| Bildirim açıkken internet yok | Kuyruğa alınır, bağlantı gelince gönderilir |

## Sonuçlar

**`devices` tablosunda push token yok.** Sunucu kime ne göndereceğini bilmiyor. Tablo yalnızca çevrimiçi durumu ve sürüm bilgisi tutar.

**`POST /devices` endpoint'i var**, ama bildirim kaydı değil, varlık kaydı içindir. WebSocket açılışında `app_version` bildirilir.

**Kullanıcı beklentisi yönetilmeli.** Uygulama içinde bu davranış açıkça yazılıdır; ayarlarda "bildirimler" başlığında durum gösterilir.

**Demo riski.** Demo gününde telefonu kilitleyen bir sunum yapılırsa bildirim gelmez. Demo akışı bu varsayımla prova edilir.