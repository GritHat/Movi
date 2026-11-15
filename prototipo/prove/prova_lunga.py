"""prova_lunga.py — il modo lungo del prototipo rifà GLI STESSI passaggi esemplari di f15 (previsione L1) e le
etichette non cambiano l'avviso (L3). Uso (da prototipo/): $PY -I -B prove/prova_lunga.py [A1,S1,…] [--etichette]
Per ogni esemplare: esegue il passaggio con le sostituzioni dell'osservatore attive e confronta i cicli
(parole, posizioni, raggi, zone, sensori persi) con riuso/lunga_portata/10-simulatore/esemplari/<…>.json.
Tutto è simulazione."""
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from movi import config as C, lungo  # noqa: E402

ES = os.path.join(lungo.SIM, "esemplari")


def cfg_di(scen, chiamante=None, etichette="a_mano"):
    c = C.Configurazione(modo="lungo", scenario=scen, origine_dati="simulati",
                         sorgente={"tipo": "scena_lp", "scenario": scen, "passaggio": 0, "piano": [-10, 10, -10, 10],
                                   "celle_lato": 2, "condizione": {"configurazione": "alta", "etichette": etichette}})
    if chiamante:
        c.sorgente["chiamante"] = chiamante
    return c


def norm(x):
    return json.loads(json.dumps(x, default=lambda v: v.tolist() if hasattr(v, "tolist") else float(v)))


def main():
    sel = sys.argv[1].split(",") if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    esiti = []
    for f in sorted(os.listdir(ES)):
        scen = f.split("_")[0]
        if sel and scen not in sel:
            continue
        chiamante = f[:-5].split("_")[-1] if not scen.startswith("E") else None
        R, _, _ = lungo.esegui_passaggio(cfg_di(scen, chiamante))
        atteso = json.load(open(os.path.join(ES, f), encoding="utf-8"))["cicli"]
        avuto = norm(R["esemplare"]["cicli"])
        diversi = [i for i, (a, b) in enumerate(zip(atteso, avuto)) if a != b] + \
            ([-1] if len(atteso) != len(avuto) else [])
        esiti.append((f, len(atteso), len(diversi)))
        print(f"{f:34s} cicli {len(atteso):4d}  diversi {len(diversi):3d}  {'UGUALE' if not diversi else 'DIVERSO'}",
              flush=True)
    if "--etichette" in sys.argv:
        for scen in (sel or ["A1", "S1"]):
            r = {}
            for et in ("a_mano", "nessuna"):
                R, _, _ = lungo.esegui_passaggio(cfg_di(scen, "prudente", et))
                r[et] = [[(o["id"], o["possibile_presenza_raggio_m"]) for o in c["uscite"]] for c in R["esemplare"]["cicli"]]
            ug = sum(a == b for a, b in zip(r["a_mano"], r["nessuna"]))
            print(f"L3 {scen}: cicli con avvisi identici con e senza etichette {ug} su {len(r['a_mano'])}", flush=True)
    ko = sum(1 for e in esiti if e[2])
    print(f"L1: {len(esiti) - ko} file su {len(esiti)} identici")
    return 1 if ko else 0


if __name__ == "__main__":
    sys.exit(main())
