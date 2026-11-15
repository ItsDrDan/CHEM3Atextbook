#!/usr/bin/env python3
"""Builds bank/ch09_adapt.json (Chapter 9 ADAPT homework-only items, text only; 42 items, none repeated from
bank/ch09.json).
usage: python3 tools/gen_adapt_ch09.py bank/ch09_adapt.json
Same conventions, helpers and markup as tools/gen_bank_ch09.py (exact 32, 1.8, 273.15, 4.184 and 4184; specific
heats and water's heats of fusion and vaporization from the Chapter 9 text; H2O 18.015 g/mol; sig figs from the
givens; no trailing-zero givens without a decimal point). y[0] begins "Correct: ". Every item is rechecked by
tools/check_bank_ch09.py."""
import json, sys, re, os, collections
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 40
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
MS = json.load(open(os.path.join(HERE, 'yellow_sheet_masses.json')))['masses']
M = '&minus;'
B = []
PREFIX = 'c9-h%02d'

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
    assert f is None, 'ADAPT items are text only'
    y = ["Correct: " + y[0]] + y[1:]
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

# ======================= ch09-energy (4) =======================
T = 'ch09-energy'
Q(T, "Which of these is mainly <b>potential</b> energy?",
  ["A stretched rubber tourniquet before it is released", "A wheelchair rolling down a ramp",
   "Fast-moving molecules in warm air", "Wind turning the blades of a turbine"],
  ["A stretched elastic band stores energy of position (its shape) until it snaps back.",
   "A rolling wheelchair is moving, so its energy is kinetic.",
   "The random motion of molecules is thermal energy, a kind of kinetic energy.",
   "Moving air has kinetic energy, and so do the spinning blades."],
  "Stored, waiting to be released, or moving right now?",
  "The stretched tourniquet stores energy: <b>potential energy</b>.", 1)

Q(T, "A car battery runs the starter motor, which turns the engine. Which sequence describes the main energy changes?",
  ["Chemical potential energy &rarr; electrical energy &rarr; kinetic energy (plus some heat)",
   "Kinetic energy &rarr; chemical potential energy &rarr; electrical energy",
   "Electrical energy is created in the battery and then destroyed in the motor",
   "Heat &rarr; chemical potential energy &rarr; kinetic energy"],
  ["The battery's reactions release stored chemical energy as electricity, and the motor turns it into motion; some always becomes heat.",
   "The energy starts stored in the battery's chemicals, not as motion.",
   "Energy is never created or destroyed; it changes form.",
   "The battery does not start with heat; its energy is stored chemically."],
  "Where is the energy stored before the key is turned?",
  "<b>Chemical PE &rarr; electrical &rarr; kinetic (+ heat)</b>; the total is conserved.", 2)

Q(T, "Which statement about kinetic energy is correct?",
  ["At the same speed, an object with more mass has more kinetic energy.",
   "Kinetic energy depends only on mass, not on speed.",
   "A book resting on a high shelf has a large kinetic energy.",
   "The molecules in a room-temperature object have no kinetic energy."],
  ["Kinetic energy grows with both mass and speed, so a heavier object moving at the same speed has more.",
   "Speed matters too: the faster something moves, the more kinetic energy it has.",
   "The resting book has potential energy of position; it is not moving, so it has no kinetic energy.",
   "Atoms and molecules are always moving; temperature measures their average kinetic energy."],
  "Kinetic energy is energy of motion. What two things set it?",
  "<b>More mass at the same speed means more kinetic energy.</b>", 2)

Q(T, "A student says, &ldquo;When a bouncing ball finally stops, its energy has disappeared.&rdquo; Which is the best correction?",
  ["The energy changed into heat in the ball, the floor, and the air; the total energy is conserved.",
   "The energy was destroyed by friction.",
   "The ball's energy turned back into chemical potential energy.",
   "The student is right; a stopped ball has used up its energy."],
  ["Each bounce turns some energy of motion into thermal energy and sound, which spread into the surroundings.",
   "Friction converts energy into heat; it does not destroy it.",
   "The ball's energy spreads out as heat, not back into chemical energy.",
   "Energy is never used up, only changed in form or moved."],
  "Energy cannot be created or destroyed. Where did it go?",
  "It became <b>heat (thermal energy) in the surroundings</b>; total energy is conserved.", 1)

# ======================= ch09-temp (5) =======================
T = 'ch09-temp'
Cg = '-15.0'; ans = c2f(Cg)
Q(T, "Some vaccines are stored frozen at &minus;15.0 °C. What is this temperature in degrees Fahrenheit?",
  [ans + " °F", qd(rnd(D('1.8') * (D(Cg) + 32), 3), 1) + " °F", num(D(Cg) / D('1.8') + 32, 3) + " °F", num((D(Cg) - 32) / D('1.8'), 3) + " °F"],
  ["°F = 1.8(&minus;15.0) + 32 = &minus;27.0 + 32.",
   "This adds 32 before multiplying, 1.8(&minus;15.0 + 32). Multiply first, then add 32.",
   "This divides by 1.8 instead of multiplying.",
   "This uses the °F &rarr; °C formula, (T &minus; 32)/1.8, on a Celsius temperature."],
  "°F = 1.8(°C) + 32, and keep the minus sign.",
  "°F = 1.8(&minus;15.0) + 32 = &minus;27.0 + 32 = <b>" + ans + " °F</b>.", 2, 1)

