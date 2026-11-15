#!/usr/bin/env python3
"""Chapter 9 figures (SVG), phone-first (~470 px wide). python3 tools/figs_ch09.py"""
import os, math, random
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch09'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
RED="#c0392b"; BLUE="#2f5fa8"; GRN="#2e7d32"; GRAY="#c9d3dc"
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
def circ(x,y,r,fill='#fff',sw=1.4): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,c=INK,w=1.6,dash=''): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" {"stroke-dasharray=%s" % chr(34)+dash+chr(34) if dash else ""}/>'

# 1. Kinetic and potential energy of particles
o=T(235,22,'Two kinds of energy in matter',16,weight='800')
o+=rect(10,38,218,214)+rect(242,38,218,214)
o+=T(119,60,'Kinetic energy, KE (motion)',13,weight='800')+T(351,60,'Potential energy, PE (position)',13,weight='800')
# kinetic: cool vs hot particles
o+=T(64,84,'Cooler',12,weight='700',fill=BLUE)+T(174,84,'Hotter',12,weight='700',fill=RED)
o+=line(119,76,119,200,GRAY,1.4)
random.seed(4)
for (x,y) in [(40,110),(80,104),(54,146),(92,150),(44,184),(86,188)]:
    o+=circ(x,y,9,'#dbe7f6')+arrow(x+10,y,x+20,y-3,1.6,BLUE,'arB')
for (x,y,ang) in [(140,104,20),(196,112,-150),(150,150,-40),(206,152,100),(142,190,10),(196,188,-120)]:
    a=math.radians(ang); o+=circ(x,y,9,'#f9d9d4')+arrow(x+9*math.cos(a),y+9*math.sin(a),x+28*math.cos(a),y+28*math.sin(a),1.8,RED,'arR')
o+=T(119,222,'Faster particles = higher temperature',12,weight='700')
o+=T(119,240,'Temperature measures average KE',11,weight='600')
# potential: attracted particles
o+=T(351,84,'Attracted particles',12,weight='700')
o+=circ(300,118,13,'#e3f2e1')+circ(326,118,13,'#e3f2e1')+T(313,148,'Close together:',11,weight='700')+T(313,162,'LOW PE',12,weight='800')
o+=circ(372,118,13,'#e3f2e1')+circ(432,118,13,'#e3f2e1')+line(386,118,418,118,INK,1.4,'4 3')
o+=T(402,148,'Pulled apart:',11,weight='700')+T(402,162,'HIGH PE',12,weight='800')
o+=T(351,190,'Separating particles takes energy,',12,weight='700')+T(351,206,'like stretching a spring.',12,weight='700')
o+=T(351,232,'Chemical energy is stored this way',11,weight='600')+T(351,246,'in bonds and between molecules.',11,weight='600')
svg('ke_pe.svg',470,262,o,'Two kinds of energy in matter. Left panel, kinetic energy (energy of motion): cooler particles move slowly, shown with short arrows; hotter particles move faster in random directions, shown with long arrows. Faster particles mean a higher temperature; temperature measures the average kinetic energy. Right panel, potential energy (energy of position): two attracted particles close together have low potential energy; the same particles pulled apart have high potential energy. Separating particles takes energy, like stretching a spring. Chemical energy is stored this way, in bonds and between molecules.')

# 2. Temperature scales
o=T(235,22,'Three temperature scales',16,weight='800')
cols=[(140,'°F'),(255,'°C'),(370,'K')]
top,bot=60,330
rows=[('Water boils',212,'212 °F','100 °C','373.15 K'),('Body temperature',98.6,'98.6 °F','37.0 °C','310.15 K'),('Water freezes',32,'32 °F','0 °C','273.15 K'),('Absolute zero',-459.67,'−459.67 °F','−273.15 °C','0 K')]
def ypos(f):  # piecewise so labels do not crowd
    return {212:72,98.6:150,32:198,-459.67:318}[f]
for x,lab in cols:
    o+=T(x,48,lab,13,weight='800')
    o+=f'<rect x="{x-9}" y="{top}" width="18" height="{bot-top}" rx="9" fill="#fff" stroke="{INK}" stroke-width="1.8"/>'
    o+=circ(x,bot+6,14,'#f2b8b0',1.8)+f'<rect x="{x-4}" y="{ypos(98.6)}" width="8" height="{bot-ypos(98.6)}" fill="#f2b8b0"/>'
