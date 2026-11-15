#!/usr/bin/env python3
"""Builds bank/ch12.json (Chapter 12 Try It items: properties of acids and bases, Bronsted-Lowry and conjugate
pairs, strong and weak acids and bases, water and Kw, pH and pOH, buffers).
Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch12.py bank/ch12.json
Conventions (Chapter 12 text): strong acids HCl, HBr, HI, HNO3, HClO4, H2SO4 (H2SO4 kept out of pH math); strong
bases = Group 1 hydroxides and Ca(OH)2, Sr(OH)2, Ba(OH)2 (2 OH- each); every other acid or base is weak (double
arrow). H3O+ notation; Kw = [H3O+][OH-] = 1.0 x 10^-14 at 25 C (2 significant figures); pH = -log[H3O+],
pOH = -log[OH-], pH + pOH = 14.00; log rule: decimal places in pH (pOH) = significant figures in the concentration,
and back again; round half up. Indicators (12.1): litmus blue -> red in acid, red -> blue in base; phenolphthalein
colorless in acid and neutral, pink in base; red cabbage pH 1-2 red, 3-4 pink, 5-7 purple, 8 blue, 9-11 green,
12-14 yellow. Blood 7.35-7.45. Buffers qualitative only (no Henderson-Hasselbalch).
Markup: {HPO4^2-} formula or ion, [[HF(aq) + OH^-(aq) -> F^-(aq) + H2O(l)]] equation (<=> = double arrow).
The helpers are imported by tools/gen_adapt_ch12.py. Every number is recomputed independently by
tools/check_bank_ch12.py."""
import json, sys, re, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
M = '&minus;'
B = []
CFG = {'prefix': 'c12-%03d', 'adapt': False}

# ---------------- formulas, ions and equations ----------------
def F(s):
    base, _, ch = s.partition('^')
    h = re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', base)
    return h + ('<sup>' + ch.replace('-', M) + '</sup>' if ch else '')
SPH = re.compile(r'^(.*?)(\((?:s|l|g|aq)\))?$')
def EQ(s):
    out = []
    for tok in s.split():
        if tok == '->': out.append('&rarr;')
        elif tok == '<=>': out.append('&rlarr;')
        elif tok == '+' or re.fullmatch(r'\d+', tok): out.append(tok)
        else:
            m = SPH.match(tok); out.append(F(m.group(1)) + (m.group(2) or ''))
    return ' '.join(out)
def X(s):
    s = re.sub(r'\[\[(.+?)\]\]', lambda m: EQ(m.group(1)), s)
    s = re.sub(r'(?<![\w;])-(?=\d)', M, s)
    return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)

# ---------------- numbers ----------------
def num(x, n=3):
    x = D(x); e = x.adjusted()
    m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if abs(m) >= 10:
        e += 1; m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if -3 <= e <= n - 1:
        s = format(m.scaleb(e).quantize(D(1).scaleb(min(0, e - n + 1))), 'f')
        if e == n - 1 and s.endswith('0'): s += '.'
    else:
        s = '%s &times; 10<sup>%s</sup>' % (m, (M + str(-e)) if e < 0 else str(e))
    return s
def qd(x, d): return format(D(x).quantize(D(1).scaleb(-d), rounding=ROUND_HALF_UP), 'f')
def S(v, n, u='M'): return num(v, n) + ' ' + u
def sci(m, e):
    """a given as written: sci('6.2', -4) -> 6.2 x 10^-4"""
    return '%s &times; 10<sup>%s</sup>' % (m, (M + str(-e)) if e < 0 else str(e))
def V(m, e): return D(m) * D(10) ** e
KW = D('1.0e-14')
def p(x, d):
    """-log10(x) to d decimal places (log rule)."""
    return qd(-D(x).log10(), d)
def ten(pv): return D(10) ** (-D(pv))
def sub14(pv):
    """14.00 - a p value with 2 decimal places."""
    return qd(D('14.00') - D(pv), 2)

