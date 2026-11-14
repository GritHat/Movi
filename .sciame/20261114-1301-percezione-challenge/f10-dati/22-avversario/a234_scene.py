#!/usr/bin/env python3
"""A2, A3, A4 — matrici di profondità scritte a mano (848×480, senza rumore, posa esatta) passate nella catena.
Uso: <python> -I -B a234_scene.py"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import av_comune as A                                          # noqa: E402
import numpy as np                                             # noqa: E402
from catena import Catena                                      # noqa: E402
from mappa import InvarianteViolato                            # noqa: E402
from parametri import IN_OMBRA, LIBERO, NON_OSSERVATO, OCCUPATO, Parametri   # noqa: E402
import scene_a_mano as M                                       # noqa: E402

NOMI = {NON_OSSERVATO: "non_oss", LIBERO: "LIBERO", OCCUPATO: "occupato", IN_OMBRA: "ombra"}
SC = M.Scena()
FPS = 15.0


def senza_ritorno(pannelli_veri, pannelli_muti):
    """I pannelli «muti» nascondono ciò che sta dietro ma i loro pixel escono a 0 (nessun dato)."""
    con = SC.fotogramma(pannelli=list(pannelli_veri) + list(pannelli_muti))
    senza = SC.fotogramma(pannelli=list(pannelli_veri))
    solo = SC.fotogramma(pannelli=list(pannelli_muti))
    muto = (con == solo) & (con != senza)             # pixel in cui la superficie più vicina è un pannello muto
    f = con.copy()
    f[muto] = 0
    return f


def celle_di(cat, x0, x1, z0, z1, n=9):
    s = set()
    for x in np.linspace(x0, x1, n):
        for z in np.linspace(z0, z1, n):
            c = cat.griglia.cella(float(x), float(z))
            if c:
                s.add(c)
    return sorted(s)


def a2():
    print("== A2a: palo largo 3 cm, alto 1,5 m, a z = 2,05 m, pixel a 0 (nessun ritorno); 6 fotogrammi ==")
    cat = Catena(M.META, Parametri())
    f = senza_ritorno([], [(-0.015, 0.015, 2.05, 1.5)])
    print("pixel a 0 del palo:", int((f == 0).sum() - (SC.fotogramma() == 0).sum()))
    for k in range(6):
        u = cat.ciclo(k, k / FPS, f)
        cs = celle_di(cat, -0.015, 0.015, 2.05, 2.05)
        print(f"  fot. {k}: celle del piede {cs} → {[NOMI[int(cat.mappa_ciclo.stati[c])] for c in cs]}; occupato {u['celle']['occupato']}, "
              f"in ombra {u['celle']['in_ombra']}, tracce {len(u['tracce'])}")
    print("== A2b: lastra 0,4 × 1,7 m a z = 2,0 m senza ritorno che compare al fotogramma 3 ==")
    cat = Catena(M.META, Parametri())
    vuoto = SC.fotogramma()
    lastra = senza_ritorno([], [(-0.2, 0.2, 2.0, 1.7)])
    for k in range(8):
        u = cat.ciclo(k, k / FPS, vuoto if k < 3 else lastra)
        imp = celle_di(cat, -0.19, 0.19, 2.01, 2.09)           # impronta (fronte della lastra)
        dietro = celle_di(cat, -0.15, 0.15, 2.2, 2.9)          # ombra vera dietro la lastra
        si = [NOMI[int(cat.mappa_ciclo.stati[c])] for c in imp]
        sd = [NOMI[int(cat.mappa_ciclo.stati[c])] for c in dietro]
        print(f"  fot. {k}: impronta {len(imp)} celle: LIBERO {si.count('LIBERO')}; dietro {len(dietro)} celle: LIBERO {sd.count('LIBERO')}, "
              f"ombra {sd.count('ombra')}, non_oss {sd.count('non_oss')}; tracce {len(u['tracce'])}; possibile presenza {int(cat.possibile_presenza.sum())}")


def passa(nome, fotogrammi, nascosti, par=None):
    """fotogrammi: lista di (matrice, {nome: (x, z, nascosto)}). Stampa gli eventi e lo stato attorno ai soggetti."""
    cat = Catena(M.META, par or Parametri())
    print(f"== {nome} ==")
    fuori = []
    try:
        for k, (f, sogg) in enumerate(fotogrammi):
            u = cat.ciclo(k, k / FPS, f)
            riga = {"k": k, "eventi": u["eventi"], "pp": int(cat.possibile_presenza.sum()), "sogg": {}}
            for n, (x, z, nasc) in sogg.items():
                c = cat.griglia.cella(x, z)
                oss = [tr for tr in u["tracce"] if tr["stato"] == "osservato"]
                riga["sogg"][n] = {"x": x, "nascosto": nasc, "cella": NOMI[int(cat.mappa_ciclo.stati[c])] if c else None,
                                   "in_pp": bool(cat.possibile_presenza[c]) if c else None}
            riga["tracce"] = [(tr["id"], tr["stato"], round(tr["ultima_misura"][0], 2), round(tr["ultima_misura"][1], 2),
                               tr["misura_tagliata"]) for tr in u["tracce"] if tr["stato"] != "in_conferma"]
            fuori.append(riga)
            ev = [e for e in u["eventi"] if e["tipo"] not in ("nascita",)]
            if ev:
                print(f"  fot. {k}: " + "; ".join(str(e) for e in ev))
    except InvarianteViolato as e:
        print("  INVARIANTE VIOLATO:", e)
    return fuori


def a3():
    pann = (-0.5, 0.5, 1.8, 1.8)
    quadri = []
    for k in range(52):
        xa = min(-1.7 + 1.2 * k / FPS, -0.25)                   # A entra da sinistra e si ferma nascosta a x = -0,25
        xb = 0.2 if k < 24 else 0.2 + 1.2 * (k - 24) / FPS      # B è dietro dall'inizio; dal fotogramma 24 esce a destra
        f = SC.fotogramma(pannelli=[pann, (xa - 0.2, xa + 0.2, 2.3, 1.7), (xb - 0.2, xb + 0.2, 2.3, 1.7)])
        lim = 0.5 * 2.3 / 1.8
        quadri.append((f, {"A": (xa, 2.3, abs(xa) + 0.2 <= lim), "B": (xb, 2.3, abs(xb) + 0.2 <= lim)}))
    r = passa("A3: due persone nella stessa ombra (pannello 1 × 1,8 m a 1,8 m; A entra, B esce)", quadri, None)
    id_a = None
    for riga in r:
        if riga["k"] in (10, 20, 23, 27, 28, 29, 30, 31, 32, 36, 40, 45, 51):
            print(f"  fot. {riga['k']}: A x={riga['sogg']['A']['x']:+.2f} nascosta={riga['sogg']['A']['nascosto']} cella={riga['sogg']['A']['cella']} "
                  f"in_possibile_presenza={riga['sogg']['A']['in_pp']} | B x={riga['sogg']['B']['x']:+.2f} nascosta={riga['sogg']['B']['nascosto']} "
                  f"| celle pp={riga['pp']} | tracce {riga['tracce']}")
    # conteggi
    senza_avviso = sum(1 for riga in r if riga["sogg"]["A"]["nascosto"] and riga["k"] >= 24 and not riga["sogg"]["A"]["in_pp"])
    oss_su_b = 0
    for riga in r:
        if riga["k"] >= 24 and riga["sogg"]["A"]["nascosto"]:
            for (i, st, x, z, tg) in riga["tracce"]:
                if i == 2 and st == "osservato":
                    oss_su_b += 1
    print(f"  dopo il fotogramma 24: fotogrammi con A nascosta e fuori dalla possibile presenza: {senza_avviso}; "
          f"fotogrammi con la traccia 2 «osservato» mentre A è nascosta: {oss_su_b} (l'identità di A va letta dagli eventi sopra)")


def a4():
    quadri = []
    for k in range(80):
        xa0 = min(-1.7 + 1.2 * k / FPS, 0.0)                    # A entra e si ferma dietro il centro del pannello (fot. 22)
        s = 0.0 if k < 28 else 0.5 * (k - 28) / FPS             # dal fotogramma 28 pannello e A scorrono a destra a 0,5 m/s
        s = min(s, 1.5)
        xa = xa0 + s
        pann = (-0.5 + s, 0.5 + s, 1.8, 1.8)
        f = SC.fotogramma(pannelli=[pann, (xa - 0.2, xa + 0.2, 2.3, 1.7)])
        lim0, lim1 = (-0.5 + s) * 2.3 / 1.8, (0.5 + s) * 2.3 / 1.8
        quadri.append((f, {"A": (xa, 2.3, (xa - 0.2 >= lim0) and (xa + 0.2 <= lim1))}))
    r = passa("A4: occlusore che si muove (pannello e A scorrono insieme a 0,5 m/s dal fotogramma 28)", quadri, None)
    for riga in r:
        if riga["k"] in (20, 27, 35, 45, 55, 65, 75, 79):
            print(f"  fot. {riga['k']}: A x={riga['sogg']['A']['x']:+.2f} nascosta={riga['sogg']['A']['nascosto']} cella={riga['sogg']['A']['cella']} "
                  f"in_possibile_presenza={riga['sogg']['A']['in_pp']} | celle pp={riga['pp']} | tracce {riga['tracce']}")
    fuori = [riga["k"] for riga in r if riga["sogg"]["A"]["nascosto"] and not riga["sogg"]["A"]["in_pp"]]
    nasc = [riga["k"] for riga in r if riga["sogg"]["A"]["nascosto"]]
    print(f"  A nascosta in {len(nasc)} fotogrammi ({nasc[0]}–{nasc[-1]}); nascosta E fuori dalla possibile presenza in {len(fuori)}"
          + (f" (dal fot. {fuori[0]})" if fuori else ""))
    lib = [riga["k"] for riga in r if riga["sogg"]["A"]["nascosto"] and riga["sogg"]["A"]["cella"] == "LIBERO"]
    print(f"  A nascosta su cella «libero»: {len(lib)} fotogrammi")


if __name__ == "__main__":
    quale = sys.argv[1:] or ["a2", "a3", "a4"]
    for q in quale:
        {"a2": a2, "a3": a3, "a4": a4}[q]()
