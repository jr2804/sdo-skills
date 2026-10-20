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

Rules point **up**: `sdo-drafting` may name `sdo-docx`, `sdo-docx` may not name
`sdo-drafting`. A rule is placed in the highest layer where it holds without
qualification. That keeps `common` reusable for a fourth SDO or a national body,
and keeps SDO layers thin.

## The tree as it stands (2026-10-20)

**19 skills**: 4 `common`, 4 `etsi`, 8 `3gpp`, 3 `itut`. The linter reports zero
errors and zero warnings.

| Layer    | Skills                                                                                                                        |
| -------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `common` | `sdo-writing`, `sdo-docx`, `sdo-drafting`, `sdo-ipr`, `sdo-project-setup`                                                     |
| `etsi`   | `etsi-governance`, `etsi-directives`, `etsi-procedures`, `etsi-tools`                                                         |
| `3gpp`   | `3gpp-basics`, `3gpp-working-groups`, `3gpp-meetings`, `3gpp-tdocs`, `3gpp-change-request`, `3gpp-releases`, `3gpp-specifications`, `3gpp-portal-authentication` |
| `itut`   | `itut-reference`, `itut-contributions`                                                                                        |

### What the consolidation changed

- The 23 inherited skills became 19. Merges: `sdo-writing-style` +
  `sdo-writing-conventions` → `sdo-writing`; `sdo-docx-formatting` +
  `sdo-docx-operations` → `sdo-docx`; the three `*-drafting` skills →
  `sdo-drafting` with a per-SDO reference subtree; `etsi-basics` →
  `etsi-governance`; `itut-basics` + `itut-recommendations` → `itut-reference`;
  `itut-patents` → `sdo-ipr`; `etsi-spec` → `etsi-tools`.
- New: `etsi-procedures` (meetings, contributions, work items, approval).
- Every skill body is now under the 8 KiB budget, and the detail sits in
  `references/`, `assets/` or `scripts/`.
- The 3GPP skills also absorbed the second-generation split from
  `forge.3gpp.org/rep/reimes/awesome-3gpp-skills`: runnable
  `scripts/portal_session.py` and `scripts/tdoc_pattern.py`, the specification
  and TDoc number-format references, and the working-group FTP structure. The
  forge variant is superseded by this tree.

### Known gaps

- `3gpp-basics`, `3gpp-meetings` and `3gpp-releases` are still single-file
  skills with a few kilobytes of inline detail. They are under budget, so
  they are left alone until something pushes them over.
- `etsi-directives` keeps its 13 chapters as a generated reference tree; only
  the index and the core frameworks are in `SKILL.md`.

## Not decided yet

- Generated skill catalog page (from frontmatter) versus hand-written README tables.
- Vendoring CLI: `sdo-skills sync --profile etsi --target <repo>`.
- Evaluation harness: does a profile actually improve a drafted contribution?
