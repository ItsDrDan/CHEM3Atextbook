#!/usr/bin/env python3
"""Builds bank/ch04.json (Chapter 4 Try It items: naming compounds). Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch04.py bank/ch04.json
Formulas are typed in braces, {Ca(NO3)2}, {SO4^2-}, {CuSO4.5H2O}, {HCl(aq)}, and turned into HTML by X():
digits after a symbol or ')' become subscripts, ^n+ / ^n- become a superscript charge, '.' becomes a raised dot.
tools/check_bank_ch04.py parses every formula back and checks it against its own ion tables and name generators."""
import json, sys, re
OUT = sys.argv[1]
M = '&minus;'
B = []

def F(s):
    """'Ca(NO3)2' -> Ca(NO<sub>3</sub>)<sub>2</sub>; 'SO4^2-' -> SO<sub>4</sub><sup>2&minus;</sup>; 'CuSO4.5H2O' -> CuSO<sub>4</sub>&middot;5H<sub>2</sub>O."""
    ch = ''
    if '^' in s: s, ch = s.split('^')
    tail = ''
    m = re.search(r'\((aq|g)\)$', s)
    if m: s, tail = s[:m.start()], m.group(0)
    parts = s.split('.')
    parts = [re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', p) for p in parts]
    out = '&middot;'.join(parts) + tail
    if ch: out += '<sup>' + ch.replace('-', M) + '</sup>'
    return out

def X(s): return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)

def Q(t, q, c, y, h, w, d, f=None):
    it = {"id": "c4-%03d" % (len(B) + 1), "t": t, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y], "h": X(h), "w": X(w), "d": d, "k": 0}
    if f:
        for fg in f:
            if fg['type'] == 'table':
                fg['head'] = [X(x) for x in fg['head']]; fg['rows'] = [[X(x) for x in r] for r in fg['rows']]
        it["f"] = f
    B.append(it)

# ======================= ch04-formulas (10) =======================
T = 'ch04-formulas'
Q(T, "Aluminum nitrate has the formula {Al(NO3)3}. How many <b>oxygen</b> atoms are in one formula unit?",
  ["9", "3", "6", "12"],
  ["Each nitrate group, NO<sub>3</sub>, has 3 O atoms, and the subscript 3 after the parentheses means three nitrate groups: 3 &times; 3 = 9.",
   "This counts the O atoms in only one nitrate group. The subscript after the parentheses multiplies everything inside them.",
   "This adds the two 3s (3 + 3) instead of multiplying. Three groups of 3 oxygen atoms is 3 &times; 3.",
   "This counts every atom inside the parentheses (1 N + 3 O = 4) and multiplies by 3. The question asks only for oxygen atoms."],
  "Find the oxygen inside the parentheses, then ask what the subscript outside the parentheses does.",
  "In {Al(NO3)3}, the subscript 3 outside the parentheses multiplies everything inside: 3 N atoms and 3 &times; 3 = <b>9 O atoms</b>, plus 1 Al atom.", 1)

Q(T, "Ammonium sulfate, {(NH4)2SO4}, is a nitrogen fertilizer used on many Valley farms. How many atoms <b>in total</b> are in one formula unit?",
  ["15", "10", "20", "4"],
  ["N: 1 &times; 2 = 2. H: 4 &times; 2 = 8. S: 1. O: 4. Total 2 + 8 + 1 + 4 = 15.",
   "This counts the ammonium group only once (1 N + 4 H + 1 S + 4 O). The subscript 2 after the parentheses doubles the N and the H.",
   "This doubles the sulfate as well. The 2 belongs to the parentheses around NH<sub>4</sub>; the S and O come after it and are not multiplied.",
   "This is the number of different elements (N, H, S and O), not the number of atoms."],
  "Multiply only what is inside the parentheses by the subscript after them; then add everything up.",
  "N: 2; H: 4 &times; 2 = 8; S: 1; O: 4. Total = <b>15 atoms</b>. The sulfate group is outside the parentheses, so it is counted once.", 2)

Q(T, "Tooth enamel is mostly hydroxyapatite, {Ca10(PO4)6(OH)2}. How many <b>oxygen</b> atoms are in one formula unit?",
  ["26", "24", "25", "5"],
  ["The six phosphate groups hold 6 &times; 4 = 24 O atoms, and the two hydroxide groups hold 2 &times; 1 = 2 more: 24 + 2 = 26.",
   "This counts the oxygen in the phosphate groups but leaves out the oxygen in the two hydroxide groups.",
   "This counts the hydroxide oxygen only once. The subscript 2 after (OH) means two hydroxide groups, so two O atoms.",
   "This adds the oxygen subscripts inside the parentheses (4 + 1) without multiplying by the subscripts outside them."],
  "Oxygen appears in two different sets of parentheses. Count each set separately.",
  "Phosphate: 6 &times; 4 = 24 O. Hydroxide: 2 &times; 1 = 2 O. Total = <b>26 O atoms</b> (along with 10 Ca, 6 P and 2 H).", 3)

Q(T, "During exercise, muscle cells break down glucose, {C6H12O6}. How many <b>carbon</b> atoms are in 2 {C6H12O6} (two glucose molecules)?",
  ["12", "6", "8", "2"],
  ["The coefficient 2 counts whole molecules, and each molecule has 6 C atoms: 2 &times; 6 = 12.",
   "This is the carbon count for one molecule. The coefficient 2 in front means two molecules.",
   "This adds the coefficient and the subscript (2 + 6). A coefficient multiplies every atom in the formula.",
   "This counts the molecules, not the carbon atoms in them."],
  "A coefficient in front of a formula multiplies every atom in it.",
  "One {C6H12O6} molecule has 6 C atoms, so 2 {C6H12O6} has 2 &times; 6 = <b>12 C atoms</b> (and 24 H, 12 O).", 2)

Q(T, "Which of these elements exists as a <b>diatomic</b> molecule (two atoms bonded together) when it is uncombined?",
  ["iodine", "argon", "calcium", "carbon"],
  ["Iodine is one of the seven diatomic elements (H<sub>2</sub>, N<sub>2</sub>, O<sub>2</sub>, F<sub>2</sub>, Cl<sub>2</sub>, Br<sub>2</sub>, I<sub>2</sub>), so uncombined iodine is written I<sub>2</sub>.",
   "Argon is a noble gas; its atoms stay single and are written Ar.",
   "Calcium is a metal and is written as the single symbol Ca.",
   "Carbon is not on the list of seven diatomic elements; it is written as the single symbol C."],
  "Find the \"7\" shape on the periodic table that starts at element 7, and add hydrogen.",
  "The diatomic elements are H<sub>2</sub>, N<sub>2</sub>, O<sub>2</sub>, F<sub>2</sub>, Cl<sub>2</sub>, Br<sub>2</sub> and I<sub>2</sub>. Of these choices, only <b>iodine</b> (I<sub>2</sub>) is on the list.", 1)

Q(T, "A patient receives supplemental oxygen from a tank. The gas in the tank is uncombined (elemental) oxygen. Which formula represents it?",
  ["{O2}", "{O}", "2O", "{O^2-}"],
  ["Oxygen is diatomic: uncombined oxygen is made of O<sub>2</sub> molecules, two O atoms bonded together.",
   "A single O is one oxygen atom. Oxygen gas is not made of single atoms; it is one of the seven diatomic elements.",
   "2O means two separate oxygen atoms. In oxygen gas the two atoms are bonded into one molecule, shown with a subscript.",
   "This is the oxide ion, which has gained two electrons. It exists only in ionic compounds, not in a gas tank."],
  "Is oxygen on the list of diatomic elements? How is a bonded pair of atoms written?",
  "Oxygen is one of the seven diatomic elements, so the gas in the tank is <b>O<sub>2</sub></b>. Writing O instead of O<sub>2</sub> is a common mistake.", 1)

Q(T, "Which compound is <b>ionic</b> even though every element in it is a nonmetal?",
  ["{NH4Cl}", "{NCl3}", "{HCl(aq)}", "{CCl4}"],
  ["NH<sub>4</sub>Cl starts with the ammonium ion, NH<sub>4</sub><sup>+</sup>, so it is made of NH<sub>4</sub><sup>+</sup> and Cl<sup>" + M + "</sup> ions: ionic.",
   "N and Cl are both nonmetals and the formula has no ammonium ion, so this is a molecular compound (nitrogen trichloride).",
   "This formula starts with H and is dissolved in water, so it is an acid (hydrochloric acid).",
   "C and Cl are both nonmetals sharing electrons, so this is a molecular compound (carbon tetrachloride)."],
  "One cation in this course contains no metal at all.",
  "A formula that starts with a metal <i>or with NH<sub>4</sub></i> is ionic. <b>NH<sub>4</sub>Cl</b> contains ammonium ions and chloride ions, so it is ionic even though N, H and Cl are all nonmetals.", 2)

