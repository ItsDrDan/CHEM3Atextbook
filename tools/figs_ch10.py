#!/usr/bin/env python3
"""Chapter 10 figures (SVG), phone-first (~470 px wide). python3 tools/figs_ch10.py"""
import os, math, random
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch10'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
RED="#c0392b"; BLUE="#2f5fa8"; GRN="#2e7d32"; GRAY="#c9d3dc"; GREY2="#55606b"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=(f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker>'
      f'<marker id="arR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{RED}"/></marker>'
      f'<marker id="arB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker></defs>')
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.4,c=INK,m='ar'): return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#{m})"/>'
def sub(s,z=10): return f'<tspan baseline-shift="sub" font-size="{z}">{s}</tspan>'
def rect(x,y,w,h,fill='#f6fafe',rx=10,sw=1.6,stroke=INK): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def circ(x,y,r,fill='#fff',sw=1.4,stroke=INK): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,c=INK,w=1.6,dash=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'
def dots(x,y,w,h,n,seed,r=4.5,fill='#9fb6d6',arrows=False):
    random.seed(seed); s=''
    for _ in range(n):
        px=x+r+3+random.random()*(w-2*r-6); py=y+r+3+random.random()*(h-2*r-6)
        s+=circ(px,py,r,fill,1)
        if arrows:
            a=random.uniform(0,6.28); s+=arrow(px+r*math.cos(a),py+r*math.sin(a),px+(r+12)*math.cos(a),py+(r+12)*math.sin(a),1.3,BLUE,'arB')
    return s

# 1. Kinetic molecular theory
o=T(235,22,'Kinetic molecular theory of gases',16,weight='800')
o+=f'<rect x="14" y="40" width="200" height="200" fill="#fff" stroke="{INK}" stroke-width="2.4"/>'
o+=dots(14,40,200,200,11,19,5,'#9fb6d6',True)
o+=circ(200,110,5,'#f2b8b0',1)+arrow(196,104,180,92,1.4,RED,'arR')+T(206,92,'hit',10,anchor='start',weight='800',fill=RED)
o+=T(114,258,'Gas particles in a container',12,weight='700')
pts=['1. Particles are tiny and far apart;','   most of a gas is empty space.','2. They move constantly, randomly,','   in straight lines.','3. Collisions are elastic (no energy','   is lost); hits on the walls','   cause pressure.','4. No attractions or repulsions','   between particles.','5. Average kinetic energy is','   proportional to Kelvin temperature.']
for i,p in enumerate(pts): o+=T(228,56+i*18,p,11.5,anchor='start',weight='700' if p[0].isdigit() else '600')
svg('kmt.svg',470,272,o,'Kinetic molecular theory of gases. Left: a square container with eleven widely spaced gas particles, each with an arrow showing it moving in a random direction; one particle is shown hitting the wall. Right, the five main ideas: 1, particles are tiny and far apart, so most of a gas is empty space. 2, they move constantly and randomly in straight lines. 3, collisions are elastic, so no energy is lost, and hits on the walls cause pressure. 4, there are no attractions or repulsions between particles. 5, the average kinetic energy is proportional to the Kelvin temperature.')

