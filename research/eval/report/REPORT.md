# Does the substrate matter? — the evaluation report

**Status:** v1.0 — 2026-07-26 (S8). Synthesis over WS0–WS6; this file adds no new
measurement. Method: [METHODS.md](../METHODS.md) · findings ledger: [STATE.md](../STATE.md)
· the argument and its fragility ledger: [ASSESSMENT.md](../ASSESSMENT.md) · presentable
figures: [exhibits.md](./exhibits.md) · narrative colour: [war-stories.md](./war-stories.md).

**How to read this file.** Sections 1–5 map **1:1 onto the talk's core arc**
([PLAN §9](../PLAN.md)) so the deck can lift each section without re-deciding anything.
Every exhibit carries four things: the number, its **denominator**, the caveat that travels
with it, and a pointer to the `data/` file it comes from. War stories appear only as named
cross-references to [war-stories.md](./war-stories.md), always *after* the robust number
they illustrate. Where a published output was corrected by hand adjudication (twice, in S7),
this report cites the **corrected** figure and names the audit file that holds the
correction; the original JSON outputs are deliberately not edited (METHODS §6 rules 2, 8).

---

## 0. The rules this report is written under

Three rules from [ASSESSMENT §5.1](../ASSESSMENT.md), binding here and on the deck:

1. **Nothing fragile leads a section or carries a claim.** Single-event findings are
   illustrations placed after a robust number, each stated with its n.
2. **No two fragile findings are aggregated to imply a rate.** One confabulation, one
   manufactured decision and one stale claim are three anecdotes, not a trend of three.
3. **A robust count does not license the sentence built on top of it.** Every caption below
   was checked against the reading it invites, not just the number it states. Both S7
   corrections came from that check, and both made the corpus smaller.

Plus the standing evidence rules (METHODS §6): a claim that "we decided X" needs an
artifact that *states* the decision (Tier A/B); a declared supersession is the discipline
working, never a failure; `n/a` is not zero; survivorship counts are lower bounds.

One vocabulary rule runs through everything: **btest is ephemeral, not flat.** It carries a
212-line agent-instruction file, and at least 10 of its 94 observed working artifacts
existed without ever reaching git. No exhibit below compares "substrate" against "nothing";
the comparison is durable-and-addressable against ephemeral-and-unaddressed.

---

## 1. The case, cold *(talk section 1)*

Over two weeks, a legacy component at a regulated financial institution was re-engineered
with AI assistance into **19 gated increments**, delivering business-level parity, now
running in UAT. That is the whole claim this section makes about the work project in this
public report: no employer name, no component name, and no instrumented numbers — P8's git
history and session logs exist only inside the org, and measuring them is the round-trip
this repo's instruments were built to survive ([PLAN §5](../PLAN.md)).

What the evaluation can say about P8 today:

- **Adoption score: 18/24, PROVISIONAL-INFERRED**, placing it 3rd of 8 in the corpus
  (`data/rubric-scores.json`). Four of eight axes were inferred from the paper's account
  rather than scored from artifacts; **A5 (decision records) is the lowest-confidence cell
  in the whole matrix** and should be overruled from the operator's memory if memory
  disagrees. A high-but-not-top placement is what a two-week timeboxed brownfield job under
  partial discipline should look like — which is why the number is credible.
- Its mechanics have a **local rehearsal in the corpus**: b-autobot, a 6-day sprint that
  prototyped the same behavioural-lock-in pattern on personal time in March (§3.2).

The question the room should hold, and the question this report answers with evidence
rather than conviction: *this wasn't model magic — what actually carried it?*

---

## 2. The frame — and what the evidence did to it *(talk section 2)*

The frame in one slide: in this kind of work the human supplies intent, decisions and
taste; the pipeline supplies expansion; a **shared external substrate carries the state**
between sessions, tools and minds.