Q(T, "Which of these is an <b>acid</b>?",
  ["{HBr(aq)}", "{NaOH}", "{CH4}", "{NH4Br}"],
  ["HBr(aq) starts with H and is dissolved in water, where it releases H<sup>+</sup> ions: an acid.",
   "NaOH starts with the metal sodium and ends in OH, the hydroxide ion. It is ionic (sodium hydroxide), not an acid.",
   "CH<sub>4</sub> contains hydrogen, but its formula starts with C. It is a molecular compound (methane), not an acid.",
   "NH<sub>4</sub>Br starts with the ammonium ion, so it is ionic (ammonium bromide)."],
  "Look at the first symbol in each formula, and at whether it is dissolved in water.",
  "Acids have formulas that <i>start</i> with H and release H<sup>+</sup> in water. <b>HBr(aq)</b> is hydrobromic acid. A formula that ends in OH after a metal is a hydroxide, not an acid.", 2)

Q(T, "Which of these compounds is <b>molecular</b>?",
  ["{N2O}", "{Na2O}", "{ZnO}", "{Al2O3}"],
  ["N and O are both nonmetals, so they share electrons and form molecules: N<sub>2</sub>O is molecular (the dental gas nitrous oxide).",
   "Na is a metal (group 1), so Na<sub>2</sub>O is made of Na<sup>+</sup> and O<sup>2" + M + "</sup> ions: ionic.",
   "Zn is a metal, so ZnO is made of Zn<sup>2+</sup> and O<sup>2" + M + "</sup> ions: ionic.",
   "Al is a metal, so Al<sub>2</sub>O<sub>3</sub> is made of Al<sup>3+</sup> and O<sup>2" + M + "</sup> ions: ionic."],
  "Find the staircase line on the periodic table. Which first element is to its right?",
  "Molecular compounds contain only nonmetals. Na, Zn and Al are metals, so their oxides are ionic; <b>N<sub>2</sub>O</b> contains only nitrogen and oxygen, so it is molecular.", 1)

Q(T, "Magnesium hydroxide, {Mg(OH)2}, is the active ingredient in milk of magnesia. How is it classified?",
  ["Ionic, because its formula starts with a metal",
   "An acid, because its formula contains H",
   "Molecular, because O and H are nonmetals",
   "Molecular, because it has parentheses"],
  ["Mg is a group 2 metal, so this compound is made of Mg<sup>2+</sup> ions and hydroxide ions, OH<sup>" + M + "</sup>.",
   "An acid's formula <i>starts</i> with H. Here H is part of the hydroxide ion, OH<sup>" + M + "</sup>, after a metal; hydroxides are not acids.",
   "O and H are nonmetals, but they are bonded together as the hydroxide <i>ion</i>, which pairs with the metal ion Mg<sup>2+</sup>.",
   "Parentheses show that there is more than one of a polyatomic ion; they appear in ionic formulas all the time."],
  "Look at the first symbol in the formula. Is it left or right of the staircase?",
  "The formula starts with the metal Mg, so it is <b>ionic</b>: one Mg<sup>2+</sup> ion and two OH<sup>" + M + "</sup> (hydroxide) ions. A formula that ends in OH after a metal is a hydroxide, not an acid.", 1)

# ======================= ch04-ionicformula (12) =======================
T = 'ch04-ionicformula'
Q(T, "What is the formula of the ionic compound formed by <b>calcium and nitrogen</b>?",
  ["{Ca3N2}", "{Ca2N3}", "{CaN}", "{N2Ca3}"],
  ["Ca<sup>2+</sup> and N<sup>3" + M + "</sup>: swap the charge numbers and drop them, giving Ca<sub>3</sub>N<sub>2</sub>. Check: 3(2+) + 2(3" + M + ") = 0.",
   "This gives each ion its <i>own</i> charge as its subscript. In swap-drop, each charge number goes to the <i>other</i> ion. Check: 2(2+) + 3(3" + M + ") is not zero.",
   "This ignores the charges. One Ca<sup>2+</sup> and one N<sup>3" + M + "</sup> leave a 1" + M + " charge, so the compound would not be neutral.",
   "The subscripts are right, but the cation always comes first in an ionic formula."],
  "Write each ion with its charge first. Calcium is in group 2; nitrogen is in group 15.",
  "Ca<sup>2+</sup> and N<sup>3" + M + "</sup>. Swap-drop gives <b>Ca<sub>3</sub>N<sub>2</sub></b>; 3 &times; 2 = 6 and 2 &times; 3 = 6, so the charges cancel and no reducing is needed.", 1)

Q(T, "What is the formula of <b>barium sulfide</b>?",
  ["{BaS}", "{Ba2S2}", "{BaS2}", "{BaSO4}"],
  ["Ba<sup>2+</sup> and S<sup>2" + M + "</sup> have equal and opposite charges, so they combine 1 : 1.",
   "Swap-drop gives Ba<sub>2</sub>S<sub>2</sub>, but the last step is to reduce: 2 : 2 is 1 : 1.",
   "One Ba<sup>2+</sup> and two S<sup>2" + M + "</sup> give 2+ + 4" + M + " = 2" + M + "; the compound would not be neutral.",
   "This is barium sulfate. Sulfide (-ide) is the single ion S<sup>2" + M + "</sup>; sulfate (-ate) is SO<sub>4</sub><sup>2" + M + "</sup>."],
  "After you swap and drop, there is one more step.",
  "Ba<sup>2+</sup> and S<sup>2" + M + "</sup>: swap-drop gives Ba<sub>2</sub>S<sub>2</sub>, which reduces to <b>BaS</b>. Ions with charges 2+ and 2" + M + " always combine 1 : 1.", 1)

Q(T, "Dental air-abrasion units blast tiny particles of <b>aluminum oxide</b> at a tooth surface. What is the formula of aluminum oxide?",
  ["{Al2O3}", "{Al3O2}", "{AlO}", "{AlO3}"],
  ["Al<sup>3+</sup> and O<sup>2" + M + "</sup>: swap-drop gives Al<sub>2</sub>O<sub>3</sub>. Check: 2(3+) + 3(2" + M + ") = 6+ + 6" + M + " = 0.",
   "This puts each ion's own charge on itself. Check: 3(3+) + 2(2" + M + ") = 5+, not zero.",
   "One Al<sup>3+</sup> and one O<sup>2" + M + "</sup> leave a 1+ charge, so the compound would not be neutral.",
   "This gives oxygen the 3 from aluminum but never gives aluminum the 2 from oxygen; swap both numbers."],
  "Aluminum is a fixed-charge metal. What charge does it carry, and what charge does oxide carry?",
  "Al<sup>3+</sup> and O<sup>2" + M + "</sup>. Swap-drop: <b>Al<sub>2</sub>O<sub>3</sub></b>. The 2 and 3 have no common factor, so the formula is already reduced.", 1)

Q(T, "What is the formula of <b>magnesium phosphate</b>?",
  ["{Mg3(PO4)2}", "{Mg3PO42}", "{Mg2(PO4)3}", "{MgPO4}"],
  ["Mg<sup>2+</sup> and PO<sub>4</sub><sup>3" + M + "</sup>: swap-drop gives 3 Mg and 2 phosphate groups. Two phosphates need parentheses: Mg<sub>3</sub>(PO<sub>4</sub>)<sub>2</sub>.",
   "The ratio is right, but without parentheses the 2 runs into the 4 and reads as \"42 oxygen atoms.\" Put the phosphate in parentheses.",
   "This gives each ion its own charge as its subscript. Check: 2(2+) + 3(3" + M + ") = 5" + M + ", not zero.",
   "One Mg<sup>2+</sup> and one PO<sub>4</sub><sup>3" + M + "</sup> leave a 1" + M + " charge."],
  "Treat phosphate as one unit. If you need more than one, what must go around it?",
  "Mg<sup>2+</sup> and PO<sub>4</sub><sup>3" + M + "</sup>. Swap-drop: 3 Mg and 2 PO<sub>4</sub>, written <b>Mg<sub>3</sub>(PO<sub>4</sub>)<sub>2</sub></b>. Check: 3(2+) + 2(3" + M + ") = 0.", 2)

