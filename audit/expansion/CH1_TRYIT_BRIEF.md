# Brief: new Chapter 1 Try It question sets (writers)

Goal (Dr. Dan, 2026-11-17): give each Chapter 1 measurement page its own Try It pool. Today 1.2.1–1.2.2 share 11 items,
1.3.1–1.3.3 share 12 and 1.4.1–1.4.5 share 11 (1.4.5 Percents has no matching item at all). Gap analysis:
`audit/expansion/INTERACTIVES_GAP.md` §1–2.

REPO = /Users/dan/Desktop/Study Games/github/CHEM3Atextbook

## New topic keys

| Key | Page (draft file) | Items | Writer |
|---|---|---|---|
| `ch01-scinot` | 1.2.1 Scientific Notation (`drafts/ch01/1.2.1_scientific_notation.html`) | 12 | A |
| `ch01-sigcalc` | 1.3.2 Significant Figures in Calculations (`1.3.2_sig_figs_calculations.html`) | 10 | A |
| `ch01-read` | 1.3.3 Reading Measuring Tools (`1.3.3_reading_tools.html`) | 10, at least 6 with a picture | A |
| `ch01-multistep` | 1.4.2 Multi-step Conversions (`1.4.2_multistep.html`) | 8 | B |
| `ch01-powers` | 1.4.3 Units Raised to a Power (`1.4.3_units_powers.html`) | 8 | B |
| `ch01-dosage` | 1.4.4 Word Problems and Dosage Calculations (`1.4.4_word_problems_dosage.html`) | 10 | B |
| `ch01-percent` | 1.4.5 Percents as Conversion Factors (`1.4.5_percents.html`) | 8 | B |

Read the page first: every item must test what that page teaches, with its methods and wording (Given/Desired, T-table,
"go through the base unit", underline-then-round-at-the-end, etc.). Read `bank/ch01.json` (items c1-066 to c1-099 are the
current measurement items) and do NOT duplicate them or the page's own worked examples/exercises: new numbers and contexts.

## Item format (one dict per item; the merger adds ids)
```python
dict(t="ch01-scinot", q="question HTML", c=[correct, wrong1, wrong2, wrong3], y=[why correct, why wrong1, why wrong2, why wrong3],
     h="hint (a nudge, not the answer)", w="worked explanation; the answer in <b>…</b>", d=1|2|3, k=0|1, f=[figure] (optional))
```
- **c[0] is always the correct answer** (the widget shuffles). Exactly 4 choices, all different, same format and units.
- y[i] explains choice i: for wrong choices name the actual mistake (the distractors must come from real student mistakes:
  decimal moved the wrong way, factor upside down, squared the number but not the unit, rounded too early, percent of the
  wrong total, wrong number of sig figs, read the meniscus top, read a buret upward, …).
- k = 1 when a calculator is needed. d: 1 recall/one step, 2 two steps, 3 multi-step.
- HTML: `<b> <i> <sub> <sup> <br />` only, balanced; use entities (`&times; &minus; &micro; &divide; &rarr; &deg; &nbsp;`);
  no bare `&`. No "all/none of the above".
- About half the items set in health care (nursing, pharmacy tech, dental hygiene, radiologic tech, respiratory therapy, lab
  tech, EMS), the rest lab / everyday / Central Valley. Every dosing or clinical-math item starts with
  `<b>Math practice only; always follow the order and facility policy.</b>` Clinical values must be realistic.
- Values: CHEM 3A yellow sheet (`tools/yellow_sheet_conversions.md`; only 1 in = 2.54 cm and 1 cal = 4.184 J are exact;
  1 lb = 453.59 g, 1 kg = 2.2046 lb). Health-care equalities such as 1 tsp = 5 mL may be given in the question.
- Sig-fig rules (CLAUDE.md): trailing zeros without a decimal point are NOT significant (2500 → 2); a trailing decimal point
  makes them significant (500. → 3); counted and defined numbers are exact; round only at the end; ×/÷ → fewest sig figs,
  +/− → fewest decimal places. Answers keep the right sig figs; use scientific notation when the sig figs need it.
- Exams, Skill Checks, homework and publisher test banks are never copied.

## Figures (ch01-read)
Supported by the widget (`js/fbx.js` fScale), drawn exactly at the value you give:
- `{"type":"cylinder","lo":10,"hi":20,"minor":0.5,"major":2,"level":16.3,"unit":"mL"}` (level = bottom of meniscus)
- `{"type":"buret","lo":12,"hi":15,"minor":0.1,"major":1,"level":13.62,"unit":"mL"}` (numbers increase downward)
- `{"type":"ruler","lo":0,"hi":5,"minor":0.1,"major":1,"half":0.5,"start":0,"len":3.47,"unit":"cm"}`
- `{"type":"balance","read":"12.470"}` (digital readout text, grams implied; say the unit in the question)
Rules: state the mark spacing in the question; the correct reading has exactly one estimated digit beyond the smallest mark,
and the level you draw must be readable to that digit (e.g., cylinder marks 0.5 mL apart → read to 0.1 mL; put the level at
a value like 16.3, not 16.25). Use ranges where major marks get labels (the widget labels every `major`).
A screen-reader user cannot see the picture, so the question text must not depend on a color, and each picture item should
still name the tool and mark spacing.

## Output
Write `tools/bank_ch01_new_<A|B>.py` defining `ITEMS = [dict(...), ...]`. Compute every number in the file with Python and
`assert` the correct choice and each numeric distractor match the computation (as strings, with the stated rounding).
Run it (`python3 -I tools/bank_ch01_new_A.py` should print the count and pass). Edit no other file. Do not commit.
Report: count per key, any value you were unsure of, and anything in the page that looked wrong.
