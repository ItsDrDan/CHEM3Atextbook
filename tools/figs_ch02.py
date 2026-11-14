#!/usr/bin/env python3
"""Chapter 2 figures (SVG), phone-first (~470 px wide, 13-17 px text). python3 tools/figs_ch02.py
Colors are never the only cue: patterns, letters and labels carry the meaning."""
import os, math
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch02'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=f'''<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker>
<pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#fdf0d8"/><circle cx="2" cy="2" r="1" fill="#d4a24c"/></pattern>
<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#eaf5e8"/><line x1="0" y1="0" x2="0" y2="8" stroke="#8cc286" stroke-width="1.6"/></pattern></defs>'''
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.4): return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK}" stroke-width="{w}" fill="none" marker-end="url(#ar)"/>'
def p(x,y,r=11): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#d9534f" stroke="{INK}" stroke-width="1.4"/>'+T(x,y+5,'+',15,weight='900',fill='#fff')
def n(x,y,r=11): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#cfd6dc" stroke="{INK}" stroke-width="1.4"/>'+T(x,y+4,'n',12,weight='800')
def e(x,y,r=7): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#4a6fd1" stroke="{INK}" stroke-width="1.2"/>'+T(x,y+4.5,'&#8722;',13,weight='900',fill='#fff')

# 1. Gold foil experiment
o=''
o+=f'<rect x="10" y="80" width="60" height="50" rx="6" fill="#eef5fb" stroke="{INK}" stroke-width="2"/>'+T(40,102,'alpha',13)+T(40,118,'source',13)
o+=f'<rect x="70" y="98" width="70" height="14" fill="#f2f2f2" stroke="{INK}" stroke-width="1.5"/>'
o+=f'<rect x="230" y="40" width="10" height="130" fill="#e8c35a" stroke="{INK}" stroke-width="1.5"/>'+T(235,30,'gold foil',13)
o+=f'<path d="M330 20 A150 150 0 0 1 330 190" fill="none" stroke="#9aa" stroke-width="10" opacity=".5"/>'+T(395,212,'detector screen',13)
for dy in (-14,-7,0,7,14): o+=arrow(140,105+dy,325,105+dy*1.4,2)
o+=arrow(150,105,232,105)
o+=f'<path d="M235 101 Q240 60 300 30" stroke="#c0392b" stroke-width="2.6" fill="none" marker-end="url(#ar)"/>'
o+=f'<path d="M235 103 Q200 95 170 70" stroke="#c0392b" stroke-width="2.6" fill="none" marker-end="url(#ar)"/>'
o+=T(10,250,'Most alpha particles pass straight through.',14,anchor='start',weight='600')
o+=T(10,270,'A few bounce off at large angles (red arrows).',14,anchor='start',weight='600')
o+=T(10,290,'Conclusion: an atom is mostly empty space with a',14,anchor='start',weight='600')
o+=T(10,310,'tiny, dense, positively charged nucleus.',14,anchor='start',weight='600')
svg('gold_foil.svg',470,322,o,'Rutherford gold foil experiment. A beam of positively charged alpha particles from a source is aimed at a thin gold foil, with a detector screen around it. Most alpha particles pass straight through the foil; a few are deflected at large angles or bounce back. Conclusion: an atom is mostly empty space with a tiny, dense, positively charged nucleus.')

# 2. Nuclear atom
o=''
cx,cy=150,150
o+=f'<circle cx="{cx}" cy="{cy}" r="125" fill="#eef2fb" stroke="{INK}" stroke-width="1.5" stroke-dasharray="5 5"/>'
for a,r in [(20,95),(130,105),(250,90),(320,110),(80,70),(200,60)]:
    o+=e(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a)))
nuc=[(-9,-9,'p'),(9,-9,'n'),(-9,9,'n'),(9,9,'p'),(0,0,'p'),(0,-16,'n')]
for dx,dy,k in nuc: o+=(p if k=='p' else n)(cx+dx,cy+dy,10)
o+=f'<line x1="{cx+18}" y1="{cy+6}" x2="300" y2="190" stroke="{INK}" stroke-width="1.2"/>'+T(305,184,'Nucleus:',15,anchor='start',weight='800')+T(305,203,'protons (+) and',14,anchor='start',weight='600')+T(305,221,'neutrons (n); almost',14,anchor='start',weight='600')+T(305,239,'all of the mass',14,anchor='start',weight='600')
o+=f'<line x1="{cx+105}" y1="{cy-60}" x2="300" y2="60" stroke="{INK}" stroke-width="1.2"/>'+T(305,55,'Electron cloud:',15,anchor='start',weight='800')+T(305,74,'electrons (&#8722;) move',14,anchor='start',weight='600')+T(305,92,'through mostly',14,anchor='start',weight='600')+T(305,110,'empty space',14,anchor='start',weight='600')
o+=T(235,300,'Not to scale: if the nucleus were the size of a pea,',13,weight='600')+T(235,318,'the atom would be about the size of a football stadium.',13,weight='600')
svg('nuclear_atom.svg',470,330,o,'Model of an atom. A tiny central nucleus contains protons, marked plus, and neutrons, marked n; it holds almost all of the mass. Electrons, marked minus, move through a large, mostly empty electron cloud around the nucleus. Not to scale: if the nucleus were the size of a pea, the atom would be about the size of a football stadium.')

