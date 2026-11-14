#!/usr/bin/env python3
"""(d) L'estraneo: la scena A3 dell'avversario di f10 (22-avversario/a234_scene.py, riscritta qui con le stesse
matrici a mano: 848×480, senza rumore, posa esatta) e 11 varianti. A entra da sinistra e si ferma NASCOSTA dietro il
pannello; B, mai vista, è nascosta dall'inizio ed esce a destra. Per ogni configurazione: l'identità di A passa a B?
In quanti fotogrammi A è nascosta e fuori dall'avviso?   Uso: <python> -I -B estraneo.py → risultati/estraneo.json"""
import dataclasses
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prova as P                                              # carica la copia della catena
from catena import Catena                                      # noqa: E402
import scene_a_mano as M                                       # noqa: E402  (della copia: identico a f10)

SC, FPS = M.Scena(), 15.0
PANN = (-0.5, 0.5, 1.8, 1.8)
LIM = 0.5 * 2.3 / 1.8


def scena(x_sosta, k_uscita, v_b, x_b0=0.2, n=56):
    quadri = []
    for k in range(n):
        xa = min(-1.7 + 1.2 * k / FPS, x_sosta)
        xb = x_b0 if k < k_uscita else x_b0 + v_b * (k - k_uscita) / FPS
        f = SC.fotogramma(pannelli=[PANN, (xa - 0.2, xa + 0.2, 2.3, 1.7), (xb - 0.2, xb + 0.2, 2.3, 1.7)])
        quadri.append((f, (xa, 2.3, abs(xa) + 0.2 <= LIM), (xb, 2.3, abs(xb) + 0.2 <= LIM)))
    return quadri


def passa(quadri, par, k_uscita):
    cat = Catena(M.META, par)
    voti, id_a = {}, None
    sbagliata = fuori = nasc = oss_nascosta = 0
    primo_sbaglio = None
    for k, (f, a, b) in enumerate(quadri):
        u = cat.ciclo(k, k / FPS, f)
        vicina = lambda tr, s: tr["misura_nel_ciclo"] and math.hypot(tr["ultima_misura"][0] - s[0], tr["ultima_misura"][1] - s[1]) <= 0.5   # noqa: E731
        if not a[2] and id_a is None:                          # A in vista: l'identità più votata
            for tr in u["tracce"]:
                if tr["stato"] == "osservato" and vicina(tr, a):
                    voti[tr["id"]] = voti.get(tr["id"], 0) + 1
        if a[2]:
            if id_a is None and voti:
                id_a = max(voti, key=voti.get)
            if k >= k_uscita:
                nasc += 1
                c = cat.griglia.cella(a[0], a[1])
                fuori += not (c is not None and cat.possibile_presenza[c])
            for tr in u["tracce"]:
                if tr["id"] == id_a and tr["stato"] == "osservato":
                    oss_nascosta += 1
                    if not b[2] and vicina(tr, b):
                        sbagliata += 1
                        primo_sbaglio = k if primo_sbaglio is None else primo_sbaglio
    return {"id_A": id_a, "identita_di_A_su_B_fotogrammi": sbagliata, "primo_scambio": primo_sbaglio,
            "A_osservato_mentre_nascosta": oss_nascosta, "A_nascosta_dopo_uscita_B": nasc, "A_fuori_avviso": fuori}


def main():
    varianti = [(xs, ku, vb) for xs in (-0.25, -0.1, 0.05) for ku in (24, 32) for vb in (1.2, 0.7)]
    ris = {c: [] for c in P.CONFIG}
    for xs, ku, vb in varianti:
        quadri = scena(xs, ku, vb)
        for c in P.CONFIG:
            r = passa(quadri, dataclasses.replace(P.K.Parametri(), **P.CONFIG[c]), ku)
            r["variante"] = {"x_sosta_A": xs, "fotogramma_uscita_B": ku, "v_B": vb}
            ris[c].append(r)
    os.makedirs(P.RIS, exist_ok=True)
    with open(os.path.join(P.RIS, "estraneo.json"), "w", encoding="utf-8") as f:
        json.dump(ris, f, ensure_ascii=False, indent=1)
    print("conf; varianti con l'identità di A passata a B; fotogrammi A «osservato» mentre è nascosta; A nascosta e fuori dall'avviso (dopo l'uscita di B)")
    for c in ris:
        n = len(ris[c])
        sc = sum(1 for r in ris[c] if r["identita_di_A_su_B_fotogrammi"] > 0)
        print(f"{c}; {sc} su {n}; {sum(r['A_osservato_mentre_nascosta'] for r in ris[c])}; "
              f"{sum(r['A_fuori_avviso'] for r in ris[c])} su {sum(r['A_nascosta_dopo_uscita_B'] for r in ris[c])}")
    r0 = ris["prima"][0]
    print("variante originale A3 (x = -0,25; uscita al fot. 24; 1,2 m/s), conf «prima»:", {k: v for k, v in r0.items() if k != "variante"})


if __name__ == "__main__":
    main()
