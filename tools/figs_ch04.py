#!/usr/bin/env python3
"""Chapter 4 figures (SVG), phone-first (~470 px wide, 13-17 px text). python3 tools/figs_ch04.py"""
import os
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch04'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>'
def svg(name,W,H,body,aria,title=None):
    t=f'<title>{title}</title>' if title else ''
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}">{t}<rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.2,c=INK): return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#ar)"/>'
def box(x,y,w,h,fill,lines,size=14,stroke=INK,rx=8):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
    n=len(lines); y0=y+h/2-(n-1)*size*0.62+size*0.35
    for i,l in enumerate(lines): s+=T(x+w/2,y0+i*size*1.24,l,size,weight='800' if i==0 else '600')
    return s
def sup(s,z=11): return f'<tspan baseline-shift="super" font-size="{z}">{s}</tspan>'
def sub(s,z=11): return f'<tspan baseline-shift="sub" font-size="{z}">{s}</tspan>'

# 1. Swap-drop
o=T(235,24,'Swap-drop: aluminum oxide',16,weight='800')
o+=T(150,82,'Al'+sup('3+',20),34,weight='800')+T(320,82,'O'+sup('2−',20),34,weight='800')
# crossing arrows from charges to subscript positions
o+=f'<path d="M180 94 C 230 120, 280 140, 330 160" stroke="#c0392b" stroke-width="2.4" fill="none" marker-end="url(#ar)"/>'
o+=f'<path d="M345 94 C 290 120, 220 140, 165 160" stroke="#2f6f9a" stroke-width="2.4" fill="none" marker-end="url(#ar)"/>'
o+=T(235,200,'Al'+sub('2',24)+'O'+sub('3',24),38,weight='800')
o+=T(235,250,'The number of each charge (not its sign) becomes',13,weight='600')+T(235,268,'the subscript of the OTHER ion.',13,weight='600')
o+=T(235,292,'Check: 2(3+) + 3(2−) = 6+ + 6− = 0',14,weight='800')
o+=f'<line x1="20" y1="300" x2="450" y2="300" stroke="#c9d3dc" stroke-width="1.5"/>'
o+=T(235,326,'Reduce when you can: calcium oxide',16,weight='800')
o+=T(235,362,'Ca'+sup('2+',15)+'  O'+sup('2−',15)+'  →  Ca'+sub('2',15)+'O'+sub('2',15)+'  →  CaO',24,weight='800')
o+=T(235,394,'Ionic formulas use the smallest whole-number ratio.',13,weight='600')
svg('swap_drop.svg',470,408,o,'Swap-drop method. Aluminum ion, Al 3+, and oxide ion, O 2-, are written side by side. Crossing arrows carry the 3 from aluminum down to become the subscript of oxygen and the 2 from oxide down to become the subscript of aluminum, giving Al2O3. Check: 2 times 3+ plus 3 times 2- equals 6+ plus 6- equals 0. Second example: Ca 2+ and O 2- swap to Ca2O2, which reduces to CaO, because ionic formulas use the smallest whole-number ratio.')

# 2. Oxyanion ladder (chlorine family)
o=T(235,24,'Oxyanions of chlorine (all 1− charge)',16,weight='800')
rows=[('per___ate','ClO'+sub('4')+sup('−'),'perchlorate','one MORE O than -ate'),('___ate','ClO'+sub('3')+sup('−'),'chlorate','the -ate ion on your green sheet'),('___ite','ClO'+sub('2')+sup('−'),'chlorite','one LESS O than -ate'),('hypo___ite','ClO'+sup('−'),'hypochlorite','one less O than -ite')]
y=44
for i,(pat,f,name,note) in enumerate(rows):
    fill=['#efe3f7','#fde9c8','#dbe7f6','#e3f2e1'][i]
    o+=f'<rect x="20" y="{y}" width="430" height="64" rx="10" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>'
    o+=T(40,y+28,f,22,anchor='start',weight='800')+T(150,y+28,name,17,anchor='start',weight='800')+T(150,y+50,note,13,anchor='start',weight='600')
    o+=T(400,y+28,f'{4-i} O',15,weight='800')
    y+=74
