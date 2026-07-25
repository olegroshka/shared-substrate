# Shared Substrate — Empirical Evaluation Plan

**Status:** DRAFT v0.1 — 2026-07-25
**Deadline anchor:** talk on Thursday 2026-07-30 (1h slot; flexible split — ~30 min talk +
long discussion if the room engages, up to ~55 min talk if it prefers to listen)
**Owner:** Oleg (+ Claude, in-discipline)

---

## 1. Purpose and framing

The talk is about **what human–AI-assisted work *is*** — from the conceptual level (how we
engage with information in this paradigm: the human supplying the intent and creative input
no pipeline can generate, the machine supplying expansion, a shared external substrate
carrying the state between them) down to the implementation level (how you actually practice
this day to day, and what goes wrong when you don't). The origin anecdote — being asked to
account for heavy AI-credit usage — is thirty seconds of stage-setting, no more; the thesis
it provoked is the subject: organisations that fail to move their people up the abstraction
stack, away from cognitive load and toward the creative input only humans supply, fall behind.

The evaluation's job is to ground that arc — concept to practice — in evidence from real
projects rather than conviction. Concretely, it must speak to:

1. **The paradigm claim.** In this mode of work the human's contribution should migrate up
   the abstraction hierarchy — intent, decisions, taste — while mechanical load transfers to
   the pipeline. Is that migration *visible* in real session logs and artifacts, and does the
   substrate enable it?
2. **The failure-mode claim.** Drift, phantom decisions, restart cost, reference rot are
   properties of *unsubstrated collaboration* — the paradigm, not any tool or model. Do they
   appear wherever the substrate is absent, across different tools, and respond where it is
   present?
3. **The practice claim.** Does the discipline observably change project behaviour — same
   author, same domain, same model era, with and without it?
4. **The boundary.** The paper says exploratory research is out of scope. The corpus includes
   research-nature projects to test that boundary honestly — including whether research work
   carries its *own* substrate instruments instead of none.

Posture throughout: **experience shared, not authority claimed.** Every confound is named in
the report and in the talk. The honesty is the structure, not a disclaimer.

---

## 2. Corpus

Seven local projects spanning the full spectrum of substrate adoption and project nature,
plus one work-side extension:

| # | Project | Nature | Substrate posture | Git evidence | Session logs |
|---|---------|--------|-------------------|--------------|--------------|
| P1 | **blive** | live algo-execution engine (greenfield; the discipline's origin project) | Full: CONTEXT_INVENTORY v0.26, CONTEXT_PROTOCOL, 50+ ADRs, KB/INV/DD/OQ/RETRO graph, gates, freezes, glossary | 67 commits, 2026-04-26 → 06-06 | Claude Code 56K ⚠ coverage gap — audit in WS0 |
| P2 | **btest** | backtesting/research platform, same trading domain | Flat: 212-line CLAUDE.md/AGENTS.md, no decision records, ~25 `tmp_*` files at root | 421 commits, 2025-12-09 → 2026-07-09 | Claude Code 21M |
| P3 | **b-autobot** | Java trading-blotter sprint (IdeaProjects; Maven, regression template) | Partial: CLAUDE.md, BLOTTER_DESIGN.md | 57 commits in 6 days, 2026-03-05 → 03-11 | Claude Code 28K + Copilot `jb/` store |
| P4 | **datacli** | data-ops CLI freshly extracted from btest | Light, post-methodology (SCENARIOS.md); à-la-carte case | 35 commits, 2026-07-09 → 07-19 | Claude Code 320K |
| P5 | **smim** | research project | Unknown; **git barely used (1 commit)** — itself a data point | 1 commit, 2026-05-02 | none found locally |
| P6 | **harp** | empirical research (UK/EU panel) | Research-native instruments: **pre-registration doc**, data manifest, journal plan | 11 commits, 2026-04-08 → 04-26 | none found locally |
| P7 | **seamQ** | research-paper sprint (LaTeX + ablations) | Flat | 25 commits in 3 days, 2026-05-16 → 05-18 | none found locally (seam-reproduction has CC logs) |
| P8 | **work-project rewrite** | brownfield component replacement at a regulated institution (the paper's worked example 2); **the talk's focal case** — 2 weeks, 19 gated increments, business-level parity, in UAT | Partial discipline | at work only | Copilot CLI at work |

Roles: P1 vs P2 is the central natural-experiment pair. P3 is the **local rehearsal of the
focal case** — its own design doc names it a BDD regression suite for a fixed-income blotter
with a WireMock-simulated incumbent, i.e. the "behavioural lock-in of the incumbent" practice
prototyped on personal time in March, months before it was applied to a real production
component at work; its
artifacts illustrate P8's mechanics without touching work data. P4 tests whether the
discipline's instincts persist à la carte in small greenfield work. P5–P7 are the boundary
cases for the "does not apply to exploratory research" claim — with the twist that P6's
pre-registration shows research work has its *own* substrate instruments (a pre-registration
is a frozen intent contract). P8 is the talk's focal case study (§9): its narrative and
already-stated outcome numbers carry Thursday; its instrumented measurement is the work-side
extension leg (§5). Optional: pt-liqadj (Oct 2025, an earlier research project in the same
business domain) if a pre-methodology domain baseline proves useful.

---

## 3. Evidence channels

1. **Git histories** — commits, churn, message conventions, artifact file histories.
2. **Substrate artifacts** — the artifact graphs themselves (inventories, ADR logs, retros,
   freezes) and `method/amendments-log.md` in this repo (the incident→amendment record from P1).
3. **Claude Code transcripts** — `~/.claude/projects/<munged-path>/*.jsonl`; per-session
   token counts, timestamps, turn structure. Present for P1–P4 (+ this repo).
4. **Copilot JetBrains logs** — `~/.copilot/jb/<session-uuid>/partition-N.jsonl`, 22MB total.
   Sessions are not labelled by project; WS0 maps them by grepping workspace paths.
5. **Work-side** (P8): git history + Copilot CLI logs, accessed only at work (§5).

Known gaps to audit in WS0: blive's tiny local transcript volume (sessions possibly in
claude.ai web or elsewhere); no local logs found for P5–P7.

---

## 4. Workstreams

### WS0 — Evidence audit (prerequisite)
**Question:** what evidence exists, where, and what is missing?
**Method:** map Copilot `jb/` sessions → projects; inventory Claude Code transcripts per
project (sessions, spans, token totals); record gaps explicitly in the report's methods section.
**Output:** `data/evidence-map.json` + a coverage table in the report.
**Effort:** ~half a day. **Risk:** low.

### WS1 — Adoption rubric (the spine)
**Question:** how much substrate does each project actually have?
**Method:** turn the paper's à-la-carte menu into a scored instrument — ~8 axes, 0–3 each,
**grouped under the talk's four advertised practices** so every eval output speaks the
abstract's vocabulary:
1. *Structural decomposition* — abstraction layers · gated increments/milestones
2. *Explicit guardrails* — behavioural contracts & budgets · edit protocol/constraints
3. *System representation* — stable IDs + decision records · inventories/DDs/glossary
   (single source of truth)
4. *Continuous validation* — oracle-per-layer with tests in the loop · observability-to-agent
Score P1–P7 from artifacts; score P8 provisionally from memory, marked PROVISIONAL until
refreshed at work.
**Output:** `rubric/RUBRIC.md` (instrument), `data/rubric-scores.json`, one comparison chart;
plus a **one-page audience handout** version ("score your own project") for the interactive
segment of the talk.
**Effort:** ~half a day. **Risk:** circularity — the rubric measures adoption, not effect;
it must always be presented alongside WS2/WS4 outcomes.

### WS-X — Complexity profile (cross-cutting; feeds WS1–WS5 interpretation)
**Question:** how complex is each project — so that no cross-project comparison is read
without it, and so the corpus can test the paper's own moderator claim (the discipline pays
off only *above* a complexity threshold; below it, flat notes win).
**Metric choice, stated honestly:** there is no single reputable "project complexity"
metric — code-level metrics aggregated to project level mostly recapitulate size (Shepperd
1988; El Emam et al. 2001), and composite indices with invented weights are methodologically
frowned upon. The defensible design is a **vector of established primitives, never collapsed
into a scalar**, leaning on the process-metrics literature (change entropy: Hassan, ICSE
2009; churn: Nagappan & Ball 2005; process ≥ code metrics: D'Ambros et al. 2010), which is
cross-language and computable from git alone.
**Method:** per project, two parts:
(a) **Objective vector** (stdlib script, git + files), exact definitions:
   - *Size:* non-blank LOC over `git ls-files` source files; file count; language count.
   - *Change entropy* (Hassan 2009): H = −Σ pᵢ log pᵢ over the distribution of commits'
     file changes, normalised by log n; full-history and per-quarter.
   - *Coordination scope* — *the paper's own threshold construct (sessions, decisions,
     collaborators), measured directly:* duration · session count (WS0 evidence map) ·
     distinct directories touched per active month · decision count where records exist.
   - *Dependency count:* direct dependencies parsed from pyproject.toml / pom.xml.
   - *Algorithmic information (AIT):* LZMA-compressed size of the concatenated tracked
     source files (sorted paths, pinned compressor + preset for reproducibility) as a
     practical **upper-bound estimator of Kolmogorov complexity** (Kolmogorov 1965; Li &
     Vitányi; the compression-distance tradition of Cilibrasi & Vitányi 2005) · plus the
     compression ratio as a redundancy indicator. Complements LOC: raw volume counts
     boilerplate, compressed size approximates information content, so repetition-inflated
     codebases rank lower here than by LOC. Language-agnostic by construction. *Not to be
     conflated with WS5's kernel:* WS5 estimates *conditional* complexity of deposits given
     the substrate, K(x | S), via LLM log-loss (Delétang et al. 2023); WS-X measures plain
     project-level K(repo) by classical compression — related quantities, different
     estimators, different questions.
   No cyclomatic/Halstead aggregation: language-bound tooling breaks cross-language
   comparability, and the size-confound critique applies.
   **Robustness check instead of weights:** report rank concordance (Kendall's W) of the
   project ordering across all primitives — the moderator analysis stands only on orderings
   stable under every metric, so no weighting choice is load-bearing.
(b) **Declared qualitative ratings** (0–3 each, criteria stated, honestly labelled as author
judgment in the COCOMO cost-driver tradition; used for narrative placement only, never in
computation): integration surface (external APIs, brokers, gateways) · constraint tightness
(latency, parity, regulatory) · statefulness/concurrency.
**Use:** every WS2/WS3 metric is reported *alongside* the complexity profile (rates, not
absolutes, wherever possible); the headline cross-project exhibits plot substrate adoption ×
complexity × outcome, so "does the substrate matter?" can be answered the way the paper
predicts — *increasingly, with complexity*. The audience handout gets a complexity check for
the same reason: "below the threshold, flat notes are fine" is part of the honest message.
**Output:** `scripts/complexity_profile.py`, `data/complexity-profiles.json`, one table in
the report; a complexity row under the rubric chart.
**Effort:** ~half a day, mostly shared with WS2. **Risk:** the qualitative ratings are the
author rating his own projects — mitigated by publishing the criteria and the underlying
objective numbers next to them.

### WS2 — Git outcome proxies
**Question:** do adoption differences co-occur with different observable project behaviour?
**Method:** one portable miner script (Python, stdlib-only, git-only) computing per repo:
short-horizon churn (code rewritten within N days — rework proxy), fix/revert commit ratio,
re-fix recurrence (same files patched for fixes repeatedly), commit-gap recovery patterns
(what the first commits after a ≥5-day gap do), root-directory hygiene (untracked litter),
test-count trajectory.
**Output:** `scripts/git_miner.py`, `data/git-metrics/*.json`, small multiples chart.
**Effort:** ~1 day. **Risk:** heavy confounds (project nature, age, model era, author
learning). Reported as *texture, not proof*; confounds ledger is mandatory (§7).

### WS3 — Session-log analysis: operator altitude and the retransmission tax
**Question:** what is the *human* actually doing in these sessions — and how much of the
machine's work is re-derivation of state that should have been stored?
**Method:** parse Claude Code + Copilot JSONL into a common session schema (project, start/end,
tokens in/out, turns; human turns extracted verbatim). Then three analyses:
(a) **Operator altitude** — classify each human turn by the abstraction level it operates at:
intent/goal declaration · decision/trade-off resolution · design/contract shaping ·
mechanical steering (paste this error, fix that line, re-explain context). Compare the
distribution across substrate postures and over each project's lifetime. This is the direct
test of the paradigm claim: in substrated work the human's turns should concentrate at the
top; in flat work they should be dragged down into mechanics. The migration itself —
if visible in P2→P1→P4 chronology — is the talk's central exhibit.
(b) **Warm-up fraction / retransmission tax** — classify each session's early turns as
context reconstruction vs new work; compare across substrate postures. The paper predicts
substrated projects pay a bounded warm-up cost; flat projects pay an unbounded, recurring one.
(c) **Volume vs durable yield** (supporting, not headline) — link sessions to the
commits/artifacts they produced and whether those survived k sessions; a `V/I`-style
calibration ratio per project, connecting to the paper's felt-vs-validated productivity gap.
**Output:** `scripts/log_miner.py`, `data/session-metrics/*.json`; headline figure: the
altitude distribution per project, side by side with its rubric score.
**Effort:** 1.5 days. **Risk:** turn-classification is the crux — build a small labelled
sample by hand first, report agreement; coverage gaps (WS0) may limit P1's session evidence.

### WS4 — Phantom-decision probe (pre-registered mini-experiment)
**Question:** does the substrate measurably reduce confabulation and orientation cost?
**Method:** ~20 questions per project with checkable ground truth ("did we decide X?",
"what is the current state of Y?", "why was Z rejected?") for P1, P2, P3. Freeze the question
list and scoring rubric **by commit before any run** (pre-registration; the commit hash is the
timestamp). Run fresh agent instances per project; score answers correct / abstained /
confabulated; separately measure orientation cost (turns/tokens until the agent correctly
states project status).
**Output:** `probes/PROTOCOL.md`, `probes/questions-{p1,p2,p3}.md` (frozen),
`data/probe-results.json`, the confabulation-rate bar chart — the talk's one controlled number.
**Effort:** ~1.5 days incl. question design. **Risk:** small n; selection bias countered by
pre-registration. Local runs use one model (Claude); the protocol file is written so the
identical probe reruns under Copilot CLI at work (P8) — cross-tool replication, later.

### WS5 — Decision survival + kernel teaser
**Question:** is the paper's accounting computable on a real project?
**Method:** (a) **Survival curves** from P1 git history: fraction of ADRs / KB entries /
frozen artifacts surviving k subsequent sessions without silent reversal; contrast with
decision-reversal archaeology in P2 commit messages. (b) **Kernel teaser** (stretch, cut
first): estimate κ(x) ≈ −log p(x | S) via LLM scoring for 3–5 blive deposits conditioned on
the prior substrate snapshot.
**Output:** `scripts/survival.py`, `data/survival.json`, survival-curve figure; kernel numbers
only if they are defensible.
**Effort:** survival ~half a day; kernel ~1 day (stretch). **Risk:** kernel estimation
half-baked is worse than absent — it ships only as "first data point of the research
programme," or not at all.

### WS6 — Drift archaeology (the war stories)
**Question:** what actually went wrong, and which discipline element exists because of it?
**Method:** pair every element in `method/amendments-log.md` and P1's retros with the concrete
incident that forced it (chaos drill → KB-7; the leverage trilemma → ADR-052/OQ-032; the
`AccountSnapshot.equity` bug → DD-1 v0.3). Mirror hunt in P2: incidents with no capture
mechanism, left as scar tissue (tmp-file litter, CLAUDE.md accretion, re-explained context,
re-fixed bugs found in WS2).
**Output:** `report/war-stories.md` — 3–4 stories with receipts (commits, artifact diffs).
**Effort:** ~1 day of reading, parallelisable with report drafting. **Risk:** anecdotal by
construction; motivates, does not prove — placed accordingly in the talk.

---

## 5. Work-side extension protocol (P8, after the talk)

P8 lives in an **isolated corporate environment**: its code, git history, and session logs
are accessible only inside the org, and nothing in this repo or on this machine ever touches
them directly. The enrichment leg of this research therefore runs as a **round-trip through
this repo**:

1. **Outbound — instruments via this repo.** Everything under `research/eval/` (this plan,
   the rubric, the probe protocol, the miner scripts) is pushed to the public shared-substrate
   repo and is the *only* thing that crosses into the org — pulled or brought in there through
   the approved channel. The artifacts are written to be self-sufficient: anyone (Oleg with
   Copilot CLI, or a colleague) can run the identical protocol inside the org with no
   dependency on this machine.
2. **In-org enrichment run.** The same workstreams execute against P8's real git history and
   Copilot logs, inside the corporate environment, with GitHub Copilot CLI as the agent
   harness. Raw outputs stay there as a private work-side annex.
3. **Inbound — cleared aggregates only.** Only anonymised aggregate metrics, cleared per
   employer policy, merge back into the public report here.

Constraints that make the round-trip possible:

- **Portability:** all scripts stdlib-only Python operating on git + files;
  no network, no model calls except WS4 (which goes through whatever agent CLI is available);
  rubric and probe protocol are plain-markdown instruments.
- **Data hygiene (non-negotiable):** nothing leaves the work environment except aggregate
  metrics — counts, ratios, curves. No code, no paths, no identifiers, no business terms.
  The raw annex stays at work; only cleared aggregates merge into the public report, with the
  project described only as "a component rewrite at a regulated financial institution."
  Clearance per employer policy before anything is pushed.
- **Talk vs public report:** the talk is internal at work — P8 specifics already stated in
  the circulated abstract (component name, increment count, parity, UAT status) are fine *in
  the room*. The public GitHub report is the stricter surface: there P8 appears only as
  "work-project" with anonymised aggregates — no employer name, no component name.
- **Sequence:** talk (Jul 30) presents the P8 case study + P1–P7 evidence + provisional P8
  rubric score; the work leg then refreshes P8 with real git/log data as the research continues.

## 6. Deliverables and repo layout

```
research/eval/
├── PLAN.md                  # this document
├── rubric/RUBRIC.md         # WS1 instrument + audience handout section
├── probes/                  # WS4: protocol + frozen question sets
├── scripts/                 # WS2/WS3/WS5 miners — stdlib-only, portable
├── data/                    # extracted metrics (JSON/CSV) per project
└── report/
    ├── REPORT.md            # the research report; sections map 1:1 to talk sections
    └── war-stories.md       # WS6
```

Pushed to the public GitHub repo (local projects' *metrics and excerpts* only — P1–P7 are
Oleg's personal projects; P8 per §5). This tree doubles as the **portable kit** the §5
round-trip carries into the corporate environment: instruments and scripts are written to run
there unmodified, which is why `data/` keeps extracted metrics strictly separate from the
instruments that produce them.

**Talk material lives separately** in `talks/does-the-substrate-matter/`
(abstract, outline, deck, handout, speaker notes) — one folder per talk, so future
talks slot in alongside. `docs/presentation.md` remains the *general method* walkthrough, a
different presentation the talk borrows from but does not replace. The talk folder consumes
this report's exhibits; it is **not** part of the §5 portable kit — only `research/eval/`
crosses into the org.

## 7. Confounds ledger (named in the report and in the talk)

1. **No controls:** P1 vs P2 differ in nature (production engine vs research platform), age,
   and model era. Case comparison, not experiment — except WS4, which is controlled.
   Partially mitigated by WS-X: every comparison is reported against the projects'
   complexity profiles, and complexity is treated as the theory's own moderator rather than
   left as an unmeasured nuisance.
2. **Learning effect:** the author was more experienced by the time P1 existed; discipline
   and skill co-evolved.
3. **Selection:** projects chosen by the person evaluating their own methodology; countered by
   pre-registration (WS4), by including boundary cases expected *not* to show the effect
   (P5–P7), and by publishing the raw extraction scripts.
4. **Instrument circularity:** the rubric operationalises the author's own method (WS1 risk).
5. **Log coverage:** uneven transcripts (P1 gap; P5–P7 none found locally) — reported, not
   patched over.

The METR result (experienced devs 19% slower while feeling 20% faster) is the standing
reminder that felt productivity is untrustworthy — including the author's own. This ledger is
what distinguishes the talk from advocacy.

## 8. Timeline (Sat 07-25 → Thu 07-30)

| Day | Work |
|-----|------|
| **Sat** | Lock this plan · WS0 evidence audit · WS1 rubric v1 drafted |
| **Sun** | WS2 git miner + run on P1–P7 · WS3 parsers for both log formats, first extraction |
| **Mon** | WS1 scoring pass (all projects; P8 provisional) · WS5 survival curves · **WS4 pre-registration commit** (questions frozen) |
| **Tue** | WS4 probe runs + scoring · WS3 spend-vs-yield accounting · WS6 archaeology · report drafting |
| **Wed** | Report freeze · talk deck (core arc + expansion modules + appendix bench) · dry run of the branch points, not a fixed script |
| **Thu** | Talk |

Cut order under time pressure: WS5 kernel teaser first, then WS3(c), then WS4 shrinks to
P1-vs-P2 only, then WS2 drops to the three cheapest metrics. WS1, WS3(a–b), WS6 and the
report are not cut.

## 9. Talk shape (flexible core + expansion modules; no hard timeboxes)

Advertised as: **"Does the substrate matter?"** — a candid case study of the work-project
re-engineering (2 weeks, 19 gated increments, business-level parity, running in UAT),
organised around four engineering practices, examining the felt-faster/delivered-slower
research, honest about what the experiment supports and where evidence remains uncertain.
The arc follows the abstract; the conceptual frame is the interpretive thread inside it, and
the local corpus is the answer to the n=1 objection.

**Design principle: the room sets the length, the deck flexes.** A core arc (~30 min) that
is complete on its own, plus optional deep-dive modules that expand it toward ~55 min if the
audience prefers listening; the interactive segment is the elastic buffer, growing when the
room engages and shrinking when it doesn't. Every workstream delivers its figures
**presentation-ready** into an appendix bench — many numbers available on demand, none
mandatory. Nothing is committed to a clock; the dry run rehearses the *branch points*, not a
fixed script.

**Core arc:**

1. **The case, cold:** the work project in two weeks — what was delivered, under what
   constraints. Then the question the room should hold: this wasn't model magic; what
   actually carried it? *Does the substrate matter?*
2. **The frame in one slide:** what this kind of work *is* — the human supplies intent,
   decisions, taste (the creative kernel); the pipeline supplies expansion; a shared external
   substrate carries the state between sessions, tools, and minds.
3. **Four practices, each told the same way** — *what we did on the work project → the concept
   underneath (one aphorism, one figure) → does it generalise (exhibit from the personal
   corpus):*
   - **Structural decomposition** — 19 gated increments; layers as the shortest description
     first. Corpus: blive's M0→M3 gate record.
   - **Explicit guardrails** — behavioural lock-in of the incumbent, budgets from the live
     system; *"gain is indifferent to sign."* Corpus: b-autobot — the same lock-in rehearsed
     on personal time in March.
   - **System representation** — the substrate itself: decision records, inventories, stable
     IDs; *"drift is excursion without reversion."* Corpus: the phantom-decision probe result
     (pre-registered) + the ADR survival curve.
   - **Continuous validation** — parity as oracle, checks in the loop; *"an oracle the agent
     cannot query is an audit, not a guardrail."* Corpus: test trajectories and rework rates
     across substrate postures.
4. **The research, examined:** METR −19% vs felt +20%; +26% field; +56% greenfield; the
   substrate-shaped moderators that reconcile them. What this experiment supports, where the
   evidence remains uncertain — the confounds ledger, out loud. Closing exhibit: the
   operator-altitude distribution — where the human's attention actually went, measured from
   real session logs.
5. **Interactive (elastic):** audience scores their own project on the one-page
   four-practices rubric; moderated discussion of the spread — where is *your* work on the
   altitude scale?

**Expansion modules (pulled in as the room's appetite dictates, any order):**

- **M-A · The seven-project spectrum in depth** — full rubric matrix walk-through, project by
  project, including the research-nature boundary cases (P5–P7) and what they say about where
  the discipline does *not* apply.
- **M-B · War stories with receipts (WS6)** — the chaos drill that became KB-7; the leverage
  trilemma (ADR-052/OQ-032); the `AccountSnapshot.equity` bug; btest's scar tissue.
- **M-C · Session-log deep dive (WS3)** — warm-up/retransmission tax across projects;
  volume-vs-durable-yield calibration ratios; methodology of the altitude classifier.
- **M-D · The probe protocol (WS4)** — how the phantom-decision experiment was pre-registered
  and run; full per-question results; orientation-cost curves.
- **M-E · Git archaeology (WS2)** — churn half-lives, re-fix recurrence, gap-recovery
  patterns; the confounds each metric carries.
- **M-F · The measurement programme (WS5 + paper §)** — survival curves in full; the
  kernel/accrual/net-rate accounting and its first data points; the research roadmap.
