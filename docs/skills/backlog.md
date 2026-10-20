# Consolidation backlog

!!! note "Status"
    The consolidation pass is largely done. The tree went from 23 inherited
    skills to **19** (`5 common`, `4 etsi`, `8 3gpp`, `2 itut`), every body is
    under the 8 KiB budget, and the linter reports **0 errors, 0 warnings**.
    The writer repository, the install path and the routing evals are done as
    well; what is left is in [Remaining work](#remaining-work).

    The analysis below was written on 2026-05-21 for 21 skills in a single flat
    directory. It is kept as the record of *what was found*, not as a task list.
    Section names and skill IDs in it are the pre-merge ones.

## Inventory as inherited

| Layer | 3GPP | ITU-T | ETSI | Common (sdo-) |
|-------|------|-------|------|---------------|
| **1. Common** | -- | -- | -- | 5 skills |
| **2. Reference** | 8 skills | 3 skills | 2 skills | -- |
| **3. Drafting** | 1 skill | 1 skill | 1 skill | -- |
| **Total** | 9 | 4 | 3 | 5 = **21** |

______________________________________________________________________

## A. Missing skills (as found on 2026-05-21)

| Skill | SDO | Priority | Why needed | Now |
|-------|-----|----------|-----------|-----|
| `itut-meetings` | ITU-T | Medium | Meeting scheduling, collective letters, cancellation criteria | still open |
| `etsi-meetings` | ETSI | Medium | No meeting structure/procedures skill existed | **closed** by `etsi-procedures` |
| `etsi-contributions` | ETSI | Medium | Contribution submission procedures, TDoc numbering | **closed** by `etsi-procedures` |
| `etsi-work-items` | ETSI | Low | Work Item lifecycle | **closed** by `etsi-procedures` |
| `3gpp-spec-retrieval` | 3GPP | Low | Parallel to `etsi-spec` | still open |
| `itut-spec-retrieval` | ITU-T | Low | Parallel to `etsi-spec` | still open |

## B. Cross-reference gaps (as found)

| Skill | References | Issue | Now |
|-------|-----------|-------|-----|
| `itut-drafting` | `itut-meetings` | Skill did not exist | reference dropped in the merge |
| `sdo-docx-operations` | `docx-svg` | Valid skill outside this tree | still open |
| `sdo-docx-formatting` | `3gpp-drafting` | Missing 3GPP in the cross-refs | **closed** |

Older Layer 2 skills used `@skill-name` instead of `` `skill-name` ``. All
`@`-mentions are gone; the linter now warns on them.

## C. Capability coverage as found

| Capability | 3GPP | ITU-T | ETSI |
|-----------|------|-------|------|
| Organisation basics | `3gpp-basics` | `itut-basics` | `etsi-basics` |
| Meeting structure | `3gpp-meetings` | *missing* | *missing* |
| Working groups | `3gpp-working-groups` | *(in basics)* | *(not applicable)* |
| Contributions/submissions | `3gpp-tdocs` (data) | `itut-contributions` | *missing* |
| Change requests | `3gpp-change-request` | *(in basics)* | *(not applicable)* |
| Spec numbering/formats | `3gpp-specifications` | `itut-recommendations` | `etsi-spec` |
| Spec retrieval script | *missing* | *missing* | `etsi-spec` |
| Release structure | `3gpp-releases` | *(in basics)* | *(not applicable)* |
| Portal authentication | `3gpp-portal-auth` | *missing* | *missing* |
| Work items | *(partial, in basics)* | *(in basics)* | *missing* |
| Drafting (.docx) | `3gpp-drafting` | `itut-drafting` | `etsi-drafting` |
| Style-name mapping | table in drafting | table in drafting | table in drafting |
| Drafting template | Tdoc_Template.docx | template.docx | *missing* |
| Project setup | `sdo-project-setup` | `sdo-project-setup` | `sdo-project-setup` |

## D. Feature completeness as found

### Common layer (sdo-)

| Skill | Depth | Gaps as found |
|-------|-------|--------------|
| `sdo-docx-formatting` | High -- 6 reference files | Missing: `3gpp-drafting` in cross-refs |
| `sdo-docx-operations` | High -- 5 scripts, schemas, 4 references | None significant |
| `sdo-project-setup` | High -- script, 3 references | None |
| `sdo-writing-conventions` | High -- 11-section extract | None; ITU-specific parts were generalized |
| `sdo-writing-style` | High -- 14 core rules + checks | None |

### 3GPP layer

All eight reference skills were single-file with 5-9 KB of inline detail, and
all used `@skill-name` cross-references. `3gpp-drafting` had no reference from
`sdo-docx-formatting` back to it. All of that is resolved.

### ITU-T layer

`itut-drafting` was 24.5 KiB, the largest body in the tree. `itut-basics` and
`itut-recommendations` were complete on their own.

### ETSI layer

`etsi-drafting` had no `.docx` template asset, and its style names were taken
from the 3GPP pool (likely correct, never verified against an ETSI skeleton).

## E. SDO-specific drafting completeness

### Template availability

| SDO | Template | Location now |
|-----|----------|--------------|
| 3GPP | Tdoc_Template.docx | `common/sdo-drafting/assets/3gpp/` |
| ITU-T | itu-t-recommendation-skeleton.docx | `common/sdo-drafting/assets/itut/` |
| ETSI | 10 ETSI skeletons | `common/sdo-drafting/assets/etsi/` |

### Metadata/property sync

| SDO | Mechanism |
|-----|-----------|
| 3GPP | `sdo-project-setup/scripts/set_docx_props.py` with the 3GPP `--props` mapping |
| ITU-T | same script with the ITU-T `--props` mapping |
| ETSI | **still open** -- needs ETSI custom property names |

### Style-name mapping coverage

All 16 abstract names from the former `sdo-docx-formatting` are mapped in all
three drafting sub-trees.

______________________________________________________________________

## Target shape: what the merge actually produced

The planned target was 12 skills. The delivered tree has 19, because the
3GPP and ITU-T reference skills were left as separate IDs rather than being
folded into two large `*-reference` skills. The reasoning: each 3GPP reference
skill answers a distinct question (working groups, releases, TDoc numbers,
portal auth), and merging them would have produced a skill that must be read
whole to answer any one of them. Progressive disclosure works per skill, not
only within a skill.

| Old | New | State |
| --- | --- | --- |
| `sdo-writing-style`, `sdo-writing-conventions` | `sdo-writing` | done |
| `sdo-docx-formatting`, `sdo-docx-operations` | `sdo-docx` | done |
| `3gpp-drafting`, `etsi-drafting`, `itut-drafting` | `sdo-drafting` + per-SDO references | done |
| `itut-patents` + ETSI IPR material | `sdo-ipr` | done |
| `etsi-basics` | `etsi-governance` | done |
| - (gap) | `etsi-procedures` | done |
| `etsi-spec` | `etsi-tools` | done |
| 8 x `3gpp-*` | kept as 8 IDs, each split into `references/` + `scripts/` | done differently |
| `itut-basics`, `itut-recommendations` | `itut-reference` | done |
| `itut-contributions` | `itut-contributions` | unchanged ID |
| `sdo-project-setup` | unchanged | ETSI `--props` mapping still missing |

Three rules that kept the merge safe:

- **8 KiB body budget.** Anything longer moves to a reference; the linter
  reports offenders.
- **ITU-T gets a sub-tree, not a single file** - `references/itut/{style-map,structure,equations,terms,numbering}.md`,
  because `itut-drafting` was 24.5 KiB and an ETSI-only consumer must not pay
  for it.
- **Descriptions became trigger enumerations** (the `etsi-directives` style),
  not summaries. That is what carries routing after a merge.

## Remaining work

| # | Item | Where | Notes |
|---|------|-------|-------|
| 1 | ETSI docx property mapping | `common/sdo-project-setup` | the `--props` hole from section E |
| 2 | `itut-meetings` | `skills/itut/` | meeting procedures from ITU-T A.1 |
| 3 | Spec retrieval for 3GPP and ITU-T | `skills/3gpp/`, `skills/itut/` | parallel to `etsi-tools/scripts/get_etsi_spec.py` |
| 4 | Generated skill catalog | `docs/` | catalog page from frontmatter instead of hand-written tables |
| 5 | Drop the per-project skill copies | consumer projects | `.agents/skills/` copies are now stale |

## Completed

- **Writer repository** - [jr2804/opencode-sdo-writer](https://github.com/jr2804/opencode-sdo-writer):
  one agent, three profiles (`etsi`, `3gpp`, `itut`), an install CLI and a
  `vendor.lock` that pins this repository at a tag.
- **Install path** - `opencode-sdo-writer init --profile etsi` copies the skill
  directories into `~/.config/opencode/skills/`, writes the agent into
  `~/.config/opencode/agents/` and records a manifest, so `update` and
  `uninstall` know what belongs to the package.
- **Routing evals** - `evals/routing.json`: 42 requests with the expected
  skill. The linter fails when a case names a skill that does not exist and
  warns when a skill of the tree is not expected by any case.
- **`itut-patents`** (2025-05-22) - from the Common Patent Policy Guidelines
  (2022) and the ITU patents book Ch.15: patent policy, IPR disclosure,
  3 licensing options, declaration forms, database, neutrality principles.
  Now part of `sdo-ipr`.
- **Skill map and lint** - the tree is split into layers and
  `scripts/lint_skills.py` is green.
- **Common merges** - `sdo-writing`, `sdo-docx`, `sdo-drafting`.
- **ETSI layer** - `etsi-governance`, `etsi-procedures`, `etsi-tools`.
- **3GPP and ITU-T** - 3GPP skills split into `references/` + `scripts/`,
  ITU-T reference skills merged.
- **3GPP cross-check against `awesome-3gpp-skills`** - the forge variant's
  `portal_session.py`, `tdoc_pattern.py`, specification and TDoc number
  references and the working-group FTP structure were imported. The forge
  repository is superseded by this tree and can be archived.
- **Tool invocation** - every external tool is pulled on demand through
  `mise x <spec> -- <tool>`; nothing is assumed to be installed.
