#!/usr/bin/env python3
"""WS3(a)+(b): operator altitude and the retransmission tax.

Applies the frozen taxonomy in rubric/ALTITUDE.md to every classifiable operator
turn produced by log_miner.py, scores itself against the hand labels in
data/altitude-labels.json, and computes the warm-up / retransmission metrics.

Stdlib-only, read-only, path-parameterised (PLAN.md 5).

The rules below are a direct transcription of ALTITUDE.md 2 (R1-R9) and its
precedence order:  UNK -> M(bare assent) -> C -> D -> I -> M(default).
They were written while re-reading the DEV half of the labelled sample only;
the held-out half is scored once, at the end, and both numbers are published.

Usage:
  python altitude_classify.py --turns ../data/session-metrics/turns.json \
      --fulltext ../data/session-metrics/local/turns-fulltext.jsonl \
      --labels ../data/altitude-labels.json \
      --sample ../data/session-metrics/altitude-sample.json \
      --out-dir ../data/session-metrics
"""

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus_common import CORPUS_PROJECTS, eprint, norm_ws  # noqa: E402

VERSION = "1.0"
CLASSES = ["I", "D", "C", "M"]
HIGH = {"I", "D", "C"}

# --------------------------------------------------------------------------
# R3 - bare assent / continuation
# --------------------------------------------------------------------------
# A turn made only of these tokens carries no information beyond "proceed".
FILLER = set("""
ok okay k oki yes yep yeah ye y sure great good nice cool perfect excellent
awesome thanks thank thx ta pls please plz lets let us go ahead continue
proceed carry on keep going do it this that the a an all now again and then
next well fine agreed agree sounds sound looks look right correct execute run
run's start started begin hey ok.. yes.. sure.. plan you we i to of is it's its
""".split())
BARE_MAX_CHARS = 60

# --------------------------------------------------------------------------
# R6 - contract / design cues  (checked FIRST: the binding clause wins)
# --------------------------------------------------------------------------
C_CUES = [
    r"\bquality gate", r"\bacceptance criteri", r"\bdefinition of done\b",
    r"\b(must|should) (be|have|not|always|never)\b",
    r"\b(add|include|introduce) a rule\b", r"\brule:",
    r"\bdocument (why|the reason|the rationale)\b",
    r"\b(directory|folder|repo|project) structure\b", r"\bstructure for\b",
    r"\bso that\b[^.]{0,90}\b(reader|user|analyst|developer|agent|anyone)\b",
    r"\b(naming )?convention\b", r"\bschema\b", r"\binterface\b", r"\bcontract\b",
    r"\bprotocol\b", r"\bconsistently\b",
    r"\b[A-Za-z]{2,}Id\s*=",                      # PTId=... - an ID schema
    r"\b(given|when)\b[^.]{0,80}\bthen\b",        # a scenario contract
    r"\bkeep\b[^.]{0,40}\bin\b[^.]{0,20}\bfolder\b",
]

# --------------------------------------------------------------------------
# R4/R5 - decision cues
# --------------------------------------------------------------------------
D_CUES = [
    r"^\s*no\b", r"\bno,\s", r"\binstead\b", r"\brather than\b",
    r"\blet'?s not\b", r"\blet not\b",
    r"^\s*\d{1,2}\s*$", r"\boption \d\b", r"\bboth\b",
    r"\bi (actually )?(agree|prefer|like|disagree)\b", r"\bi don'?t like\b",
    r"\bright call\b", r"\bgood (call|point)\b",
    # "should we X?" raises a policy trade-off (R5); "what/how should we X?" asks
    # the agent to orient the operator, which is not the operator resolving.
    r"(?<!what )(?<!how )\bshould we\b[^?]{0,120}\?",
    r"\bbut without\b", r"\bkeep only\b",
    r"\bwhy don'?t we\b", r"\byes,? but\b",
    r"\bthe (first|second|third|latter|former)( one| option| approach)\b",
]

