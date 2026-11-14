#!/usr/bin/env python3
"""esp9-P8 (S7 = stessa grandezza di S6), esp9-P9 (diluizione della probabilita'), esp9-P10 (costo).
Numeri del nucleo (SOLUZIONE_V2 B1,B4): Kalman a velocita' quasi costante, T=1/15 s, q=0,2 m^2/s^3,
rumore del centro a 2 m: 1,5 cm (nominale) / 4 (pessimista) / 5 (torneo); aggiungo 20 cm come «dato cattivo».
Uso: python3 p8_p9_p10.py   (seme fisso)"""
import math, random, timeit
random.seed(20261114)
# ---------- P8: identita' ----------
mx=0.0
for _ in range(10000):
    x,z=random.uniform(-3,3),random.uniform(0.3,3); vx,vz=random.uniform(-2.5,2.5),random.uniform(-2.5,2.5)
    r2=x*x+z*z; v=math.hypot(vx,vz)
    if v<1e-3: continue
    cross=x*vz-z*vx
    thdot=abs(cross)/r2                      # |velocita' angolare del rilevamento|
    dline=abs(cross)/v                       # distanza della retta di moto dal punto di osservazione
    mx=max(mx,abs(thdot-dline*v/r2)/max(thdot,1e-12))
print(f"P8a identita' |theta_punto| = d_retta*|v|/r^2: scarto relativo massimo su 10000 stati = {mx:.2e}")
print("P8b controesempio: sensore in (0,0); punto protetto (varco) in x=1,0 m; oggetto da (1,0; 3,0) con v=(0; -1,2) m/s, cioe' DRITTO sul varco")
for z in (3.0,2.5,2.0,1.5):
    x=1.0; vx,vz=0.0,-1.2
    th_s=abs(x*vz-z*vx)/(x*x+z*z)            # visto dal sensore
    xr,zr=x-1.0,z-0.0
    th_p=abs(xr*vz-zr*vx)/(xr*xr+zr*zr)      # visto dal punto protetto
    print(f"   z={z:.1f} m: velocita' angolare vista dal sensore {math.degrees(th_s):5.1f} gradi/s; vista dal punto protetto {math.degrees(th_p):4.1f} gradi/s")
print("P8c una soglia fissa su theta_punto equivale a un raggio protetto che cambia con la distanza (v=1,2 m/s, soglia 5 gradi/s):")
for r in (3.0,2.0,1.5,1.0):
    print(f"   r={r:.1f} m -> d equivalente = {math.radians(5)*r*r/1.2:.2f} m")
# ---------- Kalman stazionario per asse ----------
def staz(q,sig,T=1/15):
    P=[[1.0,0.0],[0.0,1.0]]
    for _ in range(5000):
        # predizione
        a=P[0][0]+2*T*P[0][1]+T*T*P[1][1]+q*T**3/3; b=P[0][1]+T*P[1][1]+q*T*T/2; c=P[1][1]+q*T
        S=a+sig*sig; k0=a/S; k1=b/S
        P=[[a-k0*a, b-k0*b],[b-k1*a, c-k1*b]]
    return P
def sigma_pred(P,q,t):
    return math.sqrt(P[0][0]+2*t*P[0][1]+t*t*P[1][1]+q*t**3/3)
q=0.2; R=0.5
print(f"P9 rotta di collisione esatta (d_CPA=0), volume protetto di raggio {R} m, q={q}")
print("   sigma_mis   sigma_v  | t_CPA: 0,5 s          1,0 s          1,5 s          2,0 s      (sigma di posizione prevista per asse; P_intrusione forma chiusa / Monte Carlo 20000)")
for sig in (0.015,0.04,0.05,0.20):
    P=staz(q,sig); riga=f"   {sig:5.3f} m   {math.sqrt(P[1][1]):.3f} m/s |"
    for t in (0.5,1.0,1.5,2.0):
        s=sigma_pred(P,q,t); pc=1-math.exp(-R*R/(2*s*s))
        n=20000; mc=sum(1 for _ in range(n) if math.hypot(random.gauss(0,s),random.gauss(0,s))<=R)/n
        riga+=f"  s={s:.2f} P={pc:.2f}/{mc:.2f}"
    print(riga)
print("   stessa geometria, solo q diverso (sigma_mis 0,05): P_intrusione a 2 s")
for qq in (0.05,0.2,0.5,1.0):
    P=staz(qq,0.05); s=sigma_pred(P,qq,2.0); print(f"     q={qq}: sigma={s:.2f} m  P={1-math.exp(-R*R/(2*s*s)):.2f}")
print("   prova alternativa «l'ellisse al 95 % (raggio 2,45 sigma) tocca il volume»: d_CPA - 2,45*sigma <= R")
P=staz(q,0.05)
for t in (0.5,1.0,1.5,2.0):
    s=sigma_pred(P,q,t)
    print(f"     t_CPA={t} s: sigma={s:.2f} m; scatta per ogni d_CPA <= {R+2.45*s:.2f} m (rotta di collisione: sempre; passaggio a 1,5 m di lato: {'scatta (falso allarme)' if 1.5<=R+2.45*s else 'non scatta'})")
print("   orizzonte oltre il quale la rotta di collisione esatta ha P_intrusione < 0,5 (sigma_mis 0,05):", end=' ')
t=0.0
while True:
    t+=0.01; s=sigma_pred(P,q,t)
    if 1-math.exp(-R*R/(2*s*s))<0.5: print(f"{t:.2f} s (sigma={s:.2f} m)"); break
# ---------- P6: distanza protettiva ----------
print("P6 distanza protettiva (forma lineare di Marvel e Norcross, macchina ferma: S = vH*(TR+TS) + C + ZS), vH=1,6 m/s, ZS=0,10 m")
for nome,TR,TS,C in (("chiede a una persona: latenza 0,155 + reazione umana 1,0 s; C=0,85",1.155,0.0,0.85),("idem, C=0",1.155,0.0,0.0),
                     ("arresto automatico: latenza 0,155 + arresto 0,3 s; C=0,85",0.155,0.3,0.85),("idem, C=0",0.155,0.3,0.0)):
    print(f"   {nome}: S = {1.6*(TR+TS)+C+0.10:.2f} m")
print("   velocita' massima coperta con portata 3 m, conferma della traccia 4 fotogrammi (0,27 s), C=0,85, ZS=0,10: v = (3-0,85-0,10)/(T):", f"persona nel ciclo {2.05/(1.155+0.27):.2f} m/s; arresto automatico {2.05/(0.455+0.27):.2f} m/s")
# ---------- P10: costo ----------
def valuta(x,z,vx,vz,Ppp,Ppv,Pvv,q=0.2,R=0.5):
    v2=vx*vx+vz*vz
    t=max(0.0,-(x*vx+z*vz)/v2) if v2>1e-6 else 0.0
    dx,dz=x+vx*t,z+vz*t; d=math.hypot(dx,dz)
    s=math.sqrt(Ppp+2*t*Ppv+t*t*Pvv+q*t**3/3)
    tocca = d-2.45*s<=R
    r2=x*x+z*z; thdot=(x*vz-z*vx)/r2; rdot=(x*vx+z*vz)/math.sqrt(r2)
    return t,d,s,tocca,thdot,rdot
n=200000
dt=timeit.timeit(lambda: valuta(0.3,2.5,-0.1,-1.2,P[0][0],P[0][1],P[1][1]),number=n)
print(f"P10 costo di S6+S7 per traccia in Python puro: {1e6*dt/n:.2f} microsecondi ({n} chiamate)")
