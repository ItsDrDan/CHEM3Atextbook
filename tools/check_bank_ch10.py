#!/usr/bin/env python3
"""Checker for the Chapter 10 banks (kinetic molecular theory, pressure, gas laws, ideal gas law, gas stoichiometry,
Dalton's law). Structural checks as in tools/check_bank_ch09.py (ch10 topic ids; ADAPT = 42 items, text only, y[0]
begins "Correct: "; tables at most 3 columns; figures only of fbx types table/plot), plus, written independently of
the generators:
  - every calculation item (k=1): the key and each numeric distractor's intended error recomputed with Decimal from
    the givens as written in the stem, TWO ways: (a) round once (exact T = C + 273.15, exact P_atm - P_H2O, carried
    to the end) and (b) strict (the kelvin value and the over-water difference rounded first by the addition rule,
    then used); the item is an error unless both agree, so every key is unambiguous;
  - sig figs by the multiplication rule from the givens (kelvins counted as written by the addition rule;
    760, 101.325, 273.15 and mole ratios exact; 14.7 psi, 22.4 L/mol, R = 0.082058 and 62.36 counted), sums and
    differences by the decimal-place rule;
  - every "C + 273.15 = K" written anywhere is rechecked; every quoted R, 22.4 L/mol, pressure equality and water
    vapor pressure is the chapter's value; vapor-pressure and air tables are read and checked;
  - every equation anywhere is parsed back out of the HTML and must balance; stoichiometry mole ratios are read
    from the stem's own equation;
  - every quoted molar mass is the checker's own (yellow-sheet atomic masses, addition rule);
  - conceptual items: a gas-law key table (variables related, direct/inverse, which are held constant), speed and
    density by molar mass, altitude by elevation, Dalton (partial pressure set by own moles) and the R/unit rules
    are used to recheck keys; the rest are listed as read by hand;
  - course rule: no whole number ending in 0 without a decimal point in a calculation stem;
  - exactly one correct choice (recomputed values all different; four different choices);
  - no stem reuses a draft worked example or exercise (two shared givens with a draft block, or one of the listed
    worked-example givens); no stem in both banks.
usage: python3 tools/check_bank_ch10.py bank/ch10.json bank/ch10_adapt.json"""
import json, sys, re, os, collections, glob
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 50; getcontext().rounding = ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YS = json.load(open(os.path.join(ROOT, 'tools', 'yellow_sheet_masses.json')))
AM = YS['masses']
TOP = {'ch10-kmt', 'ch10-pressure', 'ch10-laws', 'ch10-ideal', 'ch10-stoich', 'ch10-dalton'}
err = []

