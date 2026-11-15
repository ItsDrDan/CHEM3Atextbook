#!/usr/bin/env python3
"""Chapter 12 figures (SVG), phone-first (~470 px wide, labels 14 px or larger). python3 tools/figs_ch12.py"""
import os, math, random
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch12'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
RED="#c0392b"; BLUE="#2f5fa8"; GRN="#2e7d32"; GRAY="#c9d3dc"; GREY2="#55606b"; PUR="#7b4fa0"; ORG="#c56a00"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=(f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker>'
      f'<marker id="arR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{RED}"/></marker>'
      f'<marker id="arB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker></defs>')
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.4,c=INK,m='ar'): return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#{m})"/>'
def sub(s,z=11): return f'<tspan baseline-shift="sub" font-size="{z}">{s}</tspan>'
def sup(s,z=11): return f'<tspan baseline-shift="super" font-size="{z}">{s}</tspan>'
def rect(x,y,w,h,fill='#f6fafe',rx=10,sw=1.6,stroke=INK): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def circ(x,y,r,fill='#fff',sw=1.4,stroke=INK): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,c=INK,w=1.6,dash=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'
def beaker(x,y,w,h,fill='#dbe7f6',level=0.8):
    lv=y+h*(1-level)
    return f'<rect x="{x+1}" y="{lv:.1f}" width="{w-2}" height="{y+h-lv-1:.1f}" fill="{fill}"/><path d="M{x} {y} v{h} h{w} v{-h}" fill="none" stroke="{INK}" stroke-width="2.2"/>'
H3O='H'+sub('3')+'O'+sup('+'); OH='OH'+sup('−')

# 1. pH scale with everyday substances (vertical, phone-first)
W,H=470,684
o=T(235,26,'The pH scale',18,weight='800')
x0=150; top=60; step=40  # pH 0 at top, 14 at bottom
cols=['#b71c1c','#c62828','#d84315','#ef6c00','#f9a825','#c0ca33','#7cb342','#43a047','#00897b','#0097a7','#0277bd','#1565c0','#283593','#4527a0','#6a1b9a']
for p in range(15):
    y=top+p*step
    o+=f'<rect x="{x0}" y="{y-step/2:.1f}" width="34" height="{step}" fill="{cols[p]}" opacity="0.85"/>'
    o+=T(x0-10,y+5,str(p),15,anchor='end',weight='800')
o+=f'<rect x="{x0}" y="{top-step/2}" width="34" height="{15*step}" fill="none" stroke="{INK}" stroke-width="1.6"/>'
o+=T(x0-10,top-28,'pH',15,anchor='end',weight='800')
# [H3O+] labels on far left
o+=T(14,top-28,'[H'+sub('3')+'O'+sup('+')+'] (M)',14,anchor='start',weight='800')
for p in (0,2,4,7,10,12,14):
    y=top+p*step; o+=T(14,y+5,'10'+sup('−'+str(p) if p else '0'),14,anchor='start',weight='700',fill=GREY2)
# substances on right
items=[(1.5,'stomach acid (1.5–3.5)'),(2.0,'lemon juice (about 2)'),(2.6,'cola soft drink (about 2.5)'),(3.0,'vinegar (about 3)'),
       (5.0,'black coffee (about 5)'),(6.5,'milk (about 6.5)'),(7.0,'pure water (7.00, neutral)'),(8.3,'baking soda in water (about 8.3)'),
       (10.5,'milk of magnesia (about 10.5)'),(11.5,'household ammonia (about 11.5)'),(12.6,'bleach (about 12.5)'),(13.8,'drain cleaner (about 14)')]
lx=x0+60
used=[]
for p,lab in items:
    y=top+p*step
    ty=y+5
    for u in used:
        if abs(ty-u)<22: ty=u+22
    used.append(ty)
    o+=line(x0+34,y,lx-4,ty-5,INK,1.3)+circ(x0+34,y,2.5,INK,0.5,INK)
    o+=T(lx,ty,lab,14,anchor='start',weight='700')