# --------------------------------------------------------------------------
# R1/R2 - intent cues
# --------------------------------------------------------------------------
# A durable referent: a file, a path, or a named plan unit that outlives the
# conversation. "the 8-task plan" (proposed a moment ago) deliberately does not
# match - that is R2.
REFERENT = re.compile(
    r"([\w./\\-]+\.(?:md|tex|txt|json|ya?ml|py|ipynb|pdf|cfg|conf)\b"
    r"|[\w-]+[/\\][\w./\\-]{3,}"
    r"|\b(?:milestone|phase|round|week|pass|part|iteration)\s*[-#]?\s*[A-Za-z0-9]\b"
    r"|\bM\d\b)", re.I)
# Dispatch verbs: reading or executing what the artifact already says. NOT
# "update"/"edit"/"write" - maintaining an artifact is not dispatching from it.
DISPATCH = re.compile(
    r"\b(read|re-?read|execute|run|go|start|address|follow|per|according to"
    r"|from|continue with|work through|implement)\b", re.I)
GOAL_VERBS = (r"build|create|make|add|do|study|research|investigate|explore"
              r"|plan|pull|write|design|set up|have a look|clean|implement"
              r"|find|search|draft|extend|migrate|extract|port")
# "do" is deliberately absent from the sentence-initial alternation: "do you
# think ...?" and "do we ...?" are questions, not goal declarations.
LEAD_VERBS = GOAL_VERBS.replace("|do|", "|")
I_CUES = [
    r"\blet'?s (?:%s)\b" % GOAL_VERBS,
    r"\bi want (?:us )?to\b",
    r"\bnext task\b", r"\bnext (?:phase|milestone|step) (?:is|will)\b",
    r"\bcan you (?:please )?(?:%s)\b" % GOAL_VERBS,
    r"^(?:hey )?(?:%s)\b" % LEAD_VERBS,
]

# R9 - re-transmitting a constraint the agent lost or violated is mechanical,
# however high-altitude the constraint itself is. Checked before C/D so that
# "I asked you to keep X in Y ... and instead you ..." does not read as a fresh
# decision.
RETRANSMIT_CUES = [
    r"\bi (?:already )?(?:asked|told) you\b", r"\bas i (?:said|explained)\b",
    r"\bi said (?:before|earlier|already)\b",
    r"\byou (?:ignored|forgot|lost|missed)\b",
    r"\b(?:again|once more),? (?:i|we|please)\b",
]

C_RE = [re.compile(p, re.I) for p in C_CUES]
D_RE = [re.compile(p, re.I) for p in D_CUES]
I_RE = [re.compile(p, re.I) for p in I_CUES]
RT_RE = [re.compile(p, re.I) for p in RETRANSMIT_CUES]

PASTE_ONLY = re.compile(r"^\s*(\[Pasted text[^\]]*\]|\[Image[^\]]*\]|[\s.,!?:;-])+\s*$")


def dispatch_by_reference(text):
    """R2: a durable referent with a read/execute verb near it."""
    for m in REFERENT.finditer(text):
        a, b = m.start(), m.end()
        window = text[max(0, a - 45):min(len(text), b + 45)]
        if DISPATCH.search(window):
            return True
    return False


def classify(text, paste_text=""):
    """-> (class, rule_that_fired). Precedence per ALTITUDE.md 2."""
    t = norm_ws(text)
    if not t or (PASTE_ONLY.match(t) and not paste_text.strip()):
        return "UNK", "R0-paste-only-unrecoverable"

    joined = t + ("\n" + paste_text if paste_text else "")
    tokens = [w.strip(".,!?:;'\"()").lower() for w in t.split()]
    tokens = [w for w in tokens if w]
    if len(t) <= BARE_MAX_CHARS and tokens and all(w in FILLER for w in tokens):
        return "M", "R3-bare-assent"

    for rx in RT_RE:
        if rx.search(t):
            return "M", "R9-retransmission"
    for rx in C_RE:
        if rx.search(joined):
            return "C", "R6-contract:" + rx.pattern[:34]
    for rx in D_RE:
        if rx.search(t):
            return "D", "R4-decision:" + rx.pattern[:34]
    # R8: a paste is input, not the act - dispatch must be read from what the
    # operator TYPED, or every pasted stack trace containing a path becomes an
    # intent declaration.
    if dispatch_by_reference(t):
        return "I", "R2-dispatch-by-reference"
    for rx in I_RE:
        if rx.search(t):
            return "I", "R1-goal:" + rx.pattern[:34]
    return "M", "R8-default-mechanical"