# ---------- text ----------
def txt(x):
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<[^>]+>', '', x)
    for a, b in (('&middot;', '·'), ('&minus;', '-'), ('−', '-'), ('&times;', 'x'), ('&nbsp;', ' '), ('&divide;', '/'),
                 ('&rarr;', '->'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&deg;', '°'), ('&ndash;', '–'), ('&lt;', '<'),
                 ('&gt;', '>'), ('&prop;', '∝'), ('&frac12;', '½'), ('&amp;', '&')):
        x = x.replace(a, b)
    return x
def plain(x): return re.sub(r'\s+', ' ', txt(x)).strip().lower()

# ---------- structural checks ----------
OUT_OF_SCOPE = r"Graham|effusion rate|van der Waals|root[- ]mean[- ]square|rms speed|Hess|all of the above|none of the above"
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
        if len(set(plain(c) for c in q['c'])) != 4: err.append(i + ' dup choice')
        for k in ('q', 'h', 'w'):
            if not str(q.get(k, '')).strip(): err.append(i + ' empty ' + k)
        if q.get('d') not in (1, 2, 3): err.append(i + ' bad d')
        if q.get('k') not in (0, 1): err.append(i + ' bad k')
        s = ' '.join([q['q'], q['h'], q['w']] + q['c'] + q['y'])
        for tg in ('sub', 'sup', 'b', 'i'):
            if len(re.findall('<%s>' % tg, s)) != len(re.findall('</%s>' % tg, s)): err.append(i + ' unbalanced <%s>' % tg)
        if re.search(r'&(?!(?:[a-zA-Z]+\d*|#\d+);)', s): err.append(i + ' bare &')
        if '{' in s or '}' in s or '[[' in s or ']]' in s: err.append(i + ' unconverted markup')
        if re.search(r'(?<![\w;])-(?=\d)', s): err.append(i + ' hyphen used as a minus sign')
        if re.search(OUT_OF_SCOPE, s, re.I): err.append(i + ' out of scope term or AOTA/NOTA')
        if 'f' in q and not allow_f: err.append(i + ' has f (ADAPT items must be text only)')
        for f in q.get('f', []):
            if f['type'] == 'table':
                if max(len(f['head']), *[len(r) for r in f['rows']]) > 3: err.append(i + ' table wider than 3 columns')
                if max(len(plain(x)) for r in f['rows'] + [f['head']] for x in r) > 32: err.append(i + ' table cell too long for a phone')
            elif f['type'] != 'plot': err.append(i + ' figure type not checked here: ' + f['type'])
        if label == 'HW' and not q['y'][0].startswith('Correct: '): err.append(i + ' ADAPT y[0] lacks "Correct: "')
        if label == 'TRY' and q['y'][0].startswith('Correct'): err.append(i + ' Try It y[0] starts with "Correct"')
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if re.search(r'(?<![\d.])' + re.escape(right) + r'(?![\d])', plain(q['y'][j])): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c10-%03d', 'TRY', True)
structural(HW, 'c10-h%02d', 'HW', False)
if len(HW) != 42: err.append('ADAPT has %d items, not 42' % len(HW))
if sum(1 for q in TRY if q.get('f')) > 4: err.append('more than 4 figures')
fbx = open(os.path.join(ROOT, 'js', 'fbx.js'), encoding='utf-8').read()
for t_ in {f['type'] for q in TRY for f in q.get('f', [])}:
    if not re.search(r'[{,]%s:' % t_, fbx): err.append('figure type %s not supported by js/fbx.js' % t_)
wid = open(os.path.join(ROOT, 'js', 'widget.js'), encoding='utf-8').read()
for t_ in TOP:
    if "'%s'" % t_ not in wid: err.append('topic %s missing from js/widget.js TOPICS' % t_)
WANT_T = {'ch10-kmt': 9, 'ch10-pressure': 10, 'ch10-laws': 15, 'ch10-ideal': 13, 'ch10-stoich': 11, 'ch10-dalton': 12}
WANT_H = {'ch10-kmt': 5, 'ch10-pressure': 6, 'ch10-laws': 9, 'ch10-ideal': 8, 'ch10-stoich': 7, 'ch10-dalton': 7}
for nm, B, W in (('Try It', TRY, WANT_T), ('ADAPT', HW, WANT_H)):
    got = dict(collections.Counter(q['t'] for q in B))
    if got != W: err.append('%s topic counts %s, planned %s' % (nm, got, W))
ALL = TRY + HW

def ok(cond, msg):
    print('   ', 'OK ' if cond else 'BAD', msg)
    if not cond: err.append(msg)

# ---------- numbers ----------
def sf(s):
    s = s.strip().lstrip('+-')
    if 'e' in s.lower(): s = s.lower().split('e')[0]
    if '.' in s: return len(s.replace('.', '').lstrip('0'))
    return len(s.lstrip('0').rstrip('0'))
def dec(s): return len(s.partition('.')[2])
def fmt(v, n):
    m, e = format(D(v), '.%de' % (n - 1)).split('e'); e = int(e)
    if e < -3 or e > n - 1: return '%s x 10^%d' % (m, e)
    s = format(D(m) * D(10) ** e, 'f')
    want_dec = n - 1 - e
    if want_dec > 0:
        ip, _, fp = s.partition('.'); s = ip + '.' + (fp + '0' * want_dec)[:want_dec]
    else:
        s = s.split('.')[0]
        if s.endswith('0'): s += '.'
    return s
def rq(v, d): return format(D(v).quantize(D(10) ** -d), 'f')
def U(v, n, u=''): return (fmt(v, n) + ' ' + u).strip()
def N(*a): return min(x if isinstance(x, int) else sf(x) for x in a)
def ADD(*s):
    """sum of strings as written ('-x' subtracts), decimal-place rule."""
    return rq(sum(D(x) for x in s), min(dec(x.lstrip('-')) for x in s))

# ---------- constants (Chapter 10 text) ----------
E273 = D('273.15'); MMHG = D(760); KPA = D('101.325'); PA = D(101325); PSI = D('14.7')
R = D('0.082058'); R2 = D('62.36'); VM = D('22.4'); TSTP = D(273)
VPW = {'20.0': '17.5', '25.0': '23.8', '30.0': '31.8', '37.0': '47.1'}
def K(c, m):
    """kelvins from a Celsius string: m=0 carried exactly, m=1 rounded by the addition rule first."""
    v = D(c) + E273
    return v if m == 0 else D(rq(v, dec(c)))
def nK(c): return sf(rq(D(c) + E273, dec(c)))
def DRY(pa, pw, m):
    """P_atm - P_H2O: m=0 exact, m=1 rounded by the decimal-place rule first."""
    return D(pa) - D(pw) if m == 0 else D(ADD(pa, '-' + pw))
def nDRY(pa, pw): return sf(ADD(pa, '-' + pw))

# ---------- formulas, molar masses, equations ----------
def atoms(f):
    stack = [collections.Counter()]; i = 0
    while i < len(f):
        if f[i] == '(':
            stack.append(collections.Counter()); i += 1
        elif f[i] == ')':
            j = i + 1
            while j < len(f) and f[j].isdigit(): j += 1
            g = stack.pop()
            for k, v in g.items(): stack[-1][k] += v * int(f[i + 1:j] or 1)
            i = j
        else:
            m = re.match(r'([A-Z][a-z]?)(\d*)', f[i:])
            if not m or m.group(1) not in AM: raise ValueError(f)
            stack[-1][m.group(1)] += int(m.group(2) or 1); i += m.end()
    return stack[0]
def MM(f):
    c = atoms(f); q = min(len(AM[e].partition('.')[2]) for e in c)
    return sum((D(AM[e]) * n for e, n in c.items()), D(0)).quantize(D(10) ** -q)
for f, want in (('CO2', '44.009'), ('H2O', '18.015'), ('C6H12O6', '180.156'), ('CH4', '16.043'), ('NH3', '17.031'),
                ('CaCO3', '100.09'), ('C3H8', '44.097'), ('O2', '31.998'), ('N2', '28.014')):
    if str(MM(f)) != want: err.append('checker molar mass %s = %s, text says %s' % (f, MM(f), want))
NAMES = {'water': 'H2O', 'glucose': 'C6H12O6', 'zinc': 'Zn', 'methane': 'CH4'}
print('Quoted molar masses against the yellow sheet (addition rule)')
nmm = 0
for q in ALL:
    for h in [q['q'], q['w'], q['h']] + q['c'] + q['y']:
        t = txt(h)
        hits = re.findall(r'([A-Za-z][A-Za-z0-9()]*)(?: molecules| atoms)?,? \(([\d.]+) g/mol\)', t)
        hits += re.findall(r'([A-Z][A-Za-z0-9()]*), ([\d.]+) g/mol', t)
        for f, v in hits:
            f = NAMES.get(f.lower(), f) if f[0].islower() or f.lower() in NAMES else f
            try: want = str(MM(f))
            except ValueError: err.append('%s unknown formula %r before %s g/mol' % (q['id'], f, v)); continue
            nmm += 1
            if want != v: err.append('%s quotes %s %s g/mol; checker %s' % (q['id'], f, v, want))
        for v in re.findall(r'(?<![\d.])([\d.]+) g/mol', t):
            if not any(v == hv for _, hv in hits) and not re.search(r'= ' + re.escape(v) + ' g/mol|' + re.escape(v) + r' g/mol(?:\)|,)? *$', t):
                if q['k'] == 0: err.append('%s quotes %s g/mol with no formula' % (q['id'], v))
print('    %d molar masses quoted, all recomputed' % nmm)

SPC = r'(?:\d+ )?[A-Z(][A-Za-z0-9()]*(?:\((?:s|l|g|aq)\))?'
EQRE = re.compile(SPC + r'(?: \+ ' + SPC + r')* -> ' + SPC + r'(?: \+ ' + SPC + r')*')
def sp(tok):
    m = re.fullmatch(r'(\d+) (.+)', tok.strip()); co = int(m.group(1)) if m else 1
    t = m.group(2) if m else tok.strip()
    m = re.fullmatch(r'(.+?)\((s|l|g|aq)\)', t); ph = None
    if m: t, ph = m.group(1), m.group(2)
    atoms(t); return co, t, ph
def parse_eq(s):
    L, R_ = s.split(' -> ')
    return [sp(t) for t in L.split(' + ')], [sp(t) for t in R_.split(' + ')]
def eqs_in(h):
    out = []
    for m in EQRE.finditer(txt(h)):
        try: out.append((m.group(), parse_eq(m.group())))
        except ValueError: pass
    return out
def balanced(e):
    def side(S):
        c = collections.Counter()
        for co, f, ph in S:
            for el, n in atoms(f).items(): c[el] += co * n
        return c
    return side(e[0]) == side(e[1])
print('Equations (every field) balance')
neq = 0
for q in ALL:
    for h in [q['q'], q['h'], q['w']] + q['c'] + q['y']:
        for s_, e in eqs_in(h):
            neq += 1
            if not balanced(e): err.append('%s unbalanced equation %s' % (q['id'], s_))
print('    %d equations parsed, all balanced' % neq)

# ---------- quoted constants, kelvin conversions ----------
print('Quoted constants, vapor pressures and every "C + 273.15 = K" in the text')
nk = 0
for q in ALL:
    s = txt(' '.join([q['q'], q['w'], q['h']] + q['c'] + q['y']))
    for v in re.findall(r'R = (\d+\.\d+)', s):
        if v not in ('0.082058', '62.36', '8.3144'): err.append('%s quotes R = %s' % (q['id'], v))
    for v in re.findall(r'([\d.]+) L/mol', s):
        if v != '22.4' and not (v == '25.5' and 'about 25.5' in s): err.append('%s quotes %s L/mol' % (q['id'], v))
    for a, u in re.findall(r'1 atm = ([\d.,]+) (\w+)', s):
        if {'mmHg': '760', 'torr': '760', 'kPa': '101.325', 'Pa': '101,325', 'psi': '14.7'}.get(u) != a: err.append('%s quotes 1 atm = %s %s' % (q['id'], a, u))
    for v, c in re.findall(r'([\d.]+) mmHg at ([\d.]+) °C', s) + [(b, a) for a, b in re.findall(r'at ([\d.]+) °C is ([\d.]+) mmHg', s)]:
        if VPW.get(c) != v: err.append('%s quotes water vapor pressure %s mmHg at %s °C' % (q['id'], v, c))
    for c, k in re.findall(r'(-?[\d.]+) \+ 273\.15 = ([\d.]+) K', s):
        nk += 1
        if rq(D(c) + E273, dec(c)) != k: err.append('%s writes %s + 273.15 = %s K' % (q['id'], c, k))
print('    %d kelvin conversions rechecked' % nk)

# ---------- calculation items ----------
def by(sub):
    m = [q for q in ALL if sub in txt(q['q'])]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
checked, hand = set(), set()
g = D
CUR = {}
def CO(f):
    for side in CUR['eq']:
        for co, ff, ph in side:
            if ff == f: return D(co)
    raise KeyError(f)
def RT(a, b): return CO(b) / CO(a)          # mol b per mol a from the stem's equation
CALC = []
def calc(sub, givens, specs): CALC.append((sub, givens, specs))

# ---- ch10-pressure ----
calc('reads 742 mmHg', ['742'], {0: lambda m: U(g(742) / MMHG, 3, 'atm'), 1: lambda m: U(g(742) * MMHG, 3, 'atm'), 2: lambda m: U(g(742) / KPA, 3, 'atm'), 3: lambda m: U(g(742) / PSI, 3, 'atm')})
calc('pressurized to 2.40 atm', ['2.40'], {0: lambda m: U(g('2.40') * KPA, 3, 'kPa'), 1: lambda m: U(g('2.40') * PA, 3, 'kPa'), 2: lambda m: U(g('2.40') / KPA, 3, 'kPa'), 3: lambda m: U(g('2.40') * MMHG, 3, 'kPa')})
calc('inflated to 85.5 psi', ['85.5'], {0: lambda m: U(g('85.5') / PSI, 3, 'atm'), 1: lambda m: U(g('85.5') * PSI, 3, 'atm'), 2: lambda m: U(g('85.5') / MMHG, 3, 'atm'), 3: lambda m: U(g('85.5') / KPA, 3, 'atm')})
calc('pressure is 41.5 mmHg', ['41.5'], {0: lambda m: U(g('41.5') * KPA / MMHG, 3, 'kPa'), 1: lambda m: U(g('41.5') * KPA, 3, 'kPa'), 2: lambda m: U(g('41.5') / KPA, 3, 'kPa'), 3: lambda m: U(g('41.5') * MMHG / KPA, 3, 'kPa')})
calc('flask to 18.6 torr', ['18.6'], {0: lambda m: U(g('18.6') / MMHG, 3, 'atm'), 1: lambda m: U(g('18.6') * MMHG, 3, 'atm'), 2: lambda m: U(g('18.6') / KPA, 3, 'atm'), 3: lambda m: U(g('18.6') / PSI, 3, 'atm')})
calc('as 101.9 kPa', ['101.9'], {0: lambda m: U(g('101.9') * MMHG / KPA, 4, 'mmHg'), 1: lambda m: U(g('101.9') * MMHG, 4, 'mmHg'), 2: lambda m: U(g('101.9') / MMHG, 4, 'mmHg'), 3: lambda m: U(g('101.9') * KPA / MMHG, 4, 'mmHg')})
calc('runs at 2.85 atm', ['2.85'], {0: lambda m: U(g('2.85') * MMHG, 3, 'mmHg'), 1: lambda m: U(g('2.85') / MMHG, 3, 'mmHg'), 2: lambda m: U(g('2.85') * KPA, 3, 'mmHg'), 3: lambda m: U(g('2.85') * PSI, 3, 'mmHg')})
calc('inflated to 34.5 psi', ['34.5'], {0: lambda m: U(g('34.5') / PSI * KPA, 3, 'kPa'), 1: lambda m: U(g('34.5') * PSI * KPA, 3, 'kPa'), 2: lambda m: U(g('34.5') * PSI / KPA, 3, 'kPa'), 3: lambda m: U(g('34.5') * KPA, 3, 'kPa')})
calc('is 95.5 mmHg', ['95.5'], {0: lambda m: U(g('95.5') / MMHG, 3, 'atm'), 1: lambda m: U(g('95.5') * MMHG, 3, 'atm'), 2: lambda m: U(g('95.5') / KPA, 3, 'atm'), 3: lambda m: U(g('95.5') / PSI, 3, 'atm')})
calc('pressurized to 78.5 kPa', ['78.5'], {0: lambda m: U(g('78.5') / KPA, 3, 'atm'), 1: lambda m: U(g('78.5') * KPA, 3, 'atm'), 2: lambda m: U(g('78.5') / MMHG, 3, 'atm'), 3: lambda m: U(g('78.5') / PA, 3, 'atm')})

# ---- ch10-laws ----
n_ = N('3.45', '1.60', '1.05')
calc('volume of 1.60 mL where the pressure is 3.45 atm', ['1.60', '3.45', '1.05'], {0: lambda m: U(g('3.45') * g('1.60') / g('1.05'), n_, 'mL'), 1: lambda m: U(g('1.60') * g('1.05') / g('3.45'), n_, 'mL'), 2: lambda m: U(g('3.45') * g('1.60'), n_, 'mL'), 3: lambda m: U(g('3.45') * g('1.05') / g('1.60'), n_, 'mL')})
calc('occupies 4.25 L at 0.955 atm', ['4.25', '0.955', '1.65'], {0: lambda m: U(g('0.955') * g('4.25') / g('1.65'), 3, 'atm'), 1: lambda m: U(g('0.955') * g('1.65') / g('4.25'), 3, 'atm'), 2: lambda m: U(g('0.955') * g('4.25'), 3, 'atm'), 3: lambda m: U(g('4.25') * g('1.65') / g('0.955'), 3, 'atm')})
calc('from 2.40 L to 2.52 L', ['2.40', '2.52', '760.'], {0: lambda m: U(g(760) * g('2.40') / g('2.52'), N('760.', '2.40', '2.52'), 'mmHg'), 1: lambda m: U(g(760) * g('2.52') / g('2.40'), 3, 'mmHg'), 2: lambda m: U(g(760) * g('2.40'), 3, 'mmHg'), 3: lambda m: U(g('2.40') / g('2.52'), 3, 'mmHg')})
n_ = N('1.85', nK('24.5'), nK('-18.5'))
calc('A 1.85 L balloon at 24.5 °C', ['1.85', '24.5', '-18.5'], {0: lambda m: U(g('1.85') * K('-18.5', m) / K('24.5', m), n_, 'L'), 1: lambda m: U(g('1.85') * g('-18.5') / g('24.5'), n_, 'L'), 2: lambda m: U(g('1.85') * K('24.5', m) / K('-18.5', m), n_, 'L'), 3: lambda m: U(g('1.85') * K('-18.5', m) / g('24.5'), n_, 'L')})
n_ = N('45.0', '49.5', nK('20.5'))
calc('holds 45.0 mL of air at 20.5 °C', ['45.0', '20.5', '49.5'], {0: lambda m: U(K('20.5', m) * g('49.5') / g('45.0'), n_, 'K'), 1: lambda m: U(g('20.5') * g('49.5') / g('45.0'), n_, 'K'), 2: lambda m: U(K('20.5', m) * g('45.0') / g('49.5'), n_, 'K'), 3: lambda m: U(K('20.5', m) * g('49.5') / g('45.0'), n_, '°C')})
n_ = N('1.85', nK('21.5'), nK('425'))
calc('gas at 1.85 atm at 21.5 °C', ['1.85', '21.5', '425'], {0: lambda m: U(g('1.85') * K('425', m) / K('21.5', m), n_, 'atm'), 1: lambda m: U(g('1.85') * g(425) / g('21.5'), n_, 'atm'), 2: lambda m: U(g('1.85') * K('21.5', m) / K('425', m), n_, 'atm'), 3: lambda m: U(g('1.85') * g(425) / K('21.5', m), n_, 'atm')})
n_ = N('2.25', '2.48', nK('15.5'))
calc('at 2.25 atm at 15.5 °C', ['2.25', '15.5', '2.48'], {0: lambda m: U(K('15.5', m) * g('2.48') / g('2.25'), n_, 'K'), 1: lambda m: U(g('15.5') * g('2.48') / g('2.25'), n_, 'K'), 2: lambda m: U(K('15.5', m) * g('2.25') / g('2.48'), n_, 'K'), 3: lambda m: U(K('15.5', m) * g('2.48') / g('2.25'), n_, '°C')})
calc('holds 0.245 mol of helium', ['0.245', '5.80', '0.185'], {0: lambda m: U(g('5.80') * g('0.185') / g('0.245'), 3, 'L'), 1: lambda m: U(g('5.80') * g('0.245') / g('0.185'), 3, 'L'), 2: lambda m: U(g('5.80') * (g('0.245') - g('0.185')) / g('0.245'), 3, 'L'), 3: lambda m: U(g('0.185') / g('0.245'), 3, 'L')})
n_ = N('2.65', '1.12', '0.875', nK('18.5'), nK('37.5'))
def _comb(V1, P1, P2, T1, T2): return g(V1) * g(P1) / g(P2) * T2 / T1
calc('nitrogen occupies 2.65 L', ['2.65', '1.12', '18.5', '0.875', '37.5'], {0: lambda m: U(_comb('2.65', '1.12', '0.875', K('18.5', m), K('37.5', m)), n_, 'L'), 1: lambda m: U(_comb('2.65', '1.12', '0.875', g('18.5'), g('37.5')), n_, 'L'),
     2: lambda m: U(_comb('2.65', '0.875', '1.12', K('18.5', m), K('37.5', m)), n_, 'L'), 3: lambda m: U(_comb('2.65', '1.12', '0.875', K('37.5', m), K('18.5', m)), n_, 'L')})
n_ = N('11.5', '1.01', '18.4', nK('23.5'), nK('-8.5'))
calc('helium balloon holds 11.5 L', ['11.5', '1.01', '23.5', '18.4', '-8.5'], {0: lambda m: U(_comb('1.01', '11.5', '18.4', K('23.5', m), K('-8.5', m)), n_, 'atm'), 1: lambda m: U(_comb('1.01', '11.5', '18.4', g('23.5'), g('-8.5')), n_, 'atm'),
     2: lambda m: U(_comb('1.01', '18.4', '11.5', K('23.5', m), K('-8.5', m)), n_, 'atm'), 3: lambda m: U(_comb('1.01', '11.5', '18.4', K('-8.5', m), K('23.5', m)), n_, 'atm')})
calc('convert -12.5 °C to kelvins', ['-12.5'], {0: lambda m: rq(g('-12.5') + E273, 1) + ' K', 1: lambda m: rq(g('12.5') + E273, 1) + ' K', 2: lambda m: rq(g('-12.5') - E273, 1) + ' K', 3: lambda m: str(g('-12.5') + E273) + ' K'})
n_ = N('1.35', '745', '1.12')
calc('occupies 1.35 L at 745 mmHg', ['1.35', '745', '1.12'], {0: lambda m: U(g('1.35') * g(745) / MMHG / g('1.12'), n_, 'L'), 1: lambda m: U(g('1.35') * g(745) / g('1.12'), n_, 'L'), 2: lambda m: U(g('1.35') * g('1.12') / (g(745) / MMHG), n_, 'L'), 3: lambda m: U(g('1.35') * g(745) / MMHG, n_, 'L')})
n_ = N('3.85', nK('20.5'), nK('46.5'))
calc('A 3.85 L balloon at 20.5 °C', ['3.85', '20.5', '46.5'], {0: lambda m: U(g('3.85') * K('46.5', m) / K('20.5', m), n_, 'L'), 1: lambda m: U(g('3.85') * g('46.5') / g('20.5'), n_, 'L'), 2: lambda m: U(g('3.85') * K('20.5', m) / K('46.5', m), n_, 'L'), 3: lambda m: U(g('3.85') * g('46.5') / K('20.5', m), n_, 'L')})
n_ = N('138', nK('19.5'), nK('41.5'))
calc('is at 138 atm at 19.5 °C', ['138', '19.5', '41.5'], {0: lambda m: U(g(138) * K('41.5', m) / K('19.5', m), n_, 'atm'), 1: lambda m: U(g(138) * g('41.5') / g('19.5'), n_, 'atm'), 2: lambda m: U(g(138) * K('19.5', m) / K('41.5', m), n_, 'atm'), 3: lambda m: U(g(138) * K('41.5', m) / g('19.5'), n_, 'atm')})
n_ = N('1.55', '2.05', nK('22.5'))
calc('at 1.55 atm and 22.5 °C', ['1.55', '22.5', '2.05'], {0: lambda m: U(K('22.5', m) * g('2.05') / g('1.55'), n_, 'K'), 1: lambda m: U(g('22.5') * g('2.05') / g('1.55'), n_, 'K'), 2: lambda m: U(K('22.5', m) * g('1.55') / g('2.05'), n_, 'K'), 3: lambda m: U(K('22.5', m) * g('2.05') / g('1.55'), n_, '°C')})
calc('holds 0.190 mol of air at 4.65 L', ['0.190', '4.65', '6.20'], {0: lambda m: U(g('0.190') * g('6.20') / g('4.65'), 3, 'mol'), 1: lambda m: U(g('0.190') * g('4.65') / g('6.20'), 3, 'mol'), 2: lambda m: U(g('0.190') * g('6.20') / g('4.65') - g('0.190'), 3, 'mol'), 3: lambda m: U(g('6.20') / VM, 3, 'mol')})
n_ = N('186', '741', nK('25.5'), '273')
calc('collects 186 mL of dry gas', ['186', '741', '25.5'], {0: lambda m: U(g(186) * g(741) / MMHG * TSTP / K('25.5', m), n_, 'mL'), 1: lambda m: U(g(186) * g(741) * TSTP / K('25.5', m), n_, 'mL'),
     2: lambda m: U(g(186) * g(741) / MMHG * K('25.5', m) / TSTP, n_, 'mL'), 3: lambda m: U(g(186) * MMHG / g(741) * TSTP / K('25.5', m), n_, 'mL')})
n_ = N('2.20', '1.05', '1.85', '1.42', nK('17.5'))
calc('occupies 2.20 L at 1.05 atm and 17.5 °C', ['2.20', '1.05', '17.5', '1.85', '1.42'], {0: lambda m: U(K('17.5', m) * g('1.42') * g('1.85') / (g('1.05') * g('2.20')), n_, 'K'), 1: lambda m: U(g('17.5') * g('1.42') * g('1.85') / (g('1.05') * g('2.20')), n_, 'K'),
     2: lambda m: U(K('17.5', m) * g('1.05') * g('2.20') / (g('1.42') * g('1.85')), n_, 'K'), 3: lambda m: U(K('17.5', m) * g('1.42') / g('1.05'), n_, 'K')})

# ---- ch10-ideal ----
def nPV(P, V, T): return P * V / (R * T)
n_ = N('3.75', '8.65', nK('22.5'), '0.082058')
calc('3.75 L tank of helium', ['3.75', '8.65', '22.5'], {0: lambda m: U(nPV(g('8.65'), g('3.75'), K('22.5', m)), n_, 'mol'), 1: lambda m: U(nPV(g('8.65'), g('3.75'), g('22.5')), n_, 'mol'), 2: lambda m: U(g('3.75') / VM, n_, 'mol'), 3: lambda m: U(1 / nPV(g('8.65'), g('3.75'), K('22.5', m)), n_, 'mol')})
n_ = N('0.685', '1.15', nK('31.5'))
calc('0.685 mol of CO2', ['0.685', '1.15', '31.5'], {0: lambda m: U(g('0.685') * R * K('31.5', m) / g('1.15'), n_, 'L'), 1: lambda m: U(g('0.685') * R * g('31.5') / g('1.15'), n_, 'L'), 2: lambda m: U(g('0.685') * VM, n_, 'L'), 3: lambda m: U(g('0.685') * R * K('31.5', m), n_, 'L')})
n_ = N('0.0425', '1.25', nK('24.0'), '62.36')
calc('holds 0.0425 mol of nitrous oxide', ['1.25', '0.0425', '24.0'], {0: lambda m: U(g('0.0425') * R2 * K('24.0', m) / g('1.25'), n_, 'torr'), 1: lambda m: U(g('0.0425') * R * K('24.0', m) / g('1.25'), n_, 'torr'),
     2: lambda m: U(g('0.0425') * R2 * g('24.0') / g('1.25'), n_, 'torr'), 3: lambda m: U(g('0.0425') * R * K('24.0', m) / g('1.25') / MMHG, n_, 'torr')})
calc('contains 0.415 mol of argon', ['5.25', '0.415', '2.05'], {0: lambda m: U(g('2.05') * g('5.25') / (g('0.415') * R), 3, 'K'), 1: lambda m: U(g('0.415') * R / (g('2.05') * g('5.25')), 3, 'K'), 2: lambda m: U(g('2.05') * g('5.25') / (g('0.415') * R2), 3, 'K'), 3: lambda m: U(g('2.05') * g('5.25') / (g('0.415') * R), 3, '°C')})
n_ = N('285', '738', nK('21.5'))
calc('285 mL flask holds argon', ['285', '738', '21.5'], {0: lambda m: U(nPV(g(738) / MMHG, g('0.285'), K('21.5', m)), n_, 'mol'), 1: lambda m: U(nPV(g(738), g('0.285'), K('21.5', m)), n_, 'mol'),
     2: lambda m: U(nPV(g(738) / MMHG, g(285), K('21.5', m)), n_, 'mol'), 3: lambda m: U(nPV(g(738) / MMHG, g('0.285'), g('21.5')), n_, 'mol')})
calc('0.365 mol of O2 occupy at STP', ['0.365'], {0: lambda m: U(g('0.365') * VM, 3, 'L'), 1: lambda m: U(g('0.365') / VM, 3, 'L'), 2: lambda m: U(VM / g('0.365'), 3, 'L'), 3: lambda m: U(g('0.365') * R * g('298.15'), 3, 'L')})
calc('7.25 g of methane', ['7.25'], {0: lambda m: U(g('7.25') / MM('CH4') * VM, 3, 'L'), 1: lambda m: U(g('7.25') * VM, 3, 'L'), 2: lambda m: U(g('7.25') / VM, 3, 'L'), 3: lambda m: U(g('7.25') / MM('CH4') / VM, 3, 'L')})
n_ = N('1.45', '0.825', '1.05', nK('27.5'))
calc('1.45 g sample of an unknown gas', ['1.45', '0.825', '1.05', '27.5'], {0: lambda m: U(g('1.45') / nPV(g('1.05'), g('0.825'), K('27.5', m)), n_, 'g/mol'), 1: lambda m: U(g('1.45') / nPV(g('1.05'), g('0.825'), g('27.5')), n_, 'g/mol'),
     2: lambda m: U(nPV(g('1.05'), g('0.825'), K('27.5', m)) / g('1.45'), n_, 'g/mol'), 3: lambda m: U(g('1.45') / g('0.825'), n_, 'g/mol')})
calc('0.842 g sample of a gas', ['0.842', '625'], {0: lambda m: U(g('0.842') / g('0.625'), 3, 'g/L'), 1: lambda m: U(g('0.842') / g(625), 3, 'g/L'), 2: lambda m: U(g('0.625') / g('0.842'), 3, 'g/L'), 3: lambda m: U(g('0.842') * g('0.625'), 3, 'g/L')})
n_ = N('0.645', '12.5', nK('24.5'))
calc('holds 0.645 mol of oxygen', ['12.5', '0.645', '24.5'], {0: lambda m: U(g('0.645') * R * K('24.5', m) / g('12.5'), n_, 'atm'), 1: lambda m: U(g('0.645') * R * g('24.5') / g('12.5'), n_, 'atm'), 2: lambda m: U(g('0.645') * VM / g('12.5'), n_, 'atm'), 3: lambda m: U(g('0.645') * R * K('24.5', m), n_, 'atm')})
n_ = N('2.15', '0.985', nK('37.0'))
calc('2.15 x 10^-3 mol of CO2', ['37.0', '0.985'], {0: lambda m: U(g('2.15e-3') * R * K('37.0', m) / g('0.985') * 1000, n_, 'mL'), 1: lambda m: U(g('2.15e-3') * R * g('37.0') / g('0.985') * 1000, n_, 'mL'),
     2: lambda m: U(g('2.15e-3') * R * K('37.0', m) / g('0.985'), n_, 'mL'), 3: lambda m: U(g('2.15e-3') * VM * 1000, n_, 'mL')})
n_ = N('2.75', '632', nK('26.5'), '62.36')
calc('contains neon at 632 torr', ['2.75', '632', '26.5'], {0: lambda m: U(g(632) * g('2.75') / (R2 * K('26.5', m)), n_, 'mol'), 1: lambda m: U(nPV(g(632), g('2.75'), K('26.5', m)), n_, 'mol'),
     2: lambda m: U(g(632) * g('2.75') / (R2 * g('26.5')), n_, 'mol'), 3: lambda m: U(g(632) / MMHG * g('2.75') / (R2 * K('26.5', m)), n_, 'mol')})
calc('holds 0.312 mol of nitrogen', ['6.50', '0.312', '1.27'], {0: lambda m: U(g('1.27') * g('6.50') / (g('0.312') * R), 3, 'K'), 1: lambda m: U(g('0.312') * R / (g('1.27') * g('6.50')), 3, 'K'), 2: lambda m: U(g('1.27') * g('6.50') / (g('0.312') * R2), 3, 'K'), 3: lambda m: U(g('1.27') * g('6.50') / (g('0.312') * R), 3, '°C')})
calc('in 8.65 L of N2 at STP', ['8.65'], {0: lambda m: U(g('8.65') / VM, 3, 'mol'), 1: lambda m: U(g('8.65') * VM, 3, 'mol'), 2: lambda m: U(VM / g('8.65'), 3, 'mol'), 3: lambda m: U(g('8.65') / (R * g('298.15')), 3, 'mol')})
n_ = N('0.635', '345', '0.968', nK('23.5'))
calc('0.635 g sample of a gas', ['0.635', '345', '0.968', '23.5'], {0: lambda m: U(g('0.635') / nPV(g('0.968'), g('0.345'), K('23.5', m)), n_, 'g/mol'), 1: lambda m: U(g('0.635') / nPV(g('0.968'), g(345), K('23.5', m)), n_, 'g/mol'),
     2: lambda m: U(g('0.635') / nPV(g('0.968'), g('0.345'), g('23.5')), n_, 'g/mol'), 3: lambda m: U(nPV(g('0.968'), g('0.345'), K('23.5', m)) / g('0.635'), n_, 'g/mol')})

# ---- ch10-stoich (mole ratios read from the stem's equation) ----
calc('from 8.50 g of H2O2', ['8.50'], {0: lambda m: U(g('8.50') / MM('H2O2') * RT('H2O2', 'O2') * VM, 3, 'L'), 1: lambda m: U(g('8.50') / MM('H2O2') * VM, 3, 'L'), 2: lambda m: U(g('8.50') / MM('H2O2') / RT('H2O2', 'O2') * VM, 3, 'L'), 3: lambda m: U(g('8.50') * RT('H2O2', 'O2') * VM, 3, 'L')})
calc('from 6.72 L of N2 at STP', ['6.72'], {0: lambda m: U(g('6.72') / VM * RT('N2', 'NH3') * MM('NH3'), 3, 'g'), 1: lambda m: U(g('6.72') / VM * MM('NH3'), 3, 'g'), 2: lambda m: U(g('6.72') / VM / RT('N2', 'NH3') * MM('NH3'), 3, 'g'), 3: lambda m: U(g('6.72') * RT('N2', 'NH3') * MM('NH3'), 3, 'g')})
n_ = N('3.65', '0.975', nK('27.5'))
_pr = lambda: g('3.65') / MM('C3H8')
calc('from 3.65 g of C3H8', ['3.65', '0.975', '27.5'], {0: lambda m: U(_pr() * RT('C3H8', 'CO2') * R * K('27.5', m) / g('0.975'), n_, 'L'), 1: lambda m: U(_pr() * RT('C3H8', 'CO2') * VM, n_, 'L'),
     2: lambda m: U(_pr() * R * K('27.5', m) / g('0.975'), n_, 'L'), 3: lambda m: U(_pr() * RT('C3H8', 'CO2') * R * g('27.5') / g('0.975'), n_, 'L')})
n_ = N('0.385', '0.982', nK('23.5'))
calc('make 0.385 L of H2', ['0.385', '0.982', '23.5'], {0: lambda m: U(nPV(g('0.982'), g('0.385'), K('23.5', m)) * RT('H2', 'Zn') * g(AM['Zn']), n_, 'g'), 1: lambda m: U(nPV(g('0.982'), g('0.385'), g('23.5')) * RT('H2', 'Zn') * g(AM['Zn']), n_, 'g'),
     2: lambda m: U(g('0.385') / VM * RT('H2', 'Zn') * g(AM['Zn']), n_, 'g'), 3: lambda m: U(nPV(g('0.982'), g('0.385'), K('23.5', m)) * RT('H2', 'HCl') * g(AM['Zn']), n_, 'g')})
calc('when 3.20 L of C2H6 burns', ['3.20'], {0: lambda m: U(g('3.20') * RT('C2H6', 'H2O'), 3, 'L'), 1: lambda m: U(g('3.20') / RT('C2H6', 'H2O'), 3, 'L'), 2: lambda m: U(g('3.20'), 3, 'L'), 3: lambda m: U(g('3.20') * CO('H2O'), 3, 'L')})
n_ = N('4.25', '1.02', nK('22.5'))
_kc = lambda: g('4.25') / MM('KClO3')
calc('from 4.25 g of KClO3', ['4.25', '1.02', '22.5'], {0: lambda m: U(_kc() * RT('KClO3', 'O2') * R * K('22.5', m) / g('1.02'), n_, 'L'), 1: lambda m: U(_kc() * R * K('22.5', m) / g('1.02'), n_, 'L'),
     2: lambda m: U(_kc() / RT('KClO3', 'O2') * R * K('22.5', m) / g('1.02'), n_, 'L'), 3: lambda m: U(_kc() * RT('KClO3', 'O2') * R * g('22.5') / g('1.02'), n_, 'L')})
calc('from 15.5 g of glucose', ['15.5'], {0: lambda m: U(g('15.5') / MM('C6H12O6') * RT('C6H12O6', 'CO2') * VM, 3, 'L'), 1: lambda m: U(g('15.5') / MM('C6H12O6') * VM, 3, 'L'), 2: lambda m: U(g('15.5') * RT('C6H12O6', 'CO2') * VM, 3, 'L'), 3: lambda m: U(g('15.5') / MM('C6H12O6') * RT('C6H12O6', 'CO2') / VM, 3, 'L')})
calc('from 0.575 L of N2O', ['0.575'], {0: lambda m: U(g('0.575') * RT('N2O', 'O2'), 3, 'L'), 1: lambda m: U(g('0.575') / RT('N2O', 'O2'), 3, 'L'), 2: lambda m: U(g('0.575'), 3, 'L'), 3: lambda m: U(g('0.575') / VM * RT('N2O', 'O2'), 3, 'L')})
n_ = N('0.750', '0.988', nK('37.0'))
_cc = lambda: g('0.750') / MM('CaCO3') * RT('CaCO3', 'CO2')
calc('from 0.750 g of CaCO3', ['0.750', '0.988', '37.0'], {0: lambda m: U(_cc() * R * K('37.0', m) / g('0.988'), n_, 'L'), 1: lambda m: U(_cc() * VM, n_, 'L'), 2: lambda m: U(_cc() * R * g('37.0') / g('0.988'), n_, 'L'), 3: lambda m: U(_cc() * RT('CaCO3', 'HCl') * R * K('37.0', m) / g('0.988'), n_, 'L')})
n_ = N('5.35', '1.10', nK('19.5'))
_o = lambda m: nPV(g('1.10'), g('5.35'), K('19.5', m))
calc('uses up 5.35 L of O2', ['5.35', '1.10', '19.5'], {0: lambda m: U(_o(m) * RT('O2', 'CH4') * MM('CH4'), n_, 'g'), 1: lambda m: U(_o(m) * MM('CH4'), n_, 'g'), 2: lambda m: U(_o(m) / RT('O2', 'CH4') * MM('CH4'), n_, 'g'), 3: lambda m: U(g('5.35') / VM * RT('O2', 'CH4') * MM('CH4'), n_, 'g')})
calc('from 2.65 L of N2', ['2.65'], {0: lambda m: U(g('2.65') * RT('N2', 'NO'), 3, 'L'), 1: lambda m: U(g('2.65') / RT('N2', 'NO'), 3, 'L'), 2: lambda m: U(g('2.65'), 3, 'L'), 3: lambda m: U(g('2.65') / VM * RT('N2', 'NO'), 3, 'L')})
calc('with 4.15 g of Na', ['4.15'], {0: lambda m: U(g('4.15') / MM('Na') * RT('Na', 'Cl2') * VM, 3, 'L'), 1: lambda m: U(g('4.15') / MM('Na') * VM, 3, 'L'), 2: lambda m: U(g('4.15') / MM('Na') / RT('Na', 'Cl2') * VM, 3, 'L'), 3: lambda m: U(g('4.15') * RT('Na', 'Cl2') * VM, 3, 'L')})
n_ = N('25.5', '0.995', nK('32.5'))
_gl = lambda: g('25.5') / MM('C6H12O6')
calc('from 25.5 g of glucose', ['25.5', '0.995', '32.5'], {0: lambda m: U(_gl() * RT('C6H12O6', 'CO2') * R * K('32.5', m) / g('0.995'), n_, 'L'), 1: lambda m: U(_gl() * RT('C6H12O6', 'CO2') * VM, n_, 'L'),
     2: lambda m: U(_gl() * R * K('32.5', m) / g('0.995'), n_, 'L'), 3: lambda m: U(_gl() * RT('C6H12O6', 'CO2') * R * g('32.5') / g('0.995'), n_, 'L')})
n_ = N('1.45', '0.978', nK('24.5'))
_ox = lambda m: nPV(g('0.978'), g('1.45'), K('24.5', m))
calc('give 1.45 L of O2', ['1.45', '0.978', '24.5'], {0: lambda m: U(_ox(m) * RT('O2', 'H2O2') * MM('H2O2'), n_, 'g'), 1: lambda m: U(_ox(m) * MM('H2O2'), n_, 'g'), 2: lambda m: U(_ox(m) / RT('O2', 'H2O2') * MM('H2O2'), n_, 'g'), 3: lambda m: U(g('1.45') / VM * RT('O2', 'H2O2') * MM('H2O2'), n_, 'g')})
n_ = N('2.85', '1.05', nK('21.5'), '22.4')
_me = lambda: g('2.85') / VM * RT('CH4', 'O2')
calc('A 2.85 L sample of CH4', ['2.85', '1.05', '21.5'], {0: lambda m: U(_me() * R * K('21.5', m) / g('1.05'), n_, 'L'), 1: lambda m: U(g('2.85') * RT('CH4', 'O2'), n_, 'L'), 2: lambda m: U(g('2.85') / VM * R * K('21.5', m) / g('1.05'), n_, 'L'), 3: lambda m: U(_me() * R * g('21.5') / g('1.05'), n_, 'L')})
calc('from 14.2 g of KO2', ['14.2'], {0: lambda m: U(g('14.2') / MM('KO2') * RT('KO2', 'O2') * VM, 3, 'L'), 1: lambda m: U(g('14.2') / MM('KO2') * VM, 3, 'L'), 2: lambda m: U(g('14.2') / MM('KO2') / RT('KO2', 'O2') * VM, 3, 'L'), 3: lambda m: U(g('14.2') * RT('KO2', 'O2') * VM, 3, 'L')})

# ---- ch10-dalton ----
calc('O2 is 6.82 atm', ['6.82', '13.9'], {0: lambda m: ADD('6.82', '13.9') + ' atm', 1: lambda m: ADD('13.9', '-6.82') + ' atm', 2: lambda m: rq((g('6.82') + g('13.9')) / 2, 1) + ' atm', 3: lambda m: str(g('6.82') + g('13.9')) + ' atm'})
calc('total pressure of 2.65 atm', ['2.65', '1.95'], {0: lambda m: ADD('2.65', '-1.95') + ' atm', 1: lambda m: ADD('2.65', '1.95') + ' atm', 2: lambda m: U(g('1.95') / g('2.65'), 3, 'atm'), 3: lambda m: U(g('2.65') / 2, 3, 'atm')})
_t3 = ADD('0.385', '0.125', '0.0400')
calc('0.385 mol N2, 0.125 mol O2', ['0.385', '0.125', '0.0400'], {0: lambda m: U(g('0.125') / g(_t3), N('0.125', _t3)), 1: lambda m: '0.125', 2: lambda m: U(g('0.125') / g('0.385'), 3), 3: lambda m: U(g(_t3) / g('0.125'), 3)})
calc('mole fraction of N2O is 0.650', ['1.02', '0.650'], {0: lambda m: U(g('0.650') * g('1.02'), 3, 'atm'), 1: lambda m: U(g('0.650') / g('1.02'), 3, 'atm'), 2: lambda m: U(g('1.02') / g('0.650'), 3, 'atm'), 3: lambda m: U((1 - g('0.650')) * g('1.02'), 3, 'atm')})
calc('78.1% N2 by moles', ['78.1', '749'], {0: lambda m: U(g('78.1') / 100 * g(749), 3, 'mmHg'), 1: lambda m: U(g('78.1') * g(749), 3, 'mmHg'), 2: lambda m: U(g(749) / (g('78.1') / 100), 3, 'mmHg'), 3: lambda m: ADD('749', '-78.1') + ' mmHg'})
_t6 = ADD('4.45', '1.15')
calc('holds 4.45 mol of helium', ['4.45', '1.15', '165'], {0: lambda m: U(g('1.15') / g(_t6) * 165, N('1.15', _t6, '165'), 'atm'), 1: lambda m: U(g('1.15') / g('4.45') * 165, 3, 'atm'), 2: lambda m: U(g('4.45') / g(_t6) * 165, 3, 'atm'), 3: lambda m: U(g('1.15') * 165, 3, 'atm')})
def _vp_table(q):
    rows = {r[0]: r[1] for r in q['f'][0]['rows']}
    ok(rows == VPW, '%s vapor-pressure table = chapter values %s' % (q['id'], rows))
    return rows
calc('oxygen over water at 30.0 °C when the room pressure is 751 mmHg', ['30.0', '751'], {0: lambda m: ADD('751', '-' + VPW['30.0']) + ' mmHg', 1: lambda m: ADD('751', '-' + VPW['25.0']) + ' mmHg', 2: lambda m: ADD('751', VPW['30.0']) + ' mmHg', 3: lambda m: '751 mmHg'})
n_ = N('48.5', nDRY('746', '17.5'), nK('20.0'))
calc('collects 48.5 mL of oxygen', ['48.5', '20.0', '746', '17.5'], {0: lambda m: U(nPV(DRY('746', '17.5', m) / MMHG, g('0.0485'), K('20.0', m)), n_, 'mol'), 1: lambda m: U(nPV(g(746) / MMHG, g('0.0485'), K('20.0', m)), n_, 'mol'),
     2: lambda m: U(nPV(DRY('746', '17.5', m), g('0.0485'), K('20.0', m)), n_, 'mol'), 3: lambda m: U(nPV((g(746) + g('17.5')) / MMHG, g('0.0485'), K('20.0', m)), n_, 'mol')})
AIR = {}
def _air(q):
    rows = {txt(r[0]): D(r[1].rstrip('%')) for r in q['f'][0]['rows']}
    ok(rows == {'N2': D('78.08'), 'O2': D('20.95'), 'Ar': D('0.93')}, '%s dry-air table (standard composition, by moles) %s' % (q['id'], {k: str(v) for k, v in rows.items()}))
    AIR.update(rows)
calc('about 438 mmHg', ['438'], {0: lambda m: U(AIR['O2'] / 100 * 438, N(str(AIR['O2']), '438'), 'mmHg'), 1: lambda m: U(AIR['O2'] * 438, 3, 'mmHg'), 2: lambda m: U(AIR['O2'] / 100 * 760, 3, 'mmHg'), 3: lambda m: U(g(438) / (AIR['O2'] / 100), 3, 'mmHg')})
n_ = N('0.285', nDRY('758', '47.1'))
calc('mole fraction of about 0.285', ['0.285', '47.1', '758', '37.0'], {0: lambda m: U(g('0.285') * DRY('758', '47.1', m), n_, 'mmHg'), 1: lambda m: U(g('0.285') * 758, n_, 'mmHg'), 2: lambda m: U(g('0.285') * (g(758) + g('47.1')), n_, 'mmHg'), 3: lambda m: U((1 - g('0.285')) * DRY('758', '47.1', m), n_, 'mmHg')})
calc('N2 at 569 mmHg', ['569', '116', '28.5', '47.1'], {0: lambda m: ADD('569', '116', '28.5', '47.1') + ' mmHg', 1: lambda m: ADD('569', '116', '28.5') + ' mmHg', 2: lambda m: U((g(569) + g(116) + g('28.5') + g('47.1')) / 4, 3, 'mmHg'), 3: lambda m: str(g(569) + g(116) + g('28.5') + g('47.1')) + ' mmHg'})
calc('32.0% O2 by moles', ['32.0', '2.45'], {0: lambda m: U(g('32.0') / 100 * g('2.45'), 3, 'atm'), 1: lambda m: U(g('32.0') * g('2.45'), 3, 'atm'), 2: lambda m: U(g('2.45') / g('0.320'), 3, 'atm'), 3: lambda m: U((1 - g('0.320')) * g('2.45'), 3, 'atm')})
_t8 = ADD('0.275', '0.0850')
calc('0.275 mol of argon and 0.0850 mol of neon', ['0.275', '0.0850', '1.45'], {0: lambda m: U(g('0.0850') / g(_t8) * g('1.45'), N('0.0850', _t8, '1.45'), 'atm'), 1: lambda m: U(g('0.0850') / g('0.275') * g('1.45'), 3, 'atm'), 2: lambda m: U(g('0.275') / g(_t8) * g('1.45'), 3, 'atm'), 3: lambda m: U(g('0.0850') * g('1.45'), 3, 'atm')})
calc('barometer reads 744 mmHg', ['744', '31.8', '47.1'], {0: lambda m: ADD('744', '-47.1') + ' mmHg', 1: lambda m: ADD('744', '-31.8') + ' mmHg', 2: lambda m: ADD('744', '47.1') + ' mmHg', 3: lambda m: '744 mmHg'})
n_ = N('62.5', nDRY('765', '31.8'), nK('30.0'))
calc('62.5 mL of H2 is collected', ['62.5', '30.0', '765', '31.8'], {0: lambda m: U(nPV(DRY('765', '31.8', m) / MMHG, g('0.0625'), K('30.0', m)), n_, 'mol'), 1: lambda m: U(nPV(g(765) / MMHG, g('0.0625'), K('30.0', m)), n_, 'mol'),
     2: lambda m: U(nPV(DRY('765', '31.8', m) / MMHG, g('62.5'), K('30.0', m)), n_, 'mol'), 3: lambda m: U(nPV(DRY('765', '31.8', m), g('0.0625'), K('30.0', m)), n_, 'mol')})
calc('mole fraction of N2 is 0.715', ['3.60', '0.715'], {0: lambda m: U((1 - g('0.715')) * g('3.60'), 3, 'atm'), 1: lambda m: U(g('0.715') * g('3.60'), 3, 'atm'), 2: lambda m: str(1 - g('0.715')) + ' atm', 3: lambda m: ADD('3.60', '-0.715') + ' atm'})

print('Calculation items: key and distractors recomputed (round once = strict, and = the choice as written)')
for sub, givens, specs in CALC:
    q = by(sub)
    if not q: continue
    checked.add(q['id']); stem = txt(q['q']); figt = ' '.join(txt(x) for f in q.get('f', []) for r in f.get('rows', []) for x in r)
    if q.get('f'):
        if 'Vapor' in q['f'][0].get('cap', ''): _vp_table(q)
        if 'air' in q['f'][0].get('cap', ''): _air(q)
    eqs = eqs_in(q['q']); CUR['eq'] = eqs[0][1] if eqs else ([], [])
    for gv in givens:
        pat = r'(?<![\d.])' + re.escape(gv) + r'(?![\d])'
        if not re.search(pat, stem) and not re.search(pat, figt): err.append(q['id'] + ' given %r not in stem as written' % gv)
    print('  %s %s' % (q['id'], sub[:52]))
    keys = []
    for j, fn in sorted(specs.items()):
        try: a, b = fn(0), fn(1)
        except Exception as e_: err.append('%s c[%d] spec failed: %r' % (q['id'], j, e_)); continue
        if a != b: err.append('%s c[%d] ambiguous: %s (round once) vs %s (strict)' % (q['id'], j, a, b))
        keys.append(a)
        ok(txt(q['c'][j]).strip() == a, '%s c[%d] %-26r = %r' % (q['id'], j, txt(q['c'][j]).strip(), a))
    if len(set(keys)) != 4: err.append(q['id'] + ' recomputed values not all different: %s' % keys)
    k0 = keys[0].split(' ')[0] if keys else ''
    if k0 and k0 not in txt(q['w']): err.append(q['id'] + ' answer %s not in w' % k0)
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')

# ---------- conceptual items: key tables ----------
print('Conceptual items checked against key tables')
LAWS = {"Boyle": ({'P', 'V'}, 'inverse', {'T', 'n'}), "Charles": ({'V', 'T'}, 'direct', {'P', 'n'}),
        "Gay-Lussac": ({'P', 'T'}, 'direct', {'V', 'n'}), "Avogadro": ({'V', 'n'}, 'direct', {'P', 'T'})}
WORD = {'P': 'pressure', 'V': 'volume', 'T': 'temperature', 'n': 'amount'}
def law_for(changed, const):
    return [k for k, (vs, rel, cs) in LAWS.items() if changed <= vs and const <= cs]
def chk(sub, cond, msg):
    q = by(sub)
    if q: checked.add(q['id']); ok(cond(q), '%s %s' % (q['id'], msg))
chk("In Gay-Lussac's law, which two variables", lambda q: all(WORD[v] in plain(q['c'][0]) for v in LAWS['Gay-Lussac'][2]) and all(not all(WORD[v] in plain(c) for v in LAWS['Gay-Lussac'][2]) for c in q['c'][1:]),
    'Gay-Lussac holds %s constant; only c[0] names both' % sorted(LAWS['Gay-Lussac'][2]))
chk('moved from a warm room into a freezer', lambda q: law_for({'V', 'T'}, {'P', 'n'}) == ['Charles'] and LAWS['Charles'][1] == 'direct' and plain(q['c'][0]).startswith('it decreases') and 'direct' in plain(q['c'][0]),
    'Charles (direct): T down -> V down')
def vfactor(pf, tf): return D(tf) / D(pf)   # V ∝ T/P
chk('amount of gas doubled, and at the same time its Kelvin temperature is doubled', lambda q: D(2) * 2 / 1 == 4 and 'four times' in plain(q['c'][0]), 'P ∝ nT/V: x2 x2 -> x4')
chk('pressure on a gas is tripled', lambda q: vfactor(3, 1) == D(1) / 3 and 'one-third' in plain(q['c'][0]), 'Boyle: x3 P -> x1/3 V')
chk('cuff of a patient', lambda q: law_for({'P', 'V'}, {'T', 'n'}) == ['Boyle'] and plain(q['c'][0]).startswith("boyle"), 'T and n constant, P and V change -> Boyle')
def _pv(q):
    rows = [(D(a), D(b)) for a, b in q['f'][0]['rows']]
    prods = {p * v for p, v in rows}; ratios = {p / v for p, v in rows}
    return len(prods) == 1 and len(ratios) == len(rows) and 'inverse' in plain(q['c'][0]) and 'boyle' in plain(q['c'][0]) and str(prods.pop()) in ('6.0000', '6.000', '6.00000')
chk('The table shows data for a gas sample at constant temperature', _pv, 'P x V constant (6.00 atm·L), P/V not constant -> inverse, Boyle')
def mm_choices(q): return [D(x) for x in re.findall(r'\(([\d.]+) g/mol\)', ' '.join(txt(c) for c in q['c']))]
chk('which atoms move fastest', lambda q: (lambda ms: len(ms) == 4 and ms[0] == min(ms))(mm_choices(q)), 'fastest = smallest molar mass')
chk('lowest average molecular speed', lambda q: (lambda ms: len(ms) == 4 and ms[0] == max(ms))(mm_choices(q)), 'slowest = largest molar mass')
chk('which gas has the greatest density', lambda q: (lambda ms: len(ms) == 4 and ms[0] == max(ms))(mm_choices(q)), 'same T and P: densest = largest molar mass')
chk('white ring of NH4Cl', lambda q: MM('NH3') < MM('HCl') and 'hcl end' in plain(q['c'][0]) and 'nh3' in plain(q['c'][0]).split('because')[1], 'NH3 (%s) lighter than HCl (%s): faster, ring near HCl end' % (MM('NH3'), MM('HCl')))
chk('How do the average kinetic energies', lambda q: 'same' in plain(q['c'][0]), 'same T -> same average KE')
chk('Kelvin temperature of a gas sample is doubled', lambda q: plain(q['c'][0]) == 'it doubles.', 'KE ∝ T(K)')
REAL = {'less ideal': ('cool', 'high pressure', 'condens'), 'more ideal': ('heat', 'lower', 'expand')}
chk('depart more from ideal-gas behavior', lambda q: plain(q['c'][0]).startswith('cool') and all(any(w in plain(c) for w in REAL['more ideal']) for c in q['c'][1:]),
    'low T (toward condensation) -> less ideal; heating, lower P, expansion -> more ideal')
chk('very high pressure take up more volume', lambda q: 'own volume' in plain(q['c'][0]), 'high P: particle volume no longer negligible')
def _alt(q):
    el = []
    for c in q['c']:
        m = re.search(r'([\d,]+) ft( below)?', txt(c)); v = D(m.group(1).replace(',', '')); el.append(-v if m.group(2) else v)
    return el[0] == max(el)
chk('has the lowest average air pressure', _alt, 'lowest pressure = highest elevation')
chk('pressure in mmHg and the volume in liters', lambda q: '62.36' in q['c'][0] and 'torr' in q['c'][0], 'mmHg = torr -> R = 62.36')
chk('Which conversions are needed first', lambda q: all(u in plain(q['c'][0]) for u in ('ml to l', 'mmhg to atm', '°c to k')), 'R = 0.082058 needs L, atm, K')
chk('1.00 mol of gas at 37 °C', lambda q: R * D('310.15') > VM and 'too small' in plain(q['c'][0]), 'true molar volume at 37 °C %s L > 22.4 L' % fmt(R * D('310.15'), 3))
chk('leaving the pressure in mmHg', lambda q: plain(q['c'][0]) == 'it is 760 times too large.', 'n ∝ P; mmHg number = 760 x atm number')
chk('Helium is pumped into a rigid tank', lambda q: plain(q['c'][0]).startswith('it stays the same'), "Dalton: O2's partial pressure set by its own n, V, T")
chk('three times as many moles', lambda q: 'three times that of' in plain(q['c'][0]) and plain(q['c'][0]).index('n2') < plain(q['c'][0]).index('o2'), 'P_i ∝ n_i: N2 three times O2')
chk('all substances as gases', lambda q: plain(q['c'][0]).startswith('2 l of h2 react with 1 l of o2 to make 2 l'), 'coefficients 2 : 1 : 2 as volumes')
chk('4.0 L of H2 makes 4.0 L of water', lambda q: any(ph == 'l' and f == 'H2O' for co, f, ph in eqs_in(q['q'])[0][1][1]) and 'liquid' in plain(q['c'][0]), 'water is (l): volume ratios do not apply')

# ---------- course rule: trailing zeros in calculation stems ----------
print('Trailing-zero rule in calculation stems; every k=1 item recomputed')
for q in ALL:
    if q['k'] == 1:
        s = re.sub(r'<sub>\d+</sub>', '', q['q']); s = txt(s)
        for m in re.finditer(r'(?<![\d.^,])(\d*[1-9]\d*0)(?![\d.^,])', s):
            err.append(q['id'] + ' calculation stem has ambiguous trailing-zero value %r' % m.group(1))
        if q['id'] not in checked: err.append(q['id'] + ' calculation item not recomputed')
for q in ALL:
    if q['id'] not in checked: hand.add(q['id'])

# ---------- draft overlap ----------
print('Draft overlap: no stem reuses a worked example or exercise from drafts/ch10')
GIV = r'(-?\d+\.\d+|\d+\.|\d+)(?: x 10\^(-?\d+))? ?(g|mol|°C|K|L|mL|atm|mmHg|torr|kPa|psi|%)(?![A-Za-z/])'
CONST = {'760', '760.', '273.15', '0.082058', '62.36', '22.4', '101.325', '14.7', '1', '1.00', '273', '0', '17.5', '23.8',
         '31.8', '47.1', '8.3144', '2', '3', '4', '37', '25', '20', '30', '1.0', '20.95', '78.08', '0.93'}
def givens_in(t): return {(a + ('e' + b if b else ''), u) for a, b, u in re.findall(GIV, t) if a not in CONST}
BANNED = {('752', 'mmHg'), ('2.00e3', 'psi'), ('1.25', 'atm'), ('98.5', 'kPa'), ('118', 'mmHg'), ('255', 'mL'), ('2.35', 'atm'),
          ('4.70', 'L'), ('136', 'atm'), ('2.50', 'L'), ('1.50', 'atm'), ('1.80', 'L'), ('0.0750', 'mol'), ('0.120', 'mol'),
          ('5.00', 'L'), ('375', 'mmHg'), ('10.0', 'mL'), ('25.0', 'mL'), ('2.15', 'atm'), ('3.25', 'L'), ('5.85', 'L'),
          ('12.5', 'g'), ('0.846', 'g'), ('0.355', 'L'), ('2.25', 'mol'), ('4.40', 'g'), ('65.0', 'g'), ('10.0', 'g'),
          ('4.50', 'L'), ('0.500', 'g'), ('25.0', 'g'), ('30.0', 'g'), ('6.00', 'L'), ('20.9', '%'), ('0.720', 'mol'),
          ('0.280', 'mol'), ('0.0405', 'g'), ('42.1', 'mL'), ('755', 'mmHg'), ('0.580', 'atm'), ('0.0270', 'atm'),
          ('1.50', 'mol'), ('0.500', 'mol'), ('3.00', 'atm'), ('748', 'mmHg')}
blocks = []
for p_ in sorted(glob.glob(os.path.join(ROOT, 'drafts', 'ch10', '*.html'))):
    h = open(p_, encoding='utf-8').read()
    for b in re.split(r'(?=Example \\\(\\PageIndex|Exercise \\\(\\PageIndex|<h2|Problem 10\.\d+\b)', h):
        t = re.sub(r'\\\(|\\\)|\\dfrac|\\text|\\times|\\ |\\qquad|\\left|\\right|\\cdot|\\tfrac', ' ', b)
        t = re.sub(r'\{\}\^\\circ\s*', '°', t).replace('\\circ', '°').replace('10^{3}', '10^3')
        t = txt(re.sub(r'[{}]', ' ', t)); t = re.sub(r'\s+', ' ', t)
        m = re.search(r'Problem (10\.\d+)', t)
        blocks.append((os.path.basename(p_) + (' Problem ' + m.group(1) if m else ''), givens_in(t), t.split(' Answer')[0]))
W = lambda s_: set(w for w in re.findall(r'[a-z0-9.]+', s_.lower()) if len(w) > 2)
nover = 0; notes = []
for q in ALL:
    qt = txt(q['q']); qg = givens_in(qt); qw = W(qt)
    for g_ in qg & BANNED:
        nover += 1; err.append('%s uses the draft worked-example given %s %s' % (q['id'], *g_))
    for nm, gs, bt in blocks:
        if len(qg & gs) >= 2:
            nover += 1; err.append('%s shares givens %s with %s' % (q['id'], sorted(qg & gs), nm))
        if 'Problem' in nm:
            bw = W(bt); j = len(qw & bw) / max(1, len(qw | bw))
            if j > 0.45: nover += 1; err.append('%s stem is %.2f similar to %s' % (q['id'], j, nm))
            elif j > 0.3: notes.append('%s stem %.2f similar to %s (checked by hand)' % (q['id'], j, nm))
print('    %d draft blocks compared (%s); %d overlaps' % (len(blocks), ', '.join(sorted({b[0].split(' ')[0] for b in blocks})), nover))
for n_ in notes: print('    NOTE', n_)

# ---------- Mateo, coverage, counts, duplicates ----------
mateo = [q['id'] for q in ALL if 'Mateo' in q['q'] + ' '.join(q['y']) + q['w']]
if len(mateo) > 2: err.append('Mateo appears in %d items (max 2): %s' % (len(mateo), mateo))
print('Mateo items:', mateo)
print('Items with a machine check: %d of %d' % (len(checked), len(ALL)))
print('  conceptual (key read by hand; quoted values still checked):', ' '.join(sorted(hand)))
for nm, B in (('Try It', TRY), ('ADAPT', HW)):
    print(nm, len(B), dict(collections.Counter(q['t'] for q in B)), 'with figures:', sum(1 for q in B if q.get('f')),
          'd:', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1:', sum(q['k'] for q in B))
normq = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip().lower()
for nm, B in (('Try It', TRY), ('ADAPT', HW)):
    c_ = collections.Counter(normq(q['q']) for q in B)
    d_ = [k for k, v in c_.items() if v > 1]
    if d_: err.append('%s repeats a stem: %s' % (nm, d_))
dup = set(normq(q['q']) for q in TRY) & set(normq(q['q']) for q in HW)
if dup: err.append('same question in both banks: %s' % dup)
print('ERRORS:', err if err else 'none')
