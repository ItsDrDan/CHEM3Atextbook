# CHEM 3A textbook: interactive practice gap analysis

Analysis only, 2026-11-17. Sources: `drafts/chNN/*.html` (iframes parsed), `bank/chNN.json` (items counted per topic key `t`), the game clones in `~/Desktop/Study Games/github/`, the hub registry `games/data/hub.js`, and PhET URLs checked with HTTP requests on 2026-11-17.

**Totals.** 986 Try It items in 87 topic keys. Every teaching section from 1.1 to 14.7 has a Try It box. There are 19 Explore It boxes on 17 pages (18 from the CLAUDE.md list, plus PhET pH Scale in 12.5). Every teaching page has 1–3 Dr. Dan videos. Each chapter has a Practice Games page.

**How to read the tables.** "Shared" means one topic key feeds several pages, so each page draws on the same small pool. "Diluted" means 12 or fewer items shared across 3 or more pages. "Thin" means fewer than 8 items. Chapter guides, practice-problem pages and Practice Games pages are left out of the rows. Their Try It boxes only mix the section keys again.

## 1. Inventory by chapter

### Chapter 1

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 1.0 chapter intro | — | — | 1 | intro page |
| 1.1 scientific method | `ch01-method` (11) | — | 1 |  |
| 1.2 taking measurements | — | — | 1 | **NO interactive** |
| 1.2.1 scientific notation | `ch01-units` (11; shared by 2 pages) | — | 1 | shared |
| 1.2.2 units | `ch01-units` (11; shared by 2 pages) | — | 1 | shared |
| 1.3 significant figures | — | — | 0 | **NO interactive** |
| 1.3.1 sig figs precision | `ch01-sigfig` (12; shared by 3 pages) | — | 1 | diluted (12/3 pages) |
| 1.3.2 sig figs calculations | `ch01-sigfig` (12; shared by 3 pages) | — | 2 | diluted (12/3 pages) |
| 1.3.3 reading tools | `ch01-sigfig` (12; shared by 3 pages) | — | 1 | diluted (12/3 pages) |
| 1.4 conversions | — | — | 1 | **NO interactive** |
| 1.4.1 unit conversions | `ch01-convert` (11; shared by 5 pages) | — | 1 | diluted (11/5 pages) |
| 1.4.2 multistep | `ch01-convert` (11; shared by 5 pages) | — | 1 | diluted (11/5 pages) |
| 1.4.3 units powers | `ch01-convert` (11; shared by 5 pages) | — | 1 | diluted (11/5 pages) |
| 1.4.4 word problems dosage | `ch01-convert` (11; shared by 5 pages) | — | 1 | diluted (11/5 pages) |
| 1.4.5 percents | `ch01-convert` (11; shared by 5 pages) | — | 1 | diluted (11/5 pages) |
| 1.5 classifying matter | `ch01-classify` (11) | — | 1 |  |
| 1.6 states of matter | `ch01-states` (10) | — | 1 |  |
| 1.7 electric charge | `ch01-charge` (10) | — | 1 |  |
| 1.8 properties and changes | `ch01-change` (12) | — | 1 |  |
| 1.9 density | `ch01-density` (11; shared by 2 pages) | `labpractical/?mode=vlab&labs=1a` | 1 | shared |
| 1.9.1 density conversion | `ch01-density` (11; shared by 2 pages) | — | 1 | shared |

Practice Games page embeds/links: `finalexam/?course=3A`, `sigfig/`, `metric/`, `elements/`

### Chapter 2

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 2.0 chapter intro | — | — | 1 | intro page |
| 2.1 atomic theory | `ch02-theory` (10) | — | 1 |  |
| 2.2 subatomic particles | `ch02-particles` (11) | — | 1 |  |
| 2.3 periodic table | `ch02-table` (11) | — | 1 |  |
| 2.4 ions | `ch02-ions` (11) | — | 1 |  |
| 2.5 isotopes | `ch02-isotopes` (11) | `labpractical/?mode=bench&labs=2a` | 1 |  |
| 2.6 atomic mass | `ch02-mass` (10) | `labpractical/?mode=vlab&labs=2a` | 1 |  |

Practice Games page embeds/links: `finalexam/?course=3A`, `elements/`

