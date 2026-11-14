#!/usr/bin/env python3
"""Chapter 1 figures (SVG). python3 tools/figs_ch01.py -> figures/ch01/*.svg
Labelled figures are uploaded as files and shown with <img> (LibreTexts' glossary script breaks <text> in inline SVG).
Phone-first: about 470 px wide with 14-16 px text, so labels stay readable (>= 10 px) on a 354 px phone screen.
Colors are never the only cue: every particle carries its element letter and a different size."""
import os, math, random
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch01'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
EL={'H':('#f4f4f4',9,'#333'),'O':('#d9534f',14,'#fff'),'He':('#f2c14e',11,'#333'),'Ne':('#7fb8e0',12,'#333'),'N':('#4a6fd1',13,'#fff'),'C':('#555',13,'#fff'),'Na':('#9b6cc4',14,'#fff'),'Cl':('#5cb85c',15,'#fff')}
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
def atom(x,y,el,sc=1.0):
    c,r,tc=EL[el]; r*=sc
    s=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{c}" stroke="{INK}" stroke-width="1.4"/>'
    fs=11 if len(el)==1 else 9
    return s+T(x,y+fs*0.36,el,fs*sc,weight='800',fill=tc)
def mol(x,y,parts,rot):
    """parts: list of element symbols; first is central."""
    o=''; n=len(parts); ca,sa=math.cos(rot),math.sin(rot)
    if n==1: return atom(x,y,parts[0])
    if n==2:
        d=EL[parts[0]][1]*0.8
        pts=[(-d,0),(d,0)]
    else: # bent triatomic (water-like) central first
        r0=EL[parts[0]][1]; pts=[(0,0)]
        for a in (-38,218):
            ar=math.radians(a); pts.append(((r0+3)*math.cos(ar),(r0+3)*math.sin(ar)))
    order=list(range(1,n))+[0] if n==3 else list(range(n))
    for i in order:
        px,py=pts[i]; o+=atom(x+px*ca-py*sa,y+px*sa+py*ca,parts[i])
    return o
def box(x,y,w,h,items,seed,title=None,cluster=False):
    rnd=random.Random(seed); o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    placed=[]
    for k,(parts) in enumerate(items):
        ext=max(EL[p][1] for p in parts)*(1 if len(parts)==1 else 2.0)+3
        best=None;bd=-1e9
        for t in range(800):
            if cluster and isinstance(cluster,dict):
                x0,x1=cluster[tuple(parts)]; px=x+ext+x0*(w-2*ext)+rnd.random()*(x1-x0)*(w-2*ext)
            else: px=x+ext+rnd.random()*(w-2*ext)
            py=y+ext+rnd.random()*(h-2*ext)
            d=min([math.hypot(px-a,py-b)-e-ext for a,b,e in placed] or [99])
            if d>bd: bd=d;best=(px,py)
            if d>6: break
        placed.append((best[0],best[1],ext)); o+=mol(best[0],best[1],parts,rnd.random()*6.28)
    if title:
        for i,line in enumerate(title): o+=T(x+w/2,y+h+22+i*19,line,15 if i==0 else 13,weight='800' if i==0 else '600')
    return o
def svg(name,W,H,body,aria):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{body}</svg>'
    open(os.path.join(OUT,name),'w').write(s)


defs=f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>'
def arrow(x,y,dx,dy=0):
    return f'<path d="M{x} {y} l{dx} {dy}" stroke="{INK}" stroke-width="3" marker-end="url(#ar)"/>'

