# AGENTS.md — POLICIES / plans & docs

Detail file for `.agents/POLICIES.md`. Where planning artifacts live, and how
they become durable records.

## Implementation Plans

- Plans, refactoring plans, and design docs go in
  `.agents/plans/<YYYY-MM-DD>-<feature-name>/` — NOT under version control.
- Phase-number prefixes keep file order matching implementation order, e.g.
  `01-sub-feature.md`, `02-next-sub-feature.md`.
- NEVER commit plans to git. They are mutable working artifacts.
- Shipped docs (user-facing guides, API references) go in `docs/` and
  ARE committed.

## Archive a plan

The trigger is **plan completion** — the moment the work lands, not a later
maintenance pass:

1. Consolidate `.agents/plans/<YYYY-MM-DD>-<feature-name>/` into one file
   `.agents/history/<YYYY-MM-DD-plan-name>.md`.
2. Delete the plan directory.
3. Add an entry to `.agents/HISTORY.md` referencing the archive and its commit.

If the plan directory's date prefix is missing or wrong, use the date work
started and record the filename exactly as-is.

## Documentation

- When `.agents/HISTORY.md` grows too large, archive older entries to
  `.agents/history/` and keep a pointer.
- `.agents/history/` IS version-controlled (durable decision records);
  `.agents/plans/` never is.
- AGENTS.md and state files describe the project's current contracts — never
  append session notes, iteration logs, or changelogs; delete stale text
  instead. `.agents/HISTORY.md` is the only permitted exception and holds
  high-level decisions only.
