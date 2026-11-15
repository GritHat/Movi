"""stima_v5.py — estensione di f19-volo/03-confidenza/stima_v4.py (che resta intatto e viene importato):
(1) quarto regime IMM «accelerazione longitudinale» (CAL): stato p,v,a con strappo bianco anisotropo,
    densità q_long lungo la direzione della velocità e q_perp di traverso: Q = kron(J(dt), D), D = q_long·uuᵀ + q_perp(I−uuᵀ);
(2) previsione durante la perdita a PESI FISSATI (μ congelati all'istante della perdita, regimi propagati ciascuno per sé);
(3) σ_rif² (rumore della verità e del sensore simulato) sommata al blocco di posizione di ogni regime;
(4) C monotona per costruzione: minimo progressivo C̃(τ) = min_{s≤τ} C(s) (solo prudente)."""
import math, os, sys
import numpy as np
sys.path.insert(0, "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f19-volo/03-confidenza")
import stima_v4 as S4

NOMI4 = ["cv", "ct", "ca", "cal"]
PARAM_CAL = {"aerei_veloci": dict(q_long=0.5, q_perp=0.005), "droni_ala_fissa": dict(q_long=1.0, q_perp=0.02),
             "multirotori": dict(q_long=1.0, q_perp=0.05)}        # IPOTESI di partenza, scalate col fattore tarato


def Q_cal(x, dt, p):
    v = x[3:6]; n = np.linalg.norm(v)
    u = v / n if n > 1e-3 else np.array([1.0, 0, 0])
    D = p["q_long"] * np.outer(u, u) + p["q_perp"] * (np.eye(3) - np.outer(u, u))
    Q = np.zeros((10, 10))
    Q[:9, :9] = np.kron(S4._jerk(dt, 1.0), D)
    Q[9, 9] = p["q_w"] * dt
    return Q


def predici4(j, x, P, dt, p):
    if j < 3: return S4.predici_modello(j, x, P, dt, p)
    F = S4.F_ca(dt); return F @ x, F @ P @ F.T + Q_cal(x, dt, p)


def parametri(cl, f):
    p = S4.scala_parametri(S4.PARAMETRI_BASE[cl], f)
    p.update({k: v * f for k, v in PARAM_CAL[cl].items()})
    return p


class IMM4(S4.IMM):
    def __init__(self, z, R, t, p, mu0=(0.7, 0.1, 0.1, 0.1)):
        self.p, self.t = p, t
        x = np.zeros(10); x[:3] = z
        P = np.diag([R[0, 0], R[1, 1], R[2, 2]] + [p["sv0"] ** 2] * 3 + [p["a_prior"] ** 2] * 3 + [0.05 ** 2])
        self.x = [x.copy() for _ in NOMI4]; self.P = [P.copy() for _ in NOMI4]
        self.mu = np.array(mu0, float)

    def Pi(self, dt):
        ps = math.exp(-dt / self.p["T_soggiorno"]); M = np.full((4, 4), (1 - ps) / 3); np.fill_diagonal(M, ps); return M

    def _interazione(self, dt):
        M = self.Pi(dt); c = M.T @ self.mu
        W = (M * self.mu[:, None]) / np.maximum(c[None, :], 1e-300)
        xs, Ps = [], []
        for j in range(4):
            x0 = sum(W[i, j] * self.x[i] for i in range(4))
            Ps.append(sum(W[i, j] * (self.P[i] + np.outer(self.x[i] - x0, self.x[i] - x0)) for i in range(4))); xs.append(x0)
        return c, xs, Ps

    def prevedi(self, t):
        dt = t - self.t
        if dt <= 0: return
        c, xs, Ps = self._interazione(dt)
        for j in range(4): self.x[j], self.P[j] = predici4(j, xs[j], Ps[j], dt, self.p)
        self.mu = c / c.sum(); self.t = t

    def aggiorna(self, z, R, H=None):
        H = np.eye(10)[:3] if H is None else H
        lik = np.zeros(4)
        for j in range(4):
            nu = z - H @ self.x[j]; Sm = H @ self.P[j] @ H.T + R; Si = np.linalg.inv(Sm)
            K = self.P[j] @ H.T @ Si; IK = np.eye(10) - K @ H
            self.x[j] = self.x[j] + K @ nu; self.P[j] = IK @ self.P[j] @ IK.T + K @ R @ K.T
            lik[j] = math.exp(-0.5 * min(nu @ Si @ nu, 700)) / math.sqrt(max(np.linalg.det(2 * math.pi * Sm), 1e-300))
        m = self.mu * lik
        self.mu = m / m.sum() if m.sum() > 0 else self.mu

    def media(self): return sum(self.mu[j] * self.x[j] for j in range(4))

    def copia(self):
        n = IMM4.__new__(IMM4); n.p, n.t, n.mu = self.p, self.t, self.mu.copy()
        n.x = [x.copy() for x in self.x]; n.P = [P.copy() for P in self.P]; return n


def predizione_pesi_fissati(f, taus, passo=1.0):
    """Durante la perdita: μ congelati, ciascun regime propagato col suo modello (nessuna interazione)."""
    mu = f.mu.copy(); xs = [x.copy() for x in f.x]; Ps = [P.copy() for P in f.P]; t = 0.0; out = []
    for tau in sorted(taus):
        while t < tau - 1e-9:
            h = min(passo, tau - t)
            for j in range(len(xs)): xs[j], Ps[j] = predici4(j, xs[j], Ps[j], h, f.p)
            t += h
        out.append((tau, mu.copy(), [x.copy() for x in xs], [P.copy() for P in Ps]))
    return out


def con_rif(mix, srif):
    mu, xs, Ps = mix
    Q = []
    for P in Ps:
        P = P.copy(); P[:3, :3] += srif ** 2 * np.eye(3); Q.append(P)
    return mu, xs, Q


def minimo_progressivo(C):
    out, m = [], 1.0
    for c in C: m = min(m, c); out.append(m)
    return out
