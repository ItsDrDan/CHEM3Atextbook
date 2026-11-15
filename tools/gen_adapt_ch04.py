#!/usr/bin/env python3
"""Builds bank/ch04_adapt.json (Chapter 4 ADAPT homework-only items, text only). Scratch generator.
usage: python3 tools/gen_adapt_ch04.py bank/ch04_adapt.json
Formula notation in braces as in tools/gen_bank_ch04.py; every formula and name is re-derived by tools/check_bank_ch04.py."""
import json, sys, re
OUT = sys.argv[1]
M = '&minus;'
B = []

def F(s):
    ch = ''
    if '^' in s: s, ch = s.split('^')
    tail = ''
    m = re.search(r'\((aq|g)\)$', s)
    if m: s, tail = s[:m.start()], m.group(0)
    parts = [re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', p) for p in s.split('.')]
    out = '&middot;'.join(parts) + tail
    if ch: out += '<sup>' + ch.replace('-', M) + '</sup>'
    return out
def X(s): return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)

def Q(t, q, c, y, h, w, d):
    y = ["Correct: " + y[0]] + y[1:]
    B.append({"id": "c4-h%02d" % (len(B) + 1), "t": t, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y], "h": X(h), "w": X(w), "d": d, "k": 0})

# ---------------- ch04-formulas (7) ----------------
T = 'ch04-formulas'
Q(T, "Ammonium hydrogen phosphate, {(NH4)2HPO4}, is a common fertilizer. How many <b>hydrogen</b> atoms are in one formula unit?",
  ["9", "5", "8", "10"],
  ["Two ammonium groups give 2 &times; 4 = 8 H, and the hydrogen phosphate ion adds 1 more: 8 + 1 = 9.",
   "This counts the ammonium H only once (4 + 1). The subscript 2 after the parentheses doubles everything inside.",
   "This counts the ammonium hydrogens but misses the H in HPO<sub>4</sub>.",
   "This multiplies the H in HPO<sub>4</sub> by 2 as well. The 2 belongs only to the parentheses around NH<sub>4</sub>."],
  "Hydrogen appears in two places in this formula.",
  "Ammonium: 2 &times; 4 = 8 H. Hydrogen phosphate: 1 H. Total <b>9 H atoms</b> (with 2 N, 1 P and 4 O).", 3)

Q(T, "How many atoms <b>in total</b> are in one formula unit of {Mg3(PO4)2}?",
  ["13", "8", "9", "3"],
  ["Mg: 3. P: 1 &times; 2 = 2. O: 4 &times; 2 = 8. Total 3 + 2 + 8 = 13.",
   "This counts the phosphate only once (3 + 1 + 4). The subscript 2 after the parentheses doubles P and O.",
   "This doubles the P but not the O. The subscript outside the parentheses multiplies every atom inside.",
   "3 is only the number of Mg atoms (or of different elements). Count every atom, including those inside the parentheses."],
  "Multiply everything inside the parentheses by the subscript after them.",
  "Mg 3, P 2, O 8: <b>13 atoms</b> in one formula unit.", 2)

Q(T, "How many <b>oxygen</b> atoms are shown in 3 {CO2} (three carbon dioxide molecules)?",
  ["6", "2", "5", "3"],
  ["Each CO<sub>2</sub> has 2 O atoms, and the coefficient 3 means three molecules: 3 &times; 2 = 6.",
   "This is the oxygen count for one molecule.",
   "This adds the coefficient and the subscript (3 + 2) instead of multiplying.",
   "This counts the molecules (or the carbon atoms), not the oxygen atoms."],
  "A coefficient multiplies every atom in the formula after it.",
  "3 &times; 2 = <b>6 O atoms</b> (and 3 C atoms).", 1)

Q(T, "Air is about 78% uncombined nitrogen. Which formula represents nitrogen as it exists in air?",
  ["{N2}", "{N}", "{N^3-}", "2N"],
  ["Nitrogen is one of the seven diatomic elements, so uncombined nitrogen is N<sub>2</sub> molecules.",
   "A single N atom is not how nitrogen exists in air; it is diatomic.",
   "This is the nitride ion, found only in ionic compounds.",
   "2N means two separate atoms. In nitrogen gas the two atoms are bonded together, shown with a subscript 2."],
  "Is nitrogen on the list of seven diatomic elements?",
  "Uncombined nitrogen is <b>N<sub>2</sub></b>: H<sub>2</sub>, N<sub>2</sub>, O<sub>2</sub>, F<sub>2</sub>, Cl<sub>2</sub>, Br<sub>2</sub> and I<sub>2</sub> are diatomic.", 1)

