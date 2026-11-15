"""cp_video_dettaglio.py - (1) lp_A1: per i fotogrammi con avviso, distanza fra il drone vero nascosto e la cella
'libero' piu' vicina DENTRO l'avviso, e stato della cella del drone. (2) lp_E1, lp_E2: avvisi accesi e detriti al
primo e all'ultimo fotogramma dopo l'evento; raggio dell'impronta; ultimo fotogramma con detriti. Legge solo i registri."""
import json, math
B = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/uscite/video/"
L = [json.loads(x) for x in open(B + "lp_A1/registro.jsonl")]
g = list(L[0]["griglie"].values())[0] if isinstance(L[0]["griglie"], dict) else None
import ast
g = g or list(ast.literal_eval(L[0]["griglie"]).values())[0]
(x0, x1), (y0, y1), (nx, ny) = g["x"], g["y"], g["n"]; dx, dy = (x1-x0)/(nx-1), (y1-y0)/(ny-1)
for r in L:
    if r.get("tipo") != "fotogramma" or not r["avvisi"]: continue
    cel = [s for s, k in r["celle"]["rle"] for _ in range(k)]
    dr = [o for o in r["verita"]["oggetti"] if o["id"].startswith("drone")][0]["pos"]
    i, j = round((dr[0]-x0)/dx), round((dr[1]-y0)/dy)
    best = None
    for a in r["avvisi"]:
        c, R = a["forma"]["centro"], a["raggio_m"]
        for idx, s in enumerate(cel):
            if s != "libero": continue
            jj, ii = divmod(idx, nx); p = (x0+ii*dx, y0+jj*dy)
            if math.dist(p, c) <= R:
                d = math.dist(p, dr[:2]); best = d if best is None else min(best, d)
    print("lp_A1 t=%.1f drone=(%.0f,%.0f,%.0f) cella_drone=%s libero_piu_vicino_nell_avviso=%.0f m lato_cella=%.0f m libero_per=%s" % (r["t"], *dr, cel[j*nx+i], best, dx, r["libero_per_classi"]))
for sc in ("lp_E1", "lp_E2"):
    L = [json.loads(x) for x in open(B + sc + "/registro.jsonl")]; F = [r for r in L if r.get("tipo") == "fotogramma"]
    con = [r for r in F if r.get("detriti")]
    if not con: print(sc, "nessun detrito"); continue
    a, z = con[0], con[-1]
    print(sc, "detriti da t=%.1f a t=%.1f (ultimo fotogramma t=%.1f); impronta_raggio=%s m; volume_raggio=%s m; avvisi accesi: primo %d, ultimo %d; tracce_avvisate=%s; tracce nell'ultimo=%d" % (
        a["t"], z["t"], F[-1]["t"], z["detriti"].get("impronta_raggio_m"), z["detriti"].get("raggio_volume_m"), len(a["avvisi"]), len(z["avvisi"]), z["detriti"].get("tracce_avvisate") if not isinstance(z["detriti"].get("tracce_avvisate"), list) else len(z["detriti"]["tracce_avvisate"]), len(z["tracce"])))
    print("   piano della vista:", ast.literal_eval(L[0]["griglie"]) if isinstance(L[0]["griglie"], str) else L[0]["griglie"])
