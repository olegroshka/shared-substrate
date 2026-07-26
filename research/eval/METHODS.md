# Methods — how this evaluation was done, and what it may be trusted for

**Status:** v1.0 — 2026-07-26, after S6 (WS0–WS5 + the survivorship audit complete).
**Scope:** method only. *Findings* live in [STATE.md](./STATE.md); *what the evidence
argues* lives in [ASSESSMENT.md](./ASSESSMENT.md); *the plan and its confounds ledger*
live in [PLAN.md](./PLAN.md). This file is the one to read first if you want to judge
the work, replicate it, or run it somewhere else.

---

## 1. The question

Does a shared external substrate — decision records, inventories, stable IDs, session
protocols — measurably change how human–AI collaborative work goes? Evaluated over
eight real projects by one author, using evidence that already existed rather than
evidence generated for the study.

Four sub-claims, from PLAN §1: does the human's attention migrate up the abstraction
stack · do drift/restart-cost/reference-rot follow the *absence* of substrate · does
the discipline change project behaviour with author and domain held fixed · does the
"not for exploratory research" boundary hold.

---

## 2. Corpus

Eight projects, chosen to span substrate postures *and* project natures, including
cases expected **not** to show the effect.

| | project | nature | posture | git |
|---|---|---|---|---|
| P1 | blive | live algo-execution engine | full: 53 ADRs, inventories, gates, freezes | 67 commits, 41d |
| P2 | btest | backtesting platform, same domain | **ephemeral**: 212-line CLAUDE.md, no decision records | 415 commits, 213d |
| P3 | b-autobot | Java trading-blotter sprint | partial: CLAUDE.md + design doc | 57 commits, 6d |
| P4 | datacli | CLI extracted from btest | light, post-methodology | 35 commits |
| P5 | smim | research | 1 squashed commit — itself a data point | 1 commit |
| P6 | harp | empirical research | research-native: pre-registration, manifest | 11 commits |
| P7 | seamQ | paper sprint | substrate stripped at publication | 25 commits, 3d |
| P8 | work project | brownfield rewrite, regulated institution | partial | in-org only (§8) |

P1-vs-P2 is the central pair: same author, same domain, same model era. P5–P7 are the
boundary cases. P8 is the talk's focal case and is measured only inside the org.

**"Ephemeral", not "flat".** P2's substrate was not absent — at least 26 working
artifacts existed and never reached git (§5.8). Every comparison in this eval uses that
word.

---

## 3. Evidence channels

| channel | coverage | boundary |
|---|---|---|
| git histories | all 7 local repos | P5's history is squashed to 1 commit — reported `n/a: history lost`, never 0 |
| substrate artifacts | committed files only | see §5.8 — the surviving subset, not what was practised |
| Claude Code transcripts | recent window only (retention) | blive's sessions are **gone**; btest 4 sessions Jul 6–16 |
| Claude Code history.jsonl | **every user prompt since 2026-03-03** | human turns only; no assistant side |
| Copilot JetBrains store | Mar 20 – May 31 | no token fields; 48 of 57 sessions carry only machine-composed briefs |

Consolidated: **1,480 turns across 168 sessions**, of which **1,061 are classifiable
operator turns**. Slash commands, machine-rendered briefs, off-project and
unrecoverable-paste turns are excluded **and counted**.

Two coverage facts that constrain every session-based claim: btest's Dec 2025 – Feb 2026
era used JetBrains AI Assistant, which keeps no recoverable transcript; and blive's
session logs start 2026-05-02, after 30 of its 70 commits.

---

## 4. Instruments — frozen before use

Five plain-markdown instruments, each written and frozen *before* the measurement it
governs, so the scoring rule could not be tuned to the data.

| instrument | governs | shape |
|---|---|---|
| `rubric/RUBRIC.md` | WS1 adoption | 8 axes × 0–3, grouped under four practices; anchors per axis; **scope statement**: scores *durable* substrate only |
| `rubric/ALTITUDE.md` | WS3 turn classification | 4 classes, 9 numbered boundary rules, fixed precedence; frozen after hand-labelling, before the classifier was written |
| `probes/PROTOCOL.md` | WS4 experiment | subject model, isolation rules H1–H9, scoring rules SC1–SC10, one pre-registered test, published sensitivity reading |
| `probes/questions-p{1,2,3}.md` | WS4 items | 20 questions × 3 projects on one fixed slot template (7 decide / 7 state / 6 why) |
| script docstrings | WS2, WS-X, WS5, WS0-bis | each metric's definition, approximations and known biases, echoed into every output's `_meta.definitions` |