### Chapter 3

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 3.0 chapter intro | — | — | 1 | intro page |
| 3.1 light | `ch03-light` (12) | — | 1 |  |
| 3.2 bohr model | `ch03-bohr` (9) | `labpractical/?mode=bench&labs=3a` | 1 |  |
| 3.3 orbitals | `ch03-orbitals` (11) | — | 1 |  |
| 3.4 electron configurations | `ch03-config` (12) | — | 1 |  |
| 3.5 valence electrons | `ch03-valence` (10) | — | 2 |  |
| 3.6 periodic trends | `ch03-trends` (10) | — | 1 |  |

Practice Games page embeds/links: `quantumchemistry/?course=3A`, `finalexam/?course=3A`

### Chapter 4

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 4.0 chapter intro | — | — | 1 | intro page |
| 4.1 formulas and types | `ch04-formulas` (10; shared by 2 pages) | — | 1 | shared |
| 4.2 ionic formulas | `ch04-ionicformula` (12; shared by 2 pages), `ch04-polyatomic` (10; shared by 2 pages) | — | 3 | shared |
| 4.3 naming ionic | `ch04-ionicname` (14; shared by 2 pages) | — | 2 |  |
| 4.4 naming molecular | `ch04-molecular` (10; shared by 2 pages) | — | 1 | shared |
| 4.5 naming acids | `ch04-acids` (10; shared by 2 pages) | — | 1 | shared |
| 4.6 naming any compound | `ch04-formulas` (10; shared by 2 pages), `ch04-ionicformula` (12; shared by 2 pages), `ch04-polyatomic` (10; shared by 2 pages), `ch04-ionicname` (14; shared by 2 pages), `ch04-molecular` (10; shared by 2 pages), `ch04-acids` (10; shared by 2 pages) | — | 0 | shared |

Practice Games page embeds/links: `polyatomic/?course=3A`, `ionicformula/?course=3A`, `finalexam/?course=3A`

### Chapter 5

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 5.0 chapter intro | — | — | 1 | intro page |
| 5.1 the mole | `ch05-mole` (12) | — | 1 |  |
| 5.2 molar mass | `ch05-molarmass` (16) | — | 1 |  |
| 5.3 mass moles particles | `ch05-convert` (16; shared by 2 pages) | — | 2 |  |
| 5.4 moles within formula | `ch05-formula` (16; shared by 2 pages) | — | 1 |  |
| 5.5 putting it together | `ch05-convert` (16; shared by 2 pages), `ch05-formula` (16; shared by 2 pages) | — | 1 |  |

Practice Games page embeds/links: `moles/?course=3A`, `finalexam/?course=3A`

### Chapter 6

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 6.0 chapter intro | — | — | 1 | intro page |
| 6.1 ionic bonding | `ch06-ionic` (9) | — | 1 |  |
| 6.2 covalent bonds | `ch06-lewis` (13; shared by 2 pages) | — | 1 |  |
| 6.3 lewis structures | `ch06-lewis` (13; shared by 2 pages) | — | 1 |  |
| 6.4 vsepr | `ch06-vsepr` (12; shared by 2 pages) | `labpractical/?mode=bench&labs=6a` | 1 | shared |
| 6.5 polarity | `ch06-polarity` (12), `ch06-vsepr` (12; shared by 2 pages) | — | 2 | shared |
| 6.6 percent composition | `ch06-percent` (10) | — | 1 |  |
| 6.7 empirical molecular | `ch06-empirical` (10) | — | 1 |  |
| 6.11 going further | — | — | 0 | Going Further (optional) |

Practice Games page embeds/links: `lewisstructures/?course=3A`, `moles/?course=3A`, `finalexam/?course=3A`

### Chapter 7

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 7.0 chapter intro | — | — | 1 | intro page |
| 7.1 chemical equations | `ch07-equations` (12; shared by 2 pages) | — | 2 | shared |
| 7.2 balancing | `ch07-equations` (12; shared by 2 pages) | `labpractical/?mode=bench&labs=10a` | 2 | shared |
| 7.3 reaction patterns | `ch07-types` (10) | — | 2 |  |
| 7.4 solubility | `ch07-solubility` (10) | — | 2 |  |
| 7.5 precipitation | `ch07-netionic` (10) | `labpractical/?mode=vlab&labs=10a` | 1 |  |
| 7.6 acid base gas | `ch07-acidgas` (9) | — | 1 |  |
| 7.7 redox | `ch07-redox` (12) | — | 1 |  |
| 7.8 activity series | `ch07-activity` (7) | — | 1 | thin (7) |
| 7.12 going further | — | — | 0 | Going Further (optional) |

