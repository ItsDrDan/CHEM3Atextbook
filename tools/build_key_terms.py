#!/usr/bin/env python3
"""Key Equations and Key Terms for each Chapter Guide (2026-11-19).

Key Terms come from backmatter/glossary_3A.json (the same source as the Glossary), in the order they are taught, each
linked back to its section. Key Equations are written below (Chapters 1-3, 5, 6, 8-14; Chapters 4 and 7 have none).
Both go after Key Ideas and before Video Lessons. Idempotent: an existing Key Equations / Key Terms block is replaced.
usage: python3 tools/build_key_terms.py [chNN ...]"""
import json, os, re, sys, glob, html
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(R)

src = open('backmatter/build_backmatter.py').read()
ns = {}; exec(src[src.index('IDS = {'):src.index('\n\n', src.index("'14.10'"))], ns); IDS = ns['IDS']
GO = 'https://chem.libretexts.org/@go/page/'

def m(tex): return f'\\( {tex} \\)'
# (equation HTML, what it is for, section)
EQ = {
 1: [(m(r"A \times 10^{n}") + ', with 1 &le; A &lt; 10', 'Write very large or very small numbers in scientific notation', '1.2.1'),
     ('1 mL = 1 cm<sup>3</sup>; 1 L = 1000 mL', 'Switch between volume units (exact)', '1.2.2'),
     (m(r'\text{given} \times \dfrac{\text{desired unit}}{\text{given unit}} = \text{desired}'), 'Set up any unit conversion (dimensional analysis)', '1.4.1'),
     ('1 m<sup>3</sup> = (100 cm)<sup>3</sup> = 10<sup>6</sup> cm<sup>3</sup>', 'Convert squared or cubed units: square or cube the whole factor', '1.4.3'),
     ('34.0% N = 34.0 g N / 100 g fertilizer', 'Use a percent as a conversion factor ("out of 100")', '1.4.5'),
     (m(r'd = \dfrac{m}{V}'), 'Find density, or use it to convert between mass and volume', '1.9'),
     (m(r'V = V_{\text{final}} - V_{\text{initial}}'), 'Find the volume of an irregular solid by water displacement', '1.9')],
 2: [('A = protons + neutrons', 'Find the mass number', '2.5'),
     ('neutrons = A &minus; Z', 'Count neutrons from the mass number and atomic number', '2.5'),
     ('charge = protons &minus; electrons', 'Find the charge of an ion, or its electron count', '2.4'),
     (m(r'\text{average atomic mass} = \sum \left(\dfrac{\%}{100} \times \text{isotope mass}\right)'), 'Calculate an average atomic mass from isotope abundances', '2.6')],
 3: [(m(r'c = \lambda \nu'), 'Convert between wavelength and frequency', '3.1'),
     (m(r'E = h\nu = \dfrac{hc}{\lambda}'), 'Find the energy of one photon', '3.1'),
     (m(r'c = 3.00 \times 10^{8}\;\text{m s}^{-1}') + '; ' + m(r'h = 6.626 \times 10^{-34}\;\text{J s}'), 'Constants for light problems (convert nm to m first)', '3.1'),
     (m(r'\Delta E = \dfrac{hc}{\lambda}'), 'Relate an energy-level gap to the wavelength of light emitted or absorbed', '3.2'),
     ('s 2, p 6, d 10, f 14 electrons', 'Maximum electrons in each kind of subshell (2 per orbital)', '3.3')],
 5: [(m(r'1\;\text{mol} = 6.0221 \times 10^{23}\;\text{particles}'), "Avogadro's number: convert between moles and particles", '5.1'),
     ('molar mass (g/mol) = sum of the atomic masses in the formula', 'Find the molar mass of a compound', '5.2'),
     (m(r'\text{moles} = \dfrac{\text{grams}}{\text{molar mass}}'), 'Convert grams to moles (multiply to go back)', '5.3'),
     ('1 mmol = 10<sup>&minus;3</sup> mol', 'Switch between millimoles and moles', '5.3'),
     ('1 mol CO<sub>2</sub> : 1 mol C : 2 mol O', 'Use subscripts as exact mole ratios inside a formula', '5.4')],
 6: [(m(r'\text{mass percent} = \dfrac{\text{mass of part}}{\text{mass of whole}} \times 100\%'), 'Find the percent composition of a compound', '6.6'),
     (m(r'n = \dfrac{\text{molar mass}}{\text{empirical formula mass}}'), 'Find how many empirical units make the molecular formula', '6.7'),
     ('molecular formula = n &times; empirical formula', 'Scale the empirical formula up (n is a whole number)', '6.7'),
     (m(r'\Delta\text{EN} = \text{EN}_{\text{higher}} - \text{EN}_{\text{lower}}'), 'Classify a bond: 0&ndash;0.4 nonpolar, above 0.4 to 2.0 polar covalent, above 2.0 ionic', '6.5')],
 8: [(m(r'\text{mol A} \times \dfrac{\text{mol B}}{\text{mol A}} = \text{mol B}'), 'Use the coefficients as a mole ratio', '8.1'),
     ('grams A &rarr; mol A &rarr; mol B &rarr; grams B', 'The stoichiometry road map: always go through moles', '8.2'),
     ('mol = M &times; L', 'Moles from a solution volume and molarity', '8.3'),
     ('1 mol gas = 22.4 L at STP (0 &deg;C, 1 atm)', 'Moles from a gas volume at STP', '8.3'),
     ('leftover = initial &minus; used', 'Find how much excess reactant remains', '8.4'),
     (m(r'\text{percent yield} = \dfrac{\text{actual yield}}{\text{theoretical yield}} \times 100\%'), 'Compare what you made with the most you could make', '8.5'),
     ('&Delta;H &lt; 0 exothermic; &Delta;H &gt; 0 endothermic', 'Read the sign of a reaction enthalpy; &Delta;H goes with the moles as written', '8.6')],
 9: [('K = &deg;C + 273.15', 'Convert Celsius to kelvins (exact)', '9.2'),
     (m(r'^{\circ}\text{C} = \dfrac{^{\circ}\text{F} - 32}{1.8}') + '; ' + m(r'^{\circ}\text{F} = 1.8(^{\circ}\text{C}) + 32'), 'Convert between Fahrenheit and Celsius (exact constants)', '9.2'),
     ('1 cal = 4.184 J; 1 Cal = 1 kcal = 1000 cal', 'Convert energy units; a food Calorie is a kilocalorie', '9.3'),
     (m(r'q = mc\Delta T') + ', with ' + m(r'\Delta T = T_{\text{final}} - T_{\text{initial}}'), 'Heat to change the temperature of a sample (a slope on a heating curve)', '9.4'),
     ('c (water) = 4.184 J/(g&middot;&deg;C); ice 2.09; steam 2.01', 'Specific heats for water problems', '9.4'),
     (m(r'q_{\text{lost}} = -q_{\text{gained}}') + '; ' + m(r'q_{\text{reaction}} = -q_{\text{solution}}'), 'Calorimetry: heat lost by one part is gained by the other', '9.4'),
     (m(r'q = n\Delta H'), 'Heat for a phase change (a plateau on a heating curve)', '9.5'),
     (m(r'\Delta H_{\text{fus}} = 6.02\;\text{kJ/mol}') + '; ' + m(r'\Delta H_{\text{vap}} = 40.7\;\text{kJ/mol}'), 'Melting and boiling water', '9.5')],
 10: [('1 atm = 760 mmHg = 760 torr = 101.325 kPa = 14.7 psi', 'Convert pressure units', '10.2'),
      (m(r'P_1 V_1 = P_2 V_2'), "Boyle's law: pressure and volume (inverse)", '10.3'),
      (m(r'\dfrac{V_1}{T_1} = \dfrac{V_2}{T_2}'), "Charles's law: volume and temperature (direct; kelvins)", '10.3'),
      (m(r'\dfrac{P_1}{T_1} = \dfrac{P_2}{T_2}'), "Gay-Lussac's law: pressure and temperature (direct; kelvins)", '10.3'),
      (m(r'\dfrac{V_1}{n_1} = \dfrac{V_2}{n_2}'), "Avogadro's law: volume and moles (direct)", '10.3'),
      (m(r'\dfrac{P_1 V_1}{n_1 T_1} = \dfrac{P_2 V_2}{n_2 T_2}'), 'Combined gas law: cross out whatever stays constant', '10.3'),
      (m(r'PV = nRT') + ', ' + m(r'R = 0.082058\;\text{L atm mol}^{-1}\;\text{K}^{-1}'), 'Ideal gas law: one gas in one state', '10.4'),
      ('1 mol = 22.4 L at STP (273 K, 1 atm)', 'Molar volume of a gas at STP', '10.4'),
      ('molar mass M = m/n; density d = m/V', 'Molar mass (grams per mole) and density of a gas', '10.4'),
      (m(r'P_{\text{total}} = P_1 + P_2 + \cdots') + '; ' + m(r'P_i = X_i P_{\text{total}}'), "Dalton's law of partial pressures", '10.6'),
      (m(r'P_{\text{gas}} = P_{\text{atm}} - P_{\text{H}_2\text{O}}'), 'Pressure of a gas collected over water', '10.6')],
 11: [(m(r'\%(\text{m/m}) = \dfrac{\text{g solute}}{\text{g solution}} \times 100\%'), 'Mass percent of a solution', '11.3'),
      (m(r'\%(\text{m/v}) = \dfrac{\text{g solute}}{\text{mL solution}} \times 100\%'), 'Mass/volume percent (0.9% NaCl is 0.9 g per 100 mL)', '11.3'),
      ('1 ppm &asymp; 1 mg/L (in water)', 'Very dilute solutions', '11.3'),
      (m(r'M = \dfrac{\text{mol solute}}{\text{L solution}}') + '; 1 M = 1000 mM', 'Molarity', '11.3'),
      ('[ion] = (ions per formula unit) &times; [compound]', 'Ion concentration from a dissolved salt', '11.4'),
      (m(r'M_1 V_1 = M_2 V_2'), 'Dilution (moles stay the same; V<sub>2</sub> is the total volume)', '11.4'),
      ('V &times; M &rarr; mol &rarr; mole ratio &rarr; mol &rarr; V, M, or g', 'Solution stoichiometry and titration', '11.5'),
      (m(r'm = \dfrac{\text{mol solute}}{\text{kg solvent}}') + '; osmolality = i &times; m', 'Molality and particle concentration', '11.6'),
      (m(r'\Delta T_f = i K_f m') + '; ' + m(r'\Delta T_b = i K_b m'), 'Freezing-point drop and boiling-point rise; for water ' + m(r'K_f = 1.86') + ' and ' + m(r'K_b = 0.512\;^{\circ}\text{C kg mol}^{-1}'), '11.6')],
 12: [(m(r'K_w = [\text{H}_3\text{O}^+][\text{OH}^-] = 1.0 \times 10^{-14}'), 'Find [H<sub>3</sub>O<sup>+</sup>] from [OH<sup>&minus;</sup>], or the reverse (25 &deg;C)', '12.4'),
      (m(r'\text{pH} = -\log[\text{H}_3\text{O}^+]') + '; ' + m(r'[\text{H}_3\text{O}^+] = 10^{-\text{pH}}'), 'Convert between pH and hydronium concentration', '12.5'),
      (m(r'\text{pOH} = -\log[\text{OH}^-]'), 'The same idea for hydroxide', '12.5'),
      ('pH + pOH = 14.00', 'Move between the two scales', '12.5'),
      ('decimal places in pH = significant figures in the concentration', 'Round a pH correctly', '12.5')],
 13: [(m(r'K = \dfrac{[\text{products}]^{\text{coefficients}}}{[\text{reactants}]^{\text{coefficients}}}'), 'Write an equilibrium constant expression (leave out pure solids and liquids)', '13.3'),
      (m(r'K_{\text{reverse}} = \dfrac{1}{K_{\text{forward}}}'), 'K for the reaction written backward', '13.3'),
      ('K &gt; 1 favors products; K &lt; 1 favors reactants', 'Read what a K value means', '13.3')],
 14: [('alpha ' + m(r'^{4}_{2}\text{He}') + '; beta ' + m(r'^{0}_{-1}\text{e}') + '; positron ' + m(r'^{0}_{+1}\text{e}') + '; gamma ' + m(r'^{0}_{0}\gamma'), 'Particles in nuclear equations (mass numbers and atomic numbers each balance)', '14.2'),
      ('1 Bq = 1 decay/s', 'Units of activity', '14.1'),
      (m(r'n = \dfrac{\text{time}}{\text{half-life}}'), 'Count the half-lives that have passed (a whole number in this course)', '14.3'),
      (m(r'\text{amount left} = \text{initial} \times \left(\tfrac{1}{2}\right)^{n}'), 'Find how much is left after n half-lives', '14.3'),
      ('age = n &times; 5730 years', 'Radiocarbon dating (carbon-14 half-life 5730 years)', '14.4'),
      (m(r'E = mc^{2}'), 'Mass lost in fission or fusion becomes energy', '14.5')],
}

