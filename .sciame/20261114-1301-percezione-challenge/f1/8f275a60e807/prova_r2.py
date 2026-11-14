"""Prova di classe 2 per rovesciatore-2: durante l'occlusione, copertura dell'ellisse al 95% di un Kalman
a velocita' costante che prosegue alla cieca (catena della bozza) contro l'insieme raggiungibile
(disco v_max*tau attorno all'ultima osservazione, intersecato con la regione non osservata).
Python puro, seme fisso. Uso: python3 prova_r2.py
"""
import math
import random

FS = 15.0
T = 1.0 / FS
R_M = 0.05           # rumore di misura per asse, m
PAN_Y, PAN_HALF = 2.0, 0.75
RANGE_MAX = 6.0
Y_T = 4.0            # distanza della corsia del pedone
V_MAX = 2.5
CHI2_95 = 5.991
N = 2000
K = PAN_HALF / PAN_Y  # |x| <= K*y  => in ombra


def in_ombra(x, y):
    return y > PAN_Y and abs(x) <= K * y


def visibile(x, y):
    return (not in_ombra(x, y)) and math.hypot(x, y) <= RANGE_MAX


def traiettoria(rnd):
    """Restituisce la lista (t, x, y) a FS Hz. Manovra dentro l'ombra: 60% prosegue, 25% sosta, 15% torna."""
    v = min(1.8, max(0.8, rnd.gauss(1.3, 0.2)))
    x, y, vx = -4.0, Y_T, v
    u = rnd.random()
    manovra = "prosegue" if u < 0.60 else ("sosta" if u < 0.85 else "torna")
    x_man = rnd.uniform(-1.2, 1.2)
    sosta = rnd.uniform(2.0, 6.0)
    fatto, fermo_fino = False, -1.0
    out, t, vis_dopo = [], 0.0, 0.0
    entrato = False
    while t < 20.0:
        out.append((t, x, y))
        if in_ombra(x, y):
            entrato = True
        elif entrato:
            vis_dopo += T
            if vis_dopo > 1.0:
                break
        if not fatto and x >= x_man:
            fatto = True
            if manovra == "sosta":
                fermo_fino = t + sosta
            elif manovra == "torna":
                vx = -v
        if t < fermo_fino:
            cur = 0.0
        else:
            vx += rnd.gauss(0, 0.1) * T          # piccola irregolarita' del passo
            cur = vx
        x += cur * T
        t += T
    return out, manovra


class KF1:
    def __init__(self, q, r):
        self.q, self.r = q, r
        self.x, self.P = None, None
        self.n = 0

    def predict(self):
        q, x, P = self.q, self.x, self.P
        self.x = [x[0] + T * x[1], x[1]]
        p00 = P[0][0] + T * (P[1][0] + P[0][1]) + T * T * P[1][1] + q * T ** 3 / 3
        p01 = P[0][1] + T * P[1][1] + q * T ** 2 / 2
        p11 = P[1][1] + q * T
        self.P = [[p00, p01], [p01, p11]]

    def update(self, z):
        """Restituisce la log-verosimiglianza dell'innovazione."""
        if self.x is None:
            self.x = [z, 0.0]
            self.P = [[self.r, 0.0], [0.0, 4.0]]
            return None
        P = self.P
        s = P[0][0] + self.r
        y = z - self.x[0]
        k0, k1 = P[0][0] / s, P[1][0] / s
        self.x = [self.x[0] + k0 * y, self.x[1] + k1 * y]
        self.P = [[(1 - k0) * P[0][0], (1 - k0) * P[0][1]],
                  [P[1][0] - k1 * P[0][0], P[1][1] - k1 * P[0][1]]]
        return -0.5 * (math.log(2 * math.pi * s) + y * y / s)


def insegui(traj, q, rnd):
    """Fa girare il Kalman. Per ogni passo restituisce (tau, in_ombra, d2, xhat, yhat, vera, ll, salto)."""
    kx, ky = KF1(q, R_M ** 2), KF1(q, R_M ** 2)
    rows, t_last, ultimo = [], None, None
    for (t, x, y) in traj:
        if kx.x is not None:
            kx.predict()
            ky.predict()
        vis = visibile(x, y)
        ll, salto = None, False
        if vis:
            zx, zy = x + rnd.gauss(0, R_M), y + rnd.gauss(0, R_M)
            salto = t_last is not None and (t - t_last) > 1.5 * T
            a, b = kx.update(zx), ky.update(zy)
            if a is not None:
                ll = a + b
            t_last, ultimo = t, (zx, zy)
        if kx.x is None:
            continue
        d2 = (x - kx.x[0]) ** 2 / kx.P[0][0] + (y - ky.x[0]) ** 2 / ky.P[0][0]
        area = math.pi * CHI2_95 * math.sqrt(kx.P[0][0] * ky.P[0][0])
        rows.append((t - t_last, in_ombra(x, y), d2, kx.x[0], ky.x[0], (x, y), ll, salto, ultimo, area))
    return rows


