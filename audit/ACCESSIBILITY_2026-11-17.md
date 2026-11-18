# CHEM 3A draft book: accessibility test (2026-11-17)

Standard tested: **WCAG 2.1 AA** (the level California community colleges and Section 508 point to), plus the WCAG 2.2 AA
rules axe can check and axe "best practice" rules, plus the book's own checklist in CLAUDE.md.

## What was tested and how

| Test | Scope | Tool | Result |
|---|---|---|---|
| Automated WCAG scan of the rendered page content | Live Revision Draft pages at phone width 375 px: 72 of 171 pages fully rendered (with math) and scanned; then all 171 pages scanned from their LibreTexts-rendered content inside the live page layout, every hidden answer opened | axe-core 4.14.1 injected into each page on chem.libretexts.org (content area only; LibreTexts' own header/menus are LibreTexts' responsibility) | 1 issue (Practice Games link contrast); fixed in drafts |
| Same scan on the draft files | All 161 draft pages (local preview) | axe-core 4.14.1 | 1 issue (6.5 table header held only math); fixed |
| Phone-width overflow (content wider than the screen, forcing sideways scrolling, WCAG 1.4.10 Reflow) | All 171 live pages at 375 px, answers opened (math checked on the 72 fully rendered pages) | Script: any element past the right edge that is not inside a scroll box | 0 pages overflow; on the local preview, tables and long math looked too wide, but LibreTexts reflows tables into labeled cards and MathJax 4 wraps math, so those were preview artifacts |
| Long math on phones | 1.12 (the worst page in the preview), all 38 answers opened; plus the math on the 72 rendered pages | Live render, MathJax 4.1.3 | MathJax 4 on LibreTexts wraps long inline math; no overflow found. Pages 2.6 and 2.8 (long formulas in the preview) not yet checked live |
| Book checklist (static) | All 161 drafts | Script | Headings start at h2 and never skip a level (1,061 h2, 185 h3); all 92 images have meaningful alt text; all 162 data tables have header cells and a lead-in sentence; all 330 iframes have a title; every hidden answer is `<details><summary>`; no "click here" links; every new-tab link has rel="noopener" |
| Try It widget (practice.html, 142 boxes in the book) | Before and after answering | axe-core | 0 issues; feedback is announced through a polite live region; choices are real buttons |
| Final Boss deep link | iPhone 17 simulator, real taps | iOS Simulator | Opens on the chapter's topics and scrolls to the question; answering works |

## Issues found and fixed (in drafts, commit ddd011b; published 2026-11-17 and re-scanned clean)

1. **Link told apart by color only (WCAG 1.4.1), 14 pages.** On every Practice Games page the "Dr. Dan's Chemistry Study Hub"
   link sits in a gray caption; the blue link had 1.4:1 contrast with the gray text and no underline. Fix: the link is underlined.
2. **Table header with no readable text (6.5).** The ΔEN column header was only a math expression. Fix: plain text
   "ΔEN (electronegativity difference)"; the phone labels (data-th) now read "ΔEN".

## Not covered by automated tools (honest limits)

- **Screen-reader listening test.** axe checks structure, names and contrast, but not whether a page *sounds* right. A short
  VoiceOver pass on two or three pages (one with math, one with a Try It box) by a person is still worth doing; MathJax 4
  provides speech for math.
- **Color contrast inside figures (SVG/PNG).** axe cannot see text drawn inside images. The figures use dark text on light
  backgrounds and the alt text carries the content, but they were not measured.
- **Videos.** Captions on Dr. Dan's YouTube videos are YouTube's (auto or uploaded); not checked here.
- **Games and sims inside iframes** (Final Boss, labpractical, IMF, PhET) are scanned separately from the page; only the Try It
  widget and the Final Boss deep link were tested this round.
- **iOS Simulator.** Real taps covered the Final Boss deep link and earlier the Try It boxes. A page-by-page simulator pass of
  all LIVE_COUNT pages was not done: the Workbench is private (the simulator's Safari is not signed in), and the phone-width
  scan above covers layout on every page instead.
- **LibreTexts' own interface** (header, menus, search, the Previous/Next arrows) is outside the book's control.

## Second pass against the CHEM 3B checklist (textbook/audit/WEB-PDF-ACCESSIBILITY-QA.md), 2026-11-17 evening

| Check (from the 3B list) | Result | Action |
|---|---|---|
| Widget and game addresses | 1,036 distinct external links: 915 answer 200; 119 YouTube links refused the script (429 rate limit), and all 107 video IDs behind them exist (YouTube oEmbed 200); 2 citation sites (doi.org, escholarship.org) block scripts (403) | none |
| Widget parameters (topic exists, pool >= n) | 9.1 and 9.7 asked for 8 from pools of 7 | 16 new items: ch07-activity, ch09-energy, ch09-solids, ch14-health, ch14-medicine now 10 each (848b19b) |
| Picture answer choices with identical names (3B finding A1) | 3A has no picture answer choices | none |
| Widget contrast, measured by hand (3B A5) | choice letters 3.67:1, footer 4.08:1, white on the selected/right/wrong circles 2.9–3.1:1 | darker colors; every state now 4.5:1 or more (measured before answering, selected, hint open, wrong, right) |
| 44 px touch targets | "Play the game" button 39 px | min-height 44 px |
| Keyboard-only use | works (Tab to a choice, Space selects, Enter checks, feedback announced); focus ring #9fb0ff was 2:1; focus fell to the top of the page after Check | ring #3346c4 (6.7–7.5:1); focus moves to New Question after Check |
| `lang`, reduced motion, live region | present | none |
| Glossary pop-ups (platform, 3B A2) | same LibreTexts ARIA failure in 3A; **plus a 3A bug:** one-letter symbol synonyms (A, X, m, i, c, K, P …) made every "a" a pop-up (49 on page 1.4.5 alone) | glossary generator drops one-letter synonyms and writes "Symbol: X." into the definition (glossary_page.html rebuilt; **publish pending**) |
| Accessibility statement | 3A had none | drafted in drafts/front/accessibility_statement.html (**needs Dr. Dan's OK** to add as a front-matter page) |
| PDF (Full (24).pdf) | tagged (/Marked true, StructTreeRoot), Lang en, 92/92 Figure tags with Alt, 162 tables with 580 TH, H1/H2/H3 tags | none |
| iOS Simulator (separate iPhone 17, live GitHub Pages) | Try It: wrong answer, right answer, picture question, new colors, 44 px button; Final Boss chapter link (Ch 14) | pass |

Still not covered: a VoiceOver listening session; 400% zoom reflow on the live LibreTexts pages (375 px tested); the live LibreTexts pages in the simulator (the draft is private, so the simulator's Safari would need Dr. Dan's sign-in).
