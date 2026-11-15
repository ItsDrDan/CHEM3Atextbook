#!/usr/bin/env python3
"""Chapter 7 figures (SVG), phone-first (~470 px wide). python3 tools/figs_ch07.py"""
import os, math
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch07'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#c0392b"/></marker></defs>'
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.2,c=INK,m='ar'): return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#{m})"/>'
def sub(s,z=11): return f'<tspan baseline-shift="sub" font-size="{z}">{s}</tspan>'
def sup(s,z=11): return f'<tspan baseline-shift="super" font-size="{z}">{s}</tspan>'
def beaker(x,y,w=80,h=90,fill='#e8f2fb'):
    return f'<path d="M{x} {y} L{x} {y+h-8} Q{x} {y+h} {x+8} {y+h} L{x+w-8} {y+h} Q{x+w} {y+h} {x+w} {y+h-8} L{x+w} {y}" fill="none" stroke="{INK}" stroke-width="2"/><rect x="{x+2}" y="{y+28}" width="{w-4}" height="{h-30}" fill="{fill}"/>'
def ion(x,y,lab,fill,r=13): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1.3"/>'+T(x,y+4,lab,10,weight='800')

# 1. Signs of a chemical reaction
o=T(235,22,'Evidence that a chemical reaction happened',15,weight='800')
cells=[('Gas forms','bubbles'),('A solid forms','precipitate'),('Color changes','new substance'),('Energy changes','heat, light, or cold')]
for i,(t1,t2) in enumerate(cells):
    col=i%2; row=i//2; X=14+col*228; Y=36+row*160
    o+=f'<rect x="{X}" y="{Y}" width="218" height="150" rx="10" fill="#f8fafc" stroke="#c9d3dc"/>'
    bx=X+69
    if i==0:
        o+=beaker(bx,Y+14)
        for (dx,dy,r) in [(20,70,5),(40,55,6),(58,75,4),(30,40,5),(50,90,5)]: o+=f'<circle cx="{bx+dx}" cy="{Y+dy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1.3"/>'
    if i==1:
        o+=beaker(bx,Y+14)+f'<path d="M{bx+4} {Y+98} Q{bx+40} {Y+86} {bx+76} {Y+98} L{bx+76} {Y+102} L{bx+4} {Y+102}z" fill="#f4f4f4" stroke="{INK}" stroke-width="1.3"/>'
        for k in range(12): o+=f'<circle cx="{bx+10+k*5.5}" cy="{Y+96-(k%3)*2}" r="2.2" fill="{INK}"/>'
    if i==2:
        o+=beaker(bx-30,Y+14,60,90,'#cfe2f7')+arrow(bx+36,Y+70,bx+56,Y+70)+beaker(bx+62,Y+14,60,90,'#d8ead2')
        o+=T(bx,Y+80,'blue',11,weight='700')+T(bx+92,Y+80,'green',11,weight='700')
    if i==3:
        o+=beaker(bx,Y+14)+''.join(f'<path d="M{bx+20+k*20} {Y+38} q6 -6 0 -12 q-6 -6 0 -12" stroke="#c0392b" stroke-width="2" fill="none"/>' for k in range(3))
    o+=T(X+109,Y+128,t1,14,weight='800')+T(X+109,Y+144,t2,12,weight='600')
o+=T(235,370,'Evidence is a clue, not proof: boiling water bubbles too (a physical change).',12,weight='600')
svg('signs_of_reaction.svg',470,382,o,'Four kinds of evidence that a chemical reaction happened, each with a beaker sketch: gas forms (bubbles rising in the liquid); a solid forms (a precipitate settling at the bottom of a clear solution); color changes (a blue solution becoming a green one, a new substance); and energy changes (heat, light, or cold, shown as wavy lines above the beaker). Evidence is a clue, not proof: boiling water bubbles too, which is a physical change.')

