#!/usr/bin/env python3
"""Builds bank/ch05_adapt.json (Chapter 5 ADAPT homework-only items, text only; 40 items, none repeated from bank/ch05.json).
usage: python3 tools/gen_adapt_ch05.py bank/ch05_adapt.json
Same conventions and helpers as tools/gen_bank_ch05.py (yellow-sheet masses, addition rule for molar masses,
Avogadro 6.0221e23, one rounding at the end). Every number is recomputed by tools/check_bank_ch05.py."""
import json, sys, re, os, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
MS = json.load(open(os.path.join(HERE, 'yellow_sheet_masses.json')))['masses']
NA = D('6.0221e23')
M = '&minus;'
B = []
SYM = ('H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr '
       'Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba').split()
Z = {s: i + 1 for i, s in enumerate(SYM)}

# ---------------- formulas ----------------
def F(s):
    """'Ca(NO3)2' -> Ca(NO<sub>3</sub>)<sub>2</sub>; 'SO4^2-' -> SO<sub>4</sub><sup>2&minus;</sup>; 'CuSO4.5H2O' -> CuSO<sub>4</sub>&middot;5H<sub>2</sub>O."""
    ch = ''
    if '^' in s: s, ch = s.split('^')
    parts = [re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', p) for p in s.split('.')]
    out = '&middot;'.join(parts)
    if ch: out += '<sup>' + ch.replace('-', M) + '</sup>'
    return out
def X(s): return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)

def parse(f):
    """element counts (ordered by first appearance); handles parentheses and hydrate dots ('CuSO4.5H2O')."""
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
def rawsum(f): return sum(D(MS[e]) * n for e, n in parse(f).items())
def mm(f):
    """molar mass, rounded to the fewest decimal places of the atomic masses used."""
    q = min(dp(MS[e]) for e in parse(f))
    return rawsum(f).quantize(D(1).scaleb(-q), rounding=ROUND_HALF_UP)
def G(f): return str(mm(f))
def zsum(f): return sum(Z[e] * n for e, n in parse(f).items())
def terms(f):
    return ' + '.join(('%d(%s)' % (n, MS[e])) if n > 1 else MS[e] for e, n in parse(f).items())
def mmwork(f):
    r = rawsum(f); s = format(r.normalize(), 'f') if r != r.to_integral() else str(r)
    return '%s = %s &rarr; %s g/mol' % (terms(f), s, G(f)) if str(mm(f)) != s else '%s = %s g/mol' % (terms(f), G(f))
def masses(f): return ', '.join('%s %s' % (e, MS[e]) for e in parse(f))

# ---------------- numbers ----------------
def num(x, n):
    """x to n significant figures: plain for 10^-3 .. 10^(n-1) (a trailing '.' when the last kept digit is a 0
    in the ones place), scientific notation otherwise."""
    x = D(x); e = x.adjusted()
    m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if m >= 10:
        e += 1; m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if -3 <= e <= n - 1:
        s = format(m.scaleb(e).quantize(D(1).scaleb(min(0, e - n + 1))), 'f')
        if e == n - 1 and s.endswith('0'): s += '.'
        return s
    return '%s &times; 10<sup>%s</sup>' % (m, (M + str(-e)) if e < 0 else str(e))
AV = '6.0221 &times; 10<sup>23</sup>'

