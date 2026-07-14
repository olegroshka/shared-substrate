# Shared Substrate

**A discipline for sustained human–AI coupling on complex problems.**

> For complex work that spans many sessions, many decisions, and many abstraction layers, **the substrate matters at least as much as the model** — the substrate being the externalised state any sustained reasoning, organic or artificial, must traverse.

📄 **[Read the paper (PDF)](paper/shared_substrate.pdf)** — draft v0.2, July 2026 · [LaTeX source](paper/shared_substrate.tex)

---

## What this is

Modern AI agents have characteristic limitations on long-horizon work: bounded context windows, drift across iterations, phantom decisions, reference rot, lost intent, and the cost of restarting cold every session. These are not model failures that scaling will dissolve — they are **substrate failures**, and they respond to substrate-level interventions far more reliably than to model-level scaling.

**Shared Substrate** names a discipline of forming, maintaining, and cascading hierarchical external representations across the full trajectory of a project — practised by the author across many domains and years, made explicit by the demands of multi-session AI collaboration. It is domain-agnostic: software engineering appears in the paper only as the worked instance. The same discipline applies to a research programme, a design, a strategy — anything manifestable.

## The idea in five images

1. **The pinned centroid.** The participants in sustained work — the human operator, AI agents, successive model generations, colleagues — are noisy point masses. The substrate is the deliberately *pinned centre of mass* of that ensemble: session drift is excursion, warm-up is reversion, and a model swap moves a point mass without moving the centroid.

2. **Compressed source.** Layered by abstraction, the substrate is a *compressed representation* of the thing being manifested; agentic pipelines are its decompressor. Only what no pipeline can re-derive — the choices, the intent, the taste — must be stored. The append-only Decision Records are the incompressible kernel. Drift is decoder error; a phantom decision is the decoder inventing source bits; restart cost is retransmission.

3. **A language and an oracle at every layer.** Each abstraction layer pairs a representation formalism with the strongest available verification oracle — executable behavioural contracts at the top, schemas and contract tests in the middle, measurable non-functional envelopes at the bottom. The user is the one oracle only the user can be; everything below that gets a mechanical one.

4. **Observability closes the loop.** An oracle the agent cannot query is not a guardrail; it is an audit. Amplification is indifferent to sign: run open-loop, an agent amplifies divergence at the same gain it amplifies progress — a proposed mechanism for the measured cases where AI assistance made experienced practitioners *slower*. The work's state must be observable *to the agent*, so excursions are detected and capped while correction is still cheap.

5. **Human-governed, agent-executed.** The discipline's execution is progressively delegated to agents through a five-layer adoption stack — warm-up, integrity watchdog, in-situ decision capture, auto-drafted handoffs, graph-native substrate. What never delegates: intent, decision approval, scope, voice.

**The discipline's purpose in one line: separate genuine human creative input from cognitive load.** The human deposits the bits no pipeline can derive — once, at the layer where they belong. Everything derivable is carried by the substrate and executed by the pipeline, with oracles bounding the distortion of the expansion.

## Why now

The empirical record on AI-assisted work is genuinely contested: a rigorous RCT found experienced developers **19% slower** with AI tools on mature codebases (while believing they were 20% faster); large field experiments found **+26%** task completion; greenfield studies found **+56%**. The moderators that reconcile these results — task abstraction level, project maturity, operator experience — are precisely substrate-adjacent variables. The discipline is an intervention on those moderators, and the claim is falsifiable.

## Repository layout

```
shared-substrate/
├── paper/
│   ├── shared_substrate.tex     # canonical draft (v0.2) — LaTeX source
│   ├── shared_substrate.pdf     # built PDF
│   ├── references.bib           # bibliography (entries verified against arXiv)
│   ├── README.md                # build instructions
│   └── archive/                 # v0.1 draft (Cognitive Cartography), frozen
├── method/
│   ├── field-manual.md          # the practitioner's compact field manual
│   └── amendments-log.md        # historical amendment record from the origin project
├── research/
│   └── human-ai-centroid-research.md   # literature survey grounding the paper
├── CITATION.cff
└── LICENSE                      # CC BY 4.0
```

## The discipline at a glance

- **Six artefact categories** partition all project knowledge: Knowledge Bases, Inventories, Data Dictionaries, Decision Records (append-only), Open Questions, Glossary.
- **Stable identifiers** (`KB-N`, `ADR-N`, `OQ-N`, …) for every cross-reference — never file paths, never paraphrases. Identifiers survive reorganisation; paraphrases rot.
- **A status lifecycle** — `MISSING → DRAFT → STABLE → STALE → DEPRECATED` — with explicit, triggered transitions.
- **An edit protocol** with an impact check, single-source-of-truth enforcement, and a generously sized trivial-fix lane so ceremony never exceeds benefit.
- **Forward and reverse propagation** across an explicit hierarchy of abstraction layers; reverse propagation always passes through a Decision Record.
- **A session protocol** — warm-up (revert to the substrate), work (edit by protocol), handoff (deposit back) — identical whether the previous session ended cleanly or crashed.

See the [field manual](method/field-manual.md) for the printable version, or §4 of the paper for the full specification.

## Building the paper

Requires a standard TeX Live installation (`tikz`, `booktabs`, `natbib`, `hyperref`, …).

```bash
cd paper
latexmk -pdf shared_substrate
```

## Status and roadmap

**Draft v0.2** — a self-contained articulation of the method and its grounding, suitable for reading and discussion. Not yet submitted anywhere.

The research programme it opens, deliberately flagged in the paper as future work rather than developed there:

- a rate–distortion treatment of the human↔agent specification channel (rate = specification effort; distortion = residual intent misalignment);
- formal per-layer representation optimality (description length × macro-expressibility × distortion);
- measurable non-functional contracts as first-class, layer-attached specifications;
- pre-registered empirical tests against the contested productivity baselines.

## Provenance

The discipline documented here was not invented for the paper. It is the articulation of a practice cultivated by the author over years across many domains; collaboration with current-generation AI agents is what made its elements demand explicit naming. AI assistance in *writing* the paper is acknowledged in the paper's Acknowledgements — a collaboration conducted, fittingly, in the discipline the paper describes.

## Citing

See [CITATION.cff](CITATION.cff), or:

```bibtex
@misc{roshka2026sharedsubstrate,
  author = {Roshka, Oleg},
  title  = {Shared Substrate: A Discipline for Sustained Human--AI Coupling on Complex Problems},
  year   = {2026},
  note   = {Draft v0.2},
  url    = {https://github.com/olegroshka/shared-substrate}
}
```

## License

[CC BY 4.0](LICENSE) — share and adapt with attribution.
