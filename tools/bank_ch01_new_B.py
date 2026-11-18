"""New Chapter 1 Try It items, writer B (2026-11-17).

Keys: ch01-multistep (1.4.2), ch01-powers (1.4.3), ch01-dosage (1.4.4), ch01-percent (1.4.5).
Brief: audit/expansion/CH1_TRYIT_BRIEF.md. c[0] is always correct. Every number is computed below and
asserted as the exact string shown in the choices. Run: python3 -I tools/bank_ch01_new_B.py
Values: yellow sheet (1 in = 2.54 cm exact; 1 kg = 2.2046 lb; 1 gal = 3.785 L).
"""
from decimal import Decimal, ROUND_HALF_UP
from math import floor, log10
import re
import collections

MP = "<b>Math practice only; always follow the order and facility policy.</b> "


def sf(x, n):
    """x rounded to n significant figures (half up), as a plain decimal string."""
    d = Decimal(repr(float(x)))
    e = floor(log10(abs(float(x))))
    q = Decimal(1).scaleb(e - n + 1)
    r = d.quantize(q, rounding=ROUND_HALF_UP)
    if abs(r) >= Decimal(10) ** (e + 1):  # rounding bumped the magnitude
        q = Decimal(1).scaleb(e - n + 2)
        r = d.quantize(q, rounding=ROUND_HALF_UP)
    s = format(r, "f")
    return s


def sci(x, n):
    """x to n significant figures in scientific notation, as item HTML."""
    e = floor(log10(abs(float(x))))
    m = sf(float(x) / 10 ** e, n)
    if float(m) >= 10:
        e += 1
        m = sf(float(x) / 10 ** e, n)
    es = ("&minus;%d" % -e) if e < 0 else str(e)
    return "%s &times; 10<sup>%s</sup>" % (m, es)


def eq(a, b):
    assert a == b, (a, b)


LB = 2.2046  # lb per kg (yellow sheet)
CM_IN = 2.54  # cm per in (exact)
L_GAL = 3.785  # L per gal (yellow sheet)

ITEMS = []

# ---------------------------------------------------------------- ch01-multistep (1.4.2)

# M1 kg -> g -> mg
v = 0.0450 * 1000 * 1000
eq(sci(v, 3), "4.50 &times; 10<sup>4</sup>")
eq(sf(0.0450 * 1000, 3), "45.0")
eq(sci(0.0450 / 1000 / 1000, 3), "4.50 &times; 10<sup>&minus;8</sup>")
eq(sci(v, 2), "4.5 &times; 10<sup>4</sup>")
ITEMS.append(dict(
    t="ch01-multistep",
    q="A student weighs out 0.0450 kg of table salt for a class demonstration. What is this mass in milligrams?",
    c=["4.50 &times; 10<sup>4</sup> mg", "45.0 mg", "4.50 &times; 10<sup>&minus;8</sup> mg", "4.5 &times; 10<sup>4</sup> mg"],
    y=["Going through the base unit: kg &rarr; g (&times; 1000), then g &rarr; mg (&times; 1000). The answer keeps the 3 significant figures of 0.0450, including the trailing zero.",
       "This stops after the first step: 0.0450 kg is 45.0 <i>grams</i>. You still need the second factor, 1000 mg / 1 g.",
       "Both factors were put in upside down, so the number got smaller. A milligram is far smaller than a kilogram, so the number of milligrams must be much bigger.",
       "The setup is right, but 0.0450 has 3 significant figures (the trailing zero after the decimal point counts). Write 4.50, not 4.5."],
    h="Go through the base unit: kg &rarr; g &rarr; mg. Each step uses 1000 from the prefix table.",
    w="0.0450 kg &times; (1000 g / 1 kg) &times; (1000 mg / 1 g) = 45,000 mg = <b>4.50 &times; 10<sup>4</sup> mg</b>. Both factors are exact, so the 3 significant figures of 0.0450 kg carry through. Check: a kilogram is a million milligrams, so the number gets a million times bigger.",
    d=2, k=0))

# M2 ms -> s -> us
v = 25 / 1000 * 1e6
eq(sci(v, 2), "2.5 &times; 10<sup>4</sup>")
eq(sci(25 * 100, 2), "2.5 &times; 10<sup>3</sup>")
eq(sci(25 * 1e6, 2), "2.5 &times; 10<sup>7</sup>")
eq(sci(25 / 1000, 2), "2.5 &times; 10<sup>&minus;2</sup>")
ITEMS.append(dict(
    t="ch01-multistep",
    q=MP + "A radiologic technologist sets an X-ray exposure time of 25 ms (milliseconds). What is this time in microseconds (&micro;s)?",
    c=["2.5 &times; 10<sup>4</sup> &micro;s", "2.5 &times; 10<sup>3</sup> &micro;s", "2.5 &times; 10<sup>7</sup> &micro;s", "2.5 &times; 10<sup>&minus;2</sup> &micro;s"],
    y=["ms &rarr; s (1000 ms = 1 s), then s &rarr; &micro;s (1 s = 10<sup>6</sup> &micro;s): 25 &divide; 1000 &times; 10<sup>6</sup> = 25,000 &micro;s, with 2 significant figures.",
       "This guesses 1 ms = 100 &micro;s. Prefix-to-prefix factors are not on the sheet; go through seconds and you get 1 ms = 1000 &micro;s.",
       "This multiplies by 10<sup>6</sup> straight from milliseconds, skipping the ms &rarr; s step. 10<sup>6</sup> &micro;s is one <i>second</i>, not one millisecond.",
       "This divides by 1000 as if a microsecond were larger than a millisecond. A microsecond is smaller, so there must be more of them."],
    h="Prefix A &rarr; base unit &rarr; prefix B. Start with 1 s / 1000 ms.",
    w="25 ms &times; (1 s / 1000 ms) &times; (10<sup>6</sup> &micro;s / 1 s) = <b>2.5 &times; 10<sup>4</sup> &micro;s</b> (25,000 &micro;s). Both factors are exact, so the answer keeps the 2 significant figures of 25 ms. Check: a microsecond is smaller than a millisecond, so the number must get bigger.",
    d=2, k=0))

# M3 ug/dL -> mg/L
v = 3.5 / 1e6 * 1000 * 10
eq(sf(v, 2), "0.035")
eq(sf(3.5 / 1e6 * 1000, 2), "0.0035")
eq(sci(3.5 / 1e6 * 1000 / 10, 2), "3.5 &times; 10<sup>&minus;4</sup>")
eq(sci(3.5 * 1000 * 10, 2), "3.5 &times; 10<sup>4</sup>")
ITEMS.append(dict(
    t="ch01-multistep",
    q=MP + "A clinical lab reports a child's blood lead level as 3.5 &micro;g/dL. A research study lists results in mg/L. What is this result in mg/L? (1 dL = 10<sup>&minus;1</sup> L, so 10 dL = 1 L.)",
    c=["0.035 mg/L", "0.0035 mg/L", "3.5 &times; 10<sup>&minus;4</sup> mg/L", "3.5 &times; 10<sup>4</sup> mg/L"],
    y=["Top: &micro;g &rarr; g &rarr; mg divides by 1000. Bottom: per dL &rarr; per L multiplies by 10. Overall 3.5 &divide; 100 = 0.035 mg/L (2 significant figures).",
       "Only the top unit was converted. &micro;g/dL &rarr; mg/L also needs the bottom changed: a liter holds 10 deciliters, so multiply by 10.",
       "The dL factor is upside down. dL is on the bottom of the given, so the next factor needs dL on top: 10 dL / 1 L.",
       "The microgram factor went the wrong way. A milligram is bigger than a microgram, so the number of milligrams must be smaller."],
    h="Do the top (&micro;g &rarr; g &rarr; mg) first, then the bottom (dL &rarr; L). A unit on the bottom cancels with a factor that has it on top.",
    w="3.5 &micro;g/dL &times; (1 g / 10<sup>6</sup> &micro;g) &times; (1000 mg / 1 g) &times; (10 dL / 1 L) = <b>0.035 mg/L</b>. All factors are exact; 3.5 has 2 significant figures. Check: &divide; 1000 for the top, &times; 10 for the bottom, so the number gets 100 times smaller.",
    d=3, k=1))

