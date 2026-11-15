"""limite.py - X7: rifà due prove di 10-simulatore/prove_lp.py (non modificato) con parametri al limite, modo prudente.
Uso: MOVI_CHIAMANTE=prudente [MOVI_FALSI_4D=1.0] python -I -B limite.py <scenario> <N> <variante: nominale|limite>
Scrive solo in questa cartella (limite_<scenario>_<variante>.json). Simulazione: nessun sensore fisico.
"""
import json, os, sys, time, multiprocessing as mp
sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(QUI), "10-simulatore"))
import prove_lp as P

scen, N, var = sys.argv[1], int(sys.argv[2]), sys.argv[3]
if var == "limite" and scen == "A1":
    P.CAT["radar_sorveglianza_droni"]["falsi_per_passata"] = 5.0      # uccelli e disturbo del terreno: ipotesi
    P.CAT["radar_drone_pannello"]["falsi_per_passata"] = 0.5
    P.RCS["multirotore"] = 0.005                                       # sezione vera meta' di quella della classe
# S1 al limite: MOVI_FALSI_4D=1.0 dall'ambiente (valore del JSON di 02-sensori)
t0 = time.time()
lav = [(scen, c, i) for c in ("min", "alta") for i in range(N)]
with mp.get_context("fork").Pool(8, initializer=P._init) as pool:
    righe = pool.map(P._lavoro, lav, chunksize=2)
err = [r for r in righe if "errore" in r[3]]
agg = P.aggrega(righe)
ris = {"scenario": scen, "variante": var, "N": N, "chiamante": P.CHIAMANTE, "falsi_4D": P.CAT["radar_4d_auto"]["falsi_per_passata"],
       "falsi_IRIS": P.CAT["radar_sorveglianza_droni"]["falsi_per_passata"], "rcs_drone_vero": P.RCS["multirotore"],
       "errori": len(err), "durata_s": round(time.time() - t0, 1), "agg": agg}
json.dump(ris, open(os.path.join(QUI, "limite_%s_%s.json" % (scen, var)), "w"), ensure_ascii=False, indent=1, default=float)
print(scen, var, "errori", len(err), "durata", ris["durata_s"])