# 2. Balanced equation atom count: CH4 + 2O2 -> CO2 + 2H2O
def mol(x,y,parts):
    s=''
    for (dx,dy,l,f,r) in parts: s+=f'<circle cx="{x+dx}" cy="{y+dy}" r="{r}" fill="{f}" stroke="{INK}" stroke-width="1.2"/>'+T(x+dx,y+dy+4,l,10 if r<11 else 11,weight='800')
    return s
C='#d9dde2'; O='#f6d5d1'; H='#ffffff'
o=T(235,22,'A balanced equation: atoms are only rearranged',15,weight='800')
o+=T(235,52,'CH'+sub('4')+'(g) + 2 O'+sub('2')+'(g) → CO'+sub('2')+'(g) + 2 H'+sub('2')+'O(g)',17,weight='800')
y=110
o+=mol(40,y,[(0,0,'C',C,13),(-18,-16,'H',H,9),(18,-16,'H',H,9),(-18,16,'H',H,9),(18,16,'H',H,9)])
o+=T(78,y+5,'+',18)+mol(108,y-20,[(0,0,'O',O,11),(20,0,'O',O,11)])+mol(108,y+20,[(0,0,'O',O,11),(20,0,'O',O,11)])
o+=arrow(160,y,220,y,2.6)
o+=mol(254,y,[(-22,0,'O',O,11),(0,0,'C',C,13),(22,0,'O',O,11)])+T(304,y+5,'+',18)
o+=mol(345,y-22,[(0,0,'O',O,11),(-16,12,'H',H,9),(16,12,'H',H,9)])+mol(400,y+12,[(0,0,'O',O,11),(-16,12,'H',H,9),(16,12,'H',H,9)])
o+=T(100,y+64,'Reactants',14,weight='800')+T(340,y+64,'Products',14,weight='800')
rows=[('C','1','1'),('H','4','2 × 2 = 4'),('O','2 × 2 = 4','2 + 2 = 4')]
yy=y+92
for e,a,b in rows: o+=T(100,yy,f'{e}: {a}',14,weight='700')+T(340,yy,f'{e}: {b}',14,weight='700'); yy+=22
o+=T(235,yy+10,'Coefficients (big numbers in front) count molecules;',12,weight='600')+T(235,yy+28,'never change subscripts to balance.',12,weight='600')
svg('balanced_equation.svg',470,yy+40,o,'A balanced equation for the combustion of methane: CH4(g) + 2 O2(g) gives CO2(g) + 2 H2O(g), drawn with ball molecules. Reactants: one methane molecule (one C, four H) and two O2 molecules. Products: one CO2 molecule and two water molecules. Atom counts: carbon 1 on each side; hydrogen 4 on the left and 2 times 2 equals 4 on the right; oxygen 2 times 2 equals 4 on the left and 2 plus 2 equals 4 on the right. Coefficients count molecules; never change subscripts to balance.')

# 3. Reaction patterns
o=T(235,22,'Five reaction patterns',16,weight='800')
pats=[('Combination','A + B → AB','2 Mg + O'+sub('2')+' → 2 MgO'),('Decomposition','AB → A + B','2 H'+sub('2')+'O'+sub('2')+' → 2 H'+sub('2')+'O + O'+sub('2')),('Single displacement','A + BC → AC + B','Zn + CuSO'+sub('4')+' → ZnSO'+sub('4')+' + Cu'),('Double displacement','AB + CD → AD + CB','AgNO'+sub('3')+' + NaCl → AgCl + NaNO'+sub('3')),('Combustion','fuel + O'+sub('2')+' → CO'+sub('2')+' + H'+sub('2')+'O','CH'+sub('4')+' + 2 O'+sub('2')+' → CO'+sub('2')+' + 2 H'+sub('2')+'O')]
fills=['#dbe7f6','#fde9c8','#e3f2e1','#efe3f7','#fbe3d8']
for i,(n,g,e) in enumerate(pats):
    Y=36+i*78
    o+=f'<rect x="14" y="{Y}" width="442" height="70" rx="10" fill="{fills[i]}" stroke="{INK}" stroke-width="1.5"/>'
    o+=T(28,Y+24,n,15,anchor='start',weight='800')+T(442,Y+24,g,14,anchor='end',weight='800')+T(28,Y+52,'Example: '+e,13,anchor='start',weight='600')
