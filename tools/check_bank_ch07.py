#!/usr/bin/env python3
"""Checker for the Chapter 7 banks (equations and balancing, reaction patterns, electrolytes and solubility,
precipitation and net ionic equations, acid-base and gas evolution, redox, activity series). Structural checks as in
tools/check_bank_ch06.py (ch07 topic ids), plus a chemistry engine written independently of the generators:
  - every equation in a correct choice, a stem, or the bold answer of a worked explanation is parsed back out of the
    HTML: atoms balance, charge balances (ionic, net ionic and half-reactions), coefficients are the lowest whole
    numbers, no H2CO3 / H2SO3 / NH4OH left as a product, and every (aq)/(s) label on an ionic compound agrees with
    the green-sheet solubility table of Section 7.4 (applied in code; the "slightly soluble" and Li+ cases are errors);
    ionic equations may not leave an aqueous strong electrolyte unsplit;
  - per-item specifications (looked up by stem text): the engine predicts the products itself (double displacement
    with solubility, neutralization, unstable products, H2S; single displacement by the activity series
    Li K Ca Na Mg Al Zn Fe Ni Sn Pb H2 Cu Ag Au; combination from ion charges; carbonate decomposition; complete and
    incomplete combustion), balances by solving the atom (and charge) equations exactly, and writes the molecular,
    complete ionic and net ionic equations; the key must equal the prediction and each distractor must differ;
  - classification of reaction patterns; oxidation numbers by the ordered rules of Section 7.7; oxidized/reduced
    species, agents, electrons transferred, half-reactions; redox vs not;
  - activity-series lists quoted in stems are contiguous slices of the series, in order;
  - exactly one correct choice per checked item (key correct, each distractor not correct);
  - no correct equation copies an equation from the Chapter 7 drafts (H+ + OH- -> H2O excepted), and no stem is
    shared between the banks.
usage: python3 tools/check_bank_ch07.py bank/ch07.json bank/ch07_adapt.json"""
import json, sys, re, os, collections, glob
from fractions import Fraction as Fr
from math import gcd
from functools import reduce
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = {'ch07-equations', 'ch07-types', 'ch07-solubility', 'ch07-netionic', 'ch07-acidgas', 'ch07-redox', 'ch07-activity'}
err = []

# ---------- structural checks ----------
OUT_OF_SCOPE = r'Henderson|molarity|limiting reactant|stoichiometr|enthalpy|disproportionation|acidic solution|basic solution|half-cell|standard reduction potential|galvanic|electrolytic cell'
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
        if re.search(r'all of the above|none of the above', json.dumps(q), re.I): err.append(i + ' AOTA/NOTA')
        s = ' '.join([q['q'], q['h'], q['w']] + q['c'] + q['y'])
        for tg in ('sub', 'sup', 'b', 'i'):
            if len(re.findall('<%s>' % tg, s)) != len(re.findall('</%s>' % tg, s)): err.append(i + ' unbalanced <%s>' % tg)
        if re.search(r'&(?!(?:[a-zA-Z]+|#\d+);)', s): err.append(i + ' bare &')
        if '{' in s or '}' in s or '[[' in s or ']]' in s: err.append(i + ' unconverted markup')
        if 'f' in q and not allow_f: err.append(i + ' has f (ADAPT items must be text only)')
        for f in q.get('f', []):
            if f['type'] != 'table': err.append(i + ' figure type not used/checked here: ' + f['type'])
            elif max(len(f['head']), *[len(r) for r in f['rows']]) > 3: err.append(i + ' table wider than 3 columns')
            elif max(len(plain(x)) for r in f['rows'] + [f['head']] for x in r) > 32: err.append(i + ' table cell too long for a phone')
        if re.search(OUT_OF_SCOPE, s, re.I): err.append(i + ' out of scope term')
        if label == 'HW' and not q['y'][0].startswith('Correct: '): err.append(i + ' ADAPT y[0] lacks "Correct: "')
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if right in plain(q['y'][j]): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c7-%03d', 'TRY', True)
structural(HW, 'c7-h%02d', 'HW', False)
if len(HW) != 42: err.append('ADAPT has %d items, not 42' % len(HW))
ALL = TRY + HW

