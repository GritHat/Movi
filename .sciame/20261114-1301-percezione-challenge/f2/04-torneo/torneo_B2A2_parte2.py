#!/usr/bin/env python3
"""Parte 2, seconda tornata: B2 (due persone, associazione in due stadi) e A2 (q dal NIS sui tratti visibili di G1).
Uso: timeout 120 python3 torneo_B2A2_parte2.py B2|A2"""
import math
import random
import sys
import torneo_parte2 as T

DT, SIG, C95, C99, K95 = T.DT, T.SIG, T.C95, T.C99, T.K95


def scene2(rnd, W, kinds, variant, q=0.5, same_dir=False):
    dy = rnd.uniform(0.3, 1.0)
    if same_dir:   # stessa direzione: B segue A di 0,6-1,6 m
        P = [T.Person(rnd, -1, W, kinds[0]), T.Person(rnd, -1, W, kinds[1], off=rnd.uniform(0.6, 1.6))]
    else:
        P = [T.Person(rnd, -1, W, kinds[0]), T.Person(rnd, +1, W, kinds[1], off=rnd.uniform(0, 0.8))]
    ys = [4.0, 4.0 + dy]
    tracks = []  # [id, ax, ay, miss, hits]
    nid = 0
    last = [None, None]
    was_hidden = [False, False]
    vis_after = [0.0, 0.0]
    amb = False
    t = 0.0
    while t < 16.0:
        for tr in tracks:
            tr[1].predict()
            tr[2].predict()
            tr[3] += 1
        keep = []
        for tr in tracks:
            if tr[4] < 3:
                ok = tr[3] <= 2                      # tentativa: muore dopo 2 mancati
            elif variant == "persa15":
                ok = K95 * math.sqrt(tr[1].a) <= 1.5
            else:
                ok = tr[3] * DT <= 3.0
            if ok:
                keep.append(tr)
        tracks = keep
        dets = []
        for i, p in enumerate(P):
            if abs(p.x) > W / 2:
                dets.append((i, p.x + rnd.gauss(0, SIG), ys[i] + rnd.gauss(0, SIG)))
                if was_hidden[i]:
                    vis_after[i] += DT
            else:
                was_hidden[i] = True
                vis_after[i] = 0.0
        free = list(range(len(dets)))
        for stage in (0, 1):
            cand = [tr for tr in tracks if (tr[4] >= 3) == (stage == 0)]
            if not cand or not free:
                continue
            cost = [[None] * len(free) for _ in cand]
            for i, tr in enumerate(cand):
                for jj, j in enumerate(free):
                    c = T.d2(tr[1], tr[2], dets[j][1], dets[j][2])
                    if c <= C99:
                        cost[i][jj] = c
            asg = T.best_assign(cost, len(cand), len(free))
            rest = []
            for jj, j in enumerate(free):
                i = asg[jj]
                if i is None:
                    rest.append(j)
                    continue
                tr = cand[i]
                if stage == 0 and tr[3] >= 3:
                    n_tr = sum(1 for ii in range(len(cand)) if cost[ii][jj] is not None)
                    n_dt = sum(1 for k in range(len(free)) if cost[i][k] is not None)
                    if n_tr >= 2 or n_dt >= 2:
                        amb = True
                tr[1].update(dets[j][1])
                tr[2].update(dets[j][2])
                tr[3] = 0
                tr[4] += 1
                last[dets[j][0]] = tr[0]
            free = rest
        for j in free:
            tr = [nid, T.Ax(q), T.Ax(q), 0, 3 if t == 0.0 else 1]   # al primo fotogramma le due tracce sono date
            nid += 1
            tr[1].update(dets[j][1])
            tr[2].update(dets[j][2])
            tracks.append(tr)
            last[dets[j][0]] = tr[0]
        for p in P:
            p.step(t)
        t += DT
        if all(was_hidden) and min(vis_after) >= 1.0:
            break
    swap = last[0] == 1 or last[1] == 0
    kept = last[0] == 0 and last[1] == 1
    return swap, kept, amb


