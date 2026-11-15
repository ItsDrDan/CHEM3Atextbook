#!/usr/bin/env python3
"""Chapter 4 figures (SVG), phone-first (~470 px wide, 13-17 px text). python3 tools/figs_ch04.py"""
import os
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch04'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>'
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
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

# 4. Naming flowchart (stacked, phone-first)
o=T(235,22,'Naming any compound',17,weight='800')
o+=box(85,36,300,48,'#f3f6fa',['Look at the formula'],15)
o+=arrow(235,84,235,104)
o+=box(20,106,430,62,'#fde9c8',['Starts with H and is dissolved in water (aq)?','YES → ACID (Section 4.5)'],14)
o+=arrow(235,168,235,188)+T(244,182,'no',12,anchor='start',weight='700')
o+=box(20,190,430,62,'#dbe7f6',['Starts with a metal or NH'+sub('4')+'?','YES → IONIC (Sections 4.2–4.3)'],14)
o+=arrow(235,252,235,272)+T(244,266,'no',12,anchor='start',weight='700')
o+=box(20,274,430,62,'#e3f2e1',['Only nonmetals?','YES → MOLECULAR (Section 4.4)'],14)
# details
y=360
o+=T(20,y,'ACID',14,anchor='start',weight='900')+T(80,y,'H + -ide → hydro-…-ic acid;  -ate → -ic;  -ite → -ous',13,anchor='start',weight='600')
y+=26
o+=T(20,y,'IONIC',14,anchor='start',weight='900')+T(80,y,'Fixed-charge metal (groups 1, 2; Al, Zn, Ag) → metal name',13,anchor='start',weight='600')
o+=T(80,y+19,'Any other metal → Roman numeral for its charge',13,anchor='start',weight='600')
o+=T(80,y+38,'Anion: -ide for one element; polyatomic name as is',13,anchor='start',weight='600')
y+=64
o+=T(20,y,'MOLEC.',14,anchor='start',weight='900')+T(80,y,'Greek prefixes (no mono- on the first element);',13,anchor='start',weight='600')
o+=T(80,y+19,'second element ends in -ide',13,anchor='start',weight='600')
svg('naming_flowchart.svg',470,y+32,o,'Flowchart for naming any compound. Look at the formula. First question: does it start with H and is it dissolved in water (aq)? If yes, it is an acid (Section 4.5). If no, does it start with a metal or NH4? If yes, it is ionic (Sections 4.2 and 4.3). If no, is it only nonmetals? If yes, it is molecular (Section 4.4). Summary of rules: Acid: H plus an -ide ion gives hydro- -ic acid; -ate gives -ic acid; -ite gives -ous acid. Ionic: a fixed-charge metal (groups 1 and 2, plus Al, Zn, and Ag) keeps its name; any other metal gets a Roman numeral for its charge; the anion ends in -ide if it is one element, or keeps its polyatomic name. Molecular: Greek prefixes, no mono- on the first element, second element ends in -ide.')

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
