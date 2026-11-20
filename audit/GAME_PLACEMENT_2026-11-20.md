# Game placement audit (2026-11-20)

Goal: put the study games that are only on the Practice Games pages into the sections where students learn each topic, as
green Explore It boxes. Chapters 9 and 11–14 already have in-section game boxes; Chapters 1–8 and 10 had only Lab Practical.

Nothing is published or changed in any game. Draft boxes are in `audit/GAME_PLACEMENT_2026-11-20_boxes.html`.

## How it was checked

- Each game clone pulled to its latest `main` (2026-11-19 "Deep links for the Demo Library" commits).
- Each deep link loaded with `course=3A` in Chromium (Playwright) at phone size, with the local clones served as
  itsdrdan.github.io; what is on screen after load was recorded, plus console errors and sideways overflow.
- Frame width: an Explore It iframe on the live book is **328 px wide** on a 375 px phone (measured on the draft book).
- Page jump: each link loaded in an iframe 1,500 px down a test page, to see whether the game scrolls the page around it.

## Results

| Section | Game: lab | Deep link | Opens on the lab for 3A | Fits 328 px | Pulls the page down |
|---|---|---|---|---|---|
| 1.3.3 Reading tools | Sig Fig Sleuth: Read the glassware | `sigfig/?course=3A&topic=glass` | yes | yes | **yes** |
| 3.4 Electron configurations | Quantum Quest: Orbital diagrams | `quantumchemistry/?course=3A&mode=orbitals` | yes | 24 px wide (mode buttons) | **yes** |
| 4.2 Ionic formulas | Polyatomic Posse: Ion Builder | `polyatomic/?course=3A&mode=family&builder=1` | yes | yes | **yes** |
| 4.3 Naming ionic compounds | Name That Compound!: Ionic Builder | `ionicformula/?course=3A&open=builder` | yes | yes | **yes** |
| 5.3 Mass, moles, particles | Holy Moley!: Mole Machine | `moles/?course=3A&open=molemachine` | yes | 31 px wide (top bar) | **yes** |
| 6.5 Polarity | Lewis Structure Studio: Polarity Lab | `lewisstructures/?course=3A&mode=polarity` | yes | yes | **yes** |
| 7.5 Precipitation (2nd box) | Reaction Rumble: Mixing Bench | `reactions/?course=3A&mode=bench` | yes | 17 px wide (top bar) | no |
| 7.7 Redox | LEO Goes GER!: Identify Redox | `redox/?course=3A&mode=roles` | yes | yes | **yes** |
| 8.4 Limiting reactant (2nd box) | Stoichiometry Quest: Reaction Tray | `stoichiometry/?course=3A&quest=limiting&tray=1` | yes | 31 px wide (top bar) | **yes** |
| 9.4 Specific heat (2nd box) | Thermochemistry: Heat Explorer | `thermochemistry/?course=3A&topic=explore` | yes | 24 px wide (top bar) | **yes** |
| 10.2 Pressure | Under Pressure: Piston Lab | `gaslaws/?course=3A&open=lab` | yes | 19 px wide (top bar) | **yes** |

No console errors on any link. For comparison, the games already in the book (Nuclear, IMF, Proton Swap!, Equilibrium Park,
Lab Practical) fit 328 px and do not move the page.

### Links that do not work for CHEM 3A (by design in the game)

- **7.8 Activity series:** `redox/?mode=activity` is CHEM 1A only; with `course=3A` the game opens Oxidation Numbers instead.
  The book teaches the activity series in 7.8, so opening that mode for 3A would be a game change (your call).
- `redox/?mode=cells&bench=1` (Cell Bench) and `quantumchemistry/?mode=light&bench=1` (Photoelectric Bench) are 1A/1B only.
  Neither topic is in the CHEM 3A outline, so they stay out.
