#!/usr/bin/env python3
"""Builds bank/ch13_adapt.json (Chapter 13 ADAPT homework-only items, text only; 42 items, none repeated from
bank/ch13.json).
usage: python3 tools/gen_adapt_ch13.py bank/ch13_adapt.json
Same conventions, helpers and markup as tools/gen_bank_ch13.py (imported from it): effective collisions; Ea = top -
reactants, dH = products - reactants; equal rates and constant concentrations at equilibrium; K = products over
reactants with coefficients as exponents, (s) and (l) left out, reverse K = 1/K; K > 1 favors products, K < 1
reactants, K near 1 (about 0.1 to 10) both; add -> away, take -> toward; heat as a reactant or product; only
temperature changes K; volume by moles of gas; catalysts and inert gases no shift. y[0] begins "Correct: ".
Every item is rechecked by tools/check_bank_ch13.py."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bank_ch13 import *
import gen_bank_ch13 as G
G.CFG.update(prefix='c13-h%02d', adapt=True)


def build_hw():
    # ======================= ch13-rates (9) =======================
    T = 'ch13-rates'
    Q(T, "Two molecules collide with exactly the right orientation, but they bounce apart unchanged. What is the most likely reason?",
      ["The collision had less than the activation energy.", "The activation energy was too low.",
       "The molecules were at equilibrium, so they could not react.", "Molecules with the right orientation never react."],
      ["Orientation is only one requirement; the collision must also have at least E<sub>a</sub> to break the bonds that need to break.",
       "A low activation energy makes reacting easier; the problem is that this collision did not reach it.",
       "Molecules keep reacting at equilibrium; the reverse reaction keeps pace with the forward one.",
       "The right orientation is required for reaction; together with enough energy, it gives an effective collision."],
      "Orientation was right. What is the other requirement?",
      "Right orientation but no reaction: <b>not enough energy</b>.", 1)

    r, top, p = 64, 151, 97
    Q(T, "A reaction's energy diagram shows the reactants at %d kJ, the products at %d kJ, and the peak of the hill at %d kJ. What is &Delta;H, and is the reaction exothermic or endothermic?" % (r, p, top),
      ["+%d kJ, endothermic" % (p - r), "-%d kJ, exothermic" % (p - r), "+%d kJ, endothermic" % (top - r), "-%d kJ, exothermic" % (top - p)],
      ["&Delta;H = products &minus; reactants = %d &minus; %d = +%d kJ. The products are higher in energy, so heat is absorbed." % (p, r, p - r),
       "This is reactants &minus; products. &Delta;H is products &minus; reactants, which is positive here.",
       "This is the activation energy (%d &minus; %d), the height of the hill, not &Delta;H." % (top, r),
       "This measures from the peak of the hill down to the products; &Delta;H compares only the start and the end."],
      "&Delta;H = products &minus; reactants.",
      "&Delta;H = %d kJ &minus; %d kJ = <b>+%d kJ, endothermic</b>." % (p, r, p - r), 2, 1)

    r, top, p = 92, 127, 15
    Q(T, "An exothermic reaction's energy diagram shows the reactants at %d kJ and the products at %d kJ, with the peak of the hill at %d kJ. How much energy must a collision have, at least, for the forward reaction to happen?" % (r, p, top),
      ["%d kJ" % (top - r), "%d kJ" % (top - p), "%d kJ" % top, "%d kJ" % (r - p)],
      ["The minimum energy is the activation energy: peak &minus; reactants = %d &minus; %d = %d kJ." % (top, r, top - r),
       "This measures from the products. E<sub>a</sub> for the forward reaction starts at the reactants.",
       "This is the energy of the peak, not its height above the reactants.",
       "This is the size of &Delta;H (reactants minus products), not the height of the hill."],
      "The minimum energy for an effective collision is E<sub>a</sub>. Measure it from the reactants.",
      "E<sub>a</sub> = %d kJ &minus; %d kJ = <b>%d kJ</b>." % (top, r, top - r), 2, 1)

    Q(T, "Two gases react in a sealed container. The same amounts of gas are moved into a container half the size, at the same temperature. How does the rate change?",
      ["Faster, because the molecules are more crowded and collide more often", "Slower, because the molecules have less room to move",
       "No change, because the amounts of gas are the same", "Faster, because the smaller container lowers the activation energy"],
      ["Halving the volume doubles the concentration of each gas, so there are more collisions per second.",
       "Less room means more crowding and more collisions, which speeds the reaction.",
       "The amounts are the same, but the concentrations are higher in the smaller volume.",
       "The container does not change E<sub>a</sub>; only a catalyst does. The extra collisions are what speed it up."],
      "Same amount of gas in half the space: what happens to the concentration?",
      "Higher concentration &rarr; <b>faster, from more collisions</b>.", 2)

    Q(T, "A donor kidney is carried to the transplant hospital in a cold preservation solution packed in ice. How does the cold help protect the organ?",
      ["It slows the cells' enzyme-catalyzed reactions, so the tissue uses up its stored energy and builds up waste more slowly.",
       "It kills every microbe on the organ, so the organ cannot be damaged.",
       "It speeds up the cells' reactions so the organ stays active.",
       "It raises the activation energy of every reaction in the cells."],
      ["At low temperature, molecules collide less often and fewer collisions reach E<sub>a</sub>, so metabolism slows and the organ lasts longer.",
       "Cold slows microbes but does not sterilize; the main benefit is slower reactions in the organ's own cells.",
       "Cold slows reactions; it does not speed them up.",
       "Temperature does not change the height of the hill; it changes how many collisions get over it."],
      "What does cooling do to reaction rates?",
      "Cold <b>slows the cells' reactions</b>.", 2)

    Q(T, "Why do wood shavings catch fire much more easily than a log of the same wood?",
      ["The shavings have far more surface area, so more wood is exposed to collisions with {O2}.",
       "Shavings are made of a different substance than logs.",
       "Shavings contain a catalyst that logs do not.",
       "A log has a lower activation energy, so it burns more slowly."],
      ["Breaking a solid into small pieces exposes more particles to collisions, so the reaction is faster.",
       "Both are the same wood; only the amount exposed to the air differs.",
       "No catalyst is involved; small pieces simply expose more surface.",
       "A lower E<sub>a</sub> would make burning faster, not slower; the difference is surface area."],
      "Same wood, different size of pieces.",
      "<b>More surface area</b> &rarr; more collisions with {O2}.", 1)

    Q(T, "The platinum and rhodium in a car's catalytic converter help change CO and NO in the exhaust into {CO2} and {N2}. Which statement is true?",
      ["The metals lower the activation energy of the reactions and are not used up.",
       "The metals are used up and must be replaced at each oil change.",
       "The metals work by heating the exhaust gas.",
       "The metals make the reactions release more heat."],
      ["A catalyst provides a lower-energy path and comes out unchanged, so the converter works for years.",
       "A catalyst is not consumed; that is why a small amount of metal can treat exhaust for many miles.",
       "A catalyst lowers E<sub>a</sub>; it does not act by heating the gas.",
       "A catalyst does not change &Delta;H."],
      "What are the two defining features of a catalyst?",
      "<b>Lower E<sub>a</sub>, not used up</b>.", 1)

    Q(T, "A farmworker with heat stroke on a July afternoon has a core body temperature of 41.5 °C. Why is so high a temperature dangerous for the body's enzyme-catalyzed reactions, even though higher temperatures usually speed reactions up?",
      ["At very high temperatures, enzymes begin to change shape (denature), so they slow down or stop working.",
       "Higher temperatures always slow reactions down.",
       "At 41.5 °C the molecules in the body stop colliding.",
       "A high temperature raises the activation energy of the body's reactions."],
      ["Enzymes are proteins whose shape matters; too much heat changes the shape, and the catalyzed reactions slow down.",
       "Raising the temperature usually speeds reactions up; the danger here comes from the enzymes themselves.",
       "Molecules collide more, not less, as the temperature rises.",
       "Temperature does not change E<sub>a</sub>; the problem is that the enzyme loses its working shape."],
      "Enzymes are proteins. What can heat do to a protein?",
      "Very high temperature <b>denatures enzymes</b>.", 2)

    Q(T, "Yeast enzymes ferment sugar in bread dough, making the {CO2} that makes it rise. Which change makes the dough rise faster?",
      ["Setting the dough in a warm spot", "Setting the dough in the refrigerator", "Using less yeast", "Mixing the dough with ice water"],
      ["A warmer temperature (but not too hot for the yeast) means more collisions, and more of them with at least E<sub>a</sub>.",
       "Cold slows the yeast's reactions, so the dough rises more slowly.",
       "Less yeast means less enzyme (catalyst), so the reactions are slower.",
       "Ice water cools the dough and slows the yeast's reactions."],
      "Which change raises the number of effective collisions per second?",
      "<b>A warm spot</b> speeds up the yeast's reactions.", 1)

    # ======================= ch13-dynamic (7) =======================
    T = 'ch13-dynamic'
    Q(T, "Which describes the concentrations of the reactants and products in a mixture at equilibrium?",
      ["They stay constant, but they are usually not equal.", "They are equal to each other.",
       "They are zero, because the reaction is complete.", "They keep changing, because both reactions are running."],
      ["Equal rates mean no net change, so every concentration stays constant at its own value.",
       "Equilibrium means constant concentrations, not equal ones.",
       "In most reactions some reactant remains, because the reverse reaction keeps running.",
       "Both reactions run, but at equal rates, so the concentrations do not change."],
      "Equal rates, constant amounts.",
      "<b>Constant, but usually not equal.</b>", 1)

    Q(T, "A sealed flask is filled with NO and {Br2}: [[2 NO(g) + Br2(g) <=> 2 NOBr(g)]] The [NOBr] readings were 0 M at 0 s, 0.0186 M at 6 s, 0.0254 M at 12 s, 0.0271 M at 18 s, 0.0271 M at 24 s, and 0.0271 M at 36 s. By which reading had the system reached equilibrium?",
      ["18 s", "12 s", "36 s", "6 s"],
      ["From this reading on, [NOBr] stays at 0.0271 M: constant concentration means equal forward and reverse rates.",
       "[NOBr] still rises after this reading (0.0254 M, then 0.0271 M), so the forward reaction is still faster.",
       "This is a later reading of the same constant value; the system was at equilibrium before it.",
       "[NOBr] is still rising quickly at this point."],
      "Find the first reading after which the value stops changing.",
      "[NOBr] is 0.0271 M from 18 s on: <b>by 18 s</b>.", 2)

    Q(T, "Nitrogen and oxygen are sealed in a flask at a very high temperature: [[N2(g) + O2(g) <=> 2 NO(g)]] Immediately afterward, before any NO has formed, which is true?",
      ["The forward rate is at its highest and the reverse rate is zero.", "The forward and reverse rates are equal.",
       "The reverse rate is at its highest.", "Both rates are zero until the mixture reaches equilibrium."],
      ["With the most reactant and no product, the forward reaction is as fast as it will be, and the reverse cannot run yet.",
       "The rates become equal only at equilibrium, after NO builds up.",
       "There is no NO yet, so the reverse reaction cannot happen at all.",
       "The forward reaction starts right away; it is the reverse rate that starts at zero."],
      "Which reaction can run when there is no product yet?",
      "<b>Forward rate highest, reverse rate zero.</b>", 2)

    Q(T, "A few iodine crystals are sealed in a flask, and a few more are left in an open dish, at the same temperature. [[I2(s) <=> I2(g)]] Which statement is correct?",
      ["In the sealed flask the violet vapor reaches a steady color, an equilibrium; in the open dish the crystals slowly disappear.",
       "Both reach equilibrium, because the change from solid to gas is reversible.",
       "Only the open dish reaches equilibrium, because the vapor can spread out.",
       "Neither reaches equilibrium, because a solid cannot be in equilibrium with a gas."],
      ["In the sealed flask, vapor turns back into crystals as fast as crystals turn to vapor. In the open dish the vapor drifts away, so the crystals keep shrinking.",
       "Reversible, yes, but equilibrium also needs a closed system, so that the vapor stays to re-form crystals.",
       "Open containers let a product escape, which prevents equilibrium.",
       "A solid and its vapor can reach dynamic equilibrium in a closed container."],
      "Equilibrium needs a closed system.",
      "<b>Only the sealed flask</b> reaches equilibrium.", 2)

    Q(T, "A sealed flask at equilibrium holds 0.12 M reactant and 0.88 M product, and the values do not change. What is true about the forward and reverse rates?",
      ["The two rates are equal.", "The forward rate is faster, because there is more product.",
       "The reverse rate is faster, because there is more product to react.", "Both rates are zero."],
      ["Constant concentrations mean no net change, so the rates must match, even though the amounts differ.",
       "A faster forward rate would keep raising the product concentration, but it is constant.",
       "A faster reverse rate would keep lowering the product concentration, but it is constant.",
       "Both reactions keep running at equilibrium; their rates are equal, not zero."],
      "Constant amounts tell you what about the rates?",
      "Constant concentrations: <b>equal rates</b>.", 2)

    Q(T, "Which of these is the best model of a dynamic equilibrium?",
      ["Two connected fish tanks, with fish swimming through the tube both ways at the same rate, so the number in each tank stays the same",
       "Two connected fish tanks with the tube blocked, so no fish move",
       "Two connected fish tanks, with fish moving mostly from the first tank into the second",
       "Two connected fish tanks that hold exactly the same number of fish"],
      ["Movement continues both ways at equal rates, so each count is constant: dynamic equilibrium.",
       "Nothing moves here; equilibrium is dynamic, not stopped.",
       "The counts are still changing, so the rates in the two directions are not equal.",
       "Equal amounts are not the point; equal rates in both directions are."],
      "Look for equal rates in both directions with constant amounts.",
      "<b>Fish moving both ways at the same rate.</b>", 1)

    Q(T, "On a concentration-versus-time graph for a reversible reaction, how can you tell when equilibrium has been reached?",
      ["Every concentration line has become flat (horizontal).", "The reactant and product lines cross.",
       "The product line reaches the top of the graph.", "The reactant line reaches zero."],
      ["Flat lines mean the concentrations are constant, which happens only when the forward and reverse rates are equal.",
       "Crossing lines show equal concentrations at one moment; equilibrium is about constant concentrations.",
       "The product line levels off at its equilibrium value, wherever that is on the graph.",
       "In most reactions some reactant is always left, because the reverse reaction keeps running."],
      "What does a constant concentration look like on a graph?",
      "<b>All lines flat.</b>", 1)

    # ======================= ch13-k (10) =======================
    T = 'ch13-k'
    Q(T, "Nitrous oxide (laughing gas) can break down at high temperature: [[2 N2O(g) <=> 2 N2(g) + O2(g)]] Write the equilibrium constant expression.",
      [KX([('N2', 2), ('O2', 1)], [('N2O', 2)]), KX([('N2O', 2)], [('N2', 2), ('O2', 1)]),
       "K = 2[N<sub>2</sub>][O<sub>2</sub>] / 2[N<sub>2</sub>O]", KX([('N2', 1), ('O2', 1)], [('N2O', 1)])],
      ["Products over reactants, with each coefficient as an exponent: N<sub>2</sub> and N<sub>2</sub>O are squared.",
       "This is reactants over products; K always puts products on top.",
       "Coefficients become exponents, not multipliers.",
       "This leaves out the exponents; the coefficient 2 on N<sub>2</sub> and N<sub>2</sub>O must become a power of 2."],
      "Products over reactants; coefficients become exponents.",
      "<b>%s</b>" % KX([('N2', 2), ('O2', 1)], [('N2O', 2)]), 2)

    Q(T, "Write the equilibrium constant expression for [[CH4(g) + 2 H2S(g) <=> CS2(g) + 4 H2(g)]]",
      [KX([('CS2', 1), ('H2', 4)], [('CH4', 1), ('H2S', 2)]), KX([('CH4', 1), ('H2S', 2)], [('CS2', 1), ('H2', 4)]),
       KX([('CS2', 1), ('H2', 1)], [('CH4', 1), ('H2S', 1)]), "K = [CS<sub>2</sub>] + [H<sub>2</sub>]<sup>4</sup> / ([CH<sub>4</sub>] + [H<sub>2</sub>S]<sup>2</sup>)"],
      ["All species are gases, so all appear: products on top, with H<sub>2</sub> to the 4th power and H<sub>2</sub>S squared.",
       "This is reactants over products; products go on top.",
       "This leaves out the exponents 4 and 2.",
       "Concentrations in K are multiplied, not added."],
      "Products over reactants, multiplied, with coefficients as exponents.",
      "<b>%s</b>" % KX([('CS2', 1), ('H2', 4)], [('CH4', 1), ('H2S', 2)]), 2)

    Q(T, "When baking soda is heated in a closed container, it sets up this equilibrium: [[2 NaHCO3(s) <=> Na2CO3(s) + H2O(g) + CO2(g)]] Write the equilibrium constant expression.",
      [KX([('H2O', 1), ('CO2', 1)], []), KX([('CO2', 1)], []), KX([('Na2CO3', 1), ('H2O', 1), ('CO2', 1)], [('NaHCO3', 2)]), KX([], [('H2O', 1), ('CO2', 1)])],
      ["The two solids are left out. Water is a gas here, so it stays in with the CO<sub>2</sub>.",
       "Water is left out only as a liquid; H<sub>2</sub>O(g) is a gas, so it belongs in K.",
       "Pure solids (NaHCO<sub>3</sub> and Na<sub>2</sub>CO<sub>3</sub>) are left out of K.",
       "This puts the products on the bottom; products go on top."],
      "Cross out the (s) species. Is the water a gas or a liquid?",
      "<b>K = [H<sub>2</sub>O][CO<sub>2</sub>]</b>", 3)

    Q(T, "In the Mond process for purifying nickel, nickel reacts with carbon monoxide: [[Ni(s) + 4 CO(g) <=> Ni(CO)4(g)]] Write the equilibrium constant expression.",
      [KX([('Ni(CO)4', 1)], [('CO', 4)]), KX([('Ni(CO)4', 1)], [('Ni', 1), ('CO', 4)]), KX([('CO', 4)], [('Ni(CO)4', 1)]), KX([('Ni(CO)4', 1)], [('CO', 1)])],
      ["Solid nickel is left out; the gases remain, with [CO] raised to the 4th power.",
       "Ni(s) is a pure solid, so it is left out of K.",
       "This is reactants over products; the product gas goes on top.",
       "The coefficient 4 on CO must become an exponent of 4."],
      "Cross out the solid, then use the coefficient of CO as an exponent.",
      "<b>%s</b>" % KX([('Ni(CO)4', 1)], [('CO', 4)]), 2)

    cs = {'N2': '0.784', 'O2': '0.217', 'NO': '0.00369'}
    n = ns(*cs.values()); k_ = Kv([(cs['NO'], 2)], [(cs['N2'], 1), (cs['O2'], 1)])
    Q(T, "At the very high temperature of a car engine, nitrogen and oxygen react: [[N2(g) + O2(g) <=> 2 NO(g)]] An equilibrium mixture contains [{N2}] = %s M, [{O2}] = %s M, and [NO] = %s M. Calculate K." % (cs['N2'], cs['O2'], cs['NO']),
      [num(k_, n), num(1 / k_, n), num(D(cs['NO']) / (D(cs['N2']) * D(cs['O2'])), n), num(2 * D(cs['NO']) / (D(cs['N2']) * D(cs['O2'])), n)],
      ["K = [NO]<sup>2</sup> / ([N<sub>2</sub>][O<sub>2</sub>]) = (%s)<sup>2</sup> / [(%s)(%s)]; three significant figures." % (cs['NO'], cs['N2'], cs['O2']),
       "This is reactants over products, the inverse of K.",
       "This forgets to square [NO]; its coefficient is 2.",
       "This multiplies [NO] by 2; the coefficient becomes an exponent, not a multiplier."],
      "Square the NO term.",
      "K = (%s)<sup>2</sup> / [(%s)(%s)] = <b>%s</b>. K &lt; 1, so reactants are favored." % (cs['NO'], cs['N2'], cs['O2'], num(k_, n)), 3, 1)

    cs = {'NO2': '0.0472', 'CO': '0.0316', 'NO': '0.0926', 'CO2': '0.0926'}
    n = ns(*cs.values()); k_ = Kv([(cs['NO'], 1), (cs['CO2'], 1)], [(cs['NO2'], 1), (cs['CO'], 1)])
    Q(T, "An equilibrium mixture for [[NO2(g) + CO(g) <=> NO(g) + CO2(g)]] contains [{NO2}] = %s M, [CO] = %s M, [NO] = %s M, and [{CO2}] = %s M. Calculate K." % (cs['NO2'], cs['CO'], cs['NO'], cs['CO2']),
      [num(k_, n), num(1 / k_, n), num((D(cs['NO']) + D(cs['CO2'])) / (D(cs['NO2']) + D(cs['CO'])), n), num(D(cs['NO']) * D(cs['CO2']) * D(cs['NO2']) * D(cs['CO']), n)],
      ["K = [NO][CO<sub>2</sub>] / ([NO<sub>2</sub>][CO]); all coefficients are 1. Three significant figures.",
       "This is reactants over products, the inverse of K.",
       "This adds concentrations; they are multiplied in K.",
       "This multiplies all four concentrations; the reactant terms belong in the denominator."],
      "Products over reactants, multiplied, not added.",
      "K = (%s)(%s) / [(%s)(%s)] = <b>%s</b>. K &gt; 1, so products are favored, but K is close to 1 (between 0.1 and 10), so sizable amounts of both are present." % (cs['NO'], cs['CO2'], cs['NO2'], cs['CO'], num(k_, n)), 3, 1)

    cs = {'NO': '0.0217', 'Br2': '0.0474', 'NOBr': '0.0632'}
    n = ns(*cs.values()); k_ = Kv([(cs['NOBr'], 2)], [(cs['NO'], 2), (cs['Br2'], 1)])
    Q(T, "An equilibrium mixture for [[2 NO(g) + Br2(g) <=> 2 NOBr(g)]] contains [NO] = %s M, [{Br2}] = %s M, and [NOBr] = %s M. Calculate K." % (cs['NO'], cs['Br2'], cs['NOBr']),
      [num(k_, n), num(1 / k_, n), num(D(cs['NOBr']) / (D(cs['NO']) * D(cs['Br2'])), n), num(D(cs['NOBr']) / (D(cs['NO']) + D(cs['Br2'])), n)],
      ["K = [NOBr]<sup>2</sup> / ([NO]<sup>2</sup>[Br<sub>2</sub>]) = (%s)<sup>2</sup> / [(%s)<sup>2</sup>(%s)]; three significant figures." % (cs['NOBr'], cs['NO'], cs['Br2']),
       "This is reactants over products, the inverse of K.",
       "This leaves out the exponents; [NOBr] and [NO] must each be squared.",
       "This adds the reactant concentrations; they are multiplied in K, and each is raised to its coefficient."],
      "Square the two terms with a coefficient of 2.",
      "K = (%s)<sup>2</sup> / [(%s)<sup>2</sup>(%s)] = <b>%s</b>. K &gt; 1, so NOBr is favored." % (cs['NOBr'], cs['NO'], cs['Br2'], num(k_, n)), 3, 1)

    k0 = '0.0472'
    Q(T, "At a certain temperature, K = %s for [[CS2(g) + 4 H2(g) <=> CH4(g) + 2 H2S(g)]] What is K for [[CH4(g) + 2 H2S(g) <=> CS2(g) + 4 H2(g)]] at the same temperature?" % k0,
      [num(1 / D(k0), 3), k0, '-' + k0, num(1 - D(k0), 3)],
      ["The second equation is the first one reversed, so its K is the reciprocal: 1 / %s." % k0,
       "Reversing the reaction flips products and reactants, so K becomes 1/K.",
       "K is never negative. Reversing a reaction flips the sign of &Delta;H, not of K.",
       "The reverse K is 1 divided by K, not 1 minus K."],
      "Compare the two equations. What does reversing do to K?",
      "K<sub>reverse</sub> = 1 / %s = <b>%s</b>." % (k0, num(1 / D(k0), 3)), 2, 1)

    Q(T, "A reaction has K = 2.1 &times; 10<sup>&minus;12</sup> at 25 °C. What does the equilibrium mixture contain?",
      ["Mostly reactants, with almost no product formed", "Mostly products, with almost no reactant left",
       "Sizable amounts of both reactants and products", "Equal concentrations of reactants and products"],
      ["K &lt; 1, and very small (&#8810; 1): reactants are favored, and the reaction barely happens.",
       "That describes a K far greater than 1; this K is far less than 1.",
       "That describes K close to 1 (roughly 0.1 to 10).",
       "K does not mean equal concentrations; a K this small means far more reactant than product."],
      "Compare K with 1.",
      "K &#8810; 1: <b>mostly reactants</b>.", 1)

    Q(T, "Two sealed flasks of the same reaction at the same temperature start with different amounts of reactants. After each reaches equilibrium, how do their K values compare?",
      ["They are the same, because K depends only on the reaction and the temperature.",
       "The flask that started with more reactant has a larger K.",
       "The flask that started with more reactant has a smaller K.",
       "K cannot be compared, because the equilibrium concentrations are different."],
      ["Different starting mixtures reach different equilibrium concentrations, but the same ratio K at a given temperature.",
       "More starting reactant gives more of everything at equilibrium, but the same K.",
       "K does not depend on the starting amounts.",
       "The concentrations differ, but plugging each set into the K expression gives the same value."],
      "What is the only thing that changes K?",
      "<b>Same K</b>; only temperature changes K.", 2)

    # ======================= ch13-lechat (16) =======================
    T = 'ch13-lechat'
    EW = "[[CO(g) + H2O(g) <=> CO2(g) + H2(g)]]"
    Q(T, "Steam, {H2O}(g), is added to this mixture at equilibrium: " + EW + " What happens to [CO]?",
      ["Shifts right, and [CO] decreases", "Shifts left, and [CO] increases", "No shift, because water is left out of K", "Shifts right, and [CO] increases"],
      ["Add &rarr; away: steam is a reactant, so the system shifts right and uses up some CO.",
       "Adding a reactant pushes the system to the right, not the left.",
       "Here water is a gas, so it appears in K and adding it causes a shift.",
       "A shift to the right uses up reactants, so [CO] goes down."],
      "Which side is the steam on?",
      "Add steam &rarr; <b>shifts right; [CO] decreases</b>.", 2)

    ES = "[[2 H2S(g) <=> 2 H2(g) + S2(g)]]"
    Q(T, "{H2} is removed from this mixture through a membrane that only {H2} can pass: " + ES + " Which way does the equilibrium shift?",
      ["Shifts right, toward the removed {H2}", "Shifts left, away from the removed {H2}", "No shift, because {H2} is a product", "Shifts right, and K increases"],
      ["Take &rarr; toward: removing a product shifts the system right, so more {H2S} breaks down.",
       "Removing a substance pulls the system toward it, not away.",
       "Products count just as much as reactants; removing one causes a shift.",
       "The shift is right, but K changes only with temperature."],
      "Take &rarr; toward.",
      "Remove {H2} &rarr; <b>shifts right</b>.", 2)

    EP = "[[CO(g) + Cl2(g) <=> COCl2(g)]]"
    Q(T, "Extra {COCl2} is added to this mixture at equilibrium: " + EP + " What happens to [{Cl2}]?",
      ["Shifts left, and [{Cl2}] increases", "Shifts right, and [{Cl2}] decreases", "No shift, and [{Cl2}] does not change", "Shifts left, and [{Cl2}] decreases"],
      ["Add &rarr; away: adding the product shifts the system left, which makes more CO and {Cl2}.",
       "Adding a product pushes the system left, not right.",
       "Adding a product upsets the ratio in K, so the system shifts.",
       "A shift to the left makes reactants, so [{Cl2}] goes up."],
      "First find the shift, then follow it to {Cl2}.",
      "<b>Shifts left; [{Cl2}] increases.</b>", 2)

    EB = "[[2 NaHCO3(s) <=> Na2CO3(s) + H2O(g) + CO2(g)]]"
    Q(T, "More solid {NaHCO3} is added to this mixture at equilibrium in a sealed container: " + EB + " Which way does the equilibrium shift?",
      ["No shift, because a pure solid does not appear in K", "Shifts right, away from the added {NaHCO3}",
       "Shifts left, toward the added {NaHCO3}", "Shifts right, and [{CO2}] increases"],
      ["K = [H<sub>2</sub>O][CO<sub>2</sub>] has no NaHCO<sub>3</sub> term, so adding the solid changes nothing.",
       "Add &rarr; away applies to gases and dissolved species, not to pure solids.",
       "Adding never shifts the system toward the added substance, and a solid causes no shift.",
       "With no shift, [CO<sub>2</sub>] stays the same."],
      "Is {NaHCO3}(s) in the K expression?",
      "Solid added: <b>no shift</b>.", 2)

    Q(T, "In the Mond process, nickel carbonyl gas is carried away as it forms: [[Ni(s) + 4 CO(g) <=> Ni(CO)4(g)]] Which way does the equilibrium shift?",
      ["Shifts right, so more nickel reacts with CO", "Shifts left, so {Ni(CO)4} breaks down", "No shift, because nickel is a solid", "Shifts right, and K increases"],
      ["Take &rarr; toward: removing the product shifts the system right, so more solid nickel is turned into the gas and carried off.",
       "Removing a product pulls the system toward it, not away from it.",
       "Nickel is left out of K, but {Ni(CO)4} is a gas in K, so removing it causes a shift.",
       "The shift is right, but only temperature changes K."],
      "Take &rarr; toward.",
      "Remove {Ni(CO)4} &rarr; <b>shifts right</b>.", 2)

    Q(T, "For this reaction, &Delta;H = -109 kJ: " + EP + " The mixture is cooled. Which describes the shift and K?",
      ["Shifts right, and K increases", "Shifts left, and K decreases", "Shifts right, and K does not change", "No shift, and K increases"],
      ["Exothermic: heat is a product. Cooling removes it, so take &rarr; toward shifts the system right, and K gets larger.",
       "This treats heat as a reactant; for a negative &Delta;H, heat is a product.",
       "The direction is right, but temperature is the one stress that changes K.",
       "Cooling is a stress, so the system shifts to match the new, larger K."],
      "Exothermic: which side is heat on?",
      "Heat is a product; cooling &rarr; <b>shifts right, K increases</b>.", 2)

    EN = "[[N2(g) + O2(g) <=> 2 NO(g)]]"
    Q(T, "Captured {CO2} can be turned into CO by the reverse water&ndash;gas shift reaction, &Delta;H = +41.2 kJ: [[CO2(g) + H2(g) <=> CO(g) + H2O(g)]] The temperature of the equilibrium mixture is raised. Which describes the shift and K?",
      ["Shifts right, and K increases", "Shifts left, and K decreases", "Shifts right, and K does not change", "Shifts left, and K increases"],
      ["Endothermic: heat is a reactant. Adding heat shifts the system right, toward CO, and K gets larger.",
       "This treats heat as a product; for a positive &Delta;H, heat is a reactant.",
       "The direction is right, but a temperature change always changes K.",
       "Heating an endothermic reaction shifts it right, not left."],
      "Positive &Delta;H: heat is on which side?",
      "Heat is a reactant: <b>shifts right, K increases</b>.", 2)

    Q(T, "The decomposition of baking soda is endothermic: " + EB + " What does the heat of an oven do to this equilibrium in a batter?",
      ["Shifts right, and [{CO2}] increases", "Shifts left, and [{CO2}] decreases", "No shift, because the reactant is a solid", "Shifts right, and K does not change"],
      ["Heat is a reactant, so adding heat shifts the system right, making the {CO2} gas that helps the batter rise.",
       "This treats heat as a product; for an endothermic reaction, heat is a reactant.",
       "Temperature shifts every equilibrium; the solid only stays out of K.",
       "The direction is right, but a temperature change always changes K."],
      "Endothermic: heat is a reactant.",
      "Add heat &rarr; <b>shifts right, more {CO2}</b>.", 2)

    Q(T, "For [[2 NO(g) + Cl2(g) <=> 2 NOCl(g)]] &Delta;H = -77.2 kJ. Which change increases the amount of NOCl at equilibrium?",
      ["Decreasing the volume", "Raising the temperature", "Adding a catalyst", "Removing some {Cl2}"],
      ["3 mol of gas on the left, 2 on the right: a smaller volume shifts the system right, toward fewer moles, making more NOCl.",
       "Exothermic: heat is a product, so heating shifts the system left and lowers the amount of NOCl.",
       "A catalyst speeds both directions equally; the equilibrium amount of NOCl stays the same.",
       "Take &rarr; toward: removing {Cl2} shifts the system left, lowering the amount of NOCl."],
      "Check each change: concentration, temperature, volume, catalyst.",
      "<b>Decreasing the volume</b> shifts the system toward fewer moles of gas (right).", 3)

    Q(T, "The volume of the container is decreased for this mixture at equilibrium: " + EW + " Which way does the equilibrium shift?",
      ["No shift, because each side has 2 moles of gas", "Shifts right, toward the products", "Shifts left, toward the side with water", "Shifts right, and K increases"],
      ["1 + 1 = 2 mol of gas on each side, so a volume change does not favor either side.",
       "Both sides have the same number of moles of gas, so there is no side with fewer moles to shift toward.",
       "Water is a gas here and is counted like the others; the sides are equal, 2 mol each.",
       "There is no shift, and a volume change never changes K."],
      "Count moles of gas on each side.",
      "2 mol = 2 mol of gas: <b>no shift</b>.", 2)

    Q(T, "The volume of the container is decreased for this mixture at equilibrium: " + ES + " Which way does the equilibrium shift?",
      ["Shifts left, toward the side with fewer moles of gas", "Shifts right, toward the side with more moles of gas",
       "No shift, because {H2S} is the only reactant", "Shifts left, and K decreases"],
      ["Left: 2 mol of gas; right: 2 + 1 = 3 mol. A smaller volume shifts the system toward fewer moles of gas, the left.",
       "A smaller volume (higher pressure) favors the side with fewer gas particles.",
       "What matters is the number of moles of gas on each side, not the number of reactants.",
       "The direction is right, but K does not change with volume."],
      "Count the gas coefficients on each side.",
      "2 mol vs 3 mol of gas: <b>shifts left</b>.", 2)

    Q(T, "Nitrogen gas, which does not react with any of these gases, is pumped into a rigid tank (constant volume) holding this mixture at equilibrium: " + ES + " What happens?",
      ["No shift, because the concentrations of {H2S}, {H2}, and {S2} do not change", "Shifts left, because the total pressure increased",
       "Shifts right, because nitrogen takes up space", "Shifts left, and K decreases"],
      ["The added {N2} is inert here and the volume is fixed, so no reacting gas changes concentration, and nothing in K changes.",
       "Total pressure rises, but the reacting gases' concentrations stay the same, so there is no stress.",
       "At constant volume, the added gas does not crowd the reacting gases into less space.",
       "There is no shift, and K changes only with temperature."],
      "Does an inert gas at constant volume change any concentration in K?",
      "Inert gas, constant volume: <b>no shift</b>.", 2)

    Q(T, "Activated carbon, the catalyst used to make phosgene, is added to a sealed flask holding this mixture at equilibrium: " + EP + " What happens?",
      ["No shift: [{COCl2}] does not change, though the reactions in both directions run faster", "Shifts right, and [{COCl2}] increases",
       "Shifts left, and [{COCl2}] decreases", "No shift, but K increases"],
      ["A catalyst speeds the forward and reverse reactions equally, so the equilibrium amounts and K stay the same.",
       "A catalyst does not favor products; it speeds up the reverse reaction just as much.",
       "A catalyst does not favor reactants either.",
       "A catalyst never changes K; only temperature does."],
      "Which direction does a catalyst speed up?",
      "<b>No shift</b>; equilibrium is just reached faster.", 2)

    Q(T, "In iron-deficiency anemia, red blood cells contain less hemoglobin. Compared with a healthy person breathing the same air, what does the lower [Hb] do to this equilibrium? " + EH_(),
      ["Shifts left, and [{HbO2}] decreases, so the blood carries less {O2}", "Shifts right, and [{HbO2}] increases",
       "No shift, because hemoglobin is a catalyst", "Shifts left, and [{O2}] decreases"],
      ["Less of the reactant Hb means less {HbO2} can form (take &rarr; toward the left), so the blood carries less oxygen.",
       "With less Hb, a reactant, the system shifts left, not right.",
       "Hemoglobin is a reactant that binds {O2}, not a catalyst.",
       "A shift to the left releases {O2}, so [{O2}] goes up, not down."],
      "Hb is a reactant. Is it added or taken away?",
      "Less Hb &rarr; <b>shifts left, less {HbO2}</b>.", 3)

    Q(T, "A patient with broken ribs takes only shallow breaths because breathing hurts, and {CO2} builds up in her blood. What happens to this equilibrium? " + EC_(),
      ["Shifts right, [{H^+}] increases, and blood pH falls", "Shifts left, [{H^+}] decreases, and blood pH rises",
       "Shifts right, [{H^+}] decreases, and blood pH rises", "No shift, because {CO2} is not part of the equilibrium"],
      ["Add &rarr; away: built-up {CO2} shifts the system right, making more {H^+}, so the pH falls (respiratory acidosis).",
       "This is what fast breathing does; here {CO2} is building up, not being removed.",
       "A shift to the right makes more {H^+}, not less.",
       "{CO2} is the first reactant in this equilibrium."],
      "Is {CO2} being added or removed?",
      "{CO2} builds up &rarr; <b>shifts right, more {H^+}, pH falls</b>.", 2)

    Q(T, "In some emergencies, sodium bicarbonate is given by IV, which adds {HCO3^-} to the blood. What happens to this equilibrium? " + EC_() + " (Context only; drugs are given as ordered.)",
      ["Shifts left, [{H^+}] decreases, and blood pH rises", "Shifts right, [{H^+}] increases, and blood pH falls",
       "Shifts left, [{H^+}] decreases, and blood pH falls", "No shift, because {HCO3^-} is a spectator ion"],
      ["Add &rarr; away: {HCO3^-} is a product, so the system shifts left; {H^+} is used up, so the pH rises, and the extra {CO2} formed is breathed out.",
       "Adding a product pushes the system left, not right.",
       "Less {H^+} means a higher pH, not a lower one.",
       "{HCO3^-} is part of this equilibrium, so adding it causes a shift."],
      "Which side is {HCO3^-} on?",
      "Add {HCO3^-} &rarr; <b>shifts left, less {H^+}, pH rises</b>.", 3)


def EH_(): return "[[Hb(aq) + O2(aq) <=> HbO2(aq)]]"
def EC_(): return "[[CO2(aq) + H2O(l) <=> H2CO3(aq) <=> H^+(aq) + HCO3^-(aq)]]"
def EE_(): return "[[Ca5(PO4)3OH(s) <=> 5 Ca^2+(aq) + 3 PO4^3-(aq) + OH^-(aq)]]"


if __name__ == '__main__':
    build_hw()
    dump(sys.argv[1])
