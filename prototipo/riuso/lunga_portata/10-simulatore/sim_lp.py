"""sim_lp.py - simulatore dei sensori a lunga portata di MoVi (f15/10-simulatore, sciame-validazione).

Solo numpy. Tutto e' simulazione dalle schede (02-sensori/parametri_lunga_portata.json) o ipotesi dichiarata:
NIENTE e' provato su un sensore fisico. Solo osservazione e avviso: nessuna funzione d'ingaggio o di puntamento
di mezzi (le camere sono 'orientate' dal radar solo per osservare).

Indipendenza: la geometria (linea di vista, orizzonte, nubi), il rumore e i falsi allarmi sono scritti qui, non
presi dal nucleo movi_lp.py. In comune col nucleo: la formula di Pd (Swerling 1) e i numeri delle schede.

Interfaccia:
  catalogo()                                 -> {nome: parametri del sensore simulato}
  SensoreSim(nome, pos, par, meteo=1.0)      .scansioni(verita, t_fine, rng, ...) -> lista di record
  ostacoli_da_poligoni(poligoni)             -> segmenti (p1, p2, h) per la griglia del nucleo e per la vista
  in_vista(pos_s, p, ostacoli, nubi, t, tipo)
  genera_verita(oggetto, comportamento, fattore_v, rng, ...) -> (T, P, V)
"""
import json
import math
import os

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
F15 = os.path.dirname(QUI)
PAR = json.load(open(os.path.join(F15, "02-sensori", "parametri_lunga_portata.json"), encoding="utf-8"))
DEG = math.pi / 180


def _v(sens, campo):
    return PAR["sensori"][sens][campo][0]


