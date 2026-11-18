# Gap analysis brief: expanding the CHEM 3A OER from Dr. Dan's lectures and videos

Goal: Dr. Dan (Daniel Kwasniewski, FCC) wants every chapter of his CHEM 3A book expanded with a deep dive, using his own teaching material as much as possible: (1) deepen existing sections (more step-by-step explanation, worked examples, misconceptions, analogies, memory aids, calculator tips the way HE teaches them) and (2) add NEW sections where his slides/videos teach a subtopic the book doesn't cover yet. You are doing the ANALYSIS only. Do not write book content and do not edit the repo.

## Inputs
- Book chapters (current text): `REPO/drafts/chNN/*.html` (REPO = "/Users/dan/Desktop/Study Games/github/CHEM3Atextbook"). Ch 1's inherited pages 1.2–1.4.3, 1.9.1, 1.12 are only in `SCRATCH/chapters/ch01.txt` (PDF text).
- Lecture slide text (with speaker notes): `SCRATCH/expand/slides/*.txt` (one file per deck; "--- slide N ---" markers). The deck→course-outline map is in `REPO/tools/SOURCES.md`. IGNORE "Lecture 26 Nucelic Acids" (CHEM 3B), anything in Skill Checks, Exams, Homework (never copied). PlayPosit files are fine for seeing what he emphasizes.
- Video transcripts: `SCRATCH/expand/videos/<videoId>.txt` (title on line 1, `[m:ss]` timestamps), index `SCRATCH/expand/videos/INDEX.tsv` (id, words, title). Many are CHEM 3B (organic/biochem): skip those.
- Scope rules: `REPO/CLAUDE.md` ("Scope decisions", "Chemistry conventions", "CHEM 3A scope notes") and `REPO/tools/COR_outline.md`. Never propose topics beyond the COR/CLAUDE.md scope (e.g., no quantum numbers ℓ/mℓ, no formal-charge minimization in main path, no Henderson–Hasselbalch, no ICE tables, no gauge pressure except "Going further"). Going Further pages exist for resonance/octet exceptions, acidic/basic redox, special equilibria.
- SCRATCH = /private/tmp/claude-501/-Users-dan-Desktop-Study-Games/902fb8b8-e606-48c8-860b-c64087a289e1/scratchpad

## Method
1. For each chapter: read the chapter's section pages (skim guides/problems), then read the matching slide decks fully and the matching video transcripts (search INDEX.tsv titles; grep transcripts for key terms).
2. Find: (a) concepts, explanations, worked-example types, misconceptions, memory aids, analogies, real-world/clinical examples, and calculator/technique tips in slides/videos that the book lacks or treats thinly; (b) whole subtopics with no section.
3. For each, give the SOURCE precisely: deck file + slide numbers, and/or video id + timestamp range (m:ss–m:ss). Prefer things he says/teaches repeatedly.

## Output
Write ONLY `SCRATCH/expand/gaps/chNN.md` per chapter with:
- `## Current coverage` (sections + one-line depth note each; word count).
- `## Deepen existing sections` — table: Section | What to add (specific: e.g., "worked example: grams→particles 3-step with mole map, his 'mole is the bridge' framing") | Source (deck/slide#, video id @ m:ss) | Priority (High/Med/Low) | Est. words.
- `## New sections proposed` — table: Proposed title | Placement (after x.y) | Content outline (bullets) | Source | COR item | Priority.
- `## Out of scope / skip` — slide/video topics you deliberately excluded and why.
- `## Best video moments to embed/cite` — up to 8: video id, title, m:ss, what it shows.
Be concrete and source-grounded; don't invent content he didn't teach. Final message: per-chapter counts of High-priority items and new sections proposed.
