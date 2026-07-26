# War stories with receipts — WS6 drift archaeology

**Status:** v1.0 — 2026-07-26 (S7). Author judgment over evidence six prior sessions
instrumented. Method: [METHODS.md](../METHODS.md) · findings ledger:
[STATE.md](../STATE.md) · what the argument supports: [ASSESSMENT.md](../ASSESSMENT.md).

---

## How to read this file

Every story below is **n = 1**. That is what a war story is. ASSESSMENT §5.1 splits the
corpus into about five findings resting on hundreds of observations and about seven
resting on a single event, and it binds this file with two rules: **nothing here leads a
section, and no two of these are ever aggregated to imply a rate.** Each story therefore
names the robust number it stands behind. Told in that order they are colour that makes a
measured claim memorable; told first they are anecdote, and the first sharp question in
the room ends the argument.

Three further rules from [METHODS §6](../METHODS.md) constrain what could be written here:

- **Tier A/B evidence (rule 5).** A claim that "we decided X" rests on an artifact that
  *states* the decision. Nothing below infers a decision from a diff, a rename or a
  config change.
- **Declared is not failed (rule 6).** In an append-only substrate a supersession, a
  frozen retro and a registered-MISSING artifact are the discipline *working*. Story 1
  turns on exactly that and would have been a category error told the other way.
- **Void and report (rule 4).** Two stories that looked strong did not survive their own
  receipts. Both are named in §6 rather than quietly dropped, and one of them qualifies a
  published exhibit.

One vocabulary correction runs through all four. btest is **ephemeral**, not flat: at
least ten of its working artifacts existed and never reached git (§6.2 revises S6's
"at least 26"), and its `CLAUDE.md` is a 212-line agent-instruction file. Nothing here
argues that btest failed to write things down.

---

## 1. The hole that was named forty days before anything fell into it

*Stands behind the rework contrast: blive reverses 5.2% of the lines it ever wrote,
btest 82.2% (ASSESSMENT §3.4). This story is one reason blive's number is small.*

**The incident.** On 2026-06-05, in milestone M3.5, the operator stopped and restarted a
live IB Gateway while a purpose-written probe watched
(blive `scripts/probe_ib_reconnect.py`, commit `a2c78f5`). The drill was a substitute for
observing IB's nightly 23:45 ET restart. Three things came back, and the commit body
records them under the heading *"Observed behaviour (recorded from the drill, not
predicted)"*: `IBBroker.is_connected` — a cached boolean — stayed **stale-`True`** while
the real socket had gone; recovery required an explicit `disconnect()` + `connect()`
because `connect()` no-ops on the stale flag; and the restart raised IB error **10141**
("paper trading disclaimer must first be accepted") plus a transient `clientId 1 already
in use`. Positions reconciled on resume.

**What it cost.** Almost nothing — one drill in a milestone that finished on estimate
(RETRO-M3, *Effort vs estimate*: ~5 sessions against ~5–7). The cost is in the
counterfactual: a multi-day live run against a gateway that restarts nightly, with the
engine believing it is connected and no reconciliation on resume. The drill converted
that from an unbounded production risk into a dated paragraph.

**The discipline element that exists because of it.** `KB-7 failure_modes.md`, MISSING →
DRAFT v0.1, carrying FM-1. Also `INV-14 ib_error_codes` v0.9 → v0.10, promoting 10141
from unlisted to catalogued with an operator action attached; the probe script itself
committed as the reusable fixture; and G4 exit criteria #5 and #6 marked MET.

