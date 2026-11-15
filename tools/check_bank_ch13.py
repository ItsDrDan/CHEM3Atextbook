#!/usr/bin/env python3
"""Checker for the Chapter 13 banks (collision theory and rates, dynamic equilibrium, equilibrium constants,
Le Chatelier's principle).
Structural checks as in tools/check_bank_ch11.py (ch13 topic ids and planned counts; ADAPT = 42 items, text only,
y[0] begins "Correct: "; at most 4 figures, tables at most 3 columns; figures only of types js/fbx.js supports;
no Going Further terms (Ka, Kb, Kw, Ksp, Kp, solubility product, common ion), no AOTA/NOTA), plus, written
independently of the generators:
  - every equation anywhere (-> or <=>, including chained equilibria) is parsed back out of the HTML, with phases
    and ionic charges, and must balance in atoms and in charge;
  - K expressions: every expression in a choice is parsed (species, exponents, coefficient multipliers, sums) and
    compared with the expression the checker derives from the stem's own equation (products over reactants,
    coefficients as exponents, (s) and (l) left out); the key must match and every distractor must differ;
  - calculation items (k=1): K, and each numeric distractor's intended error (inverted, no exponents, coefficient
    as a multiplier, sums instead of products, all multiplied, water left out), recomputed with Decimal from the
    concentrations as written in the stem (or its table) TWO ways: round once at the end, and strict (every power,
    product and sum rounded first); both must give the choice as written, and the exact value must not sit on a
    rounding tie; reverse-reaction K = 1/K; activation energy and delta H from the stem or the figure;
  - Le Chatelier key table: for every shift item the stress is written here by hand (add/remove a species, heat
    or cool, decrease/increase the volume, catalyst, inert gas); the expected shift is computed from the stem's
    equation (side of the species, (s)/(l) -> no shift, sign of delta H or the words endo/exothermic, moles of gas
    on each side, catalyst/inert -> none), with the effect on K (temperature only) and on each species, [H+]/pH
    and color; every choice's claims are parsed (direction, K, [X], pH, color): the key must be wholly true, and
    every distractor must make at least one false claim; stress-choice items map each choice to a stress and
    exactly the key meets the target;
  - other key tables: rate factors (concentration, temperature, surface area, catalyst), lower Ea is faster,
    the enzyme-table optimum, the 10 °C doubling rule, equilibrium time from readings or the graph, reverse
    reactions, size of K (K > 10 products, K < 0.1 reactants, else both), smallest K;
  - course rule: no whole number ending in 0 without a decimal point in a calculation stem;
  - exactly one correct choice (four different choices; recomputed values all different);
  - no stem reuses a draft worked example or exercise (a given from a draft Example/Exercise, two shared givens,
    the same equation as a draft Example/Exercise apart from the listed teaching equations, or a similar stem);
    no stem in both banks; Mateo in at most 2 items.
usage: python3 tools/check_bank_ch13.py bank/ch13.json bank/ch13_adapt.json"""
import json, sys, re, os, collections, glob
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 50; getcontext().rounding = ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = {'ch13-rates', 'ch13-dynamic', 'ch13-k', 'ch13-lechat'}
err = []

# ---------- text ----------
def tx(x):
    """text with tags removed in place (sub/sup kept inline), single spaces."""
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<span[^>]*display:block[^>]*>', ' ', x)
    x = re.sub(r'<[^>]+>', '', x)
    for a, b in (('&minus;', '-'), ('&times;', 'x'), ('&nbsp;', ' '), ('&rarr;', '->'), ('&rlarr;', '<=>'), ('&ldquo;', '"'),
                 ('&rdquo;', '"'), ('&ndash;', '–'), ('&lt;', '<'), ('&gt;', '>'), ('&#8811;', '>>'), ('&#8810;', '<<'),
                 ('&Delta;', 'Δ'), ('&amp;', '&')):
        x = x.replace(a, b)
    return re.sub(r'\s+', ' ', x).strip()
txt = tx
def plain(x): return tx(x).lower()

# ---------- structural checks ----------
OUT_OF_SCOPE = r"\bK(?:a|b|w|sp|p)\b|solubility product|common[- ]ion|all of the above|none of the above"
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
        for tg in ('sub', 'sup', 'b', 'i', 'span'):
            if len(re.findall('<%s[ >]' % tg, s)) != len(re.findall('</%s>' % tg, s)): err.append(i + ' unbalanced <%s>' % tg)
        if re.search(r'&(?!(?:[a-zA-Z]+\d*|#\d+);)', s): err.append(i + ' bare &')
        if '{' in s or '}' in s or '[[' in s or ']]' in s: err.append(i + ' unconverted markup')
        if re.search(r'(?<![\w;])-(?=\d)', s): err.append(i + ' hyphen used as a minus sign')
        if re.search(OUT_OF_SCOPE, tx(s), re.I): err.append(i + ' out of scope term (Going Further) or AOTA/NOTA')
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
structural(TRY, 'c13-%03d', 'TRY', True)
structural(HW, 'c13-h%02d', 'HW', False)
if len(HW) != 42: err.append('ADAPT has %d items, not 42' % len(HW))
if sum(1 for q in TRY if q.get('f')) > 4: err.append('more than 4 figures')
fbx = open(os.path.join(ROOT, 'js', 'fbx.js'), encoding='utf-8').read()
for t_ in {f['type'] for q in TRY for f in q.get('f', [])}:
    if not re.search(r'[{,]%s:' % t_, fbx): err.append('figure type %s not supported by js/fbx.js' % t_)