# 2. Barometer
o=T(235,22,'A mercury barometer',16,weight='800')
o+=f'<path d="M112 48 h22 v236" fill="none" stroke="{INK}" stroke-width="2.2"/><path d="M112 48 v236" stroke="{INK}" stroke-width="2.2"/>'
o+=f'<rect x="114" y="84" width="18" height="214" fill="#b8c2cc"/>'
o+=T(160,66,'vacuum',11.5,anchor='start',weight='700')+line(136,64,156,64,GREY2,1)
o+=f'<path d="M40 262 v50 h168 v-50" fill="none" stroke="{INK}" stroke-width="2.2"/><rect x="42" y="282" width="164" height="28" fill="#b8c2cc"/>'
o+=T(124,330,'dish of mercury (Hg)',11.5,weight='700')
o+=line(92,84,92,282,RED,1.6)+line(86,84,98,84,RED,1.6)+line(86,282,98,282,RED,1.6)
o+=T(84,180,'760 mm',12,anchor='end',weight='800',fill=RED)+T(84,196,'at sea level',10.5,anchor='end',weight='600',fill=RED)
for x in [60,180]: o+=arrow(x,238,x,276,2,BLUE,'arB')
o+=T(232,300,'air pressure pushes',11,anchor='start',weight='700',fill=BLUE)+T(232,314,'on the dish',11,anchor='start',weight='700',fill=BLUE)
o+=rect(262,60,196,170,'#f6fafe')
o+=T(360,82,'Pressure units',13,weight='800')
for i,l in enumerate(['1 atm = 760 mmHg','= 760 torr','= 101,325 Pa','= 101.325 kPa','= 14.7 psi']): o+=T(360,108+i*24,l,13,weight='800' if i==0 else '700')
o+=T(360,256,'Higher air pressure pushes',11.5,weight='700')+T(360,272,'the mercury column higher.',11.5,weight='700')
svg('barometer.svg',470,342,o,'A mercury barometer: a glass tube, closed at the top, stands upside down in a dish of mercury. Above the mercury in the tube is a vacuum. Air pressure pushes down on the mercury in the dish and holds up a column of mercury 760 mm tall at sea level. Pressure units: 1 atm = 760 mmHg = 760 torr = 101,325 Pa = 101.325 kPa = 14.7 psi. Higher air pressure pushes the mercury column higher.')

# 3. Four simple gas laws
o=T(235,22,'The simple gas laws',16,weight='800')
P=[(10,40,"Boyle's law: P and V",'inverse','P'+sub('1')+'V'+sub('1')+' = P'+sub('2')+'V'+sub('2'),'constant n, T'),(240,40,"Charles's law: V and T",'direct','V'+sub('1')+'/T'+sub('1')+' = V'+sub('2')+'/T'+sub('2'),'constant n, P'),(10,236,"Gay-Lussac's law: P and T",'direct','P'+sub('1')+'/T'+sub('1')+' = P'+sub('2')+'/T'+sub('2'),'constant n, V'),(240,236,"Avogadro's law: V and n",'direct','V'+sub('1')+'/n'+sub('1')+' = V'+sub('2')+'/n'+sub('2'),'constant P, T')]
for x,y,t,rel,eq,cst in P:
    o+=rect(x,y,220,186)+T(x+110,y+20,t,12.5,weight='800')+T(x+110,y+152,eq,14,weight='800')+T(x+110,y+172,rel+' relationship; '+cst,10.5,weight='600',fill=GREY2)
# Boyle: two cylinders with pistons
def cyl(x,y,h,n,seed,label):
    s=f'<path d="M{x} {y} v76 h56 v-76" fill="none" stroke="{INK}" stroke-width="2"/>'
    py=y+76-h; s+=f'<rect x="{x+2}" y="{py-8}" width="52" height="8" fill="{GREY2}"/>'+line(x+28,py-8,x+28,y-4,GREY2,4)
    s+=dots(x+2,py,52,h,n,seed,3.5)+T(x+28,y+94,label,10.5,weight='700')
    return s
o+=cyl(36,72,62,8,1,'low P, big V')+cyl(140,72,28,8,1,'high P, small V')+arrow(102,124,132,124,1.8)
# Charles: balloons
o+=f'<ellipse cx="290" cy="112" rx="22" ry="26" fill="#dbe7f6" stroke="{INK}" stroke-width="1.6"/>'+T(290,154,'cold',10.5,weight='700',fill=BLUE)
o+=f'<ellipse cx="392" cy="106" rx="34" ry="40" fill="#f9d9d4" stroke="{INK}" stroke-width="1.6"/>'+T(392,160,'warm: bigger',10.5,weight='700',fill=RED)+arrow(318,112,350,112,1.8)
# Gay-Lussac: rigid can
for (cx,lab,col,n) in [(70,'cool: lower P',BLUE,1),(170,'hot: higher P',RED,2)]:
    o+=f'<rect x="{cx-26}" y="262" width="52" height="84" rx="6" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    o+=dots(cx-26,262,52,84,7,3,3.5,'#9fb6d6' if n==1 else '#f2b8b0',n==2)
    o+=T(cx,358,lab,10.5,weight='700',fill=col)