**The part that makes it a substrate story rather than an engineering story.** KB-7 did
not begin at the drill. It was registered as **MISSING in `CONTEXT_INVENTORY.md` at
commit `13f6997` — the repository's first commit, 2026-04-26 — forty days earlier**, with
a stated content contract ("Every failure mode + required engine response + chaos-test
fixture") and a named owner. The drill did not discover that blive had no failure-mode
catalogue. It filled a hole the substrate had already named, dated and assigned. WS5
finding 9 measured the same mechanism from the other end: seven artifacts registered
MISSING with a stated future milestone are why blive's genuine dangling-reference count
across 171 files is **1**, not 8.

**What it generalises to.** An inventory that can hold a *typed absence* changes the
question a project can ask itself. "What don't we know about our failure modes" is
unanswerable; "KB-7 is MISSING, due at M3" is a work item. The cheap version of this is
not an ADR system — it is one table with a row per artifact you have not written yet.

---

## 2. The option that was not on the list

*Stands behind the length-banded altitude result: btest is the lowest-altitude project in
every one of the four turn-length bands (ASSESSMENT §3.5). This is what the operator's
attention was doing at the top of the band.*

**The incident.** At M3.3 on 2026-06-05, resolving OQ-031 (whether Phase 1 could deploy
under a PMA-bound retail account), the agent drafted the option set: accept the non-fill ·
seek Professional-Client classification · de-lever · switch to a mean-reverting archetype.
The operator read it and caught what was missing. From RETRO-M3, *Surprises*
(`docs/retros/M3_retrospective.md:63`):

> **The OQ-031 option set was incomplete as first drafted.** It listed accept /
> Pro-Client / de-lever / mean-revert — all of which drop the leverage or the strategy.
> The operator caught the omission of the *leverage-preserving* path (3× via margin on a
> 1× Nasdaq UCITS, which likely dodges the volatility-triggered PMA cap).

**What it cost.** It cost the reframing, and nothing else, because it was caught before
the ADR. Had it not been, ADR-052 would have resolved OQ-031 against an option set from
which the only intent-preserving choice had been silently removed — and the honest shape
of the problem would never have been stated. It is a **trilemma**, not a menu: PRIIPs
blocks US leveraged ETPs, the PMA cap blocks UK ones, and a Cash account blocks
margin-leverage, so a UK-retail Cash account has *no* open path to leveraged equity
exposure. That framing is now the spine of OQ-032, the central Phase-2 decision.

**The discipline element that exists because of it — and it landed in two different
stores.** In the repository: OQ-032 rewritten to carry the full design space including the
margin-on-a-1×-UCITS path, and ADR-052 introducing the `refined-by:` frontmatter backref
convention. Outside it, the retro routes the general lesson explicitly
(`M3_retrospective.md:113`):

> **Decision option-sets must include the intent-preserving option.** The OQ-031 omission
> (caught by the operator) shows an agent-drafted option list can steer by omission.
> Before surfacing options, explicitly ask "what keeps the original goal, just achieved
> differently?" **Captured in agent memory; not ADR-worthy on its own.**

That agent-memory file exists and is readable:
`~/.claude/projects/C--Users-olegr-PycharmProjects-blive/memory/feedback_surface_full_option_space.md`,
written the same day, quoting the operator directly — *"Omitting it pre-biases the Phase-2
decision toward giving up leverage, when the operator may simply want to obtain it a
different way"* — and closing with the rule in the imperative: *"An option set that drops
the intent-preserving choice is not neutral; it steers the decision by omission."*

**What it generalises to.** Two things, and the second is uncomfortable.

The first: an agent-drafted option list is not a neutral instrument. It is the most
consequential artifact in a decision and the one least likely to be reviewed as a design
object in its own right. blive's substrate had a place to put the correction, and a
protocol that made someone decide *where* it belonged — repo or memory, decision or
standing instruction.

The second: **the fix for this incident is the least durable artifact in the story.** The
agent-memory store is not in git, is not versioned, is not portable across harnesses, and
was invisible to this evaluation's own survivorship instrument for every project whose
transcripts had aged out (§6.2). The retro sentence "captured in agent memory" is a
committed, addressable pointer to something that is none of those things. blive scores
22/24 and still routed a real methodological lesson to its most volatile surface.

---

## 3. One session, two defects, in the project that scores 22/24

*Stands behind the pre-registered null: WS4b, 120 answers, Fisher's exact p = 1.0
(ASSESSMENT §3.1). The negative belongs behind the negative.*

**The incident.** Commit `febc4e3`, 2026-06-06, 13:51 — the Phase-2 readiness-audit
refresh. Its own body describes it as a substrate-only session: *"single-mode, no code
... Tests unchanged (591)."* Four files, +683/−369 lines, three new open questions. Two of
the three are defective, in different ways, and both defects are still in the tree.

**Defect one — a decision that never happened.** `OPEN_QUESTIONS.md:369` records:
*"**Operator decision (2026-06-06): source from EODHD** — not from sfera, and not by
consuming sfera's pre-computed `vix_vxx_rotation.parquet`."* The operator confirms sfera
was never on the table as a blive data source; the standing plan was always EODHD + IB.
The audit took a default nobody had questioned and gave it a date, a decider and a
rejected alternative. Nothing about the code is wrong. What is wrong is that a future
reader — human or agent — will believe a deliberation occurred.

**Defect two — a factual claim that has never been true.** `OPEN_QUESTIONS.md:395`, in
OQ-035: *"blive's order-type surface is `MKT` / `LMT` / `ADAPTIVE_MKT` only ...; it has no
`OPG`-class order type or opening-auction TIF."* `src/blive/domain/types.py:39` defines
**seven** `OrderType` members — MKT, LMT, MOC, LOC, STP, STP_LMT, ADAPTIVE_MKT — and
`TimeInForce` includes OPG. MOC, LOC, STP, STP_LMT and OPG have been there since
`13f6997`, the first commit, 41 days earlier, unchanged. There is no interval during which
the sentence was true. *(The partial rescue, stated because it is real: the IB adapter's
**submit** path builds five order types; MOC/LOC and the OPG TIF appear only in the
inbound parse maps, so "no submit-side OPG wiring" is defensible. "Three only" is not, on
either reading.)*

**The detail that turns this from an error into a mechanism.** The same sentence cites the
record that refutes it. OQ-035 continues: *"INV-2 (order types) and INV-3 (TIFs) are
MISSING per CONTEXT_INVENTORY §3."* The INV-2 row it points at reads, in full:

> `| **INV-2** | docs/inv/order_types.md | MISSING | MKT, LMT, MOC, LOC, STP, STP_LMT, OPG, IOC, FOK + IB support matrix per asset class | ... |`

That row was written at the initial commit and, verified by `git log -S`, **has never been
edited**. The record consulted the pointer for its *status* and never read its *content* —
and the content, one file away, in a row it was already citing by stable id, lists OPG.

**What it cost.** OQ-035's false premise became a design input rather than a correction:
it propagated into `PHASE_2_READINESS.md` v0.2 and `NEXT_PROMPT.md` v1.6 in the same
commit, and it framed a Phase-2 work item ("MOO is not expressible today") that was
partly already expressible. It is also, by coincidence, the divergence this evaluation
built a probe trap on — which is how it was found at all.

**The discipline element that exists because of it: none, in either arm.** This is the
finding. Pair it with btest's `CLAUDE.md:102` — `backtest_runner.py (main orchestrator
~2600 LOC)`, written 2026-03-15 when the file was 1,519 lines, maximum across all 18
commits that ever touched it 1,618, still stated at HEAD. Two opposite substrate
postures, one defect each, and **the same defect: a record that was wrong on the day it
was deposited.** Neither posture has an instrument that checks a factual claim at deposit
time. Every check either project has — supersession backlinks, index tables, freshness
clocks, warm-up protocols — runs at *retrieval*.

**The control that keeps this fair, from the same substrate, one day earlier.** At M3.4 on
2026-06-05 the same discipline correctly declined to manufacture a record. A live
mixed-currency reconciliation found `AccountSnapshot.equity` reading the GBP sleeve
(£902,839) instead of the consolidated `BASE` total (£1,003,886) — a ~10% understatement
on a real account, invisible at M2-IB because the account had been single-currency. It was
fixed, regression-tested, given a diagnostic script, and logged as
**"Bug-fix, no ADR (DD-1 already specified equity = total NAV)"** with DD-1 bumped
§2.8 v0.2 → v0.3. The code was wrong and the record was right, so no decision record was
created. Twenty-four hours later the same substrate dated a decision that was never made.

**What it generalises to.** Append-only discipline preserves what you deposit with high
fidelity — and it is *equally* faithful to errors, to copied-forward wrong anchors (WS5
finding 6: two malformed anchors account for 20 of blive's 26 broken links, because citing
is done by copy), and to non-decisions. There is a second, sharper generalisation
available here, and it must be stated with its n: **both of blive's defects in this
workstream came from the same session, and it is the one session type with no execution
feedback loop.** A session whose job is "go re-audit everything" writes records *about*
things instead of *from* things; the drill in story 1 and the bug fix above both ran code
and both produced records that hold. That is a mechanism observed once, in one session —
not a rate, and not evidence that audit sessions are generally unsafe. It is a hypothesis
with a receipt, and it is cheap to test: require every factual claim in an audit record to
carry the file:line it was read from.

---

## 4. 104,959 lines, and the reasoning is in a chat log

*Stands behind the retransmission tax: blive warms up in 9 of 10 sessions at ~106
characters and falling; btest in 43 of 68 at ~417 and rising (ASSESSMENT §2.1). This is
what the cold end of that looks like at full scale.*

**The incident**, timestamped across one morning, 2026-05-02:

- **09:35:09** — the operator types 748 characters asking for an extraction plan, with the
  reasoning stated in the turn: *"smim does/should not have too many dependencies on dsl
  proj, it is a separate research proje, harp is spinned by smim eg and is also a separate
  proj ... stop.. wait.. think hard.. plan ahead in details."* (sha1 `e66460c50699`,
  `data/session-metrics/turns-classified.json`.)
- **09:43:24** — he pastes back the 6,806-character engineered prompt the agent produced.
  Its first instruction is: *"Execute the prompt below **make sure you first create a plan
  and other context md files you can refer to while working on this long task**."* The
  body carries the full design rationale — a five-way A–E module classification, the named
  coupling risk (`smim/signals`, `profiling.py`, not the numerical core), and the standing
  rule *"The core repo should not depend on btest."* (sha1 `3a39b4ff5c61`.)
- **13:27:50** — commit `7d9b86f`: **387 files, +292 / −104,959**. Commit body: **empty**
  (one byte). Subject in full: `refactor: extract SMIM into standalone repo`.

**What it cost.** The largest single deletion in the corpus has no in-repo statement of
why it happened. WS4a tried to build a probe question on it and could not construct one
from the repository (WS4a finding 2). The plan and context files the operator explicitly
asked for that morning are not in git — they are in the class §6.2 counts, artifacts that
did their job for one session and left no trace. What survives of the reasoning survives
because a JetBrains Copilot session store covering **2026-03-20 to 2026-05-31** happened
to be retained on this machine. A month either side of that window and this receipt does
not exist.

**The discipline element that exists because of it — and it is not an absence.** The same
commit rewrote `CLAUDE.md`'s Architecture Rules. Four rules went in, including
`CLAUDE.md:173-174`:

> - SMIM was extracted into the standalone sibling repo at `...\smim`
> - Do not add new implementation under `src/quantdsl_backtest/smim/`; that duplicate tree
>   has been retired from `btest`

plus a `## SMIM note` section and a matching edit to the Testing Rules. btest's capture
mechanism fired, on the day, correctly. Twelve weeks later those rules are still at HEAD
and still true — WS5 finding 4 measured this arm and found **zero unexplained rule
withdrawals** across 74 rules and 7 versions.

