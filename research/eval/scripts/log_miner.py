#!/usr/bin/env python3
"""WS3 session-log extraction: three log formats -> one session/turn schema.

Stdlib-only, read-only on every log store, all paths parameterised, so the
identical script runs inside a corporate environment against P8's Copilot CLI
logs (PLAN.md 5).

Sources (PLAN.md 4 / WS0 findings):

  1. claude_code    ~/.claude/projects/<munged>/<session>.jsonl
                    Two-sided and token-accounted, but retention-trimmed to the
                    most recent sessions. Used for assistant-side volume,
                    tokens, tool calls - and as an independent CHECK on the
                    human-turn counts, never as a second copy of them.
  2. claude_history ~/.claude/history.jsonl
                    Every user prompt since 2026-03-03 with project, sessionId
                    and timestamp. This is the canonical human-turn source for
                    all Claude Code work, which is what makes the altitude
                    analysis corpus-wide.
  3. copilot_jb     ~/.copilot/jb/<uuid>/partition-N.jsonl
                    Two-sided, Mar 20 - May 31, no token fields (bytes are the
                    volume proxy).

Definitions that must travel with the numbers:

  * HUMAN TURN. A turn typed by the operator. In claude_history that is one
    record. In claude_code transcripts, `type=="user"` records are NOT all
    human: tool results, `<task-notification>` blocks, compaction continuations
    and `[Request interrupted by user]` markers all wear the same type. They are
    filtered by SYNTHETIC_USER_RE and counted separately.
  * VERBATIM vs RENDERED. Copilot writes `user.message` (verbatim typed text)
    and `user.message_rendered` (the same turn with IDE file attachments
    prepended). 48 of its 57 sessions have ONLY a rendered record, and those
    read as machine-composed briefs in the third person ("The user wants ...").
    Rendered-only turns are carried with verbatim=false and are excluded from
    the altitude denominator by default: classifying them would measure the
    renderer, not the operator.
  * SLASH TURNS. `/clear`, `/model`, `/effort max` are operator actions but
    carry no altitude signal; kept, counted, excluded from the distribution.
    A trailing `/clear` is retained deliberately - it marks a deliberate context
    drop, which WS3(b) reads as the start of the next warm-up.
  * OFF-PROJECT TURNS. The log stores contain non-engineering work done in a
    corpus folder (phone malware forensics in the btest folder; phishing
    reporting in seam-reproduction). Flagged, counted, excluded - "how do I
    disable Phone Link" is not mechanical steering of a backtesting engine.

Usage:
  python log_miner.py --claude-dir ~/.claude/projects \
                      --history-file ~/.claude/history.jsonl \
                      --copilot-dir ~/.copilot/jb \
                      --out-dir ../data/session-metrics
"""

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from corpus_common import (  # noqa: E402
    CORPUS_PROJECTS, FOLDER_ALIASES, PROJECT_PATH_RE, canonical_project, eprint,
    iso_from_ms, iter_jsonl, norm_ws,
)

VERSION = "1.0"
PREVIEW_CHARS = 160

# --------------------------------------------------------------------------
# 1. synthetic "user" records in Claude Code transcripts
# --------------------------------------------------------------------------

# These wear type=="user" but nobody typed them. Anchored at the start of the
# message text; the list is exhaustive for this corpus and any unmatched
# oddity stays IN (a false human turn is visible in the sample, a silently
# dropped one is not).
SYNTHETIC_USER_RE = re.compile(
    r"^\s*(?:"
    r"<local-command-stdout>|<command-name>|<local-command-caveat>"
    r"|<task-notification>|<system-reminder>|<user-prompt-submit-hook>"
    r"|\[Request interrupted by user"
    r"|Caveat: The messages below were generated"
    r"|This session is being continued from a previous conversation"
    r"|API Error|\[No response requested\]"
    r")",
)

SLASH_RE = re.compile(r"^/([a-zA-Z][a-zA-Z0-9:_-]*)\s*(.*)$", re.DOTALL)

