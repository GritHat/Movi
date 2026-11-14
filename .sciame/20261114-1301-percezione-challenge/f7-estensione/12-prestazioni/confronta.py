# confronta.py — stessa configurazione su core e lanci diversi. Uso: python3 -I confronta.py
def leggi(p):
    R = {}
    for r in open(p):
        if not r.startswith("rep="): continue
        d = {}
        for kv in r.split():
            k, v = kv.split("=", 1)
            try: d[k] = float(v)
            except ValueError: d[k] = v
        n = d["rep"] + (f"{int(d['fasce'])}" if "fasce" in d else "") + (f"_{int(d['portata'])}m" if "portata" in d else "")
        R[(n, d["scena"], int(d["res_cm"]), int(d["passo"]))] = d
    return R
A = leggi("tutti.txt"); B = leggi("risultati_ripetizione_core0.txt"); C = leggi("risultati_core_lento.txt")
print("config | core2 (giro principale) media/p95/max | core0 (ripetizione) media/p95/max | core9 lento media/p95/max | rapporto medie core0/core2 | lento/core2 | ns/passo lento")
rap = []; rapl = []
for k in sorted(B, key=lambda k: (k[2], k[3], k[0])):
    a, b, c = A.get(k), B[k], C.get(k)
    if not a or not c: continue
    f = lambda d: f"{d['agg_media_ms']:8.3f}/{d['agg_p95_ms']:8.3f}/{d['agg_max_ms']:8.3f}"
    r1 = b['agg_media_ms'] / a['agg_media_ms']; r2 = c['agg_media_ms'] / a['agg_media_ms']; rap.append(r1); rapl.append(r2)
    print(f"{k[0]:15s} {k[2]:2d}cm p{k[3]} | {f(a)} | {f(b)} | {f(c)} | {r1:.2f} | {r2:.2f} | {c.get('ns_passo', 0):.2f}")
rap.sort(); rapl.sort()
print(f"rapporto core0/core2: min {rap[0]:.2f} mediana {rap[len(rap)//2]:.2f} max {rap[-1]:.2f} su {len(rap)} configurazioni")
print(f"rapporto lento/core2: min {rapl[0]:.2f} mediana {rapl[len(rapl)//2]:.2f} max {rapl[-1]:.2f}")