# M4 gal/min -> L/s
v = 450 * L_GAL / 60
eq(sf(v, 2), "28")
eq(sf(v, 3), "28.4")
eq(sf(450 / L_GAL / 60, 2), "2.0")
eq(sci(450 * L_GAL * 60, 2), "1.0 &times; 10<sup>5</sup>")
ITEMS.append(dict(
    t="ch01-multistep",
    q="An irrigation well on a Central Valley almond farm pumps 450 gal/min. What is this flow rate in liters per second? (1 gal = 3.785 L)",
    c=["28 L/s", "28.4 L/s", "2.0 L/s", "1.0 &times; 10<sup>5</sup> L/s"],
    y=["450 &times; 3.785 &divide; 60 = 28.39 L/s. 450 has no decimal point, so it has 2 significant figures: 28 L/s.",
       "The setup is right, but 450 (no decimal point) has only 2 significant figures, so the answer gets 2.",
       "The gallon factor is upside down (dividing by 3.785). A liter is smaller than a gallon, so there must be more liters than gallons.",
       "The time factor is upside down (multiplying by 60). Minutes are on the bottom, so the factor is 1 min / 60 s; the number per second must be smaller than the number per minute."],
    h="Top: gal &rarr; L. Bottom: min &rarr; s, with minutes on top of that factor so they cancel.",
    w="450 gal/min &times; (3.785 L / 1 gal) &times; (1 min / 60 s) = 28.39 L/s &rarr; <b>28 L/s</b>. 450 has 2 significant figures; 60 s = 1 min is exact. Check: one gallon a minute is a bit under 4 L a minute, and a second is 1/60 of a minute: 450 &times; 4 &divide; 60 &asymp; 30.",
    d=3, k=1))

# M5 L/min -> mL/s
v = 2.0 * 1000 / 60
eq(sf(v, 2), "33")
eq(sf(v, 3), "33.3")
eq(sci(2.0 * 1000 * 60, 2), "1.2 &times; 10<sup>5</sup>")
eq(sci(2.0 / 1000 / 60, 2), "3.3 &times; 10<sup>&minus;5</sup>")
ITEMS.append(dict(
    t="ch01-multistep",
    q=MP + "A respiratory therapist sets a nasal cannula to deliver oxygen at 2.0 L/min. What is this flow in mL/s?",
    c=["33 mL/s", "33.3 mL/s", "1.2 &times; 10<sup>5</sup> mL/s", "3.3 &times; 10<sup>&minus;5</sup> mL/s"],
    y=["2.0 &times; 1000 &divide; 60 = 33.33 mL/s. 2.0 has 2 significant figures, so 33 mL/s.",
       "The setup is right, but 2.0 L/min has only 2 significant figures; 1000 and 60 are exact and do not count.",
       "The minutes factor is upside down (multiplying by 60). Flow per second must be smaller than flow per minute.",
       "The liter factor is upside down (dividing by 1000). A milliliter is smaller than a liter, so there must be more of them."],
    h="Top: L &rarr; mL. Bottom: min &rarr; s. Ask: should the number per second be bigger or smaller than per minute?",
    w="2.0 L/min &times; (1000 mL / 1 L) &times; (1 min / 60 s) = 33.33 mL/s &rarr; <b>33 mL/s</b> (2 significant figures). Check: 2000 mL each minute spread over 60 seconds is about 33 mL each second.",
    d=2, k=1))

# M6 ft/s -> km/h
v = 3.2 * 12 * CM_IN / 100 / 1000 * 60 * 60
eq(sf(v, 2), "3.5")
eq(sf(v, 3), "3.51")
eq(sf(3.2 * CM_IN / 100 / 1000 * 3600, 2), "0.29")
eq(sci(3.2 * 12 * CM_IN / 100 / 1000 / 3600, 2), "2.7 &times; 10<sup>&minus;7</sup>")
ITEMS.append(dict(
    t="ch01-multistep",
    q="Water in a Central Valley irrigation canal flows at 3.2 ft/s. What is this speed in km/h? (1 ft = 12 in; 1 in = 2.54 cm, exact)",
    c=["3.5 km/h", "3.51 km/h", "0.29 km/h", "2.7 &times; 10<sup>&minus;7</sup> km/h"],
    y=["Distance first: ft &rarr; in &rarr; cm &rarr; m &rarr; km; then time: s &rarr; min &rarr; h (&times; 60 &times; 60). 3.2 &times; 12 &times; 2.54 &divide; 100 &divide; 1000 &times; 3600 = 3.511, which rounds to 3.5 km/h.",
       "The chain is right, but 3.2 ft/s has 2 significant figures, and every factor here is exact. Round once, at the end, to 3.5.",
       "The 12 in / 1 ft step was skipped, so feet were treated as inches. Write every factor in the chain; each one cancels the unit the one before it made.",
       "The time factors are upside down (dividing by 3600). Seconds are on the bottom, so the factor needs seconds on top: 60 s / 1 min, then 60 min / 1 h."],
    h="Do all the distance factors first, then the time factors. Seconds are on the bottom of the given, so they cancel with a factor that has seconds on top.",
    w="3.2 ft/s &times; (12 in / 1 ft) &times; (2.54 cm / 1 in) &times; (1 m / 100 cm) &times; (1 km / 1000 m) &times; (60 s / 1 min) &times; (60 min / 1 h) = 3.511 km/h &rarr; <b>3.5 km/h</b>. All factors are exact, so the 2 significant figures of 3.2 set the answer.",
    d=3, k=1))

# M7 which setup (g/L -> mg/mL)
v0 = 8.5 * 1000 / 1000
eq(sf(v0, 2), "8.5")
eq(sci(8.5 * 1000 * 1000, 2), "8.5 &times; 10<sup>6</sup>")
eq(sci(8.5 / 1000 / 1000, 2), "8.5 &times; 10<sup>&minus;6</sup>")
ITEMS.append(dict(
    t="ch01-multistep",
    q="A lab technician has a protein stock solution at 8.5 g/L and needs its concentration in mg/mL. Which setup is correct?",
    c=["8.5 g/L &times; (1000 mg / 1 g) &times; (1 L / 1000 mL)",
       "8.5 g/L &times; (1000 mg / 1 g) &times; (1000 mL / 1 L)",
       "8.5 g/L &times; (1 g / 1000 mg) &times; (1 L / 1000 mL)",
       "8.5 g/L &times; (1000 mg / 1 g)"],
    y=["Grams (top) cancel with grams on the bottom of the first factor; liters (bottom) cancel with liters on top of the second. The result is 8.5 mg/mL.",
       "The volume factor is upside down. L is on the bottom of the given, so the factor needs L on top; here L would be left as L<sup>2</sup> on the bottom.",
       "The mass factor is upside down: g on top of the given needs g on the bottom of the factor. Here grams do not cancel at all.",
       "Only the top unit was converted; this gives 8500 mg/L. A concentration needs both its top and its bottom unit changed."],
    h="Check each factor: is the unit you want to cancel on the opposite side of where it sits in the given?",
    w="g is on top, so use 1000 mg / 1 g; L is on the bottom, so use 1 L / 1000 mL: <b>8.5 g/L &times; (1000 mg / 1 g) &times; (1 L / 1000 mL)</b> = 8.5 mg/mL. The two factors of 1000 cancel, so g/L and mg/mL are the same number.",
    d=2, k=0))

