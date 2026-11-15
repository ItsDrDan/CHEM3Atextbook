#!/usr/bin/env python3
"""Builds bank/ch09.json (Chapter 9 Try It items: energy, temperature scales, heat units and heat flow, specific
heat and calorimetry, phase changes and heating curves, intermolecular forces, liquids and solids, vapor pressure
and ranking). Scratch generator; the JSON file is the deliverable.
usage: python3 tools/gen_bank_ch09.py bank/ch09.json
Conventions (Chapter 9 text): K = C + 273.15; C = (F - 32)/1.8; F = 1.8(C) + 32 (32, 1.8, 273.15 exact; the
addition rule keeps the measurement's decimal places, the multiplication rule its significant figures; values are
chosen so that every reasonable reading of the rules gives the same answer). 1 cal = 4.184 J, 1 Cal = 4184 J
(exact). q = mc(dT), dT = Tf - Ti. Specific heats J/(g.C): water 4.184, ice 2.09, steam 2.01, ethanol 2.42,
Al 0.903, Fe 0.449, Cu 0.385, Ag 0.235, Au 0.128, Pb 0.128. Water dHfus 6.02 kJ/mol (334 J/g), dHvap 40.7 kJ/mol;
H2O 18.015 g/mol (yellow sheet). Multi-step heats: each step rounded to its significant figures in kJ, then added
by the decimal-place rule (as in Section 9.5). Markup: {CH3OH} formula.
Every number is recomputed independently by tools/check_bank_ch09.py."""
import json, sys, re, os, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
MS = json.load(open(os.path.join(HERE, 'yellow_sheet_masses.json')))['masses']
M = '&minus;'
B = []
PREFIX = 'c9-%03d'

# ---------------- formulas ----------------
def F(s):
    ch = ''
    if '^' in s: s, ch = s.split('^')
    out = re.sub(r'(?<=[A-Za-z\)])(\d+)', r'<sub>\1</sub>', s)
    if ch: out += '<sup>' + ch.replace('-', M) + '</sup>'
    return out
def X(s):
    s = re.sub(r'(?<![\w;])-(?=\d)', M, s)
    return re.sub(r'\{([^{}]+)\}', lambda m: F(m.group(1)), s)
def parse(f):
    tot = collections.Counter(); stack = [collections.Counter()]; i = 0
    while i < len(f):
        if f[i] == '(':
            stack.append(collections.Counter()); i += 1
        elif f[i] == ')':
            j = i + 1
            while j < len(f) and f[j].isdigit(): j += 1
            n = int(f[i + 1:j] or 1); g = stack.pop()
            for k, v in g.items(): stack[-1][k] += v * n
            i = j
        else:
            m = re.match(r'([A-Z][a-z]?)(\d*)', f[i:]); stack[-1][m.group(1)] += int(m.group(2) or 1); i += m.end()
    return stack[0]
def dp(s): return len(s.split('.')[1]) if '.' in s else 0
def mm(f):
    q = min(dp(MS[e]) for e in parse(f))
    return sum(D(MS[e]) * n for e, n in parse(f).items()).quantize(D(1).scaleb(-q), rounding=ROUND_HALF_UP)
MW = mm('H2O')   # 18.015

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
def sg(x, n=3):
    """signed: + for positive."""
    s = num(x, n); return s if s.startswith('-') else '+' + s
def rnd(x, n=3):
    x = D(x); return x.quantize(D(1).scaleb(x.adjusted() - n + 1), rounding=ROUND_HALF_UP)
def sfs(s):
    s = s.lstrip('-')
    if '.' in s: return len(s.replace('.', '').lstrip('0'))
    return len(s.lstrip('0').rstrip('0'))
def qd(x, d):
    return format(D(x).quantize(D(1).scaleb(-d), rounding=ROUND_HALF_UP), 'f')
def ndp(x):
    e = D(x).as_tuple().exponent; return -e if e < 0 else 0
def sub(a, b):
    """a - b as strings, decimal-place rule; returns string."""
    return format((D(a) - D(b)).quantize(D(1).scaleb(-min(dp(a), dp(b)))), 'f')
def add_k(*vals):
    """sum of already-rounded Decimals by the decimal-place rule."""
    q = min(ndp(v) for v in vals); return sum(vals).quantize(D(1).scaleb(-q), rounding=ROUND_HALF_UP)
# temperature conversions (strings in, display strings out)
def c2k(C): return qd(D(C) + D('273.15'), dp(C))
def k2c(K): return qd(D(K) - D('273.15'), dp(K))
def f2c(Fv):
    d = qd(D(Fv) - 32, dp(Fv)); return num(D(d) / D('1.8'), sfs(d))
def c2f(C):
    p = rnd(D('1.8') * D(C), sfs(C)); return qd(p + 32, ndp(p))
def t(s): return s.replace('-', M)   # display a given that may be negative
CW, CICE, CSTEAM, CETH = D('4.184'), D('2.09'), D('2.01'), D('2.42')
CAL, CFE, CCU, CAG, CAU, CPB = D('0.903'), D('0.449'), D('0.385'), D('0.235'), D('0.128'), D('0.128')
HFUS, HVAP = D('6.02'), D('40.7')
UC = 'J/(g·°C)'

def Q(t_, q, c, y, h, w, d, k=0, f=None):
    it = {"id": PREFIX % (len(B) + 1), "t": t_, "q": X(q), "c": [X(x) for x in c], "y": [X(x) for x in y],
          "h": X(h), "w": X(w), "d": d, "k": k}
    assert len(set(it['c'])) == 4, it['c']
    if f:
        for fg in f:
            if fg['type'] == 'table':
                fg['head'] = [X(x) for x in fg['head']]; fg['rows'] = [[X(x) for x in r] for r in fg['rows']]
                if fg.get('cap'): fg['cap'] = X(fg['cap'])
        it["f"] = f
    B.append(it)

# ======================= ch09-energy (7) =======================
T = 'ch09-energy'
Q(T, "Which of these is mainly <b>kinetic</b> energy?",
  ["Blood flowing through an artery", "Glycogen stored in a liver cell", "A fully charged defibrillator battery",
   "Water held in Millerton Lake behind Friant Dam"],
  ["Kinetic energy is energy of motion, and flowing blood is moving.",
   "Glycogen stores chemical potential energy in the arrangement of its atoms; it is released only when the body breaks it down.",
   "A charged battery stores chemical potential energy until it is used.",
   "Water held behind a dam has potential energy of position; it gains kinetic energy only when it is released and falls."],
  "Ask: is it moving right now?",
  "Kinetic energy is energy of motion: <b>flowing blood</b>. The other three are stored (potential) energy.", 1)

Q(T, "An IV bag of dextrose (glucose) solution supplies energy to a patient. Before cells use the glucose, what kind of energy does it hold?",
  ["Chemical potential energy, stored in the arrangement of its atoms and bonds",
   "Kinetic energy, because glucose molecules are always moving",
   "Heat, because the bag is at room temperature",
   "No energy until it reacts; the reaction creates the energy"],
  ["Food molecules such as glucose store chemical potential energy, released during cellular respiration.",
   "The molecules do move, but that thermal motion is not the energy the body gets from glucose; the usable energy is stored in its bonds.",
   "Heat is energy that flows because of a temperature difference. The bag is at the same temperature as the room, so no heat is flowing.",
   "Energy cannot be created. A reaction only releases energy that was already stored as chemical potential energy."],
  "Is the energy moving, or stored until something happens?",
  "Glucose holds <b>chemical potential energy</b>; respiration in cells releases it.", 1)

Q(T, "An air-activated hand warmer gets hot as iron powder inside reacts with oxygen. Which statement agrees with the law of conservation of energy?",
  ["Chemical potential energy of the reactants becomes heat; the total energy stays the same.",
   "The reaction creates new energy, which is why the packet gets hot.",
   "When the packet cools, its energy is destroyed.",
   "The heat comes from the air, which loses all of its energy to the packet."],
  ["Energy changes form. The stored chemical energy of iron and oxygen is released as heat that spreads into your hands and the air.",
   "Energy is never created; the heat was stored as chemical potential energy in the reactants.",
   "Energy is not destroyed when the packet cools; the heat moves into the surroundings and spreads out.",
   "The air supplies oxygen, a reactant, but the heat comes from the reaction's stored chemical energy, not from the air's energy."],
  "Energy can change form or move. Can it be made or destroyed?",
  "The <b>chemical potential energy becomes heat</b>; total energy is conserved.", 2)

Q(T, "A cyclist eats a banana, then rides to the top of a hill and stops. Which sequence best describes the main energy changes?",
  ["Chemical potential energy (food) &rarr; kinetic energy of motion &rarr; potential energy of position at the top, plus heat",
   "Kinetic energy (food) &rarr; chemical potential energy &rarr; kinetic energy at the top",
   "Chemical potential energy (food) is used up and disappears as the cyclist climbs",
   "Potential energy of position &rarr; chemical potential energy &rarr; heat"],
  ["Cells release the food's chemical energy, the muscles turn it into motion, and lifting the body uphill stores energy of position. Much of the energy also becomes body heat.",
   "Food holds stored (potential) energy, not kinetic energy, and the cyclist is stopped at the top.",
   "Energy is not used up; it changes form into motion, energy of position, and heat.",
   "The energy starts as chemical energy in the food, not as energy of position."],
  "Start with the banana: is its energy stored or moving?",
  "<b>Chemical PE &rarr; kinetic energy &rarr; PE of position (+ heat)</b>. The total is conserved at every step.", 2)

Q(T, "One basin of water is at 15.0 °C and another is at 45.0 °C. Which statement is true?",
  ["The water molecules at 45.0 °C have the higher average kinetic energy.",
   "The water molecules at 15.0 °C have the higher average kinetic energy.",
   "Both have the same average kinetic energy, because both are water.",
   "The molecules at 45.0 °C are larger, so they hold more energy."],
  ["Temperature measures the average kinetic energy of the particles, so the warmer water has faster-moving molecules on average.",
   "A lower temperature means slower molecules on average, not faster ones.",
   "The kind of substance does not set the average kinetic energy; the temperature does.",
   "Molecules do not grow when warmed; they move faster."],
  "What does temperature measure on the particle level?",
  "Higher temperature = higher average kinetic energy: <b>the 45.0 °C water</b>.", 1)

