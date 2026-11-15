"""cp_X.py - controprova (sciame-avversario) degli attacchi X1, X3, X4, X6 sul nucleo v2 COPIATO NEL PROTOTIPO.
Calcoli miei (spostamento vero integrato a passi di 1 ms, non la formula del nucleo). Solo simulazione/conto."""
import sys, json, types
import numpy as np
V2 = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/riuso/lunga_portata_v2"
sys.path.insert(0, V2); import movi_lp_v2 as m
R = m.carica_regole(V2 + "/regole_lunga_portata_v2.json"); out = {}
def spost(tau, v0, vmax, a, dt=1e-3):           # integrazione mia: accelera in linea retta fino a vmax
    x = v = 0.0; v = v0
    for _ in range(int(round(tau/dt))):
        v = min(vmax, v + a*dt); x += v*dt
    return x
for fam in ("sito_droni_rullaggio", "aeroporto_e_droni"):
    cl = R["scenari"][fam]["classi_ammesse"]; inv = m.inviluppo(R, cl)
    tr = types.SimpleNamespace(t_vista=0.0, sigp_ultima=1.0, sigv_ultima=0.3, v_ultima=np.zeros(3), p_ultima=np.zeros(3))
    righe = []
    for (a, vmax, nome) in ((22.0, 45.0, "X1 ATTACCO: 22 m/s2 fino a 45"), (30.0, 45.0, "oltre: 30 m/s2 fino a 45"), (25.0, 60.0, "oltre: 25 m/s2 fino a 60 (FPV)")):
        fuori = []
        for tau in (0.5, 1, 2, 3, 5, 8, 10, 20, 30):
            ip = m.insieme_presenza(tr, tau, R, cl); d = spost(tau, 0.0, vmax, a)
            if d > ip["raggio"]: fuori.append([tau, round(d, 1), round(ip["raggio"], 1)])
        righe.append({"caso": nome, "tau_fuori_[tau,vero,raggio]": fuori})
    out[fam] = {"inviluppo": inv, "X1": righe,
                "X3_distanza_avviso_operatore_di_sito_m": round(float(m.distanza_avviso(R, cl, "operatore_di_sito")), 1),
                "X4_n_eff_5_passate": float(m.n_effettivo(5, inv["rho_passate"]))}
out["X5_mappa_nucleo_predefinita"] = m.MAPPA_CERTIFICATA_PREDEFINITA
out["X5_mappa_nel_prototipo"] = "movi/lungo.py:74 imposta MAPPA_CERTIFICATA_PREDEFINITA = True"
tutte = set(R["classi"]); out["X6_classi_ne_ammesse_ne_escluse"] = {f: sorted(tutte - set(s["classi_ammesse"]) - set(s.get("classi_escluse", []))) for f, s in R["scenari"].items()}
print(json.dumps(out, indent=1, default=float))