**What it generalises to.** *The capture mechanism you have determines the shape of what
survives.* An instruction file captures **rules**: imperative, undated, without
alternatives, addressed to whoever loads the file next. It structurally cannot capture a
**decision**, which is dated, has a decider, names the options that lost, and needs a
stable id so that later records can cite it. btest wrote the rule and the rule is correct;
the reason is recoverable only from a chat log that survives by retention accident.

Two things this story is careful **not** to claim. It is not "the flat project didn't write
it down" — the operator wrote 7,554 characters of rationale that morning, and the paired
Python 3.12 case (WS5 finding 3) shows btest recording a *why* well, in a commit body,
when it chose to. And it is not a decision that lived only in conversation: the decision
itself is deposited, in `CLAUDE.md`, in the imperative. DEC-N2 remains **0 for 3** — across
three projects the evaluation could not construct a single decision that lived only in a
transcript, and that must be stated as "we could not find one", never as "they do not
exist". What was lost here is the *reasoning*, and what it lacks is an address.

---

## 5. What the four have in common

Read together, and only together, the stories say something the individual measurements
do not:

1. **Every discipline element in this file exists because something went wrong once.** KB-7
   is a chaos drill. The `refined-by:` convention is an omitted option. The
   option-space rule is a near-miss on a Phase-2 scope. None of them was designed in
   advance; all of them are scar tissue that happened to get typed into a file with a
   name. The substrate is not a plan. It is an accretion with an index on it.
