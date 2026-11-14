#!/usr/bin/env python3
"""Convertitori dei dati pubblici nel formato comune (scena.json + verita.csv).

Uso (interprete dell'ambiente, con -I):
    python -I converti.py <auto|droni|alfa|treni|trajair|live|zenodo|statistiche> <cartella 01-dati>

I dati scaricati sono dati non fidati: qui si leggono solo con csv/json/zipfile.
Tutte le velocita' di verita.csv sono DERIVATE dalle posizioni con una differenza
centrata su una finestra dichiarata (campo "finestra_velocita_s" di scena.json):
niente e' misurato da un sensore di questo progetto.
"""
import csv, io, json, math, os, sys, glob, zipfile, datetime
import numpy as np

R_TERRA = 6371008.8  # sfera media; proiezione equirettangolare locale (errore < 0,5 % su decine di km)


def enu(lat, lon, lat0, lon0):
    x = np.radians(np.asarray(lon) - lon0) * math.cos(math.radians(lat0)) * R_TERRA
    y = np.radians(np.asarray(lat) - lat0) * R_TERRA
    return x, y


def deriva(t, p, W):
    """Differenza centrata su finestra W (s), con interpolazione lineare; ai bordi la finestra si accorcia."""
    tp = np.clip(t + W / 2, t[0], t[-1])
    tm = np.clip(t - W / 2, t[0], t[-1])
    dt = np.maximum(tp - tm, 1e-9)
    return (np.interp(tp, t, p) - np.interp(tm, t, p)) / dt


def cinematica(t, x, y, z, W, vmin):
    vx, vy, vz = deriva(t, x, W), deriva(t, y, W), deriva(t, z, W)
    v = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
    vo = np.hypot(vx, vy)
    a = deriva(t, v, W)                      # accelerazione longitudinale (derivata del modulo)
    rotta = np.unwrap(np.arctan2(vx, vy))    # rotta da nord, in senso orario
    om = np.degrees(deriva(t, rotta, W))     # velocita' di virata, gradi/s
    om = np.where(vo > vmin, om, np.nan)     # sotto vmin la rotta non e' definita
    return vx, vy, vz, v, a, om


def scrivi_tratto(base, classe, nome, tipo, t, x, y, z, W, vmin, origine, extra=None):
    """Scrive una scena con un solo oggetto. Ritorna il riassunto del tratto (per le statistiche)."""
    t = np.asarray(t, float); x = np.asarray(x, float); y = np.asarray(y, float); z = np.asarray(z, float)
    ok = np.concatenate([[True], np.diff(t) > 1e-6])   # tempi strettamente crescenti
    t, x, y, z = t[ok], x[ok], y[ok], z[ok]
    t = t - t[0]
    vx, vy, vz, v, a, om = cinematica(t, x, y, z, W, vmin)
    d = os.path.join(base, "traiettorie", classe, nome)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "verita.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tempo", "id", "x", "y", "z", "vx", "vy", "vz", "vis_rif"])
        for i in range(len(t)):
            w.writerow(["%.3f" % t[i], nome, "%.2f" % x[i], "%.2f" % y[i], "%.2f" % z[i],
                        "%.3f" % vx[i], "%.3f" % vy[i], "%.3f" % vz[i], 1])
    scena = {
        "nome": nome,
        "formato": "f15-comune-0.1",
        "oggetti": [{"id": nome, "classe": classe, "tipo": tipo, "etichetta": "assegnata a mano dal convertitore (dalla fonte), nessun classificatore"}],
        "riferimento": {"sistema": "locale in metri, x est, y nord, z quota", **origine},
        "sensori": [{"id": "rif", "posizione": [0, 0, 0],
                     "nota": "SEGNAPOSTO: nessun sensore e' definito qui; vis_rif=1 ovunque. I ruoli degli scenari mettono sensori e ostacoli e ricalcolano la visibilita'."}],
        "ostacoli": [],
        "finestra_velocita_s": W,
        "velocita": "derivate dalle posizioni (differenza centrata sulla finestra), non misurate",
        "campioni": int(len(t)), "durata_s": float(t[-1]),
        "passo_mediano_s": float(np.median(np.diff(t))) if len(t) > 1 else None,
    }
    scena.update(extra or {})
    with open(os.path.join(d, "scena.json"), "w") as f:
        json.dump(scena, f, ensure_ascii=False, indent=1)
    return {"nome": nome, "classe": classe, "tipo": tipo, "n": int(len(t)), "durata": float(t[-1]),
            "passo": float(np.median(np.diff(t))), "v": v, "a": a, "om": om}


