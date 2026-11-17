# CHEM 3A — Implementation log (2026-11-17 release-gate audit)

**Branch:** `audit/2026-11-17-release-gate` in `ItsDrDan/CHEM3Atextbook` (local; **not pushed**). Base: `main` @ `686c024`.
**Writes outside the repo:** none. No LibreTexts, ADAPT, GitHub, Canvas or game changes were made.
**Session limits:** the built-in browser was signed out of LibreTexts, so the live pages could not be read, and no new PDF export or live-page check was possible.

## Commits

| Commit | What |
|---|---|
| `9596f45` | Science and answer-key fixes from the 14-chapter review (25 draft pages, 9 bank files, 7 generator scripts) + new original figure `figures/ch01/accuracy_targets.svg/.png` + `tools/fig_targets_ch01.py` |
| next | Ch 8 Experiment 8a title matches the Fall 2026 manual and Ch 10 |
| next | `backmatter/` glossary (350 terms) and index (425 entries) data, `build_backmatter.py` → `glossary_page.html`, `index_tags.json`; audit tools (`tools/pdftext.swift`, `render.swift`, `sheet.swift`, `linkcheck.py`, `apply_repl.py`); reviewer findings in `audit/findings/` |
| next | The seven `audit/CHEM3A-*.md` reports |

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
