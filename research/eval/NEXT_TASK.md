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
  Mar 20–May 31, no token fields (use bytes as the volume proxy). **Confirmed in S2 to be
  the only Copilot store on the machine** (OQ-3 closed): b-autobot's Mar 5–11 sprint
  predates it, so those logs are lost, not mislaid — do not go hunting again.
- **claude.ai artifacts in `~/Downloads` (found S2, OQ-2).** No conversation exports exist,
  but three authored artifacts survive and are evidence: `ib_algo_engine_requirements_v0.md`
  (2026-04-26, blive's first commit day — the paper's "first artefact deposited to the
  substrate"), and `HANDOFF_to_new_chat_v2.md` + `KICKOFF_PROMPT_v2.md` (2026-04-30,
  **seamQ**). Read the kickoff early: *"The prior version of this prompt assumed
  `/home/claude/` would persist across chats. It doesn't."* That is a retransmission-tax
  artifact in raw form and belongs in WS3(b), not just WS6.
- **btest's Dec 2025–Feb 2026 era has no session log by construction** (OQ-1 closed in S2):
  it was PyCharm 2025.2 + JetBrains AI Assistant on a metered quota, a surface that keeps
  no recoverable transcript. Treat it as the corpus's **unsubstrated baseline**, evidenced
  by commit prose (49 mean chars vs 585 from March) rather than by turns.

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

**Nothing is pending on Oleg.** As of S2 the rubric is reviewed (v1.1), the 21 declared
complexity ratings are set (`data/qualitative-ratings.json`), and all three open questions
are closed. Two items are carried as *reconcile-before-the-talk*, not blockers:

1. blive's Requirements v0 is **3,375 words**; the paper says "around six thousand". Either
   the document grew before its v0.2 pass or the paper rounds generously — check which, and
   fix whichever artifact is wrong.
2. seamQ's claude.ai design work predates its first commit by over two weeks, so its **git
   span (1.9 days) is not its project duration**. `duration_days` in
   `data/complexity-profiles.json` is correctly labelled but must not be read as project
   length for that project in any exhibit.

The one genuinely soft number in the corpus is **P8 A5** (rubric decisions axis, scored 2
PROVISIONAL-INFERRED) — the paper cannot settle 1-vs-2, and Oleg's memory can. Worth one
question if the topic comes up; not worth blocking on.