o+=arrow(102,304,138,304,1.8)
# Avogadro: add gas
o+=f'<ellipse cx="290" cy="306" rx="22" ry="26" fill="#e3f2e1" stroke="{INK}" stroke-width="1.6"/>'+T(290,350,'fewer moles',10.5,weight='700')
o+=f'<ellipse cx="392" cy="300" rx="34" ry="40" fill="#e3f2e1" stroke="{INK}" stroke-width="1.6"/>'+T(392,354,'more moles: bigger',10.5,weight='700')+arrow(318,306,350,306,1.8)
o+=T(235,446,'Temperatures in every gas law must be in kelvins.',12.5,weight='800')
svg('gas_laws.svg',470,458,o,"Four panels showing the simple gas laws. Boyle's law, P and V: pushing a piston down raises the pressure and shrinks the volume; an inverse relationship, P1 V1 = P2 V2, at constant moles and temperature. Charles's law, V and T: a warm balloon is bigger than a cold one; a direct relationship, V1 over T1 = V2 over T2, at constant moles and pressure. Gay-Lussac's law, P and T: heating gas in a rigid can makes the particles move faster and raises the pressure; a direct relationship, P1 over T1 = P2 over T2, at constant moles and volume. Avogadro's law, V and n: adding more moles of gas makes a balloon bigger; a direct relationship, V1 over n1 = V2 over n2, at constant pressure and temperature. Temperatures in every gas law must be in kelvins.")

# 4. Breathing and Boyle's law
o=T(235,22,"Breathing follows Boyle's law",16,weight='800')
def chest(x,inhale):
    s=rect(x,40,212,250,'#f6fafe')
    s+=T(x+106,62,'Inhale' if inhale else 'Exhale',14,weight='800',fill=BLUE if inhale else RED)
    w=58 if inhale else 46; h=86 if inhale else 70
    for dx in [-1,1]:
        s+=f'<ellipse cx="{x+106+dx*34}" cy="{150 if inhale else 142}" rx="{w/2+4}" ry="{h/2+6}" fill="#f9d9d4" stroke="{INK}" stroke-width="1.6"/>'
    s+=line(x+106,74,x+106,110,INK,4)
    dy=208 if inhale else 200
    s+=f'<path d="M{x+30} {dy} Q{x+106} {dy+ (8 if inhale else -14)} {x+182} {dy}" fill="none" stroke="{GRN}" stroke-width="4"/>'
    s+=T(x+106,dy+(26 if inhale else 34),'diaphragm '+('contracts, moves down' if inhale else 'relaxes, moves up'),10.5,weight='700',fill=GRN)
    if inhale: s+=arrow(x+130,96,x+114,108,2,BLUE,'arB')+T(x+150,92,'air in',11,anchor='start',weight='800',fill=BLUE)
    else: s+=arrow(x+114,104,x+132,90,2,RED,'arR')+T(x+138,90,'air out',11,anchor='start',weight='800',fill=RED)
    s+=T(x+106,256,'lung volume '+('increases' if inhale else 'decreases'),11.5,weight='800')
    s+=T(x+106,274,'pressure in lungs '+('drops below' if inhale else 'rises above'),10.5,weight='700')+T(x+106,286,'air pressure',10.5,weight='700')
    return s
