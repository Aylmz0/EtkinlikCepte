# ADR-0003: Kullanılmayacak bağımlılıklar

**Tarih:** 2026-10-06
**Durum:** Kabul edildi
**Kapsam:** §3.5

## Karar

Aşağıdaki bağımlılıklar projeye eklenmez.

## Gerekçe

| Ne | Neden |
|---|---|
| `tauri-plugin-shell` | Telefonda çalışmıyor, güvenlik riski |
| `keyring` eklentisi | Telefonda arkasında gerçek arka plan yok |
| HTMX | Tauri sunucu tarafı sayfa üretimini desteklemiyor |
| selectolax, BeautifulSoup4 | lxml + parsel yeterli; ikinci kütüphane gerekmiyor |
| passlib | Bakımı durdu |
| bcrypt | Uzun parolaları sessizce kırpıyor |
| shiki | Etkinlik açıklamasında kod bloğu yok |
| Tarayıcıda grafik kütüphanesi | Grafikleri sunucu üretir |
| MinIO | Nisan 2026'da bakımı durdu |
| UnoCSS | Bkz. [ADR-0007](0007-css-framework.md) |

İki gerekçe türü var ve ikisi de geçerli:

**Bakım durduğu için** — passlib, MinIO. Bakımı durmuş bir kütüphaneye güvenlik açığı çıktığında yama alacak kimse yok. Yeni bir bağımlılık eklenirken de aynı ölçüt uygulanır: son 12 ayda sürüm çıkmadıysa eklenmez.

**Proje dışı olduğu için** — shiki, tarayıcı grafik kütüphanesi. Çalışmayacak kod yazmak, sonradan "belki lazım olur" diye büyütmekten iyidir.

## Sonuçlar

**Denetim otomatik.** `deny.txt` bu listeyi tutar; CI, PR'ın eklediği bağımlılıkları bu listeye karşı kontrol eder. Yeni bir bağımlılık eklemek isteyen bu dosyayı güncellemek zorundadır — gerekçeyi ADR'ye yazar.

**İkinci kütüphane eklenmez.** lxml ve parsel birlikte çalışır, ikisi de aynı C parser'ı kullanır. HTML çözümlemesi ikinci bir kütüphaneyi ölçülebilir bir darboğaz yaratmadığı sürece eklenmez.

**Grafikler sunucuda.** `GET /discover/events/[id]/trend` PNG vektör döndürür, telefon indirip çizmez. Bu, paket boyutunu ve pil tüketimini düşürür.