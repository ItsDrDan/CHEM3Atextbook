# CHEM 3A Atoms First OER — Release gate (2026-11-17)

## Verdict: **READY AFTER SPECIFIC FIXES**

**The Nov 17 export as it stands is not ready to hand to students.** It carries a wrong worked-example key in Chapter 1, a 625-page archive, placeholder back matter and an "Unknown" cover. The instructional core, Chapters 2–14 and the new Chapter 1 pages, **is scientifically sound**: seven reviewers recomputed every number and read all 1,562 bank items, and they found **no wrong answer key in Chapters 2–14**. Every correction is already made in the repo or written out as an exact edit. What remains is applying them on LibreTexts and ADAPT with your approval, then one fresh PDF check.

Evidence: [Science](CHEM3A-SCIENCE-AND-ANSWERS.md) · [Matrix](CHEM3A-14-CHAPTER-MATRIX.md) · [PDF/Web QA](CHEM3A-PDF-AND-WEB-QA.md) · [OER/Back matter](CHEM3A-OER-AND-BACK-MATTER.md) · [Lab sync](CHEM3A-LAB-AND-REFERENCE-SHEET-SYNC.md) · [Implementation log](CHEM3A-IMPLEMENTATION-LOG.md)

## Blocking (must be done before students get the book)

| # | Sev | Item | State |
|---|---|---|---|
| B1 | P0 | 1.3.1 Example 1.3.1.3: target image contradicts the "precise but inaccurate" key | **Done 2026-11-17** (new figure live) |
| B2 | P1 | 1.2.1 Example 1.2.1.3: Answer column clipped off the PDF page | **Done 2026-11-17** |
| B3 | P1 | 1.12 exercises: broken answer lists; "100 K"/"300 K" keys break the course sig-fig rule | **Done 2026-11-17** (+ 122.0 °F and −273.15 °C key fixes) |
| B4 | P1 | 25 book pages with fixes (incl. 12.4 garbled tip, 14.36 backward K–Ar dating, 8.5 undefined percent error) | **Done 2026-11-17** |
| B5 | P1 | Retired Pages (42% of the PDF) in the student TOC and export; un-prefixed archive titles | Reversible plan (back up → rename → Private → recompile); **your approval** |
| B6 | P1 | Glossary and Index print placeholders | **Done 2026-11-17** (350 glossary entries; 839 index tags on 97 pages); confirm in next PDF |
| B7 | P1 | Cover author "Unknown"; Detailed Licensing empty | Needs your credit line; then fix tags and rerun |
| B8 | P1 | 12 inherited Ch 1 pages print "a license … Staff": NC/NC-SA/CK-12 terms not shown, your curation uncredited | **Done 2026-11-17** (tags + Licensing-page statement) |
| B9 | P1 | ADAPT c1-h19 (1-sig-fig volume keyed to 3), c1-h21 feedback | Fixed in bank; update ADAPT |

## Nonblocking (fix when practical)

- **Printed answers.** In the PDF, Practice Problem answers print directly under each problem (P2, owner decision; see QA Q13).
- **Lab numbers.** Exp 3a and 11a are cited but have no Fall 2026 write-up, although both are COR lab topics (Lab sync L1, L2).
- **About 40 P2 wording and display fixes.** All are applied in the repo; 2 optional ones were not applied.
- **External citations.** 3 citation links blocked automated checks; a reviewer could not confirm 2 cited figures offline.
- **Video timestamp links.** Links whose text is only a time ("8:30") are weak for screen-reader link lists.
- **Try It privacy note.** The widget sends anonymous per-question stats (Do Not Track honored; no names). The page footer says only that progress is saved in the browser. Consider one line of disclosure: "Anonymous answer statistics help improve the questions."

## Gate B: student walkthrough (from the PDF and repo; live pages not tested)

| Path | Finding |
|---|---|
| A. Math-anxious allied-health student | New pages model every conversion with labeled factors, a "Check", and Professor Tips for the TI-36X Pro. **Weakest point: the 12 inherited Ch 1 measurement pages**, where this student starts. They use a different format, have no Common Mistakes, and hold every remaining Ch 1 defect. Rewriting them is the highest-value improvement after release. |
| B. Studying before an exam | Every chapter has a Chapter Guide (Key Ideas, video moments, worked examples), a Practice Problems page with reasoning in every answer, a mixed Try It set and a Final Boss link. Reference-sheet conventions (yellow/green) are named where used. Once B6 is applied, the glossary and index make terms findable. |
| C. Recovering from a misconception | Every Try It and ADAPT choice has its own feedback; 7 explanations that named the wrong slip were corrected (11.28, 11.37, 11.40, 9.47, c10-h29, c11-h08, c7-039). Solubility, pH and gas-law feedback reads correctly. |
| D. Limited time / phone | Sections are short, with 3–5-question Try It boxes and no login. Phone fixes (data-th table labels, responsive video iframes, scrolling equations) are in the source. **Not re-tested on a phone this session.** |
| E. Assistive technology | Static checks pass: 89/89 images have meaningful alt text, 301/301 iframes are titled, 114/114 tables have header cells, headings never skip levels, every game has a new-tab link and a statement of what it is. Not tested: screen reader, keyboard order, MathJax speech on the web. In the **PDF**, math is drawn as vector paths, so selectable text and PDF screen reading lose exponents and cross-reference numbers (platform behavior). |
| Instructor adoption | COR map, scope decisions, Going Further labels, conventions and licensing are documented. There is no "report an error" route in the book; consider adding an errata or contact line to the front matter. |

## Owner decisions needed

1. Approve the archive plan (B5): back up, rename, set Private, recompile. Permanent deletion only on a later, separate approval.
2. Cover and credit line (B7), including whether to credit Seth Yates's original compilation.
3. Approve the LibreTexts writes (B1–B4, B6, B8), the ADAPT updates (B9) and a `git push` of the Try It banks.
4. Printed answers placement (QA Q13).
5. Lab numbers for Exp 3a and 11a (Lab sync L1, L2).
