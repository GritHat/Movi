"""stima_v4.py — IMM (CV, virata coordinata con tasso stimato, accelerazione) e confidenza nel tempo dopo la perdita
di continuità (f19-volo/03-confidenza, sciame-kalman). Solo numpy. Solo osservazione, monitoraggio e avviso.

Stato comune (10): x = [px, py, pz, vx, vy, vz, ax, ay, az, w]   (m, m/s, m/s^2, rad/s; z = quota)
Regione: {x : (x_d - c)^T A^-1 (x_d - c) <= 1} sulle componenti di posizione d (2 o 3); c fisso o «previsione».

confidenza(...)  = probabilità che la posizione stia nella regione, per gaussiana e per miscela (somma pesata).
  - gaussiana: integrale ESATTO su ellisse/ellissoide ridotto a 1 (2D) o 2 (3D) integrali di Gauss-Legendre
    con sostituzione trigonometrica; errore di quadratura misurato in prove_confidenza.py (P1).
  - miscela IMM: somma pesata delle gaussiane dei regimi (esatta PER LA MISCELA; la miscela è un'approssimazione
    della vera densità a regimi commutanti: fusione dei momenti e linearizzazione della virata).
Forme chiuse (centrata, isotropa): 2D C = 1 - exp(-r^2/2s^2); 3D C = erf(k/sqrt2) - sqrt(2/pi) k exp(-k^2/2), k = r/s;
s^2(tau) = s0^2 + 2 s0v tau + sv^2 tau^2 + q tau^3/3 (velocità quasi costante, densità q).
"""
import json
import math
import numpy as np

S2 = math.sqrt(2.0)


# ---------------------------------------------------------------- funzioni speciali (solo numpy)
def erfc(x):
    """erfc con errore relativo < 1.2e-7 (Chebyshev, Numerical Recipes 'erfcc')."""
    x = np.asarray(x, float)
    z = np.abs(x)
    t = 1.0 / (1.0 + 0.5 * z)
    y = t * np.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (
        -0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))))
    return np.where(x >= 0, y, 2.0 - y)


def Phi(x):
    return 0.5 * erfc(-np.asarray(x, float) / S2)


_GL = {}


def _gl(n):
    if n not in _GL:
        _GL[n] = np.polynomial.legendre.leggauss(n)
    return _GL[n]


def _intervallo_theta(h, mu, sd, k=9.0):
    """Angoli [a,b] tali che x = h sin(theta) copra [-h,h] ∩ [mu-k sd, mu+k sd]."""
    lo = np.maximum(-h, mu - k * sd)
    hi = np.minimum(h, mu + k * sd)
    hh = np.where(h > 0, h, 1.0)
    a = np.arcsin(np.clip(lo / hh, -1, 1))
    b = np.arcsin(np.clip(hi / hh, -1, 1))
    return a, np.maximum(b, a)


def prob_palla_unitaria(mu, sd, n=64):
    """P(|z| <= 1) con z_i ~ N(mu_i, sd_i^2) indipendenti, d = 2 o 3. Integrazione esatta a meno della quadratura."""
    mu = np.asarray(mu, float)
    sd = np.maximum(np.asarray(sd, float), 1e-12)
    o = np.argsort(-sd)                     # esterno = asse più largo, interno analitico = asse più stretto
    mu, sd = mu[o], sd[o]
    x, w = _gl(n)
    a, b = _intervallo_theta(1.0, mu[0], sd[0])
    if b - a <= 0:
        return 0.0
    th = 0.5 * (b - a) * x + 0.5 * (b + a)
    wt = 0.5 * (b - a) * w
    z0 = np.sin(th)
    h1 = np.cos(th)                         # semicorda; dz0 = cos(th) dth
    f0 = np.exp(-0.5 * ((z0 - mu[0]) / sd[0]) ** 2) / (sd[0] * math.sqrt(2 * math.pi)) * h1
    if mu.size == 2:
        g = Phi((h1 - mu[1]) / sd[1]) - Phi((-h1 - mu[1]) / sd[1])
        return float(np.sum(wt * f0 * g))
    a1, b1 = _intervallo_theta(h1, mu[1], sd[1])                     # (n,)
    ph = 0.5 * (b1 - a1)[:, None] * x[None, :] + 0.5 * (b1 + a1)[:, None]
    wp = 0.5 * (b1 - a1)[:, None] * w[None, :]
    z1 = h1[:, None] * np.sin(ph)
    h2 = h1[:, None] * np.cos(ph)
    f1 = np.exp(-0.5 * ((z1 - mu[1]) / sd[1]) ** 2) / (sd[1] * math.sqrt(2 * math.pi)) * h2
    g = Phi((h2 - mu[2]) / sd[2]) - Phi((-h2 - mu[2]) / sd[2])
    inner = np.sum(wp * f1 * g, axis=1)
    return float(np.sum(wt * f0 * inner))