Fg = '104.0'; ans = f2c(Fg)
Q(T, "On a July afternoon in Fresno, the air temperature reaches 104.0 °F. What is this in degrees Celsius?",
  [ans + " °C", qd(D(Fg) - D(32) / D('1.8'), 1) + " °C", num((D(Fg) - 32) * D('1.8'), 4) + " °C", num((D(Fg) + 32) / D('1.8'), 4) + " °C"],
  ["(104.0 &minus; 32) &divide; 1.8 = 72.0 &divide; 1.8.",
   "This divides only the 32 by 1.8. Put parentheses around (104.0 &minus; 32).",
   "This multiplies by 1.8; going from °F to °C you divide.",
   "This adds 32; going from °F to °C you subtract 32."],
  "°C = (°F &minus; 32) &divide; 1.8.",
  "(104.0 &minus; 32) &divide; 1.8 = <b>" + ans + " °C</b>.", 2, 1)

Kg = '194.7'; ans = k2c(Kg)
Q(T, "Dry ice (solid carbon dioxide) sublimes at 194.7 K at 1 atm. What is this temperature in degrees Celsius?",
  [ans + " °C", qd(D(Kg) + D('273.15'), 1) + " °C", qd(D('273.15') - D(Kg), 1) + " °C", qd(rnd(D('1.8') * D(Kg), 4) + 32, 1) + " °C"],
  ["°C = 194.7 &minus; 273.15. Dry ice is far below the freezing point of water.",
   "This adds 273.15. Going from K to °C you subtract.",
   "This subtracts in the wrong order; the answer must be negative, below 0 °C.",
   "This uses the Fahrenheit formula on a Kelvin temperature."],
  "°C = K &minus; 273.15.",
  "194.7 &minus; 273.15 = <b>" + ans + " °C</b> (1 decimal place, like 194.7).", 2, 1)

dFg = '12.5'
Q(T, "Overnight, the water in a lab's water bath cools by 12.5 °F. By how many kelvins did its temperature fall?",
  [num(D(dFg) / D('1.8'), 3) + " K", num(D(dFg) * D('1.8'), 3) + " K", dFg + " K", num((D(dFg) - 32) / D('1.8'), 3) + " K"],
  ["A Fahrenheit degree is 1/1.8 of a Celsius degree, and a kelvin equals a Celsius degree: 12.5 &divide; 1.8.",
   "This multiplies by 1.8. A kelvin is larger than a Fahrenheit degree, so the change in K is the smaller number.",
   "This assumes Fahrenheit degrees and kelvins are the same size; a kelvin is 1.8 Fahrenheit degrees.",
   "This subtracts 32, which is only for converting a temperature, not a temperature change."],
  "For a change, only the size of the degree matters.",
  "12.5 °F &divide; 1.8 = <b>" + num(D(dFg) / D('1.8'), 3) + " K</b> (same as " + num(D(dFg) / D('1.8'), 3) + " °C).", 3, 1)

Fg = '102.2'; c_ = f2c(Fg); ans = c2k(c_)
Q(T, "A patient's temperature is 102.2 °F. What is it in kelvins?",
  [ans + " K", c2k(qd(D(Fg) - D(32) / D('1.8'), 1)) + " K", c_ + " K", qd(D(c_) - D('273.15'), 1) + " K"],
  ["(102.2 &minus; 32) &divide; 1.8 = 39.0 °C; 39.0 + 273.15.",
   "This leaves out the parentheses, dividing only the 32 by 1.8, before adding 273.15.",
   "This stops at the Celsius value; add 273.15 to get kelvins.",
   "This subtracts 273.15; going from °C to K you add it. Kelvin temperatures are never negative."],
  "°F &rarr; °C &rarr; K.",
  "(102.2 &minus; 32) &divide; 1.8 = " + c_ + " °C; " + c_ + " + 273.15 = <b>" + ans + " K</b>.", 2, 1)

# ======================= ch09-units (5) =======================
T = 'ch09-units'
x = D('83.0') * 4184
Q(T, "A cup of nonfat milk provides 83.0 Cal. How many joules is this? (1 Cal = 4184 J)",
  [num(x) + " J", num(D('83.0') * D('4.184')) + " J", num(D('83.0') / D('4.184')) + " J", num(x * 1000) + " J"],
  ["83.0 Cal &times; 4184 J/Cal.",
   "This uses 4.184, which converts Cal to kJ (or cal to J). The answer would be in kJ, not J.",
   "This divides by 4.184; joules are smaller units, so the number must be larger.",
   "This multiplies by an extra 1000. 1 Cal = 4184 J."],
  "1 Cal = 1 kcal = 4184 J.",
  "83.0 Cal &times; (4184 J / 1 Cal) = <b>" + num(x) + " J</b>.", 2, 1)

