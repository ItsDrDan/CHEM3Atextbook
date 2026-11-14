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
| **YouTube transcripts** | `~/Desktop/YouTube Production/Subtitles/` (all ItsDrDan videos) |
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

- **Draft reordered to COR order 2026-11-14** (with his go-ahead): 14 chapters, blueprint titles, sections renumbered, pages moved between chapters per the blueprint, superseded pages moved to a "Retired Pages" holder (597819) at the end. Full map and undo notes: `tools/REORDER_2026-11-14.md`. Page ids did not change. New Chapter 1 path is now `.../01:_Matter_and_the_Scientific_Method`. Source of truth from now on is LibreTexts; pull before re-editing. Tags: `article:topic(-guide)`, `author@Daniel Kwasniewski`, `authorname:dkwasniewski`, `license:ccby`, `licenseversion:40`, `showtoc:no`.

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
