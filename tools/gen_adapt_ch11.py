#!/usr/bin/env python3
"""Builds bank/ch11_adapt.json (Chapter 11 ADAPT homework-only items, text only; 42 items, none repeated from
bank/ch11.json).
usage: python3 tools/gen_adapt_ch11.py bank/ch11_adapt.json
Same conventions, helpers and markup as tools/gen_bank_ch11.py (imported from it): percents with the solution in the
denominator; 1 ppm = 1 mg/L, 1 ppb = 1 ug/L in dilute water; M = mol/L solution; M1V1 = M2V2 with matching units;
volume used = final - initial; molality per kg solvent; complete dissociation i; Kf 1.86, Kb 0.512 C/m; yellow-sheet
molar masses. y[0] begins "Correct: ". Every item is rechecked by tools/check_bank_ch11.py."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bank_ch11 import *
import gen_bank_ch11 as G
G.CFG.update(prefix='c11-h%02d', adapt=True)


def build_hw():
    # ======================= ch11-dissolve (6) =======================
    T = 'ch11-dissolve'
    Q(T, "Yellow brass, used in plumbing fittings, is about 67% copper and 33% zinc by mass. Which metal is the solvent?",
      ["Copper", "Zinc", "Neither metal; a solid cannot be a solution", "Both metals equally, because they are melted together"],
      ["Copper is present in the larger amount, so it is the solvent; brass is a solid solution.",
       "Zinc is the solute here: there is less of it (33%) than of the other metal (67%).",
       "Solutions can be solids: brass and dental amalgam are solid solutions of metals.",
       "Melting them together makes a homogeneous mixture, but the component present in the larger amount is still the solvent."],
      "The solvent is the component present in the largest amount.",
      "67% is the larger share: <b>copper</b> is the solvent.", 1)

    Q(T, "Which substance dissolves best in hexane, {C6H14}?",
      ["Decane, {C10H22}", "Sodium chloride, NaCl", "Sucrose, {C12H22O11}", "Potassium nitrate, {KNO3}"],
      ["Decane and hexane are both nonpolar hydrocarbons with dispersion forces only: like dissolves like.",
       "NaCl is ionic; nonpolar hexane cannot form ion&ndash;dipole attractions with its ions.",
       "Sucrose is polar with many O&ndash;H groups; it dissolves in water, not hexane.",
       "{KNO3} is ionic, so it dissolves in polar water, not in nonpolar hexane."],
      "Hexane is nonpolar. Which solute is also nonpolar?",
      "Like dissolves like: nonpolar <b>decane</b> dissolves in nonpolar hexane.", 1)

    Q(T, "Which solute is a strong electrolyte in water?",
      ["{Na2SO4}", "ethylene glycol, {C2H6O2}", "methanol, {CH3OH}", "acetone, {C3H6O}"],
      ["{Na2SO4} is a soluble ionic compound that separates into Na<sup>+</sup> and SO<sub>4</sub><sup>2&minus;</sup> ions.",
       "Ethylene glycol dissolves as whole molecules, so it is a nonelectrolyte.",
       "Methanol dissolves as whole molecules, so it is a nonelectrolyte.",
       "Acetone is molecular and forms no ions in water, so it is a nonelectrolyte."],
      "Strong electrolytes are soluble ionic compounds.",
      "Ionic and soluble: <b>{Na2SO4}</b>.", 1)

    Q(T, "Salad oil and vinegar (which is mostly water) separate into layers no matter how hard they are shaken. Why?",
      ["Water molecules hydrogen bond to each other and squeeze out the nonpolar oil molecules.",
       "Oil and water react to form a third layer.",
       "Oil molecules hydrogen bond to each other more strongly than water molecules do.",
       "Oil is denser than water, so it sinks and cannot mix."],
      ["Nonpolar oil cannot form strong attractions with water, so water's hydrogen bonds keep the water together and push the oil out.",
       "Oil and water do not react; they are immiscible because their intermolecular forces do not match.",
       "Oil molecules are nonpolar, with dispersion forces only; they do not hydrogen bond.",
       "Oil floats on water (it is less dense), and density decides which layer is on top, not whether the liquids mix."],
      "Compare the intermolecular forces of oil and of water.",
      "Unlike substances: <b>water's hydrogen bonds squeeze out the nonpolar oil</b>.", 2)

    Q(T, "The solubility of {NaNO3} is 88.0 g per 100 g of water at 20 °C. A solution at 20 °C contains 176 g of {NaNO3} dissolved in 200. g of water. How is it described?",
      ["Saturated", "Supersaturated", "Unsaturated", "Immiscible"],
      ["200. g of water holds 88.0 &times; 2 = 176 g at 20 °C, exactly the amount dissolved: the solution holds the maximum.",
       "This compares 176 g with 88.0 g, but 88.0 g is for 100 g of water. This solution has twice as much water.",
       "This solution is not below the limit: it holds exactly the maximum for 200. g of water.",
       "Immiscible describes two liquids that form layers."],
      "Scale the solubility to 200. g of water.",
      "Capacity = 88.0 g &times; 200./100 = 176 g = the amount dissolved: <b>saturated</b>.", 3)

    Q(T, "Acetone ({C3H6O}), a polar liquid, and water mix in all proportions. What is the term for two liquids that do this?",
      ["Miscible", "Immiscible", "Saturated", "Supersaturated"],
      ["Miscible liquids mix in all proportions, as acetone and water do.",
       "That term (with the prefix im-, &ldquo;not&rdquo;) describes liquids that form separate layers, like oil and water.",
       "Saturated describes a solution that holds the maximum amount of a solute.",
       "Supersaturated describes an unstable solution holding more than the solubility."],
      "Water and ethanol are another example.",
      "<b>Miscible</b>.", 1)

    # ======================= ch11-solubility (6) =======================
    T = 'ch11-solubility'
    S1, P1, P2 = '8.26', '0.209', '0.155'; v = D(S1) * D(P2) / D(P1); n = ns(S1, P1, P2)
    Q(T, "At 25.0 °C, water in contact with air ({O2} partial pressure %s atm) dissolves %s mg/L of {O2}. A high-elevation reservoir, also at 25.0 °C, has an {O2} partial pressure of only %s atm. What is the solubility of {O2} in the lake?" % (P1, S1, P2),
      [S(v, n, 'mg/L'), S(D(S1) * D(P1) / D(P2), n, 'mg/L'), S(D(S1) * D(P2), n, 'mg/L'), S1 + ' mg/L'],
      ["S<sub>2</sub> = S<sub>1</sub> &times; P<sub>2</sub>/P<sub>1</sub>; lower partial pressure, less dissolved {O2}.",
       "This inverts the pressure ratio; Henry's law is direct, so the solubility must fall.",
       "This multiplies by P<sub>2</sub> without dividing by P<sub>1</sub>.",
       "The partial pressure changed, so the solubility of the gas changes too."],
      "S<sub>1</sub>/P<sub>1</sub> = S<sub>2</sub>/P<sub>2</sub>.",
      "S<sub>2</sub> = %s &times; %s / %s = <b>%s</b>." % (S1, P2, P1, S(v, n, 'mg/L')), 2, 1)

    S1, P1, S2 = '1.68', '0.850', '6.85'; v = D(S2) * D(P1) / D(S1); n = ns(S1, P1, S2)
    Q(T, "At 15.0 °C, %s g/L of {CO2} dissolves in water at a {CO2} pressure of %s atm. What {CO2} pressure gives a solubility of %s g/L at the same temperature?" % (S1, P1, S2),
      [S(v, n, 'atm'), S(D(S1) * D(P1) / D(S2), n, 'atm'), S(D(S2) / D(S1), n, 'atm'), S(D(S2) * D(S1) / D(P1), n, 'atm')],
      ["P<sub>2</sub> = P<sub>1</sub> &times; S<sub>2</sub>/S<sub>1</sub>: about four times the solubility needs about four times the pressure.",
       "This inverts the ratio, giving a lower pressure for a higher solubility.",
       "This is only the solubility ratio; multiply it by P<sub>1</sub> = %s atm." % P1,
       "This multiplies the two solubilities; solve S<sub>1</sub>/P<sub>1</sub> = S<sub>2</sub>/P<sub>2</sub> for P<sub>2</sub>."],
      "Solve Henry's law for P<sub>2</sub>.",
      "P<sub>2</sub> = %s atm &times; %s / %s = <b>%s</b>." % (P1, S2, S1, S(v, n, 'atm')), 3, 1)

    Q(T, "Which change increases the amount of {CO2} that can dissolve in water?",
      ["Cooling the water and raising the {CO2} pressure", "Warming the water and raising the {CO2} pressure",
       "Cooling the water and lowering the {CO2} pressure", "Warming the water and lowering the {CO2} pressure"],
      ["Both changes help: gases dissolve better in colder water and at higher partial pressure.",
       "Higher pressure helps, but warming lowers a gas's solubility.",
       "Cooling helps, but lower pressure means less dissolved gas (Henry's law).",
       "Both changes lower a gas's solubility; this is how a soda goes flat."],
      "Treat temperature and pressure separately.",
      "<b>Colder and higher pressure</b>.", 1)

    Q(T, "Hot tea dissolves more sugar than iced tea. Which statement explains this?",
      ["For most solids, solubility increases as the temperature rises.", "For most solids, solubility decreases as the temperature rises.",
       "Hot tea is under higher pressure, which dissolves more sugar.", "Sugar molecules break into ions in hot water."],
      ["Faster-moving water molecules break up the solid more easily, so most solids dissolve better when hot.",
       "That is the rule for gases, not for most solids.",
       "Pressure has almost no effect on the solubility of solids.",
       "Sugar dissolves as whole molecules at any temperature."],
      "Solids and gases respond to temperature in opposite ways.",
      "Most solids: <b>more soluble when hotter</b>.", 1)

    hi, lo = '65.6', '29.4'; v = addp(hi, '-' + lo)
    Q(T, "The solubility of {NH4Cl} is %s g per 100. g of water at 80.0 °C and %s g per 100. g at 0 °C. A saturated solution made with 100. g of water at 80.0 °C is chilled to 0 °C. What mass of {NH4Cl} crystallizes?" % (hi, lo),
      [v + ' g', hi + ' g', lo + ' g', addp(hi, lo) + ' g'],
      ["The solution held %s g; only %s g can stay dissolved at 0 °C, so the rest crystallizes." % (hi, lo),
       "This is all the dissolved {NH4Cl}; %s g of it stays dissolved." % lo,
       "This is the amount that stays dissolved at 0 °C.",
       "This adds the solubilities; subtract them."],
      "Amount crystallized = amount dissolved hot &minus; amount that stays dissolved cold.",
      "%s &minus; %s = <b>%s g</b>." % (hi, lo, v), 2, 1)

    Q(T, "Bubbles form as soon as a bottle of soda is opened, even though its temperature has not changed. Why?",
      ["The {CO2} pressure above the liquid drops, so less {CO2} can stay dissolved.",
       "Opening the bottle raises the {CO2} pressure, which forces gas out of the liquid.",
       "{CO2} is more soluble at low pressure, so it dissolves and forms bubbles.",
       "Air rushes into the bottle and reacts with the sugar to make gas."],
      ["Henry's law: gas solubility is proportional to the gas's partial pressure. Opening the bottle lowers it, and the extra {CO2} comes out as bubbles.",
       "Opening the bottle lets the high-pressure {CO2} escape, so the pressure above the liquid falls.",
       "This reverses Henry's law: gases are <i>less</i> soluble at lower pressure.",
       "No reaction takes place; the bubbles are {CO2} leaving solution."],
      "What happens to the gas pressure above the soda when the cap comes off?",
      "Lower {CO2} pressure, <b>less {CO2} can stay dissolved</b>.", 1)

    # ======================= ch11-conc (8) =======================
    T = 'ch11-conc'
    g_, w_ = '6.40', '145.0'; tot = addp(g_, w_); v = D(g_) / D(tot) * 100; n = ns(g_, tot)
    Q(T, "A solution is made by dissolving %s g of potassium iodide, KI, in %s g of water. What is the mass percent of KI?" % (g_, w_),
      [P(v, n), P(D(g_) / D(w_) * 100, n), P(D(w_) / D(tot) * 100, n), P(D(g_) / D(tot), n)],
      ["Mass of solution = %s + %s = %s g; %s/%s &times; 100%%." % (g_, w_, tot, g_, tot),
       "This divides by the mass of water; the denominator is the whole solution.",
       "This is the percent of water.",
       "This is the mass fraction without &times; 100%."],
      "Solution = solute + solvent.",
      "%s / %s &times; 100%% = <b>%s</b>." % (g_, tot, P(v, n)), 2, 1)

    V, pc = '10.0', '0.050'; v = D(V) * D(pc) / 100; n = ns(V, pc)
    Q(T, "An over-the-counter fluoride mouth rinse is %s%% (m/v) sodium fluoride, NaF. How many grams of NaF are in a %s mL dose?" % (pc, V),
      [S(v, n, 'g'), S(D(V) * D(pc), n, 'g'), S(v / 100, n, 'g'), S(D(V) / D(pc), n, 'g')],
      ["%s%% (m/v) = %s g per 100 mL: %s mL &times; %s g/100 mL. (Context only; follow the product directions.)" % (pc, pc, V, pc),
       "This multiplies by %s without dividing by 100 mL." % pc,
       "This divides by 100 twice.",
       "This divides the volume by the percent; use the percent as g per 100 mL."],
      "%(m/v) means grams per 100 mL of solution.",
      "%s mL &times; (%s g / 100 mL) = <b>%s</b> (%s mg)." % (V, pc, S(v, n, 'g'), num(v * 1000, n)), 2, 1)

    mg, V = '98.5', '2.50'; v = D(mg) / D(V); n = ns(mg, V)
    Q(T, "A %s L water sample from a Valley well contains %s mg of nitrate. What is the nitrate concentration in ppm?" % (V, mg),
      [S(v, n, 'ppm'), S(D(mg) * D(V), n, 'ppm'), S(D(V) / D(mg), n, 'ppm'), S(v * 1000, n, 'ppm')],
      ["1 ppm &asymp; 1 mg/L: %s mg / %s L. That is below the 45 mg/L nitrate limit." % (mg, V),
       "This multiplies mg by L; ppm is mg <i>per</i> liter.",
       "This divides liters by mg; the solute goes on top.",
       "This multiplies by 1000 (mg to &mu;g), which gives ppb."],
      "ppm &asymp; mg/L in dilute water.",
      "%s mg / %s L = <b>%s</b>." % (mg, V, S(v, n, 'ppm')), 2, 1)

    mg, V = '0.0185', '1.50'; v = D(mg) / D(V) * 1000; n = ns(mg, V)
    Q(T, "A %s L sample of tap water from an older school building contains %s mg of lead. What is the lead concentration in ppb?" % (V, mg),
      [S(v, n, 'ppb'), S(D(mg) / D(V), n, 'ppb'), S(D(mg) * 1000, n, 'ppb'), S(D(mg) / D(V) * 10 ** 6, n, 'ppb')],
      ["%s mg / %s L = %s mg/L; &times; 1000 &mu;g/mg; 1 &mu;g/L &asymp; 1 ppb." % (mg, V, num(D(mg) / D(V), n)),
       "This is mg/L, which is ppm; convert to &mu;g/L for ppb.",
       "This converts to &mu;g but ignores the %s L volume." % V,
       "This multiplies by 10<sup>6</sup>, giving ng/L (ppt)."],
      "mg/L &rarr; &mu;g/L.",
      "%s mg/L &times; 1000 = <b>%s</b>." % (num(D(mg) / D(V), n), S(v, n, 'ppb')), 2, 1)

    g_, V = '4.75', '150.0'; mw = mm('MgCl2'); mol = D(g_) / mw; v = mol / L(V); n = ns(g_, V)
    Q(T, "What is the molarity of a solution made by dissolving %s g of {MgCl2} (%s g/mol) in enough water to make %s mL of solution?" % (g_, mw, V),
      [S(v, n, 'M'), S(mol / D(V), n, 'M'), S(D(g_) / L(V), n, 'M'), S(L(V) / mol, n, 'M')],
      ["%s g / %s g/mol = %s mol; &divide; %s L." % (g_, mw, num(mol, 4), Ls(V)),
       "This divides by mL; convert to L.",
       "This uses grams instead of moles.",
       "This divides liters by moles; molarity is mol / L."],
      "Grams to moles, mL to L.",
      "%s mol / %s L = <b>%s</b>." % (num(mol, 4), Ls(V), S(v, n, 'M')), 2, 1)

    g_, V = '18.9', '300.0'; mw = mm('NaHCO3'); mol = D(g_) / mw; v = mol / L(V); n = ns(g_, V)
    Q(T, "A hospital pharmacy dissolves %s g of {NaHCO3} (%s g/mol) in water to make %s mL of solution. What is the molarity?" % (g_, mw, V),
      [S(v, n, 'M'), S(mol / D(V), n, 'M'), S(D(g_) / L(V), n, 'M'), S(L(V) / mol, n, 'M')],
      ["%s g / %s g/mol = %s mol; &divide; %s L." % (g_, mw, num(mol, 4), Ls(V)),
       "This divides by mL instead of L.",
       "This divides grams by liters; convert grams to moles first.",
       "This divides liters by moles."],
      "M = mol / L of solution.",
      "%s mol / %s L = <b>%s</b>." % (num(mol, 4), Ls(V), S(v, n, 'M')), 2, 1)

    pc, d_ = '7.00', '1.05'; mw = mm('NaCl'); mol = D(pc) / mw; Vs = 100 / D(d_); v = mol / (Vs / 1000); n = ns(pc, d_)
    Q(T, "A %s%% (m/m) NaCl solution has a density of %s g/mL. What is its molarity? (NaCl, %s g/mol)" % (pc, d_, mw),
      [S(v, n, 'M'), S(mol / D('0.100'), n, 'M'), S(mol / (100 * D(d_) / 1000), n, 'M'), S(D(pc) / (Vs / 1000), n, 'M')],
      ["100. g of solution: %s g NaCl = %s mol; volume = 100. g &divide; %s g/mL = %s mL." % (pc, num(mol, 4), d_, num(Vs, 4)),
       "This takes 100. g of solution as 100. mL; use the density.",
       "This multiplies by the density; volume = mass &divide; density.",
       "This uses grams of NaCl instead of moles."],
      "Assume 100. g of solution.",
      "%s mol / %s L = <b>%s</b>." % (num(mol, 4), num(Vs / 1000, 4), S(v, n, 'M')), 3, 1)

    Q(T, "In dilute water solutions, a concentration of 1 ppb is about the same as which of these?",
      ["1 &mu;g per liter", "1 mg per liter", "1 g per liter", "1 ng per liter"],
      ["1 L of dilute water has a mass of about 1 kg = 10<sup>9</sup> &mu;g, so 1 &mu;g/L is 1 part per billion.",
       "1 mg/L is about 1 ppm.",
       "1 g/L is about 1 part per thousand, or 0.1%.",
       "1 ng/L is about 1 ppt (part per trillion)."],
      "1 L of dilute water is about 1 kg.",
      "<b>1 ppb &asymp; 1 &mu;g/L</b>.", 1)

    # ======================= ch11-dilution (8) =======================
    T = 'ch11-dilution'
    V, c_ = '42.5', '0.0875'; v = L(V) * D(c_); n = ns(V, c_)
    Q(T, "How many moles of KCl are in %s mL of %s M KCl?" % (V, c_),
      [S(v, n, 'mol'), S(D(V) * D(c_), n, 'mol'), S(L(V) / D(c_), n, 'mol'), S(D(c_) / L(V), n, 'mol')],
      ["mol = M &times; L = %s &times; %s L." % (c_, Ls(V)),
       "This uses mL in place of L.",
       "This divides the volume by the molarity.",
       "This divides the molarity by the volume."],
      "mol = M &times; V (L).",
      "%s L &times; %s mol/L = <b>%s</b>." % (Ls(V), c_, S(v, n, 'mol')), 1, 1)

    V, c_ = '100.0', '0.450'; mw = mm('Na2SO4'); mol = L(V) * D(c_); v = mol * mw; n = ns(V, c_)
    Q(T, "What mass of {Na2SO4} (%s g/mol) is needed to prepare %s mL of %s M {Na2SO4}?" % (mw, V, c_),
      [S(v, n, 'g'), S(D(V) * D(c_) * mw, n, 'g'), S(mol, n, 'g'), S(mol / mw, n, 'g')],
      ["%s L &times; %s M = %s mol; &times; %s g/mol." % (Ls(V), c_, num(mol, 4), mw),
       "This uses mL as liters.",
       "This stops at moles; multiply by the molar mass.",
       "This divides by the molar mass."],
      "L &rarr; mol &rarr; g.",
      "%s mol &times; %s g/mol = <b>%s</b>." % (num(mol, 4), mw, S(v, n, 'g')), 2, 1)

    V1, c1, V2 = '8.00', '1.35', '50.0'; v = D(c1) * D(V1) / D(V2); n = ns(V1, c1, V2)
    Q(T, "An %s mL portion of %s M NaCl is diluted to a total volume of %s mL. What is the new molarity?" % (V1, c1, V2),
      [S(v, n, 'M'), S(D(c1) * D(V2) / D(V1), n, 'M'), S(D(c1) * D(V1), n, 'M'), S(D(c1) * D(V1) / (D(V2) + D(V1)), n, 'M')],
      ["M<sub>2</sub> = M<sub>1</sub>V<sub>1</sub>/V<sub>2</sub>; %s mL is already the total volume." % V2,
       "This inverts the volumes; the diluted solution must be weaker.",
       "This is M<sub>1</sub>V<sub>1</sub> without dividing by V<sub>2</sub>.",
       "This adds %s mL to %s mL; the %s mL is already the total." % (V1, V2, V2)],
      "M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>.",
      "(%s)(%s) / %s = <b>%s</b>." % (c1, V1, V2, S(v, n, 'M')), 2, 1)

    c1, V2, c2 = '0.425', '200.0', '12.5'; v = D(c2) / 1000 * D(V2) / D(c1); n = ns(c1, V2, c2)
    Q(T, "How many milliliters of %s M KCl stock are needed to make %s mL of %s mM KCl?" % (c1, V2, c2),
      [S(v, n, 'mL'), S(D(c2) * D(V2) / D(c1), n, 'mL'), S(D(c1) * D(V2) / (D(c2) / 1000), n, 'mL'), S(D(c2) / 1000 * D(c1) / D(V2), n, 'mL')],
      ["%s mM = %s M; V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>/M<sub>1</sub>." % (c2, num(D(c2) / 1000, 3)),
       "This mixes mM and M; convert first.",
       "This puts M<sub>1</sub> on top.",
       "This divides by V<sub>2</sub>."],
      "Make the concentration units match.",
      "(%s)(%s) / %s = <b>%s</b>." % (num(D(c2) / 1000, 3), V2, c1, S(v, n, 'mL')), 2, 1)

    V1, c1, c2 = '50.0', '0.640', '0.160'; V2 = D(c1) * D(V1) / D(c2); n = ns(V1, c1, c2); V2s = num(V2, n); wa = addp(V2s, '-' + V1)
    Q(T, "A %s mL sample of %s M glucose is diluted to %s M. How much water must be added?" % (V1, c1, c2),
      [wa + ' mL', V2s + ' mL', S(D(c2) * D(V1) / D(c1), n, 'mL'), addp(V2s, V1) + ' mL'],
      ["V<sub>2</sub> = %s mL total; water = %s &minus; %s." % (V2s, V2s, V1),
       "This is the total volume, which includes the %s mL of stock." % V1,
       "This inverts the concentration ratio.",
       "This adds V<sub>1</sub> to V<sub>2</sub>; V<sub>2</sub> is already the total."],
      "Total volume from M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>, then subtract V<sub>1</sub>.",
      "V<sub>2</sub> = %s mL; water = <b>%s mL</b>." % (V2s, wa), 3, 1)

    mol, c_ = '1.50', '25.0'; mo = D(mol) / 10 ** 4; v = mo / (D(c_) / 1000) * 1000; n = ns(mol, c_)
    Q(T, "What volume of %s mM KCl contains %s &times; 10<sup>&minus;4</sup> mol of KCl? Give the answer in mL." % (c_, mol),
      [S(v, n, 'mL'), S(mo / (D(c_) / 1000), n, 'mL'), S(mo * D(c_) / 1000 * 1000, n, 'mL'), S(D(c_) / 1000 / mo * 1000, n, 'mL')],
      ["%s mM = %s M; V = mol &divide; M = %s L; &times; 1000 mL/L." % (c_, num(D(c_) / 1000, 3), num(mo / (D(c_) / 1000), n)),
       "This is the volume in liters with an mL label.",
       "This multiplies moles by molarity.",
       "This divides molarity by moles."],
      "Convert mM to M; V (L) = mol / M.",
      "%s L = <b>%s</b>." % (num(mo / (D(c_) / 1000), n), S(v, n, 'mL')), 2, 1)

    c0 = D('2.0'); v = c0 / 25
    Q(T, "A technician adds 1.0 mL of 2.0 M stock to 4.0 mL of water and mixes. Then 1.0 mL of that solution is added to another 4.0 mL of water. What is the final concentration?",
      [S(v, 2, 'M'), S(c0 / 5, 2, 'M'), S(c0 / 10, 2, 'M'), S(c0 / 16, 2, 'M')],
      ["Each step is 1.0 mL diluted to 5.0 mL total, a factor of 5; two steps: 5 &times; 5 = 25.",
       "This counts only one dilution.",
       "This adds the factors (5 + 5); dilution factors multiply.",
       "This divides by 4 each time, using the water added as V<sub>2</sub>; V<sub>2</sub> is the total, 5.0 mL."],
      "Each step: V<sub>2</sub> = 1.0 + 4.0 = 5.0 mL.",
      "2.0 M &divide; 25 = <b>%s</b>." % S(v, 2, 'M'), 3, 1)

    Q(T, "A student's dilution calculation gives a final concentration larger than the stock concentration. What most likely went wrong?",
      ["The volumes were swapped (V<sub>1</sub> and V<sub>2</sub> reversed).", "The student used the total volume as V<sub>2</sub>.",
       "The stock was diluted too much.", "Nothing; diluting can raise the concentration."],
      ["Dilution spreads the same moles through more volume, so M<sub>2</sub> must be smaller; a larger answer means the volumes are reversed.",
       "Using the total volume as V<sub>2</sub> is correct.",
       "Diluting too much would make the answer smaller, not larger.",
       "Adding solvent always lowers the concentration."],
      "Which way must the concentration change when solvent is added?",
      "M<sub>2</sub> &gt; M<sub>1</sub> is impossible: <b>the volumes were swapped</b>.", 2)

    # ======================= ch11-titration (7) =======================
    T = 'ch11-titration'
    Vs, cb_, i_, f_ = '12.00', '0.09850', '0.45', '19.80'; Vt = addp(f_, '-' + i_); mol = L(Vt) * D(cb_); v = mol / L(Vs); n = ns(Vt, cb_, Vs)
    Q(T, "In a sports-science lab, a %s mL sample of lactic acid solution, {HC3H5O3}, is titrated with %s M NaOH. The buret reads %s mL at the start and %s mL at the phenolphthalein endpoint. What is the molarity of the lactic acid? [[HC3H5O3(aq) + NaOH(aq) -> NaC3H5O3(aq) + H2O(l)]]" % (Vs, cb_, i_, f_),
      [S(v, n, 'M'), S(L(f_) * D(cb_) / L(Vs), n, 'M'), S(L(Vs) * D(cb_) / L(Vt), n, 'M'), S(mol / L(Vt), n, 'M')],
      ["Volume = %s &minus; %s = %s mL; mol NaOH = %s mol = mol lactic acid (1 : 1); &divide; %s L." % (f_, i_, Vt, num(mol, 4), Ls(Vs)),
       "This uses the final reading as the volume; subtract the initial reading.",
       "This swaps the acid and base volumes.",
       "This divides by the NaOH volume; divide by the volume of the acid sample."],
      "Volume used = final &minus; initial.",
      "%s mol / %s L = <b>%s</b>." % (num(mol, 4), Ls(Vs), S(v, n, 'M')), 2, 1)

    g_, Vb = '0.1700', '25.85'; mw = mm('H2C2O4'); ma = D(g_) / mw; v = ma * 2 / L(Vb); n = ns(g_, Vb)
    Q(T, "A %s g sample of oxalic acid, {H2C2O4} (%s g/mol), needs %s mL of NaOH to reach the endpoint. What is the molarity of the NaOH? [[H2C2O4(aq) + 2 NaOH(aq) -> Na2C2O4(aq) + 2 H2O(l)]]" % (g_, mw, Vb),
      [S(v, n, 'M'), S(ma / L(Vb), n, 'M'), S(ma / 2 / L(Vb), n, 'M'), S(D(g_) * 2 / L(Vb), n, 'M')],
      ["%s mol acid &times; 2 = %s mol NaOH; &divide; %s L." % (num(ma, 4), num(ma * 2, 4), Ls(Vb)),
       "This uses a 1 : 1 ratio; oxalic acid needs 2 NaOH.",
       "This flips the mole ratio.",
       "This uses grams as moles."],
      "Solid known: g &rarr; mol acid &rarr; &times; 2 &rarr; &divide; L.",
      "%s mol / %s L = <b>%s</b>." % (num(ma * 2, 4), Ls(Vb), S(v, n, 'M')), 3, 1)

    Va, cb_, Vb = '5.00', '0.1120', '18.24'; mb = L(Vb) * D(cb_); v = mb / 2 / L(Va); n = ns(Va, cb_, Vb)
    Q(T, "A %s mL sample of {H2SO4} needs %s mL of %s M NaOH to reach the endpoint. What is the molarity of the {H2SO4}? [[H2SO4(aq) + 2 NaOH(aq) -> Na2SO4(aq) + 2 H2O(l)]]" % (Va, Vb, cb_),
      [S(v, n, 'M'), S(mb / L(Va), n, 'M'), S(mb * 2 / L(Va), n, 'M'), S(mb / 2 / L(Vb), n, 'M')],
      ["mol NaOH = %s mol; &divide; 2 = %s mol {H2SO4}; &divide; %s L." % (num(mb, 4), num(mb / 2, 4), Ls(Va)),
       "This uses 1 : 1; {H2SO4} uses 2 NaOH per molecule.",
       "This multiplies by 2; divide moles of NaOH by 2 to get moles of acid.",
       "This divides by the NaOH volume."],
      "mol NaOH &rarr; &divide; 2 &rarr; &divide; L acid.",
      "%s mol / %s L = <b>%s</b>." % (num(mb / 2, 4), Ls(Va), S(v, n, 'M')), 3, 1)

    s_, cb_, Vb = '0.8125', '0.1088', '32.18'; mw = mm('KHC8H4O4'); mol = L(Vb) * D(cb_); gk = mol * mw; v = gk / D(s_) * 100; n = ns(s_, cb_, Vb)
    Q(T, "A %s g sample of impure potassium hydrogen phthalate, {KHC8H4O4} (KHP, %s g/mol), needs %s mL of %s M NaOH. What is the mass percent of KHP in the sample? [[KHC8H4O4(aq) + NaOH(aq) -> KNaC8H4O4(aq) + H2O(l)]]" % (s_, mw, Vb, cb_),
      [P(v, n), S(gk, n, 'g'), P(mol / D(s_) * 100, n), P(D(s_) / gk * 100, n)],
      ["mol = %s mol; &times; %s g/mol = %s g KHP; &divide; %s g &times; 100%%." % (num(mol, 4), mw, num(gk, 4), s_),
       "This is the mass of KHP, not the percent.",
       "This divides moles by grams.",
       "This divides the sample by the KHP mass."],
      "g KHP found &divide; sample mass &times; 100%.",
      "%s / %s &times; 100%% = <b>%s</b>." % (num(gk, 4), s_, P(v, n)), 3, 1)

    Va, ca, cb = '22.5', '0.140', '0.115'; mol = L(Va) * D(ca); v = mol * 3 / D(cb) * 1000; n = ns(Va, ca, cb)
    Q(T, "What volume of %s M {AgNO3} reacts completely with %s mL of %s M {AlCl3}? [[AlCl3(aq) + 3 AgNO3(aq) -> 3 AgCl(s) + Al(NO3)3(aq)]]" % (cb, Va, ca),
      [S(v, n, 'mL'), S(mol / D(cb) * 1000, n, 'mL'), S(mol / 3 / D(cb) * 1000, n, 'mL'), S(mol * 3 / D(ca) * 1000, n, 'mL')],
      ["mol {AlCl3} = %s mol; &times; 3 = %s mol {AgNO3}; &divide; %s M." % (num(mol, 4), num(mol * 3, 4), cb),
       "This skips the 1 : 3 mole ratio.",
       "This flips the mole ratio (divides by 3 instead of multiplying).",
       "This divides by the {AlCl3} molarity instead of the {AgNO3} molarity."],
      "Each {AlCl3} supplies 3 Cl<sup>&minus;</sup>, so it needs 3 {AgNO3}.",
      "%s mol &divide; %s M = <b>%s</b>." % (num(mol * 3, 4), cb, S(v, n, 'mL')), 3, 1)

    Q(T, "Why must a NaOH solution be standardized against a weighed solid acid before it is used in a titration?",
      ["NaOH slowly absorbs {CO2} from the air, so its molarity changes.", "NaOH is a weak base, so its molarity cannot be calculated.",
       "Phenolphthalein does not work with NaOH unless it is standardized.", "NaOH solutions get more concentrated as they sit."],
      ["{CO2} from the air reacts with some of the NaOH, so the exact molarity must be measured, for example with oxalic acid.",
       "NaOH is a strong base; the problem is that its concentration drifts.",
       "Phenolphthalein turns pink in any basic solution.",
       "Reaction with {CO2} uses up NaOH, so the molarity falls, not rises."],
      "What in the air reacts with a base?",
      "NaOH <b>absorbs {CO2}</b>, so its molarity must be checked.", 2)

    Q(T, "At the endpoint of a titration of HCl with NaOH, which statement is true?",
      ["The moles of NaOH added equal the moles of HCl in the flask.", "The volume of NaOH added equals the volume of HCl.",
       "The molarity of the NaOH equals the molarity of the HCl.", "The buret reads 0.00 mL."],
      ["HCl and NaOH react 1 : 1, so at the endpoint the moles match.",
       "Volumes match only if the molarities happen to be equal.",
       "The molarities can be different; it is the moles that match.",
       "The buret reads 0.00 at the top; at the endpoint the reading is the starting value plus the volume added."],
      "What does the balanced equation say about moles?",
      "<b>mol NaOH = mol HCl</b> (1 : 1).", 1)

    # ======================= ch11-colligative (7) =======================
    T = 'ch11-colligative'
    g_, w_ = '14.2', '315.0'; mw = mm('C3H8O3'); mol = D(g_) / mw; v = mol / (D(w_) / 1000); n = ns(g_, w_)
    Q(T, "What is the molality of a solution of %s g of glycerol ({C3H8O3}, %s g/mol) in %s g of water?" % (g_, mw, w_),
      [S(v, n, 'm'), S(mol / D(w_), n, 'm'), S(D(g_) / (D(w_) / 1000), n, 'm'), S(mol / ((D(g_) + D(w_)) / 1000), n, 'm')],
      ["%s mol / %s kg water." % (num(mol, 4), num(D(w_) / 1000, 4)),
       "This divides by grams of water.",
       "This uses grams of glycerol.",
       "This divides by the whole solution; molality uses the solvent only."],
      "m = mol solute / kg solvent.",
      "%s mol / %s kg = <b>%s</b>." % (num(mol, 4), num(D(w_) / 1000, 4), S(v, n, 'm')), 2, 1)

    m_ = '0.215'; dT = 4 * KF * D(m_)
    Q(T, "What is the freezing point of a %s m {AlCl3} solution in water, assuming complete dissociation? (K<sub>f</sub> = 1.86 °C/m)" % m_,
      [tf(dT) + ' °C', qd(dT, 2) + ' °C', tf(KF * D(m_)) + ' °C', tf(4 * KB * D(m_)) + ' °C'],
      ["{AlCl3} gives 4 ions (i = 4): &Delta;T<sub>f</sub> = (4)(1.86)(%s) = %s °C." % (m_, num(dT, 3)),
       "This adds instead of subtracting; the freezing point goes down.",
       "This forgets i = 4.",
       "This uses K<sub>b</sub>."],
      "&Delta;T<sub>f</sub> = iK<sub>f</sub>m; subtract from 0.00 °C.",
      "T<sub>f</sub> = 0.00 &minus; %s = <b>%s °C</b>." % (num(dT, 3), tf(dT)), 2, 1)

    Q(T, "Which aqueous solution has the <b>highest</b> boiling point?",
      ["0.10 m {Na2SO4}", "0.25 m sucrose", "0.12 m KBr", "0.075 m {MgCl2}"],
      ["i &times; m = 3 &times; 0.10 = 0.30 m of particles, the most.",
       "Sucrose is a nonelectrolyte (i = 1): 0.25 m of particles.",
       "KBr gives 2 ions: 2 &times; 0.12 = 0.24 m of particles.",
       "{MgCl2} gives 3 ions: 3 &times; 0.075 = 0.225 m of particles."],
      "Compare i &times; m.",
      "Most particles: <b>0.10 m {Na2SO4}</b> (0.30 m).", 3)

    m_ = '0.0850'; v = D(m_) * 3 * 1000
    Q(T, "What is the osmolality of a %s m {Na2SO4} solution in mOsm/kg, assuming complete dissociation?" % m_,
      [S(v, 3, 'mOsm/kg'), S(D(m_) * 1000, 3, 'mOsm/kg'), S(D(m_) * 2 * 1000, 3, 'mOsm/kg'), S(D(m_) * 3, 3, 'mOsm/kg')],
      ["{Na2SO4} gives 3 ions (i = 3): 3 &times; %s = %s Osm/kg." % (m_, num(D(m_) * 3, 3)),
       "This forgets i.",
       "This uses i = 2; {Na2SO4} gives 2 Na<sup>+</sup> + 1 SO<sub>4</sub><sup>2&minus;</sup>.",
       "This is in Osm/kg; &times; 1000 for mOsm/kg."],
      "Osmolality = i &times; m.",
      "3 &times; %s = <b>%s</b>." % (m_, S(v, 3, 'mOsm/kg')), 2, 1)

    Q(T, "Red blood cells are placed in 0.45% NaCl (half-normal saline), which has about half the particle concentration of normal saline. How is the fluid described, and what happens to the cells?",
      ["Hypotonic: water flows into the cells, and they swell", "Hypertonic: water flows out of the cells, and they shrink",
       "Isotonic: no net water flow", "Hypotonic: water flows out of the cells, and they shrink"],
      ["About half of 0.9% NaCl's particle concentration is below serum's 275&ndash;295 mOsm/kg, so water moves toward the higher particle concentration inside the cells. (Context only; IV fluids are given exactly as ordered.)",
       "A hypertonic fluid has <i>more</i> particles than the cells, such as 3% NaCl.",
       "0.9% NaCl is isotonic; half that concentration is not.",
       "The label is right, but the direction is reversed: water moves <i>into</i> cells in a hypotonic fluid."],
      "Water follows solute. Which side has more particles?",
      "Fewer particles outside: <b>hypotonic, water flows in, and the cells swell</b>.", 2)

    Tf = '12.0'; v = D(Tf) / KF
    Q(T, "Propylene glycol, a nonelectrolyte, is used in RV antifreeze because it is less toxic than ethylene glycol. What molality of propylene glycol in water freezes at &minus;12.0 °C? (K<sub>f</sub> = 1.86 °C/m)",
      [S(v, 3, 'm'), S(D(Tf) / (2 * KF), 3, 'm'), S(D(Tf) / KB, 3, 'm'), S(KF * D(Tf), 3, 'm')],
      ["i = 1; m = &Delta;T<sub>f</sub> / K<sub>f</sub> = 12.0 / 1.86.",
       "This uses i = 2; propylene glycol is molecular (i = 1).",
       "This uses K<sub>b</sub>.",
       "This multiplies by K<sub>f</sub>; divide."],
      "Solve &Delta;T<sub>f</sub> = iK<sub>f</sub>m for m.",
      "12.0 / 1.86 = <b>%s</b>." % S(v, 3, 'm'), 2, 1)

    Q(T, "A membrane that lets only water pass separates 0.10 m NaCl from 0.10 m glucose. Which way does water flow by osmosis?",
      ["Toward the NaCl side, because it has twice the particle concentration", "Toward the glucose side, because glucose molecules are larger",
       "Neither way, because the molalities are equal", "Toward the glucose side, because water moves toward the lower particle concentration"],
      ["NaCl gives 2 ions (i = 2): 0.20 m of particles, versus 0.10 m for glucose. Water follows solute.",
       "Particle size does not matter; only the number of particles does.",
       "Equal molality, but NaCl makes twice as many particles.",
       "This reverses osmosis; water moves toward the higher particle concentration."],
      "Count particles with i.",
      "0.20 m vs 0.10 m of particles: <b>toward the NaCl side</b>.", 3)


if __name__ == '__main__':
    build_hw()
    dump(sys.argv[1])
