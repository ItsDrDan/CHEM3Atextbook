#!/usr/bin/env python3
"""Builds bank/ch08_adapt.json (Chapter 8 ADAPT homework-only items, text only; 42 items, none repeated from
bank/ch08.json).
usage: python3 tools/gen_adapt_ch08.py bank/ch08_adapt.json
Same conventions, helpers and markup as tools/gen_bank_ch08.py (yellow-sheet masses with the addition rule, STP
22.4 L/mol, standard Delta H values only, sig figs from the givens, no trailing-zero givens without a decimal point).
y[0] begins "Correct: ". Every item is rechecked by tools/check_bank_ch08.py."""
import json, sys, re, os, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
MS = json.load(open(os.path.join(HERE, 'yellow_sheet_masses.json')))['masses']
M = '&minus;'
B = []
PREFIX = 'c8-h%02d'

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
    y = ["Correct: " + y[0]] + y[1:]
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


# ======================= ch08-moleratio (7) =======================
T = 'ch08-moleratio'
x = D('0.620') * 3 / 2
Q(T, "Heating potassium chlorate releases oxygen: [[2 KClO3(s) -> 2 KCl(s) + 3 O2(g)]]. How many moles of {O2} form from 0.620 mol of {KClO3}?",
  [num(x) + " mol {O2}", num(D('0.620') * 2 / 3) + " mol {O2}", "0.620 mol {O2}", num(D('0.620') * 3) + " mol {O2}"],
  ["0.620 mol {KClO3} &times; (3 mol {O2} / 2 mol {KClO3}).",
   "This uses 2/3, the ratio upside down.",
   "This skips the mole ratio; the coefficients are 2 and 3.",
   "This uses 3/1, leaving out the coefficient 2 on {KClO3}."],
  "Both coefficients, 2 and 3, belong in the ratio.",
  "0.620 mol {KClO3} &times; (3 mol {O2} / 2 mol {KClO3}) = <b>" + num(x) + " mol {O2}</b>.", 1, 1)

x = D('5.30') * 3 / 2
Q(T, "For ammonia fertilizer, [[N2(g) + 3 H2(g) -> 2 NH3(g)]]. How many moles of {H2} are needed to make 5.30 mol of {NH3}?",
  [num(x) + " mol {H2}", num(D('5.30') * 2 / 3) + " mol {H2}", "5.30 mol {H2}", num(D('5.30') * 3) + " mol {H2}"],
  ["5.30 mol {NH3} &times; (3 mol {H2} / 2 mol {NH3}).",
   "This uses 2/3, the ratio upside down.",
   "This skips the mole ratio.",
   "This uses 3/1, leaving out the coefficient 2 on {NH3}."],
  "Want {H2} on top, have {NH3} on the bottom.",
  "5.30 mol {NH3} &times; (3 mol {H2} / 2 mol {NH3}) = <b>" + num(x) + " mol {H2}</b>.", 2, 1)

x = D('0.715') * 2 / 3
Q(T, "Ethanol burns in a fuel blend by [[C2H5OH(l) + 3 O2(g) -> 2 CO2(g) + 3 H2O(g)]]. How many moles of {CO2} form when 0.715 mol of {O2} is used?",
  [num(x) + " mol {CO2}", num(D('0.715') * 3 / 2) + " mol {CO2}", "0.715 mol {CO2}", num(D('0.715') * 2) + " mol {CO2}"],
  ["The coefficients of {CO2} (2) and {O2} (3) make the ratio: 0.715 &times; 2/3.",
   "This uses 3/2, the ratio upside down.",
   "This skips the mole ratio.",
   "This uses 2/1, leaving out the coefficient 3 on {O2}."],
  "Link {O2} to {CO2} with their own coefficients.",
  "0.715 mol {O2} &times; (2 mol {CO2} / 3 mol {O2}) = <b>" + num(x) + " mol {CO2}</b>.", 2, 1)

Q(T, "Photosynthesis is [[6 CO2(g) + 6 H2O(l) -> C6H12O6(aq) + 6 O2(g)]]. Which factor converts moles of {CO2} used into moles of glucose made?",
  ["1 mol {C6H12O6} / 6 mol {CO2}", "6 mol {CO2} / 1 mol {C6H12O6}", "6 mol {C6H12O6} / 6 mol {CO2}", "1 mol {C6H12O6} / 6 mol {O2}"],
  ["Glucose has coefficient 1 and {CO2} has 6; mol {CO2} on the bottom cancels.",
   "This is upside down: mol {CO2} would not cancel.",
   "The 6 in C<sub>6</sub> is a subscript, not the coefficient of glucose.",
   "This links glucose to {O2}, not to {CO2}."],
  "Glucose's coefficient is 1 (not written).",
  "mol {CO2} &times; <b>(1 mol {C6H12O6} / 6 mol {CO2})</b> = mol glucose.", 1)