# --- Figure: particle views of elements, compounds, mixtures (2 columns x 3 rows)
bw,bh=215,160; o=''
panels=[
 ([['He']]*9,['(a) Element','atoms of one kind (He)']),
 ([['O','O']]*6,['(b) Element','molecules of one element (O₂)']),
 ([['O','H','H']]*6,['(c) Compound','two elements bonded (H₂O)']),
 ([['He']]*5+[['Ne']]*5,['(d) Mixture of elements','He and Ne atoms, not bonded']),
 ([['O','O']]*4+[['N','N']]*4,['(e) Mixture of elements','N₂ and O₂, like air']),
 ([['O','H','H']]*4+[['O','O']]*3,['(f) Mixture','compound (H₂O) with O₂']),
]
for i,(items,title) in enumerate(panels):
    cx=8+(i%2)*240; cy=8+(i//2)*222
    o+=box(cx,cy,bw,bh,items,11+i*7,title)
svg('particles_classify.svg',470,670,o,'Six boxes of particles. (a) Helium atoms, all alike: an element. (b) O2 molecules, each two oxygen atoms bonded: an element. (c) Water molecules, one O bonded to two H: a compound. (d) Separate helium and neon atoms: a mixture of elements. (e) N2 and O2 molecules together, like air: a mixture of elements. (f) Water molecules with O2 molecules: a mixture of a compound and an element.')

# --- Figure: solid / liquid / gas, stacked rows (box left, words right)
o=defs; rnd=random.Random(4)
def frame(y): return f'<rect x="8" y="{y}" width="190" height="150" rx="10" fill="#fff" stroke="{INK}" stroke-width="2"/>'
y0=8; o+=frame(y0)
for r in range(5):
    for c in range(6): o+=atom(26+c*30,y0+18+r*28.5,'Ne')
y1=178; o+=frame(y1); pts=[]
tries=0
while len(pts)<18 and tries<20000:
    tries+=1; px,py=8+16+rnd.random()*158, y1+48+rnd.random()*80
    if all(math.hypot(px-a,py-b)>24 for a,b in pts): pts.append((px,py))
for px,py in pts: o+=atom(px,py,'Ne')
y2=348; o+=frame(y2)
for px,py,dx,dy in [(45,y2+35,16,8),(140,y2+30,-14,12),(170,y2+120,-8,-16),(55,y2+120,16,-6),(105,y2+80,12,12)]:
    o+=atom(px,py,'Ne')+arrow(px+dx*0.9,py+dy*0.9,dx*1.2,dy*1.2)
lab=[('(a) Solid',['Fixed shape and volume.','Particles packed in rows,','vibrating in place.']),('(b) Liquid',['Fixed volume; takes the','shape of its container.','Particles touch but slide.']),('(c) Gas',['Fills its whole container.','Particles far apart,','moving fast.'])]
for i,(t,ls) in enumerate(lab):
    yy=[y0,y1,y2][i]+48; o+=T(215,yy,t,17,anchor='start',weight='800')
    for j,l in enumerate(ls): o+=T(215,yy+24+j*20,l,15,anchor='start',weight='600')
svg('states.svg',470,506,o,'Three boxes of neon atoms, stacked. (a) Solid: atoms packed in neat rows; fixed shape and volume; particles vibrate in place. (b) Liquid: atoms touching but disordered, filling the bottom of the box; fixed volume, takes the shape of the container; particles slide past each other. (c) Gas: a few atoms far apart with arrows showing fast motion; fills its container.')

# --- Figure: electric charges
def charge(x,y,s):
    c='#d9534f' if s=='+' else '#4a6fd1'
    return f'<circle cx="{x}" cy="{y}" r="22" fill="{c}" stroke="{INK}" stroke-width="2"/>'+T(x,y+10,'+' if s=='+' else '−',30,weight='900',fill='#fff')
o=defs
rows=[('+','+','repel','Like charges repel'),('−','−','repel','Like charges repel'),('+','−','attract','Opposite charges attract')]
for i,(a,b,kind,lab) in enumerate(rows):
    y=40+i*92; xa,xb=170,300
    o+=charge(xa,y,a)+charge(xb,y,b)
    if kind=='repel': o+=arrow(xa-28,y,-44)+arrow(xb+28,y,44)
    else: o+=arrow(xa+28,y,30)+arrow(xb-28,y,-30)
    o+=T(235,y+50,lab,16,weight='800')
o+=f'<line x1="10" y1="300" x2="460" y2="300" stroke="#999" stroke-dasharray="5 5"/>'
o+=charge(70,350,'+')+charge(125,350,'−')+T(98,400,'Close together:',15)+T(98,420,'strong attraction',15,weight='600')
o+=charge(270,350,'+')+charge(430,350,'−')+T(350,400,'Far apart:',15)+T(350,420,'weaker attraction',15,weight='600')
svg('charges.svg',470,432,o,'Top: two positive charges push apart, two negative charges push apart, and a positive and a negative charge pull together. Bottom: a positive and a negative charge close together attract strongly; the same pair far apart attracts more weakly.')

# --- Figure: scientific method (vertical)
o=defs
steps=[('Observe','qualitative and quantitative data'),('Ask a question',''),('Hypothesis','a testable, falsifiable explanation'),('Experiment','change one variable; keep a control'),('Analyze','do the data support the hypothesis?')]
for i,(a,b) in enumerate(steps):
    y=10+i*84; o+=f'<rect x="20" y="{y}" width="300" height="62" rx="12" fill="#eef5fb" stroke="{INK}" stroke-width="2"/>'
    o+=T(170,y+(26 if b else 37),a,17,weight='800')+(T(170,y+48,b,14,weight='600') if b else '')
    if i<4: o+=arrow(170,y+62,0,16)
o+=f'<path d="M320 377 h30 V209 h-26" fill="none" stroke="{INK}" stroke-width="2.4" stroke-dasharray="6 4" marker-end="url(#ar)"/>'
o+=T(358,280,'not',14,anchor='start',weight='700')+T(358,297,'supported:',14,anchor='start',weight='700')
o+=T(358,314,'revise and',14,anchor='start',weight='700')+T(358,331,'test again',14,anchor='start',weight='700')
o+=arrow(170,434,0,18)
o+=T(235,470,'Results confirmed many times build:',14,weight='700')
o+=f'<rect x="8" y="482" width="220" height="74" rx="12" fill="#f1f8f3" stroke="{INK}" stroke-width="2"/>'+T(118,508,'Scientific law',16,weight='800')+T(118,528,'describes WHAT happens',13,weight='600')+T(118,546,'(often an equation)',13,weight='600')
o+=f'<rect x="242" y="482" width="220" height="74" rx="12" fill="#f1f8f3" stroke="{INK}" stroke-width="2"/>'+T(352,508,'Scientific theory',16,weight='800')+T(352,528,'explains WHY it happens',13,weight='600')+T(352,546,'(tested many times)',13,weight='600')
svg('method.svg',470,566,o,'Flowchart of the scientific method, top to bottom: observe (qualitative and quantitative data), ask a question, form a testable, falsifiable hypothesis, experiment (change one variable and keep a control), analyze (do the data support the hypothesis?). A dashed arrow from analyze back to hypothesis says: not supported, revise and test again. Results confirmed many times build scientific laws, which describe what happens, often as an equation, and scientific theories, which explain why it happens.')

# --- Figure: classification flowchart (two columns)
o=defs
def node(x,y,w,t1,t2='',fill='#eef5fb'):
    s=f'<rect x="{x-w/2}" y="{y}" width="{w}" height="{58 if t2 else 40}" rx="10" fill="{fill}" stroke="{INK}" stroke-width="2"/>'+T(x,y+25,t1,16,weight='800')
    if t2: s+=T(x,y+46,t2,14,weight='600')
    return s
def line(x1,y1,x2,y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK}" stroke-width="2" marker-end="url(#ar)"/>'
def it(x,y,t,anchor='middle'): return T(x,y,t,13,anchor=anchor,weight='600',extra='font-style="italic"')
o+=node(235,8,230,'Matter','has mass, takes up space')
o+=line(190,66,125,112)+line(280,66,345,112)
o+=it(118,90,'one kind',anchor='end')+it(118,104,'of particle',anchor='end')+it(352,90,'two or more kinds,',anchor='start')+it(352,104,'not bonded',anchor='start')
o+=node(118,114,212,'Pure substance','fixed composition')+node(352,114,212,'Mixture','variable composition')
o+=line(118,172,118,210)+line(352,172,352,210)
o+=node(118,212,212,'Element','one kind of atom: He, O₂, Fe',fill='#fff')
o+=node(352,212,212,'Homogeneous','uniform: saline, air',fill='#fff')
o+=it(118,292,'or')+it(352,292,'or')
o+=node(118,302,212,'Compound','elements bonded: H₂O, NaCl',fill='#fff')
o+=node(352,302,212,'Heterogeneous','not uniform: whole blood',fill='#fff')
o+=it(118,388,'separated only by')+it(118,404,'chemical change')+it(352,388,'separated by')+it(352,404,'physical methods')
svg('classify_flow.svg',470,414,o,'Flowchart. Matter divides into pure substances (one kind of particle, fixed composition) and mixtures (two or more kinds, not bonded, variable composition). A pure substance is either an element (one kind of atom: He, O2, Fe) or a compound (elements bonded: H2O, NaCl); pure substances are separated only by chemical change. A mixture is either homogeneous (uniform: saline, air) or heterogeneous (not uniform: whole blood); mixtures are separated by physical methods.')

# --- Figure: density column
o=''
layers=[(250,330,'#e8b04a','Corn syrup','1.37 g/mL'),(170,250,'#bfe0f5','Water','1.00 g/mL'),(110,170,'#f6e7a1','Vegetable oil','0.92 g/mL')]
for y1,y2,c,n,d in layers:
    o+=f'<rect x="42" y="{y1}" width="136" height="{y2-y1}" fill="{c}"/>'
    o+=f'<line x1="190" y1="{(y1+y2)/2}" x2="214" y2="{(y1+y2)/2}" stroke="{INK}" stroke-width="1.5"/>'
    o+=T(222,(y1+y2)/2-2,n,16,anchor='start',weight='800')+T(222,(y1+y2)/2+17,d,15,anchor='start',weight='600')
o+=f'<path d="M42 330 a12 12 0 0 0 12 12 h112 a12 12 0 0 0 12 -12 z" fill="#e8b04a"/>'
o+=f'<path d="M40 30 v300 a14 14 0 0 0 14 14 h112 a14 14 0 0 0 14 -14 v-300" fill="none" stroke="{INK}" stroke-width="3"/>'
o+=f'<rect x="90" y="104" width="28" height="22" rx="3" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'+T(104,120,'C',13)
o+=f'<circle cx="130" cy="250" r="13" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'+T(130,255,'P',13)
o+=f'<rect x="65" y="315" width="28" height="18" rx="3" fill="#aaa" stroke="{INK}" stroke-width="1.5"/>'+T(79,329,'S',13)
leg=['C = cork (0.24 g/mL): floats on the oil.','P = plastic bead (1.05 g/mL): sinks in water,','       floats on corn syrup.','S = steel nut (7.9 g/mL): sinks to the bottom.','Densest layer on the bottom, least dense on top.']
for j,l in enumerate(leg): o+=T(12,378+j*21,l.replace('       ','  '),15,anchor='start',weight='600',extra='xml:space="preserve"')
svg('density_column.svg',470,478,o,'A tall cylinder with three liquid layers: corn syrup (1.37 g/mL) on the bottom, water (1.00 g/mL) in the middle, vegetable oil (0.92 g/mL) on top. A cork (0.24 g/mL) floats at the top of the oil, a plastic bead (1.05 g/mL) rests at the boundary between the water and the syrup, and a steel nut (7.9 g/mL) lies on the bottom.')
print('ok', sorted(os.listdir(OUT)))
