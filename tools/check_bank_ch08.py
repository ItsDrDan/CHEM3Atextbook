#!/usr/bin/env python3
"""Checker for the Chapter 8 banks (mole ratios, mass-to-mass, solutions and gases, limiting reactant, yield,
enthalpy of reaction). Structural checks as in tools/check_bank_ch07.py (ch08 topic ids; ADAPT = 42 items, text only,
y[0] begins "Correct: "; tables at most 3 columns), plus, written independently of the generators:
  - every equation anywhere in an item (stem, choices, feedback, hint, worked explanation) is parsed back out of the
    HTML and must balance atom for atom (an unbalanced equation is allowed only in a stem that says "unbalanced");
  - every Delta H quoted in a stem is checked against the allowed standard values (CH4 -890.3, glucose -2803,
    2 H2 + O2 -> 2 H2O(l) -571.6, C3H8 -2220, CaCO3 -> CaO + CO2 +178 kJ), scaled by the equation's coefficients and
    sign-flipped when reversed;
  - every "formula x g/mol" and "Symbol x g/mol" anywhere is the checker's own molar mass (yellow-sheet atomic masses,
    Decimal, addition rule: round once to the fewest decimal places of the masses used);
  - every calculation item (k=1): the key and each numeric distractor's intended error are recomputed with Decimal
    from the givens as written in the stem, mole ratios read from the stem's own equation, molar volume 22.4 L/mol
    (3 s.f.), sig figs by the multiplication/division rule (mole ratios exact) and the decimal-place rule for
    leftovers; limiting reactants found by running each reactant to the product;
  - conceptual items with numbers or particle/table figures (limiting reactant, exact ratios, Delta H scaling,
    conservation of mass) are checked by spec; the rest are listed as read by hand;
  - course rule: no whole number ending in 0 without a decimal point in a calculation stem;
  - exactly one correct choice (the recomputed key differs from every distractor; four different choices);
  - no stem reuses a draft worked example or exercise (same equation and a shared given), no stem in both banks.
usage: python3 tools/check_bank_ch08.py bank/ch08.json bank/ch08_adapt.json"""
import json, sys, re, os, collections, glob
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
from fractions import Fraction as Fr
getcontext().prec = 50; getcontext().rounding = ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YS = json.load(open(os.path.join(ROOT, 'tools', 'yellow_sheet_masses.json')))
AM = YS['masses']
TOP = {'ch08-moleratio', 'ch08-massmass', 'ch08-solgas', 'ch08-limiting', 'ch08-yield', 'ch08-enthalpy'}
err = []

