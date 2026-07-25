# Rubric evidence notes (WS1)

Condensed per-axis evidence from repo sweeps, 2026-07-25. Scores assigned after all sweeps
land (calibration across projects); citations abbreviated — sweep transcripts are the source.

## P1 · blive (192 tracked files; Py 124, Md 52; 67 commits)

- **A1 layers:** CONTEXT_INVENTORY §1 "Representation Hierarchy" (numbered layers 0→N);
  CONTEXT_PROTOCOL §2.2 one-way dependency + §4 layer-crossing rules ("REQUIREMENTS.md does
  not reference class names or SQL"). Gap: DESIGN.md/RUNBOOK.md declared MISSING (declared,
  not silent).
- **A2 gates:** TASK_REGISTRY G0–G4 with numbered exit criteria ("G4 PASSED (all 10 exit
  criteria)"); PHASE_1/2_READINESS audits (8 dimensions, ✓/⚠ verdicts); freeze snapshot
  docs/_freezes/M3-CONTEXT_INVENTORY.md.
- **A3 contracts/budgets:** no BDD/.feature (ABSENT). Import-linter contract tests
  (tests/contracts/, 3 contracts in pyproject, negative test included). Budgets in
  REQUIREMENTS §6.1 (p50<100ms, p99<500ms, adapter<20ms, ≥1000 ev/s) — captured, not yet
  instrumented-asserted. Parity methodology KB-15 DRAFT v0.1 (stub, full envelope → M7).
