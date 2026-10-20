"""Validate the skill tree under ``skills/``.

Checks (errors fail the run, warnings only report):

- every skill directory contains a ``SKILL.md`` with YAML frontmatter
  carrying ``name`` and ``description``
- the directory name is a valid skill ID (kebab-case, no length overflow)
- path references (``references/``, ``assets/``, ``scripts/``, ``examples/``,
  ``tools/``) point at files that exist inside the skill directory
- every skill-ID looking token names a skill in this repository, an external
  skill from the allowlist, or an adjective such as ``ETSI-specific``
- ``@skill-name`` mentions (not machine-discoverable) are flagged
- the ``SKILL.md`` body stays within the size budget

Usage:
    python scripts/lint_skills.py [--root skills] [--strict] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_REF_RE = re.compile(r"(?<![\w/-])((?:sdo|etsi|3gpp|itut|officecli)(?:-[a-z0-9]+)+)(?![\w-]|\.\w)")
PATH_REF_RE = re.compile(r"(?<![\w/])((?:references|assets|scripts|examples|tools)/[\w./-]+)")
AT_REF_RE = re.compile(r"(?<![\w`/])@((?:sdo|etsi|3gpp|itut|officecli)(?:-[a-z0-9]+)+)(?![\w-])")
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)

# Skills that live outside this repository (tools repo / other packages).
EXTERNAL_SKILLS = {
    "officecli",
    "etsi-portal-tool",
    "docx-svg",
}
# Adjective forms such as ``ETSI-specific`` are prose, not skill IDs.
GENERIC_SUFFIXES = {
    "agnostic",
    "aware",
    "based",
    "compliant",
    "context",
    "facing",
    "initiated",
    "level",
    "like",
    "neutral",
    "only",
    "originated",
    "related",
    "scope",
    "specific",
    "style",
    "wide",
}
MAX_ID_LENGTH = 64
MAX_BODY_BYTES = 8192
PLACEHOLDER_CHARS = set("<>{}[]*")
TRAILING_PUNCT = ".,;:)'\""


class Report:
    """Collect findings."""

    def __init__(self) -> None:
        self.items: list[dict[str, str | int]] = []

    def add(self, severity: str, path: Path, line: int, message: str) -> None:
        item = {"severity": severity, "path": str(path), "line": line, "message": message}
        if item not in self.items:
            self.items.append(item)

    @property
    def errors(self) -> int:
        return sum(1 for item in self.items if item["severity"] == "error")

    @property
    def warnings(self) -> int:
        return len(self.items) - self.errors


@dataclass(frozen=True)
class Context:
    """Shared lookup state for one repository scan."""

    skill_ids: set[str]
    report: Report

    def unknown(self, ref: str) -> bool:
        """Return True when a skill-ID token does not resolve."""
        if ref in self.skill_ids or ref in EXTERNAL_SKILLS:
            return False
        return ref.rsplit("-", 1)[-1] not in GENERIC_SUFFIXES


def parse_frontmatter(text: str) -> dict[str, str]:
    """Return the scalar top-level fields of the YAML frontmatter."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and key and not key.startswith(" "):
            fields[key.strip()] = value.strip().strip("'\"")
    return fields


def split_frontmatter(text: str) -> str:
    """Return the body that follows the frontmatter."""
    match = FRONTMATTER_RE.match(text)
    return text[match.end() :] if match else text


def check_refs(markdown_file: Path, body: str, first_line: int, skill_dir: Path, ctx: Context) -> None:
    """Validate path references and skill cross-references in a Markdown file."""
    for lineno, line in enumerate(body.splitlines(), start=first_line):
        for raw in PATH_REF_RE.findall(line):
            rel = raw.rstrip(TRAILING_PUNCT)
            if PLACEHOLDER_CHARS & set(rel):
                continue
            if not (skill_dir / rel).exists():
                ctx.report.add("error", markdown_file, lineno, f"path reference {rel!r} does not exist")

        for ref in SKILL_REF_RE.findall(line):
            if ctx.unknown(ref):
                ctx.report.add("error", markdown_file, lineno, f"unknown skill reference {ref!r}")

        for name in AT_REF_RE.findall(line):
            ctx.report.add("warning", markdown_file, lineno, f"@{name} is not machine-discoverable; use the skill tool or an ID in backticks")


def check_skill(skill_dir: Path, ctx: Context) -> None:
    """Validate one skill directory."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        ctx.report.add("error", skill_dir, 0, "missing SKILL.md")
        return

    skill_id = skill_dir.name
    if not ID_RE.match(skill_id) or len(skill_id) > MAX_ID_LENGTH:
        ctx.report.add("error", skill_file, 1, f"directory name {skill_id!r} is not a valid skill ID")

    text = skill_file.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    if not fields:
        ctx.report.add("error", skill_file, 1, "missing YAML frontmatter")
    for key in ("name", "description"):
        if not fields.get(key):
            ctx.report.add("error", skill_file, 1, f"frontmatter has no {key!r}")

    body = split_frontmatter(text)
    size = len(body.encode("utf-8"))
    if size > MAX_BODY_BYTES:
        ctx.report.add("warning", skill_file, 1, f"body is {size} bytes, budget is {MAX_BODY_BYTES} (move detail to references/)")

    check_refs(skill_file, body, 3, skill_dir, ctx)
    for markdown_file in sorted(skill_dir.rglob("*.md")):
        if markdown_file != skill_file:
            check_refs(markdown_file, markdown_file.read_text(encoding="utf-8"), 1, skill_dir, ctx)


def discover(root: Path) -> list[Path]:
    """Return all directories that contain a SKILL.md, sorted by path."""
    return sorted({path.parent for path in root.rglob("SKILL.md")})


def main(argv: list[str] | None = None) -> int:
    """Run the linter."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("skills"))
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    if not args.root.is_dir():
        print(f"error: {args.root} is not a directory", file=sys.stderr)
        return 2

    skills = discover(args.root)
    report = Report()
    ctx = Context(skill_ids={skill.name for skill in skills}, report=report)
    for skill in skills:
        check_skill(skill, ctx)

    if args.json:
        print(json.dumps({"skills": len(skills), "items": report.items}, indent=2))
    else:
        for item in report.items:
            print(f"{str(item['severity']).upper():5} {item['path']}:{item['line']}  {item['message']}")
        print(f"\n{len(skills)} skills, {report.errors} errors, {report.warnings} warnings")

    failed = report.errors > 0 or (args.strict and report.warnings > 0)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
