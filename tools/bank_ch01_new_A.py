"""New Chapter 1 Try It items, writer A (2026-11-17).
Keys: ch01-scinot (1.2.1), ch01-sigcalc (1.3.2), ch01-read (1.3.3).
Every number is computed here and asserted against the answer choices. Run: python3 -I tools/bank_ch01_new_A.py
c[0] is always the correct answer; the merger adds ids.
"""
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_DOWN
import math
import re

MP = '<b>Math practice only; always follow the order and facility policy.</b> '


def sci(x, sf):
    """Decimal x -> 'A &times; 10<sup>B</sup>' with sf significant figures (round half up)."""
    x = D(str(x))
    e = x.adjusted()
    m = x.scaleb(-e).quantize(D(1).scaleb(-(sf - 1)), ROUND_HALF_UP)
    if m >= 10:
        e += 1
        m = x.scaleb(-e).quantize(D(1).scaleb(-(sf - 1)), ROUND_HALF_UP)
    return '%s &times; 10<sup>%s</sup>' % (m, str(e).replace('-', '&minus;'))


def sci_raw(a, e):
    """Write a given A part (string) and exponent as HTML."""
    return '%s &times; 10<sup>%s</sup>' % (a, str(e).replace('-', '&minus;'))


def rdp(x, places):
    """Round Decimal x to a number of decimal places (half up), as string."""
    return str(D(str(x)).quantize(D(1).scaleb(-places), ROUND_HALF_UP))


def rsf(x, sf):
    """Round Decimal x to sf significant figures in standard form, keeping placeholder zeros (commas for >= 10000)."""
    x = D(str(x))
    q = D(1).scaleb(x.adjusted() - sf + 1)
    r = x.quantize(q, ROUND_HALF_UP)
    if q >= 1:
        n = int(r)
        return '{:,}'.format(n) if n >= 10000 else str(n)
    return str(r)


def plain(x):
    """Standard-form string of a Decimal with no exponent."""
    return format(D(str(x)), 'f')


ITEMS = []

# ---------------------------------------------------------------- ch01-scinot (1.2.1 Scientific Notation)

# S1 large number, placeholder zeros dropped
v = D('1850000000')
ans = sci(v, 3)
assert ans == '1.85 &times; 10<sup>9</sup>'
ITEMS.append(dict(
    t='ch01-scinot',
    q='A Valley water district reports that its reservoir holds 1,850,000,000 gallons. Which shows this volume in scientific notation?',
    c=[ans + ' gal', sci_raw('1.85', -9) + ' gal', sci_raw('18.5', 8) + ' gal', sci_raw('1.850000000', 9) + ' gal'],
    y=['The decimal point hops nine places to the left to sit after the 1, so the exponent is +9. The trailing zeros are placeholders (no decimal point), so A keeps only 1.85.',
       'A big number gets a positive exponent. A negative exponent would mean a number smaller than 1.',
       '18.5 is not between 1 and 10. Move its decimal point one more place left and add 1 to the exponent.',
       'This keeps the placeholder zeros in A, claiming 10 significant figures. With no decimal point, the trailing zeros of 1,850,000,000 are not significant.'],
    h='Move the decimal point until exactly one nonzero digit is in front of it, and count the hops. Which zeros are only placeholders?',
    w='Hop the decimal point left until only the 1 is in front of it: 9 places, so the exponent is +9. The significant digits are 1, 8, and 5. Answer: <b>1.85 &times; 10<sup>9</sup> gal</b>.',
    d=1, k=0))

# S2 small number with a significant trailing zero
v = D('0.00020')
ans = sci(v, 2)
assert ans == '2.0 &times; 10<sup>&minus;4</sup>' and v == D('2.0E-4')
ITEMS.append(dict(
    t='ch01-scinot',
    q='A respiratory therapy textbook gives the diameter of one alveolus (an air sac in the lung) as 0.00020 m. Which is this length in scientific notation?',
    c=[ans + ' m', sci_raw('2', -4) + ' m', sci_raw('2.0', 4) + ' m', sci_raw('2.0', -3) + ' m'],
    y=['The decimal point moves four places right to sit after the 2, so the exponent is &minus;4. The final zero comes after a decimal point, so it is significant and stays: 2.0.',
       'This drops a significant zero. 0.00020 has 2 significant figures, so A must be 2.0.',
       'A number smaller than 1 gets a negative exponent. Typing 2.0 &times; 10<sup>4</sup> back into a calculator gives 20000, not 0.00020.',
       'This counts the three zeros after the decimal point instead of the hops. The decimal point must move four places to get past the 2.'],
    h='Count how many places the decimal point moves to land just after the first nonzero digit. Is the final zero significant?',
    w='Move the decimal point right past the 2: four places, so the exponent is &minus;4. The trailing zero after the decimal point is significant. Answer: <b>2.0 &times; 10<sup>&minus;4</sup> m</b>.',
    d=1, k=0))

# S3 back to standard form, negative exponent
v = D('3.5E-6')
ans = plain(v)
assert ans == '0.0000035'
assert plain(D('3.5E-7')) == '0.00000035' and plain(D('3.5E-5')) == '0.000035'
ITEMS.append(dict(
    t='ch01-scinot',
    q='<b>Context only; a math example.</b> A lab report lists a child\'s blood lead level as 3.5 &times; 10<sup>&minus;6</sup> g per deciliter. Which is the same value in standard form?',
    c=[ans + ' g/dL', '0.00000035 g/dL', '0.000035 g/dL', '3,500,000 g/dL'],
    y=['A negative exponent means a small number: move the decimal point six places left. The 3 lands in the sixth place after the decimal point.',
       'This writes six zeros after the decimal point, which moves it seven places. That is 3.5 &times; 10<sup>&minus;7</sup>.',
       'This moves the decimal point only five places. That is 3.5 &times; 10<sup>&minus;5</sup>.',
       'This moves the decimal point to the right, as for a positive exponent. A negative exponent means a number smaller than 1.'],
    h='Negative exponent, small number. Which way does the decimal point move, and in which place should the 3 land?',
    w='The exponent is &minus;6, so move the decimal point six places left. The 3 fills one of the six places, so five zeros come before it: <b>0.0000035 g/dL</b>. Check: typing 3.5E&minus;6 into the calculator gives 0.0000035.',
    d=1, k=0))

