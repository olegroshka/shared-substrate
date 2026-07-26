---
marp: true
theme: default
paginate: true
---

<!--
V2 of the deck (v1 kept as slides.md).
Render as slides:  npx @marp-team/marp-cli talks/does-the-substrate-matter/slides-v2.md -o slides.html
Or open in VS Code with the Marp extension. Reads as plain markdown on GitHub.

What v2 changes vs v1: section 2 opens with the paper's philosophical frame before any
evidence — the era claim (engaging Google's New-SDLC quote), creative input vs cognitive
load, the responsibility inversion, and the personal-evolving-substrate reading of
AI-assist. Section 4 gains one slide: the deck-building miss (surface pattern-matching
vs implied intent), told as the evaluation's third self-correction. The close carries
the era framing. Core arc ~44 slides, ~35 min; the section mapping onto REPORT §§1–5
still holds, with §2 extended beyond the report by paper material (docs/presentation.md
is the source for the borrowed concepts).

Every number travels with its caveat ON THE SAME SLIDE — a slide that shows an exhibit
without its caveat is misquoting the report. Slide titles follow the honest captions in
report/exhibits.md and are not sharpened beyond them. Self-sufficiency rule: a first-time
viewer needs no prior context — every entity introduced, every term glossed at first use.

Public-surface rule: this file is committed to the public repo. The work project appears
only as "a legacy component at a regulated financial institution". Where the in-room talk
may name it, NOTES.md says "name verbally".
-->

# Does the substrate matter?

## A case study, the evidence — and what this new era asks of the human

**Two weeks, one legacy component — and seven personal projects instrumented to answer the n=1 objection**

Oleg Roshka · internal talk · 2026-07-30
Evidence & instruments: [github.com/olegroshka/shared-substrate](https://github.com/olegroshka/shared-substrate) `research/eval/`

---

# 1 · The case, cold

Over two weeks, a legacy component at a regulated financial institution was re-engineered with AI assistance into **19 gated increments** — business-level parity, now running in UAT.

<!-- name the component and employer verbally; they are in the circulated abstract, not in this committed deck -->

That is the whole claim this talk makes about the work project up front. No instrumented numbers — its git history and session logs live inside the org; measuring them properly is a planned follow-up there.

The question to hold for the rest of this talk:

> ### This wasn't model magic. What actually carried it?

---

## The case on its own yardstick

Scored on the same 8-axis adoption rubric as the personal corpus (you'll score your own project on it later):

- **18 / 24 — PROVISIONAL-INFERRED** · 3rd of 8 projects
- High but **not top** — which is what a two-week, timeboxed, brownfield job under partial discipline *should* look like. That is why the number is credible.
- Its mechanics had a **local rehearsal**: a 6-day personal sprint in March prototyped the same behavioural-lock-in pattern (more later).

*Caveats on this number: four of eight axes inferred from a written account, not scored from artifacts; the decisions axis (A5) is the lowest-confidence cell in the whole matrix; the row is refreshed in-org against real history later.*

---

# 2 · What is actually shifting

Google's recent whitepaper on the new software development lifecycle puts it like this:

> *"The most profound shift in software engineering isn't a new language, framework, or cloud service. It's the transition from writing code to expressing intent, and trusting intelligent systems to translate that intent into working software."*
> — Google, *The New SDLC: From Vibe Coding to Agentic Engineering* (2026)

True — and, I will argue, **too narrow**. Code → intent is one floor of a taller building.

**The shift is in how humans engage with information.** Software engineering is just where it lands first, because software has oracles — compilers, tests, an incumbent to measure against. The same transition is coming for every discipline whose work is thinking made durable.

---

## Purpose, in one line

# Separate genuine human creative input from cognitive load.

- **Creative input** — the choices, the intent, the taste. What no pipeline can derive from what is already on record.
- **Cognitive load** — the re-explaining, the re-deriving, the bookkeeping, the expansion. Everything a pipeline *can* derive.

The human deposits the first, **once, at the right layer**. The machinery carries the second.

Everything else in this talk is the engineering required to make that separation real — and measurable.

---

## What offloads — and what cannot

The working test, in plain words: **how surprised would a strong model be by your contribution, given everything already on record?**

| you produce | surprise | so it is |
|---|---|---|
| renames, formatting, a boilerplate adapter from a schema | ≈ none | **load — offload it** |
| a summary of a document the agent can read itself | ≈ none | **load — offload it** |
| *"Settle T+1, not T+2 — the broker's cutoff is 17:30 CET"* | high | **yours — deposit it** |
| *"this option list is missing the one path that keeps our goal"* | high | **yours — deposit it** |

As models strengthen, the top rows grow and the bottom rows do not. **The human migrates up, not out.**

*(The formal version — conditional description length, the κ measure — lives in module M-F for anyone who wants it.)*

---

## The inversion: your edge becomes your job

When everything derivable is offloaded, what remains is not less work — it is a **different job**:

# Intent. Decisions. Scope. Taste. Judgment of meaning.

- Whatever you are genuinely better at than the model stops being a comparative advantage and becomes your **entire responsibility surface**.
- The one oracle that cannot be automated is **you**: model output is *plausible by construction, not correct by construction*, and only the intent-holder can tell the difference at the top layer.
- Delegation is not the human doing less. **It is the human's effort converging on the only work that was ever irreducibly theirs.**

*(Hold this thought — in section 4 I will show you this job being done, on this very talk.)*

---

## There is no generic substrate

How should AI assistance be perceived, then? Not as a tool you adopt — as a **coupling you grow**. And what grows on your side is a **personal substrate: individual, evolving, yours**.

- Every element of the discipline in tonight's evidence exists because something went wrong **once**, for this operator, on this project. A substrate is **scar tissue with an index**, not a template.
- The same author runs different substrates on different projects, scaled to their complexity — you will see a small CLI that keeps gates and contracts and skips the rest, correctly.
- So an organisation cannot roll a substrate out. It can only make **growing one cheap** — and teach people what belongs in theirs.
- And the change does not arrive because a few people discuss ideas in a room. It arrives as **continuous mass implementation**: everyone practising, daily, each closing their own **self-reflection loop** — notice the miss, deposit the lesson, work differently tomorrow. A skill is refined the way skills always are: **by reps with feedback, not by rollout.**

*Your substrate will not look like mine. The evidence tonight is about whether growing one matters at all.*

---

## The frame in one picture

<p align="center"><img src="../../assets/fig-centroid.png" width="560" alt="The pinned centroid"></p>

In this kind of work the **human** supplies intent, decisions and taste; the **pipeline** supplies expansion; a **shared external substrate** carries the state between sessions, tools and minds.

That was the claim going in. Seven projects and six workstreams later, the evidence supports a **sharper, narrower** version —

---

## The thesis, as the evidence left it

> The substrate's measurable benefit is **on the human's side of the loop, not the model's.** A good agent-instruction file and a strong model will retrieve your recorded facts. What they cannot do is make re-entry cheap, keep your short turns as delegation rather than assent, or make your reasoning findable later.
>
> The substrate is not what makes you write things down. It is what makes what you wrote down **still be there, and still be findable, three sessions later.**

Three exhibits carry this. All three measure **operator behaviour repeated across hundreds of turns** — the robust half of the evidence.

---

## The evidence base — seven of my own projects

The answer to the "it's one project" objection: same author, same era, **instrumented rather than remembered**.

| project | what it is | substrate posture |
|---|---|---|
| **blive** | live algo-execution engine (trading) | **full discipline**: decision records, inventories, protocols |
| **btest** | backtesting platform, same domain | **ephemeral**: a 212-line agent-instruction file, no decision records; working files often never reached git |
| b-autobot | 6-day Java sprint — the March rehearsal | partial |
| datacli | small data-ops CLI | light, à la carte |
| smim · harp · seamQ | research projects | research-native instruments (more later) |

**blive vs btest is the central pair** — same author, same trading domain, opposite postures. Evidence: 1,480 session-log turns across three log stores, 600+ commits, every extraction script published. Nothing tonight is from memory.

*Caveat that governs everything: this is a case comparison, not an experiment — the full confounds ledger comes at the end, out loud.*

---

## Exhibit 1 · The retransmission tax

**Re-entry costs 4× as much, is paid half as often, and moves the wrong way in the ephemeral project.**

A *warm-up turn* is what you type at session start to rebuild context before new work begins.

| | warm-up frequency | cost per warm-up | over project life |
|---|---|---|---|
| **blive** (substrated) | 9 of 10 sessions | ~106 chars | **falling** 192 → 106 |
| **btest** (ephemeral) | 43 of 68 sessions | ~417 chars | **rising** 477 → 607 |

Same author, same domain. This is intent going cold, measured.

*Denominator: 78 sessions, 1,061 classifiable operator turns. Caveats: btest's sessions also lengthened (9.1 → 19.8 turns); paste bodies survive in only 74 of 204 paste-referencing turns, so payload-shaped warm-ups are under-counted — conservative against this finding.*

---

## Exhibit 2 · What a short turn is made of

**In a substrated project brevity is delegation; in an ephemeral one it is a clock tick.**

Among turns under 40 characters — dispatch-by-reference (*"read `NEXT_PROMPT.md`, execute"*) per bare assent (*"continue"*):

| seamQ | b-autobot | blive | btest |
|---|---|---|---|
| **5.0** | 0.50 | 0.25 | **0.10** |

btest also has the *most* short turns: 147 — 19% of everything its operator typed.

*These are the four projects with enough surviving session logs to measure. Fragile numerator, stated per the rules: btest's ratio rests on **3** dispatches against 29 "continue"s — two more found dispatches would move it.*

---

## Exhibit 3 · Re-entry is the recurring event the substrate is for

- btest took **16** gaps of ≥5 days across its 213-day history; blive took **1**; datacli **1**.
- After btest's gaps, fix-commits run at 20.8% against an 18.3% baseline — re-entry is **not obviously costlier per event**; btest simply paid the entry fee sixteen times.

And the tool-era baseline underneath it all: the same repo, pre-methodology (Dec 2025 – Feb 2026, AI-assisted, no substrate, no recoverable log): mean commit message **49 characters** (n=78). Methodology era: **585** (n=337).

*Caveats: gap counts, not rates — small n everywhere but btest. The 49 → 585 jump sits at a tool boundary too: tool change and methodology adoption co-occur, so this separates eras, not causes.*

---

# 3 · Four practices

Each told the same way:

**what the work project did → the concept underneath → does it generalise** (exhibit from the personal corpus, honest limits attached)

1. Structural decomposition
2. Explicit guardrails
3. System representation
4. Continuous validation

---

## 3.1 · Structural decomposition

**Work project:** 19 gated increments; layers as the shortest description first.

<p align="center"><img src="../../assets/fig-hierarchy.png" width="360" alt="Hierarchy of layers"></p>

**Corpus:** blive ran gated milestones M0→M3 with exit criteria recorded per gate and a readiness freeze before each phase. And adoption is à-la-carte, scaling with complexity: **datacli** — a 117-file CLI — kept gates, executable contracts and status-tagged manifests while *skipping* ADRs, glossary and session protocol. Exactly what the complexity-threshold claim predicts for a small project.

---

## The moderator behind every cross-project claim

Complexity ordering, stable under every measured primitive:

> **btest > b-autobot > blive > harp > datacli > seamQ**

Kendall's W 0.465–0.605, p < 0.001 — so no cross-project comparison in this talk is read without it.

*Caveats: chi-square approximation indicative at n=7; smim's rank is unstable by construction (1 squashed commit — `n/a: history lost`, never zero); `duration_days` is a **git span**, not project length — seamQ's real span is ~3 weeks, not the 1.9 days its git reports.*

---

## 3.2 · Explicit guardrails

**Work project:** behavioural lock-in of the incumbent; budgets taken from the live system.

> *"Gain is indifferent to sign."*

<p align="center"><img src="../../assets/fig-divergence.png" width="480" alt="Open vs closed loop divergence"></p>

**Corpus:** b-autobot is the March rehearsal — a BDD regression suite locking in a simulated incumbent, **91 executable scenarios** on the critical surface.

*Honesty note that travels with it: its guardrails score was adjudicated **down** (3→2) in review — its latency budgets are comments in a config file, not asserted values. The same deficiency held the top-scoring project to 2.*

---

## What the probe added here — an honest negative

*(The probe — a pre-registered experiment, told in full two slides on: fresh AI-agent instances quizzed against each repo, with checkable ground truth.)*

The predicted mechanism *"stale in-tree references induce confabulation"* **did not fire**.

On both questions built around b-autobot's doc/tree divergence, a fresh agent counted the tree and was right: **91 scenarios, not the docs' 66; CI disabled, not the README badge's live nightly**.

A 2026-era agent checks the code against the doc. What it cannot check is a claim about a **conversation** — which is where the next practice picks up.

*Fragility note: b-autobot's zero-confabulation sheet rests on two abstentions held by a conservative tie-break; read as commitments they become 2 confabulations.*

---

## 3.3 · System representation

> *"Drift is excursion without reversion."*

The practice the evaluation **changed the most**. Two robust results first — one positive, one null — then the case studies.

**The probe, in one line:** 20 questions per project with checkable ground truth — *did we decide X? what is the state of Y? why was Z rejected?* — put to fresh AI-agent instances with repo-only access, two independent runs each. Questions and scoring frozen by commit **before any run**.

**Robust result 1: facts that are written down come back near-perfectly in *both* arms** (substrated and ephemeral alike). On the questions whose answers are recorded in the repo: blive **28/28** · btest **28/28** · b-autobot **24/28**.
Retrieval of deposited facts is **not** where the substrate boundary sits.

*Denominator: 84 recorded-answer questions across 3 projects, 2 runs each.*

---

## Robust result 2 · Zero silent reversals

blive keeps its decisions as **53 append-only Architecture Decision Records (ADRs)** — dated, reasoned, citable by stable ID. The question: do later sessions silently contradict them?

**No blive decision record was silently reversed in 12 sessions of exposure — the failures live elsewhere.**

- Survival S(k) — the share of records still standing un-contradicted k sessions after they were written — is **1.000** at every k from 0 to 12.
- The *declared* curve falls only to 0.962 — one record replaced by a successor that says so, on both ends. A declared supersession is the discipline **working**.

*Every point carries its `at_risk` denominator: at k=12 the curve rests on **26 of the 53** records, not 53. "Sessions" here are a git proxy (maximal commit runs, 4-hour gap threshold). Coverage disclosed: 18 of 53 ADRs were read against the tree; the rest are not counted as having survived a test they were never given. And this curve has **one arm** — btest has no decision records; its column is `n/a` (a different substrate type: instruction rules + commit prose), never a zero on a shared denominator.*

---

## The pre-registered experiment, told straight

**My own pre-registered experiment failed to show the substrate reduces confabulation — and the one confabulation belongs to the full-substrate project.**

*(Confabulation: an invented answer presented as recorded fact.)*

- Questions and scoring frozen by commit **before any run**. Fisher's exact **p = 1.0**.
- btest 38/38 correct, zero confabulations · blive 37/38, the corpus's **only** confabulation · b-autobot 36/38.
- The one invented answer invented a **why** — a rationale for a deliberation that never happened.

*Caveats: the reversed direction rests on **one** confabulation (fragile); the null survives any single re-scoring. 3 of 20 question slots were voided on ground-truth failure — 15% of the instrument — every void ran against the hypothesis.*

---

## Why the null is evidence *for* the reframe

**A 212-line CLAUDE.md — the project-root instruction file AI coding agents load automatically — plus git history plus a 2026-era model was enough for a perfect retrieval score.**

The floor has risen. *"Your agent will invent decisions without a substrate"* is no longer true of a fresh agent doing retrieval — and I would rather concede that from up here than have it raised from the floor.

The confound is part of the story: the "flat" arm is **not flat** — it is *ephemeral*, with a real agent-instruction file. That may explain the null on its own.

**btest is ephemeral, not flat** — no exhibit in this talk compares "substrate" against "nothing". The comparison is durable-and-addressable against ephemeral-and-unaddressed.

---

## What actually separates the arms: addressability

**Both repos recorded the same decision the same day; one record is cited from five artifacts, the other from zero.** *(n = 1 by construction — a case study, not a rate.)*

2026-06-05, the Python floor moves to 3.12 in both repos. Same operator, same day, same decision:

- blive writes **ADR-053** (4,902 chars) — cited from **five** artifacts, including the one an agent auto-loads.
- btest writes commit `fd106f9` (1,025 chars) — and it is a **good** record: reason, validation, exact edits, flagged follow-up. Cited from **zero** artifacts; reachable only by knowing the sha.
- ADR-053's `companion:` field even names `fd106f9`: the addressable record of btest's decision lives **in blive's repo**.

**The naive story — "the flat project didn't write down why" — is false.** Reasons are deposited *unevenly and unaddressably*, not undeposited.

---

## A taxonomy is not an address

**btest's commit-convention history, retitled after correction:** a stable-ID convention was replaced by a taxonomy.

- 293 of 415 commits carry a bracketed tag — but **280 of 293 are `[SMIM]`** — a research subproject that lived inside btest — **and SMIM left the repository** in May, extracted to its own repo.
- Scoped stable ids (`[SMIM DATA-6]`): 163 in March · **2 in April** · 0 after.
- July is *differently* tagged: 9 of 10 commits carry a conventional-commit prefix. On "any structured prefix" the curve reads 0 → 96 → 97 → 64 → 100 *(n=5)* → 90%.

`feat(costs):` tells you a commit's **kind**; `[SMIM DATA-6]` tells you what it is **about** and lets a later record cite it — the same distinction the Python 3.12 pair turns on.

*Caption rule honoured here: never show "0% in July" as an absence of discipline.*

---

## And the substrate carries state only if artifacts survive

**Everything blive's sessions produced reached git; at least one in nine of btest's working artifacts never did.**

Observed through three independent channels — typed prompts, IDE local-history records, agent tool-call paths — matched against everything ever committed:

| blive | btest | seamQ | b-autobot | harp |
|---|---|---|---|---|
| **0 of 33** ephemeral | **≥10 of 94** *(firm floor 8)* | ≥33 of 89 | 0 | 2 |

All lower bounds — a file never typed and never tool-written is invisible to every channel we have.

*These are the **hand-corrected** figures (the instrument's first run said ≥26 for btest; adjudication removed 16 false positives). Two instrument properties travel with any use: every false-positive class inflates an ephemeral count and blive's zero is unlowerable — the noise is one-directional and runs **with** my hypothesis; and the agent-side channel reaches only projects whose transcripts survived retention — blive's own ten agent-memory files were structurally unobservable.*

---

## The discipline's own failure surface

Stated so this section is not advocacy. In the 22/24 project:

- The index table *inside* the ADR file went stale — 2 wrong statuses, 2 missing rows of 53 — while the project-level artifact inventory stayed correct. **What goes stale is the index, not the records.**
- Two malformed anchors were copied forward into 20 of its 26 broken cross-references. Append-only preserves errors with the fidelity it preserves decisions.
- One open question records an **"Operator decision" for an option that was never on the table** — append-only records can manufacture history as well as preserve it. *(n = 1; operator recollection.)*

And the slot built to catch "a decision that lived only in conversation" failed to find one in three attempts (**0 for 3**) — which cuts *for* deposit-everything, but rests on negative constructions: **"we could not find one," never "they do not exist."**

---

## 3.4 · Continuous validation

**Work project:** parity against the incumbent as the oracle; checks in the loop.

> *"An oracle the agent cannot query is an audit, not a guardrail."*

<p align="center"><img src="../../assets/fig-loop.png" width="520" alt="The control loop"></p>

---

## The rework contrast

**Four fifths of every line the ephemeral project added was later deleted — against one line in twenty.**

| | reversed, any horizon | within 14 days |
|---|---|---|
| blive | **5.2%** | 3.9% |
| btest | **82.2%** | 32.6% |

**The confound is stated wherever this number appears:** btest's history is **5× longer** (213 vs 41 days), giving its lines more opportunity to die, and the projects differ in nature. **Texture, not proof.**

*Denominators: tens of thousands of added lines per repo; churn is a blame-free LIFO approximation with documented biases; the 14-day column is comparable only across blive/btest/harp.*

---

## The honest split — and the shared defect

**Tests follow project nature, not substrate posture.** b-autobot 0.79→0.72 test-file share (a BDD suite *is* tests) · btest 0.13→0.35 · blive 0.22→0.30 · harp 1 test file · seamQ 0. The research projects' oracle is elsewhere: pre-registration, adversarial review.

**And the cross-arm statement, said plainly because it cuts against the thesis:** neither posture checks a factual claim **at deposit time**. One record in each arm was wrong *on the day it was written* — in projects scoring 22/24 and 12/24. Every check either project owns runs at *retrieval*.

The practice's frontier, offered as a hypothesis with a receipt (n=1): require every factual claim in an audit-produced record to carry the `file:line` it was read from.

*(One defect per project — a pair of anecdotes whose symmetry is the point, not a rate.)*

---

# 4 · The research, examined

| claim | verdict |
|---|---|
| 1 · Attention migrates up; substrate enables it | **Partial** — survives only length-controlled |
| 2 · Failure modes follow absent substrate | **Split** — restart cost yes; phantom decisions **null** |
| 3 · Same author, same domain, with/without | **Weak** — the "without" arm is ephemeral, not without |
| 4 · Exploratory research is out of scope | **Supported, and refined** — research work carries *its own* substrate instruments (pre-registration is a frozen intent contract) |

---

## The standing reminder

> **METR (2025): experienced developers were 19% slower with AI tools — while believing they were 20% faster.**

Including the author's own felt productivity. Every positive number in this talk is read against that result.

The same class of tools measures **+26%** in large field experiments (gains concentrated in less experienced developers) and **+56%** on well-specified greenfield tasks. The moderators that reconcile them — task abstraction level, codebase maturity, operator experience — are substrate-shaped.

Two of the sharpest items in this evaluation — the survivorship confound and the fragility ledger — exist because the **operator pushed back on the evaluation**, not because an instrument caught them.

This ledger is what separates the talk from advocacy.

---

## What the experiment failed to show — 1 of 4

### The pre-registered experiment came back null.

p = 1.0 — and its nominal direction *reversed*: the corpus's only confabulation belongs to the full-substrate project.

*(Told in full in §3.3. Stated separately from the other three negatives — four negatives, never a "trend of four".)*

---

## What the experiment failed to show — 2 of 4

### Altitude does not track discipline inside btest.

*(Altitude: every turn the operator types, classified by the level it works at — declaring intent, making decisions, shaping design = **high**; pasting errors, steering line-fixes, re-explaining context = **low**. The full exhibit comes in a moment.)*

**The month with the least artifact discipline had the second-highest altitude.**

Monthly high-altitude share: 0.256 · 0.251 · 0.192 · 0.400 *(n=5)* · 0.303 — against a tag curve of 91 → 96 → 50 → 40 → 0%.

The hoped-for within-project migration is **not supported**.

*Caveats: June is 5 turns; and the tag curve itself is largely a composition change (§3.3).*

---

## What the experiment failed to show — 3 of 4

### btest's instruction file does not decay silently.

**28 of 74 rules were withdrawn — zero unexplained** (25 in one scope-change commit). The hypothesis going in was the opposite.

*Conservative: rewording counts as removal + addition, biasing the removal count up. Committed file only — the ephemeral class is unobserved.*

---

## What the experiment failed to show — 4 of 4

### Zero blive ADRs were silently reversed.

The drift the discipline exists to prevent **was not found in the discipline's own record**. The real failures were records **born wrong** — one per arm, at deposit time, where neither posture has a check.

---

## And two corrections this evaluation applied to itself

- btest's ephemeral-artifact floor: published **≥26 → corrected ≥10** (16 false positives, itemised by hand).
- The tag-decay curve: reread as a **composition change**, not "discipline went to zero".

> **Each time this corpus has been read adversarially, its headline numbers have got smaller and its argument narrower.** That trend has not turned around — and a third careful reader would probably find something too.

Which is the strongest reason this talk presents the *reframe*, not the original claim.

---

## A third correction happened while building this deck

Three days before this talk, the agent that built these slides — holding the **entire evaluation report** in context — produced a deck perfectly faithful to it and **illegible to anyone without it**. It passed every check it had. Every one of those checks compared the slides to sources the agent was *holding*; none asked what a reader **without** them would see.

It was caught by the operator, applying a rule written down nowhere: *a presentation must be self-sufficient.*

The same shape appears across this corpus *(n = 1 each — a shape, not a rate)*:

- a record that cited the very row refuting it — it read the pointer's **status**, never its **content**;
- an option list that silently dropped the only intent-preserving path;
- these slides — every fact correct, the implied reader missing.

**Perfect surface pattern-matching; the implied intent missed.** The check that would catch it — a fresh-context decode test — is this evaluation's own probe, pointed at deliverables instead of repos. Until that exists, the catch is the human's job. **This is the §2 inversion, demonstrated: that judgment *is* the job now.**

---

## Closing exhibit · Where the human's attention actually went

**Controlled for turn length, the ephemeral project's operator sits lowest in every band.**

Every one of 1,061 operator turns classified by what it does: intent, decisions, design (**high altitude**) vs mechanical steering — *paste this error, fix that line* (**low**). High-altitude share, blive vs btest, per typed-length band:

| 0–39 chars | 40–119 | 120–399 | 400+ |
|---|---|---|---|
| **0.19** vs 0.08 | **0.26** vs 0.15 | **0.42** vs 0.35 | **0.80** vs 0.65 |

btest is lowest of the four measurable projects in **all four bands**.

***Never publish altitude without its band:** the raw ordering is a verbosity artifact that puts the least substrated build on top. Denominator: 1,061 turns; held-out agreement κ = 0.902 is one-rater stability, not inter-rater reliability; seamQ was scored on its stripped tree but measured in-flight.*

---

## The confounds ledger, out loud

1. **No controls** — case comparison, not experiment (except the probe, which was controlled — and came back null).
2. **Learning effect** — discipline and skill co-evolved; not separable here.
3. **Selection** — projects chosen by the person evaluating his own methodology.
4. **Instrument circularity** — the rubric operationalises the author's own method; never shown without an outcome measure.
5. **Log coverage** — uneven transcripts; the substrated project's early sessions are gone.
6. **Artifact survivorship — the most serious, because it is correlated with the treatment.** Every artifact-based measurement sees a *surviving* subset, and the bias runs **with** the hypothesis. Measured, then hand-corrected; the framing is *ephemeral*, not flat.

About five findings rest on hundreds of observations; about seven rest on a single event. **Every robust finding measures operator behaviour repeated across sessions; every fragile one measures an agent's behaviour on one question.** The reframe rests entirely on the robust half.

---

# 5 · Score your own project

The handout: **four practices, eight questions, 0–3 each.** Two minutes, honest answers.

**Step 0 is the complexity check** — days of work, one person, few decisions? **Stop: flat notes are the right tool.** The discipline predicts its own irrelevance below the threshold — "score low and simple" is a fine place to be. (datacli is the in-corpus demonstration: à-la-carte at 117 files.)

The spectrum to place yourself on:

| blive | smim | work-project | datacli | harp | b-autobot | btest | seamQ |
|---|---|---|---|---|---|---|---|
| 22 | 20 | 18 *(provisional)* | 17 | 16 | 15 | 12 | 7 |

*Caveats on the slide, not the appendix: the rubric scores **durable** substrate only; seamQ's 7 scores a deliberately stripped publication tree, not its in-flight posture; the instrument operationalises the author's own method — which is why it never appears without the outcome evidence you just saw.*

---

## The closing question

The altitude exhibit earned this:

> ### When you type a short message to your agent — is it a dispatch, or a "continue"?

---

## What this evaluation is not allowed to claim

- Whether the substrate causes better **outcomes** — the proxies are behavioural.
- Whether it works for **anyone else** — one author, one domain family, one model era.
- Whether the *practised* substrate differed from the *recorded* one where content is unrecoverable.
- Anything about **team** collaboration — every project is single-operator.
- The work project's instrumented numbers — those exist only inside the org, until the follow-up leg runs there.

---

# Close

- The shift is bigger than code → intent: it is a change in **how humans engage with information** — software is only where it lands first.
- The measurable benefit is on the **human's side of the loop**: cheap re-entry, brevity as delegation, reasons that stay findable.
- Recorded facts come back near-perfectly **in both arms** — the floor has risen; the boundary is the **why**, and its address.
- Neither posture checks a claim **at deposit time** — and catching what the pattern-matcher misses is now the operator's defining job.
- Your substrate will be **personal and evolving** — and below the complexity threshold, flat notes win; the discipline says so itself.

**The substrate is not what makes you write things down. It is what makes what you wrote down still be there, and still be findable, three sessions later.**

Paper, field manual, evidence: [github.com/olegroshka/shared-substrate](https://github.com/olegroshka/shared-substrate)

---

# Expansion modules

**Everything after this slide is optional** — pulled in as the room's appetite dictates, any order. The core arc you just saw is complete without them.

- **M-A** · The eight-project spectrum in depth
- **M-B** · War stories with receipts
- **M-C** · Session-log deep dive
- **M-D** · The probe protocol
- **M-E** · Git archaeology
- **M-F** · The measurement programme

---

## M-A · The spectrum in depth (1/2)

| Axis | blive | smim | P8 | datacli | harp | b-autobot | btest | seamQ |
|------|-------|------|-----|---------|------|-----------|-------|-------|
| A1 layers | 3 | 2 | 2? | 2 | 1 | 1 | 1 | 0 |
| A2 gates | 3 | 3 | 3? | 3 | 3 | 2 | 1 | 0 |
| A3 contracts | 2 | 2 | 3? | 3 | 3 | 2 | 2 | 2 |
| A4 protocol | 3 | 2 | 1? | 1 | 1 | 2 | 1 | 0 |
| A5 decisions | 3 | 2 | 2?? | 2 | 2 | 1 | 1 | 1 |
| A6 inventories | 3 | 3 | 2? | 2 | 2 | 2 | 2 | 1 |
| A7 oracles | 2 | 3 | 3? | 2 | 2 | 3 | 2 | 2 |
| A8 observability | 3 | 3 | 2? | 2 | 2 | 2 | 2 | 1 |
| **/24** | **22** | **20** | **18?** | **17** | **16** | **15** | **12** | **7** |

*`?` = inferred from the written account (P8 refreshed in-org later); `??` = the matrix's lowest-confidence cell. Two scores were adjudicated **down** in review — both against this talk's own argument.*

---

## M-A · The spectrum in depth (2/2)

**The ordering defies the naive story.** Research projects score mid-high — via **research-native** instruments:

- harp: a pre-registration with stop-for-futility rules — **a frozen intent contract**.
- smim: notation sheet + kill rules.
- seamQ: a three-persona adversarial-review pipeline — built, used, then **deliberately stripped at publication** (its 7/24 scores the stripped tree).

The boundary claim refines: exploratory work has *different substrate artifact types and lifecycle* — not no substrate.

**Inverse profiles:** b-autobot (guardrails + validation) and blive (representation + session protocol) are strong on opposite axes — the four practices are separable in practice.

---

## M-B · War stories with receipts

Four incidents, each **behind the robust number it illustrates** — n = 1 each, never aggregated:

1. **The hole named forty days before anything fell into it** *(behind the rework contrast)* — a chaos drill filled the failure-modes knowledge base (KB-7), which the project's artifact inventory had registered as MISSING — with an owner and a content contract — at the repo's **first commit**. A typed absence is a work item.
2. **The option that was not on the list** *(behind the altitude exhibit)* — an agent-drafted option set silently dropped the only intent-preserving path; the operator caught it. An option list steers by omission.
3. **One session, two defects, in the 22/24 project** *(behind the null)* — a substrate-only audit session manufactured a decision **and** deposited a claim that was never true — while citing the row that refutes it. The cheap testable fix (n=1, a proposal, not a finding): audit records carry the `file:line` each claim was read from.
4. **104,959 lines, and the reasoning is in a chat log** *(behind the retransmission tax)* — the corpus's largest deletion has a 1-byte commit body; the rationale survives only in a retained-by-accident session store. The rules were captured; the *reason* has no address.

*Three of four are the substrated project's — it is the only project with retros to read incidents from. That is a selection property of the evidence.*

---

## M-C · Session-log deep dive

**Corpus:** 1,480 turns / 168 sessions across three log stores; **1,061 classifiable operator turns**; exclusions counted.

- **Altitude instrument:** four classes, nine boundary rules, frozen after hand-labelling 99 stratified turns *before* the classifier was written. Held-out agreement 0.947 (κ = 0.902) on the high/low collapse — *one-rater stability, not IRR*. The four-way split is noisier and is not used for exhibits.
- **Warm-up detection** is prefix-based per session; paste bodies survive in only 74 of 204 paste-referencing turns → warm-up costs are floors.
- **Orientation cost is inconclusive and shown only as the honest refusal:** the substrated project produced both the *cheapest and the most expensive* orientation in the corpus (118,735 and 447,000 tokens, n=2). A 3.8× within-project spread supports no directional claim.

*Coverage caveats: the substrated project's transcripts are gone (logs start after 30 of its 70 commits); the ephemeral project's pre-methodology era has no recoverable transcript at all.*

---

## M-D · The probe protocol

**Pre-registered:** questions, scoring rubric and hypotheses frozen by commit (`ab9c62d`) **before any run**. 20 questions × 3 projects × 2 runs; fresh agent, repo-only access, isolation verified (the subject once tried to list its own memory directory — denied by the guard).

- Scoring: correct / abstained / confabulated, ties resolve **against** the hypothesis; a sensitivity reading (SC9) published alongside.
- **3 of 20 slots voided on ground-truth failure — 15% of the instrument** — every void ran *against* the hypothesis. No key edited, no answer regenerated.
- The review adopted a standing evidence rule: "we decided X" needs an artifact that **states** the decision; a diff can ground a claim about code state, never about a decision.
- The one stable orientation difference is **completeness, not cost**: the substrated project stated 4 of 4 key facts in both runs; each other project missed the *same* fact twice.

*The protocol is written to re-run unmodified inside any org, under any agent CLI — that is the work-side follow-up leg.*

---

## M-E · Git archaeology

| project | rework any-horizon | fix% | gaps ≥5d | root litter |
|---------|-----------|------|----------|-------------|
| blive | 5.2% | 10.4% | 1 | 1 |
| btest | 82.2% | 18.3% | 16 | 26 |
| b-autobot | 47.4%† | 14.0% | 0 | 0 |
| datacli | 3.7%† | 20.0% | 1 | 0 |
| harp | 0.7% | 0.0% | 1 | 0 |
| seamQ | 90.9%† | 8.0% | 0 | 1 |

*† shorter than the 14-day window — that column is whole-history rework, not fast rework; the 14-day comparison is licensed only for blive/btest/harp. Churn is a blame-free LIFO approximation; commit classes are regex-based with published precedence; every metric travels with the complexity profile.*

**Reversal narration:** the substrated project narrates its reversals (8/8 genuine on hand-read, 11.9 per 100 commits); the ephemeral one reverses 82% of its lines and narrates once in 415 commits — **shown with the prose-volume confound: 362.5 vs 62.7 words/commit; per-10k-words the automated gap is 2.1×, not 50×.**

---

## M-F · The measurement programme

The paper proposes accounting for validated intent: κ (non-derivable bits) × v (oracle-validated) × s (survived k sessions) — and a calibration gap (felt vs validated volume) as METR's finding made continuous.

**What this evaluation actually delivered of it:**

- **s(k), the survival term, is computable on a real project** — the zero-silent-reversals curve *is* s(k) for decision records, with `at_risk` denominators and a frozen definition of "silent".
- **κ was not attempted** — first in the cut order; a half-baked estimate is worse than none. No numbers exist, and none are claimed.
- The round-trip design: the instruments (rubric, probe protocol, miners — stdlib-only, portable) cross into the org; **only cleared aggregates come back**.

*Roadmap status: one data point of a research programme, honestly labelled — not a validated metric.*

---

## Appendix pointer

Every number in this deck, with its source file, honest caption and the caveat that travels:

- `research/eval/report/REPORT.md` — the argument, sections 1:1 with this deck
- `research/eval/report/exhibits.md` — the full exhibit bench (23 exhibits, 5 groups)
- `research/eval/METHODS.md` — instruments, definitions, the rules, and what the study cannot answer
- `research/eval/data/` — every extracted metric, per project

**Nothing in the bench is mandatory; nothing shown tonight is caveat-free.**
