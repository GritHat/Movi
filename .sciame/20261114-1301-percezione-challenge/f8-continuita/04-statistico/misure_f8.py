#!/usr/bin/env python3
"""sciame-statistico, f8 corsia A: come si valuta una previsione probabilistica di posizione, applicato ai dati dello sciame.
Python puro, semi fissati. Uso (un lancio alla volta, ciascuno sotto timeout 120):
  PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -B misure_f8.py tabelle|misure|fotogrammi|conforme
Che cosa NON e' mio: il filtro Ax (riscritto dall'avversario in f2/04-torneo/torneo_parte2.py) e i generatori g1 (avversario)
e g2 (copia di truth() di tracciamento). Li importo senza modificarli. Sono miei: le misure, i semi, le miscele, la capsula."""
import bisect
import math
import os
import random
import sys

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(QUI, "..", "..", "f2", "04-torneo")))
import torneo_parte2 as tp  # noqa: E402

DT, SIG, R, NV = tp.DT, tp.SIG, tp.R, tp.NV
Q = 0.2
C50, C90, C95 = 1.3863, 4.6052, 5.9915  # quantili chi-quadro a 2 gradi
KINDS = ("prosegue", "sosta", "torna", "svolta")
MIX_T = {"prosegue": 0.60, "sosta": 0.15, "torna": 0.10, "svolta": 0.15}  # miscela del torneo (G1)
MIX_SQ = {"prosegue": 0.90, "sosta": 0.10, "torna": 0.0, "svolta": 0.0}   # «squadra» (fissata nelle previsioni)
MIX_GI = {"prosegue": 0.50, "sosta": 0.20, "torna": 0.20, "svolta": 0.10}  # «giurato» (fissata nelle previsioni)
HORS = (0.5, 1.0, 2.0, 3.0, 5.0)
Z95 = 1.959964


# ------------------------------------------------------------------ strumenti
def wilson(k, n, z=Z95):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def binom_pmf(n, p):
    return [math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]


