# AGENTS.md — HISTORY

State file. The one file that may reference the past — sparingly. Read when
relevant to the current task; long-term memory for decisions, not a log.
Routine history lives in git; only record what is costly to rediscover.

## Format

| Date       | Decision   | Rationale | Git ref           |
| ---------- | ---------- | --------- | ----------------- |
| 2026-11-06 | Adopted the `agents-scaffold` DOX framework as the state-file layout: added `.agents/TOOLS.md`, split `POLICIES.md` into `.agents/policies/` detail files, tracked `/.agents/<topic>/` subdirectories in `.gitignore` | Keeps `AGENTS.md` lean and gives tooling an owned home; the 120-line state-file budget forced the split rather than growing `POLICIES.md` | `agents-scaffold@b495205` |

## Record

- High-level architectural decisions and breaking changes.
- Dependency, tooling, and platform choices — including the alternative that lost.
- False turns and rejected approaches, with the reason.
- Completion of an implementation plan (link to its archive below).

## Do not record

- Routine commits, refactor logs, session activity, release notes.
- Anything obvious from git, the code, or current AGENTS.md/state files.

## Guidance

- Keep entries brief — enough to reconstruct the reasoning.
- Link to the relevant commits or tags.
- If this file grows large, move older entries to `.agents/history/` and keep
  a pointer here.
- Completed implementation plans are archived as single files at
  `.agents/history/<YYYY-MM-DD-plan-name>.md` and linked from the decision
  entry they belong to. The trigger to archive is **plan completion**, not
  file growth — see **Archive a plan** below.

## Archive a plan

When a plan's work is complete — the point to do this is when the
implementation lands, not at the planning stage:

1. Consolidate `.agents/plans/<YYYY-MM-DD>-<feature-name>/` into a single
   file `.agents/history/<YYYY-MM-DD-plan-name>.md` (use the plan directory's
   date prefix, e.g. `2026-07-14-api-migration.md`).
2. Delete the plan directory.
3. Add an entry to `.agents/HISTORY.md` referencing the archive and its
   commit.

If the date prefix on the plan directory is missing or wrong, use the date
work started — record it in the archive filename exactly as-is.
