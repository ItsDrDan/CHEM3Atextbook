#!/usr/bin/env python3
"""Try It page splits (audit/TRYIT_POOLS_2026-11-20.md): 17 new questions, then each of 1.9/1.9.1, 6.2/6.3 and 7.1/7.2 gets
its own question ids. Every number is recomputed here before anything is written. c[0] is the right answer; the widget
shuffles the choices. Run once from the repo root: python3 tools/bank_page_splits.py"""
import json
from decimal import Decimal as D, ROUND_HALF_UP
from math import gcd


def sf(x, n):
    x = D(str(x))
    return x.quantize(D(1).scaleb(x.adjusted() - n + 1), rounding=ROUND_HALF_UP)


# ---------- the math behind every answer ----------
assert sf(D('65.0') * D('0.786'), 3) == D('51.1') and sf(D('65.0') / D('0.786'), 3) == D('82.7')
assert sf(D('0.786') / D('65.0'), 3) == D('0.0121')
assert sf(D('40.0') / D('1.04'), 3) == D('38.5') and sf(D('40.0') * D('1.04'), 3) == D('41.6')
assert sf(D('1.04') / D('40.0'), 3) == D('0.0260')
assert sf(D('3.80') * 1000 * D('1.03') / 1000, 3) == D('3.91') and sf(D('3.80') / D('1.03'), 3) == D('3.69')
assert sf(D('1500') / D('0.784') / 1000, 3) == D('1.91') and sf(D('1.50') * D('0.784'), 3) == D('1.18')
assert sf(D('0.784') / D('1.50'), 3) == D('0.523')
assert sf(D('12.0') * D('1.025'), 3) == D('12.3') and sf(D('12.0') / D('1.025'), 3) == D('11.7')
assert sf(D('1.025') / D('12.0'), 3) == D('0.0854')
assert 385 - 112 == 273 and 385 + 112 == 497
assert sf(D('50.0') / D('0.789'), 3) == D('63.4') and sf(D('50.0') / D('1.00'), 3) == D('50.0')
assert 3 * 2 + 2 == 8 and 2 * 2 * 2 == 8


def balanced(left, right):
    tot = lambda side: {e: sum(c * f.get(e, 0) for c, f in side) for c0, f0 in side for e in f0}
    return tot(left) == tot(right)


N2, H2, NH3 = {'N': 2}, {'H': 2}, {'N': 1, 'H': 3}
assert balanced([(1, N2), (3, H2)], [(2, NH3)])
CaN, NaP = {'Ca': 1, 'N': 2, 'O': 6}, {'Na': 3, 'P': 1, 'O': 4}
CaP, NaN = {'Ca': 3, 'P': 2, 'O': 8}, {'Na': 1, 'N': 1, 'O': 3}
assert balanced([(3, CaN), (2, NaP)], [(1, CaP), (6, NaN)])
EtOH, O2, CO2, H2O = {'C': 2, 'H': 6, 'O': 1}, {'O': 2}, {'C': 1, 'O': 2}, {'H': 2, 'O': 1}
assert balanced([(1, EtOH), (3, O2)], [(2, CO2), (3, H2O)])
Al, Al2O3 = {'Al': 1}, {'Al': 2, 'O': 3}
assert balanced([(4, Al), (3, O2)], [(2, Al2O3)])
assert gcd(gcd(4, 3), 2) == 1 and gcd(gcd(3, 2), 6) == 1

S = lambda n: '<sub>%d</sub>' % n

