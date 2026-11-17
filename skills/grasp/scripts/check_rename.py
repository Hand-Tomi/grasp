#!/usr/bin/env python3
"""Check a literal identifier replacement between merge-base and head.

Run inside the reviewed Git repository:
    check_rename.py <base>...<head> <old> <new> -- <paths...>

This checks complete-file textual replacement, preserving whitespace. It does
not parse source or prove semantic equivalence: strings, public APIs, name
collisions, and callers outside the selected paths still need separate review.
No code or modules from the reviewed repository are executed.
"""

import argparse
import re
import subprocess
import sys


class CheckError(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        super().error(f"FAIL: {message}")


def git(*args: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", *args],
            capture_output=True,
            check=True,
        )
    except FileNotFoundError as exc:
        raise CheckError("Git is not available") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.decode("utf-8", "replace").strip()
        raise CheckError(f"Git failed: {message!r}") from exc
    except OSError as exc:
        raise CheckError(f"cannot run Git: {exc}") from exc
    return result.stdout


def commit(revision: str) -> str:
    if (not revision or revision.startswith("-") or ":" in revision
            or any(ch.isspace() or ord(ch) < 32 for ch in revision)):
        raise CheckError(f"invalid revision: {revision!r}")
    value = git("rev-parse", "--verify", "--quiet", "--end-of-options",
                revision + "^{commit}").decode("ascii", "replace").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", value):
        raise CheckError(f"cannot resolve commit: {revision!r}")
    return value


def check(comparison: str, old: str, new: str, paths: list[str]) -> list[str]:
    if comparison.count("...") != 1:
        raise CheckError("comparison must be <base>...<head>")
    if not all(re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", name) for name in (old, new)):
        raise CheckError("names must be ASCII identifiers: [A-Za-z_$][A-Za-z0-9_$]*")
    if old == new:
        raise CheckError("old and new identifiers must differ")
    if not paths:
        raise CheckError("at least one path is required")
    base_revision, head_revision = comparison.split("...")
    base, head = commit(base_revision), commit(head_revision)
    merge_base = git("merge-base", base, head).decode("ascii", "replace").strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", merge_base):
        raise CheckError("cannot determine a single merge-base")
    raw = git("diff", "--raw", "-z", "--no-renames", "--no-ext-diff", "--no-textconv",
              "--abbrev=64", merge_base, head, "--", *paths)
    if not raw:
        raise CheckError("no changed files in the selected paths")
    entries = raw.split(b"\0")
    if entries[-1] != b"" or len(entries) % 2 != 1:
        raise CheckError("unexpected Git diff output")
    identifier = re.compile(r"(?<![\w$])" + re.escape(old) + r"(?![\w$])")
    failures = []
    for index in range(0, len(entries) - 1, 2):
        metadata, path = entries[index], entries[index + 1]
        label = repr(path.decode("utf-8", "surrogateescape"))
        fields = metadata[1:].split() if metadata.startswith(b":") else []
        if len(fields) != 5:
            raise CheckError("unexpected Git diff metadata")
        old_mode, new_mode, old_oid, new_oid, status = fields
        if status != b"M" or old_mode != new_mode or old_mode not in (b"100644", b"100755"):
            failures.append(f"{label}: requires an existing regular file with unchanged mode")
            continue
        if not all(re.fullmatch(rb"[0-9a-f]{40,64}", oid) for oid in (old_oid, new_oid)):
            raise CheckError("unexpected Git blob identifier")
        before = git("cat-file", "blob", old_oid.decode("ascii"))
        after = git("cat-file", "blob", new_oid.decode("ascii"))
        try:
            if b"\0" in before or b"\0" in after:
                raise ValueError("binary content")
            before_text, after_text = before.decode("utf-8"), after.decode("utf-8")
        except (UnicodeDecodeError, ValueError):
            failures.append(f"{label}: requires UTF-8 text without NUL bytes")
            continue
        if identifier.sub(lambda _: new, before_text) != after_text:
            failures.append(f"{label}: differs from the complete literal identifier replacement")
    return failures


def main() -> int:
    parser = Parser(description=__doc__)
    parser.add_argument("comparison", help="<base>...<head> (merge-base to head)")
    parser.add_argument("old", help="old identifier")
    parser.add_argument("new", help="new identifier")
    parser.add_argument("paths", nargs="+", help="Git pathspecs to check")
    args = parser.parse_args()
    try:
        failures = check(args.comparison, args.old, args.new, args.paths)
    except CheckError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("PASS: changed files match the complete literal identifier replacement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
