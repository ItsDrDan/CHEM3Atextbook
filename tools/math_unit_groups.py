#!/usr/bin/env python3
"""Keep numbers with their units when MathJax wraps (2026-11-19, iPhone Safari check).
LibreTexts' MathJax 4 wraps long equations on phones and may break at the space in "36.7\;\\text{L}", leaving the unit
alone on the next line. Wrapping each number-unit pair in braces, {36.7\;\\text{L}}, makes it one unbreakable group.
Speech and print are unchanged. Idempotent (an already-braced pair is not matched). usage: math_unit_groups.py [--dry]"""
import re, os, sys, glob
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(R)
B = r'\x5c'   # a literal backslash in the regex
NUM = r'-?\d[\d.]*(?:\{,\}\d+)*(?:\s*' + B + r'times\s*10\^(?:\{-?\d+\}|\d))?'
PAIR = re.compile(r'(?<![{}\w.,^\-])(' + NUM + B + ';' + B + r'(?:text|mathrm)\{[^{}]+\})')
dry = '--dry' in sys.argv; total = 0; pages = 0
for f in sorted(glob.glob('drafts/**/*.html', recursive=True)):
    s = open(f).read()
    out, n = PAIR.subn(r'{\1}', s)
    if n:
        total += n; pages += 1
        assert out.count('{') - s.count('{') == n and out.count('}') - s.count('}') == n
        if not dry: open(f, 'w').write(out)
print(('would group' if dry else 'grouped'), total, 'number-unit pairs on', pages, 'pages')