2. **The two failures are both at deposit time, and neither posture has a check there.**
   OQ-035 and "~2600 LOC" are the same defect in projects that score 22/24 and 12/24. That
   is the strongest cross-arm statement in this file and it cuts against the thesis.
3. **The most durable thing in a substrate is a rule; the least durable is a reason.**
   btest kept the SMIM rules and lost the reasoning. blive kept ADR-052 and routed the
   generalisable lesson to an agent-memory file. Both projects preserved the imperative
   and were careless with the argument.
4. **Nothing here is a survival-rate story.** Zero blive ADRs were silently reversed;
   S(k) = 1.000 at every k (WS5). The interesting failures are not decisions that decayed.
   They are records that were born wrong, reasons that were never addressed, and
   corrections that were filed somewhere git cannot see.

---

## 6. What was cut, and what did not survive its own receipts

**6.1 Cut: b-autobot's 9,248 committed `node_modules` files** (WS2 finding 5). It has a
clean receipt and a good laugh in it, and it fails beat three: no discipline element was
created, and no absence generalises — it is a missing `.gitignore` line, not a substrate
property. It earned a place in this session's *instrument* audit instead (§6.2): three of
b-autobot's four "ephemeral artifacts" turned out to be Maven-generated third-party
licence files under `b-bot-core/target/reports/apidocs/legal/`.

