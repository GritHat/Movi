"""scorta_f7.py - scenario F7 «scorta» (sciame-tracciamento, f20-chiusura/05-scorta). VERSIONE NUOVA, file proprio.

MoVi a bordo di un drone portatore (25-35 m/s, profilo deterministico, posa da navigazione inerziale con rumore e
deriva dichiarati, moto proprio compensato con la posa STIMATA) mantiene la traccia di un drone bersaglio 150-300 m
avanti (35-45 m/s, con manovra); a 30-100 m dal portatore due droni collidono: fiammata che satura le camere 0,5-3 s,
fumo 5-20 s, frammenti con la velocita' dei mezzi piu' la dispersione, echi dei frammenti e echi spuri nel radar.

Riuso dichiarato:
 - frammenti_volo(): COPIA testuale della funzione di f19-volo/04-scenari/eventi_volo.py (integratore semi-implicito,
   stabile), qui sotto; il file di fase 3 non e' toccato (copia di riferimento: eventi_volo_f7_copia_origine.py).
 - il nucleo v3i (prove_volo.py + movi_lp_v3) usa griglie polari di sensori FERMI: non si applica a un sensore in moto.
   Qui ne riprendo le REGOLE (mai «libero» sul non osservato; insieme di presenza r0 + dv tau + a tau^2/2; C(tau) che
   non cresce durante la perdita; evento che non sparisce; sensore perso che non torna «affidabile»), non il codice.
   Copia di riferimento: prove_volo_v3i_copia_origine.py. Non tocco il nucleo v4 di un altro agente.
Tutto SIMULATO. Stesso autore di scenario e tracciatore: il controllo non e' indipendente dalla fisica ipotizzata.
Solo osservazione e avviso: nessun comando al portatore, nessun inseguimento.

Uso: python -I -B scorta_f7.py sviluppo|valutazione [processi]      -> passaggi_<fase>.jsonl, risultati_<fase>.json
     python -I -B scorta_f7.py --registro DIR                        -> registro_F7_<variante>.jsonl (sda, idx 0)
"""
import json
import math
import os
import sys

sys.dont_write_bytecode = True
import numpy as np  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
G = 9.81
DT = 0.1
T_FINE = 24.0
T_EV = 6.0
K99 = math.sqrt(11.3449)     # chi2_3 0,99
K90 = math.sqrt(6.2514)      # chi2_3 0,90
GATE = 16.27                 # chi2_3 0,999
PFA_LN = math.log(1e-6)

# ------------------------------------------------------------------ parametri (I = ipotesi; S = da scheda)
CFG = {
    "att": {"radar": {"periodo": 0.2, "az": 60.0, "el": 40.0, "dietro": False, "s_r": 1.5, "s_a": math.radians(1.0),
                      "s_d": 0.3, "r_ref": 800.0, "rcs_ref": 0.01, "falsi": 0.5, "r_max": 1200.0},
            "camera": {"fov": 30.0, "s_a": math.radians(0.05), "r_max": 800.0, "pd": 0.95, "brandeggio": False},
            "nota": "I: radar FMCW piccolo di bordo (5 Hz, +-60 gradi avanti, Pd 0,5 a 800 m per 0,01 m2), camera fissa "
                    "+-30 gradi; nessuna scheda aperta in questo lavoro: classe dichiarata come ipotesi"},
    "sda": {"radar": {"periodo": 0.05, "az": 180.0, "el": 60.0, "dietro": True, "s_r": 1.0, "s_a": math.radians(0.5),
                      "s_d": 0.15, "r_ref": 1400.0, "rcs_ref": 0.01, "falsi": 0.5, "r_max": 2000.0},
            "camera": {"fov": 180.0, "s_a": math.radians(0.02), "r_max": 2000.0, "pd": 0.97, "brandeggio": True},
            "nota": "I: radar a scansione elettronica 20 Hz, 4 pannelli (360 gradi), 0,5 gradi (classe EchoShield da "
                    "parametri_volo.json, scheda NON APERTA), EO/IR raffreddato su brandeggio puntato sul bersaglio"},
}
INS = {"s_p0": 0.5, "s_b": 0.02, "s_rw": 0.05, "s_att0": math.radians(0.1), "s_om": math.radians(0.005),
       "nota": "I: errore di posizione 0,5 m + deriva 0,02 m/s + passeggiata 0,05 m/sqrt(s); assetto 0,1 gradi + "
               "deriva 0,005 gradi/s (classe INS tattica con GNSS; nessuna scheda aperta)"}
PORTATORE = {"v_m_s": [25, 35], "a_max_m_s2": 4.0, "T_r_s": 0.25, "gdl": 6, "olonomo": "quasi", "canale_avviso": "comando",
             "sensore_in_moto": True, "nota": "profilo deterministico (schema f14 profili_portatore.json), valori I"}
DETRITI = {"n": 30, "dv_sim": 50.0, "dv_decl": 80.0, "vt": [5.0, 30.0], "rcs": [1e-4, 1e-2], "v_mezzi": [30.0, 40.0],
           "nota": "dv_sim 50 m/s nel simulatore; dv_decl 80 m/s nel volume dichiarato (margine dichiarato, I)"}
Q_TR = 80.0          # densita' del rumore d'accelerazione del tracciatore (m^2/s^3), I
A_MAX_INV = 10.0     # inviluppo del bersaglio: |a| <= 10 m/s^2 (I; la virata simulata e' 8)
GPORTA = 30.0        # porta per C(tau)
VT_MAX_DECL = 40.0   # velocita' limite massima dichiarata dei frammenti (sim: <= 30), I