Q(T, "Ice melts at 0 °C. While it melts, the temperature stays at 0 °C even though heat keeps flowing in. What happens to the energy of the water molecules?",
  ["Their potential energy rises as they move apart; their average kinetic energy stays the same.",
   "Their average kinetic energy rises, so they move faster.",
   "Their potential energy falls as they move closer together.",
   "The heat is destroyed, which is why the temperature does not change."],
  ["During a phase change the added heat separates the molecules (potential energy rises). The temperature, which tracks kinetic energy, does not change.",
   "If the average kinetic energy rose, the temperature would rise, but it stays at 0 °C.",
   "Melting moves molecules apart (from a rigid solid to a liquid), so their potential energy rises. Lower potential energy goes with freezing.",
   "Energy is never destroyed; it goes into separating the molecules."],
  "Temperature constant means kinetic energy constant. So where does the heat go?",
  "On a plateau, heat raises <b>potential energy</b> (molecules move apart); kinetic energy and temperature stay constant.", 2)

Q(T, "A large pot of soup and a teaspoon of the same soup are both at 70 °C. Which statement is correct?",
  ["They have the same average kinetic energy of particles, but the pot holds far more thermal energy and can release more heat.",
   "The pot has the higher temperature because it holds more soup.",
   "The teaspoon's particles have the higher average kinetic energy because there are fewer of them.",
   "They hold the same amount of thermal energy because they are at the same temperature."],
  ["Temperature depends on the average kinetic energy per particle; total thermal energy also depends on how many particles there are.",
   "Both are at 70 °C. Amount does not change temperature.",
   "The same temperature means the same average kinetic energy, whatever the number of particles.",
   "The same temperature does not mean the same total energy. The pot has many more molecules, so it holds much more thermal energy."],
  "Temperature is an average. Thermal energy is a total.",
  "Same temperature, same <b>average</b> KE; the pot has more particles, so <b>more total thermal energy</b>.", 2)

# ======================= ch09-temp (10) =======================
T = 'ch09-temp'
Cg = '38.9'; ans = c2f(Cg)
Q(T, "A patient's temperature is 38.9 °C. What is it in degrees Fahrenheit?",
  [ans + " °F", qd(rnd(D('1.8') * (D(Cg) + 32), 4), 1) + " °F", num(D(Cg) / D('1.8') + 32, 3) + " °F", c2k(Cg) + " °F"],
  ["°F = 1.8(38.9) + 32 = 70.0 + 32. Multiply first, then add 32.",
   "This adds 32 before multiplying, 1.8(38.9 + 32). The formula multiplies the Celsius temperature by 1.8 first.",
   "This divides by 1.8 instead of multiplying. A Fahrenheit degree is smaller, so the Fahrenheit number is larger.",
   "This adds 273.15, which converts to kelvins, not to Fahrenheit."],
  "°F = 1.8(°C) + 32.",
  "°F = 1.8(38.9) + 32 = <b>" + ans + " °F</b>, a fever. The 1.8 and 32 are exact; 1.8 &times; 38.9 = 70.0 (3 significant figures, 1 decimal place), and adding 32 keeps 1 decimal place.", 2, 1)

Fg = '96.8'; ans = f2c(Fg)
Q(T, "A newborn's axillary (underarm) temperature reads 96.8 °F. What is it in degrees Celsius?",
  [ans + " °C", qd(D(Fg) - D(32) / D('1.8'), 1) + " °C", num((D(Fg) - 32) * D('1.8'), 3) + " °C", num((D(Fg) + 32) / D('1.8'), 3) + " °C"],
  ["(96.8 &minus; 32) &divide; 1.8 = 64.8 &divide; 1.8. Subtract 32 first, inside parentheses.",
   "This divides only the 32 by 1.8 (96.8 &minus; 32/1.8). Without parentheses the calculator divides first.",
   "This multiplies the difference by 1.8. Going from °F to °C you divide by 1.8.",
   "This adds 32. Going from °F to °C you subtract 32."],
  "°C = (°F &minus; 32) &divide; 1.8. Type the parentheses.",
  "(96.8 &minus; 32) &divide; 1.8 = 64.8 &divide; 1.8 = <b>" + ans + " °C</b>, a little below normal, so the baby is kept warm. (Context only.)", 2, 1)

Cg = '-80.0'; ans = c2k(Cg)
Q(T, "Many blood and tissue samples are stored in a freezer at &minus;80.0 °C. What is this temperature in kelvins?",
  [ans + " K", qd(D('80.0') + D('273.15'), 1) + " K", qd(D(Cg) - D('273.15'), 1) + " K", qd(-(D(Cg) + D('273.15')), 1) + " K"],
  ["K = &minus;80.0 + 273.15. Adding a negative number is the same as subtracting 80.0 from 273.15.",
   "This drops the minus sign on &minus;80.0. The sample is below 0 °C, so the Kelvin value must be below 273.15 K.",
   "This subtracts 273.15. To go from °C to K you add 273.15; a Kelvin temperature is never negative.",
   "Kelvin temperatures are never negative; 0 K is the lowest possible temperature."],
  "K = °C + 273.15, and watch the sign of the Celsius temperature.",
  "K = &minus;80.0 + 273.15 = <b>" + ans + " K</b>. The answer keeps 1 decimal place, like &minus;80.0.", 2, 1)

Kg = '4.22'; ans = k2c(Kg)
Q(T, "The liquid helium that cools an MRI scanner's magnet boils at about 4.22 K. What is this temperature in degrees Celsius?",
  [ans + " °C", qd(D(Kg) + D('273.15'), 2) + " °C", qd(D('273.15') - D(Kg), 2) + " °C", num(D(Kg) * D('1.8') + 32, 3) + " °C"],
  ["°C = K &minus; 273.15 = 4.22 &minus; 273.15. The answer is just above absolute zero (&minus;273.15 °C).",
   "This adds 273.15. Going from K to °C you subtract 273.15.",
   "This subtracts in the wrong order (273.15 &minus; 4.22). A temperature this cold must be far below 0 °C.",
   "This uses the Fahrenheit formula, 1.8(T) + 32, on a Kelvin temperature."],
  "°C = K &minus; 273.15.",
  "4.22 &minus; 273.15 = <b>" + ans + " °C</b>, kept to 2 decimal places like 4.22.", 2, 1)

Fg = '93.2'; c_ = f2c(Fg); ans = c2k(c_)
Q(T, "A hiker rescued from a cold river has a core temperature of 93.2 °F, a sign of hypothermia. What is this in kelvins?",
  [ans + " K",
   c2k(qd(D(Fg) - D(32) / D('1.8'), 1)) + " K",
   c_ + " K",
   c2k(qd(D(Fg) - 32, 1)) + " K"],
  ["First °C: (93.2 &minus; 32) &divide; 1.8 = 34.0 °C. Then K = 34.0 + 273.15.",
   "This leaves out the parentheses, so only 32 is divided by 1.8, before adding 273.15.",
   "This stops at the Celsius value and labels it K. Add 273.15 to finish.",
   "This subtracts 32 but never divides by 1.8, then adds 273.15."],
  "Two steps: °F &rarr; °C, then °C &rarr; K.",
  "(93.2 &minus; 32) &divide; 1.8 = " + c_ + " °C; " + c_ + " + 273.15 = <b>" + ans + " K</b>. (Context only.)", 3, 1)

Kg = '90.19'; c_ = k2c(Kg); ans = c2f(c_)
Q(T, "Liquid oxygen, used in some home and hospital oxygen supplies, boils at 90.19 K. What is this temperature in degrees Fahrenheit?",
  [ans + " °F", qd(D(Kg) * D('1.8') + 32, 2) + " °F", c_ + " °F", c2f(qd(D(Kg) + D('273.15'), 2)) + " °F"],
  ["First °C: 90.19 &minus; 273.15 = &minus;182.96 °C. Then °F = 1.8(&minus;182.96) + 32.",
   "This puts the Kelvin temperature straight into the °F formula. Convert K to °C first.",
   "This stops at the Celsius temperature and labels it °F.",
   "This adds 273.15 instead of subtracting it in the first step."],
  "K &rarr; °C (subtract 273.15), then °C &rarr; °F.",
  "90.19 &minus; 273.15 = " + c_ + " °C; 1.8(" + c_ + ") + 32 = <b>" + ans + " °F</b>, kept to 2 decimal places like the measurement.", 3, 1)

Q(T, "Which statement about absolute zero is correct?",
  ["It is 0 K, or &minus;273.15 °C, the lowest possible temperature; Kelvin temperatures are never negative.",
   "It is 0 °C, the temperature at which water freezes.",
   "It is &minus;273.15 K, the coldest temperature ever measured.",
   "It is 0 °F, so very cold objects can have negative Kelvin temperatures."],
  ["The Kelvin scale starts at absolute zero, where particles have the least possible energy, so there are no negative kelvins.",
   "0 °C is the freezing point of water, which is 273.15 K, far above absolute zero.",
   "Absolute zero is 0 K, which equals &minus;273.15 °C. A temperature of &minus;273.15 K is not possible.",
   "0 °F is about &minus;17.8 °C, not absolute zero; and Kelvin temperatures are never negative."],
  "Where does the Kelvin scale start?",
  "Absolute zero = <b>0 K = &minus;273.15 °C</b>, the lowest possible temperature.", 1)

dCg = '2.4'
Q(T, "During an infection, a patient's temperature rises by 2.4 °C. By how many kelvins and how many Fahrenheit degrees did it rise?",
  ["%s K and %s °F" % (dCg, num(D('1.8') * D(dCg), 2)),
   "%s K and %s °F" % (c2k(dCg), c2f(dCg)),
   "%s K and %s °F" % (dCg, dCg),
   "%s K and %s °F" % (dCg, num(D(dCg) / D('1.8'), 2))],
  ["A kelvin is the same size as a Celsius degree, and a Celsius degree is 1.8 Fahrenheit degrees: 1.8 &times; 2.4 = 4.3.",
   "This converts 2.4 as if it were a temperature, adding 273.15 and 32. For a temperature change, those offsets cancel.",
   "A Fahrenheit degree is smaller than a Celsius degree, so a change of 2.4 °C is more than 2.4 Fahrenheit degrees.",
   "This divides by 1.8. A Celsius degree is larger, so the change in °F is a larger number, not a smaller one."],
  "This is a temperature change, not a temperature. Which offsets cancel?",
  "Change in K = change in °C = 2.4 K; change in °F = 1.8 &times; 2.4 = <b>" + num(D('1.8') * D(dCg), 2) + " °F</b>.", 2, 1)