# --------------------------------------------------------------------------
# 2. project attribution
# --------------------------------------------------------------------------
#
# Folder attribution has known bleed (WS0: btest's first history entry is the
# b-autobot bootstrap prompt, pasted while sitting in the btest folder). Two
# rules re-attribute, both conservative, both reported separately, and every
# re-attributed turn is listed in the output so the call stays auditable.
#
#   RULE P (path)      - the turn names an explicit other-corpus-project path
#                        (PycharmProjects/<X>) and no path for its own folder.
#   RULE S (signature) - the turn carries >=2 markers of exactly one other
#                        corpus project and 0 markers of its own. Signatures are
#                        deliberately narrow: stack + domain tokens that cannot
#                        plausibly appear in the folder project's own work.

PROJECT_SIGNATURES = {
    "b-autobot": [
        "ag grid", "aggrid", "ag-grid", "cucumber", "stepdefs", "gherkin",
        "pom.xml", "maven", "java 21", "src/test/java", "finance demo",
        "b-autobot",
    ],
    "btest": [
        "btest", "quantdsl", "backtest", "eodhd", "tearsheet", "arcticdb",
        "vectorbt", "sp500", "factor engine",
    ],
    "blive": [
        "blive", "ib_algo", "ibkr", "interactive brokers", "accountsnapshot",
        "algo engine",
    ],
    "datacli": ["datacli", "data-ops shell", "eodhd>"],
    "smim": ["smim", "kim filter", "markov-switching", "oplearn"],
    "harp": ["harp", "harp paper", "liquidity adjustment", "pt-liqadj"],
    "seamQ": ["seamq", "seam paper", "seam_paper", "seam-reproduction"],
}

# Work done in a corpus folder that is not that project's engineering work.
# Narrow and published: each token is a whole different domain.
OFF_PROJECT_MARKERS = [
    "malware", "adb shell", "pixel 9", "phone link", "phishing", "scam domain",
    "scam website", "intune", "bootloader", "android",
    "printer", "brother mfc", "print job", "print queue", "printing",
    "test page", "spooler",
]


def _marker_re(marker):
    """Word-boundary match for alphanumeric markers so 'harp' does not fire on
    'sharp' and 'regime' does not fire on 'regimes of'. Markers containing
    punctuation or spaces are matched literally."""
    if re.fullmatch(r"[a-z0-9]+", marker):
        return re.compile(r"\b%s\b" % re.escape(marker))
    return re.compile(re.escape(marker))


_MARKER_CACHE = {}


def _hits(text_lower, markers):
    n = 0
    for m in markers:
        rx = _MARKER_CACHE.get(m)
        if rx is None:
            rx = _MARKER_CACHE[m] = _marker_re(m)
        if rx.search(text_lower):
            n += 1
    return n


def markers_for(text_lower, project):
    return _hits(text_lower, PROJECT_SIGNATURES.get(project, []))


RULES = {"windows": {}, "overrides": []}     # populated from attribution-rules.json


def in_window(project, ts):
    """Is `project` allowed to own a turn at `ts`? (see attribution-rules.json)

    Three corpus projects were EXTRACTED from btest (smim 2026-05-02, harp
    2026-04-08, datacli 2026-07-09) and one was designed weeks before its first
    commit (seamQ). Without a window, every pre-extraction 'docs/smim/...' turn
    inside btest is misread as smim-repo work.
    """
    w = RULES["windows"].get(project)
    if not w or not ts:
        return True
    day = str(ts)[:10]
    if w.get("start") and day < w["start"]:
        return False
    if w.get("end") and day > w["end"]:
        return False
    return True


def attribute(folder_project, text, ts=None):
    """-> (project, attribution_rule). Never returns None for project."""
    tl = (text or "").lower()

    # Guard: only corpus folders participate. The eval repo's own sessions
    # discuss every project by construction; re-attributing them would inject
    # meta-research turns into the projects being measured.
    if folder_project not in CORPUS_PROJECTS:
        return folder_project, "folder"

    # RULE P: explicit foreign path, no own path.
    paths = {canonical_project(m.group(1)) for m in PROJECT_PATH_RE.finditer(text or "")}
    foreign = {p for p in paths if p in CORPUS_PROJECTS and p != folder_project
               and in_window(p, ts)}
    if len(foreign) == 1 and folder_project not in paths:
        return foreign.pop(), "path"

    # RULE S: >=2 markers of exactly one other project, 0 of its own.
    if markers_for(tl, folder_project) == 0:
        hits = {p: markers_for(tl, p) for p in CORPUS_PROJECTS
                if p != folder_project and in_window(p, ts)}
        strong = [p for p, n in hits.items() if n >= 2]
        if len(strong) == 1:
            return strong[0], "signature"

    return folder_project, "folder"


