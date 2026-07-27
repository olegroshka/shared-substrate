# Speaker notes — Does the substrate matter?

**For the talk (1h slot, flexible talk/discussion split).** The deck (`slides.md`) is a
core arc of 47 slides (~35–40 min full, compressible toward ~30) that is complete on its
own, plus six optional modules behind an explicit divider. **The room sets the length;
these notes exist so the flex is rehearsed, not improvised.** The dry run rehearses the
branch points below, not a fixed script (PLAN §9).

**Public-surface reminder.** This file is committed to the public repo. The in-room talk
may name the work project's component and employer — they are in the circulated internal
abstract. The committed deck says only "a legacy component at a regulated financial
institution"; on slides 2–3 and the spectrum slide (43), **name it verbally**. Nothing on
a slide, in the handout, or in these notes carries the name.

**Standing rules for any future deck edit** (all per Oleg, S9):

- **Style — guided interpretation** for a general professional audience: every exhibit's
  interpretation walks the viewer through what the number means and what follows from
  it, in full sentences; no aphoristic fragments, no mid-dot number chains, no insider
  shorthand without a plain-language gloss. The paper's three practice aphorisms remain
  as quotes, each with a plain-language explanation on the slide. Claim strength stays
  pinned to the bench captions — wording may change, claims may not.
- **Voice — experience shared, never lectured.** No prescriptive second person; first
  person ("I will argue") or third person ("the human", "the operator"). Deliberate
  exceptions where addressing the room *is* the point: the closing question, the
  self-score invitation, and "Your substrate will not look like mine" (peer voice).
- **No invented setting.** Nothing on an artifact may assume a scene the materials do
  not establish — no "tonight", no "stage". Setting-neutral phrasing only ("this talk",
  "here", "the audience").
- **Self-sufficiency.** A first-time viewer needs no prior context: every entity
  introduced before first use, every term glossed on the slide that uses it.

---

## Slide map (the deck's own numbering)

§1 the case: 2–3 · §2 frame: 4 era · 5 substrate defined · 6 purpose · 7 offload test ·
8 inversion · 9 precedents · 10 personal substrate · 11 frame picture ·
12 thesis/reframe · 13 corpus · 14–16 exhibits (retransmission, short messages,
re-entry) · §3 practices: 17 divider · 18 decomposition · 19 complexity moderator ·
20 guardrails · 21 probe negative · 22 representation + retrieval result · 23 zero
silent reversals · 24 the null · 25 baseline moved · 26 addressability pair ·
27 classification vs citable · 28 survivorship · 29 discipline's own failures ·
30 validation · 31 rework · 32 two honest findings · §4: 33 scorecard · 34 METR ·
35–38 four negatives · 39 corrections · 40 the miss · 41 attention exhibit ·
42 confounds ledger · §5: 43 self-score · 44 practical menu · 45 closing question ·
46 cannot-claim · 47 close · 48 modules divider · 49–56 M-A…M-F + appendix.

**Never-cut set:** 4 (era), 5 (the definition — the title's word), 10 (personal
substrate), 12 (reframe), 13 (corpus — without it the project names mean nothing),
14 (retransmission tax), 24 (null), 39 (corrections), 40 (the miss), 42 (ledger),
44 (practical menu — it is what the abstract advertises).

---

## The origin anecdote — thirty seconds, no more

> I was asked, entirely reasonably, to account for some heavy AI-credit usage. Fair
> question. But the honest answer wasn't a number — it was that the question is about
> the wrong resource. The scarce thing isn't credits, it's what the credits were being
> converted *into*, and whether any of it survived the session that produced it. This
> talk is what happened when I tried to answer that properly.

Thirty seconds gets from the question to the thesis. It is stage-setting, not content —
do not let it grow. If someone asks about the credit question later, that is discussion
time, not arc time.

---

## Time skeleton (indicative, not a clock)

