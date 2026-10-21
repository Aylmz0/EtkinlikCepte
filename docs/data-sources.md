# Data sources v1

Every source is disabled until its Terms of Service and `robots.txt` review is
recorded here. The adapter never bypasses a block; a failed check means the
source is not collected.

| Name | Adapter | Entry point | Terms checked | Status | Rate limit |
|---|---|---|---|---|---|
| `etkinlik_io_istanbul` | `rss` | `https://etkinlik.io/rss/sorgu` (city filter in `source_configs.config`) | 2026-10-21: public RSS service, attribution required | candidate | 0.5 rps |
| `etkinlik_io_ankara` | `rss` | `https://etkinlik.io/rss/sorgu` (city filter in `source_configs.config`) | 2026-10-21: public RSS service, attribution required | candidate | 0.5 rps |
| `kultur_jsonld` | `jsonld` | To be selected by P3; `schema.org/Event` required | pending | disabled | 0.5 rps |

Rules:

- A source PR adds a row here with the review date, URL, adapter and rate limit.
- `enabled=false` is the default in `source_configs`; P3 flips it only after the
  review is recorded.
- Two independent sources must cover every information type (§4.3).
- Raw rows land in `source_events`; nothing is shown to users before
  normalization and dedup.
