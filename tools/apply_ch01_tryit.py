#!/usr/bin/env python3
"""Point each Chapter 1 measurement page's Try It box at its own topic pool (2026-11-17) and add mixed boxes to the
section openers 1.2, 1.3 and 1.4. Idempotent: re-running replaces the same boxes."""
import re, os, sys
from urllib.parse import quote_plus
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'drafts', 'ch01')
U = 'https://itsdrdan.github.io/CHEM3Atextbook/practice.html'

# file: (keys, n, title, game, description)
BOX = {
 '1.2_taking_measurements': ('ch01-scinot,ch01-units', 8, 'Numbers and units mix', 'metric',
   'A mix from Sections 1.2.1 and 1.2.2: scientific notation, SI units, and metric prefixes.'),
 '1.2.1_scientific_notation': ('ch01-scinot', 8, 'Scientific notation', 'metric',
   'Write numbers in scientific notation, read them back, enter them on a calculator, and multiply and divide powers of ten.'),
 '1.2.2_units': ('ch01-units', 6, 'Numbers and units', 'metric', None),
 '1.3_significant_figures': ('ch01-sigfig,ch01-sigcalc,ch01-read', 8, 'Significant figures mix', 'sigfig',
   'A mix from Sections 1.3.1&ndash;1.3.3: counting significant figures, carrying them through calculations, and reading measuring tools.'),
 '1.3.1_sig_figs_precision': ('ch01-sigfig', 6, 'Significant figures', 'sigfig', None),
 '1.3.2_sig_figs_calculations': ('ch01-sigcalc', 8, 'Significant figures in calculations', 'sigfig',
   'Round, and carry significant figures through multiplication, division, addition, subtraction, and mixed steps.'),
 '1.3.3_reading_tools': ('ch01-read', 8, 'Reading measuring tools', 'sigfig',
   'Read cylinders, burets, rulers, and balances to the right number of digits.'),
 '1.4_conversions': ('ch01-convert,ch01-multistep,ch01-powers,ch01-dosage,ch01-percent', 10, 'Conversions mix', 'metric',
   'A mix from Sections 1.4.1&ndash;1.4.5: one-step and multi-step conversions, squared and cubed units, dosage, and percents.'),
 '1.4.1_unit_conversions': ('ch01-convert', 6, 'Conversions', 'metric', None),
 '1.4.2_multistep': ('ch01-multistep', 8, 'Multi-step conversions', 'metric',
   'Chain conversion factors, go through the base unit, and convert both parts of a rate.'),
 '1.4.3_units_powers': ('ch01-powers', 8, 'Units raised to a power', 'metric',
   'Convert areas and volumes by squaring or cubing the whole conversion factor.'),
 '1.4.4_word_problems_dosage': ('ch01-dosage', 8, 'Word problems and dosage', 'metric',
   'Pull the givens out of a word problem and set up dosage and rate calculations. Math practice only, not dosing guidance.'),
 '1.4.5_percents': ('ch01-percent', 8, 'Percents', 'algebra',
   'Use a percent as a conversion factor: find the part, the whole, or the percent.'),
}
MIX_OLD = 'ch01-method,ch01-units,ch01-sigfig,ch01-convert,'
MIX_NEW = 'ch01-method,ch01-units,ch01-scinot,ch01-sigfig,ch01-sigcalc,ch01-read,ch01-convert,ch01-multistep,ch01-powers,ch01-dosage,ch01-percent,'

def src(keys, n, title, game):
    return f'{U}?t={keys}&amp;n={n}&amp;title={quote_plus(title)}&amp;game={game}'

def box(keys, n, title, game, desc):
    s = src(keys, n, title, game)
    return (f'<div class="box-note" style="border-left:6px solid #86509b;">\n<p class="boxtitle">Try It: {title}</p>\n'
            f'<p>{desc} Every answer choice gives feedback.</p>\n'
            f'<p><iframe src="{s}" width="100%" height="620" style="border:0;border-radius:12px;background:#f5f6fb;" title="Try It: {title}" loading="lazy"></iframe></p>\n'
            f'<p style="font-size:0.9em;">Not loading? <a href="{s}" target="_blank" rel="noopener">Open this practice in a new tab</a>.</p>\n</div>\n')

BOXRE = re.compile(r'<div class="box-note" style="border-left:6px solid #86509b;">\s*<p class="boxtitle">Try It:.*?</div>\n', re.S)
for name, (keys, n, title, game, desc) in BOX.items():
    p = os.path.join(D, name + '.html'); s = open(p).read()
    m = BOXRE.findall(s)
    if len(m) == 1:
        old = m[0]
        if desc is None:  # keep the page's own description
            desc = re.search(r'<p>(.*?) Every answer choice gives feedback\.</p>', old).group(1)
        s = s.replace(old, box(keys, n, title, game, desc))
    elif len(m) == 0:  # section opener: add before the Video Lesson heading
        assert s.count('<h2>Video Lesson</h2>') == 1, name
        s = s.replace('<h2>Video Lesson</h2>', box(keys, n, title, game, desc) + '\n<h2>Video Lesson</h2>')
    else:
        sys.exit(name + ': more than one Try It box')
    open(p, 'w').write(s); print('ok', name)
for name in ('1.10_chapter_guide', '1.13_practice_games'):
    p = os.path.join(D, name + '.html'); s = open(p).read()
    if MIX_NEW not in s:
        assert MIX_OLD in s, name; s = s.replace(MIX_OLD, MIX_NEW); open(p, 'w').write(s)
    s = open(p).read()
    s = s.replace('t=ch01-units,ch01-sigfig,ch01-convert&amp;n=12', 't=ch01-units,ch01-scinot,ch01-sigfig,ch01-sigcalc,ch01-read,ch01-convert,ch01-multistep,ch01-powers,ch01-dosage,ch01-percent&amp;n=12')
    open(p, 'w').write(s); print('ok', name)
