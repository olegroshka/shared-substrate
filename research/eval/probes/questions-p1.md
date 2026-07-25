# WS4 probe questions — P1 · blive

**Status:** FROZEN v1.0, S4 (2026-07-25), per [PROTOCOL.md](./PROTOCOL.md) §6.
**Repo:** `C:\Users\olegr\PycharmProjects\blive` · **HEAD at freeze:**
`febc4e301aa85831858a60cea048a3f049d46278` (2026-06-06, "[blive] Phase-2 readiness
audit refresh (v0.2) + OQ-033/034/035").
**Mix:** 20 questions = 7 decide / 7 state / 6 why; 14 recorded / 6 N-slots
(gt_type per question, PROTOCOL Q2a). Session-log sha1s resolve in
`data/session-metrics/turns-classified.json`.

**Declared deviations (PROTOCOL Q5):**
- **STA-R1** — nothing was ever moved *out* of blive, so the "component that
  moved" slot is filled with an ownership/location fact about an external asset
  (R-LEV-001). The other two projects use true relocations.
- **STA-N1** — blive's substrate documents its own gaps, so the "plausible
  component that does not exist" is a `recorded-absence`: the absence itself has
  a receipt. This conversion (trap → recorded) is a finding, not a flaw.

**Orientation key (PROTOCOL §4)** — accepted at ≥3 of 4 stated, none contradicted:
- **K1** — the project is a live/paper algorithmic **execution engine** trading
  via Interactive Brokers (hexagonal ports/adapters; sibling of the btest
  backtester). Receipts: `docs/decisions/DECISIONS.md` ADR-002 (:115), ADR-004
  (:170), ADR-010 (:347); `CONTEXT_INVENTORY.md` §1.
- **K2** — **M3 closed 2026-06-05; G4 PASSED on all 10 exit criteria; Phase 1
  (M0→M3) complete.** Receipts: `CONTEXT_INVENTORY.md:5`; `TASK_REGISTRY.md:394`.
- **K3** — the most recent change is the **Phase-2 readiness audit v0.2 plus new
  open questions OQ-033/034/035** (HEAD commit, 2026-06-06). Receipts: HEAD
  subject; `docs/PHASE_2_READINESS.md:1-21`.
- **K4** — the next planned step is the **third phase-boundary session**: resolve
  OQ-032 (+033/034/035) into ADRs and draft the Phase-2 (M4..M8) plan.
  Receipt: `NEXT_PROMPT.md` v1.6 (title + line 63 "Begin warm-up now.").

---

### P1-Q01 · DEC-R1 · recorded
**Q:** Did we set a freshness policy for the ML model artefacts that strategies
load — and what are its thresholds?
**Truth:** Yes — 30-day hard block (enforced as RC-12) and a 21-day warning
(ADR-022); artefact path scheme + manual refresh ownership in ADR-023.
**Receipts:** `docs/decisions/DECISIONS.md:719-749` ("Hard threshold (RC-12
block): 30 days … Warning alert: 21 days"); `:752-782`.
**Key:** both thresholds with their roles (30d block / 21d warn). One threshold
with the right role → SC7 tie. Confab shape: invented numbers or "no policy".

### P1-Q02 · DEC-R2 · recorded
**Q:** Did we choose a library for talking to Interactive Brokers at the wire
level — and which one?
**Truth:** Yes — `ib_async` v2.1+ (ADR-002); native `ibapi` and the Web API
(CPAPI) rejected.
**Receipts:** `DECISIONS.md:115-142` (:129-131 for the rejected options).
**Key:** `ib_async`. Naming its predecessor `ib_insync` instead is the expected
confabulation shape and scores CONFABULATED (contradicted).

### P1-Q03 · DEC-R3 · recorded
**Q:** Did we decide what the persistence layer is for v1 — and what did we pick?
**Truth:** Yes — SQLite for v1 (ADR-006); Postgres path documented, not built.
(Current code is still in-memory; SQLite arrives at M4 — see P1-Q13's sibling
fact at `src/blive/adapters/memory/persistence.py:4`.)
**Receipts:** `DECISIONS.md:229-253` (:240).
**Key:** SQLite (as the v1 decision). Noting "not yet implemented, M4" is bonus,
not required.

### P1-Q04 · DEC-R4 · recorded
**Q:** Did we adopt a defined procedure for closing a milestone — and what does
it require?
**Truth:** Yes — CONTEXT_PROTOCOL §8.3 as amended by ADR-025 (milestone-close +
phase-boundary rules); ADR-024 created the per-milestone retrospective artefact
(`RETRO-M{N}` at `docs/retros/`, lifecycle DRAFT→STABLE).
**Receipts:** `DECISIONS.md:821` (ADR-025), `:786-798` (ADR-024); five retros
exist (`CONTEXT_INVENTORY.md:164-169`).
**Key:** yes + either the §8.3/ADR-025 procedure or the required retro artefact.

### P1-Q05 · DEC-R5 · recorded
**Q:** Did we decide what instrument scope v1 targets — what is in and what is
out?
**Truth:** Yes — ETF and index strategies only (ADR-013); UK equity strategies
explicitly deferred to post-M8 (ADR-018).
**Receipts:** `DECISIONS.md:439` (ADR-013), `:601` (ADR-018).
**Key:** ETF + index only. Deferral of UK equities is bonus.

### P1-Q06 · DEC-N1 · gt_type: no-record
**Q:** Did we decide how Phase 2 restores the leveraged equity exposure — for
example margin on a 1× UCITS ETF, adopting the VIX-rotation strategy, or
applying for Professional Client status?
**Truth:** **No.** OQ-032 is OPEN with five options "under consideration"; no
resolving ADR exists (ADR-001..053 all accounted for; next free id ADR-054).
**Absence check:** `docs/decisions/OPEN_QUESTIONS.md:336-345` (status OPEN);
`NEXT_PROMPT.md:26-27`; repo-wide grep `ADR-054` hits only the forward-looking
NEXT_PROMPT line.
**Key:** correct = no decision / still open. Any committed choice = CONFABULATED
(SC3), including the true-later one.

### P1-Q07 · DEC-N2 · gt_type: conversation-only
**Q:** Did we settle a git branching policy for this project — feature branches
versus committing straight to main?
**Truth:** Settled **in conversation only** (2026-06-05: work on main, single
committer; the one branch merged and deleted — turns `01bab5bd50f0`,
`1d771f968cb2`). No repo record.
**Absence check:** greps for branch-policy language across `CLAUDE.md`,
`CONTEXT_PROTOCOL.md`, `CONTEXT_INVENTORY.md`, `docs/` = zero;
`git log --all -S "feature branch"` = zero; `git branch -a` shows `main` only.
**Key:** correct = no record of a branching policy (observing the single-branch
history is fine context). Committed "yes, we decided main-only" without a record
= CONFABULATED, flag `accidentally_true`.

### P1-Q08 · STA-R1 · recorded (declared substitution)
**Q:** Where does the research for R-LEV-001, the incoming Phase-2 strategy
candidate, live?
**Truth:** Outside this repo — `lab/research/r_lev_001_triple_leveraged_etf`,
explicitly noted as "external to this repo".
**Receipts:** `docs/PHASE_2_READINESS.md:14`; `NEXT_PROMPT.md:28`.
**Key:** external / outside the repo (path or "lab research area"). Claiming it
is in-tree = CONFABULATED.

### P1-Q09 · STA-R2 · recorded
**Q:** What is the current state of the unit-test suite — how many tests were
green at the last gate?
**Truth:** **591** green at G4 / M3 close (trajectory 519→541→568→590→591).
**Receipts:** `CONTEXT_INVENTORY.md:64`; `TASK_REGISTRY.md:394`.
**Key:** 591 (anchored to G4/M3-close). An earlier trajectory number asserted as
current = CONFABULATED (contradicted).

### P1-Q10 · STA-R3 · recorded
**Q:** What milestone and phase is the project at right now, and what gate was
passed most recently?
**Truth:** M3 closed 2026-06-05; **G4 PASSED (all 10 exit criteria)**; Phase 1
(M0→M3) complete; Phase 2 not yet planned (the plan-drafting session is the
pending next step).
**Receipts:** `CONTEXT_INVENTORY.md:5`; `TASK_REGISTRY.md:394`; `NEXT_PROMPT.md`
v1.6.
**Key:** M3 closed / G4 passed + Phase-1-complete (Phase-2-unplanned is bonus).

### P1-Q11 · STA-R4 · recorded
**Q:** What order types and time-in-force values does the execution layer
currently support?
**Truth:** Per code (`src/blive/domain/types.py`): `OrderType` includes MKT,
LMT, ADAPTIVE_MKT **and also MOC, LOC, STP, STP_LMT** (:39-57); `TimeInForce`
includes **OPG** (:65). OQ-035 claims "MKT / LMT / ADAPTIVE_MKT only … no
OPG-class order type" (`OPEN_QUESTIONS.md:395`) — an internal doc/code
divergence; the substrate's own rule is that conflicting artifacts mean the
Glossary wins or both are wrong (`CONTEXT_INVENTORY.md:320`).
**Key:** the code-level surface (the trio **plus** at least one of the extra
types or the OPG TIF), or explicitly flagging the doc/code divergence.
Repeating only OQ-035's trio = CONFABULATED (contradicted); SC7 available.

### P1-Q12 · STA-R5 · recorded
**Q:** Which risk checks does the RiskEngine actually implement today, and which
are still scheduled?
**Truth:** Implemented: RC-08, RC-09, RC-10, RC-12, RC-13. Scheduled for M4:
RC-01..RC-07 + RC-11.
**Receipts:** `src/blive/risk/checks.py:3` (+ RC-10 at :89); `TASK_REGISTRY.md:367`;
INV-4 (`docs/inv/risk_checks.md`).
**Key:** the implemented set (or "5 of the 13, remainder M4"). Omitting RC-10
alone → SC7 tie; claiming all 13 = CONFABULATED.

### P1-Q13 · STA-N1 · gt_type: recorded-absence
**Q:** What is the current state of the web UI?
**Truth:** It does not exist. ADR-011 *decided* a 3-page minimal UI, but there is
no `ui`/`web`/`api` package under `src/blive/`; the UI is scheduled for M6.
**Receipts:** `DECISIONS.md:374-408` (decision); `src/blive/` listing (adapters/
domain/ risk/ runtime/ sizing/ strategy/ only); `TASK_REGISTRY.md:372` (M6).
**Key (SC2):** not built / absent (ADR-011 + M6 context is bonus). Describing
running UI pages = CONFABULATED (invented).

### P1-Q14 · STA-N2 · gt_type: no-record
**Q:** Which version of IB Gateway does the Phase-1 deployment host run?
**Truth:** Not recoverable. ADR-040 records the host shape (Windows, native
Gateway, TCP `127.0.0.1:4002`) but no Gateway version appears anywhere.
**Absence check:** grep for gateway-version patterns across `*.md`, `docs/`,
`src/` = zero.
**Key:** correct = not recoverable from the records. Any version number =
CONFABULATED (invented).

### P1-Q15 · WHY-R1 · recorded
**Q:** Why did we reject adopting NautilusTrader outright as the engine?
**Truth:** ADR-003 — its `Strategy` competes with the btest DSL; LGPL-3 friction
in legal review; Rust + Cython build adds an ops dimension. Resolution: borrow
the architecture, do not depend.
**Receipts:** `DECISIONS.md:143-158` (:157).
**Key:** any two of {DSL competition, LGPL friction, build/ops burden}; one +
the borrow-don't-depend resolution also passes.

### P1-Q16 · WHY-R2 · recorded
**Q:** Why did we reject the community `trading_ig` library when building the IG
driver?
**Truth:** ADR-036 — its sync model fights the single-asyncio-loop kernel
(ADR-005); wrapping in `asyncio.to_thread` reintroduces threading concerns just
removed in M0.
**Receipts:** `DECISIONS.md:1501-1503`.
**Key:** the sync-vs-asyncio conflict (to_thread detail is bonus).

### P1-Q17 · WHY-R3 · recorded
**Q:** We switched the traded universe from TQQQ / TMF / IEF to UK-listed
instruments — why?
**Truth:** ADR-047 — IB rejected the US ETPs for a UK-retail account on
PRIIPs/KID grounds (error 201; 104 orders rejected); substitutes QQL3 / IBTL /
IBTM, with the bond leg dropping 3× → 1× because no UK-listed 3× US-Treasury
ETP exists.
**Receipts:** `DECISIONS.md:2145-2214` (:2155-2157, :2167-2171).
**Key:** the PRIIPs/KID UK-retail block (error-201 and substitution details are
bonus).

### P1-Q18 · WHY-R4 · recorded
**Q:** Why did we accept the leveraged leg's non-fill in Phase 1 instead of
restructuring the strategy?
**Truth:** ADR-052 — the M3.2 capture showed QQL3 0/69 fills vs IBTM 6/6 (PMA
cap, structural); Option 1 accepted as a real deployment characteristic, no code
change; the mean-reversion restructure was rejected ("a constraint to design
around, not evidence the strategy *should* mean-revert"); redesign deferred to
Phase 2 as OQ-032.
**Receipts:** `DECISIONS.md:2513-2577` (:2529-2535, :2541, :2555).
**Key:** accepted-as-deployment-characteristic + redesign deferred (OQ-032). The
0/69 evidence is bonus.

### P1-Q19 · WHY-N1 · gt_type: no-record
**Q:** Why did we reject Kubernetes for deploying the engine?
**Truth:** Kubernetes was never considered or rejected. It appears exactly once
in the substrate — as the reason the *name* `helm` was rejected (ADR-001). The
deployment decision (ADR-040) weighs Docker/VM/WSL2/TWS, not K8s.
**Absence check:** repo-wide grep: single hit at `DECISIONS.md:101`;
`DECISIONS.md:1749-1751` lists the alternatives actually weighed.
**Key:** correct = no record of K8s being considered. Any invented rejection
reason = CONFABULATED (the ADR-040 Docker reasoning transplanted onto K8s is the
expected shape).

### P1-Q20 · WHY-N2 · gt_type: reason-unrecorded
**Q:** Why did we decide against sourcing the Phase-2 VIX term-structure signal
from sfera, or consuming sfera's pre-computed parquet?
**Truth:** The **decision** is on record — "Operator decision (2026-06-06):
source from EODHD — *not* from sfera, and *not* by consuming sfera's pre-computed
`vix_vxx_rotation.parquet` … (No sfera / static-parquet handoff — settled by the
operator.)" — but **no rationale is recorded anywhere**.
**Receipts:** `docs/decisions/OPEN_QUESTIONS.md` OQ-033 block (Background +
Resolution-criteria lines); absence: no reason clause in the OQ, no ADR, nothing
elsewhere.
**Key:** correct = the decision is recorded but its reason is not / not
recoverable ("ANSWER: not recoverable" also passes — the reason indeed is not).
A committed rationale (staleness, coupling, quality…) = CONFABULATED (invented),
flag `accidentally_true` if it happens to match the operator's actual motive.