def Q(t_, q, c, y, h, w, d, k=0, f=None):
    y = list(y)
    if CFG['adapt'] and not y[0].startswith('Correct: '): y[0] = 'Correct: ' + y[0]
    it = {"id": CFG['prefix'] % (len(B) + 1), "t": t_, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    if f:
        for fg in f:
            if fg['type'] == 'table':
                fg['head'] = [X(x) for x in fg['head']]; fg['rows'] = [[X(x) for x in r] for r in fg['rows']]
                if fg.get('cap'): fg['cap'] = X(fg['cap'])
        it["f"] = f
    B.append(it)

def dump(out):
    json.dump(B, open(out, 'w'), ensure_ascii=False, indent=1)
    print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')),
          'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))

CABBAGE = [["1&ndash;2", "red"], ["3&ndash;4", "pink"], ["5&ndash;7", "purple"], ["8", "blue"], ["9&ndash;11", "green"], ["12&ndash;14", "yellow"]]


def build():
    # ======================= ch12-props (10) =======================
    T = 'ch12-props'
    Q(T, "A drop of an unknown solution turns blue litmus paper red. What does this tell you?",
      ["The solution is acidic.", "The solution is basic.", "The solution is neutral.", "The solution is a strong acid with a pH below 2."],
      ["Acids turn blue litmus red (&ldquo;BRA&rdquo;: blue turns red in acid).",
       "Bases do the opposite: they turn <i>red</i> litmus blue.",
       "A neutral solution leaves both colors of litmus unchanged.",
       "Litmus only tells acid or base; it cannot tell how strong the acid is or give a pH."],
      "Remember &ldquo;BRA&rdquo;: Blue turns Red in Acid.",
      "Blue litmus turned red, so the solution is <b>acidic</b>. (Litmus does not tell how acidic.)", 1)

    Q(T, "A few drops of phenolphthalein are added to a clear solution, and it stays colorless. What can you conclude?",
      ["The solution is acidic or neutral.", "The solution is basic.", "The solution must be acidic.", "The solution must be pure water."],
      ["Phenolphthalein is colorless in acidic <i>and</i> neutral solutions; only a base turns it pink.",
       "A basic solution would turn phenolphthalein pink.",
       "Neutral water also leaves phenolphthalein colorless, so acid is possible but not certain.",
       "Any acidic solution would also leave it colorless; this test cannot single out pure water."],
      "Phenolphthalein: &ldquo;pink means base.&rdquo; What does colorless rule out?",
      "Colorless rules out only a base: the solution is <b>acidic or neutral</b>.", 2)

    Q(T, "Use the table of red cabbage indicator colors. A sample of seltzer (carbonated water) turns the indicator pink. What are its approximate pH and type?",
      ["pH 3&ndash;4, acidic", "pH 1&ndash;2, strongly acidic", "pH 8, slightly basic", "pH 9&ndash;11, basic"],
      ["Pink is the color for pH 3&ndash;4; dissolved carbon dioxide makes seltzer acidic.",
       "pH 1&ndash;2 gives red, not pink.",
       "pH 8 gives blue.",
       "pH 9&ndash;11 gives green."],
      "Find &ldquo;pink&rdquo; in the color column and read across.",
      "Pink = <b>pH 3&ndash;4, acidic</b>.", 1, 0,
      [{"type": "table", "cap": "Red cabbage indicator colors (approximate)", "head": ["pH", "Color"], "rows": CABBAGE}])

    Q(T, "A student tests a sample of an unknown cleaner. Which single result proves that the cleaner is basic?",
      ["Red litmus paper turns blue.", "Blue litmus paper turns red.", "Phenolphthalein stays colorless.", "A magnesium ribbon fizzes and gives off hydrogen gas."],
      ["Bases turn red litmus blue (and phenolphthalein pink).",
       "Blue litmus turning red is the test for an acid.",
       "Colorless phenolphthalein means acidic or neutral; a base would turn it pink.",
       "Reacting with an active metal to make hydrogen gas is a property of acids."],
      "Bases change red litmus to which color?",
      "<b>Red litmus turns blue</b> in a base.", 1)

    Q(T, "Iron filings are dropped into hydrochloric acid, and bubbles form as the iron dissolves. Iron forms Fe<sup>2+</sup> ions. What are the products?",
      ["{FeCl2}(aq) and {H2}(g)", "{FeCl2}(aq) and {H2O}(l)", "{FeCl2}(aq), {H2O}(l), and {CO2}(g)", "{Fe(OH)2}(s) and {Cl2}(g)"],
      ["Acid + active metal &rarr; salt + hydrogen gas: [[Fe(s) + 2 HCl(aq) -> FeCl2(aq) + H2(g)]].",
       "Water forms when an acid reacts with a base; there is no oxygen in the reactants here.",
       "Carbon dioxide forms only when an acid reacts with a carbonate or bicarbonate.",
       "An acid does not make a hydroxide or chlorine gas with a metal; the H<sup>+</sup> becomes {H2} gas."],
      "Acid + active metal gives a salt and which gas?",
      "[[Fe(s) + 2 HCl(aq) -> FeCl2(aq) + H2(g)]]: the bubbles are <b>hydrogen gas</b>, and the salt is {FeCl2}.", 2)

    Q(T, "In buttermilk pancakes, baking soda ({NaHCO3}) reacts with the lactic acid ({HC3H5O3}) in the buttermilk, and the batter puffs up. Which set of products is correct?",
      ["{NaC3H5O3}(aq), {H2O}(l), and {CO2}(g)", "{NaC3H5O3}(aq) and {H2CO3}(aq)", "{NaC3H5O3}(aq) and {H2}(g)", "NaOH(aq) and {CO2}(g)"],
      ["Acid + bicarbonate &rarr; salt + water + carbon dioxide: [[NaHCO3(s) + HC3H5O3(aq) -> NaC3H5O3(aq) + H2O(l) + CO2(g)]]. The {CO2} bubbles puff up the batter.",
       "{H2CO3} forms first, but it breaks down into {H2O} and {CO2}; write those instead.",
       "Hydrogen gas comes from an acid reacting with an active metal, not with a bicarbonate.",
       "An acid does not make a hydroxide; the bicarbonate takes the acid's H<sup>+</sup> and gives off {CO2}."],
      "Acid + carbonate or bicarbonate gives a salt, water, and a gas.",
      "[[NaHCO3(s) + HC3H5O3(aq) -> NaC3H5O3(aq) + H2O(l) + CO2(g)]]: <b>sodium lactate, {H2O}, and {CO2}</b> (the gas that puffs the batter).", 2)

    Q(T, "Hydrobromic acid is neutralized by lithium hydroxide. What is the net ionic equation?",
      ["[[H^+(aq) + OH^-(aq) -> H2O(l)]]", "[[HBr(aq) + LiOH(aq) -> LiBr(aq) + H2O(l)]]", "[[Li^+(aq) + Br^-(aq) -> LiBr(aq)]]", "[[H^+(aq) + Br^-(aq) -> HBr(aq)]]"],
      ["HBr and LiOH are a strong acid and a strong base, so they are all ions; Li<sup>+</sup> and Br<sup>&minus;</sup> are spectators.",
       "This is the molecular equation. The net ionic equation leaves out the spectator ions.",
       "Li<sup>+</sup> and Br<sup>&minus;</sup> are spectator ions; they stay dissolved and do not react.",
       "HBr is a strong acid and stays fully ionized; the H<sup>+</sup> reacts with OH<sup>&minus;</sup> instead."],
      "Strong acid + strong base: cross out the spectator ions.",
      "Spectators Li<sup>+</sup> and Br<sup>&minus;</sup> drop out: <b>[[H^+(aq) + OH^-(aq) -> H2O(l)]]</b>.", 2)

    Q(T, "Pure water barely conducts electricity, but hydrochloric acid conducts well. Why?",
      ["HCl forms ions ({H3O^+} and {Cl^-}) that carry charge through the solution.", "HCl molecules are polar, and polar molecules carry current.",
       "HCl contains hydrogen, which conducts like a metal.", "HCl releases free electrons into the water."],
      ["Acids are electrolytes: HCl ionizes completely, and the moving ions carry the current.",
       "Polar molecules without charge, such as water itself, carry almost no current; ions are needed.",
       "Hydrogen is a nonmetal; conduction in a solution comes from dissolved ions.",
       "Solutions conduct by moving ions, not by free electrons."],
      "What has to be present for a solution to conduct?",
      "HCl ionizes into <b>{H3O^+} and {Cl^-} ions</b>, which carry charge.", 1)

    Q(T, "Acid rain slowly dissolves marble statues, which are made of calcium carbonate, {CaCO3}. Which gas is released as the marble reacts with the acid?",
      ["Carbon dioxide, {CO2}", "Hydrogen, {H2}", "Oxygen, {O2}", "Sulfur dioxide, {SO2}"],
      ["Acid + carbonate &rarr; salt + water + carbon dioxide.",
       "Hydrogen gas comes from an acid reacting with an active metal, not a carbonate.",
       "No oxygen gas forms; the oxygen ends up in {H2O} and {CO2}.",
       "{SO2} is a pollutant that helps <i>make</i> acid rain; it is not released by the marble."],
      "Which reaction type is acid + carbonate?",
      "Acid + carbonate gives a salt, water, and <b>carbon dioxide</b>.", 1)

    Q(T, "Milk of magnesia, {Mg(OH)2}, neutralizes stomach acid (HCl). In the balanced equation, how many water molecules form for each {Mg(OH)2}?",
      ["2", "1", "4", "0"],
      ["[[Mg(OH)2(s) + 2 HCl(aq) -> MgCl2(aq) + 2 H2O(l)]]: each OH<sup>&minus;</sup> meets one H<sup>+</sup> and makes one water.",
       "One water would use only one of the two OH<sup>&minus;</sup> ions in {Mg(OH)2}.",
       "This counts H atoms instead of water molecules.",
       "A neutralization always makes water: H<sup>+</sup> + OH<sup>&minus;</sup> &rarr; {H2O}."],
      "The number of waters equals the number of H<sup>+</sup> (or OH<sup>&minus;</sup>) that react.",
      "[[Mg(OH)2(s) + 2 HCl(aq) -> MgCl2(aq) + 2 H2O(l)]]: <b>2</b> waters.", 2)

    # ======================= ch12-bl (12) =======================
    T = 'ch12-bl'
    Q(T, "According to the Arrhenius definition, a base is a substance that",
      ["produces OH<sup>&minus;</sup> ions when it dissolves in water.", "donates H<sup>+</sup> ions in water.",
       "produces H<sup>+</sup> ions when it dissolves in water.", "contains hydrogen atoms that it can release."],
      ["Arrhenius bases make hydroxide ions in water, such as NaOH &rarr; Na<sup>+</sup> + OH<sup>&minus;</sup>.",
       "Donating H<sup>+</sup> describes an acid, not a base.",
       "Producing H<sup>+</sup> in water is the Arrhenius definition of an acid.",
       "Having hydrogen does not make something a base (or an acid); {NH3} has H atoms and is a base."],
      "Arrhenius: acids make H<sup>+</sup>; bases make ___.",
      "An Arrhenius base <b>produces OH<sup>&minus;</sup> in water</b>.", 1)

    Q(T, "A Br&oslash;nsted&ndash;Lowry acid is best described as a",
      ["proton (H<sup>+</sup>) donor", "proton (H<sup>+</sup>) acceptor", "substance that produces OH<sup>&minus;</sup> in water", "substance that tastes bitter"],
      ["Acids donate H<sup>+</sup> (&ldquo;BAD&rdquo;: bases accept, acids donate).",
       "Accepting a proton is what a Br&oslash;nsted&ndash;Lowry base does.",
       "Producing OH<sup>&minus;</sup> is the Arrhenius definition of a base.",
       "A bitter taste is an old observed property of bases, not a definition of an acid."],
      "&ldquo;BAD&rdquo;: Bases Accept, Acids Donate.",
      "A Br&oslash;nsted&ndash;Lowry acid is a <b>proton donor</b>.", 1)

    Q(T, "Ammonia, {NH3}, neutralizes acids, yet it contains no hydroxide ion. Which definition explains why {NH3} is a base?",
      ["Br&oslash;nsted&ndash;Lowry: {NH3} accepts a proton and becomes {NH4^+}.", "Arrhenius: {NH3} releases OH<sup>&minus;</sup> from its formula.",
       "Br&oslash;nsted&ndash;Lowry: {NH3} donates one of its three H atoms.", "Arrhenius: {NH3} releases H<sup>+</sup> in water."],
      ["The lone pair on nitrogen accepts H<sup>+</sup>: [[NH3(aq) + H2O(l) <=> NH4^+(aq) + OH^-(aq)]].",
       "{NH3} has no OH in its formula; the OH<sup>&minus;</sup> comes from the water that lost a proton.",
       "Donating H<sup>+</sup> would make {NH3} an acid. Ammonia gains an H instead.",
       "Releasing H<sup>+</sup> describes an Arrhenius acid."],
      "Does ammonia gain or lose an H when it reacts with water?",
      "{NH3} gains H<sup>+</sup> to form {NH4^+}: a <b>Br&oslash;nsted&ndash;Lowry base (proton acceptor)</b>.", 2)

    Q(T, "What is the hydronium ion, and how does it form?",
      ["{H3O^+}; an H<sup>+</sup> ion attaches to a lone pair on a water molecule.", "{OH^-}; a water molecule loses an H<sup>+</sup>.",
       "{H2O^+}; a water molecule loses an electron.", "{H3O^-}; a water molecule gains a hydride ion."],
      ["A bare proton is too reactive to float alone: H<sup>+</sup> + {H2O} &rarr; {H3O^+}.",
       "Water losing H<sup>+</sup> gives the hydroxide ion, not hydronium.",
       "Hydronium has three H atoms; it forms by gaining a proton, not by losing an electron.",
       "Hydronium is positive: it is water plus one H<sup>+</sup>."],
      "Hydronium = water + one proton.",
      "<b>{H3O^+}</b>, formed when H<sup>+</sup> bonds to a water molecule.", 1)

    Q(T, "In the reaction below, which reactant is the Br&oslash;nsted&ndash;Lowry <b>base</b>?<br>[[HC2H3O2(aq) + NH3(aq) <=> NH4^+(aq) + C2H3O2^-(aq)]]",
      ["{NH3}", "{HC2H3O2}", "{NH4^+}", "{C2H3O2^-}"],
      ["{NH3} gains an H<sup>+</sup> and becomes {NH4^+}, so it is the proton acceptor.",
       "Acetic acid loses an H<sup>+</sup> (it becomes acetate), so it is the acid.",
       "{NH4^+} is a product: it is the conjugate acid of {NH3}.",
       "Acetate is a product: it is the conjugate base of acetic acid."],
      "The base is the reactant that gains an H from left to right.",
      "{NH3} becomes {NH4^+}: <b>{NH3}</b> accepts the proton.", 2)

    Q(T, "In the reaction below, what is the conjugate base of {HCO3^-}?<br>[[HCO3^-(aq) + OH^-(aq) <=> CO3^2-(aq) + H2O(l)]]",
      ["{CO3^2-}", "{H2O}", "{H2CO3}", "{OH^-}"],
      ["{HCO3^-} loses one H<sup>+</sup>, and its charge drops by 1: {CO3^2-}.",
       "Water is the conjugate acid of {OH^-}, the base in this reaction.",
       "{H2CO3} has one <i>more</i> H<sup>+</sup>: it is the conjugate acid of {HCO3^-}.",
       "{OH^-} is the base that accepts the proton, not the partner of {HCO3^-}."],
      "Conjugate base = the acid minus one H<sup>+</sup> (charge goes down by 1).",
      "{HCO3^-} &minus; H<sup>+</sup> = <b>{CO3^2-}</b>.", 2)

    Q(T, "Dihydrogen phosphate reacts with water as shown. Which choice lists one of its two conjugate acid&ndash;base pairs?<br>[[H2PO4^-(aq) + H2O(l) <=> HPO4^2-(aq) + H3O^+(aq)]]",
      ["{H2PO4^-} and {HPO4^2-}", "{H2PO4^-} and {H2O}", "{H2O} and {HPO4^2-}", "{H3O^+} and {HPO4^2-}"],
      ["They differ by exactly one H<sup>+</sup> (one H and one unit of charge).",
       "These are the two reactants (the acid and the base); a pair is a reactant with its product partner.",
       "{H2O} pairs with {H3O^+}, not with {HPO4^2-}; they differ by more than one H<sup>+</sup>.",
       "These are the two products; each pairs with a reactant."],
      "Pair each reactant with the product that differs from it by one H<sup>+</sup>.",
      "{H2PO4^-} loses H<sup>+</sup> to become {HPO4^2-}: <b>{H2PO4^-}/{HPO4^2-}</b> (the other pair is {H2O}/{H3O^+}).", 2)

    Q(T, "What is the conjugate base of phosphoric acid, {H3PO4}?",
      ["{H2PO4^-}", "{H2PO4}", "{H4PO4^+}", "{PO4^3-}"],
      ["Remove one H<sup>+</sup>: one fewer H, and the charge drops from 0 to 1&minus;.",
       "This removes the H but forgets the charge; removing H<sup>+</sup> leaves a 1&minus; charge.",
       "This <i>adds</i> H<sup>+</sup>, which makes a conjugate acid, not a conjugate base.",
       "This removes all three protons; a conjugate base differs by only one H<sup>+</sup>."],
      "Conjugate base: one fewer H, charge one lower.",
      "{H3PO4} &minus; H<sup>+</sup> = <b>{H2PO4^-}</b>.", 2)

    Q(T, "What is the conjugate acid of the hydrogen sulfide ion, {HS^-}?",
      ["{H2S}", "{S^2-}", "{H2S^-}", "{H3S^+}"],
      ["Add one H<sup>+</sup>: one more H, and the charge rises from 1&minus; to 0.",
       "Removing H<sup>+</sup> gives the conjugate <i>base</i>, {S^2-}.",
       "This adds the H but forgets the charge; adding H<sup>+</sup> raises the charge by 1.",
       "This adds two H<sup>+</sup>; a conjugate pair differs by one."],
      "Conjugate acid: one more H, charge one higher.",
      "{HS^-} + H<sup>+</sup> = <b>{H2S}</b>.", 2)

    Q(T, "What is the conjugate acid of the carbonate ion, {CO3^2-}?",
      ["{HCO3^-}", "{H2CO3}", "{HCO3^2-}", "{CO3^-}"],
      ["Add one H<sup>+</sup>: one more H, and the charge goes from 2&minus; to 1&minus;.",
       "This adds two H<sup>+</sup>; {H2CO3} would be the conjugate acid of bicarbonate, one step further.",
       "This adds the H but leaves the charge at 2&minus;; adding H<sup>+</sup> raises the charge by 1.",
       "This changes the charge without adding the H atom."],
      "Add one H and raise the charge by one.",
      "{CO3^2-} + H<sup>+</sup> = <b>{HCO3^-}</b>.", 2)

    Q(T, "In which reaction does water act as a Br&oslash;nsted&ndash;Lowry <b>acid</b>?",
      ["[[CN^-(aq) + H2O(l) <=> HCN(aq) + OH^-(aq)]]", "[[HI(aq) + H2O(l) -> H3O^+(aq) + I^-(aq)]]",
       "[[HClO4(aq) + H2O(l) -> H3O^+(aq) + ClO4^-(aq)]]", "[[HNO2(aq) + H2O(l) <=> H3O^+(aq) + NO2^-(aq)]]"],
      ["Water gives an H<sup>+</sup> to {CN^-} and becomes {OH^-}: here water is the proton donor.",
       "Here water gains H<sup>+</sup> and becomes {H3O^+}, so it is the base.",
       "Water accepts the proton from {HClO4} (it becomes {H3O^+}), so it is the base.",
       "Water accepts the proton from {HNO2} and becomes {H3O^+}, so it is the base."],
      "Water is the acid when it turns into {OH^-}.",
      "Only in the cyanide reaction does water lose H<sup>+</sup> (to become {OH^-}): <b>[[CN^-(aq) + H2O(l) <=> HCN(aq) + OH^-(aq)]]</b>.", 2)

    Q(T, "Which species is <b>amphoteric</b>, able to act as either an acid or a base?",
      ["{HCO3^-}", "{CO3^2-}", "{Cl^-}", "{Na^+}"],
      ["Bicarbonate can lose H<sup>+</sup> (to {CO3^2-}) or gain H<sup>+</sup> (to {H2CO3}).",
       "Carbonate has no H to donate, so it can act only as a base.",
       "Chloride has no H to donate and is too weak a base to take one; it is a spectator ion.",
       "Na<sup>+</sup> neither donates nor accepts protons; it is a spectator ion."],
      "An amphoteric species needs an H to give and room to take one.",
      "<b>{HCO3^-}</b> can donate or accept a proton.", 2)

    # ======================= ch12-strength (12) =======================
    T = 'ch12-strength'
    Q(T, "Which acid is a <b>strong</b> acid?",
      ["HI", "{HNO2}", "{HC3H5O3}", "{H2CO3}"],
      ["Hydroiodic acid is one of the six strong acids on the green sheet: it ionizes completely.",
       "Nitrous acid ({HNO2}) is not nitric acid ({HNO3}); it is not on the strong list, so it is weak.",
       "Lactic acid is not on the strong list, so it is weak.",
       "Carbonic acid is weak; it is the acid partner of the blood buffer."],
      "Strong acids: HCl, HBr, HI, {HNO3}, {HClO4}, {H2SO4}.",
      "<b>HI</b> is on the strong-acid list; the others are weak.", 1)

    Q(T, "Which acid is a <b>weak</b> acid?",
      ["HF", "HCl", "HBr", "{HNO3}"],
      ["HF is not on the strong-acid list, so it ionizes only slightly.",
       "HCl is a strong acid (green sheet).",
       "HBr is a strong acid (green sheet).",
       "{HNO3} is a strong acid (green sheet)."],
      "Any acid not on the list of six strong acids is weak.",
      "<b>HF</b> is weak; HCl, HBr, and {HNO3} are strong.", 1)

    Q(T, "Which compound is a <b>strong</b> base?",
      ["{Ca(OH)2}", "{NH3}", "{Mg(OH)2}", "{CH3OH}"],
      ["Calcium hydroxide is on the strong-base list (Group 1 hydroxides plus Ca, Sr, and Ba hydroxides).",
       "Ammonia accepts protons only to a small extent: a weak base.",
       "Magnesium hydroxide is not on the strong-base list; it is poorly soluble and treated as weak.",
       "Methanol is an alcohol: its OH is covalently bonded, not a hydroxide ion, so it is not a base."],
      "Strong bases: Group 1 hydroxides plus {Ca(OH)2}, {Sr(OH)2}, {Ba(OH)2}.",
      "<b>{Ca(OH)2}</b> is on the strong-base list.", 1)

    Q(T, "Nitrous acid, {HNO2}, is a weak acid. Which equation correctly shows it ionizing in water?",
      ["[[HNO2(aq) + H2O(l) <=> H3O^+(aq) + NO2^-(aq)]]", "[[HNO2(aq) + H2O(l) -> H3O^+(aq) + NO2^-(aq)]]",
       "[[HNO2(aq) + H2O(l) <=> H2NO2^+(aq) + OH^-(aq)]]", "[[HNO2(aq) -> H^+(aq) + NO2^-(aq)]]"],
      ["A weak acid ionizes only slightly, so it gets a double arrow, and it donates its H<sup>+</sup> to water.",
       "A single arrow means complete ionization, which is only for strong acids.",
       "This has the acid accepting a proton from water; an acid donates its proton.",
       "This shows a single arrow (complete ionization) and leaves out the water that takes the proton; a weak acid needs a double arrow."],
      "Weak acid: double arrow, and the acid gives its H<sup>+</sup> to water.",
      "<b>[[HNO2(aq) + H2O(l) <=> H3O^+(aq) + NO2^-(aq)]]</b> (double arrow for a weak acid).", 2)

    Q(T, "Acetic acid, {HC2H3O2}, is dissolved in water. Which description fits the solution (water molecules not counted)?",
      ["Mostly intact {HC2H3O2} molecules, with a few {H3O^+} and {C2H3O2^-} ions",
       "Only {H3O^+} and {C2H3O2^-} ions, with no intact molecules",
       "Only intact {HC2H3O2} molecules, with no ions at all",
       "Mostly {H3O^+} ions and intact molecules, but no acetate ions"],
      ["Acetic acid is weak: only a small fraction of its molecules donate a proton at any moment.",
       "All ions and no molecules describes a strong acid; acetic acid is weak.",
       "A weak acid does ionize a little, which is why vinegar conducts weakly.",
       "Each molecule that ionizes makes one {H3O^+} <i>and</i> one acetate ion."],
      "Weak acids ionize only slightly.",
      "Weak acid: <b>mostly intact molecules, a few ions</b>.", 2)

    Q(T, "Solution A is 0.0020 M {HNO3}; solution B is 3.0 M {HC2H3O2}. Which statement is true?",
      ["A is a dilute solution of a strong acid; B is a concentrated solution of a weak acid.",
       "A is a weak acid because it is dilute; B is a strong acid because it is concentrated.",
       "Both are strong acids, because both ionize completely.",
       "Both are weak acids, because both contain intact acid molecules."],
      ["Strength is about the fraction that ionizes (a property of the acid); concentration is how much is dissolved.",
       "This mixes up strength with concentration. Dilute {HNO3} is still fully ionized.",
       "Acetic acid is weak at any concentration; most of its molecules stay intact.",
       "{HNO3} is strong: even dilute, it has essentially no intact molecules."],
      "Strong or weak depends on which acid it is, not on how much is dissolved.",
      "{HNO3} is strong (but dilute here); acetic acid is weak (but concentrated here): <b>A dilute strong acid, B concentrated weak acid</b>.", 2)

    Q(T, "Which compound is a <b>salt</b>?",
      ["{CaBr2}", "HBr", "{Ca(OH)2}", "{C2H5OH}"],
      ["A salt is ionic, with a cation from a base (Ca<sup>2+</sup>) and an anion from an acid (Br<sup>&minus;</sup>).",
       "HBr has its acidic H written first: it is an acid.",
       "{Ca(OH)2} contains hydroxide ions: it is a base.",
       "Ethanol is molecular; it is neither an acid nor a base, and not a salt."],
      "Salt = a base's cation + an acid's anion.",
      "<b>{CaBr2}</b> (Ca<sup>2+</sup> from {Ca(OH)2}, Br<sup>&minus;</sup> from HBr) is a salt.", 1)

    Q(T, "Isopropyl alcohol (rubbing alcohol), {C3H7OH}, contains an OH group. How is it classified?",
      ["Neither an acid nor a base", "A strong base", "A weak base", "A weak acid"],
      ["Its OH is covalently bonded to carbon; it is not a hydroxide ion, and it has no acidic H written first.",
       "Strong bases are ionic metal hydroxides that release OH<sup>&minus;</sup>; an alcohol does not.",
       "Weak bases are ammonia, amines, carbonates, and bicarbonates; an alcohol is none of these.",
       "Alcohols do not have an acidic H written first or a &ndash;COOH group."],
      "Is the OH a hydroxide ion or a covalent group?",
      "An alcohol's OH is not OH<sup>&minus;</sup>: <b>neither an acid nor a base</b>.", 2)

    Q(T, "Which compound is a <b>base</b>?",
      ["{NaHCO3} (baking soda)", "NaCl (table salt)", "{HC2H3O2} (acetic acid)", "{C6H12O6} (glucose)"],
      ["Bicarbonate accepts protons, so baking soda is a base (and also a salt).",
       "NaCl is a salt; neither of its ions accepts or donates protons.",
       "Acetic acid has an acidic H (in its &ndash;COOH group): it is an acid.",
       "Glucose is molecular; its OH groups are not hydroxide ions, so it is neither."],
      "Bases include hydroxides, carbonates and bicarbonates, and ammonia and amines.",
      "<b>{NaHCO3}</b>: bicarbonate is a proton acceptor.", 1)

    Q(T, "Hydroiodic acid neutralizes barium hydroxide. What salt forms?",
      ["{BaI2}", "BaI", "{Ba2I}", "{BaH2}"],
      ["Ba<sup>2+</sup> and I<sup>&minus;</sup> balance as {BaI2}: [[2 HI(aq) + Ba(OH)2(aq) -> BaI2(aq) + 2 H2O(l)]].",
       "BaI leaves the charges unbalanced: Ba<sup>2+</sup> needs two I<sup>&minus;</sup>.",
       "This swaps the subscripts the wrong way; Ba<sup>2+</sup> needs two iodide ions, not two barium ions.",
       "The salt is the base's cation with the acid's anion; the H<sup>+</sup> ends up in water."],
      "Salt = base's cation + acid's anion, with balanced charges.",
      "[[2 HI(aq) + Ba(OH)2(aq) -> BaI2(aq) + 2 H2O(l)]]: <b>{BaI2}</b>.", 2)

    Q(T, "Potassium hydroxide neutralizes hydroiodic acid. What are the products?",
      ["KI(aq) and {H2O}(l)", "KI(aq) and {H2}(g)", "{K2O}(s) and {I2}(s)", "No products; KOH and HI do not react."],
      ["Acid + base &rarr; salt + water: [[HI(aq) + KOH(aq) -> KI(aq) + H2O(l)]].",
       "Hydrogen gas comes from acids reacting with active metals, not with bases.",
       "Neutralization makes a salt and water; it does not make an oxide or a different acid.",
       "A strong acid and a strong base react completely: H<sup>+</sup> + OH<sup>&minus;</sup> &rarr; {H2O}."],
      "Acid + base &rarr; salt + water.",
      "[[HI(aq) + KOH(aq) -> KI(aq) + H2O(l)]]: <b>KI and water</b>.", 1)

    Q(T, "Calcium hydroxide dissolves in water. How many OH<sup>&minus;</sup> ions does each formula unit release, and which arrow belongs in its equation?",
      ["2 OH<sup>&minus;</sup>; a single arrow (&rarr;)", "2 OH<sup>&minus;</sup>; a double arrow (&rlarr;)",
       "1 OH<sup>&minus;</sup>; a single arrow (&rarr;)", "1 OH<sup>&minus;</sup>; a double arrow (&rlarr;)"],
      ["[[Ca(OH)2(aq) -> Ca^2+(aq) + 2 OH^-(aq)]]: two hydroxides, and a strong base dissociates completely.",
       "{Ca(OH)2} is a strong base, so the dissolved part dissociates completely: a single arrow.",
       "The subscript 2 outside the parentheses means two OH<sup>&minus;</sup> per formula unit.",
       "Both parts are wrong: two OH<sup>&minus;</sup> per formula unit, and strong bases get a single arrow."],
      "Read the subscript after (OH), and check the strong-base list.",
      "[[Ca(OH)2(aq) -> Ca^2+(aq) + 2 OH^-(aq)]]: <b>2 OH<sup>&minus;</sup>, single arrow</b>.", 2)

    # ======================= ch12-water (12) =======================
    T = 'ch12-water'
    Q(T, "Which equation shows the autoionization of water?",
      ["[[H2O(l) + H2O(l) <=> H3O^+(aq) + OH^-(aq)]]", "[[2 H2O(l) -> 2 H2(g) + O2(g)]]",
       "[[H2O(l) + H2O(l) -> H3O^+(aq) + OH^-(aq)]]", "[[H2O(l) + H2O(l) <=> H2O2(aq) + H2(g)]]"],
      ["One water molecule donates a proton to another; the double arrow shows that only a tiny fraction is ionized at any moment.",
       "This is the decomposition of water into elements (by electrolysis), not a proton transfer.",
       "A single arrow would mean water ionizes completely; it ionizes only about two molecules per billion.",
       "Autoionization moves a proton; it does not make hydrogen peroxide."],
      "Water is amphoteric: one molecule is the acid, the other the base.",
      "<b>[[H2O(l) + H2O(l) <=> H3O^+(aq) + OH^-(aq)]]</b>.", 1)

    Q(T, "Pure water at 25 °C has pH 7.00. What is its [{OH^-}]?",
      [sci('1.0', -7) + ' M', sci('1.0', -14) + ' M', '7.00 M', '0 M, because pure water contains no hydroxide'],
      ["In pure water [{H3O^+}] = [{OH^-}], and their product is 1.0 &times; 10<sup>&minus;14</sup>, so each is 1.0 &times; 10<sup>&minus;7</sup> M.",
       "1.0 &times; 10<sup>&minus;14</sup> is K<sub>w</sub>, the <i>product</i> of the two concentrations, not either one.",
       "7.00 is the pH (and pOH) of pure water, not a concentration.",
       "Water autoionizes slightly, making one {OH^-} for every {H3O^+}."],
      "Two equal concentrations multiply to 1.0 &times; 10<sup>&minus;14</sup>.",
      "&radic;(1.0 &times; 10<sup>&minus;14</sup>) = <b>1.0 &times; 10<sup>&minus;7</sup> M</b>.", 1)

    h = V('7.9', -5)
    Q(T, "A sample of tomato juice has [{H3O^+}] = " + sci('7.9', -5) + " M at 25 °C. What is [{OH^-}]?",
      [S(KW / h, 2), S(KW * h, 2), S(h / KW, 2), sci('1.0', -7) + ' M'],
      ["[{OH^-}] = K<sub>w</sub> / [{H3O^+}] = (1.0 &times; 10<sup>&minus;14</sup>) / (7.9 &times; 10<sup>&minus;5</sup>); two significant figures.",
       "This multiplies by K<sub>w</sub>; the product [{H3O^+}][{OH^-}] equals K<sub>w</sub>, so divide.",
       "This divides the wrong way (concentration / K<sub>w</sub>), giving an impossible value.",
       "1.0 &times; 10<sup>&minus;7</sup> M is [{OH^-}] in pure water; an acidic juice has less."],
      "Divide K<sub>w</sub> by the concentration you know.",
      "[{OH^-}] = 1.0 &times; 10<sup>&minus;14</sup> / 7.9 &times; 10<sup>&minus;5</sup> = <b>%s</b>." % S(KW / h, 2), 2, 1)

    o = V('5.5', -3)
    Q(T, "A dilute soap solution has [{OH^-}] = " + sci('5.5', -3) + " M at 25 °C. What is [{H3O^+}]?",
      [S(KW / o, 2), S(KW * o, 2), S(o / KW, 2), S(1 / o, 2)],
      ["[{H3O^+}] = K<sub>w</sub> / [{OH^-}] = (1.0 &times; 10<sup>&minus;14</sup>) / (5.5 &times; 10<sup>&minus;3</sup>).",
       "This multiplies by K<sub>w</sub> instead of dividing.",
       "This divides [{OH^-}] by K<sub>w</sub>; the concentration you know goes in the denominator.",
       "This leaves out K<sub>w</sub> (it computes 1 / [{OH^-}])."],
      "[{H3O^+}] = K<sub>w</sub> / [{OH^-}].",
      "1.0 &times; 10<sup>&minus;14</sup> / 5.5 &times; 10<sup>&minus;3</sup> = <b>%s</b>." % S(KW / o, 2), 2, 1)

    Q(T, "A solution has [{H3O^+}] = " + sci('3.8', -9) + " M at 25 °C. How is it classified?",
      ["Basic", "Acidic", "Neutral", "It cannot be classified without [{OH^-}]."],
      ["3.8 &times; 10<sup>&minus;9</sup> is smaller than 1.0 &times; 10<sup>&minus;7</sup>, so [{H3O^+}] &lt; [{OH^-}]: basic.",
       "This misreads the exponent: 10<sup>&minus;9</sup> is <i>smaller</i> than 10<sup>&minus;7</sup>.",
       "Neutral means exactly 1.0 &times; 10<sup>&minus;7</sup> M.",
       "[{H3O^+}] alone is enough: K<sub>w</sub> fixes [{OH^-}], and comparing with 10<sup>&minus;7</sup> M classifies it."],
      "Compare with 1.0 &times; 10<sup>&minus;7</sup> M. Which is bigger?",
      "[{H3O^+}] is below 1.0 &times; 10<sup>&minus;7</sup> M: <b>basic</b>.", 2)

    Q(T, "A solution has [{OH^-}] = " + sci('2.7', -11) + " M at 25 °C. How is it classified?",
      ["Acidic", "Basic", "Neutral", "Neither, because [{OH^-}] is too small to measure"],
      ["[{OH^-}] is far below 1.0 &times; 10<sup>&minus;7</sup> M, so [{H3O^+}] must be above it (K<sub>w</sub> = [{H3O^+}][{OH^-}]): acidic.",
       "Being given [{OH^-}] does not make a solution basic; this one has very little hydroxide.",
       "Neutral would need [{OH^-}] = 1.0 &times; 10<sup>&minus;7</sup> M.",
       "Every water solution has both ions; a small [{OH^-}] means a large [{H3O^+}]."],
      "If [{OH^-}] is below 10<sup>&minus;7</sup> M, where is [{H3O^+}]?",
      "[{OH^-}] &lt; 1.0 &times; 10<sup>&minus;7</sup> M, so [{H3O^+}] &gt; 1.0 &times; 10<sup>&minus;7</sup> M: <b>acidic</b>.", 2)

    Q(T, "Use the table (all at 25 °C). Which solution is the <b>most acidic</b>?",
      ["Solution D", "Solution A", "Solution B", "Solution C"],
      ["D: [{H3O^+}] = 1.0 &times; 10<sup>&minus;14</sup> / 3.3 &times; 10<sup>&minus;12</sup> = 3.0 &times; 10<sup>&minus;3</sup> M, the largest [{H3O^+}] of the four.",
       "A has [{H3O^+}] = 4.1 &times; 10<sup>&minus;5</sup> M, acidic but less than D's 3.0 &times; 10<sup>&minus;3</sup> M.",
       "B has a large [{OH^-}], so it is basic.",
       "C has [{H3O^+}] below 10<sup>&minus;7</sup> M, so it is basic."],
      "Convert every [{OH^-}] to [{H3O^+}] with K<sub>w</sub>, then compare.",
      "A 4.1 &times; 10<sup>&minus;5</sup>, B 1.3 &times; 10<sup>&minus;12</sup>, C 9.0 &times; 10<sup>&minus;9</sup>, D 3.0 &times; 10<sup>&minus;3</sup> M [{H3O^+}]: <b>Solution D</b>.", 3, 0,
      [{"type": "table", "cap": "Four solutions at 25 °C", "head": ["Solution", "Given"],
        "rows": [["A", "[{H3O^+}] = " + sci('4.1', -5) + " M"], ["B", "[{OH^-}] = " + sci('7.9', -3) + " M"],
                 ["C", "[{H3O^+}] = " + sci('9.0', -9) + " M"], ["D", "[{OH^-}] = " + sci('3.3', -12) + " M"]]}])

    a = D('0.045')
    Q(T, "What is [{OH^-}] in 0.045 M HBr at 25 °C?",
      [S(KW / a, 2), '0.045 M', S(KW * a, 2), S(KW / (2 * a), 2)],
      ["HBr is a strong acid, so [{H3O^+}] = 0.045 M; [{OH^-}] = 1.0 &times; 10<sup>&minus;14</sup> / 0.045.",
       "0.045 M is [{H3O^+}], not [{OH^-}].",
       "This multiplies by K<sub>w</sub> instead of dividing.",
       "This doubles [{H3O^+}]; HBr gives one {H3O^+} per molecule."],
      "Strong acid: [{H3O^+}] = the acid's molarity. Then use K<sub>w</sub>.",
      "[{H3O^+}] = 0.045 M; [{OH^-}] = 1.0 &times; 10<sup>&minus;14</sup> / 0.045 = <b>%s</b>." % S(KW / a, 2), 2, 1)

    b = D('0.0045')
    Q(T, "What is [{OH^-}] in 0.0045 M {Ba(OH)2}?",
      [S(2 * b, 2), S(b, 2), S(KW / (2 * b), 2), S(KW / b, 2)],
      ["[[Ba(OH)2(aq) -> Ba^2+(aq) + 2 OH^-(aq)]]: [{OH^-}] = 2 &times; 0.0045 M.",
       "This forgets the 2: each {Ba(OH)2} releases two hydroxide ions.",
       "This is [{H3O^+}], found from K<sub>w</sub>; the question asks for [{OH^-}].",
       "This is [{H3O^+}] with the factor of 2 forgotten as well."],
      "How many OH<sup>&minus;</sup> does one {Ba(OH)2} release?",
      "[{OH^-}] = 2 &times; 0.0045 M = <b>%s</b>." % S(2 * b, 2), 2, 1)

    c_ = D('0.0012')
    Q(T, "What is [{H3O^+}] in 0.0012 M {Ca(OH)2} at 25 °C?",
      [S(KW / (2 * c_), 2), S(KW / c_, 2), S(2 * c_, 2), S(KW * 2 * c_, 2)],
      ["[{OH^-}] = 2 &times; 0.0012 = 0.0024 M; [{H3O^+}] = 1.0 &times; 10<sup>&minus;14</sup> / 0.0024.",
       "This forgets to double [{OH^-}]: {Ca(OH)2} gives two hydroxides.",
       "0.0024 M is [{OH^-}]; the question asks for [{H3O^+}].",
       "This multiplies by K<sub>w</sub>; divide K<sub>w</sub> by [{OH^-}]."],
      "Double first, then divide K<sub>w</sub> by [{OH^-}].",
      "[{OH^-}] = 0.0024 M; [{H3O^+}] = 1.0 &times; 10<sup>&minus;14</sup> / 0.0024 = <b>%s</b>." % S(KW / (2 * c_), 2), 3, 1)

    Q(T, "A few drops of acid are added to pure water at 25 °C, and [{H3O^+}] rises. What happens to [{OH^-}]?",
      ["It falls, so that [{H3O^+}][{OH^-}] stays 1.0 &times; 10<sup>&minus;14</sup>.", "It rises along with [{H3O^+}].",
       "It stays at 1.0 &times; 10<sup>&minus;7</sup> M.", "It drops to zero, because an acidic solution has no {OH^-}."],
      ["K<sub>w</sub> is constant, so the two concentrations are inversely related, like a seesaw.",
       "If both rose, their product would grow larger than K<sub>w</sub>.",
       "[{OH^-}] is 1.0 &times; 10<sup>&minus;7</sup> M only when the solution is neutral.",
       "Every water solution contains both ions; [{OH^-}] gets small but never zero."],
      "The product of the two concentrations is fixed at 25 °C.",
      "K<sub>w</sub> is constant: [{OH^-}] <b>falls</b>.", 1)

    Q(T, "The relationship K<sub>w</sub> = [{H3O^+}][{OH^-}] = 1.0 &times; 10<sup>&minus;14</sup> applies to which solutions at 25 °C?",
      ["Every water solution: acidic, basic, or neutral", "Only pure water", "Only neutral solutions", "Only solutions of strong acids and bases"],
      ["K<sub>w</sub> holds in every aqueous solution at 25 °C, from lemon juice to drain cleaner.",
       "It is found from pure water, but it stays true when acids or bases are added.",
       "Acidic and basic solutions obey it too; only the balance between the two ions changes.",
       "Weak acids and bases, salts, and blood obey it as well."],
      "What stays the same when an acid is added to water?",
      "K<sub>w</sub> applies to <b>every water solution</b> at 25 °C.", 2)

    # ======================= ch12-ph (16) =======================
    T = 'ch12-ph'
    a = D('0.0072')
    Q(T, "What is the pH of 0.0072 M HBr?",
      [p(a, 2), qd(D(a).log10(), 2), qd(14 + D(a).log10(), 2), p(a, 1)],
      ["HBr is strong, so [{H3O^+}] = 0.0072 M; pH = &minus;log(0.0072); 2 significant figures give 2 decimal places.",
       "This leaves out the minus sign (pH = log[{H3O^+}]); the pH of a solution like this is positive.",
       "This is 14.00 &minus; pH, which is the pOH, not the pH.",
       "The value is right, but it has one decimal place; 0.0072 has 2 significant figures, so the pH needs 2 decimal places."],
      "pH = &minus;log[{H3O^+}]; decimal places in pH = significant figures in the concentration.",
      "pH = &minus;log(0.0072) = <b>%s</b>." % p(a, 2), 2, 1)

    a = V('2.85', -3)
    Q(T, "What is the pH of " + sci('2.85', -3) + " M HCl?",
      [p(a, 3), qd(D(a).log10(), 3), p(a, 2), qd(14 + D(a).log10(), 3)],
      ["HCl is strong, so [{H3O^+}] = 2.85 &times; 10<sup>&minus;3</sup> M; 3 significant figures give 3 decimal places.",
       "This drops the minus sign in pH = &minus;log[{H3O^+}].",
       "This has 2 decimal places; 2.85 has 3 significant figures, so the pH needs 3 decimal places.",
       "This is the pOH (14 &minus; pH), not the pH."],
      "Count significant figures in 2.85 to set the decimal places.",
      "pH = &minus;log(2.85 &times; 10<sup>&minus;3</sup>) = <b>%s</b>." % p(a, 3), 2, 1)

    b = D('0.0039')
    Q(T, "What is the pH of 0.0039 M NaOH at 25 °C?",
      [sub14(p(b, 2)), p(b, 2), sub14(p(2 * b, 2)), qd(D(sub14(p(b, 2))), 1)],
      ["[{OH^-}] = 0.0039 M; pOH = &minus;log(0.0039) = %s; pH = 14.00 &minus; %s." % (p(b, 2), p(b, 2)),
       "This is the pOH. For a base, subtract the pOH from 14.00 to get the pH.",
       "This doubles [{OH^-}]; NaOH has only one OH<sup>&minus;</sup> per formula unit.",
       "This has one decimal place; 0.0039 has 2 significant figures, so the pH needs 2 decimal places."],
      "Base: [{OH^-}] &rarr; pOH &rarr; pH = 14.00 &minus; pOH.",
      "pOH = %s; pH = 14.00 &minus; %s = <b>%s</b>." % (p(b, 2), p(b, 2), sub14(p(b, 2))), 2, 1)

    b = D('0.0033')
    Q(T, "What is the pH of 0.0033 M {Ba(OH)2} at 25 °C?",
      [sub14(p(2 * b, 2)), sub14(p(b, 2)), p(2 * b, 2), qd(D(sub14(p(2 * b, 2))), 1)],
      ["[{OH^-}] = 2 &times; 0.0033 = 0.0066 M; pOH = %s; pH = 14.00 &minus; %s." % (p(2 * b, 2), p(2 * b, 2)),
       "This forgets to double [{OH^-}]: each {Ba(OH)2} releases two hydroxide ions.",
       "This is the pOH; subtract it from 14.00.",
       "This has only one decimal place; the concentration has 2 significant figures."],
      "Double [{OH^-}] for {Ba(OH)2}, then pOH, then pH.",
      "[{OH^-}] = 0.0066 M; pOH = %s; pH = <b>%s</b>." % (p(2 * b, 2), sub14(p(2 * b, 2))), 3, 1)

    b = V('3.3', -4)
    Q(T, "Limewater is a solution of {Ca(OH)2}. What is the pH of " + sci('3.3', -4) + " M {Ca(OH)2} at 25 °C?",
      [sub14(p(2 * b, 2)), sub14(p(b, 2)), p(2 * b, 2), qd(-D(sub14(p(2 * b, 2))), 2)],
      ["[{OH^-}] = 2 &times; 3.3 &times; 10<sup>&minus;4</sup> = 6.6 &times; 10<sup>&minus;4</sup> M; pOH = %s; pH = 14.00 &minus; %s." % (p(2 * b, 2), p(2 * b, 2)),
       "This forgets the factor of 2 for {Ca(OH)2}.",
       "This is the pOH, not the pH.",
       "A pH this negative is a sign of a dropped minus sign; basic solutions have pH above 7."],
      "{Ca(OH)2} gives two OH<sup>&minus;</sup>; finish with pH = 14.00 &minus; pOH.",
      "[{OH^-}] = 6.6 &times; 10<sup>&minus;4</sup> M; pOH = %s; pH = <b>%s</b>." % (p(2 * b, 2), sub14(p(2 * b, 2))), 3, 1)

    pv = '3.37'
    Q(T, "A glass of orange juice has pH 3.37. What is its [{H3O^+}]?",
      [S(ten(pv), 2), S(ten(sub14(pv)), 2), S(D(10) ** D(pv), 2), S(ten(pv), 3)],
      ["[{H3O^+}] = 10<sup>&minus;3.37</sup>; 2 decimal places in the pH give 2 significant figures.",
       "This is 10<sup>&minus;(14 &minus; pH)</sup>, which is [{OH^-}], not [{H3O^+}].",
       "This leaves out the minus sign: 10<sup>3.37</sup> instead of 10<sup>&minus;3.37</sup>.",
       "The value is right, but it has 3 significant figures; a pH with 2 decimal places gives 2."],
      "[{H3O^+}] = 10<sup>&minus;pH</sup>.",
      "10<sup>&minus;3.37</sup> = <b>%s</b>." % S(ten(pv), 2), 2, 1)

    pv = '9.62'
    Q(T, "A hand soap solution has pH 9.62 at 25 °C. What is its [{OH^-}]?",
      [S(ten(sub14(pv)), 2), S(ten(pv), 2), sub14(pv) + ' M', S(D(10) ** D(sub14(pv)), 2)],
      ["pOH = 14.00 &minus; 9.62 = 4.38; [{OH^-}] = 10<sup>&minus;4.38</sup>.",
       "10<sup>&minus;9.62</sup> is [{H3O^+}], not [{OH^-}].",
       "4.38 is the pOH; it is not a concentration. Take 10<sup>&minus;pOH</sup>.",
       "This leaves out the minus sign: 10<sup>4.38</sup> instead of 10<sup>&minus;4.38</sup>."],
      "Find the pOH first, then [{OH^-}] = 10<sup>&minus;pOH</sup>.",
      "pOH = 4.38; [{OH^-}] = 10<sup>&minus;4.38</sup> = <b>%s</b>." % S(ten(sub14(pv)), 2), 3, 1)

    a = V('7.94', -6)
    Q(T, "What is the pH of a solution with [{H3O^+}] = " + sci('7.94', -6) + " M?",
      [p(a, 3), p(a, 2), qd(D(a).log10(), 3), qd(14 + D(a).log10(), 3)],
      ["pH = &minus;log(7.94 &times; 10<sup>&minus;6</sup>); 3 significant figures give 3 decimal places.",
       "This has 2 decimal places; 7.94 has 3 significant figures.",
       "This leaves out the minus sign in pH = &minus;log[{H3O^+}].",
       "This is the pOH, 14 &minus; pH."],
      "Three significant figures in the concentration &rarr; three decimal places in the pH.",
      "&minus;log(7.94 &times; 10<sup>&minus;6</sup>) = <b>%s</b>." % p(a, 3), 2, 1)

    po = '3.85'
    Q(T, "A solution has pOH 3.85 at 25 °C. What is its pH?",
      [sub14(po), po, qd(D('14.00') + D(po), 2), S(ten(po), 2)],
      ["pH + pOH = 14.00, so pH = 14.00 &minus; 3.85.",
       "This repeats the pOH; the pH is 14.00 minus the pOH.",
       "This adds the pOH to 14.00 instead of subtracting.",
       "This is [{OH^-}] = 10<sup>&minus;3.85</sup>, a concentration, not the pH."],
      "pH + pOH = 14.00.",
      "pH = 14.00 &minus; 3.85 = <b>%s</b> (basic).", 1, 1)
    B[-1]['w'] = B[-1]['w'] % sub14(po)

    Q(T, "Use the table of typical pH values. Which item has about 1000 times the [{H3O^+}] of black coffee?",
      ["Lemon juice", "Vinegar", "Cola", "Milk"],
      ["Lemon juice (pH 2) is 3 pH units below coffee (pH 5): 10 &times; 10 &times; 10 = 1000 times the [{H3O^+}].",
       "Vinegar (pH 3) is 2 units below coffee: 10<sup>2</sup> = 100 times, not 1000.",
       "Cola (pH 2.5) is 2.5 units below coffee: about 300 times.",
       "Milk (pH 6.5) has a <i>higher</i> pH than coffee, so it has less {H3O^+}."],
      "Each pH unit is a factor of 10. How many units is 1000?",
      "1000 = 10<sup>3</sup>: 3 pH units below coffee's 5, so pH 2: <b>lemon juice</b>.", 2, 0,
      [{"type": "table", "cap": "Typical pH values (real samples vary)", "head": ["Item", "pH"],
        "rows": [["Lemon juice", "2"], ["Cola", "2.5"], ["Vinegar", "3"], ["Black coffee", "5"], ["Milk", "6.5"], ["Baking soda in water", "8.3"], ["Household ammonia", "11.5"]]}])

    Q(T, "Four solutions have pH 8.3, 2.5, 6.5, and 11.5. Which list puts them in order of <b>increasing acidity</b> (least acidic first)?",
      ["11.5, 8.3, 6.5, 2.5", "2.5, 6.5, 8.3, 11.5", "6.5, 8.3, 2.5, 11.5", "8.3, 11.5, 2.5, 6.5"],
      ["Acidity increases as pH decreases, so the highest pH (least acidic) comes first.",
       "This is decreasing acidity (most acidic first); lower pH means more acidic.",
       "This order does not follow the pH values at all; sort by pH, highest first.",
       "This is not sorted; least acidic means the highest pH."],
      "Lower pH = more acidic.",
      "Least acidic (highest pH) to most acidic: <b>11.5, 8.3, 6.5, 2.5</b>.", 2)

    Q(T, "Solution X has pH 3.0 and solution Y has pH 6.0. How does [{H3O^+}] in X compare with Y?",
      ["X has 1000 times the [{H3O^+}] of Y.", "X has 2 times the [{H3O^+}] of Y.", "X has 30 times the [{H3O^+}] of Y.", "Y has 1000 times the [{H3O^+}] of X."],
      ["Three pH units apart: 10 &times; 10 &times; 10 = 1000, and the lower pH (X) has more {H3O^+}.",
       "This divides the pH values (6.0 / 3.0); pH is logarithmic, so 3 units is a factor of 10<sup>3</sup>.",
       "Each unit is a factor of 10, and factors multiply: 10 &times; 10 &times; 10 = 1000, not 10 &times; 3.",
       "The factor is right, but the direction is reversed: the lower pH has more {H3O^+}."],
      "Each pH unit is a tenfold change in [{H3O^+}].",
      "10<sup>6.0 &minus; 3.0</sup> = 10<sup>3</sup>: <b>X has 1000 times</b> the [{H3O^+}] of Y.", 2)

    Q(T, "A patient's arterial blood gas shows pH 7.52. How is this described?",
      ["Alkalosis (above the normal 7.35&ndash;7.45)", "Acidosis (below the normal range)", "Normal (within 7.35&ndash;7.45)", "Neutral, because it is close to 7"],
      ["Normal arterial pH is 7.35&ndash;7.45; 7.52 is above it, so the blood is too basic: alkalosis.",
       "Acidosis is a pH <i>below</i> 7.35.",
       "7.52 is outside the normal range, which ends at 7.45.",
       "Blood is judged against its own normal range, 7.35&ndash;7.45, not against 7.00."],
      "Compare with the normal arterial range, 7.35&ndash;7.45.",
      "7.52 &gt; 7.45: <b>alkalosis</b>.", 1)

    pv = '7.38'
    Q(T, "By the next morning, after treatment has opened Mateo's airways, his arterial pH is 7.38. What is his [{H3O^+}] now?",
      [S(ten(pv), 2), S(D(10) ** D(pv), 2), S(ten(pv), 3), S(ten(sub14(pv)), 2)],
      ["[{H3O^+}] = 10<sup>&minus;7.38</sup>; two decimal places give two significant figures. pH 7.38 is back inside 7.35&ndash;7.45.",
       "This leaves out the minus sign: 10<sup>7.38</sup>.",
       "The value is right, but a pH with 2 decimal places gives 2 significant figures, not 3.",
       "This is 10<sup>&minus;(14 &minus; pH)</sup>, which is [{OH^-}]."],
      "[{H3O^+}] = 10<sup>&minus;pH</sup>.",
      "10<sup>&minus;7.38</sup> = <b>%s</b>, within the normal range." % S(ten(pv), 2), 2, 1)

    a = V('6.10', -9)
    Q(T, "A solution has [{H3O^+}] = " + sci('6.10', -9) + " M. Which pH is reported correctly?",
      [p(a, 3), p(a, 2), p(a, 4), p(a, 1)],
      ["6.10 has 3 significant figures, so the pH has 3 decimal places.",
       "This gives the pH 3 significant figures in all; the digit before the decimal point comes from the power of 10 and does not count.",
       "This keeps too many digits; 3 significant figures in the concentration allow 3 decimal places.",
       "This keeps too few digits; the trailing zero in 6.10 is significant."],
      "Decimal places in pH = significant figures in the concentration.",
      "3 significant figures &rarr; 3 decimal places: pH = <b>%s</b>." % p(a, 3), 2, 1)

    a1, a2 = D('0.012'), D('0.0012')
    Q(T, "A 0.012 M {HNO3} solution is diluted tenfold, to 0.0012 M. What is the new pH?",
      [p(a2, 2), p(a1 * 10, 2), p(a1, 2), qd(D(p(a1, 2)) * 10, 1)],
      ["pH = &minus;log(0.0012); a tenfold dilution raises the pH of a strong acid by one unit, from %s." % p(a1, 2),
       "This treats dilution as making the acid more concentrated; diluting lowers [{H3O^+}] and raises the pH.",
       "This is the pH before dilution; diluting a strong acid changes [{H3O^+}].",
       "This multiplies the pH by 10; a tenfold change in concentration changes the pH by 1."],
      "A factor of 10 in [{H3O^+}] is one pH unit.",
      "&minus;log(0.0012) = <b>%s</b>, one unit higher than %s." % (p(a2, 2), p(a1, 2)), 2, 1)

    # ======================= ch12-buffers (10) =======================
    T = 'ch12-buffers'
    Q(T, "What is a buffer?",
      ["A solution that resists changes in pH when small amounts of acid or base are added",
       "A solution whose pH is exactly 7.00", "A mixture of a strong acid and a strong base",
       "A solution whose pH never changes, no matter how much acid is added"],
      ["A buffer limits pH changes; blood stays at 7.35&ndash;7.45 largely because of buffers.",
       "Buffers can hold a pH far from 7; an acetate buffer is acidic.",
       "A strong acid and a strong base simply neutralize each other; neither part remains to absorb more.",
       "A buffer has a limited capacity; add too much acid and the pH falls sharply."],
      "Think of what blood does when acid enters it.",
      "A buffer <b>resists pH change</b> when small amounts of acid or base are added.", 1)

    Q(T, "Which mixture is a buffer?",
      ["HClO and NaClO", "{HClO4} and {NaClO4}", "HClO and NaCl", "NaOH and NaClO"],
      ["Hypochlorous acid, HClO, is a weak acid, and NaClO supplies ClO<sup>&minus;</sup>, its conjugate base.",
       "{HClO4} (perchloric acid) is a strong acid, so its anion cannot take back a proton.",
       "HClO is weak, but Cl<sup>&minus;</sup> is not its conjugate base (hypochlorite, ClO<sup>&minus;</sup>, is).",
       "NaOH is a strong base, and there is no weak acid to neutralize added base."],
      "A weak acid plus a salt of its own conjugate base.",
      "HClO/ClO<sup>&minus;</sup> differ by one H<sup>+</sup>, and HClO is weak: <b>HClO and NaClO</b>.", 2)

    Q(T, "Which mixture is <b>not</b> a buffer?",
      ["HI and NaI", "HF and KF", "{NH3} and {NH4Br}", "{NaH2PO4} and {Na2HPO4}"],
      ["HI is a strong acid; it is fully ionized, and I<sup>&minus;</sup> cannot take back a proton.",
       "HF is weak and F<sup>&minus;</sup> is its conjugate base: a buffer.",
       "{NH3} is a weak base and {NH4^+} is its conjugate acid: a buffer.",
       "{H2PO4^-} and {HPO4^2-} differ by one H<sup>+</sup>, and neither is strong: a buffer."],
      "Look for a strong acid or base: it cannot be part of a buffer.",
      "HI is on the strong-acid list: <b>HI and NaI</b> is not a buffer.", 2)

    Q(T, "A buffer contains {HNO2} and {NaNO2}. Which species reacts with a small amount of added {H3O^+}?",
      ["{NO2^-}", "{HNO2}", "Na<sup>+</sup>", "{H2O}"],
      ["The conjugate base takes the proton: [[NO2^-(aq) + H3O^+(aq) -> HNO2(aq) + H2O(l)]].",
       "{HNO2} is the acid partner; it reacts with added base, not added acid.",
       "Na<sup>+</sup> is a spectator ion; it does not accept protons.",
       "Water alone cannot absorb added acid; that is why pure water's pH changes so much."],
      "Added acid is neutralized by the base partner.",
      "[[NO2^-(aq) + H3O^+(aq) -> HNO2(aq) + H2O(l)]]: <b>{NO2^-}</b>.", 2)

    Q(T, "A buffer contains HF and F<sup>&minus;</sup>. Which equation shows it neutralizing a small amount of added {OH^-}?",
      ["[[HF(aq) + OH^-(aq) -> F^-(aq) + H2O(l)]]", "[[F^-(aq) + H3O^+(aq) -> HF(aq) + H2O(l)]]",
       "[[H3O^+(aq) + OH^-(aq) -> 2 H2O(l)]]", "[[HF(aq) + H2O(l) <=> H3O^+(aq) + F^-(aq)]]"],
      ["The weak acid partner gives up its proton to the added hydroxide, making more F<sup>&minus;</sup>.",
       "This is how the buffer handles added <i>acid</i>.",
       "A buffer has very little {H3O^+} on hand; the HF partner is what absorbs {OH^-}.",
       "This is HF ionizing in water; it does not use up the added {OH^-}."],
      "Added base is neutralized by the acid partner.",
      "<b>[[HF(aq) + OH^-(aq) -> F^-(aq) + H2O(l)]]</b>.", 2)

    Q(T, "Which pair makes up the main buffer in blood?",
      ["{H2CO3} and {HCO3^-}", "HCl and Cl<sup>&minus;</sup>", "{H2CO3} and {CO3^2-}", "NaOH and Na<sup>+</sup>"],
      ["Carbonic acid (weak) and bicarbonate (its conjugate base) are the bicarbonate buffer.",
       "Stomach acid is HCl, but a strong acid cannot buffer, and it is not the blood's buffer.",
       "These differ by two H<sup>+</sup>; a buffer pair differs by one.",
       "NaOH is a strong base, and Na<sup>+</sup> does not react with acids or bases."],
      "Blood's buffer links carbon dioxide to H<sup>+</sup>.",
      "<b>{H2CO3}/{HCO3^-}</b>, the bicarbonate buffer.", 1)

    Q(T, "The body can adjust both partners of the bicarbonate buffer. Which organ controls the blood's {HCO3^-} level, and how fast?",
      ["The kidneys, over hours to days", "The lungs, within minutes", "The kidneys, within seconds", "The stomach, by secreting HCl"],
      ["The kidneys keep or excrete bicarbonate (and excrete acid in urine), a slow adjustment over hours to days.",
       "The lungs control {CO2} (and so {H2CO3}) within minutes; bicarbonate is the kidneys' job.",
       "The organ is right, but the kidneys act slowly, over hours to days.",
       "Stomach acid does not set blood bicarbonate; the kidneys do."],
      "Lungs handle {CO2}; which organ handles bicarbonate?",
      "<b>The kidneys</b>, over hours to days (the lungs adjust {CO2} in minutes).", 2)

    Q(T, "In the blood, {CO2} + {H2O} &rlarr; {H2CO3} &rlarr; H<sup>+</sup> + {HCO3^-}. Which change, by itself, <b>lowers</b> blood pH?",
      ["A rise in blood {CO2}", "A drop in blood {CO2}", "Faster, deeper breathing", "The kidneys keeping more {HCO3^-}"],
      ["More {CO2} makes more {H2CO3}, which releases more H<sup>+</sup>, so [{H3O^+}] rises and the pH falls.",
       "Less {CO2} means less carbonic acid and less H<sup>+</sup>, so the pH rises.",
       "Faster breathing blows off {CO2}, which removes acid and raises the pH.",
       "Bicarbonate is the base partner; more of it neutralizes acid and raises the pH."],
      "More {CO2} means more of which acid?",
      "{CO2} up, then {H2CO3} up, then H<sup>+</sup> up: <b>a rise in blood {CO2}</b> lowers the pH.", 2)

    Q(T, "A hiker who climbs quickly to high altitude breathes faster and deeper than usual and blows off extra {CO2}. What happens to the blood pH?",
      ["It rises, because less {H2CO3} forms and less H<sup>+</sup> is released (respiratory alkalosis).",
       "It falls, because the buffer runs out of bicarbonate (respiratory acidosis).",
       "It falls, because removing {CO2} releases more H<sup>+</sup>.",
       "It does not change, because the buffer keeps the pH exactly constant."],
      ["Less {CO2} means less carbonic acid and fewer H<sup>+</sup>, so [{H3O^+}] falls and the pH rises.",
       "Blowing off {CO2} removes acid; it does not use up bicarbonate.",
       "This is reversed: less {CO2} means less acid.",
       "A buffer limits pH change, but changing {CO2} changes the buffer's own acid partner."],
      "Less {CO2} means less of which acid?",
      "{CO2} down &rarr; {H2CO3} down &rarr; H<sup>+</sup> down: <b>pH rises (respiratory alkalosis)</b>.", 2)

    Q(T, "A buffer is made with 0.10 mol of a weak acid, HA, and 0.10 mol of its conjugate base, A<sup>&minus;</sup>. Then 0.20 mol of HCl is added. What happens?",
      ["The A<sup>&minus;</sup> is used up after 0.10 mol of HCl, and the extra acid makes the pH drop sharply.",
       "The pH stays nearly constant, because buffers absorb any amount of acid.",
       "The HA neutralizes the added HCl, so the pH rises.",
       "The pH stays nearly constant, because HCl is a weak acid in a buffer."],
      ["Only 0.10 mol of A<sup>&minus;</sup> can react with H<sup>+</sup>; the remaining 0.10 mol of HCl is past the buffer's capacity.",
       "A buffer has a limited capacity, set by how much of each partner it contains.",
       "HA is the acid partner; it reacts with added base, not added acid.",
       "HCl is a strong acid in any solution."],
      "Compare the moles of HCl with the moles of A<sup>&minus;</sup>.",
      "0.20 mol HCl &gt; 0.10 mol A<sup>&minus;</sup>: the <b>capacity is exceeded, and the pH drops sharply</b>.", 3)


if __name__ == '__main__':
    build()
    dump(sys.argv[1])
