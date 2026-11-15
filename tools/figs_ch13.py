#!/usr/bin/env python3
"""Chapter 13 figures (SVG), phone-first (~470 px wide). python3 tools/figs_ch13.py"""
import os, math, random
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch13'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
RED="#c0392b"; BLUE="#2f5fa8"; GRN="#2e7d32"; GRAY="#c9d3dc"; GREY2="#55606b"; PUR="#7b4fa0"; ORG="#d35400"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
def mk(i,c): return f'<marker id="{i}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
DEFS='<defs>'+mk('ar',INK)+mk('arB',BLUE)+mk('arR',RED)+mk('arG',GRN)+'</defs>'
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
def eq(x,y,w=34,c=INK,wt=2):
    """equilibrium arrow (two half-headed harpoons) centered at x, y"""
    a,b=x-w/2,x+w/2
    return (f'<path d="M{a:.1f} {y-3:.1f} H{b:.1f} l-7 -5" stroke="{c}" stroke-width="{wt}" fill="none"/>'
            f'<path d="M{b:.1f} {y+3:.1f} H{a:.1f} l7 5" stroke="{c}" stroke-width="{wt}" fill="none"/>')
def path(d,c=INK,w=2.6,dash='',fill='none'):
    dd=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{fill}"{dd}/>'
def axes(x0,y0,w,h,xl,yl):
    s=arrow(x0,y0,x0+w,y0,1.8)+arrow(x0,y0,x0,y0-h,1.8)
    s+=T(x0+w/2,y0+22,xl,12,weight='700')+T(x0-14,y0-h/2,yl,12,weight='700',extra=f'transform="rotate(-90 {x0-14} {y0-h/2})"')
    return s
def curve(f,x0,y0,w,h,n=60,c=INK,wd=3,dash=''):
    pts=' '.join(f'{x0+w*i/n:.1f},{y0-h*f(i/n):.1f}' for i in range(n+1))
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{wd}"{d}/>'

# ---------- 1. Collision orientation: CO + NO2 -> CO2 + NO
def atom(x,y,el):
    col={'C':'#555','O':'#e57373','N':'#7fa7e0'}[el]; r={'C':12,'O':11,'N':12}[el]
    return circ(x,y,r,col,1.3)+T(x,y+4.5,el,11,weight='800',fill='#fff' if el=='C' else INK)
def CO(x,y,flip=False):  # C then O to the right (or flipped)
    a,b=('O','C') if flip else ('C','O')
    return line(x,y,x+22,y,INK,3)+atom(x,y,a)+atom(x+22,y,b)
def NO2(x,y,pointO_left=True):
    # N at center, one O pointing left (toward CO) and one up-right
    s=line(x,y,x-22,y,INK,3)+line(x,y,x+12,y-19,INK,3) if pointO_left else line(x,y,x+22,y,INK,3)+line(x,y,x-12,y-19,INK,3)
    if pointO_left: s+=atom(x-22,y,'O')+atom(x+12,y-19,'O')+atom(x,y,'N')
    else: s+=atom(x+22,y,'O')+atom(x-12,y-19,'O')+atom(x,y,'N')
    return s
