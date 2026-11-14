# Author brief – CHEM 3A OER textbook overhaul (read fully before writing)

Adapted from `ItsDrDan/textbook/tools/AUTHOR_BRIEF.md` (CHEM 3B) using the decisions in `CLAUDE.md`. If the two disagree, `CLAUDE.md` wins.

You are writing for the revision draft of **"Introductory Chemistry, Atoms First for FCC"** on LibreTexts (Conductor project `DTvJm7TcCY`), the book for **CHEM 3A, Introductory General Chemistry, at Fresno City College**. Several FCC instructors will teach from it. Students: about 75% allied health (nursing, dental hygiene, radiologic technology, respiratory therapy); the rest biology, chemistry and engineering; many from California's Central Valley. Most have had little or no chemistry. Prerequisite math is MATH 103 or MATH 3A.

**Scope:** `tools/COR_outline.md`. Everything you write sits inside the COR unit for your chapter. Never add topics beyond it; never drop below it. Chapter plan: `tools/BLUEPRINT.md`. Sources and how each may be used: `tools/SOURCES.md`.

## What you edit

- Chapter pages are HTML **fragments** (no `<html>/<head>/<body>`) that are pasted into LibreTexts. Scripts are stripped. Keep drafts in `drafts/chNN/` named after the page, for example `drafts/ch01/1.2_classifying_matter.html`.
- Once a page has been edited directly on LibreTexts, LibreTexts is the source of truth: pull the live HTML into `drafts/` before you change it again, and never re-run an upload that could overwrite newer edits.
- **Never write to LibreTexts without Dr. Dan's go-ahead. Never touch the live book** (`Courses/Fresno_City_College/Introductory_Chemistry_Atoms_First_for_FCC`).

## Page structure

Every rewritten section:
```
<div class="box-objectives"><p class="boxtitle">Learning Objectives</p><ul>…3–5 items, each traceable to a COR line…</ul></div>
<p>lead paragraph: why this matters, ideally in a health-career or Valley setting</p>
<h2>…</h2> teaching sections, figures, tables
<div class="box-note"><p class="boxtitle">Professor Tip</p>…</div>
<div class="box-example"><p class="boxtitle">Example \(\PageIndex{1}\): …</p> Problem / Solution / Check </div>  (2–3 per section)
Try It widget (iframe, see below)
<div class="box-note"><p class="boxtitle">Clinical Connection: Nursing</p>…</div>  (or another box type)
<h2>Common Mistakes</h2> (when useful)
<h2>Summary</h2><ul>…</ul>
Attribution box
```
Chapter Guide: Learning Objectives → Key Ideas (numbered `<h3>`) → Video Lessons → Worked Examples → Common Mistakes → Practice. Do not rename existing `<h2>`/`<h3>` headings once a build script anchors on them.

Use `\(\PageIndex{n}\)` for example, figure, table and exercise numbers. Never hard-code numbers left over from source books ("Example 2.2.1").

## Box vocabulary (existing CSS only)

`box-objectives`, `box-note` with these titles, `box-example`, `box-exercise`, `figure class="figure"` + `figcaption`, `table class="mt-responsive-table"` with `<thead>`.

| Box title | Length | Rules |
|---|---|---|
| Professor Tip | 30–120 words | Teaching voice. Never "Dr. Dan says". |
| Clinical Connection: Nursing / Dental Hygiene / Radiologic Technology / Respiratory Therapy | 80–220 words | Tied to the skill just taught; medical terms defined on first use; context only, **never treatment advice or dosing instructions** (math practice with given orders is fine, framed "always follow the order and facility policy"). |
| Biology Connection: Anatomy & Physiology / Microbiology / Biology | 60–180 words | Where the chemistry shows up in the body, in cells, or in microbes. Use as often as the tie is real (Dr. Dan wants these ties wherever possible); also weave them into teaching text, examples and problems. Each chapter's planned ties are in `BLUEPRINT.md`. |
| Major Connection: Chemistry / Engineering (and biology research careers) | 50–120 words | Shorter and fewer than the clinical boxes (at most one per chapter page set unless the blueprint says otherwise). |
| Valley Connection | 120–400 words | Real, cited sources (agency or peer-reviewed; link and name the source in the box). Central Valley agriculture, water, air, dairy, local health care, careers. Tie clinical and major boxes to the Valley where it fits naturally. |
| Patient Case: Mateo | 80–200 words | Approved Case A (`tools/PATIENT_CASE_PROPOSAL.md`). Only in chapters with a strong tie (marked "Patient-case beat" in `BLUEPRINT.md`); first appears in Chapter 2. Elsewhere he may appear in a problem if it fits naturally. |
| In the Lab | 40–120 words | Points to the matching Fall 2026 lab-manual experiment. pH work uses red cabbage indicator, never a pH meter. |
| Going Further (not on CHEM 3A exams) | — | Only for material the blueprint marks beyond the COR. |

