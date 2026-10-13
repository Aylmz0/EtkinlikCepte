# EtkinlikCepte — working agreement

The philosophy and the rules. Nothing here describes the current code: if a line
would become false because someone shipped a feature or renamed a function, it
does not belong here. Versions, inventories, screens, endpoints, and schedules
live in `development.md` and `docs/plan/`, both linked at the bottom.

Read this before your first change. For what the product is, read `development.md`
§1–§2 (Product and Architecture) first.

---

## The one thing

**The contract comes first. Seven people working in parallel lose their time to
contract drift, not to typing.**

Everything else here is downstream of that sentence. The API contract (`/v1`)
and the database schema are locked; they change by PR, never by handshake
(§2.1 Principles, §8.1 Contract rules). When two designs disagree about where a rule lives, the contract
wins. When a shortcut would move faster this week by bending the schema, it
loses — the six other people pay for it next week.

The date serves the same sentence: the week-7 Friday demo runs end to end. The
plan exists to protect that date, not the other way round.

---

## How to decide

Judgement calls, not checker rules. They are here because the temptation runs
the other way every time.

### Simplicity is the default (KISS)

Complexity is a maintenance tax paid forever; a deadline is paid once. When in
doubt, take the boring option.

| Prefer | Over |
|--------|------|
| A plain query in `repos/` | A clever abstraction over queries nobody asked for |
| One router per §8 API contract group | A generic CRUD machine with configuration |
| A named constant | An inline literal with a comment beside it |
| Direct access and a plain `if` | A builder, a DSL, or a macro layer |
| Log it and continue | A deep error hierarchy for a condition you can survive |

The test: **can someone read this and know exactly what it does, without opening
another file?** If not, it is too clever. Break it up.

The counter-rule matters just as much: **simplicity is not an excuse for sloppy
work.** Simple *and* correct. A short function with a wrong branch is still wrong.

### DRY, but not at any cost

The rule is not "never repeat yourself." It is: *give the shared thing a name
when the same logic appears three or more times, or when two copies have
already drifted apart.*

Extracting too early is a real cost. A helper that takes six parameters to
avoid a second call site is worse than the duplication. Accept the linter's
complaint there, with a reason.

The failure mode to watch for is drift, not repetition. When duplicated logic
disagrees, that is a latent bug and the extraction was overdue. Update every
site or extract a helper; updating some of them is how a fix lands on one code
path and misses another.

**Understand the duplication before you remove it.** The UI language is small
and closed on purpose (`tokens.css`, 13 custom components in three layers) —
extend it deliberately, once, or reuse what is there.

### Boring technology

Use the thing already proven that you do not have to maintain. Integrate; do
not reimplement. The stack choices went through ADRs, and refusals live in
`deny.txt` (ADR-0003) — a dependency on that list needs an ADR to come back,
and CI enforces it.

The exception is a real one: a dependency whose cost shows up in the §11 Performance targets
budget (memory, APK size, response time) is a reason to write your own. Measure
first.

### Coherence — a new thing must belong

A feature can be tested, documented, and still be wrong, because it looks
bolted on. Two checks before it is done: does it reuse the existing shapes,
names, and Turkish copy conventions (`locales/tr.json`, never inline Turkish)?
And does a tuning value live where it belongs — a global rule or a per-place
property (ranking weights live in the `ranking_weights` table, not in code)?

---

## How to write it

### Docstrings and comments

The format is mechanical; what follows is the judgement the format cannot carry.

- **Python:** Google-style docstrings. Module docstring on every file (what the
  module is for, once). `Args:` / `Returns:` / `Raises:` on public functions.
- **TypeScript:** JSDoc on every exported function. Same contract idea.
- **Svelte:** header comment on every component — props in, events out.
- **Three levels, not interchangeable.** Module header states purpose. Doc
  comment states the public contract for a caller. Plain comment records a
  local decision for a reader. Promoting a local note into a doc comment bloats
  the reference; dropping a contract into a body loses it.

**A comment earns its place by explaining a why the code cannot.**

| Write a comment for | Leave the code to say |
|---|---|
| A tuned number and the reasoning behind it | What a line obviously does |
| A constraint a reader would otherwise violate | Restating the signature |
| An ordering requirement that is not obvious | Narrating a loop body |
| A bug that was fixed, and the trap behind it | A todo with no owner |
| Why the obvious approach was rejected | Your own name in a comment |

**Write for the reader who arrives in six months with no memory of writing it.**
A concrete example beats an abstract description. Name where the decision came
from.

**A doc comment is a promise about behaviour.** Change what a function does and
the doc is now a lie. Fixing it is part of the change, not a follow-up.

### Documentation is part of the change

A public item without a doc comment is unfinished work, like a failing test.
Write it in the same commit. An ADR for a decision goes with the PR that takes
it — `docs/adr/` that lags the code is worse than none, because people trust it.

### Naming and constants

Names carry intent, comments carry why. If a name needs a comment to be
understood, rename it instead. A literal in logic is a constant waiting to be
named — one place to tune it, one place to see it, greppable. Guard clauses
over nesting. **Fail loudly in development, gently in production:** raise with
context for a broken invariant; log and continue for a survivable condition. A
bare `except: pass` is never acceptable.

### Language

Code, commits, documents, and PR text are English. Always. The app UI is
Turkish first, English second: every user-facing string lives in
`locales/tr.json` (primary) with a complete `locales/en.json` beside it — no
hardcoded UI text, no Turkish or English in identifiers (§6.2 Working rules, §16 Definition of done). A screen
is not done until it renders in both locales.