def salva_riassunti(base, chiave, rs):
    """Tiene i campioni cinematici per le statistiche (file .npz per fonte)."""
    d = os.path.join(base, "convertitori", "campioni")
    os.makedirs(d, exist_ok=True)
    tipi = sorted(set(r["tipo"] for r in rs))
    out = {}
    meta = []
    for r in rs:
        meta.append([r["nome"], r["classe"], r["tipo"], r["n"], r["durata"], r["passo"], float(np.max(r["v"]))])
    for tp in tipi:
        sel = [r for r in rs if r["tipo"] == tp]
        out["v__" + tp] = np.concatenate([r["v"] for r in sel])
        out["a__" + tp] = np.concatenate([r["a"] for r in sel])
        out["om__" + tp] = np.concatenate([r["om"] for r in sel])
    np.savez_compressed(os.path.join(d, chiave + ".npz"), **out)
    json.dump(meta, open(os.path.join(d, chiave + "_tratti.json"), "w"))
    print(chiave, "tratti:", len(rs), {tp: sum(1 for r in rs if r["tipo"] == tp) for tp in tipi})


# ---------------------------------------------------------------- AUTO: NGSIM US-101
def auto(base):
    src = os.path.join(base, "scaricati", "auto_ngsim", "us101.csv")
    gr = {}
    with open(src, newline="") as f:
        for r in csv.DictReader(f):
            gr.setdefault(r["vehicle_id"], []).append((int(r["global_time"]), float(r["global_x"]), float(r["global_y"]), r["v_class"]))
    righe = sum(len(v) for v in gr.values())
    X0, Y0 = 6451000.0, 1873000.0   # piedi, piano di stato della California zona 5 (origine locale scelta qui)
    rs = []; scartati = 0
    for vid, pts in sorted(gr.items(), key=lambda kv: int(kv[0])):
        pts.sort()
        tt = np.array([p[0] for p in pts]) / 1000.0
        tagli = np.where(np.diff(tt) > 0.25)[0] + 1   # lo stesso id ricorre in periodi diversi di ripresa
        for k, idx in enumerate(np.split(np.arange(len(pts)), tagli)):
            if len(idx) < 100:
                scartati += 1; continue
            sub = [pts[i] for i in idx]
            t = np.array([p[0] for p in sub]) / 1000.0
            x = (np.array([p[1] for p in sub]) - X0) * 0.3048
            y = (np.array([p[2] for p in sub]) - Y0) * 0.3048
            tipo = {"1": "moto", "2": "auto", "3": "camion"}.get(sub[0][3], "auto")
            rs.append(scrivi_tratto(base, "auto", "ngsim_us101_v%s_%d" % (vid, k), tipo, t, x, y, np.zeros(len(t)), 1.0, 1.0,
                                    {"origine": "piano di stato California zona 5: x0=%.0f ft, y0=%.0f ft; piedi convertiti in metri (0,3048)" % (X0, Y0)},
                                    {"fonte": "NGSIM US-101 (FHWA, US DOT), data.transportation.gov risorsa 8ect-6jqj", "licenza": "dati aperti del governo federale USA (vedi PROVENIENZA.md)",
                                     "tempo_iniziale_ms": sub[0][0]}))
    print("righe lette", righe, "spezzoni scartati (<100 campioni)", scartati)
    salva_riassunti(base, "auto_ngsim", rs)


