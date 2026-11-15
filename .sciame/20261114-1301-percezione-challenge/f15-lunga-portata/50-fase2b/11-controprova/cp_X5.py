"""cp_X5.py - X5 rifatto sul nucleo v2 del prototipo: edificio VERO a 500 m non in pianta, drone dietro a 600 m,
5 passate senza ritorno (l'edificio lo nasconde). Con mappa certificata (come fa movi/lungo.py:74) e senza. Solo conto."""
import sys, json, math
import numpy as np
V2 = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/riuso/lunga_portata_v2"; sys.path.insert(0, V2); import movi_lp_v2 as m
R = m.carica_regole(V2 + "/regole_lunga_portata_v2.json"); par = R["sensori_segnaposto"]["radar_sorveglianza"]
cl = [R["classi"][c] for c in R["scenari"]["sito_droni_rullaggio"]["classi_ammesse"]]
out = {}
for cert in (True, False, None):
    for in_pianta in (False, True):
        s = m.Sensore("radar", [0, 0, 10], par)
        ost = [((500, -20), (500, 20), 40.0)] if in_pianta else []
        g = m.GrigliaPolare(s, 1500, 50, 360, ostacoli=ost, mappa_certificata=cert)
        for k in range(5): g.passata(float(k), rilevamenti=[])
        st = g.stato_punto([600, 0, 10], 4.5, cl)
        out["mappa_certificata=%s, edificio_in_pianta=%s" % (cert, in_pianta)] = str(st)
print(json.dumps(out, indent=1))