def scegli_q(trajs, includi_riaggancio):
    best = None
    for q in (0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0):
        rnd = random.Random(7)
        tot = 0.0
        for traj, _ in trajs:
            for r in insegui(traj, q, rnd):
                if r[6] is not None and (includi_riaggancio or not r[7]):
                    tot += r[6]
        if best is None or tot > best[1]:
            best = (q, tot)
    return best[0]


def valuta(trajs, q):
    rnd = random.Random(11)
    n_occ = 0
    fuori = {"mai": 0, "1s": 0, "3s": 0}
    fuori_reach = 0
    fantasma = 0
    per_manovra = {}
    per_tau = {}
    for traj, man in trajs:
        pm = per_manovra.setdefault(man, [0, 0])
        for (tau, omb, d2, xh, yh, vera, ll, salto, ultimo, area) in insegui(traj, q, rnd):
            if not omb:
                continue
            n_occ += 1
            out = d2 > CHI2_95
            fuori["mai"] += out
            fuori["1s"] += out or tau > 1.0
            fuori["3s"] += out or tau > 3.0
            pm[0] += out
            pm[1] += 1
            b = per_tau.setdefault(int(tau), [0, 0, 0.0])
            b[0] += out
            b[1] += 1
            b[2] += area
            fantasma += visibile(xh, yh)
            r = V_MAX * tau + 3 * R_M
            fuori_reach += math.hypot(vera[0] - ultimo[0], vera[1] - ultimo[1]) > r
    return n_occ, fuori, fuori_reach, fantasma, per_manovra, per_tau


def area_raggiungibile():
    """Frazione dell'ombra (entro la portata) coperta dal disco v_max*tau centrato nel punto d'ingresso."""
    cx, cy, h = -K * Y_T, Y_T, 0.05
    celle = []
    yy = PAN_Y + h / 2
    while yy < RANGE_MAX:
        xx = -K * RANGE_MAX
        while xx < K * RANGE_MAX:
            if in_ombra(xx, yy) and math.hypot(xx, yy) <= RANGE_MAX:
                celle.append((xx, yy))
            xx += h
        yy += h
    tot = len(celle)
    res = []
    for i in range(1, 31):
        tau = i * 0.1
        r = V_MAX * tau + 3 * R_M
        dentro = sum(1 for (a, b) in celle if math.hypot(a - cx, b - cy) <= r)
        res.append((tau, dentro / tot, dentro * h * h))
    return tot * h * h, res


if __name__ == "__main__":
    rnd = random.Random(42)
    trajs = [traiettoria(rnd) for _ in range(N)]
    cont = {}
    for _, m in trajs:
        cont[m] = cont.get(m, 0) + 1
    print("traiettorie:", N, cont)
    for nome, inc in (("q tarato sui tratti visibili continui (PRIMARIA)", False),
                      ("q tarato includendo le innovazioni di riaggancio (sensibilita')", True)):
        q = scegli_q(trajs[:400], inc)
        n_occ, fuori, fr, fant, pm, pt = valuta(trajs, q)
        print("\n== %s: q = %g m^2/s^3" % (nome, q))
        print("secondi-bersaglio in occlusione: %.0f" % (n_occ * T))
        for k in ("mai", "1s", "3s"):
            print("  M1 fuori dall'ellisse 95%% (traccia cancellata: %s): %.1f%%" % (k, 100 * fuori[k] / n_occ))
        print("  M2 fuori dall'insieme raggiungibile: %.2f%%" % (100 * fr / n_occ))
        print("  (esplorativa) media prevista del Kalman in zona VISIBILE mentre il vero e' in ombra: %.1f%%" % (100 * fant / n_occ))
        for m, (a, b) in sorted(pm.items()):
            print("  per manovra %-9s fuori ellisse: %.1f%% (%d passi)" % (m, 100 * a / b, b))
        for k in sorted(pt):
            a, b, ar = pt[k]
            print("  tau in [%d,%d) s: fuori %.1f%%, area media ellisse %.1f m^2 (%d passi)" % (k, k + 1, 100 * a / b, ar / b, b))
    tot, res = area_raggiungibile()
    print("\nombra entro la portata: %.1f m^2" % tot)
    tstar = None
    for tau, fr, ar in res:
        if tstar is None and fr >= 0.90:
            tstar = tau
        if abs(tau * 10 % 5) < 1e-6 or abs(tau * 10 % 5 - 5) < 1e-6:
            print("  tau=%.1f s: raggiungibile∩ombra = %.1f m^2 = %.0f%% dell'ombra" % (tau, ar, 100 * fr))
    print("M3 tau* (>=90%% dell'ombra): %s s" % tstar)
