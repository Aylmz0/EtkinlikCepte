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
