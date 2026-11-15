#!/usr/bin/env python3
"""Checker for the Chapter 3 banks: structural checks copied from tools/check_bank_ch02.py (ch03 topic ids)
plus independent recomputation of every numeric answer and numeric distractor, electron counts of every
configuration and orbital diagram, Aufbau/Pauli/Hund checks, ion electron counts, valence electrons from the
group number, periodic-trend rankings against tabulated data, and periodic-table figure cells.
Course sig-fig rule: trailing zeros without a decimal point are not significant.
usage: python3 tools/check_bank_ch03.py bank/ch03.json bank/ch03_adapt.json"""
import json, sys, re, collections, math
from decimal import Decimal, ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
TOP = {'ch03-light', 'ch03-bohr', 'ch03-orbitals', 'ch03-config', 'ch03-valence', 'ch03-trends'}
err = []

# ---------- structural checks (same as ch02 checker) ----------
def structural(B, pat, label, allow_f):
    ids = [q['id'] for q in B]
    if len(set(ids)) != len(ids): err.append(label + ' dup ids')
    if ids != [pat % i for i in range(1, len(B) + 1)]: err.append(label + ' ids not sequential')
    for q in B:
        i = q['id']
        if q.get('t') not in TOP: err.append(i + ' bad t')
        if len(q.get('c', [])) != 4: err.append(i + ' c!=4')
        if len(q.get('y', [])) != 4: err.append(i + ' y!=4')
        if any(not str(y).strip() for y in q.get('y', [])): err.append(i + ' empty y')
        if len(set(re.sub(r'\s+', ' ', c).strip().lower() for c in q['c'])) != 4: err.append(i + ' dup choice')
        for k in ('q', 'h', 'w'):
            if not str(q.get(k, '')).strip(): err.append(i + ' empty ' + k)
        if q.get('d') not in (1, 2, 3): err.append(i + ' bad d')
        if q.get('k') not in (0, 1): err.append(i + ' bad k')
        if re.search(r'all of the above|none of the above', json.dumps(q), re.I): err.append(i + ' AOTA/NOTA')
        s = ' '.join([q['q'], q['h'], q['w']] + q['c'] + q['y'])
        for tg in ('sub', 'sup', 'b', 'i'):
            if len(re.findall('<%s>' % tg, s)) != len(re.findall('</%s>' % tg, s)): err.append(i + ' unbalanced <%s>' % tg)
        if re.search(r'&(?!(?:[a-z]+|#\d+);)', s): err.append(i + ' bare &')
        if 'f' in q and not allow_f: err.append(i + ' has f (ADAPT items must be text only)')
        for f in q.get('f', []):
            if f['type'] not in ('table', 'ptgrid', 'orbitals'): err.append(i + ' figure type not used/checked here: ' + f['type'])
        # scope limits (CHEM 3A)
        if re.search(r'Rydberg|electronegativ|electron affinity|quantum number|ℓ|m<sub>[ls]', s, re.I): err.append(i + ' out of scope term')
        if label == 'HW' and not q['y'][0].startswith('Correct: '): err.append(i + ' ADAPT y[0] lacks "Correct: "')
        plain = lambda x: re.sub(r'<[^>]+>', '', x).strip().lower()
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if right in plain(q['y'][j]): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c3-%03d', 'TRY', True)
structural(HW, 'c3-h%02d', 'HW', False)

ALL = TRY + HW
def by(sub):
    m = [q for q in ALL if sub in q['q']]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
def txt(x):
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<[^>]+>', '', x)
    return x.replace('&minus;', '-').replace('−', '-').replace('&times;', 'x').replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ')
def ok(cond, msg):
    print('   ', 'OK ' if cond else 'BAD', msg)
    if not cond: err.append(msg)
checked = set()

# ---------- elements ----------
SYM = ('H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr '
       'Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba').split()
Z = {s: i + 1 for i, s in enumerate(SYM)}; Z['Fr'] = 87
NAMES = dict(hydrogen='H', helium='He', carbon='C', nitrogen='N', oxygen='O', fluorine='F', neon='Ne', sodium='Na',
             magnesium='Mg', aluminum='Al', silicon='Si', phosphorus='P', sulfur='S', chlorine='Cl', argon='Ar',
             potassium='K', calcium='Ca', vanadium='V', arsenic='As', selenium='Se', francium='Fr')