x = D('2.75') * 1000 / D('4.184')
Q(T, "A small heater delivers 2.75 kJ of heat. How many calories is this?",
  [num(x) + " cal", num(D('2.75') * D('4.184')) + " cal", num(D('2.75') / D('4.184')) + " cal", num(D('2.75') * 1000 * D('4.184')) + " cal"],
  ["2.75 kJ = 2750 J; &divide; 4.184 J/cal.",
   "This multiplies kJ by 4.184; convert to J, then divide by 4.184.",
   "This divides by 4.184 without converting kJ to J, giving kcal (Cal), not cal.",
   "This multiplies by 4.184 instead of dividing."],
  "kJ &rarr; J &rarr; cal.",
  "2.75 kJ &times; (1000 J / 1 kJ) &times; (1 cal / 4.184 J) = <b>" + num(x) + " cal</b>.", 2, 1)

Q(T, "Which of these is the largest amount of energy?",
  ["1.00 kcal", "1.00 kJ", "1.00 cal", "500. J"],
  ["1.00 kcal (one food Calorie) = 4184 J, the largest of the four.",
   "1.00 kJ = 1000 J, about a quarter of the largest one.",
   "1.00 cal = 4.184 J, the smallest of the four.",
   "500. J is half of a kilojoule."],
  "Convert each one to joules.",
  "In joules: 4184 (kcal), 1000 (kJ), 4.184 (cal), 500. The largest is <b>1.00 kcal</b>.", 2)

Q(T, "Steam from a pot condenses on a cook's hand. Taking the steam as the system, which statement is correct?",
  ["Condensing is exothermic: the steam releases heat into the skin, so q &lt; 0.",
   "Condensing is endothermic: the steam absorbs heat from the skin, so q &gt; 0.",
   "Condensing is exothermic, so q &gt; 0.",
   "No heat flows, because the temperature stays at 100 °C."],
  ["Gas to liquid brings molecules together, which releases heat. Heat leaving the system makes q negative.",
   "Condensing releases heat; vaporizing is the change that absorbs heat.",
   "Exothermic means heat leaves the system, so q is negative.",
   "Heat flows during a phase change even though the temperature is constant; here it flows into the skin."],
  "Gas to liquid: are the molecules coming together or moving apart?",
  "<b>Exothermic, q &lt; 0</b>: the steam releases heat into the skin.", 2)

Q(T, "A reaction is run in a beaker, and the beaker feels cold in your hand. Which statement is correct?",
  ["The reaction is endothermic: it absorbs heat from the beaker and your hand, so q &gt; 0.",
   "The reaction is exothermic: it releases cold, so q &lt; 0.",
   "The reaction is exothermic, because your hand loses heat.",
   "The reaction is endothermic, so q &lt; 0."],
  ["Your hand feels cold because it is losing heat to the system. Heat into the system is endothermic, with a positive q.",
   "Cold is not something that can be released; heat flows into the reaction.",
   "Your hand (the surroundings) loses heat, which means the system gains heat: endothermic.",
   "Endothermic means heat enters the system, so q is positive."],
  "What feels cold is losing heat. Where does the heat go?",
  "<b>Endothermic, q &gt; 0</b> for the reaction.", 1)

# ======================= ch09-specheat (7) =======================
T = 'ch09-specheat'
m_, Ti, Tf = '375', '18.0', '42.5'; dT = sub(Tf, Ti); x = D(m_) * CETH * D(dT)
Q(T, "How much heat is needed to warm 375 g of ethanol from 18.0 °C to 42.5 °C? (c for ethanol = 2.42 J/(g·°C))",
  [num(x) + " J", num(D(m_) * CW * D(dT)) + " J", num(-x) + " J", num(x / 1000) + " J"],
  ["&Delta;T = 42.5 &minus; 18.0 = 24.5 °C; q = (375)(2.42)(24.5).",
   "This uses water's specific heat. Use the c of the substance being warmed, ethanol.",
   "This uses initial minus final. The ethanol warms, so q is positive.",
   "This is the answer in kJ labeled J."],
  "q = mc&Delta;T, with ethanol's specific heat.",
  "q = (375 g)(2.42 J/(g·°C))(24.5 °C) = <b>" + num(x) + " J</b>.", 2, 1)

m_, Ti, Tf = '165', '88.5', '22.0'; dT = sub(Tf, Ti); x = D(m_) * CPB * D(dT)
Q(T, "A 165 g lead fishing weight cools from 88.5 °C to 22.0 °C. What is q for the lead? (c for lead = 0.128 J/(g·°C))",
  ["q = " + num(x) + " J", "q = " + sg(-x) + " J", "q = " + num(x / 1000) + " J", "q = " + sg(D(m_) * CPB * D(Tf)) + " J"],
  ["&Delta;T = 22.0 &minus; 88.5 = &minus;66.5 °C; q = (165)(0.128)(&minus;66.5). Cooling releases heat, so q is negative.",
   "This uses initial minus final. &Delta;T is final minus initial, which is negative for cooling.",
   "This is the answer in kJ labeled J.",
   "This uses the final temperature as &Delta;T."],
  "&Delta;T = T<sub>f</sub> &minus; T<sub>i</sub>.",
  "q = (165 g)(0.128)(&minus;66.5 °C) = <b>" + num(x) + " J</b>.", 2, 1)

