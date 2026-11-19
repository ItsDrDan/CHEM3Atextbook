#!/usr/bin/env python3
"""Third OpenStax figure batch (2026-11-19): Chapters 3-9 and 13. Same pattern as add_openstax_figs_2.py, but the figure
list comes from audit/figures/batch3_*.json (written to audit/figures/BATCH3_BRIEF.md and reviewed before use).
Images from the LibreTexts copy of OpenStax Chemistry 2e (CC BY 4.0) in figures/openstax/; our own alt text and captions;
credit with a source link; the OpenStax sentence added to the page's Attribution box; captions renumbered. Idempotent.
usage: python3 tools/add_openstax_figs_3.py [--dry]"""
import re, os, sys, json, glob
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(R)
BASE = 'https://itsdrdan.github.io/CHEM3Atextbook/figures/openstax/'
OS = 'https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)/'
ATTR = (' Figures marked &ldquo;From OpenStax&rdquo; are from <a href="https://chem.libretexts.org/Bookshelves/General_Chemistry/'
        'Chemistry_2e_(OpenStax)" target="_blank" rel="noopener">OpenStax, <i>Chemistry 2e</i></a> (CC BY 4.0), with the credits given in each caption.')
dry = '--dry' in sys.argv

def credit(sec, path, extra=''):
    e = f'; {extra}' if extra else ''
    return f'(From <a href="{OS}{path}" target="_blank" rel="noopener">OpenStax, <i>Chemistry 2e</i>, Section {sec}</a>, CC BY 4.0{e}.)'

def block(img, alt, cap, cred):
    assert '<' not in alt and '>' not in alt and '"' not in alt, ('alt text must be plain text without quotes', img)
    return (f'<figure class="figure"><img src="{BASE}{img}" alt="{alt}" style="max-width:100%;height:auto;" />\n'
            f'<figcaption>Figure \\(\\PageIndex{{0}}\\): {cap} {cred}</figcaption></figure>\n')

FIGS = []
for f in sorted(glob.glob('audit/figures/batch3_*.json')):
    FIGS += json.load(open(f))

touched = []
for F in FIGS:
    page, key, where, img = F['page'], F['key'], F['where'], F['img']
    assert os.path.exists(f'figures/openstax/{img}'), img
    p = os.path.join('drafts', page); s = open(p).read()
    if BASE + img in s: continue
    assert s.count(key) == 1, (page, key, s.count(key)); i = s.find(key)
    if where == 'after':
        cands = [(s.find(t, i), t) for t in ('</p>', '</ul>', '</ol>') if s.find(t, i) >= 0]; k, t = min(cands); ins = k + len(t) + 1
    elif where == 'afterbox':
        k = s.find('</div>', i); ins = s.find('\n', k) + 1
    elif where == 'afterfig':
        k = s.find('</figure>', i); ins = s.find('\n', k) + 1
    else:
        raise ValueError(where)
    pre = s[:ins]
    assert pre.count('<div') == pre.count('</div>'), ('figure would land inside a box', page, img)
    lead = F.get('lead', '').strip()
    s = pre + lead + ('\n' if lead else '') + block(img, F['alt'], F['caption'], credit(F['credit_section'], F['credit_path'], F.get('credit_extra', ''))) + s[ins:]
    if ATTR.strip() not in s:
        a = s.find('<p class="boxtitle">Attribution</p>'); assert a >= 0, page
        j = s.find('</p>', a + 40); s = s[:j] + ATTR + s[j:]
    if not dry: open(p, 'w').write(s)
    touched.append(p); print('added', img, 'to', page)

for p in sorted(set(touched)):
    if dry: break
    s = open(p).read(); n = [0]
    def num(m):
        n[0] += 1; return f'<figcaption>Figure \\(\\PageIndex{{{n[0]}}}\\):'
    s = re.sub(r'<figcaption>Figure \\\(\\PageIndex\{\d+\}\\\):', num, s); open(p, 'w').write(s)
    print(os.path.basename(p), n[0], 'figures')
