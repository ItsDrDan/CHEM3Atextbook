#!/usr/bin/env python3
"""Checker for the Chapter 9 banks (energy, temperature, heat units, specific heat and calorimetry, phase changes
and heating curves, intermolecular forces, liquids and solids, vapor pressure and ranking). Structural checks as in
tools/check_bank_ch08.py (ch09 topic ids; ADAPT = 42 items, text only, y[0] begins "Correct: "; tables at most 3
columns; figures only of fbx types table/plot), plus, written independently of the generators:
  - temperature conversions computed two ways (strict: multiplication rule then addition rule on the rounded
    intermediate; and: carry the unrounded value, round once to the measurement's decimal places); the item is an
    error unless both agree, so every key is unambiguous under the Chapter 9 text's rules (32, 1.8, 273.15 exact);
  - every calculation item (k=1): the key and each numeric distractor's intended error recomputed with Decimal
    from the givens as written in the stem (q = mc(dT), dT = Tf - Ti, solving for dT, Tf, m, c; -q_hot = q_cold;
    q = n(dH) with H2O 18.015 g/mol from the yellow sheet; heating-curve sums with each step rounded to its
    significant figures in kJ and then added by the decimal-place rule, as in Section 9.5);
  - calorimetry data are physically consistent (heat lost by the metal matches heat gained by the water to 1.5%);
  - conceptual items: an intermolecular-force table (bonds -> polar? by the Chapter 6 rules with yellow-sheet
    electronegativities and SNAP, H on N/O/F -> hydrogen bonding, strongest force, electron count), a solid-type
    classifier (metal only -> metallic; metal + nonmetal -> ionic; diamond/graphite/SiO2/SiC -> covalent network;
    other nonmetals -> molecular), and ranking by solid type -> strongest force -> size are used to recheck keys;
    the heating-curve plot and the tables are read and rechecked; the rest are listed as read by hand;
  - course rule: no whole number ending in 0 without a decimal point in a calculation stem (100 °C, the normal
    boiling point, is exempt);
  - exactly one correct choice (recomputed values all different; four different choices);
  - no stem reuses a draft worked example or exercise (two shared givens with a draft block, or one of the listed
    worked-example givens); no stem in both banks.
usage: python3 tools/check_bank_ch09.py bank/ch09.json bank/ch09_adapt.json"""
import json, sys, re, os, collections, glob
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 50; getcontext().rounding = ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YS = json.load(open(os.path.join(ROOT, 'tools', 'yellow_sheet_masses.json')))
AM = YS['masses']; EN = {k: D(v) for k, v in YS['electronegativity'].items()}
TOP = {'ch09-energy', 'ch09-temp', 'ch09-units', 'ch09-specheat', 'ch09-phase', 'ch09-imf', 'ch09-solids', 'ch09-vapor'}
err = []

# ---------- text ----------
def txt(x):
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<[^>]+>', '', x)
    for a, b in (('&middot;', '·'), ('&minus;', '-'), ('−', '-'), ('&times;', 'x'), ('&nbsp;', ' '), ('&divide;', '/'),
                 ('&rarr;', '->'), ('&ldquo;', '"'), ('&rdquo;', '"'), ('&deg;', '°'), ('&Delta;', 'Δ'), ('&delta;', 'δ'),
                 ('&ndash;', '–'), ('&lt;', '<'), ('&gt;', '>'), ('&asymp;', '≈'), ('&amp;', '&')):
        x = x.replace(a, b)
    return x
def plain(x): return re.sub(r'\s+', ' ', txt(x)).strip().lower()

# ---------- structural checks ----------
OUT_OF_SCOPE = r"Hess|PV ?= ?nRT|ideal gas law|Clausius|enthalpy of formation|phase diagram|triple point|critical point|molality|all of the above|none of the above"
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
        if '{' in s or '}' in s: err.append(i + ' unconverted markup')
        if re.search(r'(?<![\w;])-(?=\d)', s): err.append(i + ' hyphen used as a minus sign')
        if re.search(OUT_OF_SCOPE, s, re.I): err.append(i + ' out of scope term or AOTA/NOTA')
        if 'f' in q and not allow_f: err.append(i + ' has f (ADAPT items must be text only)')
        for f in q.get('f', []):
            if f['type'] == 'table':
                if max(len(f['head']), *[len(r) for r in f['rows']]) > 3: err.append(i + ' table wider than 3 columns')
                if max(len(plain(x)) for r in f['rows'] + [f['head']] for x in r) > 32: err.append(i + ' table cell too long for a phone')
            elif f['type'] != 'plot': err.append(i + ' figure type not checked here: ' + f['type'])
        if label == 'HW' and not q['y'][0].startswith('Correct: '): err.append(i + ' ADAPT y[0] lacks "Correct: "')
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if right in plain(q['y'][j]): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c9-%03d', 'TRY', True)
structural(HW, 'c9-h%02d', 'HW', False)
if len(HW) != 42: err.append('ADAPT has %d items, not 42' % len(HW))
if sum(1 for q in TRY if q.get('f')) > 4: err.append('more than 4 figures')
fbx = open(os.path.join(ROOT, 'js', 'fbx.js'), encoding='utf-8').read()
for t_ in {f['type'] for q in TRY for f in q.get('f', [])}:
    if not re.search(r'[{,]%s:' % t_, fbx): err.append('figure type %s not supported by js/fbx.js' % t_)
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
def dec(s): return len(s.partition('.')[2]) if 'e' not in s.lower() else None
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
def plus(s): return s if s.startswith('-') else '+' + s
def back(s):
    """number string as written ('6.19 x 10^4', '160.') -> Decimal and its decimal places (None for sci)."""
    m = re.fullmatch(r'(-?[\d.]+)(?: x 10\^(-?\d+))?', s)
    v = D(m.group(1).rstrip('.') if m.group(1).endswith('.') else m.group(1)) * (D(10) ** int(m.group(2)) if m.group(2) else 1)
    if m.group(2): return v, -int(m.group(2)) + len(m.group(1).partition('.')[2])
    return v, len(m.group(1).partition('.')[2])
def addr(*strs):
    """sum of rounded values (strings as formatted) by the decimal-place rule."""
    vals = [back(s) for s in strs]; q = min(p for v, p in vals)
    return rq(sum(v for v, p in vals), q) if q >= 0 else fmt(sum(v for v, p in vals), len(str(int(abs(sum(v for v, p in vals))))) + q)

# ---------- temperature (two readings of the rules; they must agree) ----------
E32, E18, E273 = D(32), D('1.8'), D('273.15')
def C2K(C):  return rq(D(C) + E273, dec(C))
def K2C(K):  return rq(D(K) - E273, dec(K))
def F2C(F):
    d = rq(D(F) - E32, dec(F)); a = fmt(D(d) / E18, sf(d)); b = rq((D(F) - E32) / E18, dec(F))
    if a != b: err.append('F->C %s ambiguous: %s (strict) vs %s (decimal places)' % (F, a, b))
    return a
def C2F(C):
    p = fmt(E18 * D(C), sf(C)); a = rq(D(p) + E32, dec(p)); b = rq(E18 * D(C) + E32, dec(C))
    if a != b: err.append('C->F %s ambiguous: %s (strict) vs %s (decimal places)' % (C, a, b))
    return a
def F2K(F):
    c = F2C(F); a = C2K(c); b = rq((D(F) - E32) / E18 + E273, dec(c))
    if a != b: err.append('F->K %s ambiguous: %s (rounded C) vs %s (unrounded)' % (F, a, b))
    return a
def K2F(K):
    c = K2C(K); a = C2F(c); b = rq(E18 * (D(K) - E273) + E32, dec(c))
    if a != b: err.append('K->F %s ambiguous: %s vs %s' % (K, a, b))
    return a
