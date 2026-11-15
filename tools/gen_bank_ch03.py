#!/usr/bin/env python3
"""Builds bank/ch03.json (Chapter 3 Try It items). Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch03.py bank/ch03.json
Numbers in calculation items are computed here with c = 3.00e8 m s^-1 and h = 6.626e-34 J s and rounded once
at the end; tools/check_bank_ch03.py recomputes every one of them independently."""
import json, sys, math
from decimal import Decimal, ROUND_HALF_UP
OUT = sys.argv[1]
C, H = 3.00e8, 6.626e-34
M = '&minus;'
UP, DN, UD, E0 = '[↑]', '[↓]', '[↑↓]', '[&nbsp;&nbsp;]'
B = []
def Q(t, q, c, y, h, w, d, k=0, f=None):
    it = {"id": "c3-%03d" % (len(B) + 1), "t": t, "q": q, "c": c, "y": y, "h": h, "w": w, "d": d, "k": k}
    if f: it["f"] = f
    B.append(it)

def num(x, n=3):
    """x to n significant figures: plain decimal for 0.01 <= x < 1000, otherwise m &times; 10<sup>e</sup>."""
    e = math.floor(math.log10(abs(x)))
    m = Decimal(repr(x / 10 ** e)).quantize(Decimal(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if m >= 10: m = (m / 10).quantize(Decimal(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP); e += 1
    if -2 <= e <= 2:
        v = m * Decimal(10) ** e
        return ('%.' + str(max(0, n - 1 - e)) + 'f') % v
    return '%s &times; 10<sup>%s</sup>' % (m, (M + str(-e)) if e < 0 else str(e))
def sup(s): return s.replace('^', '')
def cfg(s):
    """'1s2 2s2 2p6' -> HTML with superscripts; '[Ne] 3s2' keeps the bracket."""
    out = []
    for tok in s.split():
        if tok.startswith('['): out.append(tok)
        else: out.append(tok[:2] + '<sup>' + tok[2:] + '</sup>')
    return ' '.join(out)
def ion(sym, ch):
    if not ch: return sym
    mag = '' if abs(ch) == 1 else str(abs(ch))
    return sym + '<sup>' + mag + ('+' if ch > 0 else M) + '</sup>'
PT_SHOW = {"H": [1, 1], "He": [1, 18]}

# ======================= ch03-light (12) =======================
T = 'ch03-light'
Q(T, "On a drawing of a light wave, what does the <b>wavelength</b> measure?",
  ["The distance from one peak of the wave to the next peak",
   "The number of peaks that pass a point each second",
   "The height of a peak above the middle line of the wave",
   "The speed at which the wave travels"],
  ["Wavelength (&lambda;) is a length: the distance from one peak to the next, often given in nanometers for light.",
   "Peaks per second is the frequency (&nu;), measured in hertz (s<sup>" + M + "1</sup>).",
   "The height of the wave is its amplitude, which relates to brightness, not to the color or energy of each photon.",
   "All light travels at the same speed in a vacuum, c = 3.00 &times; 10<sup>8</sup> m s<sup>" + M + "1</sup>, whatever its wavelength."],
  "Wavelength has units of length, such as nanometers or meters.",
  "The <b>wavelength</b>, &lambda;, is the distance from one peak to the next. The frequency, &nu;, counts peaks per second. They are tied together by c = &lambda;&nu;.", 1)

Q(T, "Light of one color is replaced by light whose wavelength is <b>twice as long</b>. What happens to the frequency?",
  ["It is cut in half.", "It doubles.", "It stays the same, because the speed of light does not change.", "It increases four times."],
  ["c = &lambda;&nu; and c is fixed, so if &lambda; doubles, &nu; must drop to half to keep the product the same.",
   "Wavelength and frequency are inversely related; they cannot both go up while their product stays equal to c.",
   "The speed stays the same, and that is exactly why the frequency has to change when the wavelength does.",
   "Frequency changes by the same factor as the wavelength (2), only in the opposite direction; nothing is squared in c = &lambda;&nu;."],
  "The product of wavelength and frequency is always the speed of light.",
  "Because &lambda;&nu; = c is constant, doubling &lambda; means &nu; is <b>cut in half</b>. Longer waves pass a point less often.", 1)

nu = C / 589e-9
Q(T, "Some older street lamps in Valley towns glow yellow-orange because they contain sodium vapor, which gives off light at 589 nm. What is the frequency of this light?",
  [num(nu) + " Hz", num(C / 589) + " Hz", num(C * 589e-9) + " Hz", num(589e-9 / C) + " Hz"],
  ["Convert first: 589 nm = 5.89 &times; 10<sup>" + M + "7</sup> m. Then &nu; = c/&lambda; = (3.00 &times; 10<sup>8</sup> m s<sup>" + M + "1</sup>)/(5.89 &times; 10<sup>" + M + "7</sup> m), about 10<sup>14</sup> Hz, the size expected for visible light.",
   "This divides by 589 without changing nanometers to meters. The speed of light is in meters per second, so &lambda; must be in meters.",
   "This multiplies c by &lambda;. Solving c = &lambda;&nu; for &nu; means dividing c by &lambda;.",
   "This divides &lambda; by c, which is upside down; the units come out as seconds, not s<sup>" + M + "1</sup>."],
  "Put the wavelength in meters first, then solve c = &lambda;&nu; for &nu; and check which unit is left.",
  "589 nm &times; (10<sup>" + M + "9</sup> m / 1 nm) = 5.89 &times; 10<sup>" + M + "7</sup> m. &nu; = c/&lambda; = (3.00 &times; 10<sup>8</sup>)/(5.89 &times; 10<sup>" + M + "7</sup>) = <b>" + num(nu) + " Hz</b> (3 significant figures).", 2, 1)

lam = C / 6.39e7
Q(T, "A 1.5-tesla MRI scanner sends radio-frequency pulses at 6.39 &times; 10<sup>7</sup> Hz. What is the wavelength of these radio waves?",
  [num(lam) + " m", num(6.39e7 / C) + " m", num(C * 6.39e7) + " m", num(lam) + " nm"],
  ["&lambda; = c/&nu; = (3.00 &times; 10<sup>8</sup> m s<sup>" + M + "1</sup>)/(6.39 &times; 10<sup>7</sup> s<sup>" + M + "1</sup>). The seconds cancel and leave meters; radio waves are meters long, as expected.",
   "This divides &nu; by c, which is upside down; the units would be m<sup>" + M + "1</sup>, not meters.",
   "This multiplies c by &nu;. Solving c = &lambda;&nu; for &lambda; means dividing c by &nu;.",
   "The number is right, but the unit is not. c is in meters per second, so &lambda; comes out in meters; calling it nanometers makes it a billion times too small."],
  "Solve c = &lambda;&nu; for &lambda;, and check which unit is left after the seconds cancel.",
  "&lambda; = c/&nu; = (3.00 &times; 10<sup>8</sup> m s<sup>" + M + "1</sup>)/(6.39 &times; 10<sup>7</sup> s<sup>" + M + "1</sup>) = <b>" + num(lam) + " m</b>. Radio waves are the longest waves in the spectrum, so a wavelength of a few meters makes sense.", 2, 1)

E = H * 1.18e15
Q(T, "Germicidal UV-C light used to disinfect biosafety cabinets has a frequency of 1.18 &times; 10<sup>15</sup> Hz. What is the energy of one photon of this light?",
  [num(E) + " J", num(H / 1.18e15) + " J", num(1.18e15 / H) + " J", num(H * C / 1.18e15) + " J"],
  ["E = h&nu; = (6.626 &times; 10<sup>" + M + "34</sup> J s)(1.18 &times; 10<sup>15</sup> s<sup>" + M + "1</sup>). Seconds cancel and leave joules: a tiny energy, as expected for one photon.",
   "This divides h by &nu;. The equation is E = h&nu;, a product: higher frequency must give more energy.",
   "This divides &nu; by h, giving an impossibly huge energy for a single photon.",
   "This uses hc/&nu;, mixing up E = hc/&lambda; with E = h&nu;. When frequency is given, multiply h by &nu; and leave c out."],
  "Which equation links energy directly to frequency, with no speed of light in it?",
  "E = h&nu; = (6.626 &times; 10<sup>" + M + "34</sup> J s)(1.18 &times; 10<sup>15</sup> s<sup>" + M + "1</sup>) = <b>" + num(E) + " J</b> (3 significant figures, set by the frequency).", 2, 1)

E = H * C / 455e-9
Q(T, "Newborn jaundice is often treated with phototherapy, blue light that the baby's skin absorbs. One phototherapy lamp uses LEDs that give off light at 455 nm. What is the energy of one photon of this light?",
  [num(E) + " J", num(H * C / 455) + " J", num(C / 455e-9) + " J", num(H / 455e-9) + " J"],
  ["455 nm = 4.55 &times; 10<sup>" + M + "7</sup> m, and E = hc/&lambda; = (6.626 &times; 10<sup>" + M + "34</sup> J s)(3.00 &times; 10<sup>8</sup> m s<sup>" + M + "1</sup>)/(4.55 &times; 10<sup>" + M + "7</sup> m). Visible photons are a few times 10<sup>" + M + "19</sup> J.",
   "This leaves the wavelength in nanometers, so the energy is a billion (10<sup>9</sup>) times too small.",
   "This is the frequency, c/&lambda;, with joules written after it. One more step, E = h&nu;, turns the frequency into an energy.",
   "This divides h by &lambda; and leaves out the speed of light. The combined equation is E = hc/&lambda;."],
  "Convert nm to m, then either find &nu; first or use the combined equation E = hc/&lambda;.",
  "&lambda; = 4.55 &times; 10<sup>" + M + "7</sup> m. E = hc/&lambda; = (6.626 &times; 10<sup>" + M + "34</sup>)(3.00 &times; 10<sup>8</sup>)/(4.55 &times; 10<sup>" + M + "7</sup>) = <b>" + num(E) + " J</b>. This is context only: the energy of one photon, not a dose.", 3, 1)

Q(T, "Which list puts these regions of the electromagnetic spectrum in order of <b>increasing photon energy</b>?",
  ["radio waves &lt; infrared &lt; ultraviolet &lt; X-rays",
   "X-rays &lt; ultraviolet &lt; infrared &lt; radio waves",
   "infrared &lt; radio waves &lt; ultraviolet &lt; X-rays",
   "radio waves &lt; ultraviolet &lt; infrared &lt; X-rays"],
  ["Energy rises as wavelength gets shorter: radio waves are longest and X-rays are shortest of these four.",
   "This is the order of increasing <i>wavelength</i>, which is the order of decreasing energy.",
   "Radio waves have longer wavelengths than infrared, so radio photons have the least energy.",
   "Infrared sits next to red light on the long-wavelength side of the visible band; ultraviolet sits past violet and carries more energy."],
  "Shorter wavelength means more energy per photon. Visible light sits between infrared and ultraviolet.",
  "From long wavelength to short: radio, microwave, infrared, visible, ultraviolet, X-ray, gamma. Energy rises in the same order, so <b>radio &lt; infrared &lt; ultraviolet &lt; X-rays</b>.", 1)

Q(T, "A pulse oximeter shines red light at 660 nm and infrared light at 940 nm through a fingertip. Which statement compares the two photons correctly?",
  ["The 660 nm photon has the higher frequency and the higher energy.",
   "The 940 nm photon has the higher energy, because its wavelength is larger.",
   "The 940 nm photon has the higher frequency, but the 660 nm photon has the higher energy.",
   "Both photons have the same energy, because both travel at the speed of light."],
  ["The shorter wavelength (660 nm) goes with the higher frequency, and E = h&nu;, so it also has the higher energy.",
   "Energy and wavelength are inversely related: the longer 940 nm wave has less energy per photon.",
   "Frequency and energy always go together (E = h&nu;); a photon cannot have the higher frequency and the lower energy.",
   "Every photon travels at c, but its energy depends on its frequency, and these frequencies differ."],
  "Wavelength goes one way; frequency and energy go the other way together.",
  "Shorter wavelength means higher frequency (c = &lambda;&nu;) and higher energy (E = h&nu;). The <b>660 nm red photon</b> has the higher frequency and energy, about 940/660 &asymp; 1.4 times that of the infrared photon.", 2)

Q(T, "A dental assistant turns a curing light to a brighter setting without changing its color. What changes?",
  ["More photons come out each second; each photon has the same energy as before.",
   "Each photon now has more energy.",
   "The wavelength of the light gets shorter.",
   "The frequency of the light goes up."],
  ["Brightness is the number of photons. The energy of each photon depends only on its wavelength, which did not change.",
   "Photon energy is set by wavelength (E = hc/&lambda;). Same color, same wavelength, same energy per photon.",
   "Changing the wavelength would change the color; the color stayed the same.",
   "A higher frequency would mean a shorter wavelength and a different color."],
  "What sets the energy of a single photon? Did that quantity change?",
  "A brighter light sends out <b>more photons</b>, but each photon's energy depends only on its wavelength (E = hc/&lambda;), which is unchanged because the color is the same.", 2)

Q(T, "Radiology staff wear dosimeters and lead aprons around X-ray equipment, but nobody worries about the radio waves from a cell phone in the same way. Why?",
  ["Each X-ray photon has enough energy to knock electrons out of atoms; each radio photon has far too little.",
   "X-rays travel faster than radio waves.",
   "Radio waves have shorter wavelengths, so they pass through the body without stopping.",
   "Radio waves are not electromagnetic radiation."],
  ["X-rays have very short wavelengths and very high photon energies, enough to ionize atoms and damage DNA. Radio photons are billions of times weaker.",
   "All electromagnetic radiation travels at the same speed, c.",
   "Radio waves have the <i>longest</i> wavelengths in the spectrum, and long wavelength means low energy.",
   "Radio waves are electromagnetic radiation, at the long-wavelength, low-energy end of the spectrum."],
  "Compare the energy of one photon in each region.",
  "X-rays and gamma rays are called <b>ionizing radiation</b> because each photon carries enough energy to knock electrons out of atoms. Radio photons have very long wavelengths and very low energies, too little to break bonds or ionize atoms.", 1)

r = 589 / 254
Q(T, "A UV-C germicidal lamp gives off light at 254 nm, and a sodium lamp gives off light at 589 nm. About how many times more energy does one UV-C photon carry than one sodium-lamp photon?",
  [num(r) + " times", num(254 / 589) + " times", "%d times" % (589 - 254), num(r ** 2) + " times"],
  ["E = hc/&lambda;, so the ratio of energies is the inverse ratio of wavelengths: 589/254. h and c cancel, so you do not need them.",
   "This is 254/589, the ratio the wrong way up; it says the UV-C photon has <i>less</i> energy, but its shorter wavelength means it has more.",
   "This subtracts the wavelengths. A ratio of energies needs division, and the answer has no units of nm.",
   "This squares the wavelength ratio. Energy is inversely proportional to wavelength itself, not to its square."],
  "Write E = hc/&lambda; for each photon and divide one by the other. What cancels?",
  "E<sub>UV</sub>/E<sub>Na</sub> = (hc/254 nm)/(hc/589 nm) = 589/254 = <b>" + num(r) + "</b>. Shorter wavelength, more energy: each UV-C photon carries a bit more than twice the energy, enough to damage the DNA of microbes.", 3, 1)

Q(T, "The table lists light used in four settings. Which photon has the <b>lowest frequency</b>?",
  ["Near-infrared light measured by an orchard-imaging drone", "Sodium street lamp", "Dental curing light", "Germicidal UV-C lamp"],
  ["850 nm is the longest wavelength in the table, and the longest wavelength has the lowest frequency (c = &lambda;&nu;).",
   "589 nm is shorter than 850 nm, so the sodium lamp's light has a higher frequency than the near-infrared light.",
   "470 nm is shorter than both 589 nm and 850 nm, so its frequency is higher than theirs.",
   "254 nm is the shortest wavelength in the table, so UV-C has the <i>highest</i> frequency here."],
  "Frequency and wavelength are inversely related.",
  "Because c = &lambda;&nu;, the longest wavelength has the lowest frequency: <b>near-infrared, 850 nm</b>. In order of increasing frequency: 850 nm &lt; 589 nm &lt; 470 nm &lt; 254 nm.", 2, 0,
  [{"type": "table", "cap": "Light used in four settings", "head": ["Source", "Wavelength (nm)"],
    "rows": [["Sodium street lamp", "589"], ["Germicidal UV-C lamp", "254"], ["Near-infrared light measured by an orchard-imaging drone", "850"], ["Dental curing light", "470"]]}])

# ======================= ch03-bohr (9) =======================
T = 'ch03-bohr'
Q(T, "White light from a bulb passes through a prism and spreads into a smooth rainbow. Light from a hydrogen discharge tube shows only a few sharp colored lines. What are these two kinds of spectra called?",
  ["The rainbow is a continuous spectrum; the hydrogen lines are a line (emission) spectrum.",
   "The rainbow is a line spectrum; the hydrogen lines are a continuous spectrum.",
   "Both are continuous spectra, because both come from light.",
   "Both are emission spectra, so they always look the same."],
  ["A continuous spectrum contains every color blending smoothly; a line spectrum has only certain wavelengths, which is what a glowing gas gives off.",
   "This swaps the names: the smooth rainbow with no gaps is the continuous one.",
   "The hydrogen tube gives only a few colors with dark gaps between them, so its spectrum is not continuous.",
   "They look very different: one has every color, the other only a few lines. Each element's line spectrum is its own pattern."],
  "Continuous means no gaps.",
  "White light gives a <b>continuous spectrum</b>, every color with no gaps. A glowing gas such as hydrogen gives a <b>line (emission) spectrum</b>: only certain wavelengths, a pattern unique to that element.", 1)

Q(T, "In a hydrogen atom, which electron jump gives off a photon of light?",
  ["n = 4 to n = 2", "n = 1 to n = 3", "n = 2 to n = 5", "n = 2 to n = 2"],
  ["The electron drops to a lower level, and the energy difference leaves as one photon.",
   "Moving up from n = 1 to n = 3 needs energy; the atom absorbs a photon instead of giving one off.",
   "Moving up from n = 2 to n = 5 needs energy, so it is absorption, not emission.",
   "Staying in the same level involves no energy change, so no photon is given off."],
  "Up arrows absorb energy; down arrows give off light.",
  "Emission happens when an electron <b>drops to a lower level</b>: n = 4 to n = 2 releases the energy difference as a photon (hydrogen's 486 nm blue-green line). Upward jumps absorb energy.", 1)

Q(T, "In hydrogen, the drop from n = 3 to n = 2 gives the red line at 656 nm, and the drop from n = 4 to n = 2 gives the blue-green line at 486 nm. Why does the n = 4 to n = 2 drop give the shorter wavelength?",
  ["It is a bigger energy drop, so its photon has more energy, and more energy means a shorter wavelength.",
   "It is a smaller energy drop, and smaller drops give shorter wavelengths.",
   "Electrons in higher levels move faster, so the light they give off moves faster.",
   "Blue-green light is brighter than red light."],
  ["n = 4 is higher than n = 3, so falling from n = 4 to n = 2 releases more energy; by E = hc/&lambda;, a larger E means a smaller &lambda;.",
   "Falling from n = 4 is a <i>bigger</i> drop than falling from n = 3 to the same level, and a bigger drop gives the shorter wavelength.",
   "All light travels at the same speed, c; the difference is in the energy of each photon.",
   "Brightness depends on how many photons are given off, not on the wavelength of each one."],
  "Compare how far the electron falls in each case, then use E = hc/&lambda;.",
  "Falling from n = 4 to n = 2 is a <b>bigger energy drop</b> than n = 3 to n = 2. A bigger drop gives a higher-energy photon, and since E = hc/&lambda;, a higher energy means a shorter wavelength: 486 nm instead of 656 nm.", 2)

Q(T, "A flame test turns a flame bright yellow-orange for sodium, red for strontium, and blue-green for copper. What does the Bohr model say causes each element's own colors?",
  ["Each element has its own set of fixed energy levels, so its electrons can drop only by certain amounts, giving only certain wavelengths.",
   "Each element absorbs every wavelength equally and gives off the leftover colors.",
   "The color depends only on how hot the flame is.",
   "Electrons can have any energy, so each element picks a favorite color."],
  ["Fixed levels mean fixed energy gaps, and each gap gives a photon of one particular wavelength. The set of gaps is different for every element.",
   "The colors come from electrons dropping between that element's own levels, not from leftovers of absorbed light.",
   "The same flame gives different colors for different elements, so the element, not just the heat, sets the color.",
   "In the Bohr model electron energies are quantized: only certain values are allowed, with nothing in between."],
  "Think about the staircase picture: which steps does each element have?",
  "Heat excites the electrons; when they drop back, each drop releases a photon whose energy equals the gap. Because <b>each element has its own fixed energy levels</b>, it gives off its own set of wavelengths, like a bar code.", 2)

Q(T, "Which statement describes an atom in an <b>excited state</b>?",
  ["At least one electron has absorbed energy and is in a higher level than it would be in the ground state.",
   "All of its electrons are in the lowest energy levels available.",
   "It has lost an electron and become a positive ion.",
   "Its electrons sit between two energy levels."],
  ["An excited state is any arrangement with more energy than the ground state, reached by absorbing energy from heat, electricity or light.",
   "Electrons all in the lowest available levels is the ground state.",
   "Losing an electron entirely is ionization; an excited electron is still in the atom, just in a higher level.",
   "Electrons can only be <i>in</i> a level, never between levels; energy is quantized."],
  "Excitation is the step that comes before an atom gives off light.",
  "In the <b>excited state</b>, an electron has absorbed energy and jumped to a higher level. It soon drops back to the ground state and gives off the energy difference as a photon.", 1)

Q(T, "Which statement about the Bohr model is <b>true</b>?",
  ["It explains hydrogen's line spectrum well, but it does not work for atoms with more than one electron.",
   "It describes electrons as clouds called orbitals.",
   "It says electrons can have any amount of energy.",
   "It was replaced because it could not explain hydrogen's spectrum."],
  ["Bohr's fixed energy levels predict hydrogen's lines very well; for atoms with more electrons the model fails, so the quantum-mechanical model took over.",
   "Orbitals belong to the later quantum-mechanical model; Bohr pictured electrons moving in fixed circular orbits.",
   "The central idea of the Bohr model is the opposite: electron energies are quantized.",
   "Hydrogen's spectrum is exactly what the Bohr model gets right; it falls short for other atoms."],
  "What did Bohr set out to explain, and what happened when the model was tried on other atoms?",
  "The Bohr model's quantized energy levels <b>explain hydrogen's lines</b>, and that central idea is still correct. But it <b>fails for atoms with more than one electron</b>, and electrons do not move in neat orbits; the quantum-mechanical model, with orbitals, replaced it.", 2)

E = H * C / 486e-9
Q(T, "Hydrogen's blue-green line has a wavelength of 486 nm. What is the energy of one photon of this light?",
  [num(E) + " J", num(H * C / 486) + " J", num(H / 486e-9) + " J", num(C / 486e-9) + " J"],
  ["486 nm = 4.86 &times; 10<sup>" + M + "7</sup> m; E = hc/&lambda; = (6.626 &times; 10<sup>" + M + "34</sup> J s)(3.00 &times; 10<sup>8</sup> m s<sup>" + M + "1</sup>)/(4.86 &times; 10<sup>" + M + "7</sup> m).",
   "This leaves &lambda; in nanometers, so the energy comes out 10<sup>9</sup> times too small.",
   "This divides h by &lambda; and leaves out c. The combined equation is E = hc/&lambda;.",
   "This is c/&lambda;, the frequency in Hz; multiply it by h to get the energy."],
  "Change nm to m before you divide, and make sure the units left over are joules.",
  "E = hc/&lambda; = (6.626 &times; 10<sup>" + M + "34</sup>)(3.00 &times; 10<sup>8</sup>)/(4.86 &times; 10<sup>" + M + "7</sup>) = <b>" + num(E) + " J</b>, the energy gap between hydrogen's n = 4 and n = 2 levels.", 3, 1)

Q(T, "A sodium street lamp gives off mostly yellow-orange light near 589 nm instead of a full rainbow. What does this tell you?",
  ["Sodium's electrons can drop only between certain energy levels, so only certain wavelengths are given off.",
   "Sodium atoms absorb all colors except yellow-orange.",
   "The lamp's glass filters out the other colors.",
   "Yellow-orange light has the most energy of all visible colors."],
  ["A lamp full of glowing sodium gives sodium's line spectrum, whose strongest lines are near 589 nm, because only certain energy drops are possible.",
   "The light comes from electrons dropping in excited sodium atoms; it is emitted, not left over after absorption.",
   "The color comes from the sodium atoms themselves; every sodium source, even a flame test, gives the same yellow-orange.",
   "Violet light has the most energy of the visible colors; yellow-orange is in the middle-to-low part."],
  "Is the light from a glowing gas a continuous spectrum or a line spectrum?",
  "Sodium's electrons have only certain allowed energies, so only certain drops, and therefore <b>only certain wavelengths</b>, are possible. Its strongest lines are yellow-orange, near 589 nm.", 1)

Q(T, "The table gives hydrogen's four visible emission lines. Each line comes from an electron dropping to n = 2. The 434 nm line comes from a drop from which level?",
  ["n = 5 to n = 2", "n = 2 to n = 5", "n = 3 to n = 2", "n = 7 to n = 2"],
  ["The lines from n = 3 (656 nm) and n = 4 (486 nm) are given; the next-shorter wavelength, 434 nm, is the next-bigger drop, from n = 5.",
   "Emission lines come from electrons dropping down; n = 2 to n = 5 is a jump up that absorbs energy.",
   "n = 3 to n = 2 is the smallest of these drops and gives the longest wavelength, the 656 nm red line.",
   "Higher starting levels give even shorter wavelengths; 410 nm is from n = 6, so a drop from n = 7 would be shorter still."],
  "Order the lines from longest to shortest wavelength; each step shorter is one level higher.",
  "Bigger drop, shorter wavelength. 656 nm is n = 3 &rarr; 2 and 486 nm is n = 4 &rarr; 2, so 434 nm is <b>n = 5 &rarr; 2</b> and 410 nm is n = 6 &rarr; 2.", 3, 0,
  [{"type": "table", "cap": "Visible emission lines of hydrogen", "head": ["Wavelength (nm)", "Color", "Drop"],
    "rows": [["656", "red", "n = 3 to n = 2"], ["486", "blue-green", "n = 4 to n = 2"], ["434", "blue-violet", "?"], ["410", "violet", "n = 6 to n = 2"]]}])

# ======================= ch03-orbitals (11) =======================
T = 'ch03-orbitals'
Q(T, "What is the greatest number of electrons that one orbital can hold?",
  ["2", "1", "6", "8"],
  ["By the Pauli exclusion principle, an orbital holds at most two electrons, and they must have opposite spins.",
   "An orbital can hold a second electron if its spin is opposite to the first.",
   "6 is the capacity of a whole p subshell, which is three orbitals.",
   "8 is the capacity of the whole second shell (2s plus 2p)."],
  "Think about the arrows in one box of an orbital diagram.",
  "Each orbital holds at most <b>2 electrons</b>, drawn as one up arrow and one down arrow (&uarr;&darr;). Subshells hold more only because they contain more orbitals.", 1)

Q(T, "How many orbitals are in a <b>p subshell</b>, and how many electrons can the subshell hold?",
  ["3 orbitals, 6 electrons", "1 orbital, 6 electrons", "3 orbitals, 3 electrons", "6 orbitals, 12 electrons"],
  ["A p subshell has three orbitals (pointing along x, y and z), and each holds 2 electrons: 3 &times; 2 = 6.",
   "A p subshell is three separate orbitals; a single orbital can never hold more than 2 electrons.",
   "Each of the three orbitals can hold 2 electrons, not 1, so the subshell holds 6.",
   "6 is the number of electrons, not the number of orbitals."],
  "Each orbital holds 2 electrons. How many directions do the p orbitals point in?",
  "The p subshell has <b>3 orbitals</b>, each holding 2 electrons, so it holds <b>6 electrons</b>. That is also why the p block of the periodic table is 6 columns wide.", 1)

Q(T, "How many electrons can the <b>fourth shell</b> (n = 4) hold in all?",
  ["32", "8", "18", "16"],
  ["Shell 4 has 4s, 4p, 4d and 4f subshells: 2 + 6 + 10 + 14 = 32, which matches 2n<sup>2</sup> = 2(4)<sup>2</sup>.",
   "8 counts only the 4s and 4p subshells; shell 4 also has 4d and 4f.",
   "18 is the capacity of shell 3 (3s, 3p, 3d); shell 4 adds an f subshell.",
   "16 is n<sup>2</sup> = 4<sup>2</sup>, the number of <i>orbitals</i> in shell 4; each orbital holds 2 electrons."],
  "List the subshells in shell 4 (shell n has n kinds of subshells), then add their capacities.",
  "Shell 4 has four subshells: 4s (2), 4p (6), 4d (10) and 4f (14). Total = <b>32 electrons</b> (2n<sup>2</sup> with n = 4).", 2)

Q(T, "Which description matches the <b>shapes</b> of s and p orbitals?",
  ["An s orbital is a sphere around the nucleus; a p orbital has two lobes on opposite sides of the nucleus.",
   "An s orbital has two lobes; a p orbital is a sphere.",
   "Both are spheres, but p orbitals are larger.",
   "Both are flat circles, like the orbits in the Bohr model."],
  ["s orbitals are spherical, and the three p orbitals are dumbbell-shaped, pointing along x, y and z.",
   "This swaps them: the sphere is the s orbital and the two-lobed dumbbell is the p orbital.",
   "A p orbital is not a sphere; its two lobes sit on opposite sides of the nucleus.",
   "Orbitals are three-dimensional regions where an electron is likely to be found, not flat circular paths."],
  "One of these orbital types has no direction to it; the other points along an axis.",
  "An <b>s orbital is a sphere</b> centered on the nucleus (a 2s sphere is bigger than a 1s). A <b>p orbital has two lobes</b>, like a dumbbell, and the three p orbitals point along three perpendicular directions.", 1)

Q(T, "A student draws the 2p subshell of a nitrogen atom as 2p [↑↓][↑][&nbsp;&nbsp;]. Which rule is broken?",
  ["Hund's rule", "The Pauli exclusion principle", "The Aufbau principle", "No rule is broken; the diagram is correct."],
  ["Hund's rule: in equal-energy orbitals, put one electron in each, all with the same spin, before pairing any. The three 2p electrons should be [↑][↑][↑].",
   "Pauli says no orbital holds more than 2 electrons, and paired electrons have opposite spins; the paired box here does follow that.",
   "The Aufbau principle is about filling lower-energy subshells first; all three boxes here are the same 2p subshell.",
   "Two 2p electrons are paired while a 2p orbital is still empty, which is not allowed in the ground state."],
  "All three 2p orbitals have the same energy. How should electrons spread among equal-energy orbitals?",
  "In equal-energy orbitals, electrons go one per orbital with the same spin before any pair up (<b>Hund's rule</b>), like passengers taking empty bus seats first. Nitrogen's 2p is [↑][↑][↑], with 3 unpaired electrons.", 2)

Q(T, "Which orbital box breaks the <b>Pauli exclusion principle</b>?",
  ["[↑↑]", "[↑↓]", "[↑]", "[&nbsp;&nbsp;]"],
  ["Two electrons in one orbital must have opposite spins; two up arrows in one box means the same spin twice.",
   "One up and one down arrow is a correctly paired orbital.",
   "One electron in an orbital is allowed.",
   "An empty orbital breaks no rule; it may simply not be needed."],
  "Pauli limits what can share a box: how many electrons, and with what spins?",
  "The Pauli exclusion principle allows at most two electrons per orbital, with <b>opposite spins</b>. <b>[↑↑]</b> puts two same-spin electrons in one box, so it is not allowed.", 2)

Q(T, "Following the Aufbau principle, which subshell fills <b>right after 3p</b>?",
  ["4s", "3d", "4p", "3f"],
  ["The diagonal method gives 1s 2s 2p 3s 3p <b>4s</b> 3d 4p: 4s is lower in energy than 3d, so it fills first.",
   "3d comes after 4s; this is the most common filling-order mistake.",
   "4p comes after both 4s and 3d.",
   "There is no 3f subshell: shell 3 has only 3s, 3p and 3d."],
  "Use the diagonal method; the order is not simply shell by shell.",
  "Filling order: 1s 2s 2p 3s 3p <b>4s</b> 3d 4p 5s. That is why potassium and calcium, in row 4, put their last electrons in 4s before any 3d electrons appear.", 2)

def orb(subs):  # [('1s','ud'),('2p','ud u u')] -> fbx orbitals figure
    return [{"type": "orbitals", "subs": [{"name": n, "boxes": [x if x != '_' else '' for x in b.split()]} for n, b in subs]}]
Q(T, "The orbital diagram shows a neutral atom in its ground state. Which element is it?",
  ["Silicon", "Carbon", "Sulfur", "Neon"],
  ["Counting arrows: 2 + 2 + 6 + 2 + 2 = 14 electrons, so Z = 14, silicon.",
   "Carbon also ends with two unpaired p electrons (2p<sup>2</sup>), but it has only 6 electrons in all; this atom has filled 2p and 3s subshells as well.",
   "Sulfur (16 electrons) would have 4 electrons in 3p; this diagram has 2.",
   "Neon has 10 electrons and stops at a full 2p subshell; this atom continues into 3s and 3p."],
  "Count every arrow; a neutral atom has as many electrons as protons.",
  "Arrows: 1s (2), 2s (2), 2p (6), 3s (2), 3p (2) = 14 electrons. Z = 14 is <b>silicon</b>. The two 3p electrons are in separate orbitals with the same spin, as Hund's rule requires.", 2, 0,
  orb([('1s', 'ud'), ('2s', 'ud'), ('2p', 'ud ud ud'), ('3s', 'ud'), ('3p', 'u u _')]))

Q(T, "How many <b>unpaired electrons</b> does a ground-state oxygen atom have?",
  ["2", "0", "4", "6"],
  ["Oxygen's 2p subshell holds 4 electrons: [↑↓][↑][↑]. Three go in one per box, the fourth pairs, leaving 2 unpaired.",
   "Oxygen has an even number of electrons, but Hund's rule leaves two of its 2p electrons unpaired.",
   "4 is the number of 2p electrons; two of them are paired in the same box.",
   "6 is the number of valence electrons (2s<sup>2</sup> 2p<sup>4</sup>), not the number of unpaired ones."],
  "Draw the 2p boxes: put one arrow in each box first, then pair.",
  "O has 8 electrons: 1s [↑↓] 2s [↑↓] 2p [↑↓][↑][↑]. Count the single arrows: <b>2 unpaired electrons</b>.", 2)

Q(T, "Which diagram correctly shows the <b>valence subshells</b> (3s and 3p) of a ground-state silicon atom?",
  ["3s [↑↓] 3p [↑][↑][&nbsp;&nbsp;]", "3s [↑↓] 3p [↑↓][&nbsp;&nbsp;][&nbsp;&nbsp;]", "3s [↑↑] 3p [↑][↑][&nbsp;&nbsp;]", "3s [↑] 3p [↑][↑][↑]"],
  ["3s fills first with an opposite-spin pair; the two 3p electrons go into separate orbitals with the same spin.",
   "The two 3p electrons are paired while other 3p orbitals sit empty, which breaks Hund's rule.",
   "Two same-spin arrows in the 3s box break the Pauli exclusion principle.",
   "This puts an electron into 3p before 3s is full, which breaks the Aufbau principle (the count, 4, is right)."],
  "Silicon has 4 electrons beyond neon. Check each diagram against all three filling rules.",
  "Si is [Ne] 3s<sup>2</sup> 3p<sup>2</sup>. Fill 3s with a pair (Pauli), then put the two 3p electrons in different orbitals with the same spin (Hund): <b>3s [↑↓] 3p [↑][↑][&nbsp;&nbsp;]</b>.", 3)

Q(T, "A student drew this orbital diagram for a <b>ground-state</b> carbon atom. Which rule does it break?",
  ["The Aufbau principle", "Hund's rule", "The Pauli exclusion principle", "It breaks no rule; it is the ground state of carbon."],
  ["An electron was put into 2p while 2s still had room. Lower-energy subshells fill first, so 2s should be [↑↓].",
   "The three 2p electrons are spread one per box with the same spin, which is exactly what Hund's rule asks.",
   "No box holds two electrons with the same spin, and none holds more than two.",
   "The diagram has the right count (6), but carbon's ground state is 1s [↑↓] 2s [↑↓] 2p [↑][↑][&nbsp;&nbsp;]; moving an electron up from 2s needs energy."],
  "Check whether every lower-energy subshell is full before the next one gets electrons.",
  "The diagram shows 2s with one electron and 2p with three. In the ground state, <b>2s fills before 2p (Aufbau principle)</b>. Carbon's ground state is 1s<sup>2</sup> 2s<sup>2</sup> 2p<sup>2</sup>; the drawing is an excited state.", 3, 0,
  orb([('1s', 'ud'), ('2s', 'u'), ('2p', 'u u u')]))

# ======================= ch03-config (12) =======================
T = 'ch03-config'
Q(T, "Magnesium ions are needed by hundreds of enzymes in the body. What is the full electron configuration of a magnesium <b>atom</b>?",
  [cfg("1s2 2s2 2p6 3s2"), cfg("1s2 2s2 2p6 3s1"), cfg("1s2 2s2 2p8"), cfg("1s2 2s2 2p6 3p2")],
  ["Mg has 12 electrons: 2 + 2 + 6 fill the first two shells, and the last 2 go into 3s.",
   "The superscripts add to 11, which is sodium. Magnesium has 12 electrons.",
   "A p subshell holds at most 6 electrons, so the 2p subshell cannot hold 8.",
   "3s fills before 3p, so the last two electrons go into 3s."],
  "Find Z, then fill 1s 2s 2p 3s ... and check that the superscripts add up to Z.",
  "Mg (Z = 12): <b>" + cfg("1s2 2s2 2p6 3s2") + "</b>. Check: 2 + 2 + 6 + 2 = 12. Magnesium is in group 2, and every group 2 element ends in s<sup>2</sup>.", 1)

Q(T, "Potassium is a key electrolyte in nerve and heart cells. What is the full electron configuration of a potassium atom (Z = 19)?",
  [cfg("1s2 2s2 2p6 3s2 3p6 4s1"), cfg("1s2 2s2 2p6 3s2 3p6 3d1"), cfg("1s2 2s2 2p6 3s2 3p6"), cfg("1s2 2s2 2p6 3s2 3p6 4s2")],
  ["After 3p fills (18 electrons), the 19th goes into 4s, which is lower in energy than 3d.",
   "4s fills before 3d, so potassium's last electron goes into 4s, not 3d.",
   "These superscripts add to 18, which is argon, or the K<sup>+</sup> ion; the neutral atom has one more electron.",
   "These superscripts add to 20, which is calcium."],
  "Use the diagonal method for what comes after 3p, and check the total.",
  "K (19 electrons): <b>" + cfg("1s2 2s2 2p6 3s2 3p6 4s1") + "</b>. Check: 2 + 2 + 6 + 2 + 6 + 1 = 19. Group 1 elements all end in s<sup>1</sup>.", 2)

Q(T, "Calcium ions trigger muscle contraction. What is the noble-gas (shorthand) configuration of a calcium <b>atom</b>?",
  ["[Ar] 4s<sup>2</sup>", "[Ne] 4s<sup>2</sup>", "[Ar] 3d<sup>2</sup>", "[Ar] 4s<sup>1</sup>"],
  ["Ca is in row 4, so the noble gas from the row above is argon (18 electrons); 18 + 2 = 20.",
   "Neon (10) plus 2 is only 12 electrons; neon is two rows above calcium, so the 3s and 3p electrons would be missing.",
   "4s fills before 3d, so calcium's two electrons beyond argon go into 4s.",
   "18 + 1 = 19 is potassium; calcium is in group 2 and ends in s<sup>2</sup>."],
  "Use the noble gas at the end of the row above calcium, then continue from the start of calcium's row.",
  "Ca (Z = 20) is in row 4, group 2. Argon ends row 3, so <b>[Ar] 4s<sup>2</sup></b>. Check: 18 + 2 = 20.", 2)

Q(T, "Which element has the configuration [Ne] 3s<sup>2</sup> 3p<sup>4</sup>?",
  ["Sulfur", "Oxygen", "Selenium", "Argon"],
  ["Neon has 10 electrons; 10 + 2 + 4 = 16, and Z = 16 is sulfur (row 3, group 16).",
   "Oxygen is 1s<sup>2</sup> 2s<sup>2</sup> 2p<sup>4</sup>; it ends in p<sup>4</sup> too, but in shell 2, with only 8 electrons.",
   "Selenium ends in 4p<sup>4</sup> and has 34 electrons ([Ar] 4s<sup>2</sup> 3d<sup>10</sup> 4p<sup>4</sup>).",
   "Argon has a full 3p<sup>6</sup> subshell and 18 electrons."],
  "Add the electrons in the bracket to the superscripts.",
  "[Ne] = 10 electrons, plus 3s<sup>2</sup> 3p<sup>4</sup> = 6 more: 16 electrons, so Z = 16, <b>sulfur</b>. The 3p tells you row 3, and p<sup>4</sup> tells you the fourth column of the p block (group 16).", 2)

Q(T, "Iodide in iodized salt helps the thyroid gland make its hormones. What is the noble-gas configuration of an iodine atom (Z = 53)?",
  [cfg("[Kr] 5s2 4d10 5p5"), cfg("[Kr] 5s2 5d10 5p5"), cfg("[Kr] 5s2 5p5"), cfg("[Xe] 5s2 4d10 5p5")],
  ["Row 5 after krypton: 5s (2), the row-5 d block, which is 4d (10), then 5 columns into the p block (5p<sup>5</sup>). 36 + 17 = 53.",
   "The d block in row 5 is 4d, not 5d: the d shell number is the row number minus 1.",
   "This skips the d block. In row 5 you pass through all ten 4d columns before reaching the p block; the total here is only 43.",
   "Xenon is at the end of iodine's own row; the bracket uses the noble gas from the row above (krypton). This would total 71 electrons."],
  "Read across row 5 from the start until you reach iodine; remember how the d block is numbered.",
  "I is in row 5, group 17. After [Kr] (36 electrons), read across row 5: 5s<sup>2</sup>, 4d<sup>10</sup>, 5p<sup>5</sup>. <b>" + cfg("[Kr] 5s2 4d10 5p5") + "</b>. Check: 36 + 2 + 10 + 5 = 53, and like every halogen it ends in s<sup>2</sup> p<sup>5</sup>.", 3)

Q(T, "Arsenic, a contaminant in some Central Valley well water, is in row 4, group 15. Which subshell does arsenic's <b>last electron</b> enter?",
  ["4p", "3p", "3d", "4d"],
  ["Group 15 is in the p block, and in row 4 the p subshell is 4p (shell number = row number for s and p).",
   "3p is the p subshell of row 3 (phosphorus, the element above arsenic, ends in 3p<sup>3</sup>).",
   "3d is the row-4 d block, groups 3 to 12; arsenic has already passed through it.",
   "4d is the d block of row 5, not row 4."],
  "Which block is group 15 in, and how is the shell number of that block related to the row?",
  "Arsenic sits in the p block (groups 13 to 18) of row 4, so its last electron enters <b>4p</b>: As is [Ar] 4s<sup>2</sup> 3d<sup>10</sup> 4p<sup>3</sup>.", 2)

Q(T, "What is the electron configuration of the potassium <b>ion</b>, K<sup>+</sup>?",
  [cfg("1s2 2s2 2p6 3s2 3p6"), cfg("1s2 2s2 2p6 3s2 3p6 4s2"), cfg("1s2 2s2 2p6 3s2 3p5 4s1"), cfg("1s2 2s2 2p6 3s2 3p6 4s1")],
  ["K has 19 electrons and K<sup>+</sup> has 18: the 4s electron, in the highest shell, is the one removed. This is argon's configuration.",
   "This adds an electron (20 in all). A positive ion has <i>lost</i> electrons.",
   "Cations lose electrons from the highest-numbered shell first, which is 4s, not 3p.",
   "This is the neutral potassium atom with 19 electrons; the ion has one fewer."],
  "A 1+ charge means one electron was lost. Which shell gives it up first?",
  "K is " + cfg("1s2 2s2 2p6 3s2 3p6 4s1") + ". Removing the 4s electron gives <b>" + cfg("1s2 2s2 2p6 3s2 3p6") + "</b> (18 electrons), isoelectronic with argon.", 2)

Q(T, "What is the electron configuration of the nitride ion, N<sup>3" + M + "</sup>?",
  [cfg("1s2 2s2 2p6"), cfg("1s2 2s2"), cfg("1s2 2s2 2p3"), cfg("1s2 2s2 2p4")],
  ["N has 7 electrons; a 3" + M + " ion has gained 3, giving 10, which fills the 2p subshell (neon's configuration).",
   "This removes 3 electrons, which would make N<sup>3+</sup>. A negative charge means electrons were gained.",
   "This is the neutral nitrogen atom with 7 electrons; the ion has 3 more.",
   "This adds only 1 electron (8 in all); a 3" + M + " charge means 3 electrons were gained."],
  "A negative charge means extra electrons. Add them to the next open spots.",
  "N is 1s<sup>2</sup> 2s<sup>2</sup> 2p<sup>3</sup> (7 electrons). Adding 3 gives <b>" + cfg("1s2 2s2 2p6") + "</b>, 10 electrons, isoelectronic with neon.", 2)

Q(T, "Which electrolyte ion is <b>isoelectronic with argon</b>?",
  [ion("Ca", 2), ion("Na", 1), ion("Mg", 2), ion("F", -1)],
  ["Ca has 20 electrons; Ca<sup>2+</sup> has 20 " + M + " 2 = 18, the same as argon.",
   "Na<sup>+</sup> has 11 " + M + " 1 = 10 electrons, like neon, not argon.",
   "Mg<sup>2+</sup> has 12 " + M + " 2 = 10 electrons, like neon.",
   "F<sup>" + M + "</sup> has 9 + 1 = 10 electrons, like neon."],
  "Count the electrons in each ion: protons minus the charge. Argon has 18.",
  "Isoelectronic means same number of electrons (same configuration). Argon has 18. Ca<sup>2+</sup>: 20 " + M + " 2 = 18, so <b>Ca<sup>2+</sup></b>. Na<sup>+</sup>, Mg<sup>2+</sup> and F<sup>" + M + "</sup> each have 10, like neon.", 2)

Q(T, "A student writes " + cfg("1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p3") + " for selenium (Z = 34). What is wrong?",
  ["It has one electron too few: the superscripts add to 33, which is arsenic. Selenium ends in 4p<sup>4</sup>.",
   "The 3d subshell should come before 4s.",
   "The d block in row 4 should be written as 4d.",
   "Nothing is wrong; it is the correct configuration of selenium."],
  ["2 + 2 + 6 + 2 + 6 + 2 + 10 + 3 = 33. Selenium is in group 16, the fourth column of the p block, so it needs 4p<sup>4</sup>.",
   "4s fills before 3d in the diagonal order, so the order written is right.",
   "The row-4 d block is 3d (row number minus 1), so 3d is right.",
   "Add the superscripts and compare with Z = 34."],
  "Add the superscripts and compare with the atomic number.",
  "Total: 2 + 2 + 6 + 2 + 6 + 2 + 10 + 3 = 33, one short. <b>Selenium is " + cfg("1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p4") + "</b> (34 electrons); the student's version belongs to arsenic.", 3)

Q(T, "A neutral atom has the configuration " + cfg("1s2 2s2 2p6 3s2 3p3") + ". Which element is it?",
  ["Phosphorus", "Nitrogen", "Arsenic", "Vanadium"],
  ["2 + 2 + 6 + 2 + 3 = 15 electrons, so Z = 15, phosphorus. It ends in 3p<sup>3</sup>: row 3, group 15.",
   "Nitrogen also ends in p<sup>3</sup>, but in 2p, with only 7 electrons.",
   "Arsenic ends in 4p<sup>3</sup> and has 33 electrons.",
   "Vanadium has 23 electrons; 3 is only the last superscript, not the total."],
  "Add all the superscripts.",
  "2 + 2 + 6 + 2 + 3 = 15 electrons. A neutral atom with 15 electrons has Z = 15: <b>phosphorus</b>.", 1)

Q(T, "Which electron configuration belongs to the element marked X on the periodic table outline?",
  [cfg("[Ar] 4s2 3d10 4p3"), cfg("[Ar] 4s2 4p3"), cfg("[Ar] 4s2 4d10 4p3"), cfg("[Ne] 3s2 3p3")],
  ["X is in row 4, group 15. After [Ar], row 4 crosses 4s (2), the 3d block (10) and 3 columns of 4p: 18 + 15 = 33, arsenic.",
   "This skips the ten 3d columns that come before the p block in row 4; it totals only 23.",
   "The row-4 d block is 3d, not 4d (row number minus 1).",
   "This is phosphorus, the element in row 3 directly above X."],
  "Count the row first, then read across that row from the left edge until you reach X.",
  "X is in row 4, group 15 (arsenic, Z = 33). After [Ar], read across row 4: 4s<sup>2</sup>, 3d<sup>10</sup>, 4p<sup>3</sup>. <b>" + cfg("[Ar] 4s2 3d10 4p3") + "</b>. Check: 18 + 2 + 10 + 3 = 33.", 3, 0,
  [{"type": "ptgrid", "periods": 5, "show": PT_SHOW, "cells": {"X": [4, 15]}}])

# ======================= ch03-valence (10) =======================
T = 'ch03-valence'
Q(T, "Chloride is the main negative ion in blood. How many valence electrons does a chlorine <b>atom</b> have?",
  ["7", "17", "1", "8"],
  ["Chlorine is in group 17; for groups 13 to 18, valence electrons = group number " + M + " 10 = 7 (3s<sup>2</sup> 3p<sup>5</sup>).",
   "17 is the group number (and the atomic number). For groups 13 to 18, subtract 10.",
   "Chlorine is one electron <i>short</i> of an octet, so it gains 1; it has 7 valence electrons, not 1.",
   "8 is the octet chlorine reaches as Cl<sup>" + M + "</sup>; the atom has one fewer."],
  "For groups 13 to 18, how do you get valence electrons from the group number?",
  "Cl is in group 17: 17 " + M + " 10 = <b>7 valence electrons</b>, the 3s<sup>2</sup> 3p<sup>5</sup> electrons of its highest shell. Gaining 1 gives Cl<sup>" + M + "</sup> an octet.", 1)

Q(T, "Selenium is [Ar] 4s<sup>2</sup> 3d<sup>10</sup> 4p<sup>4</sup>. How many valence electrons does it have?",
  ["6", "16", "4", "34"],
  ["The highest shell is n = 4: 4s<sup>2</sup> 4p<sup>4</sup> = 6. The 3d electrons are in a lower shell and do not count.",
   "16 counts the 3d electrons too (2 + 10 + 4). For main-group elements only the s and p electrons of the highest shell count.",
   "4 counts only the 4p electrons; the 4s electrons are in the same (highest) shell and count too.",
   "34 is the total number of electrons (Z), not the valence electrons."],
  "Which shell has the highest number? Count only the electrons in that shell.",
  "Selenium's highest shell is n = 4, holding 4s<sup>2</sup> 4p<sup>4</sup>: <b>6 valence electrons</b>. This matches group 16: 16 " + M + " 10 = 6.", 2)

Q(T, "Aluminum is in group 13. Use the octet rule to predict the ion it forms.",
  [ion("Al", 3), ion("Al", -5), ion("Al", -3), ion("Al", 1)],
  ["Al has 3 valence electrons. Losing 3 is far easier than gaining 5, and it leaves neon's configuration: Al<sup>3+</sup>.",
   "Gaining 5 electrons would reach an octet in principle, but a metal with only 3 valence electrons loses them instead.",
   "A 3" + M + " charge would mean gaining 3 electrons, which gives 6 valence electrons, not an octet; it also has the sign backward.",
   "Losing just 1 electron would leave 2 valence electrons, not a noble-gas configuration."],
  "How many valence electrons does aluminum have, and is it easier to lose those or to gain enough to reach 8?",
  "Group 13: 13 " + M + " 10 = 3 valence electrons. Aluminum is a metal and <b>loses all 3</b>, forming <b>Al<sup>3+</sup></b> with neon's configuration (10 electrons).", 2)

Q(T, "Why does oxygen form O<sup>2" + M + "</sup> rather than O<sup>6+</sup>?",
  ["Gaining 2 electrons to reach an octet is much easier than losing all 6 valence electrons.",
   "Oxygen has 2 valence electrons, and it gains 2 more.",
   "Oxygen always loses electrons, because it is a nonmetal.",
   "O<sup>2" + M + "</sup> has the same number of protons as neon."],
  ["Oxygen has 6 valence electrons. It is 2 steps from neon's octet by gaining, but 6 steps by losing; the shorter path wins.",
   "Oxygen is in group 16 and has 6 valence electrons (2s<sup>2</sup> 2p<sup>4</sup>), not 2.",
   "Nonmetals in groups 15 to 17 tend to <i>gain</i> electrons; metals lose them.",
   "O<sup>2" + M + "</sup> has the same number of <i>electrons</i> as neon (10), but it keeps oxygen's 8 protons."],
  "Count how many steps oxygen is from the nearest noble gas, going each way.",
  "Oxygen has 6 valence electrons. Gaining 2 reaches an octet (neon's configuration) in 2 steps; losing 6 would take 6. So oxygen forms <b>O<sup>2" + M + "</sup></b>, oxide.", 2)

Q(T, "Why are the noble gases, such as neon and argon, so unreactive?",
  ["Their valence shells are already full (an octet, or 2 electrons for helium).",
   "They have no valence electrons at all.",
   "Their atoms are too large to react.",
   "They have only one valence electron, which they hold very tightly."],
  ["A full ns<sup>2</sup> np<sup>6</sup> valence shell is the stable arrangement that other atoms gain or lose electrons to reach.",
   "Neon and argon each have 8 valence electrons; the shell is full, not empty.",
   "Noble gases are among the <i>smallest</i> atoms in their rows.",
   "Noble gases have 8 valence electrons (helium has 2), not 1."],
  "Look at the valence configuration of group 18.",
  "Group 18 atoms already have a <b>full valence shell</b>: ns<sup>2</sup> np<sup>6</sup>, an octet (helium: 1s<sup>2</sup>). They have no electrons to lose easily and no room to gain more, so they barely react.", 1)

Q(T, "Four main-group elements are marked on the periodic table outline. Which one is most likely to form a <b>2" + M + "</b> ion?",
  ["C", "A", "B", "D"],
  ["C is in group 16: 6 valence electrons, so it gains 2 to reach an octet and forms a 2" + M + " ion (like O<sup>2" + M + "</sup> and S<sup>2" + M + "</sup>).",
   "A is in group 2. With 2 valence electrons, it loses them and forms a 2+ ion: the right size of charge, but the wrong sign.",
   "B is in group 17. With 7 valence electrons, it gains just 1 and forms a 1" + M + " ion.",
   "D is in group 18, a noble gas; its valence shell is already full, so it does not form ions."],
  "Find the group of each letter, then decide how many electrons each must gain or lose to reach 8.",
  "A 2" + M + " ion means gaining 2 electrons, which fits an atom with 6 valence electrons: group 16. <b>C</b> is in group 16. A (group 2) forms 2+, B (group 17) forms 1" + M + ", and D (group 18) forms no ion.", 2, 0,
  [{"type": "ptgrid", "periods": 4, "show": PT_SHOW, "cells": {"A": [4, 2], "B": [3, 17], "C": [3, 16], "D": [2, 18]}}])

Q(T, "Which pair of elements would you expect to have the most similar chemical properties?",
  ["Sodium and potassium", "Sodium and magnesium", "Potassium and calcium", "Chlorine and argon"],
  ["Na and K are both in group 1, each with one valence electron (3s<sup>1</sup> and 4s<sup>1</sup>), so both form 1+ ions and react with water the same way.",
   "Na (group 1) and Mg (group 2) are neighbors in the same row, but they have different numbers of valence electrons.",
   "K and Ca are in the same row but different groups (1 and 2), with 1 and 2 valence electrons.",
   "Cl (7 valence electrons) reacts readily; Ar (8) barely reacts at all."],
  "Chemical properties follow the number of valence electrons. Which pair shares a group?",
  "Elements in the same group have the same valence configuration. <b>Sodium and potassium</b> are both group 1 (ns<sup>1</sup>), so both lose one electron to form Na<sup>+</sup> and K<sup>+</sup>.", 1)

Q(T, "IV fluid labels give ion amounts in milliequivalents (mEq), a unit that accounts for charge. For which ion does <b>1 mmol equal 2 mEq</b>?",
  [ion("Ca", 2), ion("K", 1), ion("Na", 1), ion("Cl", -1)],
  ["Calcium (group 2) gives up its 2 valence electrons, so each ion carries a 2+ charge, and 1 mmol counts as 2 mEq.",
   "K<sup>+</sup> has a 1+ charge (group 1), so 1 mmol is 1 mEq.",
   "Na<sup>+</sup> has a 1+ charge (group 1), so 1 mmol is 1 mEq.",
   "Cl<sup>" + M + "</sup> has a charge of size 1 (group 17 gains one electron), so 1 mmol is 1 mEq."],
  "Which of these elements gives up two valence electrons when it forms its ion?",
  "Milliequivalents = millimoles &times; size of the charge. Group 2 calcium loses 2 valence electrons to form <b>Ca<sup>2+</sup></b>, so 1 mmol = 2 mEq. Na<sup>+</sup>, K<sup>+</sup> and Cl<sup>" + M + "</sup> each have a charge of size 1. (Context only; this is not dosing guidance.)", 2)

Q(T, "In an electron-dot (Lewis) symbol, how many dots are drawn around the symbol for nitrogen?",
  ["5", "7", "3", "2"],
  ["The dots show valence electrons only. Nitrogen is in group 15: 15 " + M + " 10 = 5 (2s<sup>2</sup> 2p<sup>3</sup>).",
   "7 is nitrogen's total number of electrons, including the 2 core electrons in 1s.",
   "3 is the number of electrons nitrogen gains to form N<sup>3" + M + "</sup>, or its number of unpaired electrons; the dot symbol shows all 5 valence electrons.",
   "2 is the number of core (1s) electrons; dot symbols show the valence electrons."],
  "A dot symbol shows only one kind of electron.",
  "Dot symbols show <b>valence electrons</b>. Nitrogen (group 15) has 2s<sup>2</sup> 2p<sup>3</sup>: <b>5 dots</b>.", 1)

Q(T, "Na<sup>+</sup> has the same electron configuration as a neon atom. Which statement is true?",
  ["Na<sup>+</sup> is still sodium, because it still has 11 protons.",
   "Na<sup>+</sup> has turned into a neon atom.",
   "Na<sup>+</sup> has 11 electrons.",
   "Na<sup>+</sup> has 10 protons."],
  ["The element is set by the number of protons. Na<sup>+</sup> lost an electron, not a proton, so it is still sodium, with 11 protons and 10 electrons.",
   "Neon has 10 protons. Na<sup>+</sup> keeps sodium's 11 protons, so it is isoelectronic with neon but not neon.",
   "Na<sup>+</sup> has lost one of sodium's 11 electrons, leaving 10.",
   "Forming an ion changes the number of electrons, never the number of protons."],
  "What decides which element an atom or ion is?",
  "Na<sup>+</sup> has 11 protons and 10 electrons. It is <b>isoelectronic</b> with neon (10 electrons) but <b>still sodium</b>, because the proton count did not change.", 2)

# ======================= ch03-trends (10) =======================
T = 'ch03-trends'
Q(T, "Which of these group 1 atoms has the <b>largest</b> atomic radius?",
  ["Rb", "Li", "Na", "K"],
  ["Rb is lowest in the group (row 5), so its valence electron is in the highest shell, farthest from the nucleus.",
   "Li is at the top of group 1, with its valence electron in shell 2; it is the smallest of these.",
   "Na (shell 3) is larger than Li, but there are two elements below it that are larger still.",
   "K (shell 4) is large, but Rb, below it, has one more shell."],
  "What changes each time you go one row down a group?",
  "Going down a group adds a shell, so atomic radius increases: Li &lt; Na &lt; K &lt; Rb. <b>Rb</b> is the largest.", 1)

Q(T, "Rank Al, P and Cl in order of <b>increasing</b> atomic radius.",
  ["Cl &lt; P &lt; Al", "Al &lt; P &lt; Cl", "P &lt; Cl &lt; Al", "Cl &lt; Al &lt; P"],
  ["All three are in row 3. Moving right adds protons while electrons stay in shell 3, so atoms shrink: Cl (farthest right) is smallest and Al largest.",
   "This is the order of <i>decreasing</i> radius. Across a row, atoms get smaller, not larger.",
   "Cl is to the right of P, so Cl is smaller than P.",
   "Al is the farthest left of the three, so it is the largest, not in the middle."],
  "All three are in the same row. Which way do atoms shrink across a row?",
  "Across a period, the nuclear charge grows while electrons go into the same shell, so atomic radius decreases left to right. Increasing radius: <b>Cl &lt; P &lt; Al</b>.", 2)

Q(T, "Which row-3 element has the <b>highest</b> first ionization energy: Na, Si, S or Ar?",
  ["Ar", "Na", "Si", "S"],
  ["Ionization energy increases across a period, and the noble gas at the end of each row, with its full shell, has the highest value: argon.",
   "Na, at the far left, has the <i>lowest</i> ionization energy in row 3; it loses its one valence electron easily.",
   "Si is in the middle of the row; elements farther right hold their electrons more tightly.",
   "S is close, but Ar is farther right and has a full octet."],
  "Ionization energy runs opposite to atomic radius.",
  "Across a row, ionization energy increases. The noble gas, <b>Ar</b>, has the highest in row 3; Na has the lowest.", 2)

Q(T, "Which halogen has the <b>lowest</b> first ionization energy?",
  ["I", "F", "Cl", "Br"],
  ["Iodine is lowest in the group, so its valence electrons are farthest from the nucleus and best shielded, and the easiest to remove.",
   "Fluorine, at the top, holds its electrons the most tightly: it has the <i>highest</i> ionization energy of the group.",
   "Chlorine is below fluorine but above bromine and iodine; its electrons are held more tightly than theirs.",
   "Bromine is above iodine, so its valence electrons are held a little more tightly."],
  "How does ionization energy change going down a group?",
  "Going down a group, valence electrons are in higher shells, farther out and more shielded, so ionization energy decreases: F &gt; Cl &gt; Br &gt; I. <b>Iodine</b> is lowest.", 2)

Q(T, "Which is larger, a chlorine atom (Cl) or a chloride ion (Cl<sup>" + M + "</sup>), and why?",
  ["Cl<sup>" + M + "</sup>, because it has one more electron than protons, so its electrons repel each other more and the cloud spreads out.",
   "Cl, because the ion has gained a proton.",
   "Cl, because adding an electron pulls the cloud in tighter.",
   "They are the same size, because both have 17 protons."],
  ["An anion is larger than its atom: 18 electrons around 17 protons push apart more than 17 electrons do.",
   "Ions form by gaining or losing electrons, never protons.",
   "The extra electron adds repulsion without adding any nuclear pull, so the cloud grows, not shrinks.",
   "The proton count is the same, but the number of electrons is not, and that changes the size."],
  "Is Cl<sup>" + M + "</sup> a cation or an anion? How do those compare with their atoms?",
  "Anions are larger than their atoms. <b>Cl<sup>" + M + "</sup></b> has 18 electrons and 17 protons; the extra electron increases repulsion and the electron cloud spreads out.", 2)

Q(T, "Na<sup>+</sup> and K<sup>+</sup> both carry a 1+ charge, but potassium channels in nerve cells sort them by size. Which ion is larger?",
  ["K<sup>+</sup>, because its outermost electrons are in a higher shell (shell 3) than those of Na<sup>+</sup> (shell 2).",
   "Na<sup>+</sup>, because sodium comes first in the group.",
   "They are the same size, because they have the same charge.",
   "Na<sup>+</sup>, because it has fewer protons pulling on its electrons."],
  ["K<sup>+</sup> is [Ar], with its outer electrons in shell 3; Na<sup>+</sup> is [Ne], with its outer electrons in shell 2. One more shell makes K<sup>+</sup> larger.",
   "Being higher in the group means fewer shells, which makes Na<sup>+</sup> <i>smaller</i>.",
   "Charge alone does not set size; the number of occupied shells matters most here.",
   "Fewer protons, yes, but also one fewer shell; going down a group, the added shell wins and size increases."],
  "Write the noble-gas configuration of each ion and compare the highest occupied shells.",
  "Down a group, ions get larger just as atoms do. <b>K<sup>+</sup></b> (18 electrons, outer shell 3) is larger than Na<sup>+</sup> (10 electrons, outer shell 2). Channel proteins use this size difference to pass K<sup>+</sup> selectively.", 2)

Q(T, "Which element has the most <b>metallic character</b>?",
  ["Cs", "Al", "S", "Cl"],
  ["Metallic character is greatest where ionization energy is lowest: the lower left. Cesium, in group 1, row 6, loses its valence electron most easily.",
   "Al is a metal, but it is farther right and higher than Cs, so it holds its electrons more tightly.",
   "S is a nonmetal on the upper right; it tends to gain electrons.",
   "Cl is a nonmetal and tends to gain an electron, not lose one."],
  "Metals lose electrons easily. Where on the table is ionization energy lowest?",
  "Metallic character increases toward the lower left, where atoms are large and ionization energies are low. Of these, <b>Cs</b> is farthest down and to the left.", 1)

Q(T, "Four elements are marked on the periodic table outline. Which one has the <b>largest atomic radius</b>?",
  ["B", "A", "C", "D"],
  ["B is in row 4, group 1: the farthest down and the farthest left of the four, so it is the largest.",
   "A is in row 2, group 17, at the upper right: one of the smallest atoms.",
   "C is in row 3, group 16. It is farther down than A but far to the right, so it is smaller than B.",
   "D is in row 2, group 2: on the left, but high up, with one shell fewer than C and two fewer than B."],
  "Atoms get bigger going down and to the left.",
  "Atomic radius increases down a group and decreases across a row, so the largest atom is the one farthest down and left: <b>B</b> (row 4, group 1, potassium).", 3, 0,
  [{"type": "ptgrid", "periods": 4, "show": PT_SHOW, "cells": {"A": [2, 17], "B": [4, 1], "C": [3, 16], "D": [2, 2]}}])

Q(T, "Four elements are marked on the periodic table outline. Which one has the <b>highest first ionization energy</b>?",
  ["A", "B", "C", "D"],
  ["A is in row 2, group 17: the farthest up and to the right of the four, so it holds its electrons the most tightly.",
   "B is in row 3, group 14: lower and farther left than A, so its outer electrons are easier to remove.",
   "C is in row 4, group 2: a metal on the left side that loses electrons easily.",
   "D is in row 5, group 1: farthest down and left, so it has the <i>lowest</i> ionization energy of the four."],
  "Ionization energy runs opposite to atomic radius.",
  "Ionization energy increases up a group and across a row, so it is highest toward the upper right: <b>A</b> (row 2, group 17, fluorine). D (rubidium) is lowest.", 3, 0,
  [{"type": "ptgrid", "periods": 5, "show": PT_SHOW, "cells": {"A": [2, 17], "B": [3, 14], "C": [4, 2], "D": [5, 1]}}])

Q(T, "Why do atoms get <b>smaller</b> from left to right across a period, even though each one has more electrons?",
  ["Each step adds a proton while the new electron goes into the same shell, so the stronger nuclear pull draws the valence electrons closer.",
   "Each step adds a new shell, which squeezes the electrons together.",
   "Electrons repel each other less when there are more of them.",
   "The atoms on the right lose electrons more easily."],
  ["Across a row the shell number stays the same, but the nuclear charge grows; electrons in the same shell shield each other poorly, so the effective nuclear charge rises.",
   "New shells are added going <i>down</i> a group, which makes atoms larger, not smaller.",
   "More electrons mean more repulsion, not less; the size drops because of the extra protons.",
   "Atoms on the right have <i>higher</i> ionization energies; they hold their electrons more tightly."],
  "What is added to the nucleus at each step, and which shell do the new electrons enter?",
  "Across a period, every element adds <b>one proton</b>, while its electrons stay in <b>the same shell</b>. Same-shell electrons shield each other poorly, so the effective nuclear charge increases and pulls the valence electrons in.", 3)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
import collections
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')))