wid = open(os.path.join(ROOT, 'js', 'widget.js'), encoding='utf-8').read()
for t_ in TOP:
    if "'%s'" % t_ not in wid: err.append('topic %s missing from js/widget.js TOPICS' % t_)
WANT_T = {'ch13-rates': 16, 'ch13-dynamic': 12, 'ch13-k': 16, 'ch13-lechat': 26}
WANT_H = {'ch13-rates': 9, 'ch13-dynamic': 7, 'ch13-k': 10, 'ch13-lechat': 16}
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
def R(x, n, m): return D(x) if m == 0 else D(fmt(x, n).replace(' x 10^', 'e'))
def tie(x, n):
    x = abs(D(x)); e = x.adjusted(); f = x.scaleb(n - 1 - e); return f - int(f) == D('0.5')
def rq(v, d):
    s = format(D(v).quantize(D(10) ** -d), 'f')
    return s + '.' if d == 0 and s.endswith('0') else s
def ADDs(xs, m):
    """sum of concentration strings: exact (m=0) or by the decimal-place rule (m=1)."""
    v = sum(D(x) for x in xs)
    return v if m == 0 else D(rq(v, min(dec(x) for x in xs)))
def num_in(s):
    """'9.75 x 10^-4' or '26.0' -> Decimal"""
    m = re.fullmatch(r'(-?[\d.]+)(?: x 10\^(-?\d+))?', s.strip())
    return D(m.group(1).rstrip('.')) * (D(10) ** int(m.group(2)) if m.group(2) else 1)

# ---------- species and equations (phases, charges) ----------
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
            if not m: raise ValueError(f)
            stack[-1][m.group(1)] += int(m.group(2) or 1); i += m.end()
    return stack[0]
def charge(ch):
    if not ch: return 0
    m = re.fullmatch(r'\^(\d*)([+-])', ch); return (int(m.group(1) or 1)) * (1 if m.group(2) == '+' else -1)
SP = r'(?:\d+ )?(?:heat|[A-Z(][A-Za-z0-9()]*(?:\^\d*[+-])?\((?:s|l|g|aq)\))'
SIDE = SP + r'(?: \+ ' + SP + r')*'
EQRE = re.compile(SIDE + r'(?: (?:->|<=>) ' + SIDE + r')+')
def sp(tok):
    tok = tok.strip()
    m = re.fullmatch(r'(\d+) (.+)', tok); co = int(m.group(1)) if m else 1
    t = m.group(2) if m else tok
    if t == 'heat': return (co, 'heat', None, None)
    m = re.fullmatch(r'(.+?)(\^\d*[+-])?\((s|l|g|aq)\)', t)
    f, ch, ph = m.group(1), m.group(2) or '', m.group(3)
    atoms(f); return (co, f + ch, ph, charge(ch))
def parse_eq(s):
    parts = re.split(r' (?:->|<=>) ', s)
    arrows = re.findall(r' (->|<=>) ', s)
    return [[sp(t) for t in p.split(' + ')] for p in parts], arrows
def eqs_in(h):
    t = tx(h); out = []
    for m in EQRE.finditer(t):
        try: out.append((m.group(), parse_eq(m.group())))
        except (ValueError, AttributeError): pass
    return out
def side_count(S_):
    c = collections.Counter(); q_ = 0
    for co, f, ph, ch in S_:
        if f == 'heat': continue
        for el, n in atoms(re.sub(r'\^.*', '', f)).items(): c[el] += co * n
        q_ += co * ch
    return c, q_
def balanced(parts):
    return all(side_count(parts[i]) == side_count(parts[i + 1]) for i in range(len(parts) - 1))
print('Equations (every field) balance in atoms and charge')
neq = 0
for q in ALL:
    for h in [q['q'], q['h'], q['w']] + q['c'] + q['y']:
        for s_, (parts, ar) in eqs_in(h):
            neq += 1
            if not balanced(parts): err.append('%s unbalanced equation %s' % (q['id'], s_))
print('    %d equations parsed, all balanced' % neq)
def stem_eq(q, i=0):
    e = eqs_in(q['q'])
    return e[i][1][0] if len(e) > i else None

