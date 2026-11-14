#!/usr/bin/env python3
"""genera.py — genera le sequenze del simulatore nel formato comune (f10, 11-simulatore).

Uso (sempre con l'interprete dell'ambiente, -I -B):
  …/ambiente/venv/bin/python -I -B genera.py --elenco                 # che cosa c'è nel catalogo e quanto pesa
  …/ambiente/venv/bin/python -I -B genera.py --gruppo a12             # genera un gruppo (salta ciò che esiste)
  …/ambiente/venv/bin/python -I -B genera.py --nome d435i_nom__pavimento_vuoto [--rifai]
  …/ambiente/venv/bin/python -I -B genera.py --indice                 # riscrive sequenze/INDICE.csv

Da codice (senza scrivere su disco):
  import sys; sys.path.insert(0, "<…>/f10-dati/11-simulatore")
  import genera, catalogo
  spec = catalogo.catalogo()[0]          # oppure una specifica propria (stesse chiavi)
  for i, t, prof_mm, ver, extra in genera.simula(spec): ...
"""
import csv
import math
import os
import shutil
import sys
import time

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
sys.path.insert(0, os.path.normpath(os.path.join(QUI, "..", "03-infrastruttura")))

import numpy as np                                  # noqa: E402
from scipy import ndimage, special                  # noqa: E402

import catalogo as C                                # noqa: E402
import simsens as S                                 # noqa: E402
from controlla_sequenza import scrivi_sequenza      # noqa: E402

SEQUENZE = os.path.join(QUI, "sequenze")


def prepara(spec, larghezza=424):
    prof = S.carica_profilo(spec["profilo"], spec["livello"], larghezza=larghezza)
    sc, incl = C.scena(spec["scena"], **spec["arg"])
    cam = S.Camera(prof, altezza_m=1.2, inclinazione_gradi=incl)
    statica = S.resa_statica(sc, cam)
    tracce, n = [], spec.get("n")
    for p in spec["persone"]:
        if "fermo" in p:
            tracce.append({"fermo": True, "par": {"fermo": p["fermo"]}})
        else:
            x, z, vx, vz, par = C.passaggio(p["caso"], p["k"])
            tracce.append({"x": x, "z": z, "vx": vx, "vz": vz, "par": par})
            n = len(x) if n is None else min(n, len(x))
    for p, tr in zip(spec["persone"], tracce):
        if tr.get("fermo"):
            tr["x"], tr["z"] = np.full(n, p["fermo"][0]), np.full(n, p["fermo"][1])
            tr["vx"], tr["vz"] = np.zeros(n), np.zeros(n)
    return prof, cam, sc, statica, tracce, int(n)


