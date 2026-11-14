#!/usr/bin/env python3
"""Scratch checker for Chapter 2 banks: structural checks copied from tools/check_bank_ch01.py
(ch02 topic ids) plus independent recomputation of every numeric answer and distractor, with the
course sig-fig rule (trailing zeros without a decimal point are not significant).
usage: python3 check_bank_ch02.py bank/ch02.json bank/ch02_adapt.json"""
import json, sys, re, collections, math
from decimal import Decimal, ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
TOP = {'ch02-theory', 'ch02-particles', 'ch02-table', 'ch02-ions', 'ch02-isotopes', 'ch02-mass'}
err = []

# ---------- structural checks (same as ch01 checker) ----------
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
            if f['type'] == 'particles':
                for b in f['boxes']:
                    for m in b['mols']:
                        for a in m:
                            if a not in f['key']: err.append(i + ' atom not in key ' + a)
        # wrong-choice feedback must not quote the right answer's text
        plain = lambda x: re.sub(r'<[^>]+>', '', x).strip().lower()
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if right in plain(q['y'][j]): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c2-%03d', 'TRY', True)
structural(HW, 'c2-h%02d', 'HW', False)

# ---------- helpers ----------
ALL = TRY + HW
def by(sub):
    m = [q for q in ALL if sub in q['q']]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
def plain(x): return re.sub(r'<[^>]+>', '', x).replace('&minus;', '-').replace('−', '-')
def has(q, j, s, why):
    ok = q is not None and s in plain(q['c'][j])
    print('  %-7s c[%d] %-42s %s %s' % (q['id'] if q else '?', j, repr(s), 'OK ' if ok else 'BAD', why))
    if not ok: err.append('%s c[%d] expected %r (%s)' % (q['id'] if q else '?', j, s, why))
def sf(s):
    """significant figures of a number written as a string (course rule)."""
    s = s.strip().lstrip('-')
    if 'e' in s.lower(): s = s.lower().split('e')[0]
    if '.' in s:
        d = s.replace('.', '').lstrip('0'); return len(d)
    d = s.lstrip('0').rstrip('0'); return len(d)
def rnd(x, place):  # round to 10**place, half up
    q = Decimal(1).scaleb(place)
    return Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP) if place < 0 else (Decimal(repr(x)) / q).quantize(Decimal(1), rounding=ROUND_HALF_UP) * q
def fmt(x, place): v = rnd(x, place); return ('%.' + str(max(0, -place)) + 'f') % float(v)
def lastplace(v, n): return math.floor(math.log10(abs(v))) - n + 1
def fmt_sf(v, n): return fmt(v, lastplace(v, n))
def avg_sig(iso, scale=100.0):
    """weighted average with each product limited to its sig figs, then the sum to the coarsest place."""
    tot, places = 0.0, []
    for m, p in iso:
        prod = float(m) * float(p) / scale
        n = min(sf(m) if '.' in m else 99, sf(p))
        places.append(lastplace(prod, n)); tot += prod
    return tot, max(places)
Z = dict(H=1, He=2, Li=3, B=5, C=6, N=7, O=8, F=9, Ne=10, Na=11, Mg=12, Al=13, P=15, S=16, Cl=17, Ar=18, K=19, Ca=20,
         V=23, Fe=26, Co=27, Ni=28, Cu=29, Zn=30, As=33, Se=34, Br=35, Kr=36, Rb=37, Tc=43, Rh=45, Cd=48, Sn=50, Te=52,
         I=53, Xe=54, Ba=56, Ir=77, Tl=81)
NAME = {v: k for k, v in Z.items()}
AMASS = dict(Zn=65.38, Sn=118.71, Se=78.97, Cu=63.55, Rb=85.4678)   # periodic-table values used by "rounded atomic mass" distractors

