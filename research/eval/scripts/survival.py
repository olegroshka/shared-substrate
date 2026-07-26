#!/usr/bin/env python3
"""WS5(a) decision survival: do decision records still describe the system?

Stdlib-only, read-only on the target repos (`git --no-optional-locks`), every
path parameterised, so the identical script runs inside a corporate environment
against P8 (PLAN.md 5).

==========================================================================
THE DEFINITION, FROZEN BEFORE THE MEASUREMENT WAS WRITTEN
==========================================================================

A decision record R asserts a decision D (or a fact F about the system).

  REVERSAL           the project's committed state ceases to conform to D:
                     a different choice is in force.

  DECLARED reversal  a reversal accompanied by MOVEMENT OF THE RECORD, i.e.
                     at least one of
                       D1  R's own status becomes SUPERSEDED-BY-* / DEPRECATED
                       D2  a later record R' carries `supersedes: R`
                       D3  R's body is edited to state the change
                       D4  an OQ resolution, retro or amendments-log entry
                           names R and records the change
                     This is the discipline WORKING. blive's substrate is
                     append-only with explicit supersedes, so a declared
                     reversal is a success, NOT a failure, and is never
                     counted as one. Getting this boundary wrong would make
                     the whole workstream measure the opposite of its subject.

  SILENT reversal    a reversal where NONE of D1-D4 occurred: the record still
                     asserts D, unmoved, while the repository asserts not-D.
                     This is the only event the survival curve treats as a
                     failure.

Explicitly NOT silent reversals:
  - refinement with a pointer.  A later record that narrows, parameterises or
    extends R while naming R (ADR-030 "amends ADR-010"; ADR-046 "refines
    ADR-032") has moved the record graph. Not a reversal.
  - non-implementation.  A decision not yet built is not a decision reversed.
  - a record the code has simply outgrown in scope, where the record says so.
    blive registers artefacts it has NOT written (CONTEXT_INVENTORY marks
    INV-2, INV-3, DD-4..6 MISSING); a declared absence is a receipt, not a gap.

Three DISTINCT divergence classes are counted, never pooled, because they are
different failures with different severities:

  SR-1  decision reversed         the choice recorded is not the choice in force
  SR-2  record-fact drift         the record's factual assertions about the
                                  system (counts, enumerations, paths, versions)
                                  are contradicted by the tree, with the record
                                  unmoved. The decision may still hold.
  SR-3  index/body incoherence    the substrate's own navigation surface
                                  disagrees with its own content (an index row
                                  whose status differs from the record body; a
                                  record absent from its own index).

And one INVERSE failure, which is not a reversal at all and is reported apart:

  MD-0  manufactured decision     a record states a decision that was never
                                  taken. Append-only discipline can create
                                  decisions as well as preserve them
                                  (WS4b finding 7, blive OQ-033).

WHAT THIS SCRIPT DECIDES AND WHAT IT DOES NOT
---------------------------------------------
SR-3 is fully machine-checkable and is computed here, with the session at which
each divergence OPENED, from git.

SR-1 and SR-2 are NOT decidable by script: they require reading a record and the
code it governs. They are therefore supplied from `--audit`, a hand-authored,
published INPUT file (the `qualitative-ratings.json` / `probes/scores.json`
pattern), so that re-running this script can never silently overwrite author
judgment and never silently invent it either. Every audit finding carries its
own file:line receipts and is verified by this script where mechanically
possible (`verified_receipts`).

SESSIONS
--------
"k subsequent sessions" needs a session. The log-derived session lists (WS3)
cover blive only from 2026-05-02, i.e. after 30 of its 70 commits and after 41
of its 53 ADRs, so they cannot carry this measurement. The session proxy here is
git-derived and therefore portable: a SESSION is a maximal run of consecutive
non-merge commits (author-date order) whose successive gaps are all <= G hours,
default G=4. Sensitivity at G in {2, 4, 8} is emitted, and the log-derived
session count is emitted alongside as a cross-check wherever WS3 has one.

CENSORING
---------
A record introduced in the second-to-last session cannot be observed for 10
subsequent sessions. Every survival point therefore publishes its `at_risk`
denominator: S(k) is computed only over records with at least k subsequent
sessions. No curve point may be read without it.

Usage:
  python survival.py --repo blive=C:/Users/olegr/PycharmProjects/blive \
                     --repo btest=C:/Users/olegr/PycharmProjects/btest \
                     --audit ../data/survival-audit.json \
                     --out ../data/survival.json
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
    eprint, git, git_version, read_log, redact_path,
)

VERSION = "1.0"
HOUR = 3600
DAY = 86400

# --------------------------------------------------------------------------
# Record shapes.
#
# Parameterised per repo so P8 can point this at its own layout; the defaults
# below are blive's, which is the only corpus project with a decision-record
# system at all. A repo with no decision file yields an empty ADR set and its
# survival curve is emitted as n/a rather than as zero (WS2 finding 8 pattern).
# --------------------------------------------------------------------------

DEFAULT_LAYOUT = {
    "decisions_file": "docs/decisions/DECISIONS.md",
    "questions_file": "docs/decisions/OPEN_QUESTIONS.md",
    "inventory_file": "CONTEXT_INVENTORY.md",
    "artifact_globs": ["docs/kb/*.md", "docs/inv/*.md", "docs/dd/*.md",
                       "docs/retros/*.md", "docs/decisions/*.md", "docs/*.md"],
    "instruction_files": ["CLAUDE.md", "AGENTS.md"],
    # Prose that is ABOUT the method rather than part of the substrate. Scanning
    # it for stable IDs produced a false "dangling ADR-12" from a paper draft
    # using a hypothetical identifier as an example; excluded and the exclusion
    # published rather than silently applied.
    "reference_scan_exclude": ["docs/method/"],
}

# `## ADR-007 - In-process event bus for v1`
ADR_HEAD_RE = re.compile(r"^##\s+(ADR-\d+)\s*[-\u2014\u2013]\s*(.+?)\s*$", re.M)
# `### OQ-031 - ...` and the combined form `### OQ-015 / OQ-018 - ...`, which
# blive uses for one question answered by one ADR. Reading only the first id
# reported OQ-018 as a dangling reference with 10 citations; it is not.
OQ_HEAD_RE = re.compile(
    r"^###\s+(OQ-\d+(?:\s*/\s*OQ-\d+)*)\s*[-\u2014\u2013]\s*(.+?)\s*$", re.M)
OQ_ID_RE = re.compile(r"OQ-\d+")
# `- **status:** ACCEPTED` / `- **supersedes:** ADR-021` (body field lines)
FIELD_RE = re.compile(r"^-\s+\*\*(\w+):\*\*\s*(.*?)\s*$", re.M)
# Index-table row: `| [ADR-021](#anchor) | title | SUPERSEDED-BY-ADR-043 | date | ... |`
INDEX_ROW_RE = re.compile(r"^\|\s*\[?(ADR-\d+)\]?[^|]*\|([^|]*)\|([^|]*)\|", re.M)

# The lifecycle vocabulary. Anything here at the head of a status value is the
# record having MOVED; the parenthetical prose blive attaches to several of its
# statuses ("ACCEPTED (drafted ... flipped ...)") is deliberately tolerated,
# since it is the record moving in the most explicit way the corpus contains.
STATUS_HEAD_RE = re.compile(
    r"^(SUPERSEDED-BY-ADR-\d+|SUPERSEDED|DEPRECATED|ACCEPTED|PROPOSED|REJECTED"
    r"|OPEN|RESOLVED-BY-ADR-\d+|RESOLVED|CLOSED|DRAFT|STABLE|MISSING)", re.I,
)
REVERSED_STATUS_RE = re.compile(r"^(SUPERSEDED|DEPRECATED)", re.I)

# YAML frontmatter of a substrate artefact.
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
FM_FIELD_RE = re.compile(r"^(\w+):\s*(.*?)\s*$", re.M)

# Any stable substrate ID, anywhere. The trailing negative lookahead stops
# `RETRO-M2-IB` from also matching as a reference to a non-existent `RETRO-M2`
# - which it did, 71 times, until the register was checked against `ls docs/`.
STABLE_ID_RE = re.compile(
    r"\b(ADR|KB|INV|DD|OQ|RETRO|RC)-([A-Za-z]?\d+(?:\.\d+)?)\b(?!-[A-Za-z])")

# A "rule" in an agent-instruction file: a markdown bullet with real content.
# btest's substrate is instructions, not decision records (WS4b finding 10), so
# this is the record type its arm of the comparison is actually measured on.
RULE_RE = re.compile(r"^\s*[-*]\s+(.{16,})$", re.M)

# --------------------------------------------------------------------------
# Reversal vocabulary for commit-message archaeology.
#
# Deliberately tight, and precedence-free (a message either announces undoing a
# prior choice or it does not). Loose matching was tried first and returned
# "mean-reverting ranks", "revert fast in absolute level" and a FRED tag note as
# reversals in btest; those false positives are what forced the word-boundary
# and negative-lookahead forms below. The published rate is per 100 commits so
# repo length does not drive it.
# --------------------------------------------------------------------------

REVERSAL_RES = {
    "revert": re.compile(r"\b(revert|reverted|reverting|reverts)\b(?!\w)", re.I),
    "rollback": re.compile(r"\b(roll(ed|ing)?[ -]?back|rollback)\b", re.I),
    "back_out": re.compile(r"\b(back(ed|ing)?[ -]out|undo|undid|undone)\b", re.I),
    "supersede": re.compile(r"\b(supersede[ds]?|superseding|obsolete[ds]?)\b", re.I),
    "abandon": re.compile(r"\b(abandon(ed|ing)?|scrap(ped|ping)?|give[ns]? up on)\b", re.I),
    "change_of_mind": re.compile(
        r"\b(changed? (our|my|the) mind|on second thought|reconsider(ed|ing)?"
        r"|earlier decision|previous(ly)? (decided|chosen|approach)"
        r"|no longer (the|our|valid|correct|used|using))\b", re.I),
    "replace_decision": re.compile(
        r"\b(replace[sd]?|switch(ed|ing)? (back|to)|instead of)\b", re.I),
}
# `replace` and `instead of` are the loose end of the lexicon: they fire on
# ordinary refactors ("replace 24 xfail stubs with real tests"). They are
# counted and reported SEPARATELY from the strict set so the headline number
# does not rest on them.
STRICT_REVERSAL_KEYS = ["revert", "rollback", "back_out", "supersede",
                        "abandon", "change_of_mind"]


# --------------------------------------------------------------------------
# sessions
# --------------------------------------------------------------------------

def sessionise(commits, gap_hours=4):
    """Maximal runs of commits with successive gaps <= gap_hours.

    Returns a list of sessions; each is {'index', 'commits': [Commit], ...}.
    Index is 1-based and monotonic in time, so `session_of[sha]` is directly
    the 'k sessions later' clock.
    """
    sessions = []
    cur = []
    for c in commits:
        if cur and (c.ts - cur[-1].ts) > gap_hours * HOUR:
            sessions.append(cur)
            cur = []
        cur.append(c)
    if cur:
        sessions.append(cur)
    out = []
    for i, grp in enumerate(sessions, 1):
        out.append({
            "index": i,
            "start": grp[0].iso[:16],
            "end": grp[-1].iso[:16],
            "commits": len(grp),
            "span_hours": round((grp[-1].ts - grp[0].ts) / HOUR, 2),
            "shas": [c.sha for c in grp],
        })
    return out


def session_index_map(sessions):
    m = {}
    for s in sessions:
        for sha in s["shas"]:
            m[sha] = s["index"]
    return m


# --------------------------------------------------------------------------
# record extraction from a blob at a given commit
# --------------------------------------------------------------------------

def blob(repo, sha, path):
    """File content at a commit, or None if it did not exist there."""
    out = git(repo, "show", "%s:%s" % (sha, path), check=False)
    return out if out else None


def commits_touching(repo, path):
    """Non-merge commit shas that touched `path`, oldest first."""
    out = git(repo, "log", "--no-merges", "--reverse", "--format=%H",
              "--follow", "--", path, check=False)
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def parse_adrs(text):
    """-> {id: {title, status, fields, body_span}} from a decisions file body."""
    if not text:
        return {}
    heads = list(ADR_HEAD_RE.finditer(text))
    out = {}
    for i, m in enumerate(heads):
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[start:end]
        fields = {k.lower(): v for k, v in FIELD_RE.findall(body[:1200])}
        out[m.group(1)] = {
            "title": m.group(2).strip(),
            "status": fields.get("status", ""),
            "date": fields.get("date", ""),
            "supersedes": fields.get("supersedes", ""),
            "resolves": fields.get("resolves", ""),
            "body_chars": len(body),
        }
    return out


def parse_oqs(text):
    """A combined heading (`### OQ-015 / OQ-018 - ...`) yields BOTH ids, each
    pointing at the same body, with `shared_with` naming the sibling."""
    if not text:
        return {}
    heads = list(OQ_HEAD_RE.finditer(text))
    out = {}
    for i, m in enumerate(heads):
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[start:end]
        fields = {k.lower(): v for k, v in FIELD_RE.findall(body[:1200])}
        ids = OQ_ID_RE.findall(m.group(1))
        for qid in ids:
            out[qid] = {
                "title": m.group(2).strip(),
                "status": fields.get("status", ""),
                "body_chars": len(body),
                "shared_with": [x for x in ids if x != qid],
            }
    return out


def parse_index_rows(text):
    """-> {id: status_as_the_index_claims_it} from the decisions file's index."""
    if not text:
        return {}
    rows = {}
    for m in INDEX_ROW_RE.finditer(text):
        aid, _title, status = m.group(1), m.group(2), m.group(3).strip()
        # Only the first (index) occurrence counts; later tables repeat ids.
        if aid not in rows:
            rows[aid] = status
    return rows


