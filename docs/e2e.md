# E2E flow list

## Web — Playwright (8)

1. Register → login → event → ticket
2. Discover → event detail
3. Club → create post → follower sees it
4. Club chat send/receive
5. Direct message
6. Invitation link → redeem
7. Door check-in with QR
8. Offline ticket wallet opens without network

Skeleton lives in `e2e/web/`; scenarios are filled in H4.13 and H6.2.

## Phone — adb + UI Automator (3)

1. Location permission flow
2. QR scan at the door
3. Offline ticket wallet with airplane mode

Playwright does not run inside the Android WebView; these three are device
tests by design (§12).
