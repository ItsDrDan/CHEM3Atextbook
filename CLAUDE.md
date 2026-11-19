# CHEM3Atextbook: CHEM 3A LibreTexts overhaul

Read this whole file at the start of every session. It holds the decisions already made; do not re-ask them.

## What this project is

A major overhaul of the free LibreTexts textbook for **CHEM 3A (Introductory General Chemistry) at Fresno City College**, built the same way as Dr. Dan's CHEM 3B book (repo `ItsDrDan/textbook`). Dr. Dan (Daniel Kwasniewski) leads it. **Multiple FCC faculty will use the book**, so:

- **Chapter order and scope follow the CHEM 3A COR (course outline of record), not Dr. Dan's syllabus.** Never add topics beyond the COR or drop below it.
- No "Dr. Dan says" anywhere in the text. Teaching-voice asides are **"Professor Tip"** boxes.

**Students:** about 75% allied health (nursing, dental hygiene, radiologic technology, respiratory therapy). The rest are biology, chemistry and engineering students. Many are from California's Central Valley.

## Where things are

| Thing | Location |
|---|---|
| **Live book (do not edit)** | "Introductory Chemistry, Atoms First for FCC": https://chem.libretexts.org/Courses/Fresno_City_College/Introductory_Chemistry_Atoms_First_for_FCC. A co-worker's book that students are using now. |
| **Draft book (we edit this)** | Conductor project "Introductory Chemistry Atoms First for FCC - Revision Draft", project ID `DTvJm7TcCY` (https://commons.libretexts.org/projects/DTvJm7TcCY). Workbench: https://chem.libretexts.org/Workbench/Introductory_Chemistry_Atoms_First_for_FCC_-_Revision_Draft_DTvJm7TcCY |
| **Plan for the draft** | Once the draft is approved, it moves into the live book during the term gap. If it is not approved, Dr. Dan uses the draft as his own book. |
| **Chapter 1 audit tracker** | https://claude.ai/artifact/Q4kDNVZkdMhjkA1ztvTueS (Sheets: "Ch 1 Audit" and "Chapter Progress") |
| **CHEM 3B model repo** | `ItsDrDan/textbook`. Read its README, `tools/AUTHOR_BRIEF.md`, `tools/REVIEW_BRIEF.md` and `tools/COR_outline.md` before building anything. |
| **Course files** | `~/Desktop/FCC Teaching/` (CHEM 3A subfolders: lecture slides, worksheets, homework, study guides, exams, lab manual) |
| **YouTube transcripts** | `~/Desktop/Study Games/github/games/data/transcripts.json` (all ItsDrDan videos; the old Subtitles folder is gone) |
| **Test banks and textbooks** | `~/Desktop/Study Games/CHEM 3A Resources/` |
| **Question banks** | `ItsDrDan/questionbank` (shared bank), `ItsDrDan/finalexam` (Final Boss, including CHEM 3A) |
| **Games hub** | https://itsdrdan.github.io/games (repos `ItsDrDan/<game>`) |

### Draft book status (Nov 14, 2026)

- **Structure.** All 14 chapters were remixed into the draft, chapter numbering matches the live book, and the stray "_xx_ delete-test" page was left out. Chapters: 1 Basics of Measurement, 2 Atomic Structure, 3 Light, Electrons, and the Periodic Table, 4 Compounds and Chemical Bonds, 5 The Mole and Chemical Formulas, 6 Lewis Structures, Shapes, and Intermolecular Forces, 7 Solids, Liquids, and Phase Changes, 8 Gases, 9 Aqueous Solutions, 10 Chemical Reactions, 11 Stoichiometry, 12 Acids and Bases, 13 Chemical Equilibrium, 14 Radioactivity and Nuclear Chemistry. Chapter order will change to follow the COR.
- **Transclusion.** The Remixer transcludes by default: each page is a live mirror of the live book and cannot be edited until it is **forked**.
  - **Chapter 1 is fully forked and audited**, and 57 of its 62 issues are fixed.
  - **Chapters 2–14 are still transcluded.** Dr. Dan chose to fork chapter by chapter as each one is revised. Pages that are rebuilt from scratch can simply replace the transcluded ones.
- **Old Chapter 1 (now Chapter 5, "Measurement and the Mole") page IDs** (titles below are the old numbers; now 5.1–5.4 and 9.2 for Temperature, 5.10 for Exercises):

  | Page | ID |
  |---|---|
  | Chapter 1 | 597481 |
  | 1.1 | 597495 |
  | 1.1.1 | 597593 |
  | 1.1.2 | 597594 |
  | 1.2 | 597496 |
  | 1.2.1 | 597595 |
  | 1.2.2 | 597596 |
  | 1.3 | 597497 |
  | 1.3.1 | 597597 |
  | 1.3.2 | 597598 |
  | 1.3.3 | 597599 |
  | 1.4 | 597498 |
  | 1.5 | 597499 |
  | 1.6 Exercises | 597500 |

- **Draft reordered to COR order 2026-11-14** (with his go-ahead): 14 chapters, blueprint titles, sections renumbered, pages moved between chapters per the blueprint, superseded pages moved to a "Retired Pages" holder (597819) at the end. **2026-11-17: holder + 169 subpages moved out of the book to `User:2797c837-8938-496d-8fee-2095d3d22cc5/CHEM_3A_Retired_Pages_2026-11` and set Private (ids unchanged); restore by moving 597819 back under the book.** Full map and undo notes: `tools/REORDER_2026-11-14.md`. Page ids did not change. New Chapter 1 path is now `.../01:_Matter_and_the_Scientific_Method`. Source of truth from now on is LibreTexts; pull before re-editing. Tags: `article:topic(-guide)`, `author@Daniel Kwasniewski`, `authorname:dkwasniewski`, `license:ccby`, `licenseversion:40`, `showtoc:no`.

  | Page | ID |
  |---|---|
  | 1: Matter and the Scientific Method | 597676 |
  | 1.1 The Scientific Method | 597677 |
  | 1.2 Classifying Matter | 597678 |
  | 1.3 States of Matter | 597679 |
  | 1.4 Electric Charge | 597680 |
  | 1.5 Physical and Chemical Properties and Changes | 597681 |
  | 1.6 Density | 597682 |
  | 1.7 Chapter Guide | 597683 |
  | 1.8 Practice Problems | 597684 |
  | 1.9 Practice Games | 597685 |

- **Chapter 1 items still open:**
  - New Exercise 1 image for 1.2.1 (it duplicates Example 1b).
  - New accuracy/precision target image for 1.2.1 (target "a" does not clearly show "precise but inaccurate").
  - Temperature problems in 1.5 and 1.6 that use values like 5800 K or 300 K: rewrite the values so their precision is clear, and re-key the answers.
  - Optional health-careers replacement for the mercury-thermometer density example in 1.4.
  - Question-bank rebuild for 1.6.

- **Chapter 2 (2026-11-14):** intro on chapter page 597482; 2.1–2.9 = 597862–597870. Old transcluded pages 597502–597510 retired to 597819 as "Old 2.x …".
- **Chapter 3 (2026-11-14):** intro on chapter page 597483; 3.1–3.9 = 597878–597886. Old transcluded pages 597511–597517 (with subpages) retired to 597819 as "Old 3.x …". ADAPT assignment 224844, folder 15020.
- **Chapter 4 (2026-11-14):** intro on chapter page 597484; 4.1–4.9 = 597891–597899 (4.5 retitled "Naming Acids and Bases" 2026-11-17). Old transcluded pages 597520, 597522–597524 (with subpages) retired to 597819 as "Old 4.x …". ADAPT assignment 224846, folder 15021. Naming follows his slides: fixed-charge metals = groups 1–2, Al, Zn, Ag; Stock names plus older -ous/-ic names; "bi-" names; polyatomic list = green sheet.
- **Chapter 5 (2026-11-14):** "The Mole": intro on chapter page 597481 (its old measurement intro saved in drafts/archive/); 5.1–5.4 = 597906–597909; **5.5 Putting It Together: Multi-Step Mole Problems = 598089** (added 2026-11-17 in the lecture/video expansion pilot); 5.6 guide 597910, 5.7 problems 597911, 5.8 games 597912 (moved/retitled, same ids). Old transcluded pages 597525–597529, 597535 retired to 597819 as "Old 5.x …". ADAPT assignment 224849, folder 15023. **All molar masses use the yellow-sheet atomic masses in `tools/yellow_sheet_masses.json`** (addition rule on the printed decimals). Updating an existing page property (e.g. overview) = PUT `pages/{id}/properties/{double-encoded name}?etag=<ETag without quotes>`; POST gives 409.
- **Expansion from lectures/videos (2026-11-17):** all 14 chapters deepened from Dr. Dan's slides and video transcripts (audit/expansion/: gap files, EXPAND_BRIEF.md, EXPANSION-LOG.md); every chapter science-reviewed before publishing. New pages: 5.5 (598089; guide/problems/games moved to 5.6–5.8), 1.3.3 Reading Measuring Tools (598091), 1.4.4 Word Problems and Dosage Calculations (598092), 1.4.5 Percents as Conversion Factors (598093). Use `&#8644;` for the equilibrium arrow: LibreTexts stores the HTML5 entity `&rlarr;` as literal text. Publishing method: push the drafts, then from a signed-in LibreTexts tab fetch old/new files from raw.githubusercontent.com/ItsDrDan/CHEM3Atextbook/<sha>/, check live text == old (normalized), POST new, read back.
- **Chapter 6 (2026-11-14):** intro on chapter page 597486 (Chemistry in the Community: Valley ozone; no Mateo); 6.1–6.11 = 597922–597932 (6.8 guide, 6.9 problems, 6.10 games, 6.11 Going Further: resonance and octet exceptions). Old transcluded pages 597530–597533, 597536–597539, 597541 retired to 597819 as "Old 6.x …". ADAPT assignment 224851, folder 15025. Polarity follows his slides: ΔEN 0–0.4 nonpolar (C–H 0.4 nonpolar), >0.4–2.0 polar covalent, >2.0 ionic; SNAP; yellow-sheet electronegativities in `tools/yellow_sheet_masses.json`.
- **Chapter 7 (2026-11-14):** intro on chapter page 597490 (old intro saved in drafts/archive/); 7.1–7.12 = 597944–597955 (7.9 guide, 7.10 problems, 7.11 games, 7.12 Going Further: acidic/basic redox, batteries). Old transcluded pages 597562–597571, 597606 retired to 597819 as "Old 7.x …". ADAPT assignment 224852, folder 15026. Solubility follows the green sheet; unstable products H2CO3/H2SO3/NH4OH; oxidation-number rules in his priority order; no H2O/H+/OH− redox balancing in the main path.
- **Chapter 8 (2026-11-14):** "Stoichiometry": intro on chapter page 597491 (Biology Connection opener, no Mateo; old intro saved in drafts/archive/); 8.1–8.9 = 597962–597970 (8.7 guide, 8.8 problems, 8.9 games). Old transcluded pages 597534, 597572–597576 retired to 597819 as "Old 8.x …". ADAPT assignment 224853, folder 15027. Limiting reactant found by "product each reactant could make"; STP = 0 °C, 1 atm, 22.4 L/mol; ΔH values that end in zeros are written in scientific notation (−2.220 × 10³ kJ).
- **Chapter 9 (2026-11-14):** "Energy, Solids, and Liquids": intro on chapter page 597487 (Chemistry in the Community: Valley heat and Cal/OSHA; no Mateo opener, one Mateo practice problem; old intro saved in drafts/archive/); 9.1–9.11 = 597980–597990 (9.9 guide, 9.10 problems, 9.11 games). Old transcluded pages 597540, 597542–597548, 597499 (with subpages) retired to 597819 as "Old 9.x …". ADAPT assignment 224854, folder 15028. Conventions: K = °C + 273.15, °C = (°F − 32)/1.8 (exact constants); 1 cal = 4.184 J; water c 4.184, ice 2.09, steam 2.01 J/(g·°C); ΔHfus 6.02, ΔHvap 40.7 kJ/mol; IMF ranking dispersion < dipole–dipole < H bond < ion–dipole. ΔEN 0.4 bonds (S–H, P–H, H–I, C–Br) count as nonpolar under his rule, so H2S/PH3/HI are avoided as "polar" examples.
- **Chapter 10 (2026-11-14):** "Gases": intro on chapter page 597488 (Patient Case: Mateo on 2 L/min oxygen; old intro saved in drafts/archive/); 10.1–10.9 = 597999–598007 (10.7 guide, 10.8 problems, 10.9 games). Old transcluded pages 597549–597555, 597657 (with subpages) retired to 597819 as "Old 10.x …". ADAPT assignment 224855, folder 15029. Conventions: R = 0.082058 L·atm/(mol·K) (yellow sheet; 62.36 L·torr); STP = 273 K, 1 atm, 22.4 L/mol; 1 atm = 760 mmHg = 760 torr = 101.325 kPa = 14.7 psi; water vapor pressures from his slides (17.5/23.8/31.8 mmHg at 20/25/30 °C) plus 47.1 at 37 °C; K = °C + 273.15, round half up; gas density/molar mass as one paragraph + one example. Gauge vs absolute pressure is not taught in CHEM 3A: mention only as "Going further", never in Try It/ADAPT.
- **Chapter 11 (2026-11-14):** "Solutions": intro on chapter page 597489 (Patient Case: Mateo's 0.9% NaCl IV and nebulizer dilution; old intro saved in drafts/archive/); 11.1–11.9 = 598016–598024 (11.7 guide, 11.8 problems, 11.9 games). Old transcluded pages 597556–597561, 597656, 597659 (with subpages) retired to 597819 as "Old 11.x …". ADAPT assignment 224856, folder 15030. Conventions: molality tied to osmolality (serum 275–295 mOsm/kg), ideal i values, Kf 1.86 and Kb 0.512 °C kg mol⁻¹; 0.9% NaCl treated as isotonic.
- **Chapter 12 (2026-11-15):** "Acids and Bases": intro on chapter page 597492 (Patient Case: Mateo's blood gas pH 7.30, respiratory acidosis; old intro saved in drafts/archive/); 12.1–12.9 = 598030–598038 (12.7 guide, 12.8 problems, 12.9 games). Old transcluded pages 597577–597581 retired to 597819 as "Old 12.x …". ADAPT assignment 224857, folder 15031. Conventions: strong acids HCl, HBr, HI, HNO3, HClO4, H2SO4 (first proton; never used in pH math); strong bases = Group 1 hydroxides + Ca(OH)2, Sr(OH)2, Ba(OH)2 (Mg(OH)2 weak); H3O+ notation; Kw = 1.0 × 10⁻¹⁴; pH + pOH = 14.00; decimal places in pH = sig figs in concentration; buffers qualitative (no Henderson–Hasselbalch). Explore It: Red Cabbage Indicator (vlab 12a) in 12.1, PhET pH Scale (bench 12a) in 12.5. Note: a moved page leaves a redirect at its old path, so a new page cannot reuse an old path segment (12.1 lives at 12.01:_Acid_and_Base_Properties).
- **Chapter 13 (2026-11-15):** "Chemical Equilibrium": intro on chapter page 597493 (Patient Case: Mateo breathing fast, CO2 ⇌ H2CO3 ⇌ H+ + HCO3−; old intro saved in drafts/archive/); 13.1–13.8 = 598045–598052 (13.5 guide, 13.6 problems, 13.7 games, 13.8 Going Further: Ka/Kb, Ksp, common ion). Old transcluded pages 597582–597587 retired to 597819. ADAPT assignment 224861, folder 15032. Conventions: K > 1 favors products, K < 1 favors reactants, K close to 1 (about 0.1–10) both; very large/small K nearly complete/barely happens; reverse K = 1/K; pure solids and liquids omitted; only temperature changes K; Le Chatelier is the main skill.
- **Chapter 14 (2026-11-15):** "Radioactivity and Nuclear Chemistry": intro on chapter page 597494 (Patient Case: Mateo's V/Q scan with Tc-99m, 6.0 h); 14.1–14.10 = 598058–598063, 598071, 598064–598066 (14.6 Radiation and Health, 14.7 Radiation in Medicine (598071, split from the old 14.6 on 2026-11-15 with his OK), 14.8 guide, 14.9 problems, 14.10 games). Old transcluded pages 597588–597592 retired to 597819. ADAPT assignment 224862, folder 15033 (117 questions; Try It topics include ch14-health). Conventions: whole numbers of half-lives only; C-14 5730 years with ages to 3 sig figs (avoid 5 half-lives, a rounding tie); nuclear symbols as <sup>A</sup><sub>Z</sub>X in banks; electron capture and bombardment included (from his slides).
- **Explore It boxes (2026-11-14, Dr. Dan):** interactive sims from the game repos may be embedded in sections as green "Explore It" boxes (iframe + "open in a new tab" link + "Interactive by ItsDrDan (all rights reserved; linked, not part of the licensed text)"). Only deep links that open the right lab for `course=3A`; enabling a lab for 3A is a game change (simulator-test, ask before pushing). **Live 2026-11-14 (18 boxes):** 1.9 vlab 1a; 2.5 bench 2a; 2.6 vlab 2a; 3.2 bench 3a; 6.4 bench 6a; 7.2 bench 10a; 7.5 vlab 10a; 8.4 bench 11a; 9.4 bench 7a; 9.5 IMF curve; 9.6 IMF lab + well; 10.3 bench 8a; 10.6 vlab 8a; 11.1 IMF mix; 11.4 vlab 9a; 11.5 vlab 12b; 11.6 IMF solutions + cell (labpractical = `https://itsdrdan.github.io/labpractical/?mode=bench|vlab&labs=XX`; PhET boxes credit PhET, CC BY 4.0). Each box sits just before the Video Lesson(s) heading. No deep link exists for Ch 4/5 sims (ionicformula Free Builder, polyatomic Ion Builder, moles Mole Machine) or gaslaws Piston Lab; labpractical (since e698fc3) skips its intro inside a frame, so the lab card is on top.
- **Final Boss deep links (2026-11-17, finalexam v54):** each Practice Games page embeds `https://itsdrdan.github.io/finalexam/?course=3A&mode=topic&topic=<keys>` (comma list for two topics: Ch 1 measure,matter; Ch 6 bonding,moles; Ch 9 energy,bonding), which opens Topic Training on the chapter and scrolls to the question. Accessibility test: audit/ACCESSIBILITY_2026-11-17.md (axe-core on all 171 live pages; underline links inside gray captions). Interactives gap and OER remix comparison: audit/expansion/INTERACTIVES_GAP.md, REMIX_COMPARISON.md.
- **Glossary and accessibility (2026-11-17):** never list one-letter symbols as glossary synonyms (LibreTexts matches case-insensitively, so "A" made every "a" a pop-up); backmatter/build_backmatter.py now drops them and writes "(Symbol: X.)" into the definition. The live Glossary page (597477) is LibreTexts' own layout, so edit its rows in place rather than replacing the page. Accessibility Statement = Front Matter page 598094 (source drafts/front/accessibility_statement.html).
- **Hints and explanations (2026-11-17, Dr. Dan):** every question explains the right answer, every wrong choice (mistake + fix) and has a hint. Every exercise/practice-problem box has `<details><summary>Hint</summary>` above `<details><summary>Answer</summary>` (1,398, published); new exercises must follow this. Hints point to the first step in the book's words and never settle a multiple-choice question (no restated correct choice, no full list, no numeric factor). Bank wrong-choice reasons give the fix too. Tools and record: audit/hints/ (README, HINT_BRIEF, check_hints.py, apply_hints.py).
- **OpenStax figures (2026-11-18):** remix figures only from the LibreTexts copy of OpenStax *Chemistry 2e* (pages tagged CC BY 4.0; openstax.org itself is not the source). Download into figures/openstax/ (compress photos to ~100 KB), write our own alt text and caption, end the caption with "(From OpenStax, Chemistry 2e, Section X.Y [linked], CC BY 4.0; photo credits.)", and add the OpenStax sentence to the page's Attribution box. Scripts: tools/add_openstax_figs.py, _2.py, _3.py (renumber captions; _3 reads audit/figures/batch3_*.json, brief in audit/figures/BATCH3_BRIEF.md). Batches 1-2 live (Ch 1, 2, 10, 11, 12, 14); batch 3 (Ch 3-9, 13; 30 figures) 2026-11-19. Only "modification of work by" or uncredited OpenStax art; never put a full-width figure inside a fig-wrap zone (move it past the next heading, box or table); check in-text "Figure N" references after renumbering.
- **Key Equations and Key Terms (2026-11-19):** each Chapter Guide has "Key Equations" (Ch 1-3, 5, 6, 8-14) and "Key Terms" tables after Key Ideas, built by tools/build_key_terms.py (terms from backmatter/glossary_3A.json, section links via @go/page ids; equations written in the script). Rerun the script after glossary or equation changes; it replaces both blocks.
- **Chapter map for cross-references:** 1 Measurement/Matter, 2 Atoms, 3 Light/Electrons, 4 Naming, 5 Mole, 6 Bonds/Shapes/Composition, 7 Reactions, 8 Stoichiometry, 9 Energy/Solids/Liquids (IMF, temperature), 10 Gases, 11 Solutions, 12 Acids/Bases, 13 Equilibrium, 14 Nuclear.
- **Phones:** every YouTube iframe gets `style="max-width:100%;height:auto;aspect-ratio:16/9;"` (LibreTexts fixes them at 560 px); long display equations sit in `<p style="text-align:center;overflow-x:auto;overflow-y:hidden;">`.
- **Print style position (2026-11-19):** the print-only `<style>` on exercise pages must be the LAST thing on the page (tools/print_layout.py puts it there). When it was first, any page with an OpenStax photo printed as if it had no style (tested in Full (35)).
- **Tables:** run `python3 tools/add_data_th.py <drafts>` on every new page (phone labels on LibreTexts).

### Editing LibreTexts pages (what worked)

- **Read a page:** `GET /@api/deki/pages/{id}/contents?mode=edit&dream.out.format=json`, from a browser tab signed in on chem.libretexts.org.
- **Write a page:** `POST /@api/deki/pages/{id}/contents?edittime=now&dream.out.format=json` with the page HTML as `text/plain; charset=utf-8`.
- **Make every write safe:**
  - Apply exact string replacements.
  - Require each replacement to match exactly once, and abort otherwise.
  - Re-read the page after saving.
  - Check the rendered page for "Math Processing Error" or raw `\(`.
- **Fork a transcluded page:** use the page's "Forker" menu item ("Fork this transcluded page"). It shows a `confirm()` dialog, so override `window.confirm` before clicking.
- **Remixer v3** uses HTML5 drag-and-drop, which needs dispatched `dragstart`/`dragover`/`drop` events. Always open it from the project page's "Open OER Remixer v3" button.
- **Lessons from CHEM 3B:**
  - LibreTexts' glossary script breaks words inside inline-SVG `<text>`. Upload labeled figures as SVG/PNG files and use `<img>`.
  - Once pages are edited directly on LibreTexts, LibreTexts is the source of truth. Pull the live HTML back into the repo before rebuilding.
  - Never re-run an upload script that could overwrite newer edits.
- `\(\PageIndex{n}\)` renders as page number plus index (for example 1.1.1.1). Use it instead of hard-coded numbers left over from source books (such as "Example 2.2.1").

## Decisions already made

### Book structure

- **Chapter order:** follow the COR, not the syllabus. The CHEM 3A COR is not public online. Find it in `~/Desktop/FCC Teaching` or Dr. Dan's Canvas, or ask him for it. Save it as `tools/COR_outline.md` once you have it.
- **Repo:** this repo, separate from `ItsDrDan/textbook`. Copy (do not link) the tools you need from that repo, and adapt them for 3A.
- **Chapters (approved 2026-11-14):** 14 chapters in COR order, as in `tools/BLUEPRINT.md`. COR unit 1 is split into three chapters (1 Matter and the Scientific Method; 2 Atoms, Ions, and Isotopes; 3 Light, Electrons, and the Periodic Table). The audited old Chapter 1 becomes Chapter 5; temperature moves to Chapter 9.

- **Measurement is in Chapter 1 (Dr. Dan, 2026-11-14).** Chapter 1 is "Measurement, Matter, and the Scientific Method": the audited measurement sections (units, scientific notation, significant figures, conversions, density as a conversion factor) are merged into it. Measurement opens the course on purpose: it is the segue that shows students why these skills matter for their careers in health care, science and engineering. This is a deliberate exception to COR order (COR unit 3 comes after units 1–2). Chapter 5 keeps the mole. Temperature stays in Chapter 9.

### Scope decisions (Dr. Dan, 2026-11-14; these override the COR conflict notes)

- **Activity series:** shown, but very lightly (a short given list, "will this metal replace that one?").
- **Gas density / molar mass:** one paragraph and one worked example, very light; not a main skill.
- **Redox:** simple half-reactions only (for example, single displacement). No balancing in acidic or basic solution (that goes in Going Further).
- **Corrosion:** used as relatable examples inside the redox section (rusting, tarnish, dental amalgam), not a separate topic.
- **Enthalpy of reaction** (thermochemical equations, heat in stoichiometry): taught in the main path.
- **Buffers:** taught in the main path at the CHEM 3A level (qualitative; blood bicarbonate buffer). No Henderson–Hasselbalch.
- **Equilibrium:** the emphasis is Le Chatelier's principle. Writing K expressions and reading large vs small K stay, lightly; "special types of equilibria" (old 13.5) goes in Going Further.
- **Molality:** taught in the main path, tied to **osmolality and physiology** (serum osmolality, IV fluids, colligative properties in the body).
- **Going Further (not on CHEM 3A exams):** resonance, octet-rule exceptions, redox balancing in acidic/basic solution, batteries, special types of equilibria. Keep them as labeled pages so other faculty can assign them.

### Scope decisions (Dr. Dan, 2026-11-17)

- **Colligative properties:** the main skill is how much the freezing point is lowered (ΔTf) or the boiling point raised (ΔTb). Finding the new freezing point is a short optional last step; CHEM 3A problems usually stop at ΔT.
- **Nuclear:** simple decay, bombardment and electron capture are the main skills. Balancing fission and fusion equations is a challenge item (fine in the ADAPT bank as challenge problems).
- **Equilibrium:** no ICE tables; K expressions (products over reactants) and Keq only.
- **Electron configurations:** the Cr and Cu exceptions are a normal CHEM 3A problem (taught in 3.4).
- **Phase changes:** heating/cooling curves with q = mcΔT are the main skill; phase diagrams are shown so students see both (Going Further section in 9.5).
- **Naming:** Dr. Dan's "blue sheet" is the naming flowchart he gives students (metal? → transition metal? → count elements; no metal → hydrogen first? → acid, else diatomic or covalent binary). Section 4.6 follows its logic.
- **"James Bond / Alien" slide:** shows that films portray acids eating through metal (villains using acid); used as a "Movie Chemistry" misconception box in 7.3.
- **Chapter 1 measurement pages:** rewrite the inherited pages as his own, tied to nursing and health care (why measurement, accuracy and precision matter). Done 2026-11-17: all 12 inherited pages (1.2–1.4.3, 1.9.1, 1.12; same page ids) now hold his CC BY text; Chapter 1 has no CK-12 or NC-SA pages left. Yellow-sheet values: tools/yellow_sheet_conversions.md.
- **Lab safety in examples:** no benzene in student-facing lab examples; use a safer liquid.

### Patient case (approved 2026-11-14)

**Case A: Mateo Herrera, 34**, an irrigation technician on a Fresno County almond orchard, with asthma (see `tools/PATIENT_CASE_PROPOSAL.md`). He appears **only where the chemistry has a strong tie** to his care, not in every chapter. Chapters without him (1, 6, 8, 9) open with one of: a short one-off patient vignette (a different person), a Biology Connection opener, or a **Chemistry in the Community** opener (local, Valley-based), whichever fits the chapter best (Dr. Dan, 2026-11-14).

### Biology ties (Dr. Dan, 2026-11-14)

Show where the chemistry ties into **biology, anatomy, physiology and microbiology** as much as possible: in the teaching text, worked examples, problems and a "Biology Connection" box (anatomy, physiology, microbiology). This is in addition to the allied-health boxes and is not limited the way the Major Connection boxes are.

### Features (all chosen)

1. **Chapter Guides and rewritten sections**, tied to Dr. Dan's CHEM 3A lecture slides. Each has:
   - Learning Objectives
   - Key Ideas
   - Video Lessons
   - Worked Examples in Problem / Solution / Check form
   - Common Mistakes
   - Professor Tips
2. **Try It widgets and a Practice Games page for every chapter.**
   - Use auto-graded Try It widgets in the text. This needs a CHEM 3A version of the `practice.html` widget plus 3A bank JSON files.
   - Each chapter's Practice Games page links the CHEM 3A games for that chapter.
3. **Practice Problems and ADAPT homework.**
   - Each chapter gets 40–60 original, checked problems, with reasoning shown in every answer.
   - Each chapter's ADAPT homework is worth 100 points, has about 50 questions, scales points per question to the question count, and uses rotating (randomized) question sets.
   - Give per-choice feedback for right and wrong answers everywhere. Dr. Dan wants as much feedback as possible.
4. **Career and Valley boxes.**
   - **Allied-health clinical boxes:** Nursing, Dental Hygiene, **Radiologic Technology**, **Respiratory Therapy**. Each is 80–220 words, tied to the chemistry skill just taught, with medical terms defined on first use. They give context only, never treatment advice.
   - **Add-ins for other majors:** Biology, Chemistry and Engineering students, for example a "Major Connection" box. Keep them shorter and fewer than the allied-health boxes; about 75% of the class is allied health.
   - **Valley Connection boxes:** 120–400 words with real, cited sources, tying the chemistry to Central Valley life and careers (agriculture, water, air quality, dairy, local health care, and so on). Give the allied-health and other majors' boxes Valley tie-ins where they fit naturally.
   - **A running patient case across chapters.** The CHEM 3B book uses an adult with type 2 diabetes ("Rosa"). Propose a different case suited to 3A topics (measurement, dosing math, gases, solutions, acids/bases, nuclear medicine) and get Dr. Dan's approval before writing it. **Approved: Case A (Mateo), strong-tie chapters only.**
5. **Videos.**
   - Embed Dr. Dan's own ItsDrDan YouTube videos in chapter intros and the relevant sections. Use the transcripts to choose videos and to point to key moments (timestamps).
   - Never invent video links. Verify each link and title.

### Chemistry conventions (apply everywhere)

- **Significant figures:** trailing zeros without a decimal point are **not** significant (2500 → 2, 500 → 1, 3800 → 2). A trailing decimal point makes them significant (500. → 3, 2500. → 4). Scientific notation shows any other precision.
- **Course reference sheets:**
  - The **yellow sheet** (periodic table, conversions, constants). Avogadro's number is **6.0221 × 10²³**.
  - The **green sheet** (polyatomic ions, solubility rules, strong acids and bases).
- **Calculator tips** are written for the TI-36X Pro.
- **CHEM 3A scope notes:**
  - Quantum: only simple wavelength/frequency/energy calculations, orbital diagrams (no ℓ, mℓ, ms), full and noble-gas electron configurations, and simple periodic trends.
  - Gas density: one light paragraph and example only (see Scope decisions).
  - Activity series: very light only (see Scope decisions).
  - Intermolecular forces: polarity in new Chapter 6, IMF in new Chapter 9 (old book Chapters 6 and 7).
  - The CHEM 3A lab uses red cabbage indicator, never a pH meter.
- **Exam-style problem conventions:**
  - Reactions centered on their own line.
  - Molar masses given in a small chart.
  - Data presented in tables.
  - Units with denominators written like g mol⁻¹.
  - Picture-based questions are welcome: glassware and balance readings, accuracy versus precision, particle diagrams.

### Sources and how they may be used

- **Dr. Dan's materials:** lecture slides, worksheets and homework, study guides, exams, lab manual (Fall 2026), and MyOpenMath. All are allowed for alignment and language.
  - **Exams, Skill Checks and homework are never copied.** Similar problems with new numbers and molecules are fine.
  - Exact copies of Skill Check questions are never allowed.
- **Publisher test banks** (Tro Intro Chemistry, in Study Games): guide difficulty only. Never copy or closely paraphrase them.
- **OER source text:** the current book's sources may be kept, rewritten or replaced with other openly licensed text. Keep each source's license and attribution.
- **Licensing:**
  - Book content is CC BY 4.0 unless otherwise indicated. Pages adapted from NC or SA sources keep those terms; follow the CHEM 3B book's pattern.
  - Dr. Dan's games are all rights reserved: link to them, never fold them into the licensed text.
  - Check OER standards against Dr. Dan's CELA-308 materials (SCCCD Canvas courses 33246 and 108299). OER Coordinator: Sally Potter.
- **Accessibility:**
  - Headings in order.
  - Meaningful alt text on every image.
  - Tables with header cells and a lead-in sentence.
  - Never rely on color alone.
  - Spell out abbreviations on first use.
  - `<details><summary>Answer</summary>` for hidden answers.

### Lecture slides and lab manual (Dr. Dan, 2026-11-14)

For every chapter, use the matching CHEM 3A lecture decks in `~/Desktop/FCC Teaching/CHEM 3A/Lecture Slides/` (map in `tools/SOURCES.md`) to align content, emphasis, wording and examples with how the course is taught, and to write Lecture Connection notes. Visuals may be pulled from the slides when a chapter needs them: redraw them as original, phone-first figures (slides can contain publisher or web images that cannot go into the open book). Use the Fall 2026 lab manual (`Lab Manual/DK-Lab Manual - Chem 3A - Fall 2026.docx`) for "In the Lab" connections to the matching experiment.

## Working rules

- Commit freely in this repo. **Ask Dr. Dan before pushing to GitHub, and before any write to LibreTexts.** Never touch the live CHEM 3A book.
- Verify every number by running the math. Look at every figure and page render before calling it done; the CHEM 3B repo has preview and check tools for this.
- Keep a running issues log in the format of the Chapter 1 audit tracker (page, category, priority, issue, fix, status).
- When a decision is genuinely Dr. Dan's to make (the patient case, chapter mergers, anything that changes what other faculty teach), ask him. For everything else, use the defaults in this file and keep going.

## First session plan

1. **COR.** Find the CHEM 3A COR in `~/Desktop/FCC Teaching` (or ask for it). Save it to `tools/COR_outline.md`.
2. **Inventory.** List what is in the CHEM 3A course folders (slides by lecture, worksheets, study guides, lab manual, MyOpenMath exports) and in the YouTube Subtitles folder. Write `tools/SOURCES.md`, mapping each file to COR topics.
3. **Blueprint.** Write `tools/BLUEPRINT.md`, with one entry per chapter in COR order:
   - the sections and the current draft pages they come from (or "new")
   - lecture slides
   - videos with timestamps
   - games
   - question-bank topics
   - the clinical, major and Valley boxes planned
   - the patient-case beat
4. **Author brief.** Adapt `ItsDrDan/textbook/tools/AUTHOR_BRIEF.md` into `tools/AUTHOR_BRIEF.md` for 3A, using this file's decisions.
5. **Review with Dr. Dan.** Show him the blueprint and the patient-case proposal. Start building Chapter 1 only after he approves. **Done 2026-11-14: approved with the decisions above.**
