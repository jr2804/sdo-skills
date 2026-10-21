# AGENTS.md — FILES

Single source of truth for paths, config keys, and naming conventions.
Kept compact — agents hallucinate less when they know where definitions live.

## Pattern

- One file owns each class of definition (paths, config defaults, enums).
- Import from that file. Never hard-code values in other modules.
- Variables that address files get `_file` suffix; directories get `_dir`.

## Project-specific sources of truth

| What                   | Where                                                           | Key names                                       |
| ---------------------- | --------------------------------------------------------------- | ----------------------------------------------- |
| Skill tree             | `skills/{common,etsi,3gpp,itut}/<skill-id>/`                    | `SKILL.md`, `references/`, `assets/`, `scripts/` |
| Skill rules            | `skills/AGENTS.md`                                              | anatomy, layer contract, 8 KiB budget            |
| Skill validator        | `scripts/lint_skills.py`                                        | `mise run lint:skills`                          |
| Skill backlog          | `docs/skills/backlog.md`                                        | merge map, target IDs                           |
| Package source root    | `src/sdo_skills/`  | `__init__.py`, `__about__.py` (version)         |
| Test suite             | `tests/`                                                        | `test_*.py`, `conftest.py`                      |
| Project metadata       | `pyproject.toml`                                                | `[project]`, `[tool.pytest.ini_options]`        |
| Linter/formatter       | `ruff.toml`                                                     | Ruff rule selection, line length                |
| Structural sorter      | `.config/pyreorder.toml`                                         | `sections`, `strategies`, `hoist_inline_imports` |
| Type checker           | `ty.toml`                                                       | ty strictness                                   |
| Markdown linter        | `.config/rumdl.toml`                                            | `line-length`, `flavor`, disabled rules         |
| mise tasks             | `.config/mise/config.toml` + `.config/mise/conf.d/*.toml`       | `[tasks.dev]`, `[tasks.test]`, ...              |
| Copier answers         | `.copier-answers.yml`                                           | Template version + answers (regenerated)        |
| Pre-commit config      | `.pre-commit-config.yaml`                                       | Hook list                                       |

## Naming conventions

- **Repository name** (`project_slug`): kebab-case (`my-project`)
- **Python package** (`package_slug`): snake_case (`my_project`)
- **Layout**: `src/sdo_skills/`
- **Test files**: `test_<module>.py`
- **Template files** (in source template): `filename.ext.jinja` — the `.jinja`
  suffix is stripped on generation