for name,f,a,b,c in rows:
    y=ypos(f)
    o+=line(20,y,452,y,GRAY,1.2,'5 4')
    for (x,_),v in zip(cols,(a,b,c)):
        o+=line(x-12,y,x+12,y,INK,2.2)+T(x+16,y-5,v,12,anchor='start',weight='800')
    o+=T(10,y+15,name,11,anchor='start',weight='700',fill='#55606b')
o+=T(130,362,'K = °C + 273.15',13,weight='800')+T(340,362,'°C = (°F − 32) ÷ 1.8',13,weight='800')
o+=T(235,380,'A kelvin and a Celsius degree are the same size; a Celsius degree is 1.8 °F.',11,weight='600')
svg('temp_scales.svg',470,392,o,'Three thermometers side by side for the Fahrenheit, Celsius, and Kelvin scales, with dashed lines across them at four temperatures. Water boils: 212 °F, 100 °C, 373.15 K. Body temperature: 98.6 °F, 37.0 °C, 310.15 K. Water freezes: 32 °F, 0 °C, 273.15 K. Absolute zero: −459.67 °F, −273.15 °C, 0 K. Formulas: K = °C + 273.15, and °C = (°F − 32) divided by 1.8. A kelvin and a Celsius degree are the same size; a Celsius degree is 1.8 Fahrenheit degrees. The thermometers are not drawn to scale.')

# 3. Heat flow: system and surroundings
o=T(235,22,'Heat flows from hot to cold',16,weight='800')
for i,(x,title,sign,col,mk,desc1,desc2,ex) in enumerate([(14,'Exothermic','q &lt; 0',RED,'arR','System releases heat;','surroundings warm up.','Hand warmer, burning fuel, freezing water'),(244,'Endothermic','q &gt; 0',BLUE,'arB','System absorbs heat;','surroundings cool down.','Cold pack, melting ice, evaporating sweat')]):
    o+=rect(x,38,212,232)
    o+=T(x+106,60,title,15,weight='800',fill=col)
    o+=rect(x+56,86,100,66,'#fff7e6' if i==0 else '#e8f1fb',12,1.8)+T(x+106,116,'system',13,weight='800')+T(x+106,134,'(the change)',11,weight='600')
    for (dx,dy) in [(-1,0),(1,0),(0,-1),(0,1)]:
        cx,cy=x+106,119
        if i==0: o+=arrow(cx+dx*56,cy+dy*37,cx+dx*84,cy+dy*50,2.2,col,mk)
        else: o+=arrow(cx+dx*86,cy+dy*52,cx+dx*58,cy+dy*38,2.2,col,mk)
    o+=T(x+106,198,sign,15,weight='800',fill=col)+T(x+106,216,desc1,12,weight='700')+T(x+106,232,desc2,12,weight='700')
    o+=T(x+106,256,ex,10.5,weight='600',fill='#55606b')
o+=T(235,292,'Everything outside the system is the surroundings (your hand, the water, the air).',11.5,weight='700')
svg('heat_flow.svg',470,302,o,'Heat flows from hot to cold. Left, exothermic: arrows point outward from the system (the change) to the surroundings; q is less than 0; the system releases heat and the surroundings warm up. Examples: a hand warmer, burning fuel, freezing water. Right, endothermic: arrows point inward from the surroundings to the system; q is greater than 0; the system absorbs heat and the surroundings cool down. Examples: a cold pack, melting ice, evaporating sweat. Everything outside the system is the surroundings, such as your hand, the water, or the air.')

# 4. Specific heat bar chart
data=[('Water (liquid)',4.184),('Ethanol',2.42),('Aluminum',0.903),('Iron',0.449),('Copper',0.385),('Gold',0.128)]
o=T(235,22,'Specific heat capacity, c (J/g·°C)',16,weight='800')
x0,x1=128,430; ymax=4.5
for v in [0,1,2,3,4]:
    X=x0+(x1-x0)*v/ymax; o+=line(X,40,X,40+len(data)*40,GRAY,1)+T(X,58+len(data)*40,str(v),11,weight='600')