def status_head(value):
    """Normalise a status value to its leading lifecycle token."""
    m = STATUS_HEAD_RE.match((value or "").strip())
    return m.group(1).upper() if m else (value or "").strip().upper()


def parse_frontmatter(text):
    if not text:
        return None
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return {k.lower(): v for k, v in FM_FIELD_RE.findall(m.group(1))}


def parse_rules(text):
    """Agent-instruction rules -> {normalised_text: raw_text}."""
    if not text:
        return {}
    out = {}
    for m in RULE_RE.finditer(text):
        raw = m.group(1).strip()
        if raw.startswith("[") and "](" in raw:      # pure link list entry
            continue
        norm = re.sub(r"[^a-z0-9 ]+", " ", raw.lower())
        norm = " ".join(norm.split())
        if len(norm) >= 16:
            out.setdefault(norm, raw)
    return out


# --------------------------------------------------------------------------
# first-appearance mining
# --------------------------------------------------------------------------

def first_appearance(repo, path, parser, sessmap, all_commits_index):
    """For every key the parser yields, the commit/session it first appeared in.

    Walks only the commits that touched `path` (blive: ~30 of 70), reading each
    blob once. Cheaper and more exact than `git log -S` per record, and it also
    yields the per-record edit history for free.
    """
    touching = commits_touching(repo, path)
    first = {}          # key -> (sha, session)
    history = defaultdict(list)   # key -> [(sha, session, snapshot_dict)]
    prev = {}
    for sha in touching:
        text = blob(repo, sha, path)
        parsed = parser(text)
        sess = sessmap.get(sha)
        for key, val in parsed.items():
            if key not in first:
                first[key] = (sha, sess)
                history[key].append((sha, sess, val))
            elif prev.get(key) != val:
                history[key].append((sha, sess, val))
        prev = parsed
    return first, history, touching


