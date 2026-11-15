#!/usr/bin/env python3
"""Chapter 11 figures (SVG), phone-first (~470 px wide). python3 tools/figs_ch11.py"""
import os, math, random
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch11'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
RED="#c0392b"; BLUE="#2f5fa8"; GRN="#2e7d32"; GRAY="#c9d3dc"; GREY2="#55606b"; PUR="#7b4fa0"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=(f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker>'
      f'<marker id="arB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker></defs>')
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.4,c=INK,m='ar'): return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#{m})"/>'
def sub(s,z=10): return f'<tspan baseline-shift="sub" font-size="{z}">{s}</tspan>'
def sup(s,z=10): return f'<tspan baseline-shift="super" font-size="{z}">{s}</tspan>'
def rect(x,y,w,h,fill='#f6fafe',rx=10,sw=1.6,stroke=INK): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def circ(x,y,r,fill='#fff',sw=1.4,stroke=INK): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,c=INK,w=1.6,dash=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'
def water(x,y,ang):  # O toward angle direction reversed
    a=math.radians(ang); s=circ(x,y,7,'#f6d5d1',1.1)
    for d in (-0.75,0.75):
        hx,hy=x-11*math.cos(a+d),y-11*math.sin(a+d); s+=circ(hx,hy,4.2,'#fff',1)
    return s
def beaker(x,y,w,h,fill='#dbe7f6',level=0.75):
    lv=y+h*(1-level)
    return f'<rect x="{x+1}" y="{lv:.1f}" width="{w-2}" height="{y+h-lv-1:.1f}" fill="{fill}"/><path d="M{x} {y} v{h} h{w} v{-h}" fill="none" stroke="{INK}" stroke-width="2.2"/>'

# 1. Dissolving NaCl and like dissolves like
o=T(235,22,'How an ionic compound dissolves in water',16,weight='800')
o+=rect(10,38,450,214)
# crystal on left
for i in range(3):
    for j in range(3):
        cx,cy=40+i*26,120+j*26; na=(i+j)%2==0
        o+=circ(cx,cy,8 if na else 11,'#fde9c8' if na else '#cfe8cf',1.2)+T(cx,cy+4,'+' if na else '−',10,weight='800')
o+=T(66,196,'NaCl crystal',12,weight='800')
o+=arrow(120,146,160,146,2.2)
# hydrated Na+
cx,cy=230,120; o+=circ(cx,cy,10,'#fde9c8',1.4)+T(cx,cy+4,'Na'+sup('+',8),10,weight='800')
for k in range(6):
    a=k*60; r=30; wx,wy=cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a)); o+=water(wx,wy,a+180)
o+=T(cx,182,'O ends (δ−) face Na'+sup('+',8),11,weight='700')
cx,cy=360,120; o+=circ(cx,cy,12,'#cfe8cf',1.4)+T(cx,cy+4,'Cl'+sup('−',8),10,weight='800')
for k in range(6):
    a=k*60+30; r=32; wx,wy=cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a)); o+=water(wx,wy,a)
o+=T(cx,182,'H ends (δ+) face Cl'+sup('−',8),11,weight='700')
o+=T(235,222,'Ion–dipole attractions pull the ions out of the crystal;',12,weight='700')
o+=T(235,240,'each ion is surrounded by water molecules (hydrated).',12,weight='700')
o+=T(235,276,'"Like dissolves like": polar or ionic solutes dissolve in polar solvents;',12,weight='800')
o+=T(235,294,'nonpolar solutes dissolve in nonpolar solvents.',12,weight='800')
svg('dissolving.svg',470,306,o,'How an ionic compound dissolves in water. On the left, a crystal of NaCl made of alternating sodium and chloride ions. An arrow points to two dissolved ions on the right: a sodium ion surrounded by six water molecules with their partially negative oxygen ends facing it, and a chloride ion surrounded by six water molecules with their partially positive hydrogen ends facing it. Ion–dipole attractions pull the ions out of the crystal, and each ion is surrounded by water molecules (hydrated). Like dissolves like: polar or ionic solutes dissolve in polar solvents, and nonpolar solutes dissolve in nonpolar solvents.')

