#!/usr/bin/env python3
"""Builds bank/ch11.json (Chapter 11 Try It items: how solutions form, temperature/pressure and solubility,
concentration, molarity and dilution, solution stoichiometry and titration, molality and colligative properties).
Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch11.py bank/ch11.json
Conventions (Chapter 11 text): %(m/m) = g solute / g solution x 100%; %(m/v) = g solute / mL solution x 100%;
%(v/v) = mL solute / mL solution x 100%; in dilute water 1 ppm = 1 mg/L, 1 ppb = 1 ug/L, 1 ppt = 1 ng/L;
M = mol solute / L solution; M1V1 = M2V2 with matching units (1 M = 1000 mM), V2 = total final volume; titration
endpoint with phenolphthalein, volume used = final - initial buret reading; molality m = mol solute / kg solvent;
complete dissociation i (NaCl 2, KBr 2, CaCl2 3, MgCl2 3, Na2SO4 3, AlCl3 4, nonelectrolytes 1); osmolality = i x m;
serum 275-295 mOsm/kg; dTf = i Kf m (Kf 1.86 C/m), dTb = i Kb m (Kb 0.512 C/m); Henry's law S1/P1 = S2/P2.
Molar masses from tools/yellow_sheet_masses.json (addition rule). Sig figs from the givens; no trailing-zero givens
without a decimal point in calculation stems; round half up.
Markup: {CaCl2} formula, [[2 KI(aq) + Pb(NO3)2(aq) -> PbI2(s) + 2 KNO3(aq)]] equation.
The helpers are imported by tools/gen_adapt_ch11.py. Every number is recomputed independently by
tools/check_bank_ch11.py."""
import json, sys, re, os, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
HERE = os.path.dirname(os.path.abspath(__file__))
MS = json.load(open(os.path.join(HERE, 'yellow_sheet_masses.json')))['masses']
M = '&minus;'
B = []
CFG = {'prefix': 'c11-%03d', 'adapt': False}

# ---------------- formulas and equations ----------------
def F(s):
    return re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', s)
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
def MMs(f): return str(mm(f))

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
def P(v, n): return num(v, n) + '%'
def addp(*s):
    """sum of strings (use '-x' to subtract), decimal-place rule; returns string."""
    d = min(dp(x) for x in s); r = qd(sum(D(x) for x in s), d)
    return r + '.' if d == 0 and r.endswith('0') else r
def ns(*a):
    """fewest significant figures among strings (as written) and ints."""
    return min(x if isinstance(x, int) else sfs(x) for x in a)
def L(mL): return D(mL) / 1000
def Ls(mL): return num(L(mL), sfs(mL))          # liters as written, same sig figs
KF, KB = D('1.86'), D('0.512')
def tf(dT):
    """freezing point string from an exact dT: 0.00 - dT rounded by the decimal-place rule after dT is rounded to 3 s.f."""
    d = D(num(dT, 3)); return qd(D('0.00') - dT, max(0, min(2, dp(str(d)))))