m_, Ti, q_ = '85.0', '22.5', '1.25'; dT = rnd(D(q_) * 1000 / (D(m_) * CFE), 3); x = add_k(D(Ti), dT)
dTw = rnd(D(q_) * 1000 / (D(m_) * CW), 3)
Q(T, "An 85.0 g iron nail at 22.5 °C absorbs 1.25 kJ of heat. What is its final temperature? (c for iron = 0.449 J/(g·°C))",
  [qd(x, 1) + " °C", num(dT) + " °C", qd(D(Ti) - dT, 1) + " °C", qd(add_k(D(Ti), dTw), 1) + " °C"],
  ["&Delta;T = 1250 &divide; (85.0 &times; 0.449) = %s °C; T<sub>f</sub> = 22.5 + %s." % (num(dT), num(dT)),
   "This is &Delta;T; add it to the starting temperature.",
   "This subtracts &Delta;T. Absorbing heat makes the nail hotter.",
   "This uses water's specific heat for the iron."],
  "kJ &rarr; J, then &Delta;T = q/(mc), then add.",
  "&Delta;T = 1250 J &divide; (85.0 g &times; 0.449) = " + num(dT) + " °C; T<sub>f</sub> = <b>" + qd(x, 1) + " °C</b>.", 3, 1)

q_, Ti, Tf = '2.45', '20.5', '65.0'; dT = sub(Tf, Ti); x = D(q_) * 1000 / (CCU * D(dT))
Q(T, "What mass of copper absorbs 2.45 kJ as it warms from 20.5 °C to 65.0 °C? (c for copper = 0.385 J/(g·°C))",
  [num(x) + " g", num(D(q_) / (CCU * D(dT))) + " g", num(D(q_) * 1000 * CCU / D(dT)) + " g", num(D(q_) * 1000 / (CCU * D(Tf))) + " g"],
  ["2.45 kJ = 2450 J; &Delta;T = 44.5 °C; m = 2450 &divide; (0.385 &times; 44.5).",
   "This leaves q in kJ; convert to 2450 J first.",
   "This multiplies q by c. m = q / (c&Delta;T).",
   "This uses the final temperature as &Delta;T."],
  "m = q / (c&Delta;T), q in joules.",
  "m = 2450 J &divide; (0.385 &times; 44.5 °C) = <b>" + num(x) + " g</b>.", 3, 1)

m_, q_, Ti, Tf = '28.4', '175', '21.3', '47.6'; dT = sub(Tf, Ti); x = D(q_) / (D(m_) * D(dT))
Q(T, "A 28.4 g sample absorbs 175 J as it warms from 21.3 °C to 47.6 °C. What is its specific heat?",
  [num(x) + " " + UC, num(D(q_) / (D(m_) * D(Tf))) + " " + UC, num(D(m_) * D(dT) / D(q_)) + " " + UC, num(D(q_) * D(dT) / D(m_)) + " " + UC],
  ["&Delta;T = 26.3 °C; c = 175 &divide; (28.4 &times; 26.3).",
   "This uses the final temperature as &Delta;T.",
   "This is (m&Delta;T)/q, upside down.",
   "This multiplies q by &Delta;T instead of dividing."],
  "c = q / (m&Delta;T).",
  "c = 175 J &divide; (28.4 g &times; 26.3 °C) = <b>" + num(x) + " " + UC + "</b>.", 2, 1)

mm_, Tm, mw, Tw, Tfin = '65.0', '99.5', '75.0', '19.5', '32.1'
qw = D(mw) * CW * D(sub(Tfin, Tw)); dTm = sub(Tfin, Tm); x = -qw / (D(mm_) * D(dTm))
Q(T, "A 65.0 g metal block at 99.5 °C is placed in 75.0 g of water at 19.5 °C in a calorimeter. Both end at 32.1 °C. What is the specific heat of the metal? (c for water = 4.184 J/(g·°C))",
  [num(x) + " " + UC, num(qw / (D(mm_) * D(Tfin))) + " " + UC, num(qw / (D(mw) * (D(Tm) - D(Tfin)))) + " " + UC, num(qw / (D(mm_) * (D(Tfin) - D(Tw)))) + " " + UC],
  ["q<sub>water</sub> = (75.0)(4.184)(12.6) = %s J = &minus;q<sub>metal</sub>; &Delta;T<sub>metal</sub> = &minus;67.4 °C; c = q &divide; (m&Delta;T). This matches aluminum." % num(qw),
   "This uses the final temperature as the metal's &Delta;T.",
   "This uses the water's mass for the metal.",
   "This uses the water's &Delta;T for the metal."],
  "Heat lost by the metal = heat gained by the water.",
  "c = &minus;(" + num(qw) + " J) &divide; (65.0 g &times; &minus;67.4 °C) = <b>" + num(x) + " " + UC + "</b>, aluminum.", 3, 1)

