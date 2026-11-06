# Revising a Change Request

A revision re-issues an existing CR. It does not start a new CR: the CR
number stays, the revision number counts up, and the change itself is
usually the same text the WG already agreed.

Normative source: the 3GPP step-by-step guide, "Change Requests -
Step-by-step"
(<https://www.3gpp.org/specifications-technologies/specifications-by-series/change-requests-step-by-step>).

## What Changes on a Revision

| Element | On a revision |
|---|---|
| CR number | Unchanged. The 4-digit number allocated by the portal stays (`0009` = the 9th CR to that spec). |
| CR revision number | Incremented. The original version carries a hyphen (`-`, revision zero); the first revision shows `1`, the second `2`. |
| TDoc number | Changed. Every version is its own TDoc. |
| CR body | Unchanged unless the WG or the TSG changed it. |
| Date | The date the revised version was produced (`yyyy-MM-dd`). |
| Source to WG | Unchanged. Still the organization(s) that proposed the CR at WG level. |
| Source to TSG | Changed to the actual state: the identity of the TSG debating the matter, the organization(s) proposing the revised version, or text such as "WG Chairman" or "WG Secretary". |
| CR revision history | Optional. Records what changed from the original version to revision 1, revision 2, and so on. |

The header showing the original meeting and WG document number is
preserved; the document identity of the new version is marked by placing
the text "revision of" before the original WG document header.

## Portal Procedure

1. Create the new document on the 3GU portal with the document type **CR**.
   The type *Draft CR* is deprecated and its use is strongly discouraged -
   only legacy items still on the portal carry it.
2. Set the **Is revision of:** field to the TDoc number of the version being
   revised. The portal copies that version's metadata into the new document
   and keeps the link to its predecessor (the TDoc metadata field is
   `is_revision_of`, see `3gpp-tdocs`).
3. Download the cover sheet of the new TDoc from the template generator.
   Always start from this file - it carries the meeting reference, the
   document properties and the cover-sheet fields already filled in:

   ```text
   https://portal.3gpp.org/ngppapp/TdocTemplateGenerator.aspx?uid=<tdoc-nbr>
   ```

   Example: `https://portal.3gpp.org/ngppapp/TdocTemplateGenerator.aspx?uid=S4-261945`
4. Add the one thing the generator does not cover: the *revision of* marker
   on the second line of the cover page (next section).
5. Add the CR body, then upload the document to the portal.

Because the portal fills the cover sheet from the version named in **Is
revision of:**, the CR number comes back unchanged and the revision number
is already incremented.

## The One Manual Gap: the "revision of" Marker

The generated cover sheet has two header lines:

```text
3GPP TSG-SA4 Meeting #138                                    S4-261945
Calgary, Canada, 16th Nov 2026 - 20th Nov 2026
```

Line 1 ends with the TDoc number, right-aligned. Line 2 carries the
place, the country and the meeting dates. Neither line says which version
is being revised, so the marker has to be added by hand:

```text
Calgary, Canada, 16th Nov 2026 - 20th Nov 2026     revision of S4-261186
```

The marker is a tab, then the text `revision of` (with a trailing space) and
the TDoc number of the version being revised - lowercase, no colon. It is
right-aligned through a right tab stop at 9639 twips, the same stop that
right-aligns the TDoc number on line 1.

### DOCX Structure

Both cover lines use the paragraph style `CRCoverPage`. The generator
emits the right tab stop on line 1 only, so the paragraph properties of
line 2 need the tab stop as well:

```xml
<w:pPr>
  <w:pStyle w:val="CRCoverPage"/>
  <w:tabs><w:tab w:val="right" w:pos="9639"/></w:tabs>
  <w:outlineLvl w:val="0"/>
  <w:rPr><w:b/><w:noProof/><w:sz w:val="24"/></w:rPr>
</w:pPr>
```

The marker is appended as the last runs of that paragraph, in the same
character formatting as the place and date text (bold, 12 pt):

```xml
<w:r><w:rPr><w:b/><w:noProof/><w:sz w:val="24"/></w:rPr><w:tab/><w:t xml:space="preserve">revision of </w:t></w:r>
<w:r><w:rPr><w:b/><w:noProof/><w:sz w:val="24"/></w:rPr><w:t>S4-261186</w:t></w:r>
```

The place, the country and the dates are `DOCPROPERTY` fields. Keep them
intact - copy the original paragraph, add the tab stop and the marker
runs, and replace the paragraph as a whole. Patch it with `officecli
raw-set`, targeting the second `CRCoverPage` paragraph, and use a real
tab run (`<w:tab/>`), never spaces. See `sdo-docx` for the raw-set
patterns and the safe-edit rules.

```bash
mise x github:iOfficeAI/OfficeCLI -- officecli raw-set "<file>.docx" /document \
  --xpath '(//w:p[w:pPr/w:pStyle/@w:val="CRCoverPage"])[2]' \
  --action replace --xml '<w:p>...</w:p>'
```

## File Name

When the CR is presented to the TSG for approval, the Word file is named:

```text
<specnumber_no_dot>_CR<4-character_CR_number>[r<revision_number>]_(<release>)_[<WG_tdoc_number>[_<free_text>]].doc[x]
```

- `<specnumber_no_dot>`: the TS or TR the CR applies to, the dot after the
  series part omitted (`21900` for TR 21.900)
- `<4-character_CR_number>`: the CR number, padded with leading zeros to
  four characters (`0012`)
- `[r<revision_number>]`: only for a revised CR; a single digit (very
  rarely two), separated from the CR number by a lower case `r`
- `(<release>)`: the Release identity in the usual format (`R99`, `Rel-4`,
  `Rel-5`)
- `[<WG_tdoc_number>]`: the TDoc identity under which the CR was agreed at
  working group level
- `[_<free_text>]`: optional free text, for example an abbreviated title

`<WG_tdoc_number>` and the underscore in front of it are omitted when the
CR has not previously been presented to the responsible working group. That
is in particular the case when the CR is modified from what the WG agreed -
for example when it is revised by email agreement after the WG meeting, or
when it is revised as a result of discussion during the TSG plenary itself.

At working group level the Word file is named per the 3GPP Working
Procedures, and the zip file that carries it is named simply as the TDoc
number.

## Worked Example

CR 0009 to TS 26.260 (Rel-20), revised twice:

| Version | TDoc | CR number | Revision | Cover line 2 |
|---|---|---|---|---|
| Original | S4-260953 | 0009 | `-` | meeting 136, Montreal |
| Revision 1 | S4-261186 | 0009 | 1 | `revision of S4-260953` |
| Revision 2 | S4-261945 | 0009 | 2 | `revision of S4-261186` |

The CR number `0009` never changes, the revision number counts 1, 2, and
each version is a new TDoc. The cover sheet downloaded from the template
generator for `S4-261945` already carries `0009` and revision `2`; only the
`revision of S4-261186` marker is missing.

## Related

- `references/cr-format.md` - CR number format, status codes, categories,
  cover-sheet fields
- `references/workflow.md` - lifecycle and submission steps
- `references/cr-checklist.md` - submission and revision checklists
- `3gpp-tdocs` - TDoc numbers and portal metadata fields
- `3gpp-portal-authentication` - portal login and metadata access
- `sdo-drafting` - template, front matter and the TDoc revision workflow