Q(T, "Which of these compounds is <b>ionic</b>?",
  ["{(NH4)2CO3}", "{CO2}", "{H2CO3(aq)}", "{CH4}"],
  ["The formula starts with ammonium, NH<sub>4</sub><sup>+</sup>, so it is made of ammonium ions and carbonate ions: ionic.",
   "C and O are both nonmetals, and there is no ammonium ion: molecular.",
   "This starts with H and is dissolved in water: an acid (carbonic acid).",
   "C and H are both nonmetals: molecular (methane)."],
  "A formula that starts with a metal, or with one special cation, is ionic.",
  "<b>(NH<sub>4</sub>)<sub>2</sub>CO<sub>3</sub></b> contains NH<sub>4</sub><sup>+</sup> and CO<sub>3</sub><sup>2" + M + "</sup> ions, so it is ionic even though it has no metal.", 1)

Q(T, "Which compound below is <b>molecular</b>?",
  ["{PCl3}", "{AlCl3}", "{NH4Cl}", "{ZnCl2}"],
  ["P and Cl are both nonmetals, so they share electrons in molecules: phosphorus trichloride.",
   "Al is a metal, so AlCl<sub>3</sub> is made of Al<sup>3+</sup> and Cl<sup>" + M + "</sup> ions: ionic.",
   "NH<sub>4</sub>Cl starts with the ammonium ion, so it is ionic.",
   "Zn is a metal, so ZnCl<sub>2</sub> is ionic."],
  "Which first element is to the right of the staircase line?",
  "Only <b>PCl<sub>3</sub></b> is made of nonmetals alone with no ammonium ion, so it is molecular.", 2)

Q(T, "Potassium hydroxide, {KOH}, is used to make soap. How is it classified?",
  ["Ionic, because its formula starts with a metal",
   "An acid, because it contains H",
   "Molecular, because O and H are nonmetals",
   "An acid, because it contains the OH group"],
  ["K is a group 1 metal, so KOH is made of K<sup>+</sup> ions and hydroxide ions, OH<sup>" + M + "</sup>.",
   "An acid's formula starts with H. Here the H is part of the hydroxide ion after a metal.",
   "O and H are bonded together as the hydroxide ion, which pairs with the K<sup>+</sup> ion.",
   "A formula ending in OH after a metal is a hydroxide. Hydroxides are not acids."],
  "Look at the first symbol in the formula.",
  "K is a metal, so KOH is <b>ionic</b>: potassium hydroxide, K<sup>+</sup> and OH<sup>" + M + "</sup>.", 1)

# ---------------- ch04-ionicformula (7) ----------------
T = 'ch04-ionicformula'
Q(T, "What is the formula of the ionic compound formed by <b>strontium and phosphorus</b>?",
  ["{Sr3P2}", "{Sr2P3}", "{SrP}", "{P2Sr3}"],
  ["Sr<sup>2+</sup> and P<sup>3" + M + "</sup>: swap-drop gives Sr<sub>3</sub>P<sub>2</sub>. Check: 3(2+) + 2(3" + M + ") = 0.",
   "Each charge number goes to the <i>other</i> ion. Check: 2(2+) + 3(3" + M + ") is not zero.",
   "One Sr<sup>2+</sup> and one P<sup>3" + M + "</sup> leave a 1" + M + " charge.",
   "The subscripts are right, but the cation comes first in an ionic formula."],
  "Strontium is in group 2; phosphorus is in group 15.",
  "Sr<sup>2+</sup> and P<sup>3" + M + "</sup>: <b>Sr<sub>3</sub>P<sub>2</sub></b> (strontium phosphide).", 1)