# --------------------------------------------------------------------------
# WS3(b) - warm-up / retransmission tax
# --------------------------------------------------------------------------
# A warm-up turn re-establishes shared context rather than advancing work. Two
# shapes, and the difference is the whole point of the analysis:
#   POINTER  - names a durable artifact and lets the agent read it. Bounded: the
#              cost does not grow with project history.
#   PAYLOAD  - re-transmits the context itself as prose or a paste. Unbounded:
#              the cost grows with everything that has to be re-said.
WARMUP_POINTER = [
    r"\b(read|re-?read|warm up|warm yourself|catch up|familiaris|familiariz)\b",
    r"\b(start|begin) (?:by|with) reading\b",
    r"\bread\b[^.]{0,40}(README|STATE|PLAN|NEXT_PROMPT|CLAUDE|INDEX|\.md\b)",
]
WARMUP_PAYLOAD = [
    r"\bcontinue from where we (left|stopped)\b", r"\bwhere we left\b",
    r"\b(as|like) (we|i) (discussed|said|agreed|decided)\b",
    r"\bpreviously\b", r"\bin (the )?(last|previous) (session|chat|conversation)\b",
    r"\byesterday\b", r"\bi had to restart\b", r"\byou (lost|forgot)\b",
    r"\blet me (remind|re-?explain)\b", r"\bfor context\b", r"\bto recap\b",
    r"\bi (already )?(asked|told) you\b", r"\bi asked you to\b",
    r"\bpick (up )?(from )?where\b", r"\bresume\b", r"\bcan you pick from\b",
    r"\bremind me\b", r"\bremember\b",
]
WP_RE = [re.compile(p, re.I) for p in WARMUP_POINTER]
WL_RE = [re.compile(p, re.I) for p in WARMUP_PAYLOAD]
PAYLOAD_CHARS = 400


def warmup_kind(text, paste_text, has_paste, seq):
    """-> None | 'pointer' | 'payload'."""
    t = norm_ws(text)
    joined = t + " " + norm_ws(paste_text)
    pointer = any(rx.search(joined) for rx in WP_RE)
    payload = any(rx.search(joined) for rx in WL_RE)
    if not (pointer or payload):
        return None
    if payload and (has_paste or len(t) > PAYLOAD_CHARS):
        return "payload"
    if payload and not pointer:
        return "payload"
    return "pointer"


# --------------------------------------------------------------------------
# agreement statistics
# --------------------------------------------------------------------------


def cohens_kappa(pairs, classes):
    n = len(pairs)
    if not n:
        return None
    obs = sum(1 for a, b in pairs if a == b) / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    exp = sum((ca[c] / n) * (cb[c] / n) for c in classes)
    if exp >= 1.0:
        return None
    return (obs - exp) / (1 - exp)


def agreement_block(pairs, classes):
    n = len(pairs)
    if not n:
        return {"n": 0}
    matrix = defaultdict(Counter)
    for hand, auto in pairs:
        matrix[hand][auto] += 1
    per_class = {}
    for c in classes:
        tp = matrix[c][c]
        fp = sum(matrix[h][c] for h in classes if h != c)
        fn = sum(matrix[c][a] for a in classes if a != c)
        prec = tp / (tp + fp) if tp + fp else None
        rec = tp / (tp + fn) if tp + fn else None
        per_class[c] = {"hand_n": sum(matrix[c].values()), "auto_n": tp + fp,
                        "precision": round(prec, 3) if prec is not None else None,
                        "recall": round(rec, 3) if rec is not None else None}
    return {
        "n": n,
        "raw_agreement": round(sum(1 for a, b in pairs if a == b) / n, 3),
        "cohens_kappa": round(cohens_kappa(pairs, classes), 3),
        "confusion_hand_rows_auto_cols": {h: dict(matrix[h]) for h in classes
                                          if matrix[h]},
        "per_class": per_class,
    }


# --------------------------------------------------------------------------


