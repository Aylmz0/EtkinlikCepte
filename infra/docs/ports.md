# Portlar (§13.2 + compose*.yaml)

| Servis | Port | Nerede açık |
|---|---|---|
| PostgreSQL | 5432 | Yalnızca localhost (dev) |
| Valkey | 6379 | Yalnızca localhost (dev) |
| Martin | 3000 | Yalnızca localhost (dev) |
| Caddy | 80, 443 | Herkese |
| LiveKit API/WS | 7880 TCP | Yalnızca localhost (dev) |
| LiveKit RTC | 7881 TCP, 7882 UDP (tüm medya bu tek UDP portundan, UDP mux) | Yalnızca localhost (dev); sunucuda güvenlik grubunda açık |

## Telefonla yerel deneme (R9)

Konteynerdeki LiveKit ICE adayında konteyner IP'sini bildirir; 7880/7881/7882
varsayılan olarak 127.0.0.1'e bağlı olduğundan LAN'daki telefon bağlanamaz. Compose `.env`'i
`infra/` altından okur; en kolayı değişkenleri komutla vermek
(`LIVEKIT_BIND=0.0.0.0 LIVEKIT_NODE_IP=192.168.1.20 just dev`):

- `LIVEKIT_BIND=0.0.0.0`
- `LIVEKIT_NODE_IP=<PC LAN IP'si>` (LiveKit'e `--node-ip` olarak geçer)

Windows güvenlik duvarında TCP 7880/7881 ve UDP 7882 portlarını aç.

## Neden 50000-50100 aralığı yok (R9, 2026-10-19 doğrulandı)

Geliştirme makinesinde aralık açılamadı: Windows 50000-50059'u rezerve ediyor
(`netsh int ipv4 show excludedportrange protocol=udp`), antivirüs de 50067-50072'yi tutuyordu.
LiveKit `udp_port` ile tüm medyayı tek UDP portundan geçirir (`port_range_*` ayarlıysa
`udp_port` yok sayılır). Tek node için yeterli ve güvenlik duvarında tek port açılır.
`development.md` §13.2'deki 50000-50100 satırı P1 onayıyla güncellenmeli.
