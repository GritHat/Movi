#!/usr/bin/env python3
"""Ablazione dell'ordine dei compiti sul grafo v2 (piano MIN, sensore posseduto).
Rifare:  timeout 120 python3 ablazione.py > risultati_ablazione.txt
(lo script importa piano_mc.py dalla propria cartella: e' codice mio, non materiale scaricato)
"""
import random
import statistics
import piano_mc as pm

ORDINI = {
    "a rango": {},
    "b gradini": dict(pm.CLASSE),
    "c due corsie": {**pm.CLASSE, "N4r": 1, "N5": 1, "C1": 1, "N4": 1},
}

def main():
    rng0 = random.Random(pm.SEME)
    disp = {}
    for d in (24, 36, 48):
        lo, moda, hi = pm.ORE_UTILI[d]
        disp[d] = [rng0.triangular(lo, hi, moda)
                   - rng0.triangular(pm.CHIUSURA[0], pm.CHIUSURA[2], pm.CHIUSURA[1])
                   for _ in range(pm.N_ESTRAZIONI)]
    print(f"# ablazione.py, seme {pm.SEME}, {pm.N_ESTRAZIONI} estrazioni per cella; stesse durate per i tre ordini")
    print("# colonne: mediana / 80-esimo percentile in ore di lavoro a k = 1; k*(80 %) a 24, 36, 48 ore")
    for nome_piano, spec in (("MIN", pm.MIN), ("MED", pm.MED)):
        for sens in ("posseduto", "nuovo", "assente"):
            piano = pm.costruisci(spec, sens)
            ranghi = pm.rango(piano)
            for n in (3, 4, 5):
                rng = random.Random(pm.SEME + n)
                estrazioni = [pm.estrai(piano, rng) for _ in range(pm.N_ESTRAZIONI)]
                for nome, classe in ORDINI.items():
                    pm.CLASSE.clear()
                    pm.CLASSE.update(classe)
                    pt = {t: [] for t, _ in pm.TAPPE}
                    for dur in estrazioni:
                        fine = pm.calendario(piano, dur, n, ranghi)
                        for t, chiavi in pm.TAPPE:
                            ks = list(piano) if chiavi is None else [k for k in chiavi if k in piano]
                            pt[t].append(max(fine[k] for k in ks))
                    print(f"-- {nome_piano}, sensore {sens}, N = {n}, ordine {nome}")
                    for t, _ in pm.TAPPE:
                        ks = [pm.quantile([a / m for a, m in zip(disp[d], pt[t])], 0.20)
                              for d in (24, 36, 48)]
                        print(f"   {t:34s} {statistics.median(pt[t]):5.1f} / {pm.quantile(pt[t], 0.8):5.1f} h"
                              f"   k* {ks[0]:4.2f}  {ks[1]:4.2f}  {ks[2]:4.2f}")

if __name__ == "__main__":
    main()
