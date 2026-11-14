#!/usr/bin/env python3
"""Conti miei in forma chiusa (nessuna libreria esterna, nessun file del progetto importato)."""
import math
from statistics import NormalDist
N=NormalDist(); Phi=N.cdf
DT=1/15
def sz(d,c): return {'nom':d*d*0.08/(424*0.05),'pes':0.04*(d/2)**2,'sev':0.05*(d/2)**2}[c]
print("== regola «mobile», prova singola alla finestra massima 13 passi, 0,5 m/s, avvicinamento da 3 m ==")
delta=0.5*13*DT; m=3; ks=5
for c in ('pes','sev'):
    soglia=ks*sz(3.0,c)*math.sqrt(2/m)
    # (A) rumore uguale ai due capi, scarto tipo a 3 m (formula della proposizione alla lettera)
    sdA=sz(3.0,c)*math.sqrt(2/m)
    pA=Phi((delta-soglia)/sdA)+Phi((-delta-soglia)/sdA)
    # (B) soglia a 3 m, fluttuazione con lo scarto tipo al centro delle due medie (2,967 m e 2,533 m)
    d1,d2=3.0-0.5*DT,3.0-0.5*14*DT
    sdB=math.sqrt((sz(d1,c)**2+sz(d2,c)**2)/m)
    pB=Phi((delta-soglia)/sdB)+Phi((-delta-soglia)/sdB)
    print(f" {c}: spostamento {delta:.4f} m; soglia {soglia:.4f} m; (A) sigma_delta {sdA:.4f} -> P = {pA:.4f}; (B) capi a {d1:.3f} e {d2:.3f} m, sigma_delta {sdB:.4f} -> P = {pB:.4f}")
print(" prove nel primo secondo (k = 5..15 con j = 2): ", len(range(5,16)), "; limite usato nel testo: 13")
print("== posa: errore di quota a 3 m con 1 grado ==")
for rho in (2,2.8,3): print(f" rho={rho}: lineare {100*rho*math.radians(1):.2f} cm; rho*tan {100*rho*math.tan(math.radians(1)):.2f} cm")
print("== retta del costo a n_T=152 == ", 0.33+0.30*152)
print("== zero su N: limite superiore di Wilson z^2/(N+z^2) ==")
z2=N.inv_cdf(0.975)**2
for n in (90,131,300,400,6000,24835,20000,140,264): print(f" N={n}: {100*z2/(n+z2):.4f} %  (3/N = {100*3/n:.4f} %)")
print("== +- di 85,85 % e 26,60 % su 2000 ==", 196*math.sqrt(.8585*.1415/2000), 196*math.sqrt(.266*.734/2000))
print("== quote == 928/23402 = %.4f %%, 24/23402 = %.4f %%, 4/9152 = %.4f %%" % (100*928/23402,100*24/23402,100*4/9152))
print("== denominatori dell'avviso == 4324-297-106 =",4324-297-106," 4325-297-106 =",4325-297-106)