**Demoted rather than cut: the `AccountSnapshot.equity` bug → DD-1 v0.3**, named in
PLAN §4 as one of three spine items. As its own story its third beat is a documentation
version bump plus a regression test, which any tested project produces; it does not
isolate anything about the substrate. It is far more useful where it now sits — as the
control inside story 3, showing the same substrate declining to manufacture a decision one
day before it manufactured one.

**6.2 Did not survive: "at least 26 btest working artifacts were ephemeral."** ASSESSMENT
§2.6 calls the survivorship audit "the strongest single number in the corpus" and §5.1
lists it as robust with the note *"individual names are spot-checkable."* They were spot
checked this session, one by one, and **16 of btest's 26 path-attributed names are false
positives** in three classes:

| class | n | why it is not an ephemeral working artifact |
|---|---|---|
| Claude Code auto-memory files | 7 | `feedback_recommend_over_poll.md`, `project_datacli.md`, … are durable on disk in `~/.claude/projects/*/memory/`. `artifact_survivorship.py:113` says in its own comment that these "are agent state, not deposits"; `NON_SUBSTRATE` excludes only the literal `memory.md` index. One of the seven, `work-project-anonymization.md`, is shared-substrate's and mis-attributed. |
| flattened duplicates of committed files | 5 | `docs_smim_experiment_plan.md` etc. are `docs/smim/EXPERIMENT_PLAN.md` and its four siblings with the separators mangled. All five were verified committed in btest (`git log --all --diff-filter=A`, one adding commit each) **and** in the smim repo. |
| basenames spliced out of a binary store | 4 | `fredfred1d data.md`, `globalglobal1d data.md`, `reportsreports data_readiness.md`, and one 40-character path fragment ending `readme.md` — adjacent strings joined by regex over `changes.storageData`. |

