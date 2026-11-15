#!/usr/bin/env python3
"""Chapter 8 figures (SVG), phone-first (~470 px wide). python3 tools/figs_ch08.py"""
import os
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch08'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>'
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.4,c=INK): return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#ar)"/>'
def sub(s,z=11): return f'<tspan baseline-shift="sub" font-size="{z}">{s}</tspan>'
def box(x,y,w,h,fill,lines,size=15,rx=10):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="1.8"/>'
    n=len(lines); y0=y+h/2-(n-1)*size*0.62+size*0.35
    for i,l in enumerate(lines): s+=T(x+w/2,y0+i*size*1.24,l,size if i==0 else size-2,weight='800' if i==0 else '600')
    return s
def wheel(x,y,r=16): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="3"/><circle cx="{x}" cy="{y}" r="3" fill="{INK}"/>'
def frame(x,y): return f'<path d="M{x-22} {y} L{x} {y-24} L{x+22} {y} L{x-22} {y} M{x} {y-24} L{x+6} {y-34} M{x+2} {y-34} h12" stroke="#c0392b" stroke-width="3.5" fill="none" stroke-linejoin="round"/>'
def bike(x,y): return wheel(x-26,y)+wheel(x+26,y)+frame(x,y)

# 1. Recipe ratio: bicycles
o=T(235,22,'A balanced equation is a recipe',16,weight='800')
o+=frame(70,96)+T(70,120,'1 frame',13,weight='700')+T(122,90,'+',22)+wheel(160,84)+wheel(200,84)+T(180,120,'2 wheels',13,weight='700')
o+=arrow(232,84,276,84,2.6)+bike(350,92)+T(350,128,'1 bicycle',13,weight='700')
o+=T(235,158,'Frame + 2 Wheel → Bicycle',15,weight='800')
o+=f'<line x1="20" y1="176" x2="450" y2="176" stroke="#c9d3dc" stroke-width="1.5"/>'
o+=T(235,202,'You have 4 frames and 6 wheels. How many bicycles?',14,weight='800')
for i in range(4): o+=frame(50+i*50,262)
for i in range(6): o+=wheel(250+(i%3)*44,232+(i//3)*44,15)
o+=T(110,290,'4 frames → enough for 4 bikes',12,weight='600')+T(338,316,'6 wheels → enough for only 3 bikes',12,weight='600')
o+=T(235,346,'Answer: 3 bicycles. Wheels run out first: they are LIMITING.',13,weight='800')
o+=T(235,366,'One frame is left over (in excess).',13,weight='600')
svg('recipe_bikes.svg',470,378,o,'A balanced equation as a recipe, using bicycles. One frame plus 2 wheels makes 1 bicycle: Frame + 2 Wheel gives Bicycle. Below: with 4 frames and 6 wheels, the 4 frames are enough for 4 bikes, but the 6 wheels are enough for only 3 bikes. Answer: 3 bicycles. The wheels run out first, so they are limiting; one frame is left over, in excess.')

# 2. Stoichiometry road map
o=T(235,22,'The stoichiometry road map',16,weight='800')
o+=box(14,44,180,58,'#fde9c8',['grams of A','(given)'],15)+box(276,44,180,58,'#fde9c8',['grams of B','(wanted)'],15)
o+=box(14,170,180,58,'#dbe7f6',['moles of A',''],16)+box(276,170,180,58,'#dbe7f6',['moles of B',''],16)
o+=arrow(104,104,104,166)+T(112,140,'÷ molar mass A',12,anchor='start',weight='700')
o+=arrow(366,168,366,106)+T(358,140,'× molar mass B',12,anchor='end',weight='700')
o+=arrow(196,199,272,199,3)+T(235,190,'mole ratio',12,weight='800')+T(235,220,'(coefficients)',11,weight='700')
o+=box(14,282,180,62,'#e3f2e1',['liters of gas at STP','÷ 22.4 L/mol'],13)+arrow(104,282,104,232)
o+=box(14,360,180,62,'#efe3f7',['liters of solution','× molarity (mol/L)'],13)+f'<path d="M194 391 C 230 391, 230 230, 190 222" stroke="{INK}" stroke-width="2.2" fill="none" marker-end="url(#ar)"/>'
o+=box(276,282,180,62,'#fbe3d8',['heat (kJ)','× ΔH per mol (Sec 8.6)'],13)+arrow(366,232,366,278)
o+=T(235,446,'Every route passes through the mole ratio between moles of A and moles of B.',12,weight='700')
svg('stoich_roadmap.svg',470,458,o,'The stoichiometry road map. Top row: grams of A (given) and grams of B (wanted). Middle row: moles of A and moles of B. Grams of A divided by the molar mass of A gives moles of A; moles of A times the mole ratio from the balanced equation coefficients gives moles of B; moles of B times the molar mass of B gives grams of B. Other entry points into moles of A: liters of gas at STP divided by 22.4 liters per mole, and liters of solution times molarity. From moles of B you can also find heat in kilojoules using the enthalpy change per mole (Section 8.6). Every route passes through the mole ratio between moles of A and moles of B.')

# 3. Limiting reactant particles: 2 H2 + O2 -> 2 H2O with 6 H2 and 4 O2
def h2(x,y): return f'<circle cx="{x-7}" cy="{y}" r="8" fill="#fff" stroke="{INK}" stroke-width="1.3"/><circle cx="{x+7}" cy="{y}" r="8" fill="#fff" stroke="{INK}" stroke-width="1.3"/>'+T(x-7,y+4,'H',9,weight='800')+T(x+7,y+4,'H',9,weight='800')
def o2(x,y): return f'<circle cx="{x-9}" cy="{y}" r="10" fill="#f6d5d1" stroke="{INK}" stroke-width="1.3"/><circle cx="{x+9}" cy="{y}" r="10" fill="#f6d5d1" stroke="{INK}" stroke-width="1.3"/>'+T(x-9,y+4,'O',10,weight='800')+T(x+9,y+4,'O',10,weight='800')
def h2o(x,y): return f'<circle cx="{x}" cy="{y}" r="10" fill="#f6d5d1" stroke="{INK}" stroke-width="1.3"/><circle cx="{x-12}" cy="{y+10}" r="7" fill="#fff" stroke="{INK}" stroke-width="1.2"/><circle cx="{x+12}" cy="{y+10}" r="7" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'+T(x,y+4,'O',10,weight='800')+T(x-12,y+13,'H',7,weight='800')+T(x+12,y+13,'H',7,weight='800')
o=T(235,22,'2 H'+sub('2')+' + O'+sub('2')+' → 2 H'+sub('2')+'O with 6 H'+sub('2')+' and 4 O'+sub('2'),15,weight='800')
o+=f'<rect x="14" y="40" width="190" height="170" rx="10" fill="#f6fafe" stroke="{INK}" stroke-width="1.5"/><rect x="266" y="40" width="190" height="170" rx="10" fill="#f6fafe" stroke="{INK}" stroke-width="1.5"/>'
for i,(x,y) in enumerate([(50,70),(110,64),(170,74),(56,120),(118,118),(176,128)]): o+=h2(x,y)
for (x,y) in [(56,176),(116,180),(176,172),(96,152)]: o+=o2(x,y)
o+=arrow(210,125,260,125,2.6)
for (x,y) in [(300,68),(360,62),(420,70),(304,122),(364,118),(424,126)]: o+=h2o(x,y)
o+=o2(360,176)
o+=T(109,228,'Before',14,weight='800')+T(361,228,'After',14,weight='800')
o+=T(235,258,'6 H'+sub('2')+' need only 3 O'+sub('2')+'. H'+sub('2')+' runs out first: it is the limiting reactant.',13,weight='700')
o+=T(235,278,'6 H'+sub('2')+'O form, and 1 O'+sub('2')+' is left over (excess reactant).',13,weight='600')
svg('limiting_particles.svg',470,290,o,'Particle view of a limiting-reactant problem for 2 H2 + O2 gives 2 H2O. Before: a box with 6 H2 molecules and 4 O2 molecules. After: a box with 6 H2O molecules and 1 O2 molecule left over. The 6 H2 molecules need only 3 O2 molecules, so H2 runs out first and is the limiting reactant; 6 H2O form, and 1 O2 is left over as the excess reactant.')

# 4. Enthalpy diagrams
def panel(x0,title,exo):
    s=T(x0+105,46,title,15,weight='800')
    s+=arrow(x0+10,250,x0+10,64,2)+T(x0+4,160,'energy',12,weight='700',extra=f'transform="rotate(-90 {x0+4} 160)"')
    yR,yP=(100,200) if exo else (200,100)
    s+=f'<line x1="{x0+30}" y1="{yR}" x2="{x0+100}" y2="{yR}" stroke="{INK}" stroke-width="3"/>'+T(x0+65,yR-8,'reactants',12,weight='700')
    s+=f'<line x1="{x0+120}" y1="{yP}" x2="{x0+190}" y2="{yP}" stroke="{INK}" stroke-width="3"/>'+T(x0+155,yP-8,'products',12,weight='700')
    col='#c0392b' if exo else '#2f6f9a'
    s+=arrow(x0+110,yR,x0+110,yP+(-4 if exo else 4),3,col)
    s+=T(x0+105,276,('ΔH &lt; 0: heat released' if exo else 'ΔH &gt; 0: heat absorbed'),13,weight='800',fill=col)
    s+=T(x0+105,296,('surroundings warm up' if exo else 'surroundings cool down'),12,weight='600')
    return s
o=panel(10,'Exothermic',True)+panel(245,'Endothermic',False)
svg('enthalpy_diagrams.svg',470,308,o,'Two energy diagrams. Exothermic: the reactants line is higher than the products line; a red arrow points down from reactants to products; delta H is less than 0, heat is released, and the surroundings warm up. Endothermic: the reactants line is lower than the products line; a blue arrow points up; delta H is greater than 0, heat is absorbed, and the surroundings cool down.')
print('ok')