The evaluation supports a sharper, narrower version of that claim than the one it started
with ([ASSESSMENT §4](../ASSESSMENT.md)):

> The substrate's measurable benefit is **on the human's side of the loop, not the
> model's.** A good agent-instruction file and a strong model will retrieve your recorded
> facts. What they cannot do is make re-entry cheap, keep your short turns as delegation
> rather than assent, or make your reasoning findable later.
>
> The substrate is not what makes you write things down. It is what makes what you wrote
> down **still be there, and still be findable, three sessions later.**

Three exhibits carry this section. All three measure operator behaviour repeated across
hundreds of turns — the robust half of the corpus.

**2a. The retransmission tax** — the strongest single number in the corpus.
blive opens **9 of its 10** sessions with a warm-up turn costing **~106 characters**, and
the cost *falls* over the project's life (192 → 106). btest warms up in **43 of 68**
sessions at **~417 characters**, and the cost *rises* (477 → 607). Four times the cost,
half as often, moving the wrong way — same author, same domain. This is intent going cold,
measured. *(Denominator: 78 sessions, within a corpus of 1,061 classifiable operator
turns. Source: `data/session-metrics/warmup.json`.)*
Two caveats travel with it: btest's sessions also lengthened (9.1 → 19.8 turns), and paste
bodies survive for only 74 of 204 paste-referencing turns, so payload-shaped warm-ups are
**under**-counted — conservative against the finding.
→ *Colour, after the number: [war story 4](./war-stories.md) — "104,959 lines, and the
reasoning is in a chat log" — what the cold end looks like at full scale.*

**2b. Brevity means opposite things in the two postures.**
Among turns under 40 characters, dispatch-by-reference ("read `NEXT_PROMPT.md`, execute")
per bare assent ("continue"): **seamQ 5.0 · b-autobot 0.50 · blive 0.25 · btest 0.10**.
In a substrated project a short turn is delegation; in an ephemeral one it is a clock tick.
btest also has the most short turns: 147, 19% of everything it typed. *(Source:
`data/session-metrics/turns-classified.json`. Fragile numerator, stated per rule 1:
btest's ratio rests on **3** dispatches against 29 "continue"s — two more found dispatches
would move it.)*

**2c. Re-entry is the recurring event the substrate is for.** btest took **16** gaps of
≥5 days across its 213-day history; blive took 1, datacli 1. After btest's gaps, fix-commits
run at 20.8% against an 18.3% baseline — re-entry is not obviously costlier per event, but
btest paid the entry fee sixteen times. *(Counts, not rates — small n everywhere but btest.
Source: `data/git-metrics/*.json`.)*

The tool-era baseline behind all of this: btest's Dec 2025–Feb 2026 era (JetBrains AI
Assistant, no recoverable transcripts, no methodology) produced a mean commit message of
**49 characters** (n=78 commits) against **585** in the methodology era (n=337) — the
corpus's unsubstrated baseline, not a hole in it. *(Source: STATE.md OQ-1;
`data/git-metrics/btest.json`. Caveat: the tool change and the methodology adoption
co-occur — this separates eras, not causes.)*

---

## 3. Four practices *(talk section 3)*

Each practice: what the work project did → the concept → does it generalise, with the
corpus exhibit and its honest limits.

### 3.1 Structural decomposition

**P8:** 19 gated increments; layers as the shortest description first.

**Corpus:** blive ran gated milestones M0→M3 with exit criteria recorded per gate and a
readiness freeze before each phase (WS1 axis A1–A2 evidence, `data/rubric-evidence.md`).
The corpus-wide pattern is à-la-carte adoption scaling with complexity: datacli — a
117-file CLI — kept gates, executable contracts and status-tagged manifests while skipping
ADRs, glossary and session protocol, exactly what the complexity-threshold claim predicts
for a small project *(WS1 finding 3)*.

