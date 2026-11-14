# diagnosi_f10.py — perche' V18 da' cosi' poco libero sui fotogrammi di f10: che cosa leggono i pixel dell'impronta.
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from libero import *
F10 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "f10-dati"))
out = []
for rel, k, f, posa in (("12-dati-veri/sequenze/tum_fr3_walking_static", 0.004, 360, "fotogramma"),
                        ("11-simulatore/sequenze/d435i_lim__pavimento_vuoto", 0.01, 10, "meta"),
                        ("11-simulatore/sequenze/d435i_lim__pavimento_lucido", 0.01, 10, "meta")):
    d = os.path.join(F10, rel)
    m = json.load(open(os.path.join(d, "meta.json")))
    h, t = m["posa"]["altezza_m"], m["posa"]["inclinazione_gradi"]
    if posa == "fotogramma":
        r = open(os.path.join(d, "posa_per_fotogramma.csv")).read().split("\n")[1 + f].split(",")
        h, t = float(r[1]), float(r[2])
    reg = Regole(Camera(m["larghezza"], m["altezza"], m["fx"], m["fy"], m["cx"], m["cy"], h, t), k)
    D = np.load(os.path.join(d, "profondita", "%06d.npy" % f), allow_pickle=False).astype(float) / 1000.0
    dd = D.ravel()[reg.fp_idx]
    v = dd > 0
    sc = dd[v] - reg.fp_z[v]
    mm = reg.fp_m[v]
    riga = "%s fot. %d (posa %.3f m, %.2f gradi): pixel dell'impronta %d ; validi %.1f %% ; dei validi: sul suolo atteso entro m(z) %.1f %%, piu' vicini (qualcosa sopra il suolo) %.1f %%, piu' lontani %.1f %% ; scarto mediano %.3f m" % (
        rel, f, h, t, len(dd), 100 * v.mean(), 100 * (np.abs(sc) <= mm).mean(), 100 * (sc < -mm).mean(), 100 * (sc > mm).mean(), np.median(sc))
    for (a, b) in ((1.3, 2.0), (2.0, 2.5), (2.5, 3.0)):
        rr = (reg.fp_c % NR + 0.5) * DR
        s = (rr >= a) & (rr < b)
        if s.sum():
            riga += " | %.1f-%.1f m: validi %.0f %%" % (a, b, 100 * (dd[s] > 0).mean())
    out.append(riga)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagnosi_f10.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