def prob_gauss_ellissoide(m, S, c, A, n=64):
    """P(x in {(x-c)^T A^-1 (x-c) <= 1}) per x ~ N(m, S). Esatta a meno della quadratura (vedi P1)."""
    L = np.linalg.cholesky(np.asarray(A, float))
    Li = np.linalg.inv(L)
    mp = Li @ (np.asarray(m, float) - np.asarray(c, float))
    Sp = Li @ np.asarray(S, float) @ Li.T
    l, U = np.linalg.eigh(0.5 * (Sp + Sp.T))
    return prob_palla_unitaria(U.T @ mp, np.sqrt(np.maximum(l, 0.0)), n)


# ---------------------------------------------------------------- forme chiuse e tempi
def sigma2_cv(tau, s0sq, s0v, svsq, q):
    tau = np.asarray(tau, float)
    return s0sq + 2 * s0v * tau + svsq * tau ** 2 + q * tau ** 3 / 3.0


def C_disco_centrato(r, s2):
    return 1.0 - np.exp(-np.asarray(r, float) ** 2 / (2 * np.asarray(s2, float)))


def C_sfera_centrata(r, s2):
    k = np.asarray(r, float) / np.sqrt(np.asarray(s2, float))
    return (1 - erfc(k / S2)) - math.sqrt(2 / math.pi) * k * np.exp(-0.5 * k * k)


def k_sfera(alfa):
    """k tale che C_sfera_centrata(k, 1) = alfa (bisezione; radice del chi-quadro a 3 gradi)."""
    lo, hi = 0.0, 20.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if C_sfera_centrata(mid, 1.0) < alfa:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def k_livello(alfa, d):
    return math.sqrt(-2 * math.log(1 - alfa)) if d == 2 else k_sfera(alfa)


def t_C(alfa, r, s0sq, s0v, svsq, q, d=2):
    """Tempo al quale la confidenza della regione (disco/sfera di raggio r centrata sulla previsione, covarianza
    isotropa per asse) scende sotto alfa: radice reale positiva della cubica q t^3/3 + sv^2 t^2 + 2 s0v t + s0^2 - (r/k)^2 = 0."""
    s2_lim = (r / k_livello(alfa, d)) ** 2
    if s0sq >= s2_lim:
        return 0.0
    rad = np.roots([q / 3.0, svsq, 2 * s0v, s0sq - s2_lim])
    rr = [z.real for z in rad if abs(z.imag) < 1e-9 * max(1, abs(z)) and z.real > 0]
    return float(min(rr)) if rr else float("inf")


def r_livello(alfa, tau, s0sq, s0v, svsq, q, d=2):
    """Raggio che tiene la confidenza alfa al tempo tau (la regione che cresce): r = k_alfa s(tau)."""
    return k_livello(alfa, d) * np.sqrt(sigma2_cv(tau, s0sq, s0v, svsq, q))


# ---------------------------------------------------------------- modelli
def _cwna(dt, q):
    return q * np.array([[dt ** 3 / 3, dt ** 2 / 2], [dt ** 2 / 2, dt]])


def _jerk(dt, q):
    return q * np.array([[dt ** 5 / 20, dt ** 4 / 8, dt ** 3 / 6], [dt ** 4 / 8, dt ** 3 / 3, dt ** 2 / 2],
                         [dt ** 3 / 6, dt ** 2 / 2, dt]])


def F_cv(dt):
    F = np.eye(10)
    for i in range(3):
        F[i, 3 + i] = dt
        F[6 + i, 6 + i] = 0.0               # accelerazione non usata: azzerata, varianza a priori in Q
    return F


def Q_cv(dt, p):
    Q = np.zeros((10, 10))
    for i in range(3):
        Q[np.ix_([i, 3 + i], [i, 3 + i])] = _cwna(dt, p["q_cv"])
        Q[6 + i, 6 + i] = p["a_prior"] ** 2
    Q[9, 9] = p["q_w"] * dt
    return Q


def F_ca(dt):
    F = np.eye(10)
    for i in range(3):
        F[i, 3 + i] = dt
        F[i, 6 + i] = dt ** 2 / 2
        F[3 + i, 6 + i] = dt
    return F