for f_, c_ in (('212.0', '100.0'), ('50.0', '10.0'), ('-40.0', '-40.0'), ('98.6', '37.0')):
    if F2C(f_) != c_ or C2F(c_) != f_: err.append('checker anchor %s °F = %s °C fails' % (f_, c_))
print('Temperature anchors (212.0/100.0, 50.0/10.0, -40.0/-40.0, 98.6/37.0) and the draft examples reproduce:',
      F2C('103.5'), C2K(F2C('103.5')), K2C('77.4'), rq(E18 * (D('77.4') - E273) + E32, 1))
if (F2C('103.5'), K2C('77.4')) != ('39.7', '-195.8'): err.append('checker does not reproduce the 9.2 worked examples')

# ---------- constants (Chapter 9 text) ----------
CW, CICE, CSTEAM, CETH = D('4.184'), D('2.09'), D('2.01'), D('2.42')
C_ = {'water': '4.184', 'ice': '2.09', 'steam': '2.01', 'ethanol': '2.42', 'aluminum': '0.903', 'iron': '0.449',
      'copper': '0.385', 'silver': '0.235', 'gold': '0.128', 'lead': '0.128'}
HF_, HV_ = '6.02', '40.7'
def MMraw(f):
    c = atoms(f); return sum((D(AM[e]) * n for e, n in c.items()), D(0)), c
def atoms(f):
    tot = collections.Counter(); stack = [collections.Counter()]; i = 0
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
    raw, c = MMraw(f); q = min(len(AM[e].partition('.')[2]) for e in c)
    return raw.quantize(D(10) ** -q)
MW = MM('H2O')
if str(MW) != '18.015': err.append('checker H2O molar mass %s' % MW)
# the constants quoted anywhere must be the chapter's values
for q in ALL:
    s = txt(' '.join([q['q'], q['w']] + q['y']))
    for nm, v in re.findall(r'c for (\w+) = ([\d.]+)', s):
        if C_.get(nm) != v: err.append('%s quotes c for %s = %s' % (q['id'], nm, v))
    for v in re.findall(r'ΔHfus = ([\d.]+) (?:kJ/mol|J/g)', s):
        if v not in (HF_, '334'): err.append('%s quotes ΔHfus = %s' % (q['id'], v))
    for v in re.findall(r'ΔHvap = ([\d.]+) (?:kJ/mol|J/g)', s):
        if v != HV_: err.append('%s quotes ΔHvap = %s' % (q['id'], v))
    for v in re.findall(r'H2O ([\d.]+) g/mol', s):
        if v != str(MW): err.append('%s quotes H2O %s g/mol' % (q['id'], v))
    for st, v in re.findall(r'c(ice|water|steam) = ([\d.]+)', s):
        if C_[st] != v: err.append('%s quotes c%s = %s' % (q['id'], st, v))
print('Quoted specific heats, heats of fusion/vaporization and the H2O molar mass match the Chapter 9 text')

# ---------- heat helpers (strings as written in the stem) ----------
def dT(Tf, Ti):
    # 0 °C and 100 °C (water's normal melting and boiling points) are exact; otherwise the decimal-place rule
    ds = [dec(x) for x in (Tf, Ti) if x not in ('0', '100')]
    return rq(D(Tf) - D(Ti), min(ds))
def qmc(m, c, d): return D(m) * D(c) * D(d), min(sf(m), sf(c), sf(d))
def Sx(v, n, unit, sign=False):
    s = fmt(v, n); s = plus(s) if sign else s
    return s + ' ' + unit
def nH(g, H):  # grams -> mol -> kJ
    return D(g) / MW * D(H), min(sf(g), sf(H), 5)

# ---------- calculation items ----------
def by(sub):
    m = [q for q in ALL if sub in txt(q['q'])]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
checked, hand = set(), set()
UC = 'J/(g·°C)'
def F3(v, n, u): return fmt(v, n) + ' ' + u
CALC = []
def calc(sub, givens, specs): CALC.append((sub, givens, specs))

# ---- ch09-temp (Try It) ----
calc('temperature is 38.9 °C', ['38.9'], {0: (lambda: C2F('38.9') + ' °F', '1.8C + 32'),
     1: (lambda: rq(D(fmt(E18 * (D('38.9') + 32), 4)) , 1) + ' °F', 'added 32 first'),
     2: (lambda: fmt(D('38.9') / E18 + 32, 3) + ' °F', 'divided by 1.8'), 3: (lambda: C2K('38.9') + ' °F', 'added 273.15')})
calc('reads 96.8 °F', ['96.8'], {0: (lambda: F2C('96.8') + ' °C', '(F-32)/1.8'), 1: (lambda: rq(D('96.8') - E32 / E18, 1) + ' °C', 'no parentheses'),
     2: (lambda: fmt((D('96.8') - E32) * E18, 3) + ' °C', 'multiplied by 1.8'), 3: (lambda: fmt((D('96.8') + E32) / E18, 3) + ' °C', 'added 32')})
calc('freezer at -80.0 °C', ['-80.0'], {0: (lambda: C2K('-80.0') + ' K', 'C + 273.15'), 1: (lambda: C2K('80.0') + ' K', 'dropped the sign'),
     2: (lambda: rq(D('-80.0') - E273, 1) + ' K', 'subtracted 273.15'), 3: (lambda: rq(-(D('-80.0') + E273), 1) + ' K', 'negative kelvins')})
calc('boils at about 4.22 K', ['4.22'], {0: (lambda: K2C('4.22') + ' °C', 'K - 273.15'), 1: (lambda: C2K('4.22') + ' °C', 'added 273.15'),
     2: (lambda: rq(E273 - D('4.22'), 2) + ' °C', 'subtracted backward'), 3: (lambda: fmt(D('4.22') * E18 + 32, 3) + ' °C', 'F formula on K')})
calc('core temperature of 93.2 °F', ['93.2'], {0: (lambda: F2K('93.2') + ' K', 'F -> C -> K'), 1: (lambda: C2K(rq(D('93.2') - E32 / E18, 1)) + ' K', 'no parentheses'),
     2: (lambda: F2C('93.2') + ' K', 'stopped at C'), 3: (lambda: C2K(rq(D('93.2') - E32, 1)) + ' K', 'never divided by 1.8')})
calc('boils at 90.19 K', ['90.19'], {0: (lambda: K2F('90.19') + ' °F', 'K -> C -> F'), 1: (lambda: rq(D('90.19') * E18 + 32, 2) + ' °F', 'K in the F formula'),
     2: (lambda: K2C('90.19') + ' °F', 'stopped at C'), 3: (lambda: C2F(C2K('90.19')) + ' °F', 'added 273.15')})
calc('rises by 2.4 °C', ['2.4'], {0: (lambda: '2.4 K and %s °F' % fmt(E18 * D('2.4'), 2), 'change: x1.8, no offsets'),
     1: (lambda: '%s K and %s °F' % (C2K('2.4'), C2F('2.4')), 'converted as a temperature'),
     2: (lambda: '2.4 K and 2.4 °F', 'same-size degrees'), 3: (lambda: '2.4 K and %s °F' % fmt(D('2.4') / E18, 2), 'divided by 1.8')})
calc('reads 25 °C', ['25'], {0: (lambda: C2K('25') + ' K', 'decimal places of 25'), 1: (lambda: str(D('25') + E273) + ' K', 'kept 273.15 decimals'),
     2: (lambda: rq(D('25') + E273, 1) + ' K', 'one decimal place'), 3: (lambda: fmt(D('25') + E273, 2) + ' K', 'rounded to 2 s.f.')})
calc('A large apple provides about 116 Cal', ['116'], {0: (lambda: F3(D('116') * D('4.184'), 3, 'kJ'), 'x 4.184'), 1: (lambda: F3(D('116') * 4184, 3, 'kJ'), 'x 4184 labeled kJ'),
     2: (lambda: F3(D('116') / D('4.184'), 3, 'kJ'), 'divided'), 3: (lambda: F3(D('116') * D('4.184') / 1000, 3, 'kJ'), 'Cal treated as cal')})