o=T(235,22,'A collision must have the right orientation',16,weight='800')
o+=T(235,40,'CO + NO'+sub('2')+' → CO'+sub('2')+' + NO',13,weight='700')
# panel A: effective
o+=rect(10,52,450,128,'#eef7ee',stroke=GRN)
o+=T(22,72,'Effective: C of CO hits an O of NO'+sub('2')+', with enough energy',12,anchor='start',weight='800',fill=GRN)
o+=CO(40,120,True)+arrow(88,120,118,120,2.2)+NO2(170,120,True)
o+=arrow(206,120,250,120,2.6,GRN,'arG')
# products: CO2 and NO
o+=line(282,120,326,120,INK,3)+atom(282,120,'O')+atom(304,120,'C')+atom(326,120,'O')
o+=line(380,120,402,120,INK,3)+atom(380,120,'N')+atom(402,120,'O')
o+=T(304,154,'CO'+sub('2'),12,weight='800')+T(391,154,'NO',12,weight='800')+T(345,124,'+',14,weight='800')
o+=T(150,170,'reaction happens',11.5,weight='700',fill=GRN)
# panel B: wrong orientation
o+=rect(10,192,450,128,'#fdf0ee',stroke=RED)
o+=T(22,212,'Not effective: O of CO hits the N side, so they bounce apart',12,anchor='start',weight='800',fill=RED)
o+=CO(40,262)+arrow(88,262,118,262,2.2)+NO2(150,262,False)
o+=arrow(206,262,250,262,2.6,RED,'arR')
o+=CO(282,250)+NO2(390,272,False)
o+=arrow(270,238,252,226,1.8,RED,'arR')+arrow(418,284,438,296,1.8,RED,'arR')
o+=T(150,308,'no reaction',11.5,weight='700',fill=RED)
o+=T(235,344,'Effective collisions need (1) the right orientation and (2) at least the activation energy.',11.3,weight='800')
svg('collision_orientation.svg',470,356,o,'Collision theory for carbon monoxide reacting with nitrogen dioxide to form carbon dioxide and nitric oxide. Top panel, effective: the carbon end of CO strikes an oxygen atom of NO2 with enough energy, the oxygen atom transfers, and CO2 and NO form. Bottom panel, not effective: the oxygen end of CO hits the nitrogen side of NO2, and the two molecules bounce apart unchanged. Effective collisions need the right orientation and at least the activation energy.')

# ---------- 2. Activation energy diagram with and without catalyst
o=T(235,22,'Activation energy, with and without a catalyst',16,weight='800')
x0,y0,w,h=60,300,380,250
o+=axes(x0,y0,w,h,'Reaction progress','Energy')
def hump(t,peak,start=0.62,end=0.25):
    base=start+(end-start)*(1/(1+math.exp(-(t-0.5)*14)))
    return base+(peak-max(start,end))*math.exp(-((t-0.5)/0.13)**2)+ (max(start,end)-base)*math.exp(-((t-0.5)/0.13)**2)
f1=lambda t: hump(t,0.92); f2=lambda t: hump(t,0.76)
o+=curve(f1,x0+10,y0,w-30,h,80,INK,3)+curve(f2,x0+10,y0,w-30,h,80,BLUE,3,'7 5')
yR=y0-h*0.62; yP=y0-h*0.25; yT=y0-h*0.92; yC=y0-h*0.76
o+=line(x0+10,yR,x0+w-20,yR,GRAY,1.2,'4 4')
o+=T(x0+20,yR+20,'reactants',12,anchor='start',weight='800')+T(x0+w-24,yP+20,'products',12,anchor='end',weight='800')
xm=x0+10+(w-30)*0.5
o+=arrow(xm-60,yR,xm-60,yT+3,2,INK)+T(xm-68,(yR+yT)/2+4,'E'+sub('a'),13,anchor='end',weight='800')
o+=arrow(xm+46,yR,xm+46,yC+3,2,BLUE,'arB')+T(xm+54,(yR+yC)/2+8,'lower E'+sub('a'),12,anchor='start',weight='800',fill=BLUE)
o+=T(xm,yT-10,'without catalyst (solid)',11.5,weight='800')
o+=T(xm+80,yC-22,'with catalyst (dashed)',11.5,anchor='start',weight='800',fill=BLUE)
o+=arrow(x0+w-40,yR,x0+w-40,yP-3,1.8,GREY2)+T(x0+w-46,(yR+yP)/2+4,'ΔH',12,anchor='end',weight='800',fill=GREY2)
o+=T(235,346,'A catalyst lowers the energy hill for both directions; ΔH does not change.',11.5,weight='800')
svg('activation_energy.svg',470,358,o,'Energy diagram for an exothermic reaction. The vertical axis is energy and the horizontal axis is reaction progress. Reactants start at a medium energy, the path climbs over a hill, and products end at a lower energy. The height of the hill above the reactants is the activation energy, Ea. A dashed second path, with a catalyst, has a lower hill, so a lower activation energy. The energy difference between reactants and products, delta H, is the same for both paths. A catalyst lowers the energy hill for both directions and does not change delta H.')

