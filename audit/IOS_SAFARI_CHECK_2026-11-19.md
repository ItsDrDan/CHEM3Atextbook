# iPhone Safari check (2026-11-19)

Real Safari (WebKit) on the iPhone 17 simulator, iOS 26, signed in to LibreTexts, with real taps. Earlier checks (axe-core,
reflow, text spacing) ran in the Chromium browser pane at phone width; this check covers what only iPhone Safari shows.
VoiceOver cannot run in the simulator, so the listening test in `audit/VOICEOVER_TEST_SCRIPT.md` is still needed on a real device.

## Pages and parts checked

| What | Where | Result |
|---|---|---|
| Section text, boxes, figures, videos | 10.5, 13.4 | Good: text and box styles render cleanly, figures fill the width with readable labels, videos fit the width. |
| Worked-example math | 10.5 (Examples 10.5.1, 10.5.2) | **Problem 1** below: long equations wrap with lines too close together and units split from their numbers. |
| Try It box, real taps | ch10-stoich (10.5) | Good: wrong answer marked red *and* explained in words; right answer green with ✅ and the worked step; question queued for review. |
| Explore It lab | Equilibrium Park `?mode=lab&sys=hb` (13.4) | Good: opens on Particle Lab with Hemoglobin selected, large tap targets, real subscripts. Takes a few seconds to load the first time. When opened on its own, the floating feedback bubble covers the end of the equation line (minor). |
| Chapter Guide Key Terms cards | 10.7 | Good: each term becomes a labeled card with an "En español" row. **Problem 2** below: the Spanish word "en" opens the electronegativity pop-up. |
| Practice Problems Hint/Answer | 10.8 | Works when tapped, but **Problem 3** below: nothing shows the labels are buttons. |
| Dark mode | 10.8, Try It | Good: LibreTexts and the Try It box both stay light, so there are no half-dark or low-contrast patches. |
| Signed-out reader | any page | The draft book is **Private**: a signed-out reader gets "You do not have permission to view this page." Expected for a Workbench draft; the review packet now says reviewers need project access or the PDF, and the release checklist includes making the book public. |
| LibreTexts' own controls | every page | Platform (not fixable in the book): the floating chat button and the right-edge toolbar cover the last letters of some lines on a phone. |

## Problem 1: long equations wrap badly on phones (MathJax 4 line breaking)

LibreTexts runs MathJax 4.1.3, which wraps long inline equations to the screen width (`overflow="linebreak"`), so the book's
sideways-scroll boxes never come into play. Two things go wrong when it wraps:
- lines sit too close, so a stacked fraction on one line touches or overlaps the next (10.5 Example 10.5.1: the "P" of nRT/P
  runs into the next numerator in Safari);
- MathJax may break at the space between a number and its unit, leaving "L" alone on a line (Examples 10.5.1 and 10.5.2).

**Tested fix (in the browser, not saved):** in equation paragraphs, (a) raise the line height to 2.6 and (b) wrap each
number-unit pair in braces, `{36.7\;\text{L}}`, which MathJax will not break inside. Result: clean, evenly spaced lines and
"= 36.7 L" kept together. Speech and print are unchanged. Scope: 867 centered equation paragraphs and 1,503 number-unit pairs
on 64 pages (repo count). Measured on the live book at 360 px: see "Wrapped-equation count" below.

## Problem 2: "en" in the Spanish column opens the electronegativity pop-up

The Glossary row "electronegativity, EN" makes LibreTexts' glossary script (case-insensitive) turn the Spanish word "en" into a
pop-up: "reactivo **en** exceso", "porcentaje **en** masa", "porcentaje **en** volumen", "reacción **en** cadena", and the
"**En** español" intro. Every other glossary match in the Spanish column is a true cognate (gas, ion, metal, mol, pH…), whose
pop-up gives the right meaning. **Fix (built, not published):** drop ", EN" from that one Glossary row and add "(Symbol: EN.)" to
its definition; `backmatter/build_backmatter.py` now leaves out symbols that are common Spanish words, so a rebuild keeps it out.

## Problem 3: Hint and Answer do not look tappable

LibreTexts' stylesheet makes `<summary>` display inline, which hides the disclosure arrow in every browser. The labels are plain
14.4 px text about 17.5 px tall, stacked tightly; a student may not know they open, and the tap target is well under Apple's
44-point guideline. **Tested fix (local test page in iPhone Safari):** a screen-only style for `details > summary` on the
exercise pages: an outlined button with ▸/▾ arrow (hidden from screen readers with `content: "▸" / ""`), 44 px tall, bold
16 px text, visible focus ring, shaded when open. Print rules are unchanged (hints still print open). It would go in the style
block that `tools/print_layout.py` already keeps at the end of the 118 exercise pages.

## Wrapped-equation count (live book, 360 px)

Running when this file was written: after 56 of 166 pages, 140 wrapped equations on 23 pages (mostly Chapter 1 conversions and
Chapter 2 average atomic mass). Final count to be added.

## Fixed and published (2026-11-19, Dr. Dan approved "All three")

- Problem 1: `tools/math_unit_groups.py` grouped 1,492 number-unit pairs on 64 pages; `tools/print_layout.py` gives equation
  paragraphs line-height 2.6 on phones (screen only). Commit b1c49c1.
- Problem 2: Glossary page 597477, row "electronegativity, EN" → "electronegativity", with "(Symbol: EN.)" added to the definition.
- Problem 3: Hint/Answer button style (screen only) on 126 pages, just before the print style. Commit b1c49c1.
- The partial count before the fix: 219 wrapped equations on 26 of the first 76 pages checked at 360 px (the loop stopped when
  the session restarted). Wrapping itself is expected on phones; the fixes make wrapped lines readable.
- Follow-up (same day): the button style did not apply on most pages. LibreTexts' glossary script scans text inside the page
  content, including `<style>` text; the word "solid" (a glossary term) in `border:1.5px solid` made it re-parse the style as
  HTML, and the `<![CDATA[` marker LibreTexts adds swallowed the selector. The outline is now an inset box-shadow (no glossary
  words), and `tools/print_layout.py` fails if any glossary term appears in the screen style.
