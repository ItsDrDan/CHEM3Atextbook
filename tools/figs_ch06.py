#!/usr/bin/env python3
"""Chapter 6 figures (SVG), phone-first (~470 px wide). python3 tools/figs_ch06.py"""
import os, math
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch06'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#c0392b"/></marker></defs>'
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.2,c=INK,m='ar'): return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#{m})"/>'
def sub(s,z=11): return f'<tspan baseline-shift="sub" font-size="{z}">{s}</tspan>'
def sup(s,z=11): return f'<tspan baseline-shift="super" font-size="{z}">{s}</tspan>'
def box(x,y,w,h,fill,lines,size=15,rx=10):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="1.8"/>'
    n=len(lines); y0=y+h/2-(n-1)*size*0.62+size*0.35
    for i,l in enumerate(lines): s+=T(x+w/2,y0+i*size*1.24,l,size if i==0 else size-2,weight='800' if i==0 else '600')
    return s

# --- Lewis helper: atoms {name:(x,y,label)}, bonds [(a,b,order)], lone pairs {name:[angles deg]}
def lewis(atoms,bonds,lps,R=13,fs=20):
    s=''
    for a,b,o in bonds:
        x1,y1,_=atoms[a]; x2,y2,_=atoms[b]; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L; px,py=-uy,ux
        for k in range(o):
            off=(k-(o-1)/2)*6
            s+=f'<line x1="{x1+ux*R+px*off:.1f}" y1="{y1+uy*R+py*off:.1f}" x2="{x2-ux*R+px*off:.1f}" y2="{y2-uy*R+py*off:.1f}" stroke="{INK}" stroke-width="2.2"/>'
    for n,(x,y,lab) in atoms.items(): s+=T(x,y+fs*0.36,lab,fs,weight='800')
    for n,angs in lps.items():
        x,y,_=atoms[n]
        for a in angs:
            r=math.radians(a); cx,cy=x+math.cos(r)*(R+4),y-math.sin(r)*(R+4); px,py=-math.sin(r),-math.cos(r)
            for d in (-4,4): s+=f'<circle cx="{cx+px*d:.1f}" cy="{cy+py*d:.1f}" r="2.3" fill="{INK}"/>'
    return s

# 1. Ionic bond formation
o=T(235,22,'Ionic bonding: electrons are transferred',16,weight='800')+'<g transform="translate(0,26)">'
o+=T(90,80,'Na',26,weight='800')+f'<circle cx="114" cy="66" r="3" fill="#c0392b"/>'
o+=T(240,80,'Cl',26,weight='800')
for (dx,dy) in [(0,-24),(0,22),(24,0)]:
    for d in (-4,4): o+=f'<circle cx="{240+dx+(d if dy else 0)}" cy="{72+dy+(0 if dy else d)}" r="2.6" fill="{INK}"/>'
o+=f'<circle cx="216" cy="68" r="2.6" fill="{INK}"/>'
o+=f'<path d="M118 60 C 150 30, 190 30, 212 62" stroke="#c0392b" stroke-width="2.2" fill="none" marker-end="url(#arr)"/>'
o+=T(165,30,'1 electron moves',12,weight='700',fill='#c0392b')
o+=T(90,112,'1 valence e⁻',12,weight='600')+T(240,112,'7 valence e⁻',12,weight='600')
o+=arrow(300,72,350,72,2.6)
o+=T(395,80,'Na⁺ Cl⁻',22,weight='800')+T(395,104,'opposite charges',12,weight='600')+T(395,120,'attract',12,weight='600')
o+=T(235,146,'Na loses 1 e⁻ → Na⁺ (the octet of neon)',12,weight='600')+T(235,162,'Cl gains 1 e⁻ → Cl⁻ (the octet of argon)',12,weight='600')
o+=f'<line x1="20" y1="176" x2="450" y2="176" stroke="#c9d3dc" stroke-width="1.5"/>'
o+=T(235,198,'Three kinds of ionic compounds in this course',14,weight='800')
o+=box(14,210,140,62,'#dbe7f6',['Salts','NaCl, CaCl'+sub('2'),'K'+sub('2')+'SO'+sub('4')],14)
o+=box(165,210,140,62,'#fde9c8',['Bases (hydroxides)','NaOH, Ca(OH)'+sub('2')],14)
o+=box(316,210,140,62,'#e3f2e1',['Metal oxides','MgO, Fe'+sub('2')+'O'+sub('3')],14)+'</g>'
svg('ionic_bonding.svg',470,312,o,'Ionic bonding. A sodium atom with one valence electron transfers that electron to a chlorine atom with seven valence electrons, shown by a red curved arrow. The result is Na+ and Cl-, opposite charges that attract. Sodium loses one electron to become Na+ with the octet of neon; chlorine gains one electron to become Cl- with the octet of argon. Below, three kinds of ionic compounds in this course: salts, such as NaCl, CaCl2, and K2SO4; bases (hydroxides), such as NaOH and Ca(OH)2; and metal oxides, such as MgO and Fe2O3.')