# ------------------------------------------------------------------ frammenti (COPIA di eventi_volo.frammenti_volo)
def frammenti_volo(ev, rng, dt=0.05, t_max=90.0):
    p0 = np.asarray(ev["p"], float)
    vc = np.asarray(ev["vc"], float)
    w = np.asarray(ev.get("vento", [0, 0, 0]), float)
    gv = np.array([0.0, 0.0, -G])
    out = []
    for _ in range(ev["n_frammenti"]):
        u = rng.standard_normal(3)
        u = u / np.linalg.norm(u) * ev["dv_max_m_s"] * rng.random() ** (1 / 3)
        vt = math.exp(rng.uniform(math.log(ev["v_t_m_s"][0]), math.log(ev["v_t_m_s"][1])))
        k = G / vt ** 2
        p, v, T, P, t = p0.copy(), vc + u, [0.0], [p0.copy()], 0.0
        while t < t_max - 1e-9:
            if p[2] <= 0:
                p[2], v = 0.0, np.zeros(3)
            else:
                kv = k * np.linalg.norm(v - w) * dt
                v = (v + gv * dt + kv * w) / (1 + kv)
                p = p + v * dt
                if p[2] <= 0:
                    p[2], v = 0.0, np.zeros(3)
            t += dt
            T.append(t)
            P.append(p.copy())
        out.append((np.array(T), np.array(P), vt, float(np.linalg.norm(u))))
    return out


def chi2_3_cdf(x):
    if x <= 0:
        return 0.0
    return math.erf(math.sqrt(x / 2)) - math.sqrt(2 * x / math.pi) * math.exp(-x / 2)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


# ------------------------------------------------------------------ verita'
def verita(var, cfg, idx, base):
    sv = np.random.SeedSequence(base, spawn_key=(7, ("lato", "davanti", "dietro", "vira", "F7c").index(var), idx))
    rv = np.random.default_rng(sv)
    rs = np.random.default_rng(np.random.SeedSequence(base, spawn_key=(7, 10 + ("att", "sda").index(cfg), ("lato", "davanti", "dietro", "vira", "F7c").index(var), idx)))
    Tt = np.arange(0, T_FINE + 1e-9, DT)
    n = len(Tt)
    vc = rv.uniform(*PORTATORE["v_m_s"])
    Pc = np.zeros((n, 3))
    Pc[:, 0] = vc * Tt
    Pc[:, 2] = 120.0
    Vc = np.tile([vc, 0, 0], (n, 1))
    # bersaglio: velocita' 35-45, zig-zag laterale 3 m/s^2, periodo 8 s; virata 8 m/s^2 nella variante «vira»
    vt = rv.uniform(35.0, 45.0)
    D0 = rv.uniform(150.0, 300.0)
    p = np.array([D0, rv.uniform(-30, 30), 120.0 + rv.uniform(-15, 15)])
    v = np.array([vt, 0.0, 0.0])
    fase = rv.uniform(0, 2 * math.pi)
    d_sat = rv.uniform(0.5, 3.0)
    segno = rv.choice([-1.0, 1.0])
    Pt, Vt = np.zeros((n, 3)), np.zeros((n, 3))
    for i, t in enumerate(Tt):
        Pt[i], Vt[i] = p, v
        h = np.array([-v[1], v[0], 0.0])
        h /= np.linalg.norm(h)
        a = 3.0 * math.sin(2 * math.pi * t / 8.0 + fase) * h
        if var == "vira" and T_EV <= t <= T_EV + d_sat + 2.0:
            a = 8.0 * segno * h
        v = v + a * DT
        v = v / np.linalg.norm(v) * vt
        p = p + v * DT
    # collisione: punto relativo al portatore all'istante dell'evento
    ie = int(round(T_EV / DT))
    if var in ("lato",):
        rel = np.array([rv.uniform(-20, 20), rv.choice([-1, 1]) * rv.uniform(30, 100), rv.uniform(-10, 10)])
    elif var in ("davanti", "vira"):
        rel = np.array([rv.uniform(30, 100), rv.uniform(-10, 10), rv.uniform(-10, 10)])
    elif var == "dietro":
        rel = np.array([-rv.uniform(30, 100), rv.uniform(-10, 10), rv.uniform(-10, 10)])
    else:   # F7c: quasi collisione, passaggio a 30-60 m di lato o davanti, senza urto
        rel = np.array([rv.uniform(30, 100), rv.choice([-1, 1]) * rv.uniform(30, 60), rv.uniform(-10, 10)])
    pev = Pc[ie] + rel
    hA, hB = rv.uniform(0, 2 * math.pi), None
    hB = hA + rv.uniform(math.radians(60), math.radians(180))
    sA, sB = rv.uniform(*DETRITI["v_mezzi"]), rv.uniform(*DETRITI["v_mezzi"])
    vA = sA * np.array([math.cos(hA), math.sin(hA), 0.0])
    vB = sB * np.array([math.cos(hB), math.sin(hB), 0.0])
    off = np.zeros(3)
    if var == "F7c":
        off = np.array([0, 0, rv.uniform(30, 60)])   # distanza minima 30-60 m in quota: nessun urto
    oggetti = {}
    PA = pev[None, :] + (Tt - T_EV)[:, None] * vA[None, :]
    PB = pev[None, :] + off[None, :] + (Tt - T_EV)[:, None] * vB[None, :]
    VA, VB = np.tile(vA, (n, 1)), np.tile(vB, (n, 1))
    fr = []
    eventi = {"t_ev": None, "d_sat": None, "fumo": None, "glint": None}
    if var != "F7c":
        PA[ie:] = PA[ie]
        PB[ie:] = PB[ie]          # i corpi diventano frammenti pesanti (sotto)
        vm = 0.5 * (vA + vB)
        fr = frammenti_volo({"p": pev, "vc": vm, "n_frammenti": DETRITI["n"], "v_t_m_s": DETRITI["vt"],
                             "dv_max_m_s": DETRITI["dv_sim"]}, rv, dt=0.05, t_max=T_FINE - T_EV)
        fr += frammenti_volo({"p": pev, "vc": vm, "n_frammenti": 2, "v_t_m_s": [20.0, 30.0], "dv_max_m_s": 15.0}, rv, dt=0.05, t_max=T_FINE - T_EV)
        eventi.update(t_ev=T_EV, d_sat=d_sat,
                      fumo={"c": pev, "deriva": 0.3 * vm, "r0": 5.0, "cresc": 3.0, "rmax": 30.0, "dur": rv.uniform(5, 20)})
        PA[ie:] = EVF
        PB[ie:] = EVF
    else:
        if rv.random() < 0.5:
            eventi["glint"] = (rv.uniform(3, 18), 0.5)
    oggetti["droneA"] = (PA, VA, 0.03)
    oggetti["droneB"] = (PB, VB, 0.03)
    frs = []
    for j, (T, P, vtj, un) in enumerate(fr):
        Pi = np.stack([np.interp(Tt - T_EV, T, P[:, c]) for c in range(3)], 1)
        Pi[Tt < T_EV] = EVF
        rcs = 0.02 if j >= DETRITI["n"] else math.exp(rv.uniform(math.log(DETRITI["rcs"][0]), math.log(DETRITI["rcs"][1])))
        frs.append((Pi, rcs))
    ins = (rv.standard_normal(3) * INS["s_p0"], rv.standard_normal(3) * INS["s_b"],
           np.cumsum(rv.standard_normal((n, 3)) * INS["s_rw"] * math.sqrt(DT), 0),
           rv.standard_normal(2) * INS["s_att0"], rv.standard_normal(2) * INS["s_om"])
    return dict(T=Tt, Pc=Pc, Vc=Vc, Pt=Pt, Vt=Vt, ogg=oggetti, frs=frs, ev=eventi, ins=ins, rs=rs, var=var, cfg=cfg, idx=idx,
                vc=vc, rel=rel.tolist(), vt=vt, D0=D0, d_sat=d_sat)


