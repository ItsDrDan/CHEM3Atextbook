#!/usr/bin/env python3
"""Builds bank/ch14.json (Chapter 14 Try It items: radioactivity and detection, nuclear decay and equations,
half-life, radiocarbon dating, fission and fusion, radiation in medicine).
Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch14.py bank/ch14.json
Conventions (Chapter 14 text): alpha 4/2 He, beta 0/-1 e, positron 0/+1 e, gamma 0/0 gamma, neutron 1/0 n,
proton 1/1 H; mass numbers and atomic numbers each add up on both sides; electron capture puts 0/-1 e on the left;
penetrating power gamma > beta > alpha, ionizing power alpha > beta > gamma; shields paper / aluminum (lab coat) /
lead or concrete. 1 Ci = 3.7 x 10^10 Bq (exact), 1 Bq = 1 decay/s, 1 Gy = 1 J/kg = 100 rad, 1 Sv = 100 rem.
Half-lives as in the 14.3/14.4 tables (F-18 110 min, Tc-99m 6.0 h, I-123 13 h, Rn-222 3.8 days, I-131 8.0 days,
P-32 14.3 days, Co-60 5.27 years, C-14 5730 years (3 s.f.), H-3 12.3 years, K-40 1.25 x 10^9 years, U-238 4.5 x 10^9
years) plus standard values for a few others (Na-24 15.0 h, Ga-67 3.26 days, Xe-133 5.25 days, Cr-51 27.7 days,
Lu-177 6.65 days, In-111 2.80 days, Ir-192 73.8 days). Whole numbers of half-lives only: n = time / half-life
(exact count), amount = initial x (1/2)^n keeps the initial amount's significant figures; time = n x half-life keeps
the half-life's; ages = n x 5730 years to 3 s.f. Inverse-square law for distance. Round half up, no ties.
Markup: [[Po-210]] nuclide (Z from the periodic table), [[alpha]] [[beta]] [[positron]] [[gamma]] [[n]] [[p]] [[e]]
particles, ' -> ' arrow, {CO2} formula. Nuclear symbols are plain HTML <sup>A</sup><sub>Z</sub>X (no MathJax).
The helpers are imported by tools/gen_adapt_ch14.py. Every number is recomputed independently by
tools/check_bank_ch14.py."""
import json, sys, re, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
M = '&minus;'
B = []
CFG = {'prefix': 'c14-%03d', 'adapt': False}

# ---------------- nuclides ----------------
EL = ('H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr '
      'Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt '
      'Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm').split()
ZOF = {s: i + 1 for i, s in enumerate(EL)}
PART = {'alpha': ('4', 2, 'He'), 'beta': ('0', -1, 'e'), 'e': ('0', -1, 'e'), 'positron': ('0', 1, 'e'),
        'gamma': ('0', 0, '&gamma;'), 'n': ('1', 0, 'n'), 'p': ('1', 1, 'H')}
def ns(A, z, s):
    zs = (M + str(-z)) if z < 0 else ('+%d' % z if s == 'e' and z > 0 else str(z))
    return '<sup>%s</sup><sub>%s</sub>%s' % (A, zs, s)
def NU(tok):
    if tok in PART: return ns(*PART[tok])
    s, a = tok.split('-'); return ns(a, ZOF[s], s)
def F(s): return re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', s)
def X(s):
    s = re.sub(r'\[\[([^\]]+)\]\]', lambda m: NU(m.group(1)), s)
    s = s.replace(' -> ', ' &rarr; ')
    s = re.sub(r'(?<![\w;])-(?=\d)', M, s)
    return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)

# ---------------- numbers ----------------
def num(x, n=3):
    x = D(x); e = x.adjusted()
    m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if abs(m) >= 10:
        e += 1; m = x.scaleb(-e).quantize(D(1).scaleb(-(n - 1)), rounding=ROUND_HALF_UP)
    if -3 <= e <= n - 1:
        s = format(m.scaleb(e).quantize(D(1).scaleb(min(0, e - n + 1))), 'f')
        if e == n - 1 and s.endswith('0'): s += '.'
    else:
        s = '%s &times; 10<sup>%s</sup>' % (m, (M + str(-e)) if e < 0 else str(e))
    return s
def sfs(s):
    s = s.lstrip('-')
    if '.' in s: return len(s.replace('.', '').lstrip('0'))
    return len(s.lstrip('0').rstrip('0'))
def S(v, n, u): return num(v, n) + ' ' + u
def ns_(*a): return min(x if isinstance(x, int) else sfs(x) for x in a)
def left(a, n): return D(a) / (2 ** n)
def AM(a, n, u): return S(left(a, n), sfs(a), u)            # amount after n half-lives
def TM(t, n, u): return S(D(t) * n, sfs(t), u)               # time for n half-lives
def PC(n):
    s = format(D(100) / (2 ** n), 'f')                 # exact percent left
    if '.' in s: s = s.rstrip('0').rstrip('.')
    return s + '%'
def AGE(n): return S(5730 * n, 3, 'years')
def steps(a, n, u=''):
    """halving chain as written: 6.40 -> 3.20 -> 1.60 (each step to the initial amount's s.f.)."""
    out = [a]; v = D(a)
    for _ in range(n):
        v = D(num(v / 2, sfs(a)).rstrip('.')); out.append(num(v, sfs(a)))
    return ' &rarr; '.join(out) + (' ' + u if u else '')

