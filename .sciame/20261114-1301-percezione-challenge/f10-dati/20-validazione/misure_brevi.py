#!/usr/bin/env python3
"""Misure brevi: (a) costo per ciclo sulle simulate; (b) sensore coperto, mezzo coperto, azzeramento progressivo;
(c) THÖR con q = 0,1 su exp3 (a posteriori, fuori dalla regola di taratura). Uso: <python> -I -B misure_brevi.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K
import numpy as np
import banco_thor as B

for et in ("sim", "sim_p40"):
    e = json.load(open(os.path.join(K.USCITE, et, "ELENCO.json")))["sequenze"]
    tutti = []
    for s in e:
        tutti += [r["tempo_ciclo_ms"] for r in K.leggi_righe(os.path.join(K.USCITE, et, s["nome"]))]
    per_seq = [s["tempo_ciclo_ms"]["media"] for s in e]
    peggio = max(e, key=lambda s: s["tempo_ciclo_ms"]["p95"])
    print(f"(a) costo {et}: {len(tutti)} cicli a 424×240; media {np.mean(tutti):.2f} ms; mediana {np.median(tutti):.2f}; "
          f"p95 {np.percentile(tutti, 95):.2f}; p99 {np.percentile(tutti, 99):.2f}; massimo {np.max(tutti):.2f}; cicli oltre 66 ms: "
          f"{int((np.array(tutti) > 66).sum())}; sequenza peggiore {peggio['nome']} (media {peggio['tempo_ciclo_ms']['media']}, "
          f"p95 {peggio['tempo_ciclo_ms']['p95']}); media per sequenza min–max {min(per_seq):.2f}–{max(per_seq):.2f}")

for et in ("sim", "sim_p40"):
    for n in ("d435i_nom__sensore_coperto", "d435i_nom__azzeramento_progressivo", "d435i_nom__sensore_mezzo_coperto"):
        righe = K.leggi_righe(os.path.join(K.USCITE, et, n))
        st = K.leggi_griglie(os.path.join(K.USCITE, et, n))["stati"]
        pv = np.array([r["pixel_validi"] for r in righe])
        lib = np.array([r["celle"]["libero"] for r in righe])
        zero = np.nonzero(pv == 0)[0]
        if "mezzo" in n:
            ver = K.leggi_verita(os.path.join(K.SEQ_SIM, n))
            cop = [k for k, f in enumerate(ver["fotogrammi"]) if f.get("evento", {}).get("copertura")]
            sx = (st[:, :90] == K.LIBERO).sum(axis=(1, 2))
            dx = (st[:, 90:] == K.LIBERO).sum(axis=(1, 2))
            print(f"(b) {et} {n}: coperti {cop[0]}–{cop[-1]}; «libero» a sinistra (azimut < 0) prima {sx[cop[0]-1]}, nei coperti "
                  f"{sx[cop].tolist()}; a destra min {dx[cop].min()}")
            stati_tr = [[t_["stato"] for t_ in righe[k]["tracce"] if t_["stato"] != "in_conferma"] for k in (cop[0], cop[3], cop[-1])]
            print("     stati delle tracce (primo, quarto, ultimo coperto):", [sorted(set(s)) for s in stati_tr])
        else:
            seq = [int(lib[k]) for k in zero]
            print(f"(b) {et} {n}: fotogrammi tutti a zero {len(zero)} (dal {zero[0] if len(zero) else '—'}); «libero» in quelli: {seq[:6]}…; "
                  f"dal 3° in poi max {max(seq[2:]) if len(seq) > 2 else '—'}; pixel validi e «libero» ogni 10 fotogrammi: "
                  f"{[(round(float(pv[k]) / 101760, 2), int(lib[k])) for k in range(0, len(lib), 10)]}")

fin3, n_pre = B.finestre("thor_exp3_run1")
r = B.valuta(fin3, n_pre, 0.1, 0.02, 3)
print("(c) THÖR exp3, q = 0,1 (a posteriori): copertura 90 % a 1/2/3 s",
      [round(float(np.mean([x[f"nucleo_in90_{h}"] for x in r])), 3) for h in (1.0, 2.0, 3.0)],
      "; raggio 95 % mediano", [round(float(np.median([x[f"nucleo_r95_{h}"] for x in r])), 2) for h in (1.0, 2.0, 3.0)])
