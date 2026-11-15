"""e1_stabile.py - K-709: rifà E1 (collisione fra multirotori lenti, f15 fase 2c, eventi_v3) con l'integratore STABILE
dei frammenti (resistenza semi-implicita di f19-volo/04-scenari/eventi_volo.frammenti_volo), versione vettoriale con
le STESSE estrazioni casuali di eventi_v3.frammenti_vett: cambia solo il passo d'integrazione.
eventi_v3.py è solo importato (nessuna modifica). Uscite in questa cartella.
Uso: python -I -B e1_stabile.py stabile N  |  python -I -B e1_stabile.py euler N   (controllo: deve riprodurre f15)
"""
import json
import math
import os
import sys

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(QUI))
sys.path.insert(0, os.path.join(RADICE, "f15-lunga-portata", "60-fase2c", "01-correzioni"))
import numpy as np  # noqa: E402

import eventi_v3 as EV  # noqa: E402

_euler = EV.frammenti_vett


def frammenti_vett_stabile(ev, rng, t_fine_rel=60.0, dt=0.05):
    n = ev["n_frammenti"]
    p0 = np.asarray(ev["p"], float)
    vc = np.asarray(ev.get("vc", [0, 0, 0]), float)
    w = np.asarray(ev.get("vento", [0, 0, 0]), float)
    u = rng.standard_normal((n, 3))
    u = u / np.linalg.norm(u, axis=1, keepdims=True) * ev["dv_max_m_s"] * rng.random((n, 1)) ** (1 / 3)
    vt = np.exp(rng.uniform(math.log(ev["v_t_m_s"][0]), math.log(ev["v_t_m_s"][1]), n))
    k = (EV.G / vt ** 2)[:, None]
    gv = np.array([0.0, 0.0, -EV.G])
    p, v = np.tile(p0, (n, 1)), vc + u
    T = np.arange(0.0, t_fine_rel + 1e-9, dt)
    P = np.empty((len(T), n, 3))
    P[0] = p
    for i in range(1, len(T)):
        kv = k * np.linalg.norm(v - w, axis=1, keepdims=True) * dt
        v = (v + gv * dt + kv * w) / (1 + kv)             # semi-implicito, come eventi_volo.frammenti_volo
        p = p + v * dt
        terra = p[:, 2] <= 0
        p[terra, 2] = 0.0
        v[terra] = 0.0
        P[i] = p
    return T, P, vt, np.linalg.norm(u, axis=1)


if __name__ == "__main__":
    modo, N = sys.argv[1], int(sys.argv[2])
    i0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    EV.frammenti_vett = frammenti_vett_stabile if modo == "stabile" else _euler
    out = os.path.join(QUI, "e1_%s_%03d.jsonl" % (modo, i0))
    with open(out, "a", encoding="utf-8") as f:
        for i in range(i0, i0 + N):
            try:
                r = EV.passaggio("E1", "alta", i)
                r = {k: r[k] for k in ("scenario", "idx", "evento", "ritardo_evento_s", "falso_evento", "frammenti_dentro_V") if k in r}
            except Exception as e:
                r = {"errore": repr(e)}
            f.write(json.dumps({"lavoro": ["E1", "alta", i], "integratore": modo, **r}, ensure_ascii=False, default=float) + "\n")
            f.flush()
