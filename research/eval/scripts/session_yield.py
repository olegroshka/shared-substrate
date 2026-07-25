#!/usr/bin/env python3
"""WS3(c): operator volume against durable yield (supporting analysis).

For each project, put what the human SPENT (sessions, turns, typed characters)
next to what the repository RETAINED over the same window (commits, added source
lines, net source lines), and report the ratios. This is the V/I-style
calibration the paper asks for: felt productivity is untrustworthy (METR), so
volume is only meaningful against something durable.

Stdlib-only, read-only on the repos (`git --no-optional-locks`).

Window alignment is the whole methodological point: session logs start
2026-03-03, several repos start earlier, and one (btest) has 78 commits before
any log exists. Every ratio is therefore computed over the OVERLAP of the log
window and the commit window, and both bounds are published with the number.

Usage:
  python session_yield.py --turns ../data/session-metrics/turns.json \
      --repo btest=C:/Users/olegr/PycharmProjects/btest ... \
      --out ../data/session-metrics/yield.json
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_common import eprint, git_version, is_source, read_log  # noqa: E402

VERSION = "1.0"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--turns", type=Path, required=True)
    ap.add_argument("--repo", action="append", default=[],
                    type=lambda s: s.split("=", 1))
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    turns = json.load(open(args.turns, encoding="utf-8"))["turns"]
    by_proj = defaultdict(list)
    for t in turns:
        if (t["kind"] == "prompt" and t["verbatim"] and not t["off_project"]
                and t["source"] in ("claude_history", "copilot_jb")):
            by_proj[t["project"]].append(t)

    results = {}
    for name, path in args.repo:
        sel = by_proj.get(name, [])
        if not sel:
            eprint("no turns for %s" % name)
            continue
        ts = sorted(t["ts"] for t in sel if t["ts"])
        log_from, log_to = ts[0][:10], ts[-1][:10]
        try:
            commits = read_log(Path(path))
        except Exception as exc:
            eprint("git failed for %s: %s" % (name, exc))
            continue
        if not commits:
            continue
        git_from, git_to = commits[0].iso[:10], commits[-1].iso[:10]
        lo, hi = max(log_from, git_from), min(log_to, git_to)

        if lo > hi:
            results[name] = {"windows": {"log": [log_from, log_to],
                                         "git": [git_from, git_to],
                                         "overlap": None},
                             "note": "log window and commit window do not "
                                     "overlap - no ratio is computable"}
            continue

        inwin = [c for c in commits if lo <= c.iso[:10] <= hi]
        added = deleted = 0
        nb_added = nb_deleted = 0          # .ipynb: JSON with embedded outputs,
        for c in inwin:                    # where one commit can be 151k "lines"
            for a, d, _old, new in c.files:
                if not is_source(new):
                    continue
                added += a or 0
                deleted += d or 0
                if new.lower().endswith(".ipynb"):
                    nb_added += a or 0
                    nb_deleted += d or 0
        sessions = len({t["session_id"] for t in sel})
        wsel = [t for t in sel if t["ts"] and lo <= t["ts"][:10] <= hi]
        wturns = len(wsel)
        wchars = sum(t["chars"] + t["paste_chars"] for t in wsel)
        net = added - deleted
        ratio = lambda a, b: round(a / b, 2) if b else None

        results[name] = {
            "windows": {
                "log": [log_from, log_to],
                "git": [git_from, git_to],
                "overlap": [lo, hi],
                "commits_before_any_log": sum(1 for c in commits
                                              if c.iso[:10] < log_from),
                "note": "all ratios below are computed over the overlap window",
            },
            "spent": {
                "sessions_all_time": sessions,
                "turns_in_window": wturns,
                "typed_plus_pasted_chars_in_window": wchars,
                "turns_all_time": len(sel),
            },
            "retained": {
                "commits_in_window": len(inwin),
                "source_lines_added": added,
                "source_lines_deleted": deleted,
                "net_source_lines": net,
                "notebook_lines_added": nb_added,
                "notebook_lines_deleted": nb_deleted,
                "source_lines_added_ex_notebooks": added - nb_added,
                "net_source_lines_ex_notebooks": net - (nb_added - nb_deleted),
                "largest_net_deletion_commits": [
                    {"date": c.iso[:10], "subject": c.subject[:80],
                     "net_deleted": nd}
                    for nd, c in sorted(
                        ((sum(d or 0 for a, d, _o, n in c.files if is_source(n))
                          - sum(a or 0 for a, d, _o, n in c.files if is_source(n)),
                          c) for c in inwin),
                        key=lambda t: -t[0])[:3] if nd > 0],
            },
            "ratios": {
                "turns_per_commit": ratio(wturns, len(inwin)),
                "chars_per_commit": ratio(wchars, len(inwin)),
                "net_lines_per_turn": ratio(net, wturns),
                "chars_per_net_line": ratio(wchars, net) if net > 0 else None,
                "added_lines_per_turn": ratio(added, wturns),
                "retention": round(net / added, 4) if added else None,
                "retention_ex_notebooks": (
                    round((net - (nb_added - nb_deleted)) / (added - nb_added), 4)
                    if added - nb_added else None),
            },
        }

    meta = {
        "script": "session_yield.py",
        "version": VERSION,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_version": git_version(),
        "definitions": {
            "retained": "computed on SOURCE files only (corpus_common.is_source), "
                        "non-merge commits, inside the overlap window",
            "net_source_lines": "added minus deleted in the window - a transparent "
                                "retention proxy, NOT the LIFO survival "
                                "reconstruction WS2 uses; the two answer different "
                                "questions and are not interchangeable",
            "turns_per_commit": "operator turns spent per commit that landed",
        },
        "verdict": (
            "INCONCLUSIVE, and reported as such. Turns per landed commit sits in "
            "a narrow 1.6-2.9 band across the four projects large enough to "
            "measure and does not separate the substrate postures. Line-based "
            "yield is not usable in this corpus at all: a single btest notebook "
            "commit adds 151,591 'source lines', and btest's negative net over "
            "the window is produced by two deliberate extractions (SMIM, datacli) "
            "plus a research/ tree removal, not by waste. WS3(c) is the analysis "
            "PLAN 8 lists first in the cut order; this is why."
        ),
        "caveats": [
            "Copilot-era volume is under-counted: b-autobot's Copilot logs are "
            "lost entirely and btest's surviving Copilot store is mostly "
            "machine-composed briefs, so btest's turn count is a LOWER bound and "
            "its turns_per_commit is therefore flattering to btest - the "
            "direction is conservative against this research's own argument.",
            "A commit is not a unit of value and a line is not a unit of work. "
            "These ratios are texture (PLAN 7), and they are dominated by project "
            "nature: a paper repo retains prose, a trading engine retains little.",
            "smim's history is a single squashed commit, so every line in its "
            "window is 'added' once and nothing can be seen to have been reworked.",
            "datacli and harp ratios are attribution artefacts, not measurements: "
            "both were built inside ANOTHER project's folder (datacli during July "
            "btest sessions, harp during April btest sessions) before their own "
            "session history existed, so their turn counts are far too low against "
            "their commit counts. Do not read 0.15 turns/commit as efficiency.",
            "Notebook (.ipynb) deltas are reported separately because they are "
            "JSON with embedded outputs: one btest commit adds 151,591 lines.",
        ],
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump({"_meta": meta, "projects": results}, fh, indent=2)

    print("%-11s %8s %7s %8s %9s %9s %9s" % (
        "project", "turns", "cmts", "trn/cmt", "add-exNB", "net-exNB", "retain"))
    print("-" * 68)
    usable = {k: v for k, v in results.items() if "spent" in v}
    for n, r in sorted(usable.items(),
                       key=lambda kv: -(kv[1]["spent"]["turns_in_window"])):
        print("%-11s %8d %7d %8s %9d %9d %9s" % (
            n, r["spent"]["turns_in_window"], r["retained"]["commits_in_window"],
            r["ratios"]["turns_per_commit"],
            r["retained"]["source_lines_added_ex_notebooks"],
            r["retained"]["net_source_lines_ex_notebooks"],
            r["ratios"]["retention_ex_notebooks"]))
    for n, r in results.items():
        if "spent" not in r:
            print("%-11s %s" % (n, r.get("note", "")))
    print("\nwrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
