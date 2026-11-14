#!/usr/bin/env python3
"""Un passaggio fotogramma per fotogramma con la copia corretta. Uso: diagnosi.py <sequenza su disco> <conf> [da] [a] [json extra]"""
import dataclasses, json, os, sys
sys.argv, argv = sys.argv[:1], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prova as P
K = P.K
nome, conf = argv[0], argv[1]
da, a = int(argv[2]) if len(argv) > 2 else 0, int(argv[3]) if len(argv) > 3 else 999
extra = json.loads(argv[4]) if len(argv) > 4 else {}
cart = os.path.join(K.SEQ_SIM, nome)
ver = K.leggi_verita(cart)
sorg = K.SorgenteCartella(cart)
from catena import Catena
cat = Catena(sorg.meta, dataclasses.replace(K.Parametri(), **dict(P.CONFIG[conf], **extra)))
for k, (i, t, prof) in enumerate(sorg):
    u = cat.ciclo(i, t, prof)
    if not da <= k <= a:
        continue
    s = ver["fotogrammi"][k]["soggetti"][0]
    gr = [(round(g["x"], 2), round(g["z"], 2), round(g["larghezza_m"], 2), g["celle"], g["punti"], "T" if g["tagliato"] else "") for g in u["gruppi"]]
    tr = [(x["id"], x["stato"][:5], round(x["ultima_misura"][0], 2), round(x["ultima_misura"][1], 2), "m" if x["misura_nel_ciclo"] else "-", x["si_muove"]) for x in u["tracce"] if x["stato"] != "in_conferma"]
    ev = [{k_: v for k_, v in e.items() if k_ in ("tipo", "id", "motivo", "misura_tagliata")} for e in u["eventi"] if e["tipo"] not in ("nascita",)]
    print(f"k={k} vero=({s['x']:+.2f},{s['z']:.2f}) vis={s['frazione_visibile']:.2f} pp={int(cat.possibile_presenza.sum())}\n   gruppi {gr}\n   tracce {tr}\n   eventi {ev}")
