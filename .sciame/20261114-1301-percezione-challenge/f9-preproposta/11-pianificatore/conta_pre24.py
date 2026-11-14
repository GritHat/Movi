#!/usr/bin/env python3
"""Conta esatta delle estrazioni in cui il taglio a 24 ore della preproposta (PRE24) sta, modello v2.
Rifare:  timeout 120 python3 conta_pre24.py > risultati_conta_pre24.txt
"""
import random
import piano_mc as pm

rng = random.Random(pm.SEME)
disp = {}
for d in (24, 36, 48):
    lo, moda, hi = pm.ORE_UTILI[d]
    disp[d] = [rng.triangular(lo, hi, moda) - rng.triangular(pm.CHIUSURA[0], pm.CHIUSURA[2], pm.CHIUSURA[1])
               for _ in range(pm.N_ESTRAZIONI)]
print("sensore  N  | stanno su 4000 a 24, 36, 48 ore | rapporto massimo (ore disponibili / ore necessarie) a 48 ore")
for sens in ("posseduto", "nuovo", "assente"):
    piano = pm.costruisci(pm.PRE24, sens)
    ranghi = pm.rango(piano)
    for n in (3, 4, 5):
        ms = [max(pm.calendario(piano, pm.estrai(piano, rng), n, ranghi).values())
              for _ in range(pm.N_ESTRAZIONI)]
        conti = [sum(a >= m for a, m in zip(disp[d], ms)) for d in (24, 36, 48)]
        print(f"{sens:10s} {n} | {conti[0]:4d} {conti[1]:4d} {conti[2]:4d} | "
              f"{max(a / m for a, m in zip(disp[48], ms)):.2f}")
