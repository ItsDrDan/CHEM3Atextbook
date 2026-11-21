# Try It pool depth (2026-11-20)

Read-only. Nothing was changed. Counted from `bank/chNN.json` (the files the widget loads; `chNN_adapt.json` is ADAPT only)
and the Try It frames in `drafts/`.

## Pool sizes are healthy

1,068 questions in 94 topics (8 to 26 per topic, median 11). No topic has fewer than 8, and no teaching-page box has fewer
than 6 questions. Every question has 4 choices, with no duplicate choices. The "diluted" pools flagged on 2026-11-17 in
`audit/expansion/INTERACTIVES_GAP.md` have been fixed.

## The real problem: pages that share a topic show the same questions

`js/widget.js` picks a box's questions by hashing each question id with the topic list. It does not use the page or the box
size, so two boxes with the same `t=` get the same order, and the smaller box is a subset of the larger one.

| Pages | Shared topic | Repeats | What the student sees |
|---|---|---|---|
| 7.1 → 7.2 | `ch07-equations` (12) | all 8 of 7.1 | 7.1 asks 4 balancing questions before balancing is taught. 7.2 adds only 2 new questions, and only 5 of its 10 are balancing. |
| 6.2 → 6.3 | `ch06-lewis` (13) | all 8 of 6.2 | 6.2 (bonds) asks for valence-electron counts and full Lewis structures before 6.3 teaches the method. 6.3 adds only 2 new. |
| 1.9 → 1.9.1 | `ch01-density` (11) | all 6 | The two boxes are identical. No question in the topic uses density as a conversion factor, which is the skill of 1.9.1. |

Smaller overlaps are expected, because those boxes are review mixes: 5.5 with 5.3/5.4 (3 each), 6.5 with 6.4 (3), and the
parent pages 1.2, 1.3 and 1.4 with their subsections (1 to 4 each).

Open question: the parent pages 1.2, 1.3 and 1.4 come before their subsections but draw on all of them, so a student who
tries the box first meets skills not yet taught.

## Proposed fix

Use the widget's existing `ids=` setting to give each page its own questions, and add new questions where a page has too few:

| Page | Existing questions | New questions needed |
|---|---|---|
| 7.1 | c7-001 to c7-006 (6) | 0 |
| 7.2 | c7-007 to c7-012 (6) | about 4 balancing |
| 6.2 | bond-count and shared-pair items | about 5 |
| 6.3 | valence-count and Lewis items | 0 |
| 1.9 | existing `ch01-density` | 0 |
| 1.9.1 | none | about 8 |

About 17 new questions, each with a hint and a reason for every choice, checked by running the math.

## Count to correct in the review packet

`review/01_DEPARTMENT_SUMMARY.md` says "about 290 boxes." The drafts have **146 Try It frames on 130 pages**; 290 looks like
frames plus their "open in a new tab" links. The 1,068-question count is correct.

## Fix built (2026-11-20, Dr. Dan: "Yes, write them"; not pushed or published yet)

`tools/bank_page_splits.py` added 17 questions (c1-166 to c1-173, c6-067 to c6-071, c7-074 to c7-077; 1,085 in all), each with
a hint, a worked answer and a reason for all four choices. Its arithmetic is asserted in the script, and the four balancing
questions are solved independently by `tools/check_bank_ch07.py` (new specs added). The Chapter 1, 6 and 7 checkers report
no new errors; the older Chapter 6 and 7 notes they print are unchanged.

| Page | Questions shown | From |
|---|---|---|
| 1.9 | 6 | c1-055 to c1-065 |
| 1.9.1 | 8 | c1-166 to c1-173 (new) |
| 6.2 | 7 | c6-017, c6-022, c6-067 to c6-071 (5 new) |
| 6.3 | 10 | c6-010 to c6-016, c6-018 to c6-021 |
| 7.1 | 6 | c7-001 to c7-006 |
| 7.2 | 10 | c7-007 to c7-012, c7-074 to c7-077 (4 new) |

No question appears on two of these pages. All six boxes load at 328 px with the right count and no script errors. Real taps
in iPhone Safari (iPhone 17 simulator, local copy in a frame) on the 1.9.1 box: a wrong choice gets its specific explanation.
Choice order is shuffled (30 loads: the right answer in all four positions). Publish order: push `bank/` first, then
update the six live pages using `audit/TRYIT_PAGE_SWAPS_2026-11-20.json`. A student's saved progress in these six boxes restarts.
