"""riconta.py - riconto indipendente (codice dell'avversario) di valutazione_v4c.jsonl e controllo dei semi."""
import json, math, sys, collections, glob, os
def w(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return "%d/%d [%.3f; %.3f]" % (k, n, max(0, c-h), min(1, c+h))
f = sys.argv[1]
R = [json.loads(l) for l in open(f, encoding="utf-8")]
celle = collections.defaultdict(list)
for r in R:
    celle[(r["lavoro"][0], r["lavoro"][1])].append(r)
out = {}
dur = collections.defaultdict(list)
for (e, c), v in sorted(celle.items()):
    idx = sorted(r["lavoro"][2] for r in v)
    o = {"n": len(v), "idx": [idx[0], idx[-1]], "idx_unici": len(set(idx))}
    o["falso_evento"] = w(sum(bool(r.get("falso_evento")) for r in v), len(v))
    o["evento_qualunque"] = w(sum(r.get("evento") is not None for r in v), len(v))
    o["libero_vero"] = w(sum(r["libero_sul_vero"][0] > 0 for r in v), len(v))
    dl = [r.get("ritardo_evento_s") for r in v]
    for t in (1, 2):
        o["entro_%d" % t] = w(sum(x is not None and 0 <= x <= t + 1e-9 for x in dl), len(v))
    o["prima"] = w(sum(x is not None and x < 0 for x in dl), len(v))
    # attacco: in F3 un evento prima dell'urto conta come falso allarme
    if e == "F3":
        o["F3_successo_stretto_entro2_senza_precoci"] = o["entro_2"]
    o["durata_med_s"] = sorted(r.get("durata_calcolo_s", 0) for r in v)[len(v)//2]
    out["%s/%s" % (e, c)] = o
print(json.dumps(out, indent=1, ensure_ascii=False))
