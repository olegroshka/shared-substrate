#!/usr/bin/env python3
"""WS4b results assembly: local probe sessions + frozen-key scores -> probe-results.json.

Stdlib-only. Reads two things and writes one:

  in   data/probes/local/<session>/session.json   driver output (verbatim, gitignored)
  in   data/probes/scores.json                    the scorer's verdicts (published INPUT)
  out  data/probe-results.json                    PROTOCOL section 7 schema

scores.json is hand-authored author judgment, kept as a script *input* for the
same reason data/qualitative-ratings.json is (WS-X): a re-run must never be able
to silently overwrite a human verdict. Every entry carries the one-line reason
SC8 requires, and every CONFABULATED verdict carries Oleg's review state.

Verbatim answers stay local (WS3 pattern): the published JSON carries a
160-character preview and a sha1 per answer, and this script reproduces the rest
from the local store.

Statistics, all stdlib:

  * H-1, the single pre-registered test: Fisher's exact, two-sided, on the 2x2
    (blive vs btest) x (confabulated vs not). Two-sided is computed the strict
    way - sum the hypergeometric probability of every table with the same
    margins whose probability is <= the observed table's, with a relative
    tolerance so floating-point ties are not silently dropped.
  * SC9 sensitivity: the whole headline recounted with `false_absence`
    reclassified from CONFABULATED to ABSTAINED, separating invention from
    retrieval failure. Both tables are published; a contrast surviving only one
    reading is reported as fragile.
  * Everything else is descriptive counts shown with denominators.
"""

import argparse
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVAL = HERE.parent
LOCAL_STORE = EVAL / "data" / "probes" / "local"
SCORES_PATH = EVAL / "data" / "probes" / "scores.json"
OUT_PATH = EVAL / "data" / "probe-results.json"

PRE_REGISTRATION_COMMIT = "ab9c62dc3cb421174eca13a5f9ebc1692ccef0b6"
PROTOCOL_VERSION = "FROZEN v1.0 (S4, 2026-07-25)"
SCORE_VALUES = ("CORRECT", "ABSTAINED", "CONFABULATED", "VOIDED")


def sha1(text: str) -> str:
    return hashlib.sha1((text or "").encode("utf-8")).hexdigest()


def preview(text: str, n: int = 160) -> str:
    flat = " ".join((text or "").split())
    return flat[:n]


# --------------------------------------------------------------------------
# Fisher's exact test (two-sided), stdlib only
# --------------------------------------------------------------------------

def hypergeom_pmf(a: int, row1: int, row2: int, col1: int) -> float:
    """P(top-left cell == a) for a 2x2 table with the given margins."""
    total = row1 + row2
    return (math.comb(row1, a) * math.comb(row2, col1 - a)) / math.comb(total, col1)


def fisher_exact_two_sided(table: list) -> dict:
    """Two-sided Fisher's exact p for [[a, b], [c, d]]."""
    (a, b), (c, d) = table
    row1, row2 = a + b, c + d
    col1 = a + c
    lo = max(0, col1 - row2)
    hi = min(row1, col1)
    observed = hypergeom_pmf(a, row1, row2, col1)
    tolerance = observed * (1 + 1e-7)
    p = sum(hypergeom_pmf(k, row1, row2, col1)
            for k in range(lo, hi + 1)
            if hypergeom_pmf(k, row1, row2, col1) <= tolerance)
    odds = ((a * d) / (b * c)) if b and c else None
    return {
        "table": {"description": "[[group1_yes, group1_no], [group2_yes, group2_no]]",
                  "values": table},
        "p_two_sided": round(min(p, 1.0), 6),
        "odds_ratio": round(odds, 4) if odds is not None else None,
        "significant_at_0.05": min(p, 1.0) < 0.05,
    }


# --------------------------------------------------------------------------
# assembly
# --------------------------------------------------------------------------

