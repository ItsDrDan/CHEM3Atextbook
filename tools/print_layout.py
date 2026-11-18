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
    return len(re.sub(r'<[^>]+>|\\\(.*?\\\)', '', seg).strip())
dry = '--dry' in sys.argv; files = [f for f in sys.argv[1:] if f != '--dry'] or sorted(glob.glob('drafts/**/*.html', recursive=True))
for f in files:
    s = open(f).read(); o = s
    if OLD in s: s = s.replace(OLD, NEW)
    for m in reversed(list(re.finditer(r'<figure class="figure">\s*<img src="([^"]+)"', s))):
        a = aspect(m.group(1)); t = following_text(s, m.start())
        if a and a < 1.3 and not boxed(s, m.start()) and t >= 200:
            s = s[:m.start()] + '<figure class="figure fig-wrap">' + s[m.start() + len('<figure class="figure">'):]
            print(f'wrap {os.path.basename(f)} {os.path.basename(m.group(1))} aspect {a:.2f} text {t}')
    if s != o and not dry: open(f, 'w').write(s)
