# NEXT_TASK — post-talk brief (no session scheduled)

**S9 closed the pre-talk work.** The deck, handout and speaker notes are in
`talks/does-the-substrate-matter/`; the report and bench are frozen; the word-count
discrepancy is reconciled (STATE.md S9 findings). **The talk itself (Thursday
2026-07-30) needs no session** — what remains before it is Oleg's, not a model's:

- run the **live branch-point rehearsal** (checklist at the end of
  `talks/does-the-substrate-matter/NOTES.md`; the branch-point map is the thing to
  rehearse, not a script);
- print `handout-rubric.md`;
- decide which module to *prefer* if the room listens (NOTES recommends M-B);
- remember the two "name verbally" points — the committed deck is scrubbed.

**If the rehearsal surfaces deck rework**, it is self-serve or a short session: edit
`slides.md`, keep the binding rules (caveat on the same slide; titles held to
`report/exhibits.md`'s captions; nothing fragile leads; no two fragile findings
aggregated), and re-check `NOTES.md`'s slide numbers afterwards — they reference the
current slide order. Where a slide and exhibits.md disagree, the bench wins.

---

## The next real work: the P8 work-side leg (PLAN §5 round-trip)

This is the first piece of eval work that happens **after** the talk, and it happens
**inside the org**, not on this machine. The design is already written — PLAN §5; this
brief is just the operational order.

**Outbound.** `research/eval/` is the portable kit and the *only* thing that crosses:
PLAN, METHODS, STATE, ASSESSMENT, rubric/ (incl. ALTITUDE.md), probes/ (frozen),
scripts/ (stdlib-only, git-only, path-parameterised), report/. **`talks/` does not
cross** and nothing in it may be required reading for the in-org leg.

**In-org run, in rough order of value per hour:**

1. **Re-score the P8 rubric row from artifacts** (currently 18/24
   PROVISIONAL-INFERRED). The A5 cell (decision records) is the matrix's
   lowest-confidence call — settle it from the real increment plan and any decision
   log first. Evidence citations per axis, same as the local corpus.
2. **`scripts/git_miner.py` + `scripts/complexity_profile.py`** on P8's repo — the
   cheap, deterministic half of the evidence. Read every number against the complexity
   profile, as at home.
3. **The probe protocol** (`probes/PROTOCOL.md`) under Copilot CLI — the cross-tool
   replication WS4 was designed for. The question set must be authored in-org against
   P8's actual ground truth (the frozen local sets are corpus-specific; the *protocol*
   is what replicates, including pre-registration by commit before any run).
4. **`scripts/log_miner.py` + the altitude instrument** on Copilot CLI logs, if the
   org's retention has kept them.

**Inbound.** Cleared aggregates only — counts, ratios, curves; no code, no paths, no
identifiers, no business terms; clearance per employer policy before anything is
pushed. They land as: the P8 rubric row moving PROVISIONAL → scored, and P8 columns
beside the existing exhibits in REPORT/exhibits (each keeping its caveat). The public
surface stays "a legacy component at a regulated financial institution".

---

## Carried items (unchanged priority: none block the talk)

1. **`artifact_survivorship.py`'s five recorded fixes** have never been run
   (`data/survivorship-audit.json` → `recommended_fixes_for_any_future_run`). Worth
   doing only if the eval continues past the talk; if the in-org leg uses the
   survivorship instrument, apply them **first** there.
2. **War story 3's cheap testable hypothesis** — audit-produced records carry the
   `file:line` each factual claim was read from (n=1, a proposal). Now public in deck
   module M-B, stated as a proposal. If the eval continues: it is the cheapest real
   experiment on the deposit-time-check gap, in either arm.
3. **The "shorter" sentence in the paper** was dropped in S9 because v0.1 was never
   captured. If Oleg's memory says v0.1 was in fact ~6k words and shrank in the v0.2
   pass, the sentence can be restored *with that provenance stated* (operator
   recollection, artifact unrecoverable). Otherwise leave as is.
4. **Post-talk deposit:** whatever the room actually did — which branch points fired,
   which module ran, which challenges came — is WS-grade evidence about the talk's own
   design. A paragraph in STATE.md's session log is enough; write it while it's warm.

**Constraints (standing):** console output ASCII-only (Windows cp1252); Python 3.11 via
`python`; never modify the corpus repos; author judgment stays in published input files;
public-surface rule on everything committed here.

---

**Nothing is pending on Oleg for the eval.** For the talk: the rehearsal, the printout,
and the module preference — all his, all before Thursday.