# S4 back to standard form, positive exponent
v = D('4.3E6')
ans = '{:,}'.format(int(v))
assert ans == '4,300,000'
assert int(D('4.3E5')) == 430000 and int(D('4.3E7')) == 43000000
ITEMS.append(dict(
    t='ch01-scinot',
    q='About 4.3 &times; 10<sup>6</sup> people live in the San Joaquin Valley. Which is this number in standard form?',
    c=[ans, '430,000', '43,000,000', '0.0000043'],
    y=['A positive exponent means a big number: move the decimal point six places right, filling with zeros. 4.3 million is 4,300,000.',
       'This moves the decimal point only five places, which is 4.3 &times; 10<sup>5</sup>.',
       'This writes six zeros after 43, but the 3 already used one of the six places. That is 4.3 &times; 10<sup>7</sup>.',
       'This moves the decimal point left, as for a negative exponent. A positive exponent means a number larger than 1.'],
    h='Positive exponent, big number. Move the decimal point right; the 3 uses up one of the places.',
    w='Move the decimal point six places right: 4.3 &rarr; 4,300,000. Answer: <b>4,300,000</b> people (4.3 million).',
    d=1, k=0))

# S5 trailing zeros measured: show 3 sig figs
ans = sci(D('1800'), 3)
assert ans == '1.80 &times; 10<sup>3</sup>'
ITEMS.append(dict(
    t='ch01-scinot',
    q='A nurse records a patient\'s 24-hour urine output as 1,800 mL, measured to <b>three</b> significant figures. How should it be written so that all three significant figures show?',
    c=[ans + ' mL', sci_raw('1.8', 3) + ' mL', sci_raw('1.800', 3) + ' mL', sci_raw('18.0', 2) + ' mL'],
    y=['Every digit in A counts. 1.80 has exactly three significant figures, and 10<sup>3</sup> keeps the size at 1,800.',
       '1.8 shows only 2 significant figures, the same as writing 1,800 with no decimal point.',
       '1.800 shows 4 significant figures, one more than was measured.',
       'This has three significant figures, but 18.0 is not between 1 and 10, so it is not proper scientific notation.'],
    h='Under this book\'s rule, 1,800 shows only 2 significant figures. In scientific notation, every digit in A counts.',
    w='Write A with exactly three digits: 1.80. The decimal point moved three places left, so the exponent is +3. Answer: <b>1.80 &times; 10<sup>3</sup> mL</b>.',
    d=2, k=0))

# S6 multiply, A needs adjusting
a = D('1.2') * D('8.5')
assert a == D('10.20')
prod = D('1.2E2') * D('8.5E3')
ans = sci(prod, 2)
assert ans == '1.0 &times; 10<sup>6</sup>'
w1 = sci_raw('1.0', 5)   # moved A's decimal point but subtracted 1 from the exponent
w2 = sci_raw('1.0', 7)   # multiplied exponents 2*3 = 6, then adjusted to 7
w3 = sci(prod, 3)        # kept 3 sig figs
assert w3 == '1.02 &times; 10<sup>6</sup>'
ITEMS.append(dict(
    t='ch01-scinot',
    q='A Valley almond orchard has 1.2 &times; 10<sup>2</sup> trees per acre on 8.5 &times; 10<sup>3</sup> acres. About how many trees are in the orchard?',
    c=[ans + ' trees', w1 + ' trees', w2 + ' trees', w3 + ' trees'],
    y=['1.2 &times; 8.5 = 10.2 and 2 + 3 = 5, giving 10.2 &times; 10<sup>5</sup>. Moving the decimal point of A one place left adds 1 to the exponent: 1.02 &times; 10<sup>6</sup>, rounded to 2 significant figures.',
       'Moving the decimal point of A to the left makes A smaller, so the exponent must go <b>up</b> by 1, not down.',
       'This multiplies the exponents (2 &times; 3 = 6). When you multiply numbers, you <b>add</b> the exponents.',
       'Both values have 2 significant figures, so the answer gets 2, not 3.'],
    h='Multiply the A parts and add the exponents. If the new A is 10 or more, adjust it and the exponent together.',
    w='(1.2 &times; 8.5) = 10.2, and 10<sup>2</sup> &times; 10<sup>3</sup> = 10<sup>5</sup>. Adjust: 10.2 &times; 10<sup>5</sup> = 1.02 &times; 10<sup>6</sup>. The acres cancel, leaving trees. Both values have 2 significant figures: <b>1.0 &times; 10<sup>6</sup> trees</b>.',
    d=2, k=1))

# S7 divide with a negative exponent in the denominator
quot = D('3.6E8') / D('9.0E-1')
ans = sci(quot, 2)
assert ans == '4.0 &times; 10<sup>8</sup>'
w1 = sci(D('3.6E8') / D('9.0E1'), 2)     # ignored the minus sign: 8 - 1 = 7
assert w1 == '4.0 &times; 10<sup>6</sup>'
w2 = sci_raw('4.0', 10)                  # 0.40 x 10^9 adjusted the wrong way
w3 = sci(D('9.0E-1') / D('3.6E8'), 2)    # divided upside down
assert w3 == '2.5 &times; 10<sup>&minus;9</sup>'
ITEMS.append(dict(
    t='ch01-scinot',
    q='A clinical laboratory scientist counts 3.6 &times; 10<sup>8</sup> bacteria in 9.0 &times; 10<sup>&minus;1</sup> mL of a broth culture. How many bacteria are in each milliliter?',
    c=[ans + ' bacteria/mL', w1 + ' bacteria/mL', w2 + ' bacteria/mL', w3 + ' bacteria/mL'],
    y=['3.6 &divide; 9.0 = 0.40 and 8 &minus; (&minus;1) = 9, giving 0.40 &times; 10<sup>9</sup>. Moving the decimal point of A one place right subtracts 1: 4.0 &times; 10<sup>8</sup>.',
       'This subtracts 8 &minus; 1 and ignores the minus sign on the &minus;1. Subtracting a negative exponent adds: 8 &minus; (&minus;1) = 9.',
       'Moving the decimal point of A to the right makes A bigger, so the exponent must go <b>down</b> by 1, not up.',
       'This divides milliliters by bacteria (the factor is upside down). Bacteria per milliliter puts bacteria on top.'],
    h='Divide the A parts and subtract the exponents, top minus bottom. Watch the sign of the bottom exponent.',
    w='3.6 &divide; 9.0 = 0.40, and 8 &minus; (&minus;1) = 9: 0.40 &times; 10<sup>9</sup>. Adjust A to be between 1 and 10: <b>4.0 &times; 10<sup>8</sup> bacteria/mL</b>. Check: dividing by a number smaller than 1 makes the answer bigger than 3.6 &times; 10<sup>8</sup>.',
    d=2, k=0))