def apply_override(turn):
    """Hand-adjudicated single-turn corrections (attribution-rules.json).

    Matched on session id + preview prefix rather than sequence number, so an
    override survives a turn being inserted earlier in the same session.
    """
    for ov in RULES["overrides"]:
        sid = ov["turn_id"].split(":")[1]
        if turn["session_id"] != sid:
            continue
        if not turn["preview"].startswith(ov["match_preview"][:40]):
            continue
        if turn["project"] != ov["verdict"]:
            turn["project"] = ov["verdict"]
            turn["attribution"] = "override"
        return True
    return False


def is_off_project(text, project):
    tl = (text or "").lower()
    if markers_for(tl, project) > 0:
        return False
    return _hits(tl, OFF_PROJECT_MARKERS) >= 2


def session_off_project(turns):
    """Whole-session off-project detection.

    A per-turn test is too weak on its own: an eight-turn printer-troubleshooting
    session inside the btest folder yields turns like "printer is on
    192.168.50.91" that carry a single marker each and slip through, while the
    session is unambiguously not btest work. So the markers are pooled across
    the session and the session must show ZERO markers of any corpus project
    before it is disqualified - a session that drifts into a printer problem and
    back to real work keeps all of its turns.
    """
    blob = " ".join((t["_full"] + " " + t["_paste"]) for t in turns).lower()
    if not blob.strip():
        return False
    if any(markers_for(blob, p) for p in CORPUS_PROJECTS):
        return False
    return _hits(blob, OFF_PROJECT_MARKERS) >= 2


# --------------------------------------------------------------------------
# 3. turn / session records
# --------------------------------------------------------------------------


def sha1(s):
    return hashlib.sha1((s or "").encode("utf-8", "replace")).hexdigest()[:12]


def make_turn(source, session_id, folder_raw, seq, ts, text,
              paste_text="", kind="prompt", verbatim=True):
    text = text or ""
    folder_project = canonical_project(folder_raw)
    slash = SLASH_RE.match(text.strip())
    cmd = None
    if kind == "prompt" and slash and "\n" not in text.strip():
        kind, cmd = "slash", slash.group(1).lower()
    joined = text + ("\n" + paste_text if paste_text else "")
    project, rule = attribute(folder_project, joined, ts)
    turn = {
        "turn_id": "%s:%s:%d" % (source, session_id, seq),
        "source": source,
        "session_id": session_id,
        "seq": seq,
        "ts": ts,
        "folder_project": folder_project,
        "folder_raw": folder_raw if folder_raw != folder_project else None,
        "project": project,
        "attribution": rule,
        "kind": kind,
        "slash_cmd": cmd,
        "verbatim": verbatim,
        "off_project": is_off_project(joined, project),
        "off_project_scope": "turn" if is_off_project(joined, project) else None,
        "chars": len(text),
        "words": len(text.split()),
        "paste_chars": len(paste_text),
        "has_paste": bool(paste_text),
        "sha1": sha1(text),
        "preview": norm_ws(text, PREVIEW_CHARS),
        "_full": text,          # stripped before the published JSON is written
        "_paste": paste_text,   # ditto
    }
    apply_override(turn)
    return turn


def blank_session(source, session_id, project):
    return {
        "session_id": session_id,
        "source": source,
        "project": project,
        "folder_project": project,
        "start_ts": None,
        "end_ts": None,
        "duration_min": None,
        "human_turns": 0,
        "slash_turns": 0,
        "rendered_turns": 0,
        "off_project_turns": 0,
        "off_project_session": False,
        "human_chars": 0,
        "paste_chars": 0,
        "assistant_msgs": 0,
        "tool_calls": 0,
        "sidechain_msgs": 0,
        "synthetic_user_records": 0,
        "tokens_in": 0,
        "tokens_out": 0,
        "tokens_cache_read": 0,
        "bytes": 0,
        "parse_errors": 0,
    }


