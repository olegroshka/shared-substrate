#!/usr/bin/env python3
"""WS-X complexity profile: a vector of established primitives, never a scalar.

PLAN.md 4 WS-X states the design constraint this script implements: there is no
reputable single "project complexity" number, and composite indices with
invented weights are not defensible. So five primitives are computed per
project and reported side by side; instead of weighting them, rank concordance
across them (Kendall's W) is reported, so the moderator analysis can rest only
on orderings that are stable under every metric.

Primitives
  1. size            - non-blank LOC over `git ls-files` source files, by tier
                       (code / docs / config), file count, language count
  2. change entropy  - Hassan (ICSE 2009), normalised; full history + per quarter
  3. coordination    - duration, session count (WS0 evidence map), distinct
     scope             directories touched per active month, decision-record count
  4. dependencies    - direct deps parsed from pyproject.toml / pom.xml / package.json
  5. AIT             - LZMA-compressed size of the concatenated sorted source
                       files (pinned compressor + preset) as a practical upper
                       bound on K(repo), plus the compression ratio

Not to be conflated with WS5's kernel: that estimates K(x | S) by LLM log-loss;
this is plain K(repo) by classical compression.

Usage:
  python complexity_profile.py --repo blive=C:/.../blive [--repo ...] \
      --evidence-map ../data/evidence-map.json --out ../data/complexity-profiles.json
"""

import argparse
import json
import lzma
import math
import re
import sys
import tomllib
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median

sys.path.insert(0, str(Path(__file__).resolve().parent))

from corpus_common import (  # noqa: E402
    classify, eprint, git, git_version, is_source, is_vendored, read_log,
)

VERSION = "1.0"
DAY = 86400
MAX_FILE_BYTES = 5_000_000        # guards against a stray generated blob

# Pinned so the AIT figure is reproducible across machines and years.
LZMA_FILTERS = [{"id": lzma.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME}]
LZMA_SPEC = "FORMAT_RAW / FILTER_LZMA2 / preset=9|PRESET_EXTREME"


# --------------------------------------------------------------------------
# 1 + 5. size and algorithmic information
# --------------------------------------------------------------------------

def size_and_ait(repo):
    tracked = [p for p in git(repo, "ls-files").splitlines() if p.strip()]
    vendored = [p for p in tracked if is_vendored(p)]
    loc = Counter()
    files = Counter()
    langs = Counter()
    kept = []                        # (path, tier, raw) in sorted-path order
    missing = 0
    oversize = 0

    for path in sorted(tracked):
        tier, lang = classify(path)
        if tier is None:
            continue
        fp = Path(repo) / path
        try:
            if fp.stat().st_size > MAX_FILE_BYTES:
                oversize += 1
                continue
            raw = fp.read_bytes()
        except OSError:
            missing += 1              # tracked but absent from the worktree
            continue
        files[tier] += 1
        langs[lang] += 1 if tier == "code" else 0
        text = raw.decode("utf-8", errors="replace")
        loc[tier] += sum(1 for ln in text.splitlines() if ln.strip())
        kept.append((path, tier, raw))

    # Sorted-PATH order exactly as PLAN.md 4 WS-X specifies. Grouping by tier
    # first would compress ~differently (like-with-like packs better), so the
    # concatenation order is part of the metric definition, not an incidental.
    all_source = b"".join(raw for _, _, raw in kept)
    code_only = b"".join(raw for _, t, raw in kept if t == "code")
    comp_all = lzma.compress(all_source, format=lzma.FORMAT_RAW, filters=LZMA_FILTERS)
    comp_code = lzma.compress(code_only, format=lzma.FORMAT_RAW, filters=LZMA_FILTERS)

    code_langs = {k: v for k, v in langs.items() if v}
    n_source = sum(files.values())
    return {
        "size": {
            "tracked_files_total": len(tracked),
            "vendored_files_excluded": len(vendored),
            "source_files": n_source,
            "files_by_tier": dict(files),
            "loc_by_tier": dict(loc),
            "loc_source_total": sum(loc.values()),
            "loc_code": loc["code"],
            "docs_loc_share_of_code_plus_docs": (
                round(loc["docs"] / (loc["code"] + loc["docs"]), 4)
                if (loc["code"] + loc["docs"]) else None
            ),
            "language_count": len(code_langs),
            "languages": dict(Counter(code_langs).most_common()),
            "files_missing_from_worktree": missing,
            "files_skipped_oversize": oversize,
        },
        "ait": {
            "estimator": ("LZMA-compressed size of tracked source files "
                          "concatenated in sorted-path order; a practical upper "
                          "bound on K(repo) (Kolmogorov 1965; Li & Vitanyi; the "
                          "compression-distance tradition of Cilibrasi & "
                          "Vitanyi 2005)"),
            "compressor": LZMA_SPEC,
            "raw_bytes_source": len(all_source),
            "compressed_bytes_source": len(comp_all),
            "compression_ratio_source": (
                round(len(comp_all) / len(all_source), 5) if all_source else None
            ),
            "raw_bytes_code": len(code_only),
            "compressed_bytes_code": len(comp_code),
            "compression_ratio_code": (
                round(len(comp_code) / len(code_only), 5) if code_only else None
            ),
        },
    }