calc('releases 8.50 x 10^3 J', ['8.50e3'], {0: (lambda: F3(D('8.50e3') / D('4.184'), 3, 'cal'), '/ 4.184'), 1: (lambda: F3(D('8.50e3') * D('4.184'), 3, 'cal'), 'x 4.184'),
     2: (lambda: F3(D('8.50e3') / 4184, 3, 'cal'), '/ 4184 (kcal)'), 3: (lambda: F3(D('8.50e3') / 1000, 3, 'cal'), 'J -> kJ labeled cal')})
calc('uses about 6.70 x 10^2 kJ', ['6.70e2'], {0: (lambda: F3(D('670') / D('4.184'), 3, 'Cal'), '/ 4.184'), 1: (lambda: F3(D('670') * D('4.184'), 3, 'Cal'), 'x 4.184'),
     2: (lambda: F3(D('670') / 4184, 3, 'Cal'), '/ 4184'), 3: (lambda: F3(D('670') * 1000 / D('4.184'), 3, 'Cal'), 'small calories')})
calc('absorbs 3.25 kcal', ['3.25'], {0: (lambda: F3(D('3.25') * 4184, 3, 'J'), 'x 4184'), 1: (lambda: F3(D('3.25') * D('4.184'), 3, 'J'), 'kcal as cal'),
     2: (lambda: F3(D('3250') / D('4.184'), 3, 'J'), 'divided'), 3: (lambda: F3(D('3.25') * 4184 * 1000, 3, 'J'), 'x 1000 twice')})
# ---- ch09-specheat (Try It) ----
def _q(m, c, Tf, Ti, f=1): v, n = qmc(m, c, dT(Tf, Ti)); return v * f, n
calc('holds 955 g of water', ['955', '52.5', '37.0'], {0: (lambda: 'q = ' + Sx(*_q('955', '4.184', '37.0', '52.5'), 'J'), 'mcΔT, ΔT<0'),
     1: (lambda: 'q = ' + Sx(*_q('955', '4.184', '52.5', '37.0'), 'J', True), 'ΔT backward'),
     2: (lambda: 'q = ' + Sx(*_q('955', '4.184', '37.0', '52.5', D('0.001')), 'J'), 'kJ labeled J'),
     3: (lambda: 'q = ' + Sx(D('955') * CW * D('37.0'), 3, 'J', True), 'Tf as ΔT')})
calc('A 250.0 g aluminum pan', ['250.0', '21.0', '175.0'], {0: (lambda: Sx(*_q('250.0', '0.903', '175.0', '21.0'), 'J'), 'mcΔT'),
     1: (lambda: Sx(*_q('250.0', '4.184', '175.0', '21.0'), 'J'), "water's c"), 2: (lambda: Sx(*_q('250.0', '0.903', '21.0', '175.0'), 'J'), 'ΔT backward'),
     3: (lambda: Sx(D('250.0') * D('0.903') * D('175.0'), 3, 'J'), 'Tf as ΔT')})
calc('65.0 g silver bracelet absorbs 412 J', ['65.0', '412'], {0: (lambda: F3(D('412') / (D('65.0') * D('0.235')), 3, '°C'), 'q/(mc)'),
     1: (lambda: F3(D('412') * D('65.0') * D('0.235'), 3, '°C'), 'q m c'), 2: (lambda: F3(D('412') / D('65.0') * D('0.235'), 3, '°C'), 'c on top'),
     3: (lambda: F3(D('412') / (D('65.0') * CW), 3, '°C'), "water's c")})
def _tf(Ti, q_kJ, m, c, sign=1):
    d = fmt(D(q_kJ) * 1000 / (D(m) * D(c)), 3); return addr(Ti, ('-' if sign < 0 else '') + d), d
calc('312 g copper pot at 24.5 °C', ['312', '24.5', '5.60'], {0: (lambda: _tf('24.5', '5.60', '312', '0.385')[0] + ' °C', 'Ti + ΔT'),
     1: (lambda: _tf('24.5', '5.60', '312', '0.385')[1] + ' °C', 'ΔT only'), 2: (lambda: _tf('24.5', '5.60', '312', '0.385', -1)[0] + ' °C', 'subtracted ΔT'),
     3: (lambda: _tf('24.5', '5.60', '312', '4.184')[0] + ' °C', "water's c")})
calc('supplies 7.75 kJ of heat', ['7.75', '18.5', '37.0'], {0: (lambda: F3(D('7750') / (CW * D(dT('37.0', '18.5'))), 3, 'g'), 'q/(cΔT)'),
     1: (lambda: F3(D('7.75') / (CW * D(dT('37.0', '18.5'))), 3, 'g'), 'q in kJ'), 2: (lambda: F3(D('7750') * CW / D(dT('37.0', '18.5')), 3, 'g'), 'q c / ΔT'),
     3: (lambda: F3(D('7750') / (CW * D('37.0')), 3, 'g'), 'Tf as ΔT')})
calc('75.0 g sample of a metal absorbs 863 J', ['75.0', '863', '19.8', '49.7'], {0: (lambda: F3(D('863') / (D('75.0') * D(dT('49.7', '19.8'))), 3, UC), 'q/(mΔT)'),
     1: (lambda: F3(D('863') / (D('75.0') * D('49.7')), 3, UC), 'Tf as ΔT'), 2: (lambda: F3(D('75.0') * D(dT('49.7', '19.8')) / D('863'), 3, UC), 'inverted'),
     3: (lambda: F3(D('863') * D(dT('49.7', '19.8')) / D('75.0'), 3, UC), 'q ΔT / m')})
calc('65.0 g piece of iron at 99.2 °C', ['65.0', '99.2', '45.0', '21.0', '31.5'], {0: (lambda: 'qiron = ' + Sx(*_q('45.0', '4.184', '31.5', '21.0', -1), 'J'), '-q_water'),
     1: (lambda: 'qiron = ' + Sx(*_q('45.0', '4.184', '31.5', '21.0'), 'J', True), "water's q (sign)"),
     2: (lambda: 'qiron = ' + Sx(*_q('65.0', '4.184', '31.5', '21.0', -1), 'J'), 'metal mass with water c'),
     3: (lambda: 'qiron = ' + Sx(-D('45.0') * CW * D('31.5'), 3, 'J'), 'Tf as ΔT')})
def _cm(mm_, Tm, mw, Tw, Tf, mode=0):
    qw = D(mw) * CW * D(dT(Tf, Tw))
    if mode == 0: return -qw / (D(mm_) * D(dT(Tf, Tm)))
    if mode == 1: return qw / (D(mm_) * D(Tf))
    if mode == 2: return qw / (D(mw) * -D(dT(Tf, Tm)))
    return qw / (D(mm_) * D(dT(Tf, Tw)))
CAL1 = ('85.0', '99.5', '45.0', '22.5', '33.9'); CAL2 = ('65.0', '99.5', '75.0', '19.5', '32.1')
calc('An 85.0 g metal block at 99.5 °C', list(CAL1), {0: (lambda: F3(_cm(*CAL1), 3, UC), 'c = -q_w/(mΔT)'), 1: (lambda: F3(_cm(*CAL1, 1), 3, UC), 'Tf as ΔT'),
     2: (lambda: F3(_cm(*CAL1, 2), 3, UC), 'water mass'), 3: (lambda: F3(_cm(*CAL1, 3), 3, UC), "water's ΔT")})
# ---- ch09-phase (Try It) ----
def _nh(g, H, sign=1, unit='kJ', per_g=False):
    v, n = (D(g) * D(H), min(sf(g), sf(H))) if per_g else nH(g, H)
    return 'q = ' + Sx(sign * v, n, unit, True)