CH01 = [
    dict(t='ch01-density', d=1, k=1,
         q='A bottle of rubbing alcohol has a density of 0.786 g/mL. What is the mass of 65.0 mL of it?',
         c=['51.1 g', '82.7 g', '0.0121 g', '51.1 mL'],
         y=['65.0 mL &times; (0.786 g / 1 mL) = 51.09 g, which rounds to 51.1 g. The mL cancel and grams remain.',
            'This divides by the density, so the units do not cancel to grams. Going from mL to g, put mL on the bottom of the factor.',
            'This divides the density by the volume. Start with the volume that stands alone, then multiply by g/mL.',
            'The number is right, but the question asks for a mass. After mL cancels, the unit left is grams.'],
         h='Start with the volume. Which way up must the density go so that mL cancels?',
         w='65.0 mL &times; (0.786 g / 1 mL) = 51.09 g = <b>51.1 g</b> (3 significant figures). Check: the density is less than 1 g/mL, so the mass in grams should be smaller than the volume in mL.'),
    dict(t='ch01-density', d=1, k=1,
         q='A compounding pharmacist needs 40.0 g of propylene glycol (d = 1.04 g/mL) but will measure it by volume. What volume is needed?',
         c=['38.5 mL', '41.6 mL', '0.0260 mL', '38.5 g'],
         y=['40.0 g &times; (1 mL / 1.04 g) = 38.46 mL, which rounds to 38.5 mL. The grams cancel and mL remain.',
            'This multiplies by g/mL, which leaves g<sup>2</sup>/mL. Flip the density so grams are on the bottom.',
            'This divides the density by the mass. Start with the mass, then multiply by the factor with g on the bottom.',
            'The number is right, but the question asks for a volume. After grams cancel, the unit left is mL.'],
         h='You have grams and want mL. Write the density with grams on the bottom.',
         w='40.0 g &times; (1 mL / 1.04 g) = 38.46 mL = <b>38.5 mL</b>. Check: the density is a little more than 1 g/mL, so the volume should be a little less than 40.0.'),
    dict(t='ch01-density', d=1, k=0,
         q='Which setup correctly finds the volume of 30.0 g of ethanol (d = 0.789 g/mL)?',
         c=['30.0 g &times; (1 mL / 0.789 g)', '30.0 g &times; (0.789 g / 1 mL)', '30.0 g &times; (0.789 mL / 1 g)', '30.0 mL &times; (0.789 g / 1 mL)'],
         y=['Grams are on top in the given and on the bottom of the factor, so they cancel and leave mL.',
            'Grams are on top twice here, so they do not cancel. Flip the density.',
            'The units were swapped on the number: 0.789 belongs with grams, because 0.789 g takes up 1 mL.',
            'The given quantity is a mass, 30.0 g, not a volume. Start with the units the problem gives you.'],
         h='Check the units first. In the right setup, the unit you start with cancels.',
         w='The density says 0.789 g = 1 mL. To cancel grams, use <b>30.0 g &times; (1 mL / 0.789 g)</b>, which is 38.0 mL.'),
    dict(t='ch01-density', d=2, k=1,
         q='A 3.80 L jug of whole milk from a Valley dairy has a density of 1.03 g/mL. What is the mass of the milk in kilograms?',
         c=['3.91 kg', '3.69 kg', '3910 kg', '0.00391 kg'],
         y=['3.80 L &rarr; 3800 mL; 3800 mL &times; 1.03 g/mL = 3914 g; 3914 g &divide; 1000 = 3.91 kg.',
            'This divides by the density. Going from volume to mass, multiply by g/mL.',
            'This leaves out the last step. The product is in grams, so divide by 1000 to get kilograms.',
            'The metric step went the wrong way. There are 1000 mL in 1 L, so the number of mL is larger than the number of L.'],
         h='The density uses mL, so change liters to mL first. Then go to grams, then to kilograms.',
         w='3.80 L &times; (1000 mL / 1 L) &times; (1.03 g / 1 mL) &times; (1 kg / 1000 g) = <b>3.91 kg</b>. The metric factors are exact, so the answer has 3 significant figures.'),
    dict(t='ch01-density', d=3, k=1,
         q='A salon supplier ships 1.50 kg of acetone (d = 0.784 g/mL), the solvent in nail polish remover. What volume is this, in liters?',
         c=['1.91 L', '1.18 L', '1910 L', '0.523 L'],
         y=['1.50 kg &rarr; 1500 g; 1500 g &times; (1 mL / 0.784 g) = 1913 mL; 1913 mL &divide; 1000 = 1.91 L.',
            'This multiplies by the density. Going from mass to volume, use the factor with grams on the bottom.',
            'This stops at mL but labels the number as liters. Divide by 1000 to go from mL to L.',
            'This divides the density by the mass. Start with the mass, and let its unit cancel.'],
         h='Plan the path: kg to g, g to mL using the density, then mL to L.',
         w='1.50 kg &times; (1000 g / 1 kg) &times; (1 mL / 0.784 g) &times; (1 L / 1000 mL) = <b>1.91 L</b>. Check: the density is below 1 g/mL, so the liters should be more than the kilograms.'),
    dict(t='ch01-density', d=2, k=1,
         q='A urine sample has a specific gravity of 1.025. About what is the mass of a 12.0 mL portion of the sample?',
         c=['12.3 g', '11.7 g', '12.0 g', '0.0854 g'],
         y=['A specific gravity of 1.025 means a density of about 1.025 g/mL: 12.0 mL &times; 1.025 g/mL = 12.3 g.',
            'This divides by the density. Going from mL to g, multiply by g/mL.',
            'This treats the sample as pure water. The specific gravity says it is slightly denser than water.',
            'This divides the density by the volume. Start with the volume, then multiply by the density.'],
         h='Specific gravity compares a density with water at about 1 g/mL. Turn it into a density first.',
         w='Density &asymp; 1.025 g/mL, so 12.0 mL &times; (1.025 g / 1 mL) = <b>12.3 g</b> (3 significant figures).'),
    dict(t='ch01-density', d=1, k=0,
         q='After a procedure, soaked surgical sponges weigh 385 g. The same sponges weighed 112 g dry. Using the rule 1 g &asymp; 1 mL, about how much blood do they hold?',
         c=['273 mL', '385 mL', '497 mL', '112 mL'],
         y=['The blood is the difference: 385 g &minus; 112 g = 273 g, and 1 g &asymp; 1 mL gives about 273 mL.',
            'This counts the mass of the sponges too. Subtract their dry mass first.',
            'This adds the two masses. The soaked mass already includes the sponges, so subtract.',
            'This is the mass of the dry sponges, which hold no blood.'],
         h='What part of the soaked mass is actually blood?',
         w='Blood mass = 385 g &minus; 112 g = 273 g. By the rule 1 g &asymp; 1 mL, that is about <b>273 mL</b>.'),
    dict(t='ch01-density', d=2, k=0,
         q='You pour out 50.0 g of water (d = 1.00 g/mL) and 50.0 g of ethanol (d = 0.789 g/mL). Which sample takes up more volume, and why?',
         c=['Ethanol, because each gram of it takes up more mL',
            'Water, because each gram of it takes up more mL',
            'Neither, because equal masses have equal volumes',
            'Ethanol, because each mL of it holds more grams'],
         y=['Volume = mass &divide; density. The smaller density gives the larger volume: 63.4 mL of ethanol versus 50.0 mL of water.',
            'Water is the denser liquid, so one gram of it takes up less space. Compare 1/d for each liquid.',
            'Equal masses have equal volumes only when the densities match, and these do not.',
            'The liquid is right, but the reason is backward: 0.789 g/mL means fewer grams in each mL than water.'],
         h='Flip each density to get mL per gram. Which liquid has the larger number?',
         w='Water: 50.0 g &times; (1 mL / 1.00 g) = 50.0 mL. Ethanol: 50.0 g &times; (1 mL / 0.789 g) = 63.4 mL. <b>Ethanol takes up more volume</b> because its lower density means more mL per gram.'),
]

