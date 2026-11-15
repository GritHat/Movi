#!/usr/bin/env python3
"""Misura NOTATA DOPO (non era fra le previsioni): quanto dura la regione STRETTA del predittore della zona e se
contiene la persona vera, su tutti i fotogrammi a persona nascosta (non solo a 1, 2, 3 s).
Uso: python -I -B prove/misura_stretta.py <caso> <k0> <k1>   (braccio zona+libero)"""
import os
import sys

sys.dont_write_bytecode = True
RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RADICE)
from movi import config, nucleo, sorgenti                     # noqa: E402
from movi.corto import dentro                                 # noqa: E402
from movi.tabellone import wilson                             # noqa: E402


def main(caso, k0, k1):
    k_in = n = 0
    durate = []
    for k in range(k0, k1 + 1):
        cfg = config.Configurazione(sorgente={"tipo": "simulata", "nome": f"d435i_nom__pannello_{caso}__s{k}"},
                                    interruttori={"predittore_zona": True, "libero_dal_fotogramma": True})
        sor = sorgenti.apri(cfg)
        nuc = nucleo.crea(cfg, sor.meta)
        g = nuc.intestazione()["griglie"]["polare_corto"]
        ultima = 0.0
        for f in sor:
            v = sor.verita(f.indice)
            r = nuc.passo(f, v)
            o = v["oggetti"][0]
            if o["visibile"]:
                continue
            _, s = dentro(r, o["pos"][0], o["pos"][1], g)
            if s is not None:
                n += 1
                k_in += bool(s)
                ultima = max([tr["non_vista_da_s"] for tr in r["tracce"] if tr.get("regione")] + [ultima])
        durate.append(ultima)
    lo, hi = wilson(k_in, n)
    durate.sort()
    print(f"caso {caso}, k {k0}…{k1}: persona dentro la regione stretta {k_in} su {n} fotogrammi "
          f"(Wilson 95 %: {100 * lo:.1f}–{100 * hi:.1f} %); durata della regione stretta dopo l'ingresso: "
          f"mediana {durate[len(durate) // 2]:.2f} s, massimo {durate[-1]:.2f} s")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