x = 2 * mm('Na')
Q(T, "For [[2 Na(s) + Cl2(g) -> 2 NaCl(s)]], what mass of sodium reacts with exactly 1 mol of {Cl2}? (Na 22.99 g/mol)",
  [str(x) + " g Na", MS['Na'] + " g Na", str(2 * mm('Cl2')) + " g Na", "2 g Na"],
  ["1 mol {Cl2} reacts with 2 mol Na, and 2 mol &times; 22.99 g/mol = 45.98 g.",
   "This is 1 mol of Na. The equation needs 2 mol Na per mol {Cl2}.",
   "This is the mass of 2 mol of {Cl2} (2 &times; 70.90 g), not of sodium.",
   "This reads the coefficient as grams. Coefficients are moles."],
  "Coefficient = moles; then use the molar mass of Na.",
  "1 mol {Cl2} &times; (2 mol Na / 1 mol {Cl2}) &times; 22.99 g/mol = <b>" + str(x) + " g Na</b>.", 2, 1)

x = D('3.52') * 11 / 8
Q(T, "Roasting pyrite ore, [[4 FeS2(s) + 11 O2(g) -> 2 Fe2O3(s) + 8 SO2(g)]], releases sulfur dioxide. How many moles of {O2} are used when 3.52 mol of {SO2} forms?",
  [num(x) + " mol {O2}", num(D('3.52') * 8 / 11) + " mol {O2}", "3.52 mol {O2}", num(D('3.52') * 11 / 4) + " mol {O2}"],
  ["3.52 mol {SO2} &times; (11 mol {O2} / 8 mol {SO2}).",
   "This uses 8/11, the ratio upside down.",
   "This skips the mole ratio.",
   "This uses 4, the coefficient of {FeS2}, instead of 8 for {SO2}."],
  "Use the coefficients of {O2} and {SO2} only.",
  "3.52 mol {SO2} &times; (11 mol {O2} / 8 mol {SO2}) = <b>" + num(x) + " mol {O2}</b>.", 3, 1)

Q(T, "A student writes the unbalanced equation [[H2(g) + O2(g) -> H2O(l)]] and uses 1 mol {H2O} / 1 mol {O2}. After balancing, how many moles of {H2O} form per mole of {O2}?",
  ["2 mol {H2O} per 1 mol {O2}", "1 mol {H2O} per 1 mol {O2}", "1 mol {H2O} per 2 mol {O2}", "3 mol {H2O} per 1 mol {O2}"],
  ["Balanced: 2 {H2} + {O2} &rarr; 2 {H2O}. One {O2} makes two waters.",
   "That ratio comes from the unbalanced equation; it has 2 O on the left and only 1 on the right.",
   "This is upside down.",
   "Coefficients are not added (2 + 1); {H2O}'s coefficient is 2."],
  "Balance the O atoms first.",
  "[[2 H2(g) + O2(g) -> 2 H2O(l)]]: <b>2 mol {H2O} per 1 mol {O2}</b>. Always balance before writing a mole ratio.", 2)

# ======================= ch08-massmass (7) =======================
T = 'ch08-massmass'
n_ = D('6.35') / mm('H2'); x = n_ * mm('H2O')
Q(T, "A hydrogen fuel-cell bus runs on [[2 H2(g) + O2(g) -> 2 H2O(l)]]. What mass of water forms from 6.35 g of {H2}? " + MMS('H2', 'H2O'),
  [num(x) + " g {H2O}", num(n_ * 2 * mm('H2O')) + " g {H2O}", num(D('6.35') * mm('H2') / mm('H2O')) + " g {H2O}", num(n_) + " mol {H2O}"],
  ["6.35 g &divide; 2.016 g/mol = 3.150 mol {H2}; 2 : 2 ratio; &times; 18.015 g/mol.",
   "This multiplies the molar mass of water by its coefficient. The 2 belongs in the mole ratio, where it cancels.",
   "This uses the molar masses upside down.",
   "This stops at moles."],
  "g {H2} &rarr; mol {H2} &rarr; mol {H2O} &rarr; g {H2O}.",
  "6.35 g &times; (1 mol / 2.016 g) &times; (2 mol {H2O} / 2 mol {H2}) &times; (18.015 g / 1 mol) = <b>" + num(x) + " g {H2O}</b>.", 2, 1)

n_ = D('9.20') / mm('C2H5OH'); x = n_ * 2 * mm('CO2')
Q(T, "What mass of {CO2} forms when 9.20 g of ethanol burns? [[C2H5OH(l) + 3 O2(g) -> 2 CO2(g) + 3 H2O(g)]] " + MMS('C2H5OH', 'CO2'),
  [num(x) + " g {CO2}", num(n_ * mm('CO2')) + " g {CO2}", num(n_ / 2 * mm('CO2')) + " g {CO2}", num(n_ * 2 * 2 * mm('CO2')) + " g {CO2}"],
  ["9.20 g &divide; 46.069 g/mol = 0.1997 mol; &times; 2 = 0.3994 mol {CO2}; &times; 44.009 g/mol.",
   "This skips the mole ratio.",
   "This uses 1/2, the ratio upside down.",
   "This uses the 2 twice: in the ratio and on the molar mass."],
  "Each ethanol has 2 C atoms.",
  "9.20 g &times; (1 mol / 46.069 g) &times; (2 mol {CO2} / 1 mol) &times; (44.009 g / 1 mol) = <b>" + num(x) + " g {CO2}</b>.", 2, 1)