for i,(n,v) in enumerate(data):
    y=46+i*40; w=(x1-x0)*v/ymax
    o+=T(x0-8,y+20,n,12.5,anchor='end',weight='800')
    o+=f'<rect x="{x0}" y="{y+4}" width="{w:.1f}" height="24" fill="{BLUE if i==0 else "#9fb6d6"}" stroke="{INK}" stroke-width="1.2"/>'
    o+=T(x0+w+6,y+21,f'{v}',12,anchor='start',weight='800')
o+=T(235,316,'Higher c: more heat needed for each 1 °C change.',12.5,weight='800')
o+=T(235,334,'Water is hard to heat and slow to cool; metals heat quickly.',12,weight='600')
svg('specific_heat.svg',470,346,o,'Bar chart of specific heat capacity in joules per gram per degree Celsius: liquid water 4.184, ethanol 2.42, aluminum 0.903, iron 0.449, copper 0.385, gold 0.128. Water has by far the highest value. A higher specific heat means more heat is needed for each 1 °C change, so water is hard to heat and slow to cool, while metals heat quickly.')

# 5. Heating curve of water
o=T(235,22,'Heating curve for water',16,weight='800')
X0,Y0,W,H=62,300,388,250   # axes origin bottom-left
def P(q,t): return X0+q*W, Y0-(t+30)/160*H  # t from -30 to 130
o+=line(X0,Y0,X0+W,Y0,INK,2)+line(X0,Y0,X0,Y0-H,INK,2)
for t in [-20,0,20,40,60,80,100,120]:
    _,y=P(0,t); o+=line(X0-5,y,X0,y,INK,1.4)+T(X0-9,y+4,str(t).replace('-','−'),11,anchor='end',weight='600')
o+=T(20,Y0-H/2,'Temperature (°C)',12,weight='800',extra=f'transform="rotate(-90 20 {Y0-H/2})"')
o+=T(X0+W/2,Y0+26,'Heat added (q) →',12,weight='800')
pts=[(0,-20),(0.06,0),(0.20,0),(0.33,100),(0.90,100),(0.97,120)]
o+=f'<polyline points="{" ".join("%.1f,%.1f"%P(q,t) for q,t in pts)}" fill="none" stroke="{RED}" stroke-width="3.2" stroke-linejoin="round"/>'
for t in [0,100]:
    x,y=P(0,t); x2,_=P(1,t); o+=line(x,y,x2,y,GRAY,1,'4 4')
labs=[(0.03,-10,'1','ice warms','q = mcΔT',-1),(0.13,0,'2','ice melts','q = n·ΔH'+sub('fus',9),1),(0.265,50,'3','water warms','q = mcΔT',-1),(0.615,100,'4','water boils','q = n·ΔH'+sub('vap',9),1),(0.935,110,'5','steam','warms',-1)]
for q,t,num,a,b,side in labs:
    x,y=P(q,t)
    o+=circ(x,y,10,'#fff',1.6)+T(x,y+4,num,11,weight='800')
leg=['1 Ice warms: q = mcΔT','2 Ice melts at 0 °C: q = n·ΔH'+sub('fus',9),'3 Liquid water warms: q = mcΔT','4 Water boils at 100 °C: q = n·ΔH'+sub('vap',9),'5 Steam warms: q = mcΔT']
for i,l in enumerate(leg): o+=T(70,Y0+52+i*18,l,12,anchor='start',weight='700')
o+=T(235,Y0+150,'Slopes: temperature changes. Plateaus: phase changes at constant temperature.',11.5,weight='800')
svg('heating_curve.svg',470,462,o,'Heating curve for water: temperature in degrees Celsius on the vertical axis from −20 to 120, heat added on the horizontal axis. Segment 1, a rising slope from −20 to 0 °C: ice warms, q = m c delta T. Segment 2, a flat plateau at 0 °C: ice melts, q = n times delta H of fusion. Segment 3, a rising slope from 0 to 100 °C: liquid water warms, q = m c delta T. Segment 4, a long flat plateau at 100 °C: water boils, q = n times delta H of vaporization; it is the longest segment because vaporizing takes the most heat. Segment 5, a rising slope above 100 °C: steam warms. Slopes show temperature changes; plateaus show phase changes at constant temperature.')

# 6. Four intermolecular forces
def mol_HCl(x,y,flip=False):
    a,b=(x,x+30) if not flip else (x+30,x)
    return circ(a,y,10,'#fff')+T(a,y+4,'H',10,weight='800')+circ(b,y,14,'#cfe8cf')+T(b,y+4,'Cl',10,weight='800')
