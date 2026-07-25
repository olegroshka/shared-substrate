#!/usr/bin/env python3
"""WS3(a) helper: draw the hand-labelling sample, deterministically.

Systematic (every k-th) sampling inside per-project strata over turns sorted by
timestamp: reproducible without an RNG seed, and it cannot miss an era the way
a small random draw can. The dev/held-out split is positional (3 of every 5 to
dev), so both halves span the same projects and months - the held-out half is
what makes the reported agreement mean anything, since the rules are written
while reading the dev half only.

Usage:
  python sample_turns.py --turns ../data/session-metrics/turns.json \
      --fulltext ../data/session-metrics/local/turns-fulltext.jsonl \
      --quota btest=40 blive=20 b-autobot=15 seamQ=12 harp=5 datacli=5 smim=2 \
      --out ../data/session-metrics/local/sample-to-label.txt \
      --manifest ../data/session-metrics/altitude-sample.json
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_common import norm_ws  # noqa: E402

TEXT_LIMIT = 700


def eligible(t):
    """Classifiable operator turns: typed prose, on-project, not a slash command,
    not a machine-composed Copilot brief."""
    return (t["kind"] == "prompt" and t["verbatim"] and not t["off_project"]
            and t["source"] in ("claude_history", "copilot_jb"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--turns", type=Path, required=True)
    ap.add_argument("--fulltext", type=Path, required=True)
    ap.add_argument("--quota", nargs="+", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    args = ap.parse_args()

    quota = dict((k, int(v)) for k, v in (q.split("=") for q in args.quota))
    turns = json.load(open(args.turns, encoding="utf-8"))["turns"]
    full = {}
    for line in open(args.fulltext, encoding="utf-8"):
        o = json.loads(line)
        full[o["turn_id"]] = (o["text"], o["paste"])

    picked = []
    for proj, n in quota.items():
        pool = sorted([t for t in turns if t["project"] == proj and eligible(t)],
                      key=lambda t: (t["ts"] or "", t["turn_id"]))
        if not pool:
            continue
        n = min(n, len(pool))
        step = len(pool) / float(n)
        idx = sorted({int(i * step) for i in range(n)})
        for rank, i in enumerate(idx):
            t = dict(pool[i])
            t["_split"] = "dev" if rank % 5 < 3 else "held_out"
            t["_pool_size"] = len(pool)
            picked.append(t)

    picked.sort(key=lambda t: (t["project"], t["ts"] or ""))

    lines = []
    for i, t in enumerate(picked, 1):
        text, paste = full.get(t["turn_id"], ("", ""))
        body = norm_ws(text, TEXT_LIMIT)
        if paste:
            body += "  ||PASTE|| " + norm_ws(paste, 300)
        elif "Pasted text" in text:
            body += "  ||PASTE-CONTENT-NOT-RECOVERABLE||"
        lines.append("[%03d] %s | %s | %s | %s\n      %s" % (
            i, t["project"], (t["ts"] or "")[:10], t["_split"], t["turn_id"], body))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    manifest = [{"n": i + 1, "turn_id": t["turn_id"], "project": t["project"],
                 "ts": t["ts"], "split": t["_split"], "sha1": t["sha1"],
                 "preview": t["preview"]} for i, t in enumerate(picked)]
    with open(args.manifest, "w", encoding="utf-8") as fh:
        json.dump({"_meta": {"script": "sample_turns.py",
                             "method": "systematic every-k sampling within "
                                       "per-project strata, turns time-sorted; "
                                       "split = 3 of every 5 to dev",
                             "quota": quota,
                             "pool_sizes": {p: next((t["_pool_size"] for t in picked
                                                     if t["project"] == p), 0)
                                            for p in quota}},
                   "sample": manifest}, fh, indent=2)
    print("sampled %d turns -> %s" % (len(picked), args.out))
    for p in quota:
        k = [t for t in picked if t["project"] == p]
        print("  %-10s %3d of %4d eligible (dev %d / held-out %d)" % (
            p, len(k), k[0]["_pool_size"] if k else 0,
            sum(1 for t in k if t["_split"] == "dev"),
            sum(1 for t in k if t["_split"] == "held_out")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
