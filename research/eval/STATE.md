# Eval research — session state (warm-up / handoff file)

> Read this first in every eval session; deposit status + next step before ending.
> **How the evaluation was done, in one clean read: [METHODS.md](./METHODS.md)** —
> corpus, evidence channels, instruments, measurements, the eleven rules that govern
> them, and what the study cannot answer. Start there if you are judging or replicating
> the work rather than continuing it.
> Source of truth for scope and plan: [PLAN.md](./PLAN.md). One session per workstream.
> The next session's ready-to-paste prompt + model schedule: [NEXT_TASK.md](./NEXT_TASK.md).
> **Where the argument actually stands** — what the evidence supports, what it does
> not, and the recommended reframe: [ASSESSMENT.md](./ASSESSMENT.md) (mid-eval, written
> after S5; revisit after WS5 and WS6). Read it before writing anything for the talk.

## Status

| WS | Status | Session · model | Notes |
|----|--------|-----------------|-------|
| WS0 evidence audit | **DONE 2026-07-25** | S1 · Fable 5 | `data/evidence-map.json`; findings below |
| WS1 rubric | **DONE (REVIEWED) 2026-07-25** | S1 · Fable 5 → reviewed S2 | instrument `rubric/RUBRIC.md`; evidence `data/rubric-evidence.md`; scores `data/rubric-scores.json` v1.1 — judgment calls adjudicated; **P8 blanks stay open** (only fillable in-org) |
| WS-X complexity profile | **DONE 2026-07-25** | S2 · Opus 5 | `scripts/complexity_profile.py` → `data/complexity-profiles.json`; Kendall's W in 3 runs; declared ratings set via `data/qualitative-ratings.json` |
| WS2 git miners | **DONE 2026-07-25** | S2 · Opus 5 | `scripts/git_miner.py` (+ `scripts/corpus_common.py`) → `data/git-metrics/*.json` |
| WS3 session-log analysis | **DONE 2026-07-25** | S3 · Opus 5 | `scripts/log_miner.py` + `sample_turns.py` + `altitude_classify.py` + `session_yield.py` → `data/session-metrics/*.json`; instrument `rubric/ALTITUDE.md` v1.0; hand labels `data/altitude-labels.json`; **(a) survives only length-controlled, (b) is the clean positive, (c) inconclusive** |
| WS4a probe pre-registration | **DONE 2026-07-25** | S4 · Fable 5 | frozen at commit `ab9c62d` **before any run**: `probes/PROTOCOL.md` + 60 questions (20 x 3, one fixed slot template); subject `claude-sonnet-5`; 2 runs/project |
| WS4b probe runs + scoring | **DONE (REVIEWED) 2026-07-26** | S5 · Opus 5 | 6 sessions, 120 answers, `data/probe-results.json`; driver `scripts/probe_driver.py` + `scripts/probe_guard.py`; verdicts `data/probes/scores.json`. **H-1 is NULL (p=1.0)**; SC8 review done — 3 of 20 slots voided, **one confabulation left in the whole corpus** — findings below |
| WS5 survival curves | **DONE 2026-07-26** | S6 · Opus 5 | `scripts/survival.py` → `data/survival.json`; hand-audit input `data/survival-audit.json` (10 findings, 21/21 receipts verified). **Zero blive ADRs silently reversed**; the findings are elsewhere. Kernel teaser (WS5b) **not attempted** — see below |
| **WS0-bis artefact survivorship** | **DONE 2026-07-26** | S6 · Opus 5 | `scripts/artifact_survivorship.py` → `data/artifact-survivorship.json`. **blive 0 of 33 ephemeral; btest >=26; seamQ >=33.** Raised by Oleg, not by an instrument. New **PLAN §7 confound 6**; RUBRIC scope statement; ASSESSMENT §2.6/§3.8 |
| WS6 archaeology | **DONE 2026-07-26** | S7 · Opus 5 | `report/war-stories.md` — 4 stories with receipts (3 blive, 1 btest), one of them a negative. Hand-audit input `data/survivorship-audit.json`. **Two published exhibits corrected** (WS0-bis count; WS2 tag curve) — findings below |
| Report assembly | **DONE 2026-07-26** | S8 · Fable 5 | `report/REPORT.md` (sections 1:1 to PLAN §9 core arc) + `report/exhibits.md` (the appendix bench, 23 exhibits in 5 groups). No new measurement; findings below |
| Deck + dry run | **DONE 2026-07-26** | S9 · Fable 5 | `talks/does-the-substrate-matter/`: `slides.md` (core arc 1:1 with REPORT + M-A…M-F) · `handout-rubric.md` · `NOTES.md` (branch-point map + if-challenged lines). Deck-side caption/caveat audit done (1 bench caption fixed); **live rehearsal pending on Oleg**. Requirements-v0 word-count discrepancy reconciled — findings below |

This table is the **source of truth for the session/model schedule**; NEXT_TASK.md carries
only the next session's prompt.

## WS0 findings (2026-07-25)

Three local session-log sources, complementary coverage (details in `data/evidence-map.json`):

