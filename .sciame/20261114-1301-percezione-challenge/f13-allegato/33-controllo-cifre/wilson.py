#!/usr/bin/env python3
"""Ricalcolo indipendente degli intervalli di Wilson stampati nell'allegato (cap. 1, 3, 4, 6, 7, 9, app. B).
Nessuna libreria oltre a quella standard. Ogni voce: (dove, k, n, m, stampato_basso, stampato_alto, unita, nota)
unita: 'f' frazione, '%' percento, 'pm' per mille. None = estremo non stampato.
Regola di confronto: l'estremo stampato coincide se e' l'arrotondamento al piu' vicino OPPURE (solo estremo alto,
regola dichiarata nel cap. 1) l'arrotondamento per eccesso, alle cifre stampate."""
import math
from statistics import NormalDist
def z(m=1): return NormalDist().inv_cdf(1-0.05/(2*m))
def wilson(k,n,zz):
    p=k/n; d=1+zz*zz/n; c=(p+zz*zz/(2*n))/d; h=zz*math.sqrt(p*(1-p)/n+zz*zz/(4*n*n))/d
    return max(0,c-h),min(1,c+h)
def dec(s): return len(s.split('.')[1]) if '.' in s else 0
V=[
# capitolo 1
("c1 libero cella 0/300",0,300,1,"0","1.3","%"),
("c1 libero ombra 0/131",0,131,1,"0","2.9","%"),
("c1 continuita 0/24835",0,24835,1,"0","0.016","%"),
("c1 continuita 0/6000 (6,4 su 10000)",0,6000,1,None,"0.064","%"),
("c1 copertura 2125/2279",2125,2279,1,"0.921",None,"f"),
("c1 copertura 1754/1922",1754,1922,1,"0.899",None,"f"),
("c1 G1 942/1045",942,1045,1,"0.882",None,"f"),
("c1 G1 942/1045 m=5 ('0,87')",942,1045,5,"0.87",None,"f"),
("c1 826/879",826,879,1,"0.922",None,"f"),
("c1/5/8/9 avviso 10/10",10,10,1,"72","100","%"),
("c1 id 10711/10757",10711,10757,1,"0.994",None,"f"),
("c1 id 9228/9240",9228,9240,1,"0.998",None,"f"),
("c1 id 6772/6967",6772,6967,1,"0.968",None,"f"),
("c1/6 id 0/90",0,90,1,"0","4.1","%"),
("c1/4/6 id 176/180",176,180,1,"94","99","%"),
("c1/4/6 id 174/180",174,180,1,"93","98","%"),
("c1 thor 214/219 (0,977)",214,219,1,"0.948","0.990","f"),
("c1/6 mobile 2000/2000",2000,2000,1,"99.81",None,"%"),
("c1/4/6 pannello 79/90",79,90,1,"79.4","93.0","%"),
# capitolo 3
("c3 830/897",830,897,1,"90.6","94.1","%"),
("c3 132/134",132,134,1,"94.7","99.6","%"),
("c3 44/87",44,87,1,"40.3","60.8","%"),
("c3 0/321",0,321,1,"0","1.18","%"),
("c3 0/900",0,900,1,"0","0.43","%"),
# capitolo 4
("c4 5/90",5,90,1,"2.4","12.4","%"),
("c4/6 7/10",7,10,1,"40","89","%"),
("c4/6 45/60",45,60,1,"63","84","%"),
("c4 41/45",41,45,1,"79.3","96.5","%"),
("c4/6 2/10",2,10,1,"6","51","%"),
("c4/6 6/10",6,10,1,"31","83","%"),
("c4/6 2400/2400",2400,2400,1,"99.84","100","%"),
("c4/6/8/9 19/20",19,20,1,"76","99","%"),
# capitolo 6
("c6/B 826/879 4 cifre",826,879,1,"0.9220","0.9536","f"),
("c6 90/100 m=1",90,100,1,"0.826","0.945","f"),
("c6 90/100 m=12",90,100,12,"0.782","0.958","f"),
("c6 oss 283/339",283,339,1,"0.792","0.871","f"),
("c6 oss 226/282",226,282,1,"0.751","0.844","f"),
("c6 sic 1/5704 (<0,99 per mille)",1,5704,1,None,"0.99","pm"),
("c6 sic 17/5704",17,5704,1,"1.9","4.8","pm"),
("c6 sic 0/14400",0,14400,1,"0","0.027","%"),
("c6 sic 13/4800",13,4800,1,"0.16","0.46","%"),
("c6 sic 15/90",15,90,1,"10.4","25.7","%"),
("c6 cont 1958/1958",1958,1958,1,"99.8","100","%"),
("c6 cont 1991/2000",1991,2000,1,"99.1","99.8","%"),
("c6 cont 1999/2000",1999,2000,1,"99.7","100","%"),
("c6 cont 0/13638",0,13638,1,"0","0.028","%"),
("c6 cont 0/5600",0,5600,1,"0","0.069","%"),
("c6 cont 0/5597",0,5597,1,"0","0.069","%"),
("c6 soglie 826/879",826,879,1,"0.922","0.954","f"),
("c6 soglie 826/879 z45",826,879,45,"0.908",None,"f"),
("c6 soglie 461/513",461,513,1,"0.869","0.922","f"),
("c6 soglie 437/472",437,472,1,"0.899","0.946","f"),
("c6 soglie 711/774",711,774,1,"0.897","0.936","f"),
("c6 soglie 1222/1265",1222,1265,1,"0.955",None,"f"),
("c6 soglie 1222/1265 z30",1222,1265,30,"0.946",None,"f"),
("c6 soglie 666/698",666,698,1,"0.936",None,"f"),
("c6 soglie 666/698 z30",666,698,30,"0.922",None,"f"),
("c6 soglie 2125/2279 z30",2125,2279,30,"0.914",None,"f"),
("c6 soglie 1754/1922 z30",1754,1922,30,"0.890",None,"f"),
("c6 soglie 942/1045 z5",942,1045,5,"0.875",None,"f"),
("c6 soglie 1257/1388",1257,1388,1,"0.889",None,"f"),
("c6 soglie 845/984",845,984,1,"0.836",None,"f"),
("c6 fuori 174/221",174,221,1,"0.729","0.836","f"),
("c6 fuori 36/46",36,46,1,"0.64","0.88","f"),
("c6 fuori 83/90",83,90,1,"0.85","0.96","f"),
("c6 id 400/400",400,400,1,"99.05","100","%"),
("c6 id 0/10",0,10,1,"0","28","%"),
("c6 id 1/10",1,10,1,"2","40","%"),
("c6 id 3027/3041",3027,3041,1,"0.992","0.997","f"),
("c6 id 3493/3616",3493,3616,1,"0.960","0.971","f"),
("c6 id 3239/3546",3239,3546,1,"0.904","0.922","f"),
("c6 id 12/12",12,12,1,"76","100","%"),
("c6 id 0/264",0,264,1,"0","1.4","%"),
("c6 mob 0/400",0,400,1,"0","0.95","%"),
("c6 mob 0/140",0,140,1,"0","2.7","%"),
("c6 mob 0/60",0,60,1,"0","6","%"),
# capitolo 7
("c7 4/9152",4,9152,1,"0.02","0.11","%"),
]
import sys
EXTRA=[]
if len(sys.argv)>1:
    for l in open(sys.argv[1],encoding='utf8'):
        l=l.strip()
        if l and not l.startswith('#'):
            a=l.split('|'); EXTRA.append((a[0],int(a[1]),int(a[2]),int(a[3]),a[4] if a[4]!='-' else None,a[5] if a[5]!='-' else None,a[6]))
print(f"z1={z(1):.6f} z5={z(5):.4f} z12={z(12):.4f} z30={z(30):.4f} z45={z(45):.4f} z60={z(60):.4f}")
bad=0;tot=0
for (w,k,n,m,lo,hi,u) in V+EXTRA:
    a,b=wilson(k,n,z(m)); f={'f':1,'%':100,'pm':1000}[u]; a*=f; b*=f
    esiti=[]
    for nome,val,st in (("basso",a,lo),("alto",b,hi)):
        if st is None: continue
        tot+=1; d=dec(st); q=10**d
        vicino=round(val*q)/q; ecc=math.ceil(val*q-1e-9)/q
        ok=abs(vicino-float(st))<1e-9 or (nome=="alto" and abs(ecc-float(st))<1e-9)
        if not ok: bad+=1
        esiti.append(f"{nome}: calcolato {val:.5f} stampato {st} {'ok' if ok else 'NON TORNA'}")
    print(f"{w:38s} k={k} n={n} m={m} [{u}] "+"; ".join(esiti))
print(f"estremi confrontati: {tot}; non tornano: {bad}")