def testB2():
    N = 2000
    print("== B2. Due persone, ungherese + porta al 99%% (q=0,5), associazione in due stadi (confermate prima), N=%d ==" % N)
    print("   tenuta = stesse due identita'; scambio = una persona finisce con l'identita' dell'altra; nuova = nessuno scambio, almeno un'identita' nuova;")
    print("   ambigue = almeno un riaggancio con >=2 candidati in porta; muti = scambi senza alcun riaggancio ambiguo")
    cases = (("(i) opposti, proseguono", ("prosegue", "prosegue"), False),
             ("(ii) opposti, tornano entrambi", ("torna", "torna"), False),
             ("(iv) opposti, uno sosta 1-3 s", ("sosta", "prosegue"), False),
             ("(v) opposti, uno torna e uno sosta", ("torna", "sosta"), False),
             ("(iii) opposti, miscela 70/18/12", None, False),
             ("(vi) stessa direzione, il primo sosta", ("sosta", "prosegue"), True),
             ("(vii) stessa direzione, miscela", None, True))
    for variant in ("persa15", "tetto3s"):
        for W in (1.0, 2.0):
            for ci, (label, mix, sd) in enumerate(cases):
                rnd = random.Random(4000 + int(W * 10) + 7 * ci + (0 if variant == "persa15" else 500))
                sw = kp = mu = am = 0
                for _ in range(N):
                    if mix is None:
                        ks = []
                        for _i in range(2):
                            u = rnd.random()
                            ks.append("prosegue" if u < 0.70 else "sosta" if u < 0.88 else "torna")
                    else:
                        ks = mix
                    s, k, a = scene2(rnd, W, ks, variant, same_dir=sd)
                    sw += s
                    kp += k
                    am += a
                    mu += s and not a
                print("  %-8s W=%.0f m %-38s tenuta %.3f  scambio %.3f+-%.3f  nuova %.3f  ambigue %.3f  muti %.3f" % (
                    variant, W, label, kp / N, sw / N, T.se(sw / N, N), 1 - (kp + sw) / N, am / N, mu / N))


def testA2():
    print("== A2. q scelto dal NIS medio sui tratti VISIBILI di G1 (camminata dritta), poi copertura sulla miscela G1 ==")
    rnd = random.Random(8)
    vis = []
    for _ in range(1500):
        traj, _k = T.g1(rnd, 2.0, "prosegue")
        vis.append(traj[:T.NV + 30])
    best = None
    for q in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 5.0):
        rn = random.Random(9)
        s = n = 0
        for traj in vis:
            ax, ay = T.Ax(q), T.Ax(q)
            for k, (x, y) in enumerate(traj):
                ax.predict()
                ay.predict()
                zx, zy = x + rn.gauss(0, SIG), y + rn.gauss(0, SIG)
                if k >= 15:
                    s += T.d2(ax, ay, zx, zy)
                    n += 1
                ax.update(zx)
                ay.update(zy)
        print("  q=%-6g NIS medio=%.3f" % (q, s / n))
        if best is None or abs(s / n - 2) < best[1]:
            best = (q, abs(s / n - 2))
    qn = best[0]
    for q in sorted({qn, 0.02, 0.05}):
        for D in (1.0, 2.0):
            rnd = random.Random(1000 + int(D * 10))   # stesse traiettorie della prova A
            ok = 0
            N = 4000
            for _ in range(N):
                traj, _k = T.g1(rnd, D)
                ok += T.reappear_d2(traj, rnd, (q,))[0] <= C95
            p = ok / N
            print("  q=%g%s: copertura 95%% a %.0f s su G1 = %.3f+-%.3f ; P(passare 26/30)=%.3f" % (
                q, " (scelto dal NIS)" if q == qn else "", D, p, T.se(p, N), T.binom_ge(26, 30, p)))


if __name__ == "__main__":
    {"B2": testB2, "A2": testA2}[sys.argv[1]]()
