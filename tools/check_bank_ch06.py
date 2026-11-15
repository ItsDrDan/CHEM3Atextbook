#!/usr/bin/env python3
"""Checker for the Chapter 6 banks (ionic bonding, Lewis structures, VSEPR, polarity, percent composition,
empirical and molecular formulas). Structural checks as in tools/check_bank_ch05.py (ch06 topic ids), plus, written
independently of the generators:
  - a table of Lewis structures (atoms, lone pairs, bonds) for every molecule used; each is verified by electron
    arithmetic (valence electrons from group numbers and the charge = 2 x bonding pairs + 2 x lone pairs; every atom
    an octet, H a duet; atoms match the formula);
  - valence-electron totals (with charge) and the intended errors (charge ignored or reversed, subscript dropped,
    octet count, atomic numbers);
  - per-choice Lewis structures for "which structure is correct" items: only the key uses the right number of
    electrons and gives every atom an octet (duet);
  - bonding/lone-pair counts, electron groups, VSEPR shape and angle from the rule table (up to 4 groups);
  - dEN from the yellow-sheet electronegativities, bond class (0-0.4 nonpolar, >0.4-2.0 polar, >2.0 ionic),
    partial charges and dipole direction; molecular polarity from a rule table (no polar bonds, or symmetrical with no
    lone pairs on the centre and identical outer atoms -> nonpolar; otherwise polar);
  - ionic items: electrons lost/gained from group numbers, formulas that balance them, salt/base/oxide classes;
  - percent composition from the formula (yellow-sheet masses, Decimal, addition rule, 4 s.f. as in Section 6.6) or
    from lab masses (subtraction and division sig-fig rules), with every distractor's intended error;
  - empirical formulas from masses/percents (moles, divide by smallest, smallest multiplier 1-6 within 0.1),
    molecular formulas from n = M / empirical mass, hydrate water counts;
  - quoted electronegativities and atomic masses, dEN subtractions, and every "a / b = c" in the text;
  - exactly one correct choice per checked item (key correct, each distractor not correct).
usage: python3 tools/check_bank_ch06.py bank/ch06.json bank/ch06_adapt.json"""
import json, sys, re, os, collections, math
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 50; getcontext().rounding = ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
YS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yellow_sheet_masses.json')))
AM = YS['masses']; ENV = {k: D(v) for k, v in YS['electronegativity'].items()}
TOP = {'ch06-ionic', 'ch06-lewis', 'ch06-vsepr', 'ch06-polarity', 'ch06-percent', 'ch06-empirical'}
err = []

# ---------- structural checks ----------
OUT_OF_SCOPE = r'resonance|formal charge|expanded octet|hybridi[sz]|\bsp[23]\b|seesaw|octahedral|bipyramid|square planar|T-shaped|molecular orbital|limiting reactant|molarity'
def plain(x): return re.sub(r'<[^>]+>', '', x).strip().lower()
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
        if q['t'] in ('ch06-percent', 'ch06-empirical') and re.search(r'\d', q['q']) and re.search(r'\d+\.\d+ ?(g|%)', q['q']) and q['k'] != 1:
            err.append(i + ' calculation item without k=1')
        if re.search(r'all of the above|none of the above', json.dumps(q), re.I): err.append(i + ' AOTA/NOTA')
        s = ' '.join([q['q'], q['h'], q['w']] + q['c'] + q['y'])
        for tg in ('sub', 'sup', 'b', 'i'):
            if len(re.findall('<%s>' % tg, s)) != len(re.findall('</%s>' % tg, s)): err.append(i + ' unbalanced <%s>' % tg)
        if re.search(r'&(?!(?:[a-zA-Z]+|#\d+);)', s): err.append(i + ' bare &')
        if '{' in s or '}' in s: err.append(i + ' unconverted {formula}')
        if 'f' in q and not allow_f: err.append(i + ' has f (ADAPT items must be text only)')
        for f in q.get('f', []):
            if f['type'] != 'table': err.append(i + ' figure type not used/checked here: ' + f['type'])
            elif max(len(f['head']), *[len(r) for r in f['rows']]) > 3: err.append(i + ' table wider than 3 columns')
        if re.search(OUT_OF_SCOPE, s, re.I): err.append(i + ' out of scope term')
        if label == 'HW' and not q['y'][0].startswith('Correct: '): err.append(i + ' ADAPT y[0] lacks "Correct: "')
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if right in plain(q['y'][j]): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c6-%03d', 'TRY', True)
structural(HW, 'c6-h%02d', 'HW', False)
ALL = TRY + HW

def txt(x):
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = x.replace('&middot;', '.')
    x = re.sub(r'<[^>]+>', '', x)
    return (x.replace('&minus;', '-').replace('−', '-').replace('&times;', 'x').replace('&nbsp;', ' ')
             .replace('&divide;', '/').replace('&rarr;', '->').replace('&ldquo;', '"').replace('&rdquo;', '"')
             .replace('&ndash;', '–').replace('&equiv;', '≡').replace('&deg;', '°').replace('&Delta;', 'Δ')
             .replace('&delta;', 'δ').replace('&lt;', '<').replace('&gt;', '>'))
def by(sub):
    m = [q for q in ALL if sub in q['q'] or sub in txt(q['q'])]
    if len(m) != 1: sys.exit('lookup %r matched %d items' % (sub, len(m)))
    return m[0]
def ok(cond, msg):
    print('   ', 'OK ' if cond else 'BAD', msg)
    if not cond: err.append(msg)
checked = set()
C = lambda q, j: txt(q['c'][j]).strip()

# ---------- chemistry from first principles ----------
ORDER = ('H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn '
         'Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I').split()
ZN = {s: i + 1 for i, s in enumerate(ORDER)}
VAL = {'H': 1, 'Li': 1, 'Na': 1, 'K': 1, 'Mg': 2, 'Ca': 2, 'Zn': 2, 'Al': 3, 'C': 4, 'Si': 4, 'N': 5, 'P': 5,
       'O': 6, 'S': 6, 'F': 7, 'Cl': 7, 'Br': 7, 'I': 7}
METALS = {'Li', 'Na', 'K', 'Mg', 'Ca', 'Al', 'Zn', 'Fe', 'Cu', 'Sn', 'Ni'}
def atoms(f):
    def grp(s, i):
        c = collections.Counter()
        while i < len(s) and s[i] != ')':
            if s[i] == '(':
                inner, i = grp(s, i + 1); i += 1
                m = re.match(r'\d*', s[i:]); k = int(m.group() or 1); i += m.end()
                for e in inner: c[e] += inner[e] * k
            else:
                m = re.match(r'([A-Z][a-z]?)(\d*)', s[i:])
                if not m: raise ValueError('bad formula %r at %d' % (s, i))
                c[m.group(1)] += int(m.group(2) or 1); i += m.end()
        return c, i
    total = collections.Counter()
    for k, piece in enumerate(f.split('.')):
        m = re.match(r'(\d*)(.+)', piece); mult = int(m.group(1) or 1) if k else 1
        c, _ = grp(m.group(2), 0)
        for e in c: total[e] += c[e] * mult
    return total
def places(s): return len(s.partition('.')[2])
def MMraw(f): return sum((D(AM[e]) * n for e, n in atoms(f).items()), D(0))
def MM(f): return MMraw(f).quantize(D(10) ** -min(places(AM[e]) for e in atoms(f)))
def sf(s):
    s = s.strip()
    digits = s.replace('.', '').lstrip('0')
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
def VE(f, ch=0): return sum(VAL[e] * n for e, n in atoms(f).items()) - ch