# ---------- 3. Four factors that change rate
o=T(235,22,'Four ways to speed up a reaction',16,weight='800')
def particles(x,y,w,h,n,seed,col,r=4.5,fast=False):
    random.seed(seed); s=''; placed=[]
    tries=0
    while len(placed)<n and tries<5000:
        tries+=1
        px,py=x+r+14+random.random()*(w-2*r-18),y+r+4+random.random()*(h-2*r-8)
        if all((px-a)**2+(py-b)**2>(2*r+2)**2 for a,b in placed): placed.append((px,py))
    for px,py in placed:
        s+=circ(px,py,r,col,1)
        if fast: s+=line(px-r-2,py,px-r-11,py,GREY2,1.4)
    return s
panels=[(10,40,'More concentration','more collisions per second'),(240,40,'Higher temperature','faster and harder collisions'),
        (10,172,'More surface area','more particles exposed'),(240,172,'Add a catalyst','lower activation energy')]
for x,y,t,s in panels:
    o+=rect(x,y,220,124,'#f6fafe')+T(x+110,y+20,t,13,weight='800')+T(x+110,y+114,s,11,weight='700')
o+=rect(24,68,86,58,'#fff',4,1.2)+particles(24,68,86,58,4,1,'#9fb6d6')+rect(130,68,86,58,'#fff',4,1.2)+particles(130,68,86,58,10,2,'#9fb6d6')
o+=arrow(110,97,128,97,1.6)
o+=rect(254,68,86,58,'#fff',4,1.2)+particles(254,68,86,46,6,3,'#c9d7ea')+rect(360,68,86,58,'#fff',4,1.2)+particles(360,68,86,46,6,4,'#f2b8b0',fast=True)
o+=arrow(340,97,358,97,1.6)+T(297,123,'cool',10,weight='700')+T(403,123,'hot',10,weight='700',fill=RED)
o+=f'<rect x="40" y="200" width="44" height="44" fill="#fde9c8" stroke="{INK}" stroke-width="1.4"/>'
o+=arrow(98,222,124,222,1.6)
for i in range(4):
    for j in range(3):
        o+=f'<rect x="{136+i*20}" y="{198+j*16}" width="12" height="11" fill="#fde9c8" stroke="{INK}" stroke-width="1"/>'
o+=T(62,260,'one lump',10,weight='700')+T(170,260,'powder',10,weight='700')
gx,gy=256,262
o+=curve(lambda t: 0.10+0.62*math.exp(-((t-0.5)/0.16)**2),gx,gy,120,90,40,INK,2.4)
o+=curve(lambda t: 0.10+0.30*math.exp(-((t-0.5)/0.16)**2),gx,gy,120,90,40,BLUE,2.4,'6 4')
o+=T(gx+110,214,'no catalyst',10,anchor='start',weight='700')+T(gx+110,236,'catalyst',10,anchor='start',weight='700',fill=BLUE)
o+=T(gx+110,248,'(dashed)',10,anchor='start',weight='700',fill=BLUE)
o+=T(235,318,'Each change raises the number of effective collisions per second.',12,weight='800')
svg('rate_factors.svg',470,330,o,'Four ways to speed up a reaction, in four panels. More concentration: a box with a few particles becomes a box with many particles, so there are more collisions per second. Higher temperature: cool, slow particles become hot, fast-moving particles, so collisions are more frequent and more energetic. More surface area: one solid lump is broken into a powder, so more particles are exposed. Add a catalyst: a small energy diagram shows the dashed catalyzed path with a lower hill, a lower activation energy. Each change raises the number of effective collisions per second.')