# --------------------------------------------------------------------------
# survival curve
# --------------------------------------------------------------------------

def survival_curve(records, n_sessions, event_key, max_k=None):
    """Right-censored survival with a published at-risk denominator.

    records: list of {'id', 'first_session', event_key: session_or_None}
    S(k) = |{r : exposure(r) >= k and (event is None or event - first > k)}|
           / |{r : exposure(r) >= k}|
    """
    if not records:
        return []
    exposures = [n_sessions - r["first_session"] for r in records
                 if r["first_session"] is not None]
    if not exposures:
        return []
    top = max_k if max_k is not None else max(exposures)
    curve = []
    for k in range(0, top + 1):
        at_risk = [r for r in records
                   if r["first_session"] is not None
                   and (n_sessions - r["first_session"]) >= k]
        if not at_risk:
            break
        alive = [r for r in at_risk
                 if r.get(event_key) is None
                 or (r[event_key] - r["first_session"]) > k]
        curve.append({
            "k": k,
            "at_risk": len(at_risk),
            "alive": len(alive),
            "survival": round(len(alive) / len(at_risk), 4),
        })
    return curve


# --------------------------------------------------------------------------
# integrity checks (SR-3 and the record-graph audit)
# --------------------------------------------------------------------------

def index_coherence(repo, path, sessmap, adr_history):
    """SR-3: index rows vs record bodies, and records missing from the index.

    The session at which each divergence OPENED is recovered from the body
    history: it is the session in which the body's status last changed to the
    value the index still fails to show.
    """
    head_text = blob(repo, "HEAD", path)
    if not head_text:
        return None
    bodies = parse_adrs(head_text)
    index = parse_index_rows(head_text)

    missing_from_index = sorted(set(bodies) - set(index),
                                key=lambda x: int(x.split("-")[1]))
    absent_body = sorted(set(index) - set(bodies))

    mismatches = []
    for aid in sorted(set(bodies) & set(index), key=lambda x: int(x.split("-")[1])):
        b = status_head(bodies[aid]["status"])
        i = status_head(index[aid])
        if b == i:
            continue
        opened = None
        for sha, sess, snap in adr_history.get(aid, []):
            if status_head(snap.get("status", "")) == b:
                opened = {"session": sess, "sha": sha[:10]}
                break
        mismatches.append({
            "id": aid,
            "index_says": index[aid].strip(),
            "body_says": bodies[aid]["status"].strip()[:60],
            "divergence_opened": opened,
            "still_open_at_head": True,
        })

    # supersession graph: if A says SUPERSEDED-BY-B, does B claim `supersedes: A`?
    edges, broken = [], []
    for aid, rec in bodies.items():
        m = re.match(r"SUPERSEDED-BY-(ADR-\d+)", status_head(rec["status"]))
        if not m:
            continue
        target = m.group(1)
        back = bodies.get(target, {}).get("supersedes", "")
        ok = aid in back
        edges.append({"from": aid, "to": target, "backlink_present": ok})
        if not ok:
            broken.append({"id": aid, "claims_superseded_by": target,
                           "target_supersedes_field": back[:80]})

    return {
        "records_in_body": len(bodies),
        "records_in_index": len(index),
        "missing_from_index": missing_from_index,
        "in_index_but_no_body": absent_body,
        "status_mismatches": mismatches,
        "supersession_edges": edges,
        "supersession_edges_without_backlink": broken,
    }


