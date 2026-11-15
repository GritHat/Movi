"""curva_video.py — C(τ) e r_0,9(τ) per un aereo a 210 m/s e un drone a 45 m/s (traiettorie SINTETICHE rettilinee,
sensore simulato come in prove_v5), 0–30 s, con l'IMM4 a pesi fissati, σ_rif e il livello ricalibrato a*(fascia, regime)
appresi sulla metà di taratura; banda osservata dalla metà di prova (tabella_*.json). Più la prova di monotonia (P-T4)
su 24 traiettorie sintetiche variate per classe. Uso: python -I curva_video.py <cartella>"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stima_v5 as S5
import prove_v5 as PV
S4 = S5.S4
D = sys.argv[1]
TAUS = [round(0.5 * i, 1) for i in range(61)]


def traccia(cl, v, w=0.0, acc=0.0, seme=1, T=60):
    rng = np.random.default_rng(seme); R = json.load(open(os.path.join(D, "ris_%s.json" % ("aerei" if cl == "aerei_veloci" else cl))))
    p = S5.parametri(cl, R["fq_scelto"]); f = None
    pos = np.array([-6000.0, 2000.0, 1500.0]) if cl == "aerei_veloci" else np.array([600.0, -400.0, 120.0])
    hd, sp = 0.0 if cl == "aerei_veloci" else math.pi / 2, v
    for k in range(T + 1):
        z, Rm = PV.misura(cl, pos, rng)
        if f is None: f = S5.IMM4(z, Rm, float(k), p)
        else: f.prevedi(float(k)); f.aggiorna(z, Rm)
        hd += w; sp += acc; pos = pos + sp * np.array([math.cos(hd), math.sin(hd), 0.0])
    return f, R


def curva(f, R, r0):
    pr = S5.predizione_pesi_fissati(f, [max(t, 1e-3) for t in TAUS], passo=0.5)
    modo = S5.NOMI4[int(np.argmax(f.mu))]
    C, r90, a_used = [], [], []
    for (tau, mu, xs, Ps) in pr:
        mix = S5.con_rif((mu, xs, Ps), R["srif_scelto"])
        C.append(S4.confidenza(mix, dict(dims=[0, 1, 2], A=r0 ** 2 * np.eye(3), c=None), n=40))
        et = PV.fascia(max(tau, 1.0)) or "21-30"
        a = R["astar"].get(et + "|" + modo, R["astar"].get(et, 0.9)); a_used.append(round(a, 4))
        r90.append(S4.raggio_per_livello(mix, min(a, 0.9995), (0, 1, 2), n=28, iter_=26))
    return C, r90, a_used, modo


def violazioni(C):
    return sum(1 for a, b in zip(C, C[1:]) if b > a + 1e-9)


out = {"stato": "calcolato nel modello (IMM a quattro regimi, pesi fissati) con parametri tarati su traiettorie pubbliche "
                 "(metà di taratura) e sensore simulato; banda osservata sulla metà di prova; nessuna misura su hardware",
       "formula": {"sigma2": "Σ_j(τ) = F_j(τ) P_j0 F_j(τ)ᵀ + Q_j(τ) + σ_rif² I (per regime j, pesi μ_j fissati alla perdita)",
                   "C": "C(τ) = min_{s≤τ} Σ_j μ_j · P(‖x − m(s)‖ ≤ r0 | x ~ N(m_j(s), Σ_j(s))) (sfera 3D centrata sulla previsione, integrale esatto a quadratura)",
                   "raggio": "r_0,9(τ) = raggio della sfera centrata sulla previsione con C = a*(fascia(τ), regime dominante); a* = quantile 0,9 del PIT sulla metà di taratura (ricalibrazione isotonica)",
                   "caso_1regime_2D": "σ²(τ) = σ0² + 2σ0v·τ + σv²·τ² + q·τ³/3 + σ_rif²; C = 1 − exp(−r²/2σ²); r_α = k_α σ, k_0,9 = 2,146"},
       "mezzi": {}}
for cl, v, nome, r0 in (("aerei_veloci", 210.0, "aereo_210", 150.0), ("droni_ala_fissa", 45.0, "drone_45", 80.0)):
    f, R = traccia(cl, v)
    C, r90, a, modo = curva(f, R, r0)
    Cm = S5.minimo_progressivo(C)
    tab = json.load(open(os.path.join(D, "tabella_%s.json" % ("aerei" if cl == "aerei_veloci" else cl))))[cl]
    banda = {et: dict(osservata=tab["cal"][et]["oss"], wilson_per_caso=tab["cal"][et]["wilson"],
                      bootstrap_mezzi=tab["cal"][et]["boot_mezzi"], n=tab["cal"][et]["n"], mezzi=tab["cal"][et]["mezzi"], r90_mediano_reale_m=tab["area"][et]["r90_mediano_m"]["r90_cal"])
             for et in ["1-2", "3-5", "6-10", "11-20", "21-30"]}
    out["mezzi"][nome] = dict(classe=cl, velocita_m_s=v, traiettoria="sintetica rettilinea, 60 s di inseguimento a 1 Hz",
                              regime_dominante=modo, sigma_rif_m=R["srif_scelto"], fattore_q=R["fq_scelto"], r0_m=r0,
                              tempi_s=TAUS, C=[round(c, 5) for c in Cm], C_grezza=[round(c, 5) for c in C],
                              violazioni_monotonia_grezza=violazioni(C), violazioni_monotonia=violazioni(Cm),
                              raggio_0_9_m=[round(r, 1) for r in np.maximum.accumulate(r90)], raggio_0_9_grezzo_m=[round(r, 1) for r in r90], nota_raggio="massimo progressivo: la regione non si restringe mai senza osservazione (a* cambia fra fasce)", livello_nominale_a_star=a,
                              banda_osservata_copertura_0_9=banda,
                              nota_banda="copertura osservata della regione r_0,9 per fascia di τ, su traiettorie reali della stessa classe (non di questo mezzo); i casi sono correlati dentro un mezzo")
# P-T4: monotonia su 24 traiettorie variate per classe
mono = {}
rng = np.random.default_rng(20261115)
for cl, v0, r0 in (("aerei_veloci", 120.0, 150.0), ("droni_ala_fissa", 25.0, 40.0)):
    grezze, dopo = 0, 0
    for s in range(24):
        f, R = traccia(cl, v0 * (0.6 + 1.2 * rng.random()), w=rng.normal(0, 0.02), acc=rng.normal(0, 0.3), seme=100 + s)
        pr = S5.predizione_pesi_fissati(f, [max(t, 1e-3) for t in TAUS], passo=0.5)
        C = [S4.confidenza(S5.con_rif(p[1:], R["srif_scelto"]), dict(dims=[0, 1, 2], A=r0 ** 2 * np.eye(3), c=None), n=40) for p in pr]
        grezze += violazioni(C); dopo += violazioni(S5.minimo_progressivo(C))
    mono[cl] = dict(traiettorie=24, passi=60, violazioni_grezze=grezze, violazioni_dopo_minimo=dopo)
out["prova_monotonia"] = mono
json.dump(out, open(os.path.join(D, "curva_video.json"), "w"), indent=1, ensure_ascii=False)
for k, m in out["mezzi"].items():
    print(k, m["regime_dominante"], "C", m["C"][::10], "r90", m["raggio_0_9_m"][::10], "viol", m["violazioni_monotonia_grezza"])
print(mono)