# 2. Solubility curves
o=T(235,22,'Temperature and solubility',16,weight='800')
def plot(x0,y0,w,h,xmax,ymax,xt,yt,xl,yl,series,title):
    s=T(x0+w/2,y0-h-14,title,12.5,weight='800')+line(x0,y0,x0+w,y0,INK,1.8)+line(x0,y0,x0,y0-h,INK,1.8)
    for t in xt: X=x0+w*t/xmax; s+=line(X,y0,X,y0+4,INK,1.2)+T(X,y0+16,str(t),10.5,weight='600')
    for t in yt: Y=y0-h*t/ymax; s+=line(x0-4,Y,x0,Y,INK,1.2)+T(x0-7,Y+4,str(t),10.5,anchor='end',weight='600')+line(x0,Y,x0+w,Y,GRAY,0.8)
    s+=T(x0+w/2,y0+32,xl,11,weight='700')+T(x0-36,y0-h/2,yl,11,weight='700',extra=f'transform="rotate(-90 {x0-36} {y0-h/2})"')
    for pts,col,lab,lx,ly in series:
        s+=f'<polyline points="{" ".join("%.1f,%.1f"%(x0+w*a/xmax,y0-h*b/ymax) for a,b in pts)}" fill="none" stroke="{col}" stroke-width="2.8"/>'
        s+=T(x0+w*lx/xmax,y0-h*ly/ymax,lab,11,anchor='start',weight='800',fill=col)
    return s
kno3=[(0,13.3),(20,31.6),(40,63.9),(60,110),(80,169),(100,246)]
nacl=[(0,35.7),(20,36.0),(40,36.6),(60,37.3),(80,38.4),(100,39.8)]
o+=plot(60,250,170,196,100,250,[0,50,100],[0,50,100,150,200,250],'Temperature (°C)','g per 100 g water',[(kno3,RED,'KNO'+sub('3',9),22,165),(nacl,BLUE,'NaCl',52,55)],'Solids: usually rise')
o2=[(0,14.6),(10,11.3),(20,9.1),(30,7.6),(40,6.4)]
o+=plot(300,250,150,196,40,16,[0,20,40],[0,4,8,12,16],'Temperature (°C)','mg O'+sub('2',8)+' per L',[(o2,GRN,'O'+sub('2',9)+' (1 atm air)',14,13.2)],'Gases: always fall')
o+=T(235,316,'Most solids dissolve better in hot water; gases dissolve better in cold water.',11.5,weight='800')
svg('solubility_curves.svg',470,328,o,'Two graphs of solubility versus temperature. Left, solids, in grams per 100 g of water from 0 to 100 °C: potassium nitrate rises steeply from about 13 g at 0 °C to about 246 g at 100 °C; sodium chloride is nearly flat, from about 36 g to about 40 g. Right, a gas: oxygen dissolved in water in contact with air, in milligrams per liter, falls from about 14.6 mg/L at 0 °C to about 6.4 mg/L at 40 °C. Most solids dissolve better in hot water; gases dissolve better in cold water.')

# 3. Saturation
o=T(235,22,'Unsaturated, saturated, and supersaturated',16,weight='800')
for i,(x,t,d1,d2,extra) in enumerate([(14,'Unsaturated','less than the maximum;','more solid dissolves',0),(170,'Saturated','the maximum at this T;','extra solid stays solid',1),(326,'Supersaturated','more than the maximum;','unstable: a seed crystal','')]):
    o+=beaker(x+25,60,80,110)
    random.seed(i+3)
    n=[8,16,22][i]
    for _ in range(n): o+=circ(x+32+random.random()*66,96+random.random()*68,3,'#9fb6d6',0.8)
    if i==1:
        for k in range(6): o+=f'<rect x="{x+38+k*9}" y="{160-(k%2)*4}" width="7" height="7" fill="#fde9c8" stroke="{INK}" stroke-width="0.8"/>'
    if i==2: o+=f'<rect x="{x+60}" y="70" width="8" height="8" fill="#fde9c8" stroke="{INK}" stroke-width="1"/>'+arrow(x+64,58,x+64,68,1.6)
    o+=T(x+65,192,t,13,weight='800')+T(x+65,210,d1,10.5,weight='600')+T(x+65,224,d2,10.5,weight='600')
o+=T(391,238,'makes solid crash out',10.5,weight='600')
o+=T(235,266,'Solubility = the most solute that dissolves in a given amount of solvent at a given T.',11.5,weight='700')
svg('saturation.svg',470,278,o,'Three beakers of solution. Unsaturated: fewer dissolved particles than the maximum; more solid would dissolve. Saturated: the maximum amount is dissolved at this temperature; extra solid stays undissolved on the bottom. Supersaturated: more dissolved than the maximum; it is unstable, and a seed crystal dropped in makes solid crash out. Solubility is the most solute that dissolves in a given amount of solvent at a given temperature.')

