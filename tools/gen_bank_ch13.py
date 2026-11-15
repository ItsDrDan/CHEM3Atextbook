#!/usr/bin/env python3
"""Builds bank/ch13.json (Chapter 13 Try It items: collision theory and reaction rates, dynamic equilibrium,
equilibrium constants, Le Chatelier's principle).
Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch13.py bank/ch13.json
Conventions (Chapter 13 text): effective collision = right orientation + at least Ea; Ea = top of hill - reactants,
dH = products - reactants; rate factors: concentration, temperature, surface area, catalyst (lowers Ea, not used up,
dH unchanged); rule of thumb: rate about doubles per 10 C rise. Equilibrium: equal rates, constant (not equal)
concentrations, closed system, reachable from either side. K = products over reactants, coefficients as exponents,
(s) and (l) left out, no units; K >> 1 products favored, K << 1 reactants favored; reverse reaction K' = 1/K.
Le Chatelier: add -> away, take -> toward; heat is a reactant (dH > 0) or a product (dH < 0); only temperature
changes K; smaller volume -> fewer moles of gas; catalysts, inert gases, solids and liquids: no shift.
Going Further material (Ka, Kb, Ksp, common-ion effect) is kept out. Sig figs from the givens; no trailing-zero
givens without a decimal point in calculation stems; round half up.
Markup: {NO2} or {HCO3^-} formula, [[2 NO(g) + O2(g) <=> 2 NO2(g)]] equation (a display line in a stem).
The helpers are imported by tools/gen_adapt_ch13.py. Every number, K expression and keyed shift is rechecked
independently by tools/check_bank_ch13.py."""
import json, sys, re, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
M = '&minus;'
B = []
CFG = {'prefix': 'c13-%03d', 'adapt': False}


# ---------------- formulas, equations, K expressions ----------------
def F(s):
    base, _, ch = s.partition('^')
    out = re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', base)
    return out + ('<sup>%s</sup>' % ch.replace('-', M) if ch else '')
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
def X(s, disp=False):
    if disp: s = re.sub(r'\s*\[\[(.+?)\]\]\s*', lambda m: '<span style="display:block;text-align:center;margin:6px 0">%s</span>' % EQ(m.group(1)), s)
    s = re.sub(r'\[\[(.+?)\]\]', lambda m: EQ(m.group(1)), s)
    s = re.sub(r'(?<![\w;])-(?=\d)', M, s)
    return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)
def term(f, p): return '[%s]%s' % (F(f), '<sup>%d</sup>' % p if p > 1 else '')
def KX(num, den):
    """K expression as HTML from [(formula, power)] lists."""
    n = ''.join(term(f, p) for f, p in num) or '1'
    if not den: return 'K = ' + n
    d = ''.join(term(f, p) for f, p in den)
    return 'K = %s / %s' % (n, '(%s)' % d if len(den) > 1 else d)

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
def sfs(s):
    s = s.lstrip('-')
    if '.' in s: return len(s.replace('.', '').lstrip('0'))
    return len(s.lstrip('0').rstrip('0'))
def ns(*a): return min(sfs(x) for x in a)
def Kv(num_, den_):
    """K from [(conc string, power)] lists (round once at the end)."""
    v = D(1)
    for c, p in num_: v *= D(c) ** p
    for c, p in den_: v /= D(c) ** p
    return v