calc('melt 42.5 g of ice', ['42.5'], {0: (lambda: _nh('42.5', HF_), 'n ΔHfus'), 1: (lambda: 'q = ' + Sx(D('42.5') * D(HF_), 3, 'kJ', True), 'grams x kJ/mol'),
     2: (lambda: _nh('42.5', HV_), 'ΔHvap'), 3: (lambda: _nh('42.5', HF_, -1), 'sign')})
calc('boil away 36.5 g of water', ['36.5'], {0: (lambda: _nh('36.5', HV_), 'n ΔHvap'), 1: (lambda: 'q = ' + Sx(D('36.5') * D(HV_), 3, 'kJ', True), 'grams x kJ/mol'),
     2: (lambda: _nh('36.5', HF_), 'ΔHfus'), 3: (lambda: _nh('36.5', HV_, -1), 'sign')})
calc('8.75 g of steam at 100 °C', ['8.75'], {0: (lambda: _nh('8.75', HV_, -1), '-n ΔHvap'), 1: (lambda: _nh('8.75', HV_), 'sign'),
     2: (lambda: _nh('8.75', HF_, -1), 'ΔHfus'), 3: (lambda: 'q = ' + Sx(-D('8.75') * D(HV_), 3, 'kJ', True), 'grams x kJ/mol')})
calc('holds 125 g of liquid water', ['125'], {0: (lambda: _nh('125', HF_, -1), '-n ΔHfus'), 1: (lambda: _nh('125', HF_), 'sign'),
     2: (lambda: _nh('125', HV_, -1), 'ΔHvap'), 3: (lambda: 'q = ' + Sx(-D('125') * D(HF_), 3, 'kJ', True), 'grams x kJ/mol')})
calc('does 18.6 g of ice absorb', ['18.6', '334'], {0: (lambda: F3(D('18.6') * 334, 3, 'J'), 'm ΔHfus (J/g)'), 1: (lambda: F3(D('18.6') / MW * 334, 3, 'J'), 'needless g -> mol'),
     2: (lambda: F3(D('18.6') / 334, 3, 'J'), 'divided'), 3: (lambda: F3(D('18.6') * 334 / 1000, 3, 'J'), 'kJ labeled J')})
def kJ(v, n): return fmt(v / 1000, n)
def _two():
    a = kJ(*qmc('30.5', '4.184', dT('100', '64.0'))); b = fmt(*nH('30.5', HV_)); return a, b
calc('take 30.5 g of water at 64.0 °C', ['30.5', '64.0'], {0: (lambda: addr(*_two()) + ' kJ', 'mcΔT + nΔHvap'), 1: (lambda: _two()[1] + ' kJ', 'forgot warming'),
     2: (lambda: addr(_two()[0], fmt(*nH('30.5', HF_))) + ' kJ', 'ΔHfus for boiling'),
     3: (lambda: fmt(back(_two()[0])[0] + back(fmt(D('30.5') * D(HV_), 3))[0], 3) + ' kJ', 'no g -> mol')})
def _three(cice='2.09'):
    a = kJ(*qmc('16.5', cice, dT('0', '-12.5'))); b = fmt(*nH('16.5', HF_)); c = kJ(*qmc('16.5', '4.184', dT('35.0', '0'))); return a, b, c
calc('16.5 g of ice at -12.5 °C', ['16.5', '-12.5', '35.0'], {0: (lambda: addr(*_three()) + ' kJ', 'three steps'), 1: (lambda: addr(*_three()[1:]) + ' kJ', 'forgot warming the ice'),
     2: (lambda: addr(_three()[0], _three()[2]) + ' kJ', 'forgot melting'), 3: (lambda: addr(*_three('4.184')) + ' kJ', "water's c for ice")})
# ---- ADAPT ----
calc('stored frozen at -15.0 °C', ['-15.0'], {0: (lambda: C2F('-15.0') + ' °F', '1.8C + 32'), 1: (lambda: rq(D(fmt(E18 * (D('-15.0') + 32), 3)), 1) + ' °F', 'added 32 first'),
     2: (lambda: fmt(D('-15.0') / E18 + 32, 3) + ' °F', 'divided by 1.8'), 3: (lambda: fmt((D('-15.0') - 32) / E18, 3) + ' °F', 'F->C formula')})
calc('reaches 104.0 °F', ['104.0'], {0: (lambda: F2C('104.0') + ' °C', '(F-32)/1.8'), 1: (lambda: rq(D('104.0') - E32 / E18, 1) + ' °C', 'no parentheses'),
     2: (lambda: fmt((D('104.0') - 32) * E18, 4) + ' °C', 'x 1.8'), 3: (lambda: fmt((D('104.0') + 32) / E18, 4) + ' °C', 'added 32')})
calc('sublimes at 194.7 K', ['194.7'], {0: (lambda: K2C('194.7') + ' °C', 'K - 273.15'), 1: (lambda: C2K('194.7') + ' °C', 'added'),
     2: (lambda: rq(E273 - D('194.7'), 1) + ' °C', 'backward'), 3: (lambda: rq(D(fmt(E18 * D('194.7'), 4)) + 32, 1) + ' °C', 'F formula on K')})
calc('cools by 12.5 °F', ['12.5'], {0: (lambda: F3(D('12.5') / E18, 3, 'K'), '/1.8'), 1: (lambda: F3(D('12.5') * E18, 3, 'K'), 'x1.8'),
     2: (lambda: '12.5 K', 'same size'), 3: (lambda: F3((D('12.5') - 32) / E18, 3, 'K'), 'subtracted 32')})
calc('temperature is 102.2 °F', ['102.2'], {0: (lambda: F2K('102.2') + ' K', 'F -> C -> K'), 1: (lambda: C2K(rq(D('102.2') - E32 / E18, 1)) + ' K', 'no parentheses'),
     2: (lambda: F2C('102.2') + ' K', 'stopped at C'), 3: (lambda: rq(D(F2C('102.2')) - E273, 1) + ' K', 'subtracted 273.15')})
calc('provides 83.0 Cal', ['83.0'], {0: (lambda: F3(D('83.0') * 4184, 3, 'J'), 'x 4184'), 1: (lambda: F3(D('83.0') * D('4.184'), 3, 'J'), 'x 4.184'),
     2: (lambda: F3(D('83.0') / D('4.184'), 3, 'J'), 'divided'), 3: (lambda: F3(D('83.0') * 4184 * 1000, 3, 'J'), 'extra 1000')})
calc('delivers 2.75 kJ of heat', ['2.75'], {0: (lambda: F3(D('2750') / D('4.184'), 3, 'cal'), 'kJ -> J -> cal'), 1: (lambda: F3(D('2.75') * D('4.184'), 3, 'cal'), 'kJ x 4.184'),
     2: (lambda: F3(D('2.75') / D('4.184'), 3, 'cal'), 'kcal'), 3: (lambda: F3(D('2750') * D('4.184'), 3, 'cal'), 'x 4.184')})
calc('warm 375 g of ethanol', ['375', '18.0', '42.5'], {0: (lambda: Sx(*_q('375', '2.42', '42.5', '18.0'), 'J'), 'mcΔT'), 1: (lambda: Sx(*_q('375', '4.184', '42.5', '18.0'), 'J'), "water's c"),
     2: (lambda: Sx(*_q('375', '2.42', '18.0', '42.5'), 'J'), 'ΔT backward'), 3: (lambda: Sx(*_q('375', '2.42', '42.5', '18.0', D('0.001')), 'J'), 'kJ labeled J')})