n_ = D('48.5') / mm('CO(NH2)2'); x = n_ * 2 * mm('NH3')
Q(T, "Urea fertilizer is made by [[2 NH3(g) + CO2(g) -> CO(NH2)2(s) + H2O(g)]]. What mass of {NH3} is needed to make 48.5 g of urea? " + MMS('CO(NH2)2', 'NH3'),
  [num(x) + " g {NH3}", num(n_ * mm('NH3')) + " g {NH3}", num(n_ / 2 * mm('NH3')) + " g {NH3}", num(n_ * 2 * 2 * mm('NH3')) + " g {NH3}"],
  ["48.5 g &divide; 60.056 g/mol = 0.8076 mol urea; &times; 2 = 1.615 mol {NH3}; &times; 17.031 g/mol.",
   "This skips the mole ratio (2 {NH3} : 1 urea).",
   "This uses 1/2, the ratio upside down.",
   "This puts the coefficient 2 into the molar mass as well."],
  "Work backward from the product.",
  "48.5 g urea &times; (1 mol / 60.056 g) &times; (2 mol {NH3} / 1 mol urea) &times; (17.031 g / 1 mol) = <b>" + num(x) + " g {NH3}</b>.", 3, 1)

n_ = D('5.75') / mm('CH4'); x = n_ * 2 * mm('H2O')
Q(T, "Natural gas burns by [[CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(l)]]. What mass of water forms from 5.75 g of {CH4}? " + MMS('CH4', 'H2O'),
  [num(x) + " g {H2O}", num(n_ * mm('H2O')) + " g {H2O}", num(n_ / 2 * mm('H2O')) + " g {H2O}", num(n_ * 2 * 2 * mm('H2O')) + " g {H2O}"],
  ["5.75 g &divide; 16.043 g/mol = 0.3584 mol {CH4}; &times; 2 = 0.7168 mol {H2O}; &times; 18.015 g/mol.",
   "This skips the mole ratio.",
   "This uses 1/2, the ratio upside down.",
   "This uses the coefficient twice."],
  "One {CH4} makes two {H2O}.",
  "5.75 g &times; (1 mol / 16.043 g) &times; (2 mol {H2O} / 1 mol {CH4}) &times; (18.015 g / 1 mol) = <b>" + num(x) + " g {H2O}</b>.", 2, 1)

n_ = D('2.15') / mm('NaCl'); x = n_ * mm('AgCl')
Q(T, "A lab tests for chloride with silver nitrate: [[AgNO3(aq) + NaCl(aq) -> AgCl(s) + NaNO3(aq)]]. What mass of AgCl precipitate forms from 2.15 g of NaCl? " + MMS('NaCl', 'AgCl'),
  [num(x) + " g AgCl", "2.15 g AgCl", num(D('2.15') * mm('NaCl') / mm('AgCl')) + " g AgCl", num(n_) + " mol AgCl"],
  ["2.15 g &divide; 58.44 g/mol = 0.03679 mol NaCl = 0.03679 mol AgCl; &times; 143.32 g/mol.",
   "A 1 : 1 mole ratio is not a 1 : 1 mass ratio; AgCl is much heavier than NaCl.",
   "This uses the molar masses upside down.",
   "This stops at moles."],
  "1 : 1 in moles; molar masses differ.",
  "2.15 g &times; (1 mol / 58.44 g) &times; (1 mol AgCl / 1 mol NaCl) &times; (143.32 g / 1 mol) = <b>" + num(x) + " g AgCl</b>.", 3, 1)

Q(T, "In a mass-to-mass problem, which step is the only one that uses the coefficients of the balanced equation?",
  ["mol A &rarr; mol B", "g A &rarr; mol A", "mol B &rarr; g B", "g A &rarr; g B"],
  ["The mole ratio, from the coefficients, is the bridge between two substances.",
   "This step uses the molar mass of A, not the coefficients.",
   "This step uses the molar mass of B.",
   "There is no direct grams-to-grams step; coefficients are mole ratios."],
  "Which step is the bridge on the road map?",
  "Only <b>mol A &rarr; mol B</b> uses the coefficients.", 1)

n_ = D('0.350') / mm('Mg(OH)2'); x = n_ * 2 * mm('HCl')
Q(T, "Milk of magnesia neutralizes stomach acid: [[Mg(OH)2(s) + 2 HCl(aq) -> MgCl2(aq) + 2 H2O(l)]]. What mass of HCl can 0.350 g of {Mg(OH)2} neutralize? " + MMS('Mg(OH)2', 'HCl'),
  [num(x) + " g HCl", num(n_ * mm('HCl')) + " g HCl", num(n_ / 2 * mm('HCl')) + " g HCl", num(n_ * 2 * 2 * mm('HCl')) + " g HCl"],
  ["0.350 g &divide; 58.32 g/mol = 0.006001 mol; &times; 2 = 0.01200 mol HCl; &times; 36.46 g/mol.",
   "This skips the mole ratio.",
   "This uses 1/2, the ratio upside down.",
   "This uses the coefficient twice."],
  "One {Mg(OH)2} neutralizes two HCl.",
  "0.350 g &times; (1 mol / 58.32 g) &times; (2 mol HCl / 1 mol) &times; (36.46 g / 1 mol) = <b>" + num(x) + " g HCl</b>. (Context only; follow the label.)", 2, 1)