def reference_integrity(repo, defined_ids, registered_ids, declared_missing, exclude=()):
    """Every stable ID referenced in tracked text, resolved against what exists.

    Three outcomes, never pooled:
      DEFINED     the artefact exists and was parsed
      REGISTERED  the project's own inventory carries a row for it but the file
                  is not written yet (MISSING, or DRAFT-inline-elsewhere). This
                  is a RECEIPT for a known gap, not a dangling pointer -
                  counting it as a defect would score blive's honesty about its
                  own holes as drift.
      DANGLING    referenced, not defined, not registered anywhere.
    """
    files = [p for p in git(repo, "ls-files").splitlines()
             if p.lower().endswith((".md", ".py", ".txt", ".yaml", ".yml", ".toml"))
             and not any(p.startswith(x) for x in exclude)]
    refs = Counter()
    where = defaultdict(set)
    for p in files:
        text = blob(repo, "HEAD", p)
        if not text:
            continue
        for m in STABLE_ID_RE.finditer(text):
            rid = "%s-%s" % (m.group(1), m.group(2))
            refs[rid] += 1
            where[rid].add(p)
    resolvable, declared, dangling = {}, {}, {}
    for rid, n in refs.items():
        if rid in defined_ids:
            resolvable[rid] = n
        elif rid in registered_ids:
            declared[rid] = n
        else:
            dangling[rid] = n
    # Only ID families the project actually operates are meaningful as dangling.
    families = {rid.split("-")[0] for rid in defined_ids} | {"ADR", "OQ", "KB", "INV", "DD"}
    dangling = {k: v for k, v in dangling.items() if k.split("-")[0] in families}
    return {
        "files_scanned": len(files),
        "files_excluded_from_scan": sorted(exclude),
        "distinct_ids_referenced": len(refs),
        "resolvable": len(resolvable),
        "registered_but_unwritten_referenced": sorted(declared),
        "dangling": dict(sorted(dangling.items(), key=lambda kv: (-kv[1], kv[0]))[:25]),
        "dangling_count": len(dangling),
        "dangling_locations": {k: sorted(where[k])[:4] for k in dangling},
        "unreferenced_records": sorted(
            rid for rid in defined_ids
            if refs.get(rid, 0) <= 1 and rid.startswith("ADR-")
        ),
    }


# GitHub heading-anchor slug: lowercase, drop punctuation other than hyphen and
# underscore, spaces -> hyphens. An APPROXIMATION of GitHub's exact algorithm
# (it is not published as a spec); a link this check calls broken is re-read by
# hand before it enters any finding.
def gh_slug(heading):
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.U)
    # EACH space becomes a hyphen; collapsing runs first (the initial version)
    # turned the double hyphen every `ADR-NNN - Title` heading produces into a
    # single one and called 758 of 900 anchors broken. The corpus's real broken
    # count is two orders of magnitude smaller.
    return re.sub(r"\s", "-", s).strip("-")


HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
MD_LINK_RE = re.compile(r"\]\(([^)\s]*?)#([^)\s]+)\)")


def anchor_integrity(repo, exclude=()):
    """Markdown intra-substrate links whose #anchor does not resolve.

    A stable-ID reference can be perfectly resolvable while the LINK carrying it
    is broken - which is the failure a reader actually hits. blive's ADR-015
    resolves-field links OQ-015 to `#oq-015--ml-model-training...`, but that
    question shares a combined heading with OQ-018, so the real anchor is
    `#oq-015--oq-018--...`. Counted apart from dangling IDs.
    """
    files = [p for p in git(repo, "ls-files").splitlines()
             if p.lower().endswith(".md")
             and not any(p.startswith(x) for x in exclude)]
    slugs = {}
    for p in files:
        text = blob(repo, "HEAD", p) or ""
        counts = Counter()
        s = set()
        for h in HEADING_RE.findall(text):
            base = gh_slug(h)
            counts[base] += 1
            s.add(base if counts[base] == 1 else "%s-%d" % (base, counts[base] - 1))
        slugs[p] = s
    broken, checked = [], 0
    for p in files:
        text = blob(repo, "HEAD", p) or ""
        base_dir = p.rsplit("/", 1)[0] if "/" in p else ""
        for m in MD_LINK_RE.finditer(text):
            target, anchor = m.group(1), m.group(2)
            if target.startswith(("http://", "https://")):
                continue
            if not target:                       # same-file anchor
                tpath = p
            else:
                tpath = target if target.startswith("docs/") or "/" not in p else \
                    "/".join(filter(None, (base_dir + "/" + target).split("/")))
                tpath = re.sub(r"[^/]+/\.\./", "", tpath)
                tpath = tpath.lstrip("./")
            if tpath not in slugs:
                continue                          # target outside the md set
            checked += 1
            if anchor.lower() not in slugs[tpath]:
                broken.append({"file": p, "target": tpath, "anchor": anchor[:70]})
    distinct = Counter((b["target"], b["anchor"]) for b in broken)
    return {
        "anchors_checked": checked,
        "broken_count": len(broken),
        "broken_share": round(len(broken) / checked, 4) if checked else None,
        # The headline is DISTINCT broken targets, not occurrences: in blive two
        # malformed anchors account for 20 of 26 hits because a wrong
        # cross-reference gets copied forward rather than corrected. Reporting
        # occurrences alone would read as 26 independent defects.
        "distinct_broken_targets": len(distinct),
        "distinct_broken": [{"target": t, "anchor": a, "occurrences": n}
                            for (t, a), n in distinct.most_common()],
        "broken": broken[:30],
        "note": ("slug rule is an approximation of GitHub's unpublished "
                 "algorithm; every finding derived from this list is re-read "
                 "by hand before it is published"),
    }


def freshness_clock(repo, artifacts, sessmap):
    """An artefact whose `last_reviewed` predates its own last commit is a
    record that moved without its freshness marker moving. Reported as a count
    plus the offending list; it is a weak signal on its own (a typo fix moves
    the file without touching what the record asserts), so the DAYS of lag are
    published rather than a bare flag."""
    rows = []
    for path, fm in artifacts.items():
        lr = (fm or {}).get("last_reviewed", "")
        if not re.match(r"\d{4}-\d{2}-\d{2}", lr or ""):
            continue
        out = git(repo, "log", "-1", "--format=%aI", "--", path, check=False).strip()
        if not out:
            continue
        last_commit = out[:10]
        if last_commit > lr[:10]:
            d0 = datetime.strptime(lr[:10], "%Y-%m-%d")
            d1 = datetime.strptime(last_commit, "%Y-%m-%d")
            rows.append({"path": path, "id": fm.get("id", ""),
                         "last_reviewed": lr[:10], "last_commit": last_commit,
                         "lag_days": (d1 - d0).days})
    rows.sort(key=lambda r: -r["lag_days"])
    return {"artifacts_with_last_reviewed": sum(
        1 for fm in artifacts.values()
        if re.match(r"\d{4}-\d{2}-\d{2}", (fm or {}).get("last_reviewed", "") or "")),
        "stale_marker_count": len(rows), "stale_markers": rows}


