#!/usr/bin/env python3
"""Somma i JSON di prove/misura_corto.py per braccio e caso, con Wilson al 95 %. Uso:
    python -I -B prove/riassumi_misure.py uscite/misure > uscite/misure/RIASSUNTO.txt"""
import collections
import glob
import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from movi.tabellone import wilson          # noqa: E402


def w(k, n):
    if not n:
        return f"{k} su {n}"
    lo, hi = wilson(k, n)
    return f"{k} su {n} ({100 * k / n:.1f} %, Wilson 95 %: {100 * lo:.1f}–{100 * hi:.1f} %)"


def main(cartella):
    per = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(cartella, "*_*_*.json"))):
        r = json.load(open(f))
        per[r["braccio"]].append(r)
    for braccio in ("zona_libero", "zona", "base"):
        R = per.get(braccio, [])
        if not R:
            continue
        print(f"\n=== braccio {braccio}: {len(R)} passaggi ===")
        for caso in ("tutti", "a12", "a05", "b", "c", "d"):
            S = [r for r in R if caso == "tutti" or r["caso"] == caso]
            if not S:
                continue
            tot = lambda c: sum(r[c] for r in S)          # noqa: E731
            print(f"-- {caso} ({len(S)} passaggi, {tot('fotogrammi')} fotogrammi)")
            print(f"  P1 cicli nascosti dopo l'ingresso senza regione né avviso: "
                  f"{w(tot('dopo_ingresso_senza_regione_ne_avviso'), tot('dopo_ingresso'))}")
            print(f"  P2 fotogrammi nascosti senza avviso: {w(tot('nascosti_senza_avviso'), tot('nascosti'))}")
            rit = [r["ritardo_avviso_cicli"] for r in S if r["ritardo_avviso_cicli"] is not None]
            print(f"     ritardo dell'avviso (cicli dal primo nascosto): max {max(rit) if rit else '-'}; "
                  f"passaggi con avviso {len(rit)} su {sum(r['nascosti'] > 0 for r in S)} con persona nascosta")
            print(f"  P3 celle «libero» nell'ombra vera interna: {tot('libero_in_ombra_interna')} su "
                  f"{tot('celle_ombra_interna')} celle·fotogramma; di bordo: {tot('libero_in_ombra_bordo')}")
            for h in ("1", "2", "3"):
                O = [r["orizzonti"][h] for r in S if h in r["orizzonti"]]
                Op = [o for o in O if o["entro_portata"]]
                St = [o for o in O if o["stretta"] is not None]
                print(f"  P4 a {h} s: mostrato {w(sum(o['mostrato'] for o in O), len(O))}; entro 3 m "
                      f"{w(sum(o['mostrato'] for o in Op), len(Op))}; P4b stretta {w(sum(bool(o['stretta']) for o in St), len(St))}")
            if caso in ("a12", "a05", "b"):
                T = [r for r in S if r["tornata_visibile"]]
                ri = [r for r in T if r["riaggancio"]]
                certe = sum(x["identita"] == "certa" for r in S for x in r["riaggancio"])
                print(f"  P5 ritorni con riaggancio «presunta»: {w(len(ri), len(T))}; riagganci «certa»: {certe}; "
                      f"nascite dopo l'ingresso (media): {sum(r['nascite_dopo_ingresso'] for r in T) / max(1, len(T)):.2f}")
            print(f"  P7 avvisi tolti senza guardare: {tot('avvisi_tolti_senza_guardare')}; righe non valide: "
                  f"{tot('righe_non_valide')}")
            tm = sorted(t for r in S for t in r["tempi_ms"])
            print(f"  tempo per ciclo (6 processi insieme, NON vale per P6): mediana {tm[len(tm) // 2]:.1f} ms, "
                  f"p95 {tm[int(0.95 * (len(tm) - 1))]:.1f} ms")


if __name__ == "__main__":
    main(sys.argv[1])
