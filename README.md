# SDO Skills

> Portable agent skills for writing standards contributions and deliverables (ETSI, 3GPP, ITU-T)

<!-- markdownlint-disable MD033 -->
<p align="center">
  <a href="#"><img alt="Python 3.13+" src="https://img.shields.io/badge/python-3.13%2B-3776ab?logo=python"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
</p>
<!-- markdownlint-enable MD033 -->

---

## Quick Start

```bash
# Install dependencies
mise dev
```

## Usage

### Running Tests

```bash
mise test
# or
uv run pytest
```

### Code Quality

```bash
mise lint       # ruff + ty + codespell
mise format     # ruff format + isort
mise all        # test + lint + format in one pass
```

## Development

### Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

### Documentation

```bash
mise docs-serve          # live preview at http://localhost:8000
mise docs-build          # build static site to site/
```

## CI/CD

GitHub Actions runs on every push and PR:

| Workflow | Triggers | Jobs |
|----------|----------|------|
| **CI** (`ci.yml`) | push, PR to main | test matrix (3.13, 3.14) + lint + type-check |
| **Release** (`release.yml`) | tag `v*` | build + publish to PyPI |

## Project Structure

```text
sdo-skills/
├── .config/mise/               # mise task definitions
├── .github/workflows/          # CI + release workflows
├── docs/                       # MkDocs documentation
├── src/sdo_skills/     # Source package
│   ├── __init__.py
│   ├── __about__.py
├── tests/                      # Test suite
├── .copier-answers.yml         # Template version tracking
├── pyproject.toml              # uv + hatch + pytest config
├── ruff.toml                   # Linter + formatter config
├── ty.toml                     # Type checker config
└── README.md
```

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Package manager | [uv](https://docs.astral.sh/uv/) | Fast installs, deterministic lockfile |
| Task runner | [mise](https://mise.jdx.dev/) | DAG-based tasks, tool version management |
| Linter + formatter | [ruff](https://docs.astral.sh/ruff/) | Single-binary code quality |
| Type checker | [ty](https://github.com/google/ty) | Strict type checking |
| Testing | [pytest](https://pytest.org/) | Test framework with 100% coverage gate |
| Spell check | [codespell](https://github.com/codespell-project/codespell) | Code and doc spell checking |
| Documentation | [Zensical](https://github.com/zensical/zensical) | MkDocs Material with executable examples |
| Versioning | [uv-dynamic-versioning](https://github.com/ninoseki/uv-dynamic-versioning) | Git tag-based versioning |
| Hooks | [pre-commit](https://pre-commit.com/) | Automated quality gate |
| CI/CD | GitHub Actions | Test matrix + PyPI release |

## License

MIT — see [LICENSE](LICENSE) for details.

---

Generated from [copier-uv-plus](https://codeberg.org/jr2804/copier-uv-plus).
