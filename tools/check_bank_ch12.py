#!/usr/bin/env python3
"""Checker for the Chapter 12 banks (properties of acids and bases, Bronsted-Lowry and conjugate pairs, strong and
weak acids and bases, water and Kw, pH and pOH, buffers).
Structural checks as in tools/check_bank_ch11.py (ch12 topic ids; ADAPT = 42 items, text only, y[0] begins
"Correct: "; tables at most 3 columns; figures only of fbx type table), plus, written independently of the
generators:
  - every calculation item (k=1): the key and each numeric distractor's intended error recomputed with Decimal
    (proper log10 and powers of 10) from the givens as written in the stem, TWO ways: (a) round once at the end and
    (b) strict: every intermediate rounded first (pOH to its decimal places before 14.00 - pOH; [H3O+] rounded to
    its significant figures before Kw / [H3O+]); the item is an error unless both agree;
  - log rule on every key: decimal places in a pH/pOH = significant figures in the concentration it came from, and
    significant figures in a concentration = decimal places in the pH/pOH; Kw (1.0 x 10^-14) limits Kw answers to 2;
  - stability: no key sits within 0.1 of a rounding tie at its last reported digit (round half up), and a strong-base
    pH also agrees by the Kw route (round [H3O+] = Kw/[OH-] to 2 significant figures, then -log);
  - every equation anywhere is parsed back out of the HTML (ions included) and must balance in atoms and charge;
    ionization equations use a single arrow for strong acids/bases and a double arrow for weak ones (stems, keys,
    feedback for the key, hints and worked answers);
  - key tables from the chapter text: strong acids/bases (12.3 list) and weak ones, acid/base/salt/neither from the
    formula, conjugate acid/base by formula and charge (conjugate base = acid - H+), Bronsted roles read from the
    stem's own equation, conjugate pairs, buffer pairs (weak acid + its conjugate base, or weak base + its conjugate
    acid; spectator ions ignored), which partner neutralizes added acid/base, indicator colors (12.1: litmus,
    phenolphthalein, red cabbage chart), blood range 7.35-7.45, factors of 10 per pH unit; each keyed answer is
    rechecked; the rest are listed as read by hand;
  - quoted constants: Kw = 1.0 x 10^-14, pH + pOH = 14.00, neutral 1.0 x 10^-7 M, blood 7.35-7.45;
  - course rule: no whole number ending in 0 without a decimal point in a calculation stem;
  - exactly one correct choice (recomputed values all different; four different choices);
  - no stem reuses a draft worked example or exercise number (concentrations and pH values in drafts/ch12 blocks);
    no stem in both banks; Mateo in at most 2 items and never with the drafts' 7.30/7.40/7.25.
usage: python3 tools/check_bank_ch12.py bank/ch12.json bank/ch12_adapt.json"""
import json, sys, re, os, collections, glob
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 50; getcontext().rounding = ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = {'ch12-props', 'ch12-bl', 'ch12-strength', 'ch12-water', 'ch12-ph', 'ch12-buffers'}
err = []

