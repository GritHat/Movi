#!/usr/bin/env python3
"""Arbitro f9, che-cosa-succede-se: N5 (7 ore probabili, una persona) spezzato in due meta' parallele.
IPOTESI MIA, NON VERIFICATA: che il compito sia divisibile cosi' e che le due meta' costino meta' ciascuna.
Rifare:  PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -B piano_14h_spezzato.py > risultati_piano_14h_spezzato.txt
"""
import random, statistics
import piano_mc as pm
from piano_14h import calendario_tcam, ORE14, DUE_CORSIE

MIN_S = dict(pm.MIN)
del MIN_S["N5 ciclo di vita + cuneo (strato 1)"]
MIN_S["N5a cuneo d'ombra (strato 1) sulla mappa simulata"] = (2.5, 3.5, 7, ["X0b"], False, 3)
MIN_S["N5b ciclo di vita della traccia"] = (2.5, 3.5, 7, ["N4r"], False, 3)
MIN_S["C1 previsione continua a una ipotesi, ritagliata"] = (2, 3, 6, ["N5a", "N5b"], False, 4)
MIN_S["EV registro degli eventi"] = (1, 2, 3, ["N5b"], False, 4)
MIN_S["J1 percezione vera dentro le tracce"] = (2, 3, 6, ["N3r", "N5a", "N5b"], False, 3)

def main():
    rng0 = random.Random(pm.SEME)
    disp = [rng0.triangular(ORE14[0], ORE14[2], ORE14[1]) for _ in range(pm.N_ESTRAZIONI)]
    pm.CLASSE.clear(); pm.CLASSE.update({**DUE_CORSIE, "N5a": 1, "N5b": 1})
    tappe = [(t, (c + ["N5a", "N5b"]) if (c and "N5" in c) else c) for t, c in pm.TAPPE]
    print(f"# piano_14h_spezzato.py, seme {pm.SEME}, {pm.N_ESTRAZIONI} estrazioni; MIN con N5 spezzato in N5a + N5b (ipotesi dell'arbitro, non verificata)")
    print("# colonne: mediana / 80-esimo percentile (ore, k = 1) | P(entro le ore utili) | P(entro 14,0 h) | k*(80 %)")
    piano = pm.costruisci(MIN_S, "assente"); ranghi = pm.rango(piano)
    som = sum(t["p"] for t in piano.values())
    print(f"# somma delle durate probabili {som:.1f} h (piano MIN del pianificatore, sensore assente: {sum(t['p'] for t in pm.costruisci(pm.MIN, 'assente').values()):.1f} h)")
    for n in (3, 4, 5):
        rng = random.Random(pm.SEME + n)
        pt = {t: [] for t, _ in tappe}
        for _ in range(pm.N_ESTRAZIONI):
            dur = pm.estrai(piano, rng)
            fine = calendario_tcam(piano, dur, n, ranghi, 0.0)
            for t, chiavi in tappe:
                ks = list(piano) if chiavi is None else [k for k in chiavi if k in piano]
                pt[t].append(max(fine[k] for k in ks))
        print(f"-- MIN con N5 spezzato, nessun sensore (dati registrati o simulati), N = {n}")
        for t, _ in tappe:
            p_w = sum(1 for a, m in zip(disp, pt[t]) if m <= a) / pm.N_ESTRAZIONI
            p_14 = sum(1 for m in pt[t] if m <= 14.0) / pm.N_ESTRAZIONI
            ks = pm.quantile([a / m for a, m in zip(disp, pt[t])], 0.20)
            print(f"   {t:34s} {statistics.median(pt[t]):5.1f} / {pm.quantile(pt[t], 0.8):5.1f} h | {100*p_w:5.1f} % | {100*p_14:5.1f} % | k* {ks:4.2f}")

if __name__ == "__main__":
    main()