Q(T, "What is the formula of <b>aluminum sulfide</b>?",
  ["{Al2S3}", "{Al3S2}", "{AlS}", "{Al2(SO4)3}"],
  ["Al<sup>3+</sup> and S<sup>2" + M + "</sup>: swap-drop gives Al<sub>2</sub>S<sub>3</sub>. Check: 2(3+) + 3(2" + M + ") = 0.",
   "This leaves each charge on its own ion. Check: 3(3+) + 2(2" + M + ") = 5+.",
   "One Al<sup>3+</sup> and one S<sup>2" + M + "</sup> leave a 1+ charge.",
   "This is aluminum sulfate. Sulfide (-ide) is the single S<sup>2" + M + "</sup> ion."],
  "Check the ending: -ide means a single-atom anion.",
  "Al<sup>3+</sup> and S<sup>2" + M + "</sup>: <b>Al<sub>2</sub>S<sub>3</sub></b>.", 1)

Q(T, "What is the formula of the compound formed by tin(IV) ions and oxide ions?",
  ["{SnO2}", "{Sn2O4}", "{SnO}", "{Sn4O}"],
  ["Sn<sup>4+</sup> and O<sup>2" + M + "</sup>: swap-drop gives Sn<sub>2</sub>O<sub>4</sub>, which reduces to SnO<sub>2</sub>.",
   "Swap-drop gives this, but 2 : 4 must be reduced to 1 : 2.",
   "One Sn<sup>4+</sup> and one O<sup>2" + M + "</sup> leave a 2+ charge. That ratio is tin(II) oxide.",
   "The Roman numeral IV is a charge, not a subscript. Four tin ions and one oxide do not balance."],
  "The Roman numeral gives the tin ion's charge. Remember the last step of swap-drop.",
  "Sn<sup>4+</sup> and O<sup>2" + M + "</sup> &rarr; Sn<sub>2</sub>O<sub>4</sub> &rarr; reduce: <b>SnO<sub>2</sub></b>.", 2)

Q(T, "Calcium acetate is given to some kidney patients to bind phosphate. What is its formula?",
  ["{Ca(C2H3O2)2}", "{CaC2H3O22}", "{Ca2C2H3O2}", "{CaC2H3O2}"],
  ["Ca<sup>2+</sup> and C<sub>2</sub>H<sub>3</sub>O<sub>2</sub><sup>" + M + "</sup>: two acetate ions are needed, and two of a polyatomic ion need parentheses.",
   "Without parentheses, the 2 runs into the O subscript and reads as \"22 O atoms.\"",
   "Two Ca<sup>2+</sup> and one acetate give 4+ + 1" + M + "; the 2 belongs on acetate.",
   "One Ca<sup>2+</sup> and one 1" + M + " acetate leave a 1+ charge."],
  "Acetate is 1" + M + ". How many are needed to cancel Ca<sup>2+</sup>?",
  "Ca<sup>2+</sup> + 2 C<sub>2</sub>H<sub>3</sub>O<sub>2</sub><sup>" + M + "</sup>: <b>Ca(C<sub>2</sub>H<sub>3</sub>O<sub>2</sub>)<sub>2</sub></b>. (Context only; not dosing information.)", 2)

Q(T, "What is the charge on the <b>cobalt</b> ion in {CoPO4}?",
  ["3+", "1+", "4+", "3" + M],
  ["One phosphate is 3" + M + ", and there is one cobalt ion, so it must be 3+.",
   "No subscript on Co means one cobalt ion, not a 1+ charge. The charge comes from the anion.",
   "The 4 counts oxygen atoms inside the phosphate ion; it is not a charge.",
   "3" + M + " is phosphate's charge. Cobalt is the cation, so its charge is positive."],
  "What is the charge of phosphate on the green sheet?",
  "PO<sub>4</sub><sup>3" + M + "</sup> = 3" + M + " and there is one Co, so <b>Co<sup>3+</sup></b>: cobalt(III) phosphate.", 2)

Q(T, "What is the formula of <b>ammonium dichromate</b>?",
  ["{(NH4)2Cr2O7}", "{NH4Cr2O7}", "{NH42Cr2O7}", "{(NH4)2CrO4}"],
  ["NH<sub>4</sub><sup>+</sup> and Cr<sub>2</sub>O<sub>7</sub><sup>2" + M + "</sup>: two ammonium ions, in parentheses, cancel one dichromate.",
   "One NH<sub>4</sub><sup>+</sup> and one 2" + M + " dichromate leave a 1" + M + " charge.",
   "Without parentheses, the 2 runs into the 4 and reads as \"42 H atoms.\"",
   "This is ammonium chromate. Dichromate is Cr<sub>2</sub>O<sub>7</sub><sup>2" + M + "</sup>."],
  "Find dichromate on the green sheet, and treat ammonium as one unit.",
  "2 NH<sub>4</sub><sup>+</sup> + Cr<sub>2</sub>O<sub>7</sub><sup>2" + M + "</sup>: <b>(NH<sub>4</sub>)<sub>2</sub>Cr<sub>2</sub>O<sub>7</sub></b>.", 3)

