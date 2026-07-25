# ALTITUDE — the operator-altitude taxonomy (WS3a instrument)

**Status:** frozen v1.0, S3 (2026-07-25). Written *after* the 99-turn hand-labelling
pass and *before* `scripts/altitude_classify.py`, so the rules below are what the
labeller actually used, not a post-hoc rationalisation of what a regex could match.

**What it measures.** For each operator-typed turn, the abstraction level the human
is operating at. The paradigm claim under test (PLAN §4 WS3a): in substrated work the
human's turns concentrate at the top; in flat work they are dragged down into
mechanics.

**What it does not measure.** Quality, effort, or value. A mechanical turn is not a
bad turn — pasting a traceback is often exactly the right move. The claim is about
*where the human's attention has to sit*, not about whether they are working well.

---

## 1. The four classes

| Code | Class | The operator is… |
|------|-------|------------------|
| **I** | intent / goal declaration | naming *what should become true* — a goal, a task, a milestone, an investigation — without re-deriving how |
| **D** | decision / trade-off resolution | *resolving or raising* a choice the agent cannot settle: selecting among options, rejecting, accepting with qualification, setting policy |
| **C** | design / contract shaping | *binding future work*: structure, interfaces, schemas, naming, acceptance criteria, quality gates, standing rules, protocol |
| **M** | mechanical steering | *driving execution*: supplying errors or data, operational commands, bare assent or continuation, pointing at defects, re-transmitting context the agent lost |
| **UNK** | unclassifiable | the typed text is only a paste placeholder and the paste body is not recoverable |

`I`, `D` and `C` together are **high altitude**; `M` is **low**. The
high-vs-low collapse is the robust reading (see §5); the four-way split is the
finer, noisier one.

---

## 2. Decision rules (the boundaries that labelling forced)

These are stated because each one materially moves the distribution. They were
written down as they were encountered, and applied to the whole sample.

**R1 — Pointer-shaped intent is intent.**
"read `NEXT_PROMPT.md`, reflect, execute this milestone" is **I**, not M. The goal
lives in a durable artifact; the turn dispatches it. Brevity here is a *property of
the substrate*, not a demotion of the operator. Getting this rule wrong inverts the
entire exhibit — a well-substrated project's highest-altitude turns are its shortest.

**R2 — Dispatch-by-reference needs a durable referent.**
`I` requires the referent to persist outside the conversation: a file, a named
milestone (`M3`), a plan unit (`week 2 plan`, `round B`, `phase 0 task`), a review
folder. Assent to something the agent proposed *in this conversation* ("go ahead with
the 8-task plan") is **M**. The distinction is precisely whether the substrate or the
transcript is carrying the intent.

**R3 — Bare assent and continuation are mechanical.**
"continue", "ok go", "yes please", "let's continue", "looks sound let's execute" →
**M**. The human is a clock, not a decider. This is the most consequential rule in
the instrument and it is *conservative against the argument*: substrated projects
say "yes, go" too. §5 reports the sensitivity run where these are counted as `D`
instead.

**R4 — Assent becomes a decision when it carries content.**
A selection among presented options ("3", "both, correctness fixes first"), a
rejection ("no — retry for the missing parts"), or an accept-with-qualification
("yes, but without any overclaiming"; "5 scenarios → make it 11") is **D**. The test
is whether removing the turn would leave the choice unmade.

**R5 — A trade-off raised is a trade-off resolved (for classification).**
"should we be more careful with words like *innovation*?" is **D**. The operator is
exercising judgment about the artifact's claims; that the resolution lands next turn
does not make the act mechanical. But a bare request for the agent's opinion with no
named trade-off ("what do you think?") is **M**.

**R6 — Contracts beat goals; the binding clause wins.**
When a turn both declares a goal and binds how future work must be done — quality
gates per step, "do not copy the md files", "document *why*", an ID schema, an
acceptance criterion for the reader — it is **C**. Rationale: any turn can be read as
having a goal, so `I` would otherwise absorb everything.

**R7 — Volume decides genuinely mixed turns.**
Where a turn contains several acts and no clause clearly binds future work, the class
of the *bulk* of the turn wins. Applied to the long feature briefs.

**R8 — Machine output is input, not the act.**
A pasted traceback defaults the turn to **M**, but a stated goal, a resolved choice,
or a bound contract in the same turn wins over it. "clean these warnings [paste] and
make sure all tests still pass" is **I**.

**R9 — Re-transmission is mechanical.**
Re-stating a constraint the agent has lost or violated ("I *asked* you to keep the
quantum-journal paper in its folder…") is **M**, however high-altitude the constraint
itself is. This is the definitional link to WS3(b): the retransmission tax is paid in
mechanical turns.

**Precedence when several rules fire:**
`UNK` → `M`(bare assent, R3) → `M`(retransmission, R9) → `C` → `D` → `I` → `M`(default).

Two asymmetries in how the pasted payload is read, both deliberate:
`C` is tested against the typed text *and* the paste, because an operator who
pastes a specification is shaping the contract — that paste is authored, not
machine output. `I`'s dispatch test (R2) reads the **typed text only**, because a
path inside a pasted stack trace is not a dispatch.

---

## 3. Scope — which turns are classified

Included: operator-typed prompts (`kind == "prompt"`), verbatim, on-project.

Excluded, each counted and reported rather than dropped silently:
- **slash turns** (`/clear`, `/model`, `/effort max`) — operator actions with no
  altitude content;
- **rendered-only Copilot turns** — machine-composed briefs; classifying them would
  measure the renderer;
- **off-project turns** — printer troubleshooting, phone forensics and phishing
  reports done inside a corpus folder;
- **UNK** — paste-only turns whose paste body did not survive.

---

## 4. Known biases of the instrument

1. **Self-labelling.** The author of the method labelled his own turns. Countered by
   publishing every label with its reason, and by R3 being conservative against the
   argument.
2. **Verbosity confound — the largest one, and it is measured.** Long turns carry
   more cues, so they classify high more easily: btest's high share runs
   0.08 → 0.15 → 0.35 → 0.65 across the 0–39 / 40–119 / 120–399 / 400+ character
   bands. No cross-project altitude comparison is publishable without the
   length-banded table beside it (`by_length_band` in `altitude.json`).
3. **`M` is the residual sink.** A high-altitude turn with no lexical cue —
   "ok next how about we create a cli terminal for this" — falls to `M`. The
   corpus is also typo-dense ("qality gates" does not match `quality gate`), and
   every miss lands in `M`. The bias therefore runs *against* the argument:
   published high-altitude shares are floors, not estimates.
4. **Era confound.** Model capability improved across the corpus window; later turns
   can be shorter for reasons that have nothing to do with substrate. Within-project
   chronology (btest) is the control that partly absorbs this.
5. **The taxonomy is one author's.** No second rater exists. The reported
   hand-vs-automated agreement is therefore an *instrument-stability* number, not an
   inter-rater reliability number. It is labelled as such everywhere it appears.

---

## 5. Reporting rules

Every published altitude figure carries: n, the excluded counts, the high/low collapse
alongside the four-way split, and the R3 sensitivity run (bare assent counted as `D`).
A distribution is never shown without its project's rubric score and complexity
profile next to it (PLAN §WS-X).