The corrected floor is **at least 10 of 94 observed** (10.6%) against a published
≥26 of 105 (24.8%); two of the ten (`data.md`, `lock.md`) are single generic words seen
only through LocalHistory with zero prompt mentions, so the firm floor is **8**. Applying
the same read elsewhere: b-autobot **4 → 0**, shared-substrate **3 → 1**, and
**seamQ's 33 and blive's 0 are unchanged** — seamQ's list is clean on hand-read
(`4a adversarial review of b1.md`, `hostile_referee_report_v2.md`, `synthesis_pass3.md` …),
and blive's zero is a floor that no false positive can lower.

Two things follow, and the second is the one that matters.

*The direction.* Every false-positive class **inflates** an ephemeral count, and blive's
count is 0 and cannot be inflated. The instrument's noise is one-directional and runs
**with** the hypothesis.

*The asymmetry.* The auto-memory class can only reach a project whose Claude Code
transcripts survived retention. Enumerated this session: btest 10 transcript files,
shared-substrate 3, datacli 2, and **blive 0, b-autobot 0**. All six btest memory files
that were counted carry mtimes between 2026-07-11 and 2026-07-25 — precisely the surviving
window — while the eight with March–April mtimes are absent. blive has ten memory `.md`
files of its own, including the `feedback_*` files quoted in story 2; the instrument was
structurally incapable of seeing any of them. So the headline pair was, in part, comparing
a project whose agent-side artifacts were visible against one whose were not.

The finding is narrowed, not withdrawn. The primary evidence for it is the operator's own
disclosure that he routinely created and deleted working artifacts, and every count was
published as a lower bound. The itemised adjudication is at
[`data/survivorship-audit.json`](../data/survivorship-audit.json), kept as a published
input; `data/artifact-survivorship.json` is **not** edited and the script is **not**
re-run, per METHODS rule 2.

**6.3 Did not survive as told: "btest's discipline decayed to zero."** This was the most
tempting story in the corpus and it is the one that most needed archaeology. WS2 finding 2
reports btest's bracketed stable-ID commit share by month as 0% → 91% → **96% (Apr,
peak)** → 50% → 40% → **0% (Jul)**. Every number reproduces. What they mean does not
survive the breakdown:

| month | commits | bracket-tagged | of those, carrying a scoped **stable id** | tag family |
|---|---|---|---|---|
| Dec–Feb | 78 | 0 | 0 | — |
| Mar | 216 | 196 | **163** | `[SMIM]` |
| Apr | 92 | 88 | **2** | `[SMIM]` |
| May | 14 | 7 | 0 | `[btest]` |
| Jun | 5 | 2 | 0 | `[btest]` |
| Jul | 10 | 0 | 0 | — |

Three corrections, each verified by an independent shell count (293 · 165 · 280 · 9 · 9,
all reproduced exactly):

- **280 of the 293 tagged commits are `[SMIM]`, and SMIM left the repository** on
  2026-05-02 in `7d9b86f` — story 4's commit. The fall from 96% to 50% is largely a
  *composition* change: the tagged work moved to another repo. btest's own convention,
  `[btest]`, ran for exactly **nine commits** over one month. The residual decay claim
  rests on 29 commits, not 415.
- **The stable-ID discipline collapsed in April, not July.** April's 96% "peak" is 88
  commits tagged `[SMIM]` with **no id inside the bracket at all**; the scoped form
  (`[SMIM DATA-6]`, `[SMIM M4.5-T1]`) runs 163 in March and **2** in April. The peak month
  on the published curve is the month the addressable part disappeared.
- **July is not untagged; it is differently tagged.** Nine of ten July commits carry a
  conventional-commit prefix (`feat(eodhd):`, `chore(eodhd):`, `fix(eodhd):`,
  `feat(datacli):`, `refactor:`). On "does the subject carry *any* structured prefix" the
  curve reads 0% · 96.3% · 96.7% · 64.3% · 100% (n=5) · 90% — adoption in March,
  sustained. That is not a decay curve.

The defensible version is narrower and still worth showing, because it is about the right
property: **btest adopted a stable-ID commit convention in March, stopped scoping it to
ids in April, and lost it entirely when the subproject that owned it was extracted. What
replaced it — conventional commits — is a taxonomy, not an address.** `feat(costs):`
tells you a commit's kind; `[SMIM DATA-6]` tells you what it is *about* and lets a later
record cite it. That distinction is the same one story 4 ends on, and it is the one the
talk actually needs. The published curve as phrased invites "btest stopped being
disciplined", and the evidence does not support that reading.