Q(T, "What is the formula of <b>zinc hydroxide</b>?",
  ["{Zn(OH)2}", "{ZnOH2}", "{ZnOH}", "{Zn2OH}"],
  ["Zn<sup>2+</sup> and OH<sup>" + M + "</sup>: two hydroxides, in parentheses, cancel one Zn<sup>2+</sup>.",
   "Without parentheses, the 2 applies only to H: one O and two H. Two whole OH groups need parentheses.",
   "One Zn<sup>2+</sup> and one OH<sup>" + M + "</sup> leave a 1+ charge.",
   "Two Zn<sup>2+</sup> and one OH<sup>" + M + "</sup> give 4+ + 1" + M + "; the 2 belongs on hydroxide."],
  "Zinc is a fixed-charge metal. What is its charge?",
  "Zn<sup>2+</sup> + 2 OH<sup>" + M + "</sup>: <b>Zn(OH)<sub>2</sub></b>.", 1)

# ---------------- ch04-polyatomic (6) ----------------
T = 'ch04-polyatomic'
Q(T, "What is the formula of the <b>phosphate</b> ion?",
  ["{PO4^3-}", "{PO4^2-}", "{PO3^3-}", "{P^3-}"],
  ["Phosphate, from the green sheet, is PO<sub>4</sub><sup>3" + M + "</sup>.",
   "Phosphate is 3" + M + "; 2" + M + " is the charge of hydrogen phosphate, HPO<sub>4</sub><sup>2" + M + "</sup>.",
   "This has one fewer O, so it is phosphite.",
   "This is phosphide, the -ide ion, with no oxygen."],
  "Phosphate is one of the -ate ions to memorize.",
  "Phosphate is <b>PO<sub>4</sub><sup>3" + M + "</sup></b>, the ion in bone mineral.", 1)

Q(T, "Dried apricots from the Valley are often treated with sulfur compounds that form the {SO3^2-} ion. What is the name of this ion?",
  ["sulfite", "sulfate", "sulfide", "sulfur trioxide"],
  ["Sulfate is SO<sub>4</sub><sup>2" + M + "</sup>; one fewer O with the same charge is the -ite ion.",
   "Sulfate has four O atoms. This ion has three.",
   "Sulfide is S<sup>2" + M + "</sup>, with no oxygen.",
   "Sulfur trioxide is the neutral molecule SO<sub>3</sub>. The 2" + M + " charge makes this an ion."],
  "Compare the number of O atoms with sulfate, SO<sub>4</sub><sup>2" + M + "</sup>.",
  "One fewer O than sulfate, same charge: <b>sulfite</b>, SO<sub>3</sub><sup>2" + M + "</sup>.", 1)

Q(T, "Chlorate is {ClO3^-}. What is the formula of the <b>perchlorate</b> ion?",
  ["{ClO4^-}", "{ClO2^-}", "{ClO^-}", "{ClO4^2-}"],
  ["Per-...-ate means one more O than the -ate ion, with the same charge.",
   "This has one fewer O than chlorate, so it is chlorite.",
   "This is hypochlorite, two fewer O than chlorate.",
   "Adding an O atom does not change the charge; perchlorate is 1" + M + ", like chlorate."],
  "What does the prefix per- do to the number of oxygen atoms? Does it change the charge?",
  "Chlorate ClO<sub>3</sub><sup>" + M + "</sup> + one O: <b>ClO<sub>4</sub><sup>" + M + "</sup></b>, perchlorate.", 2)