# ---------- text ----------
def txt(x):
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<[^>]+>', '', x)
    for a, b in (('&middot;', '.'), ('&minus;', '-'), ('−', '-'), ('&times;', 'x'), ('&nbsp;', ' '), ('&divide;', '/'),
                 ('&rarr;', '->'), ('→', '->'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&deg;', '°'), ('&Delta;', 'Δ'),
                 ('&lt;', '<'), ('&gt;', '>'), ('&sup2;', '²'), ('&amp;', '&')):
        x = x.replace(a, b)
    return x
def plain(x): return re.sub(r'\s+', ' ', txt(x)).strip().lower()

# ---------- structural checks ----------
OUT_OF_SCOPE = r"Hess|PV ?= ?nRT|ideal gas law|molality|bond energ|specific heat|calorimeter|equilibrium constant|all of the above|none of the above"
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
        if re.search(OUT_OF_SCOPE, s, re.I): err.append(i + ' out of scope term or AOTA/NOTA')
        if 'f' in q and not allow_f: err.append(i + ' has f (ADAPT items must be text only)')
        for f in q.get('f', []):
            if f['type'] == 'table':
                if max(len(f['head']), *[len(r) for r in f['rows']]) > 3: err.append(i + ' table wider than 3 columns')
                if max(len(plain(x)) for r in f['rows'] + [f['head']] for x in r) > 32: err.append(i + ' table cell too long for a phone')
            elif f['type'] != 'particles': err.append(i + ' figure type not checked here: ' + f['type'])
        if label == 'HW' and not q['y'][0].startswith('Correct: '): err.append(i + ' ADAPT y[0] lacks "Correct: "')
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if right in plain(q['y'][j]): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c8-%03d', 'TRY', True)
structural(HW, 'c8-h%02d', 'HW', False)
if len(HW) != 42: err.append('ADAPT has %d items, not 42' % len(HW))
if sum(1 for q in TRY if q.get('f')) > 4: err.append('more than 4 figures')
ALL = TRY + HW

def ok(cond, msg):
    print('   ', 'OK ' if cond else 'BAD', msg)
    if not cond: err.append(msg)

# ---------- formulas and molar masses ----------
def atoms(f):
    def grp(s, i):
        c = collections.Counter()
        while i < len(s) and s[i] != ')':
            if s[i] == '(':
                inner, i = grp(s, i + 1)
                if i >= len(s): raise ValueError(f)
                i += 1
                m = re.match(r'\d*', s[i:]); k = int(m.group() or 1); i += m.end()
                for e in inner: c[e] += inner[e] * k
            else:
                m = re.match(r'([A-Z][a-z]?)(\d*)', s[i:])
                if not m or m.group(1) not in AM: raise ValueError('bad formula %r' % f)
                c[m.group(1)] += int(m.group(2) or 1); i += m.end()
        return c, i
    total = collections.Counter()
    for k, piece in enumerate(f.split('.')):
        m = re.match(r'(\d*)(.+)', piece); mult = int(m.group(1) or 1) if k else 1
        c, i = grp(m.group(2), 0)
        if i != len(m.group(2)): raise ValueError('bad formula %r' % f)
        for e in c: total[e] += c[e] * mult
    return total
def places(s): return len(s.partition('.')[2])
def MMraw(f): return sum((D(AM[e]) * n for e, n in atoms(f).items()), D(0))
def MM(f): return MMraw(f).quantize(D(10) ** -min(places(AM[e]) for e in atoms(f)))
for f, want in (('C6H12O6', '180.156'), ('CO2', '44.009'), ('N2', '28.014'), ('NH3', '17.031'), ('CH4', '16.043'),
                ('O2', '31.998'), ('H2O', '18.015'), ('Mg(OH)2', '58.32'), ('Fe2O3', '159.70'), ('AlCl3', '133.33'),
                ('MgO', '40.31'), ('C7H6O3', '138.122'), ('C9H8O4', '180.159'), ('CaCO3', '100.09'), ('CaO', '56.08'),
                ('KAl(SO4)2.12H2O', '474.37'), ('Cl2', '70.90')):
    if str(MM(f)) != want: err.append('checker molar mass %s = %s, chapter text says %s' % (f, MM(f), want))
print('Checker molar masses agree with the Chapter 8 text (glucose 180.156, CO2 44.009, NH3 17.031, alum 474.37, ...)')

# ---------- numbers ----------
def sf(s):
    s = s.strip()
    if re.search(r'e', s, re.I): s = s.lower().split('e')[0]
    digits = s.replace('.', '').replace('-', '').lstrip('0')
    if '.' in s: return len(digits)
    return len(digits.rstrip('0'))
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
def dec(s): return len(s.partition('.')[2])
def addsub(a, b, sign=1):
    """a +/- b, both strings as written; decimal-place rule."""
    q = min(dec(a), dec(b)); return format((D(a) + sign * D(b)).quantize(D(10) ** -q), 'f')
def left(present, used, n):
    """leftover = present (string as written) - used (rounded to n s.f. first); decimal-place rule."""
    u = fmt(used, n)
    if 'x' in u: raise ValueError(u)
    return addsub(present, u, -1), u

# ---------- equations ----------
SPC = r'(?:\d+ )?[A-Z(][A-Za-z0-9()]*(?:\((?:s|l|g|aq)\))?'
EQRE = re.compile(SPC + r'(?: \+ ' + SPC + r')* -> ' + SPC + r'(?: \+ ' + SPC + r')*')
def sp(tok):
    m = re.fullmatch(r'(\d+) (.+)', tok.strip()); co = int(m.group(1)) if m else 1
    t = m.group(2) if m else tok.strip()
    ph = None
    m = re.fullmatch(r'(.+?)\((s|l|g|aq)\)', t)
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
def key_of(f): return frozenset(atoms(f).items())
def eqvec(e):
    v = collections.Counter()
    for co, f, ph in e[0]: v[key_of(f)] -= co
    for co, f, ph in e[1]: v[key_of(f)] += co
    return v
BASE = [('CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(l)', D('-890.3')), ('C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O', D('-2803')),
        ('2 H2(g) + O2(g) -> 2 H2O(l)', D('-571.6')), ('C3H8(g) + 5 O2(g) -> 3 CO2(g) + 4 H2O(l)', D('-2220')),
        ('CaCO3(s) -> CaO(s) + CO2(g)', D('178'))]
BASE = [(eqvec(parse_eq(s)), v, parse_eq(s)) for s, v in BASE]
def expected_dH(e):
    v = eqvec(e)
    for bv, dh, be in BASE:
        if set(bv) != set(v): continue
        k0 = Fr(v[next(iter(v))], bv[next(iter(v))])
        if all(Fr(v[x], bv[x]) == k0 for x in v):
            # H2O(l) required where the standard value is for liquid water
            for co, f, ph in e[0] + e[1]:
                if f == 'H2O' and ph not in (None, 'l') and any(f2 == 'H2O' and p2 == 'l' for c2, f2, p2 in be[1]):
                    return None
            return dh * D(k0.numerator) / D(k0.denominator)
    return None
def num_of(s):
    s = s.replace(' ', '')
    m = re.fullmatch(r'([+-]?[\d.]+)(?:x10\^(-?\d+))?', s)
    return D(m.group(1)) * (D(10) ** int(m.group(2)) if m.group(2) else 1)

print('Equations (every field) balance; Delta H values in stems are the standard ones, scaled and signed')
neq = 0
for q in ALL:
    i = q['id']
    for where, h in [('q', q['q']), ('h', q['h']), ('w', q['w'])] + [('c%d' % j, c) for j, c in enumerate(q['c'])] + [('y%d' % j, y) for j, y in enumerate(q['y'])]:
        for s_, e in eqs_in(h):
            neq += 1
            if not balanced(e):
                if not (where == 'q' and 'unbalanced' in q['q']): err.append('%s %s: unbalanced equation %s' % (i, where, s_))
    st = txt(q['q'])
    for m in re.finditer(r'ΔH = ([+-]?[\d.]+(?: x 10\^\d+)?) kJ', st):
        before = [x for x in eqs_in(q['q']) if st.find(x[0]) < m.start()]
        if not before: err.append(i + ' Delta H with no equation before it'); continue
        s_, e = before[-1]
        want = expected_dH(e); got = num_of(m.group(1))
        ok(want is not None and got == want, '%s ΔH %s kJ for %s (standard %s)' % (i, m.group(1), s_, want))
print('    %d equations parsed, all balanced' % neq)

# ---------- molar masses quoted anywhere ----------
print('Quoted molar masses (formula x g/mol) against the yellow sheet and the addition rule')
nmm = 0
for q in ALL:
    for h in [q['q'], q['w'], q['h']] + q['c'] + q['y']:
        for f, v in re.findall(r'(?<![A-Za-z0-9(])([A-Z][A-Za-z0-9().]*?) (\d+\.\d+) g/mol', txt(h)):
            try: want = str(MM(f))
            except ValueError: err.append('%s unknown formula %r before %s g/mol' % (q['id'], f, v)); continue
            nmm += 1
            if want != v: err.append('%s quotes %s %s g/mol; checker %s' % (q['id'], f, v, want))
    for h in [q['q'], q['w']] + q['y']:   # "(Na 22.99" style atomic masses
        for sym, v in re.findall(r'\((?:[^()]*; )?([A-Z][a-z]?) (\d+\.\d+)(?: g/mol)?[;)]', txt(h)):
            if sym in AM and AM[sym] != v: err.append('%s quotes %s %s; yellow sheet %s' % (q['id'], sym, v, AM[sym]))
print('    %d molar masses quoted, all recomputed' % nmm)

# ---------- calculation items ----------
def by(sub):
    m = [q for q in ALL if sub in txt(q['q'])]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
CUR = {}
def C(f): return CUR['coef'][f]
def R(a, b): return D(C(b)) / D(C(a))
def mol(g_, f): return D(g_) / MM(f)
def DHmag(): return CUR['dH']
def lim(amts, prod):
    """amts {formula: moles}; returns (limiting formula, {formula: moles of prod it could make})."""
    p = {f: n * R(f, prod) for f, n in amts.items()}
    lo = min(p, key=p.get)
    if list(p.values()).count(p[lo]) != 1: raise ValueError('tie')
    return lo, p
checked, hand = set(), set()
g = D
# (stem substring, givens as written (stem or figure), formulas whose molar mass is used, other factors (s.f. only),
#  unit, {choice: (value, why[, unit])}); value: Decimal (formatted to the item's s.f.) or ('raw', exact text)
CALC = [
 # ---- ch08-moleratio ----
 ('3.60 mol of NH3', ['3.60'], [], [], 'mol O2', {0: (lambda: g('3.60') * R('NH3', 'O2'), 'x 5/4'), 1: (lambda: g('3.60') * R('O2', 'NH3'), 'flipped'), 2: (lambda: g('3.60'), 'skipped ratio'), 3: (lambda: g('3.60') * R('NH3', 'H2O'), 'used H2O coefficient')}),
 ('produce 0.480 mol of CO2', ['0.480'], ['C6H12O6'], [], 'mol C6H12O6', {0: (lambda: g('0.480') * R('CO2', 'C6H12O6'), 'x 1/6'), 1: (lambda: g('0.480') * R('C6H12O6', 'CO2'), 'flipped'), 2: (lambda: g('0.480'), 'skipped ratio'), 3: (lambda: g('0.480') * R('CO2', 'C6H12O6') * MM('C6H12O6'), 'went on to grams', 'g C6H12O6')}),
 ('form from 0.856 mol of H2O2', ['0.856'], ['O2'], [], 'mol O2', {0: (lambda: g('0.856') * R('H2O2', 'O2'), 'x 1/2'), 1: (lambda: g('0.856') * R('O2', 'H2O2'), 'flipped'), 2: (lambda: g('0.856'), 'skipped ratio'), 3: (lambda: g('0.856') * R('H2O2', 'O2') * MM('O2'), 'went on to grams', 'g O2')}),
 ('produce 1.25 mol of Fe', ['1.25'], [], [], 'mol CO', {0: (lambda: g('1.25') * R('Fe', 'CO'), 'x 3/2'), 1: (lambda: g('1.25') * R('CO', 'Fe'), 'flipped'), 2: (lambda: g('1.25'), 'skipped ratio'), 3: (lambda: g('1.25') * R('Fe', 'Fe2O3'), 'moles of Fe2O3')}),
 ('if 2.46 mol of H2O formed', ['2.46'], [], [], 'mol O2', {0: (lambda: g('2.46') * R('H2O', 'O2'), 'x 5/4'), 1: (lambda: g('2.46') * R('O2', 'H2O'), 'flipped'), 2: (lambda: g('2.46') * R('H2O', 'C3H8'), 'moles of propane'), 3: (lambda: g('2.46'), 'skipped ratio')}),
 ('thin oxide layer that protects aluminum', ['0.80'], [], [], 'mol O2', {0: (lambda: g('0.80') * R('Al', 'O2'), 'x 3/4'), 1: (lambda: g('0.80') * R('O2', 'Al'), 'flipped'), 2: (lambda: g('0.80') * R('Al', 'Al2O3'), 'used Al2O3 coefficient'), 3: (lambda: g('0.80'), 'skipped ratio')}),
 ('0.620 mol of KClO3', ['0.620'], [], [], 'mol O2', {0: (lambda: g('0.620') * R('KClO3', 'O2'), 'x 3/2'), 1: (lambda: g('0.620') * R('O2', 'KClO3'), 'flipped'), 2: (lambda: g('0.620'), 'skipped ratio'), 3: (lambda: g('0.620') * C('O2'), 'left out the 2')}),
 ('make 5.30 mol of NH3', ['5.30'], [], [], 'mol H2', {0: (lambda: g('5.30') * R('NH3', 'H2'), 'x 3/2'), 1: (lambda: g('5.30') * R('H2', 'NH3'), 'flipped'), 2: (lambda: g('5.30'), 'skipped ratio'), 3: (lambda: g('5.30') * C('H2'), 'left out the 2')}),
 ('when 0.715 mol of O2 is used', ['0.715'], [], [], 'mol CO2', {0: (lambda: g('0.715') * R('O2', 'CO2'), 'x 2/3'), 1: (lambda: g('0.715') * R('CO2', 'O2'), 'flipped'), 2: (lambda: g('0.715'), 'skipped ratio'), 3: (lambda: g('0.715') * C('CO2'), 'left out the 3')}),
 ('exactly 1 mol of Cl2', [], ['Na'], [], 'g Na', {0: (lambda: ('raw', str(C('Na') * MM('Na') / C('Cl2')) + ' g Na'), '2 mol Na'), 1: (lambda: ('raw', AM['Na'] + ' g Na'), '1 mol Na'), 2: (lambda: ('raw', str(C('Na') * MM('Cl2')) + ' g Na'), 'mass of 2 mol Cl2'), 3: (lambda: ('raw', '%d g Na' % C('Na')), 'coefficient as grams')}),
 ('when 3.52 mol of SO2 forms', ['3.52'], [], [], 'mol O2', {0: (lambda: g('3.52') * R('SO2', 'O2'), 'x 11/8'), 1: (lambda: g('3.52') * R('O2', 'SO2'), 'flipped'), 2: (lambda: g('3.52'), 'skipped ratio'), 3: (lambda: g('3.52') * R('FeS2', 'O2'), 'used FeS2 coefficient')}),
 # ---- ch08-massmass ----
 ('from 75.0 g of glucose', ['75.0'], ['C6H12O6', 'C2H5OH'], [], 'g C2H5OH', {0: (lambda: mol('75.0', 'C6H12O6') * R('C6H12O6', 'C2H5OH') * MM('C2H5OH'), 'road map'), 1: (lambda: mol('75.0', 'C6H12O6') * MM('C2H5OH'), 'skipped ratio'), 2: (lambda: mol('75.0', 'C6H12O6') * R('C6H12O6', 'C2H5OH') * C('C2H5OH') * MM('C2H5OH'), 'coefficient in molar mass'), 3: (lambda: mol('75.0', 'C6H12O6') * R('C6H12O6', 'C2H5OH'), 'stopped at moles', 'mol C2H5OH')}),
 ('contains 0.750 g of calcium carbonate', ['0.750'], ['CaCO3', 'HCl'], [], 'g HCl', {0: (lambda: mol('0.750', 'CaCO3') * R('CaCO3', 'HCl') * MM('HCl'), 'road map'), 1: (lambda: mol('0.750', 'CaCO3') * MM('HCl'), 'skipped ratio'), 2: (lambda: mol('0.750', 'CaCO3') * R('HCl', 'CaCO3') * MM('HCl'), 'flipped'), 3: (lambda: g('0.750') * C('HCl'), 'grams x coefficient')}),
 ('make 85.0 g of NH3', ['85.0'], ['NH3', 'H2'], [], 'g H2', {0: (lambda: mol('85.0', 'NH3') * R('NH3', 'H2') * MM('H2'), 'road map'), 1: (lambda: mol('85.0', 'NH3') * MM('H2'), 'skipped ratio'), 2: (lambda: mol('85.0', 'NH3') * R('H2', 'NH3') * MM('H2'), 'flipped'), 3: (lambda: mol('85.0', 'NH3') * R('NH3', 'H2') * MM('H'), 'H atom mass')}),
 ('oxidize 16.5 g of glucose', ['16.5'], ['C6H12O6', 'O2'], [], 'g O2', {0: (lambda: mol('16.5', 'C6H12O6') * R('C6H12O6', 'O2') * MM('O2'), 'road map'), 1: (lambda: mol('16.5', 'C6H12O6') * MM('O2'), 'skipped ratio'), 2: (lambda: mol('16.5', 'C6H12O6') * R('C6H12O6', 'O2') * MM('O'), 'O atom mass'), 3: (lambda: mol('16.5', 'C6H12O6') * R('O2', 'C6H12O6') * MM('O2'), 'flipped')}),
 ('from 3.65 g of Mg', ['3.65'], ['Mg', 'MgO'], [], 'g MgO', {0: (lambda: mol('3.65', 'Mg') * R('Mg', 'MgO') * MM('MgO'), 'road map'), 1: (lambda: g('3.65'), 'same mass as Mg'), 2: (lambda: mol('3.65', 'Mg') * R('Mg', 'MgO') * C('MgO') * MM('MgO'), 'coefficient in molar mass'), 3: (lambda: mol('3.65', 'Mg') * R('Mg', 'MgO'), 'stopped at moles', 'mol MgO')}),
 ('when 26.5 g of propane burns', ['26.5'], ['C3H8', 'CO2'], [], 'g CO2', {0: (lambda: mol('26.5', 'C3H8') * R('C3H8', 'CO2') * MM('CO2'), 'road map'), 1: (lambda: mol('26.5', 'C3H8') * MM('CO2'), 'skipped ratio'), 2: (lambda: mol('26.5', 'C3H8') * R('CO2', 'C3H8') * MM('CO2'), 'flipped'), 3: (lambda: mol('26.5', 'C3H8') * R('C3H8', 'CO2') * C('CO2') * MM('CO2'), 'coefficient twice')}),
 ('when 8.40 g of iron rusts', ['8.40'], ['Fe', 'O2'], [], 'g O2', {0: (lambda: mol('8.40', 'Fe') * R('Fe', 'O2') * MM('O2'), 'road map'), 1: (lambda: mol('8.40', 'Fe') * R('O2', 'Fe') * MM('O2'), 'flipped'), 2: (lambda: mol('8.40', 'Fe') * R('Fe', 'O2') * MM('O'), 'O atom mass'), 3: (lambda: mol('8.40', 'Fe') * MM('O2'), 'skipped ratio')}),
 ('exactly with 3.45 g of salicylic acid', ['3.45'], ['C7H6O3', 'C4H6O3'], [], 'g C4H6O3', {0: (lambda: mol('3.45', 'C7H6O3') * R('C7H6O3', 'C4H6O3') * MM('C4H6O3'), 'road map'), 1: (lambda: g('3.45'), '1:1 read as equal mass'), 2: (lambda: g('3.45') * MM('C7H6O3') / MM('C4H6O3'), 'molar masses flipped'), 3: (lambda: mol('3.45', 'C7H6O3') * R('C7H6O3', 'C4H6O3'), 'stopped at moles', 'mol C4H6O3')}),
 ('from 3.36 g of NaHCO3', ['3.36'], ['NaHCO3', 'CO2'], [], 'g CO2', {0: (lambda: mol('3.36', 'NaHCO3') * R('NaHCO3', 'CO2') * MM('CO2'), 'road map'), 1: (lambda: mol('3.36', 'NaHCO3') * MM('CO2'), 'skipped ratio'), 2: (lambda: mol('3.36', 'NaHCO3') * R('CO2', 'NaHCO3') * MM('CO2'), 'flipped'), 3: (lambda: g('3.36') / (C('NaHCO3') * MM('NaHCO3')) * R('NaHCO3', 'CO2') * MM('CO2'), 'coefficient in molar mass')}),
 ('road map for 30.0 g of glucose', ['30.0'], ['C6H12O6', 'CO2'], [], 'g CO2', {0: (lambda: mol('30.0', 'C6H12O6') * R('C6H12O6', 'CO2') * MM('CO2'), 'road map'), 1: (lambda: mol('30.0', 'C6H12O6') * MM('CO2'), 'skipped ratio'), 2: (lambda: mol('30.0', 'C6H12O6') * R('C6H12O6', 'CO2') * C('CO2') * MM('CO2'), 'coefficient again'), 3: (lambda: mol('30.0', 'C6H12O6') * R('C6H12O6', 'CO2'), 'moles labeled grams')}),
 ('exactly with 12.5 g of Fe2O3', ['12.5'], ['Fe2O3', 'Al'], [], 'g Al', {0: (lambda: mol('12.5', 'Fe2O3') * R('Fe2O3', 'Al') * MM('Al'), 'road map'), 1: (lambda: mol('12.5', 'Fe2O3') * MM('Al'), 'skipped ratio'), 2: (lambda: mol('12.5', 'Fe2O3') * R('Al', 'Fe2O3') * MM('Al'), 'flipped'), 3: (lambda: mol('12.5', 'Fe2O3') * R('Fe2O3', 'Al') * C('Al') * MM('Al'), 'coefficient in molar mass')}),
 ('from 6.35 g of H2', ['6.35'], ['H2', 'H2O'], [], 'g H2O', {0: (lambda: mol('6.35', 'H2') * R('H2', 'H2O') * MM('H2O'), 'road map'), 1: (lambda: mol('6.35', 'H2') * R('H2', 'H2O') * C('H2O') * MM('H2O'), 'coefficient in molar mass'), 2: (lambda: g('6.35') * MM('H2') / MM('H2O'), 'molar masses flipped'), 3: (lambda: mol('6.35', 'H2') * R('H2', 'H2O'), 'stopped at moles', 'mol H2O')}),
 ('when 9.20 g of ethanol burns', ['9.20'], ['C2H5OH', 'CO2'], [], 'g CO2', {0: (lambda: mol('9.20', 'C2H5OH') * R('C2H5OH', 'CO2') * MM('CO2'), 'road map'), 1: (lambda: mol('9.20', 'C2H5OH') * MM('CO2'), 'skipped ratio'), 2: (lambda: mol('9.20', 'C2H5OH') * R('CO2', 'C2H5OH') * MM('CO2'), 'flipped'), 3: (lambda: mol('9.20', 'C2H5OH') * R('C2H5OH', 'CO2') * C('CO2') * MM('CO2'), 'coefficient twice')}),
 ('make 48.5 g of urea', ['48.5'], ['CO(NH2)2', 'NH3'], [], 'g NH3', {0: (lambda: mol('48.5', 'CO(NH2)2') * R('CO(NH2)2', 'NH3') * MM('NH3'), 'road map'), 1: (lambda: mol('48.5', 'CO(NH2)2') * MM('NH3'), 'skipped ratio'), 2: (lambda: mol('48.5', 'CO(NH2)2') * R('NH3', 'CO(NH2)2') * MM('NH3'), 'flipped'), 3: (lambda: mol('48.5', 'CO(NH2)2') * R('CO(NH2)2', 'NH3') * C('NH3') * MM('NH3'), 'coefficient in molar mass')}),
 ('from 5.75 g of CH4', ['5.75'], ['CH4', 'H2O'], [], 'g H2O', {0: (lambda: mol('5.75', 'CH4') * R('CH4', 'H2O') * MM('H2O'), 'road map'), 1: (lambda: mol('5.75', 'CH4') * MM('H2O'), 'skipped ratio'), 2: (lambda: mol('5.75', 'CH4') * R('H2O', 'CH4') * MM('H2O'), 'flipped'), 3: (lambda: mol('5.75', 'CH4') * R('CH4', 'H2O') * C('H2O') * MM('H2O'), 'coefficient twice')}),
 ('from 2.15 g of NaCl', ['2.15'], ['NaCl', 'AgCl'], [], 'g AgCl', {0: (lambda: mol('2.15', 'NaCl') * R('NaCl', 'AgCl') * MM('AgCl'), 'road map'), 1: (lambda: g('2.15'), '1:1 read as equal mass'), 2: (lambda: g('2.15') * MM('NaCl') / MM('AgCl'), 'molar masses flipped'), 3: (lambda: mol('2.15', 'NaCl') * R('NaCl', 'AgCl'), 'stopped at moles', 'mol AgCl')}),
 ('can 0.350 g of Mg(OH)2 neutralize', ['0.350'], ['Mg(OH)2', 'HCl'], [], 'g HCl', {0: (lambda: mol('0.350', 'Mg(OH)2') * R('Mg(OH)2', 'HCl') * MM('HCl'), 'road map'), 1: (lambda: mol('0.350', 'Mg(OH)2') * MM('HCl'), 'skipped ratio'), 2: (lambda: mol('0.350', 'Mg(OH)2') * R('HCl', 'Mg(OH)2') * MM('HCl'), 'flipped'), 3: (lambda: mol('0.350', 'Mg(OH)2') * R('Mg(OH)2', 'HCl') * C('HCl') * MM('HCl'), 'coefficient twice')}),
 # ---- ch08-solgas ----
 ('in 35.0 mL of 0.150 M HCl', ['35.0', '0.150'], [], [], 'mol HCl', {0: (lambda: g('35.0') / 1000 * g('0.150'), 'L x M'), 1: (lambda: g('35.0') * g('0.150'), 'mL not converted'), 2: (lambda: g('35.0') / 1000 / g('0.150'), 'L / M'), 3: (lambda: g('0.150') / g('35.0'), 'M / mL')}),
 ('reacts with 0.315 g of NaHCO3', ['0.315', '0.125'], ['NaHCO3'], [], 'mL', {0: (lambda: mol('0.315', 'NaHCO3') * R('NaHCO3', 'HCl') / g('0.125') * 1000, 'mol / M -> mL'), 1: (lambda: mol('0.315', 'NaHCO3') * R('NaHCO3', 'HCl') / g('0.125'), 'liters labeled mL'), 2: (lambda: mol('0.315', 'NaHCO3') * R('NaHCO3', 'HCl') * g('0.125') * 1000, 'mol x M'), 3: (lambda: mol('0.315', 'NaHCO3') * R('NaHCO3', 'HCl'), 'stopped at moles', 'mol')}),
 ('forms from 0.346 mol of H2O2', ['0.346'], [], ['22.4'], 'L O2', {0: (lambda: g('0.346') * R('H2O2', 'O2') * g('22.4'), 'ratio x 22.4'), 1: (lambda: g('0.346') * g('22.4'), 'skipped ratio'), 2: (lambda: g('0.346') * R('O2', 'H2O2') * g('22.4'), 'flipped'), 3: (lambda: g('0.346') * R('H2O2', 'O2'), 'stopped at moles', 'mol O2')}),
 ('forms from 15.0 g of CaCO3', ['15.0'], ['CaCO3'], ['22.4'], 'L CO2', {0: (lambda: mol('15.0', 'CaCO3') * R('CaCO3', 'CO2') * g('22.4'), 'g -> mol -> L'), 1: (lambda: g('15.0') * g('22.4'), 'grams x 22.4'), 2: (lambda: mol('15.0', 'CaCO3') * R('CaCO3', 'CO2'), 'stopped at moles', 'mol CO2'), 3: (lambda: mol('15.0', 'CaCO3') * R('CaCO3', 'CO2') / g('22.4'), 'divided by 22.4')}),
 ('forms from 0.0425 g of Mg', ['0.0425'], ['Mg'], ['22.4'], 'mL H2', {0: (lambda: mol('0.0425', 'Mg') * R('Mg', 'H2') * g('22.4') * 1000, 'L -> mL'), 1: (lambda: mol('0.0425', 'Mg') * R('Mg', 'HCl') * g('22.4') * 1000, 'used HCl coefficient'), 2: (lambda: mol('0.0425', 'Mg') * R('Mg', 'H2') * g('22.4'), 'liters labeled mL'), 3: (lambda: mol('0.0425', 'Mg') * R('Mg', 'H2'), 'stopped at moles', 'mol H2')}),
 ('forms from 12.6 g of glucose', ['12.6', '24.5'], ['C6H12O6'], ['22.4'], 'L CO2', {0: (lambda: mol('12.6', 'C6H12O6') * R('C6H12O6', 'CO2') * g('24.5'), 'x 24.5 L/mol'), 1: (lambda: mol('12.6', 'C6H12O6') * R('C6H12O6', 'CO2') * g('22.4'), '22.4 off STP'), 2: (lambda: mol('12.6', 'C6H12O6') * g('24.5'), 'skipped ratio'), 3: (lambda: mol('12.6', 'C6H12O6') * R('C6H12O6', 'CO2'), 'stopped at moles', 'mol CO2')}),
 ('neutralizes 15.0 mL of 0.180 M', ['0.250', '15.0', '0.180'], [], [], 'mL NaOH', {0: (lambda: g('15.0') / 1000 * g('0.180') * R('H2SO4', 'NaOH') / g('0.250') * 1000, 'mol ratio, / M'), 1: (lambda: g('15.0') / 1000 * g('0.180') * R('NaOH', 'H2SO4') / g('0.250') * 1000, 'flipped'), 2: (lambda: g('15.0') / 1000 * g('0.180') / g('0.250') * 1000, 'skipped ratio'), 3: (lambda: g('15.0') / 1000 * g('0.180') * R('H2SO4', 'NaOH') / g('0.250'), 'liters labeled mL')}),
 ('reacts with 40.0 mL of 0.600 M HCl', ['40.0', '0.600'], ['Zn'], [], 'g Zn', {0: (lambda: g('40.0') / 1000 * g('0.600') * R('HCl', 'Zn') * MM('Zn'), 'L x M x ratio x M'), 1: (lambda: g('40.0') / 1000 * g('0.600') * MM('Zn'), 'skipped ratio'), 2: (lambda: g('40.0') * g('0.600') * R('HCl', 'Zn') * MM('Zn'), 'mL not converted'), 3: (lambda: g('40.0') / 1000 * g('0.600') * R('Zn', 'HCl') * MM('Zn'), 'flipped')}),
 ('in 125 mL of a 0.0400 M', ['125', '0.0400'], [], [], 'mol', {0: (lambda: g('125') / 1000 * g('0.0400'), 'L x M'), 1: (lambda: g('125') * g('0.0400'), 'mL not converted'), 2: (lambda: g('125') / 1000 / g('0.0400'), 'L / M'), 3: (lambda: g('0.0400') / g('125'), 'M / mL')}),
 ('make 0.875 mol of NH3', ['0.875'], [], ['22.4'], 'L N2', {0: (lambda: g('0.875') * R('NH3', 'N2') * g('22.4'), 'ratio x 22.4'), 1: (lambda: g('0.875') * g('22.4'), 'skipped ratio'), 2: (lambda: g('0.875') * R('N2', 'NH3') * g('22.4'), 'flipped'), 3: (lambda: g('0.875') * R('NH3', 'N2'), 'stopped at moles', 'mol N2')}),
 ('when 20.0 mL of 0.115 M', ['20.0', '0.115'], ['AgCl'], [], 'g AgCl', {0: (lambda: g('20.0') / 1000 * g('0.115') * R('AgNO3', 'AgCl') * MM('AgCl'), 'L x M x M'), 1: (lambda: g('20.0') * g('0.115') * MM('AgCl'), 'mL not converted'), 2: (lambda: g('20.0') / 1000 * g('0.115'), 'stopped at moles', 'mol AgCl'), 3: (lambda: g('20.0') / 1000 * g('0.115') * MM('AgNO3'), 'AgNO3 molar mass')}),
 ('when 3.85 g of propane burns', ['3.85'], ['C3H8'], ['22.4'], 'L CO2', {0: (lambda: mol('3.85', 'C3H8') * R('C3H8', 'CO2') * g('22.4'), 'g -> mol -> L'), 1: (lambda: mol('3.85', 'C3H8') * g('22.4'), 'skipped ratio'), 2: (lambda: mol('3.85', 'C3H8') * R('CO2', 'C3H8') * g('22.4'), 'flipped'), 3: (lambda: mol('3.85', 'C3H8') * R('C3H8', 'CO2'), 'stopped at moles', 'mol CO2')}),
 ('neutralizes 45.0 mL of 0.0800 M HCl', ['45.0', '0.0800'], ['Mg(OH)2'], [], 'g Mg(OH)2', {0: (lambda: g('45.0') / 1000 * g('0.0800') * R('HCl', 'Mg(OH)2') * MM('Mg(OH)2'), 'L x M x ratio x M'), 1: (lambda: g('45.0') / 1000 * g('0.0800') * MM('Mg(OH)2'), 'skipped ratio'), 2: (lambda: g('45.0') * g('0.0800') * R('HCl', 'Mg(OH)2') * MM('Mg(OH)2'), 'mL not converted'), 3: (lambda: g('45.0') / 1000 * g('0.0800') * R('Mg(OH)2', 'HCl') * MM('Mg(OH)2'), 'flipped')}),
 ('burn 8.00 g of CH4', ['8.00'], ['CH4'], ['22.4'], 'L O2', {0: (lambda: mol('8.00', 'CH4') * R('CH4', 'O2') * g('22.4'), 'g -> mol -> L'), 1: (lambda: mol('8.00', 'CH4') * g('22.4'), 'skipped ratio'), 2: (lambda: mol('8.00', 'CH4') * R('O2', 'CH4') * g('22.4'), 'flipped'), 3: (lambda: mol('8.00', 'CH4') * R('CH4', 'O2'), 'stopped at moles', 'mol O2')}),
 # ---- ch08-limiting ----
 ('1.80 mol of N2 and 4.80 mol of H2', ['1.80', '4.80'], [], [], 'mol NH3', {0: (lambda: min(lim({'N2': g('1.80'), 'H2': g('4.80')}, 'NH3')[1].values()), 'smaller product (H2)'), 1: (lambda: max(lim({'N2': g('1.80'), 'H2': g('4.80')}, 'NH3')[1].values()), 'used excess N2'), 2: (lambda: sum(lim({'N2': g('1.80'), 'H2': g('4.80')}, 'NH3')[1].values()), 'added'), 3: (lambda: g('4.80') * C('NH3'), '2:1 for H2')}),
 ('14.0 g of N2 and 3.60 g of H2', ['14.0', '3.60'], ['N2', 'H2', 'NH3'], [], 'g NH3', {0: (lambda: min(lim({'N2': mol('14.0', 'N2'), 'H2': mol('3.60', 'H2')}, 'NH3')[1].values()) * MM('NH3'), 'N2 limits'), 1: (lambda: max(lim({'N2': mol('14.0', 'N2'), 'H2': mol('3.60', 'H2')}, 'NH3')[1].values()) * MM('NH3'), 'used excess H2'), 2: (lambda: ('raw', addsub('14.0', '3.60') + ' g NH3'), 'added masses'), 3: (lambda: mol('14.0', 'N2') * MM('NH3'), 'skipped ratio')}),
 ('3.40 mol CO and 2.10 mol O2', ['3.40', '2.10'], [], [], 'mol O2', {0: (lambda: ('raw', left('2.10', g('3.40') * R('CO', 'O2'), 3)[0] + ' mol O2'), 'present - used'), 1: (lambda: g('3.40') * R('CO', 'O2'), 'amount used'), 2: (lambda: ('raw', addsub('3.40', '2.10', -1) + ' mol CO'), 'subtracted reactants'), 3: (lambda: ('raw', 'None; both are used up'), 'no leftover')}),
 ('6.50 g of iron and 4.25 g of sulfur', ['6.50', '4.25'], ['Fe', 'S'], [], 'g S', {0: (lambda: ('raw', left('4.25', mol('6.50', 'Fe') * R('Fe', 'S') * MM('S'), 3)[0] + ' g S'), 'present - used'), 1: (lambda: mol('6.50', 'Fe') * R('Fe', 'S') * MM('S'), 'amount used'), 2: (lambda: ('raw', addsub('6.50', '4.25', -1) + ' g'), 'subtracted masses'), 3: (lambda: ('raw', left('4.25', mol('6.50', 'Fe') * R('Fe', 'S') * MM('S'), 3)[0] + ' g Fe'), 'wrong substance')}),
 ('6.60 g of propane and 20.0 g of O2', ['6.60', '20.0'], ['C3H8', 'O2', 'CO2'], [], 'g CO2', {0: (lambda: min(lim({'C3H8': mol('6.60', 'C3H8'), 'O2': mol('20.0', 'O2')}, 'CO2')[1].values()) * MM('CO2'), 'O2 limits'), 1: (lambda: max(lim({'C3H8': mol('6.60', 'C3H8'), 'O2': mol('20.0', 'O2')}, 'CO2')[1].values()) * MM('CO2'), 'used excess propane'), 2: (lambda: ('raw', addsub('6.60', '20.0') + ' g CO2'), 'added masses'), 3: (lambda: mol('20.0', 'O2') * C('CO2') * MM('CO2'), '3 CO2 : 1 O2')}),
 ('3.40 g of NH3 and 12.5 g of H2SO4', ['3.40', '12.5'], ['NH3', 'H2SO4', '(NH4)2SO4'], [], 'g (NH4)2SO4', {0: (lambda: min(lim({'NH3': mol('3.40', 'NH3'), 'H2SO4': mol('12.5', 'H2SO4')}, '(NH4)2SO4')[1].values()) * MM('(NH4)2SO4'), 'NH3 limits'), 1: (lambda: max(lim({'NH3': mol('3.40', 'NH3'), 'H2SO4': mol('12.5', 'H2SO4')}, '(NH4)2SO4')[1].values()) * MM('(NH4)2SO4'), 'used excess H2SO4'), 2: (lambda: mol('3.40', 'NH3') * MM('(NH4)2SO4'), 'skipped ratio'), 3: (lambda: ('raw', addsub('3.40', '12.5') + ' g (NH4)2SO4'), 'added masses')}),
 ('5.75 g of Na and 8.15 g of Cl2', ['5.75', '8.15'], ['Na', 'Cl2'], [], 'g Na', {0: (lambda: ('raw', left('5.75', mol('8.15', 'Cl2') * R('Cl2', 'Na') * MM('Na'), 3)[0] + ' g Na'), 'present - used'), 1: (lambda: mol('8.15', 'Cl2') * R('Cl2', 'Na') * MM('Na'), 'amount used'), 2: (lambda: ('raw', addsub('8.15', '5.75', -1) + ' g'), 'subtracted masses'), 3: (lambda: ('raw', left('5.75', mol('8.15', 'Cl2') * MM('Na'), 3)[0] + ' g Na'), '1:1 ratio for Na')}),
 ('1.50 mol CH4 and 2.40 mol O2', ['1.50', '2.40'], [], [], 'mol CO2', {0: (lambda: min(lim({'CH4': g('1.50'), 'O2': g('2.40')}, 'CO2')[1].values()), 'O2 limits'), 1: (lambda: max(lim({'CH4': g('1.50'), 'O2': g('2.40')}, 'CO2')[1].values()), 'used excess CH4'), 2: (lambda: sum(lim({'CH4': g('1.50'), 'O2': g('2.40')}, 'CO2')[1].values()), 'added'), 3: (lambda: g('2.40') * R('CO2', 'O2'), 'flipped')}),
 ('5.40 g of Al and 18.0 g of Fe2O3', ['5.40', '18.0'], ['Al', 'Fe2O3', 'Fe'], [], 'g Fe', {0: (lambda: min(lim({'Al': mol('5.40', 'Al'), 'Fe2O3': mol('18.0', 'Fe2O3')}, 'Fe')[1].values()) * MM('Fe'), 'Al limits'), 1: (lambda: max(lim({'Al': mol('5.40', 'Al'), 'Fe2O3': mol('18.0', 'Fe2O3')}, 'Fe')[1].values()) * MM('Fe'), 'used excess Fe2O3'), 2: (lambda: mol('18.0', 'Fe2O3') * MM('Fe'), 'skipped ratio'), 3: (lambda: ('raw', addsub('5.40', '18.0') + ' g Fe'), 'added masses')}),
 ('2.60 mol N2 and 6.30 mol H2', ['2.60', '6.30'], [], [], 'mol N2', {0: (lambda: ('raw', left('2.60', g('6.30') * R('H2', 'N2'), 3)[0] + ' mol N2'), 'present - used'), 1: (lambda: g('6.30') * R('H2', 'N2'), 'amount used'), 2: (lambda: ('raw', addsub('6.30', '2.60', -1) + ' mol'), 'subtracted reactants'), 3: (lambda: ('raw', 'None; both are used up'), 'no leftover')}),
 ('0.180 mol Zn and 0.300 mol HCl', ['0.180', '0.300'], [], [], 'mol H2', {0: (lambda: min(lim({'Zn': g('0.180'), 'HCl': g('0.300')}, 'H2')[1].values()), 'HCl limits'), 1: (lambda: max(lim({'Zn': g('0.180'), 'HCl': g('0.300')}, 'H2')[1].values()), 'used excess Zn'), 2: (lambda: g('0.300'), 'skipped ratio'), 3: (lambda: g('0.180') * R('H2', 'HCl'), '2:1 for Zn')}),
 # ---- ch08-yield ----
 ('theoretical yield of 18.6 g', ['18.6', '15.9'], [], [], '%', {0: (lambda: g('15.9') / g('18.6'), 'actual/theoretical'), 1: (lambda: g('18.6') / g('15.9'), 'inverted'), 2: (lambda: 1 - g('15.9') / g('18.6'), 'percent lost'), 3: (lambda: ('raw', addsub('18.6', '15.9', -1) + '%'), 'gram difference')}),
 ('Burning 1.20 g of Mg', ['1.20', '1.79'], ['Mg', 'MgO'], [], '%', {0: (lambda: g('1.79') / (mol('1.20', 'Mg') * R('Mg', 'MgO') * MM('MgO')), 'actual/theoretical'), 1: (lambda: mol('1.20', 'Mg') * R('Mg', 'MgO') * MM('MgO') / g('1.79'), 'inverted'), 2: (lambda: g('1.79') / g('1.20'), 'vs reactant mass'), 3: (lambda: g('1.79') / (mol('1.20', 'Mg') * R('Mg', 'MgO') * C('MgO') * MM('MgO')), 'coefficient in molar mass')}),
 ('from 1.38 g of salicylic acid', ['1.38'], ['C7H6O3', 'C9H8O4'], [], 'g C9H8O4', {0: (lambda: mol('1.38', 'C7H6O3') * R('C7H6O3', 'C9H8O4') * MM('C9H8O4'), 'road map'), 1: (lambda: g('1.38'), 'equal mass'), 2: (lambda: g('1.38') * MM('C7H6O3') / MM('C9H8O4'), 'molar masses flipped'), 3: (lambda: mol('1.38', 'C7H6O3') * R('C7H6O3', 'C9H8O4'), 'stopped at moles', 'mol C9H8O4')}),
 ('mixes 2.76 g of salicylic acid', ['2.76', '3.06', '2.95'], ['C7H6O3', 'C4H6O3', 'C9H8O4'], [], '%', {0: (lambda: g('2.95') / (min(lim({'C7H6O3': mol('2.76', 'C7H6O3'), 'C4H6O3': mol('3.06', 'C4H6O3')}, 'C9H8O4')[1].values()) * MM('C9H8O4')), 'limiting reactant'), 1: (lambda: g('2.95') / (max(lim({'C7H6O3': mol('2.76', 'C7H6O3'), 'C4H6O3': mol('3.06', 'C4H6O3')}, 'C9H8O4')[1].values()) * MM('C9H8O4')), 'excess reactant'), 2: (lambda: min(lim({'C7H6O3': mol('2.76', 'C7H6O3'), 'C4H6O3': mol('3.06', 'C4H6O3')}, 'C9H8O4')[1].values()) * MM('C9H8O4') / g('2.95'), 'inverted'), 3: (lambda: g('2.95') / g('2.76'), 'vs reactant mass')}),
 ('theoretical yield of 42.5 g', ['42.5', '76.0'], [], [], 'g', {0: (lambda: g('42.5') * g('76.0') / 100, 'x 0.760'), 1: (lambda: g('42.5') / (g('76.0') / 100), 'divided'), 2: (lambda: g('42.5') * g('76.0'), 'forgot /100'), 3: (lambda: g('42.5') * (1 - g('76.0') / 100), 'mass lost')}),
 ('From 64.0 g of glucose', ['64.0', '82.0'], ['C6H12O6', 'C2H5OH'], [], 'g C2H5OH', {0: (lambda: mol('64.0', 'C6H12O6') * R('C6H12O6', 'C2H5OH') * MM('C2H5OH') * g('82.0') / 100, 'theoretical x yield'), 1: (lambda: mol('64.0', 'C6H12O6') * R('C6H12O6', 'C2H5OH') * MM('C2H5OH'), 'theoretical only'), 2: (lambda: mol('64.0', 'C6H12O6') * R('C6H12O6', 'C2H5OH') * MM('C2H5OH') / (g('82.0') / 100), 'divided'), 3: (lambda: mol('64.0', 'C6H12O6') * MM('C2H5OH') * g('82.0') / 100, 'skipped ratio')}),
 ('starts with 0.825 g of Al', ['0.825', '12.9'], ['Al', 'KAl(SO4)2.12H2O'], [], '%', {0: (lambda: g('12.9') / (mol('0.825', 'Al') * MM('KAl(SO4)2.12H2O')), 'hydrate molar mass'), 1: (lambda: mol('0.825', 'Al') * MM('KAl(SO4)2.12H2O') / g('12.9'), 'inverted'), 2: (lambda: g('12.9') / (mol('0.825', 'Al') * MM('KAl(SO4)2')), 'left out the waters'), 3: (lambda: ('raw', fmt(g('12.9') / (mol('0.825', 'Al') * MM('KAl(SO4)2.12H2O')), 3) + '%'), 'forgot x100')}),
 ('theoretical yield is 6.48 g', ['6.48', '5.62'], [], [], '%', {0: (lambda: g('5.62') / g('6.48'), 'actual/theoretical'), 1: (lambda: g('6.48') / g('5.62'), 'inverted'), 2: (lambda: 1 - g('5.62') / g('6.48'), 'percent lost'), 3: (lambda: ('raw', fmt(g('5.62') / g('6.48'), 3) + '%'), 'forgot x100')}),
 ('5.60 g of N2 reacts with excess', ['5.60', '5.95'], ['N2', 'NH3'], [], '%', {0: (lambda: g('5.95') / (mol('5.60', 'N2') * R('N2', 'NH3') * MM('NH3')), 'actual/theoretical'), 1: (lambda: mol('5.60', 'N2') * R('N2', 'NH3') * MM('NH3') / g('5.95'), 'inverted'), 2: (lambda: g('5.95') / (mol('5.60', 'N2') * MM('NH3')), 'skipped ratio'), 3: (lambda: g('5.95') / g('5.60'), 'vs reactant mass')}),
 ('25.0 g of CaCO3 gives a 91.5% yield', ['25.0', '91.5'], ['CaCO3', 'CaO'], [], 'g CaO', {0: (lambda: mol('25.0', 'CaCO3') * R('CaCO3', 'CaO') * MM('CaO') * g('91.5') / 100, 'theoretical x yield'), 1: (lambda: mol('25.0', 'CaCO3') * R('CaCO3', 'CaO') * MM('CaO'), 'theoretical only'), 2: (lambda: mol('25.0', 'CaCO3') * R('CaCO3', 'CaO') * MM('CaO') / (g('91.5') / 100), 'divided'), 3: (lambda: g('25.0') * g('91.5') / 100, 'yield on reactant mass')}),
 ('4.50 g of Fe and 3.20 g of S', ['4.50', '3.20', '6.25'], ['Fe', 'S', 'FeS'], [], '%', {0: (lambda: g('6.25') / (min(lim({'Fe': mol('4.50', 'Fe'), 'S': mol('3.20', 'S')}, 'FeS')[1].values()) * MM('FeS')), 'limiting reactant'), 1: (lambda: g('6.25') / (max(lim({'Fe': mol('4.50', 'Fe'), 'S': mol('3.20', 'S')}, 'FeS')[1].values()) * MM('FeS')), 'excess reactant'), 2: (lambda: min(lim({'Fe': mol('4.50', 'Fe'), 'S': mol('3.20', 'S')}, 'FeS')[1].values()) * MM('FeS') / g('6.25'), 'inverted'), 3: (lambda: g('6.25') / D(addsub('4.50', '3.20')), 'vs total reactant mass')}),
 ('Step 1 has an 85.0% yield', ['85.0', '72.0'], [], [], '%', {0: (lambda: g('85.0') * g('72.0') / 10000, 'product'), 1: (lambda: (g('85.0') + g('72.0')) / 200, 'average'), 2: (lambda: (g('85.0') + g('72.0')) / 100, 'added'), 3: (lambda: ('raw', addsub('85.0', '72.0', -1) + '%'), 'difference')}),
 # ---- ch08-enthalpy ----
 ('when 1.35 mol of O2 reacts', ['1.35', '571.6'], [], [], 'kJ released', {0: (lambda: g('1.35') * DHmag() / C('O2'), 'per mol O2'), 1: (lambda: g('1.35') * DHmag() / C('H2'), 'used H2 coefficient'), 2: (lambda: g('1.35') * DHmag() * C('H2') / C('O2'), 'doubled'), 3: (lambda: g('1.35') * DHmag() / C('O2'), 'wrong sign', 'kJ absorbed')}),
 ('when 5.00 g of propane burns', ['5.00', '2.220e3'], ['C3H8'], [], 'kJ released', {0: (lambda: mol('5.00', 'C3H8') * DHmag() / C('C3H8'), 'g -> mol -> kJ'), 1: (lambda: g('5.00') * DHmag(), 'grams x dH'), 2: (lambda: mol('5.00', 'C3H8') * DHmag() / C('O2'), 'used O2 coefficient'), 3: (lambda: mol('5.00', 'C3H8') * DHmag() / C('C3H8'), 'wrong sign', 'kJ absorbed')}),
 ('release 3.60 x 10^4 kJ', ['3.60e4', '890.3'], ['CH4'], [], 'g CH4', {0: (lambda: g('3.60e4') / DHmag() * C('CH4') * MM('CH4'), 'kJ -> mol -> g'), 1: (lambda: g('3.60e4') / DHmag() * C('CH4'), 'stopped at moles', 'mol CH4'), 2: (lambda: g('3.60e4') / DHmag() * C('CH4') / MM('CH4'), 'divided by molar mass'), 3: (lambda: g('3.60e4') / DHmag() / C('O2') * MM('CH4'), 'used O2 coefficient')}),
 ('released by 5.40 g of glucose', ['5.40', '2803'], ['C6H12O6'], ['4.184'], 'kJ released', {0: (lambda: mol('5.40', 'C6H12O6') * DHmag(), 'g -> mol -> kJ'), 1: (lambda: g('5.40') * DHmag(), 'grams x dH'), 2: (lambda: mol('5.40', 'C6H12O6') * DHmag() / C('O2'), 'used O2 coefficient'), 3: (lambda: mol('5.40', 'C6H12O6') * DHmag() / g('4.184'), 'kcal labeled kJ')}),
 ('does 12.0 g of glucose release', ['12.0', '2803', '4.184'], ['C6H12O6'], [], 'Cal', {0: (lambda: mol('12.0', 'C6H12O6') * DHmag() / g('4.184'), 'kJ / 4.184'), 1: (lambda: mol('12.0', 'C6H12O6') * DHmag(), 'kJ labeled Cal'), 2: (lambda: mol('12.0', 'C6H12O6') * DHmag() * g('4.184'), 'multiplied by 4.184'), 3: (lambda: mol('12.0', 'C6H12O6') * DHmag() / g('4.184') / C('O2'), 'used O2 coefficient')}),
 ('decompose 35.0 g of CaCO3', ['35.0', '178'], ['CaCO3'], [], 'kJ absorbed', {0: (lambda: mol('35.0', 'CaCO3') * DHmag(), 'g -> mol -> kJ'), 1: (lambda: mol('35.0', 'CaCO3') * DHmag(), 'wrong sign', 'kJ released'), 2: (lambda: g('35.0') * DHmag(), 'grams x dH'), 3: (lambda: mol('35.0', 'CaCO3'), 'stopped at moles', 'mol CaCO3')}),
 ('when 2.75 mol of O2 is used', ['2.75', '890.3'], [], [], 'kJ released', {0: (lambda: g('2.75') * DHmag() / C('O2'), 'per 2 mol O2'), 1: (lambda: g('2.75') * DHmag(), 'ignored coefficient'), 2: (lambda: g('2.75') / DHmag(), 'mol / dH'), 3: (lambda: g('2.75') * DHmag() / C('O2'), 'wrong sign', 'kJ absorbed')}),
 ('release 1.50 x 10^4 kJ', ['1.50e4', '2.220e3'], ['C3H8'], [], 'g C3H8', {0: (lambda: g('1.50e4') / DHmag() * C('C3H8') * MM('C3H8'), 'kJ -> mol -> g'), 1: (lambda: g('1.50e4') / DHmag() * C('C3H8'), 'stopped at moles', 'mol C3H8'), 2: (lambda: g('1.50e4') / DHmag() * C('O2') * MM('C3H8'), 'used O2 coefficient'), 3: (lambda: g('1.50e4') / DHmag() / MM('C3H8'), 'divided by molar mass')}),
 ('released by 18.5 g of H2', ['18.5', '571.6'], ['H2'], [], 'kJ released', {0: (lambda: mol('18.5', 'H2') * DHmag() / C('H2'), 'per 2 mol H2'), 1: (lambda: mol('18.5', 'H2') * DHmag(), 'ignored coefficient'), 2: (lambda: g('18.5') * DHmag() / C('H2'), 'grams for moles'), 3: (lambda: mol('18.5', 'H2') * DHmag() / C('H2'), 'wrong sign', 'kJ absorbed')}),
 ('supplies 25.0 Cal from glucose', ['25.0', '4.184', '2803'], ['C6H12O6'], [], 'g', {0: (lambda: g('25.0') * g('4.184') / DHmag() * MM('C6H12O6'), 'Cal -> kJ -> mol -> g'), 1: (lambda: g('25.0') / DHmag() * MM('C6H12O6'), 'Cal used as kJ'), 2: (lambda: g('25.0') * g('4.184') / DHmag(), 'stopped at moles', 'mol'), 3: (lambda: g('25.0') * g('4.184') / DHmag() * C('O2') * MM('C6H12O6'), 'used O2 coefficient')}),
]
print('Calculation items (givens as written set the sig figs; mole ratios from the stem equation are exact)')
for sub, given, fac, consts, unit, ch in CALC:
    q = by(sub)
    if not q: continue
    checked.add(q['id'])
    stem = txt(q['q']); figtxt = ' '.join(txt(x) for f in q.get('f', []) if f['type'] == 'table' for r in f['rows'] for x in r)
    for gv in given:
        if 'e' in gv:
            m_, e_ = gv.split('e'); pat = re.escape(m_) + r' x 10\^' + re.escape(e_)
        else:
            pat = r'(?<![\d.])' + re.escape(gv) + r'(?![\d])'
        if not re.search(pat, stem) and not re.search(r'(?<![\d.])' + re.escape(gv) + r'(?![\d])', figtxt):
            err.append(q['id'] + ' given %r not in stem as written' % gv)
    eqs = eqs_in(q['q'])
    CUR.clear()
    if eqs:
        e = eqs[0][1]; CUR['coef'] = {f: co for co, f, ph in e[0] + e[1]}
    m = re.search(r'ΔH = ([+-]?[\d.]+(?: x 10\^\d+)?) kJ', stem)
    if m: CUR['dH'] = abs(num_of(m.group(1)))
    n = min([sf(x) for x in given] + [sf(str(MM(f))) for f in fac] + [sf(x) for x in consts] + [9])
    print('  %s %s (%d s.f.)' % (q['id'], sub[:50], n))
    keys = []
    for j, spec in sorted(ch.items()):
        fn, why = spec[0], spec[1]; u = spec[2] if len(spec) > 2 else unit
        try: v = fn()
        except Exception as e_: err.append('%s c[%d] spec failed: %r' % (q['id'], j, e_)); continue
        if isinstance(v, tuple): want = v[1]
        elif u == '%': want = fmt(v * 100, n) + '%'
        else: want = fmt(v, n) + ' ' + u
        keys.append(want)
        ok(txt(q['c'][j]).strip() == want, '%s c[%d] %-26r = %r (%s)' % (q['id'], j, txt(q['c'][j]).strip(), want, why))
    if len(set(keys)) != 4: err.append(q['id'] + ' recomputed values not all different: %s' % keys)
    k0 = keys[0] if keys else ''
    k0n = k0.split(' ')[0].rstrip('%') if not k0.startswith('None') else ''
    if k0n and k0n.split(' x')[0] not in txt(q['w']): err.append(q['id'] + ' answer %s not in w' % k0)
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')
# leftover items: the excess reactant really is the one named, and the leftover is positive
for sub, amts, prod in (('3.40 mol CO and 2.10 mol O2', {'CO': g('3.40'), 'O2': g('2.10')}, 'CO2'),
                        ('2.60 mol N2 and 6.30 mol H2', {'N2': g('2.60'), 'H2': g('6.30')}, 'NH3')):
    q = by(sub); CUR['coef'] = {f: co for co, f, ph in sum(eqs_in(q['q'])[0][1], [])}
    lo, p = lim(amts, prod); ex = [f for f in amts if f != lo][0]
    ok(txt(q['c'][0]).endswith(' mol ' + ex) and D(txt(q['c'][0]).split()[0]) > 0, '%s limiting %s, excess %s left over' % (q['id'], lo, ex))
for sub, gm, prod in (('6.50 g of iron and 4.25 g of sulfur', {'Fe': '6.50', 'S': '4.25'}, 'FeS'), ('5.75 g of Na and 8.15 g of Cl2', {'Na': '5.75', 'Cl2': '8.15'}, 'NaCl')):
    q = by(sub); CUR['coef'] = {f: co for co, f, ph in sum(eqs_in(q['q'])[0][1], [])}
    lo, p = lim({f: mol(v, f) for f, v in gm.items()}, prod); ex = [f for f in gm if f != lo][0]
    ok(txt(q['c'][0]).endswith(' g ' + ex), '%s limiting %s, leftover is %s' % (q['id'], lo, ex))

# ---------- conceptual items with checkable content ----------
print('Conceptual items with numbers, figures, limiting-reactant reasoning, or Delta H scaling')
def setcur(q):
    CUR.clear(); e = eqs_in(q['q'])[0][1]; CUR['coef'] = {f: co for co, f, ph in e[0] + e[1]}
    return e
q = by('react with 1 g of O2'); checked.add(q['id']); setcur(q)
ok(str(C('Mg') * MM('Mg')) in txt(q['c'][0]) and str(MM('O2')) in txt(q['c'][0]), '%s 2 mol Mg = %s g, 1 mol O2 = %s g' % (q['id'], C('Mg') * MM('Mg'), MM('O2')))
q = by('4 mol of reactant molecules make only 2 mol'); checked.add(q['id']); setcur(q)
lhs = C('N2') * MM('N2') + C('H2') * MM('H2'); rhs = C('NH3') * MM('NH3')
ok(lhs == rhs == D('34.062') and txt(q['y'][0]).count('34.062') == 2 and C('N2') + C('H2') == 4 and C('NH3') == 2, '%s mass in %s g = mass out %s g; 4 mol -> 2 mol' % (q['id'], lhs, rhs))
q = by('A student converts 0.3150 mol O2'); checked.add(q['id']); setcur(q)
ok(fmt(D('0.3150') * R('O2', 'CO2'), 4) in txt(q['w']) and sf('0.3150') == 4 and q['c'][0].startswith('4,'), '%s 0.3150 x 16/25 = %s, 4 s.f.' % (q['id'], fmt(D('0.3150') * R('O2', 'CO2'), 4)))
q = by('from 5.5 g of H2 with'); checked.add(q['id']); setcur(q)
ok(fmt(mol('5.5', 'H2') * R('H2', 'H2O') * MM('H2O'), 2) + ' g' in txt(q['w']) and fmt(mol('5.5', 'H2'), 3) + ' mol' in txt(q['y'][0]), '%s correct mass %s g H2O' % (q['id'], fmt(mol('5.5', 'H2') * R('H2', 'H2O') * MM('H2O'), 2)))
q = by('in 25.0 mL of 0.150 M NaOH as'); checked.add(q['id'])
ok(fmt(D('25.0') * D('0.150'), 3) == '3.75' and fmt(D('25.0') / 1000 * D('0.150'), 3) in txt(q['c'][0]), '%s 25.0 x 0.150 = 3.75; correct %s mol' % (q['id'], fmt(D('25.0') / 1000 * D('0.150'), 3)))
q = by('6.20 g of Na and 7.10 g of Cl2'); checked.add(q['id']); setcur(q)
lo, p = lim({'Na': mol('6.20', 'Na'), 'Cl2': mol('7.10', 'Cl2')}, 'NaCl')
ok(lo == 'Cl2' and txt(q['c'][0]).startswith('Cl2') and fmt(p['Na'], 4) in txt(q['y'][0]) and fmt(p['Cl2'], 4) in txt(q['y'][0]) and D('7.10') > D('6.20'),
   '%s limiting %s (NaCl %s vs %s), the larger mass' % (q['id'], lo, fmt(p['Na'], 4), fmt(p['Cl2'], 4)))
q = by('The box shows the molecules before'); checked.add(q['id']); setcur(q)
cnt = collections.Counter(''.join(m_) for m_ in q['f'][0]['boxes'][0]['mols'])
lo, p = lim({'N2': D(cnt['NN']), 'H2': D(cnt['HH'])}, 'NH3')
ok(lo == 'H2' and txt(q['c'][0]) == '%d NH3 molecules; H2 is limiting' % p['H2'] and txt(q['c'][1]).startswith('%d NH3' % p['N2']) and txt(q['c'][2]).startswith('%d NH3' % cnt['NN']) and txt(q['c'][3]).startswith('%d NH3' % (cnt['NN'] + cnt['HH'])),
   '%s figure %d N2 + %d H2 -> %s NH3 (limiting %s)' % (q['id'], cnt['NN'], cnt['HH'], p['H2'], lo))
q = by('has 3.4 mol of H2 and 2.0 mol of O2'); checked.add(q['id']); setcur(q)
lo, p = lim({'H2': D('3.4'), 'O2': D('2.0')}, 'H2O'); ok(lo == 'H2' and 'H2 is limiting' in txt(q['c'][0]), '%s limiting %s (%s vs %s mol H2O)' % (q['id'], lo, p['H2'], p['O2']))
q = by('which mixture in the table'); checked.add(q['id']); setcur(q)
exact = [r[0] for r in q['f'][0]['rows'] if D(r[1]) * R('SO2', 'O2') == D(r[2])]
ok(exact == ['B'] and q['c'][0] == 'Mixture B', '%s only mixture %s is in the 2:1 ratio' % (q['id'], exact))
q = by('thin oxide layer that protects aluminum'); setcur(q)
ok(all(D(r[1]) * R('Al', 'O2') == D(r[2]) for r in q['f'][0]['rows'][:2]), '%s table rows follow 4:3' % q['id'])
q = by('road map for 30.0 g of glucose'); setcur(q); r_ = q['f'][0]['rows']
ok(r_[0][1] == '30.0' and txt(r_[1][1]) == fmt(mol('30.0', 'C6H12O6'), 4) and txt(r_[2][1]) == fmt(mol('30.0', 'C6H12O6') * R('C6H12O6', 'CO2'), 4) and str(MM('C6H12O6')) in txt(r_[1][0]) and str(MM('CO2')) in txt(r_[3][0]), '%s table steps' % q['id'])
q = by('0.40 mol Fe2O3 and 0.90 mol CO'); checked.add(q['id']); setcur(q)
lo, p = lim({'Fe2O3': D('0.40'), 'CO': D('0.90')}, 'Fe'); ok(lo == 'CO' and fmt(p['CO'], 2) in txt(q['c'][0]) and D('0.40') * R('Fe2O3', 'CO') == D('1.20'), '%s limiting %s (Fe %s vs %s)' % (q['id'], lo, p['Fe2O3'], p['CO']))
q = by('6 CO molecules and 2 O2 molecules'); checked.add(q['id']); setcur(q)
lo, p = lim({'CO': D(6), 'O2': D(2)}, 'CO2'); usedCO = p[lo] * R('CO2', 'CO')
ok(lo == 'O2' and txt(q['c'][0]) == '%d CO2 and %d CO' % (p[lo], 6 - usedCO), '%s %s CO2, %s CO left' % (q['id'], p[lo], 6 - usedCO))
for sub, base_sign in (('What is ΔH for the reverse reaction', -1), ('what is ΔH for 4 H2', 1), ('What is ΔH for photosynthesis', -1)):
    q = by(sub); checked.add(q['id'])
    E = eqs_in(q['q']); dh1 = expected_dH(E[0][1]); dh2 = expected_dH(E[1][1])
    val = lambda c: num_of(txt(c).replace(' kJ', ''))
    ok(val(q['c'][0]) == dh2 and val(q['c'][1]) != dh2, '%s key %s kJ = recomputed %s (from %s)' % (q['id'], txt(q['c'][0]), dh2, dh1))
    alt = {val(q['c'][j]) for j in (1, 2, 3)}
    ok(dh2 not in alt and (dh1 in alt or -dh2 in alt), '%s distractors include the unscaled/unsigned value' % q['id'])
q = by('A student measures the density of copper'); hand.add(q['id'])

# ---------- course rule: trailing zeros in calculation stems ----------
print('Trailing-zero rule in calculation stems; every k=1 item recomputed')
for q in ALL:
    if q['k'] == 1:
        s = re.sub(r'<sub>\d+</sub>', '', q['q']); s = re.sub(r'&middot;\d+', '', s); s = txt(s)
        for m in re.finditer(r'(?<![\d.^])(\d*[1-9]\d*0)(?![\d.^])', s):
            err.append(q['id'] + ' calculation stem has ambiguous trailing-zero value %r' % m.group(1))
        if q['id'] not in checked: err.append(q['id'] + ' calculation item not recomputed')
for q in ALL:
    if q['id'] not in checked: hand.add(q['id'])

# ---------- draft overlap ----------
print('Draft overlap: no stem reuses a worked example or exercise from drafts/ch08 (same equation and a shared given)')
GIV = r'(\d+\.\d+|\d+\.|\d+)(?: x 10\^(-?\d+))? (?:g|mol|mL|L|M|kJ|kg|mg)\b(?!/)'
CONST = {D('890.3'), D('2803'), D('571.6'), D('2220'), D('178'), D('4.184'), D('22.4'), D('1143.2')}
def givens_in(t):
    """measured givens only: numbers with a decimal point (exact counts such as '2 mol' and the standard
    Delta H values and constants are not givens)."""
    out = set()
    for a, b in re.findall(GIV, t):
        v = D(a) * (D(10) ** int(b) if b else 1)
        if '.' in a and v not in CONST: out.add(v)
    return out
blocks = []; notes = []
for p_ in sorted(glob.glob(os.path.join(ROOT, 'drafts', 'ch08', '*.html'))):
    h = open(p_, encoding='utf-8').read()
    for b in re.split(r'(?=Example \\\(\\PageIndex|Exercise \\\(\\PageIndex|<h2)', h):
        t = txt(re.sub(r'\\\(|\\\)|\\dfrac|\\text|\\times|\\ |[{}]', ' ', b))
        es = set()
        for s_, e in eqs_in(b):
            es.add(frozenset(eqvec(e).items()))
        blocks.append((os.path.basename(p_), es, givens_in(t)))
nover = 0
for q in ALL:
    qe = {frozenset(eqvec(e).items()) for s_, e in eqs_in(q['q'])}
    qg = givens_in(txt(q['q']))
    for nm, es, gs in blocks:
        if qe & es and qg & gs:
            msg = '%s shares an equation and given(s) %s with a block of %s' % (q['id'], [str(x) for x in sorted(qg & gs)], nm)
            # sections 8.0-8.6 (teaching text, worked examples, exercises) are errors; the chapter guide, practice
            # problems and games pages (8.7+) are written separately and only reported
            if re.match(r'8\.[0-6]_', nm): nover += 1; err.append(msg)
            else: notes.append(msg)
print('    %d draft blocks compared; %d overlaps with sections 8.0-8.6' % (len(blocks), nover))
for n_ in notes: print('    NOTE', n_)

# ---------- coverage, counts, duplicates ----------
print('Items with a machine check: %d of %d' % (len(checked), len(ALL)))
print('  conceptual (key read by hand; equations and quoted values still checked):', ' '.join(sorted(hand)))
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