o+=chest(14,True)+chest(244,False)
o+=T(235,312,'Air always flows from higher pressure to lower pressure.',12,weight='800')
svg('breathing.svg',470,324,o,"Breathing follows Boyle's law. Left, inhale: the diaphragm contracts and moves down, the lungs expand, lung volume increases, and pressure in the lungs drops below air pressure, so air flows in. Right, exhale: the diaphragm relaxes and moves up, lung volume decreases, and pressure in the lungs rises above air pressure, so air flows out. Air always flows from higher pressure to lower pressure.")

# 5. Which gas law?
o=T(235,22,'Which gas equation should I use?',16,weight='800')
def dbox(x,y,w,h,lines,fill='#fff7e6',size=12.5,bold=False):
    s=rect(x,y,w,h,fill,10,1.6)
    for i,l in enumerate(lines): s+=T(x+w/2,y+h/2-(len(lines)-1)*9+4+i*18,l,size,weight='800' if (bold or i==0) else '700')
    return s
o+=dbox(85,40,300,48,['Does the gas change from one set','of conditions to another (1 → 2)?'])
o+=arrow(160,88,110,120)+T(118,104,'yes',11,anchor='end',weight='800')+arrow(310,88,360,120)+T(352,104,'no',11,anchor='start',weight='800')
o+=dbox(14,122,206,108,['Combined gas law','P'+sub('1')+'V'+sub('1')+'/T'+sub('1')+' = P'+sub('2')+'V'+sub('2')+'/T'+sub('2'),'Cross out what stays','constant (n, P, V, or T).'],'#dbe7f6')
o+=dbox(250,122,206,108,['Ideal gas law','PV = nRT','One set of conditions;','R = 0.082058 L·atm/(mol·K)'],'#e3f2e1')
o+=dbox(250,250,206,62,['At STP (273 K, 1 atm):','1 mol gas = 22.4 L'],'#efe3f7',12)
o+=arrow(353,230,353,248)
o+=dbox(14,250,206,62,['Reaction? Use moles and','mole ratios (Section 10.5).'],'#fbe3d8',12)
o+=T(235,340,'Always: T in K; match P units to R (atm with 0.082058).',12,weight='800')
svg('which_law.svg',470,352,o,'Flowchart: which gas equation should I use? If the gas changes from one set of conditions to another (1 to 2), use the combined gas law, P1 V1 over T1 = P2 V2 over T2, and cross out whatever stays constant (n, P, V, or T). If there is only one set of conditions, use the ideal gas law, PV = nRT, with R = 0.082058 L·atm/(mol·K); at STP (273 K and 1 atm), 1 mol of gas = 22.4 L. For a reaction, use moles and mole ratios (Section 10.5). Always use T in kelvins and match the pressure units to R (atm with 0.082058).')

# 6. Dalton's law
o=T(235,22,"Dalton's law of partial pressures",16,weight='800')
for i,(x,lab,col,n,seed,pl) in enumerate([(14,'O'+sub('2')+' alone','#f2b8b0',3,11,'P = 0.20 atm'),(170,'N'+sub('2')+' alone','#9fb6d6',12,12,'P = 0.80 atm'),(326,'Mixed together','',0,0,'P'+sub('total')+' = 1.00 atm')]):
    o+=f'<rect x="{x}" y="44" width="130" height="130" fill="#fff" stroke="{INK}" stroke-width="2.2"/>'
    if n: o+=dots(x,44,130,130,n,seed,5,col)
    else: o+=dots(x,44,130,130,3,11,5,'#f2b8b0')+dots(x,44,130,130,12,12,5,'#9fb6d6')
    o+=T(x+65,192,lab,12.5,weight='800')+T(x+65,212,pl,12.5,weight='800',fill=RED if i==2 else INK)
