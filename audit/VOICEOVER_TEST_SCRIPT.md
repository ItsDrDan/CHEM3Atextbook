# VoiceOver listening test (about 10 minutes)

Purpose: the one test the Accessibility Conformance Report lists as planned. A person listens to three pages with a screen
reader and notes anything that sounds wrong. Automated checks (2026-11-19) already confirmed names, roles, reading order,
live-region feedback, and the spoken text MathJax generates; this test confirms how it actually sounds.

## Setup
- **Mac:** Safari, then turn VoiceOver on with Command-F5 (or Touch ID button pressed three times). VO keys = Control-Option.
  Speak the rotor with VO-U (headings, links, form controls). Read from the cursor with VO-A. Turn VoiceOver off with Command-F5.
- **iPhone:** Settings > Accessibility > VoiceOver (or ask Siri "turn on VoiceOver"). Swipe right/left to move; double-tap to
  activate; two-finger swipe up to read all.

## Page 1: 1.3.2 Significant Figures in Calculations (math, hints, Try It)
1. Open the rotor (VO-U), Headings: the list should read the section headings in order (Learning Objectives box title is not a heading).
2. Move to the first worked example. Listen to an equation: it should say, for example, "10.2 centimeters times 7.6 centimeters
   equals 77.52 centimeters squared, right arrow 78 centimeters squared". **Listen for the word "empty" between numbers and units**
   (fixed 2026-11-19; if you hear it, the fix did not publish).
3. Find an Exercise. The Hint and Answer should be announced as collapsed disclosure buttons; activate Hint and hear the hint text.
4. Find a Try It box (it is a frame; VO-Shift-Down enters it). Choose an answer (it should say "selected" or "pressed"),
   then Check. You should hear "Not quite..." with the reason, or "Correct!" with the explanation, without moving the cursor.

## Page 2: 10.7 Chapter Guide (Key Equations and Key Terms tables)
1. Rotor > Tables (or move to "Key Equations"). On a Mac, VoiceOver should announce the table and its size; moving across a row should
   read the column header (Equation, Use it to, Section) with each cell.
2. On iPhone the tables reflow into cards; each cell should be read with its label (Equation, Use it to, Section).
3. Listen to the ideal gas law row: "P V equals n R T", then "R equals 0.082058 L atm mol to the negative 1 power K to the negative 1 power".

## Page 3: 13.4 Le Chatelier's Principle (figures, Explore It)
1. Move to a figure: VoiceOver should read the description (alt text), then the caption "Figure 13.4.x ...".
2. Move to the Explore It box: the frame should be announced as "Explore It: Particle Lab". Enter it and confirm the mode buttons and
   the reaction buttons (Hb + O2 ...) are announced as buttons.

## Record
For each page: anything confusing, missing, or out of order (page, what you heard, what you expected). Send the notes and the report's
"listening test" line can be changed from planned to done.
