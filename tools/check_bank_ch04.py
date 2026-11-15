#!/usr/bin/env python3
"""Checker for the Chapter 4 banks (naming compounds). Structural checks copied from tools/check_bank_ch03.py
(ch04 topic ids; only 'table' figures allowed), plus, with its own ion tables and name generators:
  * every formula in a right answer is parsed and must be a known ion, a charge-balanced and reduced ionic
    compound (hydrates included), an acid whose H count equals the anion charge, or a compound of nonmetals only;
  * atom counts, compound types, deduced ion charges, ion names and formulas, ionic / molecular / acid names
    from formulas and formulas from names are re-derived for every item listed in SPEC, and every distractor
    must NOT also be a right answer;
  * scope: only the elements, metals, Roman numerals and polyatomic ions of Sections 4.1-4.6.
usage: python3 tools/check_bank_ch04.py bank/ch04.json bank/ch04_adapt.json"""
import json, sys, re, collections, html
from math import gcd
TRY = json.load(open(sys.argv[1])); HW = json.load(open(sys.argv[2]))
TOP = {'ch04-formulas', 'ch04-ionicformula', 'ch04-polyatomic', 'ch04-ionicname', 'ch04-molecular', 'ch04-acids'}
err = []

# ---------- structural checks (same as ch03 checker) ----------
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
        if '{' in s or '}' in s: err.append(i + ' unexpanded {formula}')
        if 'f' in q and not allow_f: err.append(i + ' has f (ADAPT items must be text only)')
        for f in q.get('f', []):
            if f['type'] != 'table': err.append(i + ' figure type not used/checked here: ' + f['type'])
        if label == 'HW' and not q['y'][0].startswith('Correct: '): err.append(i + ' ADAPT y[0] lacks "Correct: "')
        plain = lambda x: re.sub(r'<[^>]+>', '', x).strip().lower()
        right = plain(q['c'][0])
        if len(right) > 3:
            for j in (1, 2, 3):
                if right in plain(q['y'][j]): err.append(i + ' y[%d] names the right answer' % j)
structural(TRY, 'c4-%03d', 'TRY', True)
structural(HW, 'c4-h%02d', 'HW', False)
ALL = TRY + HW

def txt(x):
    x = re.sub(r'<sub>(\d+)</sub>', r'\1', x)
    x = re.sub(r'<sup>([^<]*)</sup>', r'^\1', x)
    x = re.sub(r'<[^>]+>', '', x)
    x = x.replace('&minus;', '-').replace('&middot;', '.')
    return html.unescape(x).replace('−', '-').replace(' ', ' ')
def ok(cond, msg):
    print('   ', 'OK ' if cond else 'BAD', msg)
    if not cond: err.append(msg)
def norm(s): return re.sub(r'\s+', ' ', s).strip().lower()

# ---------- element and ion tables (from Sections 4.1-4.5) ----------
ELNAME = dict(H='hydrogen', B='boron', C='carbon', N='nitrogen', O='oxygen', F='fluorine', Si='silicon', P='phosphorus',
              S='sulfur', Cl='chlorine', Se='selenium', Br='bromine', I='iodine', He='helium', Ne='neon', Ar='argon',
              Li='lithium', Na='sodium', K='potassium', Rb='rubidium', Cs='cesium', Mg='magnesium', Ca='calcium', Sr='strontium',
              Ba='barium', Al='aluminum', Zn='zinc', Ag='silver', Cu='copper', Fe='iron', Co='cobalt', Cr='chromium', Sn='tin',
              Pb='lead', Hg='mercury', Mn='manganese')
NONMETAL = set('H B C N O F Si P S Cl Se Br I He Ne Ar'.split())
IDE = dict(H='hydride', B='boride', C='carbide', N='nitride', O='oxide', F='fluoride', Si='silicide', P='phosphide',
           S='sulfide', Cl='chloride', Se='selenide', Br='bromide', I='iodide')
DIATOMIC = {'H', 'N', 'O', 'F', 'Cl', 'Br', 'I'}
ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}
# cations: (unit, charge, [names])
FIXED = [('Li', 1), ('Na', 1), ('K', 1), ('Rb', 1), ('Cs', 1), ('Mg', 2), ('Ca', 2), ('Sr', 2), ('Ba', 2), ('Al', 3), ('Zn', 2), ('Ag', 1)]
CATIONS = [(u, z, [ELNAME[u]]) for u, z in FIXED] + [('NH4', 1, ['ammonium'])]
VAR = [('Cu', 1, 'cuprous'), ('Cu', 2, 'cupric'), ('Fe', 2, 'ferrous'), ('Fe', 3, 'ferric'), ('Co', 2, 'cobaltous'), ('Co', 3, 'cobaltic'),
       ('Cr', 2, 'chromous'), ('Cr', 3, 'chromic'), ('Sn', 2, 'stannous'), ('Sn', 4, 'stannic'), ('Pb', 2, 'plumbous'), ('Pb', 4, 'plumbic'),
       ('Hg2', 2, 'mercurous'), ('Hg', 2, 'mercuric')]