# --------------------------------------------------------------------------
# commit-message reversal archaeology (P2's arm)
# --------------------------------------------------------------------------

def reversal_archaeology(repo, commits, sessmap):
    """How often does the commit log ANNOUNCE undoing an earlier choice?

    This is the only decision surface a repo without decision records has. Two
    counts are published: the strict lexicon, and the strict lexicon plus the
    loose `replace`/`instead of` forms which fire on ordinary refactors.
    """
    strict_hits, loose_hits = [], []
    per_kind = Counter()
    total_words = 0
    bodied = 0
    for c in commits:
        full = git(repo, "log", "-1", "--format=%s%n%b", c.sha, check=False)
        # The substrate's own field syntax is not a claim: an ADR block pasted
        # into a commit body carries a literal `- **supersedes:** none` line.
        prose = re.sub(r"^\s*[-*]?\s*\**supersede[sd]?\**\s*:.*$", "", full,
                       flags=re.M | re.I)
        total_words += len(prose.split())
        if len(full) > len(c.subject) + 2:
            bodied += 1
        kinds = [k for k, rx in REVERSAL_RES.items() if rx.search(prose)]
        if not kinds:
            continue
        rec = {
            "sha": c.sha[:10], "date": c.iso[:10], "session": sessmap.get(c.sha),
            "kinds": kinds,
            "subject": c.subject[:120],
            "body_chars": max(0, len(full) - len(c.subject)),
        }
        for k in kinds:
            per_kind[k] += 1
        if any(k in STRICT_REVERSAL_KEYS for k in kinds):
            strict_hits.append(rec)
        else:
            loose_hits.append(rec)
    n = len(commits)
    return {
        "commits": n,
        "commits_with_a_body": bodied,
        # Rate per 100 commits is confounded by how much prose a project writes
        # per commit: a repo whose bodies average 40 words cannot express a
        # reversal it never narrates. Both denominators are published.
        "commit_prose_words": total_words,
        "mean_prose_words_per_commit": round(total_words / n, 1) if n else None,
        "strict_reversal_commits": len(strict_hits),
        "strict_rate_per_100_commits": round(100 * len(strict_hits) / n, 2) if n else None,
        "strict_rate_per_10k_prose_words": (
            round(10000 * len(strict_hits) / total_words, 2) if total_words else None),
        "loose_only_commits": len(loose_hits),
        "loose_rate_per_100_commits": round(100 * len(loose_hits) / n, 2) if n else None,
        "by_kind": dict(per_kind.most_common()),
        "strict_examples": strict_hits[:20],
        "loose_examples": loose_hits[:15],
    }


# --------------------------------------------------------------------------
# instruction-rule survival (P2's actual record type)
# --------------------------------------------------------------------------

def instruction_rule_survival(repo, paths, sessmap, n_sessions):
    """btest's substrate is a 212-line agent-instruction file, not decision
    records (WS4b finding 10). Its arm of this comparison is therefore measured
    on the record type it HAS: how long does a stated rule survive, and when a
    rule disappears, does anything say so?

    A rule is a markdown bullet of >=16 informative characters. Rules are
    matched on a case- and punctuation-normalised form, so rewording counts as
    removal-plus-addition; that is conservative in the direction of shorter
    survival and is stated rather than corrected for.
    """
    out = {}
    for path in paths:
        touching = commits_touching(repo, path)
        if not touching:
            continue
        seen_first, seen_last, texts = {}, {}, {}
        removals = []
        prev = set()
        for sha in touching:
            rules = parse_rules(blob(repo, sha, path))
            cur = set(rules)
            for r in cur:
                if r not in seen_first:
                    seen_first[r] = sha
                    texts[r] = rules[r]
                seen_last[r] = sha
            gone = prev - cur
            if gone:
                msg = git(repo, "log", "-1", "--format=%s%n%b", sha, check=False)
                # A rule dropped alongside many others in one commit is a SCOPE
                # change (btest's SMIM extraction withdrew 24 SMIM rules at
                # once, and the commit subject says so). Scoring those the same
                # as an isolated silent drop would have made btest look far
                # worse than it is; the bulk size travels with every removal.
                bulk = len(gone)
                for r in sorted(gone):
                    # Did the removing commit mention any distinctive token of
                    # the rule it deleted? 5+ char words, ignoring boilerplate.
                    toks = [w for w in re.findall(r"[A-Za-z_]{5,}", texts.get(r, r))
                            if w.lower() not in
                            ("should", "always", "never", "every", "which", "there",
                             "these", "those", "using", "under", "before", "after")]
                    named = sum(1 for w in set(toks) if re.search(
                        r"\b%s\b" % re.escape(w), msg, re.I))
                    removals.append({
                        "sha": sha[:10], "session": sessmap.get(sha),
                        "rule": texts.get(r, r)[:120],
                        "distinct_tokens": len(set(toks)),
                        "tokens_named_in_commit_message": named,
                        "rules_removed_in_same_commit": bulk,
                        "bulk_scope_change": bulk >= 5,
                        "announced": named >= 2,
                    })
            prev = cur
        head_rules = set(parse_rules(blob(repo, "HEAD", path)))
        records = []
        for r, sha in seen_first.items():
            fs = sessmap.get(sha)
            ev = None
            if r not in head_rules:
                for rem in removals:
                    if rem["rule"][:60] == texts.get(r, r)[:60]:
                        ev = rem["session"]
                        break
            records.append({"id": r[:60], "first_session": fs, "removed_session": ev})
        isolated = [r for r in removals if not r["bulk_scope_change"]]
        out[path] = {
            "versions": len(touching),
            "rules_ever_stated": len(seen_first),
            "rules_at_head": len(head_rules),
            "rules_removed": len(removals),
            "removals_announced_in_commit_message": sum(
                1 for r in removals if r["announced"]),
            "bulk_scope_removals": len(removals) - len(isolated),
            "isolated_removals": len(isolated),
            "isolated_removals_announced": sum(1 for r in isolated if r["announced"]),
            "removals": removals[:40],
            "survival_curve": survival_curve(records, n_sessions, "removed_session"),
        }
    return out


