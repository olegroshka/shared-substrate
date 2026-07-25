# NEXT_TASK — S3: WS3 session-log analysis (operator altitude + retransmission tax)

**Recommended model: Opus 5** (per STATE.md's schedule column — the altitude taxonomy is
judgment-heavy and is the talk's closing exhibit). Copy the prompt below into a fresh
session started in this repo.

---

## Prompt for S3

Warm up first, then execute. This is session S3 of the shared-substrate eval research.

**Warm-up (read in this order, ~5 min):**
1. `research/eval/STATE.md` — status, WS0/WS1/WS2/WS-X findings, open questions.
2. `research/eval/PLAN.md` §4 WS3 — the spec (three analyses: altitude, warm-up
   fraction, volume-vs-yield). Follow it exactly, including the labelled-sample
   agreement requirement.
3. `research/eval/data/evidence-map.json` — what logs exist per project, and the
   coverage gaps you must not paper over.
4. Skim `research/eval/scripts/corpus_common.py` — reuse its git/path helpers rather
   than re-deriving them; add anything log-shaped to it if both scripts need it.

**Evidence sources (all local, all read-only):**
- Claude Code full transcripts: `~/.claude/projects/<munged-path>/*.jsonl` — two-sided,
  token-accounted, but retention-trimmed to btest (4 sessions), datacli (2),
  shared-substrate (3). `isSidechain: true` marks subagent traffic — separate it from
  real human turns before classifying anything.
- Claude Code global history: `~/.claude/history.jsonl` — **every user prompt since
  2026-03-03**, with project, sessionId, timestamp. Human-side turns for all corpus
  projects; this is what makes altitude analysis corpus-wide (WS0 finding 2).
- Copilot JetBrains store: `~/.copilot/jb/<uuid>/partition-N.jsonl` — two-sided,
  Mar 20–May 31, no token fields (use bytes as the volume proxy).

**Corpus paths (P1–P7):** P1 blive · P2 btest · P3 b-autobot (`IdeaProjects/`) ·
P4 datacli · P5 smim · P6 harp · P7 seamQ — all under `C:\Users\olegr\PycharmProjects\`
except P3.

**Task A — `research/eval/scripts/log_miner.py`.** Stdlib-only, path-parameterised,
read-only. Parse all three formats into one session schema (project, start/end, turns,
tokens where they exist, human turns verbatim) → `research/eval/data/session-metrics/`.
Attribution by folder has known bleed (WS0: btest's first history entry is a b-autobot
bootstrap prompt) — attribute by content where it matters and report how many turns
you re-attributed.

**Task B — the altitude classifier (WS3a; this is the judgment work, not the scripting).**
Classify each human turn into: intent/goal declaration · decision/trade-off resolution ·
design/contract shaping · mechanical steering. **Hand-label a sample first** (~100 turns,
stratified across projects and eras), freeze the taxonomy and its decision rules in
`research/eval/rubric/ALTITUDE.md`, then apply it and **report agreement between your
hand labels and the automated pass** — PLAN §4 calls turn classification the crux, so an
unreported agreement number makes the exhibit worthless. Compare distributions across
substrate postures and along each project's lifetime; btest spans both eras, so its
within-project P2 chronology is the strongest available signal (as with WS2's ID curve).

**Task C — warm-up fraction / retransmission tax (WS3b).** Classify each session's early
turns as context reconstruction vs new work; compare across postures. The prediction to
test honestly: substrated projects pay a *bounded* warm-up cost, flat projects an
unbounded recurring one.

**Task D — volume vs durable yield (WS3c, supporting).** Only if A–C are solid; it is
first in the cut order after WS5's kernel.

**Constraints (learned in S1–S2):** console output ASCII-only (Windows cp1252 — no
arrows, no unicode); Python 3.11 via `python`; never modify the target repos or the log
stores. Coverage gaps (blive's 119 prompts and 2 Copilot sessions; nothing for smim/harp
/seamQ beyond history.jsonl) are **findings to report**, not problems to work around —
session-based claims about blive stay modest, exactly as WS0 recorded.

**Sanity (S2 earned this the hard way — three of five hand-checks caught real bugs):**
hand-verify at least two extracted quantities against independent counts on one small
log set *before* the full pass, and record the verification in the output JSON's `_meta`
header, as `git_miner.py` and `complexity_profile.py` do.

**Deposit before ending:** update `research/eval/STATE.md` (WS3 status + 3–6 line
findings summary + session-log entry), then **rewrite this NEXT_TASK.md** for S4 — the
next session and model come from the schedule column in STATE.md's status table
(S4 = WS4a probe pre-registration, Fable 5), which is the source of truth for the
session/model plan. Note for S4: WS4a's pre-registration commit must land **before** any
probe is run.

---

Oleg's parallel inputs (any time): review DRAFT rubric scores + fill P8 blanks
(`data/rubric-scores.json`); fill the three `declared_qualitative` ratings per project in
`data/complexity-profiles.json` (0–3 each, criteria are inline in the file — they are
author judgment by design and no script will ever compute them); answer STATE.md OQ-1
(btest Dec–Feb tooling — WS2 now shows that era at 0% ID-tagging with free-text commit
subjects, so what built it is a live question) and OQ-2 (claude.ai exports for blive's
lost sessions — these would directly widen WS3's thinnest coverage).
