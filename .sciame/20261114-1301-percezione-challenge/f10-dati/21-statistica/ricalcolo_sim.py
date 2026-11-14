#!/usr/bin/env python3
"""sciame-statistico, f10/21-statistica — ricalcolo indipendente delle misure sul simulato.

Legge SOLO le uscite grezze della catena (20-validazione/uscite/<etichetta>/<sequenza>/{griglie.npz, fotogrammi.jsonl})
e la verità del simulatore (11-simulatore/sequenze/<sequenza>/verita.json). Non importa nessun modulo di
20-validazione, della catena o del simulatore. Scrive tabelle/sim_<etichetta>.json e stampa le tabelle.
Uso: <python> -I -B ricalcolo_sim.py sim | sim_p40
"""
import json
import math
import os
import re
import sys

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
F10 = os.path.dirname(QUI)
USC = os.path.join(F10, "20-validazione", "uscite")
SEQ = os.path.join(F10, "11-simulatore", "sequenze")
NON_OSS, LIBERO, OCCUPATO, IN_OMBRA = 0, 1, 2, 3          # verificato sotto contro i conteggi di fotogrammi.jsonl
CHI2_90 = 4.605
RNG = np.random.default_rng(14112026)


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def q(k, n):
    a, b = wilson(k, n)
    return f"{k}/{n} ({100 * a:.1f}–{100 * b:.1f} %)" if n else "0/0"


def boot(v, f=np.median, n=4000):
    v = np.asarray(v, dtype=float)
    if len(v) < 2:
        return (float("nan"), float("nan"))
    r = [f(v[RNG.integers(0, len(v), len(v))]) for _ in range(n)]
    return float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))


def leggi(et, nome):
    d = os.path.join(USC, et, nome)
    g = np.load(os.path.join(d, "griglie.npz"), allow_pickle=False)
    with open(os.path.join(d, "fotogrammi.jsonl"), encoding="utf-8") as f:
        righe = [json.loads(r) for r in f if r.strip()]
    with open(os.path.join(SEQ, nome, "verita.json"), encoding="utf-8") as f:
        ver = json.load(f)
    return g["stati"], g["possibile_presenza"], righe, ver


def codici_stato(stati, righe):
    """Controlla che 0,1,2,3 = non osservato, libero, occupato, in ombra, sui conteggi scritti dalla catena."""
    k = len(righe) // 2
    c = righe[k]["celle"]
    att = [c["non_osservato"], c["libero"], c["occupato"], c["in_ombra"]]
    return [int((stati[k] == i).sum()) for i in range(4)] == att


def classi_cella(ver, na=180, nr=30, fa=(0.0, 0.5, 1.0)):
    """Classe d'ombra di ogni cella polare (1° × 0,1 m) in NOVE punti (angoli, metà dei lati, centro), letta nella
    maschera cartesiana della verità col campione più vicino. tutta = i 9 punti in classe 1 o 3; parte = almeno uno.
    (Via mia: la validazione usa 25 punti interni; il simulatore dà anche una maschera polare, usata sotto.)"""
    c = ver["ombra_suolo"]["cartesiana"]
    m = np.array([[int(ch) for ch in riga] for riga in c["celle"]], dtype=np.uint8)
    x0, z0, p = c["x_m_centro_prima"], c["z_m_centro_prima"], c["passo_m"]
    fa = np.array(fa)
    az = np.radians(-90.0 + np.arange(na)[:, None, None, None] + fa[None, None, :, None])
    rr = (np.arange(nr)[None, :, None, None] + fa[None, None, None, :]) * 0.1
    x, z = np.sin(az) * rr, np.cos(az) * rr
    ix, iz = np.rint((x - x0) / p).astype(int), np.rint((z - z0) / p).astype(int)
    den = (ix >= 0) & (ix < m.shape[1]) & (iz >= 0) & (iz < m.shape[0])
    cl = np.where(den, m[np.clip(iz, 0, m.shape[0] - 1), np.clip(ix, 0, m.shape[1] - 1)], 2).reshape(na, nr, len(fa) ** 2)
    omb = (cl == 1) | (cl == 3)
    return omb.all(axis=2), omb.any(axis=2), cl


