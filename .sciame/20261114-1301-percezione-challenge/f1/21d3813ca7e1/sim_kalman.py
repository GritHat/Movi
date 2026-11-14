#!/usr/bin/env python3
"""Simulazione Monte Carlo per la consegna di sciame-kalman (f1, corsia A).

Python puro (numpy non installato). Rifare con:
    python3 sim_kalman.py | tee risultati.txt
Semi fissati. Le previsioni sono in PREVISIONI.md, scritte prima di questo file.

La verita' NON e' il modello del filtro: pedone con velocita' desiderata che salta a istanti
di Poisson (0,4 salti/s: arresto con prob. 0,2, altrimenti nuova velocita' 0,6-1,8 m/s e
virata N(0, 60 gradi)), rilassamento del primo ordine tau = 0,4 s, velocita' <= 2 m/s.
Misura: posizione 2D sul piano del suolo + rumore gaussiano isotropo sigma_z per asse.
"""
import math
import random
import time

CHI2_2_95 = 5.991
CHI2_2_99 = 9.210
BASE = 30            # Hz dei campioni della verita'
SUB = 10             # sottopassi di integrazione per campione (300 Hz)


# ---------- algebra minima ----------
def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def tr(A):
    return [list(r) for r in zip(*A)]


def add(A, B):
    return [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def cv_model(T, q):
    return ([[1, T], [0, 1]],
            [[q * T ** 3 / 3, q * T ** 2 / 2], [q * T ** 2 / 2, q * T]])


def ca_model(T, q):
    return ([[1, T, T * T / 2], [0, 1, T], [0, 0, 1]],
            [[q * T ** 5 / 20, q * T ** 4 / 8, q * T ** 3 / 6],
             [q * T ** 4 / 8, q * T ** 3 / 3, q * T ** 2 / 2],
             [q * T ** 3 / 6, q * T ** 2 / 2, q * T]])


def predict_P(F, Q, P):
    return add(mm(mm(F, P), tr(F)), Q)


def precompute(F, Q, R, P0, nsteps):
    """Covarianze e guadagni (non dipendono dai dati). Misura a ogni passo. Forma di Joseph."""
    n = len(F)
    P = P0
    out = [(None, None, None, P0)]
    for _ in range(1, nsteps):
        Pp = predict_P(F, Q, P)
        S = Pp[0][0] + R
        K = [Pp[i][0] / S for i in range(n)]
        A = [[(1.0 if i == j else 0.0) - (K[i] if j == 0 else 0.0) for j in range(n)]
             for i in range(n)]
        Pn = add(mm(mm(A, Pp), tr(A)), [[K[i] * R * K[j] for j in range(n)] for i in range(n)])
        out.append((Pp, S, K, Pn))
        P = Pn
    return out


def run_axis(F, pre, z):
    """Filtro su un asse; restituisce innovazioni e stati a posteriori."""
    n = len(F)
    x = [z[0]] + [0.0] * (n - 1)
    nus = [0.0]
    xs = [x]
    for k in range(1, len(z)):
        xp = [sum(F[i][j] * x[j] for j in range(n)) for i in range(n)]
        nu = z[k] - xp[0]
        K = pre[k][2]
        x = [xp[i] + K[i] * nu for i in range(n)]
        nus.append(nu)
        xs.append(x)
    return nus, xs


# ---------- verita' ----------
def gen_truth(rng, dur, lam=0.4, tau=0.4, vmax=2.0):
    dt = 1.0 / (BASE * SUB)
    h = rng.uniform(0, 2 * math.pi)
    s = rng.uniform(0.6, 1.8)
    ux, uy = s * math.cos(h), s * math.sin(h)
    vx, vy = ux, uy
    px = py = 0.0
    out = []
    n = int(round(dur * BASE)) * SUB + 1
    sq = 0.3 * math.sqrt(dt)
    for i in range(n):
        ax, ay = (ux - vx) / tau, (uy - vy) / tau
        if i % SUB == 0:
            out.append((px, py, vx, vy, ax, ay))
        if rng.random() < lam * dt:
            if rng.random() < 0.2:
                ux = uy = 0.0
            else:
                s = rng.uniform(0.6, 1.8)
                h += rng.gauss(0, math.radians(60))
                ux, uy = s * math.cos(h), s * math.sin(h)
        vx += ax * dt + sq * rng.gauss(0, 1)
        vy += ay * dt + sq * rng.gauss(0, 1)
        sp = math.hypot(vx, vy)
        if sp > vmax:
            vx, vy = vx * vmax / sp, vy * vmax / sp
        px += vx * dt
        py += vy * dt
    return out


def make_set(seed, nruns, dur):
    rng = random.Random(seed)
    truths, noises = [], []
    for _ in range(nruns):
        t = gen_truth(rng, dur)
        truths.append(t)
        noises.append([(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in t])
    return truths, noises


T_VIS = 4.0     # secondi di visibilita' prima dell'occlusione
T_SS = 1.5      # da qui si considerano le statistiche di regime


def visible_stats(model, q, rate, sz, dataset, want_states=False):
    """Fase visibile [0, T_VIS]. Restituisce statistiche di regime e (se chiesto) lo stato a T_VIS."""
    truths, noises = dataset
    stride = BASE // rate
    T = 1.0 / rate
    F, Q = model(T, q)
    n = len(F)
    R = sz * sz
    P0 = [[0.0] * n for _ in range(n)]
    P0[0][0] = R
    P0[1][1] = 1.5 ** 2
    if n == 3:
        P0[2][2] = 1.0 ** 2
    nst = int(round(T_VIS * rate)) + 1
    pre = precompute(F, Q, R, P0, nst)
    k_ss = int(round(T_SS * rate))
    s_nis = cnt = 0.0
    s_nees = 0.0
    s_ep = s_ev = s_ea = s_a2 = 0.0
    c01 = c00 = 0.0
    finals = []
    for tr_, nz in zip(truths, noises):
        zx = [tr_[k * stride][0] + sz * nz[k * stride][0] for k in range(nst)]
        zy = [tr_[k * stride][1] + sz * nz[k * stride][1] for k in range(nst)]
        nux, xsx = run_axis(F, pre, zx)
        nuy, xsy = run_axis(F, pre, zy)
        for k in range(k_ss, nst):
            S = pre[k][1]
            Pn = pre[k][3]
            s_nis += (nux[k] ** 2 + nuy[k] ** 2) / S
            t_ = tr_[k * stride]
            for ax_, xs_ in ((0, xsx), (1, xsy)):
                e0 = xs_[k][0] - t_[ax_]
                e1 = xs_[k][1] - t_[2 + ax_]
                s_ep += e0 * e0
                s_ev += e1 * e1
                if n == 2:
                    det = Pn[0][0] * Pn[1][1] - Pn[0][1] ** 2
                    s_nees += (Pn[1][1] * e0 * e0 - 2 * Pn[0][1] * e0 * e1 + Pn[0][0] * e1 * e1) / det
                else:
                    e2 = xs_[k][2] - t_[4 + ax_]
                    s_ea += e2 * e2
                    s_a2 += t_[4 + ax_] ** 2
            if k + 1 < nst:
                c01 += nux[k] * nux[k + 1] + nuy[k] * nuy[k + 1]
                c00 += nux[k] ** 2 + nuy[k] ** 2
            cnt += 1
        if want_states:
            finals.append((xsx[-1], xsy[-1]))
    Pss = pre[-1][3]
    res = {
        "nis": s_nis / cnt, "nees": s_nees / cnt if n == 2 else float("nan"),
        "rmse_p": math.sqrt(s_ep / (2 * cnt)), "rmse_v": math.sqrt(s_ev / (2 * cnt)),
        "sig_p": math.sqrt(Pss[0][0]), "sig_v": math.sqrt(Pss[1][1]),
        "rho1": c01 / c00, "Pss": Pss, "F": F, "Q": Q, "R": R,
    }
    if n == 3:
        res["rmse_a"] = math.sqrt(s_ea / (2 * cnt))
        res["rms_a_true"] = math.sqrt(s_a2 / (2 * cnt))
        res["sig_a"] = math.sqrt(Pss[2][2])
    if want_states:
        res["finals"] = finals
    return res


def tune(model, grid, rate, sz, dataset):
    best = None
    for q in grid:
        r = visible_stats(model, q, rate, sz, dataset)
        if best is None or abs(r["nis"] - 2) < abs(best[1] - 2):
            best = (q, r["nis"])
    return best


def occlusion(res, rate, sz, dataset, durations):
    """Dalla fine della fase visibile: sola predizione per T_occ, poi confronto alla ricomparsa."""
    truths, noises = dataset
    F, Q, R = res["F"], res["Q"], res["R"]
    n = len(F)
    T = 1.0 / rate
    out = {}
    for d in durations:
        steps = int(round(d * rate))
        P = res["Pss"]
        for _ in range(steps):
            P = predict_P(F, Q, P)
        Ppp = P[0][0]
        idx = int(round((T_VIS + d) * BASE))
        tt = steps * T
        cov_t = cov_z = 0
        se = 0.0
        for (fx, fy), tr_, nz in zip(res["finals"], truths, noises):
            px = fx[0] + fx[1] * tt + (fx[2] * tt * tt / 2 if n == 3 else 0.0)
            py = fy[0] + fy[1] * tt + (fy[2] * tt * tt / 2 if n == 3 else 0.0)
            ex, ey = px - tr_[idx][0], py - tr_[idx][1]
            se += ex * ex + ey * ey
            if (ex * ex + ey * ey) / Ppp <= CHI2_2_95:
                cov_t += 1
            ix = tr_[idx][0] + sz * nz[idx][0] - px
            iy = tr_[idx][1] + sz * nz[idx][1] - py
            if (ix * ix + iy * iy) / (Ppp + R) <= CHI2_2_95:
                cov_z += 1
        N = len(truths)
        out[d] = (cov_t / N, cov_z / N, math.sqrt(CHI2_2_95 * Ppp), math.sqrt(se / N))
    return out


def time_to_radius(res, rate, radius):
    F, Q = res["F"], res["Q"]
    P = res["Pss"]
    for k in range(1, 20 * rate):
        P = predict_P(F, Q, P)
        if math.sqrt(CHI2_2_95 * P[0][0]) > radius:
            return k / rate
    return float("inf")


# ---------- S3: moto proprio ----------
def rot(a, x, y):
    c, s = math.cos(a), math.sin(a)
    return c * x - s * y, s * x + c * y


def cpa(rx, ry, wx, wy):
    w2 = wx * wx + wy * wy
    if w2 < 1e-9:
        return math.hypot(rx, ry)
    ts = max(0.0, -(rx * wx + ry * wy) / w2)
    return math.hypot(rx + wx * ts, ry + wy * ts)


def ego_motion(q, rate=15, sz=0.05, nruns=500, seed=7, v_obj=(0.0, 0.0)):
    rng = random.Random(seed)
    T = 1.0 / rate
    F, Q = cv_model(T, q)
    R = sz * sz
    dur = 3.0
    nst = int(round(dur * rate)) + 1
    pre = precompute(F, Q, R, [[R, 0], [0, 1.5 ** 2]], nst)
    vu = 1.2
    amp, f = math.radians(30), 0.5
    bias = math.radians(1.0)
    arw = math.radians(0.05)       # gradi/sqrt(s): 0,5 gradi/s di rumore a 100 Hz
    stats = {v: [0.0, 0, 0, 0] for v in "abc"}   # somma err^2 CPA, n, mobile, n
    k1 = int(round(1.0 * rate))
    for _ in range(nruns):
        ph = rng.uniform(0, 2 * math.pi)
        eps = rng.gauss(0, 0.10)
        sgn = rng.choice((-1, 1))
        w = 0.0
        za, zb, zc, pu_hat = ([], []), ([], []), ([], []), []
        true_cpa = []
        for k in range(nst):
            t = k * T
            psi = amp * (math.sin(2 * math.pi * f * t + ph) - math.sin(ph))
            if k:
                w += arw * math.sqrt(T) * rng.gauss(0, 1)
            psih = psi + sgn * bias * t + w
            ox, oy = 4.6 + v_obj[0] * t, 1.0 + v_obj[1] * t
            rx, ry = ox - vu * t, oy
            bx, by = rot(-psi, rx, ry)
            bx += sz * rng.gauss(0, 1)
            by += sz * rng.gauss(0, 1)
            sx, sy = rot(psih, bx, by)
            ph_x = vu * (1 + eps) * t
            za[0].append(bx); za[1].append(by)
            zb[0].append(sx); zb[1].append(sy)
            zc[0].append(ph_x + sx); zc[1].append(sy)
            pu_hat.append(ph_x)
            true_cpa.append(cpa(rx, ry, v_obj[0] - vu, v_obj[1]))
        for name, z in (("a", za), ("b", zb), ("c", zc)):
            _, xsx = run_axis(F, pre, z[0])
            _, xsy = run_axis(F, pre, z[1])
            for k in range(k1, nst):
                Pvv = pre[k][3][1][1]
                vx, vy = xsx[k][1], xsy[k][1]
                if name == "c":
                    m = cpa(xsx[k][0] - pu_hat[k], xsy[k][0], vx - vu * (1 + eps), vy)
                else:
                    m = cpa(xsx[k][0], xsy[k][0], vx, vy)
                st = stats[name]
                st[0] += (m - true_cpa[k]) ** 2
                st[1] += 1
                st[2] += (vx * vx + vy * vy) / Pvv > CHI2_2_99
                st[3] += 1
    return {k: (math.sqrt(v[0] / v[1]), v[2] / v[3]) for k, v in stats.items()}


def time_to_mobile(q, rate=15, sz=0.05, nruns=1000, seed=11, speed=1.2):
    rng = random.Random(seed)
    T = 1.0 / rate
    F, Q = cv_model(T, q)
    R = sz * sz
    nst = int(round(4.0 * rate)) + 1
    pre = precompute(F, Q, R, [[R, 0], [0, 1.5 ** 2]], nst)
    times = []
    for _ in range(nruns):
        h = rng.uniform(0, 2 * math.pi)
        zx = [speed * math.cos(h) * k * T + sz * rng.gauss(0, 1) for k in range(nst)]
        zy = [speed * math.sin(h) * k * T + sz * rng.gauss(0, 1) for k in range(nst)]
        _, xsx = run_axis(F, pre, zx)
        _, xsy = run_axis(F, pre, zy)
        tdet = float("inf")
        for k in range(1, nst):
            if (xsx[k][1] ** 2 + xsy[k][1] ** 2) / pre[k][3][1][1] > CHI2_2_99:
                tdet = k * T
                break
        times.append(tdet)
    times.sort()
    return times[len(times) // 2], times[int(0.95 * len(times))]


def main():
    t0 = time.time()
    print("== sim_kalman.py: verita' = pedone che manovra (non il modello del filtro) ==")
    tune_set = make_set(1, 300, T_VIS)
    eval_set = make_set(2, 1500, T_VIS + 3.0)
    qgrid = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0]
    durs = (0.5, 1.0, 2.0, 3.0)

    print("\n-- S1: che cosa e' stimabile (velocita' quasi costante, q tarato sul NIS; valori per asse) --")
    print("Hz  sz[m]  q*    NIS(2) NEES(4) rho1   sig_p  rmse_p  sig_v  rmse_v [m, m/s]")
    ref = None
    tuned = {}
    for rate, sz in ((10, 0.05), (15, 0.05), (30, 0.05), (15, 0.02), (15, 0.10)):
        q, _ = tune(cv_model, qgrid, rate, sz, tune_set)
        r = visible_stats(cv_model, q, rate, sz, eval_set, want_states=True)
        tuned[(rate, sz)] = (q, r)
        print(f"{rate:<3d} {sz:<6.2f} {q:<5.2f} {r['nis']:<6.2f} {r['nees']:<7.2f} {r['rho1']:<+6.2f} "
              f"{r['sig_p']:<6.3f} {r['rmse_p']:<7.3f} {r['sig_v']:<6.3f} {r['rmse_v']:<6.3f}")
        if (rate, sz) == (15, 0.05):
            ref = (q, r)
    qref, rref = ref

    print("\n-- S2: occlusione, sola predizione; alla ricomparsa (1500 prove) --")
    print("config                T_occ  copertura95(verita')  copertura95(misura)  raggio95[m]  rmse2D[m]")
    occ_ref = None
    for label, rate, sz, q in (
            (f"CV 15Hz q*={qref}", 15, 0.05, qref),
            ("CV 15Hz q=0.01 (ottim.)", 15, 0.05, 0.01),
            (f"CV 15Hz q=4q*={4 * qref}", 15, 0.05, 4 * qref),
            (f"CV 10Hz q*={tuned[(10, 0.05)][0]}", 10, 0.05, tuned[(10, 0.05)][0]),
            (f"CV 30Hz q*={tuned[(30, 0.05)][0]}", 30, 0.05, tuned[(30, 0.05)][0]),
            (f"CV 15Hz sz=10cm q*={tuned[(15, 0.10)][0]}", 15, 0.10, tuned[(15, 0.10)][0])):
        r = visible_stats(cv_model, q, rate, sz, eval_set, want_states=True)
        o = occlusion(r, rate, sz, eval_set, durs)
        if occ_ref is None:
            occ_ref = o
        for d in durs:
            print(f"{label:<28s} {d:<5.1f} {o[d][0]:<21.3f} {o[d][1]:<20.3f} {o[d][2]:<12.2f} {o[d][3]:.2f}")
    for rad in (1.0, 1.5, 2.0):
        print(f"raggio95 > {rad} m dopo {time_to_radius(rref, 15, rad):.2f} s di occlusione (CV 15 Hz, q*={qref})")

    print("\n-- S2b: accelerazione costante (jerk tarato sul NIS), 15 Hz, 5 cm --")
    jgrid = [0.5, 1, 2, 5, 10, 20, 50, 100, 200]
    qj, nisj = tune(ca_model, jgrid, 15, 0.05, tune_set)
    rc = visible_stats(ca_model, qj, 15, 0.05, eval_set, want_states=True)
    print(f"jerk q*={qj}  NIS={rc['nis']:.2f}  sig_a dichiarata={rc['sig_a']:.2f} m/s^2  rmse_a={rc['rmse_a']:.2f}  "
          f"valore efficace a vera={rc['rms_a_true']:.2f}  rapporto rmse_a/rms_a={rc['rmse_a'] / rc['rms_a_true']:.2f}")
    print(f"sig_v={rc['sig_v']:.3f} rmse_v={rc['rmse_v']:.3f}")
    oc = occlusion(rc, 15, 0.05, eval_set, durs)
    for d in durs:
        print(f"CA T_occ={d}: copertura95={oc[d][0]:.3f} raggio95={oc[d][2]:.2f} m rmse2D={oc[d][3]:.2f} m "
              f"(CV: {occ_ref[d][3]:.2f} m; rapporto CA/CV={oc[d][3] / occ_ref[d][3]:.2f})")

    print("\n-- S3: moto proprio (portatore 1,2 m/s, testa +-30 gradi a 0,5 Hz; ostacolo FERMO) --")
    e = ego_motion(qref)
    for k, lab in (("a", "nessuna compensazione"), ("b", "solo giroscopio"), ("c", "giroscopio + traslazione (10%)")):
        print(f"({k}) {lab:<32s} errore RMS CPA = {e[k][0]:.2f} m   dichiarato 'mobile' = {100 * e[k][1]:.1f}% del tempo")
    e2 = ego_motion(qref, v_obj=(0.0, -0.8), seed=8)
    print("   stesso scenario, ostacolo MOBILE (0,8 m/s trasversale):")
    for k in "abc":
        print(f"({k}) errore RMS CPA = {e2[k][0]:.2f} m   dichiarato 'mobile' = {100 * e2[k][1]:.1f}%")
    med, p95 = time_to_mobile(qref)
    print(f"tempo per dichiarare 'mobile' un pedone a 1,2 m/s (riferimento compensato): mediana {med:.2f} s, 95% {p95:.2f} s")
    med, p95 = time_to_mobile(qref, speed=0.0, seed=12)
    print(f"ostacolo fermo, riferimento ideale: primo falso 'mobile' mediana {med} s (inf = mai in 4 s)")

    print("\n-- S4: massa (punto materiale, forza ignota): x = x0 + v0 t + (F/m) t^2/2 --")
    Fm, m_, sig = 80.0, 70.0, 0.05
    a11 = a12 = a22 = 0.0
    for k in range(45):
        t = k / 15
        jF, jm = t * t / (2 * m_), -Fm * t * t / (2 * m_ * m_)
        a11 += jF * jF / sig ** 2
        a12 += jF * jm / sig ** 2
        a22 += jm * jm / sig ** 2
    det = a11 * a22 - a12 * a12
    print(f"FIM(F,m): det/traccia^2 = {det / (a11 + a22) ** 2:.2e} (0 = rango 1: osservabile solo F/m)")
    print(f"\ntempo di calcolo: {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