Q(T, "A room thermometer reads 25 °C. What is the temperature in kelvins, with correct significant figures?",
  [c2k('25') + " K", "298.15 K", "298.2 K", "3.0 &times; 10<sup>2</sup> K"],
  ["25 + 273.15 = 298.15. 273.15 is exact, so the measurement sets the precision: 25 has no decimal places, so the answer has none.",
   "273.15 is exact, but the measured 25 °C is known only to the ones place, so the answer cannot have two decimal places.",
   "25 °C is known to the ones place, so the sum is rounded to the ones place, not to one decimal place.",
   "Addition keeps decimal places, not significant figures. Rounding to 2 significant figures throws away a digit that the measurement supports."],
  "Adding: keep the decimal places of the measurement.",
  "25 + 273.15 = 298.15, rounded to the ones place like 25: <b>" + c2k('25') + " K</b>.", 2, 1)

R4 = [('101.1', '°F'), ('38.1', '°C'), ('311.4', 'K'), ('100.6', '°F')]
Q(T, "Four temperatures were recorded for four patients on different devices. Which is the highest temperature?",
  ["101.1 °F", "38.1 °C", "311.4 K", "100.6 °F"],
  ["(101.1 &minus; 32) &divide; 1.8 = %s °C, the highest of the four." % f2c('101.1'),
   "38.1 °C is a fever, but one of the other readings converts to a higher Celsius value.",
   "311.4 is the biggest number, but in kelvins it is %s &minus; 273.15 = %s °C. Compare temperatures on the same scale." % ('311.4', k2c('311.4')),
   "(100.6 &minus; 32) &divide; 1.8 = %s °C, lower than another reading." % f2c('100.6')],
  "Convert all four to °C before you compare.",
  "In °C: 101.1 °F = %s, 38.1 °C, 311.4 K = %s, 100.6 °F = %s. Highest: <b>101.1 °F</b>." % (f2c('101.1'), k2c('311.4'), f2c('100.6')), 3, 1)

# ======================= ch09-units (8) =======================
T = 'ch09-units'
x = D('116') * D('4.184')
Q(T, "A large apple provides about 116 Cal (food Calories). How many kilojoules is this? (1 Cal = 4.184 kJ)",
  [num(x) + " kJ", num(D('116') * 4184) + " kJ", num(D('116') / D('4.184')) + " kJ", num(x / 1000) + " kJ"],
  ["116 Cal &times; 4.184 kJ/Cal. A kilojoule is smaller than a Calorie, so the number grows about 4 times.",
   "This multiplies by 4184, which converts Calories to joules, and then labels the answer kJ.",
   "This divides by 4.184, the conversion upside down; kJ should be a larger number than Cal.",
   "This treats a food Calorie as a small calorie (1 cal = 4.184 J), giving joules and then kJ. A food Calorie is 1000 cal."],
  "1 Cal = 1 kcal = 4.184 kJ. Should the number of kJ be bigger or smaller than 116?",
  "116 Cal &times; (4.184 kJ / 1 Cal) = <b>" + num(x) + " kJ</b>. 4.184 is exact, so the 3 significant figures of 116 set the answer.", 1, 1)

x = D('8.50e3') / D('4.184')
Q(T, "Dissolving a sample of calcium chloride in a hot pack releases 8.50 &times; 10<sup>3</sup> J. How many calories is this?",
  [num(x) + " cal", num(D('8.50e3') * D('4.184')) + " cal", num(D('8.50e3') / 4184) + " cal", "8.50 cal"],
  ["8.50 &times; 10<sup>3</sup> J &divide; 4.184 J/cal. A calorie is bigger than a joule, so there are fewer calories than joules.",
   "This multiplies by 4.184, the conversion upside down.",
   "This divides by 4184, which gives food Calories (kcal), not calories.",
   "This only moves the decimal point, as if converting J to kJ, and labels the answer cal."],
  "1 cal = 4.184 J. Which unit is bigger?",
  "8.50 &times; 10<sup>3</sup> J &times; (1 cal / 4.184 J) = <b>" + num(x) + " cal</b>.", 2, 1)

x = D('6.70e2') / D('4.184')
Q(T, "A half-hour brisk walk uses about 6.70 &times; 10<sup>2</sup> kJ for one adult. How many food Calories is this?",
  [num(x) + " Cal", num(D('6.70e2') * D('4.184')) + " Cal", num(D('6.70e2') / 4184) + " Cal", num(D('6.70e2') * 1000 / D('4.184')) + " Cal"],
  ["6.70 &times; 10<sup>2</sup> kJ &divide; 4.184 kJ/Cal. The trailing decimal point shows 3 significant figures.",
   "This multiplies by 4.184; a Calorie is bigger than a kJ, so the number of Calories is smaller.",
   "This divides by 4184 as if the energy were in joules. The energy is in kJ, and 1 Cal = 4.184 kJ.",
   "This converts to small calories (cal), not food Calories; 1 Cal = 1000 cal."],
  "1 Cal = 4.184 kJ.",
  "6.70 &times; 10<sup>2</sup> kJ &times; (1 Cal / 4.184 kJ) = <b>" + num(x) + " Cal</b>.", 2, 1)

x = D('3.25') * 4184
Q(T, "A sample of water absorbs 3.25 kcal of heat. How many joules is this?",
  [num(x) + " J", num(D('3.25') * D('4.184')) + " J", num(D('3.25e3') / D('4.184')) + " J", num(x * 1000) + " J"],
  ["3.25 kcal &times; 1000 cal/kcal &times; 4.184 J/cal = 3.25 &times; 4184 J.",
   "This converts calories, not kilocalories; 1 kcal = 1000 cal, so the result is 1000 times too small.",
   "This divides by 4.184. Joules are smaller units, so the number of joules must be larger than the number of calories.",
   "This multiplies by 1000 twice. 1 kcal = 4184 J."],
  "1 kcal = 1000 cal = 4184 J.",
  "3.25 kcal &times; (4184 J / 1 kcal) = <b>" + num(x) + " J</b>.", 2, 1)

Q(T, "Sweat evaporates from a runner's skin. Taking the sweat as the system, which statement is correct?",
  ["Evaporation is endothermic: the sweat absorbs heat from the skin, q &gt; 0, and the skin cools.",
   "Evaporation is exothermic: q &lt; 0, because the skin feels cooler.",
   "Evaporation is endothermic, so q &lt; 0 for the sweat.",
   "Evaporation is exothermic: the sweat releases heat, q &gt; 0."],
  ["Turning liquid into vapor pulls molecules apart, which takes heat. The sweat absorbs it from the skin, so q is positive for the sweat.",
   "The skin feels cool because it loses heat to the sweat. For the sweat, the system, heat comes in: endothermic.",
   "Endothermic means heat enters the system, so q is positive, not negative.",
   "Exothermic means heat leaves the system, and q is then negative. Neither part fits evaporation."],
  "Which way does heat flow: from skin to sweat, or sweat to skin?",
  "Heat flows into the sweat: <b>endothermic, q &gt; 0</b>; the skin (surroundings) cools.", 2)

Q(T, "In the calorimetry lab, a student dissolves a solid in water in a foam cup, and the water's temperature drops from 22.4 °C to 18.9 °C. Which statement is correct?",
  ["Dissolving is endothermic: the solid (system) absorbs heat from the water, so q &gt; 0 for the dissolving.",
   "Dissolving is exothermic, because the temperature changed.",
   "The water is the system, and it absorbed heat.",
   "Dissolving is endothermic, so q &lt; 0 for the dissolving."],
  ["The water (surroundings) got colder, so it lost heat to the dissolving solid. Heat into the system means endothermic and a positive q.",
   "Any heat flow changes the temperature. The water got colder, so the system took heat in, which is endothermic.",
   "The dissolving solid is the system; the water is the surroundings, and its temperature fell because it lost heat.",
   "Endothermic means heat into the system, so q is positive."],
  "Water colder means the water lost heat. Where did that heat go?",
  "The water lost heat to the dissolving: <b>endothermic, q &gt; 0</b> for the system.", 2)

Q(T, "An instant hot pack warms a patient's hands when a salt dissolves inside it. Which describes the dissolving process (the system)?",
  ["Exothermic: q &lt; 0, and heat flows from the pack into the hands", "Endothermic: q &gt; 0, and heat flows into the pack",
   "Exothermic: q &gt; 0, because heat is produced", "Endothermic: q &lt; 0, because the hands warm up"],
  ["The dissolving releases heat to its surroundings (the hands), so it is exothermic with a negative q.",
   "If heat flowed into the pack, the pack would feel cold, like a cold pack.",
   "Heat released by the system makes q negative; the sign is written from the system's point of view.",
   "Warm hands mean heat left the system: exothermic, not endothermic."],
  "Heat out of the system: what sign?",
  "<b>Exothermic, q &lt; 0</b>: the pack releases heat to the hands. (Context only; wrap packs and follow directions.)", 1)

Q(T, "Which of these changes is <b>exothermic</b>?",
  ["Frost forming directly from water vapor on a windshield", "Ice melting on a sprained ankle",
   "Dry ice turning into gas", "Rubbing alcohol evaporating from the skin"],
  ["Gas to solid (deposition) brings molecules together, which releases heat.",
   "Melting pulls molecules apart, which absorbs heat (endothermic).",
   "Sublimation (solid to gas) absorbs heat (endothermic).",
   "Evaporation absorbs heat from the skin (endothermic), which is why it feels cold."],
  "Changes that bring particles together release heat.",
  "<b>Deposition (frost forming)</b> releases heat; the other three absorb it.", 1)

# ======================= ch09-specheat (11) =======================
T = 'ch09-specheat'
m_, Ti, Tf = '955', '52.5', '37.0'; dT = sub(Tf, Ti); x = D(m_) * CW * D(dT)
Q(T, "A hot-water bottle holds 955 g of water. How much heat does it release to a patient's feet as it cools from 52.5 °C to 37.0 °C? (c for water = 4.184 J/(g·°C))",
  ["q = " + num(x) + " J", "q = " + sg(-x) + " J", "q = " + num(x / 1000) + " J", "q = " + sg(D(m_) * CW * D(Tf)) + " J"],
  ["&Delta;T = 37.0 &minus; 52.5 = &minus;15.5 °C, so q = (955)(4.184)(&minus;15.5). The negative sign means heat is released.",
   "This uses initial minus final. &Delta;T is final minus initial; cooling gives a negative &Delta;T and a negative q.",
   "This is the answer in kJ labeled as J. q = mc&Delta;T gives joules when c is in J/(g·°C).",
   "This uses the final temperature, 37.0 °C, as &Delta;T. &Delta;T is the change, final minus initial."],
  "&Delta;T = T<sub>final</sub> &minus; T<sub>initial</sub>. Cooling: what sign?",
  "q = (955 g)(4.184 J/(g·°C))(&minus;15.5 °C) = <b>" + num(x) + " J</b>; about " + num(-x / 1000) + " kJ is released. (Context only; follow device directions.)", 2, 1)