Q(T, "Some toilet-bowl cleaners contain the <b>hydrogen sulfate</b> (bisulfate) ion. What is its formula?",
  ["{HSO4^-}", "{HSO4^2-}", "{HSO3^-}", "{H2SO4}"],
  ["Sulfate is SO<sub>4</sub><sup>2" + M + "</sup>; one added H<sup>+</sup> makes the charge 1" + M + ".",
   "Adding H<sup>+</sup> lowers the negative charge by one: 2" + M + " becomes 1" + M + ".",
   "This is hydrogen sulfite (bisulfite), built from sulfite.",
   "This is sulfuric acid, a neutral compound with two H."],
  "Start from sulfate. What does adding one H<sup>+</sup> do to the charge?",
  "SO<sub>4</sub><sup>2" + M + "</sup> + H<sup>+</sup> = <b>HSO<sub>4</sub><sup>" + M + "</sup></b>.", 2)

Q(T, "What is the name of the ion {Cr2O7^2-}?",
  ["dichromate", "chromate", "dichromite", "perchromate"],
  ["Cr<sub>2</sub>O<sub>7</sub><sup>2" + M + "</sup>, with two Cr atoms, is dichromate, from the green sheet.",
   "Chromate is CrO<sub>4</sub><sup>2" + M + "</sup>, with one Cr atom.",
   "Both chromium ions on the green sheet end in -ate.",
   "The per- prefix is not used with chromium in this course; count the Cr atoms instead."],
  "Count the chromium atoms.",
  "Cr<sub>2</sub>O<sub>7</sub><sup>2" + M + "</sup> is <b>dichromate</b>; CrO<sub>4</sub><sup>2" + M + "</sup> is chromate.", 2)

Q(T, "What is the formula of the <b>peroxide</b> ion?",
  ["{O2^2-}", "{O^2-}", "{O2}", "{OH^-}"],
  ["Peroxide, from the green sheet, is two bonded O atoms with a 2" + M + " charge.",
   "This is the oxide ion, a single O atom.",
   "This is the neutral oxygen molecule, with no charge.",
   "This is the hydroxide ion."],
  "Peroxide has two oxygen atoms.",
  "Peroxide is <b>O<sub>2</sub><sup>2" + M + "</sup></b>; hydrogen peroxide is H<sub>2</sub>O<sub>2</sub>.", 2)

# ---------------- ch04-ionicname (7) ----------------
T = 'ch04-ionicname'
Q(T, "Zinc oxide, {ZnO}, is the white ingredient in many diaper creams. Which name follows the naming rules?",
  ["zinc oxide", "zinc(II) oxide", "zinc monoxide", "zinc oxygen"],
  ["Zn is on the fixed-charge list (always 2+), so no Roman numeral; O<sup>2" + M + "</sup> is oxide.",
   "Zinc is a fixed-charge metal, so it takes no Roman numeral.",
   "Ionic names never use prefixes.",
   "The anion takes the -ide ending: oxide."],
  "Is zinc on the fixed-charge list?",
  "<b>zinc oxide</b>: fixed-charge metal, no numeral, no prefixes.", 1)

Q(T, "What is the name of {MgBr2}?",
  ["magnesium bromide", "magnesium dibromide", "magnesium(II) bromide", "magnesium bromate"],
  ["Mg is group 2 (fixed 2+) and Br<sup>" + M + "</sup> is bromide.",
   "Ionic names do not use prefixes.",
   "Magnesium has only one charge, so no Roman numeral.",
   "Bromate is BrO<sub>3</sub><sup>" + M + "</sup>; a single Br is bromide."],
  "Fixed-charge metal? Single-atom anion?",
  "<b>magnesium bromide</b>.", 1)

Q(T, "What is the name of {PbO}?",
  ["lead(II) oxide", "lead oxide", "lead(I) oxide", "lead(IV) oxide"],
  ["One O<sup>2" + M + "</sup> means the single lead ion is Pb<sup>2+</sup>: lead(II).",
   "Lead forms two ions, so the name must include a Roman numeral.",
   "No subscript on Pb means one lead ion, not a 1+ charge. The charge comes from the oxide.",
   "Lead(IV) oxide is PbO<sub>2</sub>, with two oxide ions."],
  "Work out lead's charge from the oxide ion.",
  "O<sup>2" + M + "</sup> = 2" + M + ", one Pb, so Pb<sup>2+</sup>: <b>lead(II) oxide</b> (plumbous oxide).", 2)