calc('165 g lead fishing weight', ['165', '88.5', '22.0'], {0: (lambda: 'q = ' + Sx(*_q('165', '0.128', '22.0', '88.5'), 'J'), 'mcΔT'),
     1: (lambda: 'q = ' + Sx(*_q('165', '0.128', '88.5', '22.0'), 'J', True), 'ΔT backward'), 2: (lambda: 'q = ' + Sx(*_q('165', '0.128', '22.0', '88.5', D('0.001')), 'J'), 'kJ labeled J'),
     3: (lambda: 'q = ' + Sx(D('165') * D('0.128') * D('22.0'), 3, 'J', True), 'Tf as ΔT')})
calc('85.0 g iron nail at 22.5 °C', ['85.0', '22.5', '1.25'], {0: (lambda: _tf('22.5', '1.25', '85.0', '0.449')[0] + ' °C', 'Ti + ΔT'),
     1: (lambda: _tf('22.5', '1.25', '85.0', '0.449')[1] + ' °C', 'ΔT only'), 2: (lambda: _tf('22.5', '1.25', '85.0', '0.449', -1)[0] + ' °C', 'subtracted'),
     3: (lambda: _tf('22.5', '1.25', '85.0', '4.184')[0] + ' °C', "water's c")})
calc('mass of copper absorbs 2.45 kJ', ['2.45', '20.5', '65.0'], {0: (lambda: F3(D('2450') / (D('0.385') * D(dT('65.0', '20.5'))), 3, 'g'), 'q/(cΔT)'),
     1: (lambda: F3(D('2.45') / (D('0.385') * D(dT('65.0', '20.5'))), 3, 'g'), 'kJ'), 2: (lambda: F3(D('2450') * D('0.385') / D(dT('65.0', '20.5')), 3, 'g'), 'q c / ΔT'),
     3: (lambda: F3(D('2450') / (D('0.385') * D('65.0')), 3, 'g'), 'Tf as ΔT')})
calc('28.4 g sample absorbs 175 J', ['28.4', '175', '21.3', '47.6'], {0: (lambda: F3(D('175') / (D('28.4') * D(dT('47.6', '21.3'))), 3, UC), 'q/(mΔT)'),
     1: (lambda: F3(D('175') / (D('28.4') * D('47.6')), 3, UC), 'Tf as ΔT'), 2: (lambda: F3(D('28.4') * D(dT('47.6', '21.3')) / D('175'), 3, UC), 'inverted'),
     3: (lambda: F3(D('175') * D(dT('47.6', '21.3')) / D('28.4'), 3, UC), 'q ΔT / m')})
calc('A 65.0 g metal block at 99.5 °C', list(CAL2), {0: (lambda: F3(_cm(*CAL2), 3, UC), 'c = -q_w/(mΔT)'), 1: (lambda: F3(_cm(*CAL2, 1), 3, UC), 'Tf as ΔT'),
     2: (lambda: F3(_cm(*CAL2, 2), 3, UC), 'water mass'), 3: (lambda: F3(_cm(*CAL2, 3), 3, UC), "water's ΔT")})
calc('melt 2.35 mol of ice', ['2.35'], {0: (lambda: F3(D('2.35') * D(HF_), 3, 'kJ'), 'n ΔHfus'), 1: (lambda: F3(D('2.35') * D(HV_), 3, 'kJ'), 'ΔHvap'),
     2: (lambda: F3(D('2.35') / D(HF_), 3, 'kJ'), 'divided'), 3: (lambda: F3(D('2.35') * MW * D(HF_), 3, 'kJ'), 'mol -> g')})
calc('22.8 g of steam at 100 °C', ['22.8'], {0: (lambda: _nh('22.8', HV_, -1), '-n ΔHvap'), 1: (lambda: _nh('22.8', HV_), 'sign'),
     2: (lambda: _nh('22.8', HF_, -1), 'ΔHfus'), 3: (lambda: 'q = ' + Sx(-D('22.8') * D(HV_), 3, 'kJ', True), 'grams x kJ/mol')})
calc('when 45.5 g of liquid water freezes', ['45.5', '334'], {0: (lambda: _nh('45.5', '334', -1, 'J', True), '-m ΔHfus'), 1: (lambda: _nh('45.5', '334', 1, 'J', True), 'sign'),
     2: (lambda: 'q = ' + Sx(-D('45.5') / MW * 334, 3, 'J', True), 'needless g -> mol'), 3: (lambda: 'q = ' + Sx(-D('45.5') * 334 / 1000, 3, 'J', True), 'kJ labeled J')})
def _burn():
    a = fmt(*(lambda v, n: (-v, n))(*nH('5.80', HV_))); b = kJ(*qmc('5.80', '4.184', dT('45.0', '100'))); return a, b
calc('5.80 g of steam at 100 °C', ['5.80', '45.0'], {0: (lambda: 'q = ' + addr(*_burn()) + ' kJ', 'condense + cool'), 1: (lambda: 'q = ' + _burn()[0] + ' kJ', 'forgot cooling'),
     2: (lambda: 'q = ' + _burn()[1] + ' kJ', 'forgot condensing'), 3: (lambda: 'q = ' + plus(addr(*_burn()).lstrip('-')) + ' kJ', 'sign')})

for sub, givens, specs in CALC:
    q = by(sub)
    if not q: continue
    checked.add(q['id']); stem = txt(q['q'])
    for gv in givens:
        if 'e' in gv:
            m_, e_ = gv.split('e'); pat = re.escape(m_) + r' x 10\^' + re.escape(e_)
        else:
            pat = r'(?<![\d.])' + re.escape(gv) + r'(?![\d])'
        if not re.search(pat, stem): err.append(q['id'] + ' given %r not in stem as written' % gv)
    print('  %s %s' % (q['id'], sub[:48]))
    keys = []
    for j, (fn, why) in sorted(specs.items()):
        try: want = fn()
        except Exception as e_: err.append('%s c[%d] spec failed: %r' % (q['id'], j, e_)); continue
        keys.append(want)
        ok(txt(q['c'][j]).strip() == want, '%s c[%d] %-30r = %r (%s)' % (q['id'], j, txt(q['c'][j]).strip(), want, why))
    if len(set(keys)) != 4: err.append(q['id'] + ' recomputed values not all different: %s' % keys)
    k0 = re.sub(r'^q\w* = ', '', keys[0]).split(' ')[0].lstrip('+') if keys else ''
    if k0 and k0 not in txt(q['w']): err.append(q['id'] + ' answer %s not in w' % k0)
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')

# ---------- multi-step sums: rounding each step first must give the same answer as rounding once ----------
print('Multi-step heats: sum of rounded steps = unrounded sum rounded to the same place')
for sub, steps in (('take 30.5 g of water at 64.0 °C', [qmc('30.5', '4.184', dT('100', '64.0'))[0] / 1000, nH('30.5', HV_)[0]]),
                   ('16.5 g of ice at -12.5 °C', [qmc('16.5', '2.09', dT('0', '-12.5'))[0] / 1000, nH('16.5', HF_)[0], qmc('16.5', '4.184', dT('35.0', '0'))[0] / 1000]),
                   ('5.80 g of steam at 100 °C', [-nH('5.80', HV_)[0], qmc('5.80', '4.184', dT('45.0', '100'))[0] / 1000])):
    q = by(sub); key = re.sub(r'^q = ', '', txt(q['c'][0])).split(' ')[0]; p_ = dec(key)
    ok(rq(sum(steps), p_) == key, '%s unrounded sum %s -> %s = key %s' % (q['id'], fmt(sum(steps), 6), rq(sum(steps), p_), key))