def catalogo():
    """Parametri simulati. 'fonte' dice da dove viene ogni numero (scheda del JSON, conto, ipotesi)."""
    S = PAR["sensori"]
    c = {}
    # Radar per droni (Robin IRIS): 3100 m per 0,01 m2 a Pd 0,5 (scheda + ipotesi del JSON), strumentata 12 km.
    c["radar_sorveglianza_droni"] = dict(
        tipo="radar", r_rif_m=_v("radar_sorveglianza_droni", "portata_ref_m"), rcs_rif_m2=_v("radar_sorveglianza_droni", "sigma_ref_m2"),
        pd_rif=_v("radar_sorveglianza_droni", "pd_ref"), pfa=_v("radar_sorveglianza_droni", "pfa"), esponente=4,
        r_max_m=12000.0, periodo_s=_v("radar_sorveglianza_droni", "rivisita_s"), rotante=True,
        sigma_r_m=_v("radar_sorveglianza_droni", "sigma_distanza_m"), sigma_az_rad=_v("radar_sorveglianza_droni", "sigma_az_deg") * DEG,
        sigma_el_rad=_v("radar_sorveglianza_droni", "sigma_el_deg") * DEG, az_campo=(-180, 180), el_campo=(-2.0, 58.0),
        latenza_s=0.1, falsi_per_passata=0.5, z_min=0.0, fonte="IRIS (portata, campo, sigma, rivisita); el_campo -2..58: I; "
        "latenza 0,1 s: I (il JSON dice 1 s come rivisita); falsi ritorni 0,5 per giro: I")
    c["radar_drone_pannello"] = dict(
        tipo="radar", r_rif_m=1000.0, rcs_rif_m2=0.01, pd_rif=0.5, pfa=1e-6, esponente=4, r_max_m=3000.0, periodo_s=0.1,
        rotante=False, sigma_r_m=3.25, sigma_az_rad=1.0 * DEG, sigma_el_rad=1.5 * DEG, az_campo=(-60, 60), el_campo=(-10, 70),
        latenza_s=0.1, falsi_per_passata=0.05, z_min=0.0, fonte="ECHO (sigma); portata, campo, rivisita: ipotesi del JSON")
    # Radar del movimento a terra (SCANTER): 2D, 5 km per 1 m2 (ipotesi del JSON), Pd 0,9, giro 1 s (scheda).
    c["radar_movimento_a_terra"] = dict(
        tipo="radar", r_rif_m=5000.0, rcs_rif_m2=1.0, pd_rif=0.9, pfa=1e-6, esponente=4, r_max_m=9600.0, periodo_s=1.0,
        rotante=True, sigma_r_m=7.5, sigma_az_rad=0.29 * DEG / 2, sigma_el_rad=0.3, az_campo=(-180, 180), el_campo=(-30, 5.0),
        latenza_s=_v("radar_movimento_a_terra", "latenza_s"), falsi_per_passata=0.5, z_min=0.0, due_d=True,
        fonte="TERMA (giro, cella, fascio); 5 km per 1 m2, Pd 0,9, sigma 7,5 m: ipotesi del JSON; el_campo e falsi: I")
    # Radar primario d'aeroporto: SOLO dalla nota della scheda TERMA ('non coprono sotto 200-300 m, aggiornano ogni 4 s').
    c["radar_aeroporto"] = dict(
        tipo="radar", r_rif_m=60000.0, rcs_rif_m2=1.0, pd_rif=0.8, pfa=1e-6, esponente=4, r_max_m=80000.0, periodo_s=4.0,
        rotante=True, sigma_r_m=50.0, sigma_az_rad=0.1 * DEG, sigma_el_rad=1.0 * DEG, az_campo=(-180, 180), el_campo=(-1, 40),
        latenza_s=0.5, falsi_per_passata=0.5, z_min=200.0,
        fonte="giro 4 s e quota minima 200 m: nota della scheda TERMA; portata 60 km per 1 m2, sigma: I")
    c["radar_4d_auto"] = dict(
        tipo="radar", r_rif_m=300.0, rcs_rif_m2=10.0, pd_rif=0.9, pfa=1e-6, esponente=4, r_max_m=300.0, periodo_s=0.2,
        rotante=False, sigma_r_m=0.15, sigma_az_rad=0.3 * DEG, sigma_el_rad=0.6 * DEG, az_campo=(-60, 60), el_campo=(-14, 14),
        latenza_s=0.05, falsi_per_passata=float(os.environ.get("MOVI_FALSI_4D", "0.3")), z_min=0.0, v_rad_min=0.3,
        fonte="300 m: ARS548_SEC (fonte secondaria); periodo 0,2 s (scheda 0,05: I, rallentato per il costo); sigma "
        "angolari = 1/4 della risoluzione: I; soglia Doppler 0,3 m/s: I; falsi 0,3 per quadro (il JSON dice 1: I; "
        "con 1 per quadro vedi la prova di sensibilita')")
    # LiDAR: modello 'equivalente' con esponente 4 e riferimento sul drone piccolo (I): 150 m (AT128) e 230 m (Tele-15),
    # cioe' la portata al 10 % ridotta di sqrt(0,05/0,1) per un bersaglio scuro piu' piccolo del passo (I).
    c["lidar_auto_campo_largo"] = dict(
        tipo="lidar", r_rif_m=150.0, rcs_rif_m2=0.01, pd_rif=0.9, pfa=1e-4, esponente=4, r_max_m=_v("lidar_auto_campo_largo", "portata_max_m"),
        periodo_s=0.2, rotante=False, sigma_r_m=0.03, sigma_az_rad=0.05 * DEG, sigma_el_rad=0.1 * DEG, az_campo=(-60, 60),
        el_campo=(-12.7, 12.7), latenza_s=0.1, falsi_per_passata=0.05, z_min=0.0,
        fonte="AT128 (portata 210 m, campo, risoluzione); riferimento drone 150 m, Pd 0,9, periodo 0,2 s (10 Hz in scheda: "
        "rallentato per il costo), falsi 0,1 per quadro: I")
    c["lidar_tele"] = dict(
        tipo="lidar", r_rif_m=230.0, rcs_rif_m2=0.01, pd_rif=0.9, pfa=1e-4, esponente=4, r_max_m=_v("lidar_tele", "portata_max_m"),
        periodo_s=0.2, rotante=False, sigma_r_m=0.02, sigma_az_rad=0.03 * DEG, sigma_el_rad=0.03 * DEG, az_campo=(-7.25, 7.25),
        el_campo=(-8.1, 8.1), latenza_s=0.1, falsi_per_passata=0.05, z_min=0.0,
        fonte="TELE15 (portata 320/500 m, campo, sigma); riferimento drone 230 m, periodo 0,2 s: I")
    # Camere: solo direzione. Distanza 'da triangolazione o telemetro' con sigma 10 % (I). Orientate dal radar.
    c["camera_eo_ottica_lunga"] = dict(
        tipo="camera", pd_in=_v("camera_eo_ottica_lunga", "pd_in_portata"), portata_km={0.3: 2.0, 10: 15.0, 35: 20.0},
        periodo_s=0.2, sigma_ang_rad=_v("camera_eo_ottica_lunga", "sigma_angolo_deg") * DEG, sigma_r_frac=0.10,
        latenza_s=0.1, falsi_per_passata=0.05, campo_deg=2.71, fonte="OSDAR23/conto (campo, IFOV); portata pratica: ipotesi "
        "del JSON; sigma_r 10 %, periodo 0,2 s, falsi: I")
    c["camera_termica_ottica_lunga"] = dict(
        tipo="camera", pd_in=0.8, portata_km={0.3: 0.2, 10: 6.5, 35: 22.8}, periodo_s=0.2, sigma_ang_rad=120e-6,
        sigma_r_frac=0.10, latenza_s=0.1, falsi_per_passata=0.05, campo_deg=4.4,
        fonte="portata = criterio di 12,8 pixel della scheda (conto); Pd 0,8, sigma_r, periodo: I")
    c["ads_b"] = dict(tipo="cooperativa", periodo_s=1.0, sigma_pos_m=92.6 / 2, sigma_vel_ms=10 / 2, lat_non_comp_s=0.6,
                      pd_msg=0.9, portata_m=300000.0, latenza_s=0.0,
                      fonte="CFR91227 (periodo, NACp, NACv, 0,6 s non compensati); sigma = limite/2: I; Pd 0,9: I")
    c["identificazione_remota"] = dict(tipo="cooperativa", periodo_s=1.0, sigma_pos_m=30.5 / 2, sigma_z_m=45.7 / 2,
                                       sigma_vel_ms=2.0, lat_non_comp_s=1.0, pd_msg=0.9, portata_m=1000.0, latenza_s=0.0,
                                       fonte="CFR89310 (periodo, 95 %, latenza); portata 1 km e Pd: I")
    for k in c:
        c[k]["nome_tipo"] = k
    return c