The moderator behind every cross-project statement: the complexity ordering
**btest > b-autobot > blive > harp > datacli > seamQ** is stable under every primitive
(Kendall's W 0.465–0.605, p < 0.001, chi-square indicative at n=7; smim's rank is
unstable by construction — 1 squashed commit). *(Source: `data/complexity-profiles.json`.
Caveats: `duration_days` is a **git span**, not project length — seamQ's real span is
~3 weeks, not the 1.9 days its git reports; smim is `n/a: history lost`, never zero.)*

### 3.2 Explicit guardrails

**P8:** behavioural lock-in of the incumbent; budgets taken from the live system. *"Gain is
indifferent to sign."*

**Corpus:** b-autobot is the March rehearsal — a BDD regression suite locking in a
WireMock-simulated incumbent, **91 executable scenarios** on the critical surface. Honesty
note that travels with it: its guardrails axis was adjudicated **down** (3→2) in review
because its latency budgets are comments in a config file, not asserted values — the same
deficiency blive was held to 2 for *(WS1 review, S2)*.

The probe adds an honest negative that sharpens this practice: the predicted mechanism
"stale in-tree references *induce* confabulation" **did not fire**. On both questions built
around b-autobot's doc/tree divergence, a fresh agent counted the tree and was right — 91
scenarios, not the docs' 66; CI disabled, not the README badge's live nightly *(WS4b
finding 5; `data/probe-results.json`)*. A 2026-era agent checks the code against the doc.
What it cannot check is a claim about a *conversation* — which is where §3.3 picks up.
*(Fragility note: b-autobot's zero-confabulation sheet rests on two abstentions held by a
conservative tie-break; read as commitments they become 2 confabulations — n stated per
rule 1.)*

### 3.3 System representation

*"Drift is excursion without reversion."* This is the practice the evaluation changed the
most, and the section leads with its two robust results — one positive, one null — before
any single-event illustration.

**Robust result 1: recorded facts come back near-perfectly in *both* arms.** Across the
pre-registered probe's recorded slots, a fresh agent retrieved blive **28/28**, btest
**28/28**, b-autobot **24/28**. Retrieval of deposited facts is not where the substrate
boundary sits. *(Denominator: 84 recorded slots across 3 projects, 2 runs each. Source:
`data/probe-results.json`, verdicts in `data/probes/scores.json`.)*

**Robust result 2: zero blive decision records were silently reversed.** S(k) = 1.000 at
every k from 0 to 12 sessions; the *declared* curve falls only to 0.962 at k=12 on blive's
single, both-ends-declared supersession (ADR-021 → ADR-043). **Every point carries its
`at_risk` denominator: k=12 rests on 26 of the 53 ADRs**, and the coverage is disclosed —
18 of 53 ADRs were read against the tree; the rest are not counted as having survived a
test they were never given. *(Source: `data/survival.json`, hand audit in
`data/survival-audit.json`. Structural caveat: this curve has **one arm** — btest has no
decision records, so its column is `n/a`, a different substrate type (instruction rules +
commit prose), never a zero on a shared denominator.)*

**The pre-registered experiment, told straight.** WS4b, frozen by commit `ab9c62d` before
any run, asked whether the substrate reduces confabulation. **It does not, at this corpus
size: Fisher's exact p = 1.0** — btest 38/38 correct with zero confabulations, blive 37/38
with the corpus's **only** confabulation, b-autobot 36/38. After review the nominal
direction runs *backwards*: the one invented answer belongs to the full-substrate project,
and it invented a **why** — a rationale for a deliberation that never happened. *(Sources:
`data/probe-results.json`, `data/probes/scores.json`; 3 of 20 question slots were voided
on ground-truth failure — 15% of the instrument — and every void ran against the
hypothesis. Fragility per rule 1: the reversed direction rests on **one** confabulation;
the null survives any single re-scoring.)*