# ---------- Lewis-structure table (derived by hand; verified below) ----------
# name: (formula, charge, atoms, lone pairs per atom, bonds "i-j" / "i=j" / "i#j", central atom index or None)
LEW = {
 'H2O': ('H2O', 0, 'O H H', '2 0 0', '0-1 0-2', 0),
 'NH3': ('NH3', 0, 'N H H H', '1 0 0 0', '0-1 0-2 0-3', 0),
 'CH4': ('CH4', 0, 'C H H H H', '0 0 0 0 0', '0-1 0-2 0-3 0-4', 0),
 'CO2': ('CO2', 0, 'C O O', '0 2 2', '0=1 0=2', 0),
 'CS2': ('CS2', 0, 'C S S', '0 2 2', '0=1 0=2', 0),
 'CH2O': ('CH2O', 0, 'C H H O', '0 0 0 2', '0-1 0-2 0=3', 0),
 'O3': ('O3', 0, 'O O O', '1 2 3', '0=1 0-2', 0),
 'SO2': ('SO2', 0, 'S O O', '1 2 3', '0=1 0-2', 0),
 'PCl3': ('PCl3', 0, 'P Cl Cl Cl', '1 3 3 3', '0-1 0-2 0-3', 0),
 'PH3': ('PH3', 0, 'P H H H', '1 0 0 0', '0-1 0-2 0-3', 0),
 'NF3': ('NF3', 0, 'N F F F', '1 3 3 3', '0-1 0-2 0-3', 0),
 'CCl4': ('CCl4', 0, 'C Cl Cl Cl Cl', '0 3 3 3 3', '0-1 0-2 0-3 0-4', 0),
 'CF4': ('CF4', 0, 'C F F F F', '0 3 3 3 3', '0-1 0-2 0-3 0-4', 0),
 'CH3Cl': ('CH3Cl', 0, 'C H H H Cl', '0 0 0 0 3', '0-1 0-2 0-3 0-4', 0),
 'CH2Cl2': ('CH2Cl2', 0, 'C H H Cl Cl', '0 0 0 3 3', '0-1 0-2 0-3 0-4', 0),
 'CH2F2': ('CH2F2', 0, 'C H H F F', '0 0 0 3 3', '0-1 0-2 0-3 0-4', 0),
 'CHCl3': ('CHCl3', 0, 'C H Cl Cl Cl', '0 0 3 3 3', '0-1 0-2 0-3 0-4', 0),
 'SCl2': ('SCl2', 0, 'S Cl Cl', '2 3 3', '0-1 0-2', 0),
 'OF2': ('OF2', 0, 'O F F', '2 3 3', '0-1 0-2', 0),
 'H3O+': ('H3O', 1, 'O H H H', '1 0 0 0', '0-1 0-2 0-3', 0),
 'NH4+': ('NH4', 1, 'N H H H H', '0 0 0 0 0', '0-1 0-2 0-3 0-4', 0),
 'HF': ('HF', 0, 'H F', '0 3', '0-1', None),
 'N2': ('N2', 0, 'N N', '1 1', '0#1', None),
 'O2': ('O2', 0, 'O O', '2 2', '0=1', None),
 'Cl2': ('Cl2', 0, 'Cl Cl', '3 3', '0-1', None),
 'CO': ('CO', 0, 'C O', '1 1', '0#1', None),
 'C2H2': ('C2H2', 0, 'C C H H', '0 0 0 0', '0#1 0-2 1-3', None),
 'C2H4': ('C2H4', 0, 'C C H H H H', '0 0 0 0 0 0', '0=1 0-2 0-3 1-4 1-5', None),
 'CH3OH': ('CH3OH', 0, 'C O H H H H', '0 2 0 0 0 0', '0-1 0-2 0-3 0-4 1-5', None),
 'H2O2': ('H2O2', 0, 'O O H H', '2 2 0 0', '0-1 0-2 1-3', None),
 'COCl2': ('COCl2', 0, 'C O Cl Cl', '0 2 3 3', '0=1 0-2 0-3', 0),
}
def mk(at, lp, bd):
    at = at.split(); lp = [int(x) for x in lp.split()]
    bonds = [(int(a), int(b), {'-': 1, '=': 2, '#': 3}[o]) for a, o, b in (re.match(r'(\d+)([-=#])(\d+)', x).groups() for x in bd.split())]
    return at, lp, bonds
def electrons(at, lp, bonds): return 2 * sum(lp) + 2 * sum(o for a, b, o in bonds)
def around(at, lp, bonds, i): return 2 * lp[i] + 2 * sum(o for a, b, o in bonds if i in (a, b))
def octets_ok(at, lp, bonds): return all(around(at, lp, bonds, i) == (2 if e == 'H' else 8) for i, e in enumerate(at))
def valid(formula, ch, at, lp, bonds):
    return (collections.Counter(at) == atoms(formula) and electrons(at, lp, bonds) == VE(formula, ch) and octets_ok(at, lp, bonds))
S = {}
print('Lewis-structure table: electron count = valence electrons (with charge); octets (H duets); atoms match formula')
for name, (f, ch, a, l, b, cen) in LEW.items():
    at, lp, bonds = mk(a, l, b); S[name] = (at, lp, bonds, cen, f, ch)
    good = valid(f, ch, at, lp, bonds)
    if not good: err.append('Lewis table entry %s fails electron/octet check' % name)
print('    %d structures; all pass: %s' % (len(LEW), all(valid(v[4], v[5], *v[:3]) for v in S.values())))
def bp(m): return sum(o for a, b, o in S[m][2])
def lps(m): return sum(S[m][1])
def neighbors(m, i): return [b if a == i else a for a, b, o in S[m][2] if i in (a, b)]
def groups(m, i=None):
    i = S[m][3] if i is None else i
    return len(neighbors(m, i)) + S[m][1][i]
SHAPE = {(2, 0): ('linear', '180'), (3, 0): ('trigonal planar', '120'), (3, 1): ('bent', '120'),
         (4, 0): ('tetrahedral', '109.5'), (4, 1): ('trigonal pyramidal', '109.5'), (4, 2): ('bent', '109.5')}
EGEOM = {2: 'linear', 3: 'trigonal planar', 4: 'tetrahedral'}
def shape(m, i=None):
    i = S[m][3] if i is None else i
    return SHAPE[(groups(m, i), S[m][1][i])]
def dEN(a, b): return abs(ENV[a] - ENV[b])
def bclass(x):
    x = D(x)
    return 'nonpolar covalent' if x <= D('0.4') else ('polar covalent' if x <= 2 else 'ionic')
def polar(m):
    at, lp, bonds, cen, f, ch = S[m]
    if cen is None:
        assert len(at) == 2, m
        return dEN(at[0], at[1]) > D('0.4')
    outer = [at[j] for j in neighbors(m, cen)]
    if not any(dEN(at[cen], e) > D('0.4') for e in outer): return False
    if lp[cen] == 0 and len(set(outer)) == 1: return False
    return True
def findshape(t):
    for nm in ('trigonal pyramidal', 'trigonal planar', 'tetrahedral', 'linear', 'bent'):
        if nm in t: return nm
    return None
def findangle(t):
    m = re.search(r'(109\.5|120|180|90)°', t); return m.group(1) if m else None
