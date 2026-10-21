# Screen list v1 — locked

Production scope is 23 screens plus the root launch page. New screens require a
PR; route ownership follows `development.md` §1.6 and §6.

| # | Screen | Route | Owner |
|---|---|---|---|
| 1 | Discover / map | `/(tabs)/discover` | P7 |
| 2 | Filter sheet | `FilterSheet` component | P7 |
| 3 | Event detail | `/events/[id]` | P7 |
| 4 | Ticket selection | `/events/[id]/tickets` | P7 |
| 5 | Ticket wallet | `/(tabs)/tickets` | P7 |
| 6 | Club list | `/(tabs)/clubs` | P6 |
| 7 | Club detail | `/clubs/[id]` | P2, P6 |
| 8 | Club chat | `/clubs/[id]/chat` | P5 |
| 9 | Messages (DM list) | `/(tabs)/messages` | P5 |
| 10 | Direct message | `/channels/[id]` | P5 |
| 11 | Media room | `/events/[id]/room`, `/channels/[id]/room` | P5 |
| 12 | Profile | `/(tabs)/profile` | P6 |
| 13 | Login / register | `/login`, `/register` | P6 |
| 14 | Invitation accept | `/invite/[code]` | P2 |
| 15 | Door check-in | `/scanner` | P2, P7 |
| 16 | About / source attribution | `/about` | P7 |
| 17 | Settings | `/settings` | P6 |
| 18 | Notifications | `/notifications` | P5 |
| 19 | Following feed | `/(tabs)/feed` | P2, P7 |
| 20 | Following list | `/settings/following` | P2 |
| 21 | Followers | `/clubs/[id]/followers` | P2 |
| 22 | Create post | `/clubs/[id]/new-post` | P2 |
| 23 | Post comments | `Sheet` component | P2 |

The root launch page (`/`) is a development shortcut, not part of the product
screen count. The list is frozen; changes need P6/P7 approval and a PR.
