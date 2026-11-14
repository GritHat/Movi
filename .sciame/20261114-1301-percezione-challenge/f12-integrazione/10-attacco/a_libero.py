# a_libero.py — attacchi P3 (anello cieco), P4 (barra sottile), P7 (rilascio a occlusore fermo). sciame-avversario, f12.
# Usa la camera, il generatore e le regole di 03-libero (copia in libero_rifatto/, impronta in ris/IMPRONTE.txt): condivido
# quindi con quell'autore il modello di camera ideale e la regola; mio e' solo il caso. Regola provata: PR4 = «nuvole-1».
import sys, os, zlib
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, "libero_rifatto"))
sys.argv = sys.argv[:1]
import numpy as np
from libero import *
from banco_libero import render, fotogramma
NF = 30
cam = camera_ideale()

def prova(nome, scatole, r_ogg, ks=(0.004, 0.010), buchi=(("nessuno", 0.0), ("sparsi 5 %", 0.05))):
    """r_ogg = (r0, r1) indici radiali fra cui sta l'oggetto. Conta, sui 5 settori centrali di 5 gradi:
    settori-fotogramma senza alcuna cella occupata sull'oggetto, e con d (regola dei settori di 03-libero) oltre l'oggetto."""
    for k in ks:
        reg = Regole(cam, k)
        pulita, ID = render(cam, scatole, 15.0, 6.0, True)
        npx = int((ID >= 0).sum())
        NA = reg.NA; c0 = (NA - 5 * (NA // 5)) // 2; nset = NA // 5; mid = nset // 2
        sett = range(mid - 2, mid + 3)
        for bn, sp in buchi:
            rng = np.random.default_rng(zlib.crc32(("avv|%s|%g|%s" % (nome, k, bn)).encode()))
            n = nocc = oltre = 0; occ_az = tot_az = 0; ds = []; libsotto = 0
            for f in range(NF):
                D = fotogramma(pulita, ID, k, rng, (), sp, 0)
                out, qv, occ, omb = reg.tutte(D)
                L = out["PR4"]
                for s in sett:
                    a0 = c0 + 5 * s
                    o = occ[a0:a0 + 5, r_ogg[0]:r_ogg[1]].any()
                    sub = L[a0:a0 + 5, 13:]
                    primo = np.where(sub.all(1), NR - 13, (~sub).argmax(1))
                    d = float(((13 + primo) * DR).min())
                    n += 1; nocc += (not o); oltre += (d > r_ogg[1] * DR + 1e-9); ds.append(d)
                    occ_az += int(occ[a0:a0 + 5, r_ogg[0]:r_ogg[1]].any(1).sum()); tot_az += 5
                    libsotto += int(L[a0:a0 + 5, r_ogg[0]:r_ogg[1]].sum())
            print("%-44s k=%.3f %-10s | pixel dell'oggetto %5d | settori-fot. senza «occupato» sull'oggetto %3d/%d | con d oltre l'oggetto %3d/%d | d mediana %.1f m, min %.1f | azimut con «occupato» %d/%d | celle «libero» alla distanza dell'oggetto %d"
                  % (nome, k, bn, npx, nocc, n, oltre, n, float(np.median(ds)), min(ds), occ_az, tot_az, libsotto))

print("# P3 anello cieco (previsto: 0 occupate; d = 3,0 m in >= 90 %)")
prova("P3 scatola 0,35 m alta a 0,75-1,05 m (prevista)", [(-0.15, 0.15, 0.75, 1.05, 0.0, 0.35)], (7, 11))
print("# notato dopo: varianti di distanza e altezza")
prova("P3b scatola 0,35 m alta a 0,50-0,80 m", [(-0.15, 0.15, 0.50, 0.80, 0.0, 0.35)], (5, 8))
prova("P3c scatola 0,60 m alta a 0,30-0,60 m", [(-0.15, 0.15, 0.30, 0.60, 0.0, 0.60)], (3, 6))
prova("P3d corpo 0,45x0,25, alto 1,0 m, a 0,10-0,30 m (bambino sotto il sensore)", [(-0.225, 0.225, 0.05, 0.30, 0.0, 1.0)], (0, 3))
print("# P4 barra sottile sospesa a 0,8 m, a 2,0 m (previsto: >= 30 % a k 0,010; >= 10 % a k 0,004; >= 30 % coi buchi)")
for sp_cm in (1, 2, 3, 5):
    prova("P4 barra %d cm a quota 0,80 m, a 2,0 m" % sp_cm, [(-1.5, 1.5, 2.0, 2.0 + sp_cm / 100.0, 0.80, 0.80 + sp_cm / 100.0)], (19, 22))
print("# notato dopo: palo verticale sottile (largo 2 cm) a 2,5 m, alto 1 m")
prova("palo 2x2 cm alto 1,0 m a 2,5 m", [(-0.01, 0.01, 2.5, 2.52, 0.0, 1.0)], (24, 27))

# P7: celle di R100 rilasciabili a occlusore fermo (pannello largo 1 m, alto 1,8 m, a 1,8 m; griglia 1 grado x 0,1 m)
reg = Regole(cam, 0.004)
pulita, ID = render(cam, [(-0.5, 0.5, 1.8, 1.85, 0.0, 1.8)], 15.0, 6.0, True)
out, qv, occ, omb = reg.tutte(pulita)
cuneo = omb | occ
ix, iy = np.nonzero(cuneo)
px, py = reg.cx[cuneo], reg.cy[cuneo]
dist = np.sqrt(((reg.cx[..., None] - px) ** 2 + (reg.cy[..., None] - py) ** 2)).min(-1)
R100 = dist <= 0.40
L = out["PR4"]
print("# P7 pannello 1 m a 1,8 m: celle del cuneo %d; celle di R100 %d; celle di R100 «libero» ORA (fascia) %d; di queste oltre 0,40 m dal cuneo (rilasciabili secondo 1.7) %d; celle del cuneo «libero» ORA %d"
      % (int(cuneo.sum()), int(R100.sum()), int((R100 & L).sum()), int((R100 & L & (dist > 0.40)).sum()), int((cuneo & L).sum())))