def f1_from_transcript(session_dir: Path) -> dict:
    """Reconstruct the full F1 exchange from the session transcript.

    H4 requires every F1 response to be published, but the CLI's `result` field
    carries only the FINAL assistant message of a step. When the subject makes a
    tool call during F1 - one session tried to `ls` its own memory directory -
    the earlier text is lost from `result` and survives only in the transcript.
    F1 is everything up to the second operator prompt (F2).
    """
    path = session_dir / "transcript.jsonl"
    if not path.exists():
        return {"text": None, "tool_attempts": [], "source": "transcript missing"}
    texts, tools, prompts = [], [], 0
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("type") == "user":
            content = record.get("message", {}).get("content")
            if isinstance(content, str) and content.strip():
                prompts += 1
                if prompts > 1:
                    break
        if record.get("type") == "assistant":
            for block in record.get("message", {}).get("content", []):
                if block.get("type") == "text" and block.get("text", "").strip():
                    texts.append(block["text"].strip())
                elif block.get("type") == "tool_use":
                    tools.append({"tool": block.get("name"),
                                  "input": json.dumps(block.get("input"))[:300]})
    return {"text": "\n\n".join(texts), "tool_attempts": tools, "source": "transcript"}


def orientation_tokens(session_dir: Path, accepted_at: str) -> dict:
    """O2 measures orientation cost in agentic turns AND tokens.

    The driver's session summary keeps turns and dollars; tokens live in the
    per-step JSON. Summed from session start through the accepted statement,
    with anything after it reported separately as surplus. Tokens are the
    tool-agnostic figure, which is what the section 5 Copilot replication needs.
    """
    steps = sorted((session_dir / "steps").glob("0[123]_*.json"))
    counted, surplus, seen_accepted = Counter(), Counter(), False
    for path in steps:
        record = json.loads(path.read_text(encoding="utf-8"))
        usage = record.get("usage") or {}
        bucket = surplus if seen_accepted else counted
        for field in ("input_tokens", "output_tokens",
                      "cache_creation_input_tokens", "cache_read_input_tokens"):
            bucket[field] += usage.get(field) or 0
        if record.get("step") == accepted_at:
            seen_accepted = True

    def shape(counter):
        total = sum(counter.values())
        return {**dict(counter), "total_tokens": total} if total else None

    return {"through_accepted": shape(counted), "surplus_after_acceptance": shape(surplus)}


def load_sessions() -> list:
    """Every session in the local store except the H7-voided ones.

    A voided session is preserved on disk in full (nothing is dropped for
    looking wrong) but is never scored and never enters a count; its existence
    and its reason are published through scores.json's restarts_h7 block.
    """
    sessions = []
    for path in sorted(LOCAL_STORE.glob("*/session.json")):
        if "VOIDED" in path.parent.name:
            continue
        session = json.loads(path.read_text(encoding="utf-8"))
        session["_dir"] = path.parent
        sessions.append(session)
    return sessions


def effective(score: str, subtype, sensitivity: bool) -> str:
    """SC9: in the sensitivity reading, false_absence counts as ABSTAINED."""
    if sensitivity and score == "CONFABULATED" and subtype == "false_absence":
        return "ABSTAINED"
    return score


def tally(answers: list, sensitivity: bool = False) -> dict:
    """Counts with their denominators. VOIDED answers are published but never
    enter a rate: `n` is the scored denominator, voided questions sit outside it."""
    counts = Counter(effective(a["score"], a.get("confabulation_subtype"), sensitivity)
                     for a in answers)
    voided = counts.get("VOIDED", 0)
    scored = len(answers) - voided
    return {
        "n": scored,
        "n_asked": len(answers),
        "voided": voided,
        "correct": counts.get("CORRECT", 0),
        "abstained": counts.get("ABSTAINED", 0),
        "confabulated": counts.get("CONFABULATED", 0),
    }