# 2. Lewis structures gallery (H2O, NH3, CH4, CO2, N2, HCN)
o=T(235,22,'Lewis structures: every atom ends with an octet (H: 2)',14,weight='800')
cells=[]
cx,cy=80,80
o+=lewis({'O':(cx,cy,'O'),'H1':(cx-44,cy,'H'),'H2':(cx+44,cy,'H')},[('O','H1',1),('O','H2',1)],{'O':[90,270]})+T(cx,cy+64,'H'+sub('2')+'O, water',13,weight='700')
cx=235
o+=lewis({'N':(cx,cy,'N'),'H1':(cx-42,cy+24,'H'),'H2':(cx+42,cy+24,'H'),'H3':(cx,cy+44,'H')},[('N','H1',1),('N','H2',1),('N','H3',1)],{'N':[90]})+T(cx,cy+64,'NH'+sub('3')+', ammonia',13,weight='700')
cx=390
o+=lewis({'C':(cx,cy,'C'),'H1':(cx-42,cy,'H'),'H2':(cx+42,cy,'H'),'H3':(cx,cy-40,'H'),'H4':(cx,cy+40,'H')},[('C','H1',1),('C','H2',1),('C','H3',1),('C','H4',1)],{})+T(cx,cy+64,'CH'+sub('4')+', methane',13,weight='700')
cy=220; cx=80
o+=lewis({'C':(cx,cy,'C'),'O1':(cx-46,cy,'O'),'O2':(cx+46,cy,'O')},[('C','O1',2),('C','O2',2)],{'O1':[90,270],'O2':[90,270]})+T(cx,cy+50,'CO'+sub('2')+', two double bonds',13,weight='700')
cx=235
o+=lewis({'A':(cx-24,cy,'N'),'B':(cx+24,cy,'N')},[('A','B',3)],{'A':[180],'B':[0]})+T(cx,cy+50,'N'+sub('2')+', a triple bond',13,weight='700')
cx=390
o+=lewis({'H':(cx-50,cy,'H'),'C':(cx-6,cy,'C'),'N':(cx+40,cy,'N')},[('H','C',1),('C','N',3)],{'N':[0]})+T(cx,cy+50,'HCN, hydrogen cyanide',13,weight='700')
o+=T(235,300,'Line = shared pair (bond). Dot pair = lone pair (not shared).',13,weight='600')
o+=T(235,320,'Usual bonds: H 1, O 2, N 3, C 4 ("HONC 1-2-3-4").',13,weight='600')
svg('lewis_gallery.svg',470,332,o,'Lewis structures of six molecules, each with every atom ending with an octet, or 2 electrons for hydrogen. Water, H2O: O single-bonded to two H atoms with two lone pairs on O. Ammonia, NH3: N single-bonded to three H atoms with one lone pair on N. Methane, CH4: C single-bonded to four H atoms, no lone pairs. Carbon dioxide, CO2: C double-bonded to each of two O atoms, each O with two lone pairs. Nitrogen, N2: a triple bond between the two N atoms, each with one lone pair. Hydrogen cyanide, HCN: H single-bonded to C, C triple-bonded to N, one lone pair on N. A line is a shared pair (bond); a dot pair is a lone pair. Usual numbers of bonds: H 1, O 2, N 3, C 4 (HONC 1-2-3-4).')

