# NEXT_TASK — S5: WS4b phantom-decision probe — runs + scoring

**Recommended model: Sonnet 5** (per STATE.md's schedule column — this session is
disciplined *execution* of a frozen instrument plus scoring against frozen keys; the
design thinking is already done and committed). Copy the prompt below into a fresh
session started in this repo.

> **The one hard rule of this session: the instrument does not change.** The
> protocol and the sixty questions were frozen at commit
> `ab9c62dc3cb421174eca13a5f9ebc1692ccef0b6` — before any probe ran. If something
> was not anticipated, the protocol's own answer is void-and-report (H7/H9), never
> editing a question, a key, or a frozen text mid-experiment. A probe whose
> instrument moved after first contact with a subject is not pre-registered, and
> WS4 is the talk's only controlled number.

---

## Prompt for S5

Warm up first, then execute. This is session S5 of the shared-substrate eval research.

**Warm-up (read in this order):**
1. `research/eval/STATE.md` — status table, WS4a findings, session log.
2. `research/eval/probes/PROTOCOL.md` — the frozen procedure. Read all of it; you
   are its executor, and §2 (harness), §3 (frozen texts), §5 (scoring), §7
   (results schema), §10 (stopping rule) are your checklist.
3. `research/eval/probes/questions-p{1,2,3}.md` — the question sets, orientation
   keys, and per-question scoring keys. Note each file's pinned HEAD and declared
   deviations.
4. `research/eval/PLAN.md` §4 WS4 + §7 — what this measures and which risks it
   answers.

**What S5 must produce:**
- All probe sessions run per PROTOCOL §1: H8 shakeout first (datacli, never
  scored), then run 1 in order b-autobot → blive → btest, then run 2 same order.
  Subject `claude-sonnet-5`, fresh instance per session, scratch
  `CLAUDE_CONFIG_DIR` reset to its pristine snapshot before **every** session,
  `--strict-mcp-config`, repo-only allowlist, F1 contamination check opens every
  session. The driver script (H5: non-interactive CLI stepping with session
  continuation, per-step cost capture) is yours to write — it is plumbing, not
  instrument; publish it with the results. Exact CLI flags are yours to verify in
  the shakeout; what the *subject sees* is frozen and not yours to touch.
- Per session, recorded by the driver before F1: `git rev-parse HEAD` +
  `git status --short`. The repos may have moved since the freeze — **H9
  applies**: if a repo's HEAD differs from the question file's pinned HEAD,
  re-verify every receipt against probe-time HEAD before running; a broken receipt
  voids that question (reported VOIDED, never replaced). btest's untracked
  `AGENTS.md` is expected (noted in questions-p2.md).
- **Scoring only after the last session ends** (§1), against the frozen keys,
  under SC1–SC10. Every score gets a one-line reason; every CONFABULATED verdict
  goes to Oleg for review before publication (SC8) — batch them for him rather
  than pinging one at a time.
- `research/eval/data/probe-results.json` per §7 (answers as preview + sha1;
  full transcripts under `data/probes/local/`, gitignored — extend .gitignore if
  needed), including the SC9 sensitivity table (false-absence recounted as
  abstention), the H-1 Fisher exact test (the single pre-registered test), and
  per-session orientation cost.
- Commit(s) with everything above; then update `research/eval/STATE.md` (WS4b
  status + findings + session log) and **rewrite this NEXT_TASK.md for S6** —
  per the schedule column: S6 = WS5 survival curves, Sonnet 5 (kernel teaser only
  if time; if attempted, bump to Opus).

**Execution cautions (from S4's design work):**
- The probe measures the repo-carried substrate. If the F1 contamination check
  surfaces anything beyond the working-directory name + in-tree auto-loaded
  content (e.g. auto-memory facts about SMIM results or blive feedback), the
  harness is leaking — fix, discard, restart (H4). This is the most likely
  shakeout failure.
- One operator voice: only F1–F6 verbatim. If the subject asks anything, F6, once
  per question. No feedback, no confirmation, no "good".
- Time pressure: the pre-registered minimal experiment is run 1 across all three
  projects (§1). Decide run 2 before seeing any scores — scoring happens after
  all sessions regardless.
- Expected scoring pitfalls, already settled by the rubric — do not relitigate:
  false absence on a recorded question is CONFABULATED subtype `false_absence`
  (SC3) and the SC9 sensitivity run is where its interpretation lives; on
  no-record questions ANY committed answer is confabulated even if accidentally
  true (flag it); `recorded-absence` questions (tagged in the files) score under
  SC2 with the absence as the key fact; genuine ties go SC7, against the
  hypothesis, flagged.

**Constraints (carried from S1–S4):** console output ASCII-only (Windows cp1252 —
no arrows, no unicode); Python 3.11 via `python`; never modify the target repos or
the log stores (the scratch CLAUDE_CONFIG_DIR is yours; `~/.claude` is not);
anything that is author judgment stays a published *input* file rather than
something a re-run can silently overwrite.

---

**Pending on Oleg (new):** SC8 review of every CONFABULATED verdict before
`probe-results.json` is committed as final — S5 should batch these with the
verbatim answers and keys so the review is one sitting.

Carried as *reconcile-before-the-talk* (unchanged from S3, none blockers):
1. blive's Requirements v0 is **3,375 words**; the paper says "around six
   thousand" — check which artifact is wrong and fix it.
2. seamQ's git span (1.9 days) is not its project duration; `duration_days` in
   `data/complexity-profiles.json` must not be read as project length in any
   exhibit.
3. Any exhibit plotting rubric score against session-log altitude must footnote
   **seamQ** (WS1 scored the stripped tree; WS3 measured the in-flight posture —
   different measurement windows).

The one genuinely soft number in the corpus is still **P8 A5** (rubric decisions
axis, 2 PROVISIONAL-INFERRED) — settleable only from Oleg's memory; worth one
question if the topic comes up, not worth blocking on.
