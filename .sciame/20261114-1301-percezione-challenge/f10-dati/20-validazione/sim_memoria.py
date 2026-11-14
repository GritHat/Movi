#!/usr/bin/env python3
"""Sequenze generate IN MEMORIA con il simulatore di 11-simulatore (sola lettura, importato) e passate nella catena.

  bordi    V22: passaggi a12 s00–s09 (D435i nominale) con l'interruttore «bordi» spento; stessi semi di quelli su disco
  coperto  V24: `sensore_coperto` con i filtri del costruttore accesi
  fermi    V9, V10: persona ferma a 2 / 3 / 4 m e scatola di 15 cm a 2 / 3 m, 20 semi di rumore l'una
  lenti    V11: persona a 0,5 m/s che attraversa a 2 / 3 / 4 m e che si avvicina da 4,3 a 1,8 m, 20 passaggi l'una
Uso: <python> -I -B sim_memoria.py <bordi|coperto|fermi|lenti> [min_punti_ostacolo] [indici dei casi, es. 2,3]"""
import copy
import dataclasses
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K                                             # noqa: E402
import numpy as np                                             # noqa: E402

sys.path.insert(0, K.SIM)
import catalogo as C                                           # noqa: E402
import genera as G                                             # noqa: E402
import simsens as S                                            # noqa: E402
from catena import Catena                                      # noqa: E402

_passaggio_originale = C.passaggio


def passaggio_di_validazione(caso, k, scena_nome="pannello"):
    """Aggiunge ai casi del catalogo: `trD` (attraversa a z = D decimetri, 0,5 m/s) e `avv` (si avvicina)."""
    if not (caso.startswith("tr") or caso == "avv"):
        return _passaggio_originale(caso, k, scena_nome)
    rng = np.random.default_rng(S.seme_da_nome(f"validazione__{caso}__s{k:02d}"))
    verso = 1.0 if k % 2 == 0 else -1.0
    v = 0.5 * rng.uniform(0.9, 1.1)
    if caso == "avv":
        x0 = rng.uniform(-0.3, 0.3)
        punti = [(x0, 4.3), (x0, 1.8)]
    else:
        z = int(caso[2:]) / 10.0 + rng.uniform(-0.03, 0.03)
        punti = [(-verso * 0.8, z), (verso * 0.8, z)]
    x, z, vx, vz = C.campiona_percorso(punti, v, {}, "via", rng)
    return x, z, vx, vz, {"caso": caso, "passaggio": k, "velocita_crociera_ms": round(v, 4)}


C.passaggio = passaggio_di_validazione


def genera(spec, interruttori=None):
    tempi, quadri, vers, extra = [], [], [], None
    for i, t, f, ver, extra in G.simula(spec, interruttori=interruttori):
        tempi.append(t)
        quadri.append(f)
        vers.append(ver)
    meta, verita = G.meta_e_verita(spec, extra["prof"], extra["cam"], extra["scena"], extra["tracce"], vers)
    return meta, tempi, quadri, verita


def passa(meta, tempi, quadri, par):
    cat = Catena(meta, par)
    righe, stati = [], []
    for i, (t, f) in enumerate(zip(tempi, quadri)):
        righe.append(cat.ciclo(i, t, f))
        stati.append(cat.mappa_ciclo.stati.copy())
    return righe, np.array(stati)


def bordi(p_min):
    import misura_passaggi
    radice = os.path.join(K.USCITE, f"mem_bordi_spenti_p{p_min}")
    ver_dir = os.path.join(radice, "_verita")
    nomi = []
    for k in range(10):
        spec = C._spec("a12", "d435i", "nominale", "pannello", f"pannello_a12__s{k:02d}", persone=[C._pers("a12", k)])
        meta, tempi, quadri, verita = genera(spec, {"bordi": False})
        os.makedirs(os.path.join(ver_dir, spec["nome"]), exist_ok=True)
        with open(os.path.join(ver_dir, spec["nome"], "verita.json"), "w", encoding="utf-8") as f:
            json.dump(verita, f)
        K.corri(K.SorgenteMemoria(meta, tempi, quadri), os.path.join(radice, spec["nome"]),
                dataclasses.replace(K.Parametri(), min_punti_ostacolo=p_min))
        nomi.append(spec["nome"])
    K.SEQ_SIM = ver_dir
    spenti = [misura_passaggi.misura(n, radice) for n in nomi]
    K.SEQ_SIM = os.path.join(K.SIM, "sequenze")
    accesi = [misura_passaggi.misura(n, os.path.join(K.USCITE, "sim" if p_min == 3 else f"sim_p{p_min}")) for n in nomi]
    for etichetta, ms in (("bordi ACCESI (su disco)", accesi), ("bordi SPENTI (in memoria)", spenti)):
        print(f"{etichetta}, min_punti_ostacolo={p_min}, a12 s00–s09: fusione persona–pannello a soggetto intero "
              f"{sum(1 for m in ms if m['fusione_fotogrammi_interi'] > 0)} su 10; fotogrammi di fusione (mediana) "
              f"{np.median([m['fusione_fotogrammi'] for m in ms]):.0f}; continuità pulita "
              f"{sum(1 for m in ms if m.get('continuita_pulita'))} su 10; stessa identità "
              f"{sum(1 for m in ms if m.get('esito_identita') == 'stessa')}; tracce fantasma (mediana) "
              f"{np.median([m['tracce_fantasma'] for m in ms]):.0f}; pannello «si muove» "
              f"{sum(1 for m in ms if m['pannello_si_muove'])} su 10")


