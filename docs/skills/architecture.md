# Skill architecture

This page records *why* the tree is shaped the way it is. The operational rules
for editing it live in `skills/AGENTS.md`; the open work lives in
[the consolidation backlog](backlog.md).

## What this repository is

A **content** repository: portable agent skills plus thin tooling that installs,
validates and vendors them. No protocol logic, no portal client, no document
engine - those are separate repositories with their own release cadence.

```text
sdo-skills                     this repo: skill text (source of truth)
   |
   +-- opencode-sdo-writer     plugin + config profiles (ETSI / 3GPP / ITU-T writers)
   |      |
   |      +-- <writer project> consumer repo: config, paper trail, deliverables
   |
   +-- etsi-portal-tool        MCP/CLI tool: portal access, TDoc write ops
   +-- officecli               MCP/CLI tool: docx/xlsx/pptx generation and checks
```

Tools are **dependencies**, not vendored copies: consumers enable a tool through
their MCP configuration and set a version constraint. Skills are **vendored**:
consumers pull skill directories in so the agent reads them from its own tree.

## Why path-listing instead of submodules or skill packs

The OpenCode config accepts a list of skill source directories. A consumer
profile therefore selects layers by listing directories:

```jsonc
"skills": { "sources": ["../sdo-skills/skills/common", "../sdo-skills/skills/etsi"] }
```

Consequences that shaped the design:

- **No submodules.** Vendoring the ETSI profile should not drag 3GPP and ITU-T
  skills into the tree. A path list plus a sync step (symlink on Linux/macOS,
  copy on Windows) gives the same isolation without git plumbing in three
  repositories.
- **Layers are directories, not bundles.** `etsi/`, `3gpp/`, `itut/`, `common/`
  are the unit of selection, so a "pack" never has to be cut.
- **The same tree serves every consumer.** Nothing is trimmed per SDO by editing a
  skill; the profile decides what is visible.

## Three skill shapes

| Shape            | Use when                                   | Where detail goes      |
| ---------------- | ------------------------------------------ | ---------------------- |
| Inline rule      | procedure fits one screen                  | stays in `SKILL.md`    |
| Reference-heavy  | lookups, tables, spec extracts             | `references/*.md`      |
| Asset-heavy      | payloads (templates, mapping tables)       | `assets/`              |

The 8 KiB body budget is the forcing function: when a skill crosses it, the detail
is already separable and moves to `references/`.

## Layer contract

Rules point **up**: `etsi-drafting` may name `sdo-docx-formatting`,
`sdo-docx-formatting` may not name `etsi-drafting`. A rule is placed in the highest
layer where it holds without qualification. That keeps `common` reusable for a
fourth SDO or a national body, and keeps SDO layers thin.

## Audit of the inherited tree (2026-10-20)

The 22 skills migrated from `jr2804/prompts/skills/standards`, plus
`etsi-directives`:

- **23 skills**: 5 `common`, 4 `etsi`, 9 `3gpp`, 5 `itut`.
- **Cross-references are consistent.** Zero unknown skill IDs and zero broken path
  references inside `SKILL.md` and `references/`. The stale IDs quoted in earlier
  planning notes (`etsi-meetings`, `itut-meetings`, `3gpp-spec-retrieval`, ...)
  appear only in those planning notes, not in the skills themselves.
- **Seven skills exceed the 8 KiB budget** - the merge worklist is real, not
  cosmetic: `itut-drafting` (24.5 KiB), `etsi-directives` (13 KiB),
  `sdo-writing-style` (10.7 KiB), `3gpp-change-request` (9 KiB),
  `3gpp-tdocs` (8.9 KiB), `3gpp-specifications` (8.3 KiB),
  `3gpp-portal-authentication` (8.2 KiB).
- **One layout variance**: `3gpp/3gpp-change-request/workflow.md` sits at the skill
  root instead of `references/workflow.md`; the rest of the tree uses
  `references/`.
- `itut-drafting` still uses `@para` / `@w14` style references in prose. Harmless,
  but they are ambiguous with skill mentions.

## Not decided yet

- Generated skill catalog page (from frontmatter) versus hand-written README tables.
- Vendoring CLI: `sdo-skills sync --profile etsi --target <repo>`.
- Evaluation harness: does a profile actually improve a drafted contribution?
