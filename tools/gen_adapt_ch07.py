#!/usr/bin/env python3
"""Builds bank/ch07_adapt.json (Chapter 7 ADAPT homework-only items, text only; 42 items, none repeated from
bank/ch07.json).
usage: python3 tools/gen_adapt_ch07.py bank/ch07_adapt.json
Same conventions and markup as tools/gen_bank_ch07.py (green-sheet solubility table, strong-acid list, unstable
products, activity series Li K Ca Na Mg Al Zn Fe Ni Sn Pb H2 Cu Ag Au, ordered oxidation-number rules, no
H2O/H+/OH- redox balancing). y[0] begins "Correct: ". Every item is rechecked by tools/check_bank_ch07.py."""
import json, sys, re, collections
OUT = sys.argv[1]
M = '&minus;'
B = []

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

def Q(t, q, c, y, h, w, d, k=0):
    y = ["Correct: " + y[0]] + y[1:]
    it = {"id": "c7-h%02d" % (len(B) + 1), "t": t, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    B.append(it)

# ======================= ch07-equations (6) =======================
T = 'ch07-equations'
Q(T, "An equation for heating baking soda is written with a &Delta; over the arrow: [[2 NaHCO3(s) -> Na2CO3(s) + H2O(g) + CO2(g)]]. What does the &Delta; mean?",
  ["The reactant is heated.", "A catalyst is added.", "The reaction releases heat to the surroundings.", "The reaction can run in both directions."],
  ["A &Delta; (delta) over the arrow means the reactants are heated to make the reaction go.",
   "A catalyst is shown by writing its formula over the arrow, not a &Delta;.",
   "The &Delta; describes a condition (heat is supplied), not heat given off.",
   "A reaction that runs both ways is shown with a double arrow, not a &Delta;."],
  "Symbols over the arrow describe the conditions of the reaction.",
  "&Delta; over the arrow = <b>the reactants are heated</b>.", 1)

Q(T, "Ammonium phosphate is a fertilizer. How many hydrogen atoms are represented by 4 {(NH4)3PO4}?",
  ["48", "12", "16", "7"],
  ["One formula unit has 3 &times; 4 = 12 H; four of them have 4 &times; 12 = 48 H.",
   "12 is the H count in one formula unit; the coefficient 4 multiplies the whole formula.",
   "This ignores the subscript 3 outside the parentheses: 4 &times; 4 = 16.",
   "This adds the numbers (4 + 3) instead of multiplying."],
  "Coefficient &times; outside subscript &times; inside subscript.",
  "4 &times; 3 &times; 4 = <b>48</b> H atoms.", 2)

Q(T, "A beaker of sodium sulfate solution has a mass of 62.45 g, and a beaker of barium chloride solution has a mass of 58.30 g (beakers included). The two solutions are poured together into a third, empty beaker of mass 41.18 g, and a white precipitate forms. The two emptied beakers now have a mass of 82.30 g together. What is the mass of the third beaker and its contents?",
  ["79.63 g", "38.45 g", "120.75 g", "161.93 g"],
  ["Solutions transferred = (62.45 + 58.30) &minus; 82.30 = 38.45 g. Third beaker + contents = 41.18 + 38.45 = 79.63 g. The precipitate does not change the total mass.",
   "38.45 g is the mass of the solutions that were poured in; the empty beaker's 41.18 g must be added.",
   "120.75 g is the two full beakers together, before they were emptied.",
   "This adds the empty third beaker to both full beakers without subtracting the emptied beakers."],
  "Find the mass of solution that was poured, then add the empty beaker. Forming a solid does not create or destroy mass.",
  "Poured: 120.75 g &minus; 82.30 g = 38.45 g; total: 38.45 g + 41.18 g = <b>79.63 g</b>.", 3, 1)

Q(T, "Balance the equation: [[Al(s) + H2SO4(aq) -> Al2(SO4)3(aq) + H2(g)]]. What are the coefficients, in order?",
  ["2, 3, 1, 3", "2, 3, 1, 6", "1, 3, 1, 3", "4, 6, 2, 6"],
  ["Al: 2 Al; sulfate as a unit: 3 {H2SO4}; H: 6 H = 3 {H2}. Al 2 = 2; SO<sub>4</sub> 3 = 3; H 6 = 6.",
   "This counts hydrogen as atoms (6 H). Hydrogen gas is {H2}, so 6 H atoms make 3 {H2}.",
   "Aluminum does not balance: 1 on the left, 2 in {Al2(SO4)3}.",
   "Balanced, but every coefficient shares a factor of 2."],
  "Balance Al, then the sulfate unit, then H as {H2}.",
  "<b>2, 3, 1, 3</b>: [[2 Al(s) + 3 H2SO4(aq) -> Al2(SO4)3(aq) + 3 H2(g)]].", 2)

Q(T, "Hexane, {C6H14}, is a solvent used to extract cooking oil from seeds. In the balanced equation for its complete combustion, [[C6H14(l) + O2(g) -> CO2(g) + H2O(g)]], what is the lowest whole-number coefficient of {O2}?",
  ["19", "9.5", "38", "13"],
  ["C: 6 {CO2}; H: 7 {H2O}; O = 12 + 7 = 19 = 9.5 {O2}. Double: 2, 19, 12, 14.",
   "9.5 balances the atoms but is not a whole number. Double every coefficient.",
   "38 is double the lowest set.",
   "This counts 1 O in each {CO2}: 6 + 7 = 13."],
  "C, then H, then O; if O ends up odd, double everything.",
  "[[2 C6H14(l) + 19 O2(g) -> 12 CO2(g) + 14 H2O(g)]]: O 38 = 24 + 14. Coefficient of {O2}: <b>19</b>.", 3)

Q(T, "Solid potassium metal reacts with liquid water to form aqueous potassium hydroxide and hydrogen gas. Which equation is correct, balanced, and labeled?",
  ["[[2 K(s) + 2 H2O(l) -> 2 KOH(aq) + H2(g)]]",
   "[[K(s) + H2O(l) -> KOH(aq) + H(g)]]",
   "[[2 K(s) + 2 H2O(l) -> 2 KOH(s) + H2(g)]]",
   "[[K(s) + H2O(l) -> KOH(aq) + H2(g)]]"],
  ["K 2 = 2; O 2 = 2; H 4 = 2 + 2. Potassium hydroxide is aqueous, as described.",
   "Hydrogen gas is diatomic, {H2}; H(g) is not how hydrogen gas exists.",
   "The description says aqueous potassium hydroxide, so its label is (aq).",
   "H does not balance: 2 on the left, 1 + 2 = 3 on the right."],
  "Write {H2} for hydrogen gas, then balance H with coefficients.",
  "<b>[[2 K(s) + 2 H2O(l) -> 2 KOH(aq) + H2(g)]]</b>", 2)

# ======================= ch07-types (6) =======================
T = 'ch07-types'
Q(T, "Sulfur trioxide from burning sulfur-containing fuels forms acid rain: [[SO3(g) + H2O(l) -> H2SO4(aq)]]. What type of reaction is this?",
  ["Combination", "Decomposition", "Single displacement", "Double displacement"],
  ["Two reactants form one product: A + B &rarr; AB.",
   "Decomposition starts with one reactant; this has two and ends with one.",
   "Neither reactant is a free element.",
   "There is only one product, so no partners are exchanged."],
  "Count the products.",
  "Two reactants, one product: <b>combination</b>.", 1)

Q(T, "Silver oxide, used in some button batteries, breaks down when heated: [[2 Ag2O(s) -> 4 Ag(s) + O2(g)]]. What type of reaction is this?",
  ["Decomposition", "Combination", "Combustion", "Single displacement"],
  ["One compound breaks into simpler substances, here two elements.",
   "Combination makes one product from several; this goes the other way.",
   "{O2} is a product here, and there is no carbon fuel.",
   "There is only one reactant, not an element and a compound."],
  "One reactant alone, usually heated.",
  "AB &rarr; A + B: <b>decomposition</b>.", 1)

Q(T, "Which reaction is a <b>double-displacement</b> reaction?",
  ["[[Na2SO4(aq) + Ba(NO3)2(aq) -> BaSO4(s) + 2 NaNO3(aq)]]",
   "[[Sn(s) + 2 HCl(aq) -> SnCl2(aq) + H2(g)]]",
   "[[C5H12(l) + 8 O2(g) -> 5 CO2(g) + 6 H2O(g)]]",
   "[[4 Na(s) + O2(g) -> 2 Na2O(s)]]"],
  ["Two ionic compounds trade partners, AB + CD &rarr; AD + CB; {Ba^2+} and {SO4^2-} form a precipitate.",
   "An element (Sn) replaces hydrogen in an acid: single displacement.",
   "A carbon fuel burns in {O2}: combustion.",
   "Two elements form one compound: combination."],
  "Two compounds on each side, partners exchanged.",
  "Only the sodium sulfate + barium nitrate reaction swaps partners: <b>double displacement</b>.", 2)

Q(T, "Which equation correctly predicts the products of zinc metal placed in nickel(II) chloride solution?",
  ["[[Zn(s) + NiCl2(aq) -> ZnCl2(aq) + Ni(s)]]",
   "[[Zn(s) + NiCl2(aq) -> ZnNi(s) + Cl2(g)]]",
   "[[Zn(s) + NiCl2(aq) -> ZnCl(aq) + NiCl(aq)]]",
   "[[Zn(s) + NiCl2(aq) -> Zn(s) + Ni(s) + Cl2(g)]]"],
  ["Single displacement: Zn (above Ni) replaces {Ni^2+}, forming {Zn^2+} ({ZnCl2}) and nickel metal.",
   "Two metals do not form an ionic compound, and chloride ions do not become {Cl2} here.",
   "Zinc forms {Zn^2+}, so its chloride is {ZnCl2}; and the nickel ends up as the free metal.",
   "Zinc cannot appear unchanged on both sides; it is the element that reacts."],
  "Element + compound: the free metal takes the place of the metal ion.",
  "<b>[[Zn(s) + NiCl2(aq) -> ZnCl2(aq) + Ni(s)]]</b>", 2)

Q(T, "Burning orchard prunings in a pile is incomplete combustion. Treating the wood as cellulose, {C6H10O5}, which balanced equation shows it burning to carbon monoxide and water?",
  ["[[C6H10O5(s) + 3 O2(g) -> 6 CO(g) + 5 H2O(g)]]",
   "[[C6H10O5(s) + 6 O2(g) -> 6 CO2(g) + 5 H2O(g)]]",
   "[[C6H10O5(s) + 3 O2(g) -> 6 CO2(g) + 5 H2O(g)]]",
   "[[2 C6H10O5(s) + 6 O2(g) -> 12 CO(g) + 10 H2O(g)]]"],
  ["C: 6 CO; H: 5 {H2O}; O on the right = 6 + 5 = 11, minus 5 O in the cellulose = 6 O = 3 {O2}.",
   "This is complete combustion (to {CO2}), with enough oxygen. The question asks for CO.",
   "With {CO2}, O does not balance: 5 + 6 = 11 on the left, 12 + 5 = 17 on the right.",
   "Balanced, but every coefficient shares a factor of 2."],
  "Incomplete combustion gives CO. Count the O already in the fuel.",
  "<b>[[C6H10O5(s) + 3 O2(g) -> 6 CO(g) + 5 H2O(g)]]</b>: O 5 + 6 = 11 = 6 + 5.", 3)

Q(T, "Aluminum powder and sulfur combine when heated. Which equation correctly predicts and balances the product?",
  ["[[2 Al(s) + 3 S(s) -> Al2S3(s)]]",
   "[[Al(s) + S(s) -> AlS(s)]]",
   "[[4 Al(s) + 6 S(s) -> 2 Al2S3(s)]]",
   "[[Al(s) + 2 S(s) -> AlS2(s)]]"],
  ["{Al^3+} and {S^2-} combine 2 : 3 for zero charge: 2(+3) + 3(&minus;2) = 0. Al 2 = 2; S 3 = 3.",
   "AlS would need {Al^2+}. The formula comes from the charges {Al^3+} and {S^2-}.",
   "Balanced, but every coefficient shares a factor of 2.",
   "AlS<sub>2</sub> has charges +3 and 2(&minus;2) = &minus;4, which do not cancel."],
  "Predict the formula from the ion charges, then balance.",
  "{Al^3+} + {S^2-} &rarr; {Al2S3}: <b>[[2 Al(s) + 3 S(s) -> Al2S3(s)]]</b>.", 2)

# ======================= ch07-solubility (6) =======================
T = 'ch07-solubility'
Q(T, "Which substance is a <b>strong</b> electrolyte?",
  ["{HClO4}", "{HC2H3O2}", "{NH3}", "{C2H6O}"],
  ["Perchloric acid is on the strong-acid list, so it ionizes completely.",
   "Acetic acid is a weak acid: only a few molecules ionize.",
   "Ammonia is a weak base: a weak electrolyte.",
   "Ethanol dissolves as whole molecules: a nonelectrolyte."],
  "Strong electrolytes: soluble ionic compounds, the six strong acids, and strong bases.",
  "<b>{HClO4}</b> is one of the six strong acids (HCl, HBr, HI, {HNO3}, {HClO4}, {H2SO4}).", 1)

Q(T, "Use the solubility rules. Which calcium compound is <b>soluble</b> in water?",
  ["{Ca(C2H3O2)2}", "{CaCO3}", "{CaF2}", "{Ca3(PO4)2}"],
  ["Acetates are always soluble, whatever the cation.",
   "Carbonates are insoluble unless the cation is Group 1 or {NH4^+}.",
   "Fluorides are soluble except with Mg, Ca, Sr, Ba, Pb; calcium is an exception.",
   "Phosphates are insoluble unless the cation is Group 1 or {NH4^+}; calcium phosphate is the mineral of bone."],
  "Check the anion's row. Is any ion always soluble?",
  "<b>{Ca(C2H3O2)2}</b>: acetate is always soluble.", 2)

Q(T, "Which equation shows iron(III) sulfate dissolving in water?",
  ["[[Fe2(SO4)3(s) -> 2 Fe^3+(aq) + 3 SO4^2-(aq)]]",
   "[[Fe2(SO4)3(s) -> 2 Fe^3+(aq) + 3 S^6+(aq) + 12 O^2-(aq)]]",
   "[[Fe2(SO4)3(s) -> Fe2^6+(aq) + (SO4)3^6-(aq)]]",
   "[[Fe2(SO4)3(s) -> 2 Fe^2+(aq) + 3 SO4^2-(aq)]]"],
  ["Two {Fe^3+} and three {SO4^2-}: 2(+3) + 3(&minus;2) = 0. Sulfate stays together.",
   "Sulfate is a polyatomic ion; it does not break into S and O ions.",
   "Subscripts count separate ions; they do not join two iron ions or three sulfates into single ions.",
   "Iron(III) means {Fe^3+}; with {Fe^2+}, the charges do not balance (+4 vs &minus;6)."],
  "Keep polyatomic ions intact; subscripts give the number of each ion.",
  "<b>[[Fe2(SO4)3(s) -> 2 Fe^3+(aq) + 3 SO4^2-(aq)]]</b>", 2)

Q(T, "By the green-sheet rules, which compound is <b>insoluble</b> in water?",
  ["{CaSO3}", "{MgSO3}", "{Na2S}", "{NH4F}"],
  ["Sulfites follow the sulfate row: soluble except with {Ca^2+}, {Sr^2+}, {Ba^2+}, {Ag^+}, {Pb^2+}. Calcium is an exception.",
   "{Mg^2+} is not a sulfite exception, so {MgSO3} is soluble by the table.",
   "Sodium is Group 1: always soluble.",
   "Ammonium compounds are always soluble, even fluorides."],
  "Sulfite ({SO3^2-}) shares its row with sulfate.",
  "<b>{CaSO3}</b> is insoluble (sulfite with {Ca^2+}).", 3)

Q(T, "How many ions in total are released when one formula unit of {(NH4)3PO4} dissolves?",
  ["4", "2", "20", "7"],
  ["3 {NH4^+} + 1 {PO4^3-} = 4 ions. Charge: 3(+1) + (&minus;3) = 0.",
   "There are two kinds of ions, but three ammonium ions.",
   "20 is the number of atoms; each polyatomic ion stays together.",
   "This adds the subscripts 3 and 4; the 4 in {PO4} counts O atoms inside one ion."],
  "Write the dissolving equation and count the ions.",
  "[[(NH4)3PO4(s) -> 3 NH4^+(aq) + PO4^3-(aq)]]: <b>4</b> ions.", 2)

Q(T, "Blood contains both dissolved salts and urea, {CO(NH2)2}, a waste product of protein metabolism. Which pair contains one strong electrolyte and one nonelectrolyte?",
  ["{Na2SO4} and {CO(NH2)2}", "HF and {CH4O}", "HCl and NaOH", "{NH3} and {C6H12O6}"],
  ["{Na2SO4} is a soluble ionic compound (strong); urea dissolves as molecules (nonelectrolyte).",
   "HF is not on the strong-acid list, so it is weak; methanol is a nonelectrolyte.",
   "Both are strong electrolytes: a strong acid and a strong base.",
   "Ammonia is weak, and glucose is a nonelectrolyte."],
  "Classify each substance: strong (soluble ionic, strong acid or base), weak, or nonelectrolyte.",
  "<b>{Na2SO4}</b> (strong) and <b>urea</b> (nonelectrolyte).", 3)

# ======================= ch07-netionic (6) =======================
T = 'ch07-netionic'
Q(T, "Lead(II) nitrate solution is mixed with sodium bromide solution. Which product precipitates?",
  ["{PbBr2}", "{NaNO3}", "PbBr", "No precipitate forms."],
  ["Bromides are soluble except with {Ag^+}, {Hg2^2+}, {Pb^2+}: {Pb^2+} + 2 {Br^-} &rarr; {PbBr2}(s).",
   "{NaNO3} is soluble (Group 1 and nitrate).",
   "{Pb^2+} needs two {Br^-}; the formula comes from the charges.",
   "Lead(II) bromide is insoluble, so a precipitate does form."],
  "Swap partners and check each product's row.",
  "[[Pb(NO3)2(aq) + 2 NaBr(aq) -> PbBr2(s) + 2 NaNO3(aq)]]: <b>{PbBr2}</b>.", 1)

Q(T, "Older X-ray film used silver bromide, made by mixing silver nitrate and potassium bromide solutions. What is the net ionic equation?",
  ["[[Ag^+(aq) + Br^-(aq) -> AgBr(s)]]",
   "[[AgNO3(aq) + KBr(aq) -> AgBr(s) + KNO3(aq)]]",
   "[[Ag^+(aq) + Br^-(aq) -> AgBr(aq)]]",
   "[[K^+(aq) + NO3^-(aq) -> KNO3(s)]]"],
  ["{K^+} and {NO3^-} are spectators; only {Ag^+} and {Br^-} form the solid.",
   "This is the molecular equation; the net ionic equation drops the spectators.",
   "AgBr is insoluble (bromide with {Ag^+}), so it is a solid, (s).",
   "{KNO3} is soluble; these ions are the spectators."],
  "Split, cancel the spectators, keep the rest.",
  "<b>[[Ag^+(aq) + Br^-(aq) -> AgBr(s)]]</b>", 2)

Q(T, "Sodium carbonate solution is mixed with copper(II) chloride solution, and a blue-green solid forms. What are the spectator ions?",
  ["{Na^+} and {Cl^-}", "{Cu^2+} and {CO3^2-}", "{Na^+}, {Cl^-}, and {Cu^2+}", "Only {Cl^-}"],
  ["{CuCO3} precipitates (carbonate with {Cu^2+}); NaCl stays dissolved, so {Na^+} and {Cl^-} are unchanged.",
   "These two ions form the precipitate, {CuCO3}.",
   "{Cu^2+} leaves the solution in the solid, so it is not a spectator.",
   "{Na^+} also stays dissolved and unchanged."],
  "Which product is soluble? Its ions are the spectators.",
  "Net: [[Cu^2+(aq) + CO3^2-(aq) -> CuCO3(s)]]. Spectators: <b>{Na^+} and {Cl^-}</b>.", 2)

Q(T, "Sodium phosphate solution is mixed with silver nitrate solution: [[Na3PO4(aq) + 3 AgNO3(aq) -> Ag3PO4(s) + 3 NaNO3(aq)]]. What is the complete ionic equation?",
  ["[[3 Na^+(aq) + PO4^3-(aq) + 3 Ag^+(aq) + 3 NO3^-(aq) -> Ag3PO4(s) + 3 Na^+(aq) + 3 NO3^-(aq)]]",
   "[[3 Na^+(aq) + PO4^3-(aq) + 3 Ag^+(aq) + 3 NO3^-(aq) -> 3 Ag^+(aq) + PO4^3-(aq) + 3 Na^+(aq) + 3 NO3^-(aq)]]",
   "[[Na3^3+(aq) + PO4^3-(aq) + 3 Ag^+(aq) + 3 NO3^-(aq) -> Ag3PO4(s) + Na3^3+(aq) + 3 NO3^-(aq)]]",
   "[[Na^+(aq) + PO4^3-(aq) + Ag^+(aq) + NO3^-(aq) -> Ag3PO4(s) + Na^+(aq) + NO3^-(aq)]]"],
  ["Each aqueous compound is split with its coefficient and subscripts; the solid {Ag3PO4} stays together.",
   "This splits the precipitate. A solid is written as one formula.",
   "{Na3PO4} gives three separate {Na^+} ions, not a Na<sub>3</sub><sup>3+</sup> ion.",
   "The counts are wrong: {Na3PO4} gives 3 {Na^+}, and 3 {AgNO3} give 3 {Ag^+} and 3 {NO3^-}."],
  "Coefficient &times; subscript gives the number of each ion.",
  "<b>3 {Na^+} + {PO4^3-} + 3 {Ag^+} + 3 {NO3^-} &rarr; {Ag3PO4}(s) + 3 {Na^+} + 3 {NO3^-}</b>; net: [[3 Ag^+(aq) + PO4^3-(aq) -> Ag3PO4(s)]].", 3)

Q(T, "Mercury(I) nitrate solution is mixed with potassium chloride solution. What is the net ionic equation?",
  ["[[Hg2^2+(aq) + 2 Cl^-(aq) -> Hg2Cl2(s)]]",
   "[[2 Hg^+(aq) + 2 Cl^-(aq) -> Hg2Cl2(s)]]",
   "[[Hg2^2+(aq) + 2 Cl^-(aq) -> 2 HgCl(s)]]",
   "[[K^+(aq) + NO3^-(aq) -> KNO3(s)]]"],
  ["Mercury(I) is the two-atom ion {Hg2^2+}; with chloride it forms insoluble {Hg2Cl2}.",
   "Mercury(I) exists as {Hg2^2+}; it stays together as one ion, like a polyatomic ion.",
   "The solid is {Hg2Cl2}: the {Hg2^2+} ion is not split in the product either.",
   "{KNO3} is soluble; these are spectators."],
  "Mercury(I) is {Hg2^2+}, one of the H.A.P. halide exceptions.",
  "[[Hg2(NO3)2(aq) + 2 KCl(aq) -> Hg2Cl2(s) + 2 KNO3(aq)]]; net: <b>[[Hg2^2+(aq) + 2 Cl^-(aq) -> Hg2Cl2(s)]]</b>.", 3)

Q(T, "Copper(II) nitrate solution is mixed with each of these solutions. Which one gives <b>no precipitate</b>?",
  ["{NH4Cl}", "NaOH", "{K2CO3}", "{Na3PO4}"],
  ["The swapped products, {NH4NO3} and {CuCl2}, are both soluble ({Cu^2+} is not a chloride exception).",
   "{Cu(OH)2} precipitates: hydroxide with {Cu^2+} is insoluble.",
   "{CuCO3} precipitates: carbonate with {Cu^2+} is insoluble.",
   "{Cu3(PO4)2} precipitates: phosphate with {Cu^2+} is insoluble."],
  "Swap partners with {Cu(NO3)2} and check each new copper compound.",
  "<b>{NH4Cl}</b>: {CuCl2} and {NH4NO3} both dissolve, so there is no reaction.", 2)

# ======================= ch07-acidgas (6) =======================
T = 'ch07-acidgas'
Q(T, "What is the net ionic equation for hydroiodic acid, HI(aq), reacting with sodium hydroxide solution?",
  ["[[H^+(aq) + OH^-(aq) -> H2O(l)]]",
   "[[HI(aq) + OH^-(aq) -> H2O(l) + I^-(aq)]]",
   "[[Na^+(aq) + I^-(aq) -> NaI(s)]]",
   "[[HI(aq) + NaOH(aq) -> H2O(l) + NaI(aq)]]"],
  ["HI is a strong acid and NaOH a strong base; NaI is soluble. Cancel {Na^+} and {I^-}.",
   "HI is on the strong-acid list, so it is split into {H^+} and {I^-}; then {I^-} cancels.",
   "NaI is soluble (Group 1), so these ions are spectators.",
   "This is the molecular equation."],
  "Strong acid + strong base: what is left after the spectators cancel?",
  "<b>[[H^+(aq) + OH^-(aq) -> H2O(l)]]</b>", 1)

Q(T, "Some antacids contain magnesium carbonate. Which is the balanced equation for its reaction with stomach acid, HCl?",
  ["[[MgCO3(s) + 2 HCl(aq) -> MgCl2(aq) + H2O(l) + CO2(g)]]",
   "[[MgCO3(s) + 2 HCl(aq) -> MgCl2(aq) + H2CO3(aq)]]",
   "[[MgCO3(s) + HCl(aq) -> MgCl2(aq) + H2O(l) + CO2(g)]]",
   "[[MgCO3(s) + 2 HCl(aq) -> MgCl2(s) + H2O(l) + CO2(g)]]"],
  ["Swap partners, then replace {H2CO3} with {H2O}(l) + {CO2}(g). Mg 1, C 1, O 3, H 2, Cl 2 on each side.",
   "{H2CO3} is unstable and must be written as {H2O}(l) + {CO2}(g).",
   "Cl and H do not balance: 1 HCl gives 1 Cl, but {MgCl2} has 2.",
   "{MgCl2} is soluble (Mg is not a chloride exception), so it is (aq)."],
  "Carbonate + acid gives a salt, water, and carbon dioxide.",
  "<b>[[MgCO3(s) + 2 HCl(aq) -> MgCl2(aq) + H2O(l) + CO2(g)]]</b>; the {CO2} is what causes belching. (Context only.)", 2)

Q(T, "Sodium sulfide solution is mixed with hydrochloric acid. Which gas forms?",
  ["{H2S}", "{SO2}", "{H2}", "{Cl2}"],
  ["Swapping gives NaCl and {H2S}; hydrogen sulfide is already a gas (rotten-egg smell).",
   "{SO2} comes from sulfites ({SO3^2-}); a sulfide has no oxygen.",
   "{H2} comes from a metal + acid, not from a double displacement.",
   "Chloride ions stay as {Cl^-} in NaCl(aq); no {Cl2} forms."],
  "Swap partners: {H^+} pairs with {S^2-}.",
  "[[Na2S(aq) + 2 HCl(aq) -> 2 NaCl(aq) + H2S(g)]]: <b>{H2S}</b>.", 2)

Q(T, "Sulfites are preservatives in wine. Potassium sulfite reacts with hydrobromic acid: [[K2SO3(aq) + 2 HBr(aq) -> 2 KBr(aq) + H2O(l) + SO2(g)]]. What is the net ionic equation?",
  ["[[2 H^+(aq) + SO3^2-(aq) -> H2O(l) + SO2(g)]]",
   "[[2 H^+(aq) + SO3^2-(aq) -> H2SO3(aq)]]",
   "[[H^+(aq) + SO3^2-(aq) -> H2O(l) + SO2(g)]]",
   "[[2 K^+(aq) + 2 Br^-(aq) -> 2 KBr(s)]]"],
  ["{K^+} and {Br^-} are spectators. Two {H^+} and one {SO3^2-} give water and {SO2}; charge 0 = 0.",
   "{H2SO3} is unstable; write {H2O}(l) + {SO2}(g).",
   "H and charge do not balance: one {H^+} cannot make {H2O}.",
   "KBr is soluble (Group 1); these ions are spectators."],
  "Split the soluble compounds and the strong acid; water and the gas stay together.",
  "<b>[[2 H^+(aq) + SO3^2-(aq) -> H2O(l) + SO2(g)]]</b>", 3)

Q(T, "Instant cold packs contain ammonium nitrate. If it is mixed with a sodium hydroxide drain cleaner, a sharp-smelling gas forms. Which equation is correct?",
  ["[[NH4NO3(aq) + NaOH(aq) -> NaNO3(aq) + H2O(l) + NH3(g)]]",
   "[[NH4NO3(aq) + NaOH(aq) -> NaNO3(aq) + NH4OH(aq)]]",
   "[[NH4NO3(aq) + NaOH(aq) -> NaNO3(s) + H2O(l) + NH3(g)]]",
   "[[NH4NO3(aq) + NaOH(aq) -> NaNO3(aq) + H2O(l) + N2(g)]]"],
  ["Swapping gives {NaNO3} and {NH4OH}, and {NH4OH} becomes {NH3}(g) + {H2O}(l). N 2, H 5, O 4, Na 1 on each side.",
   "{NH4OH} is unstable; write {NH3}(g) + {H2O}(l).",
   "{NaNO3} is soluble (Group 1, nitrate), so it is (aq).",
   "The gas is ammonia, {NH3}, not nitrogen; with {N2} the H atoms do not balance."],
  "Ammonium salt + strong base gives which unstable product?",
  "<b>[[NH4NO3(aq) + NaOH(aq) -> NaNO3(aq) + H2O(l) + NH3(g)]]</b>", 2)

Q(T, "Hydrochloric acid is added to each of these solutions. Which one produces a gas?",
  ["{NaHCO3}", "{Na2SO4}", "NaCl", "NaOH"],
  ["Bicarbonate + acid gives {H2CO3}, which breaks into {H2O} and {CO2} gas.",
   "Sulfate is not sulfite: HCl + {Na2SO4} gives only dissolved ions, so no gas and no reaction.",
   "NaCl + HCl gives nothing new; all the ions are spectators.",
   "NaOH + HCl is a neutralization: it makes water, not a gas."],
  "Which anion makes one of the unstable products with {H^+}?",
  "[[NaHCO3(aq) + HCl(aq) -> NaCl(aq) + H2O(l) + CO2(g)]]: <b>{NaHCO3}</b>.", 3)

# ======================= ch07-redox (6) =======================
T = 'ch07-redox'
Q(T, "Rust is mostly iron(III) oxide, {Fe2O3}. What is the oxidation number of iron in {Fe2O3}?",
  ["+3", "+6", "+2", "&minus;2"],
  ["2 Fe + 3(&minus;2) = 0, so 2 Fe = +6 and each Fe = +3.",
   "+6 is the total for both Fe atoms; divide by 2.",
   "+2 is iron in FeO, iron(II) oxide.",
   "&minus;2 is the oxidation number of oxygen. (The free {O2} that rusts the iron starts at 0.)"],
  "O is &minus;2; the sum is 0; there are two Fe atoms.",
  "2 Fe + 3(&minus;2) = 0 &rarr; Fe = <b>+3</b>.", 1)

Q(T, "The carbonate ion, {CO3^2-}, is part of blood chemistry. What is the oxidation number of carbon in {CO3^2-}?",
  ["+4", "+6", "+8", "&minus;2"],
  ["C + 3(&minus;2) = &minus;2, so C = +4.",
   "+6 makes the sum 0; an ion's oxidation numbers add to its charge, &minus;2.",
   "+8 uses +2 as the total, reversing the sign of the charge.",
   "&minus;2 is the charge of the whole ion, not of carbon."],
  "O is &minus;2; the sum equals the ion's charge.",
  "C + 3(&minus;2) = &minus;2 &rarr; C = <b>+4</b>.", 2)

Q(T, "Household bleach, used to disinfect hospital surfaces, contains the hypochlorite ion, {ClO^-}. What is the oxidation number of chlorine?",
  ["+1", "&minus;1", "+2", "&minus;3"],
  ["The oxygen rule (rule 6) comes before the other-halogen rule (rule 7): O = &minus;2, so Cl + (&minus;2) = &minus;1 and Cl = +1.",
   "Chlorine is usually &minus;1, but oxygen's rule comes first; then the sum rule sets Cl.",
   "+2 makes the sum 0; the ion's charge is &minus;1.",
   "&minus;3 uses +1 as the total, reversing the sign of the charge."],
  "Apply the rules in order: which comes first, oxygen or the other halogens?",
  "O = &minus;2; Cl + (&minus;2) = &minus;1 &rarr; Cl = <b>+1</b>.", 3)

Q(T, "Chlorine water added to potassium iodide solution turns brown as iodine forms: [[Cl2(aq) + 2 KI(aq) -> 2 KCl(aq) + I2(aq)]]. What is the oxidizing agent?",
  ["{Cl2}", "KI", "KCl", "{I2}"],
  ["Cl goes from 0 to &minus;1: chlorine is reduced, so {Cl2} is the oxidizing agent.",
   "I goes from &minus;1 to 0: iodide is oxidized, so KI is the reducing agent. The agents are swapped.",
   "KCl is a product; agents are reactants.",
   "{I2} is a product; agents are reactants."],
  "The oxidizing agent contains the element that is reduced.",
  "Cl: 0 &rarr; &minus;1 (reduced); I: &minus;1 &rarr; 0 (oxidized). Oxidizing agent: <b>{Cl2}</b>.", 2)

Q(T, "How many electrons are transferred in [[2 Fe(s) + 3 Cl2(g) -> 2 FeCl3(s)]] as written?",
  ["6", "3", "2", "12"],
  ["2 Fe each lose 3 (0 &rarr; +3) = 6; 6 Cl each gain 1 (0 &rarr; &minus;1) = 6.",
   "3 is the number lost by one Fe atom; there are two.",
   "2 is the number of Fe atoms, not electrons.",
   "This adds the electrons lost and gained; they are the same 6 electrons."],
  "Electrons lost by all the Fe atoms = electrons gained by all the Cl atoms.",
  "2 Fe &rarr; 2 {Fe^3+} + 6 e<sup>&minus;</sup>; 3 {Cl2} + 6 e<sup>&minus;</sup> &rarr; 6 {Cl^-}: <b>6</b> electrons.", 3)

Q(T, "In [[Mg(s) + Sn^2+(aq) -> Mg^2+(aq) + Sn(s)]], which is the reduction half-reaction?",
  ["[[Sn^2+(aq) + 2 e^- -> Sn(s)]]",
   "[[Sn^2+(aq) -> Sn(s) + 2 e^-]]",
   "[[Mg(s) -> Mg^2+(aq) + 2 e^-]]",
   "[[Sn^2+(aq) + e^- -> Sn(s)]]"],
  ["Reduction is gain of electrons, so the electrons are reactants. Charge: +2 &minus; 2 = 0.",
   "The electrons are on the wrong side; the charge does not balance (+2 vs &minus;2).",
   "This is the oxidation half-reaction: magnesium loses electrons.",
   "{Sn^2+} needs two electrons to become neutral Sn; with one, charge does not balance."],
  "Reduction: electrons on the left.",
  "<b>[[Sn^2+(aq) + 2 e^- -> Sn(s)]]</b>", 2)

# ======================= ch07-activity (6) =======================
T = 'ch07-activity'
Q(T, series('Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu', 'Ag', 'Au') + " A silver ring is dropped into copper(II) nitrate solution. What happens?",
  ["No reaction: silver is below copper.",
   "Yes: [[2 Ag(s) + Cu(NO3)2(aq) -> 2 AgNO3(aq) + Cu(s)]]",
   "Yes: [[Ag(s) + Cu(NO3)2(aq) -> AgNO3(aq) + Cu(s)]]",
   "Yes: [[Ag(s) + Cu(NO3)2(aq) -> Ag(NO3)2(aq) + Cu(s)]]"],
  ["The free metal (Ag) is below the metal in the compound (Cu), so it cannot displace {Cu^2+}.",
   "This reads the list upside down: silver is below copper, so the ring does not react.",
   "Silver cannot displace copper, so no products form at all.",
   "Silver is below copper, so no reaction occurs (and silver forms {Ag^+}, not Ag<sup>2+</sup>)."],
  "Is the free metal above the metal in the compound?",
  "Ag is below Cu: <b>no reaction</b>.", 1)

Q(T, series('Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu') + " Which metal reacts with zinc nitrate solution?",
  ["Al", "Fe", "Ni", "Cu"],
  ["Aluminum is above zinc, so it displaces {Zn^2+}.",
   "Iron is below zinc, so it cannot displace {Zn^2+}.",
   "Nickel is below zinc.",
   "Copper is below zinc (and below {H2})."],
  "The free metal must be above zinc.",
  "Only <b>Al</b> is above Zn among the choices: [[2 Al(s) + 3 Zn(NO3)2(aq) -> 2 Al(NO3)3(aq) + 3 Zn(s)]].", 2)

Q(T, series('Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu', 'Ag') + " Nickel forms {Ni^2+}. Which equation correctly shows nickel reacting with hydrobromic acid?",
  ["[[Ni(s) + 2 HBr(aq) -> NiBr2(aq) + H2(g)]]",
   "[[Ni(s) + 2 HBr(aq) -> NiBr2(aq) + 2 H(g)]]",
   "No reaction: nickel is below hydrogen.",
   "[[Ni(s) + HBr(aq) -> NiBr(aq) + H(g)]]"],
  ["Ni is above {H2}, so it releases hydrogen gas; {Ni^2+} + 2 {Br^-} gives {NiBr2}, which is soluble.",
   "Hydrogen gas is diatomic: 2 H atoms make one {H2} molecule.",
   "Nickel is above {H2}, so it does react.",
   "Nickel forms {Ni^2+}, so its bromide is {NiBr2}; and hydrogen gas is {H2}."],
  "Metal above {H2} + acid &rarr; salt + {H2}(g).",
  "<b>[[Ni(s) + 2 HBr(aq) -> NiBr2(aq) + H2(g)]]</b>", 2)

Q(T, series('Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu') + " A metal releases {H2} from hydrochloric acid but does not react with iron(II) chloride solution. Which metal could it be?",
  ["Ni", "Zn", "Cu", "Mg"],
  ["Ni is above {H2} (reacts with HCl) but below Fe (cannot displace {Fe^2+}).",
   "Zn is above Fe, so it would react with iron(II) chloride too.",
   "Cu is below {H2}, so it would not react with HCl.",
   "Mg is above Fe, so it would react with iron(II) chloride."],
  "The metal must be below Fe but above {H2}.",
  "Of the choices, only <b>Ni</b> sits between Fe and {H2}.", 3)

Q(T, series('Mg', 'Al', 'Zn', 'Fe', 'Ni') + " What is the net ionic equation for aluminum metal reacting with nickel(II) chloride solution?",
  ["[[2 Al(s) + 3 Ni^2+(aq) -> 2 Al^3+(aq) + 3 Ni(s)]]",
   "[[Al(s) + Ni^2+(aq) -> Al^3+(aq) + Ni(s)]]",
   "[[2 Al(s) + 3 NiCl2(aq) -> 2 AlCl3(aq) + 3 Ni(s)]]",
   "[[3 Ni(s) + 2 Al^3+(aq) -> 3 Ni^2+(aq) + 2 Al(s)]]"],
  ["Al loses 3 electrons and {Ni^2+} gains 2; the least common multiple is 6, so 2 Al and 3 {Ni^2+}. Charge +6 = +6.",
   "Atoms balance, but charge does not: +2 on the left, +3 on the right.",
   "This is the molecular equation; {Cl^-} is a spectator and is left out of the net ionic equation.",
   "This is the reverse reaction. Nickel is below aluminum and cannot displace {Al^3+}."],
  "Balance electrons lost and gained (3 and 2), then check charge.",
  "<b>[[2 Al(s) + 3 Ni^2+(aq) -> 2 Al^3+(aq) + 3 Ni(s)]]</b>", 3)

Q(T, series('Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H2', 'Cu', 'Ag', 'Au') + " Gold is used in dental crowns partly because it resists acids. Which metal does <b>not</b> react with dilute hydrobromic acid, HBr?",
  ["Au", "Pb", "Ni", "Al"],
  ["Gold is below {H2} (at the bottom of the list), so it cannot displace {H^+}.",
   "Lead is above {H2}, so it reacts (slowly) with acids.",
   "Nickel is above {H2}, so it releases hydrogen from acids.",
   "Aluminum is high on the list and reacts with acids."],
  "Metals below {H2} do not react with acids such as HBr.",
  "<b>Au</b> is below {H2}: no reaction.", 2)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