o+=T(235,y+14,'Same pattern for Br and I: BrO'+sub('3')+sup('−')+' bromate, IO'+sup('−')+' hypoiodite.',13,weight='600')
o+=T(235,y+34,'Adding or removing O never changes the charge.',13,weight='800')
svg('oxyanions.svg',470,y+46,o,'Oxyanions of chlorine, all with a 1- charge, listed from most to fewest oxygen atoms: perchlorate, ClO4-, 4 oxygens, one more oxygen than the -ate ion; chlorate, ClO3-, 3 oxygens, the -ate ion on the green sheet; chlorite, ClO2-, 2 oxygens, one less oxygen than -ate; hypochlorite, ClO-, 1 oxygen, one less oxygen than -ite. The same pattern works for bromine and iodine, for example BrO3- bromate and IO- hypoiodite. Adding or removing oxygen never changes the charge.')

# 3. Ion to acid mapping
o=T(235,24,'From anion name to acid name',16,weight='800')
rows=[('-ide ion','hydro-___-ic acid','chloride, Cl'+sup('−'),'hydrochloric acid, HCl(aq)'),('-ate ion','___-ic acid','chlorate, ClO'+sub('3')+sup('−'),'chloric acid, HClO'+sub('3')),('-ite ion','___-ous acid','chlorite, ClO'+sub('2')+sup('−'),'chlorous acid, HClO'+sub('2'))]
y=44
for i,(a,b,ex1,ex2) in enumerate(rows):
    o+=box(14,y,170,64,'#dbe7f6',[a,ex1],14)+arrow(188,y+32,224,y+32,2.6)+box(230,y,228,64,'#fde9c8',[b,ex2],14)
    y+=80
o+=T(235,y+6,'Prefixes stay: hypochlorite → hypochlorous acid;',13,weight='600')+T(235,y+24,'perchlorate → perchloric acid.',13,weight='600')
y+=18;o+=T(235,y+26,'Add enough H'+sup('+')+' to cancel the anion charge: SO'+sub('4')+sup('2−')+' → H'+sub('2')+'SO'+sub('4')+' (sulfuric acid).',12,weight='600')
o+=T(235,y+50,'Memory aids: "I hate this mnemonic" (-ate → -ic);',13,weight='800')+T(235,y+68,'"Sprite is delicious" (-ite → -ous)',13,weight='800')
svg('acid_names.svg',470,y+80,o,'Matching anion names to acid names. An -ide ion becomes a hydro- -ic acid: chloride, Cl-, becomes hydrochloric acid, HCl(aq). An -ate ion becomes an -ic acid: chlorate, ClO3-, becomes chloric acid, HClO3. An -ite ion becomes an -ous acid: chlorite, ClO2-, becomes chlorous acid, HClO2. Prefixes stay: hypochlorite becomes hypochlorous acid and perchlorate becomes perchloric acid. Add enough H+ to cancel the anion charge: sulfate, SO4 2-, becomes H2SO4, sulfuric acid. Memory aids: I hate this mnemonic, for -ate to -ic; Sprite is delicious, for -ite to -ous.')

# 4. Naming flowchart (blue naming sheet order: metal? -> charges? -> count; H first? -> acid / count)
NOTE="#4a5a66"
def qbox(x,y,w,h,lines,size=13.5,fill='#f3f6fa',notes=(),nsize=11.5):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'
    yy=y+size+5
    for l in lines: s+=T(x+w/2,yy,l,size,weight='800'); yy+=size*1.25
    yy+=2
    for l in notes: s+=T(x+w/2,yy,l,nsize,weight='600',fill=NOTE,extra='font-style="italic"'); yy+=nsize*1.3
    return s
def leaf(x,y,w,lines,fill):
    h=len(lines)*16+12
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'
    for i,l in enumerate(lines): s+=T(x+w/2,y+20+i*16,l,13 if i==0 else 12.5,weight='800' if i==0 else '600')
    return s,h
def bus(cx,ytop,colx,colw,leaves,fill):
    """Vertical line from a 'count' box down the left side of a column, short arrow into each leaf."""
    s=''; y=ytop+12; lx=colx+18; lw=colw-18; mids=[]
    for lines in leaves:
        b,h=leaf(lx,y,lw,lines,fill); s+=b; mids.append(y+h/2); y+=h+8
    bx=colx+5
    s+=f'<path d="M{bx} {ytop} V{mids[-1]}" stroke="{INK}" stroke-width="1.8" fill="none"/>'
    for m in mids: s+=arrow(bx,m,lx-1,m,1.8)
    return s,y-8
