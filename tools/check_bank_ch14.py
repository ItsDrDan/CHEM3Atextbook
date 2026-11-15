#!/usr/bin/env python3
"""Checker for the Chapter 14 banks (radioactivity and detection, nuclear decay and equations, half-life,
radiocarbon dating, fission and fusion, radiation in medicine).
Structural checks as in tools/check_bank_ch11.py (ch14 topic ids; ADAPT = 42 items, text only, y[0] begins
"Correct: "; tables at most 3 columns; figures only of fbx types table/plot; planned topic counts), plus, written
independently of the generators:
  - nuclear notation: every <sup>A</sup><sub>Z</sub>X in every field is parsed; element symbol <-> Z against the
    checker's own periodic table; particles e/n/gamma/He/H against a particle table (A, Z); every "(name-A)" label and
    "element N is name" against the symbol; every "a positron"/"a beta particle" label against its symbol;
  - nuclear equations: every complete equation anywhere must conserve A and Z (coefficients counted); an equation
    with "?" (or x neutrons) in a stem is completed with each choice and only c[0] may balance; in "which equation
    is balanced" items only c[0] balances; decay-type and fission/fusion keys are classified from the equation;
  - every calculation item (k=1): the key and each numeric distractor's intended error recomputed with Decimal from
    the givens as written in the stem (or its table), TWO ways: (a) exact (1/2)^n, rounded once; (b) strict: the
    halving (or doubling) chain with every step rounded to the starting amount's significant figures. n must be a
    whole number recomputed from time / half-life (matching units) or from the amounts. Both ways must agree, no
    computed value may be a rounding tie (round half up), and the recomputed values must all differ;
  - quoted half-lives against the checker's table, which is itself checked against the 14.3 and 14.4 draft tables;
    quoted unit definitions (1 Ci = 3.7 x 10^10 Bq, 1 Gy = 1 J/kg, 1 Sv = 100 rem);
  - conceptual items: key tables (penetrating and ionizing order, shields, particle identities, units, detectors,
    imaging-tracer rule, dating-isotope rule, once-living materials, reactor parts) recheck the keys; the rest are
    listed as read by hand;
  - course rule: no whole number ending in 0 without a decimal point in a calculation stem (mass numbers in nuclear
    symbols, exponents and the drafts' half-lives 110 min and 5730 years excepted);
  - no stem reuses a draft worked example or exercise (a listed worked-example given, two shared givens with a draft
    Example/Exercise block, or the same nuclear equation); no stem in both banks; Mateo in at most 2 items.
usage: python3 tools/check_bank_ch14.py bank/ch14.json bank/ch14_adapt.json"""
import json, sys, re, os, collections, glob, math
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 50; getcontext().rounding = ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = {'ch14-radiation', 'ch14-decay', 'ch14-halflife', 'ch14-dating', 'ch14-fission', 'ch14-health', 'ch14-medicine'}
err = []