def period(z): return next(p for p, top in enumerate((2, 10, 18, 36, 54, 86, 118), 1) if z <= top)
def group(z):
    p = period(z); start = (0, 1, 3, 11, 19, 37, 55, 87)[p]; i = z - start
    if p == 1: return 1 if z == 1 else 18
    if p <= 3: return i + 1 if i < 2 else i + 11
    if p <= 5: return i + 1
    return {55: 1, 56: 2, 87: 1}[z]
def at(p, g): return next(s for s in list(SYM) + ['Fr'] if period(Z[s]) == p and group(Z[s]) == g)
ORDER = '1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s'.split()
CAP = dict(s=2, p=6, d=10, f=14)
NOBLE = dict(He=2, Ne=10, Ar=18, Kr=36, Xe=54)
def aufbau(n):
    out = []
    for sub in ORDER:
        if n <= 0: break
        k = min(n, CAP[sub[1]]); out.append((sub, k)); n -= k
    return out
def full_cfg(n): return ' '.join('%s^%d' % (s, k) for s, k in aufbau(n))
def ng_cfg(n):
    core = max((v, k) for k, v in NOBLE.items() if v < n)
    inner = len(aufbau(core[0])); rest = aufbau(n)[inner:]
    return '[%s] ' % core[1] + ' '.join('%s^%d' % (s, k) for s, k in rest)
def count_cfg(s):
    s = txt(s); m = re.match(r'\s*(?:\[(\w+)\])?\s*((?:\d[spdf]\^\d+\s*)*)$', s)
    if not m: return None
    toks = re.findall(r'(\d)([spdf])\^(\d+)', m.group(2))
    for n_, l, k in toks:
        if int(k) > CAP[l]: return -1
    return (NOBLE[m.group(1)] if m.group(1) else 0) + sum(int(k) for _, _, k in toks)
def ion_e(s):
    m = re.match(r'([A-Z][a-z]?)\^(\d*)([+-])$', txt(s).strip())
    sym, mag, sg = m.groups(); ch = int(mag or 1) * (1 if sg == '+' else -1)
    return Z[sym] - ch
def valence(z): g = group(z); return 2 if z == 2 else (g if g <= 2 else g - 10)
def ion_charge(z): return {1: 1, 2: 2, 13: 3, 15: -3, 16: -2, 17: -1}.get(group(z))

# ---------- numeric items ----------
print('Light calculations (c = 3.00e8 m/s, h = 6.626e-34 J s; one rounding at the end)')
c, h = 3.00e8, 6.626e-34
def sf(s):
    s = s.strip().lower().split('e')[0]
    if '.' in s: return len(s.replace('.', '').lstrip('0'))
    return len(s.lstrip('0').rstrip('0'))
def show(x, n):
    d = Decimal(repr(x)); e = d.adjusted()
    m = (d.scaleb(-e)).quantize(Decimal(10) ** -(n - 1), rounding=ROUND_HALF_UP)
    if m >= 10: e += 1; m = (d.scaleb(-e)).quantize(Decimal(10) ** -(n - 1), rounding=ROUND_HALF_UP)
    if -2 <= e <= 2: return format((m.scaleb(e)).quantize(Decimal(10) ** min(0, e - n + 1)), 'f')
    return '%s x 10^%d' % (m, e)