CH06 = [
    dict(t='ch06-lewis', d=1, k=0,
         q='Ammonia, NH' + S(3) + ', has three N&ndash;H bonds and one lone pair on N. How many electrons does the N atom count around itself?',
         c=['8', '7', '5', '6'],
         y=['Each bond counts as 2 electrons: 3 &times; 2 = 6, and the lone pair adds 2, for an octet.',
            'This counts the lone pair as 1 electron. A lone pair is a pair, so it counts as 2.',
            'This is the number of valence electrons N starts with. Now count all electrons in its bonds and lone pair.',
            'This counts the bonds but leaves out the lone pair. An atom counts both.'],
         h='One line is two electrons, and a lone pair is two electrons. Add both kinds.',
         w='3 bonds &times; 2 electrons + 1 lone pair &times; 2 electrons = <b>8</b> electrons, an octet.'),
    dict(t='ch06-lewis', d=2, k=0,
         q='Carbon dioxide is O=C=O. How many electrons in total are shared in its two double bonds?',
         c=['8', '4', '2', '16'],
         y=['Each double bond is 2 shared pairs, or 4 electrons. Two double bonds share 8 electrons.',
            'This is the number of shared pairs, or the electrons in only one double bond. Count both bonds, 2 electrons per line.',
            'This counts the two bonds as one pair each. A double bond is two shared pairs.',
            'This is the total number of valence electrons on all three atoms, including the lone pairs. Count only the shared ones.'],
         h='Count the lines between atoms. Each line is one shared pair.',
         w='O=C=O has 4 lines, and each line is 2 electrons: 4 &times; 2 = <b>8</b> shared electrons.'),
    dict(t='ch06-lewis', d=1, k=0,
         q='The amino acids in your proteins all contain nitrogen. In a neutral molecule, how many covalent bonds does a nitrogen atom usually form?',
         c=['3', '5', '1', '4'],
         y=['N has 5 valence electrons and needs 3 more for an octet, so it usually forms 3 bonds (the N in HONC 1-2-3-4).',
            'This is its number of valence electrons. The number of bonds is how many more electrons it needs.',
            'One bond is usual for H and the halogens. Group 15 atoms need more than one electron.',
            'Four bonds is the usual count for carbon, which has one fewer valence electron than nitrogen.'],
         h='How many more electrons does nitrogen need to reach 8? HONC can help.',
         w='Nitrogen has 5 valence electrons and needs 3 more, so it usually forms <b>3</b> bonds and keeps one lone pair.'),
    dict(t='ch06-lewis', d=2, k=0,
         q='Which list puts the carbon&ndash;carbon bonds in order from <b>shortest</b> to <b>longest</b>?',
         c=['C&equiv;C, then C=C, then C&ndash;C', 'C&ndash;C, then C=C, then C&equiv;C', 'C=C, then C&equiv;C, then C&ndash;C', 'All three are the same length'],
         y=['The more pairs two atoms share, the shorter and stronger the bond, so triple is shortest and single is longest.',
            'This is longest to shortest. More shared pairs pull the atoms closer together.',
            'The triple bond shares the most pairs, so it should come first.',
            'Bond length depends on how many pairs are shared, so these differ.'],
         h='More shared electrons pull the two nuclei closer. Which bond shares the most?',
         w='Bond length decreases as shared pairs increase: <b>C&equiv;C (shortest), then C=C, then C&ndash;C (longest)</b>.'),
    dict(t='ch06-lewis', d=2, k=0,
         q='A student draws formaldehyde, CH' + S(2) + 'O, with C bonded to two H atoms and joined to O by a single bond. Using HONC, what is wrong with this drawing?',
         c=['C has 3 bonds and O has 1, so C and O need a double bond',
            'Each H has 1 bond, so each H needs a second bond',
            'O has 1 bond, so O needs three more bonds to C',
            'C has too many bonds, so one C&ndash;H bond must go'],
         y=['HONC calls for C to have 4 bonds and O to have 2. Making the C&ndash;O bond double fixes both atoms at once.',
            'Hydrogen needs only a duet, so 1 bond is correct.',
            'Oxygen usually forms 2 bonds, not 4. It needs only one more.',
            'C has 3 bonds here, which is one too few, not too many.'],
         h='Count the bonds on each atom and compare with HONC 1-2-3-4.',
         w='C has 2 + 1 = 3 bonds (needs 4), and O has 1 (needs 2). <b>A C=O double bond</b> gives C 4 bonds and O 2 bonds.'),
]

