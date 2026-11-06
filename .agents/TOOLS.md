# AGENTS.md — TOOLS

State file: inventory of tools used in development — CLIs, MCP servers,
skills, runtimes, and project scripts. Demand-loaded like all state files;
keep it current (see `.agents/MAINTENANCE.md`).

## Rules

- Use an existing tool before adding a new one. No new tools, MCP servers,
  skills, or dependencies without explicit instruction (`.agents/POLICIES.md`).
- Each tool appears exactly once, in its primary table.
- Tables describe current usage — delete rows when tools leave; this is not a
  historical log.

## Subdirectory

If this file grows past its size budget, split detail into
`.agents/tools/<name>.md` — every file there MUST be listed above.

## CLI tools & runtimes

| Tool        | When                                         | Purpose                                                        |
| ----------- | -------------------------------------------- | -------------------------------------------------------------- |
| `mise`      | Every build, test, lint, docs run            | Task runner; owns all pinned tool versions (`.config/mise/`)     |
| `uv`        | Python env, scripts, `uvx` one-offs          | Dependency sync, PEP 723 script runner, package builds          |
| `ruff`      | Python lint/format                           | Lint (`mise lint`), format and import sort (`mise format`)      |
| `ty`        | Type checking                                | `mise typecheck` over `src/`, `tests/`, `scripts/`              |
| `pyreorder` | After moving code within a module            | Structural order gate: imports, constants, classes, functions   |
| `codespell` | Before pushing                               | `mise spell`; config in `pyproject.toml` `[tool.codespell]`     |
| `rumdl`     | After touching Markdown                      | `mise format-md` formats/checks with `.config/rumdl.toml`       |
| `pytest`    | Every code change                            | `mise test` — 100 % coverage gate                               |
| `zensical`  | Verifying `docs/` renders                    | `mise docs` builds the site                                     |
| `copier`    | Pulling upstream template changes            | `copier update`; answers in `.copier-answers.yml`               |
| `pre-commit`| Commit hygiene (not on PATH here)            | `pre-commit run --all-files`; hooks in `.pre-commit-config.yaml` |
| `ripgrep`+`tree-cli` | Orientation                          | `rg --files \| tree-cli --fromfile` for a live tree view        |
| `node`/`bun`| JS tooling pulled on demand                 | `bun x …` for MCP servers and skill installers                  |

## External tools the skills invoke (pull on demand)

Never assume these are installed; the skills pull them through `mise x`. The
spec table and invocation rule are owned by `skills/AGENTS.md` → **Tool
invocation** — this table only records why they matter here.

| Tool                 | Purpose                                        |
| -------------------- | ---------------------------------------------- |
| `officecli`          | Docx/xlsx/pptx inspection and generation       |
| `etsi-portal-tool`   | ETSI portal access and TDoc operations         |
| `opencode-sdo-writer`| Wires skills into a consumer project           |

## MCP servers

None enabled. Template answer `include_mcp_tasks: False`; no MCP config is
committed. Revisit only if a tool becomes mandatory for the workflow.

## Skills

| Skill | When | Purpose |
| ----- | ---- | ------- |
| `common/`, `etsi/`, `3gpp/`, `itut/` layers | Editing or consuming skill text | The product of this repo — see `skills/AGENTS.md` |
| `copier-uv-plus` (host) | Scaffolding or updating the Python project | Runs the real `copier` CLI against the template |
| `officecli` (host) | Producing/verifying `.docx`, `.xlsx`, `.pptx` | Wraps the `officecli` CLI with format rules |

## Project scripts & tasks

| Command | Purpose |
| ------- | ------- |
| `mise dev` | `uv sync -U --dev --all-extras --all-groups` |
| `mise test` / `mise lint` / `mise format` / `mise sort` / `mise spell` | Single-purpose quality steps |
| `mise lint:skills` | `scripts/lint_skills.py` — skill structure, refs, size budget |
| `mise format-md` | rumdl over `src/`, `docs/`, `tests/`, repo root (incl. `.agents/`) |
| `mise all` | Full gate: test, lint, lint:skills, sort, spell, format, format-md, docs |
| `scripts/gen_credits.py` | Renders the dependency credit table, inlined by `docs/credits.md` |
| `scripts/verify_split.py` | Checks a split kept every substantial line of the original |
