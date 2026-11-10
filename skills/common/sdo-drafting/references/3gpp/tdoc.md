# 3GPP TDoc conventions

3GPP-specific document structure, assets and conventions for meeting
submissions (TDocs).

## Assets

- `assets/3gpp/Tdoc_Template.docx` -- canonical Word template with all required
  3GPP styles. Copy to `ref/Tdoc_Template.docx` when initializing a new
  project (see `sdo-project-setup` for the common project bootstrap workflow).
  This is a user-crafted file containing all required styles
  (`B1`, `B2`, `NO`, `NW`, `TH`, `TAH`, `TF`, `EX`, `PL`, etc.) and is
  **not** tied to an official 3GPP release cycle.

## Heading conventions (3GPP-specific override)

3GPP headings use **manual numbering only** (never Word auto-numbering).
See `sdo-docx/references/formatting/headings.md` for full rules. The
`References` section is unnumbered and always the last section.

## Reference list entries (TDoc citations)

Mechanics of the References section (entry style, SEQ fields, bookmarks,
ordering) live in `sdo-docx/references/formatting/citations.md`. The
**citation text** for a cited 3GPP TDoc -- any TDoc series (`S4-`, `SP-`,
`RP-`, `CP-`, ...) -- always follows one pattern:

```text
3GPP <TDocNbr>: "<title>", <source>, <meeting>, <place>, <month year>
```

Example (generic):

```text
3GPP S4-261234: "Example TDoc title", Example Company Ltd, SA4#137, Stockholm, Sweden, August 2026
```

- `<source>` is the organisation that submitted **that** TDoc, not the
  source of the document being drafted.
- When citing the current revision of a revised TDoc, append
  `(revision of <TDocNbr>)`.
- Every field is mandatory. If a field is unknown (typically `source`,
  `place` or the date), look it up first -- `3gpp-tdocs` TDoc metadata and
  `3gpp-meetings` meeting pages carry the fields; ask the user only if the
  lookup fails. Never silently drop a field and never invent a value.