Q(T, "Some water-treatment plants add <b>ferric chloride</b> to clump particles together. What is its formula?",
  ["{FeCl3}", "{FeCl2}", "{Fe3Cl}", "{FeCl}"],
  ["Ferric is iron(III), Fe<sup>3+</sup>; three Cl<sup>" + M + "</sup> cancel it.",
   "This is ferrous chloride, iron(II). -ic is the higher charge.",
   "The charge 3+ is not a subscript on Fe. Three Fe<sup>3+</sup> and one Cl<sup>" + M + "</sup> do not balance.",
   "One Fe<sup>3+</sup> and one Cl<sup>" + M + "</sup> leave a 2+ charge."],
  "Does -ic mean iron's lower or higher charge?",
  "Ferric = Fe<sup>3+</sup>; with Cl<sup>" + M + "</sup>: <b>FeCl<sub>3</sub></b>, iron(III) chloride.", 2)

Q(T, "Copper fungicides sprayed in Valley orchards often contain {Cu(OH)2}. What is its name?",
  ["copper(II) hydroxide", "copper hydroxide", "copper(II) dihydroxide", "cuprous hydroxide"],
  ["Two OH<sup>" + M + "</sup> give 2" + M + ", so the copper ion is Cu<sup>2+</sup>: copper(II).",
   "Copper forms two ions, so the Roman numeral is required.",
   "Ionic names do not use prefixes.",
   "Cuprous is copper(I), the lower charge; this copper ion is 2+, the higher charge."],
  "Find copper's charge from the hydroxide ions.",
  "2 OH<sup>" + M + "</sup> = 2" + M + ": Cu<sup>2+</sup>, <b>copper(II) hydroxide</b> (cupric hydroxide).", 2)

Q(T, "What is the formula of <b>copper(II) chloride dihydrate</b>?",
  ["{CuCl2.2H2O}", "{CuCl.2H2O}", "{CuCl2.H2O}", "{Cu2Cl2.2H2O}"],
  ["Cu<sup>2+</sup> and Cl<sup>" + M + "</sup> give CuCl<sub>2</sub>; di- means two water molecules.",
   "Copper(II) is 2+, so it needs two chloride ions.",
   "Dihydrate means 2 H<sub>2</sub>O, so a 2 goes in front of the water.",
   "This puts the Roman numeral in as a subscript on Cu and never reduces; copper(II) chloride is a 1 : 2 compound."],
  "Write the ionic formula first, then the dot and the number of waters.",
  "Cu<sup>2+</sup> + 2 Cl<sup>" + M + "</sup> = CuCl<sub>2</sub>; dihydrate = 2 H<sub>2</sub>O: <b>CuCl<sub>2</sub>&middot;2H<sub>2</sub>O</b>.", 2)

Q(T, "Sodium bicarbonate, {NaHCO3}, is given by IV in some emergencies. What is its other accepted name?",
  ["sodium hydrogen carbonate", "sodium carbonate", "sodium hydrogen carbonite", "sodium(I) hydrogen carbonate"],
  ["HCO<sub>3</sub><sup>" + M + "</sup> is hydrogen carbonate (bicarbonate), and Na is fixed at 1+.",
   "Sodium carbonate is Na<sub>2</sub>CO<sub>3</sub>, without the H.",
   "Adding H does not change the -ate ending; the ion still has three O atoms.",
   "Sodium is a fixed-charge metal, so it takes no Roman numeral."],
  "Bi- is the older way to say one added hydrogen.",
  "HCO<sub>3</sub><sup>" + M + "</sup> = hydrogen carbonate: <b>sodium hydrogen carbonate</b>. (Context only; not treatment advice.)", 2)

# ---------------- ch04-molecular (7) ----------------
T = 'ch04-molecular'
Q(T, "What is the name of {SiCl4}?",
  ["silicon tetrachloride", "silicon chloride", "monosilicon tetrachloride", "tetrachlorine silicide"],
  ["Si and Cl are nonmetals: one Si (no prefix on the first element) and four Cl = tetrachloride.",
   "Molecular names need a prefix to count the Cl atoms.",
   "Mono- is never used on the first element.",
   "Name the elements in the order they are written in the formula."],
  "Two nonmetals: count the atoms with prefixes.",
  "<b>silicon tetrachloride</b>.", 1)

