import json,glob,sys,os
REPO=sys.argv[1]; dry=len(sys.argv)>2 and sys.argv[2]=='--dry'
R=json.load(open('repl.json'))
skip={'2-6'}
log=[]
cache={}
def rd(p):
    if p not in cache: cache[p]=open(p,encoding='utf8').read()
    return cache[p]
for r in R:
    if r['id'] in skip: log.append((r['id'],'SKIP-optional',r['old'][:60])); continue
    ch=r['ch']
    files=sorted(glob.glob(f'{REPO}/drafts/ch{ch}/*.html'))+[f'{REPO}/bank/ch{ch}.json',f'{REPO}/bank/ch{ch}_adapt.json']+sorted(glob.glob(f'{REPO}/tools/gen_*_ch{ch}.py'))
    variants=[(r['old'],r['new']),(json.dumps(r['old'],ensure_ascii=False)[1:-1],json.dumps(r['new'],ensure_ascii=False)[1:-1])]
    hits=[]
    for f in files:
        if not os.path.exists(f): continue
        t=rd(f)
        for o,n in variants:
            c=t.count(o)
            if c: hits.append((f,o,n,c)); break
    if not hits: log.append((r['id'],'MISS',r['old'][:80])); continue
    bad=[h for h in hits if h[3]!=1]
    if bad: log.append((r['id'],'MULTI',[(os.path.basename(h[0]),h[3]) for h in bad])); continue
    for f,o,n,c in hits:
        cache[f]=rd(f).replace(o,n)
    log.append((r['id'],'OK',[os.path.basename(h[0]) for h in hits]))
if not dry:
    for f,t in cache.items():
        if t!=open(f,encoding='utf8').read(): open(f,'w',encoding='utf8').write(t)
for l in log: print(l)
