# Speaker notes — Does the substrate matter?

**For the 2026-07-30 talk (1h slot, flexible split).** The deck (`slides.md`) is a core
arc of ~30 minutes that is complete on its own, plus six optional modules. **The room
sets the length; these notes exist so the flex is rehearsed, not improvised.** The dry
run rehearses the branch points below, not a fixed script (PLAN §9).

**Public-surface reminder.** This file is committed to the public repo. The in-room talk
may name the work project's component and employer — they are in the circulated internal
abstract. The committed deck says only "a legacy component at a regulated financial
institution"; on slides 2–3 and the spectrum slides, **name it verbally**. Nothing on a
slide, in the handout, or in these notes carries the name.

---

## The origin anecdote — thirty seconds, no more

> I was asked, entirely reasonably, to account for some heavy AI-credit usage. Fair
> question. But the honest answer wasn't a number — it was that the question is about
> the wrong resource. The scarce thing isn't credits, it's what the credits were being
> converted *into*, and whether any of it survived the session that produced it. This
> talk is what happened when I tried to answer that properly.

Thirty seconds gets you from the question to the thesis. It is stage-setting, not
content — do not let it grow. If someone asks about the credit question later, that is
discussion time, not arc time.

---

## Time skeleton (indicative, not a clock)

| segment | slides | ~min | can compress to |
|---|---|---|---|
| 1 · The case, cold | 2–3 | 4 | 2 (skip the yardstick detail, keep 18/24 + "credible because not top") |
| 2 · Frame + three exhibits | 4–8 | 8 | 5 (A1 alone carries the section) |
| 3 · Four practices | 9–24 | 12 | 8 (3.3 is the spine; 3.1 can be one sentence over the figure) |
| 4 · Research examined | 25–33 | 8 | 5 (negatives 1+4 spoken from one slide, corrections slide never cut) |
| 5 · Interactive + close | 34–37 | 5+ | elastic — this is the buffer |

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
| §2 (slide 8) | "how did you measure that?" body language, engineers leaning in | **M-C** (session-log deep dive) after the core arc, or a 60-second verbal version now: three log stores, 1,061 turns, hand-labelled before the classifier existed |
| §3.2 (slide 13, the probe negative) | interest in the probe design ("how do you probe confabulation?") | **M-D** — the pre-registration story plays well told as narrative: frozen by commit, 3 slots voided against my own hypothesis |
| §3.3 (slide 16, the null) | the null lands well / someone says "refreshing" | **M-B** war story 3 — one session, two defects, in the 22/24 project; it deepens the null instead of defending it |
| §3.4 (slide 23, the rework contrast) | "isn't that rework number confounded?" asked *with interest* rather than challenge | **M-E** — show the full table with the † footnotes; the honesty of the 14-day-window restriction converts skeptics |
| §4 (slide 33, the confounds ledger) | room still listening at the confounds ledger | **M-A** then **M-B** — the spectrum walk and war stories are the best listening material; **M-F** only if the room is research-minded |

### Compresses when the room engages (questions before §3, discussion catching fire)

