#!/usr/bin/env python3
"""Builds bank/ch06.json (Chapter 6 Try It items: ionic bonding, covalent bonds and Lewis structures, VSEPR shape,
electronegativity and polarity, percent composition, empirical and molecular formulas). Scratch generator; the JSON
file is the deliverable.
usage: python3 tools/gen_bank_ch06.py bank/ch06.json
Conventions (Sections 6.1-6.7): electronegativities and atomic masses are the yellow-sheet values in
tools/yellow_sheet_masses.json. dEN 0-0.4 nonpolar covalent (C-H = 0.4), above 0.4 to 2.0 polar covalent, above 2.0
ionic. VSEPR up to four groups only; no octet exceptions, no resonance, no formal charge. Molar masses by the addition
rule. Percent from a formula: 4 significant figures (as in Section 6.6); from lab masses: the usual rules.
Formulas are typed in braces, {Ca3(PO4)2}, {NH4^+}, {CuSO4.5H2O}. Every item is rechecked by tools/check_bank_ch06.py."""
import json, sys, re, os, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
YS = json.load(open(os.path.join(HERE, 'yellow_sheet_masses.json')))
MS = YS['masses']; EN = YS['electronegativity']
M = '&minus;'
DEG = '&deg;'
B = []

# ---------------- formulas ----------------
def F(s):
    ch = ''
    if '^' in s: s, ch = s.split('^')
    parts = [re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', p) for p in s.split('.')]
    out = '&middot;'.join(parts)
    if ch: out += '<sup>' + ch.replace('-', M) + '</sup>'
    return out
def X(s): return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)

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
def rawsum(f): return sum(D(MS[e]) * n for e, n in parse(f).items())
def mm(f):
    q = min(dp(MS[e]) for e in parse(f))
    return rawsum(f).quantize(D(1).scaleb(-q), rounding=ROUND_HALF_UP)
def G(f): return str(mm(f))
def part(f, e): return parse(f)[e] * D(MS[e])

def num(x, n):
    x = D(x); e = x.adjusted()
    m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if m >= 10:
        e += 1; m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if -3 <= e <= n - 1:
        s = format(m.scaleb(e).quantize(D(1).scaleb(min(0, e - n + 1))), 'f')
        if e == n - 1 and s.endswith('0'): s += '.'
        return s
    return '%s &times; 10<sup>%s</sup>' % (m, (M + str(-e)) if e < 0 else str(e))
def P(x, n=4): return num(D(x) * 100, n) + '%'
def den(a, b): return abs(D(EN[a]) - D(EN[b]))
def ENs(*els): return ', '.join('%s %s' % (e, EN[e]) for e in els)
def MSs(*els): return ', '.join('%s %s' % (e, MS[e]) for e in els)
DE = '&Delta;EN'
S1, S2, S3 = '&ndash;', '=', '&equiv;'