# 3. VSEPR shapes (6 shapes, 2 per row)
def shape(x,y,kind):
    s=''; R=34
    def atom(px,py,lab,r=13,fill='#e9eef4'): return f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'+T(px,py+5,lab,13,weight='800')
    def bond(px,py,qx,qy,style=''): return f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{qx:.1f}" y2="{qy:.1f}" stroke="{INK}" stroke-width="3" {style}/>'
    def lp(px,py,ang):
        r=math.radians(ang); ex,ey=px+math.cos(r)*30,py-math.sin(r)*30
        return f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="13" ry="8" transform="rotate({-ang:.0f} {ex:.1f} {ey:.1f})" fill="#fff4c4" stroke="{INK}" stroke-width="1.3" stroke-dasharray="3 2"/>'
    if kind=='linear':
        for a in (180,0): r=math.radians(a); s+=bond(x,y,x+math.cos(r)*R*1.4,y)+atom(x+math.cos(r)*R*1.4,y,'O',12,'#f6d5d1')
        s+=atom(x,y,'C',13)
    if kind=='trigonal planar':
        for a,l in ((90,'O'),(210,'H'),(330,'H')): r=math.radians(a); s+=bond(x,y,x+math.cos(r)*R*1.25,y-math.sin(r)*R*1.25)+atom(x+math.cos(r)*R*1.25,y-math.sin(r)*R*1.25,l,11 if l=='H' else 12,'#f6d5d1' if l=='O' else '#fff')
        s+=atom(x,y,'C',13)
    if kind=='tetrahedral':
        pts=[(90,1.15,''),(210,1.2,''),(330,1.2,'stroke-dasharray="4 3"'),(270,0.9,'')]
        for a,f,st in [(90,1.2,''),(200,1.2,''),(340,1.2,'stroke-dasharray="4 3"'),(285,1.05,'')]:
            r=math.radians(a); s+=bond(x,y,x+math.cos(r)*R*f,y-math.sin(r)*R*f,st)+atom(x+math.cos(r)*R*f,y-math.sin(r)*R*f,'H',11,'#fff')
        s+=atom(x,y,'C',13)
    if kind=='bent3':
        s+=lp(x,y,90)
        for a in (210,330): r=math.radians(a); s+=bond(x,y,x+math.cos(r)*R*1.25,y-math.sin(r)*R*1.25)+atom(x+math.cos(r)*R*1.25,y-math.sin(r)*R*1.25,'O',12,'#f6d5d1')
        s+=atom(x,y,'O',13,'#f6d5d1')
    if kind=='pyramidal':
        s+=lp(x,y,90)
        for a,st in [(200,''),(340,'stroke-dasharray="4 3"'),(275,'')]:
            r=math.radians(a); s+=bond(x,y,x+math.cos(r)*R*1.2,y-math.sin(r)*R*1.2,st)+atom(x+math.cos(r)*R*1.2,y-math.sin(r)*R*1.2,'H',11,'#fff')
        s+=atom(x,y,'N',13,'#d9e4f5')
    if kind=='bent4':
        s+=lp(x,y,60)+lp(x,y,120)
        for a in (215,325): r=math.radians(a); s+=bond(x,y,x+math.cos(r)*R*1.2,y-math.sin(r)*R*1.2)+atom(x+math.cos(r)*R*1.2,y-math.sin(r)*R*1.2,'H',11,'#fff')
        s+=atom(x,y,'O',13,'#f6d5d1')
    return s
rows=[('linear','Linear','2 groups, 0 lone pairs','180°','CO'+sub('2')),('trigonal planar','Trigonal planar','3 groups, 0 lone pairs','120°','CH'+sub('2')+'O'),
('tetrahedral','Tetrahedral','4 groups, 0 lone pairs','109.5°','CH'+sub('4')),('bent3','Bent','3 groups, 1 lone pair','about 120°','O'+sub('3')+' (ozone)'),
('pyramidal','Trigonal pyramidal','4 groups, 1 lone pair','about 109.5°','NH'+sub('3')),('bent4','Bent','4 groups, 2 lone pairs','about 109.5°','H'+sub('2')+'O')]
o=T(235,22,'VSEPR shapes (up to four electron groups)',16,weight='800')
for i,(k,name,grp,ang,ex) in enumerate(rows):
    X=14; Y=36+i*112
    o+=f'<rect x="{X}" y="{Y}" width="442" height="104" rx="10" fill="#f8fafc" stroke="#c9d3dc" stroke-width="1.3"/>'
    o+=shape(X+80,Y+56,k)
    o+=T(X+170,Y+30,name,16,anchor='start',weight='800')+T(X+170,Y+52,grp,13,anchor='start',weight='600')
    o+=T(X+170,Y+74,'Bond angle '+ang,13,anchor='start',weight='700')+T(X+170,Y+94,'Example: '+ex,13,anchor='start',weight='700')
