# Tracked Changes: Advanced Patterns

Patterns beyond the basic insert/delete markup of
`references/operations/tracked-changes.md`: minimal
edits, text split across runs, edits inside another author's revision, fields,
equations, author renaming and verification. All patterns were checked by
accepting and rejecting the result in Word.

## Keep visible changes minimal

- Change only the words that must change. A sign flip is two word swaps
  (`left` -> `right`, `right` -> `left`), not a deleted and retyped sentence.
- Do not stack changes on changes. When your own, not yet agreed revision is
  superseded, remove it (reject it) and apply the new edit to the original
  text, instead of deleting your own insertion as a further revision.
- Clarifying additions (new notes, definitions, explanatory clauses) are
  proposals: ask before inserting them.

## Text split across runs

Word splits running text at arbitrary points (spell check, rsids, earlier
edits), so a phrase is often spread over several `<w:r>` elements.

1. Concatenate the `<w:t>` text of the live runs (skip runs inside `<w:del>`).
2. Find the search key there; the context before and after the replaced part
   may span runs.
3. Require the replaced part itself to lie inside one run, then split that run
   into before / deleted / inserted / after, copying its `<w:rPr>` to every
   piece.
4. When swapping two words in one sentence, replace the later word first;
   otherwise the second search can hit the word just inserted.

## Edits inside another author's insertion

Text inside `<w:ins w:author="X">` is X's proposal. To change it as a
different author:

```xml
<w:ins w:id="10" w:author="X" w:date="...">
  <w:r><w:t xml:space="preserve">difference between </w:t></w:r>
  <w:del w:id="20" w:author="Y" w:date="...">
    <w:r><w:delText>right</w:delText></w:r>
  </w:del>
</w:ins>
<w:ins w:id="21" w:author="Y" w:date="...">
  <w:r><w:t>left</w:t></w:r>
</w:ins>
<w:ins w:id="22" w:author="X" w:date="...">
  <w:r><w:t xml:space="preserve"> and left levels</w:t></w:r>
</w:ins>
```

- A deletion of X's text is a `<w:del>` nested inside X's `<w:ins>`.
- An insertion closes X's `<w:ins>`, adds the new `<w:ins>`, and reopens X's
  insertion with a new `w:id` (insertions do not nest).

## Fields as tracked changes

Insert a complete field (begin, instruction, separate, cached result, end)
inside one `<w:ins>`, and delete the text it replaces with `<w:del>`:

```xml
<w:del w:id="30" w:author="Y" w:date="..."><w:r><w:delText xml:space="preserve">Table 8</w:delText></w:r></w:del>
<w:ins w:id="31" w:author="Y" w:date="...">
  <w:r><w:fldChar w:fldCharType="begin"/></w:r>
  <w:r><w:instrText xml:space="preserve"> REF TAB_RCV_ILD_ITD \h </w:instrText></w:r>
  <w:r><w:fldChar w:fldCharType="separate"/></w:r>
  <w:r><w:t>Table 7</w:t></w:r>
  <w:r><w:fldChar w:fldCharType="end"/></w:r>
</w:ins>
```

The cached result must match what the bookmark contains (here the bookmark
spans `Table 7`), so the text is right before Word updates the field.

## Equations (OMML)

- **Changing a math run:** wrap the old `<m:r>` in `<w:del>` and the new one in
  `<w:ins>`. Deleted math keeps `<m:t>`; there is no math `delText`.
- **Inserting or deleting a whole equation object:** mark every `<m:r>` and
  also every `<m:ctrlPr>`, so rejecting leaves no empty placeholder boxes:

  ```xml
  <m:ctrlPr><w:ins w:id="40" w:author="Y" w:date="..."><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr></w:ins></m:ctrlPr>
  ```

- **After Word saves the file**, it rewrites math revisions into its own form,
  with the marker inside the run:
  `<m:r><w:del ...><w:rPr>...</w:rPr><m:t>x</m:t></w:del></m:r>`.
  `mise x github:iOfficeAI/OfficeCLI -- officecli validate` reports this form
  as a schema error. It is Word's native output: compare with the validation
  result of the untouched original before treating it as a defect.

## Revision ids after a Word save

Word renumbers `w:id` values when it saves. Determine the maximum id of the
current file before every batch of new revisions, and start above it.

## Renaming revision authors

Rewrite the `w:author` attribute of the revision elements (`w:ins`, `w:del`,
`w:moveFrom`, `w:moveTo`, `w:rPrChange`, `w:pPrChange`, cell revisions) in
`word/document.xml`, headers, footers and notes, filtered by author and, if
needed, by `w:date`. Comments live in `word/comments.xml`: rename `w:author`
and adapt `w:initials`. Afterwards search every part of the package for the old
name; it must not occur anywhere.

## Removing your own revisions

To withdraw your own revisions without leaving traces, reject them rather than
deleting them as new revisions. In Word automation, rejecting changes the
`Revisions` collection: restart the iteration after every `Reject()` instead
of iterating over a stale index.

## Verification in Word

Check every batch of revisions in Word, on copies of the file:

- **Accept all** of your revisions: the text must read as intended.
- **Reject all** of your revisions: the text must equal the original.
- **Update all fields** and count results containing `Error`: none.
- Export the changed pages to PDF to check equations and figures visually.

On Windows, Word automation (`Word.Application` via COM) runs these checks
without opening a window.