# S8 calculator check of a wrong sign
typed = D('6.15E4')
assert plain(typed) == '61500'
assert sci(D('0.000615'), 3) == '6.15 &times; 10<sup>&minus;4</sup>'
ITEMS.append(dict(
    t='ch01-scinot',
    q='A pharmacy technician student writes 0.000615 L as 6.15 &times; 10<sup>4</sup> L, then types her answer back into a TI-36X Pro to check it. What does the calculator show, and what should she conclude?',
    c=['61500; the exponent should be &minus;4',
       '0.000615; the answer is correct',
       '0.0000615; the exponent should be &minus;5',
       '6150; the exponent should be 3'],
    y=['6.15 &times; 10<sup>4</sup> is a big number, 61500, not 0.000615. The decimal point moved four places right, so the exponent should be &minus;4: 6.15 &times; 10<sup>&minus;4</sup> L.',
       'The calculator shows what was typed, 6.15 &times; 10<sup>4</sup>, which is 61500. A positive exponent can never give a number smaller than 1.',
       'The calculator would show 61500 for a positive exponent. And 0.000615 needs four hops, so the exponent is &minus;4, not &minus;5.',
       'Typing 6.15 &times; 10<sup>4</sup> gives 61500, not 6150, and the problem is the sign of the exponent, not its size.'],
    h='Type 6.15, the &times;10<sup>n</sup> key, then 4, and press enter. Is the result big or small?',
    w='The calculator shows 61500, nowhere near 0.000615, so the sign is wrong. The decimal point in 0.000615 moves four places right, so the answer is 6.15 &times; 10<sup>&minus;4</sup> L. Answer: <b>61500; the exponent should be &minus;4</b>.',
    d=2, k=1))

# S9 platelets per liter -> per microliter
per_L = D('2.1E11')
per_uL = per_L / D('1E6')
ans = sci(per_uL, 2)
assert ans == '2.1 &times; 10<sup>5</sup>'
w1 = sci(per_L * D('1E6'), 2)   # multiplied by 10^6
assert w1 == '2.1 &times; 10<sup>17</sup>'
w2 = sci(per_L / D('1E3'), 2)   # used 1 L = 10^3 (that is per mL)
assert w2 == '2.1 &times; 10<sup>8</sup>'
ITEMS.append(dict(
    t='ch01-scinot',
    q='A lab reports a platelet count as 2.1 &times; 10<sup>11</sup> per liter. Which is the same count per microliter? (1 L = 10<sup>6</sup> &micro;L) (Context only; reference ranges vary by laboratory.)',
    c=[ans + ' per &micro;L', w1 + ' per &micro;L', w2 + ' per &micro;L', sci_raw('2.1', 11) + ' per &micro;L'],
    y=['A microliter is a millionth of a liter, so it holds 10<sup>6</sup> times fewer platelets: 11 &minus; 6 = 5.',
       'This adds 6 to the exponent. A microliter is much smaller than a liter, so the count per microliter must be smaller.',
       'This uses 10<sup>3</sup>, the number of milliliters in a liter. That gives the count per milliliter, not per microliter.',
       'This keeps the exponent and changes only the unit. Changing the unit changes the exponent: the same count per liter and per microliter differ by 10<sup>6</sup>.'],
    h='Is a microliter bigger or smaller than a liter? So should the count per microliter be bigger or smaller?',
    w='Divide by 10<sup>6</sup> &micro;L per liter: subtract 6 from the exponent. 2.1 &times; 10<sup>11</sup> &divide; 10<sup>6</sup> = <b>2.1 &times; 10<sup>5</sup> per &micro;L</b> (210,000 per microliter).',
    d=2, k=0))

# S10 rounding in scientific notation
v = D('2.0965E5')
ans = sci(v, 3)
assert ans == '2.10 &times; 10<sup>5</sup>'
assert sci(v, 2) == '2.1 &times; 10<sup>5</sup>' and sci(v, 4) == '2.097 &times; 10<sup>5</sup>'
trunc = (v.scaleb(-5)).quantize(D('0.01'), ROUND_DOWN)
assert str(trunc) == '2.09'
ITEMS.append(dict(
    t='ch01-scinot',
    q='A calculation of the number of yeast cells in a fermentation sample gives 2.0965 &times; 10<sup>5</sup> cells. Round it to <b>three</b> significant figures.',
    c=[ans + ' cells', sci(v, 2) + ' cells', sci_raw(str(trunc), 5) + ' cells', sci(v, 4) + ' cells'],
    y=['Underline the 9 (the third digit). The next digit is 6, so round up: 2.09 becomes 2.10. The zero stays because it is the third significant figure, and the power of ten comes down unchanged.',
       'This has only 2 significant figures. The zero after rounding up is significant and must be written.',
       'This chops off the extra digits without rounding. The digit after the 9 is a 6, so round up.',
       'This has 4 significant figures, one more than asked.'],
    h='Round only A. Underline the third digit and look at the one digit to its right.',
    w='In A = 2.0965, underline the third digit, 9. The next digit is 6, so round up: 2.09 &rarr; 2.10. Bring the power of ten down unchanged: <b>2.10 &times; 10<sup>5</sup> cells</b>.',
    d=1, k=0))

# S11 adjust A that is less than 1
v = D('0.52E-3')
ans = sci(v, 2)
assert ans == '5.2 &times; 10<sup>&minus;4</sup>'
ITEMS.append(dict(
    t='ch01-scinot',
    q='A calculation of a hormone concentration gives 0.52 &times; 10<sup>&minus;3</sup> g/L. Which is the same value in proper scientific notation?',
    c=[ans + ' g/L', sci_raw('5.2', -2) + ' g/L', sci_raw('52', -5) + ' g/L', sci_raw('5.2', -3) + ' g/L'],
    y=['A must be between 1 and 10. Moving the decimal point of 0.52 one place right makes A bigger, so subtract 1 from the exponent: &minus;3 &minus; 1 = &minus;4.',
       'This adds 1 to the exponent. Making A ten times bigger must make the power of ten ten times smaller.',
       '52 is not between 1 and 10, so this is not proper scientific notation (though the value is the same).',
       'This moves the decimal point of A but leaves the exponent alone, making the number ten times too big.'],
    h='Fix A first (0.52 &rarr; 5.2). A got ten times bigger, so what must happen to the exponent?',
    w='0.52 &rarr; 5.2 moves the decimal point one place right, so subtract 1 from the exponent: <b>5.2 &times; 10<sup>&minus;4</sup> g/L</b>. Check: both 0.52E&minus;3 and 5.2E&minus;4 display 0.00052.',
    d=2, k=0))

