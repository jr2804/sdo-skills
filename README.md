# SDO Skills

> Portable agent skills for writing standards contributions and deliverables (ETSI, 3GPP, ITU-T)

<!-- markdownlint-disable MD033 -->
<p align="center">
  <a href="#"><img alt="Python 3.13+" src="https://img.shields.io/badge/python-3.13%2B-3776ab?logo=python"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
</p>
<!-- markdownlint-enable MD033 -->

---

## What this is

Agent skills that carry the domain knowledge for standards work: which committee
decides what, how a contribution is numbered and submitted, what a deliverable
clause must look like, and how a Word file is edited without destroying its
numbering. The skills follow the Agent Skills convention (`SKILL.md` plus
`references/`, `assets/`, `scripts/`), so they work in OpenCode and in any other
host that reads that layout.

This repository is the **source of truth for skill text**. Tooling that talks to
portals (`etsi-portal-tool`), generates documents (`officecli`) or wires skills
into a project (`opencode-sdo-writer`) lives elsewhere and is consumed as a
dependency.

## Layers

| Layer    | Directory | Holds                                                                     |
| -------- | --------- | ------------------------------------------------------------------------- |
| Common   | `skills/common/` | rules valid for every SDO: writing conventions, DOCX editing, project setup |
| ETSI     | `skills/etsi/`   | ETSI governance, drafting rules, deliverable shapes, spec retrieval |
| 3GPP     | `skills/3gpp/`   | working groups, releases, TDocs, change requests, portal authentication |
| ITU-T    | `skills/itut/`   | study groups, recommendations, contributions, patent policy |

Dependencies point up: an `etsi-*` skill may name `sdo-*`, never the other way
round. A consumer selects layers by listing directories, so an ETSI-only project
never loads 3GPP or ITU-T skills.

## Skills

| Layer    | Skills |
| -------- | ------ |
| Common   | `sdo-writing`, `sdo-docx`, `sdo-drafting`, `sdo-ipr`, `sdo-project-setup` |
| ETSI     | `etsi-governance`, `etsi-directives`, `etsi-procedures`, `etsi-tools` |
| 3GPP     | `3gpp-basics`, `3gpp-meetings`, `3gpp-working-groups`, `3gpp-releases`, `3gpp-specifications`, `3gpp-tdocs`, `3gpp-change-request`, `3gpp-portal-authentication` |
| ITU-T    | `itut-reference`, `itut-contributions` |

Nineteen skills today, eleven after the last consolidation pass. The target
shape and the order of work are in
[the consolidation backlog](docs/skills/backlog.md).

## Tools pull on demand

The skills never assume a tool is installed. Every external tool is fetched
through [mise](https://mise.jdx.dev) on first use, so a fresh checkout needs
nothing but mise (or a package manager) on PATH:

```bash
mise x github:iOfficeAI/OfficeCLI -- officecli view report.docx text
mise x uv -- uv run scripts/add_bookmarks.py --doc report.docx --spec spec.json
```

Helper scripts carry their dependencies as PEP 723 inline metadata, so
`mise x uv -- uv run <script>` installs what it needs. The linter enforces
the convention.

## Using the skills

Point a consumer project at the layers it needs:

```jsonc
{
  "skills": {
    "sources": [
      "path/to/sdo-skills/skills/common",
      "path/to/sdo-skills/skills/etsi"
    ]
  }
}
```

Paths are listed, not submoduled, so the same checkout serves an ETSI, a 3GPP and
an ITU-T project without duplication. A packaged installer, profiles and the
writer agent belong to the `opencode-sdo-writer` repository.

## Repository layout

```text
sdo-skills/
  skills/                 # the product: layered skill tree
    common/  etsi/  3gpp/  itut/
  src/sdo_skills/         # package: install, validate, vendor skills
  scripts/                # lint_skills.py and friends
  docs/                   # Zensical site, design notes, backlog
  tests/                  # test suite
  .config/mise/           # task definitions
```

## Development

```bash
mise dev              # install dependencies (uv sync)
mise lint:skills      # validate skill structure, frontmatter, references, budget
mise test             # pytest with the 100% coverage gate
mise lint             # ruff
mise format           # ruff format, import order, pyreorder
mise format-md        # rumdl
mise all              # everything above
mise docs             # build the documentation site
```

`mise lint:skills` is the gate for content changes: missing `SKILL.md`, missing
`name`/`description`, invalid directory names, broken `references/` paths,
unknown skill IDs and bare tool invocations fail; oversized bodies and
`@skill` mentions warn.

## Contributing

Read `skills/AGENTS.md` before editing the tree - it holds the skill anatomy, the
layer contract and the size budget. Changes to the package follow the usual
`mise all` cycle; see [CONTRIBUTING](docs/contributing.md).

## License

MIT - see [LICENSE](LICENSE) for details.

---

Generated from [copier-uv-plus](https://codeberg.org/jr2804/copier-uv-plus).