o=T(235,22,'The intermolecular forces',16,weight='800')
panels=[(10,40,'Dispersion (all molecules)'),(240,40,'Dipole–dipole (polar molecules)'),(10,206,'Hydrogen bonding (H on N, O, F)'),(240,206,'Ion–dipole (ions in water)')]
for x,y,t in panels: o+=rect(x,y,220,156)+T(x+110,y+20,t,12.5,weight='800')
# dispersion: two atoms with uneven clouds
for cx,lab in [(70,'δ−    δ+'),(170,'δ−    δ+')]:
    o+=f'<ellipse cx="{cx}" cy="110" rx="34" ry="24" fill="#e6e1f5" stroke="{INK}" stroke-width="1.3"/>'
    o+=f'<ellipse cx="{cx-14}" cy="110" rx="16" ry="18" fill="#b9addf" opacity="0.9"/>'+circ(cx,110,5,INK,1)
    o+=T(cx,148,lab,12,weight='800')
o+=T(120,172,'A brief uneven electron cloud',11,weight='600')+T(120,186,'induces one in a neighbor.',11,weight='600')
# dipole-dipole
o+=mol_HCl(268,100)+mol_HCl(338,100)+line(312,100,326,100,INK,1.6,'3 3')
o+=T(268,84,'δ+',11,weight='800')+T(298,84,'δ−',11,weight='800')+T(338,84,'δ+',11,weight='800')+T(368,84,'δ−',11,weight='800')
o+=mol_HCl(300,140)+T(410,104,'HCl',12,weight='800')
o+=T(350,172,'The δ+ end of one attracts',11,weight='600')+T(350,186,'the δ− end of another.',11,weight='600')
# hydrogen bonding: water - water
def water(x,y,rot=0):
    s=f'<g transform="rotate({rot} {x} {y})">'+line(x,y,x-20,y+16,INK,2)+line(x,y,x+20,y+16,INK,2)+circ(x,y,12,'#f6d5d1')+T(x,y+4,'O',11,weight='800')+circ(x-20,y+16,8,'#fff')+T(x-20,y+20,'H',9,weight='800')+circ(x+20,y+16,8,'#fff')+T(x+20,y+20,'H',9,weight='800')+'</g>'
    return s
o+=water(70,262)+water(170,276,-60)
o+=line(94,280,154,278,BLUE,2.4,'4 3')
o+=T(124,266,'H bond',11,weight='800',fill=BLUE)
o+=T(120,338,'Strong dipole–dipole: H on N, O, or F',11,weight='600')+T(120,352,'attracted to a lone pair on N, O, or F.',11,weight='600')
# ion-dipole
o+=circ(350,284,16,'#fde9c8',1.8)+T(350,289,'Na'+sup('+',9),12,weight='800')
for ang in [0,90,180,270]:
    a=math.radians(ang); wx,wy=350+46*math.cos(a),284+30*math.sin(a)
    o+=circ(wx,wy,10,'#f6d5d1')+T(wx,wy+4,'O',10,weight='800')
    o+=circ(wx+12*math.cos(a)+8*math.sin(a),wy+12*math.sin(a)-8*math.cos(a),6,'#fff',1.1)+circ(wx+12*math.cos(a)-8*math.sin(a),wy+12*math.sin(a)+8*math.cos(a),6,'#fff',1.1)
o+=T(350,350,'The δ− O ends of water face the cation.',11,weight='600')
o+=T(235,380,'For molecules of similar size, weakest → strongest:',12,weight='700')+T(235,398,'dispersion &lt; dipole–dipole &lt; H bond &lt; ion–dipole',12.5,weight='800')
svg('imf_types.svg',470,410,o,'Four panels showing the intermolecular forces. Dispersion, found in all molecules: two atoms whose electron clouds are briefly uneven, delta minus on one side and delta plus on the other; a brief uneven cloud induces one in a neighbor. Dipole–dipole, found in polar molecules: HCl molecules line up so the delta plus H end of one attracts the delta minus Cl end of another. Hydrogen bonding: two water molecules, with a dashed hydrogen bond from an H on one water to the O of another; it is a strong dipole–dipole attraction between H bonded to N, O, or F and a lone pair. Ion–dipole, found with ions in water: a sodium ion surrounded by four water molecules with their partially negative oxygen ends facing the cation. For molecules of similar size, from weakest to strongest: dispersion, dipole–dipole, hydrogen bond, ion–dipole.')

