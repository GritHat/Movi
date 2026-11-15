"""pilota_A1.py - N passaggi A1 'alta' di prove_lp con nucleo v2 e regole v2, chiamata 'interfaccia'.
Uso: python -I -B pilota_A1.py N PROCESSI [v1|cert] -> pilota_A1_esito.json (con v1: nucleo e regole v1, pilota_A1_v1_esito.json). Conteggi per passaggio; Wilson 95 %."""
import json, os, sys, types
from concurrent.futures import ProcessPoolExecutor
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__)); F15 = os.path.dirname(os.path.dirname(QUI))
sys.path[:0] = [QUI, os.path.join(F15, "10-simulatore"), os.path.join(F15, "04-moto")]
V1 = len(sys.argv) > 3 and sys.argv[3] == "v1"
CERT = len(sys.argv) > 3 and sys.argv[3] == "cert"   # v2 con la mappa dichiarata completa

def uno(idx):
    if V1:
        import movi_lp as m2
    else:
        import movi_lp_v2 as m2
        m2.MAPPA_CERTIFICATA_PREDEFINITA = CERT
    sys.modules["movi_lp_import"] = types.SimpleNamespace(nucleo=m2)
    import prove_lp as P
    if not V1:
        P.REG = m2.carica_regole(os.path.join(QUI, "regole_lunga_portata_v2.json"))
    R = P.passaggio("A1", "alta", idx, chiamante="interfaccia")
    return {"idx": idx, "senza_regione": R["nasc_senza_regione"], "fuori_avviso": R["nasc_fuori_avviso"], "nasc_tot": R["nasc_tot"],
            "libero_viol": R["libero_viol"], "libero_tot": R["libero_tot"], "tempestivo": R["tempestivo"], "falsi_confermati": R["falsi_confermati"]}

if __name__ == "__main__":
    import movi_lp_v2 as m2
    N, nproc = int(sys.argv[1]), int(sys.argv[2])
    with ProcessPoolExecutor(nproc) as ex:
        rs = list(ex.map(uno, range(N)))
    k = lambda f: sum(1 for r in rs if f(r))
    out = {"N": N, "per_passaggio": rs}
    for nome, f in (("con_ciclo_senza_regione", lambda r: r["senza_regione"] > 0), ("con_ciclo_fuori_avviso", lambda r: r["fuori_avviso"] > 0),
                    ("con_libero_sull_oggetto", lambda r: sum(r["libero_viol"].values()) > 0), ("tempestivi", lambda r: r["tempestivo"])):
        out[nome] = [k(f), N, [round(x, 3) for x in m2.wilson(k(f), N)]]
    out["istanti_libero_sull_oggetto"] = [sum(sum(r["libero_viol"].values()) for r in rs), sum(sum(r["libero_tot"].values()) for r in rs)]
    out["falsi_confermati_mediana"] = sorted(r["falsi_confermati"] for r in rs)[N // 2]
    out["nascosti"] = [sum(r["nasc_tot"] > 0 for r in rs), sum(r["nasc_tot"] for r in rs)]
    json.dump(out, open(os.path.join(QUI, "pilota_A1_v1_esito.json" if V1 else ("pilota_A1_cert_esito.json" if CERT else "pilota_A1_esito.json")), "w"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k != "per_passaggio"}, ensure_ascii=False))
