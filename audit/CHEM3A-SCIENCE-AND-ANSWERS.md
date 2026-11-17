# CHEM 3A — Science and answer-key audit (2026-11-17)

Book: *Introductory Chemistry Atoms First for FCC — Revision Draft* (Workbench `DTvJm7TcCY`). Snapshot audited: `Full (19).pdf` (exported 2026-11-17, 1,478 pp.; active book = pp. 14–850) plus repo `drafts/`, `bank/` at `686c024`. Fixes are on branch `audit/2026-11-17-release-gate` (commits `9596f45`, next). **Nothing has been written to LibreTexts or ADAPT yet.**

## Method and honest coverage

- Seven independent reviewers (one per 1–3 chapters) read every active section page, worked example, exercise, Chapter Guide, Practice Problem and both item banks, and **recomputed every numerical answer and numeric distractor in Python** under the course conventions in `CLAUDE.md` (sig-fig rule, yellow-sheet masses with the addition rule, R = 0.082058, STP 273 K/1 atm/22.4 L, Kw 1.0 × 10⁻¹⁴, whole half-lives, C-14 5730 y). Balancing was checked by script (560 equations, every flag reviewed by hand) and every nuclear equation for A and Z.
- Bank format, confirmed in `js/fbx.js`: **choice index 0 is always the key; `k` is the calculator flag.** All 1,513 bank items (967 Try It + 546 ADAPT, Ch 1–14) were read; every key agrees with its explanation and per-choice feedback.
- Inherited Chapter 1 pages (1.2–1.4.3, 1.9.1, 1.12) exist only on LibreTexts. They were checked from the PDF, with ~22 pages rendered to read math the text layer drops.
- **Not covered:** figures were checked through rendered pages, SVG text and alt text, not re-drawn or measured. Cited external figures (Diablo Canyon CEC 2024 numbers, CGS SR 238 radon data, a "6.31 m pole-vault record set in 2026") could not be verified offline.
- Repo `bank/check_bank_chNN.py` checkers: all 14 pass before and after the fixes (`ERRORS: none`). Edited generators re-run → output identical to `bank/*.json` (ch02, ch05, ch07, ch08, ch06/10/11 ADAPT). `bank/ch01.json` is partly hand-kept (generator makes 65 of 99 items); the one Ch 1 Try It edit is in a hand-kept item.

## Totals

| Chapter | P0 | P1 | P2 | Fixed in repo | Pending (LibreTexts-only page) |
|---|---|---|---|---|---|
| 1 | 1 | 5 | 8 | 4 (F2, F3, F9, F10) + new figure for F1 | F1 (image swap), F4–F8, F11–F14, Ex. 1.2.1.3(c) |
| 2 | 0 | 1 | 5 | 5 (2-6 optional, not applied) | — |
| 3 | 0 | 0 | 1 | 1 | — |
| 4 | 0 | 0 | 3 | 3 | — |
| 5 | 0 | 0 | 3 | 3 | — |
| 6 | 0 | 0 | 3 | 3 | — |
| 7 | 0 | 0 | 3 | 3 | — |
| 8 | 0 | 1 | 2 | 3 | — |
| 9 | 0 | 0* | 1 | 1 | (*9-2 resolved by 8-1) |
| 10 | 0 | 0 | 2 | 1 (10-01 optional, not applied) | — |
| 11 | 0 | 0 | 8 | 8 | — |
| 12 | 0 | 1 | 2 | 3 | — |
| 13 | 0 | 0 | 1 | 1 | — |
| 14 | 0 | 1 | 1 | 2 | — |

**The book-written chapters are scientifically sound.** No answer key in Chapters 2–14 was wrong. The P1s are explanation errors (one backward science claim, one garbled tip, one missing definition, one inconsistent sum). The only P0 sits in an *inherited* Chapter 1 page.

## Critical and P1 corrections

| ID | Sev | Where | Wrong | Correct | Status |
|---|---|---|---|---|---|
| F1 | **P0** | 1.3.1 Example 1.3.1.3 (PDF p. 37), inherited CK-12 image | Key says "Set a is precise, but inaccurate", but target (a) shows two pairs of marks on opposite sides of the bullseye. No target shows a tight off-center group. | New original figure `figures/ch01/accuracy_targets.svg` (+ `.png`): (a) tight group off center, (b) spread around center, (c) tight on center, (d) scattered off center. Matches the existing key. Alt text included. | Figure made; **needs LibreTexts image swap** |
| — | P1 | 1.2.1 Example 1.2.1.3(c) (PDF p. 26) | "rounded to two significant figures" but shows 4.67 × 10⁻³¹ | 4.7 × 10⁻³¹ | Pending LibreTexts |
| F4 | P1 | 1.2.1 Example 1.2.1.3 (p. 26) | No final answers. Parts end at 38.7 × 10²¹ and 0.183 × 10⁴. | Add (a) 3.87 × 10²² (b) 1.83 × 10³ (c) 4.7 × 10⁻³¹ | Pending LibreTexts |
| F5 | P1 | 1.12 Density and Temperature | "100 K" and "300 K" (1 sig fig under course rule) keyed −173 °C, 27 °C | Write "100. K" and "300. K" | Pending LibreTexts |
| F6 | P1 | 1.12 Unit Conversions answers; Density and Temperature (pp. 127–130) | Broken list structure, blank lettered answers, answer "q." belongs to Q17 | Rebuild lists; number answers to match questions | Pending LibreTexts |
| F2 | P1 | ADAPT c1-h19 | Keys 19.3 g/mL from a 0.5 mL (1 sf) volume; cites "Chapter 5" for sig figs | Replacement item: 193 g, 20.0 → 30.0 mL, 19.3 g/mL | Fixed in `bank/ch01_adapt.json`; **ADAPT question needs update** |
| F3 | P1 | ADAPT c1-h21 feedback | 6.8 × 10⁴ g called "6800 g" | 68,000 g | Fixed in bank; ADAPT needs update |
| 2-1 | P1 | 2.6 Example 1 | "26.50 + 8.958 = 35.45" (sums to 35.46) | "26.496 + 8.9578 = 35.45" | Fixed |
| 8-1 | P1 | 8.5 Professor Tip; Try It c8-053 | "percent error (Chapter 1)", but Chapter 1 never teaches it (used in 8, 9.53, 10, ADAPT c8-h33) | Defined in 8.5: \|measured − accepted\| ÷ accepted × 100% | Fixed |
| 12-1 | P1 | 12.4 Professor Tip (PDF p. 690) | Prints "Use the (Use the (−) negative keyminus;) negative key" (nested markup) | "Use the **(−)** negative key" | Fixed |
| 14-1 | P1 | Problem 14.36 answer (p. 840) | "Argon … is trapped in the rock as it forms" (backward) | Argon escapes molten lava; only Ar-40 made after the rock hardens is trapped | Fixed |

