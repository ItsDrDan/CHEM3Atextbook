#!/usr/bin/env python3
"""Chapter 9 figure: schematic phase diagram of water (SVG), phone-first (~470 px wide).
Same house style as tools/figs_ch09.py. Not to scale.  python3 tools/fig_phase_ch09.py"""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'figures', 'ch09'); os.makedirs(OUT, exist_ok=True)
FF = "Lato, Helvetica, Arial, sans-serif"; INK = "#2d3f4b"
RED = "#c0392b"; BLUE = "#2f5fa8"; GRN = "#2e7d32"; GRAY = "#c9d3dc"; MUTE = "#55606b"

def T(x, y, s, size=15, anchor='middle', weight='700', fill=INK, extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS = (f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>')
def line(x1, y1, x2, y2, c=INK, w=1.6, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'
def arrow(x1, y1, x2, y2, w=2.0, c=INK):
    return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#ar)"/>'
def dot(x, y, r=6, fill=RED):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1.4"/>'
def poly(pts, c=INK, w=3.0):
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'

W, H = 470, 414
X0, Y0, X1, Y1 = 74, 350, 450, 52          # plot box: origin (X0, Y0), top-right (X1, Y1)
TPx, TPy = 176, 286                         # triple point
ATM = 168                                   # y of the 1 atm line
# solid-liquid line: straight, tilted LEFT going up (negative slope, as for water)
SLtop = (156, 64)
def sl_x(y):  # x on the solid-liquid line at height y
    return TPx + (y - TPy) * (SLtop[0] - TPx) / (SLtop[1] - TPy)
# liquid-gas (vapor pressure) curve: y = TPy - a (x - TPx)^p through the 1 atm point and the end point
import math
NBPx, ENDx, ENDy = 352, 438, 78
p = math.log((TPy - ENDy) / (TPy - ATM)) / math.log((ENDx - TPx) / (NBPx - TPx))
a = (TPy - ATM) / (NBPx - TPx) ** p
lg = [(x, TPy - a * (x - TPx) ** p) for x in [TPx + i * (ENDx - TPx) / 60 for i in range(61)]]
# solid-gas (sublimation) curve, from near the origin up to the triple point, concave up
sg = []
for i in range(41):
    t = i / 40
    x = X0 + 10 + t * (TPx - X0 - 10)
    y = Y0 - 6 - (Y0 - 6 - TPy) * t ** 2.2
    sg.append((x, y))
NMPx = sl_x(ATM)

o = T(W / 2, 24, 'Phase diagram of water (not to scale)', 16, weight='800')
# axes
o += arrow(X0, Y0, X0, Y1 - 10, 2.2) + arrow(X0, Y0, X1, Y0, 2.2)
o += T(X1 - 4, Y0 + 40, 'Temperature (°C) →', 13, anchor='end', weight='800')
o += T(24, (Y0 + Y1) / 2, 'Pressure (atm) →', 13, weight='800', extra=f'transform="rotate(-90 24 {(Y0 + Y1) / 2:.1f})"')
# 1 atm reference line and drop lines
o += line(X0, ATM, X1 - 6, ATM, MUTE, 1.4, '6 4') + T(X0 - 8, ATM + 5, '1 atm', 12, anchor='end', weight='800')
o += line(NMPx, ATM, NMPx, Y0, MUTE, 1.2, '3 4') + line(NBPx, ATM, NBPx, Y0, MUTE, 1.2, '3 4')
o += T(NMPx, Y0 + 18, '0 °C', 12, weight='800') + T(NBPx, Y0 + 18, '100 °C', 12, weight='800')
# the three lines (two phases at equilibrium on each)
o += poly([(TPx, TPy), SLtop], BLUE) + poly(lg, RED) + poly(sg, GRN)
# regions
o += T(112, 128, 'SOLID', 17, weight='800') + T(112, 146, '(ice)', 12, weight='700', fill=MUTE)
o += T(262, 112, 'LIQUID', 17, weight='800') + T(262, 130, '(water)', 12, weight='700', fill=MUTE)
o += T(300, 262, 'GAS', 17, weight='800') + T(300, 280, '(water vapor)', 12, weight='700', fill=MUTE)
# points
o += dot(TPx, TPy, 6.5, '#f3c34a') + dot(NMPx, ATM, 6, BLUE) + dot(NBPx, ATM, 6, RED)
o += T(TPx + 12, TPy + 22, 'Triple point', 12.5, anchor='start', weight='800')
o += T(TPx + 12, TPy + 37, '0.01 °C, 0.006 atm', 11, anchor='start', weight='700', fill=MUTE)
o += T(NMPx + 10, ATM - 10, 'Normal melting point', 11.5, anchor='start', weight='800', fill=BLUE)
o += T(NBPx + 10, ATM + 22, 'Normal', 11.5, anchor='start', weight='800', fill=RED) + T(NBPx + 10, ATM + 37, 'boiling point', 11.5, anchor='start', weight='800', fill=RED)
# line labels
o += T(168, 84, 'melting / freezing', 10.5, anchor='start', weight='700', fill=BLUE)
o += T(410, 78, 'boiling /', 10.5, anchor='end', weight='700', fill=RED) + T(410, 92, 'condensing', 10.5, anchor='end', weight='700', fill=RED)
o += T(82, 252, 'sublimation /', 10.5, anchor='start', weight='700', fill=GRN) + T(82, 266, 'deposition', 10.5, anchor='start', weight='700', fill=GRN)
o += T(W / 2, 404, 'On a line, two phases coexist. Water’s solid–liquid line tilts left.', 11.5, weight='700')

ARIA = ('Schematic phase diagram of water, not to scale. Pressure in atmospheres is on the vertical axis and temperature in degrees Celsius '
        'on the horizontal axis. Three regions: solid (ice) at the upper left, liquid (water) at the top middle, and gas (water vapor) '
        'at the lower right. Three lines separate them, and on each line two phases coexist: the melting and freezing line between solid and liquid, '
        'which tilts slightly to the left as pressure rises; the boiling and condensing curve between liquid and gas; and the sublimation and '
        'deposition curve between solid and gas. All three lines meet at the triple point, 0.01 degrees Celsius and 0.006 atm, where solid, '
        'liquid, and gas coexist. A dashed horizontal line at 1 atm crosses the solid-liquid line at the normal melting point, 0 degrees Celsius, '
        'and the liquid-gas curve at the normal boiling point, 100 degrees Celsius.')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{ARIA}">'
       f'<title>{ARIA}</title><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{o}</svg>')
open(os.path.join(OUT, 'phase_diagram_water.svg'), 'w', encoding='utf-8').write(svg)
print('wrote figures/ch09/phase_diagram_water.svg', f'p={p:.3f}', f'NMPx={NMPx:.1f}')