# ---------- calorimetry data are physically consistent ----------
print('Calorimetry data: heat lost by the metal = heat gained by the water (within 1.5%)')
for sub, (mm_, Tm, mw, Tw, Tf), c in (('65.0 g piece of iron at 99.2 °C', ('65.0', '99.2', '45.0', '21.0', '31.5'), '0.449'),
                                     ('An 85.0 g metal block at 99.5 °C', CAL1, '0.385'), ('A 65.0 g metal block at 99.5 °C', CAL2, '0.903')):
    q = by(sub); qw = D(mw) * CW * (D(Tf) - D(Tw)); qm = D(mm_) * D(c) * (D(Tf) - D(Tm))
    ok(abs(qw + qm) / qw < D('0.015'), '%s q_water %s J, q_metal %s J (c %s)' % (q['id'], fmt(qw, 4), fmt(qm, 4), c))
    if c != '0.449': ok(fmt(_cm(mm_, Tm, mw, Tw, Tf), 3) == c, '%s recomputed c %s matches %s' % (q['id'], fmt(_cm(mm_, Tm, mw, Tw, Tf), 3), c))

# ---------- conceptual items with numbers ----------
print('Conceptual items with numbers, tables or the heating-curve plot')
q = by('Which is the highest temperature?'); checked.add(q['id'])
def toC(s):
    v, u = txt(s).split(' ')
    return D(F2C(v)) if u == '°F' else (D(K2C(v)) if u == 'K' else D(v))
cs = [toC(c) for c in q['c']]; ok(cs[0] == max(cs) and cs.count(max(cs)) == 1, '%s in °C %s; highest is c[0]' % (q['id'], [str(x) for x in cs]))
for j, c in enumerate(q['c']):
    v, u = txt(c).split(' ')
    if u != '°C' and str(cs[j]) not in txt(q['w']): err.append('%s w lacks the converted %s' % (q['id'], c))
q = by('Which of these is the largest amount of energy?'); checked.add(q['id'])
J = {'Cal': 4184, 'kcal': 4184, 'kJ': 1000, 'cal': D('4.184'), 'J': 1}
js = [D(txt(c).split()[0].rstrip('.')) * J[txt(c).split()[1]] for c in q['c']]
ok(js[0] == max(js) and js.count(js[0]) == 1, '%s in J %s' % (q['id'], [str(x) for x in js]))
q = by('A 10.0 g ice cube at 0 °C absorbs 1.50 kJ'); checked.add(q['id'])
need = fmt(*nH('10.0', HF_))
ok(D(need) > D('1.50') and need in txt(q['y'][0]) and fmt(D('1500') / (D('10.0') * CW), 3) in txt(q['c'][1]) and fmt(D('1500') / (D('10.0') * CICE), 3) in txt(q['c'][2]),
   '%s melting all needs %s kJ > 1.50 kJ; distractors %s °C (liquid c), %s °C (ice c)' % (q['id'], need, fmt(D('1500') / (D('10.0') * CW), 3), fmt(D('1500') / (D('10.0') * CICE), 3)))
q = by('identify the metal'); checked.add(q['id'])
tab = {r[0]: r[1] for r in q['f'][0]['rows']}
ok(all(C_[k.lower()] == v for k, v in tab.items()), '%s table specific heats = chapter values' % q['id'])
cval = fmt(D('312') / (D('52.4') * D(dT('47.9', '22.6'))), 3); match = [k for k, v in tab.items() if v == cval]
ok(match == [q['c'][0]] and set(q['c']) == set(tab), '%s c = %s -> %s' % (q['id'], cval, match))
q = by('In which segment is the heat calculated'); checked.add(q['id'])
P = q['f'][0]['series'][0]['pts']; segs = [(P[i], P[i + 1]) for i in range(len(P) - 1)]
labs = {m_[2]: (m_[0], m_[1]) for m_ in q['f'][0]['marks']}
order = sorted(labs, key=lambda k: labs[k][0])
if order != ['A', 'B', 'C', 'D', 'E'] or len(segs) != 5: err.append('%s plot labels not in segment order' % q['id'])
for k, s in zip(order, segs):
    if not (s[0][0] - 0.5 <= labs[k][0] <= s[1][0] + 1.0): err.append('%s label %s is not beside its segment' % (q['id'], k))
def seg_of(lab): return segs[order.index(lab)]
segD, segB = seg_of('D'), seg_of('B')
flat = [s for s in segs if s[0][1] == s[1][1]]
ok(segD[0][1] == segD[1][1] == 100 and segB[0][1] == segB[1][1] == 0 and max(flat, key=lambda s: s[1][0] - s[0][0]) == segD
   and q['c'][0] == 'Segment D' and len(segs) == 5 and P[0][1] == -20 and P[-1][1] == 120,
   '%s plot: D = longest plateau at 100 °C, B = plateau at 0 °C; curve -20 -> 120 °C' % q['id'])
for lab, want in (('A', 'slope'), ('C', 'slope'), ('E', 'slope')):
    s = seg_of(lab); ok(s[0][1] != s[1][1], '%s segment %s is a %s' % (q['id'], lab, want))
q = by('Use the normal boiling points in the table'); checked.add(q['id'])
rows = [(txt(r[0]).split(',')[0], D(r[1])) for r in q['f'][0]['rows']]
BP = {'Dichloromethane': 40, 'Acetone': 56, 'Methanol': 65, 'Water': 100}   # standard values, rounded (39.6, 56, 64.7, 100)
ok(all(BP[n] == v for n, v in rows) and min(rows, key=lambda r: r[1])[0] == q['c'][0] and max(rows, key=lambda r: r[1])[0] == q['c'][3],
   '%s lowest bp (highest vapor pressure) %s; highest bp %s is a distractor' % (q['id'], q['c'][0], q['c'][3]))

# ---------- intermolecular forces ----------
Z = {'H': 1, 'He': 2, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19,
     'Ca': 20, 'Br': 35, 'Kr': 36, 'I': 53, 'Xe': 54, 'Al': 13, 'Mg': 12, 'Na': 11}
# formula -> (bonds as atom pairs (one entry per kind is enough), symmetric with identical outer atoms and no lone
# pair on the centre (SNAP)). Polar = a polar bond (dEN > 0.4) and not symmetric.
MOL = {
 'CHCl3': ([('C', 'H'), ('C', 'Cl')], False), 'CH3NH2': ([('C', 'H'), ('C', 'N'), ('N', 'H')], False),
 'CH3CH2OH': ([('C', 'H'), ('C', 'C'), ('C', 'O'), ('O', 'H')], False), 'CH3OCH3': ([('C', 'H'), ('C', 'O')], False),
 'CH2O': ([('C', 'H'), ('C', 'O')], False), 'CHF3': ([('C', 'H'), ('C', 'F')], False), 'CCl4': ([('C', 'Cl')], True),
 'CH4': ([('C', 'H')], True), 'C2H6': ([('C', 'H'), ('C', 'C')], True), 'C3H8': ([('C', 'H'), ('C', 'C')], True),
 'C4H10': ([('C', 'H'), ('C', 'C')], True), 'C5H12': ([('C', 'H'), ('C', 'C')], True), 'C6H14': ([('C', 'H'), ('C', 'C')], True),
 'CH3CH2CH2CH3': ([('C', 'H'), ('C', 'C')], True), 'CH3F': ([('C', 'H'), ('C', 'F')], False), 'H2O': ([('O', 'H')], False),
 'CH3COCH3': ([('C', 'H'), ('C', 'C'), ('C', 'O')], False), 'CH2Cl2': ([('C', 'H'), ('C', 'Cl')], False),
 'H2O2': ([('O', 'H'), ('O', 'O')], False), 'CH3COOH': ([('C', 'H'), ('C', 'C'), ('C', 'O'), ('O', 'H')], False),
 'HOCH2CH2OH': ([('O', 'H'), ('C', 'O'), ('C', 'H'), ('C', 'C')], False), 'C3H5(OH)3': ([('O', 'H'), ('C', 'O'), ('C', 'H'), ('C', 'C')], False),
 'CH3CH2CH2OH': ([('O', 'H'), ('C', 'O'), ('C', 'H'), ('C', 'C')], False), 'CH3OH': ([('O', 'H'), ('C', 'O'), ('C', 'H')], False),
 'N2': ([('N', 'N')], True), 'F2': ([('F', 'F')], True), 'HF': ([('H', 'F')], False), 'HCl': ([('H', 'Cl')], False), 'HBr': ([('H', 'Br')], False),
 'He': ([], True), 'Ne': ([], True), 'Ar': ([], True), 'Kr': ([], True), 'Xe': ([], True)}
