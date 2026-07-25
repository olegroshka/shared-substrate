# Substrate Adoption Rubric — v1

**Status:** DRAFT v1.0 — 2026-07-25 · WS1 instrument (see [PLAN.md](../PLAN.md) §4)
**Purpose:** score how much substrate discipline a project actually practises — eight axes,
two per practice, 0–3 each. Used three ways: (1) to place the eval corpus on a common scale,
(2) as the audience self-assessment handout (§4), (3) re-runnable inside any org on any repo.

Scores measure **adoption, not effect** — pair with outcome evidence (PLAN WS2–WS5) and read
against the project's complexity profile (PLAN WS-X). The discipline predicts its own
irrelevance below a complexity threshold: a low score on a simple project is *correct
practice*, not a deficiency.

## 1. Scoring scale

| Score | Generic anchor |
|-------|----------------|
| 0 | Absent — no trace of the practice |
| 1 | Ad hoc — implicit traces, inconsistent, exists only in someone's head or scattered notes |
| 2 | Present — deliberate artifacts exist but partial, irregularly maintained, or unenforced |
| 3 | Systematic — maintained, enforced, load-bearing; the project would notice its absence |

Score from artifacts and history, not from intention or memory. Cite evidence per axis
(file paths, commit examples); an axis with no citable evidence scores at most 1.

## 2. The eight axes

### Practice I — Structural decomposition

**A1 · Abstraction layers.** Are intent, requirements, design, and implementation held in
*distinct artifacts* with explicit propagation between them?
- 0: one blob (or code only) · 1: a README mixing all levels · 2: separate docs exist but
  drift silently · 3: explicit hierarchy; changes cascade down in the same change-set, and
  upward only via a recorded decision.
- *Evidence:* requirements/design docs distinct from code; documented cascade rules.

**A2 · Gated increments.** Does work advance in bounded increments with explicit exit
criteria?
- 0: continuous undifferentiated flow · 1: informal milestones ("v2 vibes") · 2: named
  milestones, fuzzy exit criteria · 3: gates with checkable criteria, pass/fail recorded,
  state frozen at closure.
- *Evidence:* milestone/readiness records, gate checklists, freeze snapshots.

### Practice II — Explicit guardrails

**A3 · Behavioural contracts & budgets.** Is intended behaviour locked in executable form,
and are non-functional envelopes (latency, memory, throughput) captured as budgets?
- 0: behaviour lives in heads · 1: prose descriptions only · 2: partial executable specs on
  some components · 3: executable contracts on the critical surface + measured budgets
  asserted against.
- *Evidence:* feature/BDD files, contract tests, budget assertions, incumbent
  instrumentation.

**A4 · Edit protocol & change discipline.** Are there documented rules for changing shared
knowledge artifacts — single-source-of-truth enforcement with a cheap trivial-fix lane?
- 0: edit anything anytime · 1: conventions in the author's head · 2: written rules,
  irregularly followed · 3: protocol followed and checkable, with an explicit trivial lane
  so ceremony never exceeds benefit.
- *Evidence:* a protocol document; edits that visibly follow it; impact checks.

### Practice III — System representation

**A5 · Decision records & stable identifiers.** Are decisions captured append-only, one
record each, and are cross-references made by stable ID rather than path or paraphrase?
- 0: decisions in chat scrollback · 1: some decisions in commit messages/READMEs · 2: a
  decision log, kept irregularly, refs by paraphrase · 3: append-only records with stable
  IDs (ADR-12) used in docs *and* commits; silent reversal impossible.
- *Evidence:* ADR files/log; ID usage in cross-refs and commit messages.

**A6 · Inventories, dictionaries, glossary.** Do single-source-of-truth artifacts exist for
lists, schemas, and terminology, with a status lifecycle?
- 0: none · 1: scattered partial lists · 2: inventories/schemas exist, freshness unknown ·
  3: exhaustive inventories + data dictionaries + a glossary, each carrying status
  (DRAFT/STABLE/STALE) with triggered transitions.
- *Evidence:* inventory/DD/glossary files; status tags actually changing over history.

### Practice IV — Continuous validation

**A7 · Oracle per layer.** Does every abstraction layer have a verification check stronger
than "looks right," run continuously rather than at the end?
- 0: manual inspection only · 1: some unit tests · 2: solid tests at one layer, others
  unchecked · 3: layer-appropriate oracles (acceptance runs, contract tests, compiler/types,
  budget assertions) wired into the loop; parity vs an incumbent where one exists.
- *Evidence:* test suites per layer, CI/gate configs, parity/regression harnesses.

