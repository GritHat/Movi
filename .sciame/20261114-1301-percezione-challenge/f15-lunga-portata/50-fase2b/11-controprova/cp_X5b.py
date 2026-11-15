"""cp_X5b.py - X5 sul nucleo v2 del prototipo, a distanza dove il 'libero' esiste: per d_bersaglio in 100..1000 m,
edificio vero a d-50 m (alto 40 m) NON in pianta oppure in pianta; 5 passate senza ritorno; stato del punto dietro.
Stati: 0 libero, 1 occupato, 2 in_ombra, 3 non_osservato. Solo conto."""
import sys, json
V2 = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/riuso/lunga_portata_v2"; sys.path.insert(0, V2); import movi_lp_v2 as m
R = m.carica_regole(V2 + "/regole_lunga_portata_v2.json"); par = R["sensori_segnaposto"]["radar_sorveglianza"]
cl = [R["classi"][c] for c in R["scenari"]["sito_droni_rullaggio"]["classi_ammesse"]]
out = {}
for cert in (True, False):
    for d in (75, 125, 175, 275, 475, 975):
        for in_p in (False, True):
            s = m.Sensore("radar", [0, 0, 10], par)
            g = m.GrigliaPolare(s, 1500, 50, 360, ostacoli=[((d-50, -20), (d-50, 20), 40.0)] if in_p else [], mappa_certificata=cert)
            for k in range(5): g.passata(float(k), rilevamenti=[])
            out["cert=%s d=%d in_pianta=%s" % (cert, d, in_p)] = int(g.stato_punto([d, 0, 10], 4.0, cl))
print(json.dumps(out, indent=0))
