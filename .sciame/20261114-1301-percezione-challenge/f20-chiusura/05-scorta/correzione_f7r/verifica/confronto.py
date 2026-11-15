import json, math, sys
sys.path.insert(0, "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f20-chiusura/05-scorta/correzione_f7r/verifica")
from riconta import wil
from scipy.stats import fisher_exact, binomtest
D = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f20-chiusura/05-scorta/"
O = {}
for l in open(sys.argv[1]):
    r = json.loads(l); O[(r["var"], r["idx"])] = r
C = {}; F = {}
for l in open(D + "correzione_f7r/passaggi_f7r_c1_valutazione.jsonl"):
    r = json.loads(l)
    if r["cfg"] == "att": C[(r["var"], r["idx"])] = r
for l in open(D + "passaggi_f7r_valutazione.jsonl"):
    r = json.loads(l)
    if r["cfg"] == "att": F[(r["var"], r["idx"])] = r
ok_r = lambda r: r.get("rit_riacq_rad") is not None and r["rit_riacq_rad"] <= 2.0
ok_a = lambda r: r["avviso_t"] is not None and r["avviso_t"] <= r["interseca_t"]
# controllo che la verita' generata sia la stessa (stesso seme -> stessa interseca_t e d_rad)
for v in ("davanti", "vira", "totale"):
    same = sum(1 for i in range(60) if O[(v, i)]["interseca_t"] == C[(v, i)]["interseca_t"] and O[(v, i)]["d_rad"] == C[(v, i)]["d_rad"])
    a = sum(ok_r(O[(v, i)]) for i in range(60)); b = sum(ok_r(C[(v, i)]) for i in range(60))
    b10 = sum(1 for i in range(60) if ok_r(C[(v, i)]) and not ok_r(O[(v, i)])); b01 = sum(1 for i in range(60) if ok_r(O[(v, i)]) and not ok_r(C[(v, i)]))
    mc = binomtest(b10, b10 + b01, 0.5).pvalue if b10 + b01 else 1.0
    fi = fisher_exact([[b, 60 - b], [a, 60 - a]])[1]
    # contro il "prima" non appaiato (seme 20261122)
    a2 = sum(ok_r(F[(v, i)]) for i in range(60)); fi2 = fisher_exact([[b, 60 - b], [a2, 60 - a2]])[1]
    print(v, "verita' uguale %d/60" % same, "| riacq<=2s orig@24 %d/60 %s  c1@24 %d/60 %s  migliora %d peggiora %d  McNemar esatto p=%.4f Fisher p=%.4f | orig@22 %d/60 Fisher(c1@24 vs orig@22) p=%.4f" % (a, wil(a, 60), b, wil(b, 60), b10, b01, mc, fi, a2, fi2))
    I = [i for i in range(60) if C[(v, i)]["interseca_t"] is not None]
    a = sum(ok_a(O[(v, i)]) for i in I); b = sum(ok_a(C[(v, i)]) for i in I); n = len(I)
    b10 = sum(1 for i in I if ok_a(C[(v, i)]) and not ok_a(O[(v, i)])); b01 = sum(1 for i in I if ok_a(O[(v, i)]) and not ok_a(C[(v, i)]))
    mc = binomtest(b10, b10 + b01, 0.5).pvalue if b10 + b01 else 1.0
    print("   avviso prima fr: orig@24 %d/%d %s  c1@24 %d/%d %s  McNemar p=%.2e  Fisher p=%.2e" % (a, n, wil(a, n), b, n, wil(b, n), mc, fisher_exact([[b, n - b], [a, n - a]])[1]))
    sp_o = sum(1 for i in range(60) if O[(v, i)].get("riacq_spurie", 0) > 0 or O[(v, i)]["assoc_detriti_non_dich"] > 0)
    sp_c = sum(1 for i in range(60) if C[(v, i)].get("riacq_spurie", 0) > 0 or C[(v, i)]["assoc_detriti_non_dich"] > 0)
    print("   spurie (riacq_spurie o assoc nd): orig@24 %d/60 %s c1@24 %d/60 %s; id_ok orig@24 %d c1@24 %d; cont_ok orig@24 %d c1 %d" % (sp_o, wil(sp_o, 60), sp_c, wil(sp_c, 60), sum(O[(v, i)]["id_ok"] in (True, "True") for i in range(60)), sum(C[(v, i)]["id_ok"] for i in range(60)), sum(O[(v,i)]["cont_ok"] in (True,"True") for i in range(60)), sum(C[(v,i)]["cont_ok"] for i in range(60))))
# Fisher per totale avviso contro seme 22 e test unione
for v in ("totale",):
    I = [i for i in range(60) if C[(v, i)]["interseca_t"] is not None]; I2 = [i for i in range(60) if F[(v, i)]["interseca_t"] is not None]
    b = sum(ok_a(C[(v, i)]) for i in I); a = sum(ok_a(F[(v, i)]) for i in I2)
    print("totale avviso c1@24 %d/%d vs orig@22 %d/%d Fisher p=%.2e" % (b, len(I), a, len(I2), fisher_exact([[b, len(I) - b], [a, len(I2) - a]])[1]))
