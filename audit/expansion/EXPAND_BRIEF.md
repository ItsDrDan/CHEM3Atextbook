# Brief: expand a chapter from Dr. Dan's lectures and videos (writers)

You are expanding one or more chapters of Dr. Dan's (Daniel Kwasniewski, Fresno City College) CHEM 3A open textbook,
the way Chapter 5 was already expanded. You WRITE the content into the repo draft files. You do NOT publish, commit,
push, or touch LibreTexts, ADAPT, the Try It banks, or any file outside your chapter folder(s).

REPO = /Users/dan/Desktop/Study Games/github/CHEM3Atextbook
SCRATCH = /private/tmp/claude-501/-Users-dan-Desktop-Study-Games/902fb8b8-e606-48c8-860b-c64087a289e1/scratchpad

## Read first
1. `REPO/CLAUDE.md`: especially "Chemistry conventions", "Scope decisions", "CHEM 3A scope notes", exam-style conventions,
   and the style/attribution rules. These override everything else.
2. Your chapter's gap analysis: `REPO/audit/expansion/gaps/chNN.md`. This is your work list: do all High items and as many
   Medium items as fit well; Low items only if they are short and clearly useful. Honor its "Out of scope / skip" list and
   its list of video misstatements (never repeat a wrong number from a video; add the caption "The video rounds some
   values while writing; use your yellow-sheet values as printed." when you link a segment with rounded numbers).
3. The model: Chapter 5 after expansion. See the diff: `git -C REPO show 30c5a91 -- drafts/ch05` and read
   `REPO/drafts/ch05/5.3_mass_moles_particles.html` and `5.5_putting_it_together.html` fully. Copy its HTML patterns
   exactly (box-objectives, box-example with Problem/Solution/Check, box-note Professor Tip, box-exercise with
   <details><summary>Answer</summary>, centered MathJax lines with `style="text-align:center;overflow-x:auto;overflow-y:hidden;"`,
   tables with class `mt-responsive-table`, `data-th` on every td, `<th scope="col">`, a caption, and the
   `<style type="text/css">@media (max-width: 37.49em) ...</style>` line right before each new table).
4. Sources: lecture slide text `SCRATCH/expand/slides/*.txt` ("--- slide N ---"), video transcripts
   `SCRATCH/expand/videos/<id>.txt` (`[m:ss]` stamps; index `INDEX.tsv`). Read the source for each item before writing it,
   so the explanation, analogy, memory aid or procedure is HIS (his words may be quoted briefly; mostly paraphrase).

## What to write
- Deepen existing sections in place: his explanations, analogies, memory aids, procedures, misconceptions, clinical/Valley
  ties he uses, calculator tips, and new worked examples of the types he teaches. Keep everything already on the page
  unless it is wrong (then fix it and note it). Keep each page's existing order: objectives, body, tips/connections,
  Video Lesson, Try It, Common Mistakes, Summary, Exercises, Attribution. Update Learning Objectives, Common Mistakes,
  Summary and the chapter guide's Key Ideas / video table so they match the new content. Add 1–3 exercises per page
  for new skills, and add new practice problems to the chapter's Practice Problems page in a final group headed
  like "N.x Putting It Together: More Problems" (or similar), numbered after the last existing problem, in the same
  answer format (MC answers explain every wrong choice).
- New sections: prefer a new `<h2>`/`<h3>` inside an existing page. Create a NEW PAGE only for a High-priority new section
  in the gap file that is clearly bigger than ~900 words. At most ONE new page per chapter. Name the file
  `N.M_slug.html` placed before the chapter guide, and RENAME the following files with `git mv` (guide, problems,
  games, going further) so numbering stays consecutive, and fix every "N.x" reference inside your chapter's files
  (intro "In This Chapter" list, guide "Practice" line, cross-references). Do not edit other chapters; instead list any
  cross-chapter reference that needs updating (grep `REPO/drafts` for "Section N.x").
- Video links: `https://youtu.be/<id>?t=<seconds>` with the m:ss text, and only to moments you have checked in the
  transcript. Embeds use the existing iframe pattern (`youtube.com/embed/<id>?start=<s>&amp;rel=0`, `loading="lazy"`,
  a title). Never cite the misstatement moments in the gap file.
- Try It boxes: reuse only topic keys that exist in `REPO/bank/chNN.json` (look at existing boxes for the format). No new banks.
- Exams, Skill Checks, homework, and Kahoot/exam-review items: NEVER copy. Use the idea with new numbers and substances.
- Stay within the COR and CLAUDE.md scope. Items the gap file flags as "decision for Dr. Dan" or beyond scope: do NOT add;
  list them in your report.
- Chapter 1: the inherited pages 1.2–1.4.3, 1.9.1, 1.12 exist only on LibreTexts (not in drafts) and are not yours to
  rewrite. You may create the new pages the gap file proposes (e.g. reading measuring tools, word problems/dosage,
  percents as conversion factors) as new draft files named for their intended place (e.g. `1.3.3_reading_tools.html`),
  and deepen the drafted pages (1.0, 1.1, 1.5–1.11, 1.13). Do not renumber Chapter 1 pages.

## Accuracy (most important)
- Every number you write: compute it with python3. Atomic masses exactly as in `REPO/tools/yellow_sheet_masses.json`
  (strings keep printed decimals); molar-mass sums rounded to the fewest decimal places (addition rule); answers to the
  sig figs of the measured givens; trailing zeros without a decimal point are NOT significant. Follow every other
  convention in CLAUDE.md (constants, ΔEN cutoffs, STP, R, Kw, pH sig figs, etc.).
- Clinical examples carry "(Context only; …)" disclaimers as the existing pages do. No dosing advice.
- After writing, run `python3 REPO/tools/check_fragment.py <file>` on every changed file (must report no errors), check
  that every `\(` has a matching `\)`, and that `<details>`, `<div>`, `<table>` are balanced.

## Report (your final message)
Per chapter: files changed/added/renamed; words before → after for the section pages; list of additions (one line each
with its source); new practice problem numbers; any new page and the required renumbering; cross-chapter references to
fix; new glossary/index terms worth adding (term + section); items skipped for Dr. Dan's decision; anything you are
unsure of. Do not commit.
