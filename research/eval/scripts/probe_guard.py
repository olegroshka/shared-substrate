#!/usr/bin/env python3
"""PreToolUse hook enforcing PROTOCOL H1 (repo-only access) for the WS4 probe.

Harness plumbing, not instrument: nothing the probe subject *sees* is defined
here. This hook is the hard half of H1's "tool allowlist that denies everything
else by default". The soft half (--allowedTools prefixes) is in probe_driver.py.

Why a hook is needed at all. Claude Code's `--allowedTools Read` allows reads of
ANY absolute path, including sibling repositories - which H1 forbids and which a
mechanics test confirmed the subject will happily do when asked. Path-scoped
rules (`Read(//<root>/**)`) fix Read, but Bash can still reach outside via
`git -C <other-repo>`, and Grep/Glob accept a `path` argument. This hook closes
all of those at the tool-call boundary.

Two rules, applied to every tool call:

  1. OUT-OF-TREE. Any path argument (file_path / path / notebook_path), or any
     absolute / parent-relative path appearing anywhere in a Bash command, that
     resolves outside PROBE_ROOT is denied. `git -C` is denied outright because
     it relocates the repository regardless of what follows.
  2. MUTATION. The probe must never modify a target repo (S5 standing
     constraint). Redirects and the writing git subcommands are denied even
     though the allowlist should already exclude them. Quoted segments are
     stripped before the redirect scan so `grep "=>" file` is not a false
     positive.

Every call is appended to PROBE_GUARD_LOG as one JSON line with its step id,
tool, decision and reason. That log is the published `access_attempts` evidence:
an agent that *reaches* for an extracted sibling repo is data (H1).

Reads stdin (the hook payload), writes a PreToolUse decision to stdout, exits 0.
A hook that cannot parse its input allows the call rather than corrupting a
session - the allowlist still applies underneath.
"""

import json
import os
import re
import sys
from pathlib import Path

PATH_KEYS = ("file_path", "path", "notebook_path")

# Absolute (C:\ or C:/), UNC-ish (//), home (~/) or parent-relative (../) paths.
PATH_IN_CMD = re.compile(r"""(?:^|[\s=:'"])((?:[A-Za-z]:[\\/]|//|~/|\.\./)[^\s'";|&)]*)""")

GIT_RELOCATE = re.compile(r"\bgit\s+(?:--\S+\s+)*-C\b")
CHDIR = re.compile(r"\b(?:cd|pushd)\s+([^\s;|&]+)")

MUTATING = re.compile(
    r"\b(?:"
    r"rm|mv|cp|mkdir|rmdir|touch|truncate|chmod|chown|tee|ln|"
    r"git\s+(?:add|commit|checkout|switch|reset|clean|stash|push|pull|fetch|"
    r"merge|rebase|restore|rm|mv|apply|am|cherry-pick|revert|gc|prune|"
    r"worktree|init|clone|tag\s+-|branch\s+-[dDmM])"
    r")\b"
)
SED_INPLACE = re.compile(r"\bsed\b[^|;&]*\s-i\b")
QUOTED = re.compile("'[^']*'" + '|"[^"]*"')
# Stream plumbing that writes nothing: `2>&1`, `2>/dev/null`, `>NUL`. Stripped
# before the redirect scan so they are not mistaken for a file write.
NULL_REDIRECT = re.compile(r"\d?>\s*&\s*\d|\d?>\s*(?:/dev/null|NUL)\b", re.IGNORECASE)


def outside(root: Path, raw) -> bool:
    """True if `raw` resolves anywhere other than root or below it."""
    if not raw:
        return False
    try:
        cand = Path(str(raw).strip().strip("'\""))
        if not cand.is_absolute():
            cand = root / cand
        cand = cand.resolve()
    except (OSError, ValueError):
        return False
    return cand != root and root not in cand.parents


def check(root: Path, tool: str, ti: dict):
    """Return a deny reason, or None to allow."""
    for key in PATH_KEYS:
        if outside(root, ti.get(key)):
            return f"out-of-tree {key}={ti.get(key)!r}"

    if tool != "Bash":
        return None

    cmd = str(ti.get("command", ""))
    if GIT_RELOCATE.search(cmd):
        return "git -C relocates the repository"
    for target in CHDIR.findall(cmd):
        if outside(root, target):
            return f"chdir out of the tree: {target!r}"
    for match in PATH_IN_CMD.findall(cmd):
        if outside(root, match):
            return f"out-of-tree path in command: {match!r}"

    unquoted = NULL_REDIRECT.sub(" ", QUOTED.sub(" ", cmd))
    if ">" in unquoted:
        return "output redirection (the probe never writes to a target repo)"
    if MUTATING.search(unquoted) or SED_INPLACE.search(unquoted):
        return "mutating command (the probe never writes to a target repo)"
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    root = Path(os.environ.get("PROBE_ROOT", ".")).resolve()
    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input") or {}
    reason = check(root, tool, ti)

    log = os.environ.get("PROBE_GUARD_LOG")
    if log:
        record = {
            "step": os.environ.get("PROBE_STEP", ""),
            "tool": tool,
            "decision": "deny" if reason else "allow",
            "reason": reason,
            "tool_input": {k: str(v)[:400] for k, v in ti.items()},
        }
        try:
            with open(log, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError:
            pass

    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "PROBE HARNESS: this session is restricted to the current "
                f"repository. Denied: {reason}."),
        }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