- `thermochemistry/?topic=hess` is 1A only (Hess's law is not in CHEM 3A).
- `metric`, `elements`, `algebratrainer`: no deep link; they stay on the Practice Games pages.

## Problems to fix in the games before any box goes in

1. **Page jump (10 games).** On load, each game scrolls its lab into view with `scrollIntoView`. Inside a frame, that also
   scrolls the textbook page, so a reader who is still reading above the box is pulled down to the game when the frame
   loads (frames load lazily, about a screen ahead). The same happens on later taps (new question, feedback).
   Fix: when the game is in a frame (`window.self !== window.top`), scroll only the game's own page (`window.scrollTo`
   to the element) instead of `scrollIntoView`. A short shim at the top of each game's script does this for every call.
   Games: sigfig, quantumchemistry, polyatomic, ionicformula, moles, lewisstructures, redox, stoichiometry,
   thermochemistry, gaslaws (reactions already stays put).
2. **Sideways wiggle (6 games).** At 328 px the top bar (course buttons, streak, book button) or Quantum's mode buttons
   are 17–31 px wider than the frame, so the game can be dragged sideways inside the box. Fix: a tighter top bar at
   ≤ 360 px. Games: moles, stoichiometry, thermochemistry, gaslaws, reactions, quantumchemistry.

Both are game changes: test with real taps in the iPhone simulator, then ask before pushing.

## Plan

1. Fix the two game problems above (10 repos), simulator-test, push with approval.
2. Publish the 11 boxes (draft file) to the live draft book with approval; each sits just before the Video Lesson(s)
   heading, like the existing 34. That makes 45 Explore It boxes.
3. Recheck in iPhone Safari: no page jump, no sideways drag, the lab is on top.
4. Optional: open the activity-series mode for CHEM 3A and add a 7.8 box.

## Game fixes (2026-11-20, committed locally in each game repo, not pushed)

- **Page jump:** a short script at the top of 11 games (the 10 above plus reactions, whose later taps could also scroll
  the page) replaces `scrollIntoView` and `focus` inside a frame so they scroll only the game. A scroll made while the
  frame is still off screen (Chromium and Safari drop it) is redone once the frame comes into view, so the lab is on top
  when the reader reaches the box. Outside a frame nothing changes.
- **Width:** a `max-width:360px` style (narrower top bar; two-column grids that can shrink) in moles, stoichiometry,
  thermochemistry, gaslaws, reactions, quantumchemistry. Wider screens are unchanged.
- **Checks:** every game's own `tools/check-*.js` passes. In Chromium frames: no page movement on load for all 11, the lab
  on top when the reader scrolls to the box, every link 328 px wide at a 328 px frame. Real taps in iPhone Safari (iPhone
  17 simulator, mock textbook page): Heat Explorer (New Question), Polarity Lab (typing, Check Answer), Piston Lab
  (temperature slider: 550 K gives 3.01 atm), Reaction Tray (prediction): the page never moved; the lab was on top.
- Still wide inside the game (by design): the Polarity Lab bond table and the picker rows scroll sideways in their own box.

## Published (2026-11-20, Dr. Dan approved "Yes, publish them")

All 11 boxes inserted into the live draft pages by an exact-once insertion just before each page's Video Lessons heading
(the repo drafts differ from live only by LibreTexts' own entity and link rewriting, so the live HTML was kept). Page ids:
1.3.3 598091, 3.4 597881, 4.2 597892, 4.3 597893, 5.3 597908, 6.5 597926, 7.5 597948, 7.7 597950, 8.4 597965,
9.4 597983, 10.2 598000. Each POST returned 200; each read-back has the box once; each rendered page shows it (7.5, 8.4,
9.4 now have two boxes). 45 Explore It boxes in all.

Live check (10.2, phone width, signed in): the frame is 328 px wide, no math errors, the page did not move on load, and
when the reader scrolls down to the box the Piston Lab is on top. Seen once in the Chromium pane: after a scripted
jump straight to the box (not reader scrolling), the frame showed the game's start screen instead of the lab (one tap
away). The iPhone simulator's Safari was signed out of LibreTexts, so the live check there was not repeated.
