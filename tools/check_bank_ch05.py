#!/usr/bin/env python3
"""Checker for the Chapter 5 banks (the mole, molar mass, conversions, moles within a formula).
Structural checks as in tools/check_bank_ch03.py (ch05 topic ids), plus, written independently of the generators:
  - its own formula parser (parentheses, hydrate dots) and molar masses from tools/yellow_sheet_masses.json with
    Decimal and the addition rule (round once to the fewest decimal places of the masses used; subscripts exact);
  - every molar-mass answer and every molar-mass distractor (wrong formula, unrounded sum, atomic-number sum, wrong unit);
  - every numeric answer and every numeric distractor's intended error, with sig figs set by the givens as written in
    the stem (multiplication/division rule; Avogadro 6.0221e23 has 5; exact counts unlimited);
  - every "Symbol mass" pair and every "x g/mol" on the answer side against the yellow sheet;
  - counting/ranking items (atoms per formula, ions per formula unit, greatest number/mass) by parsing the formulas;
  - the course sig-fig rule on calculation stems (no whole number ending in 0 without a decimal point);
  - exactly one correct choice (the recomputed key differs from every distractor).
usage: python3 tools/check_bank_ch05.py bank/ch05.json bank/ch05_adapt.json"""
import json, sys, re, os, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 50; getcontext().rounding = ROUND_HALF_UP
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
YS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yellow_sheet_masses.json')))
AM = YS['masses']; NA = D(YS['avogadro'])
assert str(NA) in ('6.0221E+23', '6.0221e23') or NA == D('6.0221e23')
TOP = {'ch05-mole', 'ch05-molarmass', 'ch05-convert', 'ch05-formula'}
err = []

# ---------- structural checks (as in ch03 checker) ----------
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
        if '{' in s or '}' in s: err.append(i + ' unconverted {formula}')
        if 'f' in q and not allow_f: err.append(i + ' has f (ADAPT items must be text only)')
        for f in q.get('f', []):
            if f['type'] != 'table': err.append(i + ' figure type not used/checked here: ' + f['type'])
        if re.search(r'empirical formula|percent composition|limiting reactant|molarity', s, re.I): err.append(i + ' out of scope term')
        if label == 'HW' and not q['y'][0].startswith('Correct: '): err.append(i + ' ADAPT y[0] lacks "Correct: "')
        plain = lambda x: re.sub(r'<[^>]+>', '', x).strip().lower()
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if right in plain(q['y'][j]): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c5-%03d', 'TRY', True)
structural(HW, 'c5-h%02d', 'HW', False)
ALL = TRY + HW

def by(sub):
    m = [q for q in ALL if sub in q['q'] or sub in txt(q['q'])]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
def txt(x):
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = x.replace('&middot;', '.')
    x = re.sub(r'<[^>]+>', '', x)
    return (x.replace('&minus;', '-').replace('−', '-').replace('&times;', 'x').replace('&nbsp;', ' ')
             .replace('&divide;', '/').replace('&rarr;', '->').replace('&ldquo;', '"').replace('&rdquo;', '"'))
def ok(cond, msg):
    print('   ', 'OK ' if cond else 'BAD', msg)
    if not cond: err.append(msg)
checked = set()

# ---------- chemistry from first principles ----------
ZN = {s: i + 1 for i, s in enumerate(('H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn '
                                       'Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I').split())}
def atoms(f):
    """recursive-descent count: formula := group ('.' [k] group)*; parentheses nest."""
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
def ZS(f): return sum(ZN[e] * n for e, n in atoms(f).items())
def sf(s):
    s = s.strip().rstrip('.') + ('.' if s.strip().endswith('.') else '')
    if re.search(r'e', s, re.I): s = s.lower().split('e')[0]
    digits = s.replace('.', '').lstrip('0')
    if '.' in s: return len(digits)
    return len(digits.rstrip('0'))          # course rule: trailing zeros without a decimal point are not significant
def fmt(v, n):
    """course display: n sig figs; plain from 1e-3 up to the ones digit of the last sig fig (trailing '.' when that digit is 0)."""
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

# molar-mass sanity against the chapter text
for f, want in (('H2O', '18.015'), ('NaCl', '58.44'), ('MgSO4', '120.37'), ('C6H12O6', '180.156'), ('Ca(NO3)2', '164.09'),
                ('CuSO4.5H2O', '249.68'), ('C19H26I3N3O9', '821.13'), ('Al2(SO4)3', '342.13'), ('MgSO4.7H2O', '246.47'),
                ('FeSO4.7H2O', '278.01'), ('CO(NH2)2', '60.056'), ('NH4NO3', '80.043'), ('NaF', '41.99'), ('C8H9NO2', '151.165')):
    if str(MM(f)) != want: err.append('checker molar mass %s = %s, text says %s' % (f, MM(f), want))
print('Checker molar masses agree with the chapter text (H2O 18.015, NaCl 58.44, MgSO4 120.37, glucose 180.156, iohexol 821.13, ...)')

def stemformula(q):
    return txt(q['q'])
def has_formula(q, f):
    return f in stemformula(q)

