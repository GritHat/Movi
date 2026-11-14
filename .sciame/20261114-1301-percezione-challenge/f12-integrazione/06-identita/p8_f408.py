#!/usr/bin/env python3
"""F-408 sulla prova P8 di f10 (sosta di 5 s dietro il pannello, scena a mano senza rumore): dopo il riaggancio, quanto
dista il filtro dalla verità? Stessa scena e stesse funzioni di catena/prove.py. Uso: <python> -I -B p8_f408.py"""
import dataclasses, os, sys
sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prova as P
import numpy as np
import prove as T                                              # della copia (catena/prove.py)

xs = [-1.6 + k / T.FPS for k in range(25)] + [0.0] * 75 + [k / T.FPS for k in range(1, 25)]
occ = T.ProvaOcclusione()
print("conf; fotogrammi dopo la sosta con la traccia «osservato»; di cui con misura tagliata; scarto massimo filtro − verità (m); "
      "identità conservata; eventi di riaggancio")
for conf in ("prima", "f408", "f402", "tutte", "tutte_p"):
    par = dataclasses.replace(P.K.Parametri(), **P.CONFIG[conf])
    catena, esiti, nascosta = occ.passaggio(xs, par)
    ident = T.traccia_vicina(esiti[5][0], xs[5], 2.3)
    fine = max(k for k in range(len(xs)) if nascosta[k])
    sc, tagl = [], 0
    for k, (u, _, _) in enumerate(esiti):
        tr = T.traccia(u, ident)
        if k > fine and tr and tr["stato"] == "osservato" and "x" in tr:
            sc.append(float(np.hypot(tr["x"] - xs[k], tr["z"] - 2.3)))
            tagl += bool(tr["misura_tagliata"])
    ri = [(k, e.get("misura_tagliata")) for k, (u, _, _) in enumerate(esiti) for e in u["eventi"] if e["tipo"] == "riaggancio"]
    print(f"{conf}; {len(sc)}; {tagl}; {max(sc) if sc else float('nan'):.2f}; {T.traccia(esiti[-1][0], ident) is not None}; {ri}")