Q(T, "Lithium carbonate is a medication used to treat bipolar disorder. What is its formula?",
  ["{Li2CO3}", "{LiCO3}", "{Li(CO3)2}", "{Li2(CO3)2}"],
  ["Li<sup>+</sup> and CO<sub>3</sub><sup>2" + M + "</sup>: it takes two Li<sup>+</sup> ions to cancel one 2" + M + " carbonate. One carbonate needs no parentheses.",
   "One Li<sup>+</sup> and one CO<sub>3</sub><sup>2" + M + "</sup> leave a 1" + M + " charge. Lithium is in group 1, so it is only 1+.",
   "This puts the 2 on the wrong ion: one Li<sup>+</sup> and two carbonates give 1+ + 4" + M + " = 3" + M + ".",
   "Two Li<sup>+</sup> and two CO<sub>3</sub><sup>2" + M + "</sup> give 2+ + 4" + M + " = 2" + M + ". Only one carbonate is needed."],
  "Lithium is in group 1. How many 1+ ions cancel one 2" + M + " ion?",
  "Li<sup>+</sup> and CO<sub>3</sub><sup>2" + M + "</sup>: swap-drop gives <b>Li<sub>2</sub>CO<sub>3</sub></b>. Check: 2(1+) + (2" + M + ") = 0. (Context only; not dosing information.)", 1)

Q(T, "What is the formula of <b>ammonium sulfide</b>?",
  ["{(NH4)2S}", "{NH42S}", "{NH4S}", "{(NH4)2SO4}"],
  ["NH<sub>4</sub><sup>+</sup> and S<sup>2" + M + "</sup>: two ammonium ions cancel one sulfide. Two ammonium ions need parentheses: (NH<sub>4</sub>)<sub>2</sub>S.",
   "Without parentheses, the 2 runs into the 4 and reads as \"42 hydrogen atoms.\" Put ammonium in parentheses.",
   "One NH<sub>4</sub><sup>+</sup> and one S<sup>2" + M + "</sup> leave a 1" + M + " charge.",
   "This is ammonium sulfate. Sulfide (-ide) is S<sup>2" + M + "</sup> alone; sulfate (-ate) is SO<sub>4</sub><sup>2" + M + "</sup>."],
  "Treat ammonium as one unit, and check the ending of the anion name.",
  "NH<sub>4</sub><sup>+</sup> and S<sup>2" + M + "</sup>. Swap-drop gives 2 ammonium and 1 sulfide: <b>(NH<sub>4</sub>)<sub>2</sub>S</b>. Check: 2(1+) + (2" + M + ") = 0.", 2)

Q(T, "Chromium(III) ions combine with hydroxide ions. What is the formula of the compound?",
  ["{Cr(OH)3}", "{CrOH3}", "{Cr3OH}", "{Cr(OH)2}"],
  ["Cr<sup>3+</sup> and OH<sup>" + M + "</sup>: three hydroxide ions cancel one Cr<sup>3+</sup>, and three hydroxides need parentheses.",
   "Without parentheses, the 3 applies only to H, so this would mean one O and three H atoms. The 3 should count whole OH groups.",
   "This puts the 3 on chromium. Three Cr<sup>3+</sup> and one OH<sup>" + M + "</sup> give 9+ + 1" + M + ", not zero.",
   "Two hydroxides would balance a 2+ ion. The Roman numeral III says this chromium ion is 3+."],
  "The Roman numeral tells you the charge of the chromium ion.",
  "Cr<sup>3+</sup> and OH<sup>" + M + "</sup>. Swap-drop gives 1 Cr and 3 OH: <b>Cr(OH)<sub>3</sub></b>. Check: (3+) + 3(1" + M + ") = 0.", 2)

Q(T, "What is the charge on each <b>cobalt</b> ion in {Co2O3}?",
  ["3+", "2+", "6+", "3" + M],
  ["Three O<sup>2" + M + "</sup> ions give 3(2" + M + ") = 6" + M + ". Two cobalt ions share 6+, so each is 3+.",
   "This reads the subscript 2 as the charge. Subscripts count ions; the charge has to be worked out from the anions.",
   "6+ is the total positive charge of both cobalt ions together. Divide by the 2 cobalt ions.",
   "The cobalt ion is the cation in this compound, so its charge is positive."],
  "Find the total negative charge from the oxide ions, then share it among the metal ions.",
  "Total negative charge: 3 &times; (2" + M + ") = 6" + M + ". The two Co ions must carry 6+ together, so each is <b>Co<sup>3+</sup></b>. Check: 2(3+) + 3(2" + M + ") = 0.", 2)

Q(T, "What is the charge on each <b>iron</b> ion in {Fe3(PO4)2}?",
  ["2+", "3+", "6+", "3" + M],
  ["Two phosphate ions give 2(3" + M + ") = 6" + M + ". Three iron ions share 6+, so each is 2+.",
   "This reads the subscript 3 as the charge. The 3 counts iron ions; work out the charge from the phosphates.",
   "6+ is the total for all three iron ions. Divide by 3.",
   "3" + M + " is the charge of the phosphate ion, the anion. Iron is the cation, so its charge is positive."],
  "Phosphate is 3" + M + ". How much negative charge do two of them carry?",
  "Total negative charge: 2 &times; (3" + M + ") = 6" + M + ". Three Fe ions carry 6+ together, so each is <b>Fe<sup>2+</sup></b>. Check: 3(2+) + 2(3" + M + ") = 0.", 3)

Q(T, "Calcium oxalate, {CaC2O4}, is the most common compound in kidney stones. The calcium ion is Ca<sup>2+</sup>. What is the charge of the oxalate ion?",
  ["2" + M, "4" + M, "1" + M, "2+"],
  ["One Ca<sup>2+</sup> pairs with one oxalate ion, so the oxalate ion must carry 2" + M + " to make the total zero.",
   "This reads the subscript 4 on O as the charge. Subscripts inside a polyatomic ion count its atoms, not its charge.",
   "One Ca<sup>2+</sup> with a 1" + M + " ion would leave a 1+ charge; the formula would need two oxalates.",
   "Oxalate is the anion here, so its charge is negative."],
  "The total charge of the formula unit is zero, and there is one of each ion.",
  "Ca<sup>2+</sup> + oxalate = 0, so oxalate is <b>2" + M + "</b>: C<sub>2</sub>O<sub>4</sub><sup>2" + M + "</sup>, as on the green sheet.", 2)

Q(T, "The table pairs each cation with each anion and gives the formula of the compound they form. Which formula belongs in the cell marked ?",
  ["{AlPO4}", "{Al3(PO4)3}", "{Al2(PO4)3}", "{Al(PO4)3}"],
  ["Al<sup>3+</sup> and PO<sub>4</sub><sup>3" + M + "</sup> have equal and opposite charges, so they combine 1 : 1.",
   "Swap-drop gives Al<sub>3</sub>(PO<sub>4</sub>)<sub>3</sub>, but 3 : 3 must be reduced to 1 : 1.",
   "This copies the pattern from the sulfate column. Check: 2(3+) + 3(3" + M + ") = 3" + M + ", not zero.",
   "One Al<sup>3+</sup> and three PO<sub>4</sub><sup>3" + M + "</sup> give 3+ + 9" + M + " = 6" + M + "."],
  "Compare the charges of the two ions. What happens when they are equal and opposite?",
  "Al<sup>3+</sup> and PO<sub>4</sub><sup>3" + M + "</sup>: swap-drop gives Al<sub>3</sub>(PO<sub>4</sub>)<sub>3</sub>, which reduces to <b>AlPO<sub>4</sub></b>. No parentheses are needed for one phosphate.", 2,
  [{"type": "table", "cap": "Formulas of ionic compounds", "head": ["Cation", "{SO4^2-}", "{PO4^3-}"],
    "rows": [["{Na^+}", "{Na2SO4}", "{Na3PO4}"], ["{Mg^2+}", "{MgSO4}", "{Mg3(PO4)2}"], ["{Al^3+}", "{Al2(SO4)3}", "?"]]}])

Q(T, "For a barium swallow X-ray, a patient drinks a suspension of <b>barium sulfate</b>. What is its formula?",
  ["{BaSO4}", "{Ba(SO4)2}", "{Ba2SO4}", "{BaS}"],
  ["Ba<sup>2+</sup> and SO<sub>4</sub><sup>2" + M + "</sup> have equal and opposite charges, so they combine 1 : 1.",
   "One Ba<sup>2+</sup> and two SO<sub>4</sub><sup>2" + M + "</sup> give 2+ + 4" + M + " = 2" + M + ".",
   "Two Ba<sup>2+</sup> and one SO<sub>4</sub><sup>2" + M + "</sup> give 4+ + 2" + M + " = 2+.",
   "This is barium sulfide. Sulfate (-ate) is the polyatomic ion SO<sub>4</sub><sup>2" + M + "</sup>; sulfide (-ide) is S<sup>2" + M + "</sup>."],
  "Barium is in group 2. Find the charge of sulfate on the green sheet.",
  "Ba<sup>2+</sup> and SO<sub>4</sub><sup>2" + M + "</sup>: swap-drop gives Ba<sub>2</sub>(SO<sub>4</sub>)<sub>2</sub>, which reduces to <b>BaSO<sub>4</sub></b>. Barium sulfate is almost insoluble, which is why it can be swallowed safely while soluble barium compounds are poisonous.", 1)

