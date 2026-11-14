#!/usr/bin/env python3
"""La catena sulle 8 sequenze VERE (12-dati-veri/sequenze): celle per stato, tracce, costo per ciclo, posa stimata.

Per ogni sequenza: un fotogramma ogni 2 se è a 30 fps (15 Hz come il nucleo); parametri del nucleo e, a parte,
min_punti_ostacolo = 40·(pixel/101760) (la soglia scelta sul simulato, riportata al numero di pixel). Dove la posa
manca la catena la stima dai primi 5 fotogrammi (RANSAC). TUM gira tre volte: posa mediana, posa per fotogramma
(dalla cattura del moto: `posa_per_fotogramma.csv`), posa stimata. Solo descrittivo: non c'è verità della scena.
Per DepthTrack e Princeton (riquadro annotato, x e z derivati dalla profondità): quota dei fotogrammi con un gruppo
entro 0,6 m dal bersaglio, identità prima e dopo i tratti annotati come del tutto nascosti, e scarto tipo del centro
attorno a una media mobile di 11 fotogrammi (limite superiore del rumore del centro: include il moto del corpo).
Uso: <python> -I -B corri_vere.py [testo nel nome] [max cicli] → uscite/vere/<sequenza>__<variante>/ e RIEPILOGO.jsonl (in coda)"""
import csv
import dataclasses
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K                                             # noqa: E402
import numpy as np                                             # noqa: E402
from catena import Catena                                      # noqa: E402
from geometria import Proiezione, posa_da_normale, punti_camera, stima_suolo  # noqa: E402

MAX_CICLI = None


def stima_suolo_vincolata(fotogrammi, meta, rollio_max_gradi=10.0, seme=0, n_prove=2000, tolleranza_m=0.03):
    """COPIA corretta di geometria.stima_suolo (codice di validazione): in più scarta i piani con rollio oltre
    `rollio_max_gradi` (una camera su treppiede non è ruotata di 30°). Stessa uscita: (posa, frazione concorde)."""
    gen = np.random.default_rng(seme)
    p = np.concatenate([punti_camera(f, meta) for f in fotogrammi])
    if len(p) > 20000:
        p = p[gen.choice(len(p), 20000, replace=False)]
    meglio, n_meglio = None, 0
    for _ in range(n_prove):
        a, b, c = p[gen.choice(len(p), 3, replace=False)]
        n = np.cross(b - a, c - a)
        lung = np.linalg.norm(n)
        if lung < 1e-9:
            continue
        n = n / lung
        d = -float(n @ a)
        if d < 0:
            n, d = -n, -d
        if -n[1] < 0.5 or not (0.2 <= d <= 3.0) or abs(math.degrees(math.asin(max(-1.0, min(1.0, n[0]))))) > rollio_max_gradi:
            continue
        k = int((np.abs(p @ n + d) <= tolleranza_m).sum())
        if k > n_meglio:
            meglio, n_meglio = (n, d), k
    if meglio is None:
        raise ValueError("nessun piano del suolo con rollio ammesso")
    conc = np.abs(p @ meglio[0] + meglio[1]) <= tolleranza_m
    q = p[conc]
    centro = q.mean(axis=0)
    n = np.linalg.svd(q - centro, full_matrices=False)[2][-1]
    d = -float(n @ centro)
    if d < 0:
        n, d = -n, -d
    return posa_da_normale(d, n, stimata=True, nota="stimata con vincolo sul rollio (copia di validazione)"), n_meglio / len(p)

RADICE = os.path.join(K.USCITE, "vere")


def posa(h, t_gradi, rollio_gradi=0.0, nota=""):
    t, r = math.radians(t_gradi), math.radians(rollio_gradi)
    su = np.array([math.sin(r), -math.cos(t) * math.cos(r), -math.sin(t) * math.cos(r)])
    return posa_da_normale(h, su, nota=nota)