CH07 = [
    dict(t='ch07-equations', d=1, k=0,
         q='Fertilizer plants make ammonia from nitrogen and hydrogen. Balance: N' + S(2) + '(g) + H' + S(2) + '(g) &rarr; NH' + S(3) + '(g). What are the coefficients, in order?',
         c=['1, 3, 2', '1, 1, 2', '1, 3, 1', '2, 6, 4'],
         y=['2 NH' + S(3) + ' balances N (2 on each side) and has 6 H, so 3 H' + S(2) + ' are needed.',
            'N balances, but the right side has 6 H and the left has only 2.',
            'Neither element balances: 1 NH' + S(3) + ' has 1 N and 3 H, against 2 N and 6 H on the left.',
            'This balances, but every coefficient can be divided by 2. Use the lowest whole numbers.'],
         h='Balance N first. Then count the H atoms on the right.',
         w='N' + S(2) + '(g) + 3 H' + S(2) + '(g) &rarr; 2 NH' + S(3) + '(g): N 2 = 2, H 6 = 6. The coefficients are <b>1, 3, 2</b>.'),
    dict(t='ch07-equations', d=3, k=0,
         q='Balance, keeping the polyatomic ions as units: Ca(NO' + S(3) + ')' + S(2) + '(aq) + Na' + S(3) + 'PO' + S(4) + '(aq) &rarr; Ca' + S(3) + '(PO' + S(4) + ')' + S(2) + '(s) + NaNO' + S(3) + '(aq). What are the coefficients, in order?',
         c=['3, 2, 1, 6', '3, 2, 1, 3', '1, 2, 1, 6', '6, 4, 2, 12'],
         y=['3 Ca and 2 PO' + S(4) + ' on the right call for 3 Ca(NO' + S(3) + ')' + S(2) + ' and 2 Na' + S(3) + 'PO' + S(4) + ', which give 6 Na and 6 NO' + S(3) + '.',
            'Ca and PO' + S(4) + ' balance, but the left has 6 Na and 6 NO' + S(3) + ' while the right has only 3 of each.',
            'The right side has 3 Ca, so the left needs 3 Ca(NO' + S(3) + ')' + S(2) + ', not 1.',
            'This balances, but every coefficient can be divided by 2. Use the lowest whole numbers.'],
         h='Start with Ca' + S(3) + '(PO' + S(4) + ')' + S(2) + ' and count Ca and PO' + S(4) + ' as units. NO' + S(3) + ' stays together too.',
         w='3 Ca(NO' + S(3) + ')' + S(2) + '(aq) + 2 Na' + S(3) + 'PO' + S(4) + '(aq) &rarr; Ca' + S(3) + '(PO' + S(4) + ')' + S(2) + '(s) + 6 NaNO' + S(3) + '(aq): Ca 3, PO' + S(4) + ' 2, Na 6, NO' + S(3) + ' 6. The coefficients are <b>3, 2, 1, 6</b>.'),
    dict(t='ch07-equations', d=3, k=0,
         q='Ethanol in fuel burns completely: C' + S(2) + 'H' + S(5) + 'OH(l) + O' + S(2) + '(g) &rarr; CO' + S(2) + '(g) + H' + S(2) + 'O(g). In the balanced equation with the lowest whole numbers, what is the coefficient of O' + S(2) + '?',
         c=['3', '3.5', '7', '6'],
         y=['2 CO' + S(2) + ' and 3 H' + S(2) + 'O have 7 O atoms. Ethanol supplies 1, so O' + S(2) + ' supplies 6 atoms: 3 O' + S(2) + '.',
            'This forgets the O atom already in ethanol, and coefficients must be whole numbers.',
            'This forgets the O atom in ethanol and then doubles. Subtract that atom before dividing by 2.',
            'This is the number of O atoms that must come from O' + S(2) + '. Each O' + S(2) + ' supplies 2 atoms.'],
         h='Balance C, then H, then O. Remember that ethanol already contains one O atom.',
         w='C' + S(2) + 'H' + S(5) + 'OH(l) + 3 O' + S(2) + '(g) &rarr; 2 CO' + S(2) + '(g) + 3 H' + S(2) + 'O(g): C 2, H 6, O 7 = 7. The coefficient of O' + S(2) + ' is <b>3</b>.'),
    dict(t='ch07-equations', d=2, k=0,
         q='A thin oxide layer protects aluminum foil. Balance: Al(s) + O' + S(2) + '(g) &rarr; Al' + S(2) + 'O' + S(3) + '(s). What are the coefficients, in order?',
         c=['4, 3, 2', '2, 3, 1', '4, 3, 1', '8, 6, 4'],
         y=['O is 2 on the left and 3 on the right, so "even the odds" with 2 Al' + S(2) + 'O' + S(3) + ' (6 O). Then 3 O' + S(2) + ' and 4 Al balance.',
            'Al balances, but the left has 6 O and the right has only 3.',
            'O does not balance (6 and 3), and Al does not either (4 and 2).',
            'This balances, but every coefficient can be divided by 2. Use the lowest whole numbers.'],
         h='Oxygen comes in 2s on one side and 3s on the other. Find a number both divide into.',
         w='4 Al(s) + 3 O' + S(2) + '(g) &rarr; 2 Al' + S(2) + 'O' + S(3) + '(s): Al 4 = 4, O 6 = 6. The coefficients are <b>4, 3, 2</b>.'),
]