o+=f'<ellipse cx="34" cy="{36+6*112+10}" rx="11" ry="7" fill="#fff4c4" stroke="{INK}" stroke-width="1.3" stroke-dasharray="3 2"/>'+T(52,36+6*112+15,'= lone pair (pushes bonds closer; not part of the shape name)',12,anchor='start',weight='600')
o+=T(52,36+6*112+33,'Dashed bond = pointing away from you (3-D).',12,anchor='start',weight='600')
svg('vsepr_shapes.svg',470,36+6*112+44,o,'VSEPR shapes for up to four electron groups, drawn as ball-and-stick sketches. Linear: 2 groups, 0 lone pairs, 180 degrees, CO2. Trigonal planar: 3 groups, 0 lone pairs, 120 degrees, CH2O. Tetrahedral: 4 groups, 0 lone pairs, 109.5 degrees, CH4. Bent: 3 groups, 1 lone pair, about 120 degrees, O3 (ozone). Trigonal pyramidal: 4 groups, 1 lone pair, about 109.5 degrees, NH3. Bent: 4 groups, 2 lone pairs, about 109.5 degrees, H2O. Each shape is shown in its own row. Lone pairs are drawn as dashed yellow lobes; they push bonds closer together but are not part of the shape name. A dashed bond points away from you in three dimensions.')