m_, Ti, Tf = '250.0', '21.0', '175.0'; dT = sub(Tf, Ti); x = D(m_) * CAL * D(dT)
Q(T, "A 250.0 g aluminum pan is heated from 21.0 °C to 175.0 °C. How much heat does it absorb? (c for aluminum = 0.903 J/(g·°C))",
  [num(x) + " J", num(D(m_) * CW * D(dT), 4) + " J", sg(-x) + " J", num(D(m_) * CAL * D(Tf)) + " J"],
  ["&Delta;T = 175.0 &minus; 21.0 = 154.0 °C; q = (250.0)(0.903)(154.0). 0.903 has 3 significant figures, so the answer has 3.",
   "This uses water's specific heat, 4.184. Use the specific heat of the substance that is warming, aluminum.",
   "This uses initial minus final. The pan warms, so &Delta;T and q are positive.",
   "This uses the final temperature as &Delta;T instead of the change."],
  "Which specific heat belongs to the pan?",
  "q = (250.0 g)(0.903 J/(g·°C))(154.0 °C) = <b>" + num(x) + " J</b>.", 2, 1)

m_, q_ = '65.0', '412'; x = D(q_) / (D(m_) * CAG)
Q(T, "A 65.0 g silver bracelet absorbs 412 J of heat from the sun. By how much does its temperature rise? (c for silver = 0.235 J/(g·°C))",
  [num(x) + " °C", num(D(q_) * D(m_) * CAG) + " °C", num(D(q_) / D(m_) * CAG) + " °C", num(D(q_) / (D(m_) * CW)) + " °C"],
  ["&Delta;T = q &divide; (mc) = 412 &divide; (65.0 &times; 0.235).",
   "This multiplies q, m, and c together. Solve q = mc&Delta;T for &Delta;T by dividing q by (m &times; c).",
   "This divides by m but multiplies by c. Both m and c belong in the denominator.",
   "This uses water's specific heat. The bracelet is silver, which warms much more easily."],
  "&Delta;T = q / (mc).",
  "&Delta;T = 412 J &divide; (65.0 g &times; 0.235 J/(g·°C)) = <b>" + num(x) + " °C</b>.", 2, 1)

m_, Ti, q_ = '312', '24.5', '5.60'; dT = rnd(D(q_) * 1000 / (D(m_) * CCU), 3); x = add_k(D(Ti), dT)
dTw = rnd(D(q_) * 1000 / (D(m_) * CW), 3)
Q(T, "A 312 g copper pot at 24.5 °C absorbs 5.60 kJ of heat. What is its final temperature? (c for copper = 0.385 J/(g·°C))",
  [qd(x, 1) + " °C", num(dT) + " °C", qd(D(Ti) - dT, 1) + " °C", qd(add_k(D(Ti), dTw), 1) + " °C"],
  ["5.60 kJ = 5600 J; &Delta;T = 5600 &divide; (312 &times; 0.385) = %s °C; T<sub>f</sub> = 24.5 + %s." % (num(dT), num(dT)),
   "This is &Delta;T, the change. The question asks for the final temperature: add &Delta;T to 24.5 °C.",
   "This subtracts &Delta;T. The pot absorbs heat, so it gets hotter.",
   "This uses water's specific heat. The pot is copper."],
  "Convert kJ to J, find &Delta;T, then add it to the starting temperature.",
  "&Delta;T = 5600 J &divide; (312 g &times; 0.385) = " + num(dT) + " °C; T<sub>f</sub> = 24.5 + " + num(dT) + " = <b>" + qd(x, 1) + " °C</b>.", 3, 1)

q_, Ti, Tf = '7.75', '18.5', '37.0'; dT = sub(Tf, Ti); x = D(q_) * 1000 / (CW * D(dT))
Q(T, "A fluid warmer supplies 7.75 kJ of heat to warm a bag of saline from 18.5 °C to 37.0 °C. Treating the saline as water, what is its mass? (c = 4.184 J/(g·°C))",
  [num(x) + " g", num(D(q_) / (CW * D(dT))) + " g", num(D(q_) * 1000 * CW / D(dT)) + " g", num(D(q_) * 1000 / (CW * D(Tf))) + " g"],
  ["7.75 kJ = 7750 J; &Delta;T = 18.5 °C; m = q &divide; (c&Delta;T) = 7750 &divide; (4.184 &times; 18.5).",
   "This leaves q in kJ. Specific heat is in joules, so convert 7.75 kJ to 7750 J first.",
   "This multiplies q by c. Solve q = mc&Delta;T for m: m = q / (c&Delta;T).",
   "This uses the final temperature as &Delta;T. &Delta;T = 37.0 &minus; 18.5."],
  "m = q / (c&Delta;T), with q in joules.",
  "m = 7750 J &divide; (4.184 &times; 18.5 °C) = <b>" + num(x) + " g</b>. (Context only.)", 3, 1)

m_, q_, Ti, Tf = '75.0', '863', '19.8', '49.7'; dT = sub(Tf, Ti); x = D(q_) / (D(m_) * D(dT))
Q(T, "A 75.0 g sample of a metal absorbs 863 J as it warms from 19.8 °C to 49.7 °C. What is its specific heat?",
  [num(x) + " " + UC, num(D(q_) / (D(m_) * D(Tf))) + " " + UC, num(D(m_) * D(dT) / D(q_)) + " " + UC, num(D(q_) * D(dT) / D(m_)) + " " + UC],
  ["&Delta;T = 49.7 &minus; 19.8 = 29.9 °C; c = q &divide; (m&Delta;T) = 863 &divide; (75.0 &times; 29.9).",
   "This uses the final temperature, 49.7 °C, as &Delta;T. Use the change, 29.9 °C.",
   "This is (m&Delta;T)/q, the equation upside down. c = q/(m&Delta;T).",
   "This multiplies q by &Delta;T. Both m and &Delta;T belong in the denominator."],
  "c = q / (m&Delta;T). Find &Delta;T first.",
  "c = 863 J &divide; (75.0 g &times; 29.9 °C) = <b>" + num(x) + " " + UC + "</b>, the value for copper.", 2, 1)

m_, q_, Ti, Tf = '52.4', '312', '22.6', '47.9'; dT = sub(Tf, Ti); x = D(q_) / (D(m_) * D(dT))
Q(T, "A 52.4 g piece of jewelry absorbs 312 J as it warms from 22.6 °C to 47.9 °C. Use the table to identify the metal.",
  ["Silver", "Copper", "Iron", "Aluminum"],
  ["&Delta;T = 25.3 °C; c = 312 &divide; (52.4 &times; 25.3) = %s %s, which matches silver." % (num(x), UC),
   "Copper's specific heat is 0.385. The calculated value is much lower; check that &Delta;T = 47.9 &minus; 22.6.",
   "Iron's specific heat is 0.449, about twice the calculated value.",
   "Aluminum's specific heat is 0.903, far higher than the calculated value."],
  "Calculate c = q / (m&Delta;T), then find it in the table.",
  "c = 312 J &divide; (52.4 g &times; 25.3 °C) = " + num(x) + " " + UC + ": <b>silver</b>.", 2, 1,
  [{"type": "table", "cap": "Specific heats of some metals", "head": ["Metal", "c, " + UC],
    "rows": [["Aluminum", "0.903"], ["Iron", "0.449"], ["Copper", "0.385"], ["Silver", "0.235"]]}])

mw, Tw, Tfin = '45.0', '21.0', '31.5'; dT = sub(Tfin, Tw); qw = D(mw) * CW * D(dT)
Q(T, "A 65.0 g piece of iron at 99.2 °C is dropped into 45.0 g of water at 21.0 °C in a calorimeter. Both end at 31.5 °C. How much heat did the iron release? (c for water = 4.184 J/(g·°C))",
  ["q<sub>iron</sub> = " + num(-qw) + " J", "q<sub>iron</sub> = " + sg(qw) + " J", "q<sub>iron</sub> = " + num(-D('65.0') * CW * D(dT)) + " J",
   "q<sub>iron</sub> = " + num(-D(mw) * CW * D(Tfin)) + " J"],
  ["Heat gained by the water: (45.0)(4.184)(31.5 &minus; 21.0) = (45.0)(4.184)(10.5). The iron released the same amount, so its q is negative.",
   "This is the water's q. The iron released that heat, so &minus;q<sub>iron</sub> = q<sub>water</sub>: the iron's q is negative.",
   "This uses the iron's mass (65.0 g) with water's specific heat. Use the water's own mass, 45.0 g.",
   "This uses the final temperature, 31.5 °C, as the water's &Delta;T. The water warmed by 10.5 °C."],
  "Find the water's heat with q = mc&Delta;T, then use &minus;q<sub>hot</sub> = q<sub>cold</sub>.",
  "q<sub>water</sub> = (45.0 g)(4.184)(10.5 °C) = " + num(qw) + " J, so <b>q<sub>iron</sub> = " + num(-qw) + " J</b>.", 3, 1)

