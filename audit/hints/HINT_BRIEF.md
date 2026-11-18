# Brief: a hint for every exercise and practice problem (writers)

Dr. Dan (2026-11-17): every question in the book should explain why the right answer is right and why each wrong answer is
wrong, with hints that guide students. Instructors and students praise the games most for their explanations. The Try It
and ADAPT banks already have hints; the 1,398 exercises and practice problems on the pages have none.

REPO = /Users/dan/Desktop/Study Games/github/CHEM3Atextbook

## Input
`audit/hints/chNN_exercises.json`: one record per exercise, in page order: `file`, `idx` (its position among the page's
exercise boxes), `title`, `question` (plain text), `answer` (plain text of the hidden answer), `mc` (multiple choice),
`terse_answer` (true when the answer is a bare result with no reasoning).

Read the section page itself (`file`) for the method and wording each hint should point to (Given/Desired, the T-table,
"go through the base unit", "the goal is the mole", the green sheet, SNAP, Le Chatelier, etc.). CLAUDE.md "Chemistry
conventions" applies.

## What to write, per exercise
1. **hint** (every exercise): 1–2 sentences, at most about 35 words, that get a stuck student moving without giving the
   answer away.
   - Point to the first step, the key idea or the right tool ("Start with the quantity that stands alone", "Which ion
     has a fixed charge?", "Write the K expression first: products over reactants", "Find moles first; the goal is the mole").
   - Never state the final answer, the correct letter, or a number that is the answer. Do not just restate the question.
   - Multi-part problems: one hint may cover the parts, or give "(a) … (b) …" briefly.
   - Multiple choice: a hint may help eliminate (e.g., "Which choices have the units the question asks for?").
   - Use the book's own words for its methods and point to a section only when it helps ("see the cue-word table in 5.3").
   - Clinical problems: hints are about the math, never about patient care.
2. **why** (only when `terse_answer` is true): one sentence to add after the existing answer that says *why* it is right
   (the rule or step), e.g., "Potassium is in Group 1 (1+) and sulfide is 2−, so two K⁺ balance one S²⁻." Must agree with
   the existing answer; do not change the answer.

Do not edit any HTML file. Check your chemistry: a hint must be true and must lead to the book's answer.

## Output
Write `audit/hints/chNN_hints.json`: a list with one object per exercise, in the same order as the input:
`{"file": ..., "idx": ..., "title": ..., "hint": "...", "why": "..." or ""}`. Plain text with these HTML pieces allowed:
`<sub> <sup> <b> <i>` and entities (`&rarr; &times; &minus; &deg;`); MathJax `\( … \)` is allowed for a short expression.
No bare `&`, no TAB characters. Then run `python3 -I audit/hints/check_hints.py audit/hints/chNN_hints.json` and fix
anything it reports. Report: counts, anything in an existing answer that looked wrong (do not fix it; list file, title, issue).