Why the null is evidence *for* the reframe rather than against the practice: **a 212-line
CLAUDE.md plus git history plus a 2026-era model was enough for a perfect retrieval
score.** The floor has risen; "your agent will invent decisions without a substrate" is no
longer true of a fresh agent doing retrieval, and conceding that from the stage is worth
more than having it raised from the floor. The confound is stated with it: the "flat" arm
is not flat — it is ephemeral, with a real agent-instruction file *(WS4b finding 10)* —
and that may explain the null on its own.
→ *Colour, after the null: [war story 3](./war-stories.md) — one substrate-only session
in the 22/24 project produced both of blive's defects, including a record that cites the
row that refutes it.*

**What actually separates the arms: addressability, shown by the corpus's only clean
control.** On 2026-06-05 the Python floor moved to 3.12 in both repos — same operator,
same day, same decision. blive wrote ADR-053 (4,902 chars), **cited from five artifacts
including the one an agent auto-loads**. btest wrote commit `fd106f9` (1,025 chars) — and
it is a *good* record: reason, validation, exact edits, flagged follow-up. It is **cited
from zero artifacts** and reachable only by knowing the sha. ADR-053's `companion:` field
even names `fd106f9`: the addressable record of btest's decision lives in blive's repo.
**The naive story — "the flat project didn't write down why" — is false. Reasons are
deposited unevenly and unaddressably, not undeposited.** *(n = 1 by construction: a case
study, not a rate. Source: `data/survival-audit.json`, WS5 finding 3.)*

**The decay exhibit, retitled after correction.** btest's commit-convention history is not
"discipline went to zero." The counts (all reproduced by independent shell greps): 293 of
415 non-merge commits carry a bracketed tag, but **280 of the 293 are `[SMIM]` — and SMIM
left the repository** in `7d9b86f` (2026-05-02); only **165 of 293 carry a scoped stable
id** (`[SMIM DATA-6]`): 163 in March, **2** in April, 0 after; and July is *differently*
tagged — 9 of its 10 commits carry a conventional-commit prefix, so on "any structured
prefix" the curve reads 0 → 96.3 → 96.7 → 64.3 → 100 (n=5) → 90%. The defensible claim:
**btest adopted a stable-ID convention, stopped scoping it to ids in April, and lost it
with the subproject that owned it; what replaced it is a taxonomy, not an address.**
`feat(costs):` tells you a commit's kind; `[SMIM DATA-6]` tells you what it is about and
lets a later record cite it — the same distinction the Python 3.12 pair turns on.
*(Sources: `data/git-metrics/btest.json`; breakdown in STATE.md WS6 finding 6 and
[war-stories.md §6.3](./war-stories.md). Caption rule: never show "0% in July" as an
absence of discipline.)*

