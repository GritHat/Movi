"""conta_v4c.py - conteggi per passaggio della valutazione v4c, con Wilson al 95 %. Uso: conta_v4c.py valutazione.jsonl uscita.json"""
import collections
import json
import math
import sys


def w(k, n, z=1.96):
    if n == 0:
        return [k, n, None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [k, n, round(max(0.0, c - h), 3), round(min(1.0, c + h), 3)]


rr = collections.defaultdict(list)
err = []
for l in open(sys.argv[1], encoding="utf-8"):
    r = json.loads(l)
    if "errore" in r:
        err.append(r["lavoro"])
        continue
    rr[(r["lavoro"][0], r["lavoro"][1])].append(r)
out = {"errori": err}
for (e, c), v in sorted(rr.items()):
    n = len(v)
    dl = [r["ritardo_evento_s"] for r in v]
    o = {"n": n, "idx": [min(r["idx"] for r in v), max(r["idx"] for r in v)],
         "falsi_eventi": w(sum(r["falso_evento"] for r in v), n),
         "libero_sul_vero_passaggi": w(sum(r["libero_sul_vero"][0] > 0 for r in v), n),
         "inneschi": dict(collections.Counter((r.get("innesco_v4c") or {}).get("perche") for r in v)),
         "tipi_evento": dict(collections.Counter((r["evento"] or {}).get("tipo", "nessuno")[:40] for r in v))}
    if e in ("F3", "F4"):
        for t in (1.0, 2.0, 2.5, 3.0):
            o["entro_%.1f_s" % t] = w(sum(x is not None and 0 <= x <= t + 1e-9 for x in dl), n)
        o["prima_dell_urto"] = w(sum(x is not None and x < 0 for x in dl), n)
        o["mai"] = w(sum(x is None for x in dl), n)
        ok = sorted(x for x in dl if x is not None)
        o["ritardo_min_med_max"] = [ok[0], ok[len(ok) // 2], ok[-1]] if ok else None
    if e == "F4":
        o["margine_operatore_min"] = min((r.get("margine_operatore_s") for r in v if r.get("margine_operatore_s") is not None), default=None)
    out["%s/%s" % (e, c)] = o
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, o in out.items():
    print(k, o)
