#!/usr/bin/env python3
"""Checker for the Chapter 11 banks (how solutions form, temperature/pressure and solubility, concentration,
molarity and dilution, solution stoichiometry and titration, molality and colligative properties).
Structural checks as in tools/check_bank_ch10.py (ch11 topic ids; ADAPT = 42 items, text only, y[0] begins
"Correct: "; tables at most 3 columns; figures only of fbx types table/plot), plus, written independently of the
generators:
  - every calculation item (k=1): the key and each numeric distractor's intended error recomputed with Decimal from
    the givens as written in the stem (or its table), TWO ways: (a) round once at the end and (b) strict: every
    intermediate (moles, liters of solution from a density, molality, mol after a mole ratio, the total volume in a
    dilution, the mass of KBr held by part of 100 g of water, delta T) rounded to its own significant figures, and
    every sum or difference (solution mass, buret volume, water added, freezing/boiling point) by the decimal-place
    rule, then used; the item is an error unless both agree, so every key is unambiguous;
  - sig figs by the multiplication rule from the givens (100 g in a percent, 1000 mL/L, 10^6, 10^9, i, mole ratios
    exact; Kf 1.86 and Kb 0.512 counted), sums and differences by the decimal-place rule;
  - every equation anywhere is parsed back out of the HTML and must balance; stoichiometry mole ratios are read from
    the stem's own equation;
  - every quoted molar mass is the checker's own (yellow-sheet atomic masses, addition rule);
  - quoted constants and conventions: Kf = 1.86, Kb = 0.512, serum 275-295 mOsm/kg, 1 ppm/ppb/ppt equivalences,
    1 M = 1000 mM, every "gives n ions (i = n)" against an i table (complete dissociation);
  - conceptual items: key tables (i values, polarity class for like dissolves like, solvent = larger amount,
    saturation from a given solubility, gas/solid solubility vs temperature and pressure, osmosis direction and
    tonicity against serum, titration endpoint, what dilution keeps fixed) recheck the keys; the rest are listed as
    read by hand;
  - course rule: no whole number ending in 0 without a decimal point in a calculation stem;
  - exactly one correct choice (recomputed values all different; four different choices);
  - no stem reuses a draft worked example or exercise (two shared givens with a draft block, or one of the listed
    worked-example givens); no stem in both banks; Mateo in at most 2 items.
usage: python3 tools/check_bank_ch11.py bank/ch11.json bank/ch11_adapt.json"""
import json, sys, re, os, collections, glob
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 50; getcontext().rounding = ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AM = json.load(open(os.path.join(ROOT, 'tools', 'yellow_sheet_masses.json')))['masses']
TOP = {'ch11-dissolve', 'ch11-solubility', 'ch11-conc', 'ch11-dilution', 'ch11-titration', 'ch11-colligative'}
err = []