# ---------- K expressions ----------
def K_of(parts):
    """expression the checker derives: (numerator dict, denominator dict) over gas/aq species, exponents = coefficients."""
    inK = lambda S_: {f: co for co, f, ph, ch in S_ if ph in ('g', 'aq')}
    return inK(parts[-1]), inK(parts[0])
def parse_K(s):
    t = tx(s); m = re.fullmatch(r'K = (.+?)(?: / (.+))?', t)
    if not m: return None
    def part(p):
        flags = set(); p = p.strip()
        if p.startswith('(') and p.endswith(')'): p = p[1:-1]
        if '+' in re.sub(r'\[[^\]]*\]', '', p): flags.add('sum')
        d_ = {}
        for co, f, e in re.findall(r'(\d*)\[([^\]]+)\](?:\^(\d+))?', p):
            if co: flags.add('mult')
            d_[f] = d_.get(f, 0) + int(e or 1)
        if not d_ and p != '1': flags.add('?')
        return d_, flags
    n_, f1 = part(m.group(1)); d_, f2 = part(m.group(2)) if m.group(2) else ({}, set())
    return n_, d_, f1 | f2
def Kmatch(expr, parts):
    p = parse_K(expr)
    return p is not None and not p[2] and (p[0], p[1]) == K_of(parts)

def by(sub):
    m = [q for q in ALL if sub in tx(q['q'])]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
checked, hand = set(), set()

print('K expressions: key = the expression derived from the stem equation; distractors differ')
for sub in ('Write the equilibrium constant expression for 2 NO(g)', 'Ammonia burns in oxygen', 'Ammonium carbonate, the solid',
            'expression for 2 H2(g) + O2(g) <=> 2 H2O(l)', 'Tin ore is reduced', 'Each hemoglobin molecule can carry',
            'Nitrous oxide (laughing gas)', 'expression for CH4(g) + 2 H2S(g)', 'baking soda is heated in a closed container',
            'In the Mond process for purifying nickel'):
    q = by(sub)
    if not q: continue
    checked.add(q['id']); e = stem_eq(q)
    good = [Kmatch(c, e) for c in q['c']]
    ok(good == [True, False, False, False] and all(parse_K(c) for c in q['c']), '%s K expression key %r (derived %s)' % (q['id'], tx(q['c'][0]), K_of(e)))
q = by('Which reaction has the equilibrium constant expression')
if q:
    checked.add(q['id']); tgt = parse_K(re.search(r'K = \[[^\]]+\]', tx(q['q'])).group())
    res = [K_of(parse_eq(tx(c))[0]) == (tgt[0], tgt[1]) for c in q['c']]
    ok(res == [True, False, False, False], '%s only c[0] has K = [CO2]: %s' % (q['id'], res))

# ---------- calculation items: K ----------
print('Calculation items: key and distractors recomputed (round once = strict = the choice as written; no ties)')
def conc_from(q):
    t = tx(q['q']); c = dict(re.findall(r'\[([^\]]+)\] = ([\d.]+) M', t))
    for f in q.get('f', []):
        if f['type'] == 'table': c.update({tx(r[0]): tx(r[1]) for r in f['rows']})
    return c
def Kmode(parts, c, mode, m):
    num_, den_ = K_of(parts)
    allc = [c[s] for s in list(num_) + list(den_)]; n = min(sf(x) for x in allc)
    pw = lambda s, e: R(D(c[s]) ** e, sf(c[s]), m)
    def prod(d_, exp=True, mul=False):
        v = D(1)
        for s, e in d_.items(): v *= (D(e) * D(c[s]) if mul else pw(s, e) if exp else D(c[s]))
        return R(v, n, m) if d_ else D(1)
    if mode.startswith('omit:'):
        x = mode[5:]; num_ = {k: v for k, v in num_.items() if k != x}; den_ = {k: v for k, v in den_.items() if k != x}; mode = 'K'
    if mode == 'K': v = prod(num_) / prod(den_)
    elif mode == 'inv': v = prod(den_) / prod(num_)
    elif mode == 'noexp': v = prod(num_, False) / prod(den_, False)
    elif mode == 'coefmul': v = prod(num_, mul=True) / prod(den_, mul=True)
    elif mode == 'sumnum': v = ADDs([c[s] for s in num_], m) / prod(den_, False)
    elif mode == 'sumden': v = prod(num_, False) / ADDs([c[s] for s in den_], m)
    elif mode == 'sumboth': v = ADDs([c[s] for s in num_], m) / ADDs([c[s] for s in den_], m)
    elif mode == 'prodall': v = prod(num_, False) * prod(den_, False)
    return v, n