# M8 mg/min -> mcg/h
v = 0.80 / 1000 * 1e6 * 60
eq(sci(v, 2), "4.8 &times; 10<sup>4</sup>")
eq(sf(0.80 * 1000 / 60, 2), "13")
eq(sf(0.80 / 1000 * 60, 2), "0.048")
eq(sci(0.80 * 1000, 2), "8.0 &times; 10<sup>2</sup>")
ITEMS.append(dict(
    t="ch01-multistep",
    q=MP + "An IV pump delivers a drug at 0.80 mg/min. The pharmacy record lists the rate in micrograms per hour (mcg/h; mcg is the health-care symbol for &micro;g). What is the rate in mcg/h?",
    c=["4.8 &times; 10<sup>4</sup> mcg/h", "13 mcg/h", "0.048 mcg/h", "8.0 &times; 10<sup>2</sup> mcg/h"],
    y=["Top: mg &rarr; g &rarr; mcg (&times; 1000). Bottom: per min &rarr; per h (&times; 60). 0.80 &times; 1000 &times; 60 = 48,000 mcg/h (2 significant figures).",
       "The time factor is upside down (dividing by 60). A pump delivers more in an hour than in a minute.",
       "The mass factor went the wrong way (dividing by 1000). A microgram is smaller than a milligram, so there are more of them.",
       "Only the top unit was converted: 800 mcg is the amount per <i>minute</i>. The bottom (min &rarr; h) must change too."],
    h="Top: mg &rarr; g &rarr; mcg. Bottom: min &rarr; h, with minutes on top of that factor.",
    w="0.80 mg/min &times; (1 g / 1000 mg) &times; (10<sup>6</sup> mcg / 1 g) &times; (60 min / 1 h) = 48,000 mcg/h = <b>4.8 &times; 10<sup>4</sup> mcg/h</b>. Scientific notation shows the 2 significant figures of 0.80. Check: 800 mcg each minute for 60 minutes is about 50,000 mcg.",
    d=3, k=1))

# ---------------------------------------------------------------- ch01-powers (1.4.3)

# P1 equality
eq((10) ** 3, 1000)
ITEMS.append(dict(
    t="ch01-powers",
    q="Since 1 cm = 10 mm, which equality is correct?",
    c=["1 cm<sup>3</sup> = 1000 mm<sup>3</sup>", "1 cm<sup>3</sup> = 10 mm<sup>3</sup>", "1 cm<sup>3</sup> = 100 mm<sup>3</sup>", "1 cm<sup>3</sup> = 30 mm<sup>3</sup>"],
    y=["A 1 cm cube is 10 mm on each side: 10 mm &times; 10 mm &times; 10 mm = 1000 mm<sup>3</sup>.",
       "This cubes the unit but not the number. Raise the whole factor to the power: (10 mm)<sup>3</sup> = 10<sup>3</sup> mm<sup>3</sup>.",
       "10<sup>2</sup> = 100 is the factor for <i>area</i> (cm<sup>2</sup> to mm<sup>2</sup>). A volume has three lengths, so cube it.",
       "This multiplies by the power (10 &times; 3) instead of raising to it. 10<sup>3</sup> means 10 &times; 10 &times; 10."],
    h="Picture a cube 1 cm on each side. How many millimeters is each edge, and how do you get a volume from three edges?",
    w="(10 mm / 1 cm)<sup>3</sup> = 10<sup>3</sup> mm<sup>3</sup> / 1 cm<sup>3</sup>, so <b>1 cm<sup>3</sup> = 1000 mm<sup>3</sup></b>. A grid of 10 &times; 10 &times; 10 tiny 1 mm cubes fills the 1 cm cube.",
    d=1, k=0))

# P2 dental cartridge mL -> mm3
v = 1.8 * 10 ** 3
eq(sci(v, 2), "1.8 &times; 10<sup>3</sup>")
eq(sf(1.8 * 10, 2), "18")
eq(sci(1.8 * 10 ** 2, 2), "1.8 &times; 10<sup>2</sup>")
eq(sci(1.8 / 10 ** 3, 2), "1.8 &times; 10<sup>&minus;3</sup>")
ITEMS.append(dict(
    t="ch01-powers",
    q="<b>Context only; a math example.</b> A dental anesthetic cartridge holds 1.8 mL. What is this volume in cubic millimeters (mm<sup>3</sup>)? (1 mL = 1 cm<sup>3</sup>; 1 cm = 10 mm)",
    c=["1.8 &times; 10<sup>3</sup> mm<sup>3</sup>", "18 mm<sup>3</sup>", "1.8 &times; 10<sup>2</sup> mm<sup>3</sup>", "1.8 &times; 10<sup>&minus;3</sup> mm<sup>3</sup>"],
    y=["1.8 mL = 1.8 cm<sup>3</sup>, and (10 mm / 1 cm)<sup>3</sup> = 1000 mm<sup>3</sup> per cm<sup>3</sup>: 1.8 &times; 1000 = 1800 mm<sup>3</sup>.",
       "The factor 10 mm / 1 cm was not cubed. A volume needs (10)<sup>3</sup>, not 10.",
       "The factor was squared (100), which is the area factor. Volume needs the cube, 10<sup>3</sup>.",
       "The cubed factor is upside down (dividing by 1000). A cubic millimeter is much smaller than a cubic centimeter, so there are more of them."],
    h="First mL &rarr; cm<sup>3</sup> (they are equal), then cube the whole factor 10 mm / 1 cm.",
    w="1.8 mL &times; (1 cm<sup>3</sup> / 1 mL) &times; (10 mm / 1 cm)<sup>3</sup> = 1.8 &times; 10<sup>3</sup> mm<sup>3</sup>, so <b>1.8 &times; 10<sup>3</sup> mm<sup>3</sup></b> (2 significant figures; the factors are exact).",
    d=2, k=0))

# P3 room ft2 -> m2
v = 180 * 12 ** 2 * CM_IN ** 2 / 100 ** 2
eq(sf(v, 2), "17")
eq(sf(v, 3), "16.7")
eq(sf(180 * 12 * CM_IN / 100, 2), "55")
eq(sci(180 * 12 ** 2 * CM_IN ** 2 / 100, 2), "1.7 &times; 10<sup>3</sup>")
ITEMS.append(dict(
    t="ch01-powers",
    q="A private hospital room has a floor area of 180 ft<sup>2</sup>. What is the area in m<sup>2</sup>? (1 ft = 12 in; 1 in = 2.54 cm, exact; 1 m = 100 cm)",
    c=["17 m<sup>2</sup>", "16.7 m<sup>2</sup>", "55 m<sup>2</sup>", "1.7 &times; 10<sup>3</sup> m<sup>2</sup>"],
    y=["Square every length factor: 180 &times; 12<sup>2</sup> &times; 2.54<sup>2</sup> &divide; 100<sup>2</sup> = 16.72 m<sup>2</sup>. 180 (no decimal point) has 2 significant figures: 17 m<sup>2</sup>.",
       "The setup is right, but 180 has only 2 significant figures (trailing zero, no decimal point).",
       "None of the factors was squared, so ft<sup>2</sup> never cancels. Each length factor must be squared, number and unit.",
       "The 12 and the 2.54 were squared, but the last factor (1 m / 100 cm) was not. Every factor in an area conversion gets squared."],
    h="Chain ft &rarr; in &rarr; cm &rarr; m, and put a power of 2 outside every factor.",
    w="180 ft<sup>2</sup> &times; (12 in / 1 ft)<sup>2</sup> &times; (2.54 cm / 1 in)<sup>2</sup> &times; (1 m / 100 cm)<sup>2</sup> = 16.72 m<sup>2</sup> &rarr; <b>17 m<sup>2</sup></b>. Check: a meter is a bit over 3 ft, so a square meter is about 10 ft<sup>2</sup>, and 180 &divide; 10 &asymp; 18.",
    d=3, k=1))

