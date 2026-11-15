"""controllo.py - riconto indipendente (sciame-statistico) delle cifre di f19-volo da file grezzi.
Uso: python -I controllo.py <f19-volo> <uscita.json>. Sola lettura dei grezzi; scrive solo <uscita.json>."""
import json, math, os, sys, random, importlib.util
from collections import defaultdict

F19, OUT = sys.argv[1], sys.argv[2]
Z = 1.959964


def wil(k, n):
    if n == 0: return [None, None]
    p = k / n; d = 1 + Z * Z / n; c = p + Z * Z / (2 * n)
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))
    return [round((c - h) / d, 4), round((c + h) / d, 4)]


def kn(k, n): return {"k": k, "n": n, "p": round(k / n, 4) if n else None, "wilson": wil(k, n)}


def chi2_sf(x, df):
    # v2: la serie della v1 perdeva precisione per x grande (p sbagliati in controllo_esito.json): si usa scipy
    from scipy.stats import chi2
    return float(chi2.sf(x, df))


def chi2_sf_v1(x, df):
    # coda superiore del chi-quadro (serie della gamma incompleta regolarizzata)
    if x <= 0: return 1.0
    a, s, t = df / 2.0, 0.0, 1.0 / (df / 2.0)
    s = t; k = 1
    while k < 500:
        t *= (x / 2.0) / (a + k); s += t; k += 1
        if t < 1e-14 * s: break
    lp = a * math.log(x / 2.0) - x / 2.0 - math.lgamma(a + 1) + math.log(s * a)
    return max(0.0, 1.0 - math.exp(lp))