# ---------- molar-mass items ----------
print('Molar masses (addition rule) and their distractors')
# (stem substring, formula shown in stem, unit, {choice: (kind, formula[, unit])}); kinds: r = rounded by rule, raw = unrounded sum,
# Z = atomic-number sum, r2 = rounded to 2 decimal places (rounding habit), u = right number with another unit
MMQ = [
 ('molar mass of chlorine gas', 'Cl2', 'g/mol', {0: ('r', 'Cl2'), 1: ('r', 'Cl'), 2: ('Z', 'Cl'), 3: ('Z', 'Cl2')}),
 ('Ammonia, NH3, is used to make', 'NH3', 'g/mol', {0: ('r', 'NH3'), 1: ('r', 'NH'), 2: ('r', '(NH)3'), 3: ('Z', 'NH3')}),
 ('CaCl2, is used in IV solutions', 'CaCl2', 'amu', {0: ('r', 'CaCl2'), 1: ('r', 'CaCl'), 2: ('Z', 'CaCl2'), 3: ('u', 'CaCl2', 'g')}),
 ('Milk of magnesia', 'Mg(OH)2', 'g/mol', {0: ('r', 'Mg(OH)2'), 1: ('r', 'MgOH2'), 2: ('r', 'MgOH'), 3: ('raw', 'Mg(OH)2')}),
 ('common nitrogen fertilizer on Valley orchards', '(NH4)2SO4', 'g/mol', {0: ('r', '(NH4)2SO4'), 1: ('r', 'NH4SO4'), 2: ('r', 'N2H4SO4'), 3: ('raw', '(NH4)2SO4')}),
 ('Bone mineral is largely calcium phosphate', 'Ca3(PO4)2', 'g/mol', {0: ('r', 'Ca3(PO4)2'), 1: ('r', 'Ca3PO4'), 2: ('r', 'Ca3P2O4'), 3: ('Z', 'Ca3(PO4)2')}),
 ('Gypsum, calcium sulfate dihydrate', 'CaSO4.2H2O', 'g/mol', {0: ('r', 'CaSO4.2H2O'), 1: ('r', 'CaSO4'), 2: ('r', '(CaSO4H2O)2'), 3: ('r', 'CaSO4.H2O')}),
 ('sodium acetate trihydrate', 'NaC2H3O2.3H2O', 'g/mol', {0: ('r', 'NaC2H3O2.3H2O'), 1: ('r', 'NaC2H3O2'), 2: ('r', '(NaC2H3O2H2O)3'), 3: ('r', 'NaC2H3O2.H2O')}),
 ('Aspirin is C9H8O4', 'C9H8O4', 'g/mol', {0: ('r', 'C9H8O4'), 1: ('Z', 'C9H8O4'), 2: ('r', 'C9H8(O2)4'), 3: ('r2', 'C9H8O4')}),
 ('KCl, is used in salt substitutes', 'KCl', 'g/mol', {0: ('r', 'KCl'), 1: ('Z', 'KCl'), 2: ('r', 'KCl2'), 3: ('r', 'K')}),
 ('Ibuprofen is', 'C13H18O2', 'g/mol', {0: ('r', 'C13H18O2'), 1: ('r', 'C13H18O'), 2: ('Z', 'C13H18O2'), 3: ('r2', 'C13H18O2')}),
 ('Iron(III) sulfate is', 'Fe2(SO4)3', 'g/mol', {0: ('r', 'Fe2(SO4)3'), 1: ('r', 'Fe2S3O4'), 2: ('r', 'Fe2SO4'), 3: ('raw', 'Fe2(SO4)3')}),
 ('molar mass of calcium dihydrogen phosphate', 'Ca(H2PO4)2', 'g/mol', {0: ('r', 'Ca(H2PO4)2'), 1: ('r', 'CaH2PO4'), 2: ('r', 'CaH4P2(O2)8'), 3: ('raw', 'Ca(H2PO4)2')}),
 ('Ozone, O3', 'O3', 'g/mol', {0: ('r', 'O3'), 1: ('r', 'O'), 2: ('Z', 'O3'), 3: ('r', 'O2')}),
 ('methane, CH4', 'CH4', 'g/mol', {0: ('r', 'CH4'), 1: ('r', 'CH'), 2: ('Z', 'CH4'), 3: ('r', '(CH)4')}),
 ('Calcium hydroxide, Ca(OH)2', 'Ca(OH)2', 'g/mol', {0: ('r', 'Ca(OH)2'), 1: ('r', 'CaOH'), 2: ('r', 'CaOH2'), 3: ('raw', 'Ca(OH)2')}),
 ('supplies both nitrogen and phosphorus', '(NH4)3PO4', 'g/mol', {0: ('r', '(NH4)3PO4'), 1: ('r', 'NH4PO4'), 2: ('r', 'N3H4PO4'), 3: ('raw', '(NH4)3PO4')}),
 ('Washing soda', 'Na2CO3.10H2O', 'g/mol', {0: ('r', 'Na2CO3.10H2O'), 1: ('r', 'Na2CO3'), 2: ('r', 'Na2CO3.H2O'), 3: ('r', '(Na2CO3H2O)10')}),
 ('Aluminum hydroxide, Al(OH)3', 'Al(OH)3', 'g/mol', {0: ('r', 'Al(OH)3'), 1: ('r', 'AlOH3'), 2: ('r', 'AlO3H'), 3: ('raw', 'Al(OH)3')}),
 ('octadecahydrate', 'Al2(SO4)3.18H2O', 'g/mol', {0: ('r', 'Al2(SO4)3.18H2O'), 1: ('r', 'Al2(SO4)3'), 2: ('r', 'Al2(SO4)3.H2O'), 3: ('r', 'Al2SO4.18H2O')}),
 ('formula mass</b> of sucrose', 'C12H22O11', 'amu', {0: ('r', 'C12H22O11'), 1: ('Z', 'C12H22O11'), 2: ('r2', 'C12H22O11'), 3: ('u', 'C12H22O11', 'g')}),
 ('potassium alum', 'KAl(SO4)2.12H2O', 'g/mol', {0: ('r', 'KAl(SO4)2.12H2O'), 1: ('r', 'KAlSO4.12H2O'), 2: ('r', 'KAl(SO4)2'), 3: ('r', 'KAl(SO4)2.H2O')}),
]
def mmval(kind, f):
    if kind in ('r', 'u'): return str(MM(f))
    if kind == 'raw': return format(MMraw(f).normalize(), 'f')
    if kind == 'Z': return str(ZS(f))
    if kind == 'r2': return str(MMraw(f).quantize(D('0.01')))
for sub, f, unit, ch in MMQ:
    q = by(sub)
    if not q: continue
    checked.add(q['id'])
    ok(has_formula(q, f), '%s stem shows %s' % (q['id'], f))
    # masses quoted in the stem must be exactly the ones the formula needs
    quoted = dict(re.findall(r'\b([A-Z][a-z]?) (\d+\.\d+)', txt(q['q'])))
    if quoted and set(quoted) != set(atoms(f)): err.append('%s stem quotes masses for %s, formula needs %s' % (q['id'], sorted(quoted), sorted(atoms(f))))
    vals = []
    for j, spec in sorted(ch.items()):
        kind, g = spec[0], spec[1]; u = spec[2] if len(spec) > 2 else unit
        want = mmval(kind, g) + ' ' + u; vals.append(want)
        ok(txt(q['c'][j]).strip() == want, '%s c[%d] %-16r = %r (%s %s)' % (q['id'], j, txt(q['c'][j]), want, kind, g))
    ok(len(set(vals)) == 4, '%s four different values' % q['id'])
    if str(MM(f)) not in txt(q['w']): err.append(q['id'] + ' molar mass not in w')
    if q['k'] != 1: err.append(q['id'] + ' molar-mass calculation item without k=1')