CALC = [('Nitrosyl chloride breaks down', ['K', 'inv', 'noexp', 'sumnum']),
        ('Use the table of equilibrium concentrations to calculate K', ['K', 'inv', 'noexp', 'coefmul']),
        ('Bromine monochloride partly breaks down', ['K', 'inv', 'noexp', 'sumnum']),
        ('An equilibrium mixture for CO(g) + Cl2(g)', ['K', 'inv', 'sumden', 'prodall']),
        ('Hot charcoal reacts with carbon dioxide', ['K', 'inv', 'noexp', 'coefmul']),
        ('At the very high temperature of a car engine', ['K', 'inv', 'noexp', 'coefmul']),
        ('An equilibrium mixture for NO2(g) + CO(g)', ['K', 'inv', 'sumboth', 'prodall']),
        ('An equilibrium mixture for 2 NO(g) + Br2(g)', ['K', 'inv', 'noexp', 'sumden'])]
for sub, modes in CALC:
    q = by(sub)
    if not q: continue
    checked.add(q['id']); e = stem_eq(q); c = conc_from(q)
    sp_all = set(K_of(e)[0]) | set(K_of(e)[1])
    if set(c) != sp_all: err.append('%s concentrations given %s, K needs %s' % (q['id'], sorted(c), sorted(sp_all)))
    print('  %s %s' % (q['id'], sub[:50]))
    keys = []
    for j, mode in enumerate(modes):
        (a, n), (b, _) = Kmode(e, c, mode, 0), Kmode(e, c, mode, 1)
        fa, fb = fmt(a, n), fmt(b, n)
        if fa != fb: err.append('%s c[%d] %s ambiguous: %s (round once) vs %s (strict)' % (q['id'], j, mode, fa, fb))
        if tie(a, n): err.append('%s c[%d] %s exact value %s is a rounding tie' % (q['id'], j, mode, a))
        keys.append(fa)
        ok(tx(q['c'][j]) == fa, '%s c[%d] %-8s %-18r = %r' % (q['id'], j, mode, tx(q['c'][j]), fa))
    if len(set(keys)) != 4: err.append(q['id'] + ' recomputed values not all different: %s' % keys)
    if keys[0] not in tx(q['w']): err.append(q['id'] + ' answer %s not in w' % keys[0])
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')
    for g_ in c.values():
        if not re.search(r'(?<![\d.])' + re.escape(g_) + r'(?![\d])', tx(q['q']) + ' ' + ' '.join(tx(x) for f in q.get('f', []) for r in f.get('rows', []) for x in r)):
            err.append('%s given %s not in stem/table' % (q['id'], g_))
for sub in ('What is K for the reverse reaction', 'What is K for CH4(g) + 2 H2S(g)'):
    q = by(sub)
    if not q: continue
    checked.add(q['id']); t = tx(q['q']); k0 = re.search(r'K = ([\d.]+) for', t).group(1); n = sf(k0)
    e1, e2 = stem_eq(q, 0), stem_eq(q, 1)
    ok(e1[0] == e2[-1] and e1[-1] == e2[0], '%s second equation is the first reversed' % q['id'])
    want = [fmt(1 / D(k0), n), k0, '-' + k0, fmt(1 - D(k0), n)]
    for x in (1 / D(k0), 1 - D(k0)):
        if tie(x, n): err.append('%s tie %s' % (q['id'], x))
    ok([tx(x) for x in q['c']] == want, '%s reverse K = 1/K: %s; distractors same K, -K, 1 - K' % (q['id'], want))
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')

# ---------- K size and ranking ----------
def Kclass(v): return 'mostly products' if v > 10 else 'mostly reactants' if v < D('0.1') else 'sizable amounts of both'
for sub in ('reaction has K = 3.7 x 10^8', 'reaction has K = 2.1 x 10^-12'):
    q = by(sub)
    if not q: continue
    checked.add(q['id']); v = num_in(re.search(r'K = ([\d.]+ x 10\^-?\d+)', tx(q['q'])).group(1))
    ok(plain(q['c'][0]).startswith(Kclass(v)) and not any(plain(c).startswith(Kclass(v)) for c in q['c'][1:]),
       '%s K = %s -> %s (lead convention: K > 1 products, < 1 reactants, ~0.1-10 both)' % (q['id'], v, Kclass(v)))
q = by('contains the largest share of reactants')
if q:
    checked.add(q['id']); vals = [num_in(tx(c)[4:]) for c in q['c']]
    ok(vals.index(min(vals)) == 0, '%s smallest K is c[0]: %s' % (q['id'], vals))