Practice Games page embeds/links: `reactions/?course=3A`, `redox/?course=3A`, `finalexam/?course=3A`

### Chapter 8

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 8.0 chapter intro | — | — | 1 | intro page |
| 8.1 mole ratios | `ch08-moleratio` (11) | — | 1 |  |
| 8.2 mass to mass | `ch08-massmass` (13) | — | 2 |  |
| 8.3 solutions gases | `ch08-solgas` (10) | — | 1 |  |
| 8.4 limiting reactant | `ch08-limiting` (12) | `labpractical/?mode=bench&labs=11a` | 1 |  |
| 8.5 percent yield | `ch08-yield` (10) | — | 1 |  |
| 8.6 enthalpy | `ch08-enthalpy` (10) | — | 1 |  |

Practice Games page embeds/links: `stoichiometry/?course=3A`, `finalexam/?course=3A`

### Chapter 9

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 9.0 chapter intro | — | — | 1 | intro page |
| 9.1 energy | `ch09-energy` (7) | — | 1 | thin (7) |
| 9.2 temperature | `ch09-temp` (10) | — | 1 |  |
| 9.3 heat units | `ch09-units` (8) | — | 1 |  |
| 9.4 specific heat | `ch09-specheat` (11) | `labpractical/?mode=bench&labs=7a` | 1 |  |
| 9.5 phase changes | `ch09-phase` (10) | `IMF/?course=3A&mode=curve` | 2 |  |
| 9.6 imf | `ch09-imf` (10) | `IMF/?course=3A&mode=lab`<br>`IMF/?course=3A&mode=well` | 2 |  |
| 9.7 liquids solids | `ch09-solids` (7) | — | 1 | thin (7) |
| 9.8 vapor pressure ranking | `ch09-vapor` (9) | — | 1 |  |

Practice Games page embeds/links: `thermochemistry/?course=3A`, `IMF/?course=3A`, `finalexam/?course=3A`

### Chapter 10

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 10.0 chapter intro | — | — | 1 | intro page |
| 10.1 kmt | `ch10-kmt` (9) | — | 1 |  |
| 10.2 pressure | `ch10-pressure` (10) | — | 1 |  |
| 10.3 gas laws | `ch10-laws` (15) | `labpractical/?mode=bench&labs=8a` | 2 |  |
| 10.4 ideal gas law | `ch10-ideal` (13) | — | 1 |  |
| 10.5 gas stoichiometry | `ch10-stoich` (11) | — | 1 |  |
| 10.6 dalton | `ch10-dalton` (12) | `labpractical/?mode=vlab&labs=8a` | 1 |  |

Practice Games page embeds/links: `gaslaws/?course=3A`, `finalexam/?course=3A`

### Chapter 11

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 11.0 chapter intro | — | — | 1 | intro page |
| 11.1 solutions form | `ch11-dissolve` (10) | `IMF/?course=3A&mode=mix` | 1 |  |
| 11.2 solubility t p | `ch11-solubility` (10) | — | 1 |  |
| 11.3 concentration | `ch11-conc` (14) | — | 2 |  |
| 11.4 molarity dilution | `ch11-dilution` (14) | `labpractical/?mode=vlab&labs=9a` | 1 |  |
| 11.5 titration | `ch11-titration` (12) | `labpractical/?mode=vlab&labs=12b` | 1 |  |
| 11.6 colligative | `ch11-colligative` (12) | `IMF/?course=3A&mode=solutions`<br>`IMF/?course=3A&mode=cell` | 1 |  |

Practice Games page embeds/links: `stoichiometry/?course=3A`, `IMF/?course=3A`, `finalexam/?course=3A`

### Chapter 12

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 12.0 chapter intro | — | — | 1 | intro page |
| 12.1 properties | `ch12-props` (10) | `labpractical/?mode=vlab&labs=12a` | 1 |  |
| 12.2 bronsted lowry | `ch12-bl` (12) | — | 2 |  |
| 12.3 strong weak | `ch12-strength` (12) | — | 1 |  |
| 12.4 water kw | `ch12-water` (12) | — | 1 |  |
| 12.5 ph | `ch12-ph` (16) | `labpractical/?mode=bench&labs=12a` | 2 |  |
| 12.6 buffers | `ch12-buffers` (10) | — | 1 |  |

