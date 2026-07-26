# Exhibit bench — every presentable figure, with its caveat attached

**Status:** v1.0 — 2026-07-26 (S8). This is the appendix bench [PLAN §9](../PLAN.md)
promises: many numbers available on demand, **none mandatory**. The deck (S9) shops from
this file; [REPORT.md](./REPORT.md) shows where each exhibit sits in the argument.

Format per row: the honest caption is the sentence the exhibit is allowed to carry on a
slide. The caveat column is not optional fine print — **an exhibit shown without its
caveat is misquoted.** Groups: A robust leads · B robust counts with corrected captions ·
C honest negatives · D case studies and texture (fragile, n stated, never lead) ·
E context and background.

---

## Caption rules (binding on any derived material)

From [ASSESSMENT §5.1](../ASSESSMENT.md):

1. Nothing from group D leads a section or carries a claim — illustration after a robust
   number, with its n.
2. No two group-D findings are aggregated to imply a rate.
3. A robust count does not license the sentence built on top of it: before a number goes
   on a slide, name the reading its caption invites and check that reading separately.

Numbers that must never appear without their qualifier:

1. Any survival-curve point carries its **`at_risk` denominator** on the axis — blive's
   k=12 rests on **26** records, not 53.
2. The two WS5 arms are **not a shared denominator**: btest has no decision records; its
   arm is instruction rules + commit prose, flagged `n/a`, never zero.
3. The reversal-narration gap (11.9 vs 0.24 per 100 commits, hand-adjudicated) is shown
   **with** the prose-volume confound: 362.5 vs 62.7 words/commit; per-10k-words the
   automated gap is **2.1×, not 50×**. Publish both.
4. Any plot of rubric score against session-log altitude footnotes **seamQ** — WS1 scored
   the stripped tree, WS3 measured the in-flight posture.
5. `duration_days` in `complexity-profiles.json` is a **git span**, not project length —
   seamQ's real span is ~3 weeks, not 1.9 days.
6. **DEC-N2 is 0 for 3**: "we could not find one", never "they do not exist".
7. btest is **ephemeral, not flat**, and carries a **212-line agent-instruction file** —
   every substrated-vs-unsubstrated exhibit needs the qualifier; it may explain the probe
   null on its own.
8. **smim is `n/a: history lost`**, never zero.

---

## Group A — robust; may lead a section

| id | exhibit · honest caption | numbers (with denominators) | source | caveat that travels |
|----|---|---|---|---|
| A1 | **Retransmission tax.** "Re-entry costs 4× as much, twice as often, and moves the wrong way in the ephemeral project." | blive warms up in 9/10 sessions at ~106 chars, **falling** 192→106; btest in 43/68 at ~417, **rising** 477→607. Corpus: 78 sessions, 1,061 classifiable turns | `data/session-metrics/warmup.json` | btest's sessions also lengthened (9.1→19.8 turns); paste bodies survive 74/204, so payload-shaped warm-ups are under-counted — conservative against the finding |
| A2 | **Length-banded altitude.** "Controlled for turn length, the ephemeral project's operator sits lowest in every band." | btest lowest of 4 measurable projects in all 4 bands; blive vs btest: 0.19/0.08 · 0.26/0.15 · 0.42/0.35 · 0.80/0.65 (bands 0–39/40–119/120–399/400+ chars); n=1,061 turns | `data/session-metrics/altitude.json` | **Never publish altitude without its band** — the raw ordering is a verbosity artifact putting b-autobot (0.46) on top. Held-out agreement κ=0.902 on high/low is one-rater *stability*, not IRR. seamQ footnote per caption rule 4 |
| A3 | **Rework contrast.** "Four fifths of every line the ephemeral project added was later deleted — against one line in twenty." | blive 5.2% any-horizon / 3.9% at 14d; btest 82.2% / 32.6%. Denominator: all lines ever added per repo | `data/git-metrics/blive.json`, `data/git-metrics/btest.json` | Confounded: btest's history is 5× longer (213d vs 41d) and the projects differ in nature — texture, not proof. Churn is a blame-free LIFO approximation (biases in `_meta.definitions`); 14d column comparable only for blive/btest/harp |
| A4 | **What a short turn is made of.** "In a substrated project brevity is delegation; in an ephemeral one it is a clock tick." | dispatch-per-assent among turns <40 chars: seamQ 5.0 · b-autobot 0.50 · blive 0.25 · btest 0.10; btest has 147 short turns, 19% of its typing | `data/session-metrics/turns-classified.json` | **Fragile numerator**: btest's ratio is 3 dispatches vs 29 "continue"s — say so on the slide |