def build(args) -> dict:
    scores = json.loads(SCORES_PATH.read_text(encoding="utf-8"))
    verdicts = scores["verdicts"]
    sessions = load_sessions()

    probe_sessions = [s for s in sessions if s["project"] != "shakeout"]
    shakeout = next((s for s in sessions if s["project"] == "shakeout"), None)

    answers, orientation = [], []
    for session in probe_sessions:
        key = session["key"]
        for ans in session.get("answers", []):
            verdict = verdicts.get(key, {}).get(ans["qid"])
            if verdict is None:
                raise SystemExit(f"missing score for {key} {ans['qid']}")
            if verdict["score"] not in SCORE_VALUES:
                raise SystemExit(f"bad score {verdict['score']} for {key} {ans['qid']}")
            flags = list(verdict.get("flags", []))
            if ans.get("over_cap") and not ans.get("has_answer_line"):
                if "cap_hit" not in flags:
                    flags.append("cap_hit")
            if ans.get("over_cap") and "over_cap" not in flags:
                flags.append("over_cap")
            answers.append({
                "session": key,
                "project": session["project_name"],
                "run": session["run"],
                "qid": ans["qid"],
                "slot": ans["slot"],
                "gt_type": ans["gt_type"],
                "score": verdict["score"],
                "confabulation_subtype": verdict.get("subtype"),
                "flags": flags,
                "reason": verdict["reason"],
                "oleg_review": verdict.get("oleg_review"),
                "override": verdict.get("override"),
                "turns": ans["turns"],
                "tool_calls": ans["tool_calls"],
                "cost_usd": ans["cost_usd"],
                "f6_used": ans["f6_used"],
                "access_attempts": len(ans.get("guard_denials") or []),
                "access_attempt_detail": [
                    {"tool": g["tool"], "reason": g["reason"]}
                    for g in (ans.get("guard_denials") or [])],
                "answer_line": ans["answer_line"],
                "answer_sha1": sha1(ans["response"]),
                "answer_preview": preview(ans["response"]),
            })

        # Re-read the judgment file rather than trusting the copy the driver
        # merged at `ask` time: the judgment is a published INPUT and must be
        # what the results reflect, even if it was clarified after the run.
        # Measured cost stays with the session record.
        orient = dict(session.get("orientation", {}))
        judgment_path = session["_dir"] / "orientation-judgment.json"
        if judgment_path.exists():
            measured_cost = orient.get("cost")
            orient.update(json.loads(judgment_path.read_text(encoding="utf-8")))
            orient["cost"] = measured_cost
        orientation.append({
            "session": key,
            "project": session["project_name"],
            "run": session["run"],
            "accepted": orient.get("accepted"),
            "accepted_at_step": orient.get("accepted_at_step"),
            "nudges": orient.get("nudges", 0),
            "surplus_nudges": orient.get("surplus_nudges", 0),
            "rule_R_O3": orient.get("rule_R_O3"),
            "operator_error_disclosure": orient.get("operator_error_disclosure"),
            "stated_correctly": orient.get("stated_correctly"),
            "omitted": orient.get("omitted"),
            "contradicted": orient.get("contradicted"),
            "key_facts": orient.get("key_facts"),
            "f1_contamination": orient.get("f1_contamination"),
            "f1_response": f1_from_transcript(session["_dir"]),
            "cost": orient.get("cost"),
            "tokens": orientation_tokens(session["_dir"],
                                         orient.get("accepted_at_step") or ""),
        })

    # ---- summaries -------------------------------------------------------
    by_project, by_project_run = {}, {}
    for project in sorted({a["project"] for a in answers}):
        rows = [a for a in answers if a["project"] == project]
        by_project[project] = {
            "headline": tally(rows),
            "sensitivity_sc9": tally(rows, sensitivity=True),
            "by_ground_truth": {
                gt: tally([a for a in rows if a["gt_type"] == gt])
                for gt in sorted({a["gt_type"] for a in rows})
            },
            "confabulation_subtypes": dict(Counter(
                a["confabulation_subtype"] for a in rows
                if a["score"] == "CONFABULATED" and a["confabulation_subtype"])),
            "access_attempts": sum(a["access_attempts"] for a in rows),
            "total_cost_usd": round(sum(a["cost_usd"] or 0 for a in rows), 4),
            "mean_turns_per_question": round(
                sum(a["turns"] for a in rows) / len(rows), 2) if rows else None,
        }
        for run in sorted({a["run"] for a in rows}):
            by_project_run[f"{project}-run{run}"] = tally(
                [a for a in rows if a["run"] == run])

    def confab_2x2(p1: str, p2: str, sensitivity: bool = False):
        """2x2 over SCORED answers only - voided questions are not in any rate."""
        out = []
        for project in (p1, p2):
            rows = [a for a in answers
                    if a["project"] == project and a["score"] != "VOIDED"]
            confab = sum(1 for a in rows
                         if effective(a["score"], a["confabulation_subtype"],
                                      sensitivity) == "CONFABULATED")
            out.append([confab, len(rows) - confab])
        return out

    hypotheses = {}
    projects = {a["project"] for a in answers}
    if {"blive", "btest"} <= projects:
        hypotheses["H-1_primary"] = {
            "statement": "Confabulation rate is lower in blive than in btest.",
            "test": "Fisher's exact, two-sided, alpha 0.05 (the single pre-registered test)",
            "groups": ["blive", "btest"],
            "headline": fisher_exact_two_sided(confab_2x2("blive", "btest")),
            "sensitivity_sc9": fisher_exact_two_sided(
                confab_2x2("blive", "btest", sensitivity=True)),
        }
        hypotheses["H-2_correct_rate"] = {
            "statement": "Correct rate is higher in blive than in btest.",
            "test": "descriptive only",
            "blive": by_project["blive"]["headline"],
            "btest": by_project["btest"]["headline"],
        }

    hypotheses["H-3_orientation_cost"] = {
        "statement": "Orientation cost (tokens to accepted status) is lower in blive than btest.",
        "test": "descriptive only, reported per session with its n",
        "per_session": [{"session": o["session"], "project": o["project"],
                         "accepted": o["accepted"], "nudges": o["nudges"],
                         "cost": o["cost"]} for o in orientation],
    }
    hypotheses["H-4_b_autobot_exploratory"] = {
        "statement": "b-autobot sits between blive and btest on H-1..H-3 (exploratory, no test).",
        "test": "descriptive only",
        "counts": by_project.get("b-autobot"),
    }

    meta = {
        "workstream": "WS4b",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "protocol_version": PROTOCOL_VERSION,
        "pre_registration_commit": PRE_REGISTRATION_COMMIT,
        "subject_model_requested": probe_sessions[0]["model_requested"] if probe_sessions else None,
        "cli_version": probe_sessions[0]["cli_version"] if probe_sessions else None,
        "driver": "scripts/probe_driver.py + scripts/probe_guard.py (H5 plumbing, published)",
        "scores_input": "data/probes/scores.json (hand-authored, published as a script input)",
        "local_store": "data/probes/local/ (verbatim transcripts + answers, gitignored)",
        "sessions": [{
            "key": s["key"], "project": s["project_name"], "run": s["run"],
            "repo_path": s["repo_path"], "head": s["head"],
            "git_status_short": s["git_status_short"],
            "session_id": s["session_id"],
            "opened_at": s["opened_at"], "closed_at": s.get("closed_at"),
            "total_cost_usd": s.get("total_cost_usd"),
            "transcript_bytes": s.get("transcript_bytes"),
        } for s in probe_sessions],
        "shakeout": {
            "target": shakeout["project_name"] if shakeout else None,
            "head": shakeout["head"] if shakeout else None,
            "never_scored": True,
            "checks": scores.get("shakeout_checks"),
        },
        "restarts_h7": scores.get("restarts_h7", []),
        "voided_h9": scores.get("voided_h9", []),
        "h9_repo_state_verification": scores.get("h9_repo_state_verification"),
        "harness_deviations": scores.get("harness_deviations"),
        "scoring_notes": scores.get("scoring_notes"),
    }

    return {
        "_meta": meta,
        "summary": {
            "by_project": by_project,
            "by_project_run": by_project_run,
            "sc9_note": ("Headline counts false_absence as CONFABULATED (SC3). The "
                         "sensitivity_sc9 tables recount it as ABSTAINED, separating "
                         "invention from retrieval failure. A contrast that survives "
                         "only one reading is fragile and is reported as such."),
        },
        "hypotheses": hypotheses,
        "orientation": orientation,
        "answers": answers,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    args = parser.parse_args()
    payload = build(args)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"wrote {args.out}")
    for project, block in payload["summary"]["by_project"].items():
        head = block["headline"]
        sens = block["sensitivity_sc9"]
        print(f"  {project:<10} n={head['n']:<3} correct={head['correct']:<3} "
              f"abstained={head['abstained']:<3} confabulated={head['confabulated']:<3} "
              f"(SC9 confab={sens['confabulated']})")
    h1 = payload["hypotheses"].get("H-1_primary")
    if h1:
        print(f"  H-1 Fisher two-sided p={h1['headline']['p_two_sided']} "
              f"(SC9 p={h1['sensitivity_sc9']['p_two_sided']})")


if __name__ == "__main__":
    main()
