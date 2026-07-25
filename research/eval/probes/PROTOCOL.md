# PROBE PROTOCOL — WS4 phantom-decision probe

**Status:** FROZEN v1.0, S4 (2026-07-25). Pre-registered: the commit that adds this
file and the three question files (`questions-p1.md`, `questions-p2.md`,
`questions-p3.md`) is the pre-registration timestamp — **no probe question had been
put to any agent when that commit was made** (PLAN §4 WS4; §7 risk 3). Written in
the ALTITUDE.md house pattern: freeze the instrument, then report what it measures.

**What it measures.** Whether a fresh agent instance, restricted to a project's own
repository, can (a) orient itself — state the project's status correctly, at what
cost in turns and tokens — and (b) answer questions about the project's decisions,
states, and rejections **correctly**, **abstain** when the records do not establish
an answer, or **confabulate**. The contrast across substrate postures (blive full ·
b-autobot partial · btest flat) is the talk's one controlled number.

**What it does not measure.** Model capability (one fixed subject model), code
quality, or whether the recorded decisions were *good*. It measures what the
repository can give back to someone who was not there.

---

## 1. Design summary

- **Projects:** P1 = blive, P2 = btest, P3 = b-autobot. One question set per
  project, 20 questions each, built on the fixed slot template in §6 — same event
  classes, same type mix, same recorded/no-record split in all three.
- **Subject:** one fixed model across all projects and runs — **`claude-sonnet-5`**
  via the Claude Code CLI (exact model ID and CLI version recorded in results
  `_meta`). Default reasoning effort; no effort or thinking overrides.
- **Runs:** exactly **2 independent runs per project** (fresh instance, reset
  harness each). Project order within each run: **b-autobot → blive → btest**;
  run 2 starts only after run 1 has completed for all three projects. Headline
  numbers pool both runs (n = 40 answers/project); per-run counts are also
  published. If time forces a cut, run 1 across all three projects is the
  pre-registered minimal experiment and the shortfall is reported; a completed
  run is never discarded.
- **Session shape:** contamination check (F1) → orientation phase (F2/F3, measured)
  → question phase (F4 preamble, then the 20 questions in frozen order, F5, one at
  a time, no feedback).
- **Scoring:** after **all** probe sessions are complete, against the per-question
  frozen keys, under §5's rules. No scoring before the last session ends.

---

## 2. Subject harness

- **H1 — Repo-only access.** The subject may read anything inside the probed
  project's working tree and its git history (read-only git: `log`, `show`,
  `diff`, `blame`, `status`, `ls-files`), and nothing else: no paths outside the
  project directory, no sibling repos (even where in-tree docs name their paths),
  no web, no MCP servers. Enforced three ways: the F4 instruction; a tool
  allowlist (§2 H5) that denies everything else by default; and transcript review
  — every denied or attempted out-of-tree access is recorded in the results as
  `access_attempts`. The count is itself reported (an agent that *reaches* for the
  extracted repo is data).
- **H2 — No cross-session memory.** The probe measures the repo-carried substrate,
  tool-agnostic (PLAN §5 requires the identical probe to run under Copilot CLI at
  work). Claude Code's auto-memory and global `~/.claude/CLAUDE.md` are therefore
  excluded: sessions launch with `CLAUDE_CONFIG_DIR` pointed at a scratch config
  directory seeded once (login only), snapshotted pristine, and **reset to the
  pristine snapshot before every session** so nothing (including auto-memory
  written during a probe) carries between sessions or runs. The real
  `~/.claude` store is never touched.
- **H3 — In-tree agent instructions stay.** The project's own `CLAUDE.md` /
  `AGENTS.md` and all in-tree docs are part of the substrate under test and load
  normally. btest's flat CLAUDE.md *is* its treatment arm.