# ---------- energy diagrams ----------
def sgn(v): return ('+%d' % v) if v > 0 else ('-%d' % -v)
def EaDH(q, r, top, p):
    t = tx(q['q'])
    if 'activation energy' in t or 'How much energy must a collision have' in t:
        want = ['%d kJ' % (top - r), '%d kJ' % (top - p), '%d kJ' % top, '%d kJ' % abs(p - r)]
        lab = 'Ea = top - reactants; distractors from products, top, |dH|'
    else:
        cls = lambda v: 'endothermic' if v > 0 else 'exothermic'
        want = ['%s kJ, %s' % (sgn(v), cls(v)) for v in (p - r, r - p, top - r, p - top)]
        lab = 'dH = products - reactants; distractors reversed, Ea, products - top'
    ok([tx(c) for c in q['c']] == want, '%s %s: %s' % (q['id'], lab, want))
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')
    checked.add(q['id'])
for q in ALL:
    t = tx(q['q'])
    m = re.search(r'reactants at (\d+) kJ,? (?:and )?the products at (\d+) kJ,? (?:and|with) the peak of the hill at (\d+) kJ', t)
    if m: EaDH(q, int(m.group(1)), int(m.group(3)), int(m.group(2)))
    elif q.get('f') and q['f'][0]['type'] == 'plot' and 'energy diagram' in t:
        f = q['f'][0]; ys = [pt[1] for pt in f['series'][0]['pts']]; r, top, p = ys[0], max(ys), ys[-1]
        labs = [mk[2] for mk in f['marks']]
        ok(labs == ['Reactants %d kJ' % r, '%d kJ' % top, 'Products %d kJ' % p] and sorted(h['y'] for h in f['hlines']) == sorted([r, top, p]),
           '%s figure marks match the curve (reactants %d, top %d, products %d)' % (q['id'], r, top, p))
        EaDH(q, int(r), int(top), int(p))

# ---------- rates key tables ----------
print('Rate items checked against key tables')
RATE = [(r'dilut', -1), (r'more concentrated', +1), (r'warm', +1), (r'refrigerator|ice|cool|cold', -1), (r'small pieces|powder', +1), (r'single thick', -1),
        (r'catalyst|enzyme', +1), (r'less yeast', -1)]
def rate_eff(c):
    for pat, v in RATE:
        if re.search(pat, plain(c)): return v
    return None
def chk(sub, cond, msg):
    q = by(sub)
    if q: checked.add(q['id']); ok(cond(q), '%s %s' % (q['id'], msg))
chk('Which change would make the reaction faster', lambda q: [rate_eff(c) for c in q['c']] == [1, -1, -1, -1], 'only more surface area speeds it (dilute, ice bath, thick strip slow)')
chk('Which change makes the dough rise faster', lambda q: [rate_eff(c) for c in q['c']] == [1, -1, -1, -1], 'only warming speeds (cold, less enzyme slow)')
def _ea(q):
    a, b = [int(x) for x in re.findall(r'Ea = (\d+) kJ', tx(q['q']))]
    return plain(q['c'][0]).startswith('reaction %s is faster' % ('a' if a < b else 'b'))
chk('reaction A has Ea = 24 kJ', _ea, 'lower Ea -> faster')
def _enz(q):
    rows = [(int(r[0]), D(r[1])) for r in q['f'][0]['rows']]; t_max = max(rows, key=lambda r: r[1])[0]
    after = [r[1] for r in rows if r[0] >= t_max]
    return t_max == 37 and all(after[i] > after[i + 1] for i in range(len(after) - 1)) and 'denature' in plain(q['c'][0]) and '37' in tx(q['q'])
chk('relative rate of a reaction catalyzed by a human enzyme', _enz, 'table optimum 37 °C, falls after; key = denaturing')
chk('A blood sample is cooled from 37 °C to 27 °C', lambda q: D(2) ** ((27 - 37) / D(10)) == D('0.5') and plain(q['c'][0]) == 'about half as fast', '27 vs 37 °C: one halving')
chk('moved into a container half the size', lambda q: plain(q['c'][0]).startswith('faster, because the molecules are more crowded'), 'higher concentration -> faster (more collisions)')

# ---------- dynamic key tables ----------
print('Dynamic-equilibrium items checked against key tables')
def first_flat(seq):
    for i in range(len(seq)):
        if all(v == seq[i][1] for _, v in seq[i:]): return seq[i][0]
def _readings(q):
    t = tx(q['q']); rd = [(int(b), D(a)) for a, b in re.findall(r'([\d.]+) M at (\d+) (?:min|s)', t)]
    unit = re.search(r'M at \d+ (min|s)', t).group(1)
    return plain(q['c'][0]) == '%d %s' % (first_flat(rd), unit)