def finish_session(s, turns):
    s["off_project_session"] = session_off_project(turns)
    if s["off_project_session"]:
        for t in turns:
            t["off_project"] = True
            t["off_project_scope"] = "session"
    ts = [t["ts"] for t in turns if t["ts"]]
    if ts:
        s["start_ts"] = s["start_ts"] or min(ts)
        s["end_ts"] = max([x for x in [s["end_ts"]] + ts if x])
    if s["start_ts"] and s["end_ts"]:
        try:
            a = datetime.fromisoformat(s["start_ts"].replace("Z", "+00:00"))
            b = datetime.fromisoformat(s["end_ts"].replace("Z", "+00:00"))
            s["duration_min"] = round((b - a).total_seconds() / 60.0, 1)
        except ValueError:
            pass
    s["human_turns"] = sum(1 for t in turns if t["kind"] == "prompt")
    s["slash_turns"] = sum(1 for t in turns if t["kind"] == "slash")
    s["rendered_turns"] = sum(1 for t in turns if t["kind"] == "rendered")
    s["off_project_turns"] = sum(1 for t in turns if t["off_project"])
    s["human_chars"] = sum(t["chars"] for t in turns if t["kind"] != "slash")
    s["paste_chars"] = sum(t["paste_chars"] for t in turns)
    # project = the modal project of its own turns (turn-level attribution wins)
    projs = Counter(t["project"] for t in turns if not t["off_project"])
    if projs:
        s["project"] = projs.most_common(1)[0][0]
    return s


# --------------------------------------------------------------------------
# 4. source parsers
# --------------------------------------------------------------------------


def parse_history(path):
    """~/.claude/history.jsonl -> (sessions, turns). One record == one turn."""
    by_session = defaultdict(list)
    order = []
    for obj, _raw in iter_jsonl(path):
        if obj is None:
            continue
        sid = obj.get("sessionId") or "unknown"
        if sid not in by_session:
            order.append(sid)
        by_session[sid].append(obj)

    sessions, turns = [], []
    for sid in order:
        recs = sorted(by_session[sid], key=lambda o: o.get("timestamp") or 0)
        raw = str(recs[0].get("project") or "").replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]
        folder = canonical_project(raw)
        s = blank_session("claude_history", sid, folder)
        s["folder_project"] = folder
        stur = []
        for i, o in enumerate(recs):
            pastes = (o.get("pastedContents") or {})
            paste_text = "\n".join(
                (p or {}).get("content") or "" for p in pastes.values()
            )
            t = make_turn("claude_history", sid, raw, i,
                          iso_from_ms(o.get("timestamp")),
                          o.get("display") or "", paste_text)
            stur.append(t)
        turns.extend(stur)
        sessions.append(finish_session(s, stur))
    return sessions, turns


def _cc_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text") or "" for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def parse_claude_code(project_dir):
    """One ~/.claude/projects/<munged>/ folder -> (sessions, turns)."""
    # The dir name is the full path with separators replaced by '-', so the
    # project is whatever follows the workspace root - split on that marker
    # rather than guessing at dash boundaries (b-autobot contains one).
    raw = (project_dir.name.split("PycharmProjects-")[-1]
           .split("IdeaProjects-")[-1])
    folder = canonical_project(raw)
    sessions, turns = [], []
    for f in sorted(project_dir.glob("*.jsonl")):
        sid = f.stem
        s = blank_session("claude_code", sid, folder)
        s["folder_project"] = folder
        s["bytes"] = f.stat().st_size
        stur = []
        seq = 0
        for obj, _raw in iter_jsonl(f):
            if obj is None:
                s["parse_errors"] += 1
                continue
            ts = obj.get("timestamp")
            if ts:
                if s["start_ts"] is None or ts < s["start_ts"]:
                    s["start_ts"] = ts
                if s["end_ts"] is None or ts > s["end_ts"]:
                    s["end_ts"] = ts
            typ = obj.get("type")
            msg = obj.get("message") if isinstance(obj.get("message"), dict) else {}
            usage = (msg or {}).get("usage") or {}
            if usage:
                s["tokens_in"] += usage.get("input_tokens", 0) or 0
                s["tokens_out"] += usage.get("output_tokens", 0) or 0
                s["tokens_cache_read"] += usage.get("cache_read_input_tokens", 0) or 0
            if obj.get("isSidechain"):
                if typ in ("user", "assistant"):
                    s["sidechain_msgs"] += 1
                continue                       # subagent traffic is never a human turn
            if typ == "assistant":
                s["assistant_msgs"] += 1
                content = (msg or {}).get("content")
                if isinstance(content, list):
                    s["tool_calls"] += sum(
                        1 for b in content
                        if isinstance(b, dict) and b.get("type") == "tool_use")
                continue
            if typ != "user":
                continue
            if obj.get("isMeta"):
                s["synthetic_user_records"] += 1
                continue
            content = (msg or {}).get("content")
            if isinstance(content, list):
                kinds = {b.get("type") for b in content if isinstance(b, dict)}
                if kinds and kinds <= {"tool_result"}:
                    s["synthetic_user_records"] += 1
                    continue
            text = _cc_text(content).strip()
            if not text or SYNTHETIC_USER_RE.match(text):
                s["synthetic_user_records"] += 1
                continue
            stur.append(make_turn("claude_code", sid, raw, seq, ts, text))
            seq += 1
        turns.extend(stur)
        sessions.append(finish_session(s, stur))
    return sessions, turns


