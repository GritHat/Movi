"""attacchi.py - controesempi X1-X6 contro movi_lp.py (non modificato). Solo conto e simulazione.
Uso: <venv>/bin/python -I -B attacchi.py  -> stampa e scrive attacchi_esito.json nella cartella di questo file.
"""
import copy, json, math, os, sys, types
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
F15 = os.path.dirname(QUI)
sys.path.insert(0, os.path.join(F15, "04-moto"))
import numpy as np
import movi_lp as m
from scipy.stats import ncx2

REG = m.carica_regole(os.path.join(F15, "04-moto", "regole_lunga_portata.json"))
AER = REG["scenari"]["aeroporto_e_droni"]["classi_ammesse"]
STR = REG["scenari"]["strada"]["classi_ammesse"]
out = {}

def traccia(p, v, sp=5.0, sv=0.5, t=0.0):
    return types.SimpleNamespace(t_vista=t, p_ultima=np.asarray(p, float), v_ultima=np.asarray(v, float), sigp_ultima=sp, sigv_ultima=sv)

def moto(v0, a, vmax, tau):          # distanza percorsa in linea retta accelerando da v0 fino a vmax
    ta = max(0.0, (vmax - v0) / a)
    return v0 * tau + 0.5 * a * tau ** 2 if tau <= ta else v0 * ta + 0.5 * a * ta ** 2 + vmax * (tau - ta)

# X1: drone fermo che scatta (ipotesi: a 20 e 25 m/s2, 45 m/s)
x1 = []
for a in (20.0, 25.0):
    tr = traccia([0, 0, 50], [0, 0, 0], sp=2.0, sv=0.3)
    for tau in (0.5, 1, 2, 3, 5, 8, 10, 15, 30):
        ins = m.insieme_presenza(tr, tau, REG, AER)
        d = moto(0.0, a, 45.0, tau)
        x1.append({"a": a, "tau": tau, "raggio_avviso_m": round(ins["raggio"], 1), "distanza_vera_m": round(d, 1), "fuori": d > ins["raggio"]})
out["X1"] = x1

# X2: aereo in decollo a 160, 205 m/s visto per l'ultima volta a quella velocita'
x2 = []
for v in (160.0, 205.0):
    tr = traccia([0, 0, 300], [v, 0, 0], sp=7.5, sv=2.0)
    for tau in (1, 2, 5, 10, 30):
        ins = m.insieme_presenza(tr, tau, REG, AER)
        x2.append({"v": v, "tau": tau, "raggio_avviso_m": round(ins["raggio"], 1), "distanza_vera_m": v * tau, "fuori": v * tau > ins["raggio"]})
out["X2"] = x2

# X3: distanza d'avviso con v_max aereo corretto (kalman-1: 210 m/s) e portata del 'libero'
rad = m.Sensore("radar", [0, 0, 10], REG["sensori_segnaposto"]["radar_sorveglianza"])
R2 = copy.deepcopy(REG)
R2["classi"]["aereo_linea_avvicinamento"]["v_max"] = 210.0
x3 = {}
for nome, R in (("attuale_90", REG), ("corretto_210", R2)):
    x3[nome] = {p: round(m.distanza_avviso(R, AER, p)) for p in ("operatore_di_sito", "pilota_in_rullaggio", "pilota_remoto_di_drone")}
x3["portata_libero_multirotore_5_passate_m"] = round(rad.portata(0.01, 0.99, 5))
x3["portata_libero_multirotore_1_passata_m"] = round(rad.portata(0.01, 0.99, 1))
x3["finestra_W_aereo_210_cella100_s"] = 100 / 210.0
out["X3"] = x3

# X4: fluttuazione correlata fra passate. Pd con SNR istantaneo s fissato: ncx2.sf(2*eta, 2, 2s), eta = -ln Pfa.
par = REG["sensori_segnaposto"]["radar_sorveglianza"]
eta = -math.log(par["pfa"])
r = rad.portata(0.01, 0.99, 5)
S = rad.snr_rif * (0.01 / par["rcs_rif_m2"]) * (par["r_rif_m"] / r) ** 4
rng = np.random.default_rng(20261115)
s = rng.exponential(S, 400000)
pd_s = ncx2.sf(2 * eta, 2, 2 * s)
x4 = {"distanza_m": round(r), "SNR_medio": round(S, 2), "Pd_swerling1_formula": round(par["pfa"] ** (1 / (1 + S)), 4),
      "Pd_media_montecarlo": round(float(pd_s.mean()), 4)}
for n in (1, 2, 3, 5):
    x4["mancate_%d_indipendenti" % n] = round((1 - par["pfa"] ** (1 / (1 + S))) ** n, 4)
    x4["mancate_%d_correlate" % n] = round(float(np.mean((1 - pd_s) ** n)), 4)
out["X4"] = x4

# X5: edificio non in pianta. Griglia senza ostacoli, 5 passate senza ritorno: lo stato nella cella del mezzo nascosto.
cls_aer = [dict(REG["classi"][c]) for c in AER]
p_mezzo = np.array([600.0, 0.0, 10.0])
x5 = {}
for nome, ost in (("edificio_non_in_pianta", ()), ("edificio_in_pianta", (((400.0, -50.0), (400.0, 50.0), 30.0),))):
    g = m.GrigliaPolare(rad, 3000.0, 100.0, 360, ostacoli=ost)
    for k in range(5):
        g.passata(float(k))
    x5[nome] = m.NOMI_STATO[g.stato_punto(p_mezzo, 4.0, cls_aer)]
# variante: auto (10 m2) ferma dietro, classi della strada
cls_str = [dict(REG["classi"][c]) for c in STR]
g = m.GrigliaPolare(rad, 3000.0, 100.0, 360)
for k in range(5):
    g.passata(float(k))
x5["auto_dietro_edificio_non_in_pianta_strada"] = m.NOMI_STATO[g.stato_punto(np.array([800.0, 0, 1.0]), 4.0, cls_str)]
out["X5"] = x5

# X6: classe non ammessa. 'libero' per le classi dello scenario ma Pd cumulata < 0,99 per un pedone / un drone C0.
def conta(classi_scen, intruso, r_max=12000.0):
    g = m.GrigliaPolare(rad, r_max, 100.0, 360)
    for k in range(5):
        g.passata(float(k))
    st = g.stati(4.0, classi_scen)
    pc = g.pd_cumulata(4.0, intruso)
    lib = st == m.LIBERO
    bad = lib & (pc < 0.99)
    rr = g.dist[bad]
    return {"celle_libere": int(lib.sum()), "libere_ma_non_verificate_per_intruso": int(bad.sum()),
            "distanza_min_m": float(rr.min()) if rr.size else None, "pd_cum_min_intruso_su_libere": float(pc[lib].min()) if lib.any() else None}
out["X6"] = {"strada_pedone_0.5m2": conta(cls_str, {"rcs_m2": 0.5, "v_max": 2.5}),
             "strada_drone_0.01m2": conta(cls_str, {"rcs_m2": 0.01, "v_max": 19.0}),
             "aeroporto_drone_C0_1.6e-4m2": conta(cls_aer, {"rcs_m2": 1.6e-4, "v_max": 19.0})}

json.dump(out, open(os.path.join(QUI, "attacchi_esito.json"), "w"), ensure_ascii=False, indent=1, default=float)
print(json.dumps(out, ensure_ascii=False, indent=1, default=float))
