#!/usr/bin/env python3
"""Prova del formato del registro sul modo corto: passa una sequenza nella catena riusata (senza toccarla),
converte ogni uscita con registro.da_catena e la valida. Uso:
    python -I -B prove/prova_registro.py <cartella della sequenza> [uscita.jsonl | -] [senza_correzioni]
Stampa: righe, righe non valide, limite superiore di Wilson al 95 %, stati visti. Esce con 3 se una riga non è valida."""
import collections
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from movi import config, corto, registro, riuso, tabellone          # noqa: E402


def main(argv):
    cartella = argv[1]
    spente = len(argv) > 3 and argv[3] == "senza_correzioni"
    cfg = config.Configurazione(sorgente={"tipo": "sequenza", "cartella": cartella},
                                interruttori={"correzioni_f12": not spente})
    cat, par, sor = riuso.modulo("catena", "catena"), riuso.modulo("catena", "parametri"), riuso.modulo("catena", "sorgente")
    sorgente = sor.SorgenteCartella(cartella)
    p = corto.parametri_da_config(cfg)
    catena = cat.Catena(sorgente.meta, p)
    testa = registro.intestazione(cfg, {"polare_corto": {"tipo": "polare", "passo_azimut_gradi": p.passo_azimut_gradi,
                                                         "passo_distanza_m": p.passo_distanza_m,
                                                         "azimut_max_gradi": p.azimut_max_gradi, "portata_m": p.portata_m}},
                                  {"origine": "sensore", "assi": "x a destra, y in avanti"}, nota="prova del formato")
    righe = [testa]
    stati, eventi, avvisi = collections.Counter(), collections.Counter(), 0
    for indice, t, prof in sorgente:
        riga = registro.da_catena(catena.ciclo(indice, t, prof), cfg, etichette=None)
        stati.update(tr["stato"] for tr in riga["tracce"])
        eventi.update((e["tipo"], e["come_lo_so"]) for e in riga["eventi"])
        avvisi += bool(riga["avvisi"])
        righe.append(riga)
    errori = registro.valida_sequenza(righe)
    n = len(righe) - 1
    cattive = len({i for i, _ in errori})
    print(f"sequenza: {os.path.basename(cartella.rstrip('/'))}; regole accese: {cfg.dichiarazioni()['regole_accese']}")
    print(f"fotogrammi: {n}; righe non valide: {cattive} su {n}; Wilson 95 %: [{tabellone.wilson(cattive, n)[0]:.4f}, "
          f"{tabellone.wilson(cattive, n)[1]:.4f}]")
    print(f"stati delle tracce (fotogrammi-traccia): {dict(stati)}")
    print(f"eventi: {dict(eventi)}")
    print(f"fotogrammi con avviso di possibile presenza: {avvisi}")
    for i, x in errori[:10]:
        print(f"  riga {i}: {x}")
    if len(argv) > 2 and argv[2] != "-":
        s = registro.Scrittore(argv[2], severo=False)
        for r in righe:
            s.scrivi(r)
        # fase 2b (sciame-sviluppatore, 15-11-2026): `movi convalida` vuole la riga di riassunto in fondo (collaudo);
        # senza, il passo 05 di prova_tutto falliva con «registro interrotto». Riassunto minimo, dichiarato.
        s.scrivi({"tipo": "riassunto", "fotogrammi": n, "nota": "prova del formato (prova_registro.py): riassunto minimo"})
        s.chiudi()
    return 3 if errori else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
