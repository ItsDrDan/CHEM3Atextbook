"""New Try It items for five thin topic sets (2026-11-17), bringing each to 10 items.

Keys: ch07-activity (+3, 7.8), ch09-energy (+3, 9.1), ch09-solids (+3, 9.7), ch14-health (+3, 14.6),
ch14-medicine (+4, 14.7). Format and rules: audit/expansion/CH1_TRYIT_BRIEF.md and CLAUDE.md conventions.
c[0] is always correct. Every number is computed below and asserted as the exact string shown.
Activity series used: the page's own list (Li, K, Ca, Na, Mg, Al, Zn, Fe, Ni, Sn, Pb, H2, Cu, Ag, Au).
Nuclear symbols: <sup>A</sup><sub>Z</sub>X; whole numbers of half-lives only.
Run: python3 -I tools/bank_thin_new.py
"""
from decimal import Decimal, ROUND_HALF_UP
from math import floor, log10
import re
import collections

CTX_MATH = "<b>Context only; a math example.</b> "
CTX = "<b>Context only.</b> "


def sf(x, n):
    """x rounded to n significant figures (half up), as a plain decimal string."""
    d = Decimal(repr(float(x)))
    e = floor(log10(abs(float(x))))
    q = Decimal(1).scaleb(e - n + 1)
    r = d.quantize(q, rounding=ROUND_HALF_UP)
    if abs(r) >= Decimal(10) ** (e + 1):
        q = Decimal(1).scaleb(e - n + 2)
        r = d.quantize(q, rounding=ROUND_HALF_UP)
    s = format(r, "f")
    return s


def eq(a, b):
    assert a == b, (a, b)


# ---- tiny formula parser to check that the chemical equations shown are balanced
def atoms(formula):
    formula = re.sub(r"<sub>(\d+)</sub>", r"\1", formula)
    tokens = re.findall(r"([A-Z][a-z]?|\(|\)|\d+)", formula)
    stack = [collections.Counter()]
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "(":
            stack.append(collections.Counter())
        elif t == ")":
            grp = stack.pop()
            m = 1
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                m = int(tokens[i + 1]); i += 1
            for k, v in grp.items():
                stack[-1][k] += v * m
        elif t.isdigit():
            pass
        else:
            m = 1
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                m = int(tokens[i + 1]); i += 1
            stack[-1][t] += m
        i += 1
    return stack[0]


def side(s):
    tot = collections.Counter()
    for term in s.split(" + "):
        term = re.sub(r"\((s|l|g|aq)\)", "", term).strip()
        m = re.match(r"(\d+) (.*)", term)
        coef, f = (int(m.group(1)), m.group(2)) if m else (1, term)
        for k, v in atoms(f).items():
            tot[k] += coef * v
    return tot


def balanced(eqn):
    left, right = eqn.split(" &rarr; ")
    return side(left) == side(right)


# ---- nuclear equation check: sums of A and Z
def nuc(sym):
    m = re.match(r"<sup>(\d+)</sup><sub>(&minus;|\+)?(\d+)</sub>", sym)
    z = int(m.group(3))
    if m.group(2) == "&minus;":
        z = -z
    return int(m.group(1)), z


SERIES = ("Li, K, Ca, Na, Mg, Al, Zn, Fe, Ni, Sn, Pb, H<sub>2</sub>, Cu, Ag, Au")
ORDER = ["Li", "K", "Ca", "Na", "Mg", "Al", "Zn", "Fe", "Ni", "Sn", "Pb", "H", "Cu", "Ag", "Au"]
ASQ = "Activity series (most active first): " + SERIES + ". "


def above(a, b):
    return ORDER.index(a) < ORDER.index(b)


ITEMS = []

# ---------------------------------------------------------------- ch07-activity (7.8)

