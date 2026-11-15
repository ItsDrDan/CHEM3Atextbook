#!/usr/bin/env python3
"""Chapter 14 figures (SVG), phone-first (~470 px wide). python3 tools/figs_ch14.py"""
import os, math, random
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch14'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
RED="#c0392b"; BLUE="#2f5fa8"; GRN="#2e7d32"; GRAY="#c9d3dc"; GREY2="#55606b"; PUR="#7b4fa0"; ORG="#d35400"
PROT="#e8a0a0"; NEUT="#9fb6d6"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
def mk(i,c): return f'<marker id="{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
DEFS='<defs>'+mk('ar',INK)+mk('arR',RED)+mk('arB',BLUE)+mk('arG',GRN)+mk('arP',PUR)+mk('arO',ORG)+'</defs>'
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.4,c=INK,m='ar',dash=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#{m})"{d}/>'
def sup(s,z=10): return f'<tspan baseline-shift="super" font-size="{z}">{s}</tspan>'
def rect(x,y,w,h,fill='#f6fafe',rx=10,sw=1.6,stroke=INK): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def circ(x,y,r,fill='#fff',sw=1.4,stroke=INK): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,c=INK,w=1.6,dash=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'
def nsym(x,y,A,Z,sym,size=15,fill=INK):
    """Nuclear symbol with A over Z stacked on the left; x = left edge of the element symbol."""
    s=T(x-1,y-size*0.55,A,size*0.62,anchor='end',weight='700',fill=fill)+T(x-1,y+size*0.28,Z,size*0.62,anchor='end',weight='700',fill=fill)
    return s+T(x+1,y,sym,size,anchor='start',weight='800',fill=fill)
def nucleus(cx,cy,n,r=6,seed=1,ratio=0.5):
    random.seed(seed); s=''
    pts=[]
    k=0
    while len(pts)<n and k<4000:
        k+=1; a=random.random()*2*math.pi; d=math.sqrt(random.random())*(r*math.sqrt(n)*0.62)
        x,y=cx+d*math.cos(a),cy+d*math.sin(a)
        if all((x-px)**2+(y-py)**2>(r*1.25)**2 for px,py in pts): pts.append((x,y))
    for i,(x,y) in enumerate(pts): s+=circ(x,y,r,PROT if (i%2==0) else NEUT,1)
    return s
def wave(x1,y,x2,amp=6,per=14,c=PUR,w=2.4):
    pts=[]; x=x1
    while x<=x2: pts.append(f'{x:.1f},{y+amp*math.sin((x-x1)/per*2*math.pi):.1f}'); x+=1.5
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="{w}"/>'

# 1. Penetrating power and shielding
o=T(235,22,'How far each kind of radiation gets',16,weight='800')
o+=rect(10,36,450,250)
xs=[(150,'Paper',"#f3ead2",6),(250,'Aluminum',"#cfd6dc",14),(350,'Lead',"#8d969e",30)]
for x,lab,fill,w in xs:
    o+=f'<rect x="{x}" y="58" width="{w}" height="170" fill="{fill}" stroke="{INK}" stroke-width="1.4"/>'
    o+=T(x+w/2,246,lab,12,weight='800')
o+=T(155,262,'or skin',10.5,weight='600')+T(257,262,'or wood, ~5 mm',10.5,weight='600')+T(365,262,'or thick concrete',10.5,weight='600')
o+=T(150+3,276,'',1)
rows=[(84,'α alpha',RED,'arR',150),(140,'β beta',BLUE,'arB',250),(196,'γ gamma',PUR,'arP',440)]
for y,lab,c,m,stop in rows:
    o+=T(22,y+5,lab,13,anchor='start',weight='800',fill=c)
    if lab.startswith('γ'):
        o+=wave(84,y,350,5,12,c)+wave(380,y,425,2.5,12,c,1.6)+arrow(425,y,446,y,1.6,c,m)
        o+=T(412,y-14,'weakened',10,weight='700',fill=c)
    else:
        o+=arrow(84,y,stop-3,y,3,c,m)
