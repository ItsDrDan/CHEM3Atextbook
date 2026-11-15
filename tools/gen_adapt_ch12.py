#!/usr/bin/env python3
"""Builds bank/ch12_adapt.json (Chapter 12 ADAPT homework-only items, text only; 42 items, none repeated from
bank/ch12.json).
usage: python3 tools/gen_adapt_ch12.py bank/ch12_adapt.json
Same conventions, helpers and markup as tools/gen_bank_ch12.py (imported from it): strong acid and base lists from
12.3; H3O+ notation; Kw = 1.0 x 10^-14 at 25 C; pH + pOH = 14.00; decimal places in pH = significant figures in the
concentration; indicator colors from 12.1; qualitative buffers. y[0] begins "Correct: ". Every item is rechecked by
tools/check_bank_ch12.py."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bank_ch12 import *
import gen_bank_ch12 as G
G.CFG.update(prefix='c12-h%02d', adapt=True)


def build_hw():
    # ======================= ch12-props (6) =======================
    T = 'ch12-props'
    Q(T, "A drop of household ammonia is placed on a strip of red litmus paper. What color does the strip turn, and why?",
      ["Blue, because ammonia is a base", "It stays red, because ammonia is a base", "Blue, because ammonia is an acid", "It stays red, because ammonia is neutral"],
      ["Bases turn red litmus blue; household ammonia (pH about 11.5) is basic.",
       "A base does change red litmus: it turns it blue.",
       "The color is right, but the reason is wrong: acids turn <i>blue</i> litmus red.",
       "Household ammonia is basic, not neutral, so the red litmus changes color."],
      "Which kind of substance turns red litmus blue?",
      "Ammonia is a base: red litmus turns <b>blue</b>.", 1)

    Q(T, "During a titration of an acid with NaOH, phenolphthalein is in the flask. The solution turns light pink and stays pink. What does this tell you?",
      ["All the acid has been used up, and a slight excess of base is present.", "The solution is still acidic.",
       "The acid is in excess, so more acid must be added.", "The solution is exactly neutral."],
      ["Phenolphthalein turns pink only in base (above about pH 8), so the first lasting pink marks the endpoint.",
       "In an acidic solution phenolphthalein stays colorless.",
       "Pink means base is in excess, not acid.",
       "Phenolphthalein is colorless at neutral; the pink appears once a little extra base is present."],
      "&ldquo;Pink means base.&rdquo;",
      "Lasting pink: <b>the acid is used up, and a little base is in excess</b>.", 2)

    Q(T, "Red cabbage indicator turns <b>yellow</b> in a sample. Which sample could it be?",
      ["Drain cleaner (sodium hydroxide solution)", "Lemon juice", "Pure water", "Vinegar"],
      ["Red cabbage turns yellow at pH 12&ndash;14, a strong base such as drain cleaner.",
       "Lemon juice (about pH 2) turns red cabbage red.",
       "Neutral water leaves the indicator purple.",
       "Vinegar (about pH 3) turns red cabbage pink."],
      "Red cabbage: red and pink in acid, purple near neutral, then blue, green, yellow toward strong base.",
      "Yellow = pH 12&ndash;14: <b>drain cleaner</b>.", 1)

    Q(T, "A zinc strip is placed in dilute sulfuric acid, and the zinc slowly dissolves. Which gas bubbles off?",
      ["Hydrogen, {H2}", "Carbon dioxide, {CO2}", "Oxygen, {O2}", "Sulfur trioxide, {SO3}"],
      ["Acid + active metal &rarr; salt + hydrogen: [[Zn(s) + H2SO4(aq) -> ZnSO4(aq) + H2(g)]].",
       "{CO2} forms when an acid reacts with a carbonate; there is no carbon here.",
       "Oxygen is not released; the metal takes the place of the acid's hydrogen.",
       "The sulfate stays in solution as {ZnSO4}; no sulfur gas forms."],
      "Acid + active metal gives a salt and which gas?",
      "[[Zn(s) + H2SO4(aq) -> ZnSO4(aq) + H2(g)]]: <b>hydrogen gas</b>.", 1)

    Q(T, "Which property belongs to acids rather than to bases?",
      ["Reacts with zinc metal to release hydrogen gas", "Feels slippery or soapy", "Turns red litmus paper blue", "Turns phenolphthalein pink"],
      ["Acids react with active metals such as Zn, Mg, and Fe to make {H2} gas.",
       "A slippery, soapy feel is a property of bases.",
       "Turning red litmus blue is the test for a base.",
       "Phenolphthalein turns pink only in bases."],
      "Three of these describe bases.",
      "<b>Reacting with an active metal to give {H2}</b> is an acid property.", 1)

    Q(T, "Potassium carbonate, {K2CO3}, reacts with hydrochloric acid. In the balanced equation, how many moles of HCl react with 1 mol of {K2CO3}?",
      ["2", "1", "3", "4"],
      ["[[K2CO3(s) + 2 HCl(aq) -> 2 KCl(aq) + H2O(l) + CO2(g)]]: carbonate (2&minus;) takes two H<sup>+</sup>.",
       "One HCl would leave the K atoms and the carbonate's charge unbalanced; {K2CO3} needs two H<sup>+</sup>.",
       "This counts the three O atoms in carbonate; the number of H<sup>+</sup> needed equals the charge, 2.",
       "Count the K and Cl atoms: two KCl need only two HCl."],
      "Balance K and Cl after writing the products salt + water + {CO2}.",
      "[[K2CO3(s) + 2 HCl(aq) -> 2 KCl(aq) + H2O(l) + CO2(g)]]: <b>2</b> mol HCl.", 2)

    # ======================= ch12-bl (7) =======================
    T = 'ch12-bl'
    Q(T, "What role does water play in this reaction?<br>[[HClO4(aq) + H2O(l) -> H3O^+(aq) + ClO4^-(aq)]]",
      ["A base: it accepts a proton and becomes {H3O^+}.", "An acid: it donates a proton.",
       "The conjugate base of {HClO4}.", "A spectator: it does not take part."],
      ["{HClO4} gives its H<sup>+</sup> to water, so water is the proton acceptor.",
       "Water would be the acid if it lost an H and became {OH^-}; here it gains one.",
       "The conjugate base of {HClO4} is {ClO4^-}, on the product side.",
       "Water gains a proton here, so it is a reactant that takes part."],
      "Does water gain or lose an H from left to right?",
      "{H2O} becomes {H3O^+}: water is the <b>base (proton acceptor)</b>.", 1)

    Q(T, "In the reaction below, which species is the <b>conjugate acid</b>?<br>[[HSO4^-(aq) + CO3^2-(aq) <=> SO4^2-(aq) + HCO3^-(aq)]]",
      ["{HCO3^-}", "{SO4^2-}", "{HSO4^-}", "{CO3^2-}"],
      ["Carbonate (the base) gains H<sup>+</sup> and becomes {HCO3^-}, its conjugate acid.",
       "{SO4^2-} is what is left after the acid donates its proton: the conjugate base.",
       "{HSO4^-} is the acid (the proton donor) on the reactant side.",
       "{CO3^2-} is the base on the reactant side."],
      "The conjugate acid is the product formed when the base gains H<sup>+</sup>.",
      "{CO3^2-} + H<sup>+</sup> &rarr; {HCO3^-}: <b>{HCO3^-}</b> is the conjugate acid.", 3)

    Q(T, "Lactic acid, {HC3H5O3}, is made by hard-working muscles. What is its conjugate base?",
      ["{C3H5O3^-}", "{C3H5O3}", "{H2C3H5O3^+}", "{HC3H5O3^-}"],
      ["Remove the acidic H<sup>+</sup>: one fewer H and a charge of 1&minus;. This is the lactate ion.",
       "This removes the H but forgets the 1&minus; charge.",
       "This adds H<sup>+</sup> to the acid, which never gives its conjugate base.",
       "This changes the charge without removing the H."],
      "Conjugate base: one fewer H, charge one lower.",
      "{HC3H5O3} &minus; H<sup>+</sup> = <b>{C3H5O3^-}</b> (lactate).", 2)

    Q(T, "What is the conjugate acid of the nitrite ion, {NO2^-}?",
      ["{HNO2}", "{HNO2^-}", "{NO2^2-}", "{H2NO2^+}"],
      ["Add one H<sup>+</sup>: one more H, and the charge rises from 1&minus; to 0 (nitrous acid).",
       "This adds the H but keeps the 1&minus; charge.",
       "This lowers the charge, as if a proton had been removed, but nitrite has no H to remove.",
       "This adds two H<sup>+</sup>."],
      "Conjugate acid: one more H, charge one higher.",
      "{NO2^-} + H<sup>+</sup> = <b>{HNO2}</b>.", 2)

    Q(T, "Which pair is <b>not</b> a conjugate acid&ndash;base pair?",
      ["{H2SO4} and {SO4^2-}", "{HSO4^-} and {SO4^2-}", "{NH4^+} and {NH3}", "{H2O} and {OH^-}"],
      ["These differ by two H<sup>+</sup>; a conjugate pair differs by exactly one.",
       "These differ by one H<sup>+</sup> (one H, one unit of charge): a pair.",
       "These differ by one H<sup>+</sup>: a pair.",
       "These differ by one H<sup>+</sup>: a pair."],
      "Count the H atoms and the charges in each pair.",
      "{H2SO4} and {SO4^2-} differ by two protons: <b>not a pair</b>.", 2)

    Q(T, "Which equation shows a substance acting as an <b>Arrhenius acid</b>?",
      ["[[HBr(aq) -> H^+(aq) + Br^-(aq)]]", "[[KOH(aq) -> K^+(aq) + OH^-(aq)]]",
       "[[NaCl(s) -> Na^+(aq) + Cl^-(aq)]]", "[[CH3OH(l) -> CH3OH(aq)]]"],
      ["An Arrhenius acid produces H<sup>+</sup> in water, as HBr does.",
       "KOH produces OH<sup>&minus;</sup>: an Arrhenius base.",
       "NaCl is a salt; it gives neither H<sup>+</sup> nor OH<sup>&minus;</sup>.",
       "Methanol dissolves as whole molecules; it makes no ions."],
      "Arrhenius acids make H<sup>+</sup> in water.",
      "<b>HBr &rarr; H<sup>+</sup> + Br<sup>&minus;</sup></b>.", 1)

    Q(T, "A student says, &ldquo;{NH3} has three hydrogen atoms, so it must be an acid.&rdquo; What is wrong with this reasoning?",
      ["Having H atoms does not make a substance an acid; {NH3} accepts a proton, so it is a base.",
       "Nothing; {NH3} donates its H atoms in water.",
       "{NH3} is an acid only in the Arrhenius definition.",
       "{NH3} is neutral, so it is neither an acid nor a base."],
      ["An acid must <i>donate</i> H<sup>+</sup>; ammonia's lone pair takes an H<sup>+</sup> and forms {NH4^+}.",
       "Ammonia gains an H in water ({NH3} becomes {NH4^+}); it does not lose one.",
       "Ammonia is not an Arrhenius acid or base; it is a Br&oslash;nsted&ndash;Lowry base.",
       "Ammonia turns red litmus blue and neutralizes acids: it is a base."],
      "Does {NH3} gain or lose an H<sup>+</sup> in water?",
      "<b>H atoms alone do not make an acid; {NH3} is a proton acceptor (base)</b>.", 2)

    # ======================= ch12-strength (7) =======================
    T = 'ch12-strength'
    Q(T, "Which compound is a <b>weak</b> base?",
      ["{NH3}", "NaOH", "KOH", "{Ba(OH)2}"],
      ["Ammonia accepts protons from water only to a small extent: a weak base.",
       "NaOH is a Group 1 hydroxide: a strong base.",
       "KOH is a Group 1 hydroxide: a strong base.",
       "{Ba(OH)2} is on the strong-base list."],
      "Strong bases are the Group 1 hydroxides plus Ca, Sr, and Ba hydroxides.",
      "<b>{NH3}</b> is a weak base.", 1)

    Q(T, "Which acid is <b>strong</b>?",
      ["HBr", "{HNO2}", "HF", "{H2CO3}"],
      ["Hydrobromic acid is on the green sheet's list of six strong acids.",
       "{HNO2} (nitrous acid) is not {HNO3}; it is weak.",
       "HF is weak, even though HCl, HBr, and HI are strong.",
       "Carbonic acid is weak; it is the acid partner of the blood buffer."],
      "Strong acids: HCl, HBr, HI, {HNO3}, {HClO4}, {H2SO4}.",
      "<b>HBr</b> is strong.", 1)

    Q(T, "Perchloric acid, {HClO4}, is dissolved in water. Which particles are present in significant amounts (besides water)?",
      ["{H3O^+} and {ClO4^-} only", "Mostly {HClO4} molecules, with a few ions", "{HClO4} molecules only",
       "{H3O^+}, {ClO4^-}, and about as many intact {HClO4} molecules"],
      ["{HClO4} is a strong acid: it ionizes completely, leaving essentially no intact molecules.",
       "Mostly molecules describes a weak acid.",
       "A strong acid does not stay as molecules; it ionizes completely.",
       "A strong acid leaves essentially no intact molecules."],
      "Is {HClO4} on the strong-acid list?",
      "Strong acid, complete ionization: <b>{H3O^+} and {ClO4^-} only</b>.", 2)

    Q(T, "How is ammonium bromide, {NH4Br}, classified?",
      ["A salt", "An acid, because its formula contains hydrogen", "A base, because it contains nitrogen like {NH3}", "Neither an acid, a base, nor a salt"],
      ["It is ionic: the cation {NH4^+} comes from the base {NH3}, and Br<sup>&minus;</sup> comes from HBr.",
       "Its H atoms are in the ammonium ion, not written first as an acidic H.",
       "{NH4^+} has already accepted its proton; the compound is the salt of {NH3} and HBr.",
       "A metal ion or {NH4^+} paired with an acid's anion makes an ionic compound of that kind."],
      "Salt = a base's cation + an acid's anion; {NH4^+} counts as the cation.",
      "{NH4^+} + Br<sup>&minus;</sup>: <b>a salt</b>.", 2)

    Q(T, "Perchloric acid neutralizes lithium hydroxide. What salt forms?",
      ["{LiClO4}", "LiCl", "{LiClO3}", "{Li(ClO4)2}"],
      ["Li<sup>+</sup> and {ClO4^-} combine 1 : 1: [[HClO4(aq) + LiOH(aq) -> LiClO4(aq) + H2O(l)]].",
       "This loses the oxygen atoms; the anion is perchlorate, {ClO4^-}, not chloride.",
       "This is chlorate; perchloric acid's anion has four O atoms.",
       "Li<sup>+</sup> has a 1+ charge, so one perchlorate balances it."],
      "Base's cation + acid's anion, charges balanced.",
      "[[HClO4(aq) + LiOH(aq) -> LiClO4(aq) + H2O(l)]]: <b>{LiClO4}</b>.", 2)

    Q(T, "Which hydroxide is <b>not</b> a strong base, according to the CHEM 3A list?",
      ["{Mg(OH)2}", "KOH", "{Sr(OH)2}", "{Ba(OH)2}"],
      ["Magnesium hydroxide is not on the strong-base list; the antacid milk of magnesia is a weak, poorly soluble base.",
       "KOH is a Group 1 hydroxide: strong.",
       "{Sr(OH)2} is on the strong-base list.",
       "{Ba(OH)2} is on the strong-base list."],
      "Strong bases: Group 1 hydroxides plus Ca, Sr, and Ba hydroxides.",
      "Mg is not on the list: <b>{Mg(OH)2}</b>.", 2)

    Q(T, "Four solutions each have a concentration of 0.10 M. Which one conducts electricity only weakly?",
      ["HF", "HCl", "NaOH", "{KNO3}"],
      ["HF is a weak acid, so it makes only a few ions: a weak electrolyte.",
       "HCl is a strong acid: all ions, a strong electrolyte.",
       "NaOH is a strong base: all ions.",
       "{KNO3} is a soluble salt: all ions."],
      "Weak acids and bases are weak electrolytes.",
      "<b>HF</b>, a weak acid, conducts weakly.", 2)

    # ======================= ch12-water (7) =======================
    T = 'ch12-water'
    h = V('8.3', -6)
    Q(T, "A sample of rainwater has [{H3O^+}] = " + sci('8.3', -6) + " M at 25 °C. What is [{OH^-}]?",
      [S(KW / h, 2), S(KW * h, 2), S(h / KW, 2), sci('1.0', -7) + ' M'],
      ["[{OH^-}] = 1.0 &times; 10<sup>&minus;14</sup> / 8.3 &times; 10<sup>&minus;6</sup>; two significant figures.",
       "This multiplies by K<sub>w</sub> instead of dividing.",
       "This divides the wrong way.",
       "This is [{OH^-}] in pure water; acidic rain has less."],
      "[{OH^-}] = K<sub>w</sub> / [{H3O^+}].",
      "1.0 &times; 10<sup>&minus;14</sup> / 8.3 &times; 10<sup>&minus;6</sup> = <b>%s</b>." % S(KW / h, 2), 2, 1)

    o = V('1.9', -4)
    Q(T, "A diluted bleach solution has [{OH^-}] = " + sci('1.9', -4) + " M at 25 °C. What is [{H3O^+}]?",
      [S(KW / o, 2), S(KW * o, 2), S(1 / o, 2), S(o / KW, 2)],
      ["[{H3O^+}] = 1.0 &times; 10<sup>&minus;14</sup> / 1.9 &times; 10<sup>&minus;4</sup>.",
       "This multiplies by K<sub>w</sub>.",
       "This leaves K<sub>w</sub> out (1 / [{OH^-}]).",
       "This divides [{OH^-}] by K<sub>w</sub>."],
      "Divide K<sub>w</sub> by [{OH^-}].",
      "1.0 &times; 10<sup>&minus;14</sup> / 1.9 &times; 10<sup>&minus;4</sup> = <b>%s</b>." % S(KW / o, 2), 2, 1)

    Q(T, "A solution has [{OH^-}] = " + sci('4.8', -8) + " M at 25 °C. How is it classified?",
      ["Acidic", "Basic", "Neutral", "Basic, because it contains {OH^-} ions"],
      ["[{OH^-}] is below 1.0 &times; 10<sup>&minus;7</sup> M, so [{H3O^+}] is above it: acidic (slightly).",
       "Basic would need [{OH^-}] above 1.0 &times; 10<sup>&minus;7</sup> M; 4.8 &times; 10<sup>&minus;8</sup> is smaller.",
       "Neutral means [{OH^-}] = 1.0 &times; 10<sup>&minus;7</sup> M exactly.",
       "Every water solution contains {OH^-}; what matters is whether it is above or below 10<sup>&minus;7</sup> M."],
      "4.8 &times; 10<sup>&minus;8</sup> = 0.48 &times; 10<sup>&minus;7</sup>. Is that above or below 10<sup>&minus;7</sup>?",
      "[{OH^-}] &lt; 1.0 &times; 10<sup>&minus;7</sup> M: <b>acidic</b>.", 2)

    b = D('0.0082')
    Q(T, "What is [{H3O^+}] in 0.0082 M KOH at 25 °C?",
      [S(KW / b, 2), '0.0082 M', S(KW * b, 2), S(KW / (2 * b), 2)],
      ["KOH is a strong base with one OH<sup>&minus;</sup>: [{OH^-}] = 0.0082 M; [{H3O^+}] = 1.0 &times; 10<sup>&minus;14</sup> / 0.0082.",
       "0.0082 M is [{OH^-}], not [{H3O^+}].",
       "This multiplies by K<sub>w</sub>.",
       "This doubles [{OH^-}]; KOH has only one OH<sup>&minus;</sup>."],
      "Strong base: [{OH^-}] = molarity &times; number of OH<sup>&minus;</sup>.",
      "1.0 &times; 10<sup>&minus;14</sup> / 0.0082 = <b>%s</b>." % S(KW / b, 2), 2, 1)

    b = D('0.0026')
    Q(T, "What is [{H3O^+}] in 0.0026 M {Sr(OH)2} at 25 °C?",
      [S(KW / (2 * b), 2), S(KW / b, 2), S(2 * b, 2), S(KW * b, 2)],
      ["[{OH^-}] = 2 &times; 0.0026 = 0.0052 M; [{H3O^+}] = 1.0 &times; 10<sup>&minus;14</sup> / 0.0052.",
       "This forgets to double: {Sr(OH)2} releases two OH<sup>&minus;</sup>.",
       "0.0052 M is [{OH^-}].",
       "This multiplies by K<sub>w</sub> (and forgets to double)."],
      "Double first, then use K<sub>w</sub>.",
      "[{OH^-}] = 0.0052 M; [{H3O^+}] = <b>%s</b>." % S(KW / (2 * b), 2), 3, 1)

    Q(T, "Pure water contains {H3O^+} and {OH^-} ions. Why is it neutral?",
      ["[{H3O^+}] equals [{OH^-}], so neither ion is in excess.", "It contains no ions at all.",
       "Its [{H3O^+}] is exactly 7 M.", "Its ions are too few to count, so they are ignored."],
      ["Autoionization makes one {H3O^+} for every {OH^-}: 1.0 &times; 10<sup>&minus;7</sup> M each at 25 °C.",
       "The question itself notes the ions; pure water does autoionize slightly.",
       "7 is the pH; [{H3O^+}] is 1.0 &times; 10<sup>&minus;7</sup> M.",
       "The ions are few, but neutral is defined by their being equal, not by their being ignored."],
      "Neutral is defined by comparing the two ions.",
      "<b>[{H3O^+}] = [{OH^-}]</b>, so pure water is neutral.", 1)

    Q(T, "Solution X has [{OH^-}] = 1 &times; 10<sup>&minus;4</sup> M, and solution Y has [{H3O^+}] = 1 &times; 10<sup>&minus;9</sup> M (both at 25 °C). Which is more basic?",
      ["X, because its [{OH^-}] (10<sup>&minus;4</sup> M) is larger than Y's (10<sup>&minus;5</sup> M)",
       "Y, because 10<sup>&minus;9</sup> is a smaller number", "They are equally basic", "Neither; both are acidic"],
      ["For Y, [{OH^-}] = 10<sup>&minus;14</sup> / 10<sup>&minus;9</sup> = 10<sup>&minus;5</sup> M; X has 10 times more {OH^-}.",
       "Comparing [{H3O^+}] in Y with [{OH^-}] in X mixes two different ions; convert first.",
       "X has [{H3O^+}] = 10<sup>&minus;10</sup> M and Y has 10<sup>&minus;9</sup> M, so they differ by 10 times.",
       "Both have [{H3O^+}] below 10<sup>&minus;7</sup> M, so both are basic."],
      "Convert both to the same ion with K<sub>w</sub>.",
      "X: [{OH^-}] 10<sup>&minus;4</sup> M; Y: 10<sup>&minus;5</sup> M: <b>X</b> is more basic.", 3)

    # ======================= ch12-ph (9) =======================
    T = 'ch12-ph'
    a = D('0.0058')
    Q(T, "What is the pH of 0.0058 M HI?",
      [p(a, 2), qd(D(a).log10(), 2), qd(14 + D(a).log10(), 2), p(a, 3)],
      ["HI is a strong acid: [{H3O^+}] = 0.0058 M; 2 significant figures give 2 decimal places.",
       "This drops the minus sign in pH = &minus;log[{H3O^+}].",
       "This is the pOH (14.00 &minus; pH).",
       "This has 3 decimal places; 0.0058 has only 2 significant figures."],
      "pH = &minus;log[{H3O^+}].",
      "&minus;log(0.0058) = <b>%s</b>." % p(a, 2), 2, 1)

    a = V('1.35', -4)
    Q(T, "What is the pH of " + sci('1.35', -4) + " M {HClO4}?",
      [p(a, 3), p(a, 2), qd(D(a).log10(), 3), qd(14 + D(a).log10(), 3)],
      ["{HClO4} is strong; 3 significant figures in 1.35 give 3 decimal places.",
       "This has 2 decimal places; the concentration has 3 significant figures.",
       "This drops the minus sign.",
       "This is the pOH."],
      "Decimal places in pH = significant figures in [{H3O^+}].",
      "&minus;log(1.35 &times; 10<sup>&minus;4</sup>) = <b>%s</b>." % p(a, 3), 2, 1)

    b = D('0.0059')
    Q(T, "What is the pH of 0.0059 M KOH at 25 °C?",
      [sub14(p(b, 2)), p(b, 2), sub14(p(2 * b, 2)), qd(D(sub14(p(b, 2))), 1)],
      ["pOH = &minus;log(0.0059) = %s; pH = 14.00 &minus; %s." % (p(b, 2), p(b, 2)),
       "This is the pOH, not the pH.",
       "This doubles [{OH^-}]; KOH has one OH<sup>&minus;</sup>.",
       "This has one decimal place; the concentration has 2 significant figures."],
      "[{OH^-}] &rarr; pOH &rarr; pH = 14.00 &minus; pOH.",
      "pOH = %s; pH = <b>%s</b>." % (p(b, 2), sub14(p(b, 2))), 2, 1)

    b = D('0.0024')
    Q(T, "What is the pH of 0.0024 M {Sr(OH)2} at 25 °C?",
      [sub14(p(2 * b, 2)), sub14(p(b, 2)), p(2 * b, 2), qd(-D(sub14(p(2 * b, 2))), 2)],
      ["[{OH^-}] = 2 &times; 0.0024 = 0.0048 M; pOH = %s; pH = 14.00 &minus; %s." % (p(2 * b, 2), p(2 * b, 2)),
       "This forgets the factor of 2 for {Sr(OH)2}.",
       "This is the pOH.",
       "A negative pH for a dilute base means a dropped minus sign; this solution is basic."],
      "Two OH<sup>&minus;</sup> per {Sr(OH)2}.",
      "[{OH^-}] = 0.0048 M; pOH = %s; pH = <b>%s</b>." % (p(2 * b, 2), sub14(p(2 * b, 2))), 3, 1)

    pv = '6.62'
    Q(T, "A sample of milk has pH 6.62. What is its [{H3O^+}]?",
      [S(ten(pv), 2), S(ten(sub14(pv)), 2), S(D(10) ** D(pv), 2), S(ten(pv), 3)],
      ["[{H3O^+}] = 10<sup>&minus;6.62</sup>; 2 decimal places give 2 significant figures.",
       "This is 10<sup>&minus;(14 &minus; pH)</sup> = [{OH^-}].",
       "This drops the minus sign: 10<sup>6.62</sup>.",
       "This has 3 significant figures; the pH has only 2 decimal places."],
      "[{H3O^+}] = 10<sup>&minus;pH</sup>.",
      "10<sup>&minus;6.62</sup> = <b>%s</b>." % S(ten(pv), 2), 2, 1)

    pv = '10.85'
    Q(T, "A floor cleaner has pH 10.85 at 25 °C. What is its [{OH^-}]?",
      [S(ten(sub14(pv)), 2), S(ten(pv), 2), sub14(pv) + ' M', S(ten(sub14(pv)), 3)],
      ["pOH = 14.00 &minus; 10.85 = 3.15; [{OH^-}] = 10<sup>&minus;3.15</sup>.",
       "10<sup>&minus;10.85</sup> is [{H3O^+}].",
       "3.15 is the pOH, not a concentration.",
       "This has 3 significant figures; 2 decimal places give 2."],
      "pOH first, then 10<sup>&minus;pOH</sup>.",
      "pOH = 3.15; [{OH^-}] = <b>%s</b>." % S(ten(sub14(pv)), 2), 3, 1)

    Q(T, "Two soil samples from a San Joaquin Valley farm have pH 8.5 and pH 6.5. Which has more {H3O^+}, and by what factor?",
      ["The pH 6.5 soil, by a factor of 100", "The pH 8.5 soil, by a factor of 100", "The pH 6.5 soil, by a factor of 2", "The pH 6.5 soil, by a factor of about 1.3"],
      ["2 pH units apart: 10<sup>2</sup> = 100, and the lower pH has more {H3O^+}.",
       "The factor is right, but the higher pH has <i>less</i> {H3O^+}.",
       "pH is logarithmic: 2 units is a factor of 100, not 2.",
       "This divides the pH values (8.5 / 6.5); compare powers of 10 instead."],
      "Each pH unit is a factor of 10.",
      "10<sup>8.5 &minus; 6.5</sup> = 100: <b>the pH 6.5 soil, 100 times</b>.", 2)

    Q(T, "An arterial blood gas shows pH 7.33. How is this described?",
      ["Acidosis, because it is below 7.35", "Normal, because it is above 7 and so slightly basic",
       "Alkalosis, because it is above 7", "Normal, because it is within 7.35&ndash;7.45"],
      ["Normal arterial pH is 7.35&ndash;7.45; below 7.35 is acidosis.",
       "Blood is compared with its own normal range, not with 7.00; 7.33 is too acidic for blood.",
       "Alkalosis is above 7.45.",
       "7.33 is below the lower limit, 7.35."],
      "Compare with 7.35&ndash;7.45.",
      "7.33 &lt; 7.35: <b>acidosis</b>.", 2)

    o = V('3.0', -5)
    Q(T, "A solution has [{OH^-}] = " + sci('3.0', -5) + " M. Which pOH is reported correctly?",
      [p(o, 2), p(o, 1), p(o, 3), p(o, 4)],
      ["3.0 has 2 significant figures (the trailing zero counts), so the pOH has 2 decimal places.",
       "This drops the significant trailing zero of 3.0 and keeps only one decimal place.",
       "This keeps 3 decimal places; the concentration has only 2 significant figures.",
       "This is the unrounded calculator value."],
      "Decimal places in pOH = significant figures in [{OH^-}].",
      "&minus;log(3.0 &times; 10<sup>&minus;5</sup>) = <b>%s</b>." % p(o, 2), 2, 1)

    # ======================= ch12-buffers (6) =======================
    T = 'ch12-buffers'
    Q(T, "Which pair of compounds, dissolved together in water, makes a buffer?",
      ["{NH3} and {NH4NO3}", "KOH and KCl", "HBr and NaBr", "{NH3} and NaCl"],
      ["{NH3} is a weak base, and {NH4NO3} supplies {NH4^+}, its conjugate acid.",
       "KOH is a strong base, and Cl<sup>&minus;</sup> is not its partner.",
       "HBr is a strong acid; Br<sup>&minus;</sup> cannot take back a proton.",
       "{NH3} is weak, but NaCl does not supply its conjugate acid, {NH4^+}."],
      "A weak base plus a salt of its conjugate acid also makes a buffer.",
      "{NH3}/{NH4^+}: <b>{NH3} and {NH4NO3}</b>.", 2)

    Q(T, "A student mixes hydrofluoric acid, HF, with potassium chloride, KCl. HF is a weak acid. Why is the mixture still <b>not</b> a buffer?",
      ["Cl<sup>&minus;</sup> is not the conjugate base of HF, so no partner can neutralize added acid.",
       "HF is a strong acid, so it cannot be in a buffer.",
       "KCl is a strong base that neutralizes all the HF.",
       "It is a buffer, because any weak acid with any salt makes one."],
      ["HF's conjugate base is F<sup>&minus;</sup> (from a salt such as KF); Cl<sup>&minus;</sup> is a spectator that cannot take up added H<sup>+</sup>.",
       "HF is weak; the problem is the salt, not the acid.",
       "KCl is a neutral salt, not a base.",
       "The salt must supply the weak acid's own conjugate base."],
      "Does KCl supply HF's own conjugate base?",
      "<b>Cl<sup>&minus;</sup> is not F<sup>&minus;</sup></b>: the base partner is missing.", 2)

    Q(T, "A phosphate buffer contains {H2PO4^-} and {HPO4^2-}. Which species reacts with a small amount of added {OH^-}?",
      ["{H2PO4^-}", "{HPO4^2-}", "Na<sup>+</sup>", "{PO4^3-}"],
      ["The acid partner gives up a proton: [[H2PO4^-(aq) + OH^-(aq) -> HPO4^2-(aq) + H2O(l)]].",
       "{HPO4^2-} is the base partner; it handles added acid.",
       "Na<sup>+</sup> is a spectator ion.",
       "{PO4^3-} is not one of the buffer partners here."],
      "Added base is neutralized by the acid partner (the one with more H).",
      "[[H2PO4^-(aq) + OH^-(aq) -> HPO4^2-(aq) + H2O(l)]]: <b>{H2PO4^-}</b>.", 2)

    Q(T, "A buffer contains lactic acid, {HC3H5O3}, and sodium lactate. Which equation shows it neutralizing added {H3O^+}?",
      ["[[C3H5O3^-(aq) + H3O^+(aq) -> HC3H5O3(aq) + H2O(l)]]", "[[HC3H5O3(aq) + OH^-(aq) -> C3H5O3^-(aq) + H2O(l)]]",
       "[[HC3H5O3(aq) + H3O^+(aq) -> H2C3H5O3^+(aq) + H2O(l)]]", "[[H3O^+(aq) + OH^-(aq) -> 2 H2O(l)]]"],
      ["The base partner (lactate) takes the proton and becomes lactic acid.",
       "This is how the buffer handles added <i>base</i>.",
       "This adds H<sup>+</sup> to the acid; the acid partner does not react with added acid.",
       "A buffer contains very little {OH^-}; the lactate is what absorbs {H3O^+}."],
      "Added acid reacts with the base partner.",
      "<b>[[C3H5O3^-(aq) + H3O^+(aq) -> HC3H5O3(aq) + H2O(l)]]</b>.", 3)

    Q(T, "A patient with severe chronic lung disease cannot breathe out enough {CO2}, so {CO2} builds up in the blood. What happens?",
      ["[{H3O^+}] rises and the blood pH falls (respiratory acidosis).", "[{H3O^+}] falls and the pH rises (respiratory alkalosis).",
       "The pH stays exactly the same, because blood is buffered.", "The extra {CO2} becomes {OH^-}, so the pH rises."],
      ["More {CO2} &rarr; more {H2CO3} &rarr; more H<sup>+</sup>, so the pH falls below normal.",
       "This is what happens when {CO2} is blown off, not when it builds up.",
       "The buffer limits the change, but {CO2} buildup adds acid, so the pH still falls.",
       "{CO2} forms carbonic acid, which releases H<sup>+</sup>, not {OH^-}."],
      "More {CO2} means more of which acid?",
      "{CO2} up &rarr; H<sup>+</sup> up: <b>pH falls (respiratory acidosis)</b>.", 2)

    Q(T, "After a sugary snack, plaque bacteria release lactic acid onto the teeth. Which part of saliva neutralizes the acid?",
      ["Bicarbonate, {HCO3^-}, a base", "Carbonic acid, {H2CO3}", "Na<sup>+</sup> ions", "Water alone"],
      ["Saliva carries bicarbonate (and phosphate), which accept H<sup>+</sup> and raise the plaque pH again.",
       "Carbonic acid is the acid partner; it reacts with added base, not acid.",
       "Na<sup>+</sup> is a spectator ion.",
       "Water alone cannot absorb acid without a big pH drop."],
      "Added acid is neutralized by a base partner.",
      "<b>Bicarbonate</b> accepts the H<sup>+</sup>.", 1)


if __name__ == '__main__':
    build_hw()
    dump(sys.argv[1])