mm_, Tm, mw, Tw, Tfin = '85.0', '99.5', '45.0', '22.5', '33.9'
qw = D(mw) * CW * D(sub(Tfin, Tw)); dTm = sub(Tfin, Tm); x = -qw / (D(mm_) * D(dTm))
Q(T, "An 85.0 g metal block at 99.5 °C is placed in 45.0 g of water at 22.5 °C in a calorimeter. The final temperature of both is 33.9 °C. What is the specific heat of the metal? (c for water = 4.184 J/(g·°C))",
  [num(x) + " " + UC, num(qw / (D(mm_) * D(Tfin))) + " " + UC, num(qw / (D(mw) * (D(Tm) - D(Tfin)))) + " " + UC, num(qw / (D(mm_) * (D(Tfin) - D(Tw)))) + " " + UC],
  ["q<sub>water</sub> = (45.0)(4.184)(11.4) = %s J, so q<sub>metal</sub> = &minus;%s J. &Delta;T<sub>metal</sub> = 33.9 &minus; 99.5 = &minus;65.6 °C; c = q &divide; (m&Delta;T)." % (num(qw), num(qw)),
   "This uses the final temperature, 33.9 °C, as the metal's &Delta;T.",
   "This uses the water's mass for the metal. Use the metal's own mass, 85.0 g, with its own &Delta;T.",
   "This uses the water's &Delta;T (11.4 °C) for the metal. The metal cooled by 65.6 °C."],
  "Heat lost by the metal = heat gained by the water. Each one gets its own m and &Delta;T.",
  "c = &minus;(" + num(qw) + " J) &divide; (85.0 g &times; &minus;65.6 °C) = <b>" + num(x) + " " + UC + "</b>, copper.", 3, 1)

Q(T, "The same amount of heat is added to 50.0 g of aluminum (c = 0.903 J/(g·°C)) and to 50.0 g of gold (c = 0.128 J/(g·°C)). Which one has the larger temperature increase?",
  ["Gold, because its specific heat is lower", "Aluminum, because its specific heat is higher",
   "Both rise by the same amount, because the masses and heats are equal", "Gold, because its specific heat is higher"],
  ["&Delta;T = q/(mc). With q and m the same, the smaller c gives the larger &Delta;T, about 0.903/0.128 &asymp; 7 times as large.",
   "A high specific heat means more heat is needed per degree, so aluminum warms less.",
   "Equal heat and mass give equal &Delta;T only if the specific heats are equal; here they differ.",
   "Gold has the lower specific heat (0.128 &lt; 0.903), not the higher one."],
  "&Delta;T = q/(mc). Which c is smaller?",
  "&Delta;T = q/(mc): the lower c gives the larger rise, so <b>gold</b> warms about 7 times as much.", 2)

Q(T, "Before a predicted freeze, Valley citrus growers often irrigate their orchards. How does water's high specific heat help?",
  ["Moist soil absorbs and stores more heat by day and releases it at night, keeping the air near the trees slightly warmer.",
   "Water has a low specific heat, so it warms the trees quickly.",
   "The water makes the air colder, which protects the fruit.",
   "Specific heat does not matter; water simply blocks the cold."],
  ["Water's high specific heat (4.184 J/(g·°C)) means wet soil holds a lot of heat per degree, and it gives that heat back as it cools overnight.",
   "Water's specific heat is high, not low; that is why it stores so much heat.",
   "The goal is to keep the air near the trees from getting as cold, not to make it colder.",
   "The stored heat released as the moist soil cools is the effect of water's high specific heat."],
  "A high specific heat means a lot of heat stored per gram per degree.",
  "High specific heat: moist soil <b>stores more heat by day and releases it at night</b>.", 2)

# ======================= ch09-phase (10) =======================
T = 'ch09-phase'
g_ = '42.5'; x = D(g_) / MW * HFUS
Q(T, "How much heat is needed to melt 42.5 g of ice at 0 °C? ({H2O} 18.015 g/mol; &Delta;H<sub>fus</sub> = 6.02 kJ/mol)",
  ["q = " + sg(x) + " kJ", "q = " + sg(D(g_) * HFUS) + " kJ", "q = " + sg(D(g_) / MW * HVAP) + " kJ", "q = " + sg(-x) + " kJ"],
  ["42.5 g &divide; 18.015 g/mol = 2.359 mol; &times; 6.02 kJ/mol. Melting absorbs heat, so q is positive.",
   "This multiplies grams by kJ/mol. Convert grams to moles first, because &Delta;H<sub>fus</sub> is per mole.",
   "This uses &Delta;H<sub>vap</sub> (40.7 kJ/mol). Melting uses the heat of fusion.",
   "Melting absorbs heat (endothermic), so q is positive."],
  "q = n&Delta;H<sub>fus</sub>. Grams to moles first.",
  "q = (42.5 g &divide; 18.015 g/mol)(6.02 kJ/mol) = <b>" + sg(x) + " kJ</b>.", 2, 1)

g_ = '36.5'; x = D(g_) / MW * HVAP
Q(T, "How much heat is needed to boil away 36.5 g of water at 100 °C? ({H2O} 18.015 g/mol; &Delta;H<sub>vap</sub> = 40.7 kJ/mol)",
  ["q = " + sg(x) + " kJ", "q = " + sg(D(g_) * HVAP) + " kJ", "q = " + sg(D(g_) / MW * HFUS) + " kJ", "q = " + sg(-x) + " kJ"],
  ["36.5 g &divide; 18.015 g/mol = 2.026 mol; &times; 40.7 kJ/mol.",
   "This multiplies grams by kJ/mol. &Delta;H<sub>vap</sub> is per mole, so convert grams to moles first.",
   "This uses &Delta;H<sub>fus</sub> (6.02 kJ/mol). Boiling uses the heat of vaporization.",
   "Boiling absorbs heat (endothermic), so q is positive."],
  "Boiling: which &Delta;H, and per what?",
  "q = (36.5 &divide; 18.015 mol)(40.7 kJ/mol) = <b>" + sg(x) + " kJ</b>.", 2, 1)

g_ = '8.75'; x = -(D(g_) / MW * HVAP)
Q(T, "A puff of steam condenses on a cook's arm: 8.75 g of steam at 100 °C becomes liquid water at 100 °C. What is q for the steam? ({H2O} 18.015 g/mol; &Delta;H<sub>vap</sub> = 40.7 kJ/mol)",
  ["q = " + num(x) + " kJ", "q = " + sg(-x) + " kJ", "q = " + num(-(D(g_) / MW * HFUS)) + " kJ", "q = " + num(-(D(g_) * HVAP)) + " kJ"],
  ["8.75 &divide; 18.015 = 0.4857 mol; &times; 40.7 kJ/mol. Condensing releases heat, so q is negative, and all of it goes into the skin.",
   "Condensing is the reverse of vaporizing: same size of heat, opposite sign. Heat is released, so q is negative.",
   "This uses &Delta;H<sub>fus</sub>. Gas to liquid uses the heat of vaporization.",
   "This multiplies grams by kJ/mol; convert grams to moles first."],
  "Condensing: same &Delta;H as boiling, opposite sign.",
  "q = &minus;(8.75 &divide; 18.015 mol)(40.7 kJ/mol) = <b>" + num(x) + " kJ</b>, released into the skin before the water even starts to cool.", 2, 1)

g_ = '125'; x = -(D(g_) / MW * HFUS)
Q(T, "An ice tray holds 125 g of liquid water at 0 °C. What is q when all of it freezes? ({H2O} 18.015 g/mol; &Delta;H<sub>fus</sub> = 6.02 kJ/mol)",
  ["q = " + num(x) + " kJ", "q = " + sg(-x) + " kJ", "q = " + num(-(D(g_) / MW * HVAP)) + " kJ", "q = " + num(-(D(g_) * HFUS)) + " kJ"],
  ["125 &divide; 18.015 = 6.939 mol; &times; 6.02 kJ/mol, with a negative sign because freezing releases heat.",
   "Freezing is the reverse of melting, so the heat has the opposite sign: it is released, and q is negative.",
   "This uses &Delta;H<sub>vap</sub>. Liquid to solid uses the heat of fusion.",
   "This multiplies grams by kJ/mol; convert grams to moles first."],
  "Freezing releases heat. Which &Delta;H?",
  "q = &minus;(125 &divide; 18.015 mol)(6.02 kJ/mol) = <b>" + num(x) + " kJ</b>.", 2, 1)

g_ = '18.6'; x = D(g_) * 334
Q(T, "After a tooth extraction, a patient holds a bag of ice to the cheek. How much heat does 18.6 g of ice absorb as it melts at 0 °C? (&Delta;H<sub>fus</sub> = 334 J/g)",
  [num(x) + " J", num(D(g_) / MW * 334) + " J", num(D(g_) / 334) + " J", num(x / 1000) + " J"],
  ["The heat of fusion is given per gram here, so q = m &times; &Delta;H<sub>fus</sub> = 18.6 g &times; 334 J/g, with no moles needed.",
   "This converts grams to moles, but &Delta;H here is in J/g, not kJ/mol. Check the units of &Delta;H before converting.",
   "This divides by &Delta;H. q = m &times; &Delta;H.",
   "This is the answer in kJ labeled J."],
  "Look at the units of &Delta;H<sub>fus</sub>: per gram or per mole?",
  "q = 18.6 g &times; 334 J/g = <b>" + num(x) + " J</b> absorbed while the ice stays at 0 °C. (Context only; follow post-operative instructions.)", 2, 1)

HC = {"type": "plot", "x": {"min": 0, "max": 16, "label": "Heat added", "ticks": []},
      "y": {"min": -40, "max": 140, "label": "Temperature (°C)", "ticks": [-20, 0, 100, 120]},
      "series": [{"pts": [[0, -20], [1, 0], [3, 0], [5.5, 100], [13.5, 100], [14.5, 120]], "color": "#2f5fa8"}],
      "marks": [[1.1, -22, "A"], [2, 10, "B"], [5.0, 50, "C"], [9.5, 112, "D"], [15.3, 110, "E"]]}
Q(T, "The heating curve shows ice at &minus;20 °C heated to steam at 120 °C. In which segment is the heat calculated with q = n&Delta;H<sub>vap</sub>?",
  ["Segment D", "Segment B", "Segment C", "Segment E"],
  ["D is the flat segment at 100 °C, where liquid water boils at constant temperature. It is the longest step because &Delta;H<sub>vap</sub> is large.",
   "B is the plateau at 0 °C, where ice melts. That step uses &Delta;H<sub>fus</sub>, not &Delta;H<sub>vap</sub>.",
   "C is a sloped segment: liquid water warming from 0 °C to 100 °C. Slopes use q = mc&Delta;T.",
   "E is a sloped segment: steam warming above 100 °C, which uses q = mc&Delta;T with c for steam."],
  "Plateaus are phase changes. Which plateau is at the boiling point?",
  "<b>Segment D</b>, the boiling plateau at 100 °C, uses q = n&Delta;H<sub>vap</sub>. B (melting) uses &Delta;H<sub>fus</sub>; A, C, and E use mc&Delta;T.", 2, 0, [HC])