def una(nome, variante, par, ogni, posa_fissa=None, pose_per_fotogramma=None, portata=None, bersaglio=False,
        vincolata=False):
    cart = os.path.join(K.SEQ_VERE, nome)
    sorg = K.SorgenteCartella(cart, ogni=ogni)
    meta = sorg.meta
    par = dataclasses.replace(par, **({"portata_m": portata} if portata else {}))
    out = {"sequenza": nome, "variante": variante, "sensore": meta["sensore"], "pixel": meta["larghezza"] * meta["altezza"],
           "ogni": ogni, "min_punti_ostacolo": par.min_punti_ostacolo, "portata_m": par.portata_m}
    quadri = []
    for q_ in sorg:
        quadri.append(q_)
        if MAX_CICLI and len(quadri) >= MAX_CICLI:
            break
    try:
        if posa_fissa is None and pose_per_fotogramma is None and meta.get("posa") is None:
            posa_fissa, fraz = (stima_suolo_vincolata if vincolata else stima_suolo)([f for _, _, f in quadri[:5]], meta)
            out["posa_stimata"] = {"altezza_m": round(posa_fissa.altezza_m, 3),
                                   "inclinazione_gradi": round(posa_fissa.inclinazione_gradi, 2),
                                   "rollio_gradi": round(posa_fissa.rollio_gradi, 2), "frazione_concorde": round(fraz, 3)}
        p0 = posa_fissa or (pose_per_fotogramma[quadri[0][0]] if pose_per_fotogramma else None)
        cat = Catena(meta, par, p0)
        out["posa_usata"] = {"altezza_m": round(cat.posa.altezza_m, 3), "inclinazione_gradi": round(cat.posa.inclinazione_gradi, 2)}
        tempi, celle, conf, eventi, righe = [], np.zeros(4), set(), {}, []
        muove = set()
        for indice, t, prof in quadri:
            if pose_per_fotogramma is not None:
                cat.mappa.pr = Proiezione(meta, pose_per_fotogramma[indice], par)      # la posa vera di quel fotogramma
            t0 = time.perf_counter()
            r = cat.ciclo(indice, t, prof)
            tempi.append((time.perf_counter() - t0) * 1000)
            celle += np.array([r["celle"][n] for n in ("non_osservato", "libero", "occupato", "in_ombra")])
            for tr in r["tracce"]:
                if tr["stato"] != "in_conferma":
                    conf.add(tr["id"])
                    if tr["si_muove"] is True:
                        muove.add(tr["id"])
            for e in r["eventi"]:
                eventi[e["tipo"]] = eventi.get(e["tipo"], 0) + 1
            righe.append(r)
        n = len(tempi)
        tot = celle.sum()
        out.update(fotogrammi=n, errore=None,
                   celle_per_fotogramma={k: round(float(v) / n, 1) for k, v in zip(("non_osservato", "libero", "occupato", "in_ombra"), celle)},
                   frazione={k: round(float(v / tot), 4) for k, v in zip(("non_osservato", "libero", "occupato", "in_ombra"), celle)},
                   libero_min_mediana_max=[int(np.min([r["celle"]["libero"] for r in righe])),
                                           float(np.median([r["celle"]["libero"] for r in righe])),
                                           int(np.max([r["celle"]["libero"] for r in righe]))],
                   pixel_validi_frazione=round(float(np.mean([r["pixel_validi"] for r in righe])) / out["pixel"], 3),
                   tracce_confermate=len(conf), tracce_si_muove=len(muove), durata_s=round(quadri[-1][1] - quadri[0][1], 2),
                   eventi=eventi,
                   tempo_ciclo_ms={"media": round(float(np.mean(tempi)), 2), "p95": round(float(np.percentile(tempi, 95)), 2),
                                   "massimo": round(float(np.max(tempi)), 2)})
        if bersaglio:
            out["bersaglio"] = segui_bersaglio(cart, righe, cat)
        os.makedirs(os.path.join(RADICE, f"{nome}__{variante}"), exist_ok=True)
        with open(os.path.join(RADICE, f"{nome}__{variante}", "fotogrammi.jsonl"), "w", encoding="utf-8") as f:
            for r in righe:
                f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    except K.InvarianteViolato as e:
        out["errore"] = f"INVARIANTE: {e}"
    except Exception as e:
        out["errore"] = f"{type(e).__name__}: {e}"
    return out