| segment | slides | ~min | can compress to |
|---|---|---|---|
| 1 · The case, cold | 2–3 | 4 | 2 (skip the yardstick detail, keep 18/24 + "credible because not top") |
| 2 · What is shifting + frame + corpus + exhibits | 4–16 | 14 | 9 (slides 6–7 in one breath — the table carries both; speak slide 9's precedents over slide 10 rather than cutting them; A1 alone can carry the exhibits) |
| 3 · Four practices | 17–32 | 12 | 8 (3.3 is the spine; 3.1 can be one sentence over the figure) |
| 4 · Research examined | 33–42 | 9 | 5 (negatives 1+4 spoken from one slide; corrections and the miss never cut) |
| 5 · Interactive + close | 43–47 | 5+ | elastic — this is the buffer |

Two hard rules whatever the pacing: **the confounds ledger and the METR slide are
spoken, never skipped** — the honesty is the structure; and **no exhibit is shown
without reading its caveat line** — an exhibit without its caveat is misquoting the
report, even when every digit is right.

---

## Branch-point map

**Default posture: run the core arc.** Expand only on a trigger; compress only into the
interactive segment, never by dropping caveats.

### Expands when the room listens (quiet, attentive, no questions by §3)

| after | trigger | pull in |
|---|---|---|
| §1 (slide 3) | management-heavy room, nods at "parity/UAT", glazes at "rubric" | stay in the case study longer: tell the week-0/week-2 shape verbally (spec and verification were the bottleneck, generation was cheap); borrow phrasing from `docs/management-brief.md`; skip M-* entirely and give the fuller §4 |
| §2 (slide 16) | "how did you measure that?" body language, engineers leaning in | **M-C** (session-log deep dive) after the core arc, or a 60-second verbal version now: three log stores, 1,061 messages, hand-labelled before the classifier existed |
| §3.2 (slide 21, the probe negative) | interest in the probe design ("how do you probe confabulation?") | **M-D** — the pre-registration story plays well told as narrative: frozen by commit, 3 questions discarded against my own hypothesis |
| §3.3 (slide 24, the null) | the null lands well / someone says "refreshing" | **M-B** war story 3 — one session, two defects, in the 22/24 project; it deepens the null instead of defending it |
| §3.4 (slide 31, the rework contrast) | "isn't that rework number confounded?" asked *with interest* rather than challenge | **M-E** — show the full table with the † footnotes; the honesty of the 14-day-window restriction converts skeptics |
| §4 (slide 42, the confounds ledger) | room still listening at the confounds ledger | **M-A** then **M-B** — the spectrum walk and war stories are the best listening material; **M-F** only if the room is research-minded |

### Compresses when the room engages (questions before §3, discussion catching fire)

- Compress §3.1 to one sentence over the hierarchy figure (the corpus case: a 117-file
  CLI that skipped half the menu and was right to).
- Compress the four negatives to negatives 1 and 4 spoken from the first negative
  slide, but **say the count**: "four honest negatives, separately — never a pattern
  of four."
- Move the handout **earlier** — it is the best discussion fuel; the spectrum slide
  (42), the practical menu (43) and the closing question work as a discussion frame
  from minute 20 onward.
- Never compress anything in the never-cut set (see the slide map above).

### The interactive segment (elastic buffer)

Hand out `handout-rubric.md` printed. Two minutes silent scoring, then two discussion
axes: *where are you on the spectrum* (slide 43) and *did Step 0 stop you — and was
that a relief?* The datacli example legitimises low scores; use it to keep the segment
from becoming confession hour. The practical menu (44) answers "so what do I actually
do" before anyone asks it. Close on the delegating-vs-keep-going question regardless
of time.

---

## Per-slide "if challenged" lines

The answers are already written; the line's job is to concede first, then place the
pointer. Never improvise a stronger defence than the report makes.

**Slide 3 · the 18/24 rubric row.**
*Challenge: "you scored your own work project from memory?"*
Concede: four of eight axes are inferred from the written account, PROVISIONAL-INFERRED,
and A5 is the lowest-confidence cell in the whole matrix — I'll overrule it from memory
if memory disagrees. The row is refreshed in-org against real history as the follow-up
leg. Note also: review moved two *other* projects' scores down, against my own argument.
→ REPORT §1; `data/rubric-scores.json`.

**Slide 4 · the era claim.**
*Challenge: "aren't you just restating the Google paper?"*
The quote is the floor; the claim is the building. Google's framing stays inside
software engineering — coder to conductor to orchestrator, a syntax tax replaced by a
verification tax. The substrate claim is about how humans engage with information in
any discipline whose work is thinking made durable — and note that the talk's evidence
is deliberately *not* about code generation at all: warm-up costs, decision records,
attention levels are information behaviours, not coding behaviours.
*(Before the talk: verify the quote wording against the whitepaper itself — Google,
"The New SDLC: From Vibe Coding to Agentic Engineering", 2026, Osmani et al.; S9
confirmed it via secondary sources only.)*

**Slide 9 · the historical precedents.**
*Verify before the talk, and the honest version if challenged.* The calculator
resistance is documented (1970s–80s US curriculum debates; the professional bodies
later endorsed calculator use; curricula moved up). The loom case: the canonical
violent machine-breakers were the **English Luddites** (1811–1816); the **French** case
on the slide is **Lyon silk weavers destroying early Jacquard looms** (c. 1801–1806,
with ~11,000 Jacquard looms in France by 1812 — the commonly cited figure; the
machine-smashing accounts are partly traditional retellings). If challenged on either:
concede the detail, keep the pattern — the honest clause is already on the slide (the
transition was hard on those who could not move). The punch-cards-to-computing lineage
(Jacquard → Babbage → Hollerith) is solid and is the reason the French case is the one
told.

**Slide 14 · retransmission tax.**
*Challenge: "isn't that just btest having longer sessions / pasting more?"*
Concede both: btest's sessions lengthened 9.1 → 19.8 messages, and paste bodies survive
in only 74 of 204 paste-referencing messages — which *under*-counts payload warm-ups, so
the bias runs against my finding, not with it. → exhibits A1;
`data/session-metrics/warmup.json`.

**Slide 15 · delegation-per-assent.**
*Challenge: "0.10 on what n?"*
It's on the slide: 3 work-delegating short messages against 29 "continue"s — two more
found would move it. The robust part is the volume (147 short messages, 19% of btest's
typing), not the ratio. → exhibits A4.

**Slide 24 · the pre-registered null.** *(The most likely fire.)*
*Challenge: "so your experiment disproved your own thesis."*
Concede immediately: it failed to show the substrate reduces confabulation, p = 1.0,
published as it came out — and the one confabulation is the full-substrate project's.
Then the two facts that size it: the "flat" arm carries a 212-line agent-instruction
file — enough to explain the null on its own — and the reversed direction rests on one
invented answer; the null survives any single re-scoring. The claim I am defending here
is the reframe (human's side of the loop), which does not rest on this experiment. The
deck itself concedes, on the very next slide (25), that the original formulation was
too strong: whether a model invents an answer depends on the model and what it can
read, not merely on discipline — the surviving exposure is claims with no readable
ground truth anywhere.
→ REPORT §3.3; exhibits C1; pre-reg commit `ab9c62d`.

**Slide 25 · "the baseline has moved".**
*Challenge: "then why bother with a substrate at all?"*
Because retrieval was never the expensive part. The tax is on the human's side —
re-entry cost, delegation vs assent, findable reasons — and that is where every robust
number in this corpus sits. → REPORT §2.

**Slide 26 · the Python 3.12 pair.**
*Challenge: "that's one anecdote."*
Yes — a single paired case by construction, labelled a case study on the slide, and it
*follows* the two robust results rather than carrying the claim. It is the corpus's
only same-operator, same-day, same-decision control. → exhibits D1.

**Slide 27 · the tag curve.**
*Challenge: "so btest just stopped being disciplined."*
No — that's the reading the original exhibit invited and the correction withdrew. 280
of 293 tags belonged to a subproject that left the repo; July is
conventionally-prefixed at 90%. The defensible claim is narrower: the *citable*
convention collapsed in April, and what replaced it classifies without being citable.
→ exhibits B2; war-stories §6.3.

**Slide 28 · survivorship.**
*Challenge: "how much of this artifact story is survivorship bias?"*
It is the most serious confound in the eval, it is correlated with the treatment, and
it was raised by the operator, not caught by an instrument. Measured across three
channels, then hand-adjudicated *down* (≥26 → ≥10; 16 false positives itemised). Two
properties: the noise is one-directional and runs with my hypothesis; and the
agent-side channel couldn't see the substrated project's own memory files at all. All
counts are lower bounds. → REPORT §4.5 confound 6; `data/survivorship-audit.json`.

**Slide 31 · the 82.2% rework contrast.**
*Challenge: "5× longer history — of course more lines died."*
Correct, and the slide says so: supporting texture, not a controlled result. The
comparable column is the 14-day one (32.6% vs 3.9%, an 8.4× gap), restricted to the
three repos long enough to support it. The line-matching method is approximate, biases
published. → exhibits A3; `data/git-metrics/`.

**Slide 40 · the deck-building miss.**
*Challenge: "your own agent failed — doesn't that undermine the whole approach?"*
The opposite, and say it plainly: the framework predicted the failure class (every
check either arm owns runs at read time — already on slide 32), it supplies the
instrument that would catch it (a fresh-context decode test — the probe pointed at
deliverables), and the catch itself is the §2 inversion doing its work: the human
judgment that cannot be offloaded, being the job. Keep it a shape with two in-corpus
siblings, each seen once — never a rate.
*Delivery: self-deprecating and quick — the room will enjoy it; do not let it become
an AI-bashing beat. The point is the failure class and whose job the catch is.*

**Slide 41 · the closing attention exhibit.**
*Challenge: "your classifier, your labels, your κ."*
One rater, so κ = 0.902 is consistency, not independent agreement — it's on the slide.
The labels were frozen before the classifier was written, on a pre-assigned held-out
split, and the raw (ungrouped) comparison is *rejected* in this talk because it
flatters the wrong project. → exhibits A2; `rubric/ALTITUDE.md`.

**Slide 43 · the spectrum.**
*Challenge: "the rubric measures your own method — circular."*
Confound 4, named on the ledger slide: the rubric was written by the person whose
method it measures, which is why it never appears without outcome evidence beside it,
and why the corpus includes boundary cases expected *not* to show the effect. Review
moved two scores down. → exhibits E1.

**Anywhere · "what about METR?"**
Agree before defending: 19% slower while feeling 20% faster, experienced devs, mature
repos — including my own felt productivity. That result is why this evaluation measures
behaviour instead of asking me how it felt. → REPORT §4.2.

**Anywhere · "one author, one domain — this proves nothing."**
Concede the scope plainly — REPORT §6 lists what this evaluation is not allowed to
claim, and "works for anyone else" is on the list. The honest offer is the instruments,
not the conclusions: rubric, probe protocol and miners are portable and re-runnable on
anyone's repo. → REPORT §6; PLAN §5.

---

## Module cheat lines (what each is *for*)

- **M-A** — for "where would my project land?" energy. Walk the matrix top-to-bottom by
  *axis*, not project; the inverse-profiles point (guardrails-strong vs
  representation-strong) is the take-home.
- **M-B** — for a listening room. Stories in receipt order: 1 (typed absence), 2 (option
  dropped by omission), 3 (born-wrong records), 4 (reasoning without an address). Each
  opens with its robust number, per the rules. Story 3's file-and-line requirement is a
  **proposal seen working once**, never a finding.
- **M-C** — for methodology skeptics. Lead with "hand-labelled 99 messages before
  writing the classifier"; the orientation-cost refusal (3.8× spread at n=2, no claim)
  buys more credibility than any positive number.
- **M-D** — for experimentalists. The discarded-questions story (15% of the instrument,
  every discard against the hypothesis) is the module's spine.
- **M-E** — for git archaeologists. Keep the † footnote discipline audible: three
  projects are shorter than the churn window.
- **M-F** — only for a research-minded room. Be plain that κ was not attempted and no
  kernel numbers exist.

---

## Dry-run checklist (branch points, not script)

- [ ] Origin anecdote lands in ≤30 seconds (time it).
- [ ] Each never-cut slide (4, 5, 10, 12, 13, 14, 24, 39, 40, 42, 44) can be delivered
      from memory.
- [ ] Practise the §3.3 sequence twice — robust → robust → null → concession → case
      study is the talk's hardest transition and its whole credibility.
- [ ] Practise *both* §4 lengths: full four-negative version and the compressed
      two-negative version.
- [ ] Rehearse the three likeliest challenges out loud: the null, the rework confound,
      the survivorship correction.
- [ ] Verify the Google-quote wording and the slide-8 precedents (notes above).
- [ ] Verify the room copy of the deck renders (Marp) and the handout is printed.
- [ ] Decide before walking in: which module to give if the room listens
      (recommendation: M-B — the stories carry the caveats naturally).
