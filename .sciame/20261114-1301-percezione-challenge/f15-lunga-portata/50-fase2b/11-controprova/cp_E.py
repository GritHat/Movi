"""cp_E.py - controprova (sciame-avversario): E1, E2 (alta), E4 (alta, min), E5 (5 m) con lo strato eventi_v2 e il
nucleo v2 caricati DAL PROTOTIPO (movi.lungo, nucleo v2), indici di passaggio MIEI 7000.. (EVENTI_V2 e riprova usano 0..59).
Aggregazione mia: entro 2 s solo con 0 <= ritardo <= 2; raggio dell'impronta; tracce avvisate; falsi eventi.
Uso: python -I -B cp_E.py N12 N45 PROCESSI -> cp_E_passaggi.jsonl, cp_E_esito.json. Solo simulazione."""
import json, os, sys, math
from multiprocessing import Pool
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__)); PROTO = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo"
_E = {}
def E():
    if not _E:
        sys.path.insert(0, PROTO)
        from movi import lungo
        lungo.scegli_nucleo("v2"); _E["E"] = lungo.moduli()["eventi_v2"]
    return _E["E"]
def lav(a): return a, E()._lavoro(a)[1]
def wilson(k, n, z=1.96):
    if not n: return [0, 1]
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [round(max(0, c-h), 3), round(min(1, c+h), 3)]
if __name__ == "__main__":
    N12, N45, NP = int(sys.argv[1]), int(sys.argv[2]), min(int(sys.argv[3]), 7)
    L = [(e, "alta", 7000+i) for e in ("E2", "E1") for i in range(N12)] + [("E4", c, 7000+i) for c in ("alta", "min") for i in range(N45)] + [("E5", "alta", 7000+i, 5.0) for i in range(N45)]
    with Pool(NP) as p: rr = p.map(lav, L, chunksize=1)
    with open(os.path.join(QUI, "cp_E_passaggi.jsonl"), "w") as f:
        for a, r in rr: f.write(json.dumps({"lavoro": list(a), **r}, default=float)+"\n")
    out = {}
    for key in ("E1/alta", "E2/alta", "E4/alta", "E4/min", "E5/alta"):
        g = [r for a, r in rr if "%s/%s" % (a[0], a[1]) == key]; ok = [r for r in g if "errore" not in r]; n = len(ok)
        K = lambda f: (lambda k: [k, n, wilson(k, n)])(sum(1 for r in ok if f(r)))
        A = {"errori": len(g)-n, "esempio_errore": next((r["traccia"][-400:] for r in g if "errore" in r), None),
             "entro_2s_ritardo_0_2": K(lambda r: r["ritardo_evento_s"] is not None and 0 <= r["ritardo_evento_s"] <= 2.0),
             "evento_prima_del_vero": K(lambda r: r["ritardo_evento_s"] is not None and r["ritardo_evento_s"] < 0),
             "falso_evento": K(lambda r: r["falso_evento"]),
             "con_evento": K(lambda r: r["evento"] is not None),
             "R_imp_m": sorted(r["evento"]["R_imp_m"] for r in ok if r["evento"]),
             "R_imp_ge_1500": K(lambda r: r["evento"] is not None and r["evento"]["R_imp_m"] >= 1500),
             "tracce_avvisate": sorted(r.get("tracce_avvisate", 0) for r in ok if r["evento"]),
             "libero_su_frammento": K(lambda r: r["libero_su_frammento_in_impronta"][0] > 0)}
        for k in ("avviso_mezzo1", "avviso_persona1"):
            xs = [r[k] for r in ok if r.get(k)]
            if xs:
                A[k+"_avvisato"] = [sum(x["t"] is not None for x in xs), len(xs)]
                A[k+"_dist_min_vera_dall_impronta_m"] = sorted(x["dist_min_dopo_m"] for x in xs)[:5]
        out[key] = A
    json.dump(out, open(os.path.join(QUI, "cp_E_esito.json"), "w"), indent=1, default=float)
    print(json.dumps(out, default=float)[:5000])