## OER standards (non-negotiable)

1. **Original prose, examples and problems.** Dr. Dan's slides, worksheets, study guides, lab manual and videos may guide alignment and language. **Exams, Skill Checks and homework are never copied**; similar problems with new numbers and new substances are fine; exact or near-exact Skill Check items are never allowed. Publisher test banks (Tro) guide difficulty only: never copy or closely paraphrase. Do not copy OpenStax, Tro, Burdge, Wikipedia or any other text.
2. **Licensing and attribution.** Book content is CC BY 4.0 unless otherwise indicated. A page adapted from an NC or SA source keeps those terms. Every rewritten page ends with an attribution box naming its sources and license, following the CHEM 3B pattern; pages that are mostly new say they were written by Dr. Dan (Daniel Kwasniewski), Fresno City College. Figure captions carry a credit. Dr. Dan's games are all rights reserved: link to them, never fold them into the licensed text.
3. **Accessibility.** Headings in order (h2 → h3, no skips); meaningful alt text on every image (describe what the figure shows and teaches); tables with `<th>` header cells and a lead-in sentence; never rely on color alone; spell out abbreviations on first use; `<details><summary>Answer</summary>` for hidden answers.
4. **Accuracy over flourish.** Run every number. Re-derive every answer. Check every clinical statement against a reliable source; hedge where evidence is soft.
5. **Scope discipline.** CHEM 3A level, per the COR. In particular: Lewis structures without formal-charge minimization; VSEPR up to four electron groups, no octet exceptions; orbital diagrams and configurations without quantum numbers ℓ, mℓ, ms; periodic trends limited to atomic radius and ionization energy (plus electronegativity for bond polarity); pH calculations only for strong acids and bases; buffers taught qualitatively (blood bicarbonate), no Henderson–Hasselbalch; equilibrium centered on Le Chatelier's principle, with K expressions and large/small K kept light; half-life with whole numbers of half-lives only; redox with simple half-reactions only (no acidic/basic balancing); activity series very light; gas density one paragraph and one example. Main path also includes enthalpy of reaction and molality tied to osmolality. Going Further pages: resonance, octet exceptions, acidic/basic redox balancing, batteries, special equilibria. Full list: "Scope decisions" in `CLAUDE.md`.

## Chemistry conventions (apply everywhere)