def load_turns(turns_path, fulltext_path):
    turns = json.load(open(turns_path, encoding="utf-8"))["turns"]
    full = {}
    for line in open(fulltext_path, encoding="utf-8"):
        o = json.loads(line)
        full[o["turn_id"]] = (o["text"], o["paste"])
    for t in turns:
        t["_full"], t["_paste"] = full.get(t["turn_id"], (t["preview"], ""))
    return turns


def classifiable(t):
    return (t["kind"] == "prompt" and t["verbatim"] and not t["off_project"]
            and t["source"] in ("claude_history", "copilot_jb"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--turns", type=Path, required=True)
    ap.add_argument("--fulltext", type=Path, required=True)
    ap.add_argument("--labels", type=Path, required=True)
    ap.add_argument("--sample", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()

    turns = load_turns(args.turns, args.fulltext)
    labels = json.load(open(args.labels, encoding="utf-8"))["labels"]
    sample = json.load(open(args.sample, encoding="utf-8"))["sample"]

    # --- classify everything ---
    for t in turns:
        if classifiable(t):
            t["altitude"], t["rule"] = classify(t["_full"], t["_paste"])
            t["warmup"] = warmup_kind(t["_full"], t["_paste"], t["has_paste"],
                                      t["seq"])
        else:
            t["altitude"], t["rule"], t["warmup"] = None, None, None

    by_id = {t["turn_id"]: t for t in turns}

    # --- agreement vs the frozen hand labels ---
    pairs = {"dev": [], "held_out": []}
    disagreements = []
    for s in sample:
        hand = labels[str(s["n"])]["label"]
        auto = by_id[s["turn_id"]]["altitude"]
        pairs[s["split"]].append((hand, auto))
        if hand != auto:
            disagreements.append({
                "n": s["n"], "split": s["split"], "project": s["project"],
                "hand": hand, "auto": auto,
                "rule": by_id[s["turn_id"]]["rule"],
                "preview": s["preview"][:110],
            })
    allpairs = pairs["dev"] + pairs["held_out"]
    four = CLASSES + ["UNK"]
    binary = lambda c: "high" if c in HIGH else ("UNK" if c == "UNK" else "low")

    agreement = {
        "four_way": {
            "dev": agreement_block(pairs["dev"], four),
            "held_out": agreement_block(pairs["held_out"], four),
            "all": agreement_block(allpairs, four),
        },
        "high_vs_mechanical": {
            "dev": agreement_block([(binary(a), binary(b)) for a, b in pairs["dev"]],
                                   ["high", "low", "UNK"]),
            "held_out": agreement_block([(binary(a), binary(b))
                                         for a, b in pairs["held_out"]],
                                        ["high", "low", "UNK"]),
            "all": agreement_block([(binary(a), binary(b)) for a, b in allpairs],
                                   ["high", "low", "UNK"]),
        },
        "disagreements": sorted(disagreements, key=lambda d: (d["split"], d["n"])),
        "interpretation_note": (
            "This is instrument STABILITY (does a stated rule set reproduce the "
            "labeller's own judgment), not inter-rater reliability - there is only "
            "one rater. The held-out half was not read while the rules were "
            "written, but the same person wrote both, so it is unrehearsed rather "
            "than blind."
        ),
        "first_run_uncontaminated": {
            "note": (
                "The FIRST run of the classifier, before any rule was touched, is "
                "the only fully uncontaminated held-out measurement: after it, four "
                "implementation defects were fixed and five held-out disagreements "
                "had been read. The fixes were all traceable to rules already "
                "written in ALTITUDE.md (R8 - a paste is input, so dispatch is read "
                "from typed text only; R9 - retransmission is mechanical, now "
                "checked before C/D) or to cue over-breadth ('do' as a "
                "sentence-initial goal verb caught 'do you think...?'; 'should we' "
                "caught 'what should we do next?'). No cue was added to rescue an "
                "individual turn. Both runs are published so the reader can take "
                "the conservative number."
            ),
            "four_way": {"dev": {"n": 61, "raw_agreement": 0.787,
                                 "cohens_kappa": 0.666},
                         "held_out": {"n": 38, "raw_agreement": 0.868,
                                      "cohens_kappa": 0.806}},
            "high_vs_mechanical": {"dev": {"n": 61, "raw_agreement": 0.836,
                                           "cohens_kappa": 0.688},
                                   "held_out": {"n": 38, "raw_agreement": 0.947,
                                                "cohens_kappa": 0.904}},
        },
    }

    # --- per-project distributions ---
    def dist(sel):
        c = Counter(t["altitude"] for t in sel if t["altitude"])
        n = sum(c[k] for k in CLASSES)
        out = {"n_classified": n, "n_unclassifiable": c.get("UNK", 0),
               "counts": {k: c.get(k, 0) for k in CLASSES}}
        out["shares"] = ({k: round(c.get(k, 0) / n, 4) for k in CLASSES}
                         if n else {k: None for k in CLASSES})
        out["high_share"] = (round(sum(c.get(k, 0) for k in HIGH) / n, 4)
                             if n else None)
        out["mean_chars"] = (round(sum(t["chars"] for t in sel if t["altitude"]
                                       and t["altitude"] != "UNK") / n, 1)
                             if n else None)
        return out

    projects = {}
    for p in CORPUS_PROJECTS:
        sel = [t for t in turns if t["project"] == p and classifiable(t)]
        if not sel:
            continue
        block = dist(sel)
        block["excluded"] = {
            "slash": sum(1 for t in turns if t["project"] == p
                         and t["kind"] == "slash"),
            "rendered": sum(1 for t in turns if t["project"] == p
                            and t["kind"] == "rendered"),
            "off_project": sum(1 for t in turns if t["project"] == p
                               and t["off_project"]),
        }
        # R3 sensitivity: bare assent counted as a decision instead
        sens = Counter()
        for t in sel:
            a = t["altitude"]
            if t["rule"] == "R3-bare-assent":
                a = "D"
            sens[a] += 1
        nn = sum(sens[k] for k in CLASSES)
        block["r3_sensitivity_high_share"] = (
            round(sum(sens[k] for k in HIGH) / nn, 4) if nn else None)
        # Verbosity control (ALTITUDE.md 4.2): a longer turn has more chances to
        # hit a cue, so a cross-project high-share gap could be a gap in how
        # much the operator types rather than in altitude. If the ordering holds
        # INSIDE every length band, it is not a length artefact.
        block["by_length_band"] = {}
        for lo, hi, name in ((0, 40, "0-39"), (40, 120, "40-119"),
                             (120, 400, "120-399"), (400, 10 ** 9, "400+")):
            sub = [t for t in sel if lo <= t["chars"] < hi]
            d = dist(sub)
            block["by_length_band"][name] = {"n": d["n_classified"],
                                             "high_share": d["high_share"]}
        # What a SHORT turn is made of. This is the cleanest test of R1/R2: in a
        # substrated project a 20-character turn can be a dispatch ("read
        # NEXT_PROMPT.md, execute"), because the artifact carries the intent; in
        # a flat project a 20-character turn is "continue".
        short = [t for t in sel if t["chars"] < 40 and t["altitude"] != "UNK"]
        rules = Counter("dispatch" if t["rule"] == "R2-dispatch-by-reference"
                        else "bare_assent" if t["rule"] == "R3-bare-assent"
                        else "other" for t in short)
        ns = sum(rules.values())
        block["short_turn_composition"] = {
            "n_under_40_chars": ns,
            "share_of_all_turns": round(ns / block["n_classified"], 4)
            if block["n_classified"] else None,
            "bare_assent": rules["bare_assent"],
            "dispatch_by_reference": rules["dispatch"],
            "other": rules["other"],
            "dispatch_per_bare_assent": (round(rules["dispatch"]
                                               / rules["bare_assent"], 3)
                                         if rules["bare_assent"] else None),
        }
        block["by_month"] = {}
        for m in sorted({(t["ts"] or "")[:7] for t in sel if t["ts"]}):
            sub = [t for t in sel if (t["ts"] or "").startswith(m)]
            d = dist(sub)
            block["by_month"][m] = {"n": d["n_classified"],
                                    "high_share": d["high_share"],
                                    "shares": d["shares"]}
        projects[p] = block

    # --- WS3(b) warm-up / retransmission ---
    sessions = defaultdict(list)
    for t in turns:
        if classifiable(t):
            sessions[(t["source"], t["session_id"])].append(t)
    warm = {}
    session_rows = []
    for (src, sid), ts in sessions.items():
        ts.sort(key=lambda t: t["seq"])
        proj = Counter(t["project"] for t in ts).most_common(1)[0][0]
        prefix = 0
        for t in ts:
            if t["warmup"]:
                prefix += 1
            else:
                break
        wt = [t for t in ts if t["warmup"]]
        session_rows.append({
            "session_id": sid, "source": src, "project": proj,
            "start_ts": ts[0]["ts"], "turns": len(ts),
            "warmup_turns": len(wt),
            "warmup_prefix_turns": prefix,
            "warmup_chars": sum(t["chars"] + t["paste_chars"] for t in wt),
            "pointer": sum(1 for t in wt if t["warmup"] == "pointer"),
            "payload": sum(1 for t in wt if t["warmup"] == "payload"),
            "session_chars": sum(t["chars"] + t["paste_chars"] for t in ts),
        })
    for p in CORPUS_PROJECTS:
        rows = [r for r in session_rows if r["project"] == p]
        if not rows:
            continue
        wt = sum(r["warmup_turns"] for r in rows)
        warm[p] = {
            "sessions": len(rows),
            "turns": sum(r["turns"] for r in rows),
            "warmup_turns": wt,
            "warmup_turn_share": round(wt / max(1, sum(r["turns"] for r in rows)), 4),
            "sessions_with_warmup": sum(1 for r in rows if r["warmup_turns"]),
            "mean_warmup_prefix_turns": round(
                sum(r["warmup_prefix_turns"] for r in rows) / len(rows), 2),
            "pointer_turns": sum(r["pointer"] for r in rows),
            "payload_turns": sum(r["payload"] for r in rows),
            "pointer_share_of_warmup": (round(sum(r["pointer"] for r in rows) / wt, 4)
                                        if wt else None),
            "mean_warmup_chars_per_session": round(
                sum(r["warmup_chars"] for r in rows) / len(rows), 1),
            "mean_chars_per_warmup_turn": (round(
                sum(r["warmup_chars"] for r in rows) / wt, 1) if wt else None),
            "warmup_char_share_of_session": round(
                sum(r["warmup_chars"] for r in rows)
                / max(1, sum(r["session_chars"] for r in rows)), 4),
        }
        # Bounded vs unbounded: does the cost of ONE re-entry grow as the project
        # accumulates history? Split the project's real sessions (>=2 turns) in
        # half by time. Reported with turns/session alongside, because a project
        # whose sessions got longer has more chances to emit a warm-up turn.
        real = sorted([r for r in rows if r["turns"] >= 2],
                      key=lambda r: r["start_ts"] or "")
        if len(real) >= 4:
            h = len(real) // 2
            mean = lambda z, k: round(sum(x[k] for x in z) / len(z), 1)
            warm[p]["trend"] = {
                "halves": [
                    {"half": "first", "sessions": len(real[:h]),
                     "from": (real[0]["start_ts"] or "")[:10],
                     "to": (real[h - 1]["start_ts"] or "")[:10],
                     "warmup_chars_per_session": mean(real[:h], "warmup_chars"),
                     "warmup_turns_per_session": mean(real[:h], "warmup_turns"),
                     "turns_per_session": mean(real[:h], "turns")},
                    {"half": "second", "sessions": len(real[h:]),
                     "from": (real[h]["start_ts"] or "")[:10],
                     "to": (real[-1]["start_ts"] or "")[:10],
                     "warmup_chars_per_session": mean(real[h:], "warmup_chars"),
                     "warmup_turns_per_session": mean(real[h:], "warmup_turns"),
                     "turns_per_session": mean(real[h:], "turns")},
                ],
            }
            a = warm[p]["trend"]["halves"][0]["warmup_chars_per_session"]
            b2 = warm[p]["trend"]["halves"][1]["warmup_chars_per_session"]
            warm[p]["trend"]["direction"] = (
                "rising" if b2 > a * 1.1 else
                "falling" if b2 < a * 0.9 else "flat")
        else:
            warm[p]["trend"] = {"note": "fewer than 4 sessions of >=2 turns"}

    meta = {
        "script": "altitude_classify.py",
        "version": VERSION,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "taxonomy": "rubric/ALTITUDE.md v1.0 (frozen before this script existed)",
        "hand_labels": str(args.labels),
        "precedence": "UNK -> M(bare assent, R3) -> C -> D -> I -> M(default)",
        "definitions": {
            "classified_turn": "operator-typed, verbatim, on-project prompt",
            "high_altitude": "I + D + C; the headline collapse",
            "warmup_pointer": "context reconstruction that names a durable artifact "
                              "and lets the agent read it - bounded cost",
            "warmup_payload": "context reconstruction that re-transmits the context "
                              "itself as prose or paste - unbounded cost",
        },
        "coverage_caveats": [
            "paste bodies survive for only 74 of 204 paste-referencing turns, so "
            "warmup_chars is a LOWER bound and paste-heavy payload warm-ups are "
            "under-measured",
            "smim (2 turns) and datacli (5) and harp (11) are too small for a "
            "distribution; they are reported as counts and must not be plotted as "
            "shares without n",
            "blive has 112 classifiable turns but no surviving assistant-side "
            "transcript (WS0), so its session-level volume is not comparable",
        ],
    }

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "altitude.json", "w", encoding="utf-8") as fh:
        json.dump({"_meta": meta, "agreement": agreement, "projects": projects},
                  fh, indent=2)
    with open(out / "warmup.json", "w", encoding="utf-8") as fh:
        json.dump({"_meta": meta, "projects": warm,
                   "sessions": sorted(session_rows,
                                      key=lambda r: (r["project"], r["start_ts"] or ""))},
                  fh, indent=2)
    with open(out / "turns-classified.json", "w", encoding="utf-8") as fh:
        json.dump({"_meta": meta,
                   "turns": [{k: v for k, v in t.items() if not k.startswith("_")}
                             for t in turns]}, fh, indent=2)

    # --- console (ASCII) ---
    a4, ab = agreement["four_way"], agreement["high_vs_mechanical"]
    print("AGREEMENT hand vs automated")
    for name, blk in (("four-way", a4), ("high/low", ab)):
        print("  %-9s dev n=%-3d raw=%-6s kappa=%-6s | held-out n=%-3d raw=%-6s kappa=%s"
              % (name, blk["dev"]["n"], blk["dev"]["raw_agreement"],
                 blk["dev"]["cohens_kappa"], blk["held_out"]["n"],
                 blk["held_out"]["raw_agreement"], blk["held_out"]["cohens_kappa"]))
    print()
    print("%-11s %5s %6s %6s %6s %6s %8s %8s" % (
        "project", "n", "I", "D", "C", "M", "high%", "r3sens%"))
    print("-" * 62)
    for p, b in sorted(projects.items(), key=lambda kv: -kv[1]["n_classified"]):
        sh = b["shares"]
        print("%-11s %5d %6s %6s %6s %6s %8s %8s" % (
            p, b["n_classified"],
            *["%.2f" % sh[k] if sh[k] is not None else "n/a" for k in CLASSES],
            "%.3f" % b["high_share"] if b["high_share"] is not None else "n/a",
            "%.3f" % b["r3_sensitivity_high_share"]
            if b["r3_sensitivity_high_share"] is not None else "n/a"))
    print()
    print("%-11s %6s %7s %8s %8s %9s %9s" % (
        "project", "sess", "warm%", "prefix", "pointer", "payload", "chars/warm"))
    print("-" * 62)
    for p, b in sorted(warm.items(), key=lambda kv: -kv[1]["turns"]):
        print("%-11s %6d %7s %8s %8d %9d %9s" % (
            p, b["sessions"], "%.3f" % b["warmup_turn_share"],
            "%.2f" % b["mean_warmup_prefix_turns"], b["pointer_turns"],
            b["payload_turns"],
            "%.0f" % b["mean_chars_per_warmup_turn"]
            if b["mean_chars_per_warmup_turn"] else "n/a"))
    print("\nwrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