def vlabel(x,y,s):
    """Rotated YES/NO label sitting on a vertical connector line (white patch behind it)."""
    h=len(s)*9+6
    return f'<rect x="{x-7}" y="{y-h/2}" width="14" height="{h}" fill="#fff"/>'+T(x+4.3,y,s,12,weight='800',extra=f'transform="rotate(-90 {x+4.3} {y})"')
NH4='NH'+sub('4')+sup('+')
LX,LW=20,218; RX,RW=246,202          # left column (metal YES), right column (metal NO)
LC,RC=LX+LW/2,RX+RW/2
o=T(235,22,'Naming any compound',17,weight='800')
o+=qbox(100,34,270,40,['Is there a metal (or '+NH4+')?'],15)
o+=f'<path d="M235 74 V86 H{LC} V104" stroke="{INK}" stroke-width="2.2" fill="none" marker-end="url(#ar)"/>'
o+=f'<path d="M235 86 H{RC} V104" stroke="{INK}" stroke-width="2.2" fill="none" marker-end="url(#ar)"/>'
o+=T(LC+8,100,'YES',12,anchor='start',weight='800')+T(RC+8,100,'NO',12,anchor='start',weight='800')
# ---- left column: ionic
o+=qbox(LX,106,LW,82,['Can the metal have','more than one charge?'],notes=['transition metals except Zn, Ag;','also Sn, Pb'])
o+=arrow(LC,188,LC,206)+T(LC+8,202,'NO',12,anchor='start',weight='800')
o+=qbox(LX,208,LW,28,['Count the elements'],13)
IONIC='#dbe7f6'
b,yend=bus(LC,236,LX,LW,[['2 elements: ionic binary','metal + nonmetal-ide','NaCl, sodium chloride'],
                          ['3 or more: ionic ternary','metal + polyatomic ion','(keep its ending)','K'+sub('2')+'CO'+sub('3')+', potassium carbonate']],IONIC)
o+=b
y2=yend+18
o+=f'<path d="M{LX} 160 H10 V{y2+14} H{LX-1}" stroke="{INK}" stroke-width="2.2" fill="none" marker-end="url(#ar)"/>'
o+=vlabel(10,(160+y2)/2,'YES')
o+=qbox(LX,y2,LW,28,['Count the elements'],13)
b,yendL=bus(LC,y2+28,LX,LW,[['2 elements: ionic binary','metal (Roman numeral charge)','+ nonmetal-ide','FeCl'+sub('3')+', iron(III) chloride'],
                            ['3 or more: ionic ternary','metal (Roman numeral charge)','+ polyatomic ion (keep ending)','CuSO'+sub('4')+', copper(II) sulfate']],IONIC)
o+=b
# ---- right column: acids and molecular
o+=qbox(RX,106,RW,50,['Is H written first','(and aqueous)?'])
o+=arrow(RC,156,RC,174)+T(RC+8,170,'YES',12,anchor='start',weight='800')
o+=qbox(RX,176,RW,28,['Acid'],13,fill='#fde9c8')
b,yend=bus(RC,204,RX,RW,[['H + one element','hydro- root -ic acid','HCl(aq), hydrochloric acid'],
                         ['-ate ion → -ic acid','HNO'+sub('3')+', nitric acid'],
                         ['-ite ion → -ous acid','HNO'+sub('2')+', nitrous acid']],'#fde9c8')
o+=b
y3=yend+18
o+=f'<path d="M{RX+RW} 131 H460 V{y3+14} H{RX+RW+1}" stroke="{INK}" stroke-width="2.2" fill="none" marker-end="url(#ar)"/>'
o+=vlabel(460,(131+y3)/2,'NO')
o+=qbox(RX,y3,RW,28,['Count the elements'],13)
b,yendR=bus(RC,y3+28,RX,RW,[['1 element: diatomic','name the element','Cl'+sub('2')+', chlorine'],
                            ['2 elements: covalent binary','prefixes + -ide','(no mono- on the first)','N'+sub('2')+'O'+sub('4')+', dinitrogen tetroxide']],'#e3f2e1')
