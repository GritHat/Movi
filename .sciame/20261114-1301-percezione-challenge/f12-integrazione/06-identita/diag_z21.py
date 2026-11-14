#!/usr/bin/env python3
"""Il passaggio a 2,1 m (k = 100, 424 px) fotogramma per fotogramma con «tutte_p», e i punti per cella del ponte.
Uso: <python> -I -B diag_z21.py [conf] [da] [a]"""
import dataclasses, os, sys
import numpy as np
np.set_printoptions(linewidth=250)
sys.argv, argv = sys.argv[:1], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prova as P
from catena import Catena
conf = argv[0] if argv else "tutte_p"
da, a = (int(argv[1]), int(argv[2])) if len(argv) > 2 else (0, 99)
lav = {"tipo": "a12z", "profilo": "d435i", "livello": "nominale", "k": 100, "larghezza": 424, "z_attore": 2.1}
meta, tempi, quadri, ver = P.genera(P.spec_di(lav), 424)
cat = Catena(meta, dataclasses.replace(P.K.Parametri(), **P.CONFIG[conf]))
for k, (t, f) in enumerate(zip(tempi, quadri)):
    u = cat.ciclo(k, t, f)
    s = ver["fotogrammi"][k]["soggetti"][0]
    if da <= k <= a:
        gr = [(round(g["x"], 2), round(g["z"], 2), round(g["larghezza_m"], 2), g["celle"], g["punti"], "T" if g["tagliato"] else "") for g in u["gruppi"]]
        tr = [(x["id"], x["stato"][:5], round(x["ultima_misura"][0], 2), round(x["ultima_misura"][1], 2), "m" if x["misura_nel_ciclo"] else "-") for x in u["tracce"] if x["stato"] != "in_conferma"]
        ev = [{k_: v for k_, v in e.items() if k_ in ("tipo", "id", "motivo")} for e in u["eventi"] if e["tipo"] != "nascita"]
        print(f"k={k} vero=({s['x']:+.2f},{s['z']:.2f}) vis={s['frazione_visibile']:.2f} gruppi {gr} tracce {tr} eventi {ev}")
        if 0.3 < s["frazione_visibile"] < 0.75:
            c = cat.griglia.cella(s["x"], s["z"])
            print("   n_ostacolo attorno (righe = azimut, colonne = anelli 16…23):")
            print(cat.mappa_ciclo.n_ostacolo[c[0] - 5:c[0] + 6, 16:24])
