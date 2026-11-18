# CHEM 3A homework in LibreTexts ADAPT

## Set up 2026-11-14

- **Course:** "CHEM 3A: Introductory General Chemistry", ADAPT course **11836** (Fresno City College, discipline Chemistry - Introductory). Not shown to students. Textbook URL: the Revision Draft workbench book. Course dates 2026-11-14 to 2027-05-28 (placeholders). LMS link is OFF; turn it on in Course Properties → LMS to connect Canvas (the CHEM 3B course 4605 uses Canvas).
- **Assignment:** "CHEM 3A Chapter 1: Measurement, Matter, and the Scientific Method", id **224842**, made from the "CHEM 3B Chapter Homework" template (145): real-time grading, 3 attempts, no attempt penalty, hints on with no penalty, late work accepted and marked late, group Homework, **2 points per question**, each student gets a random **50** questions (= 100 points). Placeholder dates: available 2026-11-14, due 2027-05-21, final deadline 2027-05-28; set real dates before use.
- **Folder:** My Questions → "CHEM 3A Ch 01 Measurement, Matter, and the Scientific Method" (folder 15018). Every question public, CC BY 4.0, author Daniel Kwasniewski.
- **Pool:** the text-only items of `bank/ch01.json` (Try It bank) and all of `bank/ch01_adapt.json` (homework-only). Question title = bank id (c1-001 …, c1-h01 …). Items with a figure (`f`: particle diagrams, glassware/ruler/buret readings, targets) are **not yet in ADAPT**; they need rendered images (the CHEM 3B recipe in ItsDrDan/textbook `adapt/README.md`, render_thin.js).

## Feedback in each question (qti_json)

- Each choice has its own feedback: the right answer shows "Correct! " + the bank's explanation; each wrong choice shows the bank's `y` entry for that choice.
- Generic wrong-answer feedback: "Not quite. Hint: " + the bank hint. The same hint is in Show Hint.

## How the questions were created (for next chapters)

POST `/api/questions` (Bearer token from the `token` cookie) with the editor-shaped body from `/api/questions/get-question-to-edit/{id}` of an existing question, minus server fields (id, page_id, iframe_id, dates, revision fields, qti_answer_json), plus: title, qti_json, qti_json_type "multiple_choice", qti_prompt, qti_simple_choice_0..3, qti_randomize_order "yes", hint, folder_id, assignment_id (auto-adds it to the assignment), attachments/learning_outcomes/media_uploads/tags/clone_history as arrays, session_identifier (UUID), source_url_required true, framework_item_sync_question {descriptors: [], levels: []}, webwork_attachments [], automatically_update_revision "1", revision_action "notify", public 1, license "ccby", license_version "4.0", author. Folders: POST `/api/saved-questions-folders` {name, type: "my_questions", action: "add"}.

## Status 2026-11-14 (end of day)

- **127 questions in assignment 224842** (87 text-only Try It items c1-001…c1-099 minus 12 figure items, plus 40 homework-only c1-h01…c1-h40). No duplicates. Random draw **50 per student × 2 points = 100 points**. Assignment not released (hidden) until Dr. Dan sets dates.
- **Read-back:** all 127 compared with the bank (stem, all four choices, correct key, every wrong-choice feedback, CC BY 4.0, public, Show Hint present). All match; the only difference is ADAPT storing `<br />` as `<br>` in c1-088.

## Picture questions added 2026-11-14

- The 12 figure items (c1-012–016, c1-052–054 particle diagrams; c1-084–087 cylinder, ruler, buret, target) are now in assignment 224842 (ADAPT ids 356178–356189). **Pool: 139 questions**, random 50 × 2 points.
- Images: `figures/adapt/<id>.svg`, built by `node tools/adapt_figs.js bank/ch01.json figures/adapt` from the same fbx.js drawings the Try It widget uses (duplicate SVG attributes removed so the files are valid XML), hosted on GitHub Pages and linked in each question stem as `<img>` with alt text from `figures/adapt/alt_ch01.json` (describes the picture without naming the answer).
- Read back: all 12 match the bank (choices, key, every wrong-choice feedback), alt text present, image loads, CC BY 4.0, public. Checked visually in ADAPT's question view (c1-014, c1-086).

## Chapter 2 (2026-11-14)