# --------------------------------------------------------------------------
# 2. change entropy (Hassan, ICSE 2009)
# --------------------------------------------------------------------------

def _entropy(counter):
    """Shannon entropy in bits over a change-count distribution, plus the
    log2(n)-normalised value. Returns (H, H_norm, n_files, n_changes)."""
    total = sum(counter.values())
    n = len(counter)
    if total == 0 or n == 0:
        return None, None, n, total
    h = -sum((c / total) * math.log2(c / total) for c in counter.values())
    h_norm = round(h / math.log2(n), 4) if n > 1 else None
    return round(h, 4), h_norm, n, total


def change_entropy(commits):
    """H over the distribution of per-file change counts.

    Hassan's construction: within a period, p_i is file i's share of all file
    changes in that period; H = -sum p_i log2 p_i; normalised by log2(n) so
    periods with different file counts are comparable. High normalised entropy
    means change is spread evenly across many files (scattered, hard to reason
    about); low means it concentrates in a few.

    Degeneracy: with a single commit every file has exactly one change, so
    H_norm == 1.0 by construction and carries no information about the project.
    That case is flagged, not silently reported.
    """
    full = Counter()
    per_q = defaultdict(Counter)
    for c in commits:
        for _, _, _, new in c.files:
            if is_vendored(new) or not is_source(new):
                continue
            full[new] += 1
            per_q[c.quarter][new] += 1

    h, h_norm, n_files, n_changes = _entropy(full)
    quarters = []
    for q in sorted(per_q):
        qh, qhn, qn, qc = _entropy(per_q[q])
        quarters.append({"quarter": q, "entropy_bits": qh,
                         "entropy_normalised": qhn,
                         "files_changed": qn, "file_changes": qc})
    degenerate = len(commits) < 2
    return {
        "definition": ("Hassan (ICSE 2009) change entropy over per-file change "
                       "counts, normalised by log2(files changed); vendored and "
                       "non-source paths excluded"),
        "entropy_bits": h,
        "entropy_normalised": h_norm,
        "files_changed": n_files,
        "file_changes": n_changes,
        "degenerate": degenerate,
        "degenerate_note": (
            "n/a: history lost - a single (squashed) commit makes every file "
            "change exactly once, forcing H_norm to 1.0 by construction"
        ) if degenerate else None,
        "per_quarter": quarters,
    }


# --------------------------------------------------------------------------
# 3. coordination scope
# --------------------------------------------------------------------------

DECISION_PATH_RE = re.compile(
    r"(^|/)(decisions?|adr|adrs|rfc|rfcs)(/|$)|(^|/)[^/]*(ADR|DECISION|RFC)[^/]*\.", re.I
)
ID_PATTERNS = {
    "ADR": re.compile(r"\bADR-\d+\b"),
    "OQ": re.compile(r"\bOQ-\d+\b"),
    "KB": re.compile(r"\bKB-\d+\b"),
    "DD": re.compile(r"\bDD-\d+\b"),
    "INV": re.compile(r"\bINV-\d+\b"),
}