Q(T, "Liquid water has a specific heat of 4.184 J/(g·°C), much higher than most substances. What is the main reason?",
  ["Hydrogen bonds between water molecules absorb part of the added energy instead of speeding the molecules up.",
   "Water molecules are very heavy.",
   "Water is nonpolar, so heat passes through it easily.",
   "Water has a low boiling point."],
  ["Some of the heat goes into stretching and breaking hydrogen bonds, so more heat is needed for each degree of warming.",
   "Water (18 g/mol) is a light molecule; mass does not explain its high specific heat.",
   "Water is polar, with strong hydrogen bonding.",
   "Water's boiling point (100 °C) is high for such a small molecule, and the boiling point does not set the specific heat."],
  "What attractions does water have that most liquids lack?",
  "<b>Hydrogen bonding</b> soaks up part of the added heat.", 2)

# ======================= ch09-phase (7) =======================
T = 'ch09-phase'
n_ = '2.35'; x = D(n_) * HFUS
Q(T, "How much heat is needed to melt 2.35 mol of ice at 0 °C? (&Delta;H<sub>fus</sub> = 6.02 kJ/mol)",
  [num(x) + " kJ", num(D(n_) * HVAP) + " kJ", num(D(n_) / HFUS) + " kJ", num(D(n_) * MW * HFUS) + " kJ"],
  ["The amount is already in moles: q = 2.35 mol &times; 6.02 kJ/mol.",
   "This uses &Delta;H<sub>vap</sub>; melting uses &Delta;H<sub>fus</sub>.",
   "This divides by &Delta;H. q = n &times; &Delta;H.",
   "This converts moles to grams first. &Delta;H is per mole, so use the moles directly."],
  "q = n&Delta;H<sub>fus</sub>.",
  "q = 2.35 mol &times; 6.02 kJ/mol = <b>" + num(x) + " kJ</b>.", 1, 1)

g_ = '22.8'; x = -(D(g_) / MW * HVAP)
Q(T, "In an autoclave, 22.8 g of steam at 100 °C condenses on cool instruments. What is q for the steam? ({H2O} 18.015 g/mol; &Delta;H<sub>vap</sub> = 40.7 kJ/mol)",
  ["q = " + num(x) + " kJ", "q = " + sg(-x) + " kJ", "q = " + num(-(D(g_) / MW * HFUS)) + " kJ", "q = " + num(-(D(g_) * HVAP)) + " kJ"],
  ["22.8 &divide; 18.015 = 1.266 mol; &times; 40.7 kJ/mol; negative because condensing releases heat to the instruments.",
   "Condensing releases heat, so q for the steam is negative.",
   "This uses &Delta;H<sub>fus</sub>; gas to liquid uses &Delta;H<sub>vap</sub>.",
   "This multiplies grams by kJ/mol; convert to moles first."],
  "Condensing: &minus;n&Delta;H<sub>vap</sub>.",
  "q = &minus;(22.8 &divide; 18.015 mol)(40.7 kJ/mol) = <b>" + num(x) + " kJ</b>.", 2, 1)

g_ = '45.5'; x = -(D(g_) * 334)
Q(T, "Using &Delta;H<sub>fus</sub> = 334 J/g, what is q when 45.5 g of liquid water freezes at 0 °C?",
  ["q = " + num(x) + " J", "q = " + sg(-x) + " J", "q = " + num(-(D(g_) / MW * 334)) + " J", "q = " + num(x / 1000) + " J"],
  ["&Delta;H<sub>fus</sub> is per gram, so q = &minus;(45.5 g &times; 334 J/g); freezing releases heat.",
   "Freezing releases heat, so q is negative.",
   "This converts to moles, but this &Delta;H is per gram.",
   "This is the answer in kJ labeled J."],
  "Check the units of &Delta;H. Freezing: what sign?",
  "q = &minus;(45.5 g)(334 J/g) = <b>" + num(x) + " J</b>.", 2, 1)

g_, T2 = '5.80', '45.0'
q1 = rnd(-(D(g_) / MW * HVAP), 3); q2 = rnd(D(g_) * CW * (D(T2) - 100) / 1000, 3); tot = add_k(q1, q2)
Q(T, "In a steam burn, 5.80 g of steam at 100 °C condenses on the skin and the water then cools to 45.0 °C. What is the total q for the water? (c<sub>water</sub> = 4.184 J/(g·°C); &Delta;H<sub>vap</sub> = 40.7 kJ/mol; {H2O} 18.015 g/mol)",
  ["q = " + qd(tot, ndp(tot)) + " kJ", "q = " + num(q1) + " kJ", "q = " + num(q2) + " kJ", "q = +" + qd(-tot, ndp(tot)) + " kJ"],
  ["Condense: &minus;(5.80 &divide; 18.015)(40.7) = %s kJ. Cool: (5.80)(4.184)(45.0 &minus; 100) = %s kJ. Add them." % (num(q1), num(q2)),
   "This is only the condensing step; the hot water also cools to 45.0 °C.",
   "This is only the cooling step; most of the heat comes from condensing.",
   "Both steps release heat into the skin, so q for the water is negative."],
  "Two steps, both releasing heat: a plateau, then a slope.",
  "q = " + num(q1) + " + (" + num(q2) + ") = <b>" + qd(tot, ndp(tot)) + " kJ</b>; the condensing step is almost 10 times larger.", 3, 1)