# 3. Isotope notation + hydrogen isotopes
o=''
o+=T(110,95,'X',72,weight='800')+T(62,52,'A',30,weight='800')+T(62,118,'Z',30,weight='800')
o+=f'<line x1="78" y1="44" x2="190" y2="30" stroke="{INK}" stroke-width="1.2"/>'+T(195,28,'mass number A = protons + neutrons',14,anchor='start',weight='700')
o+=f'<line x1="78" y1="112" x2="190" y2="130" stroke="{INK}" stroke-width="1.2"/>'+T(195,136,'atomic number Z = protons',14,anchor='start',weight='700')
o+=f'<line x1="140" y1="80" x2="190" y2="82" stroke="{INK}" stroke-width="1.2"/>'+T(195,87,'element symbol',14,anchor='start',weight='700')
o+=f'<line x1="10" y1="160" x2="460" y2="160" stroke="#bbb" stroke-dasharray="5 5"/>'
iso=[('hydrogen-1','1 p, 0 n',[('p',0,0)]),('hydrogen-2 (deuterium)','1 p, 1 n',[('p',-10,0),('n',10,0)]),('hydrogen-3 (tritium)','1 p, 2 n',[('p',-11,5),('n',11,5),('n',0,-12)])]
for i,(nm,cnt,parts) in enumerate(iso):
    x=80+i*155; y=215
    o+=f'<circle cx="{x}" cy="{y}" r="44" fill="#eef2fb" stroke="{INK}" stroke-dasharray="4 4"/>'
    for k,dx,dy in parts: o+=(p if k=='p' else n)(x+dx,y+dy,11)
    o+=e(x+40,y-20)
    o+=T(x,y+66,nm.split(' (')[0],14,weight='800')+(T(x,y+84,'('+nm.split(' (')[1],13,weight='600') if '(' in nm else '')+T(x,y+102,cnt+', 1 e&#8722;',13,weight='600')
svg('isotope_notation.svg',470,330,o,'Isotope notation: the element symbol X with the mass number A written at the upper left and the atomic number Z at the lower left. A equals protons plus neutrons; Z equals protons. Below, three isotopes of hydrogen: hydrogen-1 with 1 proton and 0 neutrons, hydrogen-2 (deuterium) with 1 proton and 1 neutron, and hydrogen-3 (tritium) with 1 proton and 2 neutrons; each has 1 electron.')

# 4. Periodic table regions (periods 1-6, no f-block)
PT=[['H','','','','','','','','','','','','','','','','','He'],
['Li','Be','','','','','','','','','','','B','C','N','O','F','Ne'],
['Na','Mg','','','','','','','','','','','Al','Si','P','S','Cl','Ar'],
['K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr'],
['Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe'],
['Cs','Ba','La','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn']]
NONMET={'H','He','C','N','O','F','Ne','P','S','Cl','Ar','Se','Br','Kr','I','Xe','Rn'}
METALLOID={'B','Si','Ge','As','Sb','Te','At'}
cw,ch,x0,y0=25.5,30,12,58; o=''
for c in range(18): o+=T(x0+c*cw+cw/2,y0-8,str(c+1),10,weight='700')
for r,row in enumerate(PT):
    o+=T(x0-6,y0+r*ch+19,str(r+1),10,weight='700',anchor='end')
    for c,s in enumerate(row):
        if not s: continue
        fill='url(#dots)' if s in NONMET else 'url(#hatch)' if s in METALLOID else '#dbe7f6'
        o+=f'<rect x="{x0+c*cw}" y="{y0+r*ch}" width="{cw}" height="{ch}" fill="{fill}" stroke="{INK}" stroke-width=".8"/>'+T(x0+c*cw+cw/2,y0+r*ch+19,s,11,weight='800',extra='stroke="#fff" stroke-width="3" paint-order="stroke"')
o+=T(x0+9*cw,y0-26,'group (column) number',12,weight='600')
by=y0+6*ch+20
for i,(f,lab) in enumerate([('#dbe7f6','metal (plain)'),('url(#hatch)','metalloid (striped)'),('url(#dots)','nonmetal (dotted)')]):
    x=x0+i*150; o+=f'<rect x="{x}" y="{by}" width="22" height="16" fill="{f}" stroke="{INK}"/>'+T(x+28,by+13,lab,13,anchor='start',weight='700')