def Q(t_, q, c, y, h, w, d, k=0, f=None):
    y = list(y)
    if CFG['adapt'] and not y[0].startswith('Correct: '): y[0] = 'Correct: ' + y[0]
    it = {"id": CFG['prefix'] % (len(B) + 1), "t": t_, "q": X(q, True), "c": [X(x) for x in c], "y": [X(x) for x in y],
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

def energy_plot(r, top, p):
    """energy diagram (fbx plot): reactants r, top of the hill, products p (kJ)."""
    up = [r + (top - r) * fr for fr in (0.08, 0.4, 0.8)]
    dn = [top - (top - p) * fr for fr in (0.2, 0.6, 0.92)]
    pts = [[0, r], [1.5, r], [2.5, up[0]], [3.5, up[1]], [4.3, up[2]], [5, top], [5.7, dn[0]], [6.5, dn[1]], [7.3, dn[2]], [8, p], [10, p]]
    return [{"type": "plot", "x": {"min": 0, "max": 10, "label": "Reaction progress", "ticks": []},
             "y": {"min": 0, "max": 140, "label": "Energy (kJ)", "noTicks": True},
             "series": [{"pts": [[a, round(b, 1)] for a, b in pts]}],
             "hlines": [{"y": r}, {"y": top}, {"y": p}],
             "marks": [[1.7, r - 12, "Reactants %d kJ" % r], [5, top + 8, "%d kJ" % top], [8.4, p + 7, "Products %d kJ" % p]]}]


def build():
    # ======================= ch13-rates (16) =======================
    T = 'ch13-rates'
    Q(T, "According to collision theory, which two things must be true of a collision for it to form products?",
      ["The particles must hit with the right orientation and with at least the activation energy.",
       "The particles must hit with the right orientation; any amount of energy is enough.",
       "The particles must hit with at least the activation energy; the direction they hit from does not matter.",
       "The particles only need to collide; every collision forms products."],
      ["An effective collision needs both: the right parts touching (orientation) and enough energy to reach E<sub>a</sub>.",
       "A gentle collision with the right orientation still fails if it does not reach the activation energy.",
       "Even a hard collision fails if the wrong parts of the molecules touch, because the right bonds cannot break and form.",
       "Most collisions do not form products; only effective collisions do."],
      "Think of the two conditions that make a collision effective.",
      "An effective collision has <b>the right orientation and at least E<sub>a</sub></b>.", 1)

    Q(T, "Two molecules collide with more than enough energy to react, yet no products form. What is the most likely reason?",
      ["They hit with the wrong orientation, so the bonds that needed to break were not in contact.",
       "The activation energy was too low for the reaction to happen.",
       "The reaction had reached equilibrium, so all reactions had stopped.",
       "High-energy collisions always bounce apart without reacting."],
      ["Energy is only one requirement; the right parts of the molecules must also collide.",
       "A lower activation energy makes a reaction easier, not harder, and these molecules had more than enough energy.",
       "Reactions do not stop at equilibrium; the forward and reverse reactions keep running at equal rates.",
       "Collisions with at least E<sub>a</sub> and the right orientation do react; high energy is not the problem."],
      "The energy was enough. What is the other requirement?",
      "Enough energy but no reaction: <b>wrong orientation</b>.", 2)

    r, top, p = 35, 118, 72
    Q(T, "Use the energy diagram. What is the activation energy of the forward reaction?",
      ["%d kJ" % (top - r), "%d kJ" % (top - p), "%d kJ" % top, "%d kJ" % (p - r)],
      ["E<sub>a</sub> is measured from the reactants (%d kJ) up to the top of the hill (%d kJ): %d &minus; %d = %d kJ." % (r, top, top, r, top - r),
       "This measures from the products to the top of the hill. E<sub>a</sub> for the forward reaction starts at the reactants.",
       "This is the energy of the top of the hill read from the bottom of the graph, not its height above the reactants.",
       "This is &Delta;H (%d &minus; %d), the difference between products and reactants, not the height of the hill." % (p, r)],
      "Start at the reactant energy and measure up to the top of the hill.",
      "E<sub>a</sub> = top &minus; reactants = %d kJ &minus; %d kJ = <b>%d kJ</b>." % (top, r, top - r), 2, 1, energy_plot(r, top, p))

    r, top, p = 88, 142, 23
    Q(T, "A reaction's energy diagram shows the reactants at %d kJ, the products at %d kJ, and the peak of the hill at %d kJ. What is &Delta;H, and is the reaction exothermic or endothermic?" % (r, p, top),
      ["-%d kJ, exothermic" % (r - p), "+%d kJ, endothermic" % (r - p), "+%d kJ, endothermic" % (top - r), "-%d kJ, exothermic" % (top - p)],
      ["&Delta;H = products &minus; reactants = %d &minus; %d = &minus;%d kJ. The products are lower in energy, so heat is released." % (p, r, r - p),
       "This is reactants &minus; products. &Delta;H is products &minus; reactants, which is negative here.",
       "This is the activation energy (%d &minus; %d), the height of the hill, not &Delta;H." % (top, r),
       "This measures from the peak of the hill down to the products; &Delta;H compares only the start and the end."],
      "&Delta;H = energy of the products &minus; energy of the reactants.",
      "&Delta;H = %d kJ &minus; %d kJ = <b>&minus;%d kJ, exothermic</b>." % (p, r, r - p), 2, 1)

    Q(T, "How does adding a catalyst change the energy diagram of a reaction?",
      ["It lowers the top of the hill, but the reactant and product energies stay the same.",
       "It lowers the energy of the products, so &Delta;H becomes more negative.",
       "It raises the top of the hill, so fewer collisions succeed.",
       "It lowers the hill and the reactant energy by the same amount."],
      ["A catalyst gives a path with a lower activation energy; the start and end points, and so &Delta;H, do not change.",
       "A catalyst does not change &Delta;H; the products end at the same energy with or without it.",
       "A catalyst lowers E<sub>a</sub>; a higher hill would slow the reaction down.",
       "The reactants have the same energy with or without a catalyst; only the path between reactants and products changes."],
      "A catalyst changes the path, not the start or the end.",
      "<b>A lower hill (smaller E<sub>a</sub>), the same &Delta;H</b>.", 2)

    Q(T, "Full-strength household bleach removes a coffee stain from a white shirt much faster than bleach diluted with water. Why?",
      ["The full-strength bleach has more hypochlorite ions in each milliliter, so they collide with the stain molecules more often.",
       "Water is a catalyst that slows the reaction down.",
       "Diluting bleach raises the activation energy of the reaction.",
       "Full-strength bleach is hotter than diluted bleach."],
      ["A higher concentration means more collisions per second, so more effective collisions and a faster reaction.",
       "Water is not a catalyst here, and a catalyst speeds a reaction up; diluting just spreads the reacting ions out.",
       "Concentration changes the number of collisions, not the height of the energy hill.",
       "Both are at room temperature; the difference is how many reacting ions are in the same space."],
      "A higher concentration of a reactant: what happens to the number of collisions?",
      "Higher concentration &rarr; <b>more collisions per second</b> &rarr; faster stain removal.", 1)

    Q(T, "Why does storing leftovers in a refrigerator at 4 °C slow down spoilage?",
      ["At low temperature, molecules collide less often and fewer collisions have at least the activation energy, so the bacteria's reactions slow down.",
       "Cold kills the bacteria, so no spoilage reactions can happen.",
       "Cold raises the activation energy of the spoilage reactions.",
       "Cold removes the oxygen from the food, so the reactions stop."],
      ["Bacterial growth depends on enzyme-catalyzed reactions, which slow down at low temperature like any reaction.",
       "Cold slows most bacteria but does not kill them; that is why food is also cooked to a safe temperature.",
       "E<sub>a</sub> belongs to the reaction path; cooling changes how many collisions reach it, not the height of the hill.",
       "Food in a refrigerator is still surrounded by air; cold slows reactions by slowing the molecules."],
      "Cooling slows the particles down.",
      "Colder &rarr; fewer, weaker collisions &rarr; <b>slower reactions</b>. The bacteria are slowed, not killed.", 1)

    Q(T, "After a cardiac arrest, some patients' body temperature is lowered by a few degrees on purpose for a time (targeted temperature management), partly to lower the brain's need for oxygen. Which collision-theory idea explains why cooling lowers the oxygen need?",
      ["At a lower temperature, molecules collide less often and fewer collisions have at least the activation energy, so the cells' enzyme reactions run more slowly.",
       "At a lower temperature, molecules collide less often, but the fraction of collisions with enough energy stays the same.",
       "Cooling raises the activation energy of the cells' reactions.",
       "Cooling destroys the enzymes, so the cells' reactions stop."],
      ["Both effects slow the reactions that use oxygen; the smaller fraction of collisions with enough energy is usually the bigger effect.",
       "This is only half of the answer: at a lower temperature, fewer of the collisions also reach E<sub>a</sub>.",
       "Temperature does not change the height of the energy hill; it changes how many collisions get over it.",
       "A few degrees of cooling slows enzymes; it does not destroy them, and the reactions keep running."],
      "Temperature has two effects on collisions.",
      "Cooler: <b>fewer collisions, and fewer of them with at least E<sub>a</sub></b>, so metabolism slows.", 2)

    Q(T, "A steel nail held in a flame only glows, but a pad of fine steel wool of the same mass burns with bright sparks. Why?",
      ["The thin fibers of steel wool have much more surface area, so many more iron atoms can collide with {O2}.",
       "Steel wool is made of a different element than the nail.",
       "The flame is hotter around steel wool than around a nail.",
       "Steel wool contains a catalyst that the nail lacks."],
      ["More surface area exposes more of the solid to collisions, so the reaction is much faster.",
       "Both are mostly iron; the difference is how much of the iron is exposed to the air.",
       "The same flame is used; the difference is in the solid, not the flame.",
       "No catalyst is involved; the fine fibers simply expose more iron to oxygen."],
      "Same metal, same mass. What is different about how much of it is exposed?",
      "Fine fibers = <b>more surface area</b> = more collisions with {O2}.", 1)

    Q(T, "Which statement about a catalyst is true?",
      ["It speeds up a reaction by providing a path with a lower activation energy, and it is not used up.",
       "It speeds up a reaction by raising the temperature of the mixture.",
       "It is used up as the reaction runs, so more must keep being added.",
       "It makes a reaction release more heat (a more negative &Delta;H)."],
      ["A catalyst lowers E<sub>a</sub> so more collisions are effective, and it comes out of the reaction unchanged.",
       "A catalyst works at the same temperature; it lowers the energy hill instead.",
       "A catalyst is regenerated, so a small amount can be used over and over.",
       "A catalyst does not change &Delta;H; the reactants and products have the same energies with or without it."],
      "What does a catalyst change on the energy diagram, and is it still there at the end?",
      "<b>A lower E<sub>a</sub>, and not used up</b>; &Delta;H is unchanged.", 1)

    Q(T, "People who are lactose intolerant make too little of the enzyme lactase, so lactose from milk is broken down too slowly in the small intestine. How does lactase speed up this breakdown?",
      ["It binds lactose in the right orientation and gives a reaction path with a lower activation energy.",
       "It raises the temperature of the small intestine.",
       "It is used up as it breaks down each lactose molecule.",
       "It changes &Delta;H so the reaction releases more energy."],
      ["Enzymes are biological catalysts: they hold the substrate in the right orientation and lower E<sub>a</sub>.",
       "Enzymes work at body temperature; they lower the energy hill instead of heating the gut.",
       "Like any catalyst, lactase comes out unchanged and can act on many lactose molecules.",
       "A catalyst does not change &Delta;H; only the hill between reactants and products is lower."],
      "Enzymes are catalysts.",
      "Lactase is a catalyst: <b>the right orientation and a lower E<sub>a</sub></b>.", 2)

    Q(T, "The table shows the relative rate of a reaction catalyzed by a human enzyme at several temperatures. Why does the rate fall above 37 °C?",
      ["The enzyme begins to change shape (denature), so it catalyzes the reaction less well.",
       "Higher temperatures always make reactions slower.",
       "Above 37 °C the molecules collide less often.",
       "The activation energy of every reaction rises above 37 °C."],
      ["Enzymes are proteins, and their shape matters; too much heat changes the shape, and the enzyme slows or stops.",
       "Below 37 °C the rate rises with temperature, as for most reactions. The drop above 37 °C comes from the enzyme itself.",
       "Molecules move faster and collide more often as the temperature rises; collisions are not the problem.",
       "E<sub>a</sub> does not jump at 37 °C; the enzyme loses its working shape, so the catalyzed path is lost."],
      "Enzymes are proteins with a working shape.",
      "The rate peaks at 37 °C (1.00), then falls: <b>the enzyme denatures</b>.", 2, 0,
      [{"type": "table", "cap": "Rate of an enzyme-catalyzed reaction", "head": ["Temperature (°C)", "Relative rate"],
        "rows": [["17", "0.28"], ["27", "0.55"], ["37", "1.00"], ["47", "0.46"], ["57", "0.04"]]}])

    Q(T, "Magnesium ribbon reacts with hydrochloric acid: [[Mg(s) + 2 HCl(aq) -> MgCl2(aq) + H2(g)]] Which change would make the reaction faster?",
      ["Cutting the ribbon into small pieces", "Diluting the acid with water", "Cooling the acid in an ice bath", "Using one single thick strip of the same mass"],
      ["Small pieces have more surface area, so more magnesium atoms are exposed to collisions with the acid.",
       "Diluting lowers the concentration of HCl, so there are fewer collisions each second and the reaction slows.",
       "Cooling means fewer collisions, and fewer with at least E<sub>a</sub>, so the reaction slows.",
       "A thick strip has less surface area than thin ribbon, so the reaction slows."],
      "Which change raises the number of effective collisions per second?",
      "More surface area: <b>cutting the ribbon into small pieces</b> speeds the reaction.", 2)

    Q(T, "At the same temperature, reaction A has E<sub>a</sub> = 24 kJ and reaction B has E<sub>a</sub> = 96 kJ. Which statement is correct?",
      ["Reaction A is faster, because a larger fraction of its collisions have at least its activation energy.",
       "Reaction B is faster, because a higher activation energy releases more energy.",
       "They have the same rate, because the temperature is the same.",
       "Reaction B is faster, because its molecules have more energy."],
      ["A lower hill means more collisions have enough energy to get over it.",
       "E<sub>a</sub> is the energy needed to start the reaction, not the energy released; a higher hill makes a reaction slower.",
       "At the same temperature, the reaction with the lower hill has more effective collisions, so it is faster.",
       "At the same temperature the molecules have the same average energy; B needs more of it to react."],
      "Lower hill or higher hill: which one do more collisions get over?",
      "Lower E<sub>a</sub> (24 kJ) &rarr; <b>reaction A is faster</b>.", 2)

    Q(T, "A match does not light while it sits in the box, but it bursts into flame when it is struck against the strip. What does striking it supply?",
      ["Energy from friction, so some collisions reach the activation energy", "A catalyst that is used up as the match burns",
       "Oxygen, which is not otherwise in contact with the match head", "A change in &Delta;H that makes the reaction exothermic"],
      ["Burning is exothermic but still has an activation energy. Friction heats the head so collisions get over the hill, and the heat released keeps the reaction going.",
       "Striking does not add a catalyst; it adds energy.",
       "The match head is already surrounded by air in the box.",
       "Burning is exothermic either way; &Delta;H does not change when you strike the match."],
      "Why does an exothermic reaction not start by itself?",
      "Striking supplies the <b>activation energy</b>.", 1)

    Q(T, "A blood sample is cooled from 37 °C to 27 °C. Using the rule of thumb that many reaction rates about double for every 10 °C rise, about how fast do the sample's enzyme-catalyzed reactions run at 27 °C compared with 37 °C?",
      ["About half as fast", "About twice as fast", "About the same", "About one-tenth as fast"],
      ["27 °C is 10 °C cooler than 37 °C: one halving, the reverse of one doubling.",
       "Cooling slows reactions down; twice as fast would be for 10 °C warmer.",
       "A 10 °C change has a large effect on most reaction rates.",
       "The rule of thumb is a factor of about 2 for each 10 °C, not a factor of 10."],
      "Is the sample warmer or cooler, and by how many 10 °C steps?",
      "One 10 °C step cooler &rarr; <b>about half as fast</b>.", 2)

    # ======================= ch13-dynamic (12) =======================
    T = 'ch13-dynamic'
    Q(T, "For a reaction at chemical equilibrium, how does the rate of the forward reaction compare with the rate of the reverse reaction?",
      ["The two rates are equal, and neither one is zero.", "Both rates are zero, because the reaction has stopped.",
       "The forward rate is larger, because products are still forming.", "The reverse rate is larger, because products are breaking down."],
      ["Equilibrium is dynamic: both reactions keep running at the same rate, so the concentrations stay constant.",
       "Nothing stops at equilibrium; molecules keep reacting in both directions.",
       "Products do keep forming, but they also break down at the same rate, so there is no net change.",
       "Products do keep breaking down, but they also form at the same rate, so there is no net change."],
      "Equal rates, constant amounts.",
      "At equilibrium <b>the rates are equal, and not zero</b>.", 1)

    Q(T, "A sealed flask holds a reaction at a constant temperature. [A] stays at 0.32 M and [B] stays at 0.68 M for hours. A student says the system cannot be at equilibrium because the concentrations are not equal. Which response is correct?",
      ["It is at equilibrium: the concentrations are constant, and they do not have to be equal.",
       "The student is right: at equilibrium the two concentrations must be equal.",
       "It is at equilibrium only because the reactions have stopped.",
       "The student is right: equilibrium is reached only when both reactions stop."],
      ["Constant concentrations show that the forward and reverse rates are equal. The equilibrium amounts depend on the reaction and are usually different.",
       "Equal rates, not equal concentrations, define equilibrium.",
       "The concentrations are constant because the two rates are equal, not because the reactions stopped.",
       "The reactions never stop at equilibrium; they keep running at equal rates."],
      "Is the definition of equilibrium about rates or about amounts?",
      "Constant, not equal: <b>it is at equilibrium</b>.", 2)

    A = [[0, 1.00], [10, 0.70], [20, 0.52], [30, 0.42], [40, 0.37], [50, 0.35], [60, 0.35], [80, 0.35], [100, 0.35]]
    Bp = [[t, round(1 - a, 2)] for t, a in A]
    Q(T, "The graph shows [A] and [B] over time for the reaction A &rlarr; B in a sealed flask that started with only A. When is equilibrium first reached?",
      ["At about 50 s, when both curves become flat", "At about 22 s, where the two curves cross",
       "At 0 s, when the reaction starts", "At 100 s, when the reactions stop"],
      ["Equilibrium is where every line goes flat: from about 50 s on, [A] and [B] stop changing.",
       "The crossing point is where [A] = [B]. Both concentrations are still changing there, and equal concentrations are not the sign of equilibrium.",
       "At 0 s there is no B yet, so the reverse reaction has not started and the forward rate is much faster.",
       "The lines are flat well before 100 s, and the reactions never stop; they continue at equal rates."],
      "Look for the time after which neither line changes.",
      "Both lines are flat from about 50 s on: <b>equilibrium at about 50 s</b>.", 2, 0,
      [{"type": "plot", "x": {"min": 0, "max": 100, "label": "Time (s)"}, "y": {"min": 0, "max": 1.0, "label": "Concentration (M)"}, "grid": True,
        "series": [{"pts": A, "label": "[A]", "labelAt": 7, "dx": 0, "dy": -22}, {"pts": Bp, "label": "[B]", "labelAt": 7, "dx": 0, "dy": -22}]}])

    Q(T, "Phosgene forms in a sealed flask: [[CO(g) + Cl2(g) <=> COCl2(g)]] The [{COCl2}] readings were 0 M at 0 min, 0.0140 M at 5 min, 0.0215 M at 10 min, 0.0238 M at 15 min, 0.0238 M at 20 min, and 0.0238 M at 25 min. By which reading had the system reached equilibrium?",
      ["15 min", "10 min", "25 min", "0 min"],
      ["From this reading on, [{COCl2}] stays at 0.0238 M. A constant concentration means the forward and reverse rates are equal.",
       "[{COCl2}] is still rising after this reading (0.0215 M, then 0.0238 M), so the forward reaction is still faster.",
       "The system was already at equilibrium earlier; this is just a later reading of the same constant value.",
       "At the start there is no product, so the reverse reaction cannot run yet."],
      "Find the first reading after which the value stops changing.",
      "[{COCl2}] is 0.0238 M from 15 min on: <b>by 15 min</b>.", 2)

    Q(T, "A sealed flask starts with only {H2} and {Br2}, which react: [[H2(g) + Br2(g) <=> 2 HBr(g)]] What happens to the forward and reverse rates as the system approaches equilibrium?",
      ["The forward rate falls and the reverse rate rises until they are equal.",
       "The forward rate rises and the reverse rate falls until they are equal.",
       "Both rates fall until they reach zero.", "Both rates stay the same the whole time."],
      ["As {H2} and {Br2} are used up, they collide less often; as HBr builds up, it breaks apart more often. The rates meet at equilibrium.",
       "This has it backward: the forward rate is highest at the start, when the most reactant is present.",
       "The rates become equal, not zero; both reactions keep running.",
       "The forward rate starts high and the reverse rate starts at zero, so they must change to become equal."],
      "At the start there is lots of reactant and no product.",
      "<b>Forward falls, reverse rises, until they are equal.</b>", 2)

    Q(T, "A sealed flask at a fixed temperature starts with only {COCl2} gas. What happens? [[CO(g) + Cl2(g) <=> COCl2(g)]]",
      ["Some {COCl2} breaks down until the forward and reverse rates are equal, giving a mixture of all three gases.",
       "Nothing happens, because equilibrium can be reached only by starting from the reactants.",
       "All of the {COCl2} breaks down into CO and {Cl2}.",
       "It reaches a mixture that has a different K than a mixture made from CO and {Cl2}."],
      ["Equilibrium can be reached from either side. The reverse reaction runs first, and as CO and {Cl2} build up, the forward reaction speeds up to match it.",
       "Equilibrium can be approached from the product side as well.",
       "As soon as CO and {Cl2} form, they react to re-form {COCl2}, so the breakdown is not complete.",
       "At the same temperature, the mixture obeys the same K no matter which side it started from."],
      "Can equilibrium be reached from the product side?",
      "<b>Partial breakdown to an equilibrium mixture of all three gases</b>, with the same K.", 2)

    Q(T, "Why does an open glass of soda go flat instead of reaching an equilibrium between dissolved and gaseous {CO2}? [[CO2(aq) <=> CO2(g)]]",
      ["{CO2} gas escapes from the open glass, so the reverse process cannot keep up; equilibrium needs a closed system.",
       "Gases cannot take part in an equilibrium.",
       "The forward and reverse rates are equal, so all of the {CO2} leaves.",
       "Dissolving {CO2} is not a reversible process."],
      ["In a sealed bottle, {CO2} gas above the soda dissolves back as fast as it leaves. In an open glass the gas drifts away, so the forward process wins.",
       "Gases take part in many equilibria, for example in a sealed soda bottle.",
       "Equal rates would mean no net loss of {CO2}; the soda goes flat because the rates are not equal.",
       "{CO2} dissolves and leaves the liquid in both directions; in a sealed bottle the two processes balance."],
      "What does an equilibrium need that an open glass does not have?",
      "The gas escapes: <b>equilibrium needs a closed system</b>.", 2)

    Q(T, "A chemist swaps a tiny fraction of the CO in an equilibrium mixture for CO made with carbon-14, keeping [CO] the same. [[CO(g) + Cl2(g) <=> COCl2(g)]] Later, carbon-14 shows up in {COCl2} molecules, but no concentration ever changes. What does this show?",
      ["Both reactions are still running at equal rates, so labeled carbon atoms move into {COCl2} and back out.",
       "The reaction had stopped, and adding the labeled CO restarted it in the forward direction only.",
       "The forward rate is faster than the reverse rate at equilibrium.",
       "Carbon-14 is a catalyst that makes new {COCl2}."],
      ["This is the evidence that equilibrium is dynamic: molecules keep forming and breaking apart with no net change.",
       "Nothing restarted; [CO] did not change, and the label spreads only because both reactions were already running.",
       "If the forward rate were faster, [{COCl2}] would rise; it stays constant.",
       "Carbon-14 is just a labeled carbon atom; it reacts like ordinary carbon and is not a catalyst."],
      "How can labeled atoms end up in the product if nothing changes?",
      "The label spreads with no net change: <b>both reactions run at equal rates</b>.", 3)

    Q(T, "Which situation is most like a dynamic equilibrium?",
      ["A parking garage where cars enter and leave at the same rate, so the number inside stays the same",
       "A parking garage that has closed for the night, so no cars move at all",
       "A parking garage that keeps filling up all morning",
       "A parking garage with exactly as many cars inside as on the street outside"],
      ["Movement continues in both directions at equal rates, so the count is constant: dynamic equilibrium.",
       "Nothing moves here; equilibrium is dynamic, not stopped.",
       "The number inside is still changing, so the in and out rates are not equal yet.",
       "Equal amounts are not the point; equal rates in and out are."],
      "Look for equal rates in both directions with a constant amount.",
      "<b>Cars entering and leaving at the same rate</b>.", 1)

    Q(T, "Write the reverse reaction for [[2 H2S(g) <=> 2 H2(g) + S2(g)]]",
      ["[[2 H2(g) + S2(g) -> 2 H2S(g)]]", "[[2 H2S(g) -> 2 H2(g) + S2(g)]]", "[[4 H2(g) + 2 S2(g) -> 4 H2S(g)]]", "[[2 H2(g) + S2(s) -> 2 H2S(g)]]"],
      ["The reverse reaction is the forward reaction read right to left, with the same coefficients and phases.",
       "This is the forward reaction; the reverse starts from the products.",
       "The reverse reaction keeps the same coefficients; doubling them gives a different equation.",
       "Phases do not change when the reaction is reversed; S<sub>2</sub> is a gas here."],
      "Read the equation from right to left.",
      "Reverse: <b>2 H<sub>2</sub>(g) + S<sub>2</sub>(g) &rarr; 2 H<sub>2</sub>S(g)</b>.", 2)

    Q(T, "A student writes, &ldquo;At equilibrium, the forward and reverse rates are both zero.&rdquo; What is wrong with this statement?",
      ["Both reactions keep running; the rates are equal, not zero.", "Nothing; at equilibrium the reactions stop, so both rates are zero.",
       "Only the reverse rate is zero at equilibrium.", "Only the forward rate is zero at equilibrium."],
      ["Equilibrium is dynamic: molecules keep reacting both ways, at the same rate, so there is no net change.",
       "The reactions do not stop; that is why it is called <i>dynamic</i> equilibrium.",
       "If the reverse rate were zero, products would keep piling up, and the concentrations would not be constant.",
       "If the forward rate were zero, reactants would keep piling up, and the concentrations would not be constant."],
      "Why is it called <i>dynamic</i> equilibrium?",
      "<b>The rates are equal, not zero.</b>", 2)

    Q(T, "At equilibrium, a reaction mixture contains far more product than reactant. Which statement is true?",
      ["The forward and reverse rates are equal; the equilibrium mixture of this reaction simply favors products.",
       "The forward rate is faster than the reverse rate, which is why there is more product.",
       "The reverse reaction has stopped, so product builds up.",
       "The system will not be at equilibrium until the amounts become equal."],
      ["At equilibrium the rates are always equal. How much product is present depends on the reaction (its K), not on unequal rates.",
       "A faster forward rate would keep making product, so the concentrations would not be constant.",
       "Both reactions run at equilibrium; neither one stops.",
       "Equilibrium means constant amounts, not equal amounts."],
      "Do unequal amounts mean unequal rates?",
      "<b>Equal rates</b>; this reaction just favors products.", 2)

    # ======================= ch13-k (16) =======================
    T = 'ch13-k'
    Q(T, "Write the equilibrium constant expression for [[2 NO(g) + O2(g) <=> 2 NO2(g)]]",
      [KX([('NO2', 2)], [('NO', 2), ('O2', 1)]), KX([('NO', 2), ('O2', 1)], [('NO2', 2)]),
       "K = 2[NO<sub>2</sub>] / (2[NO][O<sub>2</sub>])", KX([('NO2', 1)], [('NO', 1), ('O2', 1)])],
      ["Products over reactants, each raised to its coefficient: NO<sub>2</sub> squared on top, NO squared and O<sub>2</sub> on the bottom.",
       "This is reactants over products; K always puts the products on top.",
       "Coefficients become exponents, not multipliers.",
       "This leaves out the exponents; the coefficient 2 on NO and on NO<sub>2</sub> must become a power of 2."],
      "Products over reactants; coefficients become exponents.",
      "<b>%s</b>" % KX([('NO2', 2)], [('NO', 2), ('O2', 1)]), 2)

    Q(T, "Ammonia burns in oxygen: [[4 NH3(g) + 3 O2(g) <=> 2 N2(g) + 6 H2O(g)]] Write the equilibrium constant expression.",
      [KX([('N2', 2), ('H2O', 6)], [('NH3', 4), ('O2', 3)]), KX([('N2', 2)], [('NH3', 4), ('O2', 3)]),
       KX([('NH3', 4), ('O2', 3)], [('N2', 2), ('H2O', 6)]), KX([('N2', 1), ('H2O', 1)], [('NH3', 1), ('O2', 1)])],
      ["All four species are gases, so all appear, each raised to its coefficient, with products on top.",
       "Water is left out only when it is a liquid. Here it is H<sub>2</sub>O(g), a gas, so it stays in.",
       "This is reactants over products; K puts the products on top.",
       "Every concentration must be raised to its coefficient: 4, 3, 2, and 6."],
      "Check each phase label before writing K. Is the water a liquid here?",
      "Water is a gas, so it stays: <b>%s</b>" % KX([('N2', 2), ('H2O', 6)], [('NH3', 4), ('O2', 3)]), 3)

    Q(T, "Ammonium carbonate, the solid in old-fashioned smelling salts, breaks down in a sealed jar: [[(NH4)2CO3(s) <=> 2 NH3(g) + CO2(g) + H2O(g)]] Write the equilibrium constant expression.",
      [KX([('NH3', 2), ('CO2', 1), ('H2O', 1)], []), KX([('NH3', 2), ('CO2', 1), ('H2O', 1)], [('(NH4)2CO3', 1)]), KX([('NH3', 2), ('CO2', 1)], []),
       "K = 2[NH<sub>3</sub>][CO<sub>2</sub>][H<sub>2</sub>O]"],
      ["The solid is left out, so only the three gases remain, multiplied together on top, with [NH<sub>3</sub>] squared.",
       "Pure solids are left out of K; (NH<sub>4</sub>)<sub>2</sub>CO<sub>3</sub>(s) does not belong in the denominator.",
       "Water is left out only as a liquid; here it is a gas, so it stays in.",
       "The coefficient 2 on NH<sub>3</sub> becomes an exponent, not a multiplier."],
      "Cross out the (s) species first. Is the water a gas or a liquid?",
      "Leave out the solid: <b>%s</b>" % KX([('NH3', 2), ('CO2', 1), ('H2O', 1)], []), 3)

    Q(T, "Write the equilibrium constant expression for [[2 H2(g) + O2(g) <=> 2 H2O(l)]]",
      [KX([], [('H2', 2), ('O2', 1)]), KX([('H2O', 2)], [('H2', 2), ('O2', 1)]), KX([('H2', 2), ('O2', 1)], []), KX([], [('H2', 1), ('O2', 1)])],
      ["Liquid water is left out, so the numerator is 1, and the reactant gases go on the bottom with their exponents.",
       "H<sub>2</sub>O(l) is a pure liquid, so it is left out of K.",
       "The reactants belong in the denominator; with no product term left, the expression is 1 over the reactants.",
       "The coefficient 2 on H<sub>2</sub> must become an exponent of 2."],
      "Which species are left out? What is left on top when every product is a liquid?",
      "<b>%s</b>" % KX([], [('H2', 2), ('O2', 1)]), 3)

    Q(T, "Tin ore is reduced with hydrogen in a closed furnace: [[SnO2(s) + 2 H2(g) <=> Sn(s) + 2 H2O(g)]] Write the equilibrium constant expression.",
      [KX([('H2O', 2)], [('H2', 2)]), KX([('Sn', 1), ('H2O', 2)], [('SnO2', 1), ('H2', 2)]), KX([('H2', 2)], [('H2O', 2)]), KX([], [('H2', 2)])],
      ["The two solids are left out; the gases remain, each squared, products on top.",
       "Pure solids (SnO<sub>2</sub> and Sn) are left out of K.",
       "This is reactants over products; the water vapor (a product) belongs on top.",
       "This leaves out the water, but H<sub>2</sub>O(g) is a gas, so it stays in."],
      "Cross out the solids, then write products over reactants.",
      "<b>%s</b>" % KX([('H2O', 2)], [('H2', 2)]), 2)

    Q(T, "Which reaction has the equilibrium constant expression K = [{CO2}]?",
      ["[[MgCO3(s) <=> MgO(s) + CO2(g)]]", "[[C(s) + CO2(g) <=> 2 CO(g)]]", "[[CO2(aq) + H2O(l) <=> H2CO3(aq)]]", "[[MgO(s) + CO2(g) <=> MgCO3(s)]]"],
      ["Both magnesium compounds are solids and are left out, so only the product gas remains: K = [CO<sub>2</sub>].",
       "Here K = [CO]<sup>2</sup> / [CO<sub>2</sub>]; carbon is a solid, but CO is a gas product.",
       "Here K = [H<sub>2</sub>CO<sub>3</sub>] / [CO<sub>2</sub>]; only the liquid water is left out.",
       "Here CO<sub>2</sub> is a reactant, so K = 1 / [CO<sub>2</sub>]."],
      "For each reaction, cross out (s) and (l), then write products over reactants.",
      "Only the CO<sub>2</sub> is not a solid, and it is a product: <b>MgCO<sub>3</sub>(s) &rlarr; MgO(s) + CO<sub>2</sub>(g)</b>.", 3)

    Q(T, "Each hemoglobin molecule can carry four {O2} molecules: [[Hb(aq) + 4 O2(aq) <=> Hb(O2)4(aq)]] Write the equilibrium constant expression.",
      [KX([('Hb(O2)4', 1)], [('Hb', 1), ('O2', 4)]), KX([('Hb', 1), ('O2', 4)], [('Hb(O2)4', 1)]),
       "K = [Hb(O<sub>2</sub>)<sub>4</sub>] / (4[O<sub>2</sub>][Hb])",
       KX([('Hb(O2)4', 1)], [('Hb', 1), ('O2', 1)])],
      ["Products over reactants: the loaded hemoglobin on top, and [O<sub>2</sub>] raised to the 4th power on the bottom.",
       "This is reactants over products; the product goes on top.",
       "The coefficient 4 becomes an exponent, not a multiplier.",
       "This leaves out the exponent; the coefficient 4 on O<sub>2</sub> must become a power of 4."],
      "Coefficients become exponents.",
      "<b>%s</b>" % KX([('Hb(O2)4', 1)], [('Hb', 1), ('O2', 4)]), 2)

    cs = {'NOCl': '0.344', 'NO': '0.0613', 'Cl2': '0.0307'}
    n = ns(*cs.values()); k_ = Kv([(cs['NO'], 2), (cs['Cl2'], 1)], [(cs['NOCl'], 2)])
    Q(T, "Nitrosyl chloride breaks down: [[2 NOCl(g) <=> 2 NO(g) + Cl2(g)]] At equilibrium, [NOCl] = %s M, [NO] = %s M, and [{Cl2}] = %s M. Calculate K." % (cs['NOCl'], cs['NO'], cs['Cl2']),
      [num(k_, n), num(1 / k_, n), num(D(cs['NO']) * D(cs['Cl2']) / D(cs['NOCl']), n), num((D(cs['NO']) + D(cs['Cl2'])) / D(cs['NOCl']), n)],
      ["K = [NO]<sup>2</sup>[Cl<sub>2</sub>] / [NOCl]<sup>2</sup> = (%s)<sup>2</sup>(%s) / (%s)<sup>2</sup>; three significant figures." % (cs['NO'], cs['Cl2'], cs['NOCl']),
       "This is reactants over products, the inverse of K.",
       "This leaves out the exponents; [NO] and [NOCl] must each be squared.",
       "This adds the product concentrations; concentrations in K are multiplied, and each is raised to its coefficient."],
      "Write K first: products over reactants, coefficients as exponents.",
      "K = (%s)<sup>2</sup>(%s) / (%s)<sup>2</sup> = <b>%s</b>. K &lt; 1, so reactants are favored." % (cs['NO'], cs['Cl2'], cs['NOCl'], num(k_, n)), 3, 1)

    cs = {'H2': '0.0269', 'Br2': '0.0398', 'HBr': '0.715'}
    n = ns(*cs.values()); k_ = Kv([(cs['HBr'], 2)], [(cs['H2'], 1), (cs['Br2'], 1)])
    Q(T, "Use the table of equilibrium concentrations to calculate K for [[H2(g) + Br2(g) <=> 2 HBr(g)]]",
      [num(k_, n), num(1 / k_, n), num(D(cs['HBr']) / (D(cs['H2']) * D(cs['Br2'])), n), num(2 * D(cs['HBr']) / (D(cs['H2']) * D(cs['Br2'])), n)],
      ["K = [HBr]<sup>2</sup> / ([H<sub>2</sub>][Br<sub>2</sub>]) = (%s)<sup>2</sup> / [(%s)(%s)]; three significant figures." % (cs['HBr'], cs['H2'], cs['Br2']),
       "This is reactants over products, the inverse of K.",
       "This forgets to square [HBr]; its coefficient is 2.",
       "This multiplies [HBr] by its coefficient; coefficients become exponents, not multipliers."],
      "Square the HBr term, then divide by the product of the reactant terms.",
      "K = (%s)<sup>2</sup> / [(%s)(%s)] = <b>%s</b>. K &gt; 1, so HBr is favored." % (cs['HBr'], cs['H2'], cs['Br2'], num(k_, n)), 2, 1,
      [{"type": "table", "cap": "Equilibrium concentrations", "head": ["Species", "Concentration (M)"],
        "rows": [["{H2}", cs['H2']], ["{Br2}", cs['Br2']], ["HBr", cs['HBr']]]}])

    cs = {'BrCl': '0.0846', 'Br2': '0.0213', 'Cl2': '0.0220'}
    n = ns(*cs.values()); k_ = Kv([(cs['Br2'], 1), (cs['Cl2'], 1)], [(cs['BrCl'], 2)])
    Q(T, "Bromine monochloride partly breaks down: [[2 BrCl(g) <=> Br2(g) + Cl2(g)]] At equilibrium, [BrCl] = %s M, [{Br2}] = %s M, and [{Cl2}] = %s M. Calculate K." % (cs['BrCl'], cs['Br2'], cs['Cl2']),
      [num(k_, n), num(1 / k_, n), num(D(cs['Br2']) * D(cs['Cl2']) / D(cs['BrCl']), n), num((D(cs['Br2']) + D(cs['Cl2'])) / D(cs['BrCl']), n)],
      ["K = [Br<sub>2</sub>][Cl<sub>2</sub>] / [BrCl]<sup>2</sup> = (%s)(%s) / (%s)<sup>2</sup>; three significant figures." % (cs['Br2'], cs['Cl2'], cs['BrCl']),
       "This is reactants over products, the inverse of K.",
       "This leaves out the exponent; [BrCl] must be squared.",
       "This adds the product concentrations; concentrations in K are multiplied."],
      "Square the term whose coefficient is 2.",
      "K = (%s)(%s) / (%s)<sup>2</sup> = <b>%s</b>. K &lt; 1, so BrCl is favored." % (cs['Br2'], cs['Cl2'], cs['BrCl'], num(k_, n)), 3, 1)

    cs = {'CO': '0.0155', 'Cl2': '0.0241', 'COCl2': '0.145'}
    n = ns(*cs.values()); k_ = Kv([(cs['COCl2'], 1)], [(cs['CO'], 1), (cs['Cl2'], 1)])
    Q(T, "An equilibrium mixture for [[CO(g) + Cl2(g) <=> COCl2(g)]] contains [CO] = %s M, [{Cl2}] = %s M, and [{COCl2}] = %s M. Calculate K." % (cs['CO'], cs['Cl2'], cs['COCl2']),
      [num(k_, n), num(1 / k_, n), num(D(cs['COCl2']) / (D(cs['CO']) + D(cs['Cl2'])), n), num(D(cs['COCl2']) * D(cs['CO']) * D(cs['Cl2']), n)],
      ["K = [COCl<sub>2</sub>] / ([CO][Cl<sub>2</sub>]) = %s / [(%s)(%s)]; three significant figures." % (cs['COCl2'], cs['CO'], cs['Cl2']),
       "This is reactants over products, the inverse of K.",
       "This adds the reactant concentrations; they are multiplied in K.",
       "This multiplies all three concentrations; the reactant terms belong in the denominator."],
      "Products over reactants, multiplied, not added.",
      "K = %s / [(%s)(%s)] = <b>%s</b>. K &gt; 1, so COCl<sub>2</sub> is favored." % (cs['COCl2'], cs['CO'], cs['Cl2'], num(k_, n)), 2, 1)

    cs = {'CO2': '0.0371', 'CO': '0.115'}
    n = ns(*cs.values()); k_ = Kv([(cs['CO'], 2)], [(cs['CO2'], 1)])
    Q(T, "Hot charcoal reacts with carbon dioxide in a closed vessel: [[C(s) + CO2(g) <=> 2 CO(g)]] At equilibrium, [{CO2}] = %s M and [CO] = %s M. Calculate K." % (cs['CO2'], cs['CO']),
      [num(k_, n), num(1 / k_, n), num(D(cs['CO']) / D(cs['CO2']), n), num(2 * D(cs['CO']) / D(cs['CO2']), n)],
      ["Carbon is a solid and is left out: K = [CO]<sup>2</sup> / [CO<sub>2</sub>] = (%s)<sup>2</sup> / %s; three significant figures." % (cs['CO'], cs['CO2']),
       "This is reactants over products, the inverse of K.",
       "This forgets to square [CO]; its coefficient is 2.",
       "This multiplies [CO] by 2; the coefficient becomes an exponent, not a multiplier."],
      "Leave out the solid, then square the CO term.",
      "K = (%s)<sup>2</sup> / %s = <b>%s</b>." % (cs['CO'], cs['CO2'], num(k_, n)), 3, 1)

    k0 = '0.0384'
    Q(T, "At a certain temperature, K = %s for [[2 NO2(g) <=> 2 NO(g) + O2(g)]] What is K for the reverse reaction, [[2 NO(g) + O2(g) <=> 2 NO2(g)]] at the same temperature?" % k0,
      [num(1 / D(k0), 3), k0, '-' + k0, num(1 - D(k0), 3)],
      ["The K for a reaction written in reverse is the reciprocal: 1 / %s." % k0,
       "Reversing the reaction flips products and reactants, so K becomes 1/K; it does not stay the same.",
       "K is never negative. (Reversing a reaction flips the sign of &Delta;H, not of K.)",
       "The reverse K is the reciprocal (1 divided by K), not 1 minus K."],
      "Products and reactants trade places. What does that do to the fraction?",
      "K<sub>reverse</sub> = 1 / %s = <b>%s</b>." % (k0, num(1 / D(k0), 3)), 2, 1)

    Q(T, "At 25 °C, a reaction has K = 3.7 &times; 10<sup>8</sup>. What does the equilibrium mixture contain?",
      ["Mostly products, with very little reactant left", "Mostly reactants, with very little product formed",
       "Sizable amounts of both reactants and products", "Equal concentrations of reactants and products"],
      ["K &gt; 1, and very large (&#8811; 1): products are favored, and the reaction goes nearly to completion.",
       "That describes K &lt; 1, such as 10<sup>&minus;8</sup>; this K is far greater than 1.",
       "That describes K close to 1 (roughly 0.1 to 10).",
       "K does not tell you the concentrations are equal; a K this large means far more product than reactant."],
      "Compare K with 1.",
      "K &#8811; 1: <b>mostly products</b>.", 1)

    Q(T, "The burning of glucose, [[C6H12O6(s) + 6 O2(g) <=> 6 CO2(g) + 6 H2O(l)]] has an enormous K at room temperature, yet sugar sits in a bowl in air for years without burning. How can both be true?",
      ["K tells how far a reaction goes, not how fast; the activation energy is high, so at room temperature the reaction is extremely slow.",
       "A large K means a fast reaction, so the sugar must be burning without anyone noticing.",
       "Air does not contain enough oxygen for the reaction to start.",
       "A large K means the mixture is already at equilibrium, so nothing can happen."],
      ["K describes the equilibrium mixture; the rate depends on E<sub>a</sub> and collisions (Section 13.1). In your cells, enzymes provide a low-E<sub>a</sub> path.",
       "A large K is not a fast rate; if the sugar were burning, the bowl would be empty.",
       "Air is about 21% oxygen, plenty for burning; the barrier is the activation energy.",
       "Sugar and oxygen are far from equilibrium; they would form CO<sub>2</sub> and water if the reaction could get going."],
      "Does K measure how far or how fast?",
      "<b>Large K = how far, not how fast</b>; a high E<sub>a</sub> keeps the reaction slow.", 2)

    Q(T, "Four reactions have these K values at the same temperature. Which equilibrium mixture contains the largest share of reactants?",
      ["K = 4.3 &times; 10<sup>&minus;7</sup>", "K = 0.019", "K = 1.2", "K = 6.8 &times; 10<sup>5</sup>"],
      ["This is the smallest K, far below 1, so reactants are favored most strongly.",
       "This K is small, but 0.019 is much larger than 4.3 &times; 10<sup>&minus;7</sup>, so it has relatively more product.",
       "K close to 1 means sizable amounts of both reactants and products.",
       "K &gt; 1 favors products, the opposite of what is asked."],
      "The smaller the K, the more the mixture favors reactants.",
      "Smallest K: <b>K = 4.3 &times; 10<sup>&minus;7</sup></b>.", 2)

    # ======================= ch13-lechat (26) =======================
    T = 'ch13-lechat'
    E1 = "[[2 NO(g) + O2(g) <=> 2 NO2(g)]]"
    Q(T, "More {O2} is added to this mixture at equilibrium: " + E1 + " Which way does the equilibrium shift?",
      ["Shifts right, away from the added {O2}", "Shifts left, toward the added {O2}", "No shift, because K does not change", "Shifts right, and K increases"],
      ["Add &rarr; away: {O2} is a reactant, so the forward reaction speeds up for a while and uses some of it.",
       "Adding a substance pushes the system away from it, not toward it.",
       "K stays the same, but the concentrations no longer fit K, so the system shifts until they do.",
       "The shift is to the right, but only a temperature change alters K; adding {O2} does not."],
      "Add &rarr; away, take &rarr; toward.",
      "{O2} is a reactant: <b>shifts right</b>, away from it. K is unchanged.", 1)

    Q(T, "In a hydrogen plant, {CO2} is removed from this equilibrium mixture by absorbing it into a solution: [[CO(g) + H2O(g) <=> CO2(g) + H2(g)]] Which way does the equilibrium shift?",
      ["Shifts right, toward the removed {CO2}", "Shifts left, away from the removed {CO2}", "No shift, because {CO2} is a product", "Shifts left, and K decreases"],
      ["Take &rarr; toward: with less {CO2}, the reverse reaction slows, so the forward reaction wins and more {H2} forms.",
       "Removing a substance pulls the system toward it, to replace some of what was taken.",
       "Changing the amount of a product shifts an equilibrium just as changing a reactant does.",
       "The shift is to the right, and K does not change unless the temperature changes."],
      "Take &rarr; toward.",
      "{CO2} is removed: <b>shifts right</b>, toward it, making more {H2}.", 2)

    E3 = "[[4 NH3(g) + 5 O2(g) <=> 4 NO(g) + 6 H2O(g)]]"
    Q(T, "Extra steam, {H2O}(g), is added to this mixture at equilibrium: " + E3 + " What happens?",
      ["Shifts left, and [{NH3}] increases", "Shifts right, and [{NH3}] decreases", "No shift, because water is never part of K", "Shifts left, and [{NH3}] decreases"],
      ["Add &rarr; away: steam is a product, so the system shifts toward the reactants, and more {NH3} forms.",
       "Adding a product pushes the system away from the products, to the left.",
       "Water is left out of K only as a pure liquid; here it is a gas, so adding it causes a shift.",
       "A shift to the left makes reactants, so [{NH3}] goes up, not down."],
      "Is the water a gas or a liquid here? Which side is it on?",
      "Steam is a gaseous product: <b>shifts left, and [{NH3}] increases</b>.", 2)

    E4 = "[[CO(g) + Cl2(g) <=> COCl2(g)]]"
    Q(T, "Some {Cl2} is removed from this mixture at equilibrium: " + E4 + " What happens to [{COCl2}]?",
      ["Shifts left, and [{COCl2}] decreases", "Shifts right, and [{COCl2}] increases", "No shift, and [{COCl2}] does not change", "Shifts left, and [{COCl2}] increases"],
      ["Take &rarr; toward: removing the reactant {Cl2} shifts the system left, so some {COCl2} breaks down.",
       "Removing a substance pulls the system toward it, not away from it.",
       "Removing a reactant upsets the ratio in K, so the system must shift.",
       "A shift to the left uses up the product, so [{COCl2}] goes down."],
      "Take &rarr; toward. Which side is {Cl2} on?",
      "<b>Shifts left; [{COCl2}] decreases.</b>", 2)

    Q(T, "Some {NO2} is added to this mixture at equilibrium: " + E1 + " Once the new equilibrium is reached, what has happened to [{O2}]?",
      ["[{O2}] increases", "[{O2}] decreases", "[{O2}] does not change", "[{O2}] increases, and K decreases"],
      ["Adding the product {NO2} shifts the system left, which makes more NO and {O2}.",
       "This would happen after a shift to the right; adding a product shifts the system left.",
       "The shift to the left changes every concentration, including [{O2}].",
       "The concentration change is right, but K changes only with temperature."],
      "First find the direction of the shift, then follow it to {O2}.",
      "Add &rarr; away: shift left, so <b>[{O2}] increases</b>.", 3)

    E6 = "[[C(s) + CO2(g) <=> 2 CO(g)]]"
    Q(T, "More powdered carbon is added to this mixture at equilibrium: " + E6 + " Which way does the equilibrium shift?",
      ["No shift, because a pure solid does not appear in K", "Shifts right, away from the added carbon",
       "Shifts left, toward the added carbon", "Shifts right, and K increases"],
      ["K = [CO]<sup>2</sup> / [CO<sub>2</sub>] does not include C(s), so adding more of the solid changes nothing in K.",
       "Add &rarr; away applies to gases and dissolved species; a pure solid has no concentration term in K.",
       "Adding a substance never shifts the system toward it, and a solid causes no shift at all.",
       "Adding a solid neither shifts the system nor changes K."],
      "Is C(s) part of the K expression?",
      "Solid carbon is not in K: <b>no shift</b>.", 2)

    E7 = "[[Cu(H2O)4^2+(aq) + 4 NH3(aq) <=> Cu(NH3)4^2+(aq) + 4 H2O(l)]]"
    Q(T, "In this equilibrium, {Cu(H2O)4^2+} is pale blue and {Cu(NH3)4^2+} is deep blue: " + E7 + " More ammonia solution is added, raising [{NH3}]. What happens?",
      ["Shifts right, and the solution turns a deeper blue", "Shifts left, and the solution turns paler blue",
       "No shift, because water is a product", "Shifts right, and the solution turns paler blue"],
      ["Add &rarr; away: {NH3} is a reactant, so more deep blue {Cu(NH3)4^2+} forms.",
       "Adding a reactant pushes the system to the right, not the left.",
       "Liquid water is left out of K, but {NH3} is in it, so adding {NH3} causes a shift.",
       "A shift to the right makes the deep blue product, not the pale blue reactant."],
      "Which side is {NH3} on, and which color is on the side the system shifts toward?",
      "Add {NH3} &rarr; <b>shifts right, deeper blue</b>.", 2)

    Q(T, "For this reaction, &Delta;H = -41.2 kJ: [[CO(g) + H2O(g) <=> CO2(g) + H2(g)]] The mixture is heated. Which describes the shift and K?",
      ["Shifts left, and K decreases", "Shifts right, and K increases", "Shifts left, and K does not change", "No shift, and K decreases"],
      ["&Delta;H is negative, so heat is a product. Adding heat shifts the system left, away from it; a temperature change also changes K, and here K gets smaller.",
       "This treats heat as a reactant. For an exothermic reaction, heat is a product.",
       "The direction is right, but temperature is the one stress that does change K.",
       "Adding heat is a stress, so the system shifts; and when K changes, the mixture must shift to match it."],
      "Write heat into the equation on the correct side first.",
      "Exothermic: heat is a product. Heating &rarr; <b>shifts left, K decreases</b>.", 2)

    Q(T, "For this reaction, &Delta;H = +172.5 kJ: " + E6 + " The temperature is lowered. Which describes the shift and K?",
      ["Shifts left, and K decreases", "Shifts right, and K increases", "Shifts left, and K does not change", "Shifts right, and K decreases"],
      ["&Delta;H is positive, so heat is a reactant. Cooling removes it, and take &rarr; toward shifts the system left; K gets smaller.",
       "Cooling removes heat, a reactant here, so the system shifts toward the reactants, not the products.",
       "The direction is right, but a temperature change always changes K.",
       "For an endothermic reaction, cooling shifts the system left, not right."],
      "Endothermic: heat is a reactant. Is heat being added or removed?",
      "Heat is a reactant; cooling &rarr; <b>shifts left, K decreases</b>.", 2)

    Q(T, "A sealed glass vial holds liquid bromine and its brown vapor at equilibrium. Evaporating bromine is endothermic: [[Br2(l) <=> Br2(g)]] The vial is placed in warm water. What happens?",
      ["Shifts right, and K increases", "Shifts left, and K decreases", "No shift, because a pure liquid is left out of K", "Shifts right, and K does not change"],
      ["Heat is a reactant for an endothermic change. Adding heat shifts the system right, so more brown vapor forms, and K (= [Br<sub>2</sub>(g)]) increases.",
       "This treats heat as a product. For an endothermic change, heat is a reactant.",
       "The liquid is left out of K, but the vapor is in it, and a temperature change always shifts the equilibrium and changes K.",
       "The direction is right, but a temperature change always changes K."],
      "Write heat on the reactant side, then apply add &rarr; away.",
      "Heat is a reactant: <b>shifts right, K increases</b> (more brown vapor).", 2)

    Q(T, "For [[CO(g) + H2O(g) <=> CO2(g) + H2(g)]] &Delta;H = -41.2 kJ. Which change alters the value of K?",
      ["Raising the temperature", "Adding more CO", "Decreasing the volume", "Adding a catalyst"],
      ["Temperature is the only stress that changes K. Here, heating lowers K because the reaction is exothermic.",
       "Adding CO shifts the system right until the ratio equals the same K again.",
       "Both sides have 2 moles of gas, so a volume change causes no shift, and K does not change.",
       "A catalyst speeds both directions equally; it changes neither the equilibrium amounts nor K."],
      "Only one kind of stress gives a reaction a new K.",
      "Only temperature changes K: <b>raising the temperature</b>.", 2)

    Q(T, "For [[H2O(l) <=> H2O(g)]] &Delta;H = +44.0 kJ. How is heat written into this equation?",
      ["[[heat + H2O(l) <=> H2O(g)]], with heat as a reactant", "[[H2O(l) <=> H2O(g) + heat]], with heat as a product",
       "Heat appears on both sides, because &Delta;H is the same in both directions", "No heat term, because only exothermic changes have one"],
      ["&Delta;H is positive (endothermic): evaporation absorbs heat, so heat is written as a reactant on the left.",
       "Heat is a product only when &Delta;H is negative (exothermic), as in condensation.",
       "Heat goes on one side only; reversing a change flips the sign of &Delta;H.",
       "Endothermic changes have a heat term too, on the reactant side."],
      "Positive &Delta;H: is heat absorbed or released?",
      "Endothermic: <b>heat is a reactant</b>.", 1)

    Q(T, "The volume of the container is decreased (the pressure is increased) for this mixture at equilibrium: " + E3 + " Which way does the equilibrium shift?",
      ["Shifts left, toward the side with fewer moles of gas", "Shifts right, toward the side with more moles of gas",
       "No shift, because the total number of atoms is the same on both sides", "Shifts left, and K increases"],
      ["Left: 4 + 5 = 9 mol of gas; right: 4 + 6 = 10 mol of gas. A smaller volume shifts the system toward fewer moles of gas, the left.",
       "A smaller volume (higher pressure) shifts the system toward fewer gas particles, not more.",
       "Atoms always balance; for pressure, count the moles of gas on each side.",
       "The direction is right, but only temperature changes K."],
      "Count the coefficients of the gases on each side.",
      "9 mol vs 10 mol of gas: <b>shifts left</b>.", 2)

    Q(T, "The volume of the container is decreased for this mixture at equilibrium: [[H2(g) + Br2(g) <=> 2 HBr(g)]] Which way does the equilibrium shift?",
      ["No shift, because both sides have 2 moles of gas", "Shifts right, toward HBr", "Shifts left, toward {H2} and {Br2}", "Shifts right, and K increases"],
      ["1 + 1 = 2 mol of gas on the left and 2 mol on the right, so neither direction lowers the pressure.",
       "A shift happens only when one side has fewer moles of gas; here both sides have 2.",
       "Both sides have the same number of gas moles, so there is no side with fewer moles to shift toward.",
       "There is no shift, and a volume change never changes K."],
      "Count moles of gas on each side.",
      "2 mol = 2 mol of gas: <b>no shift</b>.", 2)

    Q(T, "The volume of the container is increased for this mixture at equilibrium: " + E1 + " Which way does the equilibrium shift?",
      ["Shifts left, toward the side with more moles of gas", "Shifts right, toward the side with fewer moles of gas",
       "No shift, because only temperature changes an equilibrium", "Shifts right, and K decreases"],
      ["Left: 2 + 1 = 3 mol of gas; right: 2 mol. A larger volume (lower pressure) shifts the system toward more moles of gas, the left.",
       "That is the response to a smaller volume. A larger volume shifts the system toward more moles of gas.",
       "Volume changes shift gas equilibria; temperature is just the only stress that changes K.",
       "A larger volume shifts the system left, and K does not change."],
      "Lower pressure: toward more or fewer gas particles?",
      "3 mol vs 2 mol of gas: <b>shifts left</b>.", 2)

    E16 = "[[2 NaHCO3(s) <=> Na2CO3(s) + H2O(g) + CO2(g)]]"
    Q(T, "The volume of the sealed container is decreased for this mixture at equilibrium: " + E16 + " Which way does the equilibrium shift?",
      ["Shifts left, because the right side has 2 moles of gas and the left side has none",
       "Shifts right, because the right side has more moles of substances in all",
       "No shift, because the reaction contains solids", "Shifts right, toward the side with more moles of gas"],
      ["Count gases only: 0 mol on the left, 1 + 1 = 2 mol on the right. A smaller volume shifts the system toward fewer moles of gas.",
       "Solids are not counted in pressure shifts, just as they are left out of K.",
       "The solids are not counted, but the two gases on the right still respond to a volume change.",
       "A smaller volume shifts the system toward fewer moles of gas, not more."],
      "Cross out the solids, then count moles of gas on each side.",
      "0 vs 2 mol of gas: <b>shifts left</b>.", 3)

    Q(T, "Argon gas is added to this mixture at equilibrium in a rigid container (constant volume): " + E4 + " What happens?",
      ["No shift, because the concentrations of CO, {Cl2}, and {COCl2} do not change", "Shifts right, because the total pressure increased",
       "Shifts left, because argon reacts with {Cl2}", "Shifts right, toward the side with fewer moles of gas"],
      ["Argon is inert and the volume is fixed, so every reacting gas keeps the same concentration; nothing in K changes.",
       "The total pressure rises, but the concentrations of the reacting gases do not, so there is no stress on the equilibrium.",
       "Argon is a noble gas; it does not react.",
       "That would happen if the volume were decreased; here the volume stays the same."],
      "Does adding an inert gas at constant volume change any concentration in K?",
      "Inert gas, constant volume: <b>no shift</b>.", 2)

    Q(T, "A chemist adds a platinum catalyst to a sealed vessel in which this mixture is at equilibrium: " + E3 + " What happens to the equilibrium?",
      ["No shift: [NO] does not change, though a new mixture would reach equilibrium sooner", "Shifts right, and [NO] increases",
       "Shifts left, and [NO] decreases", "No shift, but K increases"],
      ["A catalyst lowers E<sub>a</sub> for the forward and reverse reactions equally, so it speeds both and leaves the equilibrium amounts and K the same.",
       "A catalyst does not favor products; it speeds up the reverse reaction just as much as the forward one.",
       "A catalyst does not favor reactants either; the equilibrium amounts stay the same.",
       "A catalyst never changes K; only temperature does."],
      "A catalyst speeds up which direction?",
      "<b>No shift</b>; a catalyst only gets a system to equilibrium faster.", 2)

    EH = "[[Hb(aq) + O2(aq) <=> HbO2(aq)]]"
    Q(T, "In the alveoli of the lungs, the {O2} concentration is high. What happens to this equilibrium in the red blood cells passing through the lung capillaries? " + EH,
      ["Shifts right, and hemoglobin loads {O2} as {HbO2}", "Shifts left, and {HbO2} releases {O2} in the lungs",
       "No shift, because hemoglobin is a catalyst", "Shifts right, and [Hb] increases"],
      ["Add &rarr; away: the high {O2} shifts the system right, so hemoglobin picks up oxygen to carry to the tissues.",
       "Unloading happens in the tissues, where {O2} is low; in the lungs, {O2} is high.",
       "Hemoglobin is a reactant that binds {O2}, not a catalyst.",
       "A shift to the right uses up free Hb, so [Hb] goes down."],
      "Is {O2} high or low in the lungs?",
      "{O2} is high: <b>shifts right</b>, and hemoglobin loads {O2}.", 2)

    Q(T, "A family runs a gasoline generator in a closed garage, and the carbon monoxide in the air rises. What happens to this equilibrium in their blood? [[Hb(aq) + CO(aq) <=> HbCO(aq)]]",
      ["Shifts right, and [Hb] decreases, leaving less hemoglobin free to carry {O2}", "Shifts left, and [HbCO] decreases",
       "No shift, because CO does not bind hemoglobin", "Shifts right, and K increases"],
      ["Add &rarr; away: more CO shifts the system right, so more hemoglobin is tied up as HbCO and cannot carry oxygen.",
       "Adding CO, a reactant, pushes the system right, toward more HbCO.",
       "CO binds hemoglobin at the oxygen site, more than 200 times more tightly than {O2}.",
       "The shift is right, but K does not change; only temperature changes K."],
      "Is CO a reactant or a product here?",
      "Add CO &rarr; <b>shifts right</b>; less free Hb is left for {O2}.", 2)

    EC = "[[CO2(aq) + H2O(l) <=> H2CO3(aq) <=> H^+(aq) + HCO3^-(aq)]]"
    Q(T, "During a panic attack, a patient breathes much faster than her body needs and blows off {CO2}. What happens to this equilibrium in her blood? " + EC,
      ["Shifts left, [{H^+}] decreases, and blood pH rises", "Shifts right, [{H^+}] increases, and blood pH falls",
       "Shifts left, [{H^+}] decreases, and blood pH falls", "No shift, because the kidneys keep [{H^+}] fixed"],
      ["Take &rarr; toward: removing {CO2} shifts the system left. {H^+} combines with {HCO3^-}, so [{H^+}] drops and the pH rises (respiratory alkalosis).",
       "This happens when {CO2} builds up, as in hypoventilation; fast breathing removes {CO2}.",
       "Less {H^+} means a higher pH, not a lower one.",
       "The kidneys respond only slowly, over hours to days; the fast change comes from the shift."],
      "Fast breathing removes {CO2}. Which way does take &rarr; toward point?",
      "Remove {CO2} &rarr; <b>shifts left, less {H^+}, pH rises</b>.", 2)

    Q(T, "A patient with severe COPD (chronic obstructive pulmonary disease) cannot breathe out {CO2} fast enough, and his PaCO<sub>2</sub> rises. What happens to this equilibrium in his blood? " + EC,
      ["Shifts right, [{H^+}] increases, and blood pH falls", "Shifts left, [{H^+}] decreases, and blood pH rises",
       "Shifts right, [{H^+}] increases, and blood pH rises", "No shift, because {CO2} is a gas"],
      ["Add &rarr; away: built-up {CO2} shifts the system right, making more {H^+}, so the pH falls (respiratory acidosis).",
       "This is what fast breathing does; here {CO2} is building up, not being removed.",
       "More {H^+} makes blood more acidic, which means a lower pH.",
       "{CO2} is dissolved in the blood here, and it is part of the equilibrium."],
      "Is {CO2} being added or removed?",
      "{CO2} builds up &rarr; <b>shifts right, more {H^+}, pH falls</b>.", 2)

    EE = "[[Ca5(PO4)3OH(s) <=> 5 Ca^2+(aq) + 3 PO4^3-(aq) + OH^-(aq)]]"
    Q(T, "A toothpaste supplies extra {Ca^2+} and phosphate ions to the tooth surface. What happens to the enamel equilibrium? " + EE,
      ["Shifts left, and enamel re-forms (remineralization)", "Shifts right, and enamel dissolves (demineralization)",
       "No shift, because enamel is a solid", "Shifts right, and [{OH^-}] increases"],
      ["Add &rarr; away: {Ca^2+} and {PO4^3-} are products, so adding them shifts the system left, toward solid hydroxyapatite.",
       "Adding products pushes the system away from them, toward the solid.",
       "The solid is left out of K, but the ions are in it, and adding ions does cause a shift.",
       "Adding products shifts the system left, which uses up {OH^-} rather than making more."],
      "Which side are the ions on?",
      "Add products &rarr; <b>shifts left: remineralization</b>.", 2)

    Q(T, "A dental hygienist applies fluoride varnish, which raises [{F^-}] at the tooth surface. What happens to this equilibrium? [[Ca5(PO4)3OH(s) + F^-(aq) <=> Ca5(PO4)3F(s) + OH^-(aq)]]",
      ["Shifts right, and more acid-resistant fluorapatite forms", "Shifts left, and more hydroxyapatite forms",
       "No shift, because both minerals are solids", "Shifts right, and [{OH^-}] decreases"],
      ["Add &rarr; away: {F^-} is a reactant, so the system shifts right, replacing {OH^-} in the mineral to form fluorapatite.",
       "Adding a reactant pushes the system to the right, not the left.",
       "The solids are left out of K, but {F^-} and {OH^-} are in it, so adding {F^-} causes a shift.",
       "A shift to the right makes more {OH^-}, so [{OH^-}] goes up."],
      "Is {F^-} a reactant or a product?",
      "Add {F^-} &rarr; <b>shifts right: more fluorapatite</b>.", 2)

    Q(T, "Which change shifts this enamel equilibrium toward demineralization (dissolving)? " + EE,
      ["Acid from plaque bacteria removing {OH^-} ions", "Saliva adding {Ca^2+} ions", "Saliva adding phosphate ions",
       "A remineralizing paste adding {Ca^2+} and phosphate ions"],
      ["Take &rarr; toward: {H^+} from the acid reacts with {OH^-}, removing a product, so the system shifts right and enamel dissolves.",
       "Adding {Ca^2+}, a product, shifts the system left, toward remineralization.",
       "Adding phosphate, a product, shifts the system left, toward remineralization.",
       "Adding products shifts the system left, which rebuilds enamel."],
      "Dissolving is the forward direction. Which change pulls the system to the right?",
      "Removing a product shifts right: <b>acid removing {OH^-}</b>.", 3)

    Q(T, "Ammonia plants run the exothermic Haber process, [[N2(g) + 3 H2(g) <=> 2 NH3(g)]] at about 400&ndash;450 °C, even though a lower temperature would give more {NH3} at equilibrium. Why?",
      ["At a low temperature the reaction is far too slow, so a higher temperature is used to make {NH3} at a useful rate",
       "A low temperature would lower K and give less {NH3}",
       "A high temperature shifts the equilibrium toward {NH3}",
       "A high temperature lets the iron catalyst shift the equilibrium toward {NH3}"],
      ["Cooling an exothermic reaction favors products, but collisions are slower and fewer reach E<sub>a</sub>. Plants trade some yield for a useful rate.",
       "For an exothermic reaction, lowering the temperature raises K and favors {NH3}.",
       "Heat is a product of this reaction, so raising the temperature shifts it left, away from {NH3}.",
       "A catalyst never shifts an equilibrium; it helps the plant reach equilibrium faster."],
      "Low temperature helps the yield. What does it do to the rate?",
      "Equilibrium favors low T, but <b>the rate would be far too slow</b>; plants compromise.", 3)


if __name__ == '__main__':
    build()
    dump(sys.argv[1])
