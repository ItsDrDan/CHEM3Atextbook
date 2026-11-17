#!/usr/bin/env python3
"""Builds bank/ch05.json (Chapter 5 Try It items: the mole, molar mass, mass-mole-particle conversions,
moles within a formula). Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch05.py bank/ch05.json
Atomic masses: tools/yellow_sheet_masses.json (strings, printed decimals). Molar mass = sum of the atomic masses
(subscripts exact), rounded once to the fewest decimal places of the masses used. Avogadro's number 6.0221e23.
Answers: multiplication/division sig figs from the givens (course rule: trailing zeros without a decimal point are
not significant), rounded once at the end. Formulas are typed in braces, {Ca(NO3)2}, {CuSO4.5H2O}, {Mg^2+}.
Every number is recomputed independently by tools/check_bank_ch05.py."""
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

def Q(t, q, c, y, h, w, d, k=0, f=None):
    it = {"id": "c5-%03d" % (len(B) + 1), "t": t, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    if f:
        for fg in f:
            if fg['type'] == 'table':
                fg['head'] = [X(x) for x in fg['head']]; fg['rows'] = [[X(x) for x in r] for r in fg['rows']]
        it["f"] = f
    B.append(it)

# ======================= ch05-mole (12) =======================
T = 'ch05-mole'
Q(T, "Which statement best describes a <b>mole</b>?",
  ["A counting unit: 6.0221 &times; 10<sup>23</sup> particles of anything",
   "The mass of 1 g of any substance",
   "The number of atoms in 1 g of any element",
   "The mass of one carbon-12 atom"],
  ["Like a dozen (12), a mole is a number: 1 mol = 6.0221 &times; 10<sup>23</sup> atoms, molecules, formula units, or ions.",
   "A mole is a number of particles, not a mass. One mole of different substances has different masses.",
   "One gram of hydrogen and one gram of gold hold very different numbers of atoms, because their atoms have different masses. A mole is a fixed number.",
   "That mass is exactly 12 amu, a tiny mass. A mole is the number of carbon-12 atoms in 12 g, not the mass of one atom."],
  "Think of a dozen. Is a dozen a mass or a count?",
  "A <b>mole</b> is a counting unit: 1 mol = 6.0221 &times; 10<sup>23</sup> particles (Avogadro's number, N<sub>A</sub>). Its mass depends on what is being counted.", 1)

Q(T, "You have 1.00 mol of copper atoms and 1.00 mol of sucrose molecules. Which statement is true?",
  ["They contain the same number of particles, but the sucrose has more mass.",
   "They have the same mass, because both are 1.00 mol.",
   "The copper contains more particles, because copper atoms are smaller.",
   "The sucrose contains more particles, because each molecule is bigger."],
  ["A mole is a number, so both hold 6.0221 &times; 10<sup>23</sup> particles. A sucrose molecule (342.297 amu) is much heavier than a copper atom (63.55 amu), so the sucrose sample weighs more.",
   "Equal moles mean equal numbers of particles, not equal masses. Heavier particles make a heavier mole.",
   "The size of the particle does not change the count. 1.00 mol is always 6.0221 &times; 10<sup>23</sup> particles.",
   "Bigger particles make a mole heavier, not larger in number."],
  "A dozen eggs and a dozen bowling balls: same count or same mass?",
  "Both samples contain <b>the same number of particles</b> (6.0221 &times; 10<sup>23</sup>). 1.00 mol of sucrose has a mass of 342.297 g; 1.00 mol of copper, 63.55 g.", 1)

Q(T, "Sodium chloride, {NaCl}, is an ionic compound. When you count out 1 mol of {NaCl}, what particles are you counting?",
  ["6.0221 &times; 10<sup>23</sup> NaCl formula units",
   "6.0221 &times; 10<sup>23</sup> NaCl molecules",
   "6.0221 &times; 10<sup>23</sup> Cl<sub>2</sub> molecules",
   "6.0221 &times; 10<sup>23</sup> grams of NaCl"],
  ["Ionic compounds are made of ions in a repeating pattern, so the smallest unit is a formula unit (one Na<sup>+</sup> and one Cl<sup>" + M + "</sup>).",
   "Ionic compounds have no molecules; molecules are for compounds of nonmetals joined by covalent bonds.",
   "Chlorine in NaCl is present as chloride ions, not as Cl<sub>2</sub> molecules.",
   "Avogadro's number counts particles, not grams. One mole of NaCl has a mass of 58.44 g."],
  "What do we call the smallest repeating unit of an ionic compound (Section 4.1)?",
  "1 mol NaCl = 6.0221 &times; 10<sup>23</sup> <b>formula units</b>, each made of one Na<sup>+</sup> ion and one Cl<sup>" + M + "</sup> ion.", 1)

Q(T, "Which phrase names the counted particles <b>correctly</b>?",
  ["1 mol of {CO2} molecules", "1 mol of {NaCl} molecules", "1 mol of Fe molecules", "1 mol of {Mg^2+} formula units"],
  ["CO<sub>2</sub> is a molecular compound (two nonmetals), so its particles are molecules.",
   "NaCl is ionic (a metal and a nonmetal), so it is counted in formula units, not molecules.",
   "Iron is a metal element; its particles are Fe atoms.",
   "Mg<sup>2+</sup> is a single ion, so it is counted as ions. Formula units are for whole ionic compounds."],
  "Match each kind of substance with its particle: element, molecular compound, ionic compound, ion.",
  "Metal elements: atoms. Molecular compounds: molecules. Ionic compounds: formula units. Ions: ions. Only <b>1 mol of CO<sub>2</sub> molecules</b> names the particle correctly.", 2)

n = D('2.50') * NA
Q(T, "How many aluminum atoms are in 2.50 mol of aluminum?",
  [num(n, 3) + " Al atoms", num(D('2.50') / NA, 3) + " Al atoms", num(NA / D('2.50'), 3) + " Al atoms", num(D('2.50') * mm('Al'), 3) + " Al atoms"],
  ["2.50 mol &times; (6.0221 &times; 10<sup>23</sup> atoms / 1 mol): mol cancels, leaving atoms. More than 2 mol should be more than 10<sup>24</sup> atoms.",
   "This divides by Avogadro's number, the factor upside down. A particle count should be huge, not tiny.",
   "This divides Avogadro's number by the moles. Set up the factor so that mol cancels.",
   "This multiplies by the molar mass of aluminum (26.98 g/mol), which gives grams, not atoms."],
  "Moles to particles: which factor puts mol on the bottom?",
  "2.50 mol Al &times; (6.0221 &times; 10<sup>23</sup> Al atoms / 1 mol Al) = <b>" + num(n, 3) + " Al atoms</b> (3 significant figures, like 2.50).", 1, 1)

x = D('4.65e22') / NA
Q(T, "A silver ring contains 4.65 &times; 10<sup>22</sup> silver atoms. How many moles of silver is that?",
  [num(x, 3) + " mol Ag", num(D('4.65e22') * NA, 3) + " mol Ag", num(NA / D('4.65e22'), 3) + " mol Ag", num(x * mm('Ag'), 3) + " g Ag"],
  ["4.65 &times; 10<sup>22</sup> atoms &times; (1 mol / 6.0221 &times; 10<sup>23</sup> atoms). Fewer atoms than Avogadro's number gives less than 1 mol.",
   "This multiplies by Avogadro's number, the factor upside down. A sample this size cannot hold 10<sup>46</sup> mol.",
   "This divides Avogadro's number by the number of atoms, which is upside down: atoms would be left in the denominator.",
   "This goes one step too far: it multiplies the moles by silver's molar mass (107.87 g/mol) and gives grams."],
  "Particles to moles: divide by Avogadro's number.",
  "4.65 &times; 10<sup>22</sup> atoms &divide; 6.0221 &times; 10<sup>23</sup> atoms/mol = <b>" + num(x, 3) + " mol Ag</b>, a bit less than a tenth of a mole.", 2, 1)

n = D('0.0196') * NA
Q(T, "A single breath at rest (about half a liter of air) holds about 0.0196 mol of gas molecules. How many molecules is that?",
  [num(n, 3) + " molecules", num(D('0.0196') / NA, 3) + " molecules", num(NA / D('0.0196'), 3) + " molecules", num(D('0.0196') * D('6.0221'), 3) + " molecules"],
  ["0.0196 mol &times; 6.0221 &times; 10<sup>23</sup> molecules/mol. Even a small fraction of a mole is an enormous number of molecules.",
   "This divides by Avogadro's number; moles to particles means multiplying.",
   "This divides Avogadro's number by the moles, which leaves mol in the units instead of canceling it.",
   "The &times;10<sup>23</sup> part of Avogadro's number was left out on the calculator. Enter it as 6.0221E23."],
  "Is the answer a huge number or a small one?",
  "0.0196 mol &times; 6.0221 &times; 10<sup>23</sup> molecules/mol = <b>" + num(n, 3) + " molecules</b>. Respiratory therapists work with volumes, but every breath is a count of molecules.", 2, 1)

Q(T, "Which sample contains the <b>greatest number of atoms</b>?",
  ["1.0 mol of {CH4}", "1.0 mol of {H2O}", "1.0 mol of {O2}", "1.0 mol of He"],
  ["Each CH<sub>4</sub> molecule has 5 atoms (1 C + 4 H), so 1.0 mol of CH<sub>4</sub> holds 5.0 mol of atoms.",
   "Each H<sub>2</sub>O molecule has 3 atoms, so this is 3.0 mol of atoms. Another sample has more atoms per molecule.",
   "Each O<sub>2</sub> molecule has 2 atoms, so this is 2.0 mol of atoms.",
   "Helium exists as single atoms, so this is only 1.0 mol of atoms."],
  "All four samples have the same number of particles. Which particle is made of the most atoms?",
  "Same number of molecules (1.0 mol each), so count atoms per particle: CH<sub>4</sub> 5, H<sub>2</sub>O 3, O<sub>2</sub> 2, He 1. <b>1.0 mol of CH<sub>4</sub></b> has the most atoms, 5.0 mol.", 2)

Q(T, "A student calculates that 0.50 mol of water contains 8.3 &times; 10<sup>" + M + "25</sup> molecules. What went wrong?",
  ["The student divided by Avogadro's number instead of multiplying.",
   "The student used the molar mass of water instead of Avogadro's number.",
   "The student should have counted atoms, which would be 3 times larger.",
   "Nothing; half a mole is a very small amount, so the number should be tiny."],
  ["0.50 &divide; 6.0221 &times; 10<sup>23</sup> = 8.3 &times; 10<sup>" + M + "25</sup>. The setup should be 0.50 mol &times; 6.0221 &times; 10<sup>23</sup> molecules/mol = 3.0 &times; 10<sup>23</sup> molecules.",
   "0.50 mol &times; 18.015 g/mol = 9.0 g, not 10<sup>" + M + "25</sup>. That is not where this number comes from.",
   "Counting atoms would change the number by a factor of 3, not by a factor of about 10<sup>48</sup>.",
   "Half a mole is a small amount of water (about 9 g), but it still holds an enormous number of molecules. No sample can hold less than one molecule."],
  "Use the sanity check: should a particle count be a huge number or a tiny one?",
  "8.3 &times; 10<sup>" + M + "25</sup> is less than one molecule, which is impossible. It is 0.50 &divide; N<sub>A</sub>: <b>the student divided instead of multiplying</b>. The correct count is 3.0 &times; 10<sup>23</sup> molecules.", 2)

x = D('1.20e24') / NA
Q(T, "A glass holds 1.20 &times; 10<sup>24</sup> water molecules. How many moles of water is that?",
  [num(x, 3) + " mol", num(D('1.20e24') * NA, 3) + " mol", num(NA / D('1.20e24'), 3) + " mol", num(x * mm('H2O'), 3) + " g"],
  ["1.20 &times; 10<sup>24</sup> &divide; 6.0221 &times; 10<sup>23</sup> per mol: about twice Avogadro's number, so about 2 mol.",
   "This multiplies by Avogadro's number. Particles to moles means dividing.",
   "This divides Avogadro's number by the count, which is upside down.",
   "This goes on to grams by multiplying by 18.015 g/mol. The question asks for moles."],
  "Compare the number of molecules with Avogadro's number before you calculate.",
  "1.20 &times; 10<sup>24</sup> molecules &times; (1 mol / 6.0221 &times; 10<sup>23</sup> molecules) = <b>" + num(x, 3) + " mol</b> of water.", 2, 1)

Q(T, "What is Avogadro's number, as printed on the CHEM 3A yellow sheet?",
  ["6.0221 &times; 10<sup>23</sup> particles per mole", "6.0221 &times; 10<sup>" + M + "23</sup> particles per mole",
   "12.011 particles per mole", "1.6605 &times; 10<sup>" + M + "24</sup> particles per mole"],
  ["N<sub>A</sub> = 6.0221 &times; 10<sup>23</sup> mol<sup>" + M + "1</sup>: the number of particles in one mole.",
   "The exponent is positive. A mole is a huge number of particles, not a tiny fraction of one.",
   "12.011 is the molar mass of carbon in g/mol, not a count of particles.",
   "1.6605 &times; 10<sup>" + M + "24</sup> is the mass of 1 amu in grams, not a number of particles."],
  "A mole is a very large count.",
  "<b>N<sub>A</sub> = 6.0221 &times; 10<sup>23</sup></b> particles per mole, named for Amedeo Avogadro.", 1)

Q(T, "Which sample contains the <b>greatest number of particles</b>?",
  ["0.80 mol of {CO2} molecules", "3.0 &times; 10<sup>23</sup> {H2O} molecules", "0.25 mol of Fe atoms", "4.2 &times; 10<sup>23</sup> {NaCl} formula units"],
  ["0.80 mol &times; 6.0221 &times; 10<sup>23</sup> = 4.8 &times; 10<sup>23</sup> molecules, the largest of the four.",
   "3.0 &times; 10<sup>23</sup> molecules is about 0.50 mol, less than 0.80 mol.",
   "0.25 mol is 1.5 &times; 10<sup>23</sup> atoms, the smallest count here.",
   "4.2 &times; 10<sup>23</sup> formula units is about 0.70 mol, a little less than 0.80 mol."],
  "Put every sample in the same unit, either moles or particles, before comparing.",
  "In moles: CO<sub>2</sub> 0.80; H<sub>2</sub>O 3.0 &times; 10<sup>23</sup> &divide; N<sub>A</sub> = 0.50; Fe 0.25; NaCl 4.2 &times; 10<sup>23</sup> &divide; N<sub>A</sub> = 0.70. <b>0.80 mol of CO<sub>2</sub></b> has the most particles.", 3)

# ======================= ch05-molarmass (16) =======================
T = 'ch05-molarmass'
Q(T, "Why is the molar mass of an element, in g/mol, the same number as its atomic mass in amu?",
  ["Avogadro's number was chosen so that one mole of atoms has a mass in grams equal to the atomic mass in amu.",
   "One gram is defined as one amu.",
   "Every atom has a mass of exactly 1 amu, so the numbers always match.",
   "It is a coincidence that holds only for carbon."],
  ["1 mol of carbon-12 atoms is 12 g, and each atom is 12 amu. That choice of N<sub>A</sub> makes the numbers match for every element.",
   "One amu is about 1.66 &times; 10<sup>" + M + "24</sup> g, far smaller than a gram. It takes Avogadro's number of amu to make 1 g.",
   "Atoms have different masses (H 1.008 amu, Fe 55.85 amu); that is why molar masses differ.",
   "It holds for every element and compound: Na is 22.99 amu per atom and 22.99 g per mole."],
  "How was the size of a mole chosen?",
  "N<sub>A</sub> was chosen so that the mass of 1 mol in grams equals the mass of one particle in amu. So <b>one carbon atom averages 12.011 amu and one mole of carbon has a mass of 12.011 g</b>.", 1)

Q(T, "What is the molar mass of chlorine gas, {Cl2}? (Cl 35.45)",
  [G('Cl2') + " g/mol", G('Cl') + " g/mol", "%d g/mol" % zsum('Cl'), "%d g/mol" % zsum('Cl2')],
  ["Chlorine gas is diatomic: 2(35.45) = 70.90 g/mol.",
   "This is the molar mass of chlorine <i>atoms</i>. Each Cl<sub>2</sub> molecule has two atoms.",
   "17 is chlorine's atomic number (protons), not its mass.",
   "This doubles the atomic number. Use the atomic mass, 35.45, for each atom."],
  "How many Cl atoms are in each molecule, and which number under the symbol is the mass?",
  "{Cl2}: 2(35.45) = <b>" + G('Cl2') + " g/mol</b>. The answer keeps 2 decimal places, like 35.45.", 1, 1)

Q(T, "Ammonia, {NH3}, is used to make most of the nitrogen fertilizer applied in the Valley. What is its molar mass? (" + masses('NH3') + ")",
  [G('NH3') + " g/mol", G('NH') + " g/mol", G('(NH)3') + " g/mol", "%d g/mol" % zsum('NH3')],
  ["14.007 + 3(1.008) = 17.031 g/mol. Both masses have 3 decimal places, so the answer does too.",
   "This counts only one H atom. The subscript 3 means three hydrogen atoms.",
   "This multiplies the N mass by 3 as well. The subscript 3 belongs to H only.",
   "This adds atomic numbers (7 + 3 &times; 1). Molar mass uses the atomic masses."],
  "The subscript applies only to the symbol just before it.",
  "{NH3}: " + mmwork('NH3') + ". So the molar mass is <b>" + G('NH3') + " g/mol</b>.", 1, 1)

Q(T, "Calcium chloride, {CaCl2}, is used in IV solutions and as a road and dust-control salt. What is its <b>formula mass</b>? (" + masses('CaCl2') + ")",
  [G('CaCl2') + " amu", G('CaCl') + " amu", "%d amu" % zsum('CaCl2'), G('CaCl2') + " g"],
  ["40.08 + 2(35.45) = 110.98 amu: the mass of one formula unit.",
   "This counts only one chlorine. CaCl<sub>2</sub> has two Cl atoms per formula unit.",
   "This adds atomic numbers (20 + 2 &times; 17). Use the atomic masses.",
   "The number is right, but 110.98 g is the mass of one <i>mole</i>. One formula unit has a mass in amu."],
  "Formula mass is for one formula unit. What unit goes with one particle?",
  "{CaCl2}: 40.08 + 2(35.45) = <b>" + G('CaCl2') + " amu</b> per formula unit (and 110.98 g per mole).", 2, 1)

Q(T, "Milk of magnesia is a suspension of magnesium hydroxide, {Mg(OH)2}. What is its molar mass? (" + masses('Mg(OH)2') + ")",
  [G('Mg(OH)2') + " g/mol", G('MgOH2') + " g/mol", G('MgOH') + " g/mol", format(rawsum('Mg(OH)2'), 'f') + " g/mol"],
  ["The 2 multiplies both O and H: 24.31 + 2(15.999) + 2(1.008) = 58.324, rounded to 2 decimal places (Mg has 2) = 58.32 g/mol.",
   "This applies the 2 only to H, as if the formula were MgOH<sub>2</sub>. The subscript after the parentheses multiplies everything inside.",
   "This leaves out the subscript 2 after the parentheses; there are two OH groups.",
   "The sum is right but not rounded. In addition, keep the fewest decimal places of the masses used: 24.31 has only 2."],
  "What does the 2 outside the parentheses multiply? Then round by the addition rule.",
  "{Mg(OH)2}: 1 Mg, 2 O, 2 H. " + mmwork('Mg(OH)2') + ". So the molar mass is <b>" + G('Mg(OH)2') + " g/mol</b>.", 2, 1)

Q(T, "Ammonium sulfate, {(NH4)2SO4}, is a common nitrogen fertilizer on Valley orchards. What is its molar mass? (" + masses('(NH4)2SO4') + ")",
  [G('(NH4)2SO4') + " g/mol", G('NH4SO4') + " g/mol", G('N2H4SO4') + " g/mol", format(rawsum('(NH4)2SO4'), 'f') + " g/mol"],
  ["2 N, 8 H, 1 S, 4 O: 2(14.007) + 8(1.008) + 32.06 + 4(15.999) = 132.134, rounded to 2 decimal places (S has 2) = 132.13 g/mol.",
   "This ignores the subscript 2 after the parentheses; there are two ammonium ions.",
   "This doubles N but not H. The 2 outside the parentheses multiplies the H inside too (8 H).",
   "The atom count is right, but the sum must be rounded: 32.06 has only 2 decimal places."],
  "Count atoms first: how many H atoms are in (NH<sub>4</sub>)<sub>2</sub>?",
  "{(NH4)2SO4}: " + mmwork('(NH4)2SO4') + ". So the molar mass is <b>" + G('(NH4)2SO4') + " g/mol</b>.", 2, 1)

Q(T, "Bone mineral is largely calcium phosphate. What is the molar mass of {Ca3(PO4)2}? (" + masses('Ca3(PO4)2') + ")",
  [G('Ca3(PO4)2') + " g/mol", G('Ca3PO4') + " g/mol", G('Ca3P2O4') + " g/mol", "%d g/mol" % zsum('Ca3(PO4)2')],
  ["3 Ca, 2 P, 8 O: 3(40.08) + 2(30.97) + 8(15.999) = 310.172 &rarr; 310.17 g/mol.",
   "This leaves out the subscript 2 after the parentheses, counting one phosphate instead of two.",
   "This doubles P but not O. The 2 multiplies every atom inside the parentheses: 2 &times; 4 = 8 O.",
   "This adds atomic numbers. Use the atomic masses from the yellow sheet."],
  "Two phosphate groups: how many P and how many O?",
  "{Ca3(PO4)2}: " + mmwork('Ca3(PO4)2') + ". So the molar mass is <b>" + G('Ca3(PO4)2') + " g/mol</b>.", 2, 1)

Q(T, "Glucose, {C6H12O6}, has a molar mass of 180.156 g/mol. Which statement is correct?",
  ["One glucose molecule has a mass of 180.156 amu, and one mole of glucose has a mass of 180.156 g.",
   "One glucose molecule has a mass of 180.156 g.",
   "One mole of glucose has a mass of 180.156 amu.",
   "One glucose molecule has a mass of 180.156 g/mol."],
  ["The same number answers both questions: amu for one particle, grams for one mole of particles.",
   "180.156 g is the mass of 6.0221 &times; 10<sup>23</sup> molecules. One molecule is far lighter (about 3 &times; 10<sup>" + M + "22</sup> g).",
   "A mole is a huge number of molecules, so its mass is in grams; amu is for one particle.",
   "g/mol is the unit of molar mass, the mass <i>per mole</i>. One molecule's mass is in amu (or grams)."],
  "One particle: which unit? One mole: which unit?",
  "<b>One molecule: 180.156 amu. One mole: 180.156 g.</b> Molar mass, 180.156 g/mol, links the two.", 1)

Q(T, "Gypsum, calcium sulfate dihydrate ({CaSO4.2H2O}), is the raw material for the plaster and dental stone used to pour dental models. What is its molar mass? (" + masses('CaSO4.2H2O') + ")",
  [G('CaSO4.2H2O') + " g/mol", G('CaSO4') + " g/mol", G('(CaSO4H2O)2') + " g/mol", G('CaSO4.H2O') + " g/mol"],
  ["CaSO<sub>4</sub> (136.136) + 2 H<sub>2</sub>O (2 &times; 18.015 = 36.030) = 172.166 &rarr; 172.17 g/mol.",
   "This is anhydrous calcium sulfate. The &middot;2H<sub>2</sub>O adds the mass of two waters.",
   "This treats the dot as &ldquo;times&rdquo; and doubles the whole formula. The dot means &ldquo;plus&rdquo;: add 2 &times; 18.015.",
   "This adds only one water. The 2 in front of H<sub>2</sub>O means two water molecules per formula unit."],
  "The dot in a hydrate means &ldquo;plus.&rdquo; How many waters are added?",
  "{CaSO4.2H2O}: 40.08 + 32.06 + 4(15.999) + 2(18.015) = 136.136 + 36.030 = 172.166 &rarr; <b>" + G('CaSO4.2H2O') + " g/mol</b> (2 decimal places, from Ca and S).", 2, 1)

Q(T, "Reusable hand-warmer packs contain sodium acetate trihydrate, {NaC2H3O2.3H2O}. What is its molar mass? (" + masses('NaC2H3O2.3H2O') + ")",
  [G('NaC2H3O2.3H2O') + " g/mol", G('NaC2H3O2') + " g/mol", G('(NaC2H3O2H2O)3') + " g/mol", G('NaC2H3O2.H2O') + " g/mol"],
  ["NaC<sub>2</sub>H<sub>3</sub>O<sub>2</sub> (82.034) + 3(18.015) = 82.034 + 54.045 = 136.079 &rarr; 136.08 g/mol (Na has 2 decimal places).",
   "This leaves out the water of hydration. The &middot;3H<sub>2</sub>O is part of the formula.",
   "This multiplies the whole formula by 3. Only the water is counted three times.",
   "This adds one water instead of three."],
  "Find the mass of the salt part, then add three waters.",
  "{NaC2H3O2.3H2O}: 22.99 + 2(12.011) + 3(1.008) + 2(15.999) = 82.034; plus 3(18.015) = 54.045; total 136.079 &rarr; <b>" + G('NaC2H3O2.3H2O') + " g/mol</b>.", 3, 1)

Q(T, "Aspirin is {C9H8O4}. What is its molar mass? (" + masses('C9H8O4') + ")",
  [G('C9H8O4') + " g/mol", "%d g/mol" % zsum('C9H8O4'), G('C9H8(O2)4') + " g/mol", str(mm('C9H8O4').quantize(D('0.01'), rounding=ROUND_HALF_UP)) + " g/mol"],
  ["9(12.011) + 8(1.008) + 4(15.999) = 108.099 + 8.064 + 63.996 = 180.159 g/mol. All three masses have 3 decimal places, so the answer keeps 3.",
   "This adds atomic numbers (9 &times; 6 + 8 &times; 1 + 4 &times; 8). Use the atomic masses.",
   "This uses 31.998 (the mass of O<sub>2</sub>) for each oxygen atom. The formula counts O atoms, 15.999 each.",
   "This rounds to 2 decimal places by habit. Every mass used has 3 decimal places, so the answer keeps 3."],
  "Use 15.999 for each O atom, and count decimal places in the masses you used.",
  "{C9H8O4}: " + mmwork('C9H8O4') + ". So the molar mass is <b>" + G('C9H8O4') + " g/mol</b>.", 2, 1)

Q(T, "Potassium chloride, {KCl}, is used in salt substitutes and potassium supplements. What is its molar mass? (" + masses('KCl') + ")",
  [G('KCl') + " g/mol", "%d g/mol" % zsum('KCl'), G('KCl2') + " g/mol", G('K') + " g/mol"],
  ["39.10 + 35.45 = 74.55 g/mol.",
   "This adds the atomic numbers (19 + 17). Use the atomic masses.",
   "This uses the formula KCl<sub>2</sub>. K<sup>+</sup> and Cl<sup>" + M + "</sup> combine 1 : 1.",
   "This is the molar mass of potassium alone. Add the chlorine."],
  "Add one K and one Cl.",
  "{KCl}: 39.10 + 35.45 = <b>" + G('KCl') + " g/mol</b>.", 1, 1)

Q(T, "Ibuprofen is {C13H18O2}. What is its molar mass? (" + masses('C13H18O2') + ")",
  [G('C13H18O2') + " g/mol", G('C13H18O') + " g/mol", "%d g/mol" % zsum('C13H18O2'), str(mm('C13H18O2').quantize(D('0.01'), rounding=ROUND_HALF_UP)) + " g/mol"],
  ["13(12.011) + 18(1.008) + 2(15.999) = 156.143 + 18.144 + 31.998 = 206.285 g/mol (3 decimal places).",
   "This counts one O atom; the formula has two.",
   "This adds atomic numbers. Use the atomic masses.",
   "This rounds to 2 decimal places, but every mass used has 3, so the answer keeps 3."],
  "Multiply each atomic mass by its subscript, then add.",
  "{C13H18O2}: " + mmwork('C13H18O2') + ". So the molar mass is <b>" + G('C13H18O2') + " g/mol</b>.", 2, 1)

Q(T, "Iron(III) sulfate is {Fe2(SO4)3}. What is its molar mass? (" + masses('Fe2(SO4)3') + ")",
  [G('Fe2(SO4)3') + " g/mol", G('Fe2S3O4') + " g/mol", G('Fe2SO4') + " g/mol", format(rawsum('Fe2(SO4)3'), 'f') + " g/mol"],
  ["2 Fe, 3 S, 12 O: 2(55.85) + 3(32.06) + 12(15.999) = 399.868 &rarr; 399.87 g/mol.",
   "This multiplies S by 3 but not O. The 3 outside the parentheses multiplies every atom inside: 3 &times; 4 = 12 O.",
   "This leaves out the subscript 3 after the parentheses.",
   "The atom count is right, but the sum must be rounded to 2 decimal places (Fe and S have 2)."],
  "Count atoms first: Fe, then S and O inside the parentheses times 3.",
  "{Fe2(SO4)3}: " + mmwork('Fe2(SO4)3') + ". So the molar mass is <b>" + G('Fe2(SO4)3') + " g/mol</b>.", 3, 1)

r = rawsum('Na2CO3')
Q(T, "A student finds the molar mass of sodium carbonate, {Na2CO3}, as 2(22.99) + 12.011 + 3(15.999) = " + format(r, 'f') + ". How should the molar mass be reported?",
  [G('Na2CO3') + " g/mol", format(r, 'f') + " g/mol", num(r, 4) + " g/mol", num(r, 3) + " g/mol"],
  ["This is an addition, so keep the fewest decimal places: 22.99 has 2, so the answer has 2.",
   "The sum is right, but 22.99 has only 2 decimal places, so the answer cannot have 3.",
   "This uses the significant-figure rule for multiplication. Molar mass is a sum, so count decimal places.",
   "This rounds to 3 significant figures, as if multiplying. Subscripts are exact; for a sum, count decimal places."],
  "Is this addition or multiplication? Which rule applies?",
  "Addition rule: fewest decimal places among 22.99 (2), 12.011 (3), 15.999 (3), so 2 places: <b>" + G('Na2CO3') + " g/mol</b>.", 2)

o_sub = (D(8) * D(MS['O']))
Q(T, "The table sets up the molar mass of calcium dihydrogen phosphate, {Ca(H2PO4)2}, a phosphorus fertilizer. What is the molar mass?",
  [G('Ca(H2PO4)2') + " g/mol", G('CaH2PO4') + " g/mol", G('CaH4P2(O2)8') + " g/mol", format(rawsum('Ca(H2PO4)2'), 'f') + " g/mol"],
  ["The O subtotal is 8(15.999) = 127.992. Total 40.08 + 4.032 + 61.94 + 127.992 = 234.044 &rarr; 234.04 g/mol.",
   "This leaves out the subscript 2 after the parentheses, as if the formula were CaH<sub>2</sub>PO<sub>4</sub>. The table already doubles H and P; double O too.",
   "This uses 31.998 (O<sub>2</sub>) for each oxygen atom. The formula counts O atoms, 15.999 each.",
   "The sum is right but needs rounding: Ca (40.08) and P (30.97) have only 2 decimal places."],
  "How many O atoms are in two H<sub>2</sub>PO<sub>4</sub> groups? Then add the subtotals and round by the addition rule.",
  "O: 2 &times; 4 = 8 atoms, 8(15.999) = 127.992. Sum = 234.044, rounded to 2 decimal places = <b>" + G('Ca(H2PO4)2') + " g/mol</b>.", 3, 1,
  [{"type": "table", "cap": "Molar mass of Ca(H<sub>2</sub>PO<sub>4</sub>)<sub>2</sub>", "head": ["Element", "Atoms", "Atomic mass", "Subtotal"],
    "rows": [["Ca", "1", MS['Ca'], MS['Ca']], ["H", "4", MS['H'], format(4 * D(MS['H']), 'f')],
             ["P", "2", MS['P'], format(2 * D(MS['P']), 'f')], ["O", "?", MS['O'], "?"], ["Total", "", "", "?"]]}])

# ======================= ch05-convert (16) =======================
T = 'ch05-convert'
x = D('12.5') / mm('NaCl')
Q(T, "A saline-solution recipe calls for 12.5 g of sodium chloride (58.44 g/mol). How many moles is that?",
  [num(x, 3) + " mol", num(D('12.5') * mm('NaCl'), 3) + " mol", num(mm('NaCl') / D('12.5'), 3) + " mol", num(D('12.5') / zsum('NaCl'), 3) + " mol"],
  ["12.5 g &times; (1 mol / 58.44 g): grams cancel. 12.5 g is about a fifth of a mole (58.44 g).",
   "This multiplies by the molar mass, the factor upside down; the units come out g<sup>2</sup>/mol.",
   "This divides the molar mass by the mass, which leaves 1/mol, not mol.",
   "This divides by 28, the sum of the atomic numbers of Na and Cl, instead of the molar mass."],
  "Grams to moles: which way up does the molar mass go so that grams cancel?",
  "12.5 g NaCl &times; (1 mol NaCl / 58.44 g NaCl) = <b>" + num(x, 3) + " mol</b> (3 significant figures, like 12.5).", 1, 1)

x = D('0.475') * mm('CaCO3')
Q(T, "Calcium carbonate, {CaCO3} (100.09 g/mol), is the active ingredient in many antacids. What is the mass of 0.475 mol of it?",
  [num(x, 3) + " g", num(D('0.475') / mm('CaCO3'), 3) + " g", num(mm('CaCO3') / D('0.475'), 3) + " g", num(D('0.475') * zsum('CaCO3'), 3) + " g"],
  ["0.475 mol &times; 100.09 g/mol: mol cancels, leaving grams. A bit under half a mole should weigh a bit under 50 g.",
   "This divides by the molar mass; moles to grams means multiplying.",
   "This divides the molar mass by the moles, which does not cancel the units.",
   "This uses 50, the sum of atomic numbers (20 + 6 + 3 &times; 8), as the molar mass."],
  "Moles to grams: multiply or divide by the molar mass?",
  "0.475 mol &times; (100.09 g / 1 mol) = <b>" + num(x, 3) + " g</b> of CaCO<sub>3</sub>.", 1, 1)

x = D('126') * 10 / mm('C6H12O6')
Q(T, "A fasting blood glucose is reported as 126 mg/dL. Glucose, {C6H12O6}, has a molar mass of 180.156 g/mol. What is this value in mmol/L?",
  [num(x, 3) + " mmol/L", num(D('126') / mm('C6H12O6'), 3) + " mmol/L", num(x / 1000, 3) + " mmol/L", num(D('126') * 10 * mm('C6H12O6'), 3) + " mmol/L"],
  ["126 mg/dL &times; (10 dL / 1 L) &times; (1 mmol / 180.156 mg). 180.156 g/mol is the same as 180.156 mg/mmol.",
   "This skips the dL &rarr; L step. There are 10 dL in 1 L, so the value per liter is 10 times larger.",
   "This is the value in mol/L, labeled mmol/L. Using mg with mg/mmol gives millimoles directly.",
   "This multiplies by the molar mass; mass to moles means dividing."],
  "Change dL to L first, then use molar mass as 180.156 mg per mmol.",
  "126 mg/dL &times; 10 dL/L = 1260 mg/L; 1260 mg/L &divide; 180.156 mg/mmol = <b>" + num(x, 3) + " mmol/L</b>. (Context only; use the units on the facility's meter.)", 2, 1)

x = D('325') / mm('C9H8O4')
Q(T, "A regular-strength aspirin tablet contains 325 mg of aspirin, {C9H8O4} (180.159 g/mol). How many millimoles of aspirin is that?",
  [num(x, 3) + " mmol", num(x / 1000, 3) + " mmol", num(D('325') * mm('C9H8O4'), 3) + " mmol", num(x * 1000, 3) + " mmol"],
  ["325 mg &divide; 180.159 mg/mmol: mg cancels and leaves mmol (g/mol = mg/mmol).",
   "This is the answer in moles (0.325 g &divide; 180.159 g/mol) labeled as millimoles. Convert mol to mmol, or use mg with mg/mmol.",
   "This multiplies by the molar mass; mass to moles means dividing.",
   "This changes mg to g the wrong way (325 mg is 0.325 g, not 325 000 g)."],
  "g/mol is the same ratio as mg/mmol.",
  "325 mg &times; (1 mmol / 180.159 mg) = <b>" + num(x, 3) + " mmol</b> of aspirin. (Context only; this is not dosing guidance.)", 2, 1)

mol = D('3.50') / mm('NH3'); n = mol * NA
Q(T, "How many ammonia molecules are in 3.50 g of {NH3} (17.031 g/mol)?",
  [num(n, 3) + " molecules", num(mol, 3) + " molecules", num(D('3.50') * NA, 3) + " molecules", num(D('3.50') * mm('NH3') * NA, 3) + " molecules"],
  ["Two steps: 3.50 g &divide; 17.031 g/mol = 0.2055 mol; &times; 6.0221 &times; 10<sup>23</sup> molecules/mol.",
   "This stops after the first step; it is the number of moles, not molecules.",
   "This skips the molar mass and multiplies grams by Avogadro's number. Grams must become moles first.",
   "This multiplies by the molar mass in the first step (upside down), then by Avogadro's number."],
  "Grams to particles takes two steps on the road map. Where is the hub?",
  "3.50 g &times; (1 mol / 17.031 g) &times; (6.0221 &times; 10<sup>23</sup> molecules / 1 mol) = <b>" + num(n, 3) + " molecules</b>.", 2, 1)

mol = D('2.85e20') / NA; g = mol * mm('C8H10N4O2')
Q(T, "A cup of coffee holds about 2.85 &times; 10<sup>20</sup> molecules of caffeine, {C8H10N4O2} (194.194 g/mol). What mass of caffeine is that, in grams?",
  [num(g, 3) + " g", num(mol, 3) + " mol", num(mol / mm('C8H10N4O2'), 3) + " g", num(D('2.85e20') * mm('C8H10N4O2'), 3) + " g"],
  ["Molecules &rarr; moles (&divide; N<sub>A</sub>) &rarr; grams (&times; 194.194 g/mol). That is about 92 mg, typical for a cup of coffee.",
   "This stops at moles. One more step, with the molar mass, gives grams.",
   "This divides by the molar mass in the second step; moles to grams means multiplying.",
   "This multiplies molecules by the molar mass without first dividing by Avogadro's number."],
  "Particles to grams: two steps, through moles.",
  "2.85 &times; 10<sup>20</sup> &divide; 6.0221 &times; 10<sup>23</sup> = " + num(mol, 4) + " mol; &times; 194.194 g/mol = <b>" + num(g, 3) + " g</b> of caffeine (about 92 mg).", 2, 1)

Q(T, "On the mole road map, how do you get from grams of a substance to the number of molecules?",
  ["Two steps: divide by molar mass to get moles, then multiply by Avogadro's number.",
   "One step: multiply grams by Avogadro's number.",
   "One step: divide grams by the molar mass.",
   "Two steps: multiply by molar mass, then divide by Avogadro's number."],
  ["Moles are the hub. Molar mass connects grams and moles; Avogadro's number connects moles and particles.",
   "There is no single factor between grams and particles; grams must become moles first.",
   "Dividing by molar mass gives moles, which is only halfway.",
   "Both factors are upside down: grams &times; g/mol does not cancel grams."],
  "Find the start box and the end box. What is in the middle?",
  "grams &rarr; (&divide; molar mass) &rarr; moles &rarr; (&times; 6.0221 &times; 10<sup>23</sup>) &rarr; molecules: <b>two steps, through moles</b>.", 1)

x = mm('N2O') / NA
Q(T, "Nitrous oxide, {N2O} (44.013 g/mol), is the &ldquo;laughing gas&rdquo; used for sedation in some dental offices. What is the mass of <b>one</b> {N2O} molecule?",
  [num(x, 5) + " g", num(mm('N2O') * NA, 5) + " g", num(NA / mm('N2O'), 5) + " g", G('N2O') + " g"],
  ["One mole (6.0221 &times; 10<sup>23</sup> molecules) has a mass of 44.013 g, so one molecule has 44.013 g &divide; 6.0221 &times; 10<sup>23</sup>.",
   "This multiplies by Avogadro's number; one molecule must be far lighter than a mole, not heavier.",
   "This divides Avogadro's number by the molar mass, which gives molecules per gram, not grams per molecule.",
   "44.013 g is the mass of a whole mole. One molecule is 44.013 amu."],
  "Mass per molecule = mass of one mole &divide; molecules in one mole.",
  "44.013 g/mol &divide; 6.0221 &times; 10<sup>23</sup> molecules/mol = <b>" + num(x, 5) + " g</b> per molecule (5 significant figures, since 44.013 and 6.0221 both have 5).", 2, 1)

x = D('8.00') * mm('KCl')
Q(T, "An oral potassium supplement provides 8.00 mmol of potassium chloride, {KCl} (74.55 g/mol). What mass of KCl is that, in milligrams?",
  [num(x, 3) + " mg", num(D('8.00') / mm('KCl'), 3) + " mg", num(x / 1000, 3) + " mg", num(D('8.00') * mm('K'), 3) + " mg"],
  ["8.00 mmol &times; 74.55 mg/mmol (the same ratio as g/mol) = 596 mg.",
   "This divides by the molar mass; moles to mass means multiplying.",
   "This is the answer in grams (0.596 g) labeled as milligrams.",
   "This uses the molar mass of potassium alone (39.10). The question asks for the mass of KCl, so use 74.55."],
  "mmol &times; (mg/mmol) = mg.",
  "8.00 mmol &times; (74.55 mg / 1 mmol) = <b>" + num(x, 3) + " mg</b> of KCl. (Context only; follow the order and the label.)", 2, 1)

mol = D('2.75e23') / NA; g = mol * mm('Fe')
Q(T, "What is the mass of 2.75 &times; 10<sup>23</sup> iron atoms? (Fe 55.85)",
  [num(g, 3) + " g", num(mol, 3) + " mol", num(mol * Z['Fe'], 3) + " g", num(mol / mm('Fe'), 3) + " g"],
  ["Atoms &rarr; moles (&divide; 6.0221 &times; 10<sup>23</sup> = 0.4567 mol) &rarr; grams (&times; 55.85 g/mol).",
   "This stops at moles; one more step gives grams.",
   "This uses 26, iron's atomic number, as if it were the molar mass.",
   "This divides by the molar mass in the second step instead of multiplying."],
  "Two steps through moles. What is iron's molar mass?",
  "2.75 &times; 10<sup>23</sup> atoms &divide; 6.0221 &times; 10<sup>23</sup> atoms/mol = 0.4567 mol; &times; 55.85 g/mol = <b>" + num(g, 3) + " g</b> Fe.", 2, 1)

Q(T, "You have 10.0 g of each of these gases. Which sample contains the <b>most molecules</b>?",
  ["{CH4} (" + G('CH4') + " g/mol)", "{H2O} (" + G('H2O') + " g/mol)", "{NH3} (" + G('NH3') + " g/mol)", "{CO2} (" + G('CO2') + " g/mol)"],
  ["Same mass, so the lightest molecule gives the most moles: 10.0 g &divide; 16.043 g/mol = 0.623 mol.",
   "10.0 g &divide; 18.015 g/mol = 0.555 mol. Another molecule is lighter.",
   "10.0 g &divide; 17.031 g/mol = 0.587 mol. Close, but another molecule is lighter still.",
   "CO<sub>2</sub> is the heaviest molecule here, so 10.0 g of it has the fewest molecules (0.227 mol)."],
  "For the same mass, do heavier or lighter molecules give more of them?",
  "moles = grams &divide; molar mass, so equal masses give the most moles for the smallest molar mass: <b>CH<sub>4</sub></b> (0.623 mol, versus 0.587 NH<sub>3</sub>, 0.555 H<sub>2</sub>O, 0.227 CO<sub>2</sub>).", 2)

mol = D('0.150') / 1000 / mm('C15H11I4NO4'); n = mol * NA
Q(T, "Thyroxine, {C15H11I4NO4} (776.86 g/mol), is the main hormone made by the thyroid gland. A daily thyroid-replacement dose is on the order of 0.150 mg. How many thyroxine molecules are in 0.150 mg?",
  [num(n, 3) + " molecules", num(D('0.150') / mm('C15H11I4NO4') * NA, 3) + " molecules", num(mol, 3) + " mol", num(D('0.150') / 1000 * mm('C15H11I4NO4') * NA, 3) + " molecules"],
  ["0.150 mg = 1.50 &times; 10<sup>" + M + "4</sup> g; &divide; 776.86 g/mol = 1.931 &times; 10<sup>" + M + "7</sup> mol; &times; 6.0221 &times; 10<sup>23</sup>.",
   "This skips the mg &rarr; g step, so the answer is 1000 times too large. The molar mass is in g/mol.",
   "This stops at moles. One more step gives molecules.",
   "This multiplies by the molar mass instead of dividing in the first step."],
  "Change mg to g first, then go through moles.",
  "1.50 &times; 10<sup>" + M + "4</sup> g &times; (1 mol / 776.86 g) &times; (6.0221 &times; 10<sup>23</sup> / 1 mol) = <b>" + num(n, 3) + " molecules</b>. Even a tiny tablet dose is an enormous number of molecules.", 3, 1)

Q(T, "Which conversion factor changes <b>grams</b> of {NaCl} into <b>moles</b> of {NaCl}?",
  ["1 mol NaCl / 58.44 g NaCl", "58.44 g NaCl / 1 mol NaCl", "6.0221 &times; 10<sup>23</sup> formula units / 1 mol NaCl", "1 mol NaCl / 6.0221 &times; 10<sup>23</sup> formula units"],
  ["Grams on the bottom cancel the grams you start with, leaving mol.",
   "This is the right factor for moles &rarr; grams. Here grams would not cancel.",
   "Avogadro's number connects moles and particles, not grams and moles.",
   "This converts formula units to moles, not grams to moles."],
  "The unit you start with goes on the bottom.",
  "g NaCl &times; <b>(1 mol NaCl / 58.44 g NaCl)</b> = mol NaCl.", 1)

x = D('1.00') / mm('C12H22CaO14') * 1000
Q(T, "A vial contains 1.00 g of calcium gluconate, {C12H22CaO14} (430.37 g/mol). How many millimoles of calcium gluconate is that?",
  [num(x, 3) + " mmol", num(x / 1000, 3) + " mmol", num(D('1.00') * mm('C12H22CaO14'), 3) + " mmol", num(D('1.00') / mm('Ca') * 1000, 3) + " mmol"],
  ["1.00 g &divide; 430.37 g/mol = 0.002324 mol = 2.32 mmol (1 mol = 1000 mmol).",
   "This is the answer in moles (0.00232 mol) labeled as mmol. Multiply by 1000 to get mmol.",
   "This multiplies by the molar mass instead of dividing.",
   "This uses the molar mass of calcium alone. The question asks for moles of the whole compound."],
  "Grams &rarr; moles with the compound's molar mass, then moles &rarr; millimoles.",
  "1.00 g &times; (1 mol / 430.37 g) = 2.324 &times; 10<sup>" + M + "3</sup> mol = <b>" + num(x, 3) + " mmol</b>. (Context only; not dosing guidance.)", 2, 1)

mol = D('11.5') / mm('C2H5OH'); n = mol * NA
wm = D('9.01') / mm('H2O')
Q(T, "Complete the road-map table for ethanol, {C2H5OH}. How many molecules are in 11.5 g?",
  [num(n, 3) + " molecules", num(mol, 3) + " molecules", num(D('11.5') * NA, 3) + " molecules", num(D('11.5') * mm('C2H5OH') * NA, 3) + " molecules"],
  ["11.5 g &divide; 46.069 g/mol = 0.2496 mol; &times; 6.0221 &times; 10<sup>23</sup> = " + num(n, 3) + " molecules, the same two steps as the water column.",
   "This is the moles (0.250 mol), the Moles row. One more step gives molecules.",
   "This skips the molar mass: grams times Avogadro's number. Grams must become moles first.",
   "This multiplies by the molar mass in the first step instead of dividing."],
  "Follow the water row: grams &divide; molar mass = moles; moles &times; N<sub>A</sub> = molecules.",
  "Moles: 11.5 &divide; 46.069 = 0.2496 mol. Molecules: 0.2496 &times; 6.0221 &times; 10<sup>23</sup> = <b>" + num(n, 3) + " molecules</b>.", 3, 1,
  [{"type": "table", "cap": "Grams &rarr; moles &rarr; molecules", "head": ["Quantity", "{H2O}", "{C2H5OH}"],
    "rows": [["Mass (g)", "9.01", "11.5"], ["Molar mass (g/mol)", G('H2O'), G('C2H5OH')], ["Moles", num(wm, 3), "?"], ["Molecules", num(wm * NA, 3), "?"]]}])

Q(T, "Which sample has the <b>greatest mass</b>? Use the molar masses H<sub>2</sub>O 18.015, CO<sub>2</sub> 44.009, NH<sub>3</sub> 17.031, and C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> 180.156 g/mol.",
  ["0.10 mol of {C6H12O6}", "0.50 mol of {H2O}", "0.20 mol of {CO2}", "3.0 &times; 10<sup>23</sup> {NH3} molecules"],
  ["0.10 mol &times; 180.156 g/mol = 18 g, the heaviest sample even though it has the fewest moles.",
   "0.50 mol &times; 18.015 g/mol = 9.0 g. More moles, but each molecule is light.",
   "0.20 mol &times; 44.009 g/mol = 8.8 g.",
   "3.0 &times; 10<sup>23</sup> &divide; 6.0221 &times; 10<sup>23</sup> = 0.50 mol; &times; 17.031 g/mol = 8.5 g."],
  "Convert every sample to grams: moles &times; molar mass (and particles &divide; N<sub>A</sub> first).",
  "Masses: C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> 18 g, H<sub>2</sub>O 9.0 g, CO<sub>2</sub> 8.8 g, NH<sub>3</sub> 8.5 g. <b>0.10 mol of glucose</b> has the greatest mass: the most moles is not always the most grams.", 3)

# ======================= ch05-formula (16) =======================
T = 'ch05-formula'
Q(T, "How many moles of oxygen <b>atoms</b> are in 1 mol of sulfuric acid, {H2SO4}?",
  ["4 mol O", "1 mol O", "2 mol O", "7 mol O"],
  ["The subscript 4 means 4 O atoms per molecule, so 4 mol of O atoms per mole of H<sub>2</sub>SO<sub>4</sub>.",
   "The formula has a subscript 4 on O, not 1.",
   "This counts O<sub>2</sub> molecules (4 O atoms = 2 O<sub>2</sub>). There are no O<sub>2</sub> molecules in H<sub>2</sub>SO<sub>4</sub>; count atoms.",
   "7 is the total number of atoms (2 H + 1 S + 4 O), not the oxygen atoms."],
  "Subscripts count atoms in one molecule, and moles of atoms in one mole.",
  "1 mol {H2SO4} &times; (4 mol O / 1 mol {H2SO4}) = <b>4 mol O</b>.", 1)

Q(T, "Which conversion factor gives moles of <b>hydrogen atoms</b> from moles of glucose, {C6H12O6}?",
  ["12 mol H / 1 mol {C6H12O6}", "1 mol {C6H12O6} / 12 mol H", "6 mol H / 1 mol {C6H12O6}", "24 mol H / 1 mol {C6H12O6}"],
  ["Glucose has 12 H atoms per molecule, so 12 mol H per mole of glucose, with glucose on the bottom to cancel.",
   "The ratio is right but upside down: mol glucose would not cancel.",
   "6 is the subscript on C (and on O), not on H.",
   "24 is the total number of atoms in one glucose molecule, not the hydrogen atoms."],
  "The unit you start with (mol glucose) goes on the bottom.",
  "<b>12 mol H / 1 mol C<sub>6</sub>H<sub>12</sub>O<sub>6</sub></b>. This exact ratio never limits significant figures.", 1)

x = D('0.350') * 6
Q(T, "How many moles of oxygen atoms are in 0.350 mol of calcium nitrate, {Ca(NO3)2}?",
  [num(x, 3) + " mol O", num(D('0.350') * 3, 3) + " mol O", num(D('0.350'), 3) + " mol O", num(D('0.350') / 6, 3) + " mol O"],
  ["Ca(NO<sub>3</sub>)<sub>2</sub> has 2 &times; 3 = 6 O atoms, so 0.350 mol &times; 6 mol O / 1 mol.",
   "This uses 3 O per formula unit, forgetting the 2 outside the parentheses.",
   "This is the moles of calcium nitrate; the subscript step was skipped.",
   "This divides by 6, the ratio upside down. There must be more moles of O than of the compound."],
  "Count O atoms in one formula unit first, including the parentheses.",
  "0.350 mol {Ca(NO3)2} &times; (6 mol O / 1 mol {Ca(NO3)2}) = <b>" + num(x, 3) + " mol O</b>.", 2, 1)

x = D('0.125') * 3 * NA
Q(T, "How many hydrogen <b>atoms</b> are in 0.125 mol of ammonia, {NH3}?",
  [num(x, 3) + " H atoms", num(D('0.125') * NA, 3) + " H atoms", num(D('0.125') * 3, 3) + " mol H", num(D('0.125') / 3 * NA, 3) + " H atoms"],
  ["0.125 mol NH<sub>3</sub> &times; 3 mol H / 1 mol NH<sub>3</sub> = 0.375 mol H; &times; 6.0221 &times; 10<sup>23</sup>.",
   "This is the number of NH<sub>3</sub> molecules. Each molecule has 3 H atoms.",
   "This stops at moles of H; the question asks for the number of atoms.",
   "This divides by 3, the subscript ratio upside down."],
  "Use the subscript ratio first, then Avogadro's number.",
  "0.125 &times; 3 = 0.375 mol H; 0.375 &times; 6.0221 &times; 10<sup>23</sup> = <b>" + num(x, 3) + " H atoms</b>.", 2, 1)

x = D('0.0450') * 3 * NA
Q(T, "Calcium chloride, {CaCl2}, dissolves into {Ca^2+} and {Cl^-} ions. How many ions <b>in total</b> are released by 0.0450 mol of {CaCl2}?",
  [num(x, 3) + " ions", num(D('0.0450') * 2 * NA, 3) + " ions", num(D('0.0450') * NA, 3) + " ions", num(D('0.0450') * 4 * NA, 3) + " ions"],
  ["Each formula unit gives 1 Ca<sup>2+</sup> + 2 Cl<sup>" + M + "</sup> = 3 ions: 0.0450 &times; 3 = 0.135 mol ions; &times; 6.0221 &times; 10<sup>23</sup>.",
   "This counts only the chloride ions. Add the calcium ions.",
   "This counts formula units, not the ions they release.",
   "This counts the 2+ charge as two ions. Ca<sup>2+</sup> is one ion with a 2+ charge."],
  "How many ions come from one formula unit of CaCl<sub>2</sub>?",
  "1 Ca<sup>2+</sup> + 2 Cl<sup>" + M + "</sup> = 3 ions per formula unit. 0.0450 mol &times; 3 = 0.135 mol ions = <b>" + num(x, 3) + " ions</b>.", 2, 1)

x = D('0.400') * 2 * mm('Fe')
Q(T, "Rust is mostly iron(III) oxide, {Fe2O3}. What mass of iron is in 0.400 mol of {Fe2O3}? (Fe 55.85, O 15.999)",
  [num(x, 3) + " g Fe", num(D('0.400') * mm('Fe'), 3) + " g Fe", num(D('0.400') * mm('Fe2O3'), 3) + " g Fe", num(D('0.400') * 2 / mm('Fe'), 3) + " g Fe"],
  ["0.400 mol Fe<sub>2</sub>O<sub>3</sub> &times; 2 mol Fe / 1 mol = 0.800 mol Fe; &times; 55.85 g/mol.",
   "This skips the subscript: Fe<sub>2</sub>O<sub>3</sub> has 2 Fe per formula unit.",
   "This is the mass of the whole compound (0.400 mol &times; 159.70 g/mol), not the iron in it.",
   "This divides by the molar mass of iron in the last step instead of multiplying."],
  "mol compound &rarr; mol Fe (subscript) &rarr; g Fe (molar mass of Fe).",
  "0.400 mol &times; (2 mol Fe / 1 mol {Fe2O3}) &times; (55.85 g Fe / 1 mol Fe) = <b>" + num(x, 3) + " g Fe</b>.", 2, 1)

x = D('325') * mm('Fe') / mm('FeC4H2O4')
Q(T, "An iron supplement tablet contains 325 mg of ferrous fumarate, {FeC4H2O4} (169.91 g/mol). How many milligrams of elemental iron does it provide? (Fe 55.85)",
  [num(x, 3) + " mg Fe", num(D('325') / mm('FeC4H2O4'), 3) + " mg Fe", num(D('325') * mm('FeC4H2O4') / mm('Fe'), 3) + " mg Fe", num(D('325') * Z['Fe'] / mm('FeC4H2O4'), 3) + " mg Fe"],
  ["325 mg &divide; 169.91 mg/mmol = 1.913 mmol compound = 1.913 mmol Fe (1 Fe per formula unit); &times; 55.85 mg/mmol.",
   "This stops at millimoles of ferrous fumarate (1.91 mmol) and labels it mg. One more step, with the molar mass of Fe, gives the mass of iron.",
   "This uses both molar masses upside down; the iron cannot weigh more than the whole tablet compound.",
   "This uses 26, iron's atomic number, instead of its molar mass, 55.85."],
  "mg compound &rarr; mmol compound &rarr; mmol Fe &rarr; mg Fe.",
  "325 mg &times; (1 mmol / 169.91 mg) &times; (1 mmol Fe / 1 mmol) &times; (55.85 mg / 1 mmol Fe) = <b>" + num(x, 3) + " mg Fe</b>, about a third of the tablet's mass. (Context only; follow the label.)", 3, 1)

x = D('1.25') * mm('Ca') / mm('CaCO3')
Q(T, "A calcium supplement tablet contains 1.25 g of calcium carbonate, {CaCO3} (100.09 g/mol). What mass of calcium does it provide? (Ca 40.08)",
  [num(x, 3) + " g Ca", "1.25 g Ca", num(D('1.25') / mm('CaCO3'), 3) + " mol Ca", num(D('1.25') * mm('CaCO3') / mm('Ca'), 3) + " g Ca"],
  ["1.25 g &divide; 100.09 g/mol = 0.01249 mol CaCO<sub>3</sub> = 0.01249 mol Ca; &times; 40.08 g/mol. Calcium is about 40% of the compound.",
   "This treats the whole tablet compound as calcium. Most of the mass is carbonate.",
   "This stops at moles. One more step, with the molar mass of Ca, gives grams.",
   "This uses the molar masses upside down; the calcium cannot weigh more than the compound."],
  "g CaCO<sub>3</sub> &rarr; mol CaCO<sub>3</sub> &rarr; mol Ca &rarr; g Ca.",
  "1.25 g &times; (1 mol / 100.09 g) &times; (1 mol Ca / 1 mol) &times; (40.08 g / 1 mol Ca) = <b>" + num(x, 3) + " g Ca</b> (about 500 mg). (Context only; follow the label.)", 3, 1)

x = D('2.21') * mm('F') / mm('NaF')
Q(T, "A children's fluoride supplement tablet contains 2.21 mg of sodium fluoride, {NaF} (41.99 g/mol). How many milligrams of fluoride does it provide? (F 18.998)",
  [num(x, 3) + " mg F", "2.21 mg F", num(D('2.21') * mm('NaF') / mm('F'), 3) + " mg F", num(D('2.21') / mm('NaF'), 3) + " mg F"],
  ["2.21 mg &divide; 41.99 mg/mmol = 0.05263 mmol NaF = 0.05263 mmol F; &times; 18.998 mg/mmol.",
   "This counts the whole compound as fluoride. Sodium is more than half the mass.",
   "This flips both molar masses; the fluoride cannot weigh more than the compound.",
   "This stops at millimoles of NaF (0.0526 mmol) and labels it mg."],
  "mg NaF &rarr; mmol NaF &rarr; mmol F &rarr; mg F.",
  "2.21 mg &times; (1 mmol / 41.99 mg) &times; (1 mmol F / 1 mmol NaF) &times; (18.998 mg / 1 mmol F) = <b>" + num(x, 3) + " mg F</b>. (Context only; supplements are prescribed by a dentist or physician.)", 2, 1)

x = D('32.4') * 3 * mm('I') / mm('C19H26I3N3O9')
Q(T, "A CT contrast dose contains 32.4 g of iohexol, {C19H26I3N3O9} (821.13 g/mol). What mass of iodine does it contain? (I 126.90)",
  [num(x, 3) + " g I", num(D('32.4') * mm('I') / mm('C19H26I3N3O9'), 3) + " g I", num(D('32.4') * 3 * Z['I'] / mm('C19H26I3N3O9'), 3) + " g I", num(D('32.4') * 3 / mm('C19H26I3N3O9'), 3) + " mol I"],
  ["32.4 g &divide; 821.13 g/mol = 0.03946 mol iohexol; &times; 3 mol I / mol = 0.1184 mol I; &times; 126.90 g/mol.",
   "This skips the subscript 3; each iohexol molecule carries three iodine atoms.",
   "This uses 53, iodine's atomic number, instead of its molar mass, 126.90.",
   "This stops at moles of iodine. One more step gives grams."],
  "g iohexol &rarr; mol iohexol &rarr; mol I (subscript) &rarr; g I.",
  "32.4 g &times; (1 mol / 821.13 g) &times; (3 mol I / 1 mol) &times; (126.90 g / 1 mol I) = <b>" + num(x, 3) + " g I</b>, almost half the mass of the drug.", 3, 1)

x = D('125') * 2 * mm('N') / mm('CO(NH2)2')
Q(T, "Urea, {CO(NH2)2} (60.056 g/mol), is a high-nitrogen fertilizer. What mass of nitrogen is in 125 g of urea? (N 14.007)",
  [num(x, 3) + " g N", num(D('125') * mm('N') / mm('CO(NH2)2'), 3) + " g N", num(D('125') * mm('CO(NH2)2') / (2 * mm('N')), 3) + " g N", num(D('125') * 2 * mm('N2') / mm('CO(NH2)2'), 3) + " g N"],
  ["125 g &divide; 60.056 g/mol = 2.081 mol urea; &times; 2 mol N / mol = 4.163 mol N; &times; 14.007 g/mol.",
   "This counts one N per molecule. The 2 outside (NH<sub>2</sub>)<sub>2</sub> gives two N atoms.",
   "This flips the factors; the nitrogen cannot weigh more than the urea it is in.",
   "This uses 28.014 (the mass of N<sub>2</sub>) for each N atom. Atoms in a compound use 14.007 g/mol."],
  "g urea &rarr; mol urea &rarr; mol N &rarr; g N. How many N atoms are in one urea molecule?",
  "125 g &times; (1 mol / 60.056 g) &times; (2 mol N / 1 mol) &times; (14.007 g / 1 mol N) = <b>" + num(x, 3) + " g N</b>, about 46.6% of the urea, matching its 46-0-0 grade.", 2, 1)

Q(T, "To find the grams of oxygen in 2.00 mol of {CO2}, which molar mass should you use for oxygen in the last step?",
  ["15.999 g/mol, because the formula counts O atoms", "31.998 g/mol, because oxygen is diatomic", "44.009 g/mol, the molar mass of CO<sub>2</sub>", "8 g/mol, oxygen's atomic number"],
  ["2.00 mol CO<sub>2</sub> gives 4.00 mol of O <i>atoms</i>, and each mole of O atoms weighs 15.999 g.",
   "Oxygen is diatomic only as the free element, O<sub>2</sub>. In CO<sub>2</sub> it is present as atoms.",
   "That converts moles of CO<sub>2</sub> to grams of CO<sub>2</sub>, not grams of oxygen.",
   "8 is the number of protons, not the mass of a mole of atoms."],
  "After the subscript step, what particle do your moles count?",
  "2.00 mol CO<sub>2</sub> &times; 2 = 4.00 mol O atoms; &times; <b>15.999 g/mol</b> = 64.0 g O.", 2)

x = D('0.150') * 12
Q(T, "Ammonium phosphate, {(NH4)3PO4}, is a fertilizer. How many moles of hydrogen atoms are in 0.150 mol of it?",
  [num(x, 3) + " mol H", num(D('0.150') * 4, 3) + " mol H", num(D('0.150') * 3, 3) + " mol H", num(D('0.150') / 12, 3) + " mol H"],
  ["(NH<sub>4</sub>)<sub>3</sub> has 3 &times; 4 = 12 H atoms per formula unit: 0.150 &times; 12.",
   "This uses only the 4 inside the parentheses. The 3 outside multiplies it.",
   "This uses only the 3 outside the parentheses.",
   "This divides by 12, the ratio upside down."],
  "Multiply the subscript inside the parentheses by the one outside.",
  "0.150 mol &times; (12 mol H / 1 mol {(NH4)3PO4}) = <b>" + num(x, 3) + " mol H</b>.", 3, 1)

x = D('0.900') / 12
Q(T, "A sample of aluminum sulfate, {Al2(SO4)3}, contains 0.900 mol of oxygen atoms. How many moles of {Al2(SO4)3} is that?",
  [num(x, 3) + " mol", num(D('0.900') * 12, 3) + " mol", num(D('0.900') / 4, 3) + " mol", num(D('0.900') / 3, 3) + " mol"],
  ["Al<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub> has 3 &times; 4 = 12 O per formula unit: 0.900 mol O &times; (1 mol / 12 mol O).",
   "This multiplies by 12. Going from atoms back to the compound, there are fewer moles of compound than of O.",
   "This uses 4 O per formula unit, forgetting the 3 outside the parentheses.",
   "This divides by the 3 outside the parentheses only."],
  "Write the ratio with mol O on the bottom so it cancels.",
  "0.900 mol O &times; (1 mol {Al2(SO4)3} / 12 mol O) = <b>" + num(x, 3) + " mol</b> {Al2(SO4)3}.", 3, 1)

mol = D('1.00') / mm('NaCl'); x = mol * NA
Q(T, "How many sodium <b>ions</b> are in 1.00 g of sodium chloride, {NaCl} (58.44 g/mol)?",
  [num(x, 3) + " Na<sup>+</sup> ions", num(2 * x, 3) + " Na<sup>+</sup> ions", num(mol, 3) + " mol Na<sup>+</sup>", num(D('1.00') / mm('Na') * NA, 3) + " Na<sup>+</sup> ions"],
  ["1.00 g &divide; 58.44 g/mol = 0.01711 mol NaCl = 0.01711 mol Na<sup>+</sup>; &times; 6.0221 &times; 10<sup>23</sup>.",
   "This counts both ions (Na<sup>+</sup> and Cl<sup>" + M + "</sup>). The question asks only for sodium ions.",
   "This stops at moles; one more step gives the number of ions.",
   "This divides by the molar mass of Na (22.99) instead of NaCl. The sample is 1.00 g of the compound."],
  "g NaCl &rarr; mol NaCl &rarr; mol Na<sup>+</sup> &rarr; ions.",
  "1.00 g &times; (1 mol / 58.44 g) &times; (1 mol Na<sup>+</sup> / 1 mol NaCl) &times; 6.0221 &times; 10<sup>23</sup> = <b>" + num(x, 3) + " Na<sup>+</sup> ions</b>.", 2, 1)

Q(T, "The table uses the subscripts of calcium phosphate, {Ca3(PO4)2}, to find moles of each element in 0.200 mol of the compound. What belongs in the cell marked ?",
  [num(D('0.200') * 8, 3) + " mol O", num(D('0.200') * 4, 3) + " mol O", num(D('0.200') * 6, 3) + " mol O", num(D('0.200') / 8, 3) + " mol O"],
  ["2 &times; 4 = 8 O per formula unit: 0.200 &times; 8 = 1.60 mol O, the same pattern as the Ca and P rows.",
   "This uses the 4 inside the parentheses only; the 2 outside doubles it.",
   "This adds the subscripts (4 + 2) instead of multiplying them.",
   "This divides by 8; the ratio is upside down."],
  "How many O atoms are in one formula unit? Follow the pattern of the rows above.",
  "O atoms per formula unit = 2 &times; 4 = 8, so 0.200 mol &times; 8 = <b>1.60 mol O</b>.", 2, 1,
  [{"type": "table", "cap": "Moles of each element in 0.200 mol Ca<sub>3</sub>(PO<sub>4</sub>)<sub>2</sub>", "head": ["Element", "Atoms per formula unit", "Moles in 0.200 mol"],
    "rows": [["Ca", "3", num(D('0.200') * 3, 3)], ["P", "2", num(D('0.200') * 2, 3)], ["O", "8", "?"]]}])

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')),
      'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
