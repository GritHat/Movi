"""Attacco 3: F3 e F4 con parametri al limite contro V(tau) di frammenti.py. Importa eventi_volo/eventi_lp senza toccarli.
Varianti: V1 F3 |u|=dv sul bordo (120) e vento al limite (15); V2 = V1 + vc dichiarata sbagliata di 8 m/s per traccia;
V3 F4 avaria non contenuta: 5 % dei frammenti a 250 m/s, v_t 80 (pezzi di disco, ipotesi); V4 F4 aereo a 210 m/s, bordo."""
import json, math, os, sys
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, "..", "04-scenari"))
import numpy as np
import eventi_volo as V
EL, FR, G = V.EL, V.FR, 9.81

def frammenti(p0, vc, n, vt_rng, dv, vento, rng, bordo, disco=None, dt=0.05, t_max=90.0):
    w = np.asarray(vento, float); gv = np.array([0, 0, -G]); out = []
    for i in range(n):
        u = rng.standard_normal(3); u /= np.linalg.norm(u)
        if disco and i < disco[0]:
            u *= disco[1]; vt = disco[2]
        else:
            u *= dv * (1.0 if bordo else rng.random() ** (1 / 3))
            vt = math.exp(rng.uniform(math.log(vt_rng[0]), math.log(vt_rng[1])))
        k = G / vt ** 2; p = np.asarray(p0, float).copy(); v = np.asarray(vc, float) + u; T = [0.0]; P = [p.copy()]; t = 0.0
        while t < t_max - 1e-9:
            if p[2] > 0:
                kv = k * np.linalg.norm(v - w) * dt; v = (v + gv * dt + kv * w) / (1 + kv); p = p + v * dt
                if p[2] <= 0: p[2] = 0.0; v = np.zeros(3)
            t += dt; T.append(t); P.append(p.copy())
        out.append((np.array(T), np.array(P), i < (disco[0] if disco else 0)))
    return out

def prova(nome, p0, vc_vero_medio, vc_decl, r0, prof, n_fr, vt_rng, dv, vento, bordo, n_pass, disco=None):
    par = dict(EL.INV[prof]["prudente"], k_tc=EL.FRAM["k_tc"], r_rimbalzo=EL.FRAM["r_rimbalzo_m"])
    ev = {"p0": p0, "vc": vc_decl, "r0": r0}; R_imp, _ = FR.impronta(ev, par)
    tot = den = ok = nf = fuori_imp = 0; ok_disco = nd = 0; pass_ok = 0
    for i in range(n_pass):
        rng = np.random.default_rng(np.random.SeedSequence(20261134, spawn_key=(hash(nome) % 1000, i)))
        tutti_ok = True
        for T, P, is_d in frammenti(p0, vc_vero_medio, n_fr, vt_rng, dv, vento, rng, bordo, disco):
            nf += 1; d0 = den; c = 0
            ia = np.argmax(P[:, 2] <= 0) if np.any(P[:, 2] <= 0) else None
            if ia is not None and math.hypot(P[ia, 0] - p0[0], P[ia, 1] - p0[1]) > R_imp: fuori_imp += 1
            for j in range(0, len(T), 10):
                tau = T[j]; r, tq, zmin, zmax, Tc = FR.inviluppo(tau, ev, par); p = P[j]; tot += 1; c += 1
                den += int(FR.dentro_pianta(p[0], p[1], tau, ev, par) <= 1e-9 and zmin - 1e-6 <= p[2] <= zmax + 1e-6)
            sempre = (den - d0 == c); ok += sempre; tutti_ok &= sempre
            if is_d: nd += 1; ok_disco += sempre
        pass_ok += tutti_ok
    W = EL.m.wilson
    return {"variante": nome, "campioni_dentro": [den, tot, round(den / tot, 5), *[round(x, 5) for x in W(den, tot)]],
            "frammenti_sempre_dentro": [ok, nf, round(ok / nf, 4), *[round(x, 4) for x in W(ok, nf)]],
            "passaggi_tutti_dentro": [pass_ok, n_pass, *[round(x, 3) for x in W(pass_ok, n_pass)]],
            "pezzi_disco_sempre_dentro": [ok_disco, nd] if nd else None, "a_terra_fuori_impronta": fuori_imp, "R_imp_m": round(R_imp, 1)}

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
rs = []
d3 = [[40.0, 0, 0], [0, 35.0, 0]]
rs.append(prova("V1_F3_bordo_dv120_vento15", [0, 0, 120], [20.0, 17.5, 0.0], d3, 10.0, "collisione_multirotori", 60, [3, 40], 120.0, [15, 0, 0], True, N))
d3e = [[40.0, 8.0, 0], [-8.0, 35.0, 0]]   # vc dichiarata ruotata di 8 m/s di traverso (errore di traccia, ipotesi)
rs.append(prova("V2_F3_bordo_vc_errata8", [0, 0, 120], [20.0, 17.5, 0.0], d3e, 10.0, "collisione_multirotori", 60, [3, 40], 120.0, [15, 0, 0], True, N))
rs.append(prova("V3_F4_non_contenuta_5pc_disco250", [4050, 0, 450], [135.0, 0, 0], [[135.0, 0, 0]], 30.0, "avaria_motore_a_terra", 100, [5, 80], 60.0, [0, 5, 0], False, N, disco=(5, 250.0, 80.0)))
rs.append(prova("V4_F4_aereo210_bordo_dv100", [4050, 0, 450], [210.0, 0, 0], [[210.0, 0, 0]], 30.0, "avaria_motore_a_terra", 100, [5, 80], 100.0, [0, 15, 0], True, N))
json.dump(rs, open(os.path.join(QUI, "attacco_frammenti.json"), "w"), indent=1)
for r in rs: print(json.dumps(r))
