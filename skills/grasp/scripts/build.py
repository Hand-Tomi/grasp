#!/usr/bin/env python3
"""Build the grasp deep-mode page: validate the JSON, embed it in the template, write HTML.

Usage:
  python3 build.py data.json [--out PATH] [--open] [--no-verify]

Exit code 0 means the page was written. Errors are printed one per line and must be
fixed before the page is shown to the user. Warnings are printed but do not block.
Standard library only.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import datetime as dt
import html
import json
import math
import posixpath
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "template.html"

KINDS = ("code", "report")
GRADES = ("red", "yellow", "gray")
LEVELS = ("run", "read", "claimed", "inferred", "unverified")
VISUALS = ("mermaid", "before_after", "trace", "table", "code")
EDITORS = ("vscode", "vscode-insiders", "cursor", "windsurf", "idea")
MERMAID_KINDS = (
    "flowchart", "graph", "sequenceDiagram", "stateDiagram", "stateDiagram-v2", "classDiagram",
    "erDiagram", "timeline", "gantt", "journey", "mindmap", "quadrantChart", "gitGraph", "pie",
)
MAX_FILE_BYTES = 2_000_000
MAX_SOURCE_BYTES = 5_000_000      # a referenced source file or blob
MAX_CACHE_BYTES = 50_000_000      # all referenced sources together
MAX_STR = 20_000
MAX_TERM = 60
MAX_LIST = 60
MAX_CHUNKS_SOFT, MAX_CHUNKS_HARD = 4, 6
MAX_VISUALS_PER_CHUNK = 3
MAX_LOOK = 3
MAX_ANSWER_LOOK = 3
MAX_POINTS = 3
MAX_GLOSSARY = 8
MAX_MERMAID_LINES = 40
MAX_MERMAID_CHARS = 8000
MAX_MERMAID_LINE = 400
MAX_BRANCHES = 4
SAFE_INT = 2**53 - 1
COLUMN_PX = 860            # content column width in the template
OVERVIEW_MAX_H = 650       # the map's diagram sits above the chunk list, so it must stay short
MIN_SCALE = 0.75           # the template never shrinks a diagram below this
EXPECTATION_RE = re.compile(r"야[\s하?]|야$|기대|바라|원하|기준|조건|승인|괜찮|should|expect|want|accept", re.I)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(safe(f"ERROR {where}: {msg}"))

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(safe(f"WARN  {where}: {msg}"))


def safe(text: str) -> str:
    """Untrusted values end up in diagnostics; never let them send terminal control sequences."""
    return "".join(ch if ch == "\n" or (ord(ch) >= 0x20 and ord(ch) != 0x7F and not 0x80 <= ord(ch) < 0xA0)
                   else f"\\x{ord(ch):02x}" for ch in text)


def is_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def pos_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= SAFE_INT


def has_surrogate(s: str) -> bool:
    return any(0xD800 <= ord(ch) <= 0xDFFF for ch in s)


def valid_rev(v) -> bool:
    """Shape only; git itself decides whether the name exists (see resolve_rev)."""
    return (isinstance(v, str) and 0 < len(v) <= 200 and not v.startswith("-") and ":" not in v
            and not any(ch.isspace() or ord(ch) < 0x20 or ord(ch) == 0x7F for ch in v) and not has_surrogate(v))


_REV_CACHE: dict = {}


def resolve_rev(root: Path, rev: str) -> str | None:
    """Commit id for a revision name, or None. Later git reads use the id, never the name."""
    key = (str(root), rev)
    if key not in _REV_CACHE:
        out = _git(root, "rev-parse", "--verify", "--quiet", "--end-of-options", rev + "^{commit}")
        oid = out.decode("ascii", "replace").strip() if out else ""
        _REV_CACHE[key] = oid if re.fullmatch(r"[0-9a-f]{40,64}", oid) else None
    return _REV_CACHE[key]


def physical_lines(text: str) -> list[str]:
    """Split on \\n only (not U+2028 etc.), the same way the template and git do."""
    if text == "":
        return []
    if text.endswith("\n"):
        text = text[:-1]
    return text.split("\n")


def excerpt_lines(code: str) -> list[str]:
    # Must match the template: drop all trailing newlines, split on \n.
    return code.rstrip("\n").split("\n")


# ---- schema -----------------------------------------------------------------
# Every field the template reads is listed here with its type, so a page that
# validates can never crash on a wrong type. Unknown keys are reported (typos).

S, I, B, CELL = "str", "int", "bool", "cell"
REF = {"file": S, "line": I, "end": I, "rev": S, "what": S}
SIDE = {"label": S, "code": S, "text": S, "lang": S}
VISUAL = {"type": S, "title": S, "caption": S, "evidence": S, "source": S, "before": SIDE, "after": SIDE,
          "columns": [S], "rows": [[CELL]], "highlight_rows": [I], "column_rev": {},
          "file": S, "start_line": I, "rev": S, "code": S, "lang": S, "highlight": [I],
          "notes": [{"line": I, "text": S}]}
QUESTION = {"question": S, "answer": S, "explain": S, "evidence": S, "look": [REF], "points": [S], "repro": S,
            "user_answer": S, "gap": S}
CHUNK = {"id": I, "grade": S, "title": S, "size": S, "summary": S, "skip_reason": S, "unrequested": B,
         "spot_check": {**REF, "command": S}, "predict": QUESTION, "check": QUESTION, "why": S, "visuals": [VISUAL],
         "example": S, "look": [REF], "cautions": [{"text": S, "evidence": S}]}
DOC = {"kind": S, "title": S, "target": S, "purpose": S, "bottom_line": S, "your_action": S,
       "doc": {"date": S, "status": S, "latest": S},
       "unverified": [S], "not_read": [S], "corrections": [S], "root": S, "rev": S, "editor": S, "source_file": S,
       "overview": VISUAL, "glossary": [{"term": S, "def": S}], "chunks": [CHUNK],
       "teach_back": S, "wrap_up": {"remember": [S], "skipped": [S], "open": [S]}}


def check_types(v, spec, where: str, r: Report) -> None:
    if isinstance(spec, dict) and spec:
        if not isinstance(v, dict):
            r.err(where, "must be an object")
            return
        for k, val in v.items():
            if k not in spec:
                r.warn(where, f"unknown field `{k}` is ignored (typo?)")
                continue
            if val is None:
                continue
            check_types(val, spec[k], f"{where}.{k}" if where else k, r)
    elif isinstance(spec, list):
        if not isinstance(v, list):
            r.err(where, "must be a list")
            return
        if len(v) > MAX_LIST:
            r.err(where, f"{len(v)} items; keep it under {MAX_LIST}")
            return
        for i, item in enumerate(v):
            check_types(item, spec[0], f"{where}[{i}]", r)
    elif spec == {}:
        if not isinstance(v, dict) or not all(isinstance(k, str) and re.fullmatch(r"[0-9]{1,3}", k) and isinstance(x, str) for k, x in v.items()):
            r.err(where, 'must map column numbers to revisions, e.g. {"1": "abc123~1"}')
    elif spec == S:
        if not isinstance(v, str):
            r.err(where, "must be a string")
        elif len(v) > MAX_STR:
            r.err(where, f"string is {len(v)} characters; keep it under {MAX_STR}")
    elif spec == I:
        if not (isinstance(v, int) and not isinstance(v, bool) and -SAFE_INT <= v <= SAFE_INT):
            r.err(where, "must be an integer within the JavaScript safe range")
    elif spec == B:
        if not isinstance(v, bool):
            r.err(where, "must be true or false")
    elif spec == CELL:
        if isinstance(v, bool) or not isinstance(v, (str, int, float)):
            r.err(where, "table cells must be text or numbers")
        elif isinstance(v, int) and abs(v) > SAFE_INT:
            r.err(where, "number too large; write it as text")
        elif isinstance(v, str) and len(v) > MAX_STR:
            r.err(where, "cell text too long")


# ---- Mermaid ----------------------------------------------------------------

_SHAPE = r"(\[\(|\(\(|\(\[|\[\[|\{\{|\[/|\[\\|\[|\(|\{)"
_CLOSER = r"(\)\]|\)\)|\]\)|\]\]|\}\}|/\]|\\\]|\]|\)|\})"
_UNQUOTED_LABEL = re.compile(r"\b[\w-]+" + _SHAPE + r"(?![\"])([^\"\n]{0,200}?)" + _CLOSER)
_ARROW = re.compile(r"(-->|---|-\.->|==>|--\s*[^\n>]{0,80}?-->|-\.\s*[^\n>]{0,80}?\.->)")


def check_mermaid(src, where: str, r: Report) -> None:
    if not is_str(src):
        r.err(where, "mermaid `source` is empty")
        return
    if len(src) > MAX_MERMAID_CHARS:
        r.err(where, f"diagram source is {len(src)} characters; keep it under {MAX_MERMAID_CHARS}")
        return
    raw = src.split("\n")
    if any(len(ln) > MAX_MERMAID_LINE for ln in raw):
        r.err(where, f"a diagram line is longer than {MAX_MERMAID_LINE} characters; shorten the labels")
        return
    first = src.strip().split("\n")[0].strip()
    kind = first.split()[0] if first.split() else ""
    if kind not in MERMAID_KINDS:
        r.err(where, f"mermaid must start with a diagram type ({', '.join(MERMAID_KINDS[:6])}, ...), got {first[:40]!r}")
    if len([ln for ln in raw if ln.strip()]) > MAX_MERMAID_LINES:
        r.warn(where, f"diagram has more than {MAX_MERMAID_LINES} lines; split it")
    if "`" in src:
        r.err(where, "remove backticks from Mermaid source; they switch labels into markdown mode")
    if re.search(r"(^|;)\s*(click|href|link|links)\b", src, re.M) or "javascript:" in src.lower():
        r.err(where, "links in diagrams (`click`, `href`) are not allowed; put file:line refs in the text instead")
    if kind == "timeline":
        r.warn(where, "timeline diagrams render wide and with low contrast in dark mode; prefer a table (시점 / 상태 / 내용)")
    if kind == "sequenceDiagram":
        for ln in raw:
            if re.match(r"\s*participant\s+\S+\s+as\s+\"", ln):
                r.warn(where, "sequenceDiagram shows quotes in `participant X as \"...\"` literally; drop the quotes")
            if re.search(r":.*[;#]", ln):
                r.warn(where, f"';' or '#' in a sequence message breaks parsing: {ln.strip()[:50]!r}")
    if kind in ("flowchart", "graph", "stateDiagram", "stateDiagram-v2"):
        for ln in raw:
            for m in re.finditer(r'"[^"\n]*#[^"\n]*"', ln):
                if not re.search(r"#\w+;", m.group(0)):
                    r.warn(where, f"'#' inside label {m.group(0)[:50]!r} may be read as an entity code; spell it out")
    if kind in ("flowchart", "graph"):
        fan: dict[str, int] = {}
        diamonds = 0
        for ln in raw:
            for m in _UNQUOTED_LABEL.finditer(ln):
                if re.search(r"[()\[\]{}]", m.group(2)):
                    r.err(where, f"unquoted flowchart label with brackets: {m.group(0)[:60]!r}. Wrap the label in double quotes: A[\"...\"]")
            if re.search(r"<[a-zA-Z/]", ln):
                r.warn(where, "HTML tags in labels are stripped in strict mode; use plain text")
            diamonds += len(re.findall(r"\b[\w-]+\{(?!\{)", ln))
            head = re.match(r"\s*([\w-]+)", ln)
            if head and _ARROW.search(ln):
                fan[head.group(1)] = fan.get(head.group(1), 0) + 1
        wide = [k for k, n in fan.items() if n > MAX_BRANCHES]
        if wide:
            r.warn(where, f"node(s) {', '.join(wide[:5])} branch more than {MAX_BRANCHES} ways; the diagram will be too wide to read. Split or group")
        if diamonds > 2:
            r.warn(where, f"{diamonds} decision diamonds; they take a lot of space. Prefer rectangles with labelled edges")


# ---- files ------------------------------------------------------------------

_FILE_CACHE: dict = {}
_CACHE_BYTES = [0]
_LOSSY: set = set()


def _git(root: Path, *args: str) -> bytes | None:
    try:
        # fsmonitor is a configurable command; reading files must never run one.
        out = subprocess.run(["git", "-c", "core.fsmonitor=false", "-C", str(root), *args], capture_output=True, check=True, timeout=20)
    except (subprocess.SubprocessError, OSError, UnicodeError, ValueError):
        return None
    return out.stdout


def read_lines(root: Path, rel: str, rev: str | None) -> list[str] | None:
    """Lines of a regular file under root (at a git revision if given). None if unreadable."""
    key = (str(root), rel, rev)
    if key in _FILE_CACHE:
        return _FILE_CACHE[key]
    raw = None
    bad = (rel.startswith(("/", "\\", "-")) or ".." in rel.split("/") or "\x00" in rel or "\\" in rel
           or ":" in rel or has_surrogate(rel) or rel.strip() != rel or posixpath.normpath(rel) != rel
           or len(rel) > 1000)
    if not bad and rev:
        # ls-tree resolves the path relative to root (the -C directory), so a ref cannot
        # reach files outside root; mode 100644/100755 excludes trees, symlinks and submodules.
        oid = resolve_rev(root, rev)
        listing = _git(root, "ls-tree", "-z", oid, "--", rel) if oid else None
        if listing:
            meta, _, path = listing.rstrip(b"\x00").partition(b"\t")
            parts = meta.split()
            if len(parts) == 3 and parts[0] in (b"100644", b"100755") and parts[1] == b"blob" and b"\x00" not in path:
                sha = parts[2].decode("ascii", "replace")
                size = _git(root, "cat-file", "-s", sha)
                if size is not None and size.strip().isdigit() and int(size) <= MAX_SOURCE_BYTES:
                    raw = _git(root, "cat-file", "blob", sha)
    elif not bad:
        p = root / rel
        try:
            if not p.is_symlink() and p.is_file() and p.stat().st_size <= MAX_SOURCE_BYTES:
                p.resolve().relative_to(root.resolve())
                raw = p.read_bytes()
        except (ValueError, OSError, RuntimeError):
            raw = None
    if raw is not None and _CACHE_BYTES[0] + len(raw) > MAX_CACHE_BYTES:
        raw = None
    lines = None
    if raw is not None:
        try:
            lines = physical_lines(raw.decode("utf-8"))
        except UnicodeDecodeError:
            lines = physical_lines(raw.decode("utf-8", "replace"))
            _LOSSY.add(key)
    if raw is not None:
        _CACHE_BYTES[0] += len(raw)
    _FILE_CACHE[key] = lines
    return lines


class Ctx:
    def __init__(self) -> None:
        self.root: Path | None = None
        self.rev: str | None = None


def check_ref(ref, where: str, ctx: Ctx, r: Report, need_what: bool = True) -> tuple[str, int, int] | None:
    if not isinstance(ref, dict) or not is_str(ref.get("file")):
        r.err(where, "needs `file`")
        return None
    line, end = ref.get("line"), ref.get("end", ref.get("line"))
    if not pos_int(line):
        r.err(where, "`line` must be a positive integer")
        return None
    if not pos_int(end) or end < line:
        r.err(where, "`end` must be an integer >= `line`")
        return None
    if need_what and not is_str(ref.get("what")):
        r.err(where, "`what` required: what to check at that line")
    if "rev" in ref and not valid_rev(ref["rev"]):
        r.err(where, "`rev` must be a commit, tag or branch name")
        return None
    if ctx.root is None:
        return (ref["file"], line, end)
    rev = ref.get("rev") or ctx.rev
    lines = read_lines(ctx.root, ref["file"], rev)
    if lines is None:
        r.err(where, f"{ref['file']}{' at ' + rev if rev else ''} is not a readable regular file under root (normalized relative path, under {MAX_SOURCE_BYTES // 1_000_000} MB)")
        return None
    if end > len(lines):
        r.err(where, f"{ref['file']}:{line}-{end} is past the end of the file ({len(lines)} lines)")
        return None
    if (str(ctx.root), ref["file"], rev) in _LOSSY:
        r.warn(where, f"{ref['file']} is not valid UTF-8, so the page cannot show its lines (the chip offers the path or git command)")
    snip(ctx, ref["file"], line, end, rev)
    return (ref["file"], line, end)


def check_excerpt(v: dict, where: str, ctx: Ctx, r: Report) -> tuple[str, int, int] | None:
    """A code visual must match the file exactly. Only a trailing carriage return is ignored."""
    start = v.get("start_line", 1)
    if not pos_int(start):
        r.err(where, "`start_line` must be a positive integer")
        return None
    excerpt = excerpt_lines(v["code"])
    end = start + len(excerpt) - 1
    if not is_str(v.get("file")):
        if ctx.root is not None:
            r.warn(where, "code visual has no `file`; it cannot be checked against the source")
        return None
    if "rev" in v and not valid_rev(v["rev"]):
        r.err(where, "`rev` must be a commit, tag or branch name")
        return None
    if ctx.root is None:
        return (v["file"], start, end)
    rev = v.get("rev") or ctx.rev
    lines = read_lines(ctx.root, v["file"], rev)
    if lines is None:
        r.err(where, f"{v['file']}{' at ' + rev if rev else ''} is not a readable regular file under root")
        return None
    if end > len(lines):
        r.err(where, f"excerpt {v['file']}:{start}-{end} runs past the end of the file ({len(lines)} lines)")
        return None
    if (str(ctx.root), v["file"], rev) in _LOSSY:
        r.err(where, f"{v['file']} is not valid UTF-8, so the excerpt cannot be checked exactly; quote it as text instead")
        return None
    for i, got in enumerate(excerpt):
        want = lines[start - 1 + i]
        if got.removesuffix("\r") != want.removesuffix("\r"):
            r.err(where, f"excerpt differs from {v['file']}:{start + i} (copy the line exactly, including spaces and tabs)\n        file:    {want.rstrip(chr(13))[:120]!r}\n        excerpt: {got.rstrip(chr(13))[:120]!r}")
            return None
    for j, n in enumerate(v.get("notes") or []):
        if isinstance(n, dict) and isinstance(n.get("line"), int) and not (start <= n["line"] <= end):
            r.warn(f"{where}.notes[{j}]", f"line {n['line']} is outside the excerpt ({start}-{end}); the note will not show")
    return (v["file"], start, end)


# ---- visuals and questions --------------------------------------------------

def check_visual(v, where: str, ctx: Ctx, r: Report) -> tuple[str, int, int] | None:
    t = v.get("type")
    if t not in VISUALS:
        r.err(where, f"type must be one of {VISUALS}, got {t!r}")
        return None
    if not is_str(v.get("title")):
        r.err(where, "every visual needs a `title` phrased as the question it answers")
    elif not re.search(r"(\?|나|까|가|지|는가|는지|을까|ㄹ까|무엇|어디|어떻게|얼마|왜|누가|언제)\s*$", v["title"].strip()) and not re.search(r"(무엇|어디|어떻게|얼마|왜|누가|언제|어느|몇)", v["title"]):
        r.warn(where, f"title {v['title'][:30]!r} is not a question; name the question this visual answers")
    if v.get("evidence") is not None and v["evidence"] not in LEVELS:
        r.err(where, f"`evidence` must be one of {LEVELS}")
    if t == "mermaid":
        check_mermaid(v.get("source"), where, r)
    elif t == "before_after":
        for side in ("before", "after"):
            s = v.get(side)
            if not isinstance(s, dict) or not (is_str(s.get("text")) or isinstance(s.get("code"), str)):
                r.err(where, f"`{side}` needs `text` or `code`")
    elif t in ("trace", "table"):
        cols, rows = v.get("columns"), v.get("rows")
        if not cols:
            r.err(where, "`columns` must be a non-empty list of strings")
        elif not rows:
            r.err(where, "`rows` must be a non-empty list")
        else:
            for i, row in enumerate(rows):
                if len(row) != len(cols):
                    r.err(where, f"row {i} must have {len(cols)} cells")
            if len(rows) > 12:
                r.warn(where, f"{len(rows)} rows; keep tables to what the point needs")
            if any(not (0 <= x < len(rows)) for x in v.get("highlight_rows") or []):
                r.err(where, "`highlight_rows` must list 0-based row indexes")
    elif t == "code":
        if not is_str(v.get("code")):
            r.err(where, "`code` is empty")
            return None
        n = len(excerpt_lines(v["code"]))
        if n > 60:
            r.warn(where, f"code excerpt is {n} lines; show only the lines that carry the point")
        return check_excerpt(v, where, ctx, r)
    return None


def check_answer(q: dict, where: str, ctx: Ctx, r: Report) -> None:
    if not is_str(q.get("question")) or not is_str(q.get("answer")):
        r.err(where, "needs `question` and `answer`")
        return
    if q.get("evidence") not in LEVELS:
        r.err(where, f"`evidence` for the answer must be one of {LEVELS}")
    look = q.get("look") or []
    if len(look) > MAX_ANSWER_LOOK:
        r.err(where, f"`look` must have at most {MAX_ANSWER_LOOK} refs")
    if not look and q.get("evidence") in ("run", "read", "claimed"):
        r.err(where, "give `look` (file:line) so the user can check the answer themselves")
    for j, ref in enumerate(look):
        check_ref(ref, f"{where}.look[{j}]", ctx, r, need_what=False)
    pts = q.get("points")
    if pts is not None and not (1 <= len(pts) <= MAX_POINTS and all(is_str(p) for p in pts)):
        r.err(where, f"`points` must list 1-{MAX_POINTS} key ideas of the answer")


def _bigrams(s: str) -> set:
    s = re.sub(r"[^0-9A-Za-z가-힣]", "", s)
    return {s[i:i + 2] for i in range(len(s) - 1)}


HEARSAY_RE = re.compile(r"(?:고|다고|라고) (?:합니다|했습니다|답했습니다|밝혔습니다)|확인됐|확인되었|답했습니다|줄었습니다|늘었습니다")
HYPO_RE = re.compile(r"가정")  # a reported-sounding sentence stays reported even if a later clause says "…라면"


def gives_away(point: str, others: list) -> bool:
    """Near-literal copies only. Paraphrased leaks cannot be detected here; the agent must check."""
    pb = _bigrams(point)
    if len(pb) < 4:
        return False
    return any(isinstance(o, str) and len(pb & _bigrams(o)) / len(pb) >= 0.6 for o in others)


def walk_strings(v, path=""):
    if isinstance(v, str):
        yield path, v
    elif isinstance(v, dict):
        for k, x in v.items():
            yield from walk_strings(x, f"{path}.{k}" if path else k)
    elif isinstance(v, list):
        for i, x in enumerate(v):
            yield from walk_strings(x, f"{path}[{i}]")


# ---- references written inside text -----------------------------------------
# One grammar, ASCII word boundaries, shared with the template (REF_SOURCE is embedded in the page).
# Only tokens recorded here become clickable chips, so the page never links an unchecked location.

# Shared with the page's JavaScript (Unicode mode). Only explicit characters are used, never \s or \w,
# because the two engines disagree on what those include.
WS = r"\u0009-\u000D\u0020\u0085\u00A0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000\uFEFF"
DELIM = WS + r":`'" + '"' + r"()<>,;|*"
# A revision runs to the next delimiter (sentence punctuation may end it). It must be consumed whole:
# if it cannot be, the token does not match at all rather than silently dropping or shortening the @rev.
REV_PART = r"(?:@([^" + DELIM + r"]{0,199}[^" + DELIM + r".!?])(?![^" + DELIM + r".!?]))?(?!@)"
REF_SOURCE = (r"(?:^|(?<=[" + DELIM + r"]))"
              r"((?:[^" + DELIM + r"/]+/)*[^" + DELIM + r"/]+\.[A-Za-z][A-Za-z0-9]{0,9})"
              r":([0-9]{1,7})(?:-([0-9]{1,7}))?(?![0-9]|-[0-9])" + REV_PART + r"(?![A-Za-z0-9_])")
LINE_SOURCE = r"(?:^|(?<=[" + DELIM + r"]))([0-9]{1,7})(?:-([0-9]{1,7}))?행" + REV_PART
CODE_REF_RE = re.compile(REF_SOURCE)
LINE_REF_RE = re.compile(LINE_SOURCE)
# The page scans with this alternation, so build.py does too: tokens never overlap (f.py:100행 is one file reference).
ANY_REF_RE = re.compile("(?:" + REF_SOURCE + ")|(?:" + LINE_SOURCE + ")")
# A reference followed by @ that the grammar did not take (revision too long or malformed).
BROKEN_AT_RE = re.compile(r"(?:^|(?<=[" + DELIM + r"]))(?:[^" + DELIM + r"/]+/)*[^" + DELIM + r"/]+\.[A-Za-z][A-Za-z0-9]{0,9}:[0-9]"
                          r"|(?:^|(?<=[" + DELIM + r"]))[0-9]{1,7}(?:-[0-9]{1,7})?행@")
DOUBLE_TICK_RE = re.compile(r"``.+?``")
SKIP_TEXT = (".source", ".code", ".file", ".rev", ".root", ".command", ".lang", ".term", "kind", "editor", "source_file")
_TREE_CACHE: dict = {}
_SNIPS: dict = {}          # json [rev, file] -> {line number (str): text}
_SNIP_RANGES: dict = {}    # json [rev, file, line, end] -> [first, last] shown
_SNIP_CUT: dict = {}       # json [rev, file] -> {line number (str): full length} for lines shown shortened
_SNIP_BYTES = [0]
SNIP_CONTEXT = 2
SNIP_MAX = 16
SNIP_BUDGET = 400_000      # bytes of source text embedded in one page
SNIP_LINE = 2000           # longer lines are shortened, and the page says so


def jkey(*parts) -> str:
    """Key format shared with the page: JSON of the parts, no spaces."""
    return json.dumps(list(parts), ensure_ascii=False, separators=(",", ":"))


def snip(ctx, file: str, line: int, end: int, rev: str | None) -> None:
    """Keep the referenced lines (plus a little context) so the page can show them on click.
    Each source line is stored once per (rev, file); the total is capped so pages stay small."""
    if ctx.root is None:
        return
    lines = read_lines(ctx.root, file, rev)
    if lines is None or (str(ctx.root), file, rev) in _LOSSY:
        return  # not valid UTF-8: the page offers the path or git command instead of altered text
    a = max(1, line - SNIP_CONTEXT)
    b = min(len(lines), max(end, line) + SNIP_CONTEXT, a + SNIP_MAX - 1)
    store = _SNIPS.setdefault(jkey(rev or "", file), {})
    for n in range(a, b + 1):
        if str(n) not in store:
            text = lines[n - 1][:SNIP_LINE]
            size = len(text.encode("utf-8"))
            if _SNIP_BYTES[0] + size > SNIP_BUDGET:
                return
            if len(lines[n - 1]) > SNIP_LINE:
                _SNIP_CUT.setdefault(jkey(rev or "", file), {})[str(n)] = len(lines[n - 1])
            store[str(n)] = text
            _SNIP_BYTES[0] += size
    _SNIP_RANGES[jkey(rev or "", file, line, end)] = [a, b]


def tree_files(root: Path, rev: str | None) -> list[str]:
    key = (str(root), rev)
    if key not in _TREE_CACHE:
        if rev:
            oid = resolve_rev(root, rev)
            out = _git(root, "ls-tree", "-r", "-z", "--name-only", oid, "--", ".") if oid else None
        else:
            out = _git(root, "ls-files", "-z", "--", ".")
        _TREE_CACHE[key] = [x.decode("utf-8", "replace") for x in (out or b"").split(b"\x00") if x]
    return _TREE_CACHE[key]


def check_inline_refs(d: dict, ctx: Ctx, r: Report) -> dict:
    """Check every file:line (and, for reports, "N행") written in prose or table cells."""
    refs: dict = {}
    source = d.get("source_file") if is_str(d.get("source_file")) else None

    def oid_of(rev: str | None) -> str | None:
        return resolve_rev(ctx.root, rev) if (rev and ctx.root is not None) else None

    def record(token: str, rev: str | None, file: str, line: int, end: int, use_rev: str | None = None) -> None:
        # Keyed by the revision in effect where the text appears; the chip itself uses use_rev (an @rev wins).
        target = use_rev or rev
        refs[f"{rev or ''}|{token}"] = {"file": file, "line": line, "end": end, "rev": target, "oid": oid_of(target)}
        snip(ctx, file, line, end, target)

    def scan(text: str, where: str, rev: str | None) -> None:
        text = DOUBLE_TICK_RE.sub(lambda m: " " * len(m.group(0)), text)  # ``...`` is literal text
        text = text.replace("**", "  ")  # bold markers are formatting, not part of a path
        taken = {m.start() for m in ANY_REF_RE.finditer(text)}
        for m in BROKEN_AT_RE.finditer(text):
            if m.start() not in taken:
                r.warn(where, f"`{m.group(0)}...` looks like a reference but is malformed (line numbers up to 7 digits, a revision after @ of at most 200 characters ending before a space or punctuation), so it stays plain text")
        for m in ANY_REF_RE.finditer(text):
            if m.group(1) is None:
                if source:
                    line_ref(m, where, rev)
                continue
            raw, line, end, at = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2)), m.group(4)
            use_rev = at or rev
            if line < 1 or end < line:
                r.err(where, f"`{m.group(0)}`: line numbers start at 1 and the end cannot come before the start")
                continue
            if at is not None and (not valid_rev(at) or (ctx.root is not None and resolve_rev(ctx.root, at) is None)):
                r.err(where, f"`{m.group(0)}`: `{at}` is not a commit (write the whole revision after @, e.g. @abc1234~1)")
                continue
            if ctx.root is None:
                continue  # nothing to check against: stays plain text (validate warns once)
            if read_lines(ctx.root, raw, use_rev) is not None:
                cands = [raw]
            else:
                cands = [f for f in tree_files(ctx.root, use_rev) if f.endswith("/" + raw)]
            if not cands:
                if "/" in raw:
                    r.err(where, f"`{m.group(0)}`: {raw} is not a file under root{' at ' + use_rev if use_rev else ''}")
                else:
                    r.warn(where, f"`{m.group(0)}` looks like a file reference but no such file exists; it stays plain text. Wrap it in ``double backticks`` if it is not a file")
                continue
            if len(cands) > 1:
                r.err(where, f"`{m.group(0)}` matches {len(cands)} files ({', '.join(cands[:3])}...). Write the path from root")
                continue
            lines = read_lines(ctx.root, cands[0], use_rev)
            if lines is None or end > len(lines):
                r.err(where, f"`{m.group(0)}` is past the end of {cands[0]} ({0 if lines is None else len(lines)} lines){' at ' + use_rev if use_rev else ''}")
                continue
            if (str(ctx.root), cands[0], use_rev) in _LOSSY:
                r.warn(where, f"`{m.group(0)}`: {cands[0]} is not valid UTF-8, so the page cannot show its lines (the chip offers the path or git command)")
            record(m.group(0), rev, cands[0], line, end, use_rev)

    def line_ref(m, where: str, rev: str | None) -> None:
        line, end, at = int(m.group(5)), int(m.group(6) or m.group(5)), m.group(7)
        if at is not None and (not valid_rev(at) or (ctx.root is not None and resolve_rev(ctx.root, at) is None)):
            r.err(where, f"`{m.group(0)}`: `{at}` is not a commit")
            return
        use_rev = at or rev
        if line < 1 or end < line:
            r.err(where, f"`{m.group(0)}`: line numbers start at 1 and the end cannot come before the start")
            return
        if ctx.root is None:
            return
        lines = read_lines(ctx.root, source, use_rev)
        if lines is None or end > len(lines):
            r.err(where, f"`{m.group(0)}` is outside {source} ({0 if lines is None else len(lines)} lines){' at ' + use_rev if use_rev else ''}")
            return
        record(m.group(0), rev, source, line, end, use_rev)

    def visit(v, path: str, rev: str | None) -> None:
        if isinstance(v, str):
            if not path.endswith(SKIP_TEXT):
                scan(v, path, rev)
        elif isinstance(v, dict):
            cols = v.get("columns") if isinstance(v.get("columns"), list) else []
            col_rev = v.get("column_rev") if isinstance(v.get("column_rev"), dict) else {}
            for k_, rv in col_rev.items():
                if not (isinstance(k_, str) and re.fullmatch(r"0|[1-9][0-9]{0,2}", k_)) or not (0 <= int(k_) < len(cols)):
                    r.err(f"{path}.column_rev", f"column {k_!r} does not exist (columns are numbered from 0)")
                elif not valid_rev(rv) or (ctx.root is not None and resolve_rev(ctx.root, rv) is None):
                    r.err(f"{path}.column_rev", f"{rv!r} is not a commit")
            for k, x in v.items():
                if k == "rows" and isinstance(x, list):
                    for i, row in enumerate(x):
                        for j, cell in enumerate(row if isinstance(row, list) else []):
                            visit(cell, f"{path}.rows[{i}][{j}]", col_rev.get(str(j)) or rev)
                elif k != "column_rev":
                    visit(x, f"{path}.{k}" if path else k, rev)
        elif isinstance(v, list):
            for i, x in enumerate(v):
                visit(x, f"{path}[{i}]", rev)

    if not source and d.get("kind") == "report":
        for path_, text_ in walk_strings({k: v for k, v in d.items() if not k.startswith("_")}):
            if not path_.endswith(SKIP_TEXT) and LINE_REF_RE.search(text_):
                if ctx.root is not None:
                    r.err("source_file", "the text uses \"N행\" references but `source_file` is not set, so they cannot be checked. Set `source_file` to the report's path under root")
                else:
                    r.warn("source_file", "the text uses \"N행\" references but `source_file` is not set, so they are not checked or clickable")
                break
    if source and ctx.root is not None and read_lines(ctx.root, source, ctx.rev) is None:
        r.err("source_file", f"{source} is not a readable file under root")
        source = None
    for k, v in d.items():
        if not k.startswith("_") and k not in ("root", "rev", "editor", "kind", "source_file"):
            visit(v, k, ctx.rev)
    return refs


# ---- whole document ---------------------------------------------------------

def validate(d, r: Report) -> None:
    if not isinstance(d, dict):
        r.err("root", "top level must be an object")
        return
    check_types(d, DOC, "", r)
    if r.errors:
        return  # type errors first; the checks below assume correct types

    for path, text in walk_strings(d):
        if "\\`" in text and not path.endswith((".source", ".code")) and ".before." not in path and ".after." not in path:
            r.warn(path, "`\\`` does not escape a backtick here. To show a backtick inside code, wrap it in double backticks: ``a `b` c``")
    ctx = Ctx()
    kind = d.get("kind")
    if kind not in KINDS:
        r.err("kind", f"required: one of {KINDS}")
    for k in ("title", "target", "bottom_line", "your_action"):
        if not is_str(d.get(k)):
            r.err(k, "required")

    if d.get("root") is not None:
        rp = d["root"]
        if not rp.startswith("/") or has_surrogate(rp):
            r.err("root", "must be an absolute path")
        elif ".git" in Path(rp).parts:
            r.err("root", "must be a working tree directory, not inside .git")
        else:
            try:
                ok = Path(rp).is_dir()
            except (OSError, ValueError):
                ok = False
            if not ok:
                r.err("root", f"{rp[:200]} is not a readable directory")
            else:
                ctx.root = Path(rp)
    else:
        r.warn("root", "no `root`; file:line references and code excerpts are not checked, references in text stay plain, and the page says so at the top")
    if d.get("rev") is not None:
        if not valid_rev(d["rev"]):
            r.err("rev", "must be a commit, tag or branch name")
        elif ctx.root is not None and resolve_rev(ctx.root, d["rev"]) is None:
            r.err("rev", f"{d['rev']} is not a commit in {ctx.root}")
        else:
            ctx.rev = d["rev"]
    if d.get("editor") is not None and d["editor"] not in EDITORS:
        r.err("editor", f"must be one of {EDITORS} (or omitted: clicking a ref then copies the path)")
    if d.get("doc") is None and kind == "report":
        r.warn("doc", "reports should state the document's `date` and `status` so proposals are not read as facts")
    if not isinstance(d.get("not_read"), list):
        r.err("not_read", "required: list what grasp did not read or only skimmed ([] if it read everything)")

    if d.get("overview") is None:
        r.err("overview", "deep mode requires an overview visual (mermaid for flow/structure, table for claim lists)")
    else:
        check_visual(d["overview"], "overview", ctx, r)

    gl = d.get("glossary") or []
    if len(gl) > MAX_GLOSSARY:
        r.err("glossary", f"{len(gl)} terms; max {MAX_GLOSSARY}. Introduce the rest inside their chunk")
    for i, g in enumerate(gl):
        if not is_str(g.get("term")) or not is_str(g.get("def")):
            r.err(f"glossary[{i}]", "needs `term` and `def`")
        elif "`" in g["term"]:
            r.warn(f"glossary[{i}]", "write the term without backticks; it is shown as code already")
        elif len(g["term"]) > MAX_TERM:
            r.err(f"glossary[{i}]", f"term longer than {MAX_TERM} characters")

    chunks = d.get("chunks") or []
    if not chunks:
        r.err("chunks", "must be a non-empty list")
        return
    if len(chunks) > MAX_CHUNKS_HARD:
        r.err("chunks", f"{len(chunks)} chunks; max {MAX_CHUNKS_HARD}. Merge into a higher level")
    elif len(chunks) > MAX_CHUNKS_SOFT:
        r.warn("chunks", f"{len(chunks)} chunks; more than {MAX_CHUNKS_SOFT} is allowed only when grouping would bury a red item")

    rank = {g: i for i, g in enumerate(GRADES)}
    prev_rank = -1
    reds = 0
    for i, c in enumerate(chunks):
        w = f"chunks[{i}]"
        if c.get("id") != i + 1:
            r.err(w, f"`id` must be {i + 1} (numbered in display order)")
        g = c.get("grade")
        if g not in GRADES:
            r.err(w, f"`grade` must be one of {GRADES}")
            continue
        reds += g == "red"
        if rank[g] < prev_rank:
            r.warn(w, f"{g} chunk comes after a lower-priority chunk; order by importance (red, yellow, gray)")
        prev_rank = max(prev_rank, rank[g])
        if not is_str(c.get("title")):
            r.err(w, "`title` required")

        if g == "gray":
            if not is_str(c.get("skip_reason")):
                r.err(w, "gray chunks need `skip_reason` stating what you verified")
            elif len(c["skip_reason"]) > 160:
                r.warn(w, "`skip_reason` is long; one sentence is enough on the map")
            if c.get("spot_check") is None:
                r.warn(w, "add `spot_check`: the one file:line where this verdict would be proven wrong, and a `command` if a mechanical check exists")
            else:
                check_ref(c["spot_check"], f"{w}.spot_check", ctx, r)
            if any(c.get(k) for k in ("visuals", "check", "predict", "why", "example", "look", "cautions")):
                r.warn(w, "gray chunks have no page of their own; only title, size, skip_reason and spot_check are shown")
            continue

        for k in ("summary", "why", "example"):
            if not is_str(c.get(k)):
                r.err(w, f"`{k}` required for {g} chunks")
        if g == "yellow":
            if c.get("spot_check") is None:
                r.warn(w, "yellow chunks need `spot_check` too: the riskiest line in this logic, where a bug would show if grasp is wrong")
            else:
                check_ref(c["spot_check"], f"{w}.spot_check", ctx, r)
        vis = c.get("visuals") or []
        if not vis:
            r.warn(w, "no visual; fine only if no picture would answer a question the user has")
        if len(vis) > MAX_VISUALS_PER_CHUNK:
            r.err(w, f"{len(vis)} visuals; max {MAX_VISUALS_PER_CHUNK}. Keep the ones that answer a question the user has")
        shown = []
        for j, v in enumerate(vis):
            span = check_visual(v, f"{w}.visuals[{j}]", ctx, r)
            if span:
                shown.append((*span, (v.get("rev") if isinstance(v, dict) else None) or ctx.rev))

        look = c.get("look") or []
        if len(look) > MAX_LOOK:
            r.err(w, f"{len(look)} look refs; max {MAX_LOOK}")
        for j, ref in enumerate(look):
            span = check_ref(ref, f"{w}.look[{j}]", ctx, r)
            if span:
                f, a, b = span
                ref_rev = (ref.get("rev") if isinstance(ref, dict) else None) or ctx.rev
                for sf, sa, sb, srev in shown:
                    if f == sf and a <= sb and b >= sa and ref_rev == srev:
                        r.warn(f"{w}.look[{j}]", f"points at lines already shown in a code visual ({sf}:{sa}-{sb}); point somewhere new")

        cautions = c.get("cautions") or []
        for j, x in enumerate(cautions):
            if not is_str(x.get("text")):
                r.err(f"{w}.cautions[{j}]", "needs `text`")
            elif x.get("evidence") not in LEVELS:
                r.err(f"{w}.cautions[{j}]", f"`evidence` must be one of {LEVELS}")
        if g == "red" and not cautions:
            r.err(w, "red chunks need at least one caution saying why the user must decide")

        p, k = c.get("predict"), c.get("check")
        if p is not None:
            check_answer(p, f"{w}.predict", ctx, r)
            if g != "red":
                r.warn(w, "`predict` belongs on red chunks only")
            if is_str(p.get("question")) and not EXPECTATION_RE.search(p["question"]):
                r.warn(f"{w}.predict", "ask what the user expects or requires (\"~해야 하나요\", \"기준\"), not what the code does")
            if p.get("points"):
                r.warn(f"{w}.predict", "`points` are for `check` (scoring knowledge), not for expectations")
            if is_str(p.get("user_answer")) and not is_str(p.get("gap")):
                r.warn(f"{w}.predict", "the user answered: write `gap`, one line on how their answer and your analysis differ")
        if k is not None:
            check_answer(k, f"{w}.check", ctx, r)
        if isinstance(k, dict):
            others = [c.get("why"), c.get("example")] + [x.get("text") for x in cautions] + \
                     [v.get("caption") for v in vis if isinstance(v, dict)]
            for j, pt in enumerate(k.get("points") or []):
                if is_str(pt) and gives_away(pt, others):
                    r.warn(f"{w}.check.points[{j}]", "this point is already stated on the same page (why, example, caution or caption), so the question can be answered by copying. Ask about a new case")
        if isinstance(k, dict) and is_str(k.get("question")) and HEARSAY_RE.search(k["question"]) and not HYPO_RE.search(k["question"]):
            r.warn(f"{w}.check.question", "this reads like something that happened or was reported. Start the new case with \"가정:\" so the user does not remember it as fact")
        if g == "red" and k is None:
            r.warn(w, "no `check` question; fine only if a wrong answer would not change the user's decision")

    if reds >= 3 and reds == len(chunks):
        r.warn("chunks", "every chunk is red, so the colours tell the user nothing; red is for what needs their decision. Mark low-impact unrequested changes yellow with `unrequested: true`")

    d["_refs"] = check_inline_refs(d, ctx, r)
    # Commit ids for every revision name used, so copied references cannot drift when a branch moves.
    d["_oids"] = {rv: oid for (rt, rv), oid in _REV_CACHE.items() if oid and ctx.root is not None and rt == str(ctx.root)}
    d["_snips"] = {"lines": dict(_SNIPS), "ranges": dict(_SNIP_RANGES), "cut": dict(_SNIP_CUT)}
    d["_unchecked"] = ctx.root is None
    d["_ref_source"] = [REF_SOURCE, LINE_SOURCE]

    wu = d.get("wrap_up")
    if not isinstance(wu, dict) or not wu.get("remember"):
        r.err("wrap_up.remember", "list the one or two things to keep")


# ---- output -----------------------------------------------------------------

def embed(d: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    if template.count("__GRASP_DATA__") != 1:
        raise SystemExit("template is missing the __GRASP_DATA__ placeholder")
    # ASCII-only JSON with <, >, & escaped: content can never close the <script> element,
    # and lone surrogates are written as escapes instead of failing to encode.
    payload = (json.dumps(d, ensure_ascii=True, allow_nan=False)
               .replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e"))
    # Allow exactly this page script (by hash) instead of any inline script. The hash and the
    # placeholder are handled on the template alone, before any data is inserted.
    m = re.search(r"<script>\n(.*?)</script>", template, re.S)
    if not m or template.count("__SCRIPT_HASH__") != 1:
        raise SystemExit("template is missing the page script or the __SCRIPT_HASH__ placeholder")
    digest = base64.b64encode(hashlib.sha256(("\n" + m.group(1)).encode("utf-8")).digest()).decode("ascii")
    template = template.replace("__SCRIPT_HASH__", f"'sha256-{digest}'")
    return template.replace("__GRASP_DATA__", payload)


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".grasp-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def default_out(d: dict) -> Path:
    slug = re.sub(r"[^a-z0-9]+", "-", str(d.get("title", "")).lower()).strip("-")[:40] or "page"
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path(tempfile.gettempdir()) / "grasp" / f"{slug}-{stamp}.html"


def find_chrome() -> str | None:
    for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"):
        if Path(c).exists():
            return c
    for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"):
        p = shutil.which(c)
        if p:
            return p
    return None


def verify_render(out: Path, r: Report, expected: int | None = None) -> None:
    """Render every diagram in headless Chrome and report failures and unreadable widths."""
    chrome = find_chrome()
    if not chrome:
        r.warn("verify", "no Chrome/Chromium found; diagrams were not test-rendered")
        return
    url = out.resolve().as_uri() + "?grasp-verify"
    with tempfile.TemporaryDirectory() as prof:
        try:
            res = subprocess.run(
                [chrome, "--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={prof}",
                 "--window-size=1280,1000", "--virtual-time-budget=20000", "--dump-dom", url],
                capture_output=True, timeout=90)
        except (subprocess.SubprocessError, OSError) as e:
            r.warn("verify", f"headless Chrome failed to run: {e}")
            return
    # Only the attribute on the <body> tag counts: page text may contain the same string.
    m = re.search(r'<body\b[^>]*?\sdata-grasp-verify="([^"]*)"', res.stdout.decode("utf-8", "replace"))
    if not m:
        r.warn("verify", "page did not finish rendering in headless Chrome; open it and look before sending")
        return
    try:
        results = json.loads(html.unescape(m.group(1)))
        if not isinstance(results, list) or not all(isinstance(x, dict) for x in results):
            raise ValueError
    except (json.JSONDecodeError, ValueError):
        r.warn("verify", "could not read render results")
        return
    if expected is not None and len(results) != expected and not any(x.get("status") in ("crashed", "offline") for x in results):
        r.err("render", f"expected {expected} diagram(s) but the page reported {len(results)}")
        return
    if any(x.get("status") == "offline" for x in results):
        r.warn("verify", "Mermaid library could not be loaded (offline?); diagrams show as source text")
        return
    if any(x.get("status") == "crashed" for x in results):
        r.err("render", "the page script crashed: " + "; ".join(x.get("note", "") for x in results if x.get("status") == "crashed"))
        return
    limit = int(COLUMN_PX / MIN_SCALE)
    for x in results:
        src = str(x.get("source", ""))[:40]
        if x.get("status") != "ok":
            r.err("render", f"diagram starting {src!r} failed: {x.get('note') or x.get('status')}")
        elif x.get("height", 0) > (OVERVIEW_MAX_H if x.get("overview") else 900):
            where_ = "the map's overview pushes the chunk list off the first screen" if x.get("overview") else "it will not fit on one screen"
            r.warn("render", f"diagram starting {src!r} is {x['height']}px tall; {where_}. Shorten node labels or merge steps first (switching to LR often makes it too wide), or split it")
        elif x.get("width", 0) > limit:
            r.warn("render", f"diagram starting {src!r} is {x['width']}px wide (column {COLUMN_PX}px); readers must scroll or zoom. At most {MAX_BRANCHES} nodes in the widest row, try LR/TD, or split it")
    widths = ", ".join(str(x.get("width", 0)) for x in results)
    r.notes.append(f"rendered {len(results)} diagram(s); widths px: {widths or '-'}")


def count_diagrams(d: dict) -> int:
    vis = [d.get("overview")] + [v for c in d.get("chunks") or [] if c.get("grade") != "gray" for v in c.get("visuals") or []]
    return sum(1 for v in vis if isinstance(v, dict) and v.get("type") == "mermaid")


def _finite(s: str) -> float:
    v = float(s)
    if not math.isfinite(v):
        raise ValueError(f"number out of range: {s}")
    return v


def _no_constant(s: str):
    raise ValueError(f"{s} is not allowed")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--open", action="store_true", help="open the page in the default browser")
    ap.add_argument("--no-verify", action="store_true", help="skip the headless-Chrome diagram check")
    a = ap.parse_args()

    try:
        if a.data.stat().st_size > MAX_FILE_BYTES:
            print(f"ERROR data: file is larger than {MAX_FILE_BYTES} bytes")
            return 1
        d = json.loads(a.data.read_text(encoding="utf-8"), parse_float=_finite, parse_constant=_no_constant)
    except (OSError, ValueError, RecursionError) as e:
        print(f"ERROR data: cannot read JSON: {e}")
        return 1

    r = Report()
    try:
        validate(d, r)
    except RecursionError:
        print("ERROR data: the JSON is nested too deeply")
        return 1
    if r.errors:
        print("\n".join(r.errors + r.warnings))
        print(f"\n{len(r.errors)} error(s). Fix them and run again.")
        return 1

    out = a.out or default_out(d)
    try:
        write_atomic(out, embed(d))
    except (OSError, ValueError, RecursionError) as e:
        print(f"ERROR output: {e}")
        return 1

    if not a.no_verify:
        verify_render(out, r, count_diagrams(d))
    for w in r.warnings + r.notes:
        print(w)
    if r.errors:
        print("\n".join(r.errors))
        print(f"\n{len(r.errors)} render error(s). Page written to {out} but fix these before showing it.")
        return 1

    print(f"OK {out}")
    if a.open:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        if shutil.which(opener) and subprocess.run([opener, str(out)], check=False).returncode == 0:
            print("opened in the browser")
        elif shutil.which(opener):
            print(f"WARN  open: `{opener}` failed; the page was NOT opened. Give the user the path")
        else:
            print(f"WARN  open: `{opener}` not found; the page was NOT opened. Give the user the path")
    return 0


if __name__ == "__main__":
    sys.exit(main())
