"""Controllo statistico di f15/11-prove e f15/12-traiettorie (sciame-statistico).
Legge solo i file grezzi; scrive controllo.json e stampa le tavole. Tutto e' conto su simulazione e dati pubblici.
Uso: python -I controllo.py <cartella f15-lunga-portata>
"""
import json, os, re, sys, collections
import numpy as np
from scipy import stats

F15 = sys.argv[1]
Z = 1.959963984540054


def wilson(k, n, z=Z):
    if n == 0:
        return (None, None)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def cp(k, n, a=0.05):
    lo = 0.0 if k == 0 else stats.beta.ppf(a / 2, k, n - k + 1)
    hi = 1.0 if k == n else stats.beta.ppf(1 - a / 2, k + 1, n - k)
    return (lo, hi)


OUT = {}

# ---------- 1. ricalcolo dei Wilson nei JSON della simulazione ----------
def cammina(x, path, acc):
    if isinstance(x, dict):
        for k, v in x.items():
            cammina(v, path + [str(k)], acc)
    elif isinstance(x, list):
        if len(x) == 5 and all(isinstance(t, (int, float)) or t is None for t in x) and isinstance(x[0], int) and isinstance(x[1], int) and x[1] > 0 and x[3] is not None:
            acc.append(("/".join(path), x))
        else:
            for i, v in enumerate(x):
                cammina(v, path + [str(i)], acc)

scarti = []
tot = 0
for f in ["risultati_lp_interfaccia.json", "risultati_lp_prudente.json", "risultati_eventi.json"]:
    d = json.load(open(os.path.join(F15, "11-prove", f)))
    acc = []
    cammina(d, [], acc)
    for p, (k, n, _, lo, hi) in acc:
        tot += 1
        L, H = wilson(k, n)
        if abs(L - lo) > 0.002 or abs(H - hi) > 0.002:
            scarti.append((f, p, k, n, lo, hi, round(L, 4), round(H, 4)))
OUT["wilson_sim"] = {"triple": tot, "scarti_oltre_0_002": len(scarti), "esempi": scarti[:10]}
print("Wilson ricalcolati sui JSON di 11-prove:", tot, "terne; scarti > 0,002:", len(scarti))
for s in scarti[:10]:
    print("  ", s)

# ---------- 2. semi: indipendenza misurata ----------
ENT = 20261115
prime = {}
for sc in range(6):
    for cfg in range(3):          # 0 verita', 1 min, 2 alta
        for i in range(200):
            g = np.random.default_rng(np.random.SeedSequence(ENT, spawn_key=(sc, cfg, i)))
            prime[(sc, cfg, i)] = g.random(64)
M = np.array([v for v in prime.values()])
C = np.corrcoef(M)
off = C[~np.eye(len(C), dtype=bool)]
ver = {k: v for k, v in prime.items() if k[1] == 0}
OUT["semi"] = {
    "flussi": len(prime), "prime_estrazioni_distinte": len({v[0] for v in prime.values()}),
    "corr_max_abs_fra_flussi_64_estrazioni": float(np.max(np.abs(off))),
    "quota_corr_oltre_soglia_95": float(np.mean(np.abs(off) > Z / np.sqrt(64))),
    "verita_distinte_per_riga": "200 per scenario, condivise fra min e alta (spawn_key cfg=0): 1200 verita' per 2400 passaggi",
    "prudente": "spawn_key non contiene il chiamante: i 50 passaggi prudenti hanno gli stessi semi dei passaggi 0-49 del modo interfaccia (stesso campione, sottoinsieme appaiato)",
}
print("semi:", OUT["semi"])

# ---------- 3. correzioni per 'in tutte le righe' ----------
def sup_bonf(n, m, k=0):
    return cp(k, n, a=2 * 0.05 / m)[1]          # bilaterale a 0,05/m -> superiore a 0,025/m; uso unilaterale a 0,05/m
def sup_uni(n, m):
    return 1 - (0.05 / m) ** (1 / n)

corr = {
    "prudente: 0 passaggi con ciclo senza regione, 12 righe x 50": {"per_riga_sup_95": sup_uni(50, 1), "per_riga_sup_bonf12": sup_uni(50, 12), "unito_600_sup_95": sup_uni(600, 1)},
    "P1 alta 200/200 in A1, A2, S1 (3 righe)": {"per_riga_inf_95": (0.05) ** (1 / 200), "per_riga_inf_bonf3": (0.05 / 3) ** (1 / 200)},
    "identita 0/200 in 5 scenari x 2": {"per_riga_sup_95": sup_uni(200, 1), "per_riga_sup_bonf10": sup_uni(200, 10)},
    "perdita sensore 460/460": {"inf_95_unilat": 0.05 ** (1 / 460), "wilson": wilson(460, 460)},
}
OUT["correzioni"] = corr
print("correzioni:", json.dumps(corr, indent=1, default=float))