# S12 large count, two sig figs
v = D('25000000000000')
ans = sci(v, 2)
assert ans == '2.5 &times; 10<sup>13</sup>'
ITEMS.append(dict(
    t='ch01-scinot',
    q='An adult has about 25,000,000,000,000 red blood cells. Which is this count in scientific notation?',
    c=[ans + ' cells', sci_raw('2.5', 12) + ' cells', sci_raw('25', 12) + ' cells', sci_raw('2.5', -13) + ' cells'],
    y=['The decimal point hops 13 places left to sit after the 2. The trailing zeros are placeholders, so A is 2.5.',
       'This counts only the 12 zeros. The decimal point must also hop past the 5: 13 places.',
       '25 is not between 1 and 10. Move its decimal point one more place and add 1 to the exponent.',
       'A big number gets a positive exponent. 10<sup>&minus;13</sup> would mean a tiny fraction of one cell.'],
    h='Count the hops from the end of the number to just after the first digit, not the zeros.',
    w='Move the decimal point from the end of the number to just after the 2: 13 hops left, so the exponent is +13. Answer: <b>2.5 &times; 10<sup>13</sup> cells</b> (25 trillion).',
    d=1, k=0))

# ---------------------------------------------------------------- ch01-sigcalc (1.3.2 Significant Figures in Calculations)

# C1 multiply, area, round 5 up
area = D('12.5') * D('4.2')
assert area == D('52.50')
ans = rsf(area, 2)
assert ans == '53'
ITEMS.append(dict(
    t='ch01-sigcalc',
    q='A community garden plot in Clovis measures 12.5 m by 4.2 m. What is its area, with the correct significant figures and unit?',
    c=['53 m<sup>2</sup>', '52.5 m<sup>2</sup>', '52 m<sup>2</sup>', '53 m'],
    y=['12.5 &times; 4.2 = 52.5. 4.2 has 2 significant figures, so the answer gets 2: underline the 2 in the ones place; the next digit is 5, so round up to 53 m<sup>2</sup>.',
       'This keeps 3 significant figures, from 12.5. In multiplication, the value with the <b>fewest</b> significant figures (4.2, two) decides.',
       'The digit after the underlined 2 is a 5, and 5 to 9 rounds up, not down.',
       'Meters times meters is square meters. The unit is multiplied along with the numbers.'],
    h='Multiplying: count significant figures, not decimal places. And what is m &times; m?',
    w='12.5 m &times; 4.2 m = 52.5 m<sup>2</sup>. 12.5 has 3 significant figures and 4.2 has 2, so round to 2: <b>53 m<sup>2</sup></b>.',
    d=1, k=1))

# C2 divide, derived unit, significant trailing zero
c = D('2.45') / D('50.0')
assert c == D('0.049')
ans = rsf(c, 3)
assert ans == '0.0490'
inv = rsf(D('50.0') / D('2.45'), 3)
assert inv == '20.4'
ITEMS.append(dict(
    t='ch01-sigcalc',
    q='<b>Context only; a math example.</b> A pharmacy technician dissolves 2.45 g of a powder to make 50.0 mL of solution. What is the concentration in grams per milliliter?',
    c=['0.0490 g/mL', '0.049 g/mL', '0.04900 g/mL', inv + ' g/mL'],
    y=['2.45 g &divide; 50.0 mL = 0.049. Both values have 3 significant figures, so the answer needs 3: write the trailing zero, 0.0490 g/mL.',
       'The calculator shows 0.049, but that has only 2 significant figures. Both measurements have 3, so add the significant zero.',
       'This has 4 significant figures, one more than either measurement.',
       'This divides milliliters by grams (50.0 &divide; 2.45), which is mL/g, not g/mL. Grams per milliliter puts grams on top.'],
    h='Grams per milliliter: which number goes on top? Then count significant figures in each measurement.',
    w='2.45 g &divide; 50.0 mL = 0.049 g/mL on the calculator. Both values have 3 significant figures, so write 3: <b>0.0490 g/mL</b>.',
    d=2, k=1))

# C3 exact count does not limit
tot = 3 * D('0.125')
assert tot == D('0.375')
ITEMS.append(dict(
    t='ch01-sigcalc',
    q=MP + 'A patient takes 3 tablets, each containing 0.125 mg of a medication. What is the total dose, with the correct significant figures?',
    c=['0.375 mg', '0.4 mg', '0.38 mg', '0.3750 mg'],
    y=['The 3 is a count, so it is exact and does not limit the answer. 0.125 mg has 3 significant figures, so 3 &times; 0.125 = 0.375 mg keeps 3.',
       'This treats the count 3 as a measurement with 1 significant figure. Counted numbers are exact.',
       'This rounds to 2 significant figures for no reason; 0.125 mg has 3, and the 3 tablets are exact.',
       'This adds a zero that was never measured, claiming 4 significant figures.'],
    h='Is "3 tablets" a measurement or a count? Only measured values limit significant figures.',
    w='3 &times; 0.125 mg = 0.375 mg. The count (3) is exact, so 0.125 mg (3 significant figures) decides: <b>0.375 mg</b>.',
    d=1, k=0))