def txt(x):
    x = re.sub(r'<sub>([^<]*)</sub>', r'\1', x)
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<[^>]+>', '', x)
    return (x.replace('&minus;', '-').replace('−', '-').replace('&rarr;', '->').replace('→', '->').replace('&times;', 'x')
             .replace('&nbsp;', ' ').replace('\xa0', ' ').replace('&ndash;', '–').replace('&deg;', '°').replace('&Delta;', 'Δ')
             .replace('&lt;', '<').replace('&gt;', '>').replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&amp;', '&'))

# ---------- formulas ----------
ELEMENTS = set('H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Cr Mn Fe Co Ni Cu Zn Br Sr Ag Sn I Ba Au Hg Pb Ti'.split())
def atoms(f):
    def grp(s, i):
        c = collections.Counter()
        while i < len(s) and s[i] != ')':
            if s[i] == '(':
                inner, i = grp(s, i + 1)
                if i >= len(s) or s[i] != ')': raise ValueError(f)
                i += 1
                m = re.match(r'\d*', s[i:]); k = int(m.group() or 1); i += m.end()
                for e in inner: c[e] += inner[e] * k
            else:
                m = re.match(r'([A-Z][a-z]?)(\d*)', s[i:])
                if not m or m.group(1) not in ELEMENTS: raise ValueError('bad formula %r' % f)
                c[m.group(1)] += int(m.group(2) or 1); i += m.end()
        return c, i
    c, i = grp(f, 0)
    if i != len(f): raise ValueError('bad formula %r' % f)
    return c
def isformula(f):
    try: atoms(f); return True
    except ValueError: return False
def key(f): return frozenset(atoms(f).items())

# species: (formula, charge, phase); 'e' = electron
def sp(tok):
    tok = tok.strip()
    m = re.fullmatch(r'(\d+(?:\.\d+)?) (.+)', tok)
    co = Fr(m.group(1)) if m else Fr(1)
    if m: tok = m.group(2)
    ph = None
    m = re.fullmatch(r'(.+?)\((s|l|g|aq)\)', tok)
    if m: tok, ph = m.group(1), m.group(2)
    ch = 0
    if '^' in tok:
        tok, c = tok.split('^'); n = int(c[:-1] or 1); ch = n if c[-1] == '+' else -n
    if tok == 'e': return co, ('e', -1, None)
    atoms(tok)
    return co, (tok, ch, ph)
SPC = r'(?:\d+(?:\.\d+)? )?(?:e\^-|[A-Z(][A-Za-z0-9()]*(?:\^\d*[+-])?(?:\((?:s|l|g|aq)\))?)'
EQRE = re.compile(SPC + r'(?: \+ ' + SPC + r')* -> ' + SPC + r'(?: \+ ' + SPC + r')*')
def parse_eq(s):
    L, R = s.split(' -> ')
    return [sp(t) for t in L.split(' + ')], [sp(t) for t in R.split(' + ')]
def eqs_in(html):
    out = []
    for m in EQRE.finditer(txt(html)):
        try: out.append((m.group(), parse_eq(m.group())))
        except ValueError: pass
    return out
def one_eq(html):
    e = eqs_in(html)
    return e[0][1] if len(e) == 1 else None
def norm(eq, water_any=False):
    def side(S):
        c = collections.Counter()
        for co, (f, ch, ph) in S:
            k = ('e',) if f == 'e' else (key(f), ch, ('g/l' if water_any and f == 'H2O' and ph in ('g', 'l') else ph))
            c[k] += co
        return frozenset(c.items())
    return (side(eq[0]), side(eq[1]))
def show(eq):
    def s(S): return ' + '.join(('' if co == 1 else str(co) + ' ') + f + ('' if not ch else '^' + (str(abs(ch)) if abs(ch) > 1 else '') + ('+' if ch > 0 else '-')) + ('(%s)' % ph if ph else '') for co, (f, ch, ph) in S)
    return s(eq[0]) + ' -> ' + s(eq[1])

# ---------- ions and the green-sheet solubility table ----------
CAT = [('Li', 1), ('Na', 1), ('K', 1), ('NH4', 1), ('Ag', 1), ('H', 1), ('Mg', 2), ('Ca', 2), ('Sr', 2), ('Ba', 2),
       ('Zn', 2), ('Fe', 2), ('Fe', 3), ('Cu', 2), ('Ni', 2), ('Pb', 2), ('Sn', 2), ('Hg2', 2), ('Al', 3), ('Cr', 3)]
AN = [('F', -1), ('Cl', -1), ('Br', -1), ('I', -1), ('OH', -1), ('NO3', -1), ('C2H3O2', -1), ('ClO4', -1), ('ClO3', -1),
      ('HCO3', -1), ('HSO3', -1), ('SO4', -2), ('SO3', -2), ('CO3', -2), ('CrO4', -2), ('C2O4', -2), ('O', -2), ('S', -2),
      ('PO4', -3), ('N', -3)]
G1 = {'Li', 'Na', 'K'}
MOLECULAR = {'H2O', 'H2O2', 'NH3', 'CO2', 'CO', 'SO2', 'SO3', 'CH4', 'C2H2', 'C3H8', 'C4H10', 'C5H12', 'C6H14', 'C3H8O',
             'C2H6O', 'C6H12O6', 'C12H22O11', 'CON2H4', 'CH4O', 'C6H10O5', 'N2', 'O2', 'H2', 'Cl2', 'Br2', 'I2', 'O3', 'OF2'}
MOLKEYS = {key(f) for f in MOLECULAR}
STRONG_ACIDS = {key(f) for f in ('HCl', 'HBr', 'HI', 'HNO3', 'HClO4', 'H2SO4')}
def lcm(a, b): return a * b // gcd(a, b)
def split(f, ch=0):
    """formula -> (cation, qc, n_cat, anion, qa, n_an) or None"""
    if ch or key(f) in MOLKEYS: return None
    A = atoms(f); hits = []
    for c, qc in CAT:
        for a, qa in AN:
            L = lcm(qc, -qa); nc, na = L // qc, L // -qa
            t = collections.Counter()
            for e, n in atoms(c).items(): t[e] += n * nc
            for e, n in atoms(a).items(): t[e] += n * na
            if t == A: hits.append((c, qc, nc, a, qa, na))
    hits = list(set(hits))
    if len(hits) > 1:
        hits = [h for h in hits if not (h[0] == 'H' and h[3] in ('OH', 'O'))]  # H2O-like splits
    if len(hits) > 1: raise ValueError('ambiguous ions for %s: %s' % (f, hits))
    return hits[0] if hits else None
def sol(c, a):
    if c in G1 or c == 'NH4':
        if c == 'Li' and a in ('CO3', 'PO4', 'F'): return 'edge'
        return 'soluble'
    if a in ('NO3', 'C2H3O2', 'ClO4', 'ClO3'): return 'soluble'
    if a in ('Cl', 'Br', 'I'): return 'insoluble' if c in ('Ag', 'Hg2', 'Pb') else 'soluble'
    if a == 'F': return 'insoluble' if c in ('Mg', 'Ca', 'Sr', 'Ba', 'Pb') else 'soluble'
    if a in ('SO4', 'SO3'): return 'insoluble' if c in ('Ca', 'Sr', 'Ba', 'Ag', 'Pb') else 'soluble'
    if a in ('CO3', 'PO4', 'CrO4', 'C2O4'): return 'insoluble'
    if a in ('O', 'S'): return 'soluble' if c in ('Ca', 'Sr', 'Ba') else 'insoluble'
    if a == 'OH': return 'slight' if c in ('Ca', 'Sr', 'Ba') else 'insoluble'
    return None
def solubility(f):
    s = split(f)
    if not s or s[0] == 'H': return None
    return sol(s[0], s[3])
def is_acid(f):
    s = split(f); return bool(s) and s[0] == 'H'
def eclass(f):
    k = key(f)
    if k == key('NH3'): return 'weak'
    if k in MOLKEYS: return 'non'
    s = split(f)
    if s is None: raise ValueError('cannot classify ' + f)
    if s[0] == 'H': return 'strong' if k in STRONG_ACIDS else 'weak'
    return {'soluble': 'strong'}.get(sol(s[0], s[3]), 'insoluble')
def is_element(f): return len(atoms(f)) == 1 and key(f) not in {key('O3')} or f in ('O2', 'O3')
def strong_aq(f, ch, ph):
    if ph != 'aq' or ch or f == 'e': return False
    try: c = eclass(f)
    except ValueError: return False
    return c == 'strong'

# ---------- balancing (exact rational nullspace) ----------
def balance(L, R, use_charge=True):
    """L, R: lists of (formula, charge, phase) -> lowest whole-number coefficients, or error"""
    S = L + R; els = sorted({e for f, ch, ph in S if f != 'e' for e in atoms(f)})
    rows = [[(atoms(f)[e] if f != 'e' else 0) * (1 if i < len(L) else -1) for i, (f, ch, ph) in enumerate(S)] for e in els]
    if use_charge: rows.append([ch * (1 if i < len(L) else -1) for i, (f, ch, ph) in enumerate(S)])
    n = len(S); Mx = [[Fr(x) for x in r] for r in rows]; piv = []; r = 0
    for col in range(n):
        p = next((k for k in range(r, len(Mx)) if Mx[k][col] != 0), None)
        if p is None: continue
        Mx[r], Mx[p] = Mx[p], Mx[r]; pv = Mx[r][col]; Mx[r] = [x / pv for x in Mx[r]]
        for k in range(len(Mx)):
            if k != r and Mx[k][col] != 0: f_ = Mx[k][col]; Mx[k] = [a - f_ * b for a, b in zip(Mx[k], Mx[r])]
        piv.append(col); r += 1
    free = [c for c in range(n) if c not in piv]
    if len(free) != 1: raise ValueError('balance not unique for %s' % S)
    v = [Fr(0)] * n; v[free[0]] = Fr(1)
    for k, col in enumerate(piv): v[col] = -Mx[k][free[0]]
    if any(x <= 0 for x in v): raise ValueError('balance gives non-positive coefficients for %s' % S)
    den = reduce(lcm, [x.denominator for x in v]); iv = [int(x * den) for x in v]; g = reduce(gcd, iv)
    iv = [x // g for x in iv]
    return [(Fr(c), s) for c, s in zip(iv[:len(L)], L)], [(Fr(c), s) for c, s in zip(iv[len(L):], R)]

# ---------- generic equation checks ----------
def eq_problems(eq, ctx=''):
    P = []; L, R = eq
    tot = lambda S: sum((collections.Counter({e: n * co for e, n in atoms(f).items()}) for co, (f, ch, ph) in S if f != 'e'), collections.Counter())
    chg = lambda S: sum(co * ch for co, (f, ch, ph) in S)
    if tot(L) != tot(R): P.append('atoms unbalanced')
    if chg(L) != chg(R): P.append('charge unbalanced')
    cos = [co for co, s in L + R]
    if any(c.denominator != 1 for c in cos): P.append('fractional coefficient')
    elif reduce(gcd, [int(c) for c in cos]) != 1: P.append('coefficients not lowest')
    for co, (f, ch, ph) in R:
        if f != 'e' and key(f) in {key('H2CO3'), key('H2SO3'), key('NH4OH')}: P.append('unstable product %s left' % f)
    allS = L + R
    has_aq = any(ph == 'aq' for co, (f, ch, ph) in allS)
    ionic_eq = any(ch for co, (f, ch, ph) in allS if f != 'e')
    dissolution = (len(L) == 1 and L[0][1][2] == 's' and all(s[1] for co, s in R))
    for co, (f, ch, ph) in allS:
        if f == 'e' or ch: continue
        try: s = split(f)
        except ValueError as e_: P.append(str(e_)); continue
        if s is None: continue
        if ph is None: continue
        if s[0] == 'H':
            if ph != 'aq' and has_aq and not (key(f) == key('H2S') and ph == 'g'): P.append('acid %s not (aq)' % f)
            continue
        v = sol(s[0], s[3])
        if v in ('edge', 'slight', None) and (ph == 'aq' or (ph == 's' and has_aq)): P.append('%s is a %s case on the green sheet' % (f, v or 'not-listed')); continue
        if v is None: continue
        if ph == 'aq' and v != 'soluble': P.append('%s(aq) but insoluble' % f)
        if ph == 's' and v == 'soluble' and has_aq and not dissolution: P.append('%s(s) but soluble' % f)
        if ph not in ('aq', 's'): P.append('%s has phase %s' % (f, ph))
    if ionic_eq:
        for co, (f, ch, ph) in allS:
            if strong_aq(f, ch, ph): P.append('ionic equation leaves %s(aq) unsplit' % f)
    return P

# ---------- prediction engine ----------
SERIES = ['Li', 'K', 'Ca', 'Na', 'Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'H', 'Cu', 'Ag', 'Au']
MCHG = {'Li': 1, 'K': 1, 'Ca': 2, 'Na': 1, 'Mg': 2, 'Al': 3, 'Zn': 2, 'Fe': 2, 'Ni': 2, 'Sn': 2, 'Pb': 2, 'Cu': 2, 'Ag': 1, 'Au': 3}
NONMETAL_ION = {'O2': ('O', -2), 'Cl2': ('Cl', -1), 'Br2': ('Br', -1), 'I2': ('I', -1), 'F2': ('F', -1), 'N2': ('N', -3), 'S': ('S', -2)}
ELEM_PHASE = {'O2': 'g', 'H2': 'g', 'N2': 'g', 'Cl2': 'g', 'F2': 'g', 'Br2': 'l', 'I2': 's', 'S': 's', 'Hg': 'l'}
FUEL_PHASE = {'CH4': 'g', 'C2H2': 'g', 'C3H8': 'g', 'C4H10': 'g', 'C5H12': 'l', 'C6H14': 'l', 'C3H8O': 'l', 'C2H6O': 'l', 'C6H10O5': 's', 'C6H12O6': 's'}
def above(m1, m2): return SERIES.index(m1) < SERIES.index(m2)
def build(c, qc, a, qa):
    L = lcm(qc, -qa); nc, na = L // qc, L // -qa
    wrap = lambda x, n: (('(%s)' % x if len(atoms(x)) > 1 or sum(atoms(x).values()) > 1 and not re.fullmatch(r'[A-Z][a-z]?\d*', x) else x) + str(n)) if n > 1 else x
    if c == 'Hg2': return 'Hg2' + wrap(a, na)
    return wrap(c, nc) + wrap(a, na)
def phase_of(f):
    if f in ELEM_PHASE: return ELEM_PHASE[f]
    if len(atoms(f)) == 1: return 's'
    if f in FUEL_PHASE: return FUEL_PHASE[f]
    s = split(f)
    if s is None: raise ValueError('no phase for ' + f)
    if s[0] == 'H': return 'aq'
    v = sol(s[0], s[3])
    if v == 'soluble': return 'aq'
    if v == 'insoluble': return 's'
    raise ValueError('%s is a %s solubility case' % (f, v))
def dd_product(c, qc, a, qa):
    """products of cation c + anion a after the swap, with decompositions"""
    if c == 'H' and a == 'OH': return [('H2O', 0, 'l')]
    if c == 'H' and a in ('CO3', 'HCO3'): return [('CO2', 0, 'g'), ('H2O', 0, 'l')]
    if c == 'H' and a in ('SO3', 'HSO3'): return [('SO2', 0, 'g'), ('H2O', 0, 'l')]
    if c == 'H' and a == 'S': return [('H2S', 0, 'g')]
    if c == 'NH4' and a == 'OH': return [('NH3', 0, 'g'), ('H2O', 0, 'l')]
    if c == 'H' and a == 'HSO3': return [('SO2', 0, 'g'), ('H2O', 0, 'l')]
    f = build(c, qc, a, qa)
    if c == 'H' and key(f) not in STRONG_ACIDS and a != 'C2H3O2': raise ValueError('weak acid product %s not supported' % f)
    return [(f, 0, phase_of(f))]
def predict(reactants, how='complete'):
    """-> ('NR', None) or (pattern, balanced molecular equation)"""
    R = list(reactants)
    els = [f for f in R if len(atoms(f)) == 1]
    cmp_ = [f for f in R if len(atoms(f)) > 1]
    if 'O2' in R and any(set(atoms(f)) >= {'C', 'H'} for f in cmp_):
        fuel = [f for f in cmp_ if set(atoms(f)) >= {'C', 'H'}][0]
        prods = [('CO2' if how == 'complete' else 'CO', 0, 'g'), ('H2O', 0, 'g')]
        return 'combustion', balance([(fuel, 0, FUEL_PHASE[fuel]), ('O2', 0, 'g')], prods)
    if len(R) == 2 and len(els) == 2:
        metal = [f for f in R if f in MCHG][0]; nm = [f for f in R if f != metal][0]
        a, qa = NONMETAL_ION[nm]; prod = build(metal, MCHG[metal], a, qa)
        return 'combination', balance([(metal, 0, 's'), (nm, 0, ELEM_PHASE[nm])], [(prod, 0, 's')])
    if len(R) == 1:
        s = split(R[0])
        if s and s[3] == 'CO3':
            ox = build(s[0], s[1], 'O', -2)
            return 'decomposition', balance([(R[0], 0, 's')], [(ox, 0, 's'), ('CO2', 0, 'g')])
        raise ValueError('decomposition of %s not supported' % R[0])
    if len(els) == 1 and len(cmp_) == 1:
        m = els[0]; s = split(cmp_[0]); X = s[0]
        if not above(m, X): return 'NR', None
        newc = build(m, MCHG[m], s[3], s[4])
        freed = ('H2', 0, 'g') if X == 'H' else (X, 0, 's')
        return 'single displacement', balance([(m, 0, 's'), (cmp_[0], 0, phase_of(cmp_[0]))], [(newc, 0, phase_of(newc)), freed])
    if len(cmp_) == 2:
        s1, s2 = split(cmp_[0]), split(cmp_[1])
        prods = dd_product(s1[0], s1[1], s2[3], s2[4]) + dd_product(s2[0], s2[1], s1[3], s1[4])
        merged = []
        for p in prods:
            if p not in merged: merged.append(p)
        if {key(p[0]) for p in merged} == {key(f) for f in cmp_}: return 'NR', None
        eq = balance([(f, 0, phase_of(f)) for f in cmp_], merged)
        if not net_ionic(eq)[0]: return 'NR', None
        return 'double displacement', eq
    raise ValueError('cannot predict %s' % R)
def ions_of(co, f, ch, ph):
    if not strong_aq(f, ch, ph): return [(co, (f, ch, ph))]
    s = split(f)
    return [(co * s[2], (s[0], s[1], 'aq')), (co * s[5], (s[3], s[4], 'aq'))]
def complete_ionic(eq):
    L, R = eq
    def side(S):
        c = collections.OrderedDict()
        for co, s in S:
            for co2, s2 in ions_of(co, *s): c[s2] = c.get(s2, 0) + co2
        return [(v, k) for k, v in c.items()]
    return side(L), side(R)
def net_ionic(eq):
    L, R = complete_ionic(eq)
    dl = collections.OrderedDict((s, c) for c, s in L); dr = collections.OrderedDict((s, c) for c, s in R)
    for s in list(dl):
        if s in dr:
            m = min(dl[s], dr[s]); dl[s] -= m; dr[s] -= m
    L2 = [(c, s) for s, c in dl.items() if c]; R2 = [(c, s) for s, c in dr.items() if c]
    if not L2 and not R2: return [], []
    g = reduce(gcd, [int(c) for c, s in L2 + R2])
    return [(c / g, s) for c, s in L2], [(c / g, s) for c, s in R2]
def spectators(eq):
    L, R = complete_ionic(eq); n = net_ionic(eq)
    netset = {s for c, s in n[0] + n[1]}
    return {(f, ch) for c, (f, ch, ph) in L if ch and (f, ch, ph) in {s for c2, s in R} and (f, ch, ph) not in netset}
def dissolve(f):
    s = split(f)
    return [(Fr(1), (f, 0, 's'))], [(Fr(s[2]), (s[0], s[1], 'aq')), (Fr(s[5]), (s[3], s[4], 'aq'))]

# ---------- oxidation numbers (rules of Section 7.7, in order) ----------
G2 = {'Be', 'Mg', 'Ca', 'Sr', 'Ba'}
def oxnums(f, ch=0, _ionic=True):
    A = atoms(f)
    if len(A) == 1:
        e = next(iter(A)); return {e: Fr(ch, A[e])}          # rules 1 and 2
    ON = {}; rem = Fr(ch)
    def left(): return [e for e in A if e not in ON]
    for rule in ('G1', 'G2', 'F', 'H', 'O', 'X'):
        if len(left()) == 1: break
        for e in left():
            v = None
            if rule == 'G1' and e in G1: v = 1
            if rule == 'G2' and e in G2: v = 2
            if rule == 'F' and e == 'F': v = -1
            if rule == 'H' and e == 'H': v = 1
            if rule == 'O' and e == 'O': v = -2
            if rule == 'X' and e in ('Cl', 'Br', 'I'): v = -1
            if v is not None and len(left()) > 1: ON[e] = Fr(v)
    lf = left()
    if len(lf) == 1:
        e = lf[0]; ON[e] = (Fr(ch) - sum(ON[x] * A[x] for x in ON)) / A[e]; return ON
    if not lf: return ON
    s = split(f, ch) if _ionic else None
    if s:  # ionic compound whose ions each need the rules (e.g. NiSO4): monatomic ion = its charge
        out = {}
        for ion, q in ((s[0], s[1]), (s[3], s[4])):
            for e, v in oxnums(ion, q, False).items(): out[e] = v
        return out
    raise ValueError('oxidation numbers undetermined for %s' % f)
def ox_changes(eq):
    """element -> (reactant value, product value) for every element that changes"""
    L, R = eq; out = {}
    def vals(S):
        d = collections.defaultdict(set)
        for co, (f, ch, ph) in S:
            if f == 'e': continue
            for e, v in oxnums(f, ch).items(): d[e].add(v)
        return d
    a, b = vals(L), vals(R)
    for e in a:
        if a[e] != b.get(e, a[e]): out[e] = (a[e], b[e])
    return out
def is_redox(eq): return bool(ox_changes(eq))
def oxidized_species(eq):
    L, R = eq; ch = ox_changes(eq)
    return {(f, c) for co, (f, c, ph) in L if f != 'e' and any(e in ch and max(ch[e][1]) > min(ch[e][0]) and oxnums(f, c)[e] < max(ch[e][1]) for e in atoms(f))}
def reduced_species(eq):
    L, R = eq; ch = ox_changes(eq)
    return {(f, c) for co, (f, c, ph) in L if f != 'e' and any(e in ch and min(ch[e][1]) < max(ch[e][0]) and oxnums(f, c)[e] > min(ch[e][1]) for e in atoms(f))}
def electrons(eq):
    L, R = eq
    lost = sum(co * n * max(Fr(0), max(oxnums(f2, c2)[e] for co2, (f2, c2, p2) in R if f2 != 'e' and e in atoms(f2)) - oxnums(f, c)[e])
               for co, (f, c, ph) in L if f != 'e' for e, n in atoms(f).items())
    gained = sum(co * n * max(Fr(0), oxnums(f, c)[e] - min(oxnums(f2, c2)[e] for co2, (f2, c2, p2) in R if f2 != 'e' and e in atoms(f2)))
                 for co, (f, c, ph) in L if f != 'e' for e, n in atoms(f).items())
    if lost != gained: raise ValueError('electrons lost %s != gained %s' % (lost, gained))
    return lost
def half(kind, metal, ion):
    f, q = ion
    if kind == 'ox': return [(Fr(1), (metal, 0, 's'))], [(Fr(1), (f, q, 'aq')), (Fr(q), ('e', -1, None))]
    return [(Fr(1), (f, q, 'aq')), (Fr(q), ('e', -1, None))], [(Fr(1), (metal, 0, 's'))]
def classify(eq):
    L, R = eq
    fl = [f for co, (f, ch, ph) in L]; fr = [f for co, (f, ch, ph) in R]
    el = lambda f: len(atoms(f)) == 1
    if 'O2' in fl and any(set(atoms(f)) >= {'C', 'H'} for f in fl) and any(key(f) in (key('CO2'), key('CO')) for f in fr): return 'combustion'
    if len(fl) >= 2 and len(fr) == 1: return 'combination'
    if len(fl) == 1 and len(fr) >= 2: return 'decomposition'
    if len(fl) == 2 and len(fr) == 2 and sum(map(el, fl)) == 1 and sum(map(el, fr)) == 1: return 'single displacement'
    if len(fl) == 2 and not any(map(el, fl)) and len(fr) >= 2 and not any(map(el, fr)): return 'double displacement'
    return 'other'

# ---------- choice readers ----------
STOP = {'No', 'I'}
def formulas_in(t):
    """bare formulas (with optional ^charge) in plain text, in order"""
    out = []; t = re.sub(r'\((?:s|l|g|aq)\)', '', t)
    for m in re.finditer(r'(?<![A-Za-z0-9^(])([A-Z(][A-Za-z0-9()]*)(\^(\d*)([+-]))?', t):
        f = m.group(1)
        if f in STOP and not m.group(2): continue
        if not isformula(f): continue
        ch = 0
        if m.group(2): n = int(m.group(3) or 1); ch = n if m.group(4) == '+' else -n
        out.append((f, ch))
    return out
def formula_of(t):
    fs = formulas_in(txt(t))
    if not fs: raise ValueError('no formula in %r' % t)
    return fs[-1][0] if len(fs) > 1 and fs[0][0] in ('Acetic',) else fs[0][0]
def is_NR(t): return bool(re.match(r'\s*no reaction', txt(t), re.I))
def number(t):
    m = re.search(r'[+-]?\d+(?:\.\d+)?', txt(t).replace(' ', ''))
    return Fr(m.group()) if m else None

# ---------- lookups ----------
def by(sub):
    m = [q for q in ALL if sub in q['q'] or sub in txt(q['q'])]
    if len(m) != 1: sys.exit('lookup %r matched %d items' % (sub, len(m)))
    return m[0]
checked = set(); hand = set(); skipstem = set()
def ok(cond, msg):
    print('   ', 'OK ' if cond else 'BAD', msg)
    if not cond: err.append(msg)
def exactly_one(q, pred, label):
    try: res = [bool(pred(c)) for c in q['c']]
    except Exception as e_: ok(False, '%s %s: %s' % (q['id'], label, e_)); return
    ok(res == [True, False, False, False], '%s %s %s' % (q['id'], label, res))
    checked.add(q['id'])

# ===================== per-item specifications =====================
def EQSPEC(sub, reactants, mode='mol', how='complete', water_any=None):
    q = by(sub); pat, eq = predict(reactants, how)
    if pat == 'NR': target = None
    elif mode == 'mol': target = eq
    elif mode == 'cie': target = complete_ionic(eq)
    else: target = net_ionic(eq)
    wa = (pat == 'combustion') if water_any is None else water_any
    def pred(c):
        if target is None: return is_NR(c)
        if is_NR(c): return False
        e = one_eq(c)
        if e is None: raise ValueError('no single equation in choice %r' % txt(c))
        return norm(e, wa) == norm(target, wa)
    exactly_one(q, pred, '%s %s -> %s' % (mode, '+'.join(reactants), 'NR' if target is None else show(target)))
def BAL(sub, skeleton, form='eq', what=None):
    q = by(sub); skipstem.add(q['id'])
    L, R = parse_eq(skeleton); eq = balance([s for c, s in L], [s for c, s in R])
    cos = [int(c) for c, s in eq[0] + eq[1]]
    if form == 'eq': pred = lambda c: (one_eq(c) is not None and norm(one_eq(c)) == norm(eq))
    elif form == 'coefs': pred = lambda c: [int(x) for x in re.findall(r'\d+', txt(c))] == cos
    else:
        idx = [s[0] for c, s in eq[0] + eq[1]].index(what)
        pred = lambda c: number(c) == cos[idx]
    exactly_one(q, pred, 'balance %s -> %s' % (skeleton, show(eq)))
def PRED(sub, pred, label): exactly_one(by(sub), pred, label)
def HAND(sub, skip=False):
    q = by(sub); hand.add(q['id'])
    if skip: skipstem.add(q['id'])
def stem_eq(sub, n=0): return eqs_in(by(sub)['q'])[n][1]
def TYPE(sub, label=None):
    q = by(sub)
    if label is None:   # choices are labels; stem has the equation
        e = stem_eq(sub); cl = classify(e)
        exactly_one(q, lambda c: txt(c).strip().lower() == cl, 'classify %s = %s' % (show(e), cl))
    else:               # choices are equations
        def pred(c):
            e = one_eq(c)
            P = eq_problems(e)
            if P: raise ValueError('choice %s: %s' % (show(e), P))
            return classify(e) == label
        exactly_one(q, pred, 'which is %s' % label)
def OX(sub, formula, ch, el):
    v = oxnums(formula, ch)[el]
    exactly_one(by(sub), lambda c: number(c) == v, 'oxidation number of %s in %s^%d = %s' % (el, formula, ch, v))
def SPECIES(sub, fn, label):
    q = by(sub); e = stem_eq(sub); target = fn(e)
    exactly_one(q, lambda c: {formulas_in(txt(c))[0]} == {x for x in target}, '%s = %s' % (label, target))
def SOLQ(sub, want):
    PRED(sub, lambda c: solubility(formula_of(c)) == want, 'the one %s compound' % want)
def ELEC(sub, want):
    PRED(sub, lambda c: eclass(formula_of(c)) == want, 'the one %s electrolyte' % want)
def NUM(sub, value, label):
    PRED(sub, lambda c: number(c) == Fr(value), '%s = %s' % (label, value))
def pair(c): return [f for f, ch in formulas_in(txt(c))]
def SPECT(sub, reactants):
    pat, eq = predict(reactants); target = spectators(eq)
    def pred(c):
        t = txt(c)
        got = set() if re.search(r'none', t, re.I) else set(formulas_in(t))
        return got == target
    PRED(sub, pred, 'spectators %s' % target)
def PPT(sub, reactants, kind='s'):
    pat, eq = predict(reactants)
    target = set() if pat == 'NR' else {key(f) for co, (f, ch, ph) in eq[1] if ph == kind and f != 'H2O'}
    def pred(c):
        t = txt(c)
        if re.match(r'\s*no ', t, re.I): return target == set()
        return {key(f) for f, ch in formulas_in(t)} == target
    PRED(sub, pred, ('precipitate' if kind == 's' else 'gas') + ' %s' % target)
def DISS(sub, formula):
    tgt = dissolve(formula)
    PRED(sub, lambda c: one_eq(c) is not None and norm(one_eq(c)) == norm(tgt), 'dissolving %s -> %s' % (formula, show(tgt)))
def NR_PAIR(sub, want=True):
    def pred(c):
        fs = pair(c); pat, eq = predict(fs); return (pat == 'NR') == want
    PRED(sub, pred, 'the one pair with %s' % ('no reaction' if want else 'a reaction'))
def series_ok(q):
    m = re.search(r'Activity series \(most active first\): ([^.]+)\.', txt(q['q']))
    if not m: return
    lst = [x.strip().replace('H2', 'H') for x in m.group(1).split(',')]
    i = SERIES.index(lst[0]) if lst[0] in SERIES else -1
    ok(i >= 0 and SERIES[i:i + len(lst)] == lst, '%s activity list %s is a contiguous slice of the series' % (q['id'], lst))
def ACT(sub, test, label):
    q = by(sub); series_ok(q); PRED(sub, test, label)
def EQACT(sub, reactants, mode='mol'):
    series_ok(by(sub)); EQSPEC(sub, reactants, mode)

print('Per-item checks')
# ----- Try It: equations -----
HAND('best evidence that a chemical reaction')
HAND('Which one is a <b>physical</b> change')
HAND('What does the label (s) after')
NUM('How many oxygen atoms are represented by 2', 2 * atoms('Al2(SO4)3')['O'], 'O atoms in 2 Al2(SO4)3')
NUM('2.43 g of magnesium reacts completely', Fr('2.43') + Fr('1.60'), 'mass of MgO')
NUM('heats baking soda', Fr('31.62') - Fr('28.52'), 'mass of gases lost')
BAL('Sulfur dioxide from burning sulfur-containing fuel', 'SO2(g) + O2(g) -> SO3(g)')
BAL('Balance the equation: Al2(SO4)3', 'Al2(SO4)3(aq) + KOH(aq) -> Al(OH)3(s) + K2SO4(aq)', 'coefs')
BAL('Lighter fluid is butane', 'C4H10(g) + O2(g) -> CO2(g) + H2O(g)', 'coef', 'O2')
HAND('A student balances', skip=True)
BAL('Aluminum metal burns in chlorine gas', 'Al(s) + Cl2(g) -> AlCl3(s)')
BAL('In a blast furnace', 'Fe2O3(s) + CO(g) -> Fe(s) + CO2(g)')
# ----- Try It: types -----
TYPE('Heating mercury(II) oxide')
TYPE('Nickel wire is placed in silver nitrate')
TYPE('What type of reaction is AgNO3')
TYPE('Which reaction is a <b>combination</b>', 'combination')
EQSPEC('Calcium metal heated in nitrogen gas', ['Ca', 'N2'])
EQSPEC('Strontium carbonate is heated', ['SrCO3'])
PRED('Aluminum sulfate solution (used to clarify', lambda c: {key(f) for f in pair(c)} == {key(f) for co, (f, ch, ph) in predict(['Al2(SO4)3', 'Ba(NO3)2'])[1][1]}, 'products of Al2(SO4)3 + Ba(NO3)2')
EQSPEC('propane space heater', ['C3H8', 'O2'], how='incomplete')
BAL('Rubbing alcohol (isopropyl alcohol', 'C3H8O(l) + O2(g) -> CO2(g) + H2O(g)', 'coef', 'O2')
TYPE('Which reaction is a <b>single-displacement</b>', 'single displacement')
# ----- Try It: solubility -----
ELEC('Which substance is a <b>nonelectrolyte</b>', 'non')
ELEC('Solution B is most likely', 'weak')
DISS('Calcium nitrate is a fertilizer used on Valley crops', 'Ca(NO3)2')
NUM('How many ions in total are released when one formula unit of Al2(SO4)3', sum(int(c) for c, s in dissolve('Al2(SO4)3')[1]), 'ions from Al2(SO4)3')
SOLQ('Use the solubility rules. Which compound is <b>insoluble</b>', 'insoluble')
SOLQ('Which of these compounds is <b>soluble</b>', 'soluble')
SOLQ('A barium contrast agent', 'insoluble')
SOLQ('Which sulfide is', 'insoluble')
PRED('Which pair contains <b>two insoluble</b>', lambda c: all(solubility(f) == 'insoluble' for f in pair(c)), 'both insoluble')
def clauses_true(c):
    cl = re.findall(r'([A-Z][A-Za-z0-9()]*) is (soluble|insoluble)', txt(c))
    return len(cl) == 2 and all(solubility(f) == v for f, v in cl)
PRED('Which statement about strontium fluoride', clauses_true, 'solubility statements')
# ----- Try It: net ionic -----
PPT('Copper(II) sulfate solution is mixed with sodium hydroxide', ['CuSO4', 'NaOH'])
PPT('Calcium nitrate solution is mixed with potassium chloride', ['Ca(NO3)2', 'KCl'])
EQSPEC('Hard-water scale is calcium carbonate', ['Ca(NO3)2', 'K2CO3'], 'net')
EQSPEC('Zinc chloride solution is mixed with potassium sulfide', ['ZnCl2', 'K2S'], 'cie')
SPECT('Lead(II) acetate solution is mixed with potassium iodide', ['Pb(C2H3O2)2', 'KI'])
EQSPEC('Aluminum hydroxide, an ingredient in some antacids', ['Al(NO3)3', 'KOH'], 'net')
NR_PAIR('Which pair of solutions gives <b>no reaction</b> when mixed?')
EQSPEC('Struvite kidney stones', ['MgCl2', 'Na3PO4'], 'net')
EQSPEC('silver nitrate and sodium carbonate', ['AgNO3', 'Na2CO3'], 'net')
EQSPEC('Sodium sulfide solution is mixed with copper(II) nitrate', ['Na2S', 'Cu(NO3)2'], 'net')
# ----- Try It: acid-base and gas evolution -----
EQSPEC('hydrobromic acid reacting with potassium hydroxide', ['HBr', 'KOH'])
EQSPEC('Sulfuric acid is neutralized by lithium hydroxide', ['H2SO4', 'LiOH'], 'net')
EQSPEC('Milk of magnesia', ['Mg(OH)2', 'HCl'], 'net')
EQSPEC('Vinegar (acetic acid, a weak acid)', ['HC2H3O2', 'NaOH'], 'net')
def h2co3_replacement(c):
    fs = {key(f) for f, ch in formulas_in(txt(c))}
    pat, eq = predict(['K2CO3', 'HNO3'])
    made = {key(f) for co, (f, ch, ph) in eq[1]} - {key('KNO3')}
    return fs == made
PRED('a student writes carbonic acid', h2co3_replacement, 'H2CO3 -> CO2 + H2O')
PPT('Sodium bisulfite', ['NaHSO3', 'HCl'], 'g')
EQSPEC('Spreading an ammonium fertilizer', ['(NH4)2SO4', 'KOH'])
EQSPEC('Solid iron(II) sulfide reacts with hydrochloric acid', ['FeS', 'HCl'])
PRED('gives <b>no reaction</b> when it is mixed with nitric acid', lambda c: predict(['HNO3', formula_of(c)])[0] == 'NR', 'the one salt with no reaction with HNO3')
# ----- Try It: redox -----
def fate(sub, el):
    q = by(sub); e = stem_eq(sub); a, b = ox_changes(e)[el]; d = max(b) - min(a)
    want = ('loses %d electrons and is oxidized' % d) if d > 0 else ('gains %d electrons and is reduced' % -d)
    exactly_one(q, lambda c: want in txt(c), 'fate of %s: %s' % (el, want))
fate('what happens to magnesium?', 'Mg')
OX('Ground-level ozone', 'O3', 0, 'O')
OX('Nitrate, NO3^-, is a fertilizer ion', 'NO3', -1, 'N')
OX('oxidation number of chromium in potassium chromate', 'K2CrO4', 0, 'Cr')
OX('oxygen difluoride', 'OF2', 0, 'O')
SPECIES('which reactant is oxidized?', oxidized_species, 'oxidized')
SPECIES('The thermite reaction', reduced_species, 'oxidizing agent')
SPECIES('A welding torch burns acetylene', oxidized_species, 'reducing agent')
PRED('How many electrons are transferred in 2 Al(s) + 3 Sn^2+', lambda c: number(c) == electrons(stem_eq('How many electrons are transferred in 2 Al(s) + 3 Sn^2+')), 'electrons transferred')
PRED('Stainless-steel implants', lambda c: norm(one_eq(c)) == norm(half('ox', 'Cr', ('Cr', 3))), 'Cr oxidation half-reaction')
EQSPEC('Use the half-reactions', ['Al', 'AgNO3'], 'net')
def not_redox(c):
    e = one_eq(c); P = eq_problems(e)
    if P: raise ValueError('%s: %s' % (show(e), P))
    return not is_redox(e)
PRED('Which reaction is <b>not</b> a redox reaction?', not_redox, 'the one non-redox reaction')
# ----- Try It: activity series -----
EQACT('corrodes iron sprayer tanks', ['Fe', 'CuSO4'])
ACT('Which metal will <b>not</b> react with hydrochloric acid?', lambda c: not above(formula_of(c), 'H'), 'metal below H2')
ACT('Which metal could recover lead', lambda c: above(formula_of(c), 'Pb'), 'metal above Pb')
EQACT('Does lead metal react with zinc chloride', ['Pb', 'ZnCl2'])
EQACT('aluminum reacting with hydrochloric acid?', ['Al', 'HCl'])
ACT('reacts with nickel(II) nitrate solution but not with zinc', lambda c: above(formula_of(c), 'Ni') and not above(formula_of(c), 'Zn'), 'metal between Zn and Ni')
EQACT('Galvanized steel irrigation pipe', ['Zn', 'FeCl2'], 'net')

# ----- ADAPT -----
HAND('What does the &Delta; mean?')
NUM('How many hydrogen atoms are represented by 4', 4 * atoms('(NH4)3PO4')['H'], 'H atoms in 4 (NH4)3PO4')
NUM('third, empty beaker', Fr('62.45') + Fr('58.30') - Fr('82.30') + Fr('41.18'), 'mass of third beaker and contents')
BAL('Balance the equation: Al(s) + H2SO4', 'Al(s) + H2SO4(aq) -> Al2(SO4)3(aq) + H2(g)', 'coefs')
BAL('Hexane', 'C6H14(l) + O2(g) -> CO2(g) + H2O(g)', 'coef', 'O2')
BAL('Solid potassium metal reacts with liquid water', 'K(s) + H2O(l) -> KOH(aq) + H2(g)')
TYPE('Sulfur trioxide from burning')
TYPE('Silver oxide, used in some button batteries')
TYPE('Which reaction is a <b>double-displacement</b>', 'double displacement')
EQSPEC('zinc metal placed in nickel(II) chloride', ['Zn', 'NiCl2'])
EQSPEC('Burning orchard prunings', ['C6H10O5', 'O2'], how='incomplete')
EQSPEC('Aluminum powder and sulfur combine', ['Al', 'S'])
ELEC('Which substance is a <b>strong</b> electrolyte?', 'strong')
SOLQ('Which calcium compound is <b>soluble</b>', 'soluble')
DISS('iron(III) sulfate dissolving', 'Fe2(SO4)3')
SOLQ('By the green-sheet rules, which compound', 'insoluble')
NUM('formula unit of (NH4)3PO4 dissolves', sum(int(c) for c, s in dissolve('(NH4)3PO4')[1]), 'ions from (NH4)3PO4')
PRED('one strong electrolyte and one nonelectrolyte', lambda c: sorted(eclass(f) for f in pair(c)) == ['non', 'strong'], 'strong + non pair')
PPT('Lead(II) nitrate solution is mixed with sodium bromide', ['Pb(NO3)2', 'NaBr'])
EQSPEC('Older X-ray film', ['AgNO3', 'KBr'], 'net')
SPECT('Sodium carbonate solution is mixed with copper(II) chloride', ['Na2CO3', 'CuCl2'])
EQSPEC('Sodium phosphate solution is mixed with silver nitrate', ['Na3PO4', 'AgNO3'], 'cie')
EQSPEC('Mercury(I) nitrate solution', ['Hg2(NO3)2', 'KCl'], 'net')
PRED('Which one gives <b>no precipitate</b>?', lambda c: predict(['Cu(NO3)2', formula_of(c)])[0] == 'NR', 'the one salt with no reaction with Cu(NO3)2')
EQSPEC('hydroiodic acid, HI(aq), reacting with sodium hydroxide', ['HI', 'NaOH'], 'net')
EQSPEC('Some antacids contain magnesium carbonate', ['MgCO3', 'HCl'])
PPT('Sodium sulfide solution is mixed with hydrochloric acid', ['Na2S', 'HCl'], 'g')
EQSPEC('Sulfites are preservatives in wine', ['K2SO3', 'HBr'], 'net')
EQSPEC('Instant cold packs', ['NH4NO3', 'NaOH'])
PRED('Which one produces a gas?', lambda c: any(ph == 'g' for co, (f, ch, ph) in (predict(['HCl', formula_of(c)])[1] or ([], []))[1]), 'the one salt giving a gas with HCl')
OX('Rust is mostly iron(III) oxide', 'Fe2O3', 0, 'Fe')
OX('The carbonate ion, CO3^2-, is part of blood', 'CO3', -2, 'C')
OX('hypochlorite ion', 'ClO', -1, 'Cl')
SPECIES('Chlorine water added to potassium iodide', reduced_species, 'oxidizing agent')
PRED('How many electrons are transferred in 2 Fe(s)', lambda c: number(c) == electrons(stem_eq('How many electrons are transferred in 2 Fe(s)')), 'electrons transferred')
PRED('which is the reduction half-reaction?', lambda c: norm(one_eq(c)) == norm(half('red', 'Sn', ('Sn', 2))), 'Sn reduction half-reaction')
EQACT('A silver ring is dropped into copper(II) nitrate', ['Ag', 'Cu(NO3)2'])
ACT('Which metal reacts with zinc nitrate solution?', lambda c: above(formula_of(c), 'Zn'), 'metal above Zn')
EQACT('Nickel forms Ni^2+', ['Ni', 'HBr'])
ACT('does not react with iron(II) chloride solution', lambda c: above(formula_of(c), 'H') and not above(formula_of(c), 'Fe'), 'metal between Fe and H2')
EQACT('aluminum metal reacting with nickel(II) chloride', ['Al', 'NiCl2'], 'net')
ACT('dilute hydrobromic acid', lambda c: not above(formula_of(c), 'H'), 'metal below H2')

# ===================== generic checks on every item =====================
print('Generic equation checks: correct choices, stems, and bold answers in worked explanations')
neq = 0
for q in ALL:
    i = q['id']
    places = [('c[0]', q['c'][0])] + ([] if i in skipstem else [('stem', q['q'])]) + [('w<b>', b) for b in re.findall(r'<b>(.*?)</b>', q['w'])]
    for where, h in places:
        for s_, e in eqs_in(h):
            neq += 1
            try: P = eq_problems(e)
            except ValueError as e_: P = [str(e_)]
            for p_ in P: err.append('%s %s: %s [%s]' % (i, where, p_, s_))
    for where, h in [('q', q['q']), ('c', ' '.join(q['c']))]:
        for f, ch in formulas_in(txt(h)):
            if f in ('Yes',): continue
    if q['t'] == 'ch07-activity' or re.search(r'activity series', q['q'], re.I): series_ok(q)
print('    %d equations parsed and checked' % neq)

# no correct equation copied from the drafts' worked examples and exercises
# sections 7.0-7.8 and 7.12 (teaching text, worked examples, exercises) are errors; the chapter guide, practice
# problems and games pages (7.9-7.11) are only reported, since those pages are written separately.
def nophase(e): return tuple(frozenset((k[:2] if len(k) == 3 else k, v) for k, v in side) for side in e)
WHITE = {nophase(norm(parse_eq('H^+(aq) + OH^-(aq) -> H2O(l)'), True))}
warn = []
for p_ in sorted(glob.glob(os.path.join(ROOT, 'drafts', 'ch07', '*.html'))):
    nm = os.path.basename(p_); later = re.match(r'7\.(9|10|11)_', nm) is not None
    found = set()
    for s_, e in eqs_in(open(p_, encoding='utf-8').read()):
        try: found.add(nophase(norm(e, True)))
        except Exception: pass
    for q in ALL:
        for s_, e in eqs_in(q['c'][0]):
            n_ = nophase(norm(e, True))
            if n_ in found and n_ not in WHITE:
                (warn if later else err).append('%s correct choice repeats an equation in %s: %s' % (q['id'], nm, s_))
print('Draft overlap (sections 7.0-7.8, 7.12 = error; 7.9-7.11 = note):')
for w_ in warn: print('    NOTE', w_)

# ---------- coverage, counts, duplicates ----------
miss = [q['id'] for q in ALL if q['id'] not in checked and q['id'] not in hand]
if miss: err.append('items with no specification: %s' % ' '.join(miss))
print('Items with a machine check of the key and every distractor: %d of %d' % (len(checked), len(ALL)))
print('  conceptual (key read by hand; stems and keys still pass the generic checks):', ' '.join(sorted(hand)) or '(none)')
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