q = by('as 2(22.99) + 12.011 + 3(15.999)'); checked.add(q['id'])
raw = MMraw('Na2CO3')
ok(txt(q['q']).count(format(raw, 'f')) == 1 and q['c'][0] == str(MM('Na2CO3')) + ' g/mol' and q['c'][1].startswith(format(raw, 'f')),
   '%s raw sum %s, reported %s (2 decimal places from Na)' % (q['id'], raw, MM('Na2CO3')))
ok(txt(q['c'][2]).startswith(fmt(raw, 4)) and txt(q['c'][3]).startswith(fmt(raw, 3)), '%s distractors are 4 and 3 s.f. roundings %s, %s' % (q['id'], fmt(raw, 4), fmt(raw, 3)))
q = by('molar mass of calcium dihydrogen phosphate'); t = q['f'][0]['rows']
ok(all(r[2] == AM[r[0]] for r in t[:4]) and [int(r[1]) for r in t[:3]] == [atoms('Ca(H2PO4)2')[e] for e in ('Ca', 'H', 'P')] and
   all(D(r[3]) == D(r[1]) * D(r[2]) for r in t[:3]) and atoms('Ca(H2PO4)2')['O'] == 8, '%s table masses, counts, subtotals; O count = 8' % q['id'])

# ---------- numeric conversions ----------
print('Conversions (givens as written in the stem set the sig figs; exact counts and unit prefixes do not)')
M_ = MM
# (stem substring, givens as written, limiting factors (formulas whose molar mass is used, 'NA'), unit, {choice: (value, why[, unit])})
g = D
CALC = [
 # ch05-mole
 ('aluminum atoms are in 2.50 mol', ['2.50'], ['NA'], 'Al atoms', {0: (g('2.50') * NA, 'mol x NA'), 1: (g('2.50') / NA, 'flipped'), 2: (NA / g('2.50'), 'NA/mol'), 3: (g('2.50') * M_('Al'), 'used molar mass')}),
 ('4.65 &times; 10<sup>22</sup> silver atoms', ['4.65e22'], ['NA'], 'mol Ag', {0: (g('4.65e22') / NA, 'N/NA'), 1: (g('4.65e22') * NA, 'flipped'), 2: (NA / g('4.65e22'), 'NA/N'), 3: (g('4.65e22') / NA * M_('Ag'), 'went on to grams', 'g Ag')}),
 ('0.0196 mol of gas molecules', ['0.0196'], ['NA'], 'molecules', {0: (g('0.0196') * NA, 'mol x NA'), 1: (g('0.0196') / NA, 'flipped'), 2: (NA / g('0.0196'), 'NA/mol'), 3: (g('0.0196') * g('6.0221'), 'dropped x10^23')}),
 ('1.20 &times; 10<sup>24</sup> water molecules', ['1.20e24'], ['NA'], 'mol', {0: (g('1.20e24') / NA, 'N/NA'), 1: (g('1.20e24') * NA, 'flipped'), 2: (NA / g('1.20e24'), 'NA/N'), 3: (g('1.20e24') / NA * M_('H2O'), 'went on to grams', 'g')}),
 ('3.7 &times; 10<sup>13</sup> cells', ['3.7e13'], ['NA'], 'mol', {0: (g('3.7e13') / NA, 'N/NA'), 1: (g('3.7e13') * NA, 'flipped'), 2: (NA / g('3.7e13'), 'NA/N'), 3: (g('3.7e13'), 'skipped the conversion')}),
 ('mol of zinc. How many zinc atoms', ['2.85e-4'], ['NA'], 'Zn atoms', {0: (g('2.85e-4') * NA, 'mol x NA'), 1: (g('2.85e-4') / NA, 'flipped'), 2: (NA / g('2.85e-4'), 'NA/mol'), 3: (g('2.85e-4') * M_('Zn'), 'used molar mass', 'g Zn')}),
 ('molecules are in 3.25 mol', ['3.25'], ['NA'], 'N2 molecules', {0: (g('3.25') * NA, 'mol x NA'), 1: (g('3.25') / NA, 'flipped'), 2: (NA / g('3.25'), 'NA/mol'), 3: (2 * g('3.25') * NA, 'counted N atoms')}),
 ('8.43 &times; 10<sup>21</sup> molecules of carbon monoxide', ['8.43e21'], ['NA'], 'mol', {0: (g('8.43e21') / NA, 'N/NA'), 1: (g('8.43e21') * NA, 'flipped'), 2: (NA / g('8.43e21'), 'NA/N'), 3: (g('8.43e21') / NA * M_('CO'), 'went on to grams', 'g')}),
 ('copper atoms are in 0.660 mol', ['0.660'], ['NA'], 'Cu atoms', {0: (g('0.660') * NA, 'mol x NA'), 1: (g('0.660') / NA, 'flipped'), 2: (NA / g('0.660'), 'NA/mol'), 3: (g('0.660') * M_('Cu'), 'used molar mass', 'g Cu')}),
 ('3.6 &times; 10<sup>22</sup> chloride ions', ['3.6e22'], ['NA'], 'mol', {0: (g('3.6e22') / NA, 'N/NA'), 1: (g('3.6e22') * NA, 'flipped'), 2: (NA / g('3.6e22'), 'NA/N'), 3: (g('3.6e22') / NA * M_('Cl'), 'went on to grams', 'g')}),
 # ch05-convert
 ('12.5 g of sodium chloride', ['12.5'], ['NaCl'], 'mol', {0: (g('12.5') / M_('NaCl'), 'g/M'), 1: (g('12.5') * M_('NaCl'), 'flipped'), 2: (M_('NaCl') / g('12.5'), 'M/g'), 3: (g('12.5') / ZS('NaCl'), 'atomic numbers')}),
 ('mass of 0.475 mol', ['0.475'], ['CaCO3'], 'g', {0: (g('0.475') * M_('CaCO3'), 'mol x M'), 1: (g('0.475') / M_('CaCO3'), 'flipped'), 2: (M_('CaCO3') / g('0.475'), 'M/mol'), 3: (g('0.475') * ZS('CaCO3'), 'atomic numbers')}),
 ('reported as 126 mg/dL', ['126'], ['C6H12O6'], 'mmol/L', {0: (g(126) * 10 / M_('C6H12O6'), 'x10 dL/L / M'), 1: (g(126) / M_('C6H12O6'), 'skipped dL->L'), 2: (g(126) * 10 / M_('C6H12O6') / 1000, 'mol/L labeled mmol/L'), 3: (g(126) * 10 * M_('C6H12O6'), 'flipped')}),
 ('325 mg of aspirin', ['325'], ['C9H8O4'], 'mmol', {0: (g(325) / M_('C9H8O4'), 'mg/(mg/mmol)'), 1: (g(325) / M_('C9H8O4') / 1000, 'mol labeled mmol'), 2: (g(325) * M_('C9H8O4'), 'flipped'), 3: (g(325) * 1000 / M_('C9H8O4'), 'mg->g wrong way')}),
 ('ammonia molecules are in 3.50 g', ['3.50'], ['NH3', 'NA'], 'molecules', {0: (g('3.50') / M_('NH3') * NA, 'g/M x NA'), 1: (g('3.50') / M_('NH3'), 'stopped at mol'), 2: (g('3.50') * NA, 'skipped molar mass'), 3: (g('3.50') * M_('NH3') * NA, 'flipped molar mass')}),
 ('2.85 &times; 10<sup>20</sup> molecules of caffeine', ['2.85e20'], ['C8H10N4O2', 'NA'], 'g', {0: (g('2.85e20') / NA * M_('C8H10N4O2'), 'N/NA x M'), 1: (g('2.85e20') / NA, 'stopped at mol', 'mol'), 2: (g('2.85e20') / NA / M_('C8H10N4O2'), 'flipped M'), 3: (g('2.85e20') * M_('C8H10N4O2'), 'skipped NA')}),
 ('mass of <b>one</b> N<sub>2</sub>O molecule', [], ['N2O', 'NA'], 'g', {0: (M_('N2O') / NA, 'M/NA'), 1: (M_('N2O') * NA, 'M x NA'), 2: (NA / M_('N2O'), 'NA/M'), 3: (str(M_('N2O')), 'mass of a mole, as printed')}),
 ('8.00 mmol of potassium chloride', ['8.00'], ['KCl'], 'mg', {0: (g('8.00') * M_('KCl'), 'mmol x M'), 1: (g('8.00') / M_('KCl'), 'flipped'), 2: (g('8.00') * M_('KCl') / 1000, 'grams labeled mg'), 3: (g('8.00') * M_('K'), 'used K only')}),
 ('2.75 &times; 10<sup>23</sup> iron atoms', ['2.75e23'], ['Fe', 'NA'], 'g', {0: (g('2.75e23') / NA * M_('Fe'), 'N/NA x M'), 1: (g('2.75e23') / NA, 'stopped at mol', 'mol'), 2: (g('2.75e23') / NA * ZS('Fe'), 'atomic number'), 3: (g('2.75e23') / NA / M_('Fe'), 'flipped M')}),
 ('How many thyroxine molecules are in 0.150 mg', ['0.150'], ['C15H11I4NO4', 'NA'], 'molecules', {0: (g('0.150e-3') / M_('C15H11I4NO4') * NA, 'mg->g, /M, x NA'), 1: (g('0.150') / M_('C15H11I4NO4') * NA, 'skipped mg->g'), 2: (g('0.150e-3') / M_('C15H11I4NO4'), 'stopped at mol', 'mol'), 3: (g('0.150e-3') * M_('C15H11I4NO4') * NA, 'flipped M')}),
 ('1.00 g of calcium gluconate', ['1.00'], ['C12H22CaO14'], 'mmol', {0: (g('1.00') / M_('C12H22CaO14') * 1000, 'g/M -> mmol'), 1: (g('1.00') / M_('C12H22CaO14'), 'mol labeled mmol'), 2: (g('1.00') * M_('C12H22CaO14'), 'flipped'), 3: (g('1.00') / M_('Ca') * 1000, 'used Ca only')}),
 ('molecules are in 11.5 g', ['11.5'], ['C2H5OH', 'NA'], 'molecules', {0: (g('11.5') / M_('C2H5OH') * NA, 'g/M x NA'), 1: (g('11.5') / M_('C2H5OH'), 'stopped at mol'), 2: (g('11.5') * NA, 'skipped molar mass'), 3: (g('11.5') * M_('C2H5OH') * NA, 'flipped M')}),
 ('fasting glucose of 99 mg/dL', ['99'], ['C6H12O6'], 'mmol/L', {0: (g(99) * 10 / M_('C6H12O6'), 'x10 / M'), 1: (g(99) / M_('C6H12O6'), 'skipped dL->L'), 2: (g(99) * 10 / M_('C6H12O6') / 1000, 'mol/L labeled mmol/L'), 3: (g(99) * 10 * M_('C6H12O6'), 'flipped')}),
 ('500. mg of metformin hydrochloride', ['500.'], ['C4H11N5.HCl'], 'mmol', {0: (g(500) / M_('C4H11N5.HCl'), 'mg/M'), 1: (g(500) / M_('C4H11N5.HCl') / 1000, 'mol labeled mmol'), 2: (g(500) * M_('C4H11N5.HCl'), 'flipped'), 3: (g(500) / M_('C4H11N5'), 'left out HCl')}),
 ('mass of 0.0850 mol', ['0.0850'], ['NaHCO3'], 'g', {0: (g('0.0850') * M_('NaHCO3'), 'mol x M'), 1: (g('0.0850') / M_('NaHCO3'), 'flipped'), 2: (M_('NaHCO3') / g('0.0850'), 'M/mol'), 3: (g('0.0850') * ZS('NaHCO3'), 'atomic numbers')}),
 ('single glucose molecule', [], ['C6H12O6', 'NA'], 'g', {0: (M_('C6H12O6') / NA, 'M/NA'), 1: (M_('C6H12O6') * NA, 'M x NA'), 2: (NA / M_('C6H12O6'), 'NA/M'), 3: (str(M_('C6H12O6')), 'mass of a mole, as printed')}),
 ('contains 1.00 &times; 10<sup>20</sup> molecules', ['1.00e20'], ['C8H10N4O2', 'NA'], 'mg', {0: (g('1.00e20') / NA * M_('C8H10N4O2') * 1000, 'N/NA x M -> mg'), 1: (g('1.00e20') / NA * M_('C8H10N4O2'), 'grams labeled mg'), 2: (g('1.00e20') / NA, 'stopped at mol', 'mol'), 3: (g('1.00e20') / NA / M_('C8H10N4O2') * 1000, 'flipped M')}),
 ('4.65 mg of calcium ions', ['4.65'], ['Ca'], 'mmol', {0: (g('4.65') / M_('Ca'), 'mg/M'), 1: (g('4.65') / M_('Ca') * 1000, 'mg treated as g'), 2: (g('4.65') * M_('Ca'), 'flipped'), 3: (2 * g('4.65') / M_('Ca'), 'mEq, not mmol')}),
 ('2.50 g of O<sub>2</sub> gas', ['2.50'], ['O2', 'NA'], 'O2 molecules', {0: (g('2.50') / M_('O2') * NA, 'g/M x NA'), 1: (g('2.50') / M_('O') * NA, 'used O atom mass'), 2: (g('2.50') / M_('O2'), 'stopped at mol', 'mol'), 3: (g('2.50') * NA, 'skipped molar mass')}),
 ('serum potassium is 4.2 mmol/L', ['4.2'], ['K'], 'mg/dL', {0: (g('4.2') * M_('K') / 10, 'x M / 10'), 1: (g('4.2') * M_('K'), 'stopped at mg/L'), 2: (g('4.2') / M_('K') / 10, 'flipped'), 3: (g('4.2') * M_('K') / 10 / 1000, 'grams labeled mg')}),
 ('moles of water are in 45.0 g', ['45.0'], ['H2O'], 'mol', {0: (g('45.0') / M_('H2O'), 'g/M'), 1: (g('45.0') * M_('H2O'), 'flipped'), 2: (M_('H2O') / g('45.0'), 'M/g'), 3: (g('45.0') / ZS('H2O'), 'atomic numbers')}),
 ('molecules are in 1.00 mg of it', ['1.00'], ['C3H5N3O9', 'NA'], 'molecules', {0: (g('1.00e-3') / M_('C3H5N3O9') * NA, 'mg->g /M x NA'), 1: (g('1.00') / M_('C3H5N3O9') * NA, 'skipped mg->g'), 2: (g('1.00e-3') / M_('C3H5N3O9'), 'stopped at mol', 'mol'), 3: (g('1.00e-3') * M_('C3H5N3O9') * NA, 'flipped M')}),
 # ch05-formula (subscript ratios come from the checker's own parser)
 ('0.350 mol of calcium nitrate', ['0.350'], [], 'mol O', {0: (g('0.350') * atoms('Ca(NO3)2')['O'], 'x 6'), 1: (g('0.350') * 3, 'forgot parentheses'), 2: (g('0.350'), 'skipped subscript'), 3: (g('0.350') / atoms('Ca(NO3)2')['O'], 'flipped ratio')}),
 ('0.125 mol of ammonia', ['0.125'], ['NA'], 'H atoms', {0: (g('0.125') * atoms('NH3')['H'] * NA, 'x3 x NA'), 1: (g('0.125') * NA, 'skipped subscript'), 2: (g('0.125') * 3, 'stopped at mol H', 'mol H'), 3: (g('0.125') / 3 * NA, 'flipped ratio')}),
 ('released by 0.0450 mol', ['0.0450'], ['NA'], 'ions', {0: (g('0.0450') * 3 * NA, '3 ions x NA'), 1: (g('0.0450') * 2 * NA, 'Cl- only'), 2: (g('0.0450') * NA, 'formula units'), 3: (g('0.0450') * 4 * NA, 'counted the 2+ charge as ions')}),
 ('iron is in 0.400 mol', ['0.400'], ['Fe'], 'g Fe', {0: (g('0.400') * atoms('Fe2O3')['Fe'] * M_('Fe'), 'x2 x M(Fe)'), 1: (g('0.400') * M_('Fe'), 'skipped subscript'), 2: (g('0.400') * M_('Fe2O3'), 'mass of compound'), 3: (g('0.400') * 2 / M_('Fe'), 'flipped M')}),
 ('325 mg of ferrous fumarate', ['325'], ['FeC4H2O4', 'Fe'], 'mg Fe', {0: (g(325) / M_('FeC4H2O4') * M_('Fe'), 'mg->mmol->mg Fe'), 1: (g(325) / M_('FeC4H2O4'), 'stopped at mmol'), 2: (g(325) * M_('FeC4H2O4') / M_('Fe'), 'both flipped'), 3: (g(325) / M_('FeC4H2O4') * ZS('Fe'), 'atomic number')}),
 ('1.25 g of calcium carbonate', ['1.25'], ['CaCO3', 'Ca'], 'g Ca', {0: (g('1.25') / M_('CaCO3') * M_('Ca'), 'g->mol->g Ca'), 1: (g('1.25'), 'all of it is Ca'), 2: (g('1.25') / M_('CaCO3'), 'stopped at mol', 'mol Ca'), 3: (g('1.25') * M_('CaCO3') / M_('Ca'), 'flipped')}),
 ('2.21 mg of sodium fluoride', ['2.21'], ['NaF', 'F'], 'mg F', {0: (g('2.21') / M_('NaF') * M_('F'), 'mg->mmol->mg F'), 1: (g('2.21'), 'all of it is F'), 2: (g('2.21') * M_('NaF') / M_('F'), 'flipped'), 3: (g('2.21') / M_('NaF'), 'stopped at mmol')}),
 ('32.4 g of iohexol', ['32.4'], ['C19H26I3N3O9', 'I'], 'g I', {0: (g('32.4') / M_('C19H26I3N3O9') * atoms('C19H26I3N3O9')['I'] * M_('I'), 'x3 x M(I)'), 1: (g('32.4') / M_('C19H26I3N3O9') * M_('I'), 'skipped subscript'), 2: (g('32.4') / M_('C19H26I3N3O9') * 3 * ZS('I'), 'atomic number'), 3: (g('32.4') / M_('C19H26I3N3O9') * 3, 'stopped at mol I', 'mol I')}),
 ('nitrogen is in 125 g of urea', ['125'], ['CO(NH2)2', 'N'], 'g N', {0: (g(125) / M_('CO(NH2)2') * atoms('CO(NH2)2')['N'] * M_('N'), 'x2 x M(N)'), 1: (g(125) / M_('CO(NH2)2') * M_('N'), 'one N'), 2: (g(125) * M_('CO(NH2)2') / (2 * M_('N')), 'flipped'), 3: (g(125) / M_('CO(NH2)2') * 2 * M_('N2'), 'used N2 mass for N atoms')}),
 ('in 0.150 mol of it', ['0.150'], [], 'mol H', {0: (g('0.150') * atoms('(NH4)3PO4')['H'], 'x12'), 1: (g('0.150') * 4, 'inside subscript only'), 2: (g('0.150') * 3, 'outside subscript only'), 3: (g('0.150') / 12, 'flipped')}),
 ('contains 0.900 mol of oxygen atoms', ['0.900'], [], 'mol', {0: (g('0.900') / atoms('Al2(SO4)3')['O'], '/12'), 1: (g('0.900') * 12, 'multiplied'), 2: (g('0.900') / 4, 'forgot parentheses'), 3: (g('0.900') / 3, 'outside subscript only')}),
 ('sodium <b>ions</b> are in 1.00 g', ['1.00'], ['NaCl', 'NA'], 'Na^+ ions', {0: (g('1.00') / M_('NaCl') * NA, 'g/M x NA'), 1: (2 * g('1.00') / M_('NaCl') * NA, 'counted both ions'), 2: (g('1.00') / M_('NaCl'), 'stopped at mol', 'mol Na^+'), 3: (g('1.00') / M_('Na') * NA, 'used Na molar mass')}),
 ('find moles of each element in 0.200 mol', ['0.200'], [], 'mol O', {0: (g('0.200') * atoms('Ca3(PO4)2')['O'], 'x8'), 1: (g('0.200') * 4, 'inside only'), 2: (g('0.200') * 6, 'added subscripts'), 3: (g('0.200') / 8, 'flipped')}),
 ('0.250 mol of magnesium phosphate', ['0.250'], [], 'mol O', {0: (g('0.250') * atoms('Mg3(PO4)2')['O'], 'x8'), 1: (g('0.250') * 4, 'inside only'), 2: (g('0.250') / 8, 'flipped'), 3: (g('0.250') * 6, 'added subscripts')}),
 ('0.0750 mol of ammonium nitrate', ['0.0750'], ['NA'], 'N atoms', {0: (g('0.0750') * atoms('NH4NO3')['N'] * NA, 'x2 x NA'), 1: (g('0.0750') * NA, 'one N'), 2: (g('0.0750') * 2, 'stopped at mol N', 'mol N'), 3: (g('0.0750') / 2 * NA, 'flipped')}),
 ('nitrogen are in 2.50 kg', ['2.50'], ['NH4NO3', 'N'], 'kg N', {0: (g('2.50') / M_('NH4NO3') * atoms('NH4NO3')['N'] * M_('N'), 'x2 x M(N)'), 1: (g('2.50') / M_('NH4NO3') * M_('N'), 'one N'), 2: (g('2.50') * M_('NH4NO3') / (2 * M_('N')), 'flipped'), 3: (g('2.50') / M_('NH4NO3') * 2 * M_('N2'), 'used N2 mass')}),
 ('1.50 g of Ca<sub>3</sub>', ['1.50'], ['Ca3(C6H5O7)2', 'Ca'], 'g Ca', {0: (g('1.50') / M_('Ca3(C6H5O7)2') * atoms('Ca3(C6H5O7)2')['Ca'] * M_('Ca'), 'x3 x M(Ca)'), 1: (g('1.50') / M_('Ca3(C6H5O7)2') * M_('Ca'), 'skipped subscript'), 2: (g('1.50') * M_('Ca3(C6H5O7)2') / (3 * M_('Ca')), 'flipped'), 3: (g('1.50') / M_('Ca3(C6H5O7)2'), 'stopped at mol compound', 'mol Ca')}),
 ('come from 0.0200 mol', ['0.0200'], [], 'mol ions', {0: (g('0.0200') * (atoms('Na3PO4')['Na'] + 1), '3 Na+ + 1 PO4'), 1: (g('0.0200') * 3, 'Na+ only'), 2: (g('0.0200'), 'formula units'), 3: (g('0.0200') * sum(atoms('Na3PO4').values()), 'split the polyatomic ion')}),
 ('potassium ions are in 1.49 g', ['1.49'], ['KCl', 'NA'], 'K^+ ions', {0: (g('1.49') / M_('KCl') * NA, 'g/M x NA'), 1: (2 * g('1.49') / M_('KCl') * NA, 'counted both ions'), 2: (g('1.49') / M_('K') * NA, 'used K molar mass'), 3: (g('1.49') / M_('KCl'), 'stopped at mol', 'mol K^+')}),
 ('contains 0.100 g of iodine', ['0.100'], ['KI', 'I'], 'g KI', {0: (g('0.100') / M_('I') * M_('KI'), 'g I->mol->g KI'), 1: (g('0.100') * M_('I') / M_('KI'), 'flipped'), 2: (g('0.100') / M_('I'), 'stopped at mol', 'mol'), 3: (g('0.100'), 'all of it is I')}),
 ('oxygen is in 0.600 mol of water', ['0.600'], ['O'], 'g O', {0: (g('0.600') * M_('O'), 'x M(O)'), 1: (g('0.600') * M_('O2'), 'used O2'), 2: (g('0.600') * M_('H2O'), 'mass of water'), 3: (g('0.600') / M_('O'), 'flipped')}),
 ('hydrogen atoms are in 5.00 g of ethanol', ['5.00'], ['C2H5OH', 'NA'], 'H atoms', {0: (g('5.00') / M_('C2H5OH') * atoms('C2H5OH')['H'] * NA, 'x6 x NA'), 1: (g('5.00') / M_('C2H5OH') * NA, 'molecules'), 2: (g('5.00') / M_('C2H5OH') * 6, 'stopped at mol H', 'mol H'), 3: (g('5.00') / M_('C2H5OH') * 5 * NA, 'missed the OH hydrogen')}),
]
for sub, given, fac, unit, ch in CALC:
    q = by(sub)
    if not q: continue
    checked.add(q['id'])
    stem = txt(q['q'])
    for gv in given:   # each given appears in the stem exactly as written
        if 'e' in gv:
            m_, e_ = gv.split('e'); pat = re.escape(m_) + r' x 10\^' + re.escape(e_)
        else:
            pat = r'(?<![\d.])' + re.escape(gv) + (r'(?![\d])' if gv.endswith('.') else r'(?![\d.])')
        if not re.search(pat, stem): err.append(q['id'] + ' given %r not in stem as written' % gv)
    # a molar mass stated in the stem must be the checker's value for one of the formulas used
    for val in re.findall(r'(\d+\.\d+) g/mol', stem):
        if val not in [str(M_(f)) for f in fac if f != 'NA']: err.append(q['id'] + ' stem molar mass %s g/mol not one of %s' % (val, [str(M_(f)) for f in fac if f != 'NA']))
    n = min([sf(gv) for gv in given] + [sf(str(M_(f))) if f != 'NA' else 5 for f in fac] + [5])
    print('  %s %s (%d s.f.)' % (q['id'], sub[:48].replace('&times; 10<sup>', 'e').replace('</sup>', ''), n))
    keys = []
    for j, spec in sorted(ch.items()):
        v, why = spec[0], spec[1]; u = spec[2] if len(spec) > 2 else unit
        want = (v if isinstance(v, str) else fmt(v, n)) + ' ' + u; keys.append(want)
        ok(txt(q['c'][j]).strip() == want, '%s c[%d] %-28r = %r (%s)' % (q['id'], j, txt(q['c'][j]).strip(), want, why))
    if len(set(keys)) != 4: err.append(q['id'] + ' recomputed values not all different: %s' % keys)
    if fmt(ch[0][0], n) not in txt(q['w']): err.append(q['id'] + ' answer %s not in w' % fmt(ch[0][0], n))
    if q['k'] != 1: err.append(q['id'] + ' calculation item without k=1')

