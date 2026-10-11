# P1 — Abdullah Yılmaz — Teknik lider + altyapı

**Alan (sabit, §6):** Sözleşme, veritabanı şeması, kimlik doğrulama, sunucu kurulumu. 7 hafta boyunca bu kavramdasın.
**Buddy:** P3 (§6.2). **Lider haftan:** H1. **Kalıcı yetki:** `/v1` bozma, şema ve göç onayı (§6.2, §8.1).

## Envanterin

- **Tablolar (§7):** `users`, `refresh_tokens`, `devices`, `audit_log` + tüm göçler (`apps/api/alembic/`).
- **Dizinlerin (§5):** `apps/api/app/{core,domain,schemas,routers,services,repos}`, `apps/api/{pyproject.toml,tests/}`, `ruff.toml`, `.editorconfig`.
- **Uçlar (§8):** `POST /auth/register|login|refresh|logout`, `GET /auth/me`, `GET /health|metrics|openapi.json`.
- **Komutların:** `just setup|dev|migrate|hurl|ci`, `mise install|trust`, `alembic upgrade head`.
- **Kapıların (§13.1):** `contract` (diff boş), `migrate` (boş DB), `audit`, `deny`.

## H1 — Temeller (lider sensin)

- **H1.1 Depo/mise/just/Podman.** Hedef: 7 kişi aynı sürümle başlar (§4.7). Adımlar: 1. `mise.toml`'a Node 24 LTS, Python 3.13, uv, just, Podman pin'le. 2. `justfile`: `setup/dev/test/ci/hurl/migrate` + `services` (oxker §3.4) (§15). 3. Temiz makinede `just setup` dene. Kabul: ikinci makinede `just setup && just dev` çalışır. Çıktı: H1.2/H1.4/H1.12/H1.6'nın girdisi hazır.
- **H1.2 FastAPI iskeleti + OpenAPI v1.** Hedef: Pydantic'ten OpenAPI 3.1 (§4.5). Adımlar: 1. `apps/api/app/main.py` + boş router'lar (`auth, clubs, events, channels, discover, media, admin`). 2. `GET /openapi.json` + `GET /health`. 3. Yığın: Uvicorn + uvloop + orjson + hiredis + psycopg havuzu (PgBouncer yok §11) + structlog — hepsi `apps/api/app/core/`da. 4. `just api-types` provası. Kabul: `/openapi.json` 200. Çıktı: P2 (H1.7/H1.8), P3 (H1.9).
- **H1.3 Şema v1 + Alembic.** Hedef: §7 tabloları + kritik indeksler (`events(starts_at)`, `venues` GIST, `chat_messages(channel_id, created_at DESC)`…). Adımlar: 1. Modeller (para kuruş INT + `CHAR(3)`; zaman TIMESTAMPTZ). 2. `alembic revision` + boş DB'de `upgrade head`. 3. CI `migrate` adımı. Kabul: boş DB migrate + şema karşılaştırma yeşil. Çıktı: H2 backend'lerinin tamamı.
- **H1.4 Compose.** postgres+postgis, valkey, caddy, martin (§2). Adımlar: 1. `infra/compose.yaml` + `compose.dev.yaml`. 2. Caddyfile (HTTP; HTTPS H5.15'te). 3. `infra/docs/ports.md` aç. Kabul: `pg_isready` + Valkey `PING` + Martin `/health`. Çıktı: P4 (H1.10/H1.17), P5 (H1.11).
- **H1.6 CI iskeleti.** Hedef: §13.1 adımları. Adımlar: 1. Platform kararı (kurum hesabı / Forgejo). 2. `deny.txt` (ADR-0003) + ilk PR'ı CI'dan geçir. Kabul: kırmızı PR merge edilemez.
- **Desteklerin (ID'siz, pair/onay):** H1.5'te P2'nin Hurl'larını doğrula · H1.9'da P3 ile pair (R11) · H1.16 migration'ını onayla · H1.17 Nominatim profilini gözden geçir.
- **Liderlik:** Pazartesi senkron + plan tebliği + §18 imza takibi. Cuma: imzasız APK + `just dev` + `/v1` dondu kontrolü + P2'ye devir notu.

## H2 — Çekirdek

- **H2.1 Auth.** `POST /auth/*` + `GET /auth/me` (argon2-cffi, PyJWT, `refresh_tokens`; hata RFC 9457 §8.1 md.5). Adımlar: 1. Pydantic şemalar. 2. Jeton yenileme + `revoked_at`. 3. Hurl auth akışı. Kabul: kayıt→giriş→yenileme→çıkış yeşil + pytest `services/`+`domain/` %90 (§12). Çıktı: P6 (H2.9), P4/P5 korumalı uçlar.
- **H2.2 Profil.** `users` CRUD (interests TEXT[], city, bio). Kabul: `GET /auth/me` profili döner. Çıktı: P6 (H2.11).
- **H2.12 `api-client` v1.** Adımlar: 1. H1.8 taslakları + H2.1/H2.2'ye karşı ilk üretim. 2. `git diff` boş + P6/P7'ye tur. H2.3–H2.5 düşünce yeniden üretim CI'da döner (rutin, bu görevin parçası değil). Kabul: ilk üretim diff-boş + import edilebiliyor. Çıktı: H3 ekranları.

## H3 — Veri haftası (senin işin: kapsam + değerlendirme)

- **H3.8-pay.** Kimlik/sistem/yönetim Hurl'ları (kendi uçların; başkasını beklemezsin) + rapor iskeleti; birleştirme H3.9'da (ritüel). Kabul: kendi payın yeşil.
- **H3.9-değerlendirme.** Teknik tablo (çıkan/çıkmayan + ana plan 3. bölüm ikinci dalga önerisi); P3 yönetir, kararı ekip verir. Kabul: karar yazılı.

## H4 — Denetim haftan

- **H4.10 Sözleşme denetimi.** Hedef: H4'te açılan WS/token uçları `/v1`'i bozmasın. Adımlar: 1. `POST /channels/{id}/messages`, DM, token uçlarının şemalarını H1.2 taslağıyla karşılaştır. 2. Bozan varsa ana sürüm artışı dayat (§8.1 md.1). 3. WS tip listesini onayla. Kabul: statik denetim notu PR'da (taslak + §7 + §8.1'e karşı, kod beklenmez); canlı doğrulama H6.5'te. Çıktı: H5 sözleşme denetimine dayanır.
- Ayrıca: P5'in H4.1–H4.4'ünde C/danışılan konumundasın; soruları bekletmeden yanıtla.

## H5 — Staging haftan

- **H5.15 Staging HTTPS + secrets.** Hedef: Caddy Let's Encrypt + `.env` SOPS/Infisical (§13.2). Adımlar: 1. Yer tutucu adreslerde (`api.projectx.app`) staging. 2. Secret'lar depoya girmez; şifreli. 3. Headscale erişimi. Kabul: HTTPS staging ayakta + denetim log'u. Çıktı: H6.4 (sürüm hattı).
- Ayrıca: P2'nin H5.1 QR şemasında kapasite kuralını (§8.1 md.7) gözden geçirirsin.

## H6 — Sıkılaştırma

- **H6.4 İmzalama (P7 ile).** Anahtar CI secret'ında, parola gizli (§13.2); `build-apk` yalnızca `main`/`release/*`. Kabul: CI'dan imzalı APK iner.
- **H6.5 Güvenlik.** Rol denetimi, `limits` hız sınırı, gizli anahtar taraması (+ `GET /admin/audit`, `audit_log` §7) + H4.10 bulgularının canlı doğrulaması. Kabul: CI `audit` yeşil.
- **H6.6 Yük + maliyet.** k6 500 eşzamanlı okuma; p95 okuma < 200 ms, yazma < 350 ms (§11). Kabul: rapor + sunucu satırları tuttu.
- **H6.17 İzleme + hata takibi.** Hedef: Grafana + Loki (sunucu izleme) + GlitchTip (hata takibi §3.4). Adımlar: 1. Compose'a log toplama + dashboard (k6 yükü altında). 2. GlitchTip'e istemci + sunucu hata akışı. Kabul: panel açılır, test hatası düşer. Çıktı: H7 provozunun gözlemi.
- **H6.7-koordinasyon.** Herkes payını yazar; ölü link ve güncel-dışı ADR bırakmazsın.

## H7 — Demo

- **H7.1-pay.** Sözleşme ayağı provada sende.
- **H7.3 Kapanış.** §16 kutuları + §18'de 7 imza. Kabul: tüm kutular tikli.

## Risklerin

R8: `contract` kapısı H1.6'dan itibaren kırmızı PR bekletir. R6/R7: H6.6 + `just fmt`. Şema = PR + onayın; sözlü onay yok.
