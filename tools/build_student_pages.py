#!/usr/bin/env python3
"""Fill the placeholders in the two student pages (2026-11-19):
drafts/front/acs_final_prep.html  (__TOPICS__: every chapter's Try It mix topics; __CHECKLIST__: per-chapter must-know list)
drafts/front/how_to_use_this_book.html  (__ACS_ID__: page id of the ACS page once it exists; pass it as argv[1])
usage: python3 tools/build_student_pages.py [acs_page_id]"""
import re, glob, os, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(R)
GO = 'https://chem.libretexts.org/@go/page/'
GUIDES = {1: (597683, 'Measurement, Matter, and the Scientific Method'), 2: (597868, 'Atoms, Ions, and Isotopes'),
          3: (597884, 'Light, Electrons, and the Periodic Table'), 4: (597897, 'Naming Compounds'), 5: (597910, 'The Mole'),
          6: (597929, 'Chemical Bonds, Shapes, and Composition'), 7: (597952, 'Chemical Reactions'), 8: (597968, 'Stoichiometry'),
          9: (597988, 'Energy, Solids, and Liquids'), 10: (598005, 'Gases'), 11: (598022, 'Solutions'), 12: (598036, 'Acids and Bases'),
          13: (598049, 'Chemical Equilibrium'), 14: (598064, 'Radioactivity and Nuclear Chemistry')}
CHECK = {
 1: ['Count significant figures and round a calculated answer (fewest significant figures for &times; and &divide;; fewest decimal places for + and &minus;).',
     'Write and use scientific notation and metric prefixes.',
     'Convert units by dimensional analysis, including multistep, squared and cubed units, dosage, and percent problems.',
     'Tell accuracy from precision, classify matter, and tell physical from chemical properties and changes.',
     'Use density, d = m/V, as a conversion factor between mass and volume.'],
 2: ['Find protons, neutrons, and electrons from a symbol, mass number, and charge.',
     'Write isotope symbols, and predict common ion charges from the periodic table.',
     'Calculate an average atomic mass from isotope masses and abundances.',
     'Explain what the Dalton, Thomson, and Rutherford experiments showed.'],
 3: ['Use c = &lambda;&nu; and E = h&nu; = hc/&lambda; (convert nm to m first).',
     'Explain line spectra with electron energy levels.',
     'Write orbital diagrams and full and noble-gas electron configurations, for atoms and ions, including Cr and Cu.',
     'Count valence electrons, draw Lewis symbols, and rank atomic radius, ionization energy, and ion size.'],
 4: ['Write ionic formulas from ion charges, including polyatomic ions from the green sheet.',
     'Name ionic compounds, using Roman numerals for metals with more than one charge.',
     'Name molecular compounds with prefixes, and name acids (-ide &rarr; hydro-&hellip;-ic, -ate &rarr; -ic, -ite &rarr; -ous).',
     'Decide which naming system a compound needs.'],
 5: ['Calculate a molar mass from the yellow sheet.',
     'Convert among grams, moles, and particles (6.0221 &times; 10<sup>23</sup>); the goal is the mole.',
     'Use subscripts as mole ratios inside a formula.'],
 6: ['Tell ionic from covalent bonding, and draw Lewis structures.',
     'Predict shapes and bond angles for up to four electron groups (VSEPR).',
     'Classify bonds by &Delta;EN and decide whether a molecule is polar (SNAP).',
     'Calculate mass percent, and find empirical and molecular formulas.'],
 7: ['Balance equations and classify reactions (combination, decomposition, single and double displacement, combustion).',
     'Use the solubility rules to predict precipitates, and write net ionic equations.',
     'Recognize acid&ndash;base and gas-forming reactions.',
     'Assign oxidation numbers, find what is oxidized and reduced, and use the activity series.'],
 8: ['Use coefficients as mole ratios: grams &rarr; moles &rarr; moles &rarr; grams.',
     'Start from a solution volume (mol = M &times; L) or a gas volume at STP (22.4 L/mol).',
     'Find the limiting reactant, the leftover, the theoretical yield, and the percent yield.',
     'Use &Delta;H as a conversion factor, and tell exothermic from endothermic.'],
 9: ['Convert among &deg;F, &deg;C, and K, and between calories and joules.',
     'Use q = mc&Delta;T (including calorimetry) and q = n&Delta;H on heating and cooling curves.',
     'Identify intermolecular forces and rank boiling points and vapor pressures.',
     'Classify solids and relate forces to properties.'],
 10: ['Convert pressure units, and use the gas laws with temperatures in kelvins.',
      'Use PV = nRT, including molar mass of a gas and gas stoichiometry.',
      'Use Dalton&rsquo;s law, including a gas collected over water.',
      'Explain the gas laws with kinetic molecular theory.'],
 11: ['Predict solubility (like dissolves like) and the effects of temperature and pressure.',
      'Calculate %(m/m), %(m/v), ppm, and molarity, and do dilutions (M<sub>1</sub>V<sub>1</sub> = M<sub>2</sub>V<sub>2</sub>).',
      'Do solution stoichiometry and titration problems.',
      'Calculate molality and &Delta;T<sub>f</sub> or &Delta;T<sub>b</sub> with i, and predict the direction of osmosis.'],
 12: ['Identify Arrhenius and Br&oslash;nsted&ndash;Lowry acids and bases and conjugate pairs.',
      'Know the strong acids and strong bases (green sheet).',
      'Use K<sub>w</sub>, and calculate pH, pOH, [H<sub>3</sub>O<sup>+</sup>], and [OH<sup>&minus;</sup>] for strong acids and bases (decimal places in pH = significant figures in the concentration).',
      'Recognize a buffer and explain how it works.'],
 13: ['Explain how concentration, temperature, surface area, and a catalyst change a reaction rate.',
      'Describe dynamic equilibrium, and write K expressions (leave out pure solids and liquids).',
      'Interpret the size of K, and K for the reverse reaction.',
      'Predict Le Chatelier shifts for concentration, temperature, and volume changes (a catalyst causes no shift; only temperature changes K).'],
 14: ['Write nuclear equations for alpha, beta, positron, gamma, and electron capture, balancing mass and atomic numbers.',
      'Compare penetrating power and shielding.',
      'Solve half-life problems with whole numbers of half-lives, including carbon-14 dating.',
      'Describe fission, fusion, and the main uses of radiation in medicine.'],
}

def topics():
    T = []
    for f in sorted(glob.glob('drafts/ch*/*practice_games.html'), key=lambda x: int(re.search(r'ch(\d+)', x).group(1))):
        T += re.search(r'practice\.html\?t=([^"&]+)&amp;n=', open(f).read()).group(1).split(',')
    return ','.join(T)

def checklist():
    out = []
    for ch, (gid, title) in GUIDES.items():
        out.append(f'<h3><a href="{GO}{gid}">Chapter {ch}: {title}</a></h3>\n<ul>\n' + ''.join(f'<li>{x}</li>\n' for x in CHECK[ch]) + '</ul>')
    return '\n'.join(out)

p = 'drafts/front/acs_final_prep.html'; s = open(p).read()
if '__TOPICS__' in s or '__CHECKLIST__' in s:
    s = s.replace('__TOPICS__', topics()).replace('__CHECKLIST__', checklist()); open(p, 'w').write(s); print('filled', p)
if len(sys.argv) > 1:
    q = 'drafts/front/how_to_use_this_book.html'; t = open(q).read()
    if '__ACS_ID__' in t: open(q, 'w').write(t.replace('__ACS_ID__', sys.argv[1])); print('linked', q, '->', sys.argv[1])
