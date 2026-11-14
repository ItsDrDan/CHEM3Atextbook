import json,sys,re,collections,os
B=json.load(open(sys.argv[1])); C=json.load(open(os.path.join(os.path.dirname(__file__),'calc_ch01.json')))
T={'ch01-method','ch01-classify','ch01-states','ch01-charge','ch01-change','ch01-density','ch01-units','ch01-sigfig','ch01-convert'}
err=[]
ids=[q['id'] for q in B]
if len(set(ids))!=len(ids): err.append('dup ids')
if ids!=['c1-%03d'%i for i in range(1,len(B)+1)]: err.append('ids not sequential')
for q in B:
    i=q['id']
    if q.get('t') not in T: err.append(i+' bad t')
    if len(q.get('c',[]))!=4: err.append(i+' c!=4')
    if len(q.get('y',[]))!=4: err.append(i+' y!=4')
    if any(not str(y).strip() for y in q.get('y',[])): err.append(i+' empty y')
    if len(set(re.sub(r'\s+',' ',c).strip().lower() for c in q['c']))!=4: err.append(i+' dup choice')
    for k in ('q','h','w'):
        if not str(q.get(k,'')).strip(): err.append(i+' empty '+k)
    if q.get('d') not in (1,2,3): err.append(i+' bad d')
    if q.get('k') not in (0,1): err.append(i+' bad k')
    if re.search(r'all of the above|none of the above',json.dumps(q),re.I): err.append(i+' AOTA/NOTA')
    # balanced simple tags
    s=' '.join([q['q'],q['h'],q['w']]+q['c']+q['y'])
    for tg in ('sub','sup','b','i'):
        if len(re.findall('<%s>'%tg,s))!=len(re.findall('</%s>'%tg,s)): err.append(i+' unbalanced <%s>'%tg)
    if re.search(r'&(?!(?:[a-z]+|#\d+);)',s): err.append(i+' bare &')
    for f in q.get('f',[]):
        if f['type']=='particles':
            for b in f['boxes']:
                for m in b['mols']:
                    for a in m:
                        if a not in f['key']: err.append(i+' atom not in key '+a)
# numeric density checks
def r3(x):
    from math import log10,floor
    return float('%.3g'%x)
for c in C:
    q=next(x for x in B if x['id']==c['id']); m,V=c['m'],c['V']; d=m/V
    ok=abs(r3(d)-float(c['ans']))<1e-9
    print(c['id'],'m/V=%.5f'%d,'->',r3(d),'claimed',c['ans'],'OK' if ok else 'MISMATCH')
    if not ok: err.append(c['id']+' density mismatch')
    if c['ans'] not in re.sub('<[^>]+>','',q['c'][0]+' '+q['y'][0]+' '+q['w']): err.append(c['id']+' answer not stated')
    for w,how in c['wrong'].items():
        val={'V/m':V/m,'m*V':m*V,'m/V/10':d/10,'m/35.0':m/35.0,'m/20.0':m/20.0,'units':d}[how]
        good=abs(r3(val)-float(w.split()[0]))<1e-9 and any(w in x for x in q['c'][1:])
        print('   distractor',w,'=',how,'%.4g'%val,'OK' if good else 'BAD')
        if not good: err.append(c['id']+' distractor '+w)
# other numbers in text
# lead id: nearest listed density
lst={'Aluminum':2.70,'Steel':7.9,'Lead':11.3,'Gold':19.3}; print('c1-057 nearest metal:',min(lst,key=lambda k:abs(lst[k]-56.5/5.00)))
dc=4.60/5.00; print('c1-059 cap',dc,'floats in water' if dc<1.00 else 'sinks in water','/','floats in ethanol' if dc<0.789 else 'sinks in ethanol')
print('c1-060 layers top->bottom:',sorted({'Mineral oil':0.85,'water':1.00,'honey':1.42}.items(),key=lambda x:x[1]))
print('c1-062 wax halves:',(20.0)/(40.0/0.900/2))
cnt=collections.Counter(q['t'] for q in B)
print(dict(cnt)); print('with figures:',sum(1 for q in B if q.get('f')))
print('ERRORS:',err if err else 'none')
