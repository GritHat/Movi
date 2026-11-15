"""riassunto.py — tabelle da risultati_traiettorie.json e confronto coi profili di classe. Solo conti."""
import csv, glob, json, math, os, sys
import numpy as np

F15, QUI = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(F15, "04-moto"))
import movi_lp as M  # noqa: E402

R = json.load(open(os.path.join(QUI, "risultati_traiettorie.json")))
REG = M.carica_regole(os.path.join(F15, "04-moto", "regole_lunga_portata.json"))
F14 = {c["id"]: c for c in json.load(open(os.path.join(F15, "..", "f14-classificazione", "01-profili", "classi.json")))["classi"]}
W = M.wilson
TIPI = ["rettilineo", "virata", "accelerazione", "arresto"]
out = {"per_durata": {}, "per_tratto": {}, "frase": {}, "per_mezzo_10s": {}, "alfa": {}, "rapporto_5s": {}, "profili": {}}


def fw(k, n):
    a, b = W(k, n)
    return "%d/%d=%.3f [%.3f; %.3f]" % (k, n, k / n if n else float("nan"), a, b)


print("== copertura della zona 0,90 sulla metà di PROVA (Wilson 95 %; 'cons' = Wilson con n = tratti, k in proporzione)")
for cl, d in R["classi"].items():
    cs = d["casi"]
    print("\n#", cl, "tratti prova", d["tratti_prova"], "fattore q", d["fattore_q"], "NIS medio %.2f (n %d), quota > 7,81: %.3f" % (d["nis_media"], d["nis_n"], d["nis_quota_oltre_7_81"]))
    print("D | n casi | tratti | tau med | err med | err p90 | dentro | cons | raggio med | area med km2 | fuori avviso | ampio")
    out["per_durata"][cl] = {}
    for D in R["durate"]:
        c = [x for x in cs if x["D"] == D and x["raggio"] is not None]
        if not c:
            continue
        n, k = len(c), sum(x["dentro"] for x in c)
        nt = len({x["scena"] for x in c})
        kc = round(k / n * nt)
        e = np.array([x["err"] for x in c])
        rg = np.array([x["raggio"] for x in c])
        fa = sum(x["fuori_avv"] for x in c)
        am = sum(x["ampio"] for x in c)
        row = dict(n=n, tratti=nt, tau_med=float(np.median([x["tau"] for x in c])), err_med=float(np.median(e)), err_p90=float(np.percentile(e, 90)),
                   k=k, wilson=W(k, n), wilson_cons=W(kc, nt), raggio_med=float(np.median(rg)), area_med_km2=float(np.median(math.pi * rg ** 2) / 1e6),
                   fuori_avviso=fa, wilson_fuori=W(fa, n), ampio=am)
        out["per_durata"][cl][D] = row
        print("%2d | %5d | %3d | %5.1f | %8.1f | %8.1f | %s | [%.3f; %.3f] | %7.1f | %.4f | %s | %d" % (
            D, n, nt, row["tau_med"], row["err_med"], row["err_p90"], fw(k, n), *row["wilson_cons"], row["raggio_med"], row["area_med_km2"], fw(fa, n), am))
    # frase: per ogni t, k su 10 = floor(10 * min limite inferiore cons. fino a t)
    fr, lo = {}, 1.0
    for D in R["durate"]:
        if D in out["per_durata"][cl]:
            lo = min(lo, out["per_durata"][cl][D]["wilson_cons"][0])
            fr[D] = math.floor(10 * lo + 1e-9)
    out["frase"][cl] = fr
    print("frase: k su 10 fino a t:", fr)
    print("per tipo di tratto (tutte le durate; e solo D <= 10 s):")
    out["per_tratto"][cl] = {}
    for tp in TIPI:
        c = [x for x in cs if x["tipo"] == tp and x["raggio"] is not None]
        c10 = [x for x in c if x["D"] <= 10]
        if c:
            out["per_tratto"][cl][tp] = dict(n=len(c), k=sum(x["dentro"] for x in c), n10=len(c10), k10=sum(x["dentro"] for x in c10),
                                             err_med10=float(np.median([x["err"] for x in c10])) if c10 else None)
            print("  %-13s tutte %s   D<=10 %s  err med D<=10 %s" % (tp, fw(out["per_tratto"][cl][tp]["k"], len(c)),
                  fw(out["per_tratto"][cl][tp]["k10"], len(c10)) if c10 else "-", "%.1f" % out["per_tratto"][cl][tp]["err_med10"] if c10 else "-"))
    print("per mezzo a D = 10 s; e rapporto err/(v0 tau) mediano a 5 s:")
    for tm in sorted({x["tipo_mezzo"] for x in cs}):
        c = [x for x in cs if x["tipo_mezzo"] == tm and x["D"] == 10 and x["raggio"] is not None]
        c5 = [x for x in cs if x["tipo_mezzo"] == tm and x["D"] == 5 and x["v0"] > 1.0]
        rap = float(np.median([x["err"] / (x["v0"] * x["tau"]) for x in c5])) if c5 else None
        out["rapporto_5s"][tm] = rap
        if c:
            k = sum(x["dentro"] for x in c)
            out["per_mezzo_10s"][tm] = dict(n=len(c), k=k, tratti=len({x["scena"] for x in c}), err_med=float(np.median([x["err"] for x in c])))
            print("  %-36s %s tratti %d err med %.1f m; rapporto 5 s %s" % (tm, fw(k, len(c)), out["per_mezzo_10s"][tm]["tratti"],
                  out["per_mezzo_10s"][tm]["err_med"], "%.3f" % rap if rap is not None else "-"))
    if cl == "droni":
        for nome, f in [("con guasto (ALFA failure)", lambda s: "failure" in s), ("ALFA senza guasto", lambda s: s.startswith("alfa") and "failure" not in s)]:
            for D in (5, 10):
                c = [x for x in cs if f(x["scena"]) and x["D"] == D]
                if c:
                    k = sum(x["dentro"] for x in c)
                    out["alfa"]["%s D%d" % (nome, D)] = dict(n=len(c), k=k, tratti=len({x["scena"] for x in c}))
                    print("  %s D=%d: %s (tratti %d)" % (nome, D, fw(k, len(c)), len({x["scena"] for x in c})))

