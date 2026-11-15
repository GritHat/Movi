"""Tabella prima/dopo (F7r su 20261122 contro F7r-c1 su 20261124). Solo lettura dei due risultati."""
import json
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(QUI, "..", "risultati_f7r_valutazione.json"), encoding="utf-8"))
D = json.load(open(os.path.join(QUI, "risultati_f7r_c1_valutazione.json"), encoding="utf-8"))


def f(x):
    return "-" if x is None else "%d/%d [%.3f; %.3f]" % tuple(x)


def avv(t):
    return [t["intersecano_con_avviso_prima"], t["intersecano"], None, None]


righe = ["| cella | misura | prima F7r (20261122) | dopo c1 (20261124) |", "|---|---|---|---|"]
for c in P:
    p, d = P[c], D[c]
    righe.append("| %s | continuita' | %s | %s |" % (c, f(p["continuita"]), f(d["continuita"])))
    righe.append("| %s | identita' a fine passaggio | %s | %s |" % (c, f(p["identita"]), f(d["identita"])))
    if p["riacq_radar_2s"]:
        righe.append("| %s | riacquisizione radar <= 2 s | %s | %s |" % (c, f(p["riacq_radar_2s"]), f(d["riacq_radar_2s"])))
    if p["intersecano"]:
        a = d["avviso_prima_frammento"]
        righe.append("| %s | avviso prima del frammento a 10 m | %d/%d | %s |" % (c, p["intersecano_con_avviso_prima"], p["intersecano"], f(a)))
    righe.append("| %s | identita' spurie non dichiarate (passaggi) | %s | %s |" % (c, f(p["spuria_non_dich_o_riacq_spuria_passaggi"]), f(d["spurie_non_dichiarate_c1_passaggi"])))
    righe.append("| %s | riacquisizioni spurie dichiarate dubbie o no (passaggi) | %s | %s |" % (c, f(p["riacq_spurie_passaggi"]), f(d["riacq_spurie_passaggi"])))
    righe.append("| %s | falsi eventi/avvisi | %s | %s |" % (c, f(p["falsi_eventi"]), f(d["falso_avviso_passaggi"])))
    righe.append("| %s | «libero» bersaglio / frammento (passaggi) | %d / %d | %d / %d |" % (c, p["libero_bersaglio_passaggi"][0], p["libero_frammento_passaggi"][0], d["libero_bersaglio_passaggi"][0], d["libero_frammento_passaggi"][0]))
print("\n".join(righe))