# (stem substring, given numbers as written, unit, {choice: (value, why, unit override)})
CALC = [
 ('which gives off light at 589 nm. What is the frequency', ['589'], 'Hz',
  {0: (c / 589e-9, 'c/lambda'), 1: (c / 589, 'forgot nm->m'), 2: (c * 589e-9, 'multiplied'), 3: (589e-9 / c, 'lambda/c')}),
 ('MRI scanner sends radio-frequency pulses', ['6.39'], 'm',
  {0: (c / 6.39e7, 'c/nu'), 1: (6.39e7 / c, 'nu/c'), 2: (c * 6.39e7, 'multiplied'), 3: (c / 6.39e7, 'right number, unit nm', 'nm')}),
 ('Germicidal UV-C light used to disinfect', ['1.18'], 'J',
  {0: (h * 1.18e15, 'h nu'), 1: (h / 1.18e15, 'h/nu'), 2: (1.18e15 / h, 'nu/h'), 3: (h * c / 1.18e15, 'hc/nu')}),
 ('LEDs that give off light at 455 nm', ['455'], 'J',
  {0: (h * c / 455e-9, 'hc/lambda'), 1: (h * c / 455, 'forgot nm->m'), 2: (c / 455e-9, 'stopped at frequency'), 3: (h / 455e-9, 'h/lambda')}),
 ('blue-green line has a wavelength of 486 nm', ['486'], 'J',
  {0: (h * c / 486e-9, 'hc/lambda'), 1: (h * c / 486, 'forgot nm->m'), 2: (h / 486e-9, 'h/lambda'), 3: (c / 486e-9, 'stopped at frequency')}),
 ('UV-C photon carry than one sodium-lamp photon', ['254', '589'], 'times',
  {0: (589 / 254, 'ratio 589/254'), 1: (254 / 589, 'inverted'), 2: (589 - 254, 'subtracted'), 3: ((589 / 254) ** 2, 'squared')}),
 ('reflected by leaves at 842 nm', ['842'], 'Hz',
  {0: (c / 842e-9, 'c/lambda'), 1: (c / 842, 'forgot nm->m'), 2: (c * 842e-9, 'multiplied'), 3: (842e-9 / c, 'lambda/c')}),
 ('cell phone sends signals at 1.90', ['1.90'], 'm',
  {0: (c / 1.90e9, 'c/nu'), 1: (1.90e9 / c, 'nu/c'), 2: (c * 1.90e9, 'multiplied'), 3: (c / 1.90e9, 'right number, unit nm', 'nm')}),
 ('wavelength of 0.0250 nm', ['0.0250'], 'J',
  {0: (h * c / 2.50e-11, 'hc/lambda'), 1: (h * c / 0.0250, 'forgot nm->m'), 2: (c / 2.50e-11, 'stopped at frequency'), 3: (h / 2.50e-11, 'h/lambda')}),
 ('sodium lamp has a frequency of 5.09', ['5.09'], 'J',
  {0: (h * 5.09e14, 'h nu'), 1: (h / 5.09e14, 'h/nu'), 2: (5.09e14 / h, 'nu/h'), 3: (h * c / 5.09e14, 'hc/nu')}),
 ('254 nm UV-C photon carry than one 940. nm', ['254', '940.'], 'times',
  {0: (940 / 254, 'ratio 940/254'), 1: (254 / 940, 'inverted'), 2: (940 - 254, 'subtracted'), 3: ((940 / 254) ** 2, 'squared')}),
 ('blue-violet line at 434 nm', ['434'], 'J',
  {0: (h * c / 434e-9, 'hc/lambda'), 1: (h * c / 434, 'forgot nm->m'), 2: (c / 434e-9, 'stopped at frequency'), 3: (h * c * 434e-9, 'hc x lambda')}),
]
for sub, given, unit, ch in CALC:
    q = by(sub)
    if not q: continue
    checked.add(q['id'])
    n = min([sf(g) for g in given] + [3])         # c has 3 s.f., h has 4
    for g in given:   # each given value must appear in the stem exactly as written (so its s.f. are what students see)
        if not re.search(r'(?<![\d.])' + re.escape(g) + r'(?![\d])' + ('' if '.' in g else r'(?!\.)'), q['q']): err.append(q['id'] + ' given %r not in stem as written' % g)
    print('  %s %s (%d s.f.)' % (q['id'], sub[:45], n))
    for j, spec in ch.items():
        v, why = spec[0], spec[1]; u = spec[2] if len(spec) > 2 else unit
        if why == 'subtracted': want = '%d %s' % (v, u)
        else: want = show(v, n) + ' ' + u
        ok(txt(q['c'][j]).strip() == want, '%s c[%d] %-30s = %r (%s)' % (q['id'], j, repr(txt(q['c'][j])), want, why))
    if txt(q['c'][0]).split(' ')[0] not in txt(q['w']) and unit != 'times': err.append(q['id'] + ' answer not in w')
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')
# course sig-fig rule in every calculation stem: a whole number ending in 0 with no decimal point has fewer s.f. than its digits;
# such values must be written with a trailing decimal point (660. nm) or avoided
for q in ALL:
    if q['k'] == 1:
        for m in re.finditer(r'(?<![\d.])(\d*[1-9]\d*0)(?![\d.^])', txt(q['q'])):
            err.append(q['id'] + ' calculation stem has ambiguous trailing-zero value %r (write %s. or choose another value)' % (m.group(1), m.group(1)))
# order-of-magnitude sanity on the right answers
print('  sanity: 589 nm -> %.3g Hz; 6.39e7 Hz -> %.3g m; 0.0250 nm X-ray / 589 nm photon = %.0f' % (c / 589e-9, c / 6.39e7, 589 / 0.0250))

