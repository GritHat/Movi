#!/usr/bin/env python3
"""esp9-P7: la regola S8 «attesa se una cella del corridoio e' non osservata o possibile presenza»
a SCENA VUOTA. Geometria del nucleo (SOLUZIONE_V2 B1,B2,B7): griglia polare 1 grado x 0,1 m,
campo orizzontale 87 gradi, suolo visto da 1,24 m, portata 3 m. Regola dei 3 fotogrammi (C9):
una cella e' «buco» (non osservato) dopo 3 fotogrammi non validi di fila.
Buchi indipendenti per cella e per fotogramma con probabilita' 1-p_valido (ipotesi dichiarata).
Uso: python3 p7_corridoio.py   (seme fisso)"""
import math, random
random.seed(20261114)
HFOV=87.0; R_CIECO=1.24; R_MAX=3.0; DR=0.1; DTH=1.0
def celle_corridoio(larghezza, z0, z1):
    """celle polari (centro) dentro il rettangolo |x|<=larghezza/2, z0<=z<=z1 (sensore in origine, asse z avanti)"""
    out=[]
    nth=int(180/DTH); nr=int(round(3.5/DR))
    for it in range(nth):
        th=-90+DTH*(it+0.5)
        for ir in range(nr):
            r=DR*(ir+0.5)
            x=r*math.sin(math.radians(th)); z=r*math.cos(math.radians(th))
            if abs(x)<=larghezza/2 and z0<=z<=z1: out.append((th,r))
    return out
def stato_strutturale(th,r):
    if abs(th)>HFOV/2: return 'fuori campo'
    if r<R_CIECO: return 'anello cieco'
    if r>R_MAX: return 'oltre portata'
    return 'osservabile'
print("A) parte strutturale (nessun rumore): quota di celle del corridoio che NON sono osservabili")
for nome,(w,z0,z1) in {'corridoio dal sensore 0-3 m, largo 1 m':(1.0,0.0,3.0),
                       'corridoio 0-3 m, largo 2 m':(2.0,0.0,3.0),
                       'corridoio 1,24-3 m (distanza lungo l\'asse), largo 1 m':(1.0,1.24,3.0),
                       'corridoio 1,3-2,9 m, largo 1 m':(1.0,1.3,2.9),
                       'corridoio 1,3-2,9 m, largo 2 m':(2.0,1.3,2.9),
                       'corridoio 1,5-2,8 m, largo 2,4 m':(2.4,1.5,2.8)}.items():
    c=celle_corridoio(w,z0,z1); cnt={}
    for th,r in c: cnt[stato_strutturale(th,r)]=cnt.get(stato_strutturale(th,r),0)+1
    non=len(c)-cnt.get('osservabile',0)
    print(f"  {nome}: celle {len(c)}, non osservabili {non} ({100*non/len(c):.1f} %) {cnt} -> attesa permanente: {'SI' if non>0 else 'no'}")
print("B) parte casuale: corridoio tutto osservabile (1,3-2,9 m, largo 1 m), scena vuota, 15 Hz")
c=[x for x in celle_corridoio(1.0,1.3,2.9) if stato_strutturale(*x)=='osservabile']; N=len(c)
print(f"  celle: {N}")
for pv in (0.99,0.95,0.80):
    ph=(1-pv)**3
    teor=1-(1-ph)**N
    cicli=9000  # 10 minuti a 15 Hz
    for regola,soglia_celle,persist in (('S8 alla lettera: 1 cella',1,1),('>=1 cella per 3 cicli di fila',1,3),('>=2 % delle celle',max(1,math.ceil(0.02*N)),1),('>=2 % delle celle per 3 cicli',max(1,math.ceil(0.02*N)),3)):
        inval=[0]*N; att=0; fronti=0; run=0; prec=False
        for t in range(cicli):
            buchi=0
            for i in range(N):
                if random.random()<pv: inval[i]=0
                else: inval[i]+=1
                if inval[i]>=3: buchi+=1
            run = run+1 if buchi>=soglia_celle else 0
            a = run>=persist
            att+=a
            if a and not prec: fronti+=1
            prec=a
        print(f"  suolo valido {pv}: {regola:32s} cicli in attesa {100*att/cicli:6.2f} %  ingressi in attesa {fronti/10:.1f}/min" + (f"  (teoria 1 cella: {100*teor:.2f} %)" if soglia_celle==1 and persist==1 else ""))
