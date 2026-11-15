"""riprova_v3.py - fase 2c (copia di 10-riprova/riprova.py, nucleo v3 di 60-fase2c/01-correzioni). VARIANTE=letterale
(solo K-613, ritenuta spenta) o completo (predefinito). Mappa: MAPPA_CERT=1 (predefinito qui, ipotesi del simulatore).
Da riprova.py - fase 2b: A1 (min, alta), A2 (alta), A3 (min) con il nucleo v2 del prototipo, chiamata PRUDENTE.

Uso: <venv>/bin/python -I -B riprova.py N PROCESSI [scen:cfg ...]  -> riprova_esito.json, riprova_passaggi.jsonl
Nucleo e regole: prototipo/riuso/lunga_portata_v2 (copie con impronta di 01-nucleo); simulatore e prove_lp:
prototipo/riuso/lunga_portata/10-simulatore (copia di f15). Mappa dichiarata completa (MAPPA_CERTIFICATA_PREDEFINITA
= True: il simulatore conosce tutti gli ostacoli; ipotesi dichiarata). A1, A2 -> famiglia sito_droni_rullaggio;
A3 -> aeroporto_e_droni. Un record per passaggio; Wilson 95 % per passaggio. Solo simulazione."""
import json
import os
import sys
import time
import types
from concurrent.futures import ProcessPoolExecutor

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.abspath(os.path.join(QUI, "..", "..", "..", "..", "..", "prototipo"))
V2 = os.path.join(PROTO, "riuso", "lunga_portata_v2")
SIM = os.path.join(PROTO, "riuso", "lunga_portata", "10-simulatore")
FAM = {"A1": "sito_droni_rullaggio", "A2": "sito_droni_rullaggio", "A3": "aeroporto_e_droni"}
if os.environ.get("RIPROVA_FAM_A1"):          # diagnosi (notata dopo): famiglia di A1 scavalcata
    FAM["A1"] = os.environ["RIPROVA_FAM_A1"]
SUFF = os.environ.get("RIPROVA_SUFFISSO", "")
_P = {}


def _carica():
    if not _P:
        sys.path[:0] = [V2, SIM]
        sys.path.insert(0, QUI)
        import movi_lp_v3 as m2
        m2.MAPPA_CERTIFICATA_PREDEFINITA = os.environ.get("MAPPA_CERT", "1") == "1"
        if os.environ.get("VARIANTE", "completo") == "letterale":
            m2.T_RITENUTA_S = None
        sys.modules["movi_lp_import"] = types.SimpleNamespace(nucleo=m2)
        import prove_lp as P
        P.REG = m2.carica_regole(os.path.join(V2, "regole_lunga_portata_v2.json"))
        P.FAMIGLIA.update(FAM)
        _P.update(P=P, m=m2)
    return _P


def uno(a):
    scen, cfg, idx = a
    P = _carica()["P"]
    t0 = time.perf_counter()
    R = P.passaggio(scen, cfg, idx, chiamante="prudente")
    return {"scen": scen, "cfg": cfg, "idx": idx, "tempestivo": R["tempestivo"], "d_conf_m": R["d_conf_m"],
            "t_conf": R["t_conf"], "nasc_tot": R["nasc_tot"], "senza_regione": R["nasc_senza_regione"],
            "fuori_avviso": R["nasc_fuori_avviso"], "libero_viol": R["libero_viol"], "libero_tot": R["libero_tot"],
            "falsi_confermati": R["falsi_confermati"], "coop": R["coop"], "c0": R["c0"], "comportamento": R["comportamento"],
            "eventi_nucleo": R["eventi_nucleo"], "s": round(time.perf_counter() - t0, 1)}


def wilson(k, n, z=1.96):
    if n == 0:
        return [0.0, 1.0]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return [round(max(0.0, c - h), 3), round(min(1.0, c + h), 3)]


if __name__ == "__main__":
    N, NP = int(sys.argv[1]), min(int(sys.argv[2]), 7)
    sel = [x.split(":") for x in sys.argv[3:]] or [("A1", "alta"), ("A1", "min"), ("A2", "alta"), ("A3", "min")]
    t0 = time.time()
    out = {"N": N, "processi": NP, "nucleo": "60-fase2c/01-correzioni/movi_lp_v3.py", "variante": os.environ.get("VARIANTE", "completo"), "mappa_env": os.environ.get("MAPPA_CERT", "1"), "chiamante": "prudente",
           "famiglie": FAM, "inizio": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "aggregati": {}}
    with ProcessPoolExecutor(NP) as ex, open(os.path.join(QUI, "riprova_passaggi" + SUFF + ".jsonl"), "a", encoding="utf-8") as fj:
        for scen, cfg in sel:
            rs = list(ex.map(uno, [(scen, cfg, i) for i in range(N)]))
            for r in rs:
                fj.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
            fj.flush()
            k = lambda f: sum(1 for r in rs if f(r))
            A = {}
            for nome, f in (("tempestivi", lambda r: r["tempestivo"]),
                            ("con_ciclo_fuori_avviso", lambda r: r["fuori_avviso"] > 0),
                            ("con_ciclo_senza_regione", lambda r: r["senza_regione"] > 0),
                            ("con_libero_sull_oggetto", lambda r: sum(r["libero_viol"].values()) > 0),
                            ("con_fase_nascosta", lambda r: r["nasc_tot"] > 0),
                            ("confermati", lambda r: r["d_conf_m"] is not None)):
                A[nome] = [k(f), N, wilson(k(f), N)]
            A["istanti_libero_sull_oggetto"] = [sum(sum(r["libero_viol"].values()) for r in rs),
                                                sum(sum(r["libero_tot"].values()) for r in rs)]
            A["falsi_confermati_mediana"] = sorted(r["falsi_confermati"] for r in rs)[N // 2]
            dc = sorted(r["d_conf_m"] for r in rs if r["d_conf_m"] is not None)
            A["d_conf_mediana_m"] = dc[len(dc) // 2] if dc else None
            A["d_conf_p5_m"] = dc[int(0.05 * len(dc))] if dc else None
            out["aggregati"][scen + "_" + cfg] = A
            print(scen, cfg, json.dumps(A, ensure_ascii=False), round(time.time() - t0), "s", flush=True)
    out["durata_s"] = round(time.time() - t0, 1)
    nome = ("riprova_esito" + SUFF + ".json") if len(sys.argv) <= 3 else "riprova_esito" + SUFF + "_" + "_".join(x[0] + x[1] for x in sel) + ".json"
    with open(os.path.join(QUI, nome), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