print('Wavelength / energy orderings')
q = by('in order of <b>increasing energy</b>: pulse'); checked.add(q['id'])
seqs = [[int(x) for x in re.findall(r'(\d+) nm', txt(ch))] for ch in q['c']]
ok(seqs[0] == sorted(seqs[0], reverse=True), '%s c[0] %s is decreasing wavelength = increasing energy' % (q['id'], seqs[0]))
for j in (1, 2, 3): ok(seqs[j] != seqs[0], '%s c[%d] %s differs' % (q['id'], j, seqs[j]))
EM = ['radio waves', 'microwaves', 'infrared', 'visible', 'ultraviolet', 'X-rays', 'gamma']
q = by('order of <b>increasing photon energy</b>'); checked.add(q['id'])
for j, ch in enumerate(q['c']):
    seq = [EM.index(x.strip()) for x in txt(ch).split('<')]
    ok((seq == sorted(seq)) == (j == 0), '%s c[%d] %s increasing=%s' % (q['id'], j, seq, seq == sorted(seq)))
q = by('photon has the <b>lowest frequency</b>'); checked.add(q['id'])
rows = q['f'][0]['rows']; lo = max(rows, key=lambda r: float(r[1]))
ok(q['c'][0].startswith(lo[0]) and sorted(r[0] for r in rows) == sorted(q['c']), '%s longest wavelength row %s nm = c[0]' % (q['id'], lo[1]))
q = by('pulse oximeter shines red light at 660 nm and infrared'); checked.add(q['id'])
ok('660' in q['c'][0] and c / 660e-9 > c / 940e-9, '%s 660 nm: nu %.3g > %.3g Hz' % (q['id'], c / 660e-9, c / 940e-9))
q = by('germicidal lamp gives off light at 254 nm. Which region'); checked.add(q['id'])
ok(254 < 400 and q['c'][0] == 'Ultraviolet', '%s 254 nm < 400 nm -> UV' % q['id'])

print('Hydrogen lines (checker-only Rydberg check, R = 1.09678e7 m^-1; not taught in CHEM 3A)')
R = 1.09678e7
lam = lambda hi, lo: 1e9 / (R * (1 / lo ** 2 - 1 / hi ** 2))
print('   n=3,4,5,6 -> 2: %.1f %.1f %.1f %.1f nm' % tuple(lam(n, 2) for n in (3, 4, 5, 6)))
q = by('The 434 nm line comes from a drop'); checked.add(q['id'])
ok(abs(lam(5, 2) - 434) < 1 and abs(lam(3, 2) - 656) < 1 and abs(lam(4, 2) - 486) < 1 and abs(lam(6, 2) - 410) < 1 and q['c'][0] == 'n = 5 to n = 2', q['id'] + ' 434 nm is n=5->2')
def dE(a, b): return 1 / b ** 2 - 1 / a ** 2        # >0 for a drop a -> b
q = by('photon with the <b>longest</b> wavelength'); checked.add(q['id'])
drops = [tuple(int(x) for x in re.findall(r'n = (\d)', ch)) for ch in q['c']]
es = [dE(a, b) for a, b in drops]
ok(es[0] == min(es) and all(e > 0 for e in es), '%s drop energies (units of R hc) %s; smallest is c[0]' % (q['id'], ['%.3f' % e for e in es]))
q = by('which electron jump gives off a photon'); checked.add(q['id'])
drops = [tuple(int(x) for x in re.findall(r'n = (\d)', ch)) for ch in q['c']]
ok([a > b for a, b in drops] == [True, False, False, False], '%s only c[0] is a downward jump %s' % (q['id'], drops))
q = by('moves from n = 2 to n = 5'); checked.add(q['id']); ok('absorbs' in q['c'][0], q['id'] + ' upward jump absorbs')

# ---------- orbitals ----------
print('Orbital diagrams (Aufbau, Pauli, Hund; arrow counts)')
NORB = dict(s=1, p=3, d=5, f=7)
def parse_od(s):
    s = txt(s); subs = []
    for name, boxes in re.findall(r'(\d[spdf])\s*((?:\[[^\]]*\])+)', s):
        subs.append((name, [b.replace(' ', '') for b in re.findall(r'\[([^\]]*)\]', boxes)]))
    return subs