Q(T, "On the sloped segment of a heating curve where liquid water warms from 0 °C to 100 °C, which statement is correct?",
  ["The molecules speed up (kinetic energy rises), and q = mc&Delta;T with c = 4.184 J/(g·°C).",
   "The molecules move apart at constant temperature, and q = n&Delta;H.",
   "The molecules speed up, and q = mc&Delta;T with c = 2.09 J/(g·°C).",
   "No heat is absorbed, because the water does not change state."],
  ["A rising temperature means rising average kinetic energy. Use the specific heat of liquid water for this segment.",
   "That describes a plateau (phase change), where the temperature stays constant.",
   "2.09 J/(g·°C) is the specific heat of ice. Each state has its own specific heat.",
   "Heat is absorbed on every segment; on a slope it raises the temperature."],
  "Slope = temperature changing. Which state is warming?",
  "Slope: KE rises; <b>q = mc&Delta;T with liquid water's c, 4.184 J/(g·°C)</b>.", 2)

g_, T1 = '30.5', '64.0'; dT = sub('100', T1) if False else str(D('100') - D(T1))
q1 = rnd(D(g_) * CW * (D(100) - D(T1)) / 1000, 3); q2 = rnd(D(g_) / MW * HVAP, 3); tot = add_k(q1, q2)
q2f = rnd(D(g_) / MW * HFUS, 3); q2g = rnd(D(g_) * HVAP, 3)
Q(T, "How much heat is needed to take 30.5 g of water at 64.0 °C to steam at 100 °C? (c for water = 4.184 J/(g·°C); &Delta;H<sub>vap</sub> = 40.7 kJ/mol; {H2O} 18.015 g/mol)",
  [num(tot, 3) + " kJ", num(q2) + " kJ", qd(add_k(q1, q2f), ndp(add_k(q1, q2f))) + " kJ", num(q1 + q2g, 3) + " kJ"],
  ["Warm the liquid: (30.5)(4.184)(36.0) = %s kJ. Boil it: (30.5 &divide; 18.015)(40.7) = %s kJ. Add the two steps." % (num(q1), num(q2)),
   "This is only the boiling step. The water must first be warmed from 64.0 °C to 100 °C.",
   "This uses &Delta;H<sub>fus</sub> for the boiling step. Liquid to gas uses &Delta;H<sub>vap</sub>.",
   "This multiplies grams by &Delta;H<sub>vap</sub> without converting to moles."],
  "Two segments: a slope (mc&Delta;T) and a plateau (n&Delta;H). Put both in kJ, then add.",
  "q<sub>1</sub> = " + num(q1) + " kJ; q<sub>2</sub> = " + num(q2) + " kJ; total = <b>" + num(tot, 3) + " kJ</b>.", 3, 1)

g_, Ti, Tf = '16.5', '-12.5', '35.0'
q1 = rnd(D(g_) * CICE * (0 - D(Ti)) / 1000, 3); q2 = rnd(D(g_) / MW * HFUS, 3); q3 = rnd(D(g_) * CW * D(Tf) / 1000, 3)
tot = add_k(q1, q2, q3); q1w = rnd(D(g_) * CW * (0 - D(Ti)) / 1000, 3)
Q(T, "How much heat is needed to turn 16.5 g of ice at &minus;12.5 °C into liquid water at 35.0 °C? (c<sub>ice</sub> = 2.09 J/(g·°C); c<sub>water</sub> = 4.184 J/(g·°C); &Delta;H<sub>fus</sub> = 6.02 kJ/mol; {H2O} 18.015 g/mol)",
  [qd(tot, ndp(tot)) + " kJ", qd(add_k(q2, q3), ndp(add_k(q2, q3))) + " kJ", qd(add_k(q1, q3), ndp(add_k(q1, q3))) + " kJ", qd(add_k(q1w, q2, q3), ndp(add_k(q1w, q2, q3))) + " kJ"],
  ["Three steps: warm the ice, (16.5)(2.09)(12.5) = %s kJ; melt it, (16.5 &divide; 18.015)(6.02) = %s kJ; warm the water, (16.5)(4.184)(35.0) = %s kJ." % (num(q1), num(q2), num(q3)),
   "This leaves out warming the ice from &minus;12.5 °C to 0 °C.",
   "This leaves out the melting plateau, which is the largest step.",
   "This uses liquid water's specific heat for the ice. Ice has its own specific heat, 2.09 J/(g·°C)."],
  "Sketch the curve: slope, plateau, slope. Each one is its own q.",
  "q = " + num(q1) + " + " + num(q2) + " + " + num(q3) + " = <b>" + qd(tot, ndp(tot)) + " kJ</b>.", 3, 1)

g_, q_ = '10.0', '1.50'; need = rnd(D(g_) / MW * HFUS, 3)
Q(T, "A 10.0 g ice cube at 0 °C absorbs 1.50 kJ of heat. What happens? ({H2O} 18.015 g/mol; &Delta;H<sub>fus</sub> = 6.02 kJ/mol; c<sub>water</sub> = 4.184 J/(g·°C); c<sub>ice</sub> = 2.09 J/(g·°C))",
  ["Only part of the ice melts, and the temperature stays at 0 °C.",
   "All of the ice melts, and the water warms to " + num(D(q_) * 1000 / (D(g_) * CW)) + " °C.",
   "The ice warms to " + num(D(q_) * 1000 / (D(g_) * CICE)) + " °C without melting.",
   "All of the ice melts, and the liquid water stays at 0 °C."],
  ["Melting all 10.0 g takes (10.0 &divide; 18.015)(6.02) = %s kJ, more than the 1.50 kJ available, so the cube only partly melts at 0 °C." % num(need),
   "This uses q = mc&Delta;T as if the ice were already liquid. At 0 °C the heat first goes into melting.",
   "Ice at 0 °C cannot warm above 0 °C until it has melted; this uses mc&Delta;T for a phase change.",
   "Melting all 10.0 g needs more heat than the 1.50 kJ supplied, so some ice is still left."],
  "First find how much heat melting all of the ice would take. Is 1.50 kJ enough?",
  "Melting needs " + num(need) + " kJ &gt; 1.50 kJ, so <b>only part melts and the temperature stays at 0 °C</b>.", 3, 1)

# ======================= ch09-imf (10) =======================
T = 'ch09-imf'
Q(T, "Chloroform, {CHCl3}, was once used as an anesthetic. It is a polar tetrahedral molecule. Which intermolecular forces act between chloroform molecules?",
  ["Dispersion and dipole&ndash;dipole", "Dispersion only", "Dispersion, dipole&ndash;dipole, and hydrogen bonding", "Dipole&ndash;dipole only"],
  ["The C&ndash;Cl bonds are polar and do not cancel (the outer atoms are not all the same), so {CHCl3} is polar. Every molecule also has dispersion forces.",
   "Dispersion only is for nonpolar molecules. With one H and three Cl, the bond dipoles do not cancel.",
   "The H in {CHCl3} is bonded to carbon. Hydrogen bonding needs H bonded directly to N, O, or F.",
   "Every molecule has dispersion forces, including polar ones."],
  "Polar? Then dipole&ndash;dipole. Any H on N, O, or F?",
  "{CHCl3}: <b>dispersion and dipole&ndash;dipole</b> (no H on N, O, or F).", 2)

Q(T, "What is the strongest intermolecular force between molecules of methylamine, {CH3NH2}?",
  ["Hydrogen bonding", "Dipole&ndash;dipole", "Dispersion", "Ion&ndash;dipole"],
  ["Methylamine has two H atoms bonded directly to N, so N&ndash;H &middot;&middot;&middot; :N hydrogen bonds form between molecules.",
   "Methylamine is polar, but its N&ndash;H bonds add a stronger attraction on top of the dipole&ndash;dipole force.",
   "Dispersion is present, but for a small molecule with N&ndash;H bonds it is the weakest force here.",
   "There are no ions in pure methylamine."],
  "Look for H bonded directly to N, O, or F.",
  "The N&ndash;H bonds give <b>hydrogen bonding</b>, the strongest force here.", 1)

Q(T, "Which of these can hydrogen bond with itself?",
  ["{CH3CH2OH} (ethanol)", "{CH3OCH3} (dimethyl ether)", "{CH2O} (formaldehyde)", "{CHF3} (fluoroform)"],
  ["Ethanol has an O&ndash;H bond, so its H can bond to a lone pair on the O of another ethanol molecule.",
   "Dimethyl ether has an O, but every H is bonded to carbon. It is polar (dipole&ndash;dipole) but cannot hydrogen bond with itself.",
   "Formaldehyde has an O, but both H atoms are bonded to carbon. It has dipole&ndash;dipole forces, not hydrogen bonds with itself.",
   "Fluoroform has F atoms, but its H is bonded to carbon. A C&ndash;H hydrogen does not hydrogen bond."],
  "The H must be bonded directly to N, O, or F, not just be in the same molecule.",
  "Only <b>ethanol</b> has an H on O (O&ndash;H).", 2)

Q(T, "Carbon tetrachloride, {CCl4}, has polar C&ndash;Cl bonds and a symmetric tetrahedral shape. What is its strongest intermolecular force?",
  ["Dispersion", "Dipole&ndash;dipole", "Hydrogen bonding", "Ion&ndash;dipole"],
  ["Four identical polar bonds in a symmetric tetrahedron cancel, so {CCl4} is nonpolar and has dispersion forces only.",
   "The bonds are polar, but the molecule is not: symmetric shapes with identical outer atoms cancel the bond dipoles (SNAP).",
   "{CCl4} has no hydrogen at all.",
   "{CCl4} is a molecule, not an ionic compound, and there are no ions."],
  "SNAP: symmetric, nonpolar.",
  "{CCl4} is nonpolar: <b>dispersion</b> only.", 2)

Q(T, "These hydrocarbons are all nonpolar. Which has the strongest dispersion forces?",
  ["{C4H10} (butane)", "{CH4} (methane)", "{C2H6} (ethane)", "{C3H8} (propane)"],
  ["Butane has the most electrons (34), spread over the largest molecule, so its electron cloud is the most polarizable.",
   "Methane is the smallest, with only 10 electrons, so it has the weakest dispersion forces of the four.",
   "Ethane (18 electrons) is larger than methane but smaller than propane and butane.",
   "Propane (26 electrons) is second; butane has more electrons."],
  "Same kind of force: compare size (number of electrons).",
  "More electrons, more polarizable: <b>butane</b> has the strongest dispersion forces (and the highest boiling point of the four).", 1)