- Assignment **224843** "CHEM 3A Chapter 2: Atoms, Ions, and Isotopes" (template 145; 3 attempts, hints no penalty, marked late; 2 points; random 50 of the pool = 100 points; hidden; placeholder dates as Chapter 1). Folder 15019.
- Pool **104**: all 64 Try It items in `bank/ch02.json` (7 with SVG images + alt text from `figures/adapt/alt_ch02.json`; the 2 data-table items carry a real HTML table in the stem) and 40 homework-only items in `bank/ch02_adapt.json`.
- Read back: all 104 match the bank (choices, key, every wrong-choice feedback, stem), CC BY 4.0, public, Show Hint present; all 7 images load. c2-025 checked visually in the question view.

## Chapter 3 (2026-11-14)

- Assignment **224844** "CHEM 3A Chapter 3: Light, Electrons, and the Periodic Table" (template 145; same settings as Chapters 1–2: 3 attempts, hints no penalty, marked late, 2 points, random 50 of the pool = 100 points; hidden; placeholder dates). Folder 15020.
- Pool **104**: all 64 Try It items in `bank/ch03.json` (6 with SVG images + alt text from `figures/adapt/alt_ch03.json`: 2 orbital diagrams, 4 periodic-table outlines; the 2 data-table items carry an HTML table in the stem) and 40 homework-only items in `bank/ch03_adapt.json`.
- Read back: all 104 match the bank (stem, choices, key, every wrong-choice feedback), CC BY 4.0, public, Show Hint present; all 6 images load. ADAPT stores arrows as `&uarr;`/`&darr;` entities (same text).

## Chapter 4 (2026-11-14)

- Assignment **224846** "CHEM 3A Chapter 4: Naming Compounds" (template 145; same settings: 3 attempts, hints no penalty, marked late, 2 points, random 50 = 100 points; hidden; placeholder dates). Folder 15021.
- Pool **106**: all 66 Try It items in `bank/ch04.json` (4 table items carry an HTML table in the stem; no images) and 40 homework-only items in `bank/ch04_adapt.json`.
- Read back: all 106 match the bank (stem, choices, key, every wrong-choice feedback), CC BY 4.0, public, Show Hint present.

## Chapter 5 (2026-11-14)

- Assignment **224849** "CHEM 3A Chapter 5: The Mole" (template 145; same settings: 3 attempts, hints no penalty, marked late, 2 points, random 50 = 100 points; hidden; placeholder dates). Folder 15023.
- Pool **100**: all 60 Try It items in `bank/ch05.json` (3 table items carry an HTML table in the stem) and 40 homework-only items in `bank/ch05_adapt.json`. Mostly calculation items (76 of 100), molar masses from the yellow sheet.
- Read back: all 100 match the bank, no duplicates, none missing. (The upload was interrupted once by a page reload at 98; the rerun skipped existing titles, so nothing was doubled.)

## Chapter 6 (2026-11-14)

- Assignment **224851** "CHEM 3A Chapter 6: Chemical Bonds, Shapes, and Composition" (template 145; same settings: 3 attempts, hints no penalty, marked late, 2 points, random 50 = 100 points; hidden; placeholder dates). Folder 15025.
- Pool **106**: all 66 Try It items in `bank/ch06.json` (3 table items with an HTML table in the stem) and 40 homework-only items in `bank/ch06_adapt.json`.
- Read back: all 106 match the bank, no duplicates, none missing.
- Tip: if the properties icon click does not open the modal, the Vue form data still loads; set randomizations and click the visible Save button.

## Chapter 7 (2026-11-14)

- Assignment **224852** "CHEM 3A Chapter 7: Chemical Reactions" (template 145; same settings: 3 attempts, hints no penalty, marked late, 2 points, random 50 = 100 points; hidden; placeholder dates). Folder 15026.
- Pool **112**: all 70 Try It items in `bank/ch07.json` (2 table items with an HTML table in the stem) and 42 homework-only items in `bank/ch07_adapt.json`.
- Read back: all 112 match the bank, no duplicates, none missing.

## Chapter 8 (2026-11-14)

- Assignment **224853** "CHEM 3A Chapter 8: Stoichiometry" (template 145; same settings: 3 attempts, hints no penalty, marked late, 2 points, random 50 = 100 points; hidden; placeholder dates). Folder 15027.
- Pool **108**: all 66 Try It items in `bank/ch08.json` (3 table items with an HTML table in the stem; 1 particle-diagram item, c8-041, with `figures/adapt/c8-041.svg` and alt text in `figures/adapt/alt_ch08.json`) and 42 homework-only items in `bank/ch08_adapt.json`.
- Read back: all 108 match the bank, no duplicates, none missing.

## Chapter 9 (2026-11-14)

