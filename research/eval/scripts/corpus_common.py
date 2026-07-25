#!/usr/bin/env python3
"""Shared helpers for the WS2 / WS-X miners.

Stdlib-only. No project-specific constants beyond the file-classification
tables, which are stated here once so `git_miner.py` and `complexity_profile.py`
cannot drift apart in what they call a "source file".

Portability note (PLAN.md 5): this module runs unmodified inside a corporate
environment; it shells out to `git` only, never to the network.
"""

import re
import subprocess
import sys

# --------------------------------------------------------------------------
# Path classification
# --------------------------------------------------------------------------

# Vendored / generated trees. Excluded from EVERY metric, because a single
# `git add node_modules` would otherwise dominate size, churn and entropy.
# The count of what this removes is itself reported (it is a hygiene finding).
VENDORED_RE = re.compile(
    r"(^|/)("
    r"node_modules|vendor|third_party|thirdparty|bower_components"
    r"|\.venv|venv|site-packages|\.tox|\.eggs|[^/]+\.egg-info"
    r"|dist|build|target|assets_dist|\.next|\.nuxt|\.gradle"
    r"|__pycache__|\.mypy_cache|\.pytest_cache|\.ruff_cache"
    r"|htmlcov|coverage"
    r")(/|$)",
    re.IGNORECASE,
)

GENERATED_FILE_RE = re.compile(
    r"(\.min\.(js|css)|\.map"
    r"|package-lock\.json|yarn\.lock|pnpm-lock\.yaml|uv\.lock|poetry\.lock"
    r"|Cargo\.lock|composer\.lock)$",
    re.IGNORECASE,
)

# Extension -> (tier, language). Tiers: code | docs | config.
# Allowlist rather than denylist: a repo tracking 3782 parquet files (btest)
# or 25 PNGs (smim) must not have them counted as source.
EXT_TABLE = {
    # --- code ---
    "py": ("code", "Python"), "pyi": ("code", "Python"),
    "java": ("code", "Java"), "kt": ("code", "Kotlin"),
    "scala": ("code", "Scala"), "groovy": ("code", "Groovy"),
    "js": ("code", "JavaScript"), "jsx": ("code", "JavaScript"),
    "mjs": ("code", "JavaScript"), "cjs": ("code", "JavaScript"),
    "ts": ("code", "TypeScript"), "tsx": ("code", "TypeScript"),
    "mts": ("code", "TypeScript"), "cts": ("code", "TypeScript"),
    "go": ("code", "Go"), "rs": ("code", "Rust"),
    "c": ("code", "C"), "h": ("code", "C"),
    "cpp": ("code", "C++"), "cc": ("code", "C++"), "hpp": ("code", "C++"),
    "cs": ("code", "C#"), "rb": ("code", "Ruby"), "php": ("code", "PHP"),
    "sh": ("code", "Shell"), "bash": ("code", "Shell"),
    "ps1": ("code", "PowerShell"), "psm1": ("code", "PowerShell"),
    "bat": ("code", "Batch"), "cmd": ("code", "Batch"),
    "sql": ("code", "SQL"), "r": ("code", "R"), "jl": ("code", "Julia"),
    "m": ("code", "MATLAB"), "swift": ("code", "Swift"),
    "html": ("code", "HTML"), "css": ("code", "CSS"),
    "scss": ("code", "CSS"), "less": ("code", "CSS"),
    "vue": ("code", "Vue"), "svelte": ("code", "Svelte"),
    "feature": ("code", "Gherkin"),
    "ipynb": ("code", "Notebook"),
    # --- docs (authored prose; the substrate itself lives here) ---
    "md": ("docs", "Markdown"), "markdown": ("docs", "Markdown"),
    "rst": ("docs", "reST"), "adoc": ("docs", "AsciiDoc"),
    "txt": ("docs", "Text"), "tex": ("docs", "LaTeX"),
    "bib": ("docs", "BibTeX"),
    # --- config ---
    "yaml": ("config", "YAML"), "yml": ("config", "YAML"),
    "toml": ("config", "TOML"), "json": ("config", "JSON"),
    "xml": ("config", "XML"), "ini": ("config", "INI"),
    "cfg": ("config", "INI"), "conf": ("config", "Conf"),
    "properties": ("config", "Properties"),
    "gradle": ("config", "Gradle"), "example": ("config", "Example"),
}

# Extensionless files and dotfiles that are still source. (A leading-dot name
# such as ".gitignore" has no extension by the split_ext rule, so it must be
# named here explicitly - this cost 37 lines of silent undercount on seamQ
# before it was caught by hand-verification.)
BASENAME_TABLE = {
    "dockerfile": ("config", "Dockerfile"),
    "makefile": ("config", "Makefile"),
    "justfile": ("config", "Justfile"),
    "procfile": ("config", "Procfile"),
    "license": ("docs", "Text"),
    "notice": ("docs", "Text"),
    ".gitignore": ("config", "Gitignore"),
    ".gitattributes": ("config", "Gitignore"),
    ".dockerignore": ("config", "Gitignore"),
    ".editorconfig": ("config", "Conf"),
    ".env.example": ("config", "Example"),
}

TEST_DIR_RE = re.compile(
    r"(^|/)(tests?|testing|spec|specs|__tests__|features|it)(/|$)", re.IGNORECASE
)
TEST_FILE_RE = re.compile(
    r"(^|/)("
    r"test_[^/]+\.py|[^/]+_test\.py|conftest\.py"
    r"|[^/]*Test\.java|[^/]*Tests\.java|[^/]*IT\.java|[^/]*ITCase\.java"
    r"|[^/]+\.(test|spec)\.[jt]sx?"
    r"|[^/]+\.feature"
    r")$",
    re.IGNORECASE,
)


