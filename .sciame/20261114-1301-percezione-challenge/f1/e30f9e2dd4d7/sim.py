#!/usr/bin/env python3
"""Prove di classe 2 del creativo (f1). Python puro, 1D, CPU. Parametri fissati prima dell'esecuzione."""
import math
import random

random.seed(20261114)
DT = 1 / 15      # passo (15 Hz)
SIG = 0.05       # sigma misura [m]
PD = 0.9         # probabilita' di rilevamento in vista
QA = 0.3         # sigma accelerazione del filtro [m/s^2]
SH0, SH1, XMAX = 3.0, 5.0, 10.0   # ombra dell'occlusore [3,5], campo fino a 10 m
PSTOP, PGO = 0.005, 0.01           # cambi di modo per passo (filtro B)


def visible(x):
    return (0 <= x < SH0) or (SH1 < x <= XMAX)


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


class KF:
    def __init__(self, x, v, pxx=0.01, pvv=1.0):
        self.x, self.v, self.pxx, self.pxv, self.pvv = x, v, pxx, 0.0, pvv

    def predict(self, qa=QA, dt=DT):
        self.x += self.v * dt
        pxx = self.pxx + 2 * dt * self.pxv + dt * dt * self.pvv + qa * qa * dt ** 4 / 4
        pxv = self.pxv + dt * self.pvv + qa * qa * dt ** 3 / 2
        pvv = self.pvv + qa * qa * dt * dt
        self.pxx, self.pxv, self.pvv = pxx, pxv, pvv

    def update(self, z, r=SIG * SIG):
        s = self.pxx + r
        kx, kv = self.pxx / s, self.pxv / s
        y = z - self.x
        self.x += kx * y
        self.v += kv * y
        pxx = (1 - kx) * self.pxx
        pxv = (1 - kx) * self.pxv
        pvv = self.pvv - kv * self.pxv
        self.pxx, self.pxv, self.pvv = pxx, pxv, pvv

    def sample(self):
        a, b = random.gauss(0, 1), random.gauss(0, 1)
        x = self.x + math.sqrt(self.pxx) * a
        cv = max(self.pvv - self.pxv ** 2 / self.pxx, 1e-12)
        v = self.v + self.pxv / self.pxx * (x - self.x) + math.sqrt(cv) * b
        return x, v


def approach(v_true):
    """Tratto in vista da x=0 a x=3: restituisce il Kalman all'ingresso nell'ombra."""
    x = 0.0
    kf = KF(x + random.gauss(0, SIG), 1.0)
    while x < SH0:
        x += v_true * DT
        kf.predict()
        if x < SH0 and random.random() < PD:
            kf.update(x + random.gauss(0, SIG))
    return kf


def pstep(p, pstop=PSTOP):
    # p = [x, v, modo(1 in moto, 0 fermo)]
    if p[2] == 1:
        if random.random() < pstop:
            p[2] = 0
        else:
            p[1] += random.gauss(0, QA * DT)
            p[0] += p[1] * DT
    elif random.random() < PGO:
        p[2] = 1


def resample(ps, ws):
    n = len(ps)
    step = 1.0 / n
    u = random.random() * step
    out, c, i = [], ws[0], 0
    for _ in range(n):
        while u > c and i < n - 1:
            i += 1
            c += ws[i]
        out.append(list(ps[i]))
        u += step
    return out, [step] * n


def scen2a(trials=100, n=1000):
    """Bersaglio che si ferma a x=4 dietro l'occlusore. Massa in celle osservate libere a 1, 2, 3 s."""
    marks = {15: "1 s", 30: "2 s", 45: "3 s"}
    acc = {k: [0.0, 0.0, 0.0, 0.0] for k in marks}   # A libero, B libero, B ombra, B' (senza evidenza negativa) libero
    for _ in range(trials):
        kf = approach(1.2)
        ps = [list(kf.sample()) + [1] for _ in range(n)]
        ws = [1.0 / n] * n
        qs = [list(p) for p in ps]                  # B': stesso modello, nessun aggiornamento negativo
        for k in range(1, 46):
            kf.predict()
            for p in ps:
                pstep(p)
            for q in qs:
                pstep(q)
            # nessun rilevamento: il bersaglio vero e' fermo nell'ombra
            ws = [w * ((1 - PD) if visible(p[0]) else 1.0) for w, p in zip(ws, ps)]
            tot = sum(ws)
            ws = [w / tot for w in ws]
            if 1.0 / sum(w * w for w in ws) < n / 2:
                ps, ws = resample(ps, ws)
            if k in marks:
                sd = math.sqrt(kf.pxx)
                a_free = (phi((SH0 - kf.x) / sd) - phi((0 - kf.x) / sd)) + (phi((XMAX - kf.x) / sd) - phi((SH1 - kf.x) / sd))
                acc[k][0] += a_free
                acc[k][1] += sum(w for w, p in zip(ws, ps) if visible(p[0]))
                acc[k][2] += sum(w for w, p in zip(ws, ps) if SH0 <= p[0] <= SH1)
                acc[k][3] += sum(1 for q in qs if visible(q[0])) / n
    print("== 2a: bersaglio FERMO dietro l'occlusore (media su %d prove) ==" % trials)
    print("dopo  | A Kalman CV: massa in celle osservate libere | B particelle+evid.neg.: libere / ombra | B' senza evid.neg.: libere")
    for k, lab in marks.items():
        a, b, bs, b2 = [v / trials for v in acc[k]]
        print("%s   | %.3f | %.4f / %.4f | %.3f" % (lab, a, b, bs, b2))