def segui_bersaglio(cart, righe, cat):
    """Bersaglio annotato (x, z nel riferimento della CAMERA, derivati dalla profondità): lo porto sul suolo con la
    posa usata dalla catena, assumendo il centro del riquadro a metà corpo (Yc ignota → uso solo x e z·cos t)."""
    ver = {f["indice"]: f["soggetti"][0] for f in K.leggi_verita(cart)["fotogrammi"] if f["soggetti"]}
    ct = math.cos(math.radians(cat.posa.inclinazione_gradi))
    per_indice = {r["indice"]: r for r in righe}
    visti, con_gruppo, serie, ident = 0, 0, [], {}
    nascosti = sorted(i for i, s in ver.items() if s.get("occlusione_totale") or not s.get("visibile", True))
    for i, r in sorted(per_indice.items()):
        s = ver.get(i)
        if s is None or s.get("x") is None or s.get("z") is None or i in nascosti:
            continue
        x, z = s["x"], s["z"] * ct
        if math.hypot(x, z) > cat.par.portata_m - 0.3:
            continue
        visti += 1
        g = min(r["gruppi"], key=lambda g_: math.hypot(g_["x"] - x, g_["z"] - z), default=None)
        if g is not None and math.hypot(g["x"] - x, g["z"] - z) <= 0.6:
            con_gruppo += 1
            serie.append((i, r["t"], g["x"], g["z"]))
        tr = min((t_ for t_ in r["tracce"] if t_["stato"] == "osservato"),
                 key=lambda t_: math.hypot(t_["ultima_misura"][0] - x, t_["ultima_misura"][1] - z), default=None)
        if tr is not None and math.hypot(tr["ultima_misura"][0] - x, tr["ultima_misura"][1] - z) <= 0.6:
            ident[i] = tr["id"]
    # tratti del tutto nascosti: identità nell'ultimo fotogramma tracciato prima (entro 1 s) e nel primo dopo
    tratti, cur = [], []
    for i in nascosti:
        if cur and i - cur[-1] > 1:
            tratti.append(cur)
            cur = []
        cur.append(i)
    if cur:
        tratti.append(cur)
    esiti = []
    for tr_ in tratti:
        prima = [ident[i] for i in sorted(ident) if tr_[0] - 30 <= i < tr_[0]]
        dopo = [ident[i] for i in sorted(ident) if tr_[-1] < i <= tr_[-1] + 30]
        esiti.append({"fotogrammi": [tr_[0], tr_[-1]], "id_prima": prima[-1] if prima else None,
                      "id_dopo": dopo[0] if dopo else None,
                      "esito": ("non decidibile" if not prima or not dopo else "stessa" if prima[-1] == dopo[0] else "diversa")})
    # rumore del centro: residuo attorno a una media mobile di 11 fotogrammi contigui
    res = {"<2 m": [], "2-3 m": [], "3-4 m": [], ">4 m": []}
    a = np.array(serie) if serie else np.zeros((0, 4))
    for k in range(5, len(a) - 5):
        fin = a[k - 5:k + 6]
        if fin[-1, 0] - fin[0, 0] > 10 * (a[1, 0] - a[0, 0] if len(a) > 1 else 1) + 0.5:
            continue
        m = fin[:, 2:4].mean(axis=0)
        d = math.hypot(*m)
        ur = m / d
        e = a[k, 2:4] - m
        banda = "<2 m" if d < 2 else "2-3 m" if d < 3 else "3-4 m" if d < 4 else ">4 m"
        res[banda].append((float(e @ ur), float(e @ np.array([ur[1], -ur[0]]))))
    rum = {b: ({"N": len(v), "radiale_cm": round(100 * float(np.std([x[0] for x in v])), 1),
                "trasversale_cm": round(100 * float(np.std([x[1] for x in v])), 1)} if len(v) >= 20 else {"N": len(v)})
           for b, v in res.items()}
    return {"fotogrammi_annotati_in_portata": visti, "con_un_gruppo_entro_0,6_m": con_gruppo,
            "identita_distinte_sul_bersaglio": len(set(ident.values())), "tratti_nascosti": esiti,
            "scarto_del_centro_attorno_alla_media_mobile": rum}


