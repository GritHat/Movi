"""Attacco 1: copertura per tipo di moto sui casi di prova ADS-B (aerei veloci, ala fissa). Solo lettura dei casi."""
import json, math, sys
def wilson(k, n, z=1.959964):
    if n == 0: return (0.0, 1.0)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))
F = [(1, 2), (3, 5), (6, 10), (11, 20), (21, 30)]
out = {}
for nome in sys.argv[1:]:
    d = json.load(open(nome))
    for filt in ("cv", "imm"):
        for tipo in ("rettilineo", "virata", "accelerazione", "tutti"):
            for a in (0.5, 0.9):
                for lo, hi in F:
                    cs = [c for c in d[filt] if lo - 0.5 <= c["tau"] < hi + 0.5 and (tipo == "tutti" or c["tipo"] == tipo)]
                    n = len(cs); k = sum(1 for c in cs if c[filt]["u"] <= a)
                    if n:
                        w = wilson(k, n)
                        out[f"{nome.split('/')[-1]}|{filt}|{tipo}|{a}|{lo}-{hi}"] = [k, n, round(k / n, 3), round(w[0], 3), round(w[1], 3)]
    # il caso singolo peggiore: IMM con u piu' alto (promessa C=0,9 molto lontana) in virata
    vir = sorted([c for c in d["imm"] if c["tipo"] != "rettilineo"], key=lambda c: -c["imm"]["u"])[:5]
    out[nome.split('/')[-1] + "|peggiori_imm_manovra"] = [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in c.items() if k != "cv"} | {"imm": {k: round(v, 4) for k, v in c["imm"].items()}} for c in vir]
json.dump(out, open("attacco_adsb.json", "w"), indent=0)
for k, v in out.items():
    if "peggiori" in k or "|0.9|" in k and ("virata" in k or "accel" in k or "tutti" in k) or ("|0.5|" in k and "tutti" in k): print(k, v)