# 4. Henry's law
o=T(235,22,"Henry's law: gas pressure and solubility",16,weight='800')
for i,(x,lab,col,nG,nD) in enumerate([(30,'Sealed: high CO'+sub('2')+' pressure',RED,16,16),(250,'Opened: low CO'+sub('2')+' pressure',BLUE,4,5)]):
    o+=f'<path d="M{x+60} 50 h70 v20 l20 20 v170 a10 10 0 0 1 -10 10 h-90 a10 10 0 0 1 -10 -10 v-170 l20 -20 z" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    o+=f'<rect x="{x+42}" y="112" width="106" height="146" fill="#e3f2e1"/>'+line(x+42,112,x+148,112,GRN,1.6)
    if i==0: o+=f'<rect x="{x+58}" y="38" width="74" height="12" rx="3" fill="{GREY2}"/>'
    random.seed(30+i)
    for _ in range(nG): o+=circ(x+50+random.random()*90,76+random.random()*30,3.4,'#f2b8b0',0.8)
    for _ in range(nD): o+=circ(x+50+random.random()*90,122+random.random()*128,3.4,'#f2b8b0',0.8)
    if i==1:
        for k in range(4): o+=circ(x+70+k*16,180-k*14,5,'#fff',1.2,BLUE)
        o+=arrow(x+95,48,x+95,32,2,BLUE,'arB')
    o+=T(x+95,288,lab,12,weight='800',fill=col)
o+=T(235,316,'More gas pressure above a liquid → more gas dissolves (at the same T).',12.5,weight='800')
svg('henry.svg',470,328,o,"Henry's law, shown with two soda bottles. Left, sealed: the space above the liquid holds CO2 at high pressure, and many CO2 molecules are dissolved in the soda. Right, opened: the CO2 pressure above the liquid drops, CO2 escapes from the bottle, fewer molecules stay dissolved, and bubbles form. More gas pressure above a liquid means more gas dissolves at the same temperature.")

# 5. Dilution
o=T(235,22,'Diluting a stock solution',16,weight='800')
o+=beaker(30,70,90,120,'#c9b6e4',0.8)+T(75,214,'stock: M'+sub('1'),12.5,weight='800')+T(75,232,'concentrated',10.5,weight='600')
random.seed(5)
for _ in range(26): o+=circ(36+random.random()*78,98+random.random()*86,3,PUR,0.6)
o+=f'<path d="M150 60 v100 l6 14 l6 -14 v-100 z" fill="#c9b6e4" stroke="{INK}" stroke-width="1.6"/>'+T(156,196,'pipet V'+sub('1'),11,weight='800')
o+=arrow(178,120,214,120,2.2)
# volumetric flask
o+=f'<path d="M292 46 h16 v70 q50 22 50 70 a10 10 0 0 1 -10 10 h-96 a10 10 0 0 1 -10 -10 q0 -48 50 -70 z" fill="#efe6f8" stroke="{INK}" stroke-width="2"/>'+line(288,70,312,70,RED,2)
for _ in range(9): o+=circ(262+random.random()*76,150+random.random()*40,3,PUR,0.6)
o+=T(300,224,'diluted: M'+sub('2')+', V'+sub('2'),12.5,weight='800')+T(350,72,'fill to the line',10.5,anchor='start',weight='700',fill=RED)
o+=rect(30,244,410,64,'#f6fafe')
o+=T(235,268,'moles of solute stay the same: M'+sub('1')+'V'+sub('1')+' = M'+sub('2')+'V'+sub('2'),14,weight='800')
o+=T(235,292,'Only water is added, so V goes up and M goes down (inverse).',11.5,weight='700')
svg('dilution.svg',470,318,o,'Diluting a stock solution. A beaker of concentrated stock solution (molarity M1) with many solute particles. A pipet removes volume V1 of it and transfers it to a volumetric flask, which is then filled with water to the line, giving a diluted solution with molarity M2 and volume V2 and the same solute particles spread out. The moles of solute stay the same: M1 V1 = M2 V2. Only water is added, so the volume goes up and the molarity goes down, an inverse relationship.')

# 6. Titration
o=T(235,22,'An acid–base titration',16,weight='800')
o+=f'<rect x="96" y="36" width="20" height="170" rx="3" fill="#fff" stroke="{INK}" stroke-width="2"/><rect x="98" y="60" width="16" height="140" fill="#dbe7f6"/>'
for y in range(48,200,16): o+=line(96,y,104,y,INK,1)
o+=T(124,52,'0.00 mL',10,anchor='start',weight='700')+T(124,70,'buret: NaOH,',10.5,anchor='start',weight='800')+T(124,84,'known M',10.5,anchor='start',weight='800')
o+=f'<path d="M102 206 h8 v14 h-2 v10 h-4 v-10 h-2 z" fill="{GREY2}"/>'+circ(106,238,3,'#dbe7f6',1,BLUE)
def flask(cx,fill,lab1,lab2):
    s=f'<path d="M{cx-10} 250 h20 v30 l40 60 a8 8 0 0 1 -7 12 h-86 a8 8 0 0 1 -7 -12 l40 -60 z" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    s+=f'<path d="M{cx-34} 316 h68 l16 24 a8 8 0 0 1 -7 12 h-86 a8 8 0 0 1 -7 -12 z" fill="{fill}"/>'
    return s+T(cx,372,lab1,11.5,weight='800')+T(cx,388,lab2,10.5,weight='600')