# ---------- 4. Rates vs time
o=T(235,22,'Rates of the forward and reverse reactions',16,weight='800')
x0,y0,w,h=60,280,380,230
o+=axes(x0,y0,w,h,'Time','Rate')
k=6.0; fwd=lambda t: 0.45+0.45*math.exp(-k*t); rev=lambda t: 0.45*(1-math.exp(-k*t))
o+=curve(fwd,x0,y0,w-20,h,80,RED,3.2)+curve(rev,x0,y0,w-20,h,80,BLUE,3.2,'9 5')
te=x0+(w-20)*0.55
o+=line(te,y0,te,y0-h+10,GREY2,1.4,'4 4')+T(te+8,y0-h+24,'equilibrium reached:',12,anchor='start',weight='800')+T(te+8,y0-h+40,'forward rate = reverse rate',12,anchor='start',weight='800')
o+=T(x0+20,y0-h*0.92+4,'forward rate (solid) falls',12,anchor='start',weight='800',fill=RED)
o+=T(x0+30,y0-h*0.10,'reverse rate (dashed) rises',12,anchor='start',weight='800',fill=BLUE)
o+=T(235,324,'Both reactions keep going at equilibrium, at the same rate.',12,weight='800')
svg('rates_vs_time.svg',470,336,o,'Graph of reaction rate versus time for a reversible reaction that starts with only reactants. The forward rate, a solid line, starts high and falls. The reverse rate, a dashed line, starts at zero and rises. The two curves meet and then stay level at the same value: equilibrium is reached when the forward rate equals the reverse rate. Both reactions keep going at equilibrium, at the same rate.')

# ---------- 5. Concentrations vs time
o=T(235,22,'Concentrations level off at equilibrium',16,weight='800')
x0,y0,w,h=60,280,380,230
o+=axes(x0,y0,w,h,'Time','Concentration')
k=5.0; R=lambda t: 0.30+0.62*math.exp(-k*t); Pp=lambda t: 0.60*(1-math.exp(-k*t))+0.01
o+=curve(R,x0,y0,w-20,h,80,RED,3.2)+curve(Pp,x0,y0,w-20,h,80,BLUE,3.2,'9 5')
te=x0+(w-20)*0.62
o+=line(te,y0,te,y0-h+10,GREY2,1.4,'4 4')+T(te+8,y0-h+20,'equilibrium:',12,anchor='start',weight='800')+T(te+8,y0-h+36,'both flat (constant),',12,anchor='start',weight='800')+T(te+8,y0-h+52,'but not equal',12,anchor='start',weight='800')
o+=T(x0+w-22,y0-h*0.60-10,'product (dashed)',12,anchor='end',weight='800',fill=BLUE)
o+=T(x0+w-22,y0-h*0.30+20,'reactant (solid)',12,anchor='end',weight='800',fill=RED)
o+=T(235,324,'Constant does not mean equal: here product ends up about twice the reactant.',11.5,weight='800')
svg('conc_vs_time.svg',470,336,o,'Graph of concentration versus time for a reaction that starts with only reactant. The reactant concentration, a solid line, starts high and falls; the product concentration, a dashed line, starts at zero and rises. After a while both lines become flat: at equilibrium the concentrations are constant, but they are not equal. In this example the product ends up at about twice the reactant concentration.')

# ---------- 6. Size of K
o=T(235,22,'What the size of K tells you',16,weight='800')
o+=arrow(30,90,446,90,2.2)+line(30,82,30,98,INK,2)
for x,lab in [(60,'10'+sup('−30')),(150,'10'+sup('−3')),(235,'1'),(320,'10'+sup('3')),(410,'10'+sup('30'))]:
    o+=line(x,84,x,96,INK,2)+T(x,76,lab,12,weight='800')
o+=T(446,112,'K',13,anchor='end',weight='800')
for x,t1,t2,t3,col,fill in [(12,'K ≪ 1','mostly reactants','at equilibrium',RED,'#fdf0ee'),(166,'K ≈ 1','sizable amounts','of both',GREY2,'#f3f3f3'),(320,'K ≫ 1','mostly products','at equilibrium',BLUE,'#eef3fb')]:
    o+=rect(x,124,138,128,fill,stroke=col)+T(x+69,148,t1,15,weight='800',fill=col)+T(x+69,234,t2,11.5,weight='700')+T(x+69,248,t3,11.5,weight='700')
