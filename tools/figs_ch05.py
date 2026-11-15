#!/usr/bin/env python3
"""Chapter 5 figures (SVG), phone-first (~470 px wide). python3 tools/figs_ch05.py"""
import os
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch05'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>'
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.4,c=INK): return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#ar)"/>'
def box(x,y,w,h,fill,lines,size=15,rx=10):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="1.8"/>'
    n=len(lines); y0=y+h/2-(n-1)*size*0.62+size*0.35
    for i,l in enumerate(lines): s+=T(x+w/2,y0+i*size*1.24,l,size if i==0 else size-2,weight='800' if i==0 else '600')
    return s
def sup(s,z=11): return f'<tspan baseline-shift="super" font-size="{z}">{s}</tspan>'
def sub(s,z=11): return f'<tspan baseline-shift="sub" font-size="{z}">{s}</tspan>'

# 1. Mole road map (vertical, phone-first)
o=T(235,24,'The mole road map',17,weight='800')
o+=box(135,40,200,62,'#fde9c8',['GRAMS','mass of a sample'],17)
o+=box(135,190,200,62,'#dbe7f6',['MOLES','the hub'],17)
o+=box(135,340,200,62,'#e3f2e1',['PARTICLES','atoms, molecules, ions'],17)
o+=arrow(205,104,205,186)+arrow(265,186,265,104)
o+=T(195,138,'÷ molar mass',13,anchor='end',weight='700')+T(275,138,'× molar mass',13,anchor='start',weight='700')
o+=T(195,156,'(g/mol)',12,anchor='end',weight='600')+T(275,156,'(g/mol)',12,anchor='start',weight='600')
o+=arrow(205,254,205,336)+arrow(265,336,265,254)
o+=T(195,290,'× 6.0221×10'+sup('23'),13,anchor='end',weight='700')+T(275,290,'÷ 6.0221×10'+sup('23'),13,anchor='start',weight='700')
o+=T(195,308,'(Avogadro)',12,anchor='end',weight='600')+T(275,308,'(Avogadro)',12,anchor='start',weight='600')
# side branch: moles of an element in a compound
o+=f'<path d="M337 221 C 420 221, 420 221, 420 221" stroke="{INK}" stroke-width="0"/>'
o+=T(235,430,'Always go through MOLES. There is no direct path',13,weight='700')+T(235,448,'from grams to particles.',13,weight='700')
o+=T(235,474,'Subscripts link moles of a compound to moles of each',13,weight='600')+T(235,492,'element in it: 1 mol H'+sub('2')+'O contains 2 mol H and 1 mol O.',13,weight='600')
svg('mole_roadmap.svg',470,504,o,'The mole road map. Three boxes stacked vertically: GRAMS (mass of a sample) at the top, MOLES (the hub) in the middle, and PARTICLES (atoms, molecules, ions) at the bottom. Between grams and moles: going down, divide by molar mass in grams per mole; going up, multiply by molar mass. Between moles and particles: going down, multiply by Avogadro’s number, 6.0221 times 10 to the 23; going up, divide by Avogadro’s number. Always go through moles; there is no direct path from grams to particles. Subscripts link moles of a compound to moles of each element in it: 1 mole of H2O contains 2 moles of H and 1 mole of O.')

# 2. One mole of different substances (equal particles, different masses)
o=T(235,24,'One mole of each: same number of particles',16,weight='800')
items=[('Carbon','C','12.011 g',22,'#555c63'),('Water','H'+sub('2')+'O','18.015 g',27,'#9cc9ea'),('Table salt','NaCl','58.44 g',40,'#f1f1f1'),('Mercury','Hg','200.59 g',30,'#b8bec6')]
for i,(nm,f,m,r,col) in enumerate(items):
    cx=60+i*117; cy=120
    # simple beaker/mound
    o+=f'<path d="M{cx-38} 70 L{cx-38} 150 Q{cx-38} 158 {cx-30} 158 L{cx+30} 158 Q{cx+38} 158 {cx+38} 150 L{cx+38} 70" fill="none" stroke="{INK}" stroke-width="2"/>'
    h=[11,36,54,30][i]  # 2 px per mL: graphite 5.3, water 18.0, NaCl 27, Hg 14.8 mL
    o+=f'<rect x="{cx-36}" y="{157-h}" width="72" height="{h}" fill="{col}" stroke="{INK}" stroke-width="1"/>'
    o+=T(cx,182,nm,14,weight='800')+T(cx,202,f,15,weight='800')+T(cx,224,m,15,weight='800')
o+=T(235,256,'Each holds 6.0221 × 10'+sup('23')+' particles (atoms, molecules, or formula units).',13,weight='600')
o+=T(235,276,'Their masses differ because each particle has a different mass.',13,weight='600')+T(235,296,'(Sample heights are drawn to scale by volume.)',12,weight='600')
svg('mole_samples.svg',470,306,o,'One mole of each of four substances shown in identical containers, each holding the same number of particles, 6.0221 times 10 to the 23. Carbon, C: 12.011 grams, a thin layer of black solid (about 5 mL). Water, H2O: 18.015 grams of liquid (about 18 mL). Table salt, NaCl: 58.44 grams, the tallest pile, of white solid (about 27 mL). Mercury, Hg: 200.59 grams of dense silver liquid (about 15 mL). The masses differ because each particle has a different mass.')

# 3. Subscripts as mole ratios: CO2 and Mg(OH)2
o=T(235,24,'Subscripts are mole ratios',16,weight='800')
def atom(x,y,r,lab,fill): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'+T(x,y+5,lab,14,weight='800')
o+=atom(70,80,16,'O','#f6d5d1')+atom(110,80,18,'C','#d9dde2')+atom(150,80,16,'O','#f6d5d1')
o+=T(110,124,'one CO'+sub('2')+' molecule',13,weight='700')
o+=T(330,64,'1 CO'+sub('2')+' : 1 C : 2 O',16,weight='800',extra='')
o+=T(330,90,'1 mol CO'+sub('2')+' contains',13,weight='600')+T(330,108,'1 mol C and 2 mol O',13,weight='600')
o+=f'<line x1="20" y1="146" x2="450" y2="146" stroke="#c9d3dc" stroke-width="1.5"/>'
o+=atom(110,200,22,'Mg','#cfe8cf')+atom(56,200,16,'O','#f6d5d1')+atom(164,200,16,'O','#f6d5d1')+atom(30,200,10,'H','#fff')+atom(190,200,10,'H','#fff')
o+=T(110,244,'one Mg(OH)'+sub('2')+' formula unit',13,weight='700')
o+=T(330,184,'1 Mg(OH)'+sub('2')+' : 1 Mg : 2 O : 2 H',16,weight='800')
o+=T(330,210,'The 2 outside the parentheses',13,weight='600')+T(330,228,'multiplies both O and H.',13,weight='600')
svg('subscript_ratios.svg',470,258,o,'Subscripts as mole ratios. Top: one CO2 molecule drawn as a carbon atom between two oxygen atoms; 1 CO2 to 1 C to 2 O, so 1 mole of CO2 contains 1 mole of C and 2 moles of O. Bottom: one Mg(OH)2 formula unit drawn as a magnesium ion with an OH group on each side; 1 Mg(OH)2 to 1 Mg to 2 O to 2 H; the 2 outside the parentheses multiplies both O and H.')
print('ok')
