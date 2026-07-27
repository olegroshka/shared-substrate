# Talk outline — working document

**Source of truth for the talk shape:** `research/eval/PLAN.md` §9 (core arc + expansion
modules M-A…M-F, no hard timeboxes; the room sets the length). This file tracks the concrete
slide-level realisation of that shape and evolves independently as the deck is built.

## Materials to borrow

- `docs/presentation.md` — the *general method* walkthrough (a different presentation; borrow
  selectively, do not merge): the failure-modes framing, the aphorism slides, the adoption
  menu.
- `assets/fig-*.png` — rendered figures reusable as-is: `fig-centroid` (the frame slide),
  `fig-divergence` + `fig-loop` (guardrails/validation), `fig-hierarchy` (decomposition),
  `fig-projection` (system representation / compression), `fig-system` (closing panorama).
- `docs/management-brief.md` — phrasing for the non-engineer slice of the audience.
- `research/eval/report/` — the evidence exhibits (rubric spectrum, altitude distribution,
  probe result, survival curve) + the appendix bench, delivered by WS1–WS6.

## Deliverables in this folder

- `slides.md` — the deck (Marp-compatible, like `docs/presentation.md`)
- `handout-rubric.md` — one-page audience handout ("score your own project on the four
  practices"), derived from `research/eval/rubric/RUBRIC.md`
- `assets/` — talk-specific figure exports (exhibit bench renders)
- `NOTES.md` — speaker notes incl. the branch-point map (what expands when the room listens,
  what compresses when it engages)

## Status

- [x] Scaffold created
- [x] Exhibits delivered from eval workstreams (WS1–WS6 → `research/eval/report/exhibits.md`, 23 exhibits)
- [x] slides.md — the deck (S9, iterated with Oleg): core arc of 46 slides — §2 opens
      with the paper's frame (era claim vs Google's New-SDLC quote · creative input vs
      cognitive load · the inversion · historical precedents · the personal evolving
      substrate) then mirrors REPORT §§1–5; §4 carries the deck-building miss as the
      evaluation's third self-correction; §5 ends with the practical adoption menu.
      Passes applied: self-sufficiency, guided-interpretation style, shared-not-lectured
      voice, setting-neutral wording, name/date scrub. (The first draft was kept as
      slides-v2.md's sibling during iteration and removed 2026-07-27; history in git.)
- [x] Expansion-module slides drafted (M-A…M-F behind an explicit divider)
- [x] Handout finalised (`handout-rubric.md`, incl. the Step-0 complexity check)
- [x] Deck-side dry run: caption/caveat audit of every number slide against the exhibit
      bench (one bench caption error found and fixed, see STATE.md S9 findings)
- [ ] Live branch-point rehearsal (Oleg, before the talk — checklist at the end of
      `NOTES.md`)

Figures: the deck reuses `assets/fig-*.png` from the repo root (relative paths); no
talk-specific figure exports were needed, so `assets/` here stays empty. Numbers appear
as tables with denominators on-slide rather than as rendered charts — the caveat has to
sit next to the number, and a chart is where caveats get dropped.