## P2 corrections (all fixed in repo unless noted)

- **Ch 1:** F9 Try It c1-072 says "two" larger samples (all three are larger). F10 the 3% H₂O₂ in a first-aid kit boils near 100 °C, not 150 °C. *Pending LibreTexts:* F7 1.12 numbering 1,2,3,2,5. F8 "1 ÷ 77" needs "(exact)". F11 blood/fat densities differ between 1.9 and 1.9.1 (1.06 vs 1.035; 0.90 vs 0.918), and the symbols differ (d vs ρ). F12 temperature conversions asked in Ch 1 but taught in 9.2. F13 clinical mercury thermometer → "old-style … no longer used in patient care". F14 verify the "6.31 m pole vault record set in 2026".
- **Ch 2:** 2-2 4.00 ÷ 6.08 ratio text. 2-3 c2-007 88.9%. 2-4 c2-063 and 2-5 c2-058 intermediate sums. *2-6 optional, not applied* (ADAPT c2-h04 NH₃ data 8.23/1.77 vs ideal 8.22/1.78 would need re-keying).
- **Ch 3:** 3-1 Problem 3.17(b) energy loss 2.1 × 10⁻²⁰ J (subtracting rounded values gave 2.0).
- **Ch 4:** 4-1 B₂F₆ (not a known stable compound) → B₂Cl₄. 4-2 P₂O₃/P₂O₅ answers conflicted with the book's own "don't reduce P₄O₁₀" rule → P₄O₆ and N₂O₅. 4-3 confusing polyatomic-list sentence.
- **Ch 5:** 5-1 Fe₂O₃ 159.70 in c5-050 feedback. 5-2 Guide Ex. 2 "exactly three times". 5-3 "exactly 12 g" for a mole of C-12 (not exact since the 2019 SI).
- **Ch 6:** 6-1 ADAPT c6-h36 18.14 mol. 6-2 five molar masses re-rounded by the addition rule (answers unchanged). 6-3 chloroform is an inhaled anesthetic (a volatile liquid), not a gas.
- **Ch 7:** 7-1 c7-039 explanation equation balanced. 7-2 sacrificial-anode explanation (Mg is oxidized instead of the steel). 7-3 corrosion bullet implied amalgam is titanium/steel.
- **Ch 8:** 8-2 594 g CO₂ ≈ "about a day" of resting exhalation (book's own 200 mL/min). 8-3 Guide Ex. 2 molar masses 40.00/98.07/142.04.
- **Ch 9:** 9-1 Problem 9.47 C "(lowest to highest)".
- **Ch 10:** 10-02 ADAPT c10-h29 feedback. *10-01 optional, not applied* (Ex. 3 shows 295.2/310.2 K but computes with 295.15/310.15; answer unaffected).
- **Ch 11:** 11-01/02 BaSO₄ 233.39, Ca₃(PO₄)₂ 310.17. 11-03/04/05 three wrong-choice explanations now name the actual slip. 11-06 plasmolysis vs crenation. 11-07 buret marked every 0.1 mL, read to 0.01 mL. 11-08 ADAPT c11-h08 feedback.
- **Ch 12:** 12-2 CaSO₄(s) (gypsum) in the 12.1 Valley box. 12-3 Problem 12.2(d) stem had more than one correct pair.
- **Ch 13:** 13-1 the Ch 13 opener's alkalosis episode is now marked as a separate visit from Ch 12's acidosis ED visit.
- **Ch 14:** 14-2 not all radon progeny are alpha emitters (Pb-214, Bi-214 are beta).

Detailed rows with exact old → new strings and calculations: reviewer files copied to `audit/findings/chNN.md`.

## Health and safety statements

All clinical, IV, oxygen, nebulizer, radiation-dose and imaging statements were read. They are accurate, framed as "context only", and contain **no dosing, prescribing or patient-care instructions**. The 10 CFR 20 limit, EPA radon figures, ADA 2024 thyroid-collar statement, ABG ranges and serum osmolality range are consistent with current sources.