**WS4 was pre-registered by commit.** `ab9c62d` (2026-07-25 23:57 +0100) contains
exactly the four instrument files, with nothing run. The commit hash is the timestamp.

---

## 5. Measurements

Thirteen scripts, all **stdlib-only**, all **read-only** on the target repos
(`git --no-optional-locks`), all **path-parameterised**. `corpus_common.py` holds the
single shared definition of a "source file", a vendored path and a project, so no two
miners can drift apart on what they are counting.

**5.1 · WS0 evidence audit** — `evidence_audit.py` → `data/evidence-map.json`.
What logs exist, where, and what is missing.

**5.2 · WS1 adoption rubric** → `data/rubric-scores.json` + `data/rubric-evidence.md`.
Hand-scored from artifacts with a citation per axis; an axis with no citable evidence
scores at most 1. Four flagged judgment calls were adjudicated in a separate review
pass; two moved *down*, both against the hypothesis.

**5.3 · WS-X complexity profile** — `complexity_profile.py` → `data/complexity-profiles.json`.
A **vector of established primitives, never collapsed into a scalar**: non-blank LOC,
file/language counts, Hassan change entropy, coordination scope, dependency counts, and
LZMA-compressed size as a Kolmogorov upper-bound estimator. Robustness is reported as
Kendall's W across primitives rather than by choosing weights. Qualitative ratings are a
**published input file**, excluded from every computation.

**5.4 · WS2 git outcome proxies** — `git_miner.py` → `data/git-metrics/*.json`.
Seven metrics: short-horizon churn, fix/revert ratio, re-fix recurrence, gap recovery,
root hygiene, test trajectory, stable-ID prefix timeline. Churn is a **blame-free LIFO
approximation** over `git log --numstat -M`; its biases are stated in the docstring and
carried into every output.

**5.5 · WS3 session-log analysis** — `log_miner.py` · `sample_turns.py` ·
`altitude_classify.py` · `session_yield.py` → `data/session-metrics/*.json`.
Three log formats into one schema, with content-and-window project re-attribution
(rules frozen as an input file). 99 turns were hand-labelled **before** the classifier
existed. Agreement on a pre-assigned held-out split: **0.895 four-way (κ=0.835)**,
**0.947 high-vs-low (κ=0.902)**. The pre-fix run is published alongside. This is
instrument *stability*, not inter-rater reliability — there is one rater. The four-way
split is noisy, so **every exhibit is built on the high/low collapse**.

**5.6 · WS4 phantom-decision probe** — `probe_driver.py` · `probe_guard.py` ·
`probe_results.py` → `data/probe-results.json`, verdicts in `data/probes/scores.json`.
Six sessions (2 runs × 3 projects), 120 answers. The driver extracts every frozen text
and question **from the instrument files at run time**, so no probe text was retyped and
no answer key entered a session. A guard hook enforced read-only repo access; it denied
the subject's attempt to list its own memory directory, which is the isolation evidence.
Three harness deviations are declared in the output rather than hidden.

**5.7 · WS5 decision survival** — `survival.py` → `data/survival.json`, hand findings in
`data/survival-audit.json`.
The definition of **silent reversal** was frozen in the script docstring before the
measurement was written, and it is the whole workstream: a *declared* reversal (status
moves to `SUPERSEDED-BY-*`, or a later record carries `supersedes:`, or the body is
edited to state the change) is the discipline **working** and is never counted as a
failure; only an undeclared contradiction counts. Machine-checkable defects
(index/body incoherence, supersession backlinks, reference and anchor integrity) are
computed; decision-reversal and fact-drift require reading and come from the audit input.

**5.8 · WS0-bis artifact survivorship** — `artifact_survivorship.py` →
`data/artifact-survivorship.json`.
Added after the operator disclosed that working artifacts were routinely created,
uncommitted and deleted. Three independent channels — typed prompts, JetBrains
LocalHistory change records, agent tool-call paths — against every `.md` basename any
corpus repo ever added on any ref. Measures the **gap**; does not close it. Existence is
recoverable, content is not, so **WS1 is not re-scored** (§6, rule 8).

---

## 6. Rules that govern the whole evaluation

These are the reason the numbers can be argued with. Each was adopted at a specific
point and then applied backwards.

1. **Pre-register what can be pre-registered.** WS4's questions, scoring rubric and
   hypothesis were frozen by commit before any run. The result came back **null** and is
   published as it came out.
2. **Author judgment is a published input file, never a computed output.** Qualitative
   complexity ratings, probe verdicts, attribution overrides and the WS5 hand audit all
   live in `data/*.json` files that scripts *read*. A re-run can never silently overwrite
   a judgment call, and can never silently invent one.