# ---------- 4. traiettorie: mezzi distinti, separazione, copertura per mezzo ----------
def mezzo(sc):
    m = re.match(r"atl_([0-9a-f]{6})$", sc)
    if m: return "icao:" + m.group(1), "icao:" + m.group(1)
    m = re.match(r"lhrzrh_TRAIN_(\d{4}-\d\d-\d\d)_(\w+?)_(avv|dec)$", sc)
    if m: return "volo:" + m.group(1) + "_" + m.group(2), "nvolo:" + m.group(2)
    m = re.match(r"trajair_(\d+)_(\d+)_(\d+)$", sc)
    if m: return "icao:%06x" % int(m.group(2)), "icao:%06x" % int(m.group(2))
    m = re.match(r"cmu_m100_volo\d+$", sc)
    if m: return "M100:" + sc, "M100"                           # un solo esemplare (fonte)
    m = re.match(r"alfa_(\d{14})", sc)
    if m: return "T28:" + m.group(1), "T28"                       # un solo esemplare (fonte)
    m = re.match(r"ngsim_us101_v(\d+)_\d+$", sc)
    if m: return "veicolo:" + m.group(1), "veicolo:" + m.group(1)
    m = re.match(r"fi_treno(\d+)_\d+$", sc)
    if m: return "treno:" + m.group(1), "treno:" + m.group(1)
    return "?" + sc, "?" + sc

R = json.load(open(os.path.join(F15, "12-traiettorie", "risultati_traiettorie.json")))
rng = np.random.default_rng(20261115)
trj = {}
for cl, dc in R["classi"].items():
    casi = dc["casi"]
    prova_sc = sorted({c["scena"] for c in casi})
    tutte = sorted(os.listdir(os.path.join(F15, "01-dati", "traiettorie", cl)))
    tara_sc = [s for s in tutte if s not in set(prova_sc)]
    m1p = {mezzo(s)[0] for s in prova_sc}; m1t = {mezzo(s)[0] for s in tara_sc}
    m2p = {mezzo(s)[1] for s in prova_sc}; m2t = {mezzo(s)[1] for s in tara_sc}
    info = {"tratti_prova": len(prova_sc), "tratti_taratura": len(tara_sc),
            "scene_in_entrambe": len(set(prova_sc) & set(tara_sc)),
            "unita1_prova": len(m1p), "unita1_in_entrambe": len(m1p & m1t),
            "unita2_prova": len(m2p), "unita2_in_entrambe": len(m2p & m2t),
            "unita2_elenco_se_poche": sorted(m2p) if len(m2p) < 6 else None,
            "per_D": {}}
    for D in R["durate"]:
        cc = [c for c in casi if c["D"] == D]
        n = len(cc); k = sum(c["dentro"] for c in cc); fa = sum(c["fuori_avv"] for c in cc)
        riga = {"casi": n, "dentro": k, "wilson_casi": wilson(k, n), "fuori_avv": fa}
        for liv, idx in (("u1", 0), ("u2", 1)):
            g = collections.defaultdict(list)
            for c in cc:
                g[mezzo(c["scena"])[idx]].append((c["dentro"], c["fuori_avv"]))
            keys = sorted(g)
            arr = [np.array(g[u], float) for u in keys]
            G = len(arr)
            pm = np.array([a[:, 0].mean() for a in arr])       # copertura media per unita'
            # Wilson con n = unita', k = n * media delle medie (stima per unita', pesi uguali)
            wl = wilson(pm.mean() * G, G)
            if G >= 5:
                bs = []
                for _ in range(2000):
                    s = rng.integers(0, G, G)
                    num = sum(arr[i][:, 0].sum() for i in s); den = sum(len(arr[i]) for i in s)
                    bs.append(num / den)
                bq = (float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975)))
            else:
                bq = None
            fu = sum(1 for a in arr if a[:, 1].any())
            riga[liv] = {"unita": G, "media_per_unita": float(pm.mean()), "wilson_n_unita": wl,
                         "bootstrap_grappoli": bq, "unita_con_fuori_avviso": fu, "wilson_unita_fuori": wilson(fu, G),
                         "min_cop_unita": float(pm.min())}
        info["per_D"][D] = riga
    trj[cl] = info
    print("\n==", cl, {k: v for k, v in info.items() if k != "per_D"})
    for D, r in info["per_D"].items():
        a, b = r["u1"], r["u2"]
        f = lambda t: "[%.3f; %.3f]" % t if t else "n/d"
        print(" D=%2d casi %4d k/n %.3f W%s | u1 G=%3d W%s B%s fuori %d/%d | u2 G=%3d W%s B%s fuori %d/%d" % (
            D, r["casi"], r["dentro"] / r["casi"], f(r["wilson_casi"]), a["unita"], f(a["wilson_n_unita"]), f(a["bootstrap_grappoli"]),
            a["unita_con_fuori_avviso"], a["unita"], b["unita"], f(b["wilson_n_unita"]), f(b["bootstrap_grappoli"]), b["unita_con_fuori_avviso"], b["unita"]))

# sottotipi dei droni per volo
for tm in ["multirotore", "ala_fissa_senza_pilota"]:
    cc = [c for c in R["classi"]["droni"]["casi"] if c["tipo_mezzo"] == tm and c["D"] == 10]
    g = collections.defaultdict(list)
    for c in cc: g[mezzo(c["scena"])[0]].append(c["dentro"])
    pm = np.array([np.mean(v) for v in g.values()])
    print("droni", tm, "D=10 casi", len(cc), "voli", len(g), "media per volo %.3f" % pm.mean(), "Wilson n=voli", wilson(pm.mean() * len(g), len(g)))
    trj["droni"]["sottotipo_" + tm] = {"casi": len(cc), "voli": len(g), "media_per_volo": float(pm.mean()), "wilson_n_voli": wilson(pm.mean() * len(g), len(g))}
OUT["traiettorie"] = trj
json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "controllo.json"), "w"), indent=1, default=float, ensure_ascii=False)
