#!/usr/bin/env python3
"""WS2 git outcome proxies: mine behavioural signals from git history alone.

Stdlib-only, read-only on the target repos, all paths parameterised, so the
identical script runs inside a corporate environment against P8 (PLAN.md 5).

Metrics per repo (definitions are echoed into every output file so a number can
never be read without its approximation):

  1. short-horizon churn  - share of added lines re-modified within N days
  2. fix / revert ratio   - subject-pattern classification over non-merge commits
  3. re-fix recurrence    - files appearing in >=3 fix-classified commits
  4. gap recovery         - what the first commits after a >=5-day gap do
  5. root hygiene         - untracked / ignored / scratch litter in the repo root
  6. test trajectory      - test-file count at ~10 evenly spaced commits
  7. ID-prefix timeline   - per-month share of commits carrying a stable-ID
                            prefix (the btest [SMIM] discipline-decay curve)

Usage:
  python git_miner.py --repo blive=C:/Users/olegr/PycharmProjects/blive \
                      --repo btest=C:/Users/olegr/PycharmProjects/btest \
                      --out-dir ../data/git-metrics
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
    classify, count_merges, eprint, git, git_version, is_source, is_test_file,
    is_vendored, read_log,
)

VERSION = "1.0"
DAY = 86400

# --------------------------------------------------------------------------
# 2. commit-subject classification
# --------------------------------------------------------------------------

# Conventional-commit style prefix (btest, b-autobot, datacli use it).
FIX_PREFIX_RE = re.compile(r"^\s*(fix|bugfix|hotfix)(\([^)]*\))?\s*[:!]", re.I)
# Free-text fix wording (blive, seamQ, smim, harp, and btest's 2025 era).
FIX_WORD_RE = re.compile(
    r"\b(fix|fixes|fixed|fixing|bugfix|hotfix|bug|repair|repaired"
    r"|correct|corrects|corrected|correction|resolve|resolved"
    r"|patch|patched|workaround|regression|broken)\b", re.I,
)
REVERT_RE = re.compile(r"(^\s*revert\b|\brevert(s|ed|ing)?\b|\brollback\b)", re.I)

DOCS_RE = re.compile(
    r"(^\s*docs?(\([^)]*\))?\s*[:!]|\b(docs?|documentation|readme|changelog"
    r"|comment|comments|writeup|write-up)\b)", re.I,
)
TEST_RE = re.compile(
    r"(^\s*test(\([^)]*\))?\s*[:!]|\b(test|tests|testing|coverage|pytest"
    r"|unit tests?|integration tests?)\b)", re.I,
)
FEATURE_RE = re.compile(
    r"(^\s*feat(ure)?(\([^)]*\))?\s*[:!]|\b(add|adds|added|adding|implement"
    r"|implements|implemented|introduce|introduces|new|support|supports"
    r"|enable|enables|extend|extends)\b)", re.I,
)
CHORE_RE = re.compile(
    r"(^\s*(chore|refactor|style|build|ci|perf|deps?)(\([^)]*\))?\s*[:!]"
    r"|\b(chore|refactor|refactors|refactored|cleanup|clean up|tidy|tidies"
    r"|rename|renames|renamed|bump|bumps|move|moves|moved|extract|extracts"
    r"|extracted|reorganis|reorganiz|untrack|strip|remove|removes|removed"
    r"|drop|drops|dropped)\b)", re.I,
)

# Precedence is fixed and documented: a subject is assigned to the FIRST
# bucket that matches, so "fix docs typo" counts as a fix, not as docs.
CLASS_ORDER = [
    ("revert", REVERT_RE),
    ("fix", None),        # special: FIX_PREFIX_RE or FIX_WORD_RE
    ("docs", DOCS_RE),
    ("test", TEST_RE),
    ("feature", FEATURE_RE),
    ("chore", CHORE_RE),
]


def is_fix(subject):
    return bool(FIX_PREFIX_RE.search(subject) or FIX_WORD_RE.search(subject))


def classify_subject(subject):
    for name, rx in CLASS_ORDER:
        if name == "fix":
            if is_fix(subject):
                return "fix"
        elif rx.search(subject):
            return name
    return "other"


# --------------------------------------------------------------------------
# 7. stable-ID prefixes
# --------------------------------------------------------------------------

# Bracketed tag at the head of the subject. The tag may carry a scope after
# the namespace - btest's real convention is '[SMIM DATA-6]' / '[SMIM GPU-1.2]',
# not a bare '[SMIM]'. An earlier version required a space-free tag and
# undercounted btest 110 vs 293; the internal space is the norm, not the
# exception, so the tag body is captured whole and split afterwards.
BRACKET_PREFIX_RE = re.compile(r"^\s*\[([^\]\n]{1,60})\]")
# A scoped tag carries a sub-identifier beyond the namespace ('SMIM DATA-6'),
# i.e. the commit is pinned to a specific work item, not merely to a project.
SCOPED_TAG_RE = re.compile(r"^\S+[\s:_-]+\S")
# Substrate ID references anywhere in the subject: ADR-052, KB-7, OQ-032, DD-1,
# RETRO-M3, M3.4 milestone tags.
STABLE_ID_RE = re.compile(r"\b([A-Z]{2,6}-[A-Za-z]?\d+(?:\.\d+)?)\b")


# --------------------------------------------------------------------------
# 1. short-horizon churn
# --------------------------------------------------------------------------

def short_horizon_churn(commits, windows=(14, 30)):
    """Share of added lines that are re-modified within W days.

    APPROXIMATION (blame-free, documented because it is not exact):
    `git log --numstat` gives per-commit, per-file (added, deleted) counts but
    no line identity. We therefore maintain, per file, a LIFO stack of live
    added lines tagged with the timestamp at which they were added. When a
    later commit deletes D lines from that file, we pop D lines off the top of
    the stack - i.e. we assume the most recently written lines are the ones
    most likely to be rewritten (the standard recency heuristic behind the
    code-churn literature; Nagappan & Ball 2005 use blame, we cannot without
    walking every revision). A popped line whose add-timestamp is within W days
    of the deleting commit counts as short-horizon rework.

    Within a single commit deletions are applied before additions, so a
    modified line (+1/-1) does not delete itself.

    KNOWN BIASES, stated rather than hidden:
      - LIFO over-attributes rework in files with a stable head and a churning
        tail, and under-attributes it in files rewritten from the top.
      - Reformatting or import-sorting commits register as rework.
      - Renames carry their stack across (git -M), but a rename git fails to
        detect resets that file's age clock, biasing the share DOWN.
      - Deletions exceeding the reconstructed stack (pre-history content,
        undetected renames) are reported separately as `unattributed_deletions`
        and are excluded from both numerator and denominator.
    """
    stacks = defaultdict(list)         # path -> [[ts, n_lines], ...] oldest first
    total_added = 0
    rework = {w: 0 for w in windows}
    attributed_del = 0
    unattributed_del = 0

    for c in commits:
        for added, deleted, old, new in c.files:
            if added is None or deleted is None:      # binary
                continue
            if is_vendored(new) or not is_source(new):
                continue
            if old and old != new and old in stacks:  # carry rename history
                stacks[new] = stacks.pop(old) + stacks[new]
            st = stacks[new]
            need = deleted
            while need > 0 and st:
                ts, n = st[-1]
                take = min(n, need)
                age = c.ts - ts
                for w in windows:
                    if age <= w * DAY:
                        rework[w] += take
                attributed_del += take
                need -= take
                if take == n:
                    st.pop()
                else:
                    st[-1][1] = n - take
            unattributed_del += need
            if added:
                st.append([c.ts, added])
                total_added += added

    span_days = round((commits[-1].ts - commits[0].ts) / DAY, 1) if len(commits) > 1 else 0
    out = {
        "total_added_lines": total_added,
        "attributed_deletions": attributed_del,
        "unattributed_deletions": unattributed_del,
        "surviving_lines": total_added - attributed_del,
        # Denominator-free companion: rework at ANY horizon. The N-day shares
        # must always be read against this and against span_days - in a project
        # shorter than the window (seamQ: 2 days) the 14-day share is the
        # whole-history share by construction, not a fast-rework signal.
        "rework_share_any_horizon": (
            round(attributed_del / total_added, 4) if total_added else None
        ),
        "history_span_days": span_days,
    }
    for w in windows:
        out["rework_lines_%dd" % w] = rework[w]
        out["churn_share_%dd" % w] = (
            round(rework[w] / total_added, 4) if total_added else None
        )
        out["window_exceeds_history_%dd" % w] = span_days < w
    return out


# --------------------------------------------------------------------------
# 3. re-fix recurrence
# --------------------------------------------------------------------------

def refix_recurrence(commits, threshold=3, top_n=15):
    fix_touches = Counter()
    files_in_fixes = set()
    for c in commits:
        if not (is_fix(c.subject) or REVERT_RE.search(c.subject)):
            continue
        seen = set()
        for _, _, _, new in c.files:
            if is_vendored(new) or not is_source(new) or new in seen:
                continue
            seen.add(new)
            fix_touches[new] += 1
            files_in_fixes.add(new)
    recurrent = {f: n for f, n in fix_touches.items() if n >= threshold}
    return {
        "threshold": threshold,
        "files_touched_by_fix_commits": len(files_in_fixes),
        "recurrent_fix_files": len(recurrent),
        "recurrent_fix_file_share": (
            round(len(recurrent) / len(files_in_fixes), 4) if files_in_fixes else None
        ),
        "top_files": [
            {"path": f, "fix_commits": n}
            for f, n in sorted(fix_touches.items(), key=lambda kv: (-kv[1], kv[0]))[:top_n]
            if n >= 2
        ],
    }


# --------------------------------------------------------------------------
# 4. gap recovery
# --------------------------------------------------------------------------

def gap_recovery(commits, gap_days=5, follow=3):
    gaps = []
    post_gap_classes = Counter()
    for i in range(1, len(commits)):
        delta = commits[i].ts - commits[i - 1].ts
        if delta < gap_days * DAY:
            continue
        window = commits[i:i + follow]
        classes = [classify_subject(c.subject) for c in window]
        for cl in classes:
            post_gap_classes[cl] += 1
        gaps.append({
            "gap_days": round(delta / DAY, 1),
            "last_before": commits[i - 1].iso[:10],
            "first_after": commits[i].iso[:10],
            "post_gap": [
                {"date": c.iso[:10], "class": cl, "subject": c.subject[:110]}
                for c, cl in zip(window, classes)
            ],
        })
    baseline = Counter(classify_subject(c.subject) for c in commits)
    n_post = sum(post_gap_classes.values())
    n_base = sum(baseline.values())
    return {
        "gap_threshold_days": gap_days,
        "commits_classified_after_each_gap": follow,
        "gap_count": len(gaps),
        "post_gap_class_counts": dict(post_gap_classes.most_common()),
        "post_gap_class_shares": {
            k: round(v / n_post, 4) for k, v in post_gap_classes.most_common()
        } if n_post else {},
        "baseline_class_shares": {
            k: round(v / n_base, 4) for k, v in baseline.most_common()
        } if n_base else {},
        "gaps": gaps,
    }


# --------------------------------------------------------------------------
# 5. root hygiene
# --------------------------------------------------------------------------

SCRATCH_RE = re.compile(
    r"^(tmp[_.\-]|temp[_.\-]|scratch|debug[_.\-]|out\d*\.|nul$|core\.\d+)"
    r"|\.(tmp|bak|orig|rej|log|swp)$"
    r"|[_.\-](tmp|bak|old|backup|copy)(\.[A-Za-z0-9]+)?$",
    re.IGNORECASE,
)


def root_hygiene(repo):
    """Litter in the repo root, measured three ways.

    The metric as specified (untracked files per `git status --porcelain`) is
    reported first, but it ALONE is misleading: a project can silence its own
    litter with a .gitignore rule and score clean. btest is exactly that case -
    1 untracked file, 20+ tmp_* scratch files on disk, all gitignored. So the
    ignored and on-disk views are reported alongside, and the headline for the
    report is `scratch_litter_root`, which counts scratch-named root entries
    regardless of tracking status.
    """
    porcelain = git(repo, "status", "--porcelain", check=False).splitlines()
    untracked = [ln[3:].strip().strip('"') for ln in porcelain if ln.startswith("??")]
    modified = [ln for ln in porcelain if not ln.startswith("??")]
    ignored_raw = git(repo, "status", "--porcelain", "--ignored=matching",
                      check=False).splitlines()
    ignored = [ln[3:].strip().strip('"') for ln in ignored_raw if ln.startswith("!!")]

    at_root = lambda paths: [p for p in paths if "/" not in p.rstrip("/")]
    tracked_root = [p for p in git(repo, "ls-files").splitlines() if "/" not in p]

    root = Path(repo)
    fs_entries = sorted(
        p.name + ("/" if p.is_dir() else "")
        for p in root.iterdir() if p.name != ".git"
    )
    scratch = [e for e in fs_entries if SCRATCH_RE.search(e.rstrip("/"))]

    return {
        "untracked_root": len(at_root(untracked)),
        "untracked_total": len(untracked),
        "untracked_root_entries": sorted(at_root(untracked))[:40],
        "uncommitted_modifications": len(modified),
        "ignored_root": len(at_root(ignored)),
        "tracked_root_files": len(tracked_root),
        "fs_root_entries": len(fs_entries),
        "scratch_litter_root": len(scratch),
        "scratch_litter_examples": scratch[:30],
        "note": ("untracked_root follows the specified definition; "
                 "scratch_litter_root counts on-disk scratch files at the root "
                 "whether tracked, untracked or gitignored"),
    }


# --------------------------------------------------------------------------
# 6. test trajectory
# --------------------------------------------------------------------------

def test_trajectory(repo, commits, samples=10):
    if not commits:
        return {"samples": []}
    n = len(commits)
    if n <= samples:
        idx = list(range(n))
    else:
        idx = sorted({round(i * (n - 1) / (samples - 1)) for i in range(samples)})
    rows = []
    for i in idx:
        c = commits[i]
        paths = git(repo, "ls-tree", "-r", "--name-only", c.sha).splitlines()
        src = [p for p in paths if is_source(p)]
        tests = [p for p in src if is_test_file(p)]
        rows.append({
            "commit_index": i + 1,
            "date": c.iso[:10],
            "sha": c.sha[:10],
            "source_files": len(src),
            "test_files": len(tests),
            "test_file_share": round(len(tests) / len(src), 4) if src else None,
            "vendored_files_excluded": sum(1 for p in paths if is_vendored(p)),
        })
    first, last = rows[0], rows[-1]
    return {
        "sample_count": len(rows),
        "test_files_first": first["test_files"],
        "test_files_last": last["test_files"],
        "test_share_first": first["test_file_share"],
        "test_share_last": last["test_file_share"],
        "samples": rows,
    }


# --------------------------------------------------------------------------
# 7. ID-prefix (discipline) timeline
# --------------------------------------------------------------------------

def id_timeline(commits):
    per_month = defaultdict(
        lambda: {"commits": 0, "bracket_prefix": 0, "scoped_tag": 0, "stable_id": 0}
    )
    namespaces = Counter()
    tags = Counter()
    total_bracket = total_scoped = total_id = 0
    for c in commits:
        m = per_month[c.month]
        m["commits"] += 1
        bm = BRACKET_PREFIX_RE.match(c.subject)
        if bm:
            tag = bm.group(1).strip()
            m["bracket_prefix"] += 1
            total_bracket += 1
            tags[tag] += 1
            namespaces[re.split(r"[\s:_-]", tag, 1)[0]] += 1
            if SCOPED_TAG_RE.match(tag):
                m["scoped_tag"] += 1
                total_scoped += 1
        if STABLE_ID_RE.search(c.subject):
            m["stable_id"] += 1
            total_id += 1
    months = []
    for mo in sorted(per_month):
        d = per_month[mo]
        months.append({
            "month": mo,
            "commits": d["commits"],
            "bracket_prefix_commits": d["bracket_prefix"],
            "bracket_prefix_share": round(d["bracket_prefix"] / d["commits"], 4),
            "scoped_tag_commits": d["scoped_tag"],
            "scoped_tag_share": round(d["scoped_tag"] / d["commits"], 4),
            "stable_id_commits": d["stable_id"],
            "stable_id_share": round(d["stable_id"] / d["commits"], 4),
        })
    n = len(commits)
    # trailing-30-commit share: the decay headline, insensitive to month size
    tail = commits[-30:]
    tail_bracket = sum(1 for c in tail if BRACKET_PREFIX_RE.match(c.subject))
    return {
        "total_commits": n,
        "bracket_prefix_commits": total_bracket,
        "bracket_prefix_share": round(total_bracket / n, 4) if n else None,
        "scoped_tag_commits": total_scoped,
        "scoped_tag_share": round(total_scoped / n, 4) if n else None,
        "stable_id_commits": total_id,
        "stable_id_share": round(total_id / n, 4) if n else None,
        "namespaces": dict(namespaces.most_common(10)),
        "top_tags": dict(tags.most_common(12)),
        "last_30_commits_bracket_share": (
            round(tail_bracket / len(tail), 4) if tail else None
        ),
        "per_month": months,
    }


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

DEFINITIONS = {
    "commit_set": ("non-merge commits, full history, author dates; merge commits "
                   "excluded because their numstat double-counts merged-in lines "
                   "(merge count reported separately)"),
    "excluded_paths": ("vendored/generated trees (node_modules, dist, build, "
                       "target, assets_dist, .venv, __pycache__, lock files, "
                       "*.min.js, *.map) and any file outside the source-extension "
                       "allowlist (parquet/png/pdf/csv data files are not source)"),
    "short_horizon_churn": ("share of added source lines re-modified within N days, "
                            "via a per-file LIFO line-age stack over `git log "
                            "--numstat -M`; blame-free approximation - see the "
                            "docstring in git_miner.py for its biases"),
    "fix_ratio": ("commits whose subject matches a fix/bugfix/hotfix prefix or any "
                  "fix-family word, over non-merge commits; revert counted "
                  "separately and takes precedence"),
    "refix_recurrence": "source files appearing in >=3 fix- or revert-classified commits",
    "gap_recovery": ("for every inter-commit gap >=5 days, the first 3 post-gap "
                     "commits classified by subject; precedence "
                     "revert>fix>docs>test>feature>chore>other"),
    "root_hygiene": ("untracked root entries per `git status --porcelain` (as "
                     "specified) plus ignored-root and on-disk scratch counts, "
                     "because .gitignore can hide litter from the specified metric"),
    "test_trajectory": ("test-file count at ~10 evenly spaced commits, read with "
                        "`git ls-tree` (no checkout); test = source file in a test "
                        "tree or with a test naming convention"),
    "id_timeline": ("per-month share of commits carrying a bracketed stable-ID "
                    "prefix (e.g. '[SMIM] ', '[blive] ') and share referencing a "
                    "stable ID (ADR-052, KB-7, OQ-032) anywhere in the subject"),
}


def mine(name, repo, verification=None):
    commits = read_log(repo)
    n = len(commits)
    subjects = [c.subject for c in commits]
    fix_prefix = sum(1 for s in subjects if FIX_PREFIX_RE.search(s))
    fix_any = sum(1 for s in subjects if is_fix(s))
    reverts = sum(1 for s in subjects if REVERT_RE.search(s))
    classes = Counter(classify_subject(s) for s in subjects)

    degenerate = n < 2
    result = {
        "_meta": {
            "script": "git_miner.py",
            "version": VERSION,
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "git_version": git_version(),
            "project": name,
            "repo_path": str(repo),
            "definitions": DEFINITIONS,
            "verification": verification,
            "degenerate_history": degenerate,
            "degenerate_note": (
                "single-commit history (squashed): every history-derived metric "
                "below is n/a - history lost, not absent behaviour"
            ) if degenerate else None,
        },
        "history": {
            "non_merge_commits": n,
            "merge_commits": count_merges(repo),
            "first_commit": commits[0].iso[:10] if commits else None,
            "last_commit": commits[-1].iso[:10] if commits else None,
            "span_days": round((commits[-1].ts - commits[0].ts) / DAY, 1) if n > 1 else 0,
            "active_months": len({c.month for c in commits}),
        },
        "commit_classes": {
            "counts": dict(classes.most_common()),
            "shares": {k: round(v / n, 4) for k, v in classes.most_common()} if n else {},
        },
        "fix_revert": {
            "fix_prefix_commits": fix_prefix,
            "fix_commits": fix_any,
            "revert_commits": reverts,
            "fix_ratio": round(fix_any / n, 4) if n else None,
            "revert_ratio": round(reverts / n, 4) if n else None,
            "fix_or_revert_ratio": round(
                sum(1 for s in subjects if is_fix(s) or REVERT_RE.search(s)) / n, 4
            ) if n else None,
        },
        "short_horizon_churn": short_horizon_churn(commits),
        "refix_recurrence": refix_recurrence(commits),
        "gap_recovery": gap_recovery(commits),
        "root_hygiene": root_hygiene(repo),
        "test_trajectory": test_trajectory(repo, commits),
        "id_timeline": id_timeline(commits),
    }
    if degenerate:
        # Never fake a number that history cannot support.
        for key in ("short_horizon_churn", "gap_recovery"):
            result[key] = {"status": "n/a: history lost (1 commit)",
                           "computed_anyway": result[key]}
    return result


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
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--verification-note", default=None,
                    help="hand-verification statement recorded in each _meta header")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    print("%-12s %6s %6s %8s %8s %8s %7s %7s" % (
        "project", "cmts", "fix%", "churn14%", "refix>=3", "gaps>=5d", "litter", "ID%"))
    print("-" * 72)
    for name, repo in args.repo:
        try:
            res = mine(name, repo, args.verification_note)
        except Exception as exc:                       # keep the sweep going
            eprint("ERROR %s: %s" % (name, exc))
            continue
        out = args.out_dir / ("%s.json" % name)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=2)
        ch = res["short_horizon_churn"]
        ch = ch.get("computed_anyway", ch)
        gr = res["gap_recovery"]
        gr = gr.get("computed_anyway", gr)
        pct = lambda v: "n/a" if v is None else "%.1f" % (100 * v)
        print("%-12s %6d %6s %8s %8d %8d %7d %7s" % (
            name,
            res["history"]["non_merge_commits"],
            pct(res["fix_revert"]["fix_ratio"]),
            pct(ch.get("churn_share_14d")),
            res["refix_recurrence"]["recurrent_fix_files"],
            gr.get("gap_count", 0),
            res["root_hygiene"]["scratch_litter_root"],
            pct(res["id_timeline"]["bracket_prefix_share"]),
        ))
    print("\nwrote %d files to %s" % (len(args.repo), args.out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