EVF = np.array([1e7, 1e7, -1e4])     # «non ancora esistente»


def fumo_al(W, t):
    f = W["ev"]["fumo"]
    if f is None or t < T_EV or t > T_EV + f["dur"]:
        return None
    s = t - T_EV
    return f["c"] + f["deriva"] * s, min(f["r0"] + f["cresc"] * s, f["rmax"])


def seg_sfera(a, b, c, r):
    d = b - a
    L2 = float(d @ d)
    s = 0.0 if L2 == 0 else max(0.0, min(1.0, float((c - a) @ d) / L2))
    return float(np.linalg.norm(a + s * d - c)) <= r


def saturata(W, t):
    e = W["ev"]
    if e["t_ev"] is not None and e["t_ev"] <= t < e["t_ev"] + e["d_sat"]:
        return True
    if e["glint"] is not None and e["glint"][0] <= t < e["glint"][0] + e["glint"][1]:
        return True
    return False


def posa_stimata(W, i):
    e0, b, rw, a0, om = W["ins"]
    t = W["T"][i]
    return W["Pc"][i] + e0 + b * t + rw[i], a0 + om * t        # (posizione stimata, errore [imbardata, beccheggio])


def ruota(v, ea):
    y, p = ea
    cy, sy, cp, sp = math.cos(y), math.sin(y), math.cos(p), math.sin(p)
    Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
    Ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
    return Rz @ Ry @ v


def pd_radar(rc, rcs, r):
    S = 18.93 * (rcs / rc["rcs_ref"]) * (rc["r_ref"] / max(r, 1.0)) ** 4
    return math.exp(PFA_LN / (1 + S))


def in_campo_radar(rc, rel):
    r = np.linalg.norm(rel)
    az = math.degrees(math.atan2(rel[1], rel[0]))
    el = math.degrees(math.asin(rel[2] / max(r, 1e-6)))
    if rc["dietro"]:
        return abs(el) <= rc["el"] and r <= rc["r_max"]
    return abs(az) <= rc["az"] and abs(el) <= rc["el"] and r <= rc["r_max"]


def r_libero(rc):
    """portata entro la quale un oggetto di 1e-4 m2 e' rilevato con Pd >= 0,785 a scansione (0,99 su 3): oltre e' «non so»."""
    S = PFA_LN / math.log(0.785) - 1
    return rc["r_ref"] * ((1e-4 / rc["rcs_ref"]) * 18.93 / S) ** 0.25


