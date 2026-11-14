#!/usr/bin/env python3
"""Riconti del lettore critico sul solo testo del PDF (nessun dato del progetto).
Indipendenza: stessa specifica (le formule dell'allegato), codice e autore diversi."""
import math
from math import comb, sqrt, log, exp, erf

def Phi(x): return 0.5*(1+erf(x/sqrt(2)))
def wilson(k,n,z=1.959964):
    p=k/n; c=(p+z*z/(2*n))/(1+z*z/n); h=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n); return c-h,c+h
def binom_cdf(k,n,p): return sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(0,k+1))
def sf(k,n,p): return 1-binom_cdf(k-1,n,p)  # P[X>=k]

print("== Tabella 14, prova singola (Prop. 4.4), v=0,5 m/s, Tw=13/15 s, sigma a 3 m")
Tw=13/15; v=0.5
for nome,s in (("nominale",0.0340),("pessimista",0.09),("severa",0.1125)):
    sd=s*sqrt(2/3); d=v*Tw
    print(f"  {nome}: Pmob={Phi(d/sd-5)+Phi(-d/sd-5):.3f}  v05={5*sd/Tw:.3f} v09={(5+1.2816)*sd/Tw:.3f}")
print("  con Tw=1 s:", [round(Phi(0.5/(s*sqrt(2/3))-5),3) for s in (0.09,0.1125)])
print("  con sigma alla distanza media dei due capi (2,78 m):", [round(Phi(v*Tw/(s*(2.783/3)**2*sqrt(2/3))-5),3) for s in (0.09,0.1125)])

print("== Tabella 22: potenze")
def lower_test(n,p0,p1,a=0.05):  # rifiuta per k<=c
    c=-1
    while binom_cdf(c+1,n,p0)<=a: c+=1
    return c,(binom_cdf(c,n,p1) if c>=0 else 0.0)
def upper_test(n,p0,p1,a=0.05):  # rifiuta per k>=c
    c=n+1
    while c-1>=0 and sf(c-1,n,p0)<=a: c-=1
    return c,(sf(c,n,p1) if c<=n else 0.0)
def primo_e_stabile(test,p0,p1,nmax=420):
    pw=[test(n,p0,p1)[1] for n in range(1,nmax+1)]
    primo=next(i+1 for i,x in enumerate(pw) if x>=0.8)
    stab=max(i+1 for i,x in enumerate(pw) if x<0.8)+1
    return primo,test(primo,p0,p1)[0],stab
for t,p0,p1 in ((lower_test,.9,.8),(upper_test,.8,.9),(lower_test,.9,.85),(upper_test,.85,.9),(upper_test,.9,.95)):
    print("  ",p0,"contro",p1,primo_e_stabile(t,p0,p1))
print("  n=30, 0,90 contro 0,80:",lower_test(30,.9,.8))
print("  0,9^30 =",round(.9**30,4),"; P[>=9 su 10] p=0,8:",round(sf(9,10,.8),4)," p=0,9:",round(sf(9,10,.9),4))
print("  >=82 su 94: livello sotto 0,80",round(sf(82,94,.8),4),"potenza a 0,90",round(sf(82,94,.9),3))
print("  >=262 su 296: livello sotto 0,85",round(sf(262,296,.85),4),"potenza a 0,90",round(sf(262,296,.9),3))
print("  >=96 su 100: Wilson",[round(x,4) for x in wilson(96,100)],"potenza 0,95:",round(sf(96,100,.95),3),"0,97:",round(sf(96,100,.97),3))
print("  >=87 su 100: livello sotto 0,80",round(sf(87,100,.8),4),"potenza a 0,90",round(sf(87,100,.9),3))
print("  Oss 5.14: P[Bin(30,0,5)<=23]",round(binom_cdf(23,30,.5),4)," P[Bin(30,0,9)<=23]",round(binom_cdf(23,30,.9),4))
print("  N=219, alfa 0,9: P[X>=214]",f"{sf(214,219,.9):.2e}"," P[X<=174]",f"{binom_cdf(174,219,.9):.2e}"," P[X>=207]",round(sf(207,219,.9),4))

print("== Beta(k, nc+1-k), 5o percentile (bisezione sulla binomiale)")
def beta_q(k,n,q=0.05):
    # P[U_(k) <= x] = P[Bin(n,x) >= k]
    lo,hi=0.0,1.0
    for _ in range(60):
        m=(lo+hi)/2
        if sf(k,n,m)<q: lo=m
        else: hi=m
    return lo
for nc in (30,100):
    k=math.ceil(0.9*(nc+1)); print("  nc",nc,"k",k,"q05",round(beta_q(k,nc),3))
ok=[nc for nc in range(9,200) if beta_q(math.ceil(0.9*(nc+1)),nc)>0.85]
print("  primo nc con q05>0,85:",ok[0],"; stabilmente da:",max(n for n in range(9,200) if n not in ok)+1)

print("== Wilson di controllo")
for k,n in ((826,879),(942,1045),(2125,2279),(1754,1922),(1222,1265),(666,698),(79,90),(176,180),(174,180),(15,90),(17,5704),(13,4800),(4,9152)):
    a,b=wilson(k,n); print(f"  {k}/{n}: [{a:.4f}; {b:.4f}]")
print("== zero su N (Wilson):",{n:round(3.8415/(n+3.8415)*100,4) for n in (90,131,300,6000,24835)})
print("== fascia: ",round(.40/.355,3),round(.20/.355,3),"; avviso:",[round(2.05/(0.267+0.155+t),3) for t in (1.0,0.3,1.5,1.8)])
print("== somma 8.8 p.9:",1568+2983,"contro 4552;",1584+2968,"contro 4553")