TIER = {'dispersion': 1, 'dipole–dipole': 2, 'hydrogen bonding': 3}
def info(m):
    bonds, sym = MOL[m]
    pb = any(abs(EN[a] - EN[b]) > D('0.4') for a, b in bonds)
    polar = pb and not sym
    hb = any({a, b} & {'H'} and ({a, b} - {'H'}) & {'N', 'O', 'F'} for a, b in bonds)
    if hb and not polar: err.append('IMF table: %s hydrogen bonds but is marked nonpolar' % m)
    strongest = 'hydrogen bonding' if hb else ('dipole–dipole' if polar else 'dispersion')
    el = sum(Z[e] * n for e, n in atoms(m).items())
    return {'polar': polar, 'hb': hb, 'strongest': strongest, 'e': el,
            'forces': {'dispersion'} | ({'dipole–dipole'} if polar else set()) | ({'hydrogen bonding'} if hb else set()),
            'OH': len(re.findall(r'OH|^HO', m))}
for m in MOL: info(m)
assert info('CH4')['strongest'] == 'dispersion' and info('NH3' if 'NH3' in MOL else 'H2O')['hb']
print('IMF table (%d molecules): C-H nonpolar (dEN %s), C-Cl polar (dEN %s), H-bonding only with H on N/O/F' % (len(MOL), abs(EN['C'] - EN['H']), abs(EN['C'] - EN['Cl'])))
def forces_named(t):
    t = t.lower(); s = set()
    if 'dispersion' in t: s.add('dispersion')
    if 'dipole–dipole' in t and 'ion–dipole' not in t.replace('dipole–dipole', ''): s.add('dipole–dipole')
    if 'hydrogen bond' in t: s.add('hydrogen bonding')
    if 'ion–dipole' in t: s.add('ion–dipole')
    return s
def mol_in(c):
    cand = [m for m in re.findall(r'[A-Z][A-Za-z0-9()]*', txt(c)) if m in MOL]
    if not cand: raise KeyError(c)
    return cand[0]
for sub, m in (('Chloroform, CHCl3', 'CHCl3'), ('Acetone, CH3COCH3, the solvent', 'CH3COCH3')):
    q = by(sub); checked.add(q['id']); I = info(m)
    named = [forces_named(txt(c)) for c in q['c']]
    ok(named[0] == I['forces'] and all(n_ != I['forces'] for n_ in named[1:]), '%s %s forces %s; only c[0] lists exactly these' % (q['id'], m, sorted(I['forces'])))
for sub, m in (('methylamine, CH3NH2?', 'CH3NH2'), ('Carbon tetrachloride, CCl4', 'CCl4'), ('hydrogen peroxide, H2O2 (H–O–O–H)', 'H2O2')):
    q = by(sub); checked.add(q['id']); I = info(m)
    ok(forces_named(txt(q['c'][0])) == {I['strongest']}, '%s %s strongest: %s' % (q['id'], m, I['strongest']))
q = by('Which of these can hydrogen bond with itself?'); checked.add(q['id'])
hb = [info(mol_in(c))['hb'] for c in q['c']]; ok(hb == [True, False, False, False], '%s H-bond with itself %s' % (q['id'], [(mol_in(c), h) for c, h in zip(q['c'], hb)]))
q = by('cannot hydrogen bond with itself'); checked.add(q['id'])
hb = [info(mol_in(c))['hb'] for c in q['c']]; ok(hb == [False, True, True, True], '%s H-bond with itself %s' % (q['id'], [(mol_in(c), h) for c, h in zip(q['c'], hb)]))
for sub in ('Which has the strongest dispersion forces?', 'noble gases has the strongest dispersion'):
    q = by(sub); checked.add(q['id']); ms = [mol_in(c) for c in q['c']]; I = [info(m) for m in ms]
    ok(all(i['strongest'] == 'dispersion' for i in I) and I[0]['e'] == max(i['e'] for i in I) and [i['e'] for i in I].count(I[0]['e']) == 1,
       '%s electrons %s; most is c[0]' % (q['id'], [(m, i['e']) for m, i in zip(ms, I)]))
    for n_ in re.findall(r'(\d+) electrons', txt(' '.join(q['y']))):
        if int(n_) not in [i['e'] for i in I]: err.append('%s quotes %s electrons' % (q['id'], n_))
q = by('Xenon (Xe) boils'); checked.add(q['id']); ok(info('Xe')['e'] == 54 and info('Ne')['e'] == 10 and '54' in txt(q['y'][0]) and '10' in txt(q['y'][0]), '%s Xe 54 e, Ne 10 e' % q['id'])
q = by('Which pair of atoms describes a hydrogen bond?'); checked.add(q['id'])
ok(info('H2O')['hb'] and not info('CH4')['polar'] and not info('CH3F')['hb'] and info('CH3F')['polar'], '%s water H-bonds; CH4 nonpolar; CH3F polar, no H bond' % q['id'])
q = by('has the highest surface tension'); checked.add(q['id'])
I = [info(mol_in(c)) for c in q['c']]; ok(I[0]['hb'] and not any(i['hb'] for i in I[1:]), '%s only c[0] hydrogen bonds: %s' % (q['id'], [(mol_in(c), i['strongest']) for c, i in zip(q['c'], I)]))
q = by('Ethylene glycol, HOCH2CH2OH, is much more viscous'); checked.add(q['id'])
ok(info('HOCH2CH2OH')['OH'] == 2 and info('CH3CH2OH')['OH'] == 1 and info('HOCH2CH2OH')['hb'] and info('CH3CH2OH')['hb'], '%s two O–H vs one O–H, both H-bond' % q['id'])
q = by('which of these liquids has the highest vapor pressure'); checked.add(q['id'])
I = [info(mol_in(c)) for c in q['c']]; ok(not I[0]['hb'] and all(i['hb'] for i in I[1:]) and I[0]['e'] == max(i['e'] for i in I), '%s c[0] weakest (only one without H bonding, though the largest): %s' % (q['id'], [(mol_in(c), i['strongest']) for c, i in zip(q['c'], I)]))
q = by('has the lowest vapor pressure at 25 °C'); checked.add(q['id'])
I = [info(mol_in(c)) for c in q['c']]; key = [(TIER[i['strongest']], i['OH'], i['e']) for i in I]
ok(key[0] == max(key) and key.count(key[0]) == 1 and I[1]['e'] == max(i['e'] for i in I[1:]) and not I[1]['hb'],
   '%s strongest attractions c[0] %s; c[1] is the largest molar mass with dispersion only' % (q['id'], key))
def rank_mol(ms): return sorted(ms, key=lambda m: (TIER[info(m)['strongest']], info(m)['e']))
q = by('nearly the same molar mass. Rank them'); checked.add(q['id'])
nm = {'butane': 'CH3CH2CH2CH3', 'acetone': 'CH3COCH3', '1-propanol': 'CH3CH2CH2OH'}
want = ' < '.join(k for k in sorted(nm, key=lambda k: (TIER[info(nm[k])['strongest']], info(nm[k])['e'])))
bymass = ' < '.join(sorted(nm, key=lambda k: MM(nm[k])))
rows = {r[0]: r[2] for r in q['f'][0]['rows']}
ok(txt(q['c'][0]) == want and txt(q['c'][1]) == bymass and txt(q['c'][2]) == ' < '.join(reversed(want.split(' < '))) and all(rows[k] == str(MM(v)) for k, v in nm.items()),
   '%s rank %s; c[1] molar-mass order %s; table molar masses %s' % (q['id'], want, bymass, rows))