# A1 sacrificial anode
assert above("Mg", "Fe") and not above("Sn", "Fe") and not above("Cu", "Fe") and not above("Ni", "Fe")
ITEMS.append(dict(
    t="ch07-activity",
    q="Steel (iron) boat hulls on the Sacramento&ndash;San Joaquin Delta carry blocks of another metal bolted on as a sacrificial anode, which corrodes in place of the iron. " + ASQ + "Which metal would work?",
    c=["Mg", "Sn", "Ni", "Cu"],
    y=["Magnesium is above iron, so it gives up electrons more easily and is oxidized instead of the iron.",
       "Tin is below iron. It would not be oxidized first, so the iron would still rust.",
       "Nickel is just below iron, so it cannot protect it; the protecting metal must be <i>above</i> iron.",
       "Copper is far below iron (and below H<sub>2</sub>). This reads the list upside down."],
    h="The protecting metal must be oxidized more easily than iron. Where must it sit on the list?",
    w="A sacrificial metal must be above Fe on the list (Zn, Al, Mg, &hellip;). Of the choices, only <b>Mg</b> is above iron.",
    d=1, k=0))

# A2 reverse reaction does not occur
fwd = "Mg + SnCl<sub>2</sub> &rarr; MgCl<sub>2</sub> + Sn"
rev = "Sn + MgCl<sub>2</sub> &rarr; SnCl<sub>2</sub> + Mg"
assert balanced(fwd) and balanced(rev)
assert above("Mg", "Sn")
ITEMS.append(dict(
    t="ch07-activity",
    q="In lab, a magnesium ribbon placed in tin(II) chloride solution becomes coated with tin. " + ASQ
      + "A student then places a tin strip in magnesium chloride solution. What happens?",
    c=["No reaction: tin is below magnesium, so the reverse reaction does not happen on its own.",
       "Sn(s) + MgCl<sub>2</sub>(aq) &rarr; SnCl<sub>2</sub>(aq) + Mg(s), the reverse of the first reaction",
       "Magnesium metal plates out, because the metal higher on the list is the one that gets reduced.",
       "It depends on the anion: tin replaces magnesium in MgCl<sub>2</sub> but not in Mg(NO<sub>3</sub>)<sub>2</sub>."],
    y=["The free metal (Sn) is below the metal in the compound (Mg), so nothing happens. A reaction that runs one way on its own does not run in reverse on its own.",
       "This assumes the reverse also happens. Mg + Sn<sup>2+</sup> runs on its own, like water running downhill, so Sn + Mg<sup>2+</sup> does not.",
       "This has the roles backward: the metal higher on the list is <i>oxidized</i>, and the ion of the lower metal is reduced. Here the ion is Mg<sup>2+</sup>, the higher metal, so no reaction.",
       "Compare the free metal with the metal in the compound, not with the anion. Chloride or nitrate, tin is still below magnesium."],
    h="Is the lone metal (Sn) higher than the metal in the compound (Mg)?",
    w="Mg + Sn<sup>2+</sup> happens, so the reverse does not. Tin is below magnesium: <b>no reaction</b>.",
    d=2, k=0))

# A3 which strips bubble in HCl
tested = ["Zn", "Ni", "Cu", "Ag"]
react = [m for m in tested if above(m, "H")]
eq(react, ["Zn", "Ni"])
ITEMS.append(dict(
    t="ch07-activity",
    q="A lab technician drops strips of zinc, nickel, copper, and silver into separate test tubes of dilute hydrochloric acid. " + ASQ
      + "Which strips give off bubbles of H<sub>2</sub> gas?",
    c=["Zinc and nickel only", "Zinc only", "All four strips", "Copper and silver only"],
    y=["Zn and Ni are above H<sub>2</sub>, so they react with the acid: for example, Ni(s) + 2 HCl(aq) &rarr; NiCl<sub>2</sub>(aq) + H<sub>2</sub>(g). Cu and Ag are below H<sub>2</sub>.",
       "Nickel is also above H<sub>2</sub>. Only the metals at the very top (Li, K, Ca, Na) are special: they react even with water.",
       "Not every metal reacts with acids. Copper and silver are below H<sub>2</sub>, one reason they are used in coins and jewelry.",
       "This reads the list upside down. Metals <i>above</i> hydrogen react with acids."],
    h="Find H<sub>2</sub> on the list. Which of the four metals are above it?",
    w="Above H<sub>2</sub>: Zn, Ni. Below: Cu, Ag. <b>Zinc and nickel only</b> release H<sub>2</sub>.",
    d=2, k=0))

# ---------------------------------------------------------------- ch09-energy (9.1)