def polare_verita(ver, na=180, nr=30):
    """La maschera POLARE della verità riportata sulla griglia della catena (stesso passo; azimut −50…+50)."""
    p = ver["ombra_suolo"]["polare"]
    m = np.array([[int(ch) for ch in riga] for riga in p["celle"]], dtype=np.uint8)      # [distanza, azimut]
    out = np.full((na, nr), 2, dtype=np.uint8)
    a0 = int(round(p["azimut_gradi_centro_prima"] - 0.5 + 90))
    out[a0:a0 + m.shape[1], :] = m[:nr, :].T
    return out


def spigoli(ver):
    pan = [o for o in ver["ostacoli"] if o["id"] == "pannello"]
    if not pan:
        return None
    az = [math.degrees(math.atan2(x, z)) for x, z in pan[0]["vertici"]]
    return min(az), max(az)


def bordo_primo_ritorno(st):
    """Definizione scritta dalla validazione: colonne contigue allo 0° il cui primo «occupato» sta a 1,6–2,1 m."""
    occ = st == OCCUPATO
    primo = np.where(occ.any(axis=1), occ.argmax(axis=1), 99)
    pan = (primo >= 16) & (primo <= 20)
    if not (pan[89] or pan[90]):
        return None
    lo = hi = 89 if pan[89] else 90
    while lo > 0 and pan[lo - 1]:
        lo -= 1
    while hi < 179 and pan[hi + 1]:
        hi += 1
    return -90.0 + lo, -90.0 + hi + 1


def bordo_maschera(st, ir=24):
    """Variante mia (scritta DOPO le previsioni): la maschera com'è a 2,4 m, cioè le colonne contigue allo 0° che
    nell'anello 2,4–2,5 m sono «in ombra» od «occupato»."""
    m = (st[:, ir] == IN_OMBRA) | (st[:, ir] == OCCUPATO)
    if not (m[89] or m[90]):
        return None
    lo = hi = 89 if m[89] else 90
    while lo > 0 and m[lo - 1]:
        lo -= 1
    while hi < 179 and m[hi + 1]:
        hi += 1
    return -90.0 + lo, -90.0 + hi + 1


def traccia_vicina(riga, x, z, raggio=0.5):
    best, db = None, raggio
    for tr in riga["tracce"]:
        if tr["stato"] != "osservato" or not tr["misura_nel_ciclo"]:
            continue
        d = math.hypot(tr["ultima_misura"][0] - x, tr["ultima_misura"][1] - z)
        if d <= db:
            best, db = tr, d
    return best