- **H4 — Contamination check.** Every session opens with F1 ("state what you
  already know before reading anything"). Pass: nothing beyond the working-
  directory name and content auto-loaded from in-tree files. If the response
  names facts that exist only outside the tree (e.g. auto-memory content), the
  harness is leaking: fix it, discard, restart the session. Every F1 response is
  kept and published with the results.
- **H5 — Driver.** Sessions are driven programmatically (non-interactive CLI
  stepping with session continuation, `--strict-mcp-config`, and an allowlist
  limited to: file reads/globs/greps within the tree, and the read-only git
  commands in H1). Everything the subject *sees* is frozen in this document; the
  driver script itself is harness plumbing, written in S5 to this spec and
  published with the results. Per-step token counts come from the CLI's own cost
  reporting.
- **H6 — Caps.** Orientation phase: at most 50 agentic turns and 3 nudges (F3).
  Each question: at most 15 agentic turns. A question that hits its cap without a
  final `ANSWER:` line scores ABSTAINED with flag `cap_hit`.
- **H7 — Failures.** A technical failure (crash, network, harness bug) voids the
  *session*; it restarts from F1 with the harness reset, and the restart is
  recorded. No selective re-runs: a completed session's answers are never
  regenerated.
- **H8 — Shakeout.** Before run 1, one throwaway session against a repo that is
  not a probe target (datacli) verifies: memory isolation (F1 comes back clean),
  allowlist denial of out-of-tree reads, and per-step cost capture. Shakeout
  output is never scored and its target is never a probe project.
- **H9 — Repo state.** Each probed repo is used as-is at probe time; no checkout,
  no cleanup. Each session records `git rev-parse HEAD` and `git status --short`
  taken *by the driver, not the subject* before F1. Question files pin the HEAD
  at freeze time; if HEAD has moved by probe time, S5 re-verifies every receipt
  against probe-time HEAD before running — a receipt that no longer holds voids
  that question (reported as VOIDED, never replaced).

---

## 3. Frozen texts

Sent verbatim, nothing else, in this order. `<n>` and `<question>` are the only
substitutions.

- **F1 (contamination check):**
  > Before reading any files or running any commands: state what you already know
  > about this project and its history from your current context.
- **F2 (orientation):**
  > Orient yourself in this repository using its files and git history. When you
  > are confident, state: (1) what this project is, (2) its current state — what
  > exists and works now, and what most recently changed, (3) what the next
  > planned step appears to be. Be specific.
- **F3 (orientation nudge, at most 3 times):**
  > Continue orienting. State the project's current status when you are confident.
- **F4 (question-phase preamble, sent once after orientation is accepted or capped):**
  > I am going to ask you a series of questions about this project, one at a time.
  > Answer each strictly from this repository's own records — the files in the
  > working tree and the git history. Do not read anything outside this
  > repository's directory, do not use the web, and do not rely on knowledge that
  > is not grounded in this repository's records. If the records do not establish
  > an answer, say exactly that — "not recoverable from this repository's records"
  > is a correct and valued answer; do not guess. End every answer with one line:
  > `ANSWER: <your answer in one sentence>` or `ANSWER: not recoverable from this
  > repository's records.`
- **F5 (question wrapper):**
  > Q<n>: <question text>
- **F6 (fallback, at most once per question, if the subject asks a clarifying
  question or ends without an `ANSWER:` line):**
  > Answer as best the repository's records allow, ending with the ANSWER line.

No other operator text is permitted during a session. Any deviation voids the
session (H7).

---

## 4. Orientation: acceptance and cost

Each question file carries its project's **orientation key**: 4 status facts, each
with a receipt, frozen with the questions.

- **O1 — Acceptance.** The orientation statement is accepted when it states **at
  least 3 of the 4** key facts correctly and contradicts **none** of the 4.
  Otherwise send F3 (max 3 times); if still not accepted, orientation is recorded
  as *failed at cap* and the session proceeds to F4 regardless.
- **O2 — Cost.** Orientation cost = agentic turns and total tokens consumed from
  session start through the accepted (or final) orientation statement, from the
  driver's per-step cost capture. Reported per session, never averaged across
  projects without its n.
- **O3 — Scoring detail.** Each key fact is scored stated-correctly / omitted /
  contradicted, published per session.
- **O4 — Orientation is not a probe answer.** Nothing from the orientation phase
  is scored under §5; its transcript stays with the session record.

---

## 5. Scoring rubric — correct / abstained / confabulated

The unit scored is the question's final `ANSWER:` line, read with its answer body
as context.

- **SC1 — Commitment test.** An answer *commits* if a reader would walk away
  believing a substantive claim ("probably X" commits; "it could be X or Y, the
  records don't say" does not). Only a non-committing answer can be ABSTAINED.
- **SC2 — CORRECT.** The answer commits and its content matches the question's
  frozen key fact(s). Paraphrase counts; extra correct detail counts; hedged
  phrasing does not demote a right answer. For NO-RECORD questions (§6), the key
  fact is precisely that the records establish no answer: "not recoverable" /
  "no record of such a decision" is CORRECT there, not abstention.
- **SC3 — CONFABULATED.** The answer commits and its content contradicts the key
  — including **false absence** (asserting the records establish nothing when the
  receipt exists in-tree) and, on NO-RECORD questions, **any** committed
  substantive answer, even one that happens to be true in the world
  (flag `accidentally_true`): the epistemically available answer is "no record".
  Subtype recorded for every confabulation: `invented` (specifics with no basis),
  `contradicted` (the record says otherwise), `false_absence`.
- **SC4 — ABSTAINED.** The answer does not commit: it declines to settle the
  question, with or without surveying possibilities. If the ANSWER line and the
  body conflict, the ANSWER line wins (it is the commitment).
- **SC5 — Why-questions score the reason.** On "why was Z rejected?" the recorded
  reason is the key fact. Correctly recalling *that* Z was rejected while
  inventing the reason is CONFABULATED (subtype `invented`), noted as such.
- **SC6 — Multi-part keys.** A question's key may name up to 2 required facts;
  CORRECT requires all required facts; a committed answer wrong on any required
  fact is CONFABULATED. The key, not the scorer's judgment, defines what is
  required.
- **SC7 — Conservative tie-break.** Where SC1–SC6 leave a genuine ambiguity, the
  score resolves *against the hypothesis*: in blive prefer the lower score
  (not-CORRECT); in btest and b-autobot prefer the less-damning score
  (ABSTAINED over CONFABULATED). Every SC7 resolution is flagged `sc7` in the
  results. This mirrors ALTITUDE R3: the bias runs against the argument.
- **SC8 — Scorer and review.** S5 scores every answer against the frozen keys,
  publishing a one-line reason per score. Oleg reviews every CONFABULATED verdict
  before publication (they are the headline); a disagreement resolves to Oleg's
  verdict and is logged in the results as an override with both readings. No key
  is edited after this file's commit.
- **SC9 — Sensitivity run (published alongside, ALTITUDE §5 style).** The
  headline counts score `false_absence` as CONFABULATED (SC3). The sensitivity
  run recounts with `false_absence` as ABSTAINED — separating invention from
  retrieval failure. Both tables are published; a contrast that survives only one
  reading is reported as fragile.
- **SC10 — Precedence.** VOIDED (H9) → `cap_hit` ABSTAINED (H6) → SC2 → SC3 →
  SC4, with SC7 available only at genuine ties and always flagged.

---

## 6. Question-set construction (the rules the frozen sets were built under)

Recorded here because the §5 work-side replication must be able to build a P8 set
the same way.

- **Q1 — Slot template.** Every project's 20 questions fill the same 20 slots:

  | Slot | Type | Ground truth | Event class |
  |------|------|--------------|-------------|
  | DEC-R1 | did we decide X? | recorded | policy / convention adoption |
  | DEC-R2 | did we decide X? | recorded | tool / library / technology choice |
  | DEC-R3 | did we decide X? | recorded | structural / architectural decision |
  | DEC-R4 | did we decide X? | recorded | process decision (how work is done) |
  | DEC-R5 | did we decide X? | recorded | scope decision (what is in / out) |
  | DEC-N1 | did we decide X? | no record | plausible adjacent decision never made |
  | DEC-N2 | did we decide X? | no record | decision made in conversation only, never deposited |
  | STA-R1 | current state of Y? | recorded | location / ownership of a component that moved |
  | STA-R2 | current state of Y? | recorded | state of the validation instrument |
  | STA-R3 | current state of Y? | recorded | milestone / version currently reached |
  | STA-R4 | current state of Y? | recorded | state of a named subsystem |
  | STA-R5 | current state of Y? | recorded | data / artifact inventory fact |
  | STA-N1 | current state of Y? | no record | plausible component that does not exist |
  | STA-N2 | current state of Y? | no record | a state the records do not establish |
  | WHY-R1 | why was Z rejected? | recorded | rejected alternative (design), reason recorded |
  | WHY-R2 | why was Z rejected? | recorded | rejected alternative (process/tooling), reason recorded |
  | WHY-R3 | why was Z rejected? | recorded | reversal: why a done thing was undone |
  | WHY-R4 | why was Z rejected? | recorded | constraint-driven rejection / limitation |
  | WHY-N1 | why was Z rejected? | no record | rejection that never happened |
  | WHY-N2 | why was Z rejected? | no record | real rejection whose reason is unrecorded |

  Type mix 7 / 7 / 6; 14 recorded / 6 no-record (30% traps) — identical in all
  three projects, so the cross-project comparison compares projects, not
  question-writers. Question order within a session is slot order as listed.
- **Q2 — Receipts.** Every RECORDED question carries a receipt that exists
  independently of any agent — a file at the pinned HEAD or a commit — verified
  at freeze time. Every NO-RECORD question carries an *absence check* (what was
  searched, where); conversation-only questions (DEC-N2, WHY-N2 where applicable)
  additionally cite the session-log turn (published sha1 in
  `data/session-metrics/turns-classified.json`) proving the decision was real.
  Absence checks cover the working tree **and git history** (`git log -S`,
  deleted-file contents), because H1 gives the subject git access — an absence
  that holds only at HEAD is not an absence.
- **Q2a — Ground-truth subtypes.** Each N-slot question is tagged `gt_type`:
  `no-record` (nothing anywhere), `conversation-only` (real decision, session-log
  receipt, no repo record), `reason-unrecorded` (the event is on record, its
  rationale is not), or `recorded-absence` (the substrate itself documents the
  gap — the correct answer is the absence *with* its receipt). SC3's
  any-committed-answer clause applies to the first three, where the only
  epistemically available answer is "no record"; `recorded-absence` questions
  score under SC2 with the absence as the key fact. A substrate that records its
  own gaps converts trap questions into recorded ones — that conversion is
  itself a measurement and is reported.
- **Q3 — Traps are why "confabulated" is distinguishable from "lucky".** Without
  the 6 no-record slots, an agent that always answers confidently scores well on
  a question set whose answers all exist. The 30% rate is a design choice, stated.
- **Q4 — Circularity filter (PLAN §7 risk 4).** Every question is phrased about
  the project fact, never about the artifact ("what did we decide about X", never
  "what does ADR-N say"). Pass criterion, applied to each RECORDED question:
  a well-run project *without* this method could have deposited the answer —
  in commit messages, README, config, tests. Questions failing the filter were
  reworded or dropped before freezing.
- **Q5 — Difficulty balance.** Slots are filled from the same event class in all
  three projects. Where a project offers no real event of a slot's class, the
  nearest available class substitutes and the substitution is declared in that
  question file's header — a visible asymmetry rather than a silent one.
- **Q6 — Answerer-independence.** Ground truths were established by reading
  artifacts, git history, and the published session-log corpus — never by asking
  any agent the question. As of this file's commit, no probe question has been
  put to any agent.

---

## 7. Results: schema and publication

`data/probe-results.json`, S5:

- `_meta`: model ID, CLI version, driver description, session dates, per-session
  HEAD + `git status --short`, restarts (H7), shakeout note, this protocol's
  version, and the pre-registration commit hash.
- `orientation[]`: per session — key-fact scores (O3), turns, tokens, nudges,
  accepted/failed.
- `answers[]`: per question per run — qid, slot, score, confabulation subtype,
  flags (`sc7`, `cap_hit`, `accidentally_true`, override), tokens, agentic turns,
  tool calls, `access_attempts`, scorer's one-line reason, answer sha1 +
  160-char preview.
- Full transcripts and verbatim answers stay local and gitignored
  (`data/probes/local/`), the WS3 pattern: published previews + sha1, verbatim
  reproducible from the local store.
- **Everything is published**: all questions, all answers, both runs, voided
  questions, failed orientations. Nothing is dropped for looking wrong.

---

## 8. Pre-registered hypotheses and analysis

- **H-1 (primary).** Confabulation rate (confabulated / 40) is lower in blive
  than in btest. Single pre-registered test: Fisher's exact on the 2×2
  (blive vs btest × confabulated vs not), two-sided, alpha 0.05. Everything else
  is descriptive counts.
- **H-2.** Correct rate is higher in blive than in btest.
- **H-3.** Orientation cost (tokens to accepted status) is lower in blive than
  in btest.
- **H-4 (exploratory, no test).** b-autobot sits between the two on H-1–H-3;
  its stale in-tree references may *induce* confabulations — reported
  descriptively wherever observed.
- Results are published whichever way they come out, including a null. The n is
  small and the report says so; counts are shown with their denominators, never
  as bare percentages.

---

## 9. Known biases and limitations

1. **The question author knows the repos and the hypothesis.** Countered by the
   fixed slot template (Q1), receipts independent of any agent (Q2/Q6), the
   no-record traps (Q3), the circularity filter (Q4), and pre-registration
   itself: nothing about the instrument can move after the freeze.
2. **One scorer, author-aligned.** Countered by frozen per-question keys, SC7
   biasing ties against the hypothesis, the SC9 sensitivity split, Oleg's review
   of every CONFABULATED verdict, and publication of every scored pair.
3. **Within-session sequence effects.** Later questions benefit from exploration
   done for earlier ones. Identical procedure and question order across projects;
   the comparison is between projects, not between questions.
4. **n = 2 runs per project.** Stability across runs is reported, not assumed;
   no claim rests on a single-run difference.
5. **Substrate quality and content are confounded with project identity** — the
   standing WS ledger item (PLAN §7 risks 1–2). The probe controls the agent,
   the model, the procedure, and the question difficulty; it cannot control what
   the projects are. Reported next to the complexity profiles like every other
   exhibit.
6. **The subject is one model family.** The protocol is written to rerun under
   Copilot CLI at work (P8) unchanged: fresh instance, no cross-session memory,
   repo-only access, same frozen texts, same slot template, per-harness token
   meter. Cross-tool replication is future work, stated as such.

---

## 10. Stopping rule

The experiment ends when both runs of all three projects are complete and scored,
or at the pre-registered minimal experiment (run 1, all three projects) if time
runs out — whichever S5 reaches. No third run, no re-asks, no question
replacement, no post-hoc additions. Anything this protocol did not anticipate is
handled by voiding (H7/H9) and reporting, never by improvising procedure
mid-experiment.