Q(T, "Strike-anywhere match heads contain {P4S3}. What is its name?",
  ["tetraphosphorus trisulfide", "phosphorus sulfide", "tetraphosphorus trisulfur", "trisulfur tetraphosphide"],
  ["Four P = tetraphosphorus, three S = trisulfide.",
   "Without prefixes, the name does not tell you the formula; P and S form several compounds.",
   "The second element needs the -ide ending.",
   "The element written first in the formula is named first."],
  "Prefix + first element, prefix + second element with -ide.",
  "4 P, 3 S: <b>tetraphosphorus trisulfide</b>.", 2)

Q(T, "Valley dried-fruit packers treat apricots with <b>sulfur dioxide</b> gas to keep their color. What is the formula of sulfur dioxide?",
  ["{SO2}", "{SO3^2-}", "{S2O}", "{SO}"],
  ["No prefix on sulfur means one S; di- means 2 O.",
   "This is the sulfite ion, which carries a charge. Sulfur dioxide is a neutral molecule.",
   "The di- belongs to oxide, so the 2 goes on O, not on S.",
   "Di- means two oxygen atoms."],
  "Which element does the prefix di- belong to?",
  "Sulfur (1) di-oxide (2): <b>SO<sub>2</sub></b>.", 1)

Q(T, "A dental office offers <b>nitrous oxide</b> to anxious patients. What is the formula of nitrous oxide?",
  ["{N2O}", "{NO}", "{NO2}", "{N2O3}"],
  ["Nitrous oxide is the common name of dinitrogen monoxide: two N, one O.",
   "This is nitric oxide (nitrogen monoxide), the gas used in neonatal intensive care.",
   "This is nitrogen dioxide, a brown air pollutant.",
   "This is dinitrogen trioxide, with three O atoms."],
  "Its systematic name is dinitrogen monoxide.",
  "Nitrous oxide = dinitrogen monoxide = <b>N<sub>2</sub>O</b>. One subscript changes the compound completely.", 1)

Q(T, "A student names {Na2S} \"disodium sulfide\" and {CS2} \"carbon sulfide.\" Which pair of corrected names is right?",
  ["sodium sulfide; carbon disulfide", "disodium sulfide; carbon disulfide", "sodium sulfide; carbon sulfide", "sodium(I) sulfide; carbon disulfide"],
  ["Na<sub>2</sub>S is ionic (Na is a metal): no prefixes. CS<sub>2</sub> is molecular: prefixes required.",
   "Sodium is a metal, so Na<sub>2</sub>S is ionic, and ionic names never use prefixes.",
   "CS<sub>2</sub> contains only nonmetals, so it needs a prefix for the two S atoms.",
   "Sodium is a fixed-charge metal, so it never takes a Roman numeral."],
  "Classify each compound before naming it.",
  "Ionic Na<sub>2</sub>S: <b>sodium sulfide</b>. Molecular CS<sub>2</sub>: <b>carbon disulfide</b>.", 2)

Q(T, "What is the name of {BrF5}?",
  ["bromine pentafluoride", "bromine fluoride", "monobromine pentafluoride", "pentafluorine bromide"],
  ["One Br (no prefix on the first element), five F = pentafluoride.",
   "A molecular name must count the F atoms with a prefix.",
   "Mono- is never used on the first element.",
   "The first element in the formula is named first, and the second gets -ide."],
  "Count the atoms of each element.",
  "<b>bromine pentafluoride</b>.", 1)

Q(T, "Which name for {Cl2O} follows this book's prefix rules?",
  ["dichlorine monoxide", "dichlorine monooxide", "dichlorine oxide", "chlorine monoxide"],
  ["2 Cl = dichlorine; 1 O = monoxide, with the o of mono- dropped before oxide.",
   "Before oxide, the final o of mono- is dropped.",
   "Mono- is used on the second element, so oxide needs mono-.",
   "There are two chlorine atoms, so the first element needs di-."],
  "Check both prefixes, and the vowel before oxide.",
  "<b>dichlorine monoxide</b>: di- on Cl, mono- on oxide with the vowel dropped.", 2)