chk('The [COCl2] readings were', _readings, 'first reading after which [COCl2] is constant')
chk('The [NOBr] readings were', _readings, 'first reading after which [NOBr] is constant')
def _plot(q):
    s = q['f'][0]['series']; A_, B_ = s[0]['pts'], s[1]['pts']
    flat = max(first_flat([(t, D(str(v))) for t, v in A_]), first_flat([(t, D(str(v))) for t, v in B_]))
    for (t1, a1), (t2, a2), (_, b1), (_, b2) in zip(A_, A_[1:], B_, B_[1:]):
        if (a1 - b1) * (a2 - b2) < 0: cross = t1 + (t2 - t1) * (a1 - b1) / ((a1 - b1) - (a2 - b2))
    sums = {round(a + b, 6) for (_, a), (_, b) in zip(A_, B_)}
    return (plain(q['c'][0]).startswith('at about %d s, when both curves become flat' % flat) and
            plain(q['c'][1]).startswith('at about %d s, where the two curves cross' % round(cross)) and sums == {1.0})
chk('The graph shows [A] and [B] over time', _plot, 'equilibrium where both curves go flat; distractor at the crossing; [A] + [B] constant (A <=> B)')
def _rev(q):
    e = stem_eq(q); res = []
    for c in q['c']:
        p, _ = parse_eq(tx(c)); res.append(p[0] == e[-1] and p[-1] == e[0])
    return res == [True, False, False, False]
chk('Write the reverse reaction for', _rev, 'only c[0] is the stem equation read right to left (same coefficients and phases)')

# ---------- Le Chatelier key table ----------
print('Le Chatelier items: expected shift computed from the stem equation; every choice claim checked')
def dH_sign(q):
    t = tx(q['q'])
    m = re.search(r'ΔH = ([+-])', t)
    if m: return 1 if m.group(1) == '+' else -1
    if re.search(r'endothermic|ΔH positive', t): return 1
    if 'exothermic' in t: return -1
    return None
def where(parts, f):
    for i, S_ in enumerate(parts):
        for co, ff, ph, ch in S_:
            if ff == f: return i, ph
    raise KeyError(f)
def gas(S_): return sum(co for co, f, ph, ch in S_ if ph == 'g')
def effects(q, stress, parts):
    """returns (shift, K effect, species effect function)."""
    kind = stress[0]; last = len(parts) - 1
    if kind in ('add', 'remove'):
        i, ph = where(parts, stress[1]); sgn_ = 1 if kind == 'add' else -1
        s = 0 if ph in ('s', 'l') else (sgn_ if i == 0 else -sgn_ if i == last else None)
        Ke = 0
    elif kind == 'T':
        s = stress[1] * dH_sign(q); Ke = s
    elif kind == 'V':
        a, b = gas(parts[0]), gas(parts[-1]); toward_fewer = (1 if a > b else -1 if a < b else 0)
        s = toward_fewer if stress[1] < 0 else -toward_fewer; Ke = 0
    else:
        s = 0; Ke = 0
    def spe(f):
        if kind in ('add', 'remove') and f == stress[1]: return 1 if kind == 'add' else -1
        i, ph = where(parts, f)
        if ph in ('s', 'l'): return None
        return -s if i == 0 else s
    return s, Ke, spe
COLOR = {'a deeper blue': 'Cu(NH3)4^2+', 'paler blue': 'Cu(H2O)4^2+'}
def claims(c):
    t = tx(c); lo = t.lower(); cl = []
    m = re.match(r'(?:shifts )?(right|left)\b', lo)
    if m: cl.append(('dir', 1 if m.group(1) == 'right' else -1))
    elif lo.startswith('no shift'): cl.append(('dir', 0))
    m = re.search(r'\bK (increases|decreases|does not change)', t)
    if m: cl.append(('K', {'increases': 1, 'decreases': -1, 'does not change': 0}[m.group(1)]))
    for f, v in re.findall(r'\[([^\]]+)\] (increases|decreases|does not change)', t):
        cl.append(('sp', f, {'increases': 1, 'decreases': -1, 'does not change': 0}[v]))
    m = re.search(r'pH (rises|falls)', t)
    if m: cl.append(('pH', 1 if m.group(1) == 'rises' else -1))
    m = re.search(r'turns (a deeper blue|paler blue)', lo)
    if m: cl.append(('sp', COLOR[m.group(1)], 1))
    return cl
def true_claim(cl, s, Ke, spe):
    if cl[0] == 'dir': return cl[1] == s
    if cl[0] == 'K': return cl[1] == Ke
    if cl[0] == 'sp': return spe(cl[1]) == cl[2]
    if cl[0] == 'pH': return -spe('H^+') == cl[1]
