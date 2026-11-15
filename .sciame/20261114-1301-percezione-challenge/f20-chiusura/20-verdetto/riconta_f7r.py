import json, math, collections, sys
def w(k, n, z=1.96):
    if n == 0: return "%d/0" % k
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return "%d/%d [%.3f; %.3f]" % (k, n, max(0, c-h), min(1, c+h))
g = collections.defaultdict(list)
for l in open(sys.argv[1]):
    r = json.loads(l); g[(r["var"], r["cfg"])].append(r)
for (v, c), rr in sorted(g.items()):
    n = len(rr); it = [r for r in rr if r["interseca_t"] is not None]
    print("%s/%s n=%d unici %d | cont %s | libero %s | libero_fr %s | assoc_nd %s | riacq_rad2 %s | id %s | evento %s | falsi %s | avviso_prima %s | vol %d/%d" % (v, c, n, len(set(r["idx"] for r in rr)),
      w(sum(r["cont_ok"] for r in rr), n), w(sum(r["libero"] > 0 for r in rr), n), w(sum(r["libero_fr"] > 0 for r in rr), n), w(sum(r["assoc_detriti_non_dich"] > 0 for r in rr), n),
      w(sum(r.get("rit_riacq_rad") is not None and r["rit_riacq_rad"] <= 2 for r in rr), n), w(sum(r["id_ok"] for r in rr), n), w(sum(r["evento_t"] is not None for r in rr), n),
      w(sum(bool(r["falso_evento"]) for r in rr), n), w(sum(r["avviso_t"] is not None and r["avviso_t"] <= r["interseca_t"] for r in it), len(it)), sum(r["vol_dentro"] for r in rr), sum(r["vol_tot"] for r in rr)))
