import json, math, collections, sys
def w(k, n, z=1.96):
    if n == 0: return "%d/0" % k
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return "%d/%d [%.3f; %.3f]" % (k, n, max(0, c-h), min(1, c+h))
R = [json.loads(l) for l in open(sys.argv[1])]
print("errori", sum("errore" in r for r in R))
g = collections.defaultdict(list)
for r in R:
    if "errore" not in r: g[(r["gruppo"], r["var"], r["cfg"])].append(r)
for k, rr in sorted(g.items()):
    n = len(rr); inters = [r for r in rr if r["interseca_t"] is not None]; noint = [r for r in rr if r["interseca_t"] is None]
    mg = [round(r["interseca_t"]-r["avviso_t"], 2) for r in inters if r["avviso_t"] is not None]
    print("%s %s/%s n=%d | cont %s | id %s | libero_b %s | libero_fr %s | assoc_nd %s | evento %s | falsi %s | riacq2 %s | vol %d/%d tutti %s | inters %d avvisati %d margmin %s | avviso_senza %s" % (
        k[0], k[1], k[2], n, w(sum(r["cont_ok"] for r in rr), n), w(sum(r["id_ok"] for r in rr), n), w(sum(r["libero"] > 0 for r in rr), n),
        w(sum(r["libero_fr"] > 0 for r in rr), n), w(sum(r["assoc_detriti_non_dich"] > 0 for r in rr), n), w(sum(r["evento_t"] is not None for r in rr), n),
        w(sum(bool(r["falso_evento"]) for r in rr), n), w(sum(r["rit_riacq"] is not None and r["rit_riacq"] <= 2 for r in rr), n),
        sum(r["vol_dentro"] for r in rr), sum(r["vol_tot"] for r in rr), w(sum(r["vol_tot"] > 0 and r["vol_dentro"] == r["vol_tot"] for r in rr), n),
        len(inters), sum(r["avviso_t"] is not None and r["avviso_t"] <= r["interseca_t"] for r in inters), min(mg) if mg else None,
        w(sum(r["avviso_t"] is not None for r in noint), len(noint))))
