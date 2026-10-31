# H2.21 design QA — checklist

Reviewed on 2026-10-27 against `packages/ui` and the 23-screen list.

## Component checks

- [x] Button/Card use the shared `cn` utility and token classes.
- [x] `clickOutside` action removes its listener on destroy.
- [x] Calendar grid exposes button roles, labels and keyboard focus.
- [x] No component in `packages/ui` performs network, auth or route work.
- [x] Focus ring is visible on interactive elements.
- [x] 44px minimum touch target is used by primary actions.
- [x] Dark mode is class-based and uses the same semantic tokens.
- [x] Turkish primary / English secondary strings live in `tr.json` and `en.json`.

## Screen checks

- [x] Login/register: labels, autocomplete, required fields, error line.
- [x] Discover/filter: map/list states and empty filter state.
- [x] Event/club detail: loading and missing-data placeholders.
- [x] Tickets: QR/offline state has a visible badge.
- [x] Messages/chat: composer and unread indicators have labels.
- [x] Settings: language/theme/permission rows have accessible names.

## Mock data

The UI mock data lives in `apps/mobile/src/lib/*.svelte.ts` and the route files:
three cities, clubs with roles, events with dates/prices, tickets and chat
fixtures. It is intentionally local: H3 replaces it with API responses.

## Findings

No blocking accessibility issue found in the shared primitives. The remaining
work is visual polish on individual screens and real-device QR/location tests
(H4/H6), not a component contract change.
