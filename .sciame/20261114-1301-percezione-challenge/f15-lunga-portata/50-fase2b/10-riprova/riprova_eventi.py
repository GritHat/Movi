"""riprova_eventi.py - E1, E2 (alta) ed E4 (alta, min) con lo strato eventi_v2 e il NUCLEO v2, come caricati dal
prototipo (movi.lungo.moduli(), nucleo v2: regole v2, mappa dichiarata completa). Stesse soglie di EVENTI_V2 § 2.
Uso: <venv>/bin/python -I -B riprova_eventi.py N12 N4 PROCESSI -> riprova_eventi_esito.json, riprova_eventi_passaggi.jsonl
Un record per passaggio; Wilson 95 % per passaggio (eventi_v2.aggrega). Solo simulazione; nessuna scrittura altrove."""
import json
import os
import sys
import time
from multiprocessing import Pool

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
PROTO = os.path.abspath(os.path.join(QUI, "..", "..", "..", "..", "..", "prototipo"))
_E = {}


def _e2():
    if not _E:
        sys.path.insert(0, PROTO)
        from movi import lungo
        lungo.scegli_nucleo("v2")
        M = lungo.moduli()
        _E.update(E=M["eventi_v2"], nucleo=M["nucleo"], m=M["m"].__name__)
    return _E["E"]


def lavoro(a):
    return a, _e2()._lavoro(a)[1]


if __name__ == "__main__":
    N12, N4, NP = int(sys.argv[1]), int(sys.argv[2]), min(int(sys.argv[3]), 7)
    t0 = time.time()
    lav = [(e, "alta", i) for e in ("E2", "E1") for i in range(N12)] + [("E4", c, i) for c in ("alta", "min") for i in range(N4)]
    with Pool(NP) as p:
        righe = p.map(lavoro, lav, chunksize=1)
    E = _e2()
    agg = {}
    with open(os.path.join(QUI, "riprova_eventi_passaggi.jsonl"), "w", encoding="utf-8") as f:
        for a, r in righe:
            f.write(json.dumps({"lavoro": list(a), **r}, ensure_ascii=False, default=float) + "\n")
            agg.setdefault("%s/%s" % (a[0], a[1]), []).append(r)
    out = {}
    for k, rr in agg.items():
        ok = [r for r in rr if "errore" not in r]
        err = [r for r in rr if "errore" in r]
        out[k] = dict(E.aggrega(ok) if ok else {}, errori=len(err), esempio_errore=err[0]["traccia"] if err else None)
    ris = {"avvertenza": "SIMULAZIONE; strato eventi_v2 (copia del prototipo) con nucleo v2; non indipendente dallo strato",
           "nucleo": E.NUCLEO, "nucleo_modulo": _E["m"], "durata_s": round(time.time() - t0, 1),
           "n": {"E1_E2": N12, "E4": N4}, "risultati": out}
    json.dump(ris, open(os.path.join(QUI, "riprova_eventi_esito.json"), "w", encoding="utf-8"), ensure_ascii=False,
              indent=1, default=float)
    print(json.dumps(ris, ensure_ascii=False, default=float)[:6000])
