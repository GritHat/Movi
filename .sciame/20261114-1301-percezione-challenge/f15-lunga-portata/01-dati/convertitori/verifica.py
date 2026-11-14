#!/usr/bin/env python3
"""Controllo del formato comune su tutte le scene: python -I verifica.py <cartella 01-dati>. Condivide con i convertitori solo la specifica del formato."""
import csv, json, os, sys, math, glob
base = sys.argv[1]; tot = 0; err = []; per = {}
for sc in sorted(glob.glob(os.path.join(base, "traiettorie", "*", "*", "scena.json"))):
    d = os.path.dirname(sc); tot += 1
    try:
        s = json.load(open(sc))
        for k in ("nome", "oggetti", "riferimento", "sensori", "ostacoli", "fonte", "licenza"):
            assert k in s, "manca " + k
        cl = s["oggetti"][0]["classe"]; assert cl == os.path.basename(os.path.dirname(d)), "classe diversa dalla cartella"
        per[cl] = per.get(cl, 0) + 1
        r = list(csv.reader(open(os.path.join(d, "verita.csv"))))
        assert r[0] == ["tempo", "id", "x", "y", "z", "vx", "vy", "vz", "vis_rif"], "intestazione"
        assert len(r) - 1 == s["campioni"], "righe diverse da campioni"
        tp = -1.0
        for q in r[1:]:
            v = [float(q[0])] + [float(c) for c in q[2:8]]
            assert all(math.isfinite(c) for c in v), "valore non finito"
            assert v[0] > tp, "tempo non crescente"; tp = v[0]
            assert q[8] in ("0", "1") and q[1] == s["nome"], "id o visibilita'"
    except Exception as e:
        err.append((d, repr(e)))
print("scene", tot, "per classe", per, "errori", len(err)); [print(e) for e in err[:10]]