# C4 addition: a trailing decimal point means zero decimal places
s = D('250.') + D('12.75') + D('3.4')
assert s == D('266.15')
ans = rdp(s, 0)
assert ans == '266'
assert rdp(s, 1) == '266.2' and rsf(s, 2) == '270'
ITEMS.append(dict(
    t='ch01-sigcalc',
    q='A student combines 250. mL of water, 12.75 mL of a buffer, and 3.4 mL of an indicator solution. What total volume should she report?',
    c=['266 mL', '266.2 mL', '266.15 mL', '270 mL'],
    y=['When adding, the fewest decimal places wins. 250. mL is known only to the ones place (the decimal point shows the zero is significant, but there are no digits after it), so the total is reported to the ones place: 266 mL.',
       'This uses one decimal place, from 3.4 mL. But 250. mL has no decimal places, so it limits the answer to the ones place.',
       'This copies every digit from the calculator. The sum can be no more precise than its least precise measurement.',
       'This uses the multiplication rule (fewest significant figures, 2 from 3.4). Adding uses decimal places, not significant figures.'],
    h='Adding: line the numbers up at their decimal points. Which value stops soonest?',
    w='250. + 12.75 + 3.4 = 266.15 mL. Decimal places: 250. has none, 12.75 has two, 3.4 has one. Round to the ones place: <b>266 mL</b>.',
    d=2, k=0))

# C5 subtraction loses significant figures
diff = D('48.7') - D('46.28')
assert diff == D('2.42')
ans = rdp(diff, 1)
assert ans == '2.4'
ITEMS.append(dict(
    t='ch01-sigcalc',
    q='A nursing student weighs a wet wound dressing on a clinic scale (48.7 g). The same type of dressing, dry, has a mass of 46.28 g on a lab balance. What mass of fluid did the dressing absorb?',
    c=['2.4 g', '2.42 g', '2.420 g', '2.5 g'],
    y=['48.7 &minus; 46.28 = 2.42. In subtraction the fewest decimal places wins: 48.7 has one, so the answer has one: 2.4 g (only 2 significant figures).',
       'This uses the significant-figure rule (3 significant figures from 48.7). Subtraction uses decimal places, and 48.7 has only one.',
       'This adds a digit that neither measurement supports.',
       'The digit after the underlined 4 is a 2, so round down, not up.'],
    h='Subtracting: count decimal places, not significant figures. The answer can end up with fewer significant figures than either measurement.',
    w='48.7 g &minus; 46.28 g = 2.42 g. 48.7 has one decimal place and 46.28 has two, so keep one: <b>2.4 g</b>.',
    d=2, k=0))

# C6 match units before adding
tot_g = D('0.75') + D('436') / 1000
assert tot_g == D('1.186')
ans = rdp(tot_g, 2)
assert ans == '1.19'
raw = D('0.75') + D('436')
assert rdp(raw, 0) == '437'
assert rsf(tot_g, 2) == '1.2'
ITEMS.append(dict(
    t='ch01-sigcalc',
    q='A clinical lab technician mixes 0.75 g of one salt with 436 mg of another. What is the total mass in grams?',
    c=['1.19 g', '1.186 g', '437 g', '1.2 g'],
    y=['Convert first: 436 mg = 0.436 g. Then 0.75 + 0.436 = 1.186 g. 0.75 has two decimal places, so round to two: 1.19 g.',
       'This keeps three decimal places, from 0.436 g. 0.75 g has only two, so it limits the answer.',
       'This adds 436 and 0.75 as if they had the same unit. Milligrams must be converted to grams before adding.',
       'This uses the multiplication rule (2 significant figures from 0.75). Adding uses decimal places.'],
    h='Can grams and milligrams be added directly? Convert first, then use the addition rule.',
    w='436 mg &times; (1 g / 1000 mg) = 0.436 g. 0.75 g + 0.436 g = 1.186 g. Fewest decimal places is two (0.75): <b>1.19 g</b>.',
    d=2, k=0))

# C7 subtract then divide, underline, do not round early
top = D('58.44') - D('52.9')
assert top == D('5.54')
dens = top / D('4.42')
ans = rsf(dens, 2)
assert ans == '1.3'
early = rsf(D('5.5') / D('4.42'), 2)
assert early == '1.2'
three = rsf(dens, 3)
assert three == '1.25'
four = rsf(dens, 4)
assert four == '1.253'
ITEMS.append(dict(
    t='ch01-sigcalc',
    q='A pharmacy student finds the density of glycerin. The cylinder with glycerin has a mass of 58.44 g, the empty cylinder 52.9 g (weighed earlier on a less precise balance), and the glycerin\'s volume is 4.42 mL.<br />density = (58.44 g &minus; 52.9 g) &divide; 4.42 mL<br />What density should she report?',
    c=['1.3 g/mL', '1.2 g/mL', '1.25 g/mL', '1.253 g/mL'],
    y=['Top first: 58.44 &minus; 52.9 = 5.54 g, one decimal place, so underline the 5 in the tenths place (2 significant figures). Keep 5.54 and divide: 5.54 &divide; 4.42 = 1.253. Two significant figures: 1.3 g/mL.',
       'This rounds the top to 5.5 g before dividing: 5.5 &divide; 4.42 = 1.244, which rounds to 1.2. Rounding in the middle changed the last digit. Underline, do not round.',
       'This gives 3 significant figures, as if 5.54 g had 3. The subtraction left only one decimal place, so the top has just 2 significant figures.',
       'This copies too many digits from the calculator. The top (2 significant figures) limits the answer.'],
    h='Finish the top first and underline its last significant digit, but keep every digit in the calculator. Round once, at the end.',
    w='Top: 58.44 &minus; 52.9 = 5.54 g; one decimal place, so 2 significant figures (underline the 5 in the tenths place). Divide: 5.54 &divide; 4.42 mL = 1.2534 g/mL. 2 significant figures: <b>1.3 g/mL</b>.',
    d=3, k=1))

# C8 average with an exact count
s = D('104') + D('101') + D('108')
assert s == D('313')
avg = s / 3
ans = rsf(avg, 3)
assert ans == '104'
assert rdp(avg, 1) == '104.3' and rdp(avg, 2) == '104.33' and rsf(avg, 1) == '100'
ITEMS.append(dict(
    t='ch01-sigcalc',
    q='Fresno has daily high temperatures of 104 &deg;F, 101 &deg;F, and 108 &deg;F over three July days. What is the average high?',
    c=['104 &deg;F', '104.3 &deg;F', '104.33 &deg;F', '100 &deg;F'],
    y=['Add first: 313, known to the ones place (3 significant figures). Divide by the count 3, which is exact: 104.33 rounds to 3 significant figures, 104 &deg;F.',
       'This keeps a tenths digit. The readings and their sum are known only to the ones place, so the sum has 3 significant figures and so does the average.',
       'This copies the calculator. Each temperature was recorded only to the ones place.',
       'This treats the count 3 as a measurement with 1 significant figure. The number of days is exact.'],
    h='Add first (top of the fraction), then divide. Is the 3 a measurement or a count?',
    w='(104 + 101 + 108) &divide; 3 = 313 &divide; 3 = 104.33. The sum has 3 significant figures and 3 is exact, so the average has 3: <b>104 &deg;F</b>.',
    d=2, k=1))