# ---------------------------------------------------------------- DRONI: CMU, DJI Matrice 100
def droni(base):
    z = zipfile.ZipFile(os.path.join(base, "scaricati", "droni_cmu", "flights.zip"))
    nomi = sorted([n for n in z.namelist() if n.endswith(".csv")], key=lambda s: int(os.path.basename(s)[:-4]))
    rs = []; fermi = 0; rotti = 0
    for n in nomi:
        rows = list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8", newline="")))
        try:
            t = np.array([float(r["time"]) for r in rows]); lon = np.array([float(r["position_x"]) for r in rows])
            lat = np.array([float(r["position_y"]) for r in rows]); alt = np.array([float(r["position_z"]) for r in rows])
        except (ValueError, KeyError):
            rotti += 1; continue
        ok = np.isfinite(t) & np.isfinite(lat) & np.isfinite(lon) & np.isfinite(alt) & (np.abs(lat) > 1)
        t, lon, lat, alt = t[ok], lon[ok], lat[ok], alt[ok]
        if len(t) < 100:
            rotti += 1; continue
        x, y = enu(lat, lon, lat[0], lon[0])
        if np.hypot(x, y).max() < 50:      # prove a terra o in volo stazionario: non sono tratti di moto
            fermi += 1; continue
        num = os.path.basename(n)[:-4]
        rs.append(scrivi_tratto(base, "droni", "cmu_m100_volo%s" % num, "multirotore", t, x, y, alt - alt[0], 1.0, 1.0,
                                {"origine": "primo punto del volo: lat %.6f, lon %.6f, quota %.1f m s.l.m." % (lat[0], lon[0], alt[0])},
                                {"fonte": "Rodrigues et al., Data Collected with Package Delivery Quadcopter Drone, CMU KiltHub, doi:10.1184/R1/12683453", "licenza": "CC BY 4.0",
                                 "nota": "posizione dal GNSS/INS di bordo (3DM-GX5-45, +-2 m orizz., +-5 m vert. secondo il README): e' la verita' migliore disponibile, non una verita' esterna"}))
    print("voli nel file", len(nomi), "fermi/stazionari scartati", fermi, "illeggibili", rotti)
    salva_riassunti(base, "droni_cmu", rs)