def coperto():
    base = [s for s in C.catalogo() if s["nome"] == "d435i_nom__sensore_coperto"][0]
    for filtri in (False, True):
        spec = copy.deepcopy(base)
        spec["filtri"] = filtri
        spec["nome"] = spec["nome_base"] + ("__filtri" if filtri else "")
        meta, tempi, quadri, verita = genera(spec)
        righe, stati = passa(meta, tempi, quadri, K.Parametri())
        validi = [int(np.count_nonzero(q)) for q in quadri]
        cop = [i for i, v in enumerate(verita["fotogrammi"]) if v.get("evento", {}).get("copertura")]
        lib = [r["celle"]["libero"] for r in righe]
        print(f"sensore coperto, filtri {'ACCESI' if filtri else 'spenti'}: fotogrammi coperti {cop[0]}–{cop[-1]} "
              f"({len(cop)}); pixel validi nei coperti min–max {min(validi[i] for i in cop)}–{max(validi[i] for i in cop)} "
              f"su {quadri[0].size}; celle «libero» prima {lib[cop[0] - 1]}; nei coperti dal 3° in poi: min "
              f"{min(lib[i] for i in cop[2:])}, max {max(lib[i] for i in cop[2:])}, fotogrammi con «libero» > 0: "
              f"{sum(1 for i in cop[2:] if lib[i] > 0)} su {len(cop) - 2}; «libero» per fotogramma coperto: "
              f"{[lib[i] for i in cop]}")
        tr = [[t_["stato"] for t_ in r["tracce"] if t_["stato"] != "in_conferma"] for r in righe]
        print("   stati delle tracce confermate nei fotogrammi coperti (primo, terzo, ultimo):",
              tr[cop[0]], tr[cop[2]], tr[cop[-1]])


def centro_piu_vicino(riga, x, z, raggio=0.6):
    meglio, d = None, raggio
    for g in riga["gruppi"]:
        dd = math.hypot(g["x"] - x, g["z"] - z)
        if dd < d:
            meglio, d = g, dd
    return meglio


def traccia_vicina(riga, x, z, raggio=0.6):
    meglio, d = None, raggio
    for tr in riga["tracce"]:
        if tr["stato"] == "in_conferma" or not tr["misura_nel_ciclo"]:
            continue
        dd = math.hypot(tr["ultima_misura"][0] - x, tr["ultima_misura"][1] - z)
        if dd < d:
            meglio, d = tr, dd
    return meglio


def fermi(p_min):
    par = dataclasses.replace(K.Parametri(), portata_m=4.5, min_punti_ostacolo=p_min)
    fuori = []
    casi = [("persona", d) for d in (2.0, 3.0, 4.0)] + [("scatola15", d) for d in (2.0, 3.0)]
    casi = [c for i, c in enumerate(casi) if not SOLO or i in SOLO]
    for tipo, d in casi:
        sr, st, falsi, visti, altri_muove, n_celle = [], [], 0, 0, 0, []
        for seme in range(20):
            if tipo == "persona":
                spec = C._spec("val", "d435i", "nominale", "pavimento", f"val_ferma_{d}__s{seme:02d}", n=45,
                               persone=[C._ferma(0.3, d)])
                x0, z0 = 0.3, d
            else:
                spec = C._spec("val", "d435i", "nominale", "scatola15", f"val_scatola_{d}__s{seme:02d}",
                               {"distanza": d}, n=45)
                x0, z0 = 0.0, d + 0.075
            meta, tempi, quadri, _ = genera(spec)
            righe, _ = passa(meta, tempi, quadri, par)
            c = [(g["x"], g["z"], g["celle"]) for g in (centro_piu_vicino(r, x0, z0, 0.35) for r in righe) if g]
            muove = any(tr["si_muove"] is True for r in righe for tr in [traccia_vicina(r, x0, z0, 0.35)] if tr)
            altri_muove += any(t_["si_muove"] is True and math.hypot(t_["ultima_misura"][0] - x0, t_["ultima_misura"][1] - z0) > 0.35
                               for r in righe for t_ in r["tracce"] if t_["stato"] != "in_conferma")
            if len(c) >= 30:
                visti += 1
                c = np.array(c)
                r0 = math.hypot(x0, z0)
                ur, ut = np.array([x0, z0]) / r0, np.array([z0, -x0]) / r0
                sr.append(float(np.std(c[:, :2] @ ur)))
                st.append(float(np.std(c[:, :2] @ ut)))
                n_celle.append(float(np.median(c[:, 2])))
            falsi += muove
        riga = {"oggetto": tipo, "distanza_m": d, "N": 20, "visto_in_30_fotogrammi_su_45": visti,
                "sigma_radiale_cm_mediana_max": [100 * float(np.median(sr)), 100 * float(np.max(sr))] if sr else None,
                "sigma_trasversale_cm_mediana_max": [100 * float(np.median(st)), 100 * float(np.max(st))] if st else None,
                "celle_mediane": float(np.median(n_celle)) if n_celle else None,
                "sequenze_con_si_muove_falso": falsi, "sequenze_con_altre_tracce_si_muove": altri_muove,
                "soglia_radiale_cm": 100 * 5 * math.sqrt(2) * par.sigma_radiale(d),
                "soglia_trasversale_cm": 100 * 5 * math.sqrt(2) * par.sigma_tangenziale(d)}
        fuori.append(riga)
        print(json.dumps(riga, ensure_ascii=False), flush=True)
    with open(os.path.join(K.USCITE, f"mem_fermi_p{p_min}{ETI}.json"), "w", encoding="utf-8") as f:
        json.dump(fuori, f, ensure_ascii=False, indent=1)