Q(T, "Which equation and specific heat give the heat needed to warm steam from 100 °C to 115 °C?",
  ["q = mc&Delta;T with c = 2.01 J/(g·°C)", "q = mc&Delta;T with c = 4.184 J/(g·°C)", "q = n&Delta;H<sub>vap</sub>", "q = n&Delta;H<sub>fus</sub>"],
  ["Warming one state is a sloped segment, so use mc&Delta;T with the specific heat of steam.",
   "4.184 J/(g·°C) is the specific heat of liquid water; steam has its own, 2.01.",
   "&Delta;H<sub>vap</sub> is for the boiling plateau at 100 °C; here the steam is already a gas and is warming.",
   "&Delta;H<sub>fus</sub> is for melting at 0 °C."],
  "Is the temperature changing? Which state is warming?",
  "Sloped segment, gas phase: <b>q = mc&Delta;T with c<sub>steam</sub> = 2.01 J/(g·°C)</b>.", 2)

Q(T, "Which three phase changes release heat (are exothermic)?",
  ["Freezing, condensation, and deposition", "Melting, vaporization, and sublimation",
   "Freezing, vaporization, and deposition", "Melting, condensation, and sublimation"],
  ["Each of these brings particles closer together (liquid &rarr; solid, gas &rarr; liquid, gas &rarr; solid), which releases heat.",
   "These three pull particles apart, so they absorb heat.",
   "Vaporization (liquid &rarr; gas) absorbs heat.",
   "Melting and sublimation absorb heat; only condensation here releases it."],
  "Particles coming together release heat.",
  "<b>Freezing, condensation, deposition</b> release heat; their reverses absorb the same amount.", 1)

Q(T, "Why does a burn from steam at 100 °C usually cause more damage than a splash of water at 100 °C?",
  ["Steam releases its large heat of vaporization as it condenses on the skin, before the water even starts to cool.",
   "Steam is hotter than 100 °C water at the same temperature.",
   "Water at 100 °C absorbs heat from the skin.",
   "Steam has a higher specific heat than liquid water."],
  ["Condensing releases 40.7 kJ/mol into the skin first; then the hot water releases still more heat as it cools.",
   "Both are at 100 °C; the difference is the extra heat released by condensing.",
   "Water hotter than the skin releases heat to it; it does not absorb heat from it.",
   "Steam's specific heat (2.01) is lower than liquid water's (4.184), so specific heat does not explain it."],
  "What extra step does steam go through on the skin?",
  "<b>Condensing releases &Delta;H<sub>vap</sub></b> into the skin on top of the heat from cooling.", 2)

# ======================= ch09-imf (5) =======================
T = 'ch09-imf'
Q(T, "Acetone, {CH3COCH3}, the solvent in many nail polish removers, is polar and has no O&ndash;H bond. Which intermolecular forces act between acetone molecules?",
  ["Dispersion and dipole&ndash;dipole", "Dispersion only", "Dispersion, dipole&ndash;dipole, and hydrogen bonding", "Ion&ndash;dipole"],
  ["Acetone is polar (the C=O bond dipole is not canceled), and every molecule has dispersion forces.",
   "Acetone is polar, so it has dipole&ndash;dipole forces too.",
   "Acetone has an O, but all of its H atoms are on carbon, so it cannot hydrogen bond with itself.",
   "There are no ions in acetone."],
  "Polar, but is any H bonded to N, O, or F?",
  "Acetone: <b>dispersion and dipole&ndash;dipole</b>.", 2)

Q(T, "What is the strongest intermolecular force in hydrogen peroxide, {H2O2} (H&ndash;O&ndash;O&ndash;H)?",
  ["Hydrogen bonding", "Dipole&ndash;dipole", "Dispersion", "Ion&ndash;dipole"],
  ["Both H atoms are bonded directly to O, so the molecules hydrogen bond with each other.",
   "{H2O2} is polar, but its O&ndash;H bonds add a stronger attraction on top of the dipole&ndash;dipole force.",
   "Dispersion forces are present but weaker than the hydrogen bonds here.",
   "{H2O2} is a molecule; there are no ions."],
  "Look for H bonded to N, O, or F.",
  "O&ndash;H bonds: <b>hydrogen bonding</b>.", 1)

Q(T, "Which of these <b>cannot</b> hydrogen bond with itself?",
  ["{CH2Cl2} (dichloromethane)", "{CH3NH2} (methylamine)", "{H2O2} (hydrogen peroxide)", "{CH3COOH} (acetic acid)"],
  ["Both H atoms in {CH2Cl2} are bonded to carbon, and it has no N, O, or F. It has dipole&ndash;dipole forces only.",
   "Methylamine has N&ndash;H bonds, so it can hydrogen bond.",
   "Hydrogen peroxide has O&ndash;H bonds, so it can hydrogen bond.",
   "Acetic acid has an O&ndash;H group (the COOH), so it can hydrogen bond."],
  "Find the molecule with no H on N, O, or F.",
  "<b>{CH2Cl2}</b>: its H atoms are on carbon.", 2)

