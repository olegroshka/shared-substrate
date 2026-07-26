# Mid-evaluation assessment — does the evidence carry the thesis?

**Written:** 2026-07-26 after S5 (WS4b probe + SC8 review). **Revised same day after
S6** (WS5 survival + the artifact-survivorship audit) — see §2.3, §3.2, §3.8, §4,
§5.1 and §6.
**Status:** author judgment, not a computed artifact. Kept as a standing document
so S8 (report assembly) inherits the reasoning rather than re-deriving it, and so
the reframe below can be argued with rather than absorbed silently.
**Revisit after S7 (WS6 archaeology)** — §6 says how.

> **Read §5.1 first if you are deciding what goes on a slide.** The corpus splits
> cleanly into about five findings that rest on hundreds of observations and about
> seven that rest on a single event. They are not interchangeable, and the split is
> not random: the robust half is all *human-side* behaviour, the fragile half is all
> *model-side* probing.

> One-line summary: the thesis is **partially supported, and not where PLAN §1
> expected**. The measurable benefit of the substrate has moved from the model's
> side of the loop to the human's.

---

## 1. Scorecard against PLAN §1's four claims

| claim | verdict | carried by |
|-------|---------|-----------|
| **1. Paradigm** — the human's contribution migrates up the abstraction stack, and the substrate enables it | **Partial** — survives only length-controlled | WS3 findings 1–3 |
| **2. Failure modes** — drift, phantom decisions, restart cost, reference rot follow the absence of substrate | **Split** — restart cost yes, **phantom decisions null** | WS3(b) positive; WS4b null |
| **3. Practice** — same author, same domain, with and without the discipline | **Weak** — the "without" arm is not *without*, it is **ephemeral** | WS2 finding 2; WS4b finding 10; **§3.8 survivorship** |
| **4. Boundary** — exploratory research is out of scope | **Supported, and refined** (improves the paper) | WS1 finding 1 |

---

## 2. What the evidence genuinely supports

**2.1 The retransmission tax — the strongest exhibit in the corpus, and the direct
answer to "does the substrate keep intent hot?"**
blive warms up in **9 of 10** sessions at **~106 characters**, and the cost *falls*
across the project's life (192 → 106). btest warms up in **43 of 68** sessions at
**~417 characters**, and the cost *rises* (477 → 607). Four times the cost, half as
often, moving the wrong way — same author, same domain. This is intent going cold,
measured. *(WS3 finding 4; `data/session-metrics/`.)*
Caveats that travel with it: btest's sessions also got longer (9.1 → 19.8 turns), and
paste bodies survive for only 74 of 204 paste-referencing turns, so payload-shaped
warm-ups are **under**-counted — conservative against the finding.

**2.2 Brevity means opposite things in the two postures.**
Among turns under 40 characters, dispatch-by-reference ("read `NEXT_PROMPT.md`,
execute") per bare assent ("continue"): seamQ **5.0** · b-autobot **0.50** · blive
**0.25** · btest **0.10** (3 dispatches against 29 "continue"s). In a substrated
project a short turn is delegation; in a flat one it is a clock tick. btest also has
the most short turns: 147, 19% of everything it typed. *(WS3 finding 3.)*

**2.3 Decisions get deposited; reasons do not.** This held across all three probed
projects and is the cleanest pattern WS4 produced:
- b-autobot's conversational decisions were **all** deposited in code or design docs —
  S4 could not construct a conversation-only question for it at all — but its
  *reasons* were gone. *(questions-p3.md declared deviation; WS4a finding 2.)*
- blive's single confabulation in 38 scored answers was an invented **why**.
- Recorded facts came back near-perfectly everywhere: blive 28/28, btest 28/28,
  b-autobot 24/28.
The substrate boundary is not retrieval. It is rationale.

**Corrected by WS5 (S6):** the last line is too strong. btest recorded the *why* for
its Python 3.12 change, and recorded it well — 1,025 characters in commit `fd106f9`
giving the reason, the validation (317 tests on 3.12, dependency wheels confirmed),
the exact edits and a flagged follow-up. What it lacks is **addressability**: blive's
ADR-053 is cited from five artifacts including the one an agent auto-loads; btest's
reasoning is cited from zero and reachable only by knowing the sha. The accurate
statement is **"reasons are deposited unevenly and unaddressably"**, not "reasons are
not deposited." *(WS5 finding 3 — and it is the corpus's only clean control: same
operator, same day, same decision, both repos.)*

**2.4 The research boundary claim got better, not worse.** Research projects score
mid-high through *research-native* instruments — harp's pre-registration with
stop-for-futility rules, smim's notation sheet and kill rules, seamQ's three-persona
adversarial review. A pre-registration **is** a frozen intent contract. The paper's
"does not apply to exploratory work" becomes "applies with different artifact types
and lifecycle". *(WS1 finding 1.)*

