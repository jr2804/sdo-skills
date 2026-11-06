# CR Format Reference

Numbering, status codes, document structure and databases for 3GPP Change
Requests. The lifecycle and the submission steps are in
`references/workflow.md`.

## CR Number Format

The CR number is the identifier the portal allocates for the change: four
characters with leading zeros, and no "CR" prefix (`0095`, not `CR0095`).
It identifies the change to a specification, not a version of it - the
revision number counts up separately.

The document identifier built on the CR number looks like this:

```text
<specnumber_no_dot>*_CR*<4-character_CR_number>*[r*<revision_number>*]
```

**Components:**

- `<specnumber_no_dot>`: Spec number without dot (e.g., `21.456` for TS 21.456)
- `*`: Literal asterisk
- `<4-character_CR_number>`: 4-digit CR number padded with leading zeros (e.g., `0095`)
- `[r*<revision_number>*]`: Lowercase 'r' + revision number (only for revised CRs)

**Examples:**

- Initial: `31.102_0095` - CR 0095 to spec 31.102
- First revision: `31.102_0095_r1` - Revision 1 of spec 31.102
- Mirror CR: `31.103_0095` - Mirrored CR to spec 31.103

The portal allocates the CR number, and it **never changes** on a
revision - only the revision number counts up. The file name presented to
the TSG follows its own convention, see "File Naming Convention" below
and `references/cr-revision.md`.

## CR Status Meanings

| Status | TSG | WG | Meaning |
|---------|-----|----|--------|
| use | YES | YES | Valid for use |
| agreed | - | YES | WG agreed, forward to TSG |
| approved | YES | NO | Final decision (implemented) |
| rejected | YES | YES | Sustained objection |
| revised | YES | YES | Modified to new revision |
| merged | YES | YES | Combined with other CRs |
| postponed | YES | YES | Deferred to later date |
| endorsed | NO | YES | WG consensus, technically correct |
| withdrawn | YES | YES | Retracted before discussion |
| reissued | NO | NO | Recast unchanged in another TSG |
| noted | NO | NO | Deprecated (ambiguous term) |

## CR Categories

CRs are classified by category to indicate their nature:

- **Category F (Corrective)**: Corrective CRs, typically to earliest Release version
- **Category A (Mirror)**: Mirrors of CRs to previous Release versions
- **Mirror CRs require**: Same WI code per Release
- **Mirror CRs are marked**: Category A in spec history

### Category Definitions

| Category | Description |
|-----------|-------------|
| F | Corrective CRs applied to earliest Release version |
| A | Mirror CRs of same spec to different Release version |
| TEI | Technical Enhancement or Improvement |

## Step-by-Step Instructions

3GPP provides detailed step-by-step instructions for writing CRs:

- **URL**: <https://www.3gpp.org/specifications-technologies/specifications-by-series/change-requests-step-by-step>

**Key Sections:**

01. Header (meeting details, WG document number)
02. Spec number, CR number
03. CR revision number (for revised CRs only)
04. Current version
05. Title
06. Source to WG
07. Source to TSG
08. Work item code
09. Date
10. Category
11. Release
12. Consequences if not approved
13. Clauses affected
14. Other specs affected
15. Other comments
16. CR revision history
17. Filename convention
18. Body of CR
19. Other considerations

## CR Revision Number and History

Two fields carry the revision, and they mean different things:

- **CR revision number** (cover sheet): the original version carries a
  hyphen (`-`, revision zero). Every revision increments the number, so
  the first revision shows `1` and the second `2`. The CR number stays
  the same - a revision is a new version of the same CR, never a second
  CR for the same change. See `references/cr-revision.md`.
- **CR revision history** (optional): records what changed from the
  original version to revision 1, revision 2, and so on.

## File Naming Convention

At working group level the Word file is named per the 3GPP Working
Procedures, and the zip file that carries it is named simply as the TDoc
number.

When the CR is presented to the TSG for approval, the Word file is named:

```text
<specnumber_no_dot>_CR<4-character_CR_number>[r<revision_number>]_(<release>)_[<WG_tdoc_number>[_<free_text>]].doc[x]
```

- `<specnumber_no_dot>`: the TS or TR the CR applies to, the dot after the series part omitted (`21900` for TR 21.900)
- `<4-character_CR_number>`: the CR number, padded with leading zeros to four characters (`0012`)
- `[r<revision_number>]`: only for a revised CR; a single digit (very rarely two), separated from the CR number by a lower case `r`
- `(<release>)`: the Release identity in the usual format (`R99`, `Rel-4`, `Rel-5`)
- `[<WG_tdoc_number>]`: the TDoc identity under which the CR was agreed at working group level
- `[_<free_text>]`: optional free text, for example an abbreviated title

`<WG_tdoc_number>` and the underscore in front of it are omitted when the
CR was not previously presented to the responsible working group - in
particular when the CR is modified from what the WG agreed.

The zip file for the TSG submission follows the 3GPP Working Procedures
and bears a cover sheet listing the included CRs.

Revision procedure and worked example: `references/cr-revision.md`.

## Work Items

Each CR must be associated with a **Work Item (WI) code**:

- Obtained from official WI list: <https://www.3gpp.org/ftp/Specs/html-info/WI-List.htm>
- **Format**: 6-digit numeric code (e.g., `123456`)
- **Purpose**: Justifies the new feature or modification

## CR Database

### Netovate Search Tool

3GPP has an agreement with Netovate to provide a free CR database search:

- **URL**: <http://netovate.com/cr-search/>
- **Access**: Free web-based search tool
- **Features**: Search by spec number, CR number, or status

### 3GPP CR Database

Available on 3GPP FTP:

- **Directory**: `/ftp/Information/Databases/Change_Request/`
- **Format**: MS Access™ (.mdb) database
- **Access**: Direct download or via portal

### CR Status Tracking

Each spec maintains a history box listing all CRs that have been approved for that specification.

## Resources

- 3GPP Official: <https://www.3gpp.org/>
- 3GPP Portal: <https://portal.3gpp.org/>
- Step-by-step: <https://www.3gpp.org/specifications-technologies/specifications-by-series/change-requests-step-by-step>
- CR Database: /ftp/Information/Databases/Change_Request/
- WI List: <https://www.3gpp.org/ftp/Specs/html-info/WI-List.htm>
- Netovate: <http://netovate.com/cr-search/>
