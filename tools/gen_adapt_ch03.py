#!/usr/bin/env python3
"""Builds bank/ch03_adapt.json (Chapter 3 ADAPT homework-only items, text only). Scratch generator.
usage: python3 tools/gen_adapt_ch03.py bank/ch03_adapt.json
c = 3.00e8 m s^-1, h = 6.626e-34 J s; every number is recomputed by tools/check_bank_ch03.py."""
import json, sys, math
from decimal import Decimal, ROUND_HALF_UP
OUT = sys.argv[1]
C, H = 3.00e8, 6.626e-34
M = '&minus;'
B = []
def Q(t, q, c, y, h, w, d, k=0):
    y = ["Correct: " + y[0]] + y[1:]
    B.append({"id": "c3-h%02d" % (len(B) + 1), "t": t, "q": q, "c": c, "y": y, "h": h, "w": w, "d": d, "k": k})
def num(x, n=3):
    e = math.floor(math.log10(abs(x)))
    m = Decimal(repr(x / 10 ** e)).quantize(Decimal(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if m >= 10: m = (m / 10).quantize(Decimal(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP); e += 1
    if -2 <= e <= 2:
        return ('%.' + str(max(0, n - 1 - e)) + 'f') % (m * Decimal(10) ** e)
    return '%s &times; 10<sup>%s</sup>' % (m, (M + str(-e)) if e < 0 else str(e))
def cfg(s):
    return ' '.join(t if t.startswith('[') else t[:2] + '<sup>' + t[2:] + '</sup>' for t in s.split())
def ion(sym, ch):
    mag = '' if abs(ch) == 1 else str(abs(ch))
    return sym + '<sup>' + mag + ('+' if ch > 0 else M) + '</sup>'
E0 = '[&nbsp;&nbsp;]'

# ---------------- ch03-light (7) ----------------
T = 'ch03-light'
nu = C / 842e-9
Q(T, "Satellites that map the health of San Joaquin Valley orchards measure near-infrared light reflected by leaves at 842 nm. What is the frequency of this light?",
  [num(nu) + " Hz", num(C / 842) + " Hz", num(C * 842e-9) + " Hz", num(842e-9 / C) + " Hz"],
  ["842 nm = 8.42 &times; 10<sup>" + M + "7</sup> m; &nu; = c/&lambda; = (3.00 &times; 10<sup>8</sup> m s<sup>" + M + "1</sup>)/(8.42 &times; 10<sup>" + M + "7</sup> m).",
   "The wavelength was left in nanometers. Convert to meters to match the speed of light.",
   "This multiplies c by &lambda;; solving c = &lambda;&nu; for &nu; means dividing.",
   "This divides &lambda; by c, which is upside down and gives units of seconds."],
  "Units first: c is in meters per second.",
  "&lambda; = 842 &times; 10<sup>" + M + "9</sup> m = 8.42 &times; 10<sup>" + M + "7</sup> m. &nu; = c/&lambda; = <b>" + num(nu) + " Hz</b>, a little lower than red light's frequency, as expected for near-infrared.", 2, 1)

lam = C / 1.90e9
Q(T, "A cell phone sends signals at 1.90 &times; 10<sup>9</sup> Hz. What is the wavelength of these waves?",
  [num(lam) + " m", num(1.90e9 / C) + " m", num(C * 1.90e9) + " m", num(lam) + " nm"],
  ["&lambda; = c/&nu; = (3.00 &times; 10<sup>8</sup> m s<sup>" + M + "1</sup>)/(1.90 &times; 10<sup>9</sup> s<sup>" + M + "1</sup>); seconds cancel, leaving meters.",
   "This divides &nu; by c, which is upside down.",
   "This multiplies c by &nu;; solve c = &lambda;&nu; for &lambda; by dividing.",
   "The number is right but the unit is wrong: dividing m s<sup>" + M + "1</sup> by s<sup>" + M + "1</sup> leaves meters, not nanometers."],
  "Rearrange c = &lambda;&nu; and follow the units.",
  "&lambda; = c/&nu; = (3.00 &times; 10<sup>8</sup>)/(1.90 &times; 10<sup>9</sup>) = <b>" + num(lam) + " m</b> (about 16 cm), in the microwave and radio range.", 2, 1)

E = H * C / 2.50e-11
Q(T, "An X-ray photon used in diagnostic imaging has a wavelength of 0.0250 nm. What is its energy?",
  [num(E) + " J", num(H * C / 0.0250) + " J", num(C / 2.50e-11) + " J", num(H / 2.50e-11) + " J"],
  ["0.0250 nm = 2.50 &times; 10<sup>" + M + "11</sup> m; E = hc/&lambda; = (6.626 &times; 10<sup>" + M + "34</sup>)(3.00 &times; 10<sup>8</sup>)/(2.50 &times; 10<sup>" + M + "11</sup>).",
   "The wavelength was left in nanometers, which makes the energy 10<sup>9</sup> times too small.",
   "This is the frequency, c/&lambda;; multiply by h to get the energy.",
   "This divides h by &lambda; and drops c; use E = hc/&lambda;."],
  "Convert nm to m first. The same equation works for X-rays as for visible light.",
  "E = hc/&lambda; = (6.626 &times; 10<sup>" + M + "34</sup> J s)(3.00 &times; 10<sup>8</sup> m s<sup>" + M + "1</sup>)/(2.50 &times; 10<sup>" + M + "11</sup> m) = <b>" + num(E) + " J</b>, tens of thousands of times the energy of a visible photon, which is why X-rays are ionizing.", 3, 1)

E = H * 5.09e14
Q(T, "Light from a sodium lamp has a frequency of 5.09 &times; 10<sup>14</sup> Hz. What is the energy of one photon?",
  [num(E) + " J", num(H / 5.09e14) + " J", num(5.09e14 / H) + " J", num(H * C / 5.09e14) + " J"],
  ["E = h&nu; = (6.626 &times; 10<sup>" + M + "34</sup> J s)(5.09 &times; 10<sup>14</sup> s<sup>" + M + "1</sup>).",
   "This is h/&nu;; E = h&nu; is a product.",
   "This is &nu;/h, which gives an impossibly large energy for one photon.",
   "This uses hc/&nu;, mixing E = hc/&lambda; with E = h&nu;; c is not needed when &nu; is given."],
  "Use the equation that links energy and frequency directly.",
  "E = h&nu; = (6.626 &times; 10<sup>" + M + "34</sup>)(5.09 &times; 10<sup>14</sup>) = <b>" + num(E) + " J</b>.", 2, 1)

Q(T, "Put these photons in order of <b>increasing energy</b>: pulse oximeter infrared (940 nm), dental curing light (470 nm), UV-C lamp (254 nm), sodium lamp (589 nm).",
  ["940 nm &lt; 589 nm &lt; 470 nm &lt; 254 nm", "254 nm &lt; 470 nm &lt; 589 nm &lt; 940 nm", "589 nm &lt; 940 nm &lt; 470 nm &lt; 254 nm", "940 nm &lt; 470 nm &lt; 589 nm &lt; 254 nm"],
  ["Energy is inversely related to wavelength, so increasing energy means decreasing wavelength.",
   "This is the order of increasing wavelength, which is decreasing energy.",
   "940 nm is longer than 589 nm, so the infrared photon has less energy than the sodium photon.",
   "589 nm is longer than 470 nm, so the sodium photon has less energy than the blue curing-light photon."],
  "E = hc/&lambda;. Which wavelength gives the smallest energy?",
  "Longest wavelength, lowest energy: <b>940 &lt; 589 &lt; 470 &lt; 254 nm</b> (infrared &lt; yellow-orange &lt; blue &lt; ultraviolet).", 2)

Q(T, "A germicidal lamp gives off light at 254 nm. Which region of the electromagnetic spectrum is this?",
  ["Ultraviolet", "Visible", "Infrared", "Microwave"],
  ["254 nm is shorter than violet light (about 400 nm), so it is ultraviolet (UV-C).",
   "Visible light runs from about 400 to 700 nm; 254 nm is shorter than that.",
   "Infrared wavelengths are longer than red light, above about 700 nm.",
   "Microwaves have wavelengths of millimeters to centimeters, far longer than 254 nm."],
  "Compare 254 nm with the visible range, about 400 to 700 nm.",
  "254 nm is shorter than violet, so it is <b>ultraviolet</b>. UV-C photons have enough energy to damage the DNA and RNA of microbes.", 1)

r = 940 / 254
Q(T, "About how many times more energy does one 254 nm UV-C photon carry than one 940. nm pulse-oximeter infrared photon?",
  [num(r) + " times", num(254 / 940) + " times", "%d times" % (940 - 254), num(r ** 2) + " times"],
  ["E is inversely proportional to &lambda;, so E<sub>UV</sub>/E<sub>IR</sub> = 940./254, to 3 significant figures (the decimal point makes all three digits of 940. significant).",
   "This is 254/940, upside down; the shorter-wavelength UV photon has more energy, so the ratio must be more than 1.",
   "This subtracts the wavelengths; a ratio needs division.",
   "This squares the ratio; energy is inversely proportional to &lambda;, not &lambda;<sup>2</sup>."],
  "Divide hc/&lambda; for one photon by hc/&lambda; for the other.",
  "E<sub>UV</sub>/E<sub>IR</sub> = (hc/254 nm)/(hc/940. nm) = 940./254 = <b>" + num(r) + "</b>. Each UV-C photon carries almost four times the energy of an infrared photon.", 3, 1)

# ---------------- ch03-bohr (6) ----------------
T = 'ch03-bohr'
Q(T, "An electron in a hydrogen atom moves from n = 2 to n = 5. What happens?",
  ["The atom absorbs energy.", "The atom gives off a photon.", "The atom loses a proton.", "Nothing; the energy of the atom does not change."],
  ["Moving to a higher level means moving up the staircase, which takes energy.",
   "Photons are given off when electrons drop to lower levels, not when they rise.",
   "Electron jumps do not change the nucleus.",
   "Each level has a fixed energy, and n = 5 is higher than n = 2, so the energy changes."],
  "Is the electron moving up or down?",
  "n = 2 to n = 5 is a jump <b>up</b>, so the atom <b>absorbs</b> energy (excitation). It would give off light only when the electron drops back.", 1)

Q(T, "Which electron drop gives off the photon with the <b>longest</b> wavelength?",
  ["n = 4 to n = 3", "n = 4 to n = 2", "n = 4 to n = 1", "n = 3 to n = 1"],
  ["n = 4 to n = 3 is the smallest drop of these; the smallest energy gives the longest wavelength.",
   "Dropping to n = 2 releases more energy than dropping to n = 3, so the wavelength is shorter.",
   "Dropping all the way to n = 1 is the biggest drop here, so it gives the shortest wavelength.",
   "Any drop to n = 1 is large, because the gap between n = 1 and n = 2 alone is the biggest gap of all."],
  "Longest wavelength means least energy. Which drop is smallest?",
  "Bigger drop, shorter wavelength; so the smallest drop, <b>n = 4 to n = 3</b>, gives the longest wavelength (it is in the infrared).", 2)

Q(T, "Red fireworks contain strontium compounds, and green ones contain barium compounds. What does this show?",
  ["Each element has its own fixed energy levels, so its electrons give off their own set of wavelengths.",
   "The color of a firework depends only on how hot it burns.",
   "Strontium and barium have the same energy levels.",
   "Electrons can drop by any amount of energy."],
  ["Different levels mean different energy gaps, and each gap gives one wavelength, so each element has its own colors.",
   "Both burn at similar temperatures but give different colors, so the element sets the color.",
   "If their levels were the same, they would give the same colors.",
   "Electron energies are quantized; only certain drops are possible."],
  "Why would two elements give different colors in the same flame?",
  "Each element has <b>its own set of energy levels</b>, so the drops, and the wavelengths of light they give off, are unique to that element. This is the basis of flame tests.", 2)

Q(T, "In the lab, you look at an unknown gas discharge tube through a spectroscope and record its bright lines. How can you identify the gas?",
  ["Match the pattern of line wavelengths to the known line spectra of elements.",
   "Measure how bright the tube is.",
   "Look for a smooth rainbow with no gaps.",
   "Count only the number of lines, ignoring their wavelengths."],
  ["Each element's emission lines form a unique pattern, like a bar code, so the set of wavelengths identifies the element.",
   "Brightness depends on the tube's current and pressure; it does not identify the element.",
   "A glowing gas gives a line spectrum, not a continuous rainbow.",
   "Two elements could have the same number of visible lines; the wavelengths are what make the pattern unique."],
  "What makes one element's spectrum different from another's?",
  "A gas gives a <b>line spectrum unique to the element</b>. Matching the measured wavelengths to known values identifies it, the same way astronomers identify elements in stars.", 1)

E = H * C / 434e-9
Q(T, "Hydrogen gives off a blue-violet line at 434 nm. What is the energy of one photon of this light?",
  [num(E) + " J", num(H * C / 434) + " J", num(C / 434e-9) + " J", num(H * C * 434e-9) + " J"],
  ["434 nm = 4.34 &times; 10<sup>" + M + "7</sup> m; E = hc/&lambda; = (6.626 &times; 10<sup>" + M + "34</sup>)(3.00 &times; 10<sup>8</sup>)/(4.34 &times; 10<sup>" + M + "7</sup>).",
   "The wavelength was left in nanometers, so the result is 10<sup>9</sup> times too small.",
   "This is the frequency, c/&lambda;, not the energy.",
   "This multiplies by &lambda; instead of dividing; energy goes <i>down</i> as wavelength goes up."],
  "Convert first, then use the combined equation. Should the wavelength be on the top or the bottom?",
  "E = hc/&lambda; = (6.626 &times; 10<sup>" + M + "34</sup>)(3.00 &times; 10<sup>8</sup>)/(4.34 &times; 10<sup>" + M + "7</sup>) = <b>" + num(E) + " J</b>, the gap between hydrogen's n = 5 and n = 2 levels.", 3, 1)

Q(T, "An LED gives off light when electrons drop across a fixed energy gap in a semiconductor. Which LED needs the <b>largest</b> energy gap?",
  ["A blue LED", "A red LED", "An infrared LED", "All LEDs have the same gap."],
  ["Blue light has the shortest wavelength of these, so each photon has the most energy, which needs the biggest drop.",
   "Red light has a longer wavelength and less energy than blue, so its gap is smaller.",
   "Infrared light has an even longer wavelength and less energy than red.",
   "Different colors mean different photon energies, so the gaps must differ."],
  "Bigger drop, more energetic photon. Which color has the shortest wavelength?",
  "The photon's energy equals the gap. <b>Blue</b> light has the shortest wavelength and highest energy of these, so the blue LED needs the largest gap.", 2)

# ---------------- ch03-orbitals (7) ----------------
T = 'ch03-orbitals'
Q(T, "How many orbitals are in a <b>d subshell</b>?",
  ["5", "3", "10", "7"],
  ["A d subshell has 5 orbitals; at 2 electrons each, it holds 10 electrons.",
   "3 is the number of p orbitals.",
   "10 is the number of electrons a d subshell holds, not the number of orbitals.",
   "7 is the number of f orbitals."],
  "s, p, d and f subshells have 1, 3, ?, 7 orbitals.",
  "s has 1 orbital, p has 3, <b>d has 5</b>, and f has 7. That is why the d block is 10 columns wide.", 1)

Q(T, "What is the greatest number of electrons the <b>second shell</b> (n = 2) can hold?",
  ["8", "2", "6", "18"],
  ["Shell 2 has 2s (2 electrons) and 2p (6 electrons): 2 + 6 = 8, which matches 2n<sup>2</sup> = 8.",
   "2 is the capacity of the first shell, or of the 2s subshell alone.",
   "6 is the capacity of the 2p subshell alone; 2s adds 2 more.",
   "18 is the capacity of shell 3, which has a d subshell."],
  "Which subshells does shell 2 have?",
  "Shell 2 has 2s and 2p: 2 + 6 = <b>8 electrons</b>. This is the octet that row-2 elements such as neon complete.", 1)

Q(T, "Which drawing shows the 2p subshell of a ground-state <b>nitrogen</b> atom correctly?",
  ["2p [↑][↑][↑]", "2p [↑↓][↑]" + E0, "2p [↑↓][↑↓]" + E0, "2p [↑][↓][↑]"],
  ["Nitrogen has 3 electrons in 2p; Hund's rule puts one in each orbital, all with the same spin.",
   "Pairing two electrons while a 2p orbital is empty breaks Hund's rule.",
   "This shows 4 electrons, which is oxygen's 2p count, and it also pairs too early.",
   "Unpaired electrons in equal-energy orbitals all have the same spin in the ground state."],
  "Hund's rule: how should 3 electrons spread over 3 equal-energy orbitals?",
  "N is 1s<sup>2</sup> 2s<sup>2</sup> 2p<sup>3</sup>. By Hund's rule, the three 2p electrons go one per orbital with the same spin: <b>[↑][↑][↑]</b>, 3 unpaired electrons.", 2)

Q(T, "How many <b>unpaired electrons</b> does a ground-state silicon atom have?",
  ["2", "4", "0", "1"],
  ["Si is [Ne] 3s<sup>2</sup> 3p<sup>2</sup>; the two 3p electrons sit in separate orbitals (Hund's rule): 3p [↑][↑]" + E0 + ".",
   "4 is the number of valence electrons; the two 3s electrons are paired.",
   "Hund's rule keeps the two 3p electrons apart, so they are not paired.",
   "There are two electrons in 3p, and they go in different orbitals."],
  "Draw just the 3s and 3p boxes.",
  "3s [↑↓] 3p [↑][↑]" + E0 + ": <b>2 unpaired electrons</b>.", 2)

Q(T, "Following the Aufbau principle, which subshell fills <b>right after 4s</b>?",
  ["3d", "4p", "4d", "5s"],
  ["Diagonal order: ... 3p 4s <b>3d</b> 4p 5s ... In row 4, the d block (3d) comes right after 4s.",
   "4p comes after 3d; in row 4 you cross the ten d-block columns first.",
   "4d belongs to row 5 and comes after 5s.",
   "5s comes after 4p."],
  "Picture row 4 of the periodic table from left to right.",
  "After 4s comes <b>3d</b>, then 4p. That is why row 4 has ten transition metals between calcium and gallium.", 2)

Q(T, "Which is the correct orbital diagram for a ground-state <b>aluminum</b> atom (Z = 13)?",
  ["1s [↑↓] 2s [↑↓] 2p [↑↓][↑↓][↑↓] 3s [↑↓] 3p [↑]" + E0 + E0,
   "1s [↑↓] 2s [↑↓] 2p [↑↓][↑↓][↑↓] 3s [↑] 3p [↑↓]" + E0 + E0,
   "1s [↑↓] 2s [↑↓] 2p [↑↓][↑↓][↑↓] 3s [↑↓] 3p [↑][↑]" + E0,
   "1s [↑↓] 2s [↑↓] 2p [↑↓][↑↓][↑] 3s [↑↓] 3p [↑][↑]" + E0],
  ["13 arrows: 1s, 2s, 2p and 3s are full, and the 13th electron goes alone into a 3p orbital.",
   "3s should fill before an electron goes into 3p (Aufbau principle).",
   "This has 14 electrons, which is silicon.",
   "2p must be full before 3s and 3p get electrons (Aufbau principle)."],
  "Count arrows, then check each subshell is full before the next one starts.",
  "Al: 1s<sup>2</sup> 2s<sup>2</sup> 2p<sup>6</sup> 3s<sup>2</sup> 3p<sup>1</sup>. The diagram has full 1s, 2s, 2p and 3s boxes and <b>one arrow in 3p</b>, for 13 electrons and 1 unpaired electron.", 3)

Q(T, "What does the <b>Pauli exclusion principle</b> say?",
  ["An orbital holds at most two electrons, and two electrons in the same orbital must have opposite spins.",
   "Electrons fill the lowest-energy orbitals first.",
   "Electrons spread out over equal-energy orbitals before pairing.",
   "A shell holds at most eight electrons."],
  ["Pauli limits each orbital (each box) to two electrons, drawn as one up and one down arrow.",
   "This is the Aufbau principle.",
   "This is Hund's rule.",
   "Only shell 2 is limited to 8; shell 3 holds 18 and shell 4 holds 32."],
  "Pauli is the rule about a single box.",
  "<b>Pauli:</b> at most 2 electrons per orbital, with opposite spins (&uarr;&darr;). Aufbau sets the filling order and Hund's rule sets how equal-energy orbitals fill.", 1)

# ---------------- ch03-config (7) ----------------
T = 'ch03-config'
Q(T, "Silicon is used in computer chips and in some medical implants. What is the full electron configuration of a silicon atom (Z = 14)?",
  [cfg("1s2 2s2 2p6 3s2 3p2"), cfg("1s2 2s2 2p6 3s2 3p4"), cfg("1s2 2s2 2p6 3s4"), cfg("1s2 2s2 2p6 3s2 3d2")],
  ["2 + 2 + 6 + 2 + 2 = 14; after 3s fills, the last 2 electrons go into 3p.",
   "This adds to 16 (sulfur).",
   "An s subshell holds only 2 electrons, so 3s<sup>4</sup> is impossible.",
   "3p fills before 3d (in fact 4s also comes before 3d)."],
  "Fill in diagonal order and check that the superscripts add to 14.",
  "Si: <b>" + cfg("1s2 2s2 2p6 3s2 3p2") + "</b>. Silicon is in group 14, the second column of the p block, so it ends in p<sup>2</sup>.", 2)

Q(T, "Selenium is a trace element in some enzymes. What is the noble-gas configuration of a selenium atom (Z = 34)?",
  [cfg("[Ar] 4s2 3d10 4p4"), cfg("[Ar] 4s2 4p4"), cfg("[Ar] 4s2 4d10 4p4"), cfg("[Kr] 4s2 3d10 4p4")],
  ["After [Ar] (18), row 4 crosses 4s (2), 3d (10) and 4 columns of 4p: 18 + 16 = 34.",
   "This skips the 3d block, so it totals only 24.",
   "The row-4 d block is 3d, not 4d.",
   "Krypton is at the end of selenium's own row; use the noble gas from the row above."],
  "Which noble gas ends the row above selenium? Then read across row 4.",
  "Se: <b>" + cfg("[Ar] 4s2 3d10 4p4") + "</b>. Check: 18 + 2 + 10 + 4 = 34. It ends in p<sup>4</sup> like oxygen and sulfur in group 16.", 2)

Q(T, "Which element has the configuration " + cfg("1s2 2s2 2p6 3s2 3p6 4s1") + "?",
  ["Potassium", "Argon", "Sodium", "Calcium"],
  ["2 + 2 + 6 + 2 + 6 + 1 = 19 electrons: Z = 19, potassium.",
   "Argon has 18 electrons and ends at 3p<sup>6</sup>.",
   "Sodium also ends in s<sup>1</sup>, but in 3s, with 11 electrons.",
   "Calcium has 20 electrons and ends in 4s<sup>2</sup>."],
  "Add the superscripts.",
  "19 electrons, so Z = 19: <b>potassium</b>, which starts row 4 in group 1.", 1)

Q(T, "What is the electron configuration of the chloride ion, Cl<sup>" + M + "</sup>?",
  [cfg("1s2 2s2 2p6 3s2 3p6"), cfg("1s2 2s2 2p6 3s2 3p4"), cfg("1s2 2s2 2p6 3s2 3p5"), cfg("1s2 2s2 2p6 3s2 3p5 4s1")],
  ["Cl has 17 electrons; Cl<sup>" + M + "</sup> has 18, which fills 3p: the same as argon.",
   "This removes an electron (16 in all); a negative ion has gained one.",
   "This is the neutral chlorine atom.",
   "The added electron goes into the open spot in 3p, not into 4s."],
  "Add one electron to the next open spot in the filling order.",
  "Cl (" + cfg("1s2 2s2 2p6 3s2 3p5") + ") gains one electron: <b>" + cfg("1s2 2s2 2p6 3s2 3p6") + "</b>, isoelectronic with argon.", 2)

Q(T, "What is the electron configuration of the aluminum ion, Al<sup>3+</sup>?",
  [cfg("1s2 2s2 2p6"), cfg("1s2 2s2 2p6 3s2 3p4"), cfg("1s2 2s2 2p6 3s2"), cfg("1s2 2s2 2p3 3s2 3p1")],
  ["Al has 13 electrons; Al<sup>3+</sup> has 10. The three highest-shell electrons (3s<sup>2</sup> 3p<sup>1</sup>) are removed, leaving neon's configuration.",
   "This adds 3 electrons (16 in all); a positive ion has lost electrons.",
   "This removes only the 3p electron (12 in all); a 3+ ion has lost 3.",
   "Electrons come off the highest-numbered shell first (shell 3), not out of 2p."],
  "A 3+ charge means 3 electrons lost. Which shell loses them?",
  "Al: " + cfg("1s2 2s2 2p6 3s2 3p1") + ". Remove all three shell-3 electrons: <b>" + cfg("1s2 2s2 2p6") + "</b> (10 electrons), isoelectronic with neon.", 2)

Q(T, "Calcium is in row 4, group 2. In which block of the periodic table is it?",
  ["s block", "p block", "d block", "f block"],
  ["Groups 1 and 2 (plus helium) form the s block, 2 columns wide; calcium's last electron enters 4s.",
   "The p block is groups 13 to 18.",
   "The d block is groups 3 to 12.",
   "The f block is the two rows below the main table."],
  "Which block is 2 columns wide?",
  "Groups 1 and 2 are the <b>s block</b>. Calcium is [Ar] 4s<sup>2</sup>.", 1)

Q(T, "Which set of ions is <b>entirely</b> isoelectronic with neon?",
  ["O<sup>2" + M + "</sup>, F<sup>" + M + "</sup>, Na<sup>+</sup>, Mg<sup>2+</sup>",
   "F<sup>" + M + "</sup>, Cl<sup>" + M + "</sup>, Na<sup>+</sup>, K<sup>+</sup>",
   "Na<sup>+</sup>, K<sup>+</sup>, Mg<sup>2+</sup>, Ca<sup>2+</sup>",
   "O<sup>2" + M + "</sup>, S<sup>2" + M + "</sup>, Na<sup>+</sup>, Mg<sup>2+</sup>"],
  ["8 + 2, 9 + 1, 11 " + M + " 1 and 12 " + M + " 2 all equal 10 electrons, the same as neon.",
   "Cl<sup>" + M + "</sup> and K<sup>+</sup> have 18 electrons, like argon.",
   "K<sup>+</sup> and Ca<sup>2+</sup> have 18 electrons, like argon.",
   "S<sup>2" + M + "</sup> has 16 + 2 = 18 electrons, like argon."],
  "Electrons in an ion = protons " + M + " charge. Neon has 10.",
  "<b>O<sup>2" + M + "</sup>, F<sup>" + M + "</sup>, Na<sup>+</sup> and Mg<sup>2+</sup></b> each have 10 electrons (1s<sup>2</sup> 2s<sup>2</sup> 2p<sup>6</sup>). Ions of row-3 nonmetals and row-4 metals match argon instead.", 3)

# ---------------- ch03-valence (7) ----------------
T = 'ch03-valence'
Q(T, "Strontium is in group 2. How many valence electrons does a strontium atom have?",
  ["2", "38", "12", "8"],
  ["Groups 1 and 2: valence electrons = group number, so strontium has 2 (5s<sup>2</sup>).",
   "38 is strontium's atomic number, its total number of electrons.",
   "Subtracting 10 is only for groups 13 to 18; adding 10 is never the rule.",
   "8 is a full octet, which strontium does not have."],
  "Which rule applies to groups 1 and 2?",
  "Group 2: <b>2 valence electrons</b> (Sr is [Kr] 5s<sup>2</sup>). Like calcium, it loses them to form a 2+ ion.", 1)

Q(T, "Iodine is in group 17. How many valence electrons does an iodine atom have?",
  ["7", "17", "53", "1"],
  ["Groups 13 to 18: group number " + M + " 10. 17 " + M + " 10 = 7 (5s<sup>2</sup> 5p<sup>5</sup>).",
   "17 is the group number; subtract 10 for groups 13 to 18.",
   "53 is the total number of electrons.",
   "1 is the number of electrons iodine gains to form I<sup>" + M + "</sup>."],
  "Use the rule for groups 13 to 18.",
  "17 " + M + " 10 = <b>7 valence electrons</b>; iodine gains one to form iodide, I<sup>" + M + "</sup>.", 1)

Q(T, "Use the octet rule to predict the ion that rubidium (group 1) forms.",
  [ion("Rb", 1), ion("Rb", -7), ion("Rb", -1), ion("Rb", 2)],
  ["One valence electron is lost easily, leaving krypton's configuration: Rb<sup>+</sup>.",
   "Gaining 7 electrons is far harder than losing 1; metals lose electrons.",
   "Losing an electron makes a positive ion; a negative charge would mean gaining.",
   "Rubidium has only one valence electron to lose; a 2+ ion would break into the krypton core."],
  "How many valence electrons does a group 1 metal have?",
  "Rb has 1 valence electron (5s<sup>1</sup>). Losing it gives <b>Rb<sup>+</sup></b>, isoelectronic with krypton.", 2)

Q(T, "Ammonia fertilizers contain nitrogen, which is in group 15. If a nitrogen atom forms a monatomic ion, what charge does the octet rule predict?",
  ["3" + M, "5+", "5" + M, "3+"],
  ["N has 5 valence electrons; gaining 3 reaches an octet (neon's configuration): N<sup>3" + M + "</sup>, nitride.",
   "Losing 5 electrons is much harder than gaining 3.",
   "Gaining 5 would give 10 valence electrons, more than an octet.",
   "Losing 3 would leave 2 valence electrons, not a full octet, and nonmetals tend to gain."],
  "How many steps is nitrogen from neon?",
  "Group 15 has 5 valence electrons; nitrogen gains 3: <b>N<sup>3" + M + "</sup></b>. (In ammonia itself, nitrogen shares electrons instead; that is Chapter 6.)", 2)

Q(T, "Which electrolyte ion has <b>18 electrons</b>?",
  [ion("K", 1), ion("Na", 1), ion("Mg", 2), ion("F", -1)],
  ["K has 19 electrons; K<sup>+</sup> has 18, the same as argon.",
   "Na<sup>+</sup> has 11 " + M + " 1 = 10.",
   "Mg<sup>2+</sup> has 12 " + M + " 2 = 10.",
   "F<sup>" + M + "</sup> has 9 + 1 = 10."],
  "Electrons = atomic number " + M + " charge.",
  "<b>K<sup>+</sup></b>: 19 " + M + " 1 = 18 electrons, isoelectronic with argon. The other three each have 10, like neon.", 2)

Q(T, "Carbon is in group 14 and has 4 valence electrons. Why does carbon usually <b>share</b> electrons instead of forming an ion?",
  ["It is halfway to an octet: it would have to gain 4 or lose 4 electrons, both hard to do.",
   "Carbon already has a full octet.",
   "Carbon has no valence electrons.",
   "Carbon is a metal, and metals always share electrons."],
  ["Gaining or losing 4 electrons takes a lot of energy, so carbon reaches an octet by sharing (covalent bonds, Chapter 6).",
   "Carbon has 4 valence electrons, half of an octet.",
   "Carbon has 4 valence electrons (2s<sup>2</sup> 2p<sup>2</sup>).",
   "Carbon is a nonmetal; metals tend to lose electrons, not share them."],
  "How far is carbon from the nearest noble gas in each direction?",
  "Carbon is 4 steps from helium and 4 from neon, so forming an ion would mean moving 4 electrons either way. <b>Sharing</b> lets it reach an octet more easily.", 2)

Q(T, "Gallium (row 4, group 13) is [Ar] 4s<sup>2</sup> 3d<sup>10</sup> 4p<sup>1</sup>. How many valence electrons does it have?",
  ["3", "13", "1", "31"],
  ["The highest shell is n = 4: 4s<sup>2</sup> 4p<sup>1</sup> = 3. The 3d electrons are in shell 3 and do not count.",
   "13 counts the 3d electrons too (2 + 10 + 1). Only highest-shell s and p electrons are valence electrons.",
   "1 counts only the 4p electron; the 4s electrons are in the same shell.",
   "31 is gallium's total number of electrons."],
  "Which shell is highest? Count only the electrons in it.",
  "Highest shell n = 4: 4s<sup>2</sup> 4p<sup>1</sup>, <b>3 valence electrons</b>, matching group 13: 13 " + M + " 10 = 3.", 3)

# ---------------- ch03-trends (6) ----------------
T = 'ch03-trends'
Q(T, "Rank K, Mg and Cl in order of <b>increasing</b> atomic radius.",
  ["Cl &lt; Mg &lt; K", "K &lt; Mg &lt; Cl", "Mg &lt; Cl &lt; K", "Cl &lt; K &lt; Mg"],
  ["Mg and Cl are in row 3, with Cl farther right (smaller). K is in row 4 and group 1, farther down and left than either, so it is largest.",
   "This is decreasing radius.",
   "Cl is to the right of Mg in the same row, so Cl is smaller.",
   "K is farther down (one more shell) and farther left than Mg, so K is larger than Mg."],
  "Sketch the three on a tiny periodic table. Bigger toward the lower left.",
  "Smallest at the upper right, largest at the lower left: <b>Cl &lt; Mg &lt; K</b>.", 2)

Q(T, "Rank Ca, Br and Kr in order of <b>increasing</b> first ionization energy.",
  ["Ca &lt; Br &lt; Kr", "Kr &lt; Br &lt; Ca", "Br &lt; Ca &lt; Kr", "Ca &lt; Kr &lt; Br"],
  ["All three are in row 4; ionization energy increases left to right, and the noble gas (Kr) is highest.",
   "This is decreasing ionization energy.",
   "Ca, a group 2 metal on the left, has a lower ionization energy than Br.",
   "Kr is farther right than Br and has a full shell, so its ionization energy is higher."],
  "Same row: which way does ionization energy increase?",
  "Across row 4, ionization energy increases: <b>Ca &lt; Br &lt; Kr</b>.", 2)

Q(T, "Which is smaller, a magnesium atom or a magnesium ion (Mg<sup>2+</sup>), and why?",
  ["Mg<sup>2+</sup>, because it has lost its 3s electrons, so its outermost electrons are in shell 2.",
   "Mg, because the ion has gained electrons.",
   "Mg, because the ion has more protons.",
   "They are the same size, since both have 12 protons."],
  ["Losing the whole 3s shell leaves the ion with neon's configuration, one shell smaller, and 12 protons pull on only 10 electrons.",
   "A 2+ ion has lost electrons, not gained them.",
   "The proton count does not change when an ion forms.",
   "The number of electrons, and the highest occupied shell, did change."],
  "Write the configuration of each. Which shell is the outermost?",
  "Mg is [Ne] 3s<sup>2</sup>; Mg<sup>2+</sup> is [Ne]. Losing shell 3 makes <b>Mg<sup>2+</sup></b> much smaller. Cations are smaller than their atoms.", 2)

Q(T, "Fluoride in toothpaste and water strengthens tooth enamel. Which is larger, a fluorine atom (F) or a fluoride ion (F<sup>" + M + "</sup>)?",
  ["F<sup>" + M + "</sup>, because the extra electron increases repulsion and the electron cloud spreads out.",
   "F, because the ion has lost an electron.",
   "F, because the extra electron is pulled in tightly.",
   "They are the same size."],
  ["An anion is larger than its atom: 10 electrons around 9 protons spread out more than 9 electrons do.",
   "F<sup>" + M + "</sup> has <i>gained</i> an electron; the negative sign shows extra electrons.",
   "Adding an electron adds repulsion with no extra protons, so the cloud grows.",
   "The electron count changed, so the size changed."],
  "Is the fluoride ion an anion or a cation?",
  "Anions are larger than their atoms, so <b>F<sup>" + M + "</sup></b> is larger than F.", 2)

Q(T, "Which element has the highest first ionization energy of <b>all</b> the elements?",
  ["Helium", "Francium", "Fluorine", "Hydrogen"],
  ["Helium is at the very top of the noble gases, the farthest up and right, with a full 1s shell close to the nucleus.",
   "Francium, at the lower left, has one of the <i>lowest</i> ionization energies.",
   "Fluorine is high, but the noble gases at the ends of rows 1 and 2, farther right, are higher still.",
   "Hydrogen's single 1s electron feels a nuclear charge of only 1+; the other element in row 1 has 2 protons and holds its electrons more tightly."],
  "Ionization energy is highest toward the upper right.",
  "<b>Helium</b> has the highest ionization energy: it is at the top right, with its full 1s shell held by 2 protons.", 1)

Q(T, "Which row-3 element has the most <b>metallic character</b>: Na, Mg, Al or Si?",
  ["Na", "Mg", "Al", "Si"],
  ["Sodium is farthest left in row 3, so it has the lowest ionization energy and loses its electron most easily.",
   "Mg is a metal but holds its electrons more tightly than Na.",
   "Al is farther right than Na and Mg, so it is less metallic.",
   "Si is a metalloid, on the staircase between metals and nonmetals."],
  "Metallic character goes the opposite way to ionization energy.",
  "Metallic character increases toward the lower left; within a row, the leftmost element is most metallic: <b>Na</b>.", 1)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
import collections
print(len(B), dict(collections.Counter(q['t'] for q in B)))