## Group B — robust counts whose captions were corrected (S7)

| id | exhibit · honest caption | numbers | source | caveat that travels |
|----|---|---|---|---|
| B1 | **Artifact survivorship.** "Everything blive's sessions produced reached git; at least one in nine of btest's working artifacts never did." | blive **0 of 33** ephemeral · btest **≥10 of 94** (firm floor 8) · seamQ **≥33 of 89** · b-autobot 0 · harp 2. All lower bounds | corrected figures: `data/survivorship-audit.json`; original (uncorrected by design): `data/artifact-survivorship.json` | Cite the **corrected** numbers only (S6 published ≥26; 16 of btest's 26 names were false positives). Two instrument properties: noise is one-directional (only ever inflates an ephemeral count; blive's 0 is unlowerable) and runs **with** the hypothesis; agent-side channel reaches only surviving transcripts (btest 10 files, **blive 0**) |
| B2 | **Commit-convention timeline, retitled.** "A stable-ID convention was replaced by a taxonomy — `feat(costs):` tells you a commit's kind; `[SMIM DATA-6]` lets a later record cite it." | 293/415 commits bracket-tagged, but 280/293 are `[SMIM]` and SMIM left the repo (`7d9b86f`); scoped ids: 163 Mar · **2 Apr** · 0 after (165/293); July: 9/10 conventional-commit prefixed; any-structured-prefix curve 0 · 96.3 · 96.7 · 64.3 · 100 (n=5) · 90% | `data/git-metrics/btest.json`; breakdown: STATE.md WS6 finding 6, [war-stories.md §6.3](./war-stories.md) | **Never show "0% in July" as an absence of discipline.** The published 96% "April peak" is the month the addressable ids vanished. Residual `[btest]`-convention claim rests on 29 commits, not 415 |

## Group C — honest negatives (the credibility play)

| id | exhibit · honest caption | numbers | source | caveat that travels |
|----|---|---|---|---|
| C1 | **The pre-registered null.** "My own pre-registered experiment failed to show the substrate reduces confabulation — and the one confabulation belongs to the full-substrate project." | Fisher's exact two-sided **p = 1.0** (identical under SC9); btest 38/38 · blive 37/38 (1 confab) · b-autobot 36/38 (2 abstentions); 3/20 slots voided, every void against the hypothesis | `data/probe-results.json`, `data/probes/scores.json`; pre-reg commit `ab9c62d` | Direction rests on **1** confabulation (fragile); the null survives any re-scoring. Confound: the "flat" arm carries a 212-line CLAUDE.md — 6 of 20 run-1 answers needed zero tool calls. b-autobot's clean sheet rests on 2 conservative-tie-break abstentions |
| C2 | **Altitude does not track discipline inside btest.** "The month with the least artifact discipline had the second-highest altitude." | monthly high share 0.256 · 0.251 · 0.192 · 0.400 (**n=5**) · 0.303 vs tag curve 91→96→50→40→0% | `data/session-metrics/altitude.json` + `data/git-metrics/btest.json` | June is 5 turns; and per B2 the tag curve itself is largely composition. The within-project migration PLAN §4 hoped for is **not supported** |
| C3 | **The instruction file does not decay silently.** "28 of 74 rules were withdrawn — zero unexplained." | btest CLAUDE.md: 46 rules at HEAD / 74 ever / 28 removed, 0 unexplained (25 in one scope-change commit). blive: 1 removal ever, announced | `data/survival.json` | Committed file only — the ephemeral class is unobserved (confound 6). Rewording counts as removal+addition, biasing removals **up** — the negative is conservative |
| C4 | **Zero silent reversals.** "No blive decision record was silently reversed in 12 sessions of exposure — the failures live elsewhere." | S(k)=1.000 at every k 0–12; declared curve 0.962 at k=12 on 1 declared supersession; **at k=12, at_risk = 26 of 53 ADRs** | `data/survival.json`, `data/survival-audit.json` | `at_risk` on the axis (caption rule 1); one arm only — btest `n/a` (rule 2); coverage disclosed: 18/53 ADRs read against the tree, the rest not counted as tested; sessions are a git proxy (4h gap threshold; 13 blive / 83 btest — name the threshold on any k-axis) |