# ---------- average atomic mass items ----------
print('Average atomic mass (sig-fig rule: each product to its sig figs, sum to the coarsest decimal place)')
AVG = [  # (question substring, isotopes [(mass, percent)], {choice index: method})
    ('Natural boron is 19.9%', [('10.0129', '19.9'), ('11.0093', '80.1')], {1: 'simple', 2: 'pct', 3: 'swap'}),
    ('Natural potassium is almost all', [('38.964', '93.26'), ('40.962', '6.73')], {1: 'simple', 2: 'pct', 3: 'swap'}),
    ('Silver, used in some dental alloys', [('106.905', '51.84'), ('108.905', '48.16')], {1: 'simple', 2: 'swap', 3: 'pct'}),
    ('Neon has three natural isotopes', [('19.992', '90.48'), ('20.994', '0.27'), ('21.991', '9.25')], {1: 'drop1', 2: 'simple', 3: 'pct'}),
    ('Nitrogen is a major fertilizer element', [('14.003', '99.64'), ('15.000', '0.36')], {1: 'simple', 2: 'swap', 3: 'pct'}),
    ('Copper is 69.15% copper-63', [('62.930', '69.15'), ('64.928', '30.85')], {1: 'simple', 2: 'swap', 3: 'pct'}),
    ('Rubidium is 72.17%', [('84.912', '72.17'), ('86.909', '27.83')], {1: 'simple', 2: 'swap', 3: 'pct'}),
    ('Carbon is 98.93% carbon-12', [('12.000', '98.93'), ('13.003', '1.07')], {1: 'simple', 2: 'swap', 3: 'pct'}),
    ('Oxygen has three natural isotopes', [('15.995', '99.757'), ('16.999', '0.038'), ('17.999', '0.205')], {1: 'drop1', 2: 'simple', 3: 'pct'}),
    ('Element X has two isotopes', [('50', '25.0'), ('52', '75.0')], {1: 'simple', 2: 'swap', 3: 'pct'}),
]
for sub, iso, wr in AVG:
    q = by(sub)
    if not q: continue
    s = sum(float(p) for m, p in iso)
    if abs(s - 100) > 0.02: err.append(q['id'] + ' abundances sum to %.3f' % s)
    v, pl = avg_sig(iso); ans = fmt(v, pl)
    print(' %s %s: full %.5f -> %s amu (abundances sum %.3f)' % (q['id'], sub[:30], v, ans, s))
    has(q, 0, ans + ' amu', 'weighted average')
    lo, hi = min(float(m) for m, p in iso), max(float(m) for m, p in iso)
    if not lo < v < hi: err.append(q['id'] + ' average outside range')
    for j, how in wr.items():
        if how == 'simple': w = fmt(sum(float(m) for m, p in iso) / len(iso), pl)
        elif how == 'swap': w = fmt(float(iso[0][0]) * float(iso[1][1]) / 100 + float(iso[1][0]) * float(iso[0][1]) / 100, pl)
        elif how == 'drop1': w = fmt(sum(float(m) * float(p) / 100 for k, (m, p) in enumerate(iso) if k != 1), pl)
        elif how == 'pct': vv, pp = avg_sig(iso, 1.0); w = fmt(vv, pp)
        has(q, j, w + ' amu', how)
    # every number in w should show the answer
    if ans not in plain(q['w']): err.append(q['id'] + ' answer not in w')

print('Which isotope is more abundant (average vs midpoint of isotope masses)')
for sub, m1, m2, avg, right in [('Thallium has two natural isotopes', 202.9723, 204.9744, 204.38, 'Thallium-205'),
                                 ('Iridium has two natural isotopes', 190.9606, 192.9629, 192.22, 'Iridium-193')]:
    q = by(sub); mid = (m1 + m2) / 2; pick = right if (avg > mid) == ('205' in right or '193' in right) else '??'
    print('  %s midpoint %.3f, average %.2f -> heavier isotope more abundant: %s' % (q['id'], mid, avg, avg > mid))
    if not (avg > mid and q['c'][0] == right): err.append(q['id'] + ' abundance call')
