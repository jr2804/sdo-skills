# AGENTS.md — POLICIES

Always applicable. Boundaries, priorities, verification, checklist.

## Priorities

1. Correctness
2. Evidence
3. Safety
4. Minimal changes
5. Consistency
6. Performance

## Boundaries

- NEVER fabricate paths, commits, APIs, config keys, env vars, test results,
  or benchmark numbers. If you don't know, say so.
- NEVER guess at command names, flags, or paths. Read source or run `--help`.
- NEVER add secrets, API keys, or tokens to files. Use env vars.
- NEVER run destructive commands (`rm -rf`, `git reset --hard`,
  `git push --force`) without explicit confirmation.
- NEVER delete or move files without explicit instruction.
- NEVER create temp files in project root. Use dedicated temp dir.

## Change constraints

- Minimal, surgical edits. Preserve existing style.
- No new dependencies without explicit instruction.
- No unrelated refactoring while fixing a bug.

## Code quality

Universal defaults. Project-specific standards live in child AGENTS.md.

- **SRP** — one reason to change per module/function.
- **DRY** — check before adding. Extract on third occurrence (Rule of Three).
- **Redundant code** — remove dead branches, unreachable conditions, unused
  params/imports before finishing.
- **Duplication vs. abstraction** — prefer duplication over wrong premature
  abstraction.
- No new code-quality tooling by default — opt in per project.

## Completion checklist

- Change solves the stated problem
- Relevant validation ran (or gaps stated)
- No unintended side effects or secrets exposed

## DOX authoring

Tier assignment, reference-don't-restate, content rules and the size budget's
authoring rationale — see `policies/dox-authoring.md`. Apply it on every DOX
change; the operational limits stay below (**Size budget**).

## Implementation Plans & Documentation

Plan location and naming, the archive-on-completion trigger, history overflow,
the docs-are-committed rule, and the no-logbook rule — see
`policies/plans.md`.

## State file subdirectories

Each state file has a matching optional subdirectory for growth — the file
stays a lean index and the subdirectory carries the detail:

| State file       | Optional subdirectory  |
| ---------------- | ---------------------- |
| `FILES.md`       | `.agents/files/`       |
| `POLICIES.md`    | `.agents/policies/`    |
| `TOOLS.md`       | `.agents/tools/`       |
| `MAINTENANCE.md` | `.agents/maintenance/` |

- Only create a subdirectory when its state file approaches its size budget.
- Every file in a subdirectory MUST be listed in its state file (name + one
  line of what it covers). A subdirectory file missing from the index is
  dead content — move it or delete it.
- `ONBOARDING.md` and `HISTORY.md` have no subdirectories: entry points stay
  a single file, and history growth goes to `.agents/history/`.

## Size budget

- `.agents/` files: ≤ **120 lines** (always-injected context).
- Subtree `AGENTS.md`: ≤ **250 lines** (loaded cumulatively with parents).

Exceeding the budget signals restating instead of pointing, or hoarding
rationale. Cut first; split into the matching subdirectory only when the
content is genuinely needed.

## Verification

```bash
mise all        # test, lint, lint:skills, sort, spell, format, format-md, docs
mise test       # pytest with 100 % coverage gate
mise lint       # ruff --fix over src/, tests/, scripts/
mise typecheck  # ty check src/, tests/, scripts/
mise sort       # pyreorder structural-order check
mise spell      # codespell
mise format     # pyreorder run + ruff format + import sort
mise format-md  # rumdl fmt over src/, docs/, tests/, repo root (incl. .agents/)
```

CI (`.github/workflows/ci.yml`) gates `lint`, `sort`, `spell`, `lint:skills`,
`test` and `docs`; `typecheck` and `format-md` are local-only — run them before
pushing Python or Markdown changes. Pre-commit hooks (`.pre-commit-config.yaml`)
run a subset on every commit; `pre-commit run --all-files` checks the tree.

## Response format

Concise and specific. No filler, intros, or restated requirements.
Answer direct questions directly.

For review/debugging/analysis: findings with references, conclusion,
approach. Mention caveats.

## Subdirectory

- `policies/dox-authoring.md` — tier assignment, reference-don't-restate,
  rule-first wording, content rules.
- `policies/plans.md` — implementation plans, archiving, documentation rules.