**2.5 btest's own decay curve** — within-project, so no cross-project confound.
Bracketed stable-ID commit share by month: 0% (Dec–Feb, pre-methodology) → 91% (Mar)
→ **96% (Apr, peak)** → 50% (May) → 40% (Jun) → **0% (Jul)**. The last 13 commits
carry no tag at all. *(WS2 finding 2.)* Note this measures *adoption*, not outcome.

**2.6 Artifact survivorship — new in S6, and the strongest single number in the
corpus.** Across three independent channels (typed prompts over 1,480 turns,
JetBrains LocalHistory change records, Claude Code tool-call paths), against every
basename any corpus repo ever added on any ref: **blive 0 of 33 observed artifacts
never reached git. btest at least 26 of 105. seamQ at least 33 of 89.** These are
lower bounds. It is an independent channel from §2.1's warm-up measurement and it
points the same way: blive's state persisted, btest's evaporated.
*(`data/artifact-survivorship.json`; see §3.8 for what it costs.)*

---

## 3. What the evidence does not support, and must be said out loud

**3.1 The one controlled experiment came back null — and after review it reversed.**
WS4b, pre-registered at commit `ab9c62d` before any run: btest **38/38 correct, zero
confabulations**; blive **37/38 with the corpus's only confabulation**; b-autobot
36/38, zero confabulations. Fisher's exact two-sided **p = 1.0**, identical under the
SC9 sensitivity reading.

The reason matters more than the number: **a 212-line CLAUDE.md plus git history plus
a 2026-era model was enough for a perfect score.** The floor has risen. "Your agent
will invent decisions without a substrate" is no longer true of a fresh agent doing
retrieval, and a room of daily Claude Code users will know that from experience.
Conceding it from the stage is worth more than having it raised from the floor.

**3.2 The "unsubstrated" arm is not unsubstrated.** btest carries a 212-line
agent-instruction file; what it lacks is decision *records*. Six of its twenty run-1
probe answers were correct with **zero tool calls**, straight out of `CLAUDE.md`.
Every substrated-vs-flat exhibit needs that qualifier, and it may explain the null on
its own. *(WS4b finding 10.)*

**3.3 Altitude does not track discipline inside btest.** Monthly high-altitude share
0.256 (Mar) · 0.251 (Apr) · 0.192 (May) · 0.400 (Jun, n=5) · 0.303 (Jul) against a
tag curve of 91 → 96 → 50 → 40 → 0%. July has btest's least artifact discipline and
its second-highest altitude. PLAN §4's hope that the migration is visible in btest's
chronology is **not supported**. *(WS3 finding 5.)*

**3.4 The rework contrast is real but confounded.** blive 3.9% vs btest 32.6%
short-horizon churn (8.4×), 5.2% vs 82.2% at any horizon (16×). But btest's history
is 5× longer (213d vs 41d), which gives its lines more opportunity to die, and the
two projects differ in nature. Texture, not proof. *(WS2 finding 1; PLAN §7 risk 1.)*

**3.5 The naive cross-project altitude comparison fails outright.** Raw high-altitude
share puts b-autobot (0.46) — the *least* substrated build — near the top. The
ordering is mostly turn length. No altitude number is publishable without its length
band. *(WS3 finding 1.)*

**3.6 The discipline has a failure mode of its own.** blive's `OPEN_QUESTIONS.md`
OQ-033 records an *"Operator decision (2026-06-06): source from EODHD — not from
sfera"* against an option the operator confirms **was never on the table** (the
standing plan was always EODHD + IB). The readiness audit formalised a default into a
dated decision. Append-only records can manufacture history as well as preserve it.
*(WS4b finding 7 — the most intellectually honest thing the evaluation turned up.)*

**3.7 Three of twenty probe slots were voided** — 15% of the instrument — because
their ground truth did not hold. That is a finding about the S4 question design, not
about the projects, and it is why the **Tier A/B evidence rule** now binds the whole
report: a claim that "we decided X" must rest on an artifact that *states* the
decision; a decision inferred from a diff, rename or config change may ground a claim
about the **state** of the code, never about a decision. *(WS4b finding 8.)*

**3.8 The rubric measured what survived, not what was practised — and the bias runs
with the hypothesis.** This is the most serious methodological problem in the eval and
it was found by the operator, not by the instrument. Working artifacts — plans,
roadmaps, review prompts, iteration notes — were routinely created, used and deleted
without ever being committed. blive's CONTEXT_PROTOCOL requires the substrate to be
committed; btest had no such rule. So WS1's blive-22 / btest-12 gap is **partly an
artifact of what survived**, and the survivorship correlates with the treatment, which
is the worst kind of confound rather than noise.