# E1 which change loses potential energy
ITEMS.append(dict(
    t="ch09-energy",
    q="On a hot Fresno afternoon, which change involves particles <b>losing potential energy</b>?",
    c=["Water vapor condensing into droplets on the outside of a glass of iced tea",
       "Hot tea cooling from 80 &deg;C to 60 &deg;C on the counter",
       "Ice cubes melting in the iced tea",
       "Iced tea warming from 5 &deg;C to 20 &deg;C in the sun"],
    y=["Condensing pulls the water molecules closer together, so their potential energy goes down (and that energy is given off as heat).",
       "A temperature change is a kinetic energy change: the molecules slow down. Cooling liquid tea does not pull the molecules together into a new state.",
       "Melting pulls the molecules farther apart, so their potential energy goes <i>up</i>.",
       "A rising temperature means the molecules gain kinetic energy (move faster), not that they lose potential energy."],
    h="Temperature change: think kinetic energy. Change of state: think potential energy. Which state change brings particles closer?",
    w="Losing potential energy means the particles move closer together: freezing or condensing. <b>Water vapor condensing on the cold glass</b> is the only one.",
    d=2, k=0))

# E2 heat versus temperature
ITEMS.append(dict(
    t="ch09-energy",
    q="A nurse places a cold metal stethoscope on a patient's warm chest. Which statement uses the words <b>heat</b> and <b>temperature</b> correctly?",
    c=["Heat flows from the patient's warmer skin into the colder metal, so the metal's temperature rises.",
       "Cold flows from the metal into the patient's skin, so the skin's temperature falls.",
       "Temperature flows from the patient's skin into the metal until both have the same heat.",
       "The metal has a heat of 20 &deg;C, lower than the skin's heat."],
    y=["Heat is energy that flows from a hotter object to a colder one; the metal's particles speed up, so its temperature rises.",
       "There is no such thing as &ldquo;cold&rdquo; flowing. Energy (heat) flows out of the skin, which is why it feels cold.",
       "This swaps the words. Heat is what flows; temperature measures the average kinetic energy of the particles.",
       "20 &deg;C is a temperature, not heat. Heat is energy in transit, measured in joules."],
    h="Heat is energy that flows. Which way does it flow, and what does temperature measure?",
    w="Heat flows from hot to cold: <b>from the warmer skin into the colder metal, raising the metal's temperature</b>.",
    d=1, k=0))

# E3 why cold particles stick (spring / energy-well model)
ITEMS.append(dict(
    t="ch09-energy",
    q="Helium must be cooled to about &minus;269 &deg;C before it becomes a liquid, but water is a liquid at room temperature. Using the spring (energy well) model, which explanation is best?",
    c=["Helium's dispersion forces make a very shallow well, so even slow helium atoms have enough kinetic energy to pull apart; water's hydrogen bonds make a much deeper well.",
       "Particles become a liquid once they are slow enough, whatever their attractions; helium simply has to be slowed down more.",
       "Helium atoms have their highest potential energy when they are close together, so they push each other apart.",
       "Helium's attractions are the strongest, so it takes the most cooling to make the atoms stick."],
    y=["Particles stick when their attraction beats their kinetic energy. A shallow well (weak dispersion forces) is escaped easily, so helium stays a gas until its atoms are extremely slow.",
       "Cold particles do not only slow down; they stick because of their attraction. Without enough attraction, slowing down alone does not make a liquid.",
       "This gets the spring backward: attracted particles have <i>low</i> potential energy close together and high potential energy pulled apart.",
       "This reverses the strength. Weak attractions need very low temperatures to win over kinetic energy; strong ones (water's hydrogen bonds) win even at room temperature."],
    h="Compare how deep each well is with how much kinetic energy the particles have.",
    w="Attraction (potential energy well) versus kinetic energy: <b>helium's well is very shallow (dispersion only), so only extremely slow atoms stick; water's hydrogen bonds make a deep well</b>.",
    d=2, k=0))

# ---------------------------------------------------------------- ch09-solids (9.7)

