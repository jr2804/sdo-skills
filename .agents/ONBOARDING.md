# AGENTS.md — ONBOARDING

Read this when starting a new session. After first read, only revisit when
project structure or tooling changes significantly.

## Project

Portable agent skills for writing standards contributions and deliverables
(ETSI, 3GPP, ITU-T). Full docs at `README.md` or `docs/`.

## Quick start

```bash
mise dev        # install dependencies (uv sync --dev)
mise test       # pytest with 100 % coverage gate
mise lint       # ruff over src/, tests/, scripts/
mise typecheck  # ty check over src/, tests/, scripts/
mise format     # pyreorder + ruff format + import sort
mise all        # full gate (see .agents/POLICIES.md → Verification)
```

## Entry points (read these first)

| File / Section | Why |
| -------------- | --- |
| `AGENTS.md` | Root rail — rules + `.agents/` index |
| `.agents/POLICIES.md` | Boundaries, priorities, verification |
| `.agents/FILES.md` | Source-of-truth locations for this package |
| `pyproject.toml` | Dependencies, pytest config, build backend |
| `.copier-answers.yml` | Template answers (regenerated on `copier update`) |

## Layout

- **`src/sdo_skills/`** — primary package source (src layout)
- **`tests/`** — pytest suite (100% coverage gate)
- **`docs/`** — Zensical / MkDocs Material documentation
- **`.config/mise/`** — task runner config (`config.toml` + `conf.d/` fragments)

## Where to dig deeper

- `docs/` — user-facing documentation
- `.agents/TOOLS.md` — tools, MCP servers, skills, CLIs in use
- `.agents/HISTORY.md` — past decisions and rationale
- Source-tree AGENTS.md files — local contracts for each area

## Available tools

Development tools, MCP servers, skills, and CLIs are inventoried in the
state file `.agents/TOOLS.md` — read it before assuming a tool, update it
when tooling changes. If tooling grows large, detail moves to
`.agents/tools/<name>.md` (each listed in TOOLS.md).
