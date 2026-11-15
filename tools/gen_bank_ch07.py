#!/usr/bin/env python3
"""Builds bank/ch07.json (Chapter 7 Try It items: chemical equations and balancing, reaction patterns, electrolytes
and solubility, precipitation and net ionic equations, acid-base and gas-evolution reactions, oxidation-reduction,
activity series). Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch07.py bank/ch07.json
Conventions (Sections 7.1-7.8): solubility rules = the green-sheet table in Section 7.4 (no questions on the
"slightly soluble" Ca/Sr/Ba hydroxides or the Li+ notes); strong acids HCl, HBr, HI, HNO3, HClO4, H2SO4; unstable
products H2CO3 -> CO2 + H2O, H2SO3 -> SO2 + H2O, NH4OH -> NH3 + H2O, H2S is a gas; activity series exactly
Li K Ca Na Mg Al Zn Fe Ni Sn Pb H2 Cu Ag Au (Fe as Fe2+); oxidation numbers by the ordered rules of Section 7.7;
no redox balancing with H2O, H+ or OH-.
Markup: {formula} for a formula or ion ({Ca3(PO4)2}, {SO4^2-}); [[equation]] for a whole equation, species
separated by " + ", arrow "->", phases (s) (l) (g) (aq), electrons e^-. Every item is rechecked by
tools/check_bank_ch07.py."""
import json, sys, re, collections
OUT = sys.argv[1]
M = '&minus;'
B = []

# ---------------- formulas and equations ----------------
def F(s):
    ch = ''
    if '^' in s: s, ch = s.split('^')
    out = re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', s)
    if ch: out += '<sup>' + ch.replace('-', M) + '</sup>'
    return out
SP = re.compile(r'^(.*?)(\((?:s|l|g|aq)\))?$')
def EQ(s):
    out = []
    for tok in s.split():
        if tok == '->': out.append('&rarr;')
        elif tok == '+': out.append('+')
        elif re.fullmatch(r'\d+(\.\d+)?', tok): out.append(tok)
        else:
            m = SP.match(tok); out.append(F(m.group(1)) + (m.group(2) or ''))
    return ' '.join(out)
def X(s):
    s = re.sub(r'\[\[(.+?)\]\]', lambda m: EQ(m.group(1)), s)
    return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)
AS = 'Activity series (most active first): '
def series(*m): return AS + ', '.join('{H2}' if x == 'H2' else x for x in m) + '.'

