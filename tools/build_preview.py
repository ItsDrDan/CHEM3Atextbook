#!/usr/bin/env python3
"""Build a local preview site of the chapter drafts (LibreTexts-like styling) for checking renders.
python3 tools/build_preview.py <outdir>   then serve <outdir> with any static server.
GitHub Pages URLs for this repo are rewritten to local paths; YouTube iframes become placeholders; MathJax renders \\( \\)."""
import sys, os, re, shutil, glob
root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'); out=sys.argv[1]
for d in ('figures','js','css','bank'):
    if os.path.exists(os.path.join(root,d)): shutil.copytree(os.path.join(root,d),os.path.join(out,d),dirs_exist_ok=True)
shutil.copy(os.path.join(root,'practice.html'),out)
css=open(os.path.join(os.path.dirname(__file__),'preview.css')).read()
links=[]
for f in sorted(glob.glob(os.path.join(root,'drafts','ch*','*.html'))):
    src=open(f).read()
    src=src.replace('https://itsdrdan.github.io/CHEM3Atextbook/','')
    src=re.sub(r'\\\(\\PageIndex\{(\d+)\}\\\)',r'<span class="pi">N.\1</span>',src)
    src=re.sub(r'<iframe[^>]*youtube[^>]*></iframe>','<div class="yt">[YouTube video embed]</div>',src)
    name=os.path.basename(os.path.dirname(f))+'_'+os.path.basename(f); links.append(name)
    page=f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name}</title><style>{css}</style><script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]]}}}}</script><script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script><body><main>{src}</main></body>'
    open(os.path.join(out,name),'w').write(page)
open(os.path.join(out,'index.html'),'w').write('<!doctype html><meta charset="utf-8"><ul>'+''.join(f'<li><a href="{l}">{l}</a></li>' for l in links)+'</ul>')
print('built',len(links),'pages in',out)