1. **Claude Code full transcripts** (`~/.claude/projects/`) — only recent sessions survive
   retention cleanup: btest 4 sessions Jul 6–16 (**5.56M output tokens**), datacli 2,
   shared-substrate 3. Older transcripts (incl. all of blive's) are gone; their project
   folders retain only auto-`memory/`.
2. **Claude Code global history** (`~/.claude/history.jsonl`) — **every user prompt since
   2026-03-03 survives** with project, sessionId, timestamp: btest 63 sessions/829 prompts,
   b-autobot 9/123 (the Mar 5–11 sprint), blive 10/119 (May 2–Jun 6), seamQ 4/57,
   smim 1/2, harp 1/11. Human-side turns for ALL corpus projects → **operator-altitude
   analysis (WS3a) is feasible corpus-wide**; assistant-side volume is not recoverable here.
3. **Copilot JetBrains store** (`~/.copilot/jb/`) — full two-sided sessions Mar 20–May 31:
   btest 48 sessions/21.7MB, harp 4, smim 2, blive 2. No token fields (bytes as volume
   proxy). Nothing for b-autobot (predates the store).

Evidence boundaries (report these honestly):
- history.jsonl starts 2026-03-03 — btest's Dec 2025–Feb 2026 era has no local session
  evidence; tooling for that period unknown (**ask Oleg / OQ-1**).
- blive has rich *artifact* + git evidence but thin session logs (119 prompts, 2 CP
  sessions) — session-based claims about blive stay modest.
- Token accounting only possible on the recent CC window; cross-tool volume comparisons use
  message counts/bytes, not tokens.

Leads deposited for later WS:
- **WS6:** `~/.claude/projects/*/memory/` files are evidence — blive's includes
  `feedback_warmup_discipline.md` (the agent's own persistent memory of being taught the
  warm-up protocol). Also `feedback_surface_full_option_space.md`, `feedback_work_on_main.md`.
- **WS3:** CC transcripts mark subagent traffic via `isSidechain` — separate human turns
  from orchestration when classifying altitude.
- First btest history entry (Mar 3) is the b-autobot bootstrap prompt pasted in the btest
  folder — session→project attribution by folder has occasional bleed; attribute by content
  when it matters.

## Open questions — all three CLOSED 2026-07-25 (S2)

- **OQ-1 · CLOSED, answered from evidence.** btest's Dec 2025–Feb 2026 era was built in
  **PyCharm 2025.2 with JetBrains AI Assistant**, and that tool keeps no recoverable
  per-session transcript. Evidence: the `PyCharm2025.2` config dir first appears 2025-12-13
  (btest's first commit is 2025-12-09); `llm.for.code.xml`, `llm.nextEdits.xml` and
  `AIChatContextPopupPromotionState.xml` are all dated **2025-12-05**, four days before the
  project began; `AIAssistantQuotaManager2.xml` (2025-12-13) records a live metered
  subscription with **~1.39M of 3.5M units already consumed**. GitHub Copilot is absent
  until March (`github-copilot/iu/` 2026-03-03, `.copilot/jb/` store 2026-03-20) and Claude
  Code until 2026-03-15 (`CLAUDE.md` added). **VS Code is not installed anywhere on the
  machine** — the `.vscode/settings.json` committed 2026-02-11 is a false lead, not evidence
  of use. Quantitative signature of the transition: mean commit-subject+body length is
  **49 chars in Dec–Feb (n=78) vs 585 chars in Mar–Jul (n=337)**, a 12x jump at the tool
  boundary.
  *Why this matters:* that era **was** AI-assisted — quota was being burned — using a
  surface with no substrate and no recoverable log. It produced terse commits, zero
  agent-instruction files, zero decision records. It is the corpus's **unsubstrated
  baseline**, not a hole in it.
- **OQ-2 · CLOSED, partially answered.** No claude.ai conversation export exists locally
  (no `conversations.json`, no data-export archive; the four `Downloads/files*.zip` are an
  unrelated maths study guide). Transcripts for blive's lost sessions are **not
  recoverable**. But claude.ai-authored *artifacts* from the relevant windows do survive in
  `~/Downloads` and are catalogued for WS3/WS6:
  - `ib_algo_engine_requirements_v0.md` (2026-04-26 — **blive's first commit day**) is
    blive's Requirements v0, i.e. the paper's "first artefact deposited to the substrate".
    Direct evidence the origin artifact was authored in claude.ai web. **Discrepancy to
    reconcile before the talk:** it is 3,375 words; the paper says "around six thousand".
  - `HANDOFF_to_new_chat_v2.md` + `KICKOFF_PROMPT_v2.md` (2026-04-30) are **seamQ**, not
    blive. The kickoff opens: *"The prior version of this prompt assumed `/home/claude/`
    would persist across chats. It doesn't."* — a retransmission-tax artifact in raw form,
    a session protocol being revised because state was silently lost. Prime WS3/WS6 material.
  - *Consequence for WS-X:* those artifacts predate seamQ's first commit (2026-05-16) by
    over two weeks, so **seamQ's real project span is ~3 weeks, not the 1.9 days its git
    span reports**. `duration_days` is correctly labelled as git span but must not be read
    as project duration for that project.
- **OQ-3 · CLOSED, negative.** No other local Copilot store exists. `~/.copilot/` holds
  only `jb/` (plus instructions/prompts/skills); `AppData/Local/github-copilot/` is auth
  plus a 16 KB `copilot-intellij.db` with no session content. b-autobot's sprint
  (Mar 5–11) genuinely predates the `jb/` store (Mar 20) — **those logs are confirmed
  lost**, and CC history covers the sprint's human turns.

## WS1 findings (2026-07-25, reviewed in S2)

Scores (**v1.1-REVIEWED**, /24): blive 22 · smim 20 · datacli 17 · harp 16 ·
b-autobot 15 · btest 12 · seamQ 7 (current tree) · work-project provisional.

**Review outcome (S2).** Two of the four flagged judgment calls were adjudicated down,
both toward the conservative reading, and both *against* the talk's own argument:
- **b-autobot A3 3→2** — 91 BDD scenarios are executable contracts on the critical
  surface, but the latency budgets are comments in a `reference.conf` timeouts block, not
  measured values asserted against. blive A3 was held to 2 for the identical deficiency.
  b-autobot is the local rehearsal of the focal case, so this is the score most likely to
  have been inflated by the instrument's own circularity (PLAN §7 risk 4).
- **harp A6 3→2** — the 759-line manifest is an exhaustive inventory plus a real schema
  dictionary, but harp's notation lives in the paper (no glossary artifact) and its
  CRITICAL/MODERATE/LOW tags mark data-quality severity, not artifact freshness. The two
  remaining 3s on this axis (blive, smim) carry both a glossary and a status lifecycle.

Upheld: **blive A8=3** (the planned drift-audit scripts sit beyond the anchor, which asks
only for agent-runnable checks + a maintained warm-up/handoff artifact — both present) and
**smim A3=2** (partial executable spec, no NFR envelope).

**P8's four blanks (A4/A5/A6/A8) are now filled PROVISIONAL-INFERRED**, from the same
source as the rest of that row and each carrying its reasoning in `data/rubric-scores.json`:
A4=1, A5=2, A6=2, A8=2 → **P8 = 18/24**, placing it 3rd (blive 22 · smim 20 · **P8 18** ·
datacli 17 · harp 16 · b-autobot 15 · btest 12 · seamQ 7). Two things to carry forward:
**A5 is the lowest-confidence cell in the whole matrix** — the 1-vs-2 call (decisions
living in the increment plan, vs a decision log kept irregularly) is not settleable from
the paper and should be overruled from memory if memory disagrees. And P8 landing at 18
rather than 22 is a *credible* placement rather than a convenient one: the focal case
scores high but not top, which is what a two-week timeboxed brownfield job under "partial
discipline" (PLAN §2's own phrase) should look like. The whole row is still refreshed
in-org against real git history and Copilot CLI logs (PLAN §5).

Headline observations (full list in `data/rubric-scores.json`):

1. **The ordering defies the naive story.** Research projects score mid-high — via
   *research-native* instruments (harp's pre-registration with stop-for-futility rules,
   smim's notation sheet + kill rules, seamQ's adversarial-review pipeline). The paper's
   boundary claim refines: exploratory work has *different substrate artifact types and
   lifecycle*, not no substrate. Pre-registration is a frozen intent contract.
2. **btest decayed, measurably.** 293/415 non-merge commits carry a bracketed stable-ID tag
   (280 of them `[SMIM]`, often scoped as `[SMIM DATA-6]`); the trailing 13 commits carry
   none. Within-project temporal evidence — stronger than any cross-project comparison.
   **WS2 has now quantified the curve** (finding 2 below): 0% → 91% → 96% → 50% → 40% → 0%.
3. **datacli = à-la-carte in vivo:** kept gates/executable contracts/status-tagged
   manifests, skipped ADRs/glossary/session protocol at 117-file scale — consistent with
   the complexity threshold.
4. **b-autobot and blive have inverse profiles** (guardrails+validation vs
   representation+session) → the four practices are separable in practice.
5. **seamQ: substrate as scaffolding** — full workspace (warm-up INDEX, weekly gates,
   3-persona adversarial review) deliberately stripped at publication (commit e9d951e).
6. War-story leads deposited in evidence file: b-autobot stale CLAUDE.md refs to deleted
   plan docs (reference rot in vivo); harp's §9.1 "conversation-only items" context-loss
   ledger; smim's squashed history (1 commit).

## WS2 + WS-X findings (2026-07-25)

Scripts are stdlib-only, read-only (`git --no-optional-locks`), path-parameterised —
they are §5-portable as written. `corpus_common.py` holds the one shared definition of
"source file" so the two miners cannot drift apart.

| project | churn 14d | churn any | fix% | re-fix ≥3 | gaps ≥5d | root litter | tagged% |
|---------|-----------|-----------|------|-----------|----------|-------------|---------|
| blive | **3.9%** | 5.2% | 10.4% | 4 | 1 | 1 | **100%** |
| btest | **32.6%** | **82.2%** | 18.3% | 14 | 16 | **26** | 70.6% |
| b-autobot | 47.4%† | 47.4% | 14.0% | 1 | 0 | 0 | 0% |
| datacli | 3.7%† | 3.7% | 20.0% | 0 | 1 | 0 | 0% |
| smim | n/a | n/a | n/a | n/a | n/a | 0 | n/a |
| harp | 0.6% | 0.7% | 0.0% | 0 | 1 | 0 | 0% |
| seamQ | 90.9%† | 90.9% | 8.0% | 0 | 0 | 1 | 0% |

† project shorter than the 14-day window, so that column *is* its whole-history rework
share, not a fast-rework signal (`window_exceeds_history_14d` in the JSON). **The 14-day
column is only comparable across blive / btest / harp.**

1. **The P1-vs-P2 contrast survives the honest cut.** Among the three repos long enough
   for the window to mean anything, blive 3.9% vs btest 32.6% short-horizon churn (8.4×),
   and 5.2% vs 82.2% rework at any horizon (16×) — four fifths of every line btest ever
   added was later deleted. Confound stated: btest's history is 5× longer (213d vs 41d),
   which gives its lines more opportunity to die. Texture, not proof (PLAN §7).
2. **btest's discipline curve is adoption → peak → decay, not just decay.** Bracketed
   stable-ID prefix share per month: 0% (Dec–Feb, pre-methodology) → 91% (Mar) → **96%
   (Apr, peak)** → 50% (May) → 40% (Jun) → **0% (Jul, post-SMIM-extraction)**; the
   trailing 13 commits carry no tag at all. Within-project temporal evidence, headline
   exhibit. **Correction to WS1 finding 2:** the 280 `[SMIM]` commits are confirmed, but
   the denominator is 415 non-merge commits (70.6%, not 280/423 as a share of tagged
   discipline), and "the last 30 commits have zero" is imprecise — the last 30 are 30%
   tagged; the accurate claim is the last **13** commits, and all of July, are untagged.
3. **Gap recovery separates the postures.** btest took 16 gaps ≥5 days; after each, fix
   commits run at 20.8% vs an 18.3% baseline and "other" (unclassifiable subjects) *falls*
   from 42% to 25% — re-entry is not obviously costlier, but it is 16 re-entries vs
   blive's 1 and datacli's 1. Small-n on every project but btest; report as counts.
4. **Root hygiene needed a third measurement to stay honest.** The specified metric
   (`git status --porcelain` untracked, root) scores btest **1** — because its 20+ `tmp_*`
   scratch files are *gitignored*. `scratch_litter_root` counts on-disk scratch regardless
   of tracking status and scores btest **26**, matching PLAN §2's "~25 tmp_* files". A
   .gitignore rule can silence the specified metric; the JSON reports all three views.
5. **b-autobot committed its dependencies:** 9,248 of 9,456 tracked files are vendored
   `node_modules` under `src/test/webapp*/`. Excluded from every metric (and the exclusion
   count published) — but it is itself a substrate-hygiene data point for WS6, and it is
   why b-autobot's language count (8) outranks every other project.
6. **Test trajectory splits by project nature, not by substrate.** b-autobot 0.79→0.72
   test-file share (a BDD regression suite *is* tests), btest 0.13→0.35, blive 0.22→0.30,
   datacli 0.25→0.23 — versus harp 0→1 test file and seamQ 0. The research boundary cases
   have essentially no test instrument; their oracle is elsewhere (pre-registration,
   adversarial review) — consistent with WS1 finding 1.
7. **Complexity ordering is stable, so the moderator analysis has a spine.** Kendall's W
   across the primitives: 0.465 (all 7, all 9 primitives), 0.605 (entropy dropped),
   0.509 (smim excluded) — all p < 0.001, chi-square approximation flagged as indicative
   at n=7. Ordering **btest > b-autobot > blive > harp > datacli > seamQ** holds in every
   run; only **smim** moves (2nd → 4th), because its single squashed commit forces
   normalised change entropy to 1.0 by construction. That is the licensed ordering.
8. **smim is `n/a: history lost`, never zero.** Every history-derived metric is emitted
   under an explicit degeneracy flag with the computed value preserved beneath it, so no
   downstream chart can read a squashed repo as a well-behaved one.

Measurement caveats that must travel with these numbers into the report:
- Short-horizon churn is a **blame-free LIFO approximation** over `git log --numstat -M`
  (line counts, not line identity); its biases are documented in the script docstring and
  echoed into every output file's `_meta.definitions`. `unattributed_deletions` is 0 for
  all seven repos, so the reconstruction is at least internally consistent.
- Commit-subject classification is regex-based with a fixed, published precedence
  (revert > fix > docs > test > feature > chore > other); btest's pre-2026-03 era uses
  free-text subjects ("unit tests", "fix for turnover") and lands in `other` at 42%.
- The qualitative WS-X(b) ratings (integration surface, constraint tightness,
  statefulness) are emitted as **nulls with criteria** in `complexity-profiles.json` —
  author judgment, for Oleg to fill, explicitly excluded from Kendall's W.

**Hand-verification before the sweeps** (recorded in each output's `_meta.verification`):
on seamQ, fix-commit count (2/25) and total added lines (46,889) reproduced exactly by
independent shell counts; non-blank LOC (3,836) and AIT (190,452 raw → 49,704 compressed)
reproduced byte-exactly; on btest, bracket-prefix count (293/415) reproduced by
independent grep; Kendall's W recomputed by hand from the published rank matrix
(S=1036, T=120, denominator 20,544 → W=0.6051). Three of those checks caught real bugs —
a 37-line dotfile undercount, a tag regex that required a space-free tag and read btest at
110 instead of 293, and a tier-grouped AIT concatenation that diverged from PLAN §4's
sorted-path definition. All three are fixed; the sweeps above are post-fix.

## WS3 findings (2026-07-25)

Instrument: `rubric/ALTITUDE.md` v1.0 (four classes, nine numbered boundary rules,
fixed precedence), frozen after a 99-turn stratified hand-labelling pass and before
the classifier was written. Corpus: **1,480 turns / 168 sessions** from three log
stores, of which **1,061 are classifiable operator turns** (slash, machine-rendered,
off-project and unrecoverable-paste turns excluded and counted).

**Agreement (hand vs automated), the number PLAN §4 requires.** Four-way: dev
0.820 (κ=0.713), held-out **0.895 (κ=0.835)**. High-vs-mechanical collapse: dev
0.869, held-out **0.947 (κ=0.902)**. The first run, before four rule-implementation
defects were fixed, scored held-out 0.868/κ=0.806 four-way — published alongside as
the uncontaminated measurement, since five held-out disagreements had been read by
the time the fixes were made. This is instrument *stability*, not inter-rater
reliability: there is one rater. **The four-way split is noisy; the high/low split
is solid — so the exhibit is built on high/low.**

1. **The naive cross-project altitude comparison fails, and it fails for a
   measurable reason.** Raw high-altitude share: b-autobot 0.46 · seamQ 0.35 ·
   blive 0.30 · btest 0.25 — which puts the *least* substrated build near the top.
   That ordering is mostly turn length: high share rises monotonically with typed
   length inside every project (btest 0.08 → 0.15 → 0.35 → 0.65 across the 0–39 /
   40–119 / 120–399 / 400+ character bands). **No altitude number is publishable
   without its length band.**
2. **Length-controlled, the contrast returns and btest is last.** In every band,
   btest is the lowest of the four measurable projects, and blive beats it in every
   band (0–39: 0.08 vs 0.19; 40–119: 0.15 vs 0.26; 120–399: 0.35 vs 0.42; 400+:
   0.65 vs 0.80). This is the honest version of the headline claim.
3. **The sharpest exhibit is what a *short* turn is made of.** Among turns under 40
   characters — dispatch-by-reference ("read `NEXT_PROMPT.md`, execute") per bare
   assent ("continue"): **seamQ 5.0 · b-autobot 0.50 · blive 0.25 · btest 0.10**
   (3 dispatches against 29 "continue"s). btest also has the most short turns: 147,
   19% of everything it typed. In a substrated project brevity is delegation; in a
   flat one it is a clock tick.
4. **WS3(b) is the clean positive — and it is about *shape*, not amount.** blive
   opens 9 of its 10 sessions with a warm-up turn (mean prefix 1.00) costing ~106
   characters; btest warms up in 43 of 68 sessions (prefix 0.53) at ~417 characters
   — **4× the cost, half as often**. Direction over each project's own lifetime
   (first vs second half of its sessions): btest **rising** 477 → 607 warm-up chars
   per session, blive **falling** 192 → 106, seamQ falling 740 → 456, b-autobot
   rising 26 → 322 (n=7, 6-day span). Two caveats travel with this: btest's sessions
   also got longer (9.1 → 19.8 turns), and paste bodies survive for only 74 of 204
   paste-referencing turns, so payload-shaped warm-ups are *under*-counted —
   conservative against the finding.
5. **Negative result, reported as such: within btest, altitude does not track the
   discipline curve.** Monthly high share runs 0.256 (Mar) · 0.251 (Apr) · 0.192
   (May) · 0.400 (Jun, n=5) · 0.303 (Jul) against WS2's stable-ID tag curve of
   91% → 96% → 50% → 40% → 0%. July has btest's *least* artifact discipline and its
   second-highest altitude. PLAN §4's hope that "the migration is visible in P2
   chronology" is not supported by this measurement.
6. **seamQ's rubric score and its session posture disagree by construction, and
   both are right.** WS1 scored the surviving tree (7/24); seamQ stripped its
   substrate at publication (−37,861 lines, commit e9d951e). Its *in-flight* posture
   has the corpus's highest dispatch ratio and its highest warm-up share (0.176).
   Any exhibit plotting rubric score against altitude must footnote seamQ or it
   reads as a counterexample when it is a measurement-window artefact.
7. **WS3(c) is inconclusive and is written up that way.** Turns per landed commit
   sits at 1.56–2.92 across the four measurable projects and separates nothing.
   Line-based yield is unusable in this corpus: one btest notebook commit adds
   151,591 "source lines", and btest's −147,711 net over the window is produced by
   the `research/` removal (−254,072), the SMIM extraction (−104,667) and the
   datacli extraction (−15,208) — deliberate moves, not waste. Excluding notebooks,
   retention is blive 0.87 · b-autobot 0.53 · btest 0.13 · seamQ 0.09; datacli and
   harp are attribution artefacts (both were built inside btest's folder).

**Evidence corrections and coverage, for the report's honesty ledger:**
- **WS0 finding 3 was imprecise.** history.jsonl's first entry is `/init` in the
  btest folder; the b-autobot bootstrap prompts that follow are correctly recorded
  under the b-autobot folder. Folder attribution is *cleaner* than WS0 assumed —
  only **12 of 1,480 turns** were re-attributed (10 by explicit foreign path, 2 by
  hand override), and the signature rule fired zero times once extraction windows
  were applied.
- **WS0's Copilot user-message counts are ~2.3× too high.** They counted
  `user.message_rendered`; the store holds only **96 verbatim `user.message`
  records**, and 48 of its 57 sessions carry *only* a machine-composed third-person
  brief. Those are excluded from altitude — classifying them would measure the
  renderer.
- **Attribution needs time windows, not just content.** SMIM lived inside btest
  until 2026-05-02 and the EODHD tooling until 2026-07-09, so four March/April
  "smim" turns were btest's. Windows and two hand overrides are frozen in
  `data/attribution-rules.json` as a script *input*.
- **btest's last logged session (Jul 16) is printer troubleshooting**, not
  engineering — 8 turns, caught by session-level off-project pooling and excluded.
  22 off-project turns total across 4 sessions.
- Verbatim prompt text stays local and gitignored
  (`data/session-metrics/local/`); the published JSON carries a 160-character
  preview and a sha1 per turn, and re-running `log_miner.py` reproduces the rest.

## WS4a findings (2026-07-25)

1. **Pre-registered at `ab9c62dc3cb421174eca13a5f9ebc1692ccef0b6` (2026-07-25 23:57 +0100), with
   nothing run.** Instrument: PROTOCOL.md (subject `claude-sonnet-5`, repo-only access, no
   cross-session memory + contamination check, frozen texts F1–F6, SC1–SC10 scoring with a
   false-absence subtype and a published sensitivity run, ties resolve *against* the
   hypothesis, 2 runs/project, one pre-registered Fisher test) + 20 questions per project on
   one fixed slot template (7 decide / 7 state / 6 why; 14 recorded / 6 absence-shaped).
2. **The absence-shaped slots converted differently per project, and that is itself a
   result:** blive documents its own gaps (its traps became `recorded-absence` — receipts for
   what doesn't exist); b-autobot deposited every conversational *decision* in code but lost
   the *reasons* (no conversation-only decision was recoverable; the substitution is declared
   in questions-p3.md); btest lost both — the SMIM extraction (−104,959 lines) has an empty
   commit body and no recoverable rationale anywhere in the repo.
3. **Every project got a doc-vs-code divergence question** (the stale-substrate trap family):
   blive's OQ-035 vs `types.py` (order-type surface), btest's CLAUDE.md 3-scheme list vs 6 in
   code, b-autobot's "66 scenarios" vs 91 countable + a dead CI advertised by a live README
   badge.
4. **Two candidate traps were rejected at design time and recorded in questions-p3.md** (the
   combobox rejection was actually deposited; the M6/corp-env deferral has contested ground
   truth because the deletion commit claims "all milestones complete") — the reject log is
   part of the instrument's honesty.
5. **WS6 handoff — conversation-only receipts** (sha1s in `turns-classified.json`): btest
   no-skips policy `a878c86c0eeb`; blive work-on-main `01bab5bd50f0`/`1d771f968cb2`;
   b-autobot gridbot-name rejection `b64900916546`; btest SMIM-extraction rationale
   `e66460c50699`/`3a39b4ff5c61`.

## WS4b findings (2026-07-26, reviewed same day)

Six sessions (2 runs x 3 projects, b-autobot -> blive -> btest each run), subject
`claude-sonnet-5`, 120 answers, every one carrying an `ANSWER:` line. Counts below are
**post-SC8-review**: three question slots were voided (finding 8), so each project is
scored on 38. Full data, both SC9 readings, per-session orientation cost and every
scored pair are in `data/probe-results.json`; verdicts and their one-line reasons are in
`data/probes/scores.json`, kept as a script *input* so no re-run can overwrite them.

| project | n (asked 40) | correct | abstained | confabulated | SC9 confab |
|---------|--------------|---------|-----------|--------------|-----------|
| btest | 38 (2 voided) | **38** | 0 | **0** | 0 |
| blive | 38 (2 voided) | 37 | 0 | **1** | 1 |
| b-autobot | 38 (2 voided) | 36 | 2 | **0** | 0 |

1. **H-1, the pre-registered test, is NULL - and after review its nominal direction runs
   backwards.** blive 1/38 confabulations vs btest 0/38; Fisher's exact two-sided
   **p = 1.0**, identical under SC9. The single confabulation in the entire corpus
   belongs to the *full-substrate* project. Published as it came out (PROTOCOL section 8).
2. **H-2 is null too**, same direction: correct rate btest 38/38 = 1.000, blive
   37/38 = 0.974.
3. **H-3 is inconclusive, and blive's own variance swamps the contrast.** Orientation
   tokens through the accepted statement: blive **118,735 and 447,000** - the corpus's
   cheapest *and* its most expensive - against btest 173,737 / 188,681 and b-autobot
   258,292 / 330,836. Output tokens are nearly flat across all six sessions
   (3,465-5,138). A 3.8x within-project spread over n=2 supports no directional claim.
4. **The one stable orientation difference is completeness, not cost.** blive stated
   **4 of 4** orientation key facts in both runs, never needing a nudge. b-autobot and
   btest stated **3 of 4** in both runs, and each missed the *same* fact twice -
   b-autobot the sprint shape, btest how its tests are run. Reproducing the same omission
   across independent runs is the cleanest signal the probe produced.
5. **H-4 is not supported.** b-autobot does not sit between: post-review it has zero
   confabulations and the corpus's only two abstentions. The predicted mechanism - stale
   in-tree references *inducing* confabulation - did **not** fire: on both questions
   built around b-autobot's doc/tree divergence the subject counted the tree and was
   right (91 scenarios, not the docs' 66; CI disabled, not the README badge's live
   nightly).
6. **The surviving confabulation is the sharpest single datum in WS4.** blive-run2,
   P1-Q20: asked why blive decided against sourcing the VIX signal from sfera, it
   manufactured a rationale and attributed it to the record - *"The stated rationale, **as
   recorded**, is that R-LEV-001's signal is already validated and productionised
   elsewhere via sfera ... consistent with ADR-014/ADR-017."* Run 1, on the same repo,
   correctly answered that the decision is recorded and its reason is not. **The operator
   confirms sfera was never considered as a blive data source** - the standing plan was
   always EODHD + IB - so `accidentally_true` is definitively false: the agent invented a
   reason for a deliberation that never happened. Recorded slots, by contrast, came back
   near-perfect everywhere (blive 28/28, btest 28/28, b-autobot 24/28), so retrieval is
   not where the substrate boundary sits - the *why* is.
7. **A substrate failure mode found in blive, not in the agent.** `OPEN_QUESTIONS.md`
   OQ-033 records *"Operator decision (2026-06-06): source from EODHD - not from sfera"*
   for an option the operator says was never on the table. The readiness audit formalised
   a standing default into a dated decision. That over-formalisation is what created the
   probe question in the first place, and it is a WS6 item: append-only discipline can
   manufacture decisions as well as preserve them.
8. **Three of twenty slots were voided - 15% of the instrument - and that is a finding
   about the S4 question design, not about the projects.**
   - **P1-Q07** (blive, both runs): the frozen absence check claims branch-policy
     language greps to zero; `CONTEXT_PROTOCOL.md:456` (section 8.4) prescribes "Each
     session takes a unique branch". Both runs found it; run 2 said so and the key would
     have marked it wrong.
   - **P3-Q01** (b-autobot, both runs): the key asserts a settled PascalCase convention
     whose only receipt is an R100 rename buried in an unrelated mega-commit. No artifact
     states it, and the operator has no memory of settling it.
   - **P2-Q07** (btest, both runs): the receipt turn was a *situational* instruction, not
     a policy adoption, so nothing was deposited in conversation; and the question
     conflates "is there a policy statement" (no) with "is skipping acceptable in
     practice" (yes, by deliberate in-repo mechanism), which is exactly what split the two
     runs.
   Every void runs **against** the hypothesis - b-autobot loses both its confabulations,
   btest loses its only one, blive is unaffected. No void improves blive. No key was
   edited, no question replaced, no answer regenerated (H9 / section 10).
9. **The DEC-N2 slot is 0 for 3, and that is arguably the real result.** The slot built to
   catch "a decision made in conversation only, never deposited" could not be soundly
   constructed in any project: b-autobot's was **declared unfillable at freeze** (every
   conversational decision had been deposited in code or design docs), blive's turned out
   to be **in the repo after all**, and btest's turned out **not to have been a decision**.
   Three independent attempts to find a decision living only in conversation, three
   failures. This cuts *for* the substrate thesis in a way the confabulation count does
   not - but it rests on three negative constructions, so it must be stated as "we could
   not find one", never as "they do not exist".
10. **A treatment-arm confound PLAN section 2 understated.** btest's `CLAUDE.md` is a
    212-line agent-instruction file, not an absence of substrate: six of btest's twenty
    run-1 answers were correct with **zero tool calls**, straight out of it. The "flat"
    arm is flat in *decision records*, not in agent instructions - enough on its own to
    explain a null, and a qualifier every substrated-vs-unsubstrated exhibit now needs.
11. **Answers were scored on content, not method (SC2), and method was sometimes
    startling.** b-autobot-run1 P3-Q16 gave both recorded reasons for rejecting FINOS VUU
    in one turn with zero tool calls - without ever opening the git-history-only receipt
    that holds them.
12. **Harness integrity.** Two access attempts, both btest, both `uv run pytest` (outside
    H1's read-only grant). The sharpest H2 evidence is blive-run2's F1: the subject
    *attempted to list its own persistent-memory directory* and the guard denied it -
    isolation demonstrated rather than assumed. The scratch memory store was independently
    verified empty.

Caveats that must travel with these numbers:
- n is tiny where it matters: the headline now rests on **one** confabulation. Any single
  re-scored verdict moves every rate. Counts are shown with denominators.
- **Evidence rule adopted at review, now standing for the whole report (Tier A/B):** a
  claim that "we decided X" must rest on an artifact that *states* the decision (ADR, OQ
  resolution, doc sentence, commit body giving the choice). A decision *inferred* from a
  diff, rename or config change may ground a claim about the **state** of the code, never
  about a decision. Two of the three voids are applications of this rule.
- **Voiding on operator memory is a declared extension** to the frozen protocol (H9
  contemplates receipts failing against the repo, not against recollection), recorded in
  `data/probes/scores.json` under `declared_protocol_extension` rather than smuggled in.
- Two ABSTAINED verdicts rest on SC7's conservative tie-break (b-autobot P3-Q05, both
  runs); read as commitments they would take b-autobot from 0 to 2 confabulations.
- Three harness deviations are declared in `data/probes/scores.json`: `--setting-sources
  project` (the repos' own `.claude/settings.local.json` sets `bypassPermissions` and
  grants `Read` across all sibling repos - loading it would have voided H1); turn caps
  scored rather than enforced (CLI 2.1.220 has no `--max-turns`); and the CLI's dynamic
  system-prompt section, which puts `git status` and recent commit subjects in front of
  every F1.
- One session was voided and restarted under H7 (driver bug: F5's frozen placeholder is
  `<question text>`, not `<question>`, so the first b-autobot run 1 sent bare templates and
  the subject answered nothing). Preserved in full, unscored. One surplus F3 nudge was sent
  to btest-run1 by operator misjudgment; orientation cost is reported through the accepted
  statement with the surplus published separately.

## WS5 findings (2026-07-26)

Instrument: `scripts/survival.py`, stdlib-only, read-only git, path-parameterised
(§5-portable), reusing `corpus_common`'s single definition of a source file. **The
definition of "silent reversal" was frozen in the script docstring before the
measurement was written**, and the boundary it draws is the whole workstream:

> A **declared** reversal — the record's status moves to `SUPERSEDED-BY-*`/`DEPRECATED`,
> or a later record carries `supersedes:` pointing at it, or the body is edited to
> state the change — is the discipline **working**, and is never counted as a failure.
> Only an **undeclared** contradiction counts. Refinement-with-a-pointer, an
> unimplemented decision, and an artefact the inventory registers as MISSING are all
> explicitly not failures.

Three divergence classes are counted, never pooled: **SR-1** decision reversed ·
**SR-2** record-fact drift · **SR-3** index/body incoherence. One inverse failure,
**MD-0** manufactured decision, is reported apart from every reversal count. SR-3 is
machine-checked with the session at which each divergence opened; SR-1 and SR-2 are
supplied from `data/survival-audit.json`, a hand-authored, published **input** (the
`qualitative-ratings.json` / `probes/scores.json` pattern) so no re-run can overwrite
author judgment or invent it.

Sessions are git-derived — a maximal run of commits with successive gaps ≤ 4h — because
WS3's log-derived sessions start 2026-05-02 and miss 41 of blive's 53 ADRs. **blive 13
sessions** (19 / 13 / 12 at 2h / 4h / 8h), **btest 83** (96 / 83 / 72).

| | blive | btest |
|---|---|---|
| decision records | 53 ADRs · 35 OQs · 38 frontmatter artefacts | **n/a — no decision-record system** |
| declared reversals | **1** (ADR-021 → ADR-043), declared on both ends | n/a |
| **silent reversals of decision records** | **0** | n/a |
| SR-2 record-fact drift (hand) | 1 | 2 |
| SR-3 index incoherence | 4 | n/a |
| broken anchors | 26 occurrences / **7 distinct targets** / 900 checked | 0 of 0 (no cross-references exist) |
| dangling ID references | **1** (`ADR-054`, a reserved next-free id) | n/a |
| reversal-announcing commits | 8 / 67 = 11.9 per 100 (**8/8 genuine on hand-read**) | 4 / 415 = 0.96 per 100 (**1/4 genuine**) |
| mean commit prose | 362.5 words | 62.7 words |
| instruction rules at HEAD / ever / removed | 25 / 26 / 1 | 46 / 74 / 28 |

1. **The headline is a null, and it is the cheap number PLAN §4 predicted.** No blive
   ADR was found silently reversed: S(k) = 1.000 at every k from 0 to 12. The declared
   curve falls to 0.962 at k=12 on its single supersession. **Read every point with its
   `at_risk` denominator** — k=12 rests on 26 records, not 53. Reporting "97% of ADRs
   survive 12 sessions" without that denominator would be the workstream's easiest lie.
2. **The interesting failures are not reversals — they are records that were wrong on
   the day they were written.** Both projects produced exactly one such defect and
   neither is drift:
   - **blive OQ-035** (2026-06-06, still OPEN, never edited) states "blive's order-type
     surface is `MKT` / `LMT` / `ADAPTIVE_MKT` only … no `OPG`-class order type or
     opening-auction TIF." `types.py` has **seven** `OrderType` members and an `OPG`
     TIF, and `MOC`/`LOC`/`STP`/`STP_LMT`/`OPG` have been there **since the first
     commit**, 41 days earlier, unchanged. *The partial rescue, stated because it is
     real:* the IB adapter's **submit** path builds five order types; MOC/LOC and the
     OPG TIF appear only in the **inbound parse** maps, so "no submit-side OPG wiring"
     is defensible. "Three only" is not, on either reading.
   - **btest CLAUDE.md:102** says `backtest_runner.py (main orchestrator ~2600 LOC)`.
     The file was **1,519 lines the day that was written** and its maximum across all
     18 commits that have ever touched it is **1,618**. The claim has never been true.
   **Neither substrate posture has an instrument that checks a factual claim at the
   moment it is deposited.** That is the sharpest thing WS5 found and it cuts against
   both arms.
3. **The cleanest control in the entire corpus, and it reframes the thesis.** On
   **2026-06-05** the Python floor moved to 3.12 in both repos — same operator, same
   day, same decision, same model era, one repo importing the other. blive recorded
   **ADR-053** (4,902 chars: status/decider/companion, context, five-clause decision,
   alternatives, consequences, cross-refs). btest recorded **commit `fd106f9`** (1,025
   chars) — and it is a *good* record: the reason, the validation (317 tests on 3.12,
   numba/vectorbt/arcticdb wheels confirmed), the exact edits, and a flagged follow-up.
   **The naive story is false: the flat project did write down why.** What differs is
   **addressability** — ADR-053 is cited from **five** artifacts including the one an
   agent auto-loads; btest's reasoning is cited from **zero**, and is reachable only by
   knowing the sha. And ADR-053's `companion:` field names `fd106f9` explicitly: **the
   record for btest's decision lives in blive's substrate, not in btest's.** This is
   consistent with WS4b (recorded facts retrieved near-perfectly in *both* arms; the
   boundary sat at the *why*) and it is the exhibit to build the talk's
   system-representation section on.
4. **Third honest negative: btest's instruction file does not decay silently.** 28 of
   74 rules have been withdrawn, and **zero are unexplained** — 25 in one commit whose
   subject states the scope change (the SMIM extraction), 2 same-commit rewordings, 1
   announced in its subject. The hypothesis going in was the opposite. Rule matching is
   normalised for case and punctuation, so rewording counts as removal + addition,
   biasing the removal count **up** — the negative is conservative, not generous.
   Symmetric detail: blive's CLAUDE.md removed exactly one rule ever, the **same**
   Python-3.11 rule, on the same day, also announced.
5. **The substrate's own index is the thing that goes stale, not its records.** Four
   SR-3 defects, all in `DECISIONS.md`'s index table: ADR-031's row says PROPOSED (body
   ACCEPTED since session 4), ADR-032's says PROPOSED (body ACCEPTED since session 5),
   and **ADR-040 and ADR-041 have no index row at all** — the table carries 51 of 53.
   The sharp part: **blive keeps two ADR status registers and the outer one is right.**
   `CONTEXT_INVENTORY.md`'s KB-10 row reads "ADR-001..053 ACCEPTED, except ADR-021
   SUPERSEDED-BY-ADR-043" — correct. The index *inside* the artefact is the stale one.
   An append-only body is *supposed* to freeze; a Status column is not.
6. **Append-only preserves errors with the same fidelity it preserves decisions.** 26
   broken anchors over **7 distinct targets** — two malformed anchors account for 20 of
   the 26, because a wrong cross-reference is copied forward by every later record that
   cites the same target. One is a genuinely wrong pointer (ADR-039 links `FinancingCost`
   to `cost_margin_dictionary.md#5-financingcost`; FinancingCost is §3, §5 is
   MarginConfig). The slug rule is an approximation of GitHub's unpublished algorithm;
   all seven were re-read by hand against the actual headings first.
7. **Supersession propagates forward, never backward to citations — and this is NOT
   counted as a reversal.** ADR-039 (ACCEPTED, never amended) asserts twice that
   "ADR-021 status: PAUSED (not SUPERSEDED)" and "no decision is reversed"; ADR-021 was
   superseded five days later. Under blive's own CONTEXT_PROTOCOL §5 an ADR is
   append-only and point-in-time, so that statement was true when written and counting
   it as drift would score the discipline as defective for behaving exactly as
   specified. It is published as a **named mechanism**, not a defect count: a reader
   arriving at ADR-039 gets no signal, which is precisely why blive needs the
   CONTEXT_INVENTORY register layered on top of the ADR file.
8. **btest's reversal vocabulary is essentially absent, and the confound must travel
   with the number.** Hand-adjudicated: blive **8/8** automated hits are genuine
   reversal or supersession narration; btest **1/4** (two are statistical "mean-reverting
   ranks" / "revert fast in absolute level", one is about an external FRED tag).
   Adjudicated rates: **blive 11.9 vs btest 0.24 per 100 commits (~50×)**. But blive
   writes 362.5 words of commit prose per commit against btest's 62.7 — normalised per
   10k prose words the *automated* rates are 3.29 vs 1.54, a 2.1× gap. Publish both.
   The number this sits against is WS2's: btest reverses **82.2%** of every line it ever
   added (32.6% within 14 days) against blive's 5.2% / 3.9%, and narrates a reversal
   once in 415 commits. The reversals are not hidden — nothing records them.
9. **blive's declared absences are receipts, and treating them as gaps was a measurement
   bug.** `CONTEXT_INVENTORY` registers INV-2, INV-3, INV-7, INV-12, DD-4, DD-5, DD-6 as
   **MISSING** with a stated future milestone, and INV-11 as DRAFT-inline-in-REQUIREMENTS.
   Scoring those as dangling would have made blive's honesty about its own holes read as
   drift. Counted apart, blive's genuine dangling-reference count over 171 files and 144
   distinct IDs is **1** — `ADR-054`, which `NEXT_PROMPT.md` reserves as the next free id.
10. **Coverage, stated so the null is not over-read.** **18 of blive's 53 ADRs were read
    against the tree** (002, 004, 006, 007, 021, 022, 027, 031, 032, 035, 037, 039, 040,
    041, 043, 044, 049, 053) plus both audited OQs, the MISSING register and the
    supersession graph. The other 35 are either process/scope/deferred-milestone
    decisions with no code surface to contradict them at HEAD, or have a surface that
    was not read this session — **neither group is counted as having survived a test it
    was never given**, and the selection (mechanical checkability + the never-edited
    flag) is disclosed rather than presented as exhaustive.
    29 of 53 ADRs (54.7%) have never been edited after introduction — that is the
    candidate list a silent reversal would hide in, and it is published as candidates,
    not as findings. Checks that HELD are published too (`checks_that_held`, 17 entries)
    so the finding list is not mistaken for the whole audit.

**Hand-verification before the sweeps** (in `_meta.verification`): seven independent
shell counts held exactly — blive ADR headings 53, index rows 51, sessions-at-4h 13
(awk over `%at`), SUPERSEDED statuses 1; btest sessions-at-4h 83, CLAUDE.md rules at
HEAD 46 (independent normaliser), blive strict-reversal commits 8 (independent shell
pipeline). **Four real bugs were caught by that reflex before anything was published**
and are recorded in `_meta.bugs_caught_by_verification`: the declared-MISSING register
scanned whole lines instead of the first table cell (registering KB-2, KB-3, DD-7 and
ADR-034 as missing when all four exist); `STABLE_ID_RE` had no trailing boundary, so
`RETRO-M2-IB` also matched a non-existent `RETRO-M2` — **71 phantom dangling
references**; `gh_slug` collapsed whitespace runs before substituting where GitHub
substitutes each space, calling **758 of 900** anchors broken against a true 26; and
`parse_oqs` read only the first id of blive's combined `### OQ-015 / OQ-018` heading,
making OQ-018 look dangling with 10 citations. An eighth check corrected a number
before it was written: ADR-053's section is 4,902 chars, not the 27,393 an awk-to-EOF
gave, because a Changelog section follows it.

**Caveats that must travel with these numbers:**
- **The survival curve has one arm.** blive is the only corpus project with decision
  records. btest's arm is a *different substrate type* (agent instructions + commit
  prose) reported as such, not a zero on a shared denominator (the WS2 finding-8 `n/a`
  pattern). No shared denominator was forced.
- b-autobot, datacli, smim, harp and seamQ have neither decision records nor an
  inventory register and were **not swept** — including them would have meant carrying
  seamQ's WS3 finding-6 measurement-window caveat and harp/smim's WS0 log-coverage
  caveat for zero decision records.
- **Findings F1 and F5 are the same commit** (`febc4e3`, the 2026-06-06 Phase-2
  readiness audit) and F5 (OQ-033, the manufactured decision) is **carried from WS4b
  finding 7, not independently found**. The three newest records blive ever wrote
  produced two of its five defects — that is one session, n=1, and must be said so.
- The audit is **one reader, once**. No second rater, no agreement number — as with
  WS3's altitude instrument. What is published instead is the receipt trail: 21 of 21
  mechanically checkable receipts are re-verified on every run and report FAILED rather
  than being dropped or corrected.
- Session boundaries are a **git proxy**, not observed sessions. The gap threshold moves
  blive between 12 and 19 sessions and btest between 72 and 96; no finding above depends
  on which threshold is used, but any k-axis exhibit must name the threshold.

**WS5(b), the kernel teaser, was not attempted.** PLAN §4 marks it "cut first" and §8
puts it first in the cut order; a half-baked κ estimate is worse than none, and the
survival arm turned out to need the whole session's reading budget (finding 10). It
remains available as expansion module M-F material if the research continues.

## WS0-bis findings — artefact survivorship (2026-07-26)

**Raised by Oleg, not by an instrument**, at the end of S6: he routinely created
working artefacts — plans, roadmaps, review prompts, iteration notes, research
summaries — that were **not committed and were often deleted**. Every artefact-based
measurement in this eval therefore sees a *surviving* subset. The bias is not noise:
blive's CONTEXT_PROTOCOL requires the substrate to be committed and btest had no such
rule, so **the survivorship correlates with the treatment**.

Measured rather than asserted (`scripts/artifact_survivorship.py`), three independent
channels — typed prompts over the 1,480-turn WS3 corpus · JetBrains LocalHistory change
records · Claude Code tool-call `file_path`s — against every `.md` basename any corpus
repo ever added on any ref (`git log --all --diff-filter=A`, so committed-then-deleted
counts as **surviving**).

| project | observed | committed | **ephemeral (lower bound)** | share |
|---|---|---|---|---|
| **blive** | 33 | 33 | **0** | 0.0% |
| btest | 105 | 66 | **>=26** path-attributed (+13 session-only) | 24.8% path-only · 37.1% incl. session-attributed |
| seamQ | 89 | 56 | **>=33** | 37.1% |
| b-autobot | 10 | 6 | 4 | 40.0% |
| harp | 4 | 2 | 2 | 50.0% |
| datacli | 3 | 2 | 1 | 33.3% |
| shared-substrate | 19 | 17 | 2 | 10.5% |

1. **blive is the only zero, and it is a real zero.** All 33 observed blive artefacts
   are in blive's git, verified by independent enumeration. It is not an artefact of
   low observation — the channels saw 33 of blive's 50 committed `.md` files.
2. **btest's defensible number is 26, not 39.** 13 of the 39 are attributed only by
   session folder, and WS0's OQ-2 already showed several belong elsewhere
   (`ib_algo_engine_requirements_v0.md` is blive's; `handoff_to_new_chat_v2.md` and
   `kickoff_prompt_v2.md` are seamQ's; the `uk_eu_*` files are harp's). Path-attributed
   and session-attributed counts are reported separately and never merged.
3. **seamQ's 33 corroborate WS1 finding 5 through a new channel.** Its adversarial-review
   pipeline (`4a adversarial review of b1.md`, `adversarial_referee_report.md`,
   `hostile_referee_report_v2.md` …) shows up in LocalHistory and was **never committed
   at all** — distinct from the publication-time strip at `e9d951e`, which removed files
   that *had* been committed.
4. **Content is not recoverable; existence is.** PyCharm's LocalHistory on this machine
   holds change records with **no content store**, and the CC transcripts cover only the
   surviving retention window. The March–May working artefacts are gone as text.
5. **Therefore WS1 is NOT re-scored, and that is a decision, not an omission.** A rubric
   axis needs an artefact's contents; a filename cannot distinguish a maintained decision
   log from an empty stub. Any "corrected" score would be invention. The scores stand as
   a measurement of **durable** substrate and `rubric/RUBRIC.md` now carries a scope
   statement saying so.
6. **The framing changes corpus-wide: "flat" → "ephemeral".** btest was not working
   without artefacts; it was working with artefacts that did not survive. That is nearer
   to what the paper argues, since the claim is that the substrate carries state
   *between* sessions — and an artefact deleted at session end carries nothing.
7. **What is unaffected:** WS2 (commit-derived), WS3 (turn-derived) and WS4 (asks what a
   fresh agent can recover *today*, for which deleted files are correctly invisible —
   that is the question, not a flaw). **What is narrowed:** WS5 finding 4 holds for the
   *committed* instruction file only. **What is strengthened:** ASSESSMENT §3.2 — the
   "unsubstrated" arm is even less unsubstrated than the 212-line CLAUDE.md showed.

**Every count is a lower bound and must be published as "at least N".** A file created,
used and deleted without ever being typed in a prompt or written by an agent tool call
is invisible to all three channels. The instrument is conservative in three further
ways, all of which shrink the finding: the committed pool is the **union** over all
corpus repos (so a file that moved btest → smim resolves as committed), matching is on
basename only, and channels A and C see only what was named or tool-written.

**Hand-verification** (in `_meta.verification`): all 33 blive artefacts independently
confirmed present in git; `eodhd_uk_eu_migration_plan.md` and
`data_acquisition_prompts.md` confirmed absent from every corpus repo by a per-repo
shell loop. **Two regex bugs were caught by hand-reading the first output** — a path
pattern that ran greedily across sentence text and manufactured an artefact called
*"btest only, plan a safe doc-reorganization … eodhd_uk_eu_migration_plan.md"*, and a
token floor that admitted the prose fragments `_v2.md` and `_v3.md`.

**A fragility ledger was added to ASSESSMENT §5.1** in the same session, answering the
standing worry that the corpus derives too much from single events. It is true of about
seven findings and false of about five, and the split is structural: **every robust
finding measures the operator's behaviour repeated over hundreds of sessions; every
fragile one measures an agent's behaviour on one question.** §4's reframe is carried
entirely by the robust half. Two rules now bind S8/S9: nothing fragile leads a section,
and no two fragile findings are aggregated to imply a rate.

## WS6 findings — drift archaeology (2026-07-26)

Output: **[`report/war-stories.md`](./report/war-stories.md)** — four stories, each with
the same four beats (incident with a receipt → what it cost → the discipline element that
exists because of it, or the absence where none was created → what it generalises to), a
receipts index of 23 lines, and an explicit limits section. No script; narrative judgment
over evidence the prior six sessions instrumented. Every story is placed as colour behind a
named robust number, per ASSESSMENT §5.1.

**The four stories.**

1. **KB-7 — the hole named forty days before anything fell into it.** The M3.5 chaos drill
   (`a2c78f5`, 2026-06-05) found `IBBroker.is_connected` stale-`True` on an unexpected
   drop, recovery needing an explicit `disconnect()+connect()`, and IB error 10141 on
   restart. It filled `KB-7 failure_modes`, MISSING → DRAFT v0.1. **The substrate point is
   the registration, not the drill:** KB-7 was registered MISSING in `CONTEXT_INVENTORY.md`
   at `13f6997`, blive's *first* commit, with a content contract and an owner. An inventory
   that can hold a **typed absence** turns "what don't we know about our failure modes"
   into a dated work item. Same mechanism as WS5 finding 9.
2. **The option that was not on the list.** At M3.3 the agent's OQ-031 option set —
   accept / Pro-Client / de-lever / mean-revert — omitted the *leverage-preserving* path,
   and the operator caught it (`M3_retrospective.md:63`). The scope was reframed as the
   trilemma that now spines OQ-032; ADR-052 introduced the `refined-by:` backref. **The
   twist is where the general lesson went:** the retro routes it explicitly to
   *agent memory* — "Captured in agent memory; not ADR-worthy on its own"
   (`M3_retrospective.md:113`) — and the file exists, quoting the operator verbatim
   (`~/.claude/projects/…-blive/memory/feedback_surface_full_option_space.md`). The fix for
   the incident is the least durable artefact in the story: not in git, not versioned, not
   portable across harnesses, and invisible to this eval's own instrument (finding 5).
3. **One session, two defects, in the project that scores 22/24** — the negative, and the
   best story in the file. `febc4e3` (2026-06-06) is a substrate-only session by its own
   commit body ("single-mode, no code … Tests unchanged (591)"), and it produced both
   OQ-033's manufactured decision (WS4b finding 7) and OQ-035's false order-type claim
   (WS5 finding 2). **New detail found this session: OQ-035 cites the record that refutes
   it.** It says "INV-2 (order types) and INV-3 (TIFs) are MISSING per CONTEXT_INVENTORY
   §3"; the INV-2 row (`CONTEXT_INVENTORY.md:99`) lists "MKT, LMT, MOC, LOC, STP, STP_LMT,
   **OPG**, IOC, FOK" and, verified by `git log -S`, **has never been edited since
   `13f6997`**. The record read the pointer's *status* and never its *content*. Paired with
   btest's `CLAUDE.md:102` "~2600 LOC", the cross-arm statement is: **neither posture has
   an instrument that checks a factual claim at deposit time; every check either project
   has runs at retrieval.** Kept fair by a control from the same substrate one day earlier —
   M3.4's `AccountSnapshot.equity` bug was logged "Bug-fix, **no ADR** (DD-1 already
   specified equity = total NAV)". The substrate correctly declined to manufacture a record
   on 06-05 and manufactured one on 06-06.
4. **104,959 lines, and the reasoning is in a chat log** — the btest mirror. On 2026-05-02
   the operator typed the extraction rationale at 09:35 (748 chars, sha1 `e66460c50699`),
   pasted back a 6,806-char engineered prompt at 09:43 whose first instruction is *"make
   sure you first create a plan and other context md files"* (sha1 `3a39b4ff5c61`), and at
   13:27 committed `7d9b86f`: **387 files, +292/−104,959, commit body empty (1 byte)**.
   **Not an absence of capture:** the same commit added four Architecture Rules to
   `CLAUDE.md` (`:173-174`, `:184`) that are still at HEAD and still true. *The capture
   mechanism you have determines the shape of what survives* — an instruction file captures
   **rules** (imperative, undated, no alternatives) and structurally cannot capture a
   **decision** (dated, with a decider and losing options and a citable id). The plan files
   the operator asked for are in the ephemeral class; the reasoning survives only because a
   Copilot store covering 2026-03-20 → 05-31 was retained.

**Two published exhibits were corrected by the archaeology. Both corrections run *against*
the hypothesis and are the substance of this session.**

5. **WS0-bis is over-counted: btest's ephemeral floor is ≥10, not ≥26.** ASSESSMENT §5.1
   listed the survivorship finding as robust with the note "individual names are
   spot-checkable". They were spot-checked, and **16 of btest's 26 path-attributed names
   are false positives** in three classes: **7 Claude Code auto-memory files** (durable on
   disk under `~/.claude/projects/*/memory/`; `artifact_survivorship.py:113` states in its
   own comment that these are "agent state, not deposits" but `NON_SUBSTRATE` excludes only
   the literal `memory.md` index — one of the seven is shared-substrate's, mis-attributed);
   **5 slash-flattened duplicates** of `docs/smim/*.md` files verified committed in *both*
   btest and smim; and **4 basenames spliced** out of LocalHistory's binary
   `changes.storageData`. Corrected: **blive 0 of 33 · btest ≥10 of 94 (firm floor 8) ·
   seamQ ≥33 of 89** — b-autobot **4 → 0** (three are Maven-generated licence files under
   `target/reports/apidocs/legal/`, the same vendored tree as WS2 finding 5), shared-
   substrate **3 → 1**; **seamQ's 33 and blive's 0 are unchanged** and seamQ's list is clean
   on hand-read. Two structural points: **every false-positive class inflates an ephemeral
   count and blive's is 0, so the instrument's noise is one-directional and runs with the
   hypothesis**; and the auto-memory class can only reach a project with surviving
   transcripts — **btest 10 `.jsonl`, shared-substrate 3, datacli 2, blive 0, b-autobot 0**
   — so blive's ten memory `.md` files were structurally unobservable. Itemised, with
   receipts, in `data/survivorship-audit.json` (a published **input**;
   `artifact-survivorship.json` is not edited and the script is not re-run, per METHODS
   rules 2 and 8). **The finding is narrowed, not withdrawn** — its primary evidence is
   Oleg's own disclosure, and every count was published as a lower bound.
6. **WS2's tag-decay curve is largely a composition change, and its "peak" is the month the
   ids disappeared.** Every published number reproduces (293 bracket-tagged of 415, and the
   monthly shares 0 → 91 → 96 → 50 → 40 → 0%); what they mean does not survive the
   breakdown. **(a)** 280 of the 293 are `[SMIM]`, and SMIM left the repo on 2026-05-02 in
   `7d9b86f` — the 96% → 50% fall is mostly tagged work moving to another repository.
   btest's own `[btest]` convention ran for exactly **9 commits**, so the residual decay
   claim rests on 29 commits, not 415. **(b)** Of the 293, only **165 carry a scoped stable
   id** inside the bracket (`[SMIM DATA-6]`, `[SMIM M4.5-T1]`): **163 in March, 2 in April,
   0 after**. April — the published "peak" — is 88 commits tagged `[SMIM]` with no id at
   all. **(c)** July is not untagged, it is *differently* tagged: **9 of 10 July commits
   carry a conventional-commit prefix**, and on "any structured subject prefix" the curve
   reads 0 · 96.3 · 96.7 · 64.3 · 100 (n=5) · 90% — adoption in March, sustained.
   All five counts reproduced exactly by independent shell greps (293 · 165 · 280 · 9 · 9).
   **The defensible claim is narrower and better:** btest adopted a stable-ID convention in
   March, stopped scoping it to ids in April, and lost it when the subproject that owned it
   was extracted; what replaced it is a **taxonomy, not an address**. `feat(costs):` tells
   you a commit's kind; `[SMIM DATA-6]` tells you what it is about and lets a later record
   cite it. The published phrasing invites "btest stopped being disciplined", which the
   evidence does not support.

**What was cut, and named in the file rather than dropped:** b-autobot's 9,248 committed
`node_modules` files (fails beat three — a missing `.gitignore` line is not a substrate
property). **Demoted rather than cut:** the `AccountSnapshot.equity` bug → DD-1 v0.3, one
of PLAN §4's three named spine items — as its own story its third beat is a doc version
bump plus a regression test, which any tested project produces; it is far more useful as
the control inside story 3.

**Caveats that must travel with WS6:**
- **Every story is n = 1**, by construction. None leads a section, none is aggregated with
  another (ASSESSMENT §5.1 rules 1 and 2), and each names the robust number it stands
  behind: story 1 → §3.4 rework; story 2 → §3.5 length-banded altitude; story 3 → §3.1 the
  pre-registered null; story 4 → §2.1 the retransmission tax.
- **Three of the four stories are blive's**, because blive is the only corpus project with
  a retro series and an amendments log to read incidents out of. That is a selection
  property of the evidence, not a finding about the projects.
- **One reader, once** — no second rater, as with WS3's labels and WS5's audit. The
  mitigation is the receipts index, not an agreement number.
- **Story 3's "audit sessions have no execution feedback loop" is a mechanism observed in
  one session**, stated with its n and offered as a cheap-to-test hypothesis (require every
  factual claim in an audit record to carry the file:line it was read from). It is not a
  rate and not evidence that audit sessions are generally unsafe.
- **Story 4's central receipt survives by retention accident** — the JetBrains Copilot
  store covers 2026-03-20 → 05-31 only.
- Findings 5 and 6 are **corrections to published exhibits, not new measurements**. Neither
  re-runs an instrument; both are hand adjudications with per-item receipts, and both make
  the corpus's numbers smaller.

## S8 findings — report assembly (2026-07-26)

S8 wrote nothing new by design; its findings are assembly decisions, recorded so S9
inherits them rather than re-deciding.

1. **`report/REPORT.md` maps 1:1 onto PLAN §9's core arc** (five sections: the case cold ·
   the frame · four practices · the research examined · interactive), so each section
   lifts into slides without re-deciding placement. Every exhibit in it carries the
   number, its denominator, the caveat, and its `data/` pointer; war stories appear only
   as named cross-references after the robust number each stands behind (1→rework ·
   2→length-banded altitude · 3→the pre-registered null · 4→retransmission tax).
2. **`report/exhibits.md` is the bench PLAN §9 promised** — 23 exhibits in five groups
   (A robust leads · B corrected captions · C honest negatives · D fragile texture with n
   stated · E context), each with a one-line honest caption, source file and the caveat
   that travels. It opens with the caption rules: ASSESSMENT §5.1's three rules plus the
   eight never-without-qualifier numbers. It also names what is deliberately absent
   (P8 instrumented numbers, WS3(c), WS5(b), smim's history metrics).
3. **Placement decision forced by rule 1 vs NEXT_TASK's phrasing, resolved toward the
   rule.** NEXT_TASK said to "build the system-representation section on" the Python 3.12
   pair, but the pair sits in the fragile table (n=1 by construction). §3.3 therefore
   *leads* with the two robust results (recorded-slot retrieval 28/28 · 28/28 · 24/28,
   and the survival null S(k)=1.000 with at_risk denominators) and places the pair after
   them as the labelled case study that shows what differs (addressability). Same logic
   throughout: no section leads fragile.
4. **The confounds ledger is written out in REPORT §4.5** — all six PLAN §7 items, with
   confound 6 in its S7-corrected form (blive 0/33 · btest ≥10 of 94 · seamQ ≥33/89 ·
   b-autobot 0 · harp 2, plus the two instrument properties). The two S7 downward
   corrections and the "each adversarial read shrank the numbers" trend are stated in
   §4.3 as corrections to the evaluation itself, alongside the four honest negatives —
   listed separately, never aggregated.
5. **Both S7 corrections are absorbed as instructed:** REPORT cites the corrected
   survivorship figures and names `data/survivorship-audit.json` as where the correction
   lives (`artifact-survivorship.json` untouched); the tag-decay exhibit appears only
   retitled ("a stable-ID convention replaced by a taxonomy"), with the caption rule
   "never show 0%-in-July as an absence of discipline" attached in both files.
6. **P8 stays on the strict surface:** REPORT §1 describes the work project only as "a
   legacy component at a regulated financial institution" with the abstract's stated
   outcome shape (2 weeks, 19 gated increments, parity, UAT) and the provisional 18/24
   rubric row; no employer name, no component name, no instrumented numbers. The A5
   lowest-confidence flag travels with the row.
7. **No miner was re-run, no output edited, no judgment file touched.** S8 read and wrote
   markdown only.

Caveats that travel with S8's own output:
- REPORT.md is synthesis, not measurement — where it and a `data/` file disagree, the
  data file wins and the disagreement is a bug to fix in REPORT.
- The exhibit-bench captions are one author's compression of caveats recorded across
  STATE/ASSESSMENT; S9 must not shorten a caption further without re-checking the
  underlying caveat.
- The still-open reconcile-before-talk items are carried in NEXT_TASK.md, not closed
  here (Requirements v0 word count; survivorship-script future fixes; the audit-session
  `file:line` hypothesis).

## S9 findings — deck + dry run (2026-07-26)

S9 wrote the talk folder and reconciled one standing discrepancy; no instrument was run,
no `data/` file was touched.

1. **The three deliverables exist** in `talks/does-the-substrate-matter/`:
   - **`slides.md`** — Marp deck matching `docs/presentation.md`'s conventions. Core arc
     (38 slides) mirrors REPORT §§1–5 section for section; expansion modules M-A…M-F sit
     behind an explicit "everything after this slide is optional" divider. Binding rules
     applied throughout: every number slide carries its caveat and denominator **on the
     same slide**; slide titles follow the exhibit bench's honest captions and are not
     sharpened beyond them; group-D exhibits appear only after the robust number they
     illustrate, with their n on the slide; each of REPORT §4.3's four honest negatives
     has its own slide; the S8 §3.3 ordering (robust → robust → null → concession →
     n=1 case study) is kept.
   - **`handout-rubric.md`** — the one-page self-score handout: Step-0 complexity check
     ("stop: flat notes are the right tool"), the eight questions with 0–3 anchors, the
     /24 reading bands, and the dispatch-vs-continue closing question.
   - **`NOTES.md`** — the branch-point map (expand/compress triggers per module, with
     the five never-cut slides named), the thirty-second origin anecdote scripted to
     thirty seconds, per-slide "if challenged" lines for the null / rework confound /
     survivorship correction / tag curve / altitude / rubric circularity / P8 row (each
     pointing at the REPORT/ASSESSMENT answer, concession first), and the dry-run
     checklist.
2. **The deck-side dry run was executed as a caption/caveat audit** — every number on
   every slide checked against `report/exhibits.md` and REPORT. It caught one real
   defect: **exhibit A1's bench caption said "twice as often"; the data and REPORT §2a
   say the ephemeral project warms up half as often** (warm-up prefix 0.53 vs 1.00) at
   4× the cost. The bench caption is corrected with an inline provenance note; REPORT
   needed no change. Two caption-rule applications were also tightened on the slides:
   the survival slide names the 4-hour session-proxy threshold (rule: any k-axis names
   it), and the survivorship table keeps the "firm floor 8" qualifier.
3. **Reconcile-item 1 (Requirements v0 word count) is CLOSED, and the resolution is more
   interesting than either side of the discrepancy.** Measured this session: the
   claude.ai-authored v0 draft (`~/Downloads/ib_algo_engine_requirements_v0.md`,
   2026-04-26) is **3,375 words** and genuinely flat; the REQUIREMENTS.md actually in
   blive's first commit (`13f6997`, same day) is **5,757 words** — and is already
   **v0.2, post-KB pass**, cross-referenced with stable IDs, i.e. no longer flat
   (unchanged at HEAD). The paper's sentence ("flat, around six thousand words, the
   practitioner's first pass") conflated the flat first pass with the deposited state,
   and its later "became substantially shorter" is **unverifiable** — v0.1 was never
   captured anywhere, itself an instance of the ephemeral-artifact class (confound 6).
   Fixes applied to the canonical copies in this repo: `paper/shared_substrate.tex`
   now reads "around three and a half thousand words" and drops the "substantially
   shorter" claim (keeping the verifiable collapse-into-references description);
   `docs/presentation.md` field note 1 likewise (~3,400-word first deposit; "narrative
   sections collapsed into stable-ID references"). The frozen archive copy
   `paper/archive/cognitive_cartography.tex` is deliberately untouched. **If Oleg's
   memory says v0.1 was in fact ~6k words and shrank, the "shorter" sentence can be
   restored with that provenance stated — the current text claims only what a receipt
   supports.**
4. **The public-surface rule is applied to the new artifact class:** committed
   `slides.md`, `NOTES.md` and `handout-rubric.md` describe P8 only as "a legacy
   component at a regulated financial institution" (2 weeks, 19 gated increments,
   parity, UAT, 18/24 provisional); NOTES.md marks the two places to **name it
   verbally** in the room.
5. **Figures:** the deck reuses the repo's `assets/fig-*.png` (centroid, hierarchy,
   divergence, loop); no new charts were rendered — numbers are shown as on-slide tables
   so each caveat sits physically next to its number. `talks/.../assets/` stays empty.

Caveats that travel with S9's output:
- **The deck is a compression; the bench remains binding.** Where a slide and
  exhibits.md disagree, exhibits.md wins and the slide is the bug (same rule as
  REPORT-vs-data).
- **Slide numbers in NOTES.md refer to the current slide order** — any deck edit must
  re-check the branch-point map's and if-challenged lines' numbering.
- **The live branch-point rehearsal is Oleg's and has not happened** — the dry run S9
  could execute is the caption/caveat audit; the rehearsal checklist is at the end of
  NOTES.md. OUTLINE.md's last checkbox stays open until it has.
- The A1 caption fix is a **markdown correction of a bench transcription error**, with
  the correction noted inline in exhibits.md — no `data/` output was edited.

## Session log

- **S1 · 2026-07-25:** PLAN.md drafted and iterated (talk reframed to abstract; corp
  round-trip made explicit; timeboxes removed; talks/ scaffolded; anonymisation rule
  applied + saved to memory). WS0 executed: `scripts/evidence_audit.py` written and run →
  `data/evidence-map.json`. WS1 executed in same session (already warm): rubric instrument
  + handout drafted; 5 parallel repo sweeps → evidence notes → DRAFT scores. Next: **Oleg
  reviews scores**; then **WS2 + WS-X (git miners + complexity profiles)** in a fresh
  session.
- **S2 · 2026-07-25 · Opus 5:** WS2 + WS-X executed. Wrote `scripts/corpus_common.py`
  (shared source-file / vendored-path classification), `scripts/git_miner.py` (7 metrics)
  and `scripts/complexity_profile.py` (5 primitives + Kendall's W in 3 sensitivity runs);
  swept all seven repos → `data/git-metrics/*.json` + `data/complexity-profiles.json`.
  Findings above. Hand-verified 5 metrics against independent counts before the sweeps,
  which caught 3 real bugs (dotfile LOC undercount; ID-tag regex missing btest's
  `[SMIM DATA-6]` form — 110 vs 293; AIT concatenation order). Two definitional
  extensions were forced by the data and are documented in-script: root hygiene needed an
  on-disk scratch count because btest gitignores its litter, and short-horizon churn
  needed a `rework_share_any_horizon` companion plus a `window_exceeds_history` flag
  because four of seven projects are shorter than the 14-day window. Corrected WS1
  finding 2's "last 30 commits" phrasing (it is the last 13). Then closed the two open
  workstreams with Oleg: **WS-X's 21 declared ratings set** (via a new
  `data/qualitative-ratings.json`, kept as a script *input* so a re-run cannot wipe them —
  Kendall's W confirmed unchanged, proving they enter no computation), and **WS1's four
  flagged judgment calls adjudicated** (two down: b-autobot A3, harp A6; two upheld).
  Finally closed **all three open questions**: OQ-1 answered from filesystem + git evidence
  (PyCharm 2025.2 + JetBrains AI Assistant, metered quota, no recoverable transcript — the
  corpus's unsubstrated baseline), OQ-3 answered negative (b-autobot's Copilot logs
  confirmed lost), OQ-2 answered partially (no transcripts recoverable, but blive's
  Requirements v0 and two seamQ session-handoff artifacts located in `~/Downloads` and
  catalogued for WS3/WS6). P8's four blanks filled PROVISIONAL-INFERRED → 18/24.
  **Nothing is now pending on Oleg.** Next: **WS3 session-log analysis (S3, Opus 5)** — the
  altitude classifier.
- **S3 · 2026-07-25 · Opus 5:** WS3 executed end to end. Wrote `scripts/log_miner.py`
  (three log formats → one session/turn schema, with content+window project
  re-attribution), `scripts/sample_turns.py` (deterministic stratified draw),
  `scripts/altitude_classify.py` (WS3a+b) and `scripts/session_yield.py` (WS3c);
  added session-log plumbing to `corpus_common.py`. Hand-labelled 99 stratified turns
  *before* writing any classifier, froze `rubric/ALTITUDE.md` v1.0 (nine numbered
  boundary rules), then scored the automated pass against the labels on a
  pre-assigned dev/held-out split: **held-out 0.895 four-way (κ=0.835), 0.947
  high/low (κ=0.902)**, with the pre-fix run published too. Three hand-verifications
  ran before the sweeps (per-folder grep counts, Copilot turnId dedup 73→65,
  history-vs-transcript cross-check 9/11 exact with both deltas explained); two real
  defects were caught by hand-reading rather than by counts — pre-extraction smim
  turns being stolen from btest, and a printer-support session counted as btest
  operator work. Findings above. The headline moved: the raw altitude ordering is a
  **verbosity artefact**, and the defensible exhibits are the length-banded
  comparison, the short-turn composition, and WS3(b)'s bounded-vs-growing warm-up
  cost. WS3(c) is inconclusive by construction and says so. Two WS0 numbers
  corrected (the b-autobot bleed, the Copilot user-message count). Next:
  **WS4a probe pre-registration (S4, Fable 5)** — question design, frozen by commit
  before any probe runs.
- **S4 · 2026-07-25 · Fable 5:** WS4a executed — question design + freeze, nothing run.
  Warm-up per NEXT_TASK, then three parallel read-only evidence sweeps (blive, btest,
  b-autobot) + a mine of the classified session-log turns for decisions made only in
  conversation. Every candidate receipt was re-verified before freezing, and the absence
  checks were extended to **git history** (`git log -S`, deleted-file contents) because the
  probe subject gets git access — that check killed two b-autobot traps (combobox: 54
  history hits; M6/corp-env: contested by the deletion commit's blanket claim) and both
  rejections are recorded in questions-p3.md. PROTOCOL.md written in the ALTITUDE house
  pattern (numbered rules, precedence, stated biases, sensitivity run, conservative
  tie-break); the scoring rubric distinguishes invention / contradiction / false-absence,
  and SC9 publishes the headline both with and without false-absence counted as
  confabulation. **Pre-registration commit `ab9c62d` contains exactly the four instrument
  files; no probe question has been put to any agent.** Findings above; WS6 receives the
  conversation-only decision list. Next: **WS4b probe runs + scoring (S5, Sonnet 5)** —
  execute the frozen protocol, then score, then `data/probe-results.json`.
- **S5 · 2026-07-26 · Opus 5:** WS4b executed. Wrote the H5 driver
  (`scripts/probe_driver.py`) and its H1 enforcement hook (`scripts/probe_guard.py`);
  both extract F1–F6 and all 60 questions **from the frozen files at run time**, so no
  probe text was ever retyped and the keys never entered a session. H9 verification
  first: all three repos sat at their pinned HEADs, 15 commit receipts plus the
  history-only P3-Q16 receipt re-resolved by hand, and blive's dirty tree (paper drafts
  under `docs/method/paper/`) grepped for all 13 P1 answer tokens — zero hits, nothing
  voided at that stage. H8 shakeout on datacli passed all three checks. Then six
  sessions in the pre-registered order, config reset to the pristine snapshot before
  every one. Findings above; the headline is a **null on H-1**. Three things went wrong
  and are published rather than patched: a driver bug voided the first b-autobot run 1
  (H7 restart, session preserved), a surplus F3 nudge was sent to btest-run1 after the
  operator applied a stricter orientation standard to btest than to the other two (rule
  **R-O3** now states the standard; the error is disclosed and its cost excluded from
  H-3), and **P1-Q07's frozen absence check turned out to be false** at the pinned HEAD,
  voiding that question in both blive runs. The most useful outputs are not the null
  itself but finding 6 (both non-b-autobot failures are the same "invent the *why*"
  shape) and finding 7 (btest's 212-line CLAUDE.md means the "flat" arm is not flat —
  a confound large enough to explain the null on its own). **SC8 review completed the
  same session, with Oleg**, and it changed the result: he had no memory of settling
  b-autobot's feature-file naming convention, confirmed sfera was never considered as a
  blive data source, and identified btest's no-skips instruction as *situational* rather
  than a policy adoption. That converted two more questions to voids (P3-Q01, P2-Q07,
  both runs) on the **Tier A/B evidence rule** adopted at review — a decision inferred
  from a diff may ground a claim about code state, never a claim that "we decided X".
  Post-review: btest 38/38 correct, b-autobot 36/38 with 0 confabulations, blive 37/38
  with **the corpus's only confabulation**. H-1 stays null at p=1.0 with its nominal
  direction reversed. Voiding on operator memory is recorded as a **declared extension**
  to the frozen protocol. The two most useful outputs are finding 9 (**DEC-N2 is 0 for
  3** — no project yielded a decision that lived only in conversation) and finding 7
  (blive's OQ-033 formalised a standing default into a dated "Operator decision", a
  substrate failure mode for WS6). **Nothing is now pending on Oleg.** Next: **WS5
  survival curves (S6, Sonnet 5)**.
- **S6 · 2026-07-26 · Opus 5:** WS5(a) executed. Wrote `scripts/survival.py` (sessions,
  record inventory + first-appearance mining, right-censored survival curves,
  index/body coherence, supersession-graph backlinks, reference + anchor integrity,
  freshness clock, commit-message reversal archaeology, instruction-rule survival) and
  the hand-audit input `data/survival-audit.json` → `data/survival.json`. **The
  definition of "silent reversal" was frozen in the script docstring before the
  measurement was written**, and the declared-vs-silent boundary is what the whole
  result turns on: blive's append-only substrate makes a *declared* supersession the
  discipline working, so counting it would have measured the opposite of the subject.
  Seven independent shell counts held exactly before the sweep; **four real bugs were
  caught by that reflex first** — a register that scanned lines instead of table cells,
  an ID regex that manufactured 71 phantom dangling refs out of `RETRO-M2-IB`, a slug
  rule that called 758 of 900 anchors broken against a true 26, and a heading parser
  that missed blive's combined `OQ-015 / OQ-018` question. An eighth check killed a
  27,393-char figure that was really 4,902.
  **The headline is a null: zero blive ADRs silently reversed, S(k)=1.000 at every k.**
  Three results matter more than the null. (1) Both projects' only real fact-drift
  defects were **wrong on the day they were written** — blive's OQ-035 about code
  unchanged since commit 1, btest's "~2600 LOC" about a file that has never exceeded
  1,618 — so neither posture checks a claim at deposit time. (2) The **Python 3.12
  pair** (2026-06-05, same operator, same day, both repos) is the cleanest control in
  the corpus and it **reframes the thesis**: btest *did* record why, well, in a
  1,025-char commit body; what it lacks is **addressability** — ADR-053 is cited from
  five artifacts including the auto-loaded one, btest's reasoning from zero, and
  ADR-053's `companion:` field means the record for btest's decision lives in blive's
  repo. (3) A **third honest negative**: btest's instruction file does *not* decay
  silently — 28 rule removals, zero unexplained. The one class that did fail in blive
  is its **own index table** (2 stale statuses, 2 missing rows) while the outer
  CONTEXT_INVENTORY register is correct, plus 7 distinct broken anchors propagated by
  copying. ADR-039's stale citation of ADR-021 was deliberately **not** counted as a
  reversal and is published as a named mechanism instead. **WS5(b) kernel teaser not
  attempted** (PLAN §8 cut order; the audit reading consumed the budget).
  **Then Oleg raised the eval's most serious methodological problem** — that he
  routinely created working artefacts and never committed them, often deleting them —
  which makes every artefact-based measurement a survivorship sample whose bias runs
  *with* the hypothesis. Rather than re-run WS2–WS5 (deterministic on unchanged git;
  identical output), S6 added **WS0-bis**: `scripts/artifact_survivorship.py` measures
  the gap across three independent channels → **blive 0 of 33, btest >=26, seamQ >=33**,
  all lower bounds. Recovery of *content* was probed and is not possible (LocalHistory
  has no content store; CC transcripts cover only the retention window), so **WS1 is
  deliberately not re-scored** — a filename cannot distinguish a decision log from a
  stub. Instead: PLAN §7 gains **confound 6**, RUBRIC.md gains a **scope statement**,
  ASSESSMENT gains **§2.6 / §3.8** and the corpus-wide framing changes from *flat* to
  **ephemeral**. Oleg's second concern — that too much rests on single events — became
  **ASSESSMENT §5.1, a fragility ledger**: ~5 robust findings vs ~7 single-event ones,
  split structurally along human-side-repeated vs model-side-one-shot, with §4's reframe
  shown to rest entirely on the robust half. **Nothing is pending on Oleg.** Next:
  **WS6 archaeology (S7, Opus 5)**.
- **S7 · 2026-07-26 · Opus 5:** WS6 executed. Created `report/` and wrote
  **`report/war-stories.md`** — four stories with receipts, each on the same four beats,
  plus a 23-line receipts index and a limits section. Spine per PLAN §4: blive's retro
  series read against the incidents that forced each discipline element (chaos drill →
  KB-7; the OQ-031 option-set omission → OQ-032's trilemma + `refined-by:` + an
  agent-memory rule), then the btest mirror (the SMIM extraction). The negative NEXT_TASK
  asked for is story 3 and it got sharper: **OQ-035 cites the very row that refutes it** —
  `CONTEXT_INVENTORY.md:99`'s INV-2 description lists OPG and has never been edited since
  the initial commit, so the record consulted the pointer's status and never its content.
  Story 3 is kept fair by a control from the same substrate one day earlier (M3.4's
  "Bug-fix, **no ADR**"), which is also why PLAN §4's `AccountSnapshot.equity` spine item
  was **demoted rather than cut**. Two stories were rejected and are named in the file.
  **Then the archaeology turned on the eval's own numbers, and that is the session's
  substance.** ASSESSMENT §5.1 had listed the survivorship finding as robust with the note
  "individual names are spot-checkable"; spot-checking them showed **16 of btest's 26
  path-attributed names are false positives** in three classes — 7 Claude Code auto-memory
  files (durable on disk; the script's own comment at line 113 says these should be
  excluded, but `NON_SUBSTRATE` catches only the `memory.md` index), 5 slash-flattened
  duplicates of `docs/smim/*.md` files verified committed in both btest and smim, and 4
  basenames spliced out of LocalHistory's binary store. **btest ≥26 → ≥10 of 94; b-autobot
  4 → 0; shared-substrate 3 → 1; seamQ 33 and blive 0 unchanged.** Two structural points
  came with it: every false-positive class *inflates* an ephemeral count and blive's is 0,
  so the noise is one-directional and runs **with** the hypothesis; and the auto-memory
  class can only reach a project whose transcripts survived — btest 10 `.jsonl`,
  shared-substrate 3, datacli 2, **blive 0, b-autobot 0** — so blive's ten memory files
  were structurally unobservable. Published as the hand-audit input
  `data/survivorship-audit.json`; `artifact-survivorship.json` was **not** edited and
  `artifact_survivorship.py` was **not** re-run (METHODS rules 2 and 8), with five concrete
  fixes recorded for any future run. Separately, the WS2 tag-decay curve was broken down:
  every published number reproduces, but **280 of 293 tags are `[SMIM]` and SMIM left the
  repo**, only **165 of 293 carry a scoped stable id (163 Mar, 2 Apr, 0 after)**, and
  **9 of 10 July commits carry a conventional-commit prefix** — so the "96% April peak" is
  the month the ids vanished and "0% July" is a convention change, not an absence. Five
  independent shell greps reproduced 293 · 165 · 280 · 9 · 9 exactly. Both corrections make
  the corpus's numbers **smaller**. ASSESSMENT §2.5, §2.6, §5.1, §6 and §7 revised
  accordingly. **Nothing is pending on Oleg.** Next: **report assembly (S8, Fable 5)**.
- **S8 · 2026-07-26 · Fable 5:** Report assembly executed. Warm-up per NEXT_TASK
  (METHODS v1.1 → ASSESSMENT → STATE → war-stories → PLAN §6/§7/§9), then two files
  written and nothing re-run: **`report/REPORT.md`** — five sections mapping 1:1 to
  PLAN §9's core arc, every exhibit with number + denominator + caveat + `data/`
  pointer, war stories as cross-references only, the confounds ledger written out in
  full with confound 6 corrected, METHODS §9's cannot-answer list carried in as §6 —
  and **`report/exhibits.md`** — the appendix bench: 23 exhibits in five groups, each
  with an honest one-line caption, source and travelling caveat, opening with the three
  ASSESSMENT §5.1 rules and the eight never-without-qualifier numbers. The one judgment
  call worth recording: NEXT_TASK's "build §3.3 on the Python 3.12 pair" was resolved
  in favour of §5.1 rule 1 — the section leads with the robust retrieval and survival
  numbers and the pair follows as a labelled n=1 case study. Both S7 corrections are
  absorbed (corrected survivorship figures cited with their audit-file provenance; tag
  curve appears only retitled). S8 findings above; NEXT_TASK.md rewritten for S9.
  **Nothing is pending on Oleg.** Next: **deck + dry run (S9, Fable 5)** —
  `talks/does-the-substrate-matter/`.
- **S9 · 2026-07-26 · Fable 5:** Deck + dry run executed. Warm-up per NEXT_TASK (REPORT →
  exhibits → OUTLINE/ABSTRACT → PLAN §9 → war-stories), then the three deliverables
  written into `talks/does-the-substrate-matter/`: **`slides.md`** (Marp, house
  conventions; core arc of 38 slides mirroring REPORT §§1–5 in order, modules M-A…M-F
  behind an explicit optional divider; every number slide carries caveat + denominator
  on the slide; titles held to the bench's honest captions; the four honest negatives
  each get their own slide; S8's §3.3 ordering kept), **`handout-rubric.md`** (Step-0
  complexity check + 8 axes + reading bands + closing question) and **`NOTES.md`**
  (branch-point map with the five never-cut slides named, the 30-second origin anecdote
  scripted, per-slide if-challenged lines pointing concession-first at REPORT/ASSESSMENT,
  dry-run checklist). The dry run S9 could run — a caption/caveat audit of every number
  slide against the bench — caught **one bench defect: exhibit A1's caption said "twice
  as often" where the data and REPORT §2a say half as often** (warm-up prefix 0.53 vs
  1.00); fixed in exhibits.md with inline provenance. **Reconcile-item 1 closed by
  measurement:** the flat claude.ai v0 draft is 3,375 words, but what blive's first
  commit actually deposited is v0.2 at **5,757 words, already stable-ID cross-referenced**
  — the paper conflated the two states, and its "became substantially shorter" is
  unverifiable because v0.1 was never captured (itself confound-6 material). Canonical
  fixes applied in-repo (`paper/shared_substrate.tex` → "around three and a half
  thousand words", "shorter" claim dropped; `docs/presentation.md` field note aligned);
  the archive tex left frozen. Public-surface rule applied to the whole talk folder
  (P8 anonymised; NOTES marks "name verbally"). OUTLINE.md checkboxes updated; the one
  open box is the **live branch-point rehearsal, pending on Oleg** (checklist in
  NOTES.md). NEXT_TASK.md rewritten as the **post-talk brief** (P8 work-side leg per
  PLAN §5). Next: **the talk itself (Thu 2026-07-30, no session needed)**, then the
  in-org round-trip.
- **S9 addendum · 2026-07-26 · Fable 5, with Oleg:** Two operator-driven iterations
  after the S9 commit. **(1) Self-sufficiency pass.** Oleg caught that the deck assumed
  report context a first-time viewer lacks — project names unintroduced, probe/ADR/
  altitude/SMIM/arms unglossed. Fixed (corpus-intro slide + glosses at first use; core
  arc 38 slides; NOTES renumbered). The miss itself was recognised as an instance of
  the eval's own sharpest finding: a **deposit-time failure invisible to
  retrieval-time checks** — the agent held the full report, passed every fidelity
  check it had, and was caught by an operator rule written nowhere (PLAN §9's
  "complete on its own" was deposited but decoded at the wrong layer — the intent gap,
  live). Third instance in this project of the operator, not an instrument, catching
  the sharpest defect. The discussion also named the eval's honest limit: it measured
  **retrieval, never comprehension**, and measured the externalized shadow of a
  methodology whose deeper claim is about the human's semantic hierarchy (cognitive
  traces are unrecoverable in principle; candidate prospective instruments — decode
  tests, operator-catch ledger, rule-invocation journal — recorded in NEXT_TASK
  carried item 5). **(2) slides-v2.md** created per Oleg's direction as the Thursday
  candidate (v1 kept for diffing): §2 now opens with the paper's frame before any
  evidence — the era claim engaging Google's *New SDLC* whitepaper quote ("writing
  code → expressing intent" — true and too narrow: the shift is in **how humans engage
  with information**), creative-input-vs-cognitive-load, the responsibility inversion
  (what the human is genuinely better at becomes the whole job), and AI-assist
  perceived as each operator growing a **personal, evolving substrate** ("scar tissue
  with an index", grown not rolled out — arriving as continuous mass implementation
  closed by each operator's self-reflection loop, not as committee output). §4 gains
  the deck-building miss as the
  evaluation's **third self-correction** (surface pattern-matching vs implied intent;
  n=1, a shape with two in-corpus siblings, never a rate). Close carries the era
  framing. NOTES.md gains the v2 delta map, updated never-cut set, and if-challenged
  lines for the era slide and the miss slide, plus a verify-the-quote-wording task
  before Thursday (quote confirmed via secondary sources only). Feedback memory saved:
  audience-facing artifacts get an explicit self-sufficiency pass.
