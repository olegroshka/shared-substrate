#!/usr/bin/env python3
"""WS0-bis: how much substrate existed and never reached git?

Stdlib-only, read-only, every path parameterised (PLAN.md 5).

WHY THIS EXISTS
---------------
S6 review surfaced a measurement problem that invalidates a reading of WS1: the
operator created working artefacts - plans, roadmaps, review prompts, iteration
notes, research summaries - that were frequently NOT committed and were often
deleted. Every artefact-based measurement in this eval therefore sees a
SURVIVING subset, not the substrate as practised.

This matters because the bias is not noise: it is plausibly CORRELATED WITH THE
TREATMENT. blive's CONTEXT_PROTOCOL requires the substrate to be committed;
btest had no such rule. If the flat project's substrate was merely ephemeral
rather than absent, WS1's blive-22 / btest-12 gap is inflated by an artefact of
what survived.

WHAT THIS SCRIPT DOES AND DOES NOT DO
-------------------------------------
It measures the GAP. It does not close it.

  RECOVERABLE: that an artefact existed, its name, and roughly when.
  NOT RECOVERABLE: what it said. PyCharm's LocalHistory store on this machine
  holds change records (paths + timestamps) with NO content store, and the
  Claude Code transcripts cover only the sessions that survived retention. The
  March-May working artefacts are gone as text.

Consequence, stated here so it cannot be quietly forgotten downstream:
**WS1 cannot be re-scored from this.** A rubric axis such as "decision records,
0-3" needs an artefact's contents; a filename and a timestamp cannot tell a real
decision log from an empty stub. This script produces a CONFOUND MEASUREMENT and
a lower bound, never a corrected score.

THREE INDEPENDENT CHANNELS
--------------------------
  A  typed prompts     every .md filename the operator typed across the WS3 turn
                       corpus. Sees only what was named in a prompt.
  B  IDE local history  JetBrains LocalHistory change records. Full paths, so
                       project attribution is exact. No content.
  C  agent transcripts  Claude Code tool calls carrying a .md `file_path`. Has
                       content, but only for sessions that survived retention.

An artefact counts as EPHEMERAL when at least one channel saw it and NO corpus
repository has ever added a file of that basename on any ref
(`git log --all --diff-filter=A`), which counts committed-then-deleted files as
survivors. Matching is case-insensitive on the basename.

DELIBERATELY CONSERVATIVE, in three ways that all shrink the finding:
  1. The committed pool is the UNION over every corpus repo, so a file that
     moved between repos (btest -> smim, btest -> datacli) resolves as
     committed rather than as lost.
  2. Basename matching ignores directories, so any same-named file anywhere
     rescues it.
  3. Channels A and C see only artefacts the operator named or an agent wrote;
     a file created, used and deleted without ever being typed or tool-written
     is invisible to all three channels.
Every number here is therefore a LOWER BOUND and must be published as "at least
N", never as "N".

Usage:
  python artifact_survivorship.py \
      --repo blive=C:/Users/olegr/PycharmProjects/blive \
      --repo btest=C:/Users/olegr/PycharmProjects/btest \
      --turns ../data/session-metrics/local/turns-fulltext.jsonl \
      --local-history "C:/Users/olegr/AppData/Local/JetBrains" \
      --agent-transcripts "C:/Users/olegr/.claude/projects" \
      --out ../data/artifact-survivorship.json
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from corpus_common import (  # noqa: E402
    PROJECT_PATH_RE, canonical_project, eprint, git, git_version, iter_jsonl,
    redact_path,
)

VERSION = "1.0"

# A markdown filename as it appears in prose or a path. Requires a 3+ character
# alphanumeric run so prose fragments like `_v2.md` are not counted as artefacts.
MD_TOKEN_RE = re.compile(r"([A-Za-z0-9_][A-Za-z0-9_./\\-]*[A-Za-z0-9]{3}[A-Za-z0-9_./\\-]*\.md)\b")
# A full Windows path ending in .md, used for exact project attribution.
# Spaces are permitted because real artefacts here carry them (seamQ's claude.ai
# downloads: `4a adversarial review of b1.md`), but the FIRST version of this
# pattern ran greedily across sentence text and manufactured an artefact called
# "btest only, plan a safe doc-reorganization ... eodhd_uk_eu_migration_plan.md".
# is_plausible_basename() is the guard; the pattern alone is not enough.
MD_PATH_RE = re.compile(r"[A-Za-z]:[\\/][^\"<>|*?\r\n]{0,200}?\.md")
FILE_PATH_FIELD_RE = re.compile(r'"file_path"\s*:\s*"([^"]+\.md)"')

# Sentence punctuation never appears in a filename on this corpus; a candidate
# carrying it is prose the path pattern ran into.
IMPLAUSIBLE_RE = re.compile(r"[,:;?!()\[\]{}<>\"']|\s{2,}|\.\.\.")


def is_plausible_basename(b):
    if not b.lower().endswith(".md") or len(b) > 80:
        return False
    if IMPLAUSIBLE_RE.search(b):
        return False
    return len(b.split()) <= 10

# Artefacts that are not project substrate. `memory.md` and the auto-memory
# files are agent state, not deposits; the eval repo's own instruments are
# carried by the shared-substrate pool and resolve as committed anyway.
NON_SUBSTRATE = {"memory.md", "readme.md", "claude.md", "agents.md",
                 "license.md", "notice.md", "changelog.md"}


def basename(p):
    return str(p).replace("\\", "/").rstrip("/").rsplit("/", 1)[-1].lower()


def collect(text, seen_path, seen_token):
    """Both patterns, both guarded by is_plausible_basename()."""
    for m in MD_PATH_RE.finditer(text):
        b = basename(m.group(0))
        if is_plausible_basename(b):
            seen_path.append((b, m.group(0)))
    for m in MD_TOKEN_RE.finditer(text):
        b = basename(m.group(1))
        if is_plausible_basename(b):
            seen_token.append(b)


# --------------------------------------------------------------------------
# the committed pool
# --------------------------------------------------------------------------

def committed_md(repo):
    """Every .md basename ever ADDED on any ref - deletions included."""
    out = git(repo, "log", "--all", "--pretty=format:", "--name-only",
              "--diff-filter=A", check=False)
    names = {basename(l) for l in out.splitlines()
             if l.strip().lower().endswith(".md")}
    # ls-files catches anything added before the first reachable commit
    for l in git(repo, "ls-files", check=False).splitlines():
        if l.strip().lower().endswith(".md"):
            names.add(basename(l))
    return names


# --------------------------------------------------------------------------
# channel A - typed prompts
# --------------------------------------------------------------------------

def channel_typed_prompts(path):
    """-> {basename: {'sessions_project': Counter, 'mentions': n}}

    Attribution here is by the SESSION's project, which WS3 already showed is
    imperfect (12 of 1,480 turns were re-attributed). A file named in a btest
    session may belong to harp. Channel B resolves those by path; anything only
    channel A saw is flagged `attribution: session_folder`.
    """
    if not path or not Path(path).exists():
        return None
    seen = defaultdict(lambda: {"mentions": 0, "by_session_project": Counter(),
                                "by_path_project": Counter()})
    turns = 0
    for obj, _raw in iter_jsonl(path):
        if not obj:
            continue
        turns += 1
        text = obj.get("text") or ""
        proj = obj.get("project")
        paths, tokens = [], []
        collect(text, paths, tokens)
        for b, full in paths:                        # exact attribution first
            pm = PROJECT_PATH_RE.search(full)
            seen[b]["mentions"] += 1
            if pm:
                seen[b]["by_path_project"][canonical_project(pm.group(1))] += 1
        for b in tokens:
            if b not in dict(paths):
                seen[b]["mentions"] += 1
            if proj:
                seen[b]["by_session_project"][proj] += 1
    return {"turns_scanned": turns, "artifacts": dict(seen)}


# --------------------------------------------------------------------------
# channel B - JetBrains local history
# --------------------------------------------------------------------------

def channel_local_history(root):
    """JetBrains LocalHistory change records: exact paths, no content.

    The store is a binary blob; paths are readable ASCII inside it. We extract
    them and attribute by the PycharmProjects/IdeaProjects segment, so channel B
    needs no guessing. Whether a CONTENT store exists is probed and reported -
    on the machine this was written for it does not, which is why nothing here
    recovers what an artefact said.
    """
    if not root or not Path(root).exists():
        return None
    stores, hits = [], defaultdict(lambda: {"projects": Counter(), "installs": set()})
    content_available = False
    for store in sorted(Path(root).glob("*/LocalHistory/*")):
        if not store.is_file():
            continue
        try:
            blob = store.read_bytes()
        except OSError:
            continue
        stores.append({"path": redact_path(store), "bytes": len(blob)})
        text = blob.decode("latin-1", errors="replace")
        # a content store would carry markdown prose, not just paths
        if re.search(r"\n#{1,3} [A-Z][a-z]", text):
            content_available = True
        for m in MD_PATH_RE.finditer(text):
            pm = PROJECT_PATH_RE.search(m.group(0))
            b = basename(m.group(0))
            if not pm or not is_plausible_basename(b):
                continue
            hits[b]["projects"][canonical_project(pm.group(1))] += 1
            hits[b]["installs"].add(store.parent.parent.name)
    return {
        "stores": stores,
        "store_count": len(stores),
        "total_bytes": sum(s["bytes"] for s in stores),
        "content_store_available": content_available,
        "content_note": ("change records only - paths and timestamps, no file "
                         "contents. Artefact EXISTENCE is recoverable here; what "
                         "the artefact SAID is not."),
        "artifacts": {b: {"projects": dict(v["projects"]),
                          "installs": sorted(v["installs"])}
                      for b, v in hits.items()},
    }


# --------------------------------------------------------------------------
# channel C - agent transcripts
# --------------------------------------------------------------------------

def channel_agent_transcripts(root):
    """Claude Code tool calls carrying a .md file_path.

    Covers only sessions that survived retention (WS0 finding 1: btest 4
    sessions Jul 6-16, blive none). Its silence about a project is therefore
    evidence about the LOG, not about the project.
    """
    if not root or not Path(root).exists():
        return None
    hits = defaultdict(lambda: {"projects": Counter(), "refs": 0})
    files = 0
    for f in sorted(Path(root).glob("*/*.jsonl")):
        files += 1
        folder = canonical_project(f.parent.name.replace("C--Users-olegr-", "")
                                   .replace("PycharmProjects-", "")
                                   .replace("IdeaProjects-", ""))
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in FILE_PATH_FIELD_RE.finditer(raw):
            path = m.group(1)
            pm = PROJECT_PATH_RE.search(path.replace("\\\\", "/"))
            proj = canonical_project(pm.group(1)) if pm else folder
            b = basename(path)
            if not is_plausible_basename(b):
                continue
            hits[b]["projects"][proj] += 1
            hits[b]["refs"] += 1
    return {
        "transcript_files": files,
        "coverage_caveat": ("only sessions surviving Claude Code retention are "
                            "present (WS0 finding 1). Silence about a project is "
                            "evidence about the log, not about the project."),
        "artifacts": {b: {"projects": dict(v["projects"]), "refs": v["refs"]}
                      for b, v in hits.items()},
    }


# --------------------------------------------------------------------------
# union and attribution
# --------------------------------------------------------------------------

def combine(channels, pool, corpus):
    """-> per-artefact record with channels, attribution and survival."""
    A, B, C = channels
    rec = {}

    def touch(b):
        return rec.setdefault(b, {
            "basename": b, "channels": [], "committed": b in pool,
            "path_attribution": Counter(), "session_attribution": Counter(),
        })

    if B:
        for b, v in B["artifacts"].items():
            r = touch(b); r["channels"].append("B_local_history")
            r["path_attribution"].update(v["projects"])
            r["ide_installs"] = v["installs"]
    if C:
        for b, v in C["artifacts"].items():
            r = touch(b); r["channels"].append("C_agent_transcripts")
            r["path_attribution"].update(v["projects"])
    if A:
        for b, v in A["artifacts"].items():
            r = touch(b); r["channels"].append("A_typed_prompts")
            r["path_attribution"].update(v["by_path_project"])
            r["session_attribution"].update(v["by_session_project"])
            r["mentions"] = v["mentions"]

    out = []
    for b, r in rec.items():
        # Path attribution (channels B, C and A's full-path hits) is exact.
        # Session attribution is a fallback and is labelled as such, because
        # WS3 showed a file named in a btest session may belong to harp.
        if r["path_attribution"]:
            proj, conf = r["path_attribution"].most_common(1)[0][0], "path"
        elif r["session_attribution"]:
            proj, conf = r["session_attribution"].most_common(1)[0][0], "session_folder"
        else:
            proj, conf = None, "none"
        out.append({
            "basename": b,
            "project": proj,
            "attribution": conf,
            "channels": sorted(set(r["channels"])),
            "channel_count": len(set(r["channels"])),
            "committed_somewhere_in_corpus": r["committed"],
            "non_substrate": b in NON_SUBSTRATE,
            "mentions_in_prompts": r.get("mentions", 0),
            "ide_installs": r.get("ide_installs", []),
            "path_attribution": dict(r["path_attribution"]),
            "session_attribution": dict(r["session_attribution"]),
        })
    out.sort(key=lambda r: (r["project"] or "~", not r["committed_somewhere_in_corpus"],
                            r["basename"]))
    return out


def per_project(rows, corpus):
    stats = {}
    for p in corpus + [None]:
        mine = [r for r in rows if r["project"] == p and not r["non_substrate"]]
        if not mine:
            continue
        eph = [r for r in mine if not r["committed_somewhere_in_corpus"]]
        exact = [r for r in eph if r["attribution"] == "path"]
        stats[p or "_unattributed"] = {
            "artifacts_observed": len(mine),
            "committed": len(mine) - len(eph),
            "ephemeral_lower_bound": len(eph),
            "ephemeral_share": round(len(eph) / len(mine), 4) if mine else None,
            "ephemeral_path_attributed": len(exact),
            "ephemeral_session_attributed_only": len(eph) - len(exact),
            "ephemeral_names": sorted(r["basename"] for r in eph),
            "ephemeral_detail": [
                {"basename": r["basename"], "channels": r["channels"],
                 "attribution": r["attribution"], "mentions": r["mentions_in_prompts"]}
                for r in sorted(eph, key=lambda x: -x["mentions_in_prompts"])
            ],
        }
    return stats


DEFINITIONS = {
    "ephemeral_artifact": ("a .md artefact at least one channel observed, whose "
                           "basename no corpus repo has ever added on any ref "
                           "(`git log --all --diff-filter=A`, so "
                           "committed-then-deleted counts as SURVIVING)"),
    "lower_bound": ("every count is a floor. A file created, used and deleted "
                    "without ever being typed in a prompt or written by an agent "
                    "tool call is invisible to all three channels"),
    "attribution_path": "resolved from a full PycharmProjects/IdeaProjects path - exact",
    "attribution_session_folder": ("resolved from the session's project only - WS3 "
                                   "showed this misattributes (a file named in a "
                                   "btest session may belong to harp), so these are "
                                   "counted separately and never merged"),
    "why_WS1_is_not_rescored": ("existence is recoverable; content is not. A rubric "
                                "axis needs an artefact's contents to score. This "
                                "file measures a confound and never corrects a score"),
    "conservative_by_construction": ("the committed pool is the UNION over all corpus "
                                     "repos and matching is on basename only, so any "
                                     "same-named file anywhere rescues an artefact "
                                     "from the ephemeral count"),
}


def parse_repo_arg(s):
    if "=" not in s:
        raise argparse.ArgumentTypeError("expected name=path, got %r" % s)
    name, path = s.split("=", 1)
    p = Path(path).expanduser()
    if not (p / ".git").exists():
        raise argparse.ArgumentTypeError("not a git repo: %s" % p)
    return name, p


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", action="append", type=parse_repo_arg, required=True,
                    metavar="NAME=PATH")
    ap.add_argument("--turns", default=None, help="WS3 verbatim turn store (channel A)")
    ap.add_argument("--local-history", default=None, help="JetBrains root (channel B)")
    ap.add_argument("--agent-transcripts", default=None,
                    help="Claude Code projects root (channel C)")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verification-note", default=None)
    args = ap.parse_args()

    corpus = [n for n, _ in args.repo]
    pool, per_repo_pool = set(), {}
    for name, repo in args.repo:
        s = committed_md(repo)
        per_repo_pool[name] = len(s)
        pool |= s

    A = channel_typed_prompts(args.turns)
    B = channel_local_history(args.local_history)
    C = channel_agent_transcripts(args.agent_transcripts)

    rows = combine((A, B, C), pool, corpus)
    stats = per_project(rows, corpus)

    result = {
        "_meta": {
            "workstream": "WS0-bis artefact survivorship",
            "script": "artifact_survivorship.py",
            "version": VERSION,
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "git_version": git_version(),
            "definitions": DEFINITIONS,
            "verification": args.verification_note,
            "committed_md_pool_size": len(pool),
            "committed_md_per_repo": per_repo_pool,
            "channels": {
                "A_typed_prompts": {"available": A is not None,
                                    "turns_scanned": (A or {}).get("turns_scanned")},
                "B_local_history": {
                    "available": B is not None,
                    "stores": (B or {}).get("store_count"),
                    "bytes": (B or {}).get("total_bytes"),
                    "content_store_available": (B or {}).get("content_store_available"),
                },
                "C_agent_transcripts": {"available": C is not None,
                                        "files": (C or {}).get("transcript_files")},
            },
            "portability_note": ("channels B and C are machine-local stores. Inside a "
                                 "corporate environment (PLAN.md 5) they will differ or "
                                 "be absent; each is optional and its absence is "
                                 "reported rather than silently treated as zero"),
        },
        "per_project": stats,
        "channel_detail": {
            "B_local_history": {k: v for k, v in (B or {}).items() if k != "artifacts"},
            "C_agent_transcripts": {k: v for k, v in (C or {}).items() if k != "artifacts"},
        },
        "artifacts": rows,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)

    print("%-16s %10s %10s %12s %8s" % (
        "project", "observed", "committed", "ephemeral>=", "share"))
    print("-" * 60)
    for p in sorted(stats):
        s = stats[p]
        print("%-16s %10d %10d %12d %7s%%" % (
            p, s["artifacts_observed"], s["committed"], s["ephemeral_lower_bound"],
            "n/a" if s["ephemeral_share"] is None else round(100 * s["ephemeral_share"], 1)))
    ch = result["_meta"]["channels"]
    print("\nchannels: A=%s B=%s (content store: %s) C=%s" % (
        ch["A_typed_prompts"]["available"], ch["B_local_history"]["available"],
        ch["B_local_history"]["content_store_available"],
        ch["C_agent_transcripts"]["available"]))
    print("every count is a LOWER BOUND - publish as 'at least N'")
    print("wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