- Compress §3.1 to one sentence over the hierarchy figure ("layers as shortest
  description first — the corpus case is a 117-file CLI that skipped half the menu and
  was right to").
- Compress the four negatives to negatives 1 and 4 spoken from the §4.3 divider, but
  **say the count**: "four honest negatives, separately — never a trend of four."
- Move the handout **earlier** — it is the best discussion fuel; the spectrum slide and
  closing question work as a discussion frame from minute 20 onward.
- Never compress: the reframe slide (5), A1 (6), the null (16), the corrections slide
  (31), the confounds ledger (33). Those five are the talk.

### The interactive segment (elastic buffer)

Hand out `handout-rubric.md` printed. Two minutes silent scoring, then two discussion
axes: *where are you on the spectrum* (slide 34) and *did Step 0 stop you — and was
that a relief?* The datacli example legitimises low scores; use it to keep the segment
from becoming confession hour. Close on the dispatch-vs-continue question regardless of
time.

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

**Slide 6 · retransmission tax.**
*Challenge: "isn't that just btest having longer sessions / pasting more?"*
Concede both: btest's sessions lengthened 9.1 → 19.8 turns, and paste bodies survive in
only 74 of 204 paste-referencing turns — which *under*-counts payload warm-ups, so the
bias runs against my finding, not with it. → exhibits A1; `data/session-metrics/warmup.json`.

**Slide 7 · dispatch-per-assent.**
*Challenge: "0.10 on what n?"*
It's on the slide: 3 dispatches against 29 "continue"s — two more found dispatches would
move it. The robust part is the volume (147 short turns, 19% of btest's typing), not the
ratio. → exhibits A4.

**Slide 16 · the pre-registered null.** *(The most likely fire.)*
*Challenge: "so your experiment disproved your own thesis."*
Concede immediately: it failed to show the substrate reduces confabulation, p = 1.0,
published as it came out — and the one confabulation is the full-substrate project's.
Then the two facts that size it: the "flat" arm carries a 212-line agent-instruction
file — enough to explain the null on its own — and the reversed direction rests on one
confabulation; the null survives any single re-scoring. The claim I am defending tonight
is the reframe (human's side of the loop), which does not rest on this experiment.
→ REPORT §3.3; exhibits C1; pre-reg commit `ab9c62d`.

**Slide 17 · "the floor has risen".**
*Challenge: "then why bother with a substrate at all?"*
Because retrieval was never the expensive part. The tax is on the human's side — re-entry
cost, delegation vs assent, findable reasons — and that is where every robust number in
this corpus sits. → REPORT §2.

**Slide 18 · Python 3.12 pair.**
*Challenge: "that's one anecdote."*
Yes — n = 1 by construction, labelled a case study on the slide, and it *follows* the
two robust results rather than carrying the claim. It is the corpus's only same-operator,
same-day, same-decision control. → exhibits D1.

**Slide 20 · survivorship.**
*Challenge: "how much of this artifact story is survivorship bias?"*
It is the most serious confound in the eval, it is correlated with the treatment, and it
was raised by the operator, not caught by an instrument. Measured across three channels,
then hand-adjudicated *down* (≥26 → ≥10; 16 false positives itemised). Two properties:
the noise is one-directional and runs with my hypothesis; and the agent-side channel
couldn't see the substrated project's own memory files at all. All counts are lower
bounds. → REPORT §4.5 confound 6; `data/survivorship-audit.json`.

**Slide 23 · the 82.2% rework contrast.**
*Challenge: "5× longer history — of course more lines died."*
Correct, and the slide says so: texture, not proof. The comparable column is the 14-day
one (32.6% vs 3.9%, an 8.4× gap), restricted to the three repos long enough to support
it. Churn is a blame-free LIFO approximation with published biases. → exhibits A3;
`data/git-metrics/`.

**Slide 19 · the tag curve.**
*Challenge: "so btest just stopped being disciplined."*
No — that's the reading the original exhibit invited and the correction withdrew. 280 of
293 tags belonged to a subproject that left the repo; July is conventionally-prefixed at
90%. The defensible claim is narrower: the *addressable* convention collapsed in April
and what replaced it is a taxonomy, not an address. → exhibits B2; war-stories §6.3.

**Slide 32 · closing altitude exhibit.**
*Challenge: "your classifier, your labels, your κ."*
One rater, so κ = 0.902 is stability, not inter-rater reliability — it's on the slide.
The labels were frozen before the classifier was written, on a pre-assigned held-out
split, and the raw (unbanded) comparison is *rejected* in this talk because it flatters
the wrong project. → exhibits A2; `rubric/ALTITUDE.md`.

**Slide 34 · the spectrum.**
*Challenge: "the rubric measures your own method — circular."*
Confound 4, named on the ledger slide: it operationalises my own method, which is why it
never appears without outcome evidence beside it, and why the corpus includes boundary
cases expected *not* to show the effect. Review moved two scores down. → exhibits E1.

**Anywhere · "what about METR?"**
Agree before defending: 19% slower while feeling 20% faster, experienced devs, mature
repos — including my own felt productivity. That result is why this evaluation measures
behaviour instead of asking me how it felt. → REPORT §4.2.

**Anywhere · "n=1, one author, one domain."**
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
  opens with its robust number, per the rules. Story 3's file:line requirement is a
  **proposal with n=1**, never a finding.
- **M-C** — for methodology skeptics. Lead with "hand-labelled 99 turns before writing
  the classifier"; the orientation-cost refusal (3.8× spread, n=2, no claim) buys more
  credibility than any positive number.
- **M-D** — for experimentalists. The voids story (15% of the instrument, every void
  against the hypothesis) is the module's spine.
- **M-E** — for git archaeologists. Keep the † footnote discipline audible: three
  projects are shorter than the churn window.
- **M-F** — only for a research-minded room. Be plain that κ was not attempted and no
  kernel numbers exist.

---

## Dry-run checklist (branch points, not script)

- [ ] Origin anecdote lands in ≤30 seconds (time it).
- [ ] Each of the five never-cut slides (5, 6, 16, 31, 33) can be delivered from memory.
- [ ] Practise the §3.3 sequence twice — robust → robust → null → concession → case
      study is the talk's hardest transition and its whole credibility.
- [ ] Practise *both* §4 lengths: full four-negative version and the compressed
      two-negative version.
- [ ] Rehearse the three likeliest challenges out loud: the null, the rework confound,
      the survivorship correction.
- [ ] Verify the room copy of the deck renders (Marp) and the handout is printed.
- [ ] Decide before walking in: which module you *want* to give if the room listens
      (recommendation: M-B — the stories carry the caveats naturally).
