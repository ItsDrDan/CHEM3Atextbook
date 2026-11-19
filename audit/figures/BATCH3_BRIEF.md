# Brief: OpenStax figure batch 3 (Chapters 3–9 and 13)

Goal: add 3–5 high-value figures per chapter from **OpenStax *Chemistry 2e*, the LibreTexts copy only**
(`https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)/...`; pages tagged CC BY 4.0).
Never use openstax.org (now NC-SA). REPO = `/Users/dan/Desktop/Study Games/github/CHEM3Atextbook`.

## Read first
- `CLAUDE.md` (scope decisions, chemistry conventions, chapter content), especially the chapter notes for your chapters.
- `audit/expansion/REMIX_COMPARISON.md` section 3 (candidate figures per chapter).
- `tools/add_openstax_figs_2.py` (the last batch: tuple format, alt/caption/credit style, lead-ins). Match its style.
- Your chapters' section pages in `drafts/chNN/` (what each section teaches, which figures it already has: `grep -n '<figure' drafts/chNN/*.html`).

## Choosing figures
- Pick figures that show something our pages only describe in words: real photos of chemistry (precipitates, reactions,
  samples), clear diagrams, data graphs that support the skill taught. Allied-health and everyday ties are a plus.
- Stay inside CHEM 3A scope (CLAUDE.md): e.g. no photoelectric effect, no ICE tables, no Henderson–Hasselbalch, no
  quantum numbers, no pH meters. Do not duplicate a figure we already have (our own SVG diagrams count).
- Check every figure's credit line on the OpenStax page. Use it only if it is CC BY (OpenStax's own art, or "modification of
  work by …" credits). Skip anything marked copyright / all rights reserved / used by permission, and skip figures that are
  mostly a chemical-structure table students do not need.
- LibreTexts puts an Introduction page first, so OpenStax section N.k is LibreTexts page N.(k+1) (e.g. OpenStax 4.2 =
  `04%3A_.../4.03%3A_...`). Credits cite the **OpenStax** section number (4.2) and link the LibreTexts page path.

## For each chosen figure
1. Find the full-size image URL on the LibreTexts page (the `<img>` src under `/@api/deki/files/...`).
2. Download it into `figures/openstax/` named `os_<OpenStax section with dash>_<short_slug>.jpg` (or `.png` for line art),
   e.g. `os_4-2_pbi2_precipitate.jpg`. Do not overwrite existing files. Compress photos to about 100 KB or less with
   `sips` (max dimension 1200 px; JPEG quality ~70); keep line-art PNGs sharp (resize to ≤1200 px wide only).
3. **Look at the image yourself (Read the file)** and write:
   - `alt`: plain text only (no `<` or `>`; numbers and formulas in words or plain characters like H2O → "H2O" is fine,
     but no tags), describing what is actually visible, specific enough to be useful to a blind student (labels, values,
     colors that carry meaning). 1–4 sentences; long data figures may be longer.
   - `caption`: our own words, 1–2 sentences, tied to what the section teaches. HTML entities allowed (&ndash; &rsquo;
     &rarr; &deg;), and `<sub>`/`<sup>`/`<i>` allowed in the caption only.
   - `credit_section` (e.g. "4.2"), `credit_path` (LibreTexts path after `Chemistry_2e_(OpenStax)/`), `credit_extra`
     (photo credits exactly as OpenStax gives them, e.g. "photo a: modification of work by Jeff Turner"; "" if none).
4. Placement: `page` (e.g. `ch07/7.5_precipitation.html`), `key` = a short string that occurs **exactly once** in that
   page's raw HTML (check with grep -c), and `where` = `after` (after the paragraph or list containing key), `afterbox`
   (after the box containing key) or `afterfig` (after the figure containing key). Put the figure right after the text
   it illustrates, not inside an Example/Exercise box, not between a box title and its body.
5. `lead`: if the page text does not already set the figure up, a 1–3 sentence `<p>…</p>` lead-in in the book's plain
   voice (CHEM 3A level, short sentences, no "Dr. Dan"); otherwise "".

## Output
Write `audit/figures/batch3_<your chapters>.json`: a list of objects
`{"page","key","where","img","lead","alt","caption","credit_section","credit_path","credit_extra","why"}` in page order
(`why` = one line on what it adds). **Do not edit any draft HTML or other repo files** besides the JSON and the new image
files. Report: the figures chosen per chapter (and anything you considered but skipped, with the reason, especially
license problems).
