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
- **Not in ADAPT yet:** c1-012–016, c1-052–054 (particle diagrams), c1-084–087 (cylinder, ruler, buret, target).