o+=T(155,112,'+',24,weight='800')+T(311,112,'=',24,weight='800')
o+=T(235,244,'P'+sub('total')+' = P'+sub('1')+' + P'+sub('2')+' + P'+sub('3')+' + …',14,weight='800')
o+=T(235,268,'Each gas: P'+sub('i')+' = X'+sub('i')+' × P'+sub('total')+'   (X = mole fraction)',13,weight='800')
o+=T(235,290,'Same container and temperature: each gas pushes as if it were alone.',11.5,weight='600')
svg('dalton.svg',470,302,o,"Dalton's law of partial pressures. Three equal containers at the same temperature: O2 alone has a pressure of 0.20 atm; N2 alone has 0.80 atm; the two mixed together in one container have a total pressure of 1.00 atm. P total = P1 + P2 + P3 and so on. For each gas, the partial pressure P i = X i times P total, where X is the mole fraction. In the same container and temperature, each gas pushes as if it were alone.")

# 7. Collecting a gas over water (Exp 8a)
o=T(235,22,'Collecting a gas over water',16,weight='800')
o+=f'<path d="M30 150 v150 a8 8 0 0 0 8 8 h184 a8 8 0 0 0 8 -8 v-150" fill="#dbe7f6" stroke="{INK}" stroke-width="2"/>'
o+=f'<rect x="31" y="170" width="198" height="136" fill="#dbe7f6"/>'+line(30,170,230,170,BLUE,1.6)
o+=f'<rect x="108" y="44" width="44" height="236" rx="4" fill="#fff" stroke="{INK}" stroke-width="2"/>'
o+=f'<rect x="110" y="170" width="40" height="108" fill="#dbe7f6"/>'+line(110,170,150,170,BLUE,1.6)
o+=dots(110,48,40,118,8,21,3.2,'#f2b8b0')+dots(110,48,40,118,3,22,3.2,'#9fb6d6')
for y in [262,248,232]: o+=circ(130+(y%7)-3,y,3.5,'#fff',1.2,BLUE)
o+=f'<rect x="120" y="282" width="20" height="8" fill="{GREY2}"/>'+T(130,322,'Mg + HCl at the bottom',10.5,weight='700')
for i,t in enumerate(['mL'] ): pass
for y in range(60,276,24): o+=line(108,y,116,y,INK,1)
o+=T(158,72,'H'+sub('2')+' + water vapor',11,anchor='start',weight='800')
o+=arrow(70,130,70,166,2,BLUE,'arB')+arrow(196,130,196,166,2,BLUE,'arB')+T(196,122,'P'+sub('atm'),11.5,weight='800',fill=BLUE)
o+=rect(250,50,208,250,'#f6fafe')
o+=T(354,74,'When the water levels match:',12,weight='800')
o+=T(354,104,'P'+sub('atm')+' = P'+sub('H₂')+' + P'+sub('H₂O'),15,weight='800',fill=RED)
o+=T(354,134,'so P'+sub('H₂')+' = P'+sub('atm')+' − P'+sub('H₂O'),13,weight='800')
o+=T(354,166,'Water vapor pressure',12,weight='800')
for i,(t,p) in enumerate([('20 °C','17.5 mmHg'),('25 °C','23.8 mmHg'),('30 °C','31.8 mmHg'),('37 °C','47.1 mmHg')]):
    o+=T(300,190+i*22,t,12,weight='700')+T(400,190+i*22,p,12,weight='700')
o+=T(354,284,'Look it up at the water temperature.',11,weight='600',fill=GREY2)
svg('gas_over_water.svg',470,336,o,'Collecting a gas over water, as in Experiment 8a. A graduated gas collection tube is inverted in a beaker of water, with magnesium reacting with hydrochloric acid at the bottom; bubbles of hydrogen rise and collect at the top of the tube, mixed with water vapor. Air pressure pushes down on the water in the beaker. When the water levels inside and outside the tube match, P atm = P of H2 + P of H2O, so P of H2 = P atm minus P of H2O. Water vapor pressure: 17.5 mmHg at 20 °C, 23.8 mmHg at 25 °C, 31.8 mmHg at 30 °C, and 47.1 mmHg at 37 °C. Look it up at the water temperature.')
print('ok', sorted(os.listdir(OUT)))
