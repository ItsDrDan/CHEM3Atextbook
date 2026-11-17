# CHEM 3A — Lab manual and reference sheet sync (2026-11-17)

**Companion status, verified:** the Fall 2026 lab manual exists and was read: `~/Desktop/FCC Teaching/CHEM 3A/Lab Manual/DK-Lab Manual - Chem 3A - Fall 2026.pdf`, 130 pp., dated 2026-07-31. Its contents list 12 write-ups:

0a Lab Exploration · 1a Making Measurements · 3z Found or Forgery · 4b Rolling for Compound Initiative · 5a Empirical Formula · 6a Molecular Modeling · 7a Calorimetry · 8a Determination of the Gas Constant R · 9a Solutions and Dilutions · 10a Types of Reactions · 12b Determination of Citric Acid in Soda · 12a pH of Household Items

The manual's own **Lab Practical Study Guide** (pp. 120–124) also lists **3a Electrons in Atoms**, **4a Law of Constant Composition**, **11a Synthesis of Alum**, and 8a under the title "Stoichiometric Gas Production". None of these has a write-up in the Fall 2026 manual. The Summer 2024 manual has "Electrons in Atoms" (as 2a) and "Synthesis of Alum" (11a).

Green sheet: the Chapter 6–7 reviewer checked the solubility calls against the green sheet PDF in `CHEM 3A/HandOuts/`, and they match. The yellow-sheet masses are in `tools/yellow_sheet_masses.json`; all 55 molar masses in Ch 5 and every quoted molar mass in Ch 6, 8 and 11 were recomputed from it.

## Items

| # | Location | Book says | Manual (Fall 2026) | Blocking? | Action |
|---|---|---|---|---|---|
| L1 | 3.2 "In the Lab: Experiment 3a, Electrons in Atoms" (`drafts/ch03/3.2_bohr_model.html`) | Spectroscope and discharge-tube lab, 3a | No 3a write-up (only in the practical study guide) | **Nonblocking**: the description is general and accurate. The COR lab content item 10 names "atomic emission spectra". | **Owner decision:** keep (the lab is run from a separate handout?), relabel as "the spectroscope lab", or remove the number |
| L2 | 8.5 "In the Lab: Experiment 11a, Synthesis of Alum"; Problem 8.x (11a) | Alum synthesis, percent yield | No 11a write-up in Fall 2026 (present in Summer 2024 and in the practical study guide) | Nonblocking. The COR lab content item 5 names "synthesis of a compound (e.g., alum)". | Same decision as L1 |
| L3 | 8.3 and 8.8 "Experiment 8a, Gas Production" vs 10.6 and 10.8 "Determination of the Gas Constant R" | Two titles for one lab | Contents: "Determination of the Gas Constant R"; study guide: "Stoichiometric Gas Production" | — | **Fixed in repo** (Ch 8 now uses the contents title). LibreTexts pending. |
| L4 | Ch 2 has no In the Lab box (issues-log row 32) | — | 3z "Found or Forgery" has no procedure write-up | Nonblocking | Add one when the 3z write-up exists |
| L5 | Ch 5 has no In the Lab box (row 41) | — | No mole-specific lab | Not an issue | — |
| L6 | 4b "Rolling for Compound Initiative" (4.6), 5a (6.7), 6a (6.3/6.4), 7a (9.4/9.5), 9a (11.4), 10a (7.x), 12a (12.1/12.8), 12b (11.5/12.8) | Names and descriptions | Match the contents titles | — | OK |
| L7 | 12.x lab uses red cabbage indicator (CLAUDE.md: never a pH meter) | Red cabbage | 12a uses red cabbage | — | OK |

**Proposed check once the manual is final:** rerun `grep -rnoE 'Experiment [0-9]+[a-z]' drafts/` against the final contents and update L1 and L2.
