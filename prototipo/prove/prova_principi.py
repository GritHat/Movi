#!/usr/bin/env python3
"""Prove automatiche dei principi e del nucleo corto (script; esce con 1 se una prova cade). Uso:
    python -I -B prove/prova_principi.py [rapida]
  1. sv-P9  pavimento vuoto (catalogo): 0 tracce confermate, 0 avvisi
  2. sv-P10 sensore coperto 1,0–2,2 s (catalogo): affidabilità persa entro 0,27 s dall'inizio della copertura e fino
            alla fine; 0 celle «libero» o «occupato» in quei fotogrammi; settori tutti «affidabilita_persa»
  3. sv-P8  etichette: con e senza il file, avvisi, settori e celle identici riga per riga (b, k = 100…, braccio
            zona+libero; 10 passaggi, 2 con «rapida»)
  4. sv-P7  controllo fra righe: un registro artefatto con un avviso tolto senza guardare deve essere RIFIUTATO
  5. principio 1 su un registro artefatto: «libero» con affidabilità persa deve essere rifiutato
  6. sv-P6  tempo per ciclo, un processo (b, k = 100…109; 2 con «rapida»): mediana e p95
Tutto è simulazione: nessuna di queste prove riguarda un sensore fisico."""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, RADICE)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from movi import config, nucleo, registro, sorgenti          # noqa: E402
import misura_corto                                           # noqa: E402

SEQ = os.path.normpath(os.path.join(RADICE, "..", ".sciame", "20261114-1301-percezione-challenge", "f10-dati",
                                    "11-simulatore", "sequenze"))
ESITI = []


def esito(nome, ok, testo):
    ESITI.append(ok)
    print(f"[{'ok' if ok else 'CADE'}] {nome}: {testo}")


def gira(cartella, interruttori=None):
    cfg = config.Configurazione(sorgente={"tipo": "sequenza", "cartella": cartella}, interruttori=interruttori or {})
    sor = sorgenti.apri(cfg)
    nuc = nucleo.crea(cfg, sor.meta)
    return [nuc.passo(f, sor.verita(f.indice)) for f in sor]


def main(rapida):
    # 1. pavimento vuoto
    righe = gira(os.path.join(SEQ, "d435i_nom__pavimento_vuoto"), {"predittore_zona": True, "libero_dal_fotogramma": True})
    conf = {tr["id"] for r in righe for tr in r["tracce"] if tr["stato"] != "in_conferma"}
    avv = sum(bool(r["avvisi"]) for r in righe)
    visti = sum(s["livello"] == "visto_libero_fino_a" for r in righe for s in r["settori"])
    esito("sv-P9 pavimento vuoto", not conf and not avv,
          f"{len(righe)} fotogrammi, tracce confermate {len(conf)}, fotogrammi con avviso {avv}; "
          f"settori-fotogramma «visto libero fino a d»: {visti} su {sum(len(r['settori']) for r in righe)}")
    # 2. sensore coperto
    righe = gira(os.path.join(SEQ, "d435i_nom__sensore_coperto"), {"predittore_zona": True, "libero_dal_fotogramma": True})
    coperti = [r for r in righe if (r.get("verita") or {}).get("evento", {}).get("copertura")]
    t0 = min(r["t"] for r in coperti)
    tardivi = [r["indice"] for r in coperti if r["t"] - t0 > 0.27 and r["affidabilita"] != "persa"]
    celle = sum(r["celle"]["conteggi"].get("libero", 0) + r["celle"]["conteggi"].get("occupato", 0)
                for r in righe if r["affidabilita"] == "persa")
    sett = all(s["livello"] == "affidabilita_persa" for r in righe if r["affidabilita"] == "persa" for s in r["settori"])
    prima = min((r["t"] for r in coperti if r["affidabilita"] == "persa"), default=None)
    esito("sv-P10 sensore coperto", not tardivi and celle == 0 and sett and prima is not None,
          f"{len(coperti)} fotogrammi coperti da t = {t0:.3f} s; affidabilità persa dichiarata da t = {prima} "
          f"(ritardo {None if prima is None else round(prima - t0, 3)} s); coperti oltre 0,27 s senza dichiarazione: "
          f"{len(tardivi)}; celle libere o occupate con affidabilità persa: {celle}; settori tutti persi: {sett}")
    # 3. etichette
    ks = range(100, 102 if rapida else 110)
    diff = 0
    for k in ks:
        a = misura_corto.misura("zona_libero", "b", k, etichette=True)["firme"]
        b = misura_corto.misura("zona_libero", "b", k, etichette=False)["firme"]
        diff += sum(json.dumps(x) != json.dumps(y) for x, y in zip(a, b)) + abs(len(a) - len(b))
    esito("sv-P8 etichette non toccano avvisi, settori, celle", diff == 0, f"{len(ks)} passaggi b, righe diverse: {diff}")
    # 4 e 5. il controllo fra righe e quello di principio rifiutano i registri artefatti
    cfg = config.Configurazione()
    base = {"tipo": "fotogramma", "modo": "corto", "indice": 0, "t": 0.0,
            "dichiarazioni": {k: v for k, v in cfg.dichiarazioni().items() if k in ("dati", "etichette", "regole_accese", "config")},
            "sensori": [{"id": "p", "salute": "in_salute"}], "affidabilita": "ok", "celle": {"conteggi": {}},
            "settori": [], "tracce": [], "eventi": []}
    av = {"tipo": "possibile_presenza", "id_traccia": 1, "eta_s": 0.1,
          "forma": {"tipo": "settore_anulare", "azimut_gradi": [0, 5], "distanza_m": [2, 3]}}
    seq = [{"tipo": "intestazione", "dichiarazioni": {}}, dict(base, avvisi=[av]), dict(base, indice=1, t=0.07, avvisi=[])]
    e = registro.valida_sequenza(seq)
    esito("sv-P7 controllo fra righe (artefatto)", any("tolto senza guardare" in x for _, x in e), f"errori trovati: {e}")
    persa = dict(base, avvisi=[], affidabilita="persa", celle={"conteggi": {"libero": 3}})
    e = registro.valida_riga(persa)
    esito("principio 1 (artefatto)", any("PRINCIPIO" in x for x in e), f"errori trovati: {e}")
    # 6. tempo per ciclo, un processo
    tempi = []
    for k in range(100, 102 if rapida else 110):
        t0 = time.perf_counter()
        tempi += misura_corto.misura("zona_libero", "b", k)["tempi_ms"]
    tempi.sort()
    med, p95 = tempi[len(tempi) // 2], tempi[int(0.95 * (len(tempi) - 1))]
    esito("sv-P6 tempo per ciclo (un processo)", p95 <= 66.7,
          f"{len(tempi)} cicli: mediana {med:.1f} ms, p95 {p95:.1f} ms, massimo {tempi[-1]:.1f} ms")
    return 0 if all(ESITI) else 1


if __name__ == "__main__":
    sys.exit(main(len(sys.argv) > 1 and sys.argv[1] == "rapida"))