# ----------------------------------------------------------------------------- geometria (indipendente dal nucleo)
def ostacoli_da_poligoni(ostacoli):
    seg = []
    for o in ostacoli:
        pg = o["poligono"]
        for i in range(len(pg)):
            seg.append((tuple(pg[i]), tuple(pg[(i + 1) % len(pg)]), float(o["altezza"])))
    return seg


def _incrocio_2d(a, b, c, d):
    r, q = (b[0] - a[0], b[1] - a[1]), (d[0] - c[0], d[1] - c[1])
    den = r[0] * q[1] - r[1] * q[0]
    if abs(den) < 1e-12:
        return None
    ac = (c[0] - a[0], c[1] - a[1])
    s = (ac[0] * q[1] - ac[1] * q[0]) / den
    u = (ac[0] * r[1] - ac[1] * r[0]) / den
    return s if (0 < s < 1 and 0 <= u <= 1) else None


def nube_al_tempo(n, t, pos_oggetti=None):
    if t < n["t_ini"] or t > n["t_fine"]:
        return None
    dt = t - n["t_ini"]
    c = np.array(n["centro"], float) if "centro" in n else np.array(pos_oggetti(t)[:2], float)
    c = c + np.array(n.get("deriva", [0, 0, 0])[:2], float) * dt * (1 if "centro" in n else 0)
    r = min(n["raggio_m"] + n.get("crescita_m_s", 0.0) * dt, n.get("raggio_max_m", 1e9))
    return c, r, n["altezza_m"]


def in_vista(ps, p, ostacoli=(), nubi=(), t=0.0, nome_sensore=""):
    """True se il segmento sensore-punto non e' coperto da un ostacolo (sotto la sua altezza) ne' da una nube opaca."""
    for (p1, p2, h) in ostacoli:
        s = _incrocio_2d(ps, p, p1, p2)
        if s is not None and ps[2] + s * (p[2] - ps[2]) < h:
            return False
    for (c, r, h, opache) in nubi:
        if nome_sensore not in opache:
            continue
        a, b = np.asarray(ps[:2], float), np.asarray(p[:2], float)
        ab = b - a
        L2 = float(ab @ ab)
        s = 0.0 if L2 < 1e-9 else float(np.clip((c - a) @ ab / L2, 0, 1))
        if np.linalg.norm(a + s * ab - c) <= r and ps[2] + s * (p[2] - ps[2]) <= h:
            return False
    return True


