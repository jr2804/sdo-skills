# AGENTS.md — POLICIES / DOX authoring

Detail file for `.agents/POLICIES.md`. Rule: AGENTS.md and `.agents/` files
share limited context — bloat and duplication are the failure mode.

## Where a rule lives

A rule goes in the **highest (most general) tier that fully applies**:

- Applies to **all code in the project** → `.agents/POLICIES.md` (default).
- Meaningful **only inside one subtree** → that subtree's `AGENTS.md`.
- Just helps navigation → the parent's Child DOX Index, nothing else.

## Reference, don't restate

A rule appears in **exactly one file**. Other files use a **pointer line**:
`<topic> — see <file>`. Never copy the rule, rationale, or example.

## Rule first, rationale second, never third

A DOX line is the rule. If a rationale is costly to rediscover, add one
short clause. No multi-paragraph explanations or code pairs — those belong
in a skill or `docs/`, linked once.

## Content rules

- **No tree views.** Generate on demand with `rg --files | tree-cli --fromfile`.
- **No history in AGENTS.md files.** Git log has routine history. Record only
  decisions costly to rediscover — in `.agents/HISTORY.md` (or
  `.agents/history/` for overflow archives).
- **Lean state files, optional subdirectories.** State files stay brief entry
  points (index-style, not sprawling documents). A state file that grows past
  its size budget (≤ **120 lines**) must be split into
  `.agents/<topic>/<name>.md` subdirectories — not stuffed longer. Every file
  in an optional subdirectory **MUST** be mentioned in the state file that
  owns it.
- **No TODO lists.** Use issue trackers or beads.
- Prefer direct bullets with explicit names.
- Trim obvious statements, repeated rules, and detail that no longer applies.