def od_from_fig(f): return [(sb['name'], [{'u': '↑', 'd': '↓', 'ud': '↑↓', 'uu': '↑↑', 'dd': '↓↓', '': ''}[b] for b in sb['boxes']]) for sb in f['subs']]
def od_rules(subs, full_diagram=True):
    """returns (electrons, unpaired, list of broken rules)"""
    bad = set(); n = sum(len(b) for _, bx in subs for b in bx); unp = 0
    for name, bx in subs:
        if len(bx) != NORB[name[1]]: bad.add('box count')
        for b in bx:
            if len(b) > 2 or b in ('↑↑', '↓↓'): bad.add('Pauli')
        e = sum(len(b) for b in bx)
        if any(len(b) == 2 for b in bx) and any(len(b) == 0 for b in bx): bad.add('Hund')
        if len(set(b for b in bx if len(b) == 1)) > 1: bad.add('Hund')
        unp += sum(1 for b in bx if len(b) == 1)
    names = [nm for nm, _ in subs]
    for k, (name, bx) in enumerate(subs[:-1]):   # every subshell before the last must be full
        if sum(len(b) for b in bx) < 2 * NORB[name[1]]: bad.add('Aufbau')
    if names != ORDER[ORDER.index(names[0]):ORDER.index(names[0]) + len(names)]: bad.add('order')
    if full_diagram and names[0] != '1s': bad.add('not full')
    return n, unp, sorted(bad)
OD = [  # (stem substring, expected electrons of the right answer, {distractor: expected broken rule or electron count}, full diagram?)
 ('valence subshells</b> (3s and 3p) of a ground-state silicon', 4, {1: 'Hund', 2: 'Pauli', 3: 'Aufbau'}, False),
 ('ground-state <b>aluminum</b> atom (Z = 13)', 13, {1: 'Aufbau', 2: 14, 3: 'Aufbau'}, True),
 ('2p subshell of a ground-state <b>nitrogen</b>', 3, {1: 'Hund', 2: 4, 3: 'Hund'}, False),
]
for sub, ne, wr, full in OD:
    q = by(sub); checked.add(q['id'])
    n, unp, bad = od_rules(parse_od(q['c'][0]), full)
    ok(n == ne and not bad, '%s c[0] %d electrons, %d unpaired, rules broken %s' % (q['id'], n, unp, bad))
    for j, exp in wr.items():
        n2, u2, bad2 = od_rules(parse_od(q['c'][j]), full)
        good = (exp in bad2) if isinstance(exp, str) else (n2 == exp and n2 != ne)
        ok(good, '%s c[%d] %d electrons, broken %s (expected %s)' % (q['id'], j, n2, bad2, exp))
q = by('2p subshell of a nitrogen atom as 2p [↑↓][↑]'); checked.add(q['id'])
n, unp, bad = od_rules(parse_od(txt(q['q']).split('as ')[1]), False)
ok(bad == ['Hund'] and q['c'][0] == "Hund's rule", '%s stem diagram breaks %s' % (q['id'], bad))
q = by('breaks the <b>Pauli exclusion principle</b>'); checked.add(q['id'])
br = [('Pauli' in od_rules([('1s', [txt(ch).strip('[] ').replace(' ', '')])], False)[2]) for ch in q['c']]
ok(br == [True, False, False, False], '%s only c[0] breaks Pauli %s' % (q['id'], br))
q = by('shows a neutral atom in its ground state. Which element'); checked.add(q['id'])
n, unp, bad = od_rules(od_from_fig(q['f'][0]))
ok(SYM[n - 1] == NAMES[q['c'][0].lower()] and not bad, '%s figure %d electrons -> %s, rules broken %s' % (q['id'], n, SYM[n - 1], bad))
q = by('drew this orbital diagram for a <b>ground-state</b> carbon'); checked.add(q['id'])
n, unp, bad = od_rules(od_from_fig(q['f'][0]))
ok(n == Z['C'] and bad == ['Aufbau'] and q['c'][0] == 'The Aufbau principle', '%s figure %d electrons, broken %s' % (q['id'], n, bad))
def unpaired(z):
    tot = 0
    for sub, k in aufbau(z):
        o = NORB[sub[1]]; tot += k if k <= o else 2 * o - k
    return tot
for sub, sym in (('unpaired electrons</b> does a ground-state oxygen', 'O'), ('unpaired electrons</b> does a ground-state silicon', 'Si')):
    q = by(sub); checked.add(q['id'])
    ok(q['c'][0] == str(unpaired(Z[sym])) and str(unpaired(Z[sym])) not in q['c'][1:], '%s %s unpaired = %d' % (q['id'], sym, unpaired(Z[sym])))
# capacities
for sub, ans in (('<b>fourth shell</b> (n = 4)', 2 * 4 ** 2), ('<b>second shell</b> (n = 2)', 2 * 2 ** 2), ('greatest number of electrons that one orbital', 2)):
    q = by(sub); checked.add(q['id']); ok(q['c'][0] == str(ans), '%s capacity %d' % (q['id'], ans))
