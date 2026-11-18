# CHEM 3A — Implementation log (2026-11-17 release-gate audit)

**Branch:** `audit/2026-11-17-release-gate` in `ItsDrDan/CHEM3Atextbook` (local; **not pushed**). Base: `main` @ `686c024`.
**Writes outside the repo:** none. No LibreTexts, ADAPT, GitHub, Canvas or game changes were made.
**Session limits:** the built-in browser was signed out of LibreTexts, so the live pages could not be read, and no new PDF export or live-page check was possible.

## Commits

| Commit | What |
|---|---|
| `9596f45` | Science and answer-key fixes from the 14-chapter review (25 draft pages, 9 bank files, 7 generator scripts) + new original figure `figures/ch01/accuracy_targets.svg/.png` + `tools/fig_targets_ch01.py` |
| `1152916` | Ch 8 Experiment 8a title matches the Fall 2026 manual and Ch 10 |
| `791ca86` | `backmatter/` glossary (350 terms) and index (425 entries) data, `build_backmatter.py` → `glossary_page.html`, `index_tags.json`; audit tools (`tools/pdftext.swift`, `render.swift`, `sheet.swift`, `linkcheck.py`, `apply_repl.py`); reviewer findings in `audit/findings/` |
| `a7685da` | The seven `audit/CHEM3A-*.md` reports |

## Regression checks run after the edits

| Check | Result |
|---|---|
| `tools/check_bank_chNN.py` × 14 | `ERRORS: none` for all 14 |
| All `bank/*.json` parse | OK |
| Edited generators re-run (ch02, ch05, ch07, ch08 Try It; ch06, ch10, ch11 ADAPT) vs `bank/*.json` | Identical, so a rebuild keeps every fix |
| `bank/ch01.json` | Generator makes 65 of 99 items; the edited item (c1-072) is hand-kept, so the JSON is its source |
| Every replacement matched exactly once (or the expected twice for 2-4/2-5) | Yes (`tools/apply_repl.py` aborts otherwise) |
| New figure rendered and inspected at 1.5× | Matches the existing key; alt text describes all four targets |
| Diff size | 41 files, +73/−73 lines: small, reviewable string swaps |

## Pending writes (each needs your OK)

### 1. LibreTexts draft pages: push the repo fixes (25 pages)

Method (`CLAUDE.md`): GET the page, apply the repo's old→new strings with an exactly-once check, POST, read back, and check the render for raw `\(` or "Math Processing Error". Diff the live HTML against the repo first, so that newer live edits are never overwritten.

| Draft | Page id | Draft | Page id |
|---|---|---|---|
| 1.8 | 597681 | 8.3 | 597964 |
| 2.6 | 597867 | 8.5 | 597966 |
| 2.8 | 597869 | 8.7 | 597968 |
| 3.8 | 597885 | 8.8 | 597969 |
| 4.2 | 597892 | 9.10 | 597989 |
| 4.4 | 597894 | 11.5 | 598020 |
| 4.7 | 597897 | 11.8 | 598023 |
| 5.1 | 597906 | 12.1 | 598030 |
| 5.5 | 597910 | 12.4 | 598033 |
| 6.9 | 597930 | 12.8 | 598037 |
| 7.7 | 597950 | 13.0 (chapter page) | 597493 |
| 7.10 | 597953 | 14.6 | 598063 |
| | | 14.9 | 598065 |

### 2. Inherited Chapter 1 pages (LibreTexts only; exact edits)

