# Paper sources

- `shared_substrate.tex` — **canonical draft (v0.2)**: *Shared Substrate: A
  Discipline for Sustained Human–AI Coupling on Complex Problems*.
- `shared_substrate.pdf` — built PDF of the canonical draft.
- `references.bib` — bibliography. All post-2023 arXiv entries were verified
  against live arXiv metadata (titles, authors, ids) on 2026-07-14.
- `archive/` — the frozen v0.1 draft (*Cognitive Cartography*, April 2026),
  preserved verbatim as a historical artefact. v0.2 supersedes it; per the
  discipline itself, superseded records are kept, not edited.

## Build

```bash
latexmk -pdf shared_substrate
```

Or manually:

```bash
pdflatex shared_substrate
bibtex shared_substrate
pdflatex shared_substrate
pdflatex shared_substrate
```

Required packages (all in a standard full TeX Live install): `lmodern`,
`geometry`, `microtype`, `tikz` (libraries: `positioning`, `arrows.meta`,
`shapes.geometric`, `decorations.pathreplacing`, `calc`, `fit`, `backgrounds`,
`matrix`, `shapes.misc`), `booktabs`, `caption`, `natbib`, `xcolor`,
`enumitem`, `hyperref`.

## Figures and tables (all TikZ / booktabs, inline in the source)

| Label | Content |
|-------|---------|
| `fig:centroid` | the pinned centroid of the human–AI ensemble |
| `fig:drift` | drift spectrum: intent fidelity with and without substrate |
| `fig:hierarchy` | hierarchy of abstraction layers; forward/reverse propagation |
| `fig:atlas` | the artefact graph, glossary as semantic anchor |
| `fig:status` | artefact status lifecycle |
| `fig:editproto` | edit protocol with trivial-fix lane |
| `tab:oracles` | layer → representation formalism / oracle / guardrail |
| `fig:loop` | observability control loop; open- vs closed-loop divergence |
| `fig:projection` | substrate as compressed source; creative kernel in, expansion out |
| `tab:synthesis` | discipline element ↔ cognitive principle ↔ failure mode ↔ executed-by |
| `fig:session` | session lifecycle: warm-up → work → handoff |
| `fig:stack` | five-layer adoption stack |
| `fig:system` | system panorama: nested fast/slow loops over the evolving substrate |
