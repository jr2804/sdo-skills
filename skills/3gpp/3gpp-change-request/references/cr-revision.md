# Revising a Change Request

A revision re-issues an existing CR. It does not start a new CR: the CR
number stays, the revision number counts up, and the change itself is
usually the same text the WG already agreed.

Three rules hold for every revision:

1. **The CR number stays the same.** It is the four-digit, zero-padded
   identifier the portal allocated once (`0009` is the ninth CR to that
   specification). A revision never gets a new number.
2. **The CR revision number increases.** `-` (revision zero) for the
   original, then `1`, `2`, and so on.
3. **It stays the same CR.** The revision is a new TDoc - a new version of
   an existing CR, not a second CR for the same change.

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

The new version keeps the original CR's identity and gets its own TDoc
number in the header; the only visible trace of the predecessor is the
"revision of" marker on the second cover line.

## Portal Procedure

Always drive a revision through the portal - never edit the previous cover
sheet by hand.

1. Create the new document on the 3GU portal with the document type **CR**.
2. Set the **Is revision of:** field to the TDoc number of the version being
   revised, for example `S4-261186`. This single field does the work: the
   portal fills in the CR number, the incremented CR revision number, the
   meeting reference and the document properties, and keeps the link to the
   predecessor (the TDoc metadata field is `is_revision_of`, see
   `3gpp-tdocs`).
3. Open the template generator for the new TDoc and download the cover
   sheet. **Always start from this page** - it is the recommended
   starting point for every revision, because the downloaded file already
   carries the meeting, the document properties and every cover-sheet field
   the portal derived from **Is revision of:**:

   ```text
   https://portal.3gpp.org/ngppapp/TdocTemplateGenerator.aspx?uid=<tdoc-nbr>
   ```

   Example: `https://portal.3gpp.org/ngppapp/TdocTemplateGenerator.aspx?uid=S4-261945`
   produces `S4-261945.docx` - a bare cover sheet named after the TDoc. Move
   it to the project's working file name
   (`S4-261945 - <title>.docx`) before editing, and keep the generated file
   until the document is uploaded, so the manual change stays reviewable.
4. Add the one thing the generator does not cover: the *revision of* marker
   on the second line of the cover page (next section).
5. Bring the CR body across from the version being revised. The generator
   returns the cover sheet plus an empty body skeleton (`==============First
   change==============` placeholders), so the tracked changes and the
   figures still have to come from the predecessor - start from the
   predecessor file and replace only its cover page, or copy the body in.
   The revised TDoc should then differ from its predecessor on the cover
   page alone.
6. Upload the document to the portal.

Because the portal fills the cover sheet from the version named in **Is
revision of:**, the CR number comes back unchanged and the revision number
is already incremented - do not type either of them by hand.

### What the Generator Fills

The downloaded cover sheet is a `DOCPROPERTY`-driven document: every field
reads a custom property of the same name, so the visible values follow the
properties and not the text. For `S4-261945` (CR 0009, revision 2) that is:

| Property | Value | Note |
|---|---|---|
| `Spec#` | `26.260` | target spec |
| `Version` | `19.1.0` | current version of the spec |
| `Cr#` | `0009` | inherited from the version being revised |
| `Revision` | `2` | incremented by the portal |
| `Tdoc#` | `S4-261945` | the new TDoc |
| `TSG/WGRef`, `MtgSeq` | `SA4`, `138` | from the meeting |
| `Location`, `StartDate`, `EndDate` | `Calgary, Canada`, `16th Nov 2026`, `20th Nov 2026` | cover line 2; the country is already part of `Location` |
| `Country`, `MtgTitle` | `<Country>`, empty | generator leaves these unfilled - nothing uses them in the downloaded cover sheet |
| `SourceIfWg`, `SourceIfTsg` | `HEAD acoustics GmbH`, empty | source fields |
| `RelatedWis`, `Release`, `Cat`, `ResDate` | `ATIAS_Ph3-MED`, `Rel-20`, `B`, `2026-11-06` | copied or set at creation |
| `CrTitle` | `CR on Updated test methods for TS 26.260` | CR title |

