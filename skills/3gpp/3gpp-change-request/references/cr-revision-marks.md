# Revision Marks in a CR: Authorship and Review

How the revision marks of a CR body are attributed while a CR moves from
meeting to meeting, and how drafted changes are handed to the delegate for
review. These are working conventions for keeping the agreed state readable,
not rules of the 3GPP Working Procedures. The XML patterns (revision markup,
renaming authors, verification in Word) are in `sdo-docx`.

## Agreed state under the meeting name

A CR revised for the next meeting carries the revision marks of earlier
versions. Marks that reflect the state agreed at a meeting are attributed to
that meeting, so that new proposals stand out:

| Revision marks | Author |
|---|---|
| Dated up to the meeting at which they were agreed | `<WG>#<meeting>`, e.g. `SA4#136` |
| Added since that meeting | the delegate, as the user name set in Word (`Surname, Given name`) |

Rename by date: every revision element with a date before the cut-off gets the
meeting name; comments keep their authors.

## Drafted changes awaiting review

When an assistant drafts changes in a CR:

1. Mark its changes with its own author name (for example `Claude`), so the
   delegate can review exactly those changes.
2. Keep the changes minimal (word swaps, not rewritten sentences) and ask
   before adding clarifications that do not fix an error.
3. When a drafted change is superseded during review, remove the drafted
   revision and apply the new one to the original text - never a change on top
   of a change.
4. After review, rename the assistant's author to the delegate's name,
   including comment authors and initials. No assistant author may remain in
   the uploaded document.

## Maintenance CR versus new work

A CR revised from meeting to meeting carries corrections of the agreed
content. New technical proposals (new test methods, new requirements) go into
a separate contribution, so that the agreed CR is not blocked by them.

## Related

- `references/cr-revision.md` - revising a CR: portal procedure, cover sheet,
  "revision of" marker
- `sdo-docx` - revision mark XML, renaming authors, verification in Word