# --------------------------------------------------------------------------
# per-repo driver
# --------------------------------------------------------------------------

def analyse(name, repo, layout, audit, gap_hours, gap_sensitivity):
    commits = read_log(repo)
    if not commits:
        return {"_meta": {"project": name}, "status": "n/a: empty history"}

    sessions = sessionise(commits, gap_hours)
    sessmap = session_index_map(sessions)
    n_sessions = len(sessions)

    sens = {}
    for g in gap_sensitivity:
        sens["gap_%dh" % g] = len(sessionise(commits, g))

    result = {
        "sessions": {
            "definition": ("maximal run of consecutive non-merge commits whose "
                           "successive gaps are all <= %d hours" % gap_hours),
            "gap_hours": gap_hours,
            "session_count": n_sessions,
            "sensitivity_session_counts": sens,
            "first": sessions[0]["start"] if sessions else None,
            "last": sessions[-1]["end"] if sessions else None,
            "commits": len(commits),
            "sessions": [{k: v for k, v in s.items() if k != "shas"} for s in sessions],
        },
    }

    # ---- decision records -------------------------------------------------
    dec_path = layout.get("decisions_file")
    has_decisions = bool(dec_path and blob(repo, "HEAD", dec_path))
    if not has_decisions:
        result["decision_records"] = {
            "status": "n/a: no decision-record system in this repo",
            "note": ("This project has no ADR/decision file. Its arm of WS5 is "
                     "the commit-message archaeology and the instruction-rule "
                     "survival below - a different substrate type, not a zero "
                     "on a shared denominator (WS2 finding 8 pattern)."),
            "searched_for": dec_path,
        }
        adr_ids = set()
    else:
        first_adr, adr_hist, dec_commits = first_appearance(
            repo, dec_path, parse_adrs, sessmap, None)
        head_adrs = parse_adrs(blob(repo, "HEAD", dec_path))
        adr_ids = set(head_adrs)

        audit_events = {}
        for f in audit.get("findings", []):
            if f.get("project") != name:
                continue
            for rid in f.get("records", []):
                if f.get("class") in ("SR-1", "SR-2"):
                    audit_events.setdefault(rid, f.get("opened_session"))

        records = []
        for aid, meta in sorted(head_adrs.items(), key=lambda kv: int(kv[0].split("-")[1])):
            sha, sess = first_adr.get(aid, (None, None))
            st = status_head(meta["status"])
            declared_sess = None
            if REVERSED_STATUS_RE.match(st):
                for h_sha, h_sess, snap in adr_hist.get(aid, []):
                    if REVERSED_STATUS_RE.match(status_head(snap.get("status", ""))):
                        declared_sess = h_sess
                        break
            records.append({
                "id": aid,
                "title": meta["title"][:90],
                "status": meta["status"][:70],
                "status_head": st,
                "first_session": sess,
                "first_sha": sha[:10] if sha else None,
                "sessions_exposed": (n_sessions - sess) if sess else None,
                "edits_after_introduction": max(0, len(adr_hist.get(aid, [])) - 1),
                "declared_reversal_session": declared_sess,
                "silent_reversal_session": audit_events.get(aid),
            })

        never_touched = [r["id"] for r in records
                         if r["edits_after_introduction"] == 0
                         and (r["sessions_exposed"] or 0) >= 3]

        result["decision_records"] = {
            "file": dec_path,
            "file_versions": len(dec_commits),
            "records": len(records),
            "status_counts": dict(Counter(r["status_head"] for r in records).most_common()),
            "declared_reversals": [
                {"id": r["id"], "status": r["status"][:60],
                 "session": r["declared_reversal_session"]}
                for r in records if r["declared_reversal_session"] is not None
            ],
            "declared_reversal_count": sum(
                1 for r in records if r["declared_reversal_session"] is not None),
            "silent_reversal_count": sum(
                1 for r in records if r["silent_reversal_session"] is not None),
            "never_edited_after_introduction": {
                "count": len(never_touched),
                "share": round(len(never_touched) / len(records), 4) if records else None,
                "ids": never_touched,
                "note": ("candidates for hand audit, not findings: a record "
                         "never revisited is where a silent reversal would hide. "
                         "Only >=3 sessions of exposure are listed."),
            },
            "survival_silent": survival_curve(records, n_sessions, "silent_reversal_session"),
            "survival_declared": survival_curve(records, n_sessions, "declared_reversal_session"),
            "per_record": records,
        }
        result["index_coherence"] = index_coherence(repo, dec_path, sessmap, adr_hist)

    # ---- open questions ---------------------------------------------------
    q_path = layout.get("questions_file")
    if q_path and blob(repo, "HEAD", q_path):
        first_oq, oq_hist, q_commits = first_appearance(
            repo, q_path, parse_oqs, sessmap, None)
        head_oqs = parse_oqs(blob(repo, "HEAD", q_path))
        rows = []
        for qid, meta in sorted(head_oqs.items(), key=lambda kv: int(kv[0].split("-")[1])):
            sha, sess = first_oq.get(qid, (None, None))
            rows.append({"id": qid, "title": meta["title"][:80],
                         "status": meta["status"][:40], "first_session": sess,
                         "edits_after_introduction": max(0, len(oq_hist.get(qid, [])) - 1)})
        result["open_questions"] = {
            "file": q_path, "records": len(rows),
            "status_counts": dict(Counter(status_head(r["status"]) for r in rows).most_common()),
            "per_record": rows,
        }
        adr_ids |= set(head_oqs)

    # ---- frontmatter artefacts -------------------------------------------
    artifacts = {}
    seen_paths = set()
    for pattern in layout.get("artifact_globs", []):
        pat = pattern.replace("*", "[^/]*")
        rx = re.compile("^%s$" % pat)
        for p in git(repo, "ls-files").splitlines():
            if p in seen_paths or not rx.match(p):
                continue
            fm = parse_frontmatter(blob(repo, "HEAD", p))
            if fm and fm.get("id"):
                artifacts[p] = fm
                seen_paths.add(p)
    if artifacts:
        adr_ids |= {fm["id"] for fm in artifacts.values() if fm.get("id")}
        result["artifacts"] = {
            "count": len(artifacts),
            "status_counts": dict(Counter(
                status_head(fm.get("status", "")) for fm in artifacts.values()).most_common()),
            "freshness": freshness_clock(repo, artifacts, sessmap),
            "per_artifact": [
                {"path": p, "id": fm.get("id"), "status": fm.get("status"),
                 "version": fm.get("version"), "last_reviewed": fm.get("last_reviewed")}
                for p, fm in sorted(artifacts.items())
            ],
        }

    # ---- declared-missing register + reference integrity ------------------
    # A row of the inventory table registers ONE artefact: its id is in the
    # first cell and its status in the third. Scanning the whole line for ids
    # (the first implementation) swept up every id merely NAMED beside a MISSING
    # one and reported KB-2, KB-3, DD-7 and ADR-034 as declared-missing when all
    # four exist. Caught by hand-checking the register against `ls docs/`.
    declared_missing, registered = set(), set()
    inv_path = layout.get("inventory_file")
    if inv_path:
        inv = blob(repo, "HEAD", inv_path)
        if inv:
            for line in inv.splitlines():
                cells = [c.strip() for c in line.split("|")]
                if len(cells) < 4:
                    continue
                m = STABLE_ID_RE.search(cells[1])
                if not m:
                    continue
                rid = "%s-%s" % (m.group(1), m.group(2))
                registered.add(rid)
                if "MISSING" in cells[3].upper():
                    declared_missing.add(rid)
    exclude = tuple(layout.get("reference_scan_exclude", []))
    if adr_ids or registered:
        ri = reference_integrity(repo, adr_ids, registered, declared_missing, exclude)
        ri["inventory_registered_ids"] = len(registered)
        ri["declared_missing_register"] = sorted(declared_missing)
        ri["declared_missing_count"] = len(declared_missing)
        ri["note"] = ("an ID the project's own inventory registers - whether "
                      "MISSING or planned-elsewhere - is a receipt for a known "
                      "gap, counted apart from dangling references")
        result["reference_integrity"] = ri
    result["anchor_integrity"] = anchor_integrity(repo, exclude)

    # ---- P2's arms --------------------------------------------------------
    result["reversal_archaeology"] = reversal_archaeology(repo, commits, sessmap)
    instr = [p for p in layout.get("instruction_files", [])
             if blob(repo, "HEAD", p) or commits_touching(repo, p)]
    if instr:
        result["instruction_rules"] = instruction_rule_survival(
            repo, instr, sessmap, n_sessions)

    # ---- hand-audit findings for this project -----------------------------
    mine = [f for f in audit.get("findings", []) if f.get("project") == name]
    result["hand_audit"] = {
        "findings": len(mine),
        "by_class": dict(Counter(f.get("class") for f in mine).most_common()),
        "detail": mine,
    }
    return result