# ======================= ch08-solgas (7) =======================
T = 'ch08-solgas'
x = D('0.125') * D('0.0400')
Q(T, "How many moles of glucose are in 125 mL of a 0.0400 M glucose solution?",
  [num(x) + " mol", num(D('125') * D('0.0400')) + " mol", num(D('0.125') / D('0.0400')) + " mol", num(D('0.0400') / D('125')) + " mol"],
  ["125 mL = 0.125 L; 0.125 L &times; 0.0400 mol/L.",
   "This uses mL with molarity; convert to L first.",
   "This divides volume by molarity.",
   "This divides molarity by the mL volume."],
  "moles = liters &times; molarity.",
  "0.125 L &times; 0.0400 mol/L = <b>" + num(x) + " mol</b> glucose.", 1, 1)

n_ = D('0.875') / 2; x = n_ * D('22.4')
Q(T, "What volume of {N2} at STP is needed to make 0.875 mol of {NH3}? [[N2(g) + 3 H2(g) -> 2 NH3(g)]]",
  [num(x) + " L {N2}", num(D('0.875') * D('22.4')) + " L {N2}", num(D('0.875') * 2 * D('22.4')) + " L {N2}", num(n_) + " mol {N2}"],
  ["0.875 mol {NH3} &times; 1/2 = 0.4375 mol {N2}; &times; 22.4 L/mol.",
   "This skips the mole ratio.",
   "This uses 2/1, the ratio upside down.",
   "This stops at moles."],
  "Mole ratio, then 22.4 L/mol.",
  "0.875 mol {NH3} &times; (1 mol {N2} / 2 mol {NH3}) &times; (22.4 L / 1 mol) = <b>" + num(x) + " L {N2}</b>.", 2, 1)

n_ = D('0.0200') * D('0.115'); x = n_ * mm('AgCl')
Q(T, "What mass of AgCl forms when 20.0 mL of 0.115 M {AgNO3} reacts with excess NaCl? [[AgNO3(aq) + NaCl(aq) -> AgCl(s) + NaNO3(aq)]] " + MMS('AgCl', 'AgNO3'),
  [num(x) + " g AgCl", num(D('20.0') * D('0.115') * mm('AgCl')) + " g AgCl", num(n_) + " mol AgCl", num(n_ * mm('AgNO3')) + " g AgCl"],
  ["0.0200 L &times; 0.115 M = 0.00230 mol {AgNO3} = 0.00230 mol AgCl; &times; 143.32 g/mol.",
   "This uses 20.0 mL as liters; the answer is 1000 times too large.",
   "This stops at moles.",
   "This uses the molar mass of {AgNO3}; the product is AgCl."],
  "L &times; M = mol; then the molar mass of the product.",
  "0.0200 L &times; 0.115 mol/L &times; (1 mol AgCl / 1 mol {AgNO3}) &times; 143.32 g/mol = <b>" + num(x) + " g AgCl</b>.", 2, 1)

n_ = D('3.85') / mm('C3H8') * 3; x = n_ * D('22.4')
Q(T, "What volume of {CO2} at STP forms when 3.85 g of propane burns? [[C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(l)]] " + MMS('C3H8'),
  [num(x) + " L {CO2}", num(n_ / 3 * D('22.4')) + " L {CO2}", num(n_ / 9 * D('22.4')) + " L {CO2}", num(n_) + " mol {CO2}"],
  ["3.85 g &divide; 44.097 g/mol = 0.08731 mol; &times; 3 = 0.2619 mol {CO2}; &times; 22.4 L/mol.",
   "This skips the mole ratio.",
   "This uses 1/3, the ratio upside down.",
   "This stops at moles."],
  "g &rarr; mol propane &rarr; mol {CO2} &rarr; L.",
  "3.85 g &times; (1 mol / 44.097 g) &times; (3 mol {CO2} / 1 mol) &times; (22.4 L / 1 mol) = <b>" + num(x) + " L {CO2}</b>.", 3, 1)

Q(T, "A respiratory therapist measures the volume of exhaled {CO2} at body temperature (37 &deg;C) and 1 atm. Why can't 22.4 L/mol convert this volume to moles?",
  ["22.4 L/mol holds only at STP, 0 &deg;C and 1 atm; at 37 &deg;C a mole of gas fills more than 22.4 L.",
   "22.4 L/mol works only for {O2}, not {CO2}.",
   "Exhaled gas is a liquid at 37 &deg;C.",
   "It can; 22.4 L/mol holds at any temperature."],
  ["Gases expand when warmed, so the molar volume at 37 &deg;C is larger than 22.4 L.",
   "At STP, 22.4 L/mol holds for any ideal gas, not just {O2}.",
   "{CO2} is a gas at body temperature.",
   "The molar volume depends on temperature and pressure."],
  "What does STP stand for?",
  "<b>22.4 L/mol applies only at STP (0 &deg;C, 1 atm)</b>; at body temperature a mole of gas occupies more volume (Chapter 10).", 2)