# ------------------------------------------------------------------ misure radar (nel riferimento del portatore)
def scansione_radar(W, i, rc, rs):
    """Ritorna lista di (z_mondo_stimato[3], R[3x3], vr, sorgente) gia' compensate con la posa STIMATA."""
    pc = W["Pc"][i]
    pce, ea = posa_stimata(W, i)
    vc = W["Vc"][i]
    ogg = [("bersaglio", W["Pt"][i], W["Vt"][i], 0.02)]
    for k, (P, V, rcs) in W["ogg"].items():
        if P[i][2] > -1e3:
            ogg.append((k, P[i], V[i], rcs))
    for j, (P, rcs) in enumerate(W["frs"]):
        if P[i][2] > 0.5:
            vv = (P[i] - P[max(i - 1, 0)]) / DT
            ogg.append(("fr%02d" % j, P[i], vv, rcs))
    # mascheramento CFAR: frammenti a meno di 15 m in distanza e 2 larghezze di fascio dal bersaglio
    relb = W["Pt"][i] - pc
    rb = np.linalg.norm(relb)
    out = []
    for (k, p, v, rcs) in ogg:
        rel = p - pc
        if not in_campo_radar(rc, rel):
            continue
        r = float(np.linalg.norm(rel))
        pd = pd_radar(rc, rcs, r)
        if k == "bersaglio":
            for (kk, pp, vv, rr) in ogg:
                if kk.startswith("fr"):
                    rl = pp - pc
                    rr_ = np.linalg.norm(rl)
                    if abs(rr_ - rb) < 15 and math.acos(max(-1, min(1, rl @ relb / (rr_ * rb)))) < 2 * rc["s_a"] * 2.5:
                        pd *= 0.3
                        break
        if rs.random() > pd:
            continue
        out.append(_misura(rel, v - vc, rc, rs, pce, ea, k))
    # echi spuri: fondo (Poisson 0,5 per scansione nel campo) + 3 s di echi nella nube dopo l'urto (Poisson 3)
    for _ in range(rs.poisson(rc["falsi"])):
        r = rs.uniform(20, rc["r_max"])
        az = math.radians(rs.uniform(-rc["az"], rc["az"]))
        el = math.radians(rs.uniform(-rc["el"], rc["el"]))
        rel = r * np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
        out.append(_misura(rel, rs.uniform(-60, 60) * rel / r, rc, rs, pce, ea, "falso"))
    e = W["ev"]
    if e["t_ev"] is not None and e["t_ev"] <= W["T"][i] < e["t_ev"] + 3.0:
        s = W["T"][i] - e["t_ev"]
        c = e["fumo"]["c"] + e["fumo"]["deriva"] * s
        for _ in range(rs.poisson(3.0)):
            p = c + rs.standard_normal(3) * (5 + 30 * s)
            rel = p - pc
            if in_campo_radar(rc, rel):
                out.append(_misura(rel, rs.uniform(-60, 60) * rel / np.linalg.norm(rel), rc, rs, pce, ea, "spurio_nube"))
    return out


def _misura(rel, vrel, rc, rs, pce, ea, k):
    r = np.linalg.norm(rel)
    az = math.atan2(rel[1], rel[0])
    el = math.asin(rel[2] / r)
    rm = r + rs.standard_normal() * rc["s_r"]
    azm = az + rs.standard_normal() * rc["s_a"]
    elm = el + rs.standard_normal() * rc["s_a"]
    vr = float(vrel @ rel / r) + rs.standard_normal() * rc["s_d"]
    body = rm * np.array([math.cos(elm) * math.cos(azm), math.cos(elm) * math.sin(azm), math.sin(elm)])
    z = pce + ruota(body, ea)       # compensazione del moto proprio con la posa STIMATA (l'errore INS resta)
    u = body / rm
    t1 = np.array([-math.sin(azm), math.cos(azm), 0.0])
    t2 = np.cross(u, t1)
    sa_ins = math.hypot(rc["s_a"], INS["s_att0"] * 2)
    R = (rc["s_r"] ** 2) * np.outer(u, u) + (rm * sa_ins) ** 2 * (np.outer(t1, t1) + np.outer(t2, t2)) + (INS["s_p0"] * 2) ** 2 * np.eye(3)
    return (z, R, vr, k, u)


# ------------------------------------------------------------------ tracciatore
class Traccia:
    n = 0

    def __init__(self, z, R, t, ruolo="ignota"):
        Traccia.n += 1
        self.id = Traccia.n
        self.x = np.concatenate([z, np.zeros(3)])
        self.P = np.zeros((6, 6))
        self.P[:3, :3] = R
        self.P[3:, 3:] = np.eye(3) * (60.0 ** 2 if ruolo == "ignota" else 5.0 ** 2)
        self.t, self.t_vista, self.colpi, self.storia = t, t, 1, [t]
        self.confermata = ruolo == "bersaglio"
        self.ruolo = ruolo
        self.dubbi, self.sporchi, self.nel_volume = 0, 0, False
        self.r_ult = K99 * math.sqrt(np.trace(R) / 3)

    def predici(self, t):
        d = t - self.t
        if d <= 0:
            return
        F = np.eye(6)
        F[:3, 3:] = np.eye(3) * d
        Q = Q_TR * np.block([[np.eye(3) * d ** 3 / 3, np.eye(3) * d ** 2 / 2], [np.eye(3) * d ** 2 / 2, np.eye(3) * d]])
        self.x = F @ self.x
        self.P = F @ self.P @ F.T + Q
        self.t = t

    def aggiorna(self, z, R):
        H = np.hstack([np.eye(3), np.zeros((3, 3))])
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ (z - H @ self.x)
        self.P = (np.eye(6) - K @ H) @ self.P
        self.t_vista = self.t
        self.colpi += 1
        self.storia.append(self.t)
        self.r_ult = K99 * math.sqrt(np.trace(self.P[:3, :3]) / 3)

    def d2(self, z, R, vr, u, pce, vce, s_d, con_doppler):
        S = self.P[:3, :3] + R
        e = z - self.x[:3]
        d2 = float(e @ np.linalg.solve(S, e))
        if con_doppler and self.colpi >= 3:
            vrp = float((self.x[3:] - vce) @ u)
            svr = math.sqrt(s_d ** 2 + float(u @ self.P[3:, 3:] @ u)) + 2.0
            if abs(vr - vrp) > 3 * svr:
                return 1e9
            d2 += ((vr - vrp) / svr) ** 2
        return d2

    def regione(self, t, pc=None):
        """raggio dichiarato: max(r99 gaussiano, inviluppo r0 + dv tau + a tau^2/2), tau dall'ultima osservazione, PIU'
        il margine dell'errore di navigazione CORRELATO (non riducibile filtrando): 3(s_p0 + s_b t + s_rw sqrt t) +
        distanza x 3(s_att0 + s_om t). Aggiunto dopo lo sviluppo (seme 20261120 idx 0: r99 superato di 0,2-1 m)."""
        tau = max(0.0, t - self.t_vista)
        dist = 0.0 if pc is None else float(np.linalg.norm(self.x[:3] - pc))
        m_ins = 3 * (INS["s_p0"] + INS["s_b"] * t + INS["s_rw"] * math.sqrt(t)) + dist * 3 * (INS["s_att0"] + INS["s_om"] * t)
        r99 = K99 * math.sqrt(np.trace(self.P[:3, :3]) / 3) + m_ins
        if tau <= 0.3:
            return r99, tau
        dv = 3 * math.sqrt(np.trace(self.P[3:, 3:]) / 3)
        return max(r99, self.r_ult + m_ins + dv * tau + 0.5 * A_MAX_INV * tau * tau), tau


