#!/usr/bin/env python3
"""sciame-statistico — statistiche della profondità: simulatore contro registrazioni vere, con lo stesso codice.

Legge i fotogrammi .npy (allow_pickle=False; millimetri, 0 = senza dato) di 11-simulatore/sequenze e
12-dati-veri/sequenze. Per sequenza, sui primi N fotogrammi (60):
  validi          quota mediana di pixel validi per fotogramma
  mai / interm.   pixel mai validi / validi solo in parte dei fotogrammi (persistenza dei buchi)
  rumore(z)       stima robusta del rumore temporale: 1,4826·mediana|d_t − d_{t−1}|/√2 sui pixel validi in due
                  fotogrammi consecutivi, per fascia di distanza (regge il moto di pochi pixel; NON regge una camera
                  che si muove: allora è un limite superiore)
  buchi di bordo  per riga, le serie di pixel senza dato chiuse fra due pixel validi: «di bordo» se i due vicini
                  differiscono di più di 0,3 m, «di superficie» altrimenti. Quota di pixel, larghezza mediana riportata a
                  848 px, quota delle serie di bordo col vicino più VICINO a destra (banda d'occlusione stereo a sinistra
                  dell'oggetto vicino)
  banda sinistra  quota di non validi nel 3 % di colonne a sinistra contro il 3 % a destra
Uso: <python> -I -B confronto_profondita.py → tabelle/confronto_profondita.json e una tabella."""
import json
import os
import sys

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
F10 = os.path.dirname(QUI)
SIM = os.path.join(F10, "11-simulatore", "sequenze")
VERE = os.path.join(F10, "12-dati-veri", "sequenze")
N = 60
FASCE = [(0.3, 0.5), (0.5, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)]
ELENCO = [
    (SIM, "d435i_nom__pavimento_vuoto"), (SIM, "d435i_nom__pannello_vuoto"), (SIM, "d435i_nom__pannello_a12__s00"),
    (SIM, "d435i_nom__cassa_persona__s00"), (SIM, "d435i_lim__pannello_vuoto"), (SIM, "d435i_lim__pannello_a12__s00"),
    (SIM, "d455_nom__pannello_a12__s00"), (SIM, "g335_nom__pannello_a12__s00"),
    (SIM, "d435i_nom__pannello_a12__s00__filtri"),
    (VERE, "realsense_stands_still"), (VERE, "realsense_stairs"), (VERE, "depthtrack_human02_indoor"),
    (VERE, "tum_fr3_walking_static"), (VERE, "princeton_child_no1"),
]


def carica(rad, nome):
    d = os.path.join(rad, nome, "profondita")
    nomi = sorted(os.listdir(d))[:N]
    a = np.stack([np.load(os.path.join(d, n), allow_pickle=False) for n in nomi]).astype(np.float32) / 1000.0
    with open(os.path.join(rad, nome, "meta.json"), encoding="utf-8") as f:
        meta = json.load(f)
    return a, meta


