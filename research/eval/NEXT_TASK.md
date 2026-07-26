# NEXT_TASK — S8: report assembly

**Recommended model: Fable 5** (per STATE.md's schedule column). Every workstream is
done. S8 writes nothing new — it decides what the evidence is allowed to say and in what
order, and puts it in `report/REPORT.md`. The risk here is the inverse of S7's: not a
story the receipts don't support, but a *number* whose caption drifts one notch stronger
than the measurement.

> **What S7 leaves you.** WS6 delivered its four war stories — they are written and
> final in `report/war-stories.md`, and S8 should cite that file rather than re-tell
> them. What S7 also did was **correct two published exhibits downward**, and those
> corrections, not the stories, are what S8 has to absorb:
>
> 1. **The survivorship number is smaller.** btest's ephemeral floor is **≥10 of 94**,
>    not ≥26 of 105 — 16 of 26 names were false positives (auto-memory files, flattened
>    duplicates of committed files, binary-store splices). b-autobot **4 → 0**. blive's
>    **0 of 33** and seamQ's **≥33 of 89** stand. It is no longer "the strongest single
>    number in the corpus"; §2.1's warm-up cost is.
> 2. **btest's tag-decay curve is largely a composition change.** 280 of 293 tags are
>    `[SMIM]` and SMIM *left the repo* in `7d9b86f`; only 165 of 293 carry a scoped
>    stable id (163 Mar, **2** Apr, 0 after); and 9 of 10 July commits carry a
>    conventional-commit prefix. **Never show "0% in July" as an absence of discipline.**
>    The defensible claim is that a stable-ID convention was replaced by a taxonomy —
>    `feat(costs):` tells you a commit's kind, `[SMIM DATA-6]` tells you what it is about
>    and lets a later record cite it. That distinction *is* §4's reframe, so the exhibit
>    survives — retitled.
>
> **The rule that produced both corrections is now ASSESSMENT §5.1 rule 3, and it binds
> you more than anything else in this file:** a robust count does not license the sentence
> built on top of it. Before any number goes in the report, name the reading its caption
> invites and check that reading separately. Both S7 corrections came from reading the
> individual items behind a count, and both made the corpus smaller.

---

## Prompt for S8

Warm up first, then execute. This is session S8 of the shared-substrate eval research.

**Warm-up (read in this order):**
0. `research/eval/METHODS.md` (now v1.1) — the whole method in one read. §6's eleven
   rules and §7's limits are the report's honesty spine; §5.9 is new.
1. `research/eval/ASSESSMENT.md` — **this is the outline.** §1's scorecard, §2 what the
   evidence supports, §3 what it does not, §4 the reframe, §5.1 the fragility ledger with
   its **three** binding rules, §7 the bottom line. The report is this document with the
   numbers and receipts filled in, not a new argument.
2. `research/eval/STATE.md` — per-workstream findings and every caveat that must travel
   with a number. Read the **WS6 findings 5 and 6** before touching any exhibit.
3. `research/eval/report/war-stories.md` — already final. §5 ("what the four have in
   common") and §6 ("what was cut") are the parts REPORT.md should reference.
4. `research/eval/PLAN.md` §6 (deliverables), §7 (confounds ledger), §9 (talk shape) —
   §9's core arc is the section order the report must map onto 1:1.

**What S8 must produce:**
- **`research/eval/report/REPORT.md`** — sections mapping 1:1 to PLAN §9's core arc, so
  S9 can lift each section into a slide without re-deciding anything. Every exhibit
  carries: the number, its **denominator**, the caveat that travels with it, and a
  pointer to the `data/` file it came from. A war story appears only as a named cross-
  reference to `war-stories.md`, after the robust number it illustrates.
- **An exhibit bench** — a table (appendix, or a separate `report/exhibits.md`) of every
  presentable figure with its source file, its caveat, and a one-line honest caption.
  PLAN §9 promises figures "presentation-ready into an appendix bench — many numbers
  available on demand, none mandatory". This is that bench, and it is what S9 shops from.
- **The confounds ledger written out**, not referenced — PLAN §7's six items, with
  confound 6 in its corrected form.
- Findings + caveats into `research/eval/STATE.md`, and **rewrite this NEXT_TASK.md for
  S9** — per the schedule: S9 = deck + dry run, Fable 5,
  `talks/does-the-substrate-matter/`.

**The three rules from ASSESSMENT §5.1, restated because they are the whole job:**
1. **Nothing from the fragile table leads a section or carries a claim.** Each is an
   illustration after a robust number, stated with its n.
2. **No two fragile findings are aggregated** to imply a rate. One confabulation, one
   manufactured decision and one stale claim is three anecdotes, not a trend of three.
3. **A robust count does not license the sentence on top of it** (new, S7). For a count
   of artifacts, read the artifact names. For a curve, break it down by population.

**The exhibits, in the order of how much weight they can bear:**

*Robust, and the report leads with these:*
- **§2.1 the retransmission tax** — blive warms up in 9 of 10 sessions at ~106 chars and
  *falling* (192 → 106); btest in 43 of 68 at ~417 and *rising* (477 → 607). 78 sessions,
  1,061 classifiable turns. **This is now the corpus's strongest single number.** Carry
  its two caveats: btest's sessions also lengthened (9.1 → 19.8 turns), and paste bodies
  survive for only 74 of 204 paste-referencing turns, which under-counts payload-shaped
  warm-ups — conservative against the finding.
- **§3.5 length-banded altitude** — btest lowest in all four bands; held-out κ=0.902 on
  the high/low collapse. **No altitude number is publishable without its length band**;
  the raw ordering is a verbosity artefact and puts the least-substrated project on top.
- **§2.2 brevity means opposite things** — dispatch-per-assent seamQ 5.0 · b-autobot 0.50
  · blive 0.25 · btest 0.10. Fragile numerator (btest's is **3** dispatches) — say so.
- **§3.4 the rework contrast** — blive 5.2% vs btest 82.2% at any horizon, 3.9% vs 32.6%
  within 14 days. Confound stated: btest's history is 5× longer.

*Robust counts, corrected captions (S7):*
- **§2.6 survivorship** — blive 0 of 33 · btest ≥10 of 94 · seamQ ≥33 of 89, all lower
  bounds, plus the two instrument properties: the noise only ever inflates an ephemeral
  count (and blive's is zero), and channel C reaches only projects whose transcripts
  survived (btest 10 files, **blive 0**).
- **§2.5 the tag curve** — retitled per the S7 breakdown above.

*Honest negatives — four of them, and they are the credibility play:*
WS3 finding 5 (altitude does not track discipline inside btest) · WS4b H-1 (**p = 1.0**,
nominal direction reversed after review, the corpus's only confabulation belongs to the
*full-substrate* project) · WS5 finding 4 (btest's instruction file does not decay
silently — 28 removals, zero unexplained) · WS5's headline null (zero blive ADRs silently
reversed, S(k)=1.000 at every k). Plus the two S7 self-corrections. PLAN §7's METR
reminder closes the ledger.

*The cross-arm statement WS6 produced, which cuts against the thesis and should be said
plainly:* **neither substrate posture has an instrument that checks a factual claim at
deposit time.** blive's OQ-035 and btest's "~2600 LOC" are the same defect in projects
scoring 22/24 and 12/24; every check either project owns runs at *retrieval*.

*The paired control to build the "system representation" section on:* the **Python 3.12
pair** (WS5 finding 3) — same operator, same day, same decision, both repos. btest *did*
record why, well, in a commit body. What differs is **addressability**: ADR-053 is cited
from five artifacts including the auto-loaded one, btest's reasoning from zero, and
ADR-053's `companion:` field means the record for btest's decision lives in blive's repo.

**Numbers that must never appear without their qualifier:**
1. Any survival-curve point needs its **`at_risk` denominator** on the axis — blive's
   k=12 rests on **26** records, not 53.
2. The two WS5 arms are **not a shared denominator**. btest has no decision records; its
   arm is instruction rules plus commit prose. Side-by-side needs the `n/a` flag, never a
   zero.
3. The reversal-narration gap (blive 11.9 vs btest 0.24 per 100 commits, hand-adjudicated)
   must be shown with the **prose-volume confound** beside it: 362.5 vs 62.7 words per
   commit, and on the per-10k-words normalisation the automated gap is **2.1×, not 50×**.
4. Any exhibit plotting rubric score against session-log altitude must footnote **seamQ** —
   WS1 scored the stripped tree, WS3 measured the in-flight posture.
5. `duration_days` in `complexity-profiles.json` is a **git span**, not project length.
   seamQ's real span is ~3 weeks, not the 1.9 days its git reports.
6. **DEC-N2 is 0 for 3.** State it as "we could not find one", never as "they do not
   exist".
7. btest is **ephemeral, not flat** — and its `CLAUDE.md` is a **212-line
   agent-instruction file**. Every substrated-vs-unsubstrated exhibit needs that
   qualifier; WS4b finding 10 says it may explain the null on its own.
8. **smim is `n/a: history lost`**, never zero.

**Execution cautions:**
- **Do not re-run any miner.** All are deterministic on unchanged git and would produce
  identical output; a re-run's only possible effect is to overwrite a published input.
  Author judgment lives in `data/qualitative-ratings.json`, `data/probes/scores.json`,
  `data/survival-audit.json`, `data/attribution-rules.json`, `data/altitude-labels.json`
  and `data/survivorship-audit.json` — all **inputs**, never regenerated.
- **`data/artifact-survivorship.json` still carries the uncorrected numbers by design.**
  The correction is in `data/survivorship-audit.json`. The report cites the corrected
  figures and says where the correction lives; it does not quietly edit the output.
- **P8 stays out of `research/eval/`** except as the anonymised "work-project" row.
  §5's round-trip is the only thing that crosses into the org, and the report is the
  strict surface: no employer name, no component name.
- The one genuinely soft number is still **P8 A5** (rubric decisions axis, 2
  PROVISIONAL-INFERRED) — settleable only from Oleg's memory, worth one question if the
  topic comes up, not worth blocking on.

**Constraints (carried from S1–S7):** console output ASCII-only (Windows cp1252 — no
arrows, no unicode); Python 3.11 via `python`; never modify the corpus repos; anything
that is author judgment stays a published *input* file rather than something a re-run can
silently overwrite.

---

**Nothing is pending on Oleg.** WS6 raised no new questions for him and closed none that
were open.

Carried as *reconcile-before-the-talk* (none are blockers):
1. blive's Requirements v0 is **3,375 words**; the paper says "around six thousand" —
   check which artifact is wrong and fix it. *(Open since S2; the cheapest of these.)*
2. **New from S7 —** `artifact_survivorship.py` has five recorded fixes it has never been
   run with (`data/survivorship-audit.json` → `recommended_fixes_for_any_future_run`):
   exclude agent-memory paths per its own line-113 comment, normalise separators before
   taking a basename, reject repeated-leading-token and non-ASCII basenames, apply
   `corpus_common`'s vendored-path classification, and publish per-project transcript
   counts alongside every count. Only worth doing if the eval continues past the talk.
3. **New from S7 —** WS6's story 3 leaves a cheap, testable hypothesis on the table: both
   of blive's defects came from the one session type with no execution feedback loop (a
   substrate-only audit). n=1. The fix it suggests — require every factual claim in an
   audit record to carry the `file:line` it was read from — costs nothing to adopt and
   would be a genuine methodology contribution if it held.
