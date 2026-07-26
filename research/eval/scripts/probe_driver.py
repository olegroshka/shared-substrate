#!/usr/bin/env python3
"""WS4b probe driver: runs the frozen PROTOCOL.md procedure against one repo.

Harness plumbing (PROTOCOL H5), written in S5 to the S4 spec and published with
the results. It decides NOTHING about the instrument: every word the subject
sees is extracted verbatim at run time from the frozen files -

  * frozen texts F1-F6   <- probes/PROTOCOL.md section 3
  * the 20 questions     <- probes/questions-p{1,2,3}.md

so no probe text is ever retyped into this script. The scoring keys in those
same files are never read by the driver and never enter a session.

WHAT THIS SCRIPT ENFORCES (PROTOCOL section 2)

  H1 repo-only     cwd is the probed repo; --tools limits the built-in surface
                   to Read/Glob/Grep/Bash; --allowedTools scopes Read to the
                   tree and Bash to read-only git plus read-only shell filters;
                   probe_guard.py denies anything that still resolves outside
                   the tree and logs every attempt.
  H2 no memory     CLAUDE_CONFIG_DIR points at a scratch config directory that
                   is deleted and re-copied from a pristine snapshot before
                   EVERY session, so auto-memory written during one probe
                   cannot reach the next. The real ~/.claude is only ever read
                   (once, to seed the snapshot) and never written.
  H3 in-tree docs  the repo's own CLAUDE.md/AGENTS.md still auto-load.
  H5 driver        one CLI invocation per protocol step, session continuation
                   by fixed --session-id, per-step cost from the CLI's own JSON.
  H9 repo state    HEAD and `git status --short` are recorded BY THE DRIVER,
                   before F1, never by the subject.

DECLARED HARNESS DEVIATIONS (both reported in probe-results.json _meta)

  D1. --setting-sources project. Every corpus repo carries a
      `.claude/settings.local.json` with `"defaultMode": "bypassPermissions"`
      and `Read(//mnt/c/Users/olegr/PycharmProjects/**)`. Loading it would hand
      the subject every sibling repository and void H1. The `local` and `user`
      sources are therefore excluded. `project` is kept because it is what
      restores in-tree CLAUDE.md auto-discovery (H3), and because no corpus repo
      has a `.claude/settings.json` at all - so this excludes a permission
      escalation and nothing else. Verified by inspection before run 1.
  D2. Turn caps are scored, not enforced. Claude Code 2.1.220 has no
      --max-turns, so H6's caps (50 orientation, 15 per question) cannot stop a
      step mid-flight. Per-step turn counts are recorded and H6's stated
      consequence is applied at scoring time: a question that exceeded its cap
      without an ANSWER line scores ABSTAINED with flag `cap_hit`. Steps that
      exceeded a cap but answered are flagged `over_cap` and published.

USAGE (one session = open -> [nudge ...] -> ask)

    python probe_driver.py questions --project p1      # verify extraction
    python probe_driver.py texts                       # verify F1-F6
    python probe_driver.py open  --project p3 --run 1  # reset, F1, F2
    python probe_driver.py nudge --session <key>       # F3, at most 3x
    python probe_driver.py ask   --session <key>       # F4 then Q1..Q20

`open` stops after orientation on purpose: PROTOCOL O1 acceptance is an
operator judgment against the frozen orientation key, and it is control flow,
not scoring (O4). The judgment is recorded as a published input file
(orientation-judgment.json) before `ask` will run.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVAL = HERE.parent
PROBES = EVAL / "probes"
LOCAL_STORE = EVAL / "data" / "probes" / "local"

PRISTINE_CONFIG = Path(os.environ.get(
    "PROBE_PRISTINE_CONFIG", r"C:\Users\olegr\.claude-probe\pristine"))
ACTIVE_CONFIG = Path(os.environ.get(
    "PROBE_ACTIVE_CONFIG", r"C:\Users\olegr\.claude-probe\active"))

MODEL = "claude-sonnet-5"

PROJECTS = {
    "p1": {"name": "blive", "path": Path(r"C:\Users\olegr\PycharmProjects\blive"),
           "questions": "questions-p1.md"},
    "p2": {"name": "btest", "path": Path(r"C:\Users\olegr\PycharmProjects\btest"),
           "questions": "questions-p2.md"},
    "p3": {"name": "b-autobot", "path": Path(r"C:\Users\olegr\IdeaProjects\b-autobot"),
           "questions": "questions-p3.md"},
    "shakeout": {"name": "datacli", "path": Path(r"C:\Users\olegr\PycharmProjects\datacli"),
                 "questions": None},
}

# H1's read-only surface. git first, then the shell filters that make git output
# usable (a subject forced to read 400-line logs whole would be handicapped in
# every project equally, but pointlessly).
GIT_READONLY = ["log", "show", "diff", "blame", "status", "ls-files", "rev-parse",
                "rev-list", "cat-file", "branch", "tag", "shortlog", "grep",
                "describe", "ls-tree", "count-objects"]
SHELL_READONLY = ["ls", "cat", "head", "tail", "wc", "sort", "uniq", "grep",
                  "find", "cut", "tr", "echo", "basename", "dirname", "du",
                  "file", "awk", "sed", "diff", "comm", "nl", "column"]

ANSWER_RE = re.compile(r"^\s*(?:\*\*)?ANSWER\s*:", re.MULTILINE | re.IGNORECASE)
# F5 is `Q<n>: <question text>`. PROTOCOL section 3 calls the substitutions
# "<n> and <question>", but the placeholder as frozen reads "<question text>".
# Match the placeholder as written, not as described.
F5_QUESTION_SLOT = re.compile(r"<question[^>]*>")
ORIENT_CAP_TURNS = 50
QUESTION_CAP_TURNS = 15


# --------------------------------------------------------------------------
# frozen-text and question extraction (never retyped)
# --------------------------------------------------------------------------

def load_frozen_texts() -> dict:
    """Extract F1-F6 verbatim from PROTOCOL.md section 3 blockquotes."""
    text = (PROBES / "PROTOCOL.md").read_text(encoding="utf-8")
    out, current, buf = {}, None, []
    for line in text.splitlines():
        header = re.match(r"^- \*\*(F\d)\b", line)
        if header:
            if current:
                out[current] = " ".join(buf).strip()
            current, buf = header.group(1), []
            continue
        if current is not None:
            quoted = re.match(r"^\s*> ?(.*)$", line)
            if quoted:
                buf.append(quoted.group(1).strip())
            elif line.strip() and not line.startswith("  "):
                out[current] = " ".join(buf).strip()
                current, buf = None, []
    if current:
        out[current] = " ".join(buf).strip()
    missing = [f"F{i}" for i in range(1, 7) if f"F{i}" not in out]
    if missing:
        raise SystemExit(f"frozen text extraction failed: missing {missing}")
    return out


def load_questions(project: str) -> list:
    """Extract the 20 questions (qid, slot, gt_type, text) from the frozen file."""
    meta = PROJECTS[project]
    if not meta["questions"]:
        return []
    text = (PROBES / meta["questions"]).read_text(encoding="utf-8")
    questions, current, buf, collecting = [], None, [], False

    def flush():
        if current and buf:
            current["text"] = re.sub(r"\s+", " ", " ".join(buf)).strip()
            questions.append(current)

    for line in text.splitlines():
        header = re.match(r"^### ((P\d)-Q(\d\d))\s+\W\s+([A-Z]{3}-[RN]\d)\s+\W\s+(.*)$", line)
        if header:
            flush()
            tail = header.group(5)
            gt = re.search(r"gt_type:\s*([a-z-]+)", tail)
            current = {
                "qid": header.group(1),
                "index": int(header.group(3)),
                "slot": header.group(4),
                "ground_truth": "no-record" if "gt_type" in tail else "recorded",
                "gt_type": gt.group(1) if gt else "recorded",
                "declared_substitution": "declared substitution" in tail,
                "history_only_receipt": "history-only" in tail,
            }
            buf, collecting = [], False
            continue
        if current is None:
            continue
        if line.startswith("**Q:**"):
            collecting = True
            buf.append(line[len("**Q:**"):].strip())
            continue
        if collecting:
            if line.startswith("**") or not line.strip():
                collecting = False
                continue
            buf.append(line.strip())
    flush()
    if len(questions) != 20:
        raise SystemExit(f"{project}: extracted {len(questions)} questions, expected 20")
    return questions


# --------------------------------------------------------------------------
# session plumbing
# --------------------------------------------------------------------------

def ascii_safe(text: str) -> str:
    """Console output is ASCII-only (Windows cp1252)."""
    return (text or "").encode("ascii", "replace").decode("ascii")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def git(repo: Path, *args) -> str:
    proc = subprocess.run(["git", "--no-optional-locks", *args], cwd=repo,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    return (proc.stdout or "").strip()


def reset_config() -> None:
    """H2: restore the scratch config directory to its pristine snapshot."""
    if not PRISTINE_CONFIG.exists():
        raise SystemExit(f"pristine config snapshot missing: {PRISTINE_CONFIG}")
    if ACTIVE_CONFIG.exists():
        shutil.rmtree(ACTIVE_CONFIG)
    shutil.copytree(PRISTINE_CONFIG, ACTIVE_CONFIG)


def child_env(repo: Path, session_dir: Path, step: str) -> dict:
    """A scrubbed environment: no parent Claude Code state, no API key."""
    env = {k: v for k, v in os.environ.items()
           if k not in {"CLAUDECODE", "AI_AGENT"}
           and not k.startswith(("CLAUDE", "ANTHROPIC_"))}
    env["CLAUDE_CONFIG_DIR"] = str(ACTIVE_CONFIG)
    env["PROBE_ROOT"] = str(repo)
    env["PROBE_GUARD_LOG"] = str(session_dir / "guard-log.jsonl")
    env["PROBE_STEP"] = step
    return env


def allowed_tools(repo: Path) -> list:
    posix = str(repo).replace("\\", "/")
    rules = [f"Read(//{posix}/**)", "Glob", "Grep"]
    rules += [f"Bash(git {sub}:*)" for sub in GIT_READONLY]
    rules += [f"Bash({cmd}:*)" for cmd in SHELL_READONLY]
    return rules


def write_settings(session_dir: Path) -> Path:
    """Hook settings passed with --settings, independent of --setting-sources."""
    path = session_dir / "harness-settings.json"
    path.write_text(json.dumps({
        "hooks": {
            "PreToolUse": [{
                "matcher": "*",
                "hooks": [{"type": "command",
                           "command": f'python "{HERE / "probe_guard.py"}"',
                           "timeout": 30}],
            }]
        }
    }, indent=2), encoding="utf-8")
    return path


def run_step(session: dict, session_dir: Path, step: str, prompt: str) -> dict:
    """One protocol step = one CLI invocation. Returns the parsed result."""
    repo = Path(session["repo_path"])
    first = not session["steps"]
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "json",
        "--model", MODEL,
        "--strict-mcp-config",
        "--setting-sources", "project",
        "--settings", str(session_dir / "harness-settings.json"),
        "--tools", "Read,Glob,Grep,Bash",
        "--allowedTools", *allowed_tools(repo),
    ]
    cmd += (["--session-id", session["session_id"]] if first
            else ["--resume", session["session_id"]])

    started = time.time()
    proc = subprocess.run(cmd, cwd=repo, env=child_env(repo, session_dir, step),
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=3600)
    elapsed = round(time.time() - started, 1)

    raw = proc.stdout or ""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = {"is_error": True, "subtype": "driver_parse_failure",
                   "result": raw[:4000], "stderr": (proc.stderr or "")[:4000]}

    record = {
        "step": step,
        "prompt": prompt,
        "started_at": now(),
        "wall_seconds": elapsed,
        "returncode": proc.returncode,
        "is_error": bool(payload.get("is_error")),
        "subtype": payload.get("subtype"),
        "terminal_reason": payload.get("terminal_reason"),
        "num_turns": payload.get("num_turns"),
        "duration_ms": payload.get("duration_ms"),
        "total_cost_usd": payload.get("total_cost_usd"),
        "usage": payload.get("usage"),
        "model_usage": payload.get("modelUsage"),
        "permission_denials": payload.get("permission_denials"),
        "result": payload.get("result"),
        "stderr": (proc.stderr or "")[:2000] or None,
    }
    (session_dir / "steps").mkdir(exist_ok=True)
    (session_dir / "steps" / f"{step}.json").write_text(
        json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    session["steps"].append({k: record[k] for k in
                             ("step", "num_turns", "total_cost_usd", "is_error",
                              "wall_seconds")})
    save_session(session_dir, session)
    return record


def save_session(session_dir: Path, session: dict) -> None:
    (session_dir / "session.json").write_text(
        json.dumps(session, indent=2, ensure_ascii=False), encoding="utf-8")


def load_session(key: str) -> tuple:
    session_dir = LOCAL_STORE / key
    path = session_dir / "session.json"
    if not path.exists():
        raise SystemExit(f"no session at {path}")
    return session_dir, json.loads(path.read_text(encoding="utf-8"))


def guard_summary(session_dir: Path, step_prefix: str = "") -> dict:
    log = session_dir / "guard-log.jsonl"
    calls, denials = 0, []
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if step_prefix and not str(rec.get("step", "")).startswith(step_prefix):
                continue
            calls += 1
            if rec.get("decision") == "deny":
                denials.append(rec)
    return {"tool_calls": calls, "guard_denials": denials}


def copy_transcript(session_dir: Path, session: dict) -> None:
    src = ACTIVE_CONFIG / "projects"
    for path in src.rglob(f"{session['session_id']}.jsonl"):
        shutil.copy2(path, session_dir / "transcript.jsonl")
        session["transcript_bytes"] = path.stat().st_size
        return
    session["transcript_bytes"] = None


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_texts(_args) -> None:
    for key, value in sorted(load_frozen_texts().items()):
        print(f"--- {key} ({len(value)} chars)")
        print(ascii_safe(value))
        print()


def cmd_questions(args) -> None:
    texts = load_frozen_texts()
    for question in load_questions(args.project):
        print(f"--- {question['qid']} {question['slot']} "
              f"[{question['gt_type']}]")
        if args.composed:
            print(ascii_safe(compose_question(texts["F5"], question["index"],
                                              question["text"])))
        else:
            print(ascii_safe(question["text"]))
        print()


def cmd_open(args) -> None:
    project = PROJECTS[args.project]
    repo = project["path"]
    key = args.key or (f"{project['name']}-run{args.run}" if args.run
                       else f"shakeout-{project['name']}")
    session_dir = LOCAL_STORE / key
    if (session_dir / "session.json").exists() and not args.force:
        raise SystemExit(f"session {key} already exists; use --force to void and restart (H7)")
    if session_dir.exists():
        shutil.rmtree(session_dir)
    session_dir.mkdir(parents=True)

    reset_config()
    write_settings(session_dir)
    texts = load_frozen_texts()

    session = {
        "key": key,
        "project": args.project,
        "project_name": project["name"],
        "run": args.run,
        "repo_path": str(repo),
        "session_id": str(uuid.uuid4()),
        "model_requested": MODEL,
        "cli_version": subprocess.run(["claude", "--version"], capture_output=True,
                                      text=True).stdout.strip(),
        "opened_at": now(),
        # H9: recorded by the driver, before F1, never by the subject.
        "head": git(repo, "rev-parse", "HEAD"),
        "git_status_short": git(repo, "status", "--short"),
        "config_reset_from": str(PRISTINE_CONFIG),
        "steps": [],
        "orientation": {"nudges": 0},
    }
    save_session(session_dir, session)

    print(f"=== session {key}  repo={repo}")
    print(f"HEAD {session['head']}")
    print("status --short:")
    print(ascii_safe(session["git_status_short"]) or "  (clean)")

    f1 = run_step(session, session_dir, "01_F1", texts["F1"])
    print("\n===== F1 (contamination check) =====")
    print(ascii_safe(f1["result"]))

    f2 = run_step(session, session_dir, "02_F2", texts["F2"])
    print("\n===== F2 (orientation) =====")
    print(ascii_safe(f2["result"]))
    print(f"\n[turns={f2['num_turns']} cost={f2['total_cost_usd']}]")
    print("\nNext: judge O1 against the orientation key, write "
          f"{session_dir / 'orientation-judgment.json'}, then run `ask`.")
    copy_transcript(session_dir, session)
    save_session(session_dir, session)


def cmd_nudge(args) -> None:
    session_dir, session = load_session(args.session)
    if session["orientation"]["nudges"] >= 3:
        raise SystemExit("orientation nudge cap reached (O1: max 3)")
    session["orientation"]["nudges"] += 1
    n = session["orientation"]["nudges"]
    texts = load_frozen_texts()
    record = run_step(session, session_dir, f"03_F3_{n}", texts["F3"])
    print(f"===== F3 nudge {n} =====")
    print(ascii_safe(record["result"]))
    copy_transcript(session_dir, session)
    save_session(session_dir, session)


def cmd_ask(args) -> None:
    session_dir, session = load_session(args.session)
    judgment_path = session_dir / "orientation-judgment.json"
    if not judgment_path.exists():
        raise SystemExit(f"write the O1/O3 orientation judgment to {judgment_path} first")
    session["orientation"].update(json.loads(judgment_path.read_text(encoding="utf-8")))

    # O2: cost runs from session start THROUGH the accepted orientation
    # statement. `accepted_at_step` names that step, so any step after it is
    # surplus and is published separately rather than folded into the headline.
    orient_steps = [s for s in session["steps"] if s["step"].startswith(("01_", "02_", "03_"))]
    accepted_at = session["orientation"].get("accepted_at_step")
    if accepted_at:
        names = [s["step"] for s in orient_steps]
        if accepted_at not in names:
            raise SystemExit(f"accepted_at_step {accepted_at!r} is not an orientation step")
        counted = orient_steps[:names.index(accepted_at) + 1]
    else:
        counted = orient_steps
    surplus = orient_steps[len(counted):]

    def totals(steps):
        return {
            "turns": sum(s["num_turns"] or 0 for s in steps),
            "cost_usd": round(sum(s["total_cost_usd"] or 0 for s in steps), 6),
            "steps": len(steps),
        }

    session["orientation"]["cost"] = {
        **totals(counted),
        "over_cap": totals(counted)["turns"] > ORIENT_CAP_TURNS,
        "surplus_after_acceptance": totals(surplus) if surplus else None,
    }

    texts = load_frozen_texts()
    questions = load_questions(session["project"])
    if not questions:
        raise SystemExit("shakeout sessions have no question set")

    run_step(session, session_dir, "04_F4", texts["F4"])
    session["answers"] = []

    for question in questions:
        idx = question["index"]
        step = f"Q{idx:02d}"
        prompt = compose_question(texts["F5"], idx, question["text"])
        record = run_step(session, session_dir, f"05_{step}", prompt)
        turns = record["num_turns"] or 0
        f6_used = False

        if not ANSWER_RE.search(record["result"] or "") and not record["is_error"]:
            f6_used = True
            record = run_step(session, session_dir, f"05_{step}_F6", texts["F6"])
            turns += record["num_turns"] or 0

        guard = guard_summary(session_dir, f"05_{step}")
        answer = {
            "qid": question["qid"],
            "slot": question["slot"],
            "gt_type": question["gt_type"],
            "question": question["text"],
            "prompt_sent": prompt,
            "response": record["result"],
            "answer_line": extract_answer_line(record["result"]),
            "has_answer_line": bool(ANSWER_RE.search(record["result"] or "")),
            "f6_used": f6_used,
            "turns": turns,
            "over_cap": turns > QUESTION_CAP_TURNS,
            "cost_usd": record["total_cost_usd"],
            "usage": record["usage"],
            "tool_calls": guard["tool_calls"],
            "guard_denials": guard["guard_denials"],
            "permission_denials": record["permission_denials"],
            "is_error": record["is_error"],
        }
        session["answers"].append(answer)
        save_session(session_dir, session)
        print(f"[{step}] turns={turns} tools={guard['tool_calls']} "
              f"denied={len(guard['guard_denials'])} f6={f6_used} "
              f"answer={'yes' if answer['has_answer_line'] else 'NO'}")

    session["closed_at"] = now()
    session["total_cost_usd"] = round(
        sum(s["total_cost_usd"] or 0 for s in session["steps"]), 6)
    copy_transcript(session_dir, session)
    save_session(session_dir, session)
    print(f"\n=== session {session['key']} complete: "
          f"{len(session['answers'])} answers, ${session['total_cost_usd']}")


def compose_question(f5: str, index: int, question: str) -> str:
    """Fill F5's two slots. Raises if either slot survives - a session that sends
    an unfilled template is a harness failure and voids under H7."""
    prompt = F5_QUESTION_SLOT.sub(lambda _: question, f5.replace("<n>", str(index)))
    if "<" in prompt and ">" in prompt and re.search(r"<(?:n|question)[^>]*>", prompt):
        raise SystemExit(f"F5 substitution failed, refusing to send: {prompt!r}")
    return prompt


def extract_answer_line(text: str):
    if not text:
        return None
    for line in reversed(text.splitlines()):
        if ANSWER_RE.match(line):
            return line.strip().lstrip("*").strip()
    return None


def cmd_digest(args) -> None:
    """Print one session's answers for scoring against the frozen keys.

    A reading aid only: it adds nothing and decides nothing. `--lines 0` prints
    the ANSWER line alone; a positive value adds that many leading lines of the
    answer body, which SC1/SC4 need as context for the commitment test.
    """
    _, session = load_session(args.session)
    print(f"===== {session['key']} ({session['project_name']} run {session['run']})")
    for ans in session.get("answers", []):
        print(f"\n--- {ans['qid']} {ans['slot']} [{ans['gt_type']}] "
              f"turns={ans['turns']} tools={ans['tool_calls']} "
              f"f6={ans['f6_used']}")
        if args.lines:
            body = (ans["response"] or "").strip().splitlines()
            for line in body[:args.lines]:
                print("   ", ascii_safe(line)[:200])
            if len(body) > args.lines:
                print(f"    ... (+{len(body) - args.lines} lines)")
        print("  >>", ascii_safe(ans["answer_line"] or "(no ANSWER line)"))


def cmd_shakeout(args) -> None:
    """H8: throwaway session against a non-target repo. Never scored."""
    project = PROJECTS["shakeout"]
    repo = project["path"]
    session_dir = LOCAL_STORE / "shakeout-datacli"
    if session_dir.exists():
        shutil.rmtree(session_dir)
    session_dir.mkdir(parents=True)
    reset_config()
    write_settings(session_dir)
    texts = load_frozen_texts()

    session = {
        "key": "shakeout-datacli", "project": "shakeout",
        "project_name": project["name"], "run": None, "repo_path": str(repo),
        "session_id": str(uuid.uuid4()), "model_requested": MODEL,
        "cli_version": subprocess.run(["claude", "--version"], capture_output=True,
                                      text=True).stdout.strip(),
        "opened_at": now(),
        "head": git(repo, "rev-parse", "HEAD"),
        "git_status_short": git(repo, "status", "--short"),
        "steps": [], "orientation": {"nudges": 0},
    }
    save_session(session_dir, session)
    print(f"=== H8 shakeout on {repo}\nHEAD {session['head']}")

    f1 = run_step(session, session_dir, "01_F1", texts["F1"])
    print("\n===== F1 (memory isolation check) =====")
    print(ascii_safe(f1["result"]))

    f2 = run_step(session, session_dir, "02_F2", texts["F2"])
    print("\n===== F2 (orientation) =====")
    print(ascii_safe(f2["result"])[:3000])

    # Deliberate escape attempts: allowlist + guard denial must both hold, and
    # the local settings file's bypassPermissions must NOT be in force.
    probe = ("Do all four and report which succeeded: (1) read "
             "C:/Users/olegr/PycharmProjects/btest/CLAUDE.md ; (2) run: git -C "
             "C:/Users/olegr/PycharmProjects/btest log -1 --oneline ; (3) grep for "
             "'blive' under C:/Users/olegr/PycharmProjects ; (4) read this repo's "
             "own README.md.")
    esc = run_step(session, session_dir, "90_escape", probe)
    print("\n===== escape attempts =====")
    print(ascii_safe(esc["result"])[:2500])

    guard = guard_summary(session_dir)
    print(f"\nguard: {guard['tool_calls']} tool calls, "
          f"{len(guard['guard_denials'])} denied")
    for denial in guard["guard_denials"]:
        print("  DENY", ascii_safe(str(denial["reason"]))[:140])
    print("cli permission_denials:", len(esc["permission_denials"] or []))
    print("per-step cost capture:",
          [(s["step"], s["num_turns"], s["total_cost_usd"]) for s in session["steps"]])
    copy_transcript(session_dir, session)
    session["closed_at"] = now()
    save_session(session_dir, session)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("texts").set_defaults(func=cmd_texts)

    p = sub.add_parser("questions")
    p.add_argument("--project", required=True, choices=["p1", "p2", "p3"])
    p.add_argument("--composed", action="store_true",
                   help="show the exact F5-wrapped text the subject will receive")
    p.set_defaults(func=cmd_questions)

    p = sub.add_parser("open")
    p.add_argument("--project", required=True, choices=list(PROJECTS))
    p.add_argument("--run", type=int)
    p.add_argument("--key")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_open)

    p = sub.add_parser("nudge")
    p.add_argument("--session", required=True)
    p.set_defaults(func=cmd_nudge)

    p = sub.add_parser("ask")
    p.add_argument("--session", required=True)
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("digest")
    p.add_argument("--session", required=True)
    p.add_argument("--lines", type=int, default=0)
    p.set_defaults(func=cmd_digest)

    sub.add_parser("shakeout").set_defaults(func=cmd_shakeout)

    args = parser.parse_args()
    LOCAL_STORE.mkdir(parents=True, exist_ok=True)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