def in_volume(ev, p, t, margine=0.0):
    """volume dei detriti dichiarato: cono orizzontale {p0 + S(vc + u): S in [0, tau], |u| <= dv} piu' r0, quote
    [z0 - (dv+|vcz|) tau - g tau^2/2, z0 + (vcz + dv) tau] (dimostrato nel modello: resistenza lungo -v, vento nullo)."""
    tau = t - ev["t0"]
    if tau < 0:
        return False
    p0, vc, dv, r0 = ev["p0"], ev["vc"], ev["dv"], ev["r0"] + margine
    zmin = p0[2] - (dv + abs(vc[2])) * tau - 0.5 * G * tau * tau - r0
    zmax = p0[2] + (vc[2] + dv) * tau + r0
    if not (zmin <= p[2] <= zmax):
        return False
    # limite del cammino con la resistenza: d|v|/dt <= g - k|v|^2, k = g / vt_max^2 (vt_max dichiarata 40 m/s), v0 <= |vc| + dv
    vtm = VT_MAX_DECL
    a = G / vtm
    v0 = float(np.linalg.norm(vc)) + dv
    L = (vtm * vtm / G) * math.log(math.cosh(a * tau) + (v0 / vtm) * math.sinh(a * tau)) + r0
    if float(np.linalg.norm(p - p0)) > L:
        return False
    S = np.linspace(0, tau, 64)
    c = p0[:2][None, :] + S[:, None] * vc[:2][None, :]
    d = np.hypot(p[0] - c[:, 0], p[1] - c[:, 1])
    # fra due nodi della griglia il bordo esatto puo' sporgere al piu' di |vc| tau / 63: lo aggiungo (prudente)
    return bool(np.any(d <= r0 + S * dv + np.linalg.norm(vc[:2]) * tau / 63.0))


def raggio_volume(ev, t):
    tau = max(0.0, t - ev["t0"])
    a = G / VT_MAX_DECL
    v0 = float(np.linalg.norm(ev["vc"])) + ev["dv"]
    L = (VT_MAX_DECL ** 2 / G) * math.log(math.cosh(a * tau) + (v0 / VT_MAX_DECL) * math.sinh(a * tau))
    return ev["r0"] + min(ev["dv"] * tau + float(np.linalg.norm(ev["vc"])) * tau, L)