R = {}
P = os.path.join(F19, "10-prove")
EV = {"F3": 20.0, "F4": 30.0}
CPA = {"F1": 80.0, "F5": 40.24}
FASCE_C = [(0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, .9), (.9, .95), (.95, .99), (.99, 1.0001)]
for ver in ("v3b", "v3i", "v4"):
    rr = [json.loads(l) for l in open(os.path.join(P, "passaggi_volo_%s.jsonl" % ver))]
    cel = defaultdict(list)
    for r in rr: cel[(r["scenario"], r["cfg"])].append(r)
    out = {}
    for (s, c), L in sorted(cel.items()):
        n = len(L); A = {"n": n}
        A["passaggi_libero_sul_vero"] = kn(sum(r["libero_sul_vero"][0] > 0 for r in L), n)
        A["continuita"] = kn(sum(sum(r["buchi_continuita"].values()) == 0 for r in L), n)
        if s in EV:
            for t in (1, 2, 3):
                A["evento_entro_%ds" % t] = kn(sum(r["ritardo_evento_s"] is not None and r["ritardo_evento_s"] <= t for r in L), n)
            for chi in ("bordo", "operatore"):
                mm = sorted(r["margine_%s_s" % chi] for r in L if r.get("margine_%s_s" % chi) is not None)
                A["tempestivo_" + chi] = kn(sum(m >= 0 for m in mm), n)
                A["margine_%s_min_med" % chi] = [mm[0], mm[len(mm) // 2]] if mm else None
            A["libero_su_frammento"] = kn(sum(r["libero_su_frammento_in_impronta"][0] > 0 for r in L), n)
            fv = [r["frammenti_dentro_V"] for r in L if r["frammenti_dentro_V"][1] > 0]
            A["passaggi_tutti_frammenti_V"] = kn(sum(a == b for a, b in fv), len(fv))
            A["frammenti_V_campioni"] = kn(sum(a for a, _ in fv), sum(b for _, b in fv))
            # frazione per passaggio dei frammenti in V: minimo per passaggio (unita' = passaggio)
            fr = sorted(a / b for a, b in fv)
            A["frazione_V_per_passaggio_min_mediana"] = [round(fr[0], 4), round(fr[len(fr) // 2], 4)] if fr else None
        else:
            A["falsi_eventi"] = kn(sum(r["evento"] is not None for r in L), n)
        if s in CPA:
            ant = [CPA[s] - r["avviso_prossimita"][0] if r["avviso_prossimita"] else None for r in L]
            A["avviso_ge_20s"] = kn(sum(a is not None and a >= 20 for a in ant), n)
        if s == "F5":
            sw = nn = 0
            for r in L:
                a0, a1 = r["assoc_F5"].get("38.5", {}), r["assoc_F5"].get("46.0", {})
                com = [t for t in a0 if t in a1]
                if com: nn += 1; sw += any(a0[t] != a1[t] for t in com)
            A["scambio_identita"] = kn(sw, nn)
        if s in ("F4", "F5"):
            A["camere_persa_3cicli"] = kn(sum(len([v for v in r["salute_cicli"].values() if v <= 3]) >= 2 for r in L), n)
        # copertura (r99 o insieme) per passaggio: passaggi in cui TUTTI i campioni di perdita sono coperti
        cal = [[x for x in r["calib"]] for r in L]
        ok = [all(x[4] or x[5] for x in cl) for cl in cal if cl]
        A["copertura_tutti_i_cicli_per_passaggio"] = kn(sum(ok), len(ok))
        tot = [(x[4] or x[5]) for cl in cal for x in cl]
        A["copertura_campioni"] = kn(sum(tot), len(tot))
        # calibrazione: un campione per passaggio e per fascia (il primo), test di Hosmer-Lemeshow per fasce
        if ver == "v3b":
            for regime in ("nel_modello", "dopo_evento"):
                def sel(x):
                    d = s in EV and x[0] >= EV[s]
                    return d if regime == "dopo_evento" else not d
                bande, H, dfh = [], 0.0, 0
                for a, b in FASCE_C:
                    pp = []
                    for cl in cal:
                        cs = [x for x in cl if sel(x) and a <= x[2] < b]
                        if cs: pp.append(cs[0])
                    if not pp: continue
                    n_ = len(pp); o = sum(bool(x[3]) for x in pp); e = sum(x[2] for x in pp)
                    v = sum(x[2] * (1 - x[2]) for x in pp)
                    bd = {"fascia": [a, min(b, 1)], "n_passaggi": n_, "C_media": round(e / n_, 4), "oss": kn(o, n_)}
                    lo, hi = bd["oss"]["wilson"]
                    bd["C_media_dentro_wilson"] = lo <= e / n_ <= hi
                    if n_ >= 10 and v > 1e-6:
                        H += (o - e) ** 2 / v; dfh += 1
                    bande.append(bd)
                if bande:
                    A["calib_" + regime] = {"bande": bande, "HL_chi2": round(H, 2), "df": dfh,
                                            "p": round(chi2_sf(H, dfh), 5) if dfh else None}
        out["%s/%s" % (s, c)] = A
    R[ver] = out

# --- dati reali: copertura al 90 % per MEZZO (bootstrap a grappoli) ---
C3 = os.path.join(F19, "03-confidenza")
sys.argv = ["x", "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f15-lunga-portata", "/nonusata"]
spec = importlib.util.spec_from_file_location("pr", os.path.join(C3, "prove_reali.py"))
pr = importlib.util.module_from_spec(spec); sys.path.insert(0, C3); spec.loader.exec_module(pr)
sc = pr.scene(); met = pr.dividi(sc)
FAS = [(0, 2.5, "1-2"), (2.5, 5.5, "3-5"), (5.5, 10.5, "6-10"), (10.5, 20.5, "11-20"), (20.5, 40, "21-30")]
REAL = {}
for cl, fn in (("aerei_veloci", "casi_prova_aerei_veloci.json"), ("droni_ala_fissa", "casi_prova_droni_ala_fissa.json"),
               ("multirotori", "casi_prova_multirotori.json")):
    prv = [d for c, d in sc if c == cl and met[d] == "prova"]
    tar = [d for c, d in sc if c == cl and met[d] == "taratura"]
    mz_p = {pr.mezzo(os.path.basename(d)) for d in prv}; mz_t = {pr.mezzo(os.path.basename(d)) for d in tar}
    attivi = []
    for d in prv:
        t, _, _ = pr.leggi(d)
        sel, ult = [], -1e9
        for i in range(len(t)):
            if t[i] >= ult + 1.0 - 1e-6: sel.append(i); ult = t[i]
        if len(sel) >= 15: attivi.append(d)
    C = json.load(open(os.path.join(C3, fn)))
    blocchi = {}
    for nome in ("cv", "imm"):
        L = C[nome]; bl = [[]]
        for i, x in enumerate(L):
            if i and x["D"] < L[i - 1]["D"]: bl.append([])
            bl[-1].append(x)
        blocchi[nome] = bl
    info = {"sequenze_prova": len(prv), "sequenze_con_casi": len(attivi), "blocchi_trovati": len(blocchi["cv"]),
            "mezzi_prova": len(mz_p), "mezzi_taratura": len(mz_t), "intersezione_mezzi": len(mz_p & mz_t)}
    mappa_ok = len(blocchi["cv"]) == len(attivi)
    info["mappa_blocco_sequenza_ok"] = mappa_ok
    if mappa_ok:
        mz_of = [pr.mezzo(os.path.basename(d)) for d in attivi]
    else:
        mz_of = list(range(len(blocchi["cv"])))      # ripiego: grappolo = sequenza (meno prudente)
    info["casi_per_mezzo_max_quota"] = None
    rng = random.Random(20261115)
    for nome in ("cv", "imm"):
        g = defaultdict(list)
        for b, m in zip(blocchi[nome], mz_of): g[m].extend(b)
        mz = sorted(g, key=str)
        tot = sum(len(v) for v in g.values())
        info["casi_per_mezzo_max_quota"] = round(max(len(v) for v in g.values()) / tot, 3)
        res = {}
        for lo, hi, et in FAS:
            per = {m: [x[nome]["u"] <= 0.9 for x in g[m] if lo <= x["tau"] < hi] for m in mz}
            per = {m: v for m, v in per.items() if v}
            k = sum(sum(v) for v in per.values()); n = sum(len(v) for v in per.values())
            bs = []
            ms = list(per)
            for _ in range(2000):
                s_ = [per[rng.choice(ms)] for _ in ms]
                nn = sum(len(v) for v in s_); bs.append(sum(sum(v) for v in s_) / nn)
            bs.sort()
            # design effect: varianza a grappoli / binomiale
            p = k / n
            vc = sum((sum(v) - p * len(v)) ** 2 for v in per.values()) * len(per) / max(1, len(per) - 1) / n ** 2
            vb = p * (1 - p) / n
            res[et] = {"k": k, "n_casi": n, "n_mezzi": len(per), "p": round(p, 4), "wilson_casi": wil(k, n),
                       "bootstrap_mezzi_95": [round(bs[50], 4), round(bs[1949], 4)],
                       "deff": round(vc / vb, 2) if vb > 0 else None,
                       "n_efficace": round(n * vb / vc, 1) if vc > 0 else None,
                       "wilson_n_efficace": wil(round(p * n * vb / vc), round(n * vb / vc)) if vc > 0 else None}
        # adeguatezza del PIT: decili, Rao-Scott (chi2 / deff medio) su tutti i casi
        u = [x[nome]["u"] for m in mz for x in g[m]]
        cnt = [0] * 10
        for x in u: cnt[min(9, int(x * 10))] += 1
        e = len(u) / 10; X2 = sum((c - e) ** 2 / e for c in cnt)
        deffs = [v["deff"] for v in res.values() if v["deff"]]
        dm = sum(deffs) / len(deffs)
        res["PIT_decili"] = {"conteggi": cnt, "chi2": round(X2, 1), "df": 9, "p_ingenuo": chi2_sf(X2, 9),
                             "deff_medio": round(dm, 2), "chi2_RaoScott": round(X2 / dm, 1), "p_RaoScott": chi2_sf(X2 / dm, 9)}
        # virate (aerei)
        if cl == "aerei_veloci":
            for lo, hi, et in FAS[2:]:
                per = {m: [x[nome]["u"] <= 0.9 for x in g[m] if lo <= x["tau"] < hi and x["tipo"] != "rettilineo"] for m in mz}
                per = {m: v for m, v in per.items() if v}
                k = sum(sum(v) for v in per.values()); n = sum(len(v) for v in per.values())
                res["virata_" + et] = {"k": k, "n": n, "n_mezzi": len(per), "p": round(k / n, 4) if n else None, "wilson_casi": wil(k, n),
                                       "tipi": sorted({x["tipo"] for m in mz for x in g[m]})}
        info[nome] = res
    REAL[cl] = info
R["reali"] = REAL
json.dump(R, open(OUT, "w"), indent=1, ensure_ascii=False)
print("ok")