q = by('Rank HF, HCl, and HBr'); checked.add(q['id'])
want = ' < '.join(rank_mol(['HF', 'HCl', 'HBr'])); bymass = ' < '.join(sorted(['HF', 'HCl', 'HBr'], key=MM))
ok(txt(q['c'][0]) == want and txt(q['c'][1]) == bymass, '%s rank %s; c[1] molar-mass order %s' % (q['id'], want, bymass))
# ---------- types of solids ----------
METALS = {'Na', 'K', 'Mg', 'Ca', 'Al', 'Fe', 'Cu', 'Ag', 'Au', 'Pb', 'Zn'}
NETWORK = {'C', 'SiO2', 'SiC'}
def solid(f):
    els = set(atoms(f))
    if els <= METALS: return 'metallic'
    if els & METALS: return 'ionic'
    if f in NETWORK: return 'covalent network'
    return 'molecular'
SOL = {'SiC': 'covalent network', 'SiO2': 'covalent network', 'CO2': 'molecular', 'NaCl': 'ionic', 'KCl': 'ionic',
       'Ca5(PO4)3OH': 'ionic', 'C9H8O4': 'molecular', 'C': 'covalent network', 'CaF2': 'ionic', 'Al': 'metallic', 'N2': 'molecular', 'CH3OH': 'molecular', 'NaF': 'ionic', 'F2': 'molecular', 'HF': 'molecular'}
for f, v in SOL.items():
    if solid(f) != v: err.append('solid classifier %s -> %s, expected %s' % (f, solid(f), v))
q = by('Silicon carbide, SiC'); checked.add(q['id']); ok(q['c'][0].lower() == solid('SiC'), '%s SiC: %s' % (q['id'], solid('SiC')))
q = by('Tooth enamel is mostly hydroxyapatite'); checked.add(q['id']); ok(q['c'][0].lower() == solid('Ca5(PO4)3OH'), '%s hydroxyapatite: %s' % (q['id'], solid('Ca5(PO4)3OH')))
q = by('is a molecular solid?'); checked.add(q['id'])
fs = [re.search(r', (\S+)$', txt(c)).group(1) for c in q['c']]
ok([solid(f) for f in fs] == ['molecular', 'covalent network', 'ionic', 'metallic'], '%s %s' % (q['id'], [(f, solid(f)) for f in fs]))
q = by('Diamond and graphite are both pure carbon'); checked.add(q['id']); ok(q['c'][0].lower().startswith(solid('C')), '%s carbon (diamond, graphite): %s' % (q['id'], solid('C')))
q = by('Rank from lowest to highest melting point: F2'); checked.add(q['id'])
STIER = {'molecular': 0, 'metallic': 1, 'ionic': 2, 'covalent network': 3}
fl = ['F2', 'HF', 'NaF', 'SiO2']
want = ' < '.join(sorted(fl, key=lambda f: (STIER[solid(f)], TIER[info(f)['strongest']] if solid(f) == 'molecular' else 0, MM(f))))
bymass = ' < '.join(sorted(fl, key=MM))
ok(txt(q['c'][0]) == want and txt(q['c'][1]) == bymass, '%s rank %s; c[1] molar-mass order %s' % (q['id'], want, bymass))
mms = [round(float(MM(f))) for f in sorted(fl, key=MM)]
alt2 = ' < '.join(sorted(fl, key=lambda f: (0 if f != 'NaF' else 2, TIER[info(f)['strongest']] if f in MOL else 1, MM(f))))
ok(txt(q['c'][2]) == alt2, '%s c[2] = SiO2 treated as a dispersion-only molecule: %s' % (q['id'], alt2))
ok('(%s)' % ' < '.join(str(x) for x in mms) in txt(q['y'][1]), '%s quoted molar masses %s' % (q['id'], mms))

# ---------- course rule: trailing zeros in calculation stems ----------
print('Trailing-zero rule in calculation stems; every k=1 item recomputed')
for q in ALL:
    if q['k'] == 1:
        s = re.sub(r'<sub>\d+</sub>', '', q['q']); s = txt(s).replace('100 °C', '')
        for m in re.finditer(r'(?<![\d.^])(\d*[1-9]\d*0)(?![\d.^])', s):
            err.append(q['id'] + ' calculation stem has ambiguous trailing-zero value %r' % m.group(1))
        if q['id'] not in checked: err.append(q['id'] + ' calculation item not recomputed')
for q in ALL:
    if q['id'] not in checked: hand.add(q['id'])

# ---------- draft overlap ----------
print('Draft overlap: no stem reuses a worked example or exercise from drafts/ch09')
GIV = r'(-?\d+\.\d+|\d+\.|\d+)(?: x 10\^(-?\d+))? ?(g|mol|°C|°F|K|J|kJ|Cal|cal|kcal)\b'
CONST = {'4.184', '0.903', '0.449', '0.385', '0.235', '0.128', '2.09', '2.01', '2.42', '6.02', '40.7', '334', '18.015',
         '273.15', '0', '100', '32', '1.8', '4184', '1', '1000'}
def givens_in(t): return {(a + ('e' + b if b else ''), u) for a, b, u in re.findall(GIV, t) if a not in CONST}
BANNED = {('103.5', '°F'), ('77.4', 'K'), ('245', 'Cal'), ('3.65', 'kJ'), ('155', 'Cal'), ('525', 'J'), ('296', 'J'), ('125', 'J'),
          ('5.00', 'g'), ('25.0', 'g'), ('15.0', 'g'), ('20.0', 'g'), ('50.0', 'g'), ('245', 'g'), ('80.0', 'g'), ('32.6', 'g')}
blocks = []
for p_ in sorted(glob.glob(os.path.join(ROOT, 'drafts', 'ch09', '*.html'))):
    h = open(p_, encoding='utf-8').read()
    for b in re.split(r'(?=Example \\\(\\PageIndex|Exercise \\\(\\PageIndex|<h2|Problem 9\.\d+\b)', h):
        t = re.sub(r'\\\(|\\\)|\\dfrac|\\text|\\times|\\ |\\qquad|\\left|\\right|\\cdot', ' ', b)
        t = re.sub(r'\{\}\^\\circ\s*', '°', t).replace('\\circ', '°')
        t = txt(re.sub(r'[{}]', ' ', t)); t = re.sub(r'\s+', ' ', t)
        m = re.search(r'Problem (9\.\d+)', t)
        blocks.append((os.path.basename(p_) + (' Problem ' + m.group(1) if m else ''), givens_in(t), t.split(' Answer')[0]))
W = lambda s_: set(w for w in re.findall(r'[a-z0-9.]+', s_.lower()) if len(w) > 2)
nover = 0; notes = []
for q in ALL:
    qt = txt(q['q']); qg = givens_in(qt); qw = W(qt)
    for g_ in qg & BANNED:
        if q['k'] == 1:
            nover += 1; err.append('%s uses the draft worked-example given %s %s' % (q['id'], *g_))
    for nm, gs, bt in blocks:
        if len(qg & gs) >= 2:
            nover += 1; err.append('%s shares givens %s with %s' % (q['id'], sorted(qg & gs), nm))
        if 'Problem' in nm:
            bw = W(bt); j = len(qw & bw) / max(1, len(qw | bw))
            if j > 0.45: nover += 1; err.append('%s stem is %.2f similar to %s' % (q['id'], j, nm))
            elif j > 0.3: notes.append('%s stem %.2f similar to %s (different molecules/values; checked by hand)' % (q['id'], j, nm))
print('    %d draft blocks compared (9.0-9.8 sections split at examples/exercises, 9.10 split per problem); %d overlaps' % (len(blocks), nover))
for n_ in notes: print('    NOTE', n_)

# ---------- coverage, counts, duplicates ----------
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
