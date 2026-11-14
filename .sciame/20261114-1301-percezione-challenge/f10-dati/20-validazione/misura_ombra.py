#!/usr/bin/env python3
"""Misura 2 — errore del bordo della maschera d'ombra del pannello, per lato (simulato; verità: spigoli del pannello).

Per ogni fotogramma senza soggetto visibile (frazione visibile < 0,02): le colonne d'azimut contigue allo 0° il cui
primo «occupato» sta fra 1,6 e 2,1 m sono «il pannello visto dalla catena». Errore per lato = (bordo stimato −
spigolo vero), in cm a 2,4 m; POSITIVO = ombra stimata più larga della vera. Unità: la sequenza.
In più: celle «libero» in celle del tutto fuori da ciò che la verità dice osservabile (classe 2) e loro distanza
dalla cella osservabile più vicina; differenze fra le coppie con e senza i filtri del costruttore.
Uso: <python> -I -B misura_ombra.py [etichetta]"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K                                             # noqa: E402
import numpy as np                                             # noqa: E402

R_RIF = 2.4


def bordi(stati_k):
    occ = stati_k == K.OCCUPATO
    primo = np.where(occ.any(axis=1), occ.argmax(axis=1), 99)
    pann = (primo >= 16) & (primo <= 20)
    if not pann[89] and not pann[90]:
        return None
    a = 89 if pann[89] else 90
    lo = a
    while lo - 1 >= 0 and pann[lo - 1]:
        lo -= 1
    hi = a
    while hi + 1 < 180 and pann[hi + 1]:
        hi += 1
    return -90.0 + lo, -90.0 + hi + 1.0


def main():
    et = sys.argv[1] if len(sys.argv) > 1 else "sim"
    radice = os.path.join(K.USCITE, et)
    nomi = sorted(n for n in os.listdir(radice) if os.path.isdir(os.path.join(radice, n)) and "__pannello_" in n)
    fuori = []
    for n in nomi:
        g = K.leggi_griglie(os.path.join(radice, n))
        ver = K.leggi_verita(os.path.join(K.SEQ_SIM, n))
        pan = [o for o in ver["ostacoli"] if o["id"] == "pannello"][0]
        vx = [p[0] for p in pan["vertici"]]
        vz = [p[1] for p in pan["vertici"]]
        azv = [math.degrees(math.atan2(x, z)) for x, z in zip(vx, vz)]
        vero_sx, vero_dx = min(azv), max(azv)
        es, ed, senza = [], [], 0
        for k, f in enumerate(ver["fotogrammi"][:g["stati"].shape[0]]):
            if any(s["frazione_visibile"] >= 0.02 for s in f["soggetti"]):
                continue
            b = bordi(g["stati"][k])
            if b is None:
                senza += 1
                continue
            es.append((vero_sx - b[0]) * math.pi / 180 * R_RIF * 100)
            ed.append((b[1] - vero_dx) * math.pi / 180 * R_RIF * 100)
        if not es:
            continue
        q = lambda v: [float(np.percentile(v, p)) for p in (0, 5, 50, 95, 100)]            # noqa: E731
        fuori.append({"nome": n, "fotogrammi": len(es), "pannello_non_visto": senza, "sinistra_cm": q(es),
                      "destra_cm": q(ed)})
    with open(os.path.join(radice, "misura_ombra.json"), "w", encoding="utf-8") as f:
        json.dump(fuori, f, indent=1)
    gruppi = {}
    for m in fuori:
        p = m["nome"].split("__")
        chiave = p[0] + ("__filtri" if m["nome"].endswith("__filtri") else "")
        gruppi.setdefault(chiave, []).append(m)
    print("profilo; N sequenze; fotogrammi; lato; min dei minimi; mediana dei 5°; mediana delle mediane; mediana dei "
          "95°; max dei massimi (cm a 2,4 m; + = stimata più larga); sequenze con 5°–95° entro ±20 cm; entro ±10 cm; "
          "con almeno un fotogramma sotto −10 cm")
    for ch, ms in sorted(gruppi.items()):
        for lato in ("sinistra_cm", "destra_cm"):
            a = np.array([m[lato] for m in ms])
            ok20 = int(((a[:, 1] >= -20) & (a[:, 3] <= 20)).sum())
            ok10 = int(((a[:, 1] >= -10) & (a[:, 3] <= 10)).sum())
            neg = int((a[:, 0] < -10).sum())
            print(f"{ch}; {len(ms)}; {sum(m['fotogrammi'] for m in ms)}; {lato[:-3]}; {a[:, 0].min():+.1f}; "
                  f"{np.median(a[:, 1]):+.1f}; {np.median(a[:, 2]):+.1f}; {np.median(a[:, 3]):+.1f}; {a[:, 4].max():+.1f}; "
                  f"{K.quota(ok20, len(ms))}; {ok10} su {len(ms)}; {neg}")
    print("pannello non visto dalla catena (fotogrammi senza soggetto):", sum(m["pannello_non_visto"] for m in fuori))

    # --- «libero» in celle che la verità dice del tutto non osservabili (classe 2): quanto lontano dall'osservabile?
    print("\n«libero» su celle tutte di classe 2 (non osservabili per la verità): sequenza; celle·fotogramma; "
          "per fotogramma; distanza massima (in celle) dalla cella osservabile più vicina; anello minimo–massimo")
    for n in ("d455_nom__pavimento_vuoto", "d435i_nom__pavimento_vuoto", "g335_nom__pavimento_vuoto",
              "d435i_lim__pavimento_vuoto", "d435i_nom__pavimento_lucido", "d435i_nom__pannello_vuoto",
              "d435i_lim__pannello_vuoto"):
        if not os.path.isdir(os.path.join(radice, n)):
            continue
        st = K.leggi_griglie(os.path.join(radice, n))["stati"]
        ver = K.leggi_verita(os.path.join(K.SEQ_SIM, n))
        _, _, _, cl = K.classi_polari(ver)
        t2 = (cl == 2).all(axis=2)
        oss = (cl == 0).any(axis=2)
        ia, ir = np.nonzero(oss)
        lib = (st == K.LIBERO) & t2[None]
        kk, aa, rr = np.nonzero(lib)
        dmax = 0
        for a_, r_ in set(zip(aa.tolist(), rr.tolist())):
            dmax = max(dmax, int(np.min(np.maximum(np.abs(ia - a_), np.abs(ir - r_)))))
        print(f"{n}; {int(lib.sum())}; {lib.sum() / st.shape[0]:.1f}; {dmax}; "
              f"{(int(rr.min()), int(rr.max())) if len(rr) else '—'}")

    # --- coppie con e senza filtri
    print("\ncoppie filtri accesi / spenti: sequenza; celle·fotogramma diverse; «libero» con i filtri dove senza è "
          "«non osservato»; il contrario; «occupato» solo con i filtri; solo senza")
    for n in nomi + ["d435i_nom__pavimento_vuoto__filtri"]:
        if not n.endswith("__filtri"):
            continue
        a = K.leggi_griglie(os.path.join(radice, n))["stati"]
        b = K.leggi_griglie(os.path.join(radice, n[:-8]))["stati"]
        print(f"{n}; {int((a != b).sum())} su {a.size}; {int(((a == K.LIBERO) & (b == K.NON_OSSERVATO)).sum())}; "
              f"{int(((b == K.LIBERO) & (a == K.NON_OSSERVATO)).sum())}; "
              f"{int(((a == K.OCCUPATO) & (b != K.OCCUPATO)).sum())}; {int(((b == K.OCCUPATO) & (a != K.OCCUPATO)).sum())}")


if __name__ == "__main__":
    main()