What it costs and what it does not:
- **WS1's adoption scores are scoped, not wrong.** They measure *durable* substrate.
  RUBRIC.md now says so; PLAN §7 carries it as confound 6. They are **not re-scored**,
  because existence is recoverable and content is not — LocalHistory here has no content
  store, and the CC transcripts cover only the surviving retention window. A filename
  cannot distinguish a maintained decision log from an empty stub, so any "correction"
  would be invention.
- **WS2, WS3 and WS4 are untouched.** WS2 is commit-derived, WS3 is turn-derived, and
  WS4 asked what a fresh agent can recover *today* — for which deleted files are
  correctly invisible. That is the question, not a flaw in it.
- **WS5 finding 4 is narrowed**: btest's instruction file does not decay silently *as
  committed*.
- **§3.2 gets stronger, not weaker.** The "unsubstrated" arm is even less unsubstrated
  than the 212-line CLAUDE.md already showed.
- **The framing changes everywhere: flat → ephemeral.** btest was not working without
  artifacts. It was working with artifacts that did not survive — which is nearer to
  what the paper actually argues, since the paper's claim is that the substrate carries
  state *between* sessions. An artifact deleted at session end carries nothing.

---

## 4. The recommended reframe

Not a weaker version of the original claim — a different and sharper one:

> The substrate's measurable benefit is **on the human's side of the loop, not the
> model's.** A good agent-instruction file and a strong model will retrieve your
> recorded facts. What they cannot do is make re-entry cheap, keep your short turns
> as delegation rather than assent, or make your reasoning **findable later**. That
> is what the substrate buys, and it is what decays when you stop paying for it.

**Amended after S6, in the one place it was overstated.** The original wording said the
substrate preserves "the *reasons* behind decisions". WS5 finding 3 shows that is not
what separates the two arms: btest recorded its Python 3.12 reasoning *well*, in a
commit body. What it lacks is **addressability** — a stable id, an index, and a citation
from the file the agent loads on entry. And §2.6 shows the deeper version: btest's
working artifacts were not absent, they were **ephemeral** — at least 26 of them existed
and never reached git, against blive's zero. So the sharpest form of the claim is:

> The substrate is not what makes you write things down. It is what makes what you
> wrote down **still be there, and still be findable**, three sessions later.

Why this is the right move:
- It is carried by §2.1, §2.2, §2.5 and §2.6 — the exhibits that survived scrutiny,
  and per §5.1 **all four are in the robust half**. The reframe does not rest on a
  single event anywhere.
- **The null becomes evidence for it**, not against it: WS4b isolates where the
  effect isn't (retrieval of recorded facts) and therefore sharpens where it is.
- It is honest about 2026. The model got better; the argument moved. Saying so from
  the stage is the credibility play.
- It stays inside the paper's own frame — the substrate carries state "between
  sessions, tools, and minds", and *minds* includes the operator's across a gap.

What this costs: the phantom-decision result can no longer be the headline exhibit
for "System representation" in the four-practices arc (PLAN §9 core arc, item 3). It
becomes an honest negative told alongside the survival curve. The talk should
probably lead that practice with §2.3 (decisions deposited, reasons lost) instead.

---

## 5. Standing caveats on the whole corpus

- **n is small everywhere it matters.** The probe headline rests on **one**
  confabulation. Rework and altitude comparisons rest on 2–4 measurable projects.
- **The author designed the instrument, ran the study, and scored it.** Countered by
  pre-registration (WS4), frozen keys, conservative tie-breaks that run against the
  hypothesis, published sensitivity readings, and operator review — not eliminated.
- **P1 vs P2 is a case comparison, not an experiment**, except WS4 which was
  controlled and came back null. Age, project nature, model era and the author's own
  learning all co-vary. *(PLAN §7 risks 1–2.)*
- **METR remains the standing reminder**: experienced devs 19% slower while feeling
  20% faster. Including the author's own felt productivity. This ledger is what
  separates the talk from advocacy.

---

## 5.1 Fragility ledger — which findings rest on a single event (added S6)

The honest worry about this corpus is that too much is being carried by too little:
one confabulation, one manufactured decision, one stale doc claim. That worry is
**correct for half the findings and wrong for the other half**, and the split is not
random — so it is worth naming rather than feeling.

**Robust — many observations; a single re-scoring cannot move them.**

