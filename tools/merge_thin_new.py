#!/usr/bin/env python3
"""Append tools/bank_thin_new.py (16 items, 2026-11-17) to bank/ch07, ch09, ch14 after their last ids. Run once on a bank without them."""
import json, runpy, os
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, '..')
items = runpy.run_path(os.path.join(HERE, 'bank_thin_new.py'))['ITEMS']
for ch, pre in (('07', 'c7'), ('09', 'c9'), ('14', 'c14')):
    p = os.path.join(R, 'bank', f'ch{ch}.json'); B = json.load(open(p))
    assert not any(q['q'] == it['q'] for q in B for it in items), 'already merged'
    n = max(int(q['id'].split('-')[1]) for q in B); w = len(B[0]['id'].split('-')[1])
    for it in items:
        if it['t'].startswith(f'ch{ch}-'):
            n += 1; q = {'id': f'{pre}-%0{w}d' % n, **{k: it[k] for k in ('t', 'q', 'c', 'y', 'h', 'w', 'd')}, 'k': it.get('k', 0)}
            B.append(q)
    with open(p, 'w') as fh: json.dump(B, fh, ensure_ascii=False, indent=1); fh.write('\n')
    print(p, len(B))