# ======================= ch04-polyatomic (10) =======================
T = 'ch04-polyatomic'
Q(T, "In an infant's body, nitrate from well water can be converted to the <b>nitrite</b> ion. What is the formula of the nitrite ion?",
  ["{NO2^-}", "{NO3^-}", "{NO2^2-}", "{N^3-}"],
  ["Nitrate is NO<sub>3</sub><sup>" + M + "</sup>. The -ite ion has one fewer O and the same charge: NO<sub>2</sub><sup>" + M + "</sup>.",
   "This is nitrate, the -ate ion. Nitrite has one fewer oxygen atom.",
   "Removing an O atom does not change the charge. Nitrate and nitrite are both 1" + M + ".",
   "This is nitride, the -ide ion: a single N atom with no oxygen."],
  "Start from nitrate. What does -ite change, and what does it leave alone?",
  "Nitrate is NO<sub>3</sub><sup>" + M + "</sup>; -ite means one fewer O with the same charge, so nitrite is <b>NO<sub>2</sub><sup>" + M + "</sup></b>.", 1)

Q(T, "What is the name of the ion {ClO2^-}?",
  ["chlorite", "chlorine dioxide", "chlorate", "hypochlorite"],
  ["Chlorate is ClO<sub>3</sub><sup>" + M + "</sup>. One fewer O, with the same 1" + M + " charge, is the -ite ion: ClO<sub>2</sub><sup>" + M + "</sup>.",
   "Chlorine dioxide is the neutral <i>molecule</i> ClO<sub>2</sub>. The charge on ClO<sub>2</sub><sup>" + M + "</sup> makes it a polyatomic ion with its own name.",
   "Chlorate has three O atoms (ClO<sub>3</sub><sup>" + M + "</sup>); this ion has two.",
   "The hypo- ion has only one O atom (ClO<sup>" + M + "</sup>, the ion in bleach)."],
  "Start from chlorate, ClO<sub>3</sub><sup>" + M + "</sup>, and count oxygen atoms.",
  "Chlorine oxyanions: ClO<sub>4</sub><sup>" + M + "</sup> perchlorate, ClO<sub>3</sub><sup>" + M + "</sup> chlorate, ClO<sub>2</sub><sup>" + M + "</sup> <b>chlorite</b>, ClO<sup>" + M + "</sup> hypochlorite. The charge tells you it is an ion, not the molecule ClO<sub>2</sub>.", 1)

Q(T, "Iodate is {IO3^-}. What is the formula of the <b>periodate</b> ion?",
  ["{IO4^-}", "{IO3^-}", "{IO2^-}", "{I^-}"],
  ["Per-...-ate means one more O than the -ate ion, with the same charge: IO<sub>4</sub><sup>" + M + "</sup>.",
   "This is iodate itself. The prefix per- adds one O atom.",
   "This has one fewer O than iodate, which is the -ite ion (iodite).",
   "This is iodide, the -ide ion, with no oxygen."],
  "Iodine's oxyanions follow the same pattern as chlorine's. What does per- do?",
  "Per-...-ate = one more O than -ate, same charge. Iodate is IO<sub>3</sub><sup>" + M + "</sup>, so periodate is <b>IO<sub>4</sub><sup>" + M + "</sup></b>.", 2)

Q(T, "Sulfate is {SO4^2-}. What is the formula of the <b>sulfite</b> ion?",
  ["{SO3^2-}", "{SO3^-}", "{S^2-}", "{SO2^2-}"],
  ["-ite means one fewer O than the -ate ion, with the same charge: SO<sub>3</sub><sup>2" + M + "</sup>.",
   "Removing an O atom does not change the charge. Sulfate and sulfite are both 2" + M + ".",
   "This is sulfide, the -ide ion, with no oxygen.",
   "This removes two O atoms. -ite means one fewer O than -ate."],
  "-ite changes the number of oxygen atoms. Does it change the charge?",
  "Sulfate SO<sub>4</sub><sup>2" + M + "</sup> loses one O to give sulfite, <b>SO<sub>3</sub><sup>2" + M + "</sup></b>. The charge stays 2" + M + ".", 1)

Q(T, "What is the formula of the <b>hydrogen phosphate</b> ion?",
  ["{HPO4^2-}", "{HPO4^3-}", "{H2PO4^-}", "{HPO4^4-}"],
  ["Phosphate is PO<sub>4</sub><sup>3" + M + "</sup>. Adding one H<sup>+</sup> raises the charge by one: 3" + M + " + 1 = 2" + M + ".",
   "Adding H<sup>+</sup> changes the charge. Each H<sup>+</sup> cancels one negative charge, so 3" + M + " becomes 2" + M + ".",
   "This has two H atoms: it is dihydrogen phosphate.",
   "Adding a positive H<sup>+</sup> makes the ion less negative, not more."],
  "Start from phosphate, PO<sub>4</sub><sup>3" + M + "</sup>. What does adding H<sup>+</sup> do to the charge?",
  "PO<sub>4</sub><sup>3" + M + "</sup> + H<sup>+</sup> gives <b>HPO<sub>4</sub><sup>2" + M + "</sup></b>, hydrogen phosphate. Each added H<sup>+</sup> lowers the negative charge by one.", 2)

Q(T, "An arterial blood gas report lists the level of {HCO3^-} in the blood. What is the name of this ion?",
  ["hydrogen carbonate", "carbonate", "carbonic acid", "hydrogen carbonite"],
  ["HCO<sub>3</sub><sup>" + M + "</sup> is carbonate (CO<sub>3</sub><sup>2" + M + "</sup>) with one H<sup>+</sup> added; its older name is bicarbonate.",
   "Carbonate is CO<sub>3</sub><sup>2" + M + "</sup>, with no H and a 2" + M + " charge.",
   "Carbonic acid is the neutral compound H<sub>2</sub>CO<sub>3</sub>. This species has one H and a 1" + M + " charge, so it is an ion.",
   "Adding H does not change -ate to -ite. The -ite ending means one fewer oxygen atom, and this ion still has three."],
  "Which green-sheet ion is this, once you take away the H<sup>+</sup>?",
  "Remove the H<sup>+</sup> and you have carbonate, CO<sub>3</sub><sup>2" + M + "</sup>. With one H added, the ion is <b>hydrogen carbonate</b>, also called bicarbonate, the \"bicarb\" on a blood gas report.", 1)

Q(T, "IV potassium phosphate contains the <b>dihydrogen phosphate</b> ion. What is its formula?",
  ["{H2PO4^-}", "{H2PO4^3-}", "{HPO4^2-}", "{H2PO3^-}"],
  ["Phosphate is PO<sub>4</sub><sup>3" + M + "</sup>. Two added H<sup>+</sup> ions raise the charge by two: 3" + M + " + 2 = 1" + M + ".",
   "Adding H<sup>+</sup> changes the charge. Two H<sup>+</sup> make the 3" + M + " ion only 1" + M + ".",
   "This has only one H: it is hydrogen phosphate.",
   "This has only three O atoms, so it is built on phosphite (PO<sub>3</sub><sup>3" + M + "</sup>), not phosphate."],
  "Di- means two. Start from phosphate and add two H<sup>+</sup>.",
  "PO<sub>4</sub><sup>3" + M + "</sup> + 2 H<sup>+</sup> gives <b>H<sub>2</sub>PO<sub>4</sub><sup>" + M + "</sup></b>, dihydrogen phosphate. (Context only; not dosing information.)", 2)

Q(T, "Which pair of ions has the <b>same charge</b>?",
  ["nitrate and nitrite", "nitrate and nitride", "sulfate and phosphate", "carbonate and hydrogen carbonate"],
  ["-ate and -ite ions of the same element differ only in the number of oxygen atoms; both nitrate and nitrite are 1" + M + ".",
   "Nitride is the monatomic N<sup>3" + M + "</sup> ion; nitrate is 1" + M + ".",
   "Sulfate is 2" + M + " and phosphate is 3" + M + ".",
   "Carbonate is 2" + M + "; adding H<sup>+</sup> makes hydrogen carbonate 1" + M + "."],
  "Which change keeps the charge the same: changing the number of O atoms, or adding H<sup>+</sup>?",
  "Changing -ate to -ite (one fewer O) never changes the charge, so <b>nitrate (NO<sub>3</sub><sup>" + M + "</sup>) and nitrite (NO<sub>2</sub><sup>" + M + "</sup>)</b> are both 1" + M + ". Adding H<sup>+</sup> or switching to an -ide ion does change it.", 1)