def Q_ca(dt, p):
    Q = np.zeros((10, 10))
    for i in range(3):
        Q[np.ix_([i, 3 + i, 6 + i], [i, 3 + i, 6 + i])] = _jerk(dt, p["q_ca"])
    Q[9, 9] = p["q_w"] * dt
    return Q


def f_ct(x, dt):
    """Virata coordinata nel piano orizzontale con tasso w stimato; quota a velocità costante."""
    y = x.copy()
    vx, vy, w = x[3], x[4], x[9]
    wt = w * dt
    if abs(w) > 1e-6:
        s, c = math.sin(wt), math.cos(wt)
        y[0] = x[0] + (vx * s - vy * (1 - c)) / w
        y[1] = x[1] + (vx * (1 - c) + vy * s) / w
    else:                                                       # limite w -> 0 (serie al primo ordine)
        s, c = wt, 1 - wt * wt / 2
        y[0] = x[0] + vx * dt - vy * w * dt * dt / 2
        y[1] = x[1] + vy * dt + vx * w * dt * dt / 2
    y[3] = vx * c - vy * s
    y[4] = vx * s + vy * c
    y[2] = x[2] + x[5] * dt
    y[6:9] = 0.0
    return y


def F_ct(x, dt):
    """Jacobiana analitica di f_ct (verificata alle differenze finite in prove_confidenza.py)."""
    F = np.zeros((10, 10))
    vx, vy, w = x[3], x[4], x[9]
    F[0, 0] = F[1, 1] = F[2, 2] = F[5, 5] = F[9, 9] = 1.0
    F[2, 5] = dt
    if abs(w) > 1e-6:
        s, c = math.sin(w * dt), math.cos(w * dt)
        F[0, 3], F[0, 4] = s / w, -(1 - c) / w
        F[1, 3], F[1, 4] = (1 - c) / w, s / w
        F[0, 9] = (vx * (dt * c * w - s) - vy * (dt * s * w - (1 - c))) / w ** 2
        F[1, 9] = (vx * (dt * s * w - (1 - c)) + vy * (dt * c * w - s)) / w ** 2
    else:
        s, c = w * dt, 1.0
        F[0, 3], F[0, 4] = dt, -w * dt * dt / 2
        F[1, 3], F[1, 4] = w * dt * dt / 2, dt
        F[0, 9], F[1, 9] = -vy * dt * dt / 2, vx * dt * dt / 2
    F[3, 3], F[3, 4], F[4, 3], F[4, 4] = c, -s, s, c
    F[3, 9] = -dt * (vx * s + vy * c)
    F[4, 9] = dt * (vx * c - vy * s)
    return F


def Q_ct(dt, p):
    Q = np.zeros((10, 10))
    for i in range(2):
        Q[np.ix_([i, 3 + i], [i, 3 + i])] = _cwna(dt, p["q_ct"])
    Q[np.ix_([2, 5], [2, 5])] = _cwna(dt, p["q_cv"])
    for i in range(3):
        Q[6 + i, 6 + i] = p["a_prior"] ** 2
    Q[9, 9] = p["q_w"] * dt
    return Q


NOMI = ["cv", "ct", "ca"]


def predici_modello(j, x, P, dt, p):
    if j == 0:
        F = F_cv(dt); return F @ x, F @ P @ F.T + Q_cv(dt, p)
    if j == 2:
        F = F_ca(dt); return F @ x, F @ P @ F.T + Q_ca(dt, p)
    F = F_ct(x, dt)
    return f_ct(x, dt), F @ P @ F.T + Q_ct(dt, p)


PARAMETRI_BASE = {   # IPOTESI: valori di partenza; il fattore di scala si tara sulla metà di taratura (per mezzo)
    "aerei_veloci": dict(q_cv=1.0, q_ct=0.3, q_ca=0.05, q_w=1e-5, a_prior=2.0, T_soggiorno=15.0, sv0=150.0),
    "droni_ala_fissa": dict(q_cv=0.5, q_ct=0.2, q_ca=0.2, q_w=1e-4, a_prior=3.0, T_soggiorno=10.0, sv0=40.0),
    "multirotori": dict(q_cv=0.3, q_ct=0.1, q_ca=0.3, q_w=1e-3, a_prior=3.0, T_soggiorno=10.0, sv0=20.0),
}


def scala_parametri(p, f):
    p = dict(p)
    for k in ("q_cv", "q_ct", "q_ca", "q_w"):
        p[k] *= f
    return p