def passaggio(nome, stati, pres, righe, ver):
    T = len(righe)
    fot = ver["fotogrammi"][:T]
    if not fot or not fot[0]["soggetti"]:
        return None
    s = [f["soggetti"][0] for f in fot]
    fr = np.array([a["frazione_visibile"] for a in s])
    X = np.array([a["x"] for a in s])
    Z = np.array([a["z"] for a in s])
    t = np.array([r["t"] for r in righe])
    nas = np.nonzero(fr < 0.02)[0]
    o = {"nome": nome, "T": T, "nascosti": int(len(nas))}
    # pannello detto «si muove»: una traccia non «in conferma», con l'ultima misura sul pannello e lontana dal soggetto
    pm = False
    for k, r in enumerate(righe):
        for tr in r["tracce"]:
            if tr["stato"] == "in_conferma" or tr["si_muove"] is not True:
                continue
            mx, mz = tr["ultima_misura"][0], tr["ultima_misura"][1]
            if abs(mx) <= 0.65 and 1.6 <= mz <= 2.0 and not (math.hypot(mx - X[k], mz - Z[k]) <= 0.5 and fr[k] >= 0.02):
                pm = True
    o["pannello_si_muove"] = pm
    if len(nas) == 0:
        return o
    k0, k1 = int(nas[0]), int(nas[-1])
    o["t_nascosto_s"] = float(t[k1] - t[k0] + (t[1] - t[0]))
    voti, voti_d = {}, {}
    ultima_prima = None
    scarti = []
    for k in range(k0):
        tr = traccia_vicina(righe[k], X[k], Z[k])
        if tr is None:
            continue
        ultima_prima = tr["id"]
        if fr[k] >= 0.98:
            voti[tr["id"]] = voti.get(tr["id"], 0) + 1
    idp = max(voti, key=lambda i: (voti[i], -i)) if voti else None
    o["id_prima"] = idp
    # definizione ORIGINALE (16:48): primo fotogramma dopo l'ombra con frazione ≥ 0,5 e una traccia entro 0,5 m
    primo_dopo = None
    for k in range(k1 + 1, T):
        if fr[k] >= 0.5:
            tr = traccia_vicina(righe[k], X[k], Z[k])
            if tr is not None:
                if primo_dopo is None:
                    primo_dopo = tr["id"]
                if fr[k] >= 0.98:
                    voti_d[tr["id"]] = voti_d.get(tr["id"], 0) + 1
    idd = max(voti_d, key=lambda i: (voti_d[i], -i)) if voti_d else None
    o["id_dopo"] = idd
    o["ricompare"] = bool(any(fr[k] >= 0.5 for k in range(k1 + 1, T)))
    o["stessa_originale"] = bool(ultima_prima is not None and primo_dopo == ultima_prima)
    o["stessa"] = bool(idp is not None and idd == idp)
    oss_nasc, riagg_nasc = 0, 0
    cella = {"presenza": 0, "occupato": 0, "non_osservato": 0, "in_ombra_senza_avviso": 0, "libero": 0, "fuori": 0}
    # scarto sistematico centro misurato − verità sui fotogrammi interi prima dell'ombra (stima sullo STESSO passaggio)
    if idp is not None:
        for k in range(k0):
            for tr in righe[k]["tracce"]:
                if tr["id"] == idp and tr["misura_nel_ciclo"] and not tr["misura_tagliata"] and fr[k] >= 0.98:
                    d = math.hypot(X[k], Z[k])
                    ex, ez = tr["ultima_misura"][0] - X[k], tr["ultima_misura"][1] - Z[k]
                    scarti.append(((ex * X[k] + ez * Z[k]) / d, (ex * Z[k] - ez * X[k]) / d))
    orad, otra = (np.mean(scarti, axis=0) if scarti else (0.0, 0.0))
    o["scarto_rad_tra_m"] = [float(orad), float(otra)]
    o["sigma_rad_tra_m"] = [float(v) for v in np.std(scarti, axis=0)] if len(scarti) >= 4 else None
    err, err_grezzo, in90, tau_l = [], [], [], []
    for k in nas:
        tr = next((a for a in righe[k]["tracce"] if a["id"] == idp), None) if idp is not None else None
        if tr is not None and tr["stato"] == "osservato":
            oss_nasc += 1
        riagg_nasc += sum(1 for e in righe[k]["eventi"] if e["tipo"] == "riaggancio" and e.get("id") == idp)
        ia = math.floor(math.degrees(math.atan2(X[k], Z[k])) + 90.0)
        ir = math.floor(math.hypot(X[k], Z[k]) / 0.1)
        if not (0 <= ia < 180 and 0 <= ir < 30):
            cella["fuori"] += 1
        elif pres[k][ia, ir]:
            cella["presenza"] += 1
        else:
            cella[{OCCUPATO: "occupato", NON_OSS: "non_osservato", IN_OMBRA: "in_ombra_senza_avviso",
                   LIBERO: "libero"}[int(stati[k][ia, ir])]] += 1
        if tr is not None and "previsione_diagnostica" in tr:
            d = tr["previsione_diagnostica"]
            dd = math.hypot(X[k], Z[k])
            mx = X[k] + orad * X[k] / dd + otra * Z[k] / dd
            mz = Z[k] + orad * Z[k] / dd - otra * X[k] / dd
            e = np.array([d["x"] - mx, d["z"] - mz])
            cxx, cxz, czz = d["covarianza"]
            err.append(float(np.hypot(*e)))
            err_grezzo.append(float(math.hypot(d["x"] - X[k], d["z"] - Z[k])))
            in90.append(bool(e @ np.linalg.solve(np.array([[cxx, cxz], [cxz, czz]]), e) <= CHI2_90))
            tau_l.append(float(t[k] - t[k0]))
    o.update(osservato_a_nascosto=oss_nasc, riagganci_a_nascosto=riagg_nasc, cella_centro=cella,
             err=err, err_grezzo=err_grezzo, in90=in90, tau=tau_l)
    o["pulita"] = bool(o["stessa"] and oss_nasc == 0 and riagg_nasc == 0)
    return o


def gruppo(nome):
    p = nome.split("__")
    return p[0] + "__" + p[1] + ("__filtri" if nome.endswith("__filtri") else "")