Practice Games page embeds/links: `finalexam/?course=3A`, `reactions/?course=3A`

### Chapter 13

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 13.0 chapter intro | — | — | 1 | intro page |
| 13.1 rates | `ch13-rates` (16) | — | 1 |  |
| 13.2 dynamic | `ch13-dynamic` (12) | — | 1 |  |
| 13.3 k | `ch13-k` (16) | — | 1 |  |
| 13.4 le chatelier | `ch13-lechat` (26) | — | 2 |  |
| 13.8 going further | — | — | 1 | Going Further (optional) |

Practice Games page embeds/links: `finalexam/?course=3A`

### Chapter 14

| Section (draft file) | Try It key (items) | Explore It | Videos | Flag |
|---|---|---|---|---|
| 14.0 chapter intro | — | — | 1 | intro page |
| 14.1 radioactivity | `ch14-radiation` (10) | — | 1 |  |
| 14.2 decay | `ch14-decay` (18) | — | 2 |  |
| 14.3 half life | `ch14-halflife` (16) | — | 1 |  |
| 14.4 radiocarbon | `ch14-dating` (10) | — | 1 |  |
| 14.5 fission fusion | `ch14-fission` (8) | — | 1 |  |
| 14.6 radiation health | `ch14-health` (7) | — | 1 | thin (7) |
| 14.7 medicine | `ch14-medicine` (6) | — | 1 | thin (6) |

Practice Games page embeds/links: `finalexam/?course=3A`
## 2. Gaps

**A. Chapter 1 measurement skills have the thinnest practice in the book, and they matter most for allied-health students.**
- 1.2.1 (scientific notation) and 1.2.2 (units) share `ch01-units` (11 items). Only about 6 of those are scientific-notation items.
- 1.3.1, 1.3.2 and 1.3.3 share `ch01-sigfig` (12 items). 1.3.3 Reading Measuring Tools gets only 3 picture items (cylinder, ruler, buret). None of its thermometer or balance subsections has a matching item.
- Five pages (1.4.1–1.4.5) share `ch01-convert` (11 items).
  - 1.4.4 Dosage has 2 matching items (mg/kg, IV rate).
  - 1.4.5 Percents has **0**.
  - 1.4.3 Units with powers has 2.
- The parent pages 1.2, 1.3 and 1.4 have no interactive at all.
- Chapter 1 has no simulation for sig figs, glassware reading, scientific notation or conversions. Its only Explore It box is the density vlab in 1.9.
- The Chapter 1 Try It boxes have no `&game=` link, so they show no "Play Sig Fig Sleuth / Prefix Power-Up" button. Every other chapter's boxes have one.

**B. Thin keys (fewer than 8 items):** `ch07-activity` 7 (7.8), `ch09-energy` 7 (9.1), `ch09-solids` 7 (9.7), `ch14-health` 7 (14.6), `ch14-medicine` 6 (14.7). Borderline (8–9): `ch09-units` 8, `ch14-fission` 8, `ch03-bohr` 9, `ch06-ionic` 9, `ch07-acidgas` 9, `ch09-vapor` 9, `ch10-kmt` 9.

**C. No simulation where one would clearly help (COR skill → section):**

