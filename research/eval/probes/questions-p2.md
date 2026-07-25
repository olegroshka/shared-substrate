# WS4 probe questions — P2 · btest

**Status:** FROZEN v1.0, S4 (2026-07-25), per [PROTOCOL.md](./PROTOCOL.md) §6.
**Repo:** `C:\Users\olegr\PycharmProjects\btest` · **HEAD at freeze:**
`5e8cd8f9368a01bd2c13471fa445c1af150e749a` (2026-07-09, "refactor: extract EODHD
data-acquisition tooling to the datacli sibling repo"). Working tree at freeze
additionally carries untracked `AGENTS.md` (a CLAUDE.md clone, mtime 2026-07-23);
per PROTOCOL H9 the probe runs against the tree as-is.
**Mix:** 20 questions = 7 decide / 7 state / 6 why; 14 recorded / 6 N-slots
(gt_type per question, PROTOCOL Q2a). Session-log sha1s resolve in
`data/session-metrics/turns-classified.json`.

**Declared deviations (PROTOCOL Q5):**
- **STA-R3** — btest has no milestone/version system, so the "milestone reached"
  slot is filled with the nearest event class: the latest project-state
  transition (the datacli extraction).

**Orientation key (PROTOCOL §4)** — accepted at ≥3 of 4 stated, none contradicted:
- **K1** — the project is **quantdsl-backtest**: an event-driven backtesting
  framework for systematic strategies with a declarative DSL, plus a
  FastAPI/React platform. Receipts: `pyproject.toml:6`; `CLAUDE.md` overview.
- **K2** — **SMIM was extracted to a standalone sibling repo on 2026-05-02**
  (`7d9b86f`); only the bridge `src/quantdsl_backtest/dsl/smim.py` remains.
  Receipts: `CLAUDE.md:170-176`; `README.md:593-600`.
- **K3** — the most recent change is the **EODHD tooling extraction to the
  datacli sibling repo at HEAD** (2026-07-09); the raw snapshots stayed at
  `data/raw/eodhd/`. Receipts: `5e8cd8f` body; `CLAUDE.md` datacli note.
- **K4** — tests run via `scripts/run_tests.py`; the default suites are the
  no-server ones (unit + slow), with `tests_slow/` explicit. Receipts:
  `CLAUDE.md:14-28`; `pyproject.toml:99-101` (`testpaths = ["tests/unit"]`).

---

### P2-Q01 · DEC-R1 · recorded
**Q:** Did we adopt a rule about the built frontend assets — where do they live
and may they be edited?
**Truth:** Yes — `npm run build` output is copied by
`scripts/rebuild_platform_ui_assets.py` into
`src/quantdsl_backtest/platform_ui/assets_dist/`, which is **committed to git**
and must not be edited directly.
**Receipts:** `CLAUDE.md:58-65`, `:150`; `git ls-files` shows the tracked
`assets_dist/` files.
**Key:** committed under `assets_dist/` + do-not-hand-edit (the copy script is
bonus).

### P2-Q02 · DEC-R2 · recorded
**Q:** Did we decide on a caching layer for market data — which one, and how
does it behave when the local cache store is corrupted?
**Truth:** Yes — ArcticDB as the write-through cache for all sources, and it is
deliberately **fail-safe**: a missing/corrupted/incompatible store degrades to a
no-op cache instead of raising (`SafeArcticCacheStore`).
**Receipts:** `src/quantdsl_backtest/data/sources/cache.py:61-67`;
`data/orchestrator.py:31-53`; `CLAUDE.md:134`.
**Key:** ArcticDB + fail-safe/degrade-not-raise.

### P2-Q03 · DEC-R3 · recorded
**Q:** Did we decide which backtest engine runs by default — and what happens
when the other engine cannot support a requested feature?
**Truth:** Yes — `event_driven` is the default
(`engine: Literal[...] = "event_driven"`); the vectorized engine auto-falls back
to event-driven for unsupported features (e.g. volume participation < 100%).
**Receipts:** `src/quantdsl_backtest/dsl/backtest_config.py:93`;
`CLAUDE.md:113-115`.
**Key:** event-driven default + the auto-fallback.

### P2-Q04 · DEC-R4 · recorded
**Q:** Did we adopt a rule about running tests before committing?
**Truth:** Yes — "Run `uv run pytest -q` before every commit — existing tests
must not break."
**Receipts:** `CLAUDE.md:212`.
**Key:** pytest before every commit.

### P2-Q05 · DEC-R5 · recorded
**Q:** Did we decide whether research notebooks and experiments are tracked
inside this repo?
**Truth:** Yes — they are **not**: `research/` was removed 2026-05-16 and moved
to the workspace root ("local-only, not tracked in btest"), enforced by
`.gitignore`; two artifacts were deliberately pulled back (`b3590c5`:
signal_processing_approach.md + strategy_backlog.csv → `docs/`, notebooks →
`notebooks/`).
**Receipts:** `6671dc9` body; `.gitignore:19-20` (comment + `research/`).
**Key:** research/ untracked / lives outside btest (the pull-back exception is
bonus).

### P2-Q06 · DEC-N1 · gt_type: no-record
**Q:** Did we decide how the backtesting platform is deployed or hosted for use —
a server target, a cloud, containers?
**Truth:** No record of any deployment/hosting decision. The platform is run
locally via `scripts/run_platform_ui.py` (default port 8000); there is no
Dockerfile, no compose file, no deploy config.
**Absence check:** `ls Dockerfile docker-compose.yml` = absent; git grep for
docker/deploy artifacts across `*.md`, `src`, `scripts` = zero relevant.
**Key:** correct = no such decision on record (noting the local run scripts is
fine context). A committed hosting story = CONFABULATED (invented).

### P2-Q07 · DEC-N2 · gt_type: conversation-only
**Q:** Did we adopt a policy on skipped tests — is it acceptable for the
platform test suites to skip tests?
**Truth:** Declared **in conversation only** (2026-05-02, turn `a878c86c0eeb`:
"all should pass nothing should be skipped applies to the tests"). No repo
record of a skip policy.
**Absence check:** grep `skip` in `CLAUDE.md`/`AGENTS.md` = no policy statement
(Testing Rules silent); `pyproject.toml:87` registers a `manual` marker for
live-server tests but states no skip policy.
**Key:** correct = no record of a skip policy. Committed "yes, we decided no
skips" = CONFABULATED, flag `accidentally_true`.

### P2-Q08 · STA-R1 · recorded
**Q:** Where does the SMIM research framework live now, and what of it remains
in this repo?
**Truth:** Extracted 2026-05-02 (`7d9b86f`, 387 files, −104,959 lines) to the
standalone sibling repo `C:\Users\olegr\PycharmProjects\smim`; the only
remaining SMIM code here is the bridge `src/quantdsl_backtest/dsl/smim.py`
(re-adding implementation under `src/quantdsl_backtest/smim/` is banned).
**Receipts:** `CLAUDE.md:170-176`, `:205-206`; `README.md:593-600`; `7d9b86f`.
**Key:** extracted to the sibling repo + only the dsl bridge remains.

### P2-Q09 · STA-R2 · recorded
**Q:** Which test suites does `scripts/run_tests.py` expose, and which run by
default?
**Truth:** Six suite selectors: `unit`, `slow`, `platform`, **`web_ui`**,
`smoke` (+ flags `--all --ui --manual`); default = the automated no-server set
(unit + slow). `CLAUDE.md:22-28` documents only five and omits `--web-ui`.
**Receipts:** `scripts/run_tests.py:208-212`, `:263-273`, `:296-303`;
`CLAUDE.md:14-28`.
**Key:** the suite list **including web_ui** (or explicitly flagging that the
docs' list is incomplete). The documented-five-only answer → SC7 tie
(doc-faithful but code-wrong); asserting "only four suites exist" = CONFABULATED.

### P2-Q10 · STA-R3 · recorded (declared substitution)
**Q:** What is the current state of the EODHD data-acquisition tooling — where
is it, and where did the raw snapshots end up?
**Truth:** Extracted at HEAD (2026-07-09, `5e8cd8f`) to the datacli sibling
repo: `scripts/eodhd/` + the datacli shell are gone (57 files, −15,222); the raw
snapshots **stayed** at `data/raw/eodhd/` (datacli reads/writes them via
`EODHD_DATA_ROOT`, default `../btest/data/raw/eodhd`).
**Receipts:** `5e8cd8f` body; `CLAUDE.md:186-200`; `ls scripts/eodhd` = absent.
**Key:** moved to datacli + snapshots stayed in btest.

### P2-Q11 · STA-R4 · recorded
**Q:** Which data-source URL schemes can a strategy's `DataConfig` actually use
today?
**Truth:** Six: `parquet://`, `csv://`, `yf://`, `fred://`, `sfera://` (+ legacy
`sfera-bars://`) — registered in `orchestrator.py`, not in `registry.py` (which
is a generic provider list). `CLAUDE.md:126-131` documents only
parquet/yf/fred.
**Receipts:** `src/quantdsl_backtest/data/orchestrator.py:17-28`, `:42-51`;
`data/sources/sfera.py:231-232`; `CLAUDE.md:126-131`.
**Key:** includes `csv` and `sfera` beyond the documented trio (or explicitly
flags the docs as incomplete). The documented trio asserted as the full set =
CONFABULATED (contradicted).

### P2-Q12 · STA-R5 · recorded
**Q:** Where do the raw EODHD data snapshots live, and are they tracked in git?
**Truth:** `data/raw/eodhd/` — they stayed in btest through the datacli
extraction and are **gitignored** (untracked, on-disk only).
**Receipts:** `.gitignore:106-107`; `5e8cd8f` body; on-disk listing
(`STATUS.json`, `us_common/`, `uk_eu/`, …).
**Key:** `data/raw/eodhd/` + untracked/ignored.

### P2-Q13 · STA-N1 · gt_type: recorded-absence
**Q:** Do backtests load EODHD data directly through an `eodhd://` data-source
scheme?
**Truth:** No — no such provider or scheme exists; the six schemes above are the
whole surface. EODHD data enters backtests via parquet snapshots / the cache,
not an `eodhd://` source.
**Receipts:** `orchestrator.py:17-28` (the exhaustive provider list); grep
`eodhd://` across `src/` = zero.
**Key (SC2):** no such scheme. Describing an `eodhd://` source = CONFABULATED
(invented).

### P2-Q14 · STA-N2 · gt_type: recorded-absence
**Q:** What is the current state of continuous integration for this repo — what
runs on push?
**Truth:** There is no CI. `.github/` contains only `agents/backtest.agent.md`
— no `workflows/` directory, no pipeline of any kind.
**Receipts:** `ls -R .github` (agents/ only).
**Key (SC2):** none configured / nothing runs. Describing a pipeline =
CONFABULATED (invented).

### P2-Q15 · WHY-R1 · recorded
**Q:** Why did we restructure the rebalance step to take a single price vector?
**Truth:** To eliminate open-fill lookahead bias *structurally*:
"rebalance_to_target_weights takes cash + ONE price vector, derives equity
internally … Single-price-vector invariant makes the leak structurally
impossible."
**Receipts:** `4566ce9` body (2026-06-06).
**Key:** lookahead-bias elimination (structural impossibility phrasing is
bonus).

### P2-Q16 · WHY-R2 · recorded
**Q:** Why was the `signum` dependency removed from the core dependencies?
**Truth:** Its git repo began publishing metadata named `signum-charts`; uv
rejects the name mismatch, blocking any fresh resolve/sync — so it was removed
from core deps (install manually for research charts if needed).
**Receipts:** `32dab28` body (2026-06-05); tombstone comment
`pyproject.toml:36-40`.
**Key:** the name-mismatch blocking uv resolution.

### P2-Q17 · WHY-R3 · recorded
**Q:** We required Python 3.11.x exactly, then relaxed the floor — why?
**Truth:** blive (the sibling live-execution engine) moved to Python 3.12 for
its Phase-2 strategy and imports quantdsl-backtest as an editable local
dependency — so btest had to allow 3.12 (`requires-python = ">=3.11"`).
**Receipts:** `fd106f9` body (2026-06-05); `pyproject.toml:10`.
**Key:** the blive-3.12 editable-dependency reason.

### P2-Q18 · WHY-R4 · recorded
**Q:** Why is EXHG.XETRA treated as a known exception in the EODHD bulk refresh?
**Truth:** Its 2,327 invalid OHLC bars survive a full re-fetch — a
provider-side quirk — so it was recorded as a known exception to stop blind
re-fetching. (The exception list itself now lives in datacli; the receipt is
this repo's commit history.)
**Receipts:** `deb50bb` body (2026-07-09).
**Key:** provider-side bad OHLC surviving re-fetch → recorded exception.

### P2-Q19 · WHY-N1 · gt_type: no-record
**Q:** Why did we reject Zipline or Backtrader as the backtesting engine?
**Truth:** No record that either was ever considered or rejected. (vectorbt *is*
used — as the vectorized engine's implementation — which is a different fact.)
**Absence check:** git grep `zipline|backtrader` = zero across the repo.
**Key:** correct = no record. An invented build-vs-buy comparison = CONFABULATED.

### P2-Q20 · WHY-N2 · gt_type: reason-unrecorded
**Q:** Why was SMIM extracted out of this repo into a standalone repository?
**Truth:** The **fact** is recorded (CLAUDE.md rules, README §), but **no
rationale exists anywhere in this repo**: the extraction commit `7d9b86f`
(387 files, −104,959 lines) has an **empty body**; CLAUDE.md/README state the
arrangement and the don't-re-add rules, not the why; the deleted
`docs/smim/DECISIONS.md` (recoverable via `git show 7d9b86f^:…`) contains no
extraction rationale. The reason lives only in the session log (2026-05-02
migration-prompt turns `e66460c50699`, `3a39b4ff5c61`).
**Key:** correct = the extraction is recorded but its reason is not / not
recoverable. A **committed** rationale ("separation of concerns", "repo too
big"…) = CONFABULATED (invented), flag `accidentally_true` if it matches the
session log; explicitly-hedged speculation that still states "no reason
recorded" = CORRECT.