# C9 exponent: cube, unit cubed
vol = D('2.05') ** 3
assert vol == D('8.615125')
ans = rsf(vol, 3)
assert ans == '8.62'
assert rsf(D('2.05') * 3, 3) == '6.15'
ITEMS.append(dict(
    t='ch01-sigcalc',
    q='A cube of aluminum in the lab has an edge length of 2.05 cm. What is its volume? (volume of a cube = edge<sup>3</sup>)',
    c=['8.62 cm<sup>3</sup>', '8.615 cm<sup>3</sup>', '6.15 cm<sup>3</sup>', '8.62 cm'],
    y=['(2.05 cm)<sup>3</sup> = 2.05 &times; 2.05 &times; 2.05 = 8.615 cm<sup>3</sup>. Cubing is multiplication, so it keeps 3 significant figures: 8.62 cm<sup>3</sup>.',
       'This has 4 significant figures. 2.05 cm has 3, and multiplying it by itself cannot add precision.',
       'This multiplies the edge by 3 instead of cubing it (2.05 &times; 3).',
       'The number is right, but the unit is cubed too: cm &times; cm &times; cm = cm<sup>3</sup>.'],
    h='Cubing means multiplying the number by itself three times, and the unit too.',
    w='(2.05 cm)<sup>3</sup> = 8.615125 cm<sup>3</sup>. Cubing is multiplication, so keep 3 significant figures (from 2.05): <b>8.62 cm<sup>3</sup></b>.',
    d=2, k=1))

# C10 rounding a large number: keep placeholders
v = D('46782')
ans = rsf(v, 2)
assert ans == '47,000'
ITEMS.append(dict(
    t='ch01-sigcalc',
    q='A dairy calculates that a storage vat holds 46,782 L of milk, but its measurements support only <b>two</b> significant figures. What volume should it report?',
    c=[ans + ' L', '47 L', '4,700 L', '46,000 L'],
    y=['Underline the 6 (the second digit). The next digit is 7, so round up to 47 and replace the dropped digits with placeholder zeros: 47,000 L.',
       'This drops the placeholder zeros, making the volume a thousand times too small.',
       'This keeps only some of the placeholders. The rounded value must stay close to 46,782.',
       'The digit after the underlined 6 is a 7, and 5 to 9 rounds up.'],
    h='Underline the second digit and look one place to the right. Then make sure the size of the number does not change.',
    w='Underline the 6 in 46,782; the next digit is 7, so round up: 47. Fill the dropped places with zeros: <b>47,000 L</b> (2 significant figures under this book\'s rule).',
    d=1, k=0))

# ---------------------------------------------------------------- ch01-read (1.3.3 Reading Measuring Tools)
# fScale draws the meniscus bottom at `level`; its edges sit 9 px higher. Plot height 260 px.


def top_edge(f):
    """Reading a student would get from the top edge of the drawn meniscus."""
    per_unit = 260 / (f['hi'] - f['lo'])
    return f['level'] + 9 / per_unit


def check_scale(f, reading, places):
    key = 'len' if f['type'] == 'ruler' else 'level'
    assert ('%.*f' % (places, f[key])) == reading, (f, reading)
    assert f['lo'] < f[key] < f['hi']
    # one estimated digit beyond the smallest mark
    assert round(-math.log10(f['minor'])) + 1 == places, (f, places)


# R1 100 mL cylinder, 1 mL marks
f = {"type": "cylinder", "lo": 30, "hi": 50, "minor": 1, "major": 5, "level": 37.4, "unit": "mL"}
check_scale(f, '37.4', 1)
top = '%.1f' % top_edge(f)
assert top == '38.1'
ITEMS.append(dict(
    t='ch01-read',
    q='A microbiology student measures distilled water in the 100 mL graduated cylinder shown. The marks are 1 mL apart. What volume should she record?',
    c=['37.4 mL', '37 mL', '37.40 mL', top + ' mL'],
    y=['The bottom of the meniscus is between the 37 and 38 mL marks, a little less than halfway. 37 is certain, and you estimate the tenths: 37.4 mL (37.3 or 37.5 mL would also be fair).',
       'This stops at the last mark. Always estimate one more digit beyond the smallest mark.',
       'With marks 1 mL apart you can estimate only the tenths. A hundredths digit claims precision nobody could see.',
       'This reads the top edge of the curved surface, where the liquid climbs the glass. Read the <b>bottom</b> of the meniscus, at eye level.'],
    h='Find the bottom of the meniscus. Marks every 1 mL: which decimal place do you estimate?',
    w='Marks every 1 mL make the ones place certain (37) and the tenths estimated. The bottom of the meniscus is about four-tenths of the way to 38: <b>37.4 mL</b>.',
    d=1, k=0, f=[f]))

# R2 10 mL cylinder, 0.1 mL marks
f = {"type": "cylinder", "lo": 4, "hi": 7, "minor": 0.1, "major": 1, "level": 5.73, "unit": "mL"}
check_scale(f, '5.73', 2)
top = '%.2f' % top_edge(f)
assert top == '5.83'
ITEMS.append(dict(
    t='ch01-read',
    q='A pharmacy technician student measures a liquid in the 10 mL graduated cylinder shown. The marks are 0.1 mL apart. What volume should he record?',
    c=['5.73 mL', '5.7 mL', '5.730 mL', top + ' mL'],
    y=['The meniscus bottom is between the 5.7 and 5.8 mL marks, about three-tenths of the way. 5.7 is certain; estimate the hundredths: 5.73 mL (5.72 or 5.74 mL would also be fair).',
       'This stops at the last mark. With 0.1 mL marks, estimate the hundredths place.',
       'This estimates two digits past the smallest mark. Only one estimated digit is allowed.',
       'This reads the top edge of the meniscus. Read the bottom of the curve, at eye level.'],
    h='Each small mark is 0.1 mL, so the tenths place is certain. Estimate one more digit at the bottom of the curve.',
    w='Certain digits: 5.7 (the meniscus bottom is past the 5.7 mark). Estimated digit: about 3 tenths of the gap. Record <b>5.73 mL</b>.',
    d=2, k=0, f=[f]))

