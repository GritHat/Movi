#!/usr/bin/env python3
"""P10: carico a fasi lunghe. Rifare: timeout 120 python3 sim_selettore_fasi.py > risultati_selettore_fasi.txt"""
import sim_selettore as s

def traccia_fasi(seed, minuti):
    a = s.traccia(seed, minuti, 42.0, 3.0, 2.0, 2.0, 0.015, False)
    return [x + (16.0 if (k // 900) % 2 == 1 else 0.0) for k, x in enumerate(a)]   # 900 cicli = 60 s

if __name__ == "__main__":
    semi, minuti, delta = 20, 10.0, 12.0
    print("# P10: fasi di 60 s, centro 42 / 58 ms alternati, delta 12 ms, bianco 3, AR 2, punte 1,5 %; 20 semi x 10 min")
    print(f"{'variante':<24}{'cambi/min':>10}{'sfor. %':>9}{'sfor./min':>10}{'% in piena':>11}")
    for var in ("A_nessuna_isteresi", "B_isteresi_tempo", "C_due_soglie", "CB_due_soglie+tempo", "D_corretto"):
        C = S = N = P = 0
        for i in range(semi):
            c, sf, n, ip = s.simula(traccia_fasi(1000 + i, minuti), delta, var)
            C += c; S += sf; N += n; P += ip
        print(f"{var:<24}{C/(semi*minuti):>10.1f}{100.0*S/N:>9.2f}{S/(semi*minuti):>10.1f}{100.0*P/N:>11.1f}")
    for nome, d in (("sempre_piena", 0.0), ("sempre_ridotta", delta)):
        S = N = 0
        for i in range(semi):
            tr = traccia_fasi(1000 + i, minuti)
            S += sum(1 for x in tr if x - d > s.PERIODO); N += len(tr)
        print(f"{nome:<24}{0.0:>10.1f}{100.0*S/N:>9.2f}{S/(semi*minuti):>10.1f}{(100.0 if d == 0 else 0.0):>11.1f}")