3. **Hand-verify before every sweep.** At least two computed numbers per workstream are
   reproduced by an independent shell count and recorded in `_meta.verification`. It has
   caught a real bug in **every workstream that used it** — 3 in WS2/WS-X, 2 in WS3, 4 in
   WS5, 2 in WS0-bis — including a tag regex that read btest at 110 instead of 293, an ID
   pattern that manufactured 71 phantom dangling references, and a slug rule that called
   758 of 900 links broken against a true 26. The count is published per workstream
   rather than as a total, because "11 bugs" invites the wrong question; the useful fact
   is that the reflex has never once come back clean on a first draft.
4. **Void and report.** When ground truth turns out not to hold, the item is withdrawn
   and the withdrawal published. No key is edited, no question replaced, no answer
   regenerated. Three of twenty probe slots were voided this way — 15% of the instrument
   — and every void ran *against* the hypothesis.
5. **Tier A/B evidence.** A claim that "we decided X" must rest on an artifact that
   **states** the decision. A decision *inferred* from a diff, rename or config change
   may ground a claim about the **state of the code**, never about a decision.
6. **Declared is not failed.** In an append-only substrate, a supersession, a frozen
   retro and a registered-MISSING artifact are the discipline working. Counting them as
   drift would measure the opposite of the subject.
7. **`n/a` is not zero.** A project without the thing being measured is flagged, not
   scored 0 — smim's lost history, btest's absent decision records, seamQ's window
   shorter than the metric's window.
8. **Do not correct a score you cannot evidence.** Where content is unrecoverable, the
   gap is published as a confound and the score is left alone. Inventing a corrected
   number would be worse than carrying a stated bias.
9. **Ties resolve against the hypothesis**, and conservative measurement choices are
   preferred where they shrink the finding.
10. **Lower bounds are labelled.** Survivorship counts are published as "at least N".
11. **ASCII-only console output; verbatim prompt text stays local and gitignored.** The
    published JSON carries a 160-character preview and a sha1 per turn.

---

## 7. What limits the conclusions

The full ledger is [PLAN §7](./PLAN.md); the four that bite hardest:

- **No controls.** P1 and P2 differ in nature, age and model era. Case comparison, not
  experiment — except WS4, which was controlled and came back null.
- **Artifact survivorship (§5.8).** The bias is *correlated with the treatment*: blive's
  protocol required committing the substrate, btest had no such rule. WS1's adoption gap
  is inflated by it. WS2, WS3 and WS4 are unaffected.
- **Instrument circularity.** The rubric operationalises the author's own method.
- **Self-evaluation.** The author designed the instrument, ran the study and scored it.
  Countered by pre-registration, frozen keys, conservative tie-breaks, published
  sensitivity readings and an operator review pass — not eliminated.

**Fragility.** About five findings rest on hundreds of observations; about seven rest on
a single event. The split is structural — the robust ones measure operator behaviour
repeated across sessions, the fragile ones measure agent behaviour on one question.
[ASSESSMENT §5.1](./ASSESSMENT.md) is the ledger, and it binds the report: nothing
fragile leads a section, and no two fragile findings are aggregated into a rate.

---

## 8. Reproducing it, and running it elsewhere

Every script is stdlib-only Python 3.11, git-only, no network, and takes its repos as
`--repo NAME=PATH`. Nothing is hardcoded to this machine except the two optional
survivorship channels, which report their own absence rather than silently scoring zero.

```bash
python scripts/git_miner.py            --repo blive=... --repo btest=... --out-dir ../data/git-metrics
python scripts/complexity_profile.py   --repo ... --out ../data/complexity-profiles.json
python scripts/survival.py             --repo ... --audit ../data/survival-audit.json --out ../data/survival.json
python scripts/artifact_survivorship.py --repo ... --out ../data/artifact-survivorship.json
```

This portability is the point: `research/eval/` is the **only** thing that crosses into
the corporate environment for the P8 leg (PLAN §5). The instruments and scripts run there
unmodified; raw outputs stay in the org; only cleared aggregate metrics come back.

---

## 9. What this evaluation cannot answer

Stated so nobody has to discover it from the room:

- **Whether the substrate causes better outcomes.** Nothing here measures delivered
  quality. The outcome proxies are behavioural (rework, re-fix, warm-up cost).
- **Whether it would work for anyone else.** One author, one domain family, one model
  era. Every finding is about this operator's practice.
- **Whether the practised substrate differed from the recorded one** in the projects that
  did not commit theirs. Existence is partially recoverable; content is gone.
- **Anything about team collaboration.** Every project is single-operator. The paper's
  claim that the substrate carries state between *minds* is untested here.
- **P8's instrumented numbers.** They exist only inside the org (§8) and enter as cleared
  aggregates, later.
