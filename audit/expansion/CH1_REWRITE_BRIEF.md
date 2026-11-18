# Brief: rewrite Chapter 1's inherited measurement pages as Dr. Dan's own (writers)

Dr. Dan's instruction (2026-11-17): "make it amazing and it has to tie into nursing and health care when it comes to the
importance of measurements, including the accuracy and precision of numbers."

Chapter 1 still uses inherited open-textbook pages (CK-12 and Ball, some CC BY-NC-SA) for the measurement core. Replace each
with a page written fresh from Dr. Dan's lectures and videos, in the same style as the rest of the book. Do NOT copy or
paraphrase the inherited text: write new explanations, examples and exercises. You may keep the same topics, which the
course requires.

REPO = /Users/dan/Desktop/Study Games/github/CHEM3Atextbook
SCRATCH = /private/tmp/claude-501/-Users-dan-Desktop-Study-Games/902fb8b8-e606-48c8-860b-c64087a289e1/scratchpad

## Pages (keep these exact titles; they are live pages with fixed page ids)
| Page | Title | New draft file |
|---|---|---|
| 1.2 | Taking Measurements: Numbers and Units (section opener; short page introducing 1.2.1–1.2.2) | drafts/ch01/1.2_taking_measurements.html |
| 1.2.1 | Scientific Notation: Writing Large and Small Numbers | drafts/ch01/1.2.1_scientific_notation.html |
| 1.2.2 | The Basic Units of Measurement | drafts/ch01/1.2.2_units.html |
| 1.3 | Significant Figures (section opener introducing 1.3.1–1.3.3) | drafts/ch01/1.3_significant_figures.html |
| 1.3.1 | Significant Figures: Writing Numbers to Reflect Precision | drafts/ch01/1.3.1_sig_figs_precision.html |
| 1.3.2 | Significant Figures in Calculations | drafts/ch01/1.3.2_sig_figs_calculations.html |
| 1.4 | Conversions (section opener introducing 1.4.1–1.4.5) | drafts/ch01/1.4_conversions.html |
| 1.4.1 | Problem Solving and Unit Conversions | drafts/ch01/1.4.1_unit_conversions.html |
| 1.4.2 | Solving Multi-step Conversion Problems | drafts/ch01/1.4.2_multistep.html |
| 1.4.3 | Units Raised to a Power | drafts/ch01/1.4.3_units_powers.html |
| 1.9.1 | Density as a Conversion Factor | drafts/ch01/1.9.1_density_conversion.html |
| 1.12 | Measurements (Exercises) — rebuild as an original end-of-chapter measurement problem set | drafts/ch01/1.12_measurement_exercises.html |

The current inherited text (for topic coverage only; do not reuse wording) is in SCRATCH/chapters/ch01.txt (PDF text;
sections start at the headings "1.2: TAKING MEASUREMENTS", "1.2.1:", "1.2.2:", "1.3:", "1.3.1:", "1.3.2:", "1.4:", "1.4.1:",
"1.4.2:", "1.4.3:", "1.9.1:", "1.12:"). Keep: the accuracy-vs-precision targets figure in 1.3.1
(`https://itsdrdan.github.io/CHEM3Atextbook/figures/ch01/accuracy_targets.svg`, credit "Diagram: Daniel Kwasniewski, CC BY 4.0";
alt text describing four targets) and any other figures that are already Dr. Dan's (figures/ch01/*). Do not hotlink
non-open images.

Already-drafted neighbors (do not duplicate; cross-reference instead): 1.3.3 Reading Measuring Tools (tick-mark rule, meniscus,
balances), 1.4.4 Word Problems and Dosage Calculations, 1.4.5 Percents as Conversion Factors, 1.9 Density.

## Read first
- REPO/CLAUDE.md (conventions: sig-fig rules incl. trailing zeros without a decimal point NOT significant; exact numbers;
  the CHEM 3A yellow sheet's metric prefixes and US–metric equalities; rounding rules; calculator TI-36X Pro; clinical
  disclaimers "Context only; …"; attribution box text).