## Group D — case studies and texture (fragile; n stated; never lead)

| id | exhibit · honest caption | n | source | caveat that travels |
|----|---|---|---|---|
| D1 | **The Python 3.12 pair.** "Both repos recorded the same decision the same day; one record is cited from five artifacts, the other from zero." | 1 (by construction) | `data/survival-audit.json` (WS5 finding 3) | Case study, not a rate. ADR-053 (4,902 chars, cited from 5 incl. the auto-loaded file, `companion:` names btest's sha) vs `fd106f9` (1,025 chars, a *good* record, cited from 0). The claim is **addressability**, not "btest didn't write why" |
| D2 | **The manufactured decision (OQ-033).** "An audit formalised a default into a dated decision that was never made." | 1 | `data/probes/scores.json`, `data/survival-audit.json`; [war story 3](./war-stories.md) | Rests on operator recollection; reported apart from every reversal count (MD-0) |
| D3 | **Born-wrong records, one per arm.** "Neither posture checks a factual claim at deposit time — every check runs at retrieval." | 1 + 1 | `data/survival-audit.json`; [war story 3](./war-stories.md) | Two anecdotes whose *symmetry* is the point (projects scoring 22/24 and 12/24) — not a rate. OQ-035's partial rescue (submit-path reading) is stated in the audit |
| D4 | **DEC-N2: 0 for 3.** "Three attempts to find a decision living only in conversation; three failures." | 3 negative constructions | `probes/questions-p{1,2,3}.md`, `data/probes/scores.json` | "We could not find one", never "they do not exist" (caption rule 6) |
| D5 | **Orientation completeness.** "The full-substrate project stated all four key facts in both runs; each other project missed the *same* fact twice." | 2 runs/project | `data/probe-results.json` | The reproduced omission is the signal; orientation *cost* (H-3) is inconclusive — see E7 |
| D6 | **Reversal narration.** "One project narrates its reversals; the other reverses 82% of its lines and narrates once in 415 commits." | 8/8 vs 1/4 hand-adjudicated hits | `data/survival.json` (adjudication in `data/survival-audit.json`) | **Caption rule 3**: adjudicated 11.9 vs 0.24 per 100 commits shown WITH prose confound (362.5 vs 62.7 words/commit); per-10k-words automated gap is 2.1×, not 50×. Publish both |
| D7 | **War stories 1–4.** Four incidents with receipts, each behind its robust number: 1→A3 · 2→A2 · 3→C1 · 4→A1 | 1 each | [war-stories.md](./war-stories.md) | Never aggregated; three of four are blive's because only blive has retros to read incidents from (selection property of the evidence) |

## Group E — context and background (frame-setting, not outcome claims)

| id | exhibit · honest caption | numbers | source | caveat that travels |
|----|---|---|---|---|
| E1 | **Adoption spectrum (rubric).** "Eight projects, four practices, scored 0–3 per axis from citable artifacts." | blive 22 · smim 20 · **P8 18 (PROVISIONAL-INFERRED)** · datacli 17 · harp 16 · b-autobot 15 · btest 12 · seamQ 7 (/24) | `data/rubric-scores.json`, `data/rubric-evidence.md` | Scores **durable** substrate only (scope statement; confound 6); instrument circularity (author's own method) — never shown without an outcome measure; seamQ scores its stripped tree; P8's A5 is the matrix's lowest-confidence cell; review moved two scores *down* |
| E2 | **Complexity ordering.** "The moderator every cross-project claim is read against." | btest > b-autobot > blive > harp > datacli > seamQ, stable across all primitives; Kendall's W 0.465–0.605, p<0.001 (indicative at n=7) | `data/complexity-profiles.json` | smim's rank unstable by construction (1 squashed commit; `n/a: history lost`); `duration_days` is git span (rule 5); qualitative ratings are a published *input*, excluded from computation |
| E3 | **Evidence coverage.** "1,480 turns across 168 sessions, three log stores; 1,061 classifiable operator turns; exclusions counted." | CC transcripts: btest 4 sessions Jul 6–16 only; history.jsonl: every prompt since 2026-03-03; Copilot store Mar 20–May 31 | `data/evidence-map.json`, `data/session-metrics/sessions.json` | blive's transcripts are gone (logs start after 30/70 commits); btest's Dec–Feb era has no recoverable transcript (JetBrains AI Assistant); session-based blive claims stay modest |
| E4 | **The unsubstrated baseline.** "Same repo, pre-methodology: 49-character commit messages; methodology era: 585." | 49 chars mean (Dec–Feb, n=78) vs 585 (Mar–Jul, n=337) — 12× at the tool boundary | STATE.md OQ-1; `data/git-metrics/btest.json` | Tool change and methodology adoption co-occur; separates eras, not causes. That era was AI-assisted (metered quota consumed) with no substrate and no log |
| E5 | **Re-entry counts.** "The ephemeral project re-entered from a ≥5-day gap sixteen times; the substrated one, once." | btest 16 gaps ≥5d (post-gap fix 20.8% vs 18.3% baseline) · blive 1 · datacli 1 | `data/git-metrics/*.json` | Counts, not rates — small n on every project but btest; per-event cost is *not* obviously higher |
| E6 | **Test trajectory.** "Tests follow project nature, not substrate posture." | test-file share: b-autobot 0.79→0.72 · btest 0.13→0.35 · blive 0.22→0.30 · datacli 0.25→0.23 · harp 0→1 file · seamQ 0 | `data/git-metrics/*.json` | The research projects' oracle is elsewhere (pre-registration, adversarial review) — this is the boundary refinement, not a defect |
| E7 | **Orientation cost (H-3): inconclusive.** "blive produced both the cheapest and the most expensive orientation in the corpus." | blive 118,735 and 447,000 tokens; btest 173,737/188,681; b-autobot 258,292/330,836; output tokens flat (3,465–5,138) | `data/probe-results.json` | 3.8× within-project spread at n=2 supports **no** directional claim — show only to demonstrate the honest refusal |
| E8 | **The discipline's own failure surface.** "What goes stale is the index, not the records — and errors are preserved with the same fidelity as decisions." | 4 SR-3 index defects (2 stale statuses, 2 missing rows of 53; outer register correct); 26 broken anchor occurrences / 7 distinct targets / 900 checked (2 malformed anchors copied into 20 of 26); genuine dangling refs: **1** of 144 ids across 171 files | `data/survival.json` | Declared-MISSING artifacts (7) are receipts, not gaps — counting them as dangling would score honesty as drift; slug rule approximates GitHub's algorithm, all 7 targets re-read by hand |

---

## What is deliberately absent

- **P8 instrumented numbers** — exist only in-org; enter later as cleared aggregates
  ([PLAN §5](../PLAN.md)). P8 appears here only as the anonymised rubric row in E1.
- **WS3(c) volume-vs-yield** — inconclusive by construction (turns-per-commit separates
  nothing; line-based yield is destroyed by deliberate extractions). In
  `data/session-metrics/yield.json` for the record; not presentable.
- **WS5(b) kernel teaser** — not attempted (PLAN §8 cut order); no numbers exist.
- **smim's history-derived metrics** — `n/a: history lost` everywhere, by rule 8.