o+=b
NAMING_ALT=('Flowchart for naming any compound, in the order of the blue naming sheet. First question: is there a metal (or the ammonium ion, NH4+)? '
 'If yes, ask: can the metal have more than one charge? (Transition metals except Zn and Ag can, and so can Sn and Pb.) '
 'If no, count the elements: 2 elements is an ionic binary compound, named metal plus nonmetal with an -ide ending, for example NaCl, sodium chloride; '
 '3 or more elements is an ionic ternary compound, named metal plus the polyatomic ion, keeping its ending, for example K2CO3, potassium carbonate. '
 'If yes, count the elements the same way, but write the metal charge as a Roman numeral: FeCl3, iron(III) chloride; CuSO4, copper(II) sulfate. '
 'If there is no metal, ask: is H written first (and is it aqueous)? If yes, it is an acid: H plus one element is named hydro-, root, -ic acid, for example HCl(aq), hydrochloric acid; '
 'an -ate ion becomes an -ic acid, for example HNO3, nitric acid; an -ite ion becomes an -ous acid, for example HNO2, nitrous acid. '
 'If no, count the elements: 1 element is a diatomic element, named as the element, for example Cl2, chlorine; '
 '2 elements is a covalent binary compound, named with prefixes (no mono- on the first element) and an -ide ending, for example N2O4, dinitrogen tetroxide.')
svg('naming_flowchart.svg',470,max(yendL,yendR)+16,o,NAMING_ALT,title='How to name any compound (blue naming sheet order)')

# 4b. Naming flowchart, LANDSCAPE print version (same content; larger labels for the PDF, where tall images are height-limited)
def qboxP(cx,y,w,h,lines,size=16,fill='#f3f6fa',notes=(),nsize=13.5):
    x=cx-w/2; s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'
    tot=len(lines)*size*1.25+(len(notes)*nsize*1.3+3 if notes else 0)
    yy=y+(h-tot)/2+size*0.95
    for l in lines: s+=T(cx,yy,l,size,weight='800'); yy+=size*1.25
    yy+=3
    for l in notes: s+=T(cx,yy-size*0.25+nsize*0.2,l,nsize,weight='600',fill=NOTE,extra='font-style="italic"'); yy+=nsize*1.3
    return s
def leafP(x,y,w,lines,fill):
    h=len(lines)*18+14
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'
    for i,l in enumerate(lines): s+=T(x+w/2,y+23+i*18,l,15 if i==0 else 14,weight='800' if i==0 else '600')
    return s,h
def busP(ytop,colx,colw,leaves,fill):
    s=''; y=ytop+14; lx=colx+16; lw=colw-16; mids=[]
    for lines in leaves:
        b,h=leafP(lx,y,lw,lines,fill); s+=b; mids.append(y+h/2); y+=h+10
    bx=colx+5
    s+=f'<path d="M{bx} {ytop} V{mids[-1]}" stroke="{INK}" stroke-width="2" fill="none"/>'
    for m in mids: s+=arrow(bx,m,lx-1,m,2)
    return s,y-10
def lab(x,y,s):
    """YES/NO label to the right of a down arrow, on a white patch."""
    return f'<rect x="{x-3}" y="{y-14}" width="{len(s)*11+6}" height="18" fill="#fff"/>'+T(x,y,s,14,anchor='start',weight='800')
def split(cx,y1,y2,xl,xr,yend,ll,lr):
    """Down from (cx,y1) to y2, then a horizontal bar to xl and xr with down arrows to yend; labels ll (left) and lr (right)."""
    s=f'<path d="M{cx} {y1} V{y2}" stroke="{INK}" stroke-width="2.2" fill="none"/>'
    s+=f'<path d="M{xl} {y2} H{xr}" stroke="{INK}" stroke-width="2.2" fill="none"/>'
    s+=arrow(xl,y2,xl,yend)+arrow(xr,y2,xr,yend)
    s+=lab(xl+8,yend-4,ll)+lab(xr+8,yend-4,lr)
    return s
NH4P='NH'+sub('4',13)+sup('+',13)
PW=984; CW=236; CX=[8,252,496,740]; CC=[x+CW/2 for x in CX]
M12=(CC[0]+CC[1])/2; M34=(CC[2]+CC[3])/2
o=T(PW/2,26,'Naming any compound',20,weight='800')
o+=qboxP(PW/2,38,380,44,['Is there a metal (or '+NH4P+')?'],17)
o+=split(PW/2,82,98,M12,M34,118,'YES','NO')
o+=qboxP(M12,120,360,74,['Can the metal have','more than one charge?'],notes=['transition metals except Zn, Ag; also Sn, Pb'])
o+=qboxP(M34,120,320,74,['Is H written first','(and aqueous)?'])
o+=split(M12,194,208,CC[0],CC[1],230,'NO','YES')
o+=split(M34,194,208,CC[2],CC[3],230,'YES','NO')
HY=232; HH=34
for i,(t,f) in enumerate([('Count the elements','#f3f6fa'),('Count the elements','#f3f6fa'),('Acid','#fde9c8'),('Count the elements','#f3f6fa')]):
    o+=qboxP(CC[i],HY,CW,HH,[t],15.5,fill=f)