o+=flask(106,'#f5f6fb','acid + indicator','colorless at start')
o+=arrow(170,320,230,320,2)
o+=flask(300,'#f7c6dc','endpoint','first lasting faint pink')
o+=rect(250,40,210,170,'#f6fafe')
for i,l in enumerate(['1. mol base = L × M','2. mole ratio from','    the balanced equation','3. M acid = mol acid ÷ L acid']): o+=T(262,70+i*22,l,12,anchor='start',weight='800' if not l.startswith('    ') else '700')
o+=T(355,170,'Volume used = final − initial',11,weight='700')+T(355,188,'buret reading',11,weight='700')
svg('titration.svg',470,400,o,'An acid–base titration. A buret, read from 0.00 mL at the top, holds sodium hydroxide of known molarity. Below it, a flask holds the acid and an indicator, colorless at the start. Base is added drop by drop until the endpoint, when the solution turns a first lasting faint pink. Steps: 1, moles of base = liters times molarity; 2, use the mole ratio from the balanced equation; 3, molarity of acid = moles of acid divided by liters of acid. The volume used is the final buret reading minus the initial reading.')

# 7. Osmosis and red blood cells
o=T(235,22,'Red blood cells in three solutions',16,weight='800')
for i,(x,t,sub1,sub2,shape) in enumerate([(14,'Hypotonic','fewer solutes outside','cell swells, may burst','swell'),(170,'Isotonic','equal solutes','no net water flow','normal'),(326,'Hypertonic','more solutes outside','cell shrinks (crenation)','shrink')]):
    o+=rect(x,40,130,200,'#f6fafe')+T(x+65,62,t,13,weight='800')
    cx,cy=x+65,140
    if shape=='normal': o+=f'<ellipse cx="{cx}" cy="{cy}" rx="38" ry="24" fill="#f2b8b0" stroke="{INK}" stroke-width="1.6"/><ellipse cx="{cx}" cy="{cy}" rx="18" ry="9" fill="#e79a90"/>'
    elif shape=='swell': o+=circ(cx,cy,36,'#f6cbc4',1.6)
    else:
        pts=[];
        for k in range(24):
            a=2*math.pi*k/24; r=26+5*(k%2); pts.append(f'{cx+r*math.cos(a)*1.25:.1f},{cy+r*math.sin(a)*0.8:.1f}')
        o+=f'<polygon points="{" ".join(pts)}" fill="#e79a90" stroke="{INK}" stroke-width="1.6"/>'
    if shape=='swell':
        for a in (0,90,180,270): r=math.radians(a); o+=arrow(cx+58*math.cos(r),cy+58*math.sin(r),cx+40*math.cos(r),cy+40*math.sin(r),2,BLUE,'arB')
    elif shape=='shrink':
        for a in (0,90,180,270): r=math.radians(a); o+=arrow(cx+34*math.cos(r),cy+30*math.sin(r),cx+54*math.cos(r),cy+48*math.sin(r),2,BLUE,'arB')
    else:
        o+=arrow(cx-56,cy-6,cx-42,cy-6,1.6,BLUE,'arB')+arrow(cx-42,cy+6,cx-56,cy+6,1.6,BLUE,'arB')
    o+=T(cx,208,sub1,10.5,weight='700')+T(cx,224,sub2,10.5,weight='700')
o+=T(235,262,'Blue arrows: net flow of water, from lower to higher solute concentration.',11.5,weight='800')
o+=T(235,280,'0.9% NaCl (normal saline) is isotonic with blood.',11.5,weight='700')
svg('osmosis_rbc.svg',470,292,o,'Red blood cells in three solutions. Hypotonic, with fewer solutes outside the cell than inside: water flows into the cell, which swells and may burst (hemolysis). Isotonic, with equal solute concentrations: there is no net flow of water, and the cell keeps its normal disk shape. Hypertonic, with more solutes outside: water flows out of the cell, which shrinks and develops a spiky surface (crenation). Blue arrows show the net flow of water, from lower to higher solute concentration. 0.9% NaCl (normal saline) is isotonic with blood.')
print('ok', sorted(os.listdir(OUT)))