Q(T, "For molecules of similar size, which list orders the forces from weakest to strongest?",
  ["Dispersion &lt; dipole&ndash;dipole &lt; hydrogen bond &lt; ion&ndash;dipole",
   "Hydrogen bond &lt; dipole&ndash;dipole &lt; dispersion &lt; ion&ndash;dipole",
   "Dispersion &lt; hydrogen bond &lt; dipole&ndash;dipole &lt; ion&ndash;dipole",
   "Ion&ndash;dipole &lt; hydrogen bond &lt; dipole&ndash;dipole &lt; dispersion"],
  ["Temporary dipoles are weakest, permanent dipoles stronger, hydrogen bonds (a special strong dipole&ndash;dipole force) stronger still, and full ionic charges strongest.",
   "Hydrogen bonds are the strongest force between neutral molecules, not the weakest.",
   "A hydrogen bond is an especially strong dipole&ndash;dipole force, so it ranks above ordinary dipole&ndash;dipole.",
   "This list is reversed."],
  "Temporary dipole, permanent dipole, very strong dipole, full charge.",
  "<b>Dispersion &lt; dipole&ndash;dipole &lt; hydrogen bond &lt; ion&ndash;dipole</b> (for similar sizes).", 1)

Q(T, "Which of these noble gases has the strongest dispersion forces?",
  ["Kr", "He", "Ne", "Ar"],
  ["Krypton has the most electrons here (36), so its electron cloud is the most polarizable.",
   "Helium has only 2 electrons, so it has the weakest dispersion forces of all.",
   "Neon (10 electrons) is smaller than argon and krypton.",
   "Argon (18 electrons) is second; krypton has more."],
  "More electrons, more polarizable.",
  "<b>Kr</b>: most electrons, strongest dispersion forces, highest boiling point of the four.", 1)

# ======================= ch09-solids (4) =======================
T = 'ch09-solids'
Q(T, "Tooth enamel is mostly hydroxyapatite, {Ca5(PO4)3OH}, made of Ca<sup>2+</sup>, PO<sub>4</sub><sup>3&minus;</sup>, and OH<sup>&minus;</sup> ions. What type of crystalline solid is it?",
  ["Ionic", "Molecular", "Covalent network", "Metallic"],
  ["A metal cation with polyatomic anions makes an ionic solid: hard, high-melting, and brittle.",
   "Hydroxyapatite is not made of separate neutral molecules; it is a lattice of ions.",
   "Covalent network solids (diamond, graphite, quartz, SiC) have no ions.",
   "The calcium is present as Ca<sup>2+</sup> ions bonded to anions, not as a metal with a sea of electrons."],
  "Metal plus polyatomic ions.",
  "Ions in a lattice: <b>ionic</b>. (Context only.)", 1)

Q(T, "Cells in the lungs secrete pulmonary surfactant, which lowers the surface tension of the thin water film lining each alveolus (air sac). Why does that help breathing?",
  ["Lower surface tension means less inward pull on the alveoli, so they stay open and inflate with less effort.",
   "Lower surface tension makes the water film evaporate, drying the lungs.",
   "Surfactant raises the surface tension, which holds the alveoli open.",
   "Surfactant turns the water film into ice, which keeps its shape."],
  ["Water's high surface tension, from hydrogen bonding, would pull small air sacs closed; surfactant weakens that pull.",
   "The goal is not to dry the alveoli; the film stays, but it pulls inward less strongly.",
   "Surfactant lowers surface tension; higher surface tension would collapse the alveoli.",
   "The film stays liquid at body temperature."],
  "Surface tension pulls a liquid surface inward.",
  "<b>Lower surface tension, less inward pull</b>: the alveoli stay open more easily. (Context only.)", 2)

Q(T, "Window glass softens gradually over a range of temperatures instead of melting sharply at one temperature. Why?",
  ["Glass is an amorphous solid: its particles have no long-range repeating order.",
   "Glass is a crystalline solid with a perfect lattice.",
   "Glass is a metallic solid.",
   "Glass is made of small molecules held by dispersion forces."],
  ["Without a regular lattice, the attractions in glass vary from place to place, so different regions soften at different temperatures.",
   "Crystalline solids melt sharply at one temperature; glass does not.",
   "Glass does not conduct electricity or have a sea of electrons.",
   "Glass is mostly SiO<sub>2</sub> held by covalent bonds, just without a regular arrangement."],
  "Regular, repeating pattern or not?",
  "<b>Amorphous</b>: no long-range order, so it softens over a range.", 2)

Q(T, "Which of these is a <b>molecular</b> solid?",
  ["Aspirin, {C9H8O4}", "Graphite, C", "Calcium fluoride, {CaF2}", "Aluminum foil, Al"],
  ["Aspirin is made of separate molecules held together by intermolecular forces, so it is soft and melts low.",
   "Graphite is one of the covalent network solids.",
   "{CaF2} is a metal with a nonmetal: ionic.",
   "Aluminum is a metal: metallic solid."],
  "Nonmetals only, and not one of the network solids.",
  "<b>Aspirin</b> is a molecular solid.", 1)