def passaggio(var, cfg, idx, base, registro=None):
    W = verita(var, cfg, idx, base)
    rc, cc = CFG[cfg]["radar"], CFG[cfg]["camera"]
    rs = W["rs"]
    Traccia.n = 0
    T = W["T"]
    # consegna iniziale del bersaglio (designato dalla missione: etichetta a mano)
    pce0, ea0 = posa_stimata(W, 0)
    z0 = W["Pt"][0] + rs.standard_normal(3) * 2.0
    tb = Traccia(z0, np.eye(3) * 9.0, 0.0, "bersaglio")
    tb.x[3:] = W["Vt"][0] + rs.standard_normal(3)
    tracce = [tb]
    ev_decl, n_radar = None, 0
    nuove_recenti = []           # (t, z) misure non associate
    stato_cam, cam_ok_run, cam_ultima_sat = "affidabile", 0, None
    res = dict(var=var, cfg=cfg, idx=idx, cont_ok=True, cicli_fuori=0, libero=0, libero_fr=0, assoc_detriti_non_dich=0,
               assoc_dubbie=0, evento_t=None, falso_evento=False, rit_riacq=None, rit_riacq_cam=None, cam_sat_affid=0,
               vol_dentro=0, vol_tot=0, avviso_t=None, interseca_t=None, curva=[], parametri=dict(vc=W["vc"], vt=W["vt"], D0=W["D0"], rel=W["rel"], d_sat=W["d_sat"]))
    t_sat_fine = (T_EV + W["d_sat"]) if W["ev"]["t_ev"] is not None else None
    prox_radar = 0.0
    Rlib = r_libero(rc)
    righe = []
    for i, t in enumerate(T):
        if i == 0:
            continue
        pce, ea = posa_stimata(W, i)
        vce = W["Vc"][i]
        assegnate = {}
        # ---- radar (una o piu' scansioni per ciclo)
        while prox_radar <= t + 1e-9:
            mis = scansione_radar(W, i, rc, rs)
            prox_radar += rc["periodo"]
            n_radar += 1
            for tr in tracce:
                tr.predici(t)
            M = len(mis)
            if M:
                C = np.full((len(tracce), M), 1e6)
                for a, tr in enumerate(tracce):
                    for b, (z, R, vr, k, u) in enumerate(mis):
                        d2 = tr.d2(z, R, vr, u, pce, vce, rc["s_d"], True)
                        if d2 <= GATE + (8.0 if tr.colpi >= 3 else 0):
                            C[a, b] = d2
                ri, ci = linear_sum_assignment(C)
                usate = set()
                for a, b in zip(ri, ci):
                    if C[a, b] >= 1e6:
                        continue
                    tr = tracce[a]
                    z, R, vr, k, u = mis[b]
                    if tr.ruolo == "bersaglio":
                        if ev_decl is not None and in_volume(ev_decl, z, t):
                            tr.dubbi += 1           # dichiarata: associazione dentro il volume dei detriti
                            res["assoc_dubbie"] += 1
                            if k != "bersaglio":
                                tr.sporchi += 1
                        elif k != "bersaglio":
                            res["assoc_detriti_non_dich"] += 1
                            tr.sporchi += 1
                        if k == "bersaglio" and t_sat_fine is not None and t >= t_sat_fine and res["rit_riacq"] is None:
                            res["rit_riacq"] = round(t - t_sat_fine, 2)
                    tr.aggiorna(z, R)
                    usate.add(b)
                for b, m in enumerate(mis):
                    if b not in usate:
                        nt = Traccia(m[0], m[1], t)
                        if ev_decl is not None and in_volume(ev_decl, m[0], t, 20.0):
                            nt.nel_volume = True
                        tracce.append(nt)
                        nuove_recenti.append((t, m[0]))
            # conferma 3 su 5, cancellazione delle non confermate dopo 1 s e delle confermate dopo 3 s (tranne il bersaglio)
            for tr in tracce:
                if not tr.confermata and tr.colpi >= 3 and len([s for s in tr.storia if s >= t - 5 * rc["periodo"] - 1e-9]) >= 3:
                    tr.confermata = True
            tracce = [tr for tr in tracce if tr.ruolo == "bersaglio" or (t - tr.t_vista) < (3.0 if tr.confermata else 1.0)]
            # riacquisizione presunta: il bersaglio non aggiornato da > 0,5 s; una traccia confermata nata dopo la
            # perdita, fuori dal volume dei detriti, dentro l'insieme di presenza del bersaglio -> ne prende lo stato
            # (identita' «presunta»; dichiarato nel registro). Aggiunta dopo lo sviluppo (vira/att idx 4 e 8).
            if t - tb.t_vista > 0.5:
                rB_, _ = tb.regione(t, W["Pc"][i])
                cand = [tr for tr in tracce if tr is not tb and tr.confermata and not tr.nel_volume and tr.colpi >= 3
                        and tr.storia[0] >= tb.t_vista - 0.5 and np.linalg.norm(tr.x[:3] - tb.x[:3]) <= rB_
                        and not (ev_decl is not None and in_volume(ev_decl, tr.x[:3], t))]
                if cand:
                    c_ = min(cand, key=lambda tr: np.linalg.norm(tr.x[:3] - tb.x[:3]))
                    tb.x, tb.P, tb.t_vista, tb.r_ult = c_.x.copy(), c_.P.copy(), c_.t_vista, c_.r_ult
                    tb.riacquisizioni = getattr(tb, "riacquisizioni", 0) + 1
                    tracce = [tr for tr in tracce if tr is not c_]
                    res["riacq_presunte"] = res.get("riacq_presunte", 0) + 1
        # ---- evento: grappolo di >= 5 misure nuove entro 40 m in 1 s E (saturazione delle camere O tracce che convergono)
        nuove_recenti = [(s, z) for (s, z) in nuove_recenti if s >= t - 1.0]
        sat = saturata(W, t)
        if ev_decl is None and len(nuove_recenti) >= 5:
            Z = np.array([z for _, z in nuove_recenti])
            for z in Z:
                vic = Z[np.linalg.norm(Z - z, axis=1) <= 40.0]
                if len(vic) >= 5:
                    conv = False
                    conf = [tr for tr in tracce if tr.confermata and tr.ruolo != "bersaglio" and np.linalg.norm(tr.x[:3] - z) < 80]
                    for a in range(len(conf)):
                        for b in range(a + 1, len(conf)):
                            if np.linalg.norm(conf[a].x[:3] - conf[b].x[:3]) < 20:
                                conv = True
                    if sat or conv or cam_ultima_sat is not None and t - cam_ultima_sat < 1.0:
                        c = vic.mean(0)
                        vic_t = [s for (s, zz) in nuove_recenti if np.linalg.norm(zz - z) <= 40]
                        vel = [tr.x[3:] for tr in conf if tr.colpi >= 5]
                        vcs = np.mean(vel, 0) if vel else np.zeros(3)
                        dvd = DETRITI["dv_decl"] + (10.0 if vel else 60.0)
                        t0 = min(vic_t) - 0.3
                        sp = float(np.max(np.linalg.norm(vic - c, axis=1)))
                        ev_decl = {"t0": t0, "p0": c - vcs * (t - t0), "vc": vcs, "dv": dvd, "r0": 15.0 + sp, "t_dich": round(t, 2)}
                        res["evento_t"] = round(t, 2)
                        if W["ev"]["t_ev"] is None:
                            res["falso_evento"] = True
                        for tr in tracce:
                            if tr.ruolo != "bersaglio" and in_volume(ev_decl, tr.x[:3], t, 20.0):
                                tr.nel_volume = True
                    break
        # ---- camera: saturazione letta dal sensore (istogramma; nel simulatore: finestra della fiammata)
        if sat:
            cam_ultima_sat = t
            stato_cam = "non_affidabile_saturazione"
            cam_ok_run = 0
        elif stato_cam != "affidabile":
            # dopo la saturazione: «degradata (possibile fumo)» finche' la camera non rivede il bersaglio coerente col radar per 5 cicli
            rel = W["Pt"][i] - W["Pc"][i]
            ang = math.degrees(math.atan2(rel[1], rel[0]))
            r = np.linalg.norm(rel)
            fu = fumo_al(W, t)
            vis = (abs(ang) <= cc["fov"] or cc["brandeggio"]) and r <= cc["r_max"] and not (fu is not None and seg_sfera(W["Pc"][i], W["Pt"][i], fu[0], fu[1]))
            if vis and rs.random() < cc["pd"]:
                e = tb.x[:3] - pce
                if math.acos(max(-1, min(1, (e @ rel) / (np.linalg.norm(e) * r)))) < 3 * (math.sqrt(np.trace(tb.P[:3, :3]) / 3) / r) + 0.01:
                    cam_ok_run += 1
                    if res["rit_riacq_cam"] is None and t_sat_fine is not None and t >= t_sat_fine:
                        res["rit_riacq_cam"] = round(t - t_sat_fine, 2)
            else:
                cam_ok_run = 0
            stato_cam = "ripristinata_dichiarata" if cam_ok_run >= 5 else "degradata_possibile_fumo"
        if sat and stato_cam == "affidabile":
            res["cam_sat_affid"] += 1
        # ---- misure dei risultati
        rB, tauB = tb.regione(t, W["Pc"][i])
        eB = float(np.linalg.norm(W["Pt"][i] - tb.x[:3]))
        if eB > rB:
            res["cont_ok"] = False
            res["cicli_fuori"] += 1
        if W["ev"]["t_ev"] is not None and t >= T_EV:
            s2 = np.trace(tb.P[:3, :3]) / 3
            res["curva"].append((round(t - T_EV, 1), round(tauB, 2), int(eB <= K90 * math.sqrt(s2)), int(eB <= rB)))

        def libero(p):
            rel = p - W["Pc"][i]
            if not in_campo_radar(rc, rel) or np.linalg.norm(rel) > Rlib:
                return False
            if ev_decl is not None and in_volume(ev_decl, p, t):
                return False
            for tr in tracce:
                r, _ = tr.regione(t, W["Pc"][i])
                if np.linalg.norm(p - tr.x[:3]) <= r:
                    return False
            return True
        if libero(W["Pt"][i]):
            res["libero"] += 1
        if W["ev"]["t_ev"] is not None and t > T_EV:
            for (P, rcs) in W["frs"]:
                if P[i][2] > 0.5 and libero(P[i]):
                    res["libero_fr"] += 1
            if ev_decl is not None and abs(round(t * 2) - t * 2) < 1e-6:
                for (P, rcs) in W["frs"]:
                    if P[i][2] > 0.5:
                        res["vol_tot"] += 1
                        res["vol_dentro"] += int(in_volume(ev_decl, P[i], t))
            # verita': un frammento a <= 10 m dal portatore
            if res["interseca_t"] is None:
                for (P, rcs) in W["frs"]:
                    if P[i][2] > 0.5 and np.linalg.norm(P[i] - W["Pc"][i]) <= 10.0:
                        res["interseca_t"] = round(t, 2)
                        break
        avv = None
        if ev_decl is not None:
            for s in np.arange(0, 5.01, 0.2):
                pf = pce + vce * s
                if in_volume(ev_decl, pf, t + s, 1.0 + 3 * INS["s_p0"]):
                    avv = round(s, 1)
                    break
            if avv is not None and res["avviso_t"] is None:
                res["avviso_t"] = round(t, 2)
        if registro is not None:
            righe.append(_riga(W, i, t, tracce, tb, ev_decl, stato_cam, avv, rc))
    res["id_ok"] = bool(np.linalg.norm(W["Pt"][-1] - tb.x[:3]) <= 30.0 and res["assoc_detriti_non_dich"] == 0)
    res["sporchi"] = tb.sporchi
    res["err_fine_m"] = round(float(np.linalg.norm(W["Pt"][-1] - tb.x[:3])), 1)
    if registro is not None:
        with open(registro, "x", encoding="utf-8") as f:
            f.write(json.dumps({"intestazione": {"scenario": "F7-" + var, "configurazione": cfg + " (ipotesi; latenze non simulate)",
                                                 "seme": "SeedSequence(%d, spawn_key=(7, var, idx=%d))" % (base, idx), "idx": idx,
                                                 "stato": "simulato; nessun sensore fisico; etichette a mano; solo osservazione e avviso",
                                                 "parametri": res["parametri"], "riassunto": {k: res[k] for k in ("evento_t", "falso_evento", "rit_riacq", "rit_riacq_cam", "avviso_t", "interseca_t", "id_ok", "cont_ok", "libero", "libero_fr")}}},
                               ensure_ascii=False) + "\n")
            for r in righe:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return res