# P4 aquarium cm3 -> L
cm3 = 50.0 * 25.0 * 30.0
v = cm3 / 1000
eq(sf(v, 3), "37.5")
eq(sci(cm3, 3), "3.75 &times; 10<sup>4</sup>")
eq(sf(cm3 / 1e4, 3), "3.75")
eq(sf(cm3 / 1e6, 3), "0.0375")
ITEMS.append(dict(
    t="ch01-powers",
    q="A glass tank for a biology lab measures 50.0 cm &times; 25.0 cm &times; 30.0 cm on the inside. What volume does it hold, in liters? (1 L = 1000 cm<sup>3</sup>)",
    c=["37.5 L", "3.75 &times; 10<sup>4</sup> L", "3.75 L", "0.0375 L"],
    y=["V = 50.0 &times; 25.0 &times; 30.0 = 37,500 cm<sup>3</sup>, and 37,500 &divide; 1000 = 37.5 L (3 significant figures).",
       "This is the volume in cm<sup>3</sup> with the unit changed to L. Divide by 1000, since 1 L = 1000 cm<sup>3</sup>.",
       "This divides by 10<sup>4</sup> (the m<sup>2</sup>-to-cm<sup>2</sup> factor). The liter is defined as 1000 cm<sup>3</sup>, a cube 10 cm on a side.",
       "This divides by 10<sup>6</sup>, which gives cubic meters, not liters. 1 m<sup>3</sup> = 1000 L."],
    h="Length &times; width &times; height gives cm<sup>3</sup>. How many cm<sup>3</sup> are in one liter?",
    w="V = 50.0 cm &times; 25.0 cm &times; 30.0 cm = 37,500 cm<sup>3</sup>; 37,500 cm<sup>3</sup> &times; (1 L / 1000 cm<sup>3</sup>) = <b>37.5 L</b>. Each length has 3 significant figures. Check: about 10 gallons, a normal classroom tank.",
    d=2, k=1))

# P5 engine in3 -> L
v = 350 * CM_IN ** 3 / 1000
eq(sf(v, 2), "5.7")
eq(sf(v, 3), "5.74")
eq(sf(350 * CM_IN / 1000, 2), "0.89")
eq(sf(350 * CM_IN * 3 / 1000, 2), "2.7")
ITEMS.append(dict(
    t="ch01-powers",
    q="An older pickup truck on a Valley farm has a 350 in<sup>3</sup> engine (the total volume of its cylinders). What is this volume in liters? (1 in = 2.54 cm, exact; 1 L = 1000 cm<sup>3</sup>)",
    c=["5.7 L", "5.74 L", "0.89 L", "2.7 L"],
    y=["350 &times; 2.54<sup>3</sup> &divide; 1000 = 350 &times; 16.387 &divide; 1000 = 5.735 L. 350 has 2 significant figures: 5.7 L.",
       "The setup is right, but 350 (no decimal point) has only 2 significant figures.",
       "The factor 2.54 cm / 1 in was not cubed, so in<sup>3</sup> does not cancel. Use 2.54<sup>3</sup> = 16.387.",
       "This multiplies 2.54 by 3 (7.62) instead of cubing it. Use the x<sup>3</sup> or ^3 key: 2.54<sup>3</sup> = 16.387."],
    h="Cube the whole factor (2.54 cm / 1 in), then use 1 L = 1000 cm<sup>3</sup>.",
    w="350 in<sup>3</sup> &times; (2.54 cm / 1 in)<sup>3</sup> &times; (1 L / 1000 cm<sup>3</sup>) = 5.735 L &rarr; <b>5.7 L</b> (2 significant figures from 350; 2.54 is exact).",
    d=3, k=1))

# P6 BSA cm2 -> m2
v = 8.4e3 / 100 ** 2
eq(sf(v, 2), "0.84")
eq(sf(8.4e3 / 100, 2), "84")
eq(sci(8.4e3 * 100 ** 2, 2), "8.4 &times; 10<sup>7</sup>")
eq(sf(8.4e3 / 100 ** 3, 2), "0.0084")
ITEMS.append(dict(
    t="ch01-powers",
    q="<b>Context only; a math example.</b> A unit-practice worksheet gives a child's body surface area as 8.4 &times; 10<sup>3</sup> cm<sup>2</sup>. Drug references list body surface area in m<sup>2</sup>. What is it in m<sup>2</sup>? (1 m = 100 cm)",
    c=["0.84 m<sup>2</sup>", "84 m<sup>2</sup>", "8.4 &times; 10<sup>7</sup> m<sup>2</sup>", "0.0084 m<sup>2</sup>"],
    y=["(1 m / 100 cm)<sup>2</sup> = 1 m<sup>2</sup> / 10<sup>4</sup> cm<sup>2</sup>, so 8400 &divide; 10,000 = 0.84 m<sup>2</sup>, a reasonable value for a school-age child.",
       "The factor 1 m / 100 cm was not squared (dividing by 100 only). Area needs 100<sup>2</sup> = 10<sup>4</sup>.",
       "The squared factor is upside down (multiplying by 10<sup>4</sup>). A square meter is much bigger than a square centimeter, so the number must get smaller.",
       "The factor was cubed (10<sup>6</sup>). Area has two dimensions, so square it."],
    h="Square the whole factor 1 m / 100 cm, number and unit.",
    w="8.4 &times; 10<sup>3</sup> cm<sup>2</sup> &times; (1 m / 100 cm)<sup>2</sup> = 8.4 &times; 10<sup>3</sup> &divide; 10<sup>4</sup> = <b>0.84 m<sup>2</sup></b> (2 significant figures). Check: an average adult is about 1.7 to 2.0 m<sup>2</sup>, so a child under 1 m<sup>2</sup> makes sense.",
    d=2, k=0))

# P7 mm3 -> uL
mm3_in_mL = (0.1) ** 3
eq(round(mm3_in_mL * 1000, 9), 1.0)
eq(round(0.1 * 1000, 9), 100.0)
eq(round(0.1 ** 2 * 1000, 9), 10.0)
ITEMS.append(dict(
    t="ch01-powers",
    q="<b>Context only; a math example.</b> Older lab reports gave blood cell counts per cubic millimeter (mm<sup>3</sup>); most labs now report per microliter (&micro;L). How many microliters equal 1 mm<sup>3</sup>? (1 mm = 0.1 cm; 1 cm<sup>3</sup> = 1 mL)",
    c=["1 &micro;L", "100 &micro;L", "10 &micro;L", "0.001 &micro;L"],
    y=["1 mm<sup>3</sup> = (0.1 cm)<sup>3</sup> = 0.001 cm<sup>3</sup> = 0.001 mL = 1 &micro;L. That is why a count &ldquo;per mm<sup>3</sup>&rdquo; and &ldquo;per &micro;L&rdquo; is the same number.",
       "This uses 1 mm = 0.1 cm without cubing it (0.1 mL = 100 &micro;L). The whole factor must be cubed.",
       "This squares the factor (0.01 mL = 10 &micro;L). A volume needs the cube.",
       "This stops at 0.001 mL and writes &micro;L. One more step is needed: 0.001 mL &times; (1000 &micro;L / 1 mL)."],
    h="Cube 0.1 cm to get mm<sup>3</sup> in cm<sup>3</sup> (= mL), then go mL &rarr; L &rarr; &micro;L.",
    w="1 mm<sup>3</sup> &times; (0.1 cm / 1 mm)<sup>3</sup> = 10<sup>&minus;3</sup> cm<sup>3</sup> = 10<sup>&minus;3</sup> mL; 10<sup>&minus;3</sup> mL &times; (1 L / 1000 mL) &times; (10<sup>6</sup> &micro;L / 1 L) = <b>1 &micro;L</b>. A platelet count of 250,000/mm<sup>3</sup> is the same as 250,000/&micro;L.",
    d=2, k=0))