# S1 amorphous vs crystalline
ITEMS.append(dict(
    t="ch09-solids",
    q="Window glass is made mostly of SiO<sub>2</sub>, the same formula as quartz. When a glassblower heats it, the glass softens gradually over a range of temperatures instead of melting at one temperature. What kind of solid is glass?",
    c=["Amorphous: its particles have no long-range order",
       "Crystalline covalent network, the same as quartz",
       "Crystalline molecular solid made of SiO<sub>2</sub> molecules",
       "Crystalline metallic solid, since it can be bent and shaped when hot"],
    y=["Softening over a range, rather than melting sharply, is the sign of an amorphous solid; glass, rubber, and most plastics are amorphous.",
       "Same formula does not mean the same arrangement. Quartz has a regular repeating lattice; glass does not.",
       "SiO<sub>2</sub> does not form small molecules the way CO<sub>2</sub> does, and glass has no regular lattice at all.",
       "Being shaped when hot is softening, not metallic malleability. Glass is not shiny metal and does not conduct electricity."],
    h="Crystalline solids melt sharply at one temperature. What does softening over a range tell you?",
    w="No regular, repeating lattice and gradual softening: glass is an <b>amorphous solid</b>.",
    d=1, k=0))

# S2 property table
ITEMS.append(dict(
    t="ch09-solids",
    q="A liquid has a very low surface tension and a high vapor pressure. What do these tell you about its intermolecular forces, and which other properties fit?",
    c=["Weak forces: a low boiling point and a low viscosity",
       "Weak forces: a high boiling point and a high viscosity",
       "Strong forces: a high boiling point and a low viscosity",
       "Strong forces: a low boiling point and a low viscosity"],
    y=["Low surface tension and high vapor pressure both mean weak forces, and weak forces also give a low boiling point and low viscosity.",
       "The forces are weak, but weak forces give <i>low</i> boiling points and viscosities, not high ones.",
       "This reads the vapor pressure row backward. Strong forces hold molecules in the liquid and give a <i>low</i> vapor pressure.",
       "Low surface tension cannot come from strong forces; stronger forces mean higher surface tension. Every row of the table points to weak forces."],
    h="Vapor pressure is the one row that runs the other way. Strong forces give a low vapor pressure.",
    w="Low surface tension and high vapor pressure &rarr; weak intermolecular forces &rarr; <b>low boiling point and low viscosity</b>.",
    d=2, k=0))

# S3 lowest melting solid
ITEMS.append(dict(
    t="ch09-solids",
    q="Which solid melts at the lowest temperature: solid argon, Ar(s); calcium fluoride, CaF<sub>2</sub>(s); quartz, SiO<sub>2</sub>(s); or iron, Fe(s)?",
    c=["Ar(s)", "CaF<sub>2</sub>(s)", "SiO<sub>2</sub>(s)", "Fe(s)"],
    y=["Solid argon is an atomic nonbonding solid: single noble-gas atoms held only by weak dispersion forces, so it melts far below room temperature (&minus;189 &deg;C).",
       "CaF<sub>2</sub> is a metal plus a nonmetal, an ionic solid. Ionic bonds are strong, so it melts high.",
       "Quartz is a covalent network solid; covalent bonds run throughout, so it melts very high (about 1700 &deg;C). Not every solid made of atoms melts low.",
       "Iron is metallic. Metals have a wide range of melting points, but iron melts at 1538 &deg;C; mercury is the low one."],
    h="Name the type of each solid first. Which type is held together only by dispersion forces?",
    w="Ar(s) is atomic nonbonding (dispersion forces only); the others are ionic, covalent network, and metallic. <b>Ar(s)</b> melts lowest.",
    d=2, k=0))

# ---------------------------------------------------------------- ch14-health (14.6)

