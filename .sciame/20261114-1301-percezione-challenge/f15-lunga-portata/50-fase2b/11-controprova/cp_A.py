"""cp_A.py - controprova (sciame-avversario): A1 alta/min e A4 alta col nucleo v2 del prototipo, chiamata prudente,
semi MIEI (indici di passaggio 5000..5000+N-1, mai usati da riprova.py che usa 0..199). Aggregazione e Wilson miei.
Uso: python -I -B cp_A.py N PROCESSI -> cp_A_passaggi.jsonl, cp_A_esito.json. Solo simulazione."""
import json, os, sys, types, math
from concurrent.futures import ProcessPoolExecutor
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
PROTO = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo"
V2 = os.path.join(PROTO, "riuso", "lunga_portata_v2"); SIM = os.path.join(PROTO, "riuso", "lunga_portata", "10-simulatore")
FAM = {"A1": "sito_droni_rullaggio", "A4": "sito_droni_rullaggio"}
_P = {}
def carica():
    if not _P:
        sys.path[:0] = [V2, SIM]
        import movi_lp_v2 as m2
        m2.MAPPA_CERTIFICATA_PREDEFINITA = True
        sys.modules["movi_lp_import"] = types.SimpleNamespace(nucleo=m2)
        import prove_lp as P
        P.REG = m2.carica_regole(os.path.join(V2, "regole_lunga_portata_v2.json")); P.FAMIGLIA.update(FAM)
        _P["P"] = P
    return _P["P"]
def uno(a):
    s, c, i = a
    try:
        R = carica().passaggio(s, c, i, chiamante="prudente")
    except Exception as e:
        return {"scen": s, "cfg": c, "idx": i, "errore": repr(e)}
    return {"scen": s, "cfg": c, "idx": i, **{k: R[k] for k in ("tempestivo", "d_conf_m", "nasc_tot", "nasc_senza_regione",
            "nasc_fuori_avviso", "libero_viol", "libero_tot", "falsi_confermati", "c0", "comportamento", "coop")}}
def wilson(k, n, z=1.96):
    if not n: return [0, 1]
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [round(max(0, c-h), 3), round(min(1, c+h), 3)]
if __name__ == "__main__":
    N, NP = int(sys.argv[1]), min(int(sys.argv[2]), 7)
    lav = [(s, c, 5000+i) for s, c in (("A1", "alta"), ("A1", "min"), ("A4", "alta")) for i in range(N)]
    with ProcessPoolExecutor(NP) as ex:
        rs = list(ex.map(uno, lav, chunksize=2))
    with open(os.path.join(QUI, "cp_A_passaggi.jsonl"), "w") as f:
        for r in rs: f.write(json.dumps(r, default=str)+"\n")
    out = {}
    for s, c in (("A1", "alta"), ("A1", "min"), ("A4", "alta")):
        g = [r for r in rs if r["scen"] == s and r["cfg"] == c and "errore" not in r]
        nc0 = [r for r in g if not r["c0"]]
        def K(L, f): k = sum(1 for r in L if f(r)); return [k, len(L), wilson(k, len(L))]
        lib = lambda r: sum(r["libero_viol"].values()) > 0
        out[s+"_"+c] = {"errori": sum(1 for r in rs if r["scen"] == s and r["cfg"] == c and "errore" in r),
            "tempestivi": K(g, lambda r: r["tempestivo"]), "fuori_avviso": K(g, lambda r: r["nasc_fuori_avviso"] > 0),
            "senza_regione": K(g, lambda r: r["nasc_senza_regione"] > 0), "libero_oggetto_nonC0": K(nc0, lib),
            "libero_oggetto_C0": K([r for r in g if r["c0"]], lib),
            "fuori_avviso_per_comportamento": {b: K([r for r in g if r["comportamento"] == b], lambda r: r["nasc_fuori_avviso"] > 0) for b in sorted({r["comportamento"] for r in g})}}
    json.dump(out, open(os.path.join(QUI, "cp_A_esito.json"), "w"), indent=1)
    print(json.dumps(out))