# ---------- counting, ranking and sanity items ----------
print('Counting, ranking and sanity items')
def mol_atoms(ch):
    m = re.match(r'([\d.]+) mol of (\S+)', txt(ch)); return D(m.group(1)) * sum(atoms(m.group(2)).values())
for q in [by('greatest number of atoms</b>?'), by('most atoms in total</b>?')]:
    checked.add(q['id']); v = [mol_atoms(c) for c in q['c']]
    ok(v[0] == max(v) and v.count(v[0]) == 1, '%s mol of atoms %s; c[0] largest' % (q['id'], [str(x) for x in v]))
q = by('greatest number of particles'); checked.add(q['id'])
def as_mol(ch):
    t = txt(ch); m = re.match(r'([\d.]+) mol', t)
    if m: return D(m.group(1))
    m = re.match(r'([\d.]+) x 10\^(\d+)', t); return D(m.group(1)) * D(10) ** int(m.group(2)) / NA
v = [as_mol(c) for c in q['c']]; ok(v[0] == max(v) and v.count(v[0]) == 1, '%s moles %s' % (q['id'], ['%.3f' % x for x in v]))
q = by('greatest mass</b>'); checked.add(q['id'])
def mass(ch):
    t = txt(ch); f = t.split()[-1] if ' of ' in t else t.split()[3]
    return as_mol(ch) * M_(f)