| Page (id from repo notes, verify first) | Edit |
|---|---|
| 1.2.1 Scientific Notation (597593) | Example 1.2.1.3: add final answers (a) 3.87 × 10²², (b) 1.83 × 10³; (c) `4.67 \times 10^{-31}` → `4.7 \times 10^{-31}` |
| 1.3.1 Sig figs (597595) | Replace the Example 1.3.1.3 image with an upload of `figures/ch01/accuracy_targets.svg` (alt text from the SVG `aria-label`); keep the solution text |
| 1.9.1 Density as a Conversion Factor (597498) | `A mercury thermometer for measuring a patient's temperature` → `An old-style mercury thermometer (no longer used in patient care)`; table blood `1.035` → `1.06`, body fat `0.918` → `0.90`; ρ → d |
| 1.12 Measurements (Exercises) (597500) | `100 K`/`300 K` → `100. K`/`300. K`; renumber the Sig Figs question "2." → "4."; `1 ÷ 77` → `1 (exact) ÷ 77` (both items); rebuild the Unit Conversions answers and the Density and Temperature lists (remove blank lettered items, relabel "q." → 17); label the temperature items "(after Section 9.2)"; verify the "6.31 m … 2026" pole-vault claim |
| 12 inherited pages | Tags: `author@Daniel Kwasniewski`, license tags per source (NC-SA 3.0 or CK-12) — see OER doc §E |

### 3. Try It banks (GitHub Pages): `git push` of `bank/ch01, 02, 05, 07, 08.json`

### 4. ADAPT questions (live course 11836)

Update question text and feedback for c1-h19 (replacement item), c1-h21, c6-h36, c10-h29 and c11-h08 to match `bank/*_adapt.json`. Read back after each, as in the `adapt/README.md` recipe.

### 5. Back matter, archive and cover

See `CHEM3A-OER-AND-BACK-MATTER.md` §A–C.

## Known limitations and next steps

1. The live LibreTexts HTML was not compared against the repo this session. The repo matches the 11/17 PDF text on 144 of 145 pages (sampled sentences).
2. A new PDF export and a full live-page pass (phone at 375 px, keyboard, VoiceOver on one complex page per chapter) must follow the writes above.
3. Optional findings not applied: 2-6 (ADAPT c2-h04 NH₃ data) and 10-01 (rounded K values shown). Both are noted in the SCIENCE doc.
4. Rewriting the 12 inherited Ch 1 pages into the book's own format is recommended after release (P3). It would also make the whole book CC BY.

## Applied to LibreTexts, 2026-11-17 (Dr. Kwasniewski's OK: "apply the fixes to LibreTexts and ADAPT")

Every write followed the same steps: GET the page, require each old string to match exactly once (abort otherwise), POST, read back, and check the math delimiters. Page history on LibreTexts keeps every prior revision.

