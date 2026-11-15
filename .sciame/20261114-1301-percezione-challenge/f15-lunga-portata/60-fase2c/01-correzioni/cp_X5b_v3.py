"""cp_X5b_v3.py - cp_X5b della controprova (11-controprova/cp_X5b.py) rifatto sul PROTOTIPO col nucleo v3 PREDEFINITO:
il nucleo e' preso da movi.lungo.moduli() (quindi con la mappa come la imposta il prototipo), e le griglie sono fatte
con mappa_certificata=None (= il predefinito del nucleo nel prototipo), come in prove_lp._griglia. Edificio vero a
d-50 m (alto 40 m) NON in pianta oppure in pianta; 5 passate senza ritorno; stato del punto dietro.
Stati: 0 libero, 1 occupato, 2 in_ombra, 3 non_osservato. In piu': la riga cert=True (mappa dichiarata dalla scena).
Solo conto. Uso: <venv>/bin/python -I -B cp_X5b_v3.py"""
import json, os, sys
PROTO = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo"
sys.path.insert(0, PROTO); sys.dont_write_bytecode = True
os.environ.pop("MOVI_MAPPA_CERTIFICATA", None); os.environ.pop("MOVI_NUCLEO_LP", None)
from movi import lungo
M = lungo.moduli(); m = M["m"]
R = M["prove"].REG; par = R["sensori_segnaposto"]["radar_sorveglianza"]
cl = [R["classi"][c] for c in R["scenari"]["sito_droni_rullaggio"]["classi_ammesse"]]
out = {"nucleo_prototipo": M["nucleo"], "file_nucleo": m.__file__, "MAPPA_CERTIFICATA_PREDEFINITA": m.MAPPA_CERTIFICATA_PREDEFINITA}
for cert in (None, True):
    for d in (75, 125, 175, 275, 475, 975):
        for in_p in (False, True):
            s = m.Sensore("radar", [0, 0, 10], par)
            g = m.GrigliaPolare(s, 1500, 50, 360, ostacoli=[((d-50, -20), (d-50, 20), 40.0)] if in_p else [], mappa_certificata=cert)
            for k in range(5): g.passata(float(k), rilevamenti=[])
            out["cert=%s d=%d in_pianta=%s" % ("predefinito" if cert is None else cert, d, in_p)] = int(g.stato_punto([d, 0, 10], 4.0, cl))
k = [v for kk, v in out.items() if kk.startswith("cert=predefinito") and "in_pianta=False" in kk]
out["predefinito_non_in_pianta_liberi"] = [sum(x == 0 for x in k), len(k)]
print(json.dumps(out, indent=0))