# H1 distance then time (numbers chosen to differ from Problem 14.45)
r1, d1, d2, tmin = 18, 1.0, 3.0, 20
rate2 = r1 * (d1 / d2) ** 2
th = tmin / 60
dose = rate2 * th
eq(sf(rate2, 2), "2.0")
eq(sf(dose, 2), "0.67")
eq(sf(r1 * (d1 / d2) * th, 2), "2.0")      # divided by 3 instead of 3 squared
eq(sf(rate2 * tmin, 2), "40")              # used 20 as hours
eq(sf(r1 * th, 2), "6.0")                   # time but no distance
ITEMS.append(dict(
    t="ch14-health",
    q=CTX_MATH + "A patient who just received a technetium-99m dose for a bone scan gives a dose rate of 18 &mu;Sv/h at 1.0 m. A technologist works 3.0 m from the patient for 20. minutes. What dose does the technologist receive?",
    c=["0.67 &mu;Sv", "2.0 &mu;Sv", "40. &mu;Sv", "6.0 &mu;Sv"],
    y=["Three times the distance gives one-ninth the rate: 18 &times; 1/9 = 2.0 &mu;Sv/h. Then 2.0 &mu;Sv/h &times; (20. min &times; 1 h/60 min) = 0.67 &mu;Sv.",
       "This divides the rate by 3 for three times the distance (6.0 &mu;Sv/h). The dose rate falls with the <i>square</i> of the distance: one-ninth.",
       "This multiplies 2.0 &mu;Sv/h by 20. as if it were hours. Convert 20. min to hours first (0.333 h).",
       "This is 18 &times; 0.333 h: it uses the time but leaves out the distance. At 3.0 m the rate is only 2.0 &mu;Sv/h."],
    h="Find the dose rate at 3.0 m first (inverse-square law), then multiply by the time in hours.",
    w="Rate at 3.0 m = 18 &times; (1.0/3.0)<sup>2</sup> = 2.0 &mu;Sv/h. Dose = 2.0 &mu;Sv/h &times; (20./60) h = 0.667 &rarr; <b>0.67 &mu;Sv</b>.",
    d=3, k=1))

# H2 shielding for a beta emitter
ITEMS.append(dict(
    t="ch14-health",
    q="A biology research lab uses phosphorus-32, a pure beta emitter, to label DNA. Which shield is the best match for a vial of it?",
    c=["A thick plastic (acrylic) shield",
       "A sheet of paper, which stops beta particles",
       "No shield, because beta particles cannot travel through air",
       "A lead shield, because only lead can stop beta particles"],
    y=["Beta particles pass through paper but are stopped by plastic or aluminum, so a plastic shield is matched to a beta emitter.",
       "Paper (or skin) stops alpha particles. Beta particles go through paper.",
       "Beta particles travel easily through air, far enough to reach a worker standing near the bench.",
       "Lead is the match for gamma rays. Plastic or aluminum is enough to stop beta particles."],
    h="Match the shield to the radiation: paper for alpha, plastic or aluminum for beta, lead for gamma.",
    w="A pure beta emitter is shielded with <b>plastic (or aluminum)</b>.",
    d=1, k=0))

# H3 chest X-ray versus background
bg, cxr = 3, 0.1
eq(sf(bg / cxr, 1), "30")
eq(sf(cxr / bg, 1), "0.03")
eq(sf(bg / 0.01, 1), "300")
ITEMS.append(dict(
    t="ch14-health",
    q=CTX_MATH + "A chest X-ray gives a dose of about 0.1 mSv. Natural background radiation gives about 3 mSv per year. About how many chest X-rays give the same dose as one year of background radiation?",
    c=["About 30", "About 0.03", "About 300", "About 3"],
    y=["3 mSv &divide; 0.1 mSv per X-ray = 30 X-rays. One chest X-ray is roughly ten days of background.",
       "This divides 0.1 by 3, the fraction of a year's background that one X-ray gives, not the number of X-rays.",
       "This divides by 0.01 instead of 0.1, a decimal slip.",
       "This uses 3 mSv as the answer without dividing by the dose of one X-ray."],
    h="Divide the yearly background dose by the dose of one X-ray.",
    w="3 mSv &divide; 0.1 mSv = <b>about 30 chest X-rays</b>, which is why a single chest X-ray has no detectable effect.",
    d=1, k=0))

# ---------------------------------------------------------------- ch14-medicine (14.7)