def lenti(p_min):
    par = dataclasses.replace(K.Parametri(), portata_m=4.5, min_punti_ostacolo=p_min)
    fuori = []
    for caso in [c for i, c in enumerate(("tr20", "tr30", "tr40", "avv")) if not SOLO or i in SOLO]:
        entro, mai, ritardi, senza_traccia, tagl = 0, 0, [], 0, []
        fasce = {"3,5-4,3": [0, 0], "2,5-3,5": [0, 0], "1,8-2,5": [0, 0]}
        for k in range(20):
            spec = C._spec("val", "d435i", "nominale", "pavimento", f"val_{caso}__s{k:02d}", persone=[C._pers(caso, k)])
            meta, tempi, quadri, verita = genera(spec)
            righe, _ = passa(meta, tempi, quadri, par)
            t_primo, t_muove, n_tagl, n_mis = None, None, 0, 0
            for r, f in zip(righe, verita["fotogrammi"]):
                s = f["soggetti"][0]
                tr = traccia_vicina(r, s["x"], s["z"])
                g = centro_piu_vicino(r, s["x"], s["z"])
                if g is not None and t_primo is None:
                    t_primo = r["t"]                       # primo fotogramma con un gruppo sul soggetto
                if tr is not None:
                    n_mis += 1
                    n_tagl += tr["misura_tagliata"]
                    if tr["si_muove"] is True and t_muove is None:
                        t_muove = r["t"]
                    if caso == "avv":
                        for nome_f, (a, b) in (("3,5-4,3", (3.5, 4.31)), ("2,5-3,5", (2.5, 3.5)), ("1,8-2,5", (1.8, 2.5))):
                            if a <= s["z"] < b:
                                fasce[nome_f][0] += tr["si_muove"] is True
                                fasce[nome_f][1] += 1
            if t_primo is None:
                senza_traccia += 1
            elif t_muove is None:
                mai += 1
            else:
                ritardi.append(t_muove - t_primo)
                entro += (t_muove - t_primo) <= 1.0 + 1e-6
            tagl.append(n_tagl / n_mis if n_mis else float("nan"))
        riga = {"caso": caso, "N": 20, "si_muove_entro_1_s_dal_primo_gruppo": entro, "mai": mai,
                "mai_visto": senza_traccia, "IC95": [round(v, 3) for v in K.wilson(entro, 20)],
                "ritardo_s_mediana_max": [float(np.median(ritardi)), float(np.max(ritardi))] if ritardi else None,
                "quota_misure_tagliate_mediana": float(np.nanmedian(tagl))}
        if caso == "avv":
            riga["quota_fotogrammi_si_muove_per_distanza"] = {k_: (v[0] / v[1] if v[1] else None) for k_, v in fasce.items()}
        fuori.append(riga)
        print(json.dumps(riga, ensure_ascii=False), flush=True)
    with open(os.path.join(K.USCITE, f"mem_lenti_p{p_min}{ETI}.json"), "w", encoding="utf-8") as f:
        json.dump(fuori, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    cosa = sys.argv[1]
    p_min = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    SOLO = [int(v) for v in sys.argv[3].split(",")] if len(sys.argv) > 3 else []      # indici dei casi da fare
    ETI = ("_casi" + "".join(str(v) for v in SOLO)) if SOLO else ""
    {"bordi": lambda: bordi(p_min), "coperto": coperto, "fermi": lambda: fermi(p_min), "lenti": lambda: lenti(p_min)}[cosa]()