def table(cap, heads, rows):
    th = ''.join(f'<th scope="col">{h}</th>' for h in heads)
    body = '\n'.join('<tr>' + ''.join(f'<td data-th="{h}">{c}</td>' for h, c in zip(heads, r)) + '</tr>' for r in rows)
    return (f'<table class="mt-responsive-table">\n<caption>{cap}</caption>\n<thead><tr>{th}</tr></thead>\n<tbody>\n{body}\n</tbody>\n</table>\n')

def link(sec): return f'<a href="{GO}{IDS[sec]}">{sec}</a>'

G = json.load(open('backmatter/glossary_3A.json'))
def secnum(s): return [int(x) for x in s.split('.')]

def block(ch):
    out = ''
    if ch in EQ:
        def brk(e):   # one equation per line on phones, with room between stacked fractions
            parts = re.split(r'(?<=\\\))\s*[;,]\s*(?=(?:with |alpha |beta |positron |gamma )?\\\(|1 M|osmolality)', e)
            return parts[0] if len(parts) == 1 else ''.join(f'<span style="display:block;margin:0.4em 0;">{x}</span>' for x in parts)
        # a scroll box keeps a long equation from widening the page at 320 px (WCAG 1.4.10; the book's phone rule for long math)
        sc = lambda e: f'<div style="overflow-x:auto;overflow-y:hidden;">{e}</div>'
        rows = [(sc(brk(e)), u, link(s)) for e, u, s in sorted(EQ[ch], key=lambda r: secnum(r[2]))]
        out += ('<h2>Key Equations</h2>\n<p>The equations, constants, and equalities this chapter uses, with the section that teaches each one. '
                'Your yellow sheet has the constants on exams.</p>\n' + table(f'Key equations for Chapter {ch}', ['Equation', 'Use it to', 'Section'], rows))
    terms = sorted([g for g in G if g['section'].split('.')[0] == str(ch)], key=lambda g: secnum(g['section']))
    rows = []
    for g in terms:
        t = f'<strong>{g["term"]}</strong>'
        syn = [x for x in g.get('synonyms', []) if len(x) > 1]; sym = [x for x in g.get('synonyms', []) if len(x) == 1]
        bits = (['also ' + ', '.join(syn)] if syn else []) + (['symbol ' + ', '.join(sym)] if sym else [])
        if bits: t += ' (' + '; '.join(bits) + ')'
        d = g['definition'] + (' <i>(Going Further)</i>' if g.get('going_further') else '')
        rows.append((t, d, link(g['section'])))
    out += ('<h2>Key Terms</h2>\n<p>The terms this chapter defines, in the order they are taught. Each section number links back to where the term is explained; '
            'the Glossary at the end of the book lists every term from A to Z.</p>\n' + table(f'Key terms for Chapter {ch}', ['Term', 'Meaning', 'Section'], rows))
    return out

chs = [int(a[2:]) for a in sys.argv[1:]] or list(range(1, 15))
for ch in chs:
    f = glob.glob(f'drafts/ch{ch:02d}/*chapter_guide.html')[0]; s = open(f).read()
    s = re.sub(r'<h2>Key Equations</h2>.*?(?=<h2>Video Lessons</h2>)|<h2>Key Terms</h2>.*?(?=<h2>Video Lessons</h2>)', '', s, flags=re.S)
    i = s.index('<h2>Video Lessons</h2>'); s = s[:i] + block(ch) + '\n' + s[i:]
    assert s.count('\\(') == s.count('\\)')
    open(f, 'w').write(s)
    print(f, 'equations', len(EQ.get(ch, [])), 'terms', sum(1 for g in G if g['section'].split('.')[0] == str(ch)))