# M1 carbon-11: decay equation plus half-life
parent = "<sup>11</sup><sub>6</sub>C"
dau = "<sup>11</sup><sub>5</sub>B"
pos = "<sup>0</sup><sub>+1</sub>e"
wrong_dau = "<sup>11</sup><sub>7</sub>N"
A0, Z0 = nuc(parent)
(A1, Z1), (A2, Z2) = nuc(dau), nuc(pos)
assert A0 == A1 + A2 and Z0 == Z1 + Z2
assert nuc(wrong_dau) == (11, 7)
t_half, t = 20.4, 61.2
n = t / t_half
assert abs(n - round(n)) < 1e-9
n = round(n)
eq(n, 3)
a0 = 555
eq(sf(a0 * 0.5 ** n, 3), "69.4")
eq(sf(a0 / n, 3), "185")
eq(sf(a0 * 0.5 ** 2, 3), "139")
ITEMS.append(dict(
    t="ch14-medicine",
    q=CTX_MATH + "Carbon-11, used in some PET scans, decays by positron emission with a half-life of 20.4 min. A dose with an activity of 555 MBq is prepared. Which choice gives the daughter nucleus and the activity left 61.2 min later?",
    c=[dau + "; 69.4 MBq", wrong_dau + "; 69.4 MBq", dau + "; 185 MBq", dau + "; 139 MBq"],
    y=["Positron emission keeps A = 11 and lowers Z by 1 (6 &rarr; 5, boron). 61.2 &divide; 20.4 = 3 half-lives: 555 &times; (1/2)<sup>3</sup> = 69.4 MBq.",
       "Z goes <i>down</i> by 1 in positron emission (a proton becomes a neutron). Raising Z to 7 is what beta decay does.",
       "This divides 555 by 3, the number of half-lives. Halve three times instead: divide by 2<sup>3</sup> = 8.",
       "This halves only twice. 61.2 min is 3 half-lives, not 2."],
    h="Positron emission: the daughter has the same A and Z one lower. Then count half-lives: time &divide; half-life.",
    w=parent + " &rarr; " + dau + " + " + pos + ". n = 61.2 &divide; 20.4 = 3; 555 MBq &times; (1/2)<sup>3</sup> = 69.375 &rarr; <b>boron-11; 69.4 MBq</b>.",
    d=3, k=1))

# M2 barium sulfate contrast is not radioactive
ITEMS.append(dict(
    t="ch14-medicine",
    q=CTX + "A patient scheduled for a barium swallow asks whether the barium sulfate, BaSO<sub>4</sub>, will make them radioactive. Which statement is correct chemistry?",
    c=["No. BaSO<sub>4</sub> is not radioactive; its heavy barium atoms simply absorb X-rays, and it is insoluble, so it passes through the gut.",
       "Yes. Barium is a gamma emitter, and the camera detects the gamma rays it gives off.",
       "Yes, slightly. The X-rays change the barium nuclei and make them radioactive for a few days.",
       "No. BaSO<sub>4</sub> dissolves quickly in the stomach, so it leaves the body before it can become radioactive."],
    y=["Contrast agents are not radioactive. Barium blocks X-rays, and because BaSO<sub>4</sub> is insoluble (a green-sheet exception), toxic Ba<sup>2+</sup> ions are not released.",
       "This confuses a contrast agent with a nuclear medicine tracer. The X-rays come from a tube outside the patient; the barium only blocks them.",
       "X-rays pass through and deposit energy; they do not change nuclei, just as gamma-sterilized supplies do not become radioactive.",
       "BaSO<sub>4</sub> is insoluble; that is why it is safe. If it dissolved, it would release toxic Ba<sup>2+</sup> ions."],
    h="Is a contrast agent a source of radiation, or does it only block X-rays from the tube?",
    w="<b>No: BaSO<sub>4</sub> is not radioactive.</b> Its heavy atoms absorb X-rays, and its insolubility keeps toxic Ba<sup>2+</sup> out of the body.",
    d=1, k=0))

