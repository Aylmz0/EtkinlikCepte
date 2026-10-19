# Portlar (§13.2 + compose*.yaml)

| Servis | Port | Nerede açık |
|---|---|---|
| PostgreSQL | 5432 | Yalnızca localhost (dev) |
| Valkey | 6379 | Yalnızca localhost (dev) |
| Martin | 3000 | Yalnızca localhost (dev) |
| Caddy | 80, 443 | Herkese |
| LiveKit API/WS | 7880 TCP | Yalnızca localhost (dev) |
| LiveKit RTC | 7881 TCP, 7882 UDP | Yalnızca localhost (dev) |
| LiveKit medya | UDP 50000-50100 | Güvenlik grubunda açık (R9: engel H1.11'de doğrulanır) |

## Telefonla yerel deneme (R9)

Konteynerdeki LiveKit ICE adayında konteyner IP'sini bildirir; 7881/7882/50000-50100
varsayılan olarak 127.0.0.1'e bağlı olduğundan LAN'daki telefon bağlanamaz. Compose `.env`'i
`infra/` altından okur; en kolayı değişkenleri komutla vermek
(`LIVEKIT_BIND=0.0.0.0 LIVEKIT_NODE_IP=192.168.1.20 just dev`):

- `LIVEKIT_BIND=0.0.0.0`
- `LIVEKIT_NODE_IP=<PC LAN IP'si>` (LiveKit'e `--node-ip` olarak geçer)

Windows güvenlik duvarında TCP 7880/7881 ile UDP 7882 ve 50000-50100 portlarını aç.
Gerçek UDP engeli H2.18 canlı oda provasında doğrulanır.
