#!/usr/bin/env python3
"""WS0 evidence audit: inventory AI-session logs per project.

Scans Claude Code transcript dirs (~/.claude/projects/<munged>/<session>.jsonl)
and Copilot JetBrains session stores (~/.copilot/jb/<uuid>/partition-N.jsonl),
attributes sessions to projects, and emits an evidence map JSON.

Stdlib-only and path-parameterised so the identical script runs inside a
corporate environment against whatever log stores exist there.

Usage:
  python evidence_audit.py --claude-dir ~/.claude/projects --copilot-dir ~/.copilot/jb \
      --projects blive btest b-autobot datacli smim harp seamQ --out ../data/evidence-map.json
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_PATH_RE = re.compile(
    r"(?:PycharmProjects|IdeaProjects)[\\/]+([A-Za-z0-9._-]+)"
)
TS_RE = re.compile(r'"timestamp"\s*:\s*"([^"]+)"')


def iter_lines(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield line


def scan_claude_session(path):
    """One Claude Code session file -> stats dict."""
    s = {
        "file": path.name,
        "bytes": path.stat().st_size,
        "first_ts": None,
        "last_ts": None,
        "user_msgs": 0,
        "assistant_msgs": 0,
        "sidechain_msgs": 0,
        "tokens_in": 0,
        "tokens_out": 0,
        "tokens_cache_read": 0,
        "cwds": set(),
        "parse_errors": 0,
    }
    for line in iter_lines(path):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            s["parse_errors"] += 1
            continue
        ts = obj.get("timestamp")
        if ts:
            if s["first_ts"] is None or ts < s["first_ts"]:
                s["first_ts"] = ts
            if s["last_ts"] is None or ts > s["last_ts"]:
                s["last_ts"] = ts
        cwd = obj.get("cwd")
        if cwd:
            s["cwds"].add(cwd)
        typ = obj.get("type")
        if obj.get("isSidechain"):
            if typ in ("user", "assistant"):
                s["sidechain_msgs"] += 1
        elif typ == "user" and not obj.get("isMeta"):
            s["user_msgs"] += 1
        elif typ == "assistant":
            s["assistant_msgs"] += 1
        usage = (obj.get("message") or {}).get("usage") if isinstance(obj.get("message"), dict) else None
        if usage:
            s["tokens_in"] += usage.get("input_tokens", 0) or 0
            s["tokens_out"] += usage.get("output_tokens", 0) or 0
            s["tokens_cache_read"] += usage.get("cache_read_input_tokens", 0) or 0
    s["cwds"] = sorted(s["cwds"])
    return s


def scan_copilot_session(folder):
    """One Copilot session folder (partition-*.jsonl) -> stats dict."""
    s = {
        "session": folder.name,
        "bytes": 0,
        "first_ts": None,
        "last_ts": None,
        "user_msgs": 0,
        "assistant_msgs": 0,
        "project_hits": Counter(),
        "parse_errors": 0,
    }
    for part in sorted(folder.glob("partition-*.jsonl")):
        s["bytes"] += part.stat().st_size
        for line in iter_lines(part):
            for m in PROJECT_PATH_RE.finditer(line):
                s["project_hits"][m.group(1)] += 1
            try:
                obj = json.loads(line)
                ts = obj.get("timestamp")
                typ = obj.get("type", "")
            except json.JSONDecodeError:
                s["parse_errors"] += 1
                tsm = TS_RE.search(line)
                ts = tsm.group(1) if tsm else None
                typ = ""
            if ts:
                if s["first_ts"] is None or ts < s["first_ts"]:
                    s["first_ts"] = ts
                if s["last_ts"] is None or ts > s["last_ts"]:
                    s["last_ts"] = ts
            if typ.startswith("user."):
                s["user_msgs"] += 1
            elif typ.startswith("assistant.message"):
                s["assistant_msgs"] += 1
    hits = s["project_hits"]
    s["attributed_project"] = hits.most_common(1)[0][0] if hits else None
    s["project_hits"] = dict(hits.most_common(8))
    return s


def scan_history(path):
    """Global Claude Code history.jsonl (user prompts only; survives transcript
    cleanup) -> per-project aggregates."""
    from datetime import datetime, timezone

    agg = {}
    for line in iter_lines(path):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        proj = (obj.get("project") or "?").replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]
        a = agg.setdefault(proj, {"prompts": 0, "session_ids": set(),
                                  "first_ts": None, "last_ts": None})
        a["prompts"] += 1
        sid = obj.get("sessionId")
        if sid:
            a["session_ids"].add(sid)
        ts = obj.get("timestamp")
        if isinstance(ts, (int, float)):
            iso = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).isoformat()
            if a["first_ts"] is None or iso < a["first_ts"]:
                a["first_ts"] = iso
            if a["last_ts"] is None or iso > a["last_ts"]:
                a["last_ts"] = iso
    for a in agg.values():
        a["sessions"] = len(a.pop("session_ids"))
    return agg


def aggregate(per_session, key_fn):
    agg = {}
    for s in per_session:
        key = key_fn(s) or "_unattributed"
        a = agg.setdefault(key, {
            "sessions": 0, "bytes": 0, "user_msgs": 0, "assistant_msgs": 0,
            "tokens_in": 0, "tokens_out": 0, "tokens_cache_read": 0,
            "first_ts": None, "last_ts": None,
        })
        a["sessions"] += 1
        for k in ("bytes", "user_msgs", "assistant_msgs",
                  "tokens_in", "tokens_out", "tokens_cache_read"):
            a[k] += s.get(k, 0)
        for bound, cmp_first in (("first_ts", True), ("last_ts", False)):
            ts = s.get(bound)
            if ts and (a[bound] is None or (ts < a[bound]) == cmp_first):
                a[bound] = ts
    return agg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claude-dir", type=Path, default=None)
    ap.add_argument("--history-file", type=Path, default=None,
                    help="Claude Code global history.jsonl (user prompts)")
    ap.add_argument("--copilot-dir", type=Path, default=None)
    ap.add_argument("--projects", nargs="*", default=[],
                    help="corpus project names for gap reporting")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    result = {"claude_code": {}, "claude_history": {}, "copilot": {}, "gaps": []}

    if args.history_file and args.history_file.is_file():
        result["claude_history"] = scan_history(args.history_file)

    if args.claude_dir and args.claude_dir.is_dir():
        for proj_dir in sorted(args.claude_dir.iterdir()):
            if not proj_dir.is_dir():
                continue
            sessions = [scan_claude_session(f) for f in sorted(proj_dir.glob("*.jsonl"))]
            if not sessions:
                continue
            agg = aggregate(sessions, lambda s: proj_dir.name)[proj_dir.name]
            agg["per_session"] = sessions
            result["claude_code"][proj_dir.name] = agg

    if args.copilot_dir and args.copilot_dir.is_dir():
        sessions = [scan_copilot_session(d) for d in sorted(args.copilot_dir.iterdir())
                    if d.is_dir()]
        sessions = [s for s in sessions if s["bytes"] > 0]
        agg = aggregate(sessions, lambda s: s["attributed_project"])
        for k, v in agg.items():
            v["per_session"] = [s for s in sessions if (s["attributed_project"] or "_unattributed") == k]
        result["copilot"] = agg

    for p in args.projects:
        cc = [k for k in result["claude_code"] if k.endswith("-" + p)]
        ch = p in result["claude_history"]
        cp = p in result["copilot"]
        if not cc and not ch and not cp:
            result["gaps"].append(p)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, default=str)

    # human summary
    print(f"{'source/project':<52}{'sess':>5}{'  MB':>7}{'user':>6}{'asst':>6}{'tok_out(M)':>11}  span")
    for name, a in sorted(result["claude_code"].items()):
        print(f"CC  {name:<48}{a['sessions']:>5}{a['bytes']/1e6:>7.1f}{a['user_msgs']:>6}"
              f"{a['assistant_msgs']:>6}{a['tokens_out']/1e6:>11.2f}  "
              f"{(a['first_ts'] or '?')[:10]} -> {(a['last_ts'] or '?')[:10]}")
    for name, a in sorted(result["claude_history"].items()):
        print(f"CH  {name:<48}{a['sessions']:>5}{'':>7}{a['prompts']:>6}{'':>6}{'n/a':>11}  "
              f"{(a['first_ts'] or '?')[:10]} -> {(a['last_ts'] or '?')[:10]}")
    for name, a in sorted(result["copilot"].items()):
        print(f"CP  {name:<48}{a['sessions']:>5}{a['bytes']/1e6:>7.1f}{a['user_msgs']:>6}"
              f"{a['assistant_msgs']:>6}{'n/a':>11}  "
              f"{(a['first_ts'] or '?')[:10]} -> {(a['last_ts'] or '?')[:10]}")
    if result["gaps"]:
        print("\nGAPS (no logs found): " + ", ".join(result["gaps"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