# ---------- text ----------
def txt(x):
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<[^>]+>', '', x)
    for a, b in (('&middot;', '·'), ('&minus;', '-'), ('−', '-'), ('&times;', 'x'), ('&nbsp;', ' '), ('&divide;', '/'),
                 ('&rarr;', '->'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&deg;', '°'), ('&ndash;', '–'), ('&lt;', '<'),
                 ('&gt;', '>'), ('&mu;', 'µ'), ('&gamma;', 'γ'), ('&prop;', '∝'), ('&hellip;', '…'), ('&ouml;', 'ö'),
                 ('&#322;', 'ł'), ('&amp;', '&')):
        x = x.replace(a, b)
    return x
def plain(x): return re.sub(r'\s+', ' ', txt(x)).strip().lower()
def fields(q): return [q['q'], q['h'], q['w']] + q['c'] + q['y']

# ---------- structural checks ----------
OUT_OF_SCOPE = r"all of the above|none of the above|decay constant|first-order|natural log|\bln\b|half-lives? of [\d.]+ and a fraction"
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
        s = ' '.join(fields(q))
        for tg in ('sub', 'sup', 'b', 'i'):
            if len(re.findall('<%s>' % tg, s)) != len(re.findall('</%s>' % tg, s)): err.append(i + ' unbalanced <%s>' % tg)
        if re.search(r'&(?!(?:[a-zA-Z]+\d*|#\d+);)', s): err.append(i + ' bare &')
        if '{' in s or '}' in s or '[[' in s or ']]' in s: err.append(i + ' unconverted markup')
        if '\\(' in s or '\\[' in s or '$' in s: err.append(i + ' MathJax/LaTeX in a bank item')
        if re.search(r'(?<![\w;])-(?=\d)', s): err.append(i + ' hyphen used as a minus sign')
        if ' -> ' in s: err.append(i + ' raw -> arrow')
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
structural(TRY, 'c14-%03d', 'TRY', True)
structural(HW, 'c14-h%02d', 'HW', False)
if len(HW) != 42: err.append('ADAPT has %d items, not 42' % len(HW))
if sum(1 for q in TRY if q.get('f')) > 4: err.append('more than 4 figures')
fbx = open(os.path.join(ROOT, 'js', 'fbx.js'), encoding='utf-8').read()
for t_ in {f['type'] for q in TRY for f in q.get('f', [])}:
    if not re.search(r'[{,]%s:' % t_, fbx): err.append('figure type %s not supported by js/fbx.js' % t_)
wid = open(os.path.join(ROOT, 'js', 'widget.js'), encoding='utf-8').read()
for t_ in TOP:
    if "'%s'" % t_ not in wid: err.append('topic %s missing from js/widget.js TOPICS' % t_)
WANT_T = {'ch14-radiation': 10, 'ch14-decay': 18, 'ch14-halflife': 16, 'ch14-dating': 10, 'ch14-fission': 8, 'ch14-health': 7, 'ch14-medicine': 6}
WANT_H = {'ch14-radiation': 6, 'ch14-decay': 11, 'ch14-halflife': 10, 'ch14-dating': 6, 'ch14-fission': 4, 'ch14-health': 3, 'ch14-medicine': 2}
for nm, B, W in (('Try It', TRY, WANT_T), ('ADAPT', HW, WANT_H)):
    got = dict(collections.Counter(q['t'] for q in B))
    if got != W: err.append('%s topic counts %s, planned %s' % (nm, got, W))
ALL = TRY + HW

def ok(cond, msg):
    print('   ', 'OK ' if cond else 'BAD', msg)
    if not cond: err.append(msg)

# ---------- periodic table, names, particles (checker's own) ----------
PT = {}
for z, s in enumerate(('H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br '
                       'Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er '
                       'Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm').split(), 1):
    PT[s] = z
for s, z in (('H', 1), ('He', 2), ('C', 6), ('N', 7), ('O', 8), ('F', 9), ('Sr', 38), ('Y', 39), ('Tc', 43), ('I', 53), ('Xe', 54),
             ('Cs', 55), ('Ba', 56), ('Tl', 81), ('Pb', 82), ('Bi', 83), ('Po', 84), ('Rn', 86), ('Ra', 88), ('Th', 90), ('U', 92), ('Pu', 94)):
    if PT[s] != z: err.append('checker periodic table: %s is %d, expected %d' % (s, PT[s], z))
NAME = {'hydrogen': 'H', 'tritium': 'H', 'helium': 'He', 'lithium': 'Li', 'beryllium': 'Be', 'boron': 'B', 'carbon': 'C',
        'nitrogen': 'N', 'oxygen': 'O', 'fluorine': 'F', 'neon': 'Ne', 'sodium': 'Na', 'phosphorus': 'P', 'potassium': 'K',
        'chromium': 'Cr', 'cobalt': 'Co', 'zinc': 'Zn', 'gallium': 'Ga', 'germanium': 'Ge', 'krypton': 'Kr', 'rubidium': 'Rb',
        'strontium': 'Sr', 'yttrium': 'Y', 'technetium': 'Tc', 'indium': 'In', 'tellurium': 'Te', 'iodine': 'I', 'xenon': 'Xe',
        'cesium': 'Cs', 'barium': 'Ba', 'lanthanum': 'La', 'lutetium': 'Lu', 'iridium': 'Ir', 'mercury': 'Hg', 'thallium': 'Tl',
        'lead': 'Pb', 'bismuth': 'Bi', 'polonium': 'Po', 'radon': 'Rn', 'radium': 'Ra', 'actinium': 'Ac', 'thorium': 'Th',
        'protactinium': 'Pa', 'uranium': 'U', 'neptunium': 'Np', 'plutonium': 'Pu', 'argon': 'Ar', 'molybdenum': 'Mo',
        'americium': 'Am', 'zirconium': 'Zr', 'bromine': 'Br', 'chlorine': 'Cl', 'samarium': 'Sm', 'copper': 'Cu', 'nickel': 'Ni', 'magnesium': 'Mg', 'cadmium': 'Cd', 'europium': 'Eu', 'promethium': 'Pm', 'gadolinium': 'Gd', 'curium': 'Cm', 'aluminum': 'Al', 'francium': 'Fr', 'calcium': 'Ca'}
PARTICLE = {'alpha particle': (4, 2, 'He'), 'beta particle': (0, -1, 'e'), 'positron': (0, 1, 'e'), 'gamma ray': (0, 0, 'γ'),
            'neutron': (1, 0, 'n'), 'proton': (1, 1, 'H')}
PEN = {'alpha': 1, 'beta': 2, 'gamma': 3}            # penetrating power (Section 14.2 table)
ION = {'alpha': 3, 'beta': 2, 'gamma': 1}            # ionizing power
SHIELD = {'alpha': ('paper', 'skin', 'clothing'), 'beta': ('aluminum', 'plastic', 'wood', 'lab coat'), 'gamma': ('lead', 'concrete')}
UNITS = {'becquerel': 'activity', 'curie': 'activity', 'gray': 'absorbed', 'rad': 'absorbed', 'sievert': 'equivalent', 'rem': 'equivalent'}
EMIT = {'technetium-99m': {'gamma'}, 'cobalt-60': {'beta', 'gamma'}, 'uranium-238': {'alpha'}, 'carbon-14': {'beta'},
        'iodine-123': {'gamma', 'electron capture'}, 'iodine-131': {'beta', 'gamma'}, 'fluorine-18': {'positron'}}
# half-lives: (value as written, unit); the draft rows are rechecked against drafts/ch14 below
HL = {'fluorine-18': ('110', 'min'), 'technetium-99m': ('6.0', 'h'), 'iodine-123': ('13', 'h'), 'radon-222': ('3.8', 'days'),
      'iodine-131': ('8.0', 'days'), 'phosphorus-32': ('14.3', 'days'), 'cobalt-60': ('5.27', 'years'), 'carbon-14': ('5730', 'years'),
      'uranium-238': ('4.5 x 10^9', 'years'), 'hydrogen-3': ('12.3', 'years'), 'potassium-40': ('1.25 x 10^9', 'years'),
      'sodium-24': ('15.0', 'h'), 'gallium-67': ('3.26', 'days'), 'xenon-133': ('5.25', 'days'), 'chromium-51': ('27.7', 'days'),
      'lutetium-177': ('6.65', 'days'), 'indium-111': ('2.80', 'days'), 'iridium-192': ('73.8', 'days'), 'samarium-153': ('46.3', 'h')}
UNORM = {'min': 'min', 'minutes': 'min', 'h': 'h', 'hours': 'h', 'days': 'days', 'years': 'years'}
def hl_years(name):
    v, u = HL[name]; v = D(v.replace(' x 10^', 'e'))
    return v * {'min': D(1) / 525960, 'h': D(1) / 8766, 'days': D(1) / D('365.25'), 'years': D(1)}[u]

print('Half-life table against the 14.3 and 14.4 draft tables')
for p_ in ('14.3_half_life.html', '14.4_radiocarbon.html'):
    h = open(os.path.join(ROOT, 'drafts', 'ch14', p_), encoding='utf-8').read()
    for nm, val in re.findall(r'<td data-th="(?:Radioisotope|Isotope \(decays to\))">([A-Za-z]+-\d+m?)[^<]*</td><td data-th="Half-life">([^<]+)</td>', h):
        t = txt(val).strip(); m = re.fullmatch(r'([\d.]+(?: x 10\^\d+)?) (\w+)', t)
        key = nm.lower()
        ok(m is not None and key in HL and HL[key] == (m.group(1), UNORM[m.group(2)]), '%s %s: draft %s, checker %s' % (p_, key, t, HL.get(key)))

# ---------- nuclear notation ----------
NUC = re.compile(r'<sup>(\d+)(m?)</sup><sub>(&minus;|\+)?(\d+)</sub>(&gamma;|[A-Z][a-z]?|e|n)')
def nuclides(h):
    out = []
    for m in NUC.finditer(h):
        A, meta, sg, z, s = int(m.group(1)), m.group(2), m.group(3), int(m.group(4)), m.group(5)
        z = -z if sg == '&minus;' else z
        out.append((A, z, 'γ' if s == '&gamma;' else s, meta, m.start(), m.end()))
    return out
def nuc_ok(n):
    A, z, s, meta = n[:4]
    if s == 'e': return A == 0 and z in (-1, 1)
    if s == 'n': return A == 1 and z == 0
    if s == 'γ': return A == 0 and z == 0
    return s in PT and PT[s] == z and A >= z
print('Nuclear symbols: symbol <-> Z, particle A and Z, labels')
nn = 0
for q in ALL:
    for h in fields(q) + [c for f in q.get('f', []) if f['type'] == 'table' for r in f['rows'] for c in r]:
        for n in nuclides(h):
            nn += 1
            if not nuc_ok(n): err.append('%s bad nuclear symbol A=%s Z=%s %s' % (q['id'], n[0], n[1], n[2]))
            after = txt(h[n[5]:n[5] + 40])
            m = re.match(r' \(([a-z]+)-(\d+)(m?)', after)
            if m and (NAME.get(m.group(1)) != n[2] or int(m.group(2)) != n[0] or m.group(3) != n[3]):
                err.append('%s label (%s-%s%s) does not match the symbol %s-%d%s' % (q['id'], m.group(1), m.group(2), m.group(3), n[2], n[0], n[3]))
            m = re.match(r', an? (alpha particle|beta particle|positron|gamma ray|neutron|proton)', after)
            if m and PARTICLE[m.group(1)] != n[:3]: err.append('%s "%s" labels %s' % (q['id'], m.group(1), n[:3]))
            before = txt(h[max(0, n[4] - 40):n[4]])
            m = re.search(r'(?:A|An|an?) (alpha particle|beta particle|positron|gamma ray|neutron|proton), $', before)
            if m and PARTICLE[m.group(1)] != n[:3]: err.append('%s "%s" labels %s' % (q['id'], m.group(1), n[:3]))
        for zz, nm in re.findall(r'[Ee]lement (\d+) is ([a-z]+)', txt(h)):
            if PT.get(NAME.get(nm, '?')) != int(zz): err.append('%s says element %s is %s' % (q['id'], zz, nm))
        for nm, zz in re.findall(r'\b([A-Za-z]+) is element (\d+)', txt(h)):
            if PT.get(NAME.get(nm.lower(), '?')) != int(zz): err.append('%s says %s is element %s' % (q['id'], nm, zz))
        for nm in re.findall(r'\b([a-z]+)-\d+m?\b', txt(h).lower()):
            if nm not in NAME and nm not in ('half', 'one', 'two', 'three', 'four', 'up', 'x', 'single', 'double', 'non', 'per', 'nuclear', 'i', 'pre'):
                err.append('%s unknown element name %r' % (q['id'], nm))
print('    %d nuclear symbols parsed, all consistent' % nn)

# ---------- nuclear equations ----------
def tokenize(h):
    """replace each nuclide with N<k>; return the token string and the nuclide list."""
    ns_ = nuclides(h); out = []; last = 0
    for k, n in enumerate(ns_):
        out.append(h[last:n[4]]); out.append(' N%d ' % k); last = n[5]
    out.append(h[last:])
    s = re.sub(r'\s+', ' ', ''.join(out))
    s = s.replace('<i>x</i>', 'x')
    return s, ns_
TERM = r'(?:(?:\d+|x) )?N\d+|\?|energy'
EQ = re.compile(r'(?:%s)(?: \+ (?:%s))* &rarr; (?:%s)(?: \+ (?:%s))*' % (TERM, TERM, TERM, TERM))
def equations(h):
    s, ns_ = tokenize(h); out = []
    for m in EQ.finditer(s):
        L_, R_ = m.group().split(' &rarr; ')
        def side(S_):
            r = []
            for t in S_.split(' + '):
                t = t.strip()
                if t == 'energy': continue
                if t == '?': r.append(('?', None)); continue
                mm = re.fullmatch(r'(?:(\d+|x) )?N(\d+)', t)
                r.append((mm.group(1) or '1', ns_[int(mm.group(2))]))
            return r
        out.append((side(L_), side(R_)))
    return out
def tot(S_, fill=None, x=None):
    a = z = 0
    for co, n in S_:
        if co == '?' or n is None:
            if fill is None: return None
            co, n = '1', fill
        c = int(x) if co == 'x' else int(co)
        a += c * n[0]; z += c * n[1]
    return a, z
def balanced(e, fill=None, x=None):
    l, r = tot(e[0], fill, x), tot(e[1], fill, x)
    return l is not None and l == r
def sig(e, fill=None):
    f = lambda S_: frozenset(collections.Counter((n if n else fill)[:4] for co, n in S_ for _ in range(int(co) if co.isdigit() else 1)).items())
    return (f(e[0]), f(e[1]))
def heavy(e, fill=None):
    return frozenset((n if n else fill)[2] + '-' + str((n if n else fill)[0]) + (n if n else fill)[3] for co, n in e[0] + e[1]
                     if (n or fill) and (n if n else fill)[2] not in ('e', 'n', 'γ') and (n if n else fill)[0] > 4)
def classify(e):
    """decay type from a complete equation."""
    Lp = [n for co, n in e[0]]; Rp = [n for co, n in e[1]]
    prod = {(n[0], n[1], n[2]) for n in Rp}; reac = {(n[0], n[1], n[2]) for n in Lp}
    if (0, -1, 'e') in reac: return 'electron capture'
    if len(Lp) >= 2 and all(n[0] <= 4 for n in Lp): return 'fusion'
    if (1, 0, 'n') in reac and any(n[0] > 200 for n in Lp): return 'fission'
    if len(Lp) == 1:
        if (4, 2, 'He') in prod: return 'alpha decay'
        if (0, -1, 'e') in prod: return 'beta decay'
        if (0, 1, 'e') in prod: return 'positron emission'
        if (0, 0, 'γ') in prod: return 'gamma emission'
    return 'bombardment'
print('Nuclear equations: complete ones conserve A and Z; incomplete stems have exactly one choice that completes them')
neq = 0; eq_checked = set(); STEM_EQ = {}
for q in ALL:
    which = 'balanced?' in txt(q['q']) or 'is balanced' in txt(q['q'])
    for fi, h in enumerate(fields(q)):
        for e in equations(h):
            neq += 1
            has_q = any(n is None for co, n in e[0] + e[1]) or any(co == 'x' for co, n in e[0] + e[1])
            if fi == 0 and has_q:
                xs = any(co == 'x' for co, n in e[0] + e[1])
                res = []
                for c in q['c']:
                    if xs:
                        v = txt(c).strip(); res.append(v.isdigit() and balanced(e, None, v))
                    else:
                        cn = nuclides(c)
                        res.append(len(cn) >= 1 and balanced(e, cn[0]))
                ok(res == [True, False, False, False], '%s "?" equation completed by each choice balances only for c[0]: %s' % (q['id'], res))
                eq_checked.add(q['id'])
                if not xs: STEM_EQ[q['id']] = (e, nuclides(q['c'][0])[0])
                else: STEM_EQ[q['id']] = (e, None)
            elif has_q:
                err.append('%s incomplete equation outside the stem' % q['id'])
            elif fi >= 3 and fi <= 6 and which:
                pass
            elif not balanced(e):
                err.append('%s unbalanced equation in field %d: %s' % (q['id'], fi, txt(h)[:80]))
            elif fi == 0:
                STEM_EQ[q['id']] = (e, None)
    if which:
        res = [len(equations(c)) == 1 and balanced(equations(c)[0]) for c in q['c']]
        ok(res == [True, False, False, False], '%s "which equation is balanced": only c[0] balances %s' % (q['id'], res))
        eq_checked.add(q['id'])
print('    %d equations parsed' % neq)

# ---------- numbers ----------
def sf(s):
    s = s.strip().lstrip('+-').replace(',', '')
    if 'e' in s.lower(): s = s.lower().split('e')[0]
    if '.' in s: return len(s.replace('.', '').lstrip('0'))
    return len(s.lstrip('0').rstrip('0'))
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
def tie(v, n):
    v = abs(D(v))
    if v == 0: return False
    e = v.adjusted(); sc = v.scaleb(n - 1 - e)
    return sc - int(sc) == D('0.5')
TIES = []
def U(v, n, u=''):
    if tie(v, n): TIES.append((v, n))
    return (fmt(v, n) + ' ' + u).strip()
def Rd(v, n): return D(fmt(v, n).replace(' x 10^', 'e').rstrip('.'))
def chain(a, n, m, up=False):
    """amount after n halvings (or doublings): m=0 exact; m=1 every step rounded to a's s.f."""
    v = D(a); k = sf(a)
    for _ in range(n):
        v = v * 2 if up else v / 2
        if m: v = Rd(v, k)
    return v
def AMT(a, n, u, m): return U(chain(a, n, m), sf(a), u)
def BACK(a, n, u, m): return U(chain(a, n, m, True), sf(a), u)
def PCT(fr): s = format(D(100) * fr, 'f'); return (s.rstrip('0').rstrip('.') if '.' in s else s) + '%'
def whole(x, what):
    if D(x) != D(x).to_integral_value(): err.append('%s: %s is not a whole number of half-lives' % (what, x)); return 0
    return int(D(x))
def n_from(t, h, what, conv=1): return whole(D(t) * conv / D(h), what)
def n_amounts(a, b, what): return whole(D(math.log2(D(a) / D(b))) if (D(a) / D(b)) == 2 ** round(math.log2(D(a) / D(b))) else D('0.5'), what)
def AGE(n): return U(5730 * D(n), 3, 'years')
def HLs(name): return HL[name][0]

CALC = []
def calc(sub, givens, specs, hl=None): CALC.append((sub, givens, specs, hl))
# ---- ch14-radiation ----
calc('activity of 18.0 mCi', ['18.0'], {0: lambda m: U(D('18.0') / 1000 * D('3.7e10'), 3, 'Bq'), 1: lambda m: U(D('18.0') * D('3.7e10'), 3, 'Bq'),
     2: lambda m: U(D('18.0') / 1000 / D('3.7e10'), 3, 'Bq'), 3: lambda m: U(D('18.0') * 1000 * D('3.7e10'), 3, 'Bq')})
calc('dose of 0.250 rem', ['0.250'], {0: lambda m: U(D('0.250') / 100 * 1000, 3, 'mSv'), 1: lambda m: U(D('0.250') * 100, 3, 'mSv'),
     2: lambda m: U(D('0.250') / 100, 3, 'mSv'), 3: lambda m: U(D('0.250') * 1000, 3, 'mSv')})
calc('activity of 6.40 mCi', ['6.40'], {0: lambda m: U(D('6.40') * D('3.7e7') / D('1e6'), 3, 'MBq'), 1: lambda m: U(D('6.40') / 37, 3, 'MBq'),
     2: lambda m: U(D('6.40') * D('3.7e7'), 3, 'MBq'), 3: lambda m: U(D('6.40') * D('3.7e10') / D('1e6'), 3, 'MBq')})
# ---- ch14-halflife: amounts after n half-lives ----
def _amt(a, t, iso, u, kinds, conv=1):
    n = n_from(t, HLs(iso), iso, conv)
    K = {'n': lambda m: AMT(a, n, u, m), 'n+1': lambda m: AMT(a, n + 1, u, m), 'n-1': lambda m: AMT(a, n - 1, u, m),
         '/2n': lambda m: U(D(a) / (2 * n), sf(a), u), 'xn/2': lambda m: U(D(a) * n / 2, sf(a), u),
         'sub': lambda m: (lambda v: (fmt(v, sf(a)) if v else '0') + ' ' + u)(max(D(0), D(a) - n * D(a) / 2)),
         'units': lambda m: U(D(a) * D(2) ** (-D(t) / D(HLs(iso))), sf(a), u)}
    return {j: K[k] for j, k in enumerate(kinds)}
calc('sodium-24. How much remains after 45.0 h', ['6.40', '45.0', '15.0'], _amt('6.40', '45.0', 'sodium-24', 'mg', ['n', '/2n', 'xn/2', 'n+1']), 'sodium-24')
calc('capsule contains 9.60 mCi', ['9.60', '32'], _amt('9.60', '32', 'iodine-131', 'mCi', ['n', 'n+1', '/2n', 'xn/2']), 'iodine-131')
calc('activity of 2.40 GBq', ['2.40', '138.9'], _amt('2.40', '138.9', 'samarium-153', 'GBq', ['n', 'n-1', 'n+1', '/2n']), 'samarium-153')
calc('activity of 14.0 mCi when it leaves the cyclotron', ['14.0', '5.5'], _amt('14.0', '5.5', 'fluorine-18', 'mCi', ['n', 'units', 'n+1', '/2n'], 60), 'fluorine-18')
calc('contains 6.80 mCi of xenon-133', ['6.80', '15.75', '5.25'], _amt('6.80', '15.75', 'xenon-133', 'mCi', ['n', 'n+1', '/2n', 'xn/2']), 'xenon-133')
calc('activity of 3.60', ['3.60', '55.4', '27.7'], _amt('3.60', '55.4', 'chromium-51', 'µCi', ['n', 'n-1', 'sub', 'n+1']), 'chromium-51')
calc('activity of 7.20 GBq', ['7.20', '26.6', '6.65'], _amt('7.20', '26.6', 'lutetium-177', 'GBq', ['n', 'n-1', 'n+1', 'xn/2']), 'lutetium-177')
# ---- percent left ----
def _pc(t, iso, kinds):
    n = n_from(t, HLs(iso), iso)
    K = {'n': lambda m: PCT(D(1) / 2 ** n), 'n-1': lambda m: PCT(D(1) / 2 ** (n - 1)), 'n-2': lambda m: PCT(D(1) / 2 ** (n - 2)),
         'n+1': lambda m: PCT(D(1) / 2 ** (n + 1)), 'dec': lambda m: PCT(1 - D(1) / 2 ** n)}
    return {j: K[k] for j, k in enumerate(kinds)}
calc('remains after 10.54 years', ['10.54'], _pc('10.54', 'cobalt-60', ['n', 'n-1', 'n+1', 'dec']), 'cobalt-60')
calc('left after 19.0 days', ['19.0'], _pc('19.0', 'radon-222', ['n', 'n-1', 'n-2', 'dec']), 'radon-222')
calc('remains after 3 half-lives', ['3'], {0: lambda m: PCT(D(1) / 8), 1: lambda m: U(D(100) / 6, 3, '').strip() + '%', 2: lambda m: PCT(D(1) / 16), 3: lambda m: PCT(1 - D(1) / 8)})
# ---- time from amounts; half-life from data; starting amount ----
def _time(a, b, iso, u, kinds):
    n = n_amounts(a, b, iso); h = HLs(iso)
    K = {'n': lambda m: U(n * D(h), sf(h), u), 'n+1': lambda m: U((n + 1) * D(h), sf(h), u), '2^n': lambda m: U(2 ** n * D(h), sf(h), u),
         'h/n': lambda m: U(D(h) / n, sf(h), u)}
    return {j: K[k] for j, k in enumerate(kinds)}
calc('for a 24.0 &mu;Ci sample to decay to 3.00', ['24.0', '3.00', '14.3'], _time('24.0', '3.00', 'phosphorus-32', 'days', ['n', 'n+1', '2^n', 'h/n']), 'phosphorus-32')
calc('10.4 Ci source to decay to 2.60 Ci', ['10.4', '2.60', '73.8'], _time('10.4', '2.60', 'iridium-192', 'days', ['n', 'n+1', 'h/n', '2^n']), 'iridium-192')
def _hlife(a, b, t, u, kinds):
    n = n_amounts(a, b, 'data')
    K = {'t/n': lambda m: U(D(t) / n, sf(t), u), 't': lambda m: t + ' ' + u, 't/(n+1)': lambda m: U(D(t) / (n + 1), sf(t), u),
         't/(n-1)': lambda m: U(D(t) / (n - 1), sf(t), u), 't/2^n': lambda m: U(D(t) / 2 ** n, sf(t), u)}
    return {j: K[k] for j, k in enumerate(kinds)}
calc('A 9.60 mg sample of a radioisotope decays to 1.20 mg in 21.6 days', ['9.60', '1.20', '21.6'], _hlife('9.60', '1.20', '21.6', 'days', ['t/n', 't', 't/(n+1)', 't/2^n']))
calc('A 6.40 g sample of a short-lived radioisotope decays to 0.400 g in 34.8 min', ['6.40', '0.400', '34.8'], _hlife('6.40', '0.400', '34.8', 'min', ['t/n', 't', 't/(n+1)', 't/(n-1)']))
def _start(a, t, iso, u, kinds):
    n = n_from(t, HLs(iso), iso)
    K = {'n': lambda m: BACK(a, n, u, m), 'n-1': lambda m: BACK(a, n - 1, u, m), 'n+1': lambda m: BACK(a, n + 1, u, m),
         'xn': lambda m: U(D(a) * n, sf(a), u), 'halve': lambda m: AMT(a, n, u, m)}
    return {j: K[k] for j, k in enumerate(kinds)}
calc('9.78 days after it was made', ['0.650', '9.78', '3.26'], _start('0.650', '9.78', 'gallium-67', 'mCi', ['n', 'n-1', 'n+1', 'xn']), 'gallium-67')
calc('8.40 days after a dose was made', ['0.600', '8.40', '2.80'], _start('0.600', '8.40', 'indium-111', 'mCi', ['n', 'halve', 'n-1', 'xn']), 'indium-111')
_n8 = n_amounts('8', '1', 'Tc 1/8')
calc('does only 1/8 of its activity remain', ['1/8'], {0: lambda m: U(_n8 * D('6.0'), 2, 'h'), 1: lambda m: U(8 * D('6.0'), 2, 'h'), 2: lambda m: U((_n8 + 1) * D('6.0'), 2, 'h'), 3: lambda m: U(D('6.0') / _n8, 2, 'h')}, 'technetium-99m')
TABLE = {}
def _tab(q):
    rows = [(D(r[0]), D(r[1])) for r in q['f'][0]['rows']]
    iv = [rows[i + 1][0] - rows[i][0] for i in range(len(rows) - 1)]
    halv = all(rows[i + 1][1] * 2 == rows[i][1] for i in range(len(rows) - 1))
    ok(halv and len(set(iv)) == 1 and rows[0][0] == 0, '%s table halves at a constant interval %s' % (q['id'], [str(x) for x in iv]))
    TABLE.update(hl=q['f'][0]['rows'][1][0], tot=q['f'][0]['rows'][-1][0], quarter=q['f'][0]['rows'][2][0])
calc('The table shows the mass of an unknown radioisotope', [], {0: lambda m: TABLE['hl'] + ' h', 1: lambda m: TABLE['tot'] + ' h', 2: lambda m: TABLE['quarter'] + ' h',
     3: lambda m: U(D(TABLE['hl']) / 2, sf(TABLE['hl']), 'h')})
# ---- ch14-dating ----
def _age(n, kinds):
    K = {'n': lambda m: AGE(n), 'n+1': lambda m: AGE(n + 1), '2^n': lambda m: AGE(2 ** n), 'x2^n': lambda m: U(5730 * 2 ** n, 3, 'years'),
         '/2^n': lambda m: U(D(5730) / 2 ** n, 3, 'years')}
    return {j: K[k] for j, k in enumerate(kinds)}
calc('gives 3.40 decays per minute', ['13.6', '3.40'], _age(n_amounts('13.6', '3.40', 'C-14'), ['n', '2^n', '/2^n', 'n+1']), 'carbon-14')
calc('gives 1.70 decays per minute per gram of carbon. Fresh wood', ['13.6', '1.70'], _age(n_amounts('13.6', '1.70', 'C-14'), ['n', '2^n', '/2^n', 'n+1']), 'carbon-14')
calc('gives 0.200 counts per minute', ['12.8', '0.200'], _age(n_amounts('12.8', '0.200', 'C-14'), ['n', 'x2^n', 'n+1', '/2^n']), 'carbon-14')
calc('1/128 of the carbon-14', ['1/128'], _age(n_amounts('128', '1', 'C-14'), ['n', 'n+1', 'x2^n', '/2^n']), 'carbon-14')
_nt = n_amounts('4', '1', 'H-3')
calc('1/4 of the tritium', ['12.3', '1/4'], {0: lambda m: U(_nt * D('12.3'), 3, 'years'), 1: lambda m: U(4 * D('12.3'), 3, 'years'),
     2: lambda m: U((_nt + 1) * D('12.3'), 3, 'years'), 3: lambda m: U(1 * D('12.3'), 3, 'years')}, 'hydrogen-3')
# ---- ch14-health / ch14-medicine: inverse-square law ----
def _inv(r, d1, d2):
    k = D(d2) / D(d1); n = min(sf(r), sf(d1), sf(d2))
    return {0: lambda m: U(D(r) / k ** 2, n, 'µSv/h'), 'lin': lambda m: U(D(r) / k, n, 'µSv/h'), 'half': lambda m: U(D(r) / 2, n, 'µSv/h'),
            '2k': lambda m: U(D(r) / (2 * k), n, 'µSv/h'), 'cube': lambda m: U(D(r) / k ** 3, n, 'µSv/h')}
_i1 = _inv('48', '1.0', '4.0'); _i2 = _inv('64', '0.50', '2.0')
calc('dose rate of 48 µSv/h at 1.0 m', ['48', '1.0', '4.0'], {0: _i1[0], 1: _i1['lin'], 2: _i1['2k'], 3: _i1['half']})
calc('0.50 m from a sealed gamma source is 64', ['64', '0.50', '2.0'], {0: _i2[0], 1: _i2['lin'], 2: _i2['half'], 3: _i2['cube']})
_i3 = _inv('54', '2.0', '6.0')
calc('where the dose rate is 54', ['54', '2.0', '6.0'], {0: _i3[0], 1: _i3['lin'], 2: _i3['half'], 3: lambda m: U(D('54') / 6, 2, 'µSv/h')})

print('Calculation items: key and distractors recomputed (exact = halving chain rounded each step, and = the choice as written)')
checked, hand = set(), set()
def by(sub):
    m = [q for q in ALL if sub in txt(q['q'])]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
for sub, givens, specs, hl in CALC:
    q = by(txt(sub))
    if not q: continue
    checked.add(q['id']); stem = txt(q['q'])
    if q.get('f') and q['f'][0]['type'] == 'table': _tab(q)
    for gv in givens:
        if not re.search(r'(?<![\d.])' + re.escape(gv) + r'(?![\d])', stem): err.append(q['id'] + ' given %r not in stem as written' % gv)
    if hl and not re.search(r'(?<![\d.])' + re.escape(HL[hl][0]) + r'(?![\d])', stem): err.append('%s stem does not show the %s half-life %s' % (q['id'], hl, HL[hl][0]))
    print('  %s %s' % (q['id'], txt(sub)[:52]))
    keys = []; TIES.clear()
    for j, fn in sorted(specs.items()):
        try: a, b = fn(0), fn(1)
        except Exception as e_: err.append('%s c[%d] spec failed: %r' % (q['id'], j, e_)); continue
        if a != b: err.append('%s c[%d] ambiguous: %s (exact) vs %s (step-by-step)' % (q['id'], j, a, b))
        keys.append(a)
        ok(txt(q['c'][j]).strip() == a, '%s c[%d] %-26r = %r' % (q['id'], j, txt(q['c'][j]).strip(), a))
    if TIES: err.append('%s a computed value is a rounding tie: %s' % (q['id'], TIES[:2]))
    if len(set(keys)) != 4: err.append(q['id'] + ' recomputed values not all different: %s' % keys)
    k0 = keys[0].split(' ')[0] if keys else ''
    if k0 and k0 not in txt(q['w']): err.append(q['id'] + ' answer %s not in w' % k0)
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')

# ---------- quoted half-lives and unit definitions ----------
print('Quoted half-lives and unit definitions')
nh = 0
ISO = r'([A-Za-z]+)-(\d+m?)\b|\b(tritium|Tritium)\b'
for q in ALL:
    stem_isos = [(a.lower() + '-' + b) if a else 'hydrogen-3' for a, b, c in re.findall(ISO, txt(q['q']))]
    for h in [q['q'], q['h'], q['w'], q['c'][0]] + q['y']:
        t = txt(h)
        for m in re.finditer(r'half-life (?:of |is )?(?:only |about )?([\d.]+(?: x 10\^\d+)?) ?(minutes|min|hours|h|days|years)\b', t):
            pre = [(a.lower() + '-' + b) if a else 'hydrogen-3' for a, b, c in re.findall(ISO, t[:m.start()])]
            pre = [p for p in pre if p in HL] or [p for p in stem_isos if p in HL]
            nh += 1
            if not pre: err.append('%s half-life %s %s with no isotope' % (q['id'], m.group(1), m.group(2))); continue
            if HL[pre[-1]] != (m.group(1), UNORM[m.group(2)]): err.append('%s quotes %s half-life %s %s; table %s' % (q['id'], pre[-1], m.group(1), m.group(2), HL[pre[-1]]))
        for v in re.findall(r'1 Ci = ([\d.]+ x 10\^\d+) Bq', t):
            if v != '3.7 x 10^10': err.append('%s quotes 1 Ci = %s Bq' % (q['id'], v))
        for v in re.findall(r'1 Sv = (\d+) rem', t):
            if v != '100': err.append('%s quotes 1 Sv = %s rem' % (q['id'], v))
        for v in re.findall(r'1 Gy = (\d+) J/kg', t):
            if v != '1': err.append('%s quotes 1 Gy = %s J/kg' % (q['id'], v))
        for v in re.findall(r'1 mCi = (\d+) MBq', t):
            if v != '37': err.append('%s quotes 1 mCi = %s MBq' % (q['id'], v))
        for v in re.findall(r'1 rem = (\d+) mSv', t):
            if v != '10': err.append('%s quotes 1 rem = %s mSv' % (q['id'], v))
print('    %d half-lives quoted, all against the table' % nh)

# ---------- conceptual items: key tables ----------
print('Conceptual items checked against key tables')
def chk(sub, cond, msg):
    q = by(txt(sub))
    if q:
        checked.add(q['id'])
        try: r = cond(q)
        except Exception as e_: r = False; msg += ' (%r)' % e_
        ok(r, '%s %s' % (q['id'], msg))
def P0(q): return plain(q['c'][0])
def ptype(c):
    p = plain(c)
    for k in ('alpha', 'beta', 'gamma'):
        if p.startswith(k): return k
    return None
for q in ALL:
    if q['id'] in eq_checked: checked.add(q['id'])
# decay classification of stem equations
for sub, want in (('What kind of decay is this? ', None), ('Classify this reaction', None)):
    for q in [q for q in ALL if txt(sub) in txt(q['q'])]:
        e = STEM_EQ[q['id']][0]; k = classify(e)
        others = [plain(c) for c in q['c'][1:]]
        ok(P0(q) == k and k not in others, '%s decay type from the equation = %s' % (q['id'], k)); checked.add(q['id'])
chk('Which symbol represents a beta particle', lambda q: nuclides(q['c'][0])[0][:3] == PARTICLE['beta particle'] and all(nuclides(c)[0][:3] != PARTICLE['beta particle'] for c in q['c'][1:]), 'beta = 0/-1 e')
chk('mass number of 0 and a charge of 0', lambda q: nuclides(q['c'][0])[0][:2] == (0, 0) and all(nuclides(c)[0][:2] != (0, 0) for c in q['c'][1:]), 'only c[0] has A = 0, Z = 0')
_al = PARTICLE['alpha particle']
chk('number (Z) of a nucleus that gives off an alpha particle', lambda q: P0(q) == 'a decreases by %d, and z decreases by %d' % (_al[0], _al[1]), 'alpha: A - 4, Z - 2')
_po = PARTICLE['positron']
chk('during <b>positron emission</b>', lambda q: 'z decreases by %d' % _po[1] in P0(q) and 'a stays the same' in P0(q), 'positron: Z - 1, A same')
chk('the most penetrating', lambda q: ptype(q['c'][0]) == max(PEN, key=PEN.get), 'penetrating: gamma > beta > alpha')
chk('makes the most ions per centimeter', lambda q: ptype(q['c'][0]) == max(ION, key=ION.get) == min(PEN, key=PEN.get) and 'paper' in SHIELD['alpha'], 'most ionizing, stopped by paper = alpha')
chk('the lowest ionizing power', lambda q: ptype(q['c'][0]) == min(ION, key=ION.get), 'lowest ionizing = gamma')
chk('Outside the body, which kind of radiation', lambda q: ptype(q['c'][0]) == max(PEN, key=PEN.get), 'outside the body: most penetrating')
def _shield(q):
    rows = {r[0]: int(r[1].replace(',', '')) for r in q['f'][0]['rows']}
    bg = rows['Lead, 2 cm']; alpha = rows['Paper'] < 0.5 * rows['None']; gamma = rows['Aluminum, 3 mm'] > 2 * bg
    beta = rows['Paper'] - rows['Aluminum, 3 mm'] > 0.5 * rows['None']
    want = 'beta particles only' if (beta and not alpha and not gamma) else '?'
    return P0(q) == want
chk('places different shields between', _shield, 'shield table: no drop with paper, background with aluminum -> beta only')
chk('pure beta emitter, phosphorus-32', lambda q: any(w in P0(q) for w in SHIELD['beta']) and not any(w in P0(q) for w in SHIELD['gamma']), 'beta shield: aluminum/plastic/lab coat')
chk('labeled with its activity', lambda q: UNITS[P0(q).split(' ')[0]] == 'activity' and all(UNITS[plain(c).split(' ')[0].rstrip(',')] != 'activity' for c in q['c'][1:]), 'activity unit = becquerel')
chk('What does a dose in grays describe', lambda q: UNITS['gray'] == 'absorbed' and 'energy absorbed per kilogram' in P0(q) and '1 gy = 1 j/kg' in P0(q), 'gray = absorbed dose, J/kg')
chk('What does a <b>sievert</b>', lambda q: UNITS['sievert'] == 'equivalent' and P0(q).startswith('the equivalent'), 'sievert = equivalent dose')
chk('How does a Geiger counter detect', lambda q: 'ionizes the gas' in P0(q), 'Geiger: ion pulses in a gas')
chk('In a scintillation counter, what does', lambda q: 'flashes of light' in P0(q) and 'crystal' in P0(q), 'scintillation = light flashes from a crystal')
chk('dosimeter badge at the collar', lambda q: 'total radiation dose' in P0(q), 'dosimeter = total dose')
chk('check her gloves', lambda q: 'geiger' in P0(q), 'survey meter = Geiger counter')
def _pn(q):
    nm, A = re.search(r'([a-z]+)-(\d+) nucleus', txt(q['q']).lower()).groups(); z = PT[NAME[nm]]; A = int(A)
    return P0(q) == '%d protons and %d neutrons' % (z, A - z) and plain(q['c'][1]) == '%d protons and %d neutrons' % (A - z, z)
chk('protons and neutrons are in one strontium-90', _pn, 'protons = Z, neutrons = A - Z (and the swap distractor)')
chk('protons and neutrons are in one cesium-137', _pn, 'protons = Z, neutrons = A - Z (and the swap distractor)')
def _beyond(q):
    z = lambda c: PT[NAME[re.match(r'([a-z]+)-', plain(c)).group(1)]]
    return z(q['c'][0]) > 83 and all(z(c) <= 83 for c in q['c'][1:])
chk('must be radioactive, without', _beyond, 'only c[0] has Z > 83')
chk('What was new about the rays Henri Becquerel', lambda q: 'uranium' in P0(q) and 'no tube' in P0(q), 'Becquerel: uranium gave off rays on its own')
chk('Marie and Pierre Curie discover', lambda q: P0(q) == 'polonium and radium', 'Curies: polonium and radium')
chk('named one of the elements she discovered for her home country', lambda q: P0(q) == 'polonium', 'polonium for Poland')
chk('use fluorine-18 FDG within a few hours', lambda q: HL['fluorine-18'][0] + ' ' + HL['fluorine-18'][1] in P0(q) and hl_years('fluorine-18') < D(1) / 365, 'F-18: 110 min half-life')
def _img2(q):
    return P0(q).startswith('iodine-123') and hl_years('iodine-123') < hl_years('iodine-131') and 'beta' in EMIT['iodine-131'] and 'beta' not in EMIT['iodine-123']
chk('better for <b>imaging</b> the thyroid', _img2, 'I-123 (gamma, shorter) over I-131 (beta)')
chk('one particular cobalt-60 nucleus', lambda q: 'random' in P0(q) and HL['cobalt-60'][0] + ' years' in txt(q['q']), 'decay is random per nucleus')
chk('cooled in a freezer', lambda q: P0(q).startswith('nothing') and HL['technetium-99m'][0] + ' h' in P0(q), 'half-life independent of temperature')
chk('completely gone, because half of it decays', lambda q: fmt(D('6.0') / 4, 2) + ' mg' in P0(q), '6.0 -> 3.0 -> 1.5 mg')
chk('What is the correct first step', lambda q: 'n = %d' % n_from('60.0', HL['sodium-24'][0], 'Na-24') in P0(q), 'n = 60.0/15.0')
def _plot(q):
    s = dict((x, y) for x, y in q['f'][0]['series'][1]['pts']); y0 = s[0]
    t = [x for x, y in s.items() if y == y0 / 2][0]
    smooth = q['f'][0]['series'][0]['pts']; good = all(abs(y - y0 * 0.5 ** (x / t)) < 0.01 for x, y in smooth)
    return good and P0(q) == '%g h' % t
chk('The graph shows the activity of a radioactive sample', _plot, 'half-life read from the plotted curve')
chk('An animal dies', lambda q: P0(q).startswith('it decreases'), 'after death C-14 decays, not replaced')
LIVING = ('wood', 'bone', 'charcoal', 'seed', 'shell', 'cloth', 'paper', 'leather', 'food', 'ivory')
NONLIV = ('obsidian', 'copper', 'granite', 'clay', 'bronze', 'stone', 'metal', 'ochre', 'iron oxide')
chk('red ochre, a mineral', lambda q: P0(q).startswith('only the charcoal') and 'charcoal' in LIVING and 'ochre' in NONLIV, 'charcoal once-living, ochre mineral')
chk('clay pot with charred food', lambda q: 'charred food' in P0(q) and 'clay' in NONLIV, 'food residue datable, clay not')
chk('about 200,000 years old', lambda q: 'about %d half-lives' % round(200000 / 5730) in P0(q), '200,000 / 5730 = %.1f half-lives' % (200000 / 5730))
def _datiso(age):
    def f(q):
        def usable(c):
            nm = re.match(r'([a-z]+-\d+m?)', plain(c)).group(1); return D(age) / hl_years(nm) <= 10 and (nm != 'carbon-14' or D(age) <= 50000)
        return usable(q['c'][0]) and not any(usable(c) for c in q['c'][1:])
    return f
chk('volcanic rock thought to be about 2 million', _datiso(2000000), 'only c[0] has age/half-life <= 10')
chk('about as old as Earth, about 4.5 billion', _datiso(4500000000), 'only c[0] has age/half-life <= 10')
chk('about 1500 years old or about 3000', lambda q: 1500 < 5730 and 3000 < 5730 and P0(q).startswith('less than living bone'), 'both < 1 half-life: less, older less')
chk("reactor's <b>control rods</b> made of", lambda q: 'absorb neutrons' in P0(q) and ('boron' in P0(q) or 'cadmium' in P0(q)), 'control rods: boron/cadmium absorb neutrons')
chk('energy released by fusion compare', lambda q: P0(q).startswith('fusion releases even more'), 'fusion > fission per gram (14.5)')
chk('water flows through the core', lambda q: 'slows the neutrons' in P0(q) and 'heat' in P0(q), 'water = moderator + coolant')
chk('correctly compares fission and fusion', lambda q: P0(q).startswith('fission splits a heavy nucleus; fusion joins light nuclei'), 'fission splits, fusion joins')
chk('How is carbon-14 made', lambda q: (lambda e: balanced(e) and heavy(e) == frozenset({'N-14', 'C-14'}) and (1, 0, 'n') in {n[:3] for c, n in e[0]})(equations(q['c'][0])[0]), 'N-14 + n -> C-14 + p')
chk("Mateo Herrera's V/Q lung scan uses technetium-99m", lambda q: 'gamma' in P0(q) and HL['technetium-99m'][0] + ' h' in P0(q), 'Tc-99m: gamma, 6.0 h')
chk("seeps from the soil into a home's basement", lambda q: P0(q).startswith('the lungs') and max(ION, key=ION.get) == 'alpha', 'radon: inhaled alpha, lungs')
chk('sterilized with gamma rays rather than beta', lambda q: 'penetrate' in P0(q) and PEN['gamma'] > PEN['beta'], 'gamma more penetrating than beta')
chk('How do X-rays differ from gamma rays', lambda q: 'outside the nucleus' in P0(q) and 'switched off' in P0(q), 'X-rays from a tube, gamma from nuclei')
chk('cuts her time at the bedside from 20 minutes to 10', lambda q: P0(q) == 'it is cut in half', 'dose = rate x time')
chk('steps back from a patient, works faster', lambda q: P0(q).startswith('alara'), 'time, distance, shielding = ALARA')
chk('painted glowing watch dials', lambda q: 'alpha' in P0(q) and 'inside' in P0(q) and max(ION, key=ION.get) == 'alpha', 'swallowed alpha emitter: damage from inside')
chk('Patients fast for several hours', lambda q: 'compete' in P0(q), 'glucose competes with FDG')
chk('Why is fluorine-18 FDG useful', lambda q: 'positron' in P0(q) and 'two gamma rays' in P0(q) and EMIT['fluorine-18'] == {'positron'}, 'F-18 positron -> 2 gamma')

# ---------- course rule: trailing zeros in calculation stems ----------
print('Trailing-zero rule in calculation stems; every k=1 item recomputed')
for q in ALL:
    if q['k'] == 1:
        s = NUC.sub(' ', q['q']); s = txt(s)
        s = re.sub(r'half-life 110 min', '', s); s = re.sub(r'5730 years', '', s)
        s = re.sub(r'\b[A-Za-z]+-\d+m?\b', '', s); s = re.sub(r'1 (?:Sv|Ci|MBq|mCi) = [^)]*', '', s)
        for m in re.finditer(r'(?<![\d.^,/])(\d*[1-9]\d*0)(?![\d.^,])', s):
            err.append(q['id'] + ' calculation stem has ambiguous trailing-zero value %r' % m.group(1))
        if q['id'] not in checked: err.append(q['id'] + ' calculation item not recomputed')
for q in ALL:
    if q['id'] not in checked: hand.add(q['id'])

# ---------- draft overlap ----------
print('Draft overlap: no stem reuses a worked example or exercise from drafts/ch14')
GIV = r'(\d+\.\d+|\d+\.|\d+)(?: x 10\^(-?\d+))? ?(mCi|µCi|GBq|MBq|Bq|Ci|mSv|µSv/h|µSv|Sv|rem|mg|g|min|minutes|h|hours|days|years|m|%|counts|decays)(?![A-Za-z/])'
CONST = {'110', '6.0', '13', '3.8', '8.0', '14.3', '5.27', '5730', '12.3', '1.25', '4.5', '15.0', '3.26', '5.25', '27.7', '6.65', '2.80',
         '73.8', '1', '2', '3', '4', '5', '10', '100', '0', '1.0', '60', '50,000', '3.7', '1000', '6', '12'}
def givens_in(t):
    t = re.sub(r'\b[A-Za-z]+-\d+m?\b', ' ', t)
    return {(a + ('e' + b if b else ''), u.replace('minutes', 'min').replace('hours', 'h')) for a, b, u in re.findall(GIV, t) if a not in CONST}
BANNED = {('4.00', 'mCi'), ('80.0', 'mg'), ('24.0', 'days'), ('40.0', 'mCi'), ('5.00', 'mCi'), ('200.', 'mg'), ('25.0', 'mg'), ('30.0', 'h'),
          ('0.500', 'mg'), ('12.0', 'mCi'), ('64.0', 'mg'), ('4.00', 'mg'), ('2.40', 'g'), ('15.81', 'years'), ('550', 'min'), ('40.0', 'mg'),
          ('16.0', 'days'), ('20.0', 'mCi'), ('25.0', '%'), ('12.5', '%'), ('16.0', 'counts'), ('1.00', 'counts'), ('50.0', '%'), ('6.25', '%'),
          ('10.0', 'mCi'), ('2.50e6', 'Bq'), ('36', 'µSv/h'), ('20.', 'µSv/h'), ('0.50', 'h'), ('18', 'h'), ('24', 'h')}
LTX = re.compile(r'(?:(\d+)\\,\s*)?\{\}\^\{(\d+)(\\text\{m\})?\}_\{([-+]?\d+)\}\\(?:text\{([A-Za-z]+)\}|(gamma))')
def draft_sig(eq):
    if eq.count('\\rightarrow') != 1: return None
    sides = []
    for part in eq.split('\\rightarrow'):
        c = collections.Counter()
        for co, A, mt, z, sym, gm in LTX.findall(part):
            c[(int(A), int(z), 'γ' if gm else sym, 'm' if mt else '')] += int(co or 1)
        sides.append(frozenset(c.items()))
    return tuple(sides) if all(sides) else None
blocks = []; draft_eqs = []
for p_ in sorted(glob.glob(os.path.join(ROOT, 'drafts', 'ch14', '*.html'))):
    h = open(p_, encoding='utf-8').read()
    for b in re.split(r'(?=Example \\\(\\PageIndex|Exercise \\\(\\PageIndex|<h2|Problem 14\.\d+\b)', h):
        if not re.match(r'(Example|Exercise|Problem)', b): continue
        for eq in re.split(r'<p|<li', b):
            if '\\rightarrow' not in eq: continue
            for piece in re.split(r'\\qquad|\\\)', eq):
                dsg = draft_sig(piece)
                if dsg: draft_eqs.append((os.path.basename(p_), None, dsg))
        t = re.sub(r'\\\(|\\\)|\\dfrac|\\text|\\times|\\ |\\qquad|\\left|\\right|\\cdot|\\tfrac|\\,|\\;', ' ', b).replace('\\mu', 'µ')
        t = txt(re.sub(r'[{}]', ' ', t)); t = re.sub(r'\s+', ' ', t)
        nm = os.path.basename(p_) + ' ' + ' '.join(t.split()[:3])
        blocks.append((nm, givens_in(t), t.split(' Answer')[0]))
W = lambda s_: set(w for w in re.findall(r'[a-z0-9.]+', s_.lower()) if len(w) > 2)
nover = 0; notes = []
for q in ALL:
    qt = txt(q['q']); qg = givens_in(qt); qw = W(qt)
    for g_ in qg & BANNED:
        nover += 1; err.append('%s uses the draft worked-example given %s %s' % (q['id'], *g_))
    for nm, gs, bt in blocks:
        if len(qg & gs) >= 2:
            nover += 1; err.append('%s shares givens %s with %s' % (q['id'], sorted(qg & gs), nm))
        bw = W(bt); j = len(qw & bw) / max(1, len(qw | bw))
        if j > 0.45: nover += 1; err.append('%s stem is %.2f similar to %s' % (q['id'], j, nm))
        elif j > 0.3: notes.append('%s stem %.2f similar to %s (checked by hand)' % (q['id'], j, nm))
    if q['id'] in STEM_EQ:
        e, fill = STEM_EQ[q['id']]
        hs = heavy(e, fill); sg = sig(e, fill)
        for nm, dh, dsg in draft_eqs:
            if sg == dsg: nover += 1; err.append('%s stem equation %s is a draft example/exercise equation (%s)' % (q['id'], sorted(hs), nm))
print('    %d draft Example/Exercise blocks and %d draft equations compared; %d overlaps' % (len(blocks), len(draft_eqs), nover))
for n_ in notes: print('    NOTE', n_)
pp = os.path.join(ROOT, 'drafts', 'ch14', '14.8_practice_problems.html')
print('    14.8 Practice Problems:', 'compared' if os.path.exists(pp) else 'not written yet (re-run after it exists)')

# ---------- Mateo, coverage, counts, duplicates ----------
mateo = [q['id'] for q in ALL if 'Mateo' in ' '.join(fields(q))]
if len(mateo) > 2: err.append('Mateo appears in %d items (max 2): %s' % (len(mateo), mateo))
print('Mateo items:', mateo)
normq = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip().lower()
for nm, B in (('Try It', TRY), ('ADAPT', HW)):
    c_ = collections.Counter(normq(q['q']) for q in B)
    d_ = [k for k, v in c_.items() if v > 1]
    if d_: err.append('%s repeats a stem: %s' % (nm, d_))
dup = set(normq(q['q']) for q in TRY) & set(normq(q['q']) for q in HW)
if dup: err.append('same question in both banks: %s' % dup)
for a in TRY:
    for b in HW:
        wa, wb = W(txt(a['q'])), W(txt(b['q'])); j = len(wa & wb) / max(1, len(wa | wb))
        if j > 0.6: err.append('%s and %s stems are %.2f similar' % (a['id'], b['id'], j))
        elif j > 0.45: print('    NOTE %s / %s stems %.2f similar (different item, checked by hand)' % (a['id'], b['id'], j))
print('Items with a machine check: %d of %d' % (len(checked), len(ALL)))
print('  conceptual (key read by hand; symbols, equations and quoted values still checked):', ' '.join(sorted(hand)) or 'none')
for nm, B in (('Try It', TRY), ('ADAPT', HW)):
    print(nm, len(B), dict(collections.Counter(q['t'] for q in B)), 'with figures:', sum(1 for q in B if q.get('f')),
          'd:', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1:', sum(q['k'] for q in B))
print('ERRORS:', err if err else 'none')