q = by('Silver, used in some dental alloys'); print('  silver midpoint %.3f (w says 107.905)' % ((106.905 + 108.905) / 2))
q = by('gets 6355 amu')
v, pl = avg_sig([('62.93', '69.15'), ('64.93', '30.85')]); vp, pp = avg_sig([('62.93', '69.15'), ('64.93', '30.85')], 1.0)
print('  %s copper: weighted %s, with percents %s, simple %s, swapped %s' % (q['id'], fmt(v, pl), fmt(vp, pp), fmt((62.93 + 64.93) / 2, pl), fmt(62.93 * .3085 + 64.93 * .6915, -1)))
if fmt(vp, pp) != '6355' or fmt(v, pl) != '63.55' or '63.55' not in q['w'] or '63.93' not in q['y'][1] or '64.3' not in q['y'][2]: err.append(q['id'] + ' copper numbers')

# ---------- particle counts ----------
print('Particle counts (protons = Z, neutrons = A - Z, electrons = Z - charge)')
def pne(sym, A=None, ch=0):
    p = Z[sym]; return p, (A - p if A else None), p - ch
q = by('Zinc (Z = 30) is a trace element'); p, n, e = pne('Zn')
has(q, 0, '%d protons and %d electrons' % (p, e), 'neutral Zn'); has(q, 1, '%d protons' % round(AMASS['Zn']), 'rounded atomic mass')
has(q, 2, 'and %d electrons' % (round(AMASS['Zn']) - p), 'A - Z as electrons')
q = by('A neutral atom has 53 electrons'); has(q, 0, NAME_FULL := 'Iodine', 'Z=53 -> I'); assert NAME[53] == 'I' and NAME[54] == 'Xe' and NAME[52] == 'Te'
q = by('every particle in one atom'); f = q['f'][0]['boxes']; P = sum(m == ['p'] for m in f[0]['mols']); N = sum(m == ['n'] for m in f[0]['mols']); E = len(f[1]['mols'])
print('  %s figure: %d p, %d n, %d e -> %s, charge %d; p+n=%d (%s), n=%d (%s)' % (q['id'], P, N, E, NAME[P], P - E, P + N, NAME[P + N], N, NAME[N]))
if not (NAME[P] == 'F' and P == E and NAME[P + N] == 'K' and NAME[N] == 'Ne'): err.append(q['id'] + ' F figure')
q = by('About how many electrons would it take'); r = 1.0073 / 0.00055; print('  %s proton/electron mass ratio %.0f' % (q['id'], r))
if not 1700 < r < 1900: err.append(q['id'] + ' ratio')
q = by('12 protons, 12 neutrons and 12 electrons'); print('  %s Z=12 %s, Z=13 %s' % (q['id'], NAME[12], NAME[13]))
q = by('fluoride ion</b>, F'); p, n, e = pne('F', None, -1)
has(q, 0, '%d protons and %d electrons' % (p, e), 'F-'); has(q, 1, '%d protons and %d electrons' % (p, p - 1), 'sign backward')
has(q, 2, '%d protons and %d electrons' % (p + 1, e), 'charge added to protons'); has(q, 3, '%d protons and %d electrons' % (p, p), 'neutral')
q = by('Many enzymes in the body hold a zinc ion'); p, n, e = pne('Zn', None, 2)
has(q, 0, '%d protons and %d electrons' % (p, e), 'Zn2+'); has(q, 1, '%d protons and %d electrons' % (p, p + 2), 'sign backward')
has(q, 2, '%d protons and %d electrons' % (p - 2, p - 2), 'charge taken from protons'); has(q, 3, '%d protons and %d electrons' % (p, p), 'neutral')
q = by('A monatomic ion has 34 protons and 36 electrons'); print('  %s Z=34 %s charge %d; Z=36 %s; Z=35 %s' % (q['id'], NAME[34], 34 - 36, NAME[36], NAME[35]))
q = by('all the protons, neutrons and electrons of one particle'); f = q['f'][0]['boxes']; P = sum(m == ['p'] for m in f[0]['mols']); N = sum(m == ['n'] for m in f[0]['mols']); E = len(f[1]['mols'])
print('  %s figure: %d p, %d n, %d e -> %s charge %+d; Z=e %s; Z=p+n %s' % (q['id'], P, N, E, NAME[P], P - E, NAME[E], NAME[P + N]))
if not (NAME[P] == 'O' and P - E == -2 and NAME[E] == 'Ne' and NAME[P + N] == 'S'): err.append(q['id'] + ' O figure')
q = by('Iron supplements and hemoglobin'); print('  %s Fe2+ e=%d, Fe3+ e=%d, Z=27 %s' % (q['id'], 26 - 2, 26 - 3, NAME[27]))
if '24' not in q['y'][0] or '23' not in q['y'][0]: err.append(q['id'] + ' Fe electrons')
q = by('Stannous fluoride toothpaste'); p, n, e = pne('Sn', None, 2)
has(q, 0, '%d protons and %d electrons' % (p, e), 'Sn2+'); has(q, 1, '%d protons and %d electrons' % (p, p + 2), 'sign')
has(q, 2, '%d protons and %d electrons' % (p - 2, p - 2), 'protons changed (Z=48 %s)' % NAME[48]); has(q, 3, '%d protons and %d electrons' % (round(AMASS['Sn']), round(AMASS['Sn']) - 2), 'atomic mass as Z')
q = by('Technetium-99m is the most'); has(q, 0, str(99 - Z['Tc']), 'A-Z'); has(q, 1, '99', 'A'); has(q, 2, '43', 'Z'); has(q, 3, str(99 + 43), 'A+Z')
q = by('Iodine-123 and iodine-131 are both'); has(q, 0, str((131 - 53) - (123 - 53)), 'difference'); has(q, 2, str(131 - 53), 'I-131 n'); has(q, 3, str(123 - 53), 'I-123 n')
q = by('Thallium-201, given as'); p, n, e = pne('Tl', 201, 1)
has(q, 0, '%d protons, %d neutrons, %d electrons' % (p, n, e), 'Tl+'); has(q, 1, '%d protons, %d neutrons, %d electrons' % (p, n, p + 1), 'sign')
has(q, 2, '%d protons, %d neutrons, %d electrons' % (p, 201, e), 'A as n'); has(q, 3, '%d protons, %d neutrons, %d electrons' % (p, n - 1, e), 'charge on neutrons')
q = by('Fluorine-18 is used in PET'); print('  %s F-18: A=%d Z=%d; Z=18 is %s' % (q['id'], 9 + 9, Z['F'], NAME[18]))
if q['c'][0] != '<sup>18</sup><sub>9</sub>F': err.append(q['id'] + ' F-18 symbol')
q = by('urea breath test for'); f = q['f'][0]['boxes']; P = sum(m == ['p'] for m in f[0]['mols']); N = sum(m == ['n'] for m in f[0]['mols']); E = len(f[1]['mols'])
print('  %s figure: %d p %d n %d e -> %s-%d; Z=n %s; Z=A %s' % (q['id'], P, N, E, NAME[P], P + N, NAME[N], NAME[P + N]))
if not (NAME[P] == 'C' and P + N == 13 and P == E and NAME[N] == 'N' and NAME[P + N] == 'Al'): err.append(q['id'] + ' C-13 figure')
q = by('Researchers trace nitrogen fertilizer'); print('  %s N-14 n=%d, N-15 n=%d, O-16 n=%d' % (q['id'], 14 - 7, 15 - 7, 16 - 8))
q = by('The thyroid absorbs radioactive iodine-131'); print('  %s I-131 n=%d, I-127 n=%d' % (q['id'], 131 - 53, 127 - 53))
if '(78 and 74)' not in q['y'][2]: err.append(q['id'] + ' neutrons')
q = by('Xenon-133 gas'); has(q, 0, '54', 'e=Z'); has(q, 2, str(133 - 54), 'neutrons'); has(q, 3, str(133 + 54), 'A+Z')
# ADAPT counts
q = by('Selenium (Z = 34) is a trace'); has(q, 0, '34 protons and 34 electrons', 'neutral Se'); has(q, 1, '%d protons' % round(AMASS['Se']), 'atomic mass'); has(q, 2, 'and %d electrons' % (round(AMASS['Se']) - 34), 'A-Z'); has(q, 3, 'and %d electrons' % (34 + 2), 'Se2-')
q = by('A neutral atom has 27 electrons'); print('  %s Z=27 %s, 28 %s, 26 %s' % (q['id'], NAME[27], NAME[28], NAME[26]))
q = by('Copper (Z = 29) is a trace'); has(q, 0, '29 protons and 29 electrons', 'neutral'); has(q, 1, '%d protons' % round(AMASS['Cu']), 'atomic mass'); has(q, 2, 'and %d electrons' % (round(AMASS['Cu']) - 29), 'A-Z')
q = by('If an atom were enlarged'); x = 100 / 100000; print('  %s nucleus %.4f m = %.1f mm; 1 cm=100/%d; 1 m=100/%d; 100*1e5 m = %.0f km' % (q['id'], x, x * 1000, 100 / 0.01, 100 / 1, 100 * 1e5 / 1000))
q = by('Barium in X-ray contrast'); p, n, e = pne('Ba', None, 2)
has(q, 0, '%d protons and %d electrons' % (p, e), 'Ba2+'); has(q, 1, '%d protons and %d electrons' % (p, p + 2), 'sign'); has(q, 2, '%d protons and %d electrons' % (p - 2, p - 2), 'protons changed (Z=54 %s)' % NAME[54]); has(q, 3, '%d protons and %d electrons' % (p, p), 'neutral')
q = by('An ion has 26 protons and 23 electrons'); print('  %s Z=26 %s charge %+d; Z=23 %s' % (q['id'], NAME[26], 26 - 23, NAME[23]))
q = by('phosphide ion, P'); p, n, e = pne('P', None, -3)
has(q, 0, '%d protons and %d electrons' % (p, e), 'P3-'); has(q, 1, '%d protons and %d electrons' % (p, p - 3), 'sign'); has(q, 2, '%d protons and %d electrons' % (e, e), 'protons changed'); has(q, 3, '%d protons and %d electrons' % (p, p), 'neutral')
q = by('same number of electrons as a neutral neon'); print('  %s Na+ %d, K+ %d, Cl- %d, Ca2+ %d (Ne %d)' % (q['id'], 11 - 1, 19 - 1, 17 + 1, 20 - 2, Z['Ne']))
q = by('An ion has 53 protons and 54 electrons'); print('  %s charge %+d' % (q['id'], 53 - 54))
q = by('Iodine-123 is used for thyroid imaging'); p, n, e = pne('I', 123, 0)
has(q, 0, '%d protons, %d neutrons, %d electrons' % (p, n, e), 'I-123'); has(q, 1, '%d neutrons' % 123, 'A as n'); has(q, 2, '%d protons, %d neutrons' % (n, p), 'swapped'); has(q, 3, '%d electrons' % n, 'e = n')
q = by('Cobalt-60 is a radiation source'); has(q, 0, str(60 - 27), 'A-Z'); has(q, 3, str(60 + 27), 'A+Z')
q = by('Rubidium-82 is used'); print('  %s A=%d; Z=45 %s; rounded mass %d' % (q['id'], 37 + 45, NAME[45], round(AMASS['Rb'])))
q = by('Carbon-14 and nitrogen-14 have the same'); print('  %s C-14 n=%d, N-14 n=%d' % (q['id'], 14 - 6, 14 - 7))
q = by('Iodide in iodized salt'); p, n, e = pne('I', 127, -1)
has(q, 0, '%d protons, %d neutrons, %d electrons' % (p, n, e), 'I-127-'); has(q, 1, '%d neutrons, %d electrons' % (n, p - 1), 'sign'); has(q, 2, '%d neutrons' % 127, 'A as n'); has(q, 3, '%d neutrons' % (n - 1), 'charge on n')
q = by('Potassium-40 is a naturally'); has(q, 0, str(40 - 19), 'A-Z'); has(q, 3, str(39 - 19), 'K-39 neutrons')