def coordination_scope(name, repo, commits, evidence):
    dirs_by_month = defaultdict(set)
    for c in commits:
        for _, _, _, new in c.files:
            if is_vendored(new) or not is_source(new):
                continue
            dirs_by_month[c.month].add(new.rsplit("/", 1)[0] if "/" in new else ".")
    per_month = [len(v) for _, v in sorted(dirs_by_month.items())]

    # --- decision records --------------------------------------------------
    tracked = [p for p in git(repo, "ls-files").splitlines() if p.strip()]
    record_files = [p for p in tracked
                    if not is_vendored(p) and DECISION_PATH_RE.search(p)]
    ids = {k: set() for k in ID_PATTERNS}
    for p in tracked:
        tier, _ = classify(p)
        if tier != "docs":
            continue
        fp = Path(repo) / p
        try:
            if fp.stat().st_size > MAX_FILE_BYTES:
                continue
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for k, rx in ID_PATTERNS.items():
            ids[k].update(rx.findall(text))

    # --- sessions from the WS0 evidence map --------------------------------
    hist = (evidence.get("claude_history") or {}).get(name, {})
    cop = (evidence.get("copilot") or {}).get(name, {})
    cc_keys = [k for k in (evidence.get("claude_code") or {})
               if k.rsplit("-", 1)[-1] == name or k.endswith("-" + name)]
    cc_sessions = sum(evidence["claude_code"][k]["sessions"] for k in cc_keys)

    hist_sessions = hist.get("sessions", 0)
    cop_sessions = cop.get("sessions", 0)

    span = round((commits[-1].ts - commits[0].ts) / DAY, 1) if len(commits) > 1 else 0.0
    return {
        "duration_days": span,
        "active_months": len(dirs_by_month),
        "first_commit": commits[0].iso[:10] if commits else None,
        "last_commit": commits[-1].iso[:10] if commits else None,
        "sessions_claude_history": hist_sessions,
        "sessions_copilot": cop_sessions,
        "sessions_claude_code_transcripts": cc_sessions,
        "sessions_total": hist_sessions + cop_sessions,
        "sessions_note": ("total = Claude Code global history + Copilot JetBrains "
                          "store; CC full transcripts are a SUBSET of CC history "
                          "(retention-trimmed) and are therefore not added again. "
                          "History log begins 2026-03-03, so any earlier session "
                          "is invisible - btest's Dec 2025-Feb 2026 era in "
                          "particular (STATE.md OQ-1)."),
        "distinct_dirs_per_active_month": {
            "mean": round(mean(per_month), 2) if per_month else None,
            "median": round(median(per_month), 2) if per_month else None,
            "max": max(per_month) if per_month else None,
            "series": per_month,
        },
        "decision_records": {
            "record_files": len(record_files),
            "record_file_paths": sorted(record_files)[:20],
            "distinct_ids": {k: len(v) for k, v in ids.items()},
            "decision_count": len(ids["ADR"]),
            "note": ("decision_count = distinct ADR-<n> identifiers found in "
                     "tracked docs; 0 means no decision-record instrument "
                     "exists, which is a finding, not a missing measurement"),
        },
    }


# --------------------------------------------------------------------------
# 4. direct dependencies
# --------------------------------------------------------------------------

PEP508_NAME_RE = re.compile(r"^\s*([A-Za-z0-9._-]+)")


def _pep508_name(spec):
    m = PEP508_NAME_RE.match(spec)
    return m.group(1).lower() if m else None


def _maven_deps(root, out):
    """Walk a POM, skipping <dependencyManagement> (those are version pins for
    transitive deps, not direct dependencies of the module)."""
    tag = root.tag.rsplit("}", 1)[-1]
    if tag == "dependencyManagement":
        return
    if tag == "dependency":
        g = a = None
        for ch in root:
            t = ch.tag.rsplit("}", 1)[-1]
            if t == "groupId":
                g = (ch.text or "").strip()
            elif t == "artifactId":
                a = (ch.text or "").strip()
        if a:
            out.add("%s:%s" % (g or "?", a))
        return
    for ch in root:
        _maven_deps(ch, out)