# M3 holding Tc-99m waste for 10 half-lives
th99, nh = 6.0, 10
eq(sf(th99 * nh, 2), "60")          # written "60." (2 sig figs, trailing decimal point)
eq(sf(th99 / nh, 2), "0.60")
eq(2 ** nh, 1024)
eq(sf(100 / 2 ** nh, 1), "0.1")
eq(sf(100 * 0.5 / nh, 1), "5")
ITEMS.append(dict(
    t="ch14-medicine",
    q=CTX_MATH + "Used syringes from technetium-99m doses (half-life 6.0 h) are held in shielded storage for 10 half-lives before disposal. How long is that, and about what fraction of the activity is left?",
    c=["60. h, leaving about 0.1% (1/1024) of the activity",
       "60. h, leaving none of the activity",
       "60. h, leaving 5% (1/20) of the activity",
       "0.60 h, leaving about 0.1% (1/1024) of the activity"],
    y=["10 &times; 6.0 h = 60. h, and (1/2)<sup>10</sup> = 1/1024, about 0.1%. That is small enough to treat as essentially gone.",
       "Activity never reaches exactly zero; each half-life removes half of what is left. After 10 half-lives, 1/1024 remains.",
       "This multiplies 1/2 by 10 (1/20). The fraction is (1/2) multiplied by itself 10 times: 1/2<sup>10</sup>.",
       "This divides the half-life by 10 instead of multiplying: 10 half-lives of 6.0 h each is 60. h."],
    h="Time = number of half-lives &times; half-life. Fraction left = (1/2)<sup>n</sup>.",
    w="10 &times; 6.0 h = 60. h; (1/2)<sup>10</sup> = 1/1024 &asymp; 0.1%: <b>60. h, about 0.1% left</b>.",
    d=2, k=1))

# M4 choosing an imaging tracer
ITEMS.append(dict(
    t="ch14-medicine",
    q=CTX + "A nuclear medicine department needs to image a patient's thyroid. Which isotope is the best choice?",
    c=["Iodine-123: gives off gamma rays; half-life about 13 h",
       "Iodine-131: gives off beta particles and gamma rays; half-life 8.0 days",
       "Phosphorus-32: gives off only beta particles; half-life 14.3 days",
       "Radium-223: gives off alpha particles; half-life 11.4 days"],
    y=["Iodine goes to the thyroid, gamma rays leave the body to reach the camera, and a half-life of hours means the activity is gone soon after the scan.",
       "Iodine-131 does reach the thyroid, but its beta particles stay in the body and add dose without helping the image, and its 8.0-day half-life keeps it active much longer. It is used to <i>treat</i> the thyroid.",
       "Beta particles are stopped inside the body and make no image, the half-life is long, and phosphorus does not collect in the thyroid.",
       "Alpha particles are stopped within the body and cannot reach a camera, and radium does not go to the thyroid."],
    h="Ask three questions: what does it emit, how long does it last, and where does its chemistry take it?",
    w="Imaging needs gamma rays, a short half-life, and the right chemistry: <b>iodine-123</b>.",
    d=2, k=0))


# ---------------------------------------------------------------- format checks
if __name__ == "__main__":
    keys = {"ch07-activity": 3, "ch09-energy": 3, "ch09-solids": 3, "ch14-health": 3, "ch14-medicine": 4}
    cnt = collections.Counter(q["t"] for q in ITEMS)
    assert dict(cnt) == keys, cnt
    allowed = {"b", "i", "sub", "sup", "br"}
    for n_, q in enumerate(ITEMS):
        tag = "%s #%d" % (q["t"], n_)
        assert set(q) <= {"t", "q", "c", "y", "h", "w", "d", "k", "f"}, tag
        assert len(q["c"]) == 4 and len(q["y"]) == 4, tag
        assert len(set(re.sub(r"\s+", " ", c).strip().lower() for c in q["c"])) == 4, tag
        assert q["d"] in (1, 2, 3) and q["k"] in (0, 1), tag
        assert all(str(q[k]).strip() for k in ("q", "h", "w")), tag
        assert "<b>" in q["w"], tag
        s = " ".join([q["q"], q["h"], q["w"]] + q["c"] + q["y"])
        assert not re.search(r"all of the above|none of the above", s, re.I), tag
        for tg in re.findall(r"</?([a-z]+)\s*/?>", s):
            assert tg in allowed, (tag, tg)
        for tg in ("b", "i", "sub", "sup"):
            assert s.count("<%s>" % tg) == s.count("</%s>" % tg), (tag, tg)
        assert not re.search(r"&(?!(?:[a-zA-Z]+|#\d+);)", s), tag
        assert "°" not in s and "μ" not in s and "−" not in s, (tag, "use entities")
    print("items:", len(ITEMS), dict(cnt))
    print("all asserts passed")
