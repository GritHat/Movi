"""riconta_manovra.py - copertura al 90 % per tipo di moto sui casi di prova reali (aerei, ala fissa). Wilson per caso (ottimista)."""
import json, math, sys
from collections import Counter
def w(k, n, z=1.96):
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return [k,n,round(p,3),round((c-h)/d,3),round((c+h)/d,3)]
out={}
for m in ("aerei_veloci","droni_ala_fissa","multirotori"):
    d=json.load(open(f"{sys.argv[1]}/casi_prova_{m}.json"))
    print(m, Counter(c["tipo"] for c in d["imm"]))
    for f in ("cv","imm"):
        for t in sorted(set(c["tipo"] for c in d[f])):
            for a,b in ((1,2),(3,5),(6,10),(11,20),(21,30)):
                cs=[c for c in d[f] if c["tipo"]==t and a-0.5<=c["tau"]<b+0.5]
                if len(cs)>=5: out[f"{m}/{f}/{t}/{a}-{b}s"]=w(sum(c[f]["u"]<=0.9 for c in cs),len(cs))
json.dump(out,open(sys.argv[2],"w"),indent=1)
for k,v in out.items():
    if "rettilineo" not in k: print(k,v)