def dependencies(repo):
    tracked = [p for p in git(repo, "ls-files").splitlines()
               if p.strip() and not is_vendored(p)]
    py, mvn, npm = set(), set(), set()
    manifests = []

    for p in tracked:
        base = p.rsplit("/", 1)[-1]
        fp = Path(repo) / p
        if not fp.exists():
            continue
        try:
            if base == "pyproject.toml":
                manifests.append(p)
                data = tomllib.loads(fp.read_text(encoding="utf-8", errors="replace"))
                proj = data.get("project", {})
                for spec in proj.get("dependencies", []) or []:
                    n = _pep508_name(spec)
                    if n:
                        py.add(n)
                for group in (proj.get("optional-dependencies", {}) or {}).values():
                    for spec in group or []:
                        n = _pep508_name(spec)
                        if n:
                            py.add(n)
                for group in (data.get("dependency-groups", {}) or {}).values():
                    for spec in group or []:
                        if isinstance(spec, str):
                            n = _pep508_name(spec)
                            if n:
                                py.add(n)
                poetry = (data.get("tool", {}).get("poetry", {}) or {})
                for k in (poetry.get("dependencies", {}) or {}):
                    if k.lower() != "python":
                        py.add(k.lower())
            elif base == "pom.xml":
                manifests.append(p)
                _maven_deps(ET.parse(fp).getroot(), mvn)
            elif base == "package.json":
                manifests.append(p)
                data = json.loads(fp.read_text(encoding="utf-8", errors="replace"))
                npm.update(data.get("dependencies", {}) or {})
                npm.update(data.get("devDependencies", {}) or {})
        except Exception as exc:                      # a malformed manifest is data
            eprint("  warn: %s unparsed (%s)" % (p, exc.__class__.__name__))

    return {
        "python_direct": len(py),
        "maven_direct": len(mvn),
        "npm_direct": len(npm),
        "total_direct": len(py) + len(mvn) + len(npm),
        "manifests": sorted(manifests)[:20],
        "note": ("direct declared dependencies only; Maven "
                 "<dependencyManagement> pins and vendored manifests excluded"),
    }


# --------------------------------------------------------------------------
# 6. Kendall's W over the project ordering
# --------------------------------------------------------------------------

def _ranks_desc(values):
    """Average ranks, 1 = largest. Returns (ranks, tie_correction_T)."""
    order = sorted(range(len(values)), key=lambda i: -values[i])
    ranks = [0.0] * len(values)
    i = 0
    T = 0.0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        t = j - i + 1
        if t > 1:
            T += t ** 3 - t
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks, T


def _gser(a, x):
    ap, s, d = a, 1.0 / a, 1.0 / a
    for _ in range(1000):
        ap += 1
        d *= x / ap
        s += d
        if abs(d) < abs(s) * 1e-15:
            break
    return s * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _gcf(a, x):
    tiny = 1e-300
    b, c = x + 1.0 - a, 1.0 / tiny
    d = 1.0 / b if b else 1.0 / tiny
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        d = tiny if abs(d) < tiny else d
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def chi2_sf(x, df):
    """Upper tail of the chi-square distribution (regularised incomplete gamma)."""
    if x <= 0 or df <= 0:
        return 1.0
    a, xx = df / 2.0, x / 2.0
    return 1.0 - _gser(a, xx) if xx < a + 1.0 else _gcf(a, xx)


def kendalls_w(matrix, projects, label):
    """matrix: {primitive_name: {project: value}}. Missing values drop the
    primitive (a judge must rank every object)."""
    judges = {k: v for k, v in matrix.items()
              if all(v.get(p) is not None for p in projects)}
    dropped = sorted(set(matrix) - set(judges))
    m, n = len(judges), len(projects)
    if m < 2 or n < 3:
        return {"label": label, "status": "n/a: need >=2 primitives and >=3 projects",
                "primitives_used": sorted(judges), "primitives_dropped": dropped}

    rank_rows = {}
    rank_sums = {p: 0.0 for p in projects}
    T_total = 0.0
    for jname in sorted(judges):
        vals = [judges[jname][p] for p in projects]
        ranks, T = _ranks_desc(vals)
        T_total += T
        rank_rows[jname] = {p: ranks[i] for i, p in enumerate(projects)}
        for i, p in enumerate(projects):
            rank_sums[p] += ranks[i]

    rbar = m * (n + 1) / 2.0
    S = sum((rank_sums[p] - rbar) ** 2 for p in projects)
    denom = m * m * (n ** 3 - n) - m * T_total
    W = 12.0 * S / denom if denom > 0 else None
    chi2 = m * (n - 1) * W if W is not None else None
    return {
        "label": label,
        "projects": list(projects),
        "primitives_used": sorted(judges),
        "primitives_dropped": dropped,
        "n_projects": n,
        "n_primitives": m,
        "kendalls_w": round(W, 4) if W is not None else None,
        "chi_square": round(chi2, 3) if chi2 is not None else None,
        "df": n - 1,
        "p_value": round(chi2_sf(chi2, n - 1), 5) if chi2 is not None else None,
        "p_value_caveat": ("the chi-square approximation to W assumes n>7 objects; "
                           "with n=%d it is indicative only" % n),
        "rank_sums": {p: round(rank_sums[p], 1) for p in projects},
        "mean_rank": {p: round(rank_sums[p] / m, 2) for p in projects},
        "ordering_most_to_least_complex": sorted(projects, key=lambda p: rank_sums[p]),
        "rank_matrix": rank_rows,
    }