# ---------------------------------------------------------------- TRENI: Digitraffic (Finlandia)
def treni(base):
    rs = []; vsrc = []; vder = []; tot_dup = 0; tot = 0; salti = 0
    for fn in sorted(glob.glob(os.path.join(base, "scaricati", "treni_digitraffic", "t*.json")), key=lambda s: int(os.path.basename(s)[1:-5])):
        try:
            d = json.load(open(fn))
        except ValueError:
            continue
        if len(d) < 100:
            continue
        num = os.path.basename(fn)[1:-5]
        m = {}
        for r in d:
            ts = datetime.datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")).timestamp()
            m[ts] = (r["location"]["coordinates"][1], r["location"]["coordinates"][0], r["speed"])
        tot += len(d); tot_dup += len(d) - len(m)
        ts = np.array(sorted(m)); lat = np.array([m[k][0] for k in ts]); lon = np.array([m[k][1] for k in ts]); sp = np.array([m[k][2] for k in ts]) / 3.6
        # salti del GPS: via i punti che dal precedente tenuto implicano piu' di 80 m/s (288 km/h; in Finlandia il massimo e' 220 km/h)
        xx, yy = enu(lat, lon, lat[0], lon[0]); tieni = [0]
        for i in range(1, len(ts)):
            j = tieni[-1]
            if math.hypot(xx[i] - xx[j], yy[i] - yy[j]) <= 80.0 * (ts[i] - ts[j]) + 30.0:
                tieni.append(i)
        salti += len(ts) - len(tieni); tieni = np.array(tieni)
        ts, lat, lon, sp = ts[tieni], lat[tieni], lon[tieni], sp[tieni]
        # spezzoni contigui (buchi < 30 s), poi finestre di 600 s
        cand = []
        for idx in np.split(np.arange(len(ts)), np.where(np.diff(ts) > 30)[0] + 1):
            if len(idx) < 2: continue
            t0 = ts[idx[0]]
            for k in range(int((ts[idx[-1]] - t0) // 600) + 1):
                sel = idx[(ts[idx] >= t0 + 600 * k) & (ts[idx] < t0 + 600 * (k + 1))]
                if len(sel) >= 60 and sp[sel].max() > 5:
                    cand.append(sel)
        if not cand: continue
        scelti = [cand[i] for i in sorted(set(np.linspace(0, len(cand) - 1, min(3, len(cand))).round().astype(int)))]
        for j, sel in enumerate(scelti):
            x, y = enu(lat[sel], lon[sel], lat[sel][0], lon[sel][0])
            r = scrivi_tratto(base, "treni", "fi_treno%s_%d" % (num, j), "treno", ts[sel], x, y, np.zeros(len(sel)), 15.0, 2.0,
                              {"origine": "primo punto del tratto: lat %.6f, lon %.6f; quota non disponibile (z=0)" % (lat[sel][0], lon[sel][0])},
                              {"fonte": "Fintraffic / digitraffic.fi, train-locations del 2026-11-12, treno n. %s" % num, "licenza": "CC BY 4.0",
                               "tempo_iniziale_unix": float(ts[sel][0]), "nota": "posizione dal GPS di bordo; e' la verita' migliore disponibile"})
            rs.append(r); vsrc.append(sp[sel][:len(r["v"])]); vder.append(r["v"])
    a = np.concatenate(vsrc); b = np.concatenate(vder)
    diff = b - a
    print("record", tot, "doppioni di orario rimossi", tot_dup, "salti GPS rimossi", salti)
    print("controllo: velocita' derivata - velocita' della fonte (m/s): mediana %.2f, |.| mediana %.2f, |.| p95 %.2f su %d campioni" % (np.median(diff), np.median(abs(diff)), np.percentile(abs(diff), 95), len(a)))
    json.dump({"n": int(len(a)), "mediana": float(np.median(diff)), "abs_mediana": float(np.median(abs(diff))), "abs_p95": float(np.percentile(abs(diff), 95)),
               "v_fonte_p95": float(np.percentile(a, 95)), "v_fonte_max": float(a.max())},
              open(os.path.join(base, "convertitori", "campioni_controllo_treni.json"), "w"))
    salva_riassunti(base, "treni_digitraffic", rs)


# ---------------------------------------------------------------- AEREI: TrajAir (aviazione generale, 1 Hz)
def trajair(base, massimo=60):
    z = zipfile.ZipFile(os.path.join(base, "scaricati", "aerei_trajair", "7days1.zip"))
    nomi = sorted(n for n in z.namelist() if "/processed_data/" in n and n.endswith(".txt"))
    rs = []; visti = set()
    for n in nomi:
        if len(rs) >= massimo: break
        arr = np.loadtxt(io.TextIOWrapper(z.open(n)), ndmin=2)
        if arr.shape[0] < 60 or arr.shape[1] < 5: continue
        for aid in np.unique(arr[:, 1]):
            if len(rs) >= massimo: break
            s = arr[arr[:, 1] == aid]; s = s[np.argsort(s[:, 0])]
            for idx in np.split(np.arange(len(s)), np.where(np.diff(s[:, 0]) > 5)[0] + 1):
                if len(idx) < 60: continue
                q = s[idx]; x, y, zz = q[:, 2] * 1000, q[:, 3] * 1000, q[:, 4] * 1000
                if np.hypot(x - x[0], y - y[0]).max() < 500: continue
                ch = (int(aid), round(float(x[0]), 1), round(float(y[0]), 1), len(idx))
                if ch in visti: continue       # lo stesso spezzone puo' comparire in piu' file
                visti.add(ch)
                nome = "trajair_%s_%d" % (os.path.basename(n)[:-4], int(aid))
                nome += "_%d" % len([r for r in rs if r["nome"].startswith(nome)])
                rs.append(scrivi_tratto(base, "aerei", nome, "aereo_aviazione_generale_circuito", q[:, 0], x, y, zz, 5.0, 5.0,
                                        {"origine": "fine pista dell'aeroporto di Butler (KBTP), asse x allineato alla pista: NON e' est/nord (riferimento della fonte, lasciato com'e')"},
                                        {"fonte": "Patrikar et al., TrajAir: A General Aviation Trajectory Dataset, CMU KiltHub, doi:10.1184/R1/14866251 (7days1, processed_data)", "licenza": "CC BY 4.0",
                                         "nota": "tracciati ADS-B gia' elaborati dagli autori (interpolati a 1 Hz); avvicinamento, decollo e circuito non sono distinti dalla fonte"}))
                if len(rs) >= massimo: break
    salva_riassunti(base, "aerei_trajair", rs)


# ---------------------------------------------------------------- AEREI: cattura dal vivo adsb.lol attorno a un aeroporto
def live(base):
    LAT0, LON0, Z0 = 33.6407, -84.4277, 313.0   # Atlanta KATL; quota del campo 313 m: A MEMORIA, non verificata
    tr = {}
    files = sorted(glob.glob(os.path.join(base, "scaricati", "aerei_adsblol_live", "s*.json")))
    letti = 0
    for fn in files:
        try:
            s = json.load(open(fn))
        except ValueError:
            continue
        letti += 1
        for a in s.get("ac", []):
            if "lat" not in a or "seen_pos" not in a: continue
            t = s["now"] / 1000.0 - a["seen_pos"]
            terra = a.get("alt_baro") == "ground"
            alt = a.get("alt_geom", a.get("alt_baro"))
            zq = 0.0 if (terra or not isinstance(alt, (int, float))) else alt * 0.3048 - Z0
            tr.setdefault(a["hex"], []).append((round(t, 1), a["lat"], a["lon"], zq, terra, a.get("gs"), a.get("category", ""), a.get("t", ""), a.get("baro_rate", a.get("geom_rate"))))
    rs = []; gsrc = []; gder = []; scart = 0
    for hx, pts in sorted(tr.items()):
        m = {}
        for p in pts:
            m.setdefault(p[0], p)
        ts = np.array(sorted(m)); P = [m[k] for k in ts]
        lat = np.array([p[1] for p in P]); lon = np.array([p[2] for p in P])
        nuovo = np.concatenate([[True], (np.diff(lat) != 0) | (np.diff(lon) != 0) | (np.diff(ts) > 0.5)])
        x, y = enu(lat, lon, LAT0, LON0)
        perc = np.hypot(np.diff(x), np.diff(y)).sum() if len(x) > 1 else 0
        if len(ts) < 20 or perc < 150 or ts[-1] - ts[0] < 40:
            scart += 1; continue
        zq = np.array([p[3] for p in P]); terra = np.array([p[4] for p in P])
        cat = P[0][6]
        if cat == "A7": tipo = "elicottero"
        elif terra.mean() > 0.9: tipo = "aereo_rullaggio"
        elif terra[0] and not terra[-1]: tipo = "aereo_decollo"
        elif terra[-1] and not terra[0]: tipo = "aereo_avvicinamento"
        else:
            dz = zq[~terra][-1] - zq[~terra][0]
            tipo = "aereo_avvicinamento" if dz < -100 else ("aereo_decollo" if dz > 100 else "aereo_sorvolo")
        W = 10.0 if tipo == "aereo_rullaggio" else 5.0
        r = scrivi_tratto(base, "aerei", "atl_%s" % hx, tipo, ts, x, y, zq, W, 3.0,
                          {"origine": "Atlanta KATL: lat %.4f, lon %.4f; z=0 a 313 m s.l.m. (quota del campo A MEMORIA, non verificata); a terra z=0 per costruzione" % (LAT0, LON0)},
                          {"fonte": "adsb.lol, API v2/point, cattura dal vivo (vedi PROVENIENZA.md)", "licenza": "ODbL 1.0", "tempo_iniziale_unix": float(ts[0]),
                           "categoria_emettitore": cat, "tipo_aeromobile": P[0][7], "frazione_a_terra": float(terra.mean()),
                           "nota": "posizione ADS-B trasmessa dall'aereo (GNSS di bordo), quota geometrica se c'e' altrimenti barometrica; tempo = ora della risposta meno seen_pos"})
        rs.append(r)
        g = np.array([p[5] if isinstance(p[5], (int, float)) else np.nan for p in P]) * 0.514444
        gsrc.append(g[:len(r["v"])]); gder.append(r["v"])
    a = np.concatenate(gsrc); b = np.concatenate(gder); ok = np.isfinite(a)
    diff = (b - a)[ok]
    print("istantanee lette", letti, "aerei visti", len(tr), "tracce scartate (corte o ferme)", scart)
    print("controllo: |v derivata (3D)| - gs della fonte (m/s): mediana %.2f, |.| mediana %.2f, |.| p95 %.2f su %d campioni" % (np.median(diff), np.median(abs(diff)), np.percentile(abs(diff), 95), ok.sum()))
    json.dump({"n": int(ok.sum()), "mediana": float(np.median(diff)), "abs_mediana": float(np.median(abs(diff))), "abs_p95": float(np.percentile(abs(diff), 95)), "istantanee": letti},
              open(os.path.join(base, "convertitori", "campioni_controllo_aerei_live.json"), "w"))
    salva_riassunti(base, "aerei_live", rs)


# ---------------------------------------------------------------- AEREI: Zenodo 18916312 (LHR-ZRH, 1 Hz interpolato)
def zenodo(base, massimo=40):
    z = zipfile.ZipFile(os.path.join(base, "scaricati", "aerei_zenodo", "CSV.zip"))
    nomi = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
    print("file nell'archivio", len(nomi))
    rs = []; usati = 0
    for n in nomi:
        if usati >= massimo: break
        rows = list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8", newline="")))
        if len(rows) < 600: continue
        k = {c.lower(): c for c in rows[0].keys()}
        def col(*nomi_c):
            for c in nomi_c:
                if c in k: return np.array([float(r[k[c]] or "nan") for r in rows])
            raise KeyError(str(nomi_c) + " non fra " + str(list(k)))
        try:
            t = col("timestamp", "time"); lat = col("latitude", "lat"); lon = col("longitude", "lon"); alt = col("altitude", "baro_altitude", "geoaltitude")
        except (KeyError, ValueError) as e:
            print("saltato", n, e); continue
        ok = np.isfinite(t) & np.isfinite(lat) & np.isfinite(lon) & np.isfinite(alt)
        t, lat, lon, alt = t[ok], lat[ok], lon[ok], alt[ok]
        if len(t) < 600: continue
        usati += 1
        base_nome = os.path.splitext(os.path.basename(n))[0][:40].replace(" ", "_")
        alto = np.where(alt > 3000)[0]
        if len(alto) == 0: continue
        for tipo, sel in (("aereo_decollo", np.arange(0, alto[0])), ("aereo_avvicinamento", np.arange(alto[-1] + 1, len(t)))):
            if len(sel) < 60: continue
            i0 = sel[0] if tipo == "aereo_decollo" else sel[-1]
            x, y = enu(lat[sel], lon[sel], lat[i0], lon[i0])
            rs.append(scrivi_tratto(base, "aerei", "lhrzrh_%s_%s" % (base_nome, tipo[6:9]), tipo, t[sel], x, y, alt[sel] - alt[i0], 5.0, 5.0,
                                    {"origine": "punto piu' basso del tratto: lat %.5f, lon %.5f, quota %.0f m" % (lat[i0], lon[i0], alt[i0])},
                                    {"fonte": "El Ouanbi e Amellal, Cleaned ADS-B Trajectories (LHR-ZRH 2025), Zenodo 18916312; origine OpenSky Network", "licenza": "CC BY 4.0",
                                     "nota": "tratto sotto 3000 m; la fonte ha GIA' filtrato e interpolato a 1 Hz con spline cubiche: accelerazioni e virate sono lisciate dalla fonte"}))
    salva_riassunti(base, "aerei_zenodo", rs)


# ---------------------------------------------------------------- DRONI AD ALA FISSA: ALFA (CMU AirLab), Carbon Z T-28
def alfa(base):
    z = zipfile.ZipFile(os.path.join(base, "scaricati", "droni_alfa", "processed.zip"))
    nomi = sorted(n for n in z.namelist() if n.endswith("mavros-global_position-global.csv"))
    rs = []; scart = 0
    for n in nomi:
        t = []; lat = []; lon = []; alt = []
        f = io.TextIOWrapper(z.open(n), encoding="utf-8", newline="")
        h = f.readline().strip().split(",")
        it, il, io_, ia = h.index("%time"), h.index("field.latitude"), h.index("field.longitude"), h.index("field.altitude")
        for riga in f:
            c = riga.split(",")
            try:
                t.append(int(c[it]) / 1e9); lat.append(float(c[il])); lon.append(float(c[io_])); alt.append(float(c[ia]))
            except (ValueError, IndexError):
                continue
        t, lat, lon, alt = map(np.array, (t, lat, lon, alt))
        ok = np.isfinite(lat) & np.isfinite(lon) & np.isfinite(alt) & (np.abs(lat) > 1)
        t, lat, lon, alt = t[ok], lat[ok], lon[ok], alt[ok]
        if len(t) < 100:
            scart += 1; continue
        x, y = enu(lat, lon, lat[0], lon[0])
        seq = n.split("/")[-2]
        guasto = seq.split("_", 2)[2] if seq.count("_") >= 2 else ""
        rs.append(scrivi_tratto(base, "droni", "alfa_" + seq[8:].replace("-", ""), "ala_fissa_senza_pilota", t, x, y, alt - alt[0], 2.0, 3.0,
                                {"origine": "primo punto della sequenza: lat %.6f, lon %.6f, quota %.1f m" % (lat[0], lon[0], alt[0])},
                                {"fonte": "Keipour, Mousaei, Scherer, ALFA: A Dataset for UAV Fault and Anomaly Detection, CMU KiltHub, doi:10.1184/R1/12707963 (processed.zip, mavros/global_position/global)", "licenza": "CC BY 4.0",
                                 "sequenza": seq, "guasto_indotto_nella_sequenza": guasto,
                                 "nota": "posizione dal GNSS dell'autopilota di bordo; molte sequenze contengono un guasto indotto (motore, timone, alettoni, equilibratore): il moto dopo il guasto non e' quello nominale"}))
    print("sequenze", len(nomi), "scartate", scart)
    salva_riassunti(base, "droni_alfa", rs)


# ---------------------------------------------------------------- STATISTICHE
def wilson(k, n, zc=1.959964):
    if n == 0: return [None, None]
    p = k / n; d = 1 + zc * zc / n
    c = (p + zc * zc / (2 * n)) / d; h = zc * math.sqrt(p * (1 - p) / n + zc * zc / (4 * n * n)) / d
    return [max(0.0, c - h), min(1.0, c + h)]


def statistiche(base):
    d = os.path.join(base, "convertitori", "campioni")
    out = {"nota": "velocita' = modulo 3D derivato dalle posizioni; accelerazione = derivata del modulo (longitudinale); virata = derivata della rotta in pianta, solo sopra la velocita' minima. Finestra di derivazione per fonte: auto 1 s, multirotori 1 s, ala fissa senza pilota 2 s, treni 15 s, aerei 5 s (rullaggio 10 s).",
           "per_tipo": {}, "per_classe_tratti": {}}
    for fn in sorted(glob.glob(os.path.join(d, "*.npz"))):
        ch = os.path.basename(fn)[:-4]
        z = np.load(fn); meta = json.load(open(os.path.join(d, ch + "_tratti.json")))
        for tp in sorted(set(k.split("__")[1] for k in z.files)):
            v, a, om = z["v__" + tp], z["a__" + tp], z["om__" + tp]; om = np.abs(om[np.isfinite(om)])
            mt = [m for m in meta if m[2] == tp]
            q = lambda arr, p: (round(float(np.percentile(arr, p)), 3) if len(arr) else None)
            out["per_tipo"][ch + "/" + tp] = {
                "fonte": ch, "classe": mt[0][1], "tipo": tp, "tratti": len(mt), "campioni": int(len(v)),
                "durata_totale_s": round(sum(m[4] for m in mt), 1), "passo_mediano_s": round(float(np.median([m[5] for m in mt])), 3),
                "v_mediana": q(v, 50), "v_p95": q(v, 95), "v_max": round(float(v.max()), 2),
                "abs_a_mediana": q(np.abs(a), 50), "abs_a_p95": q(np.abs(a), 95), "acc_p95": q(a[a > 0], 95), "dec_p95": q(-a[a < 0], 95),
                "virata_mediana_gradi_s": q(om, 50), "virata_p95_gradi_s": q(om, 95), "campioni_virata": int(len(om)),
                "v_max_per_tratto": [round(m[6], 2) for m in mt]}
        for m in meta:
            out["per_classe_tratti"][m[1]] = out["per_classe_tratti"].get(m[1], 0) + 1
    # confronto con i profili ipotizzati (classi.json di f14), dove un profilo esiste; il contesto puo' essere diverso e lo si dice
    pc = os.path.join(base, "..", "..", "f14-classificazione", "01-profili", "classi.json")
    prof = {c["id"]: c for c in json.load(open(pc))["classi"]} if os.path.exists(pc) else {}
    mappa = {"aereo_rullaggio": ("aereo_rullaggio", "stesso contesto"), "multirotore": ("multirotore_lento", "stesso tipo; il profilo e' per il volo lento in area di lavoro"),
             "auto": ("auto_strada_urbana", "CONTESTO DIVERSO: il dato e' un'autostrada urbana congestionata"),
             "treno": ("treno_banchina", "CONTESTO DIVERSO: il dato e' in linea, il profilo e' in banchina")}
    out["confronto_profili"] = {}
    for k, s in out["per_tipo"].items():
        if s["tipo"] in mappa and mappa[s["tipo"]][0] in prof:
            pr = prof[mappa[s["tipo"]][0]]; n = s["tratti"]
            kk = sum(1 for vm in s["v_max_per_tratto"] if vm > pr["v_max"])
            out["confronto_profili"][k] = {"profilo": pr["id"], "contesto": mappa[s["tipo"]][1], "v_tip_profilo": pr["v_tip"], "v_max_profilo": pr["v_max"], "a_max_profilo": pr["a_max"], "dec_max_profilo": pr["dec_max"],
                                           "v_mediana_dati": s["v_mediana"], "v_p95_dati": s["v_p95"], "acc_p95_dati": s["acc_p95"], "dec_p95_dati": s["dec_p95"],
                                           "tratti_con_vmax_oltre_il_profilo": kk, "tratti": n, "frazione": round(kk / n, 3), "wilson95": [round(w, 3) for w in wilson(kk, n)]}
        else:
            out["confronto_profili"][k] = {"profilo": None, "nota": "nessun profilo in classi.json: da aggiungere; valori proposti = quelli misurati qui"}
    json.dump(out, open(os.path.join(base, "statistiche.json"), "w"), ensure_ascii=False, indent=1)
    for k, c in out["confronto_profili"].items():
        if c["profilo"]: print("PROFILO", k, c["profilo"], "v_max", c["v_max_profilo"], "oltre:", c["tratti_con_vmax_oltre_il_profilo"], "/", c["tratti"], c["wilson95"], "a_max", c["a_max_profilo"], "acc95", c["acc_p95_dati"], "dec95", c["dec_p95_dati"])
    print(json.dumps(out["per_classe_tratti"]))
    for k, s in out["per_tipo"].items():
        print("%-48s n=%3d camp=%7d passo=%5.2f v50=%6.2f v95=%6.2f vmax=%6.2f |a|50=%5.2f |a|95=%5.2f om50=%5.2f om95=%6.2f" % (
            k, s["tratti"], s["campioni"], s["passo_mediano_s"], s["v_mediana"], s["v_p95"], s["v_max"], s["abs_a_mediana"], s["abs_a_p95"],
            s["virata_mediana_gradi_s"] or 0, s["virata_p95_gradi_s"] or 0))


if __name__ == "__main__":
    {"auto": auto, "droni": droni, "treni": treni, "trajair": trajair, "live": live, "zenodo": zenodo, "alfa": alfa, "statistiche": statistiche}[sys.argv[1]](sys.argv[2])
