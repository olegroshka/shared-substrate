# Task: lay the article draft into LinkedIn (DRAFT ONLY — do not publish)

## Context
Repo: `C:\Users\olegr\PycharmProjects\shared-substrate`. A finished LinkedIn
article draft exists at
`article/human-edge-becomes-the-job-v2-linkedin-paste.md`. It is
self-contained: the HTML comment at the top lists the seven image files
(absolute Windows paths) in insertion order; the body marks each insertion
point with a `⟦IMAGE n — filename⟧` line followed by its italic caption.
Chrome is running and logged in to LinkedIn.

## Do this
1. Connect to Chrome. Find the LinkedIn tab (or open linkedin.com) and go to
   the article editor: **Write article** (via the post box on the feed).
2. Title field: `The Human Edge Becomes the Job: On Moving Up the
   Abstraction Stack` (plain text, no markdown).
3. Read the paste file, then lay the body into the editor **section by
   section**, translating markdown to editor formatting — markdown markers
   must never appear literally in the draft:
   - `## Heading` → the editor's header/subtitle style
   - `**bold**` → bold via the toolbar (strip the asterisks)
   - `*italic*` → italics (strip the asterisks)
   - the em-dashes, quotes and the bulleted list are plain text — keep as-is
   - the final paragraph's two links must be real hyperlinks:
     `https://doi.org/10.2139/ssrn.7218019` and
     `https://github.com/olegroshka/shared-substrate`
4. At each `⟦IMAGE n⟧` marker: insert the image file (paths in the file's
   header comment) via the editor's image control, put the caption text
   (the italic line under the marker) into LinkedIn's caption field, and do
   NOT reproduce the marker line itself.
5. LinkedIn autosaves articles as drafts — confirm the draft state. **Never
   click Publish, Next, or Post. Never share anything to the feed.**

## Verify before finishing
- All 7 images present, in order, each with its caption.
- No literal `**`, `##`, `⟦`, or `*` markers anywhere in the draft.
- The two closing links are clickable hyperlinks.
- Screenshot the top and the bottom of the draft as evidence.

## Constraints
- Draft only — publishing is done by Oleg after review, not by you.
- Do not edit any repo files; the paste file is read-only input.
- If login is expired, the editor misbehaves, or images fail to upload:
  stop, leave what is done in the autosaved draft, and report exactly what
  remains.

## Report back
What was laid in, what was verified (including the screenshots), and
anything left for manual finishing.
