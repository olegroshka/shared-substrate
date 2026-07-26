# NEXT_TASK — S7: WS6 drift archaeology (the war stories)

**Recommended model: Opus 5** (per STATE.md's schedule column). WS6 is the one
workstream with no script and no denominator: it is narrative judgment over a
corpus that six prior sessions have already instrumented. The risk here is not a
measurement bug, it is *a good story the receipts do not support*.

> **What S6 leaves you.** WS5(a) came out **null on its headline** — zero blive
> ADRs silently reversed, S(k)=1.000 at every k — and that is the corpus's fourth
> honest negative (WS3 finding 5, WS4b H-1, WS5 finding 4, WS5's null). The
> findings that matter are elsewhere, and two of them are WS6's raw material:
>
> 1. **Records wrong on the day they were written.** blive's OQ-035 and btest's
>    "~2600 LOC" are both birth defects, not drift. Neither substrate posture has
>    an instrument that checks a factual claim at deposit time. That is a
>    *missing discipline element* — exactly WS6's question shape.
> 2. **The Python 3.12 pair (2026-06-05)** is the cleanest control in the whole
>    corpus and it **reframes the thesis**: btest recorded *why* — well, in a
>    1,025-char commit body — and what it lacks is **addressability**, not
>    reasoning. Do not write a war story whose moral is "the flat project didn't
>    write it down." WS5 finding 3 and WS4b's near-perfect recorded-fact retrieval
>    both say that is false.
>
> **Three rules that now bind you.** (1) **Tier A/B evidence** (S5): a claim that
> "we decided X" must rest on an artifact that *states* the decision; a decision
> inferred from a diff, rename or config change may ground a claim about the
> **state** of the code, never about a decision. (2) **Void and report** — when a
> story's ground truth turns out not to hold, publish the failure, never repair
> the story. (3) **Declared is not failed** (S6): blive's substrate is append-only
> with explicit supersedes, so a *declared* reversal, a frozen retro, and a
> registered-MISSING artefact are all the discipline **working**. A war story that
> treats one of those as a scar is a category error — and S6 nearly made it twice.

---

## Prompt for S7

Warm up first, then execute. This is session S7 of the shared-substrate eval research.

**Warm-up (read in this order):**
0. `research/eval/METHODS.md` — new in S6. The whole method in one read: corpus,
   evidence channels, the five frozen instruments, what each script computes, and
   the eleven governing rules. If you read one file before touching anything,
   read this; §6 rules 4, 5 and 6 are the ones a war story can violate.
1. `research/eval/STATE.md` — status table, **WS5 findings**, session log.
2. `research/eval/ASSESSMENT.md` — where the argument actually stands, revised at
   the end of S6. **Read §5.1 (the fragility ledger) before you choose a single
   war story.** It splits the corpus into ~5 findings resting on hundreds of
   observations and ~7 resting on one event, and it binds you: nothing fragile
   leads a section, and no two fragile findings are aggregated to imply a rate.
   A war story is a *fragile* finding by construction — that is fine, as long as
   it is placed as colour after a robust number, never as the load-bearing claim.
3. **`research/eval/STATE.md` WS0-bis findings + PLAN §7 confound 6** — the
   artefact-survivorship audit. This is the biggest change to the eval since S1
   and it rewrites your vocabulary: **btest was not "flat", it was "ephemeral"**.
   At least 26 btest working artefacts existed and never reached git, against
   blive's zero. Any war story about btest "not writing it down" is now wrong on
   the evidence — the honest version is that btest wrote it down and it did not
   survive, or survived without being addressable.
4. `research/eval/PLAN.md` §4 WS6 + §7 (confounds ledger) + §9 module M-B.
5. `research/eval/data/survival-audit.json` — ten findings with receipts, plus
   `checks_that_held` (17 entries). **The checks that held are as much WS6
   material as the findings** — they are where the discipline demonstrably worked.
6. Ten minutes in `data/probe-results.json` `_meta` and `data/probes/scores.json`
   `voided_h9`, so you inherit what WS4b learned about publishing a negative.

**What S7 must produce:**
- `research/eval/report/war-stories.md` (the `report/` directory does not exist
  yet — create it) — **3–4 stories with receipts**: commits, artifact diffs,
  file:line, session-log sha1s. PLAN §4 names the spine: pair every element in
  blive's `docs/method/Amendments_Log.md` and its five retros (`docs/retros/`)
  with the concrete incident that forced it — the chaos drill → KB-7; the
  leverage trilemma → ADR-052 / OQ-032; the `AccountSnapshot.equity` bug → DD-1
  v0.3. Then the mirror hunt in btest: incidents with **no capture mechanism**,
  left as scar tissue.
- Each story needs the same four beats: **the incident** (with a receipt) → **what
  it cost** → **the discipline element that exists because of it** (or the absence
  where none was created) → **what it generalises to**. A story that cannot fill
  beat three is an anecdote — cut it, or say plainly that it is one.
- **A story may be a negative, and the best candidate is one.** WS4b finding 7:
  blive's readiness audit formalised a standing default into a dated "Operator
  decision (2026-06-06)" against an option the operator says was never considered
  (OQ-033) — in the **same commit** (`febc4e3`) that produced OQ-035's false claim
  about the order-type surface. One session, two defects, in the project that
  scores 22/24. Append-only discipline can manufacture decisions as well as
  preserve them. That is the most interesting thing the corpus contains; it
  belongs in the talk, not buried.
- Findings + caveats into `research/eval/STATE.md`, and **rewrite this
  NEXT_TASK.md for S8** — per the schedule column: S8 = report assembly, Fable 5,
  cross-workstream synthesis into `report/`.

**Leads already deposited — do not re-derive these:**
- **WS0:** `~/.claude/projects/*/memory/` files are evidence. blive's includes
  `feedback_warmup_discipline.md` — the agent's own persistent memory of being
  *taught* the warm-up protocol — plus `feedback_surface_full_option_space.md`
  and `feedback_work_on_main.md`.
- **WS4a finding 5 — conversation-only receipts**, sha1s in
  `data/session-metrics/turns-classified.json`: btest no-skips policy
  `a878c86c0eeb`; blive work-on-main `01bab5bd50f0` / `1d771f968cb2`; b-autobot
  gridbot-name rejection `b64900916546`; btest SMIM-extraction rationale
  `e66460c50699` / `3a39b4ff5c61`. **Carry the S5 caveat:** btest's no-skips turn
  was adjudicated a *situational instruction*, not a policy adoption — P2-Q07 was
  voided on exactly that. Re-read the void before building on it.
- **WS1 finding 6:** b-autobot's stale `CLAUDE.md` references to deleted plan docs
  (reference rot in vivo); harp §9.1's "conversation-only items" context-loss
  ledger; smim's squashed single-commit history.
- **WS2 finding 5:** b-autobot committed 9,248 vendored `node_modules` files — a
  substrate-hygiene story with a receipt.
- **WS5 finding 6:** blive's own link rot — one malformed anchor copied into 14
  records, because citing is done by copy. Append-only preserves errors with the
  same fidelity it preserves decisions.
- **WS5 finding 5:** blive keeps *two* ADR status registers. The outer one
  (`CONTEXT_INVENTORY.md`) is correct; the inner one (`DECISIONS.md`'s own index
  table) is stale on ADR-031/032 and omits ADR-040/041 entirely.
- **WS5 finding 7:** supersession propagates forward to the superseding record and
  back to the superseded one, but never to the N records that *cite* the
  superseded one (ADR-039 still says "ADR-021 … not SUPERSEDED"). Deliberately not
  counted as a defect; it is the mechanism that explains why the register on top
  of the ADR file has to exist.

**Execution cautions:**
- **The corpus's credibility is its negatives** — four of them now. WS6 is the
  workstream most able to spend that credibility, because a war story is
  *chosen* rather than measured. Pick stories that survive an unsympathetic
  reading, and **name the one you cut and why**.
- btest's `CLAUDE.md` is a **212-line agent-instruction file** (WS4b finding 10).
  Every "unsubstrated" framing needs that qualifier: btest is flat in *decision
  records*, not in agent instructions.
- seamQ, harp and smim remain boundary cases; if a story touches them, carry their
  measurement-window caveats (STATE.md WS3 finding 6; WS0 coverage boundaries).
- WS6 is prose, not data, but `report/war-stories.md` still lives in the §5
  portable tree. Keep **P8 out of it entirely** — the work-side case study is §5's
  round-trip, not this file.

**Constraints (carried from S1–S6):** console output ASCII-only (Windows cp1252 —
no arrows, no unicode); Python 3.11 via `python`; never modify the corpus repos;
anything that is author judgment stays a published *input* file rather than
something a re-run can silently overwrite.

---

**Nothing is pending on Oleg.** WS5 raised no new questions for him and closed
none that were open.

Carried as *reconcile-before-the-talk* (none are blockers):
1. blive's Requirements v0 is **3,375 words**; the paper says "around six
   thousand" — check which artifact is wrong and fix it.
2. seamQ's git span (1.9 days) is not its project duration; `duration_days` in
   `data/complexity-profiles.json` must not be read as project length.
3. Any exhibit plotting rubric score against session-log altitude must footnote
   **seamQ** (WS1 scored the stripped tree; WS3 measured the in-flight posture).
4. **New from S6 —** any survival-curve exhibit must carry its `at_risk`
   denominator on the axis. blive's k=12 point rests on **26** records, not 53;
   "97% of ADRs survive 12 sessions" without that denominator is the easiest lie
   this workstream could tell.
5. **New from S6 —** the two WS5 arms are not a shared denominator. btest has no
   decision records; its arm is instruction rules plus commit prose. Any chart
   putting them side by side needs the `n/a` flag, not a zero.
6. **New from S6 —** the reversal-narration gap (blive 11.9 vs btest 0.24 per 100
   commits, hand-adjudicated) must be shown with the prose-volume confound beside
   it: blive writes 362.5 words of commit prose per commit, btest 62.7, and on the
   per-10k-words normalisation the automated gap is 2.1×, not 50×.

**From S5, still shaping the framing:** DEC-N2 is **0 for 3** — no project yielded
a decision that lived only in conversation. State it as "we could not find one",
never as "they do not exist".

The one genuinely soft number in the corpus is still **P8 A5** (rubric decisions
axis, 2 PROVISIONAL-INFERRED) — settleable only from Oleg's memory; worth one
question if the topic comes up, not worth blocking on.