# P8 density g/cm3 -> kg/m3
v = 2.70 / 1000 * 100 ** 3
eq(sci(v, 3), "2.70 &times; 10<sup>3</sup>")
eq(sf(2.70 / 1000 * 100, 3), "0.270")
eq(sci(2.70 * 100 ** 3, 3), "2.70 &times; 10<sup>6</sup>")
eq(sci(2.70 / 1000 / 100 ** 3, 3), "2.70 &times; 10<sup>&minus;9</sup>")
ITEMS.append(dict(
    t="ch01-powers",
    q="Aluminum has a density of 2.70 g/cm<sup>3</sup>. Engineers often list densities in kg/m<sup>3</sup>. What is the density of aluminum in kg/m<sup>3</sup>?",
    c=["2.70 &times; 10<sup>3</sup> kg/m<sup>3</sup>", "0.270 kg/m<sup>3</sup>", "2.70 &times; 10<sup>6</sup> kg/m<sup>3</sup>", "2.70 &times; 10<sup>&minus;9</sup> kg/m<sup>3</sup>"],
    y=["Top: g &rarr; kg (&divide; 1000). Bottom: per cm<sup>3</sup> &rarr; per m<sup>3</sup> (&times; 10<sup>6</sup>, the cubed factor). 2.70 &times; 10<sup>6</sup> &divide; 1000 = 2.70 &times; 10<sup>3</sup> kg/m<sup>3</sup>.",
       "The factor 100 cm / 1 m was not cubed (&times; 100 instead of &times; 10<sup>6</sup>), so cm<sup>3</sup> does not cancel.",
       "The bottom was converted, but the top was left in grams. Change g &rarr; kg too.",
       "The cubed factor is upside down. cm<sup>3</sup> is on the bottom of the given, so the factor needs cm<sup>3</sup> on top: (100 cm / 1 m)<sup>3</sup>."],
    h="Do the top (g &rarr; kg) and the bottom (cm<sup>3</sup> &rarr; m<sup>3</sup>) separately. Cube the whole length factor.",
    w="2.70 g/cm<sup>3</sup> &times; (1 kg / 1000 g) &times; (100 cm / 1 m)<sup>3</sup> = <b>2.70 &times; 10<sup>3</sup> kg/m<sup>3</sup></b> (3 significant figures; the factors are exact). Check: a cubic meter of aluminum is a big block, so 2700 kg (about 3 tons) is reasonable.",
    d=3, k=1))

# ---------------------------------------------------------------- ch01-dosage (1.4.4)

# D1 stand-alone term
v = 68 * 2.0 / 50
eq(sf(v, 2), "2.7")
ITEMS.append(dict(
    t="ch01-dosage",
    q=MP + "A patient who weighs 68 kg has an order for 2.0 mg/kg of a drug. The vial on hand is labeled 50. mg/mL. To find the volume to draw up, which quantity should start the setup?",
    c=["68 kg (the body weight)", "2.0 mg/kg (the order)", "50. mg/mL (the label)", "mL (the unit of the answer)"],
    y=["The body weight is the only quantity that is not a ratio, so it stands alone and starts the setup. The order and the label are conversion factors that follow it.",
       "&ldquo;Per kg&rdquo; makes the order a conversion factor. It comes second, flipped so kg cancels the body weight.",
       "A slash makes the label a conversion factor. It comes last, with mg on the bottom so milligrams cancel.",
       "mL is the Desired unit; it is where the setup ends, not where it starts."],
    h="Which quantities are conversion factors (look for &ldquo;per&rdquo; or a slash)? What is left?",
    w="Start with <b>68 kg</b>, the term that stands alone: 68 kg &times; (2.0 mg / 1 kg) &times; (1 mL / 50. mg) = 2.72 mL &rarr; 2.7 mL (2 significant figures).",
    d=1, k=0))

# D2 distractor info (EMS drive)
v = 18 / 45 * 60
eq(sf(v, 2), "24")
eq(sf(18 / 45, 2), "0.40")
eq(sci(45 / 18 * 60, 2), "1.5 &times; 10<sup>2</sup>")
eq(sf(18 / 45 * 95, 2), "38")
ITEMS.append(dict(
    t="ch01-dosage",
    q="On a 95 &deg;F afternoon, an EMT drives an ambulance on a non-emergency transfer from a Fresno hospital to a care facility 18 mi away, at an average speed of 45 mi/h. How many minutes does the trip take?",
    c=["24 min", "0.40 min", "1.5 &times; 10<sup>2</sup> min", "38 min"],
    y=["18 mi &times; (1 h / 45 mi) &times; (60 min / 1 h) = 24 min. The temperature is a distractor.",
       "This stops at 0.40 <i>hours</i> and labels it minutes. Add 60 min / 1 h to finish.",
       "The speed factor is upside down (45 &divide; 18), so miles do not cancel. Put miles on the bottom: 1 h / 45 mi.",
       "This uses 95 (the temperature) as if it were a time factor. The temperature is not part of the path from miles to minutes."],
    h="Start with the distance (it stands alone). Which numbers are not needed at all?",
    w="18 mi &times; (1 h / 45 mi) &times; (60 min / 1 h) = <b>24 min</b> (2 significant figures). Check: 45 mi/h is three-quarters of a mile a minute, and 18 &divide; 0.75 = 24.",
    d=2, k=0))

# D3 tablets
v = 0.75 * 1000 / 250
eq(sf(v, 2), "3.0")
eq(sf(0.75 / 250, 2), "0.0030")
eq(sf(0.75 * 100 / 250, 2), "0.30")
eq(sci(250 / 0.75, 2), "3.3 &times; 10<sup>2</sup>")
ITEMS.append(dict(
    t="ch01-dosage",
    q=MP + "An order calls for 0.75 g of a drug. Each tablet on hand contains 250 mg. How many tablets make up the ordered amount?",
    c=["3.0 tablets", "0.0030 tablet", "0.30 tablet", "3.3 &times; 10<sup>2</sup> tablets"],
    y=["0.75 g &times; (1000 mg / 1 g) &times; (1 tablet / 250 mg) = 3.0 tablets (2 significant figures, set by 0.75 g).",
       "The grams were never converted to milligrams, so 0.75 was divided by 250 directly. The order and the label must be in the same unit first.",
       "This uses 100 mg = 1 g. Milli- means one-thousandth: 1 g = 1000 mg.",
       "The tablet factor is upside down (250 &divide; 0.75). Start with the order, then put mg on the bottom of the tablet factor."],
    h="The order is in grams and the label is in milligrams. Bridge them first.",
    w="0.75 g &times; (1000 mg / 1 g) &times; (1 tablet / 250 mg) = <b>3.0 tablets</b> (2 significant figures, from 0.75 g). Check: 0.75 g is 750 mg, three times 250 mg.",
    d=2, k=0))

# D4 oral liquid volume
v = 375 * 5.00 / 250.
eq(sf(v, 3), "7.50")
eq(sf(375 / 250., 3), "1.50")
eq(sf(250. * 5.00 / 375, 3), "3.33")
eq(sci(375 * 250. / 5.00, 3), "1.88 &times; 10<sup>4</sup>")
ITEMS.append(dict(
    t="ch01-dosage",
    q=MP + "An order calls for 375 mg of an antibiotic. The oral suspension on hand is labeled 250. mg per 5.00 mL. What volume holds the ordered amount?",
    c=["7.50 mL", "1.50 mL", "3.33 mL", "1.88 &times; 10<sup>4</sup> mL"],
    y=["375 mg &times; (5.00 mL / 250. mg) = 7.50 mL (3 significant figures).",
       "This divides 375 by 250 and stops; 1.50 is the number of 5.00 mL portions, not milliliters. Multiply by 5.00 mL.",
       "The setup started with the label instead of the order (250 &times; 5.00 &divide; 375). Start with the term that stands alone, the order.",
       "The label factor is upside down, so mg does not cancel. Put mg on the bottom: 5.00 mL / 250. mg."],
    h="Start with the order. Which way up must the label factor be so mg cancels?",
    w="375 mg &times; (5.00 mL / 250. mg) = <b>7.50 mL</b>. Check: 375 mg is 1.5 times 250 mg, so the volume is 1.5 &times; 5 mL = 7.5 mL.",
    d=2, k=1))