# R3 buret: initial and final readings, volume delivered
f1 = {"type": "buret", "lo": 0, "hi": 3, "minor": 0.1, "major": 1, "level": 1.25, "unit": "mL"}
f2 = {"type": "buret", "lo": 17, "hi": 20, "minor": 0.1, "major": 1, "level": 18.64, "unit": "mL"}
check_scale(f1, '1.25', 2)
check_scale(f2, '18.64', 2)
deliv = D('18.64') - D('1.25')
assert str(deliv) == '17.39'
assert str(D('18.64') + D('1.25')) == '19.89'
assert str(D('18.6') - D('1.3')) == '17.3'
ITEMS.append(dict(
    t='ch01-read',
    q='During a titration, a lab technician reads the buret before (first picture) and after (second picture) delivering a solution. The marks are 0.1 mL apart, and buret numbers increase going <b>down</b>. What volume was delivered?',
    c=[str(deliv) + ' mL', '19.89 mL', '17.3 mL', '17.390 mL'],
    y=['Initial reading 1.25 mL (halfway between 1.2 and 1.3), final reading 18.64 mL. Volume delivered = final &minus; initial = 18.64 &minus; 1.25 = 17.39 mL.',
       'This adds the two readings. The volume delivered is the difference: final minus initial.',
       'This rounds each reading to the tenths (18.6 and 1.3) before subtracting. Buret readings have two decimal places.',
       'Both readings have two decimal places, so the difference has two. A third decimal place is not justified.'],
    h='Read each buret to the hundredths at the bottom of the meniscus (numbers increase downward). Then subtract.',
    w='Initial: the meniscus bottom is halfway between 1.2 and 1.3: 1.25 mL. Final: about four-tenths of the way from 18.6 to 18.7: 18.64 mL. Delivered: 18.64 &minus; 1.25 = <b>17.39 mL</b>.',
    d=3, k=0, f=[f1, f2]))

# R4 ruler, edge exactly on a mark
f = {"type": "ruler", "lo": 0, "hi": 5, "minor": 0.1, "major": 1, "half": 0.5, "start": 0, "len": 4.20, "unit": "cm"}
check_scale(f, '4.20', 2)
ITEMS.append(dict(
    t='ch01-read',
    q='A dental hygiene student measures a strip of floss with the centimeter ruler shown. The ruler is marked every 0.1 cm, and the end of the strip lines up exactly with a mark. What length should she record?',
    c=['4.20 cm', '4.2 cm', '4.200 cm', '4 cm'],
    y=['The end sits exactly on the 4.2 cm mark, so the estimated hundredths digit is a zero, and it must be written: 4.20 cm.',
       'This drops the estimated zero. 4.2 cm tells the reader the ruler was ten times less precise than it is.',
       'This adds a thousandths digit. Only one digit past the 0.1 cm marks can be estimated.',
       'This ignores the 0.1 cm marks entirely.'],
    h='When the edge lands right on a mark, what is the estimated digit? Do you still write it?',
    w='The 0.1 cm marks make the tenths certain (4.2), and the hundredths is estimated. The end is exactly on the mark, so the estimate is 0: <b>4.20 cm</b>.',
    d=1, k=0, f=[f]))

# R5 ruler not starting at zero
f = {"type": "ruler", "lo": 1, "hi": 4, "minor": 0.1, "major": 1, "half": 0.5, "start": 1, "len": 3.86, "unit": "cm"}
check_scale(f, '3.86', 2)
L = D('3.86') - D('1.00')
assert str(L) == '2.86'
ITEMS.append(dict(
    t='ch01-read',
    q='A lab tech measures a blood smear slide label with the ruler shown (marks every 0.1 cm). The left end of the label is lined up with the 1 cm mark, not with 0. What is the length of the label?',
    c=[str(L) + ' cm', '3.86 cm', '2.9 cm', '2.860 cm'],
    y=['The right end reads 3.86 cm and the left end 1.00 cm, so the length is 3.86 &minus; 1.00 = 2.86 cm.',
       'This is the reading at the right end. The label starts at 1 cm, so subtract the starting reading.',
       'This drops the estimated hundredths digit. A ruler marked every 0.1 cm gives two decimal places.',
       'This claims a thousandths digit that nobody could read from 0.1 cm marks.'],
    h='Read both ends to the hundredths. The length is the difference.',
    w='Right end: between 3.8 and 3.9, about six-tenths of the way: 3.86 cm. Left end: 1.00 cm. Length: 3.86 &minus; 1.00 = <b>2.86 cm</b>.',
    d=2, k=0, f=[f]))

# R6 balance display, significant figures
f = {"type": "balance", "read": "0.0450"}
digits = f['read'].lstrip('0.').__len__()
assert digits == 3
ITEMS.append(dict(
    t='ch01-read',
    q='A dental materials student weighs a sample of impression powder on the digital balance shown (the display is in grams). How many significant figures does this mass have?',
    c=[str(digits), '2', '4', '5'],
    y=['The leading zeros (0.0) are placeholders. 4, 5, and the final 0 are significant; the balance measured that last zero. 0.0450 g has 3 significant figures.',
       'This drops the trailing zero. On a balance the last digit shown is measured, so it counts.',
       'This counts the zero between the decimal point and the 4. Leading zeros are never significant.',
       'This counts every digit on the display, including the leading placeholder zeros.'],
    h='Leading zeros only hold the place. What about a zero at the end, after the decimal point?',
    w='The display reads 0.0450 g. Leading zeros are not significant; the trailing zero after the decimal point is. Significant figures: 4, 5, 0, so <b>3</b>.',
    d=1, k=0, f=[f]))