svg('reaction_patterns.svg',470,36+5*78+4,o,'Five reaction patterns, each in its own colored row with a general form and an example. Combination: A + B gives AB; example 2 Mg + O2 gives 2 MgO. Decomposition: AB gives A + B; example 2 H2O2 gives 2 H2O + O2. Single displacement: A + BC gives AC + B; example Zn + CuSO4 gives ZnSO4 + Cu. Double displacement: AB + CD gives AD + CB; example AgNO3 + NaCl gives AgCl + NaNO3. Combustion: fuel + O2 gives CO2 + H2O; example CH4 + 2 O2 gives CO2 + 2 H2O.')

# 4. Precipitation particle view
o=T(235,22,'Mixing AgNO'+sub('3')+'(aq) and NaCl(aq)',15,weight='800')
AG='#d9dde2'; NO='#dbe7f6'; NA='#fde9c8'; CL='#e3f2e1'
def box(x,y,w,h): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#f6fafe" stroke="{INK}" stroke-width="1.5"/>'
o+=box(14,40,140,120)+box(166,40,140,120)
for (x,y) in [(40,70),(110,90),(60,130)]: o+=ion(x,y,'Ag⁺',AG)
for (x,y) in [(80,64),(40,112),(120,135)]: o+=ion(x,y,'NO₃⁻',NO,15)
for (x,y) in [(195,70),(260,100),(220,135)]: o+=ion(x,y,'Na⁺',NA)
for (x,y) in [(240,62),(190,110),(280,140)]: o+=ion(x,y,'Cl⁻',CL)
o+=T(84,178,'AgNO'+sub('3')+'(aq)',13,weight='700')+T(236,178,'NaCl(aq)',13,weight='700')
o+=arrow(318,100,350,100,2.6)
o+=box(356,40,100,120)
for (x,y) in [(380,60),(430,72),(390,100)]: o+=ion(x,y,'Na⁺',NA)
for (x,y) in [(420,105),(375,130),(440,135)]: o+=ion(x,y,'NO₃⁻',NO,15)
# solid at bottom
o+=f'<rect x="360" y="148" width="92" height="12" fill="#eee" stroke="{INK}"/>'+T(406,158,'AgCl(s)',10,weight='800')
o+=T(406,178,'after mixing',13,weight='700')
o+=T(235,212,'Molecular: AgNO'+sub('3')+'(aq) + NaCl(aq) → AgCl(s) + NaNO'+sub('3')+'(aq)',13,weight='700')
o+=T(235,234,'Spectator ions (unchanged): Na⁺ and NO₃⁻',13,weight='600')
o+=T(235,258,'Net ionic: Ag⁺(aq) + Cl⁻(aq) → AgCl(s)',15,weight='800')
svg('precipitation.svg',470,272,o,'Particle view of a precipitation reaction. One box shows silver nitrate solution as separate Ag+ and NO3- ions; a second box shows sodium chloride solution as separate Na+ and Cl- ions. After mixing, the third box shows Na+ and NO3- ions still free in solution, and a layer of solid AgCl at the bottom. Molecular equation: AgNO3(aq) + NaCl(aq) gives AgCl(s) + NaNO3(aq). Spectator ions, unchanged: Na+ and NO3-. Net ionic equation: Ag+(aq) + Cl-(aq) gives AgCl(s).')

