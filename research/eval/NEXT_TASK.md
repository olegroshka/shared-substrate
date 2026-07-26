# NEXT_TASK — S6: WS5 decision survival curves

**Recommended model: Sonnet 5** (per STATE.md's schedule column — WS5(a) is a
scripted git-history measurement in the WS2 house pattern, and the instrument
question is small). **If you attempt the kernel teaser (WS5b), bump to Opus 5**;
PLAN §4 marks it "cut first", and a half-baked κ estimate is worse than none.

> **What S5 leaves you.** WS4b came out **null**, and after Oleg's SC8 review its
> nominal direction reversed: btest 38/38 correct with zero confabulations, blive
> 37/38 with **the corpus's only confabulation**. Fisher p = 1.0. That was the
> talk's one controlled number, so WS5 now carries more weight than the plan
> assumed. Do not respond by making WS5 generous. The corpus has already produced
> two honest negatives (WS3 finding 5, WS4b H-1) and they are the reason the rest
> is believable.
>
> **Two rules from S5 that now bind you.** (1) **Tier A/B evidence:** a claim that
> "we decided X" must rest on an artifact that *states* the decision; a decision
> inferred from a diff, rename or config change may ground a claim about the
> **state** of the code, never about a decision. Two WS4 questions were voided for
> failing this. (2) When ground truth turns out not to hold, **void and report** —
> never edit the key, never replace the question, never regenerate an answer.

---

## Prompt for S6

Warm up first, then execute. This is session S6 of the shared-substrate eval research.

**Warm-up (read in this order):**
1. `research/eval/STATE.md` — status table, WS4b findings, session log.
2. `research/eval/PLAN.md` §4 WS5 + §7 (confounds ledger).
3. `research/eval/scripts/git_miner.py` and `scripts/corpus_common.py` — WS5's
   miner must reuse `corpus_common`'s single definition of a source file and its
   vendored-path exclusions, not restate them.
4. `research/eval/data/probe-results.json` `_meta.harness_deviations` +
   `data/probes/scores.json` — five minutes, so you inherit what WS4b learned
   about publishing a negative and about absence checks that turn out false.

**What S6 must produce:**
- `scripts/survival.py` → `data/survival.json`: for P1 (blive), the fraction of
  ADRs / KB entries / frozen artifacts surviving *k* subsequent sessions without
  silent reversal, contrasted with decision-reversal archaeology in P2 (btest)
  commit messages. Stdlib-only, read-only git, path-parameterised — §5-portable
  like every other script in this repo.
- **Define "silent reversal" before you write the measurement, and freeze the
  definition in the script docstring.** blive's substrate is append-only with
  explicit supersedes, so a *declared* reversal (ADR-N superseded by ADR-M) is
  the discipline working, not a failure; only an undeclared contradiction counts.
  Getting this boundary wrong is the whole workstream.
- Hand-verify at least two computed numbers against independent shell counts
  before the sweep, and record them in `_meta.verification` — S2 and S3 each
  caught real bugs this way, and S5's F5 bug was caught by exactly that reflex.
- Findings + caveats into `research/eval/STATE.md`, and **rewrite this
  NEXT_TASK.md for S7** — per the schedule column: S7 = WS6 archaeology, Opus 5,
  narrative judgment.

**Execution cautions:**
- blive's ADR corpus is large (ADR-001..053) and its `DECISIONS.md` is
  append-only, so "survival" is cheap to compute and easy to overstate. The
  interesting number is not how many ADRs survive — nearly all will — but
  whether any decision was *contradicted in code* without the record moving.
  That requires reading, not counting; budget for it.
- btest has no ADR system at all, so its arm of this comparison is
  commit-message archaeology against a different substrate type. Say so in the
  output rather than forcing a shared denominator — WS2 finding 8's `n/a` flag
  pattern is the precedent.
- seamQ, harp and smim are boundary cases here as elsewhere; if you include
  them, carry their known measurement-window caveats (STATE.md WS3 finding 6).
- WS4b found a real doc/code divergence in blive that WS5 should not re-discover
  by accident: OQ-035 claims a three-order-type surface where `types.py` has
  seven plus an OPG time-in-force. That is a *recorded* decision contradicted by
  code with the record unmoved — i.e. exactly the shape WS5 is looking for, and
  a free first data point.

**Constraints (carried from S1–S5):** console output ASCII-only (Windows cp1252 —
no arrows, no unicode); Python 3.11 via `python`; never modify the corpus repos;
anything that is author judgment stays a published *input* file rather than
something a re-run can silently overwrite.

---

**Nothing is pending on Oleg.** The SC8 review closed in S5: three of twenty
question slots are voided (P1-Q07, P3-Q01, P2-Q07 — each in both runs), the one
surviving CONFABULATED verdict (blive-run2 P1-Q20) is reviewed and agreed with
`accidentally_true` explicitly false, and the two SC7 tie-breaks on b-autobot
P3-Q05 stand. Details in `data/probes/scores.json` under `voided_h9` and
`declared_protocol_extension`.

Carried as *reconcile-before-the-talk* (unchanged, none blockers):
1. blive's Requirements v0 is **3,375 words**; the paper says "around six
   thousand" — check which artifact is wrong and fix it.
2. seamQ's git span (1.9 days) is not its project duration; `duration_days` in
   `data/complexity-profiles.json` must not be read as project length.
3. Any exhibit plotting rubric score against session-log altitude must footnote
   **seamQ** (WS1 scored the stripped tree; WS3 measured the in-flight posture).

**New from S5, and all three matter for how the talk is framed:**
1. **WS4b finding 10** — btest's `CLAUDE.md` is a 212-line agent-instruction file,
   so PLAN §2's "flat" arm is flat in *decision records*, not in agent
   instructions. Every exhibit contrasting "substrated" against "unsubstrated"
   needs that qualifier, and the WS4b null may be explained by it entirely.
2. **WS4b finding 9 — DEC-N2 is 0 for 3.** No project yielded a decision that
   lived only in conversation: b-autobot's slot was declared unfillable at freeze,
   blive's turned out to be in the repo, btest's turned out not to be a decision.
   This cuts *for* the thesis in a way the confabulation count does not, but it
   rests on three negative constructions — state it as "we could not find one",
   never as "they do not exist".
3. **WS4b finding 7, a WS6 lead you will want** — blive's `OPEN_QUESTIONS.md`
   OQ-033 records an "Operator decision (2026-06-06)" against an option the
   operator says was never considered. The readiness audit formalised a standing
   default into a dated decision. Append-only discipline can *manufacture*
   decisions, not just preserve them, and that is the most interesting failure
   mode the probe surfaced.

The one genuinely soft number in the corpus is still **P8 A5** (rubric decisions
axis, 2 PROVISIONAL-INFERRED) — settleable only from Oleg's memory; worth one
question if the topic comes up, not worth blocking on.