# 7. IMF flowchart
o=T(235,22,'Which intermolecular forces are present?',16,weight='800')
def dbox(x,y,w,h,lines,fill='#fff7e6',size=12.5):
    s=rect(x,y,w,h,fill,10,1.6)
    for i,l in enumerate(lines): s+=T(x+w/2,y+h/2-(len(lines)-1)*8+4+i*16,l,size,weight='800' if fill!='#fff7e6' else '700')
    return s
o+=dbox(105,40,260,46,['Is it an ion (or ionic compound)','mixed with a polar molecule?'])
o+=arrow(235,86,235,104)+T(245,100,'no',11,anchor='start',weight='800')
o+=arrow(365,63,392,63)+T(378,54,'yes',11,weight='800')+dbox(394,40,66,46,['Ion–','dipole'],'#fbe3d8',12)
o+=dbox(105,106,260,46,['Does the molecule have H bonded','directly to N, O, or F?'])
o+=arrow(365,129,392,129)+T(378,120,'yes',11,weight='800')+dbox(394,106,66,46,['H bond','+ more'],'#dbe7f6',12)
o+=arrow(235,152,235,170)+T(245,166,'no',11,anchor='start',weight='800')
o+=dbox(105,172,260,46,['Is the molecule polar?','(polar bonds, asymmetric shape)'])
o+=arrow(365,195,392,195)+T(378,186,'yes',11,weight='800')+dbox(394,172,66,46,['Dipole–','dipole +'],'#e3f2e1',12)
o+=arrow(235,218,235,236)+T(245,232,'no',11,anchor='start',weight='800')
o+=dbox(105,238,260,40,['Dispersion forces only'],'#efe3f7',13)
o+=T(235,302,'Every molecule also has dispersion forces. A molecule with H bonding',11,weight='700')
o+=T(235,318,'also has dipole–dipole and dispersion forces.',11,weight='700')
svg('imf_flowchart.svg',470,330,o,'Flowchart for deciding which intermolecular forces are present. Question 1: is it an ion or ionic compound mixed with a polar molecule? If yes, ion–dipole. If no, question 2: does the molecule have H bonded directly to N, O, or F? If yes, hydrogen bonding plus the weaker forces. If no, question 3: is the molecule polar, meaning polar bonds and an asymmetric shape? If yes, dipole–dipole plus dispersion. If no, dispersion forces only. Every molecule also has dispersion forces, and a molecule with hydrogen bonding also has dipole–dipole and dispersion forces.')

# 8. Types of crystalline solids
o=T(235,22,'Types of crystalline solids',16,weight='800')
P4=[(10,40,'Ionic','NaCl','ions held by ionic bonds','high mp; conducts if melted or dissolved'),(240,40,'Molecular','ice, dry ice, sugar','molecules held by IMFs','low mp; does not conduct'),(10,232,'Covalent network','diamond, quartz (SiO'+sub('2',9)+')','atoms in a web of covalent bonds','very high mp; very hard'),(240,232,'Metallic','Fe, Cu, Al','cations in a sea of electrons','wide range of mp; conducts')]
for x,y,t,ex,held,prop in P4: o+=rect(x,y,220,180)+T(x+110,y+20,t,14,weight='800')+T(x+110,y+38,ex,11,weight='600',fill='#55606b')+T(x+110,y+156,held,11,weight='700')+T(x+110,y+172,prop,10.5,weight='600')
# ionic lattice
for i in range(4):
    for j in range(3):
        cx,cy=58+i*40,104+j*24; na=(i+j)%2==0
        o+=circ(cx,cy,8 if na else 11,'#fde9c8' if na else '#cfe8cf',1.2)+T(cx,cy+3.5,'+' if na else '−',10,weight='800')
# molecular: water molecules spaced
for (cx,cy) in [(292,104),(352,100),(412,106),(318,140),(380,142)]:
    o+=circ(cx,cy,9,'#f6d5d1')+circ(cx-11,cy+8,5,'#fff',1)+circ(cx+11,cy+8,5,'#fff',1)
o+=line(298,116,312,130,BLUE,1.6,'3 3')+line(358,114,372,130,BLUE,1.6,'3 3')
# network: hex lattice of C
pts=[]
for j in range(3):
    for i in range(5):
        pts.append((50+i*34+(17 if j%2 else 0),296+j*24))