n_ = D('0.0450') * D('0.0800') / 2; x = n_ * mm('Mg(OH)2')
Q(T, "What mass of {Mg(OH)2} neutralizes 45.0 mL of 0.0800 M HCl? [[Mg(OH)2(s) + 2 HCl(aq) -> MgCl2(aq) + 2 H2O(l)]] " + MMS('Mg(OH)2'),
  [num(x) + " g {Mg(OH)2}", num(n_ * 2 * mm('Mg(OH)2')) + " g {Mg(OH)2}", num(D('45.0') * D('0.0800') / 2 * mm('Mg(OH)2')) + " g {Mg(OH)2}", num(n_ * 4 * mm('Mg(OH)2')) + " g {Mg(OH)2}"],
  ["0.0450 L &times; 0.0800 M = 0.00360 mol HCl; &times; 1/2 = 0.00180 mol; &times; 58.32 g/mol.",
   "This skips the mole ratio.",
   "This uses mL as liters.",
   "This uses 2/1, the ratio upside down."],
  "mL &rarr; L &rarr; mol HCl &rarr; mol {Mg(OH)2} &rarr; g.",
  "0.0450 L &times; 0.0800 mol/L &times; (1 mol {Mg(OH)2} / 2 mol HCl) &times; 58.32 g/mol = <b>" + num(x) + " g {Mg(OH)2}</b>.", 3, 1)

n_ = D('8.00') / mm('CH4') * 2; x = n_ * D('22.4')
Q(T, "Biogas methane from a dairy digester burns by [[CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(l)]]. What volume of {O2} at STP is needed to burn 8.00 g of {CH4}? " + MMS('CH4'),
  [num(x) + " L {O2}", num(n_ / 2 * D('22.4')) + " L {O2}", num(n_ / 4 * D('22.4')) + " L {O2}", num(n_) + " mol {O2}"],
  ["8.00 g &divide; 16.043 g/mol = 0.4987 mol {CH4}; &times; 2 = 0.9973 mol {O2}; &times; 22.4 L/mol.",
   "This skips the mole ratio.",
   "This uses 1/2, the ratio upside down.",
   "This stops at moles."],
  "Each {CH4} needs two {O2}.",
  "8.00 g &times; (1 mol / 16.043 g) &times; (2 mol {O2} / 1 mol {CH4}) &times; (22.4 L / 1 mol) = <b>" + num(x) + " L {O2}</b>.", 2, 1)

# ======================= ch08-limiting (7) =======================
T = 'ch08-limiting'
Q(T, "Natural gas burns by [[CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(l)]]. A mixture of 1.50 mol {CH4} and 2.40 mol {O2} burns. What is the most {CO2} that can form?",
  ["1.20 mol {CO2}", "1.50 mol {CO2}", "2.70 mol {CO2}", "4.80 mol {CO2}"],
  ["From {CH4}: 1.50 mol {CO2}; from {O2}: 2.40 &times; 1/2 = 1.20 mol. {O2} is limiting, even though there are more moles of it.",
   "This is what the {CH4}, the excess reactant, could make.",
   "This adds the two possible amounts; the smaller one is the answer.",
   "This uses 2/1, the ratio upside down."],
  "Compute the {CO2} each reactant could make.",
  "{CH4} &rarr; 1.50 mol; {O2} &rarr; 1.20 mol. <b>{O2} limits: 1.20 mol {CO2}</b>.", 2, 1)

Q(T, "For [[Fe2O3(s) + 3 CO(g) -> 2 Fe(l) + 3 CO2(g)]], 0.40 mol {Fe2O3} and 0.90 mol CO react. Which reactant is limiting?",
  ["CO, because it can make only 0.60 mol Fe", "{Fe2O3}, because there are fewer moles of it",
   "{Fe2O3}, because it has the smaller coefficient", "Neither; they are in the exact ratio"],
  ["{Fe2O3}: 0.40 &times; 2 = 0.80 mol Fe; CO: 0.90 &times; 2/3 = 0.60 mol Fe. CO makes less.",
   "Fewer moles does not mean limiting when the coefficients differ.",
   "A smaller coefficient means less of it is needed, not that it runs out first.",
   "0.40 mol {Fe2O3} needs 1.20 mol CO; only 0.90 mol is present."],
  "Convert both to moles of Fe.",
  "{Fe2O3} &rarr; 0.80 mol Fe; CO &rarr; 0.60 mol Fe. <b>CO is limiting</b>.", 2)

nAl = D('5.40') / mm('Al'); nF = D('18.0') / mm('Fe2O3')
Q(T, "A thermite mixture holds 5.40 g of Al and 18.0 g of {Fe2O3}: [[Fe2O3(s) + 2 Al(s) -> Al2O3(s) + 2 Fe(l)]]. What is the maximum mass of iron? " + MMS('Al', 'Fe2O3', 'Fe'),
  [num(nAl * mm('Fe')) + " g Fe", num(nF * 2 * mm('Fe')) + " g Fe", num(nF * mm('Fe')) + " g Fe", "23.4 g Fe"],
  ["Al: 0.2001 mol &rarr; 0.2001 mol Fe; {Fe2O3}: 0.1127 mol &rarr; 0.2254 mol Fe. Al is limiting: 0.2001 &times; 55.85 g/mol.",
   "This uses {Fe2O3}, the excess reactant.",
   "This skips the 2 : 1 ratio for {Fe2O3} and Fe.",
   "This adds the reactant masses."],
  "Each reactant &rarr; mol Fe; the smaller wins.",
  "Al &rarr; 0.2001 mol Fe (less than 0.2254), so Al limits: 0.2001 &times; 55.85 = <b>" + num(nAl * mm('Fe')) + " g Fe</b>.", 3, 1)

