"""prove_confidenza.py — P1 (integrale esatto contro forme chiuse e Monte Carlo), P2 (t_C dalla cubica),
jacobiana della virata alle differenze finite, esempio di curva per il registro. Seme 20261115."""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stima_v4 as S

rng = np.random.default_rng(20261115)
out = {}
# P1a forme chiuse
e2 = max(abs(S.prob_gauss_ellissoide([0, 0], s * s * np.eye(2), [0, 0], r * r * np.eye(2)) - S.C_disco_centrato(r, s * s))
         for s in [0.3, 1, 5, 40] for r in [0.1, 1, 3, 10, 100])
e3 = max(abs(S.prob_gauss_ellissoide([0, 0, 0], s * s * np.eye(3), [0, 0, 0], r * r * np.eye(3)) - S.C_sfera_centrata(r, s * s))
         for s in [0.3, 1, 5, 40] for r in [0.1, 1, 3, 10, 100])
out["P1_scarto_max_forma_chiusa_2D"] = float(e2)
out["P1_scarto_max_forma_chiusa_3D"] = float(e3)
# P1b Monte Carlo su 20 casi casuali anisotropi e fuori centro
N = 1_000_000
casi = []
for k in range(20):
    d = 2 if k < 10 else 3
    B = rng.standard_normal((d, d)) * rng.uniform(0.2, 5, d)
    Sg = B @ B.T + 0.01 * np.eye(d)
    m = rng.standard_normal(d) * 2
    C = rng.standard_normal((d, d)); A = C @ C.T + 0.5 * np.eye(d) * rng.uniform(1, 10)
    p = S.prob_gauss_ellissoide(m, Sg, np.zeros(d), A, n=64)
    X = rng.multivariate_normal(m, Sg, N)
    inside = np.einsum("ij,jk,ik->i", X, np.linalg.inv(A), X) <= 1
    f = inside.mean(); se = math.sqrt(max(f * (1 - f), 1e-12) / N)
    casi.append(dict(d=d, quadratura=p, montecarlo=float(f), z=float((p - f) / max(se, 1e-9)), dentro_99_9=bool(abs(p - f) <= 3.29 * se + 2e-6)))
out["P1_montecarlo"] = casi
out["P1_tutti_dentro_99_9"] = all(c["dentro_99_9"] for c in casi)
out["P1_z_max"] = max(abs(c["z"]) for c in casi)
# P2 t_C contro ricerca numerica
err = 0
for (s0, s0v, sv, q, r, a) in [(10, 0, 4, 1, 100, .9), (7.5 ** 2, 5, 2, 8, 150, .5), (1, 0, .25, .5, 5, .9), (25, -2, 1, 3, 60, .9)]:
    tc = S.t_C(a, r, s0, s0v, sv, q, d=2)
    lo, hi = 0.0, 1e4
    for _ in range(200):
        mid = (lo + hi) / 2
        if S.C_disco_centrato(r, S.sigma2_cv(mid, s0, s0v, sv, q)) >= a: lo = mid
        else: hi = mid
    err = max(err, abs(tc - lo))
    tc3 = S.t_C(a, r, s0, s0v, sv, q, d=3)
    lo, hi = 0.0, 1e4
    for _ in range(200):
        mid = (lo + hi) / 2
        if S.C_sfera_centrata(r, S.sigma2_cv(mid, s0, s0v, sv, q)) >= a: lo = mid
        else: hi = mid
    err = max(err, abs(tc3 - lo))
out["P2_scarto_max_tC_s"] = float(err)
# jacobiana della virata
p = S.PARAMETRI_BASE["aerei_veloci"]
ej = 0
for w in [0.0, 1e-7, 0.02, -0.05, 0.3]:
    x = rng.standard_normal(10) * 50; x[9] = w; dt = 1.3
    Fa = S.F_ct(x, dt); Fn = np.zeros((10, 10))
    for i in range(10):
        h = 1e-6 * max(1, abs(x[i])); e = np.zeros(10); e[i] = h
        Fn[:, i] = (S.f_ct(x + e, dt) - S.f_ct(x - e, dt)) / (2 * h)
    Fn[6:9, :] = 0
    ej = max(ej, float(np.max(np.abs(Fa - Fn)[[0, 1, 2, 3, 4, 5, 9]])))
out["jacobiana_virata_scarto_max"] = ej
# esempio di curva per il registro: aereo a 80 m/s in virata, poi perdita; regione dichiarata = disco orizzontale 300 m
f = S.IMM(np.array([0., 0, 300]), 7.5 ** 2 * np.eye(3), 0.0, p)
f2 = S.FiltroCV(np.array([0., 0, 300]), 7.5 ** 2 * np.eye(3), 0.0, p)
w = 0.03; v = 80.0
for k in range(1, 40):
    t = float(k)
    pos = np.array([v / w * math.sin(w * t), v / w * (1 - math.cos(w * t)), 300])
    z = pos + 7.5 * rng.standard_normal(3)
    for F in (f, f2):
        F.prevedi(t); F.aggiorna(z, 7.5 ** 2 * np.eye(3))
reg = dict(dims=[0, 1], A=300.0 ** 2 * np.eye(2), c=None)
out["esempio_curva_imm"] = S.curva_confidenza(f, reg, taus=[0, 1, 2, 5, 10, 15, 20, 30])
out["esempio_curva_cv"] = S.curva_confidenza(f2, reg, taus=[0, 1, 2, 5, 10, 15, 20, 30])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "prove_confidenza.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: v for k, v in out.items() if k not in ("P1_montecarlo",)}, indent=1, ensure_ascii=False)[:4000])
