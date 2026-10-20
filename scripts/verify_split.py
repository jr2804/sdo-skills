"""Verify that a split did not lose content.

Usage:
    uv run scripts/verify_split.py ORIGINAL.md NEW1.md NEW2.md ...

Prints the share of substantial original lines that survive in the new files.
A coverage below 100 % means content was dropped (headings and short lines
are ignored; they are checked separately by the caller).
"""

from __future__ import annotations

import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2

    original = Path(argv[1])
    targets = [Path(p) for p in argv[2:]]
    haystack: set[str] = set()
    for target in targets:
        if not target.exists():
            print(f"missing target: {target}")
            return 2
        haystack.update(substantial_lines(target))

    source = substantial_lines(original)
    missing = [line for line in source if line not in haystack]
    pct = 100 * (len(source) - len(missing)) / max(len(source), 1)
    print(f"{original.name}: {len(source) - len(missing)}/{len(source)} lines preserved ({pct:.1f} %)")
    for line in missing:
        print(f"  MISSING: {line[:160]}")
    return 0 if not missing else 1


def substantial_lines(path: Path) -> list[str]:
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if len(line) < 25 or line.startswith("#"):
            continue
        lines.append(line)
    return lines


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
