"""Controlla ogni sequenza convertita (programma dell'infrastruttura, tutti i fotogrammi) e ne calcola le statistiche.

Uso:  …/ambiente/venv/bin/python -I -B statistiche_tutte.py
Scrive 12-dati-veri/statistiche.json (una voce per sequenza e per traccia). Non modifica le sequenze.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune  # noqa: E402
import numpy as np  # noqa: E402
from controlla_sequenza import controlla  # noqa: E402

esito = {"sequenze": {}, "tracce": {}}
for nome in sorted(os.listdir(comune.SEQUENZE)):
    c = os.path.join(comune.SEQUENZE, nome)
    errori, avvisi, note = controlla(c, tutti=True)
    meta, s = comune.statistiche(c)
    s["controllo_infrastruttura"] = {"errori": errori, "avvisi": avvisi,
                                     "note": [n for n in note if not n.startswith("meta.json: chiave in più")]}
    # Rumore nel tempo su una griglia di pixel (ha senso solo a scena e camera ferme: lo decide chi legge).
    indici, _ = comune.leggi_tempi(c)
    k = indici[: min(len(indici), 120)]
    pila = np.stack([comune.leggi_profondita(c, i)[::8, ::8] for i in k]).astype(np.float64)
    sempre = (pila > 0).all(0)
    s["primi_fotogrammi_griglia_8px"] = {
        "fotogrammi": len(k), "pixel_sempre_validi": round(float(sempre.mean()), 4),
        "pixel_mai_validi": round(float((pila == 0).all(0).mean()), 4),
        "pixel_intermittenti": round(float(1 - sempre.mean() - (pila == 0).all(0).mean()), 4),
        "scarto_tipo_nel_tempo_mm_mediana": round(float(np.median(pila[:, sempre].std(0))), 2) if sempre.any() else None,
        "scarto_tipo_nel_tempo_mm_90pct": round(float(np.percentile(pila[:, sempre].std(0), 90)), 2) if sempre.any() else None}
    esito["sequenze"][nome] = s
    v = s["verita"]
    print(f"{nome}: {s['fotogrammi']} fot, {s['durata_s']} s, {s['frequenza_mediana_hz']} Hz, validi mediana "
          f"{s['pixel_validi_per_fotogramma']['mediana']:.3f} [{s['pixel_validi_per_fotogramma']['min']:.3f}-{s['pixel_validi_per_fotogramma']['max']:.3f}], "
          f"prof mediana {s['profondita_mm']['mediana_delle_mediane']} mm, entro 3 m {s['quota_validi_entro_3_m']:.3f}, "
          f"errori {len(errori)}, avvisi {len(avvisi)}, verità {None if v is None else (v['identita'], v['tratti_nascosti'], v['tratti_nascosti_con_ricomparsa'], v['durata_tratti_con_ricomparsa_s'])}")
    for a in avvisi + errori:
        print("    !", a[:230])
if os.path.isdir(comune.TRACCE):
    for nome in sorted(os.listdir(comune.TRACCE)):
        z = np.load(os.path.join(comune.TRACCE, nome, "tracce.npz"), allow_pickle=False)
        xy, t = z["xy_m"], z["tempo_s"]
        val = np.isfinite(xy[:, :, 0])
        tratti = []
        for j in range(val.shape[1]):
            d = np.diff(np.concatenate([[0], val[:, j].astype(int), [0]]))
            tratti += list((np.where(d == -1)[0] - np.where(d == 1)[0]) / 100.0)
        tratti = np.array(tratti)
        v = np.hypot(*np.moveaxis(np.diff(xy, axis=0), 2, 0)) * 100
        vm = v[np.isfinite(v) & (v > 0.2)]
        s = {"istanti": int(len(t)), "frequenza_hz": 100.0, "durata_s": round(float(t[-1]), 2), "persone": [str(x) for x in z["id"]],
             "quota_tracciata_per_persona": [round(float(x), 3) for x in val.mean(0)],
             "tratti_continui": {"numero": int(len(tratti)), "almeno_3_s": int((tratti >= 3).sum()), "almeno_6_s": int((tratti >= 6).sum()),
                                 "almeno_10_s": int((tratti >= 10).sum()), "mediana_s": round(float(np.median(tratti)), 2), "max_s": round(float(tratti.max()), 1)},
             "velocita_m_s": {"mediana_sopra_0_2": round(float(np.median(vm)), 3), "p95": round(float(np.percentile(vm, 95)), 3),
                              "p99_9": round(float(np.percentile(vm, 99.9)), 3)},
             "area_m": {"x": [round(float(np.nanmin(xy[:, :, 0])), 2), round(float(np.nanmax(xy[:, :, 0])), 2)],
                        "y": [round(float(np.nanmin(xy[:, :, 1])), 2), round(float(np.nanmax(xy[:, :, 1])), 2)]}}
        esito["tracce"][nome] = s
        print(nome, s["tratti_continui"], s["velocita_m_s"], s["area_m"])
comune.salva_json(os.path.join(comune.F10, "12-dati-veri", "statistiche.json"), esito)