def orizzonte_m(h_s, h_t):
    """Orizzonte radar con raggio terrestre equivalente 4/3: d_km = 4,12 (sqrt(h_s) + sqrt(h_t)) (formula del JSON)."""
    return 4120.0 * (math.sqrt(max(h_s, 0.0)) + math.sqrt(max(h_t, 0.0)))


# ----------------------------------------------------------------------------- sensore simulato
def pd_swerling(par, r, rcs):
    snr_rif = math.log(par["pfa"]) / math.log(par["pd_rif"]) - 1.0
    r = np.maximum(np.asarray(r, float), 1e-3)
    snr = snr_rif * (rcs / par["rcs_rif_m2"]) * (par["r_rif_m"] / r) ** par["esponente"]
    return np.where(r <= par["r_max_m"], par["pfa"] ** (1.0 / (1.0 + snr)), 0.0)


def portata_camera(par, d):
    ks = sorted(par["portata_km"])
    return 1000.0 * float(np.interp(math.log(max(d, 1e-3)), [math.log(k) for k in ks], [par["portata_km"][k] for k in ks]))


def scala_meteo(par, f):
    """Meteo: la portata scala del fattore f (02-sensori, 40-eventi/01-effetti)."""
    q = dict(par)
    if par["tipo"] in ("radar", "lidar"):
        q["r_rif_m"], q["r_max_m"] = par["r_rif_m"] * f, par["r_max_m"] * f
    elif par["tipo"] == "camera":
        q["portata_km"] = {k: v * f for k, v in par["portata_km"].items()}
    return q


