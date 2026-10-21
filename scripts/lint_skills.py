"""Validate the skill tree under ``skills/``.

Checks (errors fail the run, warnings only report):

- every skill directory contains a ``SKILL.md`` with YAML frontmatter
  carrying ``name`` and ``description``
- the directory name is a valid skill ID (kebab-case, no length overflow)
- path references (``references/``, ``assets/``, ``scripts/``, ``examples/``,
  ``tools/``) point at files that exist inside the skill directory, or in
  exactly one other skill of the repository (cross-skill reference)
- every skill-ID looking token names a skill in this repository, an external
  skill from the allowlist, or an adjective such as ``ETSI-specific``
- ``@skill-name`` mentions (not machine-discoverable) are flagged
- the ``SKILL.md`` body stays within the size budget
- external tools are invoked pull-on-demand (``mise x <spec> -- <tool>``)
  instead of assuming a local installation
- the routing evals name skills that exist, and every skill of the tree is
  reached by at least one eval case

Usage:
    python scripts/lint_skills.py [--root skills] [--evals evals/routing.json] [--strict] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field as dataclasses_field
from pathlib import Path

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_REF_RE = re.compile(r"(?<![\w/-])((?:sdo|etsi|3gpp|itut|officecli)(?:-[a-z0-9]+)+)(?![\w-]|\.\w)")
PATH_REF_RE = re.compile(r"(?<![\w/])((?:references|assets|scripts|examples|tools)/[\w./-]+)")
AT_REF_RE = re.compile(r"(?<![\w`/])@((?:sdo|etsi|3gpp|itut|officecli)(?:-[a-z0-9]+)+)(?![\w-])")
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
TOOL_CMD_RE = re.compile(
    r"^(?P<tool>etsi-portal-tool|officecli|uvx|uv|npx|bunx|pandoc|python3|python|py|node)"
    r"\s+(?P<args>\S.*)$"
)
#: An argument that makes an inline code span look like a real invocation
#: (placeholder, file name, path or quoted argument) rather than a mention.
ARG_HINT_RE = re.compile(r"<[^>]+>|\b[\w./\\-]+\.(?:docx|doc|json|md|py|xml|txt|csv|pptx|xlsx|pdf|svg)\b|[\"']")
SHELL_BLOCK_LANGS = {"", "bash", "sh", "shell", "console", "zsh", "fish"}
ALLOW_TOOLING_MARKER = "lint:allow-tooling"

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


@dataclass(frozen=True)
class Context:
    """Shared lookup state for one repository scan."""

    skill_ids: set[str]
    report: Report
    file_index: dict[str, list[str]] = dataclasses_field(default_factory=dict)

    def unknown(self, ref: str) -> bool:
        """Return True when a skill-ID token does not resolve."""
        if ref in self.skill_ids or ref in EXTERNAL_SKILLS:
            return False
        return ref.rsplit("-", 1)[-1] not in GENERIC_SUFFIXES

    def resolves_elsewhere(self, rel: str) -> list[str]:
        """Return the skills that provide ``rel`` when it is not local."""
        return self.file_index.get(rel, [])


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


def main(argv: list[str] | None = None) -> int:
    """Run the linter."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("skills"))
    parser.add_argument(
        "--evals",
        type=Path,
        default=Path("evals/routing.json"),
        help="routing eval file (empty string disables the check)",
    )
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    if not args.root.is_dir():
        print(f"error: {args.root} is not a directory", file=sys.stderr)
        return 2

    skills = discover(args.root)
    report = Report()
    ctx = Context(
        skill_ids={skill.name for skill in skills},
        report=report,
        file_index=build_file_index(skills),
    )
    for skill in skills:
        check_skill(skill, ctx)

    eval_path = args.evals
    if str(eval_path) and eval_path.is_file():
        check_evals(eval_path, ctx)
    elif str(eval_path):
        report.add("warning", eval_path, 0, "no routing eval file")

    if args.json:
        print(json.dumps({"skills": len(skills), "items": report.items}, indent=2))
    else:
        for item in report.items:
            print(f"{str(item['severity']).upper():5} {item['path']}:{item['line']}  {item['message']}")
        print(f"\n{len(skills)} skills, {report.errors} errors, {report.warnings} warnings")

    failed = report.errors > 0 or (args.strict and report.warnings > 0)
    return 1 if failed else 0


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

    check_refs(skill_file, body, body_start_line(text), skill_dir, ctx)
    check_tooling(skill_file, body, body_start_line(text), ctx)
    for markdown_file in sorted(skill_dir.rglob("*.md")):
        if markdown_file != skill_file:
            other = markdown_file.read_text(encoding="utf-8")
            check_refs(markdown_file, other, 1, skill_dir, ctx)
            check_tooling(markdown_file, other, 1, ctx)


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