def main():
    et = sys.argv[1] if len(sys.argv) > 1 else "sim"
    rad = os.path.join(USC, et)
    nomi = sorted(n for n in os.listdir(rad) if os.path.isdir(os.path.join(rad, n)))
    ris = {"etichetta": et, "sequenze": len(nomi), "k014": [], "ombra": [], "passaggi": []}
    cod_ok, fot_tot = 0, 0
    for n in nomi:
        stati, pres, righe, ver = leggi(et, n)
        cod_ok += codici_stato(stati, righe)
        fot_tot += stati.shape[0]
        T = stati.shape[0]
        tutta, parte, cl = classi_cella(ver)
        tutta25, parte25, _ = classi_cella(ver, fa=(0.1, 0.3, 0.5, 0.7, 0.9))     # i 25 punti interni della validazione
        pol = polare_verita(ver)
        pol_omb = (pol == 1) | (pol == 3)
        lib = stati == LIBERO
        per_cella = lib[:, tutta].sum(axis=0) if tutta.any() else np.zeros(0, int)
        ris["k014"].append({
            "nome": n, "fotogrammi": T, "celle_tutte_ombra": int(tutta.sum()), "celle_bordo": int((parte & ~tutta).sum()),
            "libero_tutta": int(lib[:, tutta].sum()), "libero_bordo": int(lib[:, parte & ~tutta].sum()),
            "celle_tutte25": int(tutta25.sum()), "libero_tutte25": int(lib[:, tutta25].sum()),
            "celle_bordo25": int((parte25 & ~tutta25).sum()), "libero_bordo25": int(lib[:, parte25 & ~tutta25].sum()),
            "celle_polare_ombra": int(pol_omb.sum()), "libero_polare_ombra": int(lib[:, pol_omb].sum()),
            "fotogrammi_con_libero_tutta": int(lib[:, tutta].any(axis=1).sum()) if tutta.any() else 0,
            "celle_distinte_con_libero": int((per_cella > 0).sum()),
            "ostacoli": sorted(str(o_["id"]) for o_ in ver.get("ostacoli", [])),
        })
        sp = spigoli(ver)
        if sp is not None and "__pannello_" in n:
            es, ed, ms, md, senza = [], [], [], [], 0
            for k, f in enumerate(ver["fotogrammi"][:T]):
                if any(a["frazione_visibile"] >= 0.02 for a in f["soggetti"]):
                    continue
                b = bordo_primo_ritorno(stati[k])
                if b is None:
                    senza += 1
                else:
                    es.append((sp[0] - b[0]) * math.pi / 180 * 240)
                    ed.append((b[1] - sp[1]) * math.pi / 180 * 240)
                b2 = bordo_maschera(stati[k])
                if b2 is not None:
                    ms.append((sp[0] - b2[0]) * math.pi / 180 * 240)
                    md.append((b2[1] - sp[1]) * math.pi / 180 * 240)
            if es:
                ris["ombra"].append({"nome": n, "fotogrammi": len(es), "pannello_non_visto": senza,
                                     "sin": [round(v, 2) for v in es], "des": [round(v, 2) for v in ed],
                                     "sin_maschera": [round(v, 2) for v in ms], "des_maschera": [round(v, 2) for v in md]})
        if "__pannello_" in n and "vuoto" not in n:
            p = passaggio(n, stati, pres, righe, ver)
            if p is not None:
                ris["passaggi"].append(p)
    os.makedirs(os.path.join(QUI, "tabelle"), exist_ok=True)
    with open(os.path.join(QUI, "tabelle", f"sim_{et}.json"), "w", encoding="utf-8") as f:
        json.dump(ris, f, ensure_ascii=False)

    print(f"# {et}: {len(nomi)} sequenze, {fot_tot} fotogrammi; codici di stato coerenti in {cod_ok}/{len(nomi)}")
    # ---------- K-014
    print("\n== K-014: «libero» in celle tutte dentro l'ombra vera (9 punti) ==")
    for filtri in (False, True):
        K = [m for m in ris["k014"] if m["nome"].endswith("__filtri") == filtri and m["celle_tutte_ombra"] > 0]
        den = sum(m["celle_tutte_ombra"] * m["fotogrammi"] for m in K)
        num = sum(m["libero_tutta"] for m in K)
        denb = sum(m["celle_bordo"] * m["fotogrammi"] for m in K)
        numb = sum(m["libero_bordo"] for m in K)
        denp = sum(m["celle_polare_ombra"] * m["fotogrammi"] for m in K)
        nump = sum(m["libero_polare_ombra"] for m in K)
        nseq = sum(1 for m in K if m["libero_tutta"] > 0)
        K25 = [m for m in ris["k014"] if m["nome"].endswith("__filtri") == filtri and m["celle_tutte25"] > 0]
        print(f"   definizione a 25 punti interni (quella della validazione): sequenze {len(K25)}; libero "
              f"{sum(m['libero_tutte25'] for m in K25)} su {sum(m['celle_tutte25'] * m['fotogrammi'] for m in K25)}; sequenze con ≥1: "
              f"{sum(1 for m in K25 if m['libero_tutte25'] > 0)}; bordo {sum(m['libero_bordo25'] for m in K25)} su "
              f"{sum(m['celle_bordo25'] * m['fotogrammi'] for m in K25)}; " + "; ".join(f"{m['nome']}: {m['libero_tutte25']}" for m in K25 if m['libero_tutte25'] > 0))
        print(f"filtri={filtri}: sequenze con ombra {len(K)}; libero {num} su {den} celle·fot; sequenze con ≥1: {q(nseq, len(K))}; "
              f"bordo {numb} su {denb}; maschera polare della verità (classe 1/3 al centro): {nump} su {denp}")
        for m in K:
            if m["libero_tutta"] > 0:
                print("   ", m["nome"], m["libero_tutta"], "celle·fot in", m["fotogrammi_con_libero_tutta"], "fotogrammi,",
                      m["celle_distinte_con_libero"], "celle distinte")
        if not filtri:
            gr = {}
            for m in K:
                gr.setdefault(gruppo(m["nome"]), []).append(m)
            geo = {}
            for m in K:
                geo.setdefault((tuple(m["ostacoli"]), m["celle_tutte_ombra"]), []).append(m["nome"])
            print(f"   combinazioni distinte profilo×livello×scena: {len(gr)}; geometrie d'ombra distinte (ostacoli, n. celle): {len(geo)}")
            for g_, v in sorted(geo.items(), key=lambda kv: -len(kv[1])):
                print("      ", len(v), "sequenze;", g_[1], "celle tutte in ombra; ostacoli", ",".join(g_[0])[:80], "; es.", v[0])
    # ---------- ombra
    print("\n== bordo d'ombra (cm a 2,4 m; + = stimata più larga) ==")
    for lab, filt in (("d435i_nom", lambda n: n.startswith("d435i_nom") and not n.endswith("__filtri")),
                      ("d455_nom", lambda n: n.startswith("d455_nom")), ("g335_nom", lambda n: n.startswith("g335_nom")),
                      ("d435i_lim", lambda n: n.startswith("d435i_lim"))):
        O = [m for m in ris["ombra"] if filt(m["nome"])]
        if not O:
            continue
        for chi in ("", "_maschera"):
            tutti = np.array([v for m in O for lato in ("sin", "des") for v in m[lato + chi]])
            if len(tutti) == 0:
                continue
            medseq = [np.median(m[lato + chi]) for m in O for lato in ("sin", "des") if m[lato + chi]]
            ok20 = sum(1 for m in O if all(m[l + chi] and np.percentile(m[l + chi], 5) >= -20 and np.percentile(m[l + chi], 95) <= 20
                                           for l in ("sin", "des")))
            val, cnt = np.unique(np.round(tutti, 1), return_counts=True)
            lv = "; ".join(f"{v:+.1f}: {100 * c / len(tutti):.1f} %" for v, c in zip(val, cnt)) if len(val) <= 12 else f"{len(val)} valori"
            sm = np.mean([np.mean(m["sin" + chi]) for m in O if m["sin" + chi]])
            dm = np.mean([np.mean(m["des" + chi]) for m in O if m["des" + chi]])
            print(f"{lab}{chi or '_primo_ritorno'}: {len(O)} sequenze, {sum(len(m['sin' + chi]) for m in O)} fotogrammi; "
                  f"mediana delle mediane {np.median(medseq):+.1f}; min {tutti.min():+.1f}; max {tutti.max():+.1f}; "
                  f"media sin {sm:+.2f} des {dm:+.2f}; sequenze con 5°–95° entro ±20: {q(ok20, len(O))}; "
                  f"fotogrammi·lato sotto 0: {int((tutti < 0).sum())}; pannello non visto: {sum(m['pannello_non_visto'] for m in O)}\n      livelli: {lv}")
    # ---------- passaggi
    print("\n== passaggi: identità, continuità, pannello «si muove» ==")
    P = [p for p in ris["passaggi"] if p["nascosti"] > 0]
    gr = {}
    for p in P:
        gr.setdefault(gruppo(p["nome"]), []).append(p)
    for g_, ps in sorted(gr.items()):
        ric = [p for p in ps if p["ricompare"]]
        n = len(ric)
        disp = [p for p in ric if re.search(r"__s\d[13579]$", p["nome"])]
        pari = [p for p in ric if re.search(r"__s\d[02468]$", p["nome"])]
        cc = {k: sum(p["cella_centro"][k] for p in ps) for k in ps[0]["cella_centro"]}
        tutto_pres = sum(1 for p in ps if p["cella_centro"]["presenza"] == p["nascosti"])
        print(f"{g_}: N {len(ps)} (ricompare {n}); stessa {q(sum(p['stessa'] for p in ric), n)}; stessa (def. originale) "
              f"{sum(p['stessa_originale'] for p in ric)}; PULITA {q(sum(p['pulita'] for p in ric), n)}; dispari "
              f"{q(sum(p['pulita'] for p in disp), len(disp))}; pari {sum(p['pulita'] for p in pari)}/{len(pari)}; "
              f"«osservato» a nascosto in {sum(1 for p in ps if p['osservato_a_nascosto'])} passaggi; pannello «si muove» "
              f"{q(sum(p['pannello_si_muove'] for p in ps), len(ps))}; centro nascosto: {cc}; passaggi col centro SEMPRE in presenza "
              f"{q(tutto_pres, len(ps))}; nascosto {np.median([p['t_nascosto_s'] for p in ps]):.2f} s")
    for lab, rx in (("d435i_nom a12+a05+b", r"^d435i_nom__pannello_(a12|a05|b)__s\d\d$"),):
        ps = [p for p in P if re.search(rx, p["nome"])]
        disp = [p for p in ps if re.search(r"[13579]$", p["nome"])]
        pari = [p for p in ps if re.search(r"[02468]$", p["nome"])]
        print(f"{lab}: tutti {q(sum(p['pulita'] for p in ps), len(ps))}; dispari {q(sum(p['pulita'] for p in disp), len(disp))}; "
              f"pari {q(sum(p['pulita'] for p in pari), len(pari))}; pannello «si muove» {q(sum(p['pannello_si_muove'] for p in ps), len(ps))}; "
              f"«osservato» a nascosto {sum(1 for p in ps if p['osservato_a_nascosto'])}")
    # ---------- errore e copertura per tempo d'occlusione (unità: il passaggio)
    print("\n== previsione a soggetto nascosto: errore (m) per fascia di tempo, mediana fra i passaggi [IC bootstrap sui passaggi; N] ==")
    fasce = [(0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1), (1, 2), (2, 3), (3, 99)]
    for caso in ("a12", "a05", "b"):
        ps = [p for p in P if re.search(rf"^d435i_nom__pannello_{caso}__s\d\d$", p["nome"])]
        for chiave in ("err", "err_grezzo"):
            celle = []
            for a, b in fasce:
                v = [np.mean([e for e, tt in zip(p[chiave], p["tau"]) if a <= tt < b]) for p in ps
                     if any(a <= tt < b for tt in p["tau"])]
                if v:
                    lo, hi = boot(v)
                    celle.append(f"{np.median(v):.2f} [{lo:.2f}–{hi:.2f}; {len(v)}]")
                else:
                    celle.append("—")
            print(f"{caso} {chiave}: " + " | ".join(celle))
        cop = [np.mean(p["in90"]) for p in ps if p["in90"]]
        tutti = sum(sum(p["in90"]) for p in ps)
        nt = sum(len(p["in90"]) for p in ps)
        if cop:
            print(f"   copertura ellisse 90 %: passaggi con previsioni {len(cop)}/{len(ps)}; media per passaggio {np.mean(cop):.3f}; "
                  f"minimo {min(cop):.2f}; passaggi con copertura 1,00: {sum(1 for c in cop if c == 1)}; fotogrammi {tutti}/{nt}")
        sg = np.array([p["sigma_rad_tra_m"] for p in ps if p.get("sigma_rad_tra_m")])
        sc = np.array([p["scarto_rad_tra_m"] for p in ps if p.get("sigma_rad_tra_m")])
        if len(sg):
            lo, hi = boot(sg[:, 0])
            print(f"   centro in moto: sigma radiale mediana {100 * np.median(sg[:, 0]):.2f} cm [{100 * lo:.2f}–{100 * hi:.2f}], trasversale "
                  f"{100 * np.median(sg[:, 1]):.2f} cm; scarto radiale {100 * np.median(sc[:, 0]):.1f} cm; N {len(sg)}")


if __name__ == "__main__":
    main()