def stable_positions(orders):
    """Projects whose place is identical in every ordering.

    The sensitivity runs cover different project sets (one drops a
    single-commit repo), so positions are compared after restricting each
    ordering to the projects common to all of them - otherwise dropping one
    project would shift everything below it and read as instability.

    This is the list PLAN.md 4 WS-X licenses for the moderator analysis: only
    an ordering that survives every primitive choice is load-bearing.
    """
    if not orders:
        return []
    common = [p for p in orders[0] if all(p in o for o in orders)]
    restricted = [[p for p in o if p in common] for o in orders]
    return [p for p in common
            if len({o.index(p) for o in restricted}) == 1]


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

# The declared qualitative ratings of PLAN.md 4 WS-X(b) are AUTHOR JUDGMENT in
# the COCOMO cost-driver tradition and are never computed. They are emitted as
# nulls so the report cannot silently omit them and this script cannot fake them.
QUALITATIVE_TEMPLATE = {
    "_instruction": ("0-3 each, filled by Oleg, never computed. Narrative "
                     "placement only - explicitly excluded from Kendall's W and "
                     "from every number above."),
    "integration_surface": None,
    "constraint_tightness": None,
    "statefulness_concurrency": None,
    "_criteria": {
        "integration_surface": "0 none; 1 one file/data source; 2 one external "
                               "API or broker; 3 multiple live external systems",
        "constraint_tightness": "0 none; 1 soft correctness; 2 latency or "
                                "numerical-parity budget; 3 regulatory or "
                                "money-at-risk parity",
        "statefulness_concurrency": "0 pure batch; 1 cached state; 2 persistent "
                                    "state across runs; 3 concurrent live state",
    },
}


def profile(name, repo, evidence, qualitative=None):
    commits = read_log(repo)
    prof = {"project": name, "repo_path": str(repo)}
    prof.update(size_and_ait(repo))
    prof["change_entropy"] = change_entropy(commits)
    prof["coordination_scope"] = coordination_scope(name, repo, commits, evidence)
    prof["dependencies"] = dependencies(repo)

    # Declared ratings come from an INPUT file, never from computation, so a
    # re-run cannot silently wipe them back to null.
    q = dict(QUALITATIVE_TEMPLATE)
    supplied = ((qualitative or {}).get("ratings") or {}).get(name)
    if supplied:
        for k in ("integration_surface", "constraint_tightness",
                  "statefulness_concurrency"):
            q[k] = supplied.get(k)
        q["note"] = supplied.get("note")
        q["_source"] = "declared by author (data/qualitative-ratings.json)"
    prof["declared_qualitative"] = q
    return prof


def build_matrix(profiles):
    """The scalar primitives that act as judges in the concordance check.
    Every one is oriented so that LARGER == MORE COMPLEX."""
    g = lambda p, *ks: _dig(p, ks)
    return {
        "loc_source_total": {p["project"]: g(p, "size", "loc_source_total") for p in profiles},
        "source_files": {p["project"]: g(p, "size", "source_files") for p in profiles},
        "language_count": {p["project"]: g(p, "size", "language_count") for p in profiles},
        "ait_compressed_bytes": {p["project"]: g(p, "ait", "compressed_bytes_source") for p in profiles},
        "change_entropy_normalised": {p["project"]: g(p, "change_entropy", "entropy_normalised") for p in profiles},
        "duration_days": {p["project"]: g(p, "coordination_scope", "duration_days") for p in profiles},
        "sessions_total": {p["project"]: g(p, "coordination_scope", "sessions_total") for p in profiles},
        "dirs_per_active_month_mean": {p["project"]: g(p, "coordination_scope", "distinct_dirs_per_active_month", "mean") for p in profiles},
        "direct_dependencies": {p["project"]: g(p, "dependencies", "total_direct") for p in profiles},
    }