ATTACH_RE = re.compile(r"^<attachments>.*?</attachments>\s*", re.DOTALL)
THIRD_PERSON_RE = re.compile(r"\bthe user (?:wants|asks|requests|would like)\b", re.I)


def parse_copilot(store_dir):
    """~/.copilot/jb/ -> (sessions, turns). Session folder == one conversation."""
    sessions, turns = [], []
    for d in sorted(store_dir.iterdir()):
        if not d.is_dir():
            continue
        parts = sorted(d.glob("partition-*.jsonl"))
        if not parts:
            continue
        sid = d.name
        s = blank_session("copilot_jb", sid, None)
        raw_msgs, rendered = {}, {}
        seq_order = []
        path_hits = Counter()
        for part in parts:
            s["bytes"] += part.stat().st_size
            for obj, raw in iter_jsonl(part):
                for m in PROJECT_PATH_RE.finditer(raw):
                    path_hits[canonical_project(m.group(1))] += 1
                if obj is None:
                    s["parse_errors"] += 1
                    continue
                ts = obj.get("timestamp")
                if ts:
                    if s["start_ts"] is None or ts < s["start_ts"]:
                        s["start_ts"] = ts
                    if s["end_ts"] is None or ts > s["end_ts"]:
                        s["end_ts"] = ts
                typ = obj.get("type", "")
                data = obj.get("data") or {}
                if typ == "user.message":
                    tid = data.get("turnId")
                    if tid not in raw_msgs:
                        seq_order.append(("raw", tid))
                    raw_msgs[tid] = (ts, data.get("content") or "")
                elif typ == "user.message_rendered":
                    tid = data.get("turnId")
                    if tid not in raw_msgs and tid not in rendered:
                        seq_order.append(("rendered", tid))
                    rendered[tid] = (ts, data.get("renderedMessage") or "")
                elif typ == "assistant.message":
                    s["assistant_msgs"] += 1
                elif typ == "tool.execution_start":
                    s["tool_calls"] += 1

        folder = (path_hits.most_common(1)[0][0] if path_hits else None) or "_unknown"
        s["folder_project"] = folder
        s["project"] = folder
        stur, seq = [], 0
        for kind, tid in seq_order:
            if tid in raw_msgs:
                ts, text = raw_msgs[tid]
                stur.append(make_turn("copilot_jb", sid, folder, seq, ts, text))
            else:
                ts, text = rendered[tid]
                stripped = ATTACH_RE.sub("", text)
                # An attachments-only render whose tail is the typed text is
                # still verbatim-ish; a third-person brief is not.
                verbatim = bool(ATTACH_RE.match(text)) and not THIRD_PERSON_RE.search(stripped)
                t = make_turn("copilot_jb", sid, folder, seq, ts, stripped,
                              kind="prompt" if verbatim else "rendered",
                              verbatim=verbatim)
                t["attachment_chars"] = len(text) - len(stripped)
                stur.append(t)
            seq += 1
        turns.extend(stur)
        sessions.append(finish_session(s, stur))
    return sessions, turns


# --------------------------------------------------------------------------
# 5. cross-source verification
# --------------------------------------------------------------------------