# ---------------- ch04-acids (6) ----------------
T = 'ch04-acids'
Q(T, "Parietal cells in the stomach produce {HCl(aq)}. What is its name?",
  ["hydrochloric acid", "hydrogen chloride", "chloric acid", "hydrochlorous acid"],
  ["Chloride (-ide) in water becomes hydro- + chlor + -ic acid.",
   "That is the name of pure HCl, a gas. The (aq) means it is dissolved in water and takes an acid name.",
   "Chloric acid is HClO<sub>3</sub>, from chlorate. HCl has no oxygen.",
   "Binary acids end in -ic, never -ous."],
  "No oxygen in the formula: which kind of acid is it?",
  "Chloride &rarr; <b>hydrochloric acid</b>. Without water, HCl is hydrogen chloride gas.", 1)

Q(T, "Nitrogen fertilizers are made from {HNO3}. What is its name?",
  ["nitric acid", "nitrous acid", "hydronitric acid", "nitrate acid"],
  ["The anion is nitrate, NO<sub>3</sub><sup>" + M + "</sup>; -ate becomes -ic.",
   "-ous comes from nitrite, NO<sub>2</sub><sup>" + M + "</sup>, with two O atoms.",
   "Oxyacids never take hydro-.",
   "The -ate ending changes to -ic in the acid name."],
  "Name the anion first, then change its ending.",
  "NO<sub>3</sub><sup>" + M + "</sup> = nitrate; -ate &rarr; -ic: <b>nitric acid</b>.", 1)

Q(T, "What is the formula of <b>hydrobromic acid</b>?",
  ["{HBr(aq)}", "{HBrO3}", "{HBr2(aq)}", "{HBrO}"],
  ["Hydro-...-ic means a binary acid from bromide, Br<sup>" + M + "</sup>; one H<sup>+</sup> cancels it, in water.",
   "This is bromic acid, from bromate. Hydro- means no oxygen.",
   "Bromide is only 1" + M + ", so the acid needs one H, and there is one Br.",
   "This is hypobromous acid, from hypobromite."],
  "What does the prefix hydro- tell you about oxygen?",
  "Hydrobromic acid &larr; bromide: <b>HBr(aq)</b>.", 1)

Q(T, "Rhubarb leaves contain <b>oxalic acid</b>. What is its formula?",
  ["{H2C2O4}", "{HC2O4}", "{HC2H3O2}", "{C2O4^2-}"],
  ["Oxalate is C<sub>2</sub>O<sub>4</sub><sup>2" + M + "</sup>; two H<sup>+</sup> cancel its 2" + M + " charge.",
   "One H<sup>+</sup> cancels only half of oxalate's 2" + M + " charge.",
   "This is acetic acid, from acetate.",
   "This is the oxalate ion; the acid is neutral."],
  "Oxalate has a 2" + M + " charge. How many H<sup>+</sup> are needed?",
  "Oxalic &larr; oxalate, C<sub>2</sub>O<sub>4</sub><sup>2" + M + "</sup>: <b>H<sub>2</sub>C<sub>2</sub>O<sub>4</sub></b>.", 2)

Q(T, "What is the name of {HClO3}?",
  ["chloric acid", "chlorous acid", "hydrochloric acid", "perchloric acid"],
  ["ClO<sub>3</sub><sup>" + M + "</sup> is chlorate; -ate becomes -ic.",
   "-ous comes from chlorite, ClO<sub>2</sub><sup>" + M + "</sup>.",
   "Hydro- is only for acids without oxygen, such as HCl(aq).",
   "HClO<sub>4</sub>, with four O atoms, comes from perchlorate and keeps the per- prefix."],
  "Which chlorine oxyanion has three O atoms?",
  "Chlorate &rarr; <b>chloric acid</b>.", 1)

Q(T, "Which acid is named with the prefix <b>hydro-</b>?",
  ["{HF(aq)}", "{HNO2}", "{H2CO3}", "{HClO4}"],
  ["HF(aq) contains no oxygen: it is a binary acid from fluoride, so it is hydrofluoric acid.",
   "HNO<sub>2</sub> contains oxygen: nitrous acid, no hydro-.",
   "H<sub>2</sub>CO<sub>3</sub> contains oxygen: carbonic acid, no hydro-.",
   "HClO<sub>4</sub> contains oxygen: perchloric acid, no hydro-."],
  "Hydro- is used only when the anion is an -ide ion.",
  "Only binary acids (no oxygen) take hydro-: <b>HF(aq)</b>, hydrofluoric acid.", 1)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
import collections
print(len(B), dict(collections.Counter(q['t'] for q in B)))