for k,(a,b) in enumerate(pts):
    for (c,d) in pts[k+1:]:
        if 20<math.hypot(a-c,b-d)<36: o+=line(a,b,c,d,INK,1.6)
for (a,b) in pts: o+=circ(a,b,6,'#c9d3dc',1.2)
# metallic
o+=f'<rect x="262" y="282" width="176" height="80" rx="8" fill="#e6e1f5" stroke="none"/>'
for i in range(5):
    for j in range(2):
        cx,cy=284+i*34,302+j*40; o+=circ(cx,cy,11,'#fde9c8',1.2)+T(cx,cy+4,'+',11,weight='800')
for (cx,cy) in [(301,322),(335,322),(369,322),(403,322),(272,316),(432,328)]:
    o+=circ(cx,cy,3.5,BLUE,0.6)

svg('solid_types.svg',470,424,o,'Four types of crystalline solids. Ionic, for example NaCl: a grid of alternating positive and negative ions held by ionic bonds; high melting point; conducts when melted or dissolved. Molecular, for example ice, dry ice, and sugar: separate molecules held together by intermolecular forces, shown as dashed attractions between water molecules; low melting point; does not conduct. Covalent network, for example diamond and quartz, SiO2: atoms joined in a web of covalent bonds; very high melting point; very hard. Metallic, for example iron, copper, and aluminum: metal cations in a sea of moving electrons; a wide range of melting points; conducts electricity.')

# 9. Vapor pressure and boiling
o=T(235,22,'Evaporation, vapor pressure, and boiling',16,weight='800')
o+=rect(10,40,220,236)+rect(240,40,220,236)
o+=T(120,60,'Closed container',13,weight='800')+T(350,60,'Boiling',13,weight='800')
# closed jar
o+=f'<path d="M40 90 h160 v160 h-160 z" fill="#fff" stroke="{INK}" stroke-width="2"/>'+f'<rect x="40" y="170" width="160" height="80" fill="#dbe7f6"/>'+line(40,170,200,170,BLUE,2)
for (x,y) in [(62,110),(110,100),(160,118),(86,140),(182,146),(132,134)]: o+=circ(x,y,5,'#9fb6d6',1)
for (x,y) in [(60,190),(90,205),(120,188),(150,210),(180,192),(75,232),(110,232),(145,236),(178,228)]: o+=circ(x,y,5,'#9fb6d6',1)
o+=arrow(100,176,96,152,1.8,RED,'arR')+arrow(146,150,150,174,1.8,BLUE,'arB')
o+=T(120,268,'Rates equal: vapor pressure',11,weight='700')
# boiling pot
o+=f'<path d="M270 110 v94 a10 10 0 0 0 10 10 h140 a10 10 0 0 0 10 -10 v-94" fill="#dbe7f6" stroke="{INK}" stroke-width="2"/>'
for (x,y,r) in [(300,186,9),(340,160,12),(380,190,10),(410,140,8),(320,130,7),(368,128,9)]: o+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{BLUE}" stroke-width="1.6"/>'
for i in range(5): o+=f'<path d="M{294+i*28} 250 q6 -8 0 -14 q-6 -7 0 -14" stroke="{RED}" stroke-width="2" fill="none"/>'
o+=arrow(350,96,350,112,2,INK)+T(350,88,'air pressure pushes down',10.5,weight='700')
o+=T(350,268,'Vapor pressure = air pressure',11,weight='700')
o+=T(235,296,'Stronger IMFs → lower vapor pressure → higher boiling point.',12,weight='800')
o+=T(235,314,'A liquid boils when its vapor pressure equals the pressure above it.',11.5,weight='600')
svg('vapor_boiling.svg',470,326,o,'Two panels. Left, a closed container partly filled with a liquid: some molecules leave the surface as vapor (evaporation) while others return (condensation); when the two rates are equal, the vapor exerts a steady pressure, the vapor pressure. Right, a pot of water being heated from below, with bubbles of vapor forming throughout the liquid while air pressure pushes down on the surface. Bubbles form when the vapor pressure of the liquid equals the pressure above it. Stronger intermolecular forces mean lower vapor pressure and a higher boiling point.')
print('ok', sorted(os.listdir(OUT)))
