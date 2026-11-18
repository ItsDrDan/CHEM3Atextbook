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