def binom_cdf_le(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def binom_ge(k, n, p):
    return 1.0 - binom_cdf_le(k - 1, n, p) if k > 0 else 1.0


def cp_lower_onesided(k, n, conf=0.95):
    """Limite inferiore di Clopper-Pearson a una coda."""
    if k == 0:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if binom_ge(k, n, m) < 1 - conf:
            lo = m
        else:
            hi = m
    return lo


def beta_quantile(a, b, prob):
    """Quantile di Beta(a,b) con a,b interi: P(Beta<=x) = P(Bin(a+b-1, x) >= a)."""
    n = a + b - 1
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if binom_ge(a, n, m) < prob:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def quant(sorted_v, p):
    if not sorted_v:
        return float("nan")
    i = min(len(sorted_v) - 1, max(0, int(math.ceil(p * len(sorted_v))) - 1))
    return sorted_v[i]


def wquant(pairs, p):
    """Quantile pesato: pairs = [(valore, peso)]."""
    pairs = sorted(pairs)
    tot = sum(w for _, w in pairs)
    acc = 0.0
    for v, w in pairs:
        acc += w
        if acc >= p * tot:
            return v
    return pairs[-1][0]


def phi(z):
    return math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def crps_gauss(mu, sd, y):
    z = (y - mu) / sd
    return sd * (z * (2 * Phi(z) - 1) + 2 * phi(z) - 1 / math.sqrt(math.pi))


def passaggio(traj, rnd, frames=False):
    """Come reappear_d2 del torneo: misure ai fotogrammi 0..NV-1, poi buio, poi la misura all'ultimo fotogramma.
    Rende gli scarti rispetto al punto previsto dal filtro (velocita' costante) e rispetto all'ultima posizione filtrata."""
    n = len(traj)
    zs = [(p[0] + rnd.gauss(0, SIG), p[1] + rnd.gauss(0, SIG)) for p in traj]
    ax, ay = tp.Ax(Q), tp.Ax(Q)
    lx = ly = vx = vy = 0.0
    hits = []
    for k in range(n - 1):
        ax.predict()
        ay.predict()
        if k < NV:
            ax.update(zs[k][0])
            ay.update(zs[k][1])
            if k == NV - 1:
                lx, ly, vx, vy = ax.x, ay.x, ax.v, ay.v
        elif frames:
            S = ax.a + R
            hits.append(((zs[k][0] - ax.x) ** 2 + (zs[k][1] - ay.x) ** 2) / S <= C90)
    ax.predict()
    ay.predict()
    S = ax.a + R
    zx, zy = zs[-1]
    rec = (zx - ax.x, zy - ay.x, S, zx - lx, zy - ly, vx, vy, (n - NV) * DT)
    return (rec, hits) if frames else rec


def deriva(rec):
    ex, ey, S, fx, fy, vx, vy, hor = rec
    ecv = math.hypot(ex, ey)
    ef = math.hypot(fx, fy)
    sp = max(1e-6, math.hypot(vx, vy))
    ux, uy = vx / sp, vy / sp
    epar = fx * ux + fy * uy
    eperp = -fx * uy + fy * ux
    L = sp * hor + 0.3
    W = 0.15 + 0.2 * sp * hor
    return {"ecv": ecv, "d2": ecv * ecv / S, "ef": ef, "S": S, "caps": max(abs(epar) / L, abs(eperp) / W), "LW": L * W,
            "ex": ex, "ey": ey, "fx": fx, "fy": fy}


def pool_g1(seed, D, n):
    rnd = random.Random(seed)
    out = {}
    for kind in KINDS:
        out[kind] = [deriva(passaggio(tp.g1(rnd, D, kind)[0], rnd)) for _ in range(n)]
    return out


def seed_of(base, D):
    return base + int(round(D * 10))


# ------------------------------------------------------------------ tabelle (numerosita', riconteggio)
def m_tabelle():
    print("== S1. Numerosita' (binomiale esatta, a una coda, alfa 0,05) ==")
    for (p0, p1, side) in ((0.90, 0.80, "giu"), (0.90, 0.95, "su"), (0.80, 0.90, "su"), (0.95, 0.90, "giu")):
        first, stable = None, None
        last_bad = 0
        for n in range(10, 701):
            pm0 = binom_pmf(n, p0)
            pm1 = binom_pmf(n, p1)
            if side == "giu":  # rifiuto se X <= c
                acc, c = 0.0, -1
                for i in range(n + 1):
                    if acc + pm0[i] > 0.05:
                        break
                    acc += pm0[i]
                    c = i
                power = sum(pm1[: c + 1]) if c >= 0 else 0.0
            else:  # rifiuto se X >= c
                acc, c = 0.0, n + 1
                for i in range(n, -1, -1):
                    if acc + pm0[i] > 0.05:
                        break
                    acc += pm0[i]
                    c = i
                power = sum(pm1[c:]) if c <= n else 0.0
            if power >= 0.80:
                if first is None:
                    first = n
            else:
                last_bad = n
        stable = last_bad + 1
        print("  H0 p=%.2f contro p=%.2f: primo n con potenza >= 0,80: %s ; n da cui la potenza resta >= 0,80: %s" % (
            p0, p1, first, stable))
    print("  Potenza con n fissato per H0 p=0,90 contro 0,80 (rifiuto se X<=c):")
    for n in (20, 30, 60, 100, 150, 200):
        pm0, pm1 = binom_pmf(n, 0.90), binom_pmf(n, 0.80)
        acc, c = 0.0, -1
        for i in range(n + 1):
            if acc + pm0[i] > 0.05:
                break
            acc += pm0[i]
            c = i
        print("    n=%3d: c=%3d  alfa vera=%.3f  potenza=%.3f" % (n, c, acc, sum(pm1[: c + 1]) if c >= 0 else 0.0))
    print("  Intervallo di Wilson al 95 %% attorno a 0,90 e limite inferiore a una coda (Clopper-Pearson 95 %%):")
    for n in (20, 30, 40, 60, 100, 150, 200, 400, 1000):
        k = round(0.9 * n)
        lo, hi = wilson(k, n)
        lo12, hi12 = wilson(k, n, 2.8653)  # Bonferroni su 12 celle: z per 1-0,05/24
        print("    n=%4d k=%4d: Wilson [%.3f; %.3f] semiampiezza %.3f | con 12 celle (z=2,87) [%.3f; %.3f] | CP inf. a una coda %.3f | n su n -> CP inf. %.3f" % (
            n, k, lo, hi, (hi - lo) / 2, lo12, hi12, cp_lower_onesided(k, n), cp_lower_onesided(n, n)))
    print("  Per dichiarare «copertura >= 0,80» (CP a una coda 95 %%) servono almeno k su n:")
    for n in (30, 40, 60, 100):
        k = next(k for k in range(n + 1) if cp_lower_onesided(k, n) >= 0.80)
        print("    n=%3d: k>=%3d (%.3f) ; P(riuscirci | copertura vera 0,90)=%.3f ; | vera 0,95)=%.3f ; | vera 0,80)=%.3f" % (
            n, k, k / n, binom_ge(k, n, 0.90), binom_ge(k, n, 0.95), binom_ge(k, n, 0.80)))

    print("\n== S2. Riconteggio con Wilson dai conteggi del torneo e del nucleo (k = round(p*n): +-2 conteggi) ==")
    righe = [
        ("G1 tutti D=0,5 (nom 95)", 0.977, 4000, "risultati_A_parte2.txt"),
        ("G1 tutti D=1 (nom 95)", 0.934, 4000, "risultati_A_parte2.txt"),
        ("G1 tutti D=2 (nom 95)", 0.927, 4000, "risultati_A_parte2.txt"),
        ("G1 tutti D=3 (nom 95)", 0.938, 4000, "risultati_A_parte2.txt"),
        ("G2 tutti D=0,5 (nom 95)", 0.922, 4000, "risultati_A_parte2.txt"),
        ("G2 tutti D=1 (nom 95)", 0.895, 4000, "risultati_A_parte2.txt"),
        ("G2 tutti D=2 (nom 95)", 0.916, 4000, "risultati_A_parte2.txt"),
        ("G2 tutti D=3 (nom 95)", 0.932, 4000, "risultati_A_parte2.txt"),
        ("G1 prosegue D=2", 1.000, 2437, "risultati_A_parte2.txt"),
        ("G1 sosta D=2", 0.955, 595, "risultati_A_parte2.txt"),
        ("G1 svolta D=2", 0.839, 583, "risultati_A_parte2.txt"),
        ("G1 torna D=0,5", 0.822, 416, "risultati_A_parte2.txt"),
        ("G1 torna D=1", 0.664, 422, "risultati_A_parte2.txt"),
        ("G1 torna D=2", 0.561, 385, "risultati_A_parte2.txt"),
        ("G1 torna D=3", 0.568, 424, "risultati_A_parte2.txt"),
        ("G2 con manovra nel buio D=1", 0.711, 1143, "risultati_A_parte2.txt"),
        ("G2 con manovra nel buio D=2", 0.841, 1848, "risultati_A_parte2.txt"),
        ("G3 tutte le riemersioni", 0.890, 4000, "risultati_A_parte2.txt"),
        ("G3 torna, buio 0,75-1,5 s", 7 / 126, 126, "risultati_A_parte2.txt"),
        ("G3 torna, buio 1,5-2,5 s", 15 / 173, 173, "risultati_A_parte2.txt"),
        ("G3 torna, buio 2,5-3,5 s", 54 / 161, 161, "risultati_A_parte2.txt"),
        ("G3 torna, buio >= 3,5 s", 95 / 121, 121, "risultati_A_parte2.txt"),
        ("nucleo con C6, demo, torna (col)", 0.500, 400, "v2_C6.txt"),
        ("nucleo con C6, demo, torna (wmin)", 0.472, 400, "v2_C6.txt"),
        ("nucleo con C6, demo, prosegue", 1.000, 2000, "v2_C6.txt"),
        ("nucleo con C6, T1, torna (col)", 0.665, 400, "v2_C6.txt"),
    ]
    for lab, p, n, f in righe:
        k = round(p * n)
        lo, hi = wilson(k, n)
        print("  %-36s %5d/%-5d = %.3f  Wilson 95 %% [%.3f; %.3f]   (%s)" % (lab, k, n, k / n, lo, hi, f))
    # paradosso della media: copertura complessiva in funzione della quota di chi torna (dati G1, D=2)
    print("  Paradosso della media (G1, D=2, nominale 95): copertura complessiva = somma dei pesi per classe")
    cov = {"prosegue": 1.000, "sosta": 0.955, "svolta": 0.839, "torna": 0.561}
    for name, mix in (("torneo 60/15/10/15", MIX_T), ("squadra 90/10/0/0", MIX_SQ), ("giurato 50/20/20/10", MIX_GI),
                      ("solo manovre 0/33/33/33", {"prosegue": 0, "sosta": 1 / 3, "torna": 1 / 3, "svolta": 1 / 3})):
        print("    %-26s -> %.3f" % (name, sum(mix[k] * cov[k] for k in cov)))


# ------------------------------------------------------------------ misure sul filtro (G1 per classe, G2)
def riga(lab, recs, sref, pesi=None):
    """recs: lista di (derivato, peso)."""
    tot = sum(w for _, w in recs)
    n = len(recs)

    def frac(c):
        return sum(w for d, w in recs if d["d2"] <= c) / tot

    c50, c90, c95 = frac(C50), frac(C90), frac(C95)
    S = recs[0][0]["S"]
    sd = math.sqrt(S)
    r90 = math.sqrt(C90 * S)
    mcv = wquant([(d["ecv"], w) for d, w in recs], 0.5)
    pcv = wquant([(d["ecv"], w) for d, w in recs], 0.9)
    mf = wquant([(d["ef"], w) for d, w in recs], 0.5)
    pf = wquant([(d["ef"], w) for d, w in recs], 0.9)
    crps_k = sum(w * 0.5 * (crps_gauss(0, sd, d["ex"]) + crps_gauss(0, sd, d["ey"])) for d, w in recs) / tot
    crps_r = sum(w * 0.5 * (crps_gauss(0, sref, d["fx"]) + crps_gauss(0, sref, d["fy"])) for d, w in recs) / tot
    mae_cv = sum(w * 0.5 * (abs(d["ex"]) + abs(d["ey"])) for d, w in recs) / tot
    mae_f = sum(w * 0.5 * (abs(d["fx"]) + abs(d["fy"])) for d, w in recs) / tot
    nll = sum(w * (math.log(2 * math.pi * S) + 0.5 * d["d2"]) for d, w in recs) / tot
    if pesi is None:
        k90 = sum(1 for d, _ in recs if d["d2"] <= C90)
        lo, hi = wilson(k90, n)
        ci = "[%.3f;%.3f]" % (lo, hi)
    else:
        ci = "(pesata)     "
    print("  %-22s n=%5d | cop 50/90/95: %.3f %.3f %.3f  IC90 %s | r90 %.2f m area %.1f m2 | err CV med %.2f p90 %.2f | fermo med %.2f p90 %.2f | CRPS filtro %.3f rif %.3f ab %+.2f | MAE CV %.3f fermo %.3f | NLL %.2f" % (
        lab, n, c50, c90, c95, ci, r90, math.pi * r90 * r90, mcv, pcv, mf, pf, crps_k, crps_r,
        1 - crps_k / crps_r if crps_r > 0 else float("nan"), mae_cv, mae_f, nll))
    return {"c50": c50, "c90": c90, "mcv": mcv, "pcv": pcv, "mf": mf, "pf": pf, "crps_k": crps_k, "crps_r": crps_r}


def m_misure():
    N = 1500
    print("== S3. Misure sul cerchio del filtro (q=0,2) — generatore g1 dell'avversario, per classe e per orizzonte ==")
    print("   unita' = il passaggio; orizzonte effettivo D + 1 fotogramma; N=%d per classe per la prova, %d per la taratura del riferimento" % (N, 600))
    print("   CRPS per componenti (m, medio su x e y); riferimento = gaussiana su «fermo» con dispersione tarata a parte; ab = 1 - CRPS/CRPS_rif")
    for D in HORS:
        cal = pool_g1(seed_of(81000, D), D, 600)
        # dispersione del riferimento sulla miscela del torneo (insieme di taratura)
        num = sum(MIX_T[k] * sum(d["fx"] ** 2 + d["fy"] ** 2 for d in cal[k]) / (2 * len(cal[k])) for k in KINDS)
        sref = math.sqrt(num)
        test = pool_g1(seed_of(82000, D), D, N)
        print("-- D=%.1f s (riferimento: sigma per asse %.2f m)" % (D, sref))
        for k in KINDS:
            riga(k, [(d, 1.0) for d in test[k]], sref)
        for name, mix in (("MISCELA 60/15/10/15", MIX_T), ("«giurato» 50/20/20/10", MIX_GI)):
            recs = [(d, mix[k] / len(test[k])) for k in KINDS for d in test[k] if mix[k] > 0]
            riga(name, recs, sref, pesi=True)
    print("\n== S3b. Lo stesso su g2 (copia di truth() di tracciamento), N=3000 per orizzonte ==")
    for D in HORS:
        rnd = random.Random(seed_of(83000, D))
        no = int(round(D / DT))
        con, senza = [], []
        calf = []
        rc = random.Random(seed_of(84000, D))
        for _ in range(600):
            traj, ev = tp.g2(rc, NV + no + 1)
            d = deriva(passaggio(traj, rc))
            calf.append(d["fx"] ** 2 + d["fy"] ** 2)
        sref = math.sqrt(sum(calf) / (2 * len(calf)))
        for _ in range(3000):
            traj, ev = tp.g2(rnd, NV + no + 1)
            d = deriva(passaggio(traj, rnd))
            (con if any(e >= NV for e in ev) else senza).append((d, 1.0))
        print("-- D=%.1f s (riferimento: sigma per asse %.2f m)" % (D, sref))
        riga("tutti", con + senza, sref)
        riga("con manovra nel buio", con, sref)
        riga("senza manovra nel buio", senza, sref)


# ------------------------------------------------------------------ fotogrammi correlati
def m_fotogrammi():
    print("== S4. Correlazione fra i fotogrammi dello stesso passaggio (indicatore «misura dentro il cerchio al 90 %») ==")
    for D in (1.0, 3.0):
        rnd = random.Random(seed_of(85000, D))
        rows = []
        for i in range(1500):
            u = rnd.random()
            kind = "prosegue" if u < 0.60 else "sosta" if u < 0.75 else "torna" if u < 0.85 else "svolta"
            traj, _ = tp.g1(rnd, D, kind)
            _, hits = passaggio(traj, rnd, frames=True)
            rows.append([1.0 if h else 0.0 for h in hits])
        m = len(rows[0])
        g = len(rows)
        means = [sum(r) / m for r in rows]
        gm = sum(means) / g
        msb = m * sum((x - gm) ** 2 for x in means) / (g - 1)
        msw = sum(sum((v - means[i]) ** 2 for v in r) for i, r in enumerate(rows)) / (g * (m - 1))
        icc = (msb - msw) / (msb + (m - 1) * msw)
        deff = 1 + (m - 1) * icc
        se_fr = math.sqrt(gm * (1 - gm) / (g * m))
        se_cl = math.sqrt(sum((x - gm) ** 2 for x in means) / (g - 1) / g)
        print("  D=%.0f s: %d passaggi x %d fotogrammi; copertura per fotogramma %.3f; correlazione intraclasse %.3f; effetto del disegno %.1f; fotogrammi efficaci per passaggio %.2f" % (
            D, g, m, gm, icc, deff, m / deff))
        print("          errore tipo se si contano i fotogrammi come indipendenti %.4f; per passaggio (giusto) %.4f; rapporto %.1f" % (
            se_fr, se_cl, se_cl / se_fr))


# ------------------------------------------------------------------ previsione conforme
def cq(scores, alpha=0.10):
    """Quantile conforme: il k-esimo piu' piccolo, k = ceil((n+1)(1-alpha)); infinito se k > n."""
    n = len(scores)
    k = int(math.ceil((n + 1) * (1 - alpha) - 1e-12))
    if k > n:
        return float("inf")
    return sorted(scores)[k - 1]


def frac_le(sorted_v, x):
    return bisect.bisect_right(sorted_v, x) / len(sorted_v)


def draw(rnd, pools, mix, key, n):
    ks = [k for k in KINDS if mix[k] > 0]
    ws = [mix[k] for k in ks]
    out = []
    for _ in range(n):
        k = rnd.choices(ks, ws)[0]
        out.append(rnd.choice(pools[k])[key])
    return out


def m_conforme():
    NP = 1500
    B = 400
    rnd = random.Random(86000)
    print("== S5. Previsione conforme a insieme separato (livello 0,90). Vasche: %d passaggi per classe per la taratura e %d per la prova, semi diversi ==" % (NP, NP))
    pools = {}
    for D in HORS:
        cal = pool_g1(seed_of(87000, D), D, NP)
        tst = pool_g1(seed_of(88000, D), D, NP)
        pools[D] = (cal, tst, {k: {key: sorted(d[key] for d in tst[k]) for key in ("ecv", "ef", "caps", "d2")} for k in KINDS})

    def cover(D, key, x, mix):
        st = pools[D][2]
        return sum(mix[k] * frac_le(st[k][key], x) for k in KINDS if mix[k] > 0)

    print("-- (a) scambiabile: taratura e prova dalla stessa miscela 60/15/10/15, D=2 s, punteggio = distanza dal punto a velocita' costante; %d ripetizioni" % B)
    D = 2.0
    for n in (20, 30, 60, 100, 200, 500):
        covs, rad = [], []
        for _ in range(B):
            qh = cq(draw(rnd, pools[D][0], MIX_T, "ecv", n))
            covs.append(cover(D, "ecv", qh, MIX_T))
            rad.append(qh)
        covs.sort()
        k = int(math.ceil((n + 1) * 0.9 - 1e-12))
        print("   n=%3d: copertura realizzata media %.3f, 5o perc. %.3f, 95o perc. %.3f | teoria Beta(%d,%d): media %.3f, 5o perc. %.3f, 95o %.3f | raggio mediano %.2f m" % (
            n, sum(covs) / B, quant(covs, 0.05), quant(covs, 0.95), k, n + 1 - k, k / (n + 1), beta_quantile(k, n + 1 - k, 0.05),
            beta_quantile(k, n + 1 - k, 0.95), sorted(rad)[B // 2]))
    print("   n minimo perche' la copertura realizzata stia >= soglia con probabilita' 0,95 (teoria Beta, livello nominale 0,90):")
    for thr in (0.80, 0.85, 0.87):
        nmin = None
        for n in range(10, 2001):
            k = int(math.ceil((n + 1) * 0.9 - 1e-12))
            if k <= n and beta_quantile(k, n + 1 - k, 0.05) >= thr:
                nmin = n
                break
        print("     soglia %.2f: n >= %s" % (thr, nmin))

    print("-- (b) spostamento: taratura sulla «squadra» 90/10/0/0 (n=100), prova su «squadra» e su «giurato» 50/20/20/10")
    for D in (1.0, 2.0, 3.0):
        cs, cg, rad = [], [], []
        for _ in range(B):
            qh = cq(draw(rnd, pools[D][0], MIX_SQ, "ecv", 100))
            cs.append(cover(D, "ecv", qh, MIX_SQ))
            cg.append(cover(D, "ecv", qh, MIX_GI))
            rad.append(qh)
        cg.sort()
        print("   D=%.0f s: raggio mediano %.2f m; copertura su «squadra» %.3f; su «giurato» media %.3f (5o-95o perc. %.3f-%.3f); per classe: %s" % (
            D, sorted(rad)[B // 2], sum(cs) / B, sum(cg) / B, quant(cg, 0.05), quant(cg, 0.95),
            ", ".join("%s %.2f" % (k, frac_le(pools[D][2][k]["ecv"], sorted(rad)[B // 2])) for k in KINDS)))

    print("-- (c) massimo sulle classi (taratura per comportamento prescritto, 50 passaggi per classe): copertura per classe e prezzo in area")
    for D in HORS:
        S = pools[D][1]["prosegue"][0]["S"]
        r90 = math.sqrt(C90 * S)
        akf = math.pi * r90 * r90
        ckf = {k: frac_le(pools[D][2][k]["d2"], C90) for k in KINDS}
        lwm = sum(d["LW"] for k in KINDS for d in pools[D][1][k]) / (4 * NP)
        print("   D=%.1f s | cerchio del filtro al 90 %%: raggio %.2f m, area %.1f m2, copertura per classe %s, «giurato» %.3f" % (
            D, r90, akf, " ".join("%s %.2f" % (k[:4], ckf[k]) for k in KINDS), sum(MIX_GI[k] * ckf[k] for k in KINDS)))
        for lab, key, classi in (("disco su vel. costante, 4 classi", "ecv", KINDS), ("disco su «fermo», 4 classi", "ef", KINDS),
                                 ("capsula, 3 classi sull'asse", "caps", KINDS[:3]), ("capsula, 4 classi", "caps", KINDS)):
            qs, pc = [], {k: [] for k in KINDS}
            cgi = []
            for _ in range(B):
                qh = max(cq([rnd.choice(pools[D][0][k])[key] for _ in range(50)]) for k in classi)
                qs.append(qh)
                for k in KINDS:
                    pc[k].append(frac_le(pools[D][2][k][key], qh))
                cgi.append(sum(MIX_GI[k] * pc[k][-1] for k in KINDS))
            qm = sorted(qs)[B // 2]
            area = (4 * qm * qm * lwm) if key == "caps" else math.pi * qm * qm
            cgi.sort()
            print("        %-34s soglia mediana %.2f%s area %.1f m2 (%.1f volte il cerchio) | copertura media per classe %s | «giurato» %.3f (5o perc. %.3f)" % (
                lab, qm, "" if key == "caps" else " m", area, area / akf,
                " ".join("%s %.2f" % (k[:4], sum(pc[k]) / B) for k in KINDS), sum(cgi) / B, quant(cgi, 0.05)))

    print("-- (d) una sola soglia per tutti gli orizzonti (punteggio normalizzato d = distanza/sigma del filtro, miscela 60/15/10/15, n=100 in tutto) contro una soglia per orizzonte (n=100 ciascuno)")
    res_p = {D: [] for D in HORS}
    res_h = {D: [] for D in HORS}
    for _ in range(B):
        sc = []
        for D in HORS:
            sc += draw(rnd, pools[D][0], MIX_T, "d2", 20)
        qp = cq(sc)
        for D in HORS:
            res_p[D].append(cover(D, "d2", qp, MIX_T))
            res_h[D].append(cover(D, "d2", cq(draw(rnd, pools[D][0], MIX_T, "d2", 100)), MIX_T))
    print("   " + " | ".join("D=%.1f: unica %.3f, per orizzonte %.3f" % (D, sum(res_p[D]) / B, sum(res_h[D]) / B) for D in HORS))


# ------------------------------------------------------------------ unione cerchio + capsula (aggiunta dopo S5: previsione P13)
def pool_g1_raw(seed, D, n):
    rnd = random.Random(seed)
    out = {}
    for kind in KINDS:
        rows = []
        for _ in range(n):
            rec = passaggio(tp.g1(rnd, D, kind)[0], rnd)
            d = deriva(rec)
            d["rec"] = rec
            d["u"] = min(math.sqrt(d["d2"] / C90), d["caps"])
            rows.append(d)
        out[kind] = rows
    return out


def m_unione():
    NP, B = 1500, 400
    rnd = random.Random(89000)
    print("== S6. Regione = cerchio del filtro (scalato di s) UNITO alla capsula (scalata di s); soglia = massimo sulle 4 classi del quantile conforme 0,90; 50 passaggi per classe ==")
    for D in HORS:
        cal = pool_g1_raw(seed_of(90000, D), D, NP)
        tst = pool_g1_raw(seed_of(91000, D), D, NP)
        st = {k: sorted(d["u"] for d in tst[k]) for k in KINDS}
        S = tst["prosegue"][0]["S"]
        r90 = math.sqrt(C90 * S)
        akf = math.pi * r90 * r90
        qs, pc, cg = [], {k: [] for k in KINDS}, []
        for _ in range(B):
            qh = max(cq([rnd.choice(cal[k])["u"] for _ in range(50)]) for k in KINDS)
            qs.append(qh)
            for k in KINDS:
                pc[k].append(frac_le(st[k], qh))
            cg.append(sum(MIX_GI[k] * pc[k][-1] for k in KINDS))
        qm = sorted(qs)[B // 2]
        # area vera dell'unione alla soglia mediana: cerchio + parte della capsula fuori dal cerchio (campionamento)
        tot, m = 0.0, 0
        for k in KINDS:
            for d in tst[k][:150]:
                ex, ey, S_, fx, fy, vx, vy, hor = d["rec"]
                sp = max(1e-6, math.hypot(vx, vy))
                ux, uy = vx / sp, vy / sp
                L = (sp * hor + 0.3) * qm
                W = (0.15 + 0.2 * sp * hor) * qm
                px, py = fx - ex, fy - ey  # punto previsto, con origine nell'ultima posizione
                rr = (qm * r90) ** 2
                fuori = 0
                for _ in range(200):
                    a, b = rnd.uniform(-L, L), rnd.uniform(-W, W)
                    x, y = a * ux - b * uy, a * uy + b * ux
                    fuori += (x - px) ** 2 + (y - py) ** 2 > rr
                tot += math.pi * rr + 4 * L * W * fuori / 200
                m += 1
        area = tot / m
        cg.sort()
        print("  D=%.1f s: soglia mediana s=%.2f | area %.1f m2 = %.2f volte il cerchio al 90 %% (%.1f m2) | copertura media per classe %s | minima fra le ripetizioni (5o perc.) %s | «giurato» %.3f (5o perc. %.3f)" % (
            D, qm, area, area / akf, akf, " ".join("%s %.3f" % (k[:4], sum(pc[k]) / B) for k in KINDS),
            " ".join("%s %.2f" % (k[:4], quant(sorted(pc[k]), 0.05)) for k in KINDS), sum(cg) / B, quant(cg, 0.05)))


# ------------------------------------------------------------------ prova incrociata: taratura su g1, prova su g2 (previsione P14)
def m_incrociata():
    NP, B = 1500, 400
    rnd = random.Random(92000)
    print("== S7. Taratura su g1 (avversario), prova su g2 (tracciamento): unione col massimo sulle 4 classi (50 per classe) e disco conforme sulla miscela 60/15/10/15 (n=100) ==")
    for D in HORS:
        cal = pool_g1_raw(seed_of(90000, D), D, NP)
        r2 = random.Random(seed_of(93000, D))
        no = int(round(D / DT))
        tu = {"con": [], "senza": []}
        te = {"con": [], "senza": []}
        td = {"con": [], "senza": []}
        for _ in range(3000):
            traj, ev = tp.g2(r2, NV + no + 1)
            d = deriva(passaggio(traj, r2))
            key = "con" if any(e >= NV for e in ev) else "senza"
            tu[key].append(min(math.sqrt(d["d2"] / C90), d["caps"]))
            te[key].append(d["ecv"])
            td[key].append(d["d2"])
        for k in tu:
            tu[k].sort()
            te[k].sort()
        ncon, nsen = len(tu["con"]), len(tu["senza"])
        cu = {"con": [], "senza": []}
        ce = {"con": [], "senza": []}
        for _ in range(B):
            qh = max(cq([rnd.choice(cal[k])["u"] for _ in range(50)]) for k in KINDS)
            qe = cq(draw(rnd, cal, MIX_T, "ecv", 100))
            for k in cu:
                cu[k].append(frac_le(tu[k], qh))
                ce[k].append(frac_le(te[k], qe))

        def tot(c):
            return [(c["con"][i] * ncon + c["senza"][i] * nsen) / (ncon + nsen) for i in range(B)]
        tU, tE = sorted(tot(cu)), sorted(tot(ce))
        kf_con = sum(1 for x in td["con"] if x <= C90) / ncon
        kf_all = (sum(1 for x in td["con"] if x <= C90) + sum(1 for x in td["senza"] if x <= C90)) / (ncon + nsen)
        print("  D=%.1f s (con manovra nel buio n=%d): cerchio del filtro 90 %%: tutti %.3f, con manovra %.3f | unione: tutti %.3f (5o perc. %.3f), con manovra %.3f (5o perc. %.3f) | disco conforme sulla miscela: tutti %.3f, con manovra %.3f" % (
            D, ncon, kf_all, kf_con, sum(tU) / B, quant(tU, 0.05), sum(cu["con"]) / B, quant(sorted(cu["con"]), 0.05),
            sum(tE) / B, sum(ce["con"]) / B))


if __name__ == "__main__":
    {"tabelle": m_tabelle, "misure": m_misure, "fotogrammi": m_fotogrammi, "conforme": m_conforme, "unione": m_unione, "incrociata": m_incrociata}[sys.argv[1]]()
