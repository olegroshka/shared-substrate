# NEXT_TASK — S4: WS4a phantom-decision probe, pre-registration

**Recommended model: Fable 5** (per STATE.md's schedule column — this session is
question *design* and a freeze, not a sweep; the reasoning is careful but the volume
is small). Copy the prompt below into a fresh session started in this repo.

> **The one hard rule of this session: the pre-registration commit lands BEFORE any
> probe is run.** Not "before scoring" — before a single question is put to a single
> agent. If you find yourself curious how an answer would come out, that is exactly
> the moment the commit must already exist. WS4 is the talk's only controlled number
> and pre-registration is the only thing that makes it one (PLAN §7 risk 3).

---

## Prompt for S4

Warm up first, then execute. This is session S4 of the shared-substrate eval research.

**Warm-up (read in this order, ~5 min):**
1. `research/eval/STATE.md` — status table, WS0–WS3 findings, corrections ledger.
2. `research/eval/PLAN.md` §4 WS4 — the spec (~20 questions per project for P1, P2,
   P3; checkable ground truth; frozen by commit; correct / abstained / confabulated;
   orientation cost measured separately). Follow it exactly.
3. `research/eval/rubric/ALTITUDE.md` — not because you need the taxonomy, but
   because it is the worked example of what "freeze the instrument, then report
   agreement" looks like in this repo. WS4's protocol should read the same way.
4. Skim the `_meta` header of `research/eval/data/session-metrics/altitude.json` and
   `data/attribution-rules.json` — the house style for published definitions, stated
   caveats, and hand judgment kept as a script *input* rather than a hard-coded
   constant.

**What S4 must produce (and nothing more):**
- `research/eval/probes/PROTOCOL.md` — the frozen procedure: how an agent instance is
  started, what it may and may not read, how many turns it gets, how orientation cost
  is measured, the exact scoring rubric for correct / abstained / confabulated, who
  scores and how ties break, and the stopping rule. Name the probe *subject* model
  and record it (PLAN suggests one fixed model across projects; Sonnet 5 unless you
  have a reason).
- `research/eval/probes/questions-p1.md`, `questions-p2.md`, `questions-p3.md` —
  ~20 questions each for **blive (P1), btest (P2), b-autobot (P3)**, every one with
  its ground truth and the artifact or commit that establishes it.
- **A commit containing exactly those files, with nothing run.** The commit hash is
  the timestamp; say so in the commit message.

**Question design is the experiment's validity — spend the session here.**
- Three question types, per PLAN: *"did we decide X?"* · *"what is the current state
  of Y?"* · *"why was Z rejected?"* Keep the mix roughly even, and the *same* mix in
  all three projects, or the cross-project comparison means nothing.
- Every question needs **checkable ground truth that exists independently of the
  agent** — an ADR, a commit, a manifest line, a test, a plan file. If you cannot
  cite the receipt, the question is not usable. Write the receipt next to the
  question.
- **Include questions whose ground truth is "no"** — decisions that were never made,
  states that do not exist. Without them, "confabulated" cannot be told apart from
  "lucky": an agent that always answers confidently scores well on a question set
  whose answers all exist.
- **Balance difficulty across projects deliberately, and write down how.** The
  obvious failure mode: blive's substrate makes it easy to write 20 answerable
  questions, btest's absence of one makes it easy to write 20 unanswerable ones, and
  the probe then measures the question-writer. Counter it by deriving questions from
  the *same event classes* in each project — a reversal, a rejected alternative, a
  current status, a naming/ownership fact — rather than from whatever each repo
  happens to document well.
- **Watch instrument circularity (PLAN §7 risk 4).** You are writing the test for a
  method you are also advocating. Ask of each question: could a well-run project
  *without* this method answer it? If the honest answer is "never", the question
  tests the presence of an artifact rather than the agent's orientation — reword or
  drop it.

**Evidence you can mine for ground truth (all local, read-only):**
- **blive (P1):** `C:\Users\olegr\PycharmProjects\blive` — ADRs, `NEXT_PROMPT.md`,
  the method docs under `docs/method/`, decision records, the KB. Richest source of
  "why was Z rejected" receipts. WS1 scored it 22/24.
- **btest (P2):** `C:\Users\olegr\PycharmProjects\btest` — 415 non-merge commits,
  `[SMIM …]` stable-ID tags on 293 of them (WS2), CLAUDE.md accretion, and the two
  extraction commits (SMIM 2026-05-02, EODHD→datacli 2026-07-09), which are excellent
  "current state of Y" material precisely because the tree moved under the agent.
- **b-autobot (P3):** `C:\Users\olegr\IdeaProjects\b-autobot` — 91 BDD scenarios, a
  6-day sprint, and stale CLAUDE.md references to deleted plan docs (a WS1 war-story
  lead, and a natural "did we decide X?" trap).
- Session logs are now parsed and classified:
  `research/eval/data/session-metrics/turns-classified.json` (previews + labels) and,
  locally, `.../local/turns-fulltext.jsonl` (verbatim, gitignored — regenerate with
  `scripts/log_miner.py`). Use them to find decisions that were made *only in
  conversation* and never deposited: those make the best confabulation traps, and
  WS6 wants the same list.

**Constraints (carried from S1–S3):** console output ASCII-only (Windows cp1252 — no
arrows, no unicode); Python 3.11 via `python`; never modify the target repos or the
log stores; anything that is author judgment stays a published *input* file rather
than something a re-run can silently overwrite.

**Deposit before ending:** update `research/eval/STATE.md` (WS4a status + 3–6 line
findings summary + session-log entry), then **rewrite this NEXT_TASK.md** for S5 —
the next session and model come from the schedule column in STATE.md's status table
(S5 = WS4b probe runs + scoring, Sonnet 5), which is the source of truth for the
session/model plan.

---

**Nothing is pending on Oleg.** Three items are carried as *reconcile-before-the-talk*,
none of them blockers, and none of them S4's job unless S4 touches them anyway:

1. blive's Requirements v0 is **3,375 words**; the paper says "around six thousand".
   Either the document grew before its v0.2 pass or the paper rounds generously —
   check which, and fix whichever artifact is wrong.
2. seamQ's claude.ai design work predates its first commit by over two weeks, so its
   **git span (1.9 days) is not its project duration**. `duration_days` in
   `data/complexity-profiles.json` is correctly labelled but must not be read as
   project length for that project in any exhibit.
3. **New from S3:** any exhibit plotting rubric score against session-log altitude
   must footnote **seamQ**. WS1 scored the surviving tree (7/24) *after* the substrate
   was deliberately stripped at publication; WS3 measured the in-flight posture, which
   is the corpus's highest. The two instruments have different measurement windows,
   and seamQ is where that shows.

The one genuinely soft number in the corpus is still **P8 A5** (rubric decisions axis,
scored 2 PROVISIONAL-INFERRED) — the paper cannot settle 1-vs-2, and Oleg's memory can.
Worth one question if the topic comes up; not worth blocking on.