- Assignment **224854** "CHEM 3A Chapter 9: Energy, Solids, and Liquids" (template 145; same settings: 3 attempts, hints no penalty, marked late, 2 points, random 50 = 100 points; hidden; placeholder dates). Folder 15028.
- Pool **114**: all 72 Try It items in `bank/ch09.json` (3 table items with an HTML table in the stem; 1 heating-curve plot item, c9-042, with `figures/adapt/c9-042.svg` and alt text in `figures/adapt/alt_ch09.json`) and 42 homework-only items in `bank/ch09_adapt.json`.
- Read back: all 114 match the bank, no duplicates, none missing.

## Chapter 10 (2026-11-14)

- Assignment **224855** "CHEM 3A Chapter 10: Gases" (template 145; same settings: 3 attempts, hints no penalty, marked late, 2 points, random 50 = 100 points; hidden; placeholder dates). Folder 15029.
- Pool **112**: all 70 Try It items in `bank/ch10.json` (3 table items with an HTML table in the stem) and 42 homework-only items in `bank/ch10_adapt.json`.
- Read back: all 112 match the bank, no duplicates, none missing.

## Chapter 11 (2026-11-14)

- Assignment **224856** "CHEM 3A Chapter 11: Solutions" (template 145; same settings: 3 attempts, hints no penalty, marked late, 2 points, random 50 = 100 points; hidden; placeholder dates). Folder 15030.
- Pool **114**: all 72 Try It items in `bank/ch11.json` (3 table items with an HTML table in the stem; 1 solubility-curve plot item, c11-012, with `figures/adapt/c11-012.svg` and alt text in `figures/adapt/alt_ch11.json`) and 42 homework-only items in `bank/ch11_adapt.json`.
- Read back: all 114 match the bank (stem, choices, key, every wrong-choice feedback, hint feedback, CC BY 4.0, public); c11-012 image loads, alt text present; Show Hint present.
- Tip: with the browser pane hidden, background-tab timer throttling slows the upload loop's 250 ms pause to many seconds; overriding `setTimeout` for that pause fixed it.

## Chapters 12–14 (2026-11-15)

- **Chapter 12** "CHEM 3A Chapter 12: Acids and Bases": assignment **224857**, folder 15031. Pool **114**: 72 Try It items in `bank/ch12.json` (3 table items with an HTML table in the stem) + 42 homework-only items in `bank/ch12_adapt.json`.
- **Chapter 13** "CHEM 3A Chapter 13: Chemical Equilibrium": assignment **224861**, folder 15032. Pool **112**: 70 Try It items in `bank/ch13.json` (2 tables; 2 plots, c13-003 and c13-019, as SVG images with alt text in `figures/adapt/alt_ch13.json`) + 42 in `bank/ch13_adapt.json`.
- **Chapter 14** "CHEM 3A Chapter 14: Radioactivity and Nuclear Chemistry": assignment **224862**, folder 15033. Pool **117** (3 health items added 2026-11-15 when 14.6 was split): 75 Try It items in `bank/ch14.json` (2 tables; decay-curve plot c14-043 as an SVG image with alt text in `figures/adapt/alt_ch14.json`) + 42 in `bank/ch14_adapt.json`.
- All three: template 145, 3 attempts, hints no penalty, marked late, 2 points, random 50 = 100 points, hidden, placeholder dates. Read back: every question matches the bank (stem, choices, key, every wrong-choice feedback, hint feedback, CC BY 4.0, public).
- **Duplicates:** ADAPT sometimes creates a question twice for one POST (consecutive ids) or answers "identical to the native question" for one it just created. After every upload, read back, and remove the extra copy with DELETE `/api/assignments/{aid}/questions/{qid}` (it stays in My Questions). Removed: 357290, 357312, 357332, 357367 (Ch 12) and 357435 (Ch 13).
- Running two uploads at once (different assignments) roughly halves the wait.

## Update of 2026-11-17: yellow-sheet lb/kg values in Chapter 1

- c1-079 (ADAPT 356121), c1-091 (356129), c1-099 (356137), c1-h34 (356171) and c1-h35 (356172) in assignment 224842 now use 1 kg = 2.2046 lb and 1 lb = 453.59 g, matching `bank/ch01.json` and `bank/ch01_adapt.json` (commit fd9352a). Intermediate values moved in the last digit; every key is unchanged.
- Saved with PATCH /api/questions/{id}: the get-question-to-edit object with **all its fields kept** except qti_answer_json (removing id, page_id and the other server fields gives a 500), plus the editor fields listed above; "automatically update", reason "Use the yellow-sheet value 1 kg = 2.2046 lb / 1 lb = 453.59 g (2026-11-17)."
- Read back: qti_json identical to what was sent for all five; no question in the assignment mentions 2.205 or 453.6; no pending revisions; correct choice still first-listed in each.
