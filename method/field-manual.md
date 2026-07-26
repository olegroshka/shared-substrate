# The Compact Field Manual

The Shared Substrate discipline in a form you can print and pin. This is the
paper's Appendix A as a standalone reference; see
[the paper](../paper/shared_substrate.pdf) §4 for the full specification and
the rationale behind every rule.

**This manual describes the discipline in full — you are not expected to adopt
it in full.** The elements are separable and each pays back on its own (the
paper's synthesis table doubles as the adoption menu). Start with whatever
targets your worst failure mode; stable identifiers are the only
near-universal prerequisite. Nothing here is all-or-nothing.

## Frontmatter (every artefact)

```yaml
---
id: KB-NNN | INV-NNN | DD-NNN | ADR-NNN | OQ-NNN
title: human-readable title
status: MISSING | DRAFT | STABLE | STALE | DEPRECATED
owner: Name | shared
last_reviewed: YYYY-MM-DD
version: 0.1
sources: [URLs with date accessed]
depends_on: [ID, ID, ...]
referenced_by: [ID, ID, ...]
---
```

## The six artefact categories

| Category | Holds | Cadence |
|---|---|---|
| **Knowledge Bases** (KB-N) | durable, slow-changing facts about the world the project operates in | changes rarely |
| **Inventories** (INV-N) | exhaustive, machine-checkable lists in well-defined categories | changes per feature |
| **Data Dictionaries** (DD-N) | schemas: every field, type, invariant, example — the contract between components | changes per interface |
| **Decision Records** (ADR-N) | one decision each: context, decision, alternatives, consequences | append-only |
| **Open Questions** (OQ-N) | deliberately unresolved questions with target dates and resolution criteria | accumulate and resolve |
| **Glossary** | the singular authority on terminology | grows and stabilises |

Every piece of project knowledge belongs to exactly one category. Every fact
has one home; everywhere else cites it by stable identifier.

## Edit protocol (every non-trivial change)

1. READ the inventory; locate the artefact.
2. READ its frontmatter.
3. IDENTIFY the SSOT for the fact you intend to change.
4. IMPACT-CHECK by walking `referenced_by`.
5. Decide the lane: trivial / normal / decision-bearing.
6. Edit; cite by stable identifier; do not restate.
7. Bump `last_reviewed`; bump `version` if substantive.
8. Update inventory if status changed.
9. Log decision as ADR if applicable.
10. Log question as OQ if applicable.
11. Commit; commit message lists every artefact touched, by ID.

### Trivial-fix lane

For typos, formatting, broken links that do not change meaning: skip steps 4,
9, 10. Still bump `last_reviewed`. **If unsure whether a fix is trivial, it
isn't; use the full lane.**

## Status transitions

- `MISSING → DRAFT` — first content commit.
- `DRAFT → STABLE` — owner review; complete; no TODOs.
- `STABLE → STALE` — `last_reviewed` older than current milestone freeze, or an upstream artefact changed.
- `STALE → STABLE` — re-review.
- any → `DEPRECATED` — superseded.

## Anti-patterns (do not)

1. Edit `STABLE` without bumping `last_reviewed`.
2. Paste the same content in two artefacts.
3. Decide in conversation without an ADR.
4. Create an artefact without an inventory row.
5. Quote another artefact's prose verbatim.
6. Let OQs accumulate without target dates.
7. Mix levels of abstraction in one artefact.
8. Defer propagation ("I'll update the tests later").
9. Edit a past ADR's body.
10. Bypass SSOT "just for clarity".

## Session protocol

- **Warm-up.** Read inventory; read protocol TL;DR; read the task's artefacts;
  spawn supplementary reads. *Static L0:* keep a project-root bootstrap file —
  a governed **pointer** to the canonical artefacts, never a restatement — so
  any agent harness auto-loads the warm-up entry point.
- **Work.** Apply the edit protocol; cite by ID; track multi-artefact edits as
  a unit.
- **Handoff.** Every edit committed; every new artefact has frontmatter and an
  inventory row; decisions in ADRs; questions in OQs; metadata current; the
  inventory's priority queue reflects the new state.

## Adoption stack (delegate in this order)

1. **L0 — warm-up:** bootstrap pointer file; agent reads the task's `depends_on` closure.
2. **L1 — watchdog:** links, inventory, frontmatter schema, staleness auto-degrade, orphans.
3. **L2 — decision capture:** agent drafts ADRs at the moment of decision; human approves.
4. **L3 — retros and handoffs:** drafted from observable state; human edits.
5. **L4 — graph-native substrate:** markdown artefacts as rendered views over a knowledge graph.

**Human surface that never delegates: intent, decision approval, scope, voice.**