class SensoreSim:
    def __init__(self, nome, pos, par, meteo=1.0, ostacoli=(), nubi=(), salute=None):
        self.nome, self.pos, self.base = nome, np.asarray(pos, float), par
        self.par = scala_meteo(par, meteo)
        self.tipo = par["tipo"]
        self.ostacoli, self.nubi = ostacoli, nubi
        self.salute = salute or []        # lista di (t_ini, t_fine, tipo): spento | pioggia_forte | abbagliamento

    def guasto(self, t):
        for (a, b, k) in self.salute:
            if a <= t < b:
                return k
        return None

    def copre(self, p, z_obj=None):
        """Campo, portata massima, orizzonte, quota minima. Non controlla ostacoli (vedi visibile)."""
        d = np.asarray(p, float) - self.pos
        r = float(np.linalg.norm(d))
        if self.tipo in ("radar", "lidar"):
            if r > self.par["r_max_m"] or r < 1.0:
                return False
            az = math.degrees(math.atan2(d[1], d[0]))
            el = math.degrees(math.asin(d[2] / r))
            a0, a1 = self.par["az_campo"]
            az = (az - self.par.get("az0", 0.0) + 180.0) % 360.0 - 180.0     # azimut relativo all'orientamento
            if not (a0 <= az <= a1) or not (self.par["el_campo"][0] <= el <= self.par["el_campo"][1]):
                return False
            if self.tipo == "radar" and r > orizzonte_m(self.pos[2], p[2]):
                return False
            if p[2] < self.par.get("z_min", 0.0):
                return False
            return True
        return True

    def visibile(self, p, t):
        return self.copre(p) and in_vista(self.pos, p, self.ostacoli, self.nubi_al(t), t, self.nome_tipo)

    def nubi_al(self, t):
        out = []
        for (n, fpos) in self.nubi:
            x = nube_al_tempo(n, t, fpos)
            if x is not None:
                out.append((x[0], x[1], x[2], n["opaca_per"]))
        return out

    def _misura(self, p, rng):
        d = p - self.pos
        r = float(np.linalg.norm(d))
        az, el = math.atan2(d[1], d[0]), math.asin(d[2] / r)
        if self.tipo == "camera":
            sr, sa, se = self.par["sigma_r_frac"] * r, self.par["sigma_ang_rad"], self.par["sigma_ang_rad"]
        else:
            sr, sa, se = self.par["sigma_r_m"], self.par["sigma_az_rad"], self.par["sigma_el_rad"]
        er = np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
        ea = np.array([-math.sin(az), math.cos(az), 0.0])
        ee = np.cross(er, ea)
        Bm = np.stack([er, ea, ee], 1)
        sig = np.array([sr, r * math.cos(el) * sa, r * se])
        R = Bm @ np.diag(sig ** 2) @ Bm.T
        z = p + Bm @ (sig * rng.standard_normal(3))
        return z, R, (r, az, el)

    def _falso(self, rng):
        if self.tipo == "camera":
            return None
        r = rng.uniform(5.0, min(self.par["r_max_m"], 15000.0))
        az = (rng.uniform(*self.par["az_campo"]) + self.par.get("az0", 0.0)) * DEG
        el = rng.uniform(max(self.par["el_campo"][0], -2.0), self.par["el_campo"][1]) * DEG
        p = self.pos + r * np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
        p[2] = max(p[2], 0.0)
        return p

    def scansioni(self, ver, t_fine, rng, segnatura, coop_stato=None, cue=None, fase=None):
        """ver: {id: (T, P, V)} verita' a passo fisso. segnatura(id, tipo) -> rcs (radar, lidar) o dimensione (camera).
        coop_stato(id, t) -> bool (trasmette). cue(id, t) -> bool (camera orientata dal radar su quell'oggetto).
        Ritorna una lista di record {t, t_consegna, sensore, salute, ril: [(id_vero|None, z, R, extra)]}."""
        per = self.par["periodo_s"]
        fase = rng.uniform(0, per) if fase is None else fase
        out = []
        t = fase
        while t <= t_fine:
            g = self.guasto(t)
            if g == "spento":
                t += per
                continue
            rec = {"t": round(t, 4), "t_consegna": round(t + self.par.get("latenza_s", 0.0), 4), "sensore": self.nome,
                   "salute": {"fondo_db": 0.0, "saturi": 0.0}, "ril": []}
            if g == "pioggia_forte" and self.tipo == "radar":
                rec["salute"]["fondo_db"] = 8.0             # indicatore (01-effetti: fondo > +6 dB)
            if g == "abbagliamento" and self.tipo == "camera":
                rec["salute"]["saturi"] = 0.3               # indicatore (01-effetti: pixel saturi > 0,05)
            for oid, (T, P, V) in ver.items():
                if self.tipo == "radar" and self.par.get("rotante"):
                    # antenna che gira: l'oggetto e' 'illuminato' alla frazione di giro del suo azimut
                    i0 = min(int(round(t / (T[1] - T[0]))), len(T) - 1)
                    az = math.atan2(P[i0, 1] - self.pos[1], P[i0, 0] - self.pos[0]) % (2 * math.pi)
                    ti = t - per + per * az / (2 * math.pi)
                else:
                    ti = t
                if ti < T[0] or ti > T[-1]:
                    continue
                i = min(int(round((ti - T[0]) / (T[1] - T[0]))), len(T) - 1)
                p, v = P[i], V[i]
                if self.tipo == "cooperativa":
                    if coop_stato is None or not coop_stato(oid, ti) or rng.random() > self.par["pd_msg"]:
                        continue
                    if np.linalg.norm(p - self.pos) > self.par["portata_m"]:
                        continue
                    if not in_vista(self.pos, p, self.ostacoli):
                        continue
                    j = max(0, i - int(round(self.par["lat_non_comp_s"] / (T[1] - T[0]))))
                    sp = np.array([self.par["sigma_pos_m"]] * 2 + [self.par.get("sigma_z_m", self.par["sigma_pos_m"])])
                    z = P[j] + sp * rng.standard_normal(3)
                    vz = V[j] + self.par["sigma_vel_ms"] * rng.standard_normal(3)
                    rec["ril"].append((oid, z, np.diag(sp ** 2), {"vel": vz, "R_vel": self.par["sigma_vel_ms"] ** 2 * np.eye(3), "id_coop": "C-" + oid, "t_ril": ti}))
                    continue
                if g == "abbagliamento" and self.tipo == "camera":
                    continue
                if not self.visibile(p, ti):
                    continue
                r = float(np.linalg.norm(p - self.pos))
                if self.tipo == "camera":
                    if cue is not None and not cue(oid, ti):
                        continue
                    pd = self.par["pd_in"] if r <= portata_camera(self.par, segnatura(oid, "camera")) else 0.0
                else:
                    if self.par.get("v_rad_min") and abs(float(v @ (p - self.pos)) / max(r, 1e-6)) < self.par["v_rad_min"]:
                        continue                         # radar Doppler: bersaglio a velocita' radiale nulla filtrato
                    pd = float(pd_swerling(self.par, r, segnatura(oid, self.tipo)))
                    if g == "pioggia_forte":
                        pd = float(pd_swerling(scala_meteo(self.par, 0.7), r, segnatura(oid, self.tipo)))
                if rng.random() < pd:
                    z, R, pol = self._misura(p, rng)
                    rec["ril"].append((oid, z, R, {"t_ril": ti, "pol": pol}))
            for _ in range(rng.poisson(self.par.get("falsi_per_passata", 0.0))):
                p = self._falso(rng)
                if p is not None and (self.tipo != "camera"):
                    z, R, pol = self._misura(p, rng)
                    rec["ril"].append((None, z, R, {"t_ril": t, "pol": pol}))
            out.append(rec)
            t += per
        return out

    @property
    def nome_tipo(self):
        return self.base.get("nome_tipo", "")