# ---------------------------------------------------------------- filtri
class FiltroCV:
    """Kalman lineare a velocità quasi costante (riferimento). Aggiornamento in forma di Joseph."""

    def __init__(self, z, R, t, p):
        self.p = p
        self.t = t
        self.x = np.zeros(10); self.x[:3] = z
        self.P = np.diag([R[0, 0], R[1, 1], R[2, 2]] + [p["sv0"] ** 2] * 3 + [p["a_prior"] ** 2] * 3 + [1e-4])

    def prevedi(self, t):
        dt = t - self.t
        if dt > 0:
            self.x, self.P = predici_modello(0, self.x, self.P, dt, self.p)
            self.t = t

    def aggiorna(self, z, R, H=None):
        H = np.eye(10)[:3] if H is None else H
        nu = z - H @ self.x
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        I_KH = np.eye(10) - K @ H
        self.x = self.x + K @ nu
        self.P = I_KH @ self.P @ I_KH.T + K @ R @ K.T
        return float(nu @ np.linalg.solve(S, nu))

    def miscela(self):
        return np.array([1.0]), [self.x.copy()], [self.P.copy()]


class IMM:
    """IMM a tre regimi (CV, CT con tasso stimato, CA) su stato comune a 10 componenti."""

    def __init__(self, z, R, t, p, mu0=(0.8, 0.1, 0.1)):
        self.p = p
        self.t = t
        x = np.zeros(10); x[:3] = z
        P = np.diag([R[0, 0], R[1, 1], R[2, 2]] + [p["sv0"] ** 2] * 3 + [p["a_prior"] ** 2] * 3 + [0.05 ** 2])
        self.x = [x.copy() for _ in NOMI]
        self.P = [P.copy() for _ in NOMI]
        self.mu = np.array(mu0, float)

    def Pi(self, dt):
        ps = math.exp(-dt / self.p["T_soggiorno"])
        M = np.full((3, 3), (1 - ps) / 2)
        np.fill_diagonal(M, ps)
        return M

    def _interazione(self, dt):
        M = self.Pi(dt)
        c = M.T @ self.mu                                     # c_j = sum_i Pi_ij mu_i
        W = (M * self.mu[:, None]) / np.maximum(c[None, :], 1e-300)   # W[i,j] = mu_{i|j}
        xs, Ps = [], []
        for j in range(3):
            x0 = sum(W[i, j] * self.x[i] for i in range(3))
            P0 = sum(W[i, j] * (self.P[i] + np.outer(self.x[i] - x0, self.x[i] - x0)) for i in range(3))
            xs.append(x0); Ps.append(P0)
        return c, xs, Ps

    def prevedi(self, t):
        dt = t - self.t
        if dt <= 0:
            return
        c, xs, Ps = self._interazione(dt)
        for j in range(3):
            self.x[j], self.P[j] = predici_modello(j, xs[j], Ps[j], dt, self.p)
        self.mu = c / c.sum()
        self.t = t

    def aggiorna(self, z, R, H=None):
        H = np.eye(10)[:3] if H is None else H
        lik = np.zeros(3)
        nis = np.zeros(3)
        for j in range(3):
            nu = z - H @ self.x[j]
            S = H @ self.P[j] @ H.T + R
            Si = np.linalg.inv(S)
            K = self.P[j] @ H.T @ Si
            I_KH = np.eye(10) - K @ H
            self.x[j] = self.x[j] + K @ nu
            self.P[j] = I_KH @ self.P[j] @ I_KH.T + K @ R @ K.T
            nis[j] = nu @ Si @ nu
            lik[j] = math.exp(-0.5 * min(nis[j], 700)) / math.sqrt(max(np.linalg.det(2 * math.pi * S), 1e-300))
        m = self.mu * lik
        self.mu = m / m.sum() if m.sum() > 0 else self.mu
        return float(self.mu @ nis)

    def miscela(self):
        return self.mu.copy(), [x.copy() for x in self.x], [P.copy() for P in self.P]

    def media(self):
        return sum(self.mu[j] * self.x[j] for j in range(3))

    def copia(self):
        n = IMM.__new__(IMM)
        n.p, n.t, n.mu = self.p, self.t, self.mu.copy()
        n.x = [x.copy() for x in self.x]; n.P = [P.copy() for P in self.P]
        return n


def copia_cv(f):
    n = FiltroCV.__new__(FiltroCV)
    n.p, n.t, n.x, n.P = f.p, f.t, f.x.copy(), f.P.copy()
    return n


