import re,sys,json,urllib.request,urllib.parse,concurrent.futures as cf
urls=[l.strip() for l in open(sys.argv[1]) if l.strip()]
def get(u,method='GET'):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'},method=method),timeout=25)
        return r.status, r.read(400000).decode('utf8','ignore') if method=='GET' else ''
    except urllib.error.HTTPError as e: return e.code,''
    except Exception as e: return str(e)[:60],''
gh=sorted({re.sub(r'[?#].*$','',u) for u in urls if 'itsdrdan.github.io' in u})
other=sorted({u for u in urls if not re.search('youtu|itsdrdan',u)})
vids=set()
for u in urls:
    m=re.search(r'(?:youtu\.be/|embed/|v=)([A-Za-z0-9_-]{11})',u)
    if m: vids.add(m.group(1))
out={}
with cf.ThreadPoolExecutor(12) as ex:
    for u,(c,_) in zip(gh,ex.map(get,gh)): out[u]=c
    for u,(c,_) in zip(other,ex.map(get,other)): out[u]=c
    vl=sorted(vids)
    for v,(c,b) in zip(vl,ex.map(lambda v:get('https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v='+v),vl)):
        out['yt:'+v]=(c, json.loads(b)['title'] if c==200 else '')
json.dump(out,open(sys.argv[2],'w'),indent=1)
bad={k:v for k,v in out.items() if (v if not isinstance(v,tuple) else v[0])!=200}
print(len(gh),'gh',len(other),'other',len(vids),'videos; bad:',len(bad))
for k,v in bad.items(): print(v,k)