def main():
    os.makedirs(RADICE, exist_ok=True)
    base = K.Parametri()
    tutti = []
    global MAX_CICLI
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    MAX_CICLI = int(sys.argv[2]) if len(sys.argv) > 2 else None
    nomi = sorted(n for n in os.listdir(K.SEQ_VERE) if filtro in n)
    for nome in nomi:
        with open(os.path.join(K.SEQ_VERE, nome, "meta.json"), encoding="utf-8") as f:
            meta = json.load(f)
        ogni = 2 if meta["fps"] >= 25 else 1
        p_scalato = max(3, int(round(40 * meta["larghezza"] * meta["altezza"] / 101760)))
        ber = nome.startswith(("depthtrack", "princeton"))
        varianti = [("nucleo", base, None, None), (f"p{p_scalato}", dataclasses.replace(base, min_punti_ostacolo=p_scalato), None, None),
                    (f"p{p_scalato}_rollio_vincolato", dataclasses.replace(base, min_punti_ostacolo=p_scalato), "vincolata", None)]
        if nome.startswith("tum"):
            pose = {}
            with open(os.path.join(K.SEQ_VERE, nome, "posa_per_fotogramma.csv"), encoding="utf-8", newline="") as f:
                for riga in csv.DictReader(f):
                    pose[int(riga["indice"])] = posa(float(riga["altezza_m"]), float(riga["inclinazione_gradi"]),
                                                     float(riga["rollio_gradi"]), "cattura del moto, per fotogramma")
            varianti = [("posa_mediana", base, None, None), ("posa_per_fotogramma", base, None, pose),
                        (f"posa_per_fotogramma_p{p_scalato}", dataclasses.replace(base, min_punti_ostacolo=p_scalato), None, pose),
                        ("posa_per_fotogramma_5m", dataclasses.replace(base, portata_m=5.0), None, pose)]
        for var, par, pf, ppf in varianti:
            vinc = pf == "vincolata"
            r = una(nome, var, par, ogni, None if vinc else pf, ppf, portata=(4.0 if ber else None), bersaglio=ber,
                    vincolata=vinc)
            tutti.append(r)
            print(json.dumps(r, ensure_ascii=False), flush=True)
        if nome.startswith("tum"):                    # posa stimata dalla catena, a confronto con quella vera
            with open(os.path.join(K.SEQ_VERE, nome, "meta.json"), encoding="utf-8") as f:
                m2 = json.load(f)
            sorg = K.SorgenteCartella(os.path.join(K.SEQ_VERE, nome), ogni=2)
            try:
                ps, fr = stima_suolo([f_ for _, _, f_ in list(sorg)[:5]], m2)
                r = {"sequenza": nome, "variante": "solo stima del suolo", "posa_stimata": {
                    "altezza_m": round(ps.altezza_m, 3), "inclinazione_gradi": round(ps.inclinazione_gradi, 2),
                    "rollio_gradi": round(ps.rollio_gradi, 2), "frazione_concorde": round(fr, 3)},
                    "posa_vera_primo_fotogramma": {"altezza_m": round(pose[0].altezza_m, 3),
                                                   "inclinazione_gradi": round(pose[0].inclinazione_gradi, 2)}}
            except Exception as e:
                r = {"sequenza": nome, "variante": "solo stima del suolo", "errore": f"{type(e).__name__}: {e}"}
            tutti.append(r)
            print(json.dumps(r, ensure_ascii=False), flush=True)
    with open(os.path.join(RADICE, "RIEPILOGO.jsonl"), "a", encoding="utf-8") as f:
        for r in tutti:
            f.write(json.dumps(dict(r, max_cicli=MAX_CICLI), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