# D5 weight-based to volume
kg = 38.5 / LB
v = kg * 15 * 5.00 / 160
eq(sf(kg, 4), "17.46")
eq(sf(v, 2), "8.2")
eq(sf(v, 3), "8.19")
eq(sf(38.5 * 15 * 5.00 / 160, 2), "18")
eq(sf(38.5 * LB * 15 * 5.00 / 160, 2), "40")
ITEMS.append(dict(
    t="ch01-dosage",
    q=MP + "A child who weighs 38.5 lb has an order for 15 mg/kg of a fever reducer. The oral suspension is labeled 160 mg per 5.00 mL. What volume holds one dose? (1 kg = 2.2046 lb)",
    c=["8.2 mL", "8.19 mL", "18 mL", "40. mL"],
    y=["38.5 lb &rarr; 17.46 kg; &times; 15 mg/kg = 262.0 mg; &times; 5.00 mL / 160 mg = 8.19 mL. The order (15) and the label (160) have 2 significant figures, so 8.2 mL.",
       "The setup is right, but 15 mg/kg and 160 mg (no decimal point) have 2 significant figures each, so the answer gets 2.",
       "The pounds were never converted to kilograms. The order is per <i>kg</i>, so 38.5 lb must first become kg.",
       "The pound factor is upside down (multiplying by 2.2046). A kilogram is heavier than a pound, so the number of kilograms must be smaller."],
    h="Start with the weight. lb &rarr; kg &rarr; mg drug &rarr; mL. Label each unit with its substance (kg body, mg drug).",
    w="38.5 lb &times; (1 kg / 2.2046 lb) &times; (15 mg / 1 kg) &times; (5.00 mL / 160 mg) = 8.19 mL &rarr; <b>8.2 mL</b>. Check: 38.5 lb is about 17.5 kg; 17.5 &times; 15 &asymp; 260 mg, a bit over 1.5 times 160 mg, and 1.6 &times; 5 mL = 8 mL.",
    d=3, k=1))