def _riga(W, i, t, tracce, tb, ev, stato_cam, avv, rc):
    tr_out = []
    for tr in tracce:
        if not tr.confermata:
            continue
        r, tau = tr.regione(t, W["Pc"][i])
        s2 = np.trace(tr.P[:3, :3]) / 3
        parola = "vista" if tau <= 0.3 else "non_vista_regione"
        ide = None
        if tr.ruolo == "bersaglio":
            ide = "confermata" if t < T_EV else ("presunta_dubbia" if tr.dubbi else "presunta")
        tr_out.append({"id": tr.id, "ruolo": tr.ruolo if tr.ruolo == "bersaglio" else ("frammento_possibile" if tr.nel_volume else "non_classificata"),
                       "identita": ide, "pos": [round(float(x), 1) for x in tr.x[:3]], "vel": [round(float(x), 1) for x in tr.x[3:]],
                       "non_vista_da_s": round(tau, 2), "parola": parola,
                       "confidenza_C": round(chi2_3_cdf(GPORTA ** 2 / s2), 4) if tr.ruolo == "bersaglio" else None,
                       "porta_m": GPORTA, "r90_m": round(K90 * math.sqrt(s2), 1), "r99_m": round(K99 * math.sqrt(s2), 1),
                       "insieme_presenza_r_m": round(r, 1)})
    evo = None
    if ev is not None:
        evo = {"tipo": "collisione_o_esplosione_vicina", "t_dichiarato": ev["t_dich"], "parola": "volume dei detriti dichiarato; frammenti non verificati uno per uno: mai libero dentro",
               "volume": {"apice": [round(float(x), 1) for x in ev["p0"]], "vc": [round(float(x), 1) for x in ev["vc"]], "dv_m_s": ev["dv"],
                          "r0_m": round(ev["r0"], 1), "t0": round(ev["t0"], 2), "raggio_m": round(raggio_volume(ev, t), 1)},
               "impronta": {"ispezionati": [0, 1]}}
    vera = {"bersaglio": [round(float(x), 1) for x in W["Pt"][i]], "portatore": [round(float(x), 1) for x in W["Pc"][i]]}
    for k, (P, V, rcs) in W["ogg"].items():
        if P[i][2] > -1e3:
            vera[k] = [round(float(x), 1) for x in P[i]]
    return {"t": round(t, 1), "tracce": tr_out, "evento": evo,
            "affidabilita_sensori": {"radar_bordo#0": "affidabile", "camera#1": stato_cam},
            "verita": vera, "frammenti_veri_in_aria": int(sum(1 for (P, r) in W["frs"] if P[i][2] > 0.5)),
            "avviso_portatore": None if avv is None else {"percorso_interseca_volume_fra_s": avv, "testo": "avviso: il percorso entra nel volume dei detriti"},
            "posa_stimata": [round(float(x), 2) for x in posa_stimata(W, i)[0]]}


