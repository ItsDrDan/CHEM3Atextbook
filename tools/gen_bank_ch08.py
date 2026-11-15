#!/usr/bin/env python3
"""Builds bank/ch08.json (Chapter 8 Try It items: mole ratios, mass-to-mass, solutions and gases, limiting reactant,
theoretical and percent yield, enthalpy of reaction). Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch08.py bank/ch08.json
Atomic masses: tools/yellow_sheet_masses.json (strings, printed decimals). Molar mass = sum of the atomic masses
(subscripts exact), rounded once to the fewest decimal places of the masses used. Molar volume at STP 22.4 L/mol.
Delta H values: only CH4 -890.3 kJ, glucose -2803 kJ, 2 H2 + O2 -> 2 H2O(l) -571.6 kJ, C3H8 -2220 kJ (written
-2.220 x 10^3 kJ, course trailing-zero rule), CaCO3 -> CaO + CO2 +178 kJ, or values given in the stem.
Answers: multiplication/division sig figs from the givens (trailing zeros without a decimal point are not
significant; mole ratios are exact), subtraction by decimal places, rounded once at the end.
Markup: {Ca(NO3)2} formula, [[2 H2(g) + O2(g) -> 2 H2O(l)]] equation (coefficients as separate tokens).
Every number is recomputed independently by tools/check_bank_ch08.py."""
import json, sys, re, os, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
MS = json.load(open(os.path.join(HERE, 'yellow_sheet_masses.json')))['masses']
M = '&minus;'
B = []
PREFIX = 'c8-%03d'

# ---------------- formulas and equations ----------------
def F(s):
    ch = ''
    if '^' in s: s, ch = s.split('^')
    parts = [re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', p) for p in s.split('.')]
    out = '&middot;'.join(parts)
    if ch: out += '<sup>' + ch.replace('-', M) + '</sup>'
    return out
SP = re.compile(r'^(.*?)(\((?:s|l|g|aq)\))?$')
def EQ(s):
    out = []
    for tok in s.split():
        if tok == '->': out.append('&rarr;')
        elif tok == '+': out.append('+')
        elif re.fullmatch(r'\d+', tok): out.append(tok)
        else:
            m = SP.match(tok); out.append(F(m.group(1)) + (m.group(2) or ''))
    return ' '.join(out)
def X(s):
    s = re.sub(r'\[\[(.+?)\]\]', lambda m: EQ(m.group(1)), s)
    return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)

def parse(f):
    tot = collections.OrderedDict()
    for part in f.split('.'):
        m = re.match(r'(\d*)(.*)$', part); mult = int(m.group(1) or 1); s = m.group(2)
        stack = [collections.OrderedDict()]; i = 0
        while i < len(s):
            if s[i] == '(':
                stack.append(collections.OrderedDict()); i += 1
            elif s[i] == ')':
                j = i + 1
                while j < len(s) and s[j].isdigit(): j += 1
                n = int(s[i + 1:j] or 1); g = stack.pop()
                for k, v in g.items(): stack[-1][k] = stack[-1].get(k, 0) + v * n
                i = j
            else:
                m2 = re.match(r'([A-Z][a-z]?)(\d*)', s[i:]); el, n = m2.group(1), int(m2.group(2) or 1)
                stack[-1][el] = stack[-1].get(el, 0) + n; i += m2.end()
        for k, v in stack[0].items(): tot[k] = tot.get(k, 0) + v * mult
    return tot
def dp(s): return len(s.split('.')[1]) if '.' in s else 0
def mm(f):
    q = min(dp(MS[e]) for e in parse(f))
    return sum(D(MS[e]) * n for e, n in parse(f).items()).quantize(D(1).scaleb(-q), rounding=ROUND_HALF_UP)
def G(f): return str(mm(f))
def MMS(*fs): return '(' + '; '.join('{%s} %s g/mol' % (f, G(f)) for f in fs) + ')'

# ---------------- numbers ----------------
def num(x, n=3):
    x = D(x); e = x.adjusted()
    m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if m >= 10:
        e += 1; m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if -3 <= e <= n - 1:
        s = format(m.scaleb(e).quantize(D(1).scaleb(min(0, e - n + 1))), 'f')
        if e == n - 1 and s.endswith('0'): s += '.'
        return s
    return '%s &times; 10<sup>%s</sup>' % (m, (M + str(-e)) if e < 0 else str(e))
def rnd(x, n=3):
    """x rounded to n sig figs, as a Decimal (for a later subtraction)."""
    x = D(x); return x.quantize(D(1).scaleb(x.adjusted() - n + 1), rounding=ROUND_HALF_UP)
def subt(a, b):
    """a - b by the decimal-place rule (a, b as Decimals already rounded)."""
    q = min(-a.as_tuple().exponent, -b.as_tuple().exponent)
    return format((a - b).quantize(D(1).scaleb(-q), rounding=ROUND_HALF_UP), 'f')
def pct(x, n=3): return num(x * 100, n) + '%'
DH = lambda v: '&Delta;H = ' + v + ' kJ'
PROPANE = M + '2.220 &times; 10<sup>3</sup>'

