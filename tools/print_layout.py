#!/usr/bin/env python3
"""Print layout (2026-11-18): one print-only <style> line at the top of each exercise page, and class="figure fig-wrap" on
figures that are about as tall as they are wide (aspect < 1.3), sit outside boxes, and are followed by running text, so
that in the PDF the text wraps beside them. Screen layout is unchanged. Idempotent. usage: print_layout.py [--dry] [files]"""
import re, os, sys, glob, subprocess
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(R)
OLD = '<style type="text/css">@media print { details > summary { display:block; page-break-after:avoid; break-after:avoid; } }</style>'
NEW = ('<style type="text/css">@media print { details > summary { display:block; page-break-after:avoid; break-after:avoid; } '
       'details:has(+ details) { page-break-inside:avoid; break-inside:avoid; } '
       'figure.figure { float:top unless-fit; } '
       'figure.fig-wrap { float:right; width:46%; margin:0.3em 0 0.8em 1.4em; } figure.fig-wrap img { width:100%; height:auto; } '
       'h2, h3, h4, table, div[class^=box] { clear:both; } div[class^=box] figure, li figure { float:none; } }</style>')
# 2026-11-19 (iPhone Safari check): LibreTexts makes <summary> display inline, which hides the disclosure arrow in every
# browser, so Hint/Answer looked like plain 14 px words. SCREEN turns them into 44 px outlined buttons with a ▸/▾ arrow
# (the arrow is hidden from screen readers by the "/ ''" alt text). It also gives equation paragraphs more line height on
# phones, because MathJax 4 wraps long equations there and stacked fractions on adjacent lines touched.
# SCREEN sits just before the print style, which must stay last.
SCREEN = ('<style type="text/css">@media screen { '
          '.mt-content-container details > summary { display:inline-flex; align-items:center; gap:0.45em; list-style:none; '
          'min-height:44px; box-sizing:border-box; padding:0 1em; margin:0.35em 0; border:1.5px solid #2f6f9f; border-radius:8px; '
          'background:#fff; color:#1d4f7a; font-weight:600; font-size:1rem; line-height:1.2; cursor:pointer; } '
          '.mt-content-container details > summary::-webkit-details-marker { display:none; } '
          '.mt-content-container details > summary::before { content:"▸"; content:"▸" / ""; font-size:1.1em; } '
          '.mt-content-container details[open] > summary::before { content:"▾"; content:"▾" / ""; } '
          '.mt-content-container details[open] > summary { background:#e3eef8; } '
          '.mt-content-container details > summary:focus-visible { outline:3px solid #1d4f7a; outline-offset:2px; } } '
          '@media screen and (max-width: 40em) { .mt-content-container p[style*="overflow-x:auto"] { line-height:2.6; } }</style>')
EQ_P = 'text-align:center;overflow-x:auto;overflow-y:hidden;'
def aspect(src):
    loc = src.split('github.io/CHEM3Atextbook/')[-1]
    if not os.path.exists(loc): return None
    if loc.endswith('.svg'):
        v = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', open(loc).read()[:3000]); return float(v.group(1)) / float(v.group(2))
    o = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', loc], capture_output=True, text=True).stdout
    return int(re.search(r'pixelWidth: (\d+)', o).group(1)) / int(re.search(r'pixelHeight: (\d+)', o).group(1))
def boxed(s, i):   # inside an open <div class="box...">?
    pre = s[:i]; return pre.count('<div') > pre.count('</div>')
def following_text(s, i):
    j = s.find('</figure>', i) + 9; m = re.search(r'<(h[2-4]|div|table|figure|details)\b', s[j:]); seg = s[j:j + (m.start() if m else len(s))]
    if m and m.group(1) == 'figure': return 0   # another figure follows: wrapping would put it beside the float
    return len(re.sub(r'<[^>]+>|\\\(.*?\\\)', '', seg).strip())
dry = '--dry' in sys.argv; files = [f for f in sys.argv[1:] if f != '--dry'] or sorted(glob.glob('drafts/**/*.html', recursive=True))
for f in files:
    s = open(f).read(); o = s
    if OLD in s: s = s.replace(OLD, NEW)
    # 2026-11-19: the style must sit at the END of the page. With it first, an OpenStax photo on the page made
    # LibreTexts' PDF engine ignore it (test on 3.1/6.5/7.8, Full (35)).
    if NEW in s and not s.rstrip().endswith(NEW):
        s = s.replace(NEW + '\n', '', 1).replace(NEW, '', 1).rstrip('\n') + '\n' + NEW + '\n'
    if NEW in s or EQ_P in s:   # SCREEN once, directly before the print style (or last on pages without one)
        s = s.replace(SCREEN + '\n', '').replace(SCREEN, '')
        if NEW in s: s = s.replace(NEW, SCREEN + '\n' + NEW, 1)
        else: s = s.rstrip('\n') + '\n' + SCREEN + '\n'
    for m in reversed(list(re.finditer(r'<figure class="figure">\s*<img src="([^"]+)"', s))):
        a = aspect(m.group(1)); t = following_text(s, m.start())
        if a and a < 1.3 and not boxed(s, m.start()) and t >= 200:
            s = s[:m.start()] + '<figure class="figure fig-wrap">' + s[m.start() + len('<figure class="figure">'):]
            print(f'wrap {os.path.basename(f)} {os.path.basename(m.group(1))} aspect {a:.2f} text {t}')
    if s != o and not dry: open(f, 'w').write(s)