# ----------------------------------------------------------------------------- verita'
def genera_verita(ogg, comportamento, fattore_v, rng, dt=0.1, t_fine=None, nascosto=None, a_lat=None, v_retro=None,
                  t_innesco=None):
    """Traiettoria vera dai 'punti' dello scenario, a velocita' di tratto * fattore_v (<= v_max), accelerazione
    limitata a a_max. comportamento: nominale | rallenta | ferma | vira | indietro, innescato al primo istante in
    cui nascosto(p) e' vero (ingresso nell'ombra) o a t_innesco. Ritorna T, P, V (passo dt)."""
    pts = [np.asarray(p, float) for p in ogg["punti"]]
    vs = [min(v * fattore_v, ogg["v_max"]) for v in ogg["v"]]
    a_max, v_max = ogg["a_max"], ogg["v_max"]
    a_lat = a_lat or a_max
    t0 = ogg.get("t0", 0.0)
    durata = sum(np.linalg.norm(pts[i + 1] - pts[i]) / vs[i] for i in range(len(vs)))
    t_fine = t_fine or (t0 + durata * 1.6 + 20)
    n = int(round(t_fine / dt)) + 1
    T = np.arange(n) * dt
    P, V = np.zeros((n, 3)), np.zeros((n, 3))
    p = pts[0].copy()
    seg, verso = 0, 1
    u = (pts[1] - pts[0]) / max(np.linalg.norm(pts[1] - pts[0]), 1e-9)
    v = vs[0] * u if t0 <= 0 else np.zeros(3)
    stato, t_stato, om, girato = "nominale", None, 0.0, 0.0
    for k in range(n):
        t = T[k]
        if t >= t0:
            if stato == "nominale" and comportamento != "nominale":
                trig = (t_innesco is not None and t >= t_innesco) or (t_innesco is None and nascosto is not None and nascosto(p, t))
                if trig:
                    stato, t_stato = comportamento, t
                    om = (1 if rng.random() < 0.5 else -1) * a_lat / max(np.linalg.norm(v), 1.0)
            # comando di velocita'
            if seg < len(vs) and 0 <= seg:
                dest = pts[seg + 1] if verso > 0 else pts[seg]
                dirz = dest - p
                dist = float(np.linalg.norm(dirz))
                u = dirz / max(dist, 1e-9)
                vc = vs[seg]
            else:
                u, vc, dist = np.zeros(3), 0.0, 0.0
            if stato == "rallenta":
                vc *= 0.3
            elif stato == "ferma":
                vc = 0.0 if t - t_stato < 15.0 else vc
            elif stato == "indietro":
                if verso > 0 and np.linalg.norm(v) < 0.2:
                    verso = -1
                vc = 0.0 if verso > 0 else min(vc, v_retro or vc)
            if stato == "vira" and girato < math.pi / 2:
                c, s = math.cos(om * dt), math.sin(om * dt)
                v = np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], v[2]])
                girato += abs(om * dt)
                vn = v
            else:
                vdes = u * vc
                dv = vdes - v
                ndv = float(np.linalg.norm(dv))
                lim = (a_max if stato == "nominale" else max(a_max, a_lat)) * dt
                vn = v + (dv if ndv <= lim else dv / ndv * lim)
            sp = float(np.linalg.norm(vn))
            if sp > v_max:
                vn = vn * v_max / sp
            p = p + 0.5 * (v + vn) * dt
            v = vn
            p[2] = max(p[2], 0.0)
            if seg < len(vs) and dist < max(np.linalg.norm(v) * dt * 1.5, 0.5):
                seg += verso
                if seg < 0:
                    seg = len(vs)
        P[k], V[k] = p, v
    return T, P, V