def body_start_line(text: str) -> int:
    """Return the 1-based line number where the frontmatter body starts."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return 1
    return match.group(0).count("\n") + 1


def check_tooling(markdown_file: Path, body: str, first_line: int, ctx: Context) -> None:
    """Require pull-on-demand (mise) invocations for external tools."""
    for lineno, tool in iter_tool_invocations(body, first_line):
        ctx.report.add(
            "warning",
            markdown_file,
            lineno,
            f"bare {tool!r} invocation: use 'mise x <spec> -- {tool} ...' so the tool is pulled on demand",
        )


def iter_tool_invocations(body: str, first_line: int) -> list[tuple[int, str]]:
    """Return ``(lineno, tool)`` for every bare external tool invocation.

    Only command positions count: the first word of a line inside a shell
    code block, or an inline code span that carries a concrete target
    (placeholder, file name, path or quoted argument). Prose mentions such
    as ``officecli batch`` are ignored. A file or line may opt out with an
    ``<!-- lint:allow-tooling -->`` marker.
    """
    found: list[tuple[int, str]] = []
    if ALLOW_TOOLING_MARKER in body:
        return found
    in_block = False
    block_lang = ""
    for offset, line in enumerate(body.splitlines()):
        lineno = first_line + offset
        stripped = line.strip()
        if ALLOW_TOOLING_MARKER in line:
            continue
        if stripped.startswith("```"):
            in_block = not in_block
            block_lang = ""
            continue
        candidates: list[str] = []
        if in_block and block_lang in SHELL_BLOCK_LANGS and stripped and not stripped.startswith("#"):
            candidates.append(stripped)
        candidates.extend(INLINE_CODE_RE.findall(line))
        for candidate in candidates:
            match = TOOL_CMD_RE.match(candidate.strip())
            if not match:
                continue
            if not ARG_HINT_RE.search(match.group("args")):
                continue
            found.append((lineno, match.group("tool")))
    return found


def check_refs(markdown_file: Path, body: str, first_line: int, skill_dir: Path, ctx: Context) -> None:
    """Validate path references and skill cross-references in a Markdown file."""
    for lineno, line in enumerate(body.splitlines(), start=first_line):
        for raw in PATH_REF_RE.findall(line):
            rel = raw.rstrip(TRAILING_PUNCT)
            if PLACEHOLDER_CHARS & set(rel):
                continue
            if (skill_dir / rel).exists():
                continue
            owners = ctx.resolves_elsewhere(rel)
            if len(owners) == 1:
                continue
            if len(owners) > 1:
                ctx.report.add(
                    "error",
                    markdown_file,
                    lineno,
                    f"path reference {rel!r} is ambiguous: provided by {', '.join(sorted(owners))}",
                )
            else:
                ctx.report.add("error", markdown_file, lineno, f"path reference {rel!r} does not exist")

        for ref in SKILL_REF_RE.findall(line):
            if ctx.unknown(ref):
                ctx.report.add("error", markdown_file, lineno, f"unknown skill reference {ref!r}")

        for name in AT_REF_RE.findall(line):
            ctx.report.add("warning", markdown_file, lineno, f"@{name} is not machine-discoverable; use the skill tool or an ID in backticks")


def check_evals(eval_path: Path, ctx: Context) -> None:
    """Validate the routing evals against the skill tree.

    Every skill named in an eval must exist, and every skill of the tree
    must be the expected answer for at least one case. An unreachable
    skill never gets loaded, so a silent gap here is a routing bug.
    """
    try:
        data = json.loads(eval_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        ctx.report.add("error", eval_path, 0, f"cannot read routing evals: {exc}")
        return

    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        ctx.report.add("error", eval_path, 0, "routing evals have no cases")
        return

    covered: set[str] = set()
    for index, case in enumerate(evals, start=1):
        if not isinstance(case, dict):
            ctx.report.add("error", eval_path, index, "eval case is not an object")
            continue
        expected = case.get("expected_skills")
        if not isinstance(expected, list) or not expected:
            ctx.report.add("error", eval_path, index, "eval case has no expected_skills")
            continue
        if not case.get("prompt"):
            ctx.report.add("error", eval_path, index, "eval case has no prompt")
        for skill_id in expected:
            if skill_id not in ctx.skill_ids:
                ctx.report.add("error", eval_path, index, f"eval names unknown skill {skill_id!r}")
            else:
                covered.add(skill_id)

    for skill_id in sorted(ctx.skill_ids - covered):
        ctx.report.add("warning", eval_path, 0, f"no routing eval expects {skill_id!r}")


def discover(root: Path) -> list[Path]:
    """Return all directories that contain a SKILL.md, sorted by path."""
    return sorted({path.parent for path in root.rglob("SKILL.md")})


def build_file_index(skills: list[Path]) -> dict[str, list[str]]:
    """Map a path relative to a skill directory to the skills that provide it."""
    index: dict[str, list[str]] = {}
    for skill in skills:
        for path in skill.rglob("*"):
            rel = path.relative_to(skill).as_posix()
            index.setdefault(rel, []).append(skill.name)
            index.setdefault(f"{rel}/", []).append(skill.name)
    return index


if __name__ == "__main__":
    raise SystemExit(main())