LC = [('More O2 is added to this mixture', ('add', 'O2')), ('In a hydrogen plant', ('remove', 'CO2')),
      ('Extra steam, H2O(g), is added', ('add', 'H2O')), ('Some Cl2 is removed', ('remove', 'Cl2')),
      ('Some NO2 is added', ('add', 'NO2')), ('More powdered carbon', ('add', 'C')), ('More ammonia solution is added', ('add', 'NH3')),
      ('The mixture is heated. Which', ('T', 1)), ('The temperature is lowered', ('T', -1)), ('placed in warm water', ('T', 1)),
      ('decreased (the pressure is increased)', ('V', -1)), ('decreased for this mixture at equilibrium: H2(g) + Br2(g)', ('V', -1)),
      ('The volume of the container is increased', ('V', 1)), ('volume of the sealed container is decreased', ('V', -1)),
      ('Argon gas is added', ('inert',)), ('platinum catalyst', ('cat',)), ('In the alveoli of the lungs', ('add', 'O2')),
      ('gasoline generator in a closed garage', ('add', 'CO')), ('During a panic attack', ('remove', 'CO2')), ('severe COPD', ('add', 'CO2')),
      ('A toothpaste supplies extra', ('add', 'Ca^2+')), ('fluoride varnish', ('add', 'F^-')),
      ('Steam, H2O(g), is added', ('add', 'H2O')), ('through a membrane that only H2', ('remove', 'H2')), ('Extra COCl2 is added', ('add', 'COCl2')),
      ('More solid NaHCO3', ('add', 'NaHCO3')), ('nickel carbonyl gas is carried away', ('remove', 'Ni(CO)4')), ('The mixture is cooled', ('T', -1)),
      ('reverse water–gas shift', ('T', 1)), ('heat of an oven', ('T', 1)),
      ('decreased for this mixture at equilibrium: CO(g) + H2O(g)', ('V', -1)), ('decreased for this mixture at equilibrium: 2 H2S(g)', ('V', -1)),
      ('Nitrogen gas, which does not react', ('inert',)), ('Activated carbon, the catalyst', ('cat',)), ('iron-deficiency anemia', ('remove', 'Hb')),
      ('broken ribs takes only shallow breaths', ('add', 'CO2')), ('sodium bicarbonate is given by IV', ('add', 'HCO3^-'))]
for sub, st in LC:
    q = by(sub)
    if not q: continue
    checked.add(q['id']); e = stem_eq(q)
    if st[0] == 'T' and dH_sign(q) is None: err.append(q['id'] + ' temperature item without a sign of ΔH'); continue
    s, Ke, spe = effects(q, st, e)
    res = []
    for j, c in enumerate(q['c']):
        cl = claims(c)
        if not cl: err.append('%s c[%d] makes no checkable claim: %r' % (q['id'], j, tx(c))); res.append(None); continue
        res.append(all(true_claim(x, s, Ke, spe) for x in cl))
    ok(res == [True, False, False, False], '%s %-22s -> shift %+d, K %+d; choices %s' % (q['id'], '%s %s' % st if len(st) > 1 else st[0], s, Ke, res))
# stress-choice items: each choice is a stress; exactly the key meets the target
def target_ok(q, st, parts, tgt):
    s, Ke, spe = effects(q, st, parts)
    return {'K': Ke != 0, 'right': s == 1}.get(tgt[0], None) if len(tgt) == 1 else spe(tgt[1]) == tgt[2] and s != 0
SC = [('Which change alters the value of K', ('K',), [('T', 1), ('add', 'CO'), ('V', -1), ('cat',)]),
      ('toward demineralization (dissolving)', ('right',), [('remove', 'OH^-'), ('add', 'Ca^2+'), ('add', 'PO4^3-'), ('add', 'Ca^2+')]),
      ('increases the amount of NOCl at equilibrium', ('sp', 'NOCl', 1), [('V', -1), ('T', 1), ('cat',), ('remove', 'Cl2')])]
for sub, tgt, sts in SC:
    q = by(sub)
    if not q: continue
    checked.add(q['id']); e = stem_eq(q)
    res = [target_ok(q, st, e, tgt) for st in sts]
    ok(res == [True, False, False, False], '%s stress-choice target %s: %s' % (q['id'], tgt, res))
chk('How is heat written into this equation', lambda q: dH_sign(q) == 1 and plain(q['c'][0]).startswith('heat +') and '+ heat' in plain(q['c'][1]),
    'ΔH > 0: heat is a reactant (left)')
def _haber(q):
    s, Ke, spe = effects(q, ('T', -1), stem_eq(q))
    return s == 1 and Ke == 1 and 'too slow' in plain(q['c'][0])
chk('Ammonia plants run the exothermic Haber process', _haber, 'exothermic: cooling favors NH3 (computed), so the reason is the rate')

# ---------- course rule: trailing zeros in calculation stems ----------
print('Trailing-zero rule in calculation stems; every k=1 item recomputed')
for q in ALL:
    if q['k'] == 1:
        s = re.sub(r'<sub>\d+</sub>', '', q['q']); s = tx(s)
        s = re.sub(EQRE, '', s)
        for m in re.finditer(r'(?<![\d.^,])(\d*[1-9]\d*0)(?![\d.^,])', s):
            err.append(q['id'] + ' calculation stem has ambiguous trailing-zero value %r' % m.group(1))
        if q['id'] not in checked: err.append(q['id'] + ' calculation item not recomputed')