# ----------------------------------------------------------------------------- verifica del simulatore
def verifica(n=4000, seme=12345):
    """V1-V5: statistiche attese e ottenute, su un solo oggetto fermo per fascia di distanza."""
    from movi_lp_import import wilson
    rng = np.random.default_rng(seme)
    cat = catalogo()
    ris = {"V1_pd": {}, "V2_rumore": {}, "V3_falsi": {}, "V4_geometria": {}, "V5_cooperativi": {}}
    tot_f, ok_f = 0, 0
    for nome in ("radar_sorveglianza_droni", "radar_movimento_a_terra", "radar_4d_auto", "lidar_auto_campo_largo", "lidar_tele"):
        par = dict(cat[nome], falsi_per_passata=0.0)
        rcs = par["rcs_rif_m2"]
        righe = []
        for f in (0.3, 0.6, 0.9, 1.0, 1.2, 1.5):
            r = min(par["r_rif_m"] * f, par["r_max_m"] * 0.999)
            p = np.array([r * math.cos(0.1), r * math.sin(0.1), 10.0 + 0.02 * r])
            s = SensoreSim(nome, [0, 0, 10.0], par)
            T = np.array([0.0, 0.1])
            vr = 5.0 * (p - np.array([0, 0, 10.0])) / np.linalg.norm(p - np.array([0, 0, 10.0]))
            ver = {"x": (T, np.stack([p, p]), np.stack([vr, vr]))}   # 5 m/s radiali: il radar 4D filtra i fermi
            m_err = []
            pd_mod = float(pd_swerling(par, np.linalg.norm(p - s.pos), rcs)) if s.visibile(p, 0.0) else 0.0
            # rilevamenti veri generati dal simulatore (non dalla formula sopra)
            recs = []
            for j in range(n // 2):
                recs += SensoreSim(nome, [0, 0, 10.0], dict(par, periodo_s=0.1, rotante=False), ).scansioni(ver, 0.1, np.random.default_rng([seme, int(f * 10), j]), lambda i, t: rcs, fase=0.0)[:1]
            kk = sum(len(rc["ril"]) for rc in recs)
            nn = len(recs)
            lo, hi = wilson(kk, nn)
            tot_f += 1
            ok_f += lo <= pd_mod <= hi
            for rc in recs:
                for (_, z, R, ex) in rc["ril"]:
                    m_err.append([ex["pol"][0] - np.linalg.norm(z - s.pos)])
            righe.append({"r_m": round(r), "pd_modello": round(pd_mod, 4), "k": kk, "n": nn, "wilson95": [round(lo, 4), round(hi, 4)]})
        ris["V1_pd"][nome] = righe
        # V2: rumore in distanza e angolo (sigma dichiarate) su 4000 misure a meta' portata
        s = SensoreSim(nome, [0, 0, 10.0], par)
        p = np.array([0.5 * par["r_rif_m"], 0.0, 10.0])
        dr, da = [], []
        for _ in range(n):
            z, R, pol = s._misura(p, rng)
            d = z - s.pos
            er = (p - s.pos) / np.linalg.norm(p - s.pos)
            dr.append(float((z - p) @ er))                 # errore proiettato sulla direzione radiale
            da.append(math.atan2(d[1], d[0]))
        ris["V2_rumore"][nome] = {"sigma_r_dich": par["sigma_r_m"], "sigma_r_ott": round(float(np.std(dr)), 4),
                                  "sigma_az_dich_rad": par["sigma_az_rad"], "sigma_az_ott_rad": round(float(np.std(da)), 6),
                                  "rapporto_r": round(float(np.std(dr)) / par["sigma_r_m"], 3), "rapporto_az": round(float(np.std(da)) / par["sigma_az_rad"], 3)}
        # V3: falsi per passata
        s = SensoreSim(nome, [0, 0, 10.0], dict(cat[nome], periodo_s=1.0, rotante=False))
        recs = s.scansioni({}, 5 * n - 1.0, np.random.default_rng([seme, 99, len(nome)]), lambda i, t: rcs, fase=0.0)
        nf = [len(rc["ril"]) for rc in recs]
        lam = cat[nome]["falsi_per_passata"]
        mu = float(np.mean(nf))
        se = math.sqrt(lam / len(nf))
        ris["V3_falsi"][nome] = {"lambda_modello": lam, "media_ottenuta": round(mu, 4), "n_passate": len(nf),
                                 "intervallo95": [round(lam - 1.96 * se, 4), round(lam + 1.96 * se, 4)], "dentro": bool(abs(mu - lam) <= 1.96 * se)}
    ris["V1_pd"]["fasce_dentro_wilson"] = [ok_f, tot_f]
    # V4: geometria
    ost = ostacoli_da_poligoni([{"poligono": [[100, -50], [120, -50], [120, 50], [100, 50]], "altezza": 30}])
    s = SensoreSim("r", [0, 0, 10.0], dict(cat["radar_sorveglianza_droni"], falsi_per_passata=0.0), ostacoli=ost)
    viol = {"dietro_ostacolo": 0, "oltre_orizzonte": 0, "sotto_quota_minima": 0, "fuori_campo": 0}
    T = np.array([0.0, 0.1])
    casi = {"dietro_ostacolo": np.array([200.0, 0.0, 20.0]), "oltre_orizzonte": np.array([11900.0, 0.0, 0.5])}
    for k, p in casi.items():
        ver = {"x": (T, np.stack([p, p]), np.zeros((2, 3)))}
        for j in range(500):
            viol[k] += sum(len(rc["ril"]) for rc in s.scansioni(ver, 0.05, np.random.default_rng([seme, 7, j]), lambda i, t: 100.0, fase=0.0))
    sa = SensoreSim("a", [0, 0, 10.0], dict(cat["radar_aeroporto"], falsi_per_passata=0.0))
    p = np.array([3000.0, 0.0, 150.0])
    ver = {"x": (T, np.stack([p, p]), np.zeros((2, 3)))}
    for j in range(500):
        viol["sotto_quota_minima"] += sum(len(rc["ril"]) for rc in sa.scansioni(ver, 0.05, np.random.default_rng([seme, 8, j]), lambda i, t: 100.0, fase=0.0))
    sl = SensoreSim("l", [0, 0, 10.0], dict(cat["lidar_tele"], falsi_per_passata=0.0))
    p = np.array([100.0, 30.0, 10.0])                     # 16,7 gradi: fuori dai 7,25
    ver = {"x": (T, np.stack([p, p]), np.zeros((2, 3)))}
    for j in range(500):
        viol["fuori_campo"] += sum(len(rc["ril"]) for rc in sl.scansioni(ver, 0.05, np.random.default_rng([seme, 9, j]), lambda i, t: 100.0, fase=0.0))
    ris["V4_geometria"] = {"rilevamenti_vietati": viol, "prove_per_caso": 500}
    # V5: cooperativi
    sc = SensoreSim("c", [0, 0, 10.0], cat["ads_b"])
    T = np.arange(0, 1000.1, 0.1)
    P = np.tile([2000.0, 0.0, 300.0], (len(T), 1))
    ver = {"x": (T, P, np.zeros_like(P))}
    for modo, f in (("presente", lambda i, t: True), ("assente", lambda i, t: False), ("intermittente", lambda i, t: (t % 20) < 10)):
        recs = sc.scansioni(ver, 1000.0, np.random.default_rng([seme, 10]), None, coop_stato=f, fase=0.0)
        k = sum(len(rc["ril"]) for rc in recs)
        ris["V5_cooperativi"][modo] = {"messaggi": k, "passate": len(recs), "quota": round(k / len(recs), 4),
                                       "attesa": {"presente": 0.9, "assente": 0.0, "intermittente": 0.45}[modo]}
    return ris


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    r = verifica()
    with open(os.path.join(QUI, "verifica_simulatore.json"), "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=1, default=float)
    print(json.dumps(r, ensure_ascii=False, default=float)[:4000])