**A8 · Observability & session protocol.** Can the *agent* observe the work's state cheaply
(checks, metrics, traces it can run itself), and do sessions start from a warm-up and end
with a handoff deposit?
- 0: agent flies blind; every session cold-starts · 1: agent can run tests if it thinks to;
  restart context re-explained each time · 2: documented entry points or a pointer file, used
  inconsistently · 3: agent-runnable checks + a maintained warm-up/handoff artifact; a
  crashed session resumes like a clean one.
- *Evidence:* agent instruction files pointing at runnable checks; NEXT_PROMPT/state files;
  session-log or retro artifacts.

## 3. Scoring sheet

| Axis | P1 blive | P2 btest | P3 b-autobot | P4 datacli | P5 smim | P6 harp | P7 seamQ | P8 work |
|------|---------|---------|--------------|-----------|---------|---------|----------|---------|
| A1 layers | 3 | 1 | 1 | 2 | 2 | 1 | 0 | 2? |
| A2 gates | 3 | 1 | 2 | 3 | 3 | 3 | 0 | 3? |
| A3 contracts | 2 | 2 | **2** | 3 | 2 | 3 | 2 | 3? |
| A4 protocol | 3 | 1 | 2 | 1 | 2 | 1 | 0 | ? |
| A5 decisions | 3 | 1 | 1 | 2 | 2 | 2 | 1 | ? |
| A6 inventories | 3 | 2 | 2 | 2 | 3 | **2** | 1 | ? |
| A7 oracles | 2 | 2 | 3 | 2 | 3 | 2 | 2 | 3? |
| A8 observability | 3 | 2 | 2 | 2 | 3 | 2 | 1 | ? |
| **Total /24** | **22** | **12** | **15** | **17** | **20** | **16** | **7** | prov. |

Ranking: blive 22 · smim 20 · datacli 17 · harp 16 · b-autobot 15 · btest 12 · seamQ 7.

Scores are **v1.1-REVIEWED** (2026-07-25), assigned by Claude from the repo sweeps in
`../data/rubric-evidence.md`, with the four flagged judgment calls adjudicated in session
S2; per-axis notes and the full review log in `../data/rubric-scores.json`. Two calls moved
(**bold** above): b-autobot A3 3→2 (executable contracts yes, but budgets are config
comments, not values asserted against — the same deficiency that held blive A3 to 2) and
harp A6 3→2 (exhaustive manifest and schema dictionary, but no glossary artifact and no
artifact status lifecycle). Both moved *against* the talk's own argument, which is the
direction a self-authored instrument should be willing to move. Two calls were upheld:
blive A8=3 and smim A3=2.

P8 is PROVISIONAL (from the paper's worked example 2) and its four blanks are **not
fillable from any artifact reachable outside the org** — the paper is silent on edit
protocol, decision records and inventories for that project. One anchor for scoring A8
when refreshed: the paper does evidence the observability half ("budgets … queryable
in-loop so that a violation surfaced during implementation rather than at review") but says
nothing about a session protocol. P7 scores the *current, deliberately stripped* tree — its
pre-publication history (session warm-up doc, weekly gates, adversarial-review pipeline)
would score far higher; see evidence notes.

## 4. Audience handout — score your own project (one page)

**Does the substrate matter — for *your* project?** Two minutes, honest answers.

**Step 0 — complexity check.** Count roughly: sessions or people involved · months of life ·
decisions that could be silently reversed · external systems integrated. If everything is
small — days of work, one person, few decisions — **stop: flat notes are the right tool.**
The discipline starts paying above that line.

**Step 1 — score 0–3 per question** (0 absent · 1 in someone's head · 2 written but partial ·
3 maintained and load-bearing):

1. Are intent, requirements, design, and code in *separate* artifacts that update in a
   known order? *(layers)*
2. Does work move through gates with checkable exit criteria? *(increments)*
3. Is intended behaviour executable — tests/contracts that fail when meaning drifts — with
   performance budgets written down? *(guardrails)*
4. Are there rules for changing shared docs — and a cheap lane for trivial fixes? *(protocol)*
5. Could you answer "did we decide X, and why?" from an append-only record with stable IDs —
   not from memory or chat scrollback? *(decisions)*
6. Is there one authoritative list/schema/glossary per kind of fact, with a freshness
   status? *(representation)*
7. Does every level have a check stronger than "looks right," running continuously?
   *(validation)*
8. Can your AI assistant *itself* check the state of the work — and does each session start
   from a written warm-up instead of your re-explanation? *(observability)*

**Step 2 — read your total /24.** 0–6: unsubstrated — expect drift, phantom decisions, and
Monday restart cost in proportion to complexity. 7–14: partial — you likely already feel
where it leaks; adopt the one missing element that hurts most (each pays back alone).
15–24: substrated — your bottleneck is elsewhere: intent quality and oracle capacity.

*Where does your attention go in AI sessions — declaring intent and making decisions, or
pasting errors and re-explaining context? That difference is what these eight questions
predict.*