for u, z, old in VAR:
    el = 'Hg' if u == 'Hg2' else u; num = 1 if u == 'Hg2' else z
    CATIONS.append((u, z, ['%s(%s)' % (ELNAME[el], ROMAN[num]), old]))
VARCHG = collections.defaultdict(set)
for u, z, old in VAR: VARCHG[ELNAME['Hg' if u == 'Hg2' else u]].add(1 if u == 'Hg2' else z)
# anions: (unit, charge, [names]); oxyanion families built from the -ate ion by the 4.2 rules
ANIONS = [(s, z, [IDE[s]]) for s, z in (('F', -1), ('Cl', -1), ('Br', -1), ('I', -1), ('O', -2), ('S', -2), ('N', -3), ('P', -3))]
def family(el, root, nate, z, per_hypo):
    out = [(el + 'O' + str(nate), z, [root + 'ate']), (el + ('O' + str(nate - 1) if nate - 1 > 1 else 'O'), z, [root + 'ite'])]
    if per_hypo: out += [(el + 'O' + str(nate + 1), z, ['per' + root + 'ate']), (el + ('O' + str(nate - 2) if nate - 2 > 1 else 'O'), z, ['hypo' + root + 'ite'])]
    return out
for el, root in (('Cl', 'chlor'), ('Br', 'brom'), ('I', 'iod')): ANIONS += family(el, root, 3, -1, True)
ANIONS += family('S', 'sulf', 4, -2, False) + family('N', 'nitr', 3, -1, False) + family('P', 'phosph', 4, -3, False)
ANIONS += [('CO3', -2, ['carbonate']), ('HCO3', -1, ['hydrogen carbonate', 'bicarbonate']), ('HSO4', -1, ['hydrogen sulfate', 'bisulfate']),
           ('HSO3', -1, ['hydrogen sulfite', 'bisulfite']), ('HPO4', -2, ['hydrogen phosphate']), ('H2PO4', -1, ['dihydrogen phosphate']),
           ('OH', -1, ['hydroxide']), ('CN', -1, ['cyanide']), ('C2H3O2', -1, ['acetate']), ('C2O4', -2, ['oxalate']),
           ('MnO4', -1, ['permanganate']), ('O2', -2, ['peroxide']), ('CrO4', -2, ['chromate']), ('Cr2O7', -2, ['dichromate'])]
ION_ONLY = [('H3O', 1, ['hydronium'])]
def chg(z): return (str(abs(z)) if abs(z) > 1 else '') + ('+' if z > 0 else '-')
ION = {}       # 'SO4^2-' -> names
for u, z, nm in CATIONS + ANIONS + ION_ONLY: ION.setdefault(u + '^' + chg(z), []).extend(nm)
ION['Hg2^2+'] = ['mercury(I)', 'mercurous']
ION = {k: [n.lower() for n in v] for k, v in ION.items()}
ION_BY_NAME = {n: k for k, v in ION.items() for n in v}
ANION_NAMES = {n for _, _, v in ANIONS for n in v}
PRE = {1: 'mono', 2: 'di', 3: 'tri', 4: 'tetra', 5: 'penta', 6: 'hexa', 7: 'hepta', 8: 'octa', 9: 'nona', 10: 'deca'}

# ---------- formula parsing ----------
def atoms(fm):
    """Counter of atoms; handles a leading coefficient ('2 C6H12O6'), parentheses, hydrates, (aq), charges."""
    fm = fm.strip(); coef = 1
    m = re.match(r'(\d+)\s*(?=[A-Z(])', fm)
    if m: coef = int(m.group(1)); fm = fm[m.end():]
    fm = re.sub(r'\^.*$', '', fm); fm = re.sub(r'\((aq|g)\)$', '', fm)
    tot = collections.Counter()
    for k, part in enumerate(fm.split('.')):
        n = 1
        if k:
            mm = re.match(r'(\d*)', part); n = int(mm.group(1) or 1); part = part[len(mm.group(1)):]
        def grp(s, i):
            c = collections.Counter()
            while i < len(s):
                if s[i] == '(':
                    sub, i = grp(s, i + 1); mm = re.match(r'\d*', s[i:]); i += len(mm.group())
                    for e, v in sub.items(): c[e] += v * int(mm.group() or 1)
                elif s[i] == ')': return c, i + 1
                else:
                    mm = re.match(r'([A-Z][a-z]?)(\d*)', s[i:])
                    if not mm: raise ValueError('bad formula ' + s)
                    c[mm.group(1)] += int(mm.group(2) or 1); i += len(mm.group())
            return c, i
        c, _ = grp(part, 0)
        for e, v in c.items(): tot[e] += v * n
    return collections.Counter({e: v * coef for e, v in tot.items()})