v = [mass(c) for c in q['c']]; ok(v[0] == max(v) and v.count(v[0]) == 1, '%s masses %s g' % (q['id'], ['%.2f' % x for x in v]))
for f, s_ in (('H2O', '18.015'), ('CO2', '44.009'), ('NH3', '17.031'), ('C6H12O6', '180.156')):
    if f + ' ' + s_ not in txt(q['q']): err.append(q['id'] + ' stem molar mass for %s' % f)
    if str(M_(f)) != s_: err.append(q['id'] + ' molar mass %s %s != %s' % (f, s_, M_(f)))
q = by('contains the <b>most molecules</b>'); checked.add(q['id'])
st = [re.match(r'(\S+) \(([\d.]+) g/mol\)', txt(c)).groups() for c in q['c']]
ok(all(str(M_(f)) == s_ for f, s_ in st) and min(st, key=lambda x: D(x[1])) == st[0], '%s stated molar masses correct; smallest is c[0] %s' % (q['id'], st[0][0]))
q = by('0.50 mol of water contains 8.3'); checked.add(q['id'])
ok(fmt(D('0.50') / NA, 2) == '8.3 x 10^-25' and fmt(D('0.50') * NA, 2) in txt(q['y'][0]), '%s 0.50/NA = %s; correct %s' % (q['id'], fmt(D('0.50') / NA, 2), fmt(D('0.50') * NA, 2)))
q = by('gets 3.5 &times; 10<sup>47</sup> mol'); checked.add(q['id'])
ok(fmt(D('5.8e23') * NA, 2) == '3.5 x 10^47' and fmt(D('5.8e23') / NA, 2) in txt(q['w']), '%s 5.8e23 x NA = %s; correct %s mol' % (q['id'], fmt(D('5.8e23') * NA, 2), fmt(D('5.8e23') / NA, 2)))
q = by('as printed on the CHEM 3A yellow sheet'); checked.add(q['id'])
ok(txt(q['c'][0]).startswith('6.0221 x 10^23') and NA == D('6.0221e23') and q['c'][2].startswith(AM['C']), '%s N_A and C molar mass decoy' % q['id'])
q = by('oxygen <b>atoms</b> are in 1 mol of sulfuric acid'); checked.add(q['id'])
a_ = atoms('H2SO4'); ok(q['c'][0] == '%d mol O' % a_['O'] and q['c'][3] == '%d mol O' % sum(a_.values()) and q['c'][2] == '%d mol O' % (a_['O'] // 2), '%s H2SO4 O=%d, total %d' % (q['id'], a_['O'], sum(a_.values())))
q = by('moles of <b>hydrogen atoms</b> from moles of glucose'); checked.add(q['id'])
a_ = atoms('C6H12O6'); ok(txt(q['c'][0]).startswith('%d mol H' % a_['H']) and txt(q['c'][3]).startswith('%d mol H' % sum(a_.values())) and txt(q['c'][2]).startswith('%d mol H' % a_['C']), '%s glucose H=%d, total %d' % (q['id'], a_['H'], sum(a_.values())))
q = by('how many moles of {K^+}'.replace('{K^+}', 'K<sup>+</sup>')); checked.add(q['id'])
a_ = atoms('K2SO4'); ok(txt(q['c'][0]) == '%d mol K^+; %d mol of ions in total' % (a_['K'], a_['K'] + 1) and txt(q['c'][1]).endswith('%d mol of ions in total' % sum(a_.values())), '%s K2SO4 -> %d K+, %d ions (split sulfate would be %d)' % (q['id'], a_['K'], a_['K'] + 1, sum(a_.values())))
q = by('mass of <b>one</b> NaCl formula unit, in amu'); checked.add(q['id'])
ok(q['c'][0] == str(M_('NaCl')) + ' amu' and txt(q['c'][2]) == fmt(M_('NaCl') / NA, 4) + ' amu' and txt(q['c'][3]) == fmt(M_('NaCl') * NA, 4) + ' amu', '%s 58.44 amu; g per unit %s' % (q['id'], fmt(M_('NaCl') / NA, 4)))
q = by('which molar mass should you use for oxygen'); checked.add(q['id'])
ok(q['c'][0].startswith(AM['O']) and q['c'][1].startswith(str(M_('O2'))) and q['c'][2].startswith(str(M_('CO2'))) and q['c'][3].startswith(str(ZN['O'])) and fmt(D('2.00') * 2 * M_('O'), 3) + ' g O' in txt(q['w']), '%s O 15.999 vs O2 %s vs CO2 %s; 64.0 g O' % (q['id'], M_('O2'), M_('CO2')))
q = by('Complete the road-map table for ethanol'); R = q['f'][0]['rows']; r = [None, R[0][1], R[1][1], R[2][1], R[3][1]]
ok(r[2] == str(M_('H2O')) and r[3] == fmt(D(r[1]) / M_('H2O'), 3) and txt(r[4]) == fmt(D(r[1]) / M_('H2O') * NA, 3) and R[1][2] == str(M_('C2H5OH')) and R[0][2] == '11.5', '%s table water column %s g -> %s mol -> %s' % (q['id'], r[1], r[3], txt(r[4])))
q = by('find moles of each element in 0.200 mol'); r = q['f'][0]['rows']
ok([int(x[1]) for x in r] == [atoms('Ca3(PO4)2')[e] for e in ('Ca', 'P', 'O')] and r[0][2] == fmt(D('0.200') * 3, 3) and r[1][2] == fmt(D('0.200') * 2, 3), '%s table counts and moles' % q['id'])
# conceptual items that still contain numbers: the numbers must be right
q = by('1.00 mol of copper atoms and 1.00 mol of sucrose'); ok(str(M_('C12H22O11')) in q['y'][0] and AM['Cu'] in q['y'][0], q['id'] + ' sucrose 342.297 and Cu 63.55 quoted')
q = by('has a molar mass of 180.156 g/mol. Which statement'); ok(str(M_('C6H12O6')) == '180.156', q['id'] + ' glucose 180.156')
q = by('1 mol of {O2} molecules and 1 mol of O atoms compare'.replace('{O2}', 'O<sub>2</sub>')); ok(str(M_('O2')) in q['c'][0] and AM['O'] in q['c'][0], q['id'] + ' O2 31.998 vs O 15.999')

# ---------- global consistency ----------
print('Global checks: quoted atomic masses, answer-side g/mol values, trailing-zero rule in calculation stems')
FORMS = set()
for sub, f, unit, ch in MMQ: FORMS.add(f)
REG = {str(M_(f)) for f in FORMS} | set(AM.values())
for f in ('H2O', 'NaCl', 'CO2', 'NH3', 'CH4', 'C6H12O6', 'CaCO3', 'C9H8O4', 'N2O', 'KCl', 'C15H11I4NO4', 'C12H22CaO14', 'C2H5OH',
          'FeC4H2O4', 'NaF', 'C19H26I3N3O9', 'CO(NH2)2', 'C4H11N5.HCl', 'C4H11N5', 'NaHCO3', 'C8H10N4O2', 'O2', 'C3H5N3O9',
          'NH4NO3', 'Ca3(C6H5O7)2', 'KI', 'Fe2O3', 'N2', 'CO', 'C12H22O11', 'Na2CO3'):
    REG.add(str(M_(f)))
for q in ALL:
    right = ' '.join([q['q'], q['w'], q['y'][0], q['c'][0], q['h']] + [' '.join(r) for f in q.get('f', []) for r in f['rows']])
    t = txt(right)
    for sym, val in re.findall(r'(?<![A-Za-z(\d])([A-Z][a-z]?) (\d+\.\d{2,})(?![\d])', t):
        if sym in AM and D(val) >= 1 and AM[sym] != val: err.append('%s quotes %s %s; yellow sheet %s' % (q['id'], sym, val, AM[sym]))
    for val in re.findall(r'(?<![\d.])(\d+\.\d+) g/mol', t):
        if val not in REG: err.append('%s answer-side molar mass %s g/mol not recomputed' % (q['id'], val))
    if q['k'] == 1:
        s = re.sub(r'<sub>\d+</sub>', '', q['q']); s = re.sub(r'&middot;\d+', '', s); s = txt(s)
        for m in re.finditer(r'(?<![\d.^])(\d*[1-9]\d*0)(?![\d.^])', s):
            err.append(q['id'] + ' calculation stem has ambiguous trailing-zero value %r' % m.group(1))
# exactly one correct choice: the recomputed key differs from all distractors (dup-choice check) and c[0] is the key
for q in ALL:
    if q['k'] == 1 and q['id'] not in checked: err.append(q['id'] + ' calculation item not recomputed')

# ---------- coverage, counts, duplicates ----------
print('Items with a machine check: %d of %d (the rest are conceptual; read by hand)' % (len(checked), len(ALL)))
print('  not machine-checked:', ' '.join(q['id'] for q in ALL if q['id'] not in checked))
for nm, B in (('Try It', TRY), ('ADAPT', HW)):
    print(nm, len(B), dict(collections.Counter(q['t'] for q in B)), 'with figures:', sum(1 for q in B if q.get('f')),
          'd:', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1:', sum(q['k'] for q in B))
if len(HW) != 40: err.append('ADAPT has %d items, not 40' % len(HW))
norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip().lower()
dup = set(norm(q['q']) for q in TRY) & set(norm(q['q']) for q in HW)
if dup: err.append('same question in both banks: %s' % dup)
print('ERRORS:', err if err else 'none')