# --------------------------------------------------------------------------
# receipt verification
# --------------------------------------------------------------------------

def verify_receipts(repos, audit):
    """Re-check every mechanically checkable claim in the audit input.

    An audit finding that asserts 'file X line L contains T' is re-read from the
    repo here. A finding whose receipt does not hold is reported FAILED, not
    dropped and not corrected (the S5 void-and-report rule).
    """
    rows = []
    for f in audit.get("findings", []):
        repo = repos.get(f.get("project"))
        if not repo:
            continue
        for rc in f.get("receipts", []):
            path, needle = rc.get("path"), rc.get("contains")
            if not path or needle is None:
                continue
            text = blob(repo, "HEAD", path)
            ok = bool(text) and needle in text
            rows.append({"finding": f.get("id"), "path": path,
                         "contains": needle[:70], "holds": ok})
    return {
        "checked": len(rows),
        "held": sum(1 for r in rows if r["holds"]),
        "failed": [r for r in rows if not r["holds"]],
        "detail": rows,
    }


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

DEFINITIONS = {
    "session": ("maximal run of consecutive non-merge commits (author-date "
                "order) whose successive gaps are all <= G hours, G=4 by "
                "default; sensitivity at G in {2,4,8} published. Git-derived "
                "because WS3's log-derived sessions start 2026-05-02 and miss "
                "41 of blive's 53 ADRs"),
    "declared_reversal": ("record moved: status became SUPERSEDED-BY-*/DEPRECATED, "
                          "or a later record carries `supersedes:` pointing at it. "
                          "The discipline working - never counted as a failure"),
    "silent_reversal": ("record did NOT move while the repository asserts the "
                        "contrary. The only failure event in the survival curve. "
                        "Supplied from the hand-audit input, never inferred"),
    "SR-1": "decision reversed - the recorded choice is not the choice in force",
    "SR-2": ("record-fact drift - the record's factual assertions (counts, "
             "enumerations, paths, versions) are contradicted by the tree"),
    "SR-3": ("index/body incoherence - the substrate's navigation surface "
             "disagrees with its own content; fully machine-checked here"),
    "MD-0": ("manufactured decision - a record states a decision never taken; "
             "the inverse failure, reported apart from every reversal count"),
    "survival_curve": ("S(k) over records with at least k subsequent sessions; "
                       "at_risk is published at every k because a record born in "
                       "the last session cannot be observed for k>0"),
    "declared_missing": ("an ID the project's own inventory registers as MISSING - "
                         "a receipt for a known gap, never counted as a dangling "
                         "reference"),
    "instruction_rules": ("markdown bullets of >=16 informative characters in an "
                          "agent-instruction file, normalised for case and "
                          "punctuation; rewording counts as removal + addition, "
                          "which biases survival DOWN and is not corrected for"),
    "reversal_archaeology": ("commits whose subject or body announces undoing an "
                             "earlier choice; strict lexicon (revert/rollback/"
                             "back out/supersede/abandon/change-of-mind) reported "
                             "apart from the loose replace/instead-of forms, which "
                             "fire on ordinary refactors"),
}


