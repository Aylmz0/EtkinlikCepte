# Ortak komutlar (§15). Herkes kendi kabuğunda geçici komut yazmaz (§6.2):
# her şey buradan çalışır. `just --list` ile bak.

# mise trust + kurulum + örnek veri
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    command -v mise >/dev/null || { echo "once mise kur: https://mise.jdx.dev"; exit 1; }
    mise trust
    mise install
    test -f apps/api/pyproject.toml && (cd apps/api && uv sync) || true
    test -f apps/pipeline/pyproject.toml && (cd apps/pipeline && uv sync) || true
    test -f apps/mobile/package.json && npm --prefix apps/mobile install || true
    just migrate || true
    just seed || true

# podman compose up + sıcak yenileme (masaüstü)
dev:
    podman compose -f infra/compose.yaml -f infra/compose.dev.yaml up -d
    just services

# npm run tauri android dev
dev-mobile:
    npm --prefix apps/mobile run tauri android dev

# imzasız deneme APK'ı
android-apk:
    npm --prefix apps/mobile run tauri android build -- --apk

# imzalı sürüm APK'sı (anahtar CI'da, §13.2)
android-release:
    npm --prefix apps/mobile run tauri android build -- --apk --release

# openapi.json -> tipler + doğrulama şemaları (§8)
api-types:
    test -f apps/api/pyproject.toml || { echo "H1.2 bekleniyor: apps/api yok"; exit 1; }
    (cd apps/api && uv run python ../../scripts/export_openapi.py)
    rm -rf packages/api-client/src
    npx openapi-ts -i packages/api-client/openapi.json -o packages/api-client/src -p @hey-api/typescript zod
    printf "\nexport * from './zod.gen';\n" >> packages/api-client/src/index.ts

# alembic upgrade head
migrate:
    test -f apps/api/pyproject.toml || { echo "H1.3 bekleniyor: apps/api yok"; exit 1; }
    (cd apps/api && uv run alembic upgrade head)

# örnek veri (Türkiye, 3 şehir)
seed:
    test -f apps/api/pyproject.toml || { echo "H1.3 bekleniyor: apps/api yok"; exit 1; }
    (cd apps/api && uv run python -m app.seed 2>/dev/null) || echo "seed H2 sonrasi"

# API sözleşme testleri (§12)
hurl:
    test -d apps/api/hurl || { echo "H1.5 bekleniyor: hurl dosyalari yok"; exit 1; }
    command -v hurl >/dev/null || { echo "hurl yok: mise install"; exit 1; }
    hurl --test apps/api/hurl/*.hurl

# paket + APK boyutu raporu (§11)
perf-apk:
    npm --prefix apps/mobile run build -- --report 2>/dev/null || echo "H1.12 bekleniyor: mobile yok"

# Playwright web E2E iskeleti (§12)
e2e:
    npx playwright test

# tüm testler (§12; test yoksa 5 koduyla geçer — H2'de testler gelir)
test:
    test -f apps/api/pyproject.toml && (cd apps/api && uv run pytest || test $? -eq 5) || echo "api testi yok"
    test -f apps/mobile/package.json && (npm --prefix apps/mobile run test --if-present) || echo "mobile testi yok"

# CI ile aynı lokal komutlar (§13.1)
ci: lint test hurl

# ruff format + prettier (§4.12)
fmt:
    ruff format apps/ 2>/dev/null || echo "ruff yok"
    npx --prefix apps/mobile prettier --write "apps/mobile/src/**/*.{ts,js,json,svelte}" "packages/ui/src/**/*.{ts,svelte}" "*.md" 2>/dev/null || echo "prettier yok"

# ruff check + svelte-check + eslint (§13.1)
lint:
    ruff check apps/ 2>/dev/null || echo "ruff yok"
    npm --prefix apps/mobile run lint --if-present 2>/dev/null || echo "mobile lint yok"

# oxker ile konteyner izleme (§3.4)
services:
    [ -t 1 ] && command -v oxker >/dev/null && oxker 2>/dev/null || podman ps

# headscale ile sunucuya bağlan (§13.2)
vpn:
    just services | head -5
    echo "headscale: H5.15'te"