- **Significant figures:** trailing zeros without a decimal point are **not** significant (2500 → 2, 500 → 1, 3800 → 2). A trailing decimal point makes them significant (500. → 3, 2500. → 4). Use scientific notation for any other precision. Choose given values so their precision is unambiguous (avoid "300 K" when you mean three sig figs; write 3.00 × 10² K or 300. K).
- **Reference sheets:** the **yellow sheet** (periodic table, conversions, constants; Avogadro's number **6.0221 × 10²³**) and the **green sheet** (polyatomic ions, solubility rules, strong acids and bases). Use the values on those sheets; say "from the yellow sheet" or "from the green sheet" when a student would look something up.
- **Calculator tips** are written for the **TI-36X Pro** (for example, the `×10ⁿ` key for scientific notation, `10^x` for antilogs).
- Notation: `<sub>`/`<sup>`; entities `&rarr;` `&rlarr;` (equilibrium) `&deg;` `&ndash;` `&times;`; units with denominators written g mol⁻¹, J g⁻¹ °C⁻¹.
- **Exam-style problem format:** reactions centered on their own line; molar masses given in a small chart; data in tables; picture-based questions welcome (glassware and balance readings, accuracy vs precision targets, particle diagrams).

## Voice and style

Clear, warm, direct second person ("you"); short paragraphs; concrete before abstract; define every technical term at first use; no filler, hype or emoji. Refer to games by their current Study Hub names (source of truth: `ItsDrDan/games` → `data/hub.js`; checked 2026-11-14): Significant Figures, Prefix Power-Up (SI Prefixes), Algebra for Chemistry, Symbol Safari (Element Symbols), Polyatomic Posse (Polyatomic Ions), Name That Compound! (Naming & Formulas), Quantum Quest, Lewis Structure Studio, Reaction Rumble (Chemical Reactions), LEO Goes GER! (Redox), The Mole, Stoichiometry, Under Pressure (Gas Laws), Thermochemistry, Sticky Molecules (Intermolecular Forces), Proton Patrol (pH & Charge), Final Exam Review (Final Boss!), Lab Practical (Station Rotation). `GAMES-INDEX.md` in Study Games is older and uses some outdated names.

## Videos

Embed only Dr. Dan's own ItsDrDan YouTube videos. **Never invent a link.** Pick videos with `python3 tools/find_moment.py "<regex>" [videoId]` (searches the transcripts), then open each link, confirm the title and that the moment really teaches the point, and only then cite it. Embed: `https://www.youtube.com/embed/<id>?start=<seconds>&rel=0`; watch link: `https://youtu.be/<id>?t=<seconds>`. Check that a video's rule matches the book's conventions (for example, significant zeros) before pointing students to it; if it differs, add a one-line note.

## Medical terminology (use where natural, never forced; define on first use)

Nursing: *electrolytes* (Na⁺, K⁺, Cl⁻, Ca²⁺, HCO₃⁻), *basic metabolic panel*, *IV infusion* (normal saline 0.9% NaCl, D5W = 5% dextrose in water, lactated Ringer's), *isotonic/hypotonic/hypertonic*, *hemolysis*, *edema*, *mg/kg dosing*, *mL/h infusion rate*, *febrile/afebrile*, *hyperthermia/hypothermia*, *acidosis/alkalosis*, *antacid*.
Anatomy, physiology and microbiology (use freely, define on first use): *alveoli*, *diaphragm*, *hemoglobin*, *plasma*, *serum osmolality*, *renal* (kidney), *thermoregulation*, *homeostasis*, *hemolysis/crenation*, *aerobic/anaerobic*, *colony-forming units (CFU)*, *autoclave*, *catalase*, *disinfectant vs antiseptic*, *plasmolysis*.
Respiratory therapy: *arterial blood gas (ABG)*, *PaO₂/PaCO₂* (partial pressures), *FiO₂* (fraction of inspired oxygen), *SpO₂* (pulse-oximeter oxygen saturation), *nebulizer*, *metered-dose inhaler (MDI)*, *bronchodilator*, *hypoxemia*, *hypercapnia*, *humidification*, *hyperbaric oxygen*.
Radiologic technology: *ionizing radiation*, *gray (Gy)* and *sievert (Sv)*, *dosimeter*, *ALARA* (as low as reasonably achievable), *time–distance–shielding*, *contrast media* (barium sulfate, iodinated contrast), *technetium-99m*, *PET* (positron emission tomography), *V/Q scan*, *half-life*.
Dental hygiene: *enamel* (hydroxyapatite), *demineralization/remineralization*, *critical pH (~5.5)*, *dental caries*, *fluoride varnish*, *stannous fluoride*, *chlorhexidine*, *xerostomia* (dry mouth), *nitrous oxide–oxygen sedation*, *curing light*, *sealants*.

## Figures

- Never paste an inline SVG that contains `<text>`: LibreTexts' glossary script breaks words inside it. Upload labeled figures as SVG/PNG files attached to the page and use `<img>` with full alt text.
- Look at every figure and every page render before calling it done (preview tool copied from the 3B repo: `python3 tools/preview.py page.html out.png 900`, then read the PNG).
- Figure caption: `Figure \(\PageIndex{n}\): …` plus a credit line.

## Try It widgets

Auto-graded iframe from the CHEM 3A version of `practice.html` (to be built in this repo from the 3B widget) with 3A bank JSON files. Every choice has feedback (right and wrong). Place one after each major skill, not only at the end.

## Problems

Practice Problems page per chapter: **40–60 original problems**, numbered continuously; mix of multiple choice, numeric, compare/contrast, predict, analyze a graphic or data table, clinical-application and Valley-application items, 1–2 integrative items linking earlier chapters. **Every answer shows the reasoning**, not just the result. No exact or near-exact homework, exam or Skill Check questions.

ADAPT homework per chapter: about 50 questions, 100 points total, points per question scaled to the count, rotating (randomized) question sets, per-choice feedback for right and wrong answers, a hint on every question.

## Verification before you finish

1. Preview every page you touched and read the image: figures, tables, boxes, math.
2. Run the fragment checker (copied from the 3B repo) on every file: balanced tags, headings in order, no scripts, alt text, no external images.
3. Recompute every number with code. Re-read every clinical and Valley sentence against its source. Confirm every COR line for the chapter is taught and nothing beyond it slipped in.
4. On LibreTexts (only after go-ahead): exact string replacements that must match exactly once (abort otherwise); re-read the page after saving; check the rendered page for "Math Processing Error" or a raw `\(`.
5. Log every issue found and fixed in `tools/ISSUES_LOG.md` (page, category, priority, issue, fix, status).
6. Report back concisely: files changed, sections added, figures made, problems added (count and numbers), inaccuracies fixed, anything uncertain.
