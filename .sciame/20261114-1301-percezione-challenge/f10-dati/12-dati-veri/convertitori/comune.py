"""Parti comuni dei convertitori di sciame-dati (f10): percorsi, scrittura nel formato comune, statistiche.

Si usa da uno script lanciato con `…/ambiente/venv/bin/python -I -B`, che aggiunge questa cartella a sys.path.
Non importa né esegue niente da `scaricati/`: da lì si leggono solo byte, con numpy, opencv, json, csv, rosbags.
"""
import json
import os
import sys

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
F10 = os.path.realpath(os.path.join(QUI, "..", ".."))
SCARICATI = os.path.join(F10, "scaricati")
SEQUENZE = os.path.join(F10, "12-dati-veri", "sequenze")
TRACCE = os.path.join(F10, "12-dati-veri", "tracce")
sys.path.insert(0, os.path.join(F10, "03-infrastruttura"))

import numpy as np  # noqa: E402
from controlla_sequenza import (leggi_meta, leggi_profondita, leggi_tempi, leggi_verita,  # noqa: E402,F401
                                scrivi_sequenza)

# Bordi dell'istogramma delle distanze, in millimetri (ultimo intervallo: oltre 10 m).
BORDI_MM = [1, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 7000, 10000, 65536]


def cartella_nuova(nome):
    """Cartella della sequenza: deve non esistere o essere vuota (non si sovrascrive mai una conversione)."""
    c = os.path.join(SEQUENZE, nome)
    if os.path.isdir(c) and os.listdir(c):
        raise SystemExit(f"la cartella {c} esiste già e non è vuota: toglila a mano se vuoi rifare la conversione")
    return c


def statistiche(cartella):
    """Statistiche descrittive di una sequenza nel formato comune, su TUTTI i fotogrammi."""
    meta = leggi_meta(cartella)
    indici, tempi = leggi_tempi(cartella)
    n = len(indici)
    validi = np.zeros(n)
    isto = np.zeros(len(BORDI_MM) - 1, dtype=np.int64)
    mediane = np.zeros(n)
    minimo, massimo = 65535, 0
    for k, i in enumerate(indici):
        a = leggi_profondita(cartella, i)
        v = a[a > 0]
        validi[k] = v.size / a.size
        if v.size:
            isto += np.histogram(v, bins=BORDI_MM)[0]
            mediane[k] = np.median(v)
            minimo, massimo = min(minimo, int(v.min())), max(massimo, int(v.max()))
    dt = np.diff(tempi)
    tot = int(isto.sum())
    s = {
        "fotogrammi": n,
        "durata_s": round(float(tempi[-1] - tempi[0]), 3) if n > 1 else 0.0,
        "frequenza_mediana_hz": round(float(1 / np.median(dt)), 2) if n > 1 else None,
        "intervallo_max_s": round(float(dt.max()), 4) if n > 1 else None,
        "quota_intervalli_oltre_1_5_volte_la_mediana": round(float((dt > 1.5 * np.median(dt)).mean()), 4) if n > 1 else None,
        "pixel_validi_per_fotogramma": {"min": round(float(validi.min()), 4), "mediana": round(float(np.median(validi)), 4),
                                        "max": round(float(validi.max()), 4)},
        "profondita_mm": {"min": minimo if tot else None, "mediana_delle_mediane": round(float(np.median(mediane))),
                          "max": massimo if tot else None},
        "istogramma_distanze": {"bordi_mm": BORDI_MM[:-1] + ["oltre"], "quota": [round(float(x) / max(tot, 1), 4) for x in isto]},
    }
    quota_3m = float(isto[:6].sum()) / max(tot, 1)
    s["quota_validi_entro_3_m"] = round(quota_3m, 4)
    v = leggi_verita(cartella)
    if v is not None:
        ids, nascosti, tratti, ricomparse, stato, lung, corr = set(), 0, 0, 0, {}, [], {}
        ind2t = dict(zip(indici, tempi))
        for f in v["fotogrammi"]:
            for sg in f["soggetti"]:
                ids.add(sg["id"])
                prima = stato.get(sg["id"])
                if not sg["visibile"]:
                    nascosti += 1
                    if prima is not False:
                        tratti += 1
                        corr[sg["id"]] = ind2t[f["indice"]]
                elif prima is False:
                    ricomparse += 1
                    lung.append(ind2t[f["indice"]] - corr[sg["id"]])
                stato[sg["id"]] = sg["visibile"]
        s["verita"] = {"fotogrammi_annotati": len(v["fotogrammi"]), "identita": len(ids), "presenze_nascoste": nascosti,
                       "tratti_nascosti": tratti, "tratti_nascosti_con_ricomparsa": ricomparse,
                       "durata_tratti_con_ricomparsa_s": {"min": round(min(lung), 2), "mediana": round(float(np.median(lung)), 2),
                                                          "max": round(max(lung), 2)} if lung else None}
    else:
        s["verita"] = None
    s["byte_su_disco"] = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(cartella) for f in fs)
    return meta, s


def salva_json(percorso, oggetto):
    with open(percorso, "w", encoding="utf-8") as f:
        json.dump(oggetto, f, ensure_ascii=False, indent=1)
        f.write("\n")
