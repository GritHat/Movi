#!/usr/bin/env python3
"""Attacco 3 della preproposta: oscillazione del selettore di configurazione.

Modello (IPOTESI, non misura): tempo per ciclo della configurazione piena
  T_piena = centro + deriva AR(1) + rumore bianco + punte rare + salti di carico
  T_ridotta = T_piena - delta
Il selettore vede il tempo per ciclo della configurazione ATTIVA (anello chiuso).
Semplificazione: un ciclo ogni 66,7 ms anche quando sfora (in realta' si salterebbe un fotogramma).

Rifare:  timeout 120 python3 sim_selettore.py > risultati_selettore.txt
"""
import math
import random
import sys

PERIODO = 66.7
HZ = 15.0
DT = 1.0 / HZ


def traccia(seed, minuti, centro, s_bianco, s_ar, tau, p_punta, salti):
    """Tempo per ciclo (ms) della configurazione piena."""
    rnd = random.Random(seed)
    n = int(minuti * 60 * HZ)
    rho = math.exp(-DT / tau)
    k_ar = math.sqrt(1 - rho * rho) * s_ar
    ar = 0.0
    out = []
    salto_fino = -1
    salto_amp = 0.0
    for k in range(n):
        ar = rho * ar + k_ar * rnd.gauss(0, 1)
        t = centro + ar + rnd.gauss(0, s_bianco)
        if salti:
            if k > salto_fino and rnd.random() < DT / 15.0:   # in media uno ogni 15 s
                salto_fino = k + int(rnd.uniform(3, 8) * HZ)
                salto_amp = 8.0 if rnd.random() < 0.5 else -8.0
            if k <= salto_fino:
                t += salto_amp
        if rnd.random() < p_punta:
            t += rnd.uniform(10, 30)
        out.append(max(5.0, t))
    return out


def percentile(v, q):
    s = sorted(v)
    i = min(len(s) - 1, max(0, int(math.ceil(q * len(s))) - 1))
    return s[i]


def simula(tr, delta, variante):
    """Ritorna (cambi, sforamenti, cicli, cicli in piena)."""
    piena = True
    storia = []          # tempi misurati (configurazione attiva)
    ultimo_cambio = -10**9
    cambi = sfor = in_piena = 0
    n = len(tr)
    for k in range(n):
        t = tr[k] if piena else tr[k] - delta
        if t > PERIODO:
            sfor += 1
        if piena:
            in_piena += 1
        storia.append(t)
        nuovo = piena
        da_cambio = k - ultimo_cambio
        if variante in ("A_nessuna_isteresi", "B_isteresi_tempo", "C_due_soglie", "CB_due_soglie+tempo"):
            if k % 8 != 7 or len(storia) < 15:      # selettore a ~2 Hz
                continue
            m = sum(storia[-15:]) / 15.0
            if variante in ("A_nessuna_isteresi", "B_isteresi_tempo"):
                nuovo = not (m > 55.0)
            else:
                if m > 55.0:
                    nuovo = False
                elif m < 45.0:
                    nuovo = True
            if variante in ("B_isteresi_tempo", "CB_due_soglie+tempo") and da_cambio < 38:   # 2,5 s
                nuovo = piena
        elif variante == "D_corretto":
            # discesa rapida: 2 sforamenti negli ultimi 15 cicli, oppure il 2o massimo degli ultimi 30 > 60 ms
            # risalita lenta: 10 s dall'ultimo cambio e 95o percentile degli ultimi 150 + delta certificato < 55 ms
            if len(storia) < 30:
                continue
            if piena:
                if da_cambio >= 15:
                    u15 = storia[-15:]
                    s30 = sorted(storia[-30:])
                    if sum(1 for x in u15 if x > PERIODO) >= 2 or s30[-2] > 60.0:
                        nuovo = False
            else:
                if da_cambio >= 150 and k % 8 == 7:
                    if percentile(storia[-150:], 0.95) + delta < 55.0:
                        nuovo = True
        if nuovo != piena:
            piena = nuovo
            cambi += 1
            ultimo_cambio = k
    return cambi, sfor, n, in_piena


def scenario(nome, centro, delta, s_bianco, s_ar, p_punta, salti, semi=20, minuti=10.0):
    print(f"\n## {nome}: centro {centro} ms, delta {delta} ms, bianco {s_bianco}, AR {s_ar}, punte {p_punta*100:.1f} %, salti {'si' if salti else 'no'}; {semi} semi x {minuti:.0f} min")
    print(f"{'variante':<24}{'cambi/min':>10}{'sfor. %':>9}{'sfor./min':>10}{'% in piena':>11}")
    ris = {}
    for var in ("A_nessuna_isteresi", "B_isteresi_tempo", "C_due_soglie", "CB_due_soglie+tempo", "D_corretto"):
        C = S = N = P = 0
        for s in range(semi):
            tr = traccia(1000 + s, minuti, centro, s_bianco, s_ar, 2.0, p_punta, salti)
            c, sf, n, ip = simula(tr, delta, var)
            C += c; S += sf; N += n; P += ip
        tot_min = semi * minuti
        ris[var] = (C / tot_min, 100.0 * S / N, S / tot_min, 100.0 * P / N)
        print(f"{var:<24}{C/tot_min:>10.1f}{100.0*S/N:>9.2f}{S/tot_min:>10.1f}{100.0*P/N:>11.1f}")
    # riferimenti: sempre piena, sempre ridotta
    for nome_f, d in (("sempre_piena", 0.0), ("sempre_ridotta", delta)):
        S = N = 0
        for s in range(semi):
            tr = traccia(1000 + s, minuti, centro, s_bianco, s_ar, 2.0, p_punta, salti)
            S += sum(1 for x in tr if x - d > PERIODO); N += len(tr)
        print(f"{nome_f:<24}{0.0:>10.1f}{100.0*S/N:>9.2f}{S/(semi*minuti):>10.1f}{(100.0 if d == 0 else 0.0):>11.1f}")
    return ris


if __name__ == "__main__":
    print("# Attacco 3: oscillazione del selettore. Semi 1000..1019. Periodo 66,7 ms; 900 cicli al minuto.")
    print("# Tetti: selettore a 2 Hz -> al piu' 112 cambi/min; con 2,5 s di tempo minimo -> al piu' 24 cambi/min.")
    for d in (5.0, 12.0, 20.0):
        scenario("attacco3_completo", 55.0, d, 3.0, 2.0, 0.015, True)
    scenario("attacco3_solo_rumore", 55.0, 12.0, 3.0, 2.0, 0.0, False)
    for sb in (1.5, 6.0):
        scenario("sensibilita_rumore", 55.0, 12.0, sb, 2.0, 0.015, True)
    scenario("P5_stazionario_media52", 52.0, 12.0, 7.0, 0.0, 0.0, False)
    scenario("P5bis_media50_code", 50.0, 12.0, 4.0, 0.0, 0.04, False)
