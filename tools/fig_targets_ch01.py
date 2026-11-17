#!/usr/bin/env python3
"""Accuracy vs precision archery targets for 1.3.1 Example 1.3.1.3 (replaces the inherited CK-12 image,
whose target (a) did not show a tight off-center cluster). Phone-first: 470 px wide, 15-16 px labels.
Writes figures/ch01/accuracy_targets.svg. Diagram: Daniel Kwasniewski, CC BY 4.0."""
import math, os
INK='#2d3f4b'; FF="Lato, Helvetica, Arial, sans-serif"
W,H=470,520
def T(x,y,s,size=15,weight='700'): return f'<text x="{x}" y="{y}" font-family="{FF}" font-size="{size}" font-weight="{weight}" text-anchor="middle" fill="{INK}">{s}</text>'
def target(cx,cy,hits,label,cap):
    o=''
    for i,r in enumerate([95,80,65,50,35,20]):
        o+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{"#d64545" if i%2==0 else "#ffffff"}" stroke="#d64545" stroke-width="1"/>'
    o+=f'<circle cx="{cx}" cy="{cy}" r="7" fill="#d64545"/>'
    for dx,dy in hits:
        o+=f'<circle cx="{cx+dx}" cy="{cy+dy}" r="5.5" fill="#111" stroke="#fff" stroke-width="1.6"/>'
    o+=T(cx,cy+124,label,17,'800')  # no captions: the example asks students to judge each target
    return o
# (a) precise, not accurate: tight cluster far from center (upper right)
a=[(40,-52),(53,-46),(42,-37),(55,-33)]
# (b) accurate on average, not precise: spread evenly around the center
b=[(-52,4),(30,-44),(38,40),(-14,50)]
# (c) precise and accurate: tight cluster on the bullseye
c=[(-6,3),(7,-4),(3,8),(-5,-7)]
# (d) neither: scattered, and their average sits well left of center
d=[(-80,8),(-28,-74),(-58,52),(-8,82)]
body=target(118,115,a,'(a)','tight group, off center')+target(352,115,b,'(b)','spread around center')+target(118,375,c,'(c)','tight group on center')+target(352,375,d,'(d)','scattered, off center')
aria=('Four archery targets. Target a: four marks close together in the upper-right ring, far from the bullseye. '
      'Target b: four marks spread out on different sides of the bullseye. Target c: four marks clustered on the bullseye. '
      'Target d: four marks scattered widely on the left half of the target, far apart and away from the bullseye.')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{aria}"><rect width="{W}" height="{H}" fill="#fff"/>{body}</svg>'
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','figures','ch01','accuracy_targets.svg')
open(out,'w').write(svg); print('wrote',os.path.normpath(out))