q = by('orbitals are in a <b>p subshell</b>'); checked.add(q['id']); ok(q['c'][0] == '%d orbitals, %d electrons' % (NORB['p'], CAP['p']), q['id'] + ' p: 3 orbitals 6 electrons')
q = by('orbitals are in a <b>d subshell</b>'); checked.add(q['id']); ok(q['c'][0] == str(NORB['d']), q['id'] + ' d: 5 orbitals')
for sub, after in (('fills <b>right after 3p</b>', '3p'), ('fills <b>right after 4s</b>', '4s')):
    q = by(sub); checked.add(q['id']); nxt = ORDER[ORDER.index(after) + 1]; ok(q['c'][0] == nxt, '%s after %s comes %s' % (q['id'], after, nxt))

# ---------- configurations ----------
print('Electron configurations (Aufbau builder; superscript totals)')
CFG = [  # (stem substring, species, charge, 'full'|'ng')
 ('full electron configuration of a magnesium <b>atom</b>', 'Mg', 0, 'full'),
 ('configuration of a potassium atom (Z = 19)', 'K', 0, 'full'),
 ('noble-gas (shorthand) configuration of a calcium', 'Ca', 0, 'ng'),
 ('noble-gas configuration of an iodine atom', 'I', 0, 'ng'),
 ('configuration of the potassium <b>ion</b>', 'K', 1, 'full'),
 ('configuration of the nitride ion', 'N', -3, 'full'),
 ('marked X on the periodic table outline', 'As', 0, 'ng'),
 ('configuration of a silicon atom (Z = 14)', 'Si', 0, 'full'),
 ('noble-gas configuration of a selenium atom', 'Se', 0, 'ng'),
 ('configuration of the chloride ion', 'Cl', -1, 'full'),
 ('configuration of the aluminum ion', 'Al', 3, 'full'),
]
for sub, sym, chg, form in CFG:
    q = by(sub)
    if not q: continue
    checked.add(q['id']); ne = Z[sym] - chg
    want = (full_cfg if form == 'full' else ng_cfg)(ne)
    got = txt(q['c'][0]).strip()
    ok(got == want and count_cfg(q['c'][0]) == ne, '%s %s%+d c[0] %r = %r (%d e)' % (q['id'], sym, chg, got, want, ne))
    for j in (1, 2, 3):
        cj = txt(q['c'][j]).strip(); nj = count_cfg(q['c'][j])
        ok(cj != want, '%s c[%d] %r differs (electrons %s)' % (q['id'], j, cj, nj))
    if sym == 'As':   # figure cell
        p, g = q['f'][0]['cells']['X']; ok(at(p, g) == 'As', '%s figure X at period %d group %d = %s' % (q['id'], p, g, at(p, g)))
# element-from-configuration items
for sub in ('has the configuration [Ne] 3s<sup>2</sup> 3p<sup>4</sup>', 'neutral atom has the configuration', 'Which element has the configuration 1s'):
    q = by(sub); checked.add(q['id'])
    m = re.search(r'configuration ((?:\[\w+\] )?(?:\d[spdf]<sup>\d+</sup>\s*)+)', q['q']); n = count_cfg(m.group(1))
    ok(NAMES[q['c'][0].lower()] == SYM[n - 1] and txt(m.group(1)).strip() == (full_cfg(n) if '[' not in m.group(1) else ng_cfg(n)),
       '%s stem config has %d electrons -> %s = c[0] %s' % (q['id'], n, SYM[n - 1], q['c'][0]))
    for ch in q['c'][1:]: ok(Z[NAMES[ch.lower()]] != n, '%s distractor %s (Z=%d) is not Z=%d' % (q['id'], ch, Z[NAMES[ch.lower()]], n))
q = by('for selenium (Z = 34). What is wrong'); checked.add(q['id'])
m = re.search(r'writes (.*?) for selenium', q['q']); n = count_cfg(m.group(1))
ok(n == 33 and SYM[n - 1] == 'As' and 'arsenic' in q['c'][0] and full_cfg(34).endswith('4p^4'), '%s student config %d electrons (%s); Se ends %s' % (q['id'], n, SYM[n - 1], full_cfg(34)[-4:]))
q = by("Which subshell does arsenic's <b>last electron</b>"); checked.add(q['id']); ok(q['c'][0] == aufbau(Z['As'])[-1][0], q['id'] + ' As last subshell ' + aufbau(Z['As'])[-1][0])
q = by('In which block of the periodic table is it'); checked.add(q['id']); ok(q['c'][0] == aufbau(Z['Ca'])[-1][0][1] + ' block', q['id'] + ' Ca block ' + aufbau(Z['Ca'])[-1][0][1])
# every configuration that appears as a right answer anywhere was counted
for q in ALL:
    if count_cfg(q['c'][0]) not in (None,) and q['id'] not in checked: err.append(q['id'] + ' configuration answer not checked')