# ---------- other calculations, with sig figs ----------
print('Other calculations (sig figs by the multiplication/division rule)')
def calc(sub, j, val, n, unit, why):
    q = by(sub); has(q, j, fmt_sf(val, n) + ' ' + unit, why + ' = %.5g -> %d s.f.' % (val, n))
calc('chewable antacids', 0, 1.25 * 0.400, 3, 'g', '1.25 x 0.400'); calc('chewable antacids', 1, 1.25 / 0.400, 3, 'g', '1.25 / 0.400')
calc('chewable antacids', 2, 1.25 * 40.0, 3, 'g', '1.25 x 40.0'); calc('chewable antacids', 3, 1.25 * 0.600, 3, 'g', '1.25 x 0.600')
calc('sample of sterile water', 0, 36.0 / 9.00 * 7.99, 3, 'g', '36.0/9.00 x 7.99'); calc('sample of sterile water', 1, 36.0 / 9.00 * 1.01, 3, 'g', '4.00 x 1.01')
calc('sample of sterile water', 3, 36.0 * 7.99, 3, 'g', '36.0 x 7.99')
calc('Sodium fluoride, used in some', 0, 2.50 * 0.452, 3, 'g', '2.50 x 0.452'); calc('Sodium fluoride, used in some', 1, 2.50 / 0.452, 3, 'g', '2.50 / 0.452')
calc('Sodium fluoride, used in some', 2, 2.50 * 45.2, 3, 'g', '2.50 x 45.2'); calc('Sodium fluoride, used in some', 3, 2.50 * (1 - 0.452), 3, 'g', '2.50 x 0.548')
calc('Anhydrous ammonia', 0, 41.2 * 1.77 / 8.23, 3, 'g', '41.2 x 1.77/8.23'); calc('Anhydrous ammonia', 2, 41.2 * 8.23 / 1.77, 3, 'g', '41.2 x 8.23/1.77')
calc('Anhydrous ammonia', 3, 41.2 * 0.177, 3, 'g', '41.2 x 0.177')
print('  real compositions: CaCO3 %%Ca %.2f, H2O %%O %.2f (given 7.99/9.00 = %.2f), NaF %%F %.2f, NH3 %%H %.2f (given %.1f)' % (
    100 * 40.078 / 100.086, 100 * 15.999 / 18.015, 100 * 7.99 / 9.00, 100 * 18.998 / 41.988, 100 * 3 * 1.008 / 17.031, 100 * 1.77 / 10.00))

# ---------- counts ----------
for nm, B in (('Try It', TRY), ('ADAPT', HW)):
    print(nm, len(B), dict(collections.Counter(q['t'] for q in B)), 'with figures:', sum(1 for q in B if q.get('f')),
          'd:', dict(collections.Counter(q['d'] for q in B)), 'k=1:', sum(q['k'] for q in B))
# ids/questions shared between the two banks?
dup = set(re.sub(r'\s+', ' ', q['q']) for q in TRY) & set(re.sub(r'\s+', ' ', q['q']) for q in HW)
if dup: err.append('same question in both banks: %s' % dup)
print('ERRORS:', err if err else 'none')