def Q(t, q, c, y, h, w, d, k=0):
    y = ["Correct: " + y[0]] + y[1:]
    it = {"id": "c5-h%02d" % (len(B) + 1), "t": t, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    B.append(it)

# ======================= ch05-mole (10) =======================
T = 'ch05-mole'
x = D('3.7e13') / NA
Q(T, "An adult human body has roughly 3.7 &times; 10<sup>13</sup> cells. How many <b>moles</b> of cells is that?",
  [num(x, 2) + " mol", num(D('3.7e13') * NA, 2) + " mol", num(NA / D('3.7e13'), 2) + " mol", "3.7 &times; 10<sup>13</sup> mol"],
  ["3.7 &times; 10<sup>13</sup> &divide; 6.0221 &times; 10<sup>23</sup> per mol. Even every cell in your body is a tiny fraction of a mole, which is why cells are counted directly.",
   "This multiplies by Avogadro's number. Particles to moles means dividing.",
   "This divides Avogadro's number by the count, which is upside down.",
   "This treats the count of cells as if it were already in moles. A count must be divided by Avogadro's number."],
  "Particles to moles: divide by Avogadro's number. 3.7 has 2 significant figures.",
  "3.7 &times; 10<sup>13</sup> cells &times; (1 mol / 6.0221 &times; 10<sup>23</sup> cells) = <b>" + num(x, 2) + " mol</b> of cells.", 2, 1)

x = D('2.85e-4') * NA
Q(T, "A zinc lozenge contains about 2.85 &times; 10<sup>" + M + "4</sup> mol of zinc. How many zinc atoms is that?",
  [num(x, 3) + " Zn atoms", num(D('2.85e-4') / NA, 3) + " Zn atoms", num(NA / D('2.85e-4'), 3) + " Zn atoms", num(D('2.85e-4') * mm('Zn'), 3) + " g Zn"],
  ["2.85 &times; 10<sup>" + M + "4</sup> mol &times; 6.0221 &times; 10<sup>23</sup> atoms/mol; mol cancels.",
   "This divides by Avogadro's number; moles to particles means multiplying.",
   "This divides Avogadro's number by the moles, which leaves mol in the units.",
   "This multiplies by zinc's molar mass (65.39 g/mol) and gives grams, not atoms."],
  "Moles to particles: multiply by Avogadro's number.",
  "2.85 &times; 10<sup>" + M + "4</sup> mol Zn &times; (6.0221 &times; 10<sup>23</sup> Zn atoms / 1 mol Zn) = <b>" + num(x, 3) + " Zn atoms</b>.", 1, 1)

Q(T, "Magnesium chloride, {MgCl2}, is ionic. Which phrase correctly names what is counted in 1 mol of {MgCl2}?",
  ["6.0221 &times; 10<sup>23</sup> MgCl<sub>2</sub> formula units", "6.0221 &times; 10<sup>23</sup> MgCl<sub>2</sub> molecules",
   "6.0221 &times; 10<sup>23</sup> Mg atoms and Cl<sub>2</sub> molecules", "6.0221 &times; 10<sup>23</sup> ions in total"],
  ["Ionic compounds are counted in formula units: one Mg<sup>2+</sup> and two Cl<sup>" + M + "</sup> per unit.",
   "Ionic compounds do not form molecules.",
   "Magnesium and chlorine are present as ions, not as Mg atoms and Cl<sub>2</sub> molecules.",
   "Each formula unit holds 3 ions, so 1 mol of MgCl<sub>2</sub> contains 3 mol of ions, not 1 mol."],
  "What is the smallest repeating unit of an ionic compound?",
  "1 mol MgCl<sub>2</sub> = 6.0221 &times; 10<sup>23</sup> <b>formula units</b> (which release 3 mol of ions when dissolved).", 1)

x = D('3.25') * NA
Q(T, "Air is mostly nitrogen. How many {N2} molecules are in 3.25 mol of {N2}?",
  [num(x, 3) + " N<sub>2</sub> molecules", num(D('3.25') / NA, 3) + " N<sub>2</sub> molecules", num(NA / D('3.25'), 3) + " N<sub>2</sub> molecules", num(2 * x, 3) + " N<sub>2</sub> molecules"],
  ["3.25 mol &times; 6.0221 &times; 10<sup>23</sup> molecules/mol.",
   "This divides by Avogadro's number. A particle count must be huge.",
   "This divides Avogadro's number by the moles; the units do not cancel.",
   "This doubles the count for the two atoms in N<sub>2</sub>, which would be N <i>atoms</i>. The question asks for molecules."],
  "The particle here is the N<sub>2</sub> molecule.",
  "3.25 mol N<sub>2</sub> &times; 6.0221 &times; 10<sup>23</sup> molecules/mol = <b>" + num(x, 3) + " N<sub>2</sub> molecules</b>.", 2, 1)

x = D('8.43e21') / NA
Q(T, "An air-quality sensor sample contains 8.43 &times; 10<sup>21</sup> molecules of carbon monoxide, CO. How many moles of CO is that?",
  [num(x, 3) + " mol", num(D('8.43e21') * NA, 3) + " mol", num(NA / D('8.43e21'), 3) + " mol", num(x * mm('CO'), 3) + " g"],
  ["8.43 &times; 10<sup>21</sup> &divide; 6.0221 &times; 10<sup>23</sup> per mol.",
   "This multiplies by Avogadro's number. Particles to moles means dividing.",
   "This divides Avogadro's number by the count, which is upside down.",
   "This goes one step further, to grams (&times; 28.010 g/mol). The question asks for moles."],
  "Compare 10<sup>21</sup> with 10<sup>23</sup>: more or less than one mole?",
  "8.43 &times; 10<sup>21</sup> molecules &times; (1 mol / 6.0221 &times; 10<sup>23</sup> molecules) = <b>" + num(x, 3) + " mol</b> CO.", 2, 1)

Q(T, "A student converts 5.8 &times; 10<sup>23</sup> atoms to moles and gets 3.5 &times; 10<sup>47</sup> mol. What went wrong?",
  ["The student multiplied by Avogadro's number instead of dividing.",
   "The student forgot to multiply by the molar mass.",
   "The student used the atomic number instead of Avogadro's number.",
   "Nothing; a large number of atoms gives a large number of moles."],
  ["5.8 &times; 10<sup>23</sup> &times; 6.0221 &times; 10<sup>23</sup> = 3.5 &times; 10<sup>47</sup>. Dividing gives 0.96 mol.",
   "Molar mass is not needed to go from atoms to moles; only Avogadro's number is.",
   "An atomic number would not produce a factor of 10<sup>23</sup>.",
   "Moles in a sample are usually about 0.001 to 10. 10<sup>47</sup> mol would outweigh the Earth many times over."],
  "Use the sanity check: is the number of moles reasonable for a sample?",
  "3.5 &times; 10<sup>47</sup> = 5.8 &times; 10<sup>23</sup> &times; N<sub>A</sub>: <b>the student multiplied instead of dividing</b>. Correct: 5.8 &times; 10<sup>23</sup> &divide; 6.0221 &times; 10<sup>23</sup> = 0.96 mol.", 2)

Q(T, "Which of these samples holds the <b>most atoms in total</b>?",
  ["0.50 mol of {C6H12O6}", "1.5 mol of {CO2}", "1.0 mol of {NH3}", "2.0 mol of He"],
  ["0.50 mol &times; 24 atoms per molecule = 12 mol of atoms, the most here.",
   "1.5 mol &times; 3 atoms = 4.5 mol of atoms.",
   "1.0 mol &times; 4 atoms = 4.0 mol of atoms.",
   "Helium is single atoms: 2.0 mol of atoms."],
  "Multiply the moles of each substance by the atoms in one of its particles.",
  "Moles of atoms: glucose 0.50 &times; 24 = 12; CO<sub>2</sub> 4.5; NH<sub>3</sub> 4.0; He 2.0. <b>0.50 mol of glucose</b> wins, even though it has the fewest moles of molecules.", 3)

x = D('0.660') * NA
Q(T, "How many copper atoms are in 0.660 mol of copper wire?",
  [num(x, 3) + " Cu atoms", num(D('0.660') / NA, 3) + " Cu atoms", num(NA / D('0.660'), 3) + " Cu atoms", num(D('0.660') * mm('Cu'), 3) + " g Cu"],
  ["0.660 mol &times; 6.0221 &times; 10<sup>23</sup> atoms/mol.",
   "This divides by Avogadro's number; moles to particles means multiplying.",
   "This divides Avogadro's number by the moles, which is upside down.",
   "This uses copper's molar mass (63.55 g/mol) and gives grams, not atoms."],
  "Which factor turns moles into atoms?",
  "0.660 mol Cu &times; 6.0221 &times; 10<sup>23</sup> atoms/mol = <b>" + num(x, 3) + " Cu atoms</b>.", 1, 1)

x = D('3.6e22') / NA
Q(T, "A sample of seawater contains 3.6 &times; 10<sup>22</sup> chloride ions. How many moles of {Cl^-} is that?",
  [num(x, 2) + " mol", num(D('3.6e22') * NA, 2) + " mol", num(NA / D('3.6e22'), 2) + " mol", num(x * mm('Cl'), 2) + " g"],
  ["3.6 &times; 10<sup>22</sup> &divide; 6.0221 &times; 10<sup>23</sup> per mol, to 2 significant figures like 3.6.",
   "This multiplies by Avogadro's number. Particles to moles means dividing.",
   "This divides Avogadro's number by the number of ions.",
   "This goes on to grams with 35.45 g/mol. The question asks for moles."],
  "Ions are particles too; divide by Avogadro's number.",
  "3.6 &times; 10<sup>22</sup> ions &divide; 6.0221 &times; 10<sup>23</sup> ions/mol = <b>" + num(x, 2) + " mol</b> Cl<sup>" + M + "</sup>. The trailing zero is significant.", 2, 1)

Q(T, "How do 1 mol of {O2} molecules and 1 mol of O atoms compare?",
  ["The O<sub>2</sub> sample has twice as many O atoms (2 mol) and twice the mass (31.998 g vs 15.999 g).",
   "They are identical, because both are 1 mol of oxygen.",
   "The O atom sample has more atoms, because atoms are smaller than molecules.",
   "They have the same mass but different numbers of atoms."],
  ["Both have 6.0221 &times; 10<sup>23</sup> particles, but each O<sub>2</sub> particle holds 2 atoms.",
   "&ldquo;1 mol of oxygen&rdquo; is ambiguous; always say which particle. The two samples differ.",
   "Both samples have the same number of particles; size does not change the count.",
   "The O<sub>2</sub> sample is heavier: 31.998 g versus 15.999 g."],
  "Same number of particles; how many atoms are in each particle?",
  "<b>1 mol O<sub>2</sub> = 2 mol O atoms = 31.998 g; 1 mol O atoms = 15.999 g.</b> Always name the particle.", 1)

# ======================= ch05-molarmass (10) =======================
T = 'ch05-molarmass'
Q(T, "Ozone, {O3}, is a summer air-quality concern in the San Joaquin Valley. What is the molar mass of ozone? (O 15.999)",
  [G('O3') + " g/mol", G('O') + " g/mol", "%d g/mol" % zsum('O3'), G('O2') + " g/mol"],
  ["3(15.999) = 47.997 g/mol.",
   "This is one O atom. Ozone has three.",
   "This uses oxygen's atomic number (3 &times; 8). Use the atomic mass.",
   "This is the molar mass of ordinary oxygen gas, O<sub>2</sub>. Ozone has three O atoms."],
  "Count the O atoms in one ozone molecule.",
  "{O3}: 3(15.999) = <b>" + G('O3') + " g/mol</b>.", 1, 1)

Q(T, "Dairies in the Valley are a major source of methane, {CH4}. What is the molar mass of methane? (" + masses('CH4') + ")",
  [G('CH4') + " g/mol", G('CH') + " g/mol", "%d g/mol" % zsum('CH4'), G('(CH)4') + " g/mol"],
  ["12.011 + 4(1.008) = 16.043 g/mol.",
   "This counts only one H atom; the subscript is 4.",
   "This adds atomic numbers (6 + 4). Use atomic masses.",
   "This multiplies carbon by 4 as well. The 4 belongs to H only."],
  "The subscript belongs to the atom just before it.",
  "{CH4}: " + mmwork('CH4') + ". So the molar mass is <b>" + G('CH4') + " g/mol</b>.", 1, 1)

Q(T, "Calcium hydroxide, {Ca(OH)2}, is used as a liner under dental fillings. What is its molar mass? (" + masses('Ca(OH)2') + ")",
  [G('Ca(OH)2') + " g/mol", G('CaOH') + " g/mol", G('CaOH2') + " g/mol", format(rawsum('Ca(OH)2'), 'f') + " g/mol"],
  ["40.08 + 2(15.999) + 2(1.008) = 74.094, rounded to 2 decimal places = 74.09 g/mol.",
   "This leaves out the 2 after the parentheses; there are two hydroxide ions.",
   "This applies the 2 only to H. The subscript after the parentheses multiplies O and H.",
   "The sum is right but not rounded; Ca (40.08) has only 2 decimal places."],
  "Multiply everything inside the parentheses by 2, then use the addition rule.",
  "{Ca(OH)2}: " + mmwork('Ca(OH)2') + ". So the molar mass is <b>" + G('Ca(OH)2') + " g/mol</b>.", 2, 1)

Q(T, "Ammonium phosphate, {(NH4)3PO4}, supplies both nitrogen and phosphorus to crops. What is its molar mass? (" + masses('(NH4)3PO4') + ")",
  [G('(NH4)3PO4') + " g/mol", G('NH4PO4') + " g/mol", G('N3H4PO4') + " g/mol", format(rawsum('(NH4)3PO4'), 'f') + " g/mol"],
  ["3 N, 12 H, 1 P, 4 O: 42.021 + 12.096 + 30.97 + 63.996 = 149.083 &rarr; 149.08 g/mol.",
   "This ignores the 3 after the parentheses.",
   "This triples N but not H; there are 3 &times; 4 = 12 H atoms.",
   "The sum is right but must be rounded to 2 decimal places (P has 2)."],
  "How many H atoms are in (NH<sub>4</sub>)<sub>3</sub>?",
  "{(NH4)3PO4}: " + mmwork('(NH4)3PO4') + ". So the molar mass is <b>" + G('(NH4)3PO4') + " g/mol</b>.", 2, 1)

Q(T, "Washing soda is sodium carbonate decahydrate, {Na2CO3.10H2O}. What is its molar mass? (" + masses('Na2CO3.10H2O') + ")",
  [G('Na2CO3.10H2O') + " g/mol", G('Na2CO3') + " g/mol", G('Na2CO3.H2O') + " g/mol", G('(Na2CO3H2O)10') + " g/mol"],
  ["Na<sub>2</sub>CO<sub>3</sub> (105.988) + 10(18.015) = 105.988 + 180.150 = 286.138 &rarr; 286.14 g/mol.",
   "This is the anhydrous salt; the ten waters are part of the hydrate's formula.",
   "This adds only one water instead of ten.",
   "This treats the dot as &ldquo;times&rdquo; and multiplies the whole formula by 10."],
  "The dot means &ldquo;plus&rdquo;: add ten waters.",
  "{Na2CO3.10H2O}: 105.988 + 10(18.015) = 286.138 &rarr; <b>" + G('Na2CO3.10H2O') + " g/mol</b> (2 decimal places, from Na).", 2, 1)

Q(T, "Aluminum hydroxide, {Al(OH)3}, is an antacid ingredient. What is its molar mass? (" + masses('Al(OH)3') + ")",
  [G('Al(OH)3') + " g/mol", G('AlOH3') + " g/mol", G('AlO3H') + " g/mol", format(rawsum('Al(OH)3'), 'f') + " g/mol"],
  ["26.98 + 3(15.999) + 3(1.008) = 78.001 &rarr; 78.00 g/mol (2 decimal places, from Al).",
   "This applies the 3 only to H.",
   "This applies the 3 only to O.",
   "The sum is right but must be rounded to 2 decimal places; the trailing zero in 78.00 is significant."],
  "The 3 after the parentheses multiplies both O and H.",
  "{Al(OH)3}: " + mmwork('Al(OH)3') + ". So the molar mass is <b>" + G('Al(OH)3') + " g/mol</b>.", 2, 1)

Q(T, "Aluminum sulfate octadecahydrate, {Al2(SO4)3.18H2O}, is used to clear drinking water. What is its molar mass? (" + masses('Al2(SO4)3.18H2O') + ")",
  [G('Al2(SO4)3.18H2O') + " g/mol", G('Al2(SO4)3') + " g/mol", G('Al2(SO4)3.H2O') + " g/mol", G('Al2SO4.18H2O') + " g/mol"],
  ["Al<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub> = 342.128; 18(18.015) = 324.270; total 666.398 &rarr; 666.40 g/mol.",
   "This leaves out the 18 waters of hydration.",
   "This adds only one water. The 18 means eighteen waters per formula unit.",
   "This ignores the 3 after (SO<sub>4</sub>), counting one sulfate instead of three."],
  "First the salt (watch the parentheses), then the waters.",
  "2(26.98) + 3(32.06) + 12(15.999) = 342.128; + 18(18.015) = 666.398 &rarr; <b>" + G('Al2(SO4)3.18H2O') + " g/mol</b>.", 3, 1)

Q(T, "What is the <b>formula mass</b> of sucrose (table sugar), {C12H22O11}? (" + masses('C12H22O11') + ")",
  [G('C12H22O11') + " amu", "%d amu" % zsum('C12H22O11'), str(mm('C12H22O11').quantize(D('0.01'), rounding=ROUND_HALF_UP)) + " amu", G('C12H22O11') + " g"],
  ["12(12.011) + 22(1.008) + 11(15.999) = 144.132 + 22.176 + 175.989 = 342.297 amu.",
   "This adds atomic numbers. Use the atomic masses.",
   "This rounds to 2 decimal places, but every mass used has 3.",
   "342.297 g is the mass of a whole mole. One molecule's formula mass is in amu."],
  "Formula mass is for one molecule, in amu.",
  "{C12H22O11}: " + terms('C12H22O11') + " = <b>" + G('C12H22O11') + " amu</b> per molecule (342.297 g per mole).", 2, 1)

x = mm('NaCl') / NA
Q(T, "The molar mass of {NaCl} is 58.44 g/mol. What is the mass of <b>one</b> NaCl formula unit, in amu?",
  ["58.44 amu", "58.44 g", num(x, 4) + " amu", num(mm('NaCl') * NA, 4) + " amu"],
  ["The formula mass in amu is the same number as the molar mass in g/mol.",
   "58.44 g is the mass of one mole of formula units, not one.",
   "This is the mass of one formula unit in <i>grams</i> (58.44 g &divide; N<sub>A</sub>), labeled amu.",
   "This multiplies by Avogadro's number, which makes no sense for a single formula unit."],
  "One particle in amu, one mole in grams: same number.",
  "One formula unit: <b>58.44 amu</b> (= 9.704 &times; 10<sup>" + M + "23</sup> g). One mole: 58.44 g.", 1)

Q(T, "Styptic pencils, used to stop bleeding from small nicks, contain potassium alum, {KAl(SO4)2.12H2O}. What is its molar mass? (" + masses('KAl(SO4)2.12H2O') + ")",
  [G('KAl(SO4)2.12H2O') + " g/mol", G('KAlSO4.12H2O') + " g/mol", G('KAl(SO4)2') + " g/mol", G('KAl(SO4)2.H2O') + " g/mol"],
  ["KAl(SO<sub>4</sub>)<sub>2</sub> = 39.10 + 26.98 + 2(32.06) + 8(15.999) = 258.192; + 12(18.015) = 216.180; total 474.372 &rarr; 474.37 g/mol.",
   "This leaves out the 2 after (SO<sub>4</sub>), counting one sulfate instead of two.",
   "This leaves out the twelve waters of hydration.",
   "This adds only one water instead of twelve."],
  "Salt part first (two sulfates), then add twelve waters.",
  "258.192 + 12(18.015) = 474.372 &rarr; <b>" + G('KAl(SO4)2.12H2O') + " g/mol</b> (2 decimal places, from K, Al and S).", 3, 1)

# ======================= ch05-convert (10) =======================
T = 'ch05-convert'
x = D('99') * 10 / mm('C6H12O6')
Q(T, "A fasting glucose of 99 mg/dL is just inside the normal range. Glucose, {C6H12O6}, is 180.156 g/mol. What is this value in mmol/L?",
  [num(x, 2) + " mmol/L", num(D('99') / mm('C6H12O6'), 2) + " mmol/L", num(x / 1000, 2) + " mmol/L", num(D('99') * 10 * mm('C6H12O6'), 2) + " mmol/L"],
  ["99 mg/dL &times; 10 dL/L &divide; 180.156 mg/mmol, to 2 significant figures like 99.",
   "This skips the dL &rarr; L step (10 dL = 1 L).",
   "This is the value in mol/L labeled mmol/L. With mg and mg/mmol you get mmol directly.",
   "This multiplies by the molar mass instead of dividing."],
  "dL &rarr; L first; g/mol = mg/mmol.",
  "99 mg/dL &times; 10 dL/L = 990 mg/L; &divide; 180.156 mg/mmol = <b>" + num(x, 2) + " mmol/L</b>. (Context only; use the facility's units.)", 2, 1)

x = D('500') / mm('C4H11N5.HCl')
Q(T, "A metformin tablet contains 500. mg of metformin hydrochloride, {C4H11N5.HCl} (165.63 g/mol). How many millimoles is that?",
  [num(x, 3) + " mmol", num(x / 1000, 3) + " mmol", num(D('500') * mm('C4H11N5.HCl'), 3) + " mmol", num(D('500') / mm('C4H11N5'), 3) + " mmol"],
  ["500. mg &divide; 165.63 mg/mmol (3 significant figures, from 500. with its decimal point).",
   "This is the answer in moles labeled mmol.",
   "This multiplies by the molar mass instead of dividing.",
   "This uses the molar mass of metformin without the HCl (129.167 g/mol). The label mass is for the hydrochloride salt."],
  "Use the molar mass of the compound named on the label.",
  "500. mg &times; (1 mmol / 165.63 mg) = <b>" + num(x, 3) + " mmol</b>. (Context only; not dosing guidance.)", 2, 1)

x = D('0.0850') * mm('NaHCO3')
Q(T, "Sodium bicarbonate, {NaHCO3} (84.01 g/mol), is baking soda and an antacid. What is the mass of 0.0850 mol of it?",
  [num(x, 3) + " g", num(D('0.0850') / mm('NaHCO3'), 3) + " g", num(mm('NaHCO3') / D('0.0850'), 3) + " g", num(D('0.0850') * zsum('NaHCO3'), 3) + " g"],
  ["0.0850 mol &times; 84.01 g/mol.",
   "This divides by the molar mass; moles to grams means multiplying.",
   "This divides the molar mass by the moles; the units do not cancel.",
   "This uses 42, the sum of the atomic numbers, as the molar mass."],
  "mol &times; (g/mol) = g.",
  "0.0850 mol &times; (84.01 g / 1 mol) = <b>" + num(x, 3) + " g</b> NaHCO<sub>3</sub>.", 1, 1)

x = mm('C6H12O6') / NA
Q(T, "What is the mass, in grams, of a single glucose molecule, {C6H12O6} (180.156 g/mol)?",
  [num(x, 5) + " g", num(mm('C6H12O6') * NA, 5) + " g", num(NA / mm('C6H12O6'), 5) + " g", G('C6H12O6') + " g"],
  ["180.156 g per 6.0221 &times; 10<sup>23</sup> molecules, to 5 significant figures (6.0221 has 5).",
   "This multiplies by Avogadro's number; one molecule must be far lighter than a mole.",
   "This is molecules per gram, the ratio upside down.",
   "This is the mass of one mole, not one molecule."],
  "Mass of one mole &divide; molecules in one mole.",
  "180.156 g &divide; 6.0221 &times; 10<sup>23</sup> = <b>" + num(x, 5) + " g</b> per molecule (180.156 amu).", 2, 1)

mol = D('1.00e20') / NA; g = mol * mm('C8H10N4O2')
Q(T, "What mass of caffeine, {C8H10N4O2} (194.194 g/mol), contains 1.00 &times; 10<sup>20</sup> molecules? Give the answer in milligrams.",
  [num(g * 1000, 3) + " mg", num(g, 3) + " mg", num(mol, 3) + " mol", num(mol / mm('C8H10N4O2') * 1000, 3) + " mg"],
  ["1.00 &times; 10<sup>20</sup> &divide; N<sub>A</sub> = 1.661 &times; 10<sup>" + M + "4</sup> mol; &times; 194.194 g/mol = 0.03225 g = 32.2 mg.",
   "This is the mass in grams labeled mg. Multiply by 1000 to get mg.",
   "This stops at moles.",
   "This divides by the molar mass in the second step."],
  "Molecules &rarr; moles &rarr; grams &rarr; milligrams.",
  "1.00 &times; 10<sup>20</sup> &divide; 6.0221 &times; 10<sup>23</sup> = 1.661 &times; 10<sup>" + M + "4</sup> mol; &times; 194.194 g/mol = 0.0322 g = <b>" + num(g * 1000, 3) + " mg</b>.", 3, 1)

x = D('4.65') / mm('Ca')
Q(T, "A 50.0 mL plasma sample contains 4.65 mg of calcium ions. How many millimoles of {Ca^2+} is that? (Ca 40.08)",
  [num(x, 3) + " mmol", num(x * 1000, 3) + " mmol", num(D('4.65') * mm('Ca'), 3) + " mmol", num(2 * x, 3) + " mmol"],
  ["4.65 mg &divide; 40.08 mg/mmol (losing two electrons does not change the mass noticeably).",
   "This treats 4.65 mg as 4.65 g, then converts mol to mmol, so it is 1000 times too large.",
   "This multiplies by the molar mass instead of dividing.",
   "This doubles for the 2+ charge, which gives milliequivalents (mEq), not millimoles."],
  "mg &divide; (mg/mmol) = mmol. The charge does not change the count.",
  "4.65 mg &times; (1 mmol / 40.08 mg) = <b>" + num(x, 3) + " mmol</b> Ca<sup>2+</sup>. (Context only.)", 2, 1)

mol = D('2.50') / mm('O2'); n = mol * NA
Q(T, "A respiratory therapist's oxygen calculation involves 2.50 g of {O2} gas (31.998 g/mol). How many {O2} molecules is that?",
  [num(n, 3) + " O<sub>2</sub> molecules", num(D('2.50') / mm('O') * NA, 3) + " O<sub>2</sub> molecules", num(mol, 3) + " mol", num(D('2.50') * NA, 3) + " O<sub>2</sub> molecules"],
  ["2.50 g &divide; 31.998 g/mol = 0.07813 mol O<sub>2</sub>; &times; 6.0221 &times; 10<sup>23</sup>.",
   "This uses 15.999 g/mol (O atoms) for O<sub>2</sub> molecules, which doubles the count.",
   "This stops at moles.",
   "This skips the molar mass; grams must become moles first."],
  "The gas is O<sub>2</sub> molecules: use 31.998 g/mol.",
  "2.50 g &times; (1 mol / 31.998 g) &times; 6.0221 &times; 10<sup>23</sup> = <b>" + num(n, 3) + " O<sub>2</sub> molecules</b>.", 2, 1)

x = D('4.2') * mm('K') / 10
Q(T, "A serum potassium is 4.2 mmol/L. What is this value in mg/dL? (K 39.10)",
  [num(x, 2) + " mg/dL", num(x * 10, 2) + " mg/dL", num(D('4.2') / mm('K') / 10, 2) + " mg/dL", num(x / 1000, 2) + " mg/dL"],
  ["4.2 mmol/L &times; 39.10 mg/mmol = 164 mg/L; &divide; 10 dL/L, to 2 significant figures like 4.2.",
   "This stops at mg per <i>liter</i>. One liter is 10 dL, so divide by 10.",
   "This divides by the molar mass instead of multiplying.",
   "This is the mass in grams per dL labeled mg/dL."],
  "mmol &rarr; mg with the molar mass, then L &rarr; dL.",
  "4.2 mmol/L &times; 39.10 mg/mmol &times; (1 L / 10 dL) = <b>" + num(x, 2) + " mg/dL</b>. (Context only; labs report potassium in mmol/L.)", 3, 1)

x = D('45.0') / mm('H2O')
Q(T, "How many moles of water are in 45.0 g of water?",
  [num(x, 3) + " mol", num(D('45.0') * mm('H2O'), 3) + " mol", num(mm('H2O') / D('45.0'), 3) + " mol", num(D('45.0') / zsum('H2O'), 3) + " mol"],
  ["45.0 g &divide; 18.015 g/mol.",
   "This multiplies by the molar mass; grams to moles means dividing.",
   "This divides the molar mass by the mass; the units do not cancel.",
   "This uses 10, the sum of the atomic numbers (1 + 1 + 8), as the molar mass."],
  "Water's molar mass is 2(1.008) + 15.999.",
  "45.0 g &times; (1 mol / 18.015 g) = <b>" + num(x, 3) + " mol</b> H<sub>2</sub>O.", 1, 1)

mol = D('1.00') / 1000 / mm('C3H5N3O9'); n = mol * NA
Q(T, "Nitroglycerin, {C3H5N3O9} (227.085 g/mol), is used to relieve chest pain. How many molecules are in 1.00 mg of it?",
  [num(n, 3) + " molecules", num(D('1.00') / mm('C3H5N3O9') * NA, 3) + " molecules", num(mol, 3) + " mol", num(D('1.00') / 1000 * mm('C3H5N3O9') * NA, 3) + " molecules"],
  ["1.00 mg = 1.00 &times; 10<sup>" + M + "3</sup> g; &divide; 227.085 g/mol = 4.404 &times; 10<sup>" + M + "6</sup> mol; &times; N<sub>A</sub>.",
   "This skips mg &rarr; g, so it is 1000 times too large.",
   "This stops at moles.",
   "This multiplies by the molar mass instead of dividing."],
  "mg &rarr; g &rarr; mol &rarr; molecules.",
  "1.00 &times; 10<sup>" + M + "3</sup> g &times; (1 mol / 227.085 g) &times; 6.0221 &times; 10<sup>23</sup> = <b>" + num(n, 3) + " molecules</b>. (Context only.)", 3, 1)

# ======================= ch05-formula (10) =======================
T = 'ch05-formula'
x = D('0.250') * 8
Q(T, "How many moles of oxygen atoms are in 0.250 mol of magnesium phosphate, {Mg3(PO4)2}?",
  [num(x, 3) + " mol O", num(D('0.250') * 4, 3) + " mol O", num(D('0.250') / 8, 3) + " mol O", num(D('0.250') * 6, 3) + " mol O"],
  ["2 &times; 4 = 8 O per formula unit: 0.250 &times; 8.",
   "This uses only the 4 inside the parentheses.",
   "This divides by 8, the ratio upside down.",
   "This adds the subscripts (4 + 2) instead of multiplying."],
  "Multiply the subscript inside the parentheses by the one outside.",
  "0.250 mol &times; (8 mol O / 1 mol {Mg3(PO4)2}) = <b>" + num(x, 3) + " mol O</b>.", 2, 1)

x = D('0.0750') * 2 * NA
Q(T, "How many nitrogen atoms are in 0.0750 mol of ammonium nitrate, {NH4NO3}?",
  [num(x, 3) + " N atoms", num(D('0.0750') * NA, 3) + " N atoms", num(D('0.0750') * 2, 3) + " mol N", num(D('0.0750') / 2 * NA, 3) + " N atoms"],
  ["NH<sub>4</sub>NO<sub>3</sub> has 2 N (one in NH<sub>4</sub><sup>+</sup>, one in NO<sub>3</sub><sup>" + M + "</sup>): 0.150 mol N &times; N<sub>A</sub>.",
   "This counts only one N per formula unit. Look in both ions.",
   "This stops at moles of N.",
   "This divides by 2, the ratio upside down."],
  "Find N in both the cation and the anion.",
  "0.0750 &times; 2 = 0.150 mol N; &times; 6.0221 &times; 10<sup>23</sup> = <b>" + num(x, 3) + " N atoms</b>.", 2, 1)

x = D('2.50') * 2 * mm('N') / mm('NH4NO3')
Q(T, "Ammonium nitrate, {NH4NO3} (80.043 g/mol), is a nitrogen fertilizer. How many kilograms of nitrogen are in 2.50 kg of it? (N 14.007)",
  [num(x, 3) + " kg N", num(D('2.50') * mm('N') / mm('NH4NO3'), 3) + " kg N", num(D('2.50') * mm('NH4NO3') / (2 * mm('N')), 3) + " kg N", num(D('2.50') * 2 * mm('N2') / mm('NH4NO3'), 3) + " kg N"],
  ["The ratio works in kg and kmol as well as g and mol: 2.50 &times; (2 &times; 14.007) &divide; 80.043.",
   "This counts only one N per formula unit.",
   "This flips the ratio; the nitrogen cannot weigh more than the fertilizer.",
   "This uses 28.014 (N<sub>2</sub>) for each N atom."],
  "mass compound &rarr; moles compound &rarr; moles N (2 per unit) &rarr; mass N.",
  "2.50 kg &times; (1 kmol / 80.043 kg) &times; (2 kmol N / 1 kmol) &times; (14.007 kg / 1 kmol N) = <b>" + num(x, 3) + " kg N</b> (35.0% N).", 3, 1)

x = D('1.50') * 3 * mm('Ca') / mm('Ca3(C6H5O7)2')
Q(T, "A calcium citrate supplement contains 1.50 g of {Ca3(C6H5O7)2} (498.44 g/mol). What mass of calcium does it contain? (Ca 40.08)",
  [num(x, 3) + " g Ca", num(D('1.50') * mm('Ca') / mm('Ca3(C6H5O7)2'), 3) + " g Ca", num(D('1.50') * mm('Ca3(C6H5O7)2') / (3 * mm('Ca')), 3) + " g Ca", num(D('1.50') / mm('Ca3(C6H5O7)2'), 3) + " mol Ca"],
  ["1.50 g &divide; 498.44 g/mol = 0.003009 mol; &times; 3 mol Ca/mol = 0.009028 mol Ca; &times; 40.08 g/mol.",
   "This skips the subscript 3; each formula unit has three Ca.",
   "This flips the ratio; the calcium cannot weigh more than the compound.",
   "This stops at moles of the compound, labeled mol Ca, and skips the subscript and molar-mass steps."],
  "g compound &rarr; mol compound &rarr; mol Ca (&times; 3) &rarr; g Ca.",
  "1.50 g &times; (1 mol / 498.44 g) &times; (3 mol Ca / 1 mol) &times; (40.08 g / 1 mol Ca) = <b>" + num(x, 3) + " g Ca</b>. (Context only.)", 3, 1)

x = D('0.0200') * 4
Q(T, "Sodium phosphate, {Na3PO4}, dissolves into {Na^+} and {PO4^3-} ions. How many moles of ions in total come from 0.0200 mol of {Na3PO4}?",
  [num(x, 3) + " mol ions", num(D('0.0200') * 3, 3) + " mol ions", num(D('0.0200'), 3) + " mol ions", num(D('0.0200') * 8, 3) + " mol ions"],
  ["3 Na<sup>+</sup> + 1 PO<sub>4</sub><sup>3" + M + "</sup> = 4 ions per formula unit.",
   "This counts only the sodium ions.",
   "This counts formula units, not ions.",
   "This splits phosphate into 1 P and 4 O. A polyatomic ion stays together as one particle."],
  "A polyatomic ion is one particle.",
  "0.0200 mol &times; 4 mol ions / 1 mol = <b>" + num(x, 3) + " mol ions</b>.", 2, 1)

mol = D('1.49') / mm('KCl'); x = mol * NA
Q(T, "How many potassium ions are in 1.49 g of potassium chloride, {KCl} (74.55 g/mol)?",
  [num(x, 3) + " K<sup>+</sup> ions", num(2 * x, 3) + " K<sup>+</sup> ions", num(D('1.49') / mm('K') * NA, 3) + " K<sup>+</sup> ions", num(mol, 3) + " mol K<sup>+</sup>"],
  ["1.49 g &divide; 74.55 g/mol = 0.01999 mol KCl = 0.01999 mol K<sup>+</sup>; &times; N<sub>A</sub>.",
   "This counts both K<sup>+</sup> and Cl<sup>" + M + "</sup>.",
   "This divides by the molar mass of K (39.10) instead of KCl.",
   "This stops at moles."],
  "g KCl &rarr; mol KCl &rarr; mol K<sup>+</sup> &rarr; ions.",
  "1.49 g &times; (1 mol / 74.55 g) &times; 6.0221 &times; 10<sup>23</sup> = <b>" + num(x, 3) + " K<sup>+</sup> ions</b>.", 2, 1)

x = D('0.100') * mm('KI') / mm('I')
Q(T, "What mass of potassium iodide, {KI} (166.00 g/mol), contains 0.100 g of iodine? (I 126.90)",
  [num(x, 3) + " g KI", num(D('0.100') * mm('I') / mm('KI'), 3) + " g KI", num(D('0.100') / mm('I'), 3) + " mol", "0.100 g KI"],
  ["0.100 g I &divide; 126.90 g/mol = 7.880 &times; 10<sup>" + M + "4</sup> mol I = mol KI; &times; 166.00 g/mol.",
   "This uses the ratio upside down; the compound must weigh more than the iodine in it.",
   "This stops at moles of iodine.",
   "This treats KI as if it were all iodine."],
  "g I &rarr; mol I &rarr; mol KI &rarr; g KI.",
  "0.100 g I &times; (1 mol I / 126.90 g) &times; (1 mol KI / 1 mol I) &times; (166.00 g / 1 mol KI) = <b>" + num(x, 3) + " g KI</b>. (Potassium iodide tablets for radiation emergencies are about 130 mg for about 100 mg of iodide; context only.)", 3, 1)

x = D('0.600') * mm('O')
Q(T, "What mass of oxygen is in 0.600 mol of water, {H2O}? (O 15.999, H 1.008)",
  [num(x, 3) + " g O", num(D('0.600') * mm('O2'), 3) + " g O", num(D('0.600') * mm('H2O'), 3) + " g O", num(D('0.600') / mm('O'), 3) + " g O"],
  ["0.600 mol H<sub>2</sub>O &times; 1 mol O / 1 mol &times; 15.999 g/mol.",
   "This uses 31.998 (O<sub>2</sub>) for O atoms.",
   "This is the mass of the whole water sample.",
   "This divides by the molar mass of O instead of multiplying."],
  "One O atom per molecule; O atoms weigh 15.999 g/mol.",
  "0.600 mol &times; (1 mol O / 1 mol H<sub>2</sub>O) &times; 15.999 g/mol = <b>" + num(x, 3) + " g O</b>.", 2, 1)

x = D('5.00') / mm('C2H5OH') * 6 * NA
Q(T, "How many hydrogen atoms are in 5.00 g of ethanol, {C2H5OH} (46.069 g/mol)?",
  [num(x, 3) + " H atoms", num(D('5.00') / mm('C2H5OH') * NA, 3) + " H atoms", num(D('5.00') / mm('C2H5OH') * 6, 3) + " mol H", num(D('5.00') / mm('C2H5OH') * 5 * NA, 3) + " H atoms"],
  ["5.00 g &divide; 46.069 = 0.1085 mol; &times; 6 mol H/mol = 0.6512 mol H; &times; N<sub>A</sub>.",
   "This counts molecules, not H atoms.",
   "This stops at moles of H.",
   "This misses the H in the OH group; ethanol has 5 + 1 = 6 H."],
  "Count every H in C<sub>2</sub>H<sub>5</sub>OH.",
  "5.00 g &times; (1 mol / 46.069 g) &times; (6 mol H / 1 mol) &times; 6.0221 &times; 10<sup>23</sup> = <b>" + num(x, 3) + " H atoms</b>.", 3, 1)

Q(T, "When 1 mol of potassium sulfate, {K2SO4}, dissolves, how many moles of {K^+} and how many moles of ions in total are released?",
  ["2 mol K<sup>+</sup>; 3 mol of ions in total", "2 mol K<sup>+</sup>; 7 mol of ions in total",
   "1 mol K<sup>+</sup>; 2 mol of ions in total", "2 mol K<sup>+</sup>; 2 mol of ions in total"],
  ["Each formula unit is two K<sup>+</sup> and one SO<sub>4</sub><sup>2" + M + "</sup>: three ions.",
   "This splits sulfate into 1 S and 4 O. A polyatomic ion stays together as one particle.",
   "This ignores the subscript 2 on K.",
   "This forgets to count the sulfate ion."],
  "Use the subscript on K, and treat sulfate as one particle.",
  "{K2SO4} &rarr; 2 {K^+} + {SO4^2-}: <b>2 mol K<sup>+</sup>, 3 mol of ions</b>.", 1)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
