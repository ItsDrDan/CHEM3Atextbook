#!/usr/bin/env python3
"""Builds bank/ch10.json (Chapter 10 Try It items: kinetic molecular theory, pressure and its units, the gas laws,
the ideal gas law, gas stoichiometry, Dalton's law). Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch10.py bank/ch10.json
Conventions (Chapter 10 text): T(K) = C + 273.15 (exact; the addition rule keeps the measurement's decimal places;
values are chosen so that the rounded kelvin value and the unrounded one give the same answer). 1 atm = 760 mmHg =
760 torr = 101,325 Pa = 101.325 kPa (exact) = 14.7 psi (3 s.f.). R = 0.082058 L.atm/(mol.K) or 62.36 L.torr/(mol.K).
STP = 273 K and 1 atm; 22.4 L/mol only at STP. Gas over water: P_gas = P_atm - P_H2O (17.5 mmHg at 20.0 C, 23.8 at
25.0 C, 31.8 at 30.0 C, 47.1 at 37.0 C), given in the stem or table. Molar masses from tools/yellow_sheet_masses.json
(addition rule). Sig figs from the givens; no trailing-zero givens without a decimal point in calculation stems.
Markup: {CH4} formula, [[2 H2(g) + O2(g) -> 2 H2O(l)]] equation.
The helpers are imported by tools/gen_adapt_ch10.py. Every number is recomputed independently by
tools/check_bank_ch10.py."""
import json, sys, re, os, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
HERE = os.path.dirname(os.path.abspath(__file__))
MS = json.load(open(os.path.join(HERE, 'yellow_sheet_masses.json')))['masses']
M = '&minus;'
B = []
CFG = {'prefix': 'c10-%03d', 'adapt': False}

# ---------------- formulas and equations ----------------
def F(s):
    out = re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', s)
    return out
SPH = re.compile(r'^(.*?)(\((?:s|l|g|aq)\))?$')
def EQ(s):
    out = []
    for tok in s.split():
        if tok == '->': out.append('&rarr;')
        elif tok == '+' or re.fullmatch(r'\d+', tok): out.append(tok)
        else:
            m = SPH.match(tok); out.append(F(m.group(1)) + (m.group(2) or ''))
    return ' '.join(out)
def X(s):
    s = re.sub(r'\[\[(.+?)\]\]', lambda m: EQ(m.group(1)), s)
    s = re.sub(r'(?<![\w;])-(?=\d)', M, s)
    return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)
def parse(f):
    stack = [collections.Counter()]; i = 0
    while i < len(f):
        if f[i] == '(':
            stack.append(collections.Counter()); i += 1
        elif f[i] == ')':
            j = i + 1
            while j < len(f) and f[j].isdigit(): j += 1
            n = int(f[i + 1:j] or 1); g = stack.pop()
            for k, v in g.items(): stack[-1][k] += v * n
            i = j
        else:
            m = re.match(r'([A-Z][a-z]?)(\d*)', f[i:]); stack[-1][m.group(1)] += int(m.group(2) or 1); i += m.end()
    return stack[0]
def dp(s): return len(s.split('.')[1]) if '.' in s else 0
def mm(f):
    q = min(dp(MS[e]) for e in parse(f))
    return sum(D(MS[e]) * n for e, n in parse(f).items()).quantize(D(1).scaleb(-q), rounding=ROUND_HALF_UP)

# ---------------- numbers ----------------
def num(x, n=3):
    x = D(x); e = x.adjusted()
    m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if abs(m) >= 10:
        e += 1; m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if -3 <= e <= n - 1:
        s = format(m.scaleb(e).quantize(D(1).scaleb(min(0, e - n + 1))), 'f')
        if e == n - 1 and s.endswith('0'): s += '.'
    else:
        s = '%s &times; 10<sup>%s</sup>' % (m, (M + str(-e)) if e < 0 else str(e))
    return s
def sfs(s):
    s = s.lstrip('-')
    if '.' in s: return len(s.replace('.', '').lstrip('0'))
    return len(s.lstrip('0').rstrip('0'))
def qd(x, d): return format(D(x).quantize(D(1).scaleb(-d), rounding=ROUND_HALF_UP), 'f')
def S(v, n, u): return num(v, n) + ' ' + u
def addp(*s):
    """sum of strings (use '-x' to subtract), decimal-place rule; returns string."""
    return qd(sum(D(x) for x in s), min(dp(x) for x in s))
def ns(*a):
    """fewest significant figures among strings (as written) and ints."""
    return min(x if isinstance(x, int) else sfs(x) for x in a)
K0 = D('273.15')
def TK(c): return D(c) + K0                     # exact kelvins (carried)
def TKs(c): return qd(D(c) + K0, dp(c))         # kelvins as written (addition rule)
def sfT(c): return sfs(TKs(c))
def kt(c, lab='T'): return '%s = %s + 273.15 = %s K' % (lab, c, TKs(c))
R, R2, VM = D('0.082058'), D('62.36'), D('22.4')
ATM_MM, KPA, PSI = D(760), D('101.325'), D('14.7')
VP = {'20.0': '17.5', '25.0': '23.8', '30.0': '31.8', '37.0': '47.1'}