def add(path, prefix, new):
    B = json.load(open(path))
    assert not any(q['q'] == n['q'] for q in B for n in new), 'already added'
    start = len(B) + 1
    assert B[-1]['id'] == '%s-%03d' % (prefix, len(B))
    out = []
    for i, n in enumerate(new):
        q = {'id': '%s-%03d' % (prefix, start + i), 't': n['t'], 'q': n['q'], 'c': n['c'], 'y': n['y'], 'h': n['h'], 'w': n['w'], 'd': n['d'], 'k': n['k']}
        assert len(q['c']) == 4 == len(q['y']) and len(set(q['c'])) == 4
        out.append(q)
    raw = open(path).read()
    json.dump(B + out, open(path, 'w'), ensure_ascii=False, indent=None if '\n' not in raw.strip() else 1)
    if raw.endswith('\n'):
        open(path, 'a').write('\n')
    return [q['id'] for q in out]


rng = lambda p, a, b: ['%s-%03d' % (p, i) for i in range(a, b + 1)]
n1 = add('bank/ch01.json', 'c1', CH01)
n6 = add('bank/ch06.json', 'c6', CH06)
n7 = add('bank/ch07.json', 'c7', CH07)
PAGES = {
    'drafts/ch01/1.9_density.html': ('t=ch01-density&amp;n=6&amp;title=Density', rng('c1', 55, 65), 6, 'Density'),
    'drafts/ch01/1.9.1_density_conversion.html': ('t=ch01-density&amp;n=6&amp;title=Density', n1, 8, 'Density+as+a+conversion+factor'),
    'drafts/ch06/6.2_covalent_bonds.html': ('t=ch06-lewis&amp;n=8&amp;title=Covalent+bonds&amp;game=lewis', ['c6-017', 'c6-022'] + n6, 7, 'Covalent+bonds&amp;game=lewis'),
    'drafts/ch06/6.3_lewis_structures.html': ('t=ch06-lewis&amp;n=10&amp;title=Lewis+structures&amp;game=lewis', rng('c6', 10, 16) + rng('c6', 18, 21), 10, 'Lewis+structures&amp;game=lewis'),
    'drafts/ch07/7.1_chemical_equations.html': ('t=ch07-equations&amp;n=8&amp;title=Chemical+equations&amp;game=reactions', rng('c7', 1, 6), 6, 'Chemical+equations&amp;game=reactions'),
    'drafts/ch07/7.2_balancing.html': ('t=ch07-equations&amp;n=10&amp;title=Balancing+equations&amp;game=reactions', rng('c7', 7, 12) + n7, 10, 'Balancing+equations&amp;game=reactions'),
}
swaps = {}
for f, (old, ids, n, title) in PAGES.items():
    s = open(f).read()
    assert s.count('practice.html?' + old) == 2, f
    new = 'ids=%s&amp;n=%d&amp;title=%s' % (','.join(ids), n, title)
    open(f, 'w').write(s.replace('practice.html?' + old, 'practice.html?' + new))
    swaps[f] = ['practice.html?' + old, 'practice.html?' + new]
json.dump(swaps, open('audit/TRYIT_PAGE_SWAPS_2026-11-20.json', 'w'), indent=1)
print('added', len(n1), len(n6), len(n7))
