# Eval research — session state (warm-up / handoff file)

> Read this first in every eval session; deposit status + next step before ending.
> Source of truth for scope and method: [PLAN.md](./PLAN.md). One session per workstream.
> The next session's ready-to-paste prompt + model schedule: [NEXT_TASK.md](./NEXT_TASK.md).

## Status

| WS | Status | Session · model | Notes |
|----|--------|-----------------|-------|
| WS0 evidence audit | **DONE 2026-07-25** | S1 · Fable 5 | `data/evidence-map.json`; findings below |
| WS1 rubric | **DONE (DRAFT) 2026-07-25** | S1 · Fable 5 | instrument `rubric/RUBRIC.md`; evidence `data/rubric-evidence.md`; scores `data/rubric-scores.json` — **pending Oleg's review** of flagged judgment calls + P8 blanks (A4/A5/A6/A8) |
| WS-X complexity profile | **DONE 2026-07-25** | S2 · Opus 5 | `scripts/complexity_profile.py` → `data/complexity-profiles.json`; Kendall's W in 3 runs |
| WS2 git miners | **DONE 2026-07-25** | S2 · Opus 5 | `scripts/git_miner.py` (+ `scripts/corpus_common.py`) → `data/git-metrics/*.json` |
| WS3 session-log analysis | pending | S3 · **Opus 5** | altitude-classifier taxonomy is judgment-heavy (headline exhibit); feasibility per project: see WS0 findings |
| WS4a probe pre-registration | pending | S4 · **Fable 5** | question design IS the experiment's validity; pre-registration commit BEFORE any run |
| WS4b probe runs + scoring | pending | S5 · **Sonnet 5** | frozen protocol execution; probe *subjects*: one fixed model across projects (suggest Sonnet 5, record in protocol) |
| WS5 survival curves | pending | S6 · **Sonnet 5** | kernel teaser only if time — if attempted, bump to Opus |
| WS6 archaeology | pending | S7 · **Opus 5** | narrative judgment; see memory-folder lead below |
| Report assembly | pending | S8 · **Fable 5** | cross-workstream synthesis → `report/` |
| Deck + dry run | pending | S9 · **Fable 5** | `talks/does-the-substrate-matter/` |

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

## Open questions

- **OQ-1:** what tooling built btest Dec 2025–Feb 2026 (pre-history-log era)? → ask Oleg.
- **OQ-2:** do claude.ai web/desktop exports exist for blive's lost sessions? → ask Oleg.
- **OQ-3:** b-autobot's Copilot-era logs (pre-`jb/` store) — any other local store? (low
  priority; CC history covers the sprint's human turns.)

## WS1 findings (2026-07-25)

Scores (DRAFT, /24): blive 22 · smim 20 · harp 17 · datacli 17 · b-autobot 16 · btest 12 ·
seamQ 7 (current tree) · work-project provisional. Headline observations (full list in
`data/rubric-scores.json`):

1. **The ordering defies the naive story.** Research projects score mid-high — via
   *research-native* instruments (harp's pre-registration with stop-for-futility rules,
   smim's notation sheet + kill rules, seamQ's adversarial-review pipeline). The paper's
   boundary claim refines: exploratory work has *different substrate artifact types and
   lifecycle*, not no substrate. Pre-registration is a frozen intent contract.
2. **btest decayed, measurably.** 280/423 commits carried [SMIM] stable IDs; after the smim
   extraction the last 30 commits have zero. Within-project temporal evidence — stronger
   than any cross-project comparison (WS2 should quantify the decay curve).
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
  finding 2's "last 30 commits" phrasing (it is the last 13). Next: **WS3
  session-log analysis (S3, Opus 5)** — the altitude classifier.