def tb(dT):
    d = D(num(dT, 3)); return qd(D('100.00') + dT, max(0, min(2, dp(str(d)))))

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
    # ======================= ch11-dissolve (10) =======================
    T = 'ch11-dissolve'
    Q(T, "A hand sanitizer gel is 62% ethanol and 38% water by volume. Which component is the solvent?",
      ["Ethanol, because it is present in the larger amount", "Water, because water is always the solvent",
       "The gelling agent, because it holds the mixture together", "Neither; a gel cannot contain a solution"],
      ["The solvent is the component present in the larger amount: 62% ethanol compared with 38% water.",
       "Water is the most common solvent, but here there is less water (38%) than ethanol (62%).",
       "The gelling agent is a small additive; the solvent is the component present in the largest amount.",
       "The liquid in the gel is a homogeneous mixture of ethanol and water, which is a solution."],
      "The solvent is whichever component there is more of.",
      "62% is more than 38%, so <b>ethanol is the solvent</b> and water is the solute.", 1)

    Q(T, "Which substance is most soluble in water?",
      ["Urea, {CH4N2O}, which has N&ndash;H groups and an oxygen atom", "Pentane, {C5H12}", "Carbon disulfide, {CS2}", "Nitrogen, {N2}"],
      ["Urea's N&ndash;H groups and its oxygen hydrogen bond with water; urea is so soluble that the kidneys excrete it dissolved in urine.",
       "Pentane contains only C and H, so it has only dispersion forces and stays out of water.",
       "{CS2} is a linear, symmetric molecule with nonpolar C&ndash;S bonds, so it cannot form strong attractions with water.",
       "{N2} is nonpolar (two identical atoms), so only a little dissolves in water."],
      "Look for the solute that can hydrogen bond with water.",
      "Urea hydrogen bonds with water: <b>urea</b> is the most soluble (like dissolves like).", 1)

    Q(T, "Which pair of liquids is <b>immiscible</b> (forms two layers)?",
      ["Water and hexane ({C6H14})", "Water and ethanol ({C2H5OH})", "Water and acetone ({C3H6O})", "Hexane and octane ({C8H18})"],
      ["Water is polar and hydrogen bonded; hexane is nonpolar. Unlike substances separate into layers.",
       "Ethanol's O&ndash;H group hydrogen bonds with water, so the two are miscible.",
       "Acetone is polar and accepts hydrogen bonds from water, so the two mix in all proportions.",
       "Both are nonpolar hydrocarbons with dispersion forces only; like dissolves like, so they mix."],
      "Immiscible liquids are unlike: one polar, one nonpolar.",
      "Polar water and nonpolar hexane do not mix: <b>water and hexane</b>.", 1)

    Q(T, "When NaCl dissolves in water, how are the water molecules arranged around the ions?",
      ["The &delta;&minus; oxygen ends face Na<sup>+</sup>, and the &delta;+ hydrogen ends face Cl<sup>&minus;</sup>.",
       "The &delta;+ hydrogen ends face Na<sup>+</sup>, and the &delta;&minus; oxygen ends face Cl<sup>&minus;</sup>.",
       "Water molecules form covalent bonds to Na<sup>+</sup> and Cl<sup>&minus;</sup>.",
       "Water molecules stay away from the ions, because water molecules have no charge."],
      ["Opposite charges attract: the partly negative oxygen faces the cation, and the partly positive hydrogens face the anion. These are ion&ndash;dipole attractions.",
       "This puts like charges together (&delta;+ next to Na<sup>+</sup>), which would repel.",
       "Dissolving makes ion&ndash;dipole attractions, not new covalent bonds.",
       "Water is neutral overall, but it is polar: its partial charges attract the ions."],
      "Which end of a water molecule is partly negative?",
      "Ion&ndash;dipole attractions: <b>oxygen ends toward Na<sup>+</sup>, hydrogen ends toward Cl<sup>&minus;</sup></b>.", 2)

    Q(T, "Which aqueous solution conducts electricity well?",
      ["{NH4Cl}(aq)", "sucrose, {C12H22O11}(aq)", "glycerol, {C3H8O3}(aq)", "acetone, {C3H6O}(aq)"],
      ["{NH4Cl} is a soluble ionic compound; it separates into NH<sub>4</sub><sup>+</sup> and Cl<sup>&minus;</sup> ions, so it is a strong electrolyte.",
       "Sucrose dissolves as whole molecules, so it is a nonelectrolyte.",
       "Glycerol dissolves as whole molecules (hydrogen bonding with water), so it is a nonelectrolyte.",
       "Acetone is a polar molecular compound that dissolves without forming ions, so it is a nonelectrolyte."],
      "A solution conducts only if it contains ions.",
      "Only the ionic compound makes ions: <b>{NH4Cl}(aq)</b> is a strong electrolyte.", 1)

    Q(T, "A glucose solution does not conduct electricity. Why?",
      ["Glucose dissolves as whole molecules, so the solution contains no ions.", "Glucose does not dissolve in water.",
       "Glucose breaks apart into C, H, and O atoms, which are neutral.", "Glucose forms ions, but its ions are too large to move."],
      ["Glucose molecules hydrogen bond with water and stay whole: dissolving does not break covalent bonds.",
       "Glucose is very soluble in water; its many O&ndash;H groups hydrogen bond with water.",
       "Dissolving does not break covalent bonds; the glucose molecules stay whole.",
       "Glucose does not form ions at all; it is a nonelectrolyte."],
      "What would have to be in the solution for it to conduct?",
      "No ions: glucose <b>dissolves as whole molecules</b>, so it is a nonelectrolyte.", 1)

    Q(T, "The solubility of {NH4Cl} is 37.2 g per 100 g of water at 20 °C. A student stirs 30.5 g of {NH4Cl} into 100. g of water at 20 °C, and it all dissolves. How is the solution described?",
      ["Unsaturated", "Saturated", "Supersaturated", "Immiscible"],
      ["30.5 g is less than the 37.2 g that 100 g of water can hold at 20 °C, so more {NH4Cl} could still dissolve.",
       "A saturated solution holds the maximum, 37.2 g here. This one holds less.",
       "A supersaturated solution holds more than the solubility; 30.5 g is less than 37.2 g.",
       "Immiscible describes two liquids that form layers, not a solid dissolved in a liquid."],
      "Compare the amount dissolved with the solubility for the same amount of water and temperature.",
      "30.5 g &lt; 37.2 g per 100 g of water: <b>unsaturated</b>.", 1)

    Q(T, "The solubility of sucrose is 204 g per 100 g of water at 20 °C. A candy maker dissolves 110. g of sucrose in 50.0 g of hot water, then cools it carefully to 20 °C without any crystals forming. How is the solution described at 20 °C?",
      ["Supersaturated", "Unsaturated", "Saturated", "Not a solution, because there is more sugar than water"],
      ["50.0 g of water holds only 204 &times; 50.0/100 = 102 g at 20 °C; 110. g is more than that, held in solution only because it was cooled carefully.",
       "This compares 110. g with 204 g, but 204 g is for 100 g of water. Only 50.0 g of water was used.",
       "A saturated solution holds exactly the maximum, 102 g in 50.0 g of water. This one holds more.",
       "A solution can contain more solute than solvent by mass; the sugar is dissolved, so it is a homogeneous mixture."],
      "Scale the solubility to 50.0 g of water first.",
      "Capacity at 20 °C: 204 g &times; 50.0/100 = 102 g. 110. g &gt; 102 g: <b>supersaturated</b>.", 3)

    Q(T, "A crystal of sugar is dropped into a <b>saturated</b> sugar solution at constant temperature. What happens?",
      ["The crystal stays undissolved, and the amount dissolved does not change.", "The crystal dissolves, because sugar is soluble in water.",
       "Extra sugar crystallizes out of the solution onto the crystal.", "The solution becomes supersaturated."],
      ["A saturated solution already holds the maximum, so added solute stays on the bottom.",
       "That would happen in an unsaturated solution. A saturated one cannot hold any more.",
       "That happens when a seed crystal is added to a <i>supersaturated</i> solution.",
       "Adding solid to a saturated solution does not push more into solution; the extra stays undissolved."],
      "Saturated means the solution holds the maximum.",
      "Saturated: <b>the crystal stays undissolved</b>.", 1)

    Q(T, "Vitamin D is a large molecule made mostly of carbon and hydrogen, with only one O&ndash;H group. Where in the body does it dissolve best?",
      ["In fat (adipose) tissue, because both are mostly nonpolar", "In blood plasma, because plasma is mostly water",
       "In urine, because the kidneys filter it out", "In stomach acid, because acids dissolve all molecules"],
      ["Like dissolves like: a mostly nonpolar vitamin dissolves in nonpolar fats, which is why vitamin D is stored in fatty tissue and the liver.",
       "Plasma is mostly polar water; a mostly nonpolar molecule dissolves poorly in it.",
       "Water-soluble (polar) vitamins are excreted in urine; fat-soluble ones are stored instead.",
       "Stomach acid is mostly water; it does not dissolve nonpolar molecules well."],
      "One O&ndash;H on a big hydrocarbon frame: is the molecule mostly polar or nonpolar?",
      "Mostly nonpolar, so <b>it dissolves in fat</b> (a fat-soluble vitamin).", 2)

    # ======================= ch11-solubility (10) =======================
    T = 'ch11-solubility'
    hi, lo = '55.3', '37.2'; v = addp(hi, '-' + lo)
    Q(T, "Use the table. A saturated solution of {NH4Cl} made with 100. g of water at 60.0 °C is cooled to 20.0 °C. What mass of {NH4Cl} crystallizes?",
      [v + ' g', hi + ' g', lo + ' g', addp(hi, lo) + ' g'],
      ["At 60.0 °C the solution holds %s g; at 20.0 °C only %s g can stay dissolved, so the difference comes out as crystals." % (hi, lo),
       "This is all the {NH4Cl} that was dissolved at 60.0 °C, but %s g of it can stay dissolved at 20.0 °C." % lo,
       "This is the amount that stays dissolved at 20.0 °C, not the amount that crystallizes.",
       "This adds the two solubilities; the amount that comes out is the difference."],
      "Read the solubility at each temperature and subtract.",
      "%s g &minus; %s g = <b>%s g</b> crystallizes." % (hi, lo, v), 2, 1,
      [{"type": "table", "cap": "Solubility of {NH4Cl} in water", "head": ["Temperature (°C)", "Solubility (g per 100 g water)"],
        "rows": [["0.0", "29.4"], ["20.0", "37.2"], ["40.0", "45.8"], ["60.0", "55.3"], ["80.0", "65.6"]]}])

    Q(T, "The graph shows the solubility of {NH4Cl} and NaCl in water. Which statement does it support?",
      ["Warming from 20 °C to 80 °C raises the solubility of {NH4Cl} far more than that of NaCl.",
       "Both salts become less soluble as the temperature rises.",
       "NaCl is more soluble than {NH4Cl} at every temperature shown.",
       "The solubility of NaCl rises more steeply with temperature than that of {NH4Cl}."],
      ["{NH4Cl} rises from about 37 to about 66 g per 100 g of water, while NaCl rises only from about 36 to 38 g.",
       "Both curves slope upward: like most solids, both become more soluble when warmer.",
       "The curves cross between 0 °C and 20 °C; above that crossing, {NH4Cl} is the more soluble salt.",
       "The NaCl curve is nearly flat; the {NH4Cl} curve is the steep one."],
      "Compare how much each curve rises between 20 °C and 80 °C.",
      "{NH4Cl} gains about 28 g per 100 g of water from 20 °C to 80 °C; NaCl gains about 2 g. <b>{NH4Cl} changes far more</b>.", 2, 0,
      [{"type": "plot", "x": {"min": 0, "max": 100, "label": "Temperature (°C)"}, "y": {"min": 20, "max": 80, "label": "g per 100 g water"}, "grid": True,
        "series": [{"pts": [[0, 29.4], [20, 37.2], [40, 45.8], [60, 55.3], [80, 65.6], [100, 77.3]], "label": "NH₄Cl", "dots": True, "labelAt": 4, "dx": -30, "dy": -18},
                   {"pts": [[0, 35.7], [20, 35.9], [40, 36.4], [60, 37.1], [80, 38.0], [100, 39.2]], "label": "NaCl", "dots": True, "labelAt": 4, "dx": 10, "dy": 22}]}])

    Q(T, "Which water sample can hold the most dissolved oxygen? (The air above each is the same.)",
      ["A mountain stream at 5 °C", "A pond at 15 °C", "A river at 25 °C", "Water near a warm discharge at 35 °C"],
      ["Gases are more soluble in colder water, so the coldest sample holds the most {O2}.",
       "15 °C water holds less {O2} than 5 °C water; gas solubility falls as temperature rises.",
       "25 °C water holds even less {O2}; gas molecules escape warm water more easily.",
       "This is the warmest sample, so it holds the least {O2}. Gas solubility falls as temperature rises, unlike most solids."],
      "Gases and solids respond to temperature in opposite ways.",
      "Gas solubility falls as temperature rises: <b>the 5 °C stream</b> holds the most {O2}.", 1)

    S1, P1, P2 = '1.69', '1.00', '3.45'; v = D(S1) * D(P2) / D(P1); n = ns(S1, P1, P2)
    Q(T, "At 20.0 °C, %s g of {CO2} dissolves in 1.00 L of water when the {CO2} pressure is %s atm. A soda is bottled at 20.0 °C under a {CO2} pressure of %s atm. What is the solubility of {CO2} in it?" % (S1, P1, P2),
      [S(v, n, 'g/L'), S(D(S1) * D(P1) / D(P2), n, 'g/L'), S(D(P2) / D(S1), n, 'g/L'), S1 + ' g/L'],
      ["Henry's law: S<sub>2</sub> = S<sub>1</sub> &times; P<sub>2</sub>/P<sub>1</sub>. More pressure, more dissolved gas.",
       "This inverts the pressure ratio, so the solubility goes down as the pressure goes up. Henry's law is a direct relationship.",
       "This divides the pressure by the solubility. Set up S<sub>1</sub>/P<sub>1</sub> = S<sub>2</sub>/P<sub>2</sub> and solve for S<sub>2</sub>.",
       "Pressure has little effect on solids, but it matters a great deal for gases."],
      "S<sub>1</sub>/P<sub>1</sub> = S<sub>2</sub>/P<sub>2</sub>.",
      "S<sub>2</sub> = %s g/L &times; %s atm / %s atm = <b>%s</b>." % (S1, P2, P1, S(v, n, 'g/L')), 2, 1)

    S1, P1, P2 = '4.35', '0.132', '2.45'; v = D(S1) * D(P2) / D(P1); n = ns(S1, P1, P2)
    Q(T, "Plasma dissolves about %s mg of {O2} per liter when the {O2} partial pressure in the alveoli is %s atm. In a hyperbaric chamber the {O2} partial pressure is raised to %s atm at the same body temperature. What dissolved {O2} concentration does Henry's law predict?" % (S1, P1, P2),
      [S(v, n, 'mg/L'), S(D(S1) * D(P1) / D(P2), n, 'mg/L'), S(D(S1) * D(P2), n, 'mg/L'), S1 + ' mg/L'],
      ["S<sub>2</sub> = S<sub>1</sub> &times; P<sub>2</sub>/P<sub>1</sub>: the pressure rose about 19 times, so the dissolved {O2} does too. This is why hyperbaric oxygen loads so much {O2} into plasma. (Context only.)",
       "This inverts Henry's law; higher pressure means more dissolved gas, not less.",
       "This multiplies by P<sub>2</sub> but never divides by P<sub>1</sub> = %s atm." % P1,
       "Gas solubility depends on the gas's partial pressure; it does not stay the same."],
      "Henry's law is direct: S<sub>1</sub>/P<sub>1</sub> = S<sub>2</sub>/P<sub>2</sub>.",
      "S<sub>2</sub> = %s mg/L &times; %s atm / %s atm = <b>%s</b>." % (S1, P2, P1, S(v, n, 'mg/L')), 3, 1)

    Q(T, "A scuba diver rises to the surface too quickly. Why can nitrogen bubbles form in the diver's blood?",
      ["The pressure drops, so less {N2} can stay dissolved, and the extra comes out of solution as bubbles.",
       "The pressure drops, so more {N2} dissolves until the blood is supersaturated with it.",
       "The water near the surface is warmer, which makes {N2} more soluble in blood.",
       "{N2} reacts with the blood at low pressure to form a new gas."],
      ["Henry's law: gas solubility is proportional to partial pressure. At depth much {N2} dissolved; rising quickly lowers the pressure faster than the lungs can remove it, causing decompression sickness. (Context only.)",
       "This reverses Henry's law: lower pressure means <i>less</i> gas can dissolve.",
       "Warmer liquids hold <i>less</i> gas, and the main change on rising is the pressure.",
       "{N2} is unreactive in the body; the bubbles are simply {N2} coming out of solution."],
      "What happens to the pressure as the diver rises, and how does that affect a gas's solubility?",
      "Less pressure, less dissolved gas: <b>{N2} comes out of solution as bubbles</b>.", 2)

    hi, lo, w_ = '94.9', '65.3', '75.0'
    v = (D(hi) - D(lo)) * D(w_) / 100
    Q(T, "The solubility of KBr is %s g per 100. g of water at 80.0 °C and %s g per 100. g at 20.0 °C. A saturated solution made with %s g of water at 80.0 °C is cooled to 20.0 °C. What mass of KBr crystallizes?" % (hi, lo, w_),
      [S(v, 3, 'g'), addp(hi, '-' + lo) + ' g', S(D(hi) * D(w_) / 100, 3, 'g'), S(D(lo) * D(w_) / 100, 3, 'g')],
      ["Only %s g of water was used: it held %s g at 80.0 °C and can hold %s g at 20.0 °C." % (w_, num(D(hi) * D(w_) / 100, 3), num(D(lo) * D(w_) / 100, 3)),
       "This is the difference for 100. g of water. The solution was made with only %s g of water." % w_,
       "This is all the KBr dissolved at 80.0 °C; part of it can stay dissolved at 20.0 °C.",
       "This is the KBr that stays dissolved at 20.0 °C, not the amount that comes out."],
      "Scale both solubilities to %s g of water, then subtract." % w_,
      "(%s &minus; %s) g per 100. g &times; %s g/100. g = <b>%s</b>." % (hi, lo, w_, S(v, 3, 'g')), 3, 1)

    Q(T, "Why do soda makers chill the drink and seal it under high {CO2} pressure?",
      ["Low temperature and high {CO2} pressure both make {CO2} more soluble.",
       "Low temperature makes {CO2} less soluble, so high pressure is needed to make up for it.",
       "High pressure keeps the sugar dissolved; the {CO2} does not depend on pressure.",
       "Cold soda is denser, so it traps gas no matter what the pressure is."],
      ["Gases dissolve better in cold liquids and under higher partial pressure (Henry's law), so cold and sealed keeps the fizz in.",
       "Cold liquids hold <i>more</i> gas, not less.",
       "Pressure hardly affects the solubility of solids such as sugar; it is the {CO2} that depends on pressure.",
       "Density is not the reason; the amount of dissolved gas is set by temperature and the gas's pressure."],
      "How do temperature and pressure each affect a gas's solubility?",
      "Cold <b>and</b> high pressure both raise the solubility of {CO2}.", 1)

    Q(T, "A sealed solution of NaCl in water is put under 5 atm of pressure at constant temperature. What happens to the solubility of the NaCl?",
      ["Almost nothing; pressure affects the solubility of gases, not solids.", "It rises five times, by Henry's law.",
       "It falls, because the pressure squeezes ions out of solution.", "It rises, because pressure works like heating."],
      ["Solids and liquids are nearly incompressible, so pressure has almost no effect on how much of them dissolves.",
       "Henry's law applies to gases dissolving in liquids, not to solids such as NaCl.",
       "Pressure does not push dissolved ions out; it has almost no effect on solids.",
       "Pressure is not the same as heating; at constant temperature it does not change a solid's solubility."],
      "Henry's law is about which kind of solute?",
      "Pressure matters only for gases: <b>NaCl's solubility hardly changes</b>.", 2)

    Q(T, "A glass of cold tap water is left on the counter. As it warms to room temperature, tiny bubbles form on the inside of the glass. What are they, and why do they form?",
      ["Dissolved air coming out of solution, because gases are less soluble in warmer water",
       "Water vapor, because the water is starting to boil",
       "Dissolved air coming out of solution, because gases are more soluble in warmer water",
       "Dissolved minerals crystallizing, because solids are less soluble in warmer water"],
      ["Cold water holds more dissolved {N2} and {O2}; as it warms, the gases become less soluble and the extra forms bubbles.",
       "Room temperature is far below the boiling point; the bubbles are dissolved air leaving solution.",
       "Gas solubility <i>falls</i> as temperature rises; if it rose, no bubbles would form on warming.",
       "Most solids become <i>more</i> soluble as water warms, and the bubbles are a gas, not crystals."],
      "Gases are less soluble in warm water.",
      "Warmer water holds less gas: the bubbles are <b>dissolved air leaving solution</b>.", 2)

    # ======================= ch11-conc (14) =======================
    T = 'ch11-conc'
    g_, w_ = '4.50', '85.5'; tot = addp(g_, w_); v = D(g_) / D(tot) * 100; n = ns(g_, tot)
    Q(T, "A student dissolves %s g of NaCl in %s g of water. What is the mass percent of NaCl?" % (g_, w_),
      [P(v, n), P(D(g_) / D(w_) * 100, n), P(D(w_) / D(tot) * 100, n), P(D(g_) / D(tot), n)],
      ["Mass of solution = %s + %s = %s g; %%(m/m) = %s/%s &times; 100%%." % (g_, w_, tot, g_, tot),
       "This divides by the mass of water. The denominator is the whole solution: solute + solvent.",
       "This is the percent of <i>water</i> in the solution, not of NaCl.",
       "This is the mass fraction; multiply by 100% to get a percent."],
      "Mass of solution = mass of solute + mass of solvent.",
      "%s g + %s g = %s g of solution; %s/%s &times; 100%% = <b>%s</b>." % (g_, w_, tot, g_, tot, P(v, n)), 2, 1)

    g_, V = '16.8', '200.0'; v = D(g_) / D(V) * 100; n = ns(g_, V)
    Q(T, "A pharmacy dissolves %s g of sodium bicarbonate ({NaHCO3}) in water to make %s mL of solution. What is the concentration in %%(m/v)?" % (g_, V),
      [P(v, n), P(D(g_) / D(V), n), P(D(V) / D(g_) * 100, n), P(D(g_) / L(V) * 100, n)],
      ["%%(m/v) = g solute / mL solution &times; 100%% = %s g / %s mL &times; 100%%. (This is the strength of the 8.4%% sodium bicarbonate injection used in hospitals.)" % (g_, V),
       "This is the ratio without the &times; 100%.",
       "This divides mL by grams; the solute goes on top.",
       "This divides by liters. %(m/v) uses milliliters of solution."],
      "%(m/v) = (g solute / mL solution) &times; 100%.",
      "%s g / %s mL &times; 100%% = <b>%s</b>." % (g_, V, P(v, n)), 1, 1)

    V, pc = '250.', '3.00'; v = D(V) * D(pc) / 100; n = ns(V, pc)
    Q(T, "How many grams of NaCl are in a %s mL bag of %s%% (m/v) NaCl, a hypertonic saline?" % (V, pc),
      [S(v, n, 'g'), S(D(V) * D(pc), n, 'g'), S(D(V) * D(pc) / 1000, n, 'g'), S(D(V) / D(pc), n, 'g')],
      ["%s%% (m/v) means %s g per 100 mL, a conversion factor: %s mL &times; %s g/100 mL." % (pc, pc, V, pc),
       "This multiplies by %s without dividing by 100 mL." % pc,
       "This treats the percent as grams per 1000 mL; percent means per 100 mL.",
       "This divides the volume by the percent; use %s g/100 mL as a conversion factor." % pc],
      "Write %s%% (m/v) as %s g NaCl / 100 mL solution." % (pc, pc),
      "%s mL &times; (%s g / 100 mL) = <b>%s</b>." % (V, pc, S(v, n, 'g')), 2, 1)

    a_, V = '35.0', '50.0'; v = D(a_) / D(V) * 100; n = ns(a_, V)
    Q(T, "A lab technician mixes %s mL of ethanol with enough water to make %s mL of solution. What is the %%(v/v) of ethanol?" % (a_, V),
      [P(v, n), P(D(V) / D(a_) * 100, n), P(D(a_) / D(V), n), P(D(a_) / (D(a_) + D(V)) * 100, n)],
      ["%%(v/v) = mL solute / mL solution &times; 100%% = %s/%s &times; 100%%." % (a_, V),
       "This divides the solution volume by the ethanol volume; the solute goes on top.",
       "This is the volume fraction; multiply by 100%.",
       "This adds %s + %s as if %s mL were the water. %s mL is already the whole solution." % (a_, V, V, V)],
      "The denominator is the total volume of solution.",
      "%s mL / %s mL &times; 100%% = <b>%s</b>." % (a_, V, P(v, n)), 1, 1)

    mg, V = '0.845', '1.25'; v = D(mg) / D(V); n = ns(mg, V)
    Q(T, "A tap-water sample contains %s mg of fluoride in %s L. What is the fluoride concentration in ppm?" % (mg, V),
      [S(v, n, 'ppm'), S(v * 1000, n, 'ppm'), S(D(V) / D(mg), n, 'ppm'), mg + ' ppm'],
      ["In dilute water, 1 ppm &asymp; 1 mg/L: %s mg / %s L. Community water fluoridation aims for about 0.7 mg/L." % (mg, V),
       "This multiplies by 1000, as if converting mg to &mu;g; that would give ppb, not ppm.",
       "This divides liters by milligrams; the solute goes on top.",
       "This ignores the volume. ppm &asymp; mg per <i>liter</i>, so divide by %s L." % V],
      "1 ppm &asymp; 1 mg/L in dilute water.",
      "%s mg / %s L = %s mg/L = <b>%s</b>." % (mg, V, num(v, n), S(v, n, 'ppm')), 2, 1)

    c_ = '0.00865'; v = D(c_) * 1000; n = sfs(c_)
    Q(T, "A rural Valley well contains %s mg of arsenic per liter. What is this concentration in ppb?" % c_,
      [S(v, n, 'ppb'), S(D(c_) * 10 ** 6, n, 'ppb'), S(D(c_) / 1000, n, 'ppb'), c_ + ' ppb'],
      ["1 mg = 1000 &mu;g, and 1 &mu;g/L &asymp; 1 ppb. This well is just under the 10 ppb arsenic limit.",
       "This multiplies by 10<sup>6</sup>, which converts mg to ng and gives ppt, not ppb.",
       "This divides by 1000; going from mg to the smaller &mu;g makes the number larger.",
       "%s mg/L is the value in ppm. ppb needs &mu;g/L." % c_],
      "Convert mg/L to &mu;g/L.",
      "%s mg/L &times; 1000 &mu;g/mg = %s &mu;g/L = <b>%s</b>." % (c_, num(v, n), S(v, n, 'ppb')), 2, 1)

    c_ = '0.00000715'; v = D(c_) * 10 ** 6; n = sfs(c_)
    Q(T, "A Valley well contains %s mg/L of 1,2,3-trichloropropane (1,2,3-TCP). What is this concentration in ppt (parts per trillion)?" % c_,
      [S(v, n, 'ppt'), S(D(c_) * 1000, n, 'ppt'), S(D(c_), n, 'ppt'), S(D(c_) * 10 ** 9, n, 'ppt')],
      ["1 mg = 10<sup>6</sup> ng, and 1 ng/L &asymp; 1 ppt. This is above California's limit of 5 ppt, so the water must be treated.",
       "This multiplies by 1000, giving &mu;g/L, which is ppb, not ppt.",
       "This is the value in mg/L, which is ppm, written in scientific notation.",
       "This multiplies by 10<sup>9</sup> (mg to pg); 1 ppt &asymp; 1 <i>ng</i>/L."],
      "Convert mg/L to ng/L (1 mg = 10<sup>6</sup> ng).",
      "%s mg/L &times; 10<sup>6</sup> ng/mg = <b>%s</b>, above the 5 ppt limit." % (c_, S(v, n, 'ppt')), 3, 1)

    mg, g_ = '0.0410', '125.0'; v = D(mg) / (D(g_) / 1000); n = ns(mg, g_)
    Q(T, "A %s g sample of canned tuna contains %s mg of mercury. What is the mercury concentration in ppm by mass?" % (g_, mg),
      [S(v, n, 'ppm'), S(D(mg) / D(g_) * 10 ** 6, n, 'ppm'), S(D(mg) / D(g_), n, 'ppm'), S(D(g_) / D(mg), n, 'ppm')],
      ["ppm by mass = mg per kg: %s mg / %s kg." % (mg, num(D(g_) / 1000, 4)),
       "This uses 10<sup>6</sup> without converting mg to g; mg/g &times; 10<sup>6</sup> counts the mass unit change twice.",
       "This is mg per gram; ppm is mg per <i>kilogram</i> (or g per 10<sup>6</sup> g).",
       "This divides the sample mass by the mercury mass; the mercury goes on top."],
      "1 ppm = 1 mg per kg.",
      "%s mg / %s kg = <b>%s</b>." % (mg, num(D(g_) / 1000, 4), S(v, n, 'ppm')), 3, 1)

    g_, V, f_ = '2.45', '75.0', 'KBr'; mw = mm(f_); mol = D(g_) / mw; v = mol / L(V); n = ns(g_, V)
    Q(T, "What is the molarity of a solution that contains %s g of {KBr} (%s g/mol) in %s mL of solution?" % (g_, mw, V),
      [S(v, n, 'M'), S(mol / D(V), n, 'M'), S(D(g_) / L(V), n, 'M'), S(L(V) / mol, n, 'M')],
      ["mol {KBr} = %s/%s = %s mol; M = mol / L = %s mol / %s L." % (g_, mw, num(mol, 4), num(mol, 4), Ls(V)),
       "This divides by %s mL. Molarity needs liters: %s L." % (V, Ls(V)),
       "This uses grams instead of moles. Convert with the molar mass first.",
       "This divides liters by moles; molarity is moles over liters."],
      "Grams to moles, mL to L, then divide.",
      "%s g / %s g/mol = %s mol; %s mol / %s L = <b>%s</b>." % (g_, mw, num(mol, 4), num(mol, 4), Ls(V), S(v, n, 'M')), 2, 1)

    g_, V, f_ = '9.70', '200.0', 'C6H12O6'; mw = mm(f_); mol = D(g_) / mw; v = mol / L(V); n = ns(g_, V)
    Q(T, "A cell-culture lab dissolves %s g of glucose ({C6H12O6}, %s g/mol) in water to make %s mL of solution. What is the molarity of glucose?" % (g_, mw, V),
      [S(v, n, 'M'), S(mol / D(V), n, 'M'), S(D(g_) / L(V), n, 'M'), S(mol, n, 'M')],
      ["%s g / %s g/mol = %s mol; %s mol / %s L." % (g_, mw, num(mol, 4), num(mol, 4), Ls(V)),
       "This divides by milliliters. Convert %s mL to %s L first." % (V, Ls(V)),
       "This divides grams by liters; molarity needs moles of glucose.",
       "This is the number of moles; it still has to be divided by the volume in liters."],
      "M = mol solute / L solution.",
      "%s mol / %s L = <b>%s</b>." % (num(mol, 4), Ls(V), S(v, n, 'M')), 2, 1)

    pc, d_, f_ = '6.00', '1.08', 'NaOCl'; mw = mm(f_); mol = D(pc) / mw; Vs = 100 / D(d_); v = mol / (Vs / 1000); n = ns(pc, d_)
    Q(T, "A household bleach is %s%% (m/m) sodium hypochlorite, {NaOCl} (%s g/mol), and has a density of %s g/mL. What is the molarity of {NaOCl}?" % (pc, mw, d_),
      [S(v, n, 'M'), S(mol / D('0.100'), n, 'M'), S(mol / (100 * D(d_) / 1000), n, 'M'), S(D(pc) / (Vs / 1000), n, 'M')],
      ["In 100. g of solution: %s g {NaOCl} = %s mol; volume = 100. g &divide; %s g/mL = %s mL = %s L." % (pc, num(mol, 4), d_, num(Vs, 4), num(Vs / 1000, 4)),
       "This takes 100. g of solution as 100. mL. Use the density to find the volume.",
       "This multiplies by the density (100 &times; %s mL). Volume = mass &divide; density." % d_,
       "This uses grams of {NaOCl} instead of moles."],
      "Assume 100. g of solution: the percent gives grams of solute, and the density gives the volume.",
      "%s mol / %s L = <b>%s</b>." % (num(mol, 4), num(Vs / 1000, 4), S(v, n, 'M')), 3, 1)

    pc, d_, f_ = '37.2', '1.19', 'HCl'; mw = mm(f_); mol = D(pc) / mw; Vs = 100 / D(d_); v = mol / (Vs / 1000); n = ns(pc, d_)
    Q(T, "Concentrated hydrochloric acid is %s%% (m/m) HCl (%s g/mol) with a density of %s g/mL. What is its molarity?" % (pc, mw, d_),
      [S(v, n, 'M'), S(mol / D('0.100'), n, 'M'), S(mol / (100 * D(d_) / 1000), n, 'M'), S(D(pc) / (Vs / 1000), n, 'M')],
      ["100. g of solution holds %s g HCl = %s mol, in 100. g &divide; %s g/mL = %s mL." % (pc, num(mol, 4), d_, num(Vs, 4)),
       "This uses 100. mL for 100. g of solution; this acid is denser than water, so use the density.",
       "This multiplies 100. g by the density; to get a volume, divide mass by density.",
       "This divides grams of HCl by liters; convert to moles first."],
      "Assume 100. g of solution.",
      "%s mol / %s L = <b>%s</b>." % (num(mol, 4), num(Vs / 1000, 4), S(v, n, 'M')), 3, 1)

    Q(T, "An IV bag is labeled 0.9% (m/v) NaCl. What does the label mean?",
      ["0.9 g of NaCl in every 100 mL of solution", "0.9 g of NaCl in every 100 g of water",
       "0.9 g of NaCl added to every 100 mL of water", "0.9 mol of NaCl in every liter of solution"],
      ["%(m/v) is grams of solute per 100 mL of <i>solution</i>.",
       "That describes a mass percent based on the water only; %(m/v) uses mL of solution.",
       "The denominator is the volume of solution, not the volume of water the salt is added to.",
       "Moles per liter is molarity; a percent uses grams."],
      "m/v = mass of solute over volume of solution.",
      "<b>0.9 g NaCl per 100 mL of solution</b>.", 1)

    Q(T, "A student adds 0.175 mol of KCl to 1.000 L of water and stirs until it dissolves. Why is the molarity <b>not</b> exactly 0.175 M?",
      ["Molarity uses liters of solution, and the solution's volume is not exactly 1.000 L.",
       "Molarity uses kilograms of solvent, not liters.",
       "KCl separates into two ions, so the molarity doubles.",
       "The moles of KCl decrease as it dissolves."],
      ["Dissolving the solid changes the volume a little. To make an exact molarity, dissolve the solute and then add water to the line of a volumetric flask.",
       "Kilograms of solvent is molality, not molarity.",
       "Molarity counts formula units of KCl; counting ions matters for colligative properties, not for the molarity of KCl.",
       "Dissolving does not destroy any KCl; the moles are unchanged."],
      "Look at the denominator of molarity.",
      "M = mol / L of <b>solution</b>, and the solution is not exactly 1.000 L.", 2)

    # ======================= ch11-dilution (14) =======================
    T = 'ch11-dilution'
    V, c_ = '36.5', '0.225'; v = L(V) * D(c_); n = ns(V, c_)
    Q(T, "How many moles of NaOH are in %s mL of %s M NaOH?" % (V, c_),
      [S(v, n, 'mol'), S(D(V) * D(c_), n, 'mol'), S(L(V) / D(c_), n, 'mol'), S(D(c_) / L(V), n, 'mol')],
      ["mol = M &times; L = %s mol/L &times; %s L." % (c_, Ls(V)),
       "This multiplies by %s mL; convert to liters first." % V,
       "This divides the volume by the molarity; mol = M &times; V.",
       "This divides the molarity by the volume, which does not give moles."],
      "mol = M &times; V (in liters).",
      "%s L &times; %s mol/L = <b>%s</b>." % (Ls(V), c_, S(v, n, 'mol')), 1, 1)

    V, c_, f_ = '200.0', '0.325', 'CaCl2'; mw = mm(f_); mol = L(V) * D(c_); v = mol * mw; n = ns(V, c_)
    Q(T, "What mass of {CaCl2} (%s g/mol) is needed to prepare %s mL of %s M {CaCl2}?" % (mw, V, c_),
      [S(v, n, 'g'), S(D(V) * D(c_) * mw, n, 'g'), S(mol, n, 'g'), S(mol / mw, n, 'g')],
      ["%s L &times; %s mol/L = %s mol; &times; %s g/mol." % (Ls(V), c_, num(mol, 4), mw),
       "This uses %s mL as liters; the answer is 1000 times too large." % V,
       "This is the number of moles; multiply by the molar mass to get grams.",
       "This divides by the molar mass; going from moles to grams, multiply."],
      "L &rarr; mol (&times; M) &rarr; g (&times; molar mass).",
      "%s mol &times; %s g/mol = <b>%s</b>." % (num(mol, 4), mw, S(v, n, 'g')), 2, 1)

    mol, c_ = '2.85', '0.125'; mo = D(mol) / 1000; v = mo / D(c_) * 1000; n = ns(mol, c_)
    Q(T, "What volume of %s M HCl contains %s &times; 10<sup>&minus;3</sup> mol of HCl? Give the answer in mL." % (c_, mol),
      [S(v, n, 'mL'), S(mo / D(c_), n, 'mL'), S(mo * D(c_) * 1000, n, 'mL'), S(D(c_) / mo, n, 'mL')],
      ["V = mol &divide; M = %s &times; 10<sup>&minus;3</sup> mol &divide; %s mol/L = %s L." % (mol, c_, num(mo / D(c_), n)),
       "This is the volume in liters with a mL label; multiply by 1000 mL/L.",
       "This multiplies moles by molarity; to get liters, divide moles by molarity.",
       "This divides molarity by moles, which is the reciprocal of the volume."],
      "V (L) = mol / M.",
      "%s L = <b>%s</b>." % (num(mo / D(c_), n), S(v, n, 'mL')), 2, 1)

    V1, c1, w_ = '12.0', '2.40', '36.0'; V2 = addp(V1, w_); v = D(c1) * D(V1) / D(V2); n = ns(c1, V1, V2)
    Q(T, "A %s mL portion of %s M HCl is mixed with %s mL of water. What is the molarity of the diluted HCl?" % (V1, c1, w_),
      [S(v, n, 'M'), S(D(c1) * D(V1) / D(w_), n, 'M'), S(D(c1) * D(V2) / D(V1), n, 'M'), S(D(c1) * D(V1), n, 'M')],
      ["V<sub>2</sub> is the total volume: %s + %s = %s mL. M<sub>2</sub> = M<sub>1</sub>V<sub>1</sub>/V<sub>2</sub>." % (V1, w_, V2),
       "This uses the %s mL of water added as V<sub>2</sub>. V<sub>2</sub> is the total final volume." % w_,
       "This inverts the volume ratio, so the &ldquo;diluted&rdquo; acid is stronger than the stock.",
       "This is M<sub>1</sub>V<sub>1</sub> without dividing by V<sub>2</sub>."],
      "Find the total final volume first.",
      "V<sub>2</sub> = %s mL; M<sub>2</sub> = (%s M)(%s mL) / %s mL = <b>%s</b>." % (V2, c1, V1, V2, S(v, n, 'M')), 3, 1)

    c1, V2, c2 = '1.25', '50.00', '35.0'; v = D(c2) / 1000 * D(V2) / D(c1); n = ns(c1, V2, c2)
    Q(T, "How many milliliters of %s M stock are needed to prepare %s mL of %s mM solution?" % (c1, V2, c2),
      [S(v, n, 'mL'), S(D(c2) * D(V2) / D(c1), n, 'mL'), S(D(c1) * D(V2) / (D(c2) / 1000), n, 'mL'), S(D(c2) / 1000 * D(c1) / D(V2), n, 'mL')],
      ["Make the units match: %s mM = %s M (1 M = 1000 mM). V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>/M<sub>1</sub>." % (c2, num(D(c2) / 1000, 3)),
       "This uses %s mM and %s M together without converting; the units on both sides must match." % (c2, c1),
       "This puts the stock concentration on top; V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>/M<sub>1</sub>.",
       "This rearranges M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub> incorrectly, dividing by V<sub>2</sub>."],
      "Convert mM to M, then V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>/M<sub>1</sub>.",
      "(%s M)(%s mL) / %s M = <b>%s</b>." % (num(D(c2) / 1000, 3), V2, c1, S(v, n, 'mL')), 2, 1)

    V1, c1, V2 = '2.00', '0.180', '50.0'; v2M = D(c1) * D(V1) / D(V2); n = ns(V1, c1, V2)
    Q(T, "A %s mL sample of %s M glucose is diluted to a total volume of %s mL. What is the new concentration in millimolar (mM)?" % (V1, c1, V2),
      [S(v2M * 1000, n, 'mM'), S(v2M, n, 'mM'), S(D(c1) * D(V2) / D(V1) * 1000, n, 'mM'), S(v2M / 1000, n, 'mM')],
      ["M<sub>2</sub> = (%s M)(%s mL)/%s mL = %s M; &times; 1000 mM/M." % (c1, V1, V2, num(v2M, n)),
       "This is the answer in M with an mM label; multiply by 1000 mM/M.",
       "This inverts the volume ratio; a diluted solution must be weaker.",
       "This divides by 1000; there are 1000 mM in 1 M, so the number of mM is larger."],
      "Dilute first (M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>), then convert M to mM.",
      "%s M &times; 1000 mM/M = <b>%s</b>." % (num(v2M, n), S(v2M * 1000, n, 'mM')), 2, 1)

    V1, c1, c2 = '16.0', '0.880', '0.275'; V2 = D(c1) * D(V1) / D(c2); n = ns(V1, c1, c2); V2s = num(V2, n); wa = addp(V2s, '-' + V1)
    Q(T, "A %s mL sample of %s M KCl is to be diluted to %s M. How much water must be added?" % (V1, c1, c2),
      [wa + ' mL', V2s + ' mL', S(D(c2) * D(V1) / D(c1), n, 'mL'), addp(V2s, V1) + ' mL'],
      ["V<sub>2</sub> = M<sub>1</sub>V<sub>1</sub>/M<sub>2</sub> = %s mL is the total volume; water added = %s &minus; %s mL." % (V2s, V2s, V1),
       "This is the total final volume V<sub>2</sub>, which already includes the %s mL of stock." % V1,
       "This inverts the ratio; the volume must grow when the solution is diluted.",
       "This adds the stock volume to V<sub>2</sub>; V<sub>2</sub> is already the total."],
      "M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub> gives the total volume. Then subtract.",
      "V<sub>2</sub> = (%s)(%s) / %s = %s mL; water = %s &minus; %s = <b>%s mL</b>." % (c1, V1, c2, V2s, V2s, V1, wa), 3, 1)

    c0 = D('4.2e6'); v = c0 / 100
    Q(T, "A urine culture has about 4.2 &times; 10<sup>6</sup> bacteria per mL. A technician adds 0.50 mL of it to 4.5 mL of sterile saline and mixes, then adds 0.50 mL of that tube to another 4.5 mL of saline (two dilutions in all). What is the concentration in the second tube?",
      [S(v, 2, 'bacteria/mL'), S(c0 / 9 ** 2, 2, 'bacteria/mL'), S(c0 / 10, 2, 'bacteria/mL'), S(c0 / 20, 2, 'bacteria/mL')],
      ["Each step dilutes 0.50 mL to a total of 5.0 mL, a factor of 10. Two steps: 10 &times; 10 = 100.",
       "This divides by 9 each time, using the saline added as V<sub>2</sub>. The total volume is 5.0 mL, so each factor is 10.",
       "This counts only one dilution; there were two.",
       "This divides by 10 + 10 = 20. Dilution factors multiply: 10 &times; 10."],
      "Each 0.50 mL + 4.5 mL step is a 1-to-10 dilution; the factors multiply.",
      "4.2 &times; 10<sup>6</sup> &divide; 100 = <b>%s</b>." % S(v, 2, 'bacteria/mL'), 3, 1)

    c1, V2, c2 = '70.0', '400.0', '45.0'; v = D(c2) * D(V2) / D(c1); n = ns(c1, V2, c2)
    Q(T, "How many milliliters of %s%% (v/v) isopropyl alcohol are needed to make %s mL of %s%% (v/v) isopropyl alcohol?" % (c1, V2, c2),
      [S(v, n, 'mL'), S(D(c1) * D(V2) / D(c2), n, 'mL'), num(D(V2) - v, n) + ' mL', S(D(c2) * D(c1) / D(V2), n, 'mL')],
      ["C<sub>1</sub>V<sub>1</sub> = C<sub>2</sub>V<sub>2</sub> works with percents: V<sub>1</sub> = (%s%%)(%s mL)/%s%%." % (c2, V2, c1),
       "This inverts the concentrations; the stock volume must be less than the final %s mL." % V2,
       "This is the volume of water to add, not the volume of stock.",
       "This rearranges the equation incorrectly; V<sub>1</sub> = C<sub>2</sub>V<sub>2</sub>/C<sub>1</sub>."],
      "Percent works in C<sub>1</sub>V<sub>1</sub> = C<sub>2</sub>V<sub>2</sub> as long as it is the same percent on both sides.",
      "V<sub>1</sub> = (%s)(%s) / %s = <b>%s</b>." % (c2, V2, c1, S(v, n, 'mL')), 2, 1)

    Q(T, "When a solution is diluted with water, which quantity stays the same?",
      ["The moles of solute", "The molarity", "The volume of solution", "The mass of the solution"],
      ["Adding solvent spreads the same moles through a larger volume; that is why M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>.",
       "The molarity goes down; that is the point of diluting.",
       "The volume goes up as solvent is added.",
       "Added water adds mass, so the mass of solution increases."],
      "M &times; V = moles. What does M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub> say stays fixed?",
      "<b>Moles of solute</b> are unchanged by dilution.", 1)

    g_, c_ = '2.40', '0.355'; mw = mm('NaCl'); mol = D(g_) / mw; v = mol / D(c_) * 1000; n = ns(g_, c_)
    Q(T, "What volume of %s M NaCl (%s g/mol) contains %s g of NaCl? Give the answer in mL." % (c_, mw, g_),
      [S(v, n, 'mL'), S(D(g_) / D(c_) * 1000, n, 'mL'), S(mol * D(c_) * 1000, n, 'mL'), S(mol / D(c_), n, 'mL')],
      ["%s g / %s g/mol = %s mol; V = %s mol &divide; %s mol/L = %s L." % (g_, mw, num(mol, 4), num(mol, 4), c_, num(mol / D(c_), n)),
       "This divides grams by molarity; convert grams to moles first.",
       "This multiplies moles by molarity; V = mol &divide; M.",
       "This is the volume in liters with an mL label."],
      "g &rarr; mol &rarr; L &rarr; mL.",
      "%s mol &divide; %s M = %s L = <b>%s</b>." % (num(mol, 4), c_, num(mol / D(c_), n), S(v, n, 'mL')), 2, 1)

    c_, V = '5.6', '5.00'; v = D(c_) / 1000 * L(V); n = ns(c_, V)
    Q(T, "A %s mL blood sample has a glucose concentration of %s mM. How many moles of glucose does it contain?" % (V, c_),
      [S(v, n, 'mol'), S(D(c_) * L(V), n, 'mol'), S(D(c_) * D(V), n, 'mol'), S(v / 1000, n, 'mol')],
      ["%s mM = %s M; %s mL = %s L; mol = M &times; L." % (c_, num(D(c_) / 1000, n), V, Ls(V)),
       "This uses %s mM as if it were %s M; divide by 1000 first." % (c_, c_),
       "This multiplies mM by mL with neither converted.",
       "This divides by 1000 one time too many."],
      "Convert both: mM &rarr; M and mL &rarr; L.",
      "(%s mol/L)(%s L) = <b>%s</b>." % (num(D(c_) / 1000, n), Ls(V), S(v, n, 'mol')), 2, 1)

    V1, V2, c2 = '4.00', '50.0', '0.0328'; v = D(c2) * D(V2) / D(V1); n = ns(V1, V2, c2)
    Q(T, "A technician pipets %s mL of a stock solution into a flask and dilutes it to a total of %s mL. The diluted solution is %s M. What was the molarity of the stock?" % (V1, V2, c2),
      [S(v, n, 'M'), S(D(c2) * D(V1) / D(V2), n, 'M'), S(D(c2) * D(V2), n, 'M'), c2 + ' M'],
      ["M<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>/V<sub>1</sub> = (%s)(%s)/%s. The stock must be stronger than the diluted solution." % (c2, V2, V1),
       "This gives a stock weaker than the diluted solution; the volumes are swapped.",
       "This is M<sub>2</sub>V<sub>2</sub> without dividing by V<sub>1</sub>.",
       "Dilution lowers the concentration, so the stock cannot be the same as the diluted solution."],
      "Solve M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub> for M<sub>1</sub>.",
      "M<sub>1</sub> = (%s M)(%s mL) / %s mL = <b>%s</b>." % (c2, V2, V1, S(v, n, 'M')), 2, 1)

    Q(T, "Which is the correct way to prepare 100.0 mL of a dilute solution from a stock solution with a 100-mL volumetric flask?",
      ["Pipet the calculated volume of stock into the flask, then add water up to the line and mix.",
       "Pipet the calculated volume of stock into the flask, then add 100.0 mL of water.",
       "Fill the flask to the line with water, then pipet in the stock.",
       "Pipet 100.0 mL of stock into the flask, then add the calculated volume of water."],
      ["V<sub>2</sub> is the total volume, so the stock goes in first and water is added up to the 100.0 mL line.",
       "Adding 100.0 mL of water makes the total more than 100.0 mL; water is added only up to the line.",
       "The flask would then hold more than 100.0 mL; the stock goes in first.",
       "This uses the final volume of stock; only the small calculated volume V<sub>1</sub> of stock is needed."],
      "V<sub>2</sub> is the total final volume.",
      "<b>Stock in first, then water to the line</b>, so the total is exactly 100.0 mL.", 1)

    # ======================= ch11-titration (12) =======================
    T = 'ch11-titration'
    Va, ca, cb = '21.5', '0.135', '0.185'; mol = L(Va) * D(ca); v = mol * 2 / D(cb) * 1000; n = ns(Va, ca, cb)
    Q(T, "What volume of %s M KI reacts completely with %s mL of %s M {Pb(NO3)2}? [[Pb(NO3)2(aq) + 2 KI(aq) -> PbI2(s) + 2 KNO3(aq)]]" % (cb, Va, ca),
      [S(v, n, 'mL'), S(mol / D(cb) * 1000, n, 'mL'), S(mol / 2 / D(cb) * 1000, n, 'mL'), S(mol * 2 * D(cb) * 1000, n, 'mL')],
      ["mol {Pb(NO3)2} = %s L &times; %s M = %s mol; &times; 2 mol KI / 1 mol {Pb(NO3)2}; &divide; %s M." % (Ls(Va), ca, num(mol, 4), cb),
       "This skips the mole ratio. Each {Pb(NO3)2} needs 2 KI.",
       "This flips the mole ratio (1/2 instead of 2/1).",
       "This multiplies moles of KI by the molarity; V = mol &divide; M."],
      "V &times; M &rarr; mol &rarr; mole ratio &rarr; mol &rarr; &divide; M.",
      "%s mol &times; 2 = %s mol KI; &divide; %s M = <b>%s</b>." % (num(mol, 4), num(mol * 2, 4), cb, S(v, n, 'mL')), 2, 1)

    Vb, cb_ = '35.0', '0.0860'; mol = L(Vb) * D(cb_); mw = mm('CaCO3'); v = mol * mw; n = ns(Vb, cb_)
    Q(T, "Calcium carbonate, the scale that builds up in Valley pipes with hard water, can be made by precipitation. What mass of {CaCO3} (%s g/mol) forms when %s mL of %s M {CaCl2} reacts with excess {Na2CO3}? [[CaCl2(aq) + Na2CO3(aq) -> CaCO3(s) + 2 NaCl(aq)]]" % (mw, Vb, cb_),
      [S(v, n, 'g'), S(D(Vb) * D(cb_) * mw, n, 'g'), S(mol, n, 'g'), S(mol / mw, n, 'g')],
      ["%s L &times; %s M = %s mol {CaCl2} = %s mol {CaCO3} (1 : 1); &times; %s g/mol." % (Ls(Vb), cb_, num(mol, 4), num(mol, 4), mw),
       "This uses mL as liters; convert %s mL to %s L." % (Vb, Ls(Vb)),
       "This is moles of {CaCO3}; multiply by the molar mass.",
       "This divides by the molar mass; going from moles to grams, multiply."],
      "V &times; M &rarr; mol {CaCl2} &rarr; mol {CaCO3} &rarr; g.",
      "%s mol &times; %s g/mol = <b>%s</b>." % (num(mol, 4), mw, S(v, n, 'g')), 2, 1)

    Vs, cb_, i_, f_ = '15.00', '0.1125', '1.25', '23.65'; Vt = addp(f_, '-' + i_); mol = L(Vt) * D(cb_); v = mol / L(Vs); n = ns(Vt, cb_, Vs)
    Q(T, "A %s mL sample of {HNO3} is titrated with %s M NaOH to a phenolphthalein endpoint. Use the buret readings in the table. What is the molarity of the {HNO3}? [[HNO3(aq) + NaOH(aq) -> NaNO3(aq) + H2O(l)]]" % (Vs, cb_),
      [S(v, n, 'M'), S(L(f_) * D(cb_) / L(Vs), n, 'M'), S(L(Vs) * D(cb_) / L(Vt), n, 'M'), S(mol / L(Vt), n, 'M')],
      ["Volume of NaOH = %s &minus; %s = %s mL; mol NaOH = %s L &times; %s M = %s mol = mol {HNO3} (1 : 1); &divide; %s L." % (f_, i_, Vt, Ls(Vt), cb_, num(mol, 4), Ls(Vs)),
       "This uses the final buret reading as the volume. The volume used is final &minus; initial.",
       "This swaps the two volumes; the moles of base come from the NaOH volume, and you divide by the acid's volume.",
       "This divides by the NaOH volume, which just gives back the NaOH molarity. Divide by the volume of the acid sample."],
      "Volume used = final &minus; initial; then mol NaOH = mol {HNO3}; divide by the acid's volume.",
      "%s mL NaOH; %s mol; %s mol / %s L = <b>%s</b>." % (Vt, num(mol, 4), num(mol, 4), Ls(Vs), S(v, n, 'M')), 2, 1,
      [{"type": "table", "cap": "Buret readings (NaOH)", "head": ["Reading", "Volume (mL)"], "rows": [["Initial", i_], ["Final (endpoint)", f_]]}])

    g_, Vb = '0.1715', '27.33'; mw = mm('H2C2O4'); ma = D(g_) / mw; v = ma * 2 / L(Vb); n = ns(g_, Vb)
    Q(T, "To standardize a NaOH solution, a student dissolves %s g of oxalic acid, {H2C2O4} (%s g/mol), in water and titrates it with the NaOH. The endpoint takes %s mL. What is the molarity of the NaOH? [[H2C2O4(aq) + 2 NaOH(aq) -> Na2C2O4(aq) + 2 H2O(l)]]" % (g_, mw, Vb),
      [S(v, n, 'M'), S(ma / L(Vb), n, 'M'), S(ma / 2 / L(Vb), n, 'M'), S(D(g_) * 2 / L(Vb), n, 'M')],
      ["%s g / %s g/mol = %s mol {H2C2O4}; &times; 2 = %s mol NaOH; &divide; %s L." % (g_, mw, num(ma, 4), num(ma * 2, 4), Ls(Vb)),
       "This treats the reaction as 1 : 1. Oxalic acid has two acidic hydrogens, so it needs 2 NaOH.",
       "This flips the mole ratio: 2 mol NaOH per 1 mol {H2C2O4}, so multiply by 2.",
       "This uses grams of oxalic acid as moles; convert with the molar mass first."],
      "Solid known: grams &rarr; mol acid &rarr; mol NaOH (&times; 2) &rarr; &divide; L NaOH.",
      "%s mol NaOH / %s L = <b>%s</b>." % (num(ma * 2, 4), Ls(Vb), S(v, n, 'M')), 3, 1)

    Va, ca, cb = '12.5', '0.0840', '0.105'; ma = L(Va) * D(ca); v = ma * 2 / D(cb) * 1000; n = ns(Va, ca, cb)
    Q(T, "What volume of %s M NaOH neutralizes %s mL of %s M {H2SO4}? [[H2SO4(aq) + 2 NaOH(aq) -> Na2SO4(aq) + 2 H2O(l)]]" % (cb, Va, ca),
      [S(v, n, 'mL'), S(ma / D(cb) * 1000, n, 'mL'), S(ma / 2 / D(cb) * 1000, n, 'mL'), S(ma * 2 / D(ca) * 1000, n, 'mL')],
      ["%s L &times; %s M = %s mol {H2SO4}; &times; 2 = %s mol NaOH; &divide; %s M." % (Ls(Va), ca, num(ma, 4), num(ma * 2, 4), cb),
       "This assumes 1 : 1. {H2SO4} has two acidic hydrogens, so each mole needs 2 mol NaOH.",
       "This flips the mole ratio; there are 2 mol NaOH per mol {H2SO4}.",
       "This divides the moles of NaOH by the acid's molarity; use the NaOH molarity."],
      "Watch the mole ratio for a diprotic acid.",
      "%s mol NaOH &divide; %s M = <b>%s</b>." % (num(ma * 2, 4), cb, S(v, n, 'mL')), 2, 1)

    s_, cb_, Vb = '0.4250', '0.1185', '18.54'; mw = mm('C9H8O4'); mol = L(Vb) * D(cb_); ga = mol * mw; v = ga / D(s_) * 100; n = ns(s_, cb_, Vb)
    Q(T, "A %s g sample of a crushed aspirin tablet is dissolved and titrated with %s M NaOH; the endpoint takes %s mL. Aspirin, {C9H8O4} (%s g/mol), reacts 1 : 1 with NaOH. What is the mass percent of aspirin in the sample? [[C9H8O4(aq) + NaOH(aq) -> NaC9H7O4(aq) + H2O(l)]]" % (s_, cb_, Vb, mw),
      [P(v, n), P(mol / D(s_) * 100, n), S(ga, n, 'g'), P(D(s_) / ga * 100, n)],
      ["mol NaOH = %s L &times; %s M = %s mol = mol aspirin; &times; %s g/mol = %s g; &divide; %s g &times; 100%%." % (Ls(Vb), cb_, num(mol, 4), mw, num(ga, 4), s_),
       "This divides moles by grams; convert moles of aspirin to grams first.",
       "This is the mass of aspirin; the question asks for the percent of the sample.",
       "This divides the sample mass by the aspirin mass; the part goes on top."],
      "Find grams of aspirin, then divide by the sample mass.",
      "%s g / %s g &times; 100%% = <b>%s</b>." % (num(ga, 4), s_, P(v, n)), 3, 1)

    i_, f_ = '0.85', '17.40'; v = addp(f_, '-' + i_)
    Q(T, "A buret reads %s mL before a titration and %s mL at the endpoint. What volume of titrant was used?" % (i_, f_),
      [v + ' mL', f_ + ' mL', addp(f_, i_) + ' mL', i_ + ' mL'],
      ["Volume used = final &minus; initial = %s &minus; %s." % (f_, i_),
       "This is the final reading, not the volume used. The buret did not start at 0.00 mL.",
       "This adds the readings; subtract the initial reading from the final one.",
       "This is just the starting reading."],
      "Volume used = final reading &minus; initial reading.",
      "%s &minus; %s = <b>%s mL</b>." % (f_, i_, v), 1, 1)

    Q(T, "A student titrating HCl with NaOH, using phenolphthalein, looks up and finds the flask a deep, dark pink. What does this mean?",
      ["The endpoint was passed: more NaOH was added than the acid needed.", "The endpoint has not been reached yet; more NaOH is needed.",
       "The flask still contains more acid than base.", "The reading is exactly at the endpoint, so the final volume is correct."],
      ["Phenolphthalein turns pink in base. The endpoint is the <i>first faint</i> pink that lasts; deep pink means extra base, so the buret reading is too large.",
       "Before the endpoint the solution stays colorless; pink means base is already in excess.",
       "Excess acid keeps phenolphthalein colorless; deep pink means excess base.",
       "The endpoint is the first faint, lasting pink. Deep pink means the student overshot it."],
      "Phenolphthalein is colorless in acid and pink in base. Which color marks the endpoint?",
      "Deep pink = excess base: <b>the endpoint was overshot</b>.", 2)

    Q(T, "Halfway through a titration, a student uses a wash bottle to rinse drops of the acid solution from the flask's walls down into the solution, adding about 15 mL of distilled water. How does this change the volume of NaOH needed to reach the endpoint?",
      ["It does not change; the moles of acid are the same.", "Less NaOH is needed, because the acid is now more dilute.",
       "More NaOH is needed, because there is more liquid in the flask.", "It doubles, because the volume in the flask went up."],
      ["The NaOH reacts with the acid, not the water. Rinsing the walls puts all the acid back into the solution, so the moles to neutralize are the same.",
       "The acid is more dilute, but there are just as many moles of it; the NaOH volume depends on moles.",
       "The water does not react with NaOH; only the moles of acid matter.",
       "Added water does not enter the calculation; the moles of acid did not change."],
      "Does the water react with the NaOH?",
      "Same moles of acid, <b>same volume of NaOH</b>.", 2)

    Vs, cb_, Vb = '35.0', '0.0950', '9.85'; mb = L(Vb) * D(cb_); v = mb / 3 / L(Vs); n = ns(Vs, cb_, Vb)
    Q(T, "A %s mL sample of lemon-lime soda needs %s mL of %s M NaOH to reach the endpoint. Assume all the acid is citric acid. What is the molarity of the citric acid? [[H3C6H5O7(aq) + 3 NaOH(aq) -> Na3C6H5O7(aq) + 3 H2O(l)]]" % (Vs, Vb, cb_),
      [S(v, n, 'M'), S(mb / L(Vs), n, 'M'), S(mb * 3 / L(Vs), n, 'M'), S(mb / 3 / L(Vb), n, 'M')],
      ["mol NaOH = %s L &times; %s M = %s mol; &divide; 3 = %s mol citric acid; &divide; %s L." % (Ls(Vb), cb_, num(mb, 4), num(mb / 3, 4), Ls(Vs)),
       "This assumes 1 : 1. Citric acid has three acidic hydrogens, so each mole uses 3 mol NaOH.",
       "This multiplies by 3; there are 3 mol NaOH per 1 mol citric acid, so divide by 3.",
       "This divides by the NaOH volume. Divide by the volume of the soda sample."],
      "Use the 1 : 3 ratio from the equation, and divide by the sample volume.",
      "%s mol &divide; %s L = <b>%s</b>." % (num(mb / 3, 4), Ls(Vs), S(v, n, 'M')), 3, 1)

    g_, ca = '0.610', '0.105'; mw = mm('CaCO3'); mo = D(g_) / mw; v = mo * 2 / D(ca) * 1000; n = ns(g_, ca)
    Q(T, "A chewable antacid tablet contains %s g of calcium carbonate, {CaCO3} (%s g/mol). What volume of %s M HCl, about the strength of stomach acid, can it neutralize? [[CaCO3(s) + 2 HCl(aq) -> CaCl2(aq) + H2O(l) + CO2(g)]]" % (g_, mw, ca),
      [S(v, n, 'mL'), S(mo / D(ca) * 1000, n, 'mL'), S(D(g_) * 2 / D(ca) * 1000, n, 'mL'), S(mo / 2 / D(ca) * 1000, n, 'mL')],
      ["%s g / %s g/mol = %s mol {CaCO3}; &times; 2 = %s mol HCl; &divide; %s M = %s L. (Context only.)" % (g_, mw, num(mo, 4), num(mo * 2, 4), ca, num(mo * 2 / D(ca), n)),
       "This skips the mole ratio; each {CaCO3} neutralizes 2 HCl.",
       "This uses grams of {CaCO3} as moles; convert with the molar mass.",
       "This flips the mole ratio; there are 2 mol HCl per mol {CaCO3}."],
      "g &rarr; mol base &rarr; mol HCl (&times; 2) &rarr; L &rarr; mL.",
      "%s mol HCl &divide; %s M = <b>%s</b>." % (num(mo * 2, 4), ca, S(v, n, 'mL')), 2, 1)

    Q(T, "Equal volumes of 0.10 M HCl and 0.10 M {H2SO4} are each titrated with the same NaOH solution. How do the volumes of NaOH compare?",
      ["The {H2SO4} needs twice as much NaOH as the HCl.", "Both need the same volume of NaOH.",
       "The HCl needs twice as much NaOH as the {H2SO4}.", "The {H2SO4} needs half as much NaOH, because it is a stronger acid."],
      ["[[H2SO4(aq) + 2 NaOH(aq) -> Na2SO4(aq) + 2 H2O(l)]] uses 2 NaOH per acid, while HCl uses 1.",
       "Same moles of acid, but {H2SO4} has two acidic hydrogens; the mole ratio is not the same.",
       "This reverses the two acids: it is {H2SO4} that gives two H<sup>+</sup>.",
       "Each {H2SO4} gives two H<sup>+</sup>, so it needs more NaOH, not less."],
      "Write both balanced equations and compare the mole ratios.",
      "Same moles of acid; {H2SO4} reacts 1 : 2 with NaOH: <b>twice as much NaOH</b>.", 2)

    # ======================= ch11-colligative (12) =======================
    T = 'ch11-colligative'
    g_, w_ = '16.3', '195.0'; mw = mm('C12H22O11'); mol = D(g_) / mw; v = mol / (D(w_) / 1000); n = ns(g_, w_)
    Q(T, "A sweet tea is made by dissolving %s g of sucrose ({C12H22O11}, %s g/mol) in %s g of water. What is the molality of the sucrose?" % (g_, mw, w_),
      [S(v, n, 'm'), S(mol / D(w_), n, 'm'), S(D(g_) / (D(w_) / 1000), n, 'm'), S(mol / ((D(g_) + D(w_)) / 1000), n, 'm')],
      ["mol sucrose = %s/%s = %s mol; kg water = %s kg; m = mol / kg solvent." % (g_, mw, num(mol, 4), num(D(w_) / 1000, 4)),
       "This divides by grams of water; molality uses kilograms of solvent.",
       "This uses grams of sucrose instead of moles.",
       "This divides by the mass of the whole solution; molality uses only the solvent."],
      "m = mol solute / kg solvent.",
      "%s mol / %s kg = <b>%s</b>." % (num(mol, 4), num(D(w_) / 1000, 4), S(v, n, 'm')), 2, 1)

    Q(T, "Which solute has a van 't Hoff factor of i = 3 in water (assuming complete dissociation)?",
      ["{Na2SO4}", "KBr", "{AlCl3}", "glucose, {C6H12O6}"],
      ["{Na2SO4} &rarr; 2 Na<sup>+</sup> + SO<sub>4</sub><sup>2&minus;</sup>: three particles (i = 3). The sulfate ion stays together as one particle.",
       "KBr &rarr; K<sup>+</sup> + Br<sup>&minus;</sup>: two particles (i = 2).",
       "{AlCl3} &rarr; Al<sup>3+</sup> + 3 Cl<sup>&minus;</sup>: four particles (i = 4).",
       "Glucose is a nonelectrolyte and stays as one molecule (i = 1)."],
      "Write the dissociation and count the ions.",
      "<b>{Na2SO4}</b> gives 2 Na<sup>+</sup> + 1 SO<sub>4</sub><sup>2&minus;</sup> = 3 particles.", 2)

    m_ = '0.155'; v = D(m_) * 3 * 1000
    Q(T, "What is the osmolality of a %s m {CaCl2} solution, assuming complete dissociation? Give the answer in mOsm/kg." % m_,
      [S(v, 3, 'mOsm/kg'), S(D(m_) * 1000, 3, 'mOsm/kg'), S(D(m_) * 2 * 1000, 3, 'mOsm/kg'), S(D(m_) * 3, 3, 'mOsm/kg')],
      ["{CaCl2} &rarr; Ca<sup>2+</sup> + 2 Cl<sup>&minus;</sup>, so i = 3: osmolality = 3 &times; %s = %s Osm/kg." % (m_, num(D(m_) * 3, 3)),
       "This forgets i; {CaCl2} gives three particles per formula unit.",
       "This uses i = 2, as for NaCl. {CaCl2} gives 1 Ca<sup>2+</sup> and 2 Cl<sup>&minus;</sup>.",
       "This is in Osm/kg; multiply by 1000 to get mOsm/kg."],
      "Osmolality = i &times; m; 1 Osm = 1000 mOsm.",
      "3 &times; %s = %s Osm/kg = <b>%s</b>." % (m_, num(D(m_) * 3, 3), S(v, 3, 'mOsm/kg')), 2, 1)

    m_ = '0.425'; dT = 2 * KF * D(m_)
    Q(T, "What is the freezing point of a %s m KBr solution in water? (K<sub>f</sub> = 1.86 °C/m)" % m_,
      [tf(dT) + ' °C', qd(dT, 2) + ' °C', tf(KF * D(m_)) + ' °C', tf(2 * KB * D(m_)) + ' °C'],
      ["KBr gives 2 ions (i = 2): &Delta;T<sub>f</sub> = (2)(1.86)(%s) = %s °C; 0.00 &minus; %s." % (m_, num(dT, 3), num(dT, 3)),
       "This adds &Delta;T<sub>f</sub> to the freezing point. Dissolved particles <i>lower</i> the freezing point.",
       "This forgets i. KBr gives two particles, K<sup>+</sup> and Br<sup>&minus;</sup>.",
       "This uses K<sub>b</sub> = 0.512, the boiling point constant. Use K<sub>f</sub> = 1.86 for freezing."],
      "&Delta;T<sub>f</sub> = iK<sub>f</sub>m; subtract from 0.00 °C.",
      "&Delta;T<sub>f</sub> = %s °C; T<sub>f</sub> = <b>%s °C</b>." % (num(dT, 3), tf(dT)), 2, 1)

    m_ = '2.35'; dT = KB * D(m_)
    Q(T, "Antifreeze is a solution of ethylene glycol ({C2H6O2}), a nonelectrolyte, in water. What is the boiling point of a %s m ethylene glycol solution at 1 atm? (K<sub>b</sub> = 0.512 °C/m)" % m_,
      [tb(dT) + ' °C', tb(KF * D(m_)) + ' °C', qd(D('100.00') - dT, 2) + ' °C', tb(2 * dT) + ' °C'],
      ["Nonelectrolyte, i = 1: &Delta;T<sub>b</sub> = (0.512)(%s) = %s °C; 100.00 + %s." % (m_, num(dT, 3), num(dT, 3)),
       "This uses K<sub>f</sub> = 1.86, the freezing point constant.",
       "This subtracts &Delta;T<sub>b</sub>; dissolved particles <i>raise</i> the boiling point.",
       "This uses i = 2; ethylene glycol is molecular and stays as one particle."],
      "&Delta;T<sub>b</sub> = iK<sub>b</sub>m; add to 100.00 °C.",
      "&Delta;T<sub>b</sub> = %s °C; T<sub>b</sub> = <b>%s °C</b>." % (num(dT, 3), tb(dT)), 2, 1)

    Q(T, "Use the table. Which aqueous solution freezes closest to 0 °C (has the <b>highest</b> freezing point)?",
      ["glucose", "{AlCl3}", "NaCl", "{CaCl2}"],
      ["Glucose has the largest molality, but it is a nonelectrolyte (i = 1): only 0.20 m of particles, the fewest, so its freezing point drops the least.",
       "{AlCl3} has the smallest molality, but it gives 4 ions: 4 &times; 0.080 = 0.32 m of particles.",
       "NaCl gives 2 ions: 2 &times; 0.15 = 0.30 m of particles.",
       "{CaCl2} gives 3 ions: 3 &times; 0.12 = 0.36 m of particles, the most, so it freezes lowest, farthest from 0 °C."],
      "Multiply each molality by i. Fewer particles, smaller freezing point depression.",
      "i &times; m: 0.20 (glucose) &lt; 0.30 (NaCl) &lt; 0.32 ({AlCl3}) &lt; 0.36 ({CaCl2}): <b>glucose</b> freezes closest to 0 °C.", 3, 0,
      [{"type": "table", "cap": "Four aqueous solutions", "head": ["Solute", "Molality (m)"],
        "rows": [["NaCl", "0.15"], ["{CaCl2}", "0.12"], ["glucose", "0.20"], ["{AlCl3}", "0.080"]]}])

    Q(T, "Why is molality, not molarity, used for freezing point and boiling point calculations?",
      ["Molality uses the mass of solvent, which does not change with temperature; volumes expand and contract.",
       "Molality counts the ions, while molarity counts formula units.",
       "Molality is always larger than molarity, which makes the changes easier to measure.",
       "Molarity cannot be used for aqueous solutions."],
      ["Freezing and boiling points are measured as the temperature changes; a mass-based unit stays the same while the solution's volume changes.",
       "Neither unit counts ions; the van 't Hoff factor i does that.",
       "For dilute water solutions the two are nearly equal; size is not the reason.",
       "Molarity is used for aqueous solutions all the time, for example in titrations."],
      "What happens to a volume when the temperature changes?",
      "<b>Mass does not change with temperature</b>, but volume does.", 2)

    Q(T, "A membrane that lets only water pass separates 5% glucose (side A) from 10% glucose (side B). Which way does water flow by osmosis?",
      ["From side A to side B, toward the higher solute concentration", "From side B to side A, toward the lower solute concentration",
       "Glucose moves from side B to side A until both are 7.5%", "No water moves, because both sides contain glucose"],
      ["Water flows from lower solute concentration to higher: &ldquo;water follows solute.&rdquo;",
       "This reverses osmosis. Water moves toward the side with more dissolved particles.",
       "The membrane blocks glucose; only water can cross.",
       "Water moves whenever the particle concentrations differ; here they do."],
      "Water follows solute.",
      "Water moves toward the more concentrated side: <b>from A to B</b>.", 1)

    Q(T, "In the emergency department, Mateo Herrera, who has asthma, receives 0.9% NaCl (normal saline) by IV. Relative to his red blood cells, how is this fluid described?",
      ["Isotonic: no net water flow, so the cells keep their shape", "Hypotonic: water flows into the cells, and they swell",
       "Hypertonic: water flows out of the cells, and they shrink", "Hypertonic: water flows into the cells, and they burst"],
      ["Normal saline has about the same particle concentration as plasma, so it adds volume to the blood without moving much water into or out of cells. (Context only; IV fluids are given as ordered.)",
       "Hypotonic fluids, such as 0.45% NaCl, have a lower particle concentration than cells; 0.9% NaCl matches them.",
       "Hypertonic fluids, such as 3% NaCl, have a higher particle concentration than cells.",
       "In a hypertonic fluid water flows <i>out</i> of cells; and 0.9% NaCl is not hypertonic."],
      "Compare 0.9% NaCl with the particle concentration inside red blood cells.",
      "0.9% NaCl is <b>isotonic</b>: no net water flow.", 1)

    g_, w_ = '1.45', '125.0'; mw = mm('MgCl2'); mol = D(g_) / mw; mo = mol / (D(w_) / 1000); v = mo * 3 * 1000; n = ns(g_, w_)
    Q(T, "A solution is made by dissolving %s g of {MgCl2} (%s g/mol) in %s g of water. What is its osmolality in mOsm/kg, assuming complete dissociation?" % (g_, mw, w_),
      [S(v, n, 'mOsm/kg'), S(mo * 1000, n, 'mOsm/kg'), S(mo * 2 * 1000, n, 'mOsm/kg'), S(mo * 3, n, 'mOsm/kg')],
      ["mol = %s/%s = %s mol; m = %s mol / %s kg = %s m; {MgCl2} gives 3 ions (i = 3), so osmolality = 3 &times; %s Osm/kg. This solution is hypertonic compared with serum (275&ndash;295 mOsm/kg)." % (g_, mw, num(mol, 4), num(mol, 4), num(D(w_) / 1000, 4), num(mo, 4), num(mo, 4)),
       "This forgets i; {MgCl2} gives Mg<sup>2+</sup> + 2 Cl<sup>&minus;</sup>, three particles.",
       "This uses i = 2; {MgCl2} gives three ions, not two.",
       "This is the answer in Osm/kg; multiply by 1000 mOsm/Osm."],
      "Molality first, then &times; i, then &times; 1000 mOsm/Osm.",
      "m = %s m; 3 &times; %s = <b>%s</b>." % (num(mo, n), num(mo, n), S(v, n, 'mOsm/kg')), 3, 1)

    Q(T, "Red blood cells are placed in seawater, which is about 1000 mOsm/kg. What happens to them?",
      ["Water flows out of the cells, and they shrink (crenation).", "Water flows into the cells, and they burst (hemolysis).",
       "Nothing; seawater is isotonic with blood.", "Salt flows into the cells until they burst."],
      ["Seawater is hypertonic (far above 275&ndash;295 mOsm/kg), so water leaves the cells toward the higher particle concentration.",
       "This is what happens in a <i>hypotonic</i> solution, such as pure water.",
       "Blood is about 275&ndash;295 mOsm/kg; seawater is more than three times that.",
       "Osmosis moves water across the membrane; the salt is largely held back."],
      "Compare 1000 mOsm/kg with blood's 275&ndash;295 mOsm/kg, then remember that water follows solute.",
      "Hypertonic: water leaves, and the cells <b>shrink (crenation)</b>.", 1)

    Tf = '5.00'; v = D(Tf) / (2 * KF)
    Q(T, "Highway crews spread NaCl on the road to Shaver Lake. What molality of NaCl solution freezes at &minus;5.00 °C, assuming complete dissociation? (K<sub>f</sub> = 1.86 °C/m)",
      [S(v, 3, 'm'), S(D(Tf) / KF, 3, 'm'), S(D(Tf) / (2 * KB), 3, 'm'), S(2 * KF * D(Tf), 3, 'm')],
      ["&Delta;T<sub>f</sub> = 5.00 °C; NaCl gives 2 ions (i = 2); m = &Delta;T<sub>f</sub> / (iK<sub>f</sub>) = 5.00 / (2 &times; 1.86).",
       "This forgets i; each NaCl gives two particles, so half this molality is enough.",
       "This uses K<sub>b</sub> = 0.512; freezing point depression uses K<sub>f</sub> = 1.86.",
       "This multiplies by iK<sub>f</sub>; solve &Delta;T<sub>f</sub> = iK<sub>f</sub>m for m by dividing."],
      "Solve &Delta;T<sub>f</sub> = iK<sub>f</sub>m for m.",
      "m = 5.00 / (2 &times; 1.86) = <b>%s</b>." % S(v, 3, 'm'), 3, 1)


if __name__ == '__main__':
    build()
    dump(sys.argv[1])
