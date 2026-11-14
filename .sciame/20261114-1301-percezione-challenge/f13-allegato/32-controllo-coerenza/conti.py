#!/usr/bin/env python3
"""Riconti indipendenti delle cifre di sommario, cap. 1, cap. 8 e conclusioni (solo aritmetica, nessun file altrui)."""
from math import sqrt
z = 1.959964
def wilson(k, n):
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return c-h, c+h
casi = [("copertura peggiore 2 s", 2125, 2279), ("copertura peggiore 3 s", 1754, 1922), ("pannello 1 m a 1 s", 942, 1045),
 ("puntiforme 2 s", 826, 879), ("identita ideale 1", 10711, 10757), ("identita ideale 2", 9228, 9240), ("identita ideale 3", 6772, 6967),
 ("identita 0/90", 0, 90), ("identita 176/180", 176, 180), ("identita 174/180", 174, 180), ("estraneo 19/20", 19, 20),
 ("THOR 1 s 214/219", 214, 219), ("mobile 2000/2000", 2000, 2000), ("pannello mobile 79/90", 79, 90), ("5/90", 5, 90),
 ("libero 0/300", 0, 300), ("libero 0/131", 0, 131), ("continuita 0/6000", 0, 6000), ("puntiforme 0/24835", 0, 24835),
 ("avviso 10/10", 10, 10), ("7/10", 7, 10), ("0/140", 0, 140), ("4/9152", 4, 9152), ("6/10", 6, 10), ("2/10", 2, 10)]
for nome, k, n in casi:
    a, b = wilson(k, n); print(f"{nome:28s} {k}/{n} = {k/n:.4f}  Wilson95 [{a:.4f}; {b:.4f}]")
print("premessa: 928/23402 = %.4f ; 24/23402 = %.4f ; 23402-928 = %d ; 23402-24 = %d" % (928/23402, 24/23402, 23402-928, 23402-24))
print("fascia: 0.40/0.355 = %.3f ; 0.20/0.355 = %.3f ; con corpo r_c=0.225: (0.40-0.225)/0.355 = %.3f" % (0.40/0.355, 0.20/0.355, (0.40-0.225)/0.355))
print("latenza: somma = %.1f ; min/max = %.1f/%.1f ; p95 = %.1f ; con 71 ms = %.1f" % (16.7+95+22+21.3, 95+22+21.3, 95+22+21.3+33.3, 95+22+21.3+0.95*33.3, 16.7+71+22+21.3))
for Tr in (1.0, 0.3, 1.8, 1.5):
    T = 0.267+0.155+Tr; print(f"T_r={Tr}: T_ant={T:.3f}  v coperta={(3-0.95)/T:.3f}  d_serve(1.4)={1.4*T+0.95:.3f}")
T=0.722; print("veicolo: d(0)=%.3f v=%.3f" % (1.0*T+1/3+0.95, (3-(1.0*T+1/3+0.95))/(T+1/1.5)))
T=0.722; print("multirotore: d(0)=%.3f" % (3*T+9/6+0.95)); T=1.922; print("persona: d(0)=%.3f" % (1*T+0.5+0.95))
h=1.2
for s,zo,zp in ((1.70,1.8,2.3),(1.70,1.9,2.3),(1.75,1.9,2.3),(1.70,1.7,2.3)):
    print(f"a_min(s={s}, z_o={zo}, z_p={zp}) = {h+(s-h)*zo/zp:.3f}")
print("13/15 = %.4f ; 0.88/0.8667 = %.3f ; 0.63/0.8667 = %.3f" % (13/15, 0.88/(13/15), 0.63/(13/15)))