**And the substrate carries state only if the artifacts survive.** Across three
independent observation channels: **blive 0 of 33 observed working artifacts never reached
git; btest at least 10 of 94; seamQ at least 33 of 89** — all lower bounds. *(Sources:
`data/artifact-survivorship.json` — which retains the uncorrected S6 numbers by design —
with the S7 hand adjudication that corrected btest ≥26 → **≥10** and b-autobot 4 → 0 in
`data/survivorship-audit.json`. Two instrument properties must be published with any use:
every false-positive class *inflates* an ephemeral count and blive's is zero, so the noise
is one-directional and runs **with** the hypothesis; and the agent-side channel reaches
only projects whose transcripts survived retention — btest 10 files, **blive 0** — so
blive's own agent-memory files were structurally unobservable.)*

The discipline's own failure surface, stated so the section is not advocacy: blive's
in-file ADR index went stale (2 wrong statuses, 2 missing rows of 53 — while the outer
CONTEXT_INVENTORY register stayed correct); two malformed anchors were copied forward into
20 of its 26 broken cross-references (7 distinct targets over 900 checked); and one open
question, OQ-033, records an "Operator decision" for an option that was never on the table
— append-only records can manufacture history as well as preserve it *(n = 1; operator
recollection; told properly in [war story 3](./war-stories.md))*. *(Source:
`data/survival.json`, `data/survival-audit.json`.)*

Finally, the slot built to catch "a decision that lived only in conversation" failed to
find one in three independent attempts (**DEC-N2: 0 for 3**). This cuts *for* the
deposit-everything thesis — but it rests on three negative constructions, so it is stated
as "we could not find one", never "they do not exist."

### 3.4 Continuous validation

**P8:** parity against the incumbent as the oracle; checks in the loop. *"An oracle the
agent cannot query is an audit, not a guardrail."*

**Corpus, the robust contrast:** blive reverses **5.2%** of every line it ever added
(3.9% within 14 days); btest reverses **82.2%** (32.6% within 14 days) — an 8–16× gap.
The confound is stated wherever the number appears: btest's history is **5× longer**
(213 days vs 41), giving its lines more opportunity to die, and the projects differ in
nature. Texture, not proof. *(Denominators: tens of thousands of added lines per repo;
churn is a blame-free LIFO approximation whose biases are documented in
`_meta.definitions`. The 14-day column is comparable only across blive/btest/harp. Source:
`data/git-metrics/*.json`.)*
→ *Colour, after the number: [war story 1](./war-stories.md) — the chaos drill that filled
a hole the substrate had named forty days earlier is one reason blive's number is small.*

**Honest split:** test trajectory follows project *nature*, not substrate posture —
b-autobot 0.79→0.72 test-file share (a BDD suite *is* tests), btest 0.13→0.35, blive
0.22→0.30, against harp's 1 test file and seamQ's 0. The research projects' oracle is
elsewhere (pre-registration, adversarial review), which is the boundary finding again
*(WS2 finding 6; source: `data/git-metrics/*.json`)*.

**The cross-arm statement, said plainly because it cuts against the thesis:** neither
substrate posture has an instrument that checks a factual claim **at deposit time**.
blive's OQ-035 (wrong about code unchanged since the first commit) and btest's
`CLAUDE.md:102` "~2600 LOC" (never true on any day) are the same defect in projects
scoring 22/24 and 12/24. Every check either project owns — supersession backlinks, index
tables, freshness clocks, warm-up protocols, parity oracles — runs at *retrieval*.
*(One defect per project; a pair of anecdotes, not a rate — but the symmetry is the
point. Source: `data/survival-audit.json`; [war story 3](./war-stories.md).)* The
practice's frontier, offered as a hypothesis with a receipt, n=1: require every factual
claim in an audit-produced record to carry the `file:line` it was read from.

---

## 4. The research, examined *(talk section 4)*

### 4.1 Scorecard against the plan's four claims

| claim ([PLAN §1](../PLAN.md)) | verdict | carried by |
|---|---|---|
| 1. Paradigm — attention migrates up, substrate enables it | **Partial** — survives only length-controlled | §4.4 below |
| 2. Failure modes follow absent substrate | **Split** — restart cost yes; **phantom decisions null** | §2a positive; §3.3 null |
| 3. Practice — same author, same domain, with/without | **Weak** — the "without" arm is ephemeral, not without | §3.3, §3.4, confound 6 |
| 4. Boundary — exploratory research out of scope | **Supported, and refined** | research-native instruments: harp's pre-registration with stop-for-futility rules, smim's kill rules, seamQ's three-persona adversarial review. A pre-registration *is* a frozen intent contract; the claim becomes "different artifact types and lifecycle", not "no substrate" *(WS1 finding 1)* |

### 4.2 The standing reminder

**METR: experienced developers were 19% slower while feeling 20% faster.** Including the
author's own felt productivity. Every positive number above is read against that result;
this ledger is what separates the talk from advocacy. Two of the sharpest items in this
evaluation — the survivorship confound and the fragility ledger — exist because the
*operator* pushed back on the evaluation, not because an instrument caught them.

### 4.3 What the experiment failed to show — four honest negatives

Stated separately, per rule 2 — four negatives, not a "trend of four":

1. **The pre-registered experiment came back null** (p = 1.0), and its nominal direction
   reversed: the corpus's only confabulation belongs to the full-substrate project (§3.3).
2. **Altitude does not track discipline inside btest.** Monthly high-altitude share 0.256 ·
   0.251 · 0.192 · 0.400 (n=5) · 0.303 against the tag curve's 91 → 96 → 50 → 40 → 0%.
   July has btest's least artifact discipline and its second-highest altitude — the hoped-for
   within-project migration is **not supported** *(WS3 finding 5)*.
3. **btest's instruction file does not decay silently.** 28 of 74 rules ever removed, zero
   unexplained — the hypothesis was the opposite. Conservative: rewording counts as
   removal+addition, biasing the removal count up *(WS5 finding 4; committed file only)*.
4. **Zero blive ADRs were silently reversed** — the drift the discipline exists to prevent
   was not found in the discipline's own record either arm could brag about; the real
   failures were records **born wrong**, one per project (§3.4).

And two corrections this evaluation applied to *itself* (S7): btest's ephemeral-artifact
floor ≥26 → **≥10**, and the tag-decay curve reread as a composition change. **Each time
this corpus has been read adversarially, its headline numbers have got smaller and its
argument narrower.** That trend has not yet turned around — which is the strongest reason
to present §2's reframe rather than the original claim, and to say a third careful reader
would probably find something too.

### 4.4 Closing exhibit: where the human's attention actually went

The raw cross-project altitude comparison **fails** — high-altitude share puts b-autobot
(0.46), the least substrated build, near the top, because high share rises monotonically
with turn length inside every project. **No altitude number is publishable without its
length band.** Length-controlled, the contrast returns: **btest is the lowest of the four
measurable projects in every band**, and blive beats it in all four (0–39 chars: 0.19 vs
0.08 · 40–119: 0.26 vs 0.15 · 120–399: 0.42 vs 0.35 · 400+: 0.80 vs 0.65).
*(Denominator: 1,061 classifiable turns; instrument stability on a pre-assigned held-out
split κ = 0.902 on the high/low collapse — one rater, so stability, not inter-rater
reliability. Any plot of rubric score against altitude must footnote **seamQ**: WS1 scored
its stripped tree, WS3 measured its in-flight posture. Source:
`data/session-metrics/altitude.json`.)*
→ *Colour, after the number: [war story 2](./war-stories.md) — what the top of blive's
band looks like: the operator catching the option an agent-drafted decision list silently
dropped.*

### 4.5 The confounds ledger, in full

Named here and on stage, per [PLAN §7](../PLAN.md):

1. **No controls.** P1 vs P2 differ in nature (production engine vs research platform),
   age and model era. Case comparison, not experiment — except WS4, which was controlled
   and came back null. Partially mitigated by the complexity profile: every comparison is
   read against it, treating complexity as the theory's own moderator.
2. **Learning effect.** The author was more experienced by the time blive existed;
   discipline and skill co-evolved and cannot be separated here.
3. **Selection.** Projects chosen by the person evaluating his own methodology. Countered
   by pre-registration (WS4), boundary cases expected *not* to show the effect (P5–P7),
   and publishing the extraction scripts.
4. **Instrument circularity.** The rubric operationalises the author's own method; its
   scores must never appear without an outcome measure beside them.
5. **Log coverage.** Uneven transcripts: blive's Claude Code sessions are gone (logs begin
   2026-05-02, after 30 of its 70 commits); btest's Dec 2025–Feb 2026 era has no
   recoverable transcript at all; P5–P7 have none found locally. Reported, not patched.
