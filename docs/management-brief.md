# Shared Substrate — Executive Brief

*What it is, why it pays, and how to measure it. One page, for decision-makers. The full method: [paper (PDF)](../paper/shared_substrate.pdf) · [overview](../README.md) · [field manual](../method/field-manual.md).*

---

## The problem: AI volume is not output

Teams adopting AI assistants report feeling dramatically faster. The best-controlled study to date measured the opposite: experienced developers were **19% slower** with AI tools on the systems they knew best — *while believing, even afterwards, that they had been 20% faster*. Other settings show genuine gains: **+26%** in large field experiments, **+56%** on green-field work.

Both findings are true. The outcome depends on how the human–AI work is **configured**, not on the tools alone. And the calibration failure is the management problem: self-reported AI productivity is systematically unreliable, so this cannot be managed by asking teams how it's going — or by counting how much gets produced.

## Why it happens: AI is an amplifier

AI multiplies whatever it is fed — including misunderstanding. Run without controls, it produces plausible volume that quietly diverges from what was intended. The cost surfaces later, as rework, and the rework regularly exceeds the time generation saved. That is the slowdown regime, and it is invisible on volume-based dashboards precisely because volume is what the amplifier inflates.

<p align="center"><img src="../assets/fig-divergence.png" width="440" alt="Open loop: divergence from intent grows past budget. Closed loop: each check clips the divergence early and keeps it capped."></p>

Run **with** controls, every check catches divergence while it is small, and correction stays cheap. Same tools, same people — opposite economics.

## The method, as three controls

1. **A durable project memory.** Decisions, definitions, requirements, and open questions live in a governed, versioned record — not in chat histories and not in people's heads. Every working session starts from it and deposits back into it. New hires, new AI models, new quarters: the memory persists, and nothing of consequence is re-explained or silently forgotten. (It is also, incidentally, the audit trail your risk and compliance functions wish you had.)

2. **Checks at every level, visible to the machine.** Business behaviour, designs, implementations, and performance budgets each get explicit acceptance criteria — and the AI can run the checks itself *while working*, so errors are caught at the moment they're cheapest. This includes non-functional budgets (latency, memory, cost): in replacement projects, the incumbent system's measured behaviour becomes the acceptance bar the new build must meet continuously.

3. **A clean division of labour.** People do what only people can: set intent, make the decisions, approve the record. Machines do the expansion, the bookkeeping, and the checking. Senior attention — your scarcest, most expensive input — is spent on judgment, not on re-establishing context.

## Productivity, measured honestly

Stop counting volume; the amplifier inflates volume whether it is right or wrong. The method makes five better numbers available as a by-product of how the work is run — no surveys, no self-reporting:

| Metric | The question it answers |
|---|---|
| **Validated output** | How much work passed its acceptance checks? |
| **Durability** | Is it still in use weeks later — or was it quietly redone? |
| **Rework liability** | How much unchecked AI output are we sitting on? (Book it as a liability, not an asset.) |
| **Context-restart cost** | How long until a session — or a new joiner — is productive? This trend should stay *flat* as the project grows. |
| **Calibration gap** | How far does felt progress diverge from validated progress? |

**Productivity = validated, durable output, net of rework liability, per senior-hour spent.** When that number and the team's felt speed disagree, believe the number — the one controlled trial we have says the feeling lies.

## Cost and payback

The method costs more in the first week or two: the project memory must be set up, and acceptance criteria must be written down. Payback typically begins within a handful of working sessions and compounds with project size and team churn. The comparison to hold in mind: **this method's costs are front-loaded and visible; unmanaged AI's costs are back-loaded and hidden** — they arrive as rework, missed budgets, and decisions nobody can reconstruct.

Adoption is also **incremental by design** — the controls pay back independently, so a team can start with the two or three that target its worst pain: a decision log alone eliminates "did we decide this?"; a project-memory entry point alone eliminates the Monday re-explaining tax; acceptance contracts on the single scariest component alone de-risk the work everyone avoids. Full adoption is the limit, not the entry fee.

## The ask

A pilot: one team, one meaningful project, six to eight weeks, with the five metrics instrumented from day one. The success criterion is falsifiable, and we state it in advance: the pilot exits the slowdown regime — validated throughput up, rework liability trending down, context-restart cost flat. If the dashboard says otherwise, the method has failed on its own terms and we say so.
