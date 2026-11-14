#!/usr/bin/env python3
"""sciame-statistico — controlli brevi sulle tabelle già prodotte (tabelle/sim_*.json, fermi_replica.json,
confronto_profondita.json) e su realsense_stands_still: copertura della regione PER PASSAGGIO, semi sopra la curva
nominale, scarto nel tempo del D435i vero, rapporti vero / simulato. Uso: <python> -I -B controlli_brevi.py"""
import json
import math
import os
import re

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(QUI, "tabelle")


def wil(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f"{100 * max(0, c - h):.1f}–{100 * min(1, c + h):.1f} %"


print("== copertura dell'ellisse al 90 % per passaggio (D435i nominale, a12 / a05 / b) ==")
for et in ("sim", "sim_p40"):
    R = json.load(open(os.path.join(T, f"sim_{et}.json"), encoding="utf-8"))
    P = [p for p in R["passaggi"] if re.search(r"^d435i_nom__pannello_(a12|a05|b)__s\d\d$", p["nome"])]
    tot = 0
    for caso in ("a12", "a05", "b"):
        ps = [p for p in P if f"_{caso}__" in p["nome"]]
        con = [p for p in ps if p["in90"]]
        pieni = sum(1 for p in con if all(p["in90"]))
        tot += pieni
        fuori = [(p["nome"][-3:], round(float(np.mean(p["in90"])), 2), round(max(p["err"]), 2)) for p in con if not all(p["in90"])]
        ult = [p["err"][-1] for p in con]
        ultg = [p["err_grezzo"][-1] for p in con]
        print(f"{et} {caso}: con previsioni {len(con)}/30; verità SEMPRE dentro {pieni}/30 ({wil(pieni, 30)}); fuori (passaggio, "
              f"copertura, errore massimo m): {fuori}; errore all'ultimo fotogramma nascosto: mediana {np.median(ult):.2f}, p90 "
              f"{np.percentile(ult, 90):.2f} m (contro il centro vero: {np.median(ultg):.2f})")
    print(f"{et}: in tutto {tot}/90 ({wil(tot, 90)})")

print("\n== persona ferma, replica: semi con sigma radiale sopra la curva nominale / sopra 1 cm ==")
D = json.load(open(os.path.join(T, "fermi_replica.json"), encoding="utf-8"))
NOM = {2.0: 1.5, 3.0: 3.4, 4.0: 6.0}
for p in (3, 40):
    for d in (2.0, 3.0, 4.0):
        sr = []
        for r in D:
            if r["p"] == p and r["distanza"] == d and len(r["centri"]) >= 30:
                c = np.array(r["centri"])
                ur = np.array([0.3, d]) / math.hypot(0.3, d)
                sr.append(100 * np.std(c[:, :2] @ ur))
        sr = np.array(sr)
        k = int((sr > NOM[d]).sum())
        print(f"soglia {p}, {d} m: sopra la nominale ({NOM[d]} cm) {k}/20 ({wil(k, 20)}); sopra 1 cm {int((sr > 1).sum())}/20; "
              f"valori ordinati: {np.round(np.sort(sr), 2).tolist()}")

d = os.path.join(os.path.dirname(QUI), "12-dati-veri", "sequenze", "realsense_stands_still", "profondita")
a = np.stack([np.load(os.path.join(d, n), allow_pickle=False) for n in sorted(os.listdir(d))[:120]]).astype(np.float64)
ok = (a > 0).all(axis=0)
s, z = a[:, ok].std(axis=0), a[:, ok].mean(axis=0)
zz = np.median(z) / 1000
print(f"\n== realsense_stands_still (D435i vero, 640x360, 120 fotogrammi): pixel sempre validi {ok.mean():.3f}; distanza mediana "
      f"{np.median(z):.0f} mm; scarto tipo nel tempo mediana {np.median(s):.2f} mm, 90° {np.percentile(s, 90):.2f} mm")
for lab, f in (("modello a 848 px", 1.0), ("modello riportato a 640 px", 848 / 640)):
    att = 1000 * 0.6 * 0.003774 * zz * zz * f
    print(f"   {lab}: temporale atteso 0,6·k·z² = {att:.2f} mm; rapporto vero / modello {np.median(s) / att:.2f}")

print("\n== rapporti vero / simulato (D435i nominale e limite, pannello_a12__s00) ==")
C = {o["nome"]: o for o in json.load(open(os.path.join(T, "confronto_profondita.json"), encoding="utf-8"))}
sn, sl = C["d435i_nom__pannello_a12__s00"], C["d435i_lim__pannello_a12__s00"]
for n in ("realsense_stairs", "depthtrack_human02_indoor", "realsense_stands_still", "tum_fr3_walking_static"):
    o = C[n]
    print(f"{n}: validi {100 * o['validi_mediana']:.1f} % contro {100 * sn['validi_mediana']:.1f} (nom) e {100 * sl['validi_mediana']:.1f} (lim): "
          f"{100 * (o['validi_mediana'] - sn['validi_mediana']):+.1f} e {100 * (o['validi_mediana'] - sl['validi_mediana']):+.1f} punti; buchi fra 0,5 e 3 m "
          f"{100 * o['buchi_in_0p5_3m']:.1f} % contro {100 * sn['buchi_in_0p5_3m']:.1f} e {100 * sl['buchi_in_0p5_3m']:.1f} "
          f"(×{o['buchi_in_0p5_3m'] / sn['buchi_in_0p5_3m']:.0f} e ×{o['buchi_in_0p5_3m'] / sl['buchi_in_0p5_3m']:.1f}); pixel della scena fra 0,5 e 3 m "
          f"{100 * o['pixel_in_0p5_3m']:.0f} %")
    for f in ("1.0-2.0", "2.0-3.0"):
        if f in o["rumore"] and f in sn["rumore"] and o["rumore"][f]["sigma_mm"] > 0:
            ro, rs, rl = o["rumore"][f], sn["rumore"][f], sl["rumore"][f]
            an, al = rs["sigma_mm"] * (ro["z_medio"] / rs["z_medio"]) ** 2, rl["sigma_mm"] * (ro["z_medio"] / rl["z_medio"]) ** 2
            print(f"     rumore {f} m: vero {ro['sigma_mm']:.1f} mm a {ro['z_medio']:.2f} m; simulato riportato con z²: nominale {an:.1f}, "
                  f"limite {al:.1f}; rapporto vero / nominale {ro['sigma_mm'] / an:.2f}, vero / limite {ro['sigma_mm'] / al:.2f}")
