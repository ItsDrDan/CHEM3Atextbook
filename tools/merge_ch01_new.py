#!/usr/bin/env python3
"""Append the new Chapter 1 measurement Try It sets (tools/bank_ch01_new_A.py, _B.py) to bank/ch01.json.
Idempotent: items with the new keys are removed first, then re-added with ids after the last existing id."""
import json, os, runpy
HERE = os.path.dirname(os.path.abspath(__file__)); BANK = os.path.join(HERE, '..', 'bank', 'ch01.json')
NEW = ('ch01-scinot', 'ch01-sigcalc', 'ch01-read', 'ch01-multistep', 'ch01-powers', 'ch01-dosage', 'ch01-percent')
B = [q for q in json.load(open(BANK)) if q['t'] not in NEW]
n = len(B)
assert [q['id'] for q in B] == ['c1-%03d' % i for i in range(1, n + 1)]
for part in ('A', 'B'):
    for it in runpy.run_path(os.path.join(HERE, f'bank_ch01_new_{part}.py'))['ITEMS']:
        n += 1
        q = {'id': 'c1-%03d' % n, 't': it['t'], 'q': it['q'], 'c': it['c'], 'y': it['y'], 'h': it['h'], 'w': it['w'],
             'd': it['d'], 'k': it.get('k', 0)}
        if it.get('f'): q['f'] = it['f']
        B.append(q)
with open(BANK, 'w') as fh:
    json.dump(B, fh, ensure_ascii=False, indent=1); fh.write('\n')
print('bank now', len(B))