def Q(t_, q, c, y, h, w, d, k=0, f=None):
    y = list(y)
    if CFG['adapt'] and not y[0].startswith('Correct: '): y[0] = 'Correct: ' + y[0]
    it = {"id": CFG['prefix'] % (len(B) + 1), "t": t_, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    if f:
        for fg in f:
            if fg['type'] == 'table':
                fg['head'] = [X(x) for x in fg['head']]; fg['rows'] = [[X(x) for x in r] for r in fg['rows']]
                if fg.get('cap'): fg['cap'] = X(fg['cap'])
        it["f"] = f
    B.append(it)

def dump(out):
    json.dump(B, open(out, 'w'), ensure_ascii=False, indent=1)
    print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')),
          'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))


def build():
    # ======================= ch10-kmt (9) =======================
    T = 'ch10-kmt'
    Q(T, "Which property of gases shows most directly that a gas is mostly empty space?",
      ["A gas can be compressed into a much smaller volume.", "A gas has a definite shape.",
       "A gas is denser than the liquid it comes from.", "Gas particles attract each other strongly."],
      ["Gas particles are far apart compared with their size, so pushing them closer together shrinks the volume a great deal.",
       "Gases have no definite shape; they take the shape of their container.",
       "Gases are about a thousand times less dense than liquids, because their particles are so far apart.",
       "In kinetic molecular theory, gas particles neither attract nor repel each other."],
      "What can you do to a tank of oxygen that you cannot do to a bottle of water?",
      "Compressibility shows the empty space: <b>a gas can be squeezed into a much smaller volume</b>.", 1)

    Q(T, "According to kinetic molecular theory, what causes the pressure a gas exerts on its container?",
      ["Gas particles colliding with the container walls", "Gas particles attracting the walls of the container",
       "The weight of the gas particles resting on the bottom of the container", "Gas particles growing larger as they are heated"],
      ["Each collision pushes on the wall; the countless pushes per second, spread over the wall's area, are the pressure.",
       "KMT treats gas particles as neither attracting nor repelling anything; pressure comes from collisions.",
       "Gas particles do not settle; they move constantly and hit every wall, including the top.",
       "Particles do not change size when heated; they move faster."],
      "Think of the particles as tiny moving balls.",
      "Pressure comes from <b>particles colliding with the walls</b>: more or harder hits, higher pressure.", 1)

    Q(T, "A cylinder of carbon dioxide ({CO2}, 44.009 g/mol) and a cylinder of nitrogen ({N2}, 28.014 g/mol) stand side by side in a hospital supply room at 22 °C. How do the average kinetic energies of their molecules compare?",
      ["They are the same, because both gases are at the same temperature.",
       "The {CO2} molecules have more, because they are heavier.",
       "The {N2} molecules have more, because they move faster.",
       "It cannot be compared without knowing the pressure in each cylinder."],
      ["Average kinetic energy depends only on the Kelvin temperature. The lighter {N2} molecules move faster, and the heavier {CO2} molecules move slower, with the same average kinetic energy.",
       "Heavier molecules at the same temperature move more slowly; their average kinetic energy is the same as that of lighter ones.",
       "The {N2} molecules are faster, but being lighter they carry the same average kinetic energy as the slower {CO2} molecules.",
       "Pressure depends on how many particles hit the walls; the average kinetic energy per particle is set by temperature alone."],
      "What single variable sets the average kinetic energy?",
      "Same temperature, so <b>the same average kinetic energy</b>; the lighter {N2} molecules simply move faster.", 2)

    Q(T, "At the same temperature, which atoms move fastest on average?",
      ["He (4.003 g/mol)", "Ar (39.95 g/mol)", "Kr (83.80 g/mol)", "Xe (131.29 g/mol)"],
      ["All four have the same average kinetic energy, so the lightest atoms must move fastest.",
       "Argon atoms are about ten times heavier than helium atoms, so they move more slowly at the same temperature.",
       "Krypton is heavier than both helium and argon, so its atoms are slower.",
       "Xenon is the heaviest, so its atoms are the slowest, not the fastest. Heavier atoms do not have more kinetic energy at the same temperature."],
      "Same temperature means same average kinetic energy. Which atoms must move fastest to get it?",
      "Same kinetic energy, so the lightest moves fastest: <b>He</b>.", 1)

    Q(T, "Cotton swabs soaked in ammonia ({NH3}, 17.031 g/mol) and hydrochloric acid ({HCl}, 36.46 g/mol) are placed at opposite ends of a long glass tube at the same time. A white ring of {NH4Cl} forms where the two gases meet. Where does the ring form?",
      ["Closer to the {HCl} end, because {NH3} molecules move faster", "Closer to the {NH3} end, because {NH3} molecules move faster",
       "Exactly in the middle, because both gases have the same average kinetic energy", "Closer to the {HCl} end, because {HCl} molecules move faster"],
      ["The lighter {NH3} molecules diffuse faster, so they travel farther down the tube before meeting the slower {HCl}.",
       "{NH3} is faster, so it covers more of the tube; the gases meet away from the {NH3} end.",
       "Equal kinetic energy does not mean equal speed: the lighter molecules move faster.",
       "{HCl} is the heavier gas, so it moves more slowly; the ring forms near its end because the {NH3} travels farther."],
      "Which gas is lighter, and so diffuses faster?",
      "{NH3} is lighter and diffuses faster, so it travels farther: <b>the ring forms closer to the {HCl} end</b>.", 3)

    Q(T, "The Kelvin temperature of a gas sample is doubled. According to kinetic molecular theory, what happens to the average kinetic energy of its particles?",
      ["It doubles.", "It is cut in half.", "It stays the same, because the number of particles does not change.", "It doubles, because each particle doubles in size."],
      ["Average kinetic energy is proportional to the Kelvin temperature, so doubling the temperature doubles it.",
       "Lower kinetic energy would mean a lower temperature. The two rise together.",
       "The kinetic energy per particle depends on temperature, not on how many particles there are.",
       "The energy doubles, but not because of size; gas particles do not grow when heated, they move faster."],
      "Average kinetic energy is proportional to which temperature?",
      "Average kinetic energy is proportional to the Kelvin temperature: <b>it doubles</b>.", 2)

    Q(T, "A sample of carbon dioxide gas starts at room temperature and 1 atm. Which change makes it depart <b>more</b> from ideal-gas behavior?",
      ["Cooling it toward the temperature where it condenses", "Heating it to a higher temperature",
       "Lowering its pressure", "Letting it expand into a larger container"],
      ["Slower particles near condensation feel their attractions, which the ideal model ignores.",
       "Faster particles make attractions less important, so the gas behaves more ideally.",
       "Lower pressure spreads the particles out, so the gas behaves more ideally.",
       "Expanding lowers the pressure and spreads the particles out, which makes the gas more ideal."],
      "When do attractions between particles start to matter?",
      "Real gases depart from ideal behavior at low temperature and high pressure: <b>cooling it toward condensation</b>.", 2)

    Q(T, "A liter of air has a mass of only about 1.2 g, while a liter of water has a mass of about a kilogram. Which idea of kinetic molecular theory explains this?",
      ["Gas particles are tiny compared with the distances between them, so a gas is mostly empty space.",
       "Gas particles are much lighter than water molecules.",
       "Gas particles attract each other weakly, so they float.",
       "Gas particles lose energy in collisions and settle out."],
      ["Few particles fit in a liter of gas because they are spread far apart, so the mass per liter is low.",
       "The particles in air ({N2}, 28.014 g/mol; {O2}, 31.998 g/mol) are actually heavier than water molecules (18.015 g/mol). The difference is spacing, not particle mass.",
       "In KMT gas particles neither attract nor repel; that does not make a gas less dense.",
       "Collisions in KMT are elastic, and gas particles never settle out."],
      "Compare how far apart the particles are in a gas and in a liquid.",
      "<b>A gas is mostly empty space</b>, so a liter holds far fewer particles than a liter of liquid.", 1)

    Q(T, "The tip of a syringe is sealed, and the plunger is pushed in at constant temperature. Why does the pressure of the trapped air rise?",
      ["The same number of particles hit a smaller wall area more often.",
       "The particles move faster because they have less room.",
       "The particles become larger when they are squeezed.",
       "Squeezing the air makes the particles attract each other."],
      ["The temperature, and so the particles' speed, is unchanged, but the particles now reach the walls more often, so there are more hits per second on each part of the wall.",
       "At constant temperature the average speed does not change; only the number of hits on the walls does.",
       "Particle size does not change; only the spaces between the particles shrink.",
       "KMT treats gas particles as having no attractions; pressure comes from collisions."],
      "Speed stays the same at constant temperature. What changes?",
      "Same particles, less room: <b>more frequent collisions with the walls</b>, so higher pressure.", 2)

    # ======================= ch10-pressure (10) =======================
    T = 'ch10-pressure'
    Q(T, "A person wearing narrow high heels sinks into a soft lawn, but the same person in flat shoes does not. Why?",
      ["The same force is spread over a smaller area, so the pressure is greater.",
       "The person weighs more in high heels.",
       "Pressure depends only on force, so the heels must push harder.",
       "A smaller area gives a smaller pressure, so the lawn is softer under heels."],
      ["P = F/A: the person's weight (the force) is the same, but the heels concentrate it on a small area.",
       "The person's weight, the force, is the same in either pair of shoes.",
       "Pressure is force divided by area, so area matters as much as force.",
       "A smaller area gives a greater pressure, not a smaller one."],
      "Use P = F/A.",
      "Same force, smaller area: <b>greater pressure</b> (P = F/A).", 1)

    Q(T, "In a mercury barometer, what holds up the column of mercury in the closed glass tube?",
      ["The atmosphere pushing down on the mercury in the open dish",
       "Suction from the vacuum at the top of the tube", "The mercury sticking to the glass walls",
       "The weight of the mercury in the dish pushing up"],
      ["Air presses on the open dish; the column rises until its weight balances that push, about 760 mm at sea level.",
       "A vacuum exerts no pull. The column is pushed up from below by air pressure on the dish.",
       "Mercury does not wet glass, and sticking could not hold up a 760 mm column.",
       "The mercury in the dish is pushed on by the air; its own weight does not lift the column."],
      "Which side of the mercury has air on it?",
      "<b>Atmospheric pressure on the dish</b> pushes the mercury up the tube until the column's weight balances it.", 2)

    Q(T, "A hiker drinks from a plastic water bottle on the summit of Mount Whitney (14,505 ft), caps it tightly, and hikes down to Lone Pine (3,727 ft). The empty bottle is crumpled. Why?",
      ["The air pressure outside is greater at the lower elevation, so the outside air pushes the bottle in.",
       "The air inside the bottle escaped through the cap on the way down.",
       "The air pressure outside is lower at the lower elevation, so the bottle collapses.",
       "The air inside the bottle got heavier at the lower elevation."],
      ["The bottle was sealed at the low summit pressure. Lower down there is more air above, so the outside pressure is higher and squeezes the bottle until the pressures balance.",
       "The cap was tight; the amount of air inside did not change.",
       "Air pressure is higher at lower elevations, because there is more air above.",
       "The mass of the trapped air does not change; the outside pressure does."],
      "Is there more air above you at the summit or in the valley?",
      "Lower elevation, more air above, <b>higher outside pressure</b>, which crushes the bottle sealed at the summit.", 2)

    P = '742'; v = D(P) / ATM_MM
    Q(T, "A barometer in a Clovis classroom reads %s mmHg. What is the pressure in atmospheres?" % P,
      [S(v, 3, 'atm'), S(D(P) * ATM_MM, 3, 'atm'), S(D(P) / KPA, 3, 'atm'), S(D(P) / PSI, 3, 'atm')],
      ["%s mmHg &times; (1 atm / 760 mmHg). A little less than 760 mmHg is a little less than 1 atm." % P,
       "This multiplies by 760. To go from mmHg to atm, divide by 760 (put mmHg on the bottom so it cancels).",
       "This divides by 101.325, the number of kPa in 1 atm. The reading is in mmHg, so use 760 mmHg = 1 atm.",
       "This divides by 14.7, the number of psi in 1 atm. The reading is in mmHg."],
      "1 atm = 760 mmHg; set it up so mmHg cancels.",
      "%s mmHg &times; (1 atm / 760 mmHg) = <b>%s</b>." % (P, S(v, 3, 'atm')), 2, 1)

    P = '2.40'; v = D(P) * KPA
    Q(T, "A hyperbaric oxygen chamber is pressurized to %s atm. What is this pressure in kilopascals?" % P,
      [S(v, 3, 'kPa'), S(D(P) * 101325, 3, 'kPa'), S(D(P) / KPA, 3, 'kPa'), S(D(P) * ATM_MM, 3, 'kPa')],
      ["%s atm &times; (101.325 kPa / 1 atm)." % P,
       "This uses 101,325, the number of <i>pascals</i> in 1 atm. In kilopascals, 1 atm = 101.325 kPa.",
       "This divides by 101.325. Going from atm to kPa, multiply: 1 atm is about 101 kPa, so the answer must be bigger than the number of atm.",
       "This multiplies by 760, which gives mmHg, not kPa."],
      "1 atm = 101.325 kPa.",
      "%s atm &times; (101.325 kPa / 1 atm) = <b>%s</b>." % (P, S(v, 3, 'kPa')), 2, 1)

    P = '85.5'; v = D(P) / PSI
    Q(T, "A road bike tire is inflated to %s psi. What is this pressure in atmospheres?" % P,
      [S(v, 3, 'atm'), S(D(P) * PSI, 3, 'atm'), S(D(P) / ATM_MM, 3, 'atm'), S(D(P) / KPA, 3, 'atm')],
      ["%s psi &times; (1 atm / 14.7 psi)." % P,
       "This multiplies by 14.7; the conversion factor is flipped. Put psi on the bottom so it cancels.",
       "This divides by 760, the number of mmHg in 1 atm. The reading is in psi: 1 atm = 14.7 psi.",
       "This divides by 101.325, the number of kPa in 1 atm. The reading is in psi."],
      "1 atm = 14.7 psi.",
      "%s psi &times; (1 atm / 14.7 psi) = <b>%s</b>." % (P, S(v, 3, 'atm')), 2, 1)

    P = '41.5'; v = D(P) / ATM_MM * KPA
    Q(T, "Some hospitals report blood gases in kilopascals. A patient's arterial carbon dioxide pressure is %s mmHg. What is it in kPa?" % P,
      [S(v, 3, 'kPa'), S(D(P) * KPA, 3, 'kPa'), S(D(P) / KPA, 3, 'kPa'), S(D(P) * ATM_MM / KPA, 3, 'kPa')],
      ["Go through atm: %s mmHg &times; (1 atm / 760 mmHg) &times; (101.325 kPa / 1 atm)." % P,
       "This multiplies mmHg by 101.325 as if the value were in atm. Convert mmHg to atm first (divide by 760).",
       "This divides by 101.325 and never uses 760 mmHg = 1 atm.",
       "This flips both conversion factors (&times; 760 &divide; 101.325). Check: 760 mmHg = 101.325 kPa, so the number of kPa must be smaller than the number of mmHg."],
      "Use 760 mmHg = 101.325 kPa (both equal 1 atm).",
      "%s mmHg &times; (101.325 kPa / 760 mmHg) = <b>%s</b>." % (P, S(v, 3, 'kPa')), 3, 1)

    P = '18.6'; v = D(P) / ATM_MM
    Q(T, "A laboratory vacuum pump lowers the pressure in a flask to %s torr. What is this pressure in atmospheres?" % P,
      [S(v, 3, 'atm'), S(D(P) * ATM_MM, 3, 'atm'), S(D(P) / KPA, 3, 'atm'), S(D(P) / PSI, 3, 'atm')],
      ["1 torr = 1 mmHg, so 760 torr = 1 atm: %s torr &times; (1 atm / 760 torr)." % P,
       "This multiplies by 760; a vacuum must be far below 1 atm. Divide by 760.",
       "This divides by 101.325 (kPa per atm). The pressure is in torr: 760 torr = 1 atm.",
       "This divides by 14.7 (psi per atm). The pressure is in torr: 760 torr = 1 atm."],
      "760 torr = 1 atm.",
      "%s torr &times; (1 atm / 760 torr) = <b>%s</b>." % (P, S(v, 3, 'atm')), 2, 1)

    P = '101.9'; v = D(P) / KPA * ATM_MM
    Q(T, "A weather report gives the air pressure in Fresno as %s kPa. What is this in mmHg?" % P,
      [S(v, 4, 'mmHg'), S(D(P) * ATM_MM, 4, 'mmHg'), S(D(P) / ATM_MM, 4, 'mmHg'), S(D(P) * KPA / ATM_MM, 4, 'mmHg')],
      ["%s kPa &times; (760 mmHg / 101.325 kPa); the answer keeps 4 significant figures, like %s." % (P, P),
       "This multiplies by 760 but never divides by 101.325, as if the pressure were in atm.",
       "This divides by 760. The pressure is in kPa; convert with 101.325 kPa = 760 mmHg.",
       "This flips the conversion factor (&times; 101.325 &divide; 760). Air pressure near sea level must be close to 760 mmHg."],
      "101.325 kPa = 760 mmHg.",
      "%s kPa &times; (760 mmHg / 101.325 kPa) = <b>%s</b>." % (P, S(v, 4, 'mmHg')), 2, 1)

    P = '124'; v = D(P) / ATM_MM
    Q(T, "A patient's blood pressure is recorded as 124/82 mmHg. Express the systolic value, 124 mmHg, in atmospheres.",
      [S(v, 3, 'atm'), S(D(P) * ATM_MM, 3, 'atm'), S(D(P) / D('101.325'), 3, 'atm'), S(D(P) / D('14.7'), 3, 'atm')],
      ["124 mmHg &times; (1 atm / 760 mmHg).",
       "This multiplies by 760; going from mmHg to atm, divide by 760.",
       "This uses 101.325, the number of kPa in 1 atm, not mmHg.",
       "This uses 14.7, the number of psi in 1 atm, not mmHg."],
      "Put 760 mmHg on the bottom so mmHg cancels.",
      "124 mmHg &times; (1 atm / 760 mmHg) = <b>%s</b>." % S(v, 3, 'atm'), 1, 1)

    # ======================= ch10-laws (15) =======================
    T = 'ch10-laws'
    Q(T, "In Gay-Lussac's law, which two variables are held constant?",
      ["Volume and amount of gas (moles)", "Pressure and amount of gas (moles)", "Temperature and amount of gas (moles)", "Pressure and temperature"],
      ["Gay-Lussac's law relates pressure and Kelvin temperature in a rigid container (constant V) with a fixed amount of gas.",
       "Constant pressure and moles is Charles's law, which relates volume and temperature.",
       "Constant temperature and moles is Boyle's law, which relates pressure and volume.",
       "Constant pressure and temperature is Avogadro's law, which relates volume and moles."],
      "Gay-Lussac relates P and T. Which two of the four variables are left?",
      "Gay-Lussac (P<sub>1</sub>/T<sub>1</sub> = P<sub>2</sub>/T<sub>2</sub>) holds <b>volume and moles</b> constant.", 1)

    Q(T, "An air-filled balloon is moved from a warm room into a freezer. The pressure and the amount of air stay the same. What happens to the balloon's volume?",
      ["It decreases, because volume and Kelvin temperature are directly related.",
       "It increases, because volume and temperature are inversely related.",
       "It stays the same, because the amount of air does not change.",
       "It decreases, because the pressure on the balloon increases."],
      ["Charles's law: colder particles move more slowly and push the walls less, so the balloon shrinks.",
       "Volume and temperature are directly related (Charles's law); cooling shrinks the gas.",
       "The amount of air is constant, but the temperature drops, so the volume drops.",
       "The pressure is constant here; the change comes from the temperature."],
      "Which law relates V and T, and is it direct or inverse?",
      "Charles's law, direct: lower temperature, <b>smaller volume</b>.", 1)

    Q(T, "A rigid tank of gas (constant volume) has its amount of gas doubled, and at the same time its Kelvin temperature is doubled. What happens to the pressure?",
      ["It increases four times.", "It doubles.", "It stays the same.", "It is cut in half."],
      ["P &prop; nT/V: doubling n doubles P, and doubling T doubles P again, so P becomes 4 times as large.",
       "This counts only one of the two changes; each one doubles the pressure.",
       "Both changes raise the pressure; neither one cancels the other.",
       "More gas and hotter gas both mean more frequent, harder collisions, so the pressure goes up."],
      "Do each change separately: what does doubling n do? What does doubling T do?",
      "&times;2 for the moles and &times;2 for the temperature: <b>4 times the pressure</b>.", 3)

    P1, V1, P2 = '3.45', '1.60', '1.05'; v = D(P1) * D(V1) / D(P2); n = ns(P1, V1, P2)
    Q(T, "An air bubble released by a scuba diver has a volume of %s mL where the pressure is %s atm. What is its volume just below the surface, where the pressure is %s atm? (Assume constant temperature.)" % (V1, P1, P2),
      [S(v, n, 'mL'), S(D(V1) * D(P2) / D(P1), n, 'mL'), S(D(P1) * D(V1), n, 'mL'), S(D(P1) * D(P2) / D(V1), n, 'mL')],
      ["Boyle's law: V<sub>2</sub> = P<sub>1</sub>V<sub>1</sub>/P<sub>2</sub>. The pressure fell, so the bubble grew.",
       "This sets up Boyle's law as a ratio (V<sub>2</sub> = V<sub>1</sub>P<sub>2</sub>/P<sub>1</sub>). P and V are inverse, so the bubble must get bigger as the pressure falls.",
       "This is P<sub>1</sub>V<sub>1</sub> without dividing by P<sub>2</sub>.",
       "This rearranges incorrectly, dividing by the volume. Solve P<sub>1</sub>V<sub>1</sub> = P<sub>2</sub>V<sub>2</sub> for V<sub>2</sub>."],
      "Pressure goes down, so should the volume go up or down?",
      "V<sub>2</sub> = (%s atm)(%s mL) / %s atm = <b>%s</b>." % (P1, V1, P2, S(v, n, 'mL')), 2, 1)

    P1, V1, V2 = '0.955', '4.25', '1.65'; v = D(P1) * D(V1) / D(V2); n = ns(P1, V1, V2)
    Q(T, "A gas in a cylinder with a movable piston occupies %s L at %s atm. It is compressed at constant temperature to %s L. What is the new pressure?" % (V1, P1, V2),
      [S(v, n, 'atm'), S(D(P1) * D(V2) / D(V1), n, 'atm'), S(D(P1) * D(V1), n, 'atm'), S(D(V1) * D(V2) / D(P1), n, 'atm')],
      ["P<sub>2</sub> = P<sub>1</sub>V<sub>1</sub>/V<sub>2</sub>. The volume shrank, so the pressure rose.",
       "This uses Boyle's law as a ratio. Squeezing a gas raises its pressure, but this answer is lower than %s atm." % P1,
       "This is P<sub>1</sub>V<sub>1</sub>, in atm&middot;L; it still needs to be divided by V<sub>2</sub>.",
       "This multiplies the two volumes and divides by the pressure; solve P<sub>1</sub>V<sub>1</sub> = P<sub>2</sub>V<sub>2</sub> for P<sub>2</sub>."],
      "Boyle's law: P<sub>1</sub>V<sub>1</sub> = P<sub>2</sub>V<sub>2</sub>.",
      "P<sub>2</sub> = (%s atm)(%s L) / %s L = <b>%s</b>." % (P1, V1, V2, S(v, n, 'atm')), 2, 1)

    P1, V1, V2 = '760.', '2.40', '2.52'; v = D('760') * D(V1) / D(V2); n = ns(P1, V1, V2)
    Q(T, "As the diaphragm contracts, the volume of a person's lungs increases from %s L to %s L at constant temperature, before any air flows in. If the pressure in the lungs started at %s mmHg, what is it at %s L?" % (V1, V2, P1, V2),
      [S(v, n, 'mmHg'), S(D('760') * D(V2) / D(V1), n, 'mmHg'), S(D('760') * D(V1), n, 'mmHg'), S(D(V1) / D(V2), n, 'mmHg')],
      ["Boyle's law: P<sub>2</sub> = P<sub>1</sub>V<sub>1</sub>/V<sub>2</sub>. The pressure drops below atmospheric, so air flows in.",
       "This is Boyle's law set up as a ratio; it predicts a higher pressure, which would push air out, not draw it in.",
       "This is P<sub>1</sub>V<sub>1</sub>, which still needs to be divided by V<sub>2</sub>.",
       "This is only the volume ratio V<sub>1</sub>/V<sub>2</sub>; multiply it by the starting pressure."],
      "The volume went up a little. What must the pressure do?",
      "P<sub>2</sub> = (760. mmHg)(%s L) / %s L = <b>%s</b>, a little below atmospheric pressure, so air flows in." % (V1, V2, S(v, n, 'mmHg')), 2, 1)

    V1, C1, C2 = '1.85', '24.5', '-18.5'; v = D(V1) * TK(C2) / TK(C1); n = ns(V1, sfT(C1), sfT(C2))
    Q(T, "A %s L balloon at %s °C is put in a freezer at %s °C. Assuming the pressure stays constant, what is its new volume?" % (V1, C1, C2),
      [S(v, n, 'L'), S(D(V1) * D(C2) / D(C1), n, 'L'), S(D(V1) * TK(C1) / TK(C2), n, 'L'), S(D(V1) * TK(C2) / D(C1), n, 'L')],
      ["Charles's law with kelvins: V<sub>2</sub> = V<sub>1</sub>T<sub>2</sub>/T<sub>1</sub>. Cooler gas, smaller volume.",
       "This uses Celsius temperatures. A negative volume is impossible; gas laws need kelvins.",
       "This turns the temperature ratio upside down, so the balloon grows when it is cooled.",
       "This converts only the freezer temperature to kelvins; both temperatures must be in kelvins."],
      "Convert both temperatures to kelvins, then V<sub>1</sub>/T<sub>1</sub> = V<sub>2</sub>/T<sub>2</sub>.",
      "%s; %s. V<sub>2</sub> = %s L &times; %s K / %s K = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), kt(C2, 'T<sub>2</sub>'), V1, TKs(C2), TKs(C1), S(v, n, 'L')), 2, 1)

    V1, C1, V2 = '45.0', '20.5', '49.5'; v = TK(C1) * D(V2) / D(V1); n = ns(V1, V2, sfT(C1))
    Q(T, "A gas-tight syringe holds %s mL of air at %s °C. It is warmed at constant pressure until the volume is %s mL. What is the final temperature in kelvins?" % (V1, C1, V2),
      [S(v, n, 'K'), S(D(C1) * D(V2) / D(V1), n, 'K'), S(TK(C1) * D(V1) / D(V2), n, 'K'), S(v, n, '°C')],
      ["T<sub>2</sub> = T<sub>1</sub>V<sub>2</sub>/V<sub>1</sub> with T<sub>1</sub> in kelvins. Larger volume, higher temperature.",
       "This uses the Celsius temperature in Charles's law. Convert to kelvins first.",
       "This inverts the volume ratio, giving a lower temperature for a larger volume.",
       "This is the right number, but it is in kelvins, not degrees Celsius."],
      "Convert %s °C to kelvins, then T<sub>2</sub> = T<sub>1</sub> &times; V<sub>2</sub>/V<sub>1</sub>." % C1,
      "%s. T<sub>2</sub> = %s K &times; %s mL / %s mL = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), TKs(C1), V2, V1, S(v, n, 'K')), 2, 1)

    P1, C1, C2 = '1.85', '21.5', '425'; v = D(P1) * TK(C2) / TK(C1); n = ns(P1, sfT(C1), sfT(C2))
    Q(T, "An aerosol can contains gas at %s atm at %s °C. If it is thrown into a fire and heated to %s °C, what pressure would the gas reach (if the can did not burst)?" % (P1, C1, C2),
      [S(v, n, 'atm'), S(D(P1) * D(C2) / D(C1), n, 'atm'), S(D(P1) * TK(C1) / TK(C2), n, 'atm'), S(D(P1) * D(C2) / TK(C1), n, 'atm')],
      ["Gay-Lussac's law with kelvins: P<sub>2</sub> = P<sub>1</sub>T<sub>2</sub>/T<sub>1</sub>. This is why aerosol cans warn against heat.",
       "This uses Celsius temperatures, which exaggerates the change. Gas laws need kelvins.",
       "This inverts the temperature ratio, so the pressure falls as the can heats up.",
       "This converts only the starting temperature to kelvins; the fire temperature must be converted too."],
      "Rigid can: P and T in kelvins are directly related.",
      "%s; %s. P<sub>2</sub> = %s atm &times; %s K / %s K = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), kt(C2, 'T<sub>2</sub>'), P1, TKs(C2), TKs(C1), S(v, n, 'atm')), 2, 1)

    P1, C1, P2 = '2.25', '15.5', '2.48'; v = TK(C1) * D(P2) / D(P1); n = ns(P1, P2, sfT(C1))
    Q(T, "The air in a tire is at %s atm at %s °C. After a drive the pressure is %s atm. Assuming the volume of the tire does not change, what is the temperature of the air in kelvins?" % (P1, C1, P2),
      [S(v, n, 'K'), S(D(C1) * D(P2) / D(P1), n, 'K'), S(TK(C1) * D(P1) / D(P2), n, 'K'), S(v, n, '°C')],
      ["T<sub>2</sub> = T<sub>1</sub>P<sub>2</sub>/P<sub>1</sub> with T<sub>1</sub> in kelvins. Higher pressure, higher temperature.",
       "This uses the Celsius temperature; convert to kelvins before using a gas law.",
       "This inverts the pressure ratio, predicting a cooler tire at higher pressure.",
       "This is the kelvin value labeled as degrees Celsius; tires do not reach temperatures that high."],
      "Gay-Lussac's law: P<sub>1</sub>/T<sub>1</sub> = P<sub>2</sub>/T<sub>2</sub>, with kelvins.",
      "%s. T<sub>2</sub> = %s K &times; %s atm / %s atm = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), TKs(C1), P2, P1, S(v, n, 'K')), 2, 1)

    V1, n1, n2 = '5.80', '0.245', '0.185'; v = D(V1) * D(n2) / D(n1); n = ns(V1, n1, n2)
    Q(T, "A balloon holds %s mol of helium and has a volume of %s L. Helium leaks out until %s mol remains, at the same temperature and pressure. What is the new volume?" % (n1, V1, n2),
      [S(v, n, 'L'), S(D(V1) * D(n1) / D(n2), n, 'L'), S(D(V1) * (D(n1) - D(n2)) / D(n1), n, 'L'), S(D(n2) / D(n1), n, 'L')],
      ["Avogadro's law: V<sub>2</sub> = V<sub>1</sub>n<sub>2</sub>/n<sub>1</sub>. Fewer moles, smaller volume.",
       "This inverts the mole ratio; the balloon cannot grow as helium leaks out.",
       "This uses the moles that leaked out (%s &minus; %s) instead of the moles that remain." % (n1, n2),
       "This is only the mole ratio n<sub>2</sub>/n<sub>1</sub>; multiply it by the starting volume."],
      "V and n are directly related at constant T and P.",
      "V<sub>2</sub> = %s L &times; %s mol / %s mol = <b>%s</b>." % (V1, n2, n1, S(v, n, 'L')), 2, 1)

    V1, P1, C1, P2, C2 = '2.65', '1.12', '18.5', '0.875', '37.5'
    v = D(V1) * D(P1) / D(P2) * TK(C2) / TK(C1); n = ns(V1, P1, P2, sfT(C1), sfT(C2))
    Q(T, "A sample of nitrogen occupies %s L at %s atm and %s °C. What volume does it occupy at %s atm and %s °C?" % (V1, P1, C1, P2, C2),
      [S(v, n, 'L'), S(D(V1) * D(P1) / D(P2) * D(C2) / D(C1), n, 'L'), S(D(V1) * D(P2) / D(P1) * TK(C2) / TK(C1), n, 'L'), S(D(V1) * D(P1) / D(P2) * TK(C1) / TK(C2), n, 'L')],
      ["Combined gas law: V<sub>2</sub> = V<sub>1</sub> &times; (P<sub>1</sub>/P<sub>2</sub>) &times; (T<sub>2</sub>/T<sub>1</sub>). Lower pressure and higher temperature both make the volume larger.",
       "This uses Celsius temperatures; 37.5/18.5 more than doubles the volume. Use kelvins.",
       "This inverts the pressure ratio. The pressure fell, so the volume must rise, not fall.",
       "This inverts the temperature ratio. The gas was warmed, so that factor should be greater than 1."],
      "Predict first: lower P makes V larger; higher T makes V larger.",
      "%s; %s. V<sub>2</sub> = %s L &times; (%s / %s) &times; (%s K / %s K) = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), kt(C2, 'T<sub>2</sub>'), V1, P1, P2, TKs(C2), TKs(C1), S(v, n, 'L')), 3, 1)

    V1, P1, C1, V2, C2 = '11.5', '1.01', '23.5', '18.4', '-8.5'
    v = D(P1) * D(V1) / D(V2) * TK(C2) / TK(C1); n = ns(V1, P1, V2, sfT(C1), sfT(C2))
    Q(T, "A helium balloon holds %s L at %s atm and %s °C. It rises to where its volume is %s L and the temperature is %s °C. What is the pressure there?" % (V1, P1, C1, V2, C2),
      [S(v, n, 'atm'), S(D(P1) * D(V1) / D(V2) * D(C2) / D(C1), n, 'atm'), S(D(P1) * D(V2) / D(V1) * TK(C2) / TK(C1), n, 'atm'), S(D(P1) * D(V1) / D(V2) * TK(C1) / TK(C2), n, 'atm')],
      ["P<sub>2</sub> = P<sub>1</sub> &times; (V<sub>1</sub>/V<sub>2</sub>) &times; (T<sub>2</sub>/T<sub>1</sub>), with kelvins.",
       "This uses Celsius temperatures; a negative pressure is impossible. Convert to kelvins.",
       "This inverts the volume ratio. The balloon got bigger, which goes with a lower pressure.",
       "This inverts the temperature ratio. Cooling lowers the pressure, so T<sub>2</sub>/T<sub>1</sub> must be less than 1."],
      "Solve P<sub>1</sub>V<sub>1</sub>/T<sub>1</sub> = P<sub>2</sub>V<sub>2</sub>/T<sub>2</sub> for P<sub>2</sub>.",
      "%s; %s. P<sub>2</sub> = %s atm &times; (%s / %s) &times; (%s K / %s K) = <b>%s</b>." % (kt(C1, 'T<sub>1</sub>'), kt(C2, 'T<sub>2</sub>'), P1, V1, V2, TKs(C2), TKs(C1), S(v, n, 'atm')), 3, 1)

    C = '-12.5'
    Q(T, "Before using Charles's law, a student must convert %s °C to kelvins. What is the correct value?" % C,
      [TKs(C) + ' K', TKs(C[1:]) + ' K', qd(D(C) - K0, dp(C)) + ' K', format(D(C) + K0, 'f') + ' K'],
      ["K = °C + 273.15 = %s + 273.15, kept to the tenths place like %s." % (C, C),
       "This drops the minus sign; %s °C is below freezing, so the kelvin value must be below 273.15 K." % C,
       "This subtracts 273.15. Kelvin temperatures are never negative; add 273.15.",
       "This keeps two decimal places. By the addition rule, the answer keeps the decimal places of the measurement (one)."],
      "K = °C + 273.15; keep the measurement's decimal places.",
      "%s + 273.15 = <b>%s K</b>." % (C, TKs(C)), 1, 1)

    Q(T, "The table shows data for a gas sample at constant temperature. Which relationship do the data show?",
      ["An inverse relationship: P &times; V stays the same (Boyle's law)", "A direct relationship: P/V stays the same (Charles's law)",
       "A direct relationship between pressure and temperature (Gay-Lussac's law)", "No relationship: the volume changes randomly"],
      ["Each P &times; V product is 6.00 atm&middot;L: doubling the pressure halves the volume.",
       "P/V is not constant (0.500/12.0 is not 3.00/2.00), and Charles's law relates volume and temperature, not pressure and volume.",
       "Temperature is constant here; the data relate pressure and volume.",
       "The volume falls in a regular way as the pressure rises; P &times; V is the same every time."],
      "Multiply P and V in each row. Then divide them.",
      "P &times; V = 6.00 atm&middot;L in every row, so P and V are <b>inversely related (Boyle's law)</b>.", 2, 0,
      [{"type": "table", "cap": "A gas sample at constant temperature", "head": ["Pressure (atm)", "Volume (L)"],
        "rows": [["0.500", "12.0"], ["1.00", "6.00"], ["2.00", "3.00"], ["3.00", "2.00"]]}])

    # ======================= ch10-ideal (13) =======================
    T = 'ch10-ideal'
    V, C, P = '3.75', '22.5', '8.65'; v = D(P) * D(V) / (R * TK(C)); n = ns(P, V, sfT(C))
    Q(T, "A %s L tank of helium is at %s atm and %s °C. How many moles of helium does it contain?" % (V, P, C),
      [S(v, n, 'mol'), S(D(P) * D(V) / (R * D(C)), n, 'mol'), S(D(V) / VM, n, 'mol'), S(R * TK(C) / (D(P) * D(V)), n, 'mol')],
      ["n = PV/RT with T in kelvins; atm, L, and K match R = 0.082058 L&middot;atm/(mol&middot;K).",
       "This uses %s °C for T. R needs kelvins." % C,
       "This divides by 22.4 L/mol, the molar volume at STP. The tank is far above 1 atm and above 0 °C, so use PV = nRT.",
       "This is RT/PV, the reciprocal of the answer. Solve PV = nRT for n: n = PV/(RT)."],
      "One set of conditions: use PV = nRT and solve for n.",
      "%s. n = (%s atm)(%s L) / [(0.082058)(%s K)] = <b>%s</b>." % (kt(C), P, V, TKs(C), S(v, n, 'mol')), 2, 1)

    nn, P, C = '0.685', '1.15', '31.5'; v = D(nn) * R * TK(C) / D(P); n = ns(nn, P, sfT(C))
    Q(T, "What volume does %s mol of {CO2} occupy at %s atm and %s °C?" % (nn, P, C),
      [S(v, n, 'L'), S(D(nn) * R * D(C) / D(P), n, 'L'), S(D(nn) * VM, n, 'L'), S(D(nn) * R * TK(C), n, 'L')],
      ["V = nRT/P, with T in kelvins.",
       "This uses the Celsius temperature in PV = nRT; convert to kelvins.",
       "This uses 22.4 L/mol, which applies only at STP (273 K and 1 atm).",
       "This is nRT without dividing by the pressure."],
      "Solve PV = nRT for V.",
      "%s. V = (%s mol)(0.082058)(%s K) / %s atm = <b>%s</b>." % (kt(C), nn, TKs(C), P, S(v, n, 'L')), 2, 1)

    nn, V, C = '0.0425', '1.25', '24.0'; v = D(nn) * R2 * TK(C) / D(V); n = ns(nn, V, sfT(C), '62.36')
    va = D(nn) * R * TK(C) / D(V)
    Q(T, "A %s L container holds %s mol of nitrous oxide ({N2O}) at %s °C. Using R = 62.36 L&middot;torr/(mol&middot;K), what is the pressure in torr?" % (V, nn, C),
      [S(v, n, 'torr'), S(va, n, 'torr'), S(D(nn) * R2 * D(C) / D(V), n, 'torr'), S(va / ATM_MM, n, 'torr')],
      ["P = nRT/V; with R = 62.36 the pressure comes out in torr.",
       "This uses R = 0.082058, which gives the pressure in atm, not torr.",
       "This uses %s °C for T; R needs kelvins." % C,
       "This finds the pressure in atm and then divides by 760; going from atm to torr you multiply by 760."],
      "The value of R decides the pressure unit.",
      "%s. P = (%s mol)(62.36)(%s K) / %s L = <b>%s</b>." % (kt(C), nn, TKs(C), V, S(v, n, 'torr')), 2, 1)

    V, nn, P = '5.25', '0.415', '2.05'; v = D(P) * D(V) / (D(nn) * R); n = ns(P, V, nn)
    Q(T, "A %s L cylinder contains %s mol of argon at %s atm. What is the temperature of the gas in kelvins?" % (V, nn, P),
      [S(v, n, 'K'), S(D(nn) * R / (D(P) * D(V)), n, 'K'), S(D(P) * D(V) / (D(nn) * R2), n, 'K'), S(v, n, '°C')],
      ["T = PV/(nR); atm and L match R = 0.082058.",
       "This is nR/(PV), the reciprocal. Solve PV = nRT for T.",
       "This uses R = 62.36, which needs the pressure in torr. With atm, use 0.082058.",
       "PV/(nR) gives kelvins, not degrees Celsius."],
      "Solve PV = nRT for T.",
      "T = (%s atm)(%s L) / [(%s mol)(0.082058)] = <b>%s</b>." % (P, V, nn, S(v, n, 'K')), 2, 1)

    Q(T, "A student will use PV = nRT with the pressure in mmHg and the volume in liters, without converting units. Which value of R must be used?",
      ["62.36 L&middot;torr/(mol&middot;K)", "0.082058 L&middot;atm/(mol&middot;K)", "8.3144 J/(mol&middot;K)", "22.4 L/mol"],
      ["1 torr = 1 mmHg, so this R matches a pressure in mmHg, a volume in L, and T in K.",
       "This R needs the pressure in atm; with mmHg the answer would be off by a factor of 760.",
       "This R is in energy units, for energy calculations.",
       "22.4 L/mol is the molar volume at STP, not a value of R."],
      "Match the pressure unit in R to the pressure unit you have.",
      "mmHg = torr, so use <b>R = 62.36 L&middot;torr/(mol&middot;K)</b>.", 1)

    Q(T, "A student plugs 455 mL, 735 mmHg, and 25.0 °C directly into PV = nRT with R = 0.082058 L&middot;atm/(mol&middot;K). Which conversions are needed first?",
      ["mL to L, mmHg to atm, and °C to K", "Only °C to K", "mL to L and °C to K only", "mmHg to atm and grams to moles"],
      ["R = 0.082058 L&middot;atm/(mol&middot;K) needs liters, atmospheres, and kelvins, so all three givens must be converted.",
       "Temperature must be in kelvins, but the volume and pressure must also match R's units.",
       "The pressure is in mmHg; with R = 0.082058 it must be in atm (or use R = 62.36 instead).",
       "No mass is given here, and the volume and temperature still need converting."],
      "Read the units in R: L, atm, mol, K.",
      "R needs L, atm, and K: convert <b>mL to L, mmHg to atm, and °C to K</b>.", 2)

    V, P, C = '285', '738', '21.5'; Pa = D(P) / ATM_MM
    v = Pa * D(V) / 1000 / (R * TK(C)); n = ns(V, P, sfT(C))
    Q(T, "A %s mL flask holds argon at %s mmHg and %s °C. How many moles of argon are in the flask?" % (V, P, C),
      [S(v, n, 'mol'), S(D(P) * D(V) / 1000 / (R * TK(C)), n, 'mol'), S(Pa * D(V) / (R * TK(C)), n, 'mol'), S(Pa * D(V) / 1000 / (R * D(C)), n, 'mol')],
      ["Convert first: %s mL = 0.%s L and %s mmHg &divide; 760 = %s atm; then n = PV/RT." % (V, V, P, num(Pa, 4)),
       "This puts mmHg into PV = nRT with R = 0.082058, so the answer is 760 times too large.",
       "This uses %s mL as if it were liters, so the answer is 1000 times too large." % V,
       "This uses the Celsius temperature; R needs kelvins."],
      "Line up the units with R = 0.082058 L&middot;atm/(mol&middot;K).",
      "P = %s atm, V = 0.%s L, %s. n = PV/RT = <b>%s</b>." % (num(Pa, 4), V, kt(C), S(v, n, 'mol')), 3, 1)

    nn = '0.365'; v = D(nn) * VM
    Q(T, "What volume does %s mol of {O2} occupy at STP?" % nn,
      [S(v, 3, 'L'), S(D(nn) / VM, 3, 'L'), S(VM / D(nn), 3, 'L'), S(D(nn) * R * D('298.15'), 3, 'L')],
      ["At STP, 1 mol of any gas occupies 22.4 L: %s mol &times; 22.4 L/mol." % nn,
       "This divides by 22.4 L/mol; moles times liters per mole gives liters.",
       "This divides 22.4 by the moles; set it up so mol cancels.",
       "This uses 25 °C (298.15 K) as the standard temperature. STP is 0 °C (273 K) and 1 atm."],
      "At STP, 1 mol = 22.4 L.",
      "%s mol &times; 22.4 L/mol = <b>%s</b>." % (nn, S(v, 3, 'L')), 1, 1)

    g = '7.25'; Mx = mm('CH4'); v = D(g) / Mx * VM
    Q(T, "What volume does %s g of methane, {CH4} (%s g/mol), occupy at STP?" % (g, Mx),
      [S(v, 3, 'L'), S(D(g) * VM, 3, 'L'), S(D(g) / VM, 3, 'L'), S(D(g) / Mx / VM, 3, 'L')],
      ["Grams to moles first (%s &divide; %s), then &times; 22.4 L/mol at STP." % (g, Mx),
       "This treats grams as moles. Convert to moles with the molar mass first.",
       "This divides grams by 22.4 and never uses the molar mass.",
       "This finds the moles and then divides by 22.4; moles times 22.4 L/mol gives liters."],
      "Our goal is the mole: g &rarr; mol &rarr; L.",
      "%s g &divide; %s g/mol = %s mol; &times; 22.4 L/mol = <b>%s</b>." % (g, Mx, num(D(g) / Mx, 4), S(v, 3, 'L')), 2, 1)

    Q(T, "A student uses 22.4 L/mol to find the volume of 1.00 mol of gas at 37 °C and 1 atm. How does the student's answer compare with the true volume?",
      ["It is too small, because a gas at 37 °C occupies more than 22.4 L per mole.",
       "It is too large, because a gas at 37 °C occupies less than 22.4 L per mole.",
       "It is correct, because 22.4 L/mol works for any gas.",
       "It is correct, because the pressure is 1 atm."],
      ["22.4 L/mol is the molar volume at 0 °C (273 K). At 37 °C the gas is warmer, so by Charles's law it takes up more room (about 25.5 L).",
       "Warming a gas at constant pressure makes its volume larger, not smaller.",
       "22.4 L/mol is the same for every ideal gas, but only at STP.",
       "STP needs both 1 atm and 0 °C; the temperature here is 37 °C."],
      "STP is 0 °C and 1 atm. Is 37 °C warmer or colder?",
      "At 37 °C, 1 mol occupies about 25.5 L, so 22.4 L is <b>too small</b>.", 3)

    m, V, P, C = '1.45', '0.825', '1.05', '27.5'; nm = D(P) * D(V) / (R * TK(C)); v = D(m) / nm; n = ns(m, V, P, sfT(C))
    Q(T, "A %s g sample of an unknown gas occupies %s L at %s atm and %s °C. What is its molar mass?" % (m, V, P, C),
      [S(v, n, 'g/mol'), S(D(m) / (D(P) * D(V) / (R * D(C))), n, 'g/mol'), S(nm / D(m), n, 'g/mol'), S(D(m) / D(V), n, 'g/mol')],
      ["Find n = PV/RT, then M = m/n.",
       "This uses %s °C in PV = nRT; convert to kelvins." % C,
       "This divides moles by grams. Molar mass is grams per mole: M = m/n.",
       "This is the density, mass divided by volume (g/L), not the molar mass."],
      "Molar mass = grams &divide; moles; get the moles from PV = nRT.",
      "%s. n = (%s)(%s) / [(0.082058)(%s)] = %s mol; M = %s g &divide; %s mol = <b>%s</b>." % (kt(C), P, V, TKs(C), num(nm, 4), m, num(nm, 4), S(v, n, 'g/mol')), 3, 1)

    m, V = '0.842', '625'; v = D(m) / (D(V) / 1000); n = ns(m, V)
    Q(T, "A %s g sample of a gas fills a %s mL flask. What is the density of the gas in g/L?" % (m, V),
      [S(v, n, 'g/L'), S(D(m) / D(V), n, 'g/L'), S(D(V) / 1000 / D(m), n, 'g/L'), S(D(m) * D(V) / 1000, n, 'g/L')],
      ["d = m/V with V in liters: %s mL = 0.%s L." % (V, V),
       "This divides by %s mL; convert to liters to get g/L." % V,
       "This is V/m; density is mass divided by volume.",
       "This multiplies mass and volume; density is mass divided by volume."],
      "d = m/V, with V in liters.",
      "d = %s g &divide; 0.%s L = <b>%s</b>." % (m, V, S(v, n, 'g/L')), 1, 1)

    Q(T, "Which problem is solved most directly with PV = nRT rather than the combined gas law?",
      ["Finding how many moles of oxygen are in a tank of known volume, pressure, and temperature",
       "Finding the new volume of a balloon after it is warmed and rises to a lower pressure",
       "Finding the new pressure in a rigid can after it is heated",
       "Finding the new volume of a gas after it is compressed at constant temperature"],
      ["There is one set of conditions and you need the moles, so use PV = nRT.",
       "This is a before-and-after change in P, V, and T: the combined gas law, with no need for R.",
       "A before-and-after change at constant volume: Gay-Lussac's law (part of the combined gas law).",
       "A before-and-after change at constant temperature: Boyle's law."],
      "Is the gas changing? Before-and-after means combined gas law; one set of conditions means PV = nRT.",
      "One set of conditions and an unknown amount: <b>finding moles in a tank</b> uses PV = nRT.", 2)

    # ======================= ch10-stoich (11) =======================
    T = 'ch10-stoich'
    g = '8.50'; Mx = mm('H2O2'); nH = D(g) / Mx; v = nH / 2 * VM
    Q(T, "Hydrogen peroxide decomposes: [[2 H2O2(aq) -> 2 H2O(l) + O2(g)]]. What volume of {O2} at STP forms from %s g of {H2O2} (%s g/mol)?" % (g, Mx),
      [S(v, 3, 'L'), S(nH * VM, 3, 'L'), S(nH * 2 * VM, 3, 'L'), S(D(g) / 2 * VM, 3, 'L')],
      ["g &rarr; mol {H2O2} &rarr; &times; (1 mol {O2} / 2 mol {H2O2}) &rarr; &times; 22.4 L/mol.",
       "This skips the mole ratio; 2 mol {H2O2} give only 1 mol {O2}.",
       "This flips the mole ratio (2/1 instead of 1/2).",
       "This uses grams of {H2O2} as if they were moles."],
      "g &rarr; mol &rarr; mole ratio &rarr; L at STP.",
      "%s g &divide; %s g/mol = %s mol {H2O2}; &times; &frac12; = %s mol {O2}; &times; 22.4 L/mol = <b>%s</b>." % (g, Mx, num(nH, 4), num(nH / 2, 4), S(v, 3, 'L')), 2, 1)

    L = '6.72'; Mx = mm('NH3'); nN = D(L) / VM; v = nN * 2 * Mx
    Q(T, "In the reaction [[N2(g) + 3 H2(g) -> 2 NH3(g)]], what mass of ammonia ({NH3}, %s g/mol) forms from %s L of {N2} at STP with excess {H2}?" % (Mx, L),
      [S(v, 3, 'g'), S(nN * Mx, 3, 'g'), S(nN / 2 * Mx, 3, 'g'), S(D(L) * 2 * Mx, 3, 'g')],
      ["L {N2} &divide; 22.4 L/mol &rarr; &times; (2 mol {NH3} / 1 mol {N2}) &rarr; &times; %s g/mol." % Mx,
       "This skips the mole ratio; each mole of {N2} makes 2 mol {NH3}.",
       "This flips the mole ratio (1/2 instead of 2/1).",
       "This treats liters as moles; divide by 22.4 L/mol first."],
      "At STP, liters &divide; 22.4 = moles.",
      "%s L &divide; 22.4 L/mol = %s mol {N2}; &times; 2 = %s mol {NH3}; &times; %s g/mol = <b>%s</b>." % (L, num(nN, 4), num(nN * 2, 4), Mx, S(v, 3, 'g')), 2, 1)

    g, P, C = '3.65', '0.975', '27.5'; Mx = mm('C3H8'); np_ = D(g) / Mx; nc = np_ * 3; v = nc * R * TK(C) / D(P); n = ns(g, P, sfT(C))
    Q(T, "Propane burns in a camp stove: [[C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(g)]]. What volume of {CO2} at %s atm and %s °C forms from %s g of {C3H8} (%s g/mol)?" % (P, C, g, Mx),
      [S(v, n, 'L'), S(nc * VM, n, 'L'), S(np_ * R * TK(C) / D(P), n, 'L'), S(nc * R * D(C) / D(P), n, 'L')],
      ["g &rarr; mol {C3H8} &rarr; &times; 3 &rarr; V = nRT/P with T in kelvins.",
       "This uses 22.4 L/mol, which is only for STP. These conditions are not STP, so use V = nRT/P.",
       "This skips the mole ratio and finds the volume of the propane's moles; each mole of propane makes 3 mol {CO2}.",
       "This uses the Celsius temperature in V = nRT/P."],
      "Not at STP: after the mole ratio, use V = nRT/P.",
      "%s g &divide; %s = %s mol {C3H8}; &times; 3 = %s mol {CO2}. %s. V = (%s)(0.082058)(%s) / %s = <b>%s</b>." % (g, Mx, num(np_, 4), num(nc, 4), kt(C), num(nc, 4), TKs(C), P, S(v, n, 'L')), 3, 1)

    L, P, C = '0.385', '0.982', '23.5'; Mx = D(MS['Zn']); nh = D(P) * D(L) / (R * TK(C)); v = nh * Mx; n = ns(L, P, sfT(C))
    Q(T, "Zinc reacts with hydrochloric acid: [[Zn(s) + 2 HCl(aq) -> ZnCl2(aq) + H2(g)]]. What mass of zinc (%s g/mol) is needed to make %s L of {H2} at %s atm and %s °C?" % (Mx, L, P, C),
      [S(v, n, 'g'), S(D(P) * D(L) / (R * D(C)) * Mx, n, 'g'), S(D(L) / VM * Mx, n, 'g'), S(nh * 2 * Mx, n, 'g')],
      ["n {H2} = PV/RT; 1 mol Zn per mol {H2}; &times; %s g/mol." % Mx,
       "This uses the Celsius temperature in n = PV/RT.",
       "This uses 22.4 L/mol, but the gas is not at STP.",
       "This uses the 2 : 1 ratio of HCl to {H2}. Zinc and {H2} are 1 : 1."],
      "L of gas &rarr; mol (PV = nRT) &rarr; mole ratio &rarr; g.",
      "%s. n = (%s)(%s) / [(0.082058)(%s)] = %s mol {H2} = mol Zn; &times; %s g/mol = <b>%s</b>." % (kt(C), P, L, TKs(C), num(nh, 4), Mx, S(v, n, 'g')), 3, 1)

    L = '3.20'; v = D(L) * 6 / 2
    Q(T, "Ethane burns: [[2 C2H6(g) + 7 O2(g) -> 4 CO2(g) + 6 H2O(g)]]. What volume of water vapor forms when %s L of {C2H6} burns, with both gases measured at the same temperature and pressure?" % L,
      [S(v, 3, 'L'), S(D(L) * 2 / 6, 3, 'L'), L + ' L', S(D(L) * 6, 3, 'L')],
      ["Same T and P, so coefficients are volume ratios: %s L &times; (6 L {H2O} / 2 L {C2H6})." % L,
       "This flips the ratio (2/6 instead of 6/2).",
       "This assumes a 1 : 1 ratio; the coefficients are 2 {C2H6} : 6 {H2O}.",
       "This multiplies by 6 but forgets to divide by the 2 in front of {C2H6}."],
      "Same T and P: liters behave like moles.",
      "%s L &times; 6/2 = <b>%s</b>." % (L, S(v, 3, 'L')), 2, 1)

    Q(T, "For [[2 H2(g) + O2(g) -> 2 H2O(l)]], a student says, &ldquo;4.0 L of {H2} makes 4.0 L of water, because the coefficients are 2 : 2.&rdquo; What is wrong?",
      ["Volume ratios apply only to gases; the water here is a liquid.",
       "Nothing; coefficients always give volume ratios.",
       "The ratio should be 2 : 1, so 4.0 L of {H2} makes 2.0 L of water.",
       "Volume ratios apply only at STP."],
      ["Equal volumes contain equal moles only for gases at the same T and P. Liquid water's volume is set by its density, not by Avogadro's law.",
       "Coefficients give volume ratios only for gases at the same temperature and pressure.",
       "The 2 : 2 mole ratio is right; the problem is that water is a liquid, so moles do not convert to liters this way.",
       "Volume ratios work at any temperature and pressure, as long as all the gases are at the same conditions."],
      "Look at the state symbol for water.",
      "Volume ratios come from Avogadro's law, which is about gases: <b>liquid water does not follow it</b>.", 2)

    g, P, C = '4.25', '1.02', '22.5'; Mx = mm('KClO3'); nk = D(g) / Mx; no = nk * 3 / 2; v = no * R * TK(C) / D(P); n = ns(g, P, sfT(C))
    Q(T, "Heating potassium chlorate releases oxygen: [[2 KClO3(s) -> 2 KCl(s) + 3 O2(g)]]. What volume of {O2} at %s atm and %s °C forms from %s g of {KClO3} (%s g/mol)?" % (P, C, g, Mx),
      [S(v, n, 'L'), S(nk * R * TK(C) / D(P), n, 'L'), S(nk * 2 / 3 * R * TK(C) / D(P), n, 'L'), S(no * R * D(C) / D(P), n, 'L')],
      ["g &rarr; mol {KClO3} &rarr; &times; 3/2 &rarr; V = nRT/P.",
       "This skips the mole ratio; 2 mol {KClO3} release 3 mol {O2}.",
       "This flips the mole ratio (2/3 instead of 3/2).",
       "This uses the Celsius temperature."],
      "Mole ratio first, then V = nRT/P with kelvins.",
      "%s g &divide; %s = %s mol; &times; 3/2 = %s mol {O2}. %s. V = <b>%s</b>." % (g, Mx, num(nk, 4), num(no, 4), kt(C), S(v, n, 'L')), 3, 1)

    g = '15.5'; Mx = mm('C6H12O6'); ng = D(g) / Mx; v = ng * 2 * VM
    Q(T, "Yeast ferments glucose: [[C6H12O6(aq) -> 2 C2H5OH(aq) + 2 CO2(g)]]. What volume of {CO2}, measured at STP, comes from %s g of glucose (%s g/mol)?" % (g, Mx),
      [S(v, 3, 'L'), S(ng * VM, 3, 'L'), S(D(g) * 2 * VM, 3, 'L'), S(ng * 2 / VM, 3, 'L')],
      ["g &rarr; mol glucose &rarr; &times; 2 &rarr; &times; 22.4 L/mol.",
       "This skips the mole ratio; each glucose makes 2 {CO2}.",
       "This uses grams of glucose as if they were moles.",
       "This divides the moles of {CO2} by 22.4; multiply by 22.4 L/mol to get liters."],
      "g &rarr; mol &rarr; mole ratio &rarr; L at STP.",
      "%s &divide; %s = %s mol; &times; 2 = %s mol {CO2}; &times; 22.4 = <b>%s</b>." % (g, Mx, num(ng, 4), num(ng * 2, 4), S(v, 3, 'L')), 2, 1)

    L = '0.575'; v = D(L) / 2
    Q(T, "Hot nitrous oxide decomposes: [[2 N2O(g) -> 2 N2(g) + O2(g)]]. What volume of {O2} forms from %s L of {N2O}, with both gases measured at the same temperature and pressure?" % L,
      [S(v, 3, 'L'), S(D(L) * 2, 3, 'L'), L + ' L', S(D(L) / VM / 2, 3, 'L')],
      ["Both are gases at the same T and P: %s L {N2O} &times; (1 L {O2} / 2 L {N2O})." % L,
       "This flips the ratio; 2 volumes of {N2O} give only 1 volume of {O2}.",
       "This assumes a 1 : 1 ratio; the coefficients are 2 : 1.",
       "This converts to moles with 22.4 L/mol and stops there; the number is moles of {O2}, not liters."],
      "Same T and P: use the coefficients as a volume ratio.",
      "%s L &times; 1/2 = <b>%s</b>." % (L, S(v, 3, 'L')), 1, 1)

    g, P, C = '0.750', '0.988', '37.0'; Mx = mm('CaCO3'); nc = D(g) / Mx; v = nc * R * TK(C) / D(P); n = ns(g, P, sfT(C))
    Q(T, "An antacid tablet neutralizes stomach acid: [[CaCO3(s) + 2 HCl(aq) -> CaCl2(aq) + H2O(l) + CO2(g)]]. What volume of {CO2} at %s atm and %s °C forms from %s g of {CaCO3} (%s g/mol)?" % (P, C, g, Mx),
      [S(v, n, 'L'), S(nc * VM, n, 'L'), S(nc * R * D(C) / D(P), n, 'L'), S(nc * 2 * R * TK(C) / D(P), n, 'L')],
      ["mol {CaCO3} = mol {CO2} (1 : 1); V = nRT/P at body temperature.",
       "This uses 22.4 L/mol, but 37.0 °C is not STP.",
       "This uses the Celsius temperature.",
       "This uses the 2 from HCl; {CaCO3} and {CO2} are 1 : 1."],
      "g &rarr; mol &rarr; 1 : 1 &rarr; V = nRT/P.",
      "%s &divide; %s = %s mol {CO2}. %s. V = (%s)(0.082058)(%s) / %s = <b>%s</b>." % (g, Mx, num(nc, 4), kt(C), num(nc, 4), TKs(C), P, S(v, n, 'L')), 3, 1)

    L, P, C = '5.35', '1.10', '19.5'; Mx = mm('CH4'); no = D(P) * D(L) / (R * TK(C)); v = no / 2 * Mx; n = ns(L, P, sfT(C))
    Q(T, "Methane burns: [[CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(g)]]. What mass of {CH4} (%s g/mol) uses up %s L of {O2} measured at %s atm and %s °C?" % (Mx, L, P, C),
      [S(v, n, 'g'), S(no * Mx, n, 'g'), S(no * 2 * Mx, n, 'g'), S(D(L) / VM / 2 * Mx, n, 'g')],
      ["n {O2} = PV/RT; &times; (1 mol {CH4} / 2 mol {O2}); &times; %s g/mol." % Mx,
       "This skips the mole ratio; 2 mol {O2} burn each mole of {CH4}.",
       "This flips the mole ratio (2/1 instead of 1/2).",
       "This uses 22.4 L/mol, but the {O2} is not at STP."],
      "L {O2} &rarr; mol (PV = nRT) &rarr; mole ratio &rarr; g {CH4}.",
      "%s. n {O2} = (%s)(%s) / [(0.082058)(%s)] = %s mol; &divide; 2 = %s mol {CH4}; &times; %s = <b>%s</b>." % (kt(C), P, L, TKs(C), num(no, 4), num(no / 2, 4), Mx, S(v, n, 'g')), 3, 1)

    # ======================= ch10-dalton (12) =======================
    T = 'ch10-dalton'
    a, b = '6.82', '13.9'; v = addp(a, b)
    Q(T, "A scuba tank holds a nitrox mixture in which the partial pressure of {O2} is %s atm and that of {N2} is %s atm. What is the total pressure?" % (a, b),
      [v + ' atm', addp(b, '-' + a) + ' atm', qd((D(a) + D(b)) / 2, 1) + ' atm', format(D(a) + D(b), 'f') + ' atm'],
      ["Dalton's law: P<sub>total</sub> = %s + %s, rounded to the tenths place like %s." % (a, b, b),
       "This subtracts the partial pressures; Dalton's law adds them.",
       "This averages the partial pressures; the total is their sum.",
       "This is the sum, but it keeps two decimal places; %s atm is known only to the tenths place." % b],
      "P<sub>total</sub> = P<sub>1</sub> + P<sub>2</sub>.",
      "%s + %s = <b>%s atm</b>." % (a, b, v), 1, 1)

    tot, he = '2.65', '1.95'; v = addp(tot, '-' + he)
    Q(T, "A tank contains only helium and oxygen at a total pressure of %s atm. The partial pressure of helium is %s atm. What is the partial pressure of oxygen?" % (tot, he),
      [v + ' atm', addp(tot, he) + ' atm', num(D(he) / D(tot), 3) + ' atm', num(D(tot) / 2, 3) + ' atm'],
      ["P<sub>O2</sub> = P<sub>total</sub> &minus; P<sub>He</sub> = %s &minus; %s, to the hundredths place." % (tot, he),
       "This adds the pressures; the total already includes helium, so subtract.",
       "This divides the helium pressure by the total, which gives helium's mole fraction, not a pressure.",
       "This is half of the total; the gases do not share the pressure equally."],
      "The partial pressures must add up to the total.",
      "%s &minus; %s = <b>%s atm</b>." % (tot, he, v), 1, 1)

    a, b, c = '0.385', '0.125', '0.0400'; tot = addp(a, b, c); v = D(b) / D(tot); n = ns(b, tot)
    Q(T, "A gas mixture contains %s mol {N2}, %s mol {O2}, and %s mol {CO2}. What is the mole fraction of {O2}?" % (a, b, c),
      [num(v, n), b, num(D(b) / D(a), n), num(D(tot) / D(b), n)],
      ["X<sub>O2</sub> = n<sub>O2</sub>/n<sub>total</sub> = %s / %s." % (b, tot),
       "This is the moles of {O2}, not its fraction of the total moles.",
       "This divides by the moles of {N2} only; divide by the total moles of all three gases.",
       "This is n<sub>total</sub>/n<sub>O2</sub>, upside down; a mole fraction is never greater than 1."],
      "Add all the moles first.",
      "n<sub>total</sub> = %s mol; X<sub>O2</sub> = %s / %s = <b>%s</b>." % (tot, b, tot, num(v, n)), 2, 1)

    X_, Pt = '0.650', '1.02'; v = D(X_) * D(Pt); n = ns(X_, Pt)
    Q(T, "During dental sedation, a nitrous oxide&ndash;oxygen mixture is delivered at a total pressure of %s atm. The mole fraction of {N2O} is %s. What is the partial pressure of {N2O}?" % (Pt, X_),
      [S(v, n, 'atm'), S(D(X_) / D(Pt), n, 'atm'), S(D(Pt) / D(X_), n, 'atm'), S((1 - D(X_)) * D(Pt), n, 'atm')],
      ["P<sub>N2O</sub> = X<sub>N2O</sub> &times; P<sub>total</sub>.",
       "This divides the mole fraction by the total pressure; multiply them.",
       "This divides the total by the mole fraction, which gives a partial pressure larger than the total.",
       "This uses 1 &minus; %s, the mole fraction of {O2}; it is the oxygen's partial pressure." % X_],
      "P<sub>i</sub> = X<sub>i</sub> &times; P<sub>total</sub>.",
      "%s &times; %s atm = <b>%s</b>." % (X_, Pt, S(v, n, 'atm')), 2, 1)

    pc, Pt = '78.1', '749'; v = D(pc) / 100 * D(Pt); n = ns(pc, Pt)
    Q(T, "Dry air is %s%% {N2} by moles. What is the partial pressure of {N2} when the barometer reads %s mmHg?" % (pc, Pt),
      [S(v, n, 'mmHg'), S(D(pc) * D(Pt), n, 'mmHg'), S(D(Pt) / (D(pc) / 100), n, 'mmHg'), addp(Pt, '-' + pc) + ' mmHg'],
      ["X<sub>N2</sub> = %s%% &divide; 100 = 0.%s; P<sub>N2</sub> = 0.%s &times; %s mmHg." % (pc, pc.replace('.', ''), pc.replace('.', ''), Pt),
       "This uses %s as the mole fraction without dividing by 100; a partial pressure cannot exceed the total." % pc,
       "This divides by the mole fraction; multiply by it.",
       "This subtracts the percent from the pressure; percent and pressure are different quantities. Multiply by the mole fraction."],
      "A percent by moles divided by 100 is a mole fraction.",
      "P<sub>N2</sub> = 0.%s &times; %s mmHg = <b>%s</b>." % (pc.replace('.', ''), Pt, S(v, n, 'mmHg')), 2, 1)

    he, ox, Pt = '4.45', '1.15', '165'; tot = addp(he, ox); v = D(ox) / D(tot) * D(Pt); n = ns(ox, tot, Pt)
    Q(T, "A diving cylinder holds %s mol of helium and %s mol of oxygen at a total pressure of %s atm. What is the partial pressure of oxygen?" % (he, ox, Pt),
      [S(v, n, 'atm'), S(D(ox) / D(he) * D(Pt), n, 'atm'), S(D(he) / D(tot) * D(Pt), n, 'atm'), S(D(ox) * D(Pt), n, 'atm')],
      ["X<sub>O2</sub> = %s / %s; P<sub>O2</sub> = X<sub>O2</sub> &times; %s atm." % (ox, tot, Pt),
       "This divides by the moles of helium only; the mole fraction uses the total moles.",
       "This is the partial pressure of helium.",
       "This multiplies the moles by the total pressure; use the mole fraction, not the moles."],
      "Mole fraction first, then P<sub>i</sub> = X<sub>i</sub>P<sub>total</sub>.",
      "n<sub>total</sub> = %s mol; X<sub>O2</sub> = %s; P<sub>O2</sub> = %s &times; %s = <b>%s</b>." % (tot, num(D(ox) / D(tot), 4), num(D(ox) / D(tot), 4), Pt, S(v, n, 'atm')), 2, 1)

    Pa, C = '751', '30.0'; v = addp(Pa, '-' + VP[C])
    Q(T, "A student collects oxygen over water at %s °C when the room pressure is %s mmHg. Use the table. What is the partial pressure of the oxygen?" % (C, Pa),
      [v + ' mmHg', addp(Pa, '-' + VP['25.0']) + ' mmHg', addp(Pa, VP[C]) + ' mmHg', Pa + ' mmHg'],
      ["P<sub>O2</sub> = P<sub>atm</sub> &minus; P<sub>H2O</sub> = %s &minus; %s, to the ones place like %s." % (Pa, VP[C], Pa),
       "This subtracts the vapor pressure at 25.0 °C. Use the value at the water's temperature, %s °C." % C,
       "This adds the water vapor; the room pressure already includes it, so subtract.",
       "This forgets the water vapor; the gas in the tube is a mixture of oxygen and water vapor."],
      "Find water's vapor pressure at %s °C in the table and subtract it." % C,
      "%s &minus; %s = <b>%s mmHg</b>." % (Pa, VP[C], v), 2, 1,
      [{"type": "table", "cap": "Vapor pressure of water", "head": ["Temperature (°C)", "Vapor pressure (mmHg)"],
        "rows": [["20.0", "17.5"], ["25.0", "23.8"], ["30.0", "31.8"], ["37.0", "47.1"]]}])

    V, C, Pa = '48.5', '20.0', '746'; pw = VP[C]; Po = D(Pa) - D(pw); Ps = addp(Pa, '-' + pw)
    v = Po / ATM_MM * D(V) / 1000 / (R * TK(C)); n = ns(V, Ps, sfT(C))
    Q(T, "A student collects %s mL of oxygen over water at %s °C. The room pressure is %s mmHg, and water's vapor pressure at %s °C is %s mmHg. How many moles of {O2} were collected?" % (V, C, Pa, C, pw),
      [S(v, n, 'mol'), S(D(Pa) / ATM_MM * D(V) / 1000 / (R * TK(C)), n, 'mol'), S(Po * D(V) / 1000 / (R * TK(C)), n, 'mol'), S((D(Pa) + D(pw)) / ATM_MM * D(V) / 1000 / (R * TK(C)), n, 'mol')],
      ["P<sub>O2</sub> = %s &minus; %s = %s mmHg = %s atm; V = 0.0%s L; n = PV/RT." % (Pa, pw, Ps, num(D(Ps) / ATM_MM, 4), V.replace('.', '')),
       "This uses the room pressure; subtract water's vapor pressure first, because only part of the pressure belongs to the {O2}.",
       "This uses mmHg with R = 0.082058, so the answer is 760 times too large.",
       "This adds the water vapor pressure; it should be subtracted."],
      "Dry gas pressure first, then convert units to match R.",
      "P<sub>O2</sub> = %s mmHg = %s atm; %s. n = (%s)(0.0%s) / [(0.082058)(%s)] = <b>%s</b>." % (Ps, num(D(Ps) / ATM_MM, 4), kt(C), num(D(Ps) / ATM_MM, 4), V.replace('.', ''), TKs(C), S(v, n, 'mol')), 3, 1)

    pc, Pt = '20.95', '438'; v = D(pc) / 100 * D(Pt); n = ns(pc, Pt)
    Q(T, "On the summit of Mount Whitney the air pressure is about %s mmHg. Use the composition of dry air in the table. What is the partial pressure of oxygen on the summit?" % Pt,
      [S(v, n, 'mmHg'), S(D(pc) * D(Pt), n, 'mmHg'), S(D(pc) / 100 * 760, n, 'mmHg'), S(D(Pt) / (D(pc) / 100), n, 'mmHg')],
      ["The percentage of {O2} is the same at altitude; only the total pressure drops. P<sub>O2</sub> = 0.2095 &times; %s mmHg." % Pt,
       "This uses 20.95 without dividing by 100.",
       "This uses sea-level pressure, 760 mmHg. On the summit the total pressure is %s mmHg." % Pt,
       "This divides by the mole fraction; multiply by it."],
      "P<sub>O2</sub> = X<sub>O2</sub> &times; P<sub>total</sub>; X = percent &divide; 100.",
      "0.2095 &times; %s mmHg = <b>%s</b>, much lower than at sea level, which is why breathing is harder at altitude." % (Pt, S(v, n, 'mmHg')), 2, 1,
      [{"type": "table", "cap": "Composition of dry air (by moles)", "head": ["Gas", "Percent"],
        "rows": [["{N2}", "78.08%"], ["{O2}", "20.95%"], ["Ar", "0.93%"]]}])

    Q(T, "Why must water's vapor pressure be subtracted from the room pressure when a gas is collected over water?",
      ["The gas in the tube is a mixture of the collected gas and water vapor, and together they balance the room pressure.",
       "Water vapor is heavier than the collected gas, so it pushes down on the tube.",
       "The water absorbs some of the gas, lowering its pressure.",
       "The room pressure must be converted to the pressure of liquid water."],
      ["Water evaporates into the tube, so P<sub>atm</sub> = P<sub>gas</sub> + P<sub>H2O</sub>; subtracting gives the dry gas pressure.",
       "Weight is not the reason; each gas in a mixture contributes its own partial pressure.",
       "The correction is for water vapor added to the gas, not gas lost into the water.",
       "Liquid water does not have a 'pressure' to convert to; its vapor contributes a partial pressure."],
      "What else, besides the collected gas, is in the tube?",
      "The tube holds <b>gas plus water vapor</b>; Dalton's law says their pressures add to P<sub>atm</sub>.", 1)

    Q(T, "Helium is pumped into a rigid tank that already contains oxygen, at constant temperature. What happens to the partial pressure of the oxygen?",
      ["It stays the same, while the total pressure increases.", "It decreases, because the helium pushes the oxygen aside.",
       "It increases, because the total pressure increases.", "It decreases, because the mole fraction of oxygen decreases while the total pressure stays the same."],
      ["The same oxygen molecules still hit the walls just as often; each gas acts as if the others were not there.",
       "Gas particles in KMT do not push each other aside; oxygen's pressure depends only on its own moles, V, and T.",
       "The total rises because helium adds its own partial pressure; oxygen's share in pressure units does not change.",
       "Oxygen's mole fraction does fall, but the total pressure rises by just enough that X &times; P<sub>total</sub> stays the same."],
      "Each gas behaves as if it were alone in the tank.",
      "Oxygen's moles, V, and T are unchanged, so <b>its partial pressure stays the same</b>; the total rises.", 2)

    X_, Pa = '0.285', '758'; pw = VP['37.0']; Pd = D(Pa) - D(pw); Ps = addp(Pa, '-' + pw); v = D(X_) * Pd; n = ns(X_, Ps)
    Q(T, "Mateo Herrera, who has asthma, is on supplemental oxygen, and the air he breathes in has an {O2} mole fraction of about %s. In his airways it is warmed to 37.0 °C and saturated with water vapor (%s mmHg). If the air pressure is %s mmHg, what is the partial pressure of {O2} in the humidified air?" % (X_, pw, Pa),
      [S(v, n, 'mmHg'), S(D(X_) * D(Pa), n, 'mmHg'), S(D(X_) * (D(Pa) + D(pw)), n, 'mmHg'), S((1 - D(X_)) * Pd, n, 'mmHg')],
      ["Water vapor takes %s mmHg of the total, leaving %s mmHg for the other gases; P<sub>O2</sub> = %s &times; %s. (Context only.)" % (pw, Ps, X_, Ps),
       "This forgets the water vapor. Humidified air in the airways includes water vapor at 47.1 mmHg.",
       "This adds the water vapor instead of subtracting it.",
       "This uses 1 &minus; %s, the share of the other gases, not oxygen's share." % X_],
      "Subtract water vapor first, then multiply by the mole fraction.",
      "%s &minus; %s = %s mmHg; %s &times; %s = <b>%s</b>." % (Pa, pw, Ps, X_, Ps, S(v, n, 'mmHg')), 3, 1)


if __name__ == '__main__':
    build()
    dump(sys.argv[1])
