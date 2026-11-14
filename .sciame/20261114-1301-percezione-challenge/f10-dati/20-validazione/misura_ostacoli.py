#!/usr/bin/env python3
"""Misura 5 — ostacoli per scena (simulato): per ogni ostacolo fisso non strutturale, in quanti fotogrammi c'è una
cella «occupato» entro 15 cm dalla sua impronta; stato delle celle dell'impronta e di quelle subito dietro.
Uso: <python> -I -B misura_ostacoli.py [etichetta] → tabella; funzione `misura(nome, radice)` per chi tara."""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K                                             # noqa: E402
import numpy as np                                             # noqa: E402
from misura_libero import distanza_da_poligono                 # noqa: E402

SCENE = ("cassa_persona", "sospeso_", "scatola15_", "vetro_", "pannello_vuoto")


def misura(nome, radice):
    g = K.leggi_griglie(os.path.join(radice, nome))
    st = g["stati"]
    ver = K.leggi_verita(os.path.join(K.SEQ_SIM, nome))
    az = np.radians(-89.5 + np.arange(180))[:, None]
    rr = (np.arange(30) + 0.5)[None, :] * 0.1
    gx, gz = np.sin(az) * rr, np.cos(az) * rr
    fuori = []
    for o in ver["ostacoli"]:
        if o.get("genere") == "struttura":
            continue
        d = distanza_da_poligono(gx, gz, o["vertici"])
        vicino, impronta = d <= 0.15, d <= 0.0501
        azv = [math.degrees(math.atan2(p[0], p[1])) for p in o["vertici"]]
        rv = [math.hypot(p[0], p[1]) for p in o["vertici"]]
        dietro = (np.degrees(az) >= min(azv)) & (np.degrees(az) <= max(azv)) & (rr > max(rv) + 0.1) & (rr <= max(rv) + 0.6)
        visto = (st[:, vicino] == K.OCCUPATO).any(axis=1)
        conta = lambda m: [int((st[:, m] == s).sum()) for s in range(4)]                   # noqa: E731
        fuori.append({"sequenza": nome, "ostacolo": o["id"], "quota_base_m": o.get("quota_base_m"),
                      "altezza_m": o.get("altezza_m"), "distanza_m": round(min(rv), 2), "fotogrammi": int(st.shape[0]),
                      "fotogrammi_visto_entro_15cm": int(visto.sum()),
                      "impronta_celle_fot [non_oss, libero, occupato, ombra]": conta(impronta),
                      "dietro_celle_fot [non_oss, libero, occupato, ombra]": conta(dietro)})
    return fuori


def main():
    et = sys.argv[1] if len(sys.argv) > 1 else "sim"
    radice = os.path.join(K.USCITE, et)
    tutti = []
    for n in sorted(os.listdir(radice)):
        if os.path.isdir(os.path.join(radice, n)) and any(s in n for s in SCENE):
            tutti += misura(n, radice)
    with open(os.path.join(radice, "misura_ostacoli.json"), "w", encoding="utf-8") as f:
        json.dump(tutti, f, ensure_ascii=False, indent=1)
    print("sequenza; ostacolo; base–cima (m); distanza; visto entro 15 cm (fotogrammi); impronta [non oss., libero, "
          "occupato, ombra] celle·fot; dietro (0,1–0,6 m) [non oss., libero, occupato, ombra]")
    for m in tutti:
        print(f"{m['sequenza']}; {m['ostacolo']}; {m['quota_base_m']}–{(m['quota_base_m'] or 0) + (m['altezza_m'] or 0):.2f}; "
              f"{m['distanza_m']}; {m['fotogrammi_visto_entro_15cm']} su {m['fotogrammi']}; "
              f"{m['impronta_celle_fot [non_oss, libero, occupato, ombra]']}; {m['dietro_celle_fot [non_oss, libero, occupato, ombra]']}")


if __name__ == "__main__":
    main()
