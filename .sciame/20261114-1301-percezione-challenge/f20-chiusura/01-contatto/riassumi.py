import json,collections,sys
c=collections.defaultdict(list)
for l in open(sys.argv[1]):
    r=json.loads(l); e,cf,i=r['lavoro'][:3]
    if 'errore' in r: print('ERR',r['lavoro'],r['errore'][:300]); continue
    c[(e,cf)].append((i,r['ritardo_evento_s'],r['falso_evento'],(r.get('innesco_v4c') or {}).get('perche'),r['libero_sul_vero'][0]))
for k,v in sorted(c.items()):
    v.sort(); ok=sum(1 for x in v if x[1] is not None and 0<=x[1]<=2); ok1=sum(1 for x in v if x[1] is not None and 0<=x[1]<=1); fa=sum(x[2] for x in v); pre=sum(1 for x in v if x[1] is not None and x[1]<0)
    print(k,len(v),'entro1',ok1,'entro2',ok,'prima_urto',pre,'falsi',fa,'libero_vero',sum(x[4] for x in v),[x[1] for x in v][:20], dict(collections.Counter(x[3] for x in v)))