def Q(t, q, c, y, h, w, d, k=0, f=None):
    it = {"id": "c6-%03d" % (len(B) + 1), "t": t, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    if f:
        for fg in f:
            if fg['type'] == 'table':
                fg['head'] = [X(x) for x in fg['head']]; fg['rows'] = [[X(x) for x in r] for r in fg['rows']]
                if 'cap' in fg: fg['cap'] = X(fg['cap'])
        it["f"] = f
    B.append(it)

# ======================= ch06-ionic (9) =======================
T = 'ch06-ionic'
Q(T, "When sodium reacts with chlorine to form sodium chloride, what happens to sodium's single valence electron?",
  ["It transfers to chlorine, forming {Na^+} and {Cl^-} ions.",
   "It is shared equally between Na and Cl in a covalent bond.",
   "Chlorine gives an electron to sodium, forming Na<sup>" + M + "</sup> and Cl<sup>+</sup> ions.",
   "It leaves sodium, but chlorine stays neutral, so only {Na^+} forms."],
  ["Sodium (a metal, 1 valence electron) gives its electron to chlorine (a nonmetal, 7 valence electrons). Both ions end up with noble-gas configurations, and the opposite charges attract: an ionic bond.",
   "Sharing happens between two nonmetals. A metal and a nonmetal transfer electrons instead.",
   "This moves the electron the wrong way. Metals lose electrons and become cations; nonmetals gain them and become anions.",
   "Electrons lost must equal electrons gained. The electron sodium loses is the one chlorine gains."],
  "Metal + nonmetal: share or transfer? Which one loses electrons?",
  "Na &middot; + Cl (7 dots) &rarr; {Na^+} + {Cl^-} (8 dots). The electron <b>transfers from Na to Cl</b>, and the attraction between the ions is the ionic bond.", 1)

Q(T, "Which pair of elements is most likely to form an <b>ionic</b> bond?",
  ["Mg and O", "C and O", "N and H", "Cu and Zn"],
  ["Magnesium is a metal (2 valence electrons) and oxygen a nonmetal that needs 2: Mg gives 2 electrons to O, forming {Mg^2+} and {O^2-} (MgO).",
   "Carbon and oxygen are both nonmetals; they share electrons (covalent bonds), as in CO<sub>2</sub>.",
   "Nitrogen and hydrogen are both nonmetals; they share electrons, as in NH<sub>3</sub>.",
   "Copper and zinc are both metals. Neither one needs extra electrons, so there is no metal-to-nonmetal transfer."],
  "Look for a metal paired with a nonmetal.",
  "Metal + nonmetal means electron transfer: <b>Mg and O</b> form the ionic compound MgO. (Their electronegativity difference, 3.5 &minus; 1.2 = 2.3, is also above 2.0.)", 1)

Q(T, "When calcium and oxygen form calcium oxide, CaO, how many electrons does each calcium atom lose, and how many does each oxygen atom gain?",
  ["Ca loses 2; O gains 2", "Ca loses 1; O gains 1", "Ca gains 2; O loses 2", "Ca loses 2; O gains 6"],
  ["Ca is in group 2 (2 valence electrons) and O in group 16 (6 valence electrons, needs 2 for an octet). 2 lost = 2 gained, so the formula is 1 : 1.",
   "Calcium has 2 valence electrons, and oxygen needs 2. Losing or gaining one would leave Ca<sup>+</sup> and O<sup>" + M + "</sup>, which are not their usual ions.",
   "This reverses the transfer. The metal (Ca) loses electrons; the nonmetal (O) gains them.",
   "Oxygen <i>has</i> 6 valence electrons; it needs only 2 more to reach 8."],
  "Use group numbers: how many valence electrons does Ca have, and how many does O need?",
  "Ca (group 2) &rarr; {Ca^2+} by losing 2; O (6 valence electrons) &rarr; {O^2-} by gaining 2. <b>Ca loses 2, O gains 2</b>: electrons lost = electrons gained, CaO.", 2)

Q(T, "Aluminum and fluorine form an ionic compound. How many fluorine atoms are needed to accept the electrons from <b>one</b> aluminum atom?",
  ["3", "1", "2", "7"],
  ["Al (group 13) loses 3 electrons; each F (7 valence electrons) gains only 1. Three F atoms take all three: {AlF3}.",
   "One F atom can accept only one electron, leaving Al with two more to give.",
   "Two F atoms take 2 electrons, but Al gives away 3.",
   "7 is the number of valence electrons fluorine already has, not the number of F atoms needed."],
  "How many electrons does Al lose? How many can one F accept?",
  "Al &rarr; {Al^3+} + 3 e<sup>" + M + "</sup>; each F + 1 e<sup>" + M + "</sup> &rarr; {F^-}. Electrons lost (3) = electrons gained (3 &times; 1), so <b>3</b> F atoms: {AlF3}.", 2)

Q(T, "In the magnesium-oxide lab (Section 6.7), some magnesium reacts with nitrogen in the air to form magnesium nitride. Each Mg atom loses 2 electrons and each N atom gains 3. Which formula makes electrons lost equal electrons gained?",
  ["{Mg3N2}", "{Mg2N3}", "MgN", "{Mg3N}"],
  ["3 Mg lose 3 &times; 2 = 6 electrons, and 2 N gain 2 &times; 3 = 6 electrons. Lost = gained, and (3)(2+) + (2)(3" + M + ") = 0.",
   "2 Mg lose 4 electrons but 3 N would need 9. The charges were placed on the wrong atoms (the swap was skipped).",
   "1 Mg loses 2 electrons, but 1 N needs 3: they do not balance.",
   "3 Mg lose 6 electrons, but 1 N gains only 3."],
  "Find the smallest numbers of Mg and N atoms that make (electrons lost) = (electrons gained). The least common multiple of 2 and 3 is 6.",
  "6 electrons: 3 Mg &times; 2 lost = 2 N &times; 3 gained. Formula <b>{Mg3N2}</b>, the same one swap-drop gives from {Mg^2+} and {N^3-}.", 3)

Q(T, "Which compound is a <b>base</b> (a metal hydroxide)?",
  ["KOH", "KCl", "{K2O}", "{CH3OH}"],
  ["Potassium hydroxide is made of {K^+} and {OH^-} ions; it releases {OH^-} in water.",
   "KCl is a salt: a cation with an anion other than {OH^-} or {O^2-}.",
   "{K2O} is a metal oxide: it contains the oxide ion, {O^2-}, not hydroxide.",
   "Methanol contains an O&ndash;H group, but it is a molecular compound of nonmetals, not an ionic hydroxide. It does not release {OH^-} ions."],
  "A base in this course is an ionic compound containing the hydroxide ion. Which choices are ionic, and which contains {OH^-}?",
  "Salts, bases, and metal oxides are the three ionic types. <b>KOH</b> (K<sup>+</sup> and OH<sup>" + M + "</sup>) is the base; KCl is a salt, {K2O} a metal oxide, and {CH3OH} a molecular compound.", 1)

Q(T, "Quicklime, CaO, reacts with water to form slaked lime: CaO + {H2O} &rarr; {Ca(OH)2}. How are CaO and {Ca(OH)2} classified?",
  ["CaO is a metal oxide; {Ca(OH)2} is a base.",
   "Both are salts.",
   "CaO is a base; {Ca(OH)2} is a metal oxide.",
   "CaO is a salt; {Ca(OH)2} is a metal oxide."],
  ["CaO contains {O^2-}, so it is a metal oxide. {Ca(OH)2} contains {OH^-}, so it is a base. Many metal oxides react with water to form bases, exactly as here.",
   "Salts contain an anion other than {OH^-} or {O^2-}. Both of these contain one of those two ions.",
   "This swaps the names: the oxide ion is in CaO, and the hydroxide ion is in {Ca(OH)2}.",
   "CaO contains the oxide ion, which makes it a metal oxide rather than a salt; {Ca(OH)2} contains hydroxide, which makes it a base."],
  "Look at the anion in each: {O^2-} or {OH^-}?",
  "CaO (Ca<sup>2+</sup>, O<sup>2" + M + "</sup>) is a <b>metal oxide</b>; {Ca(OH)2} (Ca<sup>2+</sup>, 2 OH<sup>" + M + "</sup>) is a <b>base</b>.", 2)

Q(T, "Which property is typical of an ionic compound such as sodium chloride?",
  ["A hard, brittle solid with a high melting point",
   "A soft solid that melts below 100 " + DEG + "C",
   "A solid that conducts electricity well",
   "A substance made of separate NaCl molecules"],
  ["Each ion in the crystal lattice is held by many strong attractions to ions of opposite charge, so it takes a lot of energy to melt (NaCl melts at 801 " + DEG + "C).",
   "Low melting points are typical of molecular substances such as wax or sugar, not ionic lattices.",
   "In the solid, the ions are locked in place, so solid ionic compounds do not conduct.",
   "Ionic compounds have no molecules. NaCl is a lattice; the formula gives the ratio of ions (a formula unit)."],
  "Picture the crystal lattice. How many attractions hold each ion in place?",
  "Ionic solids are lattices of cations and anions: <b>hard, brittle, high-melting</b>, and conducting only when melted or dissolved.", 1)

Q(T, "Which sample conducts electricity?",
  ["Calcium chloride melted at high temperature",
   "Solid calcium chloride crystals",
   "Solid table sugar",
   "Sugar dissolved in pure water"],
  ["When an ionic compound melts, its ions are free to move, so the liquid carries a current.",
   "In the solid, the {Ca^2+} and {Cl^-} ions are locked in the lattice and cannot move.",
   "Sugar is a molecular compound; it has no ions to carry a current.",
   "Sugar dissolves as whole, neutral molecules, not ions, so the solution does not conduct."],
  "Electric current needs charged particles that can move. Which sample has mobile ions?",
  "Only an ionic compound that is melted or dissolved has moving ions. <b>Melted calcium chloride</b> conducts; the solid does not, and sugar (molecular) never forms ions.", 2)

# ======================= ch06-lewis (13) =======================
T = 'ch06-lewis'
Q(T, "How many valence electrons are in phosphorus trichloride, {PCl3}?",
  ["26", "12", "32", "66"],
  ["P is in group 15 (5) and each Cl in group 17 (7): 5 + 3(7) = 26.",
   "This counts only one Cl (5 + 7). The subscript 3 means three Cl atoms.",
   "This gives every atom 8, the number of electrons each will <i>have</i> in the octet, not the number available.",
   "This adds atomic numbers (15 + 3 &times; 17), which counts all electrons, not just valence electrons."],
  "Use group numbers for valence electrons, and multiply by subscripts.",
  "P: 5; Cl: 3 &times; 7 = 21. Total = <b>26</b> valence electrons.", 1)

Q(T, "How many valence electrons are in the hydronium ion, {H3O^+}?",
  ["8", "9", "10", "14"],
  ["O has 6 and each H has 1: 6 + 3 = 9; the 1+ charge means one electron fewer, so 8.",
   "This forgets the charge. A positive ion has lost an electron.",
   "This adds an electron for the charge. Add for negative charges, subtract for positive charges.",
   "This counts 8 for O and 2 for each H, the electrons each atom will end up with, not the valence electrons available."],
  "Add the group numbers, then adjust for the charge. Does a 1+ charge add or remove an electron?",
  "6 + 3(1) &minus; 1 = <b>8</b> valence electrons for {H3O^+}.", 2)

Q(T, "How many valence electrons are in the phosphate ion, {PO4^3-}?",
  ["32", "29", "26", "14"],
  ["5 (P) + 4 &times; 6 (O) = 29, plus 3 for the 3&minus; charge = 32.",
   "This forgets the 3&minus; charge. Each negative charge is one extra electron.",
   "This subtracts 3 for the charge. A negative ion has gained electrons.",
   "This counts only one O atom: 5 + 6 + 3. The subscript 4 means four O atoms."],
  "Add group numbers, multiply by the subscript, then add one electron for each negative charge.",
  "5 + 4(6) + 3 = <b>32</b> valence electrons for {PO4^3-}.", 2)

Q(T, "Which atom is the central atom in oxygen difluoride, {OF2}?",
  ["O, because it appears once and is less electronegative than F",
   "F, because it appears twice",
   "F, because it is the most electronegative element",
   "Either atom; the skeleton does not matter for a three-atom molecule"],
  ["The atom that appears once, and the less electronegative one (O 3.5 versus F 4.0), goes in the middle: F&ndash;O&ndash;F.",
   "An atom that appears more than once is usually on the outside, around the single atom.",
   "The most electronegative atom is usually an outer atom; halogens are usually on the outside.",
   "The skeleton matters: F&ndash;F&ndash;O and F&ndash;O&ndash;F are different molecules, and only one gives every atom an octet with 20 electrons."],
  "The central atom is usually the one that appears once and is less electronegative.",
  "<b>O is central</b>: F&ndash;O&ndash;F, with two lone pairs on O and three on each F (20 electrons).", 1)

Q(T, "The Lewis structure of {PCl3} has P in the center with three P&ndash;Cl bonds. How many <b>lone pairs</b> does the whole molecule have?",
  ["10", "1", "9", "13"],
  ["26 electrons &minus; 6 in three bonds = 20, or 10 lone pairs: 3 on each Cl (9) and 1 on P.",
   "This counts only the lone pair on P. Each Cl also has three lone pairs.",
   "This counts the Cl lone pairs but leaves out the lone pair on P. P has 3 bonds + 1 lone pair = 8 electrons.",
   "This counts the three bonding pairs as lone pairs too. Bonds are shared pairs, not lone pairs."],
  "Total valence electrons, minus the electrons in bonds, divided by 2.",
  "26 &minus; 3(2) = 20 nonbonding electrons = <b>10 lone pairs</b> (P: 1; each Cl: 3). Check: 3 &times; 2 + 10 &times; 2 = 26.", 2)

Q(T, "Hydrofluoric acid gel is used to etch porcelain veneers in dental offices. Which describes the Lewis structure of hydrogen fluoride, HF?",
  ["H&ndash;F, with three lone pairs on F",
   "H&ndash;F, with three lone pairs on F and one lone pair on H",
   "H=F, with two lone pairs on F",
   "H&ndash;F, with four lone pairs on F"],
  ["8 valence electrons (1 + 7): one bond (2) + three lone pairs on F (6). H has its duet and F has its octet.",
   "Hydrogen needs only 2 electrons, and its one bond already supplies them. H never has lone pairs.",
   "A double bond would give H 4 electrons. Hydrogen forms only one bond.",
   "Four lone pairs plus a bond is 10 electrons, more than the 8 available, and would give F 10 electrons."],
  "Count valence electrons (H 1, F 7). Hydrogen gets a duet, F an octet.",
  "1 + 7 = 8 electrons: <b>H&ndash;F with three lone pairs on F</b>. (Context only; HF is extremely hazardous to skin.)", 2)

Q(T, "Which describes the Lewis structure of nitrogen gas, {N2}, which makes up 78% of air?",
  ["N&equiv;N, with one lone pair on each N",
   "N=N, with two lone pairs on each N",
   "N&ndash;N, with three lone pairs on each N",
   "N&equiv;N, with no lone pairs"],
  ["10 valence electrons: a triple bond (6) + one lone pair on each N (4). Each N has 6 + 2 = 8.",
   "This uses 4 + 8 = 12 electrons, but N<sub>2</sub> has only 2 &times; 5 = 10.",
   "This uses 2 + 12 = 14 electrons, more than the 10 available. Never add electrons to complete octets.",
   "This uses only 6 electrons and leaves each N with 6, not 8."],
  "N<sub>2</sub> has 10 valence electrons. Which picture uses exactly 10 and gives each N an octet?",
  "2 &times; 5 = 10 electrons. A single bond leaves N short, so lone pairs move into bonds until <b>N&equiv;N with one lone pair on each N</b> (6 + 2 + 2 = 10).", 2)

Q(T, "Acetylene (ethyne), the fuel in welding torches, is H&ndash;C&equiv;C&ndash;H. How many bonds does each carbon atom form, counting a triple bond as three?",
  ["4", "2", "3", "5"],
  ["One C&ndash;H single bond (1) + one C&equiv;C triple bond (3) = 4, matching HONC (C forms 4 bonds).",
   "This counts the lines to neighboring atoms (2) instead of bonds. A triple bond counts as three bonds.",
   "This counts only the triple bond and leaves out the C&ndash;H bond.",
   "Carbon forms 4 bonds in neutral molecules; 5 bonds would give it 10 electrons."],
  "HONC 1-2-3-4: how many bonds should C have? A triple bond counts as three.",
  "Each C: 1 (C&ndash;H) + 3 (C&equiv;C) = <b>4 bonds</b>, 8 electrons, no lone pairs. Total 5 bonding pairs = 10 electrons = 2(4) + 2(1).", 2)

Q(T, "Methanol, {CH3OH}, has 14 valence electrons. Which structure is correct?",
  ["H<sub>3</sub>C&ndash;O&ndash;H, with two lone pairs on O",
   "H<sub>3</sub>C&ndash;H&ndash;O, with three lone pairs on O",
   "H<sub>3</sub>C&ndash;O&ndash;H, with no lone pairs",
   "H<sub>3</sub>C&ndash;O&ndash;H, with three lone pairs on O"],
  ["5 bonds (10 electrons) + 2 lone pairs on O (4) = 14. C has 4 bonds, O has 2 bonds and 2 lone pairs, each H has 1 bond, all matching HONC.",
   "This puts H in the middle with two bonds. Hydrogen forms only one bond, so it is never central.",
   "This uses only 10 electrons and leaves O with 4. Outer and inner O atoms keep their lone pairs.",
   "This uses 16 electrons, more than the 14 available, and gives O 10 electrons."],
  "The formula is written in groups: a CH<sub>3</sub> group bonded to an OH group. Then count electrons.",
  "4 + 4(1) + 6 = 14 electrons: <b>H<sub>3</sub>C&ndash;O&ndash;H with two lone pairs on O</b>. Check: 5 &times; 2 + 2 &times; 2 = 14.", 2)

Q(T, "Phosgene, {COCl2}, has C as the central atom and 24 valence electrons. Which Lewis structure is correct?",
  ["C single-bonded to each Cl and double-bonded to O; 2 lone pairs on O and 3 on each Cl",
   "C single-bonded to O and to each Cl; 3 lone pairs on O and 3 on each Cl",
   "C double-bonded to O and to one Cl, single-bonded to the other Cl; 2 lone pairs on O, 2 on the double-bonded Cl, 3 on the other Cl",
   "C single-bonded to O and to each Cl; 1 lone pair on C, 3 on O, and 3 on each Cl"],
  ["4 bonding pairs (8 electrons) + 8 lone pairs (16) = 24. C has 4 bonds (8 electrons); O and each Cl have 8.",
   "This uses 24 electrons, but C has only 3 bonds (6 electrons). Move a lone pair from O into a C=O double bond.",
   "This gives C 5 bonds (10 electrons), breaking the octet, and gives Cl two bonds. Halogens usually form one bond.",
   "This uses 26 electrons, 2 more than are available. Make a double bond; never add electrons."],
  "Start with single bonds and lone pairs. Is C short of an octet? Which atom (O or Cl) usually forms a double bond?",
  "Single bonds use 6, lone pairs on O and Cl use 18 (24 total), but C has only 6. One O lone pair moves into a bond: <b>C=O with two C&ndash;Cl bonds</b>. O forms 2 bonds (HONC), Cl forms 1.", 3)

Q(T, "Which describes the Lewis structure of the ammonium ion, {NH4^+}?",
  ["N bonded to four H atoms, no lone pairs, in brackets with a 1+ charge",
   "N bonded to four H atoms, one lone pair on N, in brackets with a 1+ charge",
   "N bonded to three H atoms, one lone pair on N, and the fourth H bonded to another H",
   "N bonded to four H atoms, no lone pairs, in brackets with a 1&minus; charge"],
  ["5 + 4 &minus; 1 = 8 electrons: four N&ndash;H bonds use all 8. N has 8 and each H has 2. Ions are drawn in brackets with the charge outside.",
   "This uses 10 electrons, the count you get by adding (not subtracting) an electron for the 1+ charge, and gives N 10 electrons.",
   "One H would have two bonds. Hydrogen forms only one bond.",
   "The bonds are right, but the charge is wrong. A 1&minus; ion would have 10 electrons; this structure has 8, so it is 1+."],
  "Count electrons (subtract one for the 1+ charge), then place bonds.",
  "{NH4^+}: 5 + 4(1) &minus; 1 = 8 electrons = <b>four N&ndash;H bonds and no lone pairs</b>, drawn as [NH<sub>4</sub>]<sup>+</sup>.", 2)

Q(T, "Ethylene, {C2H4}, is the gas that ripens fruit in packing-house ripening rooms. It has 12 valence electrons. After you draw a C&ndash;C single bond and four C&ndash;H bonds, how many electrons are left, and what do you do with them?",
  ["2 are left; they become a second C&ndash;C bond, making C=C",
   "2 are left; add 2 more electrons so each C can have a lone pair",
   "None are left; the structure with single bonds is finished",
   "7 are left; place them as lone pairs on the carbons"],
  ["5 single bonds use 10 electrons, leaving 2. As a lone pair, they would give one C 8 electrons and the other only 6, so they are shared instead: C=C. Each C then has 4 bonds.",
   "Never add electrons you do not have. If octets are short, make a multiple bond.",
   "5 bonds &times; 2 = 10, not 12: 2 electrons remain, and each C has only 6 electrons with single bonds.",
   "This counts each bond line as 1 electron (12 &minus; 5). Every line is a pair, 2 electrons."],
  "Each line is 2 electrons. How many electrons do 5 single bonds use?",
  "12 &minus; 5(2) = <b>2 left</b>. With single bonds each C has 6 electrons, so the last pair becomes a second C&ndash;C bond: H<sub>2</sub>C=CH<sub>2</sub>, 6 bonding pairs = 12 electrons.", 3)

Q(T, "How many electrons are shared in the triple bond of {N2}?",
  ["6", "3", "2", "10"],
  ["A triple bond is three shared pairs: 3 &times; 2 = 6 electrons.",
   "This counts each line as one electron. Each line is a pair.",
   "Two electrons make a single bond, one shared pair.",
   "10 is the total number of valence electrons in N<sub>2</sub>, including the two lone pairs."],
  "One line = one shared pair = 2 electrons.",
  "N&equiv;N: 3 lines &times; 2 = <b>6 electrons</b> shared. The more pairs shared, the shorter and stronger the bond.", 1)

# ======================= ch06-vsepr (12) =======================
T = 'ch06-vsepr'
Q(T, "In formaldehyde, {CH2O}, carbon has two C&ndash;H bonds and one C=O double bond. How many electron groups surround the carbon?",
  ["3", "4", "5", "6"],
  ["Each bond counts as one group, whether single or double: 2 + 1 = 3 groups, so carbon is trigonal planar.",
   "This counts the double bond as two groups. Any bond between two atoms is one group.",
   "This counts the two lone pairs on O. Only groups on the central atom count.",
   "This counts the double bond twice and also the lone pairs on O."],
  "Count regions of electrons around C only; a double bond is one region.",
  "C: two C&ndash;H bonds + one C=O = <b>3 groups</b>, no lone pairs: trigonal planar, 120" + DEG + ".", 1)

Q(T, "A central atom has <b>3 electron groups</b>, and <b>1</b> of them is a lone pair. What is the molecular shape?",
  ["bent, about 120" + DEG, "trigonal planar, 120" + DEG, "trigonal pyramidal, about 109.5" + DEG, "linear, 180" + DEG],
  ["3 groups spread to 120" + DEG + " (trigonal planar electron geometry). With one lone pair, the atoms form a bent shape, as in O<sub>3</sub>.",
   "Trigonal planar is the electron geometry. The shape names only the atoms, and one corner is a lone pair.",
   "Trigonal pyramidal needs 4 groups with 1 lone pair.",
   "Linear needs 2 groups (or 2 atoms on a 180" + DEG + " line); here there are 3 groups."],
  "Electron geometry from the number of groups; then remove the lone pair to name the shape.",
  "3 groups, 1 lone pair: <b>bent, about 120" + DEG + "</b> (electron geometry trigonal planar).", 1)

Q(T, "Phosphine, {PH3}, is a fumigant gas used on stored grain and nuts. P has three P&ndash;H bonds and one lone pair. What is its shape?",
  ["trigonal pyramidal", "tetrahedral", "trigonal planar", "bent"],
  ["3 bonds + 1 lone pair = 4 groups (tetrahedral electron geometry). The lone pair is not named, so the shape is a pyramid, like NH<sub>3</sub>.",
   "Tetrahedral is the electron geometry of 4 groups. One group is a lone pair, so the shape is not tetrahedral.",
   "Trigonal planar would need 3 groups and no lone pair; the lone pair counts as a fourth group.",
   "Bent (4 groups) has 2 lone pairs and 2 bonds; PH<sub>3</sub> has 3 bonds."],
  "Count groups on P, including the lone pair; then name the shape from the atoms only.",
  "4 groups, 1 lone pair: <b>trigonal pyramidal</b>, about 109.5" + DEG + ". (Context only; phosphine is highly toxic.)", 2)

Q(T, "Water, {H2O}, has two O&ndash;H bonds and two lone pairs on O. What are its electron-group geometry and its molecular shape?",
  ["tetrahedral electron geometry; bent shape",
   "bent electron geometry; tetrahedral shape",
   "linear electron geometry; linear shape",
   "trigonal planar electron geometry; bent shape"],
  ["4 groups (2 bonds + 2 lone pairs) point to the corners of a tetrahedron. Only the 3 atoms are named, so the shape is bent, about 109.5" + DEG + ".",
   "This swaps the two terms. Electron geometry includes the lone pairs (tetrahedral); the shape names only atoms (bent).",
   "The Lewis structure is often drawn in a line, but the two lone pairs push the H atoms into a bent shape.",
   "This counts only 3 groups. O has 2 bonds and 2 lone pairs, 4 groups in all."],
  "Count all groups on O for the electron geometry; then look at the atoms only.",
  "O: 2 bonds + 2 lone pairs = 4 groups: <b>tetrahedral electron geometry, bent shape</b> (about 109.5" + DEG + "; measured 104.5" + DEG + ").", 2)

Q(T, "Ground-level ozone, {O3}, is the main summer smog pollutant in the San Joaquin Valley. Its central O atom has one double bond, one single bond, and one lone pair. What is the shape of {O3}?",
  ["bent, about 120" + DEG, "bent, about 109.5" + DEG, "linear, 180" + DEG, "trigonal planar, 120" + DEG],
  ["3 groups (a double bond, a single bond, and a lone pair) give trigonal planar electron geometry; with one lone pair the shape is bent, about 120" + DEG + ".",
   "Bent at about 109.5" + DEG + " is the 4-group bent shape (2 lone pairs, as in water). The central O in ozone has 3 groups.",
   "Linear needs 2 groups. The lone pair on the central O is a third group.",
   "Trigonal planar is the electron geometry; the shape names only the three O atoms."],
  "Count groups on the central O: each bond is one group, and so is the lone pair.",
  "Central O: 1 double + 1 single + 1 lone pair = 3 groups, 1 lone pair: <b>bent, about 120" + DEG + "</b>.", 2)

Q(T, "Methane, {CH4}, the main component of natural gas and of biogas from dairy digesters, has four C&ndash;H bonds and no lone pairs. What is the H&ndash;C&ndash;H bond angle?",
  ["109.5" + DEG, "90" + DEG, "120" + DEG, "180" + DEG],
  ["Four bonding groups spread out to the corners of a tetrahedron, 109.5" + DEG + " apart.",
   "90" + DEG + " is what the flat Lewis drawing suggests, but the molecule is three-dimensional; a tetrahedron spreads the bonds farther apart.",
   "120" + DEG + " is the angle for 3 groups (trigonal planar).",
   "180" + DEG + " is the angle for 2 groups (linear)."],
  "4 groups, 0 lone pairs. Think of four balloons tied together.",
  "4 groups, 0 lone pairs: tetrahedral, <b>109.5" + DEG + "</b>.", 1)

Q(T, "In acetylene, H&ndash;C&equiv;C&ndash;H, what is the shape around each carbon atom?",
  ["linear, 180" + DEG, "tetrahedral, 109.5" + DEG, "trigonal planar, 120" + DEG, "bent, about 120" + DEG],
  ["Each C has two groups, a single bond to H and a triple bond to the other C, so the groups point opposite each other.",
   "This counts the triple bond as three groups (1 + 3 = 4). A triple bond is one group.",
   "Three groups would need another bond or a lone pair on C; each C has only two groups.",
   "Each C has no lone pairs, so there is nothing to bend it."],
  "How many groups are on each C? A triple bond counts once.",
  "Each C: 1 single + 1 triple = 2 groups, no lone pairs: <b>linear, 180" + DEG + "</b>. The whole molecule is a straight line.", 3)

Q(T, "In carbon tetrachloride, {CCl4}, each Cl has three lone pairs. How many electron groups are on the central carbon?",
  ["4", "16", "12", "8"],
  ["C has four C&ndash;Cl bonds and no lone pairs: 4 groups (tetrahedral). The lone pairs on the Cl atoms belong to the outer atoms.",
   "This adds the 12 lone pairs on the Cl atoms to the 4 bonds. Only groups on the central atom count.",
   "12 is the number of lone pairs on the outer Cl atoms. They do not surround the C.",
   "This counts electrons in the bonds (4 &times; 2) instead of groups."],
  "Look only at the central atom. What touches C directly?",
  "C: 4 bonds, 0 lone pairs = <b>4 groups</b>; tetrahedral, 109.5" + DEG + ". Lone pairs on outer atoms do not change the shape.", 2)

Q(T, "Complete the row for sulfur dichloride, {SCl2}, whose S atom has two S&ndash;Cl bonds and two lone pairs.",
  ["4 / 2: bent, about 109.5" + DEG, "2 / 0: linear, 180" + DEG, "4 / 2: tetrahedral, 109.5" + DEG, "3 / 1: bent, about 120" + DEG],
  ["2 bonds + 2 lone pairs = 4 groups, 2 of them lone pairs: bent, like water.",
   "This counts only the bonds. Lone pairs on the central atom are groups too.",
   "Tetrahedral is the electron geometry. With 2 lone pairs, only 3 atoms are named, and they make a bent shape.",
   "This counts one lone pair. S (6 valence electrons) with 2 bonds keeps 2 lone pairs."],
  "Fill in groups / lone pairs first, then read the shape from the six-shape table.",
  "{SCl2}: <b>4 groups / 2 lone pairs: bent, about 109.5" + DEG + "</b>, the same pattern as H<sub>2</sub>O.", 3, 0,
  [{"type": "table", "cap": "Groups and lone pairs on the central atom", "head": ["Molecule", "Groups / lone pairs", "Shape"],
    "rows": [["{CH4}", "4 / 0", "tetrahedral"], ["{PCl3}", "4 / 1", "trigonal pyramidal"], ["{SCl2}", "?", "?"]]}])

Q(T, "Which molecule is <b>trigonal planar</b>?",
  ["{CH2O}", "{NH3}", "{PCl3}", "{O3}"],
  ["C has 3 groups (two C&ndash;H bonds and one C=O) and no lone pairs: all three positions hold atoms, 120" + DEG + " apart.",
   "N has 3 bonds plus a lone pair: 4 groups, trigonal pyramidal.",
   "P has 3 bonds plus a lone pair: 4 groups, trigonal pyramidal. Three outer atoms are not enough for trigonal planar.",
   "The central O has 3 groups, but one is a lone pair, so ozone is bent."],
  "Trigonal planar needs 3 groups and no lone pairs on the central atom.",
  "Only <b>{CH2O}</b> has 3 groups and 0 lone pairs. NH<sub>3</sub> and PCl<sub>3</sub> are trigonal pyramidal (4 groups, 1 lone pair); O<sub>3</sub> is bent.", 2)

Q(T, "Why do {CH4} and {NH3} have different shapes, even though both central atoms have four electron groups?",
  ["The shape names only atom positions; N has a lone pair in place of a fourth atom.",
   "N has fewer electron groups than C.",
   "Lone pairs do not take up any space around the central atom.",
   "C is larger than N, so its bonds spread out more."],
  ["Both have tetrahedral electron geometry. In NH<sub>3</sub> one corner is a lone pair, so the atoms form a trigonal pyramid instead of a tetrahedron.",
   "Both have 4 groups: C has 4 bonds; N has 3 bonds + 1 lone pair.",
   "Lone pairs take up space (a little more than bonds); that is why they still push the bonds into a pyramid.",
   "Atom size is not what VSEPR uses. The difference is a lone pair versus a bond."],
  "Compare electron geometry with molecular shape.",
  "Both have 4 groups (tetrahedral electron geometry), but <b>the shape names only atoms</b>: CH<sub>4</sub> tetrahedral; NH<sub>3</sub> (1 lone pair) trigonal pyramidal.", 1)

Q(T, "The hydronium ion, {H3O^+}, has three O&ndash;H bonds and one lone pair on O. What is its shape?",
  ["trigonal pyramidal", "trigonal planar", "tetrahedral", "bent"],
  ["3 bonds + 1 lone pair = 4 groups: tetrahedral electron geometry, trigonal pyramidal shape, like NH<sub>3</sub>.",
   "This ignores the lone pair. It is a fourth group and pushes the H atoms out of the plane.",
   "Tetrahedral is the electron geometry; one corner is a lone pair, which is not named in the shape.",
   "Bent (4 groups) would need 2 lone pairs and 2 bonds."],
  "An ion is handled exactly like a molecule: count groups on the central atom.",
  "{H3O^+}: 4 groups, 1 lone pair: <b>trigonal pyramidal</b>, about 109.5" + DEG + ".", 3)

# ======================= ch06-polarity (12) =======================
T = 'ch06-polarity'
Q(T, "Which of these elements is the <b>most electronegative</b>? (Yellow-sheet values are in the feedback.)",
  ["O", "N", "Cl", "S"],
  ["O is " + EN['O'] + ", second only to fluorine (4.0).",
   "N is " + EN['N'] + ". It is to the left of O in period 2, so it is less electronegative.",
   "Cl is " + EN['Cl'] + ". It is high, but O is higher.",
   "S is " + EN['S'] + ". It is below O in group 16, and electronegativity decreases down a group."],
  "Electronegativity increases toward fluorine: across a period and up a group.",
  "O " + EN['O'] + " &gt; N " + EN['N'] + " = Cl " + EN['Cl'] + " &gt; S " + EN['S'] + ". <b>O</b> is the most electronegative of these.", 1)

Q(T, "Which statement describes the periodic trend in electronegativity?",
  ["It increases across a period and decreases down a group.",
   "It decreases across a period and increases down a group.",
   "It increases across a period and increases down a group.",
   "It is about the same for every element in a group."],
  ["The trend matches ionization energy: F (upper right) is highest, and metals at the lower left are lowest.",
   "This reverses both directions. F (upper right) is the most electronegative element.",
   "Down a group, the valence electrons are farther from the nucleus, so the pull on shared electrons decreases (F 4.0, Cl 3.0).",
   "Values change down a group: F 4.0, Cl 3.0, Br 2.8, I 2.5."],
  "Where is fluorine on the periodic table?",
  "Electronegativity <b>increases across a period and decreases down a group</b>; fluorine (4.0) is highest.", 1)

Q(T, "Nitrogen dioxide from vehicle exhaust helps form the Valley's summer ozone. What is " + DE + " for an N&ndash;O bond, and what kind of bond is it? (" + ENs('N', 'O') + ")",
  [DE + " = 0.5, polar covalent", DE + " = 6.5, ionic", DE + " = 0.5, nonpolar covalent", DE + " = &minus;0.5, nonpolar covalent"],
  ["3.5 &minus; 3.0 = 0.5. That is above 0.4 (and not above 2.0), so the bond is polar covalent, with O as &delta;&minus;.",
   "This adds the values. " + DE + " is a difference: subtract the smaller from the larger.",
   "0.5 is just above the 0&ndash;0.4 nonpolar range, so the bond is polar covalent.",
   "Subtract the smaller value from the larger, so " + DE + " is never negative; 0.5 is in the polar covalent range."],
  "Subtract the smaller value from the larger, then compare with 0.4 and 2.0.",
  DE + " = 3.5 &minus; 3.0 = <b>0.5, polar covalent</b>; O carries &delta;&minus;.", 2)

Q(T, "Classify the C&ndash;H bond using the yellow-sheet values (" + ENs('C', 'H') + ").",
  ["nonpolar covalent (" + DE + " = 0.4)", "polar covalent (" + DE + " = 0.4)", "ionic (" + DE + " = 0.4)", "polar covalent (" + DE + " = 4.6)"],
  ["2.5 &minus; 2.1 = 0.4, which is inside the 0 to 0.4 range for nonpolar covalent bonds. This is why hydrocarbons are nonpolar.",
   "0.4 is the top of the nonpolar range; polar covalent starts above 0.4.",
   "Ionic bonds need " + DE + " above 2.0, and two nonmetals share electrons.",
   "This adds the two values. " + DE + " is the difference."],
  "Compute 2.5 &minus; 2.1 and compare with the 0.4 cutoff.",
  DE + " = 2.5 &minus; 2.1 = 0.4: <b>nonpolar covalent</b>. Remember from lecture: C&ndash;H is essentially nonpolar.", 2)

Q(T, "In fluorapatite, the fluoride-strengthened mineral of tooth enamel, fluoride ions sit next to calcium ions. Classify the Ca&ndash;F bond. (" + ENs('Ca', 'F') + ")",
  ["ionic (" + DE + " = 3.0)", "polar covalent (" + DE + " = 3.0)", "ionic (" + DE + " = 5.0)", "polar covalent (" + DE + " = 1.0)"],
  ["4.0 &minus; 1.0 = 3.0, above 2.0: ionic. Calcium (a metal) gives electrons to fluorine, forming {Ca^2+} and {F^-}.",
   "The difference is right, but 3.0 is above the 2.0 cutoff, which puts it in the ionic range.",
   "This adds the values instead of subtracting.",
   "This uses calcium's value alone. " + DE + " is the difference between the two atoms' values."],
  "Subtract, then compare with 0.4 and 2.0.",
  DE + " = 4.0 &minus; 1.0 = <b>3.0, ionic</b>: fluorapatite is an ionic crystal of Ca<sup>2+</sup>, PO<sub>4</sub><sup>3" + M + "</sup>, and F<sup>" + M + "</sup>.", 2)

Q(T, "In an O&ndash;H bond, which atom carries the partial negative charge (&delta;&minus;), and which way does the dipole arrow point? (" + ENs('O', 'H') + ")",
  ["O is &delta;&minus;; the arrow points toward O",
   "H is &delta;&minus;; the arrow points toward H",
   "O is &delta;&minus;; the arrow points toward H",
   "Neither; the O&ndash;H bond is nonpolar"],
  ["O (3.5) pulls the shared pair harder than H (2.1), so O is &delta;&minus; and H is &delta;+. The arrow points toward the more electronegative atom, with the cross at the H (positive) end.",
   "H is the less electronegative atom, so it is the &delta;+ end.",
   "The partial charges are right, but the arrow points toward the &delta;&minus; atom, not away from it.",
   DE + " = 3.5 &minus; 2.1 = 1.4, well above 0.4: the bond is polar."],
  "The more electronegative atom gets the electrons, the &delta;&minus;, and the arrowhead.",
  "O&ndash;H: " + DE + " = 1.4, polar covalent. <b>O is &delta;&minus;, and the dipole arrow points toward O</b> (cross at H).", 2)

Q(T, "Which bond is the <b>most polar</b>? (" + ENs('H', 'C', 'N', 'O', 'Cl') + ")",
  ["O&ndash;H", "C&ndash;Cl", "N&ndash;H", "C&ndash;O"],
  [DE + " = 3.5 &minus; 2.1 = 1.4, the largest difference here.",
   DE + " = 3.0 &minus; 2.5 = 0.5, barely polar.",
   DE + " = 3.0 &minus; 2.1 = 0.9.",
   DE + " = 3.5 &minus; 2.5 = 1.0, polar but less than another bond here."],
  "Compute " + DE + " for each bond; the largest difference is the most polar.",
  "C&ndash;Cl 0.5 &lt; N&ndash;H 0.9 &lt; C&ndash;O 1.0 &lt; O&ndash;H 1.4. <b>O&ndash;H</b> is the most polar.", 2)

Q(T, "Carbon dioxide, O=C=O, has polar C=O bonds. Is the {CO2} molecule polar or nonpolar?",
  ["Nonpolar: it is linear, and the two equal bond dipoles point in opposite directions and cancel.",
   "Polar, because each C=O bond is polar.",
   "Polar, because oxygen is more electronegative than carbon.",
   "Nonpolar, because " + DE + " for C=O is 0.4 or less."],
  ["Two identical dipoles on a straight line cancel, like a tug-of-war between equal teams. This is why CO<sub>2</sub> moves so easily through nonpolar cell membranes.",
   "Polar bonds are needed for a polar molecule, but they are not enough. The shape decides whether they cancel.",
   "That makes each bond polar; it does not tell you whether the bond dipoles cancel.",
   "The bonds are polar: " + DE + " = 3.5 &minus; 2.5 = 1.0. The molecule is nonpolar for a different reason."],
  "Lewis structure &rarr; shape &rarr; do the bond dipoles cancel?",
  "C has 2 groups and no lone pairs: linear. Equal C=O dipoles (" + DE + " 1.0) point opposite ways and cancel: <b>CO<sub>2</sub> is nonpolar</b>.", 2)

Q(T, "Which molecule is <b>polar</b>?",
  ["{CH3Cl}", "{CCl4}", "{CH4}", "{Cl2}"],
  ["Tetrahedral, but one C&ndash;Cl bond and three C&ndash;H bonds: the outer atoms are not identical, so the dipoles do not cancel.",
   "Four identical C&ndash;Cl dipoles point symmetrically to the corners of a tetrahedron and cancel. Polar bonds, nonpolar molecule.",
   "C&ndash;H bonds are nonpolar (" + DE + " 0.4), and the molecule is symmetrical.",
   "Two identical atoms share electrons equally (" + DE + " 0)."],
  "SNAP: Symmetrical is Nonpolar, Asymmetrical is Polar. Which tetrahedral molecule has different outer atoms?",
  "<b>{CH3Cl}</b> is asymmetrical (one Cl, three H), so it is polar. CCl<sub>4</sub> and CH<sub>4</sub> are symmetrical; Cl<sub>2</sub> has no polar bond.", 2)

Q(T, "In the lungs, {O2} and {CO2} cross the thin, fatty membranes of the alveoli and capillaries very quickly. Which statement explains this?",
  ["Both are small, nonpolar molecules.",
   "Both are polar molecules, like water.",
   "{CO2} is polar and {O2} is nonpolar.",
   "Both are ionic compounds that dissolve in the membrane."],
  ["O<sub>2</sub> has identical atoms (" + DE + " 0), and CO<sub>2</sub> is linear with canceling dipoles. Nonpolar molecules pass easily through the nonpolar membrane.",
   "Neither is polar. O<sub>2</sub> has no polar bonds; CO<sub>2</sub>'s bond dipoles cancel.",
   "CO<sub>2</sub> has polar bonds, but its linear shape cancels them, so the molecule is nonpolar.",
   "Both are molecules of nonmetals held by covalent bonds; neither contains ions."],
  "Decide the polarity of each gas: O=O, and O=C=O (linear).",
  "<b>Both are small nonpolar molecules</b>, so they slip through the nonpolar membrane; ions such as Na<sup>+</sup> need protein channels.", 3)

Q(T, "Which molecule is <b>nonpolar</b> even though its bonds are polar?",
  ["{CF4}", "{NF3}", "{CH2F2}", "HF"],
  ["C has 4 identical C&ndash;F bonds and no lone pairs: a symmetrical tetrahedron, so the four dipoles cancel.",
   "N has a lone pair, so NF<sub>3</sub> is trigonal pyramidal and the N&ndash;F dipoles do not cancel.",
   "Tetrahedral, but with two H and two F: not symmetrical, so it is polar.",
   "A single polar bond (" + DE + " 1.9) with nothing to cancel it: polar."],
  "SNAP: look for a symmetrical shape, identical outer atoms, and no lone pairs on the central atom.",
  "<b>{CF4}</b>: polar C&ndash;F bonds (" + DE + " 1.5), but the symmetrical tetrahedral shape cancels them.", 3)

Q(T, "Water is bent. Suppose instead it were linear, H&ndash;O&ndash;H in a straight line. What would be true?",
  ["It would be nonpolar, because the two equal O&ndash;H dipoles would cancel.",
   "It would still be polar, because the O&ndash;H bonds are polar.",
   "It would become an ionic compound.",
   "It would be nonpolar, because the O&ndash;H bonds would stop being polar."],
  ["Two identical dipoles pointing in opposite directions cancel, as in CO<sub>2</sub>. Water's real bent shape is what keeps it polar, so it can dissolve ions and sugars in blood.",
   "Polar bonds alone do not make a polar molecule; in a straight line, equal dipoles would cancel.",
   "Shape does not change bond type. O and H are nonmetals that share electrons.",
   "Bond polarity comes from electronegativity (" + DE + " 1.4), not from shape. The bonds stay polar; their dipoles would cancel."],
  "Compare with CO<sub>2</sub>: linear, two equal polar bonds.",
  "A linear H&ndash;O&ndash;H would be <b>nonpolar</b> (dipoles cancel). Because real water is bent, the dipoles add and water is polar.", 3)

# ======================= ch06-percent (10) =======================
T = 'ch06-percent'
f = 'NaCl'; r = part(f, 'Na') / mm(f)
Q(T, "Food labels list sodium, not salt. What is the mass percent of sodium in sodium chloride, NaCl (58.44 g/mol)? (Na 22.99)",
  [P(r), P(D(MS['Na']) / D(MS['Cl'])), P(part(f, 'Cl') / mm(f)), P(mm(f) / D(MS['Na']))],
  ["22.99 &divide; 58.44 &times; 100% = 39.34%. Each gram of salt is less than half sodium.",
   "This divides by the mass of Cl (35.45). Divide by the whole compound, 58.44.",
   "This is the percent of chlorine. The question asks for sodium.",
   "This divides the wrong way. A part cannot be more than 100% of the whole."],
  "Part &divide; whole &times; 100%.",
  "%Na = 22.99 &divide; 58.44 &times; 100% = <b>" + P(r) + "</b>. Check: %Cl = " + P(part(f, 'Cl') / mm(f)) + "; together 100.00%.", 1, 1)

f = '(NH4)2SO4'; r = part(f, 'N') / mm(f)
Q(T, "Ammonium sulfate, {(NH4)2SO4} (" + G(f) + " g/mol), is a nitrogen fertilizer used on Valley orchards. What is its mass percent of nitrogen? (N 14.007)",
  [P(r), P(D(MS['N']) / mm(f)), P((part(f, 'N') + part(f, 'H')) / mm(f)), P(part(f, 'N') / mm('NH4SO4'))],
  ["2(14.007) &divide; 132.13 &times; 100% = 21.20%. The 2 outside the parentheses gives two N atoms.",
   "This counts one N. The subscript 2 after (NH<sub>4</sub>) means two ammonium ions, so two N atoms.",
   "This is the percent of the whole NH<sub>4</sub> groups (N and H together), not nitrogen alone.",
   "This divides by the molar mass of NH<sub>4</sub>SO<sub>4</sub>, leaving out the second ammonium ion."],
  "How many N atoms are in the formula? Multiply the atomic mass by that subscript before dividing.",
  "%N = 2(14.007) &divide; " + G(f) + " &times; 100% = 28.014 &divide; " + G(f) + " &times; 100% = <b>" + P(r) + "</b> (fertilizer grade 21-0-0).", 2, 1)

f = 'Ca3(PO4)2'; r = part(f, 'Ca') / mm(f)
Q(T, "Bone mineral is largely calcium phosphate, {Ca3(PO4)2} (" + G(f) + " g/mol). What is its mass percent of calcium? (Ca 40.08)",
  [P(r), P(D(MS['Ca']) / mm(f)), P(part(f, 'P') / mm(f)), P(part(f, 'Ca') / mm('Ca3PO4'))],
  ["3(40.08) = 120.24; 120.24 &divide; 310.17 &times; 100% = 38.77%.",
   "This uses one Ca atom. The formula has three.",
   "This is the percent of phosphorus, 2(30.97) &divide; 310.17.",
   "This divides by the molar mass of Ca<sub>3</sub>PO<sub>4</sub>, leaving out the second phosphate."],
  "Subscript &times; atomic mass, divided by the molar mass of the whole compound.",
  "%Ca = 3(40.08) &divide; " + G(f) + " &times; 100% = <b>" + P(r) + "</b>.", 2, 1)

f = 'C2H5OH'; r = part(f, 'C') / mm(f)
Q(T, "Ethanol, {C2H5OH} (" + G(f) + " g/mol), is the alcohol in hand sanitizer. What is its mass percent of carbon? (C 12.011)",
  [P(r), P(D(MS['C']) / mm(f)), P(D(2) / D(9)), P(part(f, 'O') / mm(f))],
  ["2(12.011) &divide; 46.069 &times; 100% = 24.022 &divide; 46.069 &times; 100% = 52.14%.",
   "This counts one C atom; ethanol has two.",
   "This is the percent of the <i>atoms</i> that are carbon (2 of 9). Mass percent uses masses, not atom counts.",
   "This is the percent of oxygen, 15.999 &divide; 46.069."],
  "Mass of carbon in one mole &divide; molar mass &times; 100%.",
  "%C = 2(12.011) &divide; " + G(f) + " &times; 100% = <b>" + P(r) + "</b>.", 2, 1)

f = 'FeSO4.7H2O'; r = part(f, 'Fe') / mm(f)
Q(T, "Iron tablets often contain ferrous sulfate heptahydrate, {FeSO4.7H2O} (" + G(f) + " g/mol). What percent of this compound's mass is iron? (Fe 55.85)",
  [P(r), P(D(MS['Fe']) / mm('FeSO4')), P(D(MS['Fe']) / mm('FeSO4.H2O')), P(mm(f) / D(MS['Fe']))],
  ["55.85 &divide; 278.01 &times; 100% = 20.09%. The seven waters are part of the formula, so they are part of the whole.",
   "This uses the molar mass of anhydrous FeSO<sub>4</sub> (151.91). The tablet compound includes 7 waters.",
   "This adds only one water. The 7 in front of H<sub>2</sub>O means seven waters.",
   "This divides the wrong way; a part cannot be more than 100% of the whole."],
  "Use the molar mass of the whole hydrate, water included.",
  "%Fe = 55.85 &divide; " + G(f) + " &times; 100% = <b>" + P(r) + "</b>. A 325 mg tablet of this hydrate holds about 65 mg of iron. (Context only.)", 3, 1)

Q(T, "One sample of pure sodium chloride comes from sea salt, and another is mined rock salt from a different continent. What does the law of constant composition say about them?",
  ["Both have the same mass percent of sodium.",
   "The larger sample has the higher mass percent of sodium.",
   "Their percents differ, because they come from different places.",
   "Both are 50% sodium, because NaCl has one Na and one Cl."],
  ["A pure compound always contains the same elements in the same proportions by mass, wherever it comes from: NaCl is always 39.34% Na.",
   "Percent composition does not depend on sample size; that is the point of a percent.",
   "The source does not matter for a pure compound. (Impurities in unrefined salt would change the measured percent, but not the composition of NaCl itself.)",
   "Equal numbers of atoms do not mean equal masses: Na (22.99) is lighter than Cl (35.45)."],
  "What stays the same for every pure sample of a compound?",
  "Law of constant composition (definite proportions): every pure sample of NaCl has <b>the same mass percent of sodium</b>.", 1)

z = D('1.950') - D('1.308')
Q(T, "A student heats 1.308 g of zinc powder with excess sulfur. The zinc sulfide product has a mass of 1.950 g. What is the mass percent of zinc in the product?",
  [P(D('1.308') / D('1.950'), 4), P(z / D('1.950'), 3), P(D('1.308') / z, 3), P(D('1.308') / (D('1.950') + D('1.308')), 4)],
  ["1.308 g &divide; 1.950 g &times; 100% = 67.08% (4 significant figures). ZnS is " + P(D(MS['Zn']) / mm('ZnS')) + " Zn, so the result fits.",
   "This is the percent of sulfur, 0.642 g &divide; 1.950 g.",
   "This divides zinc by sulfur. Divide the part by the whole product.",
   "This adds the zinc mass to the product mass. The product already includes the zinc."],
  "The product is the whole; the zinc is the part.",
  "%Zn = 1.308 &divide; 1.950 &times; 100% = <b>" + P(D('1.308') / D('1.950'), 4) + "</b>; %S = 0.642 &divide; 1.950 &times; 100% = " + P(z / D('1.950'), 3) + ".", 2, 1)

o = D('1.502') - D('1.200')
Q(T, "Heating 1.200 g of copper in air produces 1.502 g of a black copper oxide. What is the mass percent of oxygen in the oxide?",
  [P(o / D('1.502'), 3), P(o / D('1.200'), 3), P(D('1.200') / D('1.502'), 4), P(o / (D('1.502') + D('1.200')), 3)],
  ["Oxygen gained = 1.502 &minus; 1.200 = 0.302 g (3 significant figures, from the subtraction). 0.302 &divide; 1.502 &times; 100% = 20.1%.",
   "This divides by the copper mass. The whole is the oxide product, 1.502 g.",
   "This is the percent of copper, not oxygen.",
   "This adds the copper and oxide masses. The oxide mass already includes the copper."],
  "By conservation of mass, oxygen = product &minus; metal. Then part &divide; whole.",
  "O = 1.502 g &minus; 1.200 g = 0.302 g; %O = 0.302 &divide; 1.502 &times; 100% = <b>" + P(o / D('1.502'), 3) + "</b> (CuO is " + P(D(MS['O']) / mm('CuO')) + " O).", 2, 1)

mg = D('25.701') - D('25.412'); ox = D('25.893') - D('25.412'); oo = D('25.893') - D('25.701')
Q(T, "The table shows a student's data from the magnesium-oxide lab (Experiment 5a). What is the mass percent of magnesium in the product?",
  [P(mg / ox, 3), P(mg / D('25.893'), 3), P(oo / ox, 3), P(mg / oo, 3)],
  ["Mg = 25.701 &minus; 25.412 = 0.289 g; oxide = 25.893 &minus; 25.412 = 0.481 g. 0.289 &divide; 0.481 &times; 100% = 60.1%, close to MgO's 60.31%.",
   "This divides by the crucible + lid + oxide mass. Subtract the crucible first to get the mass of the oxide alone.",
   "This is the percent of oxygen: (25.893 &minus; 25.701) &divide; 0.481.",
   "This divides the magnesium by the oxygen (0.192 g). Divide by the whole oxide."],
  "Subtract the empty crucible from each reading first.",
  "Mg 0.289 g, oxide 0.481 g: %Mg = 0.289 &divide; 0.481 &times; 100% = <b>" + P(mg / ox, 3) + "</b>.", 3, 1,
  [{"type": "table", "cap": "Magnesium oxide lab data", "head": ["Measurement", "Mass (g)"],
    "rows": [["Crucible + lid", "25.412"], ["Crucible + lid + Mg", "25.701"], ["Crucible + lid + oxide", "25.893"]]}])

Q(T, "A compound of carbon, hydrogen, and oxygen is 54.53% C and 9.15% H by mass, and the rest is oxygen. What is its mass percent of oxygen?",
  ["36.32%", "45.47%", "90.85%", "63.68%"],
  ["All the percents add to 100%: 100 &minus; 54.53 &minus; 9.15 = 36.32% O.",
   "This subtracts only the carbon. Hydrogen must be subtracted too.",
   "This subtracts only the hydrogen.",
   "This is the C and H added together, not the oxygen."],
  "The percents of all the elements add up to 100%.",
  "%O = 100% &minus; 54.53% &minus; 9.15% = <b>36.32%</b> (2 decimal places, from the subtraction).", 2, 1)

# ======================= ch06-empirical (10) =======================
T = 'ch06-empirical'
Q(T, "Butane, {C4H10}, is lighter fluid. What is its empirical formula?",
  ["{C2H5}", "{C4H10}", "{CH2}", "{C8H20}"],
  ["Divide both subscripts by 2, their largest common factor: C<sub>2</sub>H<sub>5</sub>. 5 cannot be divided further.",
   "4 and 10 share a factor of 2, so this is not the simplest ratio.",
   "This is close to 1 : 2.5 but rounded. Subscripts must be whole numbers in the exact ratio.",
   "This multiplies by 2 instead of dividing. The empirical formula is the smallest ratio."],
  "Find the largest number that divides every subscript.",
  "C<sub>4</sub>H<sub>10</sub> &divide; 2 = <b>{C2H5}</b>.", 1)

Q(T, "Which two compounds have the <b>same empirical formula</b>?",
  ["{C2H2} and {C6H6}", "{C2H4} and {C2H6}", "CO and {CO2}", "{H2O} and {H2O2}"],
  ["Both reduce to CH: 2 : 2 = 1 : 1 and 6 : 6 = 1 : 1.",
   "C<sub>2</sub>H<sub>4</sub> reduces to CH<sub>2</sub>; C<sub>2</sub>H<sub>6</sub> reduces to CH<sub>3</sub>.",
   "CO is 1 : 1 and CO<sub>2</sub> is 1 : 2; both are already in lowest terms and differ.",
   "H<sub>2</sub>O is already simplest; H<sub>2</sub>O<sub>2</sub> reduces to HO."],
  "Reduce each formula to its smallest whole-number ratio.",
  "C<sub>2</sub>H<sub>2</sub> (acetylene) and C<sub>6</sub>H<sub>6</sub> (benzene) are both <b>CH</b>.", 1)

Q(T, "In a lab, 1.020 g of aluminum reacts with oxygen to form 1.927 g of aluminum oxide. What is the empirical formula of the oxide? (" + MSs('Al', 'O') + ")",
  ["{Al2O3}", "{AlO2}", "AlO", "{Al3O2}"],
  ["O = 1.927 &minus; 1.020 = 0.907 g. Al: 1.020 &divide; 26.98 = 0.03781 mol; O: 0.907 &divide; 15.999 = 0.05669 mol. Ratio 1 : 1.499, and 1.5 &times; 2 = 3: Al<sub>2</sub>O<sub>3</sub>.",
   "This rounds 1.5 up to 2. A ratio near 1.5 means multiply everything by 2.",
   "This rounds 1.5 down to 1. Multiply by 2 instead of rounding.",
   "This inverts the ratio; the oxygen moles are the larger number."],
  "Mass of O by subtraction, then grams &rarr; moles, then divide by the smaller.",
  "Al 0.03781 mol : O 0.05669 mol = 1 : 1.499; &times; 2 = 2 : 3. <b>{Al2O3}</b>, as {Al^3+} and {O^2-} predict.", 3, 1)

Q(T, "An oxide of sulfur is 50.05% S and 49.95% O by mass. What is its empirical formula? (" + MSs('S', 'O') + ")",
  ["{SO2}", "SO", "{S2O}", "{SO3}"],
  ["Per 100 g: S, 50.05 &divide; 32.06 = 1.561 mol; O, 49.95 &divide; 15.999 = 3.122 mol. Ratio 1 : 2.000.",
   "This compares grams (50.05 g and 49.95 g, nearly equal) instead of moles. O atoms are lighter, so equal masses hold more O atoms.",
   "This inverts the ratio. There are more moles of O than of S.",
   "The mole ratio is 1 : 2.000, not 1 : 3."],
  "Assume 100 g, convert each mass to moles, then divide by the smaller.",
  "S 1.561 mol : O 3.122 mol = 1 : 2.000: <b>{SO2}</b>.", 2, 1)

Q(T, "Magnetite, a magnetic iron ore, is 72.36% Fe and 27.64% O by mass. What is its empirical formula? (" + MSs('Fe', 'O') + ")",
  ["{Fe3O4}", "FeO", "{Fe2O3}", "{Fe4O3}"],
  ["Fe: 72.36 &divide; 55.85 = 1.2956 mol; O: 27.64 &divide; 15.999 = 1.7276 mol. Ratio 1 : 1.333; &times; 3 = 3 : 4.",
   "This rounds 1.33 down to 1. A ratio near 1.33 means multiply by 3.",
   "Multiplying 1 : 1.333 by 2 gives 2 : 2.67, still not whole numbers. Use 3.",
   "This inverts the ratio; there are more moles of O than of Fe."],
  "After dividing by the smaller, a value near 1.33 is a signal, not a rounding error.",
  "Fe 1.2956 : O 1.7276 = 1 : 1.333; &times; 3 = <b>{Fe3O4}</b>.", 3, 1)

Q(T, "Lactic acid, which muscle cells make (as lactate) during hard exercise, has the empirical formula {CH2O} and a molar mass of 90.08 g/mol. What is its molecular formula? (" + MSs('C', 'H', 'O') + ")",
  ["{C3H6O3}", "{CH2O}", "{C2H4O2}", "{C6H12O6}"],
  ["CH<sub>2</sub>O = 12.011 + 2(1.008) + 15.999 = 30.026 g/mol. n = 90.08 &divide; 30.026 = 3.000, so multiply every subscript by 3.",
   "This is the empirical formula. When a molar mass is given, find n.",
   "This is n = 2 (60.052 g/mol), not 90.08 g/mol.",
   "This is n = 6 (180.156 g/mol), glucose, not lactic acid."],
  "n = molar mass &divide; empirical formula mass.",
  "n = 90.08 &divide; " + G('CH2O') + " = 3.000: <b>{C3H6O3}</b>. Check: " + G('C3H6O3') + " g/mol.", 2, 1)

Q(T, "The table gives the mass percent composition of caffeine, whose molar mass is 194.19 g/mol. What is its molecular formula? (" + MSs('C', 'H', 'N', 'O') + ")",
  ["{C8H10N4O2}", "{C4H5N2O}", "{C16H20N8O4}", "{C12H15N6O3}"],
  ["Moles per 100 g: C 4.120, H 5.149, N 2.060, O 1.030. Dividing by 1.030 gives 4 : 5 : 2 : 1, so C<sub>4</sub>H<sub>5</sub>N<sub>2</sub>O (97.097 g/mol). n = 194.19 &divide; 97.097 = 2.000.",
   "This is the empirical formula. The molar mass, 194.19 g/mol, is twice its formula mass.",
   "This is n = 4 (388.39 g/mol), double the given molar mass.",
   "This is n = 3 (291.29 g/mol), not 194.19 g/mol."],
  "Find the empirical formula first, then n = 194.19 &divide; empirical formula mass.",
  "Empirical formula C<sub>4</sub>H<sub>5</sub>N<sub>2</sub>O, " + G('C4H5N2O') + " g/mol; n = 194.19 &divide; " + G('C4H5N2O') + " = 2.000: <b>{C8H10N4O2}</b>.", 3, 1,
  [{"type": "table", "cap": "Mass percent composition of caffeine", "head": ["Element", "Mass percent"],
    "rows": [["C", "49.48%"], ["H", "5.19%"], ["N", "28.85%"], ["O", "16.48%"]]}])

w = D('3.000') - D('1.465'); xw = w / mm('H2O'); xs = D('1.465') / mm('MgSO4')
Q(T, "Epsom salt is magnesium sulfate hydrate, {MgSO4}&middot;xH<sub>2</sub>O. Heating 3.000 g of it leaves 1.465 g of anhydrous {MgSO4} (" + G('MgSO4') + " g/mol). What is x? ({H2O} " + G('H2O') + " g/mol)",
  ["7", "1", "3", "14"],
  ["Water lost = 3.000 &minus; 1.465 = 1.535 g = " + num(xw, 4) + " mol; MgSO<sub>4</sub> = 1.465 &divide; 120.37 = " + num(xs, 4) + " mol. Ratio " + num(xw / xs, 3) + ", so x = 7.",
   "This compares grams of water and salt (1.535 : 1.465), not moles.",
   "This divides by the moles of hydrate as if 3.000 g were anhydrous MgSO<sub>4</sub>; use the 1.465 g that is left after heating.",
   "This treats the whole 3.000 g as water. Only the mass lost on heating is water."],
  "Water = mass lost. Convert water and salt to moles, then divide.",
  "1.535 g &divide; 18.015 g/mol = " + num(xw, 4) + " mol H<sub>2</sub>O; 1.465 g &divide; 120.37 g/mol = " + num(xs, 4) + " mol MgSO<sub>4</sub>; ratio " + num(xw / xs, 3) + ": <b>x = 7</b>, {MgSO4.7H2O}.", 2, 1)

Q(T, "A phosphorus oxide is 43.64% P and 56.36% O by mass. What is its empirical formula? (" + MSs('P', 'O') + ")",
  ["{P2O5}", "{PO2}", "{PO3}", "{P5O2}"],
  ["P: 43.64 &divide; 30.97 = 1.409 mol; O: 56.36 &divide; 15.999 = 3.523 mol. Ratio 1 : 2.500; &times; 2 = 2 : 5.",
   "This rounds 2.5 down to 2. Multiply by 2 instead.",
   "This rounds 2.5 up to 3. Multiply by 2 instead.",
   "This inverts the ratio; there are more moles of O than of P."],
  "Moles of each, divide by the smaller; then clear the .5.",
  "P 1.409 : O 3.523 = 1 : 2.500; &times; 2 = <b>{P2O5}</b>.", 3, 1)

Q(T, "Copper wire (2.538 g) is heated with sulfur until all the copper has reacted, giving 3.178 g of a copper sulfide. What is its empirical formula? (" + MSs('Cu', 'S') + ")",
  ["{Cu2S}", "{Cu4S}", "{CuS2}", "CuS"],
  ["S = 3.178 &minus; 2.538 = 0.640 g. Cu: 2.538 &divide; 63.55 = 0.03994 mol; S: 0.640 &divide; 32.06 = 0.01996 mol. Ratio 2.001 : 1.",
   "This divides grams (2.538 &divide; 0.640 = 3.97) instead of moles. Copper atoms are about twice as heavy as sulfur atoms.",
   "This inverts the ratio; there are more moles of Cu than of S.",
   "CuS would need equal moles of Cu and S; the data give twice as many moles of Cu."],
  "Find the mass of S by subtraction, then compare moles, not grams.",
  "Cu 0.03994 mol : S 0.01996 mol = 2.001 : 1: <b>{Cu2S}</b> (copper(I) sulfide).", 2, 1)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')),
      'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