def Q(t, q, c, y, h, w, d, k=0, f=None):
    it = {"id": PREFIX % (len(B) + 1), "t": t, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    if f:
        for fg in f:
            if fg['type'] == 'table':
                fg['head'] = [X(x) for x in fg['head']]; fg['rows'] = [[X(x) for x in r] for r in fg['rows']]
                if fg.get('cap'): fg['cap'] = X(fg['cap'])
        it["f"] = f
    B.append(it)

# ======================= ch08-moleratio (11) =======================
T = 'ch08-moleratio'
Q(T, "In the balanced equation [[2 H2(g) + O2(g) -> 2 H2O(l)]], what do the coefficients tell you?",
  ["2 mol of {H2} react with 1 mol of {O2} to make 2 mol of {H2O}.",
   "2 g of {H2} react with 1 g of {O2} to make 2 g of {H2O}.",
   "2 molecules of {H2} and 1 molecule of {O2} make 3 molecules of {H2O}.",
   "Each {H2O} molecule has 2 H atoms and 1 O atom, so the coefficients repeat the subscripts."],
  ["Coefficients count particles, and the same ratio holds for moles: 2 mol {H2} : 1 mol {O2} : 2 mol {H2O}.",
   "Coefficients are not masses. An {O2} molecule is about 16 times heavier than an {H2} molecule, so equal-looking numbers of grams do not match the recipe.",
   "Coefficients on the two sides are not added together. The equation says 2 {H2} + 1 {O2} make 2 {H2O}; atoms are conserved, molecules are not.",
   "Subscripts describe one molecule; coefficients count how many molecules (or moles) take part. They are different numbers with different jobs."],
  "Coefficients count particles. What do you get if you multiply each one by Avogadro's number?",
  "Coefficients are mole ratios: <b>2 mol {H2} react with 1 mol {O2} to make 2 mol {H2O}</b>.", 1)

Q(T, "For the combustion of propane, [[C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(l)]], which conversion factor turns moles of {O2} into moles of {CO2}?",
  ["3 mol {CO2} / 5 mol {O2}", "5 mol {O2} / 3 mol {CO2}", "2 mol {CO2} / 2 mol {O2}", "3 mol {CO2} / 1 mol {C3H8}"],
  ["The coefficients of {CO2} (3) and {O2} (5) make the ratio, with the wanted unit, mol {CO2}, on top so mol {O2} cancels.",
   "This is the right pair of coefficients, but upside down: mol {O2} would not cancel.",
   "These are the subscripts in the formulas, not the coefficients. Mole ratios come from coefficients.",
   "This ratio is correct for the equation, but it converts moles of propane, not moles of {O2}."],
  "Put the substance you want on top and the substance you have on the bottom.",
  "mol {O2} &times; <b>(3 mol {CO2} / 5 mol {O2})</b> = mol {CO2}.", 1)

x = D('3.60') * 5 / 4
Q(T, "Nitric acid for fertilizer is made from ammonia. The first step is [[4 NH3(g) + 5 O2(g) -> 4 NO(g) + 6 H2O(g)]]. How many moles of {O2} react with 3.60 mol of {NH3}?",
  [num(x) + " mol {O2}", num(D('3.60') * 4 / 5) + " mol {O2}", "3.60 mol {O2}", num(D('3.60') * 6 / 4) + " mol {O2}"],
  ["3.60 mol {NH3} &times; (5 mol {O2} / 4 mol {NH3}). The equation uses more {O2} than {NH3}, so the answer is larger than 3.60.",
   "This uses 4/5, the ratio upside down. Put mol {O2} on top.",
   "This skips the mole ratio. The coefficients of {NH3} and {O2} are not equal.",
   "This uses the coefficient of {H2O} (6) instead of {O2} (5)."],
  "Which two coefficients belong in the ratio?",
  "3.60 mol {NH3} &times; (5 mol {O2} / 4 mol {NH3}) = <b>" + num(x) + " mol {O2}</b>. The mole ratio is exact, so the answer keeps the 3 significant figures of 3.60.", 1, 1)

x = D('0.480') / 6
Q(T, "In cellular respiration, [[C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O]]. How many moles of glucose are used when your cells produce 0.480 mol of {CO2}?",
  [num(x) + " mol {C6H12O6}", num(D('0.480') * 6) + " mol {C6H12O6}", "0.480 mol {C6H12O6}", num(x * mm('C6H12O6')) + " g {C6H12O6}"],
  ["0.480 mol {CO2} &times; (1 mol glucose / 6 mol {CO2}). Each glucose makes six {CO2}, so far fewer moles of glucose are needed.",
   "This multiplies by 6, the ratio upside down. One glucose makes six {CO2}, not the other way around.",
   "This skips the mole ratio; the coefficients of glucose (1) and {CO2} (6) differ.",
   "This goes one step too far, multiplying by the molar mass of glucose (180.156 g/mol). The question asks for moles."],
  "One glucose molecule makes how many {CO2} molecules?",
  "0.480 mol {CO2} &times; (1 mol {C6H12O6} / 6 mol {CO2}) = <b>" + num(x) + " mol {C6H12O6}</b>.", 2, 1)

x = D('0.856') / 2
Q(T, "Hydrogen peroxide foams on a cut because an enzyme in blood (catalase) speeds up [[2 H2O2(aq) -> 2 H2O(l) + O2(g)]]. How many moles of {O2} form from 0.856 mol of {H2O2}?",
  [num(x) + " mol {O2}", num(D('0.856') * 2) + " mol {O2}", "0.856 mol {O2}", num(x * mm('O2')) + " g {O2}"],
  ["0.856 mol {H2O2} &times; (1 mol {O2} / 2 mol {H2O2}): half as many moles of {O2} as {H2O2}.",
   "This uses 2/1, the ratio upside down. Two {H2O2} make one {O2}.",
   "This skips the mole ratio. The coefficients of {H2O2} and {O2} are 2 and 1.",
   "This converts on to grams with 31.998 g/mol. The question asks for moles of {O2}."],
  "Two {H2O2} molecules make how many {O2} molecules?",
  "0.856 mol {H2O2} &times; (1 mol {O2} / 2 mol {H2O2}) = <b>" + num(x) + " mol {O2}</b>.", 1, 1)

Q(T, "For [[2 Mg(s) + O2(g) -> 2 MgO(s)]], a student says, &ldquo;2 g of Mg react with 1 g of {O2}.&rdquo; Which statement corrects the student?",
  ["2 mol of Mg (48.62 g) react with 1 mol of {O2} (31.998 g); coefficients are mole ratios, not mass ratios.",
   "The student is right; coefficients give the ratio of grams.",
   "2 g of Mg react with 2 g of {O2}, because the product has 2 MgO.",
   "1 g of Mg reacts with 2 g of {O2}, because {O2} has two atoms."],
  ["Coefficients count moles. 2 mol Mg &times; 24.31 g/mol = 48.62 g and 1 mol {O2} = 31.998 g, so the mass ratio is not 2 : 1.",
   "Coefficients are particle and mole ratios. Mg atoms and {O2} molecules have different masses, so grams do not follow the coefficients.",
   "The product's coefficient does not set the mass of a reactant, and grams do not follow coefficients.",
   "The subscript in {O2} is part of the formula; it does not change the mole ratio, which is 2 Mg : 1 {O2}."],
  "Do 1 mol of Mg and 1 mol of {O2} have the same mass?",
  "The equation means <b>2 mol Mg (2 &times; 24.31 = 48.62 g) react with 1 mol {O2} (31.998 g)</b>. Coefficients are mole ratios; to compare masses, use molar masses.", 2)

Q(T, "In [[N2(g) + 3 H2(g) -> 2 NH3(g)]], 4 mol of reactant molecules make only 2 mol of product. What is conserved in this reaction?",
  ["The number of each kind of atom, and so the total mass", "The total number of moles of molecules",
   "The number of molecules of each substance", "Nothing; 2 mol of product weighs less than 4 mol of reactants"],
  ["2 N and 6 H atoms are on each side, so the mass of 1 mol {N2} + 3 mol {H2} (34.062 g) equals the mass of 2 mol {NH3} (34.062 g).",
   "Moles of molecules are not conserved: 1 + 3 = 4 mol become 2 mol, because atoms regroup into bigger molecules.",
   "Molecules are broken apart and rebuilt; {N2} and {H2} are used up and {NH3} forms.",
   "Mass is always conserved. Fewer, heavier {NH3} molecules have the same total mass as the reactants."],
  "Count the N and H atoms on each side.",
  "Atoms are rearranged, not created or destroyed, so <b>atoms and mass are conserved</b>; moles of molecules are not (4 mol &rarr; 2 mol).", 2)

x = D('1.25') * 3 / 2
Q(T, "In a blast furnace, iron ore is reduced by carbon monoxide: [[Fe2O3(s) + 3 CO(g) -> 2 Fe(l) + 3 CO2(g)]]. How many moles of CO are needed to produce 1.25 mol of Fe?",
  [num(x) + " mol CO", num(D('1.25') * 2 / 3) + " mol CO", "1.25 mol CO", num(D('1.25') / 2) + " mol CO"],
  ["1.25 mol Fe &times; (3 mol CO / 2 mol Fe). The equation needs 3 CO for every 2 Fe, so more than 1.25 mol.",
   "This uses 2/3, the ratio upside down. mol Fe would not cancel.",
   "This skips the mole ratio; the coefficients of CO and Fe are 3 and 2.",
   "This is the moles of {Fe2O3} needed (1 {Fe2O3} : 2 Fe), not the moles of CO."],
  "Set up mol Fe &times; (mol CO / mol Fe).",
  "1.25 mol Fe &times; (3 mol CO / 2 mol Fe) = <b>" + num(x) + " mol CO</b>.", 2, 1)

x = D('2.46') * 5 / 4
Q(T, "A propane camp stove burns fuel by [[C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(l)]]. How many moles of {O2} were used if 2.46 mol of {H2O} formed?",
  [num(x) + " mol {O2}", num(D('2.46') * 4 / 5) + " mol {O2}", num(D('2.46') / 4) + " mol {O2}", "2.46 mol {O2}"],
  ["2.46 mol {H2O} &times; (5 mol {O2} / 4 mol {H2O}). Any two substances in a balanced equation can be linked by a mole ratio, even a product and a reactant.",
   "This uses 4/5, the ratio upside down.",
   "This is the moles of propane burned (1 {C3H8} : 4 {H2O}), not the moles of {O2}.",
   "This skips the mole ratio; the coefficients of {O2} (5) and {H2O} (4) differ."],
  "Link {H2O} directly to {O2} with their coefficients.",
  "2.46 mol {H2O} &times; (5 mol {O2} / 4 mol {H2O}) = <b>" + num(x) + " mol {O2}</b>.", 3, 1)

x = D('0.80') * 3 / 4
Q(T, "The table follows the mole ratio of [[4 Al(s) + 3 O2(g) -> 2 Al2O3(s)]], which forms the thin oxide layer that protects aluminum. What belongs in the cell marked ?",
  [num(x, 2) + " mol {O2}", num(D('0.80') * 4 / 3, 2) + " mol {O2}", num(D('0.80') * 2 / 4, 2) + " mol {O2}", "0.80 mol {O2}"],
  ["0.80 mol Al &times; (3 mol {O2} / 4 mol Al) = 0.60 mol, the same 4 : 3 pattern as the rows above.",
   "This uses 4/3, the ratio upside down; Al needs fewer moles of {O2} than of Al.",
   "This uses the coefficient of {Al2O3} (2) instead of {O2} (3).",
   "This skips the mole ratio; the rows above show the moles of {O2} are not equal to the moles of Al."],
  "Check the pattern in the first two rows: what do you multiply mol Al by to get mol {O2}?",
  "mol {O2} = mol Al &times; 3/4, so 0.80 &times; 3/4 = <b>" + num(x, 2) + " mol {O2}</b>.", 2, 1,
  [{"type": "table", "cap": "Moles of Al and {O2} that react", "head": ["Trial", "mol Al", "mol {O2}"],
    "rows": [["1", "4.0", "3.0"], ["2", "2.0", "1.5"], ["3", "0.80", "?"]]}])

Q(T, "For octane in gasoline, [[2 C8H18(l) + 25 O2(g) -> 16 CO2(g) + 18 H2O(g)]]. A student converts 0.3150 mol {O2} to moles of {CO2} with the factor 16 mol {CO2} / 25 mol {O2}. How many significant figures should the answer have?",
  ["4, set by 0.3150; the mole ratio is exact", "2, set by the 16 and the 25 in the ratio",
   "1, because 16/25 is less than 1", "5, because the ratio has 5 digits in total"],
  ["Coefficients are exact counts from a balanced equation, so they never limit significant figures. Only the measured 0.3150 (4 significant figures) does.",
   "Coefficients are exact numbers, not measurements, so they have unlimited significant figures.",
   "The size of a number does not set its significant figures, and exact ratios do not limit the answer.",
   "Digits of exact numbers are not counted; only the measured given limits the answer."],
  "Is a coefficient a measured number or an exact count?",
  "Mole ratios are exact, so <b>4 significant figures</b>, like 0.3150: 0.3150 &times; 16/25 = 0.2016 mol {CO2}.", 3)

# ======================= ch08-massmass (13) =======================
T = 'ch08-massmass'
n_ = D('75.0') / mm('C6H12O6')
x = n_ * 2 * mm('C2H5OH')
Q(T, "Yeast ferment grape sugar into wine: [[C6H12O6(aq) -> 2 C2H5OH(aq) + 2 CO2(g)]]. What mass of ethanol can form from 75.0 g of glucose? " + MMS('C6H12O6', 'C2H5OH'),
  [num(x) + " g {C2H5OH}", num(n_ * mm('C2H5OH')) + " g {C2H5OH}", num(n_ * 2 * 2 * mm('C2H5OH')) + " g {C2H5OH}", num(n_ * 2) + " mol {C2H5OH}"],
  ["75.0 g &divide; 180.156 g/mol = 0.4163 mol glucose; &times; 2 = 0.8326 mol ethanol; &times; 46.069 g/mol.",
   "This skips the mole ratio. Each glucose makes 2 ethanol molecules.",
   "This doubles twice: the coefficient 2 belongs in the mole ratio only, not in the molar mass. The molar mass of ethanol is 46.069 g/mol however many moles react.",
   "This stops at moles of ethanol. One more step, with the molar mass, gives grams."],
  "g glucose &rarr; mol glucose &rarr; mol ethanol &rarr; g ethanol.",
  "75.0 g &times; (1 mol / 180.156 g) &times; (2 mol {C2H5OH} / 1 mol {C6H12O6}) &times; (46.069 g / 1 mol) = <b>" + num(x) + " g {C2H5OH}</b>.", 2, 1)

n_ = D('0.750') / mm('CaCO3')
x = n_ * 2 * mm('HCl')
Q(T, "An antacid tablet contains 0.750 g of calcium carbonate, which neutralizes stomach acid: [[CaCO3(s) + 2 HCl(aq) -> CaCl2(aq) + H2O(l) + CO2(g)]]. What mass of HCl can it neutralize? " + MMS('CaCO3', 'HCl'),
  [num(x) + " g HCl", num(n_ * mm('HCl')) + " g HCl", num(n_ / 2 * mm('HCl')) + " g HCl", "1.50 g HCl"],
  ["0.750 g &divide; 100.09 g/mol = 0.007493 mol {CaCO3}; &times; 2 = 0.01499 mol HCl; &times; 36.46 g/mol.",
   "This skips the mole ratio: one {CaCO3} neutralizes two HCl.",
   "This uses 1/2, the ratio upside down.",
   "This multiplies the grams by the coefficient. Grams must be converted to moles before a mole ratio can be used."],
  "Convert grams of {CaCO3} to moles before you use the 1 : 2 ratio.",
  "0.750 g {CaCO3} &times; (1 mol / 100.09 g) &times; (2 mol HCl / 1 mol {CaCO3}) &times; (36.46 g / 1 mol) = <b>" + num(x) + " g HCl</b>. (Context only; follow the label.)", 2, 1)

n_ = D('85.0') / mm('NH3')
x = n_ * 3 / 2 * mm('H2')
Q(T, "Valley farms rely on ammonia fertilizer made by [[N2(g) + 3 H2(g) -> 2 NH3(g)]]. What mass of {H2} is needed to make 85.0 g of {NH3}? " + MMS('NH3', 'H2'),
  [num(x) + " g {H2}", num(n_ * mm('H2')) + " g {H2}", num(n_ * 2 / 3 * mm('H2')) + " g {H2}", num(n_ * 3 / 2 * mm('H')) + " g {H2}"],
  ["85.0 g &divide; 17.031 g/mol = 4.991 mol {NH3}; &times; 3/2 = 7.486 mol {H2}; &times; 2.016 g/mol.",
   "This skips the mole ratio (3 {H2} : 2 {NH3}).",
   "This uses 2/3, the ratio upside down.",
   "This uses 1.008 g/mol, the mass of H atoms. Hydrogen gas is diatomic, {H2}, 2.016 g/mol."],
  "Work backward from the product: g {NH3} &rarr; mol {NH3} &rarr; mol {H2} &rarr; g {H2}.",
  "85.0 g {NH3} &times; (1 mol / 17.031 g) &times; (3 mol {H2} / 2 mol {NH3}) &times; (2.016 g / 1 mol) = <b>" + num(x) + " g {H2}</b>.", 2, 1)

n_ = D('16.5') / mm('C6H12O6')
x = n_ * 6 * mm('O2')
Q(T, "What mass of {O2} must you breathe in to fully oxidize 16.5 g of glucose? [[C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O]] " + MMS('C6H12O6', 'O2'),
  [num(x) + " g {O2}", num(n_ * mm('O2')) + " g {O2}", num(n_ * 6 * mm('O')) + " g {O2}", num(n_ / 6 * mm('O2')) + " g {O2}"],
  ["16.5 g &divide; 180.156 g/mol = 0.09159 mol glucose; &times; 6 = 0.5495 mol {O2}; &times; 31.998 g/mol.",
   "This skips the mole ratio: each glucose needs 6 {O2}.",
   "This uses 15.999 g/mol, the mass of O atoms. Oxygen gas is {O2}, 31.998 g/mol.",
   "This uses 1/6, the ratio upside down."],
  "How many {O2} does one glucose need?",
  "16.5 g &times; (1 mol / 180.156 g) &times; (6 mol {O2} / 1 mol {C6H12O6}) &times; (31.998 g / 1 mol) = <b>" + num(x) + " g {O2}</b>.", 2, 1)

n_ = D('3.65') / mm('Mg')
x = n_ * mm('MgO')
Q(T, "Magnesium ribbon burns with a bright white flame: [[2 Mg(s) + O2(g) -> 2 MgO(s)]]. What mass of MgO forms from 3.65 g of Mg? " + MMS('Mg', 'MgO'),
  [num(x) + " g MgO", "3.65 g MgO", num(n_ * 2 * mm('MgO')) + " g MgO", num(n_) + " mol MgO"],
  ["3.65 g &divide; 24.31 g/mol = 0.1501 mol Mg; the ratio is 2 : 2 (1 : 1), so 0.1501 mol MgO; &times; 40.31 g/mol.",
   "Mass is conserved for the whole reaction, but MgO also contains oxygen from the air, so it weighs more than the Mg alone.",
   "This multiplies the molar mass of MgO by its coefficient. The 2 belongs in the mole ratio (2 Mg : 2 MgO), and it cancels there.",
   "This stops at moles. Multiply by 40.31 g/mol to get grams."],
  "The mole ratio here is 2 : 2. What does that simplify to?",
  "3.65 g Mg &times; (1 mol / 24.31 g) &times; (2 mol MgO / 2 mol Mg) &times; (40.31 g / 1 mol) = <b>" + num(x) + " g MgO</b>.", 1, 1)

n_ = D('26.5') / mm('C3H8')
x = n_ * 3 * mm('CO2')
Q(T, "Many rural Valley homes heat with propane: [[C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(l)]]. What mass of {CO2} forms when 26.5 g of propane burns? " + MMS('C3H8', 'CO2'),
  [num(x) + " g {CO2}", num(n_ * mm('CO2')) + " g {CO2}", num(n_ / 3 * mm('CO2')) + " g {CO2}", num(n_ * 3 * 3 * mm('CO2')) + " g {CO2}"],
  ["26.5 g &divide; 44.097 g/mol = 0.6009 mol propane; &times; 3 = 1.803 mol {CO2}; &times; 44.009 g/mol.",
   "This skips the mole ratio. Propane and {CO2} have nearly the same molar mass, but each propane makes 3 {CO2}.",
   "This uses 1/3, the ratio upside down.",
   "This uses the 3 twice: once in the mole ratio and again on the molar mass of {CO2}."],
  "One propane molecule has 3 C atoms. How many {CO2} does it make?",
  "26.5 g {C3H8} &times; (1 mol / 44.097 g) &times; (3 mol {CO2} / 1 mol {C3H8}) &times; (44.009 g / 1 mol) = <b>" + num(x) + " g {CO2}</b>.", 2, 1)

n_ = D('8.40') / mm('Fe')
x = n_ * 3 / 4 * mm('O2')
Q(T, "Iron rusts by [[4 Fe(s) + 3 O2(g) -> 2 Fe2O3(s)]]. What mass of {O2} is used when 8.40 g of iron rusts completely? " + MMS('Fe', 'O2'),
  [num(x) + " g {O2}", num(n_ * 4 / 3 * mm('O2')) + " g {O2}", num(n_ * 3 / 4 * mm('O')) + " g {O2}", num(n_ * mm('O2')) + " g {O2}"],
  ["8.40 g &divide; 55.85 g/mol = 0.1504 mol Fe; &times; 3/4 = 0.1128 mol {O2}; &times; 31.998 g/mol.",
   "This uses 4/3, the ratio upside down.",
   "This uses the mass of O atoms (15.999 g/mol). The reactant is {O2} gas.",
   "This skips the mole ratio (4 Fe : 3 {O2})."],
  "Which ratio has mol {O2} on top and mol Fe on the bottom?",
  "8.40 g Fe &times; (1 mol / 55.85 g) &times; (3 mol {O2} / 4 mol Fe) &times; (31.998 g / 1 mol) = <b>" + num(x) + " g {O2}</b>.", 3, 1)

Q(T, "Which order of steps converts grams of a reactant A into grams of a product B?",
  ["g A &rarr; mol A &rarr; mol B &rarr; g B", "g A &rarr; g B, using the coefficients", "g A &rarr; mol B &rarr; mol A &rarr; g B", "mol A &rarr; g A &rarr; g B &rarr; mol B"],
  ["Molar mass of A, then the mole ratio, then the molar mass of B. Only moles have a ratio in the equation.",
   "Coefficients are mole ratios, not mass ratios, so grams cannot be converted directly.",
   "The mole ratio links mol A to mol B; you must reach mol A first, from g A.",
   "The given is in grams, so you start at g A, not mol A."],
  "Our goal is the mole: where does the mole ratio sit in the road map?",
  "The road map: <b>g A &rarr; mol A &rarr; mol B &rarr; g B</b> (molar mass of A, mole ratio, molar mass of B).", 1)

Q(T, "A student finds the mass of water made from 5.5 g of {H2} with [[2 H2(g) + O2(g) -> 2 H2O(l)]] as 5.5 g {H2} &times; (2 mol {H2O} / 2 mol {H2}) = 5.5 g {H2O}. What went wrong?",
  ["The grams of {H2} were never converted to moles, so the mole ratio was used on grams.",
   "The mole ratio is upside down.",
   "The equation is not balanced.",
   "Nothing; the ratio is 1 : 1, so the masses are equal."],
  ["A mole ratio works only on moles. 5.5 g &divide; 2.016 g/mol = 2.73 mol {H2} &rarr; 2.73 mol {H2O} &rarr; &times; 18.015 g/mol = 49 g {H2O}.",
   "2/2 is the same either way up; the problem is the missing molar masses.",
   "The equation is balanced: 4 H and 2 O on each side.",
   "A 1 : 1 mole ratio means equal moles, not equal masses. A water molecule is about 9 times heavier than an {H2} molecule."],
  "Can you multiply grams by a mole ratio?",
  "The student <b>skipped the conversion to moles</b>. 5.5 g &times; (1 mol / 2.016 g) &times; (2 mol {H2O} / 2 mol {H2}) &times; (18.015 g / 1 mol) = 49 g {H2O}.", 2)

n_ = D('3.45') / mm('C7H6O3')
x = n_ * mm('C4H6O3')
Q(T, "Aspirin is made by [[C7H6O3 + C4H6O3 -> C9H8O4 + C2H4O2]] (salicylic acid + acetic anhydride &rarr; aspirin + acetic acid). What mass of acetic anhydride reacts exactly with 3.45 g of salicylic acid? " + MMS('C7H6O3', 'C4H6O3'),
  [num(x) + " g {C4H6O3}", "3.45 g {C4H6O3}", num(D('3.45') * mm('C7H6O3') / mm('C4H6O3')) + " g {C4H6O3}", num(n_) + " mol {C4H6O3}"],
  ["3.45 g &divide; 138.122 g/mol = 0.02498 mol; 1 : 1 ratio, so 0.02498 mol {C4H6O3}; &times; 102.089 g/mol.",
   "A 1 : 1 mole ratio means equal moles, not equal grams. The two molecules have different molar masses.",
   "This uses the two molar masses upside down (multiplies by 138.122 and divides by 102.089).",
   "This stops at moles. Multiply by the molar mass of acetic anhydride."],
  "Equal moles of two substances have equal masses only if their molar masses are equal.",
  "3.45 g {C7H6O3} &times; (1 mol / 138.122 g) &times; (1 mol {C4H6O3} / 1 mol {C7H6O3}) &times; (102.089 g / 1 mol) = <b>" + num(x) + " g {C4H6O3}</b>.", 2, 1)

n_ = D('3.36') / mm('NaHCO3')
x = n_ / 2 * mm('CO2')
Q(T, "Baking soda releases {CO2} when heated in an oven: [[2 NaHCO3(s) -> Na2CO3(s) + H2O(g) + CO2(g)]]. What mass of {CO2} forms from 3.36 g of {NaHCO3}? " + MMS('NaHCO3', 'CO2'),
  [num(x) + " g {CO2}", num(n_ * mm('CO2')) + " g {CO2}", num(n_ * 2 * mm('CO2')) + " g {CO2}", num(n_ / 2 / 2 * mm('CO2')) + " g {CO2}"],
  ["3.36 g &divide; 84.01 g/mol = 0.04000 mol {NaHCO3}; &times; 1/2 = 0.02000 mol {CO2}; &times; 44.009 g/mol.",
   "This skips the mole ratio. Two {NaHCO3} make one {CO2}.",
   "This uses 2/1, the ratio upside down.",
   "This uses the coefficient twice: in the mole ratio and again on the molar mass of {NaHCO3} (2 &times; 84.01). A molar mass never includes a coefficient."],
  "Two {NaHCO3} &rarr; one {CO2}.",
  "3.36 g {NaHCO3} &times; (1 mol / 84.01 g) &times; (1 mol {CO2} / 2 mol {NaHCO3}) &times; (44.009 g / 1 mol) = <b>" + num(x) + " g {CO2}</b>.", 2, 1)

n1 = D('30.0') / mm('C6H12O6'); n2 = n1 * 2; x = n2 * mm('CO2')
Q(T, "Bread dough rises as yeast ferment sugar: [[C6H12O6 -> 2 C2H5OH + 2 CO2]]. The table follows the road map for 30.0 g of glucose. What mass of {CO2} goes in the last row?",
  [num(x) + " g {CO2}", num(n1 * mm('CO2')) + " g {CO2}", num(n2 * 2 * mm('CO2')) + " g {CO2}", num(n2) + " g {CO2}"],
  ["0.3330 mol {CO2} &times; 44.009 g/mol. The mole ratio was already applied in the third row.",
   "This multiplies the moles of glucose (row 2) by the molar mass of {CO2}, skipping the mole ratio.",
   "This multiplies by 2 again; the coefficient was already used in the mole ratio.",
   "This copies the moles of {CO2} and labels them grams. Multiply by the molar mass."],
  "Which row has moles of {CO2}? What factor turns moles into grams?",
  "0.3330 mol {CO2} &times; 44.009 g/mol = <b>" + num(x) + " g {CO2}</b>. Each row is one step of the road map.", 3, 1,
  [{"type": "table", "cap": "Road map for 30.0 g of glucose", "head": ["Step", "Value"],
    "rows": [["g {C6H12O6}", "30.0"], ["mol {C6H12O6} (&divide; 180.156)", num(n1, 4)], ["mol {CO2} (&times; 2/1)", num(n2, 4)], ["g {CO2} (&times; 44.009)", "?"]]}])

n_ = D('12.5') / mm('Fe2O3')
x = n_ * 2 * mm('Al')
Q(T, "The thermite reaction welds railroad rails: [[Fe2O3(s) + 2 Al(s) -> Al2O3(s) + 2 Fe(l)]]. What mass of Al reacts exactly with 12.5 g of {Fe2O3}? " + MMS('Fe2O3', 'Al'),
  [num(x) + " g Al", num(n_ * mm('Al')) + " g Al", num(n_ / 2 * mm('Al')) + " g Al", num(n_ * 2 * 2 * mm('Al')) + " g Al"],
  ["12.5 g &divide; 159.70 g/mol = 0.07827 mol {Fe2O3}; &times; 2 = 0.1565 mol Al; &times; 26.98 g/mol.",
   "This skips the mole ratio: each {Fe2O3} needs 2 Al.",
   "This uses 1/2, the ratio upside down.",
   "This puts the coefficient 2 into the molar mass of Al as well. The molar mass of Al is 26.98 g/mol however many Al atoms react."],
  "Never put a coefficient into a molar mass.",
  "12.5 g {Fe2O3} &times; (1 mol / 159.70 g) &times; (2 mol Al / 1 mol {Fe2O3}) &times; (26.98 g / 1 mol) = <b>" + num(x) + " g Al</b>.", 3, 1)

# ======================= ch08-solgas (10) =======================
T = 'ch08-solgas'
x = D('0.0350') * D('0.150')
Q(T, "How many moles of HCl are in 35.0 mL of 0.150 M HCl?",
  [num(x) + " mol HCl", num(D('35.0') * D('0.150')) + " mol HCl", num(D('0.0350') / D('0.150')) + " mol HCl", num(D('0.150') / D('35.0')) + " mol HCl"],
  ["35.0 mL = 0.0350 L; 0.0350 L &times; 0.150 mol/L.",
   "This multiplies mL by mol/L without converting mL to L, so the answer is 1000 times too large.",
   "This divides liters by molarity, which gives L&sup2;/mol, not moles.",
   "This divides the molarity by the volume in mL; moles = liters &times; molarity."],
  "Molarity is moles per <b>liter</b>.",
  "35.0 mL &times; (1 L / 1000 mL) &times; (0.150 mol / 1 L) = <b>" + num(x) + " mol HCl</b>.", 1, 1)

n_ = D('0.315') / mm('NaHCO3'); L = n_ / D('0.125')
Q(T, "Baking soda can neutralize acid: [[NaHCO3(s) + HCl(aq) -> NaCl(aq) + H2O(l) + CO2(g)]]. What volume of 0.125 M HCl reacts with 0.315 g of {NaHCO3}? " + MMS('NaHCO3'),
  [num(L * 1000) + " mL", num(L) + " mL", num(n_ * D('0.125') * 1000) + " mL", num(n_) + " mol"],
  ["0.315 g &divide; 84.01 g/mol = 0.003750 mol {NaHCO3} = 0.003750 mol HCl (1 : 1); &divide; 0.125 mol/L = 0.0300 L = 30.0 mL.",
   "This is the volume in liters with a mL label; multiply liters by 1000 mL/L.",
   "This multiplies moles by molarity. To get liters, divide moles by molarity (L = mol &divide; M).",
   "This stops at moles of HCl; dividing by the molarity gives the volume."],
  "liters = moles &divide; molarity.",
  "0.315 g &times; (1 mol / 84.01 g) &times; (1 mol HCl / 1 mol {NaHCO3}) &times; (1 L / 0.125 mol) = 0.0300 L = <b>" + num(L * 1000) + " mL</b>.", 2, 1)

n_ = D('0.346') / 2; x = n_ * D('22.4')
Q(T, "A 3% hydrogen peroxide solution decomposes: [[2 H2O2(aq) -> 2 H2O(l) + O2(g)]]. What volume of {O2} at STP forms from 0.346 mol of {H2O2}?",
  [num(x) + " L {O2}", num(D('0.346') * D('22.4')) + " L {O2}", num(D('0.346') * 2 * D('22.4')) + " L {O2}", num(n_) + " mol {O2}"],
  ["0.346 mol {H2O2} &times; 1/2 = 0.173 mol {O2}; &times; 22.4 L/mol at STP.",
   "This skips the mole ratio: two {H2O2} make one {O2}.",
   "This uses 2/1, the ratio upside down.",
   "This stops at moles; at STP, multiply by 22.4 L/mol."],
  "Mole ratio first, then 22.4 L/mol.",
  "0.346 mol {H2O2} &times; (1 mol {O2} / 2 mol {H2O2}) &times; (22.4 L / 1 mol) = <b>" + num(x) + " L {O2}</b>.", 2, 1)

n_ = D('15.0') / mm('CaCO3'); x = n_ * D('22.4')
Q(T, "Heating limestone in a kiln makes lime for cement and for treating farm soil: [[CaCO3(s) -> CaO(s) + CO2(g)]]. What volume of {CO2} at STP forms from 15.0 g of {CaCO3}? " + MMS('CaCO3'),
  [num(x) + " L {CO2}", num(D('15.0') * D('22.4')) + " L {CO2}", num(n_) + " mol {CO2}", num(n_ / D('22.4')) + " L {CO2}"],
  ["15.0 g &divide; 100.09 g/mol = 0.1499 mol {CaCO3} = 0.1499 mol {CO2} (1 : 1); &times; 22.4 L/mol.",
   "This multiplies grams by 22.4 L/mol. Molar volume converts moles, not grams.",
   "This stops at moles of {CO2}.",
   "This divides by 22.4 L/mol. Moles &times; (22.4 L / 1 mol) gives liters."],
  "g &rarr; mol {CaCO3} &rarr; mol {CO2} &rarr; L.",
  "15.0 g &times; (1 mol / 100.09 g) &times; (1 mol {CO2} / 1 mol {CaCO3}) &times; (22.4 L / 1 mol) = <b>" + num(x) + " L {CO2}</b> at STP.", 2, 1)

n_ = D('0.0425') / mm('Mg'); L = n_ * D('22.4')
Q(T, "In a gas-production lab, magnesium ribbon reacts with acid: [[Mg(s) + 2 HCl(aq) -> MgCl2(aq) + H2(g)]]. What volume of {H2}, in mL at STP, forms from 0.0425 g of Mg? (Mg 24.31 g/mol)",
  [num(L * 1000) + " mL {H2}", num(L * 2 * 1000) + " mL {H2}", num(L) + " mL {H2}", num(n_) + " mol {H2}"],
  ["0.0425 g &divide; 24.31 g/mol = 0.001748 mol Mg = 0.001748 mol {H2}; &times; 22.4 L/mol = 0.03916 L = 39.2 mL.",
   "This uses the HCl coefficient (2). The ratio of {H2} to Mg is 1 : 1.",
   "This is the volume in liters with a mL label; multiply by 1000 mL/L.",
   "This stops at moles of {H2}."],
  "Find liters with 22.4 L/mol, then convert to mL.",
  "0.0425 g Mg &times; (1 mol / 24.31 g) &times; (1 mol {H2} / 1 mol Mg) &times; (22.4 L / 1 mol) = 0.03916 L = <b>" + num(L * 1000) + " mL {H2}</b>.", 3, 1)

n_ = D('12.6') / mm('C6H12O6') * 2; x = n_ * D('24.5')
Q(T, "A winemaker ferments grapes at 25 &deg;C and 1 atm, where 1 mol of gas occupies 24.5 L: [[C6H12O6(aq) -> 2 C2H5OH(aq) + 2 CO2(g)]]. What volume of {CO2} forms from 12.6 g of glucose? " + MMS('C6H12O6'),
  [num(x) + " L {CO2}", num(n_ * D('22.4')) + " L {CO2}", num(n_ / 2 * D('24.5')) + " L {CO2}", num(n_) + " mol {CO2}"],
  ["12.6 g &divide; 180.156 g/mol = 0.06994 mol glucose; &times; 2 = 0.1399 mol {CO2}; &times; 24.5 L/mol, the molar volume at these conditions.",
   "This uses 22.4 L/mol, which is only for STP (0 &deg;C, 1 atm). At 25 &deg;C a mole of gas takes up more room.",
   "This skips the mole ratio: each glucose makes 2 {CO2}.",
   "This stops at moles of {CO2}."],
  "Use the molar volume given for these conditions, not the STP value.",
  "12.6 g &times; (1 mol / 180.156 g) &times; (2 mol {CO2} / 1 mol glucose) &times; (24.5 L / 1 mol) = <b>" + num(x) + " L {CO2}</b>.", 3, 1)

nA = D('0.0150') * D('0.180'); nB = nA * 2; L = nB / D('0.250')
Q(T, "In a titration, [[H2SO4(aq) + 2 NaOH(aq) -> Na2SO4(aq) + 2 H2O(l)]]. What volume of 0.250 M NaOH neutralizes 15.0 mL of 0.180 M {H2SO4}?",
  [num(L * 1000) + " mL NaOH", num(nA / 2 / D('0.250') * 1000) + " mL NaOH", num(nA / D('0.250') * 1000) + " mL NaOH", num(L) + " mL NaOH"],
  ["0.0150 L &times; 0.180 M = 0.00270 mol {H2SO4}; &times; 2 = 0.00540 mol NaOH; &divide; 0.250 M = 0.0216 L = 21.6 mL.",
   "This uses 1/2, the ratio upside down: each {H2SO4} needs two NaOH.",
   "This skips the mole ratio (1 {H2SO4} : 2 NaOH).",
   "This is the volume in liters with a mL label."],
  "mL acid &rarr; L &rarr; mol acid &rarr; mol NaOH &rarr; L NaOH &rarr; mL.",
  "0.0150 L &times; (0.180 mol / 1 L) &times; (2 mol NaOH / 1 mol {H2SO4}) &times; (1 L / 0.250 mol) = 0.0216 L = <b>" + num(L * 1000) + " mL NaOH</b>.", 3, 1)

Q(T, "For which gas sample can you use 22.4 L/mol to convert volume to moles?",
  ["Nitrogen at 0 &deg;C and 1 atm", "Exhaled air at body temperature, 37 &deg;C, and 1 atm",
   "Helium in a balloon at 25 &deg;C and 1 atm", "Oxygen in a compressed tank at 0 &deg;C and 150 atm"],
  ["0 &deg;C (273 K) and 1 atm is STP, where 1 mol of any ideal gas occupies 22.4 L.",
   "37 &deg;C is warmer than STP, so a mole of gas takes up more than 22.4 L.",
   "25 &deg;C is not STP; a mole of gas occupies about 24.5 L there.",
   "The temperature is right, but 150 atm squeezes the gas far below 22.4 L per mole."],
  "What are the two conditions of STP?",
  "22.4 L/mol holds only at STP, <b>0 &deg;C and 1 atm</b>. Chapter 10 handles other conditions.", 1)

Q(T, "A student finds the moles of NaOH in 25.0 mL of 0.150 M NaOH as 25.0 &times; 0.150 = 3.75 mol. What went wrong?",
  ["The volume was not converted to liters; the answer should be 0.00375 mol.",
   "The student should have divided: 25.0 &divide; 0.150.",
   "Molarity is mol per mL, so the answer is right.",
   "The student needed the molar mass of NaOH."],
  ["Molarity is mol per liter: 0.0250 L &times; 0.150 mol/L = 0.00375 mol, 1000 times smaller.",
   "Dividing volume by molarity does not give moles. Moles = liters &times; molarity.",
   "M means mol per <b>liter</b>, so mL must be converted first.",
   "Molar mass is not needed to get moles from a volume and a molarity."],
  "What volume unit does molarity use?",
  "<b>mL was not converted to L</b>: 25.0 mL = 0.0250 L, and 0.0250 L &times; 0.150 mol/L = 0.00375 mol NaOH.", 2)

n_ = D('0.0400') * D('0.600') / 2; x = n_ * mm('Zn')
Q(T, "Zinc dissolves in hydrochloric acid: [[Zn(s) + 2 HCl(aq) -> ZnCl2(aq) + H2(g)]]. What mass of Zn reacts with 40.0 mL of 0.600 M HCl? (Zn 65.39 g/mol)",
  [num(x) + " g Zn", num(n_ * 2 * mm('Zn')) + " g Zn", num(D('40.0') * D('0.600') / 2 * mm('Zn')) + " g Zn", num(n_ * 4 * mm('Zn')) + " g Zn"],
  ["0.0400 L &times; 0.600 M = 0.0240 mol HCl; &times; 1/2 = 0.0120 mol Zn; &times; 65.39 g/mol.",
   "This skips the mole ratio: one Zn reacts with two HCl.",
   "This uses 40.0 mL as if it were liters. Convert mL to L first.",
   "This uses 2/1, the ratio upside down."],
  "Find mol HCl with liters &times; molarity, then use the 1 Zn : 2 HCl ratio.",
  "0.0400 L &times; (0.600 mol / 1 L) &times; (1 mol Zn / 2 mol HCl) &times; (65.39 g / 1 mol) = <b>" + num(x) + " g Zn</b>.", 2, 1)

# ======================= ch08-limiting (12) =======================
T = 'ch08-limiting'
Q(T, "What is the <b>limiting reactant</b> in a reaction?",
  ["The reactant that is used up first, which sets the most product that can form",
   "The reactant present in the smallest mass",
   "The reactant with the smallest coefficient in the balanced equation",
   "The reactant that is left over when the reaction stops"],
  ["When the limiting reactant runs out, the reaction stops, so it decides the maximum amount of product.",
   "Mass alone cannot tell you; a reactant with a small molar mass can have many moles in a small mass.",
   "Coefficients are only part of the story; the amounts present matter too.",
   "That is the excess reactant."],
  "Think of bicycles: with 4 frames and 6 wheels, which part runs out first?",
  "The limiting reactant is <b>used up first and sets the maximum amount of product</b>; the other reactant is in excess and some is left over.", 1)

a = D('1.80') * 2; b = D('4.80') * 2 / 3
Q(T, "For [[N2(g) + 3 H2(g) -> 2 NH3(g)]], 1.80 mol of {N2} and 4.80 mol of {H2} react. What is the maximum amount of {NH3} that can form?",
  [num(b) + " mol {NH3}", num(a) + " mol {NH3}", num(a + b) + " mol {NH3}", num(D('4.80') * 2) + " mol {NH3}"],
  ["From {N2}: 1.80 &times; 2/1 = 3.60 mol; from {H2}: 4.80 &times; 2/3 = 3.20 mol. {H2} makes less, so it is limiting.",
   "This is what the {N2} could make. {H2} runs out first, so the reaction never gets that far.",
   "The two amounts are not added; the smaller one is the answer.",
   "This uses a 2 : 1 ratio for {H2}; the ratio is 2 {NH3} : 3 {H2}."],
  "Find the {NH3} each reactant could make. Which answer wins?",
  "{N2} &rarr; 3.60 mol {NH3}; {H2} &rarr; 3.20 mol {NH3}. <b>{H2} is limiting: " + num(b) + " mol {NH3}</b>.", 2, 1)

Q(T, "6.20 g of Na and 7.10 g of {Cl2} react: [[2 Na(s) + Cl2(g) -> 2 NaCl(s)]]. Which is the limiting reactant? (Na 22.99 g/mol; {Cl2} 70.90 g/mol)",
  ["{Cl2}, because it can make less NaCl", "Na, because its mass is smaller",
   "Na, because the equation needs 2 Na for every {Cl2}", "Neither; the two react completely"],
  ["Na: 6.20 &divide; 22.99 = 0.2697 mol &rarr; 0.2697 mol NaCl. {Cl2}: 7.10 &divide; 70.90 = 0.1001 mol &rarr; 0.2003 mol NaCl. {Cl2} makes less.",
   "Comparing grams does not work: Na atoms are much lighter than {Cl2} molecules, so 6.20 g of Na is more moles.",
   "The coefficient matters, but you must also know how many moles are present. Run both through the ratio.",
   "0.2697 mol Na would need 0.1348 mol {Cl2}, and only 0.1001 mol is present, so they do not react completely."],
  "Convert each to moles, then to moles of NaCl.",
  "Na &rarr; 0.2697 mol NaCl; {Cl2} &rarr; 0.2003 mol NaCl. <b>{Cl2} is limiting</b>, even though its mass is larger.", 2)

nN = D('14.0') / mm('N2'); nH = D('3.60') / mm('H2')
pN = nN * 2; pH = nH * 2 / 3
Q(T, "14.0 g of {N2} and 3.60 g of {H2} react: [[N2(g) + 3 H2(g) -> 2 NH3(g)]]. What is the maximum mass of {NH3} that can form? " + MMS('N2', 'H2', 'NH3'),
  [num(pN * mm('NH3')) + " g {NH3}", num(pH * mm('NH3')) + " g {NH3}", "17.6 g {NH3}", num(nN * mm('NH3')) + " g {NH3}"],
  ["{N2}: 0.4998 mol &rarr; 0.9995 mol {NH3}; {H2}: 1.786 mol &rarr; 1.190 mol {NH3}. {N2} is limiting: 0.9995 mol &times; 17.031 g/mol.",
   "This uses {H2}, the excess reactant. The smaller amount of product is the answer.",
   "This adds the reactant masses, as if both reacted completely. One reactant is left over.",
   "This skips the mole ratio for {N2}: each {N2} makes 2 {NH3}."],
  "Which reactant makes less {NH3}? Use that one.",
  "{N2} makes 0.9995 mol {NH3}, {H2} 1.190 mol, so {N2} limits: 0.9995 mol &times; 17.031 g/mol = <b>" + num(pN * mm('NH3')) + " g {NH3}</b>.", 3, 1)

used = D('3.40') / 2
Q(T, "A catalytic converter removes CO by [[2 CO(g) + O2(g) -> 2 CO2(g)]]. A mixture of 3.40 mol CO and 2.10 mol {O2} reacts. How much of the excess reactant is left over?",
  [subt(D('2.10'), used) + " mol {O2}", num(used) + " mol {O2}", "1.30 mol CO", "None; both are used up"],
  ["From CO: 3.40 mol {CO2}; from {O2}: 4.20 mol {CO2}. CO is limiting. {O2} used: 3.40 &times; 1/2 = 1.70 mol; left: 2.10 &minus; 1.70 = 0.40 mol.",
   "1.70 mol is the {O2} that reacts. Subtract it from the 2.10 mol present.",
   "This subtracts the two reactants (3.40 &minus; 2.10). Use the mole ratio to find how much of the excess reacts.",
   "3.40 mol CO needs only 1.70 mol {O2}, so some {O2} remains."],
  "Find the limiting reactant, then the amount of the other one it uses.",
  "CO is limiting; it uses 1.70 mol {O2}. Left over: 2.10 &minus; 1.70 = <b>" + subt(D('2.10'), used) + " mol {O2}</b>.", 2, 1)

nFe = D('6.50') / mm('Fe'); nS = D('4.25') / mm('S'); usedS = rnd(nFe * mm('S'))
Q(T, "6.50 g of iron and 4.25 g of sulfur are heated: [[Fe(s) + S(s) -> FeS(s)]]. What mass of the excess reactant is left? (Fe 55.85 g/mol; S 32.06 g/mol)",
  [subt(D('4.25'), usedS) + " g S", str(usedS) + " g S", "2.25 g", subt(D('4.25'), usedS) + " g Fe"],
  ["Fe: 0.1164 mol; S: 0.1326 mol; 1 : 1, so Fe is limiting. S used = 0.1164 mol &times; 32.06 g/mol = 3.73 g; left = 4.25 &minus; 3.73 = 0.52 g S.",
   "3.73 g is the sulfur that reacts. Subtract it from the 4.25 g present.",
   "This subtracts the two masses (6.50 &minus; 4.25). Iron and sulfur do not react gram for gram.",
   "Iron is the limiting reactant, so no iron is left; the leftover is sulfur."],
  "Limiting reactant first; then mass of excess used; then subtract.",
  "Fe is limiting. S used: 0.1164 mol &times; 32.06 g/mol = 3.73 g. Left: 4.25 g &minus; 3.73 g = <b>" + subt(D('4.25'), usedS) + " g S</b>.", 3, 1)

Q(T, "The box shows the molecules before [[N2(g) + 3 H2(g) -> 2 NH3(g)]] runs. What is the most {NH3} that can form, and which reactant is limiting?",
  ["4 {NH3} molecules; {H2} is limiting", "6 {NH3} molecules; {N2} is limiting",
   "3 {NH3} molecules; {N2} is limiting", "9 {NH3} molecules; neither is limiting"],
  ["3 {N2} could make 6 {NH3}, but 6 {H2} can make only 6 &times; 2/3 = 4 {NH3}. {H2} runs out first, with 1 {N2} left over.",
   "Six {NH3} would need 9 {H2}; only 6 are present.",
   "Having fewer {N2} molecules does not make {N2} limiting; each {N2} needs 3 {H2}.",
   "Molecules are not simply added; the mole ratio decides."],
  "Count each kind of molecule, then use the 1 : 3 : 2 ratio.",
  "{H2}: 6 &times; 2/3 = 4 {NH3}; {N2}: 3 &times; 2 = 6 {NH3}. <b>{H2} limits: 4 {NH3}</b>, and 1 {N2} is left.", 2, 0,
  [{"type": "particles", "seed": 8, "key": {"N": {"c": "#2f5fa8", "n": "nitrogen atom", "q": "N"}, "H": {"c": "#5f6f7b", "n": "hydrogen atom", "q": "H", "r": 8}},
    "boxes": [{"mols": [["N", "N"], ["N", "N"], ["N", "N"], ["H", "H"], ["H", "H"], ["H", "H"], ["H", "H"], ["H", "H"], ["H", "H"]], "cap": "Before"}]}])

nP = D('6.60') / mm('C3H8'); nO = D('20.0') / mm('O2')
cP = nP * 3; cO = nO * 3 / 5
Q(T, "6.60 g of propane and 20.0 g of {O2} react: [[C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(l)]]. What is the maximum mass of {CO2}? " + MMS('C3H8', 'O2', 'CO2'),
  [num(cO * mm('CO2')) + " g {CO2}", num(cP * mm('CO2')) + " g {CO2}", "26.6 g {CO2}", num(nO * 3 * mm('CO2')) + " g {CO2}"],
  ["Propane: 0.1497 mol &rarr; 0.4490 mol {CO2}. {O2}: 0.6250 mol &rarr; 0.3750 mol {CO2}. {O2} is limiting (even though its mass is larger): 0.3750 mol &times; 44.009 g/mol.",
   "This uses propane, the excess reactant. Propane is the smaller mass but not the limiting reactant.",
   "This adds the reactant masses; the products include water, and some propane is left over.",
   "This uses 3 {CO2} : 1 {O2}; the ratio is 3 {CO2} : 5 {O2}."],
  "Each reactant &rarr; mol {CO2}. The smaller one wins.",
  "{O2} &rarr; 0.3750 mol {CO2} (less than 0.4490 from propane), so {O2} limits: 0.3750 &times; 44.009 = <b>" + num(cO * mm('CO2')) + " g {CO2}</b>.", 3, 1)

Q(T, "For [[2 H2(g) + O2(g) -> 2 H2O(g)]], a student has 3.4 mol of {H2} and 2.0 mol of {O2} and says, &ldquo;{O2} is limiting because there are fewer moles of it.&rdquo; What is wrong with this reasoning?",
  ["Moles can be compared directly only when the coefficients are equal; here {H2} is limiting.",
   "Nothing; the reactant with fewer moles is always limiting.",
   "The student should compare grams instead of moles.",
   "{O2} is limiting, but only because it has the larger molar mass."],
  ["{H2} makes 3.4 mol {H2O}; {O2} makes 4.0 mol. {H2} runs out first, because the recipe needs 2 {H2} for each {O2}.",
   "That works only when the coefficients are equal. Here 2.0 mol {O2} needs 4.0 mol {H2}, and only 3.4 mol is present.",
   "Comparing grams is even less reliable; molar masses differ.",
   "{O2} is the excess reactant here, and molar mass does not decide which reactant limits."],
  "How many moles of {H2} would 2.0 mol {O2} need?",
  "{H2} &rarr; 3.4 mol {H2O}; {O2} &rarr; 4.0 mol {H2O}. <b>{H2} is limiting</b>; compare moles only through the mole ratio.", 2)

nA = D('3.40') / mm('NH3'); nS = D('12.5') / mm('H2SO4')
pA = nA / 2; pS = nS
Q(T, "Ammonium sulfate fertilizer forms by [[2 NH3(aq) + H2SO4(aq) -> (NH4)2SO4(aq)]]. 3.40 g of {NH3} and 12.5 g of {H2SO4} react. What mass of {(NH4)2SO4} can form? " + MMS('NH3', 'H2SO4', '(NH4)2SO4'),
  [num(pA * mm('(NH4)2SO4')) + " g {(NH4)2SO4}", num(pS * mm('(NH4)2SO4')) + " g {(NH4)2SO4}", num(nA * mm('(NH4)2SO4')) + " g {(NH4)2SO4}", "15.9 g {(NH4)2SO4}"],
  ["{NH3}: 0.1996 mol &rarr; 0.09982 mol product; {H2SO4}: 0.1275 mol &rarr; 0.1275 mol product. {NH3} is limiting: 0.09982 mol &times; 132.13 g/mol.",
   "This uses {H2SO4}, the excess reactant.",
   "This skips the mole ratio for {NH3}: two {NH3} make one formula unit of product.",
   "This adds the reactant masses, but some {H2SO4} is left over."],
  "Run each reactant through its own mole ratio to the product.",
  "{NH3} &rarr; 0.09982 mol; {H2SO4} &rarr; 0.1275 mol. {NH3} limits: 0.09982 &times; 132.13 = <b>" + num(pA * mm('(NH4)2SO4')) + " g {(NH4)2SO4}</b>.", 3, 1)

nNa = D('5.75') / mm('Na'); nC = D('8.15') / mm('Cl2'); usedNa = rnd(nC * 2 * mm('Na')); used11 = rnd(nC * mm('Na'))
Q(T, "5.75 g of Na and 8.15 g of {Cl2} react: [[2 Na(s) + Cl2(g) -> 2 NaCl(s)]]. What mass of the excess reactant remains? (Na 22.99 g/mol; {Cl2} 70.90 g/mol)",
  [subt(D('5.75'), usedNa) + " g Na", str(usedNa) + " g Na", "2.40 g", subt(D('5.75'), used11) + " g Na"],
  ["Na: 0.2501 mol &rarr; 0.2501 mol NaCl; {Cl2}: 0.1150 mol &rarr; 0.2299 mol NaCl. {Cl2} limits. Na used: 0.1150 &times; 2 &times; 22.99 = 5.29 g; left 5.75 &minus; 5.29 = 0.46 g.",
   "5.29 g is the Na that reacts. Subtract it from the 5.75 g present.",
   "This subtracts the masses of the two reactants (8.15 &minus; 5.75).",
   "This uses a 1 : 1 ratio for Na to {Cl2}; each {Cl2} reacts with 2 Na, so 5.29 g of Na is used, not 2.64 g."],
  "Na used = mol {Cl2} &times; (2 mol Na / 1 mol {Cl2}) &times; 22.99 g/mol.",
  "{Cl2} is limiting; it uses 5.29 g Na. Left: 5.75 &minus; 5.29 = <b>" + subt(D('5.75'), usedNa) + " g Na</b>.", 3, 1)

Q(T, "For [[2 SO2(g) + O2(g) -> 2 SO3(g)]], which mixture in the table reacts with <b>nothing left over</b>?",
  ["Mixture B", "Mixture A", "Mixture C", "Mixture D"],
  ["3.0 mol {SO2} needs 3.0 &times; 1/2 = 1.5 mol {O2}, exactly what is present.",
   "2.0 mol {SO2} needs only 1.0 mol {O2}, so 1.0 mol {O2} is left.",
   "1.0 mol {SO2} needs only 0.50 mol {O2}, so {O2} is left.",
   "1.0 mol {O2} reacts with only 2.0 mol {SO2}, so {SO2} is left."],
  "The mixture must match the 2 : 1 ratio.",
  "Only <b>Mixture B</b> (3.0 mol {SO2} : 1.5 mol {O2}) is in the exact 2 : 1 ratio.", 2, 0,
  [{"type": "table", "cap": "Starting mixtures", "head": ["Mixture", "mol {SO2}", "mol {O2}"],
    "rows": [["A", "2.0", "2.0"], ["B", "3.0", "1.5"], ["C", "1.0", "2.0"], ["D", "4.0", "1.0"]]}])

# ======================= ch08-yield (10) =======================
T = 'ch08-yield'
x = D('15.9') / D('18.6')
Q(T, "A reaction has a theoretical yield of 18.6 g, and a student collects 15.9 g of product. What is the percent yield?",
  [pct(x), pct(1 / x), pct(1 - x), "2.7%"],
  ["15.9 g &divide; 18.6 g &times; 100%: actual over theoretical.",
   "This divides theoretical by actual, giving more than 100%.",
   "This is the percent of product that was lost, 100% &minus; the percent yield.",
   "This is the difference in grams (18.6 &minus; 15.9), not a percent."],
  "Percent yield = actual &divide; theoretical &times; 100%.",
  "15.9 g &divide; 18.6 g &times; 100% = <b>" + pct(x) + "</b>.", 1, 1)

Q(T, "What is the <b>theoretical yield</b> of a reaction?",
  ["The most product that stoichiometry predicts from the limiting reactant",
   "The mass of product you weigh at the end of the lab",
   "The total mass of all the reactants",
   "The product predicted from the excess reactant"],
  ["It is the calculated maximum, assuming every bit of the limiting reactant becomes product and none is lost.",
   "That is the actual yield.",
   "Reactant mass is not product mass; some reactant may be in excess, and other products form too.",
   "The excess reactant cannot all react, so it predicts too much product."],
  "Theoretical means calculated.",
  "Theoretical yield = <b>the maximum product calculated from the limiting reactant</b>.", 1)

th = D('1.20') / mm('Mg') * mm('MgO'); x = D('1.79') / th
Q(T, "Burning 1.20 g of Mg, [[2 Mg(s) + O2(g) -> 2 MgO(s)]], gives 1.79 g of MgO. What is the percent yield? " + MMS('Mg', 'MgO'),
  [pct(x), pct(1 / x), pct(D('1.79') / D('1.20')), pct(D('1.79') / (th * 2))],
  ["Theoretical: 1.20 g &divide; 24.31 g/mol &times; (2/2) &times; 40.31 g/mol = 1.990 g MgO. 1.79 &divide; 1.990 &times; 100%.",
   "This divides theoretical by actual.",
   "This compares the product with the mass of Mg. The theoretical yield of MgO is the right comparison.",
   "This doubles the theoretical yield by multiplying the molar mass of MgO by its coefficient."],
  "Find the theoretical yield of MgO first.",
  "Theoretical = 1.990 g MgO; 1.79 g &divide; 1.990 g &times; 100% = <b>" + pct(x) + "</b>.", 2, 1)

n_ = D('1.38') / mm('C7H6O3'); x = n_ * mm('C9H8O4')
Q(T, "In a lab, aspirin is made from salicylic acid and excess acetic anhydride: [[C7H6O3 + C4H6O3 -> C9H8O4 + C2H4O2]]. What is the theoretical yield of aspirin from 1.38 g of salicylic acid? " + MMS('C7H6O3', 'C9H8O4'),
  [num(x) + " g {C9H8O4}", "1.38 g {C9H8O4}", num(D('1.38') * mm('C7H6O3') / mm('C9H8O4')) + " g {C9H8O4}", num(n_) + " mol {C9H8O4}"],
  ["1.38 g &divide; 138.122 g/mol = 0.009991 mol; 1 : 1; &times; 180.159 g/mol.",
   "Equal moles are not equal grams. Aspirin molecules are heavier than salicylic acid molecules.",
   "This uses the molar masses upside down.",
   "This stops at moles; the yield is asked in grams."],
  "Salicylic acid is limiting. Follow the road map to grams of aspirin.",
  "1.38 g &times; (1 mol / 138.122 g) &times; (1 mol {C9H8O4} / 1 mol {C7H6O3}) &times; (180.159 g / 1 mol) = <b>" + num(x) + " g {C9H8O4}</b>.", 2, 1)

nS = D('2.76') / mm('C7H6O3'); nA = D('3.06') / mm('C4H6O3'); th = nS * mm('C9H8O4'); x = D('2.95') / th
Q(T, "A student mixes 2.76 g of salicylic acid with 3.06 g of acetic anhydride, [[C7H6O3 + C4H6O3 -> C9H8O4 + C2H4O2]], and collects 2.95 g of aspirin. What is the percent yield? " + MMS('C7H6O3', 'C4H6O3', 'C9H8O4'),
  [pct(x), pct(D('2.95') / (nA * mm('C9H8O4'))), pct(1 / x), pct(D('2.95') / D('2.76'))],
  ["Salicylic acid: 0.01998 mol; acetic anhydride: 0.02997 mol; 1 : 1, so salicylic acid is limiting. Theoretical = 0.01998 &times; 180.159 = 3.600 g; 2.95 &divide; 3.600 &times; 100%.",
   "This takes the theoretical yield from acetic anhydride, the excess reactant, which makes the percent yield look too small.",
   "This divides theoretical by actual.",
   "This compares the aspirin with the mass of salicylic acid instead of with the theoretical yield."],
  "Which reactant is limiting? Only it sets the theoretical yield.",
  "Salicylic acid limits; theoretical = 3.600 g aspirin. 2.95 &divide; 3.600 &times; 100% = <b>" + pct(x) + "</b>.", 3, 1)

Q(T, "A student filters alum crystals and weighs them right away, reporting a 106% yield. What is the most likely reason?",
  ["The crystals are still wet, so their mass includes water.",
   "The reaction made more product than the limiting reactant allows.",
   "Some crystals were lost in the filtrate.",
   "The student used the limiting reactant to find the theoretical yield."],
  ["Water clinging to the crystals adds mass. Drying them would lower the mass and the percent yield.",
   "Matter is not created; no reaction can beat its theoretical yield.",
   "Lost crystals lower the yield, not raise it.",
   "Using the limiting reactant is the correct method; it does not cause a yield over 100%."],
  "A yield above 100% means the product weighs more than it should. What could add mass?",
  "A yield above 100% points to extra mass: here, <b>water left in the crystals</b>.", 2)

Q(T, "Which question does a <b>percent yield</b> answer?",
  ["How much of the possible product did I collect?", "How close is my measurement to the accepted value?",
   "How much of the excess reactant is left?", "How fast did the reaction go?"],
  ["Percent yield = actual &divide; theoretical &times; 100%.",
   "That is percent error (Chapter 1), which compares a measurement with an accepted value.",
   "That is a leftover (excess reactant) calculation.",
   "Yield says nothing about speed."],
  "Yield compares what you got with what was possible.",
  "Percent yield asks <b>how much of the possible product you collected</b>; percent error asks how close a measurement is to the accepted value.", 2)

x = D('42.5') * D('0.760')
Q(T, "A reaction has a theoretical yield of 42.5 g. If the percent yield is 76.0%, what mass of product is collected?",
  [num(x) + " g", num(D('42.5') / D('0.760')) + " g", num(D('42.5') * D('76.0')) + " g", num(D('42.5') * (1 - D('0.760'))) + " g"],
  ["actual = 0.760 &times; 42.5 g. The actual yield must be smaller than 42.5 g.",
   "This divides by 0.760, which gives more than the theoretical yield.",
   "This multiplies by 76.0 without dividing by 100.",
   "This is the mass that was not collected (24.0% of 42.5 g)."],
  "Rearrange: actual = (percent &divide; 100) &times; theoretical.",
  "Actual = 0.760 &times; 42.5 g = <b>" + num(x) + " g</b>.", 2, 1)

th = D('64.0') / mm('C6H12O6') * 2 * mm('C2H5OH'); x = th * D('0.820')
Q(T, "Ethanol for fuel is made by fermenting corn sugar: [[C6H12O6 -> 2 C2H5OH + 2 CO2]]. From 64.0 g of glucose at an 82.0% yield, what mass of ethanol is collected? " + MMS('C6H12O6', 'C2H5OH'),
  [num(x) + " g {C2H5OH}", num(th) + " g {C2H5OH}", num(th / D('0.820')) + " g {C2H5OH}", num(th / 2 * D('0.820')) + " g {C2H5OH}"],
  ["Theoretical: 64.0 &divide; 180.156 &times; 2 &times; 46.069 = 32.73 g; actual = 0.820 &times; 32.73 g.",
   "This is the theoretical yield; the 82.0% has not been applied.",
   "This divides by 0.820, which gives more than the theoretical yield.",
   "This skips the mole ratio (each glucose makes 2 ethanol)."],
  "Theoretical yield first, then take 82.0% of it.",
  "Theoretical 32.73 g &times; 0.820 = <b>" + num(x) + " g {C2H5OH}</b>.", 3, 1)

th = D('0.825') / mm('Al') * mm('KAl(SO4)2.12H2O'); x = D('12.9') / th
Q(T, "In the alum synthesis lab, each Al atom ends up in one formula unit of alum, {KAl(SO4)2.12H2O}. A student starts with 0.825 g of Al and collects 12.9 g of dry alum. What is the percent yield? (Al 26.98 g/mol; {KAl(SO4)2.12H2O} " + G('KAl(SO4)2.12H2O') + " g/mol; {KAl(SO4)2} " + G('KAl(SO4)2') + " g/mol)",
  [pct(x), pct(1 / x), pct(D('12.9') / (D('0.825') / mm('Al') * mm('KAl(SO4)2'))), num(x) + "%"],
  ["Theoretical: 0.825 g &divide; 26.98 g/mol = 0.03058 mol Al = 0.03058 mol alum; &times; 474.37 g/mol = 14.51 g. 12.9 &divide; 14.51 &times; 100%.",
   "This divides theoretical by actual.",
   "This uses the molar mass without the 12 waters. The crystals contain the water, so the hydrate's molar mass is needed; leaving it out gives a yield over 100%.",
   "This forgets to multiply the fraction by 100%."],
  "The product is the hydrate. Which molar mass belongs to it?",
  "Theoretical = 0.03058 mol &times; 474.37 g/mol = 14.51 g; 12.9 &divide; 14.51 &times; 100% = <b>" + pct(x) + "</b>.", 3, 1)

# ======================= ch08-enthalpy (10) =======================
T = 'ch08-enthalpy'
Q(T, "Hydrogen fuel cells run on [[2 H2(g) + O2(g) -> 2 H2O(l)]], " + DH(M + '571.6') + ". Which describes this reaction?",
  ["Exothermic: heat is released and the surroundings warm up", "Endothermic: heat is absorbed and the surroundings cool down",
   "Exothermic: heat is absorbed from the surroundings", "Endothermic, because &Delta;H is a large number"],
  ["A negative &Delta;H means the reaction releases heat to its surroundings.",
   "Endothermic reactions have a positive &Delta;H.",
   "Exothermic means heat is released, not absorbed.",
   "The sign, not the size, of &Delta;H tells you exo or endo."],
  "Negative &Delta;H: released or absorbed?",
  "&Delta;H &lt; 0, so the reaction is <b>exothermic</b>: 571.6 kJ is released per 2 mol {H2}.", 1)

Q(T, "An instant cold pack gets cold when ammonium nitrate dissolves in water. Which statement is true about this process?",
  ["It is endothermic, &Delta;H &gt; 0: it absorbs heat from your skin.", "It is exothermic, &Delta;H &lt; 0: it absorbs heat.",
   "It is exothermic, &Delta;H &lt; 0: cold is released into the pack.", "It is endothermic, &Delta;H &lt; 0."],
  ["The pack takes heat from its surroundings, including an injury, so the surroundings cool. That is endothermic, with a positive &Delta;H.",
   "Exothermic processes release heat; this one absorbs it.",
   "Cold is not a substance that can be released; the process absorbs heat.",
   "Endothermic processes have a positive &Delta;H."],
  "Does the pack take heat in or give heat out?",
  "The cold pack absorbs heat: <b>endothermic, &Delta;H &gt; 0</b>.", 1)

Q(T, "Heating limestone is endothermic: [[CaCO3(s) -> CaO(s) + CO2(g)]], " + DH('+178') + ". What is &Delta;H for the reverse reaction, [[CaO(s) + CO2(g) -> CaCO3(s)]]?",
  [M + "178 kJ", "+178 kJ", M + "356 kJ", "+89 kJ"],
  ["Reversing an equation changes the sign of &Delta;H; the size stays 178 kJ for 1 mol.",
   "The reverse reaction releases the heat the forward one absorbs, so the sign changes.",
   "Doubling would apply if the coefficients were doubled; they are not.",
   "Halving would apply to half the amounts. Reversing changes only the sign."],
  "Reverse the equation, reverse the sign.",
  "Reverse reaction: <b>&Delta;H = " + M + "178 kJ</b> (exothermic).", 2)

Q(T, "Given [[2 H2(g) + O2(g) -> 2 H2O(l)]], " + DH(M + '571.6') + ", what is &Delta;H for [[4 H2(g) + 2 O2(g) -> 4 H2O(l)]]?",
  [M + "1143.2 kJ", M + "571.6 kJ", "+1143.2 kJ", M + "285.8 kJ"],
  ["Every coefficient is doubled, so &Delta;H doubles: 2 &times; (" + M + "571.6 kJ).",
   "&Delta;H belongs to the amounts as written; twice the amounts release twice the heat.",
   "The reaction is still the same direction, so the sign stays negative.",
   "This halves &Delta;H; the coefficients were doubled, not halved."],
  "Double the equation, double &Delta;H.",
  "2 &times; (" + M + "571.6 kJ) = <b>" + M + "1143.2 kJ</b>.", 2)

x = D('1.35') * D('571.6')
Q(T, "For [[2 H2(g) + O2(g) -> 2 H2O(l)]], " + DH(M + '571.6') + ", how much heat is released when 1.35 mol of {O2} reacts?",
  [num(x) + " kJ released", num(x / 2) + " kJ released", num(x * 2) + " kJ released", num(x) + " kJ absorbed"],
  ["1.35 mol {O2} &times; (571.6 kJ / 1 mol {O2}). The 571.6 kJ goes with 1 mol {O2}, the coefficient of {O2}.",
   "This uses the coefficient of {H2} (2). The question is about {O2}, whose coefficient is 1.",
   "This doubles the heat; 571.6 kJ is released per 1 mol of {O2}, not per half mole.",
   "A negative &Delta;H means heat is released, not absorbed."],
  "Which coefficient goes with the 571.6 kJ when you start from {O2}?",
  "1.35 mol {O2} &times; (571.6 kJ / 1 mol {O2}) = <b>" + num(x) + " kJ released</b>.", 2, 1)

x = D('5.00') / mm('C3H8') * D('2220')
Q(T, "A propane camp stove burns fuel by [[C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(l)]], " + DH(PROPANE) + ". How much heat is released when 5.00 g of propane burns? " + MMS('C3H8'),
  [num(x) + " kJ released", num(D('5.00') * D('2220')) + " kJ released", num(x / 5) + " kJ released", num(x) + " kJ absorbed"],
  ["5.00 g &divide; 44.097 g/mol = 0.1134 mol propane; &times; 2220 kJ/mol.",
   "This multiplies grams by &Delta;H. &Delta;H goes with moles; convert grams to moles first.",
   "This divides by 5, the coefficient of {O2}. The heat per mole of propane is 2220 kJ (coefficient 1).",
   "Negative &Delta;H means heat is released."],
  "grams &rarr; moles &rarr; kJ.",
  "5.00 g &times; (1 mol / 44.097 g) &times; (2.220 &times; 10<sup>3</sup> kJ / 1 mol {C3H8}) = <b>" + num(x) + " kJ released</b>.", 2, 1)

n_ = D('3.60e4') / D('890.3')
Q(T, "A Valley dairy digester burns captured methane, [[CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(l)]], " + DH(M + '890.3') + ". What mass of methane must burn to release 3.60 &times; 10<sup>4</sup> kJ? " + MMS('CH4'),
  [num(n_ * mm('CH4')) + " g {CH4}", num(n_) + " mol {CH4}", num(n_ / mm('CH4')) + " g {CH4}", num(n_ / 2 * mm('CH4')) + " g {CH4}"],
  ["3.60 &times; 10<sup>4</sup> kJ &divide; 890.3 kJ/mol = 40.44 mol {CH4}; &times; 16.043 g/mol.",
   "This stops at moles of methane.",
   "This divides by the molar mass instead of multiplying.",
   "This uses the coefficient of {O2} (2). The 890.3 kJ goes with 1 mol {CH4}."],
  "Work backward: kJ &rarr; mol {CH4} &rarr; g {CH4}.",
  "3.60 &times; 10<sup>4</sup> kJ &times; (1 mol {CH4} / 890.3 kJ) &times; (16.043 g / 1 mol) = <b>" + num(n_ * mm('CH4')) + " g {CH4}</b>.", 3, 1)

x = D('5.40') / mm('C6H12O6') * D('2803')
Q(T, "Your cells oxidize glucose: [[C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O]], " + DH(M + '2803') + ". How much heat is released by 5.40 g of glucose? " + MMS('C6H12O6'),
  [num(x) + " kJ released", num(D('5.40') * D('2803')) + " kJ released", num(x / 6) + " kJ released", num(x / D('4.184')) + " kJ released"],
  ["5.40 g &divide; 180.156 g/mol = 0.02997 mol; &times; 2803 kJ/mol.",
   "This multiplies grams by &Delta;H; convert to moles first.",
   "This divides by 6, the coefficient of {O2}. 2803 kJ goes with 1 mol glucose.",
   "This divides by 4.184, which converts kJ into kcal (Calories). The number is then in kcal, not kJ."],
  "&Delta;H is per mole of glucose as written.",
  "5.40 g &times; (1 mol / 180.156 g) &times; (2803 kJ / 1 mol) = <b>" + num(x) + " kJ released</b>.", 2, 1)

kj = D('12.0') / mm('C6H12O6') * D('2803'); x = kj / D('4.184')
Q(T, "A food label counts the energy in carbohydrates in Calories (1 Cal = 4.184 kJ). Using [[C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O]], " + DH(M + '2803') + ", how many Calories does 12.0 g of glucose release? " + MMS('C6H12O6'),
  [num(x) + " Cal", num(kj) + " Cal", num(kj * D('4.184')) + " Cal", num(x / 6) + " Cal"],
  ["12.0 g &divide; 180.156 g/mol &times; 2803 kJ/mol = 186.7 kJ; &divide; 4.184 kJ/Cal.",
   "This is the heat in kJ with a Cal label. Divide by 4.184 kJ/Cal.",
   "This multiplies by 4.184; kJ &rarr; Cal means dividing, since a Calorie is bigger than a kJ.",
   "This divides by 6, the coefficient of {O2}."],
  "kJ first, then kJ &rarr; Cal.",
  "12.0 g &times; (1 mol / 180.156 g) &times; (2803 kJ / 1 mol) &times; (1 Cal / 4.184 kJ) = <b>" + num(x) + " Cal</b>, about 3.7 Cal per gram.", 3, 1)

x = D('35.0') / mm('CaCO3') * 178
Q(T, "Decomposing limestone absorbs heat: [[CaCO3(s) -> CaO(s) + CO2(g)]], " + DH('+178') + ". How much heat is needed to decompose 35.0 g of {CaCO3}? " + MMS('CaCO3'),
  [num(x) + " kJ absorbed", num(x) + " kJ released", num(D('35.0') * 178) + " kJ absorbed", num(D('35.0') / mm('CaCO3')) + " mol {CaCO3}"],
  ["35.0 g &divide; 100.09 g/mol = 0.3497 mol; &times; 178 kJ/mol, absorbed because &Delta;H is positive.",
   "A positive &Delta;H means heat is absorbed, not released.",
   "This multiplies grams by &Delta;H; convert to moles first.",
   "This stops at moles; multiply by 178 kJ/mol."],
  "Positive &Delta;H: heat is needed. grams &rarr; moles &rarr; kJ.",
  "35.0 g &times; (1 mol / 100.09 g) &times; (178 kJ / 1 mol) = <b>" + num(x) + " kJ absorbed</b>.", 2, 1)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')),
      'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