# blood band
yb1=top+7.35*step; yb2=top+7.45*step
o+=f'<rect x="{x0-4}" y="{yb1:.1f}" width="42" height="{yb2-yb1:.1f}" fill="none" stroke="#000" stroke-width="2.4"/>'
# blood label placed in gap between water (7) and baking soda (8.3)
yl=top+7.65*step+6
o+=line(x0+38,(yb1+yb2)/2,lx-4,yl-5,RED,2)
o+=T(lx,yl,'blood (7.35–7.45)',14,anchor='start',weight='800',fill=RED)
o+=arrow(110,top+6.2*step,110,top+0.4*step,2.4)+T(100,top+3.3*step,'more acidic',14,weight='800',extra=f'transform="rotate(-90 100 {top+3.3*step})"')
o+=arrow(110,top+7.8*step,110,top+13.6*step,2.4)+T(100,top+10.7*step,'more basic',14,weight='800',extra=f'transform="rotate(-90 100 {top+10.7*step})"')
o+=T(235,H-14,'Each step of 1 pH unit is a 10-fold change in [H'+sub('3')+'O'+sup('+')+'].',14,weight='800')
svg('ph_scale.svg',W,H,o,'The pH scale from 0 at the top to 14 at the bottom, with the hydronium ion concentration from 1 M (10 to the 0) at pH 0 to 10 to the minus 14 M at pH 14. Lower pH is more acidic; higher pH is more basic. Typical values: stomach acid 1.5 to 3.5, lemon juice about 2, cola about 2.5, vinegar about 3, black coffee about 5, milk about 6.5, pure water 7.00 (neutral), blood 7.35 to 7.45 (a narrow boxed band just above 7), baking soda in water about 8.3, milk of magnesia about 10.5, household ammonia about 11.5, bleach about 12.5, drain cleaner about 14. Each step of one pH unit is a tenfold change in hydronium ion concentration.')

# 2. Red cabbage indicator colors
W,H=470,300
o=T(235,26,'Red cabbage indicator colors',18,weight='800')
cab=[('1–2','red','#c2185b'),('3–4','pink','#d81b60'),('5–7','purple','#7b1fa2'),('8','blue','#3949ab'),('9–11','green','#2e7d32'),('12–14','yellow','#f9a825')]
bw=66
for i,(p,c,hexc) in enumerate(cab):
    x=20+i*(bw+7)
    o+=beaker(x,60,bw,110,hexc,0.78)
    o+=T(x+bw/2,196,'pH '+p,14,weight='800')
    o+=T(x+bw/2,216,c,15,weight='800')
o+=arrow(200,244,40,244,2.4)+T(120,268,'more acidic',14,weight='800')
o+=arrow(270,244,430,244,2.4)+T(350,268,'more basic',14,weight='800')
o+=T(235,292,'Colors are approximate; shades vary with the cabbage.',14,weight='600',fill=GREY2)
svg('cabbage_indicator.svg',W,H,o,'Six beakers of red cabbage indicator in solutions of different pH, each labeled with its pH range and color name: pH 1 to 2 red, pH 3 to 4 pink, pH 5 to 7 purple, pH 8 blue, pH 9 to 11 green, and pH 12 to 14 yellow. Acidic solutions give red and pink; basic solutions give blue, green, and yellow. Colors are approximate and vary with the cabbage.')

# 3. Conjugate acid-base pairs
W,H=470,300
o=T(235,26,'Conjugate acid–base pairs',18,weight='800')
y=150
xs=[50,150,300,410]
o+=T(xs[0],y,'HF',22,weight='800')+T(100,y,'+',22)+T(xs[1],y,'H'+sub('2',15)+'O',22,weight='800')
o+=T(225,y-2,'⇌',28,weight='700')
o+=T(xs[2],y,'F'+sup('−',16),22,weight='800')+T(355,y,'+',22)+T(xs[3],y,'H'+sub('3',15)+'O'+sup('+',16),22,weight='800')
o+=T(xs[0],y+30,'acid',15,weight='800',fill=RED)+T(xs[1],y+30,'base',15,weight='800',fill=BLUE)
o+=T(xs[2],y+30,'conjugate',15,weight='800',fill=RED)+T(xs[2],y+48,'base',15,weight='800',fill=RED)
o+=T(xs[3],y+30,'conjugate',15,weight='800',fill=BLUE)+T(xs[3],y+48,'acid',15,weight='800',fill=BLUE)
# pair 1 bracket above (HF -> F-)
o+=f'<path d="M{xs[0]} {y-28} V{y-60} H{xs[2]} V{y-28}" fill="none" stroke="{RED}" stroke-width="2.4" marker-end="url(#arR)"/>'
o+=T((xs[0]+xs[2])/2,y-68,'pair 1: HF loses H'+sup('+')+' → F'+sup('−'),15,weight='800',fill=RED)
# pair 2 bracket below (H2O -> H3O+)
o+=f'<path d="M{xs[1]} {y+58} V{y+90} H{xs[3]} V{y+58}" fill="none" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#arB)"/>'
o+=T((xs[1]+xs[3])/2,y+112,'pair 2: H'+sub('2')+'O gains H'+sup('+')+' → H'+sub('3')+'O'+sup('+'),15,weight='800',fill=BLUE)
o+=T(235,292,'Each pair differs by exactly one H'+sup('+')+' (one proton).',15,weight='800')
svg('conjugate_pairs.svg',W,H,o,'The reaction HF plus H2O in equilibrium with F minus plus H3O plus, with labels. HF is the acid and F minus is its conjugate base; a red bracket above connects them and reads pair 1: HF loses H plus to become F minus. H2O is the base and H3O plus is its conjugate acid; a blue bracket below connects them and reads pair 2: H2O gains H plus to become H3O plus. Each pair differs by exactly one H plus, one proton. The labels name each role, so the colors are not needed to read the figure.')