Q(T, "Xenon (Xe) boils at a much higher temperature than neon (Ne), although both are nonpolar atoms. Why?",
  ["Xe has many more electrons in a larger cloud that is easier to distort, so its dispersion forces are stronger.",
   "Xe is polar, so it has dipole&ndash;dipole forces.",
   "Xe atoms form hydrogen bonds with each other.",
   "Xe forms covalent bonds with its neighbors in the liquid."],
  ["Both have dispersion forces only. Xe (54 electrons) is far more polarizable than Ne (10 electrons).",
   "A single noble-gas atom has no permanent dipole; it is nonpolar.",
   "Hydrogen bonding needs H bonded to N, O, or F; there is no H here.",
   "Noble gases in the liquid are held by intermolecular forces, not covalent bonds."],
  "What makes dispersion forces stronger?",
  "Bigger electron cloud, more polarizable: <b>stronger dispersion forces in Xe</b>.", 2)

Q(T, "Potassium chloride, KCl, is added to many IV fluids. When it dissolves, which force holds water molecules around each K<sup>+</sup> ion?",
  ["Ion&ndash;dipole, with the &delta;&minus; oxygen ends of water pointing toward K<sup>+</sup>",
   "Ion&ndash;dipole, with the &delta;+ hydrogen ends of water pointing toward K<sup>+</sup>",
   "Hydrogen bonding between K<sup>+</sup> and the H atoms of water",
   "An ionic bond between K<sup>+</sup> and the O of water"],
  ["A positive ion attracts the partial negative end of a polar molecule: the O end of water.",
   "Like charges repel; the &delta;+ H ends point toward the negative Cl<sup>&minus;</sup> ions, not toward K<sup>+</sup>.",
   "Hydrogen bonds need H on N, O, or F and a lone pair on N, O, or F; K<sup>+</sup> has neither role.",
   "Water stays a neutral molecule; the attraction is an intermolecular ion&ndash;dipole force, not an ionic bond."],
  "Opposite partial charges attract. Which end of water is &delta;&minus;?",
  "<b>Ion&ndash;dipole</b>: water's &delta;&minus; O ends surround K<sup>+</sup>; the &delta;+ H ends surround Cl<sup>&minus;</sup>.", 2)

Q(T, "When ethanol boils, what is overcome?",
  ["The intermolecular forces between ethanol molecules; each molecule stays intact",
   "The covalent C&ndash;H bonds inside each molecule",
   "The O&ndash;H covalent bonds, which break to release hydrogen gas",
   "All the bonds, so the molecules split into separate atoms"],
  ["Boiling separates whole molecules from one another; the vapor is still {CH3CH2OH}.",
   "Covalent bonds within the molecule are much stronger than intermolecular forces and are not broken by boiling.",
   "Ethanol vapor is ethanol; no hydrogen gas forms. Hydrogen bonds between molecules are overcome, not covalent O&ndash;H bonds.",
   "Boiling is a physical change; the molecules keep their identity."],
  "Is boiling a physical or a chemical change?",
  "Boiling overcomes <b>intermolecular forces</b> (hydrogen bonds, dipole&ndash;dipole, dispersion); the molecules stay whole.", 1)

Q(T, "The two strands of DNA are held together by attractions between base pairs (A with T, G with C). What are these attractions, and why do they matter?",
  ["Hydrogen bonds between N&ndash;H groups and N or O atoms; each is weak, so the strands can unzip for copying",
   "Covalent bonds between the bases; they are very strong, so the strands never separate",
   "Ionic bonds between the bases, formed by transferring electrons",
   "Dispersion forces only, because the bases are nonpolar"],
  ["A&ndash;T pairs share two hydrogen bonds and G&ndash;C pairs share three. Each is weak, but millions together keep the helix stable.",
   "The strands must separate to copy and read genes; covalent bonds would be far too strong for that.",
   "No electrons are transferred between base pairs; they are attracted by hydrogen bonds.",
   "The bases have polar N&ndash;H, N, and O groups, which form hydrogen bonds."],
  "Look for H on N facing a lone pair on N or O.",
  "<b>Hydrogen bonds</b> hold base pairs together: weak one at a time, strong in total.", 2)

Q(T, "Which pair of atoms describes a hydrogen bond?",
  ["The H of one water molecule and the O of a neighboring water molecule",
   "The H and the O within one water molecule",
   "The H of one {CH4} molecule and the C of a neighboring {CH4} molecule",
   "The H of one {CH3F} molecule and the F of a neighboring {CH3F} molecule"],
  ["A hydrogen bond is between molecules: an H on O (or N, F) attracted to a lone pair on another molecule's O, N, or F.",
   "The O&ndash;H inside one molecule is a covalent bond, not a hydrogen bond.",
   "C&ndash;H bonds are nonpolar by the Chapter 6 rule, and C has no lone pair; methane has dispersion forces only.",
   "In {CH3F} every H is bonded to carbon, so it cannot hydrogen bond with itself, even though F is present."],
  "A hydrogen bond is an attraction between molecules, and the H must be bonded to N, O, or F.",
  "<b>H on one water molecule &middot;&middot;&middot; O of another</b>.", 2)

# ======================= ch09-solids (7) =======================
T = 'ch09-solids'
Q(T, "Which of these liquids has the highest surface tension?",
  ["Water, {H2O}", "Acetone, {CH3COCH3}", "Pentane, {C5H12}", "Dichloromethane, {CH2Cl2}"],
  ["Water's molecules are held by many hydrogen bonds, so the surface pulls inward strongly.",
   "Acetone is polar but has no O&ndash;H, so it has dipole&ndash;dipole forces, weaker than water's hydrogen bonding.",
   "Pentane is nonpolar, with dispersion forces only.",
   "Dichloromethane is polar with no H on N, O, or F: dipole&ndash;dipole, weaker than hydrogen bonding."],
  "Stronger intermolecular forces, higher surface tension.",
  "<b>Water</b>: hydrogen bonding gives the strongest pull at the surface.", 1)

Q(T, "Ethylene glycol, {HOCH2CH2OH}, is much more viscous than ethanol, {CH3CH2OH}. What is the best explanation?",
  ["Each ethylene glycol molecule has two O&ndash;H groups, so it forms more hydrogen bonds with its neighbors.",
   "Ethylene glycol is nonpolar, so its molecules slide past each other slowly.",
   "Ethanol has stronger hydrogen bonding, which makes it flow faster.",
   "Viscosity depends only on molar mass, and ethylene glycol is heavier."],
  ["Both hydrogen bond, but two O&ndash;H groups per molecule mean more attractions to overcome as the liquid flows.",
   "Ethylene glycol is polar, with two O&ndash;H groups.",
   "Stronger attractions make a liquid flow more slowly, not faster, and ethanol has fewer O&ndash;H groups.",
   "Size matters, but the number of hydrogen bonds matters at least as much here; molar mass alone does not explain the large difference."],
  "Both hydrogen bond. Which molecule can make more of them?",
  "Two O&ndash;H groups per molecule, <b>more hydrogen bonds</b>, higher viscosity.", 2)

Q(T, "During a finger-stick blood test, blood rises on its own into a thin glass capillary tube. Why?",
  ["The attraction of the blood to the glass (adhesion) is stronger than its attraction to itself (cohesion).",
   "The blood's cohesion is stronger than its adhesion to the glass.",
   "Blood has a high vapor pressure, so it moves up the tube.",
   "Gravity pulls the blood up the narrow tube."],
  ["Capillary action happens when adhesion to the walls is stronger than cohesion; water-based liquids are strongly attracted to polar glass.",
   "When cohesion wins, the liquid pulls away from the walls and does not climb.",
   "Vapor pressure is about molecules escaping into the gas phase, not climbing a tube.",
   "Gravity pulls down; capillary action works against it."],
  "Liquid-to-wall attraction versus liquid-to-liquid attraction.",
  "<b>Adhesion &gt; cohesion</b>, so the blood climbs the tube (capillary action).", 1)

Q(T, "Silicon carbide, SiC, used in grinding wheels and sandpaper, is extremely hard and does not melt even at 2000 °C. What type of solid is it?",
  ["Covalent network", "Molecular", "Ionic", "Metallic"],
  ["SiC is one of the network solids: Si and C atoms are joined by covalent bonds in an endless 3-D lattice, like diamond.",
   "SiC is made of nonmetal-like elements, but it does not exist as separate small molecules; molecular solids are soft and melt low.",
   "Si and C are both nonmetals or metalloids, with no metal cation, so SiC is not ionic.",
   "SiC contains no metal and does not conduct or bend like a metal."],
  "Nonmetals only usually means molecular. Which few are the exceptions?",
  "<b>Covalent network</b>, like diamond and quartz: covalent bonds throughout.", 2)

Q(T, "Diamond and graphite are both pure carbon, and both have very high melting points. What type of solid are they?",
  ["Covalent network: every carbon atom is joined to its neighbors by covalent bonds, which must break for the solid to melt",
   "Molecular: carbon is a nonmetal, so its atoms are held by dispersion forces",
   "Metallic: graphite conducts electricity, so it must be a metal",
   "Ionic: the carbon atoms carry positive and negative charges"],
  ["Diamond and graphite are two of the few network solids to memorize (with SiO<sub>2</sub> and SiC); the whole crystal is one covalent network.",
   "Nonmetals usually form molecular solids, but carbon in diamond and graphite is the main exception; molecular solids melt low.",
   "Graphite does conduct (some electrons move within its layers), but it contains no metal; it is a covalent network.",
   "All the atoms are carbon, so there is no electron transfer and no ions."],
  "Nonmetals only usually means molecular. Which few are the exceptions?",
  "<b>Covalent network</b>: covalent bonds throughout, so very high melting points.", 2)

Q(T, "Which statement about solid sodium chloride (table salt) is correct?",
  ["It has a high melting point and is brittle, and it does not conduct electricity until it is melted or dissolved.",
   "It conducts electricity as a solid, because it is made of ions.",
   "It has a low melting point, because its particles are held by intermolecular forces.",
   "It bends without breaking, like a metal."],
  ["The ions are locked in place in the solid; they can carry charge only when they are free to move.",
   "Ions are present, but in the solid they cannot move, so solid NaCl does not conduct.",
   "NaCl is held by ionic bonds throughout the crystal, so it melts high (801 °C).",
   "Ionic crystals are brittle: shifting a layer lines up like charges, which repel and crack the crystal."],
  "Ions can carry charge only if they can move.",
  "Ionic solids: <b>high melting point, brittle, conduct only when melted or dissolved</b>.", 1)