When the meeting data is carried into the predecessor file instead (its
cover page kept), check the form of cover line 2 there first. An older cover
page may render `Location` and `Country` as two fields
(`Montreal, Canada, ...`); copying the generator's `Location` value
`Calgary, Canada` into it then shows `Calgary, Canada, Canada`. Split the value
in that case: `Location` = `Calgary`, `Country` = `Canada`. Update the cached
field results along with the properties, so the text is right before Word
refreshes the fields.

Editing a document property is therefore the safe way to correct a field:
the cover sheet re-renders from the properties. Text typed over a field's
*result* is lost the next time Word refreshes the fields. Fix values the
portal owns at the portal (re-open the TDoc there), or in Word under
**File → Info → Properties → Advanced Properties → Custom**.

Two traps when editing the properties programmatically:

- **Never run `set_docx_props.py` on a generated CR cover sheet.** That
  script (see `sdo-project-setup`) *rebuilds* `docProps/custom.xml` from
  `PLAN.md` front matter and drops every property it does not map, so the
  cover sheet's `Cr#`, `Revision`, `Tdoc#`, `Spec#`, `Version`, `Cat`,
  `Release` and `RelatedWis` fields lose their source and Word renders them
  as field errors.
- **Never `raw-set` `/docProps/custom.xml`.** Unlike `/document`, that part
  is not patched in place: the call replaces the whole part and leaves an
  invalid stub. Rewrite the zip entry instead - read
  `docProps/custom.xml`, replace the `<vt:lpwstr>` value inside the
  `<op:property name="...">` element, write the archive back - then check
  the result with `mise x github:iOfficeAI/OfficeCLI -- officecli validate
  <file>.docx`.

The fields keep their cached result until Word refreshes them, so a wrong
property can look right in a text dump and wrong on screen after F9.

## The One Gap in the Generated Cover Sheet: the "revision of" Marker

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

The predecessor already carries such a marker, and it points one step
further back: `S4-261186`, the revision 1, says `revision of S4-260953`.
Take the formatting from that paragraph and the number from the version
you are revising - not the number you find there.

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

The place, the country and the dates are `DOCPROPERTY` fields
(`Location`, `Country`, `StartDate`, `EndDate`). Depending on the generator
version they appear as `<w:fldSimple>` elements or as
begin/separate/end `w:fldChar` runs, and `Location` may already carry the
country (`Calgary, Canada`) instead of splitting it out. Keep whatever form
is present intact - copy the original paragraph, add the tab stop and the
marker runs, and replace the paragraph as a whole. Patch it with `officecli
raw-set`, targeting the second `CRCoverPage` paragraph, and use a real
tab run (`<w:tab/>`), never spaces. See `sdo-docx` for the raw-set
patterns and the safe-edit rules.

```bash
mise x github:iOfficeAI/OfficeCLI -- officecli raw-set "<file>.docx" /document \
  --xpath '(//w:p[w:pPr/w:pStyle/@w:val="CRCoverPage"])[2]' \
  --action replace --xml '<w:p>...</w:p>'
```

A recipe that is known to work: extract the second `CRCoverPage` paragraph
with `mise x github:iOfficeAI/OfficeCLI -- officecli raw <file> /document`,
insert `<w:tabs><w:tab w:val="right" w:pos="9639" /></w:tabs>` right after
its `<w:pStyle w:val="CRCoverPage" />`, append the two marker runs before
the closing `</w:p>`, and feed the result to `raw-set --action replace`.
The body of the paragraph - the `DOCPROPERTY` fields - is carried over
unchanged, so the fields keep working. Afterwards the second line reads:

```text
Calgary, Canada, 16th Nov 2026 - 20th Nov 2026	revision of S4-261186
```

(the gap before `revision of` is the `<w:tab/>`, rendered at the new right
tab stop).

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
- `references/cr-revision-marks.md` - authorship of the revision marks in the
  CR body
- `3gpp-tdocs` - TDoc numbers and portal metadata fields
- `3gpp-portal-authentication` - portal login and metadata access
- `sdo-drafting` - template, front matter and the TDoc revision workflow