# 4. Strong vs weak acid particle picture
W,H=470,360
o=T(235,26,'Strong acid vs weak acid in water',18,weight='800')
def mol_HA(x,y,A='Cl'):
    return circ(x-7,y,6,'#fff',1.2)+circ(x+7,y,9,'#cfe8cf',1.2)+T(x-7,y+4,'H',9,weight='800')+T(x+7,y+4,A[0],9,weight='800')
def h3o(x,y): return circ(x,y,9,'#f6d5d1',1.2)+T(x,y+4,'+',13,weight='800')
def anion(x,y): return circ(x,y,9,'#cfe8cf',1.2)+T(x,y+4,'−',14,weight='800')
for k,(bx,title,sub1) in enumerate([(30,'Strong: HCl','all ionized'),(250,'Weak: HF','mostly molecules')]):
    o+=T(bx+95,58,title,16,weight='800')
    o+=beaker(bx,72,190,170,'#e6eff9',0.88)
    random.seed(7+k)
    pts=[]
    for r in range(4):
        for c in range(4):
            pts.append((bx+30+c*42+random.uniform(-6,6)+(10 if r%2 else 0), 108+r*34+random.uniform(-5,5)))
    random.shuffle(pts)
    if k==0:
        for i,(x,y) in enumerate(pts[:16]): o+=h3o(x,y) if i%2==0 else anion(x,y)
    else:
        for i,(x,y) in enumerate(pts[:12]): o+=mol_HA(x,y,'F')
        o+=h3o(*pts[12])+anion(*pts[13])
    o+=T(bx+95,264,sub1,15,weight='800')
o+=T(125,286,'8 H'+sub('3')+'O'+sup('+')+' + 8 Cl'+sup('−'),15,weight='700')
o+=T(345,286,'12 HF, 1 H'+sub('3')+'O'+sup('+')+', 1 F'+sup('−'),15,weight='700')
# legend
o+=h3o(60,322)+T(76,327,'= H'+sub('3')+'O'+sup('+'),14,anchor='start')
o+=anion(170,322)+T(186,327,'= anion',14,anchor='start')
o+=mol_HA(290,322,'F')+T(308,327,'= HF molecule',14,anchor='start')
o+=T(235,352,'Water molecules are not shown.',14,weight='600',fill=GREY2)
svg('strong_weak.svg',W,H,o,'Particle pictures of two acids in water. Left, the strong acid HCl: the beaker holds only ions, 8 hydronium ions and 8 chloride ions, and no HCl molecules, because a strong acid ionizes completely. Right, the weak acid HF: the beaker holds 12 intact HF molecules and only 1 hydronium ion and 1 fluoride ion, because a weak acid ionizes only slightly. Water molecules are not shown.')

# 5. pH / pOH / concentration map
W,H=470,400
o=T(235,26,'Moving among pH, pOH, [H'+sub('3')+'O'+sup('+')+'], and [OH'+sup('−')+']',17,weight='800')
bx=[(20,56),(300,56),(20,226),(300,226)]
names=['[H'+sub('3')+'O'+sup('+')+']','[OH'+sup('−')+']','pH','pOH']
fills=['#fde9e7','#e3ecf8','#fde9e7','#e3ecf8']
for (x,y),n,f in zip(bx,names,fills):
    o+=rect(x,y,150,52,f)+T(x+75,y+34,n,19,weight='800')