---

## What does not change

Hard invariants. A change that breaks one needs a reason written down next to it.

- **`/v1` is stable.** A backward-incompatible change is a major version and
  needs P1 approval (§8.1 Contract rules).
- **Money is integer minor units + `TRY`, never float. Time is UTC ISO-8601.
  Errors are RFC 9457. Write paths for tickets and messages carry
  `Idempotency-Key` (§8.1 Contract rules).**
- **Offline first.** The discovery list and owned tickets open without a
  network. A ticket QR is always readable (§1.5 User view).
- **`src-tauri/` belongs to P6 alone; Rust stays under 200 lines** (§4.4 Rust surface).
- **Media lives in the database (BYTEA), referenced by `*_media_id`, never by
  path or URL** (§4.9 Media storage).
- **Scope holds for the seven weeks:** no real payments (manual approval), no
  closed-app notifications, no phone screen-share, no video upload (§1.3 Non-goals).
- **Versions live in `mise.toml` only** (§4.7 Version pinning). Never repeat one in a Dockerfile,
  a README, or a commit subject.

---

## Working agreement

### The loop

1. **Understand** — read `development.md`, your `docs/plan/pN-*.md` week, and
   the surrounding code. Match what is there; areas are frozen (§6 Team).
2. **Implement** — inside your own area. Another area's code gets a question,
   not a commit.
3. **Document** — the doc comment and, if a decision moved, the ADR. Same commit.
4. **Test** — new behaviour has a test, or is verified by hand with the reason
   stated (§12 Test strategy, §16 Definition of done).
5. **Verify** — `just fmt && just lint && just test`, and the OpenAPI
   regenerate-diff is empty (§13.1 CI gates, §16 Definition of done).
6. **Commit** — English, trunk-based, to the rules below.

### Which document owns what

| Layer | What it is | Who maintains it |
|---|---|---|
| `development.md` | What the product is + scope decisions (§4 Scope decisions) | The team, Sprint 0 signature (§18 Sign-off) |
| `docs/plan/ana-plan.md` | General orchestration + master task index (`H<week>.<n>`) | Week-1 lead sets it; weekly leads amend by handover note |
| `docs/plan/p1–p7.md` | Step-by-step per person, same IDs as the index | Each owner, in their frozen area |
| `docs/adr/` | Why an expensive-to-reverse decision went its way | The author, with the deciding PR |
| Doc comments + `openapi.json` | The API reference | You, in the same commit |
| Commit log | What happened and why the diff does not show | — |

Plan logic in short: the index is the single source of task truth; personal
files carry the how. IDs match on both sides. Leadership rotates weekly
(H1 P1 → H7 P7); P1's technical authority (contract, schema, migrations) is
permanent. Buddy pairs: P1-P3, P2-P5, P4-P6.

### Area boundaries

Areas are frozen (§6 Team, `docs/plan/`). You work inside your own; another area's
code gets a question, never a commit — not even a "trivial" fix. The reasons
compound: the owner holds context you do not, parallel branches collide, and
a drive-by edit quietly becomes your responsibility when it breaks.

- **Read anywhere, write in your area.** Exploring another area to understand
  an interface is expected. Changing it is not.
- **Blocked by another area?** Ask the owner — buddy pairs first. If they are
  unavailable, record it in the handover note and take your next independent
  task. Do not route around them.
- **Shared seams have owners too.** The contract (`/v1`), the schema, and
  `packages/api-client` belong to P1; `packages/ui` to P6. Propose changes to
  shared code by PR with the owner reviewing (CODEOWNERS assigns them); do not
  widen a shared helper to fit one caller.
- **No drive-by refactors.** A wrong name or a duplicated block in someone
  else's area is their call to schedule, not yours to fix in passing. Leave it
  as a review comment and move on.

### Commits

Locked standard, set by week-1 lead decision.

```
<type>(<scope>): <imperative summary>
```

Type required, scope optional, summary imperative, lowercase. Types: `feat`,
`fix`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, and `perf` only
with a measurement. The body is for the *why*, when the diff does not make it
obvious. **No authorship trailers, from anyone** — no co-author lines, no tool
names. Trunk-based: every change starts on a fresh branch cut from `main` —
never commit straight to `main`. Nothing lands without a PR: CI green plus one
approval from the area reviewer; `main` and `release/*` are protected, so an
unreviewed merge is impossible, not just discouraged. Branch life ≤ 3 days, PR
single-topic ≤ 400 lines; schema/migration changes need P1 (§6.2 Working rules).

### Definition of done

The §16 Definition of done checklist — all of it, on every change. It is referenced here, not
copied, so it cannot drift from the source.

---

## Where the detail lives

This file stops at philosophy and rules. Everything below ages with the code
and lives elsewhere.

| For | Read |
|---|---|
| What the product does and does not do | `development.md` §1 Product |
| Stack, versions, repo layout | `development.md` §3 Stack, §5 Repo layout (`mise.toml` wins ties) |
| Who does what, when | `docs/plan/ana-plan.md` + your `docs/plan/pN-*.md` |
| Why a hard decision went its way | `docs/adr/` |
| What any function promises | Its doc comment |
| Tables, endpoints, error rules | `development.md` §7 Data model, §8 API contract, §8.1 Contract rules |
| Targets and how they are measured | `development.md` §11 Performance targets, §12 Test strategy |
| CI gates and deploy | `development.md` §13 Server and CI, or `justfile` |
| What a past change was and why | The commit log |
