# ProjectX (EtkinlikCepte)

> Project name TBD — `ProjectX` is a placeholder, as are `*.projectx.app` addresses.

Android app (APK): nearby events on a map, clubs, tickets with QR, chat, voice/video.
Seven people, seven weeks (H1–H7); week-7 Friday demo runs end to end.

## Quickstart (~10 min)

Prerequisites: `git`, `mise`, `just`, `podman`, `gh`. Tool versions live in
`mise.toml` — install exactly those (`mise install`).

```bash
git clone <repo> && cd EtkinlikCepte
mise trust && mise install   # or: just setup
cp .env.example .env         # never commit .env
just setup                   # venvs + migrate + seed (skips what is not built yet)
just dev                     # podman compose up (postgres, valkey, caddy, martin, livekit, nominatim)
just services                # container watch (oxker if present)
```

Verify: `pg_isready -h localhost` · `curl localhost:3000/health` (martin) ·
`curl localhost:7880` (livekit). `GET /openapi.json` arrives with H1.2.

Daily: `just fmt && just lint && just test`. Full local gate: `just ci`.

## Layout

| Path | What | Owner |
|---|---|---|
| `apps/mobile/` | Tauri 2 + SvelteKit app (H1.12+) | P6, P7 |
| `apps/api/` | FastAPI backend, `uv sync` → `.venv` | P1, P2, P4, P5 |
| `apps/pipeline/` | ETL (Scrapy → dedup → publish) | P3 |
| `packages/ui/` | Design system (shadcn copies + ours) | P6 |
| `packages/api-client/` | Generated from `openapi.json` (`just api-types`), never by hand | P1 |
| `infra/` | Compose + Caddy/Martin/LiveKit/Headscale configs, `docs/ports.md` | P1 |
| `docs/plan/` | `ana-plan.md` (master index) + `p1–p7.md` (same IDs) | all |
| `docs/adr/` | Why expensive decisions went their way | author |

## Docs map

- `development.md` — what + scope decisions (§4 wins ties).
- `AGENTS.md` — working agreement: philosophy, rules, docstring format. Read before first change.
- `docs/plan/ana-plan.md` — who + when (103 tasks, H1–H7).
- `docs/adr/` — ADRs, incl. Node runtime (0011) and deny list (0003 → `deny.txt`).

## Workflow (§6.2)

Trunk-based, branch ≤ 3 days, no direct `main` pushes. PR: single topic,
≤ 400 lines, CI green, one approval; schema/migrations need P1. English
code/commits/docs; user-facing Turkish only in `apps/mobile/src/locales/tr.json`.
New dependency? Check `deny.txt` first — listing needs an ADR.

## Troubleshooting

- **No `mise`:** install it (https://mise.jdx.dev), then `mise install`. System
  node/python versions are irrelevant once mise is active.
- **Podman on macOS/Windows:** init a machine first (`podman machine init`).
- **Port busy (5432/6379/3000/7880):** stop the local service or edit
  `infra/compose.dev.yaml` (localhost bindings live there).
- **`just setup` skips steps:** it skips what is not built yet (H1.2/H1.12) —
  that is expected in week 1, not an error.
- **Playwright browsers:** pip package installs with the pipeline venv;
  `playwright install chromium` runs when JS-render adapters land (H2/H5).
- **Nominatim import:** runs once, takes a while (H1.17, P4).