# ---------- text ----------
def txt(x):
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<[^>]+>', '', x)
    for a, b in (('&middot;', '·'), ('&minus;', '-'), ('−', '-'), ('&times;', 'x'), ('&nbsp;', ' '), ('&divide;', '/'),
                 ('&rarr;', '->'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&deg;', '°'), ('&ndash;', '–'), ('&lt;', '<'),
                 ('&gt;', '>'), ('&asymp;', '≈'), ('&mu;', 'µ'), ('&delta;', 'δ'), ('&Delta;', 'Δ'), ('&amp;', '&')):
        x = x.replace(a, b)
    return x
def plain(x): return re.sub(r'\s+', ' ', txt(x)).strip().lower()

# ---------- structural checks ----------
OUT_OF_SCOPE = r"Raoult|mole fraction of solvent|normality|Henderson|osmotic pressure equation|all of the above|none of the above"
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
structural(TRY, 'c11-%03d', 'TRY', True)
structural(HW, 'c11-h%02d', 'HW', False)
if len(HW) != 42: err.append('ADAPT has %d items, not 42' % len(HW))
if sum(1 for q in TRY if q.get('f')) > 4: err.append('more than 4 figures')
fbx = open(os.path.join(ROOT, 'js', 'fbx.js'), encoding='utf-8').read()
for t_ in {f['type'] for q in TRY for f in q.get('f', [])}:
    if not re.search(r'[{,]%s:' % t_, fbx): err.append('figure type %s not supported by js/fbx.js' % t_)
wid = open(os.path.join(ROOT, 'js', 'widget.js'), encoding='utf-8').read()
for t_ in TOP:
    if "'%s'" % t_ not in wid: err.append('topic %s missing from js/widget.js TOPICS' % t_)
WANT_T = {'ch11-dissolve': 10, 'ch11-solubility': 10, 'ch11-conc': 14, 'ch11-dilution': 14, 'ch11-titration': 12, 'ch11-colligative': 12}
WANT_H = {'ch11-dissolve': 6, 'ch11-solubility': 6, 'ch11-conc': 8, 'ch11-dilution': 8, 'ch11-titration': 7, 'ch11-colligative': 7}
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
def rq(v, d):
    s = format(D(v).quantize(D(10) ** -d), 'f')
    return s + '.' if d == 0 and s.endswith('0') else s
def U(v, n, u=''): return (fmt(v, n) + ' ' + u).strip()
def Pc(v, n): return fmt(v, n) + '%'
def N(*a): return min(x if isinstance(x, int) else sf(x) for x in a)
def ADD(*s):
    """sum of strings as written ('-x' subtracts), decimal-place rule."""
    return rq(sum(D(x.rstrip('.')) for x in s), min(dec(x.lstrip('-')) for x in s))
def R(x, n, m):
    """intermediate: carried exactly (m=0) or rounded to its own n significant figures first (m=1)."""
    return D(x) if m == 0 else D(fmt(x, n).replace(' x 10^', 'e'))
g = D
def Lt(mL): return D(mL) / 1000

# ---------- constants and key tables (Chapter 11 text) ----------
KF, KB = D('1.86'), D('0.512')
I = {'NaCl': 2, 'KBr': 2, 'KNO3': 2, 'KCl': 2, 'KI': 2, 'NaNO3': 2, 'NH4Cl': 2, 'CaCl2': 3, 'MgCl2': 3, 'Na2SO4': 3,
     'AlCl3': 4, 'C6H12O6': 1, 'C12H22O11': 1, 'C2H5OH': 1, 'CH4N2O': 1, 'C2H6O2': 1, 'C3H8O3': 1,
     'CH3OH': 1, 'C3H6O': 1, 'glucose': 1, 'sucrose': 1, 'urea': 1, 'ethanol': 1, 'ethylene glycol': 1, 'propylene glycol': 1,
     'glycerol': 1, 'methanol': 1, 'acetone': 1}
POL = {'glycerol': 'polar', 'C3H8O3': 'polar', 'hexane': 'nonpolar', 'C6H14': 'nonpolar', 'CCl4': 'nonpolar', 'Br2': 'nonpolar',
       'water': 'polar', 'ethanol': 'polar', 'C2H5OH': 'polar', 'acetone': 'polar', 'C3H6O': 'polar', 'octane': 'nonpolar',
       'C8H18': 'nonpolar', 'decane': 'nonpolar', 'C10H22': 'nonpolar', 'NaCl': 'ionic', 'sodium chloride': 'ionic',
       'sucrose': 'polar', 'C12H22O11': 'polar', 'KNO3': 'ionic', 'potassium nitrate': 'ionic', 'urea': 'polar', 'CH4N2O': 'polar',
       'pentane': 'nonpolar', 'C5H12': 'nonpolar', 'CS2': 'nonpolar', 'N2': 'nonpolar'}
NH4CL = {'0.0': '29.4', '20.0': '37.2', '40.0': '45.8', '60.0': '55.3', '80.0': '65.6'}   # g per 100 g water
SERUM = (275, 295)

# ---------- formulas, molar masses, equations ----------
def atoms(f):
    stack = [collections.Counter()]; i = 0
    while i < len(f):
        if f[i] == '(':
            stack.append(collections.Counter()); i += 1
        elif f[i] == ')':
            j = i + 1
            while j < len(f) and f[j].isdigit(): j += 1
            gg = stack.pop()
            for k, v in gg.items(): stack[-1][k] += v * int(f[i + 1:j] or 1)
            i = j
        else:
            m = re.match(r'([A-Z][a-z]?)(\d*)', f[i:])
            if not m or m.group(1) not in AM: raise ValueError(f)
            stack[-1][m.group(1)] += int(m.group(2) or 1); i += m.end()
    return stack[0]
def MM(f):
    c = atoms(f); q = min(len(AM[e].partition('.')[2]) for e in c)
    return sum((D(AM[e]) * n for e, n in c.items()), D(0)).quantize(D(10) ** -q)
for f, want in (('NaCl', '58.44'), ('KCl', '74.55'), ('C6H12O6', '180.156'), ('H2C2O4', '90.034'), ('C6H8O6', '176.124'),
                ('AgCl', '143.32'), ('H2O', '18.015')):
    if str(MM(f)) != want: err.append('checker molar mass %s = %s, text says %s' % (f, MM(f), want))
NAMES = {'glucose': 'C6H12O6', 'urea': 'CH4N2O', 'glycerol': 'C3H8O3', 'aspirin': 'C9H8O4', 'khp': 'KHC8H4O4', 'water': 'H2O'}
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
            if not any(v == hv for _, hv in hits) and q['k'] == 0: err.append('%s quotes %s g/mol with no formula' % (q['id'], v))
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
    L_, R_ = s.split(' -> ')
    return [sp(t) for t in L_.split(' + ')], [sp(t) for t in R_.split(' + ')]
def eqs_in(h):
    out = []
    t = txt(h)
    for m in EQRE.finditer(t):
        if '^' in m.group() or t[m.end():m.end() + 1] == '^': continue      # ion dissociations (charges) are not atom-balance equations
        try: out.append((m.group(), parse_eq(m.group())))
        except ValueError: pass
    return out
def balanced(e):
    def side(S_):
        c = collections.Counter()
        for co, f, ph in S_:
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

# ---------- quoted constants and conventions ----------
print('Quoted constants: Kf, Kb, serum range, ppm/ppb/ppt, mM, i values')
EQV = {('1 ppm', '1 mg/L'), ('1 ppb', '1 µg/L'), ('1 ppt', '1 ng/L')}
ni = 0
for q in ALL:
    s = txt(' '.join([q['q'], q['w'], q['h']] + q['c'] + q['y']))
    for v in re.findall(r'(?<!/ )Kf = (\d+\.\d+)', s):
        if v != '1.86': err.append('%s quotes Kf = %s' % (q['id'], v))
    for v in re.findall(r'(?<!/ )Kb = (\d+\.\d+)', s):
        if v != '0.512': err.append('%s quotes Kb = %s' % (q['id'], v))
    for a, b in re.findall(r'(\d+)–(\d+) mOsm/kg', s):
        if (int(a), int(b)) != SERUM: err.append('%s quotes serum %s–%s mOsm/kg' % (q['id'], a, b))
    for a, b in re.findall(r'(1 (?:ppm|ppb|ppt)) ≈ (1 [µnm]?g/L)', s) + [(y_, x_) for x_, y_ in re.findall(r'(1 [µnm]?g/L) ≈ (1 (?:ppm|ppb|ppt))', s)]:
        if (a, b) not in EQV: err.append('%s quotes %s ≈ %s' % (q['id'], a, b))
    for a in re.findall(r'1 M = (\d+) mM', s):
        if a != '1000': err.append('%s quotes 1 M = %s mM' % (q['id'], a))
    for f, n_, n2 in re.findall(r'([A-Z][A-Za-z0-9()]*) gives (\d) (?:ions|particles)(?: \(i = (\d)\))?', s):
        ni += 1
        if I.get(f) != int(n_) or (n2 and int(n2) != I.get(f)): err.append('%s says %s gives %s ions (i table %s)' % (q['id'], f, n_, I.get(f)))
    for n_, f in re.findall(r'i = (\d) for ([A-Z][A-Za-z0-9()]*)', s):
        ni += 1
        if I.get(f) != int(n_): err.append('%s says i = %s for %s' % (q['id'], n_, f))
    for f, n_ in re.findall(r'([A-Z][A-Za-z0-9()]*) ->[^:]*: (?:three|two|four) particles \(i = (\d)\)', s):
        ni += 1
        if I.get(f) != int(n_): err.append('%s says %s i = %s' % (q['id'], f, n_))
print('    %d i values quoted, all checked' % ni)

# ---------- calculation items ----------
def by(sub):
    m = [q for q in ALL if sub in txt(q['q'])]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
checked, hand = set(), set()
CUR = {}
def CO(f):
    for side in CUR['eq']:
        for co, ff, ph in side:
            if ff == f: return D(co)
    raise KeyError(f)
def RT(a, b): return CO(b) / CO(a)          # mol b per mol a from the stem's equation
CALC = []
def calc(sub, givens, specs): CALC.append((sub, givens, specs))
def FP(dT, m):
    """freezing point: dT carried (m=0) or rounded to 3 s.f. (m=1); 0.00 - dT to the decimal place of the rounded dT (max 2)."""
    d = min(2, dec(fmt(dT, 3))); x = dT if m == 0 else D(fmt(dT, 3))
    return rq(D('0.00') - x, d) + ' °C'
def BP(dT, m, sign=1):
    d = min(2, dec(fmt(dT, 3))); x = dT if m == 0 else D(fmt(dT, 3))
    return rq(D('100.00') + sign * x, d) + ' °C'

# ---- ch11-solubility ----
def _nh4(q):
    rows = {r[0]: r[1] for r in q['f'][0]['rows']}
    ok(rows == NH4CL, '%s NH4Cl solubility table = reference values %s' % (q['id'], rows))
calc('made with 100. g of water at 60.0 °C is cooled to 20.0 °C', ['60.0', '20.0', '100.'],
     {0: lambda m: ADD(NH4CL['60.0'], '-' + NH4CL['20.0']) + ' g', 1: lambda m: NH4CL['60.0'] + ' g', 2: lambda m: NH4CL['20.0'] + ' g', 3: lambda m: ADD(NH4CL['60.0'], NH4CL['20.0']) + ' g'})
calc('pressure of 3.45 atm', ['1.69', '1.00', '3.45'], {0: lambda m: U(g('1.69') * g('3.45') / g('1.00'), N('1.69', '1.00', '3.45'), 'g/L'), 1: lambda m: U(g('1.69') * g('1.00') / g('3.45'), 3, 'g/L'), 2: lambda m: U(g('3.45') / g('1.69'), 3, 'g/L'), 3: lambda m: '1.69 g/L'})
calc('raised to 2.45 atm', ['4.35', '0.132', '2.45'], {0: lambda m: U(g('4.35') * g('2.45') / g('0.132'), N('4.35', '0.132', '2.45'), 'mg/L'), 1: lambda m: U(g('4.35') * g('0.132') / g('2.45'), 3, 'mg/L'), 2: lambda m: U(g('4.35') * g('2.45'), 3, 'mg/L'), 3: lambda m: '4.35 mg/L'})
_kb = lambda S_, m: R(g(S_) * g('75.0') / 100, N(S_, '75.0'), m)
calc('made with 75.0 g of water at 80.0 °C', ['94.9', '65.3', '75.0'],
     {0: lambda m: (U((g('94.9') - g('65.3')) * g('75.0') / 100, 3, 'g') if m == 0 else ADD(str(_kb('94.9', 1)), '-' + str(_kb('65.3', 1))) + ' g'),
      1: lambda m: ADD('94.9', '-65.3') + ' g', 2: lambda m: U(_kb('94.9', m), 3, 'g'), 3: lambda m: U(_kb('65.3', m), 3, 'g')})
calc('only 0.155 atm', ['8.26', '0.209', '0.155'], {0: lambda m: U(g('8.26') * g('0.155') / g('0.209'), 3, 'mg/L'), 1: lambda m: U(g('8.26') * g('0.209') / g('0.155'), 3, 'mg/L'), 2: lambda m: U(g('8.26') * g('0.155'), 3, 'mg/L'), 3: lambda m: '8.26 mg/L'})
calc('solubility of 6.85 g/L', ['1.68', '0.850', '6.85'], {0: lambda m: U(g('0.850') * g('6.85') / g('1.68'), 3, 'atm'), 1: lambda m: U(g('1.68') * g('0.850') / g('6.85'), 3, 'atm'), 2: lambda m: U(g('6.85') / g('1.68'), 3, 'atm'), 3: lambda m: U(g('6.85') * g('1.68') / g('0.850'), 3, 'atm')})
calc('chilled to 0 °C', ['65.6', '29.4', '80.0'], {0: lambda m: ADD('65.6', '-29.4') + ' g', 1: lambda m: '65.6 g', 2: lambda m: '29.4 g', 3: lambda m: ADD('65.6', '29.4') + ' g'})

# ---- ch11-conc ----
def _mp(gs, ws):
    tot = ADD(gs, ws); n = N(gs, tot)
    return {0: lambda m: Pc(g(gs) / (g(gs) + g(ws) if m == 0 else g(tot)) * 100, n), 1: lambda m: Pc(g(gs) / g(ws) * 100, n),
            2: lambda m: Pc(g(ws) / (g(gs) + g(ws) if m == 0 else g(tot)) * 100, n), 3: lambda m: Pc(g(gs) / (g(gs) + g(ws) if m == 0 else g(tot)), n)}
calc('dissolves 4.50 g of NaCl in 85.5 g of water', ['4.50', '85.5'], _mp('4.50', '85.5'))
calc('dissolving 6.40 g of potassium iodide', ['6.40', '145.0'], _mp('6.40', '145.0'))
calc('16.8 g of sodium bicarbonate', ['16.8', '200.0'], {0: lambda m: Pc(g('16.8') / g('200.0') * 100, 3), 1: lambda m: Pc(g('16.8') / g('200.0'), 3), 2: lambda m: Pc(g('200.0') / g('16.8') * 100, 3), 3: lambda m: Pc(g('16.8') / Lt('200.0') * 100, 3)})
calc('250. mL bag of 3.00% (m/v) NaCl', ['250.', '3.00'], {0: lambda m: U(g(250) * g('3.00') / 100, N('250.', '3.00'), 'g'), 1: lambda m: U(g(250) * g('3.00'), 3, 'g'), 2: lambda m: U(g(250) * g('3.00') / 1000, 3, 'g'), 3: lambda m: U(g(250) / g('3.00'), 3, 'g')})
calc('mixes 35.0 mL of ethanol', ['35.0', '50.0'], {0: lambda m: Pc(g('35.0') / g('50.0') * 100, 3), 1: lambda m: Pc(g('50.0') / g('35.0') * 100, 3), 2: lambda m: Pc(g('35.0') / g('50.0'), 3), 3: lambda m: Pc(g('35.0') / (g('35.0') + g('50.0')) * 100, 3)})
calc('0.845 mg of fluoride in 1.25 L', ['0.845', '1.25'], {0: lambda m: U(g('0.845') / g('1.25'), 3, 'ppm'), 1: lambda m: U(g('0.845') / g('1.25') * 1000, 3, 'ppm'), 2: lambda m: U(g('1.25') / g('0.845'), 3, 'ppm'), 3: lambda m: '0.845 ppm'})
calc('0.00865 mg of arsenic per liter', ['0.00865'], {0: lambda m: U(g('0.00865') * 1000, 3, 'ppb'), 1: lambda m: U(g('0.00865') * 10 ** 6, 3, 'ppb'), 2: lambda m: U(g('0.00865') / 1000, 3, 'ppb'), 3: lambda m: '0.00865 ppb'})
calc('0.00000715 mg/L of 1,2,3-trichloropropane', ['0.00000715'], {0: lambda m: U(g('0.00000715') * 10 ** 6, 3, 'ppt'), 1: lambda m: U(g('0.00000715') * 1000, 3, 'ppt'), 2: lambda m: U(g('0.00000715'), 3, 'ppt'), 3: lambda m: U(g('0.00000715') * 10 ** 9, 3, 'ppt')})
calc('contains 0.0410 mg of mercury', ['125.0', '0.0410'], {0: lambda m: U(g('0.0410') / (g('125.0') / 1000), 3, 'ppm'), 1: lambda m: U(g('0.0410') / g('125.0') * 10 ** 6, 3, 'ppm'), 2: lambda m: U(g('0.0410') / g('125.0'), 3, 'ppm'), 3: lambda m: U(g('125.0') / g('0.0410'), 3, 'ppm')})
calc('98.5 mg of nitrate', ['2.50', '98.5'], {0: lambda m: U(g('98.5') / g('2.50'), 3, 'ppm'), 1: lambda m: U(g('98.5') * g('2.50'), 3, 'ppm'), 2: lambda m: U(g('2.50') / g('98.5'), 3, 'ppm'), 3: lambda m: U(g('98.5') / g('2.50') * 1000, 3, 'ppm')})
calc('contains 0.0185 mg of lead', ['1.50', '0.0185'], {0: lambda m: U(g('0.0185') / g('1.50') * 1000, 3, 'ppb'), 1: lambda m: U(g('0.0185') / g('1.50'), 3, 'ppb'), 2: lambda m: U(g('0.0185') * 1000, 3, 'ppb'), 3: lambda m: U(g('0.0185') / g('1.50') * 10 ** 6, 3, 'ppb')})
def _molar(gs, f, mL):
    n = N(gs, mL)
    mol = lambda m: R(g(gs) / MM(f), n, m)
    return {0: lambda m: U(mol(m) / Lt(mL), n, 'M'), 1: lambda m: U(mol(m) / g(mL), n, 'M'), 2: lambda m: U(g(gs) / Lt(mL), n, 'M'), 3: lambda m: U(Lt(mL) / mol(m), n, 'M')}
calc('contains 2.45 g of KBr', ['2.45', '75.0'], _molar('2.45', 'KBr', '75.0'))
_g = _molar('9.70', 'C6H12O6', '200.0'); _g[3] = lambda m: U(R(g('9.70') / MM('C6H12O6'), 3, m), 3, 'M')
calc('dissolves 9.70 g of glucose', ['9.70', '200.0'], _g)
calc('dissolving 4.75 g of MgCl2', ['4.75', '150.0'], _molar('4.75', 'MgCl2', '150.0'))
calc('dissolves 18.9 g of NaHCO3', ['18.9', '300.0'], _molar('18.9', 'NaHCO3', '300.0'))
def _pct_M(pc, d_, f):
    n = N(pc, d_)
    mol = lambda m: R(g(pc) / MM(f), n, m)
    vol = lambda m: R(100 / g(d_), n, m) / 1000
    return {0: lambda m: U(mol(m) / vol(m), n, 'M'), 1: lambda m: U(mol(m) / g('0.100'), n, 'M'), 2: lambda m: U(mol(m) / R(100 * g(d_) / 1000, n, m), n, 'M'), 3: lambda m: U(g(pc) / vol(m), n, 'M')}
calc('6.00% (m/m) sodium hypochlorite', ['6.00', '1.08'], _pct_M('6.00', '1.08', 'NaOCl'))
calc('37.2% (m/m) HCl', ['37.2', '1.19'], _pct_M('37.2', '1.19', 'HCl'))
calc('7.00% (m/m) NaCl solution', ['7.00', '1.05'], _pct_M('7.00', '1.05', 'NaCl'))
calc('fluoride mouth rinse is 0.050%', ['10.0', '0.050'], {0: lambda m: U(g('10.0') * g('0.050') / 100, N('10.0', '0.050'), 'g'), 1: lambda m: U(g('10.0') * g('0.050'), 2, 'g'), 2: lambda m: U(g('10.0') * g('0.050') / 10 ** 4, 2, 'g'), 3: lambda m: U(g('10.0') / g('0.050'), 2, 'g')})

# ---- ch11-dilution ----
def _mol(mL, M_):
    n = N(mL, M_)
    return {0: lambda m: U(Lt(mL) * g(M_), n, 'mol'), 1: lambda m: U(g(mL) * g(M_), n, 'mol'), 2: lambda m: U(Lt(mL) / g(M_), n, 'mol'), 3: lambda m: U(g(M_) / Lt(mL), n, 'mol')}
calc('in 36.5 mL of 0.225 M NaOH', ['36.5', '0.225'], _mol('36.5', '0.225'))
calc('in 42.5 mL of 0.0875 M KCl', ['42.5', '0.0875'], _mol('42.5', '0.0875'))
def _grams(mL, M_, f):
    n = N(mL, M_); mol = lambda m: R(Lt(mL) * g(M_), n, m)
    return {0: lambda m: U(mol(m) * MM(f), n, 'g'), 1: lambda m: U(g(mL) * g(M_) * MM(f), n, 'g'), 2: lambda m: U(mol(m), n, 'g'), 3: lambda m: U(mol(m) / MM(f), n, 'g')}
calc('prepare 200.0 mL of 0.325 M CaCl2', ['200.0', '0.325'], _grams('200.0', '0.325', 'CaCl2'))
calc('prepare 100.0 mL of 0.450 M Na2SO4', ['100.0', '0.450'], _grams('100.0', '0.450', 'Na2SO4'))
calc('contains 2.85 x 10^-3 mol of HCl', ['0.125', '2.85'], {0: lambda m: U(g('2.85e-3') / g('0.125') * 1000, 3, 'mL'), 1: lambda m: U(g('2.85e-3') / g('0.125'), 3, 'mL'), 2: lambda m: U(g('2.85e-3') * g('0.125') * 1000, 3, 'mL'), 3: lambda m: U(g('0.125') / g('2.85e-3'), 3, 'mL')})
_v2 = ADD('12.0', '36.0')
calc('mixed with 36.0 mL of water', ['12.0', '2.40', '36.0'], {0: lambda m: U(g('2.40') * g('12.0') / g(_v2), N('2.40', '12.0', _v2), 'M'), 1: lambda m: U(g('2.40') * g('12.0') / g('36.0'), 3, 'M'), 2: lambda m: U(g('2.40') * g(_v2) / g('12.0'), 3, 'M'), 3: lambda m: U(g('2.40') * g('12.0'), 3, 'M')})
def _v1(M1, V2, mM2):
    n = N(M1, V2, mM2); M2 = g(mM2) / 1000
    return {0: lambda m: U(M2 * g(V2) / g(M1), n, 'mL'), 1: lambda m: U(g(mM2) * g(V2) / g(M1), n, 'mL'), 2: lambda m: U(g(M1) * g(V2) / M2, n, 'mL'), 3: lambda m: U(M2 * g(M1) / g(V2), n, 'mL')}
calc('of 1.25 M stock are needed to prepare 50.00 mL of 35.0 mM', ['1.25', '50.00', '35.0'], _v1('1.25', '50.00', '35.0'))
calc('of 0.425 M KCl stock are needed to make 200.0 mL of 12.5 mM', ['0.425', '200.0', '12.5'], _v1('0.425', '200.0', '12.5'))
_m2 = lambda m: R(g('0.180') * g('2.00') / g('50.0'), 3, m)
calc('2.00 mL sample of 0.180 M glucose', ['2.00', '0.180', '50.0'], {0: lambda m: U(_m2(m) * 1000, 3, 'mM'), 1: lambda m: U(_m2(m), 3, 'mM'), 2: lambda m: U(g('0.180') * g('50.0') / g('2.00') * 1000, 3, 'mM'), 3: lambda m: U(_m2(m) / 1000, 3, 'mM')})
def _water(V1, M1, M2):
    n = N(V1, M1, M2); V2s = fmt(g(M1) * g(V1) / g(M2), n)
    return {0: lambda m: ADD(V2s, '-' + V1) + ' mL', 1: lambda m: V2s + ' mL', 2: lambda m: U(g(M2) * g(V1) / g(M1), n, 'mL'), 3: lambda m: ADD(V2s, V1) + ' mL'}
calc('16.0 mL sample of 0.880 M KCl', ['16.0', '0.880', '0.275'], _water('16.0', '0.880', '0.275'))
calc('50.0 mL sample of 0.640 M glucose', ['50.0', '0.640', '0.160'], _water('50.0', '0.640', '0.160'))
_F = (g('0.50') + g('4.5')) / g('0.50'); _F9 = g('4.5') / g('0.50')      # two dilutions; V2 is the total volume
calc('4.2 x 10^6 bacteria per mL', ['4.2', '0.50', '4.5'], {0: lambda m: U(g('4.2e6') / _F ** 2, 2, 'bacteria/mL'), 1: lambda m: U(g('4.2e6') / _F9 ** 2, 2, 'bacteria/mL'), 2: lambda m: U(g('4.2e6') / _F, 2, 'bacteria/mL'), 3: lambda m: U(g('4.2e6') / (2 * _F), 2, 'bacteria/mL')})
_F5 = (g('1.0') + g('4.0')) / g('1.0'); _F4 = g('4.0') / g('1.0')
calc('adds 1.0 mL of 2.0 M stock', ['1.0', '2.0', '4.0'], {0: lambda m: U(g('2.0') / _F5 ** 2, 2, 'M'), 1: lambda m: U(g('2.0') / _F5, 2, 'M'), 2: lambda m: U(g('2.0') / (2 * _F5), 2, 'M'), 3: lambda m: U(g('2.0') / _F4 ** 2, 2, 'M')})
_ip = g('45.0') * g('400.0') / g('70.0')
calc('of 70.0% (v/v) isopropyl alcohol', ['70.0', '400.0', '45.0'], {0: lambda m: U(_ip, 3, 'mL'), 1: lambda m: U(g('70.0') * g('400.0') / g('45.0'), 3, 'mL'), 2: lambda m: (ADD('400.0', '-' + fmt(_ip, 3)) if m else fmt(g('400.0') - _ip, 3)) + ' mL', 3: lambda m: U(g('45.0') * g('70.0') / g('400.0'), 3, 'mL')})
_na = lambda m: R(g('2.40') / MM('NaCl'), 3, m)
calc('contains 2.40 g of NaCl', ['0.355', '2.40'], {0: lambda m: U(_na(m) / g('0.355') * 1000, 3, 'mL'), 1: lambda m: U(g('2.40') / g('0.355') * 1000, 3, 'mL'), 2: lambda m: U(_na(m) * g('0.355') * 1000, 3, 'mL'), 3: lambda m: U(_na(m) / g('0.355'), 3, 'mL')})
calc('glucose concentration of 5.6 mM', ['5.00', '5.6'], {0: lambda m: U(g('5.6') / 1000 * Lt('5.00'), 2, 'mol'), 1: lambda m: U(g('5.6') * Lt('5.00'), 2, 'mol'), 2: lambda m: U(g('5.6') * g('5.00'), 2, 'mol'), 3: lambda m: U(g('5.6') / 1000 * Lt('5.00') / 1000, 2, 'mol')})
calc('pipets 4.00 mL of a stock', ['4.00', '50.0', '0.0328'], {0: lambda m: U(g('0.0328') * g('50.0') / g('4.00'), 3, 'M'), 1: lambda m: U(g('0.0328') * g('4.00') / g('50.0'), 3, 'M'), 2: lambda m: U(g('0.0328') * g('50.0'), 3, 'M'), 3: lambda m: '0.0328 M'})
calc('8.00 mL portion of 1.35 M NaCl', ['8.00', '1.35', '50.0'], {0: lambda m: U(g('1.35') * g('8.00') / g('50.0'), 3, 'M'), 1: lambda m: U(g('1.35') * g('50.0') / g('8.00'), 3, 'M'), 2: lambda m: U(g('1.35') * g('8.00'), 3, 'M'), 3: lambda m: U(g('1.35') * g('8.00') / (g('50.0') + g('8.00')), 3, 'M')})
calc('What volume of 25.0 mM KCl contains 1.50 x 10^-4 mol', ['25.0', '1.50'], {0: lambda m: U(g('1.50e-4') / (g('25.0') / 1000) * 1000, 3, 'mL'), 1: lambda m: U(g('1.50e-4') / (g('25.0') / 1000), 3, 'mL'), 2: lambda m: U(g('1.50e-4') * g('25.0') / 1000 * 1000, 3, 'mL'), 3: lambda m: U(g('25.0') / 1000 / g('1.50e-4') * 1000, 3, 'mL')})

# ---- ch11-titration (mole ratios from the stem's equation) ----
def _pb(m): return R(Lt('21.5') * g('0.135'), 3, m)
calc('reacts completely with 21.5 mL of 0.135 M', ['0.185', '21.5', '0.135'], {0: lambda m: U(R(_pb(m) * RT('Pb(NO3)2', 'KI'), 3, m) / g('0.185') * 1000, 3, 'mL'), 1: lambda m: U(_pb(m) / g('0.185') * 1000, 3, 'mL'),
     2: lambda m: U(_pb(m) / RT('Pb(NO3)2', 'KI') / g('0.185') * 1000, 3, 'mL'), 3: lambda m: U(R(_pb(m) * RT('Pb(NO3)2', 'KI'), 3, m) * g('0.185') * 1000, 3, 'mL')})
def _ba(m): return R(Lt('35.0') * g('0.0860'), 3, m) * RT('CaCl2', 'CaCO3')
calc('when 35.0 mL of 0.0860 M CaCl2', ['35.0', '0.0860'], {0: lambda m: U(_ba(m) * MM('CaCO3'), 3, 'g'), 1: lambda m: U(g('35.0') * g('0.0860') * MM('CaCO3'), 3, 'g'), 2: lambda m: U(_ba(m), 3, 'g'), 3: lambda m: U(_ba(m) / MM('CaCO3'), 3, 'g')})
TAB = {}
def _bur(q):
    rows = {r[0]: r[1] for r in q['f'][0]['rows']}
    ok(set(rows) == {'Initial', 'Final (endpoint)'} and D(rows['Final (endpoint)']) > D(rows['Initial']), '%s buret table has initial < final %s' % (q['id'], rows))
    TAB.update(rows)
def _hno3(m):
    vt = ADD(TAB['Final (endpoint)'], '-' + TAB['Initial'])
    return vt, R(Lt(vt) * g('0.1125'), 4, m) * RT('NaOH', 'HNO3')
calc('sample of HNO3 is titrated with 0.1125 M NaOH', ['15.00', '0.1125'], {0: lambda m: U(_hno3(m)[1] / Lt('15.00'), 4, 'M'), 1: lambda m: U(Lt(TAB['Final (endpoint)']) * g('0.1125') / Lt('15.00'), 4, 'M'),
     2: lambda m: U(Lt('15.00') * g('0.1125') / Lt(_hno3(m)[0]), 4, 'M'), 3: lambda m: U(_hno3(m)[1] / Lt(_hno3(m)[0]), 4, 'M')})
def _ox(gs, mL):
    ma = lambda m: R(g(gs) / MM('H2C2O4'), 4, m)
    return {0: lambda m: U(R(ma(m) * RT('H2C2O4', 'NaOH'), 4, m) / Lt(mL), 4, 'M'), 1: lambda m: U(ma(m) / Lt(mL), 4, 'M'), 2: lambda m: U(ma(m) / RT('H2C2O4', 'NaOH') / Lt(mL), 4, 'M'), 3: lambda m: U(g(gs) * RT('H2C2O4', 'NaOH') / Lt(mL), 4, 'M')}
calc('dissolves 0.1715 g of oxalic acid', ['0.1715', '27.33'], _ox('0.1715', '27.33'))
calc('A 0.1700 g sample of oxalic acid', ['0.1700', '25.85'], _ox('0.1700', '25.85'))
def _h2(m): return R(Lt('12.5') * g('0.0840'), 3, m)
calc('neutralizes 12.5 mL of 0.0840 M H2SO4', ['0.105', '12.5', '0.0840'], {0: lambda m: U(R(_h2(m) * RT('H2SO4', 'NaOH'), 3, m) / g('0.105') * 1000, 3, 'mL'), 1: lambda m: U(_h2(m) / g('0.105') * 1000, 3, 'mL'),
     2: lambda m: U(_h2(m) / RT('H2SO4', 'NaOH') / g('0.105') * 1000, 3, 'mL'), 3: lambda m: U(R(_h2(m) * RT('H2SO4', 'NaOH'), 3, m) / g('0.0840') * 1000, 3, 'mL')})
def _pct_solid(s_, M_, mL, f, base='NaOH'):
    mol = lambda m: R(Lt(mL) * g(M_), 4, m) * RT(base, f)
    gm = lambda m: R(mol(m) * MM(f), 4, m)
    return mol, gm
_as = _pct_solid('0.4250', '0.1185', '18.54', 'C9H8O4')
calc('crushed aspirin tablet', ['0.4250', '0.1185', '18.54'], {0: lambda m: Pc(_as[1](m) / g('0.4250') * 100, 4), 1: lambda m: Pc(_as[0](m) / g('0.4250') * 100, 4), 2: lambda m: U(_as[1](m), 4, 'g'), 3: lambda m: Pc(g('0.4250') / _as[1](m) * 100, 4)})
_kh = _pct_solid('0.8125', '0.1088', '32.18', 'KHC8H4O4')
calc('impure potassium hydrogen phthalate', ['0.8125', '0.1088', '32.18'], {0: lambda m: Pc(_kh[1](m) / g('0.8125') * 100, 4), 1: lambda m: U(_kh[1](m), 4, 'g'), 2: lambda m: Pc(_kh[0](m) / g('0.8125') * 100, 4), 3: lambda m: Pc(g('0.8125') / _kh[1](m) * 100, 4)})
calc('reads 0.85 mL before a titration', ['0.85', '17.40'], {0: lambda m: ADD('17.40', '-0.85') + ' mL', 1: lambda m: '17.40 mL', 2: lambda m: ADD('17.40', '0.85') + ' mL', 3: lambda m: '0.85 mL'})
def _cit(m):
    mb = R(Lt('9.85') * g('0.0950'), 3, m); return mb, R(mb * RT('NaOH', 'H3C6H5O7'), 3, m)
calc('lemon-lime soda needs 9.85 mL', ['35.0', '9.85', '0.0950'], {0: lambda m: U(_cit(m)[1] / Lt('35.0'), 3, 'M'), 1: lambda m: U(_cit(m)[0] / Lt('35.0'), 3, 'M'), 2: lambda m: U(_cit(m)[0] / RT('NaOH', 'H3C6H5O7') / Lt('35.0'), 3, 'M'), 3: lambda m: U(_cit(m)[1] / Lt('9.85'), 3, 'M')})
def _mg(m): return R(g('0.610') / MM('CaCO3'), 3, m)
calc('contains 0.610 g of calcium carbonate', ['0.610', '0.105'], {0: lambda m: U(R(_mg(m) * RT('CaCO3', 'HCl'), 3, m) / g('0.105') * 1000, 3, 'mL'), 1: lambda m: U(_mg(m) / g('0.105') * 1000, 3, 'mL'),
     2: lambda m: U(g('0.610') * RT('CaCO3', 'HCl') / g('0.105') * 1000, 3, 'mL'), 3: lambda m: U(_mg(m) / RT('CaCO3', 'HCl') / g('0.105') * 1000, 3, 'mL')})
def _hcl(m):
    vt = ADD('19.80', '-0.45'); return vt, R(Lt(vt) * g('0.09850'), 4, m) * RT('NaOH', 'HC3H5O3')
calc('sample of lactic acid solution', ['12.00', '0.09850', '0.45', '19.80'], {0: lambda m: U(_hcl(m)[1] / Lt('12.00'), 4, 'M'), 1: lambda m: U(Lt('19.80') * g('0.09850') / Lt('12.00'), 4, 'M'),
     2: lambda m: U(Lt('12.00') * g('0.09850') / Lt(_hcl(m)[0]), 4, 'M'), 3: lambda m: U(_hcl(m)[1] / Lt(_hcl(m)[0]), 4, 'M')})
def _s4(m):
    mb = R(Lt('18.24') * g('0.1120'), 4, m); return mb, R(mb * RT('NaOH', 'H2SO4'), 4, m)
calc('5.00 mL sample of H2SO4', ['5.00', '18.24', '0.1120'], {0: lambda m: U(_s4(m)[1] / Lt('5.00'), N('5.00', '18.24', '0.1120'), 'M'), 1: lambda m: U(_s4(m)[0] / Lt('5.00'), 3, 'M'), 2: lambda m: U(_s4(m)[0] / RT('NaOH', 'H2SO4') / Lt('5.00'), 3, 'M'), 3: lambda m: U(_s4(m)[1] / Lt('18.24'), 3, 'M')})
def _ca(m): return R(Lt('22.5') * g('0.140'), 3, m)
calc('reacts completely with 22.5 mL of 0.140 M AlCl3', ['0.115', '22.5', '0.140'], {0: lambda m: U(R(_ca(m) * RT('AlCl3', 'AgNO3'), 3, m) / g('0.115') * 1000, 3, 'mL'), 1: lambda m: U(_ca(m) / g('0.115') * 1000, 3, 'mL'),
     2: lambda m: U(_ca(m) / RT('AlCl3', 'AgNO3') / g('0.115') * 1000, 3, 'mL'), 3: lambda m: U(R(_ca(m) * RT('AlCl3', 'AgNO3'), 3, m) / g('0.140') * 1000, 3, 'mL')})

# ---- ch11-colligative ----
def _molal(gs, f, ws):
    n = N(gs, ws); mol = lambda m: R(g(gs) / MM(f), n, m); tot = ADD(gs, ws)
    return {0: lambda m: U(mol(m) / (g(ws) / 1000), n, 'm'), 1: lambda m: U(mol(m) / g(ws), n, 'm'), 2: lambda m: U(g(gs) / (g(ws) / 1000), n, 'm'), 3: lambda m: U(mol(m) / (g(tot) / 1000), n, 'm')}
calc('dissolving 16.3 g of sucrose', ['16.3', '195.0'], _molal('16.3', 'C12H22O11', '195.0'))
calc('solution of 14.2 g of glycerol', ['14.2', '315.0'], _molal('14.2', 'C3H8O3', '315.0'))
def _osm(m_, f):
    return {0: lambda m: U(g(m_) * I[f] * 1000, 3, 'mOsm/kg'), 1: lambda m: U(g(m_) * 1000, 3, 'mOsm/kg'), 2: lambda m: U(g(m_) * 2 * 1000, 3, 'mOsm/kg'), 3: lambda m: U(g(m_) * I[f], 3, 'mOsm/kg')}
calc('of a 0.155 m CaCl2 solution', ['0.155'], _osm('0.155', 'CaCl2'))
calc('of a 0.0850 m Na2SO4 solution', ['0.0850'], _osm('0.0850', 'Na2SO4'))
def _fp(m_, f):
    dT = lambda m, i: R(i * KF * g(m_), 3, m)
    return {0: lambda m: FP(dT(m, I[f]), m), 1: lambda m: rq(dT(m, I[f]), min(2, dec(fmt(dT(0, I[f]), 3)))) + ' °C',
            2: lambda m: FP(dT(m, 1), m), 3: lambda m: FP(R(I[f] * KB * g(m_), 3, m), m)}
calc('of a 0.425 m KBr solution', ['0.425'], _fp('0.425', 'KBr'))
calc('of a 0.215 m AlCl3 solution', ['0.215'], _fp('0.215', 'AlCl3'))
_eg = lambda m, k, i=1: R(i * k * g('2.35'), 3, m)
calc('2.35 m ethylene glycol', ['2.35'], {0: lambda m: BP(_eg(m, KB, I['ethylene glycol']), m), 1: lambda m: BP(_eg(m, KF), m), 2: lambda m: BP(_eg(m, KB), m, -1), 3: lambda m: BP(_eg(m, KB, 2), m)})
def _mg2(m):
    mol = R(g('1.45') / MM('MgCl2'), 3, m); return mol, R(mol / (g('125.0') / 1000), 3, m)
calc('dissolving 1.45 g of MgCl2', ['1.45', '125.0'], {0: lambda m: U(_mg2(m)[1] * I['MgCl2'] * 1000, 3, 'mOsm/kg'), 1: lambda m: U(_mg2(m)[1] * 1000, 3, 'mOsm/kg'), 2: lambda m: U(_mg2(m)[1] * 2 * 1000, 3, 'mOsm/kg'), 3: lambda m: U(_mg2(m)[1] * I['MgCl2'], 3, 'mOsm/kg')})
calc('freezes at -5.00 °C', ['5.00'], {0: lambda m: U(g('5.00') / (I['NaCl'] * KF), 3, 'm'), 1: lambda m: U(g('5.00') / KF, 3, 'm'), 2: lambda m: U(g('5.00') / (I['NaCl'] * KB), 3, 'm'), 3: lambda m: U(I['NaCl'] * KF * g('5.00'), 3, 'm')})
calc('freezes at -12.0 °C', ['12.0'], {0: lambda m: U(g('12.0') / (I['ethylene glycol'] * KF), 3, 'm'), 1: lambda m: U(g('12.0') / (2 * KF), 3, 'm'), 2: lambda m: U(g('12.0') / KB, 3, 'm'), 3: lambda m: U(KF * g('12.0'), 3, 'm')})

print('Calculation items: key and distractors recomputed (round once = strict, and = the choice as written)')
for sub, givens, specs in CALC:
    q = by(sub)
    if not q: continue
    checked.add(q['id']); stem = txt(q['q'])
    if q.get('f'):
        cap = q['f'][0].get('cap', '')
        if 'NH4Cl' in txt(cap): _nh4(q)
        if 'Buret' in cap: _bur(q)
    eqs = eqs_in(q['q']); CUR['eq'] = eqs[0][1] if eqs else ([], [])
    for gv in givens:
        pat = r'(?<![\d.])' + re.escape(gv) + r'(?![\d])'
        if not re.search(pat, stem): err.append(q['id'] + ' given %r not in stem as written' % gv)
    print('  %s %s' % (q['id'], sub[:52]))
    keys = []
    for j, fn in sorted(specs.items()):
        try: a, b = fn(0), fn(1)
        except Exception as e_: err.append('%s c[%d] spec failed: %r' % (q['id'], j, e_)); continue
        if a != b: err.append('%s c[%d] ambiguous: %s (round once) vs %s (strict)' % (q['id'], j, a, b))
        keys.append(a)
        ok(txt(q['c'][j]).strip() == a, '%s c[%d] %-26r = %r' % (q['id'], j, txt(q['c'][j]).strip(), a))
    if len(set(keys)) != 4: err.append(q['id'] + ' recomputed values not all different: %s' % keys)
    k0 = keys[0].split(' ')[0].rstrip('%') if keys else ''
    if k0 and k0 not in txt(q['w']): err.append(q['id'] + ' answer %s not in w' % k0)
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')

# ---------- conceptual items: key tables ----------
print('Conceptual items checked against key tables')
def chk(sub, cond, msg):
    q = by(sub)
    if q: checked.add(q['id']); ok(cond(q), '%s %s' % (q['id'], msg))
def first_word(c): return plain(c).split(',')[0].split(' (')[0].strip()
def solvent(q):
    parts = re.findall(r'(\d+)% (\w+)', txt(q['q'])); big = max(parts, key=lambda p: int(p[0]))[1]
    return plain(q['c'][0]).startswith(big), big
chk('62% ethanol and 38% water', lambda q: solvent(q)[0], 'solvent = larger amount (%s)' % 'ethanol')
chk('67% copper and 33% zinc', lambda q: solvent(q)[0], 'solvent = larger amount (copper)')
def cls(c):
    t = txt(c)
    for k in sorted(POL, key=len, reverse=True):
        if re.search(r'(?<![A-Za-z0-9])' + re.escape(k) + r'(?![a-z0-9])', t, re.I if k[0].islower() else 0): return POL[k]
    return None
def pair(c): return [cls(x) for x in txt(c).split(' and ')]
chk('Which substance is most soluble in water', lambda q: cls(q['c'][0]) in ('polar', 'ionic') and all(cls(c) == 'nonpolar' for c in q['c'][1:]), 'water (polar): only c[0] polar/ionic')
chk('dissolves best in hexane', lambda q: cls(q['c'][0]) == 'nonpolar' and all(cls(c) in ('polar', 'ionic') for c in q['c'][1:]), 'hexane (nonpolar): only c[0] nonpolar')
def _imm(q):
    ps = [pair(c) for c in q['c']]
    return all(None not in p for p in ps) and ps[0][0] != ps[0][1] and all(p[0] == p[1] for p in ps[1:])
chk('is <b>immiscible</b>'.replace('<b>', '').replace('</b>', ''), _imm, 'immiscible = unlike pair (polar + nonpolar); the others like pairs')
def ival(c):
    t = txt(c)
    for k in sorted(I, key=len, reverse=True):
        if re.search(r'(?<![A-Za-z0-9])' + re.escape(k) + r'(?![a-z0-9])', t): return I[k]
    return None
chk('conducts electricity well', lambda q: ival(q['c'][0]) > 1 and all(ival(c) == 1 for c in q['c'][1:]), 'only c[0] is an electrolyte (i > 1)')
chk('is a strong electrolyte in water', lambda q: ival(q['c'][0]) > 1 and all(ival(c) == 1 for c in q['c'][1:]), 'only c[0] is an electrolyte (i > 1)')
chk("van 't Hoff factor of i = 3", lambda q: ival(q['c'][0]) == 3 and all(ival(c) != 3 for c in q['c'][1:]), 'only c[0] has i = 3: %s' % 'Na2SO4')
def satur(q):
    t = txt(q['q'])
    S_ = D(re.search(r'is ([\d.]+) g per 100', t).group(1))
    gs, ws = re.search(r'([\d.]+) g of (?:sucrose|NH4Cl|NaNO3)[^.]*? (?:in|into) ([\d.]+) g of (?:hot )?water', t).groups()
    cap = S_ * D(ws.rstrip('.')) / 100; x = D(gs.rstrip('.'))
    want = 'unsaturated' if x < cap else 'saturated' if x == cap else ('supersaturated' if 'without any crystals' in t else 'saturated')
    naive = 'unsaturated' if x < S_ else 'saturated' if x == S_ else 'supersaturated'
    return plain(q['c'][0]) == want and (naive == want or any(plain(c) == naive for c in q['c'][1:])), want
for s_ in ('stirs 30.5 g of NH4Cl', 'dissolves 110. g of sucrose', 'contains 176 g of NaNO3'):
    chk(s_, lambda q: satur(q)[0], 'saturation from solubility scaled to the water used')
chk('dropped into a <b>saturated</b>'.replace('<b>', '').replace('</b>', ''), lambda q: 'stays undissolved' in plain(q['c'][0]), 'saturated: added solute stays undissolved')
chk('Vitamin D is a large molecule', lambda q: 'nonpolar' in plain(q['c'][0]) and 'fat' in plain(q['c'][0]), 'mostly nonpolar -> dissolves in fat')
chk('The graph shows the solubility', lambda q: (lambda S_: S_[0][80] - S_[0][20] > 10 * (S_[1][80] - S_[1][20]) > 0 and S_[1][0] > S_[0][0] and S_[0][40] > S_[1][40])(
    [dict(map(tuple, s['pts'])) for s in q['f'][0]['series']]) and 'far more' in plain(q['c'][0]), 'NH4Cl rises far more than NaCl; both rise; curves cross')
def _coldest(q):
    ts = [int(re.search(r'at (\d+) °C', txt(c)).group(1)) for c in q['c']]
    return ts[0] == min(ts)
chk('hold the most dissolved oxygen', _coldest, 'gas solubility falls with T: coldest holds most')
GAS = {'T': -1, 'P': +1}
chk('scuba diver rises', lambda q: plain(q['c'][0]).startswith('the pressure drops, so less'), 'Henry: P down -> less dissolved gas')
chk('chill the drink and seal it', lambda q: GAS['T'] < 0 < GAS['P'] and 'low temperature and high co2 pressure both make co2 more soluble' in plain(q['c'][0]), 'gas: colder and higher P -> more soluble')
chk('put under 5 atm of pressure', lambda q: plain(q['c'][0]).startswith('almost nothing'), 'pressure ~no effect on solids')
chk('tiny bubbles form on the inside of the glass', lambda q: 'less soluble in warmer water' in plain(q['c'][0]) and 'gas' in plain(q['c'][0]), 'gas solubility falls with T: dissolved air leaves on warming')
chk('increases the amount of CO2 that can dissolve', lambda q: plain(q['c'][0]).startswith('cooling') and 'raising' in plain(q['c'][0]), 'gas: colder and higher P')
chk('Hot tea dissolves more sugar', lambda q: 'increases as the temperature rises' in plain(q['c'][0]), 'most solids more soluble when hot')
chk('soda is opened', lambda q: 'pressure above the liquid drops' in plain(q['c'][0]), 'Henry: P down -> bubbles')
chk('labeled 0.9% (m/v) NaCl', lambda q: plain(q['c'][0]) == '0.9 g of nacl in every 100 ml of solution', '%(m/v) = g per 100 mL solution')
chk('1 ppb is about the same', lambda q: plain(q['c'][0]) == '1 µg per liter', '1 ppb ≈ 1 µg/L')
chk('adds 0.175 mol of KCl to 1.000 L of water', lambda q: 'liters of solution' in plain(q['c'][0]), 'M = mol / L solution')
chk('which quantity stays the same', lambda q: plain(q['c'][0]) == 'the moles of solute', 'dilution keeps moles')
chk('100-mL volumetric flask', lambda q: plain(q['c'][0]).startswith('pipet the calculated volume of stock into the flask, then add water up to the line'), 'stock first, then water to the line')
chk('larger than the stock concentration', lambda q: 'swapped' in plain(q['c'][0]), 'M2 > M1 -> volumes swapped')
chk('deep, dark pink', lambda q: plain(q['c'][0]).startswith('the endpoint was passed'), 'phenolphthalein: endpoint = first faint pink; deep pink = excess base')
chk('uses a wash bottle', lambda q: 'does not change' in plain(q['c'][0]), 'water does not react: same moles')
def _h2so4(q):
    e = eqs_in(q['y'][0])[0][1]; co = {f: c for side in e for c, f, ph in side}
    return co['NaOH'] / co['H2SO4'] == 2 and 'twice as much' in plain(q['c'][0]) and plain(q['c'][0]).index('h2so4') < plain(q['c'][0]).index('twice')
chk('Equal volumes of 0.10 M HCl and 0.10 M H2SO4', _h2so4, 'H2SO4 : NaOH = 1 : 2 vs HCl 1 : 1 -> twice')
chk('must a NaOH solution be standardized', lambda q: 'co2' in plain(q['c'][0]), 'NaOH absorbs CO2')
chk('At the endpoint of a titration of HCl with NaOH', lambda q: plain(q['c'][0]).startswith('the moles of naoh added equal'), '1 : 1 -> moles equal')
chk('freezes closest to 0 °C', lambda q: (lambda pm: min(pm, key=pm.get) == txt(q['c'][0]) and len(set(pm.values())) == 4 and min(pm, key=lambda k: D(dict((txt(r[0]), r[1]) for r in q['f'][0]['rows'])[k])) != txt(q['c'][0]))(
    {txt(r[0]): D(r[1]) * ival(r[0]) for r in q['f'][0]['rows']}), 'highest freezing point = smallest i x m (table); smallest molality alone points elsewhere')
def _hb(q):
    pm = {txt(c): D(re.match(r'([\d.]+) m', txt(c)).group(1)) * ival(c) for c in q['c']}
    return max(pm, key=pm.get) == txt(q['c'][0]) and len(set(pm.values())) == 4
chk('has the <b>highest</b> boiling point'.replace('<b>', '').replace('</b>', ''), _hb, 'highest boiling point = largest i x m')
chk('molality, not molarity', lambda q: 'mass of solvent' in plain(q['c'][0]), 'mass does not change with T')
def _osmo(q):
    t = txt(q['q']); a, b = [D(x) for x in re.findall(r'(\d+)% glucose', t)]
    return (a < b) and plain(q['c'][0]).startswith('from side a to side b')
chk('5% glucose (side A) from 10% glucose (side B)', _osmo, 'water moves toward higher solute (A 5% -> B 10%)')
chk('0.10 m NaCl from 0.10 m glucose', lambda q: I['NaCl'] * D('0.10') > I['glucose'] * D('0.10') and plain(q['c'][0]).startswith('toward the nacl side'), 'NaCl 0.20 m particles > glucose 0.10 m: water toward NaCl')
def tonic(osm):
    return 'isotonic' if SERUM[0] <= osm <= SERUM[1] else 'hypotonic' if osm < SERUM[0] else 'hypertonic'
_ns = 2 * D('0.9') * 10 / MM('NaCl') * 1000   # 0.9 g per 100 mL ~ 9 g per kg water, i = 2, mOsm/kg (ideal estimate)
chk('Mateo Herrera, who has asthma, receives 0.9% NaCl', lambda q: plain(q['c'][0]).startswith('isotonic') and abs(_ns - 300) < 15, '0.9%% NaCl ~ %s mOsm/kg ideal (text: about 286 measured) -> isotonic' % fmt(_ns, 3))
chk('placed in seawater, which is about 1000 mOsm/kg', lambda q: tonic(1000) == 'hypertonic' and 'out of the cells' in plain(q['c'][0]) and 'crenation' in plain(q['c'][0]), 'hypertonic -> water out, crenation')
_hn = 2 * D('0.45') * 10 / MM('NaCl') * 1000
chk('placed in 0.45% NaCl', lambda q: tonic(_hn) == 'hypotonic' and plain(q['c'][0]).startswith('hypotonic: water flows into the cells'), '0.45%% NaCl ~ %s mOsm/kg -> hypotonic, water in' % fmt(_hn, 3))
chk('NaCl dissolves in water, how are the water molecules arranged', lambda q: re.search(r'oxygen ends face na\^\+', plain(q['c'][0])) is not None, 'δ- O toward cation, δ+ H toward anion')
chk('glucose solution does not conduct', lambda q: I['glucose'] == 1 and 'whole molecules' in plain(q['c'][0]), 'glucose i = 1: no ions')
chk('separate into layers no matter how hard', lambda q: 'hydrogen bond' in plain(q['c'][0]) and 'nonpolar' in plain(q['c'][0]), 'water H-bonds squeeze out nonpolar oil')
chk('mix in all proportions. What is the term', lambda q: plain(q['c'][0]) == 'miscible', 'all proportions = miscible')

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
print('Draft overlap: no stem reuses a worked example or exercise from drafts/ch11')
GIV = r'(-?\d+\.\d+|\d+\.|\d+)(?: x 10\^(-?\d+))? ?(mg/L|g/mL|g/L|mOsm/kg|mol|mL|mM|mg|kg|ppm|ppb|ppt|atm|°C|g|L|M|m|%)(?![A-Za-z/])'
CONST = {'1.86', '0.512', '0.00', '100.00', '100', '100.', '1', '1.00', '0', '0.9', '5', '3', '2', '10', '1000', '275', '295', '286',
         '9', '4', '6', '20', '25', '37', '45', '70', '0.45', '1.0', '9.0', '0.1', '36', '300', '350', '1,000', '1,500', '22,600', '50', '1200'}
def givens_in(t): return {(a + ('e' + b if b else ''), u) for a, b, u in re.findall(GIV, t) if a not in CONST}
BANNED = {('15.0', 'g'), ('135.0', 'g'), ('500.', 'mL'), ('0.0124', 'mg/L'), ('5.25', 'g'), ('1.04', 'g/mL'), ('26.0', 'g'), ('224.0', 'g'),
          ('52', 'mg/L'), ('2.50', 'g'), ('125.0', 'mL'), ('0.150', 'M'), ('25.0', 'mL'), ('500.0', 'mL'), ('0.250', 'M'), ('0.0350', 'mol'),
          ('0.500', 'M'), ('10.00', 'mL'), ('1.80', 'M'), ('25.00', 'mL'), ('0.500', 'mL'), ('0.500', '%'), ('3.00', 'mL'), ('15.0', 'mM'),
          ('250.0', 'mL'), ('0.600', 'M'), ('0.154', 'M'), ('15.0', 'mL'), ('6.00', 'M'), ('2.00', 'M'), ('0.0500', 'M'), ('20.0', 'mL'),
          ('0.100', 'M'), ('0.1050', 'M'), ('18.45', 'mL'), ('0.2150', 'g'), ('31.62', 'mL'), ('0.500', 'g'), ('22.45', 'mL'), ('0.120', 'M'),
          ('0.200', 'M'), ('20.00', 'mL'), ('27.80', 'mL'), ('0.5000', 'M'), ('30.0', 'mL'), ('12.0', 'g'), ('250.0', 'g'), ('0.650', 'm'),
          ('1.50', 'm'), ('9.00', 'g'), ('5.85', 'g'), ('500.0', 'g'), ('80.0', 'g'), ('1.45', 'g/L'), ('3.60', 'atm'), ('0.78', 'atm'),
          ('2.34', 'atm'), ('34.2', 'g'), ('25.0', 'g'), ('38.0', 'g'), ('110', 'g'), ('31.6', 'g'), ('48.4', 'g'), ('10.0', '%')}
blocks = []
for p_ in sorted(glob.glob(os.path.join(ROOT, 'drafts', 'ch11', '*.html'))):
    h = open(p_, encoding='utf-8').read()
    for b in re.split(r'(?=Example \\\(\\PageIndex|Exercise \\\(\\PageIndex|<h2|Problem 11\.\d+\b)', h):
        t = re.sub(r'\\\(|\\\)|\\dfrac|\\text|\\times|\\ |\\qquad|\\left|\\right|\\cdot|\\tfrac|\\,|\\;|\\mu', ' ', b)
        t = re.sub(r'\{\}\^\\circ\s*', '°', t).replace('\\circ', '°').replace('\\%', '%')
        t = txt(re.sub(r'[{}]', ' ', t)); t = re.sub(r'\s+', ' ', t)
        m = re.search(r'Problem (11\.\d+)', t)
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
print('  conceptual (key read by hand; quoted values still checked):', ' '.join(sorted(hand)) or 'none')
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