Q(T, "What is the formula of the <b>acetate</b> ion?",
  ["{C2H3O2^-}", "{C2O4^2-}", "{C2H3O2^+}", "{CO3^2-}"],
  ["Acetate, from the green sheet, is C<sub>2</sub>H<sub>3</sub>O<sub>2</sub><sup>" + M + "</sup> (also written CH<sub>3</sub>COO<sup>" + M + "</sup>), the ion from vinegar's acetic acid.",
   "This is oxalate, the other two-carbon ion on the green sheet.",
   "Acetate is an anion, so its charge is negative.",
   "This is carbonate, which has one carbon atom and no hydrogen."],
  "Acetate has two carbon atoms and a 1" + M + " charge.",
  "Acetate is <b>C<sub>2</sub>H<sub>3</sub>O<sub>2</sub><sup>" + M + "</sup></b>. Oxalate, C<sub>2</sub>O<sub>4</sub><sup>2" + M + "</sup>, is easy to mix up with it.", 1)

Q(T, "The table lists the bromine oxyanions. Which name belongs in the cell marked ?",
  ["bromite", "hypobromite", "perbromate", "bromide"],
  ["BrO<sub>2</sub><sup>" + M + "</sup> has one fewer O than bromate (BrO<sub>3</sub><sup>" + M + "</sup>), so it is the -ite ion.",
   "Hypo-...-ite has two fewer O than -ate: BrO<sup>" + M + "</sup>, which is already in the table.",
   "Per-...-ate has one more O than -ate: BrO<sub>4</sub><sup>" + M + "</sup>, already in the table.",
   "Bromide is Br<sup>" + M + "</sup>, with no oxygen at all."],
  "Compare the missing ion with bromate. One more or one fewer oxygen?",
  "BrO<sub>4</sub><sup>" + M + "</sup> perbromate, BrO<sub>3</sub><sup>" + M + "</sup> bromate, BrO<sub>2</sub><sup>" + M + "</sup> <b>bromite</b>, BrO<sup>" + M + "</sup> hypobromite. Bromine follows the same pattern as chlorine.", 2,
  [{"type": "table", "cap": "Bromine oxyanions", "head": ["Formula", "Name"],
    "rows": [["{BrO4^-}", "perbromate"], ["{BrO3^-}", "bromate"], ["{BrO2^-}", "?"], ["{BrO^-}", "hypobromite"]]}])

# ======================= ch04-ionicname (14) =======================
T = 'ch04-ionicname'
Q(T, "What is the name of {K2S}?",
  ["potassium sulfide", "dipotassium sulfide", "potassium(I) sulfide", "potassium sulfate"],
  ["K is in group 1 (fixed charge, 1+), so no Roman numeral is needed, and S<sup>2" + M + "</sup> is sulfide.",
   "Ionic names never use prefixes. The charges already fix the ratio of K<sup>+</sup> to S<sup>2" + M + "</sup>.",
   "Potassium always forms K<sup>+</sup>, so its name never needs a Roman numeral.",
   "Sulfate is SO<sub>4</sub><sup>2" + M + "</sup>. A single S atom is the -ide ion."],
  "Is potassium on the fixed-charge list? Is the anion one atom or a polyatomic ion?",
  "Cation name + anion name: <b>potassium sulfide</b>. Group 1 metals never get Roman numerals, and ionic names never use prefixes.", 1)

Q(T, "What is the name of {AgCl}?",
  ["silver chloride", "silver(I) chloride", "silver chlorine", "monosilver monochloride"],
  ["Silver is on the fixed-charge list (always Ag<sup>+</sup>), so it needs no Roman numeral; Cl<sup>" + M + "</sup> is chloride.",
   "Silver forms only Ag<sup>+</sup> in this course, so a Roman numeral is not used.",
   "The anion needs the -ide ending: chlorine becomes chloride.",
   "Prefixes are for molecular compounds. Silver is a metal, so this is ionic."],
  "Check the fixed-charge list: groups 1 and 2, Al, Zn and Ag.",
  "Ag is a fixed-charge metal (Ag<sup>+</sup>), so the name is simply <b>silver chloride</b>.", 1)

Q(T, "What is the name of {Cu2O}?",
  ["copper(I) oxide", "copper(II) oxide", "dicopper oxide", "copper oxide"],
  ["One O<sup>2" + M + "</sup> is shared by two copper ions, so each is Cu<sup>+</sup>: copper(I).",
   "The 2 is the number of copper ions, not their charge. 2 Cu share a 2" + M + " charge, so each is 1+.",
   "Ionic names do not use prefixes. Copper's charge goes in a Roman numeral.",
   "Copper forms two ions, so the name must say which one is present."],
  "Find the total negative charge, then divide by the number of copper ions.",
  "O<sup>2" + M + "</sup> = 2" + M + ", shared by 2 Cu, so each is Cu<sup>+</sup>: <b>copper(I) oxide</b> (older name cuprous oxide). The Roman numeral is the charge, not the subscript.", 2)

Q(T, "What is the name of {Co(NO3)2}?",
  ["cobalt(II) nitrate", "cobalt nitrate", "cobalt(II) nitrite", "cobalt(III) nitrate"],
  ["Two NO<sub>3</sub><sup>" + M + "</sup> give 2" + M + ", so the single cobalt ion is Co<sup>2+</sup>; NO<sub>3</sub><sup>" + M + "</sup> is nitrate.",
   "Cobalt forms both Co<sup>2+</sup> and Co<sup>3+</sup>, so the name needs a Roman numeral.",
   "NO<sub>3</sub><sup>" + M + "</sup> is nitrate. Nitrite has only two O atoms (NO<sub>2</sub><sup>" + M + "</sup>).",
   "The 3 in NO<sub>3</sub> counts oxygen atoms inside the nitrate ion; it is not cobalt's charge. Two 1" + M + " nitrates make 2" + M + "."],
  "Nitrate is 1" + M + ". How many nitrates are there?",
  "2 NO<sub>3</sub><sup>" + M + "</sup> = 2" + M + ", so cobalt is Co<sup>2+</sup>: <b>cobalt(II) nitrate</b> (older name cobaltous nitrate).", 2)

Q(T, "What is the name of {Cr2(SO4)3}?",
  ["chromium(III) sulfate", "chromium(II) sulfate", "chromium(VI) sulfate", "dichromium trisulfate"],
  ["Three SO<sub>4</sub><sup>2" + M + "</sup> give 6" + M + ", shared by 2 chromium ions, so each is Cr<sup>3+</sup>.",
   "The subscript 2 counts chromium ions. It is not the charge.",
   "6+ is the total charge of both chromium ions. The Roman numeral is the charge of <i>one</i> ion.",
   "Ionic names do not use prefixes; chromium's charge goes in a Roman numeral instead."],
  "Total negative charge first; then divide by the number of chromium ions.",
  "3 &times; (2" + M + ") = 6" + M + ", over 2 Cr ions = 3+ each: <b>chromium(III) sulfate</b> (older name chromic sulfate).", 3)

Q(T, "Ferrous sulfate is a common iron supplement. What is its formula?",
  ["{FeSO4}", "{Fe2(SO4)3}", "{Fe2SO4}", "{FeS}"],
  ["Ferrous is the older name for iron(II), Fe<sup>2+</sup>; with SO<sub>4</sub><sup>2" + M + "</sup> the ions combine 1 : 1.",
   "This is ferric sulfate, iron(III). -ous is the <i>lower</i> charge; -ic is the higher.",
   "Two Fe<sup>2+</sup> and one SO<sub>4</sub><sup>2" + M + "</sup> give 4+ + 2" + M + ", not zero.",
   "This is iron(II) sulfide. Sulfate is the polyatomic ion SO<sub>4</sub><sup>2" + M + "</sup>."],
  "Does -ous mean the lower or the higher charge of iron?",
  "Ferrous = iron(II) = Fe<sup>2+</sup>. Fe<sup>2+</sup> and SO<sub>4</sub><sup>2" + M + "</sup> give <b>FeSO<sub>4</sub></b>. (Context only; not dosing information.)", 2)

