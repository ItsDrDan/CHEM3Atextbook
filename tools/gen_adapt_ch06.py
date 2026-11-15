#!/usr/bin/env python3
"""Builds bank/ch06_adapt.json (Chapter 6 ADAPT homework-only items, text only; 40 items, none repeated from bank/ch06.json).
usage: python3 tools/gen_adapt_ch06.py bank/ch06_adapt.json
Same conventions and helpers as tools/gen_bank_ch06.py (yellow-sheet electronegativities and atomic masses, dEN
cutoffs 0.4 and 2.0, VSEPR up to four groups, no octet exceptions, resonance or formal charge, addition rule for molar
masses). y[0] begins "Correct: ". Every item is rechecked by tools/check_bank_ch06.py."""
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


def Q(t, q, c, y, h, w, d, k=0):
    y = ["Correct: " + y[0]] + y[1:]
    it = {"id": "c6-h%02d" % (len(B) + 1), "t": t, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    B.append(it)

# ======================= ch06-ionic (6) =======================
T = 'ch06-ionic'
Q(T, "When potassium reacts with sulfur, which ions form?",
  ["{K^+} and {S^2-}", "K<sup>" + M + "</sup> and S<sup>2+</sup>", "K<sup>2+</sup> and S<sup>" + M + "</sup>", "{K^+} and S<sup>6" + M + "</sup>"],
  ["K (group 1) loses its 1 valence electron; S (group 16, 6 valence electrons) gains 2 to reach an octet. Two K atoms supply the two electrons: {K2S}.",
   "This reverses the transfer. The metal loses electrons and becomes the cation.",
   "Potassium has only 1 valence electron to lose, and sulfur needs 2, not 1.",
   "Sulfur <i>has</i> 6 valence electrons; it needs only 2 more for an octet."],
  "Metals lose their valence electrons; nonmetals gain enough to reach 8.",
  "K &rarr; {K^+} + e<sup>" + M + "</sup>; S + 2 e<sup>" + M + "</sup> &rarr; {S^2-}. The ions are <b>K<sup>+</sup> and S<sup>2" + M + "</sup></b>, formula {K2S}.", 1)

Q(T, "Aluminum loses 3 electrons and oxygen gains 2 when they form aluminum oxide. Which formula makes electrons lost equal electrons gained?",
  ["{Al2O3}", "{Al3O2}", "AlO", "{AlO3}"],
  ["2 Al lose 2 &times; 3 = 6 electrons; 3 O gain 3 &times; 2 = 6 electrons. Lost = gained.",
   "3 Al would lose 9 electrons, but 2 O gain only 4. The numbers are on the wrong atoms.",
   "1 Al loses 3, but 1 O gains only 2.",
   "1 Al loses 3, but 3 O would need 6."],
  "Find the least common multiple of 3 and 2.",
  "6 electrons: 2 Al &times; 3 = 3 O &times; 2. <b>{Al2O3}</b> (the ruby and sapphire mineral, and a common ceramic).", 2)

Q(T, "Which compound is a <b>salt</b>?",
  ["{MgSO4}", "{Mg(OH)2}", "MgO", "{SO2}"],
  ["Magnesium sulfate (Epsom salt) is a cation, {Mg^2+}, with an anion other than {OH^-} or {O^2-}: a salt.",
   "This contains hydroxide, so it is a base (milk of magnesia).",
   "This contains the oxide ion, so it is a metal oxide.",
   "Sulfur dioxide is made of two nonmetals; it is a molecular compound, not ionic at all."],
  "Check the anion: hydroxide means base, oxide means metal oxide, any other anion means salt.",
  "<b>{MgSO4}</b> is a salt; {Mg(OH)2} is a base; MgO is a metal oxide; {SO2} is molecular.", 1)

Q(T, "Sports drinks list sodium and potassium as electrolytes. Why does solid potassium chloride not conduct electricity, while potassium chloride dissolved in water does?",
  ["In the solid, the ions are locked in the lattice; dissolved, the ions are free to move.",
   "Solid KCl contains no ions; ions form only after it dissolves.",
   "The water itself carries the current, not the dissolved KCl.",
   "Dissolving turns KCl into KCl molecules that carry the current."],
  ["An electric current needs moving charges. Dissolving separates the {K^+} and {Cl^-} ions so they can move, which is why dissolved ions are called electrolytes.",
   "The solid is already made of {K^+} and {Cl^-} ions; they just cannot move.",
   "Pure water conducts very poorly. The dissolved ions are what carry the current.",
   "Ionic compounds never form molecules. Dissolving separates the ions."],
  "What has to be true of charged particles for a current to flow?",
  "Solid: ions fixed in the lattice, no current. Dissolved: <b>the ions are free to move</b>, so the solution conducts.", 2)

Q(T, "When fluoride from toothpaste replaces some {OH^-} ions in enamel, it forms fluorapatite, {Ca10(PO4)6F2}. What holds this mineral together?",
  ["Attractions between {Ca^2+}, {PO4^3-}, and {F^-} ions in a crystal lattice",
   "Covalent bonds between separate fluorapatite molecules",
   "Electron pairs shared equally between Ca and F atoms",
   "Attractions between neutral Ca, P, O, and F atoms"],
  ["Fluorapatite is an ionic crystal: cations and anions packed in a lattice, which is why enamel is so hard. (The P&ndash;O bonds inside each phosphate ion are covalent.)",
   "Ionic solids are lattices, not collections of molecules.",
   "Calcium is a metal and fluorine a nonmetal; calcium gives electrons to fluorine rather than sharing them.",
   "The particles carry charges: Ca<sup>2+</sup>, PO<sub>4</sub><sup>3" + M + "</sup>, and F<sup>" + M + "</sup>."],
  "Metal cations plus anions: what kind of bonding and what kind of solid?",
  "Enamel mineral is <b>an ionic lattice of Ca<sup>2+</sup>, PO<sub>4</sub><sup>3" + M + "</sup>, and F<sup>" + M + "</sup> (or OH<sup>" + M + "</sup>) ions</b>.", 2)

Q(T, "In the electron-dot picture of sodium oxide forming (2 Na&middot; + O &rarr; 2 {Na^+} + {O^2-}), how many dots does each ion show after the transfer?",
  ["{O^2-}: 8 dots; each {Na^+}: 0 dots", "{O^2-}: 6 dots; each {Na^+}: 1 dot", "{O^2-}: 8 dots; each {Na^+}: 8 dots", "{O^2-}: 7 dots; each {Na^+}: 0 dots"],
  ["O starts with 6 dots and gains 2 (one from each Na) to have 8. Each Na gives away its only valence electron, so its ion has no valence dots.",
   "These are the atoms before the transfer, not the ions.",
   "Na<sup>+</sup> has the configuration of neon, but in an electron-dot symbol it shows no valence dots, because its outer shell was emptied.",
   "Two Na atoms each give one electron, so O gains 2, not 1."],
  "Count dots before the transfer, then move them.",
  "<b>O<sup>2" + M + "</sup> has 8 dots; each Na<sup>+</sup> has 0.</b> 2 electrons lost = 2 gained, formula {Na2O}.", 2)

# ======================= ch06-lewis (7) =======================
T = 'ch06-lewis'
Q(T, "How many valence electrons are in the carbonate ion, {CO3^2-}?",
  ["24", "22", "20", "12"],
  ["4 (C) + 3 &times; 6 (O) = 22, plus 2 for the 2&minus; charge = 24.",
   "This forgets the 2&minus; charge.",
   "This subtracts 2 for the charge. A negative ion has extra electrons.",
   "This counts one O atom: 4 + 6 + 2."],
  "Group numbers, times subscripts, plus one electron per negative charge.",
  "4 + 3(6) + 2 = <b>24</b> valence electrons for {CO3^2-}.", 2)

Q(T, "How many valence electrons are in ethanol, {C2H5OH}?",
  ["20", "16", "26", "36"],
  ["2(4) + 6(1) + 6 = 20: two C, six H in all (5 + 1), one O.",
   "This counts one C atom (4 + 6 + 6). The subscript 2 means two carbons.",
   "This adds atomic numbers (2 &times; 6 + 6 &times; 1 + 8), which counts all electrons, not valence electrons.",
   "This gives every atom the number it will end up with (8 for C and O, 2 for H), not the number available."],
  "Count every atom: C<sub>2</sub>, H<sub>5</sub> plus one more H, and O.",
  "C: 2 &times; 4 = 8; H: 6 &times; 1 = 6; O: 6. Total <b>20</b>.", 2)

Q(T, "Hydrogen peroxide, {H2O2}, is a common wound antiseptic. Which describes its Lewis structure?",
  ["H&ndash;O&ndash;O&ndash;H, with two lone pairs on each O",
   "H&ndash;O=O&ndash;H, with one lone pair on each O",
   "H&ndash;O&ndash;O&ndash;H, with three lone pairs on each O",
   "O&ndash;H&ndash;H&ndash;O, with three lone pairs on each O"],
  ["14 valence electrons: 3 bonds (6) + 4 lone pairs (8). Each O has 2 bonds + 2 lone pairs = 8; each H has 2.",
   "This uses only 12 electrons. H<sub>2</sub>O<sub>2</sub> has 2(1) + 2(6) = 14, so a double bond is not needed.",
   "This uses 18 electrons, more than the 14 available.",
   "This gives each H two bonds. Hydrogen forms only one bond and is never central."],
  "Count valence electrons, build the skeleton with H on the outside, then check octets.",
  "14 electrons: <b>H&ndash;O&ndash;O&ndash;H with two lone pairs on each O</b>. Each O forms 2 bonds, as HONC predicts.", 2)

Q(T, "In a neutral molecule, a nitrogen atom forms three bonds. How many lone pairs does it have?",
  ["1", "0", "2", "3"],
  ["N has 5 valence electrons: 3 are in bonds, leaving 2, one lone pair. 3 bonds (6 electrons) + 1 lone pair (2) = 8.",
   "With no lone pair, N would have only 6 electrons.",
   "Two lone pairs plus three bonds would be 10 electrons around N.",
   "Three lone pairs go with one bond, the pattern for a halogen."],
  "Bonds + lone pairs must give N an octet.",
  "N: 3 bonds + <b>1 lone pair</b> = 8 electrons, as in NH<sub>3</sub>.", 1)

Q(T, "Carbon monoxide, CO, is the colorless gas that causes CO poisoning. Which describes its Lewis structure?",
  ["C&equiv;O, with one lone pair on each atom",
   "C=O, with two lone pairs on each atom",
   "C&ndash;O, with one lone pair on C and three on O",
   "C&equiv;O, with no lone pairs"],
  ["10 valence electrons (4 + 6): triple bond (6) + 2 lone pairs (4). C has 6 + 2 = 8, and O has 6 + 2 = 8.",
   "This uses 12 electrons; CO has only 10.",
   "This uses 10 electrons but leaves C with only 4. Move lone pairs from O into the bond.",
   "This uses only 6 electrons and leaves each atom with 6."],
  "CO has 10 valence electrons. Which picture uses 10 and gives both atoms 8?",
  "10 electrons: <b>C&equiv;O with one lone pair on each atom</b>, like N<sub>2</sub>.", 2)

Q(T, "Acetylene, {C2H2}, has 10 valence electrons. How many bonding pairs are shared between the two carbon atoms?",
  ["3", "1", "2", "4"],
  ["Two C&ndash;H bonds use 4 electrons; the other 6 must be shared between the carbons (a triple bond) so that each C has 8.",
   "With a single C&ndash;C bond, 6 electrons are left, and each C would be short of an octet.",
   "A double bond leaves 2 electrons that would have to sit on one carbon, giving the other only 6.",
   "Four shared pairs would give each C 10 electrons and use 12 in all."],
  "Place the two C&ndash;H bonds first. How many electrons are left, and how can both C atoms reach 8?",
  "H&ndash;C&equiv;C&ndash;H: <b>3 bonding pairs</b> between the carbons. 5 bonding pairs &times; 2 = 10 electrons.", 3)

Q(T, "Chloroform, {CHCl3}, was one of the first general anesthetics. In its Lewis structure (C central), how many bonding pairs and how many lone pairs are there?",
  ["4 bonding pairs, 9 lone pairs", "4 bonding pairs, 0 lone pairs", "3 bonding pairs, 9 lone pairs", "4 bonding pairs, 10 lone pairs"],
  ["26 valence electrons (4 + 1 + 21). Four bonds from C use 8; the other 18 are 9 lone pairs, 3 on each Cl.",
   "This leaves the lone pairs off the Cl atoms. Each Cl has 1 bond and 3 lone pairs.",
   "This leaves out the C&ndash;H bond; C forms 4 bonds.",
   "This uses 28 electrons, 2 more than are available (a lone pair on C would give it 10)."],
  "Count valence electrons, subtract 2 per bond, and divide the rest by 2.",
  "26 &minus; 4(2) = 18 = <b>9 lone pairs</b>, with <b>4 bonding pairs</b>. Check: 8 + 18 = 26. (Context only; chloroform is no longer used for anesthesia.)", 2)

# ======================= ch06-vsepr (7) =======================
T = 'ch06-vsepr'
Q(T, "Oxygen difluoride, {OF2}, has two O&ndash;F bonds and two lone pairs on O. What is its shape?",
  ["bent, about 109.5" + DEG, "linear, 180" + DEG, "tetrahedral, 109.5" + DEG, "bent, about 120" + DEG],
  ["2 bonds + 2 lone pairs = 4 groups (tetrahedral electron geometry); with 2 lone pairs, the 3 atoms form a bent shape, like water.",
   "This ignores the lone pairs on O. They are groups that push the F atoms together.",
   "Tetrahedral is the electron geometry; only 3 atoms are named in the shape.",
   "Bent at about 120" + DEG + " has 3 groups and 1 lone pair. O here has 4 groups."],
  "Count groups on O, including lone pairs.",
  "{OF2}: 4 groups, 2 lone pairs: <b>bent, about 109.5" + DEG + "</b>.", 2)

Q(T, "Carbon disulfide, S=C=S, is an industrial solvent. How many electron groups are on the central carbon?",
  ["2", "4", "6", "3"],
  ["Two double bonds, each one group, and no lone pairs on C: 2 groups, linear.",
   "This counts each double bond as two groups.",
   "This adds the lone pairs on the S atoms. Only groups on the central atom count.",
   "C has no lone pair, so there is no third group."],
  "Any bond, single or multiple, is one group.",
  "C: 2 double bonds = <b>2 groups</b>: linear, 180" + DEG + ", like CO<sub>2</sub>.", 1)

Q(T, "A central atom has <b>4 electron groups</b>, and <b>1</b> is a lone pair. What is the molecular shape?",
  ["trigonal pyramidal", "tetrahedral", "bent", "trigonal planar"],
  ["4 groups: tetrahedral electron geometry. With one lone pair, the central atom and its 3 neighbors form a pyramid.",
   "Tetrahedral is the electron geometry; it is the shape only with 0 lone pairs.",
   "Bent (4 groups) has 2 lone pairs.",
   "Trigonal planar has 3 groups and no lone pairs."],
  "Electron geometry from the groups; then name only the atoms.",
  "4 groups, 1 lone pair: <b>trigonal pyramidal</b>, about 109.5" + DEG + " (NH<sub>3</sub>).", 1)

Q(T, "Chloroform, {CHCl3}, has C bonded to one H and three Cl atoms, with no lone pairs on C. What is its shape?",
  ["tetrahedral", "trigonal pyramidal", "trigonal planar", "bent"],
  ["4 bonds, 0 lone pairs: tetrahedral. Different outer atoms do not change the shape (they change the polarity).",
   "Trigonal pyramidal needs a lone pair on the central atom; C has four bonds instead.",
   "Trigonal planar needs 3 groups; C has 4.",
   "Bent needs lone pairs on the central atom."],
  "Count groups on C. Do any of them belong to lone pairs?",
  "C: 4 groups, 0 lone pairs: <b>tetrahedral</b>, 109.5" + DEG + ".", 2)

Q(T, "What is the best estimate of the Cl&ndash;P&ndash;Cl bond angle in {PCl3} (three bonds and one lone pair on P)?",
  ["about 109.5" + DEG, "120" + DEG, "90" + DEG, "180" + DEG],
  ["4 groups point toward the corners of a tetrahedron, so the angle is about 109.5" + DEG + " (the lone pair squeezes it a little).",
   "120" + DEG + " is the angle for 3 groups. The lone pair is a fourth group.",
   "90" + DEG + " is what a flat drawing suggests, but the groups spread in three dimensions.",
   "180" + DEG + " is for 2 groups."],
  "Count all groups on P, including the lone pair.",
  "4 groups (trigonal pyramidal): <b>about 109.5" + DEG + "</b>.", 2)

Q(T, "In methanol, {CH3OH}, the O atom has a C&ndash;O bond, an O&ndash;H bond, and two lone pairs. What is the shape around O?",
  ["bent, about 109.5" + DEG, "linear, 180" + DEG, "trigonal pyramidal, about 109.5" + DEG, "bent, about 120" + DEG],
  ["O: 2 bonds + 2 lone pairs = 4 groups, so the C&ndash;O&ndash;H arrangement is bent, as in water.",
   "The lone pairs on O are groups; they bend the C&ndash;O&ndash;H arrangement.",
   "Trigonal pyramidal needs 3 bonds and 1 lone pair; O here has 2 bonds and 2 lone pairs.",
   "Bent at about 120" + DEG + " is the 3-group case; O here has 4 groups."],
  "In a molecule with two central atoms, find the shape around each one separately.",
  "Around O: 4 groups, 2 lone pairs: <b>bent, about 109.5" + DEG + "</b>. (Around C: tetrahedral.)", 3)

Q(T, "Which molecule is <b>linear</b>?",
  ["{CS2}", "{H2O}", "{SO2}", "{OF2}"],
  ["C has 2 groups (two C=S double bonds) and no lone pairs: linear, 180" + DEG + ".",
   "O has 2 lone pairs: 4 groups, bent.",
   "S has 3 groups (two bonds and a lone pair): bent, about 120" + DEG + ".",
   "O has 2 lone pairs: bent, about 109.5" + DEG + "."],
  "Linear (for three atoms) needs 2 groups and no lone pairs on the central atom.",
  "Only <b>{CS2}</b> has no lone pairs on the center; the other three are bent.", 2)

# ======================= ch06-polarity (7) =======================
T = 'ch06-polarity'
Q(T, "Classify the P&ndash;Cl bond in {PCl3}. (" + ENs('P', 'Cl') + ")",
  [DE + " = 0.9, polar covalent, Cl is &delta;&minus;", DE + " = 0.9, polar covalent, P is &delta;&minus;", DE + " = 5.1, ionic", DE + " = 0.9, nonpolar covalent"],
  ["3.0 &minus; 2.1 = 0.9, between 0.4 and 2.0: polar covalent. Cl is more electronegative, so it is the &delta;&minus; end.",
   "The partial negative charge goes on the more electronegative atom, which is Cl.",
   "This adds the values. " + DE + " is the difference.",
   "0.9 is above 0.4, so the bond is polar."],
  "Subtract, compare with 0.4 and 2.0, and put &delta;&minus; on the higher value.",
  DE + " = 3.0 &minus; 2.1 = <b>0.9, polar covalent, Cl &delta;&minus;</b>.", 2)

Q(T, "Potassium chloride, KCl, is used in salt substitutes. Classify the K&ndash;Cl bond. (" + ENs('K', 'Cl') + ")",
  [DE + " = 2.2, ionic", DE + " = 3.8, ionic", DE + " = 2.2, polar covalent", DE + " = &minus;2.2, polar covalent"],
  ["3.0 &minus; 0.8 = 2.2, above 2.0: ionic, matching the metal + nonmetal rule.",
   "This adds the values instead of subtracting.",
   "2.2 is above the 2.0 cutoff, so it is in the ionic range.",
   "Subtract the smaller from the larger; " + DE + " is never negative."],
  "Subtract the smaller value from the larger, then compare with 2.0.",
  DE + " = 3.0 &minus; 0.8 = <b>2.2, ionic</b>.", 1)

Q(T, "Which bond is <b>nonpolar covalent</b>? (" + ENs('H', 'C', 'N', 'O', 'Cl') + ")",
  ["C&ndash;H", "C&ndash;O", "N&ndash;H", "H&ndash;Cl"],
  [DE + " = 2.5 &minus; 2.1 = 0.4, inside the 0 to 0.4 nonpolar range.",
   DE + " = 3.5 &minus; 2.5 = 1.0: polar covalent.",
   DE + " = 3.0 &minus; 2.1 = 0.9: polar covalent.",
   DE + " = 3.0 &minus; 2.1 = 0.9: polar covalent."],
  "Find the bond with " + DE + " of 0.4 or less.",
  "<b>C&ndash;H</b> (" + DE + " 0.4) is nonpolar covalent; the others are polar covalent.", 1)

Q(T, "Chloroform, {CHCl3}, was one of the first anesthetics. Of these four chlorinated methanes, which one is <b>nonpolar</b>?",
  ["{CCl4}", "{CHCl3}", "{CH2Cl2}", "{CH3Cl}"],
  ["Four identical C&ndash;Cl bonds in a symmetrical tetrahedron: the dipoles cancel.",
   "One H and three Cl: the outer atoms differ, so the dipoles do not cancel.",
   "Two H and two Cl: not symmetrical, so polar.",
   "One Cl and three H: not symmetrical, so polar."],
  "All four are tetrahedral. Which has four identical outer atoms?",
  "SNAP: only <b>{CCl4}</b> is symmetrical, so only it is nonpolar.", 2)

Q(T, "In the C=O bond of formaldehyde, which way does the dipole arrow point? (" + ENs('C', 'O') + ")",
  ["Toward O, with the cross (+ end) at C", "Toward C, with the cross at O", "There is no dipole; C=O is nonpolar", "Toward C, because C has more bonds"],
  ["O (3.5) is more electronegative than C (2.5), so O is &delta;&minus;. The arrow points toward O; the cross marks the &delta;+ end, C.",
   "This reverses the arrow. It points toward the more electronegative atom.",
   DE + " = 1.0, so the bond is polar.",
   "The number of bonds does not decide the direction; electronegativity does."],
  "The arrowhead goes to the &delta;&minus; end.",
  "<b>Toward O</b> (&delta;&minus;), with the crossed tail at C (&delta;+); " + DE + " = 1.0.", 2)

Q(T, "{PCl3} is trigonal pyramidal, with one lone pair on P. Is it polar?",
  ["Polar: the lone pair makes it asymmetrical, so the P&ndash;Cl dipoles do not cancel.",
   "Nonpolar: three identical P&ndash;Cl bonds always cancel.",
   "Nonpolar: " + DE + " for P&ndash;Cl is 0.4 or less.",
   "Polar, because the P&ndash;Cl bonds are ionic."],
  ["The three dipoles point down and outward from the pyramid; with the lone pair on top, they do not cancel. Like NH<sub>3</sub>, PCl<sub>3</sub> is polar.",
   "Identical outer atoms cancel only in a symmetrical shape with no lone pairs on the center.",
   DE + " = 3.0 &minus; 2.1 = 0.9, so the bonds are polar.",
   DE + " = 0.9 is polar covalent, not ionic (above 2.0)."],
  "SNAP: does the central atom have a lone pair?",
  "Trigonal pyramidal with polar bonds (" + DE + " 0.9): <b>polar</b>.", 3)

Q(T, "Which list puts these elements in order of <b>increasing</b> electronegativity: Na, Mg, S, Cl?",
  ["Na &lt; Mg &lt; S &lt; Cl", "Cl &lt; S &lt; Mg &lt; Na", "Mg &lt; Na &lt; S &lt; Cl", "Na &lt; Mg &lt; Cl &lt; S"],
  ["All are in period 3, so electronegativity increases left to right: Na " + EN['Na'] + ", Mg " + EN['Mg'] + ", S " + EN['S'] + ", Cl " + EN['Cl'] + ".",
   "This is decreasing order. Electronegativity increases across a period.",
   "Mg (" + EN['Mg'] + ") is to the right of Na (" + EN['Na'] + "), so it is higher.",
   "Cl (" + EN['Cl'] + ") is to the right of S (" + EN['S'] + "), so it is higher."],
  "Same period: left is low, right is high.",
  "<b>Na " + EN['Na'] + " &lt; Mg " + EN['Mg'] + " &lt; S " + EN['S'] + " &lt; Cl " + EN['Cl'] + "</b>.", 2)

# ======================= ch06-percent (6) =======================
T = 'ch06-percent'
f = 'CO(NH2)2'; r = part(f, 'N') / mm(f)
Q(T, "Urea, {CO(NH2)2} (" + G(f) + " g/mol), is a high-nitrogen fertilizer. What is its mass percent of nitrogen? (N 14.007)",
  [P(r), P(D(MS['N']) / mm(f)), P(D(2) / D(8)), P(2 * mm('N2') / mm(f))],
  ["2(14.007) &divide; 60.056 &times; 100% = 46.65%, matching urea's 46-0-0 fertilizer grade.",
   "This counts one N. The 2 outside (NH<sub>2</sub>) gives two N atoms.",
   "This is the fraction of the <i>atoms</i> that are N (2 of 8). Mass percent uses masses.",
   "This uses 28.014 (the mass of N<sub>2</sub>) for each N atom. Atoms in a compound use 14.007."],
  "Subscript &times; atomic mass &divide; molar mass &times; 100%.",
  "%N = 2(14.007) &divide; " + G(f) + " &times; 100% = <b>" + P(r) + "</b>.", 2, 1)

f = 'CaCl2'; r = part(f, 'Cl') / mm(f)
Q(T, "Calcium chloride, {CaCl2} (" + G(f) + " g/mol), is used in IV solutions and as a dust-control salt on dirt roads. What is its mass percent of chlorine? (Cl 35.45)",
  [P(r), P(D(MS['Cl']) / mm(f)), P(part(f, 'Ca') / mm(f)), P(part(f, 'Cl') / D(MS['Ca']))],
  ["2(35.45) &divide; 110.98 &times; 100% = 63.89%.",
   "This counts one Cl; the formula has two.",
   "This is the percent of calcium.",
   "This divides by the mass of Ca. Divide by the whole compound."],
  "Two Cl atoms, divided by the molar mass of CaCl<sub>2</sub>.",
  "%Cl = 70.90 &divide; " + G(f) + " &times; 100% = <b>" + P(r) + "</b>.", 1, 1)

f = 'CH4'; r = part(f, 'C') / mm(f)
Q(T, "Dairy digesters in the Valley capture methane, {CH4} (" + G(f) + " g/mol), from manure. What is the mass percent of carbon in methane? (C 12.011)",
  [P(r), P(D(1) / D(5)), P(part(f, 'H') / mm(f)), P(mm(f) / D(MS['C']))],
  ["12.011 &divide; 16.043 &times; 100% = 74.87%. Carbon is 1 atom in 5 but most of the mass.",
   "This is the fraction of atoms that are carbon (1 of 5). Mass percent uses masses.",
   "This is the percent of hydrogen, 4(1.008) &divide; 16.043.",
   "This divides the wrong way; a part cannot be more than 100%."],
  "Mass of C in one mole &divide; molar mass.",
  "%C = 12.011 &divide; " + G(f) + " &times; 100% = <b>" + P(r) + "</b>.", 1, 1)

o = D('3.014') - D('2.374')
Q(T, "A student heats 2.374 g of tin in air until it has fully reacted, giving 3.014 g of a tin oxide. What is the mass percent of tin in the oxide?",
  [P(D('2.374') / D('3.014'), 4), P(o / D('3.014'), 3), P(D('2.374') / o, 3), P(D('2.374') / (D('3.014') + D('2.374')), 4)],
  ["2.374 &divide; 3.014 &times; 100% = 78.77%, which matches SnO<sub>2</sub>.",
   "This is the percent of oxygen (0.640 g &divide; 3.014 g).",
   "This divides tin by oxygen. Divide by the whole oxide.",
   "This adds the tin mass to the oxide mass; the oxide already includes the tin."],
  "Part (tin) &divide; whole (oxide).",
  "%Sn = 2.374 &divide; 3.014 &times; 100% = <b>" + P(D('2.374') / D('3.014'), 4) + "</b>.", 2, 1)

f = 'Ca(H2PO4)2'; r = part(f, 'P') / mm(f)
Q(T, "Calcium dihydrogen phosphate, {Ca(H2PO4)2} (" + G(f) + " g/mol), is a phosphorus fertilizer. What is its mass percent of phosphorus? (P 30.97)",
  [P(r), P(D(MS['P']) / mm(f)), P(part(f, 'Ca') / mm(f)), P(D(MS['P']) / mm('CaH2PO4'))],
  ["2(30.97) &divide; 234.04 &times; 100% = 26.47%. The 2 outside the parentheses gives two P atoms.",
   "This counts one P atom.",
   "This is the percent of calcium.",
   "This ignores the 2 outside the parentheses in both the P count and the molar mass."],
  "How many P atoms are in Ca(H<sub>2</sub>PO<sub>4</sub>)<sub>2</sub>?",
  "%P = 2(30.97) &divide; " + G(f) + " &times; 100% = <b>" + P(r) + "</b>.", 2, 1)

f = 'C6H5NO2'; r = part(f, 'N') / mm(f)
Q(T, "Niacin (vitamin B<sub>3</sub>), {C6H5NO2} (" + G(f) + " g/mol), is sold as a supplement. What is its mass percent of nitrogen? (N 14.007)",
  [P(r), P(D(1) / D(14)), P(part(f, 'C') / mm(f)), P(mm(f) / D(MS['N']))],
  ["14.007 &divide; 123.111 &times; 100% = 11.38%.",
   "This is the fraction of atoms that are N (1 of 14). Mass percent uses masses.",
   "This is the percent of carbon.",
   "This divides the wrong way."],
  "Mass of N in one mole &divide; molar mass &times; 100%.",
  "%N = 14.007 &divide; " + G(f) + " &times; 100% = <b>" + P(r) + "</b>.", 2, 1)

# ======================= ch06-empirical (7) =======================
T = 'ch06-empirical'
Q(T, "Ethylene glycol, {C2H6O2}, is the main ingredient in antifreeze. What is its empirical formula?",
  ["{CH3O}", "{C2H6O2}", "{CH3O2}", "{C4H12O4}"],
  ["All three subscripts divide by 2: C<sub>1</sub>H<sub>3</sub>O<sub>1</sub>.",
   "2, 6, and 2 share a factor of 2, so this is not the simplest ratio.",
   "This divides C and H by 2 but not O. Every subscript is divided by the same number.",
   "This multiplies by 2; the empirical formula is the smallest ratio."],
  "Divide every subscript by their largest common factor.",
  "C<sub>2</sub>H<sub>6</sub>O<sub>2</sub> &divide; 2 = <b>{CH3O}</b>.", 1)

Q(T, "Hydrogen peroxide is 5.93% H and 94.07% O by mass, and its molar mass is 34.01 g/mol. What is its molecular formula? (" + MSs('H', 'O') + ")",
  ["{H2O2}", "HO", "{H2O}", "{H4O4}"],
  ["H: 5.93 &divide; 1.008 = 5.883 mol; O: 94.07 &divide; 15.999 = 5.880 mol. Ratio 1 : 1, so HO (17.007 g/mol); n = 34.01 &divide; 17.007 = 2.000.",
   "This is the empirical formula. The molar mass shows that each molecule holds two HO units.",
   "Water is 1 : 2 O : H (11.19% H); these data give a 1 : 1 mole ratio.",
   "This is n = 4 (68.03 g/mol), twice the given molar mass."],
  "Empirical formula from moles first; then n = molar mass &divide; empirical formula mass.",
  "Empirical HO, " + G('HO') + " g/mol; n = 34.01 &divide; " + G('HO') + " = 2.000: <b>{H2O2}</b>.", 2, 1)

Q(T, "Propane, the fuel in many farm and barbecue tanks, is 81.71% C and 18.29% H by mass. What is its empirical formula? (" + MSs('C', 'H') + ")",
  ["{C3H8}", "{CH3}", "{C2H5}", "{C8H3}"],
  ["C: 81.71 &divide; 12.011 = 6.803 mol; H: 18.29 &divide; 1.008 = 18.15 mol. Ratio 1 : 2.667; &times; 3 = 3 : 8.",
   "This rounds 2.67 up to 3. A value near 2.67 (2 and 2/3) means multiply by 3.",
   "Multiplying by 2 gives 2 : 5.33, still not whole numbers; it was rounded to 5.",
   "This inverts the ratio; there are more moles of H than of C."],
  "After dividing by the smaller, a decimal near .67 or .33 means multiply by 3.",
  "C 6.803 : H 18.15 = 1 : 2.667; &times; 3 = <b>{C3H8}</b>.", 3, 1)

w = D('3.150') - D('2.491'); xw = w / mm('H2O'); xs = D('2.491') / mm('CaSO4')
Q(T, "Gypsum, the raw material for dental stone, is calcium sulfate hydrate, {CaSO4}&middot;xH<sub>2</sub>O. Heating 3.150 g of gypsum leaves 2.491 g of anhydrous {CaSO4} (" + G('CaSO4') + " g/mol). What is x? ({H2O} " + G('H2O') + " g/mol)",
  ["2", "1", "4", "5"],
  ["Water lost = 3.150 &minus; 2.491 = 0.659 g = " + num(xw, 4) + " mol; CaSO<sub>4</sub> = 2.491 &divide; 136.14 = " + num(xs, 4) + " mol. Ratio " + num(xw / xs, 3) + ".",
   "With x = 1, the 3.150 g sample would lose only about 0.37 g of water.",
   "This doubles the ratio, as if counting H atoms instead of water molecules.",
   "x = 5 is copper(II) sulfate pentahydrate; the gypsum data give a ratio near 2."],
  "Water lost &rarr; moles; anhydrous salt &rarr; moles; divide.",
  num(xw, 4) + " mol H<sub>2</sub>O &divide; " + num(xs, 4) + " mol CaSO<sub>4</sub> = " + num(xw / xs, 3) + ": <b>x = 2</b>, {CaSO4.2H2O}.", 2, 1)

Q(T, "Ibuprofen's empirical formula is {C13H18O2}, and its molar mass is 206.29 g/mol. What is its molecular formula? (" + MSs('C', 'H', 'O') + ")",
  ["{C13H18O2}", "{C26H36O4}", "{C39H54O6}", "{C13H18O}"],
  ["The empirical formula mass is 13(12.011) + 18(1.008) + 2(15.999) = 206.285 g/mol, so n = 206.29 &divide; 206.285 = 1.000. The molecular formula is the empirical formula.",
   "This assumes n = 2 (412.57 g/mol). n can be 1.",
   "This is n = 3, three times the molar mass.",
   "This drops an O atom; the molecular formula is a whole-number multiple of the empirical formula."],
  "Compute n before multiplying anything.",
  "n = 206.29 &divide; " + G('C13H18O2') + " = 1.000: <b>{C13H18O2}</b>. Many molecules, such as H<sub>2</sub>O and CO<sub>2</sub>, have n = 1.", 2, 1)

Q(T, "Zinc oxide is the white mineral in many sunscreens and diaper creams. Heating 1.635 g of zinc in air gives 2.035 g of zinc oxide. What is its empirical formula? (" + MSs('Zn', 'O') + ")",
  ["ZnO", "{Zn4O}", "{ZnO2}", "{Zn2O}"],
  ["O = 2.035 &minus; 1.635 = 0.400 g. Zn: 1.635 &divide; 65.39 = 0.02500 mol; O: 0.400 &divide; 15.999 = 0.02500 mol. Ratio 1 : 1.",
   "This divides grams (1.635 &divide; 0.400 = 4.09) instead of moles. Zinc atoms are about four times heavier than O atoms.",
   "This would need twice as many moles of O as of Zn.",
   "This would need twice as many moles of Zn as of O."],
  "Oxygen by subtraction, then compare moles.",
  "Zn 0.02500 mol : O 0.02500 mol = 1 : 1: <b>ZnO</b>, as {Zn^2+} and {O^2-} predict.", 2, 1)

Q(T, "Aspirin is 60.00% C, 4.48% H, and 35.52% O by mass. What is its empirical formula? (" + MSs('C', 'H', 'O') + ")",
  ["{C9H8O4}", "{C2H2O}", "{C5H4O2}", "{C18H16O8}"],
  ["Moles per 100 g: C 4.995, H 4.444, O 2.220. Dividing by 2.220: C 2.250, H 2.002, O 1. A ratio of 2.25 means multiply by 4: C 9, H 8, O 4.",
   "This rounds 2.25 down to 2. Values near .25 mean multiply by 4.",
   "Multiplying by 2 gives 4.5 : 4 : 2, still not whole; 4.5 was rounded to 5.",
   "This doubles a ratio that is already whole. The empirical formula is the smallest whole-number ratio."],
  "Divide by the smallest mole value; what multiplier turns 2.25 into a whole number?",
  "C 2.250 : H 2.002 : O 1; &times; 4 = <b>{C9H8O4}</b> (" + G('C9H8O4') + " g/mol; aspirin's molecular formula is also C<sub>9</sub>H<sub>8</sub>O<sub>4</sub>, so n = 1).", 3, 1)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