def Q(t_, q, c, y, h, w, d, k=0, f=None):
    y = list(y)
    if CFG['adapt'] and not y[0].startswith('Correct: '): y[0] = 'Correct: ' + y[0]
    it = {"id": CFG['prefix'] % (len(B) + 1), "t": t_, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    if f:
        for fg in f:
            if fg['type'] == 'table':
                fg['head'] = [X(x) for x in fg['head']]; fg['rows'] = [[X(x) for x in r] for r in fg['rows']]
                if fg.get('cap'): fg['cap'] = X(fg['cap'])
        it["f"] = f
    B.append(it)

def dump(out):
    json.dump(B, open(out, 'w'), ensure_ascii=False, indent=1)
    print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')),
          'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))


def build():
    # ======================= ch14-radiation (10) =======================
    T = 'ch14-radiation'
    Q(T, "R&ouml;ntgen's X-rays (1895) came from a glowing vacuum tube. What was new about the rays Henri Becquerel found in 1896?",
      ["They came from a uranium salt by itself, with no tube and no electricity", "They could pass through black paper",
       "They could be seen as a faint glow", "They were stopped completely by paper"],
      ["Becquerel's fogged photographic plate showed that the uranium itself gave off rays: the first sign of radioactivity.",
       "X-rays also pass through paper, wood, and flesh, so that was not what was new.",
       "Becquerel saw no glow; the rays were invisible and showed up only on the developed plate.",
       "The rays passed through the black paper wrapped around Becquerel's plate."],
      "What did Becquerel's experiment not need that R&ouml;ntgen's did?",
      "<b>The uranium gave off rays on its own</b>, with no tube and no electricity.", 2)

    Q(T, "Which pair of elements did Marie and Pierre Curie discover while studying radioactive ores?",
      ["Polonium and radium", "Uranium and thorium", "Radon and plutonium", "Technetium and iodine"],
      ["The Curies found polonium (named for Poland, Marie Curie's home country) and radium, both far more radioactive than uranium.",
       "Uranium was already known; it was the element Becquerel had studied.",
       "Radon was identified by other scientists, and plutonium was first made in 1940.",
       "Technetium was first made artificially in 1937, and iodine was known long before."],
      "One of the two is named for Marie Curie's home country.",
      "Marie Curie received her 1911 Nobel Prize in Chemistry for discovering <b>polonium and radium</b>.", 1)

    Q(T, "Strontium-90 is a radioisotope found in nuclear fallout. How many protons and neutrons are in one strontium-90 nucleus?",
      ["38 protons and 52 neutrons", "52 protons and 38 neutrons", "38 protons and 90 neutrons", "90 protons and 38 neutrons"],
      ["Strontium is element 38, so Z = 38; neutrons = A &minus; Z = 90 &minus; 38 = 52.",
       "This swaps the two counts. The atomic number (38, from the periodic table) is the number of protons.",
       "90 is the mass number, protons + neutrons together; subtract the 38 protons to get the neutrons.",
       "The mass number 90 counts protons and neutrons together; the protons are the atomic number, 38."],
      "Z comes from the periodic table; neutrons = A &minus; Z.",
      "[[Sr-90]]: Z = 38 protons; 90 &minus; 38 = <b>52 neutrons</b>.", 1)

    Q(T, "A vial of a radioactive tracer is labeled with its activity. Which unit could appear on that label?",
      ["Becquerel (Bq), one decay per second", "Gray (Gy), joules absorbed per kilogram", "Sievert (Sv), the biological dose",
       "Rem, the older unit of biological dose"],
      ["Activity tells how many nuclei in the source decay each second; it is measured in becquerels or curies.",
       "The gray measures the energy a person's tissue absorbs, not how fast the source decays.",
       "The sievert describes the dose a person received, adjusted for the kind of radiation.",
       "The rem, like the sievert, describes a person's biological dose, not the source."],
      "Curies and becquerels describe the source; grays and sieverts describe the person.",
      "Activity of a source: <b>becquerels</b> (or curies).", 1)

    Q(T, "A radiation therapy plan prescribes 2 Gy to a tumor in each session. What does a dose in grays describe?",
      ["The energy absorbed per kilogram of tumor tissue (1 Gy = 1 J/kg)", "How many nuclei in the source decay each second",
       "The absorbed dose adjusted for how harmful each kind of radiation is", "How long each treatment session lasts"],
      ["The gray is the SI unit of absorbed dose: 1 Gy = 1 J of radiation energy absorbed per kg of tissue (= 100 rad).",
       "Decays per second is the activity of a source, in becquerels or curies.",
       "That is the equivalent (biological) dose, measured in sieverts or rem.",
       "A gray is an amount of absorbed energy per mass, not a time."],
      "The gray replaced the older unit, the rad.",
      "Absorbed dose: <b>1 Gy = 1 J of energy per kg of tissue</b>.", 2)

    a = '18.0'; v = D(a) / 1000 * D('3.7e10')
    Q(T, "An indium-111 dose has an activity of %s mCi. What is its activity in becquerels? (1 Ci = 3.7 &times; 10<sup>10</sup> Bq, exact)" % a,
      [S(v, 3, 'Bq'), S(D(a) * D('3.7e10'), 3, 'Bq'), S(D(a) / 1000 / D('3.7e10'), 3, 'Bq'), S(D(a) * 1000 * D('3.7e10'), 3, 'Bq')],
      ["%s mCi = %s Ci; &times; 3.7 &times; 10<sup>10</sup> Bq/Ci. The exact definition does not limit the significant figures, so the answer has three, from %s." % (a, num(D(a) / 1000, 3), a),
       "This skips the mCi &rarr; Ci step; 1 Ci = 1000 mCi, so %s mCi is only %s Ci." % (a, num(D(a) / 1000, 3)),
       "This divides by 3.7 &times; 10<sup>10</sup>. Each curie is a huge number of becquerels, so multiply.",
       "This multiplies by 1000 to go from mCi to Ci; a curie is larger than a millicurie, so divide by 1000."],
      "mCi &rarr; Ci (divide by 1000), then Ci &rarr; Bq.",
      "%s mCi &times; (1 Ci / 1000 mCi) &times; (3.7 &times; 10<sup>10</sup> Bq / 1 Ci) = <b>%s</b>." % (a, S(v, 3, 'Bq')), 2, 1)

    a = '0.250'; v = D(a) / 100 * 1000
    Q(T, "A radiation worker's dosimeter report from an older lab lists a dose of %s rem. What is this dose in millisieverts? (1 Sv = 100 rem)" % a,
      [S(v, 3, 'mSv'), S(D(a) * 100, 3, 'mSv'), S(D(a) / 100, 3, 'mSv'), S(D(a) * 1000, 3, 'mSv')],
      ["%s rem &divide; 100 rem/Sv = %s Sv; &times; 1000 mSv/Sv = %s mSv. (1 rem = 10 mSv.)" % (a, num(D(a) / 100, 3), num(v, 3)),
       "This multiplies by 100; a sievert is the larger unit (1 Sv = 100 rem), so rem &rarr; Sv divides by 100.",
       "This stops at sieverts; the question asks for millisieverts (&times; 1000).",
       "This treats rem as if it were sieverts; first divide by 100 to change rem to Sv."],
      "rem &rarr; Sv (divide by 100), then Sv &rarr; mSv (multiply by 1000).",
      "%s rem = %s Sv = <b>%s</b>." % (a, num(D(a) / 100, 3), S(v, 3, 'mSv')), 2, 1)

    Q(T, "How does a Geiger counter detect radiation?",
      ["Radiation ionizes the gas in a sealed tube, and each burst of ions lets a pulse of current flow, counted as a click.",
       "Radiation makes a crystal give off flashes of light, which a light detector counts.",
       "Radiation darkens a strip of photographic film over a month of use.",
       "The counter measures the heat given off by the radioactive sample."],
      ["The Geiger counter counts ion pulses in a gas; it is used to check work areas, hands, and spills.",
       "That is a scintillation counter, the detector inside a gamma camera.",
       "That is a film badge, which records a worker's total dose over time.",
       "The heat from a medical source is far too small to measure; detectors count ions or light."],
      "Radiation is called ionizing for a reason.",
      "A Geiger counter <b>counts the current pulses made when radiation ionizes the gas in its tube</b>.", 2)

    Q(T, "In a scintillation counter, what does the light detector actually count?",
      ["Tiny flashes of light given off when radiation strikes a crystal such as sodium iodide",
       "Pulses of current from ions made in a gas-filled tube", "Dark spots on a developed photographic film",
       "The heat given off by the radioactive sample"],
      ["Scintillation means a flash of light; gamma cameras in nuclear medicine are built around large scintillation crystals.",
       "That is how a Geiger counter works.",
       "That is how a film badge records dose.",
       "The heat from a medical source is far too small to measure; detectors count ions or light."],
      "Scintillation means a flash of light.",
      "A scintillation counter counts <b>flashes of light from a crystal</b>.", 2)

    Q(T, "A dental hygienist wears a dosimeter badge at the collar. What does the badge record?",
      ["The total radiation dose the hygienist receives over weeks or months", "The activity of the X-ray machine in becquerels",
       "Each X-ray image as it is taken, with a click", "Which patients received the most radiation"],
      ["A dosimeter stores the energy from the radiation that reaches it and is read in a lab to report the wearer's total dose.",
       "An X-ray machine has no radioactive source; and the badge records the wearer's dose, not the machine's output.",
       "Clicks are made by a Geiger counter. The badge silently adds up dose over time.",
       "The badge is worn by the hygienist and records only the hygienist's own dose."],
      "The badge goes with the worker, not the patient.",
      "A dosimeter records <b>the wearer's total dose over time</b>, reported in millisieverts.", 1)

    # ======================= ch14-decay (18) =======================
    T = 'ch14-decay'
    Q(T, "Which symbol represents a beta particle?",
      ["[[beta]]", "[[positron]]", "[[alpha]]", "[[gamma]]"],
      ["A beta particle is a high-energy electron made in the nucleus: mass number 0, charge &minus;1.",
       "This is a positron: the same mass as an electron, but a +1 charge.",
       "This is an alpha particle, a helium nucleus with mass number 4 and charge +2.",
       "This is a gamma ray: no mass and no charge."],
      "A beta particle is an electron.",
      "Beta particle = electron = <b>[[beta]]</b>.", 1)

    Q(T, "What happens to the mass number (A) and atomic number (Z) of a nucleus that gives off an alpha particle?",
      ["A decreases by 4, and Z decreases by 2", "A decreases by 2, and Z decreases by 2", "A decreases by 4, and Z decreases by 1",
       "A stays the same, and Z increases by 1"],
      ["The alpha particle [[alpha]] carries away 4 mass units and 2 protons.",
       "An alpha particle has 2 protons <i>and</i> 2 neutrons, so A drops by 4, not 2.",
       "An alpha particle carries 2 protons, so Z drops by 2.",
       "That is beta decay, where a neutron changes into a proton."],
      "An alpha particle is a helium nucleus: 2 protons and 2 neutrons.",
      "Alpha decay: <b>A &minus; 4, Z &minus; 2</b>.", 1)

    Q(T, "Polonium-218, the first decay product of radon-222 in indoor air, is an alpha emitter. What is the missing product? [[Po-218]] -> ? + [[alpha]]",
      ["[[Pb-214]] (lead-214)", "[[Bi-214]] (bismuth-214)", "[[Pb-216]] (lead-216)", "[[Po-214]] (polonium-214)"],
      ["Top: 218 &minus; 4 = 214. Bottom: 84 &minus; 2 = 82. Element 82 is lead.",
       "This lowers Z by only 1. An alpha particle carries 2 protons, so Z goes from 84 to 82.",
       "This lowers A by only 2. An alpha particle has a mass number of 4.",
       "This keeps Z = 84. The atomic number must drop by 2, so the element changes."],
      "Subtract the alpha particle's 4 and 2 from the top and bottom numbers.",
      "A: 218 = ? + 4, so 214. Z: 84 = ? + 2, so 82 (lead): <b>[[Pb-214]]</b>.", 2)

    Q(T, "Yttrium-90, used in tiny beads that treat liver tumors, is a beta emitter. What is the missing product? [[Y-90]] -> ? + [[beta]]",
      ["[[Zr-90]] (zirconium-90)", "[[Sr-90]] (strontium-90)", "[[Y-89]] (yttrium-89)", "[[Zr-89]] (zirconium-89)"],
      ["Top: 90 = ? + 0, so 90. Bottom: 39 = ? + (&minus;1), so 40. Element 40 is zirconium.",
       "This lowers Z by 1. A beta particle counts as &minus;1, so the new atomic number is one <i>higher</i>: 40.",
       "This changes A and keeps the element. In beta decay A stays the same and Z rises by 1.",
       "Z = 40 is right, but A must stay 90: a beta particle has a mass number of 0."],
      "A beta particle is [[beta]]: watch the sign on the bottom.",
      "A: 90. Z: 39 + 1 = 40 (zirconium): <b>[[Zr-90]]</b>. Beta decay moves one place to the right.", 2)

    Q(T, "Sodium-22 is used as a small source to check PET scanners. Identify the missing particle: [[Na-22]] -> [[Ne-22]] + ?",
      ["[[positron]], a positron", "[[beta]], a beta particle", "[[alpha]], an alpha particle", "[[gamma]], a gamma ray"],
      ["Missing A = 22 &minus; 22 = 0; missing Z = 11 &minus; 10 = +1. A = 0 and charge +1 is a positron.",
       "A beta particle (Z = &minus;1) would make the new atomic number one higher (12, magnesium), not lower.",
       "An alpha particle would lower A by 4; here A does not change.",
       "A gamma ray changes neither A nor Z, but here Z drops from 11 to 10."],
      "Subtract: what A and Z must the particle have?",
      "A: 22 = 22 + 0. Z: 11 = 10 + 1. The particle is <b>a positron, [[positron]]</b>.", 2)

    Q(T, "Iodine-123, used for thyroid imaging, decays by electron capture. What is the product? [[I-123]] + [[e]] -> ?",
      ["[[Te-123]] (tellurium-123)", "[[Xe-123]] (xenon-123)", "[[Te-122]] (tellurium-122)", "[[I-123]] (iodine-123, unchanged)"],
      ["The captured electron is on the left: A = 123 + 0 = 123; Z = 53 + (&minus;1) = 52, tellurium.",
       "This raises Z, as if a beta particle were given off. In electron capture the electron is taken in, so Z drops by 1.",
       "The electron has a mass number of 0, so A stays 123.",
       "A proton becomes a neutron, so Z changes and the element changes."],
      "In electron capture the electron is a reactant: add it on the left.",
      "A: 123 + 0 = 123. Z: 53 &minus; 1 = 52 (tellurium): <b>[[Te-123]]</b>.", 3)

    Q(T, "Krypton-81m, a gas used in some lung ventilation images, gives off a gamma ray. What is the missing product? [[Kr-81m]] -> ? + [[gamma]]",
      ["[[Kr-81]] (krypton-81)", "[[Br-81]] (bromine-81)", "[[Rb-81]] (rubidium-81)", "[[Kr-77]] (krypton-77)"],
      ["A gamma ray has A = 0 and Z = 0, so the nucleus keeps A = 81 and Z = 36; it only loses its extra energy.",
       "This lowers Z. Gamma emission does not change the atomic number, so the element stays krypton.",
       "This raises Z. A gamma ray has no charge, so Z stays 36.",
       "This lowers A by 4. A gamma ray has no mass number, so A stays 81."],
      "What are the mass number and charge of a gamma ray?",
      "A and Z stay the same; only the extra energy leaves: <b>[[Kr-81]]</b>.", 2)

    Q(T, "Iodine-123 is made in a cyclotron by hitting tellurium-124 with protons; two neutrons come out. Complete the equation: [[Te-124]] + [[p]] -> ? + 2 [[n]]",
      ["[[I-123]] (iodine-123)", "[[I-124]] (iodine-124)", "[[I-125]] (iodine-125)", "[[Te-123]] (tellurium-123)"],
      ["Left: A = 125, Z = 53. Right: ? + 2 neutrons (2 &times; 1 = 2, Z 0). So A = 123 and Z = 53, iodine.",
       "This counts only one neutron; the coefficient 2 means 2 mass units leave.",
       "This forgets the neutrons on the right; they carry away 2 mass units.",
       "This forgets the proton's charge: Z on the left is 52 + 1 = 53."],
      "Total the left side, then subtract 2 &times; the neutron.",
      "A: 124 + 1 = 125 = ? + 2, so 123. Z: 52 + 1 = 53 = ? + 0, so 53: <b>[[I-123]]</b>.", 3)

    Q(T, "In 1919, Ernest Rutherford made the first artificial transmutation by hitting nitrogen-14 with alpha particles. Complete the equation: [[N-14]] + [[alpha]] -> ? + [[p]]",
      ["[[O-17]] (oxygen-17)", "[[O-18]] (oxygen-18)", "[[F-18]] (fluorine-18)", "[[N-17]] (nitrogen-17)"],
      ["Left: A = 18, Z = 9. Subtract the proton (1, 1): A = 17, Z = 8, oxygen.",
       "This forgets the proton on the right; it carries away 1 mass unit.",
       "This forgets the proton entirely; both its A = 1 and Z = 1 must be subtracted.",
       "This keeps Z = 7. Z on the left is 7 + 2 = 9; subtract the proton's 1 to get 8."],
      "Total A and Z on the left, then subtract the proton.",
      "A: 14 + 4 = 18 = ? + 1, so 17. Z: 7 + 2 = 9 = ? + 1, so 8: <b>[[O-17]]</b>.", 3)

    Q(T, "Chlorine-36 helps date very old groundwater. What kind of decay is this? [[Cl-36]] -> [[Ar-36]] + [[beta]]",
      ["Beta decay", "Positron emission", "Alpha decay", "Electron capture"],
      ["A beta particle is given off: A stays 36, and Z rises from 17 to 18.",
       "Positron emission gives off [[positron]] and lowers Z by 1; here Z rises.",
       "Alpha decay gives off [[alpha]] and lowers A by 4; here A does not change.",
       "In electron capture the electron is on the left as a reactant and Z drops by 1."],
      "Look at which particle is a product and whether Z goes up or down.",
      "The product [[beta]] and Z + 1 with A unchanged: <b>beta decay</b>.", 1)

    Q(T, "Uranium-234 is an alpha emitter found in groundwater in parts of the Central Valley. Which nuclear equation is balanced?",
      ["[[U-234]] -> [[Th-230]] + [[alpha]]", "[[U-234]] -> [[Th-232]] + [[alpha]]", "[[U-234]] -> [[Pa-230]] + [[alpha]]",
       "[[U-234]] -> [[Ra-230]] + [[alpha]]"],
      ["Top: 230 + 4 = 234. Bottom: 90 + 2 = 92. Both totals match.",
       "Top: 232 + 4 = 236, not 234. The alpha particle takes 4 mass units, not 2.",
       "Bottom: 91 + 2 = 93, not 92. Alpha decay lowers Z by 2, not 1.",
       "Bottom: 88 + 2 = 90, not 92. Z must drop by exactly 2."],
      "Add the top numbers and the bottom numbers on the right side of each equation.",
      "Only <b>[[U-234]] &rarr; [[Th-230]] + [[alpha]]</b> balances: 230 + 4 = 234 and 90 + 2 = 92.", 2)

    Q(T, "Radium-224 forms when a parent nucleus gives off an alpha particle. What is the parent? ? -> [[Ra-224]] + [[alpha]]",
      ["[[Th-228]] (thorium-228)", "[[Rn-220]] (radon-220)", "[[Ac-228]] (actinium-228)", "[[Ra-228]] (radium-228)"],
      ["The parent's totals equal the right side: A = 224 + 4 = 228 and Z = 88 + 2 = 90, thorium.",
       "This subtracts the alpha particle instead of adding it; the parent is heavier than its daughter.",
       "This adds only 1 to Z; the alpha particle carries 2 protons, so Z = 90.",
       "This keeps Z = 88; the parent must have 2 more protons than radium."],
      "The parent is on the left: add the right-side numbers.",
      "A: 224 + 4 = 228. Z: 88 + 2 = 90 (thorium): <b>[[Th-228]]</b>.", 3)

    Q(T, "Xenon-133, a gas used in some lung ventilation scans, is a beta emitter. What is the product? [[Xe-133]] -> ? + [[beta]]",
      ["[[Cs-133]] (cesium-133)", "[[I-133]] (iodine-133)", "[[Xe-133]] (xenon-133, unchanged)", "[[Te-129]] (tellurium-129)"],
      ["A stays 133; Z = 54 + 1 = 55, cesium. Beta decay moves one place to the right.",
       "This lowers Z, as in positron emission. A beta particle counts as &minus;1, so the new Z is 55.",
       "In beta decay a neutron becomes a proton, so Z changes and the element changes.",
       "This is alpha decay (A &minus; 4, Z &minus; 2); the particle here is a beta particle."],
      "Beta decay: A the same, Z + 1.",
      "A: 133. Z: 54 + 1 = 55 (cesium): <b>[[Cs-133]]</b>.", 2)

    Q(T, "Which kind of radiation is the <b>most penetrating</b>?",
      ["Gamma rays", "Alpha particles", "Beta particles", "All three penetrate equally"],
      ["Gamma rays have no mass and no charge, so they pass most atoms and go through the body; lead or thick concrete is needed.",
       "Alpha particles are the <i>least</i> penetrating: paper or the outer layer of skin stops them.",
       "Beta particles get through paper but are stopped by aluminum or a lab coat.",
       "They are very different: paper stops alpha, aluminum stops beta, and gamma needs lead."],
      "Which one has no mass and no charge?",
      "Penetrating power: gamma &gt; beta &gt; alpha. <b>Gamma rays</b>.", 1)

    Q(T, "A kind of radiation makes the most ions per centimeter of its path through tissue, but a sheet of paper stops it. Which radiation is it?",
      ["Alpha particles", "Gamma rays", "Beta particles", "X-rays"],
      ["A heavy, slow, doubly charged alpha particle slams into nearly every molecule it meets: the most ionizing and the least penetrating.",
       "Gamma rays are the most penetrating and the <i>least</i> ionizing; paper does not stop them.",
       "Beta particles get through paper and are only medium in ionizing power.",
       "X-rays, like gamma rays, pass through paper and the body."],
      "Penetrating power and ionizing power go in opposite directions.",
      "Most ionizing, stopped by paper: <b>alpha particles</b>.", 2)

    Q(T, "A student places different shields between a sealed radioactive source and a Geiger counter (table). Which kind of radiation does the source give off?",
      ["Beta particles only", "Alpha particles only", "Gamma rays only", "Alpha particles and gamma rays"],
      ["Paper barely changes the count, so there is no alpha; 3 mm of aluminum drops it to the background level (about the same as with lead), so there is no gamma. Beta is stopped by aluminum.",
       "Paper would stop alpha particles, but the count with paper is almost the same as with no shield.",
       "Gamma rays pass through aluminum; this source's count drops to about background with aluminum.",
       "Paper did not lower the count (no alpha), and aluminum stopped nearly everything (no gamma)."],
      "Ask which shield first makes the count drop sharply.",
      "No drop with paper, a drop to background with aluminum: <b>beta particles</b>.", 3, 0,
      [{"type": "table", "cap": "Counts with different shields", "head": ["Shield", "Counts per minute"],
        "rows": [["None", "2,416"], ["Paper", "2,409"], ["Aluminum, 3 mm", "31"], ["Lead, 2 cm", "29"]]}])

    Q(T, "Which statement describes what happens inside the nucleus during <b>positron emission</b>?",
      ["A proton changes into a neutron, so Z decreases by 1 and A stays the same.",
       "A neutron changes into a proton, so Z increases by 1 and A stays the same.",
       "The nucleus captures an inner electron, so A decreases by 1.",
       "The nucleus releases only energy, so A and Z stay the same."],
      ["[[p]] &rarr; [[n]] + [[positron]]: one fewer proton, the same total of protons and neutrons.",
       "That is beta decay, which gives off [[beta]].",
       "Electron capture also lowers Z by 1, but A never changes: the electron's mass number is 0.",
       "That is gamma emission."],
      "A positron carries away a +1 charge.",
      "Positron emission: <b>proton &rarr; neutron + positron; Z &minus; 1, A unchanged</b>.", 2)

    Q(T, "Outside the body, which kind of radiation is the biggest concern for a nuclear medicine technologist, and why?",
      ["Gamma rays, because they pass through the body and reach internal organs",
       "Alpha particles, because they are the most ionizing", "Beta particles, because they are the most penetrating",
       "Alpha particles, because they are the most penetrating"],
      ["From outside, only penetrating radiation reaches living tissue inside; gamma rays do, so lead shields and distance matter.",
       "Alpha particles are the most ionizing, but from outside they cannot get through the dead outer layer of skin. (Inside the body they are the most damaging.)",
       "Beta particles are only medium in penetrating power; a lab coat and gloves stop most of them.",
       "Alpha particles are the least penetrating; paper or skin stops them."],
      "From outside, the radiation must first get through the skin.",
      "Outside the body: <b>gamma rays</b>, the most penetrating.", 2)

    # ======================= ch14-halflife (16) =======================
    T = 'ch14-halflife'
    Q(T, "What is the half-life of a radioisotope?",
      ["The time it takes for half of the radioactive nuclei in a sample to decay", "Half of the time it takes for a sample to decay completely",
       "The time it takes for a sample to lose half of its mass number", "The age at which a radioisotope becomes stable"],
      ["After one half-life, 50% of the radioactive nuclei are left; after another, 25%; and so on.",
       "A sample never decays completely in a set time; each half-life halves what is left.",
       "Mass numbers change only by whole units in each decay; half-life is about how many nuclei have decayed.",
       "Each nucleus decays at a random moment; half-life describes the whole sample, not an age."],
      "Think of 100% &rarr; 50% &rarr; 25%.",
      "Half-life = <b>the time for half of the radioactive nuclei to decay</b>.", 1)

    Q(T, "The half-life of cobalt-60 is known very precisely (5.27 years). Why can no one predict the moment one particular cobalt-60 nucleus will decay?",
      ["Each nucleus decays at a random moment; the half-life describes what a very large number of nuclei do.",
       "Each nucleus decays exactly 5.27 years after it forms, but no one knows when it formed.",
       "A single nucleus decays faster than a large sample does.", "The half-life changes with the temperature of the source."],
      ["Each nucleus has the same chance of decaying in any moment, so the fraction of a huge sample that decays in each half-life is very predictable, even though one nucleus is not.",
       "Nuclei do not carry a timer; half of them decay in the first half-life and half of the rest in the next.",
       "Half-life does not depend on the amount; one nucleus and a large sample follow the same odds.",
       "Temperature does not change half-life."],
      "Is decay a timer or a chance event?",
      "<b>Decay is random for each nucleus</b>; half-life is a property of large numbers of nuclei.", 2)

    Q(T, "What percent of a radioisotope sample remains after 3 half-lives?",
      [PC(3), num(D(100) / 6, 3) + '%', PC(4), '87.5%'],
      ["100% &rarr; 50% &rarr; 25% &rarr; 12.5%: (1/2)<sup>3</sup> = 1/8.",
       "This divides by 2 &times; 3 = 6. Each half-life halves what is left, so divide by 2 three times (by 8).",
       "This halves four times; three half-lives means three arrows, not four numbers.",
       "This is the percent that has <i>decayed</i>; the question asks what remains."],
      "Halve once per half-life.",
      "100 &times; (1/2)<sup>3</sup> = <b>12.5%</b>.", 1, 1)

    a, t, h = '6.40', '45.0', '15.0'; n = 3
    Q(T, "Sodium-24 (half-life %s h) is used to trace leaks in water pipes. A sample contains %s mg of sodium-24. How much remains after %s h?" % (h, a, t),
      [AM(a, n, 'mg'), S(D(a) / (2 * n), 3, 'mg'), S(D(a) * n / 2, 3, 'mg'), AM(a, n + 1, 'mg')],
      ["n = %s h &divide; %s h = %d; %s &times; (1/2)<sup>3</sup>. The count of half-lives is exact, so the answer keeps three significant figures." % (t, h, n, a),
       "This divides by 2 &times; 3 = 6. (1/2)<sup>3</sup> means dividing by 2 three times, which is dividing by 8.",
       "This multiplies by (1/2) &times; 3 instead of raising 1/2 to the third power; the amount must get smaller.",
       "This halves four times. 45.0 h is 3 half-lives: count the arrows, not the amounts."],
      "Find n first: time &divide; half-life.",
      "n = 3: %s = <b>%s</b>." % (steps(a, n, 'mg'), AM(a, n, 'mg')), 2, 1)

    a, t = '9.60', '32'; n = 4
    Q(T, "Iodine-131 (half-life 8.0 days) is used to treat an overactive thyroid. A capsule contains %s mCi of iodine-131. What activity remains after %s days?" % (a, t),
      [AM(a, n, 'mCi'), AM(a, n + 1, 'mCi'), S(D(a) / (2 * n), 3, 'mCi'), S(D(a) * n / 2, 3, 'mCi')],
      ["n = 32 days &divide; 8.0 days = 4; %s &times; (1/2)<sup>4</sup> = %s &divide; 16." % (a, a),
       "This halves five times, counting the starting amount as a half-life. 32 &divide; 8.0 = 4.",
       "This divides by 2 &times; 4 = 8. Four half-lives divide by 2<sup>4</sup> = 16.",
       "This multiplies by (1/2) &times; 4 = 2; after any decay, less must remain."],
      "n = 32 &divide; 8.0. Then halve n times.",
      "n = 4: %s = <b>%s</b>." % (steps(a, n, 'mCi'), AM(a, n, 'mCi')), 2, 1)

    a, t = '2.40', '138.9'; n = 3
    Q(T, "Samarium-153 (half-life 46.3 h) relieves bone pain from cancer that has spread to bone. A dose has an activity of %s GBq. What is its activity %s h later?" % (a, t),
      [AM(a, n, 'GBq'), AM(a, n - 1, 'GBq'), AM(a, n + 1, 'GBq'), S(D(a) / (2 * n), 3, 'GBq')],
      ["n = 138.9 h &divide; 46.3 h = 3; %s &times; 1/8." % a,
       "This halves only twice; 138.9 h is three 46.3-hour half-lives.",
       "This halves four times; count the half-lives (3), not the amounts in the chain.",
       "This divides by 2 &times; 3 = 6 instead of 2<sup>3</sup> = 8."],
      "How many 46.3-hour periods fit in 138.9 h?",
      "n = 3: %s = <b>%s</b>." % (steps(a, n, 'GBq'), AM(a, n, 'GBq')), 2, 1)

    a, b, h = '24.0', '3.00', '14.3'; n = 3
    Q(T, "Phosphorus-32 (half-life %s days) labels DNA in biology research. How long does it take for a %s &mu;Ci sample to decay to %s &mu;Ci?" % (h, a, b),
      [TM(h, n, 'days'), TM(h, n + 1, 'days'), TM(h, 8, 'days'), S(D(h) / n, 3, 'days')],
      ["%s &rarr; 12.0 &rarr; 6.00 &rarr; %s is 3 half-lives; time = 3 &times; %s days, three significant figures from the half-life." % (a, b, h),
       "This counts the four amounts instead of the three arrows between them.",
       "This multiplies by 8, the fraction 1/8 turned upside down. 1/8 = (1/2)<sup>3</sup>, so n = 3.",
       "This divides the half-life by 3; time = n &times; half-life."],
      "Halve %s until you reach %s, and count the steps." % (a, b),
      "3 half-lives &times; %s days = <b>%s</b>." % (h, TM(h, n, 'days')), 2, 1)

    a = '14.0'; n = 3
    Q(T, "A dose of fluorine-18 FDG (half-life 110 min) has an activity of %s mCi when it leaves the cyclotron. What is its activity 5.5 h later?" % a,
      [AM(a, n, 'mCi'), S(D(a) * D(2) ** (D('-5.5') / 110), 3, 'mCi'), AM(a, n + 1, 'mCi'), S(D(a) / (2 * n), 3, 'mCi')],
      ["5.5 h &times; 60 min/h = 330 min; n = 330 min &divide; 110 min = 3; %s &times; 1/8." % a,
       "This divides 5.5 h by 110 min without matching the units, which makes it look as if almost no time has passed.",
       "This halves four times; 330 min is exactly 3 half-lives.",
       "This divides by 2 &times; 3 = 6 instead of 2<sup>3</sup> = 8."],
      "Put the time and the half-life in the same units first.",
      "330 min &divide; 110 min = 3: %s = <b>%s</b>." % (steps(a, n, 'mCi'), AM(a, n, 'mCi')), 3, 1)

    Q(T, "The table shows the mass of an unknown radioisotope in a sample over time. What is its half-life?",
      ["11.5 h", "34.5 h", "23.0 h", "5.75 h"],
      ["The mass halves every 11.5 h: 64.0 &rarr; 32.0 mg from 0 to 11.5 h, and so on.",
       "34.5 h is the total time for three half-lives (64.0 &rarr; 8.00 mg).",
       "At 23.0 h the mass is one-fourth of the start: that is two half-lives.",
       "This is half of the first interval; the mass takes the whole first interval to fall from 64.0 to 32.0 mg."],
      "Find the time when the mass is half of the starting mass.",
      "64.0 mg &rarr; 32.0 mg takes <b>11.5 h</b> (and each later interval of 11.5 h halves it again).", 2, 1,
      [{"type": "table", "cap": "Mass of a radioisotope", "head": ["Time (h)", "Mass (mg)"],
        "rows": [["0", "64.0"], ["11.5", "32.0"], ["23.0", "16.0"], ["34.5", "8.00"]]}])

    a, b, t = '9.60', '1.20', '21.6'; n = 3
    Q(T, "A %s mg sample of a radioisotope decays to %s mg in %s days. What is the half-life?" % (a, b, t),
      [S(D(t) / n, 3, 'days'), t + ' days', S(D(t) / (n + 1), 3, 'days'), S(D(t) / 8, 3, 'days')],
      ["%s &rarr; 4.80 &rarr; 2.40 &rarr; %s mg is 3 half-lives; half-life = %s days &divide; 3." % (a, b, t),
       "This treats the whole time as one half-life; the mass was halved three times.",
       "This divides by 4, the number of amounts in the chain; count the arrows (3).",
       "This divides by 8; 1/8 of the sample is left, which is 3 half-lives, not 8."],
      "Count the halvings, then half-life = time &divide; n.",
      "n = 3: %s &divide; 3 = <b>%s</b>." % (t, S(D(t) / n, 3, 'days')), 2, 1)

    a, t, h = '0.650', '9.78', '3.26'; n = 3
    Q(T, "Gallium-67 (half-life %s days) is used to image infections. A patient's dose is measured %s days after it was made, and %s mCi remains. What was the activity when it was made?" % (h, t, a),
      [S(D(a) * 2 ** n, 3, 'mCi'), S(D(a) * 2 ** (n - 1), 3, 'mCi'), S(D(a) * 2 ** (n + 1), 3, 'mCi'), S(D(a) * n, 3, 'mCi')],
      ["n = %s &divide; %s = 3. Going backward in time, double once per half-life: %s &times; 2<sup>3</sup>." % (t, h, a),
       "This doubles only twice; %s days is 3 half-lives." % t,
       "This doubles four times; n = %s &divide; %s = 3." % (t, h),
       "This multiplies by n = 3. Working backward doubles 3 times, a factor of 8."],
      "Working backward, double once per half-life.",
      "n = 3: %s &times; 8 = <b>%s</b>." % (a, S(D(a) * 8, 3, 'mCi')), 3, 1)

    t = '10.54'; n = 2
    Q(T, "Cobalt-60 (half-life 5.27 years) is used to sterilize medical supplies. What percent of a cobalt-60 source remains after %s years?" % t,
      [PC(n), PC(n - 1), PC(n + 1), '75%'],
      ["n = %s &divide; 5.27 = 2; (1/2)<sup>2</sup> = 1/4 = 25%%." % t,
       "50%% is left after one half-life; %s years is two." % t,
       "This halves three times; %s &divide; 5.27 = 2." % t,
       "75% is the part that has <i>decayed</i>; 25% remains."],
      "Divide the time by the half-life.",
      "n = 2: 100% &rarr; 50% &rarr; <b>25%</b>.", 2, 1)

    Q(T, "Why must a PET center use fluorine-18 FDG within a few hours of making it?",
      ["Its half-life is only 110 min, so most of it decays within a few hours.",
       "Its activity rises over time, so a later dose would be too strong.",
       "Its half-life gets shorter as the sample gets older.",
       "It loses its fluorine atoms to the air, even though its nuclei do not decay."],
      ["After 3 half-lives (330 min, 5.5 h) only 1/8 is left, so doses are made close by and used quickly.",
       "Activity only falls as the nuclei decay.",
       "Half-life is constant for each isotope.",
       "The problem is nuclear decay, not loss of atoms."],
      "Look up fluorine-18 in the half-life table.",
      "Fluorine-18's <b>110 min half-life</b> is short.", 1)

    h = '6.0'; n = 3
    Q(T, "How many hours after a technetium-99m dose is prepared does only 1/8 of its activity remain? (half-life %s h)" % h,
      [TM(h, n, 'h'), TM(h, 8, 'h'), TM(h, n + 1, 'h'), S(D(h) / n, 2, 'h')],
      ["1/8 = (1/2)<sup>3</sup>, so 3 half-lives: 3 &times; 6.0 h = 18 h (two significant figures, from 6.0).",
       "This multiplies by 8; 1/8 means three halvings, so multiply by 3.",
       "This counts four half-lives: 1 &rarr; 1/2 &rarr; 1/4 &rarr; 1/8 has three arrows.",
       "This divides the half-life by 3; time = n &times; half-life."],
      "How many halvings turn 1 into 1/8?",
      "n = 3: 3 &times; 6.0 h = <b>%s</b>." % TM(h, n, 'h'), 2, 1)

    pts = [[i / 2, float(D(80) * D(2) ** (D(-i) / 10))] for i in range(0, 41)]
    pts = [[x, round(y, 2)] for x, y in pts]
    Q(T, "The graph shows the activity of a radioactive sample over time. What is the half-life of this isotope?",
      ["5 h", "10 h", "20 h", "40 h"],
      ["The activity falls from 80 mCi to 40 mCi at 5 h, then to 20 mCi at 10 h: it halves every 5 h.",
       "At 10 h the activity is 20 mCi, one-fourth of the start: that is two half-lives.",
       "20 h is the whole time shown, four half-lives (80 &rarr; 5 mCi).",
       "40 is the activity after one half-life, read from the vertical axis, not a time."],
      "Find the time when the activity is half of its starting value.",
      "80 mCi &rarr; 40 mCi at <b>5 h</b>.", 1, 0,
      [{"type": "plot", "x": {"min": 0, "max": 20, "label": "Time (h)", "ticks": [0, 5, 10, 15, 20]},
        "y": {"min": 0, "max": 80, "label": "Activity (mCi)", "ticks": [0, 10, 20, 40, 60, 80]}, "grid": True,
        "series": [{"pts": pts, "color": "#2f5fa8"}, {"pts": [[0, 80], [5, 40], [10, 20], [15, 10], [20, 5]], "dots": True, "dotsOnly": True, "color": "#2f5fa8"}]}])

    Q(T, "A student says: &ldquo;After two half-lives a 6.0 mg sample is completely gone, because half of it decays each half-life.&rdquo; What is wrong with this reasoning?",
      ["Each half-life halves the amount that is <i>left</i>, so 1.5 mg remains after two half-lives.",
       "Nothing is wrong; 3.0 mg decays in each half-life, so none is left.",
       "The half-life gets shorter as the sample gets smaller, so the sample is gone even sooner.",
       "Half of the sample decays only in the first half-life; after that it stops decaying."],
      ["6.0 &rarr; 3.0 &rarr; 1.5 mg: the second half-life removes half of 3.0 mg, not another 3.0 mg.",
       "This subtracts half of the <i>original</i> amount each time; the amount lost gets smaller each half-life.",
       "Half-life does not depend on the amount; it stays the same.",
       "Decay continues; every half-life halves what is left."],
      "Halve what is left, not the original.",
      "6.0 &rarr; 3.0 &rarr; <b>1.5 mg</b> after two half-lives.", 2)

    # ======================= ch14-dating (10) =======================
    T = 'ch14-dating'
    Q(T, "How is carbon-14 made in the upper atmosphere?",
      ["Neutrons from cosmic rays hit nitrogen-14 nuclei: [[N-14]] + [[n]] -> [[C-14]] + [[p]]",
       "Carbon-12 atoms absorb two neutrons from sunlight: [[C-12]] + 2 [[n]] -> [[C-14]]",
       "Carbon-14 is left over from when Earth formed and has not decayed yet",
       "Plants make carbon-14 during photosynthesis"],
      ["Cosmic rays make neutrons; a neutron knocks a proton out of a nitrogen-14 nucleus, and Z drops from 7 to 6.",
       "This equation balances, but it is not how carbon-14 forms; carbon-14 comes from the nitrogen in the air.",
       "With a half-life of 5730 years, any carbon-14 from Earth's formation (4.5 billion years ago) decayed long ago; it is constantly remade.",
       "Plants take in carbon-14 that is already in the CO<sub>2</sub> of the air; they do not make it."],
      "Most of the atmosphere is nitrogen.",
      "<b>[[N-14]] + [[n]] &rarr; [[C-14]] + [[p]]</b>, driven by cosmic-ray neutrons.", 2)

    Q(T, "Why does the carbon in your own body have about the same carbon-14 to carbon-12 ratio as the CO<sub>2</sub> in the air?",
      ["Your food chain starts with plants that take in CO<sub>2</sub> from the air, and you keep replacing your body's carbon as you eat.",
       "Your lungs absorb carbon-14 from the air and store it in your bones.",
       "Your cells make carbon-14 from the nitrogen you breathe.",
       "Carbon-14 does not decay inside a living body."],
      ["Photosynthesis fixes carbon from the air; you eat plants (or animals that ate plants) and keep rebuilding your molecules, so your ratio matches the living world.",
       "The CO<sub>2</sub> you breathe out is a waste product; your body's carbon comes from food.",
       "Making carbon-14 from nitrogen takes a neutron from cosmic rays, a nuclear reaction that cells cannot do.",
       "Carbon-14 decays all the time; a living body keeps replacing it."],
      "Where does the carbon in your proteins and DNA come from?",
      "<b>Food chains start with photosynthesis</b>, and eating keeps replacing your carbon.", 2)

    Q(T, "An animal dies. What happens to the ratio of carbon-14 to carbon-12 in its bones over the next several thousand years?",
      ["It decreases, because carbon-14 decays and is no longer replaced",
       "It increases, because carbon-14 builds up after death",
       "It stays the same, because the bones keep exchanging carbon with the air",
       "It drops to zero right away, because carbon-14 decays at death"],
      ["After death, carbon intake stops; carbon-14 decays (half-life 5730 years) while carbon-12, which is stable, stays.",
       "Nothing adds carbon-14 to a dead organism; it only decays away.",
       "Exchange stops at death: no more eating or photosynthesis.",
       "It halves only every 5730 years; it does not vanish at once."],
      "After death, is carbon-14 still replaced?",
      "Carbon-14 decays and is not replaced: the ratio <b>decreases</b>.", 1)

    Q(T, "About what fraction of the carbon atoms in the atmosphere's CO<sub>2</sub> are carbon-14?",
      ["About one in a trillion", "About one in two", "About one in a hundred", "None; carbon-14 forms only after an organism dies"],
      ["Only about one carbon atom in a trillion is carbon-14, but that small fraction stays nearly constant because carbon-14 is made about as fast as it decays.",
       "Almost all carbon is stable carbon-12; carbon-14 is a tiny fraction.",
       "Carbon-13, a stable isotope, is about one in a hundred; carbon-14 is far rarer.",
       "Carbon-14 is made all the time in the upper atmosphere by cosmic-ray neutrons."],
      "The amount is tiny but nearly constant.",
      "<b>About one in a trillion</b>.", 2)

    lv, sm = '13.6', '3.40'; n = 2
    Q(T, "Carbon from living plants gives %s decays per minute per gram of carbon. Charcoal from an ancient campfire gives %s decays per minute per gram. Estimate the charcoal's age. (carbon-14 half-life 5730 years)" % (lv, sm),
      [AGE(n), AGE(4), S(D(5730) / 4, 3, 'years'), AGE(n + 1)],
      ["%s &rarr; 6.80 &rarr; %s is 2 half-lives; age = 2 &times; 5730 years = 11,460 years, three significant figures." % (lv, sm),
       "This uses the 4 from the fraction 1/4 as the number of half-lives. 1/4 = (1/2)<sup>2</sup>, so n = 2.",
       "This multiplies the fraction (1/4) by 5730. First find n, then multiply n &times; 5730 years.",
       "This counts the three activities in the chain; count the two halvings."],
      "Turn the activities into a number of halvings, n.",
      "n = 2: age = 2 &times; 5730 = <b>%s</b>." % AGE(n), 2, 1)

    lv, sm = '12.8', '0.200'; n = 6
    Q(T, "On one detector, carbon from living plants gives %s counts per minute per gram of carbon, and carbon from a burned seed at an archaeological site gives %s counts per minute per gram. Estimate the seed's age. (carbon-14 half-life 5730 years)" % (lv, sm),
      [AGE(n), S(D(5730) * 64, 3, 'years'), AGE(n + 1), S(D(5730) / 64, 3, 'years')],
      ["%s &divide; %s = 64 = 2<sup>6</sup>, so 6 half-lives: 6 &times; 5730 years = 34,380 years, three significant figures." % (lv, sm),
       "This multiplies by 64; 1/64 left means 6 halvings, so multiply 5730 years by 6.",
       "This counts 7 half-lives; %s &rarr; 6.40 &rarr; 3.20 &rarr; 1.60 &rarr; 0.800 &rarr; 0.400 &rarr; %s is 6 arrows." % (lv, sm),
       "This multiplies the fraction 1/64 by 5730; multiply the number of half-lives instead."],
      "How many times must %s be halved to reach %s?" % (lv, sm),
      "n = 6: 6 &times; 5730 = <b>%s</b>." % AGE(n), 3, 1)

    Q(T, "A cave painting has black lines drawn with charcoal and red areas painted with red ochre, a mineral (iron oxide). Which part can be dated with carbon-14?",
      ["Only the charcoal lines, because charcoal is once-living wood", "Only the red ochre, because iron oxide holds carbon-14 from the air",
       "Both, because everything in a cave has the same carbon-14 ratio", "Neither, because pigments cannot contain carbon"],
      ["Charcoal is burned wood, so its carbon came from a living tree and its carbon-14 clock started when the tree died.",
       "Iron oxide contains no carbon at all, and it was never alive.",
       "Only once-living material carries a carbon-14 clock; minerals do not.",
       "Charcoal is almost pure carbon; that is why it can be dated."],
      "Radiocarbon dating needs something that was once alive.",
      "Only once-living material can be dated: <b>the charcoal</b>.", 2)

    Q(T, "Why can radiocarbon dating not be used on a bone thought to be about 200,000 years old?",
      ["After about 35 half-lives, far too little carbon-14 is left to measure.",
       "Bones contain no carbon.", "Carbon-14 stops decaying after 50,000 years.",
       "The half-life of carbon-14 is longer than 200,000 years."],
      ["200,000 &divide; 5730 is about 35 half-lives; after even 9 half-lives (about 50,000 years), less than 0.2% is left.",
       "Bone contains collagen, a protein full of carbon; younger bones are dated this way.",
       "Carbon-14 keeps decaying; after 50,000 years so little is left that it cannot be measured reliably.",
       "Carbon-14's half-life is 5730 years, far shorter than 200,000 years."],
      "The method works to about 50,000 years. Why does it stop there?",
      "About 35 half-lives: <b>too little carbon-14 remains to measure</b>.", 2)

    Q(T, "A geologist wants the age of a layer of volcanic rock thought to be about 2 million years old. Which isotope is the best choice?",
      ["Potassium-40 (half-life 1.25 &times; 10<sup>9</sup> years)", "Carbon-14 (half-life 5730 years)",
       "Hydrogen-3, tritium (half-life 12.3 years)", "Iodine-131 (half-life 8.0 days)"],
      ["Potassium-40 decays to argon-40 slowly enough to date volcanic rock, including the layers around ancient human fossils.",
       "Carbon-14 dates only once-living material up to about 50,000 years; rock contains no carbon from a living thing.",
       "Tritium dates water that fell as rain within the last several decades.",
       "Iodine-131 would be gone within months; it is a medical isotope."],
      "The half-life should be long enough for the age being measured.",
      "Volcanic rock, millions of years: <b>potassium-40</b>.", 2)

    h = '12.3'; n = 2
    Q(T, "Tritium (hydrogen-3, half-life %s years) can check the age of a wine. A bottle has 1/4 of the tritium found in wine made this year (assume new wine has always had the same tritium level). About how old is the wine?" % h,
      [TM(h, n, 'years'), TM(h, 4, 'years'), TM(h, 3, 'years'), h + ' years'],
      ["1/4 = (1/2)<sup>2</sup>: 2 half-lives &times; %s years, three significant figures." % h,
       "This uses 4 as the number of half-lives; 1/4 is two halvings.",
       "This counts three half-lives; 1 &rarr; 1/2 &rarr; 1/4 is two.",
       "One half-life leaves 1/2 of the tritium, not 1/4."],
      "Radiocarbon reasoning works for any isotope: find n, then n &times; half-life.",
      "n = 2: 2 &times; %s = <b>%s</b>." % (h, TM(h, n, 'years')), 2, 1)

    # ======================= ch14-fission (8) =======================
    T = 'ch14-fission'
    Q(T, "Complete this fission of uranium-235: [[n]] + [[U-235]] -> [[Ba-144]] + ? + 3 [[n]]",
      ["[[Kr-89]] (krypton-89)", "[[Kr-91]] (krypton-91)", "[[Kr-88]] (krypton-88)", "[[Sr-89]] (strontium-89)"],
      ["Left: A = 1 + 235 = 236, Z = 92. Right so far: A = 144 + 3 = 147, Z = 56. Missing: A = 89, Z = 36, krypton.",
       "This counts the 3 neutrons as 1. The coefficient 3 adds 3 &times; 1 = 3 to the mass numbers.",
       "This forgets the neutron on the left; fission starts when uranium-235 absorbs a neutron, so the left total is 236.",
       "This gets Z wrong: 92 &minus; 56 = 36, krypton, not 38."],
      "Total the left side (do not forget the neutron), then count all 3 neutrons on the right.",
      "A: 236 &minus; 144 &minus; 3 = 89. Z: 92 &minus; 56 = 36: <b>[[Kr-89]]</b>.", 3)

    Q(T, "How many neutrons are released in this fission? [[n]] + [[U-235]] -> [[Xe-140]] + [[Sr-94]] + <i>x</i> [[n]]",
      ["2", "3", "1", "4"],
      ["Z: 54 + 38 = 92, already balanced. A: 236 = 140 + 94 + <i>x</i>, so <i>x</i> = 236 &minus; 234 = 2.",
       "Three is common, but here the two fragments total 234, which leaves only 2 mass units for neutrons.",
       "This leaves out the neutron that started the fission: the left side totals 1 + 235 = 236.",
       "This adds the left-side neutron to the right; the products must total 236, and the fragments already have 234."],
      "Mass numbers: 1 + 235 = 140 + 94 + <i>x</i>.",
      "236 &minus; 234 = <b>2</b> neutrons.", 2)

    Q(T, "What makes a fission <b>chain reaction</b> possible?",
      ["Each fission releases 2 or 3 neutrons, which can cause more fissions.",
       "Each fission releases a gamma ray, which splits the next nucleus.",
       "Each fission joins two light nuclei, which then split again.",
       "The control rods give off neutrons that keep the reaction going."],
      ["One neutron starts each fission and 2&ndash;3 come out, so the number of fissions can multiply: 1, 3, 9, 27, &hellip;",
       "Gamma rays come out, but it is the neutrons that are absorbed and split uranium-235.",
       "Joining light nuclei is fusion, the opposite process.",
       "Control rods <i>absorb</i> neutrons to slow the chain reaction."],
      "What particle starts a fission, and how many come out?",
      "<b>Each fission releases more neutrons than it uses</b>.", 1)

    Q(T, "What is the <b>critical mass</b> of a fissionable material?",
      ["The smallest amount that can keep a chain reaction going", "The mass of fuel used up by a reactor in one year",
       "The mass lost and turned into energy in one fission", "The largest amount that can be stored safely in one place"],
      ["Below the critical mass, too many neutrons escape through the surface before hitting another nucleus, and the chain dies out.",
       "This is not what critical mass describes; it is about whether a chain reaction can sustain itself.",
       "The mass turned into energy (E = mc<sup>2</sup>) is tiny; critical mass is an amount of fuel.",
       "The idea is the opposite: critical mass is the minimum amount for a self-sustaining chain reaction."],
      "Think about neutrons escaping from a small piece.",
      "Critical mass = <b>the least fuel that keeps a chain reaction going</b>.", 2)

    Q(T, "Which material are a reactor's <b>control rods</b> made of, and why?",
      ["Boron or cadmium, which absorb neutrons", "Uranium oxide, which supplies the fuel",
       "Water, which slows the neutrons down", "Lead, which stops gamma rays"],
      ["Lowering the rods into the core absorbs neutrons and slows or stops the chain reaction; raising them speeds it up.",
       "Uranium oxide pellets fill the fuel rods; control rods are not fuel.",
       "Water is the moderator and coolant; it slows neutrons rather than absorbing them.",
       "Lead shields gamma rays; control rods must absorb neutrons."],
      "The rods control the number of neutrons.",
      "Control rods: <b>boron or cadmium, neutron absorbers</b>.", 2)

    Q(T, "Why must spent fuel rods from a nuclear plant be stored for a very long time?",
      ["They contain fission products, such as strontium-90 and cesium-137, and plutonium that stay radioactive for a long time.",
       "They contain carbon dioxide from burning uranium.", "The uranium in them is still in a chain reaction.",
       "They give off fusion products that are toxic."],
      ["Spent fuel is cooled for years in pools of water and then stored in steel-and-concrete dry casks; some of it stays dangerous for thousands of years.",
       "Fission burns nothing and makes no carbon dioxide.",
       "Once removed from the reactor, the fuel no longer sustains a chain reaction; the problem is its radioactive products.",
       "A fission reactor makes fission products, not fusion products."],
      "What is left after a uranium nucleus splits?",
      "Long-lived <b>radioactive fission products</b> (and plutonium).", 2)

    Q(T, "Per gram of fuel, how does the energy released by fusion compare with the energy released by fission?",
      ["Fusion releases even more energy than fission", "Fusion releases less energy than fission",
       "Fusion and fission release the same energy", "Fusion absorbs energy instead of releasing it"],
      ["Both turn a little mass into energy (E = mc<sup>2</sup>), and per gram of fuel fusion releases even more; that is why fusion power is a research goal.",
       "This is backward; joining light nuclei releases more energy per gram than splitting heavy ones.",
       "The amounts differ; fusion gives more per gram of fuel.",
       "Fusion powers the Sun, so it releases a great deal of energy."],
      "What powers the Sun, and how much fuel does it use?",
      "<b>Fusion releases even more energy per gram</b>.", 2)

    Q(T, "Classify this reaction, which fusion researchers study: [[H-2]] + [[He-3]] -> [[He-4]] + [[p]]",
      ["Fusion", "Fission", "Alpha decay", "Electron capture"],
      ["Two light nuclei join to form a heavier helium-4 nucleus. It balances: 2 + 3 = 4 + 1 and 1 + 2 = 2 + 1.",
       "Fission splits one heavy nucleus after it absorbs a neutron; here two light nuclei join.",
       "Alpha decay starts from one unstable nucleus; here two nuclei collide and join.",
       "Electron capture has an electron as a reactant; there is none here."],
      "Are light nuclei joining, or a heavy nucleus splitting?",
      "Two light nuclei join: <b>fusion</b>.", 2)

    # ======================= ch14-medicine (10) =======================
    T = 'ch14-medicine'
    Q(T, "How does ionizing radiation most often damage DNA inside a cell?",
      ["It ionizes water, making free radicals such as &middot;OH that break bonds in DNA.",
       "It makes the cell radioactive, so the cell decays.", "It heats the cell until its DNA melts.",
       "It changes the carbon atoms in DNA into nitrogen atoms."],
      ["Most of a cell is water; H<sub>2</sub>O<sup>+</sup> breaks into very reactive free radicals that attack DNA, proteins, and membranes.",
       "Gamma rays and X-rays deposit energy without changing nuclei, so the cell does not become radioactive.",
       "Medical doses deposit far too little heat to matter; the damage is chemical, from ions and radicals.",
       "Ionizing radiation removes electrons; it does not change nuclei in the cell."],
      "What molecule is most common in a cell?",
      "<b>Ionized water makes free radicals that break DNA</b>.", 2)

    Q(T, "Why can radiation be used to treat cancer?",
      ["Cancer cells divide rapidly, so their damaged DNA is copied before it can be repaired.",
       "Radiation makes cancer cells radioactive, so they decay away.",
       "Only cancer cells absorb radiation; healthy cells let it pass through.",
       "Radiation heats a tumor until it melts."],
      ["Rapidly dividing cells are the most sensitive to radiation, and cancer cells divide rapidly; beams are aimed so they overlap at the tumor to spare healthy tissue.",
       "Gamma rays and X-rays change no nuclei, so the cells do not become radioactive.",
       "Healthy cells are damaged too, which is why beams are aimed carefully from several directions.",
       "The damage is chemical (ions and free radicals breaking DNA), not heat."],
      "Which cells are most sensitive to radiation?",
      "<b>Cancer cells divide rapidly</b>, so radiation damage hits them hardest.", 2)

    Q(T, "Radon-222 seeps from the soil into a home's basement. In which part of the body does it do most of its damage, and why?",
      ["The lungs: inhaled radon and its decay products give off alpha particles right next to living lung cells.",
       "The skin: its alpha particles are stopped there.", "The bones: radon is taken up like calcium.",
       "Every organ equally: radon gives off mostly gamma rays."],
      ["Radon is a gas, so it is breathed in; it and its solid decay products lodge in the lungs, where the highly ionizing alpha particles damage lung tissue.",
       "The outer layer of skin is dead cells, which is why alpha particles from outside do little harm.",
       "Radon is a noble gas; it is breathed in and out and does not build bone.",
       "Radon-222 is an alpha emitter."],
      "How does a gas get into the body?",
      "<b>The lungs</b>: alpha particles are delivered right to lung cells.", 2)

    r, d1, d2 = '48', '1.0', '4.0'; v = D(r) * (D(d1) / D(d2)) ** 2
    Q(T, "A patient who just received a tracer gives a dose rate of %s &mu;Sv/h at 1.0 m. A technologist steps back to 4.0 m. What dose rate does she receive there?" % r,
      [S(v, 2, '&mu;Sv/h'), S(D(r) / 4, 2, '&mu;Sv/h'), S(D(r) / 8, 2, '&mu;Sv/h'), S(D(r) / 2, 2, '&mu;Sv/h')],
      ["Inverse-square law: four times the distance gives (1/4)<sup>2</sup> = 1/16 of the dose rate: %s &divide; 16." % r,
       "This divides by 4; the dose rate falls with the <i>square</i> of the distance.",
       "This divides by 2 &times; 4 = 8; four times the distance divides the dose rate by 4<sup>2</sup> = 16.",
       "This halves it; four times the distance cuts it to one-sixteenth."],
      "Dose rate &prop; 1/distance<sup>2</sup>.",
      "%s &times; (1.0/4.0)<sup>2</sup> = %s &divide; 16 = <b>%s</b>." % (r, r, S(v, 2, '&mu;Sv/h')), 2, 1)

    Q(T, "A nuclear medicine technologist steps back from a patient, works faster, and draws up doses behind a lead-glass shield. What principle is she following?",
      ["ALARA: keep doses as low as reasonably achievable with time, distance, and shielding",
       "Critical mass: keep the amount of tracer below the critical mass",
       "Half-life: wait 10 half-lives before going near any patient",
       "Inverse ionization: stand closer so the radiation spreads out"],
      ["Less time, more distance, and a shield matched to the radiation are the three tools for lowering dose.",
       "Critical mass is about chain reactions in fission fuel, not tracers.",
       "Waiting 10 half-lives is used for stored waste; patient care cannot wait days.",
       "Standing closer <i>raises</i> the dose rate; distance lowers it."],
      "Three tools: time, distance, shielding.",
      "<b>ALARA</b>, using time, distance, and shielding.", 1)

    Q(T, "Why is fluorine-18 FDG useful in PET scans?",
      ["Cells take it up like glucose, and each positron it gives off makes two gamma rays that the scanner detects.",
       "Its alpha particles leave the body and are detected by the scanner.",
       "It has a half-life of several years, so one dose can be used for many scans.",
       "It gives off X-rays from its nucleus."],
      ["The positron meets an electron and the two annihilate into two gamma rays flying in opposite directions; the ring of detectors finds where they came from. Active tissue, such as a tumor, takes up more FDG.",
       "Alpha particles cannot leave the body; fluorine-18 is a positron emitter.",
       "Its half-life is 110 minutes, so it must be used within hours of being made.",
       "X-rays are made outside the nucleus; fluorine-18's nucleus gives off positrons."],
      "FDG is a glucose look-alike, and fluorine-18 is a positron emitter.",
      "<b>Taken up like glucose; positron &rarr; two gamma rays</b>.", 2)

    Q(T, "Mateo Herrera's V/Q lung scan uses technetium-99m. Which pair of properties makes technetium-99m a good imaging tracer?",
      ["It gives off gamma rays that leave the body, and its half-life is only 6.0 h.",
       "It gives off alpha particles that make sharp images, and its half-life is 6.0 days.",
       "It gives off beta particles that stay in the lungs, and its half-life is many years.",
       "It is not radioactive, so it is completely safe."],
      ["Gamma rays reach the camera outside the body, and the short half-life means the activity is gone soon after the scan.",
       "Alpha particles would be stopped inside the body and would make no image, and the half-life is 6.0 h, not days.",
       "Beta particles add dose without making an image, and a long half-life would keep him radioactive.",
       "The tracer must be radioactive to be seen by the gamma camera."],
      "Imaging needs radiation that escapes the body, and a short half-life.",
      "<b>Gamma rays out of the body, and a 6.0 h half-life</b>.", 1)

    Q(T, "Why is iodine-131 used to treat an overactive thyroid (Graves' disease)?",
      ["The thyroid collects iodide to make its hormones, so iodine-131 concentrates there and its beta particles destroy nearby thyroid tissue.",
       "Iodine-131 gives off only gamma rays, which are absorbed only by the thyroid.",
       "Iodine-131 is an alpha emitter that travels through the whole body.",
       "Iodine-131 has a half-life of a few seconds, so it acts instantly."],
      ["The thyroid cannot tell iodine-131 from stable iodine; its short-range beta particles (under about 2 mm in tissue) deliver dose locally.",
       "Iodine-131 gives off beta particles and gamma rays; the beta particles do the treating, and gamma rays pass out of the body.",
       "Iodine-131 is a beta emitter, and it collects in the thyroid rather than spreading through the body.",
       "Its half-life is 8.0 days."],
      "Which gland uses iodine?",
      "<b>The thyroid concentrates iodine-131, and its beta particles act locally</b>.", 2)

    Q(T, "Why are boxed, sealed surgical gloves sterilized with gamma rays rather than beta particles?",
      ["Gamma rays penetrate the sealed boxes; beta particles would be stopped near the surface.",
       "Beta particles would make the gloves radioactive.", "Gamma rays are more ionizing than beta particles.",
       "Beta particles cannot damage bacterial DNA."],
      ["Gamma rays are the most penetrating radiation, so whole boxes can be sterilized after packaging; neither kind makes the gloves radioactive.",
       "Neither beta particles nor gamma rays change the nuclei in the gloves.",
       "Gamma rays are the <i>least</i> ionizing; they are chosen for penetration.",
       "Beta particles are ionizing too; they just cannot reach the inside of the box."],
      "Which property matters for a sealed, boxed product?",
      "<b>Gamma rays penetrate the packaging</b>.", 2)

    Q(T, "How do X-rays differ from gamma rays?",
      ["X-rays are made outside the nucleus, in an X-ray tube that can be switched off; gamma rays come from nuclei during decay.",
       "X-rays come from radioactive nuclei; gamma rays come from machines.",
       "X-rays are particles with mass; gamma rays are light.", "X-rays are not ionizing; gamma rays are."],
      ["Both are high-energy electromagnetic radiation; the difference is the source. A radioisotope cannot be switched off.",
       "This reverses them: X-rays come from fast electrons hitting a metal target in a tube.",
       "Both X-rays and gamma rays are electromagnetic radiation, with no mass.",
       "Both are ionizing, which is why X-ray exposures are justified and kept small (ALARA)."],
      "Where does each kind of radiation come from?",
      "<b>X-rays from a tube (outside the nucleus); gamma rays from decaying nuclei</b>.", 2)


    # ======================= ch14-health (added 2026-11-15 when 14.6 was split) =======================
    T = 'ch14-health'
    Q(T, "For most people in the United States, which source gives the largest share of natural background radiation?",
      ["Radon gas from uranium in rocks and soil, breathed into the lungs",
       "Nuclear power plants", "Cosmic rays from space", "Potassium-40 in food"],
      ["Radon-222 forms from the decay of uranium-238 underground, seeps into buildings, and is the largest natural source of exposure.",
       "Nuclear power plants add only a tiny amount to the dose of people living nearby.",
       "Cosmic rays add to background radiation, more at high altitude and on flights, but they are not the largest natural source.",
       "Potassium-40 in food and in the body contributes, but less than radon."],
      "Which natural source is a gas that collects indoors?",
      "<b>Radon</b> is the largest natural source of background radiation.", 1)

    r, d1, d2 = '54', '2.0', '6.0'; v = D(r) * (D(d1) / D(d2)) ** 2
    Q(T, "During a bone scan, a technologist stands 2.0 m from the patient, where the dose rate is %s &mu;Sv/h. If she moves to 6.0 m, what dose rate does she receive?" % r,
      [S(v, 2, '&mu;Sv/h'), S(D(r) / 3, 2, '&mu;Sv/h'), S(D(r) / 2, 2, '&mu;Sv/h'), S(D(r) / 6, 2, '&mu;Sv/h')],
      ["Three times the distance gives (1/3)<sup>2</sup> = 1/9 of the dose rate: %s &divide; 9." % r,
       "This divides by 3; the dose rate falls with the <i>square</i> of the distance.",
       "This halves it; tripling the distance cuts the dose rate to one-ninth.",
       "This divides by 6, the new distance; use the ratio of the distances, squared."],
      "Dose rate &prop; 1/distance<sup>2</sup>; how many times farther is 6.0 m than 2.0 m?",
      "%s &times; (2.0/6.0)<sup>2</sup> = %s &divide; 9 = <b>%s</b>." % (r, r, S(v, 2, '&mu;Sv/h')), 2, 1)

    Q(T, "Which tissue is most sensitive to radiation damage?",
      ["Bone marrow, because its cells divide rapidly to make blood cells",
       "Adult nerve cells in the brain", "Adult muscle", "Tooth enamel"],
      ["Rapidly dividing cells are the most sensitive, because damaged DNA is copied before it can be repaired; bone marrow makes new blood cells constantly.",
       "Adult nerve cells rarely divide, so they are among the least sensitive.",
       "Adult muscle cells divide slowly, so they are less sensitive.",
       "Enamel is mostly mineral with no living, dividing cells."],
      "Which cells are most sensitive: rapidly dividing ones or slowly dividing ones?",
      "<b>Bone marrow</b>: its rapidly dividing cells are the most sensitive.", 1)

    RETOPIC = {'c14-063': 'ch14-health', 'c14-065': 'ch14-health', 'c14-066': 'ch14-health', 'c14-067': 'ch14-health'}
    for it in B:
        if it['id'] in RETOPIC and not CFG['adapt']: it['t'] = RETOPIC[it['id']]

if __name__ == '__main__':
    build()
    dump(sys.argv[1])
