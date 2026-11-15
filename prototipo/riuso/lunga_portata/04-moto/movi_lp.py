"""movi_lp.py — nucleo di riferimento delle regole di MoVi a lunga portata (f15/04-moto).

Solo numpy. Tutto e' simulazione o conto: niente e' provato su un sensore fisico.
Solo osservazione e avviso: nessuna funzione d'ingaggio o di puntamento.

Riferimento: terna locale fissa Est-Nord-Alto, metri, secondi. Azimut = atan2(y, x).

Interfaccia (vedi MODELLI_E_REGOLE.md):
  carica_regole(percorso)                      -> dict di regole_lunga_portata.json
  inviluppo(regole, classi)                    -> classe fittizia: il peggio di tutte
  Sensore(nome, pos, parametri)                .pd(distanza, rcs)  .portata(rcs, pd_cum, n)
  GrigliaPolare(sensore, ...)                  .passata(t, rilevamenti)  .stati(t, classi)  .stato_punto(p, t, classi)
  stato_fuso(griglie, p, t, classi)            -> uno dei quattro stati, su piu' sensori (classi = quelle ammesse)
  Inseguitore(regole, griglie)                 .aggiorna(misure)  .uscite(t)
  Misura(t, z, R, sensore, classe=None, vel=None, id_coop=None)
  raggio_raggiungibile(tau, v0, v_max, a_max)  ;  intervallo_binario(tau, v0, classe)
  insieme_presenza(traccia, t, regole, classi_scenario, binario=None)
  tara_regione(errori, livello)  ;  RegionePrevisione
  distanza_avviso(regole, classi, profilo)
"""
import json
import math
from collections import deque

import numpy as np

LIBERO, OCCUPATO, IN_OMBRA, NON_OSSERVATO = 0, 1, 2, 3
NOMI_STATO = ("libero", "occupato", "in_ombra", "non_osservato")
VISTA, NON_VISTA, PREVISTO_AMPIO, CHIUSA = "vista", "non vista", "previsto ampio", "non piu' rilevata"


def carica_regole(percorso):
    with open(percorso, encoding="utf-8") as f:
        return json.load(f)


def inviluppo(regole, classi):
    """Classe fittizia col peggio delle classi date: e' quella che usa l'avviso."""
    cs = [regole["classi"][c] for c in classi]
    return {"v_max": max(c["v_max"] for c in cs), "a_max": max(c["a_max"] for c in cs),
            "dec_max": max(c["dec_max"] for c in cs), "vincolo": "libero_3d",
            "rcs_m2": min(c["rcs_m2"] for c in cs)}


# ----------------------------------------------------------------------------- sensore
class Sensore:
    """Modello di rilevamento dalla scheda: Pd = Pfa^(1/(1+SNR)) (bersaglio fluttuante, Swerling 1),
    SNR = SNR_rif * (rcs/rcs_rif) * (r_rif/r)^esponente, zero oltre r_max."""

    def __init__(self, nome, pos, par):
        self.nome, self.pos, self.par = nome, np.asarray(pos, float), par
        self.snr_rif = math.log(par["pfa"]) / math.log(par["pd_rif"]) - 1.0

    def pd(self, r, rcs):
        r = np.maximum(np.asarray(r, float), 1e-3)
        snr = self.snr_rif * (rcs / self.par["rcs_rif_m2"]) * (self.par["r_rif_m"] / r) ** self.par["esponente"]
        return np.where(r <= self.par["r_max_m"], self.par["pfa"] ** (1.0 / (1.0 + snr)), 0.0)

    def portata(self, rcs, pd_cum=0.99, n=1):
        """Distanza massima a cui n passate senza ritorno danno Pd cumulata >= pd_cum."""
        pd1 = 1.0 - (1.0 - pd_cum) ** (1.0 / n)
        snr = math.log(self.par["pfa"]) / math.log(pd1) - 1.0
        r = self.par["r_rif_m"] * (self.snr_rif * rcs / self.par["rcs_rif_m2"] / snr) ** (1.0 / self.par["esponente"])
        return min(r, self.par["r_max_m"])

    def misura(self, p, rng=None):
        """Misura cartesiana (z, R) di un punto, dalle sigma polari della scheda."""
        d = np.asarray(p, float) - self.pos
        r = np.linalg.norm(d)
        az, el = math.atan2(d[1], d[0]), math.asin(d[2] / r)
        s = self.par
        er = np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
        ea = np.array([-math.sin(az), math.cos(az), 0.0])
        ee = np.cross(er, ea)
        B = np.stack([er, ea, ee], 1)
        sig = np.array([s["sigma_r_m"], r * math.cos(el) * s["sigma_az_rad"], r * s["sigma_el_rad"]])
        R = B @ np.diag(sig ** 2) @ B.T
        z = np.asarray(p, float) + (B @ (sig * rng.standard_normal(3)) if rng is not None else 0.0)
        return z, R


