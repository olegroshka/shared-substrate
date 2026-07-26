# Does the substrate matter — for *your* project?

*One page. Two minutes. Honest answers. Derived from the full instrument at
`research/eval/rubric/RUBRIC.md` — [github.com/olegroshka/shared-substrate](https://github.com/olegroshka/shared-substrate).*

---

## Step 0 — the complexity check (do this first)

Count roughly: **sessions or people involved · months of life · decisions that could be
silently reversed · external systems integrated.**

If everything is small — days of work, one person, few decisions — **stop here: flat
notes are the right tool.** The discipline predicts its own irrelevance below a
complexity threshold; a low score on a simple project is *correct practice*, not a
deficiency. "Score low and simple" is a fine place to be.

---

## Step 1 — score 0–3 per question

**0** absent · **1** in someone's head · **2** written but partial · **3** maintained and
load-bearing (the project would notice its absence)

| # | Practice | Question | 0–3 |
|---|----------|----------|-----|
| 1 | Decomposition | Are intent, requirements, design, and code in *separate* artifacts that update in a known order? | |
| 2 | Decomposition | Does work move through gates with checkable exit criteria? | |
| 3 | Guardrails | Is intended behaviour executable — tests/contracts that fail when meaning drifts — with performance budgets written down? | |
| 4 | Guardrails | Are there rules for changing shared docs — and a cheap lane for trivial fixes? | |
| 5 | Representation | Could you answer "did we decide X, and why?" from an append-only record with stable IDs — not from memory or chat scrollback? | |
| 6 | Representation | Is there one authoritative list/schema/glossary per kind of fact, with a freshness status? | |
| 7 | Validation | Does every level have a check stronger than "looks right," running continuously? | |
| 8 | Validation | Can your AI assistant *itself* check the state of the work — and does each session start from a written warm-up instead of your re-explanation? | |

Score from artifacts and history, not from intention or memory — an answer with no
citable evidence scores at most 1.

---

## Step 2 — read your total /24

- **0–6 · unsubstrated** — expect drift, phantom decisions, and Monday restart cost *in
  proportion to complexity*. (If Step 0 said "simple," this is fine.)
- **7–14 · partial** — you likely already feel where it leaks. Adopt the **one** missing
  element that hurts most; each pays back alone.
- **15–24 · substrated** — your bottleneck is elsewhere: intent quality and oracle
  capacity.

Tonight's corpus, on the same scale: 22 · 20 · 18 (provisional) · 17 · 16 · 15 · 12 · 7.
The 17 is a small CLI that deliberately skipped half the menu — and was right to.

---

## The question the evidence earned

*Where does your attention go in AI sessions — declaring intent and making decisions, or
pasting errors and re-explaining context?*

**When you type a short message to your agent — is it a dispatch, or a "continue"?**