| What | Pages | Result |
|---|---|---|
| Repo fixes pushed (47 string replacements) | 25 pages listed in §1 above | All 25: 200, every new string present, `\(`/`\)` and `\[`/`\]` balanced. 46 matched raw; 4-3 matched after `"` → `&quot;`. Before the write, a check found **no newer live edits**: none of the new text was already present, and every old string was there once. 2.6 checked rendered: no Math Processing Error, and MathJax speech label shows "26.496 amu + 8.9578 amu = 35.45 amu". |
| 1.2.1 Example 1.2.1.3 (597593) | 1 | The source **already had** an Answer column (3.87 × 10²², 1.83 × 10³, 4.7 × 10⁻³¹). The real defect: the wide equations push that column off the PDF page (p. 26). Fixed by adding "**Answer:** …" inside each explanation cell; (c) now names the 4.67 × 10⁻³¹ calculator value before rounding to 2 sig figs. Correction to F4 in the SCIENCE doc: the answers were missing from print only. |
| 1.3.1 targets image (597595), **P0** | 1 | Uploaded `accuracy_targets.svg` as file 512947 (byte-identical to the repo). It replaces CK-12 image 114120, with new alt text and the line "(Diagram: Daniel Kwasniewski, CC BY 4.0.)". Checked rendered: loads at 470 × 520, scales to the phone width. |
| 1.9.1 (597498) | 1 | Blood 1.035 → 1.06, body fat 0.918 → 0.90 (matching 1.9); "An old-style mercury thermometer (no longer used in patient care)". ρ vs d left as is (3 LaTeX uses; P2). |
| 1.12 Measurements (Exercises) (597500) | 1 | Unit Conversions answers rebuilt as numbered answers to the odd questions (no blank items). Density and Temperature section rebuilt as Q1–Q22 with numbered answers, plus a note that Q1–8 need Section 9.2. "100. K"/"300. K". Sig Figs "2." → "4.". "1 (exact) ÷ 77". **Two more key errors found and fixed while rebuilding:** 50.0 °C → **122.0 °F** (was 122 °F, losing a sig fig) and 0 K → **−273.15 °C** (was −273 °C; the book's own value). Every answer in both sections recomputed. Pole-vault "6.31 m … 2026" claim left for your verification. |
| Glossary (597477) | 1 | Template sample row replaced by **350 entries**, each with a link to its section page. The LibreTexts glossary script stays active. Tags: `license:ccby`, `licenseversion:40`, `author@Daniel Kwasniewski`. Before upload, one definition was corrected (trigonal pyramidal: "slightly less than 109.5°"). |
| Index tags | 97 pages | **839 tags added**, with existing tags kept (each page verified). The tag "pressure units: …" was renamed "pressure units (…)" first, because a colon would turn it into a namespaced tag. |
| Inherited Ch 1 license/author tags | 12 pages | `license:mixed` → `license:ccbyncsa` + `licenseversion:30` (1.2, 1.4.1, 1.4.2, 1.12) or `license:ck12` (1.2.1, 1.2.2, 1.3.1, 1.3.2, 1.4.3, 1.9.1). Added `author@Daniel Kwasniewski` + `author@Henry Agnew`, `author@Marisa Alviar-Agnew` (+ `Sridhar Budhi` on 1.3.1; `David W. Ball` on 1.12). Parent pages 1.3 and 1.4 got only the author tag; their license was left as mixed. Rendered footers now read "shared under a CK-12 license …" and "… CC BY-NC-SA 3.0 license …". 1.2.1's footer lists "Daniel Kwasniewski" twice although the tag appears once; recheck it in the next PDF (probably a LibreTexts cache). |
| Licensing page (597480) | 1 | Added the statement "CC BY 4.0 unless otherwise noted", the 12-page exception and the note that ItsDrDan media is all rights reserved, above the dynamic licensing template. |

**Not done (need you or a separate OK):** the Retired Pages plan, the cover credit line, regenerating Detailed Licensing and the PDF in Conductor, ADAPT (waiting for sign-in), and a `git push` of the Try It banks to GitHub Pages.

## Applied to ADAPT, 2026-11-17 (course 11836)

Method (CHEM 3B recipe): PATCH `/api/questions/{id}` with the editor-shaped body, `automatically_update_revision` "1", `revision_action` "notify", and a reason for the edit. Each question had a dry run first: every old string had to be present in its exact field (stem, choice, per-choice feedback, hint) and choice 0 had to stay the key. Each was read back after saving.

| Question | ADAPT id | Assignment | Change |
|---|---|---|---|
| c1-h19 | 356156 | 224842 | **Data replaced** (193 g nugget, 20.0 → 30.0 mL; key 19.3 g/mL now 3 sig figs); new distractors 6.43, 9.65, 0.0518 g/mL with matching feedback; stale "Chapter 5" note removed |
| c1-h21 | 356158 | 224842 | 6800 g → 68,000 g in feedback |
| c1-072 | 356114 | 224842 | Feedback: all three other samples are larger |
| c2-007, c2-058, c2-063 | 356196, 356247, 356252 | 224843 | Intermediate sums and percent shown correctly |
| c5-013, c5-050 | 356517, 356554 | 224849 | "exactly 12 g" → "12 g"; 159.70 g/mol |
| c6-h36 | 356706 | 224851 | 18.14 mol |
| c7-039 | 356749 | 224852 | Balanced equation in explanation |
| c8-053 | 356875 | 224853 | Percent error defined instead of "(Chapter 1)" |
| c10-h29 | 357143 | 224855 | Distractor feedback names the actual slip |
| c11-h08 | 357236 | 224856 | Distractor feedback names the actual slip |

**Read back:** all 13 saved; feedback, stem and choices identical to what was sent. For c10-h29, ADAPT stored × and ÷ as `&times;`/`&divide;`, so the bank and generator now use the same entities. Each question kept its ID, there are no duplicates, and the pools are unchanged (224842: 139, 224843: 104, 224849: 100, 224851: 106, 224852: 112, 224853: 108, 224855: 112, 224856: 114).

**Repo correction found during this step:** the 2026-11-17 bank fix for c1-h19 had changed only the stem, leaving 9.65 g / 0.5 mL choices and feedback. `bank/ch01_adapt.json` now has the full replacement; the one-line diff keeps the file's format, and `check_bank_ch01` passes. The Try It widget does not use the ADAPT bank, so no student-facing practice showed the half-fixed item.

## Retest and follow-up fix, Full (20).pdf (2026-11-17)

The retest is logged in `CHEM3A-PDF-AND-WEB-QA.md`. One defect from this session's rebuild of 1.12: answer labels 1(d) and 3(d) printed "(undefined)". Both were fixed on page 597500 (2 occurrences, read back). No other "undefined", NaN (except NaNO₃ and other formulas), placeholder or raw-TeX text appears in pp. 14–850.

## Retired Pages hidden, 2026-11-17 (Dr. Kwasniewski: "Hide Retired Pages")

- **Why a move instead of only Private:** the Workbench draft is already closed to anonymous readers (403), so restricting the archive would not change what the PDF compiler includes. The plan's reversible fallback was used instead.
- **Done:** `POST pages/597819/move?to=User:2797c837-8938-496d-8fee-2095d3d22cc5/CHEM_3A_Retired_Pages_2026-11` moved **170 pages** (the holder + 169), and every page ID is unchanged. Then `PUT security?cascade=delta` set restriction **Private** with a Manager grant to user 31641 (Dr. Kwasniewski).
- **Verified:** the book's top level now ends at Back Matter (16 entries: Front Matter, Ch 1–14, Back Matter). A signed-out request to the holder and 3 sampled children returns 403; Dr. Kwasniewski still reads them (200). The holder notice now gives the location and the restore steps.
- **Undo:** move 597819 back under `Workbench/Introductory_Chemistry_Atoms_First_for_FCC_-_Revision_Draft_DTvJm7TcCY` (old paths keep redirects, so pick the same path or a new one). Nothing was deleted.
- **To confirm:** the next PDF compile should end at about page 873 (14.10 + Index, Glossary, Detailed Licensing), with no "Retired Pages" in the outline.

## Cover credit, 2026-11-17 (Dr. Kwasniewski: "Kwasniewski, adapted Yates")

- **Title page (597474, PDF p. 2):** the empty `pdf-title-author` line now reads "Daniel Kwasniewski / Adapted from *Introductory Chemistry, Atoms First for FCC*, compiled by Seth Yates" (read back).
- **Cover (PDF p. 1) "Unknown":** not fixable from this account. The cover author comes from the site's author records (`Template:Custom/Data/Authors`, read-only for faculty), which have no entry for Kwasniewski or Yates, and the root page has no `authorname:` tag. A ready-to-send request is in `audit/LIBRETEXTS-COVER-AUTHOR-REQUEST.md`. Conductor's project settings were not checked, because Conductor needs a separate LibreOne sign-in.
- **Conductor checked (signed in, 2026-11-17):** project DTvJm7TcCY (`GET /api/v1/project`) has no author fields. It holds `libreCoverID` 597470, leads [Daniel Kwasniewski], visibility private, `hasCommonsBook` false, `bookData` empty. So nothing in Conductor sets the cover author; the LibreTexts support request is the only route.