Q(T, "Older labels use -ous and -ic names. What is the older name of {CuSO4}?",
  ["cupric sulfate", "cuprous sulfate", "cupric sulfite", "copperic sulfate"],
  ["SO<sub>4</sub><sup>2" + M + "</sup> means copper is Cu<sup>2+</sup>, the higher of copper's two charges, so it takes -ic: cupric.",
   "Cuprous is copper(I), the lower charge. One 2" + M + " sulfate needs Cu<sup>2+</sup>.",
   "SO<sub>4</sub><sup>2" + M + "</sup> is sulfate. Sulfite has three O atoms.",
   "Older names use the Latin root of copper, cupr-."],
  "Find copper's charge first. Is it copper's lower or higher charge?",
  "SO<sub>4</sub><sup>2" + M + "</sup> = 2" + M + ", so Cu<sup>2+</sup>: copper(II) sulfate, or with the older name, <b>cupric sulfate</b>.", 2)

Q(T, "What is the formula of <b>mercurous nitrate</b>?",
  ["{Hg2(NO3)2}", "{HgNO3}", "{Hg(NO3)2}", "{Hg2NO3}"],
  ["Mercurous is mercury(I), which exists as the pair Hg<sub>2</sub><sup>2+</sup>. Two NO<sub>3</sub><sup>" + M + "</sup> cancel its 2+ charge.",
   "There is no single Hg<sup>+</sup> ion. Mercury(I) is always the pair Hg<sub>2</sub><sup>2+</sup>.",
   "This is mercuric nitrate, mercury(II). -ous is the lower charge.",
   "Hg<sub>2</sub><sup>2+</sup> has a 2+ charge, so it needs two nitrates, not one."],
  "Mercury(I) is unusual. How is the mercury(I) ion written?",
  "Mercurous = mercury(I) = Hg<sub>2</sub><sup>2+</sup>. With NO<sub>3</sub><sup>" + M + "</sup>: <b>Hg<sub>2</sub>(NO<sub>3</sub>)<sub>2</sub></b>. Each Hg is 1+, but the ion is the pair.", 3)

Q(T, "Household bleach is a solution of <b>sodium hypochlorite</b>. What is its formula?",
  ["{NaClO}", "{NaClO2}", "{NaCl}", "{Na(ClO)2}"],
  ["Na<sup>+</sup> and hypochlorite, ClO<sup>" + M + "</sup>, combine 1 : 1.",
   "ClO<sub>2</sub><sup>" + M + "</sup> is chlorite. Hypo-...-ite has one fewer O than chlorite.",
   "This is sodium chloride. Hypochlorite contains oxygen.",
   "Na<sup>+</sup> and ClO<sup>" + M + "</sup> have charges of the same size, so only one hypochlorite is needed."],
  "Chlorate is ClO<sub>3</sub><sup>" + M + "</sup>. Hypo-...-ite has two fewer O.",
  "Hypochlorite is ClO<sup>" + M + "</sup>; with Na<sup>+</sup> the formula is <b>NaClO</b>. Never mix bleach with acids or ammonia.", 1)

Q(T, "Ammonium nitrate, {NH4NO3}, is a Valley fertilizer. A student writes four names for it. Which is correct?",
  ["ammonium nitrate", "ammonium nitrite", "ammonia nitrate", "ammonium(I) nitrate"],
  ["NH<sub>4</sub><sup>+</sup> is ammonium and NO<sub>3</sub><sup>" + M + "</sup> is nitrate; ionic names are cation + anion.",
   "Nitrite is NO<sub>2</sub><sup>" + M + "</sup>. This anion has three O atoms.",
   "Ammonia is the neutral molecule NH<sub>3</sub>. The cation NH<sub>4</sub><sup>+</sup> is ammonium.",
   "Ammonium is always 1+, so it never takes a Roman numeral."],
  "Name the cation, then the anion. Count the O atoms in the anion.",
  "NH<sub>4</sub><sup>+</sup> + NO<sub>3</sub><sup>" + M + "</sup> = <b>ammonium nitrate</b>. Watch the spelling: ammonium (the ion), not ammonia (the molecule).", 1)

Q(T, "Humidity-indicator cards turn pink when they absorb water to form {CoCl2.6H2O}. What is its name?",
  ["cobalt(II) chloride hexahydrate", "cobalt chloride hexahydrate", "cobalt(II) dichloride hexahydrate", "cobalt(II) chloride pentahydrate"],
  ["Two Cl<sup>" + M + "</sup> make cobalt Co<sup>2+</sup>, and six waters are hexahydrate.",
   "Cobalt has two possible charges, so the ionic part still needs its Roman numeral.",
   "The prefix goes only on \"hydrate.\" The ionic part is named without prefixes.",
   "Penta- means 5. There are six water molecules here."],
  "Name the ionic part first, then add a Greek prefix to the word hydrate.",
  "2 Cl<sup>" + M + "</sup> = 2" + M + ", so Co<sup>2+</sup>: cobalt(II) chloride. Six H<sub>2</sub>O = hexahydrate: <b>cobalt(II) chloride hexahydrate</b>.", 2)

Q(T, "Zinc sulfate heptahydrate is sprayed on some Valley orchards to correct zinc deficiency. What is its formula?",
  ["{ZnSO4.7H2O}", "{ZnSO4.6H2O}", "{ZnS.7H2O}", "{Zn2SO4.7H2O}"],
  ["Zn<sup>2+</sup> and SO<sub>4</sub><sup>2" + M + "</sup> combine 1 : 1, and hepta- means 7 waters.",
   "Hexa- is 6; hepta- is 7.",
   "This is zinc sulfide. Sulfate is SO<sub>4</sub><sup>2" + M + "</sup>.",
   "Zinc is fixed at 2+, so one Zn<sup>2+</sup> balances one sulfate."],
  "Write the ionic formula first, then a dot and the water count.",
  "Zinc sulfate is ZnSO<sub>4</sub> (Zn<sup>2+</sup>, SO<sub>4</sub><sup>2" + M + "</sup>); hepta = 7, so <b>ZnSO<sub>4</sub>&middot;7H<sub>2</sub>O</b>.", 2)

Q(T, "A student wrote the names in the table. Which row is named correctly?",
  ["Row B", "Row A", "Row C", "Row D"],
  ["FeCl<sub>3</sub>: 3 Cl<sup>" + M + "</sup> = 3" + M + ", so Fe<sup>3+</sup>, and the name in row B shows that charge as III.",
   "Na<sub>2</sub>O is ionic, and ionic names never use prefixes: it is sodium oxide.",
   "Calcium is a fixed-charge metal (group 2), so its name never takes a Roman numeral.",
   "PbO<sub>2</sub>: 2 O<sup>2" + M + "</sup> = 4" + M + ", so the lead ion is Pb<sup>4+</sup>, lead(IV), not lead(II)."],
  "For each row, decide whether the metal has a fixed or a variable charge, then check the Roman numeral and prefixes.",
  "A: sodium oxide (no prefixes). <b>B: iron(III) chloride is correct.</b> C: calcium chloride (no numeral). D: lead(IV) oxide.", 2,
  [{"type": "table", "cap": "A student's names", "head": ["Row", "Formula", "Student's name"],
    "rows": [["A", "{Na2O}", "disodium oxide"], ["B", "{FeCl3}", "iron(III) chloride"], ["C", "{CaCl2}", "calcium(II) chloride"], ["D", "{PbO2}", "lead(II) oxide"]]}])

Q(T, "Calcium supplements and bone mineral contain {Ca3(PO4)2}. What is its name?",
  ["calcium phosphate", "tricalcium diphosphate", "calcium phosphide", "calcium(II) phosphate"],
  ["Ca is group 2 (fixed 2+) and PO<sub>4</sub><sup>3" + M + "</sup> is phosphate. Ionic names are just cation + anion.",
   "Ionic names do not use prefixes; the charges already set the 3 : 2 ratio.",
   "Phosphide is P<sup>3" + M + "</sup>. PO<sub>4</sub><sup>3" + M + "</sup> is phosphate.",
   "Calcium has a fixed charge, so its name never takes a Roman numeral."],
  "Is calcium a fixed-charge metal? Is the anion an -ide ion or a polyatomic ion?",
  "Ca<sup>2+</sup> + PO<sub>4</sub><sup>3" + M + "</sup>: <b>calcium phosphate</b>, with no prefixes and no Roman numeral.", 1)

# ======================= ch04-molecular (10) =======================
T = 'ch04-molecular'
Q(T, "What is the name of {S2Cl2}?",
  ["disulfur dichloride", "sulfur chloride", "disulfur dichlorine", "sulfur dichloride"],
  ["Both elements are nonmetals, so use prefixes: 2 S = disulfur, 2 Cl = dichloride.",
   "S and Cl are nonmetals, so the name must count the atoms with prefixes.",
   "The second element needs the -ide ending: chloride, not chlorine.",
   "Sulfur dichloride is SCl<sub>2</sub>, with one S. This molecule has two S atoms."],
  "Two nonmetals: count each kind of atom and use a prefix for each.",
  "Molecular: prefix + first element, prefix + second element with -ide. 2 S, 2 Cl: <b>disulfur dichloride</b>.", 1)