# R7 balance: mass by difference from two displays
fa = {"type": "balance", "read": "48.215"}
fb = {"type": "balance", "read": "50.300"}
m = D(fb['read']) - D(fa['read'])
assert str(m) == '2.085'
assert str(D(fb['read']) + D(fa['read'])) == '98.515'
assert rdp(m, 2) == '2.09'
ITEMS.append(dict(
    t='ch01-read',
    q='A student weighs an empty beaker (first display), adds a powder, and weighs it again (second display). Both displays are in grams. What is the mass of the powder?',
    c=['2.085 g', '2.09 g', '98.515 g', '2.0850 g'],
    y=['Record every digit each display shows: 48.215 g and 50.300 g. Mass of powder = 50.300 &minus; 48.215 = 2.085 g, three decimal places like both readings.',
       'This rounds away a measured digit. Both readings have three decimal places, so the difference keeps three.',
       'This adds the two readings. The mass of the powder is the difference: beaker with powder minus empty beaker.',
       'This adds a fourth decimal place that the balance never showed.'],
    h='Write down every digit each display shows, including the trailing zeros. Then subtract.',
    w='Empty beaker: 48.215 g. Beaker with powder: 50.300 g (the zeros were measured). Powder: 50.300 &minus; 48.215 = <b>2.085 g</b>.',
    d=2, k=0, f=[fa, fb]))

# R8 thermometer exactly on a mark (text only)
ITEMS.append(dict(
    t='ch01-read',
    q='A lab thermometer is marked every 1 &deg;C. The top of the liquid column lines up exactly with the 37 &deg;C mark. What temperature should you record?',
    c=['37.0 &deg;C', '37 &deg;C', '37.00 &deg;C', '37.5 &deg;C'],
    y=['Marks every 1 &deg;C give one decimal place. The column is exactly on the mark, so the estimated tenths digit is 0, and it must be written.',
       'This leaves out the estimated digit. Writing 37 &deg;C says the thermometer was read only to the ones place.',
       'This estimates two digits past the smallest mark. Only one is allowed.',
       'The column is on the 37 mark, not halfway to 38.'],
    h='Marks every 1 &deg;C: which decimal place do you estimate? What is the estimate when the column is right on a mark?',
    w='The ones place is certain (37) and the tenths is estimated. Exactly on the mark means the estimate is 0: <b>37.0 &deg;C</b>.',
    d=1, k=0))

# R9 choosing the tool (text only, nursing)
ITEMS.append(dict(
    t='ch01-read',
    q='A nurse sees a recorded volume of 2.35 mL for a liquid medication. Which tool could have given this reading? (Context only; always follow the order, the device instructions, and facility policy.)',
    c=['An oral syringe marked every 0.1 mL', 'A medicine cup marked every 5 mL', 'A 100 mL graduated cylinder marked every 1 mL', 'A 50 mL cylinder marked every 1 mL'],
    y=['2.35 mL has two decimal places: the tenths are certain and the hundredths estimated. That fits marks 0.1 mL apart.',
       'Marks 5 mL apart allow an estimate only to about the ones place, not hundredths of a milliliter.',
       'Marks every 1 mL give one decimal place (for example 2.4 mL), not two.',
       'Marks every 1 mL give one decimal place, whatever the size of the cylinder.'],
    h='The last digit of a reading is the estimated one. How far apart must the marks be for the hundredths place to be estimated?',
    w='One estimated digit beyond the smallest mark: a reading to the hundredths needs marks every 0.1 mL. Answer: <b>an oral syringe marked every 0.1 mL</b>. Precision depends on the spacing of the marks, not the size of the tool.',
    d=2, k=0))

# R10 coarse ruler (text only)
ITEMS.append(dict(
    t='ch01-read',
    q='A meter stick at a Valley farm stand is marked only every 1 cm (no millimeter marks). The end of a zucchini is about three-tenths of the way from the 28 cm mark to the 29 cm mark. What length should be recorded?',
    c=['28.3 cm', '28 cm', '28.30 cm', '28.03 cm'],
    y=['Marks every 1 cm make the ones place certain (28), and you estimate the tenths: three-tenths of the gap is 0.3. Record 28.3 cm.',
       'This stops at the last mark and leaves out the estimated digit.',
       'This estimates two digits past the 1 cm marks. Only one estimated digit is allowed.',
       'Three-tenths of a 1 cm gap is 0.3 cm, not 0.03 cm. This puts the estimated digit in the wrong place.'],
    h='With marks 1 cm apart, which place is certain and which is estimated?',
    w='Certain: 28 (past the 28 cm mark). Estimated: about 3 tenths of the way to 29. Record <b>28.3 cm</b>. With 0.1 cm marks you could go one place further, but not with this meter stick.',
    d=1, k=0))

# ---------------------------------------------------------------- checks
ALLOWED = {'b', 'i', 'sub', 'sup', 'br'}
for n, it in enumerate(ITEMS):
    assert set(it) <= {'t', 'q', 'c', 'y', 'h', 'w', 'd', 'k', 'f'}, n
    assert len(it['c']) == 4 and len(it['y']) == 4, n
    assert len({re.sub(r'\s+', ' ', c).strip().lower() for c in it['c']}) == 4, (n, it['c'])
    assert it['d'] in (1, 2, 3) and it['k'] in (0, 1), n
    s = ' '.join([it['q'], it['h'], it['w']] + it['c'] + it['y'])
    for tg in re.findall(r'</?([a-z]+)', s):
        assert tg in ALLOWED, (n, tg)
    for tg in ('b', 'i', 'sub', 'sup'):
        assert len(re.findall('<%s>' % tg, s)) == len(re.findall('</%s>' % tg, s)), (n, tg)
    assert not re.search(r'&(?!(?:[a-z]+|#\d+);)', s), n
    assert not re.search(r'all of the above|none of the above', s, re.I), n
    assert '<b>' in it['w'], n
    # the bolded answer in w matches c[0] (ignoring case of the first letter)
    bold = re.search(r'<b>(.*?)</b>(?!.*<b>)', it['w']).group(1)
    assert bold.lower().startswith(re.sub(r'<b>|</b>', '', it['c'][0]).lower()[:6]) or it['c'][0] in bold, (n, bold, it['c'][0])
    if any(w in it['q'] for w in ('dose', 'medication', 'tablets')) and 'Context only' not in it['q']:
        assert it['q'].startswith(MP), n

from collections import Counter
cnt = Counter(it['t'] for it in ITEMS)
assert cnt == {'ch01-scinot': 12, 'ch01-sigcalc': 10, 'ch01-read': 10}, cnt
assert sum(1 for it in ITEMS if it['t'] == 'ch01-read' and it.get('f')) >= 6

if __name__ == '__main__':
    print(len(ITEMS), 'items OK', dict(cnt), '| read items with figures:',
          sum(1 for it in ITEMS if it['t'] == 'ch01-read' and it.get('f')))