def verify_history_vs_transcripts(hist_turns, cc_turns):
    """Independent check: for sessions present in BOTH stores, do the two
    human-turn counts agree? They are produced by different filters over
    different files, so a match is real evidence the filters are right."""
    h = Counter(t["session_id"] for t in hist_turns if t["kind"] == "prompt")
    c = Counter(t["session_id"] for t in cc_turns if t["kind"] == "prompt")
    shared = sorted(set(h) & set(c))
    rows = []
    for sid in shared:
        rows.append({"session_id": sid, "history_prompts": h[sid],
                     "transcript_prompts": c[sid], "delta": h[sid] - c[sid]})
    exact = sum(1 for r in rows if r["delta"] == 0)
    within1 = sum(1 for r in rows if abs(r["delta"]) <= 1)
    return {
        "sessions_in_both_stores": len(rows),
        "exact_match": exact,
        "within_one_turn": within1,
        "per_session": rows,
        "note": (
            "history.jsonl and the transcripts are parsed by different filters "
            "over different files; the deltas that remain are queued/edited "
            "prompts recorded once but delivered differently. history.jsonl is "
            "the canonical human-turn source; transcript turns are NOT added to "
            "it, so no Claude Code turn is counted twice."
        ),
    }


# --------------------------------------------------------------------------
# 6. main
# --------------------------------------------------------------------------