| finding | rests on | what would actually flip it |
|---|---|---|
| §2.1 warm-up cost (blive 106 falling / btest 417 rising) | 78 sessions, 1,061 classifiable turns | a systematic classifier error, not one turn |
| §2.6 artifact survivorship (blive 0/33 · btest ≥26/105) | 3 independent channels, 138 artifacts | a wrong committed-pool definition; individual names are spot-checkable |
| §2.5 btest's tag-decay curve (0→91→96→50→40→0%) | 415 commits | a regex error — and one was already caught and fixed (110 vs 293) |
| §3.4 rework contrast (5.2% vs 82.2%) | tens of thousands of lines | the LIFO approximation being wrong in one direction, which is documented |
| §3.5 length-banded altitude (btest lowest in all 4 bands) | 1,061 turns, held-out κ=0.902 on the high/low split | re-labelling a whole band |

**Fragile — one event, or a handful; label them as texture and never lead with them.**

| finding | n | what flips it |
|---|---|---|
| §3.1 H-1's *direction* | **1** confabulation | re-scoring blive P1-Q20 → 0 vs 0. The **null survives either way**; only the reversed direction is fragile |
| b-autobot's clean sheet | **2** abstentions on an SC7 tie-break | read as commitments → b-autobot 0 → 2 confabulations |
| WS5 record-fact drift (OQ-035, "~2600 LOC") | **1 per project** | a second reader disagreeing on either |
| WS5 the Python 3.12 pair | **1**, by construction | nothing — but it is a case study, not a rate |
| §3.6 manufactured decision (OQ-033) | **1** | operator recollection changing |
| WS4b DEC-N2 "0 for 3" | **3** negative constructions | one successful construction |
| §2.2 dispatch ratio | btest numerator is **3** dispatches | two more dispatches found |

**The pattern in that split is the finding.** Every robust row measures *the operator's
behaviour repeated over hundreds of sessions*. Every fragile row measures *an agent's
behaviour on one question*. That is not bad luck — it is structural: human-side
behaviour repeats and can be counted, and one-shot probes cannot be, at this corpus
size. Which is precisely why §4's reframe is the defensible one. **The reframe is
carried entirely by the robust half.** The fragile half is what makes it interesting,
not what makes it true.

Two rules that follow, binding on S8 and S9:
1. **Nothing from the fragile table leads a section or carries a claim.** They are
   illustrations after a robust number has been shown, and each is stated with its n.
2. **No fragile finding is ever aggregated with another** to imply a rate. "One
   confabulation and one manufactured decision and one stale claim" is three anecdotes,
   not a trend of three.

---

## 6. What could still move this

**WS5 (S6) — ANSWERED, and neither predicted branch happened.** This section asked
whether decisions were contradicted in code while the record stayed put, and predicted
two outcomes: rare-in-blive/common-in-btest (a genuine exhibit) or common-in-both
(another negative). The answer was a **third branch: rare in both — exactly one per
project — and neither is drift.** blive's OQ-035 and btest's "~2600 LOC" were both
**wrong on the day they were written**, about code that had not changed. Zero blive
ADRs were silently reversed, S(k)=1.000 at every k. So WS5 added causal weight in an
unexpected place: not in a survival rate, but in the Python 3.12 paired case (§2.3,
§4) and in the survivorship audit it provoked (§2.6, §3.8).

**WS6 (S7) is narrative, not statistical** — but it is where §3.6's manufactured
decision lives, along with b-autobot's stale CLAUDE.md references, harp's
"conversation-only items" ledger, and btest's scar tissue. Expect it to strengthen
the *practice* story and not the *measurement* story.

**Nothing pending on Oleg.** The one open judgment call in the corpus is still
**P8 A5** (rubric decisions axis, 2 PROVISIONAL-INFERRED), settleable only from
memory and not worth blocking on.

---

## 7. Honest bottom line

The corpus will not produce a knockout number and should not be presented as though
it might. What it supports is a more careful thesis than the plan started with, plus
a confounds ledger that is unusually well earned. For a room that has heard a lot of
AI-productivity stories, **"here is what my own pre-registered experiment failed to
show"** is likely to buy more credibility than the exhibit that worked.

**Added after S6.** Two of the sharpest items in this document — the survivorship
confound (§3.8) and the fragility split (§5.1) — exist because the *operator* pushed
back on the evaluation, not because an instrument caught them. That is worth saying
from the stage: the honest reading is that this corpus has had one motivated
adversarial reader, and it found real problems in a day. It has not had two.

And the §5.1 discipline is what keeps the talk defensible under questioning. Five
findings rest on hundreds of observations; seven rest on a single event. If a slide
leads with one of the seven, the first sharp question in the room ends the argument.
If it leads with one of the five, the seven become the interesting colour that makes
the five memorable. **That ordering is the whole difference between a case study and
an anecdote.**