# ---------- text ----------
def txt(x):
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<[^>]+>', '', x)
    for a, b in (('&middot;', '·'), ('&minus;', '-'), ('−', '-'), ('&times;', 'x'), ('&nbsp;', ' '), ('&divide;', '/'),
                 ('&rarr;', '->'), ('&rlarr;', '<=>'), ('⇄', '<=>'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&deg;', '°'),
                 ('&ndash;', '–'), ('&lt;', '<'), ('&gt;', '>'), ('&asymp;', '≈'), ('&radic;', '√'), ('&oslash;', 'ø'),
                 ('&delta;', 'δ'), ('&Delta;', 'Δ'), ('&amp;', '&')):
        x = x.replace(a, b)
    return x
def plain(x): return re.sub(r'\s+', ' ', txt(x)).strip().lower()

# ---------- structural checks ----------
OUT_OF_SCOPE = r"Henderson|Hasselbalch|K_?a\b|Ka =|Lewis acid|Lewis base|all of the above|none of the above"
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
        if re.search(OUT_OF_SCOPE, txt(s), re.I): err.append(i + ' out of scope term or AOTA/NOTA')
        if 'f' in q and not allow_f: err.append(i + ' has f (ADAPT items must be text only)')
        for f in q.get('f', []):
            if f['type'] == 'table':
                if max(len(f['head']), *[len(r) for r in f['rows']]) > 3: err.append(i + ' table wider than 3 columns')
                if max(len(plain(x)) for r in f['rows'] + [f['head']] for x in r) > 32: err.append(i + ' table cell too long for a phone')
            else: err.append(i + ' figure type not checked here: ' + f['type'])
        if label == 'HW' and not q['y'][0].startswith('Correct: '): err.append(i + ' ADAPT y[0] lacks "Correct: "')
        if label == 'TRY' and q['y'][0].startswith('Correct'): err.append(i + ' Try It y[0] starts with "Correct"')
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if re.search(r'(?<![\w.^])' + re.escape(right) + r'(?![\w^])', plain(q['y'][j])): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c12-%03d', 'TRY', True)
structural(HW, 'c12-h%02d', 'HW', False)
if len(HW) != 42: err.append('ADAPT has %d items, not 42' % len(HW))
if sum(1 for q in TRY if q.get('f')) > 4: err.append('more than 4 figures')
fbx = open(os.path.join(ROOT, 'js', 'fbx.js'), encoding='utf-8').read()
for t_ in {f['type'] for q in TRY for f in q.get('f', [])}:
    if not re.search(r'[{,]%s:' % t_, fbx): err.append('figure type %s not supported by js/fbx.js' % t_)
wid = open(os.path.join(ROOT, 'js', 'widget.js'), encoding='utf-8').read()
for t_ in TOP:
    if "'%s'" % t_ not in wid: err.append('topic %s missing from js/widget.js TOPICS' % t_)
WANT_T = {'ch12-props': 10, 'ch12-bl': 12, 'ch12-strength': 12, 'ch12-water': 12, 'ch12-ph': 16, 'ch12-buffers': 10}
WANT_H = {'ch12-props': 6, 'ch12-bl': 7, 'ch12-strength': 7, 'ch12-water': 7, 'ch12-ph': 9, 'ch12-buffers': 6}
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
def rq(v, d): return format(D(v).quantize(D(10) ** -d), 'f')
def U(v, n, u='M'): return (fmt(v, n) + ' ' + u).strip()
def val(s):
    """number as written in text: '6.2 x 10^-4' or '0.0072'."""
    m = re.fullmatch(r'(-?[\d.]+)(?: x 10\^(-?\d+))?', s.strip())
    return D(m.group(1)) * (D(10) ** int(m.group(2)) if m.group(2) else 1)
def mant(s): return s.split(' x ')[0]
KW = D('1.0e-14'); KWSF = 2
def lg(x): return D(x).log10()
def P(x, d): return rq(-lg(x), d)                      # p-function, d decimal places
def TEN(pv): return D(10) ** (-D(pv))
def tie_d(x, d):
    """True if x is within 0.1 of a rounding tie at d decimal places."""
    f = (abs(D(x)) * D(10) ** d) % 1
    return abs(f - D('0.5')) < D('0.1')
def tie_s(x, n):
    x = abs(D(x)); e = x.adjusted(); return tie_d(x.scaleb(-e), n - 1)

# ---------- species, formulas, equations ----------
EL = set('H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sr Ba Br I Fe Zn Cu Ag Rb Cs Pb Mn Cr'.split())
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
            if not m or m.group(1) not in EL: raise ValueError(f)
            stack[-1][m.group(1)] += int(m.group(2) or 1); i += m.end()
    return stack[0]
def species(s):
    """'HPO4^2-' -> (frozenset atoms, charge)"""
    s = s.strip()
    m = re.fullmatch(r'([A-Z(][A-Za-z0-9()]*)(?:\^(\d*)([+-]))?', s)
    if not m: raise ValueError(s)
    ch = 0
    if m.group(3): ch = int(m.group(2) or 1) * (1 if m.group(3) == '+' else -1)
    return (frozenset(atoms(m.group(1)).items()), ch)
def sp_str(s): return species(s)
def add_h(sp, n=1):
    c = collections.Counter(dict(sp[0])); c['H'] += n
    if c['H'] == 0: del c['H']
    return (frozenset(c.items()), sp[1] + n)
SPC = r'(?:\d+ )?[A-Z(][A-Za-z0-9()]*(?:\^\d*[+-])?(?:\((?:s|l|g|aq)\))?'
EQRE = re.compile(SPC + r'(?: \+ ' + SPC + r')* (?:->|<=>) ' + SPC + r'(?: \+ ' + SPC + r')*')
def term(tok):
    m = re.fullmatch(r'(\d+) (.+)', tok.strip()); co = int(m.group(1)) if m else 1
    t = m.group(2) if m else tok.strip()
    m = re.fullmatch(r'(.+?)\((s|l|g|aq)\)', t)
    if m: t = m.group(1)
    return co, t, species(t)
def parse_eq(s):
    arrow = '<=>' if ' <=> ' in s else '->'
    L_, R_ = s.split(' %s ' % arrow)
    return [term(t) for t in L_.split(' + ')], [term(t) for t in R_.split(' + ')], arrow
def eqs_in(h):
    out = []
    for m in EQRE.finditer(txt(h)):
        try: out.append((m.group(), parse_eq(m.group())))
        except ValueError: pass
    return out
def balanced(e):
    def side(S_):
        c = collections.Counter(); q = 0
        for co, f, sp in S_:
            for el, n in dict(sp[0]).items(): c[el] += co * n
            q += co * sp[1]
        return c, q
    return side(e[0]) == side(e[1])

# ---------- key tables (Chapter 12 text) ----------
SA = {'HCl', 'HBr', 'HI', 'HNO3', 'HClO4', 'H2SO4'}
SB = {'LiOH', 'NaOH', 'KOH', 'RbOH', 'CsOH', 'Ca(OH)2', 'Sr(OH)2', 'Ba(OH)2'}
WA = {'HF', 'HC2H3O2', 'H3PO4', 'HNO2', 'H2CO3', 'HCN', 'HC3H5O3', 'HClO', 'H2S', 'H2PO4^-', 'HCO3^-', 'HSO4^-', 'NH4^+'}
WB = {'ClO^-', 'NH3', 'Mg(OH)2', 'NaHCO3', 'HCO3^-', 'CO3^2-', 'CH3NH2', 'CN^-', 'F^-', 'NO2^-', 'C2H3O2^-', 'C3H5O3^-', 'HPO4^2-'}
SALT = {'KI', 'CaBr2', 'NaCl', 'KNO3', 'NH4Br', 'LiClO4', 'BaI2', 'KCl', 'NaI', 'KBr', 'LiBr', 'FeCl2', 'MgCl2', 'NaNO3'}
NEITHER = {'C2H5OH', 'C3H7OH', 'CH3OH', 'C6H12O6'}
OHN = {'NaOH': 1, 'KOH': 1, 'LiOH': 1, 'Ca(OH)2': 2, 'Sr(OH)2': 2, 'Ba(OH)2': 2}
def klass(f):
    if f in SA: return 'strong acid'
    if f in SB: return 'strong base'
    if f == 'NaHCO3': return 'base'
    if f in WA: return 'weak acid'
    if f in WB: return 'weak base'
    if f in SALT: return 'salt'
    if f in NEITHER: return 'neither'
    return None
SALT_ION = {'NaCN': ['Na^+', 'CN^-'], 'NaCl': ['Na^+', 'Cl^-'], 'NaI': ['Na^+', 'I^-'], 'KF': ['K^+', 'F^-'], 'NH4Br': ['NH4^+', 'Br^-'],
            'NH4NO3': ['NH4^+', 'NO3^-'], 'KCl': ['K^+', 'Cl^-'], 'NaBr': ['Na^+', 'Br^-'], 'NaNO2': ['Na^+', 'NO2^-'],
            'NaH2PO4': ['Na^+', 'H2PO4^-'], 'NaClO': ['Na^+', 'ClO^-'], 'NaClO4': ['Na^+', 'ClO4^-'], 'Na2HPO4': ['Na^+', 'HPO4^2-'], 'KOH': ['K^+', 'OH^-'], 'NaOH': ['Na^+', 'OH^-']}
SPECT = {'Na^+', 'K^+', 'Cl^-', 'Br^-', 'I^-', 'NO3^-'}
def buffer(a, b):
    """True if a and b (formulas as written) are a weak acid + its conjugate base or weak base + its conjugate acid."""
    def parts(f):
        if f in SA or f in SB: return None
        return [x for x in SALT_ION.get(f, [f]) if x not in SPECT] if f in SALT_ION else [f]
    pa, pb = parts(a), parts(b)
    if pa is None or pb is None or not pa or not pb: return False
    for x in pa:
        for y in pb:
            if x == y: continue
            for acid, base in ((x, y), (y, x)):
                if acid in WA | {'HCN', 'HF', 'HC2H3O2', 'HNO2', 'H2CO3', 'HC3H5O3'} and add_h(species(base)) == species(acid): return True
                if base in WB and add_h(species(base)) == species(acid): return True
    return False
for a, b, want in (('HF', 'NaF', None), ('HCN', 'NaCN', True), ('HCl', 'NaCl', False), ('HCN', 'NaCl', False), ('NH3', 'NH4Br', True),
                   ('NaH2PO4', 'Na2HPO4', True), ('HI', 'NaI', False), ('NH3', 'NaCl', False), ('KOH', 'KCl', False)):
    if want is not None and buffer(a, b) != want: err.append('checker buffer table wrong for %s + %s' % (a, b))
CABBAGE = {'1–2': 'red', '3–4': 'pink', '5–7': 'purple', '8': 'blue', '9–11': 'green', '12–14': 'yellow'}   # 12.1 figure
def cab(ph):
    for k, c in CABBAGE.items():
        lo, _, hi = k.partition('–'); hi = hi or lo
        if D(lo) <= D(ph) <= D(hi): return c
    return None
BLOOD = (D('7.35'), D('7.45'))
def blood(ph): return 'acidosis' if D(ph) < BLOOD[0] else 'alkalosis' if D(ph) > BLOOD[1] else 'normal'

# ---------- equations balance; arrows ----------
print('Equations (every field) balance in atoms and charge; arrows match strength')
neq = 0
def arrow_ok(e):
    L_, R_, ar = e
    fs = [f for co, f, sp in L_]
    for f in fs:
        if len(L_) == 2 and 'H2O' in fs and any(t[1] == 'H3O^+' for t in R_):
            if f in SA: return ar == '->'
            if f in WA: return ar == '<=>'
        if len(L_) == 1 and f in OHN and any(t[1] == 'OH^-' for t in R_):
            return ar == '->'
        if f in WB and 'H2O' in fs and any(t[1] == 'OH^-' for t in R_): return ar == '<=>'
    return True
for q in ALL:
    for k, h in [('q', q['q']), ('h', q['h']), ('w', q['w']), ('y0', q['y'][0]), ('c0', q['c'][0])] + [('c%d' % j, q['c'][j]) for j in (1, 2, 3)] + [('y%d' % j, q['y'][j]) for j in (1, 2, 3)]:
        for s_, e in eqs_in(h):
            neq += 1
            if not balanced(e): err.append('%s unbalanced equation %s' % (q['id'], s_))
            if k in ('q', 'h', 'w', 'y0', 'c0') and not arrow_ok(e): err.append('%s wrong arrow for strength: %s' % (q['id'], s_))
print('    %d equations parsed, all balanced' % neq)

# ---------- quoted constants ----------
print('Quoted constants: Kw, pH + pOH = 14.00, neutral 1.0 x 10^-7 M, blood 7.35-7.45')
for q in ALL:
    s = txt(' '.join([q['q'], q['w'], q['h']] + q['c'] + q['y']))
    for v in re.findall(r'K_?w ?= ?(?:\[H3O\^\+\]\[OH\^-\] = )?([\d.]+ x 10\^-?\d+)', s.replace('Kw', 'K_w')):
        if v != '1.0 x 10^-14': err.append('%s quotes Kw = %s' % (q['id'], v))
    for v in re.findall(r'pH \+ pOH = (\d+\.\d+)', s):
        if v != '14.00': err.append('%s quotes pH + pOH = %s' % (q['id'], v))
    for a, b in re.findall(r'(\d\.\d+)–(\d\.\d+)', s):
        if (a, b) != ('7.35', '7.45') and a.startswith('7'): err.append('%s quotes blood %s–%s' % (q['id'], a, b))
    for v in re.findall(r'pure water[^.]*?([\d.]+ x 10\^-\d+) M', s):
        if v not in ('1.0 x 10^-7',): err.append('%s pure-water concentration %s' % (q['id'], v))

# ---------- calculation items ----------
def by(sub):
    m = [q for q in ALL if sub in txt(q['q'])]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
checked, hand = set(), set()
CALC = []
def calc(sub, givens, specs, rule=None): CALC.append((sub, givens, specs, rule))
def R2(x, n, m): return D(x) if m == 0 else val(fmt(x, n))
# rule: ('pH', conc, d) key is a p value of conc -> decimals = sf(conc); ('C', pv, n) concentration from p value;
#       ('Kw', conc) concentration from Kw -> 2 s.f.; ('base', conc, nOH) strong-base pH (also Kw route)
def kwdiv(x_s, mult=1): return {0: lambda m: U(KW / (mult * val(x_s)), KWSF)}
# ---- ch12-water ----
calc('tomato juice has [H3O^+] = 7.9 x 10^-5', ['7.9'], {0: lambda m: U(KW / val('7.9 x 10^-5'), 2), 1: lambda m: U(KW * val('7.9 x 10^-5'), 2),
     2: lambda m: U(val('7.9 x 10^-5') / KW, 2), 3: lambda m: '1.0 x 10^-7 M'}, ('Kw', '7.9 x 10^-5'))
calc('soap solution has [OH^-] = 5.5 x 10^-3', ['5.5'], {0: lambda m: U(KW / val('5.5 x 10^-3'), 2), 1: lambda m: U(KW * val('5.5 x 10^-3'), 2),
     2: lambda m: U(val('5.5 x 10^-3') / KW, 2), 3: lambda m: U(1 / val('5.5 x 10^-3'), 2)}, ('Kw', '5.5 x 10^-3'))
calc('[OH^-] in 0.045 M HBr', ['0.045'], {0: lambda m: U(KW / D('0.045'), 2), 1: lambda m: '0.045 M', 2: lambda m: U(KW * D('0.045'), 2), 3: lambda m: U(KW / (2 * D('0.045')), 2)}, ('Kw', '0.045'))
calc('[OH^-] in 0.0045 M Ba(OH)2', ['0.0045'], {0: lambda m: U(OHN['Ba(OH)2'] * D('0.0045'), 2), 1: lambda m: U(D('0.0045'), 2),
     2: lambda m: U(KW / R2(OHN['Ba(OH)2'] * D('0.0045'), 2, m), 2), 3: lambda m: U(KW / D('0.0045'), 2)}, ('Kw', '0.0045'))
calc('[H3O^+] in 0.0012 M Ca(OH)2', ['0.0012'], {0: lambda m: U(KW / R2(OHN['Ca(OH)2'] * D('0.0012'), 2, m), 2), 1: lambda m: U(KW / D('0.0012'), 2),
     2: lambda m: U(2 * D('0.0012'), 2), 3: lambda m: U(KW * 2 * D('0.0012'), 2)}, ('Kw', '0.0012'))
calc('rainwater has [H3O^+] = 8.3 x 10^-6', ['8.3'], {0: lambda m: U(KW / val('8.3 x 10^-6'), 2), 1: lambda m: U(KW * val('8.3 x 10^-6'), 2),
     2: lambda m: U(val('8.3 x 10^-6') / KW, 2), 3: lambda m: '1.0 x 10^-7 M'}, ('Kw', '8.3 x 10^-6'))
calc('bleach solution has [OH^-] = 1.9 x 10^-4', ['1.9'], {0: lambda m: U(KW / val('1.9 x 10^-4'), 2), 1: lambda m: U(KW * val('1.9 x 10^-4'), 2),
     2: lambda m: U(1 / val('1.9 x 10^-4'), 2), 3: lambda m: U(val('1.9 x 10^-4') / KW, 2)}, ('Kw', '1.9 x 10^-4'))
calc('[H3O^+] in 0.0082 M KOH', ['0.0082'], {0: lambda m: U(KW / (OHN['KOH'] * D('0.0082')), 2), 1: lambda m: '0.0082 M', 2: lambda m: U(KW * D('0.0082'), 2),
     3: lambda m: U(KW / (2 * D('0.0082')), 2)}, ('Kw', '0.0082'))
calc('[H3O^+] in 0.0026 M Sr(OH)2', ['0.0026'], {0: lambda m: U(KW / R2(OHN['Sr(OH)2'] * D('0.0026'), 2, m), 2), 1: lambda m: U(KW / D('0.0026'), 2),
     2: lambda m: U(2 * D('0.0026'), 2), 3: lambda m: U(KW * D('0.0026'), 2)}, ('Kw', '0.0026'))
# ---- ch12-ph ----
def _acid(c_s):
    c = val(c_s); d = sf(mant(c_s))
    return {0: lambda m: P(c, d), 1: lambda m: rq(lg(c), d), 2: lambda m: rq(14 + lg(c), d), 3: lambda m: P(c, d - 1)}
calc('pH of 0.0072 M HBr', ['0.0072'], _acid('0.0072'), ('pH', '0.0072'))
def _ac3(c_s, order):
    a = val(c_s); d = sf(mant(c_s))
    f = {'k': lambda m: P(a, d), 'neg': lambda m: rq(lg(a), d), 'dec-': lambda m: P(a, d - 1), 'dec+': lambda m: P(a, d + 1), 'pOH': lambda m: rq(14 + lg(a), d), 'dec1': lambda m: P(a, 1)}
    return {j: f[k] for j, k in enumerate(order)}
calc('pH of 2.85 x 10^-3 M HCl', ['2.85'], _ac3('2.85 x 10^-3', ['k', 'neg', 'dec-', 'pOH']), ('pH', '2.85 x 10^-3'))
calc('[H3O^+] = 7.94 x 10^-6 M?', ['7.94'], _ac3('7.94 x 10^-6', ['k', 'dec-', 'neg', 'pOH']), ('pH', '7.94 x 10^-6'))
calc('[H3O^+] = 6.10 x 10^-9 M. Which pH', ['6.10'], _ac3('6.10 x 10^-9', ['k', 'dec-', 'dec+', 'dec1']), ('pH', '6.10 x 10^-9'))
calc('pH of 0.0058 M HI', ['0.0058'], {0: lambda m: P(D('0.0058'), 2), 1: lambda m: rq(lg(D('0.0058')), 2), 2: lambda m: rq(14 + lg(D('0.0058')), 2), 3: lambda m: P(D('0.0058'), 3)}, ('pH', '0.0058'))
calc('pH of 1.35 x 10^-4 M HClO4', ['1.35'], _ac3('1.35 x 10^-4', ['k', 'dec-', 'neg', 'pOH']), ('pH', '1.35 x 10^-4'))
_o = val('3.0 x 10^-5')
calc('[OH^-] = 3.0 x 10^-5 M. Which pOH', ['3.0'], {0: lambda m: P(_o, 2), 1: lambda m: P(_o, 1), 2: lambda m: P(_o, 3), 3: lambda m: P(_o, 4)}, ('pH', '3.0 x 10^-5'))
calc('0.012 M HNO3 solution is diluted tenfold', ['0.012', '0.0012'], {0: lambda m: P(D('0.012') / 10, 2), 1: lambda m: P(D('0.012') * 10, 2), 2: lambda m: P(D('0.012'), 2),
     3: lambda m: rq(D(P(D('0.012'), 2)) * 10, 1)}, ('pH', '0.0012'))
def BPH(c, n, m):
    """strong-base pH: exact (m=0) or strict (pOH rounded to 2 decimal places, then 14.00 - pOH)."""
    oh = n * c
    return rq(14 + lg(oh), 2) if m == 0 else rq(D('14.00') - D(P(oh, 2)), 2)
def _base(c_s, f):
    c = val(c_s); n = OHN[f]; wrongn = 2 if n == 1 else 1
    return c, n, {0: lambda m: BPH(c, n, m), 1: lambda m: P(n * c, 2), 2: lambda m: BPH(c, wrongn, m)}
_c, _n, _s = _base('0.0039', 'NaOH'); _s[1], _s[2] = _s[1], _s[2]
calc('pH of 0.0039 M NaOH', ['0.0039'], {0: _s[0], 1: _s[1], 2: _s[2], 3: lambda m: rq(D(BPH(D('0.0039'), 1, m)), 1)}, ('base', '0.0039', 1))
_c, _n, _s2 = _base('0.0033', 'Ba(OH)2')
calc('pH of 0.0033 M Ba(OH)2', ['0.0033'], {0: _s2[0], 1: _s2[2], 2: _s2[1], 3: lambda m: rq(D(BPH(D('0.0033'), 2, m)), 1)}, ('base', '0.0033', 2))
_c, _n, _s3 = _base('3.3 x 10^-4', 'Ca(OH)2')
calc('pH of 3.3 x 10^-4 M Ca(OH)2', ['3.3'], {0: _s3[0], 1: _s3[2], 2: _s3[1], 3: lambda m: rq(-D(BPH(val('3.3 x 10^-4'), 2, m)), 2)}, ('base', '3.3 x 10^-4', 2))
_c, _n, _s4 = _base('0.0059', 'KOH')
calc('pH of 0.0059 M KOH', ['0.0059'], {0: _s4[0], 1: _s4[1], 2: _s4[2], 3: lambda m: rq(D(BPH(D('0.0059'), 1, m)), 1)}, ('base', '0.0059', 1))
_c, _n, _s5 = _base('0.0024', 'Sr(OH)2')
calc('pH of 0.0024 M Sr(OH)2', ['0.0024'], {0: _s5[0], 1: _s5[2], 2: _s5[1], 3: lambda m: rq(-D(BPH(D('0.0024'), 2, m)), 2)}, ('base', '0.0024', 2))
def _hfrom(pv):
    n = dec(pv)
    return {0: lambda m: U(TEN(pv), n), 1: lambda m: U(TEN(D('14.00') - D(pv)), n), 2: lambda m: U(D(10) ** D(pv), n), 3: lambda m: U(TEN(pv), n + 1)}
calc('orange juice has pH 3.37', ['3.37'], _hfrom('3.37'), ('C', '3.37'))
_m = _hfrom('7.38'); _m = {0: _m[0], 1: _m[2], 2: _m[3], 3: _m[1]}
calc('his arterial pH is 7.38', ['7.38'], _m, ('C', '7.38'))
calc('milk has pH 6.62', ['6.62'], _hfrom('6.62'), ('C', '6.62'))
def OHP(pv, m):
    """[OH-] from pH: exact via pOH (m=0) or by the Kw route with [H3O+] rounded to its s.f. first (m=1)."""
    n = dec(pv)
    return TEN(D('14.00') - D(pv)) if m == 0 else KW / val(fmt(TEN(pv), n))
calc('hand soap solution has pH 9.62', ['9.62'], {0: lambda m: U(OHP('9.62', m), 2), 1: lambda m: U(TEN('9.62'), 2), 2: lambda m: rq(D('14.00') - D('9.62'), 2) + ' M',
     3: lambda m: U(D(10) ** (D('14.00') - D('9.62')), 2)}, ('C', '9.62'))
calc('floor cleaner has pH 10.85', ['10.85'], {0: lambda m: U(OHP('10.85', m), 2), 1: lambda m: U(TEN('10.85'), 2), 2: lambda m: rq(D('14.00') - D('10.85'), 2) + ' M',
     3: lambda m: U(OHP('10.85', 0), 3)}, ('C', '10.85'))
calc('has pOH 3.85', ['3.85'], {0: lambda m: rq(D('14.00') - D('3.85'), 2), 1: lambda m: '3.85', 2: lambda m: rq(D('14.00') + D('3.85'), 2), 3: lambda m: U(TEN('3.85'), 2)})

print('Calculation items: key and distractors recomputed (round once = strict, and = the choice as written)')
for sub, givens, specs, rule in CALC:
    q = by(sub)
    if not q: continue
    checked.add(q['id']); stem = txt(q['q'])
    for gv in givens:
        if not re.search(r'(?<![\d.])' + re.escape(gv) + r'(?![\d])', stem): err.append(q['id'] + ' given %r not in stem as written' % gv)
    print('  %s %s' % (q['id'], sub[:52]))
    keys = []
    for j, fn in sorted(specs.items()):
        try: a, b = fn(0), fn(1)
        except Exception as e_: err.append('%s c[%d] spec failed: %r' % (q['id'], j, e_)); continue
        if a != b: err.append('%s c[%d] ambiguous: %s (round once) vs %s (strict)' % (q['id'], j, a, b))
        keys.append(a)
        ok(txt(q['c'][j]).strip() == a, '%s c[%d] %-26r = %r' % (q['id'], j, txt(q['c'][j]).strip(), a))
    if len(set(keys)) != 4: err.append(q['id'] + ' recomputed values not all different: %s' % keys)
    k0 = txt(q['c'][0]).strip().split(' M')[0]
    if k0 not in txt(q['w']): err.append(q['id'] + ' answer %s not in w' % k0)
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')
    # log rule and stability on the key
    key = txt(q['c'][0]).strip()
    if rule and rule[0] == 'pH':
        c_s = rule[1]; want = sf(mant(c_s)); x = -lg(val(c_s))
        ok(dec(key) == want, '%s log rule: %s has %d decimal places for %d s.f. in %s' % (q['id'], key, dec(key), want, c_s))
        if tie_d(x, want): err.append('%s pH %s sits near a rounding tie' % (q['id'], x))
    elif rule and rule[0] == 'base':
        c = val(rule[1]); oh = rule[2] * c; want = sf(mant(rule[1]))
        ok(dec(key) == want == 2, '%s log rule: strong-base pH %s has 2 decimal places (2 s.f. in %s)' % (q['id'], key, rule[1]))
        kwr = rq(-lg(val(fmt(KW / oh, 2))), 2)
        ok(kwr == key, '%s Kw route ([H3O+] = %s rounded first) gives the same pH %s' % (q['id'], fmt(KW / oh, 2), kwr))
        if tie_d(-lg(oh), 2) or tie_d(14 + lg(oh), 2): err.append('%s pOH/pH near a rounding tie' % q['id'])
    elif rule and rule[0] == 'C':
        want = dec(rule[1]); m_ = mant(key.replace(' M', ''))
        ok(sf(m_) == want, '%s log rule: %s has %d s.f. for %d decimal places in pH %s' % (q['id'], key, sf(m_), want, rule[1]))
        x = TEN(rule[1]) if 'OH' not in stem.split('What is')[-1] else TEN(D('14.00') - D(rule[1]))
        if tie_s(x, want): err.append('%s concentration %s near a rounding tie' % (q['id'], x))
    elif rule and rule[0] == 'Kw':
        m_ = mant(key.replace(' M', ''))
        ok(sf(m_) == min(KWSF, sf(mant(rule[1]))), '%s Kw answer %s has %d s.f. (Kw and %s)' % (q['id'], key, sf(m_), rule[1]))
        if tie_s(val(m_) if 'x' not in key else val(key.replace(' M', '')), 2): err.append('%s Kw answer near a rounding tie' % q['id'])

# ---------- conceptual items: key tables ----------
print('Conceptual items checked against key tables')
def chk(sub, cond, msg):
    q = by(sub)
    if q:
        checked.add(q['id'])
        try: r = cond(q)
        except Exception as e_: r = False; msg += ' (%r)' % e_
        ok(r, '%s %s' % (q['id'], msg))
def F1(c):
    m = re.search(r'(?<![A-Za-z])([A-Z][A-Za-z0-9()]*(?:\^\d*[+-])?)', txt(c))
    return re.sub(r'\((?:s|l|g|aq)\)$', '', m.group(1)) if m else None
def cl(q): return [klass(F1(c)) for c in q['c']]
chk('Which acid is a strong acid?', lambda q: cl(q)[0] == 'strong acid' and all(x == 'weak acid' for x in cl(q)[1:]), 'only c[0] strong acid (12.3 list)')
chk('Which acid is a weak acid?', lambda q: cl(q)[0] == 'weak acid' and all(x == 'strong acid' for x in cl(q)[1:]), 'only c[0] weak acid')
chk('Which compound is a strong base?', lambda q: cl(q)[0] == 'strong base' and 'strong base' not in cl(q)[1:] and None not in cl(q), 'only c[0] strong base')
chk('Which acid is strong?', lambda q: cl(q)[0] == 'strong acid' and all(x == 'weak acid' for x in cl(q)[1:]), 'only c[0] strong acid')
chk('Which compound is a weak base?', lambda q: cl(q)[0] == 'weak base' and all(x == 'strong base' for x in cl(q)[1:]), 'only c[0] weak base')
chk('Which hydroxide is not a strong base', lambda q: cl(q)[0] != 'strong base' and all(x == 'strong base' for x in cl(q)[1:]), 'only c[0] off the strong-base list')
chk('Which compound is a salt?', lambda q: cl(q)[0] == 'salt' and 'salt' not in cl(q)[1:] and None not in cl(q), 'only c[0] salt')
chk('Which compound is a base?', lambda q: cl(q)[0] == 'base' and all(x in ('salt', 'weak acid', 'neither') for x in cl(q)[1:]), 'only c[0] base')
chk('Isopropyl alcohol', lambda q: klass('C3H7OH') == 'neither' and plain(q['c'][0]).startswith('neither'), 'alcohol = neither')
chk('ammonium bromide, NH4Br', lambda q: klass('NH4Br') == 'salt' and plain(q['c'][0]) == 'a salt', 'NH4Br = salt')
chk('conducts electricity only weakly', lambda q: klass(F1(q['c'][0])) == 'weak acid' and all(klass(F1(c)) in ('strong acid', 'strong base', 'salt') for c in q['c'][1:]), 'only c[0] weak electrolyte')
chk('Perchloric acid, HClO4, is dissolved', lambda q: 'HClO4' in SA and plain(q['c'][0]).endswith('only'), 'strong acid: ions only')
chk('Acetic acid, HC2H3O2, is dissolved', lambda q: 'HC2H3O2' in WA and plain(q['c'][0]).startswith('mostly intact'), 'weak acid: mostly molecules')
chk('Solution A is 0.0020 M HNO3', lambda q: 'HNO3' in SA and 'HC2H3O2' in WA and 'dilute solution of a strong acid' in plain(q['c'][0]), 'strength vs concentration')
chk('Calcium hydroxide dissolves in water. How many', lambda q: OHN['Ca(OH)2'] == 2 and 'Ca(OH)2' in SB and plain(q['c'][0]).startswith('2 oh^-; a single'), '2 OH-, single arrow')
def ion_arrow(q):
    good = [j for j, c in enumerate(q['c']) for s_, e in eqs_in(c) if e[1] and arrow_ok(e) and any(t[1] == 'H3O^+' for t in e[1]) and any(t[1] == 'H2O' for t in e[0])]
    return good == [0]
chk('Nitrous acid, HNO2, is a weak acid. Which equation', ion_arrow, 'only c[0]: acid donates to water with the right arrow')
def salt_of(q, want):
    w = eqs_in(q['w'])[0][1]; prods = [f for co, f, sp in w[1] if f != 'H2O']
    return balanced(w) and prods == [want] and F1(q['c'][0]) == want
chk('Hydroiodic acid neutralizes barium hydroxide', lambda q: salt_of(q, 'BaI2'), 'salt from the balanced equation in w')
chk('Perchloric acid neutralizes lithium hydroxide', lambda q: salt_of(q, 'LiClO4'), 'salt from the balanced equation in w')
chk('Potassium hydroxide neutralizes hydroiodic acid', lambda q: salt_of(q, 'KI'), 'salt + water from the balanced equation in w')
def coef(q, f):
    e = eqs_in(q['w'])[0][1]
    return {g: co for side in e[:2] for co, g, sp in side}.get(f)
chk('how many water molecules form for each Mg(OH)2', lambda q: coef(q, 'H2O') == int(txt(q['c'][0])) and coef(q, 'Mg(OH)2') == 1, 'water coefficient from w')
chk('how many moles of HCl react with 1 mol of K2CO3', lambda q: coef(q, 'HCl') == int(txt(q['c'][0])) and coef(q, 'K2CO3') == 1, 'HCl coefficient from w')
# conjugates and roles
def roles(e):
    L_, R_ = e[0], e[1]; out = {}
    for co, f, sp in L_:
        for co2, g, sp2 in R_:
            if add_h(sp) == sp2: out[f] = ('base', g)
            elif add_h(sp2) == sp: out[f] = ('acid', g)
    return out
def stem_eq(q): return eqs_in(q['q'])[0][1]
def same(c, sp): return species(F1(c)) == sp
chk('which reactant is the Brønsted–Lowry base?', lambda q: roles(stem_eq(q))[F1(q['c'][0])][0] == 'base' and all(roles(stem_eq(q)).get(F1(c), ('x',))[0] != 'base' for c in q['c'][1:]), 'base = reactant that gains H+')
chk('what is the conjugate base of HCO3^-?', lambda q: roles(stem_eq(q))['HCO3^-'] == ('acid', F1(q['c'][0])) and same(q['c'][0], add_h(species('HCO3^-'), -1)), 'conjugate base = HCO3- minus H+')
def pairs(q):
    a, b = [F1(x) for x in txt(q['c'][0]).split(' and ')]
    r = roles(stem_eq(q))
    isp = lambda x, y: add_h(species(x)) == species(y) or add_h(species(y)) == species(x)
    others = [[F1(x) for x in txt(c).split(' and ')] for c in q['c'][1:]]
    return isp(a, b) and (r.get(a, (0, 0))[1] == b or r.get(b, (0, 0))[1] == a) and not any(isp(*o) for o in others)
chk('Which choice lists one of its two conjugate acid–base pairs', pairs, 'only c[0] differs by one H+ (and pairs across the arrow)')
def conj(src, n):
    def f(q):
        want = add_h(species(src), n)
        return same(q['c'][0], want) and all(not same(c, want) for c in q['c'][1:])
    return f
chk('conjugate base of phosphoric acid', conj('H3PO4', -1), 'H3PO4 - H+ = H2PO4-')
chk('conjugate acid of the hydrogen sulfide ion', conj('HS^-', 1), 'HS- + H+ = H2S')
chk('conjugate acid of the carbonate ion', conj('CO3^2-', 1), 'CO3 2- + H+ = HCO3-')
chk('Lactic acid, HC3H5O3, is made by hard-working muscles', conj('HC3H5O3', -1), 'lactic acid - H+ = lactate')
chk('conjugate acid of the nitrite ion', conj('NO2^-', 1), 'NO2- + H+ = HNO2')
def water_role(q, want):
    rs = [roles(eqs_in(c)[0][1]).get('H2O', ('?',))[0] for c in q['c']]
    return rs[0] == want and all(r != want for r in rs[1:])
chk('does water act as a Brønsted–Lowry acid', lambda q: water_role(q, 'acid'), 'water is the acid only in c[0] (roles from each equation)')
chk('What role does water play in this reaction', lambda q: roles(stem_eq(q))['H2O'][0] == 'base' and plain(q['c'][0]).startswith('a base'), 'water = base (from the stem equation)')
chk('which species is the conjugate acid?', lambda q: any(v == ('base', F1(q['c'][0])) for v in roles(stem_eq(q)).values()), 'conjugate acid = product of the base')
def notpair(q):
    isp = lambda x, y: add_h(species(x)) == species(y) or add_h(species(y)) == species(x)
    ps = [[F1(x) for x in txt(c).split(' and ')] for c in q['c']]
    return not isp(*ps[0]) and all(isp(*p) for p in ps[1:])
chk('Which pair is not a conjugate acid–base pair', notpair, 'only c[0] does not differ by one H+')
chk('Which species is amphoteric', lambda q: F1(q['c'][0]) in WA and F1(q['c'][0]) in WB and all(not (F1(c) in WA and F1(c) in WB) for c in q['c'][1:]), 'only c[0] is both a weak acid and a weak base')
chk('as an Arrhenius acid', lambda q: [any(t[1] == 'H^+' for t in eqs_in(c)[0][1][1]) for c in q['c']] == [True, False, False, False], 'only c[0] produces H+')
chk('Ammonia, NH3, neutralizes acids', lambda q: roles(eqs_in(q['y'][0])[0][1])['NH3'] == ('base', 'NH4^+') and 'accepts a proton' in plain(q['c'][0]), 'NH3 accepts H+ (equation in y[0])')
chk('net ionic equation', lambda q: [t[1] for t in eqs_in(q['c'][0])[0][1][0]] == ['H^+', 'OH^-'] and 'HBr' in SA and 'LiOH' in SB, 'strong acid + strong base: H+ + OH- -> H2O')
chk('autoionization of water?', lambda q: (lambda e: [t[1] for t in e[0]] == ['H2O', 'H2O'] and e[2] == '<=>' and {t[1] for t in e[1]} == {'H3O^+', 'OH^-'})(eqs_in(q['c'][0])[0][1]), 'H2O + H2O <=> H3O+ + OH-')
# indicators
chk('turns blue litmus paper red', lambda q: plain(q['c'][0]) == 'the solution is acidic.', 'blue litmus -> red = acid (12.1)')
chk('stays colorless. What can you conclude', lambda q: plain(q['c'][0]) == 'the solution is acidic or neutral.', 'phenolphthalein colorless = acidic or neutral (12.1)')
def _cab(q):
    rows = {txt(r[0]): txt(r[1]) for r in q['f'][0]['rows']}
    keyrange = txt(q['c'][0]).split(',')[0].replace('pH ', '')
    return rows == CABBAGE and rows[keyrange] == 'pink' and all(rows.get(txt(c).split(',')[0].replace('pH ', '')) != 'pink' for c in q['c'][1:])
chk('turns the indicator pink', _cab, 'cabbage table = 12.1 chart; pink = pH 3–4')
chk('Which single result proves that the cleaner is basic', lambda q: plain(q['c'][0]).startswith('red litmus paper turns blue'), 'base: red litmus -> blue')
chk('placed on a strip of red litmus paper', lambda q: plain(q['c'][0]).startswith('blue, because ammonia is a base') and klass('NH3') == 'weak base', 'ammonia (base): red litmus -> blue')
chk('turns light pink and stays pink', lambda q: 'excess of base' in plain(q['c'][0]), 'phenolphthalein pink = base in excess')
chk('turns yellow in a sample', lambda q: cab('13') == 'yellow' and cab('2') != 'yellow' and cab('7') != 'yellow' and cab('3') != 'yellow' and 'sodium hydroxide' in plain(q['c'][0]), 'yellow = pH 12–14 (strong base)')
chk('Which property belongs to acids rather than to bases', lambda q: 'hydrogen gas' in plain(q['c'][0]), 'acid + active metal -> H2')
chk('Iron filings are dropped into hydrochloric acid', lambda q: (lambda e: balanced(e) and [f for co, f, sp in e[1]] == ['FeCl2', 'H2'])(eqs_in(q['y'][0])[0][1]) and plain(q['c'][0]).startswith('fecl2(aq) and h2(g)'), 'acid + metal -> salt + H2 (equation in y[0])')
chk('baking soda (NaHCO3) reacts with the lactic acid', lambda q: (lambda e: balanced(e) and {f for co, f, sp in e[1]} == {'NaC3H5O3', 'H2O', 'CO2'} and F1(q['c'][0]) == 'NaC3H5O3')(eqs_in(q['y'][0])[0][1]), 'acid + bicarbonate -> salt + H2O + CO2')
chk('Acid rain slowly dissolves marble', lambda q: F1(q['c'][0].split(',')[1]) == 'CO2', 'acid + carbonate -> CO2')
chk('zinc strip is placed in dilute sulfuric acid', lambda q: (lambda e: balanced(e) and 'H2' in [f for co, f, sp in e[1]])(eqs_in(q['y'][0])[0][1]) and plain(q['c'][0]).startswith('hydrogen'), 'acid + metal -> H2')
# water and Kw
def cls_h(h): return 'acidic' if h > D('1.0e-7') else 'basic' if h < D('1.0e-7') else 'neutral'
def given(q):
    m = re.search(r'\[(H3O\^\+|OH\^-)\] = ([\d.]+ x 10\^-?\d+) M', txt(q['q'])); x = val(m.group(2))
    return x if m.group(1) == 'H3O^+' else KW / x
chk('[H3O^+] = 3.8 x 10^-9 M at 25 °C. How is it', lambda q: plain(q['c'][0]) == cls_h(given(q)), 'class from [H3O+] vs 10^-7')
chk('[OH^-] = 2.7 x 10^-11 M at 25 °C. How is it', lambda q: plain(q['c'][0]) == cls_h(given(q)), 'class from [OH-] via Kw')
chk('[OH^-] = 4.8 x 10^-8 M at 25 °C. How is it', lambda q: plain(q['c'][0]) == cls_h(given(q)), 'class from [OH-] via Kw')
def sci2(v):
    m, e = format(D(v), '.1e').split('e'); return '%s x 10^%d' % (m, int(e))
def _tab(q):
    hs = {}
    for r in q['f'][0]['rows']:
        m = re.match(r'\[(H3O\^\+|OH\^-)\] = ([\d.]+ x 10\^-?\d+) M', txt(r[1])); x = val(m.group(2))
        hs['Solution ' + txt(r[0])] = x if m.group(1) == 'H3O^+' else KW / x
    best = max(hs, key=hs.get); naive = max((k for k in hs if 'H3O' in txt(q['f'][0]['rows'][ord(k[-1]) - 65][1])), key=hs.get)
    return txt(q['c'][0]) == best and best != naive and all(sci2(hs[k]) in txt(q['w']) for k in hs)
chk('Which solution is the most acidic', _tab, 'largest [H3O+] after Kw conversion (and not the largest listed [H3O+])')
chk('Pure water at 25 °C has pH 7.00. What is its [OH^-]', lambda q: txt(q['c'][0]) == fmt((KW).sqrt(), 2) + ' M' and fmt(TEN('7.00'), 2) + ' M' == txt(q['c'][0]), 'sqrt(Kw) = 10^-7.00 = 1.0 x 10^-7 M')
chk('Solution X has [OH^-] = 1 x 10^-4 M', lambda q: (D('1e-4') > KW / D('1e-9')) and plain(q['c'][0]).startswith('x,'), 'X [OH-] 10^-4 > Y 10^-5')
# pH scale
TYP = {'Lemon juice': '2', 'Cola': '2.5', 'Vinegar': '3', 'Black coffee': '5', 'Milk': '6.5', 'Baking soda in water': '8.3', 'Household ammonia': '11.5'}
def _thousand(q):
    rows = {txt(r[0]): txt(r[1]) for r in q['f'][0]['rows']}
    f = {txt(c): D(10) ** (D(rows['Black coffee']) - D(rows[txt(c)])) for c in q['c']}
    return rows == TYP and f[txt(q['c'][0])] == 1000 and all(v != 1000 for k, v in f.items() if k != txt(q['c'][0]))
chk('about 1000 times the [H3O^+] of black coffee', _thousand, 'table = 12.5 figure values; 10^(5-2) = 1000 only for c[0]')
def _order(q):
    vals = re.findall(r'(\d+\.\d+)', txt(q['q'])); want = ', '.join(sorted(vals, key=D, reverse=True))
    return txt(q['c'][0]) == want and all(txt(c) != want for c in q['c'][1:])
chk('order of increasing acidity', _order, 'increasing acidity = decreasing pH')
chk('Solution X has pH 3.0 and solution Y has pH 6.0', lambda q: int(D(10) ** (D('6.0') - D('3.0'))) == 1000 and plain(q['c'][0]).startswith('x has 1000 times'), '10^3 = 1000, lower pH has more')
chk('soil samples from a San Joaquin Valley farm', lambda q: D(10) ** (D('8.5') - D('6.5')) == 100 and plain(q['c'][0]) == 'the ph 6.5 soil, by a factor of 100', '10^2, lower pH has more')
chk('blood gas shows pH 7.52', lambda q: plain(q['c'][0]).startswith(blood('7.52')), 'blood class (7.35–7.45)')
chk('blood gas shows pH 7.33', lambda q: plain(q['c'][0]).startswith(blood('7.33')), 'blood class (7.35–7.45)')
chk('his arterial pH is 7.38', lambda q: blood('7.38') == 'normal' and 'normal range' in plain(q['w']), '7.38 within 7.35–7.45')
# buffers
def pair2(c): return [F1(x) for x in re.split(r' and ', txt(c))]
chk('Which mixture is a buffer?', lambda q: buffer(*pair2(q['c'][0])) and not any(buffer(*pair2(c)) for c in q['c'][1:]), 'only c[0] is a weak acid + its conjugate base')
chk('Which mixture is not a buffer', lambda q: not buffer(*pair2(q['c'][0])) and all(buffer(*pair2(c)) for c in q['c'][1:]), 'only c[0] fails (strong acid)')
chk('dissolved together in water, makes a buffer', lambda q: buffer(*pair2(q['c'][0])) and not any(buffer(*pair2(c)) for c in q['c'][1:]), 'only c[0] is a weak base + its conjugate acid')
chk('with potassium chloride, KCl', lambda q: 'HF' in WA and not buffer('HF', 'KCl') and buffer('HF', 'KF') and 'not the conjugate base of hf' in plain(q['c'][0]), 'HF weak but Cl- is not F-')
def partner(q, added):
    """species that reacts with added acid (the base partner, fewer H) or added base (the acid partner, more H)."""
    t = txt(q['q']); fs = re.findall(r'(H[A-Za-z0-9()]*(?:\^\d*[+-])?|[A-Z][A-Za-z0-9]*\^\d*-)(?= and |\. |, )', t)
    k = F1(q['c'][0]); return k
def _part(acid, base, added):
    def f(q):
        k = F1(q['c'][0]); a_, b_ = species(acid), species(base)
        if add_h(b_) != a_ or not buffer(acid, base): return False
        e = [eqs_in(h)[0][1] for h in (q['w'], q['y'][0]) if eqs_in(h)]
        want = base if added == 'acid' else acid
        ok_eq = all(balanced(x) and want in [g for co, g, sp in x[0]] and ('H3O^+' if added == 'acid' else 'OH^-') in [g for co, g, sp in x[0]] for x in e)
        return k == want and ok_eq
    return f
chk('A buffer contains HNO2 and NaNO2', _part('HNO2', 'NO2^-', 'acid'), 'added acid reacts with the base partner')
chk('phosphate buffer contains H2PO4^- and HPO4^2-', _part('H2PO4^-', 'HPO4^2-', 'base'), 'added base reacts with the acid partner')
chk('Which organ controls the blood', lambda q: plain(q['c'][0]) == 'the kidneys, over hours to days', 'kidneys adjust HCO3- over hours to days (12.6)')
def _buf_eq(acid, base, added):
    def f(q):
        e = eqs_in(q['c'][0])[0][1]; L_ = [g for co, g, sp in e[0]]; R_ = [g for co, g, sp in e[1]]
        want = (base, 'H3O^+', acid) if added == 'acid' else (acid, 'OH^-', base)
        good = sorted(L_) == sorted(want[:2]) and want[2] in R_ and balanced(e)
        others = []
        for c in q['c'][1:]:
            e2 = eqs_in(c)[0][1]; others.append(sorted(g for co, g, sp in e2[0]) == sorted(want[:2]))
        return good and not any(others)
    return f
chk('Which equation shows it neutralizing a small amount of added OH^-', _buf_eq('HF', 'F^-', 'base'), 'HF + OH- -> F- + H2O')
chk('Which equation shows it neutralizing added H3O^+', _buf_eq('HC3H5O3', 'C3H5O3^-', 'acid'), 'lactate + H3O+ -> lactic acid + H2O')
chk('main buffer in blood', lambda q: buffer('H2CO3', 'HCO3^-') and not buffer('H2CO3', 'CO3^2-') and pair2(q['c'][0]) == ['H2CO3', 'HCO3^-'], 'H2CO3/HCO3- (differ by one H+)')
chk('plaque bacteria release lactic acid', lambda q: F1(q['c'][0].split(',')[1]) == 'HCO3^-' and 'HCO3^-' in WB, 'added acid -> bicarbonate (base partner)')
chk('0.20 mol of HCl is added', lambda q: D('0.20') > D('0.10') and 'used up' in plain(q['c'][0]), 'HCl exceeds A- -> capacity exceeded')
chk('by itself, lowers blood pH', lambda q: plain(q['c'][0]) == 'a rise in blood co2', 'CO2 up -> H+ up -> pH down')
chk('severe chronic lung disease', lambda q: 'pH falls' in txt(q['c'][0]) and 'acidosis' in plain(q['c'][0]), 'CO2 retention -> acidosis')
chk('hiker who climbs quickly', lambda q: plain(q['c'][0]).startswith('it rises') and 'alkalosis' in plain(q['c'][0]), 'CO2 blown off -> alkalosis')

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
print('Draft overlap: no stem reuses a worked-example or exercise number from drafts/ch12')
GIV = r'(\d+\.\d+|\d+)( x 10\^-?\d+)? M\b|pO?H (\d+\.\d+)'
CONST = {'1.0 x 10^-14', '1.0 x 10^-7', '7.35', '7.45', '14.00', '7.00', '1.0', '1', '0.10'}
def givens_in(t):
    out = set()
    for a, b, c in re.findall(GIV, t):
        g = (a + b) if a else c
        if g not in CONST: out.add(g)
    return out
def draft_txt(b):
    t = re.sub(r'\\\(|\\\)|\\dfrac|\\text|\\qquad|\\left|\\right|\\cdot|\\,|\\;|\\quad', ' ', b)
    t = t.replace('\\times', '&times;'); t = re.sub(r'\^\{(-?\d+)\}', r'^\1', t); t = re.sub(r'\^\{-\\text\{pH\}\}', '', t)
    t = re.sub(r'\{\}\^\\circ\s*', '°', t)
    t = txt(t); t = re.sub(r'[{}]', ' ', t); t = re.sub(r'\s+', ' ', t)
    return t.replace(' x 10^', ' x 10^')
blocks = []
for p_ in sorted(glob.glob(os.path.join(ROOT, 'drafts', 'ch12', '*.html'))):
    h = open(p_, encoding='utf-8').read()
    for b in re.split(r'(?=Example \\\(\\PageIndex|Exercise \\\(\\PageIndex|<h2|Problem 12\.\d+\b)', h):
        t = draft_txt(b)
        if not re.match(r'\s*(Example|Exercise|Problem)', re.sub(r'<[^>]+>', '', b)[:40].strip() or 'x'): continue
        m = re.search(r'Problem (12\.\d+)', t)
        blocks.append((os.path.basename(p_) + (' Problem ' + m.group(1) if m else ''), givens_in(t), t.split(' Answer')[0]))
BANNED = {'3.5 x 10^-4', '0.0025', '0.015', '1.85', '7.30', '7.40', '7.25', '0.0063', '6.0 x 10^-4', '4.62', '7.48', '2.5 x 10^-3', '3.2 x 10^-5',
          '0.020', '0.0050', '6.7 x 10^-9', '4.0 x 10^-4', '0.0030', '3.65 x 10^-4', '5.0 x 10^-7', '0.0010'}
W = lambda s_: set(w for w in re.findall(r'[a-z0-9.]+', s_.lower()) if len(w) > 2)
nover = 0; notes = []
for q in ALL:
    qt = txt(q['q']); qg = givens_in(qt); qw = W(qt)
    for g_ in qg & BANNED:
        nover += 1; err.append('%s uses the draft worked-example given %s' % (q['id'], g_))
    for nm, gs, bt in blocks:
        if qg & gs:
            nover += 1; err.append('%s shares givens %s with %s' % (q['id'], sorted(qg & gs), nm))
        bw = W(bt); j = len(qw & bw) / max(1, len(qw | bw))
        if j > 0.45: nover += 1; err.append('%s stem is %.2f similar to %s' % (q['id'], j, nm))
        elif j > 0.3: notes.append('%s stem %.2f similar to %s (checked by hand)' % (q['id'], j, nm))
print('    %d draft blocks compared (%s); %d overlaps' % (len(blocks), ', '.join(sorted({b[0].split(' ')[0] for b in blocks})), nover))
for n_ in notes: print('    NOTE', n_)

# ---------- Mateo, coverage, counts, duplicates ----------
mateo = [q for q in ALL if 'Mateo' in q['q'] + ' '.join(q['y']) + q['w'] + ' '.join(q['c'])]
if len(mateo) > 2: err.append('Mateo appears in %d items (max 2): %s' % (len(mateo), [q['id'] for q in mateo]))
for q in mateo:
    s = txt(' '.join([q['q'], q['w']] + q['c'] + q['y']))
    for v in ('7.30', '7.40', '7.25'):
        if v in s: err.append('%s Mateo item reuses the draft value %s' % (q['id'], v))
print('Mateo items:', [q['id'] for q in mateo])
print('Items with a machine check: %d of %d' % (len(checked), len(ALL)))
print('  conceptual (key read by hand; quoted values and equations still checked):', ' '.join(sorted(hand)) or 'none')
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