# particle mini boxes: R squares vs P circles
random.seed(7)
def mix(x,y,nr,npp):
    s=''
    pts=[(x+14+(i%5)*22,y+10+(i//5)*20) for i in range(10)]
    for i,(px,py) in enumerate(pts):
        if i<nr: s+=f'<rect x="{px-6}" y="{py-6}" width="12" height="12" fill="#f2b8b0" stroke="{INK}" stroke-width="1"/>'
        else: s+=circ(px,py,6,'#9fb6d6',1)
    return s
o+=mix(22,162,9,1)+mix(176,162,5,5)+mix(330,162,1,9)
o+=f'<rect x="60" y="270" width="12" height="12" fill="#f2b8b0" stroke="{INK}" stroke-width="1"/>'+T(80,281,'reactant',11.5,anchor='start',weight='700')
o+=circ(176,276,6,'#9fb6d6',1)+T(188,281,'product',11.5,anchor='start',weight='700')
o+=T(330,281,'K = products ÷ reactants',11.5,anchor='middle',weight='800')
svg('k_size.svg',470,296,o,'What the size of the equilibrium constant K tells you. A number line runs from 10 to the minus 30, through 1, to 10 to the 30. Three boxes below it. K much less than 1: an equilibrium mixture that is mostly reactant squares, with almost no product: mostly reactants at equilibrium. K about 1: about half reactant squares and half product circles: sizable amounts of both. K much greater than 1: mostly product circles: mostly products at equilibrium. K equals products divided by reactants.')

# ---------- 7. Le Chatelier: add a reactant
o=T(235,22,"Le Chatelier's principle: add a reactant",16,weight='800')
def seesaw(cx,y,tilt,lab_l,lab_r,nl,nr):
    a=math.radians(tilt); L=150
    x1,y1=cx-L*math.cos(a),y+L*math.sin(a); x2,y2=cx+L*math.cos(a),y-L*math.sin(a)
    by=lambda x: y1+(x-x1)*(y2-y1)/(x2-x1)
    s=f'<path d="M{cx-18} {y+40} L{cx} {y+4} L{cx+18} {y+40} z" fill="{GRAY}" stroke="{INK}" stroke-width="1.6"/>'+line(x1,y1,x2,y2,INK,4)
    for i in range(nl):
        px=x1+12+(i%4)*18; s+=f'<rect x="{px:.1f}" y="{by(px+6.5)-17-(i//4)*16:.1f}" width="13" height="13" fill="#f2b8b0" stroke="{INK}" stroke-width="1"/>'
    for i in range(nr):
        px=x2-60+(i%4)*18; s+=circ(px,by(px)-10-(i//4)*16,6.5,'#9fb6d6',1)
    s+=T(cx-100,y+58,lab_l,11.5,weight='800',fill=RED)+T(cx+100,y+58,lab_r,11.5,weight='800',fill=BLUE)
    return s
rows=[(70,0,'1. At equilibrium','rates equal; amounts constant',4,4),(215,10,'2. Stress: add reactant','more forward collisions',8,4),(360,0,'3. Shifts right (toward products)','some new reactant becomes product; a new equilibrium',6,6)]
for y,tilt,t1,t2,nl,nr in rows:
    o+=T(20,y-26,t1,13,anchor='start',weight='800')+T(20,y-10,t2,11,anchor='start',weight='700',fill=GREY2)
    o+=seesaw(235,y+40,tilt,'reactants','products',nl,nr)
o+=T(235,486,'Add a substance → shift away from it. Remove a substance → shift toward it.',12,weight='800')
svg('lechat_seesaw.svg',470,498,o,"Le Chatelier's principle shown as a seesaw with reactant squares on the left and product circles on the right. Step 1, at equilibrium: four reactants and four products, the seesaw level; rates are equal and amounts constant. Step 2, stress: extra reactant is added, eight squares on the left, and the seesaw tips; there are more forward collisions. Step 3, the system shifts right, toward products: some of the new reactant becomes product, six and six, and a new equilibrium is reached. Add a substance and the reaction shifts away from it; remove a substance and it shifts toward it.")

# ---------- 8. Pressure / volume: N2O4 <-> 2 NO2
o=T(235,22,'Squeezing a gas mixture: count moles of gas',16,weight='800')
o+=T(160,46,'N'+sub('2')+'O'+sub('4')+'(g)',13,anchor='end',weight='800')+eq(185,42)+T(210,46,'2 NO'+sub('2')+'(g)',13,anchor='start',weight='800')
o+=T(330,46,'1 mol gas vs 2 mol gas',11.5,anchor='start',weight='700',fill=GREY2)
def n2o4(x,y): return line(x-6,y,x+6,y,INK,2.4)+circ(x-6,y,6,'#f3e0b5',1)+circ(x+6,y,6,'#f3e0b5',1)
def no2(x,y): return circ(x,y,6,'#c97a3d',1)
random.seed(11)
o+=rect(20,64,180,170,'#fff',4,2)
def spread(n,x,y,w,h,d=24):
    pts=[]; t=0
    while len(pts)<n and t<20000:
        t+=1; p=(x+random.random()*w,y+random.random()*h)
        if all((p[0]-a)**2+(p[1]-b)**2>d*d for a,b in pts): pts.append(p)
    return pts
pts=spread(14,40,84,140,130)
for i,(x,y) in enumerate(pts): o+=n2o4(x,y) if i<6 else no2(x,y)
o+=T(110,256,'before: at equilibrium',12,weight='800')+T(110,272,'6 N'+sub('2')+'O'+sub('4')+', 8 NO'+sub('2')+' (14 molecules)',11,weight='700')
o+=arrow(212,150,248,150,2.2)+T(230,138,'squeeze',10.5,weight='700')
o+=rect(262,104,150,130,'#fff',4,2)+f'<rect x="262" y="84" width="150" height="16" fill="{GRAY}" stroke="{INK}" stroke-width="1.4"/>'+arrow(337,66,337,82,2)
pts=spread(12,280,120,114,98,23)
for i,(x,y) in enumerate(pts): o+=n2o4(x,y) if i<8 else no2(x,y)
o+=T(337,256,'after: shifted left',12,weight='800')+T(337,272,'8 N'+sub('2')+'O'+sub('4')+', 4 NO'+sub('2')+' (12 molecules)',11,weight='700')
o+=rect(20,290,430,62,'#f6fafe')
o+=T(235,314,'Smaller volume (higher pressure) → shift toward FEWER moles of gas.',12,weight='800')
o+=T(235,336,'Larger volume (lower pressure) → shift toward MORE moles of gas.',12,weight='800')
svg('pressure_shift.svg',470,362,o,'Squeezing a gas mixture of dinitrogen tetroxide and nitrogen dioxide, N2O4 in equilibrium with 2 NO2: one mole of gas on the left and two moles on the right. Before, at equilibrium in a large container: 6 N2O4 molecules and 8 NO2 molecules, 14 molecules in all. A piston squeezes the container to a smaller volume. After, the equilibrium has shifted left: 8 N2O4 and 4 NO2, 12 molecules, because pairs of NO2 combined. A smaller volume, or higher pressure, shifts the reaction toward fewer moles of gas; a larger volume, or lower pressure, shifts it toward more moles of gas.')

# ---------- 9. Hemoglobin at lungs vs tissues
o=T(235,22,'Hemoglobin and oxygen: one equilibrium, two places',16,weight='800')
o+=T(150,52,'Hb + O'+sub('2'),14,anchor='end',weight='800')+eq(182,48,40)+T(210,52,'HbO'+sub('2'),14,anchor='start',weight='800')
o+=T(290,52,'(simplified)',11,anchor='start',weight='700',fill=GREY2)
for x,t,c,fill,l1,l2,l3,arr in [(10,'In the lungs (alveoli)',RED,'#fdf0ee','high O'+sub('2')+' pressure','→ shifts RIGHT','hemoglobin loads O'+sub('2'),'r'),
                                 (240,'In working tissues',BLUE,'#eef3fb','low O'+sub('2')+' pressure','← shifts LEFT','HbO'+sub('2')+' releases O'+sub('2'),'l')]:
    o+=rect(x,70,220,180,fill,stroke=c)+T(x+110,92,t,13,weight='800',fill=c)
    # red blood cell
    o+=f'<ellipse cx="{x+110}" cy="150" rx="46" ry="26" fill="#f2b8b0" stroke="{INK}" stroke-width="1.6"/><ellipse cx="{x+110}" cy="150" rx="20" ry="9" fill="#e79a90"/>'
    for k in range(5):
        ox=x+30+k*40; oy=118 if k%2 else 186
        o+=line(ox-5,oy,ox+5,oy,INK,2)+circ(ox-5,oy,5,'#fff',1.2,RED)+circ(ox+5,oy,5,'#fff',1.2,RED)
        if arr=='r': o+=arrow(ox,oy+(10 if oy<150 else -10),x+110+(ox-x-110)*0.35,150+(oy-150)*0.35,1.4,RED,'arR')
        else: o+=arrow(x+110+(ox-x-110)*0.45,150+(oy-150)*0.45,ox,oy+(10 if oy<150 else -10),1.4,BLUE,'arB')
    o+=T(x+110,212,l1,11.5,weight='800')+T(x+110,228,l2,11.5,weight='800',fill=c)+T(x+110,244,l3,11.5,weight='700')
o+=rect(10,262,450,64,'#f6f6f6',stroke=GREY2)
o+=T(235,284,'Carbon monoxide: Hb + CO '+'→'+' HbCO binds far more tightly than O'+sub('2')+',',11.5,weight='800')
o+=T(235,302,'so hemoglobin tied up as HbCO cannot carry O'+sub('2')+' (shown → for simplicity;',11.5,weight='700')
o+=T(235,318,'it is also an equilibrium, which lies far to the right).',11.5,weight='700')
svg('hemoglobin.svg',470,336,o,'Hemoglobin and oxygen, Hb plus O2 in equilibrium with HbO2, simplified. Left panel, in the lungs: the oxygen pressure in the alveoli is high, so the equilibrium shifts right and red blood cells load oxygen; arrows point from oxygen molecules into the cell. Right panel, in working tissues: oxygen pressure is low, so the equilibrium shifts left and HbO2 releases oxygen; arrows point out of the cell. Bottom: carbon monoxide binds hemoglobin far more tightly than oxygen, so hemoglobin tied up as HbCO cannot carry oxygen. That binding is also an equilibrium, one that lies far to the right.')

# ---------- 10. CO2 / bicarbonate and breathing
o=T(235,22,'Breathing rate shifts the CO'+sub('2')+' equilibrium in blood',16,weight='800')
y=58
o+=T(20,y,'CO'+sub('2')+' + H'+sub('2')+'O',13.5,anchor='start',weight='800')+eq(140,y-4,30)+T(166,y,'H'+sub('2')+'CO'+sub('3'),13.5,anchor='start',weight='800')+eq(250,y-4,30)+T(276,y,'H'+sup('+')+' + HCO'+sub('3')+sup('−'),13.5,anchor='start',weight='800')
o+=T(20,y+20,'(blood)',10.5,anchor='start',weight='700',fill=GREY2)+T(166,y+20,'carbonic acid',10.5,anchor='start',weight='700',fill=GREY2)+T(276,y+20,'H ion + bicarbonate',10.5,anchor='start',weight='700',fill=GREY2)
for yy,t,c,fill,lines in [(94,'Breathing fast (hyperventilation)',BLUE,'#eef3fb',['more CO'+sub('2')+' breathed out → CO'+sub('2')+' removed','shift LEFT ← : fewer H'+sup('+')+' ions','blood pH rises (respiratory alkalosis)']),
                          (214,'Breathing slow or blocked (hypoventilation)',RED,'#fdf0ee',['CO'+sub('2')+' builds up in the blood','shift RIGHT → : more H'+sup('+')+' ions','blood pH falls (respiratory acidosis)'])]:
    o+=rect(10,yy,450,108,fill,stroke=c)+T(24,yy+24,t,13.5,anchor='start',weight='800',fill=c)
    for i,l in enumerate(lines): o+=T(36,yy+50+i*20,l,12,anchor='start',weight='700')
o+=T(235,344,'Normal arterial blood pH is about 7.35 to 7.45.',12,weight='800')
svg('co2_breathing.svg',470,356,o,'Breathing rate shifts the carbon dioxide equilibrium in blood: CO2 plus H2O in equilibrium with carbonic acid, H2CO3, in equilibrium with hydrogen ion plus bicarbonate ion. Breathing fast, hyperventilation: more CO2 is breathed out, so CO2 is removed, the equilibrium shifts left, there are fewer hydrogen ions, and blood pH rises, respiratory alkalosis. Breathing slow or blocked, hypoventilation: CO2 builds up in the blood, the equilibrium shifts right, there are more hydrogen ions, and blood pH falls, respiratory acidosis. Normal arterial blood pH is about 7.35 to 7.45.')

print('ok', sorted(os.listdir(OUT)))