print("\n== profili: quota di tratti (TUTTI) con velocita' massima oltre v_max; p99 di |dv/dt| (dal modulo della velocita' dei dati)")
MAPPA = R["mappa"]
F14MAP = {"aereo_rullaggio": "aereo_rullaggio", "multirotore": "multirotore_lento", "auto": "auto_strada_urbana", "treno": "treno_banchina"}
per = {}
for d in sorted(glob.glob(os.path.join(F15, "01-dati", "traiettorie", "*", "*"))):
    tp = json.load(open(os.path.join(d, "scena.json")))["oggetti"][0]["tipo"]
    rows = list(csv.DictReader(open(os.path.join(d, "verita.csv"))))
    t = np.array([float(r["tempo"]) for r in rows])
    v = np.array([math.sqrt(float(r["vx"]) ** 2 + float(r["vy"]) ** 2 + float(r["vz"]) ** 2) for r in rows])
    ok = np.diff(t) > 0.05
    a = np.abs(np.diff(v)[ok] / np.diff(t)[ok]) if ok.any() else np.array([0.0])
    per.setdefault(tp, []).append((v.max(), np.percentile(a, 99)))
for tp, L in sorted(per.items()):
    vm = np.array([x[0] for x in L])
    am = np.array([x[1] for x in L])
    c = REG["classi"][MAPPA[tp]]
    s = "%-36s tratti %3d | v max mediana %.1f, massima %.1f | oltre v_max %s (%.1f): %s | a p99 mediana %.2f, max %.2f, oltre a_max %.1f: %d" % (
        tp, len(L), np.median(vm), vm.max(), MAPPA[tp], c["v_max"], fw(int((vm > c["v_max"]).sum()), len(L)), np.median(am), am.max(), c["a_max"], int((am > c["a_max"]).sum()))
    if tp in F14MAP:
        f = F14[F14MAP[tp]]
        s += " | f14 %s v_max %.1f: %s" % (F14MAP[tp], f["v_max"], fw(int((vm > f["v_max"]).sum()), len(L)))
    out["profili"][tp] = dict(n=len(L), v_max_mediana=float(np.median(vm)), v_max_max=float(vm.max()), classe=MAPPA[tp], v_max_classe=c["v_max"],
                              oltre=int((vm > c["v_max"]).sum()), a_p99_mediana=float(np.median(am)), a_p99_max=float(am.max()), a_max_classe=c["a_max"],
                              oltre_a=int((am > c["a_max"]).sum()))
    print(s)
json.dump(out, open(os.path.join(QUI, "riassunto.json"), "w"), indent=1)