Q(T, "For [[N2(g) + 3 H2(g) -> 2 NH3(g)]], 2.60 mol {N2} and 6.30 mol {H2} react. How many moles of the excess reactant are left?",
  ["0.50 mol {N2}", "2.10 mol {N2}", "3.70 mol", "None; both are used up"],
  ["{N2} &rarr; 5.20 mol {NH3}; {H2} &rarr; 4.20 mol. {H2} limits. {N2} used: 6.30 &times; 1/3 = 2.10 mol; left: 2.60 &minus; 2.10 = 0.50 mol.",
   "2.10 mol is the {N2} that reacts, not what is left.",
   "This subtracts the two reactants (6.30 &minus; 2.60).",
   "6.30 mol {H2} needs only 2.10 mol {N2}, so some {N2} remains."],
  "Limiting first; then the excess used; then subtract.",
  "{H2} limits; {N2} used = 2.10 mol; left = 2.60 &minus; 2.10 = <b>0.50 mol {N2}</b>.", 3, 1)

Q(T, "Which statement about the <b>excess reactant</b> is true?",
  ["Some of it is left over when the reaction stops.", "It decides the maximum amount of product.",
   "It is always the reactant with the larger mass.", "It is used up first."],
  ["The limiting reactant runs out first, leaving some of the excess reactant unreacted.",
   "The limiting reactant sets the maximum product.",
   "Mass alone does not decide; the mole ratio does.",
   "That describes the limiting reactant."],
  "Excess = more than enough.",
  "The excess reactant is <b>partly left over</b> when the limiting reactant runs out.", 1)

Q(T, "A box holds 6 CO molecules and 2 {O2} molecules, which react by [[2 CO(g) + O2(g) -> 2 CO2(g)]]. When the reaction stops, what is in the box?",
  ["4 {CO2} and 2 CO", "6 {CO2} and no CO", "2 {CO2} and 4 CO", "4 {CO2} and 1 {O2}"],
  ["2 {O2} can react with only 4 CO, making 4 {CO2}; {O2} is limiting, and 6 &minus; 4 = 2 CO remain.",
   "6 {CO2} would need 3 {O2}; only 2 are present.",
   "Each {O2} makes 2 {CO2}, so 2 {O2} make 4, not 2.",
   "{O2} is the limiting reactant, so none is left; the leftover is CO."],
  "Each {O2} reacts with 2 CO.",
  "{O2} limits: 2 {O2} + 4 CO &rarr; 4 {CO2}. The box holds <b>4 {CO2} and 2 CO</b>.", 2)

Q(T, "0.180 mol Zn and 0.300 mol HCl react: [[Zn(s) + 2 HCl(aq) -> ZnCl2(aq) + H2(g)]]. What is the most {H2} that can form?",
  ["0.150 mol {H2}", "0.180 mol {H2}", "0.300 mol {H2}", "0.360 mol {H2}"],
  ["Zn &rarr; 0.180 mol {H2}; HCl &rarr; 0.300 &times; 1/2 = 0.150 mol {H2}. HCl is limiting.",
   "This is what Zn, the excess reactant, could make.",
   "This skips the 2 HCl : 1 {H2} ratio.",
   "This uses 2/1 for Zn; one Zn makes one {H2}."],
  "Each reactant &rarr; mol {H2}.",
  "HCl &rarr; 0.150 mol {H2} (less than 0.180), so <b>HCl limits: 0.150 mol {H2}</b>.", 2, 1)

# ======================= ch08-yield (7) =======================
T = 'ch08-yield'
x = D('5.62') / D('6.48')
Q(T, "A student's theoretical yield is 6.48 g and the actual yield is 5.62 g. What is the percent yield?",
  [pct(x), pct(1 / x), pct(1 - x), num(x) + "%"],
  ["5.62 &divide; 6.48 &times; 100%.",
   "This divides theoretical by actual.",
   "This is the percent lost.",
   "This forgets to multiply by 100%."],
  "actual &divide; theoretical &times; 100%.",
  "5.62 g &divide; 6.48 g &times; 100% = <b>" + pct(x) + "</b>.", 1, 1)

Q(T, "A student's dried product is still mixed with unreacted starting solid, and the reported percent yield is 109%. What does this show?",
  ["The product is impure, so its mass is too high.", "The reaction made extra product from nothing.",
   "The theoretical yield should come from the excess reactant.", "A yield above 100% is normal for solids."],
  ["Leftover reactant in the product adds mass, pushing the yield above 100%.",
   "Mass is conserved; no reaction makes more than its theoretical yield.",
   "Using the excess reactant would give the wrong theoretical yield.",
   "A yield above 100% always signals extra mass, such as water or an impurity."],
  "What could make the product weigh more than possible?",
  "A yield over 100% means <b>extra mass from an impurity</b> (here, unreacted reactant).", 2)

th = D('5.60') / mm('N2') * 2 * mm('NH3'); x = D('5.95') / th
Q(T, "5.60 g of {N2} reacts with excess {H2}: [[N2(g) + 3 H2(g) -> 2 NH3(g)]]. The chemist collects 5.95 g of {NH3}. What is the percent yield? " + MMS('N2', 'NH3'),
  [pct(x), pct(1 / x), pct(D('5.95') / (th / 2)), pct(D('5.95') / D('5.60'))],
  ["Theoretical: 5.60 &divide; 28.014 &times; 2 &times; 17.031 = 6.809 g; 5.95 &divide; 6.809 &times; 100%.",
   "This divides theoretical by actual.",
   "This skips the mole ratio when finding the theoretical yield, which then comes out too small.",
   "This compares the product with the reactant mass."],
  "Theoretical yield first.",
  "Theoretical = 6.809 g; 5.95 &divide; 6.809 &times; 100% = <b>" + pct(x) + "</b>.", 2, 1)