# ======================= ch09-vapor (5) =======================
T = 'ch09-vapor'
Q(T, "When does a liquid boil?",
  ["When its vapor pressure equals the pressure of the gas above it",
   "Whenever it reaches 100 °C",
   "When its vapor pressure becomes zero",
   "When molecules at the surface begin to evaporate"],
  ["At that point bubbles of vapor can form throughout the liquid, not just at the surface.",
   "100 °C is water's normal boiling point at 1 atm only; other liquids, and water at other pressures, boil at other temperatures.",
   "Vapor pressure rises as a liquid is heated; boiling happens when it reaches the outside pressure.",
   "Evaporation at the surface happens at any temperature; boiling happens throughout the liquid."],
  "Compare the vapor pressure with the outside pressure.",
  "A liquid boils when <b>vapor pressure = outside pressure</b>.", 1)

Q(T, "An alcohol prep pad feels cold on the skin before an injection. Why?",
  ["Isopropyl alcohol is volatile; it evaporates quickly, and evaporation absorbs heat from the skin.",
   "The alcohol is stored in a refrigerator.",
   "Evaporation releases heat, which the nerves sense as cold.",
   "Alcohol has a lower temperature than any liquid at room temperature."],
  ["Weak attractions give isopropyl alcohol a high vapor pressure, and the endothermic evaporation pulls heat out of the skin.",
   "Prep pads are kept at room temperature; the cooling comes from evaporation.",
   "Evaporation absorbs heat; it is endothermic.",
   "The pad starts at room temperature; it cools the skin as it evaporates."],
  "Is evaporation endothermic or exothermic?",
  "<b>Fast, endothermic evaporation</b> of a volatile liquid cools the skin. (Context only.)", 1)

Q(T, "Evaporative (swamp) coolers on Valley roofs cool homes well on dry summer afternoons but poorly on humid days. Why?",
  ["In humid air, water evaporates from the pads more slowly, so less heat is absorbed from the air.",
   "Humid air has a lower temperature, so the cooler is not needed.",
   "Water evaporates faster in humid air, which overheats the pads.",
   "Humidity raises the boiling point of the water in the pads to 100 °C."],
  ["Evaporation absorbs heat. When the air already holds a lot of water vapor, less water evaporates, so less cooling happens.",
   "Humid days can be just as hot; the problem is slower evaporation.",
   "Evaporation is slower, not faster, in humid air.",
   "The pads work by evaporation well below the boiling point; humidity slows evaporation."],
  "The cooling comes from evaporation. What slows evaporation?",
  "<b>Humid air slows evaporation</b>, so the cooler absorbs less heat from the air.", 2)

Q(T, "Rank HF, HCl, and HBr from <b>lowest to highest</b> boiling point.",
  ["HCl &lt; HBr &lt; HF", "HF &lt; HCl &lt; HBr", "HBr &lt; HCl &lt; HF", "HF &lt; HBr &lt; HCl"],
  ["HCl and HBr have dipole&ndash;dipole forces, and HBr's extra electrons give it stronger dispersion forces. HF hydrogen bonds, so it boils highest (about 20 °C, versus about &minus;85 °C and &minus;67 °C).",
   "This ranks by molar mass alone. HF is the lightest, but it hydrogen bonds, which beats the larger dispersion forces of HBr.",
   "Between HCl and HBr, the strongest force is the same (dipole&ndash;dipole), so size breaks the tie: HBr, with more electrons, boils higher.",
   "This reverses the order; HF's hydrogen bonding makes it boil highest."],
  "Strongest force first; size only breaks ties.",
  "<b>HCl &lt; HBr &lt; HF</b>: the hydrogen bonding in HF outweighs size.", 3)

Q(T, "Which of these liquids has the <b>lowest</b> vapor pressure at 25 °C?",
  ["Ethylene glycol, {HOCH2CH2OH}", "Hexane, {C6H14}", "Ethanol, {CH3CH2OH}", "Water, {H2O}"],
  ["Two O&ndash;H groups per molecule give ethylene glycol extensive hydrogen bonding, so very few molecules escape.",
   "Hexane has the largest molar mass, but it is nonpolar with dispersion forces only, so it evaporates easily (high vapor pressure).",
   "Ethanol has one O&ndash;H group and fewer hydrogen bonds; it is more volatile than water.",
   "Water hydrogen bonds strongly, but ethylene glycol is larger and has two O&ndash;H groups, so it evaporates even less."],
  "Strongest attractions, lowest vapor pressure.",
  "<b>Ethylene glycol</b> has the strongest attractions here, so the lowest vapor pressure.", 3)

json.dump(B, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(B), dict(collections.Counter(q['t'] for q in B)), 'd', dict(sorted(collections.Counter(q['d'] for q in B).items())), 'k=1', sum(q['k'] for q in B))
