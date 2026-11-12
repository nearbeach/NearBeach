#!/usr/bin/env python3
"""Fail if agent-facing docs reference repo paths that no longer exist.

Checks AGENTS.md, CLAUDE.md, Architecture.md, nested CLAUDE.md files and
.claude/skills/*/SKILL.md. Any backtick-quoted token that looks like a repo path
(contains a "/" and a known top-level directory, or ends in a known extension)
must resolve to a file or directory. Run from anywhere:

    python3 scripts/check_agent_docs.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_GLOBS = [
    "AGENTS.md",
    "CLAUDE.md",
    "Architecture.md",
    "**/CLAUDE.md",
    ".claude/skills/*/SKILL.md",
    "docs/008-for-agents/*.rst",
    "docs/llms.txt",
]
TOP_LEVEL = {
    "NearBeach", "src", "local", "e2e", "docs", "scripts", "swagger", "tests",
    "vite.config.ts", "schema.yml", ".claude", ".github",
}
# Tokens that are intentionally not real paths (placeholders, examples, generated files)
IGNORE_SUBSTRINGS = ("<", ">", "*", "...", "XXX", "Name.", "__pycache__", "{", "}")
IGNORE_EXACT = {"NearBeach/static/NearBeach/", "db.sqlite3"}
TOKEN_RE = re.compile(r"`([^`\s]+)`")


def candidate(token: str) -> str | None:
    token = token.strip().rstrip(",.;:)").lstrip("(")
    token = token.removeprefix("@").lstrip("/")
    token = re.sub(r":\d+$", "", token)  # file.py:12
    if token in IGNORE_EXACT or any(s in token for s in IGNORE_SUBSTRINGS):
        return None
    if "/" not in token:
        return None
    if token.split("/")[0] not in TOP_LEVEL:
        return None
    return token


def resolve(token: str, doc: Path) -> bool:
    for base in (ROOT, doc.parent):
        if (base / token).exists():
            return True
    # NearBeach/ and src/ docs often use paths relative to the app dir
    return any((ROOT / top / token).exists() for top in ("NearBeach", "src"))


def main() -> int:
    docs: set[Path] = set()
    for pattern in DOC_GLOBS:
        docs.update(p for p in ROOT.glob(pattern) if p.is_file() and "node_modules" not in p.parts and "venv" not in p.parts)

    missing: list[str] = []
    for doc in sorted(docs):
        for lineno, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            for token in TOKEN_RE.findall(line):
                path = candidate(token)
                if path and not resolve(path, doc):
                    missing.append(f"{doc.relative_to(ROOT)}:{lineno}: {path}")

    if missing:
        print("Agent docs reference paths that do not exist:\n")
        print("\n".join(missing))
        return 1
    print(f"OK - {len(docs)} agent doc(s) checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