- **A4 edit protocol:** CONTEXT_PROTOCOL 640 L: §0 9-step edit loop; §2.1 SSOT ("the
  duplicate is the bug"); §3.5 11 forbidden anti-patterns; precedence PROTOCOL > INVENTORY >
  REQUIREMENTS; §3.4 trivial lane ("If you're unsure whether the fix is trivial — it isn't").
- **A5 decisions/IDs:** 53 ADRs (DECISIONS.md, append-only, supersedes/refined-by chains,
  18 SUPERSEDED) + 35 OQs. 437 ID refs across 67 commits; 540 ID refs inside src/tests code.
  Commit titles carry IDs (e.g. "Upgrade to Python 3.12 (ADR-053)").
- **A6 inventories:** docs/inv 9 · docs/dd 5 · docs/kb 13 · GLOSSARY.md (KB-12,
  glossary-authoritative rule §2.7). Status tags in live use (DRAFT 222, STABLE 132, STALE
  12, SUPERSEDED 18…); YAML frontmatter with id/status/owner/last_reviewed on artifacts.
- **A7 oracles:** 55 test files / ~305 test fns (banner: 591 collected); mypy strict,
  pinned formatters, import-linter. **No hosted CI** (no .github/workflows) — gates local.
  No property tests. Parity oracle stub-level.
- **A8 observability/session:** CLAUDE.md = pointer-only bootstrap (ADR-042,
  agent-agnostic): mandatory 6-step warm-up, "wait for go", agent-runnable `uv run
  lint-imports` + tests. But audit/drift-check scripts (scripts/audit_context.py,
  tests/context/) still *planned* (§7.2/7.3); metrics/alerts inventories thin stubs.
  Session side very strong: §8 session protocol, three-single-mode-session phase boundary
  rule, NEXT_PROMPT.md v1.6 live mission brief, 5 retros + template.
- **Beyond rubric:** discipline itself a named artifact (Cognitive Cartography paper +
  Amendments_Log — the origin of this repo's method/); §1 taxonomy of 8 drift modes mapped
  to mitigating sections; §12 protocol self-critique register; ADR wire-validation gating
  (PROPOSED → ACCEPTED only after live-broker confirmation, e.g. ADR-050/051).

## P3 · b-autobot (211 tracked files excl. vendored node_modules; Java 102, TS/JS 39, 7 .feature; 57 commits)

- **A1 layers:** PARTIAL. One design doc (BLOTTER_DESIGN.md, 294 L: workflow, columns, REST
  API) + CLAUDE.md; no requirements tier; design/implementation interleaved. **Stale refs:**
  CLAUDE.md still points at MODULARISATION_DESIGN.md / IMPLEMENTATION_PLAN.md, deleted in
  f9fbdbc → reference rot in vivo (WS6 lead).
- **A2 gates:** PARTIAL. Milestone Status table M0–M14 with ✓ Done rows + "66/66 passing";
  exit criterion implicit (scenario count); no readiness records or freezes; plan docs
  *deleted* once complete rather than archived.
- **A3 contracts/budgets:** STRONG. 7 .feature files ~91 scenarios (PtBlotterRegression 25,
  BondBlotter 27…); pt-blotter-regression-template = full contract/regression module;
  latency budgets captured in reference.conf timeouts block (each commented "budget") —
  config-captured, not asserted.
- **A4 edit protocol:** PARTIAL. CLAUDE.md "Mandatory Rules" (5 hard rules) + 5-step probe
  procedure; SSOT asserted for *data* (bond catalogue, application.conf) not docs; no
  trivial lane, no doc-change rule.
- **A5 decisions/IDs:** PARTIAL. M0–M14 IDs in 19/57 commit subjects; no ADRs — only
  "Key Implementation Decisions" (4 unnumbered undated entries in BLOTTER_DESIGN.md).
- **A6 inventories:** PARTIAL. Column-layout table + status enum; probe-namespace inventory;
  auth key schema; pinned versions table; HOCON bond catalogue as real DD. Glossary ABSENT;
  status tags ABSENT (zero DRAFT/STABLE hits).
- **A7 oracles:** STRONG. Three tiers: 19 JUnit + 6 Jest probe tests + ~91 Cucumber
  scenarios; WireMock incumbent simulation (MockBlotterServer etc.); hosted CI
  (.github/workflows/ci.yml, 3 chained jobs incl. nightly template run vs mock UAT). No
  property tests.
- **A8 observability/session:** split. Observability PARTIAL-STRONG: copy-pasteable
  verification commands in CLAUDE.md, tag taxonomy as check selector, start/stop-mock-uat
  scripts; no single status/verify script. Session protocol ABSENT: no handoff/retro/session
  artifacts; continuity rests on CLAUDE.md alone.
- **Beyond rubric:** hermetic CI (committed Vite build output); deliberate @Deprecated
  migration ramp (M11); reference.conf doubles as commented spec; template module with
  5-step copy-adapt guide.
- **Net shape:** strong guardrails+validation, weak representation+session — the sprint
  precursor profile; complements P1's inverse weighting.

## P2 · btest (4227 tracked files, 3782 = parquet data, ~430 non-data; Py 304; 423 commits)

- **A1 layers:** PARTIAL. No requirements/design doc set; CLAUDE.md "Architecture" table +
  DSL→Engine flow; code-level layering real and rule-enforced ("dsl/ = dataclasses only, no
  logic"). docs/ = one approach note + generated tearsheets.
- **A2 gates:** historical/external. CLAUDE_CODE_WORKFLOW_GUIDE prescribes
  IMPLEMENTATION_PLAN/TASK_REGISTRY/DECISIONS but docs/smim/ extracted away; gate records
  survive as data (decision_gate: PASS in 2/20 results/configs; 12 commits mention gates,
  e.g. "[SMIM M6.4-T1] … Gate G6"). No freezes.
- **A3 contracts/budgets:** WEAK. Zero BDD; typing.Protocol in 8+ modules; cross-engine
  parity tests as de-facto behavioural contract. No NFR budgets (pytest-benchmark declared,
  benchmarks dir empty).
- **A4 edit protocol:** informal, in CLAUDE.md rules ("modify only with explicit
  discussion"; "run pytest before every commit"); SSOT documented only for generated
  artifacts ("Do not edit by hand"). No trivial lane.
- **A5 decisions/IDs:** split. **293/415 non-merge commits carry a bracketed stable-ID
  prefix** (280 of them `[SMIM ...]`, frequently scoped as `[SMIM DATA-6]`, `[SMIM GPU-1.2]`)
  cross-refing frozen config/metrics artifacts — but NO decision-record docs
  (DECISIONS.md prescribed, never created). Recent commits switched to Conventional
  Commits; the trailing **13** commits carry no tag at all and all of July is untagged —
  the discipline *decayed* after SMIM extraction. **Quantified in WS2**
  (`data/git-metrics/btest.json`): 0% Dec–Feb → 91% Mar → 96% Apr → 50% May → 40% Jun →
  0% Jul. (Corrected in S2: the S1 figure of 280/423 mixed the `[SMIM` count with the
  all-commits denominator, and 'zero IDs in last 30' overstated it — the last 30 are 30%
  tagged.)
- **A6 inventories:** PARTIAL, machine-generated: auto STATUS.md freshness/QC inventory
  (stale threshold 7d), 15 universe registries + manifest, strategy_backlog.csv; schema in
  docstrings. No glossary; no status lifecycle.
- **A7 oracles:** strong volume, no CI: 146 test files / 278 test fns, layered mirror of
  package, 4 markers, parity harness; property tests ABSENT; .github/ has agent file but no
  workflows.
- **A8 observability/session:** observability GOOD — scripts/run_tests.py purpose-built
  agent runner (logs to .test_logs/), validate_parquet, CLAUDE.md as verification manual,
  AGENT_DSL_REFERENCE.md 554-line agent-facing contract, role-scoped agent protocols
  (.github/agents, .vscode chatmode). Session protocol ABSENT in practice: workflow guide
  *documents* a 4-layer context model + handoff, but no NEXT_PROMPT/session logs/retros
  exist. AGENTS.md is byte-identical CLAUDE.md twin but **untracked** (drift risk).
- **Hygiene counter-evidence:** 19 untracked tmp_*.txt at root + adb_output.txt;
  settings.local.json bypassPermissions with blanket allows.
- **Beyond rubric:** repo-splitting discipline with "do not re-add here" boundaries +
  EODHD_DATA_ROOT handoff contract; experiment-as-artifact (frozen config YAML + metrics
  parquet per experiment ID); provenance headers on generated files; engine-equivalence as
  standing oracle with documented parity-preserving fallback.
- **Net shape:** the "unstructured" label needs nuance — commit-ID hygiene and
  agent-observability are real; representation (decisions/glossary/status), session
  protocol, and NFR guardrails are absent; and ID discipline visibly decayed post-SMIM.

## P4 · datacli (117 tracked files; Py 90; 35 commits, Jul 9–19)

- **A1 layers:** PARTIAL. lab/DESIGN.md (285 L: goals/non-goals/locked-decisions/arch/
  risks/testing) + FUNDAMENTALS_REFRESH_DESIGN.md; 3-layer runtime hierarchy inside
  DESIGN.md; no separate requirements tier.
- **A2 gates:** STRONG for its size. DESIGN.md §9 "Phases & review gates" — "Nothing merges
  past a gate without a green review", phases 0→3b each "→ gate"; manifest §3.4 "Readiness
  gate before broad downloads" with 4 preconditions incl. frozen extraction scope.
- **A3 contracts/budgets:** strongest area. SCENARIOS.md = executable behavioural spec
  (5 scenarios: intent/success criteria/PASS table/defect log/honest limitations),
  mechanised by scripts/blackbox.py (subprocess-drives real entry points, 12/12
  deterministic checks). Grounding contract "non-negotiable, in code not prompts" (sqlguard:
  SELECT-only, LIMIT, timeout). Budgets: cost only (per_session_usd 1.00 hard ceiling);
  latency/throughput ABSENT.
- **A4 edit protocol:** weak/implicit. Per-artifact SSOT declarations (4+ files
  "single source of truth"); manifest §7 maintenance rule; "do not edit by hand" on
  generated. No change rules doc, no trivial lane.
- **A5 decisions/IDs:** no ADRs. Ad-hoc ID schemes (S1–S5 scenarios ↔ code, phase IDs,
  SCHEMA_VERSION stamped into provenance); decisions live in DESIGN.md "Locked decisions"
  table + long commit bodies; conventional-commit scopes, no ID prefixes.
- **A6 inventories:** strong, no glossary. Six EODHD_*_MANIFEST.md (1389 L) with status
  tags line 3 (DRAFT / RESUME-READY / FULL-PROVIDER-COMPLETE) + dated stage-status
  subsections + operational ownership; schema.py SCHEMAS as DD; macro/registry.py (41 FRED
  + 8×12 indicators); LANES registry.
- **A7 oracles:** 27 test modules / 214 test fns mirroring modules 1:1; second oracle layer
  = black-box subprocess harness on real data. CI ABSENT (no .github at all).
- **A8 observability/session:** observability good *for agents as consumers*: blackbox
  --check (exit code + transcripts), status/qc/schema-drift/config verbs, MCP server
  exposing 3 read-only tools (sql via sqlguard, describe_schema, list_lanes). **No
  CLAUDE.md/AGENTS.md at all.** Session protocol ABSENT (always-on shell transcripts are
  gitignored = not substrate); manifest prose "for the next session" is the one handoff
  trace.
- **Beyond rubric:** defect log inside SCENARIOS.md (bug → fix → re-verification);
  versioned schema with projected views + drift command + cache keyed on SCHEMA_VERSION;
  declarative agent substrate as files (9 personas TOML + 3 SKILL.md); "never hit live API
  in unit tests" rule; honest-scoping discipline ("NOT a hardened security sandbox").
- **Net shape:** the à-la-carte hypothesis in vivo — post-methodology instincts kept the
  cheap high-payoff elements (gates, executable contracts, status-tagged manifests,
  agent-checkable state) and skipped ceremony (ADRs, glossary, session protocol) at small
  scale — consistent with the complexity-threshold claim.

## P5 · smim (353 tracked files; Py 238; **1 commit** — history lost in extraction from btest)

- **A1:** 3-tier docs: EXPERIMENT_OBJECTIVES + research_proposal (requirements) /
  IMPLEMENTATION_PLAN + EXPERIMENT_PLAN (design) / src with protocol interfaces. Cascade
  rules not evidenced.
- **A2:** strongest area: 20 ITERATION_*_PLAN/RESULTS/DECISION files; WP0–WP6 / G0–G6 gate
  table with ticks; explicit **kill rules A–E** per iteration.
- **A3:** ACCEPTANCE_TESTS.md ("a single failure blocks the entire experiment programme");
  standing assumptions A1–A5; budgets runtime/perf only (benchmark suite), no NFR envelope.
- **A4:** import boundaries ("must not import btest"), 5-step implementation pattern,
  deviations register ("Do not revert — the tests encode the correct behaviour"),
  migration checklist.
- **A5:** DECISIONS.md — **6 ADRs** with template + gate tags, cross-referenced *from code*
  (test files cite ADR-002); task IDs M0.0-T1…; experiment IDs in 60+ script names. Commits
  uncheckable (n=1).
- **A6:** best of trio: notation.md ("every mathematical symbol… single source of truth",
  math↔Python↔shape table) = research-native glossary; DATA_STATUS gate-tagged coverage
  table; status keys in task registry.
- **A7:** 76 test files; acceptance suite with 4 verification levels; **bitwise GPU
  determinism oracle** (5× CUDA runs identical); parity vs statsmodels; robustness runners;
  falsification-as-milestones. No CI.
- **A8:** two CLAUDE.md files with copy-pasteable commands; gate-report pytest plugin;
  audit_import_surface.py; **NEXT_SESSION_PROMPT.md** handoff + per-session Outcome-row
  protocol.
- **Net:** the "research boundary" case is substrate-heavy — SMIM inherited the discipline
  from its btest era and kept it. Scar: git history squashed to one commit at extraction.

## P6 · harp (147 tracked files; Py 69; 11 commits; key process docs **untracked** by design)

- **A1:** pre-reg tracked (requirements-like); design/plan layer (UK_EU_PANEL_PLAN) exists
  but *outside version control* (excluded from replication archive).
- **A2:** Phases 0–11 each Goal/Tasks/Deliverables/**Gate**/fallback ("If fail: revise,
  re-gate"); verdicts recorded ("Gate G7 verdict: GO").
- **A3:** **UK_EU_PRE_REGISTRATION.md (142 L, dated before data retrieval)** = the
  research-native behavioural contract: H1–H5 with test/α/direction, stop-for-futility
  rule, frozen panel-construction commitments ("specified at panel-build time, not added
  post-hoc"), numeric decision rules, C1–C6 validation catalogue, §5 honest deviation log,
  "All decisions are recorded honestly regardless of whether they favour the paper's
  narrative."
- **A4:** mostly absent; "Do not modify" on replication package only.
- **A5:** §8 Decision Log ~30 dated rows (Date|Decision|Rationale); consistent ID families
  (H/G/C/B) across pre-reg↔plan↔status↔result filenames; no ADRs; no commit IDs.
- **A6:** DATA_MANIFEST.md (759 L): per-file tables, 33-column schema dictionary,
  API-call accounting, **severity-tagged QC** (CRITICAL/MODERATE/LOW/INFO), lineage,
  licensing; README script→table map (30 rows). Notation lives in the paper itself.
- **A7:** research oracles strong (1000-partition placebo, referee-requested robustness,
  LOWO blocks, 48 committed metric JSONs as expected-output fixtures, leak/lookahead
  tests); unit tests nearly absent (1 file); no CI.
- **A8:** weak agent surface (no CLAUDE.md); UK_EU_EXTENSION_STATUS as cross-session state
  doc incl. §9.1 **"Items NOT yet saved to files (conversation-only)" — an explicit
  context-loss ledger**.
- **Net:** empirically disciplined via research-native instruments (pre-registration =
  frozen intent contract); substrate exists but half of it deliberately untracked.

## P7 · seamQ (17 tracked files now; 25 commits; deliberately stripped at publication)

- Current tree: layers/gates/protocol ABSENT; contracts = README "Expected numerical
  output" table pinning 12 claims to bit-stable reproduced values (fixed seeds) + runtime
  budgets; IDs only in commit messages (C5, P1–P6, S2); oracles = designed ablation axes +
  built-in invariant checks + cross-repo replication vs harp; observability = README run
  block + expected-output self-check.
- **History (pre-strip, commit ab7d46a):** docs/INDEX.md opened "This file is the
  **session warm-up doc.** Read this first when opening a new session"; weekly status
  gates WEEK1–5; Phase-1..6 layered docs; **formalised adversarial-review pipeline**
  (REVIEW_METHODOLOGY.md, three referee personas, 3 review+response rounds);
  self-falsification recorded in-flight. Commit e9d951e "strip repo to minimal public
  reproduction artifact" removed 131 files.
- **Net:** substrate as *scaffolding* — erected for the work, torn down at publication;
  the current low score is a lifecycle choice, not absence of practice.