Q(T, "Eye surgeons sometimes place a bubble of <b>sulfur hexafluoride</b> gas inside the eye after retina repair. What is its formula?",
  ["{SF6}", "{S6F}", "{SF}", "{SF5}"],
  ["No prefix on sulfur means one S; hexa- means 6 F atoms.",
   "The prefix hexa- belongs to fluoride, the second element, so the 6 goes on F.",
   "Prefixes are not optional in molecular names: hexa- says there are six F atoms.",
   "Penta- is 5; hexa- is 6."],
  "Which element does the prefix hexa- belong to?",
  "Sulfur (no prefix, 1 S) hexa- (6) fluoride: <b>SF<sub>6</sub></b>.", 1)

Q(T, "In neonatal intensive care, respiratory therapists can deliver inhaled {NO} to some newborns. What is the systematic name of {NO}?",
  ["nitrogen monoxide", "mononitrogen monoxide", "nitrogen oxide", "nitrous oxide"],
  ["One N and one O: mono- is never used on the first element, but it is used on the second: nitrogen monoxide (often called nitric oxide).",
   "Mono- is never used on the first element.",
   "Without prefixes, the name does not say which nitrogen oxide this is; N and O form several.",
   "Nitrous oxide is the common name of N<sub>2</sub>O, the dental gas, a different molecule."],
  "Mono- appears in one place in this name, but not the other.",
  "<b>Nitrogen monoxide</b>: no mono- on the first element; mono- + oxide (with the o dropped) on the second. Its common name is nitric oxide.", 1)

Q(T, "On hot days the brown haze over the San Joaquin Valley includes <b>nitrogen dioxide</b>. What is its formula?",
  ["{NO2}", "{N2O}", "{NO2^-}", "{N2O4}"],
  ["No prefix on nitrogen means one N; di- means 2 O: NO<sub>2</sub>.",
   "This is dinitrogen monoxide (nitrous oxide): the 2 is on the wrong element.",
   "This is the nitrite ion. Nitrogen dioxide is a neutral molecule with no charge.",
   "This is dinitrogen tetroxide. Molecular formulas give the actual atoms in one molecule; N<sub>2</sub>O<sub>4</sub> and NO<sub>2</sub> are different molecules."],
  "Which element does di- belong to? Does a molecule carry a charge?",
  "Nitrogen (1 N) di- (2) oxide: <b>NO<sub>2</sub></b>, a neutral molecule. Do not confuse it with NO<sub>2</sub><sup>" + M + "</sup>, the nitrite ion.", 2)

Q(T, "Which formula and name are matched correctly?",
  ["{N2O4}: dinitrogen tetroxide", "{N2O4}: nitrogen dioxide", "{CO}: monocarbon monoxide", "{SiO2}: silicon oxide"],
  ["2 N = dinitrogen, 4 O = tetroxide (the a of tetra- is usually dropped before oxide).",
   "Molecular formulas are never reduced. N<sub>2</sub>O<sub>4</sub> and NO<sub>2</sub> are different molecules with different names.",
   "Mono- is never used on the first element: CO is carbon monoxide.",
   "Molecular names need prefixes: two O atoms is dioxide."],
  "Check each name for missing prefixes, extra prefixes, and reduced formulas.",
  "<b>N<sub>2</sub>O<sub>4</sub>: dinitrogen tetroxide</b> is correct. NO<sub>2</sub> is nitrogen dioxide, CO is carbon monoxide, SiO<sub>2</sub> is silicon dioxide.", 2)

Q(T, "A student names {CaF2} \"calcium difluoride\" and {SF2} \"sulfur fluoride.\" Which pair of corrected names is right?",
  ["calcium fluoride; sulfur difluoride", "calcium difluoride; sulfur difluoride", "calcium fluoride; sulfur fluoride", "calcium(II) fluoride; sulfur difluoride"],
  ["CaF<sub>2</sub> is ionic (Ca is a metal): no prefixes. SF<sub>2</sub> is molecular (two nonmetals): prefixes are required.",
   "Calcium is a metal, so CaF<sub>2</sub> is ionic, and ionic names never use prefixes.",
   "SF<sub>2</sub> has two nonmetals and no ion charges, so its name needs a prefix to count the F atoms.",
   "Calcium has a fixed charge, so it never takes a Roman numeral."],
  "Classify each compound first: metal in front, or nonmetals only?",
  "Ionic CaF<sub>2</sub>: <b>calcium fluoride</b> (no prefix). Molecular SF<sub>2</sub>: <b>sulfur difluoride</b> (prefix required). Same F count, different rules.", 2)

Q(T, "What is the name of {PBr3}?",
  ["phosphorus tribromide", "phosphorus bromide", "monophosphorus tribromide", "tribromine phosphide"],
  ["P and Br are nonmetals: one P (no prefix on the first element) and three Br = tribromide.",
   "A molecular name needs a prefix to count the Br atoms.",
   "Mono- is never used on the first element.",
   "The element written first in the formula is named first."],
  "Name the elements in the order they appear in the formula.",
  "One P, three Br: <b>phosphorus tribromide</b>.", 1)

Q(T, "Why do names of molecular compounds use Greek prefixes, when names of ionic compounds do not?",
  ["Nonmetals can combine in more than one ratio, and there are no ion charges to fix the ratio, so the name must count the atoms.",
   "Molecular compounds are made of ions with larger charges, so the prefixes give the charges.",
   "Prefixes are used whenever a compound contains oxygen.",
   "Molecular compounds always contain exactly two atoms, so the prefixes are only for spelling."],
  ["Carbon and oxygen form both CO and CO<sub>2</sub>; only the prefixes tell them apart. In ionic compounds, the charges already decide the ratio.",
   "Molecular compounds are not made of ions; their atoms share electrons.",
   "Ionic oxides such as Na<sub>2</sub>O are named without prefixes; the rule depends on the compound type, not on oxygen.",
   "Molecules can contain many atoms (for example SF<sub>6</sub>), and the prefixes count them."],
  "Think of CO and CO<sub>2</sub>. What would happen if both were called \"carbon oxide\"?",
  "Ionic ratios are fixed by charges, so the name does not need to count ions. Molecular compounds have no charges, and the same two nonmetals can form several molecules (CO, CO<sub>2</sub>), so <b>prefixes count the atoms</b>.", 2)

Q(T, "What is the name of {I2O5}?",
  ["diiodine pentoxide", "iodine pentoxide", "diiodine pentaoxide", "pentaiodine dioxide"],
  ["Two I = diiodine, five O = pentoxide; the a of penta- is dropped before oxide.",
   "There are two iodine atoms, so the first element needs di-.",
   "Before oxide, the final a of penta- is dropped: pentoxide.",
   "The prefixes are swapped. There are 2 I atoms and 5 O atoms."],
  "Count both kinds of atoms, and check what happens to penta- before oxide.",
  "2 I, 5 O: <b>diiodine pentoxide</b>. Before oxide, a vowel at the end of a prefix is usually dropped (pentoxide, monoxide).", 2)

Q(T, "The common name <b>ammonia</b> refers to which formula?",
  ["{NH3}", "{NH4^+}", "{NH4}", "{NH2}"],
  ["Ammonia is the neutral molecule NH<sub>3</sub>, one of the common names to know.",
   "This is the ammonium ion. Ammonia and ammonium sound alike but are different species.",
   "NH<sub>4</sub> without a charge is not a stable molecule; with a 1+ charge it is the ammonium ion.",
   "Ammonia has three hydrogen atoms, not two."],
  "One of these is an ion. Ammonia is a neutral molecule.",
  "Ammonia is <b>NH<sub>3</sub></b>. Adding H<sup>+</sup> gives the ammonium ion, NH<sub>4</sub><sup>+</sup>.", 1)

# ======================= ch04-acids (10) =======================
T = 'ch04-acids'
Q(T, "What is the name of {HI(aq)}?",
  ["hydroiodic acid", "iodic acid", "hydrogen iodide", "hydroiodous acid"],
  ["HI(aq) has no oxygen, so it is a binary acid from iodide: hydro- + iod + -ic acid.",
   "With no hydro- prefix, this name belongs to an oxyacid made from iodate (IO<sub>3</sub><sup>" + M + "</sup>). HI contains no oxygen.",
   "Hydrogen iodide is the name of pure HI, a gas. The (aq) shows it is dissolved in water, so it gets an acid name.",
   "Binary acids always end in -ic. The -ous ending comes from -ite anions."],
  "Does the formula contain oxygen? Which anion is hiding after the H?",
  "The anion is iodide, I<sup>" + M + "</sup>, an -ide ion, so the acid is hydro- + iod + -ic: <b>hydroiodic acid</b>.", 1)