# 5. Redox Zn in Cu2+
o=T(235,22,'Zinc metal in copper(II) sulfate solution',15,weight='800')
o+=beaker(150,40,170,150,'#cfe2f7')
o+=f'<rect x="222" y="30" width="26" height="150" fill="#b8bec6" stroke="{INK}" stroke-width="1.5"/>'+T(235,50,'Zn',13,weight='800')
for (x,y) in [(250,150),(256,165),(246,172),(222,160),(216,172)]: o+=f'<circle cx="{x}" cy="{y}" r="4" fill="#b8733f" stroke="{INK}" stroke-width="0.8"/>'
o+=ion(185,120,'Cu²⁺','#cfe2f7',14)+ion(290,110,'Cu²⁺','#cfe2f7',14)+ion(290,160,'Zn²⁺','#eee',14)
o+=f'<path d="M222 120 C 210 112, 205 115, 200 118" stroke="#c0392b" stroke-width="2" fill="none" marker-end="url(#arr)"/>'+T(190,96,'2 e⁻',12,weight='800',fill='#c0392b')
o+=T(330,148,'copper',11,anchor='start',weight='700')+T(330,162,'metal forms',11,anchor='start',weight='700')
o+=T(235,214,'Oxidation (LEO): Zn(s) → Zn²⁺(aq) + 2 e⁻',14,weight='800')
o+=T(235,236,'Reduction (GER): Cu²⁺(aq) + 2 e⁻ → Cu(s)',14,weight='800')
o+=T(235,260,'Overall: Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)',14,weight='700')
o+=T(235,284,'Zn is the reducing agent; Cu²⁺ is the oxidizing agent.',12,weight='600')
o+=T(235,302,'The blue color fades as Cu²⁺ is used up.',12,weight='600')
svg('redox_zn_cu.svg',470,314,o,'A zinc strip standing in blue copper(II) sulfate solution. Two electrons, shown by a red arrow, move from the zinc to a Cu2+ ion; reddish copper metal forms on the strip and Zn2+ ions enter the solution. Oxidation, LEO: Zn(s) gives Zn2+(aq) + 2 electrons. Reduction, GER: Cu2+(aq) + 2 electrons gives Cu(s). Overall: Zn(s) + Cu2+(aq) gives Zn2+(aq) + Cu(s). Zinc is the reducing agent; Cu2+ is the oxidizing agent. The blue color fades as Cu2+ is used up.')

# 6. Activity series
o=T(235,22,'A short activity series of metals',15,weight='800')
mets=['Li','K','Ca','Na','Mg','Al','Zn','Fe','Ni','Sn','Pb','H₂','Cu','Ag','Au']
for i,m in enumerate(mets):
    y=44+i*26; fill='#fde9c8' if m!='H₂' else '#e3f2e1'
    o+=f'<rect x="150" y="{y}" width="90" height="22" rx="5" fill="{fill}" stroke="{INK}" stroke-width="1.2"/>'+T(195,y+16,m,14,weight='800')
o+=arrow(120,430,120,48,3)+T(108,240,'more easily oxidized (more active)',12,weight='700',extra='transform="rotate(-90 108 240)"')
o+=T(260,60,'React with water',12,anchor='start',weight='700')+T(260,74,'and with acids',12,anchor='start',weight='700')
o+=T(260,200,'React with acids,',12,anchor='start',weight='700')+T(260,214,'releasing H₂',12,anchor='start',weight='700')
o+=T(260,370,'Do not react',12,anchor='start',weight='700')+T(260,384,'with acids',12,anchor='start',weight='700')
o+=T(235,456,'A metal replaces the ions of any metal BELOW it.',13,weight='800')
o+=T(235,476,'Zn + Cu²⁺ → reacts.   Cu + Zn²⁺ → no reaction.',13,weight='600')
svg('activity_series.svg',470,488,o,'A short activity series of metals, listed from most active at the top to least active at the bottom: Li, K, Ca, Na, Mg, Al, Zn, Fe, Ni, Sn, Pb, H2, Cu, Ag, Au. An arrow pointing up is labeled more easily oxidized, more active. Notes: the metals at the very top react with water and with acids; metals above hydrogen react with acids, releasing H2; metals below hydrogen (Cu, Ag, Au) do not react with acids. A metal replaces the ions of any metal below it: Zn + Cu2+ reacts; Cu + Zn2+ gives no reaction.')
print('ok')