def symbols(fm): return re.findall(r'[A-Z][a-z]?', re.sub(r'\((aq|g)\)', '', fm))
def unit_take(s, u):
    out = []
    if s.startswith('(' + u + ')'):
        r = s[len(u) + 2:]; m = re.match(r'\d+', r)
        if m: out.append((int(m.group()), r[m.end():]))
    if s.startswith(u):
        r = s[len(u):]; m = re.match(r'\d+', r)
        if m and re.fullmatch(r'[A-Z][a-z]?', u): out.append((int(m.group()), r[m.end():]))
        out.append((1, r))
    return out
def decompose(base):
    """All ways to read base as (cation x nc)(anion x na) with ions from the tables; [(cat, zc, nc, an, za, na)]."""
    res = []
    for cu, zc, _ in CATIONS:
        for nc, rest in unit_take(base, cu):
            for au, za, _ in ANIONS:
                for na, r2 in unit_take(rest, au):
                    if r2 == '': res.append((cu, zc, nc, au, za, na))
    return res
def ionic_ok(base):
    """balanced and reduced reading, or None"""
    for p in decompose(base):
        cu, zc, nc, au, za, na = p
        if nc * zc + na * za == 0 and gcd(nc, na) == 1: return p
    return None
def part(u, n): return u if n == 1 else (u + str(n) if re.fullmatch(r'[A-Z][a-z]?', u) else '(' + u + ')' + str(n))
# universe of ionic compounds built by swap-drop + reduce
IONIC = {}
for cu, zc, cn in CATIONS:
    for au, za, an in ANIONS:
        g = gcd(zc, -za); f = part(cu, -za // g) + part(au, zc // g)
        IONIC.setdefault(f, set()).update((a + ' ' + b).lower() for a in cn for b in an)
# acids
ACID = {}   # formula without (aq) -> (names, binary?)
for s, z, r in (('F', 1, 'fluor'), ('Cl', 1, 'chlor'), ('Br', 1, 'brom'), ('I', 1, 'iod'), ('S', 2, 'sulfur')):
    ACID['H' + (str(z) if z > 1 else '') + s] = ({'hydro' + r + 'ic acid'}, True)
for au, za, an in ANIONS:
    nm = an[0]
    if au in ('OH', 'CN', 'O2', 'MnO4', 'CrO4', 'Cr2O7') or au.startswith('H') or not re.search(r'(ate|ite)$', nm): continue
    root = nm[:-3]; root = root + 'ur' if root.endswith('sulf') else root + 'or' if root.endswith('phosph') else root
    ACID['H' + (str(-za) if -za > 1 else '') + au] = ({root + ('ic' if nm.endswith('ate') else 'ous') + ' acid'}, False)
# molecular (two nonmetals) and common names
MOL = {}
for a in NONMETAL - {'He', 'Ne', 'Ar'}:
    for b in IDE:
        if a == b: continue
        for n1 in range(1, 11):
            for n2 in range(1, 11):
                p = PRE[n2]
                sec = [p[:-1] + IDE[b]] if (IDE[b][0] == 'o' and p[-1] in 'ao') else [p + IDE[b]]
                if n2 == 4 and IDE[b] == 'oxide': sec.append('tetraoxide')
                first = (PRE[n1] if n1 > 1 else '') + ELNAME[a]
                MOL[a + (str(n1) if n1 > 1 else '') + b + (str(n2) if n2 > 1 else '')] = {first + ' ' + s for s in sec}
COMMON = {'H2O': {'water'}, 'NH3': {'ammonia'}, 'CH4': {'methane'}, 'H2O2': {'hydrogen peroxide'}, 'N2O': {'nitrous oxide'},
          'NO': {'nitric oxide'}, 'N2H4': {'hydrazine'}}
for k, v in COMMON.items(): MOL.setdefault(k, set()).update(v)

def strip_aq(f): return re.sub(r'\((aq|g)\)$', '', f)
def kind(f):
    if '^' in f: return 'ion'
    b = strip_aq(f)
    if b.startswith('H') and (f.endswith('(aq)') or (b in ACID and not ACID[b][1])): return 'acid'
    if ionic_ok(b.split('.')[0]) or b.split('.')[0] in IONIC: return 'ionic'
    if all(s in NONMETAL for s in symbols(b)): return 'molecular'
    return 'unknown'
def names_of(f):
    k = kind(f); b = strip_aq(f)
    if k == 'ion': return set(ION.get(f, []))
    if k == 'acid': return set(ACID[b][0]) if b in ACID else set()
    if k == 'ionic':
        base, *hyd = b.split('.')
        nm = IONIC.get(base, set())
        if hyd:
            n = int(re.match(r'(\d*)H2O$', hyd[0]).group(1) or 1)
            nm = {x + ' ' + PRE[n] + 'hydrate' for x in nm}
        return nm
    if k == 'molecular': return set(MOL.get(b, set()))
    return set()
NAME2F = collections.defaultdict(set)
for f, ns in IONIC.items():
    for n in ns: NAME2F[n].add(f)
for f, (ns, binary) in ACID.items():
    for n in ns:
        NAME2F[n].add(f + '(aq)')
        if not binary: NAME2F[n].add(f)
for f, ns in MOL.items():
    for n in ns: NAME2F[n].add(f)
for k, v in ION.items():
    for n in v: NAME2F[n + ' ion'].add(k)
def formulas_of(name):
    name = norm(name)
    m = re.match(r'(.*) (mono|di|tri|tetra|penta|hexa|hepta|octa|nona|deca)hydrate$', name)
    if m:
        n = {v: k for k, v in PRE.items()}[m.group(2)]
        return {f + '.' + (str(n) if n > 1 else '') + 'H2O' for f in NAME2F.get(m.group(1), set())}
    return set(NAME2F.get(name, set()))
def fstat(f):
    """status of one formula appearing in a right answer"""
    k = kind(f); b = strip_aq(f)
    if k == 'ion': return 'ion' if f in ION else 'unknown ion ' + f
    if k == 'acid':
        m = re.match(r'H(\d*)(.*)$', b); n = int(m.group(1) or 1)
        an = [z for u, z, _ in ANIONS if u == m.group(2)]
        if not an: return 'acid with unknown anion ' + f
        if n != -an[0]: return 'acid H count %d != anion charge %d' % (n, an[0])
        if b in ACID and ACID[b][1] and not f.endswith('(aq)'): return 'binary acid without (aq) ' + f
        return 'acid H%d + %s%+d' % (n, m.group(2), an[0])
    if k == 'ionic':
        base, *hyd = b.split('.'); p = ionic_ok(base)
        if not p: return 'ionic formula not balanced/reduced ' + f
        cu, zc, nc, au, za, na = p
        return 'ionic %d(%+d) + %d(%+d) = 0' % (nc, zc, na, za)
    if k == 'molecular': return 'molecular'
    return 'unknown formula ' + f
FTOK = re.compile(r'^(?:\d+ )?(?:\(?(?:[A-Z][a-z]?\d*)+\)?\d*)+(?:\.\d*H2O)?(?:\((?:aq|g)\))?(?:\^\d*[+-])?$')
def formulas_in(s):
    out = []
    for tok in re.split(r'[\s:;,]+(?![A-Z][a-z]?\d)', txt(s)):
        tok = tok.strip().rstrip('.?')
        if tok and FTOK.match(tok) and all(x in ELNAME for x in symbols(tok)) and (re.search(r'[\d(^]', tok) or len(symbols(tok)) > 1):
            out.append(tok)
    return out
def num_charge(s):
    m = re.fullmatch(r'(\d*)\s*([+-])', txt(s).strip()); return int(m.group(1) or 1) * (1 if m.group(2) == '+' else -1)

# ---------- every formula in a right answer ----------
print('Formulas in right answers (charge balance, H counts, known ions)')
for q in ALL:
    for f in formulas_in(q['c'][0]):
        st = fstat(f)
        ok(not st.startswith(('unknown', 'ionic formula not', 'acid H count', 'binary acid', 'acid with')), '%s c[0] %s: %s' % (q['id'], f, st))

# ---------- per-item checks ----------
def by(sub):
    m = [q for q in ALL if sub in q['q']]
    if len(m) != 1: err.append('lookup %r matched %d items' % (sub, len(m))); return None
    return m[0]
checked = set()
C = lambda q: [txt(c).strip() for c in q['c']]
SPEC = [
 # ---- Try It: formulas ----
 ('Aluminum nitrate has the formula', 'count', 'Al(NO3)3', 'O'),
 ('Ammonium sulfate, ', 'count', '(NH4)2SO4', None),
 ('Tooth enamel is mostly hydroxyapatite', 'count', 'Ca10(PO4)6(OH)2', 'O'),
 ('muscle cells break down glucose', 'count', '2 C6H12O6', 'C'),
 ('exists as a <b>diatomic</b>', 'diatomic'),
 ('supplemental oxygen from a tank', 'diatomic'),
 ('<b>ionic</b> even though every element', 'pick', 'ionic'),
 ('Which of these is an <b>acid</b>', 'pick', 'acid'),
 ('Which of these compounds is <b>molecular</b>', 'pick', 'molecular'),
 ('active ingredient in milk of magnesia', 'classify', 'Mg(OH)2'),
 # ---- ionicformula ----
 ('<b>calcium and nitrogen</b>', 'n2f', 'calcium nitride', 'nostem'),
 ('formula of <b>barium sulfide</b>', 'n2f', 'barium sulfide'),
 ('Dental air-abrasion units', 'n2f', 'aluminum oxide'),
 ('formula of <b>magnesium phosphate</b>', 'n2f', 'magnesium phosphate'),
 ('Lithium carbonate is a medication', 'n2f', 'lithium carbonate'),
 ('formula of <b>ammonium sulfide</b>', 'n2f', 'ammonium sulfide'),
 ('Chromium(III) ions combine with hydroxide', 'n2f', 'chromium(III) hydroxide', 'nostem'),
 ('each <b>cobalt</b> ion in', 'charge', 'Co2O3', 'cation'),
 ('each <b>iron</b> ion in', 'charge', 'Fe3(PO4)2', 'cation'),
 ('Calcium oxalate, ', 'charge', 'CaC2O4', 'anion'),
 ('pairs each cation with each anion', 'grid'),
 ('barium swallow X-ray', 'n2f', 'barium sulfate'),
 # ---- polyatomic ----
 ('converted to the <b>nitrite</b> ion', 'ionformula', 'nitrite'),
 ('What is the name of the ion ClO', 'ionname', 'ClO2^-'),
 ('the <b>periodate</b> ion', 'ionformula', 'periodate'),
 ('the <b>sulfite</b> ion', 'ionformula', 'sulfite'),
 ('the <b>hydrogen phosphate</b> ion', 'ionformula', 'hydrogen phosphate'),
 ('arterial blood gas report lists', 'ionname', 'HCO3^-'),
 ('<b>dihydrogen phosphate</b> ion', 'ionformula', 'dihydrogen phosphate'),
 ('has the <b>same charge</b>', 'samecharge'),
 ('the <b>acetate</b> ion', 'ionformula', 'acetate'),
 ('lists the bromine oxyanions', 'tablename'),
 # ---- ionicname ----
 ('What is the name of K<sub>2</sub>S', 'f2n', 'K2S'),
 ('What is the name of AgCl', 'f2n', 'AgCl'),
 ('What is the name of Cu<sub>2</sub>O', 'f2n', 'Cu2O'),
 ('What is the name of Co(NO', 'f2n', 'Co(NO3)2'),
 ('What is the name of Cr<sub>2</sub>(SO', 'f2n', 'Cr2(SO4)3'),
 ('Ferrous sulfate is a common', 'n2f', 'ferrous sulfate'),
 ('older name of CuSO', 'f2n', 'CuSO4'),
 ('<b>mercurous nitrate</b>', 'n2f', 'mercurous nitrate'),
 ('<b>sodium hypochlorite</b>', 'n2f', 'sodium hypochlorite'),
 ('Ammonium nitrate, NH', 'f2n', 'NH4NO3'),
 ('Humidity-indicator cards', 'f2n', 'CoCl2.6H2O'),
 ('Zinc sulfate heptahydrate is sprayed', 'n2f', 'zinc sulfate heptahydrate'),
 ('Which row is named correctly', 'tablerows'),
 ('Calcium supplements and bone mineral', 'f2n', 'Ca3(PO4)2'),
 # ---- molecular ----
 ('What is the name of S<sub>2</sub>Cl', 'f2n', 'S2Cl2'),
 ('<b>sulfur hexafluoride</b>', 'n2f', 'sulfur hexafluoride'),
 ('systematic name of NO?', 'f2n', 'NO'),
 ('includes <b>nitrogen dioxide</b>', 'n2f', 'nitrogen dioxide'),
 ('Which formula and name are matched', 'pairs'),
 ('"calcium difluoride"', 'twonames', 'CaF2', 'SF2'),
 ('What is the name of PBr', 'f2n', 'PBr3'),
 ('What is the name of I<sub>2</sub>O', 'f2n', 'I2O5'),
 ('common name <b>ammonia</b>', 'n2f', 'ammonia'),
 # ---- acids ----
 ('What is the name of HI(aq)', 'f2n', 'HI(aq)'),
 ('What is the name of H<sub>2</sub>S(aq)', 'f2n', 'H2S(aq)'),
 ('Car batteries contain', 'f2n', 'H2SO4'),
 ('What is the name of HBrO', 'f2n', 'HBrO2'),
 ('<b>phosphoric acid</b>', 'n2f', 'phosphoric acid'),
 ('<b>hypochlorous acid</b>, which kills', 'n2f', 'hypochlorous acid'),
 ('What is the name of HIO', 'f2n', 'HIO4'),
 ('<b>acetic acid</b> in water', 'n2f', 'acetic acid'),
 ('Carbon dioxide dissolved in blood', 'f2n', 'H2CO3'),
 ('anions and the acids made from them', 'acidtable'),
 # ---- ADAPT ----
 ('Ammonium hydrogen phosphate, ', 'count', '(NH4)2HPO4', 'H'),
 ('one formula unit of Mg', 'count', 'Mg3(PO4)2', None),
 ('three carbon dioxide molecules', 'count', '3 CO2', 'O'),
 ('Air is about 78%', 'diatomic'),
 ('Which of these compounds is <b>ionic</b>', 'pick', 'ionic'),
 ('Which compound below is <b>molecular</b>', 'pick', 'molecular'),
 ('Potassium hydroxide, ', 'classify', 'KOH'),
 ('<b>strontium and phosphorus</b>', 'n2f', 'strontium phosphide', 'nostem'),
 ('<b>aluminum sulfide</b>', 'n2f', 'aluminum sulfide'),
 ('tin(IV) ions and oxide ions', 'n2f', 'tin(IV) oxide', 'nostem'),
 ('Calcium acetate is given', 'n2f', 'calcium acetate'),
 ('<b>cobalt</b> ion in CoPO', 'charge', 'CoPO4', 'cation'),
 ('<b>ammonium dichromate</b>', 'n2f', 'ammonium dichromate'),
 ('<b>zinc hydroxide</b>', 'n2f', 'zinc hydroxide'),
 ('formula of the <b>phosphate</b> ion', 'ionformula', 'phosphate'),
 ('Dried apricots from the Valley', 'ionname', 'SO3^2-'),
 ('<b>perchlorate</b> ion', 'ionformula', 'perchlorate'),
 ('<b>hydrogen sulfate</b> (bisulfate)', 'ionformula', 'hydrogen sulfate'),
 ('What is the name of the ion Cr', 'ionname', 'Cr2O7^2-'),
 ('<b>peroxide</b> ion', 'ionformula', 'peroxide'),
 ('Zinc oxide, ', 'f2n', 'ZnO'),
 ('What is the name of MgBr', 'f2n', 'MgBr2'),
 ('What is the name of PbO?', 'f2n', 'PbO'),
 ('<b>ferric chloride</b>', 'n2f', 'ferric chloride'),
 ('Copper fungicides', 'f2n', 'Cu(OH)2'),
 ('<b>copper(II) chloride dihydrate</b>', 'n2f', 'copper(II) chloride dihydrate'),
 ('Sodium bicarbonate, ', 'f2n', 'NaHCO3'),
 ('What is the name of SiCl', 'f2n', 'SiCl4'),
 ('Strike-anywhere match heads', 'f2n', 'P4S3'),
 ('<b>sulfur dioxide</b> gas', 'n2f', 'sulfur dioxide'),
 ('<b>nitrous oxide</b> to anxious', 'n2f', 'nitrous oxide'),
 ('"disodium sulfide"', 'twonames', 'Na2S', 'CS2'),
 ('What is the name of BrF', 'f2n', 'BrF5'),
 ('Which name for Cl', 'f2n', 'Cl2O'),
 ('Parietal cells in the stomach', 'f2n', 'HCl(aq)'),
 ('Nitrogen fertilizers are made from', 'f2n', 'HNO3'),
 ('<b>hydrobromic acid</b>', 'n2f', 'hydrobromic acid'),
 ('<b>oxalic acid</b>', 'n2f', 'oxalic acid'),
 ('What is the name of HClO<sub>3</sub>', 'f2n', 'HClO3'),
 ('prefix <b>hydro-</b>', 'hydro'),
]
TYPEWORD = {'ionic': 'Ionic', 'molecular': 'Molecular', 'acid': 'An acid'}
print('Per-item checks (own ion tables and name generators)')
for spec in SPEC:
    q = by(spec[0])
    if not q: continue
    i, kd, cs = q['id'], spec[1], C(q); checked.add(i); stem = txt(q['q'])
    if kd == 'count':
        f, el = spec[2], spec[3]
        ok(re.sub(r'\s', '', f) in re.sub(r'\s', '', stem), '%s formula %s in stem' % (i, f))
        a = atoms(f); n = a[el] if el else sum(a.values())
        ok(cs[0] == str(n) and str(n) not in cs[1:], '%s %s %s atoms = %d; choices %s' % (i, f, el or 'total', n, cs))
    elif kd == 'diatomic':
        def isd(c):
            if c.lower() in {v: k for k, v in ELNAME.items()}: return {v: k for k, v in ELNAME.items()}[c.lower()] in DIATOMIC
            m = re.fullmatch(r'([A-Z][a-z]?)2', c); return bool(m and m.group(1) in DIATOMIC)
        r = [isd(c) for c in cs]; ok(r == [True, False, False, False], '%s diatomic %s %s' % (i, cs, r))
    elif kd == 'pick':
        r = [kind(c) for c in cs]; ok(r[0] == spec[2] and spec[2] not in r[1:], '%s types %s (want %s first only)' % (i, r, spec[2]))
    elif kd == 'classify':
        f = spec[2]; w = TYPEWORD[kind(f)]
        ok(f in stem and cs[0].startswith(w) and not any(c.startswith(w) for c in cs[1:]), '%s %s is %s; c[0] %r' % (i, f, kind(f), cs[0][:30]))
    elif kd in ('n2f',):
        nm = spec[2]; fs = formulas_of(nm)
        if len(spec) < 4: ok(norm(nm) in norm(stem), '%s name %r in stem' % (i, nm))
        ok(bool(fs) and cs[0] in fs and not any(c in fs for c in cs[1:]), '%s %r -> %s; c[0] %s; distractors %s' % (i, nm, sorted(fs), cs[0], cs[1:]))
        if fs and cs[0] in fs:
            for j, c in enumerate(cs[1:], 1):    # distractors that look like formulas must not name the same compound
                if FTOK.match(c) and norm(nm) in names_of(c): err.append('%s c[%d] %s is also %s' % (i, j, c, nm))
    elif kd == 'f2n':
        f = spec[2]; ns = names_of(f)
        ok(f in stem, '%s formula %s in stem' % (i, f))
        ok(bool(ns) and norm(cs[0]) in ns and not any(norm(c) in ns for c in cs[1:]), '%s %s -> %s; c[0] %r; distractors %s' % (i, f, sorted(ns), cs[0], cs[1:]))
        for j, c in enumerate(cs[1:], 1):
            if formulas_of(c) and f in formulas_of(c): err.append('%s c[%d] %r is a name of %s' % (i, j, c, f))
    elif kd == 'charge':
        f, which = spec[2], spec[3]; p = ionic_ok(f)
        z = (p[1] if which == 'cation' else p[4]) if p else None
        got = [num_charge(c) for c in cs]
        ok(z is not None and got[0] == z and z not in got[1:], '%s %s %s charge from balance = %s; choices %s' % (i, f, which, z, got))
    elif kd == 'ionformula':
        k = ION_BY_NAME.get(spec[2]); ok(norm(spec[2]) in norm(stem), '%s ion name in stem' % i)
        ok(k is not None and cs[0] == k and k not in cs[1:], '%s %s = %s; choices %s' % (i, spec[2], k, cs))
    elif kd == 'ionname':
        ns = set(ION.get(spec[2], [])); ok(spec[2] in stem, '%s ion %s in stem' % (i, spec[2]))
        ok(bool(ns) and norm(cs[0]) in ns and not any(norm(c) in ns for c in cs[1:]), '%s %s names %s; choices %s' % (i, spec[2], sorted(ns), cs))
    elif kd == 'samecharge':
        zs = [tuple(ION_BY_NAME[n.strip()] .split('^')[1] for n in c.split(' and ')) for c in cs]
        same = [a == b for a, b in zs]; ok(same == [True, False, False, False], '%s charges %s same %s' % (i, zs, same))
    elif kd == 'grid':
        tb = q['f'][0]; an = [txt(h) for h in tb['head'][1:]]; miss = None
        for row in tb['rows']:
            ca = txt(row[0])
            for a, cell in zip(an, row[1:]):
                cu, zc = ca.split('^')[0], (1 if ca.endswith('+') and not ca[-2].isdigit() else int(ca[-2]))
                au, za = a.split('^')[0], -(1 if not a[-2].isdigit() else int(a[-2]))
                g = gcd(zc, -za); want = part(cu, -za // g) + part(au, zc // g)
                if txt(cell) == '?': miss = want
                else: ok(txt(cell) == want and txt(cell) in IONIC, '%s cell %s + %s = %s' % (i, ca, a, want))
        ok(miss is not None and cs[0] == miss and miss not in cs[1:], '%s missing cell = %s; choices %s' % (i, miss, cs))
    elif kd == 'tablename':
        miss = None
        for f, nm in q['f'][0]['rows']:
            f = txt(f)
            if nm == '?': miss = f
            else: ok(nm in ION.get(f, []), '%s row %s = %s' % (i, f, nm))
        ns = set(ION.get(miss, [])); ok(cs[0] in ns and not any(c in ns for c in cs[1:]), '%s ? = %s names %s; choices %s' % (i, miss, sorted(ns), cs))
    elif kd == 'tablerows':
        good = [lab for lab, f, nm in q['f'][0]['rows'] if norm(nm) in names_of(txt(f))]
        ok(good == [cs[0].split()[-1]] and sorted(c.split()[-1] for c in cs) == sorted(r[0] for r in q['f'][0]['rows']), '%s correct rows %s; c[0] %s' % (i, good, cs[0]))
    elif kd == 'pairs':
        r = [norm(c.split(': ', 1)[1]) in names_of(c.split(': ', 1)[0]) for c in cs]; ok(r == [True, False, False, False], '%s pairs %s' % (i, r))
    elif kd == 'twonames':
        f1, f2 = spec[2], spec[3]
        r = [(norm(c.split(';')[0]) in names_of(f1), norm(c.split(';')[1]) in names_of(f2)) for c in cs]
        ok(r[0] == (True, True) and all(x != (True, True) for x in r[1:]) and f1 in stem and f2 in stem, '%s %s/%s %s' % (i, f1, f2, r))
    elif kd == 'hydro':
        r = [any(n.startswith('hydro') for n in names_of(c)) and kind(c) == 'acid' for c in cs]
        ok(r == [True, False, False, False], '%s hydro- %s %s' % (i, cs, [sorted(names_of(c)) for c in cs]))
    elif kd == 'acidtable':
        miss = None
        for an, f, nm in q['f'][0]['rows']:
            a = txt(an).split(', '); f = txt(f)
            ok(ION.get(a[1], [''])[0] == a[0] and fstat(f).startswith('acid H'), '%s row %s %s %s' % (i, a, f, fstat(f)))
            if nm == '?': miss = f
            else: ok(nm in names_of(f), '%s row %s = %s' % (i, f, nm))
        ns = names_of(miss); ok(cs[0] in ns and not any(c in ns for c in cs[1:]), '%s ? %s = %s; choices %s' % (i, miss, sorted(ns), cs))

# ---------- scope ----------
print('Scope (elements, Roman numerals, ion names, terms)')
TEXT = lambda q: [q['q'], q['h'], q['w']] + q['c'] + q['y'] + [c for f in q.get('f', []) for r in [f.get('head', [])] + f.get('rows', []) for c in r]
OUT_TERMS = r'electronegativ|oxidation (?:state|number)|Lewis|VSEPR|resonance|thio|silicate|arsenate|borate|\bmanganate|cyanate|molar mass|\bmoles?\b|IUPAC|Type III|\bpolar\b'
VNAMES = {v: k for k, v in ELNAME.items()}
ENGLISH = {'write', 'ate', 'state', 'separate', 'hydrate', 'quite', 'site', 'indicate', 'rate', 'create', 'plate', 'opposite', 'white', 'hydroxyapatite'}
for q in ALL:
    i = q['id']; s = ' '.join(TEXT(q))
    for m in re.finditer(OUT_TERMS, txt(s), re.I): err.append('%s out-of-scope term %r' % (i, m.group()))
    for f in [t for x in TEXT(q) for t in formulas_in(x)]:
        bad = [x for x in symbols(f) if x not in ELNAME or (x == 'Mn' and 'MnO4' not in f)]
        if bad: err.append('%s formula %s uses out-of-scope element %s' % (i, f, bad))
    core = ' '.join([q['q'], q['h'], q['w'], q['c'][0], q['y'][0]] + [c for f in q.get('f', []) for r in f.get('rows', []) for c in r])
    for m in re.finditer(r'\b([a-z]+)\((I|II|III|IV|V|VI|VII)\)', txt(s)):
        if m.group(1) not in ELNAME.values() and m.group(1) != 'ammonium': err.append('%s Roman numeral on unknown word %r' % (i, m.group()))
    core_nt = ' '.join([q['q'], q['h'], q['w'], q['c'][0], q['y'][0]])   # tables may show a student's wrong names
    for m in re.finditer(r'\b([a-z]+)\((I|II|III|IV|V|VI|VII)\)', txt(core_nt)):
        n = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}.get(m.group(2))
        if n not in VARCHG.get(m.group(1), set()): err.append('%s %r in question/right answer/explanation is not a variable-charge ion of this course' % (i, m.group()))
    for w in re.findall(r'\b([a-z]+(?:ate|ite))s?\b', txt(core).lower()):
        if w not in ANION_NAMES and w not in ENGLISH and not w.endswith('hydrate') and w not in {'per' + x for x in ANION_NAMES}:
            err.append('%s unknown -ate/-ite word %r in question/right answer/explanation' % (i, w))
    for m in re.finditer(r'\b([a-z]+(?:ous|ic))\b', txt(core).lower()):
        w = m.group(1)
        if w in ('cuprous cupric ferrous ferric cobaltous cobaltic chromous chromic stannous stannic plumbous plumbic mercurous mercuric').split(): continue
        if w.endswith(('ous', 'ic')) and re.search(re.escape(w) + r' acid', txt(core).lower()):
            if w + ' acid' not in {n for ns, _ in ACID.values() for n in ns}: err.append('%s acid name %r not generated' % (i, w + ' acid'))

# ---------- coverage, counts, duplicates ----------
print('Items with a machine check: %d of %d (the rest are conceptual; read by hand)' % (len(checked), len(ALL)))
print('  not machine-checked:', ' '.join(q['id'] for q in ALL if q['id'] not in checked) or '(none)')
for nm, B in (('Try It', TRY), ('ADAPT', HW)):
    print(nm, len(B), dict(collections.Counter(q['t'] for q in B)), 'with figures:', sum(1 for q in B if q.get('f')),
          'd:', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1:', sum(q['k'] for q in B))
if len(HW) != 40: err.append('ADAPT has %d items, not 40' % len(HW))
dup = set(re.sub(r'\s+', ' ', q['q']) for q in TRY) & set(re.sub(r'\s+', ' ', q['q']) for q in HW)
if dup: err.append('same question in both banks: %s' % dup)
print('ERRORS:', err if err else 'none')