Q(T, "What is the name of {H2S(aq)}?",
  ["hydrosulfuric acid", "sulfuric acid", "sulfurous acid", "hydrosulfurous acid"],
  ["The anion is sulfide, S<sup>2" + M + "</sup>, with no oxygen: hydro- + sulfur + -ic acid.",
   "Sulfuric acid is H<sub>2</sub>SO<sub>4</sub>, an oxyacid from sulfate. H<sub>2</sub>S has no oxygen.",
   "Sulfurous acid is H<sub>2</sub>SO<sub>3</sub>, from sulfite. H<sub>2</sub>S has no oxygen.",
   "Binary acids end in -ic, not -ous."],
  "No oxygen means a binary acid. What prefix and ending do binary acids get?",
  "Sulfide (-ide) becomes hydro-...-ic: <b>hydrosulfuric acid</b>. Sulfuric acid, H<sub>2</sub>SO<sub>4</sub>, is a different compound.", 2)

Q(T, "Car batteries contain {H2SO4}. What is the name of this acid?",
  ["sulfuric acid", "hydrosulfuric acid", "sulfurous acid", "hydrogen sulfate"],
  ["The anion is sulfate, SO<sub>4</sub><sup>2" + M + "</sup>. -ate becomes -ic, and the root lengthens to sulfur.",
   "Hydro- is only for binary acids, which have no oxygen; this name belongs to H<sub>2</sub>S(aq).",
   "-ous comes from an -ite anion (sulfite, SO<sub>3</sub><sup>2" + M + "</sup>). This anion is sulfate.",
   "Hydrogen sulfate is the HSO<sub>4</sub><sup>" + M + "</sup> ion, which has one H and a charge."],
  "Name the anion after the H's, then change its ending.",
  "SO<sub>4</sub><sup>2" + M + "</sup> is sulfate; -ate &rarr; -ic: <b>sulfuric acid</b>. Oxyacids never get hydro-.", 1)

Q(T, "What is the name of {HBrO2}?",
  ["bromous acid", "bromic acid", "hydrobromous acid", "hypobromous acid"],
  ["The anion BrO<sub>2</sub><sup>" + M + "</sup> is bromite (one fewer O than bromate), and -ite becomes -ous.",
   "Bromic acid comes from bromate, BrO<sub>3</sub><sup>" + M + "</sup>, with three O atoms.",
   "Oxyacids never take hydro-; that prefix is only for acids without oxygen.",
   "The hypo- acid, HBrO, comes from hypobromite, with only one O."],
  "Name the anion first. How does BrO<sub>2</sub><sup>" + M + "</sup> compare with bromate?",
  "BrO<sub>2</sub><sup>" + M + "</sup> = bromite; -ite &rarr; -ous: <b>bromous acid</b>.", 2)

Q(T, "Many colas contain <b>phosphoric acid</b>. What is its formula?",
  ["{H3PO4}", "{HPO4}", "{H3PO3}", "{H2PO4}"],
  ["-ic comes from -ate: phosphate, PO<sub>4</sub><sup>3" + M + "</sup>. Three H<sup>+</sup> cancel the 3" + M + " charge.",
   "One H<sup>+</sup> cancels only one of phosphate's three negative charges.",
   "This is phosphorous acid, from phosphite (PO<sub>3</sub><sup>3" + M + "</sup>). -ic means the -ate ion.",
   "Two H<sup>+</sup> leave a 1" + M + " charge; the acid must be neutral."],
  "The number of H atoms equals the size of the anion's charge.",
  "Phosphoric &larr; phosphate, PO<sub>4</sub><sup>3" + M + "</sup>; 3 H<sup>+</sup>: <b>H<sub>3</sub>PO<sub>4</sub></b>.", 2)

Q(T, "In water, bleach forms <b>hypochlorous acid</b>, which kills bacteria. What is its formula?",
  ["{HClO}", "{HClO2}", "{HCl(aq)}", "{HClO4}"],
  ["-ous comes from -ite: hypochlorite, ClO<sup>" + M + "</sup>. One H<sup>+</sup> cancels the 1" + M + " charge, and the prefix hypo- stays.",
   "This is chlorous acid, from chlorite. The hypo- prefix means one fewer O than chlorite.",
   "This is hydrochloric acid, which has no oxygen.",
   "This is perchloric acid, from perchlorate, with four O atoms."],
  "Find the anion: hypo-...-ite. How many O atoms does it have?",
  "Hypochlorous &larr; hypochlorite, ClO<sup>" + M + "</sup>; one H<sup>+</sup>: <b>HClO</b>. Prefixes such as hypo- and per- stay in acid names.", 2)

Q(T, "What is the name of {HIO4}?",
  ["periodic acid", "iodic acid", "hydroperiodic acid", "periodous acid"],
  ["IO<sub>4</sub><sup>" + M + "</sup> is periodate (one more O than iodate). -ate becomes -ic and per- stays: per + iod + ic.",
   "Iodic acid is HIO<sub>3</sub>, from iodate, with three O atoms.",
   "Oxyacids never take hydro-.",
   "-ous comes from -ite anions; periodate is an -ate ion."],
  "Name the anion first. How does IO<sub>4</sub><sup>" + M + "</sup> compare with iodate, IO<sub>3</sub><sup>" + M + "</sup>?",
  "IO<sub>4</sub><sup>" + M + "</sup> = periodate; -ate &rarr; -ic, prefix kept: <b>periodic acid</b> (per-iodic, nothing to do with the periodic table).", 2)

Q(T, "Vinegar is about 5% <b>acetic acid</b> in water. What is the formula of acetic acid?",
  ["{HC2H3O2}", "{H2C2O4}", "{H2C2H3O2}", "{C2H3O2^-}"],
  ["Acetate is C<sub>2</sub>H<sub>3</sub>O<sub>2</sub><sup>" + M + "</sup>; one H<sup>+</sup> cancels its 1" + M + " charge.",
   "This is oxalic acid, from oxalate.",
   "Acetate is only 1" + M + ", so it needs only one H<sup>+</sup>.",
   "This is the acetate ion. The acid is neutral and has an H<sup>+</sup> added."],
  "Acetate has a 1" + M + " charge. How many H<sup>+</sup> does the acid need?",
  "Acetic &larr; acetate, C<sub>2</sub>H<sub>3</sub>O<sub>2</sub><sup>" + M + "</sup>; add one H<sup>+</sup>: <b>HC<sub>2</sub>H<sub>3</sub>O<sub>2</sub></b> (also written CH<sub>3</sub>COOH).", 1)

Q(T, "Carbon dioxide dissolved in blood forms {H2CO3}. What is its name?",
  ["carbonic acid", "hydrocarbonic acid", "carbonous acid", "bicarbonate"],
  ["The anion is carbonate, CO<sub>3</sub><sup>2" + M + "</sup>; -ate becomes -ic.",
   "Hydro- is only for acids with no oxygen.",
   "-ous comes from an -ite anion; carbonate is an -ate ion.",
   "Bicarbonate is the HCO<sub>3</sub><sup>" + M + "</sup> ion, with one H and a 1" + M + " charge."],
  "Which anion is left when both H<sup>+</sup> are removed?",
  "CO<sub>3</sub><sup>2" + M + "</sup> = carbonate; -ate &rarr; -ic: <b>carbonic acid</b>. It releases H<sup>+</sup> and bicarbonate in blood.", 1)

Q(T, "The table shows anions and the acids made from them. Which name belongs in the cell marked ?",
  ["chlorous acid", "chloric acid", "hydrochlorous acid", "hypochlorous acid"],
  ["ClO<sub>2</sub><sup>" + M + "</sup> is chlorite, and -ite becomes -ous.",
   "Chloric acid comes from chlorate, ClO<sub>3</sub><sup>" + M + "</sup>.",
   "Oxyacids never take hydro-.",
   "The hypo- acid, HClO, comes from hypochlorite, ClO<sup>" + M + "</sup>, with only one O."],
  "Look at the pattern in the rows above: what does -ite become?",
  "Sulfite gave sulfurous acid, so chlorite gives <b>chlorous acid</b>, HClO<sub>2</sub>.", 2,
  [{"type": "table", "cap": "Anions and their acids", "head": ["Anion", "Acid formula", "Acid name"],
    "rows": [["sulfate, {SO4^2-}", "{H2SO4}", "sulfuric acid"], ["sulfite, {SO3^2-}", "{H2SO3}", "sulfurous acid"],
             ["nitrate, {NO3^-}", "{HNO3}", "nitric acid"], ["chlorite, {ClO2^-}", "{HClO2}", "?"]]}])

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
import collections
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')))