6. **Artifact survivorship — the most serious confound, because it is correlated with the
   treatment.** The operator routinely created working artifacts that were never committed
   and often deleted, so every artifact-based measurement sees a *surviving* subset.
   blive's protocol required committing the substrate; btest had no such rule — the bias
   runs **with** the hypothesis. Measured rather than asserted, then corrected by hand
   adjudication: **blive 0 of 33 observed artifacts ephemeral · btest ≥10 of 94 · seamQ
   ≥33 of 89 · b-autobot 0 · harp 2** — all lower bounds (a file never typed and never
   tool-written is invisible to all three channels). The instrument's noise is
   one-directional (every false-positive class inflates an ephemeral count; blive's zero
   cannot be lowered), and its agent-side channel could not see projects whose transcripts
   aged out — blive's ten agent-memory files were structurally unobservable.
   Consequences: WS1 is **not** re-scored (existence is recoverable, content is not; the
   scores stand as a measurement of *durable* substrate, and RUBRIC.md's scope statement
   says so); WS2/WS3/WS4 are unaffected (commit-derived, turn-derived, and
   what-can-a-fresh-agent-recover-today respectively); and the corpus-wide framing is
   **ephemeral**, not flat. *(Sources: `data/artifact-survivorship.json` uncorrected by
   design; corrections itemised in `data/survivorship-audit.json`.)*