# 4. Polarity: dEN scale + CO2 vs H2O dipoles
o=T(235,22,'Bond type from electronegativity difference (ΔEN)',15,weight='800')
x0,x1=30,440; y=60
def xs(v): return x0+(x1-x0)*v/3.3
o+=f'<rect x="{xs(0)}" y="{y}" width="{xs(0.4)-xs(0)}" height="34" fill="#e3f2e1" stroke="{INK}"/><rect x="{xs(0.4)}" y="{y}" width="{xs(2.0)-xs(0.4)}" height="34" fill="#fde9c8" stroke="{INK}"/><rect x="{xs(2.0)}" y="{y}" width="{xs(3.3)-xs(2.0)}" height="34" fill="#dbe7f6" stroke="{INK}"/>'
o+=T((xs(0)+xs(0.4))/2,y+22,'NP',12,weight='800')+T((xs(0.4)+xs(2.0))/2,y+22,'polar covalent',13,weight='800')+T((xs(2.0)+xs(3.3))/2,y+22,'ionic',13,weight='800')
for v in (0,0.4,2.0,3.3): o+=T(xs(v),y+52,str(v),12,weight='700')
o+=T(235,y+76,'0–0.4 nonpolar covalent (NP) · 0.4–2.0 polar covalent · above 2.0 ionic',12,weight='600')
o+=T(235,y+94,'Examples: Cl–Cl 0.0 · C–H 0.4 · O–H 1.4 · Na–Cl 2.1 (yellow-sheet values)',12,weight='600')
# dipoles
Y=210
o+=T(235,Y-28,'Polar bonds, polar or nonpolar molecule?',15,weight='800')
def at(x,y,l,f): return f'<circle cx="{x}" cy="{y}" r="15" fill="{f}" stroke="{INK}" stroke-width="1.6"/>'+T(x,y+5,l,14,weight='800')
o+=f'<line x1="60" y1="{Y+30}" x2="180" y2="{Y+30}" stroke="{INK}" stroke-width="3"/>'+at(60,Y+30,'O','#f6d5d1')+at(120,Y+30,'C','#e9eef4')+at(180,Y+30,'O','#f6d5d1')
o+=arrow(108,Y+2,72,Y+2,2.4,'#c0392b','arr')+arrow(132,Y+2,168,Y+2,2.4,'#c0392b','arr')
o+=T(120,Y+100,'CO'+sub('2')+': linear, dipoles cancel',13,weight='700')+T(120,Y+118,'NONPOLAR molecule',13,weight='800')
# water
wx,wy=350,Y+20
o+=f'<line x1="{wx}" y1="{wy}" x2="{wx-42}" y2="{wy+30}" stroke="{INK}" stroke-width="3"/><line x1="{wx}" y1="{wy}" x2="{wx+42}" y2="{wy+30}" stroke="{INK}" stroke-width="3"/>'
o+=at(wx,wy,'O','#f6d5d1')+at(wx-42,wy+30,'H','#fff')+at(wx+42,wy+30,'H','#fff')
o+=arrow(wx-30,wy+38,wx-12,wy+24,2.4,'#c0392b','arr')+arrow(wx+30,wy+38,wx+12,wy+24,2.4,'#c0392b','arr')
o+=arrow(wx+86,wy+40,wx+86,wy+2,3,'#2f6f9a')+T(wx+94,wy+26,'net',12,anchor='start',weight='800',fill='#2f6f9a')
o+=T(wx,Y-4,'δ−',13,weight='800')+T(wx-42,wy+62,'δ+',13,weight='800')+T(wx+42,wy+62,'δ+',13,weight='800')
o+=T(350,Y+100,'H'+sub('2')+'O: bent, dipoles add',13,weight='700')+T(350,Y+118,'POLAR molecule',13,weight='800')
o+=T(235,Y+146,'Arrows point toward the more electronegative atom.',12,weight='600')
o+=T(235,Y+166,'SNAP: Symmetrical = Nonpolar; Asymmetrical = Polar.',13,weight='800')
svg('polarity.svg',470,Y+178,o,'Top: a scale of electronegativity difference, delta EN, from 0 to 3.3, divided into three bands: 0 to 0.4 nonpolar covalent, 0.4 to 2.0 polar covalent, and above 2.0 ionic. Examples using yellow-sheet values: Cl-Cl 0.0, C-H 0.4, O-H 1.4, Na-Cl 2.1. Bottom: carbon dioxide is linear, O=C=O, with two bond dipole arrows pointing outward toward the oxygen atoms in opposite directions, so they cancel and CO2 is a nonpolar molecule. Water is bent, with bond dipole arrows pointing from each H toward O; they add to a net dipole pointing toward the oxygen side, so water is a polar molecule, with partial negative charge on O and partial positive charges on the H atoms. Arrows point toward the more electronegative atom. SNAP: symmetrical is nonpolar; asymmetrical is polar.')

# 5. Empirical formula flow
o=T(235,22,'Finding an empirical formula',16,weight='800')
steps=[('#fde9c8',['1. Grams of each element','(from % composition: assume 100 g)']),('#dbe7f6',['2. Moles of each element','divide by atomic mass']),('#e3f2e1',['3. Divide by the smallest','number of moles']),('#efe3f7',['4. Whole-number subscripts','(× 2 or × 3 if you see .5 or .33)']),('#f3f6fa',['5. Molecular formula?','× n, where n = molar mass ÷ empirical mass'])]
y=36
for i,(f,l) in enumerate(steps):
    o+=box(60,y,350,58,f,l,15)
    if i<len(steps)-1: o+=arrow(235,y+58,235,y+76)
    y+=78
o+=T(235,y+6,'Example: 40.0% C, 6.71% H, 53.3% O → CH'+sub('2')+'O; molar mass 180 → C'+sub('6')+'H'+sub('12')+'O'+sub('6'),12,weight='700')
svg('empirical_flow.svg',470,y+18,o,'Steps for finding an empirical formula, stacked with arrows: 1, grams of each element (from percent composition, assume 100 grams); 2, moles of each element (divide by atomic mass); 3, divide by the smallest number of moles; 4, whole-number subscripts (multiply by 2 or 3 if you see .5 or .33); 5, molecular formula, if needed: multiply by n, where n equals molar mass divided by empirical formula mass. Example: 40.0 percent C, 6.71 percent H, 53.3 percent O gives CH2O; with a molar mass of 180, the molecular formula is C6H12O6.')
print('ok')
