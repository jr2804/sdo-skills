# CR Submission Checklist and Pitfalls

What a CR cover sheet must contain, the usual mistakes, and the rules behind
mirror CRs and editorial updates.

## CR Submission Checklist

01. [ ] Unique_ID value from Work Item
02. [ ] TDoc number of Work Item Description (WID) document
03. [ ] Name of rapporteur for TS/TR (or contact coords for TR)
04. [ ] Target date from WID (approval date)
05. [ ] Source to WG (responsible 3GPP member)
06. [ ] Source to TSG (if presented directly to TSG)
07. [ ] Work item code (from WI list)
08. [ ] Release (one only)
09. [ ] Category (TEI for technical enhancements)
10. [ ] Title (descriptive, not redundant)
11. [ ] Reason for change
12. [ ] Summary of changes
13. [ ] Consequences if not approved
14. [ ] Clauses affected (list individually)
15. [ ] Other specs affected
16. [ ] Other comments (optional)
17. [ ] Date (format: yyyy-MM-dd)
18. [ ] Release (Rel-4, Rel-5, etc.)
19. [ ] (U)SIM - ME/UE - Radio Access Network - Core Network checkboxes
20. [ ] UICC field (change to (U)SIM or ISIM)

## CR Revision Checklist

Applies when a CR is revised and re-issued as a new TDoc. The procedure
and the worked example are in `references/cr-revision.md`.

01. [ ] Document type on the portal is **CR** (not the deprecated *Draft CR*)
02. [ ] "Is revision of:" points at the TDoc number of the version being revised
03. [ ] Cover sheet downloaded from the portal template generator for the new TDoc
04. [ ] CR number unchanged (the 4-digit number of the version being revised)
05. [ ] CR revision number incremented (first revision shows `1`)
06. [ ] New TDoc number in the header
07. [ ] `revision of <previous-tdoc-nbr>` right-aligned on the second cover line
08. [ ] Date set to the date the revised version was produced
09. [ ] "Source to WG" unchanged
10. [ ] "Source to TSG" reflects the actual state (TSG identity, proposing organization(s), "WG Chairman" or "WG Secretary")
11. [ ] File name carries the revision suffix `r<revision_number>`
12. [ ] CR revision history updated, if the field is used

## Common Pitfalls

1. **Multiple Releases**: One spec may be maintained in multiple Releases
2. **Parallel CRs**: Need separate CRs for each Release with same WI code
3. **Editorial Changes**: Use "dot-one" versions, not full CRs
4. **Wrong Release**: Can't use Release 6 WI code for Release 4 spec
5. **Out-of-date Specs**: Writing CR to old version that's been updated
6. **New CR number on a revision**: A revision keeps the CR number of the version it revises
7. **Missing "revision of" marker**: The portal template does not add it - the marker has to be inserted by hand

## Best Practices

1. **Always use WI codes** from official list
2. **Check spec version** before writing CR (is it in Release 4, Release 5, or current?)
3. **Target correct Release**: Each CR should target only one Release (unless mirror CR)
4. **Use proper categories**: TEI for technical enhancements, F for correctives
5. **Mirror CR requirements**: Include mirror CRs for all affected Releases if maintaining parallel versions
6. **Document revisions**: Use CR revision history field for tracking changes
7. **Format dates correctly**: Use `yyyy-MM-DD` format
8. **Start a revision from the portal template**: Let the portal fill the cover sheet, then correct what it leaves out

## Important CR Concepts

### Mirror CRs

For specs maintained in multiple parallel Releases:

- Each Release needs its own mirror CR
- Use same WI code (Work Item code) for all mirror CRs
- Example: Spec 21.456 has mirror CRs in Release 4, Release 5, etc.

### Corrective Release 7 CRs

Special category for early LTE (Release 7) features that need to work on both Release 4 and Release 5 specs.

### Editorial Updates

CRs for pure editorial changes (no technical content) are typically implemented by MCC as "dot-one" versions (e.g., 21.456.1) rather than full CRs.