def predizione_senza_misure(filtro, taus, passo=1.0):
    """Previsione dopo la perdita: per ogni tau, la miscela (pesi, medie, covarianze). Per l'IMM la commutazione
    dei regimi continua secondo la catena di Markov (interazione a ogni passo)."""
    f = filtro.copia() if isinstance(filtro, IMM) else copia_cv(filtro)
    t0 = f.t
    out = []
    for tau in sorted(taus):
        while f.t < t0 + tau - 1e-9:
            f.prevedi(min(f.t + passo, t0 + tau))
        out.append((tau,) + f.miscela())
    return out


# ---------------------------------------------------------------- confidenza
def confidenza(miscela, regione, centro_previsione=None, n=64):
    """C = sum_j mu_j P_j(regione). regione = dict(dims=[0,1] o [0,1,2], A=matrice di forma, c=centro o None:
    se c è None la regione è centrata sulla media della miscela (regione che segue la previsione)."""
    mu, xs, Ps = miscela
    d = list(regione["dims"])
    if regione.get("c") is None:
        c = sum(mu[j] * xs[j][d] for j in range(len(mu))) if centro_previsione is None else centro_previsione
    else:
        c = np.asarray(regione["c"], float)
    return float(sum(mu[j] * prob_gauss_ellissoide(xs[j][d], Ps[j][np.ix_(d, d)], c, regione["A"], n)
                     for j in range(len(mu)) if mu[j] > 1e-9))


def raggio_per_livello(miscela, alfa, dims=(0, 1, 2), n=40, iter_=40):
    """Raggio della sfera/disco centrata sulla previsione che tiene la confidenza alfa (bisezione su log r)."""
    mu, xs, Ps = miscela
    d = list(dims)
    sc = math.sqrt(max(sum(mu[j] * np.trace(Ps[j][np.ix_(d, d)]) for j in range(len(mu))), 1e-12))
    m = sum(mu[j] * xs[j][d] for j in range(len(mu)))
    sc = max(sc, max(float(np.linalg.norm(xs[j][d] - m)) for j in range(len(mu))), 1e-6)
    lo, hi = math.log(sc * 1e-3), math.log(sc * 30)
    for _ in range(iter_):
        mid = 0.5 * (lo + hi)
        r = math.exp(mid)
        if confidenza(miscela, dict(dims=d, A=r * r * np.eye(len(d)), c=None), n=n) < alfa:
            lo = mid
        else:
            hi = mid
    return math.exp(0.5 * (lo + hi))


def curva_confidenza(filtro, regione, taus=None, livelli=(0.9, 0.5), passo=1.0, n=48):
    """Uscita per il registro del prototipo: curva C(tau) per la regione dichiarata, raggio r_alfa(tau) della regione
    che cresce, tempi t_C ai livelli. Stato: calcolato nel modello (gaussiano/miscela); vedi PERDITA_DI_CONFIDENZA.md."""
    taus = list(np.arange(0, 31, 1.0)) if taus is None else list(taus)
    taus = [max(t, 1e-3) for t in taus]
    pr = predizione_senza_misure(filtro, taus, passo)
    reg = dict(regione)
    if reg.get("c") is None:          # regione dichiarata alla perdita: fissata alla previsione a tau ~ 0
        m0 = pr[0]
        reg["c"] = sum(m0[1][j] * m0[2][j][list(reg["dims"])] for j in range(len(m0[1])))
    C = [confidenza(p[1:], reg, n=n) for p in pr]
    raggi = {str(a): [raggio_per_livello(p[1:], a, reg["dims"], n=32, iter_=30) for p in pr] for a in livelli}
    tC = {}
    for a in livelli:
        sotto = [t for t, c in zip(taus, C) if c < a]
        tC[str(a)] = float(sotto[0]) if sotto else None
    return {"tipo": "curva_confidenza", "versione": "stima_v4", "tau_s": [float(t) for t in taus],
            "C": [round(c, 6) for c in C], "regione": {"dims": list(reg["dims"]), "c": np.asarray(reg["c"]).tolist(),
                                                       "A": np.asarray(reg["A"]).tolist()},
            "raggio_livello_m": {k: [round(r, 3) for r in v] for k, v in raggi.items()},
            "t_C_s": tC, "pesi_regimi_ultimo": dict(zip(NOMI, [round(float(m), 4) for m in pr[-1][1]])) if len(pr[-1][1]) == 3 else {"cv": 1.0},
            "stato": "calcolato nel modello dichiarato (gaussiano o miscela IMM); non misurato su hardware"}


def riga_registro(curva):
    return json.dumps(curva, ensure_ascii=False)