| Skill | Section | What exists now | What could fill it |
|---|---|---|---|
| Sig figs / reading glassware | 1.3.3 | Try It only | labpractical vlab 0a (verified); sigfig `glass` topic (needs a link) |
| Scientific notation, unit conversion | 1.2.1, 1.4.x | Try It only | No sim needed. Link sigfig/metric/algebratrainer from the box. |
| Atomic structure, ions | 2.2, 2.4 | Try It only | PhET Build an Atom |
| Ionic formulas, polyatomic ions | 4.2 | Try It only | ionicformula Free Builder, polyatomic Ion Builder (no deep link) |
| Mass ↔ moles ↔ particles | 5.3 | Try It only | moles Mole Machine (no deep link) |
| Lewis structures | 6.3 | Try It only | labpractical vlab 6a "Build a Model" (verified, unused) |
| Polarity | 6.5 | Try It only | PhET Molecule Polarity |
| Net ionic | 7.5 | vlab 10a | reactions Mixing Bench (no deep link) |
| Limiting reactant | 8.4 | bench 11a (PhET RPL) | stoichiometry tray lab questions (no deep link) |
| KMT, gas laws | 10.1, 10.3 | bench 8a in 10.3 | gaslaws Piston Lab (no deep link); PhET Gases Intro |
| Molarity | 11.3 | Try It only | labpractical bench 9a (PhET Molarity + Beer's Law, verified, unused); PhET Concentration |
| Strong vs weak acids | 12.3 | Try It only | PhET Acid-Base Solutions |
| Le Chatelier | 13.4 | Try It only (26 items, the best-stocked key) | **Nothing exists.** No HTML5 PhET (Reactions & Rates returns 404 as HTML5) and no Dr. Dan game. |
| Half-life, decay | 14.2, 14.3 | Try It only | PhET Alpha Decay, Beta Decay, Build a Nucleus (HTML5, verified) |

**D. Chapters 13 and 14 have no game.** Their Practice Games pages offer only Final Boss. The hub (`games/data/hub.js`) also lists no game for these two chapters.

## 3. Recommendations (ranked by impact ÷ effort)

### (a) Embed now: deep links verified in the code (no game change)

1. **1.3.3 Reading Measuring Tools:** `https://itsdrdan.github.io/labpractical/?mode=vlab&labs=0a`. This is the Water Density Challenge: tare, fill to target, read the meniscus. `BENCH_WATER` has `labs: ['0a','1a']` (labpractical `index.html` ~3862). The `labs=0a` link is accepted by the regex `^\d{1,2}[a-z]$` at line 4473.
2. **6.3 Lewis Structures:** `https://itsdrdan.github.io/labpractical/?mode=vlab&labs=6a`. This is the "Build a Model" bench (`BENCH_MODEL`, ~3827). Steps: count valence electrons, build the Lewis structure, count electron groups, find the shape and angle. The 6.4 box already uses bench 6a (PhET Molecule Shapes), so this one is different.
3. **11.3 Concentration (Molarity subsection):** `https://itsdrdan.github.io/labpractical/?mode=bench&labs=9a`. This opens PhET Molarity and Beer's Law Lab with graded tasks (`PHET` ids `molarity`, `beers`). It is not used anywhere in the book now.
4. **9.5 Phase Changes (Going Further: phase diagrams):** `https://itsdrdan.github.io/IMF/?course=3A&mode=diagram`. This opens the Phase Diagram Explorer. `init()` in `IMF/index.html:3684` allows `diagram` for 3A, because `TOPICS.curve.courses` = 3A, 1A.
5. **1.9.1 Density as a Conversion Factor (optional):** `https://itsdrdan.github.io/labpractical/?mode=bench&labs=1a`. This opens PhET Density with tasks. 1.9 already uses vlab 1a.
6. **Practice-mode drills for labs without a bench** (lab-practical questions): `?mode=practice&labs=4b` (4.6 naming), `labs=5a` (6.7 empirical formula), `labs=4a` (6.6 constant composition). One caveat: the intro-hiding `lab-embed` class (line 4493) applies only to `bench|vlab`. Inside a frame, the practice mode still shows the intro cards (see b-7).

### (b) Games that need a small change to deep link
Model to copy: `ddLabView()` in `IMF/index.html:3675` and `aminoacids/index.html:1451–1460`. With `?view=lab`, it shows only the demo plus a link to the full game. Each change is a game change: test it in the simulator and ask before pushing.

1. **gaslaws Piston Lab → 10.1 KMT (or 10.3).** The lab is `<details id="labSection">` (line 369), and its `toggle` listener (line 1191) already starts the sim. In `init` (line 1237), add: if `view=lab`, set `labSection.open = true`, scroll to it, then run `ddLabView(['labSection'])`.
2. **moles Mole Machine → 5.3.** `<details id="mmSection">` (line 315), `init` at about line 1125. Same pattern.
3. **ionicformula Free Builder → 4.2.** `<details id="builderSection">` (line 285). Its `toggle` handler (line 1538) builds the sim; `init()` is at line 1542.
4. **reactions Mixing Bench → 7.5.** The bench is opened by `enterBench()` (bound to `[data-bench]`, about line 1796). Read `?mode=bench` next to the course read at line 1511. Note: reactions defaults to 1A, so the link must include `course=3A`.
5. **polyatomic Ion Builder → 4.2 ("Naming patterns for oxyanions") or 4.5.** It lives inside "The -ate/-ite Family" topic (`ibSpec`, line 1098; UI at line 1488). It needs `?view=lab` to start that lab question from `init` (line 1480).
6. **sigfig topic links → 1.2.1 / 1.3.x.** `TOPICS` already has `glass`, `digital`, `sci`, `precision` (lines 495–506). Add `?topic=` handling at line 1786 to open one topic, e.g. `sigfig/?course=3A&topic=glass` for 1.3.3.
7. **labpractical:** add `'practice'` to the mode list on line 4493 so the (a)-6 practice-mode embeds hide the intro too.
8. **stoichiometry tray questions → 8.4** (`traySpec`, line 668; `#trayQ`, line 257). Add `?topic=limiting&view=lab`. Lower priority, because 8.4 already has PhET RPL.
9. **finalexam:** it reads only `course` (line 680). A `?ch=` filter would let each Practice Games page open Final Boss on that chapter only.

### (c) Openly licensed PhET sims (CC BY 4.0; every URL below returned HTTP 200 on 2026-11-17)
URL pattern: `https://phet.colorado.edu/sims/html/<name>/latest/<name>_all.html`.

**Already used, through labpractical benches:**
- Isotopes and Atomic Mass (2.5, 3.2)
- Models of the Hydrogen Atom (3.2)
- Molecule Shapes (6.4)
- Balancing Chemical Equations (7.2)
- Reactants, Products and Leftovers (8.4, and also shown in 12.5)
- Energy Forms and Changes (9.4)
- Gas Properties (10.3)
- pH Scale (12.5)

**In labpractical but unused:** Density (`bench 1a`); Molarity and Beer's Law Lab (`bench 9a`).

**Not in the book.** None of these is in a labpractical bench, so they would be direct PhET iframes with PhET credit. That is a new box pattern; Dr. Dan should OK it.

| Sim (`name`) | Section | Why |
|---|---|---|
| Build an Atom (`build-an-atom`) | 2.2, 2.4 | p/n/e, charge, mass number; has a game screen |
| Molecule Polarity (`molecule-polarity`) | 6.5 | ΔEN slider, bond dipoles, molecule dipole |
| Acid-Base Solutions (`acid-base-solutions`) | 12.3 | strong vs weak, particle view |
| Beta Decay / Alpha Decay (`beta-decay`, `alpha-decay`) | 14.2, 14.3 | single-atom decay plus many-atom half-life graph (only HTML5 nuclear option) |
| Build a Nucleus (`build-a-nucleus`) | 14.2 | decay modes, nuclide chart |
| Concentration (`concentration`) | 11.2 or 11.3 | saturation, solute amount vs. concentration |
| States of Matter: Basics (`states-of-matter-basics`) | 1.6 | particle motion in solid, liquid and gas |
| States of Matter (`states-of-matter`) | 9.6–9.7 | phase changes, interaction potential |
| Gases Intro (`gases-intro`) | 10.1 | KMT, simpler than Gas Properties |
| Build a Molecule (`build-a-molecule`) | 4.1 | formulas from atoms |
| Rutherford Scattering (`rutherford-scattering`) | 2.1 | gold-foil experiment |
| Blackbody Spectrum (`blackbody-spectrum`) | 3.1 (optional) | color vs. temperature |

**Not available as HTML5** (404): Reactions & Rates, Sugar and Salt Solutions, Salts & Solubility, Radioactive Dating Game.

### (d) Try It bank additions (topic → section, target)

| New or expanded key | Section | Now → target |
|---|---|---|
| `ch01-scinot` (split from `ch01-units`) | 1.2.1 | ~6 → 12 |
| `ch01-units` | 1.2.2 | ~5 left → 10 |
| `ch01-read` (picture items: cylinder, buret, ruler, thermometer, balance) | 1.3.3 | 3 → 10 |
| `ch01-sigcalc` (split) | 1.3.2 | ~3 → 10 |
| `ch01-dosage` | 1.4.4 | 2 → 10 |
| `ch01-percent` | 1.4.5 | 0 → 8 |
| `ch01-powers` | 1.4.3 | 2 → 8 |
| `ch07-activity` | 7.8 | 7 → 10 |
| `ch09-energy`, `ch09-solids`, `ch09-units` | 9.1, 9.7, 9.3 | 7/7/8 → 10 each |
| `ch14-health`, `ch14-medicine`, `ch14-fission` | 14.6, 14.7, 14.5 | 7/6/8 → 10 each |
| `ch03-bohr`, `ch06-ionic`, `ch07-acidgas`, `ch10-kmt`, `ch09-vapor` | — | 9 → 10–12 |

- Also add a mixed Try It to the parent pages 1.2, 1.3 and 1.4. Use their existing keys; no new items are needed.
- Add `&game=sigfig` or `&game=metric` to the Chapter 1 boxes.
- A stopgap until the splits exist: the widget's `&q=` regex filter (`js/widget.js:37`) can narrow a shared key to one page, e.g. `q=mg/kg|IV|mL/h`. It breaks easily, though, so splitting the keys is better.
- Reuse `w`/`y` reasons, as the bank already has them.

### (e) New mini-games (only where nothing exists)
1. **Le Chatelier "Shift It" bench (13.4).** This is the biggest hole: no HTML5 sim exists anywhere. It would be a particle and bar-graph bench for one reaction. Use CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻ (Mateo's case), or N₂ + 3H₂ ⇌ 2NH₃ (Valley fertilizer). The student adds or removes a species, heats or cools, or squeezes the container. Each step is predict → watch → explain. It would fit as a lab in an existing game, or as a new `equilibrium` game with `?course=3A&view=lab`. It would also give Chapter 13 a game.
2. **Chapter 14 "Half-Life Clock".** PhET Beta Decay covers the concept. A whole-half-life dosing tool (Tc-99m 6.0 h, I-131, C-14 5730 y; decay-equation builder with A/Z counters) would match the book's "whole half-lives only" rule and give Chapter 14 a game. This is lower priority than item 1, because PhET can fill the sim role now.

## 4. Practice Games pages

| Page | Links now | Missing / fix |
|---|---|---|
| 1.13 | sigfig, metric, elements, finalexam | **algebratrainer** (scientific notation on the TI-36X, density algebra; the hub lists it for this chapter); labpractical `?mode=practice&labs=0a` |
| 2.9 | elements, finalexam | labpractical `?mode=vlab&labs=2a` (Fresnocitium) |
| 3.9 | quantumchemistry, finalexam | elements (groups, families); algebratrainer (c = λν, E = hν) |
| 4.9 | polyatomic, ionicformula, finalexam | elements (symbols; the hub lists it); labpractical `labs=4b` |
| 5.8 | moles, finalexam | OK; algebratrainer optional |
| 6.10 | lewisstructures, moles, finalexam | labpractical `?mode=vlab&labs=6a`, `labs=5a` |
| 7.11 | reactions, redox, finalexam | labpractical `?mode=vlab&labs=10a` |
| 8.9 | stoichiometry, finalexam | **thermochemistry** (8.6 enthalpy; the hub pairs it with stoichiometry); labpractical `labs=11a` |
| 9.11 | thermochemistry, IMF, finalexam | algebratrainer (q = mcΔT, °F/°C); labpractical `labs=7a` |
| 10.9 | gaslaws, finalexam | **algebratrainer** (PV = nRT is one of its listed topics); stoichiometry (10.5 gas stoichiometry); labpractical `labs=8a` |
| 11.9 | stoichiometry, IMF, finalexam | algebratrainer (molarity); labpractical `labs=9a`, `labs=12b` |
| 12.9 | reactions, finalexam | **algebratrainer** (logarithms for pH); stoichiometry (titration; the hub lists it); labpractical `labs=12a` |
| 13.7 | finalexam | no game exists (see e-1) |
| 14.10 | finalexam | no game exists (see e-2); PhET Beta Decay link |

- **algebratrainer** ("Isolation Station", courses 3A/1A) is the only 3A game the book never links. The hub assigns it to four 3A chapters.
- Small oddity: the 2.5 Try It box uses `&game=quantum` for isotopes. `elements` or a labpractical link would fit better.
