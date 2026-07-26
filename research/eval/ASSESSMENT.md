# Mid-evaluation assessment — does the evidence carry the thesis?

**Written:** 2026-07-26, after S5 (WS4b probe + SC8 review), before WS5 and WS6.
**Status:** author judgment, not a computed artifact. Kept as a standing document
so S8 (report assembly) inherits the reasoning rather than re-deriving it, and so
the reframe below can be argued with rather than absorbed silently.
**Revisit after S6 (WS5 survival) and S7 (WS6 archaeology)** — both can move it,
and §6 says how.

> One-line summary: the thesis is **partially supported, and not where PLAN §1
> expected**. The measurable benefit of the substrate has moved from the model's
> side of the loop to the human's.

---

## 1. Scorecard against PLAN §1's four claims

| claim | verdict | carried by |
|-------|---------|-----------|
| **1. Paradigm** — the human's contribution migrates up the abstraction stack, and the substrate enables it | **Partial** — survives only length-controlled | WS3 findings 1–3 |
| **2. Failure modes** — drift, phantom decisions, restart cost, reference rot follow the absence of substrate | **Split** — restart cost yes, **phantom decisions null** | WS3(b) positive; WS4b null |
| **3. Practice** — same author, same domain, with and without the discipline | **Weak** — the "without" arm is not actually without | WS2 finding 2; WS4b finding 10 |
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

---

## 4. The recommended reframe

Not a weaker version of the original claim — a different and sharper one:

> The substrate's measurable benefit is **on the human's side of the loop, not the
> model's.** A good agent-instruction file and a strong model will retrieve your
> recorded facts. What they cannot do is make re-entry cheap, keep your short turns
> as delegation rather than assent, or preserve the *reasons* behind decisions. That
> is what the substrate buys, and it is what decays when you stop paying for it.

Why this is the right move:
- It is carried by §2.1, §2.2, §2.3 and §2.5 — the exhibits that survived scrutiny.
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

## 6. What could still move this

**WS5 (S6) is the one that can still add causal weight.** The question is not how
many ADRs survive — in an append-only corpus nearly all will — but whether any
decision was **contradicted in code while the record stayed put**. There is a free
first data point: blive's OQ-035 claims a three-order-type surface where
`src/blive/domain/types.py` declares seven plus an OPG time-in-force. If that pattern
is rare in blive and common in btest, it is a genuine exhibit. If it is common in
both, that is another honest negative and §4's reframe hardens further.

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