print('Isoelectronic ions (electrons = Z - charge)')
q = by('<b>isoelectronic with argon</b>'); checked.add(q['id'])
es = [ion_e(ch) for ch in q['c']]; ok(es[0] == NOBLE['Ar'] and NOBLE['Ar'] not in es[1:], '%s electrons %s' % (q['id'], es))
q = by('has <b>18 electrons</b>'); checked.add(q['id'])
es = [ion_e(ch) for ch in q['c']]; ok(es[0] == 18 and 18 not in es[1:], '%s electrons %s' % (q['id'], es))
q = by('<b>entirely</b> isoelectronic with neon'); checked.add(q['id'])
sets = [[ion_e(x.strip()) for x in re.sub(r'(<sup>[^<]*</sup>),', r'\1|', ch).split('|')] for ch in q['c']]
ok(all(e == 10 for e in sets[0]) and all(any(e != 10 for e in s) for s in sets[1:]), '%s electrons %s' % (q['id'], sets))
q = by('1 mmol equal 2 mEq'); checked.add(q['id'])
chs = [Z[re.match(r'[A-Z][a-z]?', ch).group()] - ion_e(ch) for ch in q['c']]; ok(abs(chs[0]) == 2 and all(abs(x) == 1 for x in chs[1:]), '%s charges %s' % (q['id'], chs))

# ---------- valence electrons and ions ----------
print('Valence electrons (groups 1-2: group number; 13-18: group - 10) and octet-rule ions')
for sub, sym in (('valence electrons does a chlorine <b>atom</b>', 'Cl'), ('Selenium is [Ar] 4s', 'Se'), ('dots are drawn around the symbol for nitrogen', 'N'),
                 ('valence electrons does a strontium atom', 'Sr'), ('valence electrons does an iodine atom', 'I'), ('Gallium (row 4, group 13)', 'Ga')):
    q = by(sub); checked.add(q['id']); v = valence(Z[sym])
    hi = max(int(s[0]) for s, k in aufbau(Z[sym])); vs = sum(k for s, k in aufbau(Z[sym]) if int(s[0]) == hi and s[1] in 'sp')
    ok(q['c'][0] == str(v) == str(vs) and str(v) not in q['c'][1:], '%s %s group %d -> %d valence (highest shell n=%d holds %d s+p)' % (q['id'], sym, group(Z[sym]), v, hi, vs))
for sub, sym in (('Aluminum is in group 13', 'Al'), ('predict the ion that rubidium', 'Rb')):
    q = by(sub); checked.add(q['id']); ch = ion_charge(Z[sym]); e = ion_e(q['c'][0])
    ok(Z[sym] - e == ch and e in NOBLE.values(), '%s %s forms charge %+d, %d electrons (noble gas)' % (q['id'], sym, ch, e))
q = by('nitrogen, which is in group 15'); checked.add(q['id']); ok(q['c'][0] == '3&minus;' and ion_charge(Z['N']) == -3 and Z['N'] + 3 == NOBLE['Ne'], q['id'] + ' N -> 3-')
q = by('Why does oxygen form O'); checked.add(q['id']); ok(ion_charge(Z['O']) == -2 and valence(Z['O']) == 6, q['id'] + ' O: 6 valence, 2-')
q = by('most likely to form a <b>2&minus;</b> ion'); checked.add(q['id'])
cells = q['f'][0]['cells']; el = {k: at(*v) for k, v in cells.items()}
ok([k for k, s in el.items() if ion_charge(Z[s]) == -2] == [q['c'][0]], '%s cells %s; 2- former = %s' % (q['id'], el, q['c'][0]))
q = by('most similar chemical properties'); checked.add(q['id'])
pairs = [[NAMES[w.lower()] for w in ch.split(' and ')] for ch in q['c']]
same = [group(Z[a]) == group(Z[b]) for a, b in pairs]; ok(same == [True, False, False, False], '%s same group %s' % (q['id'], same))