VARIANTI = ("lato", "davanti", "dietro", "vira", "F7c")


def _lavoro(a):
    var, cfg, idx, base = a
    r = passaggio(var, cfg, idx, base)
    return r


def main():
    if sys.argv[1] == "--registro":
        d = sys.argv[2]
        for var in VARIANTI:
            passaggio(var, "sda", 0, 20261121, registro=os.path.join(d, "registro_F7_%s.jsonl" % var))
        return
    fase = sys.argv[1]
    proc = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    base, n, n_c = (20261120, 10, 10) if fase == "sviluppo" else (20261121, 60, 200)
    lav = [(v, c, i, base) for v in VARIANTI for c in ("att", "sda") for i in range(n_c if v == "F7c" else n)]
    from multiprocessing import Pool
    with Pool(proc) as p:
        out = p.map(_lavoro, lav, chunksize=4)
    with open(os.path.join(QUI, "passaggi_%s%s.jsonl" % (fase, os.environ.get("F7_SUFFISSO", ""))), "x", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False, default=float) + "\n")
    print(json.dumps(riassumi(out), ensure_ascii=False, indent=0))


def riassumi(out):
    tab = {}
    for v in VARIANTI:
        for c in ("att", "sda"):
            rr = [r for r in out if r["var"] == v and r["cfg"] == c]
            N = len(rr)

            def w(k):
                return [k, N, *[round(x, 3) for x in wilson(k, N)]]
            riacq = [r["rit_riacq"] for r in rr if r["rit_riacq"] is not None]
            inters = [r for r in rr if r["interseca_t"] is not None]
            tab["%s/%s" % (v, c)] = {
                "continuita": w(sum(r["cont_ok"] for r in rr)),
                "identita": w(sum(r["id_ok"] for r in rr)),
                "riacq_2s": w(sum(1 for r in rr if r["rit_riacq"] is not None and r["rit_riacq"] <= 2.0)) if v != "F7c" else None,
                "riacq_cam_2s": w(sum(1 for r in rr if r["rit_riacq_cam"] is not None and r["rit_riacq_cam"] <= 2.0)) if v != "F7c" else None,
                "libero_bersaglio_passaggi": w(sum(1 for r in rr if r["libero"] > 0)),
                "libero_frammento_passaggi": w(sum(1 for r in rr if r["libero_fr"] > 0)),
                "assoc_non_dichiarate_passaggi": w(sum(1 for r in rr if r["assoc_detriti_non_dich"] > 0)),
                "assoc_dubbie_dichiarate_passaggi": w(sum(1 for r in rr if r["assoc_dubbie"] > 0)),
                "evento_dichiarato": w(sum(1 for r in rr if r["evento_t"] is not None)),
                "falsi_eventi": w(sum(r["falso_evento"] for r in rr)),
                "ritardo_evento_s_max": max([r["evento_t"] - T_EV for r in rr if r["evento_t"] is not None and not r["falso_evento"]], default=None),
                "volume_campioni": [sum(r["vol_dentro"] for r in rr), sum(r["vol_tot"] for r in rr)],
                "volume_passaggi_tutti_dentro": w(sum(1 for r in rr if r["vol_tot"] > 0 and r["vol_dentro"] == r["vol_tot"])),
                "intersecano": len(inters),
                "intersecano_con_avviso_prima": sum(1 for r in inters if r["avviso_t"] is not None and r["avviso_t"] <= r["interseca_t"]),
                "margine_avviso_s_min": min([r["interseca_t"] - r["avviso_t"] for r in inters if r["avviso_t"] is not None], default=None),
                "camera_affidabile_in_saturazione_cicli": sum(r["cam_sat_affid"] for r in rr),
                "cicli_fuori_regione_tot": sum(r["cicli_fuori"] for r in rr),
            }
    return tab


if __name__ == "__main__":
    main()