th = D('25.0') / mm('CaCO3') * mm('CaO'); x = th * D('0.915')
Q(T, "Lime is made by [[CaCO3(s) -> CaO(s) + CO2(g)]]. If 25.0 g of {CaCO3} gives a 91.5% yield, what mass of CaO is collected? " + MMS('CaCO3', 'CaO'),
  [num(x) + " g CaO", num(th) + " g CaO", num(th / D('0.915')) + " g CaO", num(D('25.0') * D('0.915')) + " g CaO"],
  ["Theoretical: 25.0 &divide; 100.09 &times; 56.08 = 14.01 g; &times; 0.915.",
   "This is the theoretical yield, before applying 91.5%.",
   "This divides by 0.915.",
   "This applies 91.5% to the mass of {CaCO3}, skipping the stoichiometry."],
  "Theoretical yield, then take 91.5% of it.",
  "14.01 g &times; 0.915 = <b>" + num(x) + " g CaO</b>.", 3, 1)

Q(T, "A student measures the density of copper as 8.72 g/mL; the accepted value is 8.96 g/mL. Which calculation fits this comparison?",
  ["Percent error, because a measurement is compared with an accepted value", "Percent yield, because a product mass is compared with a theoretical yield",
   "Theoretical yield, from the limiting reactant", "Percent yield, because 8.72 is smaller than 8.96"],
  ["Percent error = |measured &minus; accepted| &divide; accepted &times; 100%.",
   "No reaction product is involved; nothing is being made.",
   "There is no reaction and no limiting reactant here.",
   "Being smaller does not make it a yield; the comparison is with an accepted value."],
  "Yield is about making product; error is about measuring.",
  "This is <b>percent error</b>: a measurement compared with an accepted value.", 2)

nFe = D('4.50') / mm('Fe'); nS = D('3.20') / mm('S'); th = nFe * mm('FeS'); x = D('6.25') / th
Q(T, "4.50 g of Fe and 3.20 g of S are heated: [[Fe(s) + S(s) -> FeS(s)]]. The student collects 6.25 g of FeS. What is the percent yield? " + MMS('Fe', 'S', 'FeS'),
  [pct(x), pct(D('6.25') / (nS * mm('FeS'))), pct(1 / x), pct(D('6.25') / D('7.70'))],
  ["Fe: 0.08057 mol; S: 0.09981 mol; Fe limits. Theoretical = 0.08057 &times; 87.91 = 7.083 g; 6.25 &divide; 7.083 &times; 100%.",
   "This uses S, the excess reactant, for the theoretical yield.",
   "This divides theoretical by actual.",
   "This compares with the total reactant mass (7.70 g)."],
  "Find the limiting reactant first.",
  "Fe limits; theoretical 7.083 g FeS; 6.25 &divide; 7.083 &times; 100% = <b>" + pct(x) + "</b>.", 3, 1)

x = D('0.850') * D('0.720')
Q(T, "A drug is made in two steps. Step 1 has an 85.0% yield and step 2 has a 72.0% yield. What is the overall percent yield?",
  [pct(x), pct((D('0.850') + D('0.720')) / 2), pct(D('0.850') + D('0.720')), "13.0%"],
  ["The overall yield is the product of the step yields: 0.850 &times; 0.720.",
   "Averaging does not work; each step loses product from what the last step made.",
   "Adding gives more than 100%, which is impossible.",
   "This is the difference between the two yields."],
  "Step 2 starts with only 85.0% of the possible material.",
  "0.850 &times; 0.720 &times; 100% = <b>" + pct(x) + "</b>.", 2, 1)

# ======================= ch08-enthalpy (7) =======================
T = 'ch08-enthalpy'
Q(T, "Glucose oxidation is [[C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O]], " + DH(M + '2803') + ". What is &Delta;H for photosynthesis, [[6 CO2 + 6 H2O -> C6H12O6 + 6 O2]]?",
  ["+2803 kJ", M + "2803 kJ", "+467.2 kJ", M + "16818 kJ"],
  ["Photosynthesis is the reverse reaction, so the sign changes: it absorbs 2803 kJ per mole of glucose made.",
   "The reverse reaction has the opposite sign.",
   "This divides by 6; the amounts are the same, only reversed.",
   "This multiplies by 6 and keeps the wrong sign."],
  "Reverse the equation, reverse the sign.",
  "<b>&Delta;H = +2803 kJ</b>: photosynthesis is endothermic, powered by sunlight.", 2)

Q(T, "An iron hand warmer gets warm when iron powder rusts in air. Which describes this reaction?",
  ["Exothermic, &Delta;H &lt; 0: heat flows out to your hands", "Endothermic, &Delta;H &gt; 0: heat flows out to your hands",
   "Endothermic, &Delta;H &gt; 0: it absorbs heat from your hands", "Exothermic, &Delta;H &gt; 0"],
  ["The surroundings (your hands) warm up, so the reaction releases heat.",
   "Releasing heat is exothermic, with a negative &Delta;H.",
   "A process that absorbs heat would feel cold.",
   "Exothermic reactions have a negative &Delta;H."],
  "Warm surroundings = heat released.",
  "Heat is released: <b>exothermic, &Delta;H &lt; 0</b>.", 1)