def build_summary(projects, audit):
    """One readable block, so no headline needs reconstructing from the tree."""
    rows = {}
    for name, res in projects.items():
        dr = res.get("decision_records", {})
        ic = res.get("index_coherence") or {}
        ai = res.get("anchor_integrity") or {}
        ra = res.get("reversal_archaeology", {})
        instr = res.get("instruction_rules") or {}
        mine = [f for f in audit.get("findings", []) if f.get("project") == name]
        cls = Counter(f.get("class") for f in mine)
        rows[name] = {
            "sessions_gap_4h": res.get("sessions", {}).get("session_count"),
            "decision_records": dr.get("records", "n/a: no decision-record system"),
            "declared_reversals": dr.get("declared_reversal_count", "n/a"),
            "silent_reversals_of_decision_records": dr.get("silent_reversal_count", "n/a"),
            "SR-1_decision_reversed": cls.get("SR-1", 0),
            "SR-2_record_fact_drift": cls.get("SR-2", 0),
            "SR-3_index_incoherence": (
                len(ic.get("status_mismatches", [])) + len(ic.get("missing_from_index", []))
                + len(ic.get("supersession_edges_without_backlink", []))
                if ic else "n/a"),
            "MD-0_manufactured_decisions": cls.get("MD-0", 0),
            "broken_anchor_targets": ai.get("distinct_broken_targets"),
            "broken_anchor_occurrences": ai.get("broken_count"),
            "dangling_id_references": (res.get("reference_integrity") or {}).get("dangling_count", "n/a"),
            "reversal_commits_strict_automated": ra.get("strict_reversal_commits"),
            "reversal_rate_per_100_commits": ra.get("strict_rate_per_100_commits"),
            "reversal_rate_per_10k_prose_words": ra.get("strict_rate_per_10k_prose_words"),
            "mean_commit_prose_words": ra.get("mean_prose_words_per_commit"),
            "instruction_rules_at_head": sum(
                v.get("rules_at_head", 0) for v in instr.values()) or "n/a",
            "instruction_rules_removed": sum(
                v.get("rules_removed", 0) for v in instr.values()) or "n/a",
            "instruction_rule_isolated_removals": sum(
                v.get("isolated_removals", 0) for v in instr.values()) or "n/a",
        }
    return {
        "per_project": rows,
        "read_this_first": [
            "The survival curve proper has ONE arm: blive is the only corpus "
            "project with decision records. btest's arm is a different substrate "
            "type (agent instructions + commit prose), reported as such rather "
            "than as a zero on a shared denominator.",
            "ZERO blive ADRs were found silently reversed. That is the honest "
            "headline and it is the cheap number PLAN section 4 predicted; the "
            "informative findings are elsewhere - in the index, the anchors, and "
            "the one open question that was wrong on the day it was written.",
            "Every declared reversal is the discipline WORKING and is never "
            "counted as a failure. blive has exactly one (ADR-021 -> ADR-043) and "
            "it is declared on both ends.",
            "Survival points must be read with their at_risk denominator: "
            "blive's k=12 point rests on 26 records, not 53.",
        ],
    }


BUGS_CAUGHT_BY_VERIFICATION = [
    ("The declared-MISSING register scanned each inventory LINE for stable ids "
     "instead of the row's first CELL, so every id merely named beside a MISSING "
     "one was registered as missing too - KB-2, KB-3, DD-7 and ADR-034 all exist. "
     "Caught by reading the register against `ls docs/`."),
    ("STABLE_ID_RE had no trailing boundary, so `RETRO-M2-IB` also matched as a "
     "reference to a non-existent `RETRO-M2` - 71 phantom dangling references, "
     "the single largest number in the first draft of this output."),
    ("gh_slug collapsed whitespace RUNS to one hyphen before substituting, but "
     "GitHub's slugger substitutes EACH space. Every `## ADR-NNN - Title` heading "
     "produces a double hyphen, so the first anchor pass called 758 of 900 links "
     "broken. The true count is 26 occurrences over 7 distinct targets."),
    ("parse_oqs read only the first id of a heading, so blive's combined "
     "`### OQ-015 / OQ-018 - ...` question made OQ-018 look like a dangling "
     "reference with 10 citations. It is a deliberate shared resolution."),
]


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
    ap.add_argument("--audit", type=Path, default=None,
                    help="hand-authored SR-1/SR-2/MD-0 findings (published INPUT)")
    ap.add_argument("--layout", type=Path, default=None,
                    help="JSON {project: {decisions_file, ...}} overriding defaults")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--session-gap-hours", type=int, default=4)
    ap.add_argument("--verification-note", default=None)
    args = ap.parse_args()

    audit = {"findings": []}
    if args.audit and args.audit.exists():
        with open(args.audit, "r", encoding="utf-8") as fh:
            audit = json.load(fh)

    layouts = {}
    if args.layout and args.layout.exists():
        with open(args.layout, "r", encoding="utf-8") as fh:
            layouts = json.load(fh)

    repos = dict(args.repo)
    out = {
        "_meta": {
            "workstream": "WS5(a) decision survival",
            "script": "survival.py",
            "version": VERSION,
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "git_version": git_version(),
            "session_gap_hours": args.session_gap_hours,
            "definitions": DEFINITIONS,
            "audit_input": str(args.audit) if args.audit else None,
            "audit_input_is_published_author_judgment": True,
            "verification": args.verification_note,
            "bugs_caught_by_verification": BUGS_CAUGHT_BY_VERIFICATION,
        },
        "projects": {},
    }

    print("%-12s %6s %6s %6s %7s %8s %9s" % (
        "project", "sess", "ADRs", "decl", "silent", "SR-3", "revert/100"))
    print("-" * 62)
    for name, repo in args.repo:
        layout = dict(DEFAULT_LAYOUT)
        layout.update(layouts.get(name, {}))
        try:
            res = analyse(name, repo, layout, audit, args.session_gap_hours, (2, 4, 8))
        except Exception as exc:
            eprint("ERROR %s: %s" % (name, exc))
            continue
        res["_repo_path"] = redact_path(repo)
        out["projects"][name] = res
        dr = res.get("decision_records", {})
        ic = res.get("index_coherence") or {}
        ra = res.get("reversal_archaeology", {})
        sr3 = (len(ic.get("status_mismatches", []))
               + len(ic.get("missing_from_index", []))
               + len(ic.get("supersession_edges_without_backlink", [])))
        print("%-12s %6d %6s %6s %7s %8s %9s" % (
            name,
            res["sessions"]["session_count"],
            dr.get("records", "n/a"),
            dr.get("declared_reversal_count", "n/a"),
            dr.get("silent_reversal_count", "n/a"),
            sr3 if ic else "n/a",
            ra.get("strict_rate_per_100_commits", "n/a"),
        ))

    out["_meta"]["receipt_verification"] = verify_receipts(repos, audit)
    out["summary"] = build_summary(out["projects"], audit)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    rv = out["_meta"]["receipt_verification"]
    print("\naudit receipts: %d checked, %d held, %d FAILED"
          % (rv["checked"], rv["held"], len(rv["failed"])))
    for f in rv["failed"]:
        print("  FAILED %s: %s !~ %s" % (f["finding"], f["path"], f["contains"]))
    print("wrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