o+=line(170,82,300,82,INK,2.2)
o+=T(235,72,'[H'+sub('3')+'O'+sup('+')+'][OH'+sup('−')+']',14,weight='800')+T(235,104,'= 1.0 × 10'+sup('−14'),14,weight='800')
o+=line(170,252,300,252,INK,2.2)
o+=T(235,242,'pH + pOH',14,weight='800')+T(235,274,'= 14.00',14,weight='800')
o+=arrow(50,110,50,222,2.2)+T(58,160,'−log',15,anchor='start',weight='800')
o+=arrow(140,222,140,110,2.2)+T(148,180,'10'+sup('−pH'),15,anchor='start',weight='800')
o+=arrow(420,110,420,222,2.2)+T(412,160,'−log',15,anchor='end',weight='800')
o+=arrow(330,222,330,110,2.2)+T(322,180,'10'+sup('−pOH'),15,anchor='end',weight='800')
o+=T(235,314,'pH = −log[H'+sub('3')+'O'+sup('+')+'];  [H'+sub('3')+'O'+sup('+')+'] = 10'+sup('−pH'),15,weight='800')
o+=T(235,342,'pOH = −log[OH'+sup('−')+'];  [OH'+sup('−')+'] = 10'+sup('−pOH'),15,weight='800')
o+=T(235,384,'All at 25 °C. Start from whatever you are given.',14,weight='600',fill=GREY2)
svg('ph_map.svg',W,H,o,'A map connecting four quantities in boxes: hydronium concentration and hydroxide concentration across the top, pH and pOH across the bottom. Across the top: hydronium concentration times hydroxide concentration equals 1.0 times 10 to the minus 14. Across the bottom: pH plus pOH equals 14.00. Down the left: pH equals minus log of hydronium concentration, and back up: hydronium concentration equals 10 to the minus pH. Down the right: pOH equals minus log of hydroxide concentration, and back up: hydroxide concentration equals 10 to the minus pOH. All values are at 25 degrees Celsius; start from whatever you are given.')

# 6. Buffer neutralizing added acid and base
W,H=470,470
o=T(235,26,'How a buffer resists pH change',18,weight='800')
o+=rect(30,46,410,98,'#f3eef8')
o+=T(235,72,'Buffer: a weak acid + its conjugate base',15,weight='800')
o+=T(235,100,'HA (weak acid)   and   A'+sup('−')+' (conjugate base)',15,weight='700')
o+=T(235,126,'e.g., H'+sub('2')+'CO'+sub('3')+' and HCO'+sub('3')+sup('−')+' in blood',15,weight='700')
# left: add acid
o+=arrow(160,148,95,196,2.4)+arrow(310,148,375,196,2.4)
o+=rect(10,200,220,190,'#fde9e7')
o+=T(120,226,'Add acid (H'+sub('3')+'O'+sup('+')+')',16,weight='800',fill=RED)
o+=T(120,252,'the base part reacts:',14,weight='700')
o+=T(120,284,'A'+sup('−')+' + H'+sub('3')+'O'+sup('+'),16,weight='800')
o+=T(120,308,'→ HA + H'+sub('2')+'O',16,weight='800')
o+=T(120,342,'strong acid is used up;',14,weight='700')
o+=T(120,362,'a weak acid forms',14,weight='700')
o+=rect(240,200,220,190,'#e3ecf8')
o+=T(350,226,'Add base (OH'+sup('−')+')',16,weight='800',fill=BLUE)
o+=T(350,252,'the acid part reacts:',14,weight='700')
o+=T(350,284,'HA + OH'+sup('−'),16,weight='800')
o+=T(350,308,'→ A'+sup('−')+' + H'+sub('2')+'O',16,weight='800')
o+=T(350,342,'strong base is used up;',14,weight='700')
o+=T(350,362,'a weak base forms',14,weight='700')
o+=T(235,420,'Either way, the pH changes only a little,',15,weight='800')
o+=T(235,442,'until one part of the buffer runs out.',15,weight='800')
svg('buffer.svg',W,H,o,'How a buffer resists pH change. Top: a buffer contains a weak acid, HA, and its conjugate base, A minus, for example carbonic acid and bicarbonate in blood. Left, add acid: the base part reacts, A minus plus H3O plus gives HA plus water, so the strong acid is used up and a weak acid forms. Right, add base: the acid part reacts, HA plus OH minus gives A minus plus water, so the strong base is used up and a weak base forms. Either way the pH changes only a little, until one part of the buffer runs out.')
print('wrote', sorted(os.listdir(OUT)))