# D6 inhaler (all counts exact)
eq(200 // (2 * 4), 25)
eq(200 // 4, 50)
eq(200 // 2, 100)
eq(200 * 2 * 4, 1600)
ITEMS.append(dict(
    t="ch01-dosage",
    q=MP + "A respiratory therapist teaches a patient to use an inhaler that holds 200 puffs. The order is 2 puffs, 4 times a day. How many days will the inhaler last?",
    c=["25 days", "50 days", "100 days", "1600 days"],
    y=["2 puffs &times; 4 times a day = 8 puffs a day; 200 puffs &times; (1 day / 8 puffs) = 25 days. Every number here is a count, so it is exact.",
       "This divides by the 4 uses a day but forgets that each use is 2 puffs. Include the per-dose multiplier.",
       "This divides by 2 puffs but forgets the 4 uses each day.",
       "This multiplies instead of dividing (200 &times; 8). The number of puffs per day must be on the bottom so puffs cancel."],
    h="First build a new conversion factor: puffs per day. Then start with the 200 puffs.",
    w="(2 puffs / 1 use) &times; (4 uses / 1 day) = 8 puffs / 1 day. 200 puffs &times; (1 day / 8 puffs) = <b>25 days</b>. Counted numbers are exact, so no rounding is needed.",
    d=2, k=0))

# D7 two stand-alone terms
kg = 165 / LB
per_day = kg * 2.5 * 2
v = 1000 / per_day
eq(sf(per_day, 4), "374.2")
eq(sf(v, 2), "2.7")
eq(sf(1000 / (kg * 2.5), 2), "5.3")
eq(sf(1000 / (165 * 2.5 * 2), 2), "1.2")
eq(sf(1000 / (165 * LB * 2.5 * 2), 2), "0.55")
eq(sf(1000 / float(sf(per_day, 2)), 2), "2.7")  # rounding between parts would not change this one
ITEMS.append(dict(
    t="ch01-dosage",
    q=MP + "A patient who weighs 165 lb has an order for 2.5 mg/kg of a drug, twice a day. A vial contains 1.00 g of the drug. How many days will the vial last? (1 kg = 2.2046 lb)",
    c=["2.7 days", "5.3 days", "1.2 days", "0.55 day"],
    y=["Part 1: 165 lb &rarr; 74.84 kg &times; 2.5 mg/kg &times; 2 doses/day = 374.2 mg/day. Part 2: 1000 mg &times; (1 day / 374.2 mg) = 2.67 &rarr; 2.7 days (2 significant figures, from 2.5 mg/kg).",
       "This forgets &ldquo;twice a day&rdquo;; 5.3 is the number of <i>doses</i>, not days.",
       "The pounds were used as if they were kilograms. Convert 165 lb to kg before using the per-kg order.",
       "The pound factor is upside down (multiplying by 2.2046), which makes the patient seem to weigh 364 kg."],
    h="Two quantities stand alone (the weight and the vial). Use the weight to build mg per day, then use that factor with the vial.",
    w="Part 1: 165 lb &times; (1 kg / 2.2046 lb) &times; (2.5 mg / 1 kg &middot; dose) &times; (2 doses / 1 day) = 374.2 mg/day (do not round yet). Part 2: 1.00 g &times; (1000 mg / 1 g) &times; (1 day / 374.2 mg) = 2.67 days &rarr; <b>2.7 days</b>.",
    d=3, k=1))

# D8 sodium in a sports drink (everyday)
v = 0.500 * 1000 * 110 / 240
eq(sci(v, 2), "2.3 &times; 10<sup>2</sup>")
eq(sf(v, 3), "229")
eq(sf(0.500 * 110 / 240, 2), "0.23")
eq(sci(0.500 * 1000 * 240 / 110, 2), "1.1 &times; 10<sup>3</sup>")
ITEMS.append(dict(
    t="ch01-dosage",
    q="A 0.500 L bottle of a sports drink has a label that says each 240 mL serving contains 110 mg of sodium. How many milligrams of sodium are in the whole bottle?",
    c=["2.3 &times; 10<sup>2</sup> mg", "229 mg", "0.23 mg", "1.1 &times; 10<sup>3</sup> mg"],
    y=["0.500 L &times; (1000 mL / 1 L) &times; (110 mg sodium / 240 mL drink) = 229.2 mg. 110 and 240 (no decimal points) have 2 significant figures: 2.3 &times; 10<sup>2</sup> mg.",
       "The setup is right, but 110 and 240 have only 2 significant figures. Scientific notation shows 2: 2.3 &times; 10<sup>2</sup> mg.",
       "The liters were never converted to milliliters, so L did not cancel the mL in the serving factor.",
       "The serving factor is upside down (240 mL / 110 mg), so mL does not cancel. Put mL on the bottom."],
    h="Start with the bottle (it stands alone). Convert L to mL so it matches the serving size.",
    w="0.500 L &times; (1000 mL / 1 L) &times; (110 mg sodium / 240 mL drink) = 229.2 mg &rarr; <b>2.3 &times; 10<sup>2</sup> mg</b>. Check: the bottle is about two servings (500 &divide; 240 &asymp; 2), and 2 &times; 110 &asymp; 220 mg.",
    d=2, k=1))

# D9 IV drip rate
v = 600. / (5.00 * 60) * 10
eq(sf(v, 3), "20.0")
eq(sci(600. / 5.00 * 10, 3), "1.20 &times; 10<sup>3</sup>")
eq(sf(600. / (5.00 * 60) / 10, 3), "0.200")
eq(sf(600. / (5.00 * 60), 3), "2.00")
ITEMS.append(dict(
    t="ch01-dosage",
    q=MP + "A nurse is to infuse 600. mL of IV fluid over 5.00 h by gravity. The tubing delivers 10 drops per mL (a defined tubing calibration, exact). What drip rate, in drops per minute, is needed?",
    c=["20.0 drops/min", "1.20 &times; 10<sup>3</sup> drops/min", "0.200 drop/min", "2.00 drops/min"],
    y=["600. mL / 5.00 h &times; (1 h / 60 min) &times; (10 drops / 1 mL) = 20.0 drops/min.",
       "The hours were never converted to minutes; 1200 is the number of drops per <i>hour</i>.",
       "The drop factor is upside down (dividing by 10). mL is on top of the rate, so the factor needs mL on the bottom: 10 drops / 1 mL.",
       "This stops at 2.00 mL/min. One more factor, 10 drops / 1 mL, turns milliliters into drops."],
    h="Write the rate 600. mL / 5.00 h, then change the bottom to minutes and the top to drops.",
    w="(600. mL / 5.00 h) &times; (1 h / 60 min) &times; (10 drops / 1 mL) = <b>20.0 drops/min</b> (3 significant figures; 60 and 10 are exact). Check: 120 mL each hour is 2 mL each minute, and 2 mL is 20 drops.",
    d=3, k=1))

# D10 mcg/kg/min -> mg/h
v = 5.0 * 80.0 * 60 / 1000
eq(sf(v, 2), "24")
eq(sf(5.0 * 80.0 / 1000, 2), "0.40")
eq(sf(5.0 * 60 / 1000, 2), "0.30")
eq(sci(5.0 * 80.0 * 60 * 1000, 2), "2.4 &times; 10<sup>7</sup>")
ITEMS.append(dict(
    t="ch01-dosage",
    q=MP + "An order reads 5.0 mcg/kg/min (micrograms per kilogram of body weight per minute) for a patient who weighs 80.0 kg. The pump is programmed in mg/h. What rate does the order describe, in mg/h?",
    c=["24 mg/h", "0.40 mg/h", "0.30 mg/h", "2.4 &times; 10<sup>7</sup> mg/h"],
    y=["80.0 kg &times; 5.0 mcg/(kg&middot;min) = 400 mcg/min; &times; 60 min/h = 24,000 mcg/h; &divide; 1000 = 24 mg/h (2 significant figures, from 5.0).",
       "This stops at mg per <i>minute</i>. Multiply by 60 min / 1 h to get per hour.",
       "The body weight was left out. The order is per kg, so it must be multiplied by the patient's 80.0 kg.",
       "The mcg factor is upside down (multiplying by 1000). A milligram is larger than a microgram, so the number must get smaller."],
    h="Start with the weight. Then mcg &rarr; mg on top and min &rarr; h on the bottom.",
    w="80.0 kg &times; (5.0 mcg / 1 kg&middot;min) &times; (60 min / 1 h) &times; (1 mg / 1000 mcg) = <b>24 mg/h</b>. Check: 400 mcg a minute is 0.4 mg a minute, and 0.4 &times; 60 = 24.",
    d=3, k=1))

# ---------------------------------------------------------------- ch01-percent (1.4.5)

# Pc1 decimal -> percent
eq(sf(0.874 * 100, 3), "87.4")
eq(sf(0.874 * 10, 3), "8.74")
eq(sf(0.874 * 1000, 3), "874")
ITEMS.append(dict(
    t="ch01-percent",
    q="A student's lab report gives the fraction of product recovered as 0.874. What is this as a percent?",
    c=["87.4%", "0.874%", "8.74%", "874%"],
    y=["Decimal to percent: multiply by 100 (move the decimal point two places right): 0.874 &times; 100 = 87.4%.",
       "The % sign was added without multiplying by 100. 0.874% would mean less than 1 part in 100.",
       "The decimal point moved only one place (&times; 10). A percent is out of 100, so move it two places.",
       "The decimal point moved three places (&times; 1000). Percent means out of 100, not out of 1000."],
    h="Percent means &ldquo;out of 100.&rdquo; Going from a decimal to a percent, multiply or divide by 100?",
    w="0.874 &times; 100 = <b>87.4%</b>. Check: 0.874 is a bit less than 1 whole, and 87.4% is a bit less than 100%.",
    d=1, k=0))

# Pc2 percent as a conversion factor
ITEMS.append(dict(
    t="ch01-percent",
    q="Yellow brass is 67% copper by mass. Which conversion factor does this statement give?",
    c=["67 g copper / 100 g brass", "67 g brass / 100 g copper", "67 g copper / 33 g brass", "0.67 g copper / 100 g brass"],
    y=["Copper is the part and brass is the total: 67 g of copper in every 100 g of brass. It can also be flipped: 100 g brass / 67 g copper.",
       "The labels are swapped. The percent is of copper <i>in</i> brass, so copper (the part) goes with 67 and brass (the total) goes with 100.",
       "33 g is the mass of the other metals, not of the brass. A percent always compares the part with the total, 100 g of brass.",
       "This changes 67% to a decimal and also puts it over 100, counting the &ldquo;out of 100&rdquo; twice. Use 67 / 100 or 0.67 / 1, not both."],
    h="Which substance is the part, and which is the total? The total always goes with the 100.",
    w="67% copper by mass means <b>67 g copper / 100 g brass</b> (or 100 g brass / 67 g copper, flipped). Label both substances so you know which grams cancel.",
    d=1, k=0))

# Pc3 saline
v = 1.00 * 1000 * 0.90 / 100
eq(sf(v, 2), "9.0")
eq(sf(1.00 * 0.90 / 100, 2), "0.0090")
eq(sci(1.00 * 1000 * 0.90, 2), "9.0 &times; 10<sup>2</sup>")
eq(sci(1.00 * 1000 * 100 / 0.90, 2), "1.1 &times; 10<sup>5</sup>")
ITEMS.append(dict(
    t="ch01-percent",
    q=MP + "Normal saline is 0.90% sodium chloride, meaning 0.90 g of NaCl in every 100 mL of solution. How many grams of NaCl are in a 1.00 L IV bag of normal saline?",
    c=["9.0 g", "0.0090 g", "9.0 &times; 10<sup>2</sup> g", "1.1 &times; 10<sup>5</sup> g"],
    y=["1.00 L &times; (1000 mL / 1 L) &times; (0.90 g NaCl / 100 mL solution) = 9.0 g (2 significant figures, from 0.90).",
       "The liters were never converted to milliliters, so L did not cancel the mL in the percent factor.",
       "This multiplies by 0.90 as a plain number. The percent factor is 0.90 g / 100 mL; leaving out the 100 makes the answer 100 times too big.",
       "The percent factor is upside down (100 mL / 0.90 g), so mL does not cancel and the units come out wrong."],
    h="Write 0.90% as a fraction over 100 mL with both units labeled, then start with the bag volume.",
    w="1.00 L &times; (1000 mL / 1 L) &times; (0.90 g NaCl / 100 mL solution) = <b>9.0 g NaCl</b>. Check: 1 L is ten 100 mL portions, and 10 &times; 0.90 g = 9.0 g.",
    d=2, k=0))

# Pc4 gold (flip the factor)
v = 35.0 * 100 / 58.3
eq(sf(v, 3), "60.0")
eq(sf(35.0 * 58.3 / 100, 3), "20.4")
eq(sci(35.0 * 58.3, 3), "2.04 &times; 10<sup>3</sup>")
eq(sf(35.0 * 100 / (100 - 58.3), 3), "83.9")
ITEMS.append(dict(
    t="ch01-percent",
    q="14-karat gold is 58.3% gold by mass. A jeweler has 35.0 g of pure gold. What is the largest mass of 14-karat gold she can make with it?",
    c=["60.0 g", "20.4 g", "2.04 &times; 10<sup>3</sup> g", "83.9 g"],
    y=["Gold (the part) is given and the alloy (the total) is wanted, so flip the factor: 35.0 g gold &times; (100 g alloy / 58.3 g gold) = 60.0 g.",
       "The factor was not flipped: this finds 58.3% <i>of</i> 35.0 g. The total must come out larger than the part.",
       "This multiplies by 58.3 as a plain number, leaving out the 100.",
       "This uses 41.7% (the other metals) instead of 58.3% gold. The gold is the part that is given, so use the gold percent."],
    h="Is 35.0 g the part or the total? Then which way up must the percent factor be?",
    w="35.0 g gold &times; (100 g 14-karat gold / 58.3 g gold) = 60.03 g &rarr; <b>60.0 g</b> (3 significant figures). Check: gold is a bit more than half the alloy, so the alloy is a bit less than twice 35 g.",
    d=2, k=1))

# Pc5 mass percent from parts
v = 1.62 / 45.0 * 100
eq(sf(v, 3), "3.60")
eq(sf(1.62 / (45.0 - 1.62) * 100, 3), "3.73")
eq(sf(1.62 / 45.0, 3), "0.0360")
eq(sci(45.0 / 1.62 * 100, 3), "2.78 &times; 10<sup>3</sup>")
ITEMS.append(dict(
    t="ch01-percent",
    q="A student evaporates all the water from a 45.0 g sample of salt water and recovers 1.62 g of salt. What is the mass percent of salt in the sample?",
    c=["3.60%", "3.73%", "0.0360%", "2.78 &times; 10<sup>3</sup>%"],
    y=["Percent = part &divide; total &times; 100% = 1.62 g &divide; 45.0 g &times; 100% = 3.60%.",
       "This divides by the mass of the water (45.0 &minus; 1.62 = 43.38 g), the other part, instead of by the total sample.",
       "This is the decimal (0.0360) with a % sign added. Multiply by 100 to get a percent.",
       "The fraction is upside down (total &divide; part). A part can never be more than 100% of its whole."],
    h="Part &divide; total &times; 100%. Which mass is the whole sample?",
    w="% salt = (1.62 g salt / 45.0 g sample) &times; 100% = <b>3.60%</b> (3 significant figures). Check: seawater is about 3.5% dissolved salts, so this is close to seawater.",
    d=2, k=1))

# Pc6 hematocrit (volume percent)
v = 5.0 * 1000 * 42 / 100
eq(sci(v, 2), "2.1 &times; 10<sup>3</sup>")
eq(sf(5.0 * 42 / 100, 2), "2.1")
eq(sci(5.0 * 1000 * 42, 2), "2.1 &times; 10<sup>5</sup>")
eq(sci(5.0 * 1000 * 100 / 42, 2), "1.2 &times; 10<sup>4</sup>")
ITEMS.append(dict(
    t="ch01-percent",
    q=MP + "A patient's hematocrit is 42%, meaning red blood cells make up 42 mL of every 100 mL of blood. If the patient has 5.0 L of blood, what volume of red blood cells is that, in mL?",
    c=["2.1 &times; 10<sup>3</sup> mL", "2.1 mL", "2.1 &times; 10<sup>5</sup> mL", "1.2 &times; 10<sup>4</sup> mL"],
    y=["5.0 L &times; (1000 mL / 1 L) &times; (42 mL red cells / 100 mL blood) = 2100 mL = 2.1 &times; 10<sup>3</sup> mL (2 significant figures).",
       "This is 42% of 5.0, which is 2.1 <i>liters</i>; the unit was changed to mL without converting. Use 1000 mL / 1 L.",
       "This multiplies by 42 as a plain number, leaving out the 100.",
       "The percent factor is upside down (100 mL blood / 42 mL red cells). The part must come out smaller than the total, 5000 mL."],
    h="Convert the blood volume to mL, then use the percent with &ldquo;mL blood&rdquo; on the bottom.",
    w="5.0 L blood &times; (1000 mL / 1 L) &times; (42 mL red cells / 100 mL blood) = <b>2.1 &times; 10<sup>3</sup> mL</b>. Check: a bit less than half of 5000 mL is a bit less than 2500 mL.",
    d=3, k=1))

# Pc7 hydrocortisone cream
v = 28.4 * 1.0 / 100 * 1000
eq(sci(v, 2), "2.8 &times; 10<sup>2</sup>")
eq(sf(v, 3), "284")
eq(sf(28.4 * 1.0 / 100, 2), "0.28")
eq(sci(28.4 * 1.0 * 1000, 2), "2.8 &times; 10<sup>4</sup>")
ITEMS.append(dict(
    t="ch01-percent",
    q=MP + "A pharmacy technician checks a 28.4 g tube of 1.0% hydrocortisone cream (1.0% by mass). How many milligrams of hydrocortisone does the tube contain?",
    c=["2.8 &times; 10<sup>2</sup> mg", "284 mg", "0.28 mg", "2.8 &times; 10<sup>4</sup> mg"],
    y=["28.4 g cream &times; (1.0 g hydrocortisone / 100 g cream) &times; (1000 mg / 1 g) = 284 mg. 1.0% has 2 significant figures: 2.8 &times; 10<sup>2</sup> mg.",
       "The setup is right, but 1.0% has only 2 significant figures, so the answer gets 2.",
       "This is 0.284 <i>grams</i>, labeled mg. Add the factor 1000 mg / 1 g.",
       "This multiplies by 1.0 as a plain number and leaves out the 100 of the percent."],
    h="Write 1.0% as 1.0 g hydrocortisone / 100 g cream, then convert grams to milligrams.",
    w="28.4 g cream &times; (1.0 g hydrocortisone / 100 g cream) &times; (1000 mg / 1 g) = 284 mg &rarr; <b>2.8 &times; 10<sup>2</sup> mg</b>. Check: 1% of about 28 g is about 0.28 g, or 280 mg.",
    d=3, k=1))

# Pc8 soil: parts add to 100%
clay = 100 - 42.5 - 38.0
eq(sf(clay, 3), "19.5")
v = 250. * clay / 100
eq(sf(v, 3), "48.8")
eq(sf(250. * 42.5 / 100, 3), "106")
eq(sf(250. * 38.0 / 100, 3), "95.0")
eq(sci(250. * clay, 3), "4.88 &times; 10<sup>3</sup>")
ITEMS.append(dict(
    t="ch01-percent",
    q="A soil sample from a Central Valley field is 42.5% sand and 38.0% silt by mass; the rest is clay. What mass of clay is in 250. g of this soil?",
    c=["48.8 g", "106 g", "95.0 g", "4.88 &times; 10<sup>3</sup> g"],
    y=["The parts add to 100%, so clay = 100% &minus; 42.5% &minus; 38.0% = 19.5%. 250. g &times; (19.5 g clay / 100 g soil) = 48.75 &rarr; 48.8 g.",
       "This is the mass of <i>sand</i> (42.5%). The question asks for the clay, the part left over.",
       "This is the mass of <i>silt</i> (38.0%). Find the clay percent first: 100% minus the other two.",
       "This multiplies by 19.5 as a plain number, leaving out the 100."],
    h="The parts of a whole add to 100%. What percent is left for clay?",
    w="Clay = 100% &minus; 42.5% &minus; 38.0% = 19.5%. 250. g soil &times; (19.5 g clay / 100 g soil) = 48.75 g &rarr; <b>48.8 g clay</b> (3 significant figures). Check: about a fifth of 250 g is 50 g.",
    d=3, k=1))


# ---------------------------------------------------------------- format checks
if __name__ == "__main__":
    keys = {"ch01-multistep": 8, "ch01-powers": 8, "ch01-dosage": 10, "ch01-percent": 8}
    cnt = collections.Counter(q["t"] for q in ITEMS)
    assert dict(cnt) == keys, cnt
    allowed = {"b", "i", "sub", "sup", "br"}
    for n, q in enumerate(ITEMS):
        tag = "%s #%d" % (q["t"], n)
        assert len(q["c"]) == 4 and len(q["y"]) == 4, tag
        assert len(set(re.sub(r"\s+", " ", c).strip().lower() for c in q["c"])) == 4, tag
        assert q["d"] in (1, 2, 3) and q["k"] in (0, 1), tag
        assert all(str(q[k]).strip() for k in ("q", "h", "w")), tag
        assert "<b>" in q["w"], tag
        s = " ".join([q["q"], q["h"], q["w"]] + q["c"] + q["y"])
        assert not re.search(r"all of the above|none of the above", s, re.I), tag
        for t in re.findall(r"</?([a-z]+)\s*/?>", s):
            assert t in allowed, (tag, t)
        for t in ("b", "i", "sub", "sup"):
            assert s.count("<%s>" % t) == s.count("</%s>" % t), (tag, t)
        assert not re.search(r"&(?!(?:[a-zA-Z]+|#\d+);)", s), tag
        if q["q"].startswith(MP):
            pass
    clinical = sum(1 for q in ITEMS if q["q"].startswith(MP))
    print("items:", len(ITEMS), dict(cnt), "| health-care (Math practice line):", clinical)
    print("all asserts passed")