o+=T(235,302,'Alpha: stopped by paper. Beta: stopped by aluminum. Gamma: needs lead or concrete.',10.8,weight='800')
svg('penetration.svg',470,314,o,'Penetrating power of alpha, beta, and gamma radiation. Three barriers stand in a row: a sheet of paper (or skin), a sheet of aluminum (or about 5 mm of wood), and a thick block of lead (or thick concrete). The alpha particle arrow, in red, stops at the paper. The beta particle arrow, in blue, passes the paper and stops at the aluminum. The gamma ray, a purple wave, passes the paper and aluminum and comes out of the lead weakened. Alpha is stopped by paper, beta by aluminum, and gamma needs lead or concrete.')

# 2. Decay types as particle cartoons
o=T(235,22,'Four kinds of radioactive decay',16,weight='800')
panels=[('Alpha (α) decay','loses 2 p + 2 n','A − 4,  Z − 2',RED),('Beta (β) decay','n → p + e⁻ (beta)','A same,  Z + 1',BLUE),('Positron (β⁺) emission','p → n + e⁺ (positron)','A same,  Z − 1',GRN),('Gamma (γ) emission','releases energy only','A same,  Z same',PUR)]
for i,(t,how,chg,c) in enumerate(panels):
    x=10+(i%2)*230; y=36+(i//2)*170
    o+=rect(x,y,220,160)+T(x+110,y+22,t,13,weight='800',fill=c)
    cx,cy=x+62,y+86
    o+=nucleus(cx,cy,22,6,seed=i+2)
    if i==0:
        o+=arrow(cx+34,cy,cx+76,cy,2.4,c,'arR')
        o+=circ(cx+88,cy-6,6,PROT,1)+circ(cx+100,cy-6,6,NEUT,1)+circ(cx+88,cy+6,6,NEUT,1)+circ(cx+100,cy+6,6,PROT,1)
        o+=nsym(cx+122,cy+6,'4','2','He',14,c)
    elif i in (1,2):
        o+=arrow(cx+34,cy,cx+86,cy,2.4,c,'arB' if i==1 else 'arG')
        o+=circ(cx+100,cy,7,'#fff',1.6,c)+T(cx+100,cy+4,'−' if i==1 else '+',11,weight='800',fill=c)
        o+=nsym(cx+126,cy+6,'0','−1' if i==1 else '+1','e',14,c)
    else:
        o+=wave(cx+34,cy,cx+92,6,13,c)+arrow(cx+92,cy,cx+106,cy,2,c,'arP')
        o+=nsym(cx+126,cy+6,'0','0','γ',14,c)
    o+=T(x+110,y+132,how,11.5,weight='700')+T(x+110,y+150,chg,12,weight='800',fill=c)
o+=T(235,384,'Pink = protons, blue = neutrons. A = mass number, Z = atomic number.',11,weight='700')
svg('decay_types.svg',470,396,o,'Four kinds of radioactive decay, each shown as a nucleus of protons and neutrons giving off radiation. Alpha decay: the nucleus throws out a helium-4 nucleus of 2 protons and 2 neutrons, written with mass number 4 and atomic number 2; the new nucleus has A minus 4 and Z minus 2. Beta decay: a neutron changes into a proton and an electron, which leaves as a beta particle with mass number 0 and charge minus 1; A stays the same and Z goes up by 1. Positron emission: a proton changes into a neutron and a positron, mass number 0 and charge plus 1; A stays the same and Z goes down by 1. Gamma emission: the nucleus releases energy only as a gamma ray, mass number 0 and charge 0; A and Z stay the same.')

# 3. Half-life curve
o=T(235,22,'Half-life: half is left after each half-life',16,weight='800')
x0,y0,w,h=66,266,350,214
o+=line(x0,y0,x0+w,y0,INK,1.8)+line(x0,y0,x0,y0-h,INK,1.8)
for k in range(0,6):
    X=x0+w*k/5; o+=line(X,y0,X,y0+4,INK,1.2)+T(X,y0+17,str(k),11,weight='700')+T(X,y0+33,f'{6*k} h',10.5,weight='600',fill=GREY2)
for v in (0,25,50,75,100):
    Y=y0-h*v/100; o+=line(x0-4,Y,x0,Y,INK,1.2)+T(x0-7,Y+4,str(v),10.5,anchor='end',weight='600')+line(x0,Y,x0+w,Y,GRAY,0.8)
pts=' '.join(f'{x0+w*t/5:.1f},{y0-h*100*0.5**t/100:.1f}' for t in [i/20 for i in range(0,101)])
o+=f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="3"/>'
labs=['100%','50%','25%','12.5%','6.25%','3.13%']
for k in range(6):
    X=x0+w*k/5; Y=y0-h*100*0.5**k/100
    o+=line(X,Y,X,y0,BLUE,1,'4 3')+circ(X,Y,4.5,'#fff',2,BLUE)
    o+=T(X+(8 if k<5 else -6),Y-(9 if k<5 else 14),labs[k],11,anchor='start' if k<5 else 'middle',weight='800',fill=BLUE)
o+=T(x0+w/2,y0+50,'Number of half-lives (n), and time for Tc-99m (6 h each)',11,weight='800')
o+=T(24,y0-h/2,'Percent remaining',11.5,weight='800',extra=f'transform="rotate(-90 24 {y0-h/2})"')
o+=T(300,70,'amount left = initial × (½)ⁿ',12.5,weight='800')
svg('halflife_curve.svg',470,330,o,'A decay curve. The percent of a radioisotope remaining is plotted against the number of half-lives, from 0 to 5. The curve starts at 100 percent and falls to 50 percent after 1 half-life, 25 percent after 2, 12.5 percent after 3, 6.25 percent after 4, and 3.13 percent after 5. A second scale shows the times for technetium-99m, whose half-life is 6 hours: 0, 6, 12, 18, 24, and 30 hours. Amount left equals the initial amount times one-half to the power n.')

# 4. Carbon-14 cycle
o=T(235,22,'Carbon-14: made in the air, kept while alive',16,weight='800')
o+=rect(10,36,450,92,'#eef4fb')
o+=T(24,56,'Upper atmosphere',12,anchor='start',weight='800',fill=BLUE)
o+=T(24,76,'cosmic-ray neutron',10.5,anchor='start',weight='600')
o+=nsym(58,104,'1','0','n',15)+T(84,104,'+',15,anchor='start')+nsym(116,104,'14','7','N',15)+T(146,104,'→',15,anchor='start')
o+=nsym(184,104,'14','6','C',15,RED)+T(212,104,'+',15,anchor='start')+nsym(240,104,'1','1','H',15)
o+=T(400,72,'C-14 joins O₂',11,weight='700')+T(400,90,'to make ¹⁴CO₂',11,weight='700')
o+=arrow(400,100,400,150,2.2)
o+=rect(10,150,450,110,'#f1f8ef')
o+=T(24,172,'While alive: constant C-14/C-12 ratio',12,anchor='start',weight='800',fill=GRN)
# plant
o+=f'<path d="M80 245 v-40" stroke="{GRN}" stroke-width="4"/>'+f'<ellipse cx="68" cy="205" rx="14" ry="8" fill="#9ccc8f" stroke="{GRN}"/>'+f'<ellipse cx="92" cy="198" rx="14" ry="8" fill="#9ccc8f" stroke="{GRN}"/>'
o+=T(80,254,'plants take in CO₂',10.5,weight='700')
o+=arrow(140,215,200,215,2.2)
o+=T(170,206,'eaten',10.5,weight='700')
# animal (simple)
o+=f'<ellipse cx="250" cy="220" rx="30" ry="16" fill="#f3e1c7" stroke="{INK}" stroke-width="1.4"/>'+circ(284,206,10,'#f3e1c7',1.4)
for lx in (232,244,258,270): o+=line(lx,234,lx,242,INK,2)
o+=T(254,254,'animals eat plants',10.5,weight='700')
o+=arrow(320,215,372,215,2.2)
o+=T(410,196,'at death:',11,weight='800')+T(410,212,'no new C-14',11,weight='700')
o+=T(410,228,'C-14 decays,',11,weight='700')+T(410,244,'ratio falls',11,weight='700')
o+=rect(10,276,450,52,'#fdf3ec')
o+=nsym(40,306,'14','6','C',15,RED)+T(68,306,'→',15,anchor='start')+nsym(102,306,'14','7','N',15)+T(130,306,'+',15,anchor='start')+nsym(160,306,'0','−1','e',15)
o+=T(330,300,'half-life 5730 years',12,weight='800',fill=ORG)+T(330,318,'useful to about 50,000 years',11,weight='700')
svg('c14_cycle.svg',470,340,o,'How carbon-14 is made and used for dating. In the upper atmosphere, a neutron from cosmic rays hits a nitrogen-14 nucleus and makes carbon-14 and a proton. The carbon-14 joins oxygen to make carbon dioxide. Plants take in this carbon dioxide, and animals eat the plants, so every living thing keeps a constant ratio of carbon-14 to carbon-12. At death no new carbon-14 comes in; the carbon-14 already there decays to nitrogen-14 by beta decay, and the ratio falls. The half-life is 5730 years, and the method is useful to about 50,000 years.')

# 5. Fission chain reaction
o=T(235,22,'A fission chain reaction',16,weight='800')
def U(x,y,r=15,fs=8.5,lab='U-235'): return circ(x,y,r,'#f5d9a8',1.6)+T(x,y+3.5,lab,fs,weight='800')
def nn(x,y): return circ(x,y,4.5,NEUT,1.2)
o+=T(28,166,'n',11,weight='800')+nn(30,180)+arrow(36,180,80,180,1.8,INK)
o+=U(100,180)
for fy,ly in ((128,116),(232,252)):
    o+=arrow(100,180+(-16 if fy<180 else 16),100,fy+(8 if fy<180 else -8),1.4,PUR,'arP')+circ(100,fy,8,'#e3c7e8',1.2)
    o+=T(100,ly,'fragment',9.5,weight='700',fill=PUR)
c2=[(230,90),(230,180),(230,270)]
for x,y in c2: o+=arrow(116,180,x-18,y,1.6,INK)+U(x,y)
k=0
for x,y in c2:
    for dy in (-30,0,30):
        ty=y+dy; o+=arrow(x+15,y,352,ty,1.3,INK)+U(364,ty,10,8,'U')
        o+=arrow(375,ty,410,ty+(-6 if k%2 else 6),1,GREY2,'ar','3 2'); k+=1
o+=T(100,330,'1 neutron',11,weight='800',fill=RED)+T(230,330,'3 neutrons',11,weight='800',fill=RED)+T(364,330,'9 neutrons …',11,weight='800',fill=RED)
o+=T(235,356,'Each split releases energy and 2–3 neutrons.',11.5,weight='800')
o+=T(235,374,'Critical mass: enough U-235 for the chain to keep going.',11.5,weight='700')
svg('fission_chain.svg',470,388,o,'A fission chain reaction. One neutron hits a uranium-235 nucleus, which splits into two smaller fragment nuclei and releases energy and three neutrons. Each of those three neutrons hits another uranium-235 nucleus, which splits and releases three more neutrons, so the next step has nine neutrons, and the number keeps growing. Each split releases energy and 2 to 3 neutrons. A critical mass is enough uranium-235 for the chain to keep going.')

# 6. Time, distance, shielding
o=T(235,22,'Three ways to lower your dose',16,weight='800')
for i,(t,a,b) in enumerate([('Time','less time near','the source'),('Distance','2× the distance','= ¼ the dose'),('Shielding','lead apron, lead','glass, concrete')]):
    x=10+i*153
    o+=rect(x,36,144,196)+T(x+72,58,t,14,weight='800',fill=[BLUE,GRN,PUR][i])
    if i==0:
        o+=circ(x+72,120,34,'#fff',2)+line(x+72,120,x+72,96,INK,2.4)+line(x+72,120,x+92,128,INK,2.4)
        o+=f'<path d="M{x+72} 86 A34 34 0 0 1 {x+106} 120 L{x+72} 120 Z" fill="#cfe0f5" opacity="0.8"/>'
    elif i==1:
        o+=circ(x+20,120,8,'#f6d36b',1.4)+T(x+20,124,'☢',9,weight='800')
        o+=line(x+30,120,x+130,120,GRAY,1,'3 3')
        o+=T(x+60,108,'1 m',10.5,weight='700')+T(x+118,108,'2 m',10.5,weight='700')
        o+=line(x+60,112,x+60,128,INK,1.6)+line(x+118,112,x+118,128,INK,1.6)
        o+=T(x+60,146,'dose D',10.5,weight='700')+T(x+118,146,'D ÷ 4',10.5,weight='700')
    else:
        o+=circ(x+24,120,8,'#f6d36b',1.4)+T(x+24,124,'☢',9,weight='800')
        o+=wave(x+34,120,x+80,4,10,PUR,2)+f'<rect x="{x+82}" y="88" width="16" height="64" fill="#8d969e" stroke="{INK}"/>'
        o+=wave(x+100,120,x+130,1.5,10,PUR,1.4)
    o+=T(x+72,186,a,11,weight='700')+T(x+72,202,b,11,weight='700')
o+=T(235,252,'ALARA: keep doses as low as reasonably achievable.',12,weight='800')
svg('time_distance_shielding.svg',470,266,o,'Three ways to lower a radiation dose. Time: a clock face; spend less time near the source. Distance: a radioactive source with marks at 1 meter and 2 meters; doubling the distance gives one-fourth the dose. Shielding: a gamma ray passes into a lead barrier and comes out much weaker; examples are a lead apron, lead glass, and concrete. ALARA means keeping doses as low as reasonably achievable.')

# 7. Nuclear power plant (pressurized water reactor, simplified)
o=T(235,22,'A nuclear power plant (simplified)',16,weight='800')
o+=f'<rect x="20" y="60" width="130" height="190" rx="4" fill="#eef1f4" stroke="{INK}" stroke-width="2"/>'+T(85,52,'containment',10.5,weight='700')
o+=rect(32,96,96,124,'#dbe7f6',6)
for k in range(5): o+=f'<rect x="{42+k*17}" y="130" width="8" height="82" fill="#f5d9a8" stroke="{INK}" stroke-width="1"/>'
for k in range(4): o+=f'<rect x="{51+k*17}" y="104" width="6" height="58" fill="{GREY2}"/>'
o+=T(80,238,'reactor core',10.5,weight='800')
o+=rect(190,80,60,120,'#f6fafe',6)+T(220,236,'steam',10.5,weight='800')+T(220,249,'generator',10.5,weight='800')
o+=f'<path d="M128 120 H186" stroke="{RED}" stroke-width="3.5" fill="none" marker-end="url(#arR)"/>'+f'<path d="M190 180 H132" stroke="{BLUE}" stroke-width="3.5" fill="none" marker-end="url(#arB)"/>'
o+=T(166,111,'hot',10,weight='800',fill=RED)+T(166,198,'cooler',10,weight='800',fill=BLUE)
o+=f'<path d="M250 110 H292" stroke="{GREY2}" stroke-width="3.5" fill="none" marker-end="url(#ar)"/>'+T(270,100,'steam',10,weight='700')
o+=f'<polygon points="296,86 336,98 336,122 296,134" fill="#e7ecf0" stroke="{INK}" stroke-width="1.6"/>'+T(316,76,'turbine',10.5,weight='800')
o+=line(336,110,358,110,INK,3)+circ(380,110,22,'#fff3d6',1.8)+T(380,114,'G',13,weight='800')+T(380,76,'generator',10.5,weight='800')
o+=f'<path d="M402 110 H452" stroke="{ORG}" stroke-width="2.4" fill="none" marker-end="url(#arO)"/>'+T(428,130,'electricity',10,weight='800',fill=ORG)
o+=rect(270,170,170,44,'#e3f0fb',6)+T(355,197,'condenser',10.5,weight='800')
o+=f'<path d="M316 134 V166" stroke="{GREY2}" stroke-width="2.4" fill="none" marker-end="url(#ar)"/>'
o+=f'<path d="M270 206 H236 V206 V204" stroke="{BLUE}" stroke-width="2.4" fill="none"/>'+arrow(236,207,236,203,2.4,BLUE,'arB')
o+=f'<path d="M330 248 V218" stroke="{BLUE}" stroke-width="2.2" fill="none" marker-end="url(#arB)"/>'+f'<path d="M380 216 V246" stroke="{BLUE}" stroke-width="2.2" fill="none" marker-end="url(#arB)"/>'
o+=T(355,266,'cooling water',10.5,weight='800',fill=BLUE)+T(355,280,'(ocean or cooling tower)',10,weight='600')
o+=T(20,276,'fuel rods: U-235 pellets',10.5,anchor='start',weight='700')
o+=T(20,292,'control rods: absorb neutrons',10.5,anchor='start',weight='700')
o+=T(20,308,'water: coolant + moderator',10.5,anchor='start',weight='700')
svg('power_plant.svg',470,320,o,'A simplified nuclear power plant. Inside a containment building, the reactor core holds fuel rods of uranium-235 pellets and movable control rods that absorb neutrons; water flows through the core as both coolant and moderator. Hot water from the core flows to a steam generator and returns cooler. Steam from the steam generator turns a turbine, which spins a generator that makes electricity. The used steam is cooled back to water in a condenser by cooling water from the ocean or a cooling tower, and the water is pumped back to the steam generator.')
print('ok', sorted(os.listdir(OUT)))
