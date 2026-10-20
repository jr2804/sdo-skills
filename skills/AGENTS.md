# AGENTS.md - skills/

## Purpose

`skills/` is the product of this repository: portable agent skills for standards
work, organised in four layers. Everything here is prose plus payload files.
Nothing here is generated, and nothing here is executable by the package.

```text
skills/
  common/   sdo-*    SDO-agnostic rules (writing, docx, setup)
  etsi/     etsi-*   ETSI-specific knowledge and workflows
  3gpp/     3gpp-*   3GPP-specific knowledge and workflows
  itut/     itut-*   ITU-T-specific knowledge and workflows
```

## Ownership

- **Owns:** skill text, frontmatter, `references/`, `assets/`, `scripts/` inside
  each skill directory.
- **Does not own:** how skills are installed or vendored (`src/sdo_skills/`), which
  layers a consumer enables (consumer project profiles), tool behaviour of
  `officecli` / `etsi-portal-tool`.
- Design rationale and the consolidation backlog live in
  `docs/skills/architecture.md` and `docs/skills/backlog.md` - not here.

## Local Contracts

### Skill anatomy

```text
<layer>/<skill-id>/
  SKILL.md        required - frontmatter + rules, loaded when the skill fires
  references/     optional - background detail, read on demand
  assets/         optional - payload files copied into a deliverable
  scripts/        optional - deterministic helpers, not prose
```

- `SKILL.md` starts with YAML frontmatter carrying `name` (display label) and
  `description`. The body starts at `##`; `#` is reserved for the title.
- `description` is third person, says **what** the skill covers and **when** to
  fire ("Use when the user asks for ..."). It is the only text an agent sees
  before loading the skill, so it must contain the trigger vocabulary.
- The skill ID is the **directory name**: kebab-case, globally unique across
  layers, at most 64 characters.

### Size and disclosure

- `SKILL.md` body stays under **8 KiB**. Move lookups, tables and procedures that
  are not needed on every use into `references/`.
- A reference file may be up to a few hundred lines; split by topic, not by size.
- Payload files (`.docx` templates, `.dotx`, `.json`) go to `assets/`, never
  inline in Markdown.

### Cross-references

- Refer to another skill by its ID in backticks: `` `sdo-docx` ``.
- Do **not** use `@skill-name` mentions - they are not machine-discoverable.
- Path references (`references/...`, `assets/...`, `scripts/...`) are relative to
  the skill directory and must resolve; the linter checks both rules.
- Reference, don't restate: name the generic skill you specialise instead of
  copying its rules.

### Tool invocation (pull on demand)

Skills must work on a machine where only a package manager is installed.
Never write a bare tool invocation; always pull the tool through **mise**:

```bash
mise x github:iOfficeAI/OfficeCLI -- officecli view <doc> text
mise x uv -- uv run scripts/add_bookmarks.py --doc <doc> --spec <spec>
```

| Tool               | mise spec                  | Fallback           |
| ------------------ | -------------------------- | ------------------ |
| `officecli`        | `github:iOfficeAI/OfficeCLI` | `npm i -g @officecli/officecli` |
| `uv` / `uvx`       | `uv`                       | `uv` / `uvx` on PATH |
| `node` / `npx`     | `node`                     | `npx` on PATH      |
| `bun` / `bunx`     | `bun`                      | `bunx` on PATH     |
| `pandoc`           | `pandoc`                   | `pandoc` on PATH   |
| `etsi-portal-tool` | `uv` + `uvx --from <git>` | CLI on PATH        |

- `mise x` is the short form of `mise exec`; the first call downloads the tool.
- Helper scripts declare their dependencies as PEP 723 inline metadata, so
  `mise x uv -- uv run <script>` needs no install step.
- A file that must show the plain package-manager form (a comparison table)
  opts out with `<!-- lint:allow-tooling -->`.
- The linter flags bare invocations; keep the warning count at zero.

### Layer placement

| Layer   | Holds                                           | May depend on                  |
| ------- | ----------------------------------------------- | ------------------------------ |
| `common` | rules valid for ETSI, 3GPP and ITU-T alike      | nothing SDO-specific           |
| `etsi`  | ETSI fora, procedures, portals, deliverable shapes | `common`, other `etsi-*`    |
| `3gpp`  | 3GPP WGs, releases, TDocs, CRs, MCC conventions  | `common`, other `3gpp-*`      |
| `itut`  | ITU-T study groups, recommendations, TSB workflow | `common`, other `itut-*`      |

- Dependencies point **up** (concrete to generic). A `common` skill never names an
  SDO-specific skill.
- A rule lives in the highest layer where it fully applies. If it needs a
  qualifier ("in ETSI, ..."), it belongs in the SDO layer.
- A skill may be consumed without any other layer; `common` alone must be useful.

## Work Guidance

- **Adding a skill:** create `<layer>/<skill-id>/SKILL.md`, keep the body rule-first
  (what to do, in order), put evidence and lookups in `references/`, then run the
  linter.
- **Merging skills:** merge into the canonical ID from
  `docs/skills/backlog.md`, move unaffected detail to `references/`, add a one-line
  pointer under "Moved" only if external documents link to the old ID.
- **Renaming an ID is a breaking change:** update consumer project profiles
  (`skills.sources`, permissions, prompts) in the same change.
- **Never trim a skill for one SDO by editing it.** Layer selection happens in the
  consumer config; the same directory serves every consumer.

## Verification

```bash
mise run lint:skills            # structure, frontmatter, refs, size budget
mise run lint:skills -- --strict  # warnings fail too (use before merging)
```

Errors block CI: missing `SKILL.md`, missing `name`/`description`, invalid ID,
broken path reference, unknown skill ID. Warnings are advisory: oversized body,
`@skill` mention, bare tool invocation.

## Child DOX Index

No child `AGENTS.md` files: `common/`, `etsi/`, `3gpp/` and `itut/` are layer
buckets, not boundaries with their own rules. Layer rules are the table above.