def split_ext(path):
    """-> (basename_lower, ext_lower_without_dot)."""
    base = path.rsplit("/", 1)[-1].lower()
    ext = base.rsplit(".", 1)[-1] if "." in base[1:] else ""
    return base, ext


def is_vendored(path):
    return bool(VENDORED_RE.search(path) or GENERATED_FILE_RE.search(path))


def classify(path):
    """-> (tier, language) or (None, None) if not a source file.

    Vendored/generated paths return (None, None); callers that need the
    vendored count call is_vendored() separately.
    """
    if is_vendored(path):
        return None, None
    base, ext = split_ext(path)
    if ext and ext in EXT_TABLE:
        return EXT_TABLE[ext]
    if base in BASENAME_TABLE:
        return BASENAME_TABLE[base]
    if base.startswith("dockerfile"):
        return BASENAME_TABLE["dockerfile"]
    return None, None


def is_source(path):
    return classify(path)[0] is not None


def is_test_file(path):
    """Test file = a source file living in a test tree or carrying a test-file
    naming convention. Vendored paths never count (b-autobot's node_modules
    sit under src/test/webapp/, which would otherwise inflate the count 60x)."""
    if not is_source(path):
        return False
    return bool(TEST_DIR_RE.search(path) or TEST_FILE_RE.search(path))


# --------------------------------------------------------------------------
# git plumbing (read-only)
# --------------------------------------------------------------------------

# --no-optional-locks: never take the index lock, so a concurrent IDE or a
# read-only checkout is safe. Nothing here writes to the target repo.
GIT_BASE = ["git", "--no-optional-locks"]


def git(repo, *args, check=True):
    """Run a read-only git command in `repo`; return stdout as text."""
    proc = subprocess.run(
        GIT_BASE + ["-C", str(repo)] + list(args),
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if check and proc.returncode != 0:
        raise RuntimeError(
            "git %s failed in %s: %s" % (" ".join(args), repo, proc.stderr.strip())
        )
    return proc.stdout


def git_version():
    try:
        return subprocess.run(
            ["git", "--version"], capture_output=True, text=True
        ).stdout.strip()
    except OSError:
        return "unknown"


_RENAME_BRACE_RE = re.compile(r"\{(.*?) => (.*?)\}")


def normalize_numstat_path(field):
    """Resolve git's rename notation in a --numstat path field.

    Handles both forms git emits:
      'old/path.py => new/path.py'
      'src/{old => new}/file.py'   (and '{ => new}/file.py')
    Returns (old_path_or_None, new_path). Paths are normalised to forward
    slashes with collapsed doubles.
    """
    field = field.strip().strip('"')
    if " => " not in field:
        return None, field
    m = _RENAME_BRACE_RE.search(field)
    if m:
        old = (field[: m.start()] + m.group(1) + field[m.end():])
        new = (field[: m.start()] + m.group(2) + field[m.end():])
    else:
        old, new = field.split(" => ", 1)
    clean = lambda p: re.sub(r"/{2,}", "/", p).strip("/")
    return clean(old), clean(new)


class Commit:
    __slots__ = ("sha", "ts", "iso", "subject", "files")

    def __init__(self, sha, ts, iso, subject):
        self.sha = sha
        self.ts = ts          # int, unix seconds (author date)
        self.iso = iso        # ISO-8601 author date
        self.subject = subject
        self.files = []       # list of (added|None, deleted|None, old, new)

    @property
    def month(self):
        return self.iso[:7]

    @property
    def quarter(self):
        y, m = int(self.iso[:4]), int(self.iso[5:7])
        return "%d-Q%d" % (y, (m - 1) // 3 + 1)


REC = "\x01"
FS = "\x1f"


def read_log(repo, no_merges=True):
    """Full history with per-file numstat, oldest first.

    Merge commits are excluded by default: their numstat double-counts the
    lines already attributed to the merged-in commits.
    """
    args = ["log", "--reverse", "-M", "--numstat",
            "--pretty=format:%s%%H%s%%at%s%%aI%s%%s" % (REC, FS, FS, FS)]
    if no_merges:
        args.insert(1, "--no-merges")
    out = git(repo, *args)
    commits = []
    for chunk in out.split(REC):
        if not chunk.strip():
            continue
        lines = chunk.split("\n")
        parts = lines[0].split(FS)
        if len(parts) < 4:
            continue
        sha, ts, iso, subject = parts[0], parts[1], parts[2], FS.join(parts[3:])
        c = Commit(sha, int(ts), iso, subject)
        for line in lines[1:]:
            if not line.strip():
                continue
            bits = line.split("\t")
            if len(bits) < 3:
                continue
            a, d, path = bits[0], bits[1], "\t".join(bits[2:])
            old, new = normalize_numstat_path(path)
            added = None if a == "-" else int(a)     # '-' == binary file
            deleted = None if d == "-" else int(d)
            c.files.append((added, deleted, old, new))
        commits.append(c)
    return commits


def count_merges(repo):
    out = git(repo, "rev-list", "--count", "--merges", "HEAD", check=False)
    try:
        return int(out.strip())
    except ValueError:
        return 0


def eprint(*a):
    """ASCII-only stderr (Windows console is cp1252 - no arrows, no unicode)."""
    print(*a, file=sys.stderr)
