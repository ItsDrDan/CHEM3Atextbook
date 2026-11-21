# Accessibility inside the embedded games (2026-11-20)

Read-only. Nothing was changed. All 83 distinct game and lab frames the book embeds (19 games), loaded live in a 328 px frame
(the Explore It width on a 375 px phone). axe-core 4.14.1 with the WCAG 2.1 A and AA rules, plus a keyboard pass.

## Results

| Check | Result |
|---|---|
| axe, first screen | 70 of 83 frames clean; 13 frames have issues, in 8 games (below) |
| Keyboard traps | None. The first pass flagged 14 frames; each was retested and Tab goes through and out, Shift+Tab comes back |
| Visible focus ring | Present on every stop in 82 of 83 frames (exception: item 5) |
| Clickable things that the keyboard cannot reach | None that do anything (see item 6) |

## Issues to fix

| # | WCAG | Game | Issue |
|---|---|---|---|
| 1 | 4.1.2 (critical) | Reaction Rumble | At phone width the Green Sheet button shows only an icon and has no accessible name |
| 2 | 1.4.3 | Stoichiometry Quest, Thermochemistry | Low contrast: Tray "nothing yet" 2.46:1; Heat Explorer ΔT labels 4.25:1 (4.5:1 needed) |
| 3 | 2.1.1 | LEO Goes GER!, Stoichiometry Quest | A sideways-scrolling area cannot be reached by keyboard: the activity series chart (in the 7.8 box) and the example equation |
| 4 | 2.5.3 | Name That Compound! (88 buttons), Sticky Molecules (5), Equilibrium Park (3), Quantum Quest (1) | The spoken name leaves out the visible text (a button shows "Na⁺" but is named "Add sodium"), so voice-control users cannot say what they see |
| 5 | 4.1.2, 2.4.7 | Sticky Molecules, phase diagram (9.5) | The draggable point sits inside an element marked as an image and has no visible focus ring. Its arrow keys do work |
| 6 | minor | Final Boss | The Calculator chip has a pointer cursor but no click action was found, so it looks clickable. The separate Calculator button works |

Nine games would change. All fixes are small (labels, colors, `tabindex`, one focus style).

## Decision for Dr. Dan: the Accessibility Conformance Report

The ACR says the games are "linked, not covered." That was accurate when they were links, but 46 Explore It boxes now embed
them in the pages. Suggested wording: the games are embedded optional practice, each section teaches the same skill in
accessible text, and they were scanned on this date with the results here. The Accessibility Statement also says games are
linked "from the Practice Games pages," which is now incomplete.

## Not covered

- Only each frame's first screen. Answer feedback and later lab steps were not scanned.
- PhET simulations nested inside Lab Practical frames (PhET's own product).
- Screen-reader listening. axe checks names and structure, not how a game sounds; the VoiceOver test is still needed on a real device.
- Color contrast that axe could not decide (backgrounds with gradients or images) was not checked by hand.
