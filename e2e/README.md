# Web E2E skeleton

`npx playwright test` runs the runner smoke test and reports the eight web
flows as skipped until H4.13/H6.2 fill them in.

The eight web flows: auth→ticket, discover→detail, club→post, chat, DM,
invitation, check-in, offline ticket.

Phone-only flows (adb + UI Automator, not Playwright): location permission,
QR check-in, offline ticket wallet. See `docs/e2e.md`.
