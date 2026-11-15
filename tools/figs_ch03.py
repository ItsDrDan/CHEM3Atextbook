#!/usr/bin/env python3
"""Chapter 3 figures (SVG), phone-first (~470 px wide, 13-17 px text). python3 tools/figs_ch03.py
Colors are never the only cue."""
import os, math
OUT=os.path.join(os.path.dirname(__file__),'..','figures','ch03'); os.makedirs(OUT,exist_ok=True)
FF="Lato, Helvetica, Arial, sans-serif"; INK="#2d3f4b"
def T(x,y,s,size=15,anchor='middle',weight='700',fill=INK,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
DEFS=f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>'
def svg(name,W,H,body,aria):
    open(os.path.join(OUT,name),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{DEFS}{body}</svg>')
def arrow(x1,y1,x2,y2,w=2.4,c=INK): return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c}" stroke-width="{w}" fill="none" marker-end="url(#ar)"/>'

# 1. EM spectrum as a stacked list (long wavelength, low energy at top)
rows=[('Radio waves','over about 1 m','MRI scanners, radio'),('Microwaves','about 1 mm to 1 m','microwave ovens, cell phones'),
('Infrared','about 700 nm to 1 mm','heat lamps, pulse oximeter (940 nm)'),('Visible light','about 400 to 700 nm','red, orange, yellow, green, blue, violet'),
('Ultraviolet','about 10 to 400 nm','sunburn, germicidal UV-C lamps'),('X-rays','about 0.01 to 10 nm','radiographs, CT scans'),('Gamma rays','under about 0.01 nm','nuclear medicine, radiation therapy')]
o='';y=10
for i,(n,lam,use) in enumerate(rows):
    shade=['#f3f6fa','#e9eff7','#fbe3d8','#fff3c4','#e8e1f5','#dde3ee','#d5dbe6'][i]
    o+=f'<rect x="60" y="{y}" width="400" height="56" rx="8" fill="{shade}" stroke="{INK}" stroke-width="1.5"/>'
    o+=T(72,y+22,n,16,anchor='start',weight='800')+T(72,y+43,lam,13,anchor='start',weight='600')+T(450,y+22,'',1)
    o+=T(450,y+43,use,13,anchor='end',weight='600',extra='font-style="italic"')
    y+=62
o+=arrow(16,20,16,y-12,3)+T(36,(y)/2,'wavelength shorter, frequency and energy higher',13,weight='700',extra=f'transform="rotate(90 36 {y/2})"')
svg('em_spectrum.svg',470,y+4,o,'The electromagnetic spectrum listed from longest wavelength and lowest energy at the top to shortest wavelength and highest energy at the bottom: radio waves (longer than about 1 meter; MRI scanners, radio), microwaves (about 1 millimeter to 1 meter; microwave ovens, cell phones), infrared (about 700 nanometers to 1 millimeter; heat lamps, pulse oximeter at 940 nanometers), visible light (about 400 to 700 nanometers; red through violet), ultraviolet (about 10 to 400 nanometers; sunburn, germicidal UV-C lamps), X-rays (about 0.01 to 10 nanometers; radiographs, CT scans), and gamma rays (shorter than about 0.01 nanometer; nuclear medicine, radiation therapy). An arrow down the side says wavelength gets shorter and frequency and energy get higher.')

# 2. Bohr energy levels + hydrogen line spectrum
o=''
lv=[(1,262),(2,162),(3,117),(4,88),(5,72),(6,63)]
for n,y in lv:
    o+=f'<line x1="90" y1="{y}" x2="330" y2="{y}" stroke="{INK}" stroke-width="{2.5 if n<5 else 1.5}"/>'
    if n<5: o+=T(80,y+5,f'n = {n}',14,anchor='end',weight='800')
o+=T(80,60,'n = 5, 6 ...',12,anchor='end',weight='700')
o+=T(235,30,'Energy levels of the hydrogen atom',15,weight='800')+arrow(370,262,370,62,2)+T(380,150,'higher',13,anchor='start',weight='700')+T(380,166,'energy',13,anchor='start',weight='700')
o+=arrow(125,260,125,165,3,'#2f6f9a')+T(133,215,'absorb energy:',12,anchor='start',weight='700')+T(133,230,'excitation',12,anchor='start',weight='700')
o+=arrow(240,118,240,159,3,'#c0392b')+f'<path d="M250 140 q8 -8 16 0 t16 0 t16 0" stroke="#c0392b" stroke-width="2" fill="none"/>'+T(250,200,'emit a photon:',12,anchor='start',weight='700')+T(250,215,'relaxation',12,anchor='start',weight='700')
# line spectrum
sx,sy,sw=40,290,400
o+=f'<rect x="{sx}" y="{sy}" width="{sw}" height="50" fill="#111"/>'
for lam,lab in [(410,'410'),(434,'434'),(486,'486'),(656,'656')]:
    x=sx+(lam-380)/(720-380)*sw; col={410:'#7d4ccc',434:'#4f5bd5',486:'#2fa6c8',656:'#e0322a'}[lam]
    o+=f'<rect x="{x-2}" y="{sy}" width="4" height="50" fill="{col}"/>'+T(x,sy+68,lab,13,weight='800')
o+=T(240,sy+90,'Hydrogen emission lines, wavelength in nm (visible region)',13,weight='700')
o+=T(240,sy+108,'Each line is one jump down between two energy levels.',13,weight='600')
svg('bohr_levels.svg',470,sy+118,o,'Bohr model energy levels of hydrogen drawn as horizontal lines labeled n = 1 at the bottom through n = 5 near the top, getting closer together as n increases. An upward arrow from n = 1 to n = 2 shows an electron absorbing energy (excitation). A downward arrow from n = 3 to n = 2 with a wavy line shows an electron emitting a photon (relaxation). Below, hydrogen visible emission spectrum: four bright lines on a black background at 410, 434, 486, and 656 nanometers. Each line is one jump down between two energy levels.')

# 3. Filling order (diagonal method)
o=T(235,24,'Order in which subshells fill',16,weight='800')
grid=[['1s'],['2s','2p'],['3s','3p','3d'],['4s','4p','4d','4f'],['5s','5p','5d','5f'],['6s','6p','6d'],['7s','7p']]
cx=lambda c:70+c*70; cy=lambda r:56+r*38
for k in range(9):
    pts=sorted((r,c) for r in range(7) for c in range(len(grid[r])) if r+c==k)
    if not pts: continue
    (r1,c1),(r2,c2)=pts[0],pts[-1]
    x1,y1=cx(c1)+0.55*70,cy(r1)-0.55*38; x2,y2=cx(c2)-0.62*70,cy(r2)+0.62*38
    o+=f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="#c0392b" stroke-width="2.4" fill="none" marker-end="url(#ar)"/>'
for r,row in enumerate(grid):
    for c,s_ in enumerate(row):
        x=cx(c); y=cy(r)
        o+=f'<rect x="{x-24}" y="{y-14}" width="48" height="28" rx="6" fill="#eef5fb" stroke="{INK}" stroke-width="1.2"/>'+T(x,y+5,s_,15,weight='800')
o+=T(360,80,'Follow each red',13,anchor='start',weight='700')+T(360,97,'arrow from top',13,anchor='start',weight='700')+T(360,114,'right to bottom',13,anchor='start',weight='700')+T(360,131,'left, starting',13,anchor='start',weight='700')+T(360,148,'at the top.',13,anchor='start',weight='700')
o+=T(235,350,'1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s 4f 5d 6p 7s 5f 6d 7p',13,weight='800')
o+=T(235,372,'Capacity: s holds 2, p holds 6, d holds 10, f holds 14 electrons',13,weight='600')
svg('filling_order.svg',470,382,o,'Diagonal method for the order in which subshells fill. Subshells are written in rows: 1s; 2s 2p; 3s 3p 3d; 4s 4p 4d 4f; 5s 5p 5d 5f; 6s 6p 6d; 7s 7p. Red diagonal arrows run from upper right to lower left. Following them from the top gives the filling order: 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, 5s, 4d, 5p, 6s, 4f, 5d, 6p, 7s, 5f, 6d, 7p. Capacity: an s subshell holds 2 electrons, p holds 6, d holds 10, and f holds 14.')

# 4. Periodic table blocks
cw,ch,x0,y0=25.5,26,12,40; o=''
def blk(r,c):
    if c in (1,2) or (r==1 and c==18): return 's'
    if 3<=c<=12: return 'd'
    return 'p'
FILL={'s':'#dbe7f6','p':'#fde9c8','d':'#e3f2e1','f':'#efe3f7'}
for r in range(1,8):
    for c in range(1,19):
        if r==1 and c not in (1,18): continue
        if r in (2,3) and 3<=c<=12: continue
        b=blk(r,c); o+=f'<rect x="{x0+(c-1)*cw}" y="{y0+(r-1)*ch}" width="{cw}" height="{ch}" fill="{FILL[b]}" stroke="{INK}" stroke-width=".7"/>'
    o+=T(x0-4,y0+(r-1)*ch+18,str(r),11,anchor='end',weight='700')
for r in range(2):
    for c in range(14):
        o+=f'<rect x="{x0+3*cw+c*cw}" y="{y0+7*ch+14+r*ch}" width="{cw}" height="{ch}" fill="{FILL["f"]}" stroke="{INK}" stroke-width=".7"/>'
o+=T(x0+cw,y0+3.6*ch,'s',22,weight='900')+T(x0+7.5*cw,y0+5*ch,'d',22,weight='900')+T(x0+15*cw,y0+3.6*ch,'p',22,weight='900')+T(x0+10*cw,y0+8.8*ch+14,'f',22,weight='900')
o+=T(x0+17.5*cw,y0+18,'s',13,weight='800')+T(x0+0.5*cw,y0-8,'1',11)+T(x0+17.5*cw,y0-8,'18',11)
by=y0+9*ch+30
for i,(b,lab) in enumerate([('s','s block: groups 1–2 (and He)'),('p','p block: groups 13–18'),('d','d block: groups 3–12'),('f','f block: lanthanides, actinides')]):
    yy=by+i*22; o+=f'<rect x="{x0}" y="{yy}" width="20" height="15" fill="{FILL[b]}" stroke="{INK}"/>'+T(x0+28,yy+12,lab,13,anchor='start',weight='700')
svg('pt_blocks.svg',484,by+4*22+6,o,'Periodic table outline divided into blocks, each labeled with a large letter: the s block is groups 1 and 2 plus helium; the p block is groups 13 to 18; the d block is groups 3 to 12; the f block is the two rows set below the table (lanthanides and actinides). Rows are numbered 1 to 7.')

# 5. Orbital diagrams
def box(x,y,e):
    s=f'<rect x="{x}" y="{y}" width="34" height="30" fill="#fff" stroke="{INK}" stroke-width="1.6"/>'
    if e>=1: s+=f'<path d="M{x+11} {y+25} V{y+6} M{x+6} {y+11} L{x+11} {y+5} L{x+16} {y+11}" stroke="{INK}" stroke-width="2" fill="none"/>'
    if e==2: s+=f'<path d="M{x+23} {y+5} V{y+24} M{x+18} {y+19} L{x+23} {y+25} L{x+28} {y+19}" stroke="{INK}" stroke-width="2" fill="none"/>'
    return s
def diagram(y,label,conf,sub):
    s=T(10,y+20,label,17,anchor='start',weight='800')+T(10,y+40,conf,14,anchor='start',weight='600')
    x=150
    for name,es in sub:
        for k,e in enumerate(es): s+=box(x+k*34,y,e)
        s+=T(x+len(es)*17,y+48,name,13,weight='700'); x+=len(es)*34+22
    return s
o=diagram(10,'Nitrogen','1s² 2s² 2p³',[('1s',[2]),('2s',[2]),('2p',[1,1,1])])
o+=diagram(80,'Oxygen','1s² 2s² 2p⁴',[('1s',[2]),('2s',[2]),('2p',[2,1,1])])
o+=T(10,170,'Each box is one orbital (holds at most 2 electrons, opposite spins: Pauli).',13,anchor='start',weight='600')
o+=T(10,190,'In 2p, electrons spread out one per box before pairing (Hund).',13,anchor='start',weight='600')
svg('orbital_diagrams.svg',470,200,o,'Orbital diagrams. Nitrogen, 1s2 2s2 2p3: the 1s box and the 2s box each hold a pair of electrons drawn as one up arrow and one down arrow; the three 2p boxes each hold one up arrow. Oxygen, 1s2 2s2 2p4: 1s and 2s boxes paired; the first 2p box holds a pair and the other two hold one up arrow each. Each box is one orbital holding at most 2 electrons with opposite spins (Pauli). In the 2p subshell, electrons spread out one per box before pairing (Hund).')

# 6. Trends
def outline(x0,y0,cw=20,ch=18):
    s=''
    for r in range(1,7):
        for c in range(1,19):
            if r==1 and c not in (1,18): continue
            if r in (2,3) and 3<=c<=12: continue
            s+=f'<rect x="{x0+(c-1)*cw}" y="{y0+(r-1)*ch}" width="{cw}" height="{ch}" fill="#f4f6f9" stroke="#9aa6b2" stroke-width=".6"/>'
    return s
def panel(y,title,col,left,up,l1,l2):
    X=80; s_=T(235,y,title,16,weight='800')
    s_+=outline(X,y+40)
    tw=18*20
    if left: s_+=arrow(X+tw,y+22,X+4,y+22,3,col)+T(X+tw/2,y+16,'across a period',12,weight='700')
    else: s_+=arrow(X,y+22,X+tw-4,y+22,3,col)+T(X+tw/2,y+16,'across a period',12,weight='700')
    if up: s_+=arrow(55,y+40+6*18,55,y+44,3,col)
    else: s_+=arrow(55,y+40,55,y+40+6*18-4,3,col)
    s_+=T(42,y+40+3*18,'down a group' if not up else 'up a group',12,weight='700',extra=f'transform="rotate(-90 42 {y+40+3*18})"')
    s_+=T(235,y+40+6*18+24,l1,13,weight='700')+T(235,y+40+6*18+42,l2,13,weight='600')
    return s_
o=panel(20,'Atomic radius increases','#2f6f9a',True,False,'going DOWN a group and to the LEFT across a period','(largest atoms at the lower left, e.g. Cs)')
o+=panel(250,'Ionization energy increases','#c0392b',False,True,'going UP a group and to the RIGHT across a period','(hardest to remove an electron at the upper right, e.g. He, F)')
y2=230
svg('trends.svg',470,250+40+6*18+52,o,'Two periodic table outlines with arrows. Atomic radius: an arrow pointing left across a period and an arrow pointing down a group show that atomic radius increases going down a group and to the left across a period; the largest atoms are at the lower left, such as cesium. Ionization energy: an arrow pointing right across a period and an arrow pointing up a group show that ionization energy increases going up a group and to the right across a period; it is hardest to remove an electron at the upper right, such as helium and fluorine.')
print('ok')