def Q(t, q, c, y, h, w, d, k=0, f=None):
    it = {"id": "c7-%03d" % (len(B) + 1), "t": t, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    if f:
        for fg in f:
            if fg['type'] == 'table':
                fg['head'] = [X(x) for x in fg['head']]; fg['rows'] = [[X(x) for x in r] for r in fg['rows']]
                if 'cap' in fg: fg['cap'] = X(fg['cap'])
        it["f"] = f
    B.append(it)

# ======================= ch07-equations (12) =======================
T = 'ch07-equations'
Q(T, "Which observation is the best evidence that a chemical reaction has occurred?",
  ["Two clear, colorless solutions are mixed, and a cloudy yellow solid forms.",
   "A pot of water on the stove forms bubbles as it heats.",
   "A spoonful of sugar disappears when it is stirred into hot tea.",
   "An ice cube melts into a puddle on the counter."],
  ["A solid forming from two clear solutions (a precipitate) means a new, insoluble substance was made.",
   "Bubbles in boiling water are water vapor, the same substance in a new state: a physical change.",
   "Dissolving is a physical change; the sugar molecules are still sugar, now spread through the water.",
   "Melting changes only the state of water, not its identity."],
  "Ask: did a new substance form, or did the same substance just change form?",
  "A new solid appearing from clear solutions is a <b>precipitate</b>, one of the four signs of reaction (gas, precipitate, color change, energy change).", 1)

Q(T, "Each of these fizzes. Which one is a <b>physical</b> change, not a chemical reaction?",
  ["A bottle of soda is opened, and dissolved carbon dioxide escapes as bubbles.",
   "An antacid tablet containing calcium carbonate is dropped into hydrochloric acid.",
   "Hydrogen peroxide is poured on a cut, where the enzyme catalase breaks it into water and oxygen gas.",
   "Baking soda is stirred into vinegar."],
  ["The CO<sub>2</sub> was already in the soda, dissolved under pressure. It leaves the liquid unchanged: no new substance forms.",
   "Calcium carbonate reacts with the acid to make new substances, including CO<sub>2</sub> gas.",
   "Catalase speeds up the decomposition of {H2O2} into new substances, {H2O} and {O2}: a chemical change.",
   "Baking soda and acetic acid react to make sodium acetate, water, and new CO<sub>2</sub> gas."],
  "Bubbles are a clue, not proof. Was the gas already there, or was it made?",
  "Opening a soda only releases gas that was <b>already dissolved</b>; the other three make new substances, including a new gas.", 1)

Q(T, "Barium chloride solution is mixed with magnesium sulfate (Epsom salt) solution: [[BaCl2(aq) + MgSO4(aq) -> BaSO4(s) + MgCl2(aq)]]. What does the label (s) after {BaSO4} tell you?",
  ["{BaSO4} forms as a solid, a precipitate.",
   "{BaSO4} stays dissolved in the water.",
   "{BaSO4} is formed as a gas.",
   "Only a single unit of {BaSO4} forms."],
  ["(s) means solid. Barium sulfate is insoluble, so it settles out of the solution.",
   "Dissolved substances are labeled (aq), as {MgCl2}(aq) is here.",
   "Gases are labeled (g).",
   "Numbers of units are shown by coefficients in front of formulas, not by phase labels."],
  "The four phase labels are (s), (l), (g), and (aq).",
  "(s) = solid, (l) = liquid, (g) = gas, (aq) = dissolved in water. <b>{BaSO4}(s) is a solid precipitate</b>; {MgCl2}(aq) stays dissolved.", 1)

Q(T, "How many oxygen atoms are represented by 2 {Al2(SO4)3}?",
  ["24", "12", "8", "9"],
  ["Each {Al2(SO4)3} has 3 sulfate groups with 4 O each: 12 O. The coefficient 2 doubles it: 24.",
   "12 is the oxygen count in one formula unit. The coefficient 2 multiplies the whole formula.",
   "This ignores the subscript 3 outside the parentheses: 2 &times; 4 = 8.",
   "This adds the numbers (4 + 3 + 2) instead of multiplying."],
  "Multiply: coefficient &times; subscript outside the parentheses &times; subscript inside.",
  "2 &times; 3 &times; 4 = <b>24</b> O atoms.", 2)

Q(T, "In a sealed flask, 2.43 g of magnesium reacts completely with 1.60 g of oxygen gas: [[2 Mg(s) + O2(g) -> 2 MgO(s)]]. What mass of magnesium oxide forms?",
  ["4.03 g", "0.83 g", "2.43 g", "8.06 g"],
  ["Conservation of mass: mass of products = mass of reactants = 2.43 g + 1.60 g = 4.03 g.",
   "This subtracts the masses. Both reactants end up in the product, so their masses add.",
   "This counts only the magnesium. The oxygen atoms are now part of the MgO too.",
   "This doubles the answer because of the coefficient 2. Coefficients count particles; the total mass is still just the reactant masses added."],
  "Atoms are only rearranged, so total mass in = total mass out.",
  "2.43 g + 1.60 g = <b>4.03 g</b> MgO.", 1, 1)

Q(T, "A student heats baking soda, {NaHCO3}, in an open crucible: [[2 NaHCO3(s) -> Na2CO3(s) + H2O(g) + CO2(g)]]. Using the data in the table, what total mass of water vapor and carbon dioxide escaped?",
  ["3.10 g", "60.14 g", "28.52 g", "0 g, because mass is conserved"],
  ["The solid lost 31.62 g &minus; 28.52 g = 3.10 g. That mass left as {H2O}(g) and {CO2}(g).",
   "This adds the two readings. The gases leaving are the difference between them.",
   "28.52 g is what is left in the crucible, not what escaped.",
   "Mass is conserved overall, but the gases left the open crucible, so the crucible's mass drops."],
  "The mass lost by the open crucible is the mass of the gases that escaped.",
  "Gases escaped = 31.62 g &minus; 28.52 g = <b>3.10 g</b>. In a sealed container the total mass would not change.", 2, 1,
  [{"type": "table", "cap": "Heating baking soda", "head": ["Measurement", "Mass (g)"],
    "rows": [["Crucible + baking soda, before", "31.62"], ["Crucible + solid, after", "28.52"]]}])

Q(T, "Sulfur dioxide from burning sulfur-containing fuel reacts with oxygen in the air to form sulfur trioxide, a step toward acid rain. Which is the correctly balanced equation?",
  ["[[2 SO2(g) + O2(g) -> 2 SO3(g)]]",
   "[[SO2(g) + O2(g) -> SO4(g)]]",
   "[[4 SO2(g) + 2 O2(g) -> 4 SO3(g)]]",
   "[[SO2(g) + O2(g) -> 2 SO3(g)]]"],
  ["S: 2 = 2; O: 4 + 2 = 6 = 2 &times; 3; and 2, 1, 2 share no factor.",
   "This changes a subscript so the atoms match. {SO4} is not sulfur trioxide; only coefficients may change.",
   "The atoms balance, but every coefficient shares a factor of 2. Divide to get the lowest whole numbers.",
   "S does not balance: 1 on the left, 2 on the right."],
  "Keep the formula {SO3}. Balance S first, then O.",
  "O: 2 + 2 = 4 on the left vs 3 on the right; 2 {SO3} needs 2 {SO2} and one {O2}. <b>[[2 SO2(g) + O2(g) -> 2 SO3(g)]]</b>", 2)

Q(T, "Balance the equation: [[Al2(SO4)3(aq) + KOH(aq) -> Al(OH)3(s) + K2SO4(aq)]]. What are the coefficients, in order?",
  ["1, 6, 2, 3", "2, 12, 4, 6", "1, 3, 2, 3", "1, 6, 1, 3"],
  ["Treat {SO4^2-} and {OH^-} as units. Al: 2 {Al(OH)3}; OH: 2 &times; 3 = 6 KOH; SO<sub>4</sub>: 3 {K2SO4}; K: 6 = 6.",
   "Everything balances, but all four coefficients share a factor of 2.",
   "Al and sulfate balance, but OH does not: 3 on the left, 6 on the right (and K: 3 vs 6).",
   "Aluminum does not balance: 2 Al on the left, 1 on the right."],
  "Balance Al first, then the polyatomic units OH and {SO4}, then check K.",
  "<b>1, 6, 2, 3</b>: [[Al2(SO4)3(aq) + 6 KOH(aq) -> 2 Al(OH)3(s) + 3 K2SO4(aq)]]. Al 2 = 2; SO<sub>4</sub> 3 = 3; K 6 = 6; OH 6 = 6.", 2)

Q(T, "Lighter fluid is butane, {C4H10}. In the balanced equation for its complete combustion, [[C4H10(g) + O2(g) -> CO2(g) + H2O(g)]], what is the lowest whole-number coefficient of {O2}?",
  ["13", "6.5", "26", "9"],
  ["C: 4 {CO2}; H: 5 {H2O}; O on the right = 4(2) + 5 = 13, so 13/2 {O2}. Double everything: 2, 13, 8, 10.",
   "13/2 balances the atoms, but coefficients must be whole numbers. Double all of them.",
   "26 comes from doubling twice; 2, 13, 8, 10 already has no common factor.",
   "This counts 1 O in each {CO2} instead of 2: 4 + 5 = 9."],
  "Balance C, then H, then O. If O comes out odd, double everything.",
  "[[2 C4H10(g) + 13 O2(g) -> 8 CO2(g) + 10 H2O(g)]]: O 26 = 16 + 10. The coefficient of {O2} is <b>13</b>.", 3)

Q(T, "A student balances [[H2(g) + Cl2(g) -> HCl(g)]] by changing it to [[H2(g) + Cl2(g) -> H2Cl2(g)]]. What is wrong?",
  ["Changing a subscript makes a different substance; a coefficient of 2 in front of HCl is the fix.",
   "Nothing is wrong, because the atoms now balance.",
   "The reactants should be written as single atoms, H and Cl, so that HCl balances.",
   "The fix should be a coefficient of 2 in front of {H2} instead."],
  ["Subscripts define the substance (HCl is hydrogen chloride). Only coefficients change: H<sub>2</sub> + Cl<sub>2</sub> &rarr; 2 HCl.",
   "Atoms balance, but {H2Cl2} is not the product. Balancing must keep the correct formulas.",
   "Hydrogen and chlorine are diatomic elements, {H2} and {Cl2}; writing H or Cl changes the substances.",
   "A 2 in front of {H2} gives 4 H on the left and still only 1 on the right."],
  "What are you allowed to change when balancing: subscripts or coefficients?",
  "Never change subscripts. <b>[[H2(g) + Cl2(g) -> 2 HCl(g)]]</b>: H 2 = 2, Cl 2 = 2.", 2)

Q(T, "Aluminum metal burns in chlorine gas to form solid aluminum chloride. Which balanced equation uses the lowest whole-number coefficients?",
  ["[[2 Al(s) + 3 Cl2(g) -> 2 AlCl3(s)]]",
   "[[4 Al(s) + 6 Cl2(g) -> 4 AlCl3(s)]]",
   "[[Al(s) + 1.5 Cl2(g) -> AlCl3(s)]]",
   "[[Al(s) + Cl3(g) -> AlCl3(s)]]"],
  ["Al: 2 = 2; Cl: 6 = 6; and 2, 3, 2 share no factor.",
   "Balanced, but 4, 6, 4 share a factor of 2.",
   "Balanced, but 1.5 is not a whole number. Doubling gives 2, 3, 2.",
   "Chlorine gas is {Cl2}; Cl<sub>3</sub> does not exist. Formulas cannot be changed to balance."],
  "Write {Cl2} for chlorine gas and {AlCl3} from the charges {Al^3+} and {Cl^-}.",
  "Al + {Cl2} &rarr; {AlCl3}: Cl needs a common multiple of 2 and 3, so 3 {Cl2} and 2 {AlCl3}, then 2 Al. <b>[[2 Al(s) + 3 Cl2(g) -> 2 AlCl3(s)]]</b>", 2)

Q(T, "In a blast furnace, solid iron(III) oxide reacts with carbon monoxide gas to form solid iron and carbon dioxide gas. Which equation is correct, balanced, and labeled?",
  ["[[Fe2O3(s) + 3 CO(g) -> 2 Fe(s) + 3 CO2(g)]]",
   "[[Fe2O3(s) + CO(g) -> 2 Fe(s) + CO2(g)]]",
   "[[Fe2O3(s) + 3 CO(g) -> 2 Fe(s) + 3 CO2(aq)]]",
   "[[FeO3(s) + 3 CO(g) -> Fe(s) + 3 CO2(g)]]"],
  ["Fe 2 = 2; C 3 = 3; O 3 + 3 = 6 = 3 &times; 2. All phases match the description.",
   "Iron balances, but O does not: 4 on the left, 2 on the right.",
   "Carbon dioxide is described as a gas, so its label is (g), not (aq).",
   "Iron(III) oxide is {Fe2O3} (from {Fe^3+} and {O^2-}); the formula cannot be changed."],
  "Names first (iron(III) oxide = {Fe2O3}), then balance Fe, C, and O, then add labels.",
  "<b>[[Fe2O3(s) + 3 CO(g) -> 2 Fe(s) + 3 CO2(g)]]</b>. Check: Fe 2 = 2, C 3 = 3, O 6 = 6.", 3)

# ======================= ch07-types (10) =======================
T = 'ch07-types'
Q(T, "Heating mercury(II) oxide releases oxygen gas: [[2 HgO(s) -> 2 Hg(l) + O2(g)]]. What type of reaction is this?",
  ["Decomposition", "Combination", "Single displacement", "Combustion"],
  ["One compound breaks into simpler substances (AB &rarr; A + B), here with heat.",
   "Combination builds one product from two or more reactants; this goes the other way.",
   "Single displacement needs an element and a compound as reactants. Here there is only one reactant.",
   "Combustion needs a fuel reacting with {O2}. Here {O2} is a product."],
  "Count the reactants: one compound alone (often heated) points to one pattern.",
  "One reactant, two products: <b>decomposition</b>, AB &rarr; A + B.", 1)

Q(T, "Nickel wire is placed in silver nitrate solution: [[Ni(s) + 2 AgNO3(aq) -> Ni(NO3)2(aq) + 2 Ag(s)]]. What type of reaction is this?",
  ["Single displacement", "Double displacement", "Combination", "Decomposition"],
  ["An element (Ni) replaces the metal ion in a compound (A + BC &rarr; AC + B), releasing Ag metal.",
   "Double displacement needs two compounds swapping partners. Here one reactant is an element.",
   "There are two products, not one.",
   "There are two reactants, and nothing breaks down into simpler substances."],
  "Look at the reactant side: an element plus a compound.",
  "Element + compound &rarr; new compound + new element: <b>single displacement</b>.", 1)

Q(T, "What type of reaction is [[AgNO3(aq) + KBr(aq) -> AgBr(s) + KNO3(aq)]]?",
  ["Double displacement", "Single displacement", "Combination", "Decomposition"],
  ["Two ionic compounds swap partners (AB + CD &rarr; AD + CB); {Ag^+} pairs with {Br^-} as a precipitate.",
   "Single displacement needs a free element as a reactant. Both reactants here are compounds.",
   "Combination makes one product; this makes two.",
   "Decomposition starts with one reactant; this has two."],
  "Two compounds on the left, two on the right, partners exchanged.",
  "The cations trade anions: <b>double displacement</b> (a precipitation, since AgBr is insoluble).", 1)

Q(T, "Which reaction is a <b>combination</b> reaction?",
  ["[[2 Ca(s) + O2(g) -> 2 CaO(s)]]",
   "[[2 C2H2(g) + 5 O2(g) -> 4 CO2(g) + 2 H2O(g)]]",
   "[[2 NaN3(s) -> 2 Na(s) + 3 N2(g)]]",
   "[[Mg(s) + 2 AgNO3(aq) -> Mg(NO3)2(aq) + 2 Ag(s)]]"],
  ["Two reactants make one product (A + B &rarr; AB). It uses {O2}, but calcium is a metal, not a carbon fuel.",
   "A carbon fuel reacting with {O2} to give {CO2} and {H2O} is combustion (a welding torch).",
   "One reactant breaking into two products is decomposition (the reaction that inflates an air bag).",
   "An element replacing a metal ion in a compound is single displacement."],
  "Look for exactly one product.",
  "Only <b>2 Ca + {O2} &rarr; 2 CaO</b> makes a single product from two reactants.", 2)

Q(T, "Calcium metal heated in nitrogen gas forms calcium nitride. Which equation correctly predicts and balances the product?",
  ["[[3 Ca(s) + N2(g) -> Ca3N2(s)]]",
   "[[Ca(s) + N2(g) -> CaN2(s)]]",
   "[[3 Ca(s) + 2 N2(g) -> Ca3N2(s)]]",
   "[[6 Ca(s) + 2 N2(g) -> 2 Ca3N2(s)]]"],
  ["{Ca^2+} and {N^3-} combine 3 : 2 for zero charge: 3(+2) + 2(&minus;3) = 0. Ca 3 = 3; N 2 = 2.",
   "This copies the subscript from {N2} into the product. Write the product from the ion charges, {Ca^2+} and {N^3-}.",
   "The formula is right, but N does not balance: 4 on the left, 2 on the right.",
   "Balanced, but every coefficient shares a factor of 2."],
  "Predict the formula from charges first (nitride is {N^3-}), then balance.",
  "{Ca^2+} + {N^3-} &rarr; {Ca3N2}; <b>[[3 Ca(s) + N2(g) -> Ca3N2(s)]]</b>.", 2)

Q(T, "Strontium carbonate is heated strongly, the way limestone is heated to make lime. Which equation shows the decomposition?",
  ["[[SrCO3(s) -> SrO(s) + CO2(g)]]",
   "[[SrCO3(s) -> Sr(s) + CO3(g)]]",
   "[[2 SrCO3(s) -> 2 Sr(s) + 2 CO2(g) + O2(g)]]",
   "[[SrCO3(s) -> SrC(s) + O3(g)]]"],
  ["Heating a metal carbonate gives the metal oxide and carbon dioxide, like {CaCO3} &rarr; CaO + {CO2}.",
   "{CO3} is the carbonate ion, not a gas molecule; it cannot leave on its own.",
   "Balanced, but metal carbonates do not decompose to the free metal and {O2}. They give the oxide and {CO2}.",
   "This splits the formula into made-up pieces. The products are the oxide and {CO2}."],
  "Metal carbonate + heat &rarr; metal oxide + ?",
  "<b>[[SrCO3(s) -> SrO(s) + CO2(g)]]</b>. Sr 1 = 1; C 1 = 1; O 3 = 1 + 2.", 2)

Q(T, "Aluminum sulfate solution (used to clarify drinking water) is mixed with barium nitrate solution. Which gives the correct formulas of the two products?",
  ["{Al(NO3)3} and {BaSO4}",
   "{Al2(NO3)3} and {Ba(SO4)3}",
   "{Al(NO3)2} and {BaSO4}",
   "{AlNO3} and {BaSO4}"],
  ["Swap partners, then use charges: {Al^3+} + {NO3^-} &rarr; {Al(NO3)3}; {Ba^2+} + {SO4^2-} &rarr; {BaSO4}.",
   "These subscripts were copied from the reactants. Rebuild each formula from its ion charges.",
   "Al(NO<sub>3</sub>)<sub>2</sub> would have a 1+ charge left over: aluminum is {Al^3+}, so it needs three nitrates.",
   "A 1 : 1 ratio leaves {Al^3+} with only one nitrate, a net 2+ charge."],
  "Keep each cation, give it the other anion, and make the charges sum to zero.",
  "<b>{Al(NO3)3} and {BaSO4}</b>: [[Al2(SO4)3(aq) + 3 Ba(NO3)2(aq) -> 2 Al(NO3)3(aq) + 3 BaSO4(s)]].", 2)

Q(T, "A propane space heater run in a closed garage gets too little oxygen and makes carbon monoxide, a poison that binds hemoglobin. Which balanced equation shows this <b>incomplete</b> combustion of propane, {C3H8}?",
  ["[[2 C3H8(g) + 7 O2(g) -> 6 CO(g) + 8 H2O(g)]]",
   "[[C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(g)]]",
   "[[C3H8(g) + 2 O2(g) -> 3 CO(g) + 4 H2O(g)]]",
   "[[2 C3H8(g) + 7 O2(g) -> 6 CO2(g) + 8 H2O(g)]]"],
  ["C 6 = 6; H 16 = 16; O 14 = 6 + 8. Carbon ends up as CO because oxygen is limited.",
   "This is complete combustion (enough {O2}): the carbon becomes {CO2}, not CO.",
   "The products are right, but O does not balance: 4 on the left, 3 + 4 = 7 on the right.",
   "This keeps the coefficients for CO but writes {CO2}: O is 14 on the left and 20 on the right."],
  "Incomplete combustion gives CO. Balance C, then H, then O, and clear any fraction.",
  "C<sub>3</sub>H<sub>8</sub> &rarr; 3 CO + 4 {H2O} needs 7 O = 3.5 {O2}; double: <b>[[2 C3H8(g) + 7 O2(g) -> 6 CO(g) + 8 H2O(g)]]</b>.", 3)

Q(T, "Rubbing alcohol (isopropyl alcohol, {C3H8O}) is flammable, which is why it is kept away from oxygen equipment in hospitals. In the balanced equation for its complete combustion, [[C3H8O(l) + O2(g) -> CO2(g) + H2O(g)]], what is the lowest whole-number coefficient of {O2}?",
  ["9", "10", "4.5", "18"],
  ["C: 3 {CO2}; H: 4 {H2O}; O needed = 6 + 4 = 10, minus 1 O already in the fuel = 9 O = 4.5 {O2}. Double: 2, 9, 6, 8.",
   "This forgets the oxygen atom already in the fuel. With two fuel molecules, 2 O come from the fuel.",
   "4.5 balances the atoms but is not a whole number. Double every coefficient.",
   "18 is double the lowest set; 2, 9, 6, 8 has no common factor."],
  "Count the O inside the fuel too. Clear the fraction at the end.",
  "[[2 C3H8O(l) + 9 O2(g) -> 6 CO2(g) + 8 H2O(g)]]: O 2 + 18 = 20 = 12 + 8. Coefficient of {O2}: <b>9</b>.", 3)

Q(T, "Which reaction is a <b>single-displacement</b> reaction?",
  ["[[Fe(s) + Pb(NO3)2(aq) -> Fe(NO3)2(aq) + Pb(s)]]",
   "[[Na2CO3(aq) + 2 HCl(aq) -> 2 NaCl(aq) + H2O(l) + CO2(g)]]",
   "[[2 H2O(l) -> 2 H2(g) + O2(g)]]",
   "[[H2(g) + Cl2(g) -> 2 HCl(g)]]"],
  ["The element Fe replaces {Pb^2+} in its compound and becomes {Fe^2+}; lead metal is released.",
   "Two compounds swap partners (and {H2CO3} breaks into {H2O} and {CO2}): double displacement.",
   "One compound breaks into elements: decomposition (electrolysis of water).",
   "Two elements form one compound: combination."],
  "Look for element + compound on the left and a different element + compound on the right.",
  "<b>Fe + {Pb(NO3)2} &rarr; {Fe(NO3)2} + Pb</b> fits A + BC &rarr; AC + B.", 2)

# ======================= ch07-solubility (10) =======================
T = 'ch07-solubility'
Q(T, "Which substance is a <b>nonelectrolyte</b> when dissolved in water?",
  ["{C6H12O6}", "KCl", "{HNO3}", "{NH3}"],
  ["Glucose dissolves as whole molecules and forms no ions, so its solution does not conduct electricity.",
   "KCl is a soluble ionic compound: it separates completely into {K^+} and {Cl^-}, a strong electrolyte.",
   "Nitric acid is on the strong-acid list; it ionizes completely, a strong electrolyte.",
   "Ammonia is a weak base: it forms a few ions, so it is a weak electrolyte."],
  "Does it form ions? Sugars and alcohols dissolve as molecules.",
  "Glucose, <b>{C6H12O6}</b>, dissolves without forming ions: a nonelectrolyte. It travels in blood as whole molecules.", 1)

Q(T, "A conductivity tester is dipped into four solutions, all at the same concentration. The table shows how brightly its bulb glows. Solution B is most likely which substance?",
  ["Acetic acid, {HC2H3O2}", "Potassium chloride, KCl", "Sucrose, {C12H22O11}", "Hydrochloric acid, HCl"],
  ["A dim glow means only a few ions: a weak electrolyte. Acetic acid is a weak acid (not on the strong-acid list).",
   "KCl is a soluble ionic compound that separates completely; it would glow brightly, like solution A.",
   "Sucrose forms no ions, so it would not light the bulb at all, like solution C.",
   "HCl is a strong acid that ionizes completely; it would glow brightly."],
  "Bright = many ions (strong); dim = few ions (weak); none = no ions (nonelectrolyte).",
  "Dim glow = weak electrolyte = <b>acetic acid</b>. A could be KCl or HCl; C could be sucrose.", 2, 0,
  [{"type": "table", "cap": "Conductivity test results", "head": ["Solution", "Bulb"],
    "rows": [["A", "bright"], ["B", "dim"], ["C", "does not light"]]}])

Q(T, "Calcium nitrate is a fertilizer used on Valley crops. Which equation shows what happens when it dissolves in water?",
  ["[[Ca(NO3)2(s) -> Ca^2+(aq) + 2 NO3^-(aq)]]",
   "[[Ca(NO3)2(s) -> Ca^2+(aq) + NO3^-(aq)]]",
   "[[Ca(NO3)2(s) -> Ca^2+(aq) + 2 N^5+(aq) + 6 O^2-(aq)]]",
   "[[Ca(NO3)2(s) -> Ca^2+(aq) + (NO3)2^2-(aq)]]"],
  ["One calcium ion and two nitrate ions; polyatomic ions stay together. Charge: +2 + 2(&minus;1) = 0.",
   "The subscript 2 means two {NO3^-} ions. With only one, the charges do not balance.",
   "Nitrate is a polyatomic ion; it stays together as {NO3^-} when the salt dissolves.",
   "The subscript outside the parentheses counts separate ions; it does not join them into one 2&minus; ion."],
  "Polyatomic ions stay intact; subscripts outside the parentheses give the number of ions.",
  "<b>[[Ca(NO3)2(s) -> Ca^2+(aq) + 2 NO3^-(aq)]]</b>", 1)

Q(T, "How many ions in total are released when one formula unit of {Al2(SO4)3} dissolves completely?",
  ["5", "2", "17", "6"],
  ["2 {Al^3+} + 3 {SO4^2-} = 5 ions. Charge: 2(+3) + 3(&minus;2) = 0.",
   "There are two <i>kinds</i> of ions, but 2 aluminum ions and 3 sulfate ions.",
   "17 is the number of atoms. Each sulfate stays together as one ion.",
   "This multiplies the subscripts (2 &times; 3); add the ions instead."],
  "Write the dissolving equation and count the ions on the right.",
  "[[Al2(SO4)3(s) -> 2 Al^3+(aq) + 3 SO4^2-(aq)]]: 2 + 3 = <b>5</b> ions.", 2)

Q(T, "Use the solubility rules. Which compound is <b>insoluble</b> in water?",
  ["AgI", "NaI", "{Mg(C2H3O2)2}", "{(NH4)2CO3}"],
  ["Iodides are soluble except with {Ag^+}, {Hg2^2+}, and {Pb^2+}. Silver iodide is one of those exceptions.",
   "Sodium is in Group 1: every sodium compound is soluble.",
   "Acetates are always soluble.",
   "Ammonium compounds are always soluble, even carbonates."],
  "First check for an always-soluble ion (Group 1, {NH4^+}, nitrate, acetate). Then find the anion's row.",
  "AgI: iodide with {Ag^+} is an exception, so <b>AgI is insoluble</b>.", 1)

Q(T, "Kidney stones and the scale in kettles are insoluble salts. Which of these compounds is <b>soluble</b> in water?",
  ["{K2CO3}", "{BaCO3}", "{CaC2O4}", "{Ag2SO4}"],
  ["Carbonates are insoluble except with Group 1 and {NH4^+}. Potassium is Group 1, so {K2CO3} dissolves.",
   "Carbonate with {Ba^2+} is not an exception, so barium carbonate is insoluble.",
   "Oxalates are insoluble except with Group 1 and {NH4^+}; calcium oxalate is the main mineral in most kidney stones.",
   "Sulfates are soluble except with {Ca^2+}, {Sr^2+}, {Ba^2+}, {Ag^+}, and {Pb^2+}; silver is an exception."],
  "Carbonates, phosphates, chromates, and oxalates are insoluble unless the cation is Group 1 or ammonium.",
  "Only <b>{K2CO3}</b> has a Group 1 cation; the other three are on the insoluble side of their rows.", 2)

Q(T, "A barium contrast agent must be <b>insoluble</b>, so that almost no toxic {Ba^2+} dissolves and is absorbed. By the solubility rules, which barium compound is insoluble?",
  ["{BaSO4}", "{BaCl2}", "{Ba(NO3)2}", "BaS"],
  ["Sulfates are soluble except with {Ca^2+}, {Sr^2+}, {Ba^2+}, {Ag^+}, {Pb^2+}. Barium sulfate is an exception, so it stays solid.",
   "Chlorides are soluble unless the cation is {Ag^+}, {Hg2^2+}, or {Pb^2+}; {BaCl2} dissolves (and is toxic).",
   "Nitrates are always soluble.",
   "Sulfides are insoluble except with Group 1, {NH4^+}, {Ca^2+}, {Sr^2+}, and {Ba^2+}; barium is one of the exceptions, so BaS dissolves."],
  "Check each anion's row and whether {Ba^2+} is listed as an exception.",
  "<b>{BaSO4}</b> is insoluble (sulfate with {Ba^2+}), which is why it is used for X-ray contrast. (Context only.)", 2)

Q(T, "Which sulfide is <b>insoluble</b> in water?",
  ["ZnS", "CaS", "{Na2S}", "{(NH4)2S}"],
  ["Sulfides are insoluble except with Group 1, {NH4^+}, {Ca^2+}, {Sr^2+}, and {Ba^2+}. Zinc is not an exception.",
   "Calcium is one of the listed exceptions for sulfides and oxides, so CaS is soluble.",
   "Sodium is Group 1: always soluble.",
   "Ammonium compounds are always soluble."],
  "Read the {O^2-}, {S^2-} row carefully: its exceptions include three Group 2 ions.",
  "<b>ZnS</b> is insoluble; {Zn^2+} is not on the exception list.", 3)

Q(T, "Which pair contains <b>two insoluble</b> compounds?",
  ["{PbI2} and {Hg2Cl2}", "{PbI2} and {ZnCl2}", "{AgNO3} and AgCl", "{CaF2} and NaF"],
  ["Both are halide exceptions: iodide with {Pb^2+} and chloride with {Hg2^2+}.",
   "{PbI2} is insoluble, but {ZnCl2} is soluble; {Zn^2+} is not a chloride exception.",
   "AgCl is insoluble, but every nitrate, including {AgNO3}, is soluble.",
   "{CaF2} is insoluble (fluoride with {Ca^2+}), but NaF is soluble (Group 1)."],
  "\"What's the H.A.P. with the heavy halides?\" Which cations make insoluble chlorides, bromides, and iodides?",
  "{Pb^2+} and {Hg2^2+} are halide exceptions, so <b>{PbI2} and {Hg2Cl2}</b> are both insoluble.", 2)

Q(T, "Which statement about strontium fluoride and strontium chloride is correct?",
  ["{SrF2} is insoluble; {SrCl2} is soluble.",
   "{SrF2} is soluble; {SrCl2} is insoluble.",
   "{SrF2} is soluble; {SrCl2} is soluble.",
   "{SrF2} is insoluble; {SrCl2} is insoluble."],
  ["Fluorides are soluble except with {Mg^2+}, {Ca^2+}, {Sr^2+}, {Ba^2+}, {Pb^2+} (so {SrF2} is insoluble); chlorides are soluble except with {Ag^+}, {Hg2^2+}, {Pb^2+} (so {SrCl2} dissolves).",
   "This reverses the two rows. Strontium is a fluoride exception, not a chloride exception.",
   "{Sr^2+} is listed as an exception in the fluoride row.",
   "{Sr^2+} is not an exception in the chloride row."],
  "Fluoride has its own row with different exceptions from the other halides.",
  "<b>{SrF2} is insoluble; {SrCl2} is soluble.</b>", 3)

# ======================= ch07-netionic (10) =======================
T = 'ch07-netionic'
Q(T, "Copper(II) sulfate solution is mixed with sodium hydroxide solution. Which product is the precipitate?",
  ["{Cu(OH)2}", "{Na2SO4}", "CuOH", "No precipitate forms."],
  ["Swap partners: {Cu^2+} + {OH^-} &rarr; {Cu(OH)2}, insoluble (hydroxide, and {Cu^2+} is not an exception).",
   "Sodium is Group 1, so {Na2SO4} stays dissolved.",
   "Copper(II) is {Cu^2+}, so it needs two {OH^-}. The formula comes from the charges.",
   "One product, the copper hydroxide, is insoluble, so a precipitate does form."],
  "Swap partners, write formulas from charges, then check each product on the green sheet.",
  "[[CuSO4(aq) + 2 NaOH(aq) -> Cu(OH)2(s) + Na2SO4(aq)]]: the blue precipitate is <b>{Cu(OH)2}</b>.", 1)

Q(T, "Calcium nitrate solution is mixed with potassium chloride solution. What precipitate forms?",
  ["No precipitate forms.", "{CaCl2}", "{KNO3}", "Both {CaCl2} and {KNO3}"],
  ["The swapped products are {CaCl2} (chloride; {Ca^2+} is not an exception) and {KNO3} (Group 1 and nitrate). Both are soluble: no reaction.",
   "{Ca^2+} is not a chloride exception (only {Ag^+}, {Hg2^2+}, {Pb^2+} are), so {CaCl2} dissolves.",
   "Potassium compounds and nitrates are always soluble.",
   "Both possible products are soluble, so neither precipitates."],
  "Swap partners, then look up both products.",
  "Both {CaCl2} and {KNO3} are soluble, so every ion is a spectator: <b>no precipitate (no reaction)</b>.", 2)

Q(T, "Hard-water scale is calcium carbonate. It forms the same way it does when calcium nitrate solution is mixed with potassium carbonate solution. What is the net ionic equation?",
  ["[[Ca^2+(aq) + CO3^2-(aq) -> CaCO3(s)]]",
   "[[Ca(NO3)2(aq) + K2CO3(aq) -> CaCO3(s) + 2 KNO3(aq)]]",
   "[[2 K^+(aq) + 2 NO3^-(aq) -> 2 KNO3(aq)]]",
   "[[Ca^2+(aq) + CO3^2-(aq) -> Ca^2+(aq) + CO3^2-(aq)]]"],
  ["Only {Ca^2+} and {CO3^2-} change: they form the solid. {K^+} and {NO3^-} are spectators.",
   "This is the molecular equation. The net ionic equation leaves out the spectator ions.",
   "These are the spectators. They are the ions that do <i>not</i> react.",
   "This splits the precipitate into ions. A solid stays together; it is the thing that forms."],
  "Write the complete ionic equation, cancel ions that are identical on both sides, and keep what is left.",
  "Complete ionic: {Ca^2+} + 2 {NO3^-} + 2 {K^+} + {CO3^2-} &rarr; CaCO<sub>3</sub>(s) + 2 {K^+} + 2 {NO3^-}. Net: <b>[[Ca^2+(aq) + CO3^2-(aq) -> CaCO3(s)]]</b>.", 2)

Q(T, "Zinc chloride solution is mixed with potassium sulfide solution, forming a white precipitate. What is the complete ionic equation?",
  ["[[Zn^2+(aq) + 2 Cl^-(aq) + 2 K^+(aq) + S^2-(aq) -> ZnS(s) + 2 K^+(aq) + 2 Cl^-(aq)]]",
   "[[Zn^2+(aq) + 2 Cl^-(aq) + 2 K^+(aq) + S^2-(aq) -> Zn^2+(aq) + S^2-(aq) + 2 K^+(aq) + 2 Cl^-(aq)]]",
   "[[Zn^2+(aq) + Cl^-(aq) + K^+(aq) + S^2-(aq) -> ZnS(s) + K^+(aq) + Cl^-(aq)]]",
   "[[Zn^2+(aq) + Cl2^2-(aq) + K2^2+(aq) + S^2-(aq) -> ZnS(s) + K2^2+(aq) + Cl2^2-(aq)]]"],
  ["Split each aqueous strong electrolyte with the right counts ({ZnCl2} gives 2 {Cl^-}; {K2S} gives 2 {K^+}). The solid ZnS stays together.",
   "This splits the precipitate. ZnS is a solid and must stay as ZnS(s).",
   "The counts are wrong: {ZnCl2} gives two {Cl^-}, and {K2S} gives two {K^+}.",
   "Subscripts count separate ions; they do not make new ions such as Cl<sub>2</sub><sup>2&minus;</sup>."],
  "Molecular first: [[ZnCl2(aq) + K2S(aq) -> ZnS(s) + 2 KCl(aq)]]. Then split only the (aq) compounds.",
  "<b>[[Zn^2+(aq) + 2 Cl^-(aq) + 2 K^+(aq) + S^2-(aq) -> ZnS(s) + 2 K^+(aq) + 2 Cl^-(aq)]]</b>", 3)

Q(T, "Lead(II) acetate solution is mixed with potassium iodide solution, and yellow lead(II) iodide precipitates. What are the spectator ions?",
  ["{K^+} and {C2H3O2^-}", "{Pb^2+} and {I^-}", "{K^+} only", "There are none; all four ions react."],
  ["Potassium acetate is soluble, so {K^+} and {C2H3O2^-} stay dissolved and appear unchanged on both sides.",
   "These are the ions that react: they form the {PbI2} precipitate.",
   "Acetate also stays dissolved; it is unchanged on both sides too.",
   "Only {Pb^2+} and {I^-} leave the solution; the other two ions just watch."],
  "Spectators appear unchanged on both sides of the complete ionic equation.",
  "Net ionic: [[Pb^2+(aq) + 2 I^-(aq) -> PbI2(s)]]. Spectators: <b>{K^+} and {C2H3O2^-}</b>.", 1)

Q(T, "Aluminum hydroxide, an ingredient in some antacids, can be made by mixing aluminum nitrate solution with potassium hydroxide solution. What is the net ionic equation?",
  ["[[Al^3+(aq) + 3 OH^-(aq) -> Al(OH)3(s)]]",
   "[[Al^3+(aq) + OH^-(aq) -> AlOH(s)]]",
   "[[K^+(aq) + NO3^-(aq) -> KNO3(s)]]",
   "[[Al^3+(aq) + 3 OH^-(aq) -> Al^3+(aq) + 3 OH^-(aq)]]"],
  ["{Al^3+} needs three {OH^-} for a neutral solid; atoms and charge (+3 &minus; 3 = 0) balance.",
   "The formula must come from the charges: {Al^3+} needs three {OH^-}, giving {Al(OH)3}.",
   "{KNO3} is soluble (Group 1, nitrate), so {K^+} and {NO3^-} are spectators.",
   "This shows no change. The precipitate {Al(OH)3}(s) must appear as a product."],
  "Hydroxides are insoluble except with Group 1 and {NH4^+} (and slightly soluble with Ca, Sr, Ba).",
  "<b>[[Al^3+(aq) + 3 OH^-(aq) -> Al(OH)3(s)]]</b>; {K^+} and {NO3^-} are spectators.", 2)

Q(T, "Which pair of solutions gives <b>no reaction</b> when mixed?",
  ["{KNO3} and {MgCl2}", "KOH and {MgCl2}", "{K3PO4} and {MgCl2}", "{AgNO3} and {MgCl2}"],
  ["The swapped products, KCl and {Mg(NO3)2}, are both soluble. No precipitate, water, or gas forms.",
   "{Mg(OH)2} would precipitate: hydroxide with {Mg^2+} is insoluble.",
   "{Mg3(PO4)2} would precipitate: phosphates are insoluble except with Group 1 and {NH4^+}.",
   "AgCl would precipitate: chloride with {Ag^+} is an exception."],
  "For each pair, swap partners and check both products.",
  "{KNO3} + {MgCl2} &rarr; KCl(aq) + {Mg(NO3)2}(aq): all ions are spectators, so <b>{KNO3} and {MgCl2}</b> give no reaction.", 2)

Q(T, "Struvite kidney stones contain magnesium and phosphate ions. In the lab, magnesium phosphate precipitates when magnesium chloride solution is mixed with sodium phosphate solution. What is the net ionic equation?",
  ["[[3 Mg^2+(aq) + 2 PO4^3-(aq) -> Mg3(PO4)2(s)]]",
   "[[Mg^2+(aq) + PO4^3-(aq) -> MgPO4(s)]]",
   "[[3 Mg^2+(aq) + 2 PO4^3-(aq) + 6 Na^+(aq) + 6 Cl^-(aq) -> Mg3(PO4)2(s) + 6 Na^+(aq) + 6 Cl^-(aq)]]",
   "[[3 Mg^2+(aq) + 2 PO4^3-(aq) -> Mg3(PO4)2(aq)]]"],
  ["{Mg^2+} and {PO4^3-} combine 3 : 2 for zero charge: 3(+2) + 2(&minus;3) = 0. Atoms and charge balance.",
   "MgPO<sub>4</sub> is not neutral (+2 and &minus;3). The formula must come from the charges.",
   "This is the complete ionic equation. The spectators {Na^+} and {Cl^-} must be cancelled.",
   "Magnesium phosphate is insoluble (phosphate, and Mg is not Group 1), so it is a solid, (s), not (aq)."],
  "Find the precipitate's formula from charges, then keep only the ions that form it.",
  "[[3 MgCl2(aq) + 2 Na3PO4(aq) -> Mg3(PO4)2(s) + 6 NaCl(aq)]]; net: <b>[[3 Mg^2+(aq) + 2 PO4^3-(aq) -> Mg3(PO4)2(s)]]</b>.", 3)

Q(T, "The complete ionic equation for mixing silver nitrate and sodium carbonate solutions is [[2 Ag^+(aq) + 2 NO3^-(aq) + 2 Na^+(aq) + CO3^2-(aq) -> Ag2CO3(s) + 2 Na^+(aq) + 2 NO3^-(aq)]]. What is the net ionic equation?",
  ["[[2 Ag^+(aq) + CO3^2-(aq) -> Ag2CO3(s)]]",
   "[[Ag^+(aq) + CO3^2-(aq) -> Ag2CO3(s)]]",
   "[[2 Ag^+(aq) + 2 NO3^-(aq) + CO3^2-(aq) -> Ag2CO3(s) + 2 NO3^-(aq)]]",
   "[[Ag2^2+(aq) + CO3^2-(aq) -> Ag2CO3(s)]]"],
  ["Cancel 2 {Na^+} and 2 {NO3^-}, which are identical on both sides. What is left is balanced: 2(+1) + (&minus;2) = 0.",
   "The coefficient 2 was dropped: 1 Ag on the left, 2 in the solid.",
   "The nitrate ions are identical on both sides, so they are spectators too.",
   "Silver ions are {Ag^+}; there is no Ag<sub>2</sub><sup>2+</sup> ion. Keep 2 {Ag^+}."],
  "Cancel only ions that are identical (kind, charge, and phase) on both sides.",
  "<b>[[2 Ag^+(aq) + CO3^2-(aq) -> Ag2CO3(s)]]</b>", 3)

Q(T, "Sodium sulfide solution is mixed with copper(II) nitrate solution, and a black solid forms. What is the net ionic equation?",
  ["[[Cu^2+(aq) + S^2-(aq) -> CuS(s)]]",
   "[[Cu^2+(aq) + S^2-(aq) -> CuS(aq)]]",
   "[[Cu^2+(aq) + 2 NO3^-(aq) -> Cu(NO3)2(s)]]",
   "[[Na^+(aq) + NO3^-(aq) -> NaNO3(s)]]"],
  ["Sulfides are insoluble except with Group 1, {NH4^+}, Ca, Sr, Ba, so CuS is the black solid. {Na^+} and {NO3^-} are spectators.",
   "The black solid is the precipitate, so its label is (s).",
   "Nitrates are always soluble; {Cu(NO3)2} is a reactant here, not a precipitate.",
   "{NaNO3} is soluble (Group 1, nitrate). These ions are spectators."],
  "Which swapped product is insoluble?",
  "[[Na2S(aq) + Cu(NO3)2(aq) -> CuS(s) + 2 NaNO3(aq)]]; net: <b>[[Cu^2+(aq) + S^2-(aq) -> CuS(s)]]</b>.", 2)

# ======================= ch07-acidgas (9) =======================
T = 'ch07-acidgas'
Q(T, "What is the balanced molecular equation for hydrobromic acid reacting with potassium hydroxide?",
  ["[[HBr(aq) + KOH(aq) -> H2O(l) + KBr(aq)]]",
   "[[HBr(aq) + KOH(aq) -> H2O(l) + KBr(s)]]",
   "[[HBr(aq) + KOH(aq) -> KOBr(aq) + H2(g)]]",
   "[[HBr(aq) + KOH(aq) -> KH(aq) + BrOH(aq)]]"],
  ["Acid + base &rarr; water + salt: {H^+} and {OH^-} form {H2O}; {K^+} and {Br^-} form KBr, which is soluble.",
   "KBr is soluble (Group 1), so it stays (aq).",
   "Neutralization makes water, not hydrogen gas.",
   "This pairs the cation {K^+} with the cation {H^+}. Swap partners: each cation takes the other anion."],
  "Acid + base &rarr; water + salt. Then check the salt's solubility.",
  "<b>[[HBr(aq) + KOH(aq) -> H2O(l) + KBr(aq)]]</b>", 1)

Q(T, "Sulfuric acid is neutralized by lithium hydroxide: [[H2SO4(aq) + 2 LiOH(aq) -> 2 H2O(l) + Li2SO4(aq)]]. What is the net ionic equation?",
  ["[[H^+(aq) + OH^-(aq) -> H2O(l)]]",
   "[[2 H^+(aq) + 2 OH^-(aq) -> 2 H2O(l)]]",
   "[[H2SO4(aq) + 2 OH^-(aq) -> 2 H2O(l) + SO4^2-(aq)]]",
   "[[2 Li^+(aq) + SO4^2-(aq) -> Li2SO4(s)]]"],
  ["After cancelling 2 {Li^+} and {SO4^2-}, you get 2 {H^+} + 2 {OH^-} &rarr; 2 {H2O}; divide by 2.",
   "Correct species, but the coefficients share a factor of 2. Reduce the net ionic equation.",
   "{H2SO4} is a strong acid, so in an ionic equation it is split into 2 {H^+} and {SO4^2-}.",
   "{Li2SO4} is soluble (Group 1), so {Li^+} and {SO4^2-} are spectators."],
  "Split the strong acid and the soluble base and salt, cancel spectators, then reduce.",
  "<b>[[H^+(aq) + OH^-(aq) -> H2O(l)]]</b>, the same for every strong acid + strong base.", 2)

Q(T, "Milk of magnesia is a suspension of solid magnesium hydroxide that neutralizes stomach acid (HCl). What is the net ionic equation?",
  ["[[Mg(OH)2(s) + 2 H^+(aq) -> Mg^2+(aq) + 2 H2O(l)]]",
   "[[H^+(aq) + OH^-(aq) -> H2O(l)]]",
   "[[Mg(OH)2(s) + 2 HCl(aq) -> MgCl2(aq) + 2 H2O(l)]]",
   "[[Mg(OH)2(s) + H^+(aq) -> Mg^2+(aq) + H2O(l)]]"],
  ["{Mg(OH)2} is insoluble, so it stays together as a solid; HCl and {MgCl2} are split, and {Cl^-} cancels. Charge: +2 = +2.",
   "This splits the solid hydroxide into ions. An insoluble base is written as its formula with (s).",
   "This is the molecular equation; HCl and {MgCl2} are strong electrolytes and are split, leaving {Cl^-} as a spectator.",
   "Two {OH^-} need two {H^+}; here H, O, and charge do not balance."],
  "Hydroxides are insoluble except with Group 1 and {NH4^+}. Keep the solid together.",
  "Complete ionic: {Mg(OH)2}(s) + 2 {H^+} + 2 {Cl^-} &rarr; {Mg^2+} + 2 {Cl^-} + 2 {H2O}. Net: <b>[[Mg(OH)2(s) + 2 H^+(aq) -> Mg^2+(aq) + 2 H2O(l)]]</b>. (Context only.)", 3)

Q(T, "Vinegar (acetic acid, a weak acid) reacts with sodium hydroxide solution. What is the net ionic equation?",
  ["[[HC2H3O2(aq) + OH^-(aq) -> H2O(l) + C2H3O2^-(aq)]]",
   "[[H^+(aq) + OH^-(aq) -> H2O(l)]]",
   "[[Na^+(aq) + C2H3O2^-(aq) -> NaC2H3O2(s)]]",
   "[[HC2H3O2(aq) + NaOH(aq) -> H2O(l) + NaC2H3O2(aq)]]"],
  ["A weak acid is a weak electrolyte, so it stays together as {HC2H3O2} in ionic equations. Only {Na^+} cancels.",
   "This splits acetic acid into ions as if it were a strong acid. It is not on the strong-acid list.",
   "Sodium acetate is soluble (Group 1, acetate), so it does not precipitate.",
   "This is the molecular equation. In an ionic equation, NaOH and {NaC2H3O2} are split and {Na^+} cancels."],
  "Split only strong electrolytes. Is acetic acid a strong acid?",
  "Complete ionic: {HC2H3O2} + {Na^+} + {OH^-} &rarr; {H2O} + {Na^+} + {C2H3O2^-}. Net: <b>[[HC2H3O2(aq) + OH^-(aq) -> H2O(l) + C2H3O2^-(aq)]]</b>.", 3)

Q(T, "After swapping partners for potassium carbonate + nitric acid, a student writes carbonic acid, {H2CO3}(aq), as a product. What should it be replaced with?",
  ["[[CO2(g) + H2O(l)]]",
   "[[CO(g) + H2O2(l)]]",
   "[[H2(g) + CO3(g)]]",
   "Nothing; {H2CO3}(aq) is the final product."],
  ["Carbonic acid is unstable and falls apart into carbon dioxide gas and water: the fizz.",
   "Atoms add up, but carbonic acid breaks into {CO2} and {H2O}, not carbon monoxide and peroxide.",
   "{CO3} is the carbonate ion, not a gas; carbonic acid does not release {H2}.",
   "{H2CO3} is one of the three products that should never be a final answer."],
  "Which three \"products\" must always be rewritten as a gas plus water?",
  "{H2CO3} &rarr; <b>{CO2}(g) + {H2O}(l)</b>: [[K2CO3(aq) + 2 HNO3(aq) -> 2 KNO3(aq) + H2O(l) + CO2(g)]].", 1)

Q(T, "Sodium bisulfite ({NaHSO3}) is a preservative in dried fruit such as golden raisins and apricots. When it reacts with hydrochloric acid, which gas is released?",
  ["{SO2}", "{H2S}", "{SO3}", "{H2}"],
  ["Swapping gives NaCl and {H2SO3}; sulfurous acid is unstable and breaks into {SO2}(g) and {H2O}.",
   "{H2S} comes from an acid + a sulfide ({S^2-}). Bisulfite contains {HSO3^-}.",
   "Sulfurous acid breaks into {SO2} and water; it does not make {SO3}.",
   "Hydrogen gas comes from a metal + an acid, not from a double displacement."],
  "Swap partners and look for one of the unstable products.",
  "[[NaHSO3(aq) + HCl(aq) -> NaCl(aq) + H2O(l) + SO2(g)]]: the gas is <b>sulfur dioxide, {SO2}</b>, the sharp smell of the preservative.", 2)

Q(T, "Spreading an ammonium fertilizer together with a strong base wastes nitrogen as ammonia gas. Which equation correctly shows ammonium sulfate reacting with potassium hydroxide?",
  ["[[(NH4)2SO4(aq) + 2 KOH(aq) -> K2SO4(aq) + 2 H2O(l) + 2 NH3(g)]]",
   "[[(NH4)2SO4(aq) + 2 KOH(aq) -> K2SO4(aq) + 2 NH4OH(aq)]]",
   "[[(NH4)2SO4(aq) + KOH(aq) -> K2SO4(aq) + H2O(l) + NH3(g)]]",
   "[[(NH4)2SO4(aq) + 2 KOH(aq) -> K2SO4(s) + 2 H2O(l) + 2 NH3(g)]]"],
  ["Swapping gives {K2SO4} and {NH4OH}; {NH4OH} becomes {NH3}(g) + {H2O}(l). N 2 = 2, K 2 = 2, H 10 = 4 + 6.",
   "{NH4OH} is unstable and must be rewritten as {NH3}(g) + {H2O}(l).",
   "The products are right, but K, N, and H do not balance: 2 K on the right needs 2 KOH.",
   "{K2SO4} is soluble (Group 1), so it stays (aq)."],
  "Swap, replace {NH4OH}, then balance.",
  "<b>[[(NH4)2SO4(aq) + 2 KOH(aq) -> K2SO4(aq) + 2 H2O(l) + 2 NH3(g)]]</b>", 2)

Q(T, "Solid iron(II) sulfide reacts with hydrochloric acid and gives off a rotten-egg smell. Which is the balanced equation?",
  ["[[FeS(s) + 2 HCl(aq) -> FeCl2(aq) + H2S(g)]]",
   "[[FeS(s) + 2 HCl(aq) -> FeCl2(aq) + H2O(l) + SO2(g)]]",
   "[[FeS(s) + 2 HCl(aq) -> FeCl2(aq) + H2(g) + S(s)]]",
   "[[FeS(s) + 2 HCl(aq) -> FeCl2(s) + H2S(g)]]"],
  ["Acid + sulfide: {H^+} pairs with {S^2-} as {H2S}, already a gas (the rotten-egg smell). {FeCl2} is soluble.",
   "{SO2} comes from sulfites ({SO3^2-}). There is no oxygen in FeS or HCl, so O cannot balance.",
   "Balanced, but this is a double displacement: the partners swap and {H2S} forms; no element is released.",
   "{FeCl2} is soluble ({Fe^2+} is not a chloride exception), so it is (aq)."],
  "Swap partners: {Fe^2+} with {Cl^-}, {H^+} with {S^2-}.",
  "<b>[[FeS(s) + 2 HCl(aq) -> FeCl2(aq) + H2S(g)]]</b>", 3)

Q(T, "Which of these solutions gives <b>no reaction</b> when it is mixed with nitric acid, {HNO3}(aq)?",
  ["KCl", "KOH", "{K2CO3}", "{K2SO3}"],
  ["Swapping gives HCl and {KNO3}: a strong acid and a soluble salt, both fully ionized. No precipitate, water, or gas forms.",
   "An acid and a base make water: a neutralization.",
   "Acid + carbonate makes {H2CO3}, which releases {CO2} gas.",
   "Acid + sulfite makes {H2SO3}, which releases {SO2} gas."],
  "A double displacement needs a precipitate, water, or a gas.",
  "<b>KCl</b>: [[HNO3(aq) + KCl(aq)]] would give only HCl(aq) and {KNO3}(aq), so all four ions are spectators and there is no reaction.", 2)

# ======================= ch07-redox (12) =======================
T = 'ch07-redox'
Q(T, "In [[Mg(s) + Cl2(g) -> MgCl2(s)]], what happens to magnesium?",
  ["It loses 2 electrons and is oxidized.",
   "It gains 2 electrons and is reduced.",
   "It loses 2 electrons and is reduced.",
   "It gains 2 electrons and is oxidized."],
  ["Mg goes from 0 (element) to +2 (in {MgCl2}): loss of electrons is oxidation (LEO).",
   "Magnesium is a metal; it gives electrons to chlorine, which is the one that gains.",
   "Losing electrons is oxidation, not reduction (OIL RIG).",
   "Gaining electrons is reduction, and Mg does not gain electrons here."],
  "Track Mg's oxidation number: element (0) to {Mg^2+}.",
  "Mg: 0 &rarr; +2, so it <b>loses 2 electrons and is oxidized</b>; each Cl: 0 &rarr; &minus;1, reduced.", 1)

Q(T, "Ground-level ozone, {O3}, is a Valley air pollutant. What is the oxidation number of oxygen in {O3}?",
  ["0", "&minus;2", "&minus;6", "+2"],
  ["Rule 1: an atom in a pure element has oxidation number 0. Ozone contains only oxygen.",
   "&minus;2 is oxygen's value in compounds. Rule 1 (elements are 0) comes first.",
   "&minus;6 is 3 &times; (&minus;2), but the sum for a neutral element must be 0, and each O is 0.",
   "There is no other element here for O to be positive against."],
  "Is {O3} an element or a compound?",
  "{O3} is a form of the element oxygen, so each O is <b>0</b>.", 1)

Q(T, "Nitrate, {NO3^-}, is a fertilizer ion that can reach well water. What is the oxidation number of nitrogen in {NO3^-}?",
  ["+5", "+6", "+7", "&minus;1"],
  ["N + 3(&minus;2) = &minus;1 (the ion's charge), so N = +5.",
   "+6 makes the sum 0. A polyatomic ion's oxidation numbers add to its charge, &minus;1.",
   "+7 uses +1 as the total, reversing the sign of the charge.",
   "&minus;1 is the charge of the whole ion, not of nitrogen."],
  "O is &minus;2; the sum must equal the ion's charge.",
  "N + 3(&minus;2) = &minus;1 &rarr; N = <b>+5</b>.", 2)

Q(T, "What is the oxidation number of chromium in potassium chromate, {K2CrO4}?",
  ["+6", "+8", "+7", "&minus;2"],
  ["2(+1) + Cr + 4(&minus;2) = 0, so Cr = +6.",
   "This leaves out the two K atoms: Cr &minus; 8 = 0.",
   "This counts only one K: 1 + Cr &minus; 8 = 0.",
   "&minus;2 is the charge of the chromate ion, not of chromium."],
  "K (Group 1) is +1 and there are two; O is &minus;2 and there are four.",
  "2(+1) + Cr + 4(&minus;2) = 0 &rarr; Cr = <b>+6</b>.", 2)

Q(T, "What is the oxidation number of oxygen in oxygen difluoride, {OF2}?",
  ["+2", "&minus;2", "&minus;1", "0"],
  ["Rule 4 (F is &minus;1) comes before rule 6 (O is &minus;2). With F at &minus;1 each, O + 2(&minus;1) = 0, so O = +2.",
   "Oxygen is usually &minus;2, but the fluorine rule comes earlier and wins; then the sum rule sets O.",
   "&minus;1 is fluorine's value, not oxygen's.",
   "0 is for an element. {OF2} is a compound."],
  "Apply the rules in order. Which comes first: fluorine or oxygen?",
  "F = &minus;1 (rule 4, before oxygen's rule); O + 2(&minus;1) = 0 &rarr; O = <b>+2</b>.", 3)

Q(T, "In [[Ni(s) + 2 Ag^+(aq) -> Ni^2+(aq) + 2 Ag(s)]], which reactant is oxidized?",
  ["Ni", "{Ag^+}", "{Ni^2+}", "Ag"],
  ["Ni goes from 0 to +2: it loses electrons, so it is oxidized.",
   "{Ag^+} goes from +1 to 0: it gains an electron, so it is reduced.",
   "{Ni^2+} is the product formed when Ni is oxidized, not the reactant that was oxidized.",
   "Ag is the product formed when {Ag^+} is reduced."],
  "Which reactant's oxidation number increases?",
  "Ni: 0 &rarr; +2 (oxidized); Ag: +1 &rarr; 0 (reduced). <b>Ni</b> is oxidized.", 2)

Q(T, "The thermite reaction welds railroad rails: [[2 Al(s) + Fe2O3(s) -> Al2O3(s) + 2 Fe(s)]]. What is the oxidizing agent?",
  ["{Fe2O3}", "Al", "{Al2O3}", "Fe"],
  ["Fe goes from +3 (in {Fe2O3}) to 0: Fe is reduced, so {Fe2O3}, the reactant that contains it, is the oxidizing agent.",
   "Al goes from 0 to +3: it is oxidized, so Al is the reducing agent. The agents are swapped.",
   "{Al2O3} is a product. The agents are reactants.",
   "Fe is a product."],
  "The oxidizing agent is the reactant that contains the element that is reduced.",
  "Al: 0 &rarr; +3 (oxidized; reducing agent). Fe: +3 &rarr; 0 (reduced). Oxidizing agent: <b>{Fe2O3}</b>.", 2)

Q(T, "A welding torch burns acetylene: [[2 C2H2(g) + 5 O2(g) -> 4 CO2(g) + 2 H2O(g)]]. What is the reducing agent?",
  ["{C2H2}", "{O2}", "{CO2}", "{H2O}"],
  ["C goes from &minus;1 (in {C2H2}, with H at +1) to +4 (in {CO2}): C is oxidized, so {C2H2} is the reducing agent.",
   "O goes from 0 to &minus;2: oxygen is reduced, so {O2} is the oxidizing agent.",
   "{CO2} is a product; agents are reactants.",
   "{H2O} is a product; agents are reactants."],
  "Which reactant contains the element whose oxidation number goes up?",
  "C: &minus;1 &rarr; +4 (oxidized); O: 0 &rarr; &minus;2 (reduced); H stays +1. Reducing agent: <b>{C2H2}</b>.", 2)

Q(T, "How many electrons are transferred in [[2 Al(s) + 3 Sn^2+(aq) -> 2 Al^3+(aq) + 3 Sn(s)]] as written?",
  ["6", "3", "2", "12"],
  ["2 Al each lose 3 electrons = 6 lost; 3 {Sn^2+} each gain 2 = 6 gained. Lost = gained = 6.",
   "3 is the number lost by one Al atom. There are two Al atoms.",
   "2 is the number gained by one {Sn^2+} ion. There are three.",
   "This adds the electrons lost and gained. They are the same 6 electrons, counted once."],
  "Electrons transferred = electrons lost = electrons gained.",
  "2 Al &rarr; 2 {Al^3+} + 6 e<sup>&minus;</sup>; 3 {Sn^2+} + 6 e<sup>&minus;</sup> &rarr; 3 Sn. <b>6</b> electrons.", 2)

Q(T, "Stainless-steel implants resist corrosion because the chromium in the steel forms a thin protective layer. Where chromium is oxidized, it forms {Cr^3+}. Which is the oxidation half-reaction?",
  ["[[Cr(s) -> Cr^3+(aq) + 3 e^-]]",
   "[[Cr(s) + 3 e^- -> Cr^3+(aq)]]",
   "[[Cr^3+(aq) + 3 e^- -> Cr(s)]]",
   "[[Cr(s) -> Cr^3+(aq) + e^-]]"],
  ["Oxidation is loss of electrons, so the electrons are products. Charge: 0 = +3 + 3(&minus;1).",
   "The electrons are on the wrong side, and the charge does not balance (&minus;3 vs +3).",
   "This is the reverse: a reduction half-reaction.",
   "Cr<sup>3+</sup> means three electrons were lost; with one, the charge does not balance."],
  "Oxidation: electrons on the right. Balance the charge with electrons.",
  "<b>[[Cr(s) -> Cr^3+(aq) + 3 e^-]]</b>", 2)

Q(T, "Use the half-reactions [[Al(s) -> Al^3+(aq) + 3 e^-]] and [[Ag^+(aq) + e^- -> Ag(s)]]. What is the balanced net equation?",
  ["[[Al(s) + 3 Ag^+(aq) -> Al^3+(aq) + 3 Ag(s)]]",
   "[[Al(s) + Ag^+(aq) -> Al^3+(aq) + Ag(s)]]",
   "[[Al(s) + 3 Ag^+(aq) + 3 e^- -> Al^3+(aq) + 3 Ag(s)]]",
   "[[3 Al(s) + Ag^+(aq) -> 3 Al^3+(aq) + Ag(s)]]"],
  ["Multiply the silver half-reaction by 3 so 3 electrons are lost and 3 gained, then add and cancel the electrons. Charge: +3 = +3.",
   "Atoms balance, but charge does not: +1 on the left, +3 on the right.",
   "The electrons were not cancelled. After adding, the 3 e<sup>&minus;</sup> on each side cancel.",
   "The wrong half-reaction was multiplied: 3 Al would lose 9 electrons, and one {Ag^+} gains only 1."],
  "Make electrons lost = electrons gained, then add and cancel the electrons.",
  "Al &rarr; {Al^3+} + 3 e<sup>&minus;</sup>; 3 {Ag^+} + 3 e<sup>&minus;</sup> &rarr; 3 Ag. Sum: <b>[[Al(s) + 3 Ag^+(aq) -> Al^3+(aq) + 3 Ag(s)]]</b>.", 3)

Q(T, "Which reaction is <b>not</b> a redox reaction?",
  ["[[BaCl2(aq) + K2SO4(aq) -> BaSO4(s) + 2 KCl(aq)]]",
   "[[2 Cu(s) + O2(g) -> 2 CuO(s)]]",
   "[[Fe(s) + NiSO4(aq) -> FeSO4(aq) + Ni(s)]]",
   "[[N2(g) + 3 H2(g) -> 2 NH3(g)]]"],
  ["A double displacement: Ba stays +2, Cl &minus;1, K +1, and S +6 on both sides. No oxidation number changes.",
   "Cu goes from 0 to +2 and O from 0 to &minus;2 (copper darkening as it oxidizes in air): redox.",
   "Fe goes from 0 to +2 and Ni from +2 to 0: a single displacement, which is redox.",
   "N goes from 0 to &minus;3 and H from 0 to +1: a combination of elements is redox."],
  "Look for a free element on one side that is part of a compound on the other.",
  "Only <b>{BaCl2} + {K2SO4} &rarr; {BaSO4} + 2 KCl</b> keeps every oxidation number; double displacement is never redox.", 2)

# ======================= ch07-activity (7) =======================
T = 'ch07-activity'
Q(T, "Copper(II) sulfate solution is sprayed on Valley orchards as a fungicide, and it corrodes iron sprayer tanks. " + series('Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu', 'Ag') + " Does iron react with copper(II) sulfate solution?",
  ["Yes: [[Fe(s) + CuSO4(aq) -> FeSO4(aq) + Cu(s)]]",
   "No reaction, because iron is below copper in the series.",
   "Yes: [[Fe(s) + CuSO4(aq) -> FeSO4(s) + Cu(s)]]",
   "Yes: [[Cu(s) + FeSO4(aq) -> CuSO4(aq) + Fe(s)]]"],
  ["Fe is above Cu, so Fe displaces {Cu^2+}: iron is oxidized to {Fe^2+} and copper metal plates out.",
   "This reads the list upside down. Iron is above copper (more active).",
   "{FeSO4} is soluble (sulfate, and {Fe^2+} is not an exception), so it is (aq).",
   "This is the reverse reaction. The free metal here is iron, not copper."],
  "Is the free metal (Fe) above the metal in the compound (Cu)?",
  "Fe is above Cu: <b>[[Fe(s) + CuSO4(aq) -> FeSO4(aq) + Cu(s)]]</b>.", 1)

Q(T, series('Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu', 'Ag', 'Au') + " Which metal will <b>not</b> react with hydrochloric acid?",
  ["Cu", "Zn", "Mg", "Sn"],
  ["Copper is below {H2}, so it cannot displace {H^+} from the acid.",
   "Zinc is above {H2}, so it reacts with HCl and releases {H2} gas.",
   "Magnesium is above {H2} and reacts quickly with acids.",
   "Tin is above {H2} (just barely), so it reacts slowly with HCl."],
  "Metals above {H2} release hydrogen from acids.",
  "<b>Cu</b> is below {H2}: no reaction with HCl.", 1)

Q(T, series('Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu', 'Ag', 'Au') + " Which metal could recover lead from a solution of lead(II) nitrate?",
  ["Zn", "Cu", "Ag", "Au"],
  ["Zinc is above lead, so it displaces {Pb^2+}: [[Zn(s) + Pb(NO3)2(aq) -> Zn(NO3)2(aq) + Pb(s)]].",
   "Copper is below lead, so it cannot displace {Pb^2+}.",
   "Silver is below lead.",
   "Gold is at the bottom of the list; it displaces nothing."],
  "The free metal must be above the metal in the ion.",
  "Only <b>Zn</b> is above Pb on the list.", 2)

Q(T, series('Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb') + " Does lead metal react with zinc chloride solution?",
  ["No reaction: lead is below zinc.",
   "Yes: [[Pb(s) + ZnCl2(aq) -> PbCl2(s) + Zn(s)]]",
   "Yes: [[Pb(s) + ZnCl2(aq) -> PbCl2(aq) + Zn(s)]]",
   "Yes: [[Pb(s) + 2 ZnCl2(aq) -> PbCl4(aq) + 2 Zn(s)]]"],
  ["The free metal (Pb) is below the metal in the compound (Zn), so it cannot displace {Zn^2+}.",
   "This compares the metals the wrong way. Lead is below zinc, so no products form.",
   "Lead is below zinc, so no reaction occurs (and {PbCl2} would be insoluble anyway).",
   "Lead is below zinc, so there is no reaction; lead also forms {Pb^2+}, not Pb<sup>4+</sup>, in this chapter."],
  "Compare the free metal with the metal in the compound, not with the anion.",
  "Pb is below Zn: <b>no reaction</b>.", 2)

Q(T, series('Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu') + " Which equation correctly shows aluminum reacting with hydrochloric acid?",
  ["[[2 Al(s) + 6 HCl(aq) -> 2 AlCl3(aq) + 3 H2(g)]]",
   "[[Al(s) + 3 HCl(aq) -> AlCl3(aq) + 3 H(g)]]",
   "[[Al(s) + 2 HCl(aq) -> AlCl2(aq) + H2(g)]]",
   "[[4 Al(s) + 12 HCl(aq) -> 4 AlCl3(aq) + 6 H2(g)]]"],
  ["Al is above {H2}. {Al^3+} needs 3 {Cl^-}: {AlCl3}. H: 6 = 3 &times; 2; and 2, 6, 2, 3 share no factor.",
   "Hydrogen gas is diatomic, {H2}, not H.",
   "Aluminum forms {Al^3+}, so its chloride is {AlCl3}.",
   "Balanced, but every coefficient shares a factor of 2."],
  "Metal + acid &rarr; salt + {H2}(g). Write the salt from charges, then balance.",
  "<b>[[2 Al(s) + 6 HCl(aq) -> 2 AlCl3(aq) + 3 H2(g)]]</b>", 2)

Q(T, series('Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu') + " A metal reacts with nickel(II) nitrate solution but not with zinc nitrate solution. Which metal could it be?",
  ["Fe", "Mg", "Sn", "Cu"],
  ["Fe is above Ni (so it displaces {Ni^2+}) but below Zn (so it cannot displace {Zn^2+}).",
   "Mg is above Zn, so it would react with zinc nitrate too.",
   "Sn is below Ni, so it would not react with nickel(II) nitrate.",
   "Cu is below both Ni and Zn; it reacts with neither."],
  "The metal must sit between Zn and Ni on the list.",
  "Between Zn and Ni there is only <b>Fe</b>.", 3)

Q(T, "Galvanized steel irrigation pipe is coated with zinc, which corrodes in place of the iron. " + series('Mg', 'Al', 'Zn', 'Fe', 'Ni') + " Which net ionic equation shows zinc reacting with {Fe^2+} ions?",
  ["[[Zn(s) + Fe^2+(aq) -> Zn^2+(aq) + Fe(s)]]",
   "[[Fe(s) + Zn^2+(aq) -> Fe^2+(aq) + Zn(s)]]",
   "[[Zn(s) + 2 Fe^2+(aq) -> Zn^2+(aq) + 2 Fe(s)]]",
   "[[Zn(s) + Fe^2+(aq) -> Zn^2+(aq) + Fe(s) + 2 e^-]]"],
  ["Zn is above Fe, so Zn is oxidized to {Zn^2+} and {Fe^2+} is reduced to Fe. 2 electrons lost = 2 gained; charge +2 = +2.",
   "This is the reverse. Iron is below zinc, so it cannot displace {Zn^2+}.",
   "Charge does not balance: +4 on the left, +2 on the right. One Zn gives 2 electrons, enough for one {Fe^2+}.",
   "Electrons cancel in a net equation; here the charge does not balance (+2 vs 0)."],
  "Higher metal is oxidized; the lower metal's ion is reduced. Check charge.",
  "<b>[[Zn(s) + Fe^2+(aq) -> Zn^2+(aq) + Fe(s)]]</b>", 3)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')),
      'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