### 4.6 Fragility, named rather than felt

About five findings rest on hundreds of observations; about seven rest on a single event
— and the split is structural: **every robust finding measures the operator's behaviour
repeated across sessions; every fragile one measures an agent's behaviour on one
question.** The full ledger, including the third category S7 added (robust counts that
carried a fragile interpretation), is [ASSESSMENT §5.1](../ASSESSMENT.md). The reframe in
§2 rests entirely on the robust half. If a slide leads with one of the seven, the first
sharp question in the room ends the argument; if it leads with one of the five, the seven
become the colour that makes the five memorable.

---

## 5. Interactive segment *(talk section 5)*

The audience scores their own project on the one-page four-practices rubric (handout
derived from [`rubric/RUBRIC.md`](../rubric/RUBRIC.md)), then the moderated discussion
runs on two axes the corpus makes concrete:

- **The adoption spectrum to place themselves on:** blive 22 · smim 20 · work-project 18
  (provisional) · datacli 17 · harp 16 · b-autobot 15 · btest 12 · seamQ 7 (of 24).
  *(Source: `data/rubric-scores.json`. Caveats on the slide, not the appendix: the rubric
  scores **durable** substrate only (confound 6); seamQ's 7 scores a deliberately stripped
  publication tree, not its in-flight posture; the instrument operationalises the
  author's own method.)*
- **The complexity check, because the honest message includes the lower bound:** the
  discipline's own claim is that it pays *above* a complexity threshold — below it, flat
  notes win. datacli is the in-corpus demonstration of à-la-carte adoption at small scale
  (§3.1). "Score low and simple" is a fine place to be.

And the closing question the altitude exhibit earns: *when you type a short message to
your agent, is it a dispatch — or a "continue"?*

---

## 6. What this report is not allowed to claim

Carried verbatim from [METHODS §9](../METHODS.md), so nobody discovers it from the room:
whether the substrate causes better *outcomes* (the proxies are behavioural); whether it
works for anyone else (one author, one domain family, one model era); whether the
practised substrate differed from the recorded one where content is unrecoverable;
anything about team collaboration (every project is single-operator); and P8's
instrumented numbers, which exist only inside the org until the §5 round-trip runs.

---

## Appendix

- **[exhibits.md](./exhibits.md)** — the exhibit bench: every presentable figure with its
  source file, honest caption, and the caveat that must travel with it. The deck shops
  from that file; nothing in it is mandatory.
- **[war-stories.md](./war-stories.md)** — the four stories with receipts, their common
  pattern (§5), and what was cut and why (§6).
- Numbers that must never appear without their qualifier: [exhibits.md §caption-rules](./exhibits.md).
