#!/usr/bin/env python3
# sciame-kalman, f9/03-kalman: P-K10.  Le STESSE due ipotesi della preproposta (H1 velocita' costante, H2 smorzata verso il
# centro dell'ombra, pesi 0,8/0,2) con la verosimiglianza corretta del "nessun rilevamento": la densita' condizionata e'
# portata avanti con particelle; peso * (1 - Pd) nel visibile oltre la fascia; Lambda_i = somma dei pesi; mu_i ~ mu_i * Lambda_i.
# Uso: timeout 120 python3 sim_s4_pesi.py <prosegue|sosta> <q> <Pd_modello> <fascia_m> [N]
import sys, math, random
sys.dont_write_bytecode = True
import sim_s3s4 as S

DT, PD = S.DT, S.PD


def run(beh, q, pdm, g, N, seed):
    rng = random.Random(seed)
    NPH = 150
    snv = math.sqrt(q * DT)
    n_a = a_lt = 0
    n_b = b_gt = 0
    mus = {8: [0.0, 0], 15: [0.0, 0], 30: [0.0, 0], 45: [0.0, 0]}
    for trial in range(N):
        tr = S.Truth(rng, beh)
        dets, xs, P, fr, last, nd = [], None, None, 0, -1, 0
        while True:
            tr.step()
            fr += 1
            if not S.detectable(tr.x, tr.z):
                break
            if rng.random() < PD:
                zx, zz = tr.x + rng.gauss(0, S.SIG), tr.z + rng.gauss(0, S.SIG)
                if xs is None:
                    dets.append((fr, zx, zz))
                    if len(dets) == 2:
                        d = (dets[1][0] - dets[0][0]) * DT
                        xs = [zx, zz, (zx - dets[0][1]) / d, (zz - dets[0][2]) / d]
                        R = S.SIG ** 2
                        P = (R, R / d, 2 * R / (d * d))
                        last, nd = fr, 2
                else:
                    for _ in range(fr - last):
                        xs[0] += xs[2] * DT
                        xs[1] += xs[3] * DT
                        P = S.cov_step(P, 1.0)
                    p11, p12, p22 = P
                    Sn = p11 + S.SIG ** 2
                    k1, k2 = p11 / Sn, p12 / Sn
                    ix_, iz_ = zx - xs[0], zz - xs[1]
                    xs[0] += k1 * ix_; xs[1] += k1 * iz_; xs[2] += k2 * ix_; xs[3] += k2 * iz_
                    P = ((1 - k1) * p11, (1 - k1) * p12, p22 - k2 * p12)
                    last = fr
                    nd += 1
            if fr > 200:
                xs = None
                break
        if xs is None or nd < 4:
            continue
        px0, pz0, vx0, vz0 = xs
        sp0 = math.hypot(vx0, vz0)
        s_in = s_out = None
        if sp0 > 1e-6:
            ux, uz = vx0 / sp0, vz0 / sp0
            s = 0.0
            while s < 4.0:
                c = S.cls(px0 + s * ux, pz0 + s * uz, 0.0) == S.SH
                if c and s_in is None:
                    s_in = s
                if s_in is not None and not c:
                    s_out = s
                    break
                s += 0.02
        sc = 0.5 * (s_in + s_out) if (s_in is not None and s_out is not None) else 0.5
        alpha = sc / (sc + sp0 * DT) if sp0 > 1e-6 else 0.9
        sp_, sv_ = math.sqrt(P[0]), math.sqrt(P[2])
        H = []
        for a in (1.0, alpha):
            H.append([a,
                      [px0 + rng.gauss(0, sp_) for _ in range(NPH)], [pz0 + rng.gauss(0, sp_) for _ in range(NPH)],
                      [vx0 + rng.gauss(0, sv_) for _ in range(NPH)], [vz0 + rng.gauss(0, sv_) for _ in range(NPH)],
                      [1.0 / NPH] * NPH])
        mu = [0.8, 0.2]
        pend = fr - last
        k = 0
        was_in = False
        lastmu = None
        while k < 45:
            k += 1
            if k > pend:
                tr.step()
                if S.detectable(tr.x, tr.z) and rng.random() < PD:
                    break
            lam = [0.0, 0.0]
            for h in (0, 1):
                a, X, Z, VX, VZ, W = H[h]
                sw = 0.0
                for i in range(NPH):
                    VX[i] = a * VX[i] + rng.gauss(0.0, snv)
                    VZ[i] = a * VZ[i] + rng.gauss(0.0, snv)
                    X[i] += VX[i] * DT
                    Z[i] += VZ[i] * DT
                    if S.neginfo(X[i], Z[i], 0.0, g):
                        W[i] *= (1.0 - pdm)
                    sw += W[i]
                lam[h] = sw
                if sw > 0.0:
                    ess = 0.0
                    for i in range(NPH):
                        W[i] /= sw
                        ess += W[i] * W[i]
                    if 1.0 / ess < NPH / 2:
                        u0 = rng.random() / NPH
                        c = W[0]
                        j = 0
                        nX, nZ, nVX, nVZ = [], [], [], []
                        for i in range(NPH):
                            u = u0 + i / NPH
                            while u > c and j < NPH - 1:
                                j += 1
                                c += W[j]
                            nX.append(X[j]); nZ.append(Z[j]); nVX.append(VX[j]); nVZ.append(VZ[j])
                        H[h] = [a, nX, nZ, nVX, nVZ, [1.0 / NPH] * NPH]
                else:
                    H[h][5] = [1.0 / NPH] * NPH
            t1, t2 = mu[0] * lam[0], mu[1] * lam[1]
            if t1 + t2 > 0.0:
                mu = [t1 / (t1 + t2), t2 / (t1 + t2)]
            if k <= pend:
                continue
            tx, tz = tr.x, tr.z
            if beh == 'prosegue' and tz > S.ZP and abs(tx) < S.KW * tz and tx * tx + tz * tz <= S.RMAX2:
                was_in = True
                lastmu = mu[0]
            if k in mus and S.hidden_true(tx, tz):
                mus[k][0] += mu[0]
                mus[k][1] += 1
            if k == 45 and beh == 'sosta' and sp0 >= 1.0 and S.hidden_true(tx, tz):
                n_b += 1
                if mu[0] > 0.5:
                    b_gt += 1
        if beh == 'prosegue' and was_in:
            n_a += 1
            if lastmu < 0.5:
                a_lt += 1
    print(f"comportamento={beh} q={q} Pd_modello={pdm} fascia={g} N={N} seme={seed}")
    print("  mu1 medio a soggetto nascosto: " + "  ".join(f"{k * DT:4.2f} s: {v[0] / max(1, v[1]):5.3f} (n={v[1]})" for k, v in mus.items()))
    if beh == 'prosegue':
        print(f"  (a) transiti con il vero passato in ombra n={n_a}; mu1<0,5 all'ultimo ciclo in ombra: {a_lt} = {a_lt / max(1, n_a):5.3f}")
    else:
        print(f"  (b) soste con ingresso >= 1,0 m/s nascoste a 3 s n={n_b}; mu1>0,5: {b_gt} = {b_gt / max(1, n_b):5.3f}")


if __name__ == '__main__':
    beh = sys.argv[1]
    q = float(sys.argv[2])
    pdm = float(sys.argv[3])
    g = float(sys.argv[4])
    N = int(sys.argv[5]) if len(sys.argv) > 5 else 2000
    run(beh, q, pdm, g, N, 20261114 + (0 if beh == 'prosegue' else 1000))