S=lambda t:sub(t,12)
cols=[[['2 elements: ionic binary','metal + nonmetal-ide','NaCl, sodium chloride'],
       ['3 or more: ionic ternary','metal + polyatomic ion','(keep its ending)','K'+S('2')+'CO'+S('3')+', potassium carbonate']],
      [['2 elements: ionic binary','metal (Roman numeral charge)','+ nonmetal-ide','FeCl'+S('3')+', iron(III) chloride'],
       ['3 or more: ionic ternary','metal (Roman numeral charge)','+ polyatomic ion','(keep ending)','CuSO'+S('4')+', copper(II) sulfate']],
      [['H + one element','hydro- root -ic acid','HCl(aq), hydrochloric acid'],
       ['-ate ion → -ic acid','HNO'+S('3')+', nitric acid'],
       ['-ite ion → -ous acid','HNO'+S('2')+', nitrous acid']],
      [['1 element: diatomic','name the element','Cl'+S('2')+', chlorine'],
       ['2 elements: covalent binary','prefixes + -ide','(no mono- on the first)','N'+S('2')+'O'+S('4')+', dinitrogen tetroxide']]]
fills=[IONIC,IONIC,'#fde9c8','#e3f2e1']; ends=[]
for i in range(4):
    b,e=busP(HY+HH,CX[i],CW,cols[i],fills[i]); o+=b; ends.append(e)
svg('naming_flowchart_print.svg',PW,max(ends)+14,o,NAMING_ALT,title='How to name any compound (blue naming sheet order)')

# 5. Classify: ionic vs molecular particle picture
o=T(117,22,'Ionic: NaCl',16,weight='800')+T(352,22,'Molecular: H'+sub('2')+'O',16,weight='800')
o+=f'<rect x="12" y="34" width="210" height="190" rx="10" fill="#f6f8fb" stroke="{INK}" stroke-width="1.5"/><rect x="248" y="34" width="210" height="190" rx="10" fill="#f6f8fb" stroke="{INK}" stroke-width="1.5"/>'
for r in range(4):
    for c in range(4):
        x=45+c*48; y=62+r*44; na=(r+c)%2==0
        o+=f'<circle cx="{x}" cy="{y}" r="{12 if na else 17}" fill="{"#c9dcf0" if na else "#cfe8cf"}" stroke="{INK}" stroke-width="1.3"/>'+T(x,y+5,'Na⁺' if na else 'Cl⁻',11 if na else 12,weight='800')
import math
for (cx,cy) in [(300,80),(400,90),(320,175),(410,180),(360,128)]:
    o+=f'<circle cx="{cx}" cy="{cy}" r="17" fill="#f6d5d1" stroke="{INK}" stroke-width="1.3"/>'+T(cx,cy+5,'O',13,weight='800')
    for a in (-0.6,0.6):
        hx=cx+26*math.cos(math.pi/2+a+ (0)); hy=cy+26*math.sin(math.pi/2+a)
        o+=f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="10" fill="#fff" stroke="{INK}" stroke-width="1.3"/>'+T(hx,hy+4,'H',10,weight='800')
o+=T(117,246,'metal + nonmetal',13,weight='700')+T(117,264,'ions held by attraction',13,weight='600')
o+=T(352,246,'nonmetals only',13,weight='700')+T(352,264,'atoms share electrons',13,weight='600')
svg('ionic_vs_molecular.svg',470,276,o,'Two particle pictures. Left, ionic compound sodium chloride: a checkerboard grid of small sodium ions labeled Na+ and larger chloride ions labeled Cl-, a metal plus a nonmetal held together as ions by attraction. Right, molecular compound water: five separate molecules, each an O atom bonded to two H atoms; nonmetals only, atoms sharing electrons.')
print('ok')
