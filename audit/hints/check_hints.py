#!/usr/bin/env python3
"""Check a writer's chNN_hints.json against chNN_exercises.json (same order, same ids, hint present and short,
no leaked answer, allowed HTML only)."""
import json, re, sys, os
p = sys.argv[1]; H = json.load(open(p))
E = json.load(open(p.replace('_hints.json', '_exercises.json')))
err = []
if len(H) != len(E): err.append(f'count {len(H)} != {len(E)}')
def plain(s): return re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', s)).strip()
for h, e in zip(H, E):
    tag = f"{os.path.basename(e['file'])} #{e['idx']} {e['title']}"
    if (h.get('file'), h.get('idx')) != (e['file'], e['idx']): err.append(tag + ': file/idx mismatch'); continue
    hint = h.get('hint', '')
    if not hint.strip(): err.append(tag + ': empty hint')
    if len(plain(hint).split()) > 45: err.append(tag + f': hint {len(plain(hint).split())} words')
    if e['terse_answer'] and not h.get('why', '').strip(): err.append(tag + ': terse answer needs "why"')
    for k in ('hint', 'why'):
        s = h.get(k, '') or ''
        if '\t' in s or '\r' in s: err.append(tag + f': TAB/CR in {k}')
        if re.search(r'&(?!(?:[a-zA-Z]+|#\d+);)', s): err.append(tag + f': bare & in {k}')
        for t in re.findall(r'</?([a-zA-Z0-9]+)', s):
            if t.lower() not in ('sub', 'sup', 'b', 'i'): err.append(tag + f': tag <{t}> in {k}')
        for t in ('sub', 'sup', 'b', 'i'):
            if s.count(f'<{t}>') != s.count(f'</{t}>'): err.append(tag + f': unbalanced <{t}> in {k}')
        if s.count('\\(') != s.count('\\)'): err.append(tag + f': unbalanced \\( \\) in {k}')
    # leaked answer: the correct MC letter stated, or the first answer token (a number with 2+ digits) in the hint
    a = e['answer']
    if e['mc']:
        m = re.match(r'\(?([A-E])\b', a)
        if m and re.search(r'\b(answer|choice) (is )?' + m.group(1) + r'\b', plain(hint)): err.append(tag + ': hint names the answer letter')
    else:
        nums = re.findall(r'\d+\.\d+|\d{3,}', a.split(' ')[0] if a else '')
        for n in nums:
            if n in plain(hint): err.append(tag + f': hint contains answer value {n}')
print(f'{len(H)} hints checked;', 'ERRORS:', err if err else 'none')