names=[('Group 1: alkali metals (not H)',),('Group 2: alkaline earth metals',),('Groups 3–12: transition metals',),('Group 17: halogens; Group 18: noble gases',)]
for i,(t,) in enumerate(names): o+=T(x0,by+42+i*19,t,13,anchor='start',weight='600')
o+=T(x0,by+42+4*19,'Rows are periods. Lanthanides and actinides not shown.',12,anchor='start',weight='600')
svg('periodic_regions.svg',484,by+42+4*19+12,o,'Periodic table of periods 1 to 6 with group numbers 1 to 18 across the top. Metals, plain, fill the left and center; nonmetals, dotted, are at the upper right plus hydrogen; metalloids, striped, form a staircase from boron to astatine: B, Si, Ge, As, Sb, Te, At. Group 1 is the alkali metals (not hydrogen), group 2 the alkaline earth metals, groups 3 to 12 the transition metals, group 17 the halogens and group 18 the noble gases. Rows are periods.')

# 5. Ion formation
o=''
def atombox(x,y,w,title,pp,ee,charge):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="78" rx="10" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    s+=T(x+w/2,y+24,title,17,weight='800')+T(x+w/2,y+46,f'{pp} p&#8314;, {ee} e&#8315;',14,weight='600')+T(x+w/2,y+66,'charge: '+charge,14,weight='700')
    return s
o+=atombox(10,20,130,'Na atom',11,11,'0')+arrow(146,59,196,59)+T(171,48,'loses',12,weight='600')+T(171,82,'1 e&#8315;',12,weight='600')
o+=atombox(202,20,130,'Na&#8314; ion',11,10,'1+')+T(400,52,'cation',16,weight='800')+T(400,72,'(positive)',13,weight='600')
o+=atombox(10,130,130,'Cl atom',17,17,'0')+arrow(146,169,196,169)+T(171,158,'gains',12,weight='600')+T(171,192,'1 e&#8315;',12,weight='600')
o+=atombox(202,130,130,'Cl&#8315; ion',17,18,'1&#8722;')+T(400,162,'anion',16,weight='800')+T(400,182,'(negative)',13,weight='600')
o+=T(235,240,'The number of protons never changes when an ion forms;',13,weight='600')+T(235,258,'only the number of electrons does.',13,weight='600')
svg('ion_formation.svg',470,270,o,'Ion formation. A sodium atom, 11 protons and 11 electrons, charge 0, loses 1 electron to become a sodium ion, Na plus, with 11 protons and 10 electrons, charge 1+: a cation. A chlorine atom, 17 protons and 17 electrons, charge 0, gains 1 electron to become a chloride ion, Cl minus, with 17 protons and 18 electrons, charge 1 minus: an anion. The number of protons never changes when an ion forms; only the number of electrons does.')

# 6. Chlorine isotope abundance
o=''
bx,by,bh=70,40,200
o+=f'<line x1="{bx}" y1="{by}" x2="{bx}" y2="{by+bh}" stroke="{INK}" stroke-width="2"/><line x1="{bx}" y1="{by+bh}" x2="440" y2="{by+bh}" stroke="{INK}" stroke-width="2"/>'
for v in (0,25,50,75,100):
    y=by+bh-v*bh/100; o+=f'<line x1="{bx-5}" y1="{y}" x2="{bx}" y2="{y}" stroke="{INK}"/>'+T(bx-9,y+5,str(v),12,anchor='end',weight='600')
o+=T(22,by+bh/2,'abundance (%)',13,weight='700',extra=f'transform="rotate(-90 22 {by+bh/2})"')
for x,v,lab,m in [(140,75.77,'Cl-35','34.97 amu'),(330,24.23,'Cl-37','36.97 amu')]:
    h=v*bh/100; o+=f'<rect x="{x}" y="{by+bh-h}" width="70" height="{h}" fill="url(#hatch)" stroke="{INK}" stroke-width="1.5"/>'
    o+=T(x+35,by+bh-h-8,f'{v}%',14,weight='800')+T(x+35,by+bh+20,lab,14,weight='800')+T(x+35,by+bh+38,m,13,weight='600')
o+=T(255,by+bh+66,'Weighted average: 35.45 amu (the atomic mass on the periodic table)',13,weight='700')
svg('chlorine_isotopes.svg',470,by+bh+78,o,'Bar graph of the natural abundance of chlorine isotopes. Chlorine-35, mass 34.97 amu, makes up 75.77 percent; chlorine-37, mass 36.97 amu, makes up 24.23 percent. The weighted average, 35.45 amu, is the atomic mass on the periodic table.')
print('ok',sorted(os.listdir(OUT)))
