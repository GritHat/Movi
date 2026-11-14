#!/usr/bin/env python3
"""A1 — la catena con una posa sbagliata di e gradi (il simulatore e la catena condividono la posa esatta di meta.json).
Uso: <python> -I -B a1_posa.py"""
import dataclasses
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import av_comune as A                                          # noqa: E402
import numpy as np                                             # noqa: E402
from catena import Catena                                      # noqa: E402
from geometria import posa_da_normale                          # noqa: E402
from parametri import IN_OMBRA, LIBERO, NON_OSSERVATO, OCCUPATO, Parametri   # noqa: E402
from sorgente import SorgenteCartella                          # noqa: E402
import scene_a_mano as M                                       # noqa: E402

NOMI = {NON_OSSERVATO: "non_oss", LIBERO: "LIBERO", OCCUPATO: "occupato", IN_OMBRA: "ombra"}


def posa(h, gradi):
    t = math.radians(gradi)
    return posa_da_normale(h, [0.0, -math.cos(t), -math.sin(t)], nota=f"imposta: {h} m, {gradi}°")


def celle_impronta(cat, x0, x1, z0, z1):
    s = set()
    for x in np.linspace(x0, x1, 7):
        for z in np.linspace(z0, z1, 7):
            c = cat.griglia.cella(float(x), float(z))
            if c:
                s.add(c)
    return sorted(s)


def corri(sorgente, e, dh=0.0, impronta=None):
    meta = sorgente.meta
    cat = Catena(meta, Parametri(), posa=posa(meta["posa"]["altezza_m"] + dh, meta["posa"]["inclinazione_gradi"] + e))
    lib, occ, conf, imp_lib, imp_stati = [], [], set(), 0, []
    n = 0
    for i, t, f in sorgente:
        u = cat.ciclo(i, t, f)
        n += 1
        lib.append(u["celle"]["libero"])
        occ.append(u["celle"]["occupato"])
        conf.update(tr["id"] for tr in u["tracce"] if tr["stato"] != "in_conferma")
        if impronta:
            cs = celle_impronta(cat, *impronta)
            st = [int(cat.mappa_ciclo.stati[c]) for c in cs]
            imp_lib += int(any(s == LIBERO for s in st))
            imp_stati.append(st)
    return {"n": n, "libero": float(np.mean(lib)), "occupato": float(np.mean(occ)), "tracce": len(conf),
            "impronta_libero_fotogrammi": imp_lib, "impronta_ultimo": imp_stati[-1] if imp_stati else None,
            "celle": celle_impronta(cat, *impronta) if impronta else None}


def main():
    print("== A1a/b: d435i_nom__pavimento_vuoto, inclinazione creduta = 15° + e ==")
    print("e (gradi); dh (cm); libero medio; occupato medio; tracce confermate")
    base = None
    for e, dh in ((0, 0), (0.5, 0), (-0.5, 0), (1, 0), (-1, 0), (2, 0), (-2, 0), (3, 0), (-3, 0), (0, 0.03), (0, -0.03)):
        r = corri(SorgenteCartella(os.path.join(A.SEQ_SIM, "d435i_nom__pavimento_vuoto")), e, dh)
        base = base or r["libero"]
        print(f"{e:+.1f}; {100 * dh:+.0f}; {r['libero']:.0f} ({100 * r['libero'] / base:.0f} % di e=0); {r['occupato']:.0f}; {r['tracce']}  (N={r['n']} fot.)")
    print("\n== A1c: d435i_nom__scatola15_2p0m (scatola 15 cm, x ±0,075, z 2,00–2,15) ==")
    print("e; fotogrammi con almeno una cella dell'impronta «libero»; stati dell'impronta all'ultimo fotogramma; libero medio; occupato medio")
    for e in (0, 1, 2, 2.5, 3, 3.5, 4):
        r = corri(SorgenteCartella(os.path.join(A.SEQ_SIM, "d435i_nom__scatola15_2p0m")), e, impronta=(-0.075, 0.075, 2.0, 2.15))
        print(f"{e:+.1f}; {r['impronta_libero_fotogrammi']} su {r['n']}; celle {r['celle']} → {[NOMI[s] for s in r['impronta_ultimo']]}; "
              f"{r['libero']:.0f}; {r['occupato']:.0f}")
    print("\n== A1d: scena a mano 848×480 senza rumore, gradino/scatola alta H a z = 2,55 m, largo 0,30 m ==")
    print("H (cm); e; stati delle celle del fronte (x ±0,14, z 2,55); celle libere totali; stato del suolo accanto (x=0,6 z=2,55)")
    sc = M.Scena()
    from sorgente import SorgenteMemoria
    for H in (0.10, 0.12, 0.15):
        for e in (0, 0.5, 1.0, 1.5, 2.0, 2.5):
            f = sc.fotogramma(pannelli=[(-0.15, 0.15, 2.55, H)])
            src = SorgenteMemoria(M.META, M.tempi(4), [f] * 4)
            cat = Catena(M.META, Parametri(), posa=posa(1.2, 15 + e))
            for i, t, q in src:
                cat.ciclo(i, t, q)
            cs = celle_impronta(cat, -0.14, 0.14, 2.551, 2.559)
            st = [NOMI[int(cat.mappa_ciclo.stati[c])] for c in cs]
            acc = NOMI[int(cat.mappa_ciclo.stati[cat.griglia.cella(0.6, 2.55)])]
            cnt = {k: st.count(k) for k in sorted(set(st))}
            print(f"{100 * H:.0f}; {e:+.1f}; {cnt}; {int((cat.mappa_ciclo.stati == LIBERO).sum())}; {acc}")


if __name__ == "__main__":
    main()