Q(T, "A gray solid is shiny, bends into wire without breaking, and conducts electricity as a solid. What type of solid is it most likely to be?",
  ["Metallic", "Ionic", "Covalent network", "Molecular"],
  ["Metal cations in a sea of mobile electrons explain shine, malleability, and conduction in the solid.",
   "Ionic solids are brittle and do not conduct as solids.",
   "Network solids are very hard and usually do not conduct or bend.",
   "Molecular solids are soft and do not conduct."],
  "Which type has electrons free to move?",
  "Shiny, malleable, conducts as a solid: <b>metallic</b>.", 1)

# ======================= ch09-vapor (9) =======================
T = 'ch09-vapor'
Q(T, "At 25 °C, which of these liquids has the highest vapor pressure?",
  ["Pentane, {C5H12}", "1-Propanol, {CH3CH2CH2OH}", "Water, {H2O}", "Acetic acid, {CH3COOH}"],
  ["Pentane is nonpolar, with dispersion forces only. The other three hydrogen bond, so pentane's molecules escape most easily, even though it has the largest molar mass here.",
   "1-Propanol hydrogen bonds through its O&ndash;H group, so it holds its molecules more tightly than a nonpolar liquid of similar size.",
   "Water's extensive hydrogen bonding gives it a low vapor pressure, even though its molar mass is the smallest.",
   "Acetic acid has an O&ndash;H group and hydrogen bonds strongly, so it evaporates slowly."],
  "Weakest forces, highest vapor pressure. Compare the strongest force before size.",
  "<b>Pentane</b>: the only liquid here without hydrogen bonding, so the highest vapor pressure (most volatile).", 2)

Q(T, "Water sits in a sealed container. As it warms from 25 °C to 50 °C, what happens to its vapor pressure?",
  ["It increases, because more molecules have enough energy to escape the liquid.",
   "It decreases, because warm water holds its molecules more tightly.",
   "It stays the same, because the container is sealed.",
   "It stays the same, because vapor pressure depends only on the amount of liquid."],
  ["At a higher temperature a larger fraction of molecules move fast enough to break free, so more vapor is present at equilibrium.",
   "Warming makes molecules move faster, so they escape more easily, not less.",
   "A sealed container lets evaporation and condensation reach equilibrium, but the equilibrium vapor pressure still rises with temperature.",
   "Vapor pressure depends on the substance and the temperature, not on how much liquid there is."],
  "Higher temperature, more molecules with enough energy to escape.",
  "Vapor pressure <b>rises with temperature</b>.", 1)

Q(T, "At a high Sierra Nevada campsite, water boils below 100 °C. Why?",
  ["The air pressure is lower, so water's vapor pressure reaches the outside pressure at a lower temperature.",
   "The air pressure is higher, which lowers the boiling point.",
   "Mountain water has fewer hydrogen bonds.",
   "Boiling point does not depend on pressure; the thermometer is cold."],
  ["A liquid boils when its vapor pressure equals the outside pressure. Lower outside pressure is reached at a lower temperature.",
   "Air pressure is lower at high altitude, and higher pressure would raise the boiling point.",
   "Water is the same substance at any altitude; its hydrogen bonding is unchanged.",
   "Boiling point depends on outside pressure; 100 °C is the normal boiling point at 1 atm."],
  "Boiling: vapor pressure = outside pressure.",
  "<b>Lower outside pressure</b>, so water boils at a lower temperature, and food cooks more slowly.", 2)

Q(T, "An autoclave sterilizes surgical instruments with steam at about 121 °C. How can the water reach 121 °C?",
  ["The autoclave raises the pressure, which raises water's boiling point above 100 °C.",
   "The autoclave lowers the pressure, which raises the boiling point.",
   "Steam always has a temperature of 121 °C.",
   "The autoclave adds heat faster than water can boil, so the boiling point rises."],
  ["At higher outside pressure, water's vapor pressure must climb higher before it boils, so the boiling point rises (about 121 °C at roughly 15 psi above atmospheric pressure).",
   "Lower pressure lowers the boiling point, as at high altitude.",
   "Steam can be at many temperatures; at 1 atm, water boils at 100 °C.",
   "Heating faster makes water boil sooner, but the boiling temperature is set by the pressure."],
  "What does a higher outside pressure do to the boiling point?",
  "<b>Higher pressure, higher boiling point</b>: steam at 121 °C kills even heat-resistant spores.", 2)

Q(T, "To freeze-dry (lyophilize) a vaccine, the frozen sample is placed under very low pressure until the ice is gone. How is the ice removed?",
  ["By sublimation: the ice turns directly into water vapor, absorbing heat",
   "By deposition: the ice turns directly into vapor, releasing heat",
   "By melting the ice and then boiling the liquid",
   "By condensation of the ice into vapor"],
  ["Solid to gas without melting is sublimation, and like other changes that separate molecules, it is endothermic.",
   "Deposition is the reverse, gas to solid, and it releases heat.",
   "Freeze-drying skips the liquid; at very low pressure the ice goes straight to vapor.",
   "Condensation is gas to liquid, which is not what happens to the ice."],
  "Solid straight to gas: what is it called?",
  "<b>Sublimation</b> (endothermic) removes the ice and leaves a dry product.", 1)

Q(T, "On a cold, clear night in the Valley, frost forms on a car windshield directly from water vapor in the air. What is this change, and what happens to heat?",
  ["Deposition; heat is released", "Sublimation; heat is absorbed", "Freezing; heat is absorbed", "Condensation; heat is absorbed"],
  ["Gas to solid is deposition, and bringing molecules together releases heat (exothermic).",
   "Sublimation is solid to gas, the reverse of this change.",
   "Freezing is liquid to solid; here the water goes from vapor directly to solid. Freezing also releases heat.",
   "Condensation is gas to liquid, and it releases heat rather than absorbing it."],
  "Vapor straight to solid.",
  "<b>Deposition, exothermic</b>: heat is released as the frost forms.", 1)

mb = mm('C4H10'); ma = mm('C3H6O'); mp = mm('C3H8O')
Q(T, "The three substances in the table have nearly the same molar mass. Rank them from <b>lowest to highest</b> boiling point.",
  ["butane &lt; acetone &lt; 1-propanol", "acetone &lt; butane &lt; 1-propanol", "1-propanol &lt; acetone &lt; butane", "butane &lt; 1-propanol &lt; acetone"],
  ["Butane is nonpolar (dispersion only), acetone is polar with no O&ndash;H (dipole&ndash;dipole), and 1-propanol has an O&ndash;H (hydrogen bonding).",
   "This ranks by molar mass. With sizes this close, the strongest force decides: acetone is polar, butane is not.",
   "This is the order of vapor pressure, from highest boiling to lowest. The question asks for lowest to highest boiling point.",
   "Acetone has dipole&ndash;dipole forces only; 1-propanol hydrogen bonds, so 1-propanol boils higher."],
  "Similar size: rank by the strongest force in each.",
  "Dispersion &lt; dipole&ndash;dipole &lt; hydrogen bond: <b>butane &lt; acetone &lt; 1-propanol</b> (about 0 °C, 56 °C, and 97 °C).", 3, 0,
  [{"type": "table", "cap": "Three substances of similar size", "head": ["Substance", "Formula", "Molar mass (g/mol)"],
    "rows": [["butane", "{CH3CH2CH2CH3}", str(mb)], ["acetone", "{CH3COCH3}", str(ma)], ["1-propanol", "{CH3CH2CH2OH}", str(mp)]]}])

Q(T, "Rank from <b>lowest to highest</b> melting point: F<sub>2</sub>, HF, NaF, SiO<sub>2</sub> (quartz).",
  ["F<sub>2</sub> &lt; HF &lt; NaF &lt; SiO<sub>2</sub>", "HF &lt; F<sub>2</sub> &lt; NaF &lt; SiO<sub>2</sub>",
   "F<sub>2</sub> &lt; SiO<sub>2</sub> &lt; HF &lt; NaF", "F<sub>2</sub> &lt; NaF &lt; HF &lt; SiO<sub>2</sub>"],
  ["Solid type first: SiO<sub>2</sub> is a covalent network and NaF is ionic (both high). Of the molecular substances, HF hydrogen bonds and F<sub>2</sub> has dispersion only.",
   "This ranks by molar mass (20 &lt; 38 &lt; 42 &lt; 60). HF is the lightest, but its hydrogen bonds beat the dispersion forces of F<sub>2</sub>.",
   "This treats SiO<sub>2</sub> as a small molecule. Quartz is a covalent network and melts near 1700 °C.",
   "This puts hydrogen bonding above ionic bonding. Ionic solids such as NaF melt far higher than molecular solids."],
  "Classify each solid, then use the strongest force, then size.",
  "<b>F<sub>2</sub> &lt; HF &lt; NaF &lt; SiO<sub>2</sub></b>: molecular (dispersion) &lt; molecular (H bonds) &lt; ionic &lt; covalent network.", 3)

Q(T, "Use the normal boiling points in the table. Which liquid has the <b>highest</b> vapor pressure at 25 °C?",
  ["Dichloromethane", "Acetone", "Methanol", "Water"],
  ["The lowest boiling point means the weakest attractions, so dichloromethane's molecules escape most easily at 25 °C.",
   "Acetone boils at 56 °C, higher than the first liquid in the table, so its vapor pressure at 25 °C is lower.",
   "Methanol hydrogen bonds and boils at 65 °C, so its vapor pressure is lower than those of the two lower-boiling liquids.",
   "Water has the highest boiling point here, which means the lowest vapor pressure. Vapor pressure runs opposite to boiling point."],
  "Vapor pressure and boiling point run in opposite orders.",
  "Lowest boiling point, highest vapor pressure: <b>dichloromethane</b>.", 2, 0,
  [{"type": "table", "cap": "Normal boiling points", "head": ["Liquid", "Boiling point (°C)"],
    "rows": [["Dichloromethane, {CH2Cl2}", "40"], ["Acetone, {CH3COCH3}", "56"], ["Methanol, {CH3OH}", "65"], ["Water, {H2O}", "100"]]}])

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'figs', sum(1 for q in B if q.get('f')),
      'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