# ---------- periodic trends ----------
print('Periodic trends against tabulated data (atomic radius pm; first ionization energy kJ/mol; ionic radius pm)')
RAD = dict(Li=152, Na=186, K=227, Rb=248, Cs=265, Be=112, Mg=160, Ca=197, Al=143, Si=118, C=77, N=75, O=73, F=72,
           P=110, S=103, Cl=99, Se=117, Br=114, I=133, Ar=71, Kr=88)
IE = dict(H=1312, He=2372, Li=520, Be=899, F=1681, Ne=2081, Na=496, Mg=738, Al=578, Si=786, S=1000, Cl=1251, Ar=1521,
          K=419, Ca=590, Br=1140, Kr=1351, Rb=403, I=1008, Cs=376, Fr=393)
IONR = {'Na+': 102, 'K+': 138, 'Mg2+': 72, 'Cl-': 181, 'F-': 133, 'Cl': 99, 'F': 72, 'Mg': 160}
def rank(sub, data):
    q = by(sub); checked.add(q['id'])
    for j, ch in enumerate(q['c']):
        seq = [x.strip() for x in txt(ch).split('<')]; vals = [data[s] for s in seq]
        ok((vals == sorted(vals)) == (j == 0), '%s c[%d] %s %s increasing=%s' % (q['id'], j, seq, vals, vals == sorted(vals)))
rank('Rank Al, P and Cl', RAD); rank('Rank K, Mg and Cl', RAD); rank('Rank Ca, Br and Kr', IE)
def pick(sub, data, best, conv=lambda s: s):
    q = by(sub); checked.add(q['id']); syms = [conv(ch) for ch in q['c']]; vals = [data[s] for s in syms]
    ok(vals[0] == best(vals) and vals.count(vals[0]) == 1, '%s %s %s -> %s' % (q['id'], syms, vals, syms[0]))
pick('group 1 atoms has the <b>largest</b>', RAD, max)
pick('highest</b> first ionization energy: Na, Si, S or Ar', IE, max)
pick('halogen has the <b>lowest</b> first ionization', IE, min)
pick('highest first ionization energy of <b>all</b>', IE, max, lambda s: NAMES[s.lower()])
for sub in ('most <b>metallic character</b>?', 'most <b>metallic character</b>: Na'):
    pick(sub, IE, min)   # metallic character tracks low ionization energy
for sub, data, best in (('has the <b>largest atomic radius</b>', RAD, max), ('has the <b>highest first ionization energy</b>?', IE, max)):
    q = by(sub); checked.add(q['id']); el = {k: at(*v) for k, v in q['f'][0]['cells'].items()}; vals = {k: data[s] for k, s in el.items()}
    ok(best(vals, key=vals.get) == q['c'][0] and sorted(q['c']) == sorted(el), '%s cells %s values %s -> %s' % (q['id'], el, vals, q['c'][0]))
for sub, big, small in (('chlorine atom (Cl) or a chloride ion', 'Cl-', 'Cl'), ('which ion is larger?', 'K+', 'Na+'),
                        ('magnesium atom or a magnesium ion', 'Mg', 'Mg2+'), ('fluorine atom (F) or a fluoride ion', 'F-', 'F')):
    q = by(sub if 'which ion' not in sub else 'sort them by size'); checked.add(q['id'])
    first = re.match(r'([A-Z][a-z]?(?:\^\d*[+-])?)', txt(q['c'][0])).group(1).replace('^', '')
    ok(IONR[big] > IONR[small] and first == (small if 'smaller' in q['q'] else big), '%s %s %d pm > %s %d pm; c[0] starts %s' % (q['id'], big, IONR[big], small, IONR[small], first))

# ---------- coverage, counts, duplicates ----------
calc_ids = [q['id'] for q in ALL if q['k'] == 1]
for i in calc_ids:
    if i not in checked: err.append(i + ' calculation item not recomputed')
print('Items with a machine check: %d of %d (the rest are conceptual; read by hand)' % (len(checked), len(ALL)))
print('  not machine-checked:', ' '.join(q['id'] for q in ALL if q['id'] not in checked))
for nm, B in (('Try It', TRY), ('ADAPT', HW)):
    print(nm, len(B), dict(collections.Counter(q['t'] for q in B)), 'with figures:', sum(1 for q in B if q.get('f')),
          'd:', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1:', sum(q['k'] for q in B))
if len(HW) != 40: err.append('ADAPT has %d items, not 40' % len(HW))
dup = set(re.sub(r'\s+', ' ', q['q']) for q in TRY) & set(re.sub(r'\s+', ' ', q['q']) for q in HW)
if dup: err.append('same question in both banks: %s' % dup)
print('ERRORS:', err if err else 'none')
