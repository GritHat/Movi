#!/usr/bin/env python3
"""Misura del modo corto su passaggi NUOVI del simulatore (semi mai usati dal catalogo: k >= 100).

Uso:  python -I -B prove/misura_corto.py <braccio> <caso> <k> <uscita.json> [senza_etichette]
  braccio: base | zona | zona_libero     caso: a12 | a05 | b | c | d
Scrive un JSON con i conti del passaggio; `prove/riassumi_misure.py` li somma con Wilson al 95 %.
Il nucleo non vede la verità per decidere: qui la si usa solo per CONTARE (simulazione)."""
import json
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RADICE)
from movi import config, nucleo, registro, sorgenti          # noqa: E402
from movi.corto import dentro                                 # noqa: E402

BRACCI = {"base": {}, "zona": {"predittore_zona": True},
          "zona_libero": {"predittore_zona": True, "libero_dal_fotogramma": True}}
ORIZZONTI = (15, 30, 45)        # 1, 2, 3 s a 15 Hz


def ombra_vera_interna(polare, par):
    """Maschere sulla griglia della catena: ombra vera (codici 1 e 3) e sua parte interna (8 vicine pure in ombra)."""
    na, nr = par.n_azimut, par.n_distanza
    ombra = np.zeros((na, nr), bool)
    righe = polare["celle"]
    az0, pa = polare["azimut_gradi_centro_prima"], polare["passo_gradi"]
    for ir in range(min(nr, polare["n_distanze"])):
        for j, ch in enumerate(righe[ir]):
            ia = int(math.floor(az0 + j * pa + par.azimut_max_gradi))
            if 0 <= ia < na and ch in "13":
                ombra[ia, ir] = True
    p = np.zeros((na + 2, nr + 2), bool)
    p[1:-1, 1:-1] = ombra
    interna = ombra.copy()
    for da in (0, 1, 2):
        for dr in (0, 1, 2):
            interna &= p[da:da + na, dr:dr + nr]
    return ombra, interna


def misura(braccio, caso, k, etichette=True):
    nome = f"d435i_nom__pannello_{caso}__s{k}"
    cfg = config.Configurazione(sorgente={"tipo": "simulata", "nome": nome}, interruttori=BRACCI[braccio],
                                etichette=os.path.join(RADICE, "etichette", "persone.json") if etichette else "")
    sor = sorgenti.apri(cfg)
    nuc = nucleo.crea(cfg, sor.meta)
    testa = nuc.intestazione()
    g = testa["griglie"]["polare_corto"]
    ombra, interna = ombra_vera_interna(sor.ombra_vera, nuc.par)
    righe = [testa]
    r = {"braccio": braccio, "caso": caso, "k": k, "nome": nome, "fotogrammi": 0, "nascosti": 0,
         "nascosti_senza_avviso": 0, "dopo_ingresso": 0, "dopo_ingresso_senza_regione_ne_avviso": 0,
         "libero_in_ombra_interna": 0, "libero_in_ombra_bordo": 0, "celle_ombra_interna": 0,
         "orizzonti": {}, "tempi_ms": [], "riaggancio": [], "nascite_dopo_ingresso": 0, "tornata_visibile": False,
         "ritardo_avviso_cicli": None, "firme": []}
    t_ingresso, inizio_nascosto, prima_nascosta, n_fot = None, None, None, 0
    for fot in sor:
        v = sor.verita(fot.indice)
        riga = nuc.passo(fot, verita=v)
        righe.append(riga)
        n_fot += 1
        r["tempi_ms"].append(riga["tempo_ciclo_ms"])
        st = nuc.griglia_stati()
        lib = st == 1
        r["libero_in_ombra_interna"] += int((lib & interna).sum())
        r["libero_in_ombra_bordo"] += int((lib & ombra & ~interna).sum())
        r["celle_ombra_interna"] += int(interna.sum())
        r["firme"].append([sorted((a["id_traccia"], len(a["indici"]), sum(a["indici"])) for a in riga["avvisi"]),
                           [(s["livello"], s["d_m"]) for s in riga["settori"]], riga["celle"]["conteggi"]])
        for ev in riga["eventi"]:
            if ev["tipo"] == "ingresso_in_ombra" and t_ingresso is None:
                t_ingresso = fot.t
            if ev["tipo"] == "nascita" and t_ingresso is not None:
                r["nascite_dopo_ingresso"] += 1
            if ev["tipo"] == "riaggancio":
                tr = [x for x in riga["tracce"] if x["id"] == ev["traccia"]]
                r["riaggancio"].append({"t": fot.t, "identita": tr[0]["identita"] if tr else None})
        o = v["oggetti"][0]
        if o["visibile"]:
            if inizio_nascosto is not None:
                r["tornata_visibile"] = True
            inizio_nascosto = None
            continue
        if inizio_nascosto is None:
            inizio_nascosto = fot.indice
            prima_nascosta = fot.indice if prima_nascosta is None else prima_nascosta
        r["nascosti"] += 1
        r["nascosti_senza_avviso"] += not riga["avvisi"]
        if riga["avvisi"] and r["ritardo_avviso_cicli"] is None:
            r["ritardo_avviso_cicli"] = fot.indice - prima_nascosta
        regioni = any(x.get("regione") for x in riga["tracce"])
        if t_ingresso is not None:
            r["dopo_ingresso"] += 1
            r["dopo_ingresso_senza_regione_ne_avviso"] += not (riga["avvisi"] or regioni)
        h = fot.indice - inizio_nascosto
        if h in ORIZZONTI:
            m, s = dentro(riga, o["pos"][0], o["pos"][1], g)
            entro_portata = math.hypot(*o["pos"][:2]) < g["portata_m"]
            r["orizzonti"][str(h // 15)] = {"mostrato": bool(m), "stretta": s, "entro_portata": entro_portata}
    r["fotogrammi"] = n_fot
    errori = registro.valida_sequenza(righe)
    r["avvisi_tolti_senza_guardare"] = sum("tolto senza guardare" in e for _, e in errori)
    r["righe_non_valide"] = len({i for i, _ in errori})
    r["errori"] = [e for _, e in errori[:5]]
    return r


if __name__ == "__main__":
    braccio, caso, k, uscita = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    r = misura(braccio, caso, k, etichette=not (len(sys.argv) > 5 and sys.argv[5] == "senza_etichette"))
    with open(uscita, "w", encoding="utf-8") as f:
        json.dump(r, f)
    print(uscita, r["nascosti"], r["dopo_ingresso_senza_regione_ne_avviso"], r["libero_in_ombra_interna"])