# ----------------------------------------------------------------------------- celle
def _incrocia(a, b, c, d):
    """Parametro s in (0,1) lungo a->b dove il segmento incrocia c->d (2D), o None. Vettoriale su b."""
    r, q = b - a, d - c
    den = r[..., 0] * q[1] - r[..., 1] * q[0]
    den = np.where(np.abs(den) < 1e-12, np.nan, den)
    ac = c - a
    s = (ac[0] * q[1] - ac[1] * q[0]) / den
    u = (ac[0] * r[..., 1] - ac[1] * r[..., 0]) / den
    ok = (s > 0) & (s < 1) & (u >= 0) & (u <= 1)
    return np.where(ok, s, np.nan)


class GrigliaPolare:
    """Celle distanza-azimut(-elevazione) di UN sensore, con i quattro stati.

    ostacoli: lista di ((x1,y1),(x2,y2), altezza) noti in pianta. maschera_terreno: array bool [nr,naz,nel]
    (True = coperta dal terreno), calcolata fuori. t_cumulo: finestra entro cui le passate si cumulano
    e oltre la quale un 'libero' scade."""

    def __init__(self, sensore, r_max, dr, n_az, el=(0.0,), ostacoli=(), maschera_terreno=None,
                 t_cumulo=5.0, n_passate_max=5, pd_cum_min=0.99, az_lim=(-math.pi, math.pi)):
        self.s, self.dr, self.t_cumulo, self.n_max, self.pd_min = sensore, dr, t_cumulo, n_passate_max, pd_cum_min
        self.r = np.arange(dr / 2, r_max, dr)
        self.az_lim, self.n_az = az_lim, n_az
        self.daz = (az_lim[1] - az_lim[0]) / n_az
        self.az = az_lim[0] + (np.arange(n_az) + 0.5) * self.daz
        self.el = np.asarray(el, float)
        self.del_ = (self.el[1] - self.el[0]) if len(self.el) > 1 else math.pi
        R, A, E = np.meshgrid(self.r, self.az, self.el, indexing="ij")
        self.forma = R.shape
        self.centri = sensore.pos + np.stack([R * np.cos(E) * np.cos(A), R * np.cos(E) * np.sin(A), R * np.sin(E)], -1)
        self.dist = R
        self.ombra = np.zeros(self.forma, bool) if maschera_terreno is None else maschera_terreno.copy()
        for (p1, p2, h) in ostacoli:
            s = _incrocia(sensore.pos[:2], self.centri[..., :2], np.asarray(p1, float), np.asarray(p2, float))
            z_inc = sensore.pos[2] + s * (self.centri[..., 2] - sensore.pos[2])
            self.ombra |= np.nan_to_num(z_inc, nan=np.inf) < h
        self.passate = deque()            # (t, illuminata[bool])
        self.t_ritorno = np.full(self.forma, -np.inf)
        self.affidabile = True
        self._cache = {}

    def indice(self, p):
        d = np.asarray(p, float) - self.s.pos
        r = np.linalg.norm(d)
        if r < 1e-9 or r >= self.r[-1] + self.dr / 2:
            return None
        ia = int(math.floor((math.atan2(d[1], d[0]) - self.az_lim[0]) / self.daz))
        if not 0 <= ia < self.n_az:
            return None
        ie = 0 if len(self.el) == 1 else int(round((math.asin(d[2] / r) - self.el[0]) / self.del_))
        if not 0 <= ie < len(self.el):
            return None
        return int(r // self.dr), ia, ie

    def passata(self, t, rilevamenti=(), settore=None):
        """Una passata al tempo t. settore: maschera bool delle celle illuminate (None = tutte).
        rilevamenti: punti (x,y,z) dei ritorni. L'ombra non e' mai illuminata."""
        ill = (np.ones(self.forma, bool) if settore is None else settore) & ~self.ombra
        for p in rilevamenti:
            i = self.indice(p)
            if i is not None and ill[i]:
                self.t_ritorno[i] = t
        self._cache = {}
        self.passate.append((t, ill))
        while len(self.passate) > self.n_max:
            self.passate.popleft()

    def perdi_affidabilita(self):
        """Affidabilita' persa: tutta la griglia torna 'non osservato' finche' non si chiama ripristina()."""
        self.affidabile = False
        self._cache = {}
        self.passate.clear()
        self.t_ritorno[:] = -np.inf

    def ripristina(self):
        self.affidabile = True

    def pd_cumulata(self, t, cls, dopo=-np.inf):
        """Pd cumulata, per la classe cls = {rcs_m2, v_max}, delle passate fresche SENZA ritorno, successive
        all'ultimo ritorno e a 'dopo'. Due cautele per gli oggetti che si muovono fra una passata e l'altra:
        (1) finestra per cella = min(t_cumulo, lato della cella / v_max della classe);
        (2) minimo sulla cella e sulle 8 vicine in distanza-azimut (chi era nella vicina puo' essere entrato)."""
        ch = (round(t, 6), cls["rcs_m2"], cls["v_max"], dopo)
        if ch in self._cache:
            return self._cache[ch]
        lato = np.minimum(self.dr, self.dist * self.daz)
        W = np.minimum(self.t_cumulo, lato / cls["v_max"])
        n = np.zeros(self.forma, int)
        for (tp, ill) in self.passate:
            if tp <= t and tp > dopo:
                n += ill & (tp > self.t_ritorno) & (tp >= t - W)
        pc = 1.0 - (1.0 - self.s.pd(self.dist, cls["rcs_m2"])) ** n
        giro = abs((self.az_lim[1] - self.az_lim[0]) - 2 * math.pi) < 1e-9
        e = np.concatenate([pc[:1], pc, np.zeros_like(pc[:1])], 0)                 # oltre la portata: 0
        e = np.concatenate([e[:, -1:], e, e[:, :1]], 1) if giro else np.pad(e, ((0, 0), (1, 1), (0, 0)))
        out = np.min([e[1 + a:e.shape[0] - 1 + a, 1 + b:e.shape[1] - 1 + b] for a in (-1, 0, 1) for b in (-1, 0, 1)], 0)
        if len(self._cache) > 64:
            self._cache = {}
        self._cache[ch] = out
        return out

    def stati(self, t, classi, dopo=-np.inf):
        """Stato di ogni cella. classi: una classe {rcs_m2, v_max} o la lista delle classi ammesse.
        REGOLA DEL LIBERO: libero <=> in vista, illuminata di fresco, nessun ritorno, e Pd cumulata >= soglia
        PER OGNI classe ammessa (ognuna con la sua sezione radar e la sua finestra)."""
        classi = [classi] if isinstance(classi, dict) else list(classi)
        st = np.full(self.forma, NON_OSSERVATO, np.int8)
        if not self.affidabile:
            return st
        st[self.ombra] = IN_OMBRA
        lib = ~self.ombra
        for c in classi:
            lib &= self.pd_cumulata(t, c, dopo) >= self.pd_min
        st[lib] = LIBERO
        ult = max((tp for tp, _ in self.passate), default=-np.inf)
        st[(self.t_ritorno >= ult) & (ult >= t - self.t_cumulo) & ~self.ombra] = OCCUPATO
        return st

    def non_osservato_per(self, t, classi, dopo=-np.inf):
        """Per ogni classe: maschera delle celle in vista che NON sono 'libere' per quella classe."""
        return {i: (self.pd_cumulata(t, c, dopo) < self.pd_min) & ~self.ombra for i, c in enumerate(classi)}

    def stato_punto(self, p, t, classi, dopo=-np.inf):
        i = self.indice(p)
        return NON_OSSERVATO if i is None else int(self.stati(t, classi, dopo)[i])


def stato_fuso(griglie, p, t, classi, dopo=-np.inf):
    """Stato di un punto su piu' sensori: occupato > libero > in ombra > non osservato.
    'libero' anche quando NESSUN sensore da solo basta ma, per ogni classe, la Pd cumulata congiunta dei
    sensori che lo vedono supera la soglia."""
    classi = [classi] if isinstance(classi, dict) else list(classi)
    st, manca, soglia = [], np.ones(len(classi)), 1.0
    for g in griglie:
        i = g.indice(p)
        if i is None or not g.affidabile:
            continue
        s = int(g.stati(t, classi, dopo)[i])
        st.append(s)
        if s != IN_OMBRA:
            manca *= [1.0 - float(g.pd_cumulata(t, c, dopo)[i]) for c in classi]
        soglia = min(soglia, 1.0 - g.pd_min)
    if OCCUPATO in st:
        return OCCUPATO
    if LIBERO in st or (st and manca.max() <= soglia):
        return LIBERO
    return IN_OMBRA if IN_OMBRA in st else NON_OSSERVATO


# ----------------------------------------------------------------------------- moto
def _F_cv(dt):
    F = np.eye(6)
    F[:3, 3:] = dt * np.eye(3)
    return F


def _F_ct(dt, om):
    """Virata coordinata nel piano orizzontale a velocita' angolare nota om; quota a velocita' costante."""
    F = _F_cv(dt)
    if abs(om * dt) > 1e-9:
        s, c = math.sin(om * dt), math.cos(om * dt)
        F[0, 3], F[0, 4], F[1, 3], F[1, 4] = s / om, -(1 - c) / om, (1 - c) / om, s / om
        F[3, 3], F[3, 4], F[4, 3], F[4, 4] = c, -s, s, c
    return F


def _Q(dt, q):
    """Rumore di processo ad accelerazione bianca, densita' q^2 [(m/s^2)^2 s]."""
    Q = np.zeros((6, 6))
    Q[:3, :3] = dt ** 3 / 3 * np.eye(3)
    Q[:3, 3:] = Q[3:, :3] = dt ** 2 / 2 * np.eye(3)
    Q[3:, 3:] = dt * np.eye(3)
    return q * q * Q


H_POS = np.hstack([np.eye(3), np.zeros((3, 3))])
H_PV = np.eye(6)


class Misura:
    def __init__(self, t, z, R, sensore, classe=None, vel=None, R_vel=None, id_coop=None):
        self.t, self.z, self.R, self.sensore, self.classe, self.id_coop = t, np.asarray(z, float), np.asarray(R, float), sensore, classe, id_coop
        self.vel, self.R_vel = (None if vel is None else np.asarray(vel, float)), R_vel


class Traccia:
    """Stato [x y z vx vy vz], covarianza, miscela di modelli (IMM)."""

    def __init__(self, ident, m, regole, classe_cfg):
        self.id, self.t, self.t_vista, self.t_nascita = ident, m.t, m.t, m.t
        self.classe = m.classe                    # etichetta A MANO; None = non classificato
        self.cfg = classe_cfg
        self.modelli = classe_cfg["modelli"]
        n = len(self.modelli)
        v0 = m.vel if m.vel is not None else np.zeros(3)
        P0 = np.zeros((6, 6))
        P0[:3, :3] = m.R
        P0[3:, 3:] = (m.R_vel if m.R_vel is not None else (classe_cfg["v_max"] / 2) ** 2 * np.eye(3))
        self.xs = [np.concatenate([m.z, v0]) for _ in range(n)]
        self.Ps = [P0.copy() for _ in range(n)]
        self.mu = np.full(n, 1.0 / n)
        self.Pi = np.full((n, n), 0.05 / max(n - 1, 1)) + (0.95 - 0.05 / max(n - 1, 1)) * np.eye(n) if n > 1 else np.eye(1)
        self.storia = deque([True], maxlen=regole["tracce"]["conferma_M_su_N"][1])
        self.confermata = False
        self.stato = VISTA
        self.log_manca = 0.0                      # somma di log(1-Pd) dei mancati rilevamenti IN VISTA
        self.ampio = False                        # una volta 'previsto ampio' non torna 'previsto'
        self.sensori = {m.sensore}
        self.id_coop = m.id_coop
        self.t_persa = None
        self.verificata = m.id_coop is None       # False finche' la vede solo la sorveglianza cooperativa
        self._misc()
        self._ricorda()

    def _ricorda(self):
        """Stima all'ultima misura: da qui partono l'insieme di possibile presenza e la zona."""
        self.p_ultima, self.v_ultima = self.x[:3].copy(), self.x[3:].copy()
        self.sigp_ultima = math.sqrt(max(np.linalg.eigvalsh(self.P[:3, :3])[-1], 0.0))
        self.sigv_ultima = math.sqrt(max(np.linalg.eigvalsh(self.P[3:, 3:])[-1], 0.0))

    def _misc(self):
        self.x = sum(w * x for w, x in zip(self.mu, self.xs))
        self.P = sum(w * (P + np.outer(x - self.x, x - self.x)) for w, x, P in zip(self.mu, self.xs, self.Ps))

    def _passo(self, nome, x, dt):
        v = max(float(np.hypot(x[3], x[4])), 0.2 * self.cfg["v_max"])
        om = self.cfg["a_lat"] / v
        if nome == "ct+":
            return _F_ct(dt, om), self.cfg["q_cv"]
        if nome == "ct-":
            return _F_ct(dt, -om), self.cfg["q_cv"]
        return _F_cv(dt), (self.cfg["q_manovra"] if nome == "cv_manovra" else self.cfg["q_cv"])

    def prevedi(self, t):
        dt = t - self.t
        if dt <= 0:
            return
        n = len(self.modelli)
        if n > 1:                                  # mescolamento IMM
            c = self.Pi.T @ self.mu
            W = (self.Pi * self.mu[:, None]) / c[None, :]
            x0 = [sum(W[i, j] * self.xs[i] for i in range(n)) for j in range(n)]
            P0 = [sum(W[i, j] * (self.Ps[i] + np.outer(self.xs[i] - x0[j], self.xs[i] - x0[j])) for i in range(n)) for j in range(n)]
            self.xs, self.Ps, self.mu = x0, P0, c
        for j, nome in enumerate(self.modelli):
            F, q = self._passo(nome, self.xs[j], dt)
            self.xs[j] = F @ self.xs[j]
            self.Ps[j] = F @ self.Ps[j] @ F.T + _Q(dt, q)
        self.t = t
        self._misc()

    def _hzr(self, m):
        if m.vel is not None:
            R = np.zeros((6, 6))
            R[:3, :3], R[3:, 3:] = m.R, m.R_vel
            return H_PV, np.concatenate([m.z, m.vel]), R
        return H_POS, m.z, m.R

    def distanza(self, m):
        """Distanza di Mahalanobis al quadrato, sulla sola posizione (porta a 3 gradi di liberta')."""
        S = H_POS @ self.P @ H_POS.T + m.R
        d = m.z - self.x[:3]
        return float(d @ np.linalg.solve(S, d))

    def aggiorna(self, m):
        H, z, R = self._hzr(m)
        L = np.zeros(len(self.modelli))
        for j in range(len(self.modelli)):
            S = H @ self.Ps[j] @ H.T + R
            nu = z - H @ self.xs[j]
            K = self.Ps[j] @ H.T @ np.linalg.inv(S)
            self.xs[j] = self.xs[j] + K @ nu
            A = np.eye(6) - K @ H
            self.Ps[j] = A @ self.Ps[j] @ A.T + K @ R @ K.T
            L[j] = math.exp(-0.5 * min(float(nu @ np.linalg.solve(S, nu)), 600.0)) / math.sqrt(np.linalg.det(2 * math.pi * S))
        self.mu = self.mu * L + 1e-300
        self.mu /= self.mu.sum()
        self._misc()
        self.t_vista, self.stato, self.log_manca, self.t_persa = m.t, VISTA, 0.0, None
        self.sensori.add(m.sensore)
        self.verificata = self.verificata or m.id_coop is None
        self._ricorda()
        if m.classe is not None:
            self.classe = m.classe


class Inseguitore:
    """Piu' sensori, frequenze diverse: le misure si fondono UNA ALLA VOLTA nell'ordine d'arrivo."""

    def __init__(self, regole, scenario, griglie=()):
        self.reg, self.griglie = regole, list(griglie)
        self.classi = regole["scenari"][scenario]["classi_ammesse"]
        self.inv = inviluppo(regole, self.classi)
        cfg0 = dict(self.inv, a_lat=max(regole["classi"][c]["a_lat"] for c in self.classi),
                    modelli=["cv", "ct+", "ct-", "cv_manovra"], q_cv=0.5, q_manovra=self.inv["a_max"])
        self.cfg_non_class = cfg0
        self.tracce, self.chiuse, self.eventi, self._prossimo = [], [], [], 1
        self.porta = regole["tracce"]["porta_chi2_3gdl"]
        self.porta_dubbio = regole["tracce"]["porta_dubbio_chi2_3gdl"]

    def _cfg(self, classe):
        return self.reg["classi"][classe] if classe in self.reg["classi"] else self.cfg_non_class

    def aggiorna(self, misure):
        """misure: lista di Misura. Si ordinano per tempo; le misure dello stesso sensore e istante si
        assegnano insieme (vicino piu' prossimo globale, goloso sul costo)."""
        misure = sorted(misure, key=lambda m: (m.t, m.sensore))
        i = 0
        while i < len(misure):
            j = i
            while j < len(misure) and misure[j].t == misure[i].t and misure[j].sensore == misure[i].sensore:
                j += 1
            self._gruppo(misure[i:j])
            i = j

    def _gruppo(self, ms):
        t = ms[0].t
        tol = self.reg["tracce"]["fuori_sequenza_tolleranza_s"]
        for tr in self.tracce:
            if t >= tr.t:
                tr.prevedi(t)
            elif tr.t - t > tol:
                self.eventi.append((t, "misura fuori sequenza scartata", ms[0].sensore))
                return
        tt = self.reg["tracce"]
        for tr in [x for x in self.tracce if not x.confermata and t - x.t_vista > tt["t_tentativa_s"]]:
            self.tracce.remove(tr)                # tentativa mai confermata: tolta (non era un avviso)
        coppie, dubbia = [], {}
        for a, tr in enumerate(self.tracce):
            for b, m in enumerate(ms):
                if m.id_coop is not None and tr.id_coop is not None and m.id_coop != tr.id_coop:
                    continue
                d2 = tr.distanza(m)
                if self.porta < d2 <= self.porta_dubbio and tr.confermata:
                    dubbia.setdefault(b, tr)
                if d2 <= self.porta:
                    coppie.append((d2 - (1e6 if m.id_coop is not None and m.id_coop == tr.id_coop else 0), a, b))
        usa_t, usa_m = set(), set()
        for d2, a, b in sorted(coppie):
            if a in usa_t or b in usa_m:
                continue
            usa_t.add(a)
            usa_m.add(b)
            tr = self.tracce[a]
            tr.aggiorna(ms[b])
            if ms[b].id_coop is not None:
                tr.id_coop = ms[b].id_coop
            tr.storia.append(True)
            M = self.reg["tracce"]["conferma_M_su_N"][0]
            tr.confermata = tr.confermata or sum(tr.storia) >= M
        for b, m in enumerate(ms):
            if b in usa_m:
                continue
            if b in dubbia:
                # appena fuori porta di una traccia confermata: NON apre subito un doppione. Si scarta e si
                # annota; se succede n volte in poco tempo e' forse un secondo oggetto vicino: allora si apre.
                tr = dubbia[b]
                tr.dubbie = [x for x in getattr(tr, "dubbie", []) if t - x <= tt["dubbie_finestra_s"]] + [t]
                self.eventi.append((t, "misura dubbia", tr.id))
                if len(tr.dubbie) < tt["dubbie_per_aprire"]:
                    continue
                tr.dubbie = []
            if True:
                self.tracce.append(Traccia(self._prossimo, m, self.reg, self._cfg(m.classe)))
                self._prossimo += 1

    def mancato(self, t, sensore, traccia_id):
        """Il sensore ha passato al tempo t e NON ha rilevato la traccia (lo dice il chiamante, che sa quali
        tracce erano nel settore). In vista: accumula evidenza d'assenza, pesata con la Pd della classe piu'
        piccola. In ombra o fuori copertura: nessuna evidenza. La cooperativa non conta mai."""
        tr = next((x for x in self.tracce if x.id == traccia_id), None)
        if tr is None or sensore.par.get("tipo") == "cooperativa":
            return
        tr.prevedi(t)
        g = next((g for g in self.griglie if g.s is sensore), None)
        in_ombra = g is not None and (g.indice(tr.x[:3]) is None or g.ombra[g.indice(tr.x[:3])])
        if tr.stato == VISTA:
            tr.stato, tr.t_persa = NON_VISTA, tr.t_vista
        if in_ombra or (g is not None and not g.affidabile):
            return
        pd = float(sensore.pd(np.linalg.norm(tr.x[:3] - sensore.pos), self.inv["rcs_m2"]))
        tr.log_manca += math.log(max(1.0 - pd, 1e-12))
        tr.storia.append(False)
        if 1.0 - math.exp(tr.log_manca) >= self.reg["libero"]["pd_cumulata_min"] and not tr.ampio:
            tr.stato = CHIUSA
            self.eventi.append((t, "non piu' rilevata", tr.id))
            self.tracce.remove(tr)
            self.chiuse.append(tr)

    def affidabilita_persa(self, t, sensore):
        """Le tracce rette SOLO da quel sensore passano a 'previsto ampio' e non tornano 'previsto'."""
        self.eventi.append((t, "affidabilita' persa", sensore.nome))
        for g in self.griglie:
            if g.s is sensore:
                g.perdi_affidabilita()
        for tr in self.tracce:
            if tr.sensori <= {sensore.nome}:
                tr.ampio, tr.stato = True, PREVISTO_AMPIO
                tr.t_persa = tr.t_persa if tr.t_persa is not None else tr.t_vista

    def uscite(self, t, regioni=None, binario=None, eta_vista=None):
        """Le parole di MoVi per ogni traccia confermata. regioni: {classe: RegionePrevisione}.
        eta_vista: oltre questa eta' dell'ultima misura la traccia e' 'non vista' (default 2 periodi = 2 s)."""
        out = []
        eta_vista = 2.0 if eta_vista is None else eta_vista
        for tr in self.tracce:
            if not tr.confermata:
                continue
            tau = t - tr.t_vista
            if tr.stato == VISTA and tau > eta_vista:
                tr.stato, tr.t_persa = NON_VISTA, tr.t_vista
            r = {"id": tr.id, "classe": tr.classe or "non_classificato", "da_s": round(tau, 2), "pos": tr.x[:3].copy(),
                 "solo_cooperativa": not tr.verificata}
            if tr.stato == VISTA:
                r["parola"] = "vista" + (" (solo cooperativa: non verificata da un sensore)" if r["solo_cooperativa"] else "")
            else:
                ins = insieme_presenza(tr, t, self.reg, self.classi, binario)
                r["possibile_presenza"] = ins            # AVVISO: inviluppo dello scenario, mai l'etichetta
                reg = (regioni or {}).get(tr.classe)
                zona = reg.zona(tr, t) if (reg is not None and not tr.ampio) else None
                if zona is None or zona["raggio"] > self.reg["tracce"]["ampio_se_raggio_su_raggiungibile"] * ins["raggio"]:
                    tr.ampio = True
                if tr.ampio:
                    tr.stato = PREVISTO_AMPIO
                    r["parola"] = "previsto ampio"
                else:
                    r["parola"] = "non vista da %.0f s con zona" % tau
                    r["zona"] = zona
            out.append(r)
        return out


# ----------------------------------------------------------------------------- occlusione
def raggio_raggiungibile(tau, v0, v_max, a_max):
    """Massima distanza percorribile in tau partendo da velocita' v0, con |v|<=v_max e |a|<=a_max."""
    tau = np.asarray(tau, float)
    v0 = min(v0, v_max)
    ta = (v_max - v0) / a_max
    return np.where(tau <= ta, v0 * tau + 0.5 * a_max * tau ** 2, v0 * ta + 0.5 * a_max * ta ** 2 + v_max * (tau - ta))


def intervallo_binario(tau, v0, cfg):
    """Treno: [s_min, s_max] lungo il binario rispetto all'ultima posizione (v0 >= 0 nel verso di marcia)."""
    s_max = float(raggio_raggiungibile(tau, v0, cfg["v_max"], cfg["a_max"]))
    tf = v0 / cfg["dec_max"]
    if tau <= tf:
        s_min = v0 * tau - 0.5 * cfg["dec_max"] * tau ** 2
    else:
        s_min = v0 * tf / 2 - float(raggio_raggiungibile(tau - tf, 0.0, cfg.get("v_retro_max", cfg["v_max"]), cfg["dec_max"]))
    return s_min, s_max


def insieme_presenza(tr, t, regole, classi_scenario, binario=None):
    """Insieme di POSSIBILE PRESENZA al tempo t: e' l'avviso. Usa SEMPRE l'inviluppo dello scenario
    (mai l'etichetta); in piu' l'incertezza dell'ultima stima (k sigma) e la fascia di guardia.
    binario: polilinea [n,3] SOLO se lo scenario ammette soltanto classi vincolate al binario."""
    inv = inviluppo(regole, classi_scenario)
    tau = t - tr.t_vista
    k = regole["tracce"]["k_sigma_insieme"]
    sig_p, sig_v = tr.sigp_ultima, tr.sigv_ultima
    v0 = min(float(np.linalg.norm(tr.v_ultima)) + k * sig_v, inv["v_max"])
    w = regole["ombra"]["fascia_di_guardia_m"]
    solo_binario = binario is not None and all(regole["classi"][c]["vincolo"] == "binario" for c in classi_scenario)
    centro = tr.p_ultima.copy()
    if solo_binario:
        cfg = dict(inv, v_retro_max=max(regole["classi"][c].get("v_retro_max", 0) for c in classi_scenario))
        a, b = intervallo_binario(tau, v0, cfg)
        return {"tipo": "tratto di binario", "centro": centro, "s_min": a - k * sig_p - w, "s_max": b + k * sig_p + w,
                "raggio": max(abs(a), abs(b)) + k * sig_p + w, "tau": tau}
    return {"tipo": "sfera", "centro": centro, "tau": tau,
            "raggio": float(raggio_raggiungibile(tau, v0, inv["v_max"], inv["a_max"])) + k * sig_p + w}


def avviso_spegnibile(griglie, ins, t, classi, n_punti=400, rng=None):
    """L'avviso si spegne SOLO guardando: ogni punto campionato dell'insieme deve risultare 'libero' per la
    classe piu' piccola con passate successive alla perdita. Ritorna (bool, frazione libera)."""
    rng = rng or np.random.default_rng(0)
    d = rng.standard_normal((n_punti, 3))
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    pts = ins["centro"] + d * ins["raggio"] * rng.random((n_punti, 1)) ** (1 / 3)
    lib = np.mean([stato_fuso(griglie, p, t, classi, dopo=t - ins["tau"]) == LIBERO for p in pts])
    return bool(lib == 1.0), float(lib)


# ----------------------------------------------------------------------------- previsione
def tara_regione(errori, livello=0.90):
    """Quantile conforme: errori [n] -> raggio che copre 'livello' su un caso nuovo scambiabile."""
    e = np.sort(np.asarray(errori, float))
    k = min(int(math.ceil((len(e) + 1) * livello)), len(e)) - 1
    return float(e[k])


class RegionePrevisione:
    """Regione al livello dichiarato per UNA classe: sfera centrata sulla previsione a velocita' costante,
    raggio tarato per orizzonte. Oltre l'ultimo orizzonte tarato non dichiara niente (-> previsto ampio)."""

    def __init__(self, orizzonti, raggi, livello):
        self.tau, self.r, self.livello = np.asarray(orizzonti, float), np.asarray(raggi, float), livello

    def raggio(self, tau):
        if tau > self.tau[-1]:
            return None
        return float(np.interp(tau, np.concatenate([[0.0], self.tau]), np.concatenate([[0.0], self.r])))

    def zona(self, tr, t):
        tau = t - tr.t_vista
        r = self.raggio(tau)
        if r is None:
            return None
        # il raggio e' tarato sullo stato VERO: si allarga dell'incertezza della stima all'ultima misura
        return {"centro": tr.p_ultima + tr.v_ultima * tau, "raggio": r + 3.0 * (tr.sigp_ultima + tr.sigv_ultima * tau),
                "livello": self.livello}


def genera_traiettorie(cfg, rng, n=1, T=30.0, dt=0.1, piano=False):
    """Generatore SIMULATO di manovre limitate (non e' un dato): n traiettorie, accelerazione costante a
    tratti di durata casuale (media 5 s), |a|<=a_max, |v|<=v_max. Ritorna P, V di forma [n, passi, 3].
    Serve a tarare e a provare; va sostituito con traiettorie pubbliche."""
    m = int(round(T / dt)) + 1
    P, V = np.zeros((n, m, 3)), np.zeros((n, m, 3))

    def direzioni(k):
        d = rng.standard_normal((k, 3))
        if piano:
            d[:, 2] = 0
        return d / np.linalg.norm(d, axis=1, keepdims=True)

    V[:, 0] = direzioni(n) * cfg["v_max"] * rng.uniform(0.3, 0.9, (n, 1))
    a, resta = np.zeros((n, 3)), np.zeros(n)
    for i in range(1, m):
        c = resta <= 0
        k = int(c.sum())
        if k:
            a[c] = direzioni(k) * cfg["a_max"] * rng.random((k, 1)) * (rng.random((k, 1)) < 0.6)
            resta[c] = rng.exponential(5.0, k)
        resta -= dt
        vn = V[:, i - 1] + a * dt
        s = np.linalg.norm(vn, axis=1, keepdims=True)
        vn = vn * np.minimum(1.0, cfg["v_max"] / np.maximum(s, 1e-9))
        V[:, i] = vn
        P[:, i] = P[:, i - 1] + 0.5 * (V[:, i - 1] + vn) * dt
    return P, V


# ----------------------------------------------------------------------------- avviso
def distanza_avviso(regole, classi, profilo):
    """Distanza a cui l'avviso deve arrivare perche' chi lo riceve faccia in tempo. Usa l'inviluppo."""
    a, inv = regole["avviso"], inviluppo(regole, classi)
    p = a["profili_ricevente"][profilo]
    tr = a["tau_lat_s"] + p["T_r"] + p.get("T_collegamento", 0.0)
    if not p["v_ego"]:
        return inv["v_max"] * (tr + p["T_man"]) + a["w_m"]
    ve = p["v_ego"]
    return (ve + inv["v_max"]) * tr + ve ** 2 / (2 * p["a_fr"]) + inv["v_max"] * ve / p["a_fr"] + a["w_m"]


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 1.0
    p = k / n
    c, h = p + z * z / (2 * n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (c - h) / (1 + z * z / n)), min(1.0, (c + h) / (1 + z * z / n))