def _dig(d, keys):
    for k in keys:
        if d is None:
            return None
        d = d.get(k)
    return d


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
    ap.add_argument("--evidence-map", type=Path, required=True)
    ap.add_argument("--qualitative", type=Path, default=None,
                    help="declared WS-X(b) ratings (author judgment); omitted "
                         "leaves them null rather than inventing them")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--verification-note", default=None)
    args = ap.parse_args()

    evidence = json.loads(args.evidence_map.read_text(encoding="utf-8"))
    qualitative = (json.loads(args.qualitative.read_text(encoding="utf-8"))
                   if args.qualitative else None)

    profiles = []
    for name, repo in args.repo:
        try:
            profiles.append(profile(name, repo, evidence, qualitative))
        except Exception as exc:
            eprint("ERROR %s: %s" % (name, exc))
    names = [p["project"] for p in profiles]
    matrix = build_matrix(profiles)

    # Primary run, plus two sensitivity runs that answer the obvious objections:
    # (a) change entropy is degenerate for a squashed repo, (b) that repo may
    # be distorting the whole concordance.
    degenerate = [p["project"] for p in profiles if p["change_entropy"]["degenerate"]]
    concordance = {
        "primary": kendalls_w(matrix, names, "all projects, all primitives"),
        "sensitivity_no_entropy": kendalls_w(
            {k: v for k, v in matrix.items() if k != "change_entropy_normalised"},
            names, "change entropy dropped (degenerate for squashed histories)"),
    }
    if degenerate:
        keep = [n for n in names if n not in degenerate]
        concordance["sensitivity_excl_degenerate"] = kendalls_w(
            {k: {p: v[p] for p in keep} for k, v in matrix.items()}, keep,
            "excluding %s (single-commit history)" % ", ".join(degenerate))

    orders = [c["ordering_most_to_least_complex"] for c in concordance.values()
              if c.get("ordering_most_to_least_complex")]
    stable = stable_positions(orders)

    out = {
        "_meta": {
            "script": "complexity_profile.py",
            "version": VERSION,
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "git_version": git_version(),
            "python": sys.version.split()[0],
            "lzma_spec": LZMA_SPEC,
            "evidence_map": str(args.evidence_map),
            "design_rule": ("vector of primitives, never collapsed into a scalar "
                            "(PLAN.md 4 WS-X); no weights, concordance instead"),
            "verification": args.verification_note,
        },
        "profiles": {p["project"]: p for p in profiles},
        "primitive_matrix": matrix,
        "concordance": concordance,
        "ordering_stable_across_all_runs": stable,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)

    # --- ASCII summary (Windows console is cp1252) -------------------------
    print("%-11s %8s %7s %6s %8s %7s %7s %6s %6s" % (
        "project", "LOC", "files", "langs", "AIT_KB", "H_norm", "days", "sess", "deps"))
    print("-" * 76)
    for p in profiles:
        s, a, c, d = p["size"], p["ait"], p["coordination_scope"], p["dependencies"]
        hn = p["change_entropy"]["entropy_normalised"]
        print("%-11s %8d %7d %6d %8.1f %7s %7.0f %6d %6d" % (
            p["project"], s["loc_source_total"], s["source_files"],
            s["language_count"], a["compressed_bytes_source"] / 1024,
            ("%.3f*" % hn) if (hn is not None and p["change_entropy"]["degenerate"])
            else ("%.3f" % hn if hn is not None else "n/a"),
            c["duration_days"], c["sessions_total"], d["total_direct"]))
    if degenerate:
        print("* degenerate: single-commit history, H_norm is 1.0 by construction")
    print()
    for key, c in concordance.items():
        if c.get("kendalls_w") is None:
            continue
        print("Kendall W [%s]: W=%.3f  chi2=%.2f df=%d p=%.4f  (m=%d primitives)" % (
            c["label"], c["kendalls_w"], c["chi_square"], c["df"],
            c["p_value"], c["n_primitives"]))
        print("   order: " + " > ".join(c["ordering_most_to_least_complex"]))
    print("\nwrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
