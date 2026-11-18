# Hints and explanations pass (2026-11-17)

Dr. Dan asked that every question in the book explain why the right answer is right and why each wrong answer is wrong,
with hints that guide students.

| Question type | Before | After |
|---|---|---|
| Try It + ADAPT banks (1,644 items) | every item already had per-choice reasons, a hint and a worked answer; 207 wrong-choice reasons only named the mistake | those 207 now name the mistake **and** the fix (verified numerically); c11-h24 corrected after review |
| Page exercises and practice problems (1,398) | answers everywhere, every multiple-choice answer already explained each wrong letter; **no hints**; 49 answers gave a bare result | a Hint (details/summary) above every Answer; a "why" sentence added to the 49 terse answers |

Process: per-chapter writers (`HINT_BRIEF.md`) filled `chNN_hints.json` from `chNN_exercises.json`; `check_hints.py` checked
format, length and leaked answer values; `apply_hints.py` inserted them (idempotent). Independent review of a random sample
(168 hints, 49 whys, 40 bank reasons): no wrong chemistry; 11 hints gave too much away (multiple-choice concept items), so all
362 multiple-choice and factor hints were swept (`mc_sweep.json`) and 55 more were rewritten as guiding questions.
Wording fixes found along the way: 1.11 Problem 1.17(d) rounding 99.96; 4.2 and 4.8 "one less negative" for adding H⁺.

## Published 2026-11-17
- GitHub Pages: banks with the fuller reasons live (f0becc1).
- LibreTexts: 118 pages published from f0becc1 after a live-equals-previous check; every page read back with all its hints (1,398 total).
- ADAPT: 164 questions updated in place in the 14 chapter assignments (wrong-choice feedback only; reason "Wrong-answer feedback now gives the fix as well as the mistake (2026-11-17)."), each read back; no assignment has a pending revision.

## Print rule 2026-11-18
- Every exercise page starts with a print-only style (`details > summary { break-after: avoid }`) so a Hint or Answer label never ends a printed page. Tested on 1.3.2 (PDF: no stranded labels), then added to all 118 pages (149e514) and published; every live page has the rule once and its text matches the repo.
- New exercise pages need the same first line.