def crossing_times(kf, n, pstop, horizon=12.0):
    out = []
    steps = int(horizon / DT)
    for _ in range(n):
        x, v = kf.sample()
        p = [x, v, 1]
        t = math.inf
        for k in range(1, steps + 1):
            pstep(p, pstop)
            if p[0] > SH1:
                t = k * DT
                break
        out.append(t)
    out.sort()
    return out[int(0.05 * n)], out[int(0.95 * n) - 1]


def scen2b(trials=400, n=300):
    """Bersaglio che attraversa: copertura dell'intervallo al 90% dell'istante di riemersione, sigillato all'ingresso."""
    cov = {"A": 0, "B": 0}
    wid = {"A": [], "B": []}
    kinds = {"costante": [0, 0, 0], "rallenta": [0, 0, 0], "sosta": [0, 0, 0]}
    for _ in range(trials):
        v = random.uniform(0.8, 1.6)
        kf = approach(v)
        r = random.random()
        if r < 0.3:
            kind, t = "rallenta", (SH1 - SH0) / (v * random.uniform(0.6, 1.0))
        elif r < 0.4:
            kind, t = "sosta", (SH1 - SH0) / v + random.uniform(0, 3)
        else:
            kind, t = "costante", (SH1 - SH0) / v
        kinds[kind][0] += 1
        for j, (name, ps) in enumerate((("A", 0.0), ("B", PSTOP))):
            lo, hi = crossing_times(kf, n, ps)
            ok = lo <= t <= hi
            cov[name] += ok
            kinds[kind][1 + j] += ok
            wid[name].append(hi - lo)
    print("== 2b/3: bersaglio che ATTRAVERSA, %d passaggi ==" % trials)
    for name in ("A", "B"):
        w = sorted(wid[name])
        med = w[len(w) // 2]
        print("%s: copertura intervallo 90%% = %.3f ; larghezza mediana = %s s ; intervalli aperti (inf) = %d" % (
            name, cov[name] / trials, "inf" if math.isinf(med) else "%.2f" % med, sum(1 for x in w if math.isinf(x))))
    for kind, (m, a, b) in kinds.items():
        print("  %-9s n=%3d  coperti A=%3d  B=%3d" % (kind, m, a, b))


def scen4(trials=300, k_t=6, qt=0.8):
    """Un solo sguardo per passo fra 6 bersagli: giro a turno contro priorita' varianza / tempo al contatto."""
    res = {}
    for policy in ("turno", "priorita"):
        rnd = random.Random(4242)          # stesse scene per le due politiche
        se_thr, n_thr, se_oth, n_oth = 0.0, 0, 0.0, 0
        for _ in range(trials):
            xs = [rnd.uniform(6, 8)] + [rnd.uniform(3, 8) for _ in range(k_t - 1)]
            vs = [-rnd.uniform(1.0, 1.5)] + [rnd.uniform(-0.3, 0.3) for _ in range(k_t - 1)]
            kfs = [KF(x + rnd.gauss(0, SIG), 0.0) for x in xs]
            log = []
            step = 0
            while xs[0] > 0.5 and step < 225:
                for i in range(k_t):
                    if i == 0:
                        vs[i] = min(vs[i] + rnd.gauss(0, qt * DT), -0.3)
                    else:
                        vs[i] = 0.95 * vs[i] + rnd.gauss(0, qt * DT)
                    xs[i] = max(xs[i] + vs[i] * DT, 0.3)
                    kfs[i].predict(qa=qt)
                if policy == "turno":
                    c = step % k_t
                else:
                    def score(i):
                        ttc = max(kfs[i].x, 0.1) / max(-kfs[i].v, 0.05)
                        return kfs[i].pxx / max(ttc, 0.3)
                    c = max(range(k_t), key=score)
                kfs[c].update(xs[c] + rnd.gauss(0, SIG))
                ttc_true = [xs[i] / max(-vs[i], 0.05) for i in range(k_t)]
                m = min(range(k_t), key=lambda i: ttc_true[i])
                e_m = (kfs[m].x - xs[m]) ** 2
                e_o = sum((kfs[i].x - xs[i]) ** 2 for i in range(k_t) if i != m) / (k_t - 1)
                log.append((e_m, e_o))
                step += 1
            for e_m, e_o in log[-30:]:
                se_thr += e_m
                n_thr += 1
                se_oth += e_o
                n_oth += 1
        res[policy] = (math.sqrt(se_thr / n_thr), math.sqrt(se_oth / n_oth))
    print("== 4: un solo sguardo per passo, %d scene ==" % trials)
    for p, (a, b) in res.items():
        print("%-9s RMSE sul piu' minaccioso (ultimi 2 s) = %.3f m ; RMSE sugli altri = %.3f m" % (p, a, b))
    red = 1 - res["priorita"][0] / res["turno"][0]
    print("riduzione dell'errore sul piu' minaccioso: %.1f %% ; variazione sugli altri: %+.1f %%" % (
        100 * red, 100 * (res["priorita"][1] / res["turno"][1] - 1)))


if __name__ == "__main__":
    scen2a()
    scen2b()
    scen4()