def simula(spec, larghezza=424, interruttori=None, fps=C.FPS):
    """Generatore: (indice, tempo_s, profondità uint16 in mm, verità del fotogramma, extra).
    extra: {"ideale": Ideale, "sensore": Sensore, "grezzo": uint16 prima dei filtri}."""
    prof, cam, sc, statica, tracce, n = prepara(spec, larghezza)
    seme = S.seme_da_nome(spec["nome_base"])
    sens = S.Sensore(prof, cam, seme, interruttori)
    filtri = S.FiltriRealsense() if spec.get("filtri") else None
    ev = spec.get("eventi") or {}
    campo_azz = None
    if "azzeramento" in ev:
        g = np.random.default_rng(seme + 1).standard_normal((cam.H, cam.W))
        g = ndimage.gaussian_filter(g, 12.0, mode="wrap")
        campo_azz = special.ndtr(g / g.std())
    for i in range(n):
        t = i / fps
        persone, blur = [], []
        for p, tr in zip(spec["persone"], tracce):
            persone.append(S.Persona(p["id"], tr["x"][i], tr["z"][i], altezza=p["altezza"], materiale=p["materiale"]))
            r = math.hypot(tr["x"][i], tr["z"][i])
            v_perp = abs(tr["vx"][i] * tr["z"][i] - tr["vz"][i] * tr["x"][i]) / max(r, 1e-6)
            blur.append(0.5 * v_perp * prof["esposizione_s"])
        idl, conteggi = S.componi(statica, cam, persone, blur) if persone else (statica, [])
        forza, evento = None, {}
        if "copertura" in ev and ev["copertura"]["da_s"] <= t < ev["copertura"]["a_s"]:
            forza = np.ones((cam.H, cam.W), dtype=bool)
            if ev["copertura"]["parte"] == "sinistra":
                forza[:, cam.W // 2:] = False
            evento["copertura"] = ev["copertura"]["parte"]
        if campo_azz is not None:
            q = min(1.0, max(0.0, (t - ev["azzeramento"]["da_s"]) / (ev["azzeramento"]["a_s"] - ev["azzeramento"]["da_s"])))
            forza = campo_azz < q
            evento["quota_azzerata"] = round(q, 4)
        grezzo = sens.misura(idl, forza_zero=forza)
        uscita = filtri.applica(grezzo) if filtri else grezzo
        sogg = []
        for k, (p, tr) in enumerate(zip(spec["persone"], tracce)):
            sag, vis = conteggi[k]
            validi = int(((sens.ultimo["obj"] == S.O_PERSONA0 + k) & (grezzo > 0)).sum())
            sogg.append({"id": p["id"], "x": round(float(tr["x"][i]), 4), "z": round(float(tr["z"][i]), 4),
                         "visibile": vis > 0, "frazione_visibile": round(vis / sag, 4) if sag else 0.0,
                         "vx": round(float(tr["vx"][i]), 4), "vz": round(float(tr["vz"][i]), 4),
                         "pixel_sagoma": sag, "pixel_visibili": vis, "pixel_validi": validi,
                         "raggio_m": 0.2, "altezza_m": p["altezza"], "materiale": S.MATERIALI[p["materiale"]]})
        ver = {"indice": i, "soggetti": sogg}
        if evento:
            ver["evento"] = evento
        yield i, t, uscita, ver, {"ideale": idl, "sensore": sens, "grezzo": grezzo, "prof": prof, "cam": cam,
                                  "scena": sc, "tracce": tracce}


def meta_e_verita(spec, prof, cam, sc, tracce, fotogrammi_ver, fps=C.FPS):
    liv = spec["livello"]
    filtri = " + filtri SDK RealSense (temporale con persistenza 3, riempimento modo 1)" if spec.get("filtri") else ""
    meta = dict(cam.meta())
    meta.update({
        "fps": fps,
        "sensore": f"simulato: {prof['nome_json']}, livello {liv}, 848x480 campionato a {cam.W}x{cam.H}{filtri}",
        "origine": f"f10-dati/11-simulatore/genera.py --nome {spec['nome']} (simsens.py {S.VERSIONE}; modello "
                   "f10-dati/02-sensori/parametri_sensori.json)",
        "licenza": "nessun vincolo (dati generati)",
        "simulazione": {
            "versione": S.VERSIONE, "nome": spec["nome"], "gruppo": spec["gruppo"], "profilo": prof["nome_json"],
            "livello": liv, "scena": spec["scena"], "argomenti": spec["arg"], "filtri_costruttore": bool(spec.get("filtri")),
            "seme_rumore": S.seme_da_nome(spec["nome_base"]), "eventi": spec.get("eventi") or {},
            "percorsi": [tr["par"] for tr in tracce], "parametri_sensore": prof,
            "nota": "tempi = istanti di metà esposizione, regolari; nessun fotogramma perso; "
                    "la base stereo è lungo +x (imager destro a destra del sinistro)",
        },
    })
    verita = {"fotogrammi": fotogrammi_ver, "ostacoli": sc.in_verita(),
              "ombra_suolo": S.maschere_ombra(sc, cam, prof),
              "camera": {"altezza_m": cam.h, "inclinazione_gradi": cam.incl, "base_m": cam.base},
              "nota": "x, z: centro dell'impronta del soggetto sul suolo; visibile = almeno un pixel ideale del "
                      "soggetto non coperto; frazione_visibile = pixel non coperti / pixel della sagoma nell'immagine; "
                      "pixel_validi = pixel del soggetto con un dato dopo il modello del sensore (prima dei filtri)"}
    return meta, verita


def scrivi(spec, radice=SEQUENZE, rifai=False):
    dest = os.path.join(radice, spec["nome"])
    if os.path.isdir(dest) and os.listdir(dest):
        if not rifai:
            return None
        if os.path.commonpath([os.path.realpath(dest), os.path.realpath(radice)]) != os.path.realpath(radice):
            raise RuntimeError("destinazione fuori dalla radice")
        shutil.rmtree(dest)
    t0 = time.perf_counter()
    tempi, quadri, vers, extra = [], [], [], None
    for i, t, f, ver, extra in simula(spec):
        tempi.append(t)
        quadri.append(f)
        vers.append(ver)
    meta, verita = meta_e_verita(spec, extra["prof"], extra["cam"], extra["scena"], extra["tracce"], vers)
    t1 = time.perf_counter()
    scrivi_sequenza(dest, meta, tempi, quadri, verita)
    return len(quadri), t1 - t0, time.perf_counter() - t1


def riga_indice(spec, n):
    par = spec["persone"][0] if spec["persone"] else {}
    return {"nome": spec["nome"], "gruppo": spec["gruppo"], "profilo": S.SIGLE[spec["profilo"]],
            "livello": spec["livello"], "scena": spec["scena"], "caso": par.get("caso", "fermo" if par else ""),
            "passaggio": par.get("k", ""), "materiale_persona": S.MATERIALI[par["materiale"]] if par else "",
            "altezza_persona_m": par.get("altezza", ""), "filtri": int(bool(spec.get("filtri"))),
            "fotogrammi": n, "percorso": os.path.join("sequenze", spec["nome"])}


def main(argv):
    L = C.catalogo()
    if "--elenco" in argv:
        tot, per_gruppo = 0, {}
        for s in L:
            n = prepara(s)[5]
            tot += n
            per_gruppo[s["gruppo"]] = per_gruppo.get(s["gruppo"], 0) + n
            print(f"{s['gruppo']:9s} {n:4d}  {s['nome']}")
        byte = tot * (424 * 240 * 2 + 128)
        print(f"TOTALE: {len(L)} sequenze, {tot} fotogrammi, {byte / 1e9:.3f} GB di .npy; per gruppo: {per_gruppo}")
        return 0
    if "--indice" in argv:
        os.makedirs(SEQUENZE, exist_ok=True)
        righe = []
        for s in L:
            d = os.path.join(SEQUENZE, s["nome"], "profondita")
            if os.path.isdir(d):
                righe.append(riga_indice(s, len(os.listdir(d))))
        with open(os.path.join(SEQUENZE, "INDICE.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(righe[0].keys()))
            w.writeheader()
            w.writerows(righe)
        print(f"INDICE.csv: {len(righe)} sequenze su {len(L)} del catalogo, {sum(r['fotogrammi'] for r in righe)} fotogrammi")
        return 0
    rifai = "--rifai" in argv
    scelte = []
    if "--gruppo" in argv:
        g = argv[argv.index("--gruppo") + 1]
        scelte = [s for s in L if s["gruppo"] == g]
    elif "--nome" in argv:
        nm = argv[argv.index("--nome") + 1]
        scelte = [s for s in L if s["nome"] == nm]
    if not scelte:
        print(__doc__)
        return 2
    os.makedirs(SEQUENZE, exist_ok=True)
    n_tot, t_sim, t_scr = 0, 0.0, 0.0
    for s in scelte:
        r = scrivi(s, rifai=rifai)
        if r is None:
            print(f"già presente, salto: {s['nome']}")
            continue
        n_tot += r[0]
        t_sim += r[1]
        t_scr += r[2]
        print(f"{s['nome']}: {r[0]} fotogrammi, simulazione {1000 * r[1] / r[0]:.1f} ms/fotogramma", flush=True)
    if n_tot:
        print(f"FATTO: {n_tot} fotogrammi; simulazione {t_sim:.1f} s ({1000 * t_sim / n_tot:.1f} ms/fotogramma), "
              f"scrittura {t_scr:.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
