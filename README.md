# CHEM3Atextbook

Working repo for the overhaul of the CHEM 3A (Introductory General Chemistry, Fresno City College) LibreTexts book. Start with `CLAUDE.md`.

| File | What it is |
|---|---|
| `CLAUDE.md` | Project decisions and working rules (read first). |
| `tools/COR_outline.md` | The approved CHEM 3A COR (Spring 2027), with scope notes and conflicts. |
| `tools/SOURCES.md` | Inventory of course files, videos, banks and games, mapped to COR units. |
| `tools/BLUEPRINT.md` | Chapter-by-chapter plan in COR order (draft for review). |
| `tools/PATIENT_CASE_PROPOSAL.md` | Running patient case options (awaiting approval). |
| `tools/AUTHOR_BRIEF.md` | Writing standards for every page. |
| `tools/ISSUES_LOG.md` | Running issues log. |
| `tools/live_tree.txt` | Page tree of the live book with page ids (read-only reference). |
| `tools/find_moment.py` | Search Dr. Dan's video transcripts for a phrase and get timestamped links. |
| `drafts/ch01/` | New Chapter 1 pages (HTML fragments for LibreTexts): 1.0 intro … 1.6 sections, 1.7 Chapter Guide, 1.8 Practice Problems, 1.9 Practice Games. |
| `figures/ch01/` | Chapter 1 figures (SVG), built by `tools/figs_ch01.py`. Phone-first: ~470 px wide, text 13–17 px. |
| `practice.html`, `js/`, `css/`, `bank/` | The CHEM 3A Try It widget (adapted from the CHEM 3B one) and its question banks. `js/fbx.js` adds per-choice feedback (`y`). URL: `practice.html?t=ch01-classify&n=10&title=…`. |
| `tools/check_fragment.py` | Page checker (copied from CHEM 3B, adapted). Run on every draft. |
| `tools/build_preview.py` | Builds a local preview site of all drafts for checking renders. |

Hosting: figure and widget URLs assume GitHub Pages at `https://itsdrdan.github.io/CHEM3Atextbook/` (not live until the repo is pushed and Pages is enabled).