def F(t): return re.sub(r'[^A-Za-z0-9().]', '', t)   # choice text -> bare formula
def same(f1, f2): return atoms(f1) == atoms(f2)
def reduce(f):
    a = atoms(f); g = 0
    for v in a.values(): g = math.gcd(g, v)
    return collections.Counter({e: v // g for e, v in a.items()})
def leadint(t):
    m = re.match(r'\s*(\d+)', t); return int(m.group(1)) if m else None
def ints(t): return [int(x) for x in re.findall(r'(?<![\d.^])(\d+)(?![\d.])', t)]

# ================= ionic =================
print('Ionic bonding')
def charge_of(e): return VAL[e] if e in METALS else VAL[e] - 8
q = by('happens to sodium'); checked.add(q['id'])
ok(C(q, 0).startswith('It transfers to chlorine') and 'Na^+' in C(q, 0) and 'Cl^-' in C(q, 0) and charge_of('Na') == 1 and charge_of('Cl') == -1, q['id'] + ' Na -> Na+ (1 valence e), Cl -> Cl-')
q = by('most likely to form an <b>ionic</b> bond'); checked.add(q['id'])
pairs = [re.findall(r'[A-Z][a-z]?', C(q, j)) for j in range(4)]
isionic = [((a in METALS) != (b in METALS)) and dEN(a, b) > 2 for a, b in pairs]
ok(isionic == [True, False, False, False], '%s metal+nonmetal and dEN>2.0: %s' % (q['id'], [(p, str(dEN(*p))) for p in pairs]))
q = by('how many electrons does each calcium atom lose'); checked.add(q['id'])
def lg(t):
    m = re.search(r'Ca (loses|gains) (\d); O (gains|loses) (\d)', t); return m.groups() if m else None
want = ('loses', str(charge_of('Ca')), 'gains', str(-charge_of('O')))
ok(lg(C(q, 0)) == want and all(lg(C(q, j)) != want for j in (1, 2, 3)), '%s Ca loses %s, O gains %s; distractors differ' % (q['id'], want[1], want[3]))
q = by('accept the electrons from <b>one</b> aluminum atom'); checked.add(q['id'])
n = charge_of('Al') // -charge_of('F'); ok(leadint(C(q, 0)) == n and all(leadint(C(q, j)) != n for j in (1, 2, 3)) and leadint(C(q, 3)) == VAL['F'], '%s Al loses 3, F gains 1 -> %d F; "7" = F valence' % (q['id'], n))
for sub, cat, an in (('Each Mg atom loses 2 electrons and each N atom gains 3', 'Mg', 'N'), ('Aluminum loses 3 electrons and oxygen gains 2', 'Al', 'O')):
    q = by(sub); checked.add(q['id'])
    bal = []
    for j in range(4):
        a = atoms(F(C(q, j))); bal.append(a[cat] * charge_of(cat) + a[an] * charge_of(an) == 0)
    ok(bal == [True, False, False, False], '%s only %s balances lost/gained (%s%+d, %s%+d)' % (q['id'], C(q, 0), cat, charge_of(cat), an, charge_of(an)))
def classify(f):
    a = atoms(f)
    if not any(e in METALS for e in a) and 'NH4' not in f: return 'molecular'
    if 'OH' in f and re.search(r'\(OH\)|OH$', f) and any(e in METALS for e in a): return 'base'
    if set(a) - METALS == {'O'}: return 'oxide'
    return 'salt'
for sub, want in (('Which compound is a <b>base</b>', 'base'), ('Which compound is a <b>salt</b>', 'salt')):
    q = by(sub); checked.add(q['id'])
    cl = [classify(F(C(q, j))) for j in range(4)]
    ok(cl[0] == want and want not in cl[1:], '%s classes %s' % (q['id'], cl))
q = by('Quicklime, CaO, reacts with water'); checked.add(q['id'])
def claims(t):
    t = t.replace('Ca(OH)2', 'CAOH').replace('CaO', 'CAO')
    out = {}
    if t.startswith('Both are salts'): return {'CaO': 'salt', 'Ca(OH)2': 'salt'}
    for k, nm in (('CAO', 'CaO'), ('CAOH', 'Ca(OH)2')):
        m = re.search(k + r' is an? (metal oxide|base|salt)', t)
        if m: out[nm] = {'metal oxide': 'oxide'}.get(m.group(1), m.group(1))
    return out
truth = {'CaO': classify('CaO'), 'Ca(OH)2': classify('Ca(OH)2')}
cs = [claims(C(q, j)) for j in range(4)]
ok(cs[0] == truth and all(c != truth and len(c) == 2 for c in cs[1:]), '%s CaO %s, Ca(OH)2 %s; distractor claims %s' % (q['id'], truth['CaO'], truth['Ca(OH)2'], cs[1:]))
q = by('which ions form?'); checked.add(q['id'])
def ions(t): return dict((e, s) for e, s in re.findall(r'([A-Z][a-z]?)\^(\d?[+-])', t))
want = {'K': '+', 'S': '2-'}
ok(ions(C(q, 0)) == want and all(ions(C(q, j)) != want for j in (1, 2, 3)), '%s K%+d, S%+d' % (q['id'], charge_of('K'), charge_of('S')))
q = by('how many dots does each ion show'); checked.add(q['id'])
def dots(t):
    m = re.match(r'O\^2-: (\d) dots?; each Na\^\+: (\d) dots?', t); return m.groups() if m else None
ok(dots(C(q, 0)) == ('8', '0') and all(dots(C(q, j)) not in (None, ('8', '0')) for j in (1, 2, 3)) and dots(C(q, 1)) == (str(VAL['O']), str(VAL['Na'])),
   '%s after transfer O2- 8, Na+ 0; c[1] = before transfer (%d, %d)' % (q['id'], VAL['O'], VAL['Na']))

# ================= Lewis =================
print('Valence electrons (with charge) and intended errors')
def ve_errs(f, ch):
    a = atoms(f); base = sum(VAL[e] * n for e, n in a.items())
    e = {'key': base - ch, 'nocharge': base, 'flipcharge': base + ch,
         'octet': sum((2 if el == 'H' else 8) * n for el, n in a.items()), 'Z': sum(ZN[el] * n for el, n in a.items())}
    for el in a:
        if a[el] > 1: e['nosub ' + el] = base - VAL[el] * (a[el] - 1) - ch
    return e
for sub, f, ch, errs in (('valence electrons are in phosphorus trichloride', 'PCl3', 0, ['nosub Cl', 'octet', 'Z']),
                         ('valence electrons are in the hydronium ion', 'H3O', 1, ['nocharge', 'flipcharge', 'octet']),
                         ('valence electrons are in the phosphate ion', 'PO4', 3 * -1, ['nocharge', 'flipcharge', 'nosub O']),
                         ('valence electrons are in the carbonate ion', 'CO3', -2, ['nocharge', 'flipcharge', 'nosub O']),
                         ('valence electrons are in ethanol', 'C2H5OH', 0, ['nosub C', 'Z', 'octet'])):
    q = by(sub); checked.add(q['id']); e = ve_errs(f, ch)
    got = [leadint(C(q, j)) for j in range(4)]; want = [e['key']] + [e[x] for x in errs]
    ok(got == want and len(set(got)) == 4, '%s %s charge %+d: %s = key, %s' % (q['id'], f, -ch, got, ', '.join(errs)))
print('Which-structure items: only the key uses the right electron count and completes every octet (duet)')
# per choice: (formula, charge, atoms, lone pairs, bonds)
SC = {
 'Which describes the Lewis structure of hydrogen fluoride': ('HF', 0, [('H F', '0 3', '0-1'), ('H F', '1 3', '0-1'), ('H F', '0 2', '0=1'), ('H F', '0 4', '0-1')]),
 'Which describes the Lewis structure of nitrogen gas': ('N2', 0, [('N N', '1 1', '0#1'), ('N N', '2 2', '0=1'), ('N N', '3 3', '0-1'), ('N N', '0 0', '0#1')]),
 'Methanol, CH3OH, has 14 valence electrons': ('CH3OH', 0, [('C O H H H H', '0 2 0 0 0 0', '0-1 0-2 0-3 0-4 1-5'),
                                                ('C H H H H O', '0 0 0 0 0 3', '0-1 0-2 0-3 0-4 4-5'),
                                                ('C O H H H H', '0 0 0 0 0 0', '0-1 0-2 0-3 0-4 1-5'),
                                                ('C O H H H H', '0 3 0 0 0 0', '0-1 0-2 0-3 0-4 1-5')]),
 'Phosgene, COCl2': ('COCl2', 0, [('C O Cl Cl', '0 2 3 3', '0=1 0-2 0-3'), ('C O Cl Cl', '0 3 3 3', '0-1 0-2 0-3'),
                                 ('C O Cl Cl', '0 2 2 3', '0=1 0=2 0-3'), ('C O Cl Cl', '1 3 3 3', '0-1 0-2 0-3')]),
 'Which describes the Lewis structure of the ammonium ion': ('NH4', 1, [('N H H H H', '0 0 0 0 0', '0-1 0-2 0-3 0-4'), ('N H H H H', '1 0 0 0 0', '0-1 0-2 0-3 0-4'),
                                                             ('N H H H H', '1 0 0 0 0', '0-1 0-2 0-3 3-4'), ('N H H H H', '0 0 0 0 0', '0-1 0-2 0-3 0-4', -1)]),
 'Hydrogen peroxide, H2O2, is a common wound antiseptic': ('H2O2', 0, [('O O H H', '2 2 0 0', '0-1 0-2 1-3'), ('O O H H', '1 1 0 0', '0=1 0-2 1-3'),
                                                                      ('O O H H', '3 3 0 0', '0-1 0-2 1-3'), ('O O H H', '3 3 0 0', '2-0 2-3 3-1')]),
 'Carbon monoxide, CO, is the colorless gas': ('CO', 0, [('C O', '1 1', '0#1'), ('C O', '2 2', '0=1'), ('C O', '1 3', '0-1'), ('C O', '0 0', '0#1')]),
}
for sub, spec in SC.items():
    q = by(sub); checked.add(q['id']); f, ch, chs = spec; res = []
    for j, c in enumerate(chs):
        cch = c[3] if len(c) > 3 else ch
        at, lp, bonds = mk(*c[:3]); res.append(valid(f, cch, at, lp, bonds))
        t = C(q, j); nd = sum(1 for a, b, o in bonds if o == 2); nt = sum(1 for a, b, o in bonds if o == 3)
        if '–' in t or '=' in t or '≡' in t:
            if t.count('≡') != nt or t.count('=') != nd: err.append('%s c[%d] bond symbols do not match the encoded structure' % (q['id'], j))
    ok(res == [True, False, False, False], '%s %s (%d e): validity per choice %s' % (q['id'], f, VE(f, ch), res))
    k0 = mk(*chs[0][:3]); ref = [v for v in S.values() if v[4] == f and v[5] == ch]
    if ref and (sorted(k0[1]) != sorted(ref[0][1]) or sorted(o for a, b, o in k0[2]) != sorted(o for a, b, o in ref[0][2])): err.append(q['id'] + ' key differs from Lewis table entry')
print('Counts from the Lewis table')
q = by('How many <b>lone pairs</b> does the whole molecule have'); checked.add(q['id'])
ok([leadint(C(q, j)) for j in range(4)] == [lps('PCl3'), S['PCl3'][1][0], lps('PCl3') - S['PCl3'][1][0], lps('PCl3') + bp('PCl3')], '%s PCl3 lone pairs %d (center only %d; outer only %d; +bonds %d)' % (q['id'], lps('PCl3'), S['PCl3'][1][0], lps('PCl3') - 1, lps('PCl3') + bp('PCl3')))
q = by('bonds does each carbon atom form'); checked.add(q['id'])
nb = sum(o for a, b, o in S['C2H2'][2] if 0 in (a, b))
ok([leadint(C(q, j)) for j in range(4)] == [nb, len(neighbors('C2H2', 0)), 3, 5], '%s C2H2 bonds per C = %d (lines %d)' % (q['id'], nb, len(neighbors('C2H2', 0))))
q = by('electrons are shared in the triple bond'); checked.add(q['id'])
ok([leadint(C(q, j)) for j in range(4)] == [6, 3, 2, VE('N2')], '%s triple bond 6 e; N2 total %d' % (q['id'], VE('N2')))
q = by('how many bonding pairs and how many lone pairs'); checked.add(q['id'])
ok(ints(C(q, 0)) == [bp('CHCl3'), lps('CHCl3')] and all(ints(C(q, j)) != [bp('CHCl3'), lps('CHCl3')] for j in (1, 2, 3)), '%s CHCl3 %d bonding pairs, %d lone pairs (VE %d)' % (q['id'], bp('CHCl3'), lps('CHCl3'), VE('CHCl3')))
q = by('How many bonding pairs are shared between the two carbon atoms'); checked.add(q['id'])
o01 = [o for a, b, o in S['C2H2'][2] if {a, b} == {0, 1}][0]; ok(leadint(C(q, 0)) == o01 and VE('C2H2') == 10, '%s C2H2 C-C order %d' % (q['id'], o01))
q = by('a nitrogen atom forms three bonds'); checked.add(q['id'])
ok(leadint(C(q, 0)) == (VAL['N'] - 3) // 2 and 3 * 2 + 2 * leadint(C(q, 0)) == 8, '%s N: 3 bonds + %d lone pair = 8' % (q['id'], (VAL['N'] - 3) // 2))
q = by('After you draw a C&ndash;C single bond and four C&ndash;H bonds'); checked.add(q['id'])
rem = VE('C2H4') - 2 * 5
ok(leadint(C(q, 0)) == rem and any(o == 2 for a, b, o in S['C2H4'][2]) and leadint(C(q, 2)) is None and leadint(C(q, 3)) == VE('C2H4') - 5,
   '%s C2H4 %d e - 10 = %d left -> C=C; c[3] = 12 - 5 (1 e per line)' % (q['id'], VE('C2H4'), rem))
q = by('Which atom is the central atom in oxygen difluoride'); checked.add(q['id'])
ok(C(q, 0).startswith(S['OF2'][0][S['OF2'][3]]) and ENV['O'] < ENV['F'], '%s OF2 central O (EN O %s < F %s)' % (q['id'], ENV['O'], ENV['F']))

# ================= VSEPR =================
print('Electron groups and shapes (rule table, up to 4 groups)')
for sub, m, errs in (('How many electron groups surround the carbon', 'CH2O', None), ('each Cl has three lone pairs. How many electron groups', 'CCl4', None),
                     ('Carbon disulfide, S=C=S', 'CS2', None)):
    q = by(sub); checked.add(q['id']); g = groups(m); cen = S[m][3]
    dbl = sum(o for a, b, o in S[m][2] if cen in (a, b)) + S[m][1][cen]
    outer = sum(S[m][1][j] for j in neighbors(m, cen))
    got = [leadint(C(q, j)) for j in range(4)]
    ok(got[0] == g and g not in got[1:], '%s %s groups %d; distractors %s (multiple bond counted by order %d, + outer lone pairs %d)' % (q['id'], m, g, got[1:], dbl, g + outer))
    if m == 'CH2O' and got[1:] != [dbl, g + outer, dbl + outer]: err.append(q['id'] + ' CH2O distractors not the intended errors')
    if m == 'CCl4' and got[1:] != [g + outer, outer, 2 * bp(m)]: err.append(q['id'] + ' CCl4 distractors not the intended errors')
    if m == 'CS2' and got[1:3] != [dbl, g + outer]: err.append(q['id'] + ' CS2 distractors not the intended errors')
SH = [('Phosphine, PH3', 'PH3', None), ('Ground-level ozone, O3', 'O3', None), ('What is the H&ndash;C&ndash;H bond angle', 'CH4', None),
      ('what is the shape around each carbon atom', 'C2H2', 0), ('Complete the row for sulfur dichloride', 'SCl2', None),
      ('The hydronium ion, H3O^+, has three', 'H3O+', None), ('Oxygen difluoride, OF2, has two', 'OF2', None),
      ('Chloroform, CHCl3, has C bonded', 'CHCl3', None), ('best estimate of the Cl&ndash;P&ndash;Cl bond angle', 'PCl3', None),
      ('What is the shape around O?', 'CH3OH', 1)]
for sub, m, i in SH:
    q = by(sub); checked.add(q['id']); want = shape(m, i)
    def match(t):
        s_, a_ = findshape(t), findangle(t)
        return (s_ is None or s_ == want[0]) and (a_ is None or a_ == want[1]) and (s_ or a_)
    res = [bool(match(C(q, j))) for j in range(4)]
    ok(res == [True, False, False, False], '%s %s%s: %d groups, %d lone pairs -> %s, %s deg; choices %s' % (q['id'], m, '' if i is None else ' atom %d' % i, groups(m, i), S[m][1][S[m][3] if i is None else i], want[0], want[1], res))
    if m == 'SCl2':
        gl = '%d / %d' % (groups(m), S[m][1][0]); ok(C(q, 0).startswith(gl) and [r[1] for r in q['f'][0]['rows'][:2]] == ['%d / %d' % (groups('CH4'), 0), '%d / %d' % (groups('PCl3'), 1)] and
                                                    [r[2] for r in q['f'][0]['rows'][:2]] == [shape('CH4')[0], shape('PCl3')[0]], q['id'] + ' table rows CH4, PCl3 and key ' + gl)
q = by('A central atom has <b>3 electron groups</b>'); checked.add(q['id'])
res = [(findshape(C(q, j)), findangle(C(q, j))) == SHAPE[(3, 1)] for j in range(4)]; ok(res == [True, False, False, False], '%s 3 groups/1 LP -> %s' % (q['id'], SHAPE[(3, 1)]))
q = by('A central atom has <b>4 electron groups</b>'); checked.add(q['id'])
res = [findshape(C(q, j)) == SHAPE[(4, 1)][0] for j in range(4)]; ok(res == [True, False, False, False], '%s 4 groups/1 LP -> %s' % (q['id'], SHAPE[(4, 1)][0]))
q = by('two O&ndash;H bonds and two lone pairs on O. What are its electron-group geometry'); checked.add(q['id'])
def eg(t):
    m = re.match(r'(.+?) electron geometry; (.+?) shape', t); return m.groups() if m else None
want = (EGEOM[groups('H2O')], shape('H2O')[0])
ok(eg(C(q, 0)) == want and all(eg(C(q, j)) != want for j in (1, 2, 3)), '%s H2O %s electron geometry, %s shape' % (q['id'], *want))
for sub, target in (('Which molecule is <b>trigonal planar</b>?', 'trigonal planar'), ('Which molecule is <b>linear</b>?', 'linear')):
    q = by(sub); checked.add(q['id'])
    mols = [F(C(q, j)) for j in range(4)]; res = [shape(m)[0] == target for m in mols]
    ok(res == [True, False, False, False], '%s %s: %s' % (q['id'], target, [(m, shape(m)[0]) for m in mols]))
q = by('Why do CH4 and NH3 have different shapes'); checked.add(q['id'])
ok(groups('CH4') == groups('NH3') == 4 and shape('CH4') != shape('NH3') and S['NH3'][1][0] == 1, q['id'] + ' CH4 and NH3 both 4 groups; NH3 one lone pair')

# ================= polarity =================
print('Electronegativity, bond class, polarity')
q = by('is the <b>most electronegative</b>'); checked.add(q['id'])
v = [ENV[C(q, j)] for j in range(4)]; ok(v[0] == max(v) and v.count(v[0]) == 1, '%s EN %s' % (q['id'], [str(x) for x in v]))
q = by('order of <b>increasing</b> electronegativity'); checked.add(q['id'])
def inc(t):
    els = [x.strip() for x in t.split('<')]; return all(ENV[a] < ENV[b] for a, b in zip(els, els[1:]))
ok([inc(C(q, j)) for j in range(4)] == [True, False, False, False], q['id'] + ' increasing EN order Na Mg S Cl')
def denclaim(t):
    m = re.search(r'ΔEN = (-?\d\.\d)', t); cl = 'nonpolar covalent' if 'nonpolar covalent' in t else ('polar covalent' if 'polar covalent' in t else ('ionic' if 'ionic' in t else None))
    neg = re.search(r'([A-Z][a-z]?) is δ-', t)
    return (D(m.group(1)) if m else None, cl, neg.group(1) if neg else None)
for sub, a, b in (('for an N&ndash;O bond', 'N', 'O'), ('Classify the C&ndash;H bond', 'C', 'H'), ('Classify the Ca&ndash;F bond', 'Ca', 'F'),
                  ('Classify the P&ndash;Cl bond', 'P', 'Cl'), ('Classify the K&ndash;Cl bond', 'K', 'Cl')):
    q = by(sub); checked.add(q['id']); d_ = dEN(a, b); want = (d_, bclass(d_)); neg = a if ENV[a] > ENV[b] else b
    def right(t):
        x, cl, ng = denclaim(t); return x == want[0] and cl == want[1] and (ng is None or ng == neg)
    res = [right(C(q, j)) for j in range(4)]
    ok(res == [True, False, False, False], '%s %s-%s dEN %s %s; choices %s %s' % (q['id'], a, b, d_, want[1], [denclaim(C(q, j))[:2] for j in range(4)], res))
for sub, a, b in (('In an O&ndash;H bond, which atom carries', 'O', 'H'), ('In the C=O bond of formaldehyde', 'C', 'O')):
    q = by(sub); checked.add(q['id']); neg = a if ENV[a] > ENV[b] else b
    def dip(t):
        ng = re.search(r'([A-Z][a-z]?) is δ-', t); tw = re.search(r'[Tt]oward ([A-Z][a-z]?)', t)
        np_ = 'nonpolar' in t or 'no dipole' in t
        return (not np_) and (ng is None or ng.group(1) == neg) and (tw is not None and tw.group(1) == neg)
    ok([dip(C(q, j)) for j in range(4)] == [True, False, False, False] and dEN(a, b) > D('0.4'), '%s %s-%s: %s is delta-, arrow toward %s' % (q['id'], a, b, neg, neg))
def bonds_in(t): return re.findall(r'([A-Z][a-z]?)[–=]([A-Z][a-z]?)', t)
q = by('Which bond is the <b>most polar</b>?'); checked.add(q['id'])
v = [dEN(*bonds_in(C(q, j))[0]) for j in range(4)]; ok(v[0] == max(v) and v.count(v[0]) == 1, '%s dEN %s' % (q['id'], [str(x) for x in v]))
q = by('Which bond is <b>nonpolar covalent</b>?'); checked.add(q['id'])
v = [bclass(dEN(*bonds_in(C(q, j))[0])) for j in range(4)]; ok(v == ['nonpolar covalent'] + ['polar covalent'] * 3, '%s classes %s' % (q['id'], v))
for sub, want in (('Which molecule is <b>polar</b>?', True), ('nonpolar</b> even though its bonds are polar', False), ('which one is <b>nonpolar</b>?', False)):
    q = by(sub); checked.add(q['id'])
    mols = [F(C(q, j)) for j in range(4)]; res = [polar(m) == want for m in mols]
    ok(res == [True, False, False, False], '%s polar? %s' % (q['id'], [(m, polar(m)) for m in mols]))
    if 'bonds are polar' in sub:
        at = S[mols[0]][0]; ok(dEN(at[0], at[1]) > D('0.4'), '%s %s has polar bonds (dEN %s)' % (q['id'], mols[0], dEN(at[0], at[1])))
# per-choice claims: molecule verdicts and bond-class claims
PC = {
 'Is the CO2 molecule polar or nonpolar?': [{'CO2': False}, {'CO2': True}, {'CO2': True}, {'CO2': False, 'bond': ('C', 'O', 'nonpolar covalent')}],
 'cross the thin, fatty membranes': [{'O2': False, 'CO2': False}, {'O2': True, 'CO2': True}, {'CO2': True, 'O2': False}, {'bond': ('C', 'O', 'ionic')}],
 'is trigonal pyramidal, with one lone pair on P. Is it polar?': [{'PCl3': True}, {'PCl3': False}, {'PCl3': False, 'bond': ('P', 'Cl', 'nonpolar covalent')}, {'PCl3': True, 'bond': ('P', 'Cl', 'ionic')}],
}
for sub, chs in PC.items():
    q = by(sub); checked.add(q['id']); res = []
    for j, c in enumerate(chs):
        good = all(polar(m) == v for m, v in c.items() if m != 'bond')
        if 'bond' in c: a, b, cl = c['bond']; good = good and bclass(dEN(a, b)) == cl
        res.append(good)
        t = C(q, j)
        for m, v in c.items():
            if m != 'bond' and not (('nonpolar' in t.lower()) if v is False else ('polar' in t.lower())): err.append('%s c[%d] text does not state the encoded verdict for %s' % (q['id'], j, m))
    ok(res == [True, False, False, False], '%s claims per choice %s' % (q['id'], res))
q = by('Suppose instead it were linear'); checked.add(q['id'])
ok(dEN('O', 'H') > D('0.4') and 'nonpolar' in C(q, 0) and polar('H2O'), q['id'] + ' linear H-O-H would cancel (rule: no lone pair on centre, identical outer atoms); real bent water polar')
q = by('periodic trend in electronegativity'); checked.add(q['id'])
ok(ENV['F'] > ENV['Cl'] > ENV['Br'] > ENV['I'] and ENV['Li'] < ENV['C'] < ENV['O'] < ENV['F'] and C(q, 0).startswith('It increases across a period and decreases down a group'), q['id'] + ' trend from yellow-sheet values')

# ================= percent composition =================
print('Percent composition (formula: 4 s.f.; lab data: subtraction and division rules)')
def pf(f, e, n=None): return atoms(f)[e] * D(AM[e]) / MM(f) * 100
def nsf(f, e): return min(4, sf(AM[e]), sf(str(MM(f))))
PCT = [  # (stem substring, formula for the key or None, key element, list of (value, s.f., why))
 ('Food labels list sodium', 'NaCl', 'Na', [(D(AM['Na']) / D(AM['Cl']) * 100, 4, 'divided by Cl'), (pf('NaCl', 'Cl'), 4, '%Cl'), (MM('NaCl') / D(AM['Na']) * 100, 4, 'flipped')]),
 ('Ammonium sulfate', '(NH4)2SO4', 'N', [(D(AM['N']) / MM('(NH4)2SO4') * 100, 4, 'one N'), ((2 * D(AM['N']) + 8 * D(AM['H'])) / MM('(NH4)2SO4') * 100, 4, '%NH4'), (2 * D(AM['N']) / MM('NH4SO4') * 100, 4, 'wrong molar mass NH4SO4')]),
 ('Bone mineral is largely calcium phosphate, Ca3(PO4)2 (', 'Ca3(PO4)2', 'Ca', [(D(AM['Ca']) / MM('Ca3(PO4)2') * 100, 4, 'one Ca'), (pf('Ca3(PO4)2', 'P'), 4, '%P'), (3 * D(AM['Ca']) / MM('Ca3PO4') * 100, 4, 'Ca3PO4 molar mass')]),
 ('Ethanol, C2H5OH', 'C2H5OH', 'C', [(D(AM['C']) / MM('C2H5OH') * 100, 4, 'one C'), (D(2) / 9 * 100, 4, 'atom count'), (pf('C2H5OH', 'O'), 4, '%O')]),
 ('ferrous sulfate heptahydrate', 'FeSO4.7H2O', 'Fe', [(D(AM['Fe']) / MM('FeSO4') * 100, 4, 'anhydrous'), (D(AM['Fe']) / MM('FeSO4.H2O') * 100, 4, 'one water'), (MM('FeSO4.7H2O') / D(AM['Fe']) * 100, 4, 'flipped')]),
 ('Urea, CO(NH2)2', 'CO(NH2)2', 'N', [(D(AM['N']) / MM('CO(NH2)2') * 100, 4, 'one N'), (D(2) / 8 * 100, 4, 'atom count'), (2 * MM('N2') / MM('CO(NH2)2') * 100, 4, 'N2 mass per N')]),
 ('Calcium chloride, CaCl2', 'CaCl2', 'Cl', [(D(AM['Cl']) / MM('CaCl2') * 100, 4, 'one Cl'), (pf('CaCl2', 'Ca'), 4, '%Ca'), (2 * D(AM['Cl']) / D(AM['Ca']) * 100, 4, 'divided by Ca')]),
 ('Dairy digesters in the Valley capture methane', 'CH4', 'C', [(D(1) / 5 * 100, 4, 'atom count'), (pf('CH4', 'H'), 4, '%H'), (MM('CH4') / D(AM['C']) * 100, 4, 'flipped')]),
 ('Calcium dihydrogen phosphate, Ca(H2PO4)2', 'Ca(H2PO4)2', 'P', [(D(AM['P']) / MM('Ca(H2PO4)2') * 100, 4, 'one P'), (pf('Ca(H2PO4)2', 'Ca'), 4, '%Ca'), (D(AM['P']) / MM('CaH2PO4') * 100, 4, 'ignored outside 2')]),
 ('Niacin (vitamin B', 'C6H5NO2', 'N', [(D(1) / 14 * 100, 4, 'atom count'), (pf('C6H5NO2', 'C'), 4, '%C'), (MM('C6H5NO2') / D(AM['N']) * 100, 4, 'flipped')]),
]
for sub, f, e, dis in PCT:
    q = by(sub); checked.add(q['id'])
    n = nsf(f, e); key = fmt(pf(f, e), n) + '%'
    got = [C(q, j) for j in range(4)]; want = [key] + [fmt(v, k) + '%' for v, k, why in dis]
    ok(got == want and len(set(want)) == 4, '%s %%%s in %s = %s (%d s.f.); distractors %s' % (q['id'], e, f, key, n, ', '.join(w for _, _, w in dis)))
    if str(MM(f)) not in txt(q['q']) + txt(q['w']): err.append(q['id'] + ' molar mass %s not shown' % MM(f))
    if key not in txt(q['w']): err.append(q['id'] + ' key not in w')
    for el, val in re.findall(r'\(([A-Z][a-z]?) (\d+\.\d+)\)', txt(q['q'])):
        if AM[el] != val: err.append(q['id'] + ' quoted mass %s %s' % (el, val))
def sub_(a, b):
    r = D(a) - D(b); dpl = min(places(a), places(b)); return r.quantize(D(10) ** -dpl), dpl
def sfv(x):  # s.f. of a Decimal written with its decimal places
    return sf(format(x, 'f'))
LAB = [  # (stem substring, metal mass, product mass, key: 'metal' or 'nonmetal', predicted compound and element)
 ('1.308 g of zinc powder', '1.308', '1.950', 'metal', ('ZnS', 'Zn')),
 ('Heating 1.200 g of copper in air', '1.200', '1.502', 'nonmetal', ('CuO', 'O')),
 ('2.374 g of tin in air', '2.374', '3.014', 'metal', ('SnO2', 'Sn')),
]
for sub, mm_, pm, kind, (comp, el) in LAB:
    q = by(sub); checked.add(q['id'])
    nm, dpl = sub_(pm, mm_); s_m, s_p, s_n = sf(mm_), sf(pm), sfv(nm)
    pm_, mm2 = D(pm), D(mm_)
    metal = fmt(mm2 / pm_ * 100, min(s_m, s_p)) + '%'; non = fmt(nm / pm_ * 100, min(s_n, s_p)) + '%'
    ratio = fmt(mm2 / nm * 100, min(s_m, s_n)) + '%'; added_m = fmt(mm2 / (pm_ + mm2) * 100, min(s_m, s_p)) + '%'
    if kind == 'metal': want = [metal, non, ratio, added_m]
    else: want = [non, fmt(nm / mm2 * 100, min(s_n, s_m)) + '%', metal, fmt(nm / (pm_ + mm2) * 100, min(s_n, s_p)) + '%']
    got = [C(q, j) for j in range(4)]
    pred = pf(comp, el); meas = (mm2 if kind == 'metal' else nm) / pm_ * 100
    ok(got == want and len(set(want)) == 4 and abs(pred - meas) < D('0.5'), '%s %s: nonmetal %s g (%d s.f.); %s; distractors as intended; %s predicts %.2f%%' % (q['id'], sub[:24], nm, s_n, got[0], comp, pred))
q = by('magnesium-oxide lab (Experiment 5a)'); checked.add(q['id']); r = q['f'][0]['rows']
cr, cm, co = r[0][1], r[1][1], r[2][1]
mg, _ = sub_(cm, cr); ox, _ = sub_(co, cr); oo, _ = sub_(co, cm)
want = [fmt(mg / ox * 100, min(sfv(mg), sfv(ox))) + '%', fmt(mg / D(co) * 100, min(sfv(mg), sf(co))) + '%', fmt(oo / ox * 100, min(sfv(oo), sfv(ox))) + '%', fmt(mg / oo * 100, min(sfv(mg), sfv(oo))) + '%']
ok([C(q, j) for j in range(4)] == want and abs(mg / ox * 100 - pf('MgO', 'Mg')) < 1, '%s table: Mg %s g, oxide %s g, O %s g -> %s (MgO %.2f%%)' % (q['id'], mg, ox, oo, want[0], pf('MgO', 'Mg')))
q = by('54.53% C and 9.15% H'); checked.add(q['id'])
o_, _ = sub_(str(D(100) - D('54.53')), '9.15')
ok([C(q, j) for j in range(4)] == ['%s%%' % o_, '%s%%' % (D(100) - D('54.53')), '%s%%' % (D(100) - D('9.15')), '%s%%' % (D('54.53') + D('9.15'))] and
   fmt(pf('C4H8O2', 'C'), 4) == '54.53' and fmt(pf('C4H8O2', 'H'), 3) == '9.15', '%s %%O = %s (data fit C4H8O2: C %s, H %s)' % (q['id'], o_, fmt(pf('C4H8O2', 'C'), 4), fmt(pf('C4H8O2', 'H'), 3)))
q = by('law of constant composition say'); checked.add(q['id'])
ok(fmt(pf('NaCl', 'Na'), 4) + '%' in txt(q['y'][0]) and AM['Na'] in txt(q['y'][3]), q['id'] + ' NaCl %Na quoted as ' + fmt(pf('NaCl', 'Na'), 4))

# ================= empirical / molecular =================
print('Empirical and molecular formulas, hydrates')
def empirical(moles):
    mn = min(moles.values())
    for k in range(1, 7):
        r = {e: v / mn * k for e, v in moles.items()}
        if all(abs(x - x.to_integral_value()) <= D('0.1') for x in r.values()):
            return collections.Counter({e: int(x.to_integral_value()) for e, x in r.items()}), k, {e: v / mn for e, v in moles.items()}
    return None, None, None
def show(c): return ''.join(e + (str(n) if n > 1 else '') for e, n in c.items())
q = by('Butane, C4H10'); checked.add(q['id'])
ok(atoms(F(C(q, 0))) == reduce('C4H10') and all(atoms(F(C(q, j))) != reduce('C4H10') for j in (1, 2, 3)), '%s C4H10 -> %s' % (q['id'], show(reduce('C4H10'))))
q = by('Ethylene glycol, C2H6O2'); checked.add(q['id'])
ok(atoms(F(C(q, 0))) == reduce('C2H6O2') and all(atoms(F(C(q, j))) != reduce('C2H6O2') for j in (1, 2, 3)), '%s C2H6O2 -> %s' % (q['id'], show(reduce('C2H6O2'))))
q = by('have the <b>same empirical formula</b>'); checked.add(q['id'])
res = [reduce(a) == reduce(b) for a, b in (F(x).split('and') for x in (C(q, j).replace(' and ', 'and') for j in range(4)))]
ok(res == [True, False, False, False], '%s same empirical formula: %s' % (q['id'], res))
EMP = [  # (stem substring, data {el: grams or percent}, metal mass/product mass for lab items, index of the "divided grams" distractor or None)
 ('1.020 g of aluminum', None, ('Al', '1.020', '1.927', 'O'), None),
 ('50.05% S and 49.95% O', {'S': '50.05', 'O': '49.95'}, None, 1),
 ('Magnetite, a magnetic iron ore', {'Fe': '72.36', 'O': '27.64'}, None, None),
 ('43.64% P and 56.36% O', {'P': '43.64', 'O': '56.36'}, None, None),
 ('Copper wire (2.538 g)', None, ('Cu', '2.538', '3.178', 'S'), 1),
 ('81.71% C and 18.29% H', {'C': '81.71', 'H': '18.29'}, None, None),
 ('Heating 1.635 g of zinc', None, ('Zn', '1.635', '2.035', 'O'), 1),
 ('Aspirin is 60.00% C', {'C': '60.00', 'H': '4.48', 'O': '35.52'}, None, None),
]
for sub, data, lab, gi in EMP:
    q = by(sub); checked.add(q['id'])
    if lab:
        mt, a, b, nm_ = lab; nmass, _ = sub_(b, a); data = {mt: a, nm_: format(nmass, 'f')}
    for v in data.values():
        if lab is None and v not in txt(q['q']): err.append(q['id'] + ' datum %s not in stem' % v)
    moles = {e: D(v) / D(AM[e]) for e, v in data.items()}
    emp, k, ratios = empirical(moles)
    got = [atoms(F(C(q, j))) for j in range(4)]
    ok(emp is not None and got[0] == emp and all(g != emp for g in got[1:]), '%s moles %s; ratio %s; x%d -> %s' % (q['id'], {e: fmt(v, 4) for e, v in moles.items()}, {e: fmt(v, 4) for e, v in ratios.items()}, k, show(emp)))
    if gi is not None:
        g_emp, _, _ = empirical({e: D(v) for e, v in data.items()})
        ok(g_emp is not None and got[gi] == g_emp, '%s c[%d] is the divided-grams formula %s' % (q['id'], gi, show(g_emp) if g_emp else None))
MOL = [  # (stem substring, empirical formula or percent data, molar mass as given)
 ('Lactic acid, which muscle cells make', 'CH2O', '90.08'),
 ('mass percent composition of caffeine', {'C': '49.48', 'H': '5.19', 'N': '28.85', 'O': '16.48'}, '194.19'),
 ('Hydrogen peroxide is 5.93% H', {'H': '5.93', 'O': '94.07'}, '34.01'),
 ("Ibuprofen's empirical formula is", 'C13H18O2', '206.29'),
]
for sub, e_, Mg in MOL:
    q = by(sub); checked.add(q['id'])
    if isinstance(e_, dict):
        src = txt(q['q']) + ' ' + ' '.join(' '.join(r) for f in q.get('f', []) for r in f['rows'])
        for v in e_.values():
            if v not in src: err.append(q['id'] + ' datum %s not in stem/table' % v)
        emp, k, _ = empirical({e: D(v) / D(AM[e]) for e, v in e_.items()}); ef = show(emp)
    else:
        ef = e_
    n = D(Mg) / MM(ef); ni = int(n.to_integral_value())
    mol = collections.Counter({e: c * ni for e, c in atoms(ef).items()})
    got = [atoms(F(C(q, j))) for j in range(4)]
    others_mass = [MMraw(F(C(q, j))) for j in (1, 2, 3)]
    ok(abs(n - ni) < D('0.01') and got[0] == mol and all(g != mol for g in got[1:]) and all(abs(m - D(Mg)) > 1 for m in others_mass),
       '%s empirical %s (%s g/mol), n = %s -> %s; distractor masses %s' % (q['id'], ef, MM(ef), fmt(n, 4), show(mol), [str(MM(F(C(q, j)))) for j in (1, 2, 3)]))
HYD = [('Epsom salt is magnesium sulfate hydrate', '3.000', '1.465', 'MgSO4'), ('Gypsum, the raw material for dental stone', '3.150', '2.491', 'CaSO4')]
for sub, hm, am, salt in HYD:
    q = by(sub); checked.add(q['id'])
    w_, _ = sub_(hm, am); x = (w_ / MM('H2O')) / (D(am) / MM(salt)); xi = int(x.to_integral_value())
    got = [leadint(C(q, j)) for j in range(4)]
    ok(abs(x - xi) < D('0.05') and got[0] == xi and xi not in got[1:] and all(abs(x - g) > D('0.5') for g in got[1:]), '%s water %s g; x = %s -> %d; distractors %s' % (q['id'], w_, fmt(x, 4), xi, got[1:]))
    if salt == 'MgSO4':
        e1 = int((w_ / D(am)).to_integral_value()); e2 = int(((w_ / MM('H2O')) / (D(hm) / MM(salt))).to_integral_value()); e3 = int(((D(hm) / MM('H2O')) / (D(am) / MM(salt))).to_integral_value())
        ok(got[1:] == [e1, e2, e3], '%s distractors = grams ratio %d, hydrate mass as salt %d, whole mass as water %d' % (q['id'], e1, e2, e3))

# ---------- global consistency ----------
print('Global checks: quoted EN and atomic masses, dEN subtractions, every "a / b = c", molar masses, trailing-zero rule')
REG = set()
for f in ('NaCl', '(NH4)2SO4', 'Ca3(PO4)2', 'C2H5OH', 'FeSO4.7H2O', 'FeSO4', 'CO(NH2)2', 'CaCl2', 'CH4', 'Ca(H2PO4)2', 'C6H5NO2',
          'CH2O', 'C3H6O3', 'C2H4O2', 'C6H12O6', 'C4H5N2O', 'C8H10N4O2', 'C16H20N8O4', 'C12H15N6O3', 'MgSO4', 'H2O', 'CaSO4',
          'HO', 'H2O2', 'H4O4', 'C13H18O2', 'C26H36O4', 'C9H8O4', 'ZnS', 'CuO', 'SnO2', 'MgO', 'CaSO4.H2O', 'KCl', 'CaCO3'):
    REG.add(str(MM(f)))
REG |= {'90.08', '194.19', '34.01', '206.29', '58.44', '60.052', '180.156', '388.39', '291.29', '412.57', '68.03', '60.056'}
for q in ALL:
    i = q['id']
    everything = ' '.join([q['q'], q['w'], q['h']] + q['c'] + q['y'] + [' '.join(r) for f in q.get('f', []) for r in f['rows']])
    t = txt(everything)
    quoted = [m for grp in re.findall(r'\(([^()]*)\)', t) for m in re.findall(r'(?:^|, )([A-Z][a-z]?) (\d+\.\d+)(?=,|$)', grp)]
    for sym, val in quoted:
        if sym not in AM: continue
        if places(val) == 1:
            if sym in ENV and str(ENV[sym]) != val: err.append('%s quotes EN %s %s; yellow sheet %s' % (i, sym, val, ENV[sym]))
        elif D(val) >= 1 and AM[sym] != val and not (sym == 'O' and val == '15.999'):
            err.append('%s quotes %s %s; yellow sheet %s' % (i, sym, val, AM[sym]))
    for a, b, c in re.findall(r'(?<![\d.])(\d\.\d) - (\d\.\d) = (\d\.\d)', t):
        if D(a) - D(b) != D(c): err.append('%s subtraction %s - %s = %s' % (i, a, b, c))
        if not any((str(ENV[x]) == a) for x in ENV) or not any(str(ENV[x]) == b for x in ENV): err.append('%s dEN values %s, %s not on the yellow sheet' % (i, a, b))
    for a, b, c in re.findall(r'(?<![\d.])(?<!- )(\d+\.\d+) - (\d+\.\d+) = (\d+\.\d+)', t):
        if places(a) > 1 and D(a) - D(b) != D(c): err.append('%s subtraction %s - %s = %s' % (i, a, b, c))
    for a, b, pc, c in re.findall(r'(?<![\d.(])(\d+\.?\d*)(?: g| mol)? / (\d+\.?\d*)(?: g/mol| g| mol)?( x 100%)? = (\d+\.\d+)', t):
        v = D(a) / D(b) * (100 if pc else 1); tol = D(10) ** -places(c) * D('0.51') + v * D('0.0002')
        if abs(v - D(c)) > tol: err.append('%s arithmetic %s / %s%s = %s (is %s)' % (i, a, b, ' x 100%' if pc else '', c, fmt(v, 5)))
    for val in re.findall(r'(?<![\d.])(\d+\.\d+) g/mol', t):
        if val not in REG: err.append('%s molar mass %s g/mol not recomputed' % (i, val))
    if q['k'] == 1:
        s = re.sub(r'<sub>\d+</sub>', '', q['q']); s = re.sub(r'&middot;\d+', '', s); s = txt(s)
        for m in re.finditer(r'(?<![\d.^])(\d*[1-9]\d*0)(?![\d.^])', s):
            err.append(i + ' calculation stem has ambiguous trailing-zero value %r' % m.group(1))
    if q['k'] == 1 and i not in checked: err.append(i + ' calculation item not recomputed')

# ---------- coverage, counts, duplicates ----------
print('Items with a machine check: %d of %d (the rest are conceptual; read by hand)' % (len(checked), len(ALL)))
print('  not machine-checked:', ' '.join(q['id'] for q in ALL if q['id'] not in checked) or '(none)')
for nm, B in (('Try It', TRY), ('ADAPT', HW)):
    print(nm, len(B), dict(collections.Counter(q['t'] for q in B)), 'with figures:', sum(1 for q in B if q.get('f')),
          'd:', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1:', sum(q['k'] for q in B))
if len(HW) != 40: err.append('ADAPT has %d items, not 40' % len(HW))
norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip().lower()
dup = set(norm(q['q']) for q in TRY) & set(norm(q['q']) for q in HW)
if dup: err.append('same question in both banks: %s' % dup)
print('ERRORS:', err if err else 'none')