def serie(q):
    """Serie di non validi chiuse fra due validi, riga per riga, su un fotogramma (metri, 0 = senza dato)."""
    H, W = q.shape
    bordo_px = sup_px = 0
    larg, vicino_dx = [], 0
    n_bordo = 0
    for r in range(0, H, 2):                      # una riga su due: basta
        v = q[r] > 0
        if not v.any():
            continue
        dv = np.diff(v.astype(np.int8))
        inizi = np.nonzero(dv == -1)[0] + 1        # primo non valido dopo un valido
        fini = np.nonzero(dv == 1)[0]              # ultimo non valido prima di un valido
        for s in inizi:
            j = fini[fini >= s]
            if len(j) == 0:
                break
            e = j[0]
            zl, zr = q[r, s - 1], q[r, e + 1]
            n = e - s + 1
            if abs(zl - zr) > 0.3:
                bordo_px += n
                n_bordo += 1
                larg.append(n)
                vicino_dx += zr < zl
            else:
                sup_px += n
    tot = (H // 2 + H % 2) * W
    return bordo_px / tot, sup_px / tot, larg, vicino_dx, n_bordo


def misura(rad, nome):
    a, meta = carica(rad, nome)
    T, H, W = a.shape
    val = a > 0
    o = {"nome": nome, "vero": rad == VERE, "sensore": meta.get("sensore", "")[:60], "px": f"{W}x{H}", "fotogrammi": T,
         "validi_mediana": float(np.median(val.reshape(T, -1).mean(axis=1))),
         "mai_validi": float((~val.any(axis=0)).mean()), "intermittenti": float((val.any(axis=0) & ~val.all(axis=0)).mean())}
    # buchi entro la portata utile: non validi fra i pixel la cui mediana (sui validi nel tempo) sta fra 0,5 e 3 m
    med = np.where(val.any(axis=0), np.nanmedian(np.where(val, a, np.nan), axis=0), np.nan)
    util = (med >= 0.5) & (med <= 3.0)
    o["pixel_in_0p5_3m"] = float(util.mean())
    o["buchi_in_0p5_3m"] = float((~val[:, util]).mean()) if util.any() else None
    d = np.abs(a[1:] - a[:-1])
    amb = val[1:] & val[:-1]
    zm = 0.5 * (a[1:] + a[:-1])
    rum = {}
    for lo, hi in FASCE:
        m = amb & (zm >= lo) & (zm < hi)
        if m.sum() > 2000:
            dd = d[m]
            rum[f"{lo}-{hi}"] = {"sigma_mm": float(1000 * 1.4826 * np.median(dd) / np.sqrt(2)), "z_medio": float(zm[m].mean()),
                                 "n": int(m.sum()), "sigma_rms_mm_troncata": float(1000 * np.sqrt(np.mean(np.minimum(dd, 0.3) ** 2) / 2))}
    o["rumore"] = rum
    bp, sp, larg, vdx, nb = [], [], [], 0, 0
    for k in range(0, T, 6):
        b, s, l, v, n = serie(a[k])
        bp.append(b)
        sp.append(s)
        larg += l
        vdx += v
        nb += n
    o["buchi_bordo_px"] = float(np.mean(bp))
    o["buchi_superficie_px"] = float(np.mean(sp))
    o["larghezza_bordo_mediana_848"] = float(np.median(larg) * 848 / W) if larg else None
    o["larghezza_bordo_p90_848"] = float(np.percentile(larg, 90) * 848 / W) if larg else None
    o["serie_bordo"] = nb
    o["vicino_a_destra"] = vdx / nb if nb else None
    c = max(1, int(round(0.03 * W)))
    o["non_validi_sinistra"] = float((~val[:, :, :c]).mean())
    o["non_validi_destra"] = float((~val[:, :, -c:]).mean())
    return o


def main():
    R = []
    for rad, nome in ELENCO:
        if os.path.isdir(os.path.join(rad, nome)):
            R.append(misura(rad, nome))
            print(nome, "fatto", file=sys.stderr, flush=True)
    with open(os.path.join(QUI, "tabelle", "confronto_profondita.json"), "w", encoding="utf-8") as f:
        json.dump(R, f, indent=1)
    pc = lambda v: "—" if v is None else f"{100 * v:.1f}"                                   # noqa: E731
    print("sequenza | px | validi % | mai validi % | intermittenti % | buchi fra 0,5 e 3 m % | buchi di bordo % px | di superficie % px | "
          "larghezza bordo mediana (p90) a 848 px | vicino a destra % | non validi sin / des % | rumore temporale mm per fascia (z medio)")
    for o in R:
        rum = "; ".join(f"{k} m: {v['sigma_mm']:.1f} (z {v['z_medio']:.2f})" for k, v in o["rumore"].items())
        lw = "—" if o["larghezza_bordo_mediana_848"] is None else f"{o['larghezza_bordo_mediana_848']:.1f} ({o['larghezza_bordo_p90_848']:.1f})"
        print(f"{'VERO ' if o['vero'] else 'sim  '}{o['nome']} | {o['px']} | {pc(o['validi_mediana'])} | {pc(o['mai_validi'])} | {pc(o['intermittenti'])} | "
              f"{pc(o['buchi_in_0p5_3m'])} | {pc(o['buchi_bordo_px'])} | {pc(o['buchi_superficie_px'])} | {lw} | {pc(o['vicino_a_destra'])} | "
              f"{pc(o['non_validi_sinistra'])} / {pc(o['non_validi_destra'])} | {rum}")


if __name__ == "__main__":
    main()