for q in ALL:
    if q['id'] not in checked: hand.add(q['id'])

# ---------- draft overlap ----------
print('Draft overlap: no stem reuses a worked example or exercise from drafts/ch13')
GIV = r'(-?\d+\.\d+|\d+\.|\d+)(?: x 10\^(-?\d+))? ?(M|kJ|°C|s|min|mmHg|atm|%)(?![A-Za-z/])'
CONST = {'1', '2', '3', '4', '5', '10', '25', '37', '0', '100', '7.35', '7.45', '35', '45', '0.1'}
def givens_in(t): return {(a + ('e' + b if b else ''), u) for a, b, u in re.findall(GIV, t) if a not in CONST}
def norm_eq(parts): return tuple(tuple(sorted((co, f, ph) for co, f, ph, ch in S_)) for S_ in parts)
blocks, BANNED, DEQ, PEQ = [], set(), {}, {}
for p_ in sorted(glob.glob(os.path.join(ROOT, 'drafts', 'ch13', '*.html'))):
    h = open(p_, encoding='utf-8').read()
    for b in re.split(r'(?=Example \\\(\\PageIndex|Exercise \\\(\\PageIndex|<h2|Problem 13\.\d+\b)', h):
        if not re.match(r'Example|Exercise|Problem', b): continue
        t = re.sub(r'\\\(|\\\)|\\dfrac|\\text|\\times|\\ |\\qquad|\\left|\\right|\\cdot|\\,|\\;|\\rightleftharpoons', ' ', b)
        t = tx(re.sub(r'[{}]', ' ', t)).replace('{}^\\circ', '°')
        nm = os.path.basename(p_) + ' ' + ' '.join(t.split()[:3])
        g_ = givens_in(t); BANNED |= g_
        blocks.append((nm, g_, t.split(' Answer')[0]))
        for s_, (parts, ar) in eqs_in(b):
            if '13.6_' in nm: PEQ.setdefault(norm_eq(parts), nm)
            else: DEQ[norm_eq(parts)] = nm
ALLOW_EQ = {'CO2(aq) + H2O(l) <=> H2CO3(aq) <=> H^+(aq) + HCO3^-(aq)', 'N2(g) + 3 H2(g) <=> 2 NH3(g)'}   # teaching equations the task asks for
W = lambda s_: set(w for w in re.findall(r'[a-z0-9.]+', s_.lower()) if len(w) > 2)
nover = 0; notes = []; peq_notes = []
for q in ALL:
    qt = tx(q['q']); qg = givens_in(qt); qw = W(qt)
    for g_ in sorted(qg & BANNED):
        nover += 1; err.append('%s uses the draft worked-example given %s %s' % (q['id'], *g_))
    for s_, (parts, ar) in eqs_in(q['q']):
        if norm_eq(parts) in DEQ and s_ not in ALLOW_EQ:
            nover += 1; err.append('%s stem equation %s is a draft example/exercise equation (%s)' % (q['id'], s_, DEQ[norm_eq(parts)]))
        elif norm_eq(parts) in PEQ:
            peq_notes.append('%s shares the equation %s with %s' % (q['id'], s_, PEQ[norm_eq(parts)]))
    for nm, gs, bt in blocks:
        bw = W(bt); j = len(qw & bw) / max(1, len(qw | bw))
        if j > 0.45: nover += 1; err.append('%s stem is %.2f similar to %s' % (q['id'], j, nm))
        elif j > 0.3: notes.append('%s stem %.2f similar to %s (checked by hand)' % (q['id'], j, nm))
print('    %d draft example/exercise blocks compared, %d draft givens, %d draft equations; %d overlaps' % (len(blocks), len(BANNED), len(DEQ), nover))
for n_ in notes: print('    NOTE', n_)
print('    %d items share an equation with a 13.6 practice problem (different task or numbers; read by hand):' % len(peq_notes))
for n_ in peq_notes: print('      ', n_)
p6 = os.path.join(ROOT, 'drafts', 'ch13', '13.6_practice_problems.html')
print('    13.6 practice problems:', 'compared above' if os.path.exists(p6) else 'not written yet (rerun after it exists)')

# ---------- Mateo, coverage, counts, duplicates ----------
mateo = [q['id'] for q in ALL if 'Mateo' in q['q'] + ' '.join(q['y']) + q['w'] + q['h'] + ' '.join(q['c'])]
if len(mateo) > 2: err.append('Mateo appears in %d items (max 2): %s' % (len(mateo), mateo))
print('Mateo items:', mateo)
print('Items with a machine check: %d of %d' % (len(checked), len(ALL)))
print('  conceptual (key read by hand; equations and quoted values still checked):', ' '.join(sorted(hand)) or 'none')
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