x = D('2.75') * D('890.3') / 2
Q(T, "For [[CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(l)]], " + DH(M + '890.3') + ", how much heat is released when 2.75 mol of {O2} is used?",
  [num(x) + " kJ released", num(x * 2) + " kJ released", num(D('2.75') / D('890.3')) + " kJ released", num(x) + " kJ absorbed"],
  ["2.75 mol {O2} &times; (890.3 kJ / 2 mol {O2}). The 890.3 kJ goes with 2 mol {O2}.",
   "This ignores the coefficient 2 on {O2}.",
   "This divides moles by &Delta;H, upside down.",
   "Negative &Delta;H means heat is released."],
  "890.3 kJ per 2 mol {O2}.",
  "2.75 mol {O2} &times; (890.3 kJ / 2 mol {O2}) = <b>" + num(x) + " kJ released</b>.", 2, 1)

n_ = D('1.50e4') / D('2220')
Q(T, "A propane water heater uses [[C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(l)]], " + DH(PROPANE) + ". What mass of propane must burn to release 1.50 &times; 10<sup>4</sup> kJ? " + MMS('C3H8'),
  [num(n_ * mm('C3H8')) + " g {C3H8}", num(n_) + " mol {C3H8}", num(n_ * 5 * mm('C3H8')) + " g {C3H8}", num(n_ / mm('C3H8')) + " g {C3H8}"],
  ["1.50 &times; 10<sup>4</sup> kJ &divide; 2220 kJ/mol = 6.757 mol; &times; 44.097 g/mol.",
   "This stops at moles.",
   "This multiplies by 5, the coefficient of {O2}.",
   "This divides by the molar mass instead of multiplying."],
  "kJ &rarr; mol &rarr; g.",
  "1.50 &times; 10<sup>4</sup> kJ &times; (1 mol / 2.220 &times; 10<sup>3</sup> kJ) &times; 44.097 g/mol = <b>" + num(n_ * mm('C3H8')) + " g {C3H8}</b>.", 3, 1)

n_ = D('18.5') / mm('H2'); x = n_ * D('571.6') / 2
Q(T, "A hydrogen car runs on [[2 H2(g) + O2(g) -> 2 H2O(l)]], " + DH(M + '571.6') + ". How much heat is released by 18.5 g of {H2}? " + MMS('H2'),
  [num(x) + " kJ released", num(x * 2) + " kJ released", num(D('18.5') * D('571.6') / 2) + " kJ released", num(x) + " kJ absorbed"],
  ["18.5 g &divide; 2.016 g/mol = 9.177 mol {H2}; &times; 571.6 kJ / 2 mol {H2}.",
   "This ignores the coefficient 2 on {H2}.",
   "This uses grams instead of moles.",
   "Negative &Delta;H means heat is released."],
  "571.6 kJ goes with 2 mol {H2}.",
  "18.5 g &times; (1 mol / 2.016 g) &times; (571.6 kJ / 2 mol {H2}) = <b>" + num(x) + " kJ released</b>.", 2, 1)

kj = D('25.0') * D('4.184'); n_ = kj / D('2803')
Q(T, "A sports drink supplies 25.0 Cal from glucose (1 Cal = 4.184 kJ). Using [[C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O]], " + DH(M + '2803') + ", what mass of glucose releases this energy? " + MMS('C6H12O6'),
  [num(n_ * mm('C6H12O6')) + " g", num(D('25.0') / D('2803') * mm('C6H12O6')) + " g", num(n_) + " mol", num(n_ * 6 * mm('C6H12O6')) + " g"],
  ["25.0 Cal &times; 4.184 = 104.6 kJ; &divide; 2803 kJ/mol = 0.03732 mol; &times; 180.156 g/mol.",
   "This uses Calories as if they were kJ; convert with 4.184 kJ/Cal first.",
   "This stops at moles of glucose.",
   "This multiplies by 6, the coefficient of {O2}."],
  "Cal &rarr; kJ &rarr; mol &rarr; g.",
  "25.0 Cal &times; (4.184 kJ / 1 Cal) &times; (1 mol / 2803 kJ) &times; (180.156 g / 1 mol) = <b>" + num(n_ * mm('C6H12O6')) + " g</b> glucose.", 3, 1)

Q(T, "For [[CaCO3(s) -> CaO(s) + CO2(g)]], " + DH('+178') + ". Which statement is true?",
  ["178 kJ is absorbed for every 1 mol of {CaCO3} that decomposes.", "178 kJ is released for every 1 mol of {CaCO3} that decomposes.",
   "178 kJ is absorbed for every 1 g of {CaCO3} that decomposes.", "The reaction absorbs 178 kJ no matter how much {CaCO3} reacts."],
  ["&Delta;H belongs to the moles in the equation: 1 mol {CaCO3}, and the positive sign means absorbed.",
   "A positive &Delta;H means heat is absorbed.",
   "&Delta;H goes with moles, not grams; 1 mol is 100.09 g.",
   "Heat is proportional to the amount that reacts."],
  "Sign: absorbed or released? Amount: per what?",
  "<b>178 kJ is absorbed per 1 mol {CaCO3}</b>; twice as much {CaCO3} absorbs twice the heat.", 2)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
