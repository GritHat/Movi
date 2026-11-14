# a_coperto.py — P10: copertura del sensore e ritorno, regola di 1.9 «regione <- (regione dilatata di v_max*T + fascia) ∩ non osservato».
# Griglia e regole di 03-libero (copia). Persona vista in (-1,2; 2,3), in cammino a 1,0 m/s verso destra; sensore coperto T = 2 s;
# al ritorno la persona e' in (0,8-... no: in (-1,2 + 1,0*T'; 2,3): la provo a ogni istante del ritorno fra 0,6 e 1,8 s (dietro il pannello).
import sys, os
QUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(QUI, "libero_rifatto")); sys.argv = sys.argv[:1]
import numpy as np
from libero import *
from banco_libero import render
cam = camera_ideale(); reg = Regole(cam, 0.004)
pulita, ID = render(cam, [(-0.5, 0.5, 1.8, 1.85, 0.0, 1.8)], 15.0, 6.0, True)
out, qv, occ, omb = reg.tutte(pulita)
lib = out["PR4"]
nv = ~lib & ~occ & ~omb                      # quarto stato: «non osservato»
VMAX, FASCIA = 1.4, 0.40
x0, y0, v = -1.2, 2.3, 1.0
def cella(x, y):
    r = np.hypot(x, y); a = np.degrees(np.arctan2(x, y)) + cam.AZ0
    return int(a), int(r / DR)
print("celle: libero %d, occupato %d, in ombra %d, non osservato %d" % (lib.sum(), occ.sum(), omb.sum(), nv.sum()))
lett = masch = n = 0
for T in np.arange(0.6, 1.81, 0.1):
    x = x0 + v * T
    a, r = cella(x, y0)
    dil = np.hypot(reg.cx - x0, reg.cy - y0) <= VMAX * T + FASCIA          # disco: la regione di partenza e' il punto visto
    R_lett, R_masch = dil & nv, dil & ~lib
    n += 1; lett += bool(R_lett[a, r]); masch += bool(R_masch[a, r])
    print("T=%.1f s persona in (%.2f; %.2f) cella %s stato: %s | nella regione, lettura letterale (∩ non osservato): %s (celle %d) | lettura «non visto libero»: %s (celle %d)"
          % (T, x, y0, (a, r), "in ombra" if omb[a, r] else "occupato" if occ[a, r] else "libero" if lib[a, r] else "non osservato", bool(R_lett[a, r]), R_lett.sum(), bool(R_masch[a, r]), R_masch.sum()))
print("ESITO: persona dentro la regione al ritorno: lettura letterale %d su %d; lettura «non visto libero» %d su %d" % (lett, n, masch, n))