DEFINITIONS = {
    "human_turn": "one operator-typed prompt; synthetic user records "
                  "(tool results, task notifications, interrupt markers, "
                  "compaction continuations, slash-command echoes) excluded",
    "slash_turn": "prompt whose whole text is a single /command; counted, "
                  "excluded from the altitude denominator",
    "rendered_turn": "Copilot user.message_rendered with no verbatim "
                     "user.message; machine-composed brief, excluded from the "
                     "altitude denominator by default",
    "off_project_turn": ">=2 off-domain markers and 0 markers of the folder "
                        "project; non-engineering work done in a corpus folder",
    "canonical_human_source": "claude_history for Claude Code, user.message for "
                              "Copilot; claude_code transcripts contribute "
                              "assistant/token/tool volume and a cross-check "
                              "only, never a second copy of the human turns",
    "paste_chars": "characters of pastedContents attached to a history prompt "
                   "(the operator's clipboard payload, not typed)",
    "attribution": "folder | path (explicit foreign project path) | signature "
                   "(>=2 foreign markers, 0 own) | alias (seam-reproduction -> "
                   "seamQ)",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claude-dir", type=Path, default=None)
    ap.add_argument("--history-file", type=Path, default=None)
    ap.add_argument("--copilot-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--rules", type=Path,
                    default=Path(__file__).resolve().parent.parent
                    / "data" / "attribution-rules.json",
                    help="hand-set attribution windows + overrides (script INPUT: "
                         "a re-run must not overwrite an adjudicated call)")
    ap.add_argument("--fulltext-dir", type=Path, default=None,
                    help="where verbatim turn text is written; defaults to "
                         "<out-dir>/local (gitignored - the published JSON "
                         "carries previews and hashes only)")
    ap.add_argument("--verification-note", default="",
                    help="hand-verification statement recorded in _meta")
    args = ap.parse_args()

    if args.rules and Path(args.rules).is_file():
        with open(args.rules, encoding="utf-8") as fh:
            loaded = json.load(fh)
        RULES["windows"] = {k: v for k, v in (loaded.get("windows") or {}).items()
                            if not k.startswith("_")}
        RULES["overrides"] = loaded.get("overrides") or []
        RULES["_file"] = str(args.rules)
    else:
        eprint("WARNING: no attribution-rules.json; running on heuristics alone")

    expand = lambda p: Path(os.path.expanduser(str(p))) if p else None
    claude_dir, hist_file = expand(args.claude_dir), expand(args.history_file)
    copilot_dir = expand(args.copilot_dir)
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    full_dir = args.fulltext_dir or (out_dir / "local")
    full_dir.mkdir(parents=True, exist_ok=True)

    sessions, turns = [], []
    hist_turns, cc_turns = [], []

    if hist_file and hist_file.is_file():
        s, t = parse_history(hist_file)
        sessions += s
        hist_turns = t
        turns += t
    if claude_dir and claude_dir.is_dir():
        for pdir in sorted(claude_dir.iterdir()):
            if not pdir.is_dir():
                continue
            s, t = parse_claude_code(pdir)
            sessions += s
            cc_turns += t
            turns += t
    if copilot_dir and copilot_dir.is_dir():
        s, t = parse_copilot(copilot_dir)
        sessions += s
        turns += t

    verification = verify_history_vs_transcripts(hist_turns, cc_turns)
    reattributed = [t for t in turns
                    if t["attribution"] in ("path", "signature", "override")]

    meta = {
        "script": "log_miner.py",
        "version": VERSION,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sources": {
            "claude_history": str(hist_file) if hist_file else None,
            "claude_code": str(claude_dir) if claude_dir else None,
            "copilot_jb": str(copilot_dir) if copilot_dir else None,
        },
        "definitions": DEFINITIONS,
        "folder_aliases": FOLDER_ALIASES,
        "attribution_rules_file": RULES.get("_file"),
        "attribution_windows": RULES["windows"],
        "cross_source_check": verification,
        "reattribution": {
            "turns_reattributed": len(reattributed),
            "turns_total": len(turns),
            "by_rule": dict(Counter(t["attribution"] for t in reattributed)),
            "moves": dict(Counter("%s->%s" % (t["folder_project"], t["project"])
                                  for t in reattributed)),
            "turns": [{"turn_id": t["turn_id"], "ts": t["ts"],
                       "from": t["folder_project"], "to": t["project"],
                       "rule": t["attribution"], "preview": t["preview"]}
                      for t in reattributed],
        },
        "off_project": {
            "turns": sum(1 for t in turns if t["off_project"]),
            "by_folder": dict(Counter(t["folder_project"] for t in turns
                                      if t["off_project"])),
        },
        "hand_verification": args.verification_note or None,
        "privacy_note": (
            "The published JSON carries a %d-character preview and a sha1 per "
            "turn. Verbatim prompt text is written to %s, which is gitignored: "
            "re-running the script reproduces it from the local log stores."
        ) % (PREVIEW_CHARS, full_dir.name),
    }

    # --- full text (local only) ---
    with open(full_dir / "turns-fulltext.jsonl", "w", encoding="utf-8") as fh:
        for t in turns:
            fh.write(json.dumps({"turn_id": t["turn_id"], "ts": t["ts"],
                                 "project": t["project"], "source": t["source"],
                                 "kind": t["kind"], "text": t["_full"],
                                 "paste": t["_paste"]}) + "\n")

    published = []
    for t in turns:
        p = {k: v for k, v in t.items() if not k.startswith("_")}
        published.append(p)

    with open(out_dir / "sessions.json", "w", encoding="utf-8") as fh:
        json.dump({"_meta": meta, "sessions": sessions}, fh, indent=2)
    with open(out_dir / "turns.json", "w", encoding="utf-8") as fh:
        json.dump({"_meta": meta, "turns": published}, fh, indent=2)

    # --- console summary (ASCII only) ---
    per = defaultdict(Counter)
    for t in turns:
        c = per[t["project"]]
        c["turns"] += 1
        c[t["kind"]] += 1
        c["off"] += 1 if t["off_project"] else 0
        c[t["source"]] += 1
        c["chars"] += t["chars"]
    print("%-18s %6s %6s %6s %6s %6s %7s %7s %7s" % (
        "project", "turns", "promp", "slash", "rendr", "off", "hist", "cc", "copilot"))
    print("-" * 78)
    for p, c in sorted(per.items(), key=lambda kv: -kv[1]["turns"]):
        print("%-18s %6d %6d %6d %6d %6d %7d %7d %7d" % (
            p or "?", c["turns"], c["prompt"], c["slash"], c["rendered"], c["off"],
            c["claude_history"], c["claude_code"], c["copilot_jb"]))
    print()
    print("sessions: %d  turns: %d  re-attributed: %d %s" % (
        len(sessions), len(turns), len(reattributed),
        meta["reattribution"]["by_rule"]))
    print("cross-source check: %d sessions in both stores, %d exact, %d within 1" % (
        verification["sessions_in_both_stores"], verification["exact_match"],
        verification["within_one_turn"]))
    print("wrote %s" % out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