- REPO/audit/expansion/EXPAND_BRIEF.md (HTML patterns and the accuracy rules apply here too).
- REPO/audit/expansion/gaps/ch01.md: the High/Medium items marked for 1.2–1.4.3, 1.9.1 and 1.12 are your source list (his
  named zero rules incl. "sandwiched" zeros, Indiana Jones idol, underline the last significant digit and round only at the
  end, the translator analogy and T-table, start with the term that stands alone, go through the base unit, line-square-cube
  picture for cubed units, his "measure 5.0 kg of benzene" problem for 1.9.1 — but use a SAFER liquid than benzene, e.g.
  glycerol or ethanol, per Dr. Dan — prefix mnemonics, the yellow-sheet US↔metric table, whale hook, "chemistry is an applied
  math class", 8,800 vs 880 rounding, "least precise step wins", why 1 m³ ≠ 100 cm³, etc.). Read the cited slides
  (SCRATCH/expand/slides/*.txt) and video transcripts (SCRATCH/expand/videos/<id>.txt) before writing each item.
- Model pages: REPO/drafts/ch05/5.3_mass_moles_particles.html and REPO/drafts/ch01/1.4.4_word_problems_dosage.html.

## The health-care thread (required on every page)
Make measurement matter: each page gets at least one Clinical Connection box (Nursing, Pharmacy Tech, Dental Hygiene,
Radiologic Technology, Respiratory Therapy, EMS, Lab Tech) and worked examples set in health care where natural, e.g.:
- why a misplaced decimal (0.5 mg vs 5 mg) and "trailing zero / leading zero" rules matter (The Joint Commission's
  do-not-use list: never write a trailing zero like 5.0 mg on medication orders, always write a leading zero like 0.5 mg —
  explain the tension with lab sig-fig practice clearly: lab reports vs medication orders follow different rules);
- mcg vs mg vs g mix-ups; µ written as "mcg" in health care; mL vs cc; kg vs lb for weight-based dosing;
- accuracy vs precision with a calibrated vs miscalibrated scale, glucometer readings, thermometers, syringes;
- significant figures in lab values (e.g., potassium 4.1 mmol/L, hemoglobin 13.5 g/dL), and why a lab rounds;
- scientific notation in cell counts (WBC 7.5 × 10³/µL), bacterial counts, drug concentrations;
- units raised to a power: body surface area (m²), cm³ = mL in IV and syringes, mm² wound area;
- density as a conversion factor: specific gravity of urine, IV fluids, mass ↔ volume of liquid medications.
Clinical numbers must be realistic and labeled "Context only; not dosing guidance" where relevant. Keep it accurate and
current; no dosing advice.

## Each page
Same structure as other drafted pages: Learning Objectives, opener, sections, worked examples (Problem / Solution / Check,
Given/Desired where he uses it), Professor Tips (his techniques), Clinical Connection(s), Video Lesson (links/embeds to
verified moments in his videos), Try It box (reuse existing keys from REPO/bank/ch01.json only), Common Mistakes, Summary,
Exercises (3–6 with answers), Attribution box: "Written by Daniel Kwasniewski (Dr. Dan), Fresno City College, for CHEM 3A,
with AI assistance; reviewed by the author. Licensed CC BY 4.0. This page replaces an earlier adapted page; it is newly
written for this book. Video by ItsDrDan (all rights reserved; embedded, not part of the licensed text)." Section-opener pages
(1.2, 1.3, 1.4) are short (300–600 words): a health-care hook, why the section matters, and a list of its subsections.
1.12 is an original problem set (about 30–40 problems grouped by subsection, answers in <details>, MC answers explain every
wrong choice), not a copy of the old exercises.

## Accuracy
Compute every number with python3; follow CLAUDE.md conventions exactly; run `python3 REPO/tools/check_fragment.py <file>`
(no errors); check \( \) balance; `grep -nP "[\t\r]"` must find nothing (a TAB where "\t" was intended has broken MathJax
before — write files with care, e.g. use a Python script with raw strings).

## Report
Files written; word counts; list of additions with sources; health-care examples used (with any real-world values you
relied on, so they can be checked); anything unsure. Edit only the files assigned to you. Do not commit.
