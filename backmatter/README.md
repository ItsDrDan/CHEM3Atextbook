# Back matter: Glossary and Index data (CHEM 3A)

Data for the Glossary and Index of *Introductory Chemistry Atoms First for FCC* (CHEM 3A). These files replace the placeholder Glossary ("Sample Word 1 | Sample Definition 1") and the empty Index in the exported PDF. They are data only; nothing has been published to LibreTexts.

## Files

- `glossary_3A.json`: 350 core terms. Each entry is
  `{term, synonyms[], definition, section, source_file, going_further}`.
  - `term` is lowercase unless it is a proper name or symbol.
  - `definition` is one or two student-friendly sentences, with plain HTML `<sub>`/`<sup>` for formulas.
  - `section` is where the term is first taught, which is not always where it is first mentioned.
  - `going_further` is `true` for terms from the Going Further pages (6.11, 7.12, 13.8).
- `index_3A.json`: 425 entries, each `{term, sections[]}`.
  - The first 350 match the glossary terms. Each has up to 3 sections, and the first is the defining section.
  - The other 75 are index-only entries: named rules, equations, memory aids, people, isotopes and the book's recurring health and Valley topics. Examples are q = mcΔT, K<sub>w</sub>, HONC 1-2-3-4, technetium-99m, hydroxyapatite and the arterial blood gas.

## How they were built (2026-11-17)

1. **Term sourcing.** The bold and defined vocabulary was pulled from every section page in `drafts/chNN/`. Chapter intros, guides, practice problems and games pages were skipped.
   - Sections 1.2–1.4 and 1.9.1 are inherited LibreTexts pages that are not in `drafts`. Their terms come from the PDF text of Chapter 1, and their `source_file` reads `inherited: ...`.
   - One-off context words, box titles, step labels and clinical jargon not taught as chemistry were left out. Examples are colony, tule fog, methemoglobinemia and xerostomia.
2. **Definitions.** Each definition paraphrases or tightens the book's own defining sentence. No new claims or numbers were added. Definitions follow the "Chemistry conventions" in `CLAUDE.md`:
   - Trailing zeros without a decimal point are not significant.
   - Electronegativity difference (ΔEN): 0–0.4 is nonpolar, more than 0.4 up to 2.0 is polar covalent, and more than 2.0 is ionic.
   - The six strong acids are HCl, HBr, HI, HNO<sub>3</sub>, HClO<sub>4</sub> and H<sub>2</sub>SO<sub>4</sub>.
   - STP is 273 K and 1 atm.
   - Avogadro's number is 6.0221 × 10<sup>23</sup>.
3. **Trimming.** A first pass of about 425 terms was cut to 350. Minor terms were folded into a parent definition or moved to index-only entries. For example:
   - complete and incomplete combustion became part of "combustion"
   - adhesion and cohesion became part of "capillary action"
   - forward and reverse reactions became part of "reversible reaction"
   - pressure units became an index-only entry
4. **Self-checks** (script kept in the session scratchpad, not in the repo):
   - No duplicate headwords, compared without case. No synonym is the same as another headword.
   - Every section number is in the book's table of contents (1.1–1.13 with subsections, 2.1–2.6, …, 13.1–13.4, 13.8, 14.1–14.7).
   - For each index section, the text of that page was searched for the term or a close stem. Sections where the term was only mentioned in passing were removed.

## Counts by chapter (glossary terms, by defining section)

| Chapter | Terms |
|---|---|
| 1 | 43 |
| 2 | 28 |
| 3 | 29 |
| 4 | 15 |
| 5 | 4 |
| 6 | 28 (2 Going Further: resonance structures, radical; resonance hybrid is folded in and octet exceptions are index-only) |
| 7 | 33 (3 Going Further: galvanic cell, anode, cathode) |
| 8 | 15 |
| 9 | 41 |
| 10 | 16 |
| 11 | 30 |
| 12 | 26 |
| 13 | 14 (4 Going Further) |
| 14 | 28 |
| **Total** | **350** (9 Going Further) |

Notes on the counts:

- Chapter 5 looks small because the mole, Avogadro's number, molar mass and formula mass carry most of it. "Stoichiometry" is defined in the Chapter 8 introduction, so it is filed under 8.1.

## Notes for review

- "radical" is defined first on the Going Further page 6.11, so it is flagged `going_further`. The same idea (free radicals) is core content in 14.6, which is listed in its index entry.
- Two terms are filed under their first defining sentence, not the chapter where they are taught in depth:
  - "ionizing radiation" is filed under 2.1 (Rutherford box). It is also indexed at 3.1 and 14.2.
  - "dynamic equilibrium" is filed under 9.8 (vapor pressure). It is also indexed at 13.2.
- "acid", "base" and "salt" are defined where they are first introduced (4.1, 6.1, 6.1). Their definitions add the Chapter 12 properties. Arrhenius and Brønsted–Lowry definitions are separate entries in 12.2.
- "solution" is defined at 11.1. "homogeneous mixture" (1.5) mentions that it is also called a solution.

## License

Definitions are CC BY 4.0. They were written from Daniel Kwasniewski's text for *Introductory Chemistry Atoms First for FCC* (Fresno City College). Inherited Chapter 1 pages (1.2–1.4) keep their original CK-12 / CC BY-NC-SA source licenses. The glossary definitions for those terms are short paraphrases written for this book.