---

## 7. Receipts index

| # | claim | receipt |
|---|---|---|
| 1 | chaos drill, observed behaviour | blive `a2c78f5` body; `scripts/probe_ib_reconnect.py` |
| 1 | KB-7 MISSING → DRAFT v0.1 | `docs/kb/failure_modes.md:2,21`; RETRO-M3 *Substrate transitions* |
| 1 | KB-7 registered MISSING at first commit | `git show 13f6997:CONTEXT_INVENTORY.md` line 82 |
| 1 | 10141 catalogued | `docs/inv/ib_error_codes.md:44,114` |
| 2 | option set incomplete as drafted | `docs/retros/M3_retrospective.md:63` |
| 2 | lesson routed to agent memory | `docs/retros/M3_retrospective.md:113` |
| 2 | the memory file itself | `~/.claude/projects/C--Users-olegr-PycharmProjects-blive/memory/feedback_surface_full_option_space.md` |
| 2 | trilemma + `refined-by:` convention | ADR-052 (`d4f7bfd`); OQ-032; RETRO-M3 *ADRs raised* |
| 3 | manufactured decision | blive `docs/decisions/OPEN_QUESTIONS.md:369` (OQ-033) |
| 3 | false order-type claim | `docs/decisions/OPEN_QUESTIONS.md:395` (OQ-035) |
| 3 | seven `OrderType` members | `src/blive/domain/types.py:39-46`; `TimeInForce` OPG |
| 3 | the row that refutes it, never edited | `CONTEXT_INVENTORY.md:99`; `git log -S` returns only `13f6997` |
| 3 | both defects, one substrate-only commit | `febc4e3` body: "single-mode, no code ... Tests unchanged (591)" |
| 3 | btest's mirror defect | btest `CLAUDE.md:102`; file 1,519 lines at writing, max 1,618 |
| 3 | the control: bug-fix, no ADR | `git show 3a0ce2a:CONTEXT_INVENTORY.md` banner; DD-1 §2.8 v0.3 |
| 4 | rationale typed at 09:35 | sha1 `e66460c50699` (748 chars) |
| 4 | engineered prompt pasted at 09:43 | sha1 `3a39b4ff5c61` (6,806 chars) |
| 4 | the deletion, empty body | btest `7d9b86f`: 387 files, +292/−104,959; body 1 byte |
| 4 | the rules that were captured | btest `CLAUDE.md:173-174,184` |
| 6.2 | 16 false positives itemised | [`data/survivorship-audit.json`](../data/survivorship-audit.json) |
| 6.2 | transcript coverage asymmetry | 10 / 3 / 2 `.jsonl` for btest / shared-substrate / datacli; **0** for blive and b-autobot |
| 6.3 | tag-family breakdown | independent `git log` counts: 293 bracket · 165 scoped-id · 280 `[SMIM]` · 9 `[btest]` · 9 July conventional |

---

## 8. Limits of this file

- **Every story is n = 1** and is placed as colour behind a named robust number (§1). None
  of them is aggregated with another.
- **One reader, once.** As with WS3's altitude labels and WS5's hand audit, there is no
  second rater. What is published instead is the receipt trail in §7, so a disagreeing
  reader can check every line.
- **Selection is not measurement.** These four were chosen from a corpus already known to
  the author; a story that survives an unsympathetic reading was the selection criterion,
  and §6 names what was rejected and why. That is a mitigation, not a control.
- **Three of four stories are blive's**, because blive is the only project with a retro
  series and an amendments log to read incidents out of. The btest mirror is one story, not
  a matched set, and its receipt survives by retention accident.
- **P8 is deliberately absent.** The work-side case study is the PLAN §5 round-trip, not
  this file.
- **seamQ, harp and smim** do not appear. Any future story touching them must carry their
  measurement-window caveats (STATE.md WS3 finding 6; WS0 coverage boundaries).
