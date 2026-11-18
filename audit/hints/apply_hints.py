#!/usr/bin/env python3
"""Insert the writers' hints into the draft pages (a <details> Hint above each Answer) and add the 'why' sentence to terse
answers; apply the fuller bank reasons. Idempotent: an exercise that already has a Hint is skipped.
usage: python3 audit/hints/apply_hints.py [chNN ...]   (pages)   |   python3 audit/hints/apply_hints.py --bank"""
import json, re, sys, os, glob, collections
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
BOX = re.compile(r'<div class="box-exercise">.*?</details>\s*</div>', re.S)

def pages(chs):
    for ch in chs:
        H = json.load(open(os.path.join(R, 'audit', 'hints', f'{ch}_hints.json')))
        byfile = collections.defaultdict(dict)
        for h in H: byfile[h['file']][h['idx']] = h
        n = w = 0
        for f, hs in byfile.items():
            p = os.path.join(R, f); s = open(p).read(); blocks = list(BOX.finditer(s)); out = []; last = 0
            assert len(blocks) == max(hs) + 1, (f, len(blocks), max(hs) + 1)
            for i, m in enumerate(blocks):
                b = m.group(0); h = hs[i]
                t = re.search(r'<p class="boxtitle">(.*?)</p>', b)
                assert re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', t.group(1))).strip() == h['title'], (f, i, h['title'])
                if '<summary>Hint</summary>' not in b:
                    assert b.count('<details><summary>Answer</summary>') == 1, (f, i)
                    b = b.replace('<details><summary>Answer</summary>',
                                  f'<details><summary>Hint</summary><p>{h["hint"].strip()}</p></details>\n<details><summary>Answer</summary>', 1)
                    n += 1
                    if h.get('why', '').strip():
                        k = b.rfind('</details>'); b = b[:k] + f'<p>{h["why"].strip()}</p>\n' + b[k:]; w += 1
                out.append(s[last:m.start()] + b); last = m.end()
            out.append(s[last:]); open(p, 'w').write(''.join(out))
        print(ch, 'hints added', n, 'whys added', w)

def bank():
    rows = json.load(open(os.path.join(R, 'audit', 'hints', 'bank_short_reasons.json')))
    by = collections.defaultdict(list)
    for r in rows:
        assert r['new_reason'].strip(), r['id']; by[r['bank']].append(r)
    W = {'i1': lambda B: json.dumps(B, ensure_ascii=False, indent=1),
         'line': lambda B: '[\n' + ',\n'.join(json.dumps(q, ensure_ascii=False, separators=(',', ':')) for q in B) + '\n]'}
    for f, rs in by.items():
        p = os.path.join(R, f); raw = open(p).read(); B = json.loads(raw)
        fmt = next((k, t) for k in W for t in ('', '\n') if W[k](B) + t == raw)   # reproduce the file's exact format
        idx = {q['id']: q for q in B}
        for r in rs:
            q = idx[r['id']]; assert q['y'][r['choice_index']] == r['old_reason'], r['id']; q['y'][r['choice_index']] = r['new_reason']
        open(p, 'w').write(W[fmt[0]](B) + fmt[1])
        print(f, len(rs), 'reasons updated')

if __name__ == '__main__':
    if sys.argv[1:] == ['--bank']: bank()
    else: pages(sys.argv[1:] or [f'ch{i:02d}' for i in range(1, 15)])
